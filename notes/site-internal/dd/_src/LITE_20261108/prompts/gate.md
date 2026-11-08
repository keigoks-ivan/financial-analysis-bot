你是 DD 管線 v20 的判斷層閘（gate），標的 LITE（20261108）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（34 條）
- `f_kpi0_net_revenue_gaap`（q1_business）｜Net revenue (GAAP)＝1262.6 USD million｜期間與口徑：Q1 FY2027（季末 2026-09-26，公告於 2026-11-02）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 investor.lumentum.com Q1 FY27 press release（numbers.latest_quarter_kpis.items[0]，as_of Q1 FY2027（季末 2026-09-26，公告於 2026-11-02））
  - 註記：未查證
- `f_kpi5_gaap_gross_margin`（q1_business）｜GAAP gross margin＝51.0 %｜期間與口徑：Q1 FY2027（季末 2026-09-26，公告於 2026-11-02）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 investor.lumentum.com Q1 FY27 press release（numbers.latest_quarter_kpis.items[5]，as_of Q1 FY2027（季末 2026-09-26，公告於 2026-11-02））
  - 註記：n/a
- `f_kpi2_gaap_operating_income_ma`（q1_business）｜GAAP operating income / margin＝28.5 %｜期間與口徑：Q1 FY2027（季末 2026-09-26，公告於 2026-11-02）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 investor.lumentum.com Q1 FY27 press release（numbers.latest_quarter_kpis.items[2]，as_of Q1 FY2027（季末 2026-09-26，公告於 2026-11-02））
  - 註記：未查證
- `f_kpi1_non_gaap_operating_incom`（q1_business）｜Non-GAAP operating income / margin＝42.3 %｜期間與口徑：Q1 FY2027（季末 2026-09-26，公告於 2026-11-02）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 investor.lumentum.com Q1 FY27 press release（numbers.latest_quarter_kpis.items[1]，as_of Q1 FY2027（季末 2026-09-26，公告於 2026-11-02））
  - 註記：未查證
- `f_kpi4_guidance_q2_fy2027`（q1_business）｜Guidance: Q2 FY2027＝營收 $1.575B–$1.625B；non-GAAP 營業利益率 45.0%–46.0%；non-GAAP EPS $5.90–$6.20 range｜期間與口徑：Q1 FY2027 新聞稿（2026-11-02）對 Q2 FY2027 指引／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司新聞稿 investor.lumentum.com Q1 FY27 press release（numbers.latest_quarter_kpis.items[4]，as_of Q1 FY2027 新聞稿（2026-11-02）對 Q2 FY2027 指引）
  - 註記：未查證
- `f_earnings_recency`（q1_business）｜最近一次財報日＝2026-11-02 date｜期間與口徑：2026-11-02／距今 5 個交易日｜kind：realized
  - 來源：—（numbers.earnings_recency，as_of 2026-11-02）
- `f_peer_lite_gross_margin_pct`（q2_moat）｜LITE 毛利率＝45.91 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.LITE.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_lite_operating_margin_pct`（q2_moat）｜LITE 營業利益率＝23.35 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.LITE.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_cohr_gross_margin_pct`（q2_moat）｜COHR 毛利率＝38.16 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.COHR.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_cohr_operating_margin_pct`（q2_moat）｜COHR 營業利益率＝14.11 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.COHR.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_cien_operating_margin_pct`（q2_moat）｜CIEN 營業利益率＝14.12 %｜期間與口徑：TTM ending 2026-07-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CIEN.operating_margin_pct，as_of TTM ending 2026-07-31（4季加總））
- `f_peer_aaoi_gross_margin_pct`（q2_moat）｜AAOI 毛利率＝28.92 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.AAOI.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_mtsi_gross_margin_pct`（q2_moat）｜MTSI 毛利率＝57.13 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MTSI.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝24.83 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-11-07）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝39.01 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-11-07）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝54.41 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-11-07）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝6690.42 USD m｜期間與口徑：2026-11-08／yfinance revenue_estimate 0y 平均（21 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝10473.31 USD m｜期間與口徑：2026-11-08／yfinance revenue_estimate +1y 平均（22 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝14.85 %｜期間與口徑：2026-08-13 → 2026-11-07／FY1 共識 EPS 21.62 → 24.83（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-11-07）
- `f_kpi3_sbc_and_related_payroll_`（q4_capital）｜SBC and related payroll taxes＝146.7 USD million｜期間與口徑：Q1 FY2027（季末 2026-09-26，公告於 2026-11-02）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 investor.lumentum.com Q1 FY27 press release（含高管退休股權修改 $89.4M、薪資稅 $14.2M；占營收約 11.6%、占 GAAP 營業利益約 40.8%，為本檔換算）（numbers.latest_quarter_kpis.items[3]，as_of Q1 FY2027（季末 2026-09-26，公告於 2026-11-02））
  - 註記：n/a
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝-549.4 USD m｜期間與口徑：2026-11-08／yfinance 最新一季：總債務 1430.2、現金 1979.6（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝90.68 m shares｜期間與口徑：2026-11-08／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_ev_m`（q5_valuation）｜目前企業價值 EV（市值＋淨負債）＝48292.59 USD m｜期間與口徑：2026-11-08／市值 48841.99 ＋ 淨負債 -549.4｜kind：realized
  - 來源：—（numbers.capital_structure.ev_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝538.59 USD｜期間與口徑：2026-11-06（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-11-06（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝21.69 x｜期間與口徑：2026-11-07／分母＝FY1 EPS 24.83，分子＝快照價 538.59｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-11-07）
- `f_ps_current`（q5_valuation）｜P/S（現值）＝13.05 x｜期間與口徑：2026-11-06（RTH 收盤，UTC）／4 個年度端點內的分位＝68.7｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝68.7 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝12.9 x｜期間與口徑：2026-11-06（RTH 收盤，UTC）／4 個年度端點內的分位＝65.9｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝65.9 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ev_s_fwd`（q5_valuation）｜EV/S（EV ÷ FY1 共識營收）＝7.22 x｜期間與口徑：2026-11-08／f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）｜kind：estimate
  - 來源：—（numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝-40.41 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-11-06（RTH 收盤，UTC））
- `f_rsi14`（q5_valuation）｜RSI(14)＝29.51｜期間與口徑：2026-11-06（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ma_w52`（q5_valuation）｜52 週均線＝708.13 USD｜期間與口徑：2026-11-08／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）
- `f_ma_w104`（q5_valuation）｜104 週均線＝404.67 USD｜期間與口徑：2026-11-08／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）

### findings_digest 中方向為負或來源衝突的條目（22 條）
- `competitive_share_entrants#0`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K 風險因素：光通訊市場已成熟、日益商品化；既有對手與以亞洲為主的新進入者近年加劇競爭，造成價格壓力。
  - 來源：SEC EDGAR 10-K FY2026 Item 1A（as_of 2026-08-17）｜affects：moat_trend、decision_inputs.bear
- `competitive_share_entrants#1`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K 風險因素：競爭對手可能以新品或激進低價取得或保住份額，且公司自稱對手中許多資源較大；若供給跟不上需求，可能流失份額。
  - 來源：SEC EDGAR 10-K FY2026 Item 1A（as_of 2026-08-17）｜affects：moat_trend、thesis.R
- `competitive_share_entrants#4`（competitive_share_entrants｜方向 -｜狀態 ok）：HyperLight 薄膜鈮酸鋰調變器新進入者，威脅限於調變器而非 InP 雷射
  - 來源：marketanalysis.com（as_of 2026-06-19）｜affects：moat_trend、decision_inputs.bear
- `customer_second_source#0`（customer_second_source｜方向 -｜狀態 ok）：FY2026 10-K 風險因子：客戶的廠商選擇、採購行為變動曾導致對該等客戶銷售下滑或訂單延遲／取消，並可能持續；競爭者可能以低價策略搶市占。未見明確指出最大客戶導入第二供應商或自製的揭露。
  - 來源：SEC EDGAR 10-K FY2026 Item 1A（as_of 2026-08-17）｜affects：thesis.R、decision_inputs.bear
- `customer_second_source#1`（customer_second_source｜方向 -｜狀態 ok）：FY2026 10-K：兩大未具名客戶占營收 26.6% 與 15.0%（前一年 15.4%、16.0%）
  - 來源：SEC EDGAR 10-K FY2026（as_of 2026-08-17）｜affects：thesis.R
- `customer_concentration_credit#0`（customer_concentration_credit｜方向 -｜狀態 ok）：FY2026 10-K：單一終端客戶 Customer A 占營收 26.6%（FY2025 15.4%、FY2024 18.9%），Customer B 15.0%（FY2025 16.0%、FY2024 11.4%）；兩大客戶合計約 41.6%。
  - 來源：SEC EDGAR 10-K FY2026 Item 1（as_of 2026-08-17）｜affects：thesis.R、decision_inputs.bear
- `customer_concentration_credit#1`（customer_concentration_credit｜方向 -｜狀態 ok）：風險因子：公司長期依賴少數客戶，預期集中度持續；多數客戶以採購單下單、無數量或長期承諾，可能無預警改變採購。
  - 來源：SEC EDGAR 10-K FY2026 Item 1A（as_of 2026-08-17）｜affects：thesis.R、decision_inputs.bear
- `customer_concentration_credit#2`（customer_concentration_credit｜方向 -｜狀態 ok）：應收帳款集中：2026-06-27 兩家客戶分別占應收帳款毛額 30% 與 11%（前一年 13%、11%）。
  - 來源：SEC EDGAR 10-K FY2026 Item 8（as_of 2026-08-17）｜affects：thesis.R、decision_inputs.bear
- `regulatory_antitrust#0`（regulatory_antitrust｜方向 -｜狀態 ok）：公司 2024-08 收到 BIS 行政傳票與 DOJ 相關傳票，要求提供對華為業務的紀錄；公司持續配合，屬出口管制調查而非反壟斷；未履行出口管制可能面臨罰款、出口權限被拒與政府合約除名。
  - 來源：SEC EDGAR 10-K FY2026 Item 1A（as_of 2026-08-17）｜affects：thesis.R、decision_inputs.bear
- `regulatory_antitrust#1`（regulatory_antitrust｜方向 -｜狀態 ok）：10-K 風險因素揭露美國關稅、出口管制與制裁法規可能限制對中國等地區銷售並增加成本；232 條款半導體調查可能帶來新關稅。
  - 來源：SEC EDGAR 10-K FY2026 Item 1A（as_of 2026-08-17）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：因 BIS 對華為的出口限制，公司自 2024 年初起停止對華為（曾為中國最大網通客戶）的所有出貨
  - 來源：SEC EDGAR 10-K FY2026 Item 1A（as_of 2026-08-17）｜affects：decision_inputs.bear、thesis.R
- `reg_tariff_export#1`（reg_tariff_export｜方向 -｜狀態 ok）：中國對稀土及關鍵礦物實施出口管制，限制公司取得這些材料；中國對日本出口限制亦影響其基板供應鏈
  - 來源：SEC EDGAR 10-K FY2026 Item 1A（as_of 2026-08-17）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#2`（reg_tariff_export｜方向 -｜狀態 ok）：美國商務部 2025-04-14 依 232 條款啟動調查，可能對半導體等產品課新關稅，對公司影響不確定
  - 來源：SEC EDGAR 10-K FY2026 Item 1A（as_of 2026-08-17）｜affects：thesis.R、valuation
- `reg_tariff_export#3`（reg_tariff_export｜方向 -｜狀態 ok）：公司部分供應商位於中國，暴露於中美出口管制、關稅與報復措施風險
  - 來源：SEC EDGAR 10-K FY2026 Item 1A（as_of 2026-08-17）｜affects：thesis.R、moat_trend
- `reg_tariff_export#4`（reg_tariff_export｜方向 -｜狀態 ok）：關稅與出口管制可能推高銷貨成本，若無法轉嫁則壓縮毛利率
  - 來源：SEC EDGAR 10-K FY2026 Item 1 / MD&A（as_of 2026-08-17）｜affects：thesis.R、valuation
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：InP 供需缺口已超過 DRAM/NAND；Lumentum 雖有多座 InP 晶圓廠仍面臨供給短缺（2026 年 8 月報導）
  - 來源：TrendForce News: InP Shortage Emerges as AI Optical Interconnect Bottleneck（as_of 2026-08-06）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：FY2023 10-K：自有廠在美、泰、中、英、斯洛維尼亞、日，代工主要在泰、台、馬（搜尋摘要轉述，非逐字）
  - 來源：Lumentum FY2023 10-K（as_of 2023-08-15）｜affects：thesis.R
- `geo_supply_chain#2`（geo_supply_chain｜方向 -｜狀態 ok）：FY2022 10-K：製造集中亞洲，且 FY22 Q3 因疫情政府規定中國工廠暫時關閉（搜尋摘要轉述，非逐字）
  - 來源：Lumentum FY2022 10-K（as_of 2022-08-15）｜affects：thesis.R
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：FY2026 10-K 風險因子：市場技術變化快、新品頻繁推出；光通訊產品已成熟並日趨商品化，傳統對手與亞洲新進者加劇價格壓力，公司需持續開發差異化高階產品。
  - 來源：SEC EDGAR 10-K FY2026 Item 1A（as_of 2026-08-17）｜affects：moat_trend、decision_inputs.bear
- `substitute_technology#2`（substitute_technology｜方向 -｜狀態 ok）：Simply Wall St 敘事指出整合/矽光子對手與快速創新週期為風險（意見文，非公司揭露）。
  - 來源：Simply Wall St narrative: photonics risks and cloud consolidation will erode margins（as_of 2025-08-15）｜affects：moat_trend、decision_inputs.bear
- `major_events#1`（major_events｜方向 -｜狀態 ok）：BIS 與 DOJ 對 Lumentum 對華為出貨的傳票調查仍在進行，公司配合中、未見和解或處罰
  - 來源：SEC EDGAR 10-K FY2026 Item 1A（as_of 2026-08-17）｜affects：thesis.R、decision_inputs.bear
- `sec_investigation_restatement#0`（sec_investigation_restatement｜方向 -｜狀態 ok）：無 SEC 調查或重編；但有 BIS/DOJ 對華為出貨的出口管制調查（非 SEC），仍在進行
  - 來源：SEC EDGAR 10-K FY2026 Item 1A（as_of 2026-08-17）｜affects：thesis.R、decision_inputs.bear

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 10 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/LITE_20261108/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":1700,"bear_5y_price":360,"p_bull_pct":25,"p_bear_pct":30,"upside_5y_pct":57.8,"ev5y_pct":70.0,"irr_base_pct":9.6,"asym_ratio":5.4,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":24.83,"pe":21.69,"basis":"FY1（FY2027E，六月底年度）非 GAAP 共識 EPS，與終端倍數同為當年度前瞻口徑；全部為獨立口徑，未納入 Marvell 換股。"},"eps":{"bull":[26.5,44,64,77,85],"base":[24.8,38,46,45,50],"bear":[23.6,31,27,20,24]},"pe":{"bull":20,"base":17,"bear":15},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0,"net_buyback":0},"second_stage":{"bull_cagr_pct":12,"base_cagr_pct":8},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### LITE_Q3_2026_Earnings_Call_20260505.md
- 2026-05-05｜Wajid Ali｜guidance：CFO 給 FQ4 營收指引區間 9.6 億至 10.1 億美元（原話："in the range of $960 million to"）
- 2026-05-05｜Wajid Ali｜guidance：FQ4 非 GAAP 營業利益率指引 35%–36%，EPS 2.85–3.05 美元（原話："operating margin to be in the range of 35% to 36%"）
- 2026-05-05｜Wajid Ali｜guidance：FQ4 EPS 指引假設稅率 16.5%、稀釋股數約 1.02 億（原話："effective tax rate of 16.5%"）
- 2026-05-05｜Michael E. Hurlston｜guidance：CEO 說 FQ4 成長一半以上來自元件，其餘來自系統（高速收發器與 OCS）（原話："over half of the sequential growth will stem from"）
- 2026-05-05｜Michael E. Hurlston｜guidance：管理層稱有信心達成 OFC 活動所提的單季 20 億美元營收目標（原話："very much on track to reach our $2 billion quarterly"）
- 2026-05-05｜Michael E. Hurlston｜guidance：OCS 下半年可出貨約 4 億美元，並稱 2027 年該數字續升（原話："We've outlined this sort"）
- 2026-05-05｜Wajid Ali｜margin：非 GAAP 毛利率 47.9%，季增 540bp，並列出三項驅動因素（原話："better manufacturing utilization across the majority of our"）
- 2026-05-05｜Wajid Ali｜margin：非 GAAP 營業利益率 32.2%，季增 700bp，歸因於元件營收成長（原話："primarily driven by revenue growth in components products."）
- 2026-05-05｜Michael E. Hurlston｜margin：CEO 拆解毛利率改善：工廠吸收、砍低毛利產品線、漲價（原話："we made some"）
- 2026-05-05｜Michael E. Hurlston｜margin：CEO 承認收發器毛利率落後同業（原話："I think we are underperforming peers."）
- 2026-05-05｜Michael E. Hurlston｜margin：CEO 稱 1.6T 結構上毛利率優於 800G，預期收發器毛利率墊高（原話："1.6T is definitely better. Structurally from a margin"）
- 2026-05-05｜Michael E. Hurlston｜margin：FQ4 約 20% 模組將用自家 CW 雷射，並稱此為毛利導向（原話："it would be about 20% of our"）
- 2026-05-05｜Michael E. Hurlston｜margin：CEO 稱委外代工可提升毛利，早期階段（原話："we can actually improve our margins."）
- 2026-05-05｜Michael E. Hurlston｜margin：CEO 稱部分晶圓廠（含英國廠）仍未滿載，有利用率改善空間（原話："We've historically been underutilized."）
- 2026-05-05｜Michael E. Hurlston｜risk：收發器出貨遠低於客戶需求，受關鍵零組件供給限制（原話："supply constraints on critical components keep our shipments"）
- 2026-05-05｜Michael E. Hurlston｜risk：EML 供需缺口擴大為大於 30%，前次為 25–30%（原話："The supply-demand imbalance is probably even"）
- 2026-05-05｜Michael E. Hurlston｜risk：泵浦雷射限制為突發、先前幾季未提，缺口超過 30%，需取捨分配客戶（原話："It's hit us relatively suddenly."）
- 2026-05-05｜Michael E. Hurlston｜risk：OCS 是目前最大的執行風險，且 OCS 受供應鏈限制（原話："the biggest single tight rope that we're walking"）
- 2026-05-05｜Michael E. Hurlston｜risk：被問超額供給風險，CEO 認為低，理由是客戶仍在洽談延長長約（原話："I mean, I feel it's low."）
- 2026-05-05｜Michael E. Hurlston｜risk：雷射供給近期主要靠自己，但基板 2027 年仍需持續處理（原話："as we head into 2027, we're going to continue to"）
- 2026-05-05｜Michael E. Hurlston｜competition：CEO 稱 OCS 領先地位不會永遠，但未來一年難有人出貨類似方案（原話："That's not going to last forever, right? We know that."）
- 2026-05-05｜Michael E. Hurlston｜competition：CEO 稱正在降成本、簡化 OCS 以因應中國競爭者的創新方案（原話："We are working on cost reducing."）
- 2026-05-05｜Michael E. Hurlston｜competition：稱有定價彈性，供需失衡短期不會解決（原話："We definitely have some pricing"）
- 2026-05-05｜Michael E. Hurlston｜product：本次法說新增強調 scale-across 產品組合對毛利率的貢獻（原話："it is important to outline the considerable role"）
- 2026-05-05｜Michael E. Hurlston｜product：元件營收 5.33 億、季增 20%；窄線寬雷射出貨年增逾 120%、泵浦雷射年增 80%（原話："while pump laser shipments grew 80% year-over-year."）
- 2026-05-05｜Michael E. Hurlston｜product：雲端收發器季增逾 40%，1.6T 預計 FQ4 放量（原話："we are poised to ramp 1.6T speed transceiver shipments"）
- 2026-05-05｜Michael E. Hurlston｜product：CEO 稱 scale-up CPO 仍在初期，是最大單一成長動能，scale-out CPO 與 OCS 貢獻仍小（原話："scale-up CPO is still very much in its infancy."）
- 2026-05-05｜Michael E. Hurlston｜product：自家 CW 雷射供貨時程改口：原訂日曆 Q2 導入後退後，現因外部 CW 供應吃緊而加速（原話："we backed off just seeing so much tension on the EML line."）
- 2026-05-05｜Michael E. Hurlston｜product：Q3 超高功率雷射(CPO)季增，預計 12 月季產生有意義營收，並履行 2027 上半年數億美元訂單（原話："fulfill the multihundred million dollar purchase order"）
- 2026-05-05｜Michael E. Hurlston｜product：CEO 稱 ELS 垂直整合是非主要客戶的切入點，比單供雷射更短的上市路徑（原話："a more convincing and shorter path to"）
- 2026-05-05｜Michael E. Hurlston｜customer：OCS 仍與三家客戶合作，其中兩家占大部分量體；更多訂單尚未能公布（原話："Two of"）
- 2026-05-05｜Michael E. Hurlston｜customer：CEO 稱 Google 是最大客戶之一，並驅動大量需求（原話："They're certainly one"）
- 2026-05-05｜Michael E. Hurlston｜customer：CEO 稱 v7 與 v8 的 OCS 拉貨差異小、屬增量（原話："It's incremental. It's not that big"）
- 2026-05-05｜Wajid Ali｜capital_allocation：Q3 資本支出 1.25 億美元，聚焦雲端與 AI 產能（原話："In Q3, we spent $125 million in CapEx"）
- 2026-05-05｜Wajid Ali｜capital_allocation：現金及短期投資增至 31.7 億，主因 NVIDIA 直接投資（原話："primarily driven by NVIDIA's direct investment in Lumentum."）
- 2026-05-05｜Michael E. Hurlston｜capital_allocation：購入第五座磷化銦廠（北卡 Greensboro）（原話："we expect to take advantage of a significant number"）
- 2026-05-05｜Michael E. Hurlston｜capital_allocation：Greensboro 產能不在現有數字內，2028 年才上線，約 6 季後才有顯著貢獻（原話："the Greensboro fab is not going to come online until 2028."）
- 2026-05-05｜Michael E. Hurlston｜capital_allocation：泵浦雷射 CapEx 與客戶討論預付款、照付不議或漲價分擔（原話："That can entail prepayment, that can"）
- 2026-05-05｜Michael E. Hurlston｜commitment：承諾 2026 年 12 月季 EML 單位數較去年同期成長逾 50%（原話："on track to achieve more than 50% growth in EML"）
- 2026-05-05｜Michael E. Hurlston｜commitment：正爭取長期協議以抵銷預期資本支出（原話："we are actively working to"）
- 2026-05-05｜Michael E. Hurlston｜commitment：泵浦雷射計畫未來四季在美國 Rose Orchard 廠擴產（原話："We have a plan to ramp capacity"）
- 2026-05-05｜Michael E. Hurlston｜commitment：CEO 對長期毛利率目標表示很有信心，且認為還有上升空間（原話："We feel very comfortable with that."）
- 2026-05-05｜Michael E. Hurlston｜commitment：CEO 稱 scale-up CPO 若執行得當可增加逾 50 億美元增量營收（原話："somewhere greater than $5 billion of incremental revenue"）

### LITE_Deutsche_Bank_2026_Technology_Conference_20260827.md
- 2026-08-27｜CEO Michael Hurlston｜guidance：CEO 表示公司提出新的 2028 財年每股盈餘能力目標 $40。（原話："in 2028, we figured that we can now deliver $40 of earnings power"）
- 2026-08-27｜CEO Michael Hurlston｜customer：CEO 稱最大客戶自上次財報後大幅增加 OCS 訂單。（原話："huge uptick in our order book and the order rate"）
- 2026-08-27｜CEO Michael Hurlston｜product：CEO 認為先前公布的 OCS 80 億美元 TAM 被低估。（原話："the TAM now looks like it's significantly undercalled"）
- 2026-08-27｜CEO Michael Hurlston｜customer：CEO 承認目前 OCS 主要綁定單一客戶。（原話："we're predominantly today, I'd say, tied to one customer"）
- 2026-08-27｜CEO Michael Hurlston｜product：CEO 稱 CPO 與 NPO 對光學產業是加成而非互相取代。（原話："completely additive to the numbers that we see today"）
- 2026-08-27｜CEO Michael Hurlston｜product：CEO 稱 CPO／NPO 目前尚未反映在公司營收數字中。（原話："nothing is showing up in our number"）
- 2026-08-27｜CEO Michael Hurlston｜margin：CEO 稱 scale across 業務毛利率高且成長快但較少人討論。（原話："Our scale across business is quite high margin."）
- 2026-08-27｜CEO Michael Hurlston｜margin：CEO 說明 EML 由 100G 升到 200G 的價格倍數。（原話："you're seeing about a 2x uplift in price"）
- 2026-08-27｜CEO Michael Hurlston｜competition：CEO 稱 200G EML 目前競爭少、近期也無新進者。（原話："We don't see a lot of competitive threats on the horizon either"）
- 2026-08-27｜CEO Michael Hurlston｜product：CEO 預期 1.6T 時 EML 型收發器占比降至市場的 40%～50%（800G 約 70%～80%），絕對數量仍增加。（原話："40% to 50% of the market at 1.6T"）
- 2026-08-27｜CEO Michael Hurlston｜competition：CEO 稱目前未見中國雷射供給造成影響。（原話："we see no impact from any Chinese laser supply"）
- 2026-08-27｜CEO Michael Hurlston｜competition：CEO 認為中國雷射業者趕上所需時間比外界認為的長。（原話："I think it's going to take longer than people think."）
- 2026-08-27｜CEO Michael Hurlston｜product：CEO 稱 NPO 機會近期比 CPO 更大。（原話："actually larger than the CPO opportunity, at least in the near term"）
- 2026-08-27｜CEO Michael Hurlston｜capital_allocation：CEO 說明 Greensboro 晶圓廠於 2026 初收購、2028 初才投產。（原話："it's not operational until early calendar 2028"）
- 2026-08-27｜CEO Michael Hurlston｜commitment：CEO 表示新增產能投資前需看到類似 NVIDIA 的客戶承諾。（原話："I would definitely need to see a similar type of commitment"）
- 2026-08-27｜CEO Michael Hurlston｜product：CEO 稱 NPO 放量時點由原先預期的 2028 底／2029 初提前。（原話："it's a late 2027 into early 2028 event"）
- 2026-08-27｜CEO Michael Hurlston｜risk：CEO 稱 NPO 需求將對 Greensboro 晶圓廠產能造成壓力。（原話："it's going to put a lot of pressure, a lot of pressure on that Greensboro fab"）
- 2026-08-27｜CEO Michael Hurlston｜risk：CEO 稱產能最大限制是時間（認證週期長）。（原話："the headline is just time"）
- 2026-08-27｜CEO Michael Hurlston｜risk：CEO 稱基板供給緊，已在日本供應商之外再與 AXT 簽約。（原話："we went out and did another deal with AXTI"）
- 2026-08-27｜CEO Michael Hurlston｜customer：CEO 說明在 NVIDIA 的產品認證耗時一年。（原話："it was a year cycle for us to get qualified at NVIDIA"）
- 2026-08-27｜CEO Michael Hurlston｜product：CEO 稱系統（模組）業務單季營收規模。（原話："running well over $200 million a quarter in that business"）
- 2026-08-27｜CEO Michael Hurlston｜margin：CEO 承認模組業務毛利率尚未改善。（原話："We've yet to fix the gross margin."）
- 2026-08-27｜CEO Michael Hurlston｜margin：CEO 承認模組毛利表現不及頂尖競爭者。（原話："We don't perform as well as the top competitors."）
- 2026-08-27｜CEO Michael Hurlston｜commitment：CEO 稱 2027 年起將著手改善製造以提升毛利。（原話："how do we fix the manufacturing?"）
- 2026-08-27｜CEO Michael Hurlston｜risk：CEO 回顧 Cloud Light 過去的品質問題。（原話："a lot of quality problems coming out of Cloud Light"）
- 2026-08-27｜CEO Michael Hurlston｜competition：CEO 不視異質整合為威脅。（原話："I don't see it as a threat"）
- 2026-08-27｜CEO Michael Hurlston｜risk：CEO 稱公司被視為美國禁中國收發器的淨受益者。（原話："We are viewed, probably correctly so as a net beneficiary"）
- 2026-08-27｜CEO Michael Hurlston｜risk：CEO 指出中國收發器廠商在美國市場的占比。（原話："make 70% of the transceivers in the U.S. market"）
- 2026-08-27｜CEO Michael Hurlston｜product：CEO 指出未來 12～18 個月要觀察的重點是 scale-in（託盤內光互連）。（原話："that's the thing to watch over the next 12 to 18 months"）

### LITE_Citi_s_2026_Global_TMT_Conference_20260909.md
- 2026-09-09｜Kathryn Ta (CFO/管理層)｜guidance：CFO 說因 OCS 能見度提高，首度提出 FY28 EPS $40 指引（原話："putting out a fiscal year '28 guidance on EPS of $40"）
- 2026-09-09｜Kathryn Ta (CFO/管理層)｜customer：OCS 上行來自最大客戶，原因是需出貨更多單位（原話："that OCS upside is coming from our largest customer"）
- 2026-09-09｜Kathryn Ta (CFO/管理層)｜guidance：FY28 $40 EPS 涵蓋所有季度，OCS 貢獻隨季度線性疊加（原話："layering in linearly and increasing as we move through"）
- 2026-09-09｜Kathryn Ta (CFO/管理層)｜commitment：CFO 表示對達成 $40 有信心，並指出賣方模型（含主持人）EPS 較低（原話："we have all the confidence that we'll be able to meet"）
- 2026-09-09｜Kathryn Ta (CFO/管理層)｜guidance：被問 $40 隱含的毛利率等，CFO 不拆解，僅提及賣方模型偏低（原話："I'm hesitating to say that because we did see the sell-side"）
- 2026-09-09｜Wupen Yuen (President, Global BUs)｜risk：管理層稱供需缺口仍在擴大，雷射、EML、CPO 雷射皆短缺，2027 不會緩解（原話："we don't see the shortage going away in '27"）
- 2026-09-09｜Wupen Yuen (President, Global BUs)｜margin：管理層稱新交易定價等於或高於先前已上調的價格，並依價格與加急費分配產能（原話："All the deals we're making today are equal or higher pricing"）
- 2026-09-09｜Wupen Yuen (President, Global BUs)｜product：CPO 時程不變但需求量提高，先用於 scale-out 交換器，2027 下半年用於 scale-up（原話："No change in timing, but intensity is actually increasing"）
- 2026-09-09｜Wupen Yuen (President, Global BUs)｜product：對 scale-up 市場的看法改變：由單一客戶故事變成全產業，CPO 與 NPO 約各半（原話："CPO will be half of the market. NPO is the other half"）
- 2026-09-09｜Wupen Yuen (President, Global BUs)｜product：管理層稱 NPO 是機會的淨增加（先前只想到 CPO）（原話："the NPO is a net addition to our opportunity"）
- 2026-09-09｜Wupen Yuen (President, Global BUs)｜competition：高功率雷射只看到 Coherent 一家競爭者（NVIDIA 也與其簽 LTA）（原話："We see one competitor, right, who is Coherent"）
- 2026-09-09｜Wupen Yuen (President, Global BUs)｜competition：管理層稱中國 CW 雷射供應主要針對可插拔市場，NPO/CPO 需 120-150mW 以上高功率（原話："targeted today to serve the pluggable market"）
- 2026-09-09｜Wupen Yuen (President, Global BUs)｜capital_allocation：UHP 雷射三波擴產：San Jose、英國 2Q27 起、Greensboro 2Q28 或 mid-28 起（原話："We will start to ramp in second quarter 2028 or mid-'28"）
- 2026-09-09｜Wupen Yuen (President, Global BUs)｜risk：擴產時程最大變數為客戶認證（PCN）時間（原話："change the schedule is the qualification timing"）
- 2026-09-09｜Wupen Yuen (President, Global BUs)｜capital_allocation：新產能採新增而非取代現有產品線，含 6 吋產能（原話："So by and large, we don't sacrifice, we add."）
- 2026-09-09｜Kathryn Ta (CFO/管理層)｜product：首個 ELS 勝利來自現有 CPO 客戶，預計 2027 下半年出貨，估計取得其 15-20% 份額（原話："maybe 15% to 20% of their fleet is about the right amount"）
- 2026-09-09｜Kathryn Ta (CFO/管理層)｜commitment：CFO 預告未來數個月內可能公布首位 NPO 客戶，目前尚無 NPO 勝利公告（原話："we can expect to see something in the next handful"）
- 2026-09-09｜Wupen Yuen (President, Global BUs)｜product：1.6T/200G 每通道已超過 EML 出貨組合 25%，100G EML 仍為主力（原話："we exceed 25% of the mix"）
- 2026-09-09｜Wupen Yuen (President, Global BUs)｜competition：EML 未見中國新進入者作為合約競爭者，EML 定價維持有利（原話："our EML pricing remains very favorable"）
- 2026-09-09｜Wupen Yuen (President, Global BUs)｜competition：管理層認為 400G/lane 時 InP 有機會重拿 100G 世代的份額，矽光與薄膜鈮酸鋰各有限制（原話："indium phosphide has a good chance of regaining the share"）
- 2026-09-09｜Wupen Yuen (President, Global BUs)｜margin：CW 雷射良率已高於 EML、價格相近，毛利輪廓不及 EML 但接近（原話："our laser yield has climbed up to be higher than EMLs"）
- 2026-09-09｜Kathryn Ta (CFO/管理層)｜product：OCS 每顆 XPU 搭載率仍約 1.5:1，新拓撲互有增減後大致持平（原話："it still ends up roughly 1.5:1"）
- 2026-09-09｜Kathryn Ta (CFO/管理層)｜product：OCS 先前 $8B TAM 估計看到上行（動態叢集、容錯網路應用），約 2028 底至 2029 初可見（原話："So that probably puts upside to that $8 billion number."）
- 2026-09-09｜Wupen Yuen (President, Global BUs)｜competition：Coherent 追上高功率雷射的時程管理層表示不知道，稱客戶需要第二來源（原話："We frankly don't know, right?"）
- 2026-09-09｜Kathryn Ta (CFO/管理層)｜customer：scale-across 帶動泵浦雷射，預期未來約 5 季量增 4 倍，並與主要網通設備商簽多年 LTA 且價格較高（原話："a 4x multiplier on our volume of pump lasers"）
- 2026-09-09｜Wupen Yuen (President, Global BUs)｜commitment：管理層聲稱公司定位將涵蓋 scale across 到 scale in（原話："Lumentum's best days are yet to come"）

### LITE_Lumentum_Holdings_Inc_Marvell_Technology_Inc_M_A_Call_20261102.md
- 2026-11-02｜CEO (Marvell, Matthew Murphy)｜capital_allocation：Marvell 宣布與 Lumentum 合併（收購），Lumentum CEO 與另兩位董事將在交割後進入 Marvell 董事會（原話："Michael and 2 other members of the Lumentum Board will join"）
- 2026-11-02｜CEO (Marvell, Matthew Murphy)｜guidance：合併後 2030 年合計 TAM 估 5500 億美元，增量主要來自 NPO 與 CPO（原話："a combined TAM of $550 billion in 2030"）
- 2026-11-02｜CEO (Lumentum, Michael Hurlston)｜customer：Lumentum CEO 宣布第二個大型 NPO／CPO 訂單，預期帶來逾 50 億美元營收（原話："our second major NPO and CPO win"）
- 2026-11-02｜CEO (Lumentum, Michael Hurlston)｜competition：Lumentum CEO 說明考慮過獨立發展與自行收購等替代方案後選擇與 Marvell 合併（原話："continuing to execute as a stand-alone company"）
- 2026-11-02｜CEO (Lumentum, Michael Hurlston)｜product：Lumentum CEO 描述銅牆外移，scale-up 光學頻寬比 scale-out 再高 10 倍（原話："optics which carry another 10x increase in bandwidth"）
- 2026-11-02｜CEO (Lumentum, Michael Hurlston)｜commitment：雙方承諾維持既有 go-to-market 模式，繼續供應元件與系統給整個生態系（原話："we plan to maintain our existing go-to-market model"）
- 2026-11-02｜CEO (Marvell, Matthew Murphy)｜product：Lumentum 的 MEMS 光路交換器（OCS）被客戶越來越多採用，與網路交換器預期並存（原話："optical circuit switching are expected to coexist"）
- 2026-11-02｜CEO (Marvell, Matthew Murphy)｜capital_allocation：Marvell 說將與供應鏈夥伴投入數十億美元確保產能（原話："investing multiple billions of dollars"）
- 2026-11-02｜CEO (Lumentum, Michael Hurlston)｜capital_allocation：Lumentum 稱磷化銦晶圓廠為皇冠上的寶石，正積極擴產（原話："we are investing aggressively to expand our capacity"）
- 2026-11-02｜CFO (Marvell, Daniel Durn)｜guidance：CFO 預期交易使非 GAAP 毛利率與營業利益率增益，含逾 10 億美元年化協同效益，主要來自 COGS（原話："run rate synergies we primarily see from COGS"）
- 2026-11-02｜CFO (Marvell, Daniel Durn)｜guidance：CFO 預期交易於交割後第 1 年起對非 GAAP EPS 增益（原話："accretive to non-GAAP EPS starting in year 1 post close"）
- 2026-11-02｜CEO (Marvell, Matthew Murphy)｜margin：CEO 引用備考數字：年化營收 177 億美元、非 GAAP 營業利益率 39%（依 Marvell 當季指引與 Lumentum 當日財報）（原話："$17.7 billion in annualized revenue"）
- 2026-11-02｜CEO (Marvell, Matthew Murphy)｜guidance：合併 Lumentum 下一財季指引與 Marvell 共識，備考年化營收逾 210 億美元、營業利益率低 40% 區間（原話："pro forma annualized revenue of over $21 billion"）
- 2026-11-02｜CEO (Marvell, Matthew Murphy)｜guidance：增量 TAM 約 600 億美元，近期協同一部分反映在 COGS，另有營收協同（原話："incremental of $60 billion"）
- 2026-11-02｜CEO (Marvell, Matthew Murphy)｜customer：管理層稱關鍵客戶在交易傳出後與週末皆表達強力支持（原話："there's just tremendous support for the combination"）
- 2026-11-02｜CEO (Lumentum, Michael Hurlston)｜competition：Lumentum 雷射供應給幾乎所有（競爭）模組廠，生態系為 co-opetition（原話："we supply our lasers to almost all of our competitors"）
- 2026-11-02｜CEO (Marvell, Matthew Murphy)｜commitment：Marvell 稱元件供應策略不變，首要任務仍是 DSP 等領先與供應雷射（原話："That strategy is not going to change."）
- 2026-11-02｜CEO (Marvell, Matthew Murphy)｜risk：分析師問及雷射供需；Marvell 稱供給吃緊非此時交易的原因，磷化銦與記憶體同屬供給受限（原話："tight supply is not the reason we're wanting to enter"）
- 2026-11-02｜CEO (Marvell, Matthew Murphy)｜risk：Marvell CEO 承認 Marvell 自身亦有供給短缺，並稱 Lumentum 情況無不同（原話："Marvell's got supply shortages. I mean we're behind."）
- 2026-11-02｜CEO (Lumentum, Michael Hurlston)｜guidance：Lumentum CEO 稱去年營收翻倍，多數人預期明年再翻倍，管理層未見改變（原話："Most people have us doubling again next year"）
- 2026-11-02｜CEO (Lumentum, Michael Hurlston)｜capital_allocation：Lumentum CEO 說明出售動機：放棄控制權，因認為合併 #1 優於收購多家 #2～#4（原話："why would we go out and buy a string of pearls"）
- 2026-11-02｜CFO (Marvell, Daniel Durn)｜guidance：CFO 稱 Analyst Day 的獨立目標（800 億美元營收）仍成立，本交易為增量（原話："everything we put forward at the Analyst Day"）
- 2026-11-02｜CEO (Marvell, Matthew Murphy)｜product：Marvell 稱增量 TAM 多在 scale-up，後期在 scale-in，結合 Lumentum micro-VCSEL 與 Marvell EIC（原話："best-in-class micro-VCSEL technology"）

### 問答異常語氣（迴避／改口／保留）
- LITE_Q3_2026_Earnings_Call_20260505.md｜問：Michael Mani：若滿足所有需求，收發器可有多大；缺口相對 30%？｜答法：未給收發器缺口數字，稱「沒算過」，僅說在同一量級(ZIP code)；並澄清 30% 僅指 EML
- LITE_Q3_2026_Earnings_Call_20260505.md｜問：Ryan Koontz：scale-across 市場規模、多軌放大機會多大？｜答法：兩位主管均未量化，稱「之後適當時機再給」，僅用 huge、significant 形容
- LITE_Q3_2026_Earnings_Call_20260505.md｜問：Sahej Singh：毛利率 waterfall 拆解(mix/CapEx/量價)｜答法：未給各因素占比，只列舉 mix、利用率、價格，並重申長期目標「很有信心」
- LITE_Q3_2026_Earnings_Call_20260505.md｜問：Samik Chatterjee：OCS 新增訂單進度與規模｜答法：稱「too early to call」不給時程，僅說規模 quite sizable
- LITE_Q3_2026_Earnings_Call_20260505.md｜問：Vijay Rakesh：Google v8 對 OCS 2027–28 的影響｜答法：拒評特定客戶與架構，僅說 v7→v8 拉貨差異屬增量
- LITE_Citi_s_2026_Global_TMT_Conference_20260909.md｜問：FY28 $40 EPS 隱含的毛利率或其他損益項目為何？｜答法：未提供任何隱含數字，改談賣方模型偏低與對 $40 的信心
- LITE_Citi_s_2026_Global_TMT_Conference_20260909.md｜問：Coherent 追上高功率雷射需要 12 或 18 個月？｜答法：不給時程，稱不知道，改談客戶需要第二來源
- LITE_Lumentum_Holdings_Inc_Marvell_Technology_Inc_M_A_Call_20261102.md｜問：Tom O'Malley（Barclays）請 CFO 給出 10 億美元協同中 COGS 占比（90%？95%？）及主要來源拆解｜答法：CFO 未給百分比或分項金額，改談結合後營收規模、毛利率與長期可擴大協同
- LITE_Lumentum_Holdings_Inc_Marvell_Technology_Inc_M_A_Call_20261102.md｜問：Tore Svanberg（Stifel）問 Analyst Day 的互連營收成長（60–70%、375 億美元）在合併後如何調整｜答法：Murphy 稱「our numbers, we haven't provided them」，未給更新數字，只說仍在軌道上、TAM 更大
- LITE_Lumentum_Holdings_Inc_Marvell_Technology_Inc_M_A_Call_20261102.md｜問：Vivek Arya（BofA）問是否競價流程、是否可能有其他出價者，以及是否買在短缺高峰（隱含約 1 倍 2030 TAM）｜答法：兩位管理層均未回答是否有競爭出價者；估值問題以供需、設計定案與資料可見度回應，未談價格倍數

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 5 | 2 |
| customer_second_source | found | 2 | 2 |
| customer_concentration_credit | found | 4 | 1 |
| supply_demand_durability | found | 4 | 2 |
| regulatory_antitrust | found | 3 | 3 |
| reg_tariff_export | found | 5 | 0 |
| geo_supply_chain | found | 3 | 2 |
| end_markets | found | 3 | 2 |
| substitute_technology | found | 3 | 2 |
| channel_business_model_shift | found | 1 | 2 |
| capital_markets_pricing | found | 6 | 4 |
| major_events | found | 3 | 4 |

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260812","verdict":"觀望","role":"候選/追蹤池","H":{"status":"ok","format":"table","rows":[{"id":"H1（2Y）","text":"200G/lane EML 供需缺口持續，LITE 為唯一量產供應商，GM 維持 40%+以上","columns":{"驗證指標":"季度 GM 軌跡","2026-06-27→2026-08-12 邊際變化":"🟢 強化：GM 44.2%→50.4%，超越假設上緣"}},{"id":"H2（2Y）","text":"FY27 EPS 較 FY26 成長 &gt;100%","columns":{"驗證指標":"共識 FY27 EPS","2026-06-27→2026-08-12 邊際變化":"🟢 強化：共識 $18.13→$18.73，且 Q1 guide 中值 $4.20 遠超共識 $3.63，年化路徑上修"}},{"id":"H3（5Y）","text":"OCS/CPO 第二引擎能撐起 EML 缺貨紅利消退後的估值","columns":{"驗證指標":"OCS營收guide兌現率、CPO 首批出貨時程","2026-06-27→2026-08-12 邊際變化":"🟢 強化：Q1FY27 guide已內含首個三位數（$100M+）營收季（原判仍待驗證的「一整季軌跡」已提前在guide中出現），OCS出貨量Q3→Q4已翻倍，管理層預期2027年初超車成該大客戶OCS第一供應商；仍待實際兌現驗證"}}]},"R":{"status":"unavailable"},"single_thing":null,"kill_metrics":null,"rearm_trigger":"Fwd PE(FY27基礎，隨最新共識滾動重算)回落至≤32x或5Y分位<70%；或GM連續4季維持>48%；生意面前提：COHR 200G/lane EML於任一top hyperscaler/NVIDIA完成客戶認證前，估值觸發不因股價波動單獨視為安全邊際打開","irr_base_pct":7.5,"ev5y_pct":39.0,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"候選/追蹤池","signal":"B","val":"🔴","ma":"✅","trap":"🟡","moat_trend":"→","runway_post_y5":"🟡","asym_ratio":2.3,"ev5y_pct":39.0,"irr_base_pct":7.5,"max_dd_pct":-58.0,"bull_5y_price":1948.8,"bear_5y_price":411.9,"p_bull_pct":25.0,"p_bear_pct":30.0,"rearm_trigger":"Fwd PE(FY27基礎，隨最新共識滾動重算)回落至≤32x或5Y分位<70%；或GM連續4季維持>48%；生意面前提：COHR 200G/lane EML於任一top hyperscaler/NVIDIA完成客戶認證前，估值觸發不因股價波動單獨視為安全邊際打開","price_at_dd":820.59,"archetype":"品質複利成長","cycle_position":"晚循環/過熱頂部"}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"LITE","date":"2026-11-08","schema":"v15.0","contract":"v19","company_name":"Lumentum Holdings Inc."},"oneliner":"Lumentum 已同意以全股票併入 Marvell。股價 538.59 美元對 FY2027E 為 21.7 倍，獨立看不貴，但股東最後收到的是 Marvell 股票；換股條款與 Marvell 端價值驗證前先等，不因超賣進場。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/LITE_20261108/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/LITE_20261108/scenario.json","answers":{"q1_business":{"verdict":"Lumentum 賺的是雲端與 AI 客戶擴建光互連的錢，利潤卡在磷化銦雷射晶片這一節點。","reasoning":"Q1 FY2027 營收 12.63 億美元，GAAP 毛利率 51.0%，GAAP 營益率 28.5%，非 GAAP 營益率 42.3%；Q2 指引營收 15.75–16.25 億美元、非 GAAP 營益率 45–46%。最新可得的分部拆分是 Q4 FY2026：元件 6.49 億美元占 64.5%，系統 3.57 億美元占 35.5%（2026-08-11 CFO）。Q1 FY2027 的完整法說與分部數字不在本包，事實表未涵蓋。成長同時來自量（泵浦雷射出貨年增逾 80%、窄線寬雷射年增逾 130%）、價（新約價格不低於先前已調高的價格，2026-09-09 Wupen Yuen）與產品組合（200G EML 單價約 100G 的兩倍，2026-08-27 CEO）。單點依賴屬集中度風險：前兩大客戶占 FY2026 營收 41.6%，多數客戶用採購單下單，沒有數量承諾。供需判斷：2027 年前屬結構性缺貨，2028 年起供給可逆性升高。產業態勢裁定為雙向拉鋸：光互連滲透銅線使結構轉好，中國磷化銦新廠與 Coherent 第二來源使競爭惡化，其他變數以合併案與出口管制最大。","fact_refs":["f_kpi0_net_revenue_gaap","f_kpi5_gaap_gross_margin","f_kpi2_gaap_operating_income_ma","f_kpi1_non_gaap_operating_incom","f_kpi4_guidance_q2_fy2027","f_earnings_recency"],"verdict_values":{"revenue_quality":"營收屬元件與系統的逐筆出貨，能見度靠長約：泵浦雷射多為三年期且多數照付不議（2026-08-11 CEO），EML 產能到 2027 年已認購；其餘客戶以採購單為主，10-K 明說可能無預警改變採購。","unit_econ_note":"雷射毛利高於公司平均，EML 仍高於 CW 但差距已縮小；ELS 模組單價高、毛利略低；收發器毛利落後頂尖同業，執行長 2026-08-27 承認尚未修好。","archetype":{"primary":"循環/商品","secondary":"轉機/特殊情境","confidence":"中","fingerprint":"FY2024 營收年減 23.08%、毛利率 18.5%、營益率 −26.59%，FY2027 起靠缺貨定價把 GAAP 毛利率推到 51%；2026-11-01 簽全股票併購，成為待交割標的。"},"industry":{"clock_phase":"III","sd_verdict_source":"依據為供需與定價，不看股價：漲價、長約、擴產競賽同時出現，訂單仍在上修。2027 年前結構性缺貨（2026-09-09 管理層稱缺口不會緩解），2028 年起反轉風險升高（TrendForce 估 2026 年 EML＋CW-DFB 月產能約倍增至 5,070 萬顆，Greensboro 2028 年開出）。","bargaining":{"up":"基板吃緊，靠日本供應商的領先安排加上 AXT 新約，管理層說需求若續增還要再找貨源。","down":"前兩大客戶占 41.6%。短期缺貨讓公司握有定價權，長期買方有能力扶植第二來源，NVIDIA 已同時資助 LITE 與 Coherent。","geo":"磷化銦廠在日本兩座，美國 Greensboro 2028 年開出；泵浦在 Rose Orchard 擴產並於泰國封測；部分供應商在中國。"},"profit_pool_dir":"利潤向雷射晶片集中：LITE 過去 12 個月毛利率 45.91%，高於 Coherent 38.16% 與 AAOI 28.92%；五年前後的營業利益池占比事實表未涵蓋。","tam_table":[{"item":"OCS 可服務市場（管理層）","value":"先前估 80 億美元，2026-08-27 CEO 稱被低估"},{"item":"scale-up CPO 增量營收（管理層）","value":"2026-05-05 CEO 估逾 50 億美元；2026-11-02 再宣布第二個大型 NPO／CPO 訂單，預期逾 50 億美元"},{"item":"合併後 2030 年 TAM（Marvell 自述）","value":"5,500 億美元，其中增量約 600 億美元"},{"item":"滲透率與營業利益池占比","value":"事實表未涵蓋"}]}}},"q2_moat":{"verdict":"護城河方向判為穩定：製程與產能領先還在，但定價優勢有一大部分來自缺貨，客戶已在扶植第二來源。","reasoning":"機制是磷化銦雷射的製程經驗、規格一致性帶來的客戶良率，加上約一年的認證週期（2026-08-27 CEO，NVIDIA 認證耗時一年）。方向用利潤率對照代替 ROIC：過去 12 個月 LITE 營益率 23.35%，Coherent 14.11%，差距為正；事實表沒有同業 ROIC 與投入資本，無法驗證差距是否擴大。EML 與泵浦各約 70–80% 的份額都是管理層自述，TrendForce 的口徑是前三大合計約 72%。這項判斷會錯的情況：Coherent 遲遲過不了認證，定價面就該上調；反過來，Coherent 通過 NVIDIA 或前三大雲端認證，定價面就該下調。當期報酬、持續期與新增資本報酬分開看：當期利益率高；持續期四項檢查兩綠兩黃；新增資本報酬因缺投入資本無法計算。","fact_refs":["f_peer_lite_gross_margin_pct","f_peer_lite_operating_margin_pct","f_peer_cohr_gross_margin_pct","f_peer_cohr_operating_margin_pct","f_peer_cien_operating_margin_pct","f_peer_aaoi_gross_margin_pct","f_peer_mtsi_gross_margin_pct"],"verdict_values":{"moat":{"mechanism":"磷化銦雷射製程經驗與規格一致性帶來客戶良率優勢，加上約一年的認證週期與長約綁定的產能。","execution":8,"pricing":8,"grade":"B","trend":"→","trend_evidence":"執行面擴大：毛利率在季營收 10 億美元就過 50%，原目標是 20 億美元；EPS 連兩季高於指引上緣。定價面穩定：新約價格不低於舊約，但來源是缺貨，1.6T 世代矽光加 CW 分走 EML 占比，由 800G 的 70–80% 降到 40–50%，Coherent 也拿到 NVIDIA 長約。兩者合計判穩定。","competitor_notes":[{"name":"COHR","strategy_note":"超高功率雷射目前唯一被管理層點名的對手，NVIDIA 同時與其簽長約，最可能成為第二來源；獲利與現金流都落後 LITE，擴產壓力較大。"},{"name":"CIEN","strategy_note":"網通設備商，不是雷射晶片的直接對手，對照價值在系統層的毛利與現金流。"},{"name":"AAOI","strategy_note":"模組與雷射的擴產者，仍在虧損且現金燒得快，短期構不成定價威脅。"},{"name":"MTSI","strategy_note":"類比與光電元件廠，毛利率高於 LITE，但營益率較低，是規模較小的元件對照，不是直接替代來源。"}],"peer_na_reason":"同業 ROIC 與投入資本事實表未涵蓋，方向改用毛利率與營益率對照。","threats":[{"level":"🔴","text":"客戶扶植第二來源，加上併入 Marvell 後供應中立性受質疑：雷射賣給幾乎所有模組對手（2026-11-02 CEO），NVIDIA 同時資助 Coherent，最大客戶的 OCS 仍保留自製。","p":"35%","evidence_refs":["customer_second_source#0","customer_second_source#1","competitive_share_entrants#1"]},{"level":"🟡","text":"亞洲低價新進者與中國磷化銦新廠，先打可插拔 CW 雷射；管理層稱至今未見影響，但 10-K 已寫出價格壓力。","p":"30%","evidence_refs":["competitive_share_entrants#0","substitute_technology#0"]},{"level":"🟡","text":"矽光加 CW 在 1.6T 分走 EML 占比；LITE 也賣 CW，損失主要落在毛利差與 EML 稀缺性。3.2T 時 EML 能否回來只有管理層說法。","p":"40%","evidence_refs":["substitute_technology#2"]},{"level":"🟡","text":"薄膜鈮酸鋰新進者只搶調變器，不碰磷化銦光源，威脅範圍有限。","p":"15%","evidence_refs":["competitive_share_entrants#4"]}],"roic_durability":{"quadrant":"高利益率、周轉未知：過去 12 個月 GAAP 營益率 23.35%，投入資本事實表未涵蓋，無法落到象限。","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者是 AI 叢集，決策者是雲端架構團隊與 NVIDIA，付款者是雲端與模組廠，三者都成立。要解決的問題是銅線撐不住的頻寬，會持續；解法會從 EML 換到 CW、NPO、CPO，LITE 這幾種都有產品。代理變數：EML 出貨仍低於需求，高功率雷射缺口擴大（2026-08-11）。"},{"item":"決策層級","level":"🟡","text":"設計導入後換供應商要重新認證，NVIDIA 認證耗時一年，泵浦合約三年且多數照付不議。但缺貨時客戶有貨就用（2026-08-11 Wupen Yuen），多數客戶只下採購單，替代性比供應商家數顯示的高。"},{"item":"價值鏈分配","level":"🟡","text":"目前雷射是最稀缺環節，LITE 毛利率高於模組同業；但買方極度集中，前兩大客戶占 41.6%，NVIDIA 同時資助兩家雷射廠，長期會把超額利潤往回拿。合併後部分利潤改由 Marvell 股東分享。"},{"item":"社會容忍度","level":"🟢","text":"企業間採購，沒有民生漲價爭議，價格上限由買方議價決定。政治風險集中在出口管制與關稅，已列入風險項。"}],"roiic":"事實表未涵蓋投入資本，無法計算","reinvest_rate":"事實表未涵蓋折舊、營運資金與收購淨額，無法計算","endo_ceiling":null,"formula_note":"資本支出只有 Q3、Q4 FY2026 的 1.25 億與 1.67 億美元，沒有折舊、營運資金與投入資本，內生成長率無法推導。"}}}},"q3_growth":{"verdict":"五年後跑道判為寬：NPO、CPO 與 OCS 已有訂單，但新一代架構目前幾乎沒有營收，要到 2027 下半年才開始驗證。","reasoning":"成長同時靠量與價，沒有併購或回購貢獻。共識 EPS 為 FY2027E 24.83、FY2028E 39.01、FY2029E 54.41 美元，兩年年化 48.0%。FY2026 非 GAAP 全年 EPS 事實表未涵蓋，三年年化算不出；GAAP −92.96 美元含 78 億美元非現金損失，不能當基期。內生上限因缺投入資本無法計算，共識成長與上限的缺口無法量化，定性上來自利潤率擴張與缺貨定價，其餘無法歸因，長期信心上限為中。FY2028E 共識與管理層 40 美元目標幾乎重合，賣方沒有打折；營收共識 FY2027E 66.90 億、FY2028E 104.73 億美元。跑道以下一條成長曲線判定：第二個大型 NPO／CPO 訂單預期逾 50 億美元（2026-11-02 CEO），但 2026-08-27 時 CPO／NPO 尚未反映在營收。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_consensus_rev_3m_fy1_pct"],"verdict_values":{"growth":{"driver_mix":"量與價並進，產品組合往 200G 與高功率雷射移動；併購與回購貢獻為零。","runway_years":"事實表未涵蓋滲透率，無法換算","runway_post_y5":"🟢","endo_ceiling_basis":"事實表未涵蓋投入資本，內生上限無法計算，情境樹保守視同超出上限。","segments":[{"item":"元件（Q4 FY2026）","value":"6.494 億美元，季增 22%，年增 103%"},{"item":"系統（Q4 FY2026）","value":"3.569 億美元，季增 30%，年增 123%"},{"item":"OCS（管理層）","value":"Q1 FY2027 指引為首個單季破億美元，2026 下半年目標 4 億美元"},{"item":"超高功率雷射（管理層）","value":"2026 年底單季約 5,000 萬美元，FY2027 Q3 破億美元"},{"item":"Q1 FY2027 分部金額","value":"事實表未涵蓋"}],"decay_signals":["核心市占：1.6T 世代 EML 架構占比由 70–80% 降到 40–50%（2026-08-27 CEO），亮，LITE 以 CW 部分補回。","毛利率連兩季年減：未亮，Q4 FY2026 非 GAAP 毛利率年增 12.6 個百分點。","EPS 與營收成長差距：未亮，FY2028E EPS 年增 57.1%、營收年增 56.5%，差 0.6 個百分點。","SBC 占營收：Q1 FY2027 為 11.6%，含一次性；扣除後 3.4%，未亮。","FCF／淨利、維修性資本支出、產業倍數三年走勢：事實表未涵蓋，無法判定。"],"trap_rating":"價值陷阱風險中等，亮 1 項；長期成長性同為中等。"}}},"q4_capital":{"verdict":"現金投向合理，擴產由客戶長約分擔；最大的一筆決定是用全股票把公司賣給 Marvell，這筆交易的價值還驗證不了。","reasoning":"FY2026 自由現金流 3.00 億美元，利潤率 9.96%。FY2026 GAAP 淨損 69.35 億美元含 78 億美元非現金可轉債損失，FCF／淨利轉換率沒有意義，事實表也沒有非 GAAP 全年淨利。Q3、Q4 FY2026 資本支出 1.25 億與 1.67 億美元，泵浦擴產由三年期合約分擔。現金去向四分法與債務到期結構事實表未涵蓋。Q1 FY2027 股票報酬加薪資稅 1.467 億美元占營收 11.6%，其中 8,940 萬美元是高管退休的一次性股權修改，1,420 萬美元是薪資稅，扣除後約 4,310 萬美元，占營收 3.4%。流通股增加主要來自可轉債轉股（Q4 FY2026 減債 11 億美元）與 NVIDIA 直接投資。淨負債為 −5.49 億美元；yfinance 現金 19.80 億美元低於公司 8 月所說現金及短投 27.4 億美元，兩者時點與口徑可能不同，事實表未說明。","fact_refs":["f_kpi3_sbc_and_related_payroll_","f_net_debt_m","f_shares_diluted_m","f_ev_m"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":true,"passed":null,"input":"Cloud Light 收購金額與實現報酬事實表未涵蓋；2026-08-27 CEO 承認模組毛利不及頂尖對手且過去有品質問題，方向偏負面。"},{"name":"buyback_yield","applicable":false,"passed":null,"input":"證據包未見回購，資金用於擴產與償債。"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"以 Q1 FY2027 的 1.467 億美元年化（含一次性，偏高估）為 5.87 億美元，除以市值 488.4 億美元，約 1.2%／年，低於 1.5%；扣一次性約 0.35%。股數實際增加另含可轉債轉股與 NVIDIA 投資，屬融資行為。"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購撐，證據包未見股利或回購，現金去向四分事實表未涵蓋。"}}}},"q5_valuation":{"verdict":"現價要求 FY2028 EPS 約 39 美元之後不大幅回吐，獨立看要求不高；但股東最後拿到的是 Marvell 股票，現在還無法判斷這筆換算是否划算。","reasoning":"現價 538.59 美元對 FY2027E 21.69 倍、FY2028E 13.81 倍。較 2026-08-12 的 820.59 美元下跌 34.4%，同期 FY2027 共識由 18.73 上修到 24.83 美元。PEG 以 FY2027E 到 FY2029E 兩年年化 48.0% 計為 0.45，FY2026 非 GAAP 基期缺，不用三年口徑。五年分位事實表未涵蓋，只有四個年度端點：P/S 13.05 倍在 68.7 分位，EV/S 12.90 倍在 65.9 分位。短期上行以 12 個月後 FY2028E Base 38 美元×16 倍＝608 美元，約 +12.9%；中期以 FY2029E Base 46 美元×17 倍＝782 美元，約 +45.2%。這些都是獨立價值。循環股的優先尺是股價淨值比，事實表未涵蓋帳面淨值。現價除以 4.5 隱含 Marvell 約 119.7 美元，未扣價差；Marvell 股價與盈餘事實表未涵蓋，換股比例也來自未讀原文的聚合報導。事實表市值用 9,068 萬股，非 GAAP 稀釋股約 1.009 億股，以稀釋股計市值約 543 億美元，EV 倍數偏低約一成。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_ps_current","f_ps_percentile","f_ev_s_current","f_ev_s_percentile","f_ev_s_fwd","f_ev_m","f_net_debt_m","f_shares_diluted_m"],"verdict_values":{"valuation":{"basis":"前瞻本益比（FY2027E、FY2028E），獨立口徑，未納入 Marvell 換股；P/S 與 EV/S 僅作對照。","peers":{"expanded":false,"reason":"事實表只有同業利潤率，沒有同業前瞻本益比，不能用同業倍數當錨。"},"fwd_pe":21.69,"peg":0.45,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"倍數從前份約 43.8 倍降到 21.69 倍，偏貴的問題已解除；PEG 0.45 因分母有爭議，不計入便宜論證；P/S 年度端點 68.7 分位屬中上。綜合判為合理。","upside_short_pct":12.9,"upside_mid_pct":45.2,"denominator_disputed":true,"denominator_note":"分母是缺貨定價下的盈餘：GAAP 毛利率兩年多內由 18.5% 升到 51%，FY2028E 又與管理層目標幾乎重合。分母是否為高點正是爭點，低倍數不能當便宜的證據。"}}},"q6_how_wrong":{"verdict":"最可能看錯在兩處：雷射缺貨比本檔假設更早結束，以及獨立估值掩蓋了 Marvell 換股的真實價值。","reasoning":"歷史最大回撤與空方最強數字事實表未涵蓋；股價 26 週已跌 40.41%，RSI 29.51，距 52 週線 −23.9%。衰退信號亮 1 項，分母爭議未解，價值陷阱列中等。法說迴避紀錄值得記下：2026-09-09 不拆 40 美元 EPS 的毛利假設，Coherent 追上高功率雷射的時點答不知道；2026-11-02 不拆 10 億美元協同的成本占比，也不答是否有其他出價者。Q1 FY2027 完整法說不在本包，同季的管理層問答無法核對。","fact_refs":["f_week26_return_pct","f_rsi14","f_ma_w52","f_ma_w104","f_price_at_dd"],"verdict_values":{"trap":{"verdict":"🟡","label":"分母爭議未解，衰退信號亮 1 項"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":24.83,"pe":21.69,"basis":"FY1（FY2027E，六月底年度）非 GAAP 共識 EPS，與終端倍數同為當年度前瞻口徑；全部為獨立口徑，未納入 Marvell 換股。"},"eps":{"bull":[26.5,44,64,77,85],"base":[24.8,38,46,45,50],"bear":[23.6,31,27,20,24]},"pe":{"bull":20,"base":17,"bear":15},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0,"net_buyback":0},"second_stage":{"bull_cagr_pct":12,"base_cagr_pct":8},"max_dd":{"lo":-60,"hi":-40,"basis":"Bear 路徑 FY2030E 低谷 EPS 20 美元×12–14 倍＝240–280 美元，距現價 −48%～−55%；下緣再留合併破局的跳空，取 −60%；上緣 −40% 對應近 26 週實際跌幅 −40.41%。","trigger_time":null},"basis":{"bull":"CPO、NPO 於 2028 年放量，第二個逾 50 億美元訂單如期，缺貨延續到 2029；FY2031E 營收約 230 億美元；終端 20 倍。同業前瞻本益比事實表未涵蓋，以本檔現值 FY1 21.69 倍對照。","base":"FY2028E 略低於管理層目標，FY2029–30 缺貨紓解、價格回吐使 EPS 停在 45–46 美元，FY2031E 靠 NPO、CPO 回到 50 美元；終端 17 倍，低於本檔現值 FY1 21.69 倍。","bear":"FY2027 下半年持平，2028 年供給開出、長約重議，營收較高峰回落約兩成五、毛利率退到 40% 左右，FY2030E 低谷 20 美元；終端 15 倍取成長降到一成的倍數，參考本檔現值 FY2 13.81 倍。"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"TrendForce 估 2026 年 EML＋CW-DFB 月產能約倍增；Coherent 有 NVIDIA 長約；中國磷化銦新廠進場；多數客戶只下採購單；FY2024 營收年減 23%、毛利率 18.5%。","assumption":"2027 年前缺貨不會結束，2028 年擴產開出時需求由 NPO、CPO 接手。","consequence":"五年後虧 50% 最可能的故事：2028 年供給開出時 scale-up 延後，長約重議，EPS 回到 20 美元，倍數 12–14 倍。","ruling":"採納為 Bear 路徑核心，與唯一致命點相同，機率 30%。短期不成立，管理層 2026-09-09 仍說新約價格不低於舊約。","watch":"雷射合約價季變動、EML 缺口用語、Coherent 認證進度。","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1","customer_concentration_credit#1","geo_supply_chain#0"],"fact_refs":["f_kpi5_gaap_gross_margin"]},{"view":"論點成功但股東經濟變差","evidence":"全股票併入 Marvell，換股比例傳為 4.5 股；10 億美元協同主要在銷貨成本，CFO 不拆細項；ELS 模組毛利低於雷射；Marvell 要投數十億美元鎖產能。","assumption":"雷射需求如期，LITE 獨立 EPS 達到 40 美元。","consequence":"LITE 業務成功，但上行由合併後全體股東分享，LITE 股東拿到的是一定股數的 Marvell；若 Marvell 自身業務拖累，報酬會低於獨立路徑。","ruling":"採納。獨立情境樹的上下行比例不得當進場依據，S-4 公開後改用 Marvell 股票口徑重算。","watch":"S-4 條款，LITE 股價除以 4.5 與 Marvell 股價的價差。","evidence_refs":["ma_merger#0","major_events#0"],"fact_refs":["f_price_at_dd"]},{"view":"價格已反映太多","evidence":"P/S 13.05 倍在四個年度端點的 68.7 分位；FY2028E 共識與管理層目標幾乎重合，賣方未打折；GAAP 毛利率已到 51%。","assumption":"FY2027E 21.69 倍隱含的盈餘可持續。","consequence":"Base 終端 17 倍、EPS 50 美元時年化約一成，只落在中段。","ruling":"部分反駁。股價較前份下跌 34.4%、FY2027 共識上修 32.6%，偏貴的問題已解除；分母是否高點未解，所以只到合理。","watch":"FY2028 共識方向、毛利率是否見頂。","fact_refs":["f_ps_current","f_ps_percentile","f_fwd_pe_latest","f_consensus_eps_fy2"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟢","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟢","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 820.59 → 本次 538.59（-34.4%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=820.59","side_b":"本次 price_at_dd=538.59","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]角色由 dd_decision.py 機械路由：前份 候選/追蹤池 → 本次 追蹤","cause":"新證據","prior_field":["dca_role"],"side_a":"前份 dca_role=候選/追蹤池","side_b":"本次 dca_role=追蹤","ruling":"角色是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。沒有單一輸入能還原，屬多欄共同：估值 🔴→🟡、均線 ✅→🟢、五年後跑道 🟡→🟢。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 820.59 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 820.59 美元：Bull 價 1,948.8、Bear 價 411.9，五年期望值 +39.0%，基準年化 7.5%，不對稱比 2.3","side_b":"本次情境、股價仍用 820.59 美元：Bull 價 1,700、Bear 價 360，五年期望值 +11.6%，基準年化 0.7%，不對稱比 1.59","ruling":"先換情境、股價不動：五年期望值少 27.4 個百分點，基準年化少 6.8 個百分點。不對稱比由 2.3 變為 1.59。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 820.59 美元：五年期望值 +11.6%，基準年化 0.7%，不對稱比 1.59","side_b":"本次情境、股價 538.59 美元：五年期望值 +70.0%，基準年化 9.6%，不對稱比 5.42","ruling":"再換股價、情境不動：起點價下跌 34.4%，五年期望值多 58.4 個百分點，基準年化多 8.8 個百分點，不對稱比由 1.59 升到 5.42。合計五年期望值比前份多 31.0 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"前份估值門檻已達成","cause":"價格變動","prior_field":["val","p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份：股價 820.59 美元、FY2027 基礎前瞻本益比約 43.8 倍，估值結論偏貴，Bull 機率 25%、Bear 機率 30%，最大回撤 −58%。","side_b":"本次：股價 538.59 美元、21.69 倍，前份「前瞻本益比回落到 32 倍以下」已達成；Bull、Bear 機率維持 25%、30%，最大回撤區間 −40%～−60%。","ruling":"估值結論由偏貴改為合理。機率未動，新增訂單的利多與合併、供給風險互相抵銷。前份的 COHR 認證前提在事實表沒有新資料，毛利率連四季高於 48% 尚未達成。","evidence_level":"高","settle_metric":"FY2027E 前瞻本益比","if_then":["若股價續漲但 S-4 尚未公開，不追","若股價下跌而毛利率與新約價格未受損，S-4 確認後分批反買"],"evidence_refs":[]},{"axis":"合併案改寫持有標的，等待的理由換了","cause":"新證據","prior_field":["signal"],"side_a":"前份因估值過高而等待，卡住的是價格。","side_b":"本次價格問題解除，卡住的是事件：2026-11-01 簽約併入 Marvell，股東收到 Marvell 股票，換股條款、終止費、監管條件與 Marvell 價值都未驗證。","ruling":"裁決方向維持等待，綜合訊號維持同一級，約束條件由價格改為合併條款。此約束的否定就是重新評估條件，不設進場價。","evidence_level":"中","settle_metric":"S-4 條款與 Marvell 股票口徑的 Base 年化報酬","if_then":["若 S-4 確認條款且 Marvell 口徑 Base 年化達 12%，重跑判斷，首倉以小部位起步","若合併終止，回到獨立路徑重跑，判斷前停止加碼"],"evidence_refs":["ma_merger#0","major_events#0"]},{"axis":"交易金額與市值對不上","side_a":"聚合報導：全股票、4.5 股 Marvell 換 1 股 LITE，交易約 1,150 億美元。","side_b":"事實表 LITE 市值 488.4 億美元；若 1,150 億美元是收購價，每股約 1,140 美元，現價只有一半，不像正常交易價差。","ruling":"不採用 1,150 億美元當收購價，較可能是合併後規模或報導誤差；4.5 股換股比例也列待驗證，本檔未讀 8-K 條款全文。","evidence_level":"低","settle_metric":"合併協議全文與 S-4","if_then":["若換股比例與報導不同，全部 Marvell 口徑數字重算，重算前不追"],"evidence_refs":["major_events#0"]},{"axis":"雷射缺貨能撐多久","cause":"新證據","prior_field":["trap","moat_trend","cycle_position"],"side_a":"管理層：2027 缺口不會緩解，新約價格不低於舊約（2026-09-09）；被問超額供給，執行長認為風險低（2026-05-05）。","side_b":"TrendForce：2026 年 EML＋CW-DFB 月產能約倍增；中國磷化銦新廠陸續出現；英國廠與 Greensboro 在 2027–2028 開出。","ruling":"可調和，屬時間差：2027 年前採信管理層，2028 年起不採信。陷阱風險維持中等、護城河方向維持穩定，循環位置由晚循環到過熱頂部收斂為晚循環。","evidence_level":"中","settle_metric":"雷射合約價季變動與 EML 缺口用語","if_then":["若下季新約價格仍不低於舊約，維持 Base 路徑","若任一類雷射合約價首度季減，減碼至半倉並改用 Bear 路徑"],"evidence_refs":["geo_supply_chain#0"]},{"axis":"五年後跑道上調","cause":"新證據","prior_field":["runway_post_y5"],"side_a":"前份：跑道中等，第二引擎待驗證。","side_b":"本次：第二個大型 NPO／CPO 訂單預期逾 50 億美元（2026-11-02 CEO），NPO 放量由 2028 底提前到 2027 底（2026-08-27 CEO）。","ruling":"上調為寬，只代表需求面的下一條曲線已有訂單。營收要到 2027 下半年才能驗證，驗證前不提高 Bull 機率。","evidence_level":"中","settle_metric":"FY2027 Q3 超高功率雷射單季營收與 2028 年 NPO、CPO 出貨","if_then":["若超高功率雷射 FY2027 Q3 未破 1 億美元，跑道回調為中等並停止加碼"],"evidence_refs":[]},{"axis":"商業類型重新歸類","cause":"方法變動","prior_field":["archetype"],"side_a":"前份歸為品質複利成長。","side_b":"本次歸為循環/商品，次要屬性為特殊情境。","ruling":"近四個財年有兩年自由現金流為負，FY2024 毛利率 18.5%，獲利躍升來自缺貨定價，用複利股的尺度會高估持續性。若缺貨結束後毛利率仍守住 45% 以上，應改回成長型。","evidence_level":"高","settle_metric":"缺貨紓解後的毛利率","if_then":["若供需平衡後毛利率連四季高於 45%，改回成長型重算倍數"],"evidence_refs":[]},{"axis":"管理層說獨立前景極好，卻交出控制權","side_a":"2026-09-09 管理層對 FY28 EPS 40 美元表示有信心，並稱最好的日子還在後面。","side_b":"2026-11-01 同意全股票併入 Marvell；2026-11-02 執行長稱合併第一名勝過買下多家第二到第四名，雙方沒有回答是否有其他出價者，也沒有談買在短缺高峰的價格倍數。","ruling":"可調和。賣出本身不能證明獨立前景變差，但 40 美元目標的可信度要打折，獨立上行也不再全歸 LITE 股東。","evidence_level":"低","settle_metric":"S-4 合併背景章節的出價過程與財務顧問預測","if_then":["若 S-4 顯示財務顧問預測明顯低於 40 美元，Base 的 FY2028E 下修並停止加碼"],"evidence_refs":["ma_merger#0"]},{"axis":"OCS 客戶基礎改口","side_a":"2026-05-05 執行長：OCS 與三家客戶合作，兩家占多數。","side_b":"2026-08-27 執行長：目前主要綁定單一客戶；2026-09-09 管理層：上行來自最大客戶，該客戶還保留內部供應。","ruling":"採信後者，集中度上升，40 美元目標更依賴單一客戶。","evidence_level":"中","settle_metric":"2027 年初是否成為該客戶第一 OCS 供應商、10-K 客戶占比","if_then":["若最大客戶占比升到 35% 以上，減碼"],"evidence_refs":["customer_concentration_credit#0","customer_second_source#1"]},{"axis":"現在就買的最強論證","side_a":"FY2028E 13.81 倍，RSI 29.51，股價低於 52 週線 23.9%，EPS 連兩季高於指引上緣，訂單還在加；若合併破局，獨立路徑 Base 五年仍有約 58% 報酬。","side_b":"股東實收 Marvell 股票，Marvell 股價與盈餘不在事實表；分母爭議未解；交割前約 18 個月股價跟著 Marvell 走。","ruling":"不採納現在買進，等 S-4。代價是股價先反彈時會錯過一段，本檔接受。","evidence_level":"中","settle_metric":"S-4 與 Q2 FY2027 財報","if_then":["若股價續漲但條款未明，不追","若股價再跌且基本面無損，S-4 確認後分批反買"],"evidence_refs":[]},{"axis":"重新評估門檻更換，減碼與清倉條件另列","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"Fwd PE(FY27基礎，隨最新共識滾動重算)回落至≤32x或5Y分位<70%；或GM連續4季維持>48%；生意面前提：COHR 200G/lane EML於任一top hyperscaler/NVIDIA完成客戶認證前，估值觸發不因股價波動單獨視為安全邊際打開","side_b":"S-4 公開並讀過換股條款、終止費與監管條件後，以 Marvell 股票口徑重算，Base 年化達 12% 才重跑進場判斷。","ruling":"舊門檻的估值部分已達成，合併案使獨立估值不再是決定條件，改成事件門檻；減碼與清倉條件列在觸發器。","evidence_level":"中","settle_metric":"S-4","if_then":[],"evidence_refs":["ma_merger#0"]},{"axis":"Single Thing 首次設立","cause":"新證據","prior_field":null,"side_a":"前份未設唯一致命點（摘要此欄為空）","side_b":"2028 年底前，雷射由缺貨翻成過剩，出現第一筆合約價季減或前兩大客戶遞延長約。","ruling":"選敏感度最大的一項，合併案影響報酬形式，對盈餘的敏感度小於雷射定價。","evidence_level":"中","settle_metric":"雷射合約價與長約揭露","if_then":["若發生，減碼至半倉"],"evidence_refs":[]},{"axis":"減碼與清倉指標首次設立","cause":"新證據","prior_field":["kill_metrics"],"side_a":"前份未列減碼或清倉指標（摘要此欄為空）","side_b":"本次新增五項：毛利率連兩季低於 48%、FY2028 共識跌破 30 美元、雷射合約價首度季減、最大客戶占比達 35%、合併終止或被要求剝離資產。","ruling":"舊檔沒有下行紀律，合併與缺貨高峰下需要明確的減碼與清倉條件。","evidence_level":"中","settle_metric":"各指標來源見清單","if_then":[],"evidence_refs":[]}],"triggers":[{"n":1,"text":"Q2 FY2027 財報確認毛利率與指引","type":"假設驗證","maps_to":"H1","metric":"非 GAAP 毛利率、營收、EPS","threshold":"毛利率 ≥ 50%，營收落在 15.75–16.25 億美元，EPS 5.90–6.20 美元","action":"低於任一下緣則停止加碼，並重算 Base 路徑","source_freq":"公司新聞稿，每季","date":"2027-02"},{"n":2,"text":"管理層承諾的 12 月季 EML 出貨年增逾 50%","type":"假設驗證","maps_to":"H1","metric":"EML 單位出貨年增率","threshold":"＞50%","action":"未達則停止加碼","source_freq":"法說，每季","date":"2027-02"},{"n":3,"text":"超高功率雷射與 OCS 里程碑","type":"假設驗證","maps_to":"H3","metric":"FY2027 Q3 超高功率雷射單季營收；2026 下半年 OCS 營收；是否成為最大客戶的第一 OCS 供應商","threshold":"雷射 ≥ 1 億美元；OCS ≥ 4 億美元；2027 年 6 月前完成超車","action":"兩項未達則下修第二引擎假設並停止加碼","source_freq":"法說，每季","date":"2027-05"},{"n":4,"text":"S-4 公開後重跑判斷","type":"估值rearm","maps_to":"H4","metric":"換股比例、終止費、監管條件；Marvell 股票口徑的 Base 年化報酬","threshold":"Base 年化 ≥ 12%","action":"達標才重跑進場判斷，首倉以小部位起步","source_freq":"SEC 申報，單次","date":"2027Q1（本檔估計）","evidence_refs":["ma_merger#0"]},{"n":5,"text":"雷射合約價首度季減或前兩大客戶遞延長約","type":"Single Thing","maps_to":"H1","metric":"EML、CW、泵浦雷射合約價季變動；長約重議揭露","threshold":"任一類首度季減，或前兩大客戶任一遞延","action":"減碼至半倉，改用 Bear 路徑重算","source_freq":"法說與 TrendForce，每季","date":"至 2028-12","evidence_refs":["competitive_share_entrants#0"]},{"n":6,"text":"獲利與毛利率同時破線","type":"清倉","maps_to":"H2","metric":"FY2028 共識 EPS 與非 GAAP 毛利率","threshold":"共識跌破 30 美元，且毛利率連兩季低於 48%","action":"清倉","source_freq":"Koyfin 共識快照與公司新聞稿，每季","date":"至 2027-12"},{"n":7,"text":"合併終止或被要求剝離核心資產","type":"風險","maps_to":"R1","metric":"8-K 與監管公告","threshold":"終止、換股比例重議，或剝離磷化銦、OCS 資產","action":"停止加碼，回到獨立路徑重跑","source_freq":"SEC 申報，事件驅動","date":"至 2028-06","evidence_refs":["ma_merger#0","major_events#0"]},{"n":8,"text":"BIS、DOJ 調查的結案方式","type":"風險","maps_to":"R4","metric":"和解金額與程序性質","threshold":"和解或罰款 ≥ 3 億美元；或刑事起訴、出口權限遭拒","action":"金額達標減碼三分之一；刑事起訴或出口權限遭拒則清倉","source_freq":"10-Q 風險因素，每季","date":"結案時點事實表未涵蓋","evidence_refs":["regulatory_antitrust#0","major_events#1","sec_investigation_restatement#0"]},{"n":9,"text":"最大客戶占比續升","type":"風險","maps_to":"R2","metric":"最大客戶營收占比與應收帳款占比","threshold":"營收占比 ≥ 35%，或應收占比 ≥ 40%","action":"減碼","source_freq":"10-K，每年","date":"2027-08","evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#2"]},{"n":10,"text":"關稅或材料管制吸收失敗","type":"風險","maps_to":"R5","metric":"非 GAAP 毛利率季變動與公司歸因","threshold":"單季下降 ≥ 2 個百分點，且公司歸因關稅或材料","action":"停止加碼","source_freq":"法說，每季","date":null,"evidence_refs":["reg_tariff_export#4","reg_tariff_export#2"]},{"n":11,"text":"下次完整複審","type":"複審日期","maps_to":"H4","metric":"S-4 是否公開、Q2 FY2027 財報是否發布","threshold":"日期到期","action":"重跑判斷","source_freq":"單次","date":"2027-02"}],"kill_metrics":[{"metric":"非 GAAP 毛利率（單季）","bear_threshold":"連兩季低於 48%","window":"2027 全年","source":"公司季度新聞稿","last_status":"ok"},{"metric":"FY2028 共識 EPS","bear_threshold":"跌破 30 美元（目前 39.01 美元）","window":"至 2027-12","source":"Koyfin 共識快照","last_status":"ok"},{"metric":"雷射合約價季變動","bear_threshold":"任一類雷射合約價首度季減","window":"至 2028-12","source":"法說與 TrendForce","last_status":"ok"},{"metric":"最大客戶營收占比","bear_threshold":"≥35%（FY2026 為 26.6%）","window":"FY2027 10-K","source":"SEC 10-K","last_status":"warning"},{"metric":"合併案狀態","bear_threshold":"終止、重議換股比例，或被要求剝離磷化銦資產","window":"至 2028-06","source":"SEC 8-K 與 S-4","last_status":"unknown"}],"evidence_dismissed":[{"ref":"geo_supply_chain#2","reason":"這是 FY2022 10-K 的搜尋摘要轉述，不是原文，內容是 FY22 Q3 疫情停工，成因已消失；目前工廠分布改用 2026 年法說的日本、泰國與 Rose Orchard 資訊。"}],"action_conditions":{"rearm_trigger":"S-4 公開並讀過換股條款、終止費與監管條件後，以 Marvell 股票口徑重算，Base 年化達 12% 才重跑進場判斷。","exec_line":"S-4 公開前不開新倉，不因 RSI 低接；已持有者續抱不加碼，雷射合約價首度季減即減碼至半倉。","holding_cap":"S-4 確認前新增部位為零；確認後首倉從小部位起步，需有承受 −60% 等級回撤的準備。"}},"decision_inputs":{"signal":"B","ma":"🟢","cycle_position":"晚循環","cycle_verdict":"未觸發","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":false,"wait_for_price":true,"wait_for_price_condition":"等 S-4 公開換股條款、終止費與監管條件，以 Marvell 股票口徑重算 Base 年化報酬達 12% 再重跑判斷。"},"thesis":{"H":[{"id":"H1","text":"雷射供不應求延續到 2027 年底，定價不回吐，非 GAAP 毛利率站穩 50% 以上。","2y":"FY2027、FY2028 單季毛利率維持 50% 以上","5y":null,"10y":null,"threshold":"非 GAAP 毛利率單季 ≥ 50%（Q4 FY2026 為 50.4%）","source":"公司季度新聞稿與法說對供需缺口的用語","drift_rule":"連 2 季低於 47.5% 為削弱，連 3 季低於 45% 為反轉"},{"id":"H2","text":"FY2028 非 GAAP EPS 達 37 美元以上，管理層 40 美元目標至少兌現九成多。","2y":"FY2028 EPS ≥ 37 美元","5y":null,"10y":null,"threshold":"FY2028 EPS ≥ 37 美元（共識 39.01 美元的 95%）","source":"公司季報與 Koyfin 共識快照","drift_rule":"FY2028 共識連 2 季低於 37 美元為削弱，連 3 季低於 35 美元為反轉"},{"id":"H3","text":"CPO、NPO 與 OCS 成為第二引擎，撐住缺貨紅利消退後的獲利。","2y":null,"5y":"FY2031 前三項合計占營收三成以上","10y":null,"threshold":"2028 年超高功率雷射、ELS 與 OCS 合計營收 ≥ 30 億美元；前哨為 FY2027 Q3 超高功率雷射單季 ≥ 1 億美元","source":"法說、新聞稿與合併後分部揭露","drift_rule":"里程碑連 4 季落後 5% 以上為削弱，連 6 季落後 10% 以上為反轉"},{"id":"H4","text":"合併案在 2028 上半年完成，換到的 Marvell 股票價值不低於 LITE 獨立路徑；換股比例待原文確認。","2y":"交割時換股價值不低於獨立估值","5y":null,"10y":null,"threshold":"換股比例隱含價值 ≥ 608 美元（FY2028E Base 38 美元×16 倍）","source":"8-K、S-4 與 Marvell 股價；Marvell 資料事實表未涵蓋","drift_rule":"隱含價值連 2 季低於門檻 5% 以上為削弱，連 3 季低於門檻 10% 以上為反轉"}],"R":[{"id":"R1","text":"合併案風險：全股票換股，比例與機制待原文確認，交割預期在 2028 上半年，期間股價跟 Marvell 連動；破局或監管要求剝離資產都會改變報酬來源。終止費與核准清單事實表未涵蓋。","h_ref":"H4","clock":"🔥","threshold":"合併終止、換股比例重議，或監管要求剝離磷化銦、OCS 資產","evidence_refs":["ma_merger#0","major_events#0"]},{"id":"R2","text":"客戶集中與第二來源：最大客戶占 FY2026 營收 26.6%（FY2025 15.4%），第二大 15.0%；兩大客戶占應收 30% 與 11%；多數客戶以採購單下單，過去曾因客戶採購變動而減單。未見最大客戶導入第二來源或自製的明確揭露，客戶身分只有二手推測。","h_ref":"H2","clock":"🔥","threshold":"最大客戶占比 ≥ 35%，或最大客戶應收占比 ≥ 40%，或前兩大客戶任一減單","evidence_refs":["customer_second_source#0","customer_second_source#1","customer_concentration_credit#0","customer_concentration_credit#1","customer_concentration_credit#2"]},{"id":"R3","text":"競爭與定價：10-K 寫明光通訊產品走向商品化，亞洲新進者帶來價格壓力，對手可能以低價搶份額；目前只有管理層說法顯示未受影響。","h_ref":"H1","clock":"🔥","threshold":"雷射合約價首度季減，或 Coherent 200G EML、超高功率雷射通過 NVIDIA 或前三大雲端認證","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1","substitute_technology#0"]},{"id":"R4","text":"出口管制調查：2024-08 起 BIS 與 DOJ 傳票查華為業務，仍在進行，未見和解或處罰。公司 2024 年初已停止對華為出貨，現行營收不受影響，風險在罰款與出口權限；屬行政傳票與司法部傳票程序，罰款區間與結案時點事實表未涵蓋。","h_ref":"H4","clock":"🐢","threshold":"和解或罰款 ≥ 3 億美元，或刑事起訴、出口權限遭拒","evidence_refs":["regulatory_antitrust#0","major_events#1","sec_investigation_restatement#0","reg_tariff_export#0"]},{"id":"R5","text":"關稅與材料管制：232 條款半導體調查、美國出口管制、中國稀土與基板限制、部分供應商在中國，製造與代工集中亞洲；無法轉嫁就壓縮毛利率。","h_ref":"H1","clock":"🐢","threshold":"單季毛利率下降 ≥ 2 個百分點，且公司歸因關稅或材料管制","evidence_refs":["regulatory_antitrust#1","reg_tariff_export#1","reg_tariff_export#2","reg_tariff_export#3","reg_tariff_export#4","geo_supply_chain#1"]},{"id":"R6","text":"自身供給：磷化銦基板吃緊，AXT 新約後管理層仍說一兩季後可能不夠；雖有多座晶圓廠，缺口仍在擴大，擴產最大變數是客戶認證時間。","h_ref":"H3","clock":"🔥","threshold":"Greensboro 首批營收延到 2028 下半年之後，或基板短缺使單季營收低於指引下緣","evidence_refs":["geo_supply_chain#0"]}],"single_thing":{"description":"2028 年底前，雷射由缺貨翻成過剩，出現第一筆合約價季減或前兩大客戶遞延長約。","why_fatal":"這是情境樹最大的單一敏感項：Base 與 Bear 的終端 EPS 差 26 美元，多數來自定價與毛利率。毛利率每掉 1 個百分點，FY2028E EPS 約少 0.86 美元（營收 104.73 億美元×1%×83.5%÷1.02 億股）；上一輪下行的 FY2024 營收年減 23%、毛利率 18.5%。","if_happens":"不等合併結果，減碼至半倉並改用 Bear 路徑重算；下一季續跌且 FY2028 共識跌破 30 美元則清倉。","how_monitor":"每季毛利率、法說對 EML 與高功率雷射缺口的用語（2026-08-11 為 EML 未縮、高功率更落後）、新約價格描述、TrendForce 產能與報價；交割後改看 Marvell 光學相關揭露。","probability":"12–24 個月約 25%：2027 年前缺貨有長約支撐，風險集中在 2028 年 Greensboro、英國廠與對手產能同時開出。"}},"appendix_a":{"growth_durability":7,"quality_score":6,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":13.81,"peg_fy2":0.35,"stress":{"pass":null,"total":null}},"eps_meta":{"base_eps_path":{"FY2026A":-92.96,"FY2027E":24.83,"FY2028E":39.01,"FY2029E":54.41},"fy_end_month":6,"eps_basis":"FY2027E–FY2029E 為 Koyfin 共識，與公司非 GAAP EPS 同口徑，財年止於六月底；分析師家數事實表未涵蓋，營收共識為 21–22 家。FY2026A 欄只有 GAAP 稀釋 EPS −92.96 美元，含 78 億美元非現金可轉債損失，與共識不同口徑，不能用來算成長率；FY2026 非 GAAP 全年 EPS 事實表未涵蓋。"},"catalysts":[{"date":"2027-02","date_precision":"month","type":"guidance","event":"Q2 FY2027 財報，時點為本檔估計","impact":"高","watch":"毛利率是否站穩 50%、EML 出貨年增是否逾 50%、新約價格用語"},{"date":"2027Q1","date_precision":"quarter","type":"other","event":"合併案 S-4 公開，時點為本檔估計","impact":"高","watch":"換股比例、終止費、監管核准清單、出價過程與財務顧問預測"},{"date":"2027-05","date_precision":"month","type":"product","event":"FY2027 Q3 財報驗證超高功率雷射單季破億美元，時點為本檔估計","impact":"中","watch":"超高功率雷射營收與 OCS 第一供應商進度"},{"date":"2028Q1","date_precision":"quarter","type":"capacity","event":"Greensboro 磷化銦廠首批營收","impact":"高","watch":"是否延後，以及供給開出時雷射合約價的變化"},{"date":"2028Q2","date_precision":"quarter","type":"other","event":"Marvell 合併案預期於 2028 上半年交割","impact":"高","watch":"監管核准進度與交割前換股價差"}],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8(val爭議)","pacing":[],"holding_cap":null,"audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟢'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟢', val='🟡', moat_trend='→', week26=-40.41, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='循環/商品', cycle_position='晚循環', moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈機械讀數判定不可用，baseline rows 8/9/9b/10 的估值條件視為不可判 → 落 row8 觀望（保守方向）","hit":true,"basis":"val_denominator_disputed=True, val(機械讀數)='🟡'"},{"row":"QC-49","condition":"qc49_inherit_prior=False，不套用","hit":false,"basis":"qc49_inherit_prior=False"},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"requires_critic":[]}}
```

---

## ⑤ 覆蓋面（程式判定，你回的 ⑤ 燈號會被覆寫）

燈號 🟢：核心軸皆有證據或不適用，非核心軸也沒有空軸。plan 時 archetype 為「品質複利成長」、判斷者歸「循環/商品」，循環/商品 的專屬核心軸未採證（不計燈號）：cyclical_inventory_price_position、cyclical_supply_discipline_capacity。

⑤ 的 reason 只需評論：空軸的查詢詞是否切題、判斷有沒有交代缺口對結論的影響。

---

## 尾段：回覆格式

只回一個 JSON 陣列，①–⑧ 每條一個元素，八個全出，不得跳號、不得多列，陣列外不得有任何文字（不加前言、不加 markdown 圍欄、不加附註）：

```json
[{"item": "①", "light": "🔴|🟡|🟢", "judgment_path": "$.路徑", "reason": "一句話"}]
```
