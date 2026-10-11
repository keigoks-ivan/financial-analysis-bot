你是 DD 管線 v20 的判斷層閘（gate），標的 3167.TW（20261011）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（25 條）
- `f_kpi0_ifrs`（q1_business）｜營收（合併，IFRS）＝2859.2 百萬TWD｜期間與口徑：Q2 2026（季末 2026-06-30，公告日未查證，台股法定期限 2026-08-14）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：yfinance quarterly_income_stmt／cashflow（對應 MOPS 合併財報；台灣公司無 IR 英文新聞稿，財報日未能以公司新聞稿確認）（numbers.latest_quarter_kpis.items[0]，as_of Q2 2026（季末 2026-06-30，公告日未查證，台股法定期限 2026-08-14））
- `f_kpi1_ifrs_non_gaap`（q1_business）｜營業利益／利益率（IFRS，台股無 Non-GAAP，兩項同口徑）＝833.5 百萬TWD（利益率 29.15%）｜期間與口徑：Q2 2026（季末 2026-06-30，公告日未查證，台股法定期限 2026-08-14）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：yfinance quarterly_income_stmt／cashflow（對應 MOPS 合併財報；台灣公司無 IR 英文新聞稿，財報日未能以公司新聞稿確認）（numbers.latest_quarter_kpis.items[1]，as_of Q2 2026（季末 2026-06-30，公告日未查證，台股法定期限 2026-08-14））
- `f_kpi2`（q1_business）｜毛利率＝44.2 %｜期間與口徑：Q2 2026（季末 2026-06-30，公告日未查證，台股法定期限 2026-08-14）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：yfinance quarterly_income_stmt／cashflow（對應 MOPS 合併財報；台灣公司無 IR 英文新聞稿，財報日未能以公司新聞稿確認）；uanalyze.com.tw 報導交叉（numbers.latest_quarter_kpis.items[2]，as_of Q2 2026（季末 2026-06-30，公告日未查證，台股法定期限 2026-08-14））
- `f_kpi5_backlog`（q1_business）｜在手訂單 backlog＝7500 百萬TWD（逾）｜期間與口徑：Q2 2026（季末 2026-06-30，公告日未查證，台股法定期限 2026-08-14）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：uanalyze.com.tw 2026 年報導（媒體引述公司，非 IR 原文）（numbers.latest_quarter_kpis.items[5]，as_of Q2 2026（季末 2026-06-30，公告日未查證，台股法定期限 2026-08-14））
- `f_kpi6`（q1_business）｜月產能（設備台數）＝400 台／月（2026 年；2025 年底約 300，Q4 另加約 50 台委外）｜期間與口徑：Q2 2026（季末 2026-06-30，公告日未查證，台股法定期限 2026-08-14）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：uanalyze.com.tw 報導（媒體引述公司）（numbers.latest_quarter_kpis.items[6]，as_of Q2 2026（季末 2026-06-30，公告日未查證，台股法定期限 2026-08-14））
- `f_peer_3167_tw_gross_margin_pct`（q2_moat）｜3167.TW 毛利率＝42.4 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.3167.TW.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_3167_tw_operating_margin_pct`（q2_moat）｜3167.TW 營業利益率＝24.81 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.3167.TW.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_3167_tw_fcf_margin_pct`（q2_moat）｜3167.TW FCF 利潤率＝9.67 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.3167.TW.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_6664_two_gross_margin_pct`（q2_moat）｜6664.TWO 毛利率＝51.23 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.6664.TWO.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_6664_two_fcf_margin_pct`（q2_moat）｜6664.TWO FCF 利潤率＝27.09 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.6664.TWO.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_6187_two_gross_margin_pct`（q2_moat）｜6187.TWO 毛利率＝53.27 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.6187.TWO.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_kpi3`（q4_capital）｜自由現金流（營業現金流−資本支出）＝262.2 百萬TWD（占營收 9.2%）｜期間與口徑：Q2 2026（季末 2026-06-30，公告日未查證，台股法定期限 2026-08-14）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：yfinance quarterly_income_stmt／cashflow（對應 MOPS 合併財報；台灣公司無 IR 英文新聞稿，財報日未能以公司新聞稿確認）（numbers.latest_quarter_kpis.items[3]，as_of Q2 2026（季末 2026-06-30，公告日未查證，台股法定期限 2026-08-14））
- `f_kpi4_sbc`（q4_capital）｜SBC 占營業利益＝1.16 %（SBC 9.6 百萬TWD）｜期間與口徑：Q2 2026（季末 2026-06-30，公告日未查證，台股法定期限 2026-08-14）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：yfinance quarterly_income_stmt／cashflow（對應 MOPS 合併財報；台灣公司無 IR 英文新聞稿，財報日未能以公司新聞稿確認）（numbers.latest_quarter_kpis.items[4]，as_of Q2 2026（季末 2026-06-30，公告日未查證，台股法定期限 2026-08-14））
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝0.371 %｜期間與口徑：2026-10-11／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-10-11）
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝1055.0 USD｜期間與口徑：2026-10-08（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-10-08（RTH 收盤，UTC））
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝74.66 x｜期間與口徑：2026-10-08（RTH 收盤，UTC）／4 個年度端點內的分位＝19.7｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-10-08（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝19.7 %｜期間與口徑：2026-10-08（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-10-08（RTH 收盤，UTC））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝12.26 x｜期間與口徑：2026-10-08（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-10-08（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝100.0 %｜期間與口徑：2026-10-08（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-10-08（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝12.25 x｜期間與口徑：2026-10-08（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-10-08（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝100.0 %｜期間與口徑：2026-10-08（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-10-08（RTH 收盤，UTC））
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝84.05 %｜期間與口徑：2026-10-08（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^TWII｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-10-08（RTH 收盤，UTC））
- `f_ma_w52`（q5_valuation）｜52 週均線＝524.36 USD｜期間與口徑：2026-10-11／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-10-11）
- `f_ma_w104`（q5_valuation）｜104 週均線＝324.1 USD｜期間與口徑：2026-10-11／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-10-11）
- `f_ma_w250`（q5_valuation）｜250 週均線＝165.88 USD｜期間與口徑：2026-10-11／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-10-11）

### findings_digest 中方向為負或來源衝突的條目（3 條）
- `competitive_share_entrants#1`（competitive_share_entrants｜方向 -｜狀態 ok）：分析指出高階切割／鑽孔設備瓶頸在歐美大廠掌握的控制器，大量 2004 年起自行開發台灣製控制器與軟體；文中提及曾受中國廠商抄襲與競爭，公司轉向 AI 伺服器鑽孔機與半導體量測設備。無具體競爭對手名單或市占數字。
  - 來源：財訊（moneyweekly）大量報導（as_of 2026-09-30）｜affects：moat_trend、decision_inputs.bear
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：2025 年大量科技區域營收分布：中國 68.7%、東南亞 21.7%、台灣 9.6%（第三方 AI 摘要，非公司原文）
  - 來源：poorstock.com 大量(3167) 2026/09/04 法說會 AI 摘要（as_of 2026-09-04）｜affects：decision_inputs.bear、thesis.R
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：摘要列出風險：易受中國宏觀不確定性及美中半導體管制政策波及，須留意地緣政治與中國 PCB 廠資本支出週期
  - 來源：poorstock.com 大量(3167) 2026/09/04 法說會 AI 摘要（as_of 2026-09-04）｜affects：decision_inputs.bear、thesis.R、triggers

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/3167.TW_20261011/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":2184,"bear_5y_price":240,"p_bull_pct":25,"p_bear_pct":30,"upside_5y_pct":-33.3,"ev5y_pct":-11.4,"irr_base_pct":-7.8,"asym_ratio":1.2,"scenario_tree":{"terminal_label":"FY2030E","start":{"eps":14.13,"pe":74.66,"basis":"近四季（至 2026-06-30）每股盈餘＝判斷日股價 1,055 元 ÷ trailing 本益比 74.66 倍；終端倍數同為當年度實際每股盈餘口徑。"},"eps":{"bull":[31,52,64,70,78],"base":[29,44,42,26,32],"bear":[27,34,18,10,16]},"pe":{"bull":28,"base":22,"bear":15},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0.371,"net_buyback":0},"second_stage":{"bull_cagr_pct":15,"base_cagr_pct":8},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

[本次無舊逐字稿摘錄]

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 3 | 3 |
| customer_second_source | none | 0 | 3 |
| customer_concentration_credit | none | 1 | 2 |
| supply_demand_durability | found | 4 | 2 |
| regulatory_antitrust | none | 0 | 2 |
| reg_tariff_export | none | 0 | 3 |
| geo_supply_chain | found | 3 | 2 |
| end_markets | found | 5 | 3 |
| substitute_technology | found | 3 | 3 |
| channel_business_model_shift | found | 2 | 2 |
| capital_markets_pricing | none | 0 | 2 |
| major_events | none | 0 | 3 |

未涵蓋／不適用軸的查詢詞原文（供判相關性）：
- **customer_second_source**（none）：3167 大量科技 最大客戶 第二供應商 OR 自製 2026；3167.TW largest customer second-source OR in-house 2026；大量科技 PCB 鑽孔機 客戶集中 競爭對手 日本 Tungaloy OR 自製 OR 二供 2026
- **customer_concentration_credit**（none）：大量科技 3167 主要客戶 營收占比 客戶集中 2026；大量 3167 PCB 設備 客戶 欣興 臻鼎 資本支出 2026
- **regulatory_antitrust**（none）：3167 大量科技 反壟斷 OR 公平會 OR 監管 2026；3167.TW Tera Autotech regulation OR antitrust OR export control 2026
- **reg_tariff_export**（none）：3167 大量科技 關稅 出口管制 2026；3167.TW tariff section 232 2026 PCB equipment；大量科技 3167 中國 客戶 營收 關稅 美國 影響
- **capital_markets_pricing**（none）：3167.TW 大量 目標價 分析師 2026；3167.TW analyst consensus guidance 2026
- **major_events**（none）：大量科技 3167 併購 收購 2025 2026；大量科技 3167 訴訟 重大訊息；大量科技 3167 調查 重編 財報 更正

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"status":"no_prior_dd"}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"3167.TW","date":"2026-10-11","schema":"v15.0","contract":"v19","company_name":"大量科技"},"oneliner":"AI 伺服器板帶動高階背鑽機訂單滿到 2027 年、營收年增逾一倍，但設備訂單跟著客戶擴產循環走；現價約 36 倍前瞻本益比把高峰獲利當常態，等回到 500 元附近再評估。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/3167.TW_20261011/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/3167.TW_20261011/scenario.json","answers":{"q1_business":{"verdict":"賺 PCB 廠擴產的錢：約九成營收是 PCB 鑽孔與成型設備，錢卡在 AI 伺服器板層數升級後的高階背鑽機這一節點；產業在過熱期，供需屬週期性，客戶擴產完成後會反轉。","reasoning":"2026 年第二季營收 28.59 億元、毛利率 44.2%、營益率 29.15%。2025 年上半年 PCB 設備約占九成、半導體約一成，半導體事業已於 2026-08-01 分拆為百分之百持有的大量先進智能。錢卡在 AI 伺服器板層數升級後的高階背鑽機：一般鑽孔與成型機交期由約 45 天拉長到約 6 個月，季末在手訂單逾 75 億元，約當第二季營收 2.6 季。產業時鐘判在過熱期，依據是供給端而非股價：毛利率由 2022 年 25.1% 升到 44.2%，交期拉長約四倍，公司月產能 300 台、400 台、500 台連續擴並加開 50 台委外，20 家以上中國 PCB 廠同步擴產，供給正在追需求。供需屬週期性將反轉：AI 板升級帶來的需求是真的，但設備訂單吃的是客戶的產能增量，客戶擴產完成後訂單會回落，2023 年營收年減 45.5% 是前例。單點依賴在地區：2025 年約 68.7% 營收來自中國（第三方法說摘要，非公司原文），屬集中度風險；前幾大客戶占比未揭露，只點名金像電、瀚宇博。本季沒有逐字稿，管理層過去的財測與承諾無從對照。","fact_refs":["f_kpi0_ifrs","f_kpi1_ifrs_non_gaap","f_kpi2","f_kpi5_backlog","f_kpi6"],"verdict_values":{"revenue_quality":"設備一次性銷售、接單生產，沒有經常性收入；季末在手訂單逾 75 億元，約當第二季營收 2.6 季，能見度高但跟著客戶擴產循環。","unit_econ_note":"月產能 2026 年 400 台以上、2027 年規劃 500 台；單價與台數拆分事實表未涵蓋。","archetype":{"primary":"循環/商品","secondary":null,"confidence":"高","fingerprint":"營收 2023 年年減 45.5%、2024 與 2025 年各約倍增；營益率由 5.1% 跌到 −6.2% 再升到 2026 年第二季 29.2%，隨客戶擴產循環大幅擺盪。"},"industry":{"clock_phase":"III","sd_verdict_source":"週期性將反轉：設備訂單取決於客戶產能增量，交期約 6 個月、20 家以上中國 PCB 廠同步擴產，券商稱缺口 2027 年最大、瓶頸延續到 2027 年底。","bargaining":{"up":"上游關鍵是控制器，原由歐美大廠掌握，公司 2004 年起自製控制器與軟體；玻纖、鎢鋼棒短缺影響的是客戶擴產節奏。","down":"下游是 20 家以上擴產中的 PCB 廠，買方分散；點名客戶有金像電、瀚宇博，前幾大客戶占比未揭露。","geo":"2025 年中國約 68.7%、東南亞 21.7%、台灣 9.6%（第三方法說摘要）。"},"profit_pool_dir":"AI 板主流層數由 24–28 層升到 40 層以上，鑽孔是 PCB 設備缺口最大的環節，短缺期利潤池流向鑽孔設備；缺口補上後會回流 PCB 廠。","tam_table":{"expanded":false,"reason":"設備需求取決於客戶產能增量而非終端滲透率；鑽孔設備市場規模與公司份額事實表未涵蓋；兩則高盛 2027 年 AI PCB 規模數字（266 億與 380 億美元）口徑不一，不作承重。"}}}},"q2_moat":{"verdict":"護城河 C 級、方向穩定：自製控制器與高階背鑽帶來領先，但定價力隨循環大幅擺盪，中國同業在中階市場的在地化壓住上限。","reasoning":"機制是自製控制器加高階背鑽：公司 2004 年起自行開發控制器與軟體，避開歐美大廠掌握的控制器瓶頸，法人稱其在背鑽機握有高份額，但沒有數字。執行面在擴大：月產能由 2025 年底約 300 台擴到 400 台以上，毛利率由 2022 年 25.1% 升到 2026 年第二季 44.2%。定價面沒有跨循環的證據：2023 年營收年減 45.5% 時營益率跌到 −6.2%；近四季毛利率 42.4%，仍低於 6664.TWO 的 51.2% 與 6187.TWO 的 53.3%，自由現金流率 9.7% 遠低於 6664.TWO 的 27.1%。中國中階機械鑽孔機國產化率已逾七成，公司曾遭中國廠商抄襲；高速主軸機種國產化 15–20%、UV 雷射 5–10%，高階仍守得住。執行擴大與定價受壓相抵，方向判穩定；執行 7 分、定價 5 分，等級 C。同業投入資本與份額事實表未涵蓋，無法算報酬率差距。","fact_refs":["f_peer_3167_tw_gross_margin_pct","f_peer_3167_tw_operating_margin_pct","f_peer_3167_tw_fcf_margin_pct","f_peer_6664_two_gross_margin_pct","f_peer_6664_two_fcf_margin_pct","f_peer_6187_two_gross_margin_pct","f_kpi2","f_kpi6"],"verdict_values":{"moat":{"mechanism":"自 2004 年自製控制器與軟體，避開歐美大廠掌握的控制器瓶頸；高階 CCD 背鑽機在 AI 伺服器板層數升級中取得高份額（法人說法，無數字）。","execution":7,"pricing":5,"grade":"C","trend":"→","trend_evidence":"毛利率由 2022 年 25.1% 升到 2026 年第二季 44.2%，但近四季 42.4% 仍低於 6664.TWO 的 51.2% 與 6187.TWO 的 53.3%；2023 年營益率 −6.2% 顯示定價力不跨循環；份額方向無數字可證，執行面擴大與中國在地化壓價相抵，判穩定。","competitor_notes":[{"name":"6664.TWO","strategy_note":"毛利率 51.2%、營益率 33.8%、自由現金流率 27.1%，三項都高於本公司，同組對照下本公司的現金轉換落後最明顯。"},{"name":"2467.TW","strategy_note":"毛利率 46.8% 高於本公司，但營益率 21.7% 較低、自由現金流率 −7.4%，擴產吃現金的情形比本公司更重。"},{"name":"3583.TW","strategy_note":"毛利率 35.8%、營益率 14.4% 都低於本公司，自由現金流率 19.1% 反而較高，獲利層級不如本公司但現金較穩。"},{"name":"6187.TWO","strategy_note":"毛利率 53.3% 為組內最高、研發密度 13.3%，營益率 28.9% 高於本公司近四季 24.8%，定價力明顯較強。"}],"spread_notes":null,"peer_na_reason":"同業投入資本與報酬率事實表未涵蓋，改用利潤率比較；直接鑽孔機競品與份額不在對照組內。","threats":[{"level":"🔴","text":"中國廠商抄襲與在地化：中階機械鑽孔機國產化率已逾七成，高速主軸機種 15–20%；若向高階滲透，會直接壓縮占營收約 68.7% 的中國市場定價。","p":35,"evidence_refs":["competitive_share_entrants#1","geo_supply_chain#0"]},{"level":"🟡","text":"雷射鑽孔與玻璃基板穿孔替代：一般 HDI 微孔已用雷射，但未見取代高階背鑽的直接證據；玻璃基板大規模應用估需 2–3 年。","p":15,"evidence_refs":["substitute_technology#0","substitute_technology#1"]},{"level":"🟡","text":"美中管制與中國宏觀放緩：法說摘要自列為主要風險，屬客戶需求端衝擊而非技術替代。","p":20,"evidence_refs":["geo_supply_chain#1"]}],"roic_durability":{"quadrant":"高利益率×周轉率未知（投入資本事實表未涵蓋）","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者與付款者都是 PCB 廠，決策取決於其擴產計畫；AI 板層數升級讓高階背鑽成為必要工序，急迫性高，但持久性取決於九大雲端業者資本支出（2026 年年增約 90%）能否延續。交期約 6 個月時延後購買代價高，產能過剩時趨近於零。"},{"item":"決策層級","level":"🟡","text":"以單一產線採購衡量：中階機種國產化逾七成，替代容易；高速主軸機種國產化 15–20%，高階背鑽仍以進口為主。客戶預訂 2027 年產能反映短缺，不是轉換成本；漲價後流失率與重新認證週期事實表未涵蓋。"},{"item":"價值鏈分配","level":"🟡","text":"鑽孔是 PCB 設備缺口最大環節（券商），短缺期由設備商分到超額利潤；控制器自製讓上游少一個抽成環節，下游 20 家以上 PCB 廠議價分散。缺口補上後，利潤會回流 PCB 廠與其客戶。"},{"item":"社會容忍度","level":"🟡","text":"B2B 設備價格不受社會輿論約束；真正的上限來自政治：中國營收約 68.7%，美中管制與在地採購政策可能直接限制銷售，已列入反證紀錄。"}],"roiic":"以 2023→2025 年淨利增量 703 百萬元 ÷ 2024–2025 年（淨利−自由現金流）1,471 百萬元代理，約 48%；含產能利用率回升，屬上限。","reinvest_rate":"2022–2025 年累計（淨利−自由現金流）416 百萬元 ÷ 累計淨利 1,167 百萬元，約 36%；2024–2025 年單看約 175%，擴產期高於盈餘。","endo_ceiling":17,"formula_note":"內生成長率＝增量報酬 × 再投資率。投入資本、折舊與營運資金變動事實表未涵蓋，改以淨利減自由現金流代理再投資：0.48 × 0.36 ≈ 17%。增量報酬取循環回升窗，偏高。"}}}},"q3_growth":{"verdict":"跑道中等：2026 年 1–9 月營收年增 140.2%，靠擴產量能與高階機種組合；三年每股盈餘成長遠超內生上限，缺口來自利潤率擴張與產能利用率，2028 年後取決於客戶擴產循環與半導體第二引擎。","reasoning":"成長以量為主：月產能 2025 年底約 300 台、2026 年底 400 台以上並自第四季加 50 台委外、2027 年規劃 500 台；價與組合來自高階背鑽機。事實表沒有賣方共識，以本判斷 Base 路徑計，2025 年 8.01 元到 2028 年 42 元，三年每股盈餘年化約 74%，遠高於內生上限約 17%。缺口約 57 個百分點，歸因於利潤率擴張（營益率由 2025 年 20.0% 升到約 29–30%）與產能利用率，不是併購或回購；缺口可以歸因，但它本身就是循環高峰的特徵。跑道判中等：AI 板層數升級與半導體封裝（FOPLP、CoPoS、CoWoP、玻璃基板）提供延伸，但半導體只占約一成、尚未證實；背鑽滲透率事實表未涵蓋，無法推算到 30% 滲透要幾年。衰退信號亮兩項：每股盈餘成長高於營收成長逾 5 個百分點；自由現金流 ÷ 淨利連兩年低於 0.75（2024 年 −4.05、2025 年 −0.18）。","fact_refs":["f_kpi5_backlog","f_kpi6","f_kpi1_ifrs_non_gaap","f_kpi3"],"verdict_values":{"growth":{"driver_mix":"量為主（月產能 300→400 台＋委外 50 台→2027 年 500 台），價與組合（高階背鑽機）為輔；沒有併購、沒有回購。","runway_years":"背鑽滲透率事實表未涵蓋，無法推算","runway_post_y5":"🟡","endo_ceiling_basis":"引報酬持續期段：再投資率約 36% × 增量報酬約 48% ≈ 17%；Base 三年每股盈餘年化約 74%，超出上限。","segments":{"expanded":false,"reason":"PCB 設備約九成、半導體約一成（2025 上半年），2026 年分段營收事實表未涵蓋；半導體目前不決定整體利潤，第二引擎論點放在五年期假設追蹤。"},"decay_signals":[{"item":"毛利率連 2 季年減","lit":false,"note":"2026 年第二季 44.2%，高於 2025 年全年 39.2%"},{"item":"核心市占近 12 個月縮減","lit":null,"note":"份額數字事實表未涵蓋"},{"item":"提價後銷量下滑","lit":false,"note":"交期拉長、訂單滿載"},{"item":"每股盈餘成長高於營收成長逾 5 個百分點","lit":true,"note":"Base 2025–2028 年每股盈餘年化約 74%、營收約 51%"},{"item":"自由現金流 ÷ 淨利連 2 年低於 0.75","lit":true,"note":"2024 年 −4.05、2025 年 −0.18"},{"item":"股份基礎給付占營收逾 5% 且上升","lit":false,"note":"第二季約 0.34%"},{"item":"市場規模萎縮或被替代技術壓縮","lit":false,"note":"未見雷射取代高階背鑽的直接證據"},{"item":"產業估值倍數近 3 年系統性下移","lit":null,"note":"事實表未涵蓋"},{"item":"維護性資本支出占自由現金流逾 60%","lit":null,"note":"事實表未涵蓋"},{"item":"停止投資新產能且營收 3 年內下滑","lit":false,"note":"2027 年規劃月產能 500 台"}],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"資本配置中段：股權幾乎不稀釋，但近兩年自由現金流為負、現金投入擴產與營運資金，回購與配息去向事實表未涵蓋。","reasoning":"股權稀釋極低：第二季股份基礎給付 9.6 百萬元，占營業利益 1.16%、占營收約 0.34%。現金幾乎全數投入擴產與營運資金：2024、2025 年自由現金流各 −5.04 億元、−1.26 億元，2026 年第二季轉正為 2.62 億元（占營收 9.2%）。股息殖利率 0.37%，配息比重低。沒有併購紀錄；回購、債務到期與現金去向四分事實表未涵蓋。半導體子公司上櫃若釋股，母公司持股比例會下降，屬潛在稀釋，條件與時程事實表未涵蓋。","fact_refs":["f_kpi3","f_kpi4_sbc","f_dividend_yield_ttm"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":false,"passed":null,"input":"沒有併購紀錄，成長全靠自建產能"},{"name":"buyback_yield","applicable":null,"passed":null,"input":"回購資料事實表未涵蓋；股息殖利率 0.37%"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"第二季股份基礎給付占營業利益 1.16%、占營收約 0.34%；股數變動事實表未涵蓋，以給付金額推估年稀釋遠低於 1.5%"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購；回購、配息與債務結構事實表未涵蓋，現金去向無法四分。"}}}},"q5_valuation":{"verdict":"現價要求 2028–2030 年沒有明顯的客戶擴產回落、且市場繼續給 28 倍左右；我不信，Base 五年約 −33%，價格是唯一約束。","reasoning":"判斷日股價 1,055 元（事實表股價與均線單位標為 USD，台股報價應為新台幣，本判斷以新台幣解讀）。trailing 本益比 74.66 倍，四個年度端點內分位 19.7 是被 2023 年每股盈餘 0.16 元的低谷分母拉出來的，不能當便宜的證據；市銷率 12.26 倍與企業價值營收比 12.25 倍都在四點最高。五年分位事實表未涵蓋。以 Base 2026 年 29 元計前瞻本益比約 36 倍、2027 年 44 元約 24 倍。現價要成立，需要 2028–2030 年都沒有客戶擴產回落，而且 2031 年市場仍給 28 倍左右，那是機率 25% 的 Bull 情境。Base 用 2030 年循環中段每股盈餘 32 元 × 22 倍，得約 704 元。同業本益比未收錄，終端倍數沒有同業現值可對照（資料缺口），22 倍是循環中段設備股的判斷值。PEG 0.49 看似便宜，但分母是高峰段的盈餘成長，不成立。成長熄火壓力測試：以 2028 年 42 元為基準，之後成長降到 15%、10%、5%，分別給 25、18、12 倍，2030 年對應約 1,388、915、556 元，三項只過一項。RSI 標示不可用，不引用。","fact_refs":["f_price_at_dd","f_pe_current","f_pe_percentile","f_ps_current","f_ps_percentile","f_ev_s_current","f_ev_s_percentile","f_week26_return_pct","f_ma_w52"],"verdict_values":{"valuation":{"basis":"前瞻本益比（2026 年 Base 每股盈餘 29 元，事實表無賣方共識）＋2030 年循環中段每股盈餘 × 終端倍數","peers":{"expanded":false,"reason":"事實表同業對照只收利潤率與研發密度，沒有本益比，無法作倍數錨；直接鑽孔機競品也未收錄。"},"fwd_pe":36.4,"peg":0.49,"percentile_5y":null,"val_light":"🔴","val_light_derivation":"以 2026 年 Base 每股盈餘 29 元計前瞻本益比約 36 倍，對應毛利率 44% 的高峰獲利；以 2030 年循環中段每股盈餘 32 元 × 22 倍回推約 704 元，現價高出約五成；市銷率與企業價值營收比皆為四個年度端點最高。結論是貴。","upside_short_pct":-12,"upside_mid_pct":-33,"denominator_disputed":true,"denominator_note":"每股盈餘正處於擴產與交期拉長的上行段，毛利率由 25% 升到 44%；用高峰盈餘算出的本益比與 PEG 會低估真實倍數，便宜論證不成立，改用 2030 年循環中段盈餘檢查。"}}},"q6_how_wrong":{"verdict":"最可能看錯的是循環時點：若層數升級讓設備需求延續到 2029 年以後，觀望會錯過一段漲幅；反方向是客戶擴產在 2028 年就提前結束。陷阱風險中等。","reasoning":"反證細節在反證紀錄。兩個方向都可能錯：一是層數升級讓鑽孔需求跟著 PCB 產量、而不是擴產增量成長，2029 年的回落不會發生，Bull 路徑兌現；二是客戶擴產在 2028 年提前結束，重演 2023 年。衰退信號亮兩項，價值陷阱風險中等；最主要的陷阱是用高峰獲利算出來的低 PEG。股價為 104 週均線 3.26 倍、250 週均線 6.36 倍，一旦循環轉向，均值回歸空間很大。","fact_refs":["f_ma_w104","f_ma_w250","f_week26_return_pct"],"verdict_values":{"trap":{"verdict":"🟡","label":"高峰獲利定價陷阱（中）"}}}},"scenario_inputs":{"terminal_label":"FY2030E","start":{"eps":14.13,"pe":74.66,"basis":"近四季（至 2026-06-30）每股盈餘＝判斷日股價 1,055 元 ÷ trailing 本益比 74.66 倍；終端倍數同為當年度實際每股盈餘口徑。"},"eps":{"bull":[31,52,64,70,78],"base":[29,44,42,26,32],"bear":[27,34,18,10,16]},"pe":{"bull":28,"base":22,"bear":15},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0.37,"net_buyback":0},"second_stage":{"bull_cagr_pct":15,"base_cagr_pct":8},"max_dd":{"lo":-80,"hi":-55,"basis":"2023 年營收年減 45.5%、每股盈餘由 3.63 元降到 0.16 元；現價為 52 週均線 2.01 倍、104 週均線 3.26 倍、250 週均線 6.36 倍。跌回 52 週均線下方約 −55%（約 475 元），跌到 104 與 250 週均線之間約 −80%（約 211 元）；下限涵蓋 Bear 終點 −77%。","trigger_time":null},"basis":{"bull":"層數升級讓鑽孔需求跟著 PCB 產量而非擴產增量成長，2028 年後不回落；半導體子公司成為第二引擎；2030 年營收約為 2026 年 2.5 倍、營益率 30% 以上，市場續給 28 倍。","base":"2026 年以 1–9 月營收 84.77 億元加第四季滿載推估約 127 億元、營益率約 29%，淨利沿用 2025 年約為營業利益 0.71 倍，股數以 2025 年淨利 ÷ 每股盈餘回推約 8,940 萬股；2027 年月產能 500 台帶動營收年增約 45%；2028 年持平、利潤率小降；2029 年客戶擴產完成、營收回落約四分之一；2030 年回到循環中段，22 倍。","bear":"客戶擴產 2028 年提前結束、中國同業向高階滲透，重演 2023 年營收腰斬，2029 年每股盈餘約 10 元，2030 年回到約 16 元、15 倍。"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"2023 年營收年減 45.5%、營益率 −6.2%、每股盈餘 0.16 元；20 家以上中國 PCB 廠同時公布擴產，設備需求高峰與客戶擴產週期連動，上游玻纖、鎢鋼棒短缺也可能打亂客戶擴產節奏。","assumption":"本判斷假設訂單高檔延續到 2028 年。","consequence":"若客戶擴產在 2028 年提前結束，2030 年每股盈餘約 16 元、15 倍下約 240 元，五年虧損近八成；與 Single Thing 是同一條故事。","ruling":"採納：Bear 機率給 30%，Base 已含 2029 年營收回落約四分之一。","watch":"單月營收年增率、季末在手訂單與交期。","evidence_refs":["supply_demand_durability#3"],"fact_refs":["f_kpi5_backlog"]},{"view":"論點失敗","evidence":"2025 年約 68.7% 營收來自中國，法說摘要自列易受中國宏觀與美中半導體管制波及；兩項都出自第三方 AI 法說摘要，非公司原文。","assumption":"中國客戶的設備採購不受政策干預。","consequence":"管制或在地採購政策一出，過半營收的需求直接受限；南京在地產能避得了關稅，避不了政策性轉單。","ruling":"採納：列為短期風險，管制公告後單月營收年增連 2 個月轉負即減碼至 1% 以下；來源屬二手摘要，占比以年報區域別營收複核。","watch":"美中管制公告、年報區域別營收。","evidence_refs":["geo_supply_chain#0","geo_supply_chain#1"],"fact_refs":[]},{"view":"論點成功但股東經濟變差","evidence":"公司曾遭中國廠商抄襲，中階機械鑽孔機國產化率已逾七成；2024、2025 年自由現金流皆為負，近四季自由現金流率 9.7%，6664.TWO 為 27.1%；半導體子公司規劃上櫃。","assumption":"AI 需求延續時毛利率能守在 40% 以上，獲利能轉成現金。","consequence":"需求還在，但中國同業壓價讓毛利率回到 30% 出頭，擴產又持續吃營運資金，每股盈餘成長轉不成股東現金；子公司上櫃釋股再稀釋母公司持股。","ruling":"採納：定價只給 5 分；季毛利率連 2 季低於 38% 減碼一半，2026 年自由現金流 ÷ 淨利低於 0.5 減碼一半。","watch":"季毛利率、年度自由現金流 ÷ 淨利、子公司釋股比例。","evidence_refs":["competitive_share_entrants#1"],"fact_refs":["f_peer_3167_tw_fcf_margin_pct","f_peer_6664_two_fcf_margin_pct"]},{"view":"價格已反映太多","evidence":"股價 1,055 元為 52 週均線 2.01 倍，26 週漲 84.05%；trailing 本益比 74.66 倍，市銷率 12.26 倍為四個年度端點最高；以 2026 年 29 元計前瞻約 36 倍。","assumption":"市場在 2031 年仍願意對設備股給 25 倍以上。","consequence":"就算 2027 年每股盈餘到 44 元，2030 年循環中段 32 元 × 22 倍只有約 704 元，五年約 −33%。","ruling":"採納：價格是唯一約束，不追，等 500 元以下。","watch":"股價與 52 週均線的距離、2027 年在手訂單。","evidence_refs":[],"fact_refs":["f_price_at_dd","f_ma_w52","f_week26_return_pct","f_pe_current","f_ps_current"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 None → 本次 ✅","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=None","side_b":"本次 ma=✅","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 None → 本次 1055.0","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=None","side_b":"本次 price_at_dd=1055.0","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"需求性質：結構性升級還是設備擴產循環","cause":null,"prior_field":null,"side_a":"券商稱設備訂單排到 2028 年、2027 年供需缺口最大，鑽孔是 PCB 設備缺口最大環節；AI 板層數由 24–28 層升到 40 層以上，每片板的鑽孔與背鑽工時增加。","side_b":"設備訂單取決於客戶產能增量而非產量；20 家以上中國 PCB 廠同時擴產，2023 年營收曾年減 45.5%；交期約 6 個月時客戶有提前下單的誘因，排單長度不等於最終需求。","ruling":"可調和，屬程度差異：兩邊都同意 2027 年前需求強，分歧在 2028 年後的斜率。本判斷取中間，Base 到 2028 年持平、2029 年回落約四分之一；不把排單長度當作需求不回落的證據。","evidence_level":"券商預測＋公司月營收（已實現）","settle_metric":"2027 年下半年單月營收年增率與季末在手訂單","if_then":["若 2027 年第四季單月營收年增仍 ≥30% 且在手訂單續增，則把循環回落延到 2030 年以後並重跑研究，重評價位上調到 650 元","若單月營收年增連 3 個月低於 0%，則判定循環反轉：未持有者不進場，持有者減碼至 1% 以下"],"evidence_refs":["supply_demand_durability#1","supply_demand_durability#3"]},{"axis":"現在就買的最強論證（觀望的反面）","cause":null,"prior_field":null,"side_a":"以 2027 年 Base 每股盈餘 44 元計，現價約 24 倍；月產能明年 500 台、部分客戶已洽談 2027 年產能；若鑽孔需求跟著 PCB 產量成長，2030 年每股盈餘可到 78 元，28 倍下約 2,184 元。","side_b":"這需要 2028–2030 年都沒有客戶擴產回落，而且市場對設備股給 28 倍；2023 年的紀錄與 20 家以上同步擴產都不支持。","ruling":"不採納為現在進場的理由，保留為 Bull 25% 機率；觀望的約束是價格，不是生意。500 元來自 Base 終值 704 元以每年 8% 折回約 4.5 年。","evidence_level":"判斷層（情境機率）","settle_metric":"股價與 2027 年季末在手訂單","if_then":["若股價續漲但 2027 年訂單與毛利率沒有新證據，則不追","若股價跌回 500 元以下而單月營收年增仍為正、在手訂單未季減，則分批反買，首倉試單"],"evidence_refs":["end_markets#2"]},{"axis":"產業態勢：需求結構轉好與競爭、地緣拉鋸","cause":null,"prior_field":null,"side_a":"結構轉好：AI 板層數升級、九大雲端業者 2026 年資本支出年增約 90%、鑽孔是缺口最大環節。","side_b":"競爭與地緣：中國中階機械鑽孔機國產化逾七成、公司曾遭中國廠商抄襲；2025 年約 68.7% 營收來自中國，美中管制列為主要風險。","ruling":"雙向拉鋸：需求面結構轉好中；競爭面在中階已惡化、高階尚守住（高速主軸國產化 15–20%）；地緣是其他結構變動中最大的單項。","evidence_level":"產業報告＋第三方法說摘要","settle_metric":"季毛利率、年報區域別營收","if_then":["若季毛利率連 2 季低於 38% 而營收仍成長，則判定競爭已滲透到高階，減碼一半","若管制公告後單月營收年增連 2 個月轉負，則減碼至 1% 以下"],"evidence_refs":["competitive_share_entrants#1","competitive_share_entrants#2","geo_supply_chain#0","geo_supply_chain#1"]},{"axis":"獲利品質：帳面利潤率與現金轉換","cause":null,"prior_field":null,"side_a":"近四季營益率 24.8%、2026 年第二季 29.2%。","side_b":"2024、2025 年自由現金流各 −5.04 億元、−1.26 億元；近四季自由現金流率 9.7%，低於 6664.TWO 的 27.1%。","ruling":"可調和：擴產期營運資金與資本支出吸收，第二季自由現金流 2.62 億元已轉正；2026 全年自由現金流 ÷ 淨利低於 0.5 則改判收款或存貨問題。","evidence_level":"財報已實現","settle_metric":"2026 年自由現金流 ÷ 淨利","if_then":["若 2026 年自由現金流 ÷ 淨利 ≥0.7，則把價值鏈分配檢查點上調一級","若低於 0.5，則持有者減碼一半並把定價分數再降一分"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"單月營收年增率連 3 個月轉負，代表客戶擴產循環反轉","type":"假設驗證","maps_to":"H1","metric":"單月營收年增率","threshold":"連 3 個月低於 0%","action":"不進場；已持有者減碼至 1% 以下","source_freq":"公開資訊觀測站月營收，每月","date":null,"evidence_refs":["supply_demand_durability#3"]},{"n":2,"text":"季毛利率連 2 季跌破 38% 而營收仍成長，代表中國同業壓價或組合轉差","type":"風險","maps_to":"R3","metric":"季毛利率","threshold":"連 2 季低於 38%","action":"減碼一半","source_freq":"季報，每季","date":null,"evidence_refs":["competitive_share_entrants#1"]},{"n":3,"text":"美中管制或中國政策限制設備採購後，營收吸收不了衝擊","type":"風險","maps_to":"R2","metric":"管制公告後單月營收年增率","threshold":"公告後連 2 個月低於 0%","action":"減碼至 1% 以下","source_freq":"事件＋月營收","date":null,"evidence_refs":["geo_supply_chain#0","geo_supply_chain#1"]},{"n":4,"text":"Single Thing：季末在手訂單首次季減，且同季單月營收年增轉負","type":"Single Thing","maps_to":"Single Thing","metric":"季末在手訂單＋單月營收年增率","threshold":"在手訂單較前季減少，且同季任一月營收年增低於 0%","action":"清倉；未持有者撤銷 500 元重評價位","source_freq":"季報與法說，每季","date":null,"evidence_refs":["supply_demand_durability#3"]},{"n":5,"text":"股價回落到 500 元以下且基本面未轉弱時重跑研究","type":"估值rearm","maps_to":"H1","metric":"股價＋單月營收年增率＋在手訂單","threshold":"股價 ≤500 元，且單月營收年增高於 0% 或在手訂單未季減","action":"重跑研究，通過後試單建首倉","source_freq":"每日股價＋每月營收","date":null,"evidence_refs":[]},{"n":6,"text":"2026 年第三季財報：毛利率能否守住、自由現金流能否維持正值","type":"複審日期","maps_to":"H2","metric":"季毛利率與自由現金流","threshold":"毛利率 ≥42% 且自由現金流大於 0","action":"任一未達即下修 Base 情境並重跑","source_freq":"季報","date":"2026-11-14","evidence_refs":[]},{"n":7,"text":"2026 年自由現金流低於淨利一半，擴產吞噬現金","type":"風險","maps_to":"R4","metric":"全年自由現金流 ÷ 淨利","threshold":"低於 0.5","action":"已持有者減碼一半","source_freq":"年報","date":"2027-03-31","evidence_refs":[]}],"kill_metrics":[{"metric":"單月營收年增率","bear_threshold":"連 3 個月低於 0%","window":"每月，2027–2028 年為主","source":"公開資訊觀測站月營收","last_status":"ok"},{"metric":"季毛利率","bear_threshold":"連 2 季低於 38%","window":"每季","source":"季報","last_status":"ok"},{"metric":"季末在手訂單","bear_threshold":"首次季減且同季月營收年增轉負","window":"每季","source":"季報與法說（媒體引述公司）","last_status":"ok"},{"metric":"管制公告後單月營收年增率","bear_threshold":"公告後連 2 個月低於 0%","window":"事件後 2 個月","source":"美中管制公告＋月營收","last_status":"unknown"},{"metric":"年度自由現金流 ÷ 淨利","bear_threshold":"2026 年低於 0.5","window":"年度","source":"年報","last_status":"warning"}],"evidence_dismissed":[],"action_conditions":{"rearm_trigger":"股價≤500 元為必要條件，另需單月營收年增>0% 或季末在手訂單未季減其一；觸發後重跑研究再定首倉","exec_line":"現價不追。股價先走而訂單、毛利率沒有新證據時不追；跌回 500 元以下而月營收年增仍為正，分批反買、首倉試單；月營收年增連 3 個月轉負則撤銷重評價位，等下一輪谷底。"}},"decision_inputs":{"signal":"C","ma":"✅","cycle_position":"晚循環","cycle_verdict":"等回踩","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場把 2026–2027 年擴產與交期拉長帶來的高峰毛利當成可延續的結構獲利，以約 36 倍前瞻本益比定價；2023 年營收年減 45.5%、營益率轉負的紀錄顯示設備訂單會隨客戶擴產節奏反轉。","momentum_overheated":null,"cycle_gates_pass":false,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"股價回落至 500 元以下，且單月營收年增仍為正或季末在手訂單未季減"},"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"6","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='C'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='C'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='✅'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"輸入缺(momentum_overheated=null)，依保守方向處理：不視為觸發","input_gap":["momentum_overheated"]},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":true,"basis":"signal='C'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場把 2026–2027 年擴產與交期拉長帶來的高峰毛利當成可延續的結構獲利，以約 36 倍前瞻本益比定價；2023 年營收年減 45.5%、營益率轉負的紀錄顯示設備訂單會隨客戶擴產節奏反轉。"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='C', runway='🟡', val='🔴', moat_trend='→', week26=84.05, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='循環/商品', cycle_position='晚循環', moat='C', moat_trend='→', cycle_gates_pass=False"},{"row":"6/7/7a-verdict","condition":"Soft Veto 生效 → 觀望（max-severity wins；8a/8b 未能繞過）","hit":true,"basis":"soft_veto_rows=['6']"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":null,"requires_critic":[]},"thesis":{"H":[{"id":"H1","text":"AI 伺服器板層數升級讓高階背鑽與鑽孔設備需求延續到 2027 年，擴產量能能被吸收。","2y":"2026 年營收年增 ≥120%、2027 年營收年增 ≥30%","5y":null,"10y":null,"threshold":"2027 年全年營收年增 ≥30%；單月營收年增連 3 個月低於 0% 即反轉","source":"公開資訊觀測站月營收（每月 10 日前）、季報與法說的在手訂單","drift_rule":"近四季營收較本路徑連 2 季落後 ≥5% 為削弱，連 3 季落後 ≥10% 為反轉"},{"id":"H2","text":"高階機種組合與自製控制器讓毛利率守在 40% 以上。","2y":"2026–2027 年各季毛利率 ≥40%（2026 年第二季 44.2%）","5y":null,"10y":null,"threshold":"季毛利率 ≥40%；連 2 季低於 38% 視為反轉","source":"季報","drift_rule":"近四季毛利率較 42% 連 2 季偏離 ≥5% 為削弱，連 3 季偏離 ≥10% 為反轉"},{"id":"H3","text":"半導體子公司成為第二成長曲線，降低對 PCB 擴產循環的依賴。","2y":null,"5y":"2030 年半導體營收占比 ≥20%（2025 上半年約一成），且子公司完成上櫃","10y":null,"threshold":"半導體營收占比 ≥20%","source":"年報分部資訊、子公司上櫃公開說明書","drift_rule":"以每年占比 +2 個百分點為路徑，連 4 季落後 ≥5% 為削弱，連 6 季落後 ≥10% 為反轉"}],"R":[{"id":"R1","text":"設備訂單隨客戶擴產循環反轉：20 家以上中國 PCB 廠同步擴產，完成後設備需求斷崖式回落。","h_ref":"H1","clock":"🔥","threshold":"單月營收年增連 3 個月低於 0%，或季末在手訂單季減","evidence_refs":["supply_demand_durability#3"]},{"id":"R2","text":"中國集中與美中管制：2025 年約 68.7% 營收來自中國（第三方法說摘要），管制或中國宏觀放緩直接衝擊需求。","h_ref":"H1","clock":"⚡","threshold":"管制公告後單月營收年增連 2 個月低於 0%","evidence_refs":["geo_supply_chain#0","geo_supply_chain#1"]},{"id":"R3","text":"中國廠商抄襲與在地化向高階滲透，壓縮定價。","h_ref":"H2","clock":"🐢","threshold":"季毛利率連 2 季低於 38% 而營收仍成長","evidence_refs":["competitive_share_entrants#1"]},{"id":"R4","text":"擴產吞噬現金：2024–2025 年自由現金流皆為負，若 2026 年仍低於淨利一半，代表應收或存貨堆積。","h_ref":"H2","clock":"🔥","threshold":"2026 年自由現金流 ÷ 淨利低於 0.5","evidence_refs":[]}],"single_thing":{"description":"季末在手訂單（第二季末逾 75 億元）首次季減，且同季單月營收年增轉負，代表客戶擴產循環見頂。","why_fatal":"設備訂單吃的是客戶產能增量，見頂後回落是斷崖式：2023 年營收年減 45.5%、每股盈餘由 3.63 元降到 0.16 元。現價約 36 倍前瞻本益比建立在高峰毛利上，盈餘與倍數會同時下修；這是 2028–2030 年每股盈餘最大的單一敏感項。","if_happens":"持有者清倉；未持有者撤銷 500 元重評價位，等月營收年減幅度收斂後再看下一輪谷底。","how_monitor":"每月 10 日前公告的月營收年增率；每季財報與法說揭露的在手訂單與交期。","probability":"35%（12–24 個月內；券商稱訂單排到 2028 年，但交期拉長下的提前下單會放大回落）"}},"appendix_a":{"growth_durability":5,"quality_score":5,"ai_risk":"🟢","long_term_confidence":"低","fpe_fy2":null,"peg_fy2":null,"stress":{"pass":1,"total":3}},"eps_meta":{"base_eps_path":{"FY2025A":8.01,"FY2026E":29,"FY2027E":44,"FY2028E":42},"fy_end_month":12,"eps_basis":"IFRS 稀釋每股盈餘；事實表無賣方共識，2026E–2028E 為本判斷 Base 路徑，不是共識"},"catalysts":[{"date":"2026-11","date_precision":"month","type":"other","event":"2026 年第三季財報（法定期限 11 月 14 日）","impact":"中","watch":"毛利率是否守在 42% 以上、自由現金流是否維持正值"},{"date":"2026-12","date_precision":"quarter","type":"capacity","event":"月產能擴到 400 台以上，第四季起加開 50 台委外","impact":"中","watch":"第四季單月營收能否站上 14 億元"},{"date":"2027-03","date_precision":"month","type":"guidance","event":"2026 年年報（法定期限 3 月 31 日）與 2027 年展望","impact":"高","watch":"2027 年 500 台產能的接單覆蓋率、在手訂單、區域別營收"},{"date":null,"date_precision":null,"type":"other","event":"半導體子公司大量先進智能規劃上櫃（時程事實表未涵蓋）","impact":"中","watch":"釋股比例與母公司持股稀釋"},{"date":"2027-12","date_precision":"quarter","type":"capacity","event":"月產能擴到 500 台","impact":"中","watch":"擴產後毛利率與交期是否回落"}]}
```

---

## 尾段：回覆格式

只回一個 JSON 陣列，①–⑧ 每條一個元素，八個全出，不得跳號、不得多列，陣列外不得有任何文字（不加前言、不加 markdown 圍欄、不加附註）：

```json
[{"item": "①", "light": "🔴|🟡|🟢", "judgment_path": "$.路徑", "reason": "一句話"}]
```
