你是 DD 管線 v20 的判斷層閘（gate），標的 CW（20261108）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（27 條）
- `f_kpi0_gaap`（q1_business）｜營收（GAAP）＝952.59 USD M｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Curtiss-Wright Q3 2026 財報新聞稿（8-K Ex.99.1，2026-11-04）https://www.sec.gov/Archives/edgar/data/0000026324/000162828026070580/ex991_cwxq326xearnings.htm（numbers.latest_quarter_kpis.items[0]，as_of Q3 2026（季末 2026-09-30，公告於 2026-11-04））
- `f_kpi2_non_gaap`（q1_business）｜Non-GAAP（調整後）營業利益率＝19.9 %｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Curtiss-Wright Q3 2026 財報新聞稿（8-K Ex.99.1，2026-11-04）https://www.sec.gov/Archives/edgar/data/0000026324/000162828026070580/ex991_cwxq326xearnings.htm（numbers.latest_quarter_kpis.items[2]，as_of Q3 2026（季末 2026-09-30，公告於 2026-11-04））
- `f_kpi6`（q1_business）｜新訂單＝1100 USD M｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Curtiss-Wright Q3 2026 財報新聞稿（8-K Ex.99.1，2026-11-04）https://www.sec.gov/Archives/edgar/data/0000026324/000162828026070580/ex991_cwxq326xearnings.htm（numbers.latest_quarter_kpis.items[6]，as_of Q3 2026（季末 2026-09-30，公告於 2026-11-04））
- `f_kpi7_backlog`（q1_business）｜Backlog＝4600 USD M｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Curtiss-Wright Q3 2026 財報新聞稿（8-K Ex.99.1，2026-11-04）https://www.sec.gov/Archives/edgar/data/0000026324/000162828026070580/ex991_cwxq326xearnings.htm（numbers.latest_quarter_kpis.items[7]，as_of Q3 2026（季末 2026-09-30，公告於 2026-11-04））
- `f_kpi8_fy2026_11_04`（q1_business）｜FY2026 指引（11-04 上修）＝銷售 3,795–3,840M（+8–10%）；營業利益 731–744M；營業利益率 19.2–19.4%；稀釋 EPS 15.40–15.60；FCF 595–615M guidance｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：Curtiss-Wright Q3 2026 財報新聞稿（8-K Ex.99.1，2026-11-04）https://www.sec.gov/Archives/edgar/data/0000026324/000162828026070580/ex991_cwxq326xearnings.htm（numbers.latest_quarter_kpis.items[8]，as_of Q3 2026（季末 2026-09-30，公告於 2026-11-04））
- `f_peer_cw_gross_margin_pct`（q2_moat）｜CW 毛利率＝38.07 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CW.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝3819.63 USD m｜期間與口徑：2026-11-08／yfinance revenue_estimate 0y 平均（9 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_peer_cw_operating_margin_pct`（q2_moat）｜CW 營業利益率＝19.06 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CW.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_hei_operating_margin_pct`（q2_moat）｜HEI 營業利益率＝24.04 %｜期間與口徑：TTM ending 2026-07-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.HEI.operating_margin_pct，as_of TTM ending 2026-07-31（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_tdg_operating_margin_pct`（q2_moat）｜TDG 營業利益率＝46.47 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.TDG.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_tdy_operating_margin_pct`（q2_moat）｜TDY 營業利益率＝20.0 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.TDY.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_hwm_operating_margin_pct`（q2_moat）｜HWM 營業利益率＝28.01 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.HWM.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝15.35 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-11-07）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝17.24 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-11-07）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝19.5 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-11-07）
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝4138.6 USD m｜期間與口徑：2026-11-08／yfinance revenue_estimate +1y 平均（9 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi5_q3`（q4_capital）｜自由現金流（Q3）＝157.37 USD M｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Curtiss-Wright Q3 2026 財報新聞稿（8-K Ex.99.1，2026-11-04）https://www.sec.gov/Archives/edgar/data/0000026324/000162828026070580/ex991_cwxq326xearnings.htm（numbers.latest_quarter_kpis.items[5]，as_of Q3 2026（季末 2026-09-30，公告於 2026-11-04））
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝863.19 USD m｜期間與口徑：2026-11-08／yfinance 最新一季：總債務 1144.3、現金 281.11（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝36.27 m shares｜期間與口徑：2026-11-08／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝30.19 x｜期間與口徑：2026-11-07／分母＝FY1 EPS 15.35，分子＝快照價 463.47｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-11-07）
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝463.47 USD｜期間與口徑：2026-11-06（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-11-06（RTH 收盤，UTC））
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝30.92 x｜期間與口徑：2026-11-06（RTH 收盤，UTC）／4 個年度端點內的分位＝3.5｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-11-06（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝3.5 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝-36.39 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-11-06（RTH 收盤，UTC））
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝0.39 %｜期間與口徑：2026-08-13 → 2026-11-07／FY1 共識 EPS 15.29 → 15.35（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-11-07）
- `f_ma_w250`（q5_valuation）｜250 週均線＝338.15 USD｜期間與口徑：2026-11-08／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）
- `f_rsi14`（q5_valuation）｜RSI(14)＝40.51｜期間與口徑：2026-11-06（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-11-06（RTH 收盤，UTC））

### findings_digest 中方向為負或來源衝突的條目（8 條）
- `competitive_share_entrants#1`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K 風險因子：對手常有更大規模與資源、可能降價；最大客戶可能自製；國際競爭與跨國對手整併增加。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-12）｜affects：decision_inputs.bear、moat_trend
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：10-K 風險因子：部分產品已被關稅涵蓋，新增或提高關稅可能提高材料成本，漲價未必能完全抵銷而壓低毛利；2025 年約 27% 銷售來自美國以外客戶。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-12）｜affects：decision_inputs.bear、thesis.R
- `reg_tariff_export#3`（reg_tariff_export｜方向 -｜狀態 ok）：美國對中國核能出口許可暫緩，CW 有五件申請待 NRC 審理
  - 來源：Energy Intelligence（as_of 2018-07-26）｜affects：decision_inputs.bear
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：FY2025 10-K 風險因素：供應鏈受供應商產能、制裁與貿易限制、關稅及地緣事件影響，點名俄烏戰爭與中美台關係
  - 來源：Curtiss-Wright FY2025 Form 10-K（as_of 2026-02-12）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：FY2023 10-K：部分零組件有唯一供應商，若延遲或無法供貨可能無法及時生產
  - 來源：Curtiss-Wright FY2023 Form 10-K（as_of 2024-02-14）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#2`（geo_supply_chain｜方向 -｜狀態 ok）：Q2 2026 法說：上半年供應鏈壓力上升，特別是表面處理用稀土材料與化合物
  - 來源：Curtiss-Wright Q2 2026 Earnings Call Transcript (Webull)（as_of 2026-08-06）｜affects：thesis.R、decision_inputs.bear
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：10-K 風險因素指出：公司所處商業與政府市場技術快速變動，需持續投資研發、併購或合作才能維持競爭力；並提到商用核電（含 SMR）發展延遲可能影響業績。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-12）｜affects：moat_trend、thesis.R
- `substitute_technology#1`（substitute_technology｜方向 -｜狀態 ok）：10-K 風險因素：商用核電產業的任何重大中斷（含 SMR 開發延遲）可能影響營運結果或展望。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-12）｜affects：thesis.R、decision_inputs.bear

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 3 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CW_20261108/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":1056.0,"bear_5y_price":289.0,"p_bull_pct":25,"p_bear_pct":30,"upside_5y_pct":38.8,"ev5y_pct":38.1,"irr_base_pct":6.8,"asym_ratio":2.8,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":15.35,"pe":30.19,"basis":"FY2026 共識調整後 EPS 15.35 美元，現價 463.47 美元；終端倍數同為當年度 EPS 口徑。"},"eps":{"bull":[18.0,21.0,24.6,28.6,33.0],"base":[17.1,19.2,21.6,24.1,26.8],"bear":[15.8,16.0,16.2,16.6,17.0]},"pe":{"bull":32,"base":24,"bear":17},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0.216,"net_buyback":0},"second_stage":{"bull_cagr_pct":12,"base_cagr_pct":9},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### CW_Q2_2026_Earnings_Call_20260806.md
- 2026-08-06｜Lynn Bamford (CEO)｜guidance：全年銷售財測上調至 8%–9%（原話："Overall sales are now projected to increase 8% to 9%"）
- 2026-08-06｜Chris Farkas (CFO)｜guidance：全年 EPS 財測上調至 $15.10–$15.40（原話："our full year 2026 diluted EPS guidance to a new range of"）
- 2026-08-06｜Chris Farkas (CFO)｜guidance：全年自由現金流財測上調至 $585–605M（原話："record free cash flow of $585 million to $605 million."）
- 2026-08-06｜Chris Farkas (CFO)｜guidance：第四季營益率預期超過 20%（原話："operating margin in excess of 20% to conclude the year."）
- 2026-08-06｜Chris Farkas (CFO)｜guidance：第三季整體營收小幅成長、營益與利潤率與 Q2 持平（原話："sales to reflect modest growth relative to our second"）
- 2026-08-06｜Chris Farkas (CFO)｜guidance：Defense Electronics 第三季營益與利潤率預期季減（原話："In addition, third quarter operating income and margin are"）
- 2026-08-06｜Chris Farkas (CFO)｜guidance：地面防務全年展望維持不變，依戰術通訊產出時點（原話："the pipeline and growing strength in the 2026 order book"）
- 2026-08-06｜Chris Farkas (CFO)｜guidance：商用核能第三季預期與上季持平（原話："Of note, we anticipate sales in this market to be flat"）
- 2026-08-06｜Chris Farkas (CFO)｜guidance：一般工業全年成長指引 1%–3%，管理層稱仍偏保守（原話："conservative given the order book and the macro environment."）
- 2026-08-06｜Chris Farkas (CFO)｜guidance：DE 第三季營收預期持平至下滑，第四季量大（原話："we will see relatively flat revenues to down in"）
- 2026-08-06｜Lynn Bamford (CEO)｜margin：Q2 營業利益成長快於銷售（原話："Operating income increased 12% year-over-year, exceeding"）
- 2026-08-06｜Chris Farkas (CFO)｜margin：A&I 利潤率擴張來源：吸收、組合（原話："180 basis points, respectively, driven by favorable"）
- 2026-08-06｜Chris Farkas (CFO)｜margin：DE Q2 利潤率 28%，來自組合與成本控制（原話："operating margin of 28%, up 120 basis points"）
- 2026-08-06｜Chris Farkas (CFO)｜margin：A&I 銷量吸收率口徑與有利產品組合（原話："levels, 20% to 25% on the higher sales, but favorable mix"）
- 2026-08-06｜Lynn Bamford (CEO)｜customer：DE 訂單年增近 50%（原話："orders grew nearly 50% year-over-year and are"）
- 2026-08-06｜Lynn Bamford (CEO)｜customer：Naval & Power Q2 訂單年減，歸因潛艦訂單時點（原話："orders were down year-over-year, principally due to the"）
- 2026-08-06｜Lynn Bamford (CEO)｜customer：IFPC 計畫預期獲 FY27 預算增資（原話："on track to receive another sizable increase in funding"）
- 2026-08-06｜Chris Farkas (CFO)｜customer：CFO 稱 Q3 訂單看來也不錯（原話："I think Q3 is shaping up to look pretty good as well."）
- 2026-08-06｜Lynn Bamford (CEO)｜customer：管理層稱 DE 延遲屬時點而非需求消失（原話："I do not believe there's any demand destruction."）
- 2026-08-06｜Chris Farkas (CFO)｜customer：工業車輛 on-highway 預期高個位數成長（原話："highway is going to be up high single digits for the year"）
- 2026-08-06｜Lynn Bamford (CEO)｜customer：潛艦大單對訂單流非劇烈改變（原話："but it isn't a dramatic change in our order flow or how our"）
- 2026-08-06｜Lynn Bamford (CEO)｜risk：供應鏈壓力上半年明顯增加（原話："definitely increased in the first half of this year."）
- 2026-08-06｜Lynn Bamford (CEO)｜risk：2026 營收所需供應大致已確保，重心轉 2027（原話："we're largely secured for our 2026 revenue and the real"）
- 2026-08-06｜Lynn Bamford (CEO)｜risk：對無法替代的材料以調價反映供應鏈壓力（原話："making sure we're adjusting our prices to reflect the"）
- 2026-08-06｜Lynn Bamford (CEO)｜risk：管理層稱獲 Micron 優先配貨（原話："we have been assured that we have priority allocation out"）
- 2026-08-06｜Lynn Bamford (CEO)｜risk：M&A 市場估值偏熱（原話："The market is a bit frothy right now"）
- 2026-08-06｜Lynn Bamford (CEO)｜competition：新創國防科技公司被視為成長機會，不聚焦 Tier 2/3（原話："it's a great growth opportunity for Curtiss-Wright."）
- 2026-08-06｜Lynn Bamford (CEO)｜competition：公司定位為 Tier 2 與 Tier 3 供應商（原話："We are a Tier 2 and the Tier 3 supplier, and that's"）
- 2026-08-06｜Lynn Bamford (CEO)｜product：Golden Dome 相關計畫尚未達量（原話："program that we have not seen reach volume yet,"）
- 2026-08-06｜Lynn Bamford (CEO)｜product：彈藥相關內容占比小（原話："not that we have no content, but it's relatively minor"）
- 2026-08-06｜Lynn Bamford (CEO)｜capital_allocation：M&A 仍是資本運用首要優先（原話："it is still our top priority for our use of CapEx"）
- 2026-08-06｜Lynn Bamford (CEO)｜capital_allocation：Cheswick 設施 $80M 多年期擴建（原話："multiyear investment to expand our Cheswick, Pennsylvania"）
- 2026-08-06｜Lynn Bamford (CEO)｜capital_allocation：MIB 資金累計獲授約 $95M，3 月底為 $70M（原話："Note, this award value was $70 million as of the end"）
- 2026-08-06｜Chris Farkas (CFO)｜capital_allocation：資本支出預計年增近 30%（原話："Please note that this guidance includes a nearly 30%"）
- 2026-08-06｜Lynn Bamford (CEO)｜commitment：預期今年取得 AP1000 訂單（原話："Overall, we continue to expect an AP1000 order this year."）
- 2026-08-06｜Lynn Bamford (CEO)｜commitment：研發投入成長快於銷售的承諾（原話："investing in R&D at a pace faster than sales for the"）
- 2026-08-06｜Lynn Bamford (CEO)｜commitment：預計 2027 Q2 投資人日公布新長期目標（原話："expect to share updated long-term financial targets during"）
- 2026-08-06｜Lynn Bamford (CEO)｜commitment：持續以中段十位數速度複利盈餘（原話："compound our earnings at a mid-teens pace over time."）
- 2026-08-06｜Lynn Bamford (CEO)｜commitment：預期超越 2024 投資人日全部主要財務指標（原話："We can confidently state that we are on track to exceed all"）
- 2026-08-06｜Lynn Bamford (CEO)｜commitment：長期目標細節留待投資人日（原話："And so we will hold the thunder until"）

### 問答異常語氣（迴避／改口／保留）
- CW_Q2_2026_Earnings_Call_20260806.md｜問：Baird 追問 DE 下半年營收有多少已在 backlog、需補多少 book-and-ship｜答法：CFO 明言不提供backlog 占比數字，改談 Q2 創紀錄與第四季量大
- CW_Q2_2026_Earnings_Call_20260806.md｜問：Baird 追問商用航空下半年隱含季減約 8% 的原因｜答法：CFO 未直接解釋商航季減，改談整體 A&I 財測上調、組合與重組效益
- CW_Q2_2026_Earnings_Call_20260806.md｜問：Morgan Stanley 問未來三年是否能支撐雙位數甚至中段十位數營收成長｜答法：CEO 未給數字，改談需求順風與 R&D 投入，並稱留待 2027 Q2 投資人日公布

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 2 | 3 |
| customer_second_source | none | 0 | 2 |
| customer_concentration_credit | found | 2 | 1 |
| supply_demand_durability | found | 3 | 3 |
| regulatory_antitrust | found | 1 | 3 |
| reg_tariff_export | found | 4 | 2 |
| geo_supply_chain | found | 4 | 2 |
| end_markets | found | 2 | 2 |
| substitute_technology | found | 3 | 1 |
| channel_business_model_shift | found | 1 | 1 |
| capital_markets_pricing | found | 5 | 4 |
| major_events | found | 4 | 4 |

未涵蓋／不適用軸的查詢詞原文（供判相關性）：
- **customer_second_source**（none）：Curtiss-Wright largest customer second source OR in-house 2026；Curtiss-Wright 10-K 2025 customer concentration U.S. government largest customer percent of sales

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260529","verdict":"B","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"國防（尤其核海軍）需求結構性成長，訂單動能維持","columns":{"2Y 驗證點":"book-to-bill ≥ 1.1x；naval 段雙位數成長","5Y 驗證點":"Columbia-class 進入全速生產，潛艇含量倍增","10Y 驗證點":"潛艇建造節奏（Virginia 2+/yr、Columbia 1/yr）維持","具體數字門檻":"Naval 段營收 YoY ≥ +8%；book-to-bill ≥ 1.0x","信息來源":"公司法說 Q1'26（B2B 1.3x、backlog $4.3B）","漂移觸發條件":"連 2 季 TTM book-to-bill &lt; 1.0x → 削弱（2Y 假設）"}},{"id":"H2","text":"商業核電 renaissance 兌現：AP1000 RCP 訂單 + SMR 放量","columns":{"2Y 驗證點":"2026 內取得 ≥ 1 筆 AP1000 RCP 訂單；SMR 占商業核電 ≥ 12%","5Y 驗證點":"多座 AP1000 + 首批 SMR 進入交付（~$110M/AP1000）","10Y 驗證點":"SMR 成為商業核電主力，CW 跨設計商獨家位置變現","具體數字門檻":"SMR 占商業核電比重 2025 10% → 2026 12% → 2028 ≥ 20%","信息來源":"公司法說（SMR design→prototype shift）；Ultra Energy 整合","漂移觸發條件":"2026 無 AP1000 訂單 + SMR 占比未升 → 連 4 季偏離削弱（5Y 假設）"}},{"id":"H3","text":"Margin 擴張 + 高 FCF 轉換持續，支撐 EPS 複利","columns":{"2Y 驗證點":"Adj OPM ≥ 18%（FY26 guide 19-19.2%）；FCF 轉換 &gt; 100%","5Y 驗證點":"OPM 朝 20%+ 邁進，營運槓桿 + mix 升級","10Y 驗證點":"ROIC 維持 &gt; 15% 且 &gt; WACC","具體數字門檻":"Adj OPM TTM ≥ 17%；FCF/NI ≥ 1.0","信息來源":"FY26 guide（OPM 19-19.2%、FCF $580-600M &gt;105% 轉換）","漂移觸發條件":"連 2 季 TTM Adj OPM &lt; 17% → 削弱（2Y 假設）"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"國防預算僵局 / CR 延後潛艇撥款，訂單動能放緩","columns":{"對應假設":"H1","時間尺度":"🔥 中期（4-6 季）","監測指標":"book-to-bill、naval 段 YoY、國防授權法案進度","警戒閾值":"連 2 季 B2B &lt; 1.0x"}},{"id":"R2","text":"AP1000 RCP 訂單 2026 落空 / 大幅延後，核電敘事 air-pocket","columns":{"對應假設":"H2","時間尺度":"⚡ 短期（1-2 季可觸發）","監測指標":"Westinghouse AP1000 客戶決策、CW 季度法說對訂單時點措辭","警戒閾值":"2026 全年無 AP1000 RCP 訂單公告"}},{"id":"R3","text":"估值倍數系統性壓縮（成長正常化或 sub-sector de-rating）","columns":{"對應假設":"H3 / 市場","時間尺度":"🐢 長期（2+ 年慢變數）","監測指標":"Fwd PE 5Y 分位、同業（HEI/HWM）倍數趨勢","警戒閾值":"Fwd PE 自高位回落但 EPS 未同步 → 股價 de-rate；需 ≥ 50% 機率才砍倉"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🔴","ma":"✅","trap":"🟢","moat_trend":null,"runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":747.73,"archetype":null,"cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"CW","date":"2026-11-08","schema":"v15.0","contract":"v19","company_name":"Curtiss-Wright Corporation"},"oneliner":"海軍核動力與核能資格撐起穩健生意，訂單與現金都在走強；但跌 38% 後仍有 30 倍本益比，Base 年化約 7%，等 400 美元以下再談。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CW_20261108/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CW_20261108/scenario.json","answers":{"q1_business":{"verdict":"賺美國海軍、國防主承包商、核電業者與飛機原廠的錢，獲利卡在取得資格後很難被換掉的關鍵零組件。","reasoning":"Q3 2026 營收 9.53 億美元，Naval & Power 占 43%（4.12 億，年增 12%），Aerospace & Industrial 占 30%（2.82 億，年增 14%），Defense Electronics 占 27%（2.59 億，年增 2%）。調整後營業利益率 19.9%，TTM 毛利率 38.07%；最新一季毛利率事實表未涵蓋。在手訂單約 46 億美元，是 FY2026 共識營收的 1.2 倍。產業在擴張期：Q3 新訂單年增 15%，book-to-bill 1.1 倍，全年指引上修。單點依賴：10-K 顯示沒有單一客戶超過 10%，但國防收入的最終付款者是美國國防預算，新建核能則繫於 Westinghouse 一家。","fact_refs":["f_kpi0_gaap","f_kpi2_non_gaap","f_kpi6","f_kpi7_backlog","f_kpi8_fy2026_11_04","f_peer_cw_gross_margin_pct","f_rev_consensus_fy1_m"],"verdict_values":{"revenue_quality":"在手訂單覆蓋約 1.2 年營收，海軍與售後收入能見度高；國防電子出貨時點波動大，Q3 有部分營收由 Q4 提前。","unit_econ_note":"管理層揭露的單機含量：AP1000 反應爐冷卻水泵 1.1 億美元以上，另有 5,000–7,000 萬美元增量；Rolls-Royce SMR 超過 1 億美元；APR1400 約 2,000 萬美元。各產品毛利事實表未涵蓋。","archetype":{"primary":"品質複利成長","secondary":null,"confidence":"中","fingerprint":"訂單週期長、FCF 高於淨利、資本需求低；獲利受國防計畫時點影響，ROIC 無法由事實表驗證。"},"industry":{"clock_phase":"II","sd_verdict_source":"結構性持久：潛艦產能每年約 1.2 艘，低於最低目標 2.3 艘，單一來源大型零組件是瓶頸（2026-03 產業報導）；FY2027 海軍造船預算約 660 億美元（2026-11-05 法說，COO）。","bargaining":{"up":"部分零組件只有單一供應商；記憶體與處理器分配吃緊，靠提前採購、DPAS 優先評等與第二來源應對。","down":"公司自稱 Tier 2 與 Tier 3 供應商，面對海軍、主承包商與 Boeing、Airbus，F-35 逐批議價；沒有單一客戶超過 10%。","geo":"2025 年約 27% 銷售來自美國以外；關稅、稀土與中美台關係是供應端變數。"},"profit_pool_dir":null,"tam_table":[{"item":"AP1000 單機含量","value":"反應爐冷卻水泵 1.1 億美元以上，另有 5,000–7,000 萬美元增量（2026-11-05 法說，CEO）"},{"item":"潛在 AP1000 機組","value":"Westinghouse 要求供應鏈準備 91 座，不是訂單；全數兌現約 146–164 億美元，沒有時程，只能當上限"},{"item":"SMR 含量","value":"Rolls-Royce SMR 超過 1 億美元，X-energy 超過 1.2 億美元（管理層口徑）"},{"item":"APR1400 單機含量","value":"約 2,000 萬美元，若韓系機組勝出，單機含量大幅降低"},{"item":"TAM、滲透率、利潤池占比","value":"事實表未涵蓋"}]}}},"q2_moat":{"verdict":"護城河方向穩定：執行面在擴大，定價力穩定，還看不到相對同業拉開。","reasoning":"機制是資格認證加長期嵌入：海軍核動力與核電安全級零組件要通過設計與品質認證，管理層也轉述 Westinghouse 不想更動 AP1000 設計。事實表沒有同業 ROIC 或份額，只能用營業利益率當替代軸：CW TTM 19.06%，低於 TDY、HEI、HWM、TDG，顯示定價力不是同業最強。CW 自身利益率在升，但同業只有單期數字，差距方向無法判斷。當期 ROIC 因投入資本缺資料，不給數值。","fact_refs":["f_peer_cw_operating_margin_pct","f_peer_hei_operating_margin_pct","f_peer_tdg_operating_margin_pct","f_peer_tdy_operating_margin_pct","f_peer_hwm_operating_margin_pct","f_peer_cw_gross_margin_pct","f_kpi2_non_gaap"],"verdict_values":{"moat":{"mechanism":"海軍核動力與核電安全級零組件的資格認證，加上長期計畫嵌入，換供應商要重走設計與認證流程。","execution":8,"pricing":7,"grade":"B","trend":"→","trend_evidence":"營業利益率 FY2022 16.74%、FY2025 18.24%、TTM 19.06%，FY2026 指引 19.2–19.4%，執行面擴大。無法替代的材料可調價轉嫁（2026-08-06 法說，CEO），定價力穩定。同業沒有歷史序列與 ROIC，不能說相對拉開，因此不標擴大。","competitor_notes":[{"name":"HEI","strategy_note":"毛利率只比 CW 高約 2 點，營業利益率卻高約 5 點，差距主要在費用端。"},{"name":"TDG","strategy_note":"毛利率高出 CW 約 21 點，定價結構不是 CW 目前能對照的水準。"},{"name":"TDY","strategy_note":"營業利益率只高不到 1 點，研發密度約為 CW 兩倍，是最接近的利潤率對照。"},{"name":"HWM","strategy_note":"毛利率低於 CW，營業利益率卻高約 9 點，研發密度遠低於 CW，費用結構較輕。"}],"peer_na_reason":"事實表同業資料只有利潤率與研發密度，沒有 ROIC 或份額，無法計算 ROIC 差距。","threats":[{"level":"🟡","text":"最大客戶可能自製，規模更大的對手可能降價。","p":"15%","evidence_refs":["competitive_share_entrants#1"]},{"level":"🟡","text":"韓系 APR1400 若在美國勝出，CW 單機含量約 2,000 萬美元，遠低於 AP1000。","p":"20%","evidence_refs":[]},{"level":"🟡","text":"海外 AP1000 改用中國製泵；管理層以設計不變回應，沒有排除的硬證據。","p":"10%","evidence_refs":[]},{"level":"🟡","text":"技術快速變動，要靠持續研發與併購維持位置；國防電子走開放架構，替換門檻較低。","p":"20%","evidence_refs":["substitute_technology#0"]}],"roic_durability":{"quadrant":"事實表未涵蓋投入資本，無法歸入象限","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者是海軍與核電廠，決策者是海軍計畫單位與反應爐設計商，付款者是國防預算與電力業者，三者都成立。潛艦產能低於目標；在手訂單約 46 億美元，年初以來增加 12%。"},{"item":"決策層級","level":"🟡","text":"替代要在單一反應爐設計或武器平台層級衡量。核能段位置強；國防電子走開放架構，換供應商較容易。重新認證週期與流失率事實表未涵蓋。"},{"item":"價值鏈分配","level":"🟡","text":"公司自稱 Tier 2 與 Tier 3 供應商，TTM 營業利益率低於四家同業，F-35 逐批議價，記憶體漲價要與客戶協商，拿到的價值份額不算最好。"},{"item":"社會容忍度","level":"🟡","text":"國防與核電都靠政府預算與授權。核能目前有跨黨派支持（2026-11-05 法說，COO），但管理層也說期中選舉後的走向難判斷；定價上限與授權法源事實表未涵蓋。"}],"roiic":"事實表未涵蓋投入資本與收購淨額，無法計算","reinvest_rate":"有機代理值約 −16%：FY2023–25 淨利合計 12.44 億美元、FCF 合計 14.40 億美元，以（淨利−FCF）÷淨利計算，不含收購","endo_ceiling":null,"formula_note":"增量報酬乘再投資率在再投資率為負時沒有經濟意義，內生上界改用問三的有機營收成長代理值。"}}}},"q3_growth":{"verdict":"五年後跑道仍寬，靠海軍長週期與核能新建；第二條曲線還差第一筆大單確認。","reasoning":"三年共識 EPS 年複合約 13.7%（FY2025 調整後基期約 13.25 美元，由公司指引 15.40–15.60 等於成長 16–18% 反推；FY2028E 19.50 美元；Koyfin 快照，家數事實表未涵蓋）。成長以量與組合為主，回購加成。下一條曲線有來源：Rolls-Royce SMR 新合約、SMR 開發收入已帶動 Q3 Power & Process 雙位數成長。若 AP1000 到 2027 年中仍無單，這項判斷要降一級。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_kpi7_backlog","f_kpi8_fy2026_11_04"],"verdict_values":{"growth":{"driver_mix":"量與組合為主，價格轉嫁為輔，回購每年加成約 2 點；本期未見併購貢獻。","runway_years":"10 年以上（海軍長週期計畫與核能生命週期），滲透率事實表未涵蓋","runway_post_y5":"🟢","endo_ceiling_basis":"增量報酬公式無法計算：投入資本與收購淨額事實表未涵蓋，且 FY2023–25 FCF 高於淨利，有機再投資率為負。改以 FY2027 共識營收成長 8.35% 當有機成長上界。共識 EPS 年複合 13.7% 超出 5.4 點，約 3 點來自營業利益率每年擴張約 60 基點，約 2.4 點來自淨回購，收購 0 點。","segments":[{"item":"Naval & Power","value":"Q3 營收 4.12 億美元，年增 12%，營業利益年增 25%；FY2026 營收 +11–12%，營益率擴張 70–90 基點"},{"item":"Aerospace & Industrial","value":"Q3 營收 2.82 億美元，年增 14%；FY2026 營收 +10–11%，營益率 18.5–18.7%"},{"item":"Defense Electronics","value":"Q3 營收 2.59 億美元，年增 2%，營益率 27%，訂單年增 27%；FY2026 營收 +4–6%，營益率 27.5–27.7%"}],"decay_signals":[{"signal":"EPS 年複合高於營收年複合超過 5 點","lit":true,"evidence":"FY2022–25 為 19.1% 對 11.0%；FY2025–27 共識約 14.1% 對 8.8%"},{"signal":"FCF／淨利低於 0.75 連 2 年","lit":false,"evidence":"FY2023–25 為 1.14、1.19、1.14"},{"signal":"TAM 萎縮或被替代技術壓縮","lit":false,"evidence":"搜尋未見替代技術，CW 是多家 SMR 的指定供應商"},{"signal":"停止投資新產能且收入下滑","lit":false,"evidence":"Cheswick 8,000 萬美元與 Round Rock 3,000 萬美元擴建進行中"},{"signal":"毛利率連 2 季年減","lit":null,"evidence":"事實表只有年度與 TTM，季度未涵蓋"},{"signal":"核心市占縮減","lit":null,"evidence":"事實表未涵蓋"},{"signal":"提價後銷量下滑","lit":null,"evidence":"事實表未涵蓋"},{"signal":"SBC／營收超過 5% 且上升","lit":null,"evidence":"事實表未涵蓋"},{"signal":"產業估值倍數近 3 年系統性下移","lit":null,"evidence":"同業倍數未涵蓋；CW 自身三個月由約 49 倍降到約 30 倍"},{"signal":"維護性資本支出占 FCF 超過 60%","lit":null,"evidence":"事實表未涵蓋"}],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"現金轉換強，回購在加速，資本配置還要看新任 CEO 的併購紀律。","reasoning":"FCF／淨利 FY2023–25 為 1.14、1.19、1.14，FY2026 指引 FCF 5.95–6.15 億美元、轉換率超過 105%。今年回購約 4.6 億美元，約占 FCF 指引中點 76%，9 月追加授權後可用額度 7 億美元。2026 年資本支出年增近 30%（2026-08-06 法說，CFO），Cheswick 與 Round Rock 合計 1.1 億美元擴建走在 AP1000 訂單之前。營運槓桿為正：FY2025 營收年增 12.08%，營業利益年增約 17.5%。CEO 在 2026-08-06 說併購市場偏熱，COO 在 2026-11-05 仍把併購列為第一優先。SBC／營收、現金去向四分、回購均價、債務到期結構事實表未涵蓋。","fact_refs":["f_kpi5_q3","f_kpi8_fy2026_11_04","f_net_debt_m","f_shares_diluted_m","f_fwd_pe_latest"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":true,"passed":null,"input":"2024 年收購儀控業務與更早的 PacStar 都缺併購後獲利與投入資本，事實表未涵蓋，無法驗證。"},{"name":"buyback_yield","applicable":true,"passed":null,"input":"回購均價與 10 年期殖利率事實表未涵蓋。以現價算前瞻盈餘殖利率 3.31%，10 年期要低於 1.31% 才可能過；今年稍早以更高價買回的部分收益率更低。"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"用淨稀釋代理：稀釋股數由 FY2025 約 37.6 百萬（淨利÷EPS）降到目前 36.27 百萬。SBC 金額事實表未涵蓋，FY2023 EPS 資料有誤不採用。"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長以有機為主，FY2026 上修來自國防與工業訂單；近三年現金去向與回購均價事實表未涵蓋，無法展開。"}}}},"q5_valuation":{"verdict":"現價要賺 10% 年化，五年 EPS 年複合要到約 15%，或本益比要守在 28 倍附近；兩者我都不當 Base，估值偏貴。","reasoning":"現價 463.47 美元要 10% 年化，五年後股價需約 746 美元。用 24 倍退場，FY2031 EPS 要 31.1 美元，年複合 15.2%，高於共識；用 Base EPS 26.8 美元，本益比要 27.9 倍。假設對五年股價的影響：AP1000 落空、倍數由 24 倍降到 20 倍，約 536 美元（−17%）；營業利益率少 100 基點，EPS 約少 1.3 美元、價格 −5%；營收年增少 2 點，價格約 −9%。同業前瞻本益比事實表未涵蓋，終端倍數只能對照 CW 自身的 30.19 倍與 FY2 的 26.88 倍。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_pe_current","f_pe_percentile","f_week26_return_pct","f_consensus_rev_3m_fy1_pct"],"verdict_values":{"valuation":{"basis":"前瞻本益比，FY1 共識 EPS 15.35 美元，同時看 FY2 的 26.88 倍。","tier":null,"peers":{"expanded":false,"reason":"事實表沒有同業前瞻本益比，只有利潤率，無法做倍數對照。"},"fwd_pe":30.19,"peg":2.2,"percentile_5y":null,"val_light":"🟠","val_light_derivation":"前瞻本益比 30.19 倍，PEG 約 2.2，高於 2 屬偏貴；Base 五年年化約 7%，低於 8%。股價較前份已跌 38%，不再是最貴一級，但還沒到合理。五年分位事實表只有四個年度端點，且 FY2023 EPS 資料有誤，不採用。","upside_short_pct":3.3,"upside_mid_pct":21.2,"denominator_disputed":false,"denominator_note":"分母沒有爭議：Q3 調整後與 GAAP 營業利益只差 1.37 百萬美元。但事實表 FY2023 稀釋 EPS 0.79 美元與當年淨利 3.545 億美元對不上，屬資料錯誤，年度端點本益比分位因此不採用。"}}},"q6_how_wrong":{"verdict":"最可能看錯的地方，是把三個月跌 38% 當成單純倍數回落；本包找不到下跌原因。","reasoning":"2026-08-05 股價 748.10 美元，到 2026-11-06 為 463.47 美元，期間共識 EPS 幾乎沒動。歷史最大回撤與空方數字事實表未涵蓋。2026-08-06 法說有三題沒有正面回答：Baird 問國防電子下半年有多少已在在手訂單，CFO 不給占比；商用航空下半年隱含季減約 8% 沒有解釋；Morgan Stanley 問未來三年能否維持雙位數成長，CEO 留到投資人日。訴訟與監管未見重大項目。CEO 與 CFO 同期交接已列入風險。","fact_refs":["f_week26_return_pct","f_price_at_dd","f_consensus_rev_3m_fy1_pct","f_ma_w250","f_rsi14"],"verdict_values":{"trap":{"verdict":"🟡","label":"一項衰退信號亮燈：EPS 增速長期高於營收增速，現金與訂單未轉弱"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":15.35,"pe":30.19,"basis":"FY2026 共識調整後 EPS 15.35 美元，現價 463.47 美元；終端倍數同為當年度 EPS 口徑。"},"valuation_basis":"eps_pe","eps":{"bull":[18.0,21.0,24.6,28.6,33.0],"base":[17.1,19.2,21.6,24.1,26.8],"bear":[15.8,16.0,16.2,16.6,17.0]},"pe":{"bull":32,"base":24,"bear":17},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0.216,"net_buyback":0},"second_stage":{"bull_cagr_pct":12,"base_cagr_pct":9},"max_dd":{"lo":-50,"hi":-30,"basis":"下緣：Bear 倍數 17 倍乘 Bear 首年 EPS 15.8 美元得 269 美元，較現價 −42%，再加情緒過衝約 8 點。上緣：跌到 250 週均線 338 美元為 −27%，再向下穿越約 3 點。佐證：2026-08-05 到 11-06 三個月 −38%，期間 EPS 共識未下修。","trigger_time":null},"basis":{"bull":"AP1000 與 SMR 訂單如期放量，營收年增約 10.5%，營業利益率到 23%，股數年減約 1.9%。","base":"營收年增約 8%，營業利益率到 21.5%，股數年減約 1.5%，AP1000 只算小幅放量。回購已含在每股盈餘內，淨回購殖利率填 0。24 倍沒有同業現值可對照，事實表未涵蓋，只能參考 CW 自身 FY2 的 26.88 倍。","bear":"海軍計畫遞延加上持續決議，AP1000 到 2027 年底仍無單，營收年增約 4%，營業利益率回到約 18%。機率 30%：查不到這次下跌的原因，CEO 與 CFO 同期交接，共識增長也超過有機上界；在手訂單能見度高，所以不再往上加。"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"股價由 2026-08-05 的 748.10 美元跌到 463.47 美元，三個月 −38%，同期 FY1 共識 EPS 只上修 0.39%，Q3 又是超預期加上修。本包沒有資料解釋這次下跌。","assumption":"下跌只是倍數由約 49 倍回到 30 倍，訂單與盈餘沒有受影響。","consequence":"若市場提前反映預算協調款落空、海軍計畫遞延或核能投資降溫，FY2027 指引會低於共識 17.24 美元，EPS 停在 17 美元、本益比 17 倍，股價約 289 美元。","ruling":"部分採納。Q3 訂單與指引不支持基本面已轉壞，但共識快照可能還沒更新，不能當否證，Bear 機率放到 30%。與 Single Thing 部分重疊：AP1000 落空是放大器，海軍與國防電子訂單另設監測。","watch":"2027 年 2 月 FY2027 指引、book-to-bill、12 月 11 日持續決議到期後的預算結果。","evidence_refs":["supply_demand_durability#2"],"fact_refs":["f_week26_return_pct","f_consensus_rev_3m_fy1_pct","f_price_at_dd"]},{"view":"論點成功但股東經濟變差","evidence":"即將接任 CEO 的 COO 在 2026-11-05 重申併購是資本運用第一優先，並預告投資人日談併購做法的變化；CEO 在 2026-08-06 才說併購市場偏熱。研發增速高於銷售，1.1 億美元擴建在 AP1000 訂單到手前動工。","assumption":"成長不會靠降低資本報酬換來。","consequence":"營收達標，但 FCF／淨利跌破 1 或高價併購拉低報酬，EPS 達標時本益比仍會被壓。","ruling":"採納為監測項，暫不扣 Base。過去現金紀律尚可，但新任 CEO 與代理 CFO 沒有自己的資本配置紀錄，併購已實現報酬事實表未涵蓋。","watch":"單筆併購是否超過市值 5%、FCF／淨利、投資人日框架。","evidence_refs":["substitute_technology#0"],"fact_refs":["f_kpi8_fy2026_11_04"]},{"view":"價格已反映太多","evidence":"跌 38% 後前瞻本益比仍有 30.19 倍，PEG 約 2.2，Base 五年年化約 7%。","assumption":"跌深等於便宜。","consequence":"Base 倍數由 30 倍降到 24 倍，每年吃掉約 4.5 點報酬，約占 EPS 複利的四成。","ruling":"採納。跌幅不是安全邊際，到 400 美元以下 Base 才回到約 10%。","watch":"股價相對 FY2027 共識 EPS 的倍數；同業倍數事實表未涵蓋，需補。","evidence_refs":[],"fact_refs":["f_fwd_pe_latest","f_consensus_eps_fy2"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟠","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟠","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 747.73 → 本次 463.47（-38.0%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=747.73","side_b":"本次 price_at_dd=463.47","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 747.73 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 747.73 美元：五年期望值 前份未列，基準年化 前份未列，前份未列不對稱比","side_b":"本次情境、股價仍用 747.73 美元：Bull 價 1,056、Bear 價 289，五年期望值 −14.4%，基準年化 −3.0%，不對稱比 0.56","ruling":"先換情境、股價不動：五年期望值與基準年化前份未列，無法比較。前份未列不對稱比，本次為 0.56。Bull、Bear 價位與股價無關，只受情境影響。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 747.73 美元：五年期望值 −14.4%，基準年化 −3.0%，不對稱比 0.56","side_b":"本次情境、股價 463.47 美元：五年期望值 +38.1%，基準年化 6.8%，不對稱比 2.83","ruling":"再換股價、情境不動：起點價下跌 38.0%，五年期望值多 52.5 個百分點，基準年化多 9.7 個百分點，不對稱比由 0.56 升到 2.83。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"估值與股價變動","cause":"價格變動","prior_field":["signal","val"],"side_a":"前份股價 747.73 美元，估值屬最貴一級，評級 B。","side_b":"本次股價 463.47 美元，前瞻本益比 30.19 倍，估值降為偏貴，評級維持 B。","ruling":"可調和。估值改善全部來自股價，FY1 共識三個月只動 0.39%。前份列的倍數壓縮風險已經發生，但下跌原因本包查不到，所以評級不因跌幅上調。","evidence_level":"一手價格與快照共識","settle_metric":"FY2027 指引 EPS 對共識 17.24 美元","if_then":["若股價跌到 400 美元以下且 FY2027 指引 EPS 不低於 17.2 美元，重跑研究後分批反買，首筆不超過 3%","若股價先彈到 600 美元以上，而 AP1000 訂單與 FY2027 指引都還沒出來，不追","反向條件：若 FY2027 指引 EPS 低於 16.5 美元，取消分批反買，下修 Base 後重算"],"evidence_refs":[]},{"axis":"價值陷阱判斷","cause":"方法變動","prior_field":["trap"],"side_a":"前份判定無陷阱風險。","side_b":"本次逐項檢查十類衰退信號，EPS 增速高於營收增速超過 5 點亮燈，判定為中等。","ruling":"這不是新惡化，FY2022–25 的數字前份就存在。亮燈來源是營益率與回購，現金轉換沒有轉弱，所以停在中等。","evidence_level":"年度財報與共識","settle_metric":"FY2027 EPS 與營收增速差","if_then":["若營收增速掉到 6% 以下而 EPS 仍靠回購維持雙位數，判定升為高風險"],"evidence_refs":[]},{"axis":"前份空值欄位","cause":"方法變動","prior_field":["moat_trend","runway_post_y5","max_dd_pct","p_bull_pct","p_bear_pct","rearm_trigger","archetype","cycle_position"],"side_a":"前份摘要這些欄位都是空值，沒有可比較的舊判斷。","side_b":"本次護城河方向穩定，五年後跑道寬，類型為品質複利成長，機率 25／45／30，回撤範圍 −50% 到 −30%，重新進場價 400 美元；此公司不走循環定位。","ruling":"屬格式補齊，不代表基本面改變。","evidence_level":"本次判斷","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"Single Thing 由空白改為 AP1000 訂單期限","cause":"方法變動","prior_field":null,"side_a":"前份未設定唯一致命點（欄位為空）。","side_b":"2027-12-31 前仍拿不到首筆 AP1000 反應爐冷卻水泵訂單。","ruling":"採用。前份已把 2026 年無單列為短期風險，本次把它定為唯一致命點，期限放寬一年，因為管理層說法與波蘭進度顯示遞延比取消更可能。","evidence_level":"法說與 8-K","settle_metric":"AP1000 泵訂單公告","if_then":["若 2027-12-31 前沒有訂單，減碼一半，未持有者把進場價改為 325 美元"],"evidence_refs":["supply_demand_durability#1"]},{"axis":"減碼、清倉與重新進場門檻新設","cause":"方法變動","prior_field":null,"side_a":"前份沒有減碼與清倉門檻，也沒有重新進場條件。","side_b":"book-to-bill 連 2 季低於 1.0 倍停止加碼，連 3 季減碼；連 3 季低於 1.0 倍且營業利益率低於 17.5% 清倉；股價 ≤400 美元重新評估。","ruling":"採用。門檻依 FY2026 指引與 Base 年化 10% 的價格推出。","evidence_level":"本次判斷","settle_metric":"季報 book-to-bill、營業利益率","if_then":["若兩項門檻同時破線，清倉"],"evidence_refs":[]},{"axis":"假設門檻更新（減碼依據）","cause":"新證據","prior_field":null,"side_a":"Naval 段營收 YoY ≥ +8%；book-to-bill ≥ 1.0x；Adj OPM TTM ≥ 17%；FCF/NI ≥ 1.0。","side_b":"Naval & Power 營收 YoY ≥9%；TTM book-to-bill ≥1.05 倍；TTM 營業利益率 ≥18.5%；FCF／淨利 ≥1.0。警戒線 book-to-bill 連 2 季低於 1.0 倍不變。","ruling":"上調。FY2026 指引營益率 19.2–19.4%、海軍營收 +9–11%，舊門檻已失去警示作用。SMR 占商業核電比重 2028 ≥20% 保留，本次取不到值，標資料缺口。","evidence_level":"8-K 與法說","settle_metric":"季報分部數字","if_then":["若 TTM 營業利益率連 2 季低於 18.5%，H3 判削弱並減碼三分之一"],"evidence_refs":["end_markets#0","end_markets#1"]},{"axis":"AP1000 訂單時點","cause":null,"prior_field":null,"side_a":"2026-08-06 CEO：今年仍預期取得 AP1000 訂單。","side_b":"2026-11-05 CEO：仍預期 2026 年取得，但承認時間愈來愈短，領先專案由 DOE 改口為波蘭；指引沒有計入此單。","ruling":"可調和。承諾未變，時點風險上升，我估 2026 年底前到手約 55%。","evidence_level":"法說逐字稿","settle_metric":"2026-12-31 前的訂單公告","if_then":["若 2026-12-31 前公告訂單，Bull 機率上調 5 點、Bear 下調 5 點，進場價不變","若 2027 年 2 月法說仍無訂單且時點再改，H2 判削弱，不加碼"],"evidence_refs":["supply_demand_durability#1","end_markets#1"]},{"axis":"FY1 共識基準","cause":null,"prior_field":null,"side_a":"Koyfin 11-07 快照 15.35 美元，低於 11-04 新指引下緣 15.40 美元，兩次快照相同，很可能還沒反映 Q3。","side_b":"ChartMill 10-25 為 15.77 美元，高於新指引上緣。賣方目標價 713–774 美元多為 8 月以前，等於 FY1 的 46–50 倍。","ruling":"情境樹起點用 Koyfin，與 FY2、FY3 同源；改用指引中點 15.50 美元，本益比 29.9 倍，結論不變。舊目標價不採用，它們對應的倍數已被市場否定。","evidence_level":"第三方彙整，時間不一致","settle_metric":"FY2026 實際 EPS","if_then":["若 FY2026 實際 EPS 低於 15.40 美元，Base 首年 EPS 下修 2% 後重算進場價"],"evidence_refs":["capital_markets_pricing#1","capital_markets_pricing#3"]},{"axis":"Defense Electronics 第四季爬坡","cause":null,"prior_field":null,"side_a":"2026-08-06 CFO：第三季營收持平到下滑、第四季量大；同場不提供下半年在手訂單占比。","side_b":"2026-11-05 代理 CFO：部分營收由第四季提前到第三季，全年 +4–6% 不變，第四季仍要明顯成長，2022、2023 年有過同樣爬坡。","ruling":"可調和但未驗證。Q2、Q3 訂單支持出貨，提前認列也讓第四季的要求更高。","evidence_level":"法說逐字稿","settle_metric":"FY2026 Defense Electronics 營收成長","if_then":["若全年低於 +4%，FY2027 該分部成長假設下修到中個位數，停止加碼"],"evidence_refs":[]},{"axis":"產業態勢三軸","cause":null,"prior_field":null,"side_a":"競爭：沒有看到惡化的一手數字；10-K 列出客戶自製與降價風險，APR1400 是潛在分流。","side_b":"結構：海軍造船預算增加、潛艦產能缺口、售後與 SMR 合約增加。其他變數：關稅、記憶體與持續決議影響成本與時點。","ruling":"結構性轉好中。依據是海軍營收指引由 2 月的 +5–7% 上修到 +9–11%，以及 Rolls-Royce SMR 新增閥門合約。","evidence_level":"8-K 簡報與法說","settle_metric":"FY2027 海軍營收指引","if_then":["若 FY2027 海軍營收指引低於 +6%，改判雙向拉鋸"],"evidence_refs":["end_markets#1","competitive_share_entrants#1","reg_tariff_export#0"]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"股價三個月跌 38%，FY1 共識未下修，全年指引上修，在手訂單創新高，AP1000 又沒算進指引；Base 倍數若用 28 倍，五年年化約 10%。","side_b":"30.19 倍仍要 24 倍以上退場才有約 7%，同業倍數與下跌原因都查不到，CEO 與 CFO 同期換人。","ruling":"等價格。買進論證的前提是 28 倍守得住，目前沒有證據。","evidence_level":"本次情境推算","settle_metric":"同業前瞻本益比與 FY2027 指引","if_then":["若同業前瞻本益比中位數高於 30 倍且 FY2027 指引不低於共識，Base 倍數上調到 27–28 倍並重算進場價","反向條件：若同業中位數低於 24 倍，Base 倍數下調到 22 倍，進場價同步下修"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"股價跌到 400 美元以下，Base 年化回到約 10%","type":"估值rearm","maps_to":"H3","metric":"股價","threshold":"收盤 ≤400 美元","action":"先重跑研究，通過後分批建立首筆，不超過 3%","source_freq":"每日收盤價","date":null,"evidence_refs":[]},{"n":2,"text":"訂單動能轉弱","type":"風險","maps_to":"R1","metric":"TTM book-to-bill","threshold":"連 2 季低於 1.0 倍","action":"停止加碼；連 3 季則減碼三分之一","source_freq":"每季財報","date":"2027-02","evidence_refs":["supply_demand_durability#2"]},{"n":3,"text":"管理層承諾的 2026 年 AP1000 訂單是否到手","type":"假設驗證","maps_to":"H2","metric":"AP1000 泵訂單公告","threshold":"2026-12-31 前有公告","action":"未到手則不加碼，H2 判削弱","source_freq":"8-K 與 Q4 法說","date":"2026-12-31","evidence_refs":["substitute_technology#1"]},{"n":4,"text":"到 2027 年底仍無 AP1000 泵訂單","type":"Single Thing","maps_to":"H2","metric":"AP1000 泵訂單公告","threshold":"2027-12-31 前沒有訂單","action":"減碼一半；未持有者把進場價改為 325 美元","source_freq":"8-K 與季報","date":"2027-12-31","evidence_refs":["substitute_technology#1"]},{"n":5,"text":"供應鏈與關稅成本轉嫁失敗","type":"風險","maps_to":"R3","metric":"FY2027 分部營業利益率指引","threshold":"Aerospace & Industrial 低於 18.0% 或 Defense Electronics 低於 27.0%","action":"減碼三分之一，下修 Base 營益率路徑","source_freq":"2027 年 2 月法說","date":"2027-02","evidence_refs":["geo_supply_chain#0","geo_supply_chain#1","geo_supply_chain#2","reg_tariff_export#0"]},{"n":6,"text":"新團隊做大型併購","type":"風險","maps_to":"R4","metric":"單筆併購金額","threshold":"超過市值 5%，約 8.4 億美元","action":"停止加碼，條件公布後重跑研究","source_freq":"8-K","date":null,"evidence_refs":[]},{"n":7,"text":"價格續跌但基本面無損","type":"加碼","maps_to":"H1","metric":"股價與 FY2027 指引","threshold":"收盤 ≤350 美元且 FY2027 指引 EPS ≥17.2 美元","action":"分批反買至持股上限","source_freq":"每日收盤價與法說","date":null,"evidence_refs":[]},{"n":8,"text":"訂單與利潤同時破線","type":"清倉","maps_to":"H1","metric":"TTM book-to-bill 與 TTM 營業利益率","threshold":"book-to-bill 連 3 季低於 1.0 倍且營業利益率低於 17.5%","action":"清倉","source_freq":"每季財報","date":null,"evidence_refs":[]},{"n":9,"text":"新任 CEO 在投資人日公布長期目標","type":"複審日期","maps_to":"H3","metric":"新三年財務框架","threshold":"EPS 年複合目標不低於中段十位數","action":"低於則下修 Base EPS 後重算","source_freq":"投資人日","date":"2027-05","evidence_refs":[]}],"kill_metrics":[{"metric":"TTM book-to-bill","bear_threshold":"連 2 季低於 1.0 倍","window":"2 季","source":"公司季報與法說","last_status":"ok"},{"metric":"FY2027 營業利益率指引中點","bear_threshold":"低於 19.0%","window":"2027 年 2 月法說","source":"8-K 與法說","last_status":"ok"},{"metric":"FCF／淨利","bear_threshold":"連 2 年低於 1.0","window":"2 個會計年度","source":"年度財報","last_status":"ok"},{"metric":"AP1000 反應爐冷卻水泵訂單","bear_threshold":"2027-12-31 前仍無訂單","window":"至 2027-12-31","source":"8-K 與法說","last_status":"warning"}],"evidence_dismissed":[{"ref":"reg_tariff_export#3","reason":"這是 2018-07-26 的報導，描述當年五件待審出口許可，本包沒有這些申請的後續結果，不能代表 2026 年的出口狀態。"}],"action_conditions":{"rearm_trigger":"股價 ≤400 美元（FY2027 共識 EPS 約 23 倍，Base 年化回到約 10%）；觸發後先重跑研究。","exec_line":"463 美元附近不追。≤400 美元且 FY2027 指引 EPS 不低於 17.2 美元，重跑研究後分批買進；2027 年 2 月指引公布前不加碼。","holding_cap":"首筆不超過 3%；AP1000 訂單到手且常任 CFO 到位前不超過 6%。"}},"decision_inputs":{"signal":"B","ma":"🟠","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等股價 ≤400 美元，且 2027 年 2 月 FY2027 指引 EPS 不低於 17.2 美元。","qc48_result":"pass","qc48_note":"Bull 情境的量乘價骨架只做了一半，33 美元的 EPS 沒有推回機組數與分部營收，歷史類比也沒有做，所以還不到成立的程度；但各項也沒有找到反證，目前是證據不足而非被推翻。"},"thesis":{"H":[{"id":"H1","text":"海軍核動力與國防電子的訂單，足以撐住營收連續兩年成長 8% 以上。","2y":"到 FY2028：TTM book-to-bill 維持 1.05 倍以上，Naval & Power 營收年增至少 9%。","5y":"到 FY2031：潛艦與航母訂單把在手訂單推到 70 億美元以上。","10y":"潛艦節奏維持 Virginia 每年 2 艘以上、Columbia 每年 1 艘。","threshold":"TTM book-to-bill ≥1.05 倍；Naval & Power 營收 YoY ≥9%；在手訂單 YoY ≥8%。","source":"公司季報與法說（Q3 2026：book-to-bill 1.1 倍、在手訂單約 46 億美元、海軍營收指引 +9–11%）。","drift_rule":"2 年假設：連 2 季偏離門檻 5% 以上為削弱，連 3 季偏離 10% 以上為反轉。"},{"id":"H2","text":"商用核能從售後維修走到新建機組，第一筆 AP1000 泵訂單打開第二條成長曲線。","2y":"2027-12-31 前至少拿到一筆 AP1000 反應爐冷卻水泵訂單，Power & Process 營收年增 ≥10%。","5y":"到 FY2031：多座 AP1000 與首批 300MW 級 SMR 進入交付，單機含量兌現。","10y":"2036 年前累計至少 10 座機組訂單，新建機組成為與售後同等的收入來源。","threshold":"2027-12-31 前首筆 AP1000 泵訂單；FY2027 Power & Process 營收成長 ≥10%；SMR 占商業核電比重 2028 ≥20%（本次資料缺口）。","source":"2026-11-05 法說（AP1000 仍預期 2026 年取得、Rolls-Royce SMR 超過 1 億美元）；8-K 簡報（AP1000 未計入指引）。","drift_rule":"5 年假設：連 4 季偏離 5% 以上為削弱，連 6 季偏離 10% 以上為反轉；訂單期限已過仍未到手，直接判削弱。"},{"id":"H3","text":"營業利益率與現金轉換續升，加上回購，支撐 EPS 年複合約 12%。","2y":"FY2028 營業利益率 ≥20%，FCF／淨利 ≥1.0。","5y":"FY2031 EPS 約 26.8 美元，營業利益率 21% 以上。","10y":"ROIC 維持 15% 以上且高於資金成本（本次資料缺口）。","threshold":"TTM 營業利益率 ≥18.5%；FCF／淨利 ≥1.0；股數年減 ≥1.5%。","source":"2026-11-04 8-K 與 2026-11-05 法說（FY2026 營益率 19.2–19.4%、FCF 轉換超過 105%、回購約 4.6 億美元）。","drift_rule":"2 年假設：連 2 季偏離門檻 5% 以上為削弱，連 3 季偏離 10% 以上為反轉。"}],"R":[{"id":"R1","text":"持續決議與預算協調款不確定，潛艦或國防電子訂單延後。","h_ref":"H1","clock":"🔥","threshold":"TTM book-to-bill 連 2 季低於 1.0 倍。","evidence_refs":["supply_demand_durability#2"]},{"id":"R2","text":"AP1000 泵訂單滑出 2026 年，SMR 進度也遞延。","h_ref":"H2","clock":"⚡","threshold":"2026-12-31 前沒有訂單公告判削弱；2027-12-31 前仍沒有，依唯一致命點處理。","evidence_refs":["substitute_technology#1"]},{"id":"R3","text":"記憶體、稀土、單一來源零件與關稅墊高成本，轉嫁不完。","h_ref":"H3","clock":"🔥","threshold":"FY2027 營益率指引 Aerospace & Industrial 低於 18.0% 或 Defense Electronics 低於 27.0%。","evidence_refs":["geo_supply_chain#0","geo_supply_chain#1","geo_supply_chain#2","reg_tariff_export#0"]},{"id":"R4","text":"CEO 與 CFO 同期交接，新團隊放大併購或放寬資本紀律。","h_ref":"H3","clock":"🔥","threshold":"單筆併購超過市值 5%（約 8.4 億美元），或常任 CFO 到 2027 年 6 月仍未到位。","evidence_refs":[]},{"id":"R5","text":"成長正常化或族群重新定價，本益比再壓縮。","h_ref":"H3","clock":"🐢","threshold":"FY2 本益比低於 20 倍而共識未下修時不砍倉；共識同時下修 5% 以上才算基本面確認。","evidence_refs":[]}],"single_thing":{"description":"2027-12-31 前仍拿不到首筆 AP1000 反應爐冷卻水泵訂單。","why_fatal":"訂單本身對盈餘貢獻有限，份量在終端倍數。沒有這筆單，新建核能只是 91 座潛在機組的說法，Base 終端本益比要由 24 倍降到約 20 倍，五年股價由約 643 美元降到約 536 美元（−17%），大於營業利益率少 100 基點的影響（約 −5%）。","if_happens":"H2 判反轉，新建核能移出 Base 後重算；持有者減碼一半，未持有者把進場價由 400 美元改為 325 美元。","how_monitor":"公司 8-K 與季報、Westinghouse 與波蘭專案進度、美國能源部計畫；下次檢查是 2027 年 2 月 Q4 法說。","probability":"20%（12–24 個月）"}},"appendix_a":{"growth_durability":6,"quality_score":9,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":26.88,"peg_fy2":1.96,"stress":{"pass":null,"total":null}},"eps_meta":{"base_eps_path":{"FY2025A":12.87,"FY2026E":15.35,"FY2027E":17.24,"FY2028E":19.5},"fy_end_month":12,"eps_basis":"FY2026E 起為 Koyfin 共識調整後 EPS。FY2025A 12.87 美元是事實表的 GAAP 稀釋 EPS；由公司指引反推的調整後基期約 13.25 美元，三年年複合以調整後口徑計為 13.7%，以 GAAP 基期計為 14.9%。"},"catalysts":[{"date":"2026-12-11","date_precision":null,"type":"macro","event":"持續決議到期，FY2027 國防預算走向","impact":"中","watch":"海軍造船與協調款是否落空"},{"date":"2026-12-31","date_precision":null,"type":"other","event":"管理層承諾的 AP1000 泵訂單期限","impact":"高","watch":"8-K 或 Westinghouse 公告"},{"date":"2027-01-01","date_precision":null,"type":"other","event":"Kevin Rayment 接任 CEO","impact":"中","watch":"常任 CFO 人選與併購表態"},{"date":"2027-02","date_precision":"month","type":"guidance","event":"Q4 財報與 FY2027 指引","impact":"高","watch":"EPS 指引對共識 17.24 美元、分部營益率"},{"date":"2027-05","date_precision":"month","type":"guidance","event":"投資人日公布新長期目標","impact":"高","watch":"營收與 EPS 年複合目標、併購框架"}],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8w(原8a)","pacing":[],"holding_cap":null,"audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟠'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":true,"basis":"signal='B', runway='🟢', val='🟠', moat_trend='→', week26=-36.39, valuation_dependent=False"},{"row":"8a-QC48","condition":"row 8a 命中須經 QC-48 爆發候選 Bull 冷讀；critic 未放行（fail／not_run）→ 落 row 8","hit":false,"basis":"qc48_result='pass', 結論='Bull 情境的量乘價骨架只做了一半，33 美元的 EPS 沒有推回機組數與分部營收，歷史類比也沒有做，所以還不到成立的程度；但各項也沒有找到反證，目前是證據不足而非被推翻。'"},{"row":"8w","condition":"判斷者宣告 wait_for_price（價格合理但要等）→ 原 row8a 進場改觀望（等價格）","hit":true,"basis":"wait_for_price=True, 等待條件='等股價 ≤400 美元，且 2027 年 2 月 FY2027 指引 EPS 不低於 17.2 美元。'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"requires_critic":[]}}
```

---

## ⑤ 覆蓋面（程式判定，你回的 ⑤ 燈號會被覆寫）

燈號 🟡：非核心軸無證據：customer_second_source（客戶 second-source 與 in-house）（尾部風險或事件型，不擋）。

⑤ 的 reason 只需評論：空軸的查詢詞是否切題、判斷有沒有交代缺口對結論的影響。

---

## 尾段：回覆格式

只回一個 JSON 陣列，①–⑧ 每條一個元素，八個全出，不得跳號、不得多列，陣列外不得有任何文字（不加前言、不加 markdown 圍欄、不加附註）：

```json
[{"item": "①", "light": "🔴|🟡|🟢", "judgment_path": "$.路徑", "reason": "一句話"}]
```
