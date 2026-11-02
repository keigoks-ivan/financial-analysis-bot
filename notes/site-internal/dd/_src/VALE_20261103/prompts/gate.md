你是 DD 管線 v20 的判斷層閘（gate），標的 VALE（20261103）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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
- `f_kpi0_pro_forma_ebitda`（q1_business）｜Pro forma EBITDA＝3.5 US$ bn｜期間與口徑：3Q26（季末 2026-09-30，公告於 2026-10-29；Vale IR 頁發布標示 10/30）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Vale IR 3Q26 Quarterly Results https://vale.com/w/3q26-quarterly-results/-/categories（numbers.latest_quarter_kpis.items[0]，as_of 3Q26（季末 2026-09-30，公告於 2026-10-29；Vale IR 頁發布標示 10/30））
- `f_kpi1_net_operating_revenue_ga`（q1_business）｜營收（net operating revenue，GAAP）＝10.6 US$ bn｜期間與口徑：3Q26（季末 2026-09-30，公告於 2026-10-29；Vale IR 頁發布標示 10/30）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Investing.com 財報電話會議摘要（媒體轉載，IR 頁未列營收，待核對 Vale 完整財報）（numbers.latest_quarter_kpis.items[1]，as_of 3Q26（季末 2026-09-30，公告於 2026-10-29；Vale IR 頁發布標示 10/30））
  - 註記：consensus US$10.51bn，beat 0.9%（Investing.com）
- `f_kpi6_realized_fines_price`（q1_business）｜鐵礦砂 realized fines price＝85.1 US$/t｜期間與口徑：3Q26（季末 2026-09-30，公告於 2026-10-29；Vale IR 頁發布標示 10/30）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Vale IR 3Q26 Quarterly Results https://vale.com/w/3q26-quarterly-results/-/categories（numbers.latest_quarter_kpis.items[6]，as_of 3Q26（季末 2026-09-30，公告於 2026-10-29；Vale IR 頁發布標示 10/30））
- `f_kpi7_c1_cash_cost`（q1_business）｜鐵礦砂 C1 cash cost＝23.1 US$/t｜期間與口徑：3Q26（季末 2026-09-30，公告於 2026-10-29；Vale IR 頁發布標示 10/30）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Vale IR 3Q26 Quarterly Results https://vale.com/w/3q26-quarterly-results/-/categories（numbers.latest_quarter_kpis.items[7]，as_of 3Q26（季末 2026-09-30，公告於 2026-10-29；Vale IR 頁發布標示 10/30））
- `f_kpi8_realized_price`（q1_business）｜銅 realized price＝15314 US$/t｜期間與口徑：3Q26（季末 2026-09-30，公告於 2026-10-29；Vale IR 頁發布標示 10/30）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Vale IR 3Q26 Quarterly Results https://vale.com/w/3q26-quarterly-results/-/categories（numbers.latest_quarter_kpis.items[8]，as_of 3Q26（季末 2026-09-30，公告於 2026-10-29；Vale IR 頁發布標示 10/30））
- `f_kpi9_realized_price`（q1_business）｜鎳 realized price＝16898 US$/t｜期間與口徑：3Q26（季末 2026-09-30，公告於 2026-10-29；Vale IR 頁發布標示 10/30）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Vale IR 3Q26 Quarterly Results https://vale.com/w/3q26-quarterly-results/-/categories（numbers.latest_quarter_kpis.items[9]，as_of 3Q26（季末 2026-09-30，公告於 2026-10-29；Vale IR 頁發布標示 10/30））
- `f_kpi10`（q1_business）｜鐵礦砂產量＝88.4 Mt｜期間與口徑：3Q26（季末 2026-09-30，公告於 2026-10-29；Vale IR 頁發布標示 10/30）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Vale IR 3Q26 Quarterly Results https://vale.com/w/3q26-quarterly-results/-/categories（numbers.latest_quarter_kpis.items[10]，as_of 3Q26（季末 2026-09-30，公告於 2026-10-29；Vale IR 頁發布標示 10/30））
- `f_peer_vale_gross_margin_pct`（q2_moat）｜VALE 毛利率＝34.82 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.VALE.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_vale_operating_margin_pct`（q2_moat）｜VALE 營業利益率＝28.71 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.VALE.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_vale_fcf_margin_pct`（q2_moat）｜VALE FCF 利潤率＝8.62 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.VALE.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝1.75 USD/share｜期間與口徑：2026-11-03／yfinance 分析師共識平均（Koyfin 快照無此檔）；幣別同報價｜kind：estimate
  - 來源：yfinance earnings_estimate（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-11-03）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝1.88 USD/share｜期間與口徑：2026-11-03／yfinance 分析師共識平均（Koyfin 快照無此檔）；幣別同報價｜kind：estimate
  - 來源：yfinance earnings_estimate（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-11-03）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝41167.4 BRL m｜期間與口徑：2026-11-03／yfinance revenue_estimate 0y 平均（17 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-03）
  - 註記：財報幣別 BRL ≠ 報價幣別 USD（ADR 或跨幣別）：淨負債／營收是 BRL，股價是 USD，每股價換算必須先對齊幣別與 ADR 比例，本欄不換算；股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝41090.05 BRL m｜期間與口徑：2026-11-03／yfinance revenue_estimate +1y 平均（23 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-03）
  - 註記：財報幣別 BRL ≠ 報價幣別 USD（ADR 或跨幣別）：淨負債／營收是 BRL，股價是 USD，每股價換算必須先對齊幣別與 ADR 比例，本欄不換算；股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi3_free_cash_flow_total`（q1_business）｜Free cash flow（total）＝2.2 US$ bn｜期間與口徑：3Q26（季末 2026-09-30，公告於 2026-10-29；Vale IR 頁發布標示 10/30）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Vale IR 3Q26 Quarterly Results https://vale.com/w/3q26-quarterly-results/-/categories（numbers.latest_quarter_kpis.items[3]，as_of 3Q26（季末 2026-09-30，公告於 2026-10-29；Vale IR 頁發布標示 10/30））
- `f_kpi4_capex`（q1_business）｜Capex＝1.3 US$ bn｜期間與口徑：3Q26（季末 2026-09-30，公告於 2026-10-29；Vale IR 頁發布標示 10/30）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Vale IR 3Q26 Quarterly Results https://vale.com/w/3q26-quarterly-results/-/categories（numbers.latest_quarter_kpis.items[4]，as_of 3Q26（季末 2026-09-30，公告於 2026-10-29；Vale IR 頁發布標示 10/30））
- `f_kpi5_expanded_net_debt`（q1_business）｜Expanded net debt＝16.4 US$ bn｜期間與口徑：3Q26（季末 2026-09-30，公告於 2026-10-29；Vale IR 頁發布標示 10/30）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Vale IR 3Q26 Quarterly Results https://vale.com/w/3q26-quarterly-results/-/categories（numbers.latest_quarter_kpis.items[5]，as_of 3Q26（季末 2026-09-30，公告於 2026-10-29；Vale IR 頁發布標示 10/30））
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝9.303 %｜期間與口徑：2026-11-03／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-11-03）
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝83856.0 BRL m｜期間與口徑：2026-11-03／yfinance 最新一季：總債務 109950.0、現金 26094.0（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-03）
  - 註記：財報幣別 BRL ≠ 報價幣別 USD（ADR 或跨幣別）：淨負債／營收是 BRL，股價是 USD，每股價換算必須先對齊幣別與 ADR 比例，本欄不換算；股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝4255.76 m shares｜期間與口徑：2026-11-03／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-11-03）
  - 註記：財報幣別 BRL ≠ 報價幣別 USD（ADR 或跨幣別）：淨負債／營收是 BRL，股價是 USD，每股價換算必須先對齊幣別與 ADR 比例，本欄不換算；股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝11.48 USD｜期間與口徑：2026-11-02（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-11-02（RTH 收盤，UTC））
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝71.81 x｜期間與口徑：2026-11-02（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-11-02（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝100.0 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝0.23 x｜期間與口徑：2026-11-02（RTH 收盤，UTC）／4 個年度端點內的分位＝0.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝0.0 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝0.62 x｜期間與口徑：2026-11-02（RTH 收盤，UTC）／4 個年度端點內的分位＝0.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝0.0 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-11-02（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝5.45 x｜期間與口徑：2026-10-24／分母＝FY1 EPS 2.09，分子＝快照價 11.39｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-10-24）
- `f_kpi2_eps`（q1_business）｜EPS＝0.29 US$/ADS｜期間與口徑：3Q26（季末 2026-09-30，公告於 2026-10-29；Vale IR 頁發布標示 10/30）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Investing.com 財報電話會議摘要（媒體轉載）（numbers.latest_quarter_kpis.items[2]，as_of 3Q26（季末 2026-09-30，公告於 2026-10-29；Vale IR 頁發布標示 10/30））
  - 註記：consensus US$0.4035，miss 28.1%
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝-25.39 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-11-02（RTH 收盤，UTC））
- `f_rsi14`（q5_valuation）｜RSI(14)＝27.99｜期間與口徑：2026-11-02（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ma_state`（q5_valuation）｜週線均線六態（decision_inputs.ma 必須等於此值）＝🟠｜期間與口徑：2026-11-03／timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）
  - 原文：「price 11.4 / W52 14.35 / W104 11.56 / W250 11.01 / W250 13週斜率 0.32%」
- `f_ma_w250`（q5_valuation）｜250 週均線＝11.01 USD｜期間與口徑：2026-11-03／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）
- `f_ma_w52`（q5_valuation）｜52 週均線＝14.35 USD｜期間與口徑：2026-11-03／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）

### findings_digest 中方向為負或來源衝突的條目（33 條）
- `competitive_share_entrants#2`（competitive_share_entrants｜方向 -｜狀態 ok）：Wood Mackenzie 預期 Simandou 2026 年出口約 1,600 萬噸並續升，滿產 120 Mtpa 約占海運鐵礦近 7%；搜尋摘要稱巴西生產商（尤其 Vale）在品質上與其正面競爭（二手摘要，未核原文）。
  - 來源：Wood Mackenzie 新聞稿 / Mining Weekly：Guinea's Simandou to become largest driver of seaborne iron ore supply growth（as_of 2026-04-01）｜affects：moat_trend、decision_inputs.bear
- `customer_second_source#0`（customer_second_source｜方向 -｜狀態 ok）：S&P Global 指出 Simandou 區塊是中國將鐵礦供應從澳洲、巴西分散的核心；首船商業貨 2026-01 運抵中國並交給中國寶武。
  - 來源：S&P Global Market Intelligence, Simandou's iron ore shipments signal major industry shift（as_of 2026-04-30）｜affects：thesis.R、decision_inputs.bear
- `supply_demand_durability#0`（supply_demand_durability｜方向 -｜狀態 ok）：UBS 預期澳洲與巴西鐵礦產量 2026、2027 每年約增 3%（約 +1.2 億噸供給），並預期中國鋼需未來 3–5 年每年約降 1%（搜尋摘要轉述，未核原文）
  - 來源：Market Index: iron ore prices set to fall as global markets shift to surplus (UBS)（as_of 2026-01-15）｜affects：thesis.R、decision_inputs.bear、valuation
- `supply_demand_durability#1`（supply_demand_durability｜方向 -｜狀態 ok）：Rio Tinto 預期 Simandou 2026 年出 5–6 百萬噸、2028 年達 60 Mtpa；RBC 認為 30 個月爬坡「技術上偏樂觀」，預估 48–60 個月；Platts 消息人士稱供過於求 2027 年起可能明顯加劇（搜尋摘要轉述，未核原文）
  - 來源：Rio Tinto Guinée / S&P Global Platts ferrous week 搜尋摘要（as_of 2026-07-15）｜affects：thesis.R、decision_inputs.bear、triggers
- `supply_demand_durability#2`（supply_demand_durability｜方向 -｜狀態 ok）：worldsteel 2026 年 10 月將全球 2026 鋼需預測由 +0.3% 下修為 -0.1%，並提及鐵礦砂觸及四年低點；4 月預估中國 2027 鋼需與 2026 大致持平；印度 2026 +7.4%、2027 +9.2%（搜尋摘要轉述，未核原文）
  - 來源：worldsteel forecast via GMK Center (搜尋摘要)（as_of 2026-10-15）｜affects：thesis.R、decision_inputs.bear、valuation
- `supply_demand_durability#4`（supply_demand_durability｜方向 -｜狀態 ok）：BHP 預期鐵礦供過於求再持續約十年（日期不明）
  - 來源：Mining.com: BHP just forecast another 10 years of iron ore glut（as_of 2016-06-21）｜affects：thesis.R、decision_inputs.bear
- `regulatory_antitrust#0`（regulatory_antitrust｜方向 -｜狀態 ok）：20-F 揭露產業特定監管：EU ETS 自2026年起對航運全面實施、FuelEU Maritime 自2025年生效，可能提高 Vale 未來運費；REACH 合規。
  - 來源：SEC EDGAR 20-F FY2025（as_of 2026-03-27）｜affects：thesis.R、valuation
- `regulatory_antitrust#1`（regulatory_antitrust｜方向 -｜狀態 ok）：2026年 Vale 收到 ANM 對 Pico、Mar Azul、Gongo Soco 礦及 Fábrica 溢流的違規通知（罰款），公司列為可能損失並提出異議。
  - 來源：Vale 6-K 3Q26（as_of 2026-10-30）｜affects：thesis.R、decision_inputs.bear
- `regulatory_antitrust#2`（regulatory_antitrust｜方向 -｜狀態 ok）：巴西 Minas Gerais 當局因 Viga 礦侵蝕與水溢流下令停工，Vale 暫停兩座礦場。
  - 來源：Engineering News: Vale halts two units after water overflow triggers permit suspension（as_of 2026-01-27）｜affects：thesis.R
- `regulatory_antitrust#3`（regulatory_antitrust｜方向 -｜狀態 ok）：印尼 Vale Indonesia 僅獲約30%的 RKAB 配額申請，尋求修訂。
  - 來源：investortrust.id: Vale Seeks RKAB Revision After Only 30% Approval（as_of 2026-01-31）｜affects：thesis.R
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：Vale 20-F 揭露：2025 年對中國客戶銷售占淨營收 51%；關稅、制裁環境或中國需求變動可能降低產品需求與營收。
  - 來源：SEC EDGAR 20-F FY2025 風險因素（as_of 2026-03-27）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#1`（reg_tariff_export｜方向 -｜狀態 ok）：Vale 20-F 揭露：作為鐵礦與鎳供應商，面臨關稅、進出口管制及貿易壁壘對自身及客戶產品的影響，整體衝擊難預測。
  - 來源：SEC EDGAR 20-F FY2025 風險因素（as_of 2026-03-27）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#2`（reg_tariff_export｜方向 -｜狀態 ok）：20-F 指出 2025 年日本、南韓粗鋼產量分別年減 4.0%、2.8%，反映關稅不確定性影響出口與需求。
  - 來源：SEC EDGAR 20-F FY2025（as_of 2026-03-27）｜affects：thesis.R
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：第三方分析指 Carajás 至 Ponta da Madeira 港為單一約 900 公里鐵路，中斷即癱瘓最大鐵礦出口節點（非 Vale 官方說法）
  - 來源：energy-solutions.co, Annual Production (Vale Brazil Iron Ore Carajás)（as_of 2026-01-01）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#2`（geo_supply_chain｜方向 -｜狀態 ok）：中國占 Vale 鐵礦砂銷量比重 2021 至 2024 由 65% 降至 61%（聚合站報導，來源品質混雜）；另有報導 Oman 球團廠因中東衝突延後至 2026 Q3 重啟
  - 來源：Search summary: Panjiva / gmk.center（as_of 2026-06-10）｜affects：thesis.R、decision_inputs.bear
- `end_markets#1`（end_markets｜方向 -｜狀態 ok）：3Q26 鐵礦砂粉平均實現價 $85/t，年減 10%；淨利年減 53%
  - 來源：Kitco / SteelOrbis（as_of 2026-10-30）｜affects：valuation、thesis.R
- `end_markets#2`（end_markets｜方向 -｜狀態 ok）：worldsteel 2026年10月展望：全球鋼需 2026 持平、2027 +1.7%；中國 2026 -2%、2027 -1%
  - 來源：Engineering News: Global steel demand to remain flat this year on China slowdown（as_of 2026-10-12）｜affects：thesis.R、decision_inputs.bear
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：Vale 在 20-F 自述：可使用較低品位鐵礦的技術可能降低其高品位產品組合的相對使用價值，對鐵礦產品需求與溢價造成負面影響；公司持續監控顛覆性技術。
  - 來源：SEC EDGAR 20-F FY2025（as_of 2026-03-27）｜affects：moat_trend、thesis.R、decision_inputs.bear
- `substitute_technology#1`（substitute_technology｜方向 -｜狀態 ok）：S&P Global 2026 Q1 亞洲鎳市場回顧：買方預期 NMC 電池需求upside有限，電池廠轉向無鎳 LFP。
  - 來源：S&P Global Commodity Insights trade review（as_of 2026-01-15）｜affects：moat_trend、thesis.R
- `substitute_technology#2`（substitute_technology｜方向 -｜狀態 ok）：Mysteel：Vale Indonesia 管理層稱鎳仍有成長空間，LFP 滲透率已逾全球電動車電池 55%。
  - 來源：Mysteel flash（as_of 2026-09-11）｜affects：thesis.R、decision_inputs.bear
- `substitute_technology#3`（substitute_technology｜方向 -｜狀態 ok）：IEEFA 報告：新製程組合可讓 DRI 使用 62-65% 一般品位鐵礦，減少對高品位礦需求。
  - 來源：IEEFA（as_of 2022-01-01）｜affects：moat_trend、thesis.R
- `capital_markets_pricing#1`（capital_markets_pricing｜方向 -｜狀態 ok）：Benzinga 表列 VALE 2026 Q3 EPS 實際 0.29 美元 vs 預期 0.33 美元（10/29 公布），Q2 亦低於預期；各來源 Q2 數字不一致（未核原文）
  - 來源：Benzinga VALE earnings-forecasts（as_of 2026-10-29）｜affects：valuation、decision_inputs.bear
- `capital_markets_pricing#3`（capital_markets_pricing｜方向 -｜狀態 ok）：Investing.com 列出 Goldman Sachs 於 2026-07-27 將 VALE 降至 Hold（未核原文）
  - 來源：Investing.com VALE consensus estimates（as_of 2026-07-27）｜affects：valuation
- `major_events#0`（major_events｜方向 -｜狀態 ok）：Vale 20-F FY2025 披露：Vale 與前高管在紐約東區聯邦法院被列為美國證券集體訴訟被告，涉 Brumadinho 尾礦壩及風險管理揭露；另有 Southern Bahia 市政府 2025-06-27 對 Samarco/BHP/Vale 提起公民訴訟（無法可靠估算曝險）、Itabira 市訴訟求償約 US$5.5 billion。
  - 來源：SEC EDGAR 20-F FY2025（as_of 2026-03-27）｜affects：decision_inputs.bear、thesis.R
- `major_events#3`（major_events｜方向 -｜狀態 ok）：2026-01 Congonhas 的 Fábrica 與 Viga 兩處因水溢流遭暫停營運許可，兩處合計年產約 8 百萬噸；Vale 重申 2026 鐵礦砂指引 335–345 百萬噸。
  - 來源：Mining Weekly: Vale halts two units after water overflow triggers permit suspension（as_of 2026-01-27）｜affects：decision_inputs.bear、thesis.R
- `cyclical_supply_discipline_capacity#0`（cyclical_supply_discipline_capacity｜方向 -｜狀態 ok）：S&P Global估Simandou鐵礦出貨2026年約15-20Mt、2027年40-50Mt，2028年約70Mt；6月報告稱爬坡快於預期
  - 來源：S&P Global, Ferrous Week: Guinea's Simandou ramp-up boosts iron ore exports surpassing forecasts（as_of 2026-06-17）｜affects：valuation、decision_inputs.bear、thesis.R
- `cyclical_supply_discipline_capacity#2`（cyclical_supply_discipline_capacity｜方向 -｜狀態 ok）：BHP FY2026鐵礦產量指引258-269Mt，WAIO中期預期超過305Mt/年（RTP1、Western Ridge Crusher）
  - 來源：Nasdaq/Zacks: BHP vs. VALE（as_of 2026-04-30）｜affects：decision_inputs.bear、thesis.R
- `cyclical_supply_discipline_capacity#4`（cyclical_supply_discipline_capacity｜方向 -｜狀態 ok）：Simandou出貨預估15-20Mt(2026)、40-50Mt(2027)
  - 來源：S&P Global（as_of 2026-01-05）｜affects：decision_inputs.bear
- `cyclical_inventory_price_position#0`（cyclical_inventory_price_position｜方向 -｜狀態 ok）：SMM 35-port China iron ore inventory about 148.3 Mt on 2026-10-16, up ~2.85 Mt m/m; weak steel output and slower pick-up; accumulation expected to continue (來源摘要轉述)
  - 來源：SMM: Iron Ore Port Inventory and Port Pick-up Volume on October 16, 2026（as_of 2026-10-16）｜affects：valuation、decision_inputs.bear
- `cyclical_inventory_price_position#1`（cyclical_inventory_price_position｜方向 -｜狀態 ok）：Vale Q3 2026 net profit fell 53% on lower iron ore prices and higher costs; iron ore output 88.4 Mt (-6% y/y), below consensus
  - 來源：Mining Weekly: Vale's profit falls 53% in Q3 on lower iron-ore prices, higher costs（as_of 2026-10-30）｜affects：valuation、thesis.R
- `cyclical_prior_downcycle_behavior#0`（cyclical_prior_downcycle_behavior｜方向 -｜狀態 ok）：Vale 2015 調整後 EBITDA 為 70.81 億美元，較 2014 年低 47%，主因售價下跌；全年 EBITDA 利潤率 27.7%，4Q15 為 23.6%（該輪低點），1Q16 回升至 35.1%。
  - 來源：Vale S.A. Form 6-K (SEC) FY2016 filing（as_of 2016-04-28）｜affects：valuation、decision_inputs.bear
- `cyclical_prior_downcycle_behavior#1`（cyclical_prior_downcycle_behavior｜方向 -｜狀態 ok）：鐵礦砂現貨價自 2011 年 2 月高點約 191.9 美元/噸，跌至 2015 年底低點約 38.8 美元/噸，跌幅約 80%，歷時約 4.5–5 年（跌幅為搜尋摘要數字推算）。
  - 來源：Bloomberg / mining.com 鐵礦價格報導（2015-12）（as_of 2015-12-10）｜affects：decision_inputs.bear、valuation
- `lawsuit_class_action#0`（lawsuit_class_action｜方向 -｜狀態 ok）：Vale 與前高管為紐約東區聯邦法院美國證券集體訴訟被告（Brumadinho 相關揭露）；Southern Bahia 市政府另於 2025-06-27 提起公民訴訟。
  - 來源：SEC EDGAR 20-F FY2025（as_of 2026-03-27）｜affects：decision_inputs.bear、thesis.R

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 4 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/VALE_20261103/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":19.2,"bear_5y_price":6.1,"p_bull_pct":20,"p_bear_pct":30,"upside_5y_pct":-9.4,"ev5y_pct":-5.4,"irr_base_pct":-2.0,"asym_ratio":0.9,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":1.75,"pe":6.56,"basis":"FY2026E 共識 EPS（yfinance 平均）；終端倍數同樣套在當年度 EPS（FY2031E）上。第三季年化僅約 1.16，起點可能偏高"},"eps":{"bull":[1.8,1.95,2.1,2.25,2.4],"base":[1.3,1.2,1.35,1.5,1.6],"bear":[0.95,0.75,0.85,1.0,1.1]},"pe":{"bull":8.0,"base":6.5,"bear":5.5},"p":{"bull":20,"base":50,"bear":30},"yield_pct":{"dividend":9.303,"net_buyback":1.0},"second_stage":{"bull_cagr_pct":5,"base_cagr_pct":2},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### VALE_Q2_2026_Earnings_Call_20260731.md
- 2026-07-31｜Marcelo Bacci｜guidance：鐵礦 C1 現金成本 2026 指引上調至 22.5–23.5 美元/噸，原為 20–21.5。（原話："with our previous guidance of $20 to $21.5 per ton."）
- 2026-07-31｜Marcelo Bacci｜guidance：鐵礦 all-in 成本指引更新為 58–62 美元/噸（原 52–56）。（原話："updating the all-in cost guidance to $58 to $62 per ton"）
- 2026-07-31｜Marcelo Bacci｜guidance：銅 all-in 成本指引下調為 0–500 美元/噸（原 1,000–1,500）。（原話："now expect all-in cost to range between $0 and $500 per ton"）
- 2026-07-31｜Marcelo Bacci｜guidance：鎳 all-in 成本指引下調為 10,000–11,500 美元/噸（原 12,000–13,500）。（原話："all-in cost to range between $10,000 and $11,500 per ton"）
- 2026-07-31｜Gustavo Pimenta｜guidance：CEO 表示對達成全年所有產量指引有信心。（原話："reinforcing our confidence in achieving all production"）
- 2026-07-31｜Marcelo Bacci｜margin：新成本指引的匯率假設為 BRL 5.13（原 5.60）。（原話："average BRL exchange rate of BRL 5.13 compared to BRL 5.60"）
- 2026-07-31｜Marcelo Bacci｜margin：新成本指引的布蘭特油價假設為 86 美元/桶（原 68）。（原話："average Brent oil price of $86 per barrel versus $68"）
- 2026-07-31｜Marcelo Bacci｜margin：管理層拆解 C1 上調約 70% 來自匯率與柴油等外部因素。（原話："combined impact of external effects such as FX and diesel"）
- 2026-07-31｜Marcelo Bacci｜margin：Q2 鐵礦 C1 現金成本（不含第三方採購）24.1 美元/噸，年增 9%。（原話："was $24.1 per ton, an increase of 9% year-on-year."）
- 2026-07-31｜Marcelo Bacci｜margin：布蘭特油避險帶來約 1 億美元效益，約 1.6 美元/噸，扣除後 all-in 為 60 美元/噸。（原話："approximately $100 million benefit equivalent to $1.6 per ton"）
- 2026-07-31｜Marcelo Bacci｜margin：效率計畫與 S11D 等低成本資產使 C1 年減 0.50 美元/噸。（原話："$0.50 per ton reduction in C1 cost year-on-year"）
- 2026-07-31｜Marcelo Bacci｜margin：Q2 pro forma EBITDA 41 億美元，年增 19%。（原話："representing a strong 19% increase year-on-year"）
- 2026-07-31｜Marcelo Bacci｜margin：管理層解釋下半年 C1 下降而 all-in 持平，因 all-in 的油價權重較高。（原話："the C1 reducing in the second half of the year"）
- 2026-07-31｜Marcelo Bacci｜margin：Q2 自由現金流含匯率與油價避險交割 3.37 億美元正向現金影響。（原話："contributed a positive cash impact of $337 million"）
- 2026-07-31｜Gustavo Pimenta｜capital_allocation：董事會核准 17 億美元股息與資本利息，9 月支付。（原話："approved $1.7 billion in dividends and interest on capital"）
- 2026-07-31｜Marcelo Bacci｜capital_allocation：新庫藏股計畫最多 1 億股、18 個月，約占流通股 2.3%。（原話："a new share buyback program of up to 100 million shares"）
- 2026-07-31｜Marcelo Bacci｜capital_allocation：擴大淨債務 Q2 收在 167 億美元，管理層預期朝 150 億參考水位收斂。（原話："converging towards our reference level of $15 billion"）
- 2026-07-31｜Marcelo Bacci｜capital_allocation：管理層說明股東回饋總額取決於下半年現金流。（原話："remuneration will depend on cash flow generation"）
- 2026-07-31｜Marcelo Bacci｜capital_allocation：管理層稱大部分現金流發生在下半年，新成本指引不致實質改變下半年現金流潛力。（原話："most of our cash flow generation comes in the second half"）
- 2026-07-31｜Marcelo Bacci｜commitment：CFO 對年底擴大淨債務接近 150 億美元表達信心。（原話："we should be approaching close to $15 billion"）
- 2026-07-31｜Gustavo Pimenta｜commitment：Bacaba 試車提前至 2027 年第三季（原 2028 上半年）。（原話："commissioning in Q3 2027, significantly ahead of"）
- 2026-07-31｜Gustavo Pimenta｜commitment：銅產量目標：2035 年倍增至約 70 萬噸/年。（原話："ambition to double copper production to approximately 700,000 tons"）
- 2026-07-31｜Carlos Medeiros｜commitment：Brucutu 導入 Conceição 同類技術，預計明年上半年完成。（原話："expect to complete during the first half of next year."）
- 2026-07-31｜Shaun Usmar｜commitment：Salobo 粗顆粒浮選預計數週內正式公告。（原話："publish the coarse particle flotation announcement"）
- 2026-07-31｜Shaun Usmar｜commitment：VBM 執行長稱 Alemão 為本十年末第一個大型專案，進度符合計畫，不暗示提前。（原話："is Alemão, and we're on track for that"）
- 2026-07-31｜Gustavo Pimenta｜product：Serra Sul +20 與 Compact Crushing 合計新增 2,000 萬噸產能。（原話："will deliver 20 million tons of incremental capacity at Serra Sul"）
- 2026-07-31｜Shaun Usmar｜product：Bacaba 重組後資本支出降近 50%，報酬率由約 50% 升至近 70%。（原話："a couple of hundred million dollars, nearly 50% reduction"）
- 2026-07-31｜Shaun Usmar｜product：Bacaba 先前報酬率約 50%，現接近 70%。（原話："the returns that we had previously at about 50% are"）
- 2026-07-31｜Shaun Usmar｜product：Salobo 粗顆粒浮選預計 2029 年時間框。（原話："that's sort of the 2029 time frame"）
- 2026-07-31｜Carlos Medeiros｜product：Conceição 專案後產品組合由 50/50 變為 75% 直接還原級、25% 高爐級。（原話："the mix has changed to 75% direct reduction and 25% blast"）
- 2026-07-31｜Shaun Usmar｜product：VBM 執行長談 2028–2035 年可能超越 70 萬噸的探勘與規劃方向。（原話："go perhaps beyond the 700 because the rocks are there"）
- 2026-07-31｜Shaun Usmar｜product：整體投資組合目標 18 個月至 2 年內儲量與資源增加逾 20%。（原話："more than 20% increase in reserves and resources"）
- 2026-07-31｜Shaun Usmar｜product：Bacaba 加上 Sossego 後端，增量約 1.5–2.5 萬噸。（原話："15,000 to 25,000 ton incremental"）
- 2026-07-31｜Shaun Usmar｜risk：Sossego SAG 磨機停機 110 天（8–11 月），影響下半年銅成本與產量。（原話："That's the 110 days of downtime from August through"）
- 2026-07-31｜Gustavo Pimenta｜risk：洞穴法令（Caves Decree）修訂細節未明，對影響的評估尚早。（原話："So it's early to say what is the potential impact."）
- 2026-07-31｜Gustavo Pimenta｜risk：Fábrica 與 Viga 營運面已就緒，待州與聯邦授權；管理層稱不影響全年指引。（原話："we are not expecting to have an impact in our annual guidance"）
- 2026-07-31｜Rogério Nogueira｜risk：Oman 球團廠 10 月將停機進行新選礦廠併接。（原話："We'll have a stoppage in October to do a tie-in for the new"）
- 2026-07-31｜Marcelo Bacci｜risk：公司未在近期進行營運成本相關的短期匯率避險。（原話："we have not been operating short-term cost-related FX"）
- 2026-07-31｜Rogério Nogueira｜competition：管理層認為中國需求面比國內指標顯示的更平衡。（原話："China story is more balanced than the domestic indicators"）
- 2026-07-31｜Rogério Nogueira｜competition：管理層模擬成本曲線：每噸 95 美元時約 1.2 億噸鐵礦達成本極限。（原話："you'd have about 120 million tons of iron ore that would actually"）
- 2026-07-31｜Rogério Nogueira｜competition：海運現貨曝險由 25% 降至約 10%，下半年曝險亦低。（原話："decrease the exposure that we had of 25% to about 10%"）
- 2026-07-31｜Marcelo Bacci｜competition：2027 年燃油避險約 70%，布蘭特均價約 77 美元。（原話："70% hedging for 2027 at an average price of about $77"）
- 2026-07-31｜Gustavo Pimenta｜customer：CEO 稱公司希望持續投資銅，並預期未來更高度投入。（原話："you should expect us to continue to be highly invested"）

### 問答異常語氣（迴避／改口／保留）
- VALE_Q2_2026_Earnings_Call_20260731.md｜問：Marcio Farid（Goldman）：新簽長期海運合約的費率是否與舊約相近、有無被現貨價格影響｜答法：Rogério 稱「I cannot disclose exactly the numbers, but the numbers have been pretty good」，未給費率數字
- VALE_Q2_2026_Earnings_Call_20260731.md｜問：Daniel Sasson（Itaú BBA）：成本上調下，回購加速或發特別股息 vs 保守保資產負債表的取捨｜答法：Bacci 未表態偏向，稱視年底淨債務而定，決定留待第三季末或第四季初，並說回購與股息之選擇要看股價與稅務
- VALE_Q2_2026_Earnings_Call_20260731.md｜問：Daniel Sasson（Itaú BBA）：Bacaba 的做法能否複製到其他專案、是否可能提前達成 2035 目標｜答法：Shaun 先答「the short answer is yes」，但隨後稱不想在此階段暗示 Alemão 會提前，並說待年底更新生命週期規劃
- VALE_Q2_2026_Earnings_Call_20260731.md｜問：Alex Hacking（Citi）：Bacaba 提前後未來 2–3 年 Sossego 該如何建模｜答法：Shaun 未給 Sossego 逐年數字，談成本下降、鑽探upside 未納入礦山計畫，並請「stay tuned」待年底更新

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 4 | 2 |
| customer_second_source | found | 2 | 1 |
| customer_concentration_credit | found | 2 | 1 |
| supply_demand_durability | found | 5 | 4 |
| regulatory_antitrust | found | 4 | 3 |
| reg_tariff_export | found | 4 | 2 |
| geo_supply_chain | found | 3 | 2 |
| end_markets | found | 5 | 3 |
| substitute_technology | found | 4 | 2 |
| channel_business_model_shift | found | 1 | 2 |
| capital_markets_pricing | found | 5 | 4 |
| major_events | found | 4 | 4 |
| cyclical_supply_discipline_capacity | found | 5 | 3 |
| cyclical_inventory_price_position | found | 3 | 3 |
| cyclical_prior_downcycle_behavior | found | 3 | 3 |

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260525","verdict":"衛星候選 / 高股息 deep value 觀察","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"Vale Base Metals EBITDA 持續 ramp 至 FY28 $5B+","columns":{"2Y":"FY26 全年 BM EBITDA &gt; $4B + Q4 26 nickel +50% YoY","5Y":"FY28 BM EBITDA $5B + Salobo Stage 4 evaluation","10Y":"VBM IPO 或新銅項目 evaluation","門檻":"BM EBITDA YoY &gt; +30%（Q1 26 + 116% 基數）","來源":"Vale Q1 26 results","漂移":"連 2 季 BM EBITDA YoY &lt; +20% → 削弱"}},{"id":"H2","text":"2026 dividend 維持 $1.2-1.3/share（7%+ yield）","columns":{"2Y":"FY26 dividend &gt; $1.0/share；payout 80-100%","5Y":"FY28 dividend &gt; $1.2/share 與 FCF 同步","10Y":"dividend 政策結構化年化 $1.5","門檻":"2026 dividend $1.2+","來源":"Vale dividend history","漂移":"2026 dividend &lt; $1.0/share → 削弱（payout cut signal）"}},{"id":"H3","text":"Brumadinho 費用 2027 後 normalize 至 &lt; $0.3B/yr","columns":{"2Y":"FY26 持續 ~$0.7B / FY27 &lt; $0.5B","5Y":"FY28+ &lt; $0.3B","10Y":"2030+ 零增量","門檻":"$0.7B 2026 → $0.3B 2028","來源":"Vale 6-K filings","漂移":"FY27 仍 &gt; $0.7B → 反轉"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"中國鋼鐵需求結構性負成長 + Carajas 高品位溢價收斂（Simandou ramp 完成 + ESG demand 不如預期）","columns":{"對應假設":"H1, H3","時間尺度":"🐢 長期（2+ 年）","監測指標":"(1) 中國 crude steel production YoY；(2) Vale Carajas 高品位 vs 62% Fe 基準 premium 月均；(3) Simandou 出貨量年度","警戒閾值":"中國鋼產 -8% YoY 連 2 年 + Carajas premium &lt; +$5/t 連 4 季 → R1 觸發；Vale 鐵礦 EBITDA -30% → 立即減倉"}},{"id":"R2","text":"Lula 政府 mining royalty 加碼 / corporate tax 加碼 / 工會權利強化三重壓制","columns":{"對應假設":"H2, H3","時間尺度":"🔥 中期（4-6 季）","監測指標":"(1) 巴西 Senate / Câmara royalty 法案進度；(2) Lula 政府重要政策聲明；(3) 2026-10 巴西總統大選候選人 polls","警戒閾值":"Royalty +5pp 或 tax +5pp 落地 → R2 觸發；2026-10 大選 Lula 繼承人勝選 → R2 加重"}},{"id":"R3","text":"Brumadinho 持續費用 + 新 dam 事件 + 監管加碼","columns":{"對應假設":"H2, H3","時間尺度":"⚡ 短期（1-2 季可觸發）","監測指標":"(1) Vale 季度 Brumadinho 公告；(2) Vale dam safety reports；(3) 巴西 CVM 調查狀態","警戒閾值":"2026 全年費用 &gt; $1.0B 或新增 dam 事件 → R3 觸發；新 dam 事件 → 立即評估清倉（風險質變不可逆）"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🟡","ma":"🟡","trap":"🟡","moat_trend":null,"runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":16.48,"archetype":null,"cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"VALE","date":"2026-11-03","schema":"v15.0","contract":"v19","company_name":"Vale S.A."},"oneliner":"Vale 現價 11.48 美元，看似 6.6 倍本益比、9% 殖利率，但第三季盈餘低於預期、Simandou 新供給才開始進場、共識還在下修；長抱不碰，等實現價止穩、共識止跌再重看","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/VALE_20261103/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/VALE_20261103/scenario.json","answers":{"q1_business":{"verdict":"賺中國鋼廠買鐵礦的錢，錢卡在「礦價減掉巴西運到中國的全成本」這一段：粉礦每噸約 25 美元空間，銅鎳是第二個錢包","reasoning":"3Q26 營收約 106 億美元、年增約 2%；鐵礦粉占淨銷售 61%、球團 11%、銅鎳等 27%（媒體整理的季報數字）。pro forma EBITDA 35 億美元、年減 20%，其中基本金屬 11 億、占 31%（10-30 法說 Bacci）。粉礦實現價 85.1 美元/噸、C1 現金成本 23.1 美元、all-in 成本 60.4 美元（含運費），每噸空間約 25 美元。近四季毛利率 34.82%、營業利益率 28.71%。客戶：對中國營收占 51%（20-F FY2025），十大客戶占鐵礦營收 35.8%，無單一客戶超過 10%，單點依賴是中國這個市場，不是某一家客戶。產業時鐘在收縮期：中國鋼需 2026 年 −2%、2027 年 −1%（worldsteel 10 月），粉礦實現價年減 10%，Simandou 新供給正在進場。供需判斷：過剩偏結構性持久，Simandou 是長壽命低成本新供給、中國需求逐年降；唯一的反向力量是管理層估約 1.6 億噸虧損產能會退出，屬可逆的高成本供給，所以 Bear 給 30%。產業態勢三軸：競爭惡化（Simandou、BHP 擴產）、結構未轉好（中國鋼需降、印度增但體量不足）、其他結構變數（中國集中採購、歐盟航運碳費、低品位直接還原技術），裁決為競爭惡化中。","fact_refs":["f_kpi0_pro_forma_ebitda","f_kpi1_net_operating_revenue_ga","f_kpi6_realized_fines_price","f_kpi7_c1_cash_cost","f_kpi8_realized_price","f_kpi9_realized_price","f_kpi10","f_peer_vale_gross_margin_pct","f_peer_vale_operating_margin_pct"],"verdict_values":{"revenue_quality":"價格接受者、品質偏低：3Q26 營收年增約 2% 全來自基本金屬（銷售年增 42%），鐵礦粉實現價年減 10%；沒有長約定價，CFO 說與 CMRG 無長約或固定價安排","unit_econ_note":"粉礦每噸：實現價 85.1 美元減 all-in 60.4 美元（含運費，10-30 法說 Bacci）約 25 美元；C1 現金成本 23.1 美元、年增 12%，主因雷亞爾升值與柴油","archetype":{"primary":"循環/商品","secondary":null,"confidence":"高","fingerprint":"鐵礦價格接受者：營收主由鐵礦報價驅動、盈餘隨價格與雷亞爾匯率擺動，近四年毛利率由 45% 降到 35%；銅鎳占 EBITDA 約三成，屬另一個長期部門"},"industry":{"clock_phase":"IV","sd_verdict_source":"worldsteel 2026-10 展望、UBS 2026-01、S&P Global 2026-06 Simandou 出貨估計、SMM 2026-10-16 港口庫存、Vale 3Q26 法說（10-30）","bargaining":{"up":"上游：柴油、船租與巴西人力；約 75% 運量為固定費率長約、2027 年已鎖逾 80%，燃油 2027 年 67% 避險在每桶 78 美元（10-30 法說）","down":"下游：中國鋼廠為主，CMRG 集中採購並稱定價機制不合理，已先與 Rio Tinto 達成協議；十大客戶占鐵礦營收 35.8%，無單一客戶超過 10%","geo":"地理：對中國營收占 51%（20-F FY2025）；北部系統靠 Carajás 到港口約 900 公里單線鐵路"},"profit_pool_dir":"鐵礦利潤池往鋼廠與新進高品位供給移，對 Vale 不利；銅利潤池在擴大，Vale 銅產量計畫 2035 年倍增","tam_table":{"expanded":false,"reason":"成熟大宗商品，不是低滲透、新品類或份額擴張題材；需求用中國與印度鋼產量追蹤，已寫進產業時鐘與供需判斷"}}}},"q2_moat":{"verdict":"護城河縮減、等級 C：成本位置還在，品質溢價與對中國的議價權在流失","reasoning":"機制是成本曲線位置加礦石品位。成本端：C1 23.1 美元/噸仍在低端，但 all-in 一年上升 21% 到 60.4 美元；7-31 法說 Bacci 把 2026 all-in 指引由 52–56 上調到 58–62，約七成來自匯率與柴油；運費長約讓 2026 年比現貨省逾 30 億美元，屬合約期內的暫時保護。品位端：all-in 溢價 4.4 美元/噸與上季持平，粉礦溢價下降、靠球團撐住；高品位 IOCJ 已低於產品組合 5%，主力改成溢價 3–6 美元的中品位（10-30 法說 Rogério）；Rogério 也承認 Simandou 與 Carajás 正面競爭、多推高品位礦不一定換得到溢價。買方端：CMRG 集中採購、已先與 Rio Tinto 達成協議，Vale 仍在談。執行力給 6：Salobo 創第三季紀錄、Sudbury 精煉創 2013 年來新高、銅 all-in −200 美元/噸，但鐵礦產量年減 6%、Serra Norte 耗竭。定價力給 5：價格接受者，只剩小幅溢價。方向：執行穩定、定價力縮減，合併判向下。同業 RIO、BHP、FMG 的利潤率在事實表為空，報酬率差距無法算，方向證據改用溢價與產品組合這條可比軸。","fact_refs":["f_kpi6_realized_fines_price","f_kpi7_c1_cash_cost","f_kpi10","f_peer_vale_gross_margin_pct","f_peer_vale_operating_margin_pct","f_peer_vale_fcf_margin_pct"],"verdict_values":{"moat":{"mechanism":"成本曲線位置加礦石品位：C1 現金成本低、Carajás 與球團有品位溢價；弱點是巴西到中國的運距","execution":6,"pricing":5,"grade":"C","trend":"↓","trend_evidence":"定價力縮減的三個一手證據：IOCJ 低於組合 5% 並改賣中品位、Simandou 與 Carajás 正面競爭（10-30 法說）、CMRG 集中採購並先與 Rio Tinto 達成協議；成本面維持：C1 23.1 美元，運費與燃油避險擋住現貨上漲","competitor_notes":[{"name":"RIO","strategy_note":"Simandou 的開發者之一，Pilbara 之外多一個高品位來源，且已先與 CMRG 達成協議，中國談判籌碼比 Vale 強"},{"name":"BHP","strategy_note":"WAIO 中期目標每年超過 3.05 億噸、持續擴產；2026 年 3 月曾被中國限制採購，顯示中國集中採購對三大礦商一視同仁"},{"name":"FMG.AX","strategy_note":"CMRG 正在與其談判（10-30 法說）；利潤率資料事實表未收，無法比較成本位置"}],"peer_na_reason":"同業 RIO、BHP、FMG.AX 的季度損益在事實表全為空值，無法算利潤率或報酬率差距","threats":[{"level":"🟡","text":"Simandou 高品位礦與 Carajás 正面競爭，滿產 1.2 億噸約占海運近 7%（方向已記在護城河趨勢，這裡不重複扣分）","p":"60%","evidence_refs":["competitive_share_entrants#2"]},{"level":"🟡","text":"中國 CMRG 集中採購、稱定價機制不合理，議價權往買方移（已記在趨勢，不重複扣分）","p":"40%","evidence_refs":["customer_second_source#0"]},{"level":"🟡","text":"低品位礦用於直接還原的新製程，削弱高品位溢價（20-F 自述風險）","p":"30%","evidence_refs":["substitute_technology#0","substitute_technology#3"]},{"level":"🟡","text":"LFP 已占全球電動車電池逾 55%，壓縮鎳的電池需求，印尼供給成長壓價","p":"50%","evidence_refs":["substitute_technology#1","substitute_technology#2"]}],"roic_durability":{"quadrant":"高利益率×低周轉：近四季營業利益率 28.71%，投入資本周轉率事實表未涵蓋（礦業重資產）；要查的是資產更新負擔，Serra Norte 自 1985 年開採、正在耗竭，得靠 Serra Leste、N3、Capanema 補量","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者、決策者、付款者都是鋼廠，鋼是必需品，需求真實；但最大市場中國鋼需 2026 年 −2%、2027 年 −1%，印度 2026 年 +7.4% 只能部分補上"},{"item":"決策層級","level":"🔴","text":"替代發生在每家鋼廠的配礦比例，Vale 粉礦與 Simandou、Pilbara 礦按使用價值互換；與 CMRG 無長約或固定價（CFO 說法），管理層也說多推高品位不一定換得到溢價"},{"item":"價值鏈分配","level":"🔴","text":"CMRG 公開稱礦商與鋼廠價值分配失衡並要處理；中國鋼廠內需疲弱、靠出口約 1.3 億噸鋼撐產量，利潤池往鋼廠回流的壓力大"},{"item":"社會容忍度","level":"🟡","text":"巴西端：洞穴保護限制 Serra Norte 開採、Fábrica 與 Viga 曾遭停工、ANM 罰單；中國端：買方以「不公平」為由壓價，形成政治價格天花板；兩者已反映在目前的量與價上，未見升級"}],"roiic":"事實表未涵蓋：投入資本與折舊攤銷未收；專案層級參考 Bacaba 報酬率由約 50% 升到近 70%（7-31 法說 Usmar），不能代表全公司","reinvest_rate":"事實表未涵蓋：只有 2026 資本支出指引 54–57 億美元與 3Q26 的 12.5 億，折舊與營業資金變動未收","endo_ceiling":null,"formula_note":"內生成長率＝增量報酬×再投資率，再投資率＝（資本支出－折舊攤銷＋營業資金變動＋收購淨額）÷稅後營業利益；兩項輸入都缺，天花板留空，情境樹不用它放寬機率"}}}},"q3_growth":{"verdict":"五年後成長空間中等：鐵礦量平、中國需求下滑，第二條曲線是銅（2030 年約 50 萬噸），但銅鎳只占營收約四分之一","reasoning":"成長來源是量，價格是被動的。共識 FY1 EPS 1.75 到 FY2 1.88 增 7.4%，同期共識營收 41,167 百萬到 41,090 百萬約持平（幣別標示待核），增幅全靠利潤率改善（成本計畫、運費避險），不是量。三年共識 EPS 年複合成長率算不出：FY2028E 事實表未收，且 FY2025 基期 EPS 0.55 含非經常損失（營業利益率 29.17% 到 29.54% 持平，淨利卻年減約 62%）。缺口歸因為利潤率擴張，這在鐵礦過剩期是最不可靠的一種。五年後：鐵礦在中國已過高峰，印度與東南亞在增但體量不足；銅有一手的產能計畫（Salobo 粗顆粒浮選 2028 上半年投產、年增約 3 萬噸；Alemão 2027 年 FID、2030 年投產），屬已啟動的第二條曲線，但撐不起全公司的寬跑道，所以給中等。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_kpi0_pro_forma_ebitda","f_kpi8_realized_price"],"verdict_values":{"growth":{"driver_mix":"量為主、價被動：鐵礦 2026 年指引 3.35–3.45 億噸、2030 年目標 3.6 億噸，年增不到 2%；銅 2026 年 36–38 萬噸到 2030 年約 50 萬噸、2035 年約 70 萬噸；併購只有小額（Ligga 30%、Minas-Rio 15%）；回購計畫 1 億股約占 2.3%，執行量未知","runway_years":"鐵礦不適用滲透率概念（中國需求已過高峰）；銅成長段到 2035 年約 9 年","runway_post_y5":"🟡","endo_ceiling_basis":"內生天花板＝增量報酬×再投資率；事實表沒有投入資本、折舊攤銷與營業資金變動，兩項都算不出，天花板留空。替代參考：Bacaba 專案報酬率約 70%（7-31 法說 Usmar），但那是單一專案，不代表全公司新增資本的報酬","segments":[{"item":"鐵礦粉","value":"占 3Q26 淨銷售 61%；實現價 85.1 美元/噸、年減 10%；鐵礦產量 8,840 萬噸、年減 6%"},{"item":"球團","value":"占 11%；2Q26 實現價 137.0 美元/噸、年增 2.2%；2026 產量指引 30–34 Mt"},{"item":"銅鎳等基本金屬","value":"占 27%；3Q26 EBITDA 11 億美元、年增逾 60%、占全公司 31%；銅實現價 15,314 美元/噸、鎳 16,898 美元/噸；銅產量年減 6%，年初至今增 4%"}],"decay_signals":[{"signal":"毛利率連 2 季年減","lit":false,"evidence":"季度毛利率事實表未涵蓋；年度 2022 到 2025 由 45.19% 降到 35.04%"},{"signal":"核心市占近 12 個月縮減","lit":false,"evidence":"海運市占事實表未涵蓋；第三季產量年減 6%、銷量持平"},{"signal":"主力產品提價後銷量下滑","lit":false,"evidence":"價格接受者，不適用"},{"signal":"EPS 成長顯著高於營收成長","lit":true,"evidence":"共識 FY1 到 FY2：EPS +7.4%、營收約 −0.2%，差 7.6 個百分點"},{"signal":"FCF／淨利 <0.75 連 2 年","lit":false,"evidence":"2023 年 0.91、2024 年 0.47、2025 年 1.19，只有一年低於"},{"signal":"股權酬勞占營收 >5% 且上升","lit":false,"evidence":"礦業股權酬勞低，金額事實表未涵蓋"},{"signal":"市場萎縮或被替代技術壓縮","lit":true,"evidence":"中國鋼需 2026 −2%、2027 −1%；LFP 逾 55% 壓縮鎳；低品位直接還原製程"},{"signal":"產業估值倍數近 3 年系統性下移","lit":false,"evidence":"Vale 自身 P/S、EV/S 在四個年度端點最低，但同業倍數事實表未收，無法確認是產業性下移"},{"signal":"維持性資本支出占 FCF >60%","lit":null,"evidence":"維持性資本支出事實表未涵蓋"},{"signal":"停止投資新產能且收入 3 年內下滑","lit":false,"evidence":"仍在投資 Capanema、S11D +20、Salobo、Bacaba"}],"trap_rating":"價值陷阱風險中等（亮 2 項），長期成長性中等"}}},"q4_capital":{"verdict":"資本配置中等偏守：負債守在目標區間、以配息為主，回購執行未證，管理層還在看低價併購","reasoning":"現金轉換：FCF／淨利 2023 年 0.91、2024 年 0.47、2025 年 1.19（年度財報，FCF＝營業現金流減資本支出；7,245÷7,983、2,919÷6,166、2,795÷2,352）。3Q26 FCF 22 億美元，含營業資金釋出與避險收益（Bacci），資本支出 12.5 億、全年朝 54–57 億指引下緣。擴大淨負債 164 億美元，在 100–200 億目標區間內，但 7-31 法說說年底接近 150 億，本季只減約 2 億。9 月付了 17 億美元股息與資本利息；CFO 10-30 說今年不太可能發特別股息、要多留現金。回購：7-31 開了 1 億股、18 個月計畫（約 2.3%），執行量與均價事實表未涵蓋；Bacci 同意股價便宜、回購有吸引力，但也說可能趁低價做併購。併購規模都小（Ligga 增資約 1.9 億美元、Thompson 轉出後保留 18.9%）。現金去向四分事實表未涵蓋。","fact_refs":["f_kpi3_free_cash_flow_total","f_kpi4_capex","f_kpi5_expanded_net_debt","f_dividend_yield_ttm","f_net_debt_m","f_shares_diluted_m"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":true,"passed":null,"input":"併購規模小（Ligga 30% 增資約 1.9 億美元、Minas-Rio 15%），已實現報酬事實表未涵蓋"},{"name":"buyback_yield","applicable":true,"passed":null,"input":"計畫 1 億股、18 個月（約 2.3% 流通股，7-31 法說）；執行量與均價事實表未涵蓋；以現價與 FY1 共識算的盈餘殖利率約 15%，10 年期殖利率事實表未收"},{"name":"sbc_dilution","applicable":true,"passed":null,"input":"股權酬勞金額事實表未涵蓋；目前股數 42.56 億股"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購撐：Ligga 增資約 1.9 億美元，不到約 490 億美元市值的 1%；Minas-Rio 15% 金額事實表未涵蓋；Thompson 是轉出"}}}},"q5_valuation":{"verdict":"現價要求 2026–27 年 EPS 守在共識 1.75–1.88；以第三季年化約 1.16 看並不便宜，我不信共識守得住","reasoning":"現價 11.48 美元。FY1 共識 1.75 算 6.6 倍、FY2 1.88 算 6.1 倍；10-24 快照用的 FY1 是 2.09（5.45 倍），兩個來源口徑可能不同，但方向一致指向下修（1.75 比 2.09 低約 16%）。TTM 本益比 71.8 倍是基期含非經常損失，不能用。P/S 0.23、EV/S 0.62 在四個年度端點最低，但只有四個點，不是五年分位。TTM 殖利率 9.3%，換算每股約 1.07 美元；CFO 說今年不太可能發特別股息。賣方均價目標 15–17 美元（9 月以前），高標 21、低標 11–12，高低比約 1.9 倍；方向與我相反，因為賣方模型還沒完全反映第三季的盈餘落差。商品循環股原本優先看股價淨值比，事實表沒有帳面價值，改用前瞻本益比加殖利率。結論：分母在下修，便宜論證暫不成立，估值給中性。","fact_refs":["f_price_at_dd","f_consensus_eps_fy1","f_consensus_eps_fy2","f_pe_current","f_pe_percentile","f_ps_current","f_ps_percentile","f_ev_s_current","f_ev_s_percentile","f_fwd_pe_latest","f_dividend_yield_ttm","f_kpi2_eps"],"verdict_values":{"valuation":{"basis":"前瞻本益比（FY1、FY2 共識）加股息殖利率；商品循環股原本優先看股價淨值比，事實表沒有帳面價值","tier":"全球海運鐵礦三大之一，與 Rio Tinto、BHP 同一層","peers":{"expanded":false,"reason":"同業 RIO、BHP、FMG.AX 在事實表的損益與倍數全為空值，無法做同一層對照"},"fwd_pe":6.56,"peg":null,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"FY1 共識 6.6 倍、FY2 6.1 倍、殖利率 9.3%，表面偏便宜；但以第三季 EPS 0.29 年化約 1.16，本益比約 9.9 倍，落在礦商的中段；分母正是爭點，便宜論證不計，給中性。五年分位：只有四個年度端點，算不出。短期：Base FY2027E EPS 1.30×7.5 倍（盈餘低點給略高倍數）＝9.75，約 −15%；中期：Base FY2031E EPS 1.60×6.5 倍＝10.40，約 −9%，兩者都未含每年約 7.5% 的股息","upside_short_pct":-15.1,"upside_mid_pct":-9.4,"denominator_disputed":true,"denominator_note":"TTM 本益比 71.8 倍的分母含非經常損失；FY1 共識 1.75 高於第三季年化約 1.16，且 10-24 快照用的 FY1 為 2.09（不同來源），分母仍在下修，便宜論證暫不計"}}},"q6_how_wrong":{"verdict":"最可能看錯：鐵礦過剩來得比預期慢、銅價續強，6 倍本益比加 9% 殖利率被重估；看錯的代價是錯過約六到七成的 Bull 漲幅","reasoning":"我最大的假設是 2027–28 年海運鐵礦轉為明顯過剩。反方：管理層說海運供給持平、中國 9 月累計進口年增 4.1%、約 1.6 億噸虧損產能會退出；RBC 認為 Simandou 爬坡要 48–60 個月；2027 年運費與燃油大多已鎖價。股價 26 週跌 25.4%、RSI 28、站在 250 週均線 11.01 附近，若共識不再下修，市場會先重估。路徑風險：從 11.48 起算，Bear 終點約 −47%；上一輪鐵礦現貨跌約八成、Vale 2015 年調整後 EBITDA 年減 47%，所以最大回撤範圍給 −40%～−60%。陷阱判斷：衰退信號亮 2 項，價值陷阱風險中等，依據見反證紀錄。","fact_refs":["f_week26_return_pct","f_rsi14","f_ma_state","f_ma_w250","f_ma_w52","f_price_at_dd","f_kpi2_eps"],"verdict_values":{"trap":{"verdict":"🟡","label":"高股息低倍數，但盈餘下行未止、共識仍在下修"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":1.75,"pe":6.56,"basis":"FY2026E 共識 EPS（yfinance 平均）；終端倍數同樣套在當年度 EPS（FY2031E）上。第三季年化僅約 1.16，起點可能偏高"},"eps":{"bull":[1.8,1.95,2.1,2.25,2.4],"base":[1.3,1.2,1.35,1.5,1.6],"bear":[0.95,0.75,0.85,1.0,1.1]},"pe":{"bull":8.0,"base":6.5,"bear":5.5},"p":{"bull":20,"base":50,"bear":30},"yield_pct":{"dividend":7.5,"net_buyback":1.0},"second_stage":{"bull_cagr_pct":5,"base_cagr_pct":2},"max_dd":{"lo":-60,"hi":-40,"basis":"從 11.48 起算：Bear 終點約 −47%（1.10×5.5 倍）；上一輪鐵礦現貨 2011–2015 由約 191.9 跌到 38.8 美元、Vale 2015 年調整後 EBITDA 年減 47%；本輪股價已由前份 16.48 跌 30%，若重演 2015 型谷底再跌 40–60%","trigger_time":null},"basis":{"bull":"Simandou 爬坡照 RBC 的 48–60 個月、印度與東南亞吸收新增量，實現價回到 90 美元以上；銅價維持高檔、Salobo 與 Bacaba 提前；回購加速；終端 8 倍","base":"2027–28 年過剩把實現價壓在 75–85 美元，成本守在指引內、約 500 萬噸高成本量調降；銅 2030 年約 50 萬噸；股息殖利率假設 7.5%（低於 TTM 9.3%，因不發特別股息）；同業現值倍數事實表未涵蓋，終端 6.5 倍對照 Vale 自身 FY1 6.6 倍、10-24 快照 5.45 倍","bear":"過剩加深、實現價 65–70 美元，對 CMRG 讓價，銅價回落；股息砍半，盈餘路徑類似 2015 年（調整後 EBITDA 年減 47%）；終端 5.5 倍"},"endo_ceiling_exceeded":null},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"S&P 估 Simandou 2026 年 15–20 Mt、2027 年 40–50 Mt、2028 年約 70 Mt；BHP WAIO 中期超過 3.05 億噸；UBS 預期澳巴產量每年增約 3%、中國鋼需 3–5 年每年降約 1%；上一輪鐵礦現貨 2011–2015 由約 191.9 跌到 38.8 美元，Vale 2015 年調整後 EBITDA 年減 47%、4Q15 EBITDA 利潤率 23.6%；SMM 港口庫存在累積","assumption":"高成本產能（管理層說約 1.6 億噸虧損）會在 75–85 美元之間退出托底","consequence":"若退出慢於新增，實現價落到 65–70 美元，粉礦每噸空間剩 5–10 美元，EPS 回到 1 美元以下、股息砍半、股價再跌 40–60%","ruling":"採納：這是 Bear 機率 30% 的來源，也是現在不建倉的主因","watch":"鐵礦粉季實現價、Simandou 月出貨、中國港口庫存","evidence_refs":["cyclical_supply_discipline_capacity#0","cyclical_supply_discipline_capacity#2","supply_demand_durability#0","cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#1","cyclical_inventory_price_position#0"],"fact_refs":["f_kpi6_realized_fines_price","f_kpi7_c1_cash_cost"]},{"view":"論點失敗","evidence":"Carajás 到港口為單線約 900 公里鐵路（第三方說法）；2026-01 Fábrica 與 Viga 因水溢流停工（合計年產約 800 萬噸）；Serra Norte 洞穴限制與老礦耗竭，第三季鐵礦產量年減 6%；Oman 球團廠因中東衝突延後","assumption":"Serra Norte 2027 年持平、2028 年靠 Serra Leste 與 N3 回補","consequence":"單一中斷事件讓季產量跌破 8,000 萬噸，固定成本攤提惡化","ruling":"部分採納：2022 年鐵路停運時靠庫存未影響指引，單次中斷可吸收；耗竭是慢性問題，已放進 Base 量假設","watch":"季產量、Serra Norte 日均產量","evidence_refs":["geo_supply_chain#0","geo_supply_chain#2","major_events#3","regulatory_antitrust#2"],"fact_refs":["f_kpi10"]},{"view":"論點成功但股東經濟變差","evidence":"Brumadinho 相關美國證券集體訴訟、Itabira 市求償約 55 億美元、Southern Bahia 公民訴訟無法估算；Fábrica 相關訴訟估計約 6.04 億美元（可能損失）與 ANM 罰單；歐盟 ETS 2026 年起全面適用航運；CMRG 稱定價機制不公、要調整礦商與鋼廠的價值分配；對中國營收占 51%","assumption":"銅成長與成本計畫成功、鐵礦量守住","consequence":"增加的現金被和解、罰款、碳費與對中國讓價吃掉，股息與回購沒跟著增加","ruling":"部分採納：訴訟金額多屬可能損失、時點未定，不放進 Base EPS；CMRG 讓價放進 Bear","watch":"季度撥備、CMRG 協議條款、訴訟進度","evidence_refs":["major_events#0","lawsuit_class_action#0","regulatory_antitrust#0","regulatory_antitrust#1","customer_second_source#0","reg_tariff_export#0","reg_tariff_export#1"],"fact_refs":[]},{"view":"價格已反映太多","evidence":"便宜看的是 FY1 共識 1.75；第三季 EPS 0.29 低於預期、淨利年減 53%，Goldman 7 月降到中立；賣方均價目標 15–17 美元是 9 月以前的數字","assumption":"市場把 6 倍本益比與 9% 殖利率當地板","consequence":"共識一路下修時，每次下修都把地板往下移，低本益比不是保護；以年化 1.16 計，本益比約 9.9 倍","ruling":"採納：Bear 錨還沒穩定，正向不對稱的數字不能當進場依據","watch":"FY2027 共識三個月變化","evidence_refs":["capital_markets_pricing#1","capital_markets_pricing#3","end_markets#1"],"fact_refs":["f_kpi2_eps","f_consensus_eps_fy1","f_consensus_eps_fy2"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 🟡 → 本次 🟠","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=🟡","side_b":"本次 ma=🟠","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 16.48 → 本次 11.48（-30.3%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=16.48","side_b":"本次 price_at_dd=11.48","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 16.48 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 16.48 美元：五年期望值 前份未列，基準年化 前份未列，前份未列不對稱比","side_b":"本次情境、股價仍用 16.48 美元：Bull 價 19.2、Bear 價 6.05，五年期望值 −34.1%，基準年化 −8.8%，不對稱比 0.17","ruling":"先換情境、股價不動：五年期望值與基準年化前份未列，無法比較。前份未列不對稱比，本次為 0.17。Bull、Bear 價位與股價無關，只受情境影響。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 16.48 美元：五年期望值 −34.1%，基準年化 −8.8%，不對稱比 0.17","side_b":"本次情境、股價 11.48 美元：五年期望值 −5.4%，基準年化 −2.0%，不對稱比 0.95","ruling":"再換股價、情境不動：起點價下跌 30.3%，五年期望值多 28.7 個百分點，基準年化多 6.8 個百分點，不對稱比由 0.17 升到 0.95。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"前份漂移：股價下跌後的估值","cause":"價格變動","prior_field":["val"],"side_a":"前份（2026-05-25）：股價 16.48 美元，估值中性","side_b":"本次（2026-11-02）：股價 11.48 美元、跌 30%，倍數變低，但第三季 EPS 0.29 年化約 1.16，分母同步下修，估值仍中性","ruling":"估值結論不變：價格跌幅大致被盈餘下修抵銷","evidence_level":"事實表價格與季報數字","settle_metric":"4Q26 EPS 與 FY2027 共識 EPS","if_then":["若 FY2027 共識守在 1.80 以上且 4Q26 EPS ≥0.40：估值改判偏便宜","若 FY2027 共識跌破 1.50：估值改判偏貴，維持不碰"],"evidence_refs":[]},{"axis":"前份漂移：投資評級與價值陷阱判斷","cause":"新證據","prior_field":["signal","trap"],"side_a":"前份：評級 B，價值陷阱風險中等","side_b":"本次：評級 C，價值陷阱風險維持中等","ruling":"評級降一級的新證據：第三季 EPS 0.29 低於預期、淨利年減 53%、鐵礦產量年減 6%、粉礦實現價年減 10%；管理層估 Simandou 年化已約 5,000 萬噸，比年初預估快。陷阱判斷不變：衰退信號亮 2 項","evidence_level":"季報與法說一手、媒體轉述","settle_metric":"4Q26 產量與 EPS","if_then":["若 4Q26 與 1Q27 EPS 都回到 0.40 以上：評級回到 B 並重跑研究","若 1Q27 EPS 低於 0.25：衰退信號再亮一項，陷阱風險升為高"],"evidence_refs":["capital_markets_pricing#1","end_markets#1","cyclical_inventory_price_position#1","cyclical_supply_discipline_capacity#0"]},{"axis":"前份漂移：護城河方向","cause":"新證據","prior_field":["moat_trend"],"side_a":"前份：未判護城河方向，風險寫的是 Carajás 溢價收斂","side_b":"本次：判縮減。10-30 法說 Rogério 承認 Simandou 與 Carajás 正面競爭、多推高品位礦不一定換得到溢價；高品位 IOCJ 已低於產品組合 5%、改以中品位為主；CMRG 先與 Rio Tinto 達成協議","ruling":"前份擔心的溢價收斂已有一手證據，定價力縮減、執行力穩定，合併判向下","evidence_level":"法說一手＋20-F 自述","settle_metric":"季報 all-in 溢價與產品組合","if_then":["若 all-in 溢價連 4 季回到 6 美元以上且 IOCJ 占比回升：方向改判持平","若 all-in 溢價跌破 2 美元：維持向下並把 Bear 機率升到 35%"],"evidence_refs":["competitive_share_entrants#2","customer_second_source#0","substitute_technology#0"]},{"axis":"前份漂移：方法補齊的欄位","cause":"方法變動","prior_field":["runway_post_y5","archetype","cycle_position","rearm_trigger","p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份這些欄為空：沒有歸類、沒有循環位置、沒有五年後成長判斷、沒跑情境樹、沒有重新進場條件","side_b":"本次補齊：歸為循環／商品、循環位置中段、五年後成長空間中等、情境機率 20／50／30、最大回撤 −40%～−60%、重新進場須三條件同時成立","ruling":"屬方法補齊，不是看法翻轉；裁決與角色由程式依新欄位重算","evidence_level":"方法","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"唯一致命點（Single Thing）由空白改為鐵礦價格門檻","cause":"新證據","prior_field":["single_thing"],"side_a":"前份：未設唯一致命點（欄位為空）","side_b":"本次 Single Thing：鐵礦粉實現價季均跌破 75 美元/噸（3Q26 為 85.1）","ruling":"選價格門檻而不是尾礦壩事故：壩體事故致命但機率低，數學上最大的單一敏感度是鐵礦價格，每噸少 10 美元約少 34.5 億美元稅前利潤；Simandou 爬坡快於預期，讓這個門檻在 12–24 個月內有實際機率","evidence_level":"季報銷量推算＋第三方供給預估","settle_metric":"季實現價","if_then":["若連 2 季低於 75 美元：持有則清倉，長抱研究停止","若連 2 季高於 85 美元且港口庫存下降：Single Thing 機率降到 25%"],"evidence_refs":["supply_demand_durability#1","cyclical_supply_discipline_capacity#4"]},{"axis":"行動門檻變動（減碼／清倉）","cause":"新證據","prior_field":["kill_metrics","triggers"],"side_a":"前份門檻：Vale 鐵礦 EBITDA −30% → 立即減倉；新 dam 事件 → 立即評估清倉；中國鋼產連 2 年 −8% 且 Carajás 溢價連 4 季 <5 美元 → 風險觸發；2026 全年 Brumadinho 費用 >10 億美元；權利金或稅率 +5 個百分點","side_b":"本次門檻：鐵礦粉實現價季均 <75 美元 → 清倉；all-in 成本連 2 季 >63 美元 → 停止加碼、連 3 季 >66 → 減碼；季產量 <8,000 萬噸 → 減碼；淨負債 >200 億美元 → 減碼；集體訴訟不利和解 → 減碼一半；新尾礦壩事故或刑事追訴 → 清倉；權利金或稅率 +5 個百分點保留","ruling":"改用季報直接讀得到的價格、成本、產量。前份減倉門檻以第三季推估已觸發：pro forma EBITDA 35 億美元年減 20%、基本金屬 11 億年增逾 60%，倒推鐵礦及其他約 24 億，年減至少約 35%（含公司費用，屬推估）。中國鋼產 −8% 退休：worldsteel 預估中國 2026 −2%、2027 −1%，這個門檻在價格受損前不會觸發；Carajás 溢價改看公司揭露的 all-in 溢價，4.4 美元已低於前份的 5 美元，但前份要求兩條同時成立，另一條未達","evidence_level":"季報推算","settle_metric":"季報鐵礦分部 EBITDA","if_then":["若 4Q26 鐵礦分部 EBITDA 年減仍超過 30%：確認前份減碼門檻已觸發，維持不碰","若年減收斂到 15% 以內：前份門檻的觸發視為暫時"],"evidence_refs":["cyclical_inventory_price_position#1","end_markets#2"]},{"axis":"前份假設與風險改寫","cause":"新證據","prior_field":["thesis.H","thesis.R"],"side_a":"前份假設：基本金屬 EBITDA 到 FY28 達 50 億美元以上；2026 年配息每股 1.2–1.3 美元；Brumadinho 費用 2027 年後降到每年 3 億美元以下。前份風險：中國鋼需與 Carajás 溢價、巴西權利金與大選、Brumadinho 與壩體","side_b":"本次假設：鐵礦 all-in 守在 62 美元內；銅 2030 年約 50 萬噸、基本金屬占 EBITDA ≥30%；淨負債守 200 億美元內並維持普通配息。本次風險：鐵礦過剩、巴西營運許可、溢價與議價權、法律合規","ruling":"配息假設改寫：CFO 10-30 說今年不太可能發特別股息，TTM 殖利率 9.3% 換算每股約 1.07 美元，前份 1.2–1.3 不成立；基本金屬方向保留，改看銅產量與占比（第三季 11 億、年化約 44 億，FY28 達 50 億仍可能）；Brumadinho 年度費用事實表未涵蓋，併入法律合規風險；巴西大選結果事實表未涵蓋，權利金門檻保留在觀察指標","evidence_level":"法說一手＋事實表","settle_metric":"2027 年 3 月配息、Vale Day","if_then":["若 2027 年 3 月普通配息每股 <0.40：資產負債表與配息假設判削弱","若 FY2026 基本金屬 EBITDA ≥40 億美元：銅引擎假設強化"],"evidence_refs":["major_events#0"]},{"axis":"便宜還是分母在掉","cause":null,"prior_field":null,"side_a":"現在就買的最強論證：FY1 共識本益比 6.6 倍、10-24 快照 5.45 倍、TTM 殖利率 9.3%、P/S 與 EV/S 在四個年度端點最低、RSI 28、股價貼近 250 週均線 11.01、賣方均價目標 15–17 美元；2027 年運費逾 80% 已鎖、燃油 67% 避險在 78 美元、匯率避險 5.72，成本能見度高；基本金屬已占 EBITDA 31%","side_b":"第三季 EPS 0.29 比預期低約 28%，年化約 1.16，換算本益比約 9.9 倍；FY1 共識在 10-24 快照為 2.09、11-03 為 1.75，仍在下修；CFO 說今年不太可能發特別股息；Simandou 2027 年出貨預估 40–50 Mt、港口庫存在累積","ruling":"不可調和（方向相反），選 B 側：便宜論證靠的是還在下修的共識，跌了 30% 本身不是安全邊際；利空出現不到一季，賣方模型只部分反映（FY1 由 2.09 降到 1.75，FY2027 仍 1.88），所以不建倉、凍結任何加碼直到第一個確認數據點","evidence_level":"事實表＋法說逐字稿；共識兩個來源口徑不同","settle_metric":"4Q26 EPS（2027 年 2 月前後）與 Vale Day 2027 成本指引","if_then":["若 4Q26 EPS ≥0.40、FY2027 共識三個月不再下修、鐵礦粉實現價 ≥80 美元：重跑研究，通過才以 1% 試單分批反買","若 FY2027 共識跌破 1.50 或實現價跌破 75 美元：維持不碰，只追循環低點","若股價先漲回 104 週均線以上但上述數據未到：不追"],"evidence_refs":["capital_markets_pricing#1","capital_markets_pricing#3","end_markets#1"]},{"axis":"鐵礦市場平衡與否","cause":null,"prior_field":null,"side_a":"管理層（10-30，Rogério Nogueira）：海運供給持平、中國 9 月累計進口增 4.1%、港口庫存持平在 1.65 億噸、Simandou 年化約 5,000 萬噸仍被吸收；7-31 也說中國比國內指標顯示的平衡","side_b":"第三方：SMM 35 港庫存 1.483 億噸、月增 285 萬噸且預期續增；worldsteel 中國 2026 −2%、2027 −1%；UBS 預期澳巴產量每年增約 3%；Platts 消息稱 2027 起過剩加劇；日本、南韓鋼產 2025 年分別減 4.0%、2.8%","ruling":"不可調和，選 B 側：管理層自己的第三季實現價年減 10%、淨利年減 53%，與「平衡」說法不符；兩家庫存口徑不同（35 港與管理層全口徑），以方向為準","evidence_level":"第三方多為搜尋摘要轉述、未核原文；管理層為一手但有立場","settle_metric":"中國港口庫存月變化、鐵礦粉季實現價","if_then":["若 SMM 港口庫存連 2 個月下降且實現價回到 85 美元以上：Bear 機率由 30% 降到 25% 並重跑研究","若庫存續升破 1.6 億噸：維持不碰，Single Thing 機率上調到 45%"],"evidence_refs":["cyclical_inventory_price_position#0","supply_demand_durability#0","supply_demand_durability#2","reg_tariff_export#2","end_markets#2"]},{"axis":"管理層前一季承諾與本季兌現","cause":null,"prior_field":null,"side_a":"7-31 法說：Bacci 說年底擴大淨負債接近 150 億美元；Pimenta 說對達成所有產量指引有信心；Bacci 說股東回饋看下半年現金流，第三季末或第四季初決定","side_b":"10-30 法說：淨負債 164 億美元，只減約 2 億；鐵礦改說落在指引下緣；Bacci 說今年不太可能發特別股息、要保留現金壓低負債。正面兌現：Salobo 粗顆粒浮選比 7-31 說的 2029 年提前、2028 上半年投產；銅鎳成本優於原指引","ruling":"可調和（程度差異）：產量仍在指引內，但淨負債目標與股東回饋都往保守方向改口；鐵礦端可信度打折，基本金屬端加分","evidence_level":"兩季法說逐字稿","settle_metric":"4Q26 擴大淨負債與 2027 年 3 月配息","if_then":["若年底淨負債高於 160 億美元且 3 月普通配息每股低於 0.40：配息假設判削弱，維持不碰","若年底淨負債降到 150 億美元以下且公布回購執行量：配息假設判守住"],"evidence_refs":[]},{"axis":"Simandou 時程","cause":null,"prior_field":null,"side_a":"RBC（2025-12）：Vale 是 Simandou 延遲的明顯贏家，高品位溢價擴大；RBC 也認為 30 個月爬坡偏樂觀、要 48–60 個月","side_b":"S&P（2026-06）：爬坡快於預期，2026 年 15–20 Mt、2027 年 40–50 Mt；管理層 10-30 估年化已約 5,000 萬噸並承認與 Carajás 競爭","ruling":"不可調和，選 B 側：RBC 的前提（延遲）已過時，最新一手說法是爬坡已在進行","evidence_level":"第三方預估＋管理層一手","settle_metric":"Simandou 月出貨","if_then":["若 Simandou 2027 年實際出貨低於 30 Mt：Bull 機率由 20% 升到 25%","若 2027 年上半年年化已超過 60 Mt：Bear 機率升到 35%，維持不碰"],"evidence_refs":["competitive_share_entrants#2","cyclical_supply_discipline_capacity#0","cyclical_supply_discipline_capacity#4","supply_demand_durability#1"]},{"axis":"基本金屬是長期成長還是價格紅利","cause":null,"prior_field":null,"side_a":"長期成長：Salobo 粗顆粒浮選核准（2028 上半年投產、年增約 3 萬噸銅）、Bacaba 提前、2030 年約 50 萬噸、2035 年約 70 萬噸；鑽探米數 2026 年逾 12 萬米","side_b":"本季 EBITDA 年增逾 60% 主要來自價格：銅產量年減 6%、年初至今僅增 4%；銅實現價 15,314 美元/噸屬高檔；鎳面對 LFP 已占電動車電池逾 55% 與印尼供給，印尼子公司 RKAB 配額初期只獲約 30%","ruling":"可調和：量的成長是真的但 2028 年後才明顯，現在的利潤增幅是價格；分兩套處理，銅的長期部分另計、不隨鐵礦循環賣出，但不足以撐起全公司估值","evidence_level":"法說一手＋第三方","settle_metric":"年度銅產量、基本金屬 EBITDA 占比","if_then":["若 2027 年銅產量年增 ≥8% 且銅價未跌：Bull 機率升到 25%","若銅價回落使基本金屬 EBITDA 占比低於 25%：維持 Base，不追"],"evidence_refs":["substitute_technology#1","substitute_technology#2","regulatory_antitrust#3"]},{"axis":"投資軌與交易軌：是不是循環低點","cause":null,"prior_field":null,"side_a":"像投降：RSI 28、26 週跌 25.4%、股價 11.48 貼近 250 週均線 11.01、P/S 與 EV/S 在四年端點最低、賣方目標高於現價、Goldman 降到中立","side_b":"六項循環訊號只有估值與情緒偏買；量價偏賣（價跌 10%、量持平）、供給紀律偏賣（Simandou、BHP 擴產，管理層只說約 500 萬噸可能調降）、庫存偏賣（港口累積）；毛利率在近四年低端但高於 2015 年谷底（4Q15 EBITDA 利潤率 23.6%）","ruling":"訊號矛盾，位置判中段、標位置不明而觀望；成長靠價格不靠量、TTM 本益比在四年端點最高（分母含非經常損失），兩道反動能限制都不放行","evidence_level":"事實表＋第三方","settle_metric":"主要礦商減產公告、港口庫存月變化","if_then":["若主要礦商宣布減產、港口庫存連 2 個月下降、股價仍在 250 週均線附近：重判為深谷，按循環規則分批反買，上限 3%","若股價先反彈站上 52 週均線 14.35 但供給與庫存沒變：不追"],"evidence_refs":["cyclical_inventory_price_position#0","cyclical_supply_discipline_capacity#2","cyclical_prior_downcycle_behavior#0"]}],"triggers":[{"n":1,"text":"唯一致命點：鐵礦粉實現價季均跌破 75 美元/噸","type":"Single Thing","maps_to":"Single Thing","metric":"Vale 季報鐵礦粉實現價","threshold":"<75 美元/噸（3Q26 為 85.1）","action":"持有則清倉；長抱不再評估，改用循環低點規則","source_freq":"Vale 季報，每季","date":null,"evidence_refs":["supply_demand_durability#1","cyclical_supply_discipline_capacity#4"]},{"n":2,"text":"鐵礦全成本是否守住指引","type":"假設驗證","maps_to":"H1","metric":"鐵礦 all-in 成本（未含避險）與 C1","threshold":"all-in 連 2 季 >63 美元/噸或 C1 >23.5","action":"停止加碼；連 3 季 >66 美元則減碼","source_freq":"Vale 季報，每季","date":null},{"n":3,"text":"銅第二引擎是否按路徑成長","type":"假設驗證","maps_to":"H2","metric":"年度銅產量、基本金屬 EBITDA 占比","threshold":"2027 年銅產量低於 2026 年實際，或基本金屬占 EBITDA <25%","action":"把銅成長從 Bull 情境移出，Bull 機率降到 15%","source_freq":"Vale 季度產銷報告，每季","date":null},{"n":4,"text":"管理層把第三季 Serra Norte 減產歸因於車隊、降雨與高錳鋁礦段三個一次性因素：未證、監測","type":"假設驗證","maps_to":"R2","metric":"季度鐵礦產量年變化","threshold":"4Q26 與 1Q27 鐵礦產量仍年減 → 一次性歸因證偽","action":"下修 Base 量假設，維持不追","source_freq":"Vale 季度產銷報告，每季","date":"2027-04","evidence_refs":["cyclical_inventory_price_position#1"]},{"n":5,"text":"巴西營運中斷或許可停工","type":"風險","maps_to":"R2","metric":"季度鐵礦產量","threshold":"<8,000 萬噸，或全年低於指引下緣 3.35 億噸","action":"減碼","source_freq":"Vale 季度產銷報告、6-K 重大訊息","date":null,"evidence_refs":["regulatory_antitrust#2","major_events#3","geo_supply_chain#0","regulatory_antitrust#1"]},{"n":6,"text":"中國對 Vale 實施採購限制，或與 CMRG 的協議讓價","type":"風險","maps_to":"R3","metric":"CMRG 協議條款、中國對 Vale 礦的採購限制","threshold":"出現對 Vale 的採購限制，或協議讓價使 all-in 溢價 <2 美元/噸","action":"減碼；限制持續一季以上則清倉","source_freq":"公司公告與新聞，事件驅動","date":null,"evidence_refs":["customer_second_source#0","reg_tariff_export#0"]},{"n":7,"text":"訴訟與尾礦壩事件","type":"風險","maps_to":"R4","metric":"證券集體訴訟進度、新增撥備、壩體安全事件","threshold":"集體訴訟不利和解或判決，或單年撥備 >10 億美元 → 減碼一半；刑事追訴或新尾礦壩事故 → 清倉","action":"減碼一半或清倉","source_freq":"Vale 6-K／20-F 訴訟附註，事件驅動","date":null,"evidence_refs":["major_events#0","lawsuit_class_action#0"]},{"n":8,"text":"資產負債表與配息","type":"減碼","maps_to":"H3","metric":"擴大淨負債、普通配息每股","threshold":"淨負債 >200 億美元，或 2027 年 3 月普通配息每股 <0.40","action":"減碼","source_freq":"Vale 季報與配息公告","date":"2027-03"},{"n":9,"text":"重新進場：分母止跌","type":"估值rearm","maps_to":"rearm","metric":"鐵礦粉實現價、FY2027 共識 EPS、週收盤對 104 週均線","threshold":"三條同時成立：實現價連 2 季 ≥80 美元、共識三個月不再下修、週收盤 >104 週均線（現 11.56）","action":"重跑研究；通過才以 1% 試單分批起步","source_freq":"季報、共識週更、週線","date":null},{"n":10,"text":"Vale Day 公布 2027 成本與產量指引","type":"複審日期","maps_to":"H1,H2","metric":"2027 all-in 成本指引、鐵礦產量指引","threshold":"all-in 指引上緣 >62 美元/噸則成本假設判削弱","action":"複審全部假設與機率","source_freq":"一次性","date":"2026-12"}],"kill_metrics":[{"metric":"鐵礦粉季實現價","bear_threshold":"<75 美元/噸","window":"任一季，連 2 季確認","source":"Vale 季報 6-K","last_status":"ok"},{"metric":"鐵礦 all-in 成本（未含避險）","bear_threshold":">66 美元/噸","window":"連 3 季","source":"Vale 季報 6-K","last_status":"ok"},{"metric":"季度鐵礦產量","bear_threshold":"<8,000 萬噸","window":"任一季","source":"Vale 季度產銷報告","last_status":"ok"},{"metric":"擴大淨負債","bear_threshold":">200 億美元","window":"任一季","source":"Vale 季報 6-K","last_status":"ok"},{"metric":"中國 35 港鐵礦庫存","bear_threshold":">1.6 億噸且連 3 個月上升","window":"月","source":"SMM 週報","last_status":"warning"},{"metric":"FY2027 共識 EPS","bear_threshold":"<1.50 美元","window":"三個月","source":"yfinance 分析師共識","last_status":"ok"},{"metric":"巴西礦業權利金或企業稅率","bear_threshold":"上調 5 個百分點以上落地","window":"任一時點","source":"巴西國會法案進度（前份門檻保留，資料缺口）","last_status":"unknown"},{"metric":"單一年度新增訴訟撥備或和解","bear_threshold":">10 億美元，或新尾礦壩事故","window":"年度","source":"Vale 6-K 或 20-F 訴訟附註","last_status":"unknown"}],"evidence_dismissed":[{"ref":"supply_demand_durability#4","reason":"這條是 2016 年 6 月的舊預測（摘要標為日期不明，原文日期 2016-06-21），講的是上一輪供給週期；2026 年的過剩判斷已由 UBS、S&P、Platts 與 worldsteel 的當期資料承擔，不能拿十年前的預測重複計分"}],"action_conditions":{"rearm_trigger":"三條同時成立才重跑研究：鐵礦粉實現價連 2 季 ≥80 美元、FY2027 共識 EPS 三個月不再下修、週收盤站回 104 週均線","exec_line":"現在不建倉、不追；三條同時成立後先重跑研究，通過才以 1% 試單分批起步；股價先漲但數據未到不追","holding_cap":"長抱不持有；條件成立後上限 3%"}},"decision_inputs":{"signal":"C","ma":"🟠","cycle_position":"中循環","cycle_verdict":"未觸發","thesis_irreconcilable":true,"valuation_dependent":false,"market_wrong_reason_given":"賣方 FY2027 EPS 1.88 與 15–17 美元目標價仍用偏高的鐵礦價格與成本假設；第三季 EPS 0.29 年化約 1.16，Simandou 2027 年出貨將由 15–20 Mt 增到 40–50 Mt","momentum_overheated":false,"cycle_gates_pass":false,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等鐵礦粉實現價連 2 季 ≥80 美元且 FY2027 共識 EPS 三個月不再下修"},"thesis":{"H":[{"id":"H1","text":"鐵礦全成本守得住：all-in 成本（未含避險）維持在 2026 指引 58–62 美元/噸內，2027 年指引不高於 62 美元，C1 不高於 23.5 美元","2y":"2027 年 all-in 季值都 ≤62 美元/噸、C1 ≤23.5 美元/噸","5y":null,"10y":null,"threshold":"all-in ≤62 美元/噸（3Q26 為 60.4）；C1 ≤23.5 美元/噸（3Q26 為 23.1）","source":"Vale 季報 6-K、Vale Day 指引","drift_rule":"以 60 美元為基準：連 2 季高 5% 以上（>63）削弱，連 3 季高 10% 以上（>66）反轉"},{"id":"H2","text":"銅成為第二引擎：銅產量由 2026 年 36–38 萬噸走到 2030 年約 50 萬噸，基本金屬占 EBITDA 維持 30% 以上","2y":null,"5y":"2030 年銅產量 ≥45 萬噸；基本金屬占 EBITDA ≥30%","10y":null,"threshold":"年度銅產量逐年成長；基本金屬 EBITDA 占比 ≥30%（3Q26 為 31%）","source":"Vale 季度產銷報告、Vale Day","drift_rule":"銅產量落後目標路徑連 4 季 ≥5% 削弱，連 6 季 ≥10% 反轉"},{"id":"H3","text":"資產負債表撐住配息：擴大淨負債守在 100–200 億美元目標區間，普通配息不靠舉債維持","2y":"2027 年兩次普通配息合計每股 ≥0.8 美元（9 月一次 17 億美元約每股 0.40）","5y":null,"10y":null,"threshold":"擴大淨負債 ≤200 億美元（3Q26 為 164 億）","source":"Vale 季報 6-K、配息公告","drift_rule":"以 164 億為基準：連 2 季高 5% 以上（>172 億）削弱，連 3 季高 10% 以上（>180 億）反轉"}],"R":[{"id":"R1","text":"鐵礦供給過剩：Simandou 爬坡、澳洲巴西增產、中國鋼需下滑，把實現價壓到 all-in 成本加 15 美元以下","h_ref":"H1,H3","clock":"🔥","threshold":"鐵礦粉實現價季均 <75 美元/噸、連 2 季（3Q26 為 85.1）","evidence_refs":["competitive_share_entrants#2","supply_demand_durability#0","supply_demand_durability#1","supply_demand_durability#2","cyclical_supply_discipline_capacity#0","cyclical_supply_discipline_capacity#2","cyclical_supply_discipline_capacity#4","end_markets#1","end_markets#2","reg_tariff_export#2"]},{"id":"R2","text":"巴西營運與許可：Serra Norte 洞穴限制與老礦耗竭、Fábrica 與 Viga 停工、ANM 罰單、Carajás 單線鐵路，加上印尼鎳配額","h_ref":"H1","clock":"⚡","threshold":"季度鐵礦產量 <8,000 萬噸（3Q26 為 8,840 萬噸），或全年低於指引下緣 3.35 億噸","evidence_refs":["regulatory_antitrust#1","regulatory_antitrust#2","regulatory_antitrust#3","major_events#3","geo_supply_chain#0","cyclical_inventory_price_position#1"]},{"id":"R3","text":"品質溢價與議價權流失：中國集中採購、低品位直接還原技術、對中國營收占 51% 與關稅貿易壁壘","h_ref":"H1,H2","clock":"🐢","threshold":"all-in 溢價 <2 美元/噸連 4 季（3Q26 約 4.4），或中國對 Vale 實施採購限制","evidence_refs":["customer_second_source#0","reg_tariff_export#0","reg_tariff_export#1","substitute_technology#0","substitute_technology#3","geo_supply_chain#2"]},{"id":"R4","text":"法律與合規成本：Brumadinho 證券集體訴訟、Itabira 市約 55 億美元求償、Southern Bahia 公民訴訟、歐盟航運碳費","h_ref":"H3","clock":"🔥","threshold":"單一年度新增撥備或和解 >10 億美元，或新尾礦壩事故","evidence_refs":["major_events#0","lawsuit_class_action#0","regulatory_antitrust#0"]}],"single_thing":{"description":"鐵礦粉實現價季均跌破 75 美元/噸（3Q26 為 85.1）","why_fatal":"鐵礦粉與球團占淨銷售約 72%；以第三季粉礦銷量 8,630 萬噸年化約 3.45 億噸，每噸少 10 美元約少 34.5 億美元稅前利潤，接近 FY1 共識淨利約 74 億美元（1.75×42.56 億股）的一半（稅前對稅後，實際衝擊較小）；跌到 75 美元時與 all-in 60.4 美元只剩約 15 美元空間，股息必降","if_happens":"盈餘走 2015 年那種下修路徑（當年調整後 EBITDA 年減 47%）；長抱不碰，持有則清倉，循環交易只在高成本供給退出、港口庫存回落後才評估","how_monitor":"Vale 季報實現價、MB61 等參考價月均、Simandou 月出貨、中國 35 港庫存（SMM 週報）","probability":"35–45%（12–24 個月）：Simandou 2027 年出貨預估 40–50 Mt、中國鋼需 2027 年再降 1%；反方是約 1.6 億噸虧損產能退出會在 75–85 美元之間托底"}},"appendix_a":{"growth_durability":4,"quality_score":5,"ai_risk":"🟢","long_term_confidence":"低","fpe_fy2":6.11,"peg_fy2":0.82,"stress":{"pass":5,"total":8},"fy2_valuation_basis":"PEG 依 Koyfin 共識（2026-11-03）"},"eps_meta":{"base_eps_path":{"FY2025A":0.55,"FY2026E":1.75,"FY2027E":1.88,"FY2028E":null},"fy_end_month":12,"eps_basis":"基期為 GAAP 稀釋 EPS（含非經常損失）；FY2026E 與 FY2027E 為 yfinance 共識平均；FY2028E 事實表未涵蓋"},"catalysts":[{"date":"2026-11","date_precision":"month","type":"regulatory","event":"Alemão 銅專案環評公聽會（因大選延後到 11 月），之後取得 LP、2027 年 FID","impact":"中","watch":"公聽會是否再延、LP 時程"},{"date":"2026-12","date_precision":"month","type":"guidance","event":"Vale Day：2027 成本與產量指引、生產力計畫、銅成長與儲量更新","impact":"高","watch":"2027 all-in 指引上緣是否 ≤62 美元/噸；可能調降的約 500 萬噸鐵礦量"},{"date":"2027-Q1","date_precision":"quarter","type":"other","event":"4Q26 財報與 2027 年 3 月配息","impact":"高","watch":"4Q26 鐵礦產量是否年增（管理層承諾）；普通配息每股是否 ≥0.40"},{"date":null,"date_precision":null,"type":"other","event":"與 CMRG 的採購與定價協議","impact":"高","watch":"是否讓價、是否限制 Vale 礦採購"},{"date":"2027-Q3","date_precision":"quarter","type":"capacity","event":"Bacaba 銅礦試車（較原定 2028 上半年提前）","impact":"低","watch":"是否如期"},{"date":"2027-Q4","date_precision":"quarter","type":"capacity","event":"Simandou 2027 年出貨量（預估 40–50 Mt）","impact":"高","watch":"月出貨是否超過年化 60 Mt"}],"decision_out":{"verdict":"迴避","role":"不持有","row_hit":"2","pacing":[],"holding_cap":null,"audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='C'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":true,"basis":"thesis_irreconcilable=True"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":true,"basis":"moat_trend='↓', moat='C'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟠'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]}],"requires_critic":[]}}
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
