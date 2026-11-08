你是 DD 管線 v20 的判斷層閘（gate），標的 TPR（20261108）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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
<!-- 2026-10-20 ⑤ 改程式判定；來源 gate_contract §⑤／critic-gates ⑤ 同日改成同一條規則（核心軸 none 🔴、非核心 🟡）；重新濃縮時以本卡 ⑤ 為準 -->

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

⑤ 覆蓋面掃描——**燈號由程式判定**（核心軸 none→🔴；只有非核心軸 none→🟡；全 found／not_applicable→🟢），bundle 附程式結果，你回的 ⑤ 燈號會被覆寫。你只評論：facts.json 點名 status="none"／"not_applicable" 的軸，查詢是否切題（不以查詢次數計）、判斷有沒有交代缺口對結論的影響；不得因缺軸自行升 🔴。

⑥ 量化模組完整性抽查（強制）——(i) `moat.roic_durability.reinvest_rate`／`.roiic` 有沒有 `.formula_note` 真算（寫「估計約 X%」無算式＝🔴）；`.endo_ceiling` 是否與共識 EPS CAGR（facts.json）交叉檢查，天花板 < CAGR 且 `reasoning` 未處理＝🔴。(ii) `scenario_inputs` 的 Bull/Base/Bear EPS 是否有實質價差（Bull 幾乎等於 Base、只靠倍數撐估值＝退化，🔴）；`scenario_inputs.valuation_basis`＝`sales_multiple`（虧損公司，程式決定）時改查 Bull/Base 的營收路徑（`rev`）：Bull 終端營收須實質高於 Base、Bull 前兩年不得與 Base 相同，只靠終端 EV/S 撐價差＝退化，🔴；並看 Bear 的 `net_debt_y5`／`shares_y5` 是否反映該情境的融資缺口與稀釋（債重公司 Bear 沿用目前淨負債與股數＝樂觀，🟡）。(iii) `decision_inputs.irr_base_pct`／`ev5y_pct`／`asym_ratio` 缺省或 null 合法（程式回填），但 ROIIC 缺輸入、口徑或算式仍為實質問題。[gate_contract §⑥]

⑦ 數字新鮮度——`judgment.json` 引用的每個營運指標，是否不比 facts.json 的 `latest_quarter_kpis[].as_of` 對應項目舊？有一個更舊即 🔴。`decision_inputs.consensus_rev_3m_pct` 若依附 `stale=true` 來源，確認未被當唯一依據；引用摘要內容的欄位須標「來源：摘要」。[gate_contract §⑦]

⑧ 前份漂移歸因（QC-49）——facts.json 的 `prior_dd` 存在時，`drift_watch` 20 欄中有變動的每一欄是否都映射到 `contradictions[]` 一個帶 `cause` 的條目（可多欄共用一條目）、且主因站得住；**裁決／核心假設／情境方法變更不得併入純價格原因**；漏欄或無歸因＝🔴；前份該欄本身空或缺欄者不計，給 🟡 或 🟢。無前份時填 🟢 並註「無前份」。[gate_contract §⑧]
  - `axis` 以 `[程式歸因]` 開頭的條目是程式算的（均線、現價、期望報酬拆解、裁決、角色）。「期望報酬拆解」兩條是程式用本次情境先換情境、再換股價算出的數字（asym_ratio／ev5y_pct／irr_base_pct／bull_5y_price／bear_5y_price），視為已歸因，其中「價格變動」只是股價效果，不適用「不得併入純價格原因」。裁決／角色條目是反事實結果（逐一把矩陣輸入改回前份值重算），視為已歸因；其中「價格變動」是反事實證明估值燈單獨改變了裁決，不適用上面「不得併入純價格原因」，不要為此給 🔴（2026-09-24）。
  - QC-49 承繼（90 天內翻面須引前次已發火觸發器）只比方向：進場／觀望／迴避。「進場」與「進場·條件式」同方向，角色（核心／衛星）變動也不在 QC-49 範圍；判斷者答 `decision_inputs.qc49_inherit_prior`，前次裁決與角色由程式帶入。

## (a)(b) 兩項強制職責（2026-08-06 拍板，不得因精簡拿掉）

(a) 覆蓋面掃描：逐軸點名「哪一軸整個沒查」，做法同 checklist ⑤（燈號由程式判定，你只評論）。
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

### 判斷檔 `fact_refs` 引到的事實（29 條）
- `f_kpi0_gaap`（q1_business）｜營收（GAAP）＝1876.6 USD M｜期間與口徑：Q4 FY2026（季末 2026-06-27，公告於 2026-08-13）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q4 FY26 財報新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/1116132/000114036126032624/ef20079840_ex99-1.htm（numbers.latest_quarter_kpis.items[0]，as_of Q4 FY2026（季末 2026-06-27，公告於 2026-08-13））
- `f_kpi1_non_gaap`（q1_business）｜Non-GAAP 營業利益／利益率＝19.3 %｜期間與口徑：Q4 FY2026（季末 2026-06-27，公告於 2026-08-13）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q4 FY26 財報新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/1116132/000114036126032624/ef20079840_ex99-1.htm（numbers.latest_quarter_kpis.items[1]，as_of Q4 FY2026（季末 2026-06-27，公告於 2026-08-13））
- `f_kpi2_gaap`（q1_business）｜GAAP 營業利益／利益率＝23.6 %｜期間與口徑：Q4 FY2026（季末 2026-06-27，公告於 2026-08-13）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q4 FY26 財報新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/1116132/000114036126032624/ef20079840_ex99-1.htm（numbers.latest_quarter_kpis.items[2]，as_of Q4 FY2026（季末 2026-06-27，公告於 2026-08-13））
- `f_earnings_recency`（q1_business）｜最近一次財報日＝2026-11-05 date｜期間與口徑：2026-11-05／距今 2 個交易日｜kind：realized
  - 來源：—（numbers.earnings_recency，as_of 2026-11-05）
- `f_peer_tpr_gross_margin_pct`（q2_moat）｜TPR 毛利率＝78.31 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.TPR.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_tpr_operating_margin_pct`（q2_moat）｜TPR 營業利益率＝24.53 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.TPR.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_tpr_fcf_margin_pct`（q2_moat）｜TPR FCF 利潤率＝22.95 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.TPR.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝7.96 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-11-07）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝8.89 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-11-07）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝10.08 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-11-07）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝8599.36 USD m｜期間與口徑：2026-11-08／yfinance revenue_estimate 0y 平均（18 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝9043.81 USD m｜期間與口徑：2026-11-08／yfinance revenue_estimate +1y 平均（19 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi3`（q4_capital）｜自由現金流＝469.0 USD M｜期間與口徑：Q4 FY2026（季末 2026-06-27，公告於 2026-08-13）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q4 FY26 財報新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/1116132/000114036126032624/ef20079840_ex99-1.htm（numbers.latest_quarter_kpis.items[3]，as_of Q4 FY2026（季末 2026-06-27，公告於 2026-08-13））
- `f_kpi4_sbc`（q4_capital）｜SBC 占營業利益＝7.0 %｜期間與口徑：Q4 FY2026（季末 2026-06-27，公告於 2026-08-13）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q4 FY26 財報新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/1116132/000114036126032624/ef20079840_ex99-1.htm（Schedule 8）（numbers.latest_quarter_kpis.items[4]，as_of Q4 FY2026（季末 2026-06-27，公告於 2026-08-13））
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝3472.0 USD m｜期間與口徑：2026-11-08／yfinance 最新一季：總債務 4254.0、現金 782.0（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝196.52 m shares｜期間與口徑：2026-11-08／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝132.8 USD｜期間與口徑：2026-11-06（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-11-06（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝16.68 x｜期間與口徑：2026-11-07／分母＝FY1 EPS 7.96，分子＝快照價 132.8｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-11-07）
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝17.07 x｜期間與口徑：2026-11-06（RTH 收盤，UTC）／4 個年度端點內的分位＝7.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-11-06（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝7.0 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝75.8 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝77.9 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_rsi14`（q5_valuation）｜RSI(14)＝70.47｜期間與口徑：2026-11-06（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-11-06（RTH 收盤，UTC））
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝0.15 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-11-06（RTH 收盤，UTC））
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝1.252 %｜期間與口徑：2026-11-08／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-11-08）
- `f_ma_w52`（q5_valuation）｜52 週均線＝133.07 USD｜期間與口徑：2026-11-08／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝13.88 %｜期間與口徑：2026-08-13 → 2026-11-07／FY1 共識 EPS 6.99 → 7.96（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-11-07）
- `f_peer_mc_gross_margin_pct`（q2_moat）｜MC 毛利率＝34.36 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MC.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_cfr_fcf_margin_pct`（q2_moat）｜CFR FCF 利潤率＝24.77 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CFR.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）

### findings_digest 中方向為負或來源衝突的條目（12 條）
- `competitive_share_entrants#2`（competitive_share_entrants｜方向 -｜狀態 ok）：Michael Kors（Capri）為 Coach 在輕奢手袋的主要對手；Polene、Jacquemus 等小眾品牌透過社群與稀缺性吸引年輕客群，轉售平台（The RealReal、Vestiaire）形成間接競爭。來源為彙整型文章，非一手數據。
  - 來源：retailboss.co / Morningstar 搜尋結果彙整（Coach Is Now 89% Of Tapestry…）（as_of 2026-09-30）｜affects：moat_trend、thesis.R、decision_inputs.bear
- `regulatory_antitrust#1`（regulatory_antitrust｜方向 -｜狀態 ok）：法學評論稱 FTC 勝訴形成先例，可能限制「輕奢」層級未來的併購整合。
  - 來源：WUSTL Law Review (2026-02-25)（as_of 2026-02-25）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：Tapestry 預估美國關稅將使 FY2026 成本增加約 1.6 億美元，預期 2028 年前完全抵銷；FY2026 EPS 指引 5.30–5.45 美元，其中約 0.60 美元缺口來自關稅（含取消 de minimis 免稅）。
  - 來源：Mexico Business News: Coach Owner Warns US Tariffs May Cost US$160 Million in FY2026（發布日以 2025-08-14 財報日近似，頁面日期未讀取）（as_of 2025-08-14）｜affects：valuation、decision_inputs.bear
- `reg_tariff_export#1`（reg_tariff_export｜方向 -｜狀態 ok）：手袋多在越南、柬埔寨、菲律賓、印度生產，搜尋結果未顯示中國為主要關稅暴露來源；另已累計逾 2 億美元 IEEPA 與對等關稅成本。
  - 來源：同上搜尋彙整（Mexico Business News／Inside Retail Asia，2025-08）（as_of 2025-08-14）｜affects：moat_trend、decision_inputs.bear
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：搜尋摘要稱：越南、柬埔寨、菲律賓合計佔 Tapestry 約 70% 生產；Coach 與 Kate Spade 多數手袋在越南、柬埔寨、菲律賓、印度製造（東南亞集中）。
  - 來源：Inside Retail Asia - Can Coach carry the weight as tariffs bear down on Tapestry?（as_of 2025-08-18）｜affects：decision_inputs.bear、thesis.R
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：搜尋摘要稱：中國僅佔 Tapestry 約 10% 採購；三大生產國面臨 10% 關稅，關稅衝擊 FY2026 約 1.6 億美元。
  - 來源：Inside Retail Asia / Mexico Business News (Coach Owner Tapestry Sees US$160 Million Profit Hit from Tariffs)（as_of 2025-08-18）｜affects：valuation、thesis.R
- `geo_supply_chain#2`（geo_supply_chain｜方向 -｜狀態 ok）：搜尋摘要稱：Tapestry 在 FY2026 10-K 列美中關係不確定性與貿易協定參與變動為風險因子；國際業務約佔淨銷售 40%。10-K 全文未讀，as_of 取會計年度結束日。
  - 來源：SEC Form 10-K FY2026 (period ending 2026-06-27)（as_of 2026-06-27）｜affects：decision_inputs.bear、thesis.R
- `end_markets#1`（end_markets｜方向 -｜狀態 ok）：Kate Spade 前九個月淨銷售 -11.1% 至 $839.8M；Q4 -7% 至 $235.1M；管理層稱精簡動作對營收的拖累大於預期。
  - 來源：SEC 10-Q (tpr-20260328) 與 WWD: Tapestry Q4 earnings（搜尋摘要）（as_of 2026-08-13）｜affects：moat_trend、thesis.R、decision_inputs.bear
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：Tapestry FY2026 10-K 風險因素稱：消費者愈來愈常用 AI 購物助理來探索商品、比價、下單，可能改變商務並影響公司吸引並留住數位平台客戶的能力（as_of 為 FY2026 財年結束日，實際申報日未確認）
  - 來源：Tapestry Inc. Form 10-K FY2026 (SEC EDGAR)（as_of 2026-06-27）｜affects：decision_inputs.bear、moat_trend
- `substitute_technology#1`（substitute_technology｜方向 -｜狀態 ok）：二手奢侈品市場估計 2026 年約 416 億美元（2025 年約 379 億），成長速度約為一手市場三倍；Gen Z 衣櫃 45% 的手袋為二手（來源為聚合文章，數字未回溯至原始報告）
  - 來源：Luxury Resale Market: 2026 Gen Z $41B Boom Disrupts Status (editorialge.com)；Forbes Resale Market 2026 (2025-12-16)（as_of 2025-12-16）｜affects：thesis.R、decision_inputs.bear
- `major_events#0`（major_events｜方向 -｜狀態 ok）：兩宗與已終止之 Capri 併購相關的證券集體訴訟（2024-12-23、2025-01-28 於德拉瓦聯邦地院提起）針對 Tapestry 及高管；公司 2025-07-14 聲請駁回，10-K（FY2026）仍列為未決事項。
  - 來源：SEC EDGAR 10-K FY2026 財報附註（訴訟）（as_of 2026-08-13）｜affects：decision_inputs.bear、triggers
- `lawsuit_class_action#0`（lawsuit_class_action｜方向 -｜狀態 ok）：Capri 併購終止後的兩宗證券集體訴訟仍未決，公司 2025-07-14 聲請駁回。
  - 來源：SEC EDGAR 10-K FY2026 財報附註（訴訟）（as_of 2026-08-13）｜affects：decision_inputs.bear、triggers

### 事實表自陳的缺口（2 條）
- q2_moat：evidence.numbers.peer_financials 該欄整欄為 null（常見於未單獨揭露研發的業者），事實表 agent 若能從財報補就補，補不到即為缺口，判斷者不得自行估。
- q6_how_wrong：digest.qa_flags 有 4 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TPR_20261108/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":268.2,"bear_5y_price":70.4,"p_bull_pct":25,"p_bear_pct":30,"upside_5y_pct":38.9,"ev5y_pct":28.9,"irr_base_pct":6.8,"asym_ratio":1.8,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":8.3,"pe":16.0,"basis":"FY2027 公司財測中點 8.30 美元（2026-11-05 上調），共識快照 7.96 美元為上調前數字；終端倍數同樣以當年度 EPS 為分母。"},"eps":{"bull":[8.6,9.9,11.4,13.1,14.9],"base":[8.35,9.2,10.2,11.25,12.3],"bear":[8.0,7.6,7.0,6.6,6.4]},"pe":{"bull":18,"base":15,"bear":11},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":1.252,"net_buyback":0},"second_stage":{"bull_cagr_pct":10,"base_cagr_pct":7},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### TPR_Q4_2026_Earnings_Call_20260813.md
- 2026-08-13｜CFO｜guidance：FY27 營收財測 84–85 億美元，中個位數成長（原話："$8.4 billion to $8.5 billion"）
- 2026-08-13｜CFO｜guidance：FY27 EPS 財測 7.80–7.90 美元（原話："we expect EPS of $7.80 to $7.90"）
- 2026-08-13｜CFO｜guidance：FY27 營業利益率預期擴張 50bp 至近 24%（原話："operating margin expansion of 50 basis points to nearly 24%"）
- 2026-08-13｜CFO｜guidance：FY27 北美營收預期低個位數成長（原話："In North America, we expect revenue to increase low single digits"）
- 2026-08-13｜CFO｜guidance：FY27 歐洲與大中華預期中十位數成長（原話："we expect growth of mid-teens"）
- 2026-08-13｜CFO｜guidance：FY27 Kate Spade 營收預期高個位數衰退（原話："a high single-digit decline at Kate Spade"）
- 2026-08-13｜CFO｜guidance：FY27 Kate Spade 預期小額營業虧損（原話："expect a modest operating loss"）
- 2026-08-13｜CFO｜guidance：Q1 EPS 財測約 1.55 美元（原話："Q1 EPS is forecasted to be approximately $1.55"）
- 2026-08-13｜CFO｜guidance：Q1 Coach 兩年疊加成長中 30% 出頭（原話："mid-30s growth on a 2-year stack basis"）
- 2026-08-13｜CFO｜guidance：全年上半年與下半年營收節奏：上半年高個位數（原話："grow high single digits in the first half of the year"）
- 2026-08-13｜CFO｜guidance：FY27 自由現金流預期接近 17 億美元（原話："we anticipate adjusted free cash flow to approach $1.7 billion"）
- 2026-08-13｜CFO｜guidance：FY27 資本支出（含雲端運算成本）約 3 億美元（原話："to be in the area of $300 million or 3% to 4% of revenue"）
- 2026-08-13｜CFO｜guidance：FY27 Coach 淨增 40–50 家門市（原話："between 40 and 50 doors is our expectation on a net basis at Coach"）
- 2026-08-13｜CFO｜margin：FY27 毛利率預期增加約 30bp（營益率拆解：毛利率加 SG&A 槓桿）（原話："gross margin to increase by approximately 30 basis points"）
- 2026-08-13｜CFO｜margin：財測假設美國進口關稅率落在 20% 中段（原話："a mid-20s percent tariff rate on U.S. imports"）
- 2026-08-13｜CFO｜margin：關稅對損益的影響上半年為小幅助益，下半年轉為逆風，獲利逐季不均（原話："tariffs providing a modest benefit in the first half of the year"）
- 2026-08-13｜CFO｜margin：Q4 毛利率拆解：含出售 Stuart Weitzman 的 60bp 有利影響（原話："a favorable 60 basis point impact"）
- 2026-08-13｜CFO｜margin：Q4 關稅與關務成本逆風約 60bp（原話："a tariff and duty headwind of approximately 60 basis"）
- 2026-08-13｜CFO｜margin：Q4 行銷費用占營收 14%，年增 130bp（原話："a 130 basis point increase in marketing, which represented 14% of sales"）
- 2026-08-13｜CFO｜margin：Q4 EPS 受稅率偏高拖累逾 0.05 美元（原話："a higher tax rate versus plan due to a number of discrete items"）
- 2026-08-13｜CFO｜margin：Q1 營益率持平，SG&A 增加全數來自行銷（原話："higher SG&A due entirely to continued increases in marketing"）
- 2026-08-13｜CFO｜margin：回答毛利率橋時說全年逐季將不平順（原話："it's going to be a little lumpy through the year"）
- 2026-08-13｜CFO｜margin：稱毛利率財測屬審慎（原話："we think the guidance we've given is prudent"）
- 2026-08-13｜CFO｜margin：Q4 行銷槓桿比原先指引多一些，管理層稱有時點因素（原話："we came in with a little more leverage in marketing"）
- 2026-08-13｜CFO｜margin：行銷（需求創造）約占營收 12%、約 10 億美元（原話："It's about $1 billion in advertising"）
- 2026-08-13｜CFO｜commitment：FY27 財測沿用投資人日的長期財務框架（原話："low double-digit EPS growth, consistent with our long-term commitments"）
- 2026-08-13｜CFO｜commitment：FY27 預計回饋股東 17 億美元，含 13.5 億美元回購（原話："we expect to repurchase approximately $1.35 billion of shares"）
- 2026-08-13｜CFO｜commitment：董事會核准股利提高 16%（原話："Our Board approved a 16% increase in the dividend"）
- 2026-08-13｜CEO｜commitment：中期目標：Coach 展店計畫改造 2030 財年前約 80% 客流量（原話："concept to impact approximately 80% of our traffic by fiscal year '30"）
- 2026-08-13｜CEO｜commitment：管理層重申 Coach 邁向 100 億美元品牌（原話："a clear path to Coach becoming a $10 billion brand"）
- 2026-08-13｜CFO｜capital_allocation：併購前提：Coach 維持強勁、Kate Spade 回到可持續成長（原話："we will ensure Coach remains strong"）
- 2026-08-13｜CFO｜capital_allocation：長期總槓桿目標低於 2.5 倍（原話："long-term gross leverage target of below 2.5x"）
- 2026-08-13｜CFO｜guidance：全年財測不需要 Coach 其餘季度維持 Q1 同等成長（管理層稱審慎）（原話："full year guide doesn't require us to keep that same level"）
- 2026-08-13｜CFO｜product：財測假設單價（AUR）與件數都成長（原話："our guidance assumes both unit and AUR growth"）
- 2026-08-13｜Coach CEO｜product：Q4 Coach 件數持平是刻意減少促銷天數（原話："We had fewer promotion days in the fourth quarter"）
- 2026-08-13｜Coach CEO｜product：Coach 鎖定 200–500 美元價位帶（原話："We are going to be very focused on that $200 to $500 space"）
- 2026-08-13｜Coach CEO｜product：Coach 全球成長下限由中個位數調升到高個位數（原話："floor up from mid-single digits to high single digits"）
- 2026-08-13｜CEO｜product：Kate Spade 營收進展比計畫緩慢（原話："Although top line progress was more gradual than we planned"）
- 2026-08-13｜CEO｜risk：Kate Spade 品牌知名度（未輔助）尚未改善（原話："awareness more broadly has not yet improved"）
- 2026-08-13｜CEO｜customer：FY26 新客 1,100 萬人，Z 世代為主（原話："welcomed 11 million new customers to our brands, led by Gen Z"）
- 2026-08-13｜CEO｜customer：新客留存率位居客戶檔案中最高之列（原話："retention rates among the highest retention rates in our customer file"）
- 2026-08-13｜Coach CEO｜customer：中國過去行銷投入不足，現在將行銷拉到與整體一致（原話："we underinvested in China over the years"）
- 2026-08-13｜CFO｜guidance：FY27 日本預期回到成長（原話："In Japan, we're forecasting a return to growth"）
- 2026-08-13｜Coach CEO｜competition：Coach CEO 稱產業沒有進入門檻（原話："there are no barriers of entry in our space"）
- 2026-08-13｜CFO｜competition：CFO 稱雖無進入門檻，但規模門檻正在提高（原話："there are barriers to scale, and those barriers are getting higher"）

### 問答異常語氣（迴避／改口／保留）
- TPR_Q4_2026_Earnings_Call_20260813.md｜問：Boruchow：Q4 北美 Coach 成長受促銷時點移轉影響多少？Q1 低十位數 Coach 全球財測對應多少北美成長？｜答法：Coach CEO 與 CFO 未直接給出時點移轉的影響幅度，也未給 Q1 北美數字；改以兩年疊加約 30% 與「comping the comp」回應
- TPR_Q4_2026_Earnings_Call_20260813.md｜問：Binetti：毛利率橋顯示 Q1 後幾乎沒有擴張，能否說明全年路徑｜答法：CFO 未給逐季毛利率數字，只說「lumpy」、全年約 +30bp、結構性驅動因素不變，並稱財測審慎
- TPR_Q4_2026_Earnings_Call_20260813.md｜問：Yih-Tennant：Coach 北美中個位數成長，是指 Q1 還是全年？｜答法：CFO 與 Coach CEO 先後澄清；CFO 講北美 Coach 中個位數（Q1 與全年），Coach CEO 再補述 Q1 Coach 整體低十位數、全年高個位數；先前 CFO 在回答 Binetti 時亦用相同說法，此處為分析師反覆追問確認
- TPR_Q4_2026_Earnings_Call_20260813.md｜問：Yih-Tennant：你們最擔心哪個競爭對手？｜答法：Coach CEO 未點名任何競爭對手，改談「沒有進入門檻」、護城河、85 年品牌與文化穩定

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 4 | 3 |
| customer_second_source | found | 1 | 2 |
| customer_concentration_credit | found | 2 | 2 |
| supply_demand_durability | found | 4 | 4 |
| regulatory_antitrust | found | 2 | 3 |
| reg_tariff_export | found | 2 | 2 |
| geo_supply_chain | found | 4 | 4 |
| end_markets | found | 5 | 4 |
| substitute_technology | found | 3 | 4 |
| channel_business_model_shift | found | 2 | 2 |
| capital_markets_pricing | found | 5 | 4 |
| major_events | found | 2 | 4 |

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20261005","verdict":"進場","role":"衛星","H":{"status":"unavailable"},"R":{"status":"unavailable"},"single_thing":null,"kill_metrics":null,"rearm_trigger":"加碼條件：Q1 FY27 法說（約 2026-11）Coach 固定匯率成長 ≥ +10% 且手袋件數年增 ≥ 0，兩者同時成立","irr_base_pct":7.9,"ev5y_pct":35.6,"drift_watch_prior":{"dca_verdict":"進場","dca_role":"衛星","signal":"B","val":"🟡","ma":"🟡","trap":"🟡","moat_trend":"→","runway_post_y5":"🟡","asym_ratio":2.3,"ev5y_pct":35.6,"irr_base_pct":7.9,"max_dd_pct":-55,"bull_5y_price":241.2,"bear_5y_price":74.0,"p_bull_pct":25,"p_bear_pct":30,"rearm_trigger":"加碼條件：Q1 FY27 法說（約 2026-11）Coach 固定匯率成長 ≥ +10% 且手袋件數年增 ≥ 0，兩者同時成立","price_at_dd":118.12,"archetype":"品質複利成長","cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"TPR","date":"2026-11-08","schema":"v15.0","contract":"v19","company_name":"Tapestry, Inc."},"oneliner":"Coach 一個品牌撐起全部獲利：Q1 固定匯率成長 16%，全年 EPS 財測上調到 8.25–8.35 美元；現價約 16 倍，基準情境年報酬約 8%，關鍵在北美中個位數成長與 78% 毛利率能否守住。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TPR_20261108/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TPR_20261108/scenario.json","answers":{"q1_business":{"verdict":"賺的是全球年輕客群買 200–500 美元手袋的錢，利潤卡在 Coach 品牌這一節，Kate Spade 目前沒有貢獻獲利。","reasoning":"FY26 營收 80.0 億美元，Coach 69.1 億占 86%、年增 24%，Kate Spade 10.7 億、年減 10%。約 87% 經由自營門店與數位賣出，批發約 12%，沒有單一客戶超過 10%。2026-11-05 法說的最新一季毛利率 78.7%，營業利益率超過 23%；事實表的最新一季指標仍停在 Q4 FY26，Q1 FY27 數字取自逐字稿。單點依賴就是 Coach：FY27 財測 Coach 營益率約 36%，Kate Spade 小額虧損，獲利幾乎全來自一個品牌。產業在擴張期，依據是二手彙整的全球精品 2026 年成長 3–5%、美國 4–6%，以及管理層引述美國假期季中個位數成長的產業預測。供需屬供給可逆性高，所以空頭機率不壓低。","fact_refs":["f_kpi0_gaap","f_kpi1_non_gaap","f_kpi2_gaap","f_earnings_recency"],"verdict_values":{"revenue_quality":"約 87% 為自營門店與數位銷售，批發約 12%，沒有單一客戶超過 10%；收入靠品牌熱度維持，沒有合約保障。","unit_econ_note":"Q1 手袋 AUR 低雙位數成長、件數低個位數成長，200 美元以下刻意縮減；行銷占營收超過 12%，財務長說約為五年前的 4 倍，獲客投入持續加大。","archetype":{"primary":"品質複利成長","secondary":null,"confidence":"中","fingerprint":"高毛利、直營為主、自由現金流大多拿去回購"},"industry":{"clock_phase":"II","sd_verdict_source":"供給可逆性高：Coach 品牌執行長 2026-08-13 說這行沒有進入門檻，財務長同場說規模門檻在升高；需求靠品牌熱度，降溫時會反轉。","bargaining":{"up":"手袋代工集中在越南、柬埔寨、菲律賓約七成，事實表沒有單一供應商占比。","down":"直營約 87%，批發約 12%，沒有單一客戶超過 10%，下游議價力低。","geo":"美國進口關稅與美中關係是主要外部變數，國際業務約占淨銷售 40%。"},"profit_pool_dir":"五年營業利益池流向事實表未涵蓋，只有二手報導稱 Tapestry 從歐洲品牌手中取得份額。","tam_table":{"expanded":false,"reason":"事實表未涵蓋 TAM、SAM 與滲透率，管理層只說市場很大而未給數字，本次不自行估算。"}}}},"q2_moat":{"verdict":"護城河方向持平：定價力在擴大，但證據只到 Coach 一個品牌，第三方份額數字缺，Kate Spade 也說明平台優勢不能複製。","reasoning":"機制是 200–500 美元價位帶的品牌熱度，加上約 87% 直營帶來的價格控制，以及約 10 億美元行銷量體形成的規模門檻。可比軸用單價與毛利：FY26 手袋 AUR 中十位數、件數低雙位數成長，Q1 AUR 低雙位數、件數低個位數；毛利率由 FY23 的 70.8% 升到最新 TTM 的 78.3%。定價力評擴大，執行力評持平，因為 Kate Spade 在同一平台上續跌 10%，代表優勢長在 Coach 品牌，不在集團平台。同業表不可用，第三方份額也缺，所以方向不上調。當期 ROIC 需要投入資本，事實表未涵蓋，下方只給增量推算。","fact_refs":["f_peer_tpr_gross_margin_pct","f_peer_tpr_operating_margin_pct","f_peer_tpr_fcf_margin_pct"],"verdict_values":{"moat":{"mechanism":"200–500 美元價位帶的品牌熱度，加上直營約 87% 的價格控制與約 10 億美元行銷量體。","execution":8,"pricing":7,"grade":"B","trend":"→","trend_evidence":"定價力擴大：AUR 與件數同時成長，北美促銷減少。執行力持平：Coach 獲客強，但 Kate Spade 續跌 10%，2026-08-13 執行長也承認其知名度未改善。兩者合併為持平，且 CFO 說未來定價是通膨再加一點，目前 AUR 增速不宜外推。","competitor_notes":[{"name":"RMS","strategy_note":"事實表無財務資料，策略也未涵蓋，只能歸在管理層所說價差明顯的歐洲精品一側。"},{"name":"MC","strategy_note":"表內毛利率 34.36% 不像精品集團，疑似代號對錯，不採用；二手報導只稱 LVMH 時尚皮件表現分歧。"},{"name":"CFR","strategy_note":"表內只有 FCF 利潤率、沒有毛利率，疑似代號對錯，不作同業比較。"},{"name":"KER","strategy_note":"事實表無財務資料，無法判讀。"},{"name":"Capri（Michael Kors）","strategy_note":"Coach 在輕奢手袋的主要對手，但事實表無其財務數字；Fortune 報導 Coach 在 18–27 歲偏好已超過 Michael Kors。"}],"peer_na_reason":"同業表不能用於利差判斷：MC 毛利率與 CFR 缺毛利率都不像精品公司，疑似代號對到同名美股，本包無法核實；RMS、KER 無資料，也沒有 ROIC 欄。","threats":[{"level":"🟡","text":"Michael Kors 仍是主要對手，Polene、Jacquemus 靠社群與稀缺性吸引年輕客；來源為彙整文章，沒有一手份額。","p":"30%","evidence_refs":["competitive_share_entrants#2"]},{"level":"🟡","text":"二手精品成長約為一手三倍，Gen Z 手袋二手比例高；數字來自聚合文章，未回溯原始報告，但方向與年輕客群重疊。","p":"25%","evidence_refs":["substitute_technology#1"]},{"level":"🟡","text":"AI 購物助理可能改變數位探索與比價，10-K 已列風險因素；門店 Q1 成長低雙位數，高於數位中個位數，附著點仍在自有門店。","p":"15%","evidence_refs":["substitute_technology#0"]},{"level":"🟡","text":"Bernstein 分析師 2026-11-05 問到歐洲品牌下探單價、縮小價差；Coach 品牌執行長回答價差仍大，但沒有給量化數字。","p":"20%","evidence_refs":[]}],"roic_durability":{"quadrant":"高利益率，周轉率事實表未涵蓋","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"手袋是想要而非需要，延後購買代價低；正面代理是 FY26 新客 1100 萬人，且 2026-08-13 執行長說新客留存率位居客戶檔案最高之列。"},{"item":"決策層級","level":"🟡","text":"替代發生在單一款式的購買決定，轉換成本接近零；提價後件數仍成長是目前最好的反證，但 200 美元以下是刻意縮減。"},{"item":"價值鏈分配","level":"🟢","text":"直營約 87%、沒有單一客戶超過 10%、毛利率 78% 以上，品牌端拿走鏈上大部分利潤，代工端分散在多國。"},{"item":"社會容忍度","level":"🟢","text":"非必需品，沒有社會對漲價的天花板，也不依賴監管授權；關稅屬成本面政策風險，放在風險項處理。"}],"roiic":"下限約 58%：FY27 稅後營業利益增量約 1.74 億美元 ÷ 資本支出與雲端費用約 3 億美元","reinvest_rate":"上限約 18%：3 億美元 ÷ FY27 稅後營業利益約 16.97 億美元，未扣折舊，也未含營運資金","endo_ceiling":10.3,"formula_note":"FY27 營收中點 85.5 億美元 × 營益率約 24.2% × （1−18%）得約 16.97 億；FY26 營益率以財測增幅約 100 個基點回推約 23.2%。58% × 17.7% 約 10.3%。折舊事實表未涵蓋，所以增量報酬是下限、再投資率是上限，兩者相乘等於 FY27 稅後營業利益成長率。"}}}},"q3_growth":{"verdict":"五年後的跑道中等：Coach 到 100 億美元算得出來，但北美只有中個位數，滲透率無數字，第二條成長曲線尚未成形。","reasoning":"FY27 成長拆解：價是手袋 AUR 低雙位數，量是件數低個位數與 Q1 新客 260 萬，回購使全年稀釋股數約 2 億股，較 FY26 約 2.1 億少約 5%，沒有併購。三年共識 EPS 年複合約 12.6%（基期 FY26 約 7.06 美元到 FY29 10.08 美元），分析師家數事實表未涵蓋。內生上界約 10.3%，超出的約 2.3 個百分點主要來自淨回購與 FY27 約 100 個基點的利益率擴張，不靠收購。Coach 要從 69.1 億美元到 100 億，五年需年增約 7.7%，可達，但北美財測只有中個位數，要靠國際。鞋類只貢獻 Q1 成長約 6%，還不算第二曲線。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m"],"verdict_values":{"growth":{"driver_mix":"FY27 價與量都有，AUR 貢獻大於件數；EPS 另靠回購與利益率擴張，沒有併購。","runway_years":null,"runway_post_y5":"🟡","endo_ceiling_basis":"內生上界約 10.3%，來自 FY27 財測推算的增量報酬下限 58% 乘再投資率上限約 18%；共識約 12.6% 高出約 2.3 個百分點，歸因淨回購與利益率擴張。","segments":[{"item":"Coach","value":"FY26 營收 69.1 億美元，年增 24%；Q1 FY27 固定匯率 +16%；FY27 財測高個位數成長，營益率約 36%。"},{"item":"Kate Spade","value":"FY26 營收 10.7 億美元，年減 10%；Q1 FY27 年減 10%；FY27 財測高個位數衰退並小額營業虧損。"}],"decay_signals":[{"signal":"毛利率連兩季年減","lit":false,"note":"Q1 毛利率年增 220 個基點。"},{"signal":"核心市占近 12 個月縮減","lit":false,"note":"沒有縮減證據，但第三方份額數字缺。"},{"signal":"主力產品提價後銷量下滑","lit":false,"note":"Q1 件數低個位數成長；200 美元以下是刻意縮減。"},{"signal":"EPS 成長顯著高於營收成長","lit":true,"note":"FY27 財測 EPS 年增 17–18%，營收固定匯率 6–7%；三年共識也高出約 6 個百分點。"},{"signal":"FCF 對淨利低於 0.75 連兩年","lit":false,"note":"FY26 為 1.19 倍，FY27 財測推算約 1.02 倍。"},{"signal":"SBC 占營收超過 5% 且上升","lit":false,"note":"推算不到營收 2%。"},{"signal":"TAM 萎縮或被替代","lit":false,"note":"二手市場成長快，列為威脅，沒有 TAM 萎縮證據。"},{"signal":"產業估值倍數系統性下移","lit":null,"note":"事實表未涵蓋。"},{"signal":"維護性資本支出占 FCF 超過 60%","lit":false,"note":"總資本支出與雲端費用約 3 億美元，只占 FCF 約 18%。"},{"signal":"停止投資且營收下滑","lit":false,"note":"FY27 資本支出增加，營收成長。"}],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"現金創造強、回購積極，但 FY27 股東回饋高於自由現金流，有一部分靠舉債支應。","reasoning":"FY26 自由現金流 18.1 億美元，是淨利 15.3 億的 1.19 倍；FY27 財測接近 17 億，較 FY26 下滑，以 EPS 財測中點乘 2 億股算淨利約 16.6 億，轉換率約 1.02 倍。FY27 回饋約 20 億美元，含回購 17 億與每股股利 1.85 美元，超出部分靠現金下降與商業本票。總槓桿 1.1 倍，遠低於 2.5 倍目標，目前不構成問題。SBC 在 Q4 占營業利益 7%，若全年比例相近約 1.3 億美元。管理層承諾 Coach 維持強勁且 Kate Spade 恢復成長前不併購。淨負債有兩個口徑：事實表含租賃約 34.7 億美元，管理層只算借款為 18 億美元；本次用本益比估值，不受影響。回購均價與近三年現金去向分項事實表未涵蓋。","fact_refs":["f_kpi3","f_kpi4_sbc","f_net_debt_m","f_shares_diluted_m"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":false,"passed":null,"input":"近 12 個月沒有併購，Capri 案 2024-11 終止；過往收購投入金額與增量報酬事實表未涵蓋，Kate Spade 轉為營業虧損是負面旁證，但算不出報酬率。"},{"name":"buyback_yield","applicable":true,"passed":null,"input":"以財測中點算盈餘殖利率約 6.25%（8.30 ÷ 132.8）；10 年期公債殖利率與回購均價事實表未涵蓋，無法判定。"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"稀釋股數由 FY26 約 2.10 億（淨利 15.28 億 ÷ EPS 7.27）降到 FY27 財測約 2 億，淨稀釋為負；SBC 約 1.3 億美元，約占市值 0.5%。"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購，近 12 個月沒有併購類重大申報；近三年現金去向分項事實表未涵蓋，無法展開。"}}}},"q5_valuation":{"verdict":"現價要求 EPS 五年約 10% 複利、倍數由 16 倍略降到 15 倍，才有約 8% 年報酬；基本面我信，賠率只算中等。","reasoning":"FY27 財測中點 8.30 美元算前瞻本益比 16.0 倍，共識快照 7.96 美元算 16.68 倍，共識仍是上調前數字。PEG 以共識三年年複合約 12.6% 算為 1.32，屬合理帶。Trailing 本益比在四個年度端點的 7% 分位不能當便宜證據，因為 FY25 GAAP EPS 只有 0.82 美元，把歷史端點墊高；P/S 在 75.8% 分位、EV/S 在 77.9% 分位，反映利潤率已在高位。五年分位資料不足，留空。賣方目標價平均 165–174 美元，全距 88–211 美元約 2.4 倍，方向支持進場，但多為 8 月前數字，不作依據。同業現值倍數事實表未涵蓋。短線 RSI 70.47，但 26 週報酬僅 0.15%，股價貼近 52 週均線，過熱只來自財報後跳漲。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_pe_current","f_pe_percentile","f_ps_percentile","f_ev_s_percentile","f_rsi14","f_week26_return_pct","f_dividend_yield_ttm","f_ma_w52"],"verdict_values":{"valuation":{"basis":"前瞻本益比，以 FY27 公司財測中點 8.30 美元為分母，共識快照 7.96 美元為對照。","tier":"輕奢品牌，同業現值倍數事實表未涵蓋","peers":{"expanded":false,"reason":"同業表的 MC、CFR 數字不像精品公司，RMS、KER 無資料，且沒有倍數欄，不能當估值錨。"},"fwd_pe":16.68,"peg":1.32,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"前瞻 16.0 到 16.68 倍、PEG 1.32 落在合理帶，基準年報酬約 8% 屬中段偏低。股價較前份高 12.4%，財測中點高 5.7%，差額由倍數吸收，結論維持中性。","upside_short_pct":11,"upside_mid_pct":19,"denominator_disputed":false,"denominator_note":"共識快照落後財測，兩個分母只差約 4%，不改變結論。FY27 含第 53 週與小額關稅順風，影響不大到足以改變判斷；利益率是否處於高點已放進空頭情境，不靠本益比便宜來論證。"}}},"q6_how_wrong":{"verdict":"最可能看錯的是把一段品牌熱度當成結構性優勢，其次是把回購撐出來的 EPS 當成營運成長。","reasoning":"三個看錯方向的完整推演在反證紀錄。資料面有三處要打折：同業表疑似代號對錯，不能用來證明利差；共識近三個月上修 13.88% 很可能混到財年換算；歷史最大回撤與空方最強數字事實表未涵蓋。2026-08-13 法說管理層沒有正面回答促銷時點影響、逐季毛利率路徑與最擔心的競爭對手；前兩項在 Q1 結果中部分得到驗證，競爭對手仍無答案。","fact_refs":["f_consensus_rev_3m_fy1_pct","f_pe_percentile","f_peer_mc_gross_margin_pct","f_peer_cfr_fcf_margin_pct"],"verdict_values":{"trap":{"verdict":"🟡","label":"品牌熱度退潮與高點利益率"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":8.3,"pe":16.0,"basis":"FY2027 公司財測中點 8.30 美元（2026-11-05 上調），共識快照 7.96 美元為上調前數字；終端倍數同樣以當年度 EPS 為分母。"},"valuation_basis":"eps_pe","eps":{"bull":[8.6,9.9,11.4,13.1,14.9],"base":[8.35,9.2,10.2,11.25,12.3],"bear":[8.0,7.6,7.0,6.6,6.4]},"pe":{"bull":18,"base":15,"bear":11},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":1.39,"net_buyback":0},"second_stage":{"bull_cagr_pct":10,"base_cagr_pct":7},"max_dd":{"lo":-55,"hi":-40,"basis":"下緣：空頭 FY31 EPS 6.4 美元乘低檔 9.5 倍約 61 美元，較現價 −54%，取 −55%；上緣：空頭 FY29 EPS 7.0 美元乘 11 倍約 77 美元，約 −42%，取 −40%。公司歷史最大回撤事實表未涵蓋，250 週均線 65.77 美元約 −50%，落在範圍內。","trigger_time":null},"basis":{"bull":"Coach 達到 100 億美元，集團營收約 120 億，營益率 26.5%，股數約 1.68 億；18 倍是對仍有雙位數成長的溢價，同業現值倍數事實表未涵蓋，只能對照自身現值 16.0 倍。","base":"FY27 取財測上緣；營收每年約增 6.5% 到約 110 億美元，營益率約 25%，股數約 1.75 億；15 倍低於自身現值 16.0 倍。回購效果已在 EPS 路徑內，淨回購殖利率填 0 以免重複計算。","bear":"Coach 熱度退潮，營收回到約 80 億美元，營益率回到 19%，仍高於 FY23 到 FY25 的 17–18%；回購縮手，股數約 1.8 億，機率 30% 因供給可逆性高且共識成長高於內生上界。"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"Coach 成長由 FY26 的 24% 放緩到 Q2 財測高個位數，手袋 AUR 成長由中十位數降到低雙位數；Coach 品牌執行長自己說這行沒有進入門檻；Kate Spade 在同一平台上續跌 10%。","assumption":"Coach 的年輕客群熱度能延續到 FY31，而不是一段流行週期。","consequence":"五年後虧 50% 最可能的故事：北美轉負，促銷回來，毛利率退回 73–75%，營益率回到 19%，EPS 約 6.4 美元，11 倍約 70 美元。","ruling":"採納，空頭機率維持 30%，與唯一致命點重疊，監測同一指標。反面證據是 23 季有 22 季成長，所以不把機率再往上加。","watch":"北美 Coach 固定匯率年增、手袋件數與 AUR、促銷天數。","evidence_refs":["competitive_share_entrants#2","end_markets#1"],"fact_refs":["f_peer_tpr_gross_margin_pct"]},{"view":"論點成功但股東經濟變差","evidence":"FY27 股東回饋 20 億美元高於 FCF 接近 17 億美元，差額靠現金與商業本票；EPS 財測上調 0.45 美元，FCF 財測沒有動；行銷占比持續上升，Q2 SG&A 預計增加約 120 個基點。FTC 勝訴也可能限制同層級併購，未來併購只能往較差的選項走。","assumption":"每股盈餘成長會等比例轉成每股自由現金流。","consequence":"Coach 繼續成長，但 EPS 靠縮股與高點利益率撐住，每股現金沒有同步成長，終端倍數會低於 15 倍。","ruling":"部分採納。總槓桿 1.1 倍還有空間，FY27 的超額回饋不算問題；連兩年超過 1.2 倍才算資本配置轉差。","watch":"股東回饋 ÷ 調整後 FCF、總槓桿、行銷占營收比。","evidence_refs":["regulatory_antitrust#1"],"fact_refs":["f_kpi3","f_net_debt_m"]},{"view":"價格已反映太多","evidence":"現在就賣的最強論證：毛利率由 FY23 的 70.8% 升到 78% 以上，營業利益率由 17.6% 升到 24% 以上，P/S 與 EV/S 都在年度端點約 76–78% 分位；股價一個月漲 12.4%，RSI 70.47；下半年營收只剩中個位數成長。","assumption":"16 倍本益比適用於尚未見頂的利益率。","consequence":"基本面沒破，只要本益比回到 FY28 EPS 的 12–13 倍，股價就在 110–120 美元，跌 10–17%。","ruling":"部分採納。26 週報酬僅 0.15%、股價貼近 52 週均線，稱不上整段過熱；但基準年報酬只有約 8%，容錯空間薄，所以分批而不是一次加足。","watch":"前瞻本益比是否超過 FY28 EPS 的 18 倍、毛利率年變動。","evidence_refs":[],"fact_refs":["f_ps_percentile","f_ev_s_percentile","f_rsi14","f_week26_return_pct"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 🟡 → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=🟡","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 118.12 → 本次 132.8（+12.4%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=118.12","side_b":"本次 price_at_dd=132.8","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 118.12 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 118.12 美元：Bull 價 241.2、Bear 價 74，五年期望值 +35.6%，基準年化 7.9%，不對稱比 2.3","side_b":"本次情境、股價仍用 118.12 美元：Bull 價 268.2、Bear 價 70.4，五年期望值 +44.9%，基準年化 9.3%，不對稱比 2.62","ruling":"先換情境、股價不動：五年期望值多 9.3 個百分點，基準年化多 1.4 個百分點。不對稱比由 2.3 變為 2.62。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變好。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 118.12 美元：五年期望值 +44.9%，基準年化 9.3%，不對稱比 2.62","side_b":"本次情境、股價 132.8 美元：五年期望值 +28.9%，基準年化 6.8%，不對稱比 1.81","ruling":"再換股價、情境不動：起點價上漲 12.4%，五年期望值少 16.0 個百分點，基準年化少 2.5 個百分點，不對稱比由 2.62 降到 1.81。合計五年期望值比前份少 6.7 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"評級與估值結論","cause":"價格變動","prior_field":["signal","val"],"side_a":"前份股價 118.12 美元，評級 B，估值中性。","side_b":"本次股價 132.8 美元，評級 B，估值中性。","ruling":"股價漲 12.4%，財測中點漲 5.7%，差額由本益比從約 15.0 倍升到 16.0 倍吸收，兩項結論都不變。","evidence_level":"事實表與法說","settle_metric":"前瞻本益比","if_then":[],"evidence_refs":["capital_markets_pricing#0"]},{"axis":"情境機率與回撤","cause":"價格變動","prior_field":["p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份多頭 25%、空頭 30%，最大回撤 −55%。","side_b":"本次多頭 25%、基準 45%、空頭 30%，最大回撤 −40% 到 −55%。","ruling":"機率不變。股價較高使同一空頭價位的跌幅擴大，EPS 財測上調則抵銷一部分，回撤改用範圍表達。","evidence_level":"情境推算","settle_metric":"空頭路徑的 EPS 與本益比","if_then":[],"evidence_refs":[]},{"axis":"護城河、跑道與陷阱風險","cause":"新證據","prior_field":["moat_trend","runway_post_y5","trap"],"side_a":"前份：護城河方向持平，五年後跑道中等，價值陷阱風險中等。","side_b":"本次：三項都不變。","ruling":"Q1 的新證據偏正面，Coach 固定匯率 +16%、件數與 AUR 同增，但一季不足以把品牌熱度升格為護城河擴大，滲透率與第三方份額仍缺。","evidence_level":"法說","settle_metric":"第三方份額與滲透率，事實表未涵蓋","if_then":[],"evidence_refs":["supply_demand_durability#1"]},{"axis":"公司類型與循環位置","cause":"新證據","prior_field":["archetype","cycle_position"],"side_a":"前份：品質複利成長，未標循環位置。","side_b":"本次相同。","ruling":"Q1 逐字稿沒有改變公司類型的證據；品牌熱度的週期性放在空頭情境處理，不改標循環股。","evidence_level":"法說","settle_metric":"毛利率與北美成長是否同步轉弱","if_then":[],"evidence_refs":[]},{"axis":"裁決與角色","cause":"新證據","prior_field":[],"side_a":"前份裁決進場，角色衛星。","side_b":"本次基本面輸入沒有轉弱，裁決與角色以本次輸入算出的結果為準。","ruling":"Q1 超越財測且前份加碼條件成立，沒有下修裁決的基本面理由。","evidence_level":"法說","settle_metric":"Q2 FY27 Coach 成長","if_then":[],"evidence_refs":["capital_markets_pricing#0"]},{"axis":"加碼條件更新","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"加碼條件：Q1 FY27 法說（約 2026-11）Coach 固定匯率成長 ≥ +10% 且手袋件數年增 ≥ 0，兩者同時成立","side_b":"加碼條件：Q2 FY27 法說（約 2027-02）Coach 固定匯率成長 ≥ +10% 且北美 Coach ≥ +5%，兩者同時成立","ruling":"前份加碼條件已於 2026-11-05 法說成立：Coach 固定匯率 +16%，手袋件數低個位數成長。舊條件已用掉；新條件加上北美，因為北美是最大獲利來源，且 Q2 財測 Coach 只有高個位數。","evidence_level":"法說原話","settle_metric":"Coach 固定匯率年增與北美年增","if_then":["若 Q2 兩項達標，則加碼剩下一半；","若 Coach 達標但北美低於 +5%，則停止加碼，等 Q3 法說。"],"evidence_refs":["supply_demand_durability#1"]},{"axis":"Single Thing 與清倉、減碼門檻首次建立","cause":"方法變動","prior_field":["single_thing","kill_metrics"],"side_a":"前份摘要此欄為空，無原文可引。","side_b":"Coach 北美固定匯率營收連續兩季年減。","ruling":"前份摘要沒有留存唯一致命點與清倉指標，本次依敏感度重新建立；北美同時影響營收與毛利率，是最大單一敏感項，連兩季年減即清倉，毛利率連兩季年減 100 個基點以上則減碼。","evidence_level":"情境推算","settle_metric":"北美 Coach 固定匯率年增","if_then":[],"evidence_refs":[]},{"axis":"產業態勢三軸","cause":null,"prior_field":null,"side_a":"競爭：Michael Kors 仍是主要對手，Polene、Jacquemus 搶年輕客，二手平台成長快，歐洲品牌可能下探。","side_b":"結構：Coach 在 18–27 歲品牌偏好排名第一，直營約 87%；關稅假設由中 20% 降到低至中 20%。","ruling":"雙向拉鋸。品牌與通路結構在轉好，但競爭證據多為二手彙整，關稅屬政策變數，沒有一軸足以單向定調。","evidence_level":"二手彙整與法說","settle_metric":"第三方手袋份額，事實表未涵蓋","if_then":[],"evidence_refs":["competitive_share_entrants#2","end_markets#3","substitute_technology#1"]},{"axis":"財測上調的品質","cause":null,"prior_field":null,"side_a":"2026-11-05 財務長：全年 EPS 由 7.80–7.90 美元上調到 8.25–8.35 美元。","side_b":"同場拆解：中點上調 0.45 美元，0.27 是 Q1 已實現，0.12 來自線下項目，主要是多回購，只剩約 0.06 美元是後三季營運上修；Q2 財測 3.05 美元僅略高於共識 3.02 美元。","ruling":"可調和。上調是真的，但對後三季的新資訊很少，不能外推成成長加速，基準情境的 FY27 只取財測上緣。","evidence_level":"法說原話","settle_metric":"Q2 FY27 EPS 與營收","if_then":[],"evidence_refs":["capital_markets_pricing#4"]},{"axis":"EPS 上調但現金流財測不動","cause":null,"prior_field":null,"side_a":"2026-08-13 財務長：FY27 調整後 FCF 接近 17 億美元。","side_b":"2026-11-05 財務長：EPS 上調、回購多 3.5 億美元，FCF 仍接近 17 億美元，Q1 僅 5600 萬美元。","ruling":"可調和，但未證。可能是保守或存貨投資，暫不扣分；若全年 FCF 低於 16 億美元且管理層歸因一次性，視為解釋不成立。","evidence_level":"法說原話","settle_metric":"FY27 調整後 FCF","if_then":["若 FY27 FCF 低於 16 億美元，則停止加碼。"],"evidence_refs":[]},{"axis":"毛利率擴張的來源","cause":null,"prior_field":null,"side_a":"2026-11-05 財務長：Q1 毛利率年增 220 個基點，營運 130、關稅 70、匯率 20。","side_b":"2026-08-13 財務長原估全年只增約 30 個基點，關稅假設中 20%；11-05 上調到約 80 個基點，關稅假設降為低至中 20%。","ruling":"約六成來自營運，較持久；三成多是關稅，一成是匯率，屬外部順風。外部順風部分放進空頭情境，空頭營益率回到 19%。","evidence_level":"法說原話","settle_metric":"扣除關稅與匯率後的毛利率年變動","if_then":[],"evidence_refs":["reg_tariff_export#0"]},{"axis":"進入門檻的說法","cause":null,"prior_field":null,"side_a":"2026-08-13 Coach 品牌執行長：這行沒有進入門檻。","side_b":"2026-08-13 財務長：規模門檻正在提高。","ruling":"可調和。門檻不在進入而在放大，護城河給中上評等，不給最高等級；被問最擔心哪個對手時未點名，競爭證據只能靠外部。","evidence_level":"法說原話","settle_metric":"行銷占營收比與新客數","if_then":[],"evidence_refs":["competitive_share_entrants#2"]},{"axis":"Kate Spade 的回升假設","cause":null,"prior_field":null,"side_a":"2026-08-13 執行長：營收進展比計畫慢，整體知名度未改善，全年財測高個位數衰退。","side_b":"2026-11-05 財務長：Q1 年減 10%，Q2 財測低雙位數衰退，全年仍維持高個位數衰退，等於下半年要明顯收斂。","ruling":"未證，監測。品牌已小額虧損，對獲利影響有限；但全年財測隱含下半年回升，若 Q3 仍年減 10% 以上，這項假設視為被推翻。","evidence_level":"法說原話","settle_metric":"Q3 FY27 Kate Spade 年增率","if_then":["若 Q3 年減 10% 以上，則停止加碼。"],"evidence_refs":["end_markets#1"]},{"axis":"共識上修幅度","cause":null,"prior_field":null,"side_a":"事實表：FY1 共識近三個月上修 13.88%，由 6.99 美元到 7.96 美元。","side_b":"RTTNews 記錄 2026-08-13 的 FY27 共識為 7.82 美元；6.99 美元差距太大，不像同一財年，很可能是尚未換年的 FY26 共識，同一財年實際上修約 1.8%。","ruling":"採用同一財年口徑，13.88% 不作為動能依據。換年時點無法在本包核實。財測上調後共識快照仍低於財測下緣，後續應會上修。","evidence_level":"跨來源比對","settle_metric":"下一份共識快照的 FY27 EPS","if_then":[],"evidence_refs":["capital_markets_pricing#1","capital_markets_pricing#0"]},{"axis":"現價是否加碼","cause":null,"prior_field":null,"side_a":"前份加碼條件已成立，基本面超過財測。","side_b":"RSI 70.47，股價一個月漲 12.4%，基準年報酬約 8%。","ruling":"先加計畫量的一半，原因是短線動能過熱；另一半綁 Q2 法說。Q4 件數持平曾被歸因於促銷天數減少，Q1 件數回到成長，這項解釋初步成立，再看一季。","evidence_level":"事實表與法說","settle_metric":"Q2 FY27 Coach 成長、RSI","if_then":["若股價在 Q2 法說前漲過 150 美元而證據未更新，則不追；","若股價跌到 115 美元以下且北美 Coach 仍 ≥ +3%，則分批反買。"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"Q2 FY27 法說驗證 Coach 成長與北美動能，達標才加碼剩下一半。","type":"加碼","maps_to":"H1","metric":"Coach 固定匯率年增、北美 Coach 年增","threshold":"Coach ≥ +10% 且北美 ≥ +5%","action":"加碼","source_freq":"每季法說","date":"2027-02"},{"n":2,"text":"Coach 北美固定匯率營收連續兩季年減。","type":"Single Thing","maps_to":"Single Thing","metric":"北美 Coach 固定匯率年增","threshold":"連 2 季 < 0%","action":"清倉","source_freq":"每季法說","date":null},{"n":3,"text":"毛利率連兩季明顯年減，且管理層歸因關稅或促銷，視為吸收失敗。","type":"減碼","maps_to":"R2","metric":"毛利率年變動","threshold":"連 2 季年減 ≥ 100 個基點","action":"減碼","source_freq":"每季財報","date":null,"evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","geo_supply_chain#0","geo_supply_chain#1","geo_supply_chain#2"]},{"n":4,"text":"Kate Spade 的下半年回升沒有出現。","type":"風險","maps_to":"R3","metric":"Kate Spade 營收年增","threshold":"FY27 全年年減超過 10%，或 FY28 上半年仍年減","action":"停止加碼","source_freq":"每季法說","date":"2027-08","evidence_refs":["end_markets#1"]},{"n":5,"text":"Capri 併購相關的兩宗證券集體訴訟屬民事，不涉及營運收入，求償金額事實表未涵蓋，和解時點未知；公司 2025-07-14 聲請駁回，尚待裁定。","type":"風險","maps_to":"R6","metric":"法院裁定與和解金額","threshold":"集體認證獲准且和解金額超過約 1.7 億美元（一年 FCF 的 10%）","action":"減碼","source_freq":"10-Q 與 10-K 訴訟附註","date":null,"evidence_refs":["major_events#0","lawsuit_class_action#0"]},{"n":6,"text":"股東回饋持續高於自由現金流，靠借債支撐回購。","type":"風險","maps_to":"R5","metric":"股東回饋 ÷ 調整後 FCF、總債務 ÷ 調整後 EBITDA","threshold":"連 2 年 > 1.2 倍，或槓桿 > 2.0 倍","action":"停止加碼","source_freq":"年度財報與法說","date":"2027-08"},{"n":7,"text":"股價回落但基本面無損，分批反買。","type":"估值rearm","maps_to":"H1","metric":"股價","threshold":"≤ 115 美元（約 FY28 EPS 9.2 美元的 12.5 倍）且北美 Coach ≥ +3%","action":"分批反買","source_freq":"每日收盤與每季法說","date":null},{"n":8,"text":"股價上漲而盈餘沒有同步上修，先減三分之一。","type":"減碼","maps_to":"H2","metric":"股價對 FY28 EPS 倍數","threshold":"≥ 18 倍（以 9.2 美元算約 166 美元）","action":"減碼","source_freq":"每日收盤與共識更新","date":null},{"n":9,"text":"Q2 FY27 法說後重看 Coach 基期效應與 Kate Spade 下半年回升假設。","type":"複審日期","maps_to":"H1","metric":"法說揭露","threshold":"Q2 法說公布","action":"停止加碼直到完成複審","source_freq":"一次性","date":"2027-02"}],"kill_metrics":[{"metric":"北美 Coach 固定匯率年增","bear_threshold":"連 2 季 < 0%","window":"2 季","source":"每季法說","last_status":"ok"},{"metric":"毛利率年變動","bear_threshold":"連 2 季年減 ≥ 100 個基點","window":"2 季","source":"每季財報","last_status":"ok"},{"metric":"Coach 手袋件數與 AUR","bear_threshold":"同一季兩者都年減","window":"1 季","source":"每季法說","last_status":"ok"},{"metric":"存貨年增減營收年增","bear_threshold":"連 2 季高於 5 個百分點","window":"2 季","source":"每季財報與法說","last_status":"ok"},{"metric":"股東回饋 ÷ 調整後 FCF","bear_threshold":"連 2 年 > 1.2 倍","window":"2 年","source":"年度財報與法說","last_status":"ok"}],"evidence_dismissed":[],"action_conditions":{"rearm_trigger":"加碼條件：Q2 FY27 法說（約 2027-02）Coach 固定匯率成長 ≥ +10% 且北美 Coach ≥ +5%，兩者同時成立","exec_line":"前份加碼條件已成立，現價先加計畫量的一半，原因是短線動能過熱；另一半等 Q2 法說達標。Q2 前漲過 150 美元不追，跌到 115 美元以下且基本面無損才分批反買。","holding_cap":null}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":true,"cycle_gates_pass":null,"qc49_inherit_prior":false,"wait_for_price":null,"wait_for_price_condition":null},"thesis":{"H":[{"id":"H1","text":"Coach 在 FY26 年增 24% 的高基期上，仍能維持高個位數以上成長，而且單價與件數同時成長。","2y":"FY28 Coach 營收 ≥ 80 億美元","5y":"FY31 Coach 營收 ≥ 100 億美元","10y":null,"threshold":"Coach 固定匯率年增 ≥ +7%，手袋件數年增 ≥ 0","source":"每季法說與新聞稿、10-K 分部營收","drift_rule":"兩年維度：低於門檻 5% 以上連 2 季算削弱，低於 10% 以上連 3 季算反轉；五年維度：連 4 季偏離 5% 算削弱，連 6 季偏離 10% 算反轉。"},{"id":"H2","text":"過去三年的利益率提升大部分是結構性的，來自促銷減少、單價提升與國際組合，不會退回 FY23 到 FY25 的水準。","2y":null,"5y":"FY31 毛利率 ≥ 76%，營業利益率 ≥ 23%","10y":null,"threshold":"毛利率 ≥ 76%，營業利益率 ≥ 23%","source":"10-Q 與 10-K、法說毛利率拆解","drift_rule":"連 4 季偏離 5% 算削弱，連 6 季偏離 10% 算反轉。"},{"id":"H3","text":"自由現金流持續轉成每股價值，回購不需要靠持續舉債，也不被大型併購打斷。","2y":null,"5y":"FY27 到 FY31 累計 FCF ≥ 90 億美元，稀釋股數降到 1.75 億股以下，總槓桿低於 2.5 倍","10y":null,"threshold":"年度 FCF ≥ 16 億美元，總槓桿 ≤ 2.0 倍","source":"現金流量表與每季法說","drift_rule":"連 4 季偏離 5% 算削弱，連 6 季偏離 10% 算反轉。"}],"R":[{"id":"R1","text":"Coach 北美在高基期下降溫，FY27 財測已假設中個位數，一旦低於這個水準，上調的財測就站不住。","h_ref":"H1","clock":"⚡","threshold":"北美 Coach 固定匯率年增 < +3% 連 2 季","evidence_refs":["competitive_share_entrants#2"]},{"id":"R2","text":"毛利率順風反轉：Q1 擴張 220 個基點裡有 70 個來自關稅，手袋生產集中越南、柬埔寨、菲律賓約七成，FY26 關稅成本曾估約 1.6 億美元，國際業務約占 40% 並受美中關係影響。","h_ref":"H2","clock":"🔥","threshold":"毛利率年減 ≥ 100 個基點連 2 季","evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","geo_supply_chain#0","geo_supply_chain#1","geo_supply_chain#2"]},{"id":"R3","text":"Kate Spade 續跌且虧損擴大，消耗管理層與資本；全年財測隱含下半年收斂，尚未驗證。","h_ref":"H1","clock":"🔥","threshold":"FY27 年減超過 10%，或 FY28 上半年仍年減","evidence_refs":["end_markets#1"]},{"id":"R4","text":"重回併購路線：FTC 擋下 Capri 後，同層級整合受限，未來交易可能轉向較不熟悉的領域，傷害資本報酬。","h_ref":"H3","clock":"🐢","threshold":"宣布總價超過市值 5% 的併購，且 Kate Spade 尚未恢復成長","evidence_refs":["regulatory_antitrust#1"]},{"id":"R5","text":"回購長期超過自由現金流，EPS 成長靠舉債支撐。","h_ref":"H3","clock":"🐢","threshold":"股東回饋 ÷ 調整後 FCF 連 2 年 > 1.2 倍，或總槓桿 > 2.0 倍","evidence_refs":[]},{"id":"R6","text":"Capri 併購終止相關的兩宗證券集體訴訟仍未決，金額事實表未涵蓋，不涉及核心業務。","h_ref":null,"clock":"🐢","threshold":"集體認證獲准且和解金額超過約 1.7 億美元","evidence_refs":["major_events#0","lawsuit_class_action#0"]}],"single_thing":{"description":"Coach 北美固定匯率營收連續兩季年減。","why_fatal":"北美是最大獲利來源，這件事同時打到營收與毛利率。以 FY27 營收中點 85.5 億美元、18% 稅率、2 億股算，毛利率每少 1 個百分點，EPS 少約 0.35 美元；由財測約 78.6% 退回 FY24 的 73.3%，約少 1.9 美元，相當於 FY27 EPS 的 22%。","if_happens":"清倉。空頭路徑改為基準情境，五年目標約 70 美元，完成重新判斷前不買回。","how_monitor":"每季法說的北美 Coach 固定匯率年增、促銷天數與手袋件數；Q1 為 +7%，Q2 財測中個位數。","probability":"12–24 個月約 20%，依據是 FY26 的高基期與北美只有中個位數財測；Coach 品牌執行長 2026-11-05 說 23 季有 22 季成長，是反向證據。"}},"appendix_a":{"growth_durability":6,"quality_score":7.5,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":14.94,"peg_fy2":1.19,"stress":{"pass":null,"total":null}},"eps_meta":{"base_eps_path":{"FY2026A":7.06,"FY2027E":7.96,"FY2028E":8.89,"FY2029E":10.08},"fy_end_month":6,"eps_basis":"Non-GAAP，會計年度 6 月底結束。基期由 FY27 財測 8.25–8.35 美元對應年增 17–18% 反推約 7.06 美元；FY2027E 到 FY2029E 為 2026-11-07 共識快照，仍是財測上調前數字。"},"catalysts":[{"date":"2026-12","date_precision":"month","type":"other","event":"假期檔期，Coach 改打限量與配色，促銷更少","impact":"高","watch":"促銷天數與北美直營成長"},{"date":"2027-02","date_precision":"month","type":"guidance","event":"Q2 FY27 法說","impact":"高","watch":"Coach 固定匯率成長、北美年增、毛利率是否年增約 170 個基點"},{"date":"2027-03","date_precision":"month","type":"product","event":"Chelsea 40 上市，定價 525 美元","impact":"低","watch":"500 美元以上的接受度與 AUR"},{"date":"2027-05","date_precision":"month","type":"guidance","event":"Q3 FY27 法說","impact":"中","watch":"下半年中個位數營收假設、Kate Spade 是否收斂"}],"decision_out":{"verdict":"進場","role":"衛星","row_hit":"9","pacing":["row5：動能過熱，進場節奏強制條件式分批（首階小倉＋回檔加碼），頁首掛「⚠️ 動能過熱，勿追高」"],"holding_cap":null,"audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":true,"basis":"momentum_overheated=True"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟡', moat_trend='→', week26=0.15, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position=None, moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":false,"basis":"signal='B', val='🟡'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":true,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"9-verdict","condition":"命中 row9 → 進場","hit":true,"basis":"row_hit=9"},{"row":"QC-49","condition":"qc49_inherit_prior=False，不套用","hit":false,"basis":"qc49_inherit_prior=False"}],"requires_critic":[]}}
```

---

## ⑤ 覆蓋面（程式判定，你回的 ⑤ 燈號會被覆寫）

燈號 🟢：核心軸皆有證據或不適用，非核心軸也沒有空軸。

⑤ 的 reason 只需評論：空軸的查詢詞是否切題、判斷有沒有交代缺口對結論的影響。

---

## 尾段：回覆格式

只回一個 JSON 陣列，①–⑧ 每條一個元素，八個全出，不得跳號、不得多列，陣列外不得有任何文字（不加前言、不加 markdown 圍欄、不加附註）：

```json
[{"item": "①", "light": "🔴|🟡|🟢", "judgment_path": "$.路徑", "reason": "一句話"}]
```
