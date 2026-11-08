你是 DD 管線 v20 的判斷層閘（gate），標的 ETN（20261108）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（39 條）
- `f_kpi0_gaap`（q1_business）｜營收（GAAP）＝8947 百萬美元｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-11-03）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Eaton 新聞稿 8-K Ex.99（SEC）（numbers.latest_quarter_kpis.items[0]，as_of Q3 2026（季末 2026-09-30，公告於 2026-11-03））
  - 註記：未查得
- `f_kpi1_segment_eaton_non_gaap`（q1_business）｜Segment 營業利益／利益率（Eaton 以此替代 Non-GAAP 營業利益）＝25.3 %（營業利益 $2,263M）｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-11-03）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Eaton 新聞稿 8-K Ex.99（SEC）（numbers.latest_quarter_kpis.items[1]，as_of Q3 2026（季末 2026-09-30，公告於 2026-11-03））
  - 註記：未查得
- `f_kpi2_eps_non_gaap`（q1_business）｜調整後 EPS（Non-GAAP）＝3.68 美元｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-11-03）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Eaton 新聞稿 8-K Ex.99（SEC）（numbers.latest_quarter_kpis.items[2]，as_of Q3 2026（季末 2026-09-30，公告於 2026-11-03））
  - 註記：未查得
- `f_kpi4_backlog_book_to_bill`（q1_business）｜Backlog 與 book-to-bill＝Electrical 總 backlog 年增 +46%（Americas +33%、Global +121%）；Aerospace +33%；滾動 12 個月 book-to-bill：Electrical 1.2、Aerospace 1.2 YoY／倍｜期間與口徑：Q3 2026（截至 2026-09 底，公告於 2026-11-03）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Eaton 新聞稿 8-K Ex.99（SEC）；美元 backlog 金額未揭露（numbers.latest_quarter_kpis.items[4]，as_of Q3 2026（截至 2026-09 底，公告於 2026-11-03））
  - 註記：不適用
- `f_kpi5`（q1_business）｜管理層指引＝Q4：有機成長 13–15%、segment margin 25.4–25.8%、調整後 EPS $4.05–$4.15、GAAP EPS $3.28–$3.38；全年：有機成長 13–15%（上修）、segment margin 24.1–24.5%、調整後 EPS $13.70–$13.80、GAAP EPS $10.39–$10.49 區間｜期間與口徑：Q3 2026（公告於 2026-11-03）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：Eaton 新聞稿 8-K Ex.99（SEC）；未提供 FCF 指引（numbers.latest_quarter_kpis.items[5]，as_of Q3 2026（公告於 2026-11-03））
  - 註記：全年 FY1 共識 EPS 13.67（來源：consensus_revision，2026-11-07 快照），指引區間上緣略高
- `f_peer_etn_gross_margin_pct`（q2_moat）｜ETN 毛利率＝35.05 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ETN.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_etn_operating_margin_pct`（q2_moat）｜ETN 營業利益率＝17.32 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ETN.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_etn_fcf_margin_pct`（q2_moat）｜ETN FCF 利潤率＝11.87 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ETN.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_vrt_gross_margin_pct`（q2_moat）｜VRT 毛利率＝38.12 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.VRT.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_vrt_operating_margin_pct`（q2_moat）｜VRT 營業利益率＝20.35 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.VRT.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_vrt_fcf_margin_pct`（q2_moat）｜VRT FCF 利潤率＝23.74 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.VRT.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_2308_tw_gross_margin_pct`（q2_moat）｜2308.TW 毛利率＝35.27 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.2308.TW.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_2308_tw_operating_margin_pct`（q2_moat）｜2308.TW 營業利益率＝16.98 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.2308.TW.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_2308_tw_fcf_margin_pct`（q2_moat）｜2308.TW FCF 利潤率＝9.46 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.2308.TW.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝13.67 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-11-07）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝16.28 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-11-07）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝18.94 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-11-07）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝33685.48 USD m｜期間與口徑：2026-11-08／yfinance revenue_estimate 0y 平均（25 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝37420.13 USD m｜期間與口徑：2026-11-08／yfinance revenue_estimate +1y 平均（27 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi3_fcf`（q4_capital）｜自由現金流（FCF）＝1034 百萬美元｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-11-03）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Eaton 新聞稿 8-K Ex.99（SEC）：營業現金流 $1,310M－資本支出 $275M（numbers.latest_quarter_kpis.items[3]，as_of Q3 2026（季末 2026-09-30，公告於 2026-11-03））
  - 註記：未查得
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝20104.0 USD m｜期間與口徑：2026-11-08／yfinance 最新一季：總債務 20922.0、現金 818.0（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝388.5 m shares｜期間與口徑：2026-11-08／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝0.966 %｜期間與口徑：2026-11-08／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-11-08）
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝341.72 USD｜期間與口徑：2026-11-06（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-11-06（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝25.0 x｜期間與口徑：2026-11-07／分母＝FY1 EPS 13.67，分子＝快照價 341.72｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-11-07）
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝34.14 x｜期間與口徑：2026-11-06（RTH 收盤，UTC）／4 個年度端點內的分位＝88.7｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-11-06（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝88.7 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝4.15 x｜期間與口徑：2026-11-06（RTH 收盤，UTC）／4 個年度端點內的分位＝49.2｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝49.2 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝4.78 x｜期間與口徑：2026-11-06（RTH 收盤，UTC）／4 個年度端點內的分位＝58.8｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝58.8 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝1.18 %｜期間與口徑：2026-08-13 → 2026-11-07／FY1 共識 EPS 13.51 → 13.67（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-11-07）
- `f_ev_m`（q5_valuation）｜目前企業價值 EV（市值＋淨負債）＝152862.22 USD m｜期間與口徑：2026-11-08／市值 132758.22 ＋ 淨負債 20104.0｜kind：realized
  - 來源：—（numbers.capital_structure.ev_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝-14.68 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-11-06（RTH 收盤，UTC））
- `f_rsi14`（q5_valuation）｜RSI(14)＝36.99｜期間與口徑：2026-11-06（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ma_state`（q5_valuation）｜週線均線六態（decision_inputs.ma 必須等於此值）＝🟠｜期間與口徑：2026-11-08／timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）
  - 原文：「price 341.72 / W52 382.26 / W104 357.58 / W250 268.53 / W250 13週斜率 1.27%」
- `f_ma_w52`（q5_valuation）｜52 週均線＝382.26 USD｜期間與口徑：2026-11-08／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）
- `f_ma_w104`（q5_valuation）｜104 週均線＝357.58 USD｜期間與口徑：2026-11-08／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）
- `f_ma_w250`（q5_valuation）｜250 週均線＝268.53 USD｜期間與口徑：2026-11-08／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）

### findings_digest 中方向為負或來源衝突的條目（11 條）
- `competitive_share_entrants#1`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K 風險因子承認新進入者可能衝擊其產品或區域市場地位；漲價等因應措施也可能損及市占。未點名具體新進入者。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-26）｜affects：decision_inputs.bear、moat_trend
- `supply_demand_durability#2`（supply_demand_durability｜方向 -｜狀態 ok）：Power Magazine 摘要：斷路器與開關設備市場有顯著供給過剩，但產能投資有限，限制可能在採購與專案排程而非產能；另有觀點認為缺口是採購做法造成
  - 來源：POWER Magazine, Making the Connection executive summary (Sept 2025)（as_of 2025-09-30）｜affects：decision_inputs.bear、moat_trend
- `supply_demand_durability#3`（supply_demand_durability｜方向 -｜狀態 ok）：JPMorgan（經 Nasdaq 引述）：2027 規劃資料中心容量超過 60% 尚未開工；分析指 Eaton 資料中心訂單成長由 Q1 的 240% 降至 Q2 的 85%，電力 Americas 積壓成長由 44% 降至 33%（皆為搜尋摘要，來源品質混雜）
  - 來源：Nasdaq, data center delays create opportunity（as_of 2026-07-01）｜affects：decision_inputs.bear、triggers
- `regulatory_antitrust#1`（regulatory_antitrust｜方向 -｜狀態 ok）：Eaton 2026 Q3 10-Q 法律或有事項列有反壟斷與貿易管制類事項，最終結果若不如預期可能有重大不利影響
  - 來源：SEC EDGAR 10-Q（2026-09-30 季）（as_of 2026-11-03）｜affects：decision_inputs.bear
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：Eaton 10-K FY2025 風險因素：貿易政策變動（關稅、制裁、配額）可能實質增加成本、衝擊產品毛利，並使出口至他國更困難或昂貴；供應商面臨關稅與貿易限制風險。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-26）｜affects：decision_inputs.bear、thesis.R
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：Eaton FY2025 10-K 風險因子列出國際營運面對政治不穩、關稅與貿易限制、地緣事件造成供應鏈中斷（一般性揭露，無特定國家集中度）
  - 來源：Eaton Corp plc Form 10-K FY2025（as_of 2026-02-01）｜affects：decision_inputs.bear
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：Eaton 10-K 風險因子自述：其產品所服務的資料中心等市場曾出現並可能持續出現突發的破壞性技術，可能衝擊終端市場；且新進入者可能影響其地位。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-26）｜affects：moat_trend、thesis.R、decision_inputs.bear
- `substitute_technology#1`（substitute_technology｜方向 -｜狀態 ok）：Siemens 與 Reinhausen 開發中壓固態變壓器供 800V DC AI 資料中心；Sungrow 2026-07 推出 800V DC SST（競爭者進入同一替代架構）
  - 來源：Bayern Innovativ: New Transformer for Data Centers（as_of 2026-09-01）｜affects：moat_trend、thesis.R
- `capital_markets_pricing#4`（capital_markets_pricing｜方向 -｜狀態 ok）：UBS 將 ETN 降至 Neutral，12 個月目標價由 $440 降至 $360，理由為估值偏高、近期盈餘上行空間有限（發布日期搜尋結果未載明）
  - 來源：iTiger: UBS Downgrades Eaton to Neutral（as_of 2026-11-08）｜affects：valuation、decision_inputs.bear
- `major_events#3`（major_events｜方向 -｜狀態 ok）：NHTSA 召回 25E076000（Eaton E-Locker 差速器，約 289 輛，2025-11-14 通報），規模小。
  - 來源：vehiclesafetyrecalls.com／NHTSA（as_of 2025-11-14）｜affects：decision_inputs.bear
- `product_recall_warning#0`（product_recall_warning｜方向 -｜狀態 ok）：NHTSA 召回 25E076000（Eaton E-Locker 差速器，約 289 輛），2025-11-14 通報。
  - 來源：vehiclesafetyrecalls.com／NHTSA（as_of 2025-11-14）｜affects：decision_inputs.bear

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 4 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ETN_20261108/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":858.0,"bear_5y_price":259.2,"p_bull_pct":25,"p_bear_pct":30,"upside_5y_pct":68.3,"ev5y_pct":61.2,"irr_base_pct":11.0,"asym_ratio":5.2,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":13.67,"pe":25.0,"basis":"FY1（FY2026E）共識調整後 EPS 與判斷日股價 341.72 美元，終端倍數同為當年度 EPS 口徑。"},"eps":{"bull":[17.0,20.5,24.5,28.8,33.0],"base":[16.0,18.5,20.9,23.0,25.0],"bear":[15.4,16.4,14.8,15.2,16.2]},"pe":{"bull":26,"base":23,"bear":16},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0.966,"net_buyback":0},"second_stage":{"bull_cagr_pct":12,"base_cagr_pct":8},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### ETN_Q2_2026_Earnings_Call_20260731.md
- 2026-07-31｜Paulo Sternadt｜guidance：全年有機成長指引上調至 11%–13%（中點 +200bp）（原話："total organic growth to be between 11% and 13%"）
- 2026-07-31｜Paulo Sternadt｜guidance：全年調整後 EPS 指引 13.40–13.60 美元，中點 13.50（原話："we expect full year EPS to be between $13.40 and $13.60"）
- 2026-07-31｜Paulo Sternadt｜guidance：Electrical Americas 有機成長中點上調 200bp 至 15%（原話："up 200 basis points to a midpoint of 15% growth"）
- 2026-07-31｜Paulo Sternadt｜guidance：Electrical Global 有機成長中點上調 450bp 至 12%（原話："basis points to a midpoint of 12% growth."）
- 2026-07-31｜Paulo Sternadt｜guidance：各部門利潤率指引區間維持不變（原話："confidence to reaffirm our segment margin guidance ranges"）
- 2026-07-31｜Paulo Sternadt｜guidance：全年現金流預期維持不變（原話："We are reaffirming our cash flow expectations for the year."）
- 2026-07-31｜Paulo Sternadt｜guidance：Boyd 全年營收上調至 18 億美元，其中 15 億計入 Eaton（原話："Boyd's full year revenues to $1.8 billion of which $1.5 billion"）
- 2026-07-31｜Paulo Sternadt｜guidance：全年有機成長指引逐次上調的軌跡（年初 8%）（原話："We started the year saying we'll grow 8%."）
- 2026-07-31｜Paulo Sternadt｜guidance：CEO 對下半年指引的描述：仍屬審慎（原話："We are very prudent here"）
- 2026-07-31｜Paulo Sternadt｜guidance：管理層估計今年整體可服務市場成長約 10%（原話："our total addressable market will grow about 10% this year"）
- 2026-07-31｜David Foster｜margin：Electrical Americas Q2 利潤率 27.5%，較 Q1 高 190bp（原話："margins of 27.5%, 190 basis points higher than Q1"）
- 2026-07-31｜David Foster｜margin：Americas 年減的利潤率降幅主要來自暫時性負價格/成本（原話："margin decline was driven by temporary negative price/cost."）
- 2026-07-31｜David Foster｜margin：下半年價格/成本影響預期回到大致中性（原話："this will return to a roughly neutral impact"）
- 2026-07-31｜David Foster｜margin：Q1→Q2 Americas 190bp 拆解：約 100bp 價格/成本、90bp 產出（原話："About 100 points of that was price/cost and the other 90 points was pure output"）
- 2026-07-31｜David Foster｜margin：Americas 下半年對上半年利潤率改善 450–500bp，其中 300bp 來自價格/成本、150–200bp 來自產出與生產力（原話："We'll be up 450 to 500 basis points."）
- 2026-07-31｜David Foster｜margin：漲價措施已在 Q2 或 8 月初全部落地（原話："our pricing actions have either been implemented in Q2 or early August."）
- 2026-07-31｜David Foster｜margin：Q2→Q3 Americas 改善 250bp（150bp 價格/成本、100bp 產出生產力）（原話："Q2 to Q3, which is a 250 basis point improvement"）
- 2026-07-31｜David Foster｜margin：Q3→Q4 Americas 改善 200–250bp（150bp 價格/成本、50–100bp 產出生產力）（原話："it's a 200 to 250 basis point improvement"）
- 2026-07-31｜David Foster｜margin：CFO 稱 7 月初步數據較 Q2 續有改善（原話："I have early reads on July as of this morning."）
- 2026-07-31｜David Foster｜margin：Q3 與 Q4 利潤率改善部分來自非加班、較少溢價成本（原話："we're going to be doing it on regular time versus overtime"）
- 2026-07-31｜David Foster｜margin：Electrical Global Q2 利潤率 19.8%，年減 30bp（原話："Operating margin of 19.8% was down 30 basis points"）
- 2026-07-31｜David Foster｜margin：Electrical Global 一般性漲價由 Q4 提前至 Q3（原話："pulled in our planned general price increase from Q4 to Q3"）
- 2026-07-31｜David Foster｜margin：Aerospace 利潤率擴張 60bp 至 22.8%（原話："Total Aerospace operating margin expanded by 60 basis points to 22.8%"）
- 2026-07-31｜David Foster｜margin：EPS 口徑：分部利潤優於指引 0.25 美元，被較高稅率 0.15 美元部分抵銷（原話："offset by $0.15 from a higher tax rate."）
- 2026-07-31｜Paulo Sternadt｜margin：IEEPA 退款對 Q2 影響低於 300 萬美元（不到 0.01 美元 EPS）（原話："IEEPA refunds is less than $3 million"）
- 2026-07-31｜Paulo Sternadt｜margin：回應分析師澄清：IEEPA 退款精確數字為 280 萬美元（原話："$2.8 million, if you want to be precise."）
- 2026-07-31｜Paulo Sternadt｜margin：下半年關稅退款影響不重大且已含在指引內（原話："the impact of the tariffs for the second half is immaterial"）
- 2026-07-31｜David Foster｜commitment：CFO 重申 2030 年 32% 利潤率承諾（原話："we're still committed to our 32% margin by 2030."）
- 2026-07-31｜Paulo Sternadt｜commitment：CEO 表示對 2026 與 2030 承諾有信心（原話："delivering on our 2026 and 2030 commitments."）
- 2026-07-31｜Paulo Sternadt｜commitment：Americas 下半年利潤率將進一步改善（原話："will improve further in the second half of the year"）
- 2026-07-31｜Paulo Sternadt｜commitment：Boyd 達成全年 18 億預測的信心表述（原話："I will be shocked if they cannot overdeliver on"）
- 2026-07-31｜Paulo Sternadt｜commitment：Boyd 預計 2027 年併入有機成長計算（原話："looking forward to Boyd to join the organic growth in 2027."）
- 2026-07-31｜Paulo Sternadt｜commitment：CEO 稱將改善部分產品線的交期並擴充工程支援（原話："we know the product lines where our lead times are extended"）
- 2026-07-31｜Paulo Sternadt｜commitment：CEO 表示無人在慶功，團隊聚焦於達成承諾（原話："no one is taking a victory lap here"）
- 2026-07-31｜David Foster｜customer：Electrical Americas 資料中心有機成長約 65%（原話："data centers, up about 65%"）
- 2026-07-31｜David Foster｜customer：Americas 滾動 12 個月訂單成長 41%（創紀錄）（原話："record orders up 41% on a rolling 12-month basis"）
- 2026-07-31｜Paulo Sternadt｜customer：全公司訂單出貨比 1.2（原話："total company book-to-bill remains strong at 1.2"）
- 2026-07-31｜David Foster｜customer：電氣業務整體積壓訂單年增 43%（原話："total electrical business increased 43% over prior year."）
- 2026-07-31｜Paulo Sternadt｜customer：美國資料中心積壓達 307GW（15 年，前次為 12 年）（原話："Total U.S. data center backlog has grown to 307 gigawatts"）
- 2026-07-31｜Paulo Sternadt｜customer：該積壓僅約 20% 於近期轉化，多數為 2028 年後交付（原話："Only roughly 20% of this backlog converts near term."）
- 2026-07-31｜Paulo Sternadt｜customer：Electrical Global 資料中心營收成長 65%，高於底層市場 23%（原話："faster than the underlying market that is growing at 23%"）
- 2026-07-31｜Paulo Sternadt｜customer：Electrical Global 有機積壓訂單成長 54%（扣除 Boyd）（原話："organic backlog is up 54%"）
- 2026-07-31｜Paulo Sternadt｜customer：Electrical Global 指引由 7.5% 上調至 12% 的說明（原話："to raise our guidance from 7.5% to 12%"）
- 2026-07-31｜Paulo Sternadt｜customer：管理層稱每檔資料中心內容價值 340 萬美元/MW 為建模適用數字（原話："The $3.4 million is the right number to think about"）
- 2026-07-31｜Paulo Sternadt｜customer：資料中心連續 8 季成長超過 35%（原話："8 consecutive quarters of growth beyond 35% in data centers"）
- 2026-07-31｜Paulo Sternadt｜customer：2030 承諾模型僅假設資料中心成長 17%（原話："17% of the data center growth in our model."）
- 2026-07-31｜Paulo Sternadt｜competition：Boyd 在液冷（冷板與 CDU）為市場領導者（原話："they are the market leaders for liquid cooling"）
- 2026-07-31｜Paulo Sternadt｜competition：Boyd 為廣泛晶片供應商的設計夥伴（原話："design partner for broad-based chip providers."）
- 2026-07-31｜Paulo Sternadt｜competition：CEO 指部分競爭者出現品質問題（原話："some are actually showing some quality issues from the get-go"）
- 2026-07-31｜Paulo Sternadt｜competition：CEO 稱 Eaton 在固態變壓器技術上領先（原話："we are clearly ahead in terms of technology"）
- 2026-07-31｜Paulo Sternadt｜competition：CEO 認為 800V DC 轉型必然發生（原話："I believe this is going to happen"）
- 2026-07-31｜Paulo Sternadt｜competition：預製模組化解決方案的趨勢（缺工）（原話："So there is a push towards more modular solutions."）
- 2026-07-31｜Paulo Sternadt｜product：Boyd 帶來從電網到晶片的完整產品組合（原話："we have the full portfolio"）
- 2026-07-31｜Paulo Sternadt｜product：Boyd Q2 營收 4.32 億美元，高於其承諾與 Q2 指引 20%（原話："delivered $432 million in revenue"）
- 2026-07-31｜David Foster｜product：Ultra PCS 收購符合預期（原話："acquisition is performing to our expectations."）
- 2026-07-31｜David Foster｜product：Aerospace 需求強勁預期延續（原話："Aerospace continues to see strong demand now and into the"）
- 2026-07-31｜Paulo Sternadt｜capital_allocation：投資超過 10 億美元擴充產能（原話："investing more than $1 billion in capacity expansion"）
- 2026-07-31｜David Foster｜capital_allocation：CFO 稱各項收購均達到或超越成長與利潤率預期（原話："Each acquisition is at or above"）
- 2026-07-31｜Paulo Sternadt｜capital_allocation：以 Reverse Morris Trust 剝離移動出行（汽車）業務（原話："the tough call once again on the Reverse Morris Trust"）
- 2026-07-31｜Paulo Sternadt｜risk：產能爬坡的主要陣痛已在 Q4 與 Q1 發生（原話："most of the pain now is behind us, happened in Q4 and Q1"）
- 2026-07-31｜Paulo Sternadt｜risk：Q1→Q2 為模型中最大的單季產出爬坡，管理層稱已完成（原話："the largest quarterly ramp in production output"）
- 2026-07-31｜Paulo Sternadt｜risk：Americas 每日營收自 2025 年初累計成長約 25%（原話："roughly 25% growth in revenue per day"）
- 2026-07-31｜David Foster｜risk：Mobility 有機成長 -2%，管理層提及刻意退出低利潤業務（原話："Excluding the impact of the intentional exit"）

### 問答異常語氣（迴避／改口／保留）
- ETN_Q2_2026_Earnings_Call_20260731.md｜問：Andrew Obin（BofA）：Boyd 第三季與第四季的營收節奏（cadence）為何？｜答法：CEO 談 Boyd 的競爭優勢、Q2 超標與整合進度，未給 Q3／Q4 分季數字或節奏
- ETN_Q2_2026_Earnings_Call_20260731.md｜問：Jeffrey Sprague（Vertical）：指引隱含 Electrical Americas 營收 Q2→Q4 大致持平，但利潤率要靠價格與產出，是否過於保守？｜答法：CFO 回答以加班轉正常時間、溢價成本下降、生產力與價格為主，未直接回應營收持平的假設或是否保守
- ETN_Q2_2026_Earnings_Call_20260731.md｜問：Nicole DeBlase（Deutsche）：Electrical Global 隱含下半年有機成長減速，是否有需求提前或指引保守？｜答法：CEO 回以「很審慎」並列舉指引逐次上調的軌跡與「沒有下行」，未回答是否有拉貨提前，也未給下半年 EG 分季數字
- ETN_Q2_2026_Earnings_Call_20260731.md｜問：Jeff Hammond（KeyBanc）：交期改善後，何時能取得更多公平市占？目前長交期品項的交期狀況？｜答法：CEO 強調資料中心成長 65%、連續 8 季成長，並稱知道哪些產品線交期偏長，未提供交期天數或取回市占的時間點

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 4 | 2 |
| customer_second_source | found | 1 | 2 |
| customer_concentration_credit | found | 1 | 1 |
| supply_demand_durability | found | 5 | 2 |
| regulatory_antitrust | found | 2 | 3 |
| reg_tariff_export | found | 2 | 2 |
| geo_supply_chain | found | 2 | 3 |
| end_markets | found | 3 | 2 |
| substitute_technology | found | 3 | 1 |
| channel_business_model_shift | found | 3 | 2 |
| capital_markets_pricing | found | 5 | 4 |
| major_events | found | 4 | 4 |

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260905","verdict":"觀望","role":"追蹤","H":{"status":"unavailable"},"R":{"status":"unavailable"},"single_thing":null,"kill_metrics":null,"rearm_trigger":"股價 ≤$355（FY26E 13.55×26x 或 FY27E 16.07×22x），或 FY27 共識 EPS 上修 ≥10%（≥$17.7）且股價未同步上漲 → 重跑 DD、衛星首倉 1/3","irr_base_pct":8.9,"ev5y_pct":43.0,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"追蹤","signal":"B","val":"🔴","ma":"✅","trap":"🟡","moat_trend":"→","runway_post_y5":"🟡","asym_ratio":2.97,"ev5y_pct":43.0,"irr_base_pct":8.9,"max_dd_pct":-45,"bull_5y_price":887.6,"bear_5y_price":277.2,"p_bull_pct":25,"p_bear_pct":30,"rearm_trigger":"股價 ≤$355（FY26E 13.55×26x 或 FY27E 16.07×22x），或 FY27 共識 EPS 上修 ≥10%（≥$17.7）且股價未同步上漲 → 重跑 DD、衛星首倉 1/3","price_at_dd":410.85,"archetype":"品質複利成長","cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"ETN","date":"2026-11-08","schema":"v15.0","contract":"v19","company_name":"Eaton Corporation plc"},"oneliner":"第三季再上修，電氣訂單年增 43%，股價卻從 9 月的 410.85 美元跌到 341.72 美元；現價只要 EPS 年增約 12% 就有約 10% 年報酬，但現金轉換與 2028 年後資料中心需求仍未驗證。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ETN_20261108/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ETN_20261108/scenario.json","answers":{"q1_business":{"verdict":"Eaton 賺的是資料中心、電網與工商建築的配電與電力轉換設備錢，利潤卡在電氣美洲這一節：Q3 約 55% 的分部利潤來自這個分部。","reasoning":"Q3 營收 89.47 億美元，年增 28%，其中有機 19%、併購 8 個百分點；分部利潤率 25.3%。分部方面，電氣美洲營收 41.72 億美元、利潤率 29.8%；電氣全球約 27 億美元、21.1%；航太約 12 億美元、24.9%；Mobility 由總額反推約 8.75 億美元、17.2%，預計 2027 年第一季併入 Dana。四段營收乘利潤率合計約 22.6 億美元，與公布的 22.63 億美元相符，電氣美洲占約 55%。最新季毛利率事實表未涵蓋，TTM 毛利率 35.05%、營業利益率 17.32%。單點依賴：2023 至 2025 年沒有單一客戶超過淨銷售 10%，客戶集中度不是風險；但資料中心與商用航太合計約占三分之一營收，資料中心這一塊押的是同一條 AI 資本支出。366GW 是產業已公告案量，不是 Eaton 的訂單。產業態勢：競爭面有 Siemens 等進入固態變壓器，結構面訂單與在手訂單加速，其他結構變數是 800V 直流架構遷移，裁決為雙向拉鋸。","fact_refs":["f_kpi0_gaap","f_kpi1_segment_eaton_non_gaap","f_kpi2_eps_non_gaap","f_kpi4_backlog_book_to_bill","f_kpi5"],"verdict_values":{"revenue_quality":"訂單驅動的產品加專案型營收；電氣在手訂單逾 200 億美元、年增 46%，以 Q3 電氣營收約 68.7 億美元換算，能見度約三個季度。","unit_econ_note":"CEO 於 2026-07-31 法說稱資料中心內容價值約每 MW 340 萬美元；Q3 電氣美洲價格成本金額轉正，單位利潤回升。","archetype":{"primary":"品質複利成長","secondary":"循環/商品","confidence":"中","fingerprint":"多年訂單與利潤率上行，但約三分之一營收所在的強勢市場帶有資本支出週期性，且 2026 年成長含 8 個百分點併購。"},"industry":{"clock_phase":"II","sd_verdict_source":"結構性需求、週期性交付：訂單加速且大型變壓器交期仍長於 12 至 24 個月，屬擴張期；但新產能 2027 起陸續開出，2027 年規劃容量超過六成尚未開工，供給可逆性中等。來源為 2026-11-03 法說、Rystad 與 JPMorgan 轉述，依據不含股價。","bargaining":{"up":"銅等原物料與關稅成本靠價格傳導，Q3 價格成本金額轉正。","down":"超大型雲端與託管客戶逐案議價，CFO 稱 10 月與 2 家大客戶談定，第四季還有數家要談。","geo":"利潤主要在美洲；歐亞靠跟隨全球客戶與 COL、NordicEPOD 補產品。"},"profit_pool_dir":"利潤池往能提供完整電力鏈的供應商集中，但 5 年營業利益池占比事實表未涵蓋，方向僅為定性判斷。","tam_table":{"expanded":false,"reason":"事實表未涵蓋 TAM、SAM 與滲透率；可引用的只有美國資料中心已公告案量 366GW 對已裝機 50GW，屬管理層追蹤數，不是可服務市場。"}}}},"q2_moat":{"verdict":"護城河方向穩定：端到端電力鏈與供應確定性是真的，但份額與報酬差距都沒有獨立證據支持變寬。","reasoning":"機制是從變壓器、開關設備、斷路器到 UPS 自製，再加模組整合與液冷，客戶得到單一供應商、單一保固與較短交期；CEO 於 2026-11-03 舉 Fibrebond 由 3.75 億美元成長到 6 億美元為例。ROIC 差距事實表未涵蓋，改比利潤率：Eaton 的 TTM 毛利率、營業利益率與 FCF 利潤率接近台達電，三項都低於 Vertiv。份額只有管理層自述，第三方僅有五家合計 41% 至 43%，無 Eaton 單獨份額。執行力給 8 分，電氣美洲利潤率由 Q1 約 25.6% 回到 Q3 的 29.8%，但前一段擴產確實拖累過利潤率。定價力給 7 分，Q3 價格成本轉正、1 月 2 日再調價，但大客戶逐案談，交期緊張解除後才算真正測試。","fact_refs":["f_peer_etn_gross_margin_pct","f_peer_etn_operating_margin_pct","f_peer_etn_fcf_margin_pct","f_peer_vrt_gross_margin_pct","f_peer_vrt_operating_margin_pct","f_peer_vrt_fcf_margin_pct","f_peer_2308_tw_gross_margin_pct","f_peer_2308_tw_operating_margin_pct","f_peer_2308_tw_fcf_margin_pct","f_kpi1_segment_eaton_non_gaap"],"verdict_values":{"moat":{"mechanism":"自製關鍵電力設備加系統整合，形成單一供應商、認證與交期的轉換成本；液冷與直流產品把範圍延伸到晶片端。","execution":8,"pricing":7,"grade":"B","trend":"→","trend_evidence":"執行面穩定：電氣美洲利潤率逐季回升，但年比仍下滑，25 個擴產案完成 18 個後才剛轉成產出。定價面穩定：Q3 價格成本轉正，大客戶仍逐案議價。份額沒有第三方證據，所以不標擴大。","competitor_notes":[{"name":"VRT","strategy_note":"毛利率、營業利益率與 FCF 利潤率都高於 Eaton，是純資料中心標的中現金轉換最強的對手。"},{"name":"2308.TW","strategy_note":"毛利率與營業利益率幾乎相同，研發密度明顯較高，是電源端與直流架構的主要對手。"},{"name":"SU.PA","strategy_note":"事實表無財務資料，無法比較；仍是全球配電與資料中心電力的主要競爭者。"},{"name":"2301.TW","strategy_note":"利潤率低一個層級且 FCF 為負，不宜作為 Eaton 的定價對照。"}],"spread_notes":null,"peer_na_reason":"事實表未涵蓋各家投入資本，ROIC 差距無法計算，只能比利潤率。","threats":[{"level":"🟡","text":"固態變壓器與 800V 直流架構吸引 Siemens、Reinhausen、Sungrow 進入；Eaton 有 UL 認證先行與 10 個試點，屬單點競爭，但遷移時點公司也說無法掌握。","p":35,"evidence_refs":["substitute_technology#0","substitute_technology#1"]},{"level":"🟡","text":"新進入者與模組整合商爭奪預製電力市場，10-K 也承認漲價可能損及份額；事實表沒有具名搶單案例。","p":30,"evidence_refs":["competitive_share_entrants#1"]},{"level":"🟡","text":"斷路器與開關設備可能轉向供給過剩，交期優勢消失後定價力才會受到真正測試。","p":30,"evidence_refs":["supply_demand_durability#2"]}],"roic_durability":{"quadrant":"事實表未涵蓋投入資本，無法定象限；利益率面屬中高。","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"電力設備是剛需，管理層預期 2027 年沒有終端市場衰退；但資料中心的急迫性不等於持久性，2027 年規劃容量超過六成尚未開工。"},{"item":"決策層級","level":"🟡","text":"決策單位是整條電力鏈，單一保固與認證有黏性；但大客戶可在多家合格供應商間選擇，目前靠交期與供應確定性撐住，漲價後流失率事實表未涵蓋。"},{"item":"價值鏈分配","level":"🟡","text":"Eaton 每 MW 約 340 萬美元內容價值有議價基礎，且無單一客戶超過 10%；但架構由晶片與雲端業者決定，大客戶逐案議價，Vertiv 的現金轉換也較好。"},{"item":"社會容忍度","level":"🟢","text":"客戶是企業與公用事業，尚無社會價格上限的跡象；10-Q 列有反壟斷與貿易管制事項，金額事實表未涵蓋，已列入風險監測。"}],"roiic":"資料缺口：事實表沒有投入資本。僅能做假設性推算，若 Boyd 利潤率接近公司 Q3 分部利潤率 25.3%，FY27 營收 27 億美元對 95.5 億美元收購價的稅前報酬約 7.2%，Boyd 實際利潤率未揭露。","reinvest_rate":"資料缺口：折舊、營運資金與稅率事實表未涵蓋。FY26 僅 Boyd 一筆約 95.5 億美元，約為 FY2025 淨利 40.87 億美元的 2.3 倍，屬一次性高峰。","endo_ceiling":null,"formula_note":"內生成長率應為增量 ROIC 乘再投資率；兩項輸入都缺，所以不給數字。"}}}},"q3_growth":{"verdict":"五年後跑道中等：需求案量充足，但看得到的第二條曲線仍押同一個資料中心資本支出。","reasoning":"共識三年 EPS 年複合約 16.2%：FY2025 調整後 EPS 由指引中點 13.75 美元與管理層所稱年增 14% 反推約 12.06 美元，到 FY28E 18.94 美元。FY27 共識營收年增 11.1%，EPS 年增 19.1%，差 8.0 個百分點，主要靠利潤率與併購綜效。Mobility 出表後，FY27 同範圍營收需年增約 21%，算式為（37,420－800）÷（33,685－3,500）－1，其中 3,500 是 Q3 Mobility 約 875 百萬美元的四倍；這高於管理層終端市場至少 11% 的框架，是我的 Base 低於共識的原因。缺口歸因為利潤率擴張與併購，內生上界無法計算，長期信心上限為中。公司正式的 2026 至 2030 年有機目標仍是 6% 至 9%。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_kpi4_backlog_book_to_bill","f_kpi5"],"verdict_values":{"growth":{"driver_mix":"量為主、價次之，併購墊高 2026 年約 8 個百分點，回購貢獻小。","runway_years":"事實表未涵蓋滲透率，無法換算","runway_post_y5":"🟡","endo_ceiling_basis":"投入資本、折舊、營運資金與稅率事實表都未涵蓋，內生上界無法推導；無法證明共識成長落在上界內，情境樹保守視為超過。","segments":[{"item":"電氣美洲","value":"Q3 營收 41.72 億美元、有機 +22%、利潤率 29.8%、資料中心 +54%、滾動訂單 +39%"},{"item":"電氣全球","value":"Q3 營收約 27 億美元、總成長 +58%、有機 +27%、利潤率 21.1%、滾動訂單 +51%"},{"item":"航太","value":"Q3 營收約 12 億美元、有機 +6%、利潤率 24.9%、在手訂單 56 億美元"},{"item":"Mobility","value":"Q3 營收反推約 8.75 億美元、有機 +9%、利潤率 17.2%，FY27 僅貢獻約 8 億美元"}],"decay_signals":[{"name":"毛利率連 2 季年減","lit":true,"note":"TTM 毛利率 35.05%，低於 FY2025 的 37.59%；季度年比事實表未涵蓋，以 TTM 代理。"},{"name":"EPS 成長顯著高於營收成長","lit":true,"note":"FY2022 至 FY2025 GAAP EPS 年複合 19.4%，營收 9.8%，差 9.6 個百分點。"},{"name":"FCF／淨利低於 0.75 連 2 年","lit":false,"note":"FY2024 為 0.93，FY2025 為 0.87。"},{"name":"核心市占、SBC 占比、維護性資本支出、產業倍數下移","lit":null,"note":"事實表未涵蓋。"}],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"資本配置能驗證的只有股數紀律，大型併購的報酬還要等 Boyd 的利潤數字。","reasoning":"FY2025 FCF／淨利 0.87（35.53 億÷40.87 億美元），FY2024 為 0.93，Q3 FCF 10.34 億美元。SBC 占營收、現金去向四分、債務到期與加權利率事實表未涵蓋。併購累計投入約 140 億美元，淨負債 201.04 億美元，約為 TTM 營業利益 55 億美元的 3.6 倍。CEO 於 2026-11-03 表明未來 12 個月不做 Boyd 規模併購，接下來以整合為優先。由淨利÷稀釋 EPS 推得股數，2022 年約 4.01 億股、2025 年約 3.91 億股，年減約 0.8%。","fact_refs":["f_kpi3_fcf","f_net_debt_m","f_shares_diluted_m","f_dividend_yield_ttm"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":true,"passed":null,"input":"Boyd 與其他併購的實際利潤與投入資本事實表未涵蓋；管理層稱各案達到或超過預期，但屬自述。"},{"name":"buyback_yield","applicable":true,"passed":null,"input":"回購均價與 10 年期殖利率事實表未涵蓋。"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"推得稀釋股數 2022 年約 4.01 億、2025 年約 3.91 億，年減約 0.8%，沒有淨稀釋。"}]},"governance":{"capital_returns":[{"item":"累計併購","value":"約 140 億美元（2026-11-03 法說）"},{"item":"Boyd Thermal","value":"約 95.5 億美元，2026-03-12 交割；FY26 營收指引 19 億美元，FY27 至少 27 億美元"},{"item":"COL Group","value":"8.1 億歐元，2026-09-25 同意收購"},{"item":"Mobility 分拆","value":"與 Dana 進行 Reverse Morris Trust，Eaton 股東持 50.1%，另收約 11 億美元現金，預計 2027 年第一季完成"},{"item":"股息","value":"TTM 殖利率約 0.97%"}]}}},"q5_valuation":{"verdict":"現價只要求 EPS 年複合約 12% 搭配 22 倍退出，就有約 10% 年報酬；這接近公司自訂下限，我信得過，但不算便宜。","reasoning":"反推：10% 總報酬扣約 1% 股息，股價年增 9%，五年後約 526 美元，除以 22 倍需 FY31 EPS 23.9 美元，由 13.67 美元起算年複合 11.8%。Base 年報酬約 12%，來自 EPS 複利約 12.8%、倍數收縮約 −1.7%、股息約 1%，報酬不靠重估。成長熄火壓力測試：FY28 後成長降到 15%、10%、5%，搭配 25、20、15 倍，FY31 股價約 703、492、321 美元，三種情境兩種高於現價。賣方平均目標價 431.88 至 485.47 美元，現價低於這些均值 21% 至 30%，但多數早於這波下跌；UBS 的 360 美元是較新的反方看法。全距約 1.35 倍，未到需要因分歧調降信心的程度。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_pe_current","f_pe_percentile","f_ps_current","f_ps_percentile","f_ev_s_current","f_ev_s_percentile","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_3m_fy1_pct","f_net_debt_m","f_ev_m"],"verdict_values":{"valuation":{"basis":"FY26 前瞻本益比（調整後 EPS 13.67 美元），並以 GAAP 本益比與 FCF 殖利率對照。","tier":"電力設備與資料中心基礎設施","peers":{"expanded":false,"reason":"事實表未涵蓋同業倍數，只有同業利潤率，無法做同層級對照。"},"fwd_pe":25.0,"peg":1.54,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"FY26 前瞻 25.0 倍、FY27 21.0 倍，PEG 1.54（25.0÷16.2）落在合理帶；但 GAAP 本益比 34.14 倍，FCF 殖利率約 2.9%（TTM FCF 約 38 億÷市值 1,328 億美元），所以結論是合理而非便宜。5 年分位事實表只有 4 個年度端點，無法計算，留空。上行空間：12 個月以 FY27 Base 16.0×24 倍＝384 美元；24 個月以 FY28 Base 18.5×23 倍＝425.5 美元。","upside_short_pct":12.4,"upside_mid_pct":24.5,"denominator_disputed":true,"denominator_note":"FY26 調整後與 GAAP EPS 指引相差 3.31 美元，占調整後 EPS 的 24%，FY2025 差約 1.61 美元，差距在 Boyd 後擴大。另外 FY27 共識是否完整扣除 Mobility 出表，事實表無法驗證。兩者都使 25 倍不能當成便宜的論據。"}}},"q6_how_wrong":{"verdict":"最可能看錯的地方，是把 2028 年前已排定的需求當成 2028 年後也存在。","reasoning":"最大回撤與空方論證放在情境樹與反證紀錄。週線目前低於 52 週與 104 週均線，RSI 36.99，26 週報酬 −14.68%，代表市場不認同連續上修；我把這視為未解的反方訊號，所以分批且不追價。亮燈的衰退信號有兩項，毛利率下滑與 EPS 成長高於營收，屬中等陷阱風險。歷史最大回撤與法律案件金額事實表未涵蓋。","fact_refs":["f_week26_return_pct","f_rsi14","f_ma_state","f_ma_w52","f_ma_w104","f_ma_w250","f_net_debt_m","f_kpi4_backlog_book_to_bill"],"verdict_values":{"trap":{"verdict":"🟡","label":"成長靠利潤率與併購放大，尚未到陷阱"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":13.67,"pe":25.0,"basis":"FY1（FY2026E）共識調整後 EPS 與判斷日股價 341.72 美元，終端倍數同為當年度 EPS 口徑。"},"eps":{"bull":[17.0,20.5,24.5,28.8,33.0],"base":[16.0,18.5,20.9,23.0,25.0],"bear":[15.4,16.4,14.8,15.2,16.2]},"pe":{"bull":26,"base":23,"bear":16},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0.97,"net_buyback":0},"second_stage":{"bull_cagr_pct":12,"base_cagr_pct":8},"max_dd":{"lo":-45,"hi":-30,"basis":"Bear 低點 FY29 EPS 14.8 美元乘 14 至 17 倍，得 207 至 252 美元，相對現價 −39% 至 −26%；淨負債 201 億美元會放大情緒，所以下緣放寬到 −45%，上緣取 −30%。歷史最大回撤事實表未涵蓋。","trigger_time":null},"basis":{"bull":"資料中心續強、Boyd 併入有機、固態變壓器 2028 年放量、2030 年 32% 利潤率承諾兌現；EPS 年複合 19.3%，終端 26 倍略高於現值 25.0 倍。","base":"FY27 略低於共識以反映 Mobility 出表，之後 EPS 年增由 17% 逐步降到 9%，五年年複合 12.8%，略高於管理層每年 12% 的下限；終端 23 倍低於自身現值 25.0 倍，同業倍數事實表未涵蓋；回購效果已含在 EPS 路徑，淨回購殖利率填 0 以免重複。","bear":"FY27 由在手訂單撐住，2028 年後資料中心資本支出消化、新廠產能過剩，FY29 EPS 回落到 14.8 美元，FY31 僅回到 16.2 美元；16 倍取成長熄火至 5% 的 15 倍與至 10% 的 20 倍之間、靠近下緣。Bear 機率 30% 依據為內生上界無法證明、資料中心開工延遲與單一需求來源。"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"JPMorgan 經 Nasdaq 引述，2027 年規劃資料中心容量超過六成尚未開工；電氣美洲資料中心營收成長由 Q2 約 65% 降到 Q3 的 54%，電氣美洲在手訂單成長由 Q1 的 44% 降到 33%。","assumption":"366GW 已公告案量能如期轉成 Eaton 訂單；CEO 於 2026-07-31 表示只有約 20% 近期轉換。","consequence":"五年後虧 50% 最可能的路徑：2028 年資本支出消化，新廠同時開出，EPS 跌回 13 美元以下、本益比 13 倍，股價約 170 美元。","ruling":"部分採納：Bear 機率給 30%，與唯一致命事件同一條路徑；不採納到 Base，因為 Q3 滾動 12 個月資料中心訂單仍 +101%，非資料中心訂單也在增加。","watch":"資料中心滾動 12 個月訂單、電氣 book-to-bill、2027 年初雲端資本支出指引。","evidence_refs":["supply_demand_durability#3"],"fact_refs":["f_kpi4_backlog_book_to_bill"]},{"view":"論點成功但股東經濟變差","evidence":"FY26 GAAP 與調整後 EPS 差距 3.31 美元，FY2025 約 1.61 美元；Eaton 的 TTM FCF 利潤率 11.87%，Vertiv 為 23.74%；CFO 稱大客戶逐案議價。","assumption":"需求成真時，利潤會留在 Eaton，而不是流向大客戶或被併購溢價吃掉。","consequence":"營收達標但每股 FCF 成長落後調整後 EPS，終端倍數應往 Base 下緣走。","ruling":"採納：結論不給便宜，併購報酬項不計通過；FCF／GAAP 淨利連 2 年低於 0.75 就減碼。","watch":"FCF／GAAP 淨利、Boyd 利潤率揭露、大客戶合約的原物料調整條款。","evidence_refs":["competitive_share_entrants#1","substitute_technology#0"],"fact_refs":["f_peer_etn_fcf_margin_pct","f_peer_vrt_fcf_margin_pct","f_kpi5"]},{"view":"價格已反映太多","evidence":"UBS 降評至中立，目標價由 440 降到 360 美元，僅比現價高約 5%，理由是估值偏高與近期盈餘上行有限，發布日未載明；GAAP 本益比 34.14 倍，FCF 殖利率約 2.9%。","assumption":"調整後 25.0 倍是合適的定價口徑。","consequence":"若市場改看 GAAP 或 FCF，合理的結論不成立，倍數可能再壓縮。","ruling":"部分反駁：股價自前份已跌約 17%，FY27 前瞻 21.0 倍，Base 假設倍數降到 23 倍，報酬不靠重估；但質疑保留，所以首批上限為目標部位 1/3。","watch":"2027 年 2 月指引是否使 FY27 共識 16.28 美元下修。","evidence_refs":["capital_markets_pricing#4"],"fact_refs":["f_pe_current","f_fwd_pe_latest"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟠","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟠","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 410.85 → 本次 341.72（-16.8%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=410.85","side_b":"本次 price_at_dd=341.72","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 410.85 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 410.85 美元：Bull 價 887.6、Bear 價 277.2，五年期望值 +43.0%，基準年化 8.9%，不對稱比 2.97","side_b":"本次情境、股價仍用 410.85 美元：Bull 價 858、Bear 價 259.2，五年期望值 +34.1%，基準年化 7.0%，不對稱比 2.46","ruling":"先換情境、股價不動：五年期望值少 8.9 個百分點，基準年化少 1.9 個百分點。不對稱比由 2.97 變為 2.46。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 410.85 美元：五年期望值 +34.1%，基準年化 7.0%，不對稱比 2.46","side_b":"本次情境、股價 341.72 美元：五年期望值 +61.2%，基準年化 11.0%，不對稱比 5.21","ruling":"再換股價、情境不動：起點價下跌 16.8%，五年期望值多 27.1 個百分點，基準年化多 4.0 個百分點，不對稱比由 2.46 升到 5.21。合計五年期望值比前份多 18.2 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"估值與機率（股價下跌）","cause":"價格變動","prior_field":["val","p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份 2026-09-05 股價 410.85 美元，估值偏貴、觀望，Bull／Bear 機率 25／30，最大回撤 −45%。","side_b":"本次股價 341.72 美元，FY26 前瞻 25.0 倍、FY27 21.0 倍，估值改判合理；機率與回撤下緣維持。","ruling":"變動主因是股價下跌約 17%，共識近 3 個月只上修 1.18%，不是基本面翻新；機率不因股價下跌而放寬。","evidence_level":"高：股價與共識皆有快照","settle_metric":"FY27 首次指引中點","if_then":["若股價續跌但 FY27 指引中點 ≥15.5 美元，分批反買","若股價先漲回 410 美元以上而指引未出，不追"],"evidence_refs":[]},{"axis":"基本面判斷維持","cause":"新證據","prior_field":["signal","trap","moat_trend","runway_post_y5"],"side_a":"前份訊號等級 B、陷阱風險中等、護城河方向穩定、五年後跑道中等。","side_b":"本次四項維持。Q3 訂單與利潤率轉強，但固態變壓器對手進入，TTM 毛利率下滑。","ruling":"新證據正負相抵，不足以改判；跑道不上調，因為液冷與固態變壓器仍押同一個資料中心資本支出；護城河不上調，因為份額只有管理層自述。","evidence_level":"中：訂單與利潤率為官方數字，份額無第三方","settle_metric":"第三方份額資料與固態變壓器量產訂單","if_then":["若 2027 年底前揭露固態變壓器量產訂單且資料中心以外訂單維持 ≥20%，跑道上調並加碼第二批","若份額證據轉負，停止加碼"],"evidence_refs":["substitute_technology#1"]},{"axis":"公司分類","cause":"方法變動","prior_field":["archetype","cycle_position"],"side_a":"前份分類為品質複利成長，未標循環位置。","side_b":"本次主分類不變，循環位置仍不標，第二分類標循環商品。","ruling":"判斷方法未改主分類；資料中心的週期性放在 Bear 機率 30% 與第二分類處理。","evidence_level":"中","settle_metric":"資料中心訂單是否出現負成長","if_then":["若資料中心訂單轉為年減，改用循環股框架並減碼 1/3"],"evidence_refs":[]},{"axis":"進場條件（加碼門檻變更，前份條件已發動）","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"股價 ≤$355（FY26E 13.55×26x 或 FY27E 16.07×22x），或 FY27 共識 EPS 上修 ≥10%（≥$17.7）且股價未同步上漲 → 重跑 DD、衛星首倉 1/3","side_b":"第二批加碼須 FY27 首次指引 EPS 中點 ≥$15.5 且電氣滾動 12 個月訂單年增 ≥25%；股價 ≤$300 且基本面未破則分批反買。","ruling":"前份股價條件已於 2026-11-06 收盤發動（341.72 美元低於 355 美元），另一個共識條件未發動；所以本次改寫下一批的條件，改由基本面資料點決定。","evidence_level":"高：收盤價可驗證","settle_metric":"2027 年 2 月 FY27 指引","if_then":["若兩項條件都達到，加碼第二批 1/3","若 FY27 指引中點低於 14.8 美元，減碼 1/3"],"evidence_refs":[]},{"axis":"Single Thing 建立","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份摘要此欄為空，沒有前份唯一致命點原文。","side_b":"超大型雲端資本支出進入消化期，使電氣滾動 12 個月 book-to-bill 連 2 季跌破 1.0。","ruling":"Single Thing 選情境樹最大敏感度，而不是最戲劇性的技術替代事件；發生即清倉。","evidence_level":"中","settle_metric":"電氣滾動 12 個月 book-to-bill","if_then":["若連 2 季低於 1.0，清倉","若維持 ≥1.1，不動作"],"evidence_refs":[]},{"axis":"監控指標建立（清倉與減碼門檻）","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份摘要此欄為空，沒有前份門檻原文。","side_b":"book-to-bill 低於 1.0 連 2 季清倉；資料中心滾動訂單低於 30% 連 2 季減碼；電氣美洲 FY27 利潤率低於 29% 減碼；FCF／GAAP 淨利連 2 年低於 0.75 減碼。","ruling":"改用每季可驗證的官方數字作為清倉與減碼依據。","evidence_level":"高：皆為公司季報揭露項目","settle_metric":"每季新聞稿與法說","if_then":["任一減碼門檻觸發，減碼 1/3","單一致命門檻觸發，清倉"],"evidence_refs":[]},{"axis":"管理層承諾對帳：電氣美洲利潤率","cause":"新證據","side_a":"2026-07-31 法說 CFO：Q2 到 Q3 改善 250bp，Q3 到 Q4 再改善 200 至 250bp，年比下滑歸因於暫時性負價格成本。","side_b":"2026-11-03 法說：Q3 實際 +230bp 到 29.8%，略低於路徑；CEO 提醒不要把 Q4 乘以 4；年比下滑改稱暫時性原物料。","ruling":"屬程度差異，可調和；暫時性歸因標為未證、監測。Q2 路徑隱含 Q4 約 31.8% 至 32.3%，門檻留緩衝設在 31%。","evidence_level":"高：同一管理層前後兩場法說","settle_metric":"Q4 電氣美洲利潤率","if_then":["若 Q4 <31%，停止加碼","若到 2027 年第二季利潤率年比仍下滑，暫時性歸因證偽並減碼 1/3"],"evidence_refs":[]},{"axis":"資料中心需求持久性","cause":"新證據","side_a":"CEO 2026-11-03：已公告案量由 307GW 增至 366GW，滾動訂單 +101%，跑道延伸到 2028、2029 年以後。","side_b":"JPMorgan 轉述 2027 年規劃容量超過六成未開工；另有摘要稱資料中心訂單成長由 Q1 的 240% 降到 Q2 的 85%，口徑與 Q3 的 +101% 不一定相同，來源品質混雜。","ruling":"可調和：案量不是訂單，開工延遲影響時點，尚未看到訂單反轉；證據時間窗只到 2027 年，不能宣稱 2028 年後風險已解。","evidence_level":"中：官方訂單對照轉述資料","settle_metric":"資料中心滾動 12 個月訂單年增與電氣 book-to-bill","if_then":["若資料中心訂單連 2 季低於 30%，減碼 1/3","若股價先跌但訂單維持，分批反買"],"evidence_refs":["supply_demand_durability#3","supply_demand_durability#2"]},{"axis":"上修但現金與 GAAP 未跟上","cause":"新證據","side_a":"全年調整後 EPS 中點上修 0.25 美元到 13.75 美元，第三次上修。","side_b":"全年分部利潤率 24.1% 至 24.5% 不動，現金流預期只重申；GAAP EPS 僅 10.39 至 10.49 美元。","ruling":"可調和：上修來自銷量與 Q3 超標，併購攤提壓低 GAAP；但在 FCF 跟上前，不用調整後 EPS 主張便宜。","evidence_level":"高：官方指引","settle_metric":"FY26 全年 FCF 與 FY27 現金流指引","if_then":["若 FY27 FCF／GAAP 淨利低於 0.75，停止加碼","若連 2 年低於 0.75，減碼 1/3"],"evidence_refs":[]},{"axis":"份額：管理層自述對第三方","cause":"新證據","side_a":"CEO 稱在歐洲與亞洲持續贏得份額；2026-07-31 法說稱電氣全球資料中心營收 +65%、底層市場 +23%。","side_b":"第三方只有五家合計 41% 至 43%，沒有 Eaton 單獨份額與消長；Vertiv 利潤率與現金轉換都更高。","ruling":"管理層證據支持方向但不足以上調護城河，判斷維持穩定。","evidence_level":"低：單一來源自述","settle_metric":"第三方份額報告或大客戶揭露","if_then":["若第三方資料顯示 Eaton 份額下降，停止加碼"],"evidence_refs":[]},{"axis":"現在就賣的最強論證","cause":"新證據","side_a":"連續三次上修、訂單創高，EPS 只需約 12% 年複合即有約 10% 年報酬。","side_b":"好消息之下股價仍跌，代表市場在折現 2028 年後的斷層；現金流預期未上修，調整項擴大到 3.31 美元，FCF 殖利率約 2.9%，週線低於 52 週與 104 週均線，UBS 目標價僅高於現價約 5%。","ruling":"不採納不進場，但採納不一次滿倉：首批上限為目標部位 1/3，其餘等基本面資料點。若賣方論點成立，第一個可見證據會是 FY27 指引或訂單轉弱。","evidence_level":"中","settle_metric":"FY27 指引與電氣訂單","if_then":["若 FY27 指引中點低於 14.8 美元，減碼 1/3","若指引 ≥15.5 美元且訂單 ≥25%，加碼第二批 1/3","若股價反彈但兩項資料未出，不追"],"evidence_refs":["capital_markets_pricing#4"]}],"triggers":[{"n":1,"text":"FY27 首次指引達標且電氣訂單未轉弱，加碼第二批。","type":"加碼","maps_to":"H1","metric":"FY27 調整後 EPS 指引中點；電氣滾動 12 個月訂單年增","threshold":"≥15.5 美元且 ≥25%","action":"加碼第二批 1/3","source_freq":"第四季新聞稿，年度一次","date":"2027-02"},{"n":2,"text":"第四季電氣美洲利潤率驗證擴產已轉為獲利。","type":"假設驗證","maps_to":"H2","metric":"電氣美洲第四季分部利潤率","threshold":"≥31%","action":"未達則停止加碼","source_freq":"季報","date":"2027-02"},{"n":3,"text":"資料中心訂單成長明顯降溫。","type":"風險","maps_to":"R1","metric":"資料中心滾動 12 個月訂單年增","threshold":"連 2 季 <30%","action":"減碼 1/3","source_freq":"法說，季更","date":null,"evidence_refs":["supply_demand_durability#3"]},{"n":4,"text":"電氣訂單低於出貨，需求反轉成立。","type":"Single Thing","maps_to":"Single Thing","metric":"電氣滾動 12 個月 book-to-bill","threshold":"連 2 季 <1.0","action":"清倉","source_freq":"季報","date":null},{"n":5,"text":"股價大跌但基本面未破時分批反買。","type":"估值rearm","maps_to":"H1","metric":"收盤價；H1 門檻是否仍成立","threshold":"≤300 美元（約 FY27 Base 18.75 倍）且 book-to-bill ≥1.1","action":"分批反買第三批 1/3","source_freq":"日收盤與季報","date":null},{"n":6,"text":"關稅或原物料吸收失敗。","type":"減碼","maps_to":"R3","metric":"電氣美洲價格成本與環比利潤率","threshold":"價格成本連 2 季轉負且利潤率環比下滑","action":"減碼 1/3","source_freq":"法說，季更","date":null,"evidence_refs":["reg_tariff_export#0"]},{"n":7,"text":"新產能開出後開關設備供給轉鬆。","type":"風險","maps_to":"R2","metric":"電氣美洲在手訂單年增與利潤率年變動","threshold":"在手訂單連 2 季 <10% 且利潤率年減 ≥100bp","action":"停止加碼","source_freq":"季報","date":null,"evidence_refs":["supply_demand_durability#2","competitive_share_entrants#1"]},{"n":8,"text":"固態變壓器未能由試點轉量產。","type":"風險","maps_to":"R4","metric":"量產訂單揭露與對手具名大案","threshold":"2027 年底前未揭露量產訂單，且對手取得具名大案","action":"減碼 1/3","source_freq":"法說，季更","date":"2027-12-31","evidence_refs":["substitute_technology#0","substitute_technology#1"]},{"n":9,"text":"反壟斷或貿易管制事項出現金額。","type":"風險","maps_to":"R5","metric":"10-Q 應計或揭露金額；程序性質","threshold":"≥1.9 億美元（TTM FCF 約 5%），或進入刑事程序","action":"達金額門檻減碼 1/3；刑事介入清倉","source_freq":"10-Q，季更","date":null,"evidence_refs":["regulatory_antitrust#1"]},{"n":10,"text":"Boyd 未達管理層 FY27 下限。","type":"風險","maps_to":"R6","metric":"Boyd FY27 營收","threshold":"<27 億美元","action":"停止加碼","source_freq":"法說，季更","date":"2028-02"},{"n":11,"text":"第四季財報與 FY27 指引後複審。","type":"複審日期","maps_to":"H1","metric":"指引、訂單、現金流","threshold":"財報公布後一週內完成","action":"依前述門檻執行","source_freq":"一次性","date":"2027-02"}],"kill_metrics":[{"metric":"電氣滾動 12 個月 book-to-bill","bear_threshold":"<1.0（現值 1.2）","window":"連 2 季","source":"Eaton 季度新聞稿","last_status":"ok"},{"metric":"資料中心滾動 12 個月訂單年增","bear_threshold":"<30%（現值 101%）","window":"連 2 季","source":"Eaton 法說","last_status":"ok"},{"metric":"電氣美洲全年利潤率","bear_threshold":"FY27 <29%（Q3 為 29.8%）","window":"FY27 全年","source":"Eaton 季度新聞稿","last_status":"unknown"},{"metric":"FCF／GAAP 淨利","bear_threshold":"<0.75（FY2025 為 0.87）","window":"連 2 個年度","source":"年報現金流量表","last_status":"ok"},{"metric":"固態變壓器量產訂單","bear_threshold":"未揭露量產訂單","window":"至 2027-12-31","source":"Eaton 法說","last_status":"unknown"}],"evidence_dismissed":[{"ref":"geo_supply_chain#0","reason":"證據本身是一般性風險揭露，原文未列特定國家、金額或已發生事件，無法形成可驗證門檻；關稅的損益影響已另列為風險。"},{"ref":"major_events#3","reason":"證據僅為約 289 輛車用差速器召回，沒有金額，也與電氣及航太論點無關，且與另一筆召回紀錄是同一通報。"},{"ref":"product_recall_warning#0","reason":"與前一筆是同一 NHTSA 通報的重複收錄，規模約 289 輛，來源未提供財務影響。"}],"action_conditions":{"rearm_trigger":"第二批須 FY27 首次指引 EPS 中點 ≥$15.5 且電氣滾動 12 個月訂單年增 ≥25%；股價 ≤$300 且基本面未破則分批反買","exec_line":"前份股價條件已發動，首批上限為目標部位 1/3；週線仍低於 52 週與 104 週均線，加碼一律等基本面資料點，反彈不追價。"}},"decision_inputs":{"signal":"B","ma":"🟠","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場在定價 2028 年後的資料中心斷層，但最新一季滾動訂單仍 +101%，資料中心以外的公用事業、住宅與機械 OEM 訂單也在成長；現價只要求約 12% 的 EPS 年複合成長，尚無實證支持需求反轉。","momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":false,"wait_for_price":null,"wait_for_price_condition":null},"thesis":{"H":[{"id":"H1","text":"在手訂單與新產能轉換支撐 FY27 調整後 EPS 約 16 美元、FY28 約 18.5 美元。","2y":"FY27 ≥15.5 美元，FY28 ≥17.5 美元","5y":null,"10y":null,"threshold":"FY27 首次指引中點 ≥15.5 美元；電氣滾動 12 個月 book-to-bill ≥1.1","source":"Eaton 季度新聞稿與法說，季更；2027 年 2 月首次給 FY27 指引","drift_rule":"TTM 調整後 EPS 連 2 季低於路徑 5% 為削弱，連 3 季低於路徑 10% 為反轉"},{"id":"H2","text":"電氣美洲利潤率兌現 2030 年 32% 承諾，新廠投產不再拖累；2026-07-31 法說摘錄未明講分部，按上下文解讀為電氣美洲。","2y":null,"5y":"2030 年 ≥32%","10y":null,"threshold":"FY27 全年 ≥30%，2030 年 ≥32%","source":"Eaton 季度新聞稿分部利潤率，季更","drift_rule":"TTM 利潤率連 4 季低於路徑 5% 為削弱，連 6 季低於路徑 10% 為反轉"},{"id":"H3","text":"800V 直流遷移後，Eaton 每 MW 內容價值不低於現行約 340 萬美元，固態變壓器由試點轉量產。","2y":null,"5y":null,"10y":"2036 年前直流架構下內容價值與份額不低於交流時代","threshold":"2027 年底前揭露量產訂單；每 MW 內容價值 ≥340 萬美元","source":"法說與投資人日，半年更；第三方份額事實表未涵蓋","drift_rule":"跨 2 個年度未達為削弱，跨 3 個年度未達為反轉"}],"R":[{"id":"R1","text":"資料中心開工延遲或資本支出消化，訂單成長快速降溫。","h_ref":"H1","clock":"🔥","threshold":"資料中心滾動訂單連 2 季 <30%","evidence_refs":["supply_demand_durability#3"]},{"id":"R2","text":"開關設備與斷路器供給轉鬆，多座新廠同時開出，新進入者壓低定價。","h_ref":"H2","clock":"🔥","threshold":"電氣美洲在手訂單連 2 季 <10% 且利潤率年減 ≥100bp","evidence_refs":["supply_demand_durability#2","competitive_share_entrants#1"]},{"id":"R3","text":"關稅與原物料成本再度超過價格傳導。","h_ref":"H2","clock":"⚡","threshold":"價格成本連 2 季轉負且電氣美洲利潤率環比下滑","evidence_refs":["reg_tariff_export#0"]},{"id":"R4","text":"800V 直流架構加速，對手在固態變壓器取得大案，現有交流設備內容價值縮水。","h_ref":"H3","clock":"🐢","threshold":"2027 年底前未揭露量產訂單且對手取得具名大案","evidence_refs":["substitute_technology#0","substitute_technology#1"]},{"id":"R5","text":"10-Q 列示的反壟斷與貿易管制事項惡化；受影響營收與和解時程事實表未涵蓋。","h_ref":"H1","clock":"🐢","threshold":"揭露應計或金額 ≥1.9 億美元，或進入刑事程序","evidence_refs":["regulatory_antitrust#1"]},{"id":"R6","text":"Boyd 約 95.5 億美元併購占市值逾 5%，整合或增長不如預期，高槓桿下壓縮資本彈性；Mobility 出表也增加 FY27 比較難度。","h_ref":"H1","clock":"🔥","threshold":"Boyd FY27 營收 <27 億美元","evidence_refs":["major_events#0","ma_merger#0"]}],"single_thing":{"description":"超大型雲端資本支出進入消化期，使電氣滾動 12 個月 book-to-bill 連 2 季跌破 1.0。","why_fatal":"這是情境樹最大的敏感度：Base 與 Bear 的 FY31 EPS 差 35%（25.0 對 16.2 美元），倍數再差 30%（23 對 16 倍），終端股價差 55%（575 對 259 美元）。","if_happens":"清倉，等訂單連 2 季回升後重新研究。","how_monitor":"每季新聞稿的滾動 12 個月訂單與 book-to-bill，法說的資料中心訂單與談判管線。","probability":"未來 12 至 24 個月約 20%；FY27 訂單有在手訂單與 11% 終端市場框架支撐，但 2027 年規劃容量超過六成尚未開工。"}},"appendix_a":{"growth_durability":7,"quality_score":7.5,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":20.99,"peg_fy2":1.3,"stress":{"pass":2,"total":3}},"eps_meta":{"base_eps_path":{"FY2025A":12.06,"FY2026E":13.67,"FY2027E":16.28,"FY2028E":18.94},"fy_end_month":12,"eps_basis":"調整後 EPS（Non-GAAP），Koyfin 2026-11-07 快照，分析師家數事實表未涵蓋；FY2025A 由 FY26 指引中點 13.75 美元與管理層所稱年增 14% 反推，FY1 共識 13.67 美元略低於指引下緣 13.70 美元。"},"catalysts":[{"date":"2027-02","date_precision":"month","type":"guidance","event":"第四季財報與 FY27 首次完整指引","impact":"高","watch":"EPS 中點是否 ≥15.5 美元、Mobility 出表口徑、現金流指引"},{"date":"2027-Q1","date_precision":"quarter","type":"other","event":"Mobility 與 Dana 的 Reverse Morris Trust 預計完成","impact":"中","watch":"實收現金約 11 億美元與 FY27 EPS 稀釋幅度"},{"date":"2027-03","date_precision":"month","type":"other","event":"Boyd 開始計入有機成長","impact":"中","watch":"Boyd FY27 至少 27 億美元的進度與利潤率揭露"},{"date":"2027-Q2","date_precision":"quarter","type":"capacity","event":"南卡羅來納三相變壓器廠投產爬坡","impact":"中","watch":"電氣美洲利潤率是否再度受拖累"},{"date":"2027-Q4","date_precision":"quarter","type":"product","event":"固態變壓器由試點轉量產","impact":"中","watch":"量產訂單揭露與對手具名案件"}],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8(val爭議)","pacing":[],"holding_cap":null,"audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟠'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場在定價 2028 年後的資料中心斷層，但最新一季滾動訂單仍 +101%，資料中心以外的公用事業、住宅與機械 OEM 訂單也在成長；現價只要求約 12% 的 EPS 年複合成長，尚無實證支持需求反轉。"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟡', moat_trend='→', week26=-14.68, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position=None, moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈機械讀數判定不可用，baseline rows 8/9/9b/10 的估值條件視為不可判 → 落 row8 觀望（保守方向）","hit":true,"basis":"val_denominator_disputed=True, val(機械讀數)='🟡'"},{"row":"QC-49","condition":"qc49_inherit_prior=False，不套用","hit":false,"basis":"qc49_inherit_prior=False"},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"requires_critic":[]}}
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
