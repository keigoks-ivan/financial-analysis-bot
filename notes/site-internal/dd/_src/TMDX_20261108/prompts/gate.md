你是 DD 管線 v20 的判斷層閘（gate），標的 TMDX（20261108）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（36 條）
- `f_kpi0_total_revenue_gaap`（q1_business）｜Total revenue (GAAP)＝203.0 $M｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（8-K ex99.1）https://www.sec.gov/Archives/edgar/data/0001756262/000119312526449729/tmdx-ex99_1.htm（numbers.latest_quarter_kpis.items[0]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-11-05））
  - 註記：未查
- `f_kpi1_non_gaap_operating_incom`（q1_business）｜Non-GAAP operating income / margin＝14.2 % (adj. op income $28.9M)｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（8-K ex99.1）https://www.sec.gov/Archives/edgar/data/0001756262/000119312526449729/tmdx-ex99_1.htm（numbers.latest_quarter_kpis.items[1]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-11-05））
  - 註記：未查
- `f_kpi2_gaap_operating_income_ma`（q1_business）｜GAAP operating income / margin＝13.9 % (op income $28.1M)｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（8-K ex99.1）https://www.sec.gov/Archives/edgar/data/0001756262/000119312526449729/tmdx-ex99_1.htm（numbers.latest_quarter_kpis.items[2]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-11-05））
  - 註記：未查
- `f_kpi4_guidance_fy2026_revenue_`（q1_business）｜Guidance FY2026 revenue (incl. PAD Aviation)＝764-774 $M（含 PAD；不含 PAD 750-760，上調自 737-757）｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司 Q3 2026 新聞稿（8-K ex99.1）https://www.sec.gov/Archives/edgar/data/0001756262/000119312526449729/tmdx-ex99_1.htm（numbers.latest_quarter_kpis.items[4]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-11-05））
  - 註記：未查
- `f_kpi5_gross_margin`（q1_business）｜Gross margin＝58.5 %｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（8-K ex99.1）https://www.sec.gov/Archives/edgar/data/0001756262/000119312526449729/tmdx-ex99_1.htm（numbers.latest_quarter_kpis.items[5]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-11-05））
  - 註記：n/a
- `f_peer_tmdx_gross_margin_pct`（q2_moat）｜TMDX 毛利率＝58.69 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.TMDX.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_tmdx_operating_margin_pct`（q2_moat）｜TMDX 營業利益率＝12.21 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.TMDX.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_tmdx_fcf_margin_pct`（q2_moat）｜TMDX FCF 利潤率＝11.82 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.TMDX.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_abt_operating_margin_pct`（q2_moat）｜ABT 營業利益率＝13.9 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ABT.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_mdt_operating_margin_pct`（q2_moat）｜MDT 營業利益率＝19.04 %｜期間與口徑：TTM ending 2026-07-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MDT.operating_margin_pct，as_of TTM ending 2026-07-31（4季加總））
- `f_peer_gkos_operating_margin_pct`（q2_moat）｜GKOS 營業利益率＝-25.3 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.GKOS.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_podd_gross_margin_pct`（q2_moat）｜PODD 毛利率＝71.88 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.PODD.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_podd_operating_margin_pct`（q2_moat）｜PODD 營業利益率＝18.44 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.PODD.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝1.51 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-11-07）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝2.25 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-11-07）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝3.31 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-11-07）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝769.07 USD m｜期間與口徑：2026-11-08／yfinance revenue_estimate 0y 平均（9 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝895.08 USD m｜期間與口徑：2026-11-08／yfinance revenue_estimate +1y 平均（12 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi3_sbc`（q4_capital）｜SBC＝12.1 $M（約占營收 6.0%、占 GAAP 營業利益 43%）｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（8-K ex99.1）https://www.sec.gov/Archives/edgar/data/0001756262/000119312526449729/tmdx-ex99_1.htm（10-Q 權益表列 $12.6M，口徑差異）（numbers.latest_quarter_kpis.items[3]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-11-05））
  - 註記：n/a
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝373.94 USD m｜期間與口徑：2026-11-08／yfinance 最新一季：總債務 866.9、現金 492.96（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝34.73 m shares｜期間與口徑：2026-11-08／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_ev_m`（q5_valuation）｜目前企業價值 EV（市值＋淨負債）＝3438.86 USD m｜期間與口徑：2026-11-08／市值 3064.92 ＋ 淨負債 373.94｜kind：realized
  - 來源：—（numbers.capital_structure.ev_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝88.24 USD｜期間與口徑：2026-11-06（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-11-06（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝58.44 x｜期間與口徑：2026-11-07／分母＝FY1 EPS 1.51，分子＝快照價 88.24｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-11-07）
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝24.04 x｜期間與口徑：2026-11-06（RTH 收盤，UTC）／2 個年度端點內的分位＝0.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-11-06（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝0.0 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 2 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝4.21 x｜期間與口徑：2026-11-06（RTH 收盤，UTC）／4 個年度端點內的分位＝0.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝0.0 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝4.73 x｜期間與口徑：2026-11-06（RTH 收盤，UTC）／4 個年度端點內的分位＝0.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ev_s_fwd`（q5_valuation）｜EV/S（EV ÷ FY1 共識營收）＝4.47 x｜期間與口徑：2026-11-08／f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）｜kind：estimate
  - 來源：—（numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_ma_w52`（q5_valuation）｜52 週均線＝100.08 USD｜期間與口徑：2026-11-08／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）
- `f_ma_w250`（q5_valuation）｜250 週均線＝84.35 USD｜期間與口徑：2026-11-08／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝-3.21 %｜期間與口徑：2026-08-13 → 2026-11-07／FY1 共識 EPS 1.56 → 1.51（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-11-07）
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝30.07 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-11-06（RTH 收盤，UTC））
- `f_rsi14`（q5_valuation）｜RSI(14)＝66.55｜期間與口徑：2026-11-06（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ma_state`（q5_valuation）｜週線均線六態（decision_inputs.ma 必須等於此值）＝🟠｜期間與口徑：2026-11-08／timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）
  - 原文：「price 88.24 / W52 100.08 / W104 98.73 / W250 84.35 / W250 13週斜率 1.09%」

### findings_digest 中方向為負或來源衝突的條目（19 條）
- `competitive_share_entrants#1`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K風險因子承認他方可能開發更好、更便宜產品使OCS過時，且許多對手資源更大。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-24）｜affects：thesis.R、decision_inputs.bear
- `competitive_share_entrants#2`（competitive_share_entrants｜方向 -｜狀態 ok）：XVIVO心臟冷灌注Heart Assist Transport預期2026年有機會獲FDA PMA核准，主要對手為TransMedics。
  - 來源：briefglance: New Hope for Hearts: XVIVO Trial Boosts Organ Viability（as_of 2026-04-01）｜affects：moat_trend、thesis.R
- `customer_second_source#0`（customer_second_source｜方向 -｜狀態 ok）：FY2025 10-K 風險因子揭露營收來自有限數量客戶，客戶可能改用其他器官保存方式（冷藏、常溫區域灌流）或減少業務；該段未提及任何客戶導入第二供應商或自製 OCS 的事件。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-24）｜affects：decision_inputs.bear、moat_trend
- `customer_concentration_credit#1`（customer_concentration_credit｜方向 -｜狀態 ok）：風險因素仍揭露營收來自有限數量客戶，失去或大幅減少主要客戶業務將對營收造成重大不利影響。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-24）｜affects：thesis.R、decision_inputs.bear
- `supply_demand_durability#3`（supply_demand_durability｜方向 -｜狀態 ok）：2026 adjusted operating margin outlook cut to 12.5%-14% from ~16% mainly due to accelerated OCS Kidney investment; commentary frames it as capex/execution story
  - 來源：Zacks-based article on TMDX Q2 2026（as_of 2026-07-30）｜affects：thesis.R、decision_inputs.bear
- `supply_demand_durability#5`（supply_demand_durability｜方向 -｜狀態 ok）：Competition/consolidation: Terumo acquired OrganOx for $1.5B (Aug 2025) per a single low-quality market report; no concrete 2026-27 competitor capacity announcements found
  - 來源：Market research report (organ perfusion market)（as_of 2026-01-01）｜affects：moat_trend、decision_inputs.bear
- `regulatory_antitrust#1`（regulatory_antitrust｜方向 -｜狀態 ok）：10-K 風險因子指出歐盟等主管機關對醫療公司與醫療提供者互動的審查加強，調查可能增加成本；屬產業一般性監管風險，非針對 TMDX 的已知調查。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A Risk Factors（as_of 2026-02-24）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：TMDX FY2025 10-K MD&A：進口少部分零組件的關稅使 2025 年營業成本小幅增加。
  - 來源：SEC EDGAR 10-K FY2025 Item 7 MD&A（as_of 2026-02-24）｜affects：valuation、thesis.R
- `reg_tariff_export#1`（reg_tariff_export｜方向 -｜狀態 ok）：10-K 風險因子：美國對中國及他國加徵關稅、貿易限制與出口管制，及他國報復，可能影響供應商與 OCS 產品／飛機零組件價格。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-24）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：FY2025 10-K 揭露 OCS Console 與 Perfusion Set 部分零件向單一來源、少數為唯一來源供應商採購；部分零件為客製、無現成替代，換供應商可能需 FDA 核准設計變更
  - 來源：TransMedics FY2025 Form 10-K (SEC)（as_of 2026-02-27）｜affects：decision_inputs.bear、thesis.R
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：Fresenius Kabi 為 OCS Lung 與 OCS Heart 之 OCS Solutions 單一來源供應商
  - 來源：TransMedics FY2025/FY2023 Form 10-K (SEC)（as_of 2026-02-27）｜affects：decision_inputs.bear、thesis.R
- `geo_supply_chain#2`（geo_supply_chain｜方向 -｜狀態 ok）：OCS Console 與一次性 Perfusion Set 在麻州 Andover 單一廠區設計與組裝；滅菌依賴第三方；FY2025 10-K 稱新總部預計 2028 年 1 月遷入
  - 來源：TransMedics FY2025 Form 10-K (SEC)（as_of 2026-02-27）｜affects：decision_inputs.bear、thesis.R
- `geo_supply_chain#3`（geo_supply_chain｜方向 -｜狀態 ok）：國家器官運送(NOP)依賴第三方私人飛機網絡，供給受美國私人飛機與合格飛行員數量限制，供應商未必優先配合其航班
  - 來源：TransMedics FY2023 ARS (SEC)（as_of 2024-04-01）｜affects：decision_inputs.bear、thesis.R
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：10-K 風險因子：他方可能開發出結果更好、更安全、更易用或更便宜的技術，使 OCS 過時或失去競爭力；許多替代品供應商資源遠大於公司。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-24）｜affects：moat_trend、thesis.R、decision_inputs.bear
- `substitute_technology#1`（substitute_technology｜方向 -｜狀態 ok）：10-K 風險因子：公司須持續向外科醫師、移植中心與支付方證明 OCS 相對冷藏保存（cold storage）或新競爭技術的價值。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-24）｜affects：moat_trend、thesis.R
- `capital_markets_pricing#2`（capital_markets_pricing｜方向 -｜狀態 ok）：Q2 財報後 Piper Sandler 維持 Overweight 但目標價由 $120 降至 $100；MarketBeat 8/5 標題為財報後股價跳空下跌；MarketBeat 後續共識目標價 $124.45（日期不一）。
  - 來源：MarketBeat, TransMedics earns overweight rating from Piper Sandler (2026-08-05)（as_of 2026-08-05）｜affects：valuation、decision_inputs.bear
- `capital_markets_pricing#4`（capital_markets_pricing｜方向 -｜狀態 ok）：Q2 前 Zacks 預估修正趨勢不利，Zacks Rank #5（Strong Sell）；Zacks 共識 FY 營收 $733.24M／EPS $1.82，低於當時指引中點約 2%。Benzinga 顯示放空比例約 38.6% 流通股。
  - 來源：Zacks via Nasdaq, Why Is TransMedics (TMDX) Up 10.2% Since Last Earnings Report?; Benzinga（as_of 2026-09-04）｜affects：valuation、decision_inputs.bear
- `major_events#0`（major_events｜方向 -｜狀態 ok）：證券集體訴訟 Jewik／Collins 已合併，2025-08-08 提出合併修正起訴書，被告 2025-10-07 聲請駁回，法院裁定時間未定（10-K 截至 2026-02-24）
  - 來源：SEC EDGAR 10-K FY2025 Item 3（as_of 2026-02-24）｜affects：thesis.R、decision_inputs.bear
- `lawsuit_class_action#0`（lawsuit_class_action｜方向 -｜狀態 ok）：Jewik v. TransMedics（D. Mass.）證券集體訴訟，class period 2023-02-28 至 2025-01-10；已與 Collins 合併，駁回聲請待裁
  - 來源：SEC EDGAR 10-K FY2025 Item 3（as_of 2026-02-24）｜affects：thesis.R、decision_inputs.bear

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 7 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TMDX_20261108/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":288.0,"bear_5y_price":39.6,"p_bull_pct":25,"p_bear_pct":30,"upside_5y_pct":78.5,"ev5y_pct":75.4,"irr_base_pct":12.3,"asym_ratio":3.4,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":1.51,"pe":58.44,"basis":"FY2026 共識 EPS 1.51 美元（FY1），現價 88.24 美元；終端倍數同樣以當年 EPS 為分母。"},"eps":{"bull":[2.7,4.2,5.8,7.6,9.6],"base":[2.3,3.3,4.3,5.3,6.3],"bear":[1.7,1.9,2.0,2.1,2.2]},"pe":{"bull":30,"base":25,"bear":18},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0,"net_buyback":0},"second_stage":{"bull_cagr_pct":18,"base_cagr_pct":12},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### TMDX_Q2_2026_Earnings_Call_20260804.md
- 2026-08-04｜Waleed Hassanein｜guidance：CEO 提高 2026 全年營收財測下緣至 737–757M 美元、年增 22–25%（原話："$737 million to $757 million, representing 22% to 25%"）
- 2026-08-04｜Waleed Hassanein｜guidance：財測假設不含 PAD Aviation 營收，且不含 ENHANCE Part B／DENOVO 的實質增量營收（原話："assumes no revenue contribution from PAD Aviation"）
- 2026-08-04｜Gerardo Hernandez｜guidance：CFO 說明財測中點的下半年季增型態與過去兩年平均相近（原話："because at the midpoint, it reflects a second half"）
- 2026-08-04｜Gerardo Hernandez｜guidance：全年調整後營業利益率預期（不含 PAD）為 12.5%–14%，先前預期約 16%（原話："adjusted operating margin, excluding the impact of PAD"）
- 2026-08-04｜Gerardo Hernandez｜margin：管理層將營業利益率下修歸因於 OCS Kidney 投入提高（原話："prior expectation primarily reflects the higher planned"）
- 2026-08-04｜Gerardo Hernandez｜guidance：2026 下半年毛利率預期（不含 PAD）約 59%（原話："For the second half of 2026, we expect gross margin"）
- 2026-08-04｜Gerardo Hernandez｜margin：2026 年後毛利率（不含 PAD）預期未來 2–3 年維持現水準，長期約 60%（原話："Looking beyond 2026 and excluding PAD Aviation, we expect"）
- 2026-08-04｜Gerardo Hernandez｜margin：服務毛利率由 Q1 約 27% 升至 Q2 35%，歸因於機隊使用率與效率（原話："approximately 27% in the first quarter of 2026 to 35% in"）
- 2026-08-04｜Gerardo Hernandez｜margin：產品毛利率 77%，與上季大致持平（原話："Product gross margin was 77%, broadly stable sequentially."）
- 2026-08-04｜Gerardo Hernandez｜margin：管理層預期下半年服務毛利率回落但仍高於歷史水準（原話："normalization in service margin during the second half"）
- 2026-08-04｜Gerardo Hernandez｜margin：CFO 在問答中稱 Q3 量下降時服務毛利率無法維持 Q2 水準（原話："goes down, there is no way we can achieve those levels."）
- 2026-08-04｜Gerardo Hernandez｜margin：PAD 初期合併將稀釋毛利率與營業利益率，自第三季起（原話："gross margin and operating margin beginning in the third"）
- 2026-08-04｜Gerardo Hernandez｜margin：新計畫（OCS Kidney、次世代 OCS、ENHANCE／DENOVO）占調整後營業費用年增額約一半、約 1400 萬美元（原話："clinical programs accounted for approximately half of the"）
- 2026-08-04｜Gerardo Hernandez｜guidance：下半年既有業務的調整後營業費用預期與上半年相近，R&D 維持高檔（原話："with the first half, with R&D remaining elevated and SG&A"）
- 2026-08-04｜Waleed Hassanein｜capital_allocation：CEO 重申資本配置優先序：長期營收成長優先於短期營運槓桿（原話："durable top line growth ahead of near-term operating"）
- 2026-08-04｜Waleed Hassanein｜commitment：CEO 表示營業利益率會隨投資節奏逐季波動（原話："margin will vary quarter-to-quarter with the pace of the"）
- 2026-08-04｜Waleed Hassanein｜commitment：CEO 承諾每季回報各成長計畫進度（原話："are equally committed to delivering a strong operating"）
- 2026-08-04｜Waleed Hassanein｜commitment：CEO 預期 CHOPS 納入 ENHANCE 的 IDE 補充於 Q3 末或 Q4 初核准（原話："submitted and is currently under FDA review. We expect it"）
- 2026-08-04｜Waleed Hassanein｜commitment：CEO 設定 OCS Kidney 首次臨床使用時間為 2027 下半年（原話："targeting first clinical experience later in 2027"）
- 2026-08-04｜Waleed Hassanein｜commitment：CEO 說 CHOPS 的 510(k) 現實時程為 2027 上半年（原話："I think realistically speaking, this is H1 2027 horizon for"）
- 2026-08-04｜Waleed Hassanein｜product：CEO 稱 ENHANCE Part B 與 DENOVO 啟動緩慢，目前僅少量病例（原話："We've done a handful of cases in each, nothing really to"）
- 2026-08-04｜Waleed Hassanein｜commitment：CEO 以收案起算 12–18 個月作為試驗完成的關注基準（原話："And again, we're keeping our focus around 12 to 18 months"）
- 2026-08-04｜Waleed Hassanein｜product：CEO 預期心臟業務於 Q4 起隨 ENHANCE Part B 解鎖而加速（原話："And we expect heart to continue to accelerate in the fourth"）
- 2026-08-04｜Waleed Hassanein｜product：自 7/1 新增捐贈者與受贈者臨床篩選協調服務，已簽一家波士頓大型醫療體系做試點（原話："We signed up a major health care system in Boston."）
- 2026-08-04｜Waleed Hassanein｜customer：CEO 描述 Q3 開局強勁但保留，稱 7 月為史上最高航空月（原話："July was the highest aviation month for the business."）
- 2026-08-04｜Waleed Hassanein｜risk：CEO 對 Q3 維持謹慎樂觀，指出 8 月季節性疲弱（原話："So we are cautiously optimistic about"）
- 2026-08-04｜Waleed Hassanein｜competition：CEO 稱服務營收成長主要來自物流市占提升，並稱競爭對手失去大客戶轉到 TMDX（原話："And other vendors reported earlier today that they lost a"）
- 2026-08-04｜Waleed Hassanein｜margin：CEO 稱飛機雙班制改善了利潤率並帶來營運槓桿（原話："The double-shifting gave us significant operating leverage"）
- 2026-08-04｜Waleed Hassanein｜product：物流團隊 Q2 涵蓋需空運 NOP 任務約 86%，Q1 為 82%（原話："On average, we covered approximately 86% of NOP mission"）
- 2026-08-04｜Waleed Hassanein｜customer：CEO 先稱無乾跑增加，後答覆服務營收與產品營收差距可能來自乾跑（原話："potentially dry runs because our team gets deployed and we"）
- 2026-08-04｜Waleed Hassanein｜product：管理層將預期的長期目標寫為 2032 年約 30,000 例移植、年營收逾 20 億美元（原話："support approximately 30,000 transplants by 2032, driving"）
- 2026-08-04｜Waleed Hassanein｜commitment：CEO 說明 2028 年 10,000 例目標以現有心肝肺平台計算，不含 CHOPS、腎臟或 ENHANCE Part B（原話："The 10,000 transplants is on the current platform, heart"）
- 2026-08-04｜Waleed Hassanein｜customer：CEO 在準備稿稱義大利已取得全國性補償（原話："where we have secured national reimbursement for machine"）
- 2026-08-04｜Waleed Hassanein｜customer：問答中 CEO 更正：只在義大利取得預算，並非全歐補償（原話："I said we secured a budget in Italy,"）
- 2026-08-04｜Waleed Hassanein｜risk：德國目前無補償且無 DCD 捐贈，CEO 不視為近期成長催化（原話："it's a complex market, and we are actively engaged there"）
- 2026-08-04｜Waleed Hassanein｜capital_allocation：CEO 稱 PAD 投資與 Summit 不同，需求證明前資本投入不會積極（原話："we are not going to be as bullish in capital deployment"）
- 2026-08-04｜Gerardo Hernandez｜guidance：CFO 未提供 PAD 的任何數字，預計 Q3 提供該年剩餘期間指引（原話："Not yet. I think, as we mentioned, we are not prepared just"）
- 2026-08-04｜Waleed Hassanein｜risk：CEO 表示成長計畫不含成為 OPO，因為該決定為二元結果（原話："everything we discussed today from a growth opportunities"）
- 2026-08-04｜Waleed Hassanein｜risk：CEO 稱 CMS 的 OPO 決定可能延後，且無新進展（原話："CMS may delay the decision point."）
- 2026-08-04｜Gerardo Hernandez｜guidance：CFO 對 2027 營業利益率不給方向，表示 Q4 提供 2027 指引（原話："certainly, in Q4, we will have a better view and"）
- 2026-08-04｜Gerardo Hernandez｜capital_allocation：CFO 稱臨床計畫延後使原 2026 的投資遞延至明年（原話："that those programs are delayed, that investment is going to"）

### 問答異常語氣（迴避／改口／保留）
- TMDX_Q2_2026_Earnings_Call_20260804.md｜問：JPMorgan 問服務營收強勁是否因乾跑增加及 Q3 動態｜答法：先否認曾討論乾跑增加並說到此為止；後續回答 David Rescott 時稱服務與產品差距可能是乾跑
- TMDX_Q2_2026_Earnings_Call_20260804.md｜問：Canaccord 問 FDA 對 ENHANCE／DENOVO IDE 的對話及延遲信心｜答法：拒絕評論 FDA 討論，稱 FDA 掌控時程，改談實際收案病例
- TMDX_Q2_2026_Earnings_Call_20260804.md｜問：William Blair 追問 ENHANCE／DENOVO 試驗完成度｜答法：口誤混用 Part A／Part B 後自行更正，未提供完成百分比，僅稱已做少量病例
- TMDX_Q2_2026_Earnings_Call_20260804.md｜問：William Blair 問義大利補償與歐洲成長是否優於預期｜答法：糾正提問者前提，稱只取得義大利預算而非全歐補償
- TMDX_Q2_2026_Earnings_Call_20260804.md｜問：Evercore 問 PAD 投資規模與對損益的近期影響｜答法：CFO 稱尚無法提供任何數字，延後至 Q3
- TMDX_Q2_2026_Earnings_Call_20260804.md｜問：Jefferies 問 OPO 壓力在 Q2 及下半年影響｜答法：稱無更新、不評論與自身無直接關係的動態，未量化影響
- TMDX_Q2_2026_Earnings_Call_20260804.md｜問：Stifel 追問 2027 營業利益率或 EPS 方向｜答法：CFO 未給數字或方向，只列三項驅動因素，稱 Q4 再給指引

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 3 | 2 |
| customer_second_source | found | 1 | 1 |
| customer_concentration_credit | found | 2 | 0 |
| supply_demand_durability | found | 6 | 4 |
| regulatory_antitrust | found | 2 | 2 |
| reg_tariff_export | found | 3 | 1 |
| geo_supply_chain | found | 4 | 2 |
| end_markets | found | 3 | 2 |
| substitute_technology | found | 3 | 2 |
| channel_business_model_shift | found | 2 | 2 |
| capital_markets_pricing | found | 5 | 4 |
| major_events | found | 4 | 3 |

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260525","verdict":"B 衛星候選等修復 — thesis 完整但 Q1 EPS miss 引發 trap 🟡 + MA ❌→🟠 雙減半；等 Q2 26 EPS recovery + W250 站回 ~$80 連 4 週後可升 A","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"Margin compression（Q1 26 OI margin 7.6% vs FY25 25%+）是 aviation fleet ramp 的 timing 問題不是結構性","columns":{"2Y 驗證":"Q4 26 OI margin 恢復至 ≥15%；FY26 全年 OI margin ≥ 15%","5Y 驗證":"FY28 OI margin ≥ 22%（回到 FY25 水平 + scale economy）","10Y 驗證":"FY30 OI margin ≥ 25%（aviation fleet 規模化後 leverage）","具體門檻":"Q3 26 OI margin ≥ 12% / Q4 ≥ 15% / FY28 ≥ 22%","來源":"Q1 26 earnings call mgmt commentary + Investor presentations","漂移觸發":"連 2 季 OI margin &lt; 10% → 削弱；連 4 季 &lt; 10% → 反轉"}},{"id":"H2","text":"US OCS liver 持續主驅動 + heart/lung 漸進 ramp + 歐洲 PAD Aviation 開出第二曲線","columns":{"2Y 驗證":"FY26 Revenue ≥ $727M（guide low）+ Liver YoY ≥ +25%","5Y 驗證":"FY30 Revenue ≥ $1.2B（含 EU contribution $150M+）","10Y 驗證":"FY35 Revenue ≥ $2B（全球三器官 + ADC ramp）","具體門檻":"FY26 ≥ $727M / FY27 ≥ $880M / FY28 ≥ $1.05B","來源":"FY26 公司 guide + sell-side consensus","漂移觸發":"連 2 季 Liver YoY &lt; +15% → 削弱；FY26 全年 &lt; $700M → 反轉"}},{"id":"H3","text":"OCS NMP 在 US 維持 first-and-only FDA 地位 — XVIVO/HOPE 不進入 US heart/liver 5 年內","columns":{"2Y 驗證":"FDA 觀察 — XVIVO 仍在 EU 階段 + HOPE 仍 limited use；OCS 在 NOP 服務內持續","5Y 驗證":"5 年後可能有 XVIVO 競爭但 OCS 已有 logistics moat（22 架 fleet）保護","10Y 驗證":"10 年後 NMP 平台可能多選但 OCS 仍佔 leadership 因 first-mover","具體門檻":"5 年內無 XVIVO US FDA approval for heart/liver","來源":"FDA 公告 / 競品 IPO/M&A 訊號","漂移觸發":"XVIVO 取得 US Heart/Liver FDA approval → 削弱；NRP guideline 推 OCS 取代 → 反轉 H3"}}]},"R":{"status":"unavailable"},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🟢","ma":"🟠","trap":"🟡","moat_trend":"widening","runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":68.94,"archetype":null,"cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"TMDX","date":"2026-11-08","schema":"v15.0","contract":"v19","company_name":"TransMedics Group, Inc."},"oneliner":"Q3 營收年增 41%，不含 PAD 毛利率 61.1%，成長與利潤都比五月好；但股價已從 68.94 美元漲到 88.24 美元，十月航班轉弱，2027 年利潤率也沒給方向，先等 2 月全年指引再決定進場。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TMDX_20261108/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/TMDX_20261108/scenario.json","answers":{"q1_business":{"verdict":"賺的是每一例移植的耗材費與服務費，錢卡在 OCS 一次性耗材這一節；肝臟占美國移植營收約 81%，是最大的單點依賴。","reasoning":"Q3 營收 2.03 億美元，年增 41%，有機成長 35%。產品 1.134 億美元，年增 29%，毛利率 79.2%；服務 8,960 萬美元，年增 60%，不含 PAD 年增約 43%，毛利率 32.2%，其中物流約 4,100 萬美元。器官別為肝約 1.5 億美元、心約 3,300 萬美元、肺約 200 萬美元，國際 660 萬美元。整體毛利率 58.5%，調整後營業利益率 14.2%，GAAP 13.9%。產業處在擴張期，依據是美國等候名單超過 10.4 萬人、每年約 7,000 人等不到器官，與股價無關。供需持久性判為結構性持久，但 Q3 全美已故捐贈者年減 6%，短期量會跟著捐贈數字波動。單點依賴有三個：肝臟、Fresenius Kabi 單一供應的灌注液、Andover 單一廠區。2023 至 2025 年沒有單一客戶超過營收 10%，集中度不在客戶端。","fact_refs":["f_kpi0_total_revenue_gaap","f_kpi1_non_gaap_operating_incom","f_kpi2_gaap_operating_income_ma","f_kpi4_guidance_fy2026_revenue_","f_kpi5_gross_margin"],"verdict_values":{"revenue_quality":"經常性比例高，每例移植都要用一次性耗材組與服務；但量受已故捐贈者數量與季節影響，合約年限事實表未涵蓋。","unit_econ_note":"Q3 產品毛利率 79.2%，服務毛利率 32.2%；每例收入與成本事實表未涵蓋。","archetype":{"primary":"品質複利成長","secondary":"未獲利高成長","confidence":"中","fingerprint":"每例收費的耗材加服務，已轉盈但仍在投資期，FY2025 才首度產生正 FCF。"},"industry":{"clock_phase":"II","sd_verdict_source":"結構性持久：全球可移植器官長期短缺，美國等候名單超過 10.4 萬人（Transplant International 2026 綜述）；短期量受 Q3 全美捐贈者年減 6% 影響。","bargaining":{"up":"Fresenius Kabi 是 OCS 心肺灌注液單一來源，部分零件為單一來源，換廠可能需要 FDA 核准。","down":"沒有客戶超過營收 10%，議價分散，但移植中心可以逐例選擇保存方式。","geo":"歐洲靠逐區標案進入，義大利只取得預算，德國目前沒有補償。"},"profit_pool_dir":"五年營業利益池資料事實表未涵蓋；公司同時拿器材、服務與物流三段，服務占比上升正在拉低整體毛利率。","tam_table":[{"item":"美國心肺肝移植滲透率（2025）","value":"OCS 5,139 例，約占 26%；肝臟 36%"},{"item":"短保存 DBD 心臟（ENHANCE Part B 目標）","value":"2025 年約 2,200 例，尚無適應症"},{"item":"美國肺移植（DENOVO 目標）","value":"每年約 3,500 例，多數未用機器灌注"},{"item":"美國腎移植（OCS Kidney 目標）","value":"每年約 21,000 顆已移植，另約 9,000 顆未使用；2027 下半年才首例人體"},{"item":"歐洲","value":"管理層稱與美國規模相當；2027 上半年進義大利、荷蘭、比利時"},{"item":"分段年複合成長率與營業利益池占比","value":"事實表未涵蓋"}]}}},"q2_moat":{"verdict":"機制是 OCS 裝置、NOP 取器服務與自有機隊綁成一條服務線；目前仍在拿份額，但對手資本變大，方向判持平。","reasoning":"執行面，Q3 在全美捐贈者年減 6% 下，肝與心案量仍創新高，86% 需空運的任務由自有機隊完成。定價面，服務以調價轉嫁油價，產品毛利率 79.2%，定價力還在；但公司自己推出不同價位的 CHOPS 進入 DBD 心臟與肺。份額方向只有管理層口述，獨立份額數字事實表未涵蓋。對手端，Terumo 買下 OrganOx，XVIVO 心臟產品預期爭取 FDA 核准，執行長在 Q3 法說也說現在是非常擁擠的市場。與直接對手的投入資本報酬差距無法計算，所以方向證據最多支持持平，不標擴大。這個判斷可能錯在肝臟份額實際上比外部證據顯示的更穩。","fact_refs":["f_peer_tmdx_gross_margin_pct","f_peer_tmdx_operating_margin_pct","f_peer_tmdx_fcf_margin_pct","f_peer_abt_operating_margin_pct","f_peer_mdt_operating_margin_pct","f_peer_gkos_operating_margin_pct","f_peer_podd_gross_margin_pct","f_peer_podd_operating_margin_pct"],"verdict_values":{"moat":{"mechanism":"FDA 核准的可攜式多器官溫灌注裝置，加上臨床取器服務與自有機隊，形成每例收費的整合服務。","execution":8,"pricing":7,"grade":"B","trend":"→","trend_evidence":"擴大的證據是 Q3 肝心份額增加，但只有管理層口述；縮減的證據是 Terumo 收購 OrganOx 與 XVIVO 申請核准，尚未反映在營收。兩邊都沒有獨立份額數字，故判持平。","competitor_notes":[{"name":"ABT","strategy_note":"大型多元醫材公司，不在器官保存正面競爭，只作成熟醫材的利潤率參照。"},{"name":"MDT","strategy_note":"成熟醫材規模參照；營業利益率較高反映規模，與移植領域的競爭無關。"},{"name":"GKOS","strategy_note":"成長型醫材參照；研發密度更高且仍為營業虧損，公司在這類成長股裡已先轉盈。"},{"name":"PODD","strategy_note":"耗材型經常性收入的參照；毛利率較高，對照出公司的服務與航空占比拉低毛利。"},{"name":"XVIVO","strategy_note":"直接對手，心臟冷灌注預期爭取 FDA 核准，打的正是 Part B 目標的短保存 DBD 心臟；財務事實表未涵蓋。"},{"name":"Terumo／OrganOx","strategy_note":"肝臟灌注直接對手，母公司資本遠大於公司；併購金額只有單一低品質來源。"}],"peer_na_reason":"對照表四家都不是器官保存的直接對手，直接對手 XVIVO 與 OrganOx 的財務事實表未涵蓋，投入資本報酬差距無法計算。","threats":[{"level":"🔴","text":"Terumo 買下 OrganOx，在肝臟這個核心市場放大對手的銷售與資本。肝臟占美國移植營收約 81%，屬生態層級的攻擊。","p":"35%","evidence_refs":["supply_demand_durability#5"]},{"level":"🟡","text":"XVIVO 心臟冷灌注若獲 FDA 核准，將直接競爭 ENHANCE Part B 的短保存 DBD 心臟區塊，屬單點競爭。","p":"50%","evidence_refs":["competitive_share_entrants#2"]},{"level":"🟡","text":"常溫區域灌流與冷藏是移植中心可以逐例選擇的替代方案；RE-UP 目前據管理層說只有一家中心使用。","p":"30%","evidence_refs":["customer_second_source#0"]},{"level":"🟡","text":"10-K 承認他方可能做出更好或更便宜的技術，公司也要持續向外科醫師與支付方證明 OCS 優於冷藏；目前沒有具體替代產品上市紀錄。","p":"30%","evidence_refs":["competitive_share_entrants#1","substitute_technology#0","substitute_technology#1"]}],"roic_durability":{"quadrant":"事實表未涵蓋投入資本，象限不下結論。","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者是外科醫師，決策者是移植中心，付款端已有既定補償路徑；器官短缺屬結構性，等候名單超過 10.4 萬人。Q3 捐贈者年減 6% 是供給波動，不是需求消失。"},{"item":"決策層級","level":"🟡","text":"替代性發生在每一顆器官與每位外科醫師的選擇上。Q2 法說管理層說有對手的大客戶轉過來，代表客戶換得動，反向也成立；合約年限與流失率事實表未涵蓋。"},{"item":"價值鏈分配","level":"🟡","text":"公司同時拿耗材、服務、物流，產品毛利率 79.2%，服務 32.2%；上游器官由 OPO 掌握，灌注液單一來源，毛利最高的一段又面臨冷藏低價方案。"},{"item":"社會容忍度","level":"🟡","text":"器官移植屬高必要、高敏感領域，CMS 10 月 30 日定案 OPO 認證新規，也更重視運送事件；目前對公司偏中性，但優勢部分依賴監管框架，新 OPO 進入路徑還要再立法程序。"}],"roiic":"事實表未涵蓋（投入資本與折舊攤銷都沒有），不計算。","reinvest_rate":"事實表未涵蓋，不計算。","endo_ceiling":null,"formula_note":"內生成長率等於增量報酬乘再投資率，兩項輸入都缺，不輸出上界。TTM FCF 利潤率 11.82% 接近營業利益率 12.21%，現階段成長投資多走研發費用，資本再投資率本身也難代表成長投入。情境樹保守視為超出上界，熊市機率給 30%。"}}}},"q3_growth":{"verdict":"2025 年三器官滲透率約 26%，加上腎臟與歐洲，五年後仍有成長空間，但第二曲線目前還沒有營收。","reasoning":"成長以量為主，價格次之，併購很小，沒有回購。共識 FY2026 至 FY2028 EPS 年化約 48%，由 1.51 美元到 3.31 美元；FY2027 共識營收只增 16.4%，差距幾乎全靠利潤率擴張。以 FY2025 稀釋 EPS 4.87 美元為基期的三年 CAGR 是負 12.1%，但基期含非營業項目，不能用。EPS 分析師家數事實表未涵蓋，營收 FY1 為 9 家、FY2 為 12 家。內生上界無法計算，缺口歸因於利潤率擴張。滲透率低於 35% 且有 Part B、DENOVO、腎臟三條具名曲線，所以五年後空間判寬；反例是占美國移植營收約 81% 的肝臟 2025 年滲透率已達 36%，新曲線若落空，空間會明顯變窄。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m"],"verdict_values":{"growth":{"driver_mix":"量為主，Q3 案量新高、產品年增 29%；價格次之，服務調價轉嫁油價；併購小，PAD 全年約 1,400 萬美元；沒有回購。","runway_years":"現有三器官平台約 1 到 2 年就到 30% 滲透；加上腎臟與歐洲後超過 10 年，但後者尚無營收證據。","runway_post_y5":"🟢","endo_ceiling_basis":"事實表未涵蓋投入資本與折舊攤銷，增量報酬無法計算；共識成長的缺口歸因於利潤率擴張，保守視為超過內生上界。","segments":[{"item":"產品（Q3）","value":"1.134 億美元，年增 29%，毛利率 79.2%"},{"item":"服務（Q3，含 PAD 940 萬美元）","value":"8,960 萬美元，年增 60%，毛利率 32.2%"},{"item":"物流（Q3，服務內）","value":"約 4,100 萬美元，年增約 50%"},{"item":"美國肝臟（Q3）","value":"約 1.5 億美元"},{"item":"美國心臟（Q3）","value":"約 3,300 萬美元"},{"item":"美國肺臟（Q3）","value":"約 200 萬美元"},{"item":"國際（Q3）","value":"660 萬美元，年增 82%"}],"decay_signals":[{"signal":"毛利率連 2 季年減","status":"未亮","note":"Q3 年減 40 基點，Q2 年比事實表未涵蓋；不含 PAD 為 61.1%，年增 230 基點。"},{"signal":"核心市占近 12 個月縮減","status":"未亮","note":"管理層稱肝心份額增加，沒有獨立數字。"},{"signal":"主力產品提價後銷量下滑","status":"未亮","note":"本包沒有此類證據。"},{"signal":"EPS CAGR 顯著高於營收 CAGR","status":"亮","note":"FY2026 至 FY2028 共識 EPS 年化約 48%，FY2027 營收增 16.4%。"},{"signal":"FCF／淨利連 2 年低於 0.75","status":"亮","note":"FY2024 為負，FY2025 為 0.70；FY2025 淨利含非營業項目，訊號偏機械。"},{"signal":"SBC／營收超過 5% 且逐年上升","status":"資料缺口","note":"Q3 為 6.0%，歷年趨勢事實表未涵蓋。"},{"signal":"TAM 萎縮或被替代技術壓縮","status":"未亮","note":"Q3 捐贈者年減 6% 只有一季。"},{"signal":"產業估值倍數近 3 年系統性下移","status":"資料缺口","note":"事實表未涵蓋。"},{"signal":"維護性資本支出占 FCF 超過 60%","status":"資料缺口","note":"事實表未涵蓋。"},{"signal":"停止投資新產能且收入 3 年內下滑","status":"未亮","note":"公司仍在擴張，營收持續成長。"}],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"資本配置偏弱：沒有回購，SBC 稀釋略超標，資金全壓在研發與臨床，回報要到 2027 年後才看得到。","reasoning":"FY2025 FCF 1.336 億美元，FCF／淨利 0.70，但淨利含非營業項目；TTM FCF 利潤率 11.82%。Q3 SBC 1,210 萬美元，占營收 6.0%，占 GAAP 營業利益 43%。現金 4.93 億美元，含租賃總債務 8.67 億美元，淨負債 3.74 億美元；2026 年利息支出約 2,900 萬美元，其中新總部融資租賃 1,540 萬美元。本包未見回購或配息，錢主要投 OCS Kidney、次世代 OCS、ENHANCE 與 DENOVO，Q3 調整後研發年增 91%。近三年現金去向四分事實表未涵蓋。稀釋均股 4,080 萬股明顯高於流通股 3,473 萬股，差額的組成事實表未涵蓋。","fact_refs":["f_kpi3_sbc","f_net_debt_m","f_shares_diluted_m","f_peer_tmdx_fcf_margin_pct","f_ev_m"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":false,"passed":null,"input":"PAD Aviation 才併入一季，投入金額事實表未涵蓋，沒有已實現報酬可驗。"},{"name":"buyback_yield","applicable":false,"passed":null,"input":"本包未見回購紀錄，管理層的資本配置優先序也沒有回購。"},{"name":"sbc_dilution","applicable":true,"passed":false,"input":"Q3 SBC 1,210 萬美元，年化約 4,840 萬美元，除以市值 30.65 億美元約 1.6%／年，略高於 1.5%，且沒有回購抵銷。"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購支撐，公司也沒有配息或回購紀錄；現金優先投入研發與臨床，三年現金去向事實表未涵蓋。"}}}},"q5_valuation":{"verdict":"現價要賺 10% 年化，FY2031 EPS 要到約 5.7 美元、終端 25 倍；這接近我的基本情境，判合理，不算便宜。","reasoning":"88.24 美元以 10% 年化滾五年是 142 美元，除以 25 倍得 EPS 5.68 美元，約等於 16 億美元營收加 21% 營業利益率。這個條件我部分相信，因為不含 PAD 毛利率已達 61.1%，但 2027 年利潤率沒有方向。短期上檔：FY2028 共識 EPS 3.31 美元乘 33 倍約 109 美元，約 +24%。三年上檔：FY2030 基本情境 EPS 5.30 美元乘 27 倍約 143 美元，約 +62%。賣方目標價在 6 月平均 134 美元，後續約 124.45 美元但日期不一，全距約 70 到 178 美元，最高與最低約 2.5 倍，分歧大，因此下調對報酬不對稱的信心。賣方目標價多數早於 Q3，現價低於均值的幅度只作參考，不作買進理由。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_pe_current","f_pe_percentile","f_ps_current","f_ps_percentile","f_ev_s_current","f_ev_s_fwd","f_ev_m","f_ma_w52","f_ma_w250"],"verdict_values":{"valuation":{"basis":"以 EPS 乘本益比為主。FY1 本益比 58.44 倍，FY2 39.2 倍，trailing 24.04 倍不採用。","tier":"已獲利、仍在投資期的高成長醫材","peers":{"expanded":false,"reason":"事實表只有同業利潤率，沒有同業倍數，也沒有 XVIVO 與 OrganOx 的財務；終端倍數改由自身前瞻倍數與成長放緩推算，列為資料缺口。"},"fwd_pe":58.44,"peg":1.22,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"FY1 本益比 58.44 倍的分母被 2026 年研發高峰壓低，換 FY2 為 39.2 倍。以 FY2026 至 FY2028 共識 EPS 年化 48% 計算，PEG 為 1.22，落在 1 到 2 的合理區，但基期偏低，PEG 偏好看。前瞻 EV／S 為 4.47 倍。五年分位無法計算，事實表只有 2 到 4 個年度端點，現值在端點最低，不能當便宜的證據。","upside_short_pct":24,"upside_mid_pct":62,"denominator_disputed":true,"denominator_note":"FY2025 稀釋 EPS 4.87 美元含非營業項目，淨利 1.903 億美元高於營業利益約 1.086 億美元，差額事實表未拆解，所以 trailing 24 倍不能當便宜證據。改用 FY1 與 FY2 前瞻錨定；FY1 分母被研發壓低，2026-11-07 共識快照也未顯示 Q3 後的修正。"}}},"q6_how_wrong":{"verdict":"最可能看錯三件事：肝臟份額不如管理層講的穩、2027 年利潤率再次讓位給投資、試驗時程繼續往後。","reasoning":"份額增加只有管理層口述，Q3 美國移植營收季增僅 1%。管理層紀錄有落差：Q2 法說執行長對乾跑先否認後又承認可能，對歐洲補償也當場更正；CHOPS 510(k) 從 2027 上半年延到下半年，Part B 的催化從第四季延到 2027 年第一季。財務長在兩次法說之間換人，新任不對 2027 年利潤率給方向。歷史最大回撤、訴訟金額事實表未涵蓋。價值陷阱判中度，依據是兩項衰退信號亮燈，其中一項受 FY2025 非營業項目影響，另有三項資料缺口。","fact_refs":["f_consensus_rev_3m_fy1_pct","f_week26_return_pct","f_rsi14","f_ma_state"],"verdict_values":{"trap":{"verdict":"🟡","label":"中度風險：EPS 增速遠高於營收，FCF 對淨利轉換偏低"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":1.51,"pe":58.44,"basis":"FY2026 共識 EPS 1.51 美元（FY1），現價 88.24 美元；終端倍數同樣以當年 EPS 為分母。"},"eps":{"bull":[2.7,4.2,5.8,7.6,9.6],"base":[2.3,3.3,4.3,5.3,6.3],"bear":[1.7,1.9,2.0,2.1,2.2]},"pe":{"bull":30,"base":25,"bear":18},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0,"net_buyback":0},"second_stage":{"bull_cagr_pct":18,"base_cagr_pct":12},"max_dd":{"lo":-60,"hi":-40,"basis":"深端：熊市路徑 FY2028 EPS 1.9 美元乘 20 倍約 38 美元，約 −57%，終點約 −55%，取整到 −60%。淺端：EPS 不崩，但 FY1 倍數壓到 35 倍，1.51 美元乘 35 倍約 53 美元，約 −40%。歷史最大回撤事實表未涵蓋。","trigger_time":null},"basis":{"bull":"2028 年目標延後一到兩年兌現，Part B、DENOVO 成功，腎臟 2030 年前上市；FY2031 營收約 20 億美元，營業利益率約 28%，股數約 4,400 萬股；30 倍對應當年仍有約 20% 成長。","base":"FY2028 前貼近共識，之後放緩；FY2031 營收約 16 億美元，營業利益率約 23%，股數約 4,300 萬股；25 倍。同業倍數事實表未涵蓋，以自身 FY2 39.2 倍壓縮推算。","bear":"肝臟份額流失、試驗沒有增量、研發維持高檔；FY2031 EPS 2.20 美元，低於 FY2027 共識。18 倍對應成長放緩到 10%，15% 時 22 倍，5% 時 13 倍。機率 30% 的依據是內生上界無法驗證，且 FY1 共識近三個月下修 3.21%；若共識繼續下修，熊市地板也會下移。"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"肝臟占美國移植營收約 81%，Terumo 已買下 OrganOx，執行長也說市場非常擁擠；份額增加只有管理層口述。","assumption":"整合服務足以抵擋大公司用價格與通路攻打肝臟。","consequence":"肝臟失速，FY2031 EPS 約 2.2 美元、18 倍，股價約 40 美元，五年虧約 55%。","ruling":"採納，熊市機率給 30%，與唯一致命條件同一條。","watch":"美國肝臟營收季增率，OPTN 月度移植量。","not_applicable_reason":null,"evidence_refs":["supply_demand_durability#5","competitive_share_entrants#2"]},{"view":"論點成功但股東經濟變差","evidence":"服務占營收升到 44%，毛利率 32.2%；PAD 拉低毛利率 260 基點；CHOPS 定位是不同價位的第二選項；Q3 調整後研發年增 91%；8 月才把全年營業利益率展望由約 16% 下修到 12.5% 至 14%。","assumption":"案量達標後，利潤率會回到管理層的 30% 目標。","consequence":"移植量達標，但 FY2031 營業利益率只有 18%，EPS 約比基本情境少 22%。","ruling":"部分採納，基本情境只用 23%，不採信 30%。產品毛利率 79.2% 部分來自報廢減少，能否持續未證。","watch":"不含 PAD 毛利率、產品毛利率、服務毛利率。","not_applicable_reason":null,"evidence_refs":["supply_demand_durability#3"]},{"view":"價格已反映太多","evidence":"FY1 本益比 58.44 倍，26 週上漲 30%；Q2 後 Piper Sandler 把目標價由 120 美元降到 100 美元；9 月資料顯示 Zacks Rank 5、放空比例約 38.6%；賣方目標價最高與最低約 2.5 倍。","assumption":"FY2028 EPS 3.31 美元會實現，倍數壓縮慢於盈餘成長。","consequence":"若 2 月指引讓 FY2027 EPS 下修 15%，以 30 倍計算約 57 美元，跌約 35%。","ruling":"部分採納。58 倍的分母被壓低，FY2 39.2 倍不算離譜，但賣方分歧大，因此等 2 月指引。","watch":"FY2027 共識 EPS 是否低於 2.25 美元，放空比例變化。","not_applicable_reason":null,"evidence_refs":["capital_markets_pricing#2","capital_markets_pricing#4"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 🟠 → 本次 🟠","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=🟠","side_b":"本次 ma=🟠","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 68.94 → 本次 88.24（+28.0%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=68.94","side_b":"本次 price_at_dd=88.24","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 68.94 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 68.94 美元：五年期望值 前份未列，基準年化 前份未列，前份未列不對稱比","side_b":"本次情境、股價仍用 68.94 美元：Bull 價 288、Bear 價 39.6，五年期望值 +124.5%，基準年化 18.0%，不對稱比 6.22","ruling":"先換情境、股價不動：五年期望值與基準年化前份未列，無法比較。前份未列不對稱比，本次為 6.22。Bull、Bear 價位與股價無關，只受情境影響。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 68.94 美元：五年期望值 +124.5%，基準年化 18.0%，不對稱比 6.22","side_b":"本次情境、股價 88.24 美元：五年期望值 +75.4%，基準年化 12.3%，不對稱比 3.42","ruling":"再換股價、情境不動：起點價上漲 28.0%，五年期望值少 49.1 個百分點，基準年化少 5.7 個百分點，不對稱比由 6.22 降到 3.42。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"護城河方向","cause":"新證據","prior_field":["moat_trend"],"side_a":"前份判擴大：五年內 XVIVO 不會進入美國心肝市場，22 架機隊構成物流護城河。","side_b":"本次判持平：Q3 份額仍增加，但 Terumo 買下 OrganOx，XVIVO 心臟產品爭取 FDA 核准，執行長自稱市場非常擁擠。","ruling":"採持平。份額增加只有管理層口述，對手加碼有外部來源，證據不足以支持擴大。可調和，屬程度差異。","evidence_level":"中：對手面有低品質來源，份額面沒有獨立數字。","settle_metric":"美國肝臟營收季增率；OPTN 肝移植 OCS 使用比例（事實表未涵蓋）。","if_then":["若美國肝臟營收連兩季季增至少 3% 且 XVIVO 心臟未獲核准，方向上修為擴大，部位加碼至 4%。","若美國肝臟營收連兩季季減，清倉。"],"evidence_refs":["supply_demand_durability#5","competitive_share_entrants#2"]},{"axis":"估值結論","cause":"價格變動","prior_field":["val"],"side_a":"前份股價 68.94 美元，估值判便宜（🟢）。","side_b":"本次股價 88.24 美元，FY1 本益比 58.44 倍，FY2 39.2 倍，估值判合理（🟡）。","ruling":"主因是股價上漲 28%；同期 FY1 共識近三個月反而下修 3.21%，盈餘預期沒有跟著變好。","evidence_level":"高：價格與共識都是實際數字。","settle_metric":"FY2027 共識 EPS 與股價的相對變動。","if_then":["若股價在 2 月指引前漲過 100 美元，不追。","若股價跌到 75 美元以下且第四季不含 PAD 營收不低於 1.93 億美元，分批反買。"],"evidence_refs":[]},{"axis":"評級與價值陷阱","cause":"新證據","prior_field":["signal","trap"],"side_a":"前份評級 B、價值陷阱中度，理由是 Q1 EPS 不如預期；升級條件為 Q2 EPS 回升，且股價站回 250 週均線連 4 週。","side_b":"本次維持 B 與中度，理由換成 EPS 增速遠高於營收、FCF 對淨利轉換偏低。Q2 調整後 EPS 0.44 美元低於 0.50 美元共識，Q3 回到 0.51 美元。","ruling":"不升級。Q2 沒有達到前份條件，Q3 轉好只有一季，股價現在高於 250 週均線，但連續週數事實表未涵蓋。","evidence_level":"中","settle_metric":"FY2027 全年調整後營業利益率指引。","if_then":["若指引中點至少 14%，建首倉 2%。","若指引中點低於 12.5%，停止加碼，等試驗收案資料。"],"evidence_refs":[]},{"axis":"前份假設驗證","cause":"新證據","prior_field":null,"side_a":"前份要求 Q3 營業利益率至少 12%，FY2026 至少 15%，FY2026 營收至少 7.27 億美元。","side_b":"Q3 調整後 14.2% 達標，營收指引 7.64 億至 7.74 億美元達標；FY2026 利潤率指引 12.5% 至 14%，低於 15%。","ruling":"利潤率假設部分落空。前份把壓力歸因於機隊擴張的時點，本次改為主動加碼腎臟與試驗投資，並重寫成新的利潤率論點。","evidence_level":"高：公司財報與指引。","settle_metric":"FY2027 調整後營業利益率。","if_then":["若 FY2027 低於 13%，減碼一半。"],"evidence_refs":[]},{"axis":"未填欄位補齊","cause":"方法變動","prior_field":["runway_post_y5","archetype","cycle_position","max_dd_pct","p_bull_pct","p_bear_pct"],"side_a":"前份這些欄位都是空值。","side_b":"本次依現行框架補齊：五年後空間判寬，類型為品質複利成長且信心中等，循環位置不適用，機率與回撤區間見情境樹。","ruling":"屬舊版沒有輸出，不代表看法改變。","evidence_level":"不適用","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"Single Thing 與前份對照","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設定唯一致命點（空值）。","side_b":"美國肝臟營收連兩季季減，同時全美肝移植量沒有同步下降。","ruling":"本次新設 Single Thing。肝臟占美國移植營收約 81%，是數學上最大的單一敏感項。","evidence_level":"中","settle_metric":"每季法說揭露的器官別營收。","if_then":["條件成立即清倉。"],"evidence_refs":[]},{"axis":"減碼與清倉門檻對照","cause":"方法變動","prior_field":["kill_metrics","rearm_trigger"],"side_a":"前份未設 kill_metrics 與 rearm_trigger（空值），結論只寫「等 Q2 26 EPS recovery + W250 站回 ~$80 連 4 週後可升 A」。","side_b":"美國肝臟營收連 2 季季減即清倉；TTM 調整後營業利益率低於 12% 連 2 季即減碼一半；重新進場條件為 2027 年全年調整後營業利益率指引中點至少 14%。","ruling":"舊條件以股價與單季 EPS 為主，新條件改看肝臟與利潤率，因為論點的敏感度集中在這兩項。","evidence_level":"中","settle_metric":"美國肝臟營收；調整後營業利益率。","if_then":["條件未觸發前，不因股價波動減碼。"],"evidence_refs":[]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"現在就買：有機成長 35%，不含 PAD 毛利率 61.1%，FY2 本益比 39.2 倍，放空比例高，試驗 2027 年第一季啟動；等到 2 月可能錯過重估。","side_b":"等 2 月：十月航班下降是管理層親口承認，第四季隱含營收要季增，FY2027 利潤率沒有方向，也是新財務長第一份全年指引。","ruling":"選等。基本情境年化約 12%，多等三個月的成本小；十月疲軟的消息未滿一季，且 11-07 共識快照沒有變動，尚不能確定已進賣方模型。可調和，屬時點差異。","evidence_level":"中","settle_metric":"2027 年 2 月財報的全年利潤率指引。","if_then":["若股價先漲過 100 美元而指引未出，不追。","若股價跌到 75 美元以下而第四季不含 PAD 營收不低於 1.93 億美元，分批反買。","若指引中點至少 14%，即使股價已上漲，也重跑研究後建首倉 2%。"],"evidence_refs":["capital_markets_pricing#4"]},{"axis":"2028 年目標可信度","cause":null,"prior_field":null,"side_a":"管理層在 Q2 重申，2028 年約 10,000 例、營收 12 億美元、營業利益率 30%。","side_b":"共識 FY2028 EPS 只有 3.31 美元；Q3 法說沒有重申這組數字，財務長也不給 2027 年利潤率方向。","ruling":"站共識這邊。2026 年指引只有 12.5% 至 14%，要兩年翻倍以上，沒有數據支持。基本情境 FY2028 EPS 用 3.30 美元。可調和，屬程度差異。","evidence_level":"中","settle_metric":"FY2027 調整後營業利益率。","if_then":["若 FY2027 至少 18%，上調基本情境並加碼至 4%。","若 FY2027 低於 13%，下修基本情境並減碼一半。"],"evidence_refs":[]},{"axis":"服務增速與案量的落差","cause":null,"prior_field":null,"side_a":"服務營收不含 PAD 年增約 43%，管理層歸因於 NOP 採用、份額與調價。","side_b":"產品年增 29%、季增 2%，美國移植營收季增 1%；2026-08-04 法說，執行長先否認乾跑增加，後來又說差距可能來自乾跑。","ruling":"未證、監測。預登記：不含 PAD 的服務增速連 3 季高於產品增速 10 個百分點以上，且公司未拆解案量與價格，就判定服務成長品質不足。","evidence_level":"低：公司未揭露案量與乾跑。","settle_metric":"不含 PAD 服務增速減產品增速；年度案量。","if_then":["條件成立時，FY2027 基本情境營收下修 5%，停止加碼。"],"evidence_refs":[]},{"axis":"試驗與核准時程滑動","cause":null,"prior_field":null,"side_a":"2026-08-04 法說，Waleed Hassanein：CHOPS 510(k) 現實時程是 2027 上半年，心臟預期第四季起隨 Part B 解鎖而加速。","side_b":"2026-11-05 法說，Waleed Hassanein：510(k) 目標改為 2027 下半年，Part B 與 DENOVO 催化延到 2027 年第一季，第四季指引不計入。","ruling":"管理層時程要打折，基本情境不放早於 2027 下半年的試驗增量營收。試驗讀數今天不存在，收案起算 12 到 18 個月，不可裁決至 2028 年。","evidence_level":"高：兩次法說原話。","settle_metric":"2027-03-31 前兩試驗是否開始收案；2027 年底前 510(k) 是否取得。","if_then":["若任一試驗到 2027-03-31 仍未收案，停止加碼。","若兩項里程碑都達成，維持原路徑。"],"evidence_refs":[]},{"axis":"第四季量能","cause":null,"prior_field":null,"side_a":"執行長：十月只是幾週疲軟，第四季後半通常明顯回升，車輛運送也在增加。","side_b":"Stifel 分析師：十月航班加上 11 至 12 月的季節性，案量可能季減，而不含 PAD 第四季隱含營收約 1.98 億美元。","ruling":"不可裁決至 2 月，凍結建倉到第四季財報。指引區間寬度隱含下緣約 1.93 億美元。","evidence_level":"中","settle_metric":"第四季不含 PAD 營收。","if_then":["若低於 1.93 億美元，不追，延到 2027 年 5 月財報再判斷。"],"evidence_refs":[]},{"axis":"PAD 毛利率稀釋","cause":null,"prior_field":null,"side_a":"財務長：PAD 拉低毛利率 260 基點，整合後會改善。","side_b":"PAD 併入才一季，改善沒有資料；Q3 服務毛利率 32.2% 已低於 Q2 的 35%，財務長也預告第四季回落。","ruling":"未證、監測。預登記：連 3 季 PAD 稀釋仍至少 200 基點，整合改善的說法視為不成立。","evidence_level":"低","settle_metric":"含與不含 PAD 的毛利率差距。","if_then":["條件成立時，基本情境毛利率假設下修 1 個百分點，停止加碼。"],"evidence_refs":[]},{"axis":"產業態勢三軸","cause":null,"prior_field":null,"side_a":"競爭惡化：Terumo 買下 OrganOx，XVIVO 爭取心臟核准，管理層也稱市場擁擠。","side_b":"結構轉好：器官短缺屬結構性，HHS 腎臟計畫要多做約 2,000 顆腎移植，CMS 更重視運送事件，對垂直整合有利。","ruling":"雙向拉鋸。其他結構變數是 10 月 30 日定案的 OPO 認證規則，短期交接對捐贈量的影響尚未量化。","evidence_level":"中","settle_metric":"全美已故捐贈者量；美國肝臟營收。","if_then":["若全美已故捐贈者量連 4 季年減，停止加碼。"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"2 月全年利潤率指引達標才開始建倉","type":"估值rearm","maps_to":"H1","metric":"FY2027 調整後營業利益率指引中點","threshold":"至少 14%","action":"重跑研究後建首倉 2%","source_freq":"8-K 與法說，每季","date":"2027-02","evidence_refs":["supply_demand_durability#3"]},{"n":2,"text":"第四季量能低於指引下緣","type":"風險","maps_to":"R2","metric":"第四季不含 PAD 營收","threshold":"低於 1.93 億美元","action":"不追，延到 2027 年 5 月財報判斷","source_freq":"8-K，每季","date":"2027-02","evidence_refs":[]},{"n":3,"text":"兩項試驗要在第一季底前開始收案","type":"假設驗證","maps_to":"H3","metric":"ENHANCE Part B 與 DENOVO 收案狀態","threshold":"2027-03-31 前兩項都開始收案","action":"未達成則停止加碼","source_freq":"法說，每季","date":"2027-03","evidence_refs":[]},{"n":4,"text":"肝臟營收失速","type":"Single Thing","maps_to":"Single Thing","metric":"美國肝臟營收","threshold":"連 2 季季減，且全美肝移植量未同步下降","action":"清倉","source_freq":"法說，每季；OPTN 每月","date":null,"evidence_refs":["customer_concentration_credit#1"]},{"n":5,"text":"XVIVO 心臟產品取得 FDA 核准","type":"風險","maps_to":"R3","metric":"FDA 核准公告","threshold":"取得核准","action":"停止加碼，直到兩季心臟營收確認未受影響","source_freq":"FDA 公告，不定期","date":"2026-Q4","evidence_refs":["competitive_share_entrants#2"]},{"n":6,"text":"利潤率與收案同時達標","type":"加碼","maps_to":"H1","metric":"TTM 調整後營業利益率；兩試驗累計收案","threshold":"至少 16%，且累計收案至少 300 例","action":"加碼至 4%","source_freq":"8-K 與法說，每季","date":"2027-12","evidence_refs":[]},{"n":7,"text":"利潤率持續低於門檻","type":"減碼","maps_to":"R1","metric":"TTM 調整後營業利益率","threshold":"低於 12% 連 2 季","action":"減碼一半","source_freq":"8-K，每季","date":null,"evidence_refs":["supply_demand_durability#3"]},{"n":8,"text":"集體訴訟不利進展","type":"減碼","maps_to":"R5","metric":"證券集體訴訟程序","threshold":"獲集體認證且出現不利和解","action":"減碼一半","source_freq":"10-Q 與 10-K，每季","date":null,"evidence_refs":["lawsuit_class_action#0","major_events#0"]},{"n":9,"text":"刑事介入或核心產品被迫停售","type":"清倉","maps_to":"R5","metric":"刑事調查；FDA 對 OCS Liver 的停售措施","threshold":"任一發生","action":"清倉","source_freq":"8-K 與 FDA 公告，不定期","date":null,"evidence_refs":["lawsuit_class_action#0"]},{"n":10,"text":"供應或關稅壓力侵蝕產品毛利率","type":"風險","maps_to":"R6","metric":"產品毛利率","threshold":"低於 75% 連 2 季","action":"停止加碼","source_freq":"法說，每季","date":null,"evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","geo_supply_chain#0","geo_supply_chain#1","geo_supply_chain#2","geo_supply_chain#3"]},{"n":11,"text":"捐贈者量持續下滑","type":"風險","maps_to":"R7","metric":"全美已故捐贈者量","threshold":"連 4 季年減","action":"停止加碼","source_freq":"OPTN，每月","date":null,"evidence_refs":[]},{"n":12,"text":"第四季財報後複審","type":"複審日期","maps_to":"H1","metric":"全年指引與第四季實績","threshold":"財報公布後一週內","action":"依重新進場條件決定建倉或繼續不追","source_freq":"一次性","date":"2027-02-28","evidence_refs":[]}],"kill_metrics":[{"metric":"美國肝臟營收","bear_threshold":"連 2 季季減，且全美肝移植量未同步下降","window":"2 季","source":"公司法說的器官別營收","last_status":"ok"},{"metric":"TTM 調整後營業利益率","bear_threshold":"低於 12% 連 2 季","window":"2 季","source":"公司 8-K","last_status":"warning"},{"metric":"產品毛利率","bear_threshold":"低於 75% 連 2 季","window":"2 季","source":"公司法說","last_status":"ok"},{"metric":"ENHANCE Part B 與 DENOVO 開始收案","bear_threshold":"2027-03-31 前任一未開始","window":"至 2027-03-31","source":"公司法說","last_status":"warning"},{"metric":"全美已故捐贈者量","bear_threshold":"連 4 季年減","window":"4 季","source":"OPTN 月度資料","last_status":"warning"}],"evidence_dismissed":[{"ref":"regulatory_antitrust#1","reason":"該段是 10-K 的一般性產業語句，沒有指向公司的調查、金額或時點，也無法建立可監測的門檻。"}],"action_conditions":{"rearm_trigger":"2027 年 2 月公布的全年調整後營業利益率指引中點至少 14%","exec_line":"現價不追；2 月財報後條件達成，重跑研究並建首倉 2%；利潤率與試驗收案都達標再加到 4%。"}},"decision_inputs":{"signal":"B","ma":"🟠","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場用十月航班與被研發壓低的 2026 年利潤率定價，沒有反映不含 PAD 毛利率 61.1% 與 2027 年第一季啟動的兩項試驗；但這個落差要等全年指引與實際收案才會收斂。","momentum_overheated":null,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等 2027 年 2 月第四季財報與全年指引，調整後營業利益率指引中點至少 14% 才建倉；現價不追。","asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null},"thesis":{"H":[{"id":"H1","text":"2026 年利潤率下修是公司主動加碼研發的選擇，毛利結構沒有變差，2027 年起營業槓桿會回來。","2y":"FY2028 調整後營業利益率至少 19%","5y":"FY2031 調整後營業利益率至少 23%","10y":null,"threshold":"FY2027 至少 14%；FY2028 至少 19%；不含 PAD 毛利率至少 60%","source":"公司 8-K 與法說，每季","drift_rule":"TTM 調整後營業利益率對照路徑，連 2 季偏離至少 5% 為削弱，連 3 季偏離至少 10% 為反轉。"},{"id":"H2","text":"現有心肝肺平台靠份額與服務滲透，即使全美捐贈者下滑，案量仍能維持高成長。","2y":"FY2028 美國案量至少 8,500 例，營收至少 10.4 億美元","5y":"FY2031 營收至少 16 億美元","10y":null,"threshold":"FY2026 營收至少 7.64 億美元；FY2027 至少 8.95 億美元；FY2028 至少 10.4 億美元","source":"公司 8-K 與法說，OPTN 月度資料","drift_rule":"TTM 營收對照路徑，連 2 季偏離至少 5% 為削弱，連 3 季偏離至少 10% 為反轉。"},{"id":"H3","text":"Part B、DENOVO、腎臟與歐洲會成為第二條成長曲線，讓成長延續到五年以後。","2y":"兩試驗 2027-03-31 前開始收案，2027 年底累計至少 300 例，CHOPS 510(k) 於 2027 年底前取得","5y":"FY2031 心、肺、腎與國際合計占營收至少 35%","10y":"腎臟占營收至少 25%","threshold":"合計 1,050 例收案，18 個月內完成一半以上；OCS Kidney 於 2027 下半年完成首例人體","source":"公司法說與 FDA 公告；試驗登記資料事實表未涵蓋","drift_rule":"里程碑延誤一季為削弱，延誤兩季以上為反轉；占營收比連 4 季偏離至少 5% 為削弱，連 6 季偏離至少 10% 為反轉。"}],"R":[{"id":"R1","text":"2027 年全年指引給不出利潤率擴張。財務長不給方向，研發至少維持幾季，Part B 與 DENOVO 費用還沒完全進來，賣方卻模型化擴張。","h_ref":"H1","clock":"⚡","threshold":"FY2027 調整後營業利益率指引中點低於 14%","evidence_refs":["supply_demand_durability#3"]},{"id":"R2","text":"第四季量能不如指引隱含。管理層承認十月航班下降，不含 PAD 第四季隱含營收約 1.98 億美元。","h_ref":"H2","clock":"⚡","threshold":"第四季不含 PAD 營收低於 1.93 億美元","evidence_refs":[]},{"id":"R3","text":"肝臟競爭加劇，移植中心逐例改用其他保存方式，大客戶的使用量也可能下降。","h_ref":"H2","clock":"🔥","threshold":"美國肝臟營收連 2 季季減","evidence_refs":["customer_concentration_credit#1"]},{"id":"R4","text":"試驗與核准時程繼續往後。CHOPS 510(k) 已由 2027 上半年延到下半年，Part B 催化已由第四季延到 2027 年第一季。","h_ref":"H3","clock":"🔥","threshold":"2027-03-31 前任一試驗未開始收案，或 2027 年底前 CHOPS 510(k) 未取得","evidence_refs":[]},{"id":"R5","text":"管理層與揭露可信度。CFO 在 2026-08-04 與 2026-11-05 兩次法說之間由 Gerardo Hernandez 換成 Fernando Araujo，原因本包未涵蓋；Q2 法說對乾跑與義大利補償都曾改口；證券集體訴訟駁回聲請待裁，訴訟金額事實表未涵蓋。","h_ref":"H1","clock":"🔥","threshold":"CEO 或 CFO 再異動；駁回聲請遭否且獲集體認證；出現刑事或 SEC 調查","evidence_refs":["major_events#0","lawsuit_class_action#0"]},{"id":"R6","text":"供應單點與關稅。部分零件與灌注液單一來源，Andover 單一廠區，第三方滅菌與飛機網路都有依賴；關稅已小幅墊高成本。","h_ref":"H1","clock":"🔥","threshold":"產品毛利率連 2 季低於 75%，或單一供應中斷造成停產超過 30 天","evidence_refs":["geo_supply_chain#0","geo_supply_chain#1","geo_supply_chain#2","geo_supply_chain#3","reg_tariff_export#0","reg_tariff_export#1"]},{"id":"R7","text":"OPO 制度改革造成交接混亂，全美捐贈量持續下滑，Q3 已年減 6%。","h_ref":"H2","clock":"🐢","threshold":"全美已故捐贈者量連 4 季年減","evidence_refs":[]}],"single_thing":{"description":"美國肝臟營收（Q3 約 1.5 億美元）連兩季季減，同時全美肝移植量沒有同步下降。","why_fatal":"肝臟占美國移植營收約 81%，研發與試驗資金幾乎都靠它；肝臟失速後，營收與營業槓桿會同時失去，FY2028 共識 EPS 3.31 美元站不住。","if_happens":"清倉，等肝臟營收連兩季回穩才重跑研究。","how_monitor":"每季法說揭露的器官別營收；OPTN 每月移植與航班資料作領先指標。","probability":"12 到 24 個月約 20%，依據是 Terumo／OrganOx 在肝臟正面競爭，份額只有管理層口述，Q3 美國移植營收季增僅 1%。"}},"appendix_a":{"growth_durability":7,"quality_score":6,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":39.22,"peg_fy2":0.83,"stress":{"pass":null,"total":null}},"eps_meta":{"base_eps_path":{"FY2025A":4.87,"FY2026E":1.51,"FY2027E":2.25,"FY2028E":3.31},"fy_end_month":12,"eps_basis":"共識取自 2026-11-07 Koyfin 快照，會計口徑事實表未標明；FY2025A 4.87 美元為 GAAP 稀釋 EPS，含非營業項目，淨利 1.903 億美元高於營業利益約 1.086 億美元，差額事實表未拆解，不適合當成長基期。"},"catalysts":[{"date":"2026-Q4","date_precision":"quarter","type":"regulatory","event":"XVIVO 心臟冷灌注 FDA 核准進度","impact":"中","watch":"是否取得核准，以及是否影響 Part B 收案。"},{"date":"2027-02","date_precision":"month","type":"guidance","event":"第四季財報與 2027 年全年指引，新財務長第一份全年指引","impact":"高","watch":"調整後營業利益率指引中點是否至少 14%，第四季不含 PAD 營收是否至少 1.93 億美元。"},{"date":"2027-Q1","date_precision":"quarter","type":"regulatory","event":"ENHANCE Part B 與 DENOVO 開始收案","impact":"高","watch":"2027-03-31 前兩項是否都開始收案。"},{"date":"2027-Q2","date_precision":"quarter","type":"product","event":"上半年在義大利、荷蘭、比利時推出 OCS 與 NOP","impact":"中","watch":"標案數量與國際營收成長。"},{"date":"2027-Q4","date_precision":"quarter","type":"regulatory","event":"下半年目標取得 CHOPS 510(k)","impact":"中","watch":"時程是否再延後，以及定價。"},{"date":"2027-Q4","date_precision":"quarter","type":"product","event":"下半年 OCS Kidney 首例人體使用","impact":"高","watch":"是否如期完成，以及試驗設計與對照組。"}],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8(val爭議)","pacing":[],"holding_cap":"中期 2-5 年","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟠'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"輸入缺(momentum_overheated=null)，依保守方向處理：不視為觸發","input_gap":["momentum_overheated"]},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場用十月航班與被研發壓低的 2026 年利潤率定價，沒有反映不含 PAD 毛利率 61.1% 與 2027 年第一季啟動的兩項試驗；但這個落差要等全年指引與實際收案才會收斂。"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":true,"basis":"capalloc_grade='C'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟢', val='🟡', moat_trend='→', week26=30.07, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position=None, moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈機械讀數判定不可用，baseline rows 8/9/9b/10 的估值條件視為不可判 → 落 row8 觀望（保守方向）","hit":true,"basis":"val_denominator_disputed=True, val(機械讀數)='🟡'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"requires_critic":[]}}
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
