你是 DD 管線 v20 的判斷層閘（gate），標的 GRAB（20261108）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（42 條）
- `f_kpi0_revenue_ifrs`（q1_business）｜Revenue（IFRS）＝1112 USD m｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-11-03）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Grab Q3 2026 IR 新聞稿（q4cdn）／SEC 6-K Ex.99.1（numbers.latest_quarter_kpis.items[0]，as_of Q3 2026（季末 2026-09-30，公告於 2026-11-03））
- `f_kpi2_ifrs_operating_profit`（q1_business）｜IFRS 營業利益（Operating profit）＝108 USD m（利益率 9.7%，自算 108÷1112）｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-11-03）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Grab Q3 2026 IR 新聞稿損益表（numbers.latest_quarter_kpis.items[2]，as_of Q3 2026（季末 2026-09-30，公告於 2026-11-03））
- `f_kpi9_on_demand_gmv`（q1_business）｜On-Demand GMV＝6.8 USD bn（YoY +18%，固定匯率 +22%）｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-11-03）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Grab Q3 2026 IR 新聞稿；外送 GMV 4,500（+21%），出行 GMV 2,335（+14%）（numbers.latest_quarter_kpis.items[9]，as_of Q3 2026（季末 2026-09-30，公告於 2026-11-03））
- `f_kpi10`（q1_business）｜金融服務（放款與營收）＝201 USD m 營收（YoY +124%）；當季放款發放 1.9bn（+115%）；放款組合 2,711（YoY +200%，不含 Superbank +115%）；90 天以上逾期 2.6%；首次轉正 Adjusted EBITDA 12｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-11-03）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Grab Q3 2026 IR 新聞稿（numbers.latest_quarter_kpis.items[10]，as_of Q3 2026（季末 2026-09-30，公告於 2026-11-03））
- `f_kpi8_mtu`（q1_business）｜MTU（月活交易用戶）＝57.2 百萬｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-11-03）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Grab Q3 2026 IR 新聞稿（numbers.latest_quarter_kpis.items[8]，as_of Q3 2026（季末 2026-09-30，公告於 2026-11-03））
- `f_peer_grab_gross_margin_pct`（q2_moat）｜GRAB 毛利率＝44.45 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.GRAB.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_grab_operating_margin_pct`（q2_moat）｜GRAB 營業利益率＝10.95 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.GRAB.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_grab_fcf_margin_pct`（q2_moat）｜GRAB FCF 利潤率＝-0.45 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.GRAB.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_se_gross_margin_pct`（q2_moat）｜SE 毛利率＝44.34 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.SE.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_se_operating_margin_pct`（q2_moat）｜SE 營業利益率＝8.24 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.SE.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_se_fcf_margin_pct`（q2_moat）｜SE FCF 利潤率＝16.92 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.SE.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_uber_operating_margin_pct`（q2_moat）｜UBER 營業利益率＝12.44 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.UBER.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_uber_fcf_margin_pct`（q2_moat）｜UBER FCF 利潤率＝18.44 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.UBER.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_dash_operating_margin_pct`（q2_moat）｜DASH 營業利益率＝5.55 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.DASH.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_dash_fcf_margin_pct`（q2_moat）｜DASH FCF 利潤率＝12.91 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.DASH.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_meli_operating_margin_pct`（q2_moat）｜MELI 營業利益率＝7.42 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MELI.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_meli_fcf_margin_pct`（q2_moat）｜MELI FCF 利潤率＝31.81 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MELI.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_kpi4_ocf_fcf_ocf`（q4_capital）｜營業現金流（OCF）與簡單 FCF（OCF−資本支出＋處分收入）＝-12 USD m（OCF 55；資本支出 71；處分收入 4；簡單 FCF＝55−71＋4，自算）｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-11-03）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Grab Q3 2026 IR 新聞稿 Adjusted FCF 調節表；簡單 FCF 為本報告自算，非公司口徑（numbers.latest_quarter_kpis.items[4]，as_of Q3 2026（季末 2026-09-30，公告於 2026-11-03））
- `f_kpi3_adjusted_free_cash_flow`（q1_business）｜Adjusted Free Cash Flow（公司定義）＝286 USD m｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-11-03）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Grab Q3 2026 IR 新聞稿；TTM 533。公司口徑含金融服務放款應收變動 +445、客戶存款 −184、處分資產 +4 等調整（numbers.latest_quarter_kpis.items[3]，as_of Q3 2026（季末 2026-09-30，公告於 2026-11-03））
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝0.14 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-11-07）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝0.14 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-11-07）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝0.21 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-11-07）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝4211.6 USD m｜期間與口徑：2026-11-08／yfinance revenue_estimate 0y 平均（18 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝5246.56 USD m｜期間與口徑：2026-11-08／yfinance revenue_estimate +1y 平均（18 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi6_fy2026`（q1_business）｜管理層指引：FY2026 營收＝4,150–4,200 USD m（YoY +23%～+25%）｜期間與口徑：Q3 2026 公告（2026-11-03），本季上修／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：Grab Q3 2026 IR 新聞稿 Business Outlook（numbers.latest_quarter_kpis.items[6]，as_of Q3 2026 公告（2026-11-03），本季上修）
  - 註記：對照 dd_numbers_extra.py capital_structure：FY1 營收共識均值 4,211.6（18 位分析師，查詢日 2026-11-08），指引上緣略低於共識均值
- `f_kpi5_sbc`（q4_capital）｜SBC（股權報酬費用）＝49 USD m（占營業利益 45%、占營收 4.4%，皆自算）｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-11-03）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Grab Q3 2026 IR 新聞稿 Adjusted EBITDA 調節表（numbers.latest_quarter_kpis.items[5]，as_of Q3 2026（季末 2026-09-30，公告於 2026-11-03））
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝-3827.0 USD m｜期間與口徑：2026-11-08／yfinance 最新一季：總債務 2070.0、現金 5897.0（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝3.41 USD｜期間與口徑：2026-11-06（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-11-06（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝24.36 x｜期間與口徑：2026-11-07／分母＝FY1 EPS 0.14，分子＝快照價 3.41｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-11-07）
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝34.1 x｜期間與口徑：2026-11-06（RTH 收盤，UTC）／1 個年度端點內的分位＝50.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝3.47 x｜期間與口徑：2026-11-06（RTH 收盤，UTC）／4 個年度端點內的分位＝0.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝0.0 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝2.5 x｜期間與口徑：2026-11-06（RTH 收盤，UTC）／4 個年度端點內的分位＝0.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝0.0 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ev_s_fwd`（q5_valuation）｜EV/S（EV ÷ FY1 共識營收）＝2.36 x｜期間與口徑：2026-11-08／f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）｜kind：estimate
  - 來源：—（numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_ev_m`（q5_valuation）｜目前企業價值 EV（市值＋淨負債）＝9939.17 USD m｜期間與口徑：2026-11-08／市值 13766.17 ＋ 淨負債 -3827.0｜kind：realized
  - 來源：—（numbers.capital_structure.ev_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝4037.0 m shares｜期間與口徑：2026-11-08／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝7.69 %｜期間與口徑：2026-08-13 → 2026-11-07／FY1 共識 EPS 0.13 → 0.14（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-11-07）
- `f_rsi14`（q5_valuation）｜RSI(14)＝66.31｜期間與口徑：2026-11-06（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-11-06（RTH 收盤，UTC））
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝-8.33 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ma_state`（q5_valuation）｜週線均線六態（decision_inputs.ma 必須等於此值）＝❌｜期間與口徑：2026-11-08／timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）
  - 原文：「price 3.41 / W52 3.87 / W104 4.44 / W250 3.79 / W250 13週斜率 -1.43%」
- `f_ma_w250`（q5_valuation）｜250 週均線＝3.79 USD｜期間與口徑：2026-11-08／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）

### findings_digest 中方向為負或來源衝突的條目（16 條）
- `competitive_share_entrants#0`（competitive_share_entrants｜方向 -｜狀態 ok）：20-F 列出各板塊競爭者：外送有 Foodpanda、ShopeeFood、Gojek（主要印尼）、Line Man Wongnai；叫車有 Gojek、Be、Bolt、Tada、Ryde、Xanh SM、Maxim、InDrive 等；支付有 ShopeePay、Google Pay、Dana、GoPay 等。
  - 來源：SEC EDGAR 20-F FY2025 Item 3 Risk Factors（as_of 2026-03-06）｜affects：moat_trend、decision_inputs.bear
- `competitive_share_entrants#1`（competitive_share_entrants｜方向 -｜狀態 ok）：20-F 指出競爭者包含新進入者，且法規變動可能便利本地與外國競爭者進入。
  - 來源：SEC EDGAR 20-F FY2025 Item 3 Risk Factors（as_of 2026-03-06）｜affects：moat_trend、decision_inputs.bear
- `supply_demand_durability#2`（supply_demand_durability｜方向 -｜狀態 ok）：Q1 2026 誘因占 On-Demand GMV 10.5%，Q1 與 Q3 管理層提及燃油價格波動、印尼法規變動與總體逆風。
  - 來源：Grab Q1 2026 earnings summary (Quartr) / Q3 6-K（as_of 2026-05-01）｜affects：thesis.R、decision_inputs.bear
- `regulatory_antitrust#0`（regulatory_antitrust｜方向 -｜狀態 ok）：印尼競爭監理機關 KPPU 於 2024、2025 年調查 Grab 與司機夥伴的合作安排（GrabExpress／GrabFood 及特殊租賃運輸），並另就印尼 P2P 借貸協會利率的卡特爾指控啟動程序（Grab 子公司為會員），程序仍在進行。
  - 來源：SEC EDGAR 20-F FY2025 Item 8 Legal Proceedings（as_of 2026-03-06）｜affects：thesis.R、decision_inputs.bear
- `regulatory_antitrust#1`（regulatory_antitrust｜方向 -｜狀態 ok）：20-F 風險因子指出東南亞反壟斷機關對大型科技公司濫用市場地位、反競爭協議與併購的關注升高，Grab 受競爭主管機關嚴密審視，可能面臨罰款或交易受阻；亦列出零工經濟、數位平台、AI 等法規風險。
  - 來源：SEC EDGAR 20-F FY2025 Item 3.D Risk Factors（as_of 2026-03-06）｜affects：thesis.R、moat_trend
- `regulatory_antitrust#4`（regulatory_antitrust｜方向 -｜狀態 ok）：馬來西亞零工工作者法 2026 年 3 月底前施行，設仲裁庭與三方諮詢理事會；2026-10 預算案政府與 Grab 共同出資 RM160 百萬零工福利方案。
  - 來源：Business Today: Budget 2027 Government, Grab To Fund RM160 Million Gig Worker Package（as_of 2026-10-09）｜affects：thesis.R、valuation
- `reg_tariff_export#1`（reg_tariff_export｜方向 -｜狀態 ok）：20-F 風險因子列「new or more burdensome regulations, taxes, or tariffs」為東南亞營運風險之一。
  - 來源：SEC EDGAR 20-F FY2025 Item 3（as_of 2026-03-06）｜affects：thesis.R
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：FY2025 20-F：幾乎全部營收與資產在東南亞；提示區域政治波動與地緣不確定性外溢風險
  - 來源：Grab Holdings Form 20-F FY2025（as_of 2026-03-31）｜affects：decision_inputs.bear、thesis.R
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：FY2024 20-F：曾因雲端供應商技術故障或中斷而遺失訂單或交易，平台可靠度隨擴張更難確保
  - 來源：Grab Holdings Form 20-F FY2024（as_of 2025-03-31）｜affects：decision_inputs.bear、thesis.R
- `end_markets#2`（end_markets｜方向 -｜狀態 ok）：市占／定價：搜尋僅見 2025 年 Euromonitor 估計 Grab+GoTo 合計印尼逾 91%、區域叫車 GMV 約 85%；分析稱與 GoTo 在印尼打補貼價格戰、定價權有限；Grab 近期據報未積極推動合併。無 2026 實際市占與價格數據。
  - 來源：Euromonitor: three key implications of the Grab and GoTo merger（as_of 2025-12-31）｜affects：moat_trend、decision_inputs.bear
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：20-F 風險因素：Grab 自述競爭者含新進者與提供低價替代品者；數位支付與 ShopeePay、Google Pay、Dana、GoPay 等競爭，數位銀行主要對手為新興數位銀行。
  - 來源：SEC EDGAR 20-F FY2025 Item 3.D（as_of 2026-03-06）｜affects：moat_trend、decision_inputs.bear
- `substitute_technology#1`（substitute_technology｜方向 -｜狀態 ok）：20-F 風險因素：AI 採用加深使第三方侵權主張風險上升，可能被迫停用某些技術。
  - 來源：SEC EDGAR 20-F FY2025 Item 3.D（as_of 2026-03-06）｜affects：thesis.R
- `capital_markets_pricing#4`（capital_markets_pricing｜方向 -｜狀態 ok）：個別券商 5 月調降目標價：Mizuho $7→$6（outperform）、JPMorgan 降至 $5.80（overweight）；StoneX 2026-09-16 維持 $7 買進。
  - 來源：MarketBeat Mizuho/JPMorgan price target articles 2026-05-05（as_of 2026-05-05）｜affects：valuation
- `major_events#1`（major_events｜方向 -｜狀態 ok）：20-F 列印尼 KPPU 對司機夥伴合作安排（GrabExpress、GrabFood、特殊租賃運輸）的調查，以及 P2P 利率卡特爾指控程序，仍在進行。
  - 來源：SEC EDGAR 20-F FY2025 Item 8 Legal Proceedings（as_of 2026-03-06）｜affects：decision_inputs.bear、thesis.R
- `major_events#2`（major_events｜方向 -｜狀態 ok）：菲律賓競爭委員會因 Grab 與 Uber 在併購審查期間違反臨時措施，合計罰 1,600 萬披索，Grab 分攤 800 萬披索（2026-02-03 報導）。
  - 來源：Carmudi Philippines：PCC Fines Grab, Uber PHP16 Million for Violating Order（as_of 2026-02-03）｜affects：decision_inputs.bear
- `product_recall_warning#0`（product_recall_warning｜方向 -｜狀態 ok）：搜尋未見 Grab 產品召回；僅見菲律賓競爭委員會因違反併購審查臨時措施的罰款（Grab 800 萬披索）。
  - 來源：Carmudi Philippines：PCC Fines Grab, Uber PHP16 Million for Violating Order（as_of 2026-02-03）｜affects：decision_inputs.bear

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 5 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/GRAB_20261108/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":12.8,"bear_5y_price":2.0,"p_bull_pct":25,"p_bear_pct":30,"upside_5y_pct":90.0,"ev5y_pct":96.3,"irr_base_pct":13.7,"asym_ratio":5.4,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":0.14,"pe":24.36,"basis":"FY2026E 共識 EPS（Koyfin 2026-11-07）；FY2026 只剩兩個月，近似年底 trailing，與終端 FY2031E 倍數同口徑。"},"eps":{"bull":[0.17,0.27,0.37,0.48,0.58],"base":[0.14,0.21,0.26,0.31,0.36],"bear":[0.11,0.12,0.13,0.13,0.14]},"pe":{"bull":22,"base":18,"bear":14},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0,"net_buyback":0},"second_stage":{"bull_cagr_pct":16,"base_cagr_pct":12},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### GRAB_Q2_2026_Earnings_Call_20260804.md
- 2026-08-04｜CEO｜guidance：CEO 表示因上半年表現加上 Superbank 合併與 Stash 收購，上調 2026 全年財測（原話："we are raising our full year 2026 guidance,"）
- 2026-08-04｜President and COO｜guidance：COO 說明財測上調區間為由 7 億至 7.2 億美元，並計入司機燃油補貼（原話："$700 million to $720 million does reflect the factors in"）
- 2026-08-04｜President and COO｜guidance：COO 表示新財測含 2% 至 3% 的匯率逆風（原話："includes the FX headwinds of between 2% to"）
- 2026-08-04｜President and COO｜guidance：COO 表示核心業務表現符合先前財測，新增部分來自 Superbank 與 Stash 合併及匯率（原話："the core business is performing well"）
- 2026-08-04｜President and COO｜guidance：COO 表示全年財測假設 Ojol 佣金結構維持現行（原話："does assume that the commission structure remains"）
- 2026-08-04｜CEO｜margin：CEO 報告第二季調整後 EBITDA 利潤率由 13.3% 升至 16.9%（原話："margin expanding to 16.9% of revenue from 13.3%"）
- 2026-08-04｜President and COO｜margin：COO 重申下半年集團出行利潤率維持歷史區間 8.5% 至 9%（原話："within the historical range of between 8.5% and 9%."）
- 2026-08-04｜President and COO｜margin：COO 給出本季出行利潤率數字（原話："mobility margins this quarter were 8.6%."）
- 2026-08-04｜President and COO｜commitment：COO 承諾下半年出行利潤率留在區間內，不論燃油價格如何（原話："We expect to stay within that range during the second half"）
- 2026-08-04｜CFO｜margin：CFO 說明出行 take rate 受司機補貼以外的夥伴獎勵加碼影響（原話："We're also leaning over and above that around partner"）
- 2026-08-04｜CFO｜product：CFO 稱平均客單價下降來自推出 saver 產品（原話："while the average ticket size went down because we did implement"）
- 2026-08-04｜President and COO｜risk：COO 說明已承諾的燃油補貼金額，自三月油價飆升起（原話："we have committed $7 million already to build support"）
- 2026-08-04｜President and COO｜risk：COO 說明印尼兩輪 Ojol 占出行 GMV 比重（原話："Ojol in Indonesia represents 6% of our"）
- 2026-08-04｜CEO｜risk：CEO 披露董事 Dara 於 7 月 6 日卸任，與收購 Foodpanda 台灣的治理強化有關（原話："Dara stepped down from our Board effective that date"）
- 2026-08-04｜President and COO｜commitment：COO 重申金融服務下半年達到獲利的承諾（原話："we are on track to achieve profitability for Financial Services"）
- 2026-08-04｜President and COO｜guidance：COO 給出年底放款餘額目標，含 Superbank（原話："book to exceed $3 billion by the end of this year"）
- 2026-08-04｜President and COO｜margin：COO 提供 Superbank 稅前股東權益報酬率數字（原話："pretax return on equity already hitting 5.7% in this quarter."）
- 2026-08-04｜President and COO｜guidance：COO 預期 Superbank 成本收入比年底前降至 50% 以下（原話："probably hitting below 50% by the end of the"）
- 2026-08-04｜CEO｜competition：CEO 回應 Uber 問題時引用 Uber 出售 Grab 持股後的競業限制（原話："competing with Grab in our core markets under 1 year"）
- 2026-08-04｜CEO｜customer：CEO 稱成長品質由交易量與用戶帶動而非價格（原話："What stands out is the health of that growth"）
- 2026-08-04｜President and COO｜customer：COO 說明 GrabMart 用戶僅占外送用戶的比例（原話："Mart still only consists of about 14% of our food user base"）
- 2026-08-04｜President and COO｜commitment：COO 表示擴大雜貨業務同時承諾外送利潤率逐年成長（原話："within our commitment to grow Deliveries margins year-on-"）
- 2026-08-04｜President and COO｜guidance：COO 預期雜貨成長快於整體外送，年底占外送 GMV 比重略升（原話："we expect this kind of growth to outpace the overall"）
- 2026-08-04｜President and COO｜product：COO 說明外送業務以固定匯率計成長加速（原話："accelerated again this time to 24% year-on-year growth"）
- 2026-08-04｜CFO｜capital_allocation：CFO 說明新增 7.5 億美元後累計庫藏股授權額度（原話："up to $1.75 billion of cumulative buyback"）
- 2026-08-04｜CFO｜capital_allocation：CFO 說明二月 5 億美元買回已執行的規模（原話："executed roughly about $400 million off that $500 million"）
- 2026-08-04｜CFO｜capital_allocation：CFO 表示買回視股價是否出現失衡而執行（原話："we'll execute where we continue to see a"）
- 2026-08-04｜CFO｜capital_allocation：CFO 稱併購門檻維持很高（原話："M&A, which we keep a very high bar"）
- 2026-08-04｜CFO｜commitment：CFO 稱 Foodpanda 台灣交易進度符合預期並預期年底前完成（原話："we remain on track with the progress on this transaction itself"）
- 2026-08-04｜CEO｜product：CEO 說明東南亞多數交易為低於一美元的兩輪車，使電動車商業化不經濟（原話："50% of all transactions in Southeast Asia are 2-wheel"）
- 2026-08-04｜CEO｜product：CEO 說明新加坡 Punggol 自駕服務預計第四季開始收取商業車資（原話："public in Q4 when we start charging commercial fares"）
- 2026-08-04｜CEO｜product：CEO 把 AI 視為利潤率槓桿（原話："why we can continue to treat AI as a margin lever."）
- 2026-08-04｜CFO｜commitment：CFO 結語稱金融服務轉盈是下一個催化劑（原話："is the next real catalyst for us"）

### 問答異常語氣（迴避／改口／保留）
- GRAB_Q2_2026_Earnings_Call_20260804.md｜問：Foodpanda 台灣的整合前期成本是多少？是否已計入 2026 財測？｜答法：CFO 只說進度符合預期、與監管機關密切討論、預期年底前完成，未回答整合成本金額，也未說明是否計入財測
- GRAB_Q2_2026_Earnings_Call_20260804.md｜問：出行 GMV、交易量與營收成長差距，take rate 下半年是否穩定或回升，出行營收如何展望？｜答法：CFO 解釋補貼與 saver 產品原因及出行利潤率 8.6%，未給 take rate 下半年走向或出行營收成長展望
- GRAB_Q2_2026_Earnings_Call_20260804.md｜問：燃油價格展望，以及出行利潤率何時回到區間高端？｜答法：COO 表示不預測油價，未給利潤率回到高端的時點，只說留在 8.5% 至 9% 區間內
- GRAB_Q2_2026_Earnings_Call_20260804.md｜問：Uber 擬收購 Delivery Hero 對東南亞競爭格局（經 Foodpanda）的影響？｜答法：CEO 談與 Uber 的股東對話、競業限制與結構優勢，未直接評論 Delivery Hero 交易的影響
- GRAB_Q2_2026_Earnings_Call_20260804.md｜問：一年後 Mart 占總 GMV 的比重與成長軌跡？｜答法：COO 只說年底占外送 GMV 比重略升、長期目標更高，未給具體百分比

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 4 | 2 |
| customer_second_source | not_applicable | 0 | 0 |
| customer_concentration_credit | found | 2 | 1 |
| supply_demand_durability | found | 4 | 2 |
| regulatory_antitrust | found | 5 | 2 |
| reg_tariff_export | found | 2 | 1 |
| geo_supply_chain | found | 2 | 2 |
| end_markets | found | 3 | 3 |
| substitute_technology | found | 3 | 2 |
| channel_business_model_shift | found | 1 | 1 |
| capital_markets_pricing | found | 5 | 3 |
| major_events | found | 5 | 4 |

未涵蓋／不適用軸的查詢詞原文（供判相關性）：
- **customer_second_source**（not_applicable）：（無查詢記錄）

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260905","verdict":"進場","role":"衛星","H":{"status":"unavailable"},"R":{"status":"unavailable"},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":13.6,"ev5y_pct":93.7,"drift_watch_prior":{"dca_verdict":"進場","dca_role":"衛星","signal":"B","val":"🟡","ma":"❌","trap":"🟡","moat_trend":"→","runway_post_y5":"🟢","asym_ratio":5.17,"ev5y_pct":93.7,"irr_base_pct":13.6,"max_dd_pct":-48,"bull_5y_price":12.5,"bear_5y_price":2.0,"p_bull_pct":25,"p_bear_pct":30,"rearm_trigger":null,"price_at_dd":3.42,"archetype":"品質複利成長","cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"GRAB","date":"2026-11-08","schema":"v15.0","contract":"v19","company_name":"Grab Holdings Limited"},"oneliner":"東南亞出行、外送與金融服務平台，三大分部首次同時獲利；現價只要五年 EPS 年化約 17% 就有 10% 年報酬，成敗在放款放大後的信用成本。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/GRAB_20261108/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/GRAB_20261108/scenario.json","answers":{"q1_business":{"verdict":"賺東南亞消費者、商家與借款人的錢：外送出行抽成、廣告和放款利息；錢卡在派單密度與放款定價兩個節點。","reasoning":"第三季營收 11.12 億美元，外送 5.61 億（+21%）、出行 3.49 億（+10%）、金融服務 2.01 億（+124%），占比約 50%、31%、18%。營業利益 1.08 億，營益率 9.7%；單季毛利率事實表未涵蓋，TTM 為 44.45%。以 GMV 推算，外送抽成約 12.5%、出行約 14.9%。成長最快的是金融服務，放款組合 27.11 億美元，年增 200%（不含 Superbank 為 115%），當季首次轉盈 1,200 萬美元。單點依賴在地區而非客戶：20-F 載明無重大客戶信用集中，但幾乎全部營收在東南亞，印尼監管是最敏感的單點；印尼占營收比重事實表未涵蓋。","fact_refs":["f_kpi0_revenue_ifrs","f_kpi2_ifrs_operating_profit","f_kpi9_on_demand_gmv","f_kpi10","f_kpi8_mtu","f_peer_grab_gross_margin_pct"],"verdict_values":{"revenue_quality":"外送與出行是高頻交易抽成，金融服務是利息收入，信用風險由公司承擔；成長最快的正是品質最難驗證的那一塊。","unit_econ_note":"外送抽成約 12.5%、分部利潤率 2.7%；出行抽成約 14.9%、分部利潤率 8.9%。出行 GMV 增 14%、營收增 10%，抽成下滑。GrabUnlimited 用戶占外送 MTU 兩成以上、貢獻外送 GMV 35%，交易頻率約 3 倍。","archetype":{"primary":"品質複利成長","secondary":"金融","confidence":"中","fingerprint":"三邊網絡平台加內嵌放款，FY2025 才首度全年獲利"},"industry":{"clock_phase":"II","sd_verdict_source":"擴張期：MTU 5,720 萬創新高，On-Demand GMV 固定匯率年增 22%，活躍司機年增 20%。需求屬結構性持久，但供給端可逆性不低：司機受油價壓力，要靠誘因留住。","bargaining":{"up":"司機可多棲且受油價壓力，公司要用補貼和誘因留人，上游議價力中等偏高。","down":"消費者可多棲；商家依賴流量，商家出資促銷年增 48%，平台對商家有議價力。","geo":"印尼、馬來西亞政府直接介入司機分潤，新加坡與台灣競爭主管機關限制併購。"},"profit_pool_dir":"新增利潤向金融服務與廣告移動；五年利潤池歷史事實表未涵蓋。","tam_table":{"expanded":false,"reason":"事實表未涵蓋 TAM、滲透率與利潤池歷史；管理層只說消費信貸可再大十倍，沒有可核對的基數，無法展開。"}}}},"q2_moat":{"verdict":"護城河方向穩定（→）：執行力擴大，定價權縮減，兩者相抵；等級 B。","reasoning":"機制是三邊網絡的本地密度，加上內嵌支付與放款資料。同業 ROIC 與投入資本事實表未涵蓋，改用利潤率比較：TTM 營業利益率 10.95%，高於 SE 8.24%、MELI 7.42%、DASH 5.55%，低於 UBER 12.44%；毛利率 44.45% 與 SE 44.34% 接近。FCF 利潤率 −0.45%，遠低於四家同業的 12.91%～31.81%，公司自身差距主要來自放款投入，事實表未拆出同業的放款現金流。可能看錯的地方：2026 年實際市占沒有資料，定價權縮減可能比抽成數字顯示的更快。","fact_refs":["f_peer_grab_gross_margin_pct","f_peer_grab_operating_margin_pct","f_peer_grab_fcf_margin_pct","f_peer_se_gross_margin_pct","f_peer_se_operating_margin_pct","f_peer_se_fcf_margin_pct","f_peer_uber_operating_margin_pct","f_peer_uber_fcf_margin_pct","f_peer_dash_operating_margin_pct","f_peer_dash_fcf_margin_pct","f_peer_meli_operating_margin_pct","f_peer_meli_fcf_margin_pct","f_kpi4_ocf_fcf_ocf","f_kpi3_adjusted_free_cash_flow"],"verdict_values":{"moat":{"mechanism":"司機、商家、消費者三邊網絡的本地密度，加上內嵌支付與放款資料；每一單都可多棲，靠會員與跨服務黏著降低流失。","execution":8,"pricing":6,"grade":"B","trend":"→","trend_evidence":"執行面擴大：活躍司機年增 20%、MTU 年增約 20% 到 5,720 萬、外送分部利潤率由 2.1% 升至 2.7%、GrabUnlimited 用戶貢獻外送 GMV 35%。定價面縮減：第三季出行 GMV 增 14%、營收只增 10%，saver 產品壓低客單價，印尼兩輪車新佣金框架 7 月生效，司機誘因上升。","competitor_notes":[{"name":"SE","strategy_note":"毛利率 44.34% 與 GRAB 接近，FCF 利潤率 16.92% 明顯較好；ShopeeFood 與 ShopeePay 在外送和支付直接競爭，是生態最完整的對手。"},{"name":"UBER","strategy_note":"營業利益率 12.44% 高於 GRAB，是股東也是合作方；出售持股後一年內不得在核心市場競爭，若買下 Delivery Hero 會改變這個平衡。"},{"name":"DASH","strategy_note":"毛利率 51.91% 最高、營業利益率 5.55% 較低，FCF 利潤率 12.91%；市場不重疊，只作外送經濟模型對照。"},{"name":"MELI","strategy_note":"FCF 利潤率 31.81% 與 GRAB 差距最大，事實表未拆出放款現金流，差距不能全歸因於經營品質。"},{"name":"GoTo","strategy_note":"印尼主要對手，2026-03 報導併購談判時冷時熱；Euromonitor 估兩家合計占區域叫車 GMV 約 85%，反壟斷機關已表態關注。"}],"peer_na_reason":"事實表沒有同業 ROIC 與投入資本，無法計算報酬差距，改用毛利率、營業利益率與 FCF 利潤率比較。","threats":[{"level":"🟡","text":"區域與單一市場對手（ShopeeFood、Gojek、Xanh SM、Maxim、InDrive）以低價搶單，印尼補貼戰壓抑定價；沒有 2026 年實際市占，份額方向無法驗證。","p":"30%","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1","end_markets#2"]},{"level":"🟡","text":"Uber 若買下 Delivery Hero，會透過 Foodpanda 留在東南亞；2026-08-04 法說 CEO 沒有正面回答，只提出售持股後一年內不得競爭的條款。","p":"15%"},{"level":"🟡","text":"ShopeePay、GoPay、Dana 等支付與數位銀行對手爭奪同一批用戶，金融服務的低獲客成本優勢只在 Grab 生態內成立。","p":"30%","evidence_refs":["substitute_technology#0"]},{"level":"🟡","text":"AI 代理把下單入口移到 app 外，傷的是廣告曝光，而廣告是外送利潤率的第二驅動力。履約、庫存與付款仍留在 Grab，分界年約 2030；自駕方面 COO 估混合期約十年，分界年約 2036。","p":"15%","evidence_refs":["substitute_technology#1"]}],"roic_durability":{"quadrant":null,"checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者、決策者、付款者多半同一人，出行與外送是高頻生活需求。MTU 創高，GrabUnlimited 用戶頻率約 3 倍。短期壓力來自通膨縮減家庭支出，不影響需求本身。"},{"item":"決策層級","level":"🟡","text":"替代性要用每一單衡量：消費者和司機都能多棲，對手名單長，還有主打低價者。會員制和跨服務能降低流失，同時買 Food 與 Mart 的用戶占外送 GMV 43%；漲價後流失率事實表未涵蓋。"},{"item":"價值鏈分配","level":"🟡","text":"司機與商家是最大的議價對手。油價上升時公司自行吸收司機補貼，法規方向也是保障司機收入與費用透明；另一方面商家出資促銷年增 48%、活躍廣告主年增 39%，廣告把部分利潤移回平台。"},{"item":"社會容忍度","level":"🔴","text":"實際定價上限是政治上限。印尼兩輪車新佣金框架 7 月生效、外送準則待公布，馬來西亞零工法上路且要共同出資 RM160 百萬，新加坡與台灣競爭主管機關先後擋下併購，放款利率也被印尼 KPPU 調查。"}],"roiic":"投入資本事實表未涵蓋，無法計算。FY2024 至 FY2025 營業利益由約 −0.55 億增至約 2.22 億美元，增量營業利益率約 48%，多來自營運槓桿，不是新資本的報酬。","reinvest_rate":"依公司調節表，第三季放款應收增加 4.45 億、客戶存款流入 1.84 億，淨投入 2.61 億美元，是當季營業利益 1.08 億的 2.4 倍；完整再投資率事實表未涵蓋。","endo_ceiling":null,"formula_note":"內生成長率＝增量 ROIC × 再投資率，兩項都缺投入資本，不硬算；情境按共識已超出內生上界處理。"}}}},"q3_growth":{"verdict":"五年後成長空間仍寬（🟢）：核心滲透率事實表未涵蓋，依據是已有來源的第二條曲線消費信貸，但它尚未經過信用循環。","reasoning":"成長以量為主，價格是負貢獻。FY2026 營收含 Superbank 與 Stash 併入，管理層 2028 年營收年複合 30% 以上的目標含待批的 Atome。三年共識 EPS 由 FY2025A 0.06 到 FY2028E 0.21，公式 CAGR 51.8%，是低基期結果；FY2026E 到 FY2028E 年化 22.5%，才是可用的前瞻成長。EPS 家數事實表未涵蓋，營收共識為 18 家。缺口來源以利潤率擴張為主，其次是回購與 Atome；內生上界無法量化，情境按已超出處理。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_kpi6_fy2026","f_kpi9_on_demand_gmv","f_kpi10"],"verdict_values":{"growth":{"driver_mix":"量為主（MTU、頻次、放款規模），價為負貢獻（抽成與客單價下滑），併購貢獻 Superbank、Stash 與待批的 Atome，回購為輔。","runway_years":"事實表未涵蓋滲透率，無法換算","runway_post_y5":"🟢","endo_ceiling_basis":"投入資本事實表未涵蓋，內生上界無法量化；共識 EPS 成長主要來自利潤率擴張和回購，按超出上界處理。","segments":[{"item":"外送","value":"第三季營收 5.61 億美元（+21%），GMV 45 億美元（+21%），分部利潤率 2.7%，長期目標 4% 以上；雜貨 GMV 成長為餐飲 1.8 倍。"},{"item":"出行","value":"第三季營收 3.49 億美元（+10%），GMV 23.35 億美元（+14%），分部利潤率 8.9%，管理層區間 8.5%～9%。"},{"item":"金融服務","value":"第三季營收 2.01 億美元（+124%），分部 EBITDA 1,200 萬美元，2028 年目標 5 億美元、放款 60 億美元以上，其中 3 億 EBITDA 來自 Atome 與 Superbank。"}],"decay_signals":[{"signal":"EPS 複合成長高於營收 5 個百分點以上","status":"成立","note":"FY2025A 到 FY2028E EPS 年化 51.8%，FY2025A 到 FY2027E 營收年化 24.8%，靠利潤率擴張。"},{"signal":"FCF/NI 連兩年低於 0.75","status":"成立","note":"FY2025 FCF −4,400 萬美元對淨利 2.68 億；TTM FCF 利潤率 −0.45%，主因放款投入。"}],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"資本配置 B 級：回購力道強、股權稀釋低，但放款吃掉現金，併購報酬尚待驗證。","reasoning":"FY2025 FCF −4,400 萬美元、淨利 2.68 億，轉換率為負；SBC 占營收 4.4%、占營業利益 45%。9、10 月回購 4 億美元，CFO 承諾 2027 年 9 月前完成其餘 5 億並註銷。foodpanda 台灣遭否決，5.5 億美元留在帳上，第四季認列 6,000 萬美元違約金。CFO 被問到放款需要多少公司資本時沒有給數字。法說逐字稿寫 TTM Adj. FCF 553，新聞稿為 533，以新聞稿為準。近三年現金去向四分、債務到期與回購均價事實表未涵蓋。","fact_refs":["f_kpi4_ocf_fcf_ocf","f_kpi5_sbc","f_kpi3_adjusted_free_cash_flow","f_net_debt_m","f_peer_grab_fcf_margin_pct"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":true,"passed":null,"input":"Stash 與 Superbank 併入不到一年，併購金額與增量獲利事實表未涵蓋，已實現報酬無法計算；foodpanda 台灣遭否決，Atome 待批。"},{"name":"buyback_yield","applicable":true,"passed":false,"input":"FY2026E EPS 0.14 除以 9、10 月股價約 2.79～3.42，買入收益率約 4.1%～5.0%。10 年期殖利率事實表未涵蓋，要過門檻須低於約 3%，保守判未過；回購均價未揭露。"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"第三季 SBC 4,900 萬美元，年化 1.96 億，占市值 1.4%，低於 1.5%；扣除回購後股數淨減少。"}]},"governance":{"capital_returns":[{"item":"回購","value":"9、10 月買回 4 億美元，尚餘 5 億美元，承諾 2027 年 9 月前完成並註銷。"},{"item":"累計授權","value":"上限 17.5 億美元（CFO，2026-08-04）。"},{"item":"併購","value":"Stash、Superbank 已併入；foodpanda 台灣遭否決；Atome 待批，金額事實表未涵蓋。"},{"item":"股息","value":"事實表未涵蓋，情境以 0 計。"}]}}},"q5_valuation":{"verdict":"現價要求 FY2031 年 EPS 達約 0.30、終端 18 倍，才有 10% 年報酬；我相信做得到，但要放款信用成本守住。","reasoning":"3.41 美元以 10% 年報酬滾五年約需 5.49，除以 18 倍得 EPS 0.305，較 FY2026E 0.14 年化約 17%。基本情境 FY2031 EPS 0.36，高於這個要求，差距來自利潤率擴張。同業倍數事實表未涵蓋，終端倍數只能對照公司目前 24.36 倍。可能看錯的地方：FY2027E 共識 EPS 與 FY2026E 同為 0.14，起點若含一次性項目，年化要求會更高。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_pe_current","f_ps_current","f_ps_percentile","f_ev_s_current","f_ev_s_percentile","f_ev_s_fwd","f_ev_m","f_net_debt_m","f_shares_diluted_m","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_consensus_rev_3m_fy1_pct"],"verdict_values":{"valuation":{"basis":"EPS 乘本益比為主；EV/銷售與 EV/EBITDA 只作對照，因淨現金口徑有爭議。","peers":{"expanded":false,"reason":"事實表只有同業利潤率，沒有同業倍數，無法做倍數對照，屬資料缺口。"},"fwd_pe":24.36,"peg":1.08,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"現價 3.41 美元，FY2026E 本益比 24.36 倍，PEG 1.08（FY2025A 基期公式得 0.47，是低基期假象，不採用；改用 FY2026E 到 FY2028E 年化 22.5%）。EV/FY1 營收 2.36 倍，在四個年度端點內最低，但五年區間分位事實表未涵蓋。12 個月以 FY2028E EPS 0.21×20 倍得 4.20，上檔 23.2%；24 個月以 FY2029E 0.26×20 倍得 5.20，上檔 52.5%。結論是合理價，不是便宜價。","upside_short_pct":23.2,"upside_mid_pct":52.5,"denominator_disputed":true,"denominator_note":"兩個分母都有爭議。EPS：FY2026E 與 FY2027E 共識同為 0.14，營收卻增 24.6%，事實表無法判斷是否混有一次性項目或併購攤提。EV：淨現金 38.27 億美元未扣數位銀行存款 27 億（總債務 20.7 億小於存款，存款不可能全列在內）；若存款資金仍多放在現金，EV 最高約 126 億，EV/FY1 營收約 3.0 倍。"}}},"q6_how_wrong":{"verdict":"最可能看錯在放款信用成本與監管分潤，其次才是競爭；價值陷阱風險中等。","reasoning":"成長熄火測試以 FY2028E EPS 0.21 為起點：之後年增 15%、終端 18 倍得 5.75；年增 10%、14 倍得 3.91；年增 5%、11 倍得 2.67，對現價分別 +69%、+15%、−22%，三個情境中兩個不虧。十項衰退訊號成立兩項，都和放款投入或低基期有關。歷史最大回撤與四週漲幅事實表未涵蓋；RSI 66.31 未超過 70，另知股價由 10 月 26 日附近約 2.79 反彈到 3.41。法說未正面回答的有：第三季金融服務 EBITDA 拆分、放款需要多少公司資本、印尼準則細節（2026-11-03）；出行抽成下半年走向、Uber 收購 Delivery Hero 的影響（2026-08-04）。","fact_refs":["f_kpi10","f_kpi4_ocf_fcf_ocf","f_kpi3_adjusted_free_cash_flow","f_rsi14","f_price_at_dd","f_week26_return_pct","f_ma_state","f_ma_w250"],"verdict_values":{"trap":{"verdict":"🟡","label":"放款擴張把 FCF 壓成負值，獲利成長靠利潤率擴張"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":0.14,"pe":24.36,"basis":"FY2026E 共識 EPS（Koyfin 2026-11-07）；FY2026 只剩兩個月，近似年底 trailing，與終端 FY2031E 倍數同口徑。"},"eps":{"bull":[0.17,0.27,0.37,0.48,0.58],"base":[0.14,0.21,0.26,0.31,0.36],"bear":[0.11,0.12,0.13,0.13,0.14]},"pe":{"bull":22,"base":18,"bear":14},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0,"net_buyback":0},"second_stage":{"bull_cagr_pct":16,"base_cagr_pct":12},"max_dd":{"lo":-60,"hi":-42,"basis":"歷史最大回撤事實表未涵蓋，由情境推得：空頭終點 1.96 為 −42.5%；極端空頭以倍數 14×0.8、FY1 EPS 0.14×0.9 得約 1.41，為 −58.6%，取 −60% 至 −42%。","trigger_time":null},"basis":{"bull":"FY2028 EBITDA 達 17 億美元目標以上，Atome 併入後消費信貸放大，FY2031 EPS 0.58；22 倍。同業現值倍數事實表未涵蓋，只能對照公司目前 24.36 倍。","base":"FY2027、FY2028 貼共識 0.14、0.21，之後年增由 24% 降到 16%，FY2031 EPS 0.36；回購效果已含在 EPS，淨回購殖利率填 0 避免重複；18 倍，較現值壓縮 26%。","bear":"放款信用成本上升加上印尼分潤法規壓利潤率，FY2031 EPS 停在 0.14；14 倍，依成長熄火至 10% 的情境。空頭機率 30%，因內生上界無法驗證且放款尚未經過信用循環。"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"放款組合一年變三倍到 27.11 億美元，90 天以上逾期率 2.6% 的分母剛放大；金融服務營收 2.01 億、EBITDA 1,200 萬，離 2028 年 5 億美元還很遠，其中 3 億要靠 Atome 與 Superbank。","assumption":"放款擴張到 60 億美元以上，逾期率仍可維持在 3.5% 以下，消費信貸模型在東南亞適用。","consequence":"信用循環轉差時，放款損失、收緊放款和淨現金下降同時發生，FY2031 EPS 停在 0.14，股價約 1.96，五年虧 43%；極端情況下虧損超過 50%。","ruling":"採納，列為唯一致命項。此視角與唯一致命事件直接重疊，不另寫第二個故事。空頭機率維持 30%。","watch":"逾期餘額增速相對放款增速；Atome 併入後分開看消費信貸。","evidence_refs":["regulatory_antitrust#0"],"fact_refs":["f_kpi10"]},{"view":"論點成功但股東經濟變差","evidence":"第三季 Adj. FCF 2.86 億美元，簡單 FCF 卻是 −1,200 萬；放款淨投入 2.61 億。Adj. EBITDA 2.37 億排除 SBC 4,900 萬與折舊攤銷，營業利益只有 1.08 億。","assumption":"營收和 EBITDA 目標達成，股東就分得到現金。","consequence":"目標達成但放款長期吃掉現金，回購靠既有現金而不是自由現金流，17 億美元 EBITDA 對股東的價值要打折。","ruling":"部分採納：估值以 EPS 為準，不用 Adj. EBITDA 或 Adj. FCF；基本情境終端倍數壓到 18 倍。","watch":"簡單 FCF、扣除銀行存款後淨現金、銀行占放款比重。","fact_refs":["f_kpi3_adjusted_free_cash_flow","f_kpi4_ocf_fcf_ocf","f_kpi5_sbc"]},{"view":"論點成功但股東經濟變差","evidence":"印尼兩輪車新佣金框架 7 月生效，外送準則待公布；馬來西亞零工法上路並共同出資 RM160 百萬；競爭主管機關擋下併購。社會容忍度是四項持續期檢查中最弱的一項。","assumption":"抽成率維持 13% 以上，監管只要求透明，不壓實質分潤。","consequence":"平台規模繼續擴大，但新增的經濟利益被分給司機，利潤率停在目前水準。","ruling":"採納為中期風險。管理層說不影響指引，但指引只到 2026 年底，不能當作風險已解除。","watch":"出行分部利潤率 8.5% 下限、On-Demand 抽成 13%。","evidence_refs":["regulatory_antitrust#1","regulatory_antitrust#4"]},{"view":"價格已反映太多","evidence":"FY2026E 本益比 24.36 倍，FY2027E 共識 EPS 零成長；若把 27 億美元銀行存款視為負債，EV 由 99 億美元升至約 126 億，EV/FY1 營收由 2.36 倍升至約 3.0 倍。","assumption":"淨現金 38.27 億美元都是可用現金，且 2028 年 17 億美元 EBITDA 能達成。","consequence":"EV 對 2028 年 EBITDA 目標 5.8～7.4 倍的低倍數可能是假象，真實倍數取決於目標打幾折。","ruling":"反駁一半：就算用 126 億美元 EV、目標打八折（13.6 億），也只有約 9.3 倍。但 24 倍本益比本身不便宜，因此估值結論定為合理而非便宜。","watch":"2027 年指引、Atome 付款方式、銀行占放款比重。","fact_refs":["f_fwd_pe_latest","f_ev_m","f_ev_s_fwd","f_net_debt_m"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ❌ → 本次 ❌","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=❌","side_b":"本次 ma=❌","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 3.42 → 本次 3.41（-0.3%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=3.42","side_b":"本次 price_at_dd=3.41","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]裁決由 dd_decision.py 機械路由：前份 進場 → 本次 觀望","cause":"方法變動","prior_field":["dca_verdict"],"side_a":"前份 dca_verdict=進場","side_b":"本次 dca_verdict=觀望","ruling":"裁決是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。矩陣輸入無可比對的前份值。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]角色由 dd_decision.py 機械路由：前份 衛星 → 本次 追蹤","cause":"方法變動","prior_field":["dca_role"],"side_a":"前份 dca_role=衛星","side_b":"本次 dca_role=追蹤","ruling":"角色是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。矩陣輸入無可比對的前份值。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 3.42 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 3.42 美元：Bull 價 12.5、Bear 價 2，五年期望值 +93.7%，基準年化 13.6%，不對稱比 5.17","side_b":"本次情境、股價仍用 3.42 美元：Bull 價 12.76、Bear 價 1.96，五年期望值 +95.7%，基準年化 13.6%，不對稱比 5.33","ruling":"先換情境、股價不動：五年期望值多 2.0 個百分點，基準年化多 0.0 個百分點。不對稱比由 5.17 變為 5.33。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變好。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 3.42 美元：五年期望值 +95.7%，基準年化 13.6%，不對稱比 5.33","side_b":"本次情境、股價 3.41 美元：五年期望值 +96.3%，基準年化 13.7%，不對稱比 5.37","ruling":"再換股價、情境不動：起點價下跌 0.3%，五年期望值多 0.6 個百分點，基準年化多 0.1 個百分點，不對稱比由 5.33 升到 5.37。合計五年期望值比前份多 2.6 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"基本面結論與前份比較","cause":"新證據","prior_field":["signal","val","trap","moat_trend","runway_post_y5","archetype","cycle_position"],"side_a":"2026-09-05：綜合評等 B、估值 🟡、價值陷阱 🟡、護城河 →、五年後成長空間 🟢、類型為品質複利成長、未標循環位置，裁決進場。","side_b":"2026-11-08：上述基本面結論不變。第三季金融服務提前轉盈、全年指引第二次上修；但印尼新佣金框架已生效、foodpanda 台灣遭否決、外送準則細節未定，正負相抵。","ruling":"維持前份方向，裁決與角色依本次輸入重算。","evidence_level":"公司財報與法說（2026-11-03）","settle_metric":"下次財報的 2027 年指引與逾期率","if_then":["若 2027 年 Adj. EBITDA 指引低於 10 億美元，停止加碼。","若指引不低於 11 億美元且逾期率低於 3%，分批反買補足保留部位。"]},{"axis":"情境機率與回撤範圍","cause":"方法變動","prior_field":["p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份多頭機率 25%、空頭 30%、最大回撤 −48%（單點）。","side_b":"本次多頭 25%、空頭 30%、最大回撤 −60% 至 −42%（範圍）。","ruling":"機率不動：金融服務提前轉盈的利多，與消費信貸併入、印尼法規未定的風險相抵。回撤改寫成範圍並納入極端空頭。","evidence_level":"情境假設"},{"axis":"行動門檻重設（減碼、清倉）","cause":"方法變動","prior_field":["rearm_trigger","kill_metrics"],"side_a":"前份摘要未附門檻原文，再進場條件與退出指標皆為 null。","side_b":"90 天以上逾期率 ≥4.0% 減碼一半，連兩季清倉；再進場條件為 Atome 獲批且 2027 年 Adj. EBITDA 指引不低於 11 億美元，或股價回落至 2.74 附近而指引未下修。","ruling":"前份門檻原文不可得，本次全部重新設定，無法判斷與前份差異；前份觸發器是否發火也無從逐條核對，繼承前份的欄位留空。","evidence_level":"前份摘要資料缺口"},{"axis":"Single Thing 重設","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份摘要未附唯一致命點原文（null）。","side_b":"公司正式下修 2028 年金融服務 5 億美元 EBITDA 目標，或 90 天以上逾期率單季升破 4.0%。","ruling":"以數學敏感度選定 Single Thing：金融服務占 2028 年目標 29%，若只達 1.5 億美元，集團 EBITDA 少約兩成，大於印尼 Ojol（占出行 GMV 6%）的直接影響。","evidence_level":"公司目標與法說（2026-11-03、2026-08-04）","settle_metric":"每季 90 天以上逾期率與 2028 年目標是否維持"},{"axis":"調整後 FCF 與簡單 FCF","side_a":"CFO：自由現金流幾乎翻倍，第三季 Adj. FCF 2.86 億美元、TTM 5.33 億。","side_b":"第三季 OCF 5,500 萬、資本支出 7,100 萬，簡單 FCF −1,200 萬；TTM FCF 利潤率 −0.45%，四家同業為 12.91%～31.81%。","ruling":"可調和：差額主要是放款擴張，放款是有利息收入的資產，不是營運虧損；但它也是真實資本投入，Adj. FCF 不能當作可分配現金。","evidence_level":"公司調節表","settle_metric":"金融服務的公司資本需求與銀行占放款比重，事實表未涵蓋","if_then":["若扣除銀行存款後淨現金轉負，停止加碼。","若銀行占放款比重上升且簡單 FCF 轉正，分批反買補足保留部位。"]},{"axis":"第四季指引隱含 EBITDA 約略不變","side_a":"CFO 歸因於旺季投資、司機補貼與新產品行銷，屬刻意選擇。","side_b":"指引隱含第四季 EBITDA 與第三季相近，連續擴張的斜率放緩；FY2027 共識 EPS 也與 FY2026 同為 0.14。","ruling":"可調和，但歸因未證、需監測，不採信也不否定。","evidence_level":"管理層說法，尚無後續數據","settle_metric":"2027 年第一、二季 Adj. EBITDA 利潤率","if_then":["若 2027 年第一、二季 Adj. EBITDA 利潤率連兩季低於 20%，季節性投資的說法視為不成立，減碼三分之一。"]},{"axis":"管理層前後說法","side_a":"2026-08-04 法說：CFO 稱 foodpanda 台灣進度符合預期、年底前完成；COO 稱全年指引假設 Ojol 佣金結構維持現行。","side_b":"2026-11-03 法說：CFO 說否決結果「we were anticipating it」；CEO 說印尼兩輪車新佣金框架 7 月已生效，早於 8 月那場法說。","ruling":"可調和。財務承諾都兌現：出行利潤率 8.9% 落在 8.5%～9%、金融服務提前轉盈、指引兩度上修。併購與監管的口徑偏樂觀，要自行打折。Ojol 佣金的說法可能指新框架實施後的現行結構，摘錄不足以確認。","evidence_level":"兩場法說逐字稿","settle_metric":"Atome 審批時程與印尼準則內容"},{"axis":"監管影響的時間範圍","side_a":"COO：不預期印尼新準則對指引有實質影響。","side_b":"指引只涵蓋到 2026 年底，只剩兩個月；準則細節尚未公布，影響落在 2027 年以後。第一季與第三季管理層都提到燃油與印尼法規逆風。","ruling":"不可裁決至準則細節公布。管理層的說法不能當作風險解除，保留一半部位等待。","evidence_level":"法說逐字稿，決勝資料尚不存在","settle_metric":"印尼外送準則內容；出行與外送分部利潤率","if_then":["若準則公布後出行利潤率連兩季低於 8.5%，減碼三分之一。","若準則公布後 2027 年指引未受影響，分批反買補足保留部位。"],"evidence_refs":["supply_demand_durability#2","regulatory_antitrust#1","regulatory_antitrust#4"]},{"axis":"賣方目標價","side_a":"賣方平均目標價 5.82～6.01 美元，較現價高 71%～76%，最高 8、最低 4.6，高低比 1.7 倍。","side_b":"本次 12 個月約 4.20、24 個月約 5.20；五月 Mizuho、JPMorgan 下調目標價，當時指引尚未上修。","ruling":"方向支持，幅度不採。賣方目標隱含約 28 倍 FY2028E EPS，高於目前 24.4 倍；高低比未達 2.5 倍，不必因分歧下調信心。五月的下調已被之後兩次指引上修蓋過。","evidence_level":"賣方彙整，日期不一","settle_metric":"第三季財報後目標價更新","evidence_refs":["capital_markets_pricing#4"]},{"axis":"產業態勢","side_a":"競爭面：對手名單長、印尼補貼戰持續，沒有 2026 年份額資料。","side_b":"結構面：S&P 升評至 BB、展望正面，三大分部全部獲利。其他結構變數在監管：台灣否決併購、印尼新佣金框架生效、反壟斷機關持續審視。","ruling":"雙向拉鋸：執行面轉好，定價與併購空間被監管壓縮。","evidence_level":"評級機構與 20-F","settle_metric":"On-Demand 抽成是否守住 13%"},{"axis":"現在就賣的最強論證","side_a":"股價仍在 250 週均線 3.79 下方；放款一年變三倍，逾期率的分母剛放大；FY2027 共識 EPS 零成長；Atome 規模不明而消費信貸風險最高；兩週已反彈約 22%。","side_b":"現價只要五年 EPS 年化約 17%、終端 18 倍就有 10% 年報酬，金融服務提前轉盈，淨現金與 9 億美元回購提供下檔支撐。","ruling":"可調和。賣的論證中以放款分母問題最有力，已列為唯一致命項，其餘反映在 30% 空頭機率，暫不賣。","evidence_level":"財報、共識與週線資料","settle_metric":"逾期率、2027 年指引、股價是否站回 3.79","if_then":["若股價續漲到 4.44 而逾期率與印尼準則都沒有新資料，不追。","若股價跌破 2.74 而指引未下修，分批反買。","若股價跌破 2.74 且指引下修、逾期率升破 3.5%，停止加碼。"]}],"triggers":[{"n":1,"text":"金融服務信用事件：90 天以上逾期率單季升破 4.0%，或公司下修 2028 年金融服務 5 億美元目標。","type":"Single Thing","maps_to":"Single Thing","metric":"90 天以上逾期率；2028 年金融服務 EBITDA 目標","threshold":"≥4.0%，或目標下修","action":"減碼一半；連兩季仍 ≥4.0% 則清倉","source_freq":"每季財報補充資料","date":"2027-02","evidence_refs":["regulatory_antitrust#0"]},{"n":2,"text":"2027 年指引檢驗利潤率路徑。","type":"假設驗證","maps_to":"H1","metric":"FY2027 Adj. EBITDA 指引","threshold":"低於 10 億美元","action":"停止加碼","source_freq":"年度指引","date":"2027-02"},{"n":3,"text":"逾期餘額增速領先放款增速，提前警示信用成本。","type":"假設驗證","maps_to":"H2","metric":"90 天以上逾期餘額增速減放款增速","threshold":"連兩季為正","action":"停止加碼","source_freq":"每季財報補充資料","date":"2027-05"},{"n":4,"text":"司機分潤法規或補貼吃掉出行利潤率。","type":"風險","maps_to":"R2","metric":"出行分部利潤率","threshold":"連兩季低於 8.5%","action":"減碼三分之一","source_freq":"每季財報","date":"2027-02","evidence_refs":["regulatory_antitrust#4","regulatory_antitrust#1"]},{"n":5,"text":"印尼 KPPU 對司機合作安排或 P2P 利率卡特爾作出不利裁定；屬行政程序，受影響營收事實表未涵蓋，裁定日未知。","type":"風險","maps_to":"R2","metric":"裁定罰款與營運限制","threshold":"罰款超過 1 億美元，或要求改變司機合作安排","action":"減碼三分之一","source_freq":"KPPU 公告、年報法律程序章節","date":null,"evidence_refs":["regulatory_antitrust#0","major_events#1"]},{"n":6,"text":"誘因長期化，定價權進一步流失。","type":"風險","maps_to":"R3","metric":"誘因占 On-Demand GMV","threshold":"連四季高於 11.5%（第一季 10.5%）","action":"減碼三分之一","source_freq":"每季財報","date":"2027-11","evidence_refs":["supply_demand_durability#2"]},{"n":7,"text":"兩個具名不確定事件落地，解鎖保留的一半部位。","type":"加碼","maps_to":"H2","metric":"Atome 審批；印尼外送準則","threshold":"Atome 獲批，且準則公布後 2027 年指引未受影響","action":"補足保留的一半部位","source_freq":"公司公告、法說","date":"2027"},{"n":8,"text":"股價先行兌現基本情境的中期價值。","type":"減碼","maps_to":"H1","metric":"股價","threshold":"≥6.30 美元（FY2028E EPS 0.21 的 30 倍）","action":"減碼三分之一","source_freq":"每日","date":null},{"n":9,"text":"再進場條件。","type":"估值rearm","maps_to":"H1","metric":"Atome 審批、2027 年指引、股價","threshold":"Atome 獲批且 2027 年 Adj. EBITDA 指引不低於 11 億美元；或股價回落至 2.74 附近而指引未下修","action":"重跑研究後分批建倉","source_freq":"法說、每日股價","date":"2027-02"},{"n":10,"text":"第四季財報後全面複審。","type":"複審日期","maps_to":"H1","metric":"2026 年第四季財報與 2027 年指引","threshold":"財報發布","action":"重跑研究","source_freq":"一次性","date":"2027-02"},{"n":11,"text":"資本緩衝消失且信用惡化同時發生。","type":"清倉","maps_to":"R4","metric":"扣除銀行存款後淨現金；90 天以上逾期率","threshold":"淨現金轉負且逾期率 ≥4.0%","action":"清倉","source_freq":"每季財報","date":null}],"kill_metrics":[{"metric":"放款組合 90 天以上逾期率","bear_threshold":"單季 ≥4.0%（第三季 2.6%）","window":"2026 年第四季至 2028 年第四季","source":"每季財報補充資料","last_status":"ok"},{"metric":"出行分部利潤率","bear_threshold":"連兩季低於 8.5%（第三季 8.9%）","window":"2026 年第四季起","source":"每季財報","last_status":"ok"},{"metric":"外送分部利潤率同比變化","bear_threshold":"連兩季同比下滑（第三季 2.7%，去年同期 2.1%）","window":"2026 年第四季起","source":"每季財報","last_status":"ok"},{"metric":"誘因占 On-Demand GMV","bear_threshold":"連四季高於 11.5%（2026 年第一季 10.5%）","window":"2026 年第四季至 2027 年第四季","source":"每季財報；第三季數字事實表未涵蓋","last_status":"unknown"},{"metric":"FY2027 Adj. EBITDA 指引","bear_threshold":"低於 10 億美元","window":"2026 年第四季法說","source":"公司年度指引","last_status":"unknown"},{"metric":"扣除銀行存款後淨現金","bear_threshold":"轉負（目前約 11.3 億美元，以淨現金 38.27 億減存款 27 億估算）","window":"Atome 完成後每季","source":"每季資產負債表","last_status":"ok"}],"evidence_dismissed":[],"action_conditions":{"rearm_trigger":"Atome 獲批且 2027 年 Adj. EBITDA 指引不低於 11 億美元；或股價回落至 2.74 附近而指引未下修","exec_line":"首筆不超過計畫部位一半，理由是股價兩週內由約 2.79 彈到 3.41，不追高。其餘一半等印尼外送準則細節公布且 Atome 審批有結果才加。股價跌破 2.74 而指引未下修則分批反買，指引下修則停止加碼。股價到 6.30（FY2028E EPS 0.21 的 30 倍）減碼三分之一。週線仍在 250 週均線 3.79 下方；若 2027 年 5 月前未站回且第一季指引下修，視為趨勢訊號正確，停止加碼。"}},"decision_inputs":{"signal":"B","ma":"❌","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場把放款擴張吃掉的現金當成本業燒錢（簡單 FCF −1,200 萬美元、Adj. FCF 2.86 億），並對 2028 年 17 億美元 EBITDA 打很深的折；即使用較高的 EV，目標打八折也只有約 9.3 倍。","momentum_overheated":null,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":null,"wait_for_price_condition":null},"thesis":{"H":[{"id":"H1","text":"營運槓桿帶動集團利潤率續升，2028 年調整後 EBITDA 至少達公司目標的八成。","2y":"FY2027 不低於 11 億美元，FY2028 不低於 14 億美元","5y":null,"10y":null,"threshold":"FY2027 Adj. EBITDA ≥11 億美元；FY2028 ≥14 億美元（公司目標 17 億）","source":"每季財報、年度指引","drift_rule":"TTM 較路徑偏離 5% 以上連兩季為削弱；偏離 10% 以上連三季為反轉。"},{"id":"H2","text":"金融服務規模放大而信用成本受控，成為第三個獲利引擎。","2y":"2028 年放款組合不低於 60 億美元、分部 EBITDA 不低於 3 億美元","5y":"FY2031 分部 EBITDA 不低於 6 億美元，90 天以上逾期率不高於 3.5%","10y":null,"threshold":"90 天以上逾期率 ≤3.5%；2028 年分部 EBITDA ≥3 億美元（公司目標 5 億）","source":"季報補充資料的逾期率與風險調整後報酬","drift_rule":"2 年期連兩季偏離 5% 以上削弱、連三季偏離 10% 以上反轉；5 年期連四季偏離 5% 以上削弱、連六季偏離 10% 以上反轉。"},{"id":"H3","text":"網絡密度維持領先，外送與出行利潤率兌現，AI 與自駕留在平台內。","2y":"FY2028 外送分部利潤率不低於 3.5%，出行維持 8.5%～9%","5y":"外送分部利潤率不低於 4%，On-Demand 抽成不低於 13%","10y":"自駕與人車混合派單仍由 Grab 協調，外部自駕業者需要其入口","threshold":"外送分部利潤率逐年上升，出行不低於 8.5%，On-Demand 抽成不低於 13%","source":"季報分部資料，S&P 預期抽成 13%～15% 作為外部對照（口徑可能不同）","drift_rule":"5 年期連四季偏離 5% 以上削弱、連六季偏離 10% 以上反轉；10 年期跨兩個年度削弱、跨三個年度反轉。"}],"R":[{"id":"R1","text":"放款一年變三倍，逾期率的分母剛放大，Atome 再把風險推向無擔保消費信貸。","h_ref":"H2","clock":"🔥","threshold":"90 天以上逾期率 ≥4.0%，或逾期餘額增速連兩季高於放款增速","evidence_refs":["regulatory_antitrust#0","major_events#1"]},{"id":"R2","text":"印尼兩輪車佣金框架已生效、外送準則待公布，馬來西亞零工法與 RM160 百萬福利方案上路，新增法規與稅負是持續風險，反壟斷機關持續審視；菲律賓競爭委員會的 800 萬披索罰款金額小，但印證審查強度。","h_ref":"H3","clock":"⚡","threshold":"出行分部利潤率連兩季低於 8.5%，或外送分部利潤率連兩季同比下滑","evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#1","regulatory_antitrust#4","major_events#1","major_events#2","product_recall_warning#0","reg_tariff_export#1"]},{"id":"R3","text":"油價推高司機成本，誘因與補貼長期化，對手低價競爭使定價權難以恢復；第一季誘因占 On-Demand GMV 10.5%。","h_ref":"H1","clock":"🔥","threshold":"誘因占比連四季高於 11.5%","evidence_refs":["supply_demand_durability#2","competitive_share_entrants#0","end_markets#2"]},{"id":"R4","text":"Atome 併購規模不明，加上 5 億美元回購、放款投入與自駕投資，淨現金可能快速下降；CFO 未回答放款需要多少公司資本。","h_ref":"H2","clock":"🔥","threshold":"扣除銀行存款後淨現金轉負"},{"id":"R5","text":"AI 代理與自駕改變入口，AI 侵權主張與雲端中斷是營運尾部風險。","h_ref":"H3","clock":"🐢","threshold":"代理訂單占外送 GMV 超過 20% 且廣告占比下滑","evidence_refs":["substitute_technology#0","substitute_technology#1","geo_supply_chain#1"]},{"id":"R6","text":"幾乎全部營收在東南亞，區域政治與總體波動無法分散。","h_ref":"H1","clock":"🐢","threshold":"On-Demand GMV 固定匯率年增率連四季低於 10%","evidence_refs":["geo_supply_chain#0"]}],"single_thing":{"description":"公司正式下修 2028 年金融服務 5 億美元 EBITDA 目標，或 90 天以上逾期率單季升破 4.0%（第三季 2.6%）。","why_fatal":"這是數學上最大的單一敏感項：金融服務占 2028 年 17 億美元目標的 29%。若只達 1.5 億，集團 EBITDA 少 3.5 億，約兩成，還會同時帶走市場對放款擴張與淨現金的信任。","if_happens":"減碼一半；若連兩季逾期率仍在 4.0% 以上，清倉。","how_monitor":"每季財報補充資料的逾期率與風險調整後報酬；Atome 併入後分開看消費信貸與司機商家放款；逾期餘額增速連兩季高於放款增速作為提前警示。","probability":"20%～25%（12～24 個月）。依據是放款年增 200%，事實表沒有歷史壞帳序列，屬判斷值。"}},"appendix_a":{"growth_durability":7,"quality_score":6,"ai_risk":"🟡","long_term_confidence":"中","fpe_fy2":24.36,"peg_fy2":1.08,"stress":{"pass":2,"total":3}},"eps_meta":{"base_eps_path":{"FY2025A":0.06,"FY2026E":0.14,"FY2027E":0.14,"FY2028E":0.21},"fy_end_month":12,"eps_basis":"FY2025A 為年報稀釋 EPS；FY2026E 至 FY2028E 為 Koyfin 共識快照（2026-11-07），財年 12 月底。共識是否全為 IFRS 口徑事實表未說明。"},"catalysts":[{"date":"2027-02","date_precision":"month","type":"guidance","event":"2026 年第四季財報與 2027 年指引（月份為估計）","impact":"高","watch":"FY2027 Adj. EBITDA 指引是否不低於 11 億美元，以及 90 天以上逾期率。"},{"date":"2026-Q4","date_precision":"quarter","type":"regulatory","event":"印尼外送與物流準則細節公布（時點未定，管理層稱細節開始浮現）","impact":"高","watch":"司機分潤與費用透明的具體規定，對外送利潤率的影響。"},{"date":"2027","date_precision":null,"type":"regulatory","event":"Atome 併購審批，CFO 稱目標在明年完成","impact":"高","watch":"交易金額、付款方式與 2028 年目標是否維持。"},{"date":"2027-09","date_precision":"month","type":"other","event":"9 億美元回購計畫的完成期限，買回股份將註銷","impact":"中","watch":"剩餘 5 億美元的執行速度與均價。"},{"date":"2026-Q4","date_precision":"quarter","type":"product","event":"新加坡自駕服務開始商業收費","impact":"低","watch":"車隊擴充與派單整合進度，短期不影響獲利。"}],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8(val爭議)","pacing":["row4：週線❌，進場節奏強制分批（starter 1/3＋趨勢確認後加碼），頁首掛「⚠️ 週線趨勢未確認，逢回分批勿接刀」"],"holding_cap":null,"audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":true,"basis":"ma='❌'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"輸入缺(momentum_overheated=null)，依保守方向處理：不視為觸發","input_gap":["momentum_overheated"]},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場把放款擴張吃掉的現金當成本業燒錢（簡單 FCF −1,200 萬美元、Adj. FCF 2.86 億），並對 2028 年 17 億美元 EBITDA 打很深的折；即使用較高的 EV，目標打八折也只有約 9.3 倍。"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟢', val='🟡', moat_trend='→', week26=-8.33, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position=None, moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈機械讀數判定不可用，baseline rows 8/9/9b/10 的估值條件視為不可判 → 落 row8 觀望（保守方向）","hit":true,"basis":"val_denominator_disputed=True, val(機械讀數)='🟡'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"requires_critic":[]}}
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
