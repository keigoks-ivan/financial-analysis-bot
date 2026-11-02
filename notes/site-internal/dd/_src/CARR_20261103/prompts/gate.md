你是 DD 管線 v20 的判斷層閘（gate），標的 CARR（20261103）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（47 條）
- `f_kpi0_net_sales_gaap`（q1_business）｜Net sales (GAAP)＝6263 USD m｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 https://www.carrier.com/us/en/news/corporate/2026/carrierreports-third-quarter-2026-results/（同 SEC 8-K Ex.99）（numbers.latest_quarter_kpis.items[0]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-29））
- `f_kpi1_adjusted_operating_profi`（q1_business）｜Adjusted operating profit＝1091 USD m｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 https://www.carrier.com/us/en/news/corporate/2026/carrierreports-third-quarter-2026-results/（同 SEC 8-K Ex.99）（numbers.latest_quarter_kpis.items[1]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-29））
- `f_kpi2_adjusted_operating_margi`（q1_business）｜Adjusted operating margin＝17.4 %｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 https://www.carrier.com/us/en/news/corporate/2026/carrierreports-third-quarter-2026-results/（同 SEC 8-K Ex.99）（numbers.latest_quarter_kpis.items[2]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-29））
- `f_kpi3_gaap_operating_profit_lo`（q1_business）｜GAAP operating profit (loss)＝-2273 USD m｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 https://www.carrier.com/us/en/news/corporate/2026/carrierreports-third-quarter-2026-results/（同 SEC 8-K Ex.99）（numbers.latest_quarter_kpis.items[3]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-29））
- `f_kpi7_backlog`（q1_business）｜Backlog＝8500 USD m（over）｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 https://www.carrier.com/us/en/news/corporate/2026/carrierreports-third-quarter-2026-results/（同 SEC 8-K Ex.99）（numbers.latest_quarter_kpis.items[7]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-29））
- `f_peer_carr_gross_margin_pct`（q2_moat）｜CARR 毛利率＝24.64 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CARR.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_earnings_recency`（q1_business）｜最近一次財報日＝2026-10-29 date｜期間與口徑：2026-10-29／距今 3 個交易日｜kind：realized
  - 來源：—（numbers.earnings_recency，as_of 2026-10-29）
- `f_peer_carr_operating_margin_pct`（q2_moat）｜CARR 營業利益率＝8.05 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CARR.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_carr_fcf_margin_pct`（q2_moat）｜CARR FCF 利潤率＝10.43 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CARR.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_tt_gross_margin_pct`（q2_moat）｜TT 毛利率＝34.99 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.TT.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_tt_operating_margin_pct`（q2_moat）｜TT 營業利益率＝17.92 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.TT.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_tt_fcf_margin_pct`（q2_moat）｜TT FCF 利潤率＝16.43 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.TT.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_jci_gross_margin_pct`（q2_moat）｜JCI 毛利率＝36.65 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.JCI.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_jci_operating_margin_pct`（q2_moat）｜JCI 營業利益率＝14.45 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.JCI.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_jci_fcf_margin_pct`（q2_moat）｜JCI FCF 利潤率＝6.64 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.JCI.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_lii_gross_margin_pct`（q2_moat）｜LII 毛利率＝33.1 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.LII.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_lii_operating_margin_pct`（q2_moat）｜LII 營業利益率＝19.94 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.LII.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_lii_fcf_margin_pct`（q2_moat）｜LII FCF 利潤率＝15.34 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.LII.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝2.87 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-10-31）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝3.25 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-10-31）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝3.73 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-10-31）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝23719.49 USD m｜期間與口徑：2026-11-03／yfinance revenue_estimate 0y 平均（25 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝25152.57 USD m｜期間與口徑：2026-11-03／yfinance revenue_estimate +1y 平均（25 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi6_fy2026_guidance`（q1_business）｜FY2026 guidance＝2.85–2.90 USD adj. EPS｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司新聞稿 https://www.carrier.com/us/en/news/corporate/2026/carrierreports-third-quarter-2026-results/（同 SEC 8-K Ex.99）（numbers.latest_quarter_kpis.items[6]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-29））
- `f_consensus_rev_fy2_pct`（q5_valuation）｜FY2 共識修正＝-1.52 %｜期間與口徑：2026-10-31／兩份 Koyfin 快照之間的 EPS 修正幅度（3.3 → 3.25）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.fy2.revision_pct，as_of 2026-10-31）
- `f_kpi4_free_cash_flow`（q1_business）｜Free cash flow＝674 USD m｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 https://www.carrier.com/us/en/news/corporate/2026/carrierreports-third-quarter-2026-results/（同 SEC 8-K Ex.99）（numbers.latest_quarter_kpis.items[4]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-29））
- `f_kpi5_stock_based_compensation`（q1_business）｜Stock-based compensation＝7 USD m｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 https://www.carrier.com/us/en/news/corporate/2026/carrierreports-third-quarter-2026-results/（同 SEC 8-K Ex.99）（numbers.latest_quarter_kpis.items[5]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-29））
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝10522.0 USD m｜期間與口徑：2026-11-03／yfinance 最新一季：總債務 11876.0、現金 1354.0（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝818.16 m shares｜期間與口徑：2026-11-03／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝1.756 %｜期間與口徑：2026-11-03／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-11-03）
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝54.68 USD｜期間與口徑：2026-11-02（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-11-02（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝19.05 x｜期間與口徑：2026-10-31／分母＝FY1 EPS 2.87，分子＝快照價 54.68｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-10-31）
- `f_consensus_rev_fy1_pct`（q5_valuation）｜FY1 共識修正＝-0.35 %｜期間與口徑：2026-10-31／兩份 Koyfin 快照之間的 EPS 修正幅度（2.88 → 2.87）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.fy1.revision_pct，as_of 2026-10-31）
- `f_consensus_rev_fy3_pct`（q5_valuation）｜FY3 共識修正＝-1.58 %｜期間與口徑：2026-10-31／兩份 Koyfin 快照之間的 EPS 修正幅度（3.79 → 3.73）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.fy3.revision_pct，as_of 2026-10-31）
- `f_ps_current`（q5_valuation）｜P/S（現值）＝1.96 x｜期間與口徑：2026-11-02（RTH 收盤，UTC）／4 個年度端點內的分位＝0.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝0.0 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝2.42 x｜期間與口徑：2026-11-02（RTH 收盤，UTC）／4 個年度端點內的分位＝5.9｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝5.9 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ev_m`（q5_valuation）｜目前企業價值 EV（市值＋淨負債）＝55259.0 USD m｜期間與口徑：2026-11-03／市值 44737.0 ＋ 淨負債 10522.0｜kind：realized
  - 來源：—（numbers.capital_structure.ev_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_ev_s_fwd`（q5_valuation）｜EV/S（EV ÷ FY1 共識營收）＝2.33 x｜期間與口徑：2026-11-03／f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）｜kind：estimate
  - 來源：—（numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝-16.36 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-11-02（RTH 收盤，UTC））
- `f_rsi14`（q5_valuation）｜RSI(14)＝44.59｜期間與口徑：2026-11-02（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ma_state`（q5_valuation）｜週線均線六態（decision_inputs.ma 必須等於此值）＝❌｜期間與口徑：2026-11-03／timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）
  - 原文：「price 54.43 / W52 59.75 / W104 62.71 / W250 54.64 / W250 13週斜率 0.2%」
- `f_ma_w52`（q5_valuation）｜52 週均線＝59.75 USD｜期間與口徑：2026-11-03／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）
- `f_ma_w104`（q5_valuation）｜104 週均線＝62.71 USD｜期間與口徑：2026-11-03／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）
- `f_ma_w250`（q5_valuation）｜250 週均線＝54.64 USD｜期間與口徑：2026-11-03／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）
- `f_ma_slope_w250_pct`（q5_valuation）｜W250 13 週斜率＝0.2 %｜期間與口徑：2026-11-03／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）

### findings_digest 中方向為負或來源衝突的條目（12 條）
- `competitive_share_entrants#1`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K 風險因子揭露：運輸冷凍業務有客戶的關係企業生產與公司競爭的貨櫃冷凍機組，另一客戶生產拖車冷凍機組；客戶或競爭者可能引入非傳統商業模式或破壞性技術。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A Risk Factors（as_of 2026-02-05）｜affects：moat_trend、decision_inputs.bear
- `supply_demand_durability#2`（supply_demand_durability｜方向 -｜狀態 ok）：Q4 2025 財報：住宅量大幅下滑，管理層預期需求偏弱直到房貸利率與消費者信心改善；假設 2026 美國產業銷量下滑 10–15%
  - 來源：MarketBeat, Carrier Global Q4 earnings call highlights（as_of 2026-02-06）｜affects：decision_inputs.bear、thesis.R
- `regulatory_antitrust#1`（regulatory_antitrust｜方向 -｜狀態 ok）：AFFF 訴訟：截至 2025-12-31，公司、KFI 等被列為被告的案件超過 17,000 件，已併入南卡羅來納 MDL。
  - 來源：SEC EDGAR 10-K FY2025 Item 3（as_of 2026-02-05）｜affects：thesis.R、decision_inputs.bear
- `regulatory_antitrust#2`（regulatory_antitrust｜方向 -｜狀態 ok）：2026 年 3 月起 Carrier 與其他 HVAC 製造商被列為 HVAC 聯合訂價推定集體訴訟（美國密西根東區聯邦地院）被告，公司稱無理由並於 2026-10-09 聲請駁回，簡報預計延至 2027。
  - 來源：SEC EDGAR 10-Q Q3 FY2026（as_of 2026-10-30）｜affects：thesis.R、decision_inputs.bear、valuation
- `reg_tariff_export#1`（reg_tariff_export｜方向 -｜狀態 ok）：10-K風險因子：公司在中國、墨西哥等地銷售、生產或採購，貿易限制（關稅）過去曾對業務造成負面影響，未來可能再影響；亦須遵守EAR出口管制，出口限制可能造成重大不利影響。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-05）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：FY2025 10-K 揭露：部分產品線僅有單一工廠可生產，天災等中斷可能使該產品停產
  - 來源：Carrier Global FY2025 Form 10-K（as_of 2026-02-01）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：FY2025 10-K 揭露：海外工廠與供應商眾多，新關稅、制裁或邊境限制可能影響營運
  - 來源：Carrier Global FY2025 Form 10-K（as_of 2026-02-01）｜affects：thesis.R
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：CARR 10-K 風險因素：競爭對手可能開發出先於或取代其產品被市場接受的競爭技術；客戶亦可能引入非傳統商業模式或顛覆性技術與產品；運輸冷凍客戶的關係企業已生產競爭的冷凍機組。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-05）｜affects：moat_trend、decision_inputs.bear
- `major_events#0`（major_events｜方向 -｜狀態 ok）：AFFF 訴訟：截至 2025-12-31，Carrier、KFI 等被列為超過 17,000 件訴訟被告，已合併於南卡羅來納 MDL；並簽有 Settlement and Plan Support Agreement。
  - 來源：SEC EDGAR 10-K FY2025 Item 3（as_of 2026-02-05）｜affects：decision_inputs.bear、valuation
- `major_events#3`（major_events｜方向 -｜狀態 ok）：2026-07-28 Q2 財報後股價跌 8.9%，多家原告律所（Pomerantz、Levi & Korsinsky）發佈調查公告；僅為律所徵求投資人，未見已提起之訴狀。
  - 來源：Pomerantz 新聞稿（placera.se 轉載）（as_of 2026-08-28）｜affects：decision_inputs.bear
- `lawsuit_class_action#0`（lawsuit_class_action｜方向 -｜狀態 ok）：AFFF MDL：超過 17,000 件訴訟，Carrier 與 KFI 為被告。
  - 來源：SEC EDGAR 10-K FY2025 Item 3（as_of 2026-02-05）｜affects：decision_inputs.bear、valuation
- `lawsuit_class_action#1`（lawsuit_class_action｜方向 -｜狀態 ok）：Pomerantz 等律所於 Q2 財報後股價跌 8.9% 後發佈投資人調查公告；未見已提起之證券集體訴訟。
  - 來源：Pomerantz 新聞稿（placera.se 轉載）（as_of 2026-08-28）｜affects：decision_inputs.bear

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 4 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CARR_20261103/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":134.2,"bear_5y_price":41.6,"p_bull_pct":20,"p_bear_pct":30,"upside_5y_pct":49.2,"ev5y_pct":46.5,"irr_base_pct":8.3,"asym_ratio":4.1,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":2.87,"pe":19.05,"basis":"FY2026 共識調整後 EPS 2.87（含約 4% 關稅退稅一次性），現價 54.68；終端倍數同為當年度調整後 EPS 口徑"},"eps":{"bull":[3.35,3.95,4.6,5.3,6.1],"base":[3.15,3.6,4.0,4.4,4.8],"bear":[2.75,2.85,2.95,3.05,3.2]},"pe":{"bull":22,"base":17,"bear":13},"p":{"bull":20,"base":50,"bear":30},"yield_pct":{"dividend":1.756,"net_buyback":0.0},"second_stage":{"bull_cagr_pct":10,"base_cagr_pct":7},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### CARR_Q2_2026_Earnings_Call_20260728.md
- 2026-07-28｜CEO｜guidance：CEO 開場宣布上調全年銷售、營業利潤與 EPS 財測。（原話："we are raising our full year guidance on sales"）
- 2026-07-28｜CFO｜guidance：CFO 給出新的全年調整後營業利潤指引約 35 億美元（前次 34 億）。（原話："We now expect adjusted operating profit of about $3.5"）
- 2026-07-28｜CFO｜guidance：CFO 給出全年調整後 EPS 約 2.90 美元（前次 2.80）。（原話："adjusted EPS of about $2.90, up from our prior guide of $3.4"）
- 2026-07-28｜CFO｜guidance：下半年營業利潤與 EPS 預期年增約 50%。（原話："will both be up about 50% year-over-year"）
- 2026-07-28｜CEO｜guidance：全年資料中心銷售展望由 15 億上調至約 20 億美元。（原話："full year data center sales outlook to about $2 billion"）
- 2026-07-28｜CFO｜guidance：Q3 有機成長指引約 10%（營收略低於 60 億，營業利潤率約 16.5%、EPS 約 0.75）。（原話："Organic growth is expected to be about 10%"）
- 2026-07-28｜CFO｜guidance：自由現金流指引不變，較高獲利被新美國廠增加的資本支出抵銷。（原話："No change in outlook with respect to free cash flow"）
- 2026-07-28｜CEO｜guidance：CSA 住宅銷售全年指引上調至高個位數成長。（原話："to be about high -- to be up high single digits"）
- 2026-07-28｜CEO｜guidance：管理層預期今年北美住宅市場約 700 萬至 750 萬台，與去年大致持平。（原話："market to be around 7 million to 7.5 million units"）
- 2026-07-28｜CEO｜guidance：歐洲商用空調下半年預期成長中個位數，依據為 Q2 訂單與在手訂單。（原話："give us confidence in the second half being up mid-single"）
- 2026-07-28｜CEO｜guidance：CEO 說明 CSA 輕型商用 Q3 與 Q4 的成長節奏。（原話："Q3 will be up mid-single digits."）
- 2026-07-28｜CFO｜guidance：CFO 說明 NORESCO 出售對全年營收的影響約 1.25 億美元。（原話："about $125 million year-over-year"）
- 2026-07-28｜CFO｜margin：CFO 稱 Q2 調整後營業利潤率 17.2%，略優於預期。（原話："Adjusted operating margin of 17.2% was a bit better"）
- 2026-07-28｜CFO｜margin：CFO 將 Q2 利潤率下滑部分歸因於關稅減緩措施的時間差。（原話："there is also the timing of the tariff mitigation and"）
- 2026-07-28｜CFO｜margin：CFO 稱 CSA 新建案占比高於預期，拉低整體利潤率。（原話："was a little bit higher mix than what we expected"）
- 2026-07-28｜CFO｜margin：Q3 營業利潤率指引 16.5%，CFO 列出生產力與量能槓桿為驅動。（原話："margin of 16.5% driven by strong productivity and"）
- 2026-07-28｜CFO｜margin：CFO 說明關稅相關的定價僅用於抵銷關稅，不帶來利潤率好處。（原話："we don't really get a margin benefit from that"）
- 2026-07-28｜CFO｜margin：CFO 給出 Q3 CSA（美洲）利潤率約 22%。（原話："For the Americas will be at around 22%."）
- 2026-07-28｜CFO｜margin：CFO 說明 CSA 全年利潤率約持平，商用部分低於整體。（原話："this year we expect the margins to be about flat"）
- 2026-07-28｜CFO｜margin：CFO 給出 CSA 商用利潤率區間。（原話："So they would be in the mid- to high teens."）
- 2026-07-28｜CFO｜margin：CFO 稱資料中心利潤率對整體商用空調利潤率具增益。（原話："margins with data centers are accretive to the overall"）
- 2026-07-28｜CFO｜margin：CFO 說明 2027 年起增量轉換率的區間假設（兩者同速成長下）。（原話："expect us to remain in the 25% to 30% conversion"）
- 2026-07-28｜CFO｜margin：CFO 說明今年投資額約 1 億美元，是財測上調未全額轉換為獲利的原因之一。（原話："will be roughly in the $100 million range."）
- 2026-07-28｜CFO｜margin：CFO 稱關稅減緩的時間差預期明年仍為逆風。（原話："we'd expect that to be a headwind next year"）
- 2026-07-28｜CEO｜margin：CEO 說明 CSE 區段 Q2 利潤率表現。（原話："Segment margins in 2Q were disappointing."）
- 2026-07-28｜CEO｜commitment：CEO 承諾歐洲區段在未來數年內達到中雙位數（mid-teen）營業利潤率。（原話："mid-teen operating margins over the next few years."）
- 2026-07-28｜CEO｜commitment：CEO 在問答中再次表示有信心達成歐洲 mid-teen 利潤率，並指出將更嚴守定價並削減成本。（原話："I'm confident we'll get there"）
- 2026-07-28｜CEO｜commitment：CEO 承認歐洲成本管控過去不夠積極，並表示現在會積極進行。（原話："we should have been more aggressive on cost"）
- 2026-07-28｜CEO｜commitment：CEO 表示維持售後市場全年雙位數成長的目標。（原話："We remain on track for double-digit aftermarket growth."）
- 2026-07-28｜CEO｜commitment：CEO 設定新美國廠投產目標時程為 Q1 底，預計一兩個月內決定廠址。（原話："facility up and running by the end of the first quarter"）
- 2026-07-28｜CEO｜commitment：CEO 說明歐洲新品 Vitocal 200 的上市時程。（原話："We are on track to formally launch in the fall"）
- 2026-07-28｜CEO｜commitment：CEO 對資料中心客戶交付的承諾說法。（原話："Our commitment to our customers is to be perfect quality"）
- 2026-07-28｜CFO｜capital_allocation：CFO 說明全年資本支出因新美國廠上調至約 6 億美元。（原話："We now expect full year CapEx to be about $600 million."）
- 2026-07-28｜CFO｜capital_allocation：CFO 稱全年股票回購維持 15 億美元。（原話："expected to remain at $1.5 billion for the year."）
- 2026-07-28｜CEO｜capital_allocation：CEO 稱 Q2 回饋股東約 6.4 億美元。（原話："returned about $640 million to shareholders"）
- 2026-07-28｜CEO｜capital_allocation：CEO 稱 Riello 出售已完成，NORESCO 出售於前一日宣布。（原話："the divestiture of Riello complete"）
- 2026-07-28｜CEO｜capital_allocation：CEO 說明收購 75F 後 BMS 可觸及市場擴大約 200 億美元。（原話："75F expands our TAM by about $20 billion"）
- 2026-07-28｜CEO｜capital_allocation：CEO 談及擴產風險控管：擔心資料中心資本支出放緩時過度擴張。（原話："we're very careful not to get out over our"）
- 2026-07-28｜CEO｜capital_allocation：CEO 表示液冷領域目前選擇專注自行成長，而非收購。（原話："the decision for now to focus on organic growth"）
- 2026-07-28｜CEO｜customer：CEO 稱 Q2 總訂單年增約 40%。（原話："2Q orders were very strong, up about 40%"）
- 2026-07-28｜CEO｜customer：CEO 稱資料中心訂單為去年同期的 4 倍。（原話："data centers where orders were up 4x over last year"）
- 2026-07-28｜CEO｜customer：CEO 稱總在手訂單超過 80 億美元（不含超大規模與託管業者長約預期訂單）。（原話："is now over $8 billion, up about 40% versus last year"）
- 2026-07-28｜CFO｜customer：CFO 拆解在手訂單中資料中心占比。（原話："and 40% of that is data centers."）
- 2026-07-28｜CFO｜customer：CFO 拆解全年 20 億資料中心營收：上半年約 5 億。（原話："in the first half, we saw about $500 million"）
- 2026-07-28｜CFO｜customer：CFO 說明 CSA 商用 Q2 下滑為資料中心交付時程所致，預期 Q3 大幅回升。（原話："significant sequential and year-over-year pickup in Q3"）
- 2026-07-28｜CEO｜customer：CEO 回應客戶延後交付疑慮：下半年已訂滿。（原話："we're fully booked for the second half"）
- 2026-07-28｜CEO｜customer：CEO 稱客戶要求加速交付，而非延後。（原話："they are pushing us to accelerate deliveries"）
- 2026-07-28｜CEO｜customer：CEO 回應重複下單疑慮。（原話："we're not concerned about double demand"）
- 2026-07-28｜CEO｜customer：CEO 說明輕型商用上調的來源之一為贏得全國性策略客戶。（原話："we've won some really big strategic national accounts"）
- 2026-07-28｜CEO｜competition：CEO 稱公司在資料中心領域持續取得市占。（原話："we've been gaining a lot of share in the data center space"）
- 2026-07-28｜CEO｜competition：CEO 說明公司美國商用空調起始市占低於同業。（原話："we started with very low share for commercial"）
- 2026-07-28｜CEO｜competition：CEO 預期北美住宅今年市占小幅增加。（原話："that we gain a tiny bit of share, but we want"）
- 2026-07-28｜CEO｜competition：CEO 說明與超大規模業者簽訂的長約（LTA）。（原話："give us tremendous contractual confidence in the kind of"）
- 2026-07-28｜CEO｜product：CEO 說明 CDU 液冷產品規劃：1.3MW 已有需求，2.5～2.6MW 本季推出。（原話："We have a 1.3 megawatt CDU that we've seen good demand for"）
- 2026-07-28｜CEO｜product：CEO 說明歐洲 Q2 熱泵銷售與鍋爐的表現。（原話："heat pumps up about 20% and boilers down high single digits"）
- 2026-07-28｜CEO｜product：CEO 說明北美住宅 Q2 價格實現約 3%，下半年改善 1～2 個百分點，全年約 4%。（原話："in 2Q, we were around 3%"）
- 2026-07-28｜CEO｜product：CEO 說明北美住宅下半年約 20% 成長中，10 個百分點來自去年去庫存不再重現。（原話："the absence of destocking in the second half"）
- 2026-07-28｜CEO｜risk：CEO 稱全球卡車、拖車冷鏈業務的復甦時點仍不明朗。（原話："the recovery in Global Truck, Trailer remains unclear"）
- 2026-07-28｜CEO｜risk：CEO 談中國住宅業務長期疲弱。（原話："in China, it's been soft for a while"）
- 2026-07-28｜CEO｜risk：CEO 表示團隊需思考中國住宅業務要投入多少才能根本改善。（原話："investment required to fundamentally improve the business"）

### 問答異常語氣（迴避／改口／保留）
- CARR_Q2_2026_Earnings_Call_20260728.md｜問：Scott Davis 問 Q2 利潤率下滑中，mix 與價格／成本各占多少、其中多少是時間差。｜答法：CFO 列出 mix、關稅減緩時間差與合資收益等因素，但未量化各項占比或時間差大小。
- CARR_Q2_2026_Earnings_Call_20260728.md｜問：Joe Ritchie 問新產能的潛在營收run-rate 能到多少、規劃延伸到多遠。｜答法：CEO 回以現有產能可支撐 25 億、並談市占與避免過度擴張，未給出新廠的營收規模數字。
- CARR_Q2_2026_Earnings_Call_20260728.md｜問：Andrew Obin 問全年 20 億、下半年 15 億與年底出貨率 25 億之間的算術落差。｜答法：CFO 稱 25 億是興建新廠前的數字，Q4 年化將遠高於 25 億，但未給出 Q4 或新的出貨率具體數字。
- CARR_Q2_2026_Earnings_Call_20260728.md｜問：Chris Snyder 問住宅 20% 下半年成長對照 2 年疊加並未改善，憑什麼確信需求轉好。｜答法：CEO 改談剔除去庫存後的 mid-single-digit 終端動能、經銷商來電量與房市積壓需求，未直接回應 2 年疊加數字。

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 3 | 2 |
| customer_second_source | none | 0 | 3 |
| customer_concentration_credit | found | 1 | 2 |
| supply_demand_durability | found | 4 | 4 |
| regulatory_antitrust | found | 3 | 2 |
| reg_tariff_export | found | 3 | 2 |
| geo_supply_chain | found | 5 | 4 |
| end_markets | found | 4 | 3 |
| substitute_technology | found | 2 | 2 |
| channel_business_model_shift | found | 5 | 2 |
| capital_markets_pricing | found | 4 | 4 |
| major_events | found | 4 | 5 |

未涵蓋／不適用軸的查詢詞原文（供判相關性）：
- **customer_second_source**（none）：Carrier Global largest customer concentration distributor 10-K no single customer 10% of sales；Carrier Global customer concentration largest customer distributor insourcing second source 2026；Carrier Global 10-K 2025 "no single customer" percent of sales dealers distributors

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260729","verdict":"進場","role":"衛星","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"資料中心散熱是可持續的第二成長曲線，而非一輪資本支出脈衝——Carrier 由約 10% 份額往 15–20% 走，且新增產能不會在需求放緩時變成閒置資產"},{"id":"H2","text":"美國住宅暖通空調的更換週期已經觸底回升——通路去庫存結束，市場自 700–750 萬台往正常化的 900 萬台走"},{"id":"H3","text":"調整後營益率的下滑是時間差與 mix，不是結構性侵蝕——關稅定價時間差消化、歐洲成本結構修好、商用規模吸收後，營益率回到並超越 2025 年水準"}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"下半年 15 億美元資料中心出貨的執行風險——全年 EPS 上修完全建立在 2H 調整後營益與 EPS 各 +約 50% YoY 之上，而 Q3 指引 EPS $0.75 已低於財報前共識 $0.857；執行長自承「這純粹是執行問題」，並已把資源投入供應鏈、供應商品質與自家工廠品質"},{"id":"R2","text":"歐洲分部的結構性成本問題 ＋ 關稅時間差在 2027 續為逆風——CSE 分部 Q2 營益率「令人失望」，執行長承認「我們應該在成本上更積極」；新任總裁的修復目標是「未來幾年」走到中十位數，即這是多年工程不是一季修正。同時財務長明示關稅定價時間差明年還會是逆風"},{"id":"R3","text":"Viessmann 併購的資本回報無法證明 ＋ HVAC 價格聯合訴訟——155 億美元商譽（超過股東權益）對應的 ROIC 僅約 10.2%、僅高於 WACC 1.3pp；另有一件在密西根聯邦法院提起的集體訴訟，指控 Carrier、Trane、Daikin、Bosch、Lennox、Rheem、AAON 七家業者以六年時間串謀抬價"}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"starter 1/3；加碼＝Q3 資料中心出貨兌現（營收 ≥$5.9B 且 OM ≥16.5%）或回落 $55 以下","irr_base_pct":9.4,"ev5y_pct":53.0,"drift_watch_prior":{"dca_verdict":"進場","dca_role":"衛星","signal":"B","val":"🟡","ma":"🟠","trap":"🟡","moat_trend":"→","runway_post_y5":"🟢","asym_ratio":3.7,"ev5y_pct":53.0,"irr_base_pct":9.4,"max_dd_pct":-50.0,"bull_5y_price":154.0,"bear_5y_price":38.0,"p_bull_pct":24.0,"p_bear_pct":30.0,"rearm_trigger":"starter 1/3；加碼＝Q3 資料中心出貨兌現（營收 ≥$5.9B 且 OM ≥16.5%）或回落 $55 以下","price_at_dd":63.16,"archetype":"品質複利成長","cycle_position":"早循環"}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"CARR","date":"2026-11-03","schema":"v15.0","contract":"v19","company_name":"Carrier Global Corporation"},"oneliner":"資料中心訂單與住宅量能雙雙超預期，但第三季利潤率靠關稅退稅過關、住宅漲價跟不上成本；首倉不動，等 2027 年 2 月漲價落地的讀數再決定加碼。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CARR_20261103/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CARR_20261103/scenario.json","answers":{"q1_business":{"verdict":"賺住宅替換、商用專案與售後服務的錢；住宅的錢卡在安裝商通路與安裝基數，資料中心的錢卡在交付產能與長約。","reasoning":"第三季營收 62.63 億美元、有機成長 15%：美洲氣候方案 33.54 億（約 54%，年增 24%）、歐洲 13.35 億（約 21%）、亞洲中東非洲 8.48 億（約 14%）、運輸冷凍 7.26 億（約 12%，年減 3%），四塊都超過一成。調整後營業利益 10.91 億、營益率 17.4%，其中約 1.3 億是關稅退稅，扣除後約 15.3%（(10.91−1.33)÷62.63）；GAAP 營業虧損 22.73 億來自歐洲商譽減損 31 億。TTM 毛利率 24.6%。收錢方式：住宅經由經銷商與 10 萬家以上安裝商賣替換機，商用直接賣給承包商與業主，售後靠安裝基數收服務與零件，資料中心與超大規模客戶簽含最低量的長約。單點依賴：2023–2025 年無單一客戶超過營收一成，但無風管機型仰賴與 Midea 的合作（細節未揭露），部分產品線只有單一工廠，資料中心成長集中在少數超大規模客戶（一家 10 月簽下逾 30 億美元）。產業態勢屬雙向拉鋸：競爭面住宅定價承壓（價格實現低個位數、分析師追問亞洲進口），結構面商用與資料中心轉好且有長約撐，其他結構變數是關稅與聯合訂價訴訟。","fact_refs":["f_kpi0_net_sales_gaap","f_kpi1_adjusted_operating_profi","f_kpi2_adjusted_operating_margi","f_kpi3_gaap_operating_profit_lo","f_kpi7_backlog","f_peer_carr_gross_margin_pct","f_earnings_recency"],"verdict_values":{"revenue_quality":"中等偏好：商用與售後到 2027 年底接近組合一半（管理層），在手訂單逾 85 億美元且不含長約最低量；住宅屬短循環。第三季調整後營益率含約 1.3 億美元關稅退稅，品質要扣掉看。","unit_econ_note":"第三季有機成長 15%、調整後營業利益增約 35%、邊際轉換率逾 30%（財務長）；但扣退稅後 CSA 利潤率低於公司預期，住宅價格實現低個位數（原預期中個位數），全年投入成本逆風約 8 億美元、略低於一半是關稅。","archetype":{"primary":"品質複利成長","secondary":"循環/商品","confidence":"低","fingerprint":"住宅短循環＋商用長循環＋售後安裝基數，利潤率落後同業一大截"},"industry":{"clock_phase":"I","sd_verdict_source":"商用與資料中心需求屬結構性（在手訂單逾 85 億美元且不含長約最低量，2026-10-29 法說），但產業供給可逆性高（Linesight 2026-06 稱新增產能 2026 下半年至 2027 年緩解）；住宅屬週期性回升，台數 750–800 萬仍低於正常化。判在第一階段：短循環剛走出去庫存，營收組合仍以短循環為主（商用＋售後到 2027 年底才接近一半）。","bargaining":{"up":"銅鋼鋁、運費與關稅今年全年約 8 億美元投入成本逆風、轉嫁不完全；無風管機型技術與供貨依賴 Midea 合作","down":"住宅通路分散（10 萬家以上安裝商），但品牌選擇權在安裝商；資料中心面對少數超大規模客戶，以最低量承諾換供應保證，執行長稱合約有通膨保護（條款未揭露）","geo":"在中國、墨西哥生產與採購，受關稅與出口管制影響；擴產落在美國 Fort Worth 與印度 Sri City"},"profit_pool_dir":"利潤池往商用、資料中心與售後移動；資料中心對商用冰水機利潤率有增益（管理層），住宅利潤池今年被價格成本壓縮","tam_table":[{"item":"北美住宅市場台數","value":"2026 年約 750–800 萬台（2026-10-29 法說執行長）；2026-07-28 法說預估 700–750 萬台"},{"item":"資料中心營收與訂單","value":"2026 年目標約 20 億美元；年初至今訂單逾 30 億美元、年增近 350%；第三季出貨逾 5.5 億美元"},{"item":"資料中心產能","value":"現有產能可支撐約 25 億美元年化營收（2026-07-28 法說）；Fort Worth 新廠 2027 年夏末交貨後美洲產能逾倍增"},{"item":"無風管與側出風機型","value":"約占北美住宅市場兩成（2026-10-29 法說執行長答問）"},{"item":"TAM、滲透率、段 CAGR、營業利益池占比五年變化","value":"事實表未涵蓋"}]}}},"q2_moat":{"verdict":"護城河方向持平：商用與資料中心的執行與份額在擴大，住宅定價力今年在縮減，兩者抵銷；等級 C，利潤率落後同業一大截。","reasoning":"機制：安裝基數加 10 萬家以上經銷安裝通路與品牌，帶來替換需求與售後服務（售後第三季年增 9%）；資料中心靠交付速度（18 個月的開發壓到 6 個月）、首台驗證表現（重啟時間、高溫滿載效率）與現場調試贏單。執行力 7 分：商用份額由低基期擴大、在手訂單較分拆時 4 倍；扣分在新冰水機供應鏈初期問題、新廠延後、歐洲減損。定價力 5 分：第三季各分部價格皆為正、商用定價財務長稱為正，但住宅價格實現低個位數、全年約 8 億美元投入成本轉嫁不完全。同業對照（TTM）：毛利率 Carrier 24.6%，TT 35.0%、JCI 36.7%、LII 33.1%；營益率 8.1% 對 17.9%、14.5%、19.9%；FCF 率 10.4% 對 16.4%、6.6%、15.3%。毛利率差距 8–12pp 未收斂，這是定價力 5 分的主要依據。可能看錯之處：Carrier 的 TTM 營益率口徑可能受歐洲減損影響而與同業不同，所以以毛利率差距為主；同業 ROIC 事實表未涵蓋，無法用報酬差確認方向。","fact_refs":["f_peer_carr_gross_margin_pct","f_peer_carr_operating_margin_pct","f_peer_carr_fcf_margin_pct","f_peer_tt_gross_margin_pct","f_peer_tt_operating_margin_pct","f_peer_tt_fcf_margin_pct","f_peer_jci_gross_margin_pct","f_peer_jci_operating_margin_pct","f_peer_jci_fcf_margin_pct","f_peer_lii_gross_margin_pct","f_peer_lii_operating_margin_pct","f_peer_lii_fcf_margin_pct","f_kpi7_backlog"],"verdict_values":{"moat":{"mechanism":"安裝基數＋10 萬家以上經銷安裝通路＋品牌，帶來替換與售後；資料中心靠交付速度、首台驗證表現與系統整合（冰水機＋CDU＋樓宇管理）","execution":7,"pricing":5,"grade":"C","trend":"→","trend_evidence":"執行力擴大：一家超大規模客戶簽逾 30 億美元含最低量長約、兩家客戶近一月加碼，商用銷售較分拆時 2 倍、在手訂單 4 倍。定價力縮減：CSA 住宅價格實現低個位數（原預期中個位數），全年約 8 億美元投入成本未能全數轉嫁，毛利率比 TT、JCI、LII 低 8–12pp 且未收斂。一升一降判持平；2027 上半年漲價若黏不住改判下降。","competitor_notes":[{"name":"TT","strategy_note":"商用暖通與資料中心冰水機的正面對手，TTM 營益率 17.9%、FCF 率 16.4%，是 Carrier 商用定價與組合能走多遠的標尺"},{"name":"JCI","strategy_note":"毛利率 36.7% 最高但 FCF 率只有 6.6%，樓宇控制與冰水機和 Carrier 重疊；Carrier 的現金轉換反而較好"},{"name":"LII","strategy_note":"同一北美住宅市場、同一關稅環境下營益率 19.9%，是判斷住宅定價問題屬 Carrier 自身還是全產業的對照組；LII 的 2026 價格實現事實表未涵蓋"},{"name":"6367.T","strategy_note":"日本空調同業，事實表營收缺失、只有兩季，無法比較利潤率"}],"peer_na_reason":"同業 ROIC 與 Forward P/E 事實表未涵蓋，以毛利率、營益率與 FCF 率差距作為可比軸；6367.T 營收缺失無法比較","threats":[{"level":"🟡","text":"運輸冷凍客戶的關係企業自產貨櫃冷凍機組、另一客戶自產拖車冷凍機組，屬點對點競爭，限於運輸分部（第三季營收 7.26 億美元、約 12%）","p":"20%","evidence_refs":["competitive_share_entrants#1"]},{"level":"🟡","text":"北美住宅進口與無風管機型占比上升（無風管約占市場兩成），分析師兩度追問亞洲進口對定價的影響；Carrier 自己透過 Midea 合作與 Toshiba 技術賣無風管，屬點對點但打到定價力","p":"30%","evidence_refs":[]},{"level":"🟡","text":"10-K 泛用揭露：競爭技術可能先於公司產品被接受；目前可見的替代是液冷（公司自研 CDU 因應，5MW 機型年底推出）與歐洲熱泵取代鍋爐（公司兩邊都賣）","p":"15%","evidence_refs":["substitute_technology#0"]},{"level":"🟡","text":"商用暖通產能湧入、低階對手擴產帶來的價格競爭（2026-10-29 法說分析師提問），中國與亞洲部分地區已見價格壓力","p":"25%","evidence_refs":[]}],"roic_durability":{"quadrant":"低利益率×低周轉","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"空調與暖氣是需要不是想要：住宅以替換為主、延後的代價是夏天沒冷氣；資料中心散熱是算力的必要條件，使用者、決策者、付款者都成立。代理讀數：北美住宅市場 750–800 萬台、資料中心年初至今訂單逾 30 億美元（2026-10-29 法說）。"},{"item":"決策層級","level":"🟡","text":"住宅品牌選擇發生在安裝商這一層，安裝商可在多個品牌與進口無風管機型之間換，替代性高；資料中心客戶在規格、交期與現場調試上選供應商，首台驗證與長約形成轉換成本，但客戶刻意多供應商。代理讀數：住宅量增逾 30% 但價格實現只有低個位數，漲價受安裝商抵抗。"},{"item":"價值鏈分配","level":"🟡","text":"上游銅鋼鋁與關稅今年約 8 億美元逆風、轉嫁不完全；無風管技術依賴 Midea；下游超大規模客戶集中且議價力強，以最低量承諾換供應保證。毛利率比同業低 8–12pp，Carrier 在價值鏈拿到的份額低於對手。"},{"item":"社會容忍度","level":"🟡","text":"空調是高必要品，住宅一年內再漲 8–10% 正遇上消費者負擔力問題；Carrier 同時被列為 HVAC 聯合訂價推定集體訴訟被告（2026-10-09 已聲請駁回），社會與法律對產業集體漲價的容忍度正被測試。優勢不依賴監管授權。"}],"roiic":"約 15%（判斷估計）","reinvest_rate":"約 25%（判斷估計）","endo_ceiling":3.8,"formula_note":"內生成長＝增量報酬約 15% × 再投資率約 25% ≈ 3.8%。增量報酬：資料中心擴產報酬高，但近年最大一筆再投資 Viessmann 已減損 31 億美元，兩者平均取 15%；再投資率：資本支出約 6 億美元（2026-07-28 法說財務長）加營運資金，扣折舊後淨額相對調整後營業利益約 35 億（稅後以約兩成稅率粗估約 27 億），出售 Riello、NORESCO 為負收購。當期 ROIC、投入資本、折舊與營運資金變動事實表未涵蓋，兩個輸入都是估計；象限依 GAAP 營益率 8.1% 與含大額商譽的投入資本判定。"}}}},"q3_growth":{"verdict":"五年後跑道仍寬：資料中心與歐洲熱泵取代鍋爐是兩條有據可查的曲線；但三年共識 EPS 年複合約 12.6%，遠高於內生天花板約 3.8%，缺口靠利潤率擴張與回購補，可歸因。","reasoning":"成長組成：量為主（第三季總訂單年增 35%、商用逾 60%、資料中心 300%；住宅去庫存結束後銷售增逾 30%），價為輔（2026 年價格約 2%、約四分之三與關稅相關，彙整來源；2027 宣布最高 10%），回購每年約 3%，併購為負（出售 Riello、NORESCO 拖累營收約 3 個百分點）。共識：FY2026 2.87、FY2027 3.25、FY2028 3.73 美元，家數事實表未涵蓋；營收共識 FY2026 237.2 億、FY2027 251.5 億（年增約 6%，25 位分析師）。內生天花板約 3.8%（見護城河段），缺口約 8.8pp：營益率擴張（住宅量回升、資料中心增益、漲價）約 5–6pp，淨回購約 3pp，可歸因、不依賴重新評價；但利潤率擴張正是本次最弱的假設，缺口裡最大一塊也最不確定。跑道：滲透率事實表未涵蓋，以兩條曲線判寬——資料中心（年初至今訂單逾 30 億、一家超大規模客戶逾 30 億長約）與歐洲熱泵取代鍋爐（第三季熱泵年增約 35%、鍋爐年減高個位數，管理層稱為根本轉移）。風險在 2030 年後資料中心資本支出的持續性。衰退訊號亮 2 個，價值陷阱風險與長期成長性都是黃。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_kpi7_backlog","f_kpi6_fy2026_guidance","f_consensus_rev_fy2_pct"],"verdict_values":{"growth":{"driver_mix":"量為主（商用與資料中心訂單、住宅去庫存結束），價為輔（2026 約 2%、2027 宣布最高 10%），回購約每年 3%，併購為負","runway_years":"滲透率事實表未涵蓋，無法換算年數","runway_post_y5":"🟢","endo_ceiling_basis":"增量報酬約 15% × 再投資率約 25% ≈ 3.8%（兩者為判斷估計）；共識三年 EPS 年複合約 12.6%，缺口約 8.8pp 歸因營益率擴張約 5–6pp 與淨回購約 3pp","segments":[{"item":"美洲氣候方案（CSA）","value":"第三季營收 33.54 億美元、年增 24%（有機 25%），分部營益率 22.2%（含退稅）；全年營益率指引下修至約 19%"},{"item":"歐洲氣候方案（CSE）","value":"13.35 億美元、年增 3%（有機 12%），營益率雙位數；同季提列商譽減損 31 億美元"},{"item":"亞洲中東非洲","value":"8.48 億美元、年增 2%（有機 3%），中國住宅疲弱、售後年增十幾%"},{"item":"運輸冷凍","value":"7.26 億美元、年減 3%，高利潤的卡車拖車業務中個位數下滑"}],"decay_signals":[{"signal":"毛利率連 2 季年減","lit":true,"note":"季度值事實表未涵蓋，以年度代理：2023 年 27.2%、2024 年 26.6%、2025 年 25.9%、TTM 24.6%"},{"signal":"核心市占近 12 個月縮減","lit":false,"note":"執行長稱住宅小幅增加份額、資料中心持續取得份額；第三方份額數據事實表未涵蓋"},{"signal":"主力產品提價後銷量下滑","lit":false,"note":"CSA 住宅第三季銷售增逾 30%"},{"signal":"EPS 成長顯著高於營收成長","lit":true,"note":"FY2027 共識 EPS 年增約 13.2%，營收共識年增約 6.0%，差約 7pp"},{"signal":"FCF／淨利連 2 年低於 0.75","lit":false,"note":"2025 年約 1.43；2024 年約 0.01 但淨利含出售利益，未連兩年"},{"signal":"SBC／營收高於 5% 且上升","lit":false,"note":"第三季約 0.1%"},{"signal":"TAM 萎縮或被替代技術壓縮","lit":false,"note":"歐洲鍋爐下滑由熱泵替代，公司兩邊都賣"},{"signal":"產業估值倍數近 3 年系統性下移","lit":false,"note":"同業倍數歷史事實表未涵蓋"},{"signal":"維護性資本支出占 FCF 逾 60%","lit":false,"note":"全年資本支出約 6 億、FCF 約 20 億，總資本支出約三成"},{"signal":"停止投資新產能且收入下滑","lit":false,"note":"正擴產（Fort Worth、印度 Sri City）"}],"trap_rating":"🟡（亮 2 個：年度毛利率連降、EPS 成長高於營收成長逾 5pp）"}}},"q4_capital":{"verdict":"現金轉換健康、稀釋近乎零，但最大一筆併購 Viessmann 已用 31 億美元減損承認回報失敗。","reasoning":"自由現金流：2025 年 21.21 億美元、FCF／淨利約 1.43；2026 年指引約 20 億不變（第三季 6.74 億、年初至今約 15 億）。2024 年 FCF 僅 0.44 億、淨利 56 億含出售利益，轉換率失真。SBC 約營收 0.1%。現金去向：回購每年 15 億美元（約市值 3.4%）、股息殖利率 1.76%、資本支出約 6 億（含新廠），出售 Riello 與 NORESCO 為淨流入；四分比例事實表未涵蓋。淨負債 105 億美元，約為 2026 調整後營業利益 35 億的 3 倍（EBITDA 事實表未涵蓋）。資本配置的問題不在回購或稀釋，在併購。","fact_refs":["f_kpi4_free_cash_flow","f_kpi5_stock_based_compensation","f_kpi3_gaap_operating_profit_lo","f_net_debt_m","f_shares_diluted_m","f_dividend_yield_ttm"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":true,"passed":false,"input":"Viessmann（歐洲氣候方案）於 2026 年第三季提列 31 億美元非現金商譽減損，執行長稱時點不幸；歐洲營益率仍在追中十位數承諾，已實現回報低於資金成本"},{"name":"buyback_yield","applicable":true,"passed":null,"input":"2026 年回購維持 15 億美元；回購均價與 10 年期公債殖利率事實表未涵蓋，無法驗證；以現價計 FY1 盈餘殖利率約 5.2%（2.87÷54.68），近半年股價多高於現價（26 週報酬 −16%），實際買入收益率更低"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"第三季股份基礎薪酬 700 萬美元、約營收 0.1%；財務長稱 EPS 成長部分來自股數下降，淨稀釋為負"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購撐：2026 年為淨出售（Riello、NORESCO），回購每年 15 億美元維持；併購回報失敗已記在併購增量報酬項"}}}},"q5_valuation":{"verdict":"現價要求 2027 年起 EPS 恢復雙位數成長、倍數不再下修；資料中心那一半我信，住宅定價那一半要等 2027 上半年讀數，估值合理偏低但不夠便宜到可以不看證據。","reasoning":"現價 54.68 美元、FY1 本益比 19.05 倍（FY1 共識 2.87 含約 4% 的退稅一次性）、FY2 本益比 16.8 倍（3.25）、FY3 14.7 倍（3.73）。三年共識 EPS 年複合約 12.6%，PEG 約 1.5。P/S 1.96 倍、EV/S 2.42 倍，在 4 個年度端點中分別處於 0 與 5.9 分位（非五年分位）。共識近期小幅下修（FY1 −0.35%、FY2 −1.52%、FY3 −1.58%），股價 26 週跌 16%，下跌主要是倍數下修。賣方平均目標價 66.7–70.8 美元多為 8 月以前資料，高 90、低 58，不作錨。終端倍數 Base 17 倍、Bear 13 倍、Bull 22 倍，以本身現值 19 倍為錨；同業 Forward P/E 事實表未涵蓋，無法附同業現值對照。Base 五年 81.6 美元（4.80×17），Bear 41.6 美元（約 −24%），下行有限，但短期上行也有限。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_fy1_pct","f_consensus_rev_fy2_pct","f_consensus_rev_fy3_pct","f_ps_current","f_ps_percentile","f_ev_s_current","f_ev_s_percentile","f_ev_m","f_ev_s_fwd","f_dividend_yield_ttm","f_week26_return_pct"],"verdict_values":{"valuation":{"basis":"Forward P/E 與 PEG（品質複利型的優先尺），以 FY2 本益比交叉檢查","peers":{"expanded":false,"reason":"同業 Forward P/E 事實表未涵蓋（同業對照只有利潤率），不以利潤率高一截的 TT、LII 當倍數錨"},"fwd_pe":19.05,"peg":1.5,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"FY1 本益比 19.05 倍、FY2 16.8 倍；三年 EPS 年複合約 12.6%（3.73÷2.61 開三次方），PEG 約 1.5，落在 1–2 的合理區；FY2 本益比對 FY2 到 FY3 成長 14.8% 約 1.1。年度端點 P/S、EV/S 分位 0 與 5.9（只有 4 個點，五年分位事實表未涵蓋）。分母含約 4% 退稅一次性、2027 要在結轉通膨下成長，所以停在黃不升綠。短期上行 3.7%＝2027 Base EPS 3.15 × 18 倍約 56.7 美元；中期上行 49.2%＝2031 Base EPS 4.80 × 17 倍約 81.6 美元。","upside_short_pct":3.7,"upside_mid_pct":49.2,"denominator_disputed":false,"denominator_note":"FY1 共識 2.87 含第三季認列約 1.33 億美元 IEEPA 關稅退稅（10-Q），稅後約每股 0.12 美元、占 EPS 約 4%；不是爭點核心，改以 FY2 本益比 16.8 倍交叉檢查"}}},"q6_how_wrong":{"verdict":"最可能看錯在住宅定價：若 2027 漲價黏不住，利潤率與倍數一起往下；回撤範圍 −35%～−50%。","reasoning":"最大回撤範圍：上緣以 Bear 谷底 EPS 2.75 × 13 倍約 35.8 美元（約 −35%），下緣以衰退加價格戰 EPS 回到約 2.6 × 11 倍約 28.6 美元（約 −48%），取 −50%。技術面沒有緩衝：週線收盤 54.43 低於 52 週均線 59.75、104 週均線 62.71，貼著 250 週均線 54.64，250 週均線 13 週斜率僅 0.2%，26 週報酬 −16.4%，RSI 44.6 未超賣也未過熱。成長熄火壓力測試（三年後成長降到 15%、10%、5%，倍數對應 19、16、12 倍，套 FY2029 Base 4.00）：約 76、64、48 美元，三種情境兩種不虧。2026-07-28 法說迴避紀錄四條：未量化組合與價格成本各占多少、未給新產能營收規模、未給第四季資料中心年化出貨數字、未回應住宅兩年疊加；前兩條在第三季以利潤率低於預期與新廠延後部分應驗。三種看錯方式見反證紀錄。","fact_refs":["f_week26_return_pct","f_rsi14","f_ma_state","f_ma_w52","f_ma_w104","f_ma_w250","f_ma_slope_w250_pct","f_consensus_eps_fy1"],"verdict_values":{"trap":{"verdict":"🟡","label":"利潤率陷阱風險：成長是真的，價格成本未證"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":2.87,"pe":19.05,"basis":"FY2026 共識調整後 EPS 2.87（含約 4% 關稅退稅一次性），現價 54.68；終端倍數同為當年度調整後 EPS 口徑"},"eps":{"bull":[3.35,3.95,4.6,5.3,6.1],"base":[3.15,3.6,4.0,4.4,4.8],"bear":[2.75,2.85,2.95,3.05,3.2]},"pe":{"bull":22,"base":17,"bear":13},"p":{"bull":20,"base":50,"bear":30},"yield_pct":{"dividend":1.76,"net_buyback":0.0},"second_stage":{"bull_cagr_pct":10,"base_cagr_pct":7},"max_dd":{"lo":-50,"hi":-35,"basis":"上緣：Bear 谷底 EPS 2.75 × Bear 終端 13 倍約 35.8 美元，約 −35%；下緣：衰退加價格戰，EPS 回到 FY2026 共識九成約 2.6 × 11 倍約 28.6 美元，約 −48%，取 −50%。股價已低於 52、104 週均線並貼著 250 週均線，技術面無緩衝。淨回購已含在 EPS 路徑的股數下降裡，殖利率欄填 0 避免重複計算。","trigger_time":null},"basis":{"bull":"資料中心 2027 年起每年 30 億美元以上並延續、住宅回到正常化台數、漲價黏住使營益率往同業 18–20% 收斂；EPS 年複合約 16%，終端 22 倍","base":"共識打折：2027 取 3.15（低於共識 3.25，反映退稅基期與結轉通膨），之後年增約 9–14% 逐步降速，營益率每年小幅擴張；終端 17 倍，較現值 19 倍略壓縮","bear":"漲價黏不住、資料中心 2028 年起放緩、住宅回到週期下行；EPS 年增約 2%，終端 13 倍（成長熄火到 5% 以下的工業股倍數）"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"Linesight 2026-06 稱關鍵設備需求超過全球產能、新增產能 2026 下半年至 2027 年緩解；Carrier 同時把美洲產能翻倍（Fort Worth），2026-07-28 法說執行長也說最擔心資料中心資本支出放緩時過度擴張","assumption":"資料中心需求在新產能到位後仍超過供給，住宅定價權沒有結構性流失","consequence":"若 2028 年前後資料中心資本支出降速、同業新產能湧入，商用冰水機陷入價格戰，再加上住宅定價權被進口與無風管侵蝕，營益率卡在 15% 以下、終端倍數 11–13 倍，五年後股價約 28–35 美元（−35%～−50%）","ruling":"部分採納：長約最低量承諾與逾 85 億美元在手訂單把 2027–2028 的量大致鎖住，2028 年前發生機率低；2029 年後需求能見度不足，Bear 機率維持 30%。與唯一致命點部分重疊：定價那一半就是唯一致命點，資料中心那一半另以訂單觸發器監測","watch":"資料中心訂單年增率（每季）、Fort Worth 投產時程、商用定價（財務長每季口述）","evidence_refs":["supply_demand_durability#3"],"fact_refs":["f_kpi7_backlog"]},{"view":"論點成功但股東經濟變差","evidence":"10-K 揭露部分產品線只有單一工廠能生產；第三季法說稱新冰水機初期供應鏈問題，風扇等零件改空運；AFFF 泡沫案逾 1.7 萬件並簽有和解與計畫支持協議；第三季營收指引上調近 10 億美元但調整後營業利益 35 億不變","assumption":"營收成長能按財務長說的 25–30% 轉換成營業利益","consequence":"成長兌現但每股盈餘被爬坡成本、緊急物流與訴訟現金流出吃掉，FCF 停在約 20 億美元不成長，回購力道下降","ruling":"採納為次要風險：第三季邊際轉換率逾 30%（財務長）尚未失守，但上調的營收沒有帶來營業利益上調，已是早期徵兆；AFFF 和解金額事實表未涵蓋，無法量化","watch":"財務長每季給的轉換率、FCF 指引、AFFF 和解進度","evidence_refs":["geo_supply_chain#0","regulatory_antitrust#1","lawsuit_class_action#0","major_events#0"],"fact_refs":["f_kpi4_free_cash_flow"]},{"view":"價格已反映太多","evidence":"FY1 共識 2.87 含第三季認列約 1.33 億美元關稅退稅（10-Q）；財務長稱 2027 規劃假設通膨逆風與 2026 一樣大；FY2、FY3 共識近期小幅下修","assumption":"2027 共識 3.25 美元可達","consequence":"扣退稅後 2026 基期約 2.75，2027 要成長約 18% 才到共識；若只成長 10%，2027 EPS 約 3.0，現價對應約 18 倍，不算便宜","ruling":"部分採納：估值結論停在黃、Base 2027 取 3.15 低於共識；但股價自前份已跌 13%、年度端點 P/S 處在最低，已反映部分利潤率疑慮，不判為價格反映太多","watch":"2027-02 公司給的 2027 EPS 指引對照共識 3.25","evidence_refs":["reg_tariff_export#2"],"fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_fwd_pe_latest"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 🟠 → 本次 ❌","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=🟠","side_b":"本次 ma=❌","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 63.16 → 本次 54.68（-13.4%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=63.16","side_b":"本次 price_at_dd=54.68","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]裁決由 dd_decision.py 機械路由：前份 進場 → 本次 觀望","cause":"方法變動","prior_field":["dca_verdict"],"side_a":"前份 dca_verdict=進場","side_b":"本次 dca_verdict=觀望","ruling":"裁決是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。沒有單一輸入能還原，屬多欄共同：均線 🟠→❌。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]角色由 dd_decision.py 機械路由：前份 衛星 → 本次 追蹤","cause":"方法變動","prior_field":["dca_role"],"side_a":"前份 dca_role=衛星","side_b":"本次 dca_role=追蹤","ruling":"角色是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。沒有單一輸入能還原，屬多欄共同：均線 🟠→❌。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 63.16 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 63.16 美元：Bull 價 154、Bear 價 38，五年期望值 +53.0%，基準年化 9.4%，不對稱比 3.7","side_b":"本次情境、股價仍用 63.16 美元：Bull 價 134.2、Bear 價 41.6，五年期望值 +26.9%，基準年化 5.3%，不對稱比 2.2","ruling":"先換情境、股價不動：五年期望值少 26.1 個百分點，基準年化少 4.1 個百分點。不對稱比由 3.7 變為 2.2。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 63.16 美元：五年期望值 +26.9%，基準年化 5.3%，不對稱比 2.2","side_b":"本次情境、股價 54.68 美元：五年期望值 +46.5%，基準年化 8.3%，不對稱比 4.05","ruling":"再換股價、情境不動：起點價下跌 13.4%，五年期望值多 19.7 個百分點，基準年化多 3.1 個百分點，不對稱比由 2.2 升到 4.05。合計五年期望值比前份少 6.5 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"前份加碼條件已觸發但實質未過，改設新的加碼條件","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"starter 1/3；加碼＝Q3 資料中心出貨兌現（營收 ≥$5.9B 且 OM ≥16.5%）或回落 $55 以下","side_b":"2027-02第四季財報三項全中才加碼：CSA住宅價格實現≥中個位數、扣一次性後營益率年增、2027 EPS指引雙位數成長","ruling":"前份加碼條件字面上已發火：第三季營收 62.63 億美元高於 59 億、調整後營益率 17.4% 高於 16.5%，股價 54.68 也跌破 55。但營益率含約 1.3 億美元關稅退稅，扣除後約 15.3%，低於門檻；財務長也說扣掉退稅後利潤率低於公司預期。條件的本意是驗證利潤率，實質沒過，所以不執行加碼，改以價格成本讀數為新的加碼條件","evidence_level":"高：營收與營益率來自公司新聞稿，退稅金額來自 10-Q","settle_metric":"2027-02 第四季財報的住宅價格實現與扣一次性營益率","if_then":["若 2027-02 三項全中，則首倉加到目標倉位、分兩次執行","若價格實現仍低個位數，則不加碼並把首倉減半"],"evidence_refs":[]},{"axis":"Single Thing 新設：價格成本取代分散風險","cause":"新證據","prior_field":null,"side_a":"前份未設唯一致命點（空值）","side_b":"2027 年漲價落地失敗：住宅約 8%（CSA 最高 10%）漲價本季末生效，若 2027 年第二季財報（約 2027-07 底）CSA 住宅價格實現仍為低個位數、價格成本淨額為負","ruling":"前份把風險分散在資料中心執行、歐洲成本與併購回報三條；第三季資料中心出貨逾 5.5 億美元、全年 20 億目標維持，執行風險降級；住宅價格實現低於預期、財務長預告 2027 通膨逆風與今年相當，價格成本成為數學上最大的單一敏感項（全額失效約每股 0.75 美元、占 2027 共識兩成以上），因此新設此唯一致命點，發生即清倉","evidence_refs":[]},{"axis":"停損指標新設（減碼與清倉門檻）","cause":"方法變動","prior_field":null,"side_a":"前份未設停損指標（空值）","side_b":"CSA 住宅價格實現 2027 上半年仍 ≤3%；扣一次性調整後營益率連 2 季年減；在手訂單低於 70 億美元；FY2027 共識 EPS 低於 3.00 美元","ruling":"本輪改為每個核心假設配一個可量測停損：任一觸發即減碼一半；前兩項與唯一致命點同時成立即清倉","evidence_refs":[]},{"axis":"護城河方向、整體訊號與陷阱判斷","cause":"新證據","prior_field":["moat_trend","signal","trap"],"side_a":"前份：護城河持平、訊號 B、陷阱黃","side_b":"本次：護城河持平、訊號 B、陷阱黃（值不變，依據換新）","ruling":"三欄值不變但理由換了：資料中心執行與份額（超大規模客戶逾 30 億美元長約、在手訂單逾 85 億）比前份更強，住宅定價力比前份更弱（價格實現低個位數、全年投入成本逆風約 8 億美元）。一升一降判持平；衰退訊號亮兩個（年度毛利率自 2023 年 27.2% 連降、TTM 24.6%；共識 EPS 成長高於營收成長逾 5pp），陷阱維持黃","evidence_refs":[]},{"axis":"五年後跑道、公司類型與循環位置","cause":"新證據","prior_field":["runway_post_y5","archetype","cycle_position"],"side_a":"前份：五年後跑道寬、品質複利成長型、早循環","side_b":"本次：跑道寬、品質複利成長型（信心降為低）、早循環","ruling":"北美住宅市場由預期 700 萬台以下上修到 750–800 萬台，但仍低於前份假設的正常化 900 萬台，維持早循環；跑道靠資料中心與歐洲熱泵取代鍋爐兩條有據可查的曲線維持寬；公司類型不改，但歐洲商譽減損 31 億美元與毛利率落後同業 8–12pp 讓品質這個前提的信心降為低，若 2027 價格成本失敗改列循環型","evidence_refs":[]},{"axis":"裁決與倉位角色","cause":"新證據","prior_field":[],"side_a":"前份：進場、衛星","side_b":"本次：首倉不動、等 2027-02 讀數再加碼（倉位角色依新輸入重算）","ruling":"前份進場理由是資料中心兌現與 55 美元以下的價格，兩者都到了；但新出現的價格成本證據直接打到第三條假設，加碼前要先看漲價有沒有黏住，因此改為等待事件，不追價","evidence_refs":[]},{"axis":"估值結論","cause":"價格變動","prior_field":["val"],"side_a":"前份股價 63.16 美元，估值結論黃","side_b":"本次股價 54.68 美元（約 −13.4%），FY2、FY3 共識只下修 1.52%、1.58%，估值結論仍黃","ruling":"股價跌幅約是共識下修的八倍，FY1 本益比由約 22 倍降到 19 倍；便宜了，但 FY1 含退稅一次性、2027 要在結轉通膨下成長約 13%，分母有風險，所以不升為綠","evidence_refs":[]},{"axis":"情境機率與回撤","cause":"方法變動","prior_field":["p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份 Bull 24%、Bear 30%，最大回撤 −50%（單點）","side_b":"本次 Bull 20%、Base 50%、Bear 30%，最大回撤 −35%～−50%（範圍）","ruling":"三支 EPS 路徑依第三季資料重建：Base 2027 年取 3.15（低於共識 3.25），Bull 機率因住宅定價證據轉弱下調 4pp；回撤改為以谷底 EPS 乘倍數推出的範圍，不再用單點","evidence_refs":[]},{"axis":"住宅定價權有沒有結構性流失","cause":"新證據","prior_field":null,"side_a":"管理層（2026-10-29 法說，執行長）：住宅是好生意，今年是關稅與原物料突然上漲造成的時間差，市場本質沒變，2027 會先漲價（住宅約 8%、CSA 最高 10%）","side_b":"證據：第三季住宅價格實現只有低個位數（前一季預期中個位數；2026-07-28 法說執行長預估全年約 4%），分析師兩度追問亞洲進口與無風管占比上升；同一環境下 LII 營益率 19.9%、TT 17.9%，Carrier 只有 8.1%，毛利率差 8–12pp 未收斂","ruling":"方向相反、不可調和。暫採管理層一側但打折：第三季各分部價格皆為正、財務長稱商用定價為正，住宅量回升逾 30% 也不是靠降價換來；但不把本質沒變當成已證事實，標為未證、監測，2027 上半年住宅價格實現是決勝數據。現在就買的最強論證：股價較前份跌 13% 而共識只降 1.5%，FY2 本益比 16.8 倍，資料中心在手訂單與最低量長約已鎖住 2027 商用成長大半，定價問題若真是時間差，現價等於把它當成永久","evidence_level":"中：價格實現來自管理層口述，同業價格實現事實表未涵蓋","settle_metric":"CSA 住宅價格實現（2027 年第一、二季法說）與 CSA 分部營益率扣一次性","if_then":["若 2027-02 讀數價格實現達中個位數且營益率年增，則首倉加到目標倉位","若 2027-07 讀數價格實現仍低個位數且 CSA 營益率年減，則清倉","若股價先漲回 60 美元以上但讀數未到，則不追","若股價續跌到 48 美元以下（FY2 本益比約 14.8 倍）且資料中心與住宅量能門檻未破，則分批反買，單次不超過目標倉位三分之一"],"evidence_refs":[]},{"axis":"住宅量能：年初悲觀假設對照第三季實績","cause":"新證據","prior_field":null,"side_a":"2026-02-06 第四季法說：住宅量大幅下滑，假設 2026 美國產業台數下滑 10–15%，需求偏弱直到房貸利率與信心改善","side_b":"2026-10-29 法說：北美住宅市場追蹤到 750–800 萬台（原預期 700 萬以下），CSA 住宅銷售年增逾 30%，通路庫存與去年持平","ruling":"程度差異、可調和：年初假設已被新數據取代。但第三季增幅有一大塊是去年去庫存不再重現（2026-07-28 法說執行長稱下半年約 20% 成長中 10 個百分點來自此），兩年疊加是否真正改善管理層未正面回答；住宅回升判為週期性，不當成結構性","evidence_level":"中：台數為管理層口述","settle_metric":"2027 北美住宅市場台數與 CSA 住宅銷售年增","if_then":["若 2027 北美住宅台數低於 750 萬，則住宅假設判削弱、停止加碼"],"evidence_refs":["supply_demand_durability#2"]},{"axis":"管理層承諾落差：新廠時程與利潤率指引","cause":"新證據","prior_field":null,"side_a":"2026-07-28 法說：執行長說美國新廠目標在第一季底投產；財務長給第三季營益率約 16.5%、全年 EPS 約 2.90 美元、2027 年起增量轉換率 25–30%；執行長估 CSA 住宅全年價格約 4%","side_b":"2026-10-29 法說：Fort Worth 新廠 2027 年夏末才開始交貨；第三季扣退稅後利潤率低於公司預期；全年 EPS 指引改為 2.85–2.90，營收上調近 10 億美元但調整後營業利益 35 億不變；住宅價格實現低個位數","ruling":"方向一致但程度落差、可調和：營收超、利潤不跟，上調的近 10 億美元營收邊際轉換為零，與先前講的 25–30% 不符；新廠延後約兩季，資料中心 2027 產能爬坡往後推。管理層對利潤率與時程的承諾打折，2027 雙位數 EPS 成長目標同樣打折，所以 Base 取 3.15 低於共識","evidence_level":"高：兩場法說逐字稿","settle_metric":"2027-02 公司給的 2027 EPS 指引與新廠時程","if_then":["若 2027-02 給的 2027 EPS 指引低於 3.10 美元，則 Base 路徑下修並停止加碼"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"2027 年第二季財報 CSA 住宅價格實現仍為低個位數，且扣一次性後 CSA 分部營益率年減","type":"Single Thing","maps_to":"R1","metric":"CSA 住宅價格實現；CSA 分部營益率（扣一次性）","threshold":"價格實現 ≤3% 且營益率年減","action":"清倉","source_freq":"季度法說","date":"2027-07"},{"n":2,"text":"第四季財報三項全中：CSA 住宅價格實現 ≥中個位數、扣一次性後調整後營益率年增、2027 EPS 指引雙位數成長","type":"加碼","maps_to":"H3","metric":"住宅價格實現；調整後營益率（扣一次性）；2027 EPS 指引","threshold":"三項全中","action":"首倉加到目標倉位，分兩次執行","source_freq":"季度財報","date":"2027-02"},{"n":3,"text":"資料中心 2026 全年營收達 20 億美元、在手訂單維持 85 億美元以上","type":"假設驗證","maps_to":"H1","metric":"資料中心營收；總在手訂單","threshold":"≥20 億美元；≥85 億美元","action":"達標維持；任一未達停止加碼","source_freq":"季度財報","date":"2027-02"},{"n":4,"text":"資料中心訂單連 2 季年減，或 Fort Worth 交貨延到 2027 年第四季以後","type":"減碼","maps_to":"R2","metric":"資料中心訂單年增率；新廠交貨時程","threshold":"連 2 季低於 0%；延到 2027 年第四季以後","action":"減碼一半","source_freq":"季度法說","date":"2027"},{"n":5,"text":"HVAC 聯合訂價案駁回聲請被否決並進入集體認證，或證券集體訴訟正式提起（目前只有律所招攬投資人、未見訴狀）","type":"風險","maps_to":"R3","metric":"法院程序進度","threshold":"集體認證通過、不利和解或證券訴狀提起","action":"減碼至半倉","source_freq":"10-Q 與法院公告","date":"2027","evidence_refs":["regulatory_antitrust#2","major_events#3","lawsuit_class_action#1"]},{"n":6,"text":"AFFF 泡沫案和解或判決的一次性費用超過市值 5%（約 22 億美元）；現有計提與和解金額事實表未涵蓋","type":"風險","maps_to":"R3","metric":"AFFF 一次性費用","threshold":"高於 22 億美元","action":"減碼一半","source_freq":"10-Q 與 10-K","date":null,"evidence_refs":["regulatory_antitrust#1","major_events#0","lawsuit_class_action#0"]},{"n":7,"text":"新關稅或 Section 232 鋼鋁銅關稅擴大，使財務長給的 2027 投入成本逆風超過 2026 的約 8 億美元","type":"風險","maps_to":"R1","metric":"財務長揭露的年度投入成本逆風","threshold":"高於 8 億美元","action":"停止加碼","source_freq":"季度法說","date":"2027-02","evidence_refs":["reg_tariff_export#1","geo_supply_chain#1"]},{"n":8,"text":"歐洲分部 2027 全年營益率未高於 2026","type":"風險","maps_to":"R4","metric":"歐洲分部營益率","threshold":"2027 不高於 2026","action":"停止加碼","source_freq":"季度財報","date":"2028-02"},{"n":9,"text":"2027 年 2 月第四季財報後重跑完整判斷","type":"複審日期","maps_to":null,"metric":null,"threshold":null,"action":"重跑判斷","source_freq":"一次","date":"2027-02"}],"kill_metrics":[{"metric":"CSA 住宅價格實現（年增）","bear_threshold":"2027 上半年仍 ≤3%（低個位數）","window":"2027 年第一、二季財報","source":"季度法說管理層口述","last_status":"warning"},{"metric":"公司調整後營益率（扣關稅退稅等一次性）年變化","bear_threshold":"連 2 季年減","window":"2027 年各季","source":"季度新聞稿與法說","last_status":"ok"},{"metric":"總在手訂單","bear_threshold":"低於 70 億美元","window":"2027 年任一季","source":"季度新聞稿","last_status":"ok"},{"metric":"FY2027 共識調整後 EPS","bear_threshold":"低於 3.00 美元","window":"未來 2 季","source":"Koyfin 共識快照","last_status":"ok"}],"action_conditions":{"rearm_trigger":"2027-02第四季財報三項全中才加碼：CSA住宅價格實現≥中個位數、扣一次性後營益率年增、2027 EPS指引雙位數成長","exec_line":"首倉不動、不追；2027-02 三項全中加到目標倉位，分兩次、間隔一季；唯一致命點成立即清倉；停損指標任一觸發減碼一半"}},"decision_inputs":{"signal":"B","ma":"❌","cycle_position":"早循環","cycle_verdict":"未觸發","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場把今年住宅漲價跟不上成本當成定價權永久流失，股價較 7 月底跌 13%，FY2027 共識只降 1.5%；資料中心長約最低量承諾與逾 85 億美元在手訂單已鎖住 2027 商用成長，這部分被低估。住宅定價那一半市場可能是對的，要等 2027 上半年讀數裁決。","momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":false,"wait_for_price":true,"wait_for_price_condition":"等 2027-02 第四季財報：CSA 住宅價格實現 ≥中個位數、扣一次性後營益率年增、2027 EPS 指引雙位數成長，三項全中才加碼；期間首倉不動","asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null},"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8w(原9)","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='C'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":true,"basis":"ma='❌'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場把今年住宅漲價跟不上成本當成定價權永久流失，股價較 7 月底跌 13%，FY2027 共識只降 1.5%；資料中心長約最低量承諾與逾 85 億美元在手訂單已鎖住 2027 商用成長，這部分被低估。住宅定價那一半市場可能是對的，要等 2027 上半年讀數裁決。"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟢', val='🟡', moat_trend='→', week26=-16.36, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position='早循環', moat='C', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":false,"basis":"signal='B', val='🟡'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":true,"basis":"signal='B', val='🟡', ma='❌'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟡', ma='❌'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟡', ma='❌'"},{"row":"8w","condition":"判斷者宣告 wait_for_price（價格合理但要等）→ 原 row9 進場改觀望（等價格）","hit":true,"basis":"wait_for_price=True, 等待條件='等 2027-02 第四季財報：CSA 住宅價格實現 ≥中個位數、扣一次性後營益率年增、2027 EPS 指引雙位數成長，三項全中才加碼；期間首倉不動'"},{"row":"QC-49","condition":"qc49_inherit_prior=False，不套用","hit":false,"basis":"qc49_inherit_prior=False"},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":["row4：週線❌，進場節奏強制分批（starter 1/3＋趨勢確認後加碼），頁首掛「⚠️ 週線趨勢未確認，逢回分批勿接刀」"],"holding_cap":null,"requires_critic":[]},"thesis":{"H":[{"id":"H1","text":"資料中心與非資料中心商用暖通是可持續的第二成長曲線：在手訂單與長約最低量承諾撐住 2027–2028 商用雙位數成長，Fort Worth 新產能到位後不閒置","2y":null,"5y":"2031 年商用＋售後占組合過半、資料中心營收年化 40 億美元以上（判斷目標）","10y":null,"threshold":"資料中心營收 2026 年 ≥20 億美元、2027 年 ≥30 億美元；總在手訂單 ≥85 億美元；不含資料中心的商用訂單年增 ≥10%","source":"季度新聞稿與法說（資料中心營收與訂單、在手訂單、商用訂單）","drift_rule":"5 年期：任一門檻連 4 季偏離 ≥5% 判削弱，連 6 季偏離 ≥10% 判反轉"},{"id":"H2","text":"北美住宅暖通走出去庫存，回升不靠降價：市場由 2026 年約 750–800 萬台往正常化走","2y":"2027–2028 北美住宅市場 ≥800 萬台、CSA 住宅銷售連年成長、通路庫存不高於前一年","5y":null,"10y":null,"threshold":"2027 北美住宅市場 ≥800 萬台；CSA 住宅銷售年增為正；年底通路庫存與前一年持平或更低","source":"季度法說（市場台數、通路庫存、CSA 住宅銷售）","drift_rule":"2 年期：連 2 季偏離 ≥5% 判削弱，連 3 季偏離 ≥10% 判反轉"},{"id":"H3","text":"價格成本可以回正：2027 年漲價（住宅約 8%、CSA 最高 10%）落地，抵銷與 2026 相當的結轉通膨，扣一次性後營益率恢復年增","2y":"2027 年扣一次性調整後營益率年增 ≥50bp、2028 年 CSA 分部營益率回到 20% 以上","5y":null,"10y":null,"threshold":"2027 上半年 CSA 住宅價格實現 ≥中個位數（約 4% 以上）；2027 全年扣一次性調整後營益率年增 ≥50bp","source":"2026 第四季與 2027 各季財報法說（價格實現、價格成本淨額）","drift_rule":"2 年期：連 2 季偏離 ≥5% 判削弱，連 3 季偏離 ≥10% 判反轉"}],"R":[{"id":"R1","text":"價格成本再失手：財務長規劃 2027 通膨逆風與 2026 相當（全年約 8 億美元、略低於一半是關稅），10-K 也揭露在中國、墨西哥生產與採購的關稅與出口管制風險；漲價若黏不住，營益率續壓","h_ref":"H3","clock":"⚡","threshold":"2027 年第一、二季 CSA 住宅價格實現 ≤3% 且 CSA 分部營益率（扣一次性）年減","evidence_refs":["reg_tariff_export#1","geo_supply_chain#1"]},{"id":"R2","text":"資料中心交付與產能爬坡：新冰水機初期供應鏈問題（風扇等改空運）、部分產品線只有單一工廠，Fort Worth 由原訂 2027 年第一季底延到夏末交貨；需求降速時新產能可能閒置","h_ref":"H1","clock":"🔥","threshold":"資料中心訂單連 2 季年減，或 Fort Worth 交貨延到 2027 年第四季以後","evidence_refs":["geo_supply_chain#0"]},{"id":"R3","text":"訴訟：AFFF 泡沫案逾 1.7 萬件已併入南卡羅來納多區訴訟並簽有和解與計畫支持協議；2026 年 3 月起被列為 HVAC 聯合訂價推定集體訴訟被告（密西根東區聯邦地院，民事集體案），2026-10-09 聲請駁回、簡報延至 2027；受影響營收與和解金額事實表未涵蓋","h_ref":"H3","clock":"🐢","threshold":"聯合訂價案進入集體認證或不利和解；AFFF 一次性費用高於市值 5%（約 22 億美元）","evidence_refs":["regulatory_antitrust#1","regulatory_antitrust#2","major_events#0","lawsuit_class_action#0"]},{"id":"R4","text":"歐洲修復是多年工程：執行長 2026-07-28 承諾未來數年達到中十位數營益率，第三季已是雙位數但同季提列 31 億美元商譽減損；成本削減（產能配置、供應鏈、全公司最高的管銷費用）仍在進行","h_ref":"H3","clock":"🔥","threshold":"2027 全年歐洲分部營益率不高於 2026","evidence_refs":[]}],"single_thing":{"description":"2027 年漲價落地失敗：住宅約 8%（CSA 最高 10%）漲價本季末生效，若 2027 年第二季財報（約 2027-07 底）CSA 住宅價格實現仍為低個位數、價格成本淨額為負","why_fatal":"這是數學上最大的單一敏感項：財務長規劃 2027 投入成本逆風與今年約 8 億美元相當，若漲價全數失效，以約兩成稅率粗估約每股 0.75 美元，占 2027 共識 3.25 美元兩成以上；同時會證實住宅定價權結構性流失，終端倍數由 17 倍往 13 倍走。其他單項（資料中心出貨打折、歐洲修復延後）影響都較小","if_happens":"Bear 機率升到 45% 以上、護城河趨勢改判下降，依規則轉為迴避並清倉","how_monitor":"每季法說的 CSA 住宅價格實現、CSA 分部營益率（扣一次性）、財務長的價格成本淨額；第一個讀數 2027-02 第四季財報，決定讀數 2027-07 第二季財報","probability":"約 35%（12–24 個月）"}},"appendix_a":{"growth_durability":6,"quality_score":6,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":16.8,"peg_fy2":1.1,"stress":{"pass":2,"total":3}},"eps_meta":{"base_eps_path":{"FY2025A":2.61,"FY2026E":2.87,"FY2027E":3.25,"FY2028E":3.73},"fy_end_month":12,"eps_basis":"調整後 EPS（非 GAAP）。FY2026–2028 為 Koyfin 2026-10-31 共識，家數事實表未涵蓋。FY2025 調整後實際值事實表未涵蓋，以 2026-10-29 法說「2026 年調整後 EPS 雙位數成長」與指引中點 2.875 回推上限：2.875÷1.10 約 2.61，故三年年複合約 12.6% 是下限；GAAP 稀釋 EPS 1.72 含一次性項目，口徑不同不採用"},"catalysts":[{"date":"2026-12","date_precision":"month","type":"other","event":"CSA 住宅約 8% 漲價生效（本季末）","impact":"中","watch":"安裝商提前備貨與價格接受度"},{"date":"2027-02","date_precision":"month","type":"guidance","event":"第四季財報與 2027 全年指引","impact":"高","watch":"住宅價格實現、2027 EPS 指引對照共識 3.25、新廠時程"},{"date":"2027-07","date_precision":"month","type":"guidance","event":"第二季財報：漲價是否黏住的決定讀數","impact":"高","watch":"CSA 住宅價格實現與 CSA 分部營益率扣一次性"},{"date":"2027-Q3","date_precision":"quarter","type":"capacity","event":"Fort Worth 新廠開始交貨","impact":"中","watch":"是否再延後、美洲商用產能是否如期倍增"}]}
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
