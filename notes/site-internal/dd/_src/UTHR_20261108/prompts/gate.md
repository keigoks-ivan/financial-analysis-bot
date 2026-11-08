你是 DD 管線 v20 的判斷層閘（gate），標的 UTHR（20261108）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（37 條）
- `f_kpi0_gaap`（q1_business）｜營收（GAAP）＝832.5 百萬美元｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 8-K Ex.99.1（numbers.latest_quarter_kpis.items[0]，as_of Q3 2026（季末 2026-09-30，公告於 2026-11-04））
  - 註記：未取得營收共識
- `f_kpi1_gaap`（q1_business）｜GAAP 營業利益＝307.8 百萬美元｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 8-K Ex.99.1（numbers.latest_quarter_kpis.items[1]，as_of Q3 2026（季末 2026-09-30，公告於 2026-11-04））
  - 註記：未取得
- `f_kpi2_gaap`（q1_business）｜GAAP 營業利益率＝37.0 %｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：由新聞稿 307.8/832.5 計算（numbers.latest_quarter_kpis.items[2]，as_of Q3 2026（季末 2026-09-30，公告於 2026-11-04））
  - 註記：未取得
- `f_kpi5_tyvaso`（q1_business）｜Tyvaso 總營收＝503.8 百萬美元｜期間與口徑：Q3 2026（公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 8-K Ex.99.1（numbers.latest_quarter_kpis.items[5]，as_of Q3 2026（公告於 2026-11-04））
  - 註記：不適用
- `f_kpi6_orenitram_remodulin_unit`（q1_business）｜Orenitram／Remodulin／Unituxin 營收＝145.0／122.0／52.3 百萬美元｜期間與口徑：Q3 2026（公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 8-K Ex.99.1（numbers.latest_quarter_kpis.items[6]，as_of Q3 2026（公告於 2026-11-04））
  - 註記：不適用
- `f_peer_uthr_gross_margin_pct`（q2_moat）｜UTHR 毛利率＝86.34 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.UTHR.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_uthr_operating_margin_pct`（q2_moat）｜UTHR 營業利益率＝39.39 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.UTHR.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_uthr_fcf_margin_pct`（q2_moat）｜UTHR FCF 利潤率＝27.21 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.UTHR.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_lqda_gross_margin_pct`（q2_moat）｜LQDA 毛利率＝92.54 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.LQDA.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_lqda_operating_margin_pct`（q2_moat）｜LQDA 營業利益率＝37.39 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.LQDA.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_lqda_fcf_margin_pct`（q2_moat）｜LQDA FCF 利潤率＝32.75 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.LQDA.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_jazz_operating_margin_pct`（q2_moat）｜JAZZ 營業利益率＝24.04 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.JAZZ.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_mrk_operating_margin_pct`（q2_moat）｜MRK 營業利益率＝9.2 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MRK.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_insm_operating_margin_pct`（q2_moat）｜INSM 營業利益率＝-41.66 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.INSM.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝28.02 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_largecap_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-11-07）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝33.89 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_largecap_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-11-07）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝42.41 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_largecap_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-11-07）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝3248.5 USD m｜期間與口徑：2026-11-08／yfinance revenue_estimate 0y 平均（13 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝3602.15 USD m｜期間與口徑：2026-11-08／yfinance revenue_estimate +1y 平均（14 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi4_sbc`（q4_capital）｜SBC 占營收＝4.9 %｜期間與口徑：Q3 2026（公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：新聞稿 SBC 41.0 百萬／營收 832.5 計算；占 GAAP 營業利益 13.3%（numbers.latest_quarter_kpis.items[4]，as_of Q3 2026（公告於 2026-11-04））
  - 註記：不適用
- `f_kpi7`（q1_business）｜現金與可交易投資＝3535.7 百萬美元｜期間與口徑：Q3 2026（2026-09-30）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 8-K Ex.99.1（numbers.latest_quarter_kpis.items[7]，as_of Q3 2026（2026-09-30））
  - 註記：不適用
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝-2067.9 USD m｜期間與口徑：2026-11-08／yfinance 最新一季：總債務 0.0、現金 2067.9（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝42.59 m shares｜期間與口徑：2026-11-08／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝562.02 USD｜期間與口徑：2026-11-06（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-11-06（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝20.06 x｜期間與口徑：2026-11-07／分母＝FY1 EPS 28.02，分子＝快照價 562.02｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-11-07）
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝21.22 x｜期間與口徑：2026-11-06（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-11-06（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝100.0 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝7.51 x｜期間與口徑：2026-11-06（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝100.0 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝6.86 x｜期間與口徑：2026-11-06（RTH 收盤，UTC）／4 個年度端點內的分位＝94.4｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝94.4 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ev_m`（q5_valuation）｜目前企業價值 EV（市值＋淨負債）＝21867.82 USD m｜期間與口徑：2026-11-08／市值 23935.72 ＋ 淨負債 -2067.9｜kind：realized
  - 來源：—（numbers.capital_structure.ev_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_consensus_rev_fy1_pct`（q5_valuation）｜FY1 共識修正＝0.0 %｜期間與口徑：2026-11-07／兩份 Koyfin 快照之間的 EPS 修正幅度（28.02 → 28.02）｜kind：estimate
  - 來源：DD_largecap_EPS_estimates_20261107.xlsx（numbers.consensus_revision.fy1.revision_pct，as_of 2026-11-07）
- `f_consensus_rev_fy2_pct`（q5_valuation）｜FY2 共識修正＝0.0 %｜期間與口徑：2026-11-07／兩份 Koyfin 快照之間的 EPS 修正幅度（33.89 → 33.89）｜kind：estimate
  - 來源：DD_largecap_EPS_estimates_20261107.xlsx（numbers.consensus_revision.fy2.revision_pct，as_of 2026-11-07）
- `f_consensus_rev_fy3_pct`（q5_valuation）｜FY3 共識修正＝0.0 %｜期間與口徑：2026-11-07／兩份 Koyfin 快照之間的 EPS 修正幅度（42.41 → 42.41）｜kind：estimate
  - 來源：DD_largecap_EPS_estimates_20261107.xlsx（numbers.consensus_revision.fy3.revision_pct，as_of 2026-11-07）
- `f_kpi3_gaap_eps`（q4_capital）｜GAAP 稀釋 EPS＝5.71 美元｜期間與口徑：Q3 2026（公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 8-K Ex.99.1（numbers.latest_quarter_kpis.items[3]，as_of Q3 2026（公告於 2026-11-04））
  - 註記：consensus 5.85（二手來源 Earnings Whispers，經 web_search，未對照一手），低於 2.4%
- `f_ma_w104`（q5_valuation）｜104 週均線＝433.3 USD｜期間與口徑：2026-11-08／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）

### findings_digest 中方向為負或來源衝突的條目（15 條）
- `competitive_share_entrants#0`（competitive_share_entrants｜方向 -｜狀態 ok）：Liquidia 的 Yutrepia 於 2025 年 6 月在美國上市，與 UTHR 的 treprostinil 產品競爭；Merck Winrevair 2024 年 3 月上市；Insmed TPIP 處於後期臨床。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-25）｜affects：moat_trend、decision_inputs.bear
- `competitive_share_entrants#3`（competitive_share_entrants｜方向 -｜狀態 ok）：第三方分析指 2026 上半年霧化 Tyvaso 營收下滑 20%，並稱 Winrevair 與 Yutrepia 使 PAH 格局更艱難（二手摘要，未核對公司原始財報）。
  - 來源：Panabee, United Therapeutics Q2 Earnings (2026-08-05)（as_of 2026-08-05）｜affects：moat_trend、decision_inputs.bear
- `customer_concentration_credit#0`（customer_concentration_credit｜方向 -｜狀態 ok）：FY2025 10-K 披露：應收帳款集中在少數主要客戶；若客戶不履約，最大損失曝險等於資產負債表帳面金額（未於此段列出客戶占比數字）。
  - 來源：SEC EDGAR 10-K FY2025 Item 8（as_of 2026-02-25）｜affects：thesis.R、decision_inputs.bear
- `customer_concentration_credit#1`（customer_concentration_credit｜方向 -｜狀態 ok）：聚合站稱 UTHR 美國 treprostinil 經 Accredo 與 CVS Specialty 兩家經銷，約占總營收 51% 與 36%（未核一手）
  - 來源：policyrisk.com UTHR 公司頁（as_of 2026-02-25）｜affects：thesis.R、decision_inputs.bear
- `supply_demand_durability#1`（supply_demand_durability｜方向 -｜狀態 ok）：10-Q states competition from large pharma PAH products has adversely affected treprostinil sales; Yutrepia (Liquidia) approved May 2025; settlement requires Liquidia to remove PH-ILD indication from label (搜尋摘要轉述)
  - 來源：UTHR Form 10-Q FY2026（as_of 2026-09-30）｜affects：moat_trend、decision_inputs.bear
- `supply_demand_durability#3`（supply_demand_durability｜方向 -｜狀態 ok）：Prior filings: Watson/Actavis generic Tyvaso may enter US from Jan 2026; generic Orenitram from June 2027 (Actavis) / Dec 2027 (ANI) (搜尋摘要轉述；2026年實際是否上市未證實)
  - 來源：UTHR Form 10-K FY2023（as_of 2024-02-28）｜affects：moat_trend、decision_inputs.bear、triggers
- `regulatory_antitrust#0`（regulatory_antitrust｜方向 -｜狀態 ok）：10-K 風險因素：專利和解（允許 Remodulin、Tyvaso 霧化、Orenitram 學名藥上市）可能引發 FTC 或私人反壟斷主張；公司遭 Sandoz 控違反和解協議，已提列 7,410 萬美元負債。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-25）｜affects：thesis.R、decision_inputs.bear
- `regulatory_antitrust#1`（regulatory_antitrust｜方向 -｜狀態 ok）：10-K 風險因素：公司曾遭 DOJ 調查其對非營利病患援助計畫的捐助，並被 Humana、UnitedHealth、MSP Recovery 以 RICO 等提告。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-25）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：FY2025 10-K 風險因素：關稅可能推高原料與耗材成本與建廠材料成本，使銷貨成本年增高於平均；政府並威脅對未採 MFN 定價的藥廠課重稅，多家藥廠已簽保密定價協議。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-25）｜affects：decision_inputs.bear、thesis.R
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：依賴第三方供應 Remodulin 輸注泵浦，可用泵浦數量有限，且有廠商停產某型號泵浦
  - 來源：UNITED THERAPEUTICS Corp Form 10-K FY2024（as_of 2025-02-26）｜affects：thesis.R、decision_inputs.bear
- `end_markets#1`（end_markets｜方向 -｜狀態 ok）：公司稱競爭療法對 Q3 2026 霧化 Tyvaso、Tyvaso DPI、Remodulin 銷售有負面影響；前九個月 Tyvaso 合計持平 $1,413.9M，Orenitram +約8% 至 $406.3M，Remodulin -6% 至 $374.9M
  - 來源：UTHR 10-Q FY2026 (quarter ended 2026-09-30)（as_of 2026-10-29）｜affects：moat_trend、decision_inputs.bear
- `end_markets#3`（end_markets｜方向 -｜狀態 ok）：Remodulin 美國學名藥侵蝕有限；國際 Remodulin 營收因競爭與合約移轉價下調而減少；Liquidia Yutrepia 2025年6月上市直接與公司 treprostinil 產品競爭；公司調價通常為單位數百分比
  - 來源：UTHR 10-Q FY2026 (quarter ended 2026-09-30)（as_of 2026-10-29）｜affects：moat_trend、decision_inputs.bear
- `substitute_technology#1`（substitute_technology｜方向 -｜狀態 ok）：10-K 風險因子：付款方可能要求自動學名藥替代或階梯療法（先試學名藥），使公司產品較難取得給付。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-25）｜affects：decision_inputs.bear、thesis.R
- `substitute_technology#2`（substitute_technology｜方向 -｜狀態 ok）：10-Q（截至2026-09-30）稱 Winrevair、Yutrepia 等競品已影響 treprostinil 銷售；Insmed TPIP 為後期候選
  - 來源：SEC EDGAR 10-Q 2026Q3（as_of 2026-11-01）｜affects：moat_trend、decision_inputs.bear、thesis.R
- `lawsuit_class_action#0`（lawsuit_class_action｜方向 -｜狀態 ok）：10-K FY2025 Note 14 仍揭露 Sandoz／RareGen（現 Liquidia PAH）2019 年起的反競爭訴訟（Remodulin 相關），為既有案件；搜尋未見近 12 個月新的證券集體訴訟（僅 2017–2018 年律所調查公告）
  - 來源：SEC EDGAR 10-K FY2025 Note 14 Litigation（as_of 2026-02-25）｜affects：decision_inputs.bear、moat_trend

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 3 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/UTHR_20261108/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":1332.0,"bear_5y_price":330.0,"p_bull_pct":25,"p_bear_pct":30,"upside_5y_pct":50.9,"ev5y_pct":44.8,"irr_base_pct":8.6,"asym_ratio":2.8,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":28.02,"pe":20.06,"basis":"FY2026E 共識 EPS，現價 562.02 美元；與終端年當年度 EPS 同口徑"},"eps":{"bull":[36.5,47.0,57.0,66.0,74.0],"base":[33.5,40.5,46.0,50.0,53.0],"bear":[31.0,32.0,31.5,30.5,30.0]},"pe":{"bull":18,"base":16,"bear":11},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0,"net_buyback":0},"second_stage":{"bull_cagr_pct":9,"base_cagr_pct":6},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### UTHR_Q4_2025_Earnings_Call_20260225.md
- 2026-02-25｜Martine Rothblatt｜guidance：CEO重申2027年底達年化40億美元營收run rate，且不依賴三個新產品（原話："commitment to hit that $4 billion revenue run rate"）
- 2026-02-25｜Martine Rothblatt｜guidance：CEO稱以雙位數成長外推，2027年底季營收約10億美元（原話："hitting that $1 billion a quarter by the tail end of next"）
- 2026-02-25｜Martine Rothblatt｜guidance：CEO稱40億run rate不需三個新產品貢獻（原話："It does not require the contribution of these three"）
- 2026-02-25｜Michael Benkowitz｜guidance：COO稱若趨勢延續，最晚Q2回到營收季增（原話："return to sequential revenue growth no later than Q2"）
- 2026-02-25｜Michael Benkowitz｜margin：COO拆解季節性：Q1、Q4訂單較輕，Q2、Q3較重（原話："fourth quarter tend to be lighter ordering quarters"）
- 2026-02-25｜Michael Benkowitz｜margin：COO說明銷售受經銷商訂單時點影響，未必反映病患需求（原話："may not precisely reflect patient demand"）
- 2026-02-25｜Michael Benkowitz｜margin：COO給出Q4營收與Tyvaso DPI成長口徑（原話："we recorded $790 million in total revenue"）
- 2026-02-25｜Michael Benkowitz｜margin：COO給出Tyvaso Q4營收及DPI年增（原話："Total revenue for the fourth quarter was $464 million"）
- 2026-02-25｜Michael Benkowitz｜margin：COO說明Q4新病患起始落後的原因（季節性與天候）（原話："the patient starts have lagged these trends a little bit."）
- 2026-02-25｜Michael Benkowitz｜competition：COO稱轉介率最近4個月中有3個月達Liquidia上市前水準（原話："pre-Liquidia launch levels in 3 of the last 4 months"）
- 2026-02-25｜Michael Benkowitz｜competition：COO稱處方醫師廣度、深度與病患留存不低於Liquidia上市前（原話："patient retention is at or better to where it was before"）
- 2026-02-25｜Michael Benkowitz｜competition：COO稱Liquidia宣稱缺乏佐證，並說明嘗試新品的好奇期（原話："initial curiosity to evaluate a new market entrant"）
- 2026-02-25｜Michael Benkowitz｜competition：COO稱Tyvaso仍是吸入療法的市場領導者（原話："Tyvaso remains the well-entrenched market leader"）
- 2026-02-25｜Martine Rothblatt｜product：CEO首次公開軟霧吸入器Tresmi，稱可將咳嗽降低最多90%，今年送件、明年上市（原話："file for its approval in PAH and ILD this year"）
- 2026-02-25｜Martine Rothblatt｜product：CEO稱Tresmi各項競爭優勢要到FDA核准後才揭露（原話："remain undisclosed until we end up seeing the FDA approval"）
- 2026-02-25｜Martine Rothblatt｜product：CEO稱Tyvaso IPF第二個關鍵試驗下月解盲，最晚2027年6月上市（原話："launch into IPF not later than June of 2027"）
- 2026-02-25｜Martine Rothblatt｜product：CEO稱ralinepag結果次週解盲，主打每日一次（原話："unblinding of our outcome study next week"）
- 2026-02-25｜Leigh Peterson｜product：Peterson稱TETON 2 FVC絕對改善95.6毫升（原話："absolute forced vital capacity of 95.6 milliliters"）
- 2026-02-25｜Leigh Peterson｜product：Peterson說ralinepag希望看到臨床惡化事件相對安慰劑的顯著改善（原話："clinical worsening versus placebo"）
- 2026-02-25｜Michael Benkowitz｜product：COO介紹Tyvaso DPI新增80微克卡匣與96、112微克組合包（原話："We recently introduced 80-microgram cartridges"）
- 2026-02-25｜Martine Rothblatt｜product：CEO稱Xeno已有兩位病患移植，預計2030年商業化（原話："commercial Xeno product on the market in 2030"）
- 2026-02-25｜Martine Rothblatt｜product：CEO稱預期今年內取得FDA對Miromatrix肝臟與腎臟產品的指引（原話："We expect FDA guidance on how to take this liver failure"）
- 2026-02-25｜Martine Rothblatt｜product：CEO稱Skunkworks還有每日一次吸入劑、PRN吸入劑等管線（原話："even better pills than the once-daily ralinepag"）
- 2026-02-25｜Leigh Peterson｜risk：Peterson稱TETON 1與2基線特徵相近，預期可複製（原話："The baseline characteristics of both studies are similar"）
- 2026-02-25｜Michael Benkowitz｜customer：COO稱Tyvaso轉介率達兩年高點（原話："referrals for total Tyvaso was at its highest level"）
- 2026-02-25｜Martine Rothblatt｜commitment：CEO稱管理層承諾雙位數營收成長（原話："our commitment to double-digit revenue growth."）
- 2026-02-25｜Michael Benkowitz｜commitment：COO稱預期支持持久的雙位數成長（原話："continue to support durable double-digit growth"）
- 2026-02-25｜Martine Rothblatt｜capital_allocation：CEO稱正與三家藥廠洽談，基於其AI肺臟模型（原話："fruitful discussions with three great pharmaceutical"）

### 問答異常語氣（迴避／改口／保留）
- UTHR_Q4_2025_Earnings_Call_20260225.md｜問：UBS詢問TETON 1信心與Yutrepia對DPI／霧化劑病患新增的影響｜答法：Q4新病患起始落後，管理層歸因季節性與一月天候，並稱二月已改善，未給具體病患數字
- UTHR_Q4_2025_Earnings_Call_20260225.md｜問：Jefferies詢問40億run rate軟性財測及三個新產品對長期成長的貢獻｜答法：重申承諾並稱新產品為額外加分，未量化新產品貢獻
- UTHR_Q4_2025_Earnings_Call_20260225.md｜問：Leerink詢問軟霧吸入器人體研究細節與優化特性｜答法：多數細節拒絕公開，稱待FDA核准後才揭露

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 4 | 2 |
| customer_second_source | none | 0 | 2 |
| customer_concentration_credit | found | 2 | 2 |
| supply_demand_durability | found | 4 | 2 |
| regulatory_antitrust | found | 3 | 1 |
| reg_tariff_export | found | 2 | 3 |
| geo_supply_chain | found | 2 | 2 |
| end_markets | found | 4 | 3 |
| substitute_technology | found | 3 | 1 |
| channel_business_model_shift | found | 2 | 1 |
| capital_markets_pricing | found | 4 | 3 |
| major_events | found | 3 | 5 |

未涵蓋／不適用軸的查詢詞原文（供判相關性）：
- **customer_second_source**（none）：United Therapeutics largest customer specialty pharmacy concentration risk 10-K 2026 CVS Accredo；United Therapeutics single-source supplier risk Tyvaso Remodulin manufacturing in-house 2026

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"status":"no_prior_dd"}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"UTHR","date":"2026-11-08","schema":"v15.0","contract":"v19","company_name":"United Therapeutics"},"oneliner":"基本盤在 Q3 止穩，PH-ILD 和解補回缺口，現價約 FY2027E 的 16.6 倍；股價要走得好，得靠 2027 年 4 月底 IPF 獲准和上市後放量。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/UTHR_20261108/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/UTHR_20261108/scenario.json","answers":{"q1_business":{"verdict":"UTHR 賺的是肺動脈高壓與肺間質病變病人的長期用藥錢，九成以上來自 treprostinil 同一分子，錢卡在吸入劑型的處方決定這一節點。","reasoning":"Q3 2026 營收 8.325 億美元，Tyvaso 5.038 億（60.5%，其中 DPI 3.785 億、年增 13%，霧化劑 1.253 億、年減 12%），Orenitram 1.45 億（17.4%），Remodulin 1.22 億（14.7%），Unituxin 5,230 萬（6.3%）。三個 treprostinil 產品合計 92.6%，這是最大的單點依賴，也是護城河本身。GAAP 營益率 37.0%，含 Thymmune 約 1.3 億美元一次性研發費，還原後約 52.6%。美國經銷只經 Accredo 與 CVS Specialty 兩家，真正決定收入的是肺高壓專科醫師的處方與付款方的給付條件。供需判斷：需求結構性持久，競品增加改變的是份額分配，不是需求週期。","fact_refs":["f_kpi0_gaap","f_kpi1_gaap","f_kpi2_gaap","f_kpi5_tyvaso","f_kpi6_orenitram_remodulin_unit"],"verdict_values":{"revenue_quality":"慢性重症的長期處方收入，重複性高，但 92.6% 集中在 treprostinil 三個產品。","unit_econ_note":"TTM 毛利率 86.34%，比 FY2022 的 92.17% 低 5.83 個百分點，原因事實表未拆解。","archetype":{"primary":"品質複利成長","secondary":null,"confidence":"中","fingerprint":"單一分子、高毛利、淨現金、大額回購、晚期管線待批"},"industry":{"clock_phase":"II","sd_verdict_source":"結構性持久：PAH 與肺纖維化病人需要長期用藥，治療選項增加，適應症仍在擴大；依據為 2026-09-30 的 10-Q 與 2026-11-04 法說，判斷不看股價。","bargaining":{"up":"商業原料與成品都在美國製造；ralinepag 的原料供應商被 FDA 列為 OAI，是單一供應點風險。","down":"美國只有 Accredo 與 CVS Specialty 兩家非獨家經銷；聚合站稱約占營收 51% 與 36%，未核一手。付款方可要求學名藥替代或階梯療法。","geo":"二三級供應商在中國、印度、台灣，公司對主要供應商的供應鏈能見度有限。"},"profit_pool_dir":"PAH 的利潤池被新機轉與同分子新劑型分走一部分，PH-ILD 因和解回到 UTHR 手上，IPF 是新增的池子，尚未開張。","tam_table":[{"item":"IPF、PPF、PH-COPD 美國病人數","value":"約 100 萬人，管理層 2026-11-04 法說自述，未經第三方核對"},{"item":"PH-ILD 滲透率","value":"管理層稱市場大且滲透不足，具體數字事實表未涵蓋"},{"item":"SAM、分段 CAGR、營業利益池五年變化","value":"事實表未涵蓋"}]}}},"q2_moat":{"verdict":"護城河方向判穩定：PAH 被新機轉與同分子對手削弱，PH-ILD 因 2026 年 10 月和解重新只剩 Tyvaso 有標籤，兩邊大致抵銷。","reasoning":"執行力判穩定：過去幾季常是兩個好月配一個差月，營收沒有成長；Q3 連續月份轉好，DPI 年增 13%，10 月轉介超過 1,000 件，是單月新高。同一場法說也承認軟霧吸入器送件延到 2027、三合一口服錠的生物等效試驗不足、ralinepag 原料供應商被列 OAI。定價力判穩定：公司調價維持單位數，DPI 成長含調價，美國學名藥對 Remodulin 侵蝕有限。反面是 10-Q 明寫競品傷到霧化 Tyvaso、DPI 與 Remodulin，毛利率也從 FY2022 的 92.17% 降到 TTM 86.34%。對最強同業的 ROIC 差距事實表未涵蓋，改用營益率比：UTHR TTM 39.39%，Liquidia 37.39%（至 2026-06），差距已小；Liquidia 的數字在和解之前，PH-ILD 標籤拿掉後應會變差。可能看錯的地方：和解擋的是行銷和鼓勵標示外使用，不是醫師處方，標示外使用若沒降下來，PH-ILD 的牆就比看起來薄。","fact_refs":["f_peer_uthr_gross_margin_pct","f_peer_uthr_operating_margin_pct","f_peer_uthr_fcf_margin_pct","f_peer_lqda_gross_margin_pct","f_peer_lqda_operating_margin_pct","f_peer_lqda_fcf_margin_pct","f_peer_jazz_operating_margin_pct","f_peer_mrk_operating_margin_pct","f_peer_insm_operating_margin_pct","f_kpi5_tyvaso"],"verdict_values":{"moat":{"mechanism":"吸入式 treprostinil 的分子加裝置組合，配上長年累積的肺高壓專科醫師關係與用藥支持；PH-ILD 另有和解帶來的標籤保護。","execution":8,"pricing":8,"grade":"B","trend":"→","trend_evidence":"Q3 Tyvaso 合計年增 5%，DPI 年增 13%，法院判決與和解拿掉 Yutrepia 的 PH-ILD 適應症；反向是 10-Q 寫明競品已傷及三個 treprostinil 產品，霧化劑年減 12%、Remodulin 年減 3%。","competitor_notes":[{"name":"MRK","strategy_note":"以新機轉 Winrevair 切入 PAH，資源量級遠大於 UTHR；TTM 營益率 9.2% 與研發密度 45.65% 偏離常態，原因事實表未涵蓋，不拿來比護城河。"},{"name":"INSM","strategy_note":"TPIP 在後期臨床，是 Yutrepia 之後最值得防的同類吸入對手；TTM 營益率 -41.66%，靠外部資金與其他產品撐研發。"},{"name":"LQDA","strategy_note":"Yutrepia 上市一年多，TTM 營益率已到 37.39%，說明它能自籌彈藥；失去 PH-ILD 標籤後，要看 PAH 能否撐住成長。"},{"name":"JAZZ","strategy_note":"同規模專科藥對照組，不是直接對手；UTHR 的營益率 39.39% 高於 JAZZ 的 24.04%，FCF 利潤率 27.21% 則略低於 29.97%。"},{"name":"Boehringer","strategy_note":"Jascayd 已於 2025 年第四季核准 IPF 與 PPF，Tyvaso 進 IPF 時不是空白市場，處方順位事實表未涵蓋。"}],"spread_notes":{"axis":"營益率與 FCF 利潤率","note":"UTHR 營益率高於 JAZZ 15.35 個百分點，高於 LQDA 2.0 個百分點；ROIC 差距無法計算，方向只能用利潤率近似。"},"peer_na_reason":"同業 ROIC 與投入資本事實表未涵蓋，改用營益率與 FCF 利潤率當可比軸。","threats":[{"level":"🔴","text":"Merck 的 Winrevair 以新機轉切入 PAH，Insmed 的 TPIP 進入後期；若 prostacyclin 類藥物被往後線推，PAH 基本盤會持續流失。","p":"35%","evidence_refs":["competitive_share_entrants#0","substitute_technology#2","end_markets#1"]},{"level":"🟡","text":"Yutrepia 在 PAH 直接競爭；PH-ILD 標籤雖被拿掉，現有病人不必換藥，標示外使用是否下降要靠處方資料驗證。","p":"40%","evidence_refs":["competitive_share_entrants#3","supply_demand_durability#1","end_markets#3"]},{"level":"🟡","text":"Orenitram 學名藥 2027 年 6 月與 12 月可上市，霧化 Tyvaso 學名藥依舊文件最早 2026 年 1 月可進場，實際是否上市未證實；Orenitram 占 Q3 營收 17.4%。","p":"60%","evidence_refs":["supply_demand_durability#3"]},{"level":"🟡","text":"IPF 市場已有 Jascayd，Tyvaso 上市後能排到第幾線用藥，事實表沒有資料。","p":"35%","evidence_refs":["substitute_technology#2"]}],"roic_durability":{"quadrant":"高利益率，周轉率未知（投入資本事實表未涵蓋，當期 ROIC 無法計算）","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者是重症病人，決策者是肺高壓專科醫師，付款者是保險與 Medicare；延後用藥的代價高，10 月轉介超過 1,000 件是管理層提供的單月新高。"},{"item":"決策層級","level":"🟡","text":"替代發生在每位病人的處方上。Benkowitz 說用 Yutrepia 穩定的病人不會被換回來，這句話反過來也代表新病人的份額要逐一爭取；PAH 競爭中，PH-ILD 有標籤保護。"},{"item":"價值鏈分配","level":"🟡","text":"86.34% 的毛利率說明價值大多留在 UTHR；兩家經銷商集中，付款方可推階梯療法，毛利率五年下滑的原因事實表未拆解。"},{"item":"社會容忍度","level":"🟡","text":"公司調價維持單位數，等於沒有把價格推到經濟上限；MFN 定價威脅與專利藥關稅已入 10-K 風險，尚未點名 UTHR，商業原料與成品都在美國製造可降低關稅曝險。"}],"roiic":93.3,"reinvest_rate":18.5,"endo_ceiling":17.3,"formula_note":"代理算法：財報歷史 FY2022 到 FY2025 淨利增加 6.074 億美元，除以 FY2023 到 FY2025 累計（淨利－FCF）6.512 億，得 93.3%；再投資率＝6.512 億÷三年淨利 35.146 億＝18.5%；兩者相乘 17.3%。研發費用化（TTM 研發密度 22.06%）不在分母，ROIIC 被高估，淨利也含利息收入，17.3% 只能當上限參考。"}}}},"q3_growth":{"verdict":"五年後的成長空間判寬，前提是 IPF 與 ralinepag 至少拿到一張核准；FY2026E 營收只年增 2.1%，成長要靠尚未獲批的產品接手。","reasoning":"成長來源以量為主、單位數調價為輔，EPS 再由回購放大，併購只占小部分。三年共識 EPS 由 FY2025A 27.86 美元到 FY2028E 42.41 美元，年化 15.0%；內生上界 17.3%，共識沒有超過，缺口為負 2.3 個百分點。這段成長分布不平均：FY2026E 營收年增 2.1%，FY2027E 年增 10.9%，FY2028E EPS 再跳 25%。下一條曲線有來源：TETON-1、TETON-2 都達主要終點，FDA 已受理 IPF 申請，審查期到 2027 年 4 月底；ralinepag 審查日為 2027-06-24。管理層稱 IPF、PPF、PH-COPD 合計約 100 萬美國病人，滲透率事實表未涵蓋，換算不出達 30% 滲透的年數。若 IPF 未獲准，這一項要降為中等。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_kpi5_tyvaso"],"verdict_values":{"growth":{"driver_mix":"量為主、單位數調價為輔；FY2028E 的跳升靠 IPF 與 ralinepag，回購放大每股盈餘，併購占比小。","runway_years":"事實表未涵蓋滲透率，無法換算","runway_post_y5":"🟢","endo_ceiling_basis":"引護城河段的內生上界 17.3%，由淨利增量與（淨利－FCF）推得，研發費用化使其偏高；共識三年 EPS 年化 15.0% 未超過，其中含回購貢獻。","segments":[{"item":"Tyvaso DPI","value":"Q3 2026 3.785 億美元，年增 13%，量增加上調價"},{"item":"霧化 Tyvaso","value":"Q3 2026 1.253 億美元，年減 12%，美國量下滑"},{"item":"Orenitram","value":"Q3 2026 1.45 億美元，年增 11%；學名藥 2027 年 6 月與 12 月可上市"},{"item":"Remodulin","value":"Q3 2026 1.22 億美元，年減 3%；前九個月年減 6%"},{"item":"Unituxin","value":"Q3 2026 5,230 萬美元，年增 9%"}],"decay_signals":["毛利率下滑：亮燈。FY2024 89.24%、FY2025 87.92%、TTM 86.34%；逐季年比事實表未涵蓋。","核心市占縮減：亮燈。10-Q 寫競品傷到霧化 Tyvaso、DPI 與 Remodulin，具體份額事實表未涵蓋。","主力產品提價後銷量下滑：未亮。DPI 量價齊升；霧化劑量減是否與提價有關，事實表未涵蓋。","EPS CAGR 高於營收 CAGR 超過 5 個百分點：未亮。FY2022 到 FY2025 為 22.9% 對 18.0%，差 4.9 個百分點，已接近門檻。","FCF 對淨利連兩年低於 0.75：未亮。FY2024 為 0.90，FY2025 為 0.78。","SBC 占營收超過 5% 且逐年上升：未亮。Q3 2026 為 4.9%，歷年趨勢事實表未涵蓋。","TAM 萎縮或被替代：未亮。PAH 有替代壓力，PH-ILD 與 IPF 是擴大方向。","產業倍數三年系統性下移：事實表未涵蓋。","維護性資本支出占 FCF 超過 60%：事實表未涵蓋。","停止投資新產能且收入下滑：未亮。"],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"資金運用偏向股東：帳上無負債，現金與投資 35.4 億美元，2026 年兩度核准各 20 億美元回購；回購價位的報酬目前無法驗證。","reasoning":"FCF 對淨利的轉換率 FY2022 到 FY2025 分別為 91%、76%、90%、78%，來自財報歷史。SBC 占 Q3 營收 4.9%，年化約為市值的 0.7%。回購：2026 年 3 月簽 ASR 並核准最高 20 億美元，9 月再簽 4.776 億美元 ASR，10 月 21 日再核准 20 億美元一年期計畫，相當於市值 8.4%。併購規模小：Thymmune 現金 1.4 億美元，加里程碑最高 3 億，占市值 1.25%。CFO 在 2026-11-04 法說拒絕說明買斷 Arena 的 ralinepag 權利金花了多少，這筆資本的報酬外界算不出來。現金去向四分、回購均價、10 年期公債殖利率，事實表未涵蓋。","fact_refs":["f_kpi4_sbc","f_kpi7","f_net_debt_m","f_shares_diluted_m","f_price_at_dd"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":false,"passed":null,"input":"Thymmune 尚未產生收入，交割現金占市值約 0.6%，已實現報酬無從計算；過往併購收入事實表未涵蓋。"},{"name":"buyback_yield","applicable":true,"passed":null,"input":"回購均價與 10 年期公債殖利率事實表未涵蓋；以現價估 FY2026E 盈餘殖利率 4.99%，FY2027E 6.03%。"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"Q3 SBC 4,100 萬美元，年化 1.64 億÷市值 239.4 億＝約 0.7%，低於 1.5%；此為近似，未含選擇權完整稀釋。"}]},"governance":{"capital_returns":[{"item":"2026-03-09","value":"簽 ASR，核准最高 20 億美元庫藏股"},{"item":"2026-09-08","value":"再簽 4.776 億美元 ASR"},{"item":"2026-10-21","value":"董事會核准新的 20 億美元一年期回購，約市值 8.4%"}]}}},"q5_valuation":{"verdict":"現價要有 10% 年化報酬，FY2031E EPS 得做到約 57 美元（年化約 15%）並維持 16 倍；這要 IPF 放量、基本盤不掉才到得了，我的 Base 只信到 13.6%。","reasoning":"FY2026E 本益比 20.06 倍，分母含 Thymmune 一次性費用，還原約 31 美元後約 18 倍；FY2027E 16.58 倍；PEG 以三年 EPS 年化 15.04% 計為 1.33，落在合理區。每股現金與投資約 83 美元，占股價 14.8%。事實表的淨負債只算 20.679 億美元現金，公司公布的現金與可交易投資是 35.357 億，EV 用公司數字會低約 14.7 億。Trailing P/E 21.22 倍是 4 個年度端點的最高，但樣本只有 4 點，且 TTM 盈餘含一次性費用，不能當五年高位。TTM 營益率比 FY2025 低 8.3 個百分點，Thymmune 只解釋約 4 個百分點，其餘事實表未說明。Q3 GAAP EPS 5.71 美元，共識有 5.85 與 6.04 兩個來源。賣方目標價聚合站從 533 到 664 美元不一，最高的 664.33 美元是 8 月資料，只能算弱支持，不當錨。共識兩次快照修正都是 0%，可能還沒反映 Q3 財報。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_pe_current","f_pe_percentile","f_ps_current","f_ps_percentile","f_ev_s_current","f_ev_s_percentile","f_ev_m","f_net_debt_m","f_kpi7","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_fy1_pct","f_consensus_rev_fy2_pct","f_consensus_rev_fy3_pct","f_kpi3_gaap_eps"],"verdict_values":{"valuation":{"basis":"Fwd P/E 與 PEG；盈餘為正、現金流穩定，主看 FY2027E，因 FY2026E 含一次性費用，FY2028E 依賴未獲准產品。","fwd_pe":20.06,"peers":{"expanded":false,"reason":"事實表只有同業利潤率與研發密度，未含 Fwd P/E 或 EV/S，同業倍數對照屬資料缺口。"},"peg":1.33,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"FY2027E 16.58 倍、PEG 1.33、Base 年化約 8.6%，屬合理不便宜；五年分位事實表未涵蓋，4 個年度端點不能替代。","upside_short_pct":7.3,"upside_mid_pct":22.5,"denominator_disputed":false,"denominator_note":"FY2026E 含約 1.3 億美元一次性研發費，還原後約 31 美元，一次性項目壓低而不是墊高盈餘，便宜論證不因此失效。短期上檔用 FY2027E 33.5 美元×18 倍，中期用 FY2028E 40.5 美元×17 倍。"}}},"q6_how_wrong":{"verdict":"最可能看錯的是 IPF 上市後的放量速度，以及 PH-ILD 標示外使用是否真的降下來。","reasoning":"十項衰退訊號亮兩項，毛利率下滑與核心市占縮減，歸為中等風險，不是價值陷阱。論點失敗、股東經濟變差、價格反映太多三條路徑見反證紀錄。歷史最大回撤、空方最強數字、訴訟金額全貌，事實表未涵蓋；已知的金額只有 Sandoz 案提列的 7,410 萬美元。","fact_refs":["f_peer_uthr_gross_margin_pct","f_kpi5_tyvaso","f_kpi4_sbc"],"verdict_values":{"trap":{"verdict":"🟡","label":"成長換檔期，有兩項衰退訊號，尚非價值陷阱"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":28.02,"pe":20.06,"basis":"FY2026E 共識 EPS，現價 562.02 美元；與終端年當年度 EPS 同口徑"},"eps":{"bull":[36.5,47.0,57.0,66.0,74.0],"base":[33.5,40.5,46.0,50.0,53.0],"bear":[31.0,32.0,31.5,30.5,30.0]},"pe":{"bull":18,"base":16,"bear":11},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0,"net_buyback":0},"second_stage":{"bull_cagr_pct":9,"base_cagr_pct":6},"max_dd":{"lo":-55,"hi":-35,"basis":"事實表未涵蓋歷史最大回撤，改由情境推算：Bear 終點跌 41%；若 IPF 未獲准同時 Tyvaso 轉負，FY2027E EPS 31 美元乘 9 到 12 倍得 279 到 372 美元，相對現價跌 34% 到 50%，兩端各留約 1 到 5 個百分點緩衝。","trigger_time":null},"basis":{"bull":"IPF 獲准並快速放量，ralinepag 準時上市，PH-ILD 標示外使用明顯下降，回購持續；FY2031E 營收約 68 億美元，淨利率約 42%。","base":"IPF 於 2027 年上市，ralinepag 逐步貢獻，PAH 基本盤緩慢流失；FY2031E 營收約 52.5 億美元、淨利率約 40%、股數約 3,950 萬股。FY2027E、FY2028E 略低於共識，因為軟霧吸入器延後。回購效果已進 EPS 路徑，殖利率欄填 0 以免重複計算，事實表也未見股息紀錄。終端 16 倍對照 UTHR 自身 FY2026E 20.06 倍與 FY2027E 16.58 倍；同業現值倍數事實表未涵蓋。","bear":"IPF 未獲准或放量遠低於預期，PAH 被新藥與學名藥侵蝕，Orenitram 2027 年後下滑，EPS 靠回購守在約 30 美元。終端 11 倍按成長降到 10% 以下推估。機率 30% 的依據：10-Q 已寫競品造成傷害，Orenitram 學名藥時點明確，IPF 商業化沒有對照資料。"},"endo_ceiling_exceeded":false},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"10-Q 已寫競爭療法傷到霧化 Tyvaso、DPI 與 Remodulin；IPF 市場已有 Jascayd；Orenitram 學名藥 2027 年可上市；Q3 treprostinil 占營收 92.6%。","assumption":"IPF 獲准後能快速取得處方，PAH 基本盤只是緩慢流失。","consequence":"IPF 獲准但放量慢，PAH 同時被新藥與學名藥吃掉，EPS 卡在約 30 美元，倍數跌到 11 倍，股價約 330 美元，五年虧約 41%；過程中超跌可到 50% 以上。","ruling":"採納為 Bear 路徑，機率 30%。這條與 Single Thing 部分重疊：Single Thing 管能不能拿到核准，這條管拿到之後賣不賣得動。","watch":"IPF 上市後前兩季 Tyvaso 季增金額、DPI 與霧化劑拆分、Orenitram 季營收。","evidence_refs":["substitute_technology#2","end_markets#1","supply_demand_durability#3"],"fact_refs":["f_kpi5_tyvaso","f_kpi6_orenitram_remodulin_unit"]},{"view":"論點失敗","evidence":"管理層稱專利多延伸到 2040 年代，事實表沒有逐項專利到期表，DPI 與 IPF 用途專利的強度無法獨立確認。","assumption":"新適應症與裝置專利足以擋住學名藥。","consequence":"若關鍵專利被挑戰成功，五年後的成長空間要從寬降為中等，終端倍數也要下修。","ruling":"不可裁決至取得專利到期表。先把管理層說法列為未驗證，10 年期延伸只給 Base 每年 6%。","watch":"10-K 專利章節、學名藥申請與 Paragraph IV 訴訟進度。","evidence_refs":["competitive_share_entrants#0"],"fact_refs":[]},{"view":"論點成功但股東經濟變差","evidence":"TTM 營益率 39.39%，FY2025 為 47.67%，FY2024 為 50.33%。Thymmune 約占 4 個百分點，其餘約 4 個百分點事實表沒有解釋。公司同時推 14 個管線、擴編業務團隊、做製造器官；MFN 與階梯療法風險寫進 10-K。","assumption":"新適應症的收入會以現有利潤率落到 EPS。","consequence":"IPF 與 ralinepag 都成功，但上市費用、研發與製造器官持續吃掉利潤，ralinepag 也可能分食公司既有 PAH 產品，FY2031E EPS 比 Base 少 10% 到 15%，每股約 5 到 8 美元。","ruling":"部分採納。Base 淨利率只設約 40%，不假設回到 FY2023 的 50% 營益率。","watch":"排除一次性費用後的營益率、研發密度、ralinepag 上市後 Orenitram 的變化。","evidence_refs":["reg_tariff_export#0","substitute_technology#1"],"fact_refs":["f_peer_uthr_operating_margin_pct","f_kpi1_gaap","f_kpi2_gaap"]},{"view":"價格已反映太多","evidence":"Trailing P/E 21.22 倍與 P/S 7.51 倍都是 4 個年度端點的最高；股價高於 104 週均線約 30%；FY2028E EPS 比 FY2027E 多 25%，靠尚未獲准的產品。","assumption":"FY2028E 42.41 美元能達成。","consequence":"IPF 獲准只是兌現預期，若首年銷售低於賣方模型，股價可能在好消息後不漲；Base 年化只有約 8.6%。","ruling":"部分反駁。Trailing 分母被一次性費用壓低，又只有 4 點，不能當五年高位證據；FY2027E 16.58 倍加每股現金約 83 美元，還不到反映太多。但也不便宜，所以不追價。","watch":"Q3 財報後 FY2027E、FY2028E 共識的修正方向；兩次快照都是 0%，要確認是真的沒動還是資料沒更新。","evidence_refs":[],"fact_refs":["f_pe_current","f_pe_percentile","f_ps_percentile","f_ma_w104","f_consensus_eps_fy3","f_kpi7"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 None → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=None","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 None → 本次 562.02","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=None","side_b":"本次 price_at_dd=562.02","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"一致判斷","cause":null,"prior_field":null,"side_a":"10-Q 與法說都顯示 DPI 接手霧化劑，Q3 Tyvaso 合計年增 5%。","side_b":"財報歷史顯示營收成長已由 FY2024 的 23.6% 降到 FY2025 的 10.6%，FY2026E 共識只有 2.1%。","ruling":"兩者一致指向成長換檔，基本盤止穩，下一段成長要靠新適應症。","evidence_level":"一手申報與財報歷史","settle_metric":"Tyvaso 合計年增率","if_then":["若 Tyvaso 年增維持 5% 以上，論點基礎成立。","反向：若連兩季低於 0%，減碼至一半。"],"evidence_refs":[]},{"axis":"競爭傷害與本季創紀錄","cause":null,"prior_field":null,"side_a":"10-Q 寫競爭療法在 Q3 傷到霧化 Tyvaso、DPI 與 Remodulin；前九個月 Tyvaso 合計 14.139 億美元，沒有成長；二手摘要稱上半年霧化劑年減 20%。","side_b":"2026-11-04 法說 Benkowitz 稱 Q3 是史上最佳一季，Tyvaso 5.038 億美元，10 月轉介超過 1,000 件。","ruling":"可調和，屬程度差異。競爭確實造成流失，DPI 的增量在 Q3 開始蓋過。採止穩，不採動能已恢復到雙位數。","evidence_level":"一手對一手；上半年 20% 為二手摘要，方向與 10-Q 一致。","settle_metric":"2026 Q4 與 2027 Q1 的 Tyvaso 合計年增率","if_then":["若兩季都達 5% 以上，維持 Base 路徑，可加碼一檔。","反向：若任一季低於 0%，停止加碼；連兩季低於 0%，減碼至一半。"],"evidence_refs":["end_markets#1","competitive_share_entrants#3"]},{"axis":"Q3 是否受訂單時點影響","cause":null,"prior_field":null,"side_a":"2026-02-25 Benkowitz 說 Q2、Q3 訂單較重，Q1、Q4 較輕，銷售未必反映病患需求。","side_b":"2026-11-04 Benkowitz 回答 Leerink 時說本季沒有庫存或季節因素。","ruling":"未證，先監測。管理層沒給庫存天數，不採信也不否定。共識隱含 Q4 營收約 8.51 億美元，等於要在較輕的季度再季增 2.2%。","evidence_level":"一手法說，但屬管理層說法，沒有庫存數據。","settle_metric":"2026 Q4 總營收與 2027 Q1 季增率","if_then":["若 2026 Q4 總營收低於 8.1 億美元，認定 Q3 含訂單時點，停止加碼。","反向：若達 8.4 億美元以上，接受動能說法，加碼一檔。"],"evidence_refs":[]},{"axis":"40 億美元年化營收的前提","cause":null,"prior_field":null,"side_a":"2026-02-25 Rothblatt 說 2027 年底年化 40 億美元不需要三個新產品，並承諾雙位數營收成長。","side_b":"2026-08-05 Q2 摘要稱這條路徑建立在 IPF 與 ralinepag 獲准之上；2026-11-04 法說沒有再提 40 億，FY2026E 共識營收只年增 2.1%。","ruling":"可調和，採保守側。摘要是二手，還不足以稱改口；但 FY2026 的雙位數已做不到，Base 假設 40 億要靠新產品。從 Q3 的 8.325 億到 2027 Q4 的 10 億，需要連續五季平均季增約 3.7%。","evidence_level":"一手法說對二手摘要","settle_metric":"2027 Q4 單季營收是否達 10 億美元","if_then":["若 2027 Q4 單季營收達 10 億美元，上修 Base 的 FY2028E。","反向：若 2027 Q2 單季營收低於 8.8 億美元，把 2027 年底 40 億從 Base 拿掉並減碼一檔。"],"evidence_refs":["supply_demand_durability#2"]},{"axis":"PH-ILD 還有沒有品牌競爭","cause":null,"prior_field":null,"side_a":"2026-11-04 Benkowitz 說沒有直接的品牌競爭在望，Tyvaso 有長跑道。","side_b":"同季 10-Q 把 Insmed 的 TPIP 列為 PAH、PH-ILD、IPF 或 PPF 的潛在新競品。","ruling":"採 10-Q。和解擋住的是 Yutrepia，不是 TPIP；PH-ILD 的保護期只算到 TPIP 上市前，上市時程事實表未涵蓋。","evidence_level":"一手申報優先於法說口頭說法","settle_metric":"TPIP 的 PH-ILD 試驗結果與申請時點","if_then":["若 TPIP 在 PH-ILD 提出上市申請，Base 從 FY2030E 起 EPS 下修 5%，停止加碼。","反向：若 TPIP 的 PH-ILD 試驗失敗，Bear 機率下調 5 個百分點。"],"evidence_refs":["substitute_technology#2","competitive_share_entrants#0","supply_demand_durability#1"]},{"axis":"新產品時程","cause":null,"prior_field":null,"side_a":"2026-02-25 Rothblatt 說軟霧吸入器今年送件、明年上市。","side_b":"2026-11-04 Poisson 說與 FDA 溝通後要補資料，送件延到 2027；三合一口服錠的生物等效試驗不足，還在找替代路徑；ralinepag 原料供應商被列 OAI。","ruling":"採後者。這些不影響 IPF 主線，但新產品節奏變慢，軟霧吸入器不放進 2028 年前的 Base。","evidence_level":"一手法說前後對照","settle_metric":"2027-06-24 ralinepag 審查結果、軟霧吸入器送件日","if_then":["若 ralinepag 在 2027-06-24 未獲准，下修 FY2028E 起的 EPS 並停止加碼。","反向：若準時獲准且 OAI 解除，維持 Base，不上修。"],"evidence_refs":[]},{"axis":"產業態勢","cause":null,"prior_field":null,"side_a":"競爭惡化：Winrevair、Yutrepia、Jascayd 已上市，TPIP 在後期，10-Q 寫明已傷及銷售。","side_b":"結構轉好：法院維持 UTHR 專利，和解拿掉 Yutrepia 的 PH-ILD 適應症，IPF 若獲准可打開新市場。其他結構變數：MFN 與 232 關稅未點名 UTHR，商業原料與成品都在美國製造。","ruling":"雙向拉鋸。PAH 在惡化，PH-ILD 在轉好，政策面尚未落到公司損益。","evidence_level":"一手申報與法說","settle_metric":"Tyvaso 年增率與 TTM 毛利率","if_then":["若 TTM 毛利率連兩季低於 84%，減碼一檔並下修終端倍數。","反向：若毛利率回升到 88% 以上，Bear 機率下調 5 個百分點。"],"evidence_refs":["end_markets#1","reg_tariff_export#0"]},{"axis":"多空最強論證","cause":null,"prior_field":null,"side_a":"現在就買：FY2027E 16.58 倍，每股現金約 83 美元，2026 年兩度核准各 20 億美元回購，最新一筆約市值 8.4%；IPF 有兩個 Phase 3 達標，ralinepag 已進 FDA 審查，八個月內有兩個 FDA 日期。","side_b":"現在就賣：treprostinil 占 92.6%，10-Q 已寫競品造成傷害，FY2026E 營收只年增 2.1%，FY2028E 的 25% 跳升靠未獲准的適應症，管理層 2026 年的承諾與時程已多次落空。","ruling":"可調和。現價不用等，但不值得在 IPF 結果前重押：先小倉，用財報和 FDA 結果分批加。","evidence_level":"事實表與一手法說","settle_metric":"2026 Q4 營收與 2027-04 底 FDA 決定","if_then":["價格先走證據未到：股價超過 650 美元且 IPF 尚未獲准，不追。","跌但基本面無損：股價跌到 480 美元以下且 Tyvaso 年增仍為正，分批反買。","判斷被證實為錯：Single Thing 發生，減碼至一半；同時 Tyvaso 年增連兩季低於 0%，清倉。"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"FDA 對霧化 Tyvaso IPF 適應症的決定是最大單一敏感項。","type":"Single Thing","maps_to":"Single Thing","metric":"FDA 對 IPF 補充申請的決定","threshold":"2027-04-30 前未獲准，或延審超過 6 個月","action":"減碼至原倉位一半，Base 機率移 20 個百分點到 Bear 重算","source_freq":"FDA 公告與公司 8-K，單次","date":"2027-04-30","evidence_refs":[]},{"n":2,"text":"2026 Q4 營收驗證 Q3 的動能是否真實。","type":"假設驗證","maps_to":"H1","metric":"2026 Q4 總營收","threshold":"達 8.4 億美元算過，低於 8.1 億美元算不過","action":"過：加碼一檔；不過：停止加碼","source_freq":"公司新聞稿，每季","date":"2027-02（財報日未公告）","evidence_refs":[]},{"n":3,"text":"Tyvaso 轉負代表基本盤沒有止穩。","type":"減碼","maps_to":"R1","metric":"Tyvaso 合計季營收年增率","threshold":"連兩季低於 0%","action":"減碼至原倉位一半","source_freq":"公司新聞稿與 10-Q，每季","date":"每季","evidence_refs":["end_markets#1","competitive_share_entrants#3"]},{"n":4,"text":"和解後 Yutrepia 若仍快速成長，PH-ILD 的保護可能比管理層講的弱。","type":"風險","maps_to":"R1","metric":"Liquidia 公布的 Yutrepia 季營收季增率","threshold":"和解後連兩季季增超過 10%，且 Tyvaso DPI 季增低於 3%","action":"停止加碼","source_freq":"Liquidia 財報，每季","date":"2027-05 起","evidence_refs":["supply_demand_durability#1","end_markets#3"]},{"n":5,"text":"ralinepag 的原料供應商 OAI 狀態可能影響審查日。","type":"風險","maps_to":"R2","metric":"ralinepag FDA 決定","threshold":"2027-06-24 未獲准，或公司宣布延期","action":"停止加碼，下修 FY2028E 起的 EPS","source_freq":"公司 8-K，單次","date":"2027-06-24","evidence_refs":[]},{"n":6,"text":"Orenitram 學名藥上市後的侵蝕速度。","type":"風險","maps_to":"R3","metric":"Orenitram 季營收","threshold":"學名藥上市後兩季內較 1.45 億美元下滑 25% 以上","action":"減碼一檔","source_freq":"公司新聞稿，每季","date":"2027-06 起","evidence_refs":["supply_demand_durability#3"]},{"n":7,"text":"定價與關稅壓力要看能不能被損益吸收。","type":"風險","maps_to":"R4","metric":"TTM 毛利率","threshold":"連兩季低於 84%","action":"減碼一檔並下修終端倍數","source_freq":"季報，每季","date":"每季","evidence_refs":["reg_tariff_export#0","substitute_technology#1"]},{"n":8,"text":"法律與政府調查要按程序性質處理。","type":"風險","maps_to":"R6","metric":"DOJ 或 FTC 新案、民事案估損","threshold":"民事不利判決或估損達 2 億美元；刑事調查介入","action":"民事不利：減碼至一半；刑事介入：清倉","source_freq":"10-Q 訴訟附註與 8-K，每季","date":"每季","evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#1","lawsuit_class_action#0"]},{"n":9,"text":"IPF 獲准且標籤沒有被限縮，是主要加碼點。","type":"加碼","maps_to":"H2","metric":"FDA 核准與標籤範圍","threshold":"2027-04-30 前獲准，適應症涵蓋 IPF 主要族群","action":"加碼一檔，至倉位上限","source_freq":"FDA 標籤與公司 8-K，單次","date":"2027-04-30","evidence_refs":[]},{"n":10,"text":"價格跌到 Base 年化約 12% 的位置，基本面又沒壞，可以反買。","type":"估值rearm","maps_to":"H1","metric":"股價與 Tyvaso 年增率","threshold":"股價 480 美元以下且 Tyvaso 年增為正","action":"分批反買","source_freq":"每日股價與每季財報","date":"持續","evidence_refs":[]},{"n":11,"text":"IPF 落空加上基本盤轉負，論點已不成立。","type":"清倉","maps_to":"H1、H2","metric":"IPF 決定與 Tyvaso 年增率","threshold":"IPF 未獲准，且 Tyvaso 年增連兩季低於 0%","action":"清倉","source_freq":"FDA 公告與每季財報","date":"2027 Q3 前","evidence_refs":["substitute_technology#2"]},{"n":12,"text":"兩個 FDA 日期過後重新評估。","type":"複審日期","maps_to":"H2、H3","metric":"IPF 與 ralinepag 結果","threshold":"兩項結果都出爐","action":"重跑完整研究並更新情境","source_freq":"單次","date":"2027-07-15","evidence_refs":[]}],"kill_metrics":[{"metric":"FDA 對霧化 Tyvaso IPF 適應症的決定","bear_threshold":"2027-04-30 前未獲准，或延審超過 6 個月","window":"2027-04-30 前","source":"FDA 公告與公司 8-K","last_status":"unknown"},{"metric":"Tyvaso 合計季營收年增率","bear_threshold":"連兩季低於 0%","window":"每季；Q3 2026 為 +5%","source":"公司新聞稿 8-K Ex.99.1","last_status":"ok"},{"metric":"2026 Q4 總營收","bear_threshold":"低於 8.1 億美元","window":"2027 年 2 月財報","source":"公司新聞稿","last_status":"unknown"},{"metric":"TTM 毛利率","bear_threshold":"連兩季低於 84%","window":"每季；最新 86.34%","source":"季報與 yfinance 季度損益表","last_status":"warning"},{"metric":"排除一次性費用後的營益率","bear_threshold":"連兩季低於 45%","window":"每季；Q3 2026 還原約 52.6%","source":"公司新聞稿與 10-Q","last_status":"ok"},{"metric":"Orenitram 季營收","bear_threshold":"學名藥上市後兩季內較 1.45 億美元下滑 25% 以上","window":"2027-06 起","source":"公司新聞稿","last_status":"unknown"}],"action_conditions":{"rearm_trigger":"股價 480 美元以下且 Tyvaso 年增為正；或 FDA 於 2027-04 底前核准 IPF，且 2026 Q4 營收達 8.4 億美元以上","exec_line":"現價可先建小倉；2026 Q4 營收達 8.4 億美元以上加一檔，IPF 獲准再加一檔；股價超過 650 美元而 IPF 未獲准時不追。"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場用過去幾季沒有成長的印象定價，FY2027E 只給 16.6 倍；PH-ILD 和解到 10 月中才定案，共識兩次快照都沒動。若快照只是尚未更新，這個理由要打折。","momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":null,"wait_for_price_condition":null},"thesis":{"H":[{"id":"H1","text":"基本盤止穩：DPI 的增量蓋過霧化劑流失，Tyvaso 在 IPF 上市前維持正成長。","2y":"2026 Q4 到 2027 Q2 的 Tyvaso 單季年增都在 5% 以上，2026 Q4 總營收達 8.4 億美元以上。","5y":null,"10y":null,"threshold":"Tyvaso 單季年增達 5%；2026 Q4 總營收達 8.4 億美元（共識隱含約 8.5 億）。","source":"公司新聞稿 8-K Ex.99.1 與 10-Q 的產品別營收，每季。","drift_rule":"TTM 偏離門檻連 2 季達 5% 算削弱，連 3 季達 10% 算反轉。"},{"id":"H2","text":"霧化 Tyvaso 取得 IPF 適應症並在上市後放量，成為第二條成長曲線。","2y":"2027-04-30 前獲准，2027-06 前上市，FY2028 總營收達 40 億美元。","5y":"FY2031 Tyvaso 總營收達 33 億美元（FY2026E 約 19.4 億，由前九個月加 Q4 估算）。","10y":null,"threshold":"FDA 2027-04-30 前獲准；FY2028 總營收 40 億美元；FY2031 Tyvaso 33 億美元。","source":"FDA 決定、公司 8-K、季報的 Tyvaso 分項營收。","drift_rule":"未獲准直接反轉；獲准後 TTM 低於路徑連 4 季達 5% 算削弱，連 6 季達 10% 算反轉。"},{"id":"H3","text":"ralinepag 與後續產品降低對 treprostinil 的依賴，淨現金與回購讓每股盈餘跑贏淨利。","2y":"ralinepag 於 2027-06-24 獲准，股數年減達 2.5%。","5y":"FY2031 非 treprostinil 產品占營收達 20%（Q3 2026 約 7.4%）。","10y":null,"threshold":"ralinepag 2027-06-24 獲准；非 treprostinil 占比 20%；股數年減 2.5%。","source":"FDA 決定、季報的產品別營收與股數。","drift_rule":"TTM 偏離門檻連 4 季達 5% 算削弱，連 6 季達 10% 算反轉；FDA 拒絕時直接重評。"}],"R":[{"id":"R1","text":"PAH 競爭持續侵蝕 treprostinil，Winrevair、Yutrepia、TPIP 三面夾擊；PH-ILD 還有標示外使用的漏洞。","h_ref":"H1","clock":"🔥","threshold":"Tyvaso 年增連兩季低於 0%，或 Remodulin 年減達 10%。","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#3","end_markets#1","end_markets#3","substitute_technology#2","supply_demand_durability#1"]},{"id":"R2","text":"IPF 或 ralinepag 的審查結果不如預期，或原料供應商 OAI 拖累 ralinepag 時程。","h_ref":"H2","clock":"⚡","threshold":"IPF 2027-04-30 前未獲准；ralinepag 2027-06-24 未獲准。","evidence_refs":[]},{"id":"R3","text":"學名藥與專利到期：Orenitram 2027 年可上市，霧化 Tyvaso 學名藥是否已進場未證實，管理層的 2040 年代專利說法未經逐項驗證。","h_ref":"H1","clock":"🔥","threshold":"學名藥上市後兩季內 Orenitram 下滑 25%。","evidence_refs":["supply_demand_durability#3"]},{"id":"R4","text":"藥價與給付政策：MFN、專利藥關稅、付款方階梯療法壓縮淨價。","h_ref":"H1","clock":"🐢","threshold":"TTM 毛利率連兩季低於 84%。","evidence_refs":["reg_tariff_export#0","substitute_technology#1"]},{"id":"R5","text":"經銷集中在 Accredo 與 CVS Specialty，應收帳款集中；聚合站的 51% 與 36% 未核一手。","h_ref":"H1","clock":"🐢","threshold":"任一家經銷合約終止或付款條件明顯惡化；實際占比需以 10-K 核對。","evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#1"]},{"id":"R6","text":"法律風險：Sandoz 案已提列 7,410 萬美元，專利和解可能引發反壟斷主張，公司曾遭 DOJ 調查與保險公司 RICO 提告；其餘案件金額與結案時點事實表未涵蓋。","h_ref":"H3","clock":"🐢","threshold":"DOJ 或 FTC 新立案，或單案估損達 2 億美元。","evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#1","lawsuit_class_action#0"]},{"id":"R7","text":"裝置與供應鏈：Remodulin 輸注泵浦依賴第三方且型號停產，資料來自 FY2024 10-K；Remodulin 占 Q3 營收 14.7%。","h_ref":"H1","clock":"🐢","threshold":"公司揭露泵浦短缺導致 Remodulin 單季年減達 10%。","evidence_refs":["geo_supply_chain#1"]},{"id":"R8","text":"成本與資本配置：研發、上市費用與製造器官吃掉利潤，TTM 營益率下滑有約 4 個百分點未解釋。","h_ref":"H3","clock":"🔥","threshold":"排除一次性費用後的營益率連兩季低於 45%。","evidence_refs":[]}],"single_thing":{"description":"FDA 在 2027 年 4 月底審查期結束時，未核准霧化 Tyvaso 的 IPF 適應症，或延審超過 6 個月。","why_fatal":"共識 EPS 從 FY2027E 33.89 美元跳到 FY2028E 42.41 美元，主要靠新產品。IPF 落空時，Base 的 FY2028E 40.5 美元會回到 Bear 的約 32 美元，少 21%，本益比再從 16 倍往 11.5 倍走，合計價值少約 43%，是情境裡最大的單一敏感項。","if_happens":"減碼至原倉位一半，Base 機率移 20 個百分點到 Bear 重算；同時 Tyvaso 年增連兩季低於 0% 就清倉。","how_monitor":"盯 2027-04-30 審查期與公司 8-K，獲准後看標籤的適應症範圍與用藥限制。","probability":"12 到 24 個月內約 10% 到 15%。兩個 Phase 3 都達主要終點，FDA 已受理；事實表沒有 TETON-1 效果量，這是判斷值。"}},"appendix_a":{"growth_durability":7,"quality_score":7,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":16.58,"peg_fy2":1.1,"stress":{"pass":null,"total":null}},"eps_meta":{"base_eps_path":{"FY2025A":27.86,"FY2026E":28.02,"FY2027E":33.89,"FY2028E":42.41},"fy_end_month":12,"eps_basis":"FY2025A 為 GAAP 稀釋 EPS；FY2026E 到 FY2028E 為 Koyfin 共識，GAAP 或非 GAAP 口徑事實表未標，分析師家數未列。"},"catalysts":[{"date":"2027-02","date_precision":"month","type":"guidance","event":"2026 Q4 財報，日期未公告","impact":"高","watch":"總營收是否達 8.4 億美元，Tyvaso 年增率，是否重申 40 億美元目標"},{"date":"2027-04","date_precision":"month","type":"regulatory","event":"FDA 對霧化 Tyvaso IPF 補充申請的審查期結束","impact":"高","watch":"是否獲准、適應症範圍、用藥限制"},{"date":"2027-06-24","date_precision":null,"type":"regulatory","event":"ralinepag PAH 新藥審查日","impact":"高","watch":"原料供應商 OAI 是否解除"},{"date":"2027-06","date_precision":"month","type":"product","event":"Orenitram 學名藥最早可上市，12 月第二家","impact":"中","watch":"Orenitram 季營收下滑幅度"},{"date":"2026-12","date_precision":"month","type":"other","event":"Adcirca 授權 2026-12-31 到期不續","impact":"低","watch":"其他收入的減少幅度"}],"decision_out":{"verdict":"進場","role":"衛星","row_hit":"9","pacing":[],"holding_cap":null,"audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場用過去幾季沒有成長的印象定價，FY2027E 只給 16.6 倍；PH-ILD 和解到 10 月中才定案，共識兩次快照都沒動。若快照只是尚未更新，這個理由要打折。"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟢', val='🟡', moat_trend='→', week26=-0.52, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position=None, moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":false,"basis":"signal='B', val='🟡'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":true,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"9-verdict","condition":"命中 row9 → 進場","hit":true,"basis":"row_hit=9"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]}],"requires_critic":[]}}
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
