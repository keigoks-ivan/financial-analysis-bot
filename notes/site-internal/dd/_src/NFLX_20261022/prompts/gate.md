你是 DD 管線 v20 的判斷層閘（gate），標的 NFLX（20261022）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（35 條）
- `f_kpi0_gaap`（q1_business）｜營收（GAAP）＝12874.2 USD million｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-20）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Netflix Q3'26 股東信／8-K Ex.99.1（Netflix IR 發布）（numbers.latest_quarter_kpis.items[0]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-20））
  - 註記：未取得共識數；公司自家預測：營收略高於預測
- `f_kpi1_gaap`（q1_business）｜GAAP 營業利益＝4458.6 USD million｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-20）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Netflix Q3'26 股東信／8-K Ex.99.1（numbers.latest_quarter_kpis.items[1]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-20））
  - 註記：公司稱優於自家預測，主因費用認列時點（timing of expenses），非結構性
- `f_kpi2_gaap`（q1_business）｜GAAP 營業利益率＝34.6 %｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-20）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Netflix Q3'26 股東信／8-K Ex.99.1（numbers.latest_quarter_kpis.items[2]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-20））
  - 註記：優於公司自家預測（費用時點）
- `f_kpi5_q4_2026`（q1_business）｜管理層指引：Q4 2026＝13442 USD million（營收，約 +12% YoY）｜期間與口徑：Q3 2026 公告（2026-10-20）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：Netflix Q3'26 股東信／8-K Ex.99.1（numbers.latest_quarter_kpis.items[5]，as_of Q3 2026 公告（2026-10-20））
  - 註記：未取得
- `f_kpi6_2026`（q1_business）｜管理層指引：全年 2026＝51100 USD million（營收點估計，+13% YoY）｜期間與口徑：Q3 2026 公告（2026-10-20）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：Netflix Q3'26 股東信／8-K Ex.99.1（numbers.latest_quarter_kpis.items[6]，as_of Q3 2026 公告（2026-10-20））
  - 註記：營收指引較前次區間中點低 0.2%
- `f_peer_nflx_gross_margin_pct`（q2_moat）｜NFLX 毛利率＝49.12 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.NFLX.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_earnings_recency`（q1_business）｜最近一次財報日＝2026-10-20 date｜期間與口徑：2026-10-20／距今 2 個交易日｜kind：realized
  - 來源：—（numbers.earnings_recency，as_of 2026-10-20）
- `f_peer_nflx_operating_margin_pct`（q2_moat）｜NFLX 營業利益率＝29.68 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.NFLX.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_nflx_fcf_margin_pct`（q2_moat）｜NFLX FCF 利潤率＝23.06 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.NFLX.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_meta_operating_margin_pct`（q2_moat）｜META 營業利益率＝38.08 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.META.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_googl_operating_margin_pct`（q2_moat）｜GOOGL 營業利益率＝33.11 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.GOOGL.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_pins_operating_margin_pct`（q2_moat）｜PINS 營業利益率＝6.27 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.PINS.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_roku_operating_margin_pct`（q2_moat）｜ROKU 營業利益率＝5.25 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ROKU.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝3.59 USD/share｜期間與口徑：2026-10-21／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261021.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-10-21）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝3.8 USD/share｜期間與口徑：2026-10-21／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261021.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-10-21）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝4.56 USD/share｜期間與口徑：2026-10-21／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261021.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-10-21）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝51123.53 USD m｜期間與口徑：2026-10-22／yfinance revenue_estimate 0y 平均（40 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-10-22）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝56665.35 USD m｜期間與口徑：2026-10-22／yfinance revenue_estimate +1y 平均（45 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-10-22）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi3_fcf`（q4_capital）｜自由現金流（FCF）＝2883.5 USD million｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-20）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Netflix Q3'26 股東信／8-K Ex.99.1（numbers.latest_quarter_kpis.items[3]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-20））
  - 註記：未取得
- `f_kpi4_sbc`（q4_capital）｜SBC 占營業利益＝3.0 %｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-20）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：自算：SBC 133.7M ÷ GAAP 營業利益 4,458.6M（SBC 取自同份股東信）（numbers.latest_quarter_kpis.items[4]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-20））
  - 註記：n/a
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝6909.44 USD m｜期間與口徑：2026-10-22／yfinance 最新一季：總債務 15132.39、現金 8222.95（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-10-22）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝4163.94 m shares｜期間與口徑：2026-10-22／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-10-22）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝65.04 USD｜期間與口徑：2026-10-21（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-10-21（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝18.12 x｜期間與口徑：2026-10-21／分母＝FY1 EPS 3.59，分子＝快照價 65.04｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-10-21）
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝18.8 x｜期間與口徑：2026-10-21（RTH 收盤，UTC）／4 個年度端點內的分位＝0.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-10-21（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝0.0 %｜期間與口徑：2026-10-21（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-10-21（RTH 收盤，UTC））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝5.45 x｜期間與口徑：2026-10-21（RTH 收盤，UTC）／4 個年度端點內的分位＝17.4｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-10-21（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝17.4 %｜期間與口徑：2026-10-21（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-10-21（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝5.58 x｜期間與口徑：2026-10-21（RTH 收盤，UTC）／4 個年度端點內的分位＝14.7｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-10-21（RTH 收盤，UTC））
- `f_ev_s_fwd`（q5_valuation）｜EV/S（EV ÷ FY1 共識營收）＝5.43 x｜期間與口徑：2026-10-22／f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）｜kind：estimate
  - 來源：—（numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m，as_of 2026-10-22）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝0.56 %｜期間與口徑：2026-07-16 → 2026-10-21／FY1 共識 EPS 3.57 → 3.59（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261021.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-10-21）
- `f_consensus_rev_fy2_pct`（q5_valuation）｜FY2 共識修正＝0.0 %｜期間與口徑：2026-10-21／兩份 Koyfin 快照之間的 EPS 修正幅度（3.8 → 3.8）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261021.xlsx（numbers.consensus_revision.fy2.revision_pct，as_of 2026-10-21）
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝-30.24 %｜期間與口徑：2026-10-21（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-10-21（RTH 收盤，UTC））
- `f_rsi14`（q5_valuation）｜RSI(14)＝32.61｜期間與口徑：2026-10-21（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-10-21（RTH 收盤，UTC））
- `f_consensus_rev_fy1_pct`（q5_valuation）｜FY1 共識修正＝0.28 %｜期間與口徑：2026-10-21／兩份 Koyfin 快照之間的 EPS 修正幅度（3.58 → 3.59）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261021.xlsx（numbers.consensus_revision.fy1.revision_pct，as_of 2026-10-21）

### findings_digest 中方向為負或來源衝突的條目（10 條）
- `competitive_share_entrants#0`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K 列出競爭對手涵蓋線性電視、串流（含盜版）、遊戲、開放內容平台與社群媒體，並指新進入者可能以獨特服務進場。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-01-23）｜affects：moat_trend、thesis.R
- `competitive_share_entrants#1`（competitive_share_entrants｜方向 -｜狀態 ok）：Nielsen Gauge（2026年8月報導）：Netflix 占美國電視觀看 7.9%，去年同期 8.3%；YouTube 13.5%（12.8%）、Prime Video 4.2%（3.6%）、Peacock 2.3%（1.5%）。
  - 來源：MediaPost, Streaming Climbs To 48.5%, Per Last Lame Duck Edition Of Nielsen's 'Gauge'（as_of 2026-08-01）｜affects：moat_trend、thesis.R
- `regulatory_antitrust#1`（regulatory_antitrust｜方向 -｜狀態 ok）：DOJ 就 Netflix 收購 Warner Bros. 案發出民事調查要求，檢視 Clayton Act 第 7 條與 Sherman Act 第 2 條，並詢問 Netflix 對獨立製片與創作者的議價力。
  - 來源：Bloomberg Law｜DOJ Probes Netflix's Power Over Filmmakers in Warner Deal Review（as_of 2026-02-21）｜affects：thesis.R、decision_inputs.bear、triggers
- `regulatory_antitrust#2`（regulatory_antitrust｜方向 -｜狀態 ok）：倡議團體 Demand Progress 於 2026-07-07 發起「Netflix is a Monopoly」運動，要求 DOJ、FTC 調查（倡議，非官方行動）。
  - 來源：MLex｜'Netflix is a Monopoly' campaign seeks US DOJ, FTC investigation（as_of 2026-07-07）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：川普於2025-09-29宣布對境外製作電影課100%關稅；法律依據不明，白宮稱尚未做最終決定；Netflix股價當日收跌1.9%。
  - 來源：Reuters 經 Citizen Digital 轉載：Trump says US to impose 100% tariff on movies made outside the country（as_of 2025-09-29）｜affects：decision_inputs.bear、thesis.R
- `reg_tariff_export#2`（reg_tariff_export｜方向 -｜狀態 ok）：Citigroup 估計最壞情境下電影關稅可使 Netflix EPS 約降20%
  - 來源：Forbes Australia: Netflix stock dips as Trump wields 100% movie tariffs（as_of 2025-05-05）｜affects：decision_inputs.bear、valuation
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：Netflix 10-K 風險因素：娛樂影音有訂閱、廣告、盜版等多種模式可能搶走市場，且含生成式 AI 在內的新技術快速演進
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-01-23）｜affects：moat_trend、decision_inputs.bear
- `capital_markets_pricing#0`（capital_markets_pricing｜方向 -｜狀態 ok）：Netflix 2026-07-16 Q3 指引（營收 $12.86B、EPS $0.82）低於市場共識（約 $13.0B／$0.84）；財報後股價開盤跌近 12%
  - 來源：Capital.com Netflix stock forecast／Benzinga NFLX earnings（搜尋摘要）（as_of 2026-07-16）｜affects：valuation、decision_inputs.bear
- `capital_markets_pricing#1`（capital_markets_pricing｜方向 -｜狀態 ok）：FY2026 營業利益率指引 31.5%，比共識 32.7% 低 120bps（S&P Global 引述）；Q2 2026 營收 $12.56B 略低於共識 $12.58B，EPS $0.80 優於 $0.79
  - 來源：S&P Global Market Intelligence, Netflix post-Q2 research（as_of 2026-07-22）｜affects：valuation、thesis.R
- `capital_markets_pricing#4`（capital_markets_pricing｜方向 -｜狀態 ok）：年初 Visible Alpha：2026 營收預估微升，營業利益預估下修近 3%、EPS 預估下修 3.7%（內容與廣告成本上升）
  - 來源：S&P Global, Netflix post-earnings review Q4 2025 and outlook（as_of 2026-01-25）｜affects：valuation、thesis.R

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 3 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/NFLX_20261022/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":179.4,"bear_5y_price":48.8,"p_bull_pct":22,"p_bear_pct":30,"upside_5y_pct":69.9,"ev5y_pct":64.7,"irr_base_pct":11.2,"asym_ratio":5.1,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":3.59,"pe":18.12,"basis":"FY1（FY2026E）共識 EPS 3.59，和終端倍數同為前瞻本益比口徑；可能含一次性終止費"},"eps":{"bull":[3.95,4.85,5.75,6.75,7.8],"base":[3.8,4.56,5.2,5.85,6.5],"bear":[3.45,3.4,3.5,3.62,3.75]},"pe":{"bull":23,"base":17,"bear":13},"p":{"bull":22,"base":48,"bear":30},"yield_pct":{"dividend":0,"net_buyback":0},"second_stage":{"bull_cagr_pct":12,"base_cagr_pct":8},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### NFLX_Q2_2026_Earnings_Call_20260716.md
- 2026-07-16｜Spencer Neumann｜guidance：CFO 重申 2026 全年營收成長指引為 13% 至 14%。（原話："13% to 14% top line growth for the full year"）
- 2026-07-16｜Spencer Neumann｜guidance：CFO 說明第三季指引為報價幣別成長 12%、匯率中性 11%。（原話："12% revenue growth in Q3 reported, 11% FX neutral"）
- 2026-07-16｜Spencer Neumann｜margin：CFO 以去年下半年權重較高解釋季間成長的波動，並稱公司以全年而非單季管理。（原話："a little bit of quarter-to-quarter choppiness in growth"）
- 2026-07-16｜Theodore Sarandos｜guidance：Ted 給出 2026 年內容費用預期成長約 10%。（原話："we're forecasting content expense up about 10% this year"）
- 2026-07-16｜Spencer Neumann｜customer：管理層稱全球可觸及家戶約 8 億戶。（原話："roughly 800 million addressable households"）
- 2026-07-16｜Gregory Peters｜margin：Greg 說明觀看時數與營收、利潤並非線性關係（數字口徑說明）。（原話："not a linear relationship between view hours and revenue"）
- 2026-07-16｜Gregory Peters｜product：Greg 給出直播佔內容預算與觀看時數的比重差異（預算 5%、時數 1%）。（原話："live, we expect will be 5% of our content budget this year"）
- 2026-07-16｜Gregory Peters｜customer：Greg 稱上半年觀看時數成長 2%，相較 2025 年的 1.5% 略為加快。（原話："slight acceleration compared to 1.5% growth in 2025"）
- 2026-07-16｜Gregory Peters｜margin：Greg 表示不揭露參與品質指標的細節，視為競爭優勢。（原話："We're not going to go into the details of that quality metrics"）
- 2026-07-16｜Theodore Sarandos｜product：Ted 稱第二季觀看整體無顯著變化，且今年第二季流失幅度略有改善。（原話："Our Season 2 falloff is actually slightly improved this year"）
- 2026-07-16｜Theodore Sarandos｜risk：Ted 承認大型直播帶來的訂戶可能有稍高的流失率，但稱符合模型預期。（原話："they can exhibit slightly higher churn"）
- 2026-07-16｜Theodore Sarandos｜commitment：Ted 表示會持續擴大全球直播賽事行事曆。（原話："build out that global live event calendar"）
- 2026-07-16｜Gregory Peters｜competition：Greg 稱對與 TF1 的整合表現滿意（合作僅約四週）。（原話："pleased with the performance we are seeing in that integration"）
- 2026-07-16｜Gregory Peters｜competition：Greg 稱免費方案在部分市場可能可行，並表示會持續考慮。（原話："free is something that we're going to continue to consider"）
- 2026-07-16｜Gregory Peters｜customer：Greg 確認正在多個國家測試針對新加入會員的免費試用。（原話："we're testing free trials for non-rejoining new members"）
- 2026-07-16｜Theodore Sarandos｜product：Ted 稱影音 podcast 的觀看是增量，且出現在非黃金時段。（原話："convinced us that this viewing is definitely incremental for us"）
- 2026-07-16｜Gregory Peters｜margin：Greg 稱廣告方案與無廣告標準方案的每會員營收差距正在縮小。（原話："that gap is narrowing"）
- 2026-07-16｜Gregory Peters｜customer：Greg 稱上半年美國、墨西哥、西班牙等市場的調價進展順利。（原話："markets like U.S., Mexico, Spain. They've gone well."）
- 2026-07-16｜Gregory Peters｜product：Greg 稱雲端遊戲月活躍玩家自去年 10 月以來成長 11 倍。（原話："monthly active players for cloud games have increased 11x"）
- 2026-07-16｜Gregory Peters｜capital_allocation：Greg 稱遊戲投資相對整體內容支出仍很小，會依表現調整。（原話："still very small relative to our overall content spend"）
- 2026-07-16｜Theodore Sarandos｜competition：Ted 稱產業整併已持續十年以上，公司專注於會員與健康成長。（原話："the industry has been consolidating for over 10"）
- 2026-07-16｜Theodore Sarandos｜product：Ted 稱生成式 AI 工作流程已用於約 300 部作品。（原話："gen AI workflows now have been used in roughly 300 of"）
- 2026-07-16｜Theodore Sarandos｜product：Ted 以《American Experiment》舉例，AI 強化片段製作速度與成本。（原話："produced twice as fast and at half the cost of previous options"）
- 2026-07-16｜Theodore Sarandos｜capital_allocation：Ted 稱 AI 省下的成本可能再投入更多內容。（原話："So the cost savings will likely be"）
- 2026-07-16｜Theodore Sarandos｜commitment：Ted 重申公司主要是建造者而非買家。（原話："we are primarily builders, not buyers"）
- 2026-07-16｜Theodore Sarandos｜commitment：Ted 稱進行大型併購的門檻很高。（原話："we have a very high bar to do any big M&A"）
- 2026-07-16｜Spencer Neumann｜capital_allocation：CFO 稱第二季買回 47 億美元股票，為單季歷史最大。（原話："we repurchased $4.7 billion of shares this"）

### 問答異常語氣（迴避／改口／保留）
- NFLX_Q2_2026_Earnings_Call_20260716.md｜問：參與度品質指標（Rob Sanderson）：哪些內部指標支撐「品質改善、時數軟化」的說法，成長放緩到何時會成為疑慮？｜答法：未回答疑慮門檻；表明不揭露品質指標細節，改談直播與動畫的時數差異及上半年時數 +2%。
- NFLX_Q2_2026_Earnings_Call_20260716.md｜問：AI 與 200 億美元現金內容預算（Sean Diffley）：成本節省會否降低預算，或再投入？｜答法：未給預算數字或方向，只說節省『可能再投入更多內容』，語氣為『likely』。
- NFLX_Q2_2026_Earnings_Call_20260716.md｜問：併購傳聞（Dan Kurnos）：Lionsgate、NBCUniversal 傳聞與大型併購的界線。｜答法：拒絕評論市場臆測，改重申資本配置原則與『builders, not buyers』。

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 2 | 2 |
| customer_second_source | not_applicable | 0 | 0 |
| customer_concentration_credit | not_applicable | 0 | 1 |
| supply_demand_durability | found | 1 | 2 |
| regulatory_antitrust | found | 3 | 3 |
| reg_tariff_export | found | 3 | 3 |
| geo_supply_chain | found | 1 | 2 |
| end_markets | found | 3 | 3 |
| substitute_technology | found | 2 | 1 |
| channel_business_model_shift | found | 3 | 2 |
| capital_markets_pricing | found | 5 | 4 |
| major_events | found | 5 | 4 |

未涵蓋／不適用軸的查詢詞原文（供判相關性）：
- **customer_second_source**（not_applicable）：（無查詢記錄）
- **customer_concentration_credit**（not_applicable）：Netflix 10-K concentration of credit risk customers no single customer more than 10% revenue

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260717","verdict":"進場","role":"衛星","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"廣告＋定價雙引擎，在觀看時數僅 +2% 下仍撐住 11-13% 營收成長","columns":{"2Y 驗證點":"FY26 廣告約 $3B；FY27 營收 ≥+10%","5Y 驗證點":"FY30 廣告 ≥$8B；營收 CAGR ≥10%","10Y 驗證點":"營收 &gt;$90B","具體數字門檻":"FY26 廣告 ≥$2.6B（guide $3B）；廣告 CPM ≥$25（現約 $30，自 2022 上線的約 $65 下滑）；Q3'26 UCAN YoY ≥+9%","信息來源":"Netflix Q2'26 股東信（2026-07-16）；廣告產業 CPM 彙整（信心 med）","漂移觸發條件":"連 2 季 FX 中性營收 YoY &lt;+10% → 削弱；或 2 年期堆疊 YoY 跌破 27%（vs 2026 全年穩定約 29%）→ 基期歸因證偽"}},{"id":"H2","text":"營運槓桿把 OM 由 29.5% 推至 33%+（FY27），且不被體育版權通膨打斷","columns":{"2Y 驗證點":"FY26 OM 31.5%（7/16 已重申）；FY27 OM guide ≥33%","5Y 驗證點":"FY30 OM ≥35%","10Y 驗證點":"OM 穩定 35-38%","具體數字門檻":"FY26 OM 31.5%（明文重申）；增量 OM ≥45%（現 46.5-56.8%）；內容攤銷成長率 − 營收成長率 &lt;0（現 −3~−4pp）","信息來源":"Netflix Q2'26 股東信；本報告增量 OM 推導（§6.B③）","漂移觸發條件":"內容攤銷成長率 − 營收成長率 連 2 年 &gt;0 → 削弱"}},{"id":"H3","text":"市場不再進一步降檔——終端倍數守住 18x（成熟複利框架），不滑向 11-14x（成熟媒體框架）前份 H3「估值自 5Y 低檔 re-rate 至 23-25x」本次判定反轉，已自報酬引擎移除並改寫為此防禦型假設（§12.3）","columns":{"2Y 驗證點":"Fwd PE（FY+2）≥15x","5Y 驗證點":"FY31 終端 PE ≥18x","10Y 驗證點":"—","具體數字門檻":"Fwd PE（FY+2）≥15x（現 17.75x）；對照錨：Disney 約 17-18x 而 Netflix 的 ROIC 是它的約 3.7 倍","信息來源":"本報告 §11.4／§11.5；賣方目標價下修追蹤","漂移觸發條件":"Fwd PE（FY+2）連 2 季 &lt;15x 且 FY27 共識 EPS 未上修 → 降檔確認、H3 反轉"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"注意力份額結構性流失至 YouTube／短影音 — Netflix 佔美國電視觀看 9.0%（2026-01）→7.8%（2026-04），YouTube 12.7%→13.4% 連 11 個月居首、2026-04 領先第二名 4.0pp（該榜開辦以來最大）；Netflix 上半年觀看時數僅 +2%，而串流總份額創 47.6% 新高——餅在變大，Netflix 那塊沒有。攻擊者資本量級：YouTube 隸屬 Alphabet（市值約 Netflix 的 10 倍）且內容成本 ≈0。","columns":{"對應假設":"H1（傳導至定價力）＋H2（被迫加碼內容）","時間尺度":"🔥 中期（4-6 季）","監測指標":"Nielsen Media Distributor Gauge 之 Netflix 月份額","警戒閾值":"連 6 個月 &lt;8% → 護城河趨勢降 ↓＋停止加碼並減至 starter"}},{"id":"R2","text":"體育版權成本通膨打斷 OM 階梯 — 全球體育版權 2026 支出 $673.4 億（+9.6% YoY，S&amp;P Global）；FIFA 2030/34 美國轉播權傳出報價 $15-20 億 vs Fox 2026 屆 $4.85 億（CNBC, 2026-07）；NFL 2030 起重新競標、與世足爭同一批預算。Netflix 現階段直播僅佔內容支出「just over 5%」——一次得標就是 step change。","columns":{"對應假設":"H2","時間尺度":"🔥 中期（4-6 季）","監測指標":"內容攤銷成長率 − 營收成長率（現 −3~−4pp）；體育標案結果","警戒閾值":"連 2 年 &gt;0 → H2 死；或單一體育合約 &gt;$15 億/屆 → 重算 §6.E"}},{"id":"R3","text":"廣告定向受監管限制壓縮 CPM — 德州檢察長 Ken Paxton 於 2026-05-11 對 Netflix 提告（未經適當同意違法蒐集用戶資料，含兒童）；另有廣告層隱私消費者集體訴訟。CPM 已自 2022 上線初期約 $65 降至約 $30（程序化 $20-30、直接 IO $45-65；第三方彙整，信心 med），主因供給擴張與 Prime Video 廣告開賣的競價壓力。","columns":{"對應假設":"H1（廣告腿）","時間尺度":"🐢 長期（2+ 年）","監測指標":"公司損益層閘（不預測監管結果）：FY 廣告營收 vs guide；第三方 CPM 追蹤","警戒閾值":"FY26 廣告 &lt;$2.6B，或 CPM &lt;$25 → H1 廣告腿削弱"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"starter 1%·帽 3%·加碼凍結至 Q3'26 財報（2026-10）；解凍條件＝UCAN YoY ≥+11%","irr_base_pct":12.5,"ev5y_pct":72.8,"drift_watch_prior":{"dca_verdict":"進場","dca_role":"衛星","signal":"B","val":"🟢","ma":"🟠","trap":"🟡","moat_trend":"→","runway_post_y5":"🟡","asym_ratio":6.6,"ev5y_pct":72.8,"irr_base_pct":12.5,"max_dd_pct":-48.0,"bull_5y_price":180.4,"bear_5y_price":52.8,"p_bull_pct":25.0,"p_bear_pct":28.0,"rearm_trigger":"starter 1%·帽 3%·加碼凍結至 Q3'26 財報（2026-10）；解凍條件＝UCAN YoY ≥+11%","price_at_dd":67.97,"archetype":"品質複利成長","cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"NFLX","date":"2026-10-22","schema":"v15.2","contract":"v19","company_name":"Netflix, Inc."},"oneliner":"美國片單與廣告進度落後，注意力份額小幅流失；但流失率改善、調價順利、營益率續升。FY2 本益比約 17 倍沒有計入太多成長，續抱試單，等 2027 年 1 月全年指引再決定是否加碼。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/NFLX_20261022/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/NFLX_20261022/scenario.json","answers":{"q1_business":{"verdict":"賺全球付費家戶的月費，加上快速成長的廣告預算；錢卡在『同一筆內容攤銷能讓多少家戶、以多高單價分攤』這一節點。","reasoning":"Q3'26 營收 128.7 億美元，GAAP 營益率 34.6%；公司說優於預測主要是費用認列時點，不是結構改善。TTM 毛利率 49.1%，從 2022 年 39.4% 逐年升到 2025 年 48.5%。全年營收點估 511 億美元（+13%），Q4 指引 134.4 億美元（+12%）。CFO 2026-10-20 說收入有三個槓桿：會員數、單價、廣告。Ted 2026-10-20 說約 95% 的內容支出和幾乎全部營收都在核心串流。區域營收：UCAN 56.3 億美元，年增 11%；EMEA 41.1 億美元，年增 11%（匯率中性 9%）；LATAM 16.0 億美元；APAC 事實表未涵蓋。單點依賴方面，客戶是分散的消費者，沒有集中度問題；公司稱不依賴任何單一內容供應商，但這些供應商同時也是競爭者。產業時鐘在擴張期：全球線上影音營收 2025 年 +13.5%，付費電視 −4%；不過訂閱數成長預期 2026 年降到個位數，擴張已進入後段。供需持久性屬結構性持久：收視從線性電視往串流遷移仍在進行，工作室端持續整併，不是會反轉的週期。","fact_refs":["f_kpi0_gaap","f_kpi1_gaap","f_kpi2_gaap","f_kpi5_q4_2026","f_kpi6_2026","f_peer_nflx_gross_margin_pct","f_earnings_recency"],"verdict_values":{"revenue_quality":"以訂閱月費為主，可預測性高；廣告占比仍小，但今年成長逾 80%（Greg 2026-10-20）；分部只按地區揭露","unit_econ_note":"美國每小時觀看付費是 SVOD 中最低，對手有時超過兩倍（Greg 2026-10-20）；2026 年調價後流失率仍年改善","archetype":{"primary":"品質複利成長","secondary":null,"confidence":"中","fingerprint":"營收雙位數成長、營益率逐年擴張、FCF 利潤率約兩成的輕資本訂閱模式"},"industry":{"clock_phase":"II","sd_verdict_source":"結構性持久：Omdia 2025 年全球線上影音營收 +13.5% 至 1,760 億美元，付費電視 −4% 至 1,700 億美元，收視遷移單向進行；但 2026 年訂閱數成長預期降到個位數，擴張進入後段","bargaining":{"up":"內容供應商同時是競爭者，但 Disney、Globo 等新授權案顯示 Netflix 是首選買方，且不依賴單一供應商；體育版權是議價最弱的環節","down":"消費者分散、無集中度；2026 年各市場調價反應與過往一致","geo":"美國電影進口關稅、EU 網路使用費是政策變數，法源與時點皆未定"},"profit_pool_dir":"由線性電視往串流遷移，Netflix 是淨流入方","tam_table":[{"item":"全球線上影音營收 2025","value":"1,760 億美元，年增 13.5%（Omdia）"},{"item":"全球付費電視營收 2025","value":"1,700 億美元，年減 4%（不含廣告）"},{"item":"Netflix 2025 營收對線上影音營收","value":"約 26%（451.8÷1,760，口徑不同，只看量級）"},{"item":"全球線上影音訂閱數 2025 年底","value":"22.4 億，年增 17.6%，預期 2026 年降到個位數"},{"item":"可觸及家戶","value":"約 8 億戶（CFO 2026-07-16）；Netflix 會員數與滲透率事實表未涵蓋"},{"item":"營業利益池 5 年前→現","value":"事實表未涵蓋；方向為串流淨流入"}]}}},"q2_moat":{"verdict":"護城河方向持平：定價力穩定，但注意力份額小幅流失，美國片單與廣告兩處的執行落後。","reasoning":"護城河機制是規模。全球最大的付費家戶基數分攤原創內容成本，讓美國每小時觀看單價在 SVOD 中最低（Greg 2026-10-20 稱對手每小時價格有時超過兩倍），因此有反覆調價的空間。支持方向的證據：毛利率 2022→2025 年由 39.4% 升到 48.5%，營益率由 17.8% 升到 29.5%；2026-03 美國全方案調價後，Q3 全球與美國流失率都年改善且優於預測。反向證據：Nielsen 美國電視觀看份額 8.3%→7.9%，同期 YouTube 12.8%→13.5%、Prime Video 3.6%→4.2%；管理層自承美國片單成長『沒有我們想要的快』，更換內容長、裁員，廣告進度也落後年初的積極目標。同業表是廣告與注意力平台：Netflix 營益率 29.7%，低於 META 38.1% 與 GOOGL 33.1%，高於 PINS 6.3% 與 ROKU 5.3%。同業 ROIC 事實表未涵蓋，無法驗證報酬價差方向。評分：執行 8、定價 8，YouTube 的生態攻擊扣 1 分，合計 7，等級 B。","fact_refs":["f_peer_nflx_gross_margin_pct","f_peer_nflx_operating_margin_pct","f_peer_nflx_fcf_margin_pct","f_peer_meta_operating_margin_pct","f_peer_googl_operating_margin_pct","f_peer_pins_operating_margin_pct","f_peer_roku_operating_margin_pct"],"verdict_values":{"moat":{"mechanism":"規模分攤：全球最大付費家戶基數攤提原創與在地內容成本，加上推薦系統，使每小時觀看單價最低、調價空間最大","execution":8,"pricing":8,"grade":"B","trend":"→","trend_evidence":"定價面穩定：2026-03 美國全方案調價後，Q3 全球與美國流失率年改善且優於預測（Greg 2026-10-20）。執行面也判穩定但偏弱：財務面營益率續升，內容面則是美國片單不夠好、更換內容長、廣告落後。Nielsen 份額 8.3%→7.9% 是最接近轉向下降的證據，門槓見風險一。","competitor_notes":[{"name":"GOOGL","strategy_note":"YouTube 是最直接的攻擊者：美國電視觀看份額 13.5% 且仍在升，內容成本由創作者承擔"},{"name":"META","strategy_note":"爭的是手機零碎時間與廣告預算，不是電視大螢幕；利潤率較高但模式不同，不宜當估值錨"},{"name":"PINS","strategy_note":"只在廣告預算上邊際競爭，營益率約 6%，威脅低"},{"name":"ROKU","strategy_note":"通路與廣告夥伴兼對手；Roku Channel 份額 2.5%→3.0%，營益率約 5%"},{"name":"Amazon Prime Video","strategy_note":"份額 3.6%→4.2%，廣告開賣後壓低整體廣告單價；不在同業表內，無利潤率數字"}],"spread_notes":null,"peer_na_reason":"同業表為廣告與注意力平台，不是串流同業，且沒有 ROIC 數字，報酬價差無法計算","threats":[{"level":"🔴","text":"YouTube 與短影音搶走電視大螢幕的觀看時間，攻擊者內容成本接近零、背後資本量級遠大於 Netflix","p":35,"evidence_refs":["competitive_share_entrants#1","competitive_share_entrants#0"]},{"level":"🟡","text":"生成式 AI 降低內容製作門檻，新進者與使用者生成內容平台增加供給；Netflix 自身也在用 AI 降低成本","p":20,"evidence_refs":["substitute_technology#0"]},{"level":"🟡","text":"反壟斷與政策：DOJ 曾調查 Netflix 對獨立製片的議價力，倡議團體發起反壟斷運動，美國電影關稅未定案","p":15,"evidence_refs":["regulatory_antitrust#1","regulatory_antitrust#2","reg_tariff_export#0"]}],"roic_durability":{"quadrant":"高利益率×周轉率待補（投入資本事實表未涵蓋）","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者、決策者、付款者多在同一家戶，三個環節都成立。Q3'26 全球與美國流失率年改善且優於預測，2026 年各市場調價的會員反應與過往一致（Greg 2026-10-20）。娛樂屬於想要而非需要，但每小時單價是美國 SVOD 最低，取消的動機低"},{"item":"決策層級","level":"🟡","text":"替代性要在家戶『今晚看什麼』這一層衡量：月訂閱隨時可取消、轉換成本低，對手是所有螢幕時間而不只串流。兩個代理變數方向相反：調價後流失率在改善，Nielsen 觀看份額由 8.3% 降到 7.9%"},{"item":"價值鏈分配","level":"🟢","text":"毛利率 2022→2025 年由 39.4% 升到 48.5%，價值往 Netflix 移動。Disney、Globo 授權案顯示 Netflix 是首選買方，且不依賴單一供應商（Ted 2026-10-20）。最弱環節是體育版權，直播約占 2026 年內容預算 5%（Greg 2026-07-16）"},{"item":"社會容忍度","level":"🟡","text":"反壟斷關注在升溫：DOJ 審 WBD 案時調查 Netflix 對獨立製片的議價力，倡議團體 2026-07 發起『Netflix is a Monopoly』運動；EU 網路使用費與美國電影關稅屬政策風險。目前價格仍低於經濟上限，還沒碰到社會容忍的天花板"}],"roiic":"約 127%（代理值）","reinvest_rate":"約 13.8%（代理值）","endo_ceiling":17.5,"formula_note":"代理計算：以淨利代 NOPAT、以淨利減 FCF 代再投資。2024 年再投資 87.1−69.2＝17.9 億美元；2025 年淨利增量 109.8−87.1＝22.7 億美元，增量報酬約 127%。2025 年再投資率（109.8−94.6）÷109.8＝13.8%，內生成長上界約 17.5%。限制：內容支出以攤銷計入損益，FCF 口徑會低估真實再投資；增量報酬多來自對既有用戶調價，應視為上限而非常態"}}}},"q3_growth":{"verdict":"五年後的成長跑道中等：成熟市場靠單價與廣告，新興市場靠會員，還沒有看到串流本業以外的第二條需求曲線。","reasoning":"成長來源是量（新興市場會員）、價（成熟市場調價）、廣告（今年成長逾 80%，2027 年新增 15 國廣告方案）三者；沒有併購（WBD 案已終止），淨回購每年約 1.3%。共識 EPS：FY2025A 2.53、FY2026E 3.59、FY2027E 3.80、FY2028E 4.56，三年年複合約 21.7%，算法是（4.56÷2.53）^(1/3)−1。EPS 分析師家數事實表未涵蓋（營收共識 FY1 40 家、FY2 45 家）。FY2027E 只比 FY2026E 高 6%，營收共識卻高 10.8%；推論 FY2026E 含 2026-02 收到的 28 億美元 WBD 終止費（稅前約每股 0.67 美元），這是未證推論。內生上界約 17.5%（見護城河段），缺口約 4pp，可歸因於營益率擴張（2025 年 29.5%，FY26 指引 31.5%）與淨回購，不靠重新評價。跑道：管理層稱全球可觸及家戶約 8 億戶（2026-07-16），但 Netflix 會員數與滲透率事實表未涵蓋，跑道年數無法計算；美英澳已深度滲透，成長偏向單價與廣告（Greg 2026-10-20）。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_kpi6_2026"],"verdict_values":{"growth":{"driver_mix":"價（成熟市場調價）＋量（新興市場會員）＋廣告；無併購；淨回購約每年 1.3%","runway_years":"事實表未涵蓋（缺會員數與滲透率）","runway_post_y5":"🟡","endo_ceiling_basis":"引護城河段：增量報酬約 127%×再投資率 13.8%≈17.5%，代理值且偏上限","segments":[{"item":"UCAN","value":"Q3'26 營收 56.28 億美元，年增 11%（Q2'26 為 10%）"},{"item":"EMEA","value":"41.07 億美元，年增 11%，匯率中性 9%"},{"item":"LATAM","value":"16.03 億美元，成長率未取得"},{"item":"APAC","value":"事實表未涵蓋；印度 Q3 營收年增近 20%（Greg 2026-10-20）"}],"decay_signals":[{"signal":"毛利率連 2 季年減","lit":false,"evidence":"TTM 毛利率 49.1% 高於 2025 年 48.5%"},{"signal":"核心市占近 12 個月縮減","lit":true,"evidence":"Nielsen 美國電視觀看份額 8.3%→7.9%"},{"signal":"主力產品提價後銷量下滑","lit":false,"evidence":"2026-03 調價後流失率年改善"},{"signal":"EPS 成長顯著高於營收成長","lit":true,"evidence":"共識 EPS 三年年複合 21.7%，營收約 12%，差距來自營益率擴張與回購"},{"signal":"FCF÷淨利連 2 年低於 0.75","lit":false,"evidence":"2024 年 0.79、2025 年 0.86"},{"signal":"SBC 占營收逾 5% 且上升","lit":false,"evidence":"SBC 約營收 1%"},{"signal":"TAM 萎縮或被替代技術壓縮","lit":false,"evidence":"線上影音營收 2025 年 +13.5%"},{"signal":"產業估值倍數近 3 年系統性下移","lit":false,"evidence":"自身本益比在 4 個年度端點中最低，但產業倍數事實表未涵蓋"},{"signal":"維持性資本支出占 FCF 逾 60%","lit":false,"evidence":"內容維持性支出拆分事實表未涵蓋"},{"signal":"停止投資新產能且營收 3 年內下滑","lit":false,"evidence":"2026 年內容支出約 200 億美元，較 2025 年 180 億增加"}],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"資本配置中等偏好：股權稀釋低、回購持續；但回購價格是否夠便宜無法驗證，且曾嘗試企業價值 827 億美元的大型併購。","reasoning":"FCF÷淨利 2024 年 0.79、2025 年 0.86，轉換率健康；Q3'26 FCF 28.8 億美元。SBC 占 Q3 營業利益 3%，約營收 1%。以淨利÷稀釋 EPS 推算，稀釋股數 2022→2025 年由約 45.1 億降至 43.4 億，每年淨縮減約 1.3%。Q2'26 回購 47 億美元，是單季歷史最大（CFO 2026-07-16）。淨負債 69.1 億美元（含租賃），另收到 WBD 終止費 28 億美元。現金去向四分、債務到期結構、回購均價事實表未涵蓋。爭議點：2025-12 公司簽下企業價值 827 億美元的 WBD 案，並開 50 億美元循環信貸，與 Ted 2026-07-16『主要是建造者不是買家』的說法不一致。此案雖已終止且淨賺終止費，仍顯示大型併購是管理層的選項。","fact_refs":["f_kpi3_fcf","f_kpi4_sbc","f_net_debt_m","f_shares_diluted_m"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":false,"passed":null,"input":"近三年沒有完成的重大併購；WBD 案終止並收 28 億美元終止費，沒有已實現的增量報酬可算"},{"name":"buyback_yield","applicable":true,"passed":null,"input":"回購期間股價與 10 年期殖利率事實表未涵蓋；以現價 FY2 本益比 17.1 倍換算盈餘收益率約 5.8%，10 年期殖利率要 ≤3.8% 才過"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"SBC 占 Q3'26 營業利益 3%；2022→2025 年稀釋股數約 45.1 億→43.4 億，每年淨縮減約 1.3%"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購撐：WBD 案已於 2026-02-27 終止；現金去向四分與回購均價事實表未涵蓋"}}}},"q5_valuation":{"verdict":"現價只要求 FY27 起 EPS 年增約一成、本益比維持在 17 倍上下，就有雙位數報酬。我相信成長，但不確定市場會不會改用成熟媒體股的 13 倍框架。","reasoning":"股價 65.04 美元。FY1 本益比 18.1 倍，FY2 本益比 17.1 倍；trailing 本益比 18.8 倍，是 4 個年度端點中最低；P/S 5.45 倍（分位 17.4%），前瞻 EV/S 5.43 倍。FY1 分母可能含一次性終止費，主尺改用 FY2。PEG：FY2 本益比÷共識三年 EPS 年複合 21.7%≈0.8；改用基本情境年複合 12.6% 約 1.4，仍在合理區。賣方目標價：2026-09 平均約 93.66 美元，另一來源共識 103 美元，區間 80–151 美元（高低比 1.9 倍，低於 2.5 倍），現價比均值低約 30–37%，方向支持本次不賣的結論，但賣方目標價在下修中。基本情境：一年後以 17 倍乘 FY2028E 4.56 美元得 77.5 美元（+19%）；三年後 17 倍乘 5.85 美元得 99.5 美元（+53%）。共識 FY1 EPS 近三個月 +0.6%，FY2、FY3 未動，跌幅來自倍數不是盈餘。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_pe_current","f_pe_percentile","f_ps_current","f_ps_percentile","f_ev_s_current","f_ev_s_fwd","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_3m_fy1_pct","f_consensus_rev_fy2_pct"],"verdict_values":{"valuation":{"basis":"FY2 本益比（FY2027E EPS 3.80）為主尺；FY1 分母可能含一次性終止費，只作對照","tier":"大型成熟複利","peers":{"expanded":false,"reason":"事實表同業表只有利潤率，沒有同業本益比；終端倍數的同業對照是資料缺口，改用 Netflix 自身 4 個年度端點與 13–23 倍的框架區間定錨"},"fwd_pe":18.12,"peg":0.83,"percentile_5y":0.0,"val_light":"🟢","val_light_derivation":"FY2 本益比 17.1 倍（65.04÷3.80）。共識 FY25A→FY28E EPS 年複合 21.7%，PEG 約 0.8；trailing 本益比 18.8 倍是 4 個年度端點最低（以年度端點代替五年分位），P/S 分位 17.4%。改用基本情境 EPS 年複合 12.6%，PEG 約 1.4，仍在合理區。結論：便宜偏合理","upside_short_pct":19.2,"upside_mid_pct":52.9,"denominator_disputed":false,"denominator_note":"FY26 EPS 可能含 WBD 終止費一次性收益（推論未證），所以主尺改用 FY2；以 FY2 計本益比 17.1 倍，結論不變"}}},"q6_how_wrong":{"verdict":"最可能看錯在：美國注意力流失比流失率更早反映問題。份額下滑先傷內容效率，兩三年後才傷到定價。","reasoning":"26 週股價 −30.2%，RSI 32.6，市場已把觀看疲軟計入股價。共識 FY1 EPS 近三個月 +0.6%，FY2、FY3 未動，跌幅來自倍數不是盈餘。衰退信號亮 2 個（核心市占縮減、EPS 成長遠高於營收成長），屬中度陷阱風險。三個視角的反證寫在反證紀錄。歷史最大回撤、訴訟金額事實表未涵蓋。","fact_refs":["f_week26_return_pct","f_rsi14","f_consensus_rev_fy1_pct","f_consensus_rev_3m_fy1_pct"],"verdict_values":{"trap":{"verdict":"🟡","label":"注意力份額下滑與利潤擴張並存，要看 2027 年全年指引"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":3.59,"pe":18.12,"basis":"FY1（FY2026E）共識 EPS 3.59，和終端倍數同為前瞻本益比口徑；可能含一次性終止費"},"eps":{"bull":[3.95,4.85,5.75,6.75,7.8],"base":[3.8,4.56,5.2,5.85,6.5],"bear":[3.45,3.4,3.5,3.62,3.75]},"pe":{"bull":23,"base":17,"bear":13},"p":{"bull":22,"base":48,"bear":30},"yield_pct":{"dividend":0,"net_buyback":0},"second_stage":{"bull_cagr_pct":12,"base_cagr_pct":8},"max_dd":{"lo":-50,"hi":-35,"basis":"極端空頭：FY+1 EPS 3.59×0.9＝3.23，乘空頭本益比 13×0.8＝10.4 倍，約 33.6 美元，較現價 −48%。溫和端為空頭情境終值 48.75 美元（−25%）再加上財報日跳空。26 週已跌 30.2%，所以區間取 −35% 到 −50%","trigger_time":null},"basis":{"bull":"廣告 2027 年後每年成長 30% 以上，FY31 營益率達 38%，營收年複合 12%；終端 23 倍，回到成長股框架","base":"FY27、FY28 照共識，之後 EPS 年增 11–14%：營收年複合約 10%、營益率每年擴 1pp、淨回購約 1%/年；終端 17 倍。回購效果已含在 EPS 路徑，殖利率欄不重複計入","bear":"營收成長 2027 年起跌破 10%，之後降到 5–7%；營益率卡在 31–32%，FY26 一次性收益消失；終端 13 倍，取成長熄火到 5–10% 的成熟媒體框架"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"YouTube 美國電視觀看份額 12.8%→13.5%，Netflix 8.3%→7.9%；生成式 AI 降低內容製作門檻，新進者增加","assumption":"觀看份額流失最後會傳導到定價力與流失率","consequence":"營收成長 2028 年後降到 5–7%，本益比降到 13 倍，五年後股價約 45–50 美元","ruling":"部分採納：空頭機率給 30%。這條故事與 Single Thing 部分重疊，FY27 指引跌破 10% 是它最早出現的形式，Single Thing 保留不動","watch":"Nielsen 月份額、UCAN 營收年增率","evidence_refs":["competitive_share_entrants#1","substitute_technology#0"],"fact_refs":["f_week26_return_pct"]},{"view":"論點成功但股東經濟變差","evidence":"2025-12 管理層簽下企業價值 827 億美元的 WBD 案並開 50 億美元信貸，與 Ted 2026-07-16『主要是建造者不是買家』的說法有落差。年初 EPS 預估因內容與廣告成本下修 3.7%；FY26 營益率指引 31.5% 低於共識 32.7%","assumption":"營收繼續成長，但被體育版權、內容成本或大型併購吃掉","consequence":"EPS 年增落到 8% 以下，增量報酬下降","ruling":"採納為監測項：WBD 案證明管理層願意做超大併購；再出現超過市值 10% 的併購就重跑判斷","watch":"併購公告、FY27 營益率指引","evidence_refs":["capital_markets_pricing#1","capital_markets_pricing#4"],"fact_refs":["f_net_debt_m"]},{"view":"價格已反映太多","evidence":"FY1 本益比 18.1 倍看似便宜，但 FY26 EPS 可能含 28 億美元終止費，剔除後約 21–22 倍；Citi 估電影關稅最壞情境 EPS −20%","assumption":"市場用了被一次性收益墊高的分母，真實估值不便宜","consequence":"若以乾淨 FY26 EPS 定價，下行空間比表面大","ruling":"反駁：以不含一次性收益的 FY2 計是 17.1 倍，仍在 4 個年度端點最低。電影關稅法源不明、白宮未定案，列監測，不放入基本情境","watch":"2027-01 股東信是否揭露終止費入帳科目；關稅正式公告","evidence_refs":["reg_tariff_export#2"],"fact_refs":["f_fwd_pe_latest","f_pe_current"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 🟠 → 本次 🟠","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=🟠","side_b":"本次 ma=🟠","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 67.97 → 本次 65.04（-4.3%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=67.97","side_b":"本次 price_at_dd=65.04","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 67.97 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 67.97 美元：Bull 價 180.4、Bear 價 52.8，五年期望值 +72.8%，基準年化 12.5%，不對稱比 6.6","side_b":"本次情境、股價仍用 67.97 美元：Bull 價 179.4、Bear 價 48.75，五年期望值 +57.6%，基準年化 10.2%，不對稱比 4.25","ruling":"先換情境、股價不動：五年期望值少 15.2 個百分點，基準年化少 2.3 個百分點。不對稱比由 6.6 變為 4.25。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 67.97 美元：五年期望值 +57.6%，基準年化 10.2%，不對稱比 4.25","side_b":"本次情境、股價 65.04 美元：五年期望值 +64.7%，基準年化 11.2%，不對稱比 5.15","ruling":"再換股價、情境不動：起點價下跌 4.3%，五年期望值多 7.1 個百分點，基準年化多 1.0 個百分點，不對稱比由 4.25 升到 5.15。合計五年期望值比前份少 8.1 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"注意力份額對定價力","cause":null,"prior_field":null,"side_a":"觀看份額在下滑：Nielsen 8.3%→7.9%，YouTube、Prime Video 都在升；管理層自承美國片單不夠好","side_b":"定價力完好：Q3 全球與美國流失率年改善且優於預測，2026 年調價反應與過往一致，UCAN 營收年增 11%","ruling":"不可調和，方向相反。選 B 側。依據是流失率與營收是付費行為的直接證據，份額是落後於定價力的領先指標，目前還沒傳導到付費","evidence_level":"中","settle_metric":"Nielsen 月份額與 UCAN 營收年增率","if_then":["若 Nielsen 份額連 6 個月低於 8% 且 UCAN 營收年增低於 +9%，則護城河趨勢改判下降並減碼至 0.5%","若 2027-01 指引營收 ≥+10% 且營益率 ≥33%，則加碼至 3%","反向：若份額回升到 8.3% 以上，撤銷份額警示"],"evidence_refs":["competitive_share_entrants#1"]},{"axis":"現在就賣的最強論證","cause":null,"prior_field":null,"side_a":"美國片單弱、內容長更換、裁員、廣告落後、全年指引落到區間下緣；FY26 EPS 可能含終止費，乾淨本益比約 21–22 倍","side_b":"FY2 本益比 17.1 倍，共識 EPS 三個月未下修，流失率改善，跌幅全來自倍數","ruling":"不賣，維持試單，2027-01 指引前不加碼。賣出論證全部是執行與情緒面的證據，沒有一條出現在盈餘預估或流失率上","evidence_level":"中","settle_metric":"FY27 營收與營益率指引","if_then":["若 FY27 營收指引低於 +10%，減碼至 0.5%；營益率指引同時低於 32.5%，清倉","若股價跌至 55 美元以下且 FY27 共識 EPS 未下修，分批加至 2%"],"evidence_refs":["capital_markets_pricing#0"]},{"axis":"管理層財測對照","cause":"新證據","prior_field":null,"side_a":"2026-07-16 CFO Spencer Neumann：全年營收成長 13% 至 14%；Greg 當時稱廣告為積極目標","side_b":"2026-10-20 股東信：全年營收點估 511 億美元，+13%，比前次區間中點低 0.2%；Greg 承認廣告落後年初目標，但今年仍成長逾 80%","ruling":"落在區間下緣但沒有失守，視為三槓桿論點輕度削弱，不改論點","evidence_level":"高","settle_metric":"Q4'26 營收對指引 134.42 億美元","if_then":["若 Q4'26 營收低於指引，H1 記一次削弱"],"evidence_refs":["capital_markets_pricing#0"]},{"axis":"產業態勢","cause":null,"prior_field":null,"side_a":"競爭惡化：YouTube、Prime Video、Peacock 的份額都在升，Netflix 在降","side_b":"結構轉好：線上影音營收 +13.5%、付費電視 −4%，工作室整併後供應方更需要 Netflix 的通路；其他結構變數包括反壟斷倡議與電影關稅","ruling":"雙向拉鋸：注意力競爭惡化，但收視遷移與內容授權結構轉好，兩股力量目前相抵","evidence_level":"中","settle_metric":"Nielsen 份額對比 Netflix 營收成長率","if_then":["若份額下滑同時營收成長跌破 10%，改判競爭惡化中"],"evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1"]},{"axis":"前份基本面結論漂移","cause":"新證據","prior_field":["signal","val","trap","moat_trend","runway_post_y5","archetype","cycle_position"],"side_a":"前份：綜合評等 B、估值綠、陷阱黃、護城河趨勢持平、五年後跑道黃、品質複利成長、非循環股、裁決進場、角色衛星","side_b":"本次：基本面判斷全部維持；裁決與角色由程式依本次輸入重算","ruling":"Q3 新證據正負相抵。正面：UCAN 年增 11%、流失率改善、共識 EPS 未下修。負面：廣告落後、全年指引落在區間下緣、美國片單弱與內容長更換。股價較前份 −4.3%，估值更便宜，但不改結論","evidence_level":"中","settle_metric":"2027-01 全年指引","if_then":["若 FY27 營收指引低於 +10%，護城河趨勢與跑道各降一檔重評"],"evidence_refs":["capital_markets_pricing#0"]},{"axis":"情境機率與回撤口徑","cause":"方法變動","prior_field":["p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份：多頭機率 25%、空頭機率 28%、最大回撤 −48%","side_b":"本次：多頭機率 22%、空頭機率 30%、最大回撤區間 −35% 至 −50%","ruling":"共識三年 EPS 年複合 21.7% 超過內生上界 17.5%，依規則空頭機率至少 30%；最大回撤改填區間，極端端點與前份相近","evidence_level":"高","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"加碼條件","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"starter 1%·帽 3%·加碼凍結至 Q3'26 財報（2026-10）；解凍條件＝UCAN YoY ≥+11%","side_b":"2027-01 指引 FY27 營收 ≥+10% 且營益率 ≥33% 才加碼至 3%；未達則維持 1% 試單、不追","ruling":"前份的加碼解凍條件已在 Q3'26 達成（UCAN 年增 11%），這條觸發器已發火。但同一季出現廣告落後與指引落區間下緣，所以不照舊條件加碼，改綁 2027-01 的全年指引","evidence_level":"高","settle_metric":"FY27 營收與營益率指引","if_then":["若指引達標則加碼至 3%","若指引未達則維持 1% 試單"],"evidence_refs":[]},{"axis":"Single Thing 變更","cause":"新證據","prior_field":["single_thing"],"side_a":"前份未設 Single Thing","side_b":"2027 年 1 月 Q4 財報給出的 FY27 營收成長指引低於 10%","ruling":"Q3 證據顯示雙位數成長是 17 倍與 13 倍兩種定價框架的分界，數學上是終值最大的單一敏感項，所以設為 Single Thing；發生即減碼，營益率指引同時跌破則清倉","evidence_level":"中","settle_metric":"FY27 營收成長指引","if_then":["若指引低於 10%，減碼至 0.5%；營益率指引同時低於 32.5%，清倉"],"evidence_refs":[]},{"axis":"減碼與清倉門檻","cause":"新證據","prior_field":["kill_metrics"],"side_a":"前份未設 kill 指標。前份風險門檻：Nielsen 份額連 6 個月低於 8% 則減至試單；FY26 廣告低於 26 億美元或 CPM 低於 25 美元；單一體育合約超過 15 億美元／屆；內容攤銷成長率減營收成長率連 2 年大於 0","side_b":"本次：Nielsen 門檻保留，並加上 UCAN 年增低於 +9% 才減碼；新增營收年增連 2 季低於 +10%、FY27 營益率指引低於 32.5% 兩條減碼與清倉門檻；廣告與 CPM 門檻保留，但本包沒有數據，標資料缺口","ruling":"單看份額容易誤判，因為流失率在改善，所以份額門檻要與營收同時成立才減碼；新增的兩條對應 Q3 暴露的指引下緣與重組成本","evidence_level":"中","settle_metric":"Nielsen 份額、季度營收年增率、FY27 營益率指引","if_then":["任一減碼門檻觸發，減碼至 0.5%；營收與營益率門檻同時觸發，清倉"],"evidence_refs":["competitive_share_entrants#1"]}],"triggers":[{"n":1,"text":"Q4'26 營收是否達到公司指引","type":"假設驗證","maps_to":"H1","metric":"Q4'26 營收","threshold":"低於 134.42 億美元","action":"記 H1 一次削弱，搭配 FY27 指引判斷","source_freq":"季度股東信","date":"2027-01"},{"n":2,"text":"FY27 營收成長指引跌破雙位數","type":"Single Thing","maps_to":"Single Thing","metric":"FY27 營收成長指引","threshold":"低於 10%","action":"減碼至 0.5%；營益率指引同時低於 32.5% 則清倉","source_freq":"年度指引","date":"2027-01"},{"n":3,"text":"注意力份額持續流失並傳導到營收","type":"風險","maps_to":"R1","metric":"Nielsen 美國電視觀看份額與 UCAN 營收年增率","threshold":"份額連 6 個月低於 8% 且 UCAN 年增低於 +9%","action":"減碼至 0.5%，重跑判斷","source_freq":"Nielsen 月報＋季度股東信","date":null},{"n":4,"text":"營益率擴張路徑被成本打斷","type":"風險","maps_to":"R2","metric":"FY27 營益率指引","threshold":"低於 32.5%","action":"減碼至 0.5%","source_freq":"年度指引","date":"2027-01"},{"n":5,"text":"電影進口關稅正式落地","type":"風險","maps_to":"R3","metric":"關稅適用範圍","threshold":"正式生效且適用串流原創","action":"停止加碼，以 EPS −20% 重算情境","source_freq":"白宮與商務部公告","date":null},{"n":6,"text":"全年指引確認雙引擎續航","type":"加碼","maps_to":"H1","metric":"FY27 營收與營益率指引","threshold":"營收 ≥+10% 且營益率 ≥33%","action":"加碼至 3%","source_freq":"年度指引","date":"2027-01"},{"n":7,"text":"價格先走、基本面未變時分批買回","type":"估值rearm","maps_to":"H1","metric":"股價與 FY27 共識 EPS","threshold":"股價 ≤55 美元且 FY27 共識 EPS 未下修","action":"分批加至 2%","source_freq":"每日股價＋共識快照","date":null},{"n":8,"text":"Q4 財報後全面複審","type":"複審日期","maps_to":null,"metric":"全年指引與 Nielsen 份額","threshold":"財報後一週內","action":"重跑判斷","source_freq":"一次性","date":"2027-01"}],"kill_metrics":[{"metric":"匯率中性營收年增率（季）","bear_threshold":"連 2 季低於 +10%","window":"2026Q4 至 2027Q2","source":"Netflix 季度股東信","last_status":"ok"},{"metric":"Nielsen Netflix 美國電視觀看份額","bear_threshold":"連 6 個月低於 8% 且 UCAN 年增低於 +9%","window":"滾動 6 個月","source":"Nielsen The Gauge 月報","last_status":"warning"},{"metric":"FY27 營業利益率指引","bear_threshold":"低於 32.5%","window":"2027-01 財報","source":"Netflix Q4'26 股東信","last_status":"unknown"},{"metric":"FY27 營收成長指引","bear_threshold":"低於 10%","window":"2027-01 財報","source":"Netflix Q4'26 股東信","last_status":"unknown"},{"metric":"FY26 廣告營收","bear_threshold":"低於 26 億美元（資料缺口，公司若揭露才可判）","window":"FY2026","source":"Netflix 股東信；本包未涵蓋","last_status":"unknown"}],"evidence_dismissed":[],"action_conditions":{"rearm_trigger":"2027-01 指引 FY27 營收 ≥+10% 且營益率 ≥33% 才加碼至 3%；未達則維持 1% 試單、不追","exec_line":"維持 1% 試單；Q4 財報（2027-01）前不加碼；跌到 55 美元以下且 FY27 共識 EPS 未下修，可分批加至 2%","holding_cap":"3%"}},"decision_inputs":{"signal":"B","ma":"🟠","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場把美國觀看疲軟與廣告落後外推成成熟媒體股，但共識 EPS 三個月未下修、流失率年改善、調價順利，跌幅全來自倍數壓縮；FY2 本益比 17.1 倍已接近成熟媒體框架的上緣","momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":false,"wait_for_price":null,"wait_for_price_condition":null},"decision_out":{"verdict":"進場","role":"衛星","row_hit":"9b","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟠'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場把美國觀看疲軟與廣告落後外推成成熟媒體股，但共識 EPS 三個月未下修、流失率年改善、調價順利，跌幅全來自倍數壓縮；FY2 本益比 17.1 倍已接近成熟媒體框架的上緣"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟢', moat_trend='→', week26=-30.24, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position=None, moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":false,"basis":"signal='B', val='🟢'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":false,"basis":"signal='B', val='🟢', ma='🟠'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":true,"basis":"signal='B', val='🟢', ma='🟠'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟢', ma='🟠'"},{"row":"QC-49","condition":"qc49_inherit_prior=False，不套用","hit":false,"basis":"qc49_inherit_prior=False"}],"pacing":[],"holding_cap":null,"requires_critic":[]},"thesis":{"H":[{"id":"H1","text":"會員、單價、廣告三個槓桿在觀看時數只有低個位數成長時，仍撐住雙位數營收成長","2y":"FY27 營收年增 ≥10%（共識約 +10.8%）","5y":"FY26–FY31 營收年複合 ≥9%","10y":null,"threshold":"Q4'26 營收 ≥134 億美元（指引 134.42 億美元，+12%）；UCAN 季營收年增 ≥+10%（Q3'26 為 11%）","source":"Netflix 季度股東信區域營收；2027 年 1 月全年指引","drift_rule":"匯率中性營收年增連 2 季低於 +10% 為削弱；連 3 季低於 +9% 為反轉"},{"id":"H2","text":"營益率每年擴張，FY28 達 34% 以上，體育版權與重組成本不打斷這條路","2y":"FY27 營益率指引 ≥33%（FY26 指引 31.5%）","5y":"FY31 營益率 ≥36%","10y":null,"threshold":"FY27 營益率指引 ≥33%；內容費用成長率低於營收成長率（2026 年內容費用約 +10%，營收 +13%）","source":"Netflix 股東信與年度指引；Ted 2026-07-16 內容費用預估","drift_rule":"FY27 指引低於 32.5% 為削弱；FY27 實際營益率低於 FY26 為反轉"},{"id":"H3","text":"廣告成為第二個成長引擎，廣告方案與標準方案的每會員營收差距持續縮小","2y":"2027 年廣告營收成長 ≥40%，15 國新廣告方案如期上線","5y":"FY31 廣告占營收 ≥12%","10y":null,"threshold":"管理層每季確認每會員營收差距在縮小；2027 年廣告成長率 ≥40%（2026 年逾 80%）","source":"Netflix 法說會與股東信；Greg 2026-10-20 說明","drift_rule":"連 2 季不再提差距縮小，或廣告成長低於 40%，為削弱；新國家上線延後超過 2 季為反轉"}],"R":[{"id":"R1","text":"注意力份額流向 YouTube 與短影音：Nielsen 美國電視觀看份額 8.3%→7.9%，YouTube 12.8%→13.5%","h_ref":"H1","clock":"🔥","threshold":"Nielsen 月份額連 6 個月低於 8% 且 UCAN 營收年增低於 +9%：護城河趨勢改判下降，減碼至 0.5%","evidence_refs":["competitive_share_entrants#1","competitive_share_entrants#0"]},{"id":"R2","text":"成本通膨與美國片單執行：FY26 營益率指引 31.5% 低於共識 32.7%；內容長更換，Q4 含約 120 個基點重組成本","h_ref":"H2","clock":"🔥","threshold":"內容費用成長率連 2 年高於營收成長率，或單一體育合約超過 15 億美元／屆，重算情境；FY27 營益率指引低於 32.5% 則減碼","evidence_refs":["capital_markets_pricing#1","capital_markets_pricing#4"]},{"id":"R3","text":"政策風險：電影進口 100% 關稅（Citi 估最壞 EPS −20%）、DOJ 調查 Netflix 對創作者的議價力、反壟斷倡議","h_ref":"H2","clock":"🐢","threshold":"關稅正式生效且適用串流原創，以 EPS −20% 重算；DOJ 或 FTC 對 Netflix 本身立案，減碼至 0.5%","evidence_refs":["reg_tariff_export#0","reg_tariff_export#2","regulatory_antitrust#1","regulatory_antitrust#2"]},{"id":"R4","text":"短期財測落差：Q3 指引曾低於市場，廣告進度落後年初目標，全年指引落在區間下緣","h_ref":"H3","clock":"⚡","threshold":"Q4'26 營收低於指引 134.42 億美元，或 FY27 營收指引低於 +10%，減碼","evidence_refs":["capital_markets_pricing#0"]}],"single_thing":{"description":"2027 年 1 月 Q4 財報給出的 FY27 營收成長指引低於 10%","why_fatal":"雙位數成長是市場用 17 倍（成熟複利）還是 13 倍（成熟媒體）定價的分界；跌破後基本情境終值少約 24%，三槓桿論點也同時失效","if_happens":"減碼至 0.5%；營益率指引同時低於 32.5% 則清倉","how_monitor":"2027-01 股東信全年指引；在那之前看 Q4 營收是否達 134.42 億美元","probability":"約 25%（12 個月內）。共識 FY27 營收 +10.8%，只比門檻高 0.8pp；CFO 2026-10-20 重申以維持雙位數成長為目標"}},"appendix_a":{"growth_durability":6,"quality_score":7,"ai_risk":"🟡","long_term_confidence":"中","fpe_fy2":17.12,"peg_fy2":0.79,"stress":{"pass":null,"total":null}},"eps_meta":{"base_eps_path":{"FY2025A":2.53,"FY2026E":3.59,"FY2027E":3.8,"FY2028E":4.56},"fy_end_month":12,"eps_basis":"GAAP 稀釋 EPS（拆股後口徑），共識取自 Koyfin 2026-10-21 快照，分析師家數事實表未涵蓋；FY2026E 可能含 WBD 終止費一次性收益（推論未證）"},"catalysts":[{"date":"2027-01","date_precision":"month","type":"guidance","event":"Q4'26 財報與 FY27 全年營收、營益率指引","impact":"高","watch":"營收成長是否 ≥10%、營益率是否 ≥33%"},{"date":"2026-11","date_precision":"month","type":"product","event":"感恩節前夕首場 NFL 直播；12 月聖誕節 NFL 賽事","impact":"中","watch":"直播帶來的新增會員與廣告收入"},{"date":"2027","date_precision":null,"type":"product","event":"15 個新國家上線廣告方案","impact":"中","watch":"上線時程是否延後、廣告成長率"},{"date":"2027","date_precision":null,"type":"product","event":"Narnia 等大型片 45 天戲院窗口上映","impact":"低","watch":"票房與上架後觀看時數"},{"date":null,"date_precision":null,"type":"regulatory","event":"美國電影進口關稅是否經 Section 232 正式落地","impact":"中","watch":"是否適用串流原創、公司損益影響"}]}
```

---

## ⑤ 覆蓋面（程式判定，你回的 ⑤ 燈號會被覆寫）

燈號 🟢：核心軸皆有證據或不適用，非核心軸也沒有空軸。核心軸由採證 agent 自報不適用（燈號不變，請看 note 理由）：customer_concentration_credit。

⑤ 的 reason 只需評論：空軸的查詢詞是否切題、判斷有沒有交代缺口對結論的影響。

---

## 尾段：回覆格式

只回一個 JSON 陣列，①–⑧ 每條一個元素，八個全出，不得跳號、不得多列，陣列外不得有任何文字（不加前言、不加 markdown 圍欄、不加附註）：

```json
[{"item": "①", "light": "🔴|🟡|🟢", "judgment_path": "$.路徑", "reason": "一句話"}]
```
