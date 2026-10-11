你是 DD 管線 v20 的判斷層閘（gate），標的 2404.TW（20261011）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（28 條）
- `f_kpi0_gaap`（q1_business）｜營收（GAAP，合併）＝260.8 億 TWD｜期間與口徑：Q2 2026（季末 2026-06-30，公告於 2026-08-12）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：yfinance quarterly_income_stmt（MOPS 合併財報）；月營收交叉 technews 4-6 月合計約 260.7 億（numbers.latest_quarter_kpis.items[0]，as_of Q2 2026（季末 2026-06-30，公告於 2026-08-12））
  - 註記：查無
- `f_kpi1_gaap`（q1_business）｜毛利率（GAAP）＝23.64 %｜期間與口徑：Q2 2026（季末 2026-06-30，公告於 2026-08-12）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：yfinance quarterly_income_stmt（毛利 61.65 億 ÷ 營收 260.80 億）（numbers.latest_quarter_kpis.items[1]，as_of Q2 2026（季末 2026-06-30，公告於 2026-08-12））
  - 註記：查無
- `f_kpi2_gaap_non_gaap_non_gaap`（q1_business）｜GAAP 營業利益／利益率（台股無 Non-GAAP 口徑，Non-GAAP 同略）＝52.11 億 TWD（營益率 19.98%）｜期間與口徑：Q2 2026（季末 2026-06-30，公告於 2026-08-12）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：yfinance quarterly_income_stmt（numbers.latest_quarter_kpis.items[2]，as_of Q2 2026（季末 2026-06-30，公告於 2026-08-12））
  - 註記：查無
- `f_kpi5_backlog`（q1_business）｜已簽約未認列在手訂單（backlog）＝1939.37 億 TWD｜期間與口徑：截至 2026-05 底（2026-06-11 法說會；Q2 季末值未取得）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：富果／時報報導 2026-06-11 法說會，blog.fugle.tw/post/earnings-call-2404-2026-06-11（numbers.latest_quarter_kpis.items[5]，as_of 截至 2026-05 底（2026-06-11 法說會；Q2 季末值未取得））
  - 註記：不適用
- `f_kpi6`（q1_business）｜管理層全年指引（定性）＝2026 年營收有機會再創新高；美國占比全年有機會過半 定性｜期間與口徑：2026-06-11 法說會（8 月法說內容未查得）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：時報／富果報導 2026-06-11 法說會；無量化區間（numbers.latest_quarter_kpis.items[6]，as_of 2026-06-11 法說會（8 月法說內容未查得））
  - 註記：不適用
- `f_earnings_recency`（q1_business）｜最近一次財報日＝2026-08-12 date｜期間與口徑：2026-08-12／距今 43 個交易日｜kind：realized
  - 來源：—（numbers.earnings_recency，as_of 2026-08-12）
- `f_peer_2404_tw_gross_margin_pct`（q2_moat）｜2404.TW 毛利率＝21.25 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.2404.TW.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_2404_tw_operating_margin_pct`（q2_moat）｜2404.TW 營業利益率＝17.7 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.2404.TW.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_2404_tw_fcf_margin_pct`（q2_moat）｜2404.TW FCF 利潤率＝33.49 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.2404.TW.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_6139_tw_gross_margin_pct`（q2_moat）｜6139.TW 毛利率＝19.47 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.6139.TW.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_6139_tw_operating_margin_pct`（q2_moat）｜6139.TW 營業利益率＝17.25 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.6139.TW.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_5536_two_gross_margin_pct`（q2_moat）｜5536.TWO 毛利率＝21.1 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.5536.TWO.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_6691_tw_operating_margin_pct`（q2_moat）｜6691.TW 營業利益率＝16.13 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.6691.TW.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝81.69 TWD/share｜期間與口徑：2026-10-09／Koyfin 快照共識值；原為美元，已依快照日匯率換算為新台幣（twd (koyfin usd ×31.9120 @ 2026-10-09)）｜kind：estimate
  - 來源：DD_tw_EPS_estimates_20261009.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-10-09）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝110.73 TWD/share｜期間與口徑：2026-10-09／Koyfin 快照共識值；原為美元，已依快照日匯率換算為新台幣（twd (koyfin usd ×31.9120 @ 2026-10-09)）｜kind：estimate
  - 來源：DD_tw_EPS_estimates_20261009.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-10-09）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝120.63 TWD/share｜期間與口徑：2026-10-09／Koyfin 快照共識值；原為美元，已依快照日匯率換算為新台幣（twd (koyfin usd ×31.9120 @ 2026-10-09)）｜kind：estimate
  - 來源：DD_tw_EPS_estimates_20261009.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-10-09）
- `f_kpi3_eps`（q4_capital）｜稅後淨利（歸屬母公司）／稀釋 EPS＝19.84 TWD／股（淨利 37.63 億）｜期間與口徑：Q2 2026（季末 2026-06-30，公告於 2026-08-12）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：yfinance quarterly_income_stmt；搜尋聚合站列 EPS 19.92（基本 EPS 口徑，差異未驗）（numbers.latest_quarter_kpis.items[3]，as_of Q2 2026（季末 2026-06-30，公告於 2026-08-12））
  - 註記：查無
- `f_kpi4`（q4_capital）｜自由現金流（營業現金流−資本支出）＝67.66 億 TWD｜期間與口徑：Q2 2026（季末 2026-06-30，公告於 2026-08-12）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：yfinance quarterly_cashflow（OCF 67.73 億，capex 0.07 億）（numbers.latest_quarter_kpis.items[4]，as_of Q2 2026（季末 2026-06-30，公告於 2026-08-12））
  - 註記：查無
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝3.065 %｜期間與口徑：2026-10-11／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-10-11）
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝1305.0 TWD｜期間與口徑：2026-10-08（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-10-08（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝15.98 x｜期間與口徑：2026-10-09／分母＝FY1 EPS 81.69，分子＝快照價 1305.0｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-10-09）
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝19.81 x｜期間與口徑：2026-10-08（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-10-08（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝100.0 %｜期間與口徑：2026-10-08（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-10-08（RTH 收盤，UTC））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝2.86 x｜期間與口徑：2026-10-08（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-10-08（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝100.0 %｜期間與口徑：2026-10-08（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-10-08（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝2.11 x｜期間與口徑：2026-10-08（RTH 收盤，UTC）／4 個年度端點內的分位＝93.7｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-10-08（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝93.7 %｜期間與口徑：2026-10-08（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-10-08（RTH 收盤，UTC））
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝48.5 %｜期間與口徑：2026-10-08（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^TWII｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-10-08（RTH 收盤，UTC））

### findings_digest 中方向為負或來源衝突的條目（2 條）
- `competitive_share_entrants#3`（competitive_share_entrants｜方向 -｜狀態 ok）：2025年6月工商時報：台灣五大機電與無塵室工程廠在手訂單逾5,000億元，亞翔逾2,000億元居首，漢唐逾千億元；對比2026年9月，漢唐1,939億與亞翔4,400億，亞翔訂單領先幅度擴大。
  - 來源：工商時報 ctee（as_of 2025-06-24）｜affects：moat_trend、decision_inputs.bear
- `geo_supply_chain#2`（geo_supply_chain｜方向 -｜狀態 ok）：2024 年法說會：美中貿易戰使海外客戶建廠意願低，海外營收比重降至 10% 以下
  - 來源：搜尋結果摘要（漢唐法說相關報導，來源頁未能確認）（as_of 2024-12-31）｜affects：thesis.R、decision_inputs.bear

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/2404.TW_20261011/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":2686,"bear_5y_price":550,"p_bull_pct":25,"p_bear_pct":30,"upside_5y_pct":15.9,"ev5y_pct":16.2,"irr_base_pct":3.0,"asym_ratio":1.5,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":81.69,"pe":15.98,"basis":"FY2026E共識EPS（Koyfin快照換算新台幣）；終端倍數同樣以當年度EPS為分母"},"eps":{"bull":[116,133,146,153,158],"base":[108,118,121,115,108],"bear":[100,88,72,60,55]},"pe":{"bull":17,"base":14,"bear":10},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":3.065,"net_buyback":0},"second_stage":{"bull_cagr_pct":6,"base_cagr_pct":2},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

[本次無舊逐字稿摘錄]

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 5 | 2 |
| customer_second_source | none | 0 | 2 |
| customer_concentration_credit | found | 2 | 3 |
| supply_demand_durability | found | 4 | 2 |
| regulatory_antitrust | none | 0 | 3 |
| reg_tariff_export | found | 4 | 4 |
| geo_supply_chain | found | 3 | 3 |
| end_markets | found | 8 | 3 |
| substitute_technology | none | 0 | 2 |
| channel_business_model_shift | found | 2 | 3 |
| capital_markets_pricing | found | 3 | 2 |
| major_events | found | 2 | 4 |

未涵蓋／不適用軸的查詢詞原文（供判相關性）：
- **customer_second_source**（none）（沿用 2404.TW_20261011，0d）：漢唐 2404 最大客戶 台積電 自製 OR 第二供應商 2026；漢唐集成 客戶集中 台積電 營收占比 競爭 帆宣 2026
- **regulatory_antitrust**（none）（沿用 2404.TW_20261011，0d）：漢唐 2404 公平會 OR 反壟斷 OR 調查 2026；United Integrated Services 2404 regulation OR regulatory scrutiny cleanroom engineering 2026；2404.TW 漢唐 DOJ OR FTC OR EU competition 2026
- **substitute_technology**（none）（沿用 2404.TW_20261011，0d）：漢唐 2404 無塵室 機電工程 競爭 替代 技術 2026；Marketech 2404.TW technology obsolescence risk cleanroom turnkey fab construction modular alternative 2026

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"status":"no_prior_dd"}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"2404.TW","date":"2026-10-11","schema":"v15.0","contract":"v19","company_name":"漢唐集成"},"oneliner":"台積電晶圓廠無塵室的主承包商，1,939億元在手訂單撐住2027–2028年獲利；但毛利率站在四年最高的23%、股價半年漲48.5%，五年報酬押在2029年後沒有證據的建廠需求，等回落再進","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/2404.TW_20261011/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/2404.TW_20261011/scenario.json","answers":{"q1_business":{"verdict":"賺晶圓廠建廠的無塵室與廠務系統工程錢；錢卡在「誰能準時把廠蓋好」這一節點，但最大客戶台積電握有議價權","reasoning":"最新一季（2026年第二季）營收260.8億元，毛利率23.64%，營業利益52.11億元（營益率19.98%）。事實表沒有業務分部拆分，只有地區：2026年第一季美國56%、台灣40%、其他4%，管理層預期全年美國過半。收錢方式是專案工程按進度認列。截至2026年5月底在手訂單1,939億元，約為2025年全年營收660.9億元的2.9倍，預計2–2.5年認列完。單點依賴是台積電：富果稱其12吋廠近八成無塵室由漢唐承包（這是承包比例，客戶別營收占比未揭露），這同時是護城河證據與集中度風險。產業時鐘在擴張期：台積電2026年資本支出上修至600–640億美元，SEMI估2026年晶圓廠設備支出年增24%。供需持久性屬週期性：管理層稱景氣看到2029年、瓶頸是人力不是訂單，但需求本質是可延後的建廠資本支出，2024年營收年減31.16%就是前例，能見度過後會反轉。","fact_refs":["f_kpi0_gaap","f_kpi1_gaap","f_kpi2_gaap_non_gaap_non_gaap","f_kpi5_backlog","f_kpi6","f_earnings_recency"],"verdict_values":{"revenue_quality":"專案工程收入，按完工進度認列，沒有經常性收入；在手訂單約為2025年營收的2.9倍，未來兩年能見度高，之後取決於新接單","unit_econ_note":"毛利率由2023年10.93%升至2026年第二季23.64%；資本支出單季僅0.07億元，自由現金流長期高於淨利（2025年290.6億元對90.7億元），推論來自客戶預收，資產負債表事實表未涵蓋","archetype":{"primary":"循環/商品","secondary":null,"confidence":"中","fingerprint":"營收隨客戶建廠週期擺盪（2023年+42.92%、2024年−31.16%、2025年+39.37%），資本支出近零，現金流由預收墊高"},"industry":{"clock_phase":"II","sd_verdict_source":"週期性將反轉：管理層2026年6月法說稱供不應求、景氣看到2029年；台積電稱2028年起資本支出大幅加速，外資估2027年770億美元、2028年860–900億美元；2029年後沒有證據","bargaining":{"up":"人力、分包與物料：管理層稱台灣人力與供應鏈是成長瓶頸，上游議價力上升","down":"台積電是最大客戶，已在新案壓價，管理層的毛利率目標只求維持","geo":"美國占第一季營收56%；美台協議關稅上限15%，在美建廠的台灣企業建廠期間進口設備可免232關稅"},"profit_pool_dir":"利潤池暫時流向廠務工程環節（毛利率四年由13.94%升到23%以上），反映的是供給吃緊而非結構轉移；客戶壓價代表利潤回流的壓力已經出現","tam_table":{"expanded":false,"reason":"成長不靠滲透率：台灣12吋廠份額已逾七成（產業估計），收入規模由客戶建廠資本支出決定；需求錨用台積電資本支出與SEMI設備支出，已寫在成長題"}}}},"q2_moat":{"verdict":"→：執行力在擴大，定價力在縮減，合計穩定；護城河B級","reasoning":"機制是與台積電長年合作累積的晶圓廠廠務整合能力。建廠時程緊、良率攸關，客戶傾向交給驗證過的承包商，漢唐也隨台積電赴美。可證方向用同業利潤率差：近四季毛利率21.25%、營益率17.7%，只比亞翔高1.78與0.45個百分點，高於其他三家同業但差距都不大；同業ROIC資料事實表未涵蓋。執行力給8分：2026年1–8月營收年增71.61%，在手訂單創新高，美國占比過半。定價力給6分：管理層稱後續訂單面對客戶壓價；台南案無塵室機電由漢唐與亞翔分層分工，代表客戶在單一案內維持雙供應；亞翔在手訂單約4,400億元、為漢唐的2.3倍，差距比2025年6月的約2倍擴大（漢唐引用值是5月底舊數字，比較時點不完全一致）。這些還不到份額下滑的證據，但不允許給擴大。產業態勢是雙向拉鋸：需求面結構轉好（台積電資本支出上修、美國擴廠），競爭面趨於惡化（亞翔接單差距擴大、客戶雙供應）。報酬持續期方面，資本支出近零、營運資金為負，ROIC很高但投入資本事實表未涵蓋，無法精算；持續期的弱點在價值鏈分配，不在資本。","fact_refs":["f_peer_2404_tw_gross_margin_pct","f_peer_2404_tw_operating_margin_pct","f_peer_2404_tw_fcf_margin_pct","f_peer_6139_tw_gross_margin_pct","f_peer_6139_tw_operating_margin_pct","f_peer_5536_two_gross_margin_pct","f_peer_6691_tw_operating_margin_pct","f_kpi1_gaap"],"verdict_values":{"moat":{"mechanism":"與台積電長年合作累積的晶圓廠無塵室與廠務系統整合能力，靠驗證紀錄與時程把握留住客戶，並隨客戶赴美","execution":8,"pricing":6,"grade":"B","trend":"→","trend_evidence":"執行面擴大（2026年1–8月營收年增71.61%、在手訂單1,939億元創高、美國占比過半）；定價面縮減（客戶壓價、亞翔在手訂單差距由約2倍擴大到約2.3倍、毛利率只比亞翔高1.78個百分點）","competitor_notes":[{"name":"6139.TW","strategy_note":"亞翔：利潤率與漢唐幾乎同級，在手訂單規模約為漢唐2.3倍，且在台積電新案分層分工，是唯一能直接分食的對手"},{"name":"6196.TW","strategy_note":"毛利率與營益率明顯較低，獲利結構偏設備與系統整合，不在無塵室主承包同一層競爭"},{"name":"5536.TWO","strategy_note":"毛利率與漢唐相近、營益率略低，現金轉換明顯較弱，未見搶單證據"},{"name":"6691.TW","strategy_note":"營益率接近漢唐，但自由現金流利潤率是同業最低，推論預收條件不如漢唐"}],"threats":[{"level":"🟡","text":"亞翔接單動能較強：在手訂單約4,400億元對漢唐1,939億元，差距擴大；台南案兩家分層分工，客戶維持雙供應","p":"30%","evidence_refs":["competitive_share_entrants#3","competitive_share_entrants#2"]},{"level":"🟡","text":"最大客戶壓價：管理層稱後續訂單面對價格壓力，毛利率目標只求維持現水準","p":"40%","evidence_refs":["end_markets#3"]}],"roic_durability":{"quadrant":"高利益率×高周轉（推論）：近四季營益率17.7%，資本支出近零，營運資金由預收支應；投入資本事實表未涵蓋，ROIC未精算","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者、決策者、付款者都是晶圓廠業主；台積電稱AI晶片需求大於供給、產能緊缺延續至2027年，需求真實且急迫，但建廠屬可延後支出，2024年營收年減31.16%說明急迫不等於持久"},{"item":"決策層級","level":"🟡","text":"替代性要在單一新廠發包的層級看：台南案由漢唐承包3–6層、亞翔承包1–2層，客戶在同一案內就能切換部分樓層；轉換成本來自驗證與時程，不是長約"},{"item":"價值鏈分配","level":"🟡","text":"整條鏈的利潤集中在晶圓廠與設備商，買方高度集中於台積電且已在壓價；漢唐毛利率四年由13.94%升到23%以上，主要是供給吃緊時多分到的份，客戶一有餘裕就會收回；廠務工程占建廠支出的比重事實表未涵蓋"},{"item":"社會容忍度","level":"🟢","text":"不涉民生定價或監管授權；外部約束是貿易政策：美台協議關稅上限15%，在美建廠企業的設備可免232關稅，屬政策敏感度而非社會定價上限，已列入美國業務風險"}],"roiic":"投入資本事實表未涵蓋，無法計算；資本支出單季0.07億元，營運資金由預收支應，增量投入資本近零甚至為負，比值不具意義","reinvest_rate":"近零：資本支出近零，營運資金變動為流入；2026年1月亞利桑那購地約4,100萬美元是少數實體投資","endo_ceiling":null,"formula_note":"增量ROIC×再投資率在此不適用：成長不受資本約束，受人力與客戶資本支出約束（管理層稱瓶頸是台灣人力與供應鏈）"}}}},"q3_growth":{"verdict":"🟡：2029年前有在手訂單與台積電資本支出撐腰，之後沒有證據","reasoning":"成長以量為主：營收增加來自客戶建廠案量與美國案，價格面受客戶壓制，沒有併購與回購。共識EPS由2025年實際47.73元到2028年120.63元，三年年複合約36.2%，分年為+71.2%、+35.5%、+8.9%，共識本身已預期2028年明顯放緩；共識家數事實表未涵蓋。資本公式算出的內生上限不適用（見護城河題），實際上限是接單與人力：在手訂單1,939億元分2–2.5年認列，每年約780–970億元；2026年1–8月營收已達656.94億元，接近此區間上緣，之後要靠新接單補。共識與內生上限的差距歸因為新案量加毛利率擴張（2025年20.02%到2026年第二季23.64%），不依賴本益比擴張。跑道方面，台灣12吋廠份額已逾七成（產業估計未查證），國內沒有份額空間；美國是有來源的第二條腿，但壽命綁在台積電亞利桑那的建廠時程，管理層能見度到2029年，第五年之後沒有證據，所以給中等。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_kpi5_backlog","f_kpi6","f_kpi1_gaap"],"verdict_values":{"growth":{"driver_mix":"量為主：新廠案量與美國案；價格受客戶壓制；無併購、無回購","runway_years":"約3年（管理層稱景氣看到2029年）","runway_post_y5":"🟡","endo_ceiling_basis":"資本公式不適用；以在手訂單與人力為實際上限：1,939億元分2–2.5年認列，每年約780–970億元的已簽約基礎","segments":[{"item":"美國","value":"2026年第一季占56%（一份來源寫營收結構、另一份寫新接單，口徑不一）；管理層預期全年美國過半"},{"item":"台灣","value":"2026年第一季占40%"},{"item":"其他","value":"2026年第一季占4%"},{"item":"分部毛利率","value":"事實表未涵蓋；美國案毛利率是否高於台灣沒有資料，這是判斷毛利率能否延續的關鍵缺口"}],"decay_signals":[{"signal":"毛利率連2季年減","lit":false,"note":"2026年第一、二季毛利率23.32%、23.64%，高於2025年全年20.02%"},{"signal":"核心市占近12個月縮減","lit":false,"note":"沒有市占資料；代理指標（在手訂單對亞翔比值）由約0.5倍降到約0.44倍，列入觀察，不亮燈"},{"signal":"主力產品提價後銷量下滑","lit":false,"note":"不適用：專案逐案議價，沒有標準售價"},{"signal":"EPS成長顯著高於營收成長","lit":true,"note":"2022–2025年EPS年複合31.7%、營收11.1%，差20.6個百分點，來自毛利率由13.94%升到20.02%，可能回吐"},{"signal":"自由現金流÷淨利連2年低於0.75","lit":false,"note":"2024年2.83倍、2025年3.20倍；反向風險是預收倒流"},{"signal":"股份基礎給付占營收逾5%且逐年上升","lit":false,"note":"事實表未涵蓋；推算股數2022年至2026年第二季微降約0.9%，沒有稀釋跡象"},{"signal":"市場規模萎縮或被替代技術壓縮","lit":false,"note":"台積電2026年資本支出上修，SEMI估2027年設備支出1,660億美元"},{"signal":"產業估值倍數近3年系統性下移","lit":false,"note":"同業倍數事實表未涵蓋；本身trailing P/E位於四個年度端點最高"},{"signal":"維護性資本支出占自由現金流逾60%","lit":false,"note":"資本支出單季0.07億元，近零"},{"signal":"停止投資新產能且收入3年內下滑","lit":false,"note":"不適用；2026年1月取得亞利桑那土地擴充據點"}],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"資本輕、現金靠客戶預收墊高；股數三年半微降、以配息回饋股東，景氣反轉時預收會倒流","reasoning":"現金轉換：自由現金流÷淨利在2022年為1.63倍、2023年0.94倍、2024年2.83倍、2025年3.20倍；2026年第二季自由現金流67.66億元對淨利37.63億元，為1.80倍。資本支出單季僅0.07億元，超出淨利的部分推論來自客戶預收（資產負債表事實表未涵蓋），接單放緩時會反向流出，所以不把自由現金流當成獲利品質的加分。股份基礎給付：以淨利÷稀釋EPS推算股數，2022年約1.915億股、2025年約1.900億股、2026年第二季約1.897億股，三年半合計約−0.9%，沒有稀釋。回購紀錄與現金去向四分（再投資、併購、配息、回購）事實表未涵蓋；近12個月股息殖利率3.07%。併購：近年沒有；2026年1月子公司取得亞利桑那土地約4,100萬美元，屬不動產，相對獲利規模小。","fact_refs":["f_kpi3_eps","f_kpi4","f_dividend_yield_ttm","f_peer_2404_tw_fcf_margin_pct"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":false,"passed":null,"input":"近年無併購；2026年1月亞利桑那購地約4,100萬美元屬不動產取得"},{"name":"buyback_yield","applicable":false,"passed":null,"input":"事實表未涵蓋回購紀錄"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"以淨利÷稀釋EPS推算股數：2022年約1.915億股、2025年約1.900億股、2026年第二季約1.897億股，年均約−0.3%"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長來自有機接單，沒有靠併購或回購支撐；主要回饋方式是現金股利（近12個月殖利率3.07%），配發率與回購紀錄事實表未涵蓋"}}}},"q5_valuation":{"verdict":"🟠：現價要求2027–2028年共識兌現，而且市場要繼續給峰值獲利14倍以上；前半段可信，後半段不信","reasoning":"以FY2026E共識81.69元計，Forward P/E為15.98倍；以FY2027E 110.73元計為11.79倍，PEG約0.44，表面便宜。但分母站在毛利率四年最高點：若營益率回到2022–2025年平均12.8%（近四季17.7%），FY2026E獲利約打七折、約59元，現價相當於22倍。trailing P/E 19.81倍與P/S 2.86倍都是四個年度端點中最高；五年分位事實表未涵蓋，同業倍數也未涵蓋，終端倍數只能以自身現值為錨。短期上檔：FY2027E基本情境108元×14倍約1,512元，約+15.9%。三年上檔：FY2029E 121元×14倍約1,694元，約+29.8%。但五年基本情境獲利回落到108元，含息年化約6%，落在偏弱區間；股價要回到約1,100元以下，基本情境五年年化才回到約10%。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_pe_current","f_pe_percentile","f_ps_current","f_ps_percentile","f_ev_s_current","f_ev_s_percentile","f_week26_return_pct","f_dividend_yield_ttm"],"verdict_values":{"valuation":{"basis":"Forward P/E（FY2026E與FY2027E共識）為主，輔以正常化營益率換算；同業倍數事實表未涵蓋","peers":{"expanded":false,"reason":"事實表只有同業利潤率，沒有同業倍數，不跨口徑借用；終端倍數以自身現值15.98倍（forward）與19.81倍（trailing）為錨"},"fwd_pe":15.98,"peg":0.44,"percentile_5y":null,"val_light":"🟠","val_light_derivation":"偏貴：表面倍數低（Forward 15.98倍、FY2027E 11.79倍），但分母建立在毛利率四年最高點；以2022–2025年平均營益率正常化後約22倍，trailing P/E 19.81倍為四個年度端點最高，基本情境五年含息年化約6%","upside_short_pct":15.9,"upside_mid_pct":29.8,"denominator_disputed":true,"denominator_note":"Forward P/E的分母是毛利率23.64%（2026年第二季）下的峰值獲利，而2023年毛利率只有10.93%；分母能否延續正是本檔爭點，所以不以低倍數作便宜論證"}}},"q6_how_wrong":{"verdict":"🟡：最可能看錯的是把峰值毛利率當常態，或者反過來低估了AI建廠潮的長度","reasoning":"往下看錯的路徑：毛利率回落比預期快、預收倒流使現金轉負、亞翔分走新案。往上看錯的路徑：若台積電資本支出如外資預估在2028年增至860–900億美元、且2030年後仍不降，基本情境假設2029年見頂就太保守。空頭機率給30%，依據是2024年營收年減31.16%的前例、毛利率處四年最高、客戶已在壓價。壓力測試四項過兩項：毛利率回到2024年的17.95%，仍能賺過2024年（通過）；亞翔再搶下主要新案時，在手訂單仍約為2025年營收的2.9倍（短期通過）；營收重演年減三成且毛利率同步回落（未通過）；美國業務被政策打斷，而美國已占營收過半（未通過）。訴訟方面只見一筆職災補償民事裁定，沒有金額，不構成重大事件。","fact_refs":["f_kpi1_gaap","f_kpi5_backlog","f_week26_return_pct","f_pe_percentile"],"verdict_values":{"trap":{"verdict":"🟡","label":"峰值利潤率下的低本益比"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":81.69,"pe":15.98,"basis":"FY2026E共識EPS（Koyfin快照換算新台幣）；終端倍數同樣以當年度EPS為分母"},"eps":{"bull":[116,133,146,153,158],"base":[108,118,121,115,108],"bear":[100,88,72,60,55]},"pe":{"bull":17,"base":14,"bear":10},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":3.07,"net_buyback":0},"second_stage":{"bull_cagr_pct":6,"base_cagr_pct":2},"max_dd":{"lo":-60,"hi":-45,"basis":"空頭情境五年終點約−58%（55元×10倍＝550元，對現價1,305元）；2024年營收年減31.16%顯示獲利會隨建廠週期擺盪；過去26週已漲48.5%，回吐空間大；歷史最大回撤事實表未涵蓋，範圍取−45%至−60%","trigger_time":null},"basis":{"bull":"AI帶動台積電資本支出到2028年後仍維持高檔，美國後續廠持續發包，毛利率守在22%以上：EPS由2027年116元增至2031年158元，終端17倍，介於現行forward 15.98倍與trailing 19.81倍之間（同業倍數事實表未涵蓋）","base":"2027–2028年貼近共識略低（客戶壓價），2029年見頂後建廠放緩，毛利率回到19%附近：2031年EPS 108元，終端14倍，低於現行forward 15.98倍，反映獲利已過高峰","bear":"台積電在2028年前後放緩建廠，接單斷層使營收重演2024年年減三成，毛利率回到15%以下：2031年EPS 55元，終端10倍；機率30%依據2024年前例、毛利率四年最高與客戶壓價"},"endo_ceiling_exceeded":false},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"2024年營收年減31.16%（688.9億元降至474.2億元）；2023年毛利率只有10.93%；營收近四年兩度大幅擺盪","assumption":"台積電資本支出在2028年後仍維持高檔，新接單接得上在手訂單的消化速度","consequence":"若2028–2029年客戶建廠放緩，營收回到2024年水準、毛利率回到15%以下，2031年EPS約55元，以10倍計約550元，五年虧損近六成","ruling":"採納：列為空頭情境，機率30%；與唯一致命點同源（台積電下修資本支出是這個故事的起點），不另立","watch":"台積電每季資本支出指引；漢唐法說在手訂單是否較前次下滑20%以上","evidence_refs":["supply_demand_durability#3","end_markets#6"],"fact_refs":["f_kpi5_backlog","f_kpi1_gaap"]},{"view":"論點失敗","evidence":"亞翔在手訂單約4,400億元、漢唐約1,939億元，差距由2025年6月約2倍擴大到約2.3倍；台南案兩家分層分工","assumption":"漢唐在台積電新廠仍拿主要份額","consequence":"若新廠主要樓層改發給亞翔，漢唐的接單斷層會提早到來，毛利率在搶單下先跌","ruling":"部分採納：9月報導中漢唐的引用值是5月底舊數字，比較時點不一致，還不足以判定份額下滑；護城河趨勢因此只給穩定、不給擴大","watch":"兩家同期揭露的在手訂單比值是否跌破0.4倍","evidence_refs":["competitive_share_entrants#3","competitive_share_entrants#2"],"fact_refs":["f_kpi5_backlog"]},{"view":"論點成功但股東經濟變差","evidence":"管理層稱後續訂單面對客戶價格壓力，毛利率目標只求維持；最大考驗是人才、電力、物料與人工成本；2026年1月在亞利桑那購地約4,100萬美元","assumption":"營收擴張的同時，毛利率能守在23%附近","consequence":"訂單與營收照預期成長，但美國人工成本與總價合約超支讓毛利率回到19%–20%，EPS成長落後營收；成長一放緩，預收倒流使自由現金流轉負，配息能力跟著下降","ruling":"部分採納：基本情境2027年EPS取108元，略低於共識110.73元","watch":"單季毛利率是否連兩季低於21%；營業現金流是否低於淨利","evidence_refs":["end_markets#3","channel_business_model_shift#1","major_events#0"],"fact_refs":["f_kpi1_gaap","f_kpi4","f_consensus_eps_fy2"]},{"view":"價格已反映太多","evidence":"26週漲48.5%；trailing P/E 19.81倍、P/S 2.86倍都是四個年度端點最高；共識已預期2027年EPS年增35.5%，2028年只剩8.9%","assumption":"市場會一直給峰值獲利14–16倍","consequence":"2027年即使符合共識也缺乏上修推力；當市場開始定價2028年的放緩，倍數可能壓到10–12倍","ruling":"採納，結論是等回踩。現在就買的最強論證：FY2027E只要11.79倍、殖利率3.07%、在手訂單約為2025年營收的2.9倍，外資預估台積電資本支出到2028年續增，2027–2028年獲利能見度是近四年最高。反駁點是這段能見度已在漲幅裡，五年報酬取決於能見度之外的2029–2031年","watch":"股價是否回到1,100元以下；共識2028年EPS是否上修","evidence_refs":["capital_markets_pricing#1"],"fact_refs":["f_week26_return_pct","f_pe_current","f_pe_percentile","f_ps_percentile","f_consensus_eps_fy2","f_consensus_eps_fy3"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 None → 本次 ✅","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=None","side_b":"本次 ma=✅","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 None → 本次 1305.0","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=None","side_b":"本次 price_at_dd=1305.0","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"一致判斷：2028年前的需求能見度","cause":null,"prior_field":null,"side_a":"管理層：高科技建廠供不應求，景氣看到2029年，瓶頸是人力不是訂單","side_b":"台積電：2026年資本支出上修至600–640億美元，2028年起大幅加速；外資估2027年770億美元、2028年860–900億美元","ruling":"一致：2028年前的需求有公司與客戶雙方背書，爭點只在2029年之後","evidence_level":"中（法說轉述與外資預估）","settle_metric":"台積電2027年1月公布的資本支出指引","if_then":["若2027年指引不低於770億美元，則維持基本情境2028年EPS 118元","若指引低於2026年實際值，則改走空頭情境並清倉"],"evidence_refs":["supply_demand_durability#1","supply_demand_durability#2","supply_demand_durability#3"]},{"axis":"競爭位置：份額領先，接單卻落後","cause":null,"prior_field":null,"side_a":"富果稱台積電12吋廠近八成無塵室由漢唐承包；優分析稱漢唐在台灣12吋廠市占逾七成（產業估計未查證）","side_b":"亞翔在手訂單約4,400億元，為漢唐1,939億元的2.3倍，差距比2025年6月的約2倍擴大","ruling":"可調和（程度差異）：兩家客戶組合不同，且漢唐的1,939億元是5月底舊值；但亞翔接單動能較強是事實，護城河只給穩定","evidence_level":"中（媒體轉述，口徑與時點不一）","settle_metric":"兩家同期揭露的在手訂單比值（目前約0.44倍）","if_then":["若比值跌破0.4倍且漢唐在手訂單較5月底下滑，則護城河趨勢改判縮減，已持有者減碼一半","若比值回升到0.5倍以上，則把空頭機率由30%降到25%"],"evidence_refs":["competitive_share_entrants#3","competitive_share_entrants#1","competitive_share_entrants#0","customer_concentration_credit#0"]},{"axis":"供需與定價：供不應求卻被壓價","cause":null,"prior_field":null,"side_a":"管理層稱建廠需求供不應求","side_b":"同一場法說稱後續訂單面對客戶價格壓力，毛利率目標只求維持現水準","ruling":"可調和：需求緊，但買方集中於台積電，緊俏轉成的是量而不是更高毛利；毛利率在23%附近見頂的機率高於續升","evidence_level":"中（法說轉述）","settle_metric":"2026年第三、四季單季毛利率","if_then":["若連兩季毛利率低於21%，則基本情境2027年EPS下修到100元以下，已持有者減碼一半、未持有者不追","若毛利率守在23%以上且在手訂單超過2,200億元，則上修基本情境並重算進場價位"],"evidence_refs":["end_markets#3","supply_demand_durability#1","end_markets#4"]},{"axis":"現金流品質：自由現金流遠高於淨利","cause":null,"prior_field":null,"side_a":"2025年自由現金流290.6億元，為淨利的3.2倍；近四季自由現金流利潤率33.49%，同業在9%–17%","side_b":"資本支出近零，超出淨利的現金推論來自客戶預收，接單放緩時會倒流（資產負債表事實表未涵蓋）","ruling":"可調和：強現金流是預收模式的時間差，不代表獲利品質高於淨利；估值與配息能力以淨利為準","evidence_level":"低（推論，缺資產負債表）","settle_metric":"營業現金流÷淨利","if_then":["若營業現金流連兩季低於淨利且在手訂單下滑，則視為預收倒流開始，空頭機率上調至35%並維持不追"]},{"axis":"美國業務的政策彈性","cause":null,"prior_field":null,"side_a":"美國占2026年第一季營收56%；美台協議關稅上限15%，在美建廠的台灣企業可免232關稅進口設備；漢唐在美採在地聘用","side_b":"2024年法說：美中貿易戰使海外客戶建廠意願低，海外營收占比降到一成以下（來源頁未能確認）","ruling":"可調和：2024年的下滑是客戶出海意願問題，貿易協議已扭轉；但這證明海外營收對政策高度敏感，美國占比過半後敏感度更高","evidence_level":"中","settle_metric":"美國營收占比與台積電亞利桑那後續廠進度","if_then":["若美國營收占比跌破30%或亞利桑那後續廠延後，則已持有者減碼一半","若美國占比維持過半且P3如期發包，則維持基本情境"],"evidence_refs":["geo_supply_chain#2","geo_supply_chain#0","geo_supply_chain#1","reg_tariff_export#0"]},{"axis":"裁決：觀望，還是現在就買","cause":null,"prior_field":null,"side_a":"現在就買：FY2027E 11.79倍、殖利率3.07%、在手訂單約為2025年營收的2.9倍，2027–2028年獲利能見度是近四年最高","side_b":"觀望：分母在毛利率高點，五年基本情境含息年化約6%；空頭情境約−58%，機率30%","ruling":"選觀望。依據是五年基本情境報酬低於8%，多空機率加權後上檔只約為下檔的1.5倍；能見度內的獲利已反映在半年48.5%的漲幅裡","evidence_level":"中","settle_metric":"股價與在手訂單","if_then":["若股價回落至1,100元以下且在手訂單不低於1,500億元，則分批反買，首批為目標部位三分之一","若股價續漲但毛利率與在手訂單未再創高，則不追","若台積電2027年資本支出指引不低於770億美元且漢唐在手訂單超過2,200億元，則上修基本情境並重算進場價位"],"evidence_refs":["capital_markets_pricing#1"]}],"triggers":[{"n":1,"text":"股價回落至1,100元以下，且最近一次法說在手訂單仍不低於1,500億元，分批建立首倉","type":"估值rearm","maps_to":"action_conditions.rearm_trigger","metric":"股價；法說揭露的在手訂單","threshold":"股價≤1,100元且在手訂單≥1,500億元","action":"分批反買：首批為目標部位三分之一","source_freq":"每日股價；每季法說","date":null},{"n":2,"text":"台積電年度資本支出指引低於前一年實際值，或宣布延後已公布的新廠動工","type":"Single Thing","maps_to":"thesis.single_thing","metric":"台積電資本支出指引","threshold":"2027年指引低於2026年實際值","action":"清倉並取消進場計畫","source_freq":"台積電每季法說","date":"2027-01"},{"n":3,"text":"單季毛利率連兩季低於21%，代表客戶壓價已反映到新案","type":"風險","maps_to":"R1","metric":"單季毛利率","threshold":"連2季<21%（2026年第二季23.64%）","action":"減碼一半；未持有者把進場價位下修至1,000元","source_freq":"每季財報","date":null,"evidence_refs":["end_markets#3"]},{"n":4,"text":"漢唐對亞翔的在手訂單比值跌破0.4倍，或台積電新廠主要樓層發包給亞翔","type":"風險","maps_to":"R2","metric":"在手訂單比值","threshold":"<0.4倍（2026年9月報導約0.44倍）","action":"減碼一半，護城河趨勢改判縮減","source_freq":"兩家法說與產業報導，約每半年","date":null,"evidence_refs":["competitive_share_entrants#3","competitive_share_entrants#2"]},{"n":5,"text":"美國營收占比跌破30%，或台積電亞利桑那後續廠延後","type":"風險","maps_to":"R3","metric":"美國營收占比","threshold":"<30%（2026年第一季56%）","action":"減碼一半","source_freq":"每季法說","date":null,"evidence_refs":["geo_supply_chain#2"]},{"n":6,"text":"2026年全年EPS達75元以上，驗證在手訂單如期轉成獲利","type":"假設驗證","maps_to":"H1","metric":"2026年稀釋EPS","threshold":"≥75元（共識81.69元）","action":"未達則下修基本情境，空頭機率上調至35%","source_freq":"年報","date":"2027-03"},{"n":7,"text":"台積電公布2027年資本支出指引、漢唐全年法說之後複審","type":"複審日期","maps_to":"decision","metric":"台積電資本支出指引；漢唐在手訂單","threshold":"指引≥770億美元且在手訂單≥2,200億元時上修基本情境","action":"重跑完整判斷","source_freq":"每年一次","date":"2027-03"}],"kill_metrics":[{"metric":"法說揭露的在手訂單","bear_threshold":"較前次揭露下滑20%以上（以1,939億元計，低於約1,550億元）","window":"每季法說","source":"漢唐法說會","last_status":"ok"},{"metric":"單季毛利率","bear_threshold":"連兩季低於21%","window":"每季財報","source":"漢唐季報","last_status":"ok"},{"metric":"台積電年度資本支出指引","bear_threshold":"低於前一年實際值","window":"每年1月法說","source":"台積電法說會","last_status":"ok"},{"metric":"漢唐在手訂單÷亞翔在手訂單","bear_threshold":"低於0.4倍","window":"約每半年（兩家同期揭露）","source":"兩家法說會、工商時報與經濟日報產業報導","last_status":"warning"},{"metric":"月營收年增率","bear_threshold":"連三個月轉負","window":"每月10日前","source":"公開資訊觀測站月營收","last_status":"ok"}],"evidence_dismissed":[],"action_conditions":{"rearm_trigger":"股價回落至1,100元以下，且最近一次法說在手訂單仍不低於1,500億元","exec_line":"觸發後分批進場，首批為目標部位三分之一，其餘等單季毛利率守住21%以上再加；台積電下修資本支出則取消計畫","holding_cap":"單檔上限6%；循環股深回撤可能逾五成，持有者需有心理準備，不因波動本身砍倉"}},"decision_inputs":{"signal":"C","ma":"✅","cycle_position":"中循環","cycle_verdict":"等回踩","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":null,"cycle_gates_pass":false,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等股價回落至1,100元以下（基本情境五年年化報酬回到約10%），且最近一次法說在手訂單不低於1,500億元"},"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"6","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='C'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='✅'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"輸入缺(momentum_overheated=null)，依保守方向處理：不視為觸發","input_gap":["momentum_overheated"]},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":true,"basis":"signal='C'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='C', runway='🟡', val='🟠', moat_trend='→', week26=48.5, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='循環/商品', cycle_position='中循環', moat='B', moat_trend='→', cycle_gates_pass=False"},{"row":"6/7/7a-verdict","condition":"Soft Veto 生效 → 觀望（max-severity wins；8a/8b 未能繞過）","hit":true,"basis":"soft_veto_rows=['6']"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":null,"requires_critic":[]},"thesis":{"H":[{"id":"H1","text":"在手訂單如期轉成獲利，2026–2027年EPS接近共識（81.69元、110.73元）","2y":"2026年EPS不低於75元、2027年不低於100元","5y":null,"10y":null,"threshold":"2026年EPS≥75元；2027年EPS≥100元（約共識九成）","source":"季報與年報、每月營收公告","drift_rule":"近四季EPS偏離本路徑連2季≥5%為削弱、連3季≥10%為反轉"},{"id":"H2","text":"毛利率高位有一部分是結構性的（規模與美國案），不會回到2023年一成左右的水準","2y":null,"5y":"2027–2030年年度毛利率維持18%以上","10y":null,"threshold":"年度毛利率≥18%（2023年10.93%、2025年20.02%、2026年第二季23.64%）","source":"季報","drift_rule":"近四季毛利率低於18%門檻、連4季偏離≥5%為削弱，連6季≥10%為反轉"},{"id":"H3","text":"隨台積電赴美保住主承包地位，接單規模不再被亞翔拉開","2y":null,"5y":"美國營收占比維持40%以上，漢唐對亞翔在手訂單比值不低於0.4倍","10y":null,"threshold":"在手訂單比值≥0.4倍（目前約0.44倍）；美國營收占比≥40%（2026年第一季56%）","source":"兩家法說會、工商時報與經濟日報產業報導","drift_rule":"比值較0.44倍連4季偏低≥5%為削弱、連6季≥10%為反轉"}],"R":[{"id":"R1","text":"客戶壓價使新案毛利率下滑","h_ref":"H2","clock":"⚡","threshold":"單季毛利率連2季低於21%","evidence_refs":["end_markets#3"]},{"id":"R2","text":"亞翔與其他承包商分走台積電新廠案","h_ref":"H3","clock":"🔥","threshold":"在手訂單比值低於0.4倍，或台積電新廠主要樓層發包給亞翔","evidence_refs":["competitive_share_entrants#3","competitive_share_entrants#2"]},{"id":"R3","text":"美國建廠政策逆轉：2024年貿易戰期間客戶建廠意願低，海外營收占比曾降到一成以下","h_ref":"H3","clock":"🔥","threshold":"美國營收占比低於30%，或台積電亞利桑那後續廠延後","evidence_refs":["geo_supply_chain#2","reg_tariff_export#0"]},{"id":"R4","text":"客戶建廠週期反轉，營收重演2024年的年減三成","h_ref":"H1","clock":"🐢","threshold":"法說揭露的在手訂單較前次下滑20%以上","evidence_refs":["supply_demand_durability#3"]},{"id":"R5","text":"人力瓶頸拖慢認列並推高成本","h_ref":"H1","clock":"⚡","threshold":"月營收年增率連3個月轉負，而在手訂單沒有下降","evidence_refs":["end_markets#4","channel_business_model_shift#1"]}],"single_thing":{"description":"台積電下修或延後資本支出：年度指引低於前一年實際值，或宣布延後已公布的新廠（台灣或亞利桑那）動工","why_fatal":"漢唐的最大客戶是台積電（承包其12吋廠近八成無塵室，產業估計），共識2027–2028年EPS 110.73元、120.63元仰賴新接單；接單一停，在手訂單在2–2.5年內認列完，營收重演2024年年減31%，毛利率高位也失去支撐","if_happens":"EPS路徑改走空頭情境，取消進場計畫；已持有者清倉","how_monitor":"台積電每季法說的資本支出指引（下一場在2027年1月）；漢唐法說在手訂單；每月營收","probability":"約15%（12–24個月）：台積電2026年資本支出已上修至600–640億美元，外資預估2027–2028年續增"}},"appendix_a":{"growth_durability":5,"quality_score":7,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":11.79,"peg_fy2":0.33,"stress":{"pass":2,"total":4}},"eps_meta":{"base_eps_path":{"FY2025A":47.73,"FY2026E":81.69,"FY2027E":110.73,"FY2028E":120.63},"fy_end_month":12,"eps_basis":"稀釋EPS（新台幣）；共識為Koyfin快照美元值，依2026-10-09匯率31.912換算；共識家數事實表未涵蓋"},"catalysts":[{"date":"2026-11","date_precision":"month","type":"other","event":"漢唐公布2026年第三季財報","impact":"中","watch":"單季毛利率是否守在23%以上"},{"date":"2027-01","date_precision":"month","type":"capacity","event":"台積電年度法說公布2027年資本支出指引","impact":"高","watch":"指引是否不低於外資預估的770億美元"},{"date":"2027-03","date_precision":"month","type":"guidance","event":"漢唐全年財報與法說（在手訂單與2027年展望）","impact":"高","watch":"在手訂單是否不低於1,939億元、美國營收占比是否維持過半"}]}
```

---

## 尾段：回覆格式

只回一個 JSON 陣列，①–⑧ 每條一個元素，八個全出，不得跳號、不得多列，陣列外不得有任何文字（不加前言、不加 markdown 圍欄、不加附註）：

```json
[{"item": "①", "light": "🔴|🟡|🟢", "judgment_path": "$.路徑", "reason": "一句話"}]
```
