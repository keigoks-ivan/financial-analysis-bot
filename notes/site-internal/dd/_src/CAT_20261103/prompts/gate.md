你是 DD 管線 v20 的判斷層閘（gate），標的 CAT（20261103）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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
- `f_kpi0_sales_and_revenues_gaap`（q1_business）｜營收（Sales and revenues, GAAP）＝20682 百萬美元｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 caterpillar.com 3Q26 results／8-K Ex.99.1（numbers.latest_quarter_kpis.items[0]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-29））
- `f_kpi1_adjusted`（q1_business）｜Adjusted 營業利益／利益率（排除重組成本）＝20.6 %｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 caterpillar.com 3Q26 results／8-K Ex.99.1（numbers.latest_quarter_kpis.items[1]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-29））
- `f_kpi2_gaap`（q1_business）｜GAAP 營業利益／利益率＝20.4 %｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 caterpillar.com 3Q26 results／8-K Ex.99.1（numbers.latest_quarter_kpis.items[2]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-29））
- `f_kpi3_eps_gaap_adjusted`（q1_business）｜EPS（GAAP／Adjusted）＝7.13 美元｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 caterpillar.com 3Q26 results／8-K Ex.99.1（numbers.latest_quarter_kpis.items[3]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-29））
- `f_peer_cat_gross_margin_pct`（q2_moat）｜CAT 毛利率＝32.65 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CAT.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_earnings_recency`（q1_business）｜最近一次財報日＝2026-10-29 date｜期間與口徑：2026-10-29／距今 3 個交易日｜kind：realized
  - 來源：—（numbers.earnings_recency，as_of 2026-10-29）
- `f_peer_cat_operating_margin_pct`（q2_moat）｜CAT 營業利益率＝17.59 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CAT.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_de_operating_margin_pct`（q2_moat）｜DE 營業利益率＝17.59 %｜期間與口徑：TTM ending 2026-07-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.DE.operating_margin_pct，as_of TTM ending 2026-07-31（4季加總））
- `f_peer_6301_t_operating_margin_pct`（q2_moat）｜6301.T 營業利益率＝13.82 %｜期間與口徑：TTM ending 2026-03-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.6301.T.operating_margin_pct，as_of TTM ending 2026-03-31（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_cnh_operating_margin_pct`（q2_moat）｜CNH 營業利益率＝13.75 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CNH.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_uri_operating_margin_pct`（q2_moat）｜URI 營業利益率＝25.91 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.URI.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_cat_fcf_margin_pct`（q2_moat）｜CAT FCF 利潤率＝11.08 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CAT.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝27.5 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-10-31）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝32.31 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-10-31）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝38.87 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-10-31）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝79548.42 USD m｜期間與口徑：2026-11-03／yfinance revenue_estimate 0y 平均（11 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝88185.58 USD m｜期間與口徑：2026-11-03／yfinance revenue_estimate +1y 平均（17 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi4_me_t_me_t_me_t_me_t_9m_6`（q4_capital）｜ME&T 自由現金流（自算：ME&T 營業現金流 − ME&T 資本支出 − ME&T 租賃設備支出，由 9M 累計減 6M 累計）＝3827 百萬美元｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：8-K Ex.99.1 現金流量表 ME&T 欄：9M 營業現金流 11,534、資本支出 1,993、租賃設備 16；6M（Q2 8-K Ex.99.1）7,011、1,302、11。新聞稿未直接給單季 FCF，此為自算，非公司揭露口徑（numbers.latest_quarter_kpis.items[4]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-29））
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝38099.0 USD m｜期間與口徑：2026-11-03／yfinance 最新一季：總債務 45201.0、現金 7102.0（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝1.012 %｜期間與口徑：2026-11-03／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-11-03）
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝459.67 m shares｜期間與口徑：2026-11-03／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝620.38 USD｜期間與口徑：2026-11-02（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-11-02（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝22.57 x｜期間與口徑：2026-10-31／分母＝FY1 EPS 27.5，分子＝快照價 620.62｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-10-31）
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝24.36 x｜期間與口徑：2026-11-02（RTH 收盤，UTC）／4 個年度端點內的分位＝59.5｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-11-02（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝59.5 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝3.67 x｜期間與口徑：2026-11-02（RTH 收盤，UTC）／4 個年度端點內的分位＝76.6｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝76.6 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝4.16 x｜期間與口徑：2026-11-02（RTH 收盤，UTC）／4 個年度端點內的分位＝76.5｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝76.5 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ev_m`（q5_valuation）｜目前企業價值 EV（市值＋淨負債）＝323382.42 USD m｜期間與口徑：2026-11-03／市值 285283.42 ＋ 淨負債 38099.0｜kind：realized
  - 來源：—（numbers.capital_structure.ev_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝11.25 %｜期間與口徑：2026-07-30 → 2026-10-31／FY1 共識 EPS 24.72 → 27.5（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-10-31）
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝-28.78 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-11-02（RTH 收盤，UTC））
- `f_rsi14`（q5_valuation）｜RSI(14)＝23.72｜期間與口徑：2026-11-02（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ma_w52`（q5_valuation）｜52 週均線＝759.92 USD｜期間與口徑：2026-11-03／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）
- `f_ma_w104`（q5_valuation）｜104 週均線＝572.89 USD｜期間與口徑：2026-11-03／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）

### findings_digest 中方向為負或來源衝突的條目（20 條）
- `competitive_share_entrants#0`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K FY2025 列出全球與中國區域競爭者（Komatsu、Sany、XCMG、LiuGong、SDLG、Shantui 等），並稱競爭強度有時造成特定產業或地區價格折扣、壓縮利潤。
  - 來源：SEC EDGAR 10-K FY2025 Item 1（as_of 2026-02-13）｜affects：moat_trend、decision_inputs.bear
- `competitive_share_entrants#1`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K 風險因子：競爭者積極定價等可能降低公司產業銷售份額。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-13）｜affects：thesis.R、decision_inputs.bear
- `supply_demand_durability#1`（supply_demand_durability｜方向 -｜狀態 ok）：風險面：成長高度依賴資料中心客群，AI 建設暫停會衝擊；長期 backlog 可能被改期或取消。
  - 來源：TIKR, Caterpillar's backlog hits a record $72 billion（as_of 2026-08-01）｜affects：thesis.R、decision_inputs.bear
- `supply_demand_durability#2`（supply_demand_durability｜方向 -｜狀態 ok）：設備業產能擴張：Sany India 董事稱主要建機廠產能近 2–3 年已滿載，各家都在擴產；CNH 印度 Pithampur 擴產 20–25%。
  - 來源：Autocar Pro, Sany India to invest Rs 1000 crore in next 3 years（as_of 2026-06-01）｜affects：thesis.R
- `regulatory_antitrust#1`（regulatory_antitrust｜方向 -｜狀態 ok）：Bobcat 於 2025-12-02 向美國 ITC 提出申訴，指 Caterpillar 違反裝載機、推土機、挖掘機等進口規則（Federal Register 摘要）；尚未讀到頁面，狀態未核。
  - 來源：policyrisk.com 彙整 Federal Register｜Caterpillar Files ITC Complaint Over Heavy Equipment Imports（as_of 2026-05-29）｜affects：thesis.R、decision_inputs.bear
- `regulatory_antitrust#2`（regulatory_antitrust｜方向 -｜狀態 ok）：Baird 於 2026 年 7 月下旬將 CAT 降至 Neutral，理由為各州對資料中心建設的政策阻力（含紐約州新建大型資料中心暫停令，7-14 生效）可能自 2027 年起影響發電業務。
  - 來源：Barchart｜Baird just downgraded Caterpillar stock, here's why（as_of 2026-07-29）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：CAT 預期 2026 年關稅衝擊約 26 億美元，較 2025 年實際高 8 億；若無緩解措施約再高 20%。2025 年營業利潤減少主因為製造成本不利，主要反映關稅上升。
  - 來源：SEC EDGAR 10-K FY2025 Item 7 MD&A（as_of 2026-02-13）｜affects：valuation、decision_inputs.bear、thesis.R
- `reg_tariff_export#1`（reg_tariff_export｜方向 -｜狀態 ok）：2026 年增量關稅成本約 50% 落在 Construction Industries、20% Resource Industries、30% Power & Energy；Q1 2026 預期約 8 億美元。
  - 來源：SEC EDGAR 10-K FY2025 Item 7 MD&A（as_of 2026-02-13）｜affects：valuation、thesis.R
- `reg_tariff_export#2`（reg_tariff_export｜方向 -｜狀態 ok）：10-K 風險因子揭露受 BIS、OFAC、DDTC 等進出口與制裁法規約束，貿易限制可能影響需求、競爭地位或使其無法在特定國家銷售。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-13）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：CAT Q2 2026 10-Q：排除預期 IEEPA 關稅回收，2026 年關稅成本預估約 22 億美元；IEEPA 關稅成本 2025 起至 CBP 停徵累計約 10 億美元；供應鏈關注重點為運輸、部分零組件與原物料。
  - 來源：Caterpillar Form 10-Q (quarter ended 2026-06-30)（as_of 2026-06-30）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：CAT 供應基礎為全球性：超過 600 家海外供應商、約 50 家為關鍵供應商，關稅與貿易爭端被列為零組件流動風險（二手 SWOT 文章轉述 Reuters，2024 年底）。
  - 來源：Investing.com Caterpillar SWOT analysis（as_of 2024-12-31）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#2`（geo_supply_chain｜方向 -｜狀態 ok）：次級分析：CAT 中國曝險與美中貿易關係及中國市場疲弱相關。
  - 來源：Kavout market lens（as_of 2026-01-01）｜affects：thesis.R
- `substitute_technology#1`（substitute_technology｜方向 -｜狀態 ok）：中國挖機出口 2026 上半年成長 33%，三一、中聯、徐工逐步侵蝕 Hitachi、Komatsu、Caterpillar 等國際大廠市占（KHL Yellow Table），產業轉向電動。
  - 來源：SCMP: China's excavator exports surge 33% in first half as industry pivots to electric power（as_of 2026-07-15）｜affects：moat_trend、thesis.R
- `cyclical_supply_discipline_capacity#0`（cyclical_supply_discipline_capacity｜方向 -｜狀態 ok）：Escorts Kubota 於 2026-08-19 在北方邦動土 154 英畝新廠，第一期增加最多 6 萬台曳引機與 1.5 萬台工程機械年產能，投資逾 ₹2,000 億盧比（約 200 億）；現有年產能約 17 萬台曳引機、1 萬台工程機械；完工日期未載明。
  - 來源：themachinemaker.com - Escorts Kubota announces investment plan for new plant（as_of 2026-08-19）｜affects：thesis.R、decision_inputs.bear
- `cyclical_inventory_price_position#2`（cyclical_inventory_price_position｜方向 -｜狀態 ok）：二手營建設備價值因庫存上升而下滑；農機市場處於長期下行但價格仍維持高檔（次級來源摘要）
  - 來源：equipmentfinancenews.com 'Used construction equipment values fall amid rising inventories'（as_of 2026-06-30）｜affects：valuation、decision_inputs.bear
- `cyclical_inventory_price_position#3`（cyclical_inventory_price_position｜方向 -｜狀態 ok）：管理層預期 Q4 Construction Industries 經銷商庫存下降逾 $10 億
  - 來源：Insider Monkey 'Caterpillar (CAT): Can Earnings Keep Growing After Dealers Stop Restocking?'（as_of 2026-10-12）｜affects：triggers、decision_inputs.bear、valuation
- `cyclical_prior_downcycle_behavior#0`（cyclical_prior_downcycle_behavior｜方向 -｜狀態 ok）：CAT 2016 營業利益 $498M，對比 2015 年 $3.785B，主因銷量下滑與產品組合不利，另含 Resource Industries 商譽減損與退休金 MTM 損失
  - 來源：Caterpillar FY2016 10-K / Q3 2016 8-K (SEC)（as_of 2017-02-15）｜affects：thesis.R、decision_inputs.bear
- `cyclical_prior_downcycle_behavior#1`（cyclical_prior_downcycle_behavior｜方向 -｜狀態 ok）：CAT 2020 全年營業利益率 10.9%，2019 年為 15.4%；2020 銷售約下滑 22%
  - 來源：Caterpillar 4Q20 financial results（as_of 2021-01-28）｜affects：thesis.R、decision_inputs.bear
- `cyclical_prior_downcycle_behavior#2`（cyclical_prior_downcycle_behavior｜方向 -｜狀態 ok）：CAT 2015 營收約 $47.0B，較 2014 年降 15%，獲利降 43% 至 $2.1B；Q4 2015 虧損 $87M（去年同期獲利 $757M）
  - 來源：Caterpillar FY2015 10-K (SEC)（as_of 2016-02-15）｜affects：thesis.R、decision_inputs.bear
- `cyclical_prior_downcycle_behavior#3`（cyclical_prior_downcycle_behavior｜方向 -｜狀態 ok）：Motley Fool 稱 CAT 股價 2015 年下跌約 25%
  - 來源：Motley Fool, Will 2016 be Caterpillar Inc's best year yet（as_of 2016-01-02）｜affects：decision_inputs.bear、valuation

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 4 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CAT_20261103/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":1199.0,"bear_5y_price":364.0,"p_bull_pct":23,"p_bear_pct":30,"upside_5y_pct":24.8,"ev5y_pct":20.7,"irr_base_pct":4.5,"asym_ratio":1.7,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":27.5,"pe":22.56,"basis":"FY1＝FY2026E 共識 EPS 27.5 美元（已公布三季）。終端倍數同樣套在終端年當年的 EPS，分母口徑一致。"},"eps":{"bull":[34.0,40.5,45.5,50.0,54.5],"base":[32.0,36.5,36.5,39.5,43.0],"bear":[29.5,25.0,21.5,23.5,26.0]},"pe":{"bull":22,"base":18,"bear":14},"p":{"bull":23,"base":47,"bear":30},"yield_pct":{"dividend":1.012,"net_buyback":1.9},"second_stage":{"bull_cagr_pct":9,"base_cagr_pct":6},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### CAT_Q2_2026_Earnings_Call_20260804.md
- 2026-08-04｜CFO｜guidance：全年銷售與營收成長預期上調至中高十幾%（原話："sales and revenues growth in the mid- to high teens for the"）
- 2026-08-04｜CEO｜guidance：全年調整後營業利益率高於四月預期；排除 IEEPA 退稅後接近目標區間底部（原話："we expect full year adjusted operating profit margin to be"）
- 2026-08-04｜CFO｜guidance：全年關稅成本預估約 22 億美元，在先前區間低端（原話："of around $2.2 billion or at the low end of the range we"）
- 2026-08-04｜CFO｜guidance：Q3 關稅成本預估約 6 億美元（原話："We anticipate tariff costs of around $600 million"）
- 2026-08-04｜CFO｜guidance：財測不含下半年任何額外 IEEPA 退稅（原話："Our outlook does not include any additional IEEPA tariff"）
- 2026-08-04｜CFO｜guidance：MP&E 自由現金流預期上調至年度目標區間（60–150 億）上半部（原話："expect MP&E free cash flow to be in the top half of our"）
- 2026-08-04｜CFO｜guidance：2026 年資本支出約 35 億美元，與先前預期相近（原話："Our CapEx spend for 2026 is anticipated to be approximately"）
- 2026-08-04｜CEO｜guidance：全年服務營收成長率高於先前展望（原話："Services revenues are also expected to grow at a higher rate"）
- 2026-08-04｜CEO｜guidance：下半年產能擴充將提高產出（原話："we expect to increase our throughput in the second half of"）
- 2026-08-04｜CFO｜guidance：Q4 預期 CI 經銷商庫存較典型地下降逾 10 億美元，年底庫存高於去年（原話："We plan to end the year higher than last year"）
- 2026-08-04｜CFO｜guidance：Resource Industries Q3 利潤率預期與去年相近（原話："we anticipate a similar margin percentage"）
- 2026-08-04｜CFO｜margin：Q2 認列 3.92 億美元預期 IEEPA 退稅，多數在 corporate items（原話："we recognized $392 million in expected IEEPA tariff"）
- 2026-08-04｜CFO｜margin：Q2 關稅成本約 4 億，低於四月提供的 7 億估計；原因為先前已發生關稅的計算調整（原話："favorable compared to the $700 million estimate we provided"）
- 2026-08-04｜CFO｜margin：Q2 各 segment 受關稅影響的利潤率bp 拆解（P&E 90bp）（原話："Segment margins were impacted by 90 basis points in Power &"）
- 2026-08-04｜CFO｜margin：P&E Q2 利潤率 24.6%，年增 250bp（原話："margin of 24.6% was an increase of 250 basis points"）
- 2026-08-04｜CFO｜margin：P&E 製造成本受產能擴充支出（含折舊）影響（原話："Higher manufacturing costs were impacted by spend related"）
- 2026-08-04｜CEO｜margin：下半年運費與折舊面臨壓力的說法（原話："We might see a little pressure on freight in the back half"）
- 2026-08-04｜CEO｜commitment：管理層表示有信心長期處理關稅衝擊，目標在利潤率目標區間中點附近運作（原話："I'm confident that we'll manage the impact of tariffs over"）
- 2026-08-04｜CFO｜commitment：承諾持續將幾乎全部 MP&E 自由現金流透過股息與買回還給股東（原話："substantially all of our MP&E free cash flow to our"）
- 2026-08-04｜CFO｜capital_allocation：Q2 買回約 15 億美元，其餘為股息，合計回饋 22 億（原話："Share repurchases accounted for about $1.5 billion"）
- 2026-08-04｜CFO｜capital_allocation：6 月宣布股息增加 8%（原話："In June, we announced an 8% dividend increase,"）
- 2026-08-04｜CEO｜product：重啟 10 MW 中速燃氣往復式引擎，約 1.5 GW 產能，預計 Q4 開始出貨（原話："We plan to bring about 1.5 gigawatts of capacity back online"）
- 2026-08-04｜CEO｜product：該產品 2022 年曾停產，重啟敘事不同於前期（原話："In 2022, we stopped manufacturing this product"）
- 2026-08-04｜CEO｜product：回答分析師：10 MW 機型未計入 2030 年 65 GW 目標（原話："included in the 65. But again, it's a lower volume."）
- 2026-08-04｜CEO｜product：Wamego 工廠改造為渦輪機產能，12 個月內完成（原話："converted the facility in under 12 months"）
- 2026-08-04｜CEO｜product：部分客戶詢問將柴油備用電源改用較小 C32 平台（原話："moving down to the C32 platform"）
- 2026-08-04｜CEO｜customer：管理層稱 AI／資料中心需求無客戶放緩（原話："no one is slowing down at the moment"）
- 2026-08-04｜CEO｜customer：管理層稱未見客戶退出需求（原話："we haven't seen any customers back off of demand"）
- 2026-08-04｜CEO｜customer：開始接受 2029、2030 年訂單（原話："we're starting to take orders into '29 and '30 already."）
- 2026-08-04｜CEO｜customer：油氣積壓訂單年增接近 2 倍（原話："nearly 2x bigger"）
- 2026-08-04｜CEO｜customer：燃氣 prime 與大型引擎交期已排到 2028 後段（原話："we're into '28 in gas prime, late '28 for sure"）
- 2026-08-04｜CEO｜customer：交期延長的說法（原話："We've seen, obviously, lead times start to extend here."）
- 2026-08-04｜CEO｜customer：遠期訂單通常附價格調整條款（原話："we do typically have price escalators on those"）
- 2026-08-04｜CFO｜customer：Cat Financial 逾期率 1.31%（原話："Past dues were 1.31% in the quarter"）
- 2026-08-04｜CEO｜customer：租賃載入成為 CI 銷售給用戶成長的較大部分（原話："rental loading has definitely become a bigger piece"）
- 2026-08-04｜CEO｜competition：Major Projects 為經銷商持有的全國性租賃合資公司（原話："a specialized fully Cat dealer-owned rental joint venture"）
- 2026-08-04｜CEO｜risk：地緣政治不確定性（原話："despite ongoing uncertainty due to geopolitical events"）
- 2026-08-04｜CEO｜risk：中東持續受挑戰，但預期對 EAME 銷售給用戶影響有限（原話："While the Middle East continues to be challenged"）
- 2026-08-04｜CEO｜capital_allocation：新渦輪產能提供者回收期說法：本十年底前現金回收（原話："We said last time we'll have cash payback by the"）
- 2026-08-04｜CEO｜customer：CI 積壓非供給受限，部分取決於產出追上需求（原話："somewhat of a function of us being able to produce to demand"）
- 2026-08-04｜CEO｜customer：住宅等其他 CI 領域疲弱，被視為潛在上行空間（原話："that provide some potential upside for us"）
- 2026-08-04｜CEO｜product：P&E 服務成長多數在 2030 年之後（原話："There will be some between now and 2030"）

### 問答異常語氣（迴避／改口／保留）
- CAT_Q2_2026_Earnings_Call_20260804.md｜問：Jamie Cook：積壓成長中大型專案（如 PROPWR）與廣泛訂單的組成，及 P&E 增量利潤率來源｜答法：未給拆解數字，稱「we don't really kind of talk about the specifics」，改談各 segment 訂單特性與關稅、運費、折舊因素
- CAT_Q2_2026_Earnings_Call_20260804.md｜問：Angel Castillo：10 MW 引擎首批訂單規模與增量成本，及遠期訂單定價｜答法：確認已有首批訂單但未給規模；稱投資「minimal」，定價回答僅提及價格調整條款，未給幅度
- CAT_Q2_2026_Earnings_Call_20260804.md｜問：Rob Wertheimer：2027、2028 是否已售罄、是否保留產能檔期｜答法：未直接說是否售罄，改述交期（gas prime 2028 下半至 2029）及會優先照顧長期油氣客戶、調整排程
- CAT_Q2_2026_Earnings_Call_20260804.md｜問：Mig Dobre：P&E 服務與售後市場的目前規模與占比｜答法：未給規模或占比，只談定性成長機會，主要在 2030 年後

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 2 | 2 |
| customer_second_source | not_applicable | 0 | 1 |
| customer_concentration_credit | found | 2 | 1 |
| supply_demand_durability | found | 4 | 4 |
| regulatory_antitrust | found | 4 | 2 |
| reg_tariff_export | found | 5 | 2 |
| geo_supply_chain | found | 3 | 2 |
| end_markets | found | 3 | 3 |
| substitute_technology | found | 3 | 2 |
| channel_business_model_shift | found | 3 | 3 |
| capital_markets_pricing | found | 5 | 4 |
| major_events | found | 2 | 4 |
| cyclical_supply_discipline_capacity | found | 3 | 3 |
| cyclical_inventory_price_position | found | 4 | 3 |
| cyclical_prior_downcycle_behavior | found | 4 | 3 |

未涵蓋／不適用軸的查詢詞原文（供判相關性）：
- **customer_second_source**（not_applicable）：Caterpillar largest customer concentration dealers 10-K no single customer

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260805","verdict":"觀望","role":"追蹤","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"資料中心自備發電需求在 2029 年前不中斷，且 CAT 能把它轉成 P&amp;E 分部 2026-2029 年化 ≥ 15% 的營收成長"},{"id":"H2","text":"非住宅營建與礦業資本支出在 2027-2028 不同時反轉——CI＋RI 合計約佔營收 55%，需要至少一邊撐住"},{"id":"H3","text":"CAT 能把 2026 年約 20-21% 的調整後營益率，在產能爬坡、折舊上升與 $2.2B 關稅成本下維持到 2028"}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"資料中心監理的州級收緊（但聯邦在鬆綁，方向相反）：紐約州 2026-07-14 通過全美首個資料中心建設暫停令（Responsible Data Center Development Act，20MW 以上州級許可暫停一年，參院 44-16、眾院 102-39；州長另以行政命令針對 50MW 以上超大規模，最長一年，待通用環評完成），六週內 30 多州提出 300+ 件相關法案。反向抵銷項：聯邦層級同期在降低燃氣渦輪的空氣許可負擔（2026-01 新版 NSPS；2025-09 與 2026-05 指引允許動工先於許可核發）。故本風險的正確形狀是「州與聯邦方向相反的監理拉鋸」，不是單向利空"},{"id":"R2","text":"全行業產能同步落地壓垮定價權（分層：往復引擎風險高、渦輪風險低）：CAT 大型往復引擎產能 2030 擴至 2024 近 3 倍、渦輪 2.5 倍；GE Vernova 目標 2030 年產 30GW（現 backlog 116GW、自稱「大致賣光到 2030」）；Cummins 投資 $450M 增 20GW 至 2030 年 55GW 高馬力產能，並訂下 2030 年 $9B 資料中心營收目標；Mitsubishi Power 產能翻倍；INNIO、Wärtsilä 同步擴產。分層依據：重型渦輪的真瓶頸在轉子鍛件與熱端葉片鑄件（全球僅少數幾家供應，製程無法快速擴產，交期已達 5-7 年），故渦輪線的緊缺較持久；而 CAT 的 P&amp;E 成長主體是往復引擎，該線的邊際供給成本由 CAT 自己證明極低（MaK 平台以「幾乎四捨五入等於零的投資」復產 1.5GW、Wamego 廠 12 個月改建完成）"},{"id":"R4","text":"替代技術在超大規模客戶端滲透：Bloom Energy 與 Oracle 於 2026-04 把合作擴大至 2.8GW 固態氧化物燃料電池（部署期 &lt;1 年、效率較燃氣渦輪高 10-30%）——單一合作案規模已超過 CAT 在行為表後 prime power 已公告專案的全部 3.6GW。另有天然氣供應與管線瓶頸（已申報的資料中心天然氣需求約 125GW，2026-01 一次 20% 需求衝擊使 Henry Hub 價格暴漲），可能把部分客戶推向非燃氣方案"},{"id":"R3","text":"CI／RI 雙循環同時反轉：IIJA 授權於 2026-09-30 到期且再授權延宕；美國非住宅營建支出 2026 年 6 月 $745.3B SAAR、已「大致持平」；礦業資本支出對銅金價格高度敏感"}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"價格 ≤ $700（FY27E 我方 build 21x，Base 年化 IRR 回到約 9%）且 backlog 未連 2 季 QoQ 淨下滑；或 FY27E 共識升至 ≥$36 而股價未過 $950（倍數自然消化）","irr_base_pct":4.3,"ev5y_pct":7.3,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"追蹤","signal":"B","val":"🔴","ma":"✅","trap":"🟡","moat_trend":"→","runway_post_y5":"🟢","asym_ratio":0.75,"ev5y_pct":7.3,"irr_base_pct":4.3,"max_dd_pct":-60.0,"bull_5y_price":1276.0,"bear_5y_price":392.0,"p_bull_pct":23.0,"p_bear_pct":30.0,"rearm_trigger":"價格 ≤ $700（FY27E 我方 build 21x，Base 年化 IRR 回到約 9%）且 backlog 未連 2 季 QoQ 淨下滑；或 FY27E 共識升至 ≥$36 而股價未過 $950（倍數自然消化）","price_at_dd":876.54,"archetype":"循環/商品","cycle_position":"晚循環"}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"CAT","date":"2026-11-03","schema":"v15.0","contract":"v19","company_name":"Caterpillar Inc."},"oneliner":"CAT 半年跌 29%，但 FY2026 共識 EPS 三個月上修 11%、在手訂單 780 億美元創高，跌的是倍數不是獲利。以晚循環設備股來看，620 美元的基準五年年化約 5.5%，仍不夠便宜。等 525 美元附近，或 2027 年財測確認利潤率脫離區間底部。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CAT_20261103/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CAT_20261103/scenario.json","answers":{"q1_business":{"verdict":"CAT 賺的是全球營建、採礦、油氣與資料中心業者的設備資本支出，再靠裝機基礎收零件、服務與融資的錢。錢卡在設備經獨立經銷商送到終端這一節。本輪增量集中在資料中心發電。","reasoning":"第三季（2026-10-29 公告）營收 206.82 億美元、年增 17%，GAAP 營業利益率 20.4%、調整後 20.6%，EPS 7.13 美元（調整後 7.20）；TTM 毛利率 32.65%。三大分部（第三季法說 CFO）：P&E 88 億美元（年增 18%，利潤率 24.4%）、營建 80 億（年增 18%，22.9%）、資源 46 億（年增 15%，13.5%），三者都超過營收一成；Financial Products 12 億。收錢方式：設備經 150 家獨立經銷商賣給承包商、礦商、油氣與資料中心業者，零件與服務跟著裝機基礎走，Cat Financial 收融資與租賃利差。單點依賴：10-K 稱沒有單一客戶或經銷商構成重大信用集中；但本輪增量集中在資料中心發電（發電銷售給用戶年增 75%），這是集中度風險，不是護城河證據。產業時鐘判第 III 階段：交期排到 2029–2030、CAT 與同業同步擴產、營建經銷商補庫存與租賃車隊加載、Cat Financial 逾期率 1.31% 為 1998 年以來最低，都是擴張後段的特徵；採礦訂單連 3 季轉強是唯一偏早的部分。","fact_refs":["f_kpi0_sales_and_revenues_gaap","f_kpi1_adjusted","f_kpi2_gaap","f_kpi3_eps_gaap_adjusted","f_peer_cat_gross_margin_pct","f_earnings_recency"],"verdict_values":{"revenue_quality":"以設備銷售為主，受景氣影響大。在手訂單 780 億美元，58% 預計 12 個月內出貨（第三季法說 CFO），能見度比過去高。服務與 Cat Financial 是較穩定的部分，服務占比事實表未涵蓋。","unit_econ_note":"第三季調整後營益率 20.6%，含 1.28 億美元 IEEPA 退稅。管理層稱全年排除退稅後接近目標區間底部：擴產折舊、運費與每季約 6 億美元關稅，抵銷了價格實現。","archetype":{"primary":"循環/商品","secondary":"品質複利成長","confidence":"中","fingerprint":"營收跟著營建、採礦與能源資本支出走，2015–16 年與 2020 年兩次下行時營業利益大跌。資料中心發電與裝機服務是較結構性的第二引擎。"},"industry":{"clock_phase":"III","sd_verdict_source":"營建與採礦的供需屬週期性，未來兩年有反轉風險：第四季營建經銷商去庫存約 16 億美元、二手設備價值下滑、印度建機廠同步擴產。資料中心發電需求屬結構性，但供給可逆性高：CAT 自己把大型往復引擎產能擴到 2024 年近 3 倍，10 MW 機型以極低投資復產；交期一旦縮短，緊缺溢價會先消失。來源：10-Q（2026-06-30）、第三季法說、Autocar Pro、equipmentfinancenews。","bargaining":{"up":"前三大供應商占比事實表未涵蓋。第三季法說提到大型礦卡擴產要與供應商同步爬坡，一座測試台曾停機，顯示供應鏈是產出瓶頸，而不是議價對手。","down":"客戶分散：10-K 稱沒有單一客戶或經銷商構成重大信用集中。產品經 150 家獨立經銷商銷售，庫存由經銷商自負。","geo":"2026 年關稅成本約 22 億美元（不含 IEEPA 退稅），約一半落在營建分部。推土機等品項的 Section 232 關稅於 2026 年 6 月降到 15%，效期到 2027 年底。"},"profit_pool_dir":"利潤池往發電與能源移動：第三季 P&E 利潤 21 億美元、年增 31%，利潤率 24.4% 為三大分部最高，占三大分部利潤約 46%（21 億÷45 億）。","tam_table":{"expanded":false,"reason":"資料中心發電屬新增需求，但事實表沒有 TAM、滲透率或利潤池占比資料，硬要展開只會變成推估。改用在手訂單（780 億美元）與分部營收代替。"}}}},"q2_moat":{"verdict":"護城河方向持平（→）。經銷商網路、裝機基礎的零件服務與融資把客戶綁在 Cat 體系，2026 年三大分部價格實現都為正。但中國廠在海外挖機市場擴張，2025 年價格實現為負，擴大的證據不足。","reasoning":"執行面 8 分：第三季三大分部都量增，價格實現也為正；Major Projects 租賃合資與 Cat Compact 擴大了觸及面。扣分在測試台停機、礦機試車延遲等擴產摩擦。定價面 7 分：2026 年價格實現為正，遠期訂單附價格調整條款（第二季法說 CEO）；但 2025 年價格實現約 −8 億美元，10-K 也承認對手積極定價會拿走份額，定價權隨景氣擺動。三項威脅都屬點對點：中國廠海外擴張、全行業擴產、發電同業擴產。產業態勢三軸裁決為雙向拉鋸：A 競爭惡化（中國挖機出口上半年 +33%、印度擴產）；B 結構轉好（資料中心發電、採礦訂單連 3 季強）；C 關稅與州級資料中心政策兩邊拉扯。報酬持續期：事實表缺投入資本，當期 ROIC 與增量 ROIC 都算不出。四檢查點顯示決策層級的黏著度強，但需求可以延後，價值鏈分配隨景氣擺動。","fact_refs":["f_peer_cat_operating_margin_pct","f_peer_de_operating_margin_pct","f_peer_6301_t_operating_margin_pct","f_peer_cnh_operating_margin_pct","f_peer_uri_operating_margin_pct","f_peer_cat_fcf_margin_pct","f_peer_cat_gross_margin_pct"],"verdict_values":{"moat":{"mechanism":"150 家獨立經銷商（美國 41、海外 109，服務 190 國），加上裝機基礎的售後零件與服務（Helios 連網逾 150 萬台），再加上 Cat Financial 融資與租賃。客戶換牌要同時放棄經銷商維修、零件供應、融資與操作訓練。","execution":8,"pricing":7,"grade":"B","trend":"→","trend_evidence":"營業利益率 TTM 17.59%，與 DE 相同，高於 Komatsu 13.82% 與 CNH 13.75%；FCF 利潤率 11.08% 為五家最高。營建分部銷售給用戶連 7 季成長，管理層稱跑贏產業。2026 年三分部價格實現為正，但 2025 年價格實現約 −8 億美元。執行面與定價面都穩定，判持平；與同業的 ROIC 差距事實表未涵蓋。","competitor_notes":[{"name":"DE","strategy_note":"營業利益率與 CAT 相當，FCF 利潤率較低；營建林業部門在北美中型機種正面競爭。"},{"name":"6301.T","strategy_note":"利潤率低於 CAT，是全球挖機與礦機的主要對手，同樣承受中國廠海外擴張的壓力。"},{"name":"URI","strategy_note":"租賃商，既是客戶也是通路對手，利潤率高於 CAT。CAT 經銷商的 Major Projects 租賃合資直接切入大型專案租賃。"},{"name":"CNH","strategy_note":"利潤率與 FCF 在五家中最低。農機需求 2026 年預期下滑約 5% 並維持低產量，營建機械規模小於 CAT。"},{"name":"三一、徐工、柳工等中國廠","strategy_note":"2026 上半年挖機出口成長 33%，在新興市場以價格與電動化搶份額，是對 CAT 營建分部最主要的份額威脅。"}],"peer_na_reason":"同業 ROIC 與投入資本事實表未涵蓋，只能用利潤率比較。","threats":[{"level":"🟡","text":"中國廠挖機出口 2026 上半年成長 33%，在新興市場以價格與電動化搶份額；北美有關稅與經銷商網路保護。","p":35,"evidence_refs":["substitute_technology#1","competitive_share_entrants#0"]},{"level":"🟡","text":"全行業擴產：三一印度與 CNH 印度廠擴產 20–25%、Escorts Kubota 蓋新廠。下行期供給增加會放大價格折扣，10-K 也承認對手積極定價可能拿走份額。","p":30,"evidence_refs":["supply_demand_durability#2","cyclical_supply_discipline_capacity#0","competitive_share_entrants#1"]},{"level":"🟡","text":"發電端：成長高度依賴資料中心客群，CAT 與同業同步擴產。需求一旦放緩，交期縮短會先吃掉定價。","p":30,"evidence_refs":["supply_demand_durability#1"]}],"roic_durability":{"quadrant":"事實表未涵蓋投入資本，無法定象限；營業利益率 TTM 17.59%、FCF 利潤率 11.08%，在同業中居前。","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者、決策者與付款者多半是同一個客戶（承包商、礦商、資料中心營運商），經銷商是中介。設備是剛需，但可以延後：2015 年營收年減 15%、2020 年銷售約年減 22%，客戶在下行期能把購買往後推。資料中心發電目前很急（訂單排到 2029–2030），但急迫不等於持久。"},{"item":"決策層級","level":"🟢","text":"客戶在車隊層級做決定，換牌要一併放棄經銷商維修、零件供應、Cat Financial 融資與操作訓練。代理讀數：Cat Financial 逾期率 1.31% 為 1998 年以來最低，租約到期轉購買的比率高於歷史平均（第三季法說）。"},{"item":"價值鏈分配","level":"🟡","text":"價值由 CAT 與 150 家獨立經銷商分享，庫存與租賃車隊由經銷商承擔。2025 年價格實現約 −8 億美元，2026 年才轉正，顯示 CAT 拿到的份額隨景氣擺動。發電端同業同步擴產，交期縮短後議價權會回到客戶手上。"},{"item":"社會容忍度","level":"🟡","text":"CAT 產品本身沒有漲價的社會壓力，但下游資料中心的社會容忍度在下降：紐約州對新建大型資料中心設暫停令，Baird 據此降評，指可能自 2027 年起影響發電業務。關稅與出口管制也是政策面的上限。"}],"roiic":"事實表未涵蓋（缺投入資本）","reinvest_rate":"事實表未涵蓋（逐字稿有 2026 年資本支出約 33 億美元，但缺折舊與營運資金變動，算不出淨再投資率）","endo_ceiling":null,"formula_note":"內生成長率＝增量 ROIC×再投資率。事實表缺投入資本、折舊與營運資金變動，兩項都算不出。旁證：管理層承諾把幾乎全部 ME&T 自由現金流還給股東，代表再投資率偏低，成長主要靠價格、產能利用與回購。"}}}},"q3_growth":{"verdict":"五年後跑道寬（🟢）：資料中心發電與裝機基礎服務是有來源的第二條曲線，訂單排到 2029–2030，管理層也稱 P&E 服務成長多在 2030 年後。但前五年的成長主要由景氣與利潤率修復推動，不是靠再投資。","reasoning":"成長拆解：第三季三大分部都是量增加上正向價格實現；回購讓調整後 EPS 年增約 0.15 美元；併購（RPMGlobal、Skycatch）規模小。共識三年 EPS 為 FY2026E 27.5、FY2027E 32.31、FY2028E 38.87 美元。以 FY2025A 18.81 為基期年化 27.4%，但 2025 年營業利益率受關稅壓到 16.5%（2024 年為 20.17%），基期偏低；以 FY2026E 為起點，兩年年化 18.9%。同期共識營收由 FY2025A 676 億增至 FY2027E 882 億，年化 14.2%；EPS 成長快於營收 16.9 個百分點，差額來自利潤率修復與回購。內生上界：事實表缺投入資本、折舊與營運資金，算不出。缺口歸因為利潤率修復（關稅吸收、價格實現、IEEPA 退稅）、淨回購約每年 2% 與產能利用率，不是再投資，因此視為超過上界。跑道：成熟的份額領先者沒有滲透率可算，但五年後的第二條曲線有來源：發電訂單排到 2029–2030、報價延伸到 2030 年後（第三季法說 CEO），P&E 服務成長多在 2030 年後（第二季法說 CEO），大型往復引擎產能 2030 年擴到 2024 年近 3 倍。管理層 2024–2030 年營收年化目標為 6–9%。衰退信號亮 1 項，長期成長性判 🟡。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_kpi0_sales_and_revenues_gaap"],"verdict_values":{"growth":{"driver_mix":"以量與價為主（第三季三分部都量增，價格實現也為正），回購每年約 2%，併購規模小。","runway_years":"不適用：成熟份額領先者沒有滲透率可算，以發電訂單年期（排到 2029–2030）代替。","runway_post_y5":"🟢","endo_ceiling_basis":"事實表缺投入資本、折舊與營運資金變動，增量 ROIC 與再投資率都算不出，內生上界留空。共識 FY2025A→FY2028E 的 EPS 年化 27.4%，明顯來自利潤率修復（2025 年營業利益率 16.5%，2024 年 20.17%）與回購，不是再投資，視為超過上界處理。","segments":[{"item":"Power & Energy","value":"第三季營收 88 億美元、年增 18%，利潤 21 億、利潤率 24.4%；發電銷售給用戶年增 75%。第四季因去年基期高，預期溫和成長。"},{"item":"Construction Industries","value":"第三季營收 80 億美元、年增 18%，利潤 18 億、利潤率 22.9%。第四季經銷商去庫存約 16 億美元，預期銷售與去年相近。"},{"item":"Resource Industries","value":"第三季營收 46 億美元、年增 15%，利潤 6.22 億、利潤率 13.5%。銷售給用戶只成長 4%（礦機出貨與試車延遲），訂單連 3 季強勁。"},{"item":"Financial Products","value":"第三季營收 12 億美元、年增 9%，利潤 2.64 億；逾期率 1.31%，為 1998 年以來最低。"}],"decay_signals":[{"signal":"EPS 成長顯著高於營收成長（差距超過 5 個百分點）","lit":true,"evidence":"共識 FY2025A→FY2027E 的 EPS 年化 31.1%、營收年化 14.2%，差 16.9 個百分點，靠利潤率修復撐起。"},{"signal":"毛利率連 2 季年減","lit":false,"evidence":"第三季調整後營益率年增 310 個基點；TTM 毛利率 32.65%，高於 2025 年的 31.78%。"},{"signal":"核心市占近 12 個月縮減","lit":false,"evidence":"管理層稱營建銷售給用戶跑贏產業。中國廠出口 +33% 屬產業層級資料，沒有 CAT 自身份額數字，列入監測。"},{"signal":"FCF／淨利連 2 年低於 0.75","lit":false,"evidence":"2024 年 0.82、2025 年 0.84。"},{"signal":"停止投資新產能且營收下滑","lit":false,"evidence":"2026 年資本支出約 33 億美元，仍在擴產。"},{"signal":"SBC 占營收、維持性資本支出占比、產業倍數系統性下移","lit":null,"evidence":"事實表未涵蓋。"}],"trap_rating":"🟡（亮 1 項）"}}},"q4_capital":{"verdict":"資本配置中上：幾乎全部 ME&T 自由現金流都以股息與回購還給股東，併購小而聚焦。扣分處在 2026 年的回購多在高價區執行。","reasoning":"FCF／淨利：2024 年 0.82、2025 年 0.84（年報 FCF 88.2 億÷淨利 107.9 億；74.5 億÷88.8 億），轉換尚可但低於 1。第三季 ME&T 自由現金流 38 億美元（自算），同季回饋股東 20 億（回購 12 億、股息近 7.5 億）；第二季回購約 15 億。全年 ME&T 自由現金流預期落在 60–150 億目標區間上半部，2026 年資本支出約 33 億（低於原估 35 億）。公司承諾把幾乎全部 ME&T 自由現金流還給股東，股息連 33 年提高，6 月再加 8%。淨負債 380.99 億美元含 Cat Financial 借款，企業現金 79 億美元，另有 16 億有價證券。近三年現金去向分項與 SBC 金額事實表未涵蓋。扣分處：2026 年回購多在 620–877 美元之間執行，以 FY2026E EPS 27.5 美元計，盈餘收益率只有約 3.1–4.4%。","fact_refs":["f_kpi4_me_t_me_t_me_t_me_t_9m_6","f_net_debt_m","f_dividend_yield_ttm","f_shares_diluted_m","f_consensus_eps_fy1"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":false,"passed":null,"input":"近一年併購（RPMGlobal 早期報導約 7.28 億美元、Skycatch，以及待核准的經銷商 John Fabick）合計不到市值 1%，已實現增量報酬事實表未涵蓋，不計分。"},{"name":"buyback_yield","applicable":true,"passed":false,"input":"以 FY2026E EPS 27.5 美元計，2026 年回購價位約 620–877 美元（本次與前份判斷日股價），盈餘收益率約 3.1–4.4%。10 年期公債殖利率事實表未涵蓋，但上緣 4.4% 要殖利率低於 2.4% 才過關，判不過。"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"第三季回購使平均股數下降，調整後 EPS 因此年增約 0.15 美元（約 2%），股數淨減少。SBC 金額事實表未涵蓋，以淨股數變動判過。"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購撐。第三季回購 12 億、股息近 7.5 億美元，公司承諾把幾乎全部 ME&T 自由現金流還給股東，不需另展開。"}}}},"q5_valuation":{"verdict":"現價 620 美元要求 CAT 在 2028 年交出約 39 美元 EPS（共識），並維持約 16 倍本益比。我的基準比共識保守（FY2028E 36.5 美元、五年後 18 倍），基準五年年化約 5.5%，我不認為現價已經便宜。","reasoning":"現價 620.38 美元（2026-11-02 收盤）。本益比：FY2026E 22.57 倍、FY2027E 約 19.2 倍、FY2028E 約 16.0 倍。Trailing 本益比 24.36 倍，在 4 個年度端點中位於 59.5 分位；P/S 3.67 倍、EV/S 4.16 倍分別在 76.6、76.5 分位；企業價值 3,234 億美元。26 週跌 28.78%，同期 FY1 共識三個月上修 11.25%，所以這是倍數收縮。賣方目標價（8 月資料）575–1,218 美元、均值約 959，高低比約 2.1 倍，分歧沒有超過 2.5 倍。PEG＝22.57÷18.9≈1.19，分母用 FY2026E→FY2028E 年化；以 2025 年為基期算出 0.82，但基期受關稅壓低，不採用。同業倍數事實表未涵蓋，終端倍數只能對照 CAT 自身現值。市場錯在哪：我不認為市場錯。現價仍隱含 FY2028E 共識兌現並給約 16 倍，對晚循環設備股不算保守。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_pe_current","f_pe_percentile","f_ps_current","f_ps_percentile","f_ev_s_current","f_ev_s_percentile","f_ev_m","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_3m_fy1_pct","f_week26_return_pct"],"verdict_values":{"valuation":{"basis":"Forward P/E（FY1＝FY2026E 共識 EPS）","tier":"大型工業設備（建機、礦機、發電）","peers":{"expanded":false,"reason":"事實表的同業對照只有利潤率，沒有同業本益比或企業價值倍數。終端倍數只能對照 CAT 自身現值（FY2026E 22.57 倍、Trailing 24.36 倍），同業倍數錨列為資料缺口。"},"fwd_pe":22.57,"peg":1.19,"percentile_5y":null,"val_light":"🟠","val_light_derivation":"現價 620.38 美元，FY2026E 本益比 22.57 倍、FY2027E 約 19.2 倍、FY2028E 約 16.0 倍。P/S 3.67 倍、EV/S 4.16 倍都在近 4 個年度端點的上緣（約 76–77 分位），Trailing 本益比 24.36 倍在中段（59.5 分位）。基準路徑（FY2031E EPS 43 美元配 18 倍）推出五年後約 774 美元，加股息年化約 5.5%，低於 8%；股價要到約 525 美元，年化才有 9%。故判偏貴一級（🟠），較前份降一級，原因全在股價下跌 29%。五年分位：事實表只有 4 個年度端點，沒有五年分位，留空。","upside_short_pct":3.2,"upside_mid_pct":24.8,"denominator_disputed":false,"denominator_note":"FY2026E EPS 含年初至今約 5.2 億美元的 IEEPA 關稅退款。這筆是一次性收入，稅後約每股 0.87 美元（5.2 億×0.77÷4.6 億股），使本益比分母高估約 3%，不足以改變結論。12 個月目標以 FY2027E 基準 32 美元×20 倍＝640 美元計；中期目標為五年後基準 774 美元。"}}},"q6_how_wrong":{"verdict":"最可能看錯的方向是太保守。若資料中心發電需求延續到 2030 年後，營建循環又比預期晚轉弱，FY2028E 共識 38.87 美元就會兌現，現價只有約 16 倍，會被證明便宜。反方向的錯，是循環下行比 Bear 情境更深。","reasoning":"向上看錯的情況：FY1 共識三個月上修 11.25%，股價卻跌 28.78%；RSI 23.72 處於超賣；平均目標價約 959 美元（8 月資料）高於現價；在手訂單連 4 季三分部都成長。向下看錯的情況：2015–16 年營業利益由 37.85 億掉到 4.98 億美元，而 Bear 只假設 EPS 從高點下滑 27%；若資料中心暫停與營建去庫存同時發生，跌幅可能接近歷史。陷阱判 🟡：衰退信號亮 1 項（EPS 成長快於營收逾 5 個百分點），其餘可查的都沒亮。股價已跌破 52 週均線 759.92 美元，但仍在 104 週均線 572.89 美元之上。","fact_refs":["f_week26_return_pct","f_rsi14","f_consensus_rev_3m_fy1_pct","f_ma_w52","f_ma_w104"],"verdict_values":{"trap":{"verdict":"🟡","label":"成長靠利潤率修復，EPS 增速遠高於營收"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":27.5,"pe":22.56,"basis":"FY1＝FY2026E 共識 EPS 27.5 美元（已公布三季）。終端倍數同樣套在終端年當年的 EPS，分母口徑一致。"},"eps":{"bull":[34.0,40.5,45.5,50.0,54.5],"base":[32.0,36.5,36.5,39.5,43.0],"bear":[29.5,25.0,21.5,23.5,26.0]},"pe":{"bull":22,"base":18,"bear":14},"p":{"bull":23,"base":47,"bear":30},"yield_pct":{"dividend":1.01,"net_buyback":1.9},"second_stage":{"bull_cagr_pct":9,"base_cagr_pct":6},"max_dd":{"lo":-55,"hi":-40,"basis":"從現價起算。①歷史：2015 年營收年減 15%、獲利年減 43%，2016 年營業利益只剩 4.98 億美元（2015 年為 37.85 億）；2020 年營業利益率由 15.4% 降到 10.9%；2015 年股價跌約 25%。②淺端 −40%：只有營建下行、資料中心未停，EPS 由 29.5 美元跌約 20% 至 23.6，配 16 倍約 378 美元。③深端 −55%：資料中心暫停與營建去庫存同時發生並出現超跌，EPS 21.5 美元配 13 倍，約 280 美元。Bear 終點（364 美元，−41%）落在範圍內。","trigger_time":null},"basis":{"bull":"資料中心發電需求延續到 2030 年後、採礦上行、營建只小幅停頓；調整後營益率回到目標區間中點，FY2031E EPS 54.5 美元。終端 22 倍，約等於現值 FY2026E 倍數，反映發電占比提高。","base":"FY2027E 32.0 美元，接近共識 32.31；FY2028E 36.5，低於共識 38.87（營建通路加載回吐、折舊上升）；FY2029 營建循環停頓，EPS 持平；之後隨發電與服務成長到 FY2031E 43.0。五年 EPS 年化約 9.4%，約由營收 6–7% 與回購約 2% 組成。終端 18 倍為晚循環到中循環的倍數，低於現值 22.6 倍。EPS 為每股口徑，已含回購減少的股數。","bear":"資料中心建設暫停，疊加營建去庫存與採礦停滯，FY2029E EPS 跌到 21.5 美元，較 FY2027E 高點下滑 27%；因服務與發電占比較高，跌幅輕於 2015–16 年。FY2031E 恢復到 26。終端 14 倍＝成長熄火到 5–10% 時的倍數。"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"資料中心建設面臨州級政策阻力：紐約州 7 月對新建大型資料中心設暫停令，Baird 7 月下旬據此降評，指可能自 2027 年起影響發電業務。長期訂單有被改期或取消的風險；第三季法說中，分析師也提到市場對交易對手信用的疑慮。","assumption":"P&E 帶動的 780 億美元在手訂單（部分排到 2029–2030）能如期轉成營收。","consequence":"P&E 第三季占三大分部利潤約 46%。若資料中心建設放緩，營收與利潤率會同時下滑，倍數由 22 倍壓到 14 倍，五年後股價約 364 美元（−41%）。","ruling":"採納：Bear 機率設 30%，唯一致命點設為在手訂單季減。但目前沒有取消的證據：管理層稱客戶未改變時程，框架協議也延伸到在手訂單之外，所以不提高到 35%。","watch":"每季在手訂單、12 個月內出貨比例（目前 58%）、州級暫停令是否擴散","evidence_refs":["supply_demand_durability#1","regulatory_antitrust#2"],"fact_refs":["f_kpi0_sales_and_revenues_gaap"]},{"view":"論點失敗","evidence":"營建分部的成長有一部分是通路與租賃車隊加載：上半年經銷商庫存增加 26 億美元，第四季要去化約 16 億（去年同期 6 億），二手營建設備價值也隨庫存上升而下滑。","assumption":"營建銷售給用戶的 20% 成長反映真實的終端需求。","consequence":"2027 年營建分部可能出現「終端仍好、出貨下滑」的落差；基準情境已在 FY2029 放進停頓。","ruling":"部分採納。管理層稱排除租賃加載後成長仍強，年底經銷商庫存會比 2025 年多約 7 億美元以備 2027 年，這屬未證的說法。預先登記：2027 年營建銷售給用戶連 2 季年減，即視為這個說法被推翻。","watch":"營建分部銷售給用戶年增率、年底經銷商庫存","evidence_refs":["cyclical_inventory_price_position#3","cyclical_inventory_price_position#2"],"fact_refs":["f_kpi0_sales_and_revenues_gaap"]},{"view":"論點成功但股東經濟變差","evidence":"2026 年關稅成本約 22 億美元（不含 IEEPA 退稅），一半落在營建分部。擴產帶來的折舊與運費上升，讓調整後營益率（排除退稅）停在目標區間底部。往復引擎產能 2030 年擴到 2024 年近 3 倍，同業與印度建機廠也同步擴產。","assumption":"發電需求成長能帶來更高的利潤率。","consequence":"營收照計畫成長，但新增產能的報酬被關稅、折舊，以及交期縮短後的價格競爭吃掉；EPS 成長落在營收附近，倍數不會擴張。","ruling":"採納：基準終端倍數 18 倍低於現值 22.6 倍，基準 FY2028E 36.5 美元也低於共識 38.87。","watch":"調整後營益率（排除退稅）、單季關稅成本","evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","geo_supply_chain#0"],"fact_refs":["f_kpi1_adjusted"]},{"view":"價格已反映太多","evidence":"股價已跌 29%，但仍是 FY2026E 的 22.57 倍，P/S 3.67 倍也在近 4 個年度端點的上緣。過去兩次下行：2015 年營收年減 15%、獲利年減 43%，2016 年營業利益只剩 4.98 億美元；2020 年營業利益率由 15.4% 降到 10.9%；2015 年股價跌約 25%。","assumption":"現在的 EPS 是可以持續的中循環水準。","consequence":"循環股在獲利高點時，本益比看起來不貴；一旦下行，EPS 與倍數會一起掉，回撤可到 −40%～−55%。","ruling":"採納：維持不進場，首倉價位設在 525 美元。","watch":"股價相對 525 美元、總營收年增率","evidence_refs":["cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#1","cyclical_prior_downcycle_behavior#2","cyclical_prior_downcycle_behavior#3"],"fact_refs":["f_fwd_pe_latest","f_ps_percentile","f_week26_return_pct"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 876.54 → 本次 620.38（-29.2%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=876.54","side_b":"本次 price_at_dd=620.38","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 876.54 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 876.54 美元：Bull 價 1,276、Bear 價 392，五年期望值 +7.3%，基準年化 4.3%，不對稱比 0.75","side_b":"本次情境、股價仍用 876.54 美元：Bull 價 1,199、Bear 價 364，五年期望值 −14.6%，基準年化 −2.5%，不對稱比 0.48","ruling":"先換情境、股價不動：五年期望值少 21.9 個百分點，基準年化少 6.8 個百分點。不對稱比由 0.75 變為 0.48。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 876.54 美元：五年期望值 −14.6%，基準年化 −2.5%，不對稱比 0.48","side_b":"本次情境、股價 620.38 美元：五年期望值 +20.7%，基準年化 4.5%，不對稱比 1.73","ruling":"再換股價、情境不動：起點價下跌 29.2%，五年期望值多 35.3 個百分點，基準年化多 7.0 個百分點，不對稱比由 0.48 升到 1.73。合計五年期望值比前份多 13.4 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"股價下跌與估值結論","cause":"價格變動","prior_field":["val"],"side_a":"前份（2026-08-05，股價 876.54 美元）估值判最貴一級，裁決觀望、角色追蹤","side_b":"本次股價 620.38 美元（−29%），FY2026E 本益比 22.57 倍，估值判偏貴一級；裁決與角色依本次輸入重新排定","ruling":"估值改善一級，全部來自股價下跌：同期 FY1 共識 EPS 三個月上修 11.25%，跌的是倍數不是獲利。基準五年年化約 5.5%，仍低於 8%，改善幅度不足以翻成進場。","evidence_level":"事實表股價與共識快照","settle_metric":"股價相對 525 美元","if_then":["若股價 ≤525 美元且總在手訂單未連 2 季季減→首倉 2%，分兩批","若股價反彈到 760 美元（52 週均線）以上而 2027 年財測未上修→不追"],"evidence_refs":[]},{"axis":"首倉價位與情境樹方法","cause":"方法變動","prior_field":["rearm_trigger","p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"價格 ≤ $700（FY27E 我方 build 21x，Base 年化 IRR 回到約 9%）且 backlog 未連 2 季 QoQ 淨下滑；或 FY27E 共識升至 ≥$36 而股價未過 $950（倍數自然消化）","side_b":"股價 ≤525 美元（FY2027E 約 16 倍、基準五年年化約 9%）且總在手訂單未連 2 季季減","ruling":"舊門檻用 FY27E 一年期 21 倍，等於把晚循環的高點獲利配上偏高的倍數。本次改用五年基準路徑：FY2029 營建循環停頓，FY2031E EPS 43 美元配 18 倍。基準年化 9% 對應約 525 美元，首倉門檻因此由 700 下移到 525。機率維持 23／47／30；最大回撤改由現價起算，為 −40%～−55%（前份的 −60% 含已發生的 29% 跌幅）。這是方法改變，不是看法轉壞：同期共識上修、在手訂單續增。","evidence_level":"方法","settle_metric":"基準五年年化報酬","if_then":["若 2027 年 1 月財測讓基準 FY2027E 上調到 33 美元以上→首倉價位隨基準重算上移，約 545 美元","若基準下修→首倉價位同步下移，不因舊門檻已觸發而首倉"],"evidence_refs":[]},{"axis":"前份首倉條件已成立","cause":"價格變動","prior_field":["rearm_trigger"],"side_a":"前份條件：股價 ≤700 美元，且在手訂單未連 2 季季減","side_b":"本次股價 620.38 美元；在手訂單由第二季 720 億增至第三季 780 億美元，條件成立","ruling":"條件成立後依規則重跑研究，不直接建倉。重跑結果：基準五年年化約 5.5%，低於舊條件預設的約 9%；差異來自情境樹的方法改變（見上一條），所以本次不首倉。","evidence_level":"事實表股價與第三季法說","settle_metric":"股價與總在手訂單","if_then":["若股價續跌到 525 美元且在手訂單仍未季減→首倉 2%","若在手訂單先出現季減→不首倉，等下一季確認"],"evidence_refs":[]},{"axis":"進場訊號、陷阱、護城河、跑道、歸類、循環位置維持不變","cause":"新證據","prior_field":["signal","trap","moat_trend","runway_post_y5","archetype","cycle_position"],"side_a":"前份：進場訊號 B、陷阱 🟡、護城河方向 →、五年後跑道 🟢、循環/商品、晚循環","side_b":"本次相同","ruling":"新證據逐項檢視後不改。①陷阱維持 🟡：衰退信號只亮 EPS 成長快於營收一項。②護城河方向維持持平：2026 年三分部價格實現轉正，但中國廠海外擴張、2025 年價格實現為負，擴大與縮減都證據不足。③跑道維持 🟢：管理層第二季稱 P&E 服務成長多在 2030 年後，第三季稱報價延伸到 2030 年後。④歸類維持循環：2015–16 年與 2020 年的下行紀錄仍是主要風險。⑤循環位置維持晚循環：營建通路與租賃加載、二手價下滑、Cat Financial 逾期率創 1998 年以來低點，採礦訂單轉強只能部分抵銷。⑥進場訊號維持 B：估值改善一級，但股價已跌破 52 週均線，週線轉弱。","evidence_level":"10-K、10-Q、第二與第三季法說","settle_metric":"營建價格實現與在手訂單","if_then":["若營建價格實現連 2 季為負→護城河方向改判向下，終端倍數降到 16 倍","若第四季營建銷售給用戶年減→循環位置維持晚循環，首倉價位下移到 500 美元"],"evidence_refs":["substitute_technology#1","cyclical_inventory_price_position#2"]},{"axis":"Single Thing 新設","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設定唯一致命點（null）","side_b":"大型資料中心或主力發電客戶取消或大幅延後訂單，使總在手訂單出現單季淨減少","ruling":"前份把風險分散寫在多條風險項目中。本次依敏感度挑出數學上影響最大的一項：P&E 占三大分部利潤約 46%，也是股價倍數高於一般循環股的唯一支撐；一旦發生，EPS 與倍數同時下修。觸發即不建倉，持有者減碼一半。","evidence_level":"第三季法說分部利潤","settle_metric":"總在手訂單季變動","if_then":["若總在手訂單單季季減→不建倉，持有者減碼一半","若在手訂單連 4 季續增且 12 個月內出貨比例不降→Bull 機率上調到 28%"],"evidence_refs":["supply_demand_durability#1"]},{"axis":"清倉／減碼指標新設","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設清倉或減碼指標（null）","side_b":"總在手訂單連 2 季季減；調整後營益率 2027 年任兩季年減或全年低於 18%；營建銷售給用戶連 2 季年減；P&E 營收連 2 季年增低於 10%","ruling":"前份只有首倉條件，沒有退出條件。本次補上四項，對應唯一致命點與兩條 2 年期假設：任一項觸發即減碼一半，兩項同時觸發即清倉。","evidence_level":"方法","settle_metric":"四項指標","if_then":["若任一指標觸發→減碼一半","若兩項同時觸發→清倉"],"evidence_refs":[]},{"axis":"管理層對利潤率中點的承諾時程","cause":null,"side_a":"2026-08-04 第二季法說 CEO：有信心長期處理關稅衝擊，目標是在利潤率目標區間的中點附近運作","side_b":"2026-10-29 第三季法說 CEO：因為目標區間隨營收上移，利潤率「在底部彈跳」，未來幾年才設法回到中點；全年排除退稅後仍在區間底部","ruling":"可調和，屬程度差異：方向沒變，但回到中點的時間由「長期」具體化為「未來幾年」，等於延後。不採信也不否定，列為未證，以 2027 年財測驗證。","evidence_level":"逐字稿","settle_metric":"2027 年調整後營益率（排除退稅）","if_then":["若 2027 年財測的營益率仍指向區間底部→基準 FY2028E 下修到 35 美元，首倉價位下移到約 505 美元","若 2027 年上半年調整後營益率年增 ≥100 個基點→基準上修，首倉價位上移"],"evidence_refs":[]},{"axis":"管理層對在手訂單的說法","cause":null,"side_a":"2026-08-04 第二季法說 CEO：資料中心客戶「沒有人在放慢」，已開始接 2029、2030 年的訂單","side_b":"2026-10-29 第三季法說 CEO：不要只看單季在手訂單或訂單出貨比，之後在手訂單會不規則；Baird 分析師指出訂單出貨比由年初約 1.7 降到約 1.3","ruling":"可調和：訂單出貨比仍大於 1，在手訂單也仍在增加；但管理層已開始預先降低市場對在手訂單的期待，列入唯一致命點監測。","evidence_level":"逐字稿","settle_metric":"第四季訂單出貨比與總在手訂單","if_then":["若第四季訂單出貨比低於 1 且在手訂單季減→持有者減碼一半，不建倉","若第四季訂單出貨比 ≥1.2→維持基準"],"evidence_refs":["supply_demand_durability#1"]},{"axis":"產業態勢三軸","cause":null,"side_a":"A 競爭惡化：中國挖機出口 2026 上半年 +33%，印度建機廠同步擴產，10-K 承認對手積極定價可能拿走份額","side_b":"B 結構轉好：資料中心發電需求、採礦訂單連 3 季強、在手訂單三分部連 4 季增加。C 其他結構變數：關稅（2026 年約 22 億美元）、出口管制、州級資料中心暫停令","ruling":"雙向拉鋸：發電與採礦往好，營建的競爭與供給往壞，政策兩邊都有（一邊是 Section 232 降稅與 IEEPA 退款，一邊是州級暫停令）。對 CAT 的淨效果目前偏正，但不足以支撐高於現值的倍數。","evidence_level":"10-K、SCMP、Autocar Pro、Barchart","settle_metric":"營建價格實現與發電在手訂單","if_then":["若中國廠份額擴張延伸到北美，或營建價格實現轉負→終端倍數降到 16 倍","若州級暫停令擴散到 3 州以上→Bear 機率提高到 35%"],"evidence_refs":["substitute_technology#1","supply_demand_durability#2","competitive_share_entrants#1","reg_tariff_export#2","regulatory_antitrust#2"]},{"axis":"現在就買的最強論證","cause":null,"side_a":"FY1 共識三個月上修 11.25%，股價卻跌 28.78%，RSI 23.72 超賣；FY2028E 本益比只有約 16 倍；在手訂單 780 億美元、年增 96%，發電訂單排到 2029–2030；平均目標價約 959 美元","side_b":"晚循環設備股在獲利高點用遠期本益比看，會顯得便宜；營建通路加載要回吐，營益率仍在區間底部，基準五年年化約 5.5%","ruling":"不採納進場。遠期 16 倍建立在 FY2028E 共識 38.87 美元上，這個數字需要「營益率脫離底部」與「營建不轉弱」兩件事同時成立。在 2027 年 1 月財測驗證之前，用價格換取安全邊際（525 美元）。","evidence_level":"事實表與逐字稿","settle_metric":"2027 年財測與股價","if_then":["若 2027 年 1 月財測讓基準上修，且重算後的首倉價位高於當時股價→首倉 2%","若股價未到首倉價位就回到 760 美元以上→不追"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"股價 ≤525 美元且總在手訂單未連 2 季季減：重跑後基準年化 ≥9% 即首倉 2%，分兩批","type":"估值rearm","maps_to":"H1","metric":"股價；總在手訂單","threshold":"≤525 美元；不連 2 季季減","action":"首倉 2%，分兩批","source_freq":"股價每日；在手訂單每季","date":null,"evidence_refs":[]},{"n":2,"text":"總在手訂單單季淨減少，或管理層揭露大型資料中心訂單取消或延後","type":"Single Thing","maps_to":"R1","metric":"總在手訂單（2026 年第三季 780 億美元）","threshold":"單季季減","action":"不建倉；持有者減碼一半","source_freq":"每季財報","date":null,"evidence_refs":["supply_demand_durability#1","regulatory_antitrust#2"]},{"n":3,"text":"2027 年 1 月第四季財報與 2027 年財測：看營收成長是否 ≥8%、調整後營益率是否脫離區間底部","type":"複審日期","maps_to":"H2","metric":"2027 年營收與調整後營益率財測","threshold":"營收 ≥8%；營益率指引高於 2026 年排除退稅後的水準","action":"符合就把基準 FY2027E 上調到 33 美元，並重算首倉價位；不符合則維持","source_freq":"一次性","date":"2027-01","evidence_refs":[]},{"n":4,"text":"營建分部銷售給用戶連 2 季年減，或 2026 年底營建經銷商庫存低於 2025 年底","type":"風險","maps_to":"R2","metric":"營建分部銷售給用戶年增率；經銷商庫存","threshold":"連 2 季為負；年底庫存低於 2025 年底","action":"基準 FY2027E EPS 下修到 30 美元，首倉價位同步下移","source_freq":"每季","date":null,"evidence_refs":["cyclical_inventory_price_position#3","cyclical_inventory_price_position#2"]},{"n":5,"text":"單季關稅成本（排除 IEEPA 退稅）超過 8 億美元，或 Section 232 降稅在 2027 年底到期後未延長","type":"風險","maps_to":"R5","metric":"單季關稅成本","threshold":"超過 8 億美元（第三季約 6 億）","action":"基準每年 EPS 下修約 1.3 美元，首倉價位同步下移","source_freq":"每季","date":"2027-12","evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","reg_tariff_export#2","geo_supply_chain#0"]},{"n":6,"text":"營建分部價格實現連 2 季為負，或管理層不再稱銷售給用戶跑贏產業","type":"風險","maps_to":"R4","metric":"營建分部價格實現","threshold":"連 2 季為負","action":"護城河方向改判向下，終端倍數降到 16 倍","source_freq":"每季","date":null,"evidence_refs":["substitute_technology#1","competitive_share_entrants#0","competitive_share_entrants#1"]},{"n":7,"text":"總營收連 2 季年減 ≥10%，或單季營業利益率低於 15%","type":"風險","maps_to":"R3","metric":"總營收年增率；營業利益率","threshold":"連 2 季 ≤−10%；單季低於 15%","action":"Bear 機率提高到 40%，首倉價位下移到 450 美元","source_freq":"每季","date":null,"evidence_refs":["cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#1","cyclical_prior_downcycle_behavior#2","cyclical_prior_downcycle_behavior#3"]},{"n":8,"text":"P&E 分部營收 2027 年連 2 季年增低於 10%","type":"假設驗證","maps_to":"H1","metric":"P&E 分部營收年增率","threshold":"連 2 季低於 10%","action":"Bull 機率下修到 18%，基準 FY2028E 下修到 35 美元","source_freq":"每季","date":null,"evidence_refs":[]}],"kill_metrics":[{"metric":"總在手訂單季變動","bear_threshold":"連 2 季季減，或單季季減 ≥5%","window":"2026 第四季至 2027 第四季","source":"公司季報新聞稿與法說","last_status":"ok"},{"metric":"調整後營業利益率（排除 IEEPA 退稅）","bear_threshold":"2027 年任兩季年減，或全年低於 18%","window":"2027 全年","source":"公司季報新聞稿","last_status":"ok"},{"metric":"營建分部銷售給用戶年增率","bear_threshold":"連 2 季年減","window":"2026 第四季至 2027 第三季","source":"季報新聞稿與 SEC 銷售給用戶申報","last_status":"ok"},{"metric":"P&E 分部營收年增率","bear_threshold":"連 2 季低於 10%","window":"2027 全年","source":"公司季報新聞稿","last_status":"warning"}],"evidence_dismissed":[{"ref":"regulatory_antitrust#1","reason":"同一筆資料裡，標題寫 Caterpillar 提出 ITC 申訴，內文卻寫 Bobcat 對 Caterpillar 申訴，誰是申訴方互相矛盾。來源是彙整站，頁面未讀、狀態未核，無法判定 CAT 是被告還是原告，不能當成風險證據。"},{"ref":"geo_supply_chain#1","reason":"這是二手 SWOT 文章轉述 2024 年底 Reuters 的數字，沒有附原始來源。同一主題已有 2026 年 10-Q 的一手關稅成本（約 22 億美元）納入關稅風險，這條沒有提供新的、可監測的數字。"},{"ref":"geo_supply_chain#2","reason":"次級評論沒有數字，也沒給 CAT 的中國營收占比。第三季法說顯示中國業務從低基期成長、10 噸以上挖機產業全年成長，方向與該文相反。"}],"action_conditions":{"rearm_trigger":"股價 ≤525 美元（FY2027E 約 16 倍、基準五年年化約 9%）且總在手訂單未連 2 季季減","exec_line":"觀望。唯一卡住的條件是估值：現價的基準五年年化約 5.5%。股價 ≤525 美元且在手訂單未連 2 季季減時重跑研究，基準年化 ≥9% 才首倉 2%，分兩批。若總在手訂單先出現季減，即使價格到位也不進場。","holding_cap":"首倉 2%，上限 3%（晚循環設備股，要有深回撤的心理準備）"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":"晚循環","cycle_verdict":"未觸發","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":false,"qc49_inherit_prior":false,"wait_for_price":true,"wait_for_price_condition":"等股價 ≤525 美元且總在手訂單未連 2 季季減；或 2027 年 1 月財測讓基準 EPS 上修，使現價的基準五年年化達到 9%。","qc48_result":"fail","qc48_note":"Bull 的 EPS 路徑推不回量乘以價的數字，沒有算術骨架，所以 Bull 依據不成立；五年後的成長跑道只有管理層口述的訂單年限支撐，歷史上高評價進場後的五年報酬也沒有對照過。"},"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":true,"basis":"signal='B', runway='🟢', val='🟠', moat_trend='→', week26=-28.78, valuation_dependent=False"},{"row":"8a-QC48","condition":"row 8a 命中須經 QC-48 爆發候選 Bull 冷讀；critic 未放行（fail／not_run）→ 落 row 8","hit":true,"basis":"qc48_result='fail', 結論='Bull 的 EPS 路徑推不回量乘以價的數字，沒有算術骨架，所以 Bull 依據不成立；五年後的成長跑道只有管理層口述的訂單年限支撐，歷史上高評價進場後的五年報酬也沒有對照過。'"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='循環/商品', cycle_position='晚循環', moat='B', moat_trend='→', cycle_gates_pass=False"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":true,"basis":"signal='B', val='🟠'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":false,"basis":"signal='B', val='🟠', ma='🟡'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟠', ma='🟡'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟠', ma='🟡'"},{"row":"QC-49","condition":"qc49_inherit_prior=False，不套用","hit":false,"basis":"qc49_inherit_prior=False"},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":null,"requires_critic":[]},"thesis":{"H":[{"id":"H1","text":"資料中心與油氣帶動的發電需求，能把在手訂單轉成營收：P&E 分部 2027 年營收年增 ≥15%，總在手訂單不連 2 季季減","2y":"P&E 營收年增 ≥15%（2026 年第三季為 18%）","5y":null,"10y":null,"threshold":"P&E 季營收年增 ≥15%；總在手訂單（780 億美元）不連 2 季下滑","source":"公司季報新聞稿與法說（每季）","drift_rule":"2 年期：P&E 年增率 TTM 偏離門檻連 2 季 ≥5% 視為削弱，連 3 季 ≥10% 視為反轉"},{"id":"H2","text":"擴產折舊、運費與關稅被價格實現吸收，調整後營益率（排除 IEEPA 退稅）在 2027 年脫離目標區間底部","2y":"2027 年各季調整後營益率年增 ≥0","5y":null,"10y":null,"threshold":"2027 年第三季調整後營益率 ≥20.6%，全年高於 2026 年排除退稅後的水準","source":"公司季報新聞稿、2027 年 1 月財測","drift_rule":"2 年期：TTM 營益率偏離門檻連 2 季 ≥5% 視為削弱，連 3 季 ≥10% 視為反轉"},{"id":"H3","text":"發電與服務占比提高，讓下一次營建與採礦下行時的獲利底部，高於過去兩次","2y":null,"5y":"下行年度營業利益率 ≥15%","10y":null,"threshold":"任何年度營收年減 ≥10% 時，全年營業利益率仍 ≥15%（2020 年為 10.9%；2016 年營業利益只有 4.98 億美元）","source":"年報 10-K","drift_rule":"5 年期：連 4 季偏離 ≥5% 視為削弱，連 6 季 ≥10% 視為反轉"}],"R":[{"id":"R1","text":"資料中心建設放緩：州級暫停令（紐約州 7 月）與 AI 資本支出消化，導致發電訂單改期或取消","h_ref":"H1","clock":"🔥","threshold":"總在手訂單連 2 季季減，或管理層揭露大型訂單延後或取消","evidence_refs":["supply_demand_durability#1","regulatory_antitrust#2"]},{"id":"R2","text":"營建通路與租賃車隊加載回吐：上半年經銷商庫存增加 26 億美元，第四季去化約 16 億，二手營建設備價值下滑","h_ref":"H3","clock":"⚡","threshold":"營建分部銷售給用戶連 2 季年減，或 2026 年底經銷商庫存低於 2025 年底","evidence_refs":["cyclical_inventory_price_position#2","cyclical_inventory_price_position#3"]},{"id":"R3","text":"營建與採礦同時下行，重演 2015–16 年（營收 −15%、獲利 −43%）或 2020 年（營益率由 15.4% 降到 10.9%）","h_ref":"H3","clock":"🔥","threshold":"總營收連 2 季年減 ≥10%，或單季營業利益率低於 15%","evidence_refs":["cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#1","cyclical_prior_downcycle_behavior#2","cyclical_prior_downcycle_behavior#3"]},{"id":"R4","text":"中國廠海外擴張與全行業擴產壓低營建機械價格：中國挖機出口上半年 +33%，三一印度、CNH、Escorts Kubota 都在擴產","h_ref":"H2","clock":"🐢","threshold":"營建分部價格實現連 2 季為負，或管理層不再稱銷售給用戶跑贏產業","evidence_refs":["substitute_technology#1","competitive_share_entrants#0","competitive_share_entrants#1","supply_demand_durability#2","cyclical_supply_discipline_capacity#0"]},{"id":"R5","text":"關稅與貿易限制：2026 年關稅成本約 22 億美元（一半在營建），Section 232 降稅 2027 年底到期，出口管制可能讓部分市場無法銷售","h_ref":"H2","clock":"🔥","threshold":"單季關稅成本（排除退稅）超過 8 億美元，或 Section 232 降稅未延長","evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","reg_tariff_export#2","geo_supply_chain#0"]}],"single_thing":{"description":"大型資料中心或主力發電客戶取消或大幅延後訂單，使總在手訂單（2026 年第三季 780 億美元）出現單季淨減少","why_fatal":"P&E 第三季利潤 21 億美元，占三大分部利潤約 46%，也是市場給 CAT 高於一般循環股倍數的唯一理由。訂單一旦轉為減少，EPS 與倍數會同時往下，Bear 路徑就從 30% 的機率變成主要路徑。","if_happens":"不建倉；持有者減碼一半，終端倍數改用 14 倍重算","how_monitor":"每季在手訂單，以及 12 個月內出貨的比例（第三季 58%、前季 59%）；法說中關於訂單延後、取消或交貨時段調動的說法；州級資料中心暫停令是否擴散","probability":"約 20%（12–24 個月）。管理層稱客戶沒有放慢，且有框架協議；但訂單出貨比已由約 1.7 降到約 1.3，紐約州也已立暫停令。"}},"appendix_a":{"growth_durability":6,"quality_score":7,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":19.2,"peg_fy2":1.02,"stress":{"pass":null,"total":null}},"eps_meta":{"base_eps_path":{"FY2025A":18.81,"FY2026E":27.5,"FY2027E":32.31,"FY2028E":38.87},"fy_end_month":12,"eps_basis":"FY2025A 為年報稀釋 GAAP EPS；FY2026E–FY2028E 為 Koyfin 共識快照（2026-10-31），分析師家數事實表未涵蓋。共識可能是調整後口徑，與 GAAP 基期有口徑差。"},"catalysts":[{"date":"2027-01","date_precision":"month","type":"guidance","event":"第四季財報與 2027 年財測（管理層稱 1 月詳談 2027 年）","impact":"高","watch":"營收成長，以及調整後營益率是否脫離目標區間底部"},{"date":"2026-12","date_precision":"quarter","type":"product","event":"10 MW MaK 中速燃氣引擎首批出貨（第四季）","impact":"低","watch":"2027 年產量爬坡"},{"date":"2027-12","date_precision":"month","type":"regulatory","event":"推土機等品項的 Section 232 關稅 15% 優惠到期","impact":"中","watch":"是否延長"}]}
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
