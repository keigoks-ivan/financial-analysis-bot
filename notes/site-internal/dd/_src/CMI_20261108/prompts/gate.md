你是 DD 管線 v20 的判斷層閘（gate），標的 CMI（20261108）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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
- `f_kpi0_revenue_gaap`（q1_business）｜Revenue (GAAP)＝9438 USD m｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 8-K Ex.99 (cmi2026q38-kex99.htm)（numbers.latest_quarter_kpis.items[0]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-11-05））
  - 註記：未查證
- `f_kpi1_ebitda_margin_non_gaap`（q1_business）｜EBITDA margin（公司主要口徑；公司不報 Non-GAAP 營業利益）＝18.9 %｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 8-K Ex.99；EBITDA 1,786 USD m（numbers.latest_quarter_kpis.items[1]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-11-05））
  - 註記：未查證
- `f_kpi2_gaap_operating_income`（q1_business）｜GAAP operating income＝1444 USD m（利益率 15.3%）｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 8-K Ex.99（numbers.latest_quarter_kpis.items[2]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-11-05））
  - 註記：未查證
- `f_kpi4_guidance_fy2026_revenue_`（q1_business）｜Guidance: FY2026 revenue growth＝約 +10% YoY｜期間與口徑：Q3 FY2026 公告（2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司新聞稿 8-K Ex.99（numbers.latest_quarter_kpis.items[4]，as_of Q3 FY2026 公告（2026-11-05））
  - 註記：FY1 營收共識 37,168 USD m（yfinance，見 capital_structure）；未對照指引隱含值
- `f_kpi5_guidance_fy2026_ebitda_m`（q1_business）｜Guidance: FY2026 EBITDA margin＝約 18.2% %｜期間與口徑：Q3 FY2026 公告（2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司新聞稿 8-K Ex.99（不含 Q1 低壓燃料電池事業出售 199 USD m 損失）（numbers.latest_quarter_kpis.items[5]，as_of Q3 FY2026 公告（2026-11-05））
  - 註記：未查證
- `f_peer_cmi_gross_margin_pct`（q2_moat）｜CMI 毛利率＝25.88 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CMI.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_cmi_operating_margin_pct`（q2_moat）｜CMI 營業利益率＝11.79 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CMI.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_cat_operating_margin_pct`（q2_moat）｜CAT 營業利益率＝18.33 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CAT.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_pcar_operating_margin_pct`（q2_moat）｜PCAR 營業利益率＝10.75 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.PCAR.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_alsn_operating_margin_pct`（q2_moat）｜ALSN 營業利益率＝18.88 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ALSN.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_gnrc_operating_margin_pct`（q2_moat）｜GNRC 營業利益率＝10.37 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.GNRC.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝29.59 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-11-07）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝34.81 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-11-07）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝40.69 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-11-07）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝37167.88 USD m｜期間與口徑：2026-11-08／yfinance revenue_estimate 0y 平均（12 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝40741.03 USD m｜期間與口徑：2026-11-08／yfinance revenue_estimate +1y 平均（18 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi3_free_cash_flow`（q4_capital）｜Free cash flow（營業現金流減資本支出，自算；公司未報）＝1102 USD m｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 8-K Ex.99：營業現金流 1,405、資本支出 303（numbers.latest_quarter_kpis.items[3]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-11-05））
  - 註記：未查證
- `f_peer_cmi_fcf_margin_pct`（q2_moat）｜CMI FCF 利潤率＝9.66 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CMI.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝3334.0 USD m｜期間與口徑：2026-11-08／yfinance 最新一季：總債務 7519.0、現金 4185.0（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝137.08 m shares｜期間與口徑：2026-11-08／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝1.822 %｜期間與口徑：2026-11-08／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-11-08）
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝450.07 USD｜期間與口徑：2026-11-06（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-11-06（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝15.21 x｜期間與口徑：2026-11-07／分母＝FY1 EPS 29.59，分子＝快照價 450.07｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-11-07）
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝18.78 x｜期間與口徑：2026-11-06（RTH 收盤，UTC）／4 個年度端點內的分位＝21.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-11-06（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝21.0 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝1.72 x｜期間與口徑：2026-11-06（RTH 收盤，UTC）／4 個年度端點內的分位＝65.4｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝65.4 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝1.81 x｜期間與口徑：2026-11-06（RTH 收盤，UTC）／4 個年度端點內的分位＝60.4｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝60.4 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝-0.24 %｜期間與口徑：2026-08-13 → 2026-11-07／FY1 共識 EPS 29.66 → 29.59（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-11-07）
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝-33.31 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-11-06（RTH 收盤，UTC））
- `f_rsi14`（q5_valuation）｜RSI(14)＝23.81｜期間與口徑：2026-11-06（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ma_state`（q5_valuation）｜週線均線六態（decision_inputs.ma 必須等於此值）＝🟠｜期間與口徑：2026-11-08／timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）
  - 原文：「price 450.07 / W52 577.57 / W104 464.79 / W250 327.19 / W250 13週斜率 1.46%」
- `f_ma_w250`（q5_valuation）｜250 週均線＝327.19 USD｜期間與口徑：2026-11-08／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）
- `f_consensus_rev_fy1_pct`（q5_valuation）｜FY1 共識修正＝0.0 %｜期間與口徑：2026-11-07／兩份 Koyfin 快照之間的 EPS 修正幅度（29.59 → 29.59）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.fy1.revision_pct，as_of 2026-11-07）

### findings_digest 中方向為負或來源衝突的條目（22 條）
- `competitive_share_entrants#1`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K 風險因子：替代技術（天然氣、氫、電動）持續發展，公司將面對這些新技術帶來的新競爭；新興市場客戶出口後可能與公司既有客戶競爭。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-10）｜affects：moat_trend、decision_inputs.bear
- `customer_second_source#0`（customer_second_source｜方向 -｜狀態 ok）：PACCAR為最大客戶，占2025合併銷售13%（2024、2023為16%）；長約不保證特定數量；失去該客戶或PACCAR產量大降會有不利影響。
  - 來源：SEC EDGAR 10-K FY2025 Item 1（as_of 2026-02-10）｜affects：thesis.R、decision_inputs.bear
- `customer_second_source#1`（customer_second_source｜方向 -｜狀態 ok）：10-K風險因素載明部分現有客戶可能自行開發或改向其他製造商採購（電動化動力系統情境）。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-10）｜affects：moat_trend、thesis.R
- `customer_concentration_credit#0`（customer_concentration_credit｜方向 -｜狀態 ok）：PACCAR 為 CMI 最大客戶，2025 年占合併淨銷售 13%（2024、2023 各 16%），是唯一超過 10% 的客戶；供應協議不保證特定數量，失去該客戶或其車款產量大減將對營運與財務產生不利影響。
  - 來源：SEC EDGAR 10-K FY2025 Item 1 Business（as_of 2026-02-10）｜affects：thesis.R、decision_inputs.bear
- `supply_demand_durability#3`（supply_demand_durability｜方向 -｜狀態 ok）：風險面：分析師點出重/中型卡車週期長期低迷、競爭加劇（Caterpillar 發電銷售增 72%、Generac 資料中心積壓約 16 億美元）、EPA27 與關稅不確定
  - 來源：rallies.ai / Nasdaq (Generac backlog) 摘要（as_of 2026-08-01）｜affects：decision_inputs.bear、thesis.R
- `regulatory_antitrust#0`（regulatory_antitrust｜方向 -｜狀態 ok）：Cummins 2023 年 12 月與 EPA、CARB、DOJ、加州檢察長就皮卡引擎排放認證達成和解，2024 年 4 月生效，2024 Q2 付 19 億美元；10-K 稱仍可能有額外監管行動與附帶訴訟。屬環保執法，非反壟斷。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A Risk Factors（as_of 2026-02-10）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：10-K 風險因子：Cummins 依賴全球供應鏈，關稅與貿易中斷（禁運、制裁、出口管制）可能衝擊生產成本、需求與客戶／供應商關係；美中出口管制與制裁變動可能影響應收帳款回收、中國現金調回、售後與保固支援及銷售。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-10）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#2`（reg_tariff_export｜方向 -｜狀態 ok）：MD&A 展望：關稅、出口管制與地緣緊張帶來不確定性，成本與關稅上升可能衝擊獲利，貿易中斷可能造成生產中斷。
  - 來源：SEC EDGAR 10-K FY2025 Item 7 Outlook（as_of 2026-02-10）｜affects：decision_inputs.bear、triggers
- `reg_tariff_export#3`（reg_tariff_export｜方向 -｜狀態 ok）：Q3 2025 財報電話會議：關稅成本於第三季上升，接近完全回收先前公布的關稅；單季淨衝擊為數千萬美元級。
  - 來源：Motley Fool Q3 2025 earnings call transcript（as_of 2025-11-06）｜affects：thesis.R
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：Q3 2026 10-Q：主要風險含全球貨運減少、供應商與終端成本上升、供應可得性不確定；稱關稅淨影響 Q1 不重大；並稱 single source 多項關鍵零件與原料
  - 來源：Cummins 10-Q 2026-09-30（as_of 2026-11-03）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：10-K 歷年風險因子：易受單一來源供應商短缺影響
  - 來源：Cummins 10-K FY2020（as_of 2021-02-15）｜affects：thesis.R
- `end_markets#1`（end_markets｜方向 -｜狀態 ok）：全年營收成長指引由 10–13% 下修至約 10%，主因北美皮卡需求疲弱；發電與重型卡車需求仍強。
  - 來源：Cummins Q3 2026 新聞稿彙整（investingnews）（as_of 2026-11-03）｜affects：thesis.R、valuation
- `substitute_technology#2`（substitute_technology｜方向 -｜狀態 ok）：Caterpillar 發電銷售成長 72%，大型發電機組與渦輪用於資料中心，競爭壓力增加
  - 來源：Equipment World: Caterpillar, Cummins, Rehlko generators power data center boom（as_of 2026-05-01）｜affects：moat_trend、thesis.R
- `capital_markets_pricing#0`（capital_markets_pricing｜方向 -｜狀態 ok）：2026-11-05 Q3 後公司把全年營收成長指引由 10–13% 收窄為約 10%（北美皮卡需求弱），EBITDA margin 約 18.2% 仍在原 18–18.5% 區間；Q3 營收約 $9.44B 低於市場預期約 $9.87B，EPS $8.25 與共識 $8.28 約當（聚合摘要，未逐字核對 8-K）。5 月、8 月曾兩度上修。
  - 來源：SEC 8-K Q3 2026 exhibit 99 / 搜尋摘要（as_of 2026-11-05）｜affects：thesis.R、valuation、triggers
- `major_events#1`（major_events｜方向 -｜狀態 ok）：NHTSA 對 Cummins 召回 campaign 26E066（L9 燃油濾清器油管可能鬆脫漏油）發出受理函，約39,052件；車主通知預計2026-11-20寄出。為召回受理函，非 warning letter。
  - 來源：NHTSA RCAK-26E066 acknowledgment letter（as_of 2026-09-30）｜affects：decision_inputs.bear
- `major_events#2`（major_events｜方向 -｜狀態 ok）：2026年3月 NHTSA 召回 26E011000：Cummins PD7000 電驅單元軟體錯誤可能造成非預期移動（約411~413台）。
  - 來源：vehiclesafetyrecalls.com NHTSA 26E011000（as_of 2026-03-13）｜affects：decision_inputs.bear
- `major_events#3`（major_events｜方向 -｜狀態 ok）：2024年起的證券集體訴訟 Baker v. Cummins（C.D. Cal.），涉及排放認證／defeat device，期間2019-04-30至2023-12-21；搜尋所見為2024年律所公告，目前進度未核實。
  - 來源：Kessler Topaz Meltzer Check notice (BusinessWire)（as_of 2024-03-04）｜affects：decision_inputs.bear
- `cyclical_prior_downcycle_behavior#0`（cyclical_prior_downcycle_behavior｜方向 -｜狀態 ok）：2008Q4（上一輪衰退起點）EBIT 率由 9.2% 降到 3.9%（排除重整費用 5.0%）；公司 2009 年初指引銷售降約 20%、EBIT 率 6.5%
  - 來源：Cummins press release 2009-02-03 (8-K)（as_of 2009-02-03）｜affects：decision_inputs.bear、valuation
- `cyclical_prior_downcycle_behavior#2`（cyclical_prior_downcycle_behavior｜方向 -｜狀態 ok）：2019 年 Class 8 產量九個月內下降 55%，高階主管稱 18 年來未見；ACT 稱高峰通常持續約 13-15 個月
  - 來源：ACT Research / trucknews.com（as_of 2019-06-01）｜affects：decision_inputs.bear
- `lawsuit_class_action#0`（lawsuit_class_action｜方向 -｜狀態 ok）：證券集體訴訟 Baker v. Cummins（C.D. Cal.）針對排放認證事件，為2024年提起之舊案，現況未核實；10-K 稱公司面臨日常訴訟。
  - 來源：Kessler Topaz Meltzer Check notice (BusinessWire)（as_of 2024-03-04）｜affects：decision_inputs.bear
- `product_recall_warning#0`（product_recall_warning｜方向 -｜狀態 ok）：NHTSA campaign 26E066：L9 燃油濾清器油管可能鬆脫漏油，約39,052件，受理函日期2026-09-30。
  - 來源：NHTSA RCAK-26E066 acknowledgment letter（as_of 2026-09-30）｜affects：decision_inputs.bear
- `product_recall_warning#1`（product_recall_warning｜方向 -｜狀態 ok）：NHTSA campaign 26E011000：PD7000 電驅單元軟體錯誤可能造成非預期移動。
  - 來源：vehiclesafetyrecalls.com NHTSA 26E011000（as_of 2026-03-13）｜affects：decision_inputs.bear

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 11 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CMI_20261108/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":1085.0,"bear_5y_price":313.5,"p_bull_pct":20,"p_bear_pct":30,"upside_5y_pct":49.3,"ev5y_pct":43.8,"irr_base_pct":8.3,"asym_ratio":3.1,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":29.59,"pe":15.21,"basis":"FY2026E 共識 EPS（FY1），現價 450.07 美元；終端倍數同樣用當年度 EPS 當分母。"},"eps":{"bull":[36.0,43.0,50.0,56.0,62.0],"base":[33.5,38.0,42.0,45.0,48.0],"bear":[30.0,26.5,24.0,26.5,28.5]},"pe":{"bull":17.5,"base":14,"bear":11},"p":{"bull":20,"base":50,"bear":30},"yield_pct":{"dividend":1.822,"net_buyback":1.0},"second_stage":{"bull_cagr_pct":9,"base_cagr_pct":6},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### CMI_Q2_2026_Earnings_Call_20260804.md
- 2026-08-04｜Jennifer Rumsey (CEO)｜guidance：全年營收財測上調至 +10%~13%（前次 8%~11%）（原話："total company revenues to increase 10% to 13% in 2026"）
- 2026-08-04｜Jennifer Rumsey (CEO)｜guidance：全年 EBITDA 率財測中點上調至 18%~18.5%（原話："midpoint of our EBITDA guidance to a range of 18% to 18.5%."）
- 2026-08-04｜Jennifer Rumsey (CEO)｜guidance：北美重型卡車 2026 預測 24~25 萬輛（前次 23~25 萬）（原話："up from our prior guidance of 230,000 to 250,000"）
- 2026-08-04｜Jennifer Rumsey (CEO)｜guidance：全球發電營收維持 +15%~25%，成長受產能限制（原話："growth in 2026 will continue to be constrained by capacity."）
- 2026-08-04｜Jennifer Rumsey (CEO)｜guidance：中國營收（含合資）預期約 +15%（前次 +10%）（原話："to increase approximately 15% in 2026"）
- 2026-08-04｜Jennifer Rumsey (CEO)｜guidance：採礦引擎銷售預期下修至 -5%~+5%（前次持平~+10%）（原話："engine sales to range from down 5% to up 5% for the year"）
- 2026-08-04｜Mark Smith (CFO)｜guidance：Accelera 2026 淨損預期 2.6~2.9 億美元（前次 2.7~3.0 億）（原話："prior guide of a negative $270 million to $300 million."）
- 2026-08-04｜Mark Smith (CFO)｜guidance：年度資本支出區間（原話："range of $1.35 billion to $1.45 billion"）
- 2026-08-04｜Mark Smith (CFO)｜guidance：全年有效稅率約 23%（不含離散項）（原話："effective tax rate is expected to be approximately 23%"）
- 2026-08-04｜Jennifer Rumsey (CEO)｜margin：Q2 EBITDA 率 17.5%，去年同期 18.4%（原話："EBITDA for the quarter was a record $1.7 billion or 17.5%"）
- 2026-08-04｜Mark Smith (CFO)｜margin：Q2 毛利率 26.1%（去年 26.4%）（原話："Gross margin for the quarter was $2.5 billion or 26.1%"）
- 2026-08-04｜Mark Smith (CFO)｜margin：Q2 關稅淨影響對 EBITDA 金額不重大（原話："The net impact of tariffs was immaterial to EBITDA dollars"）
- 2026-08-04｜Mark Smith (CFO)｜margin：獎金提列：下半年每季較 Q2 低約 2,500 萬美元（原話："a quarter lower in Q3 and Q4 than the Q2 expense."）
- 2026-08-04｜Mark Smith (CFO)｜margin：明年獎金重設至目標，規模約 2 億美元（原話："next year, it could be in the order of like $200 million."）
- 2026-08-04｜Mark Smith (CFO)｜margin：Components 分部 EBITDA 率財測區間下限不變、上限下調（原話："compared to our prior guide of 13.5% to 14.5%."）
- 2026-08-04｜Mark Smith (CFO)｜margin：Distribution 分部 EBITDA 率財測較前次中點下調（原話："range of 13.5% to 14.25% compared to our previous"）
- 2026-08-04｜Mark Smith (CFO)｜margin：Power Systems EBITDA 率財測中點較前次 25.5% 上移但含下半年投資（原話："compared to our previous guide of 25.5% at the midpoint,"）
- 2026-08-04｜Mark Smith (CFO)｜margin：Distribution 利潤率受獎金影響較大的原因之一為零件業務成長較慢（原話："the parts business isn't growing at the same rate"）
- 2026-08-04｜Mark Smith (CFO)｜margin：下半年無一次性項目、EBITDA 率預期高於上半年（原話："there's no onetime or anything"）
- 2026-08-04｜Mark Smith (CFO)｜margin：Power 增量利潤率優於預期的主因（原話："stronger demand in China, which helps on the JV earnings"）
- 2026-08-04｜Mark Smith (CFO)｜margin：保固成本目前約佔營收低 2%（原話："warranty costs are running in the low 2% of sales range"）
- 2026-08-04｜Mark Smith (CFO)｜margin：新平台上市通常伴隨較高保固提列（原話："those come with a higher warranty accrual"）
- 2026-08-04｜Jennifer Rumsey (CEO)｜product：EPA 2027 草案下 X15 量產時程（原話："production expected to begin in the fourth quarter of 2027."）
- 2026-08-04｜Jennifer Rumsey (CEO)｜product：X10 限量生產與量產時程（原話："with full production expected by the third quarter of 2027"）
- 2026-08-04｜Jennifer Rumsey (CEO)｜product：新一代 B 平台 2028 年 1 月上市（原話："B platform is expected to launch in January 2028"）
- 2026-08-04｜Jennifer Rumsey (CEO)｜product：宣布開發 130 公升天然氣發電機組，切入主電力市場（原話："development of 130-liter natural gas genset"）
- 2026-08-04｜Jennifer Rumsey (CEO)｜product：較長的限量生產過渡期是過去沒有過的（原話："is something that we've not had in the past."）
- 2026-08-04｜Jennifer Rumsey (CEO)｜commitment：與超大規模雲端客戶簽多年協議，涵蓋數 GW 備援發電機需求（原話："several gigawatts of future backup power genset demand"）
- 2026-08-04｜Jennifer Rumsey (CEO)｜commitment：分析師日宣布新增 20 GW 產能，明年部分上線、2028 年大幅增加（原話："investment in capacity, 20 gigawatt incremental"）
- 2026-08-04｜Jennifer Rumsey (CEO)｜commitment：產能增幅預期：2028 年為較大一步（原話："the bigger step-up happening in '28"）
- 2026-08-04｜Mark Smith (CFO)｜capital_allocation：Q2 回饋股東約營運現金流 50% 的長期承諾（原話："commitment to return approximately 50% of operating"）
- 2026-08-04｜Mark Smith (CFO)｜capital_allocation：Q2 買回與股息金額（原話："$225 million of share repurchases and $276 million in cash"）
- 2026-08-04｜Mark Smith (CFO)｜capital_allocation：董事會批准季度股息增加 10%（原話："approved a 10% increase in our quarterly cash dividend"）
- 2026-08-04｜Jennifer Rumsey (CEO)｜customer：Q2 中國發電設備銷售 +88%，資料中心需求加速（原話："Sales of power generation equipment in China increased 88%"）
- 2026-08-04｜Mark Smith (CFO)｜customer：發電機組訂單已排到 2028 下半年（原話："it's going to be the second half of 2028."）
- 2026-08-04｜Mark Smith (CFO)｜customer：管理層稱需求無暫停（原話："absolutely no pausing or blinking in demand"）
- 2026-08-04｜Jennifer Rumsey (CEO)｜customer：積壓訂單描述（原話："So backlog is very strong."）
- 2026-08-04｜Jennifer Rumsey (CEO)｜competition：本十年發電營收仍以柴油備援為主（原話："predominant revenue for power gen this decade"）
- 2026-08-04｜Jennifer Rumsey (CEO)｜competition：對 NCP 與排放額度的看法：預期不會大量用額度抵 NCP（原話："there's going to be a kind of a big use of credits"）
- 2026-08-04｜Mark Smith (CFO)｜competition：Mark 稱能同時提供產品、服務與安裝的全球業者不多（原話："there are not many players in this segment"）
- 2026-08-04｜Jennifer Rumsey (CEO)｜risk：北美工程機械需求預期持平，理由為關稅與利率不確定（原話："given ongoing tariffs and"）
- 2026-08-04｜Jennifer Rumsey (CEO)｜risk：採礦：庫存偏高預期壓抑需求（原話："inventory levels and others are expected to moderate"）
- 2026-08-04｜Jennifer Rumsey (CEO)｜risk：中國下半年預期正常季節性放緩（原話："we expect normal seasonal moderation during the second half"）
- 2026-08-04｜Jennifer Rumsey (CEO)｜risk：中國挖掘機 Q2 受 OEM 備貨影響（原話："OEM inventory stocking to mitigate potential logistics risks"）
- 2026-08-04｜Jennifer Rumsey (CEO)｜risk：2027 年需求預期溫和回落，但不會像先前預期那麼劇烈（原話："it will not be as abrupt as we might have previously"）
- 2026-08-04｜Jennifer Rumsey (CEO)｜risk：2027 年不給具體財測（原話："we won't give specific guidance"）
- 2026-08-04｜Mark Smith (CFO)｜risk：研發費用因分階段轉換將維持較高更久（原話："our R&D costs will stay elevated for a little bit longer"）
- 2026-08-04｜Mark Smith (CFO)｜risk：2027 年保固與產品涵蓋成本低於全面 1/1 上市情境（原話："product coverage costs for next year would be lower than we"）
- 2026-08-04｜Mark Smith (CFO)｜risk：NCP 預期轉嫁市場（原話："we don't expect a significant financial impact from those"）
- 2026-08-04｜Jennifer Rumsey (CEO)｜risk：預購需求：預期持續到明年（原話："some prebuy is coming in"）
- 2026-08-04｜Jennifer Rumsey (CEO)｜risk：中型卡車財測納入略高的預購（原話："modestly higher prebuy following the recent regulatory"）
- 2026-08-04｜Jennifer Rumsey (CEO)｜risk：行業景氣描述為謹慎樂觀（原話："I would describe it as cautious optimism"）

### CMI_Analyst_Investor_Day_Cummins_Inc_20260521.md
- 2026-05-21｜CEO｜guidance：CEO 宣布 2030 營收目標區間上調為 $45–50B（原話："revenue to be in the range of $45 billion to $50 billion"）
- 2026-05-21｜CEO｜guidance：2030 EBITDA margin 目標為超過 20%（原話："EBITDA to exceed 20%."）
- 2026-05-21｜CEO｜guidance：前次 2030 目標為 17–18% margin（逐字稿營收寫成 $43 million to $48 million）（原話："and 17% to 18% margin."）
- 2026-05-21｜CFO｜guidance：CFO：目標對應 6–9% 複合年增率（原話："translate into 6% to 9% compound"）
- 2026-05-21｜CFO｜guidance：資料中心貢獻 2–3% CAGR（原話："That delivers 2% to 3% of the compound annual growth rate"）
- 2026-05-21｜CFO｜margin：CFO：未來至少再 250bp 的 margin 改善（原話："a further at least 250 basis points of margin improvement."）
- 2026-05-21｜CFO｜margin：20% EBITDA 目標對應 25% 以上增量 margin（原話："that implies 25% plus incremental margins over time."）
- 2026-05-21｜CFO｜margin：Power Systems 與 Distribution 的 EBITDA% 預期持續改善，Engine/Components 隨新產品成熟（原話："we should see more continuous improvement in the EBITDA"）
- 2026-05-21｜CFO｜margin：公司不給各分部目標（原話："We didn't give individual segment guidance"）
- 2026-05-21｜CFO｜margin：2030 年 Power Systems 加 Distribution 約占總獲利不低於 50%（原話："you're probably not looking at less than 50% of the"）
- 2026-05-21｜CFO｜margin：2025 年 Power Systems 與 Distribution 合計占 EBITDA 60%（原話："exactly 60% of the total in 2025"）
- 2026-05-21｜CEO｜margin：2025 年營收與 EBITDA margin（原話："$33.7 billion in revenue and a record 17.4% EBITDA"）
- 2026-05-21｜CFO｜margin：兩年來 EBITDA margin 改善 250bp（原話："You've seen 250 basis points of margin"）
- 2026-05-21｜Power Systems president｜margin：Power Systems 過去數年 margin 改善逾 1,000bp（原話："driving over 1,000 basis points improvement in margin."）
- 2026-05-21｜CFO｜margin：管理層稱投資不會造成 margin 大幅下挫（原話："any big bathtub in margins"）
- 2026-05-21｜Engine president｜margin：新平台上市品質應計約 18 個月，完整 margin 效果要到 2028 後段（原話："quality accruals, and those will for sure take 18-ish"）
- 2026-05-21｜Engine president｜margin：多數產品要到 2028 後段才看到真正 EBITDA 表現（原話："you're in the late '28 before seeing where they are truly"）
- 2026-05-21｜CFO｜margin：Distribution margin 還有擴張空間（原話："excited about more margin expansion to come in Distribution"）
- 2026-05-21｜CEO｜margin：研發占營收比預期過 2027 後下降（原話："going to start to come down a little bit"）
- 2026-05-21｜CEO｜margin：Power Systems 研發投入增加（原話："some of the R&D investment in Power Systems"）
- 2026-05-21｜Distribution president｜margin：大型引擎市場競爭者少，定價有彈性空間但競爭仍強（原話："there's probably some ability to price more in that space"）
- 2026-05-21｜Distribution president｜margin：同上：定價競爭（原話："competition is tough in that space"）
- 2026-05-21｜Power Systems president｜guidance：資料中心營收由約 $5B 增至 2030 年 $9B 以上（原話："billion today to above $9 billion by 2030."）
- 2026-05-21｜Engine president｜guidance：美國 EPA 規則尚未定案，Q3/Q4 預期強於明年 Q1（原話："Q3, Q4 are going to be stronger than what Q1 will be next"）
- 2026-05-21｜Engine president｜guidance：預期明年第一季出現量的停頓（原話："pause or a lag in volume in the first quarter of next year"）
- 2026-05-21｜Engine president｜guidance：北美重型引擎日產量由約 250 升至 6 月底 400（原話："by the end of June, we'll be up to 400."）
- 2026-05-21｜Engine president｜guidance：北美重型引擎年初日產量（原話："we started the year making 250, 240 engines a day"）
- 2026-05-21｜CFO｜guidance：資本支出框架維持占營收 3–4%（原話："framework of 3% to 4% of revenue for the overall company"）
- 2026-05-21｜Power Systems president｜capital_allocation：新增 $450M 產能投資（原話："we're announcing an additional $450 million of"）
- 2026-05-21｜Power Systems president｜capital_allocation：高馬力引擎／發電機組產能 2030 年達 55GW（原話："20 gigawatts, reaching a total of 55 gigawatts by 2030."）
- 2026-05-21｜CFO｜capital_allocation：FCF：至少 50% 返還股東為起點（原話："at least 50% is the starting point"）
- 2026-05-21｜CFO｜capital_allocation：股利與回購承諾（原話："excess capital to shareholders in the form of share"）
- 2026-05-21｜CFO｜capital_allocation：已重啟股票回購（原話："we restarted our share repurchase activity"）
- 2026-05-21｜CEO｜capital_allocation：M&A：無大型項目在管線（原話："there's no big things that are really in the pipeline right"）
- 2026-05-21｜Engine president｜capital_allocation：Engine 投資高峰已過（原話："peak investment period is largely behind us"）
- 2026-05-21｜CFO｜capital_allocation：CFO：接近投資高峰（原話："we are getting to the point of peak investment"）
- 2026-05-21｜Components/Accelera president｜capital_allocation：Amplify 合資不再於該廠設產線、放慢投資（原話："put lines in that facility and slow the investment"）
- 2026-05-21｜CEO｜commitment：CEO：對 2030 承諾有能見度（原話："line of sight to what we're committing to you today"）
- 2026-05-21｜CFO｜commitment：CFO：對 6–9% 成長有高信心（原話："we have high confidence in the numbers going forward."）
- 2026-05-21｜CFO｜commitment：Accelera 方向為降低虧損（原話："loss improvement is the trend that we're aiming for"）
- 2026-05-21｜Power Systems president｜commitment：Accelera 已調降今年虧損預期（原話："we revised our guidance to lower losses even this year"）
- 2026-05-21｜Power Systems president｜commitment：不給 Accelera 2030 分部目標（原話："we aren't giving a segment-specific 2030 target for Accelera"）
- 2026-05-21｜Power Systems president｜commitment：第一台大型天然氣引擎 2028 年交付（原話："The launch of a natural gas large engine will be in '28."）
- 2026-05-21｜Power Systems president｜commitment：新產能 2027 年開始逐步貢獻（原話："You won't see big step changes"）
- 2026-05-21｜Engine president｜commitment：新 7 公升引擎 2028 年 1 月 1 日上市（原話："we're launching the 7-liter in Jan 1 2028"）
- 2026-05-21｜CEO｜commitment：prime 產品尚不接受正式訂單（原話："we're not taking firm orders"）
- 2026-05-21｜CFO｜commitment：prime 業務未來可達 $200M 的數倍（原話："We would expect multiples of $200 million"）
- 2026-05-21｜Power Systems president｜product：天然氣大型引擎最高 4MW prime power（原話："it extends up to 4 megawatts of prime power"）
- 2026-05-21｜Engine president｜product：L9 到 X10：馬力與扭力提升（原話："70 additional horsepower, 400-foot pounds of torque"）
- 2026-05-21｜Engine president｜product：X10 納入 Mack Granite（原話："We've already announced the X10 for Mack's Granite platform."）
- 2026-05-21｜Engine president｜product：EPA 2027 每台卡車成本增加約 $10,000，多在動力系統（原話："EPA 2027 could add roughly $10,000 to the cost of a truck"）
- 2026-05-21｜Power Systems president｜product：Cummins 自稱唯一整合供應商（原話："Cummins is the only integrated offering in the market"）
- 2026-05-21｜Components president｜product：Components 受法規驅動：EPA27 以某種形式必然發生（原話："EPA27 in some form is going to happen."）
- 2026-05-21｜CFO｜competition：大型引擎競爭者數量有限（原話："very limited number of players in large engines"）
- 2026-05-21｜Engine president｜competition：年產約 130 萬具引擎，為最近對手兩倍以上（原話："well over double our nearest competitor"）
- 2026-05-21｜Engine president｜competition：X10 預期帶動重型市占成長（原話："you will see market share growth in heavy-duty via the X10."）
- 2026-05-21｜Engine president｜competition：OEM 推動轉向終端用戶拉動（原話："More and more, we are increasingly pull led"）
- 2026-05-21｜CEO｜customer：PACCAR 為最大客戶（原話："PACCAR has been a partner of Cummins for 80 years"）
- 2026-05-21｜Engine president｜customer：北美活躍引擎保有量至少 220 萬具（原話："at least 2.2 million active on-highway engines"）
- 2026-05-21｜Engine president｜customer：售後需求高峰在 7–11 年（原話："peak somewhere between 7 and 11 years"）
- 2026-05-21｜Power Systems president｜customer：中國資料中心成長 84%（Q1）（原話："we delivered 84% growth in China, in our data center"）
- 2026-05-21｜Power Systems president｜customer：美國為 $9B 資料中心營收最大部分（原話："is the largest part of the 9"）
- 2026-05-21｜Power Systems president｜customer：中國資料中心恆為備用電源市場（原話："China will always be a backup"）
- 2026-05-21｜Power Systems president｜customer：目前 prime 訂單已在 backlog（原話："there are prime orders and customers in the backlog"）
- 2026-05-21｜Power Systems president｜customer：2030 年美國未滿足電力需求 20–50GW（原話："we think it's somewhere in that 20 to 50 gigawatts of"）
- 2026-05-21｜Power Systems president｜customer：目前 95% 為備用電源（原話："95% of our business today is standby"）
- 2026-05-21｜Power Systems president｜customer：prime 產品預期 2030 年底才進來（原話："you'll see the prime stuff come in towards the end of"）
- 2026-05-21｜Power Systems president｜customer：訂單能見度延伸至 2030 年後（原話："we see a pipeline of orders out beyond"）
- 2026-05-21｜CEO｜risk：零排放技術採用速度較慢（原話："we've seen slower adoption of 0 emissions technologies"）
- 2026-05-21｜Power Systems president｜risk：氫能投資縮減（原話："namely in hydrogen, where we stepped away from some"）
- 2026-05-21｜Engine president｜risk：車隊獲利困難（原話："it's difficult right now for a lot of the fleets to"）
- 2026-05-21｜Engine president｜risk：中型車排放法規草案未出，公司尚待釐清（原話："we can't get this draft rule fast enough to be quite honest"）
- 2026-05-21｜Power Systems president｜risk：採礦市場偏軟（原話："That market has been a little soft."）
- 2026-05-21｜CEO｜risk：預期 EPA 提前採購起點（原話："we originally thought it would start second half of last"）
- 2026-05-21｜CEO｜risk：全年 70 多項關稅政策（原話："more than 70 tariff policies that impacted our business"）

### 問答異常語氣（迴避／改口／保留）
- CMI_Q2_2026_Earnings_Call_20260804.md｜問：Jamie Cook 問下半年 EPS 約 $16-17 能否作為 2027 基期，以及 2027 上半年走勢｜答法：Rumsey 稱不給 2027 具體指引、僅說需求會有些回落但較平緩；Smith 說 'Too early to say'，未回答 $16-17 是否為基期
- CMI_Q2_2026_Earnings_Call_20260804.md｜問：David Raso 問明年發電產能相對今年的量｜答法：Smith 回 'punt that one until later in the year'，只說會更高，未給數字
- CMI_Q2_2026_Earnings_Call_20260804.md｜問：Angel Castillo 問新引擎定價與分階段轉換對利潤率、市占的影響｜答法：Smith 稱 'still working through all of the pricing'，未給定價或利潤率數字
- CMI_Q2_2026_Earnings_Call_20260804.md｜問：Kyle Menges 問簽新合約時定價有無實際改變｜答法：Smith 改談長期提升利潤率的意圖與市場競爭者少，未直接回答新合約定價是否變動
- CMI_Q2_2026_Earnings_Call_20260804.md｜問：Kristen Owen 指出自然需求改善與中型卡車預購上調之說法難以對齊｜答法：Rumsey 重申基本面改善為主、部分預購；分析師表示稍後場外再問，未當場釐清
- CMI_Analyst_Investor_Day_Cummins_Inc_20260521.md｜問：Jamie Cook：後處理與電池的增量內容金額，以及 20% EBITDA「greater than」可高出多少｜答法：CEO 改談資料中心營收規模與廠房彈性，CFO 談分部節奏並重述 25% 增量 margin，兩者均未給金額或上限
- CMI_Analyst_Investor_Day_Cummins_Inc_20260521.md｜問：Robert Wertheimer：新增 20GW 產能有多少已售出、占指引的比例｜答法：CFO 打斷，表示只談已給的營收數字；Bush 僅答訂單已排到 2028 並有 2030 後管線，未給比例
- CMI_Analyst_Investor_Day_Cummins_Inc_20260521.md｜問：KC Parker：prime 機組售後市場相對成本的規模，並要求不要回答不知道｜答法：Bush 以使用時數與大修頻率定性說明，未給金額或比例
- CMI_Analyst_Investor_Day_Cummins_Inc_20260521.md｜問：Michael Feniger：中型車排放法規情境與 2027 引擎 margin 爬坡｜答法：Merritt 稱等待草案，不談更多細節，表示會再回報
- CMI_Analyst_Investor_Day_Cummins_Inc_20260521.md｜問：Tami Zakaria：天然氣引擎 2028 交付是否已有大型 prime 訂單在 backlog｜答法：Bush 答 HSK78 已有 prime 訂單；稍後 Rumsey 補充新 prime 引擎未接正式訂單，請勿每季追問訂單
- CMI_Analyst_Investor_Day_Cummins_Inc_20260521.md｜問：David Raso：2030 年 Power Systems 與 Distribution 占獲利比例｜答法：CFO 稱難以給確切百分比，被追問後才說不低於 50%，並稱 Really a big number

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 4 | 2 |
| customer_second_source | found | 2 | 1 |
| customer_concentration_credit | found | 2 | 1 |
| supply_demand_durability | found | 5 | 4 |
| regulatory_antitrust | found | 1 | 1 |
| reg_tariff_export | found | 4 | 1 |
| geo_supply_chain | found | 2 | 2 |
| end_markets | found | 3 | 2 |
| substitute_technology | found | 3 | 2 |
| channel_business_model_shift | found | 2 | 1 |
| capital_markets_pricing | found | 3 | 2 |
| major_events | found | 4 | 4 |
| cyclical_supply_discipline_capacity | found | 4 | 3 |
| cyclical_inventory_price_position | found | 5 | 3 |
| cyclical_prior_downcycle_behavior | found | 3 | 3 |

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260518","verdict":"衛星候選 / 觀望 — Power Systems data center super-cycle + EPA 2027 prebuy thesis 真實但估值已透支；建議等 Fwd PE 分位回 60% 區（~$580-620 區）或 NA Class 8 prebuy 真實流入 FY27 EPS 共識上修後再進場","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"數據中心 backup gen 結構性需求支撐 Power Systems 段 +15% YoY 成長 + EBITDA margin &gt; 25%","columns":{"2Y 驗證點":"FY26-FY27 Power Systems Rev &gt; $9-11B（FY25 ~$7B）；EBITDA margin 平均 ≥ 26%","5Y 驗證點":"FY30 Power Systems Rev &gt; $14B、占總 Rev ≥ 32%","10Y 驗證點":"數據中心 backup gen 市場至 $19.7B 2030 + CMI 維持 30%+ NA 高功率市佔","具體數字門檻":"2026 guidance global power generation revenues +15-25% YoY；market $8.4B 2024 → $19.7B 2030E (Grand View Research, 15.2% CAGR)","信息來源":"Grand View Research data center generator market 2030 forecast；CMI Q1 2026 earnings call","漂移觸發條件":"連 2 季 Power Systems YoY &lt; +10% 或 EBITDA margin &lt; 25% → 削弱"}},{"id":"H2","text":"EPA 2027 prebuy 驅動 NA Class 8 訂單 2026 H2 +30-50% YoY，2027 拓展為「2027 規範下 HELM 提早合規」競爭優勢","columns":{"2Y 驗證點":"2026 NA Class 8 production ≥ 320,000 units；HELM X15 量產 ramp Q3-Q4 26 上線且無 quality issue","5Y 驗證點":"FY27-FY28 even after pre-buy crash，CMI Engine 段 Rev 仍能維持 FY24 水平（受惠 HELM 市佔擴張）","10Y 驗證點":"EPA 2027 / CARB 規範執行至 2030+，CMI Engine 段每 1pp 市佔加分對應 $400M Rev 增量","具體數字門檻":"NA Class 8 訂單 Feb 26 +159% YoY 至 47,200 units；ACT Research 2026 Class 8 tractor sales forecast 140,000 units (truck-only)；X15 EPA 2027 認證 / X10 75% lower NOx","信息來源":"ACT Research Class 8 2026 forecast；Cummins HELM platform announcement 2024-02-29","漂移觸發條件":"2027 H1 月訂單 &lt; 15,000 = pull-forward 反噬已現 → 削弱；連 2 季 HELM ramp issue → 反轉"}},{"id":"H3","text":"EBITDA margin 結構性升至 17.75-18.50%（FY26 mid-point 18.1%）並 sustainable，反映 Power Systems mix shift 結構性效益","columns":{"2Y 驗證點":"FY26 EBITDA margin 達 guidance mid-point 18.1%；FY27 持續 17-18%","5Y 驗證點":"FY30 EBITDA margin &gt; 18% sustainable，含 Power Systems mix shift 持續貢獻","10Y 驗證點":"長期 EBITDA margin baseline 從歷史 13-14% 升至 17-18%（結構性 reset）","具體數字門檻":"FY26 guidance EBITDA margin 17.75-18.50%（raised from prior 17.0-18.0%）；Power Systems Q1 26 EBITDA margin 29.5% × Rev mix 24% 占整體 EBITDA &gt; 35%","信息來源":"Cummins Q1 2026 earnings release 2026-05-05；Power Systems segment EBITDA breakdown","漂移觸發條件":"連 2 季 全公司 EBITDA margin &lt; 16.5% 或 Power Systems &lt; 24% → 削弱；連 4 季 &lt; 15% 或 Power Systems &lt; 22% → 反轉"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"EPA 2027 prebuy 反噬（pull-forward demand 提早結束）","columns":{"對應假設":"H2","時間尺度標記":"🔥 中期（4-6 季）","監測指標":"NA Class 8 訂單月度（ACT Research）+ CMI Engine 段季度 Rev YoY","警戒閾值":"2026 H2 月訂單 &lt; 25,000（peak 預期 ~30,000）→ 警示；2027 H1 月訂單 &lt; 15,000 → 結構性反噬，Engine 段 EBITDA margin 連 2 季 &lt; 8% 觸發減倉"}},{"id":"R2","text":"數據中心 capex pause / Power Systems 訂單 plateau","columns":{"對應假設":"H1","時間尺度標記":"🔥 中期（4-6 季）","監測指標":"Hyperscaler capex guidance（Microsoft / Google / Meta）+ Power Systems backlog 變化","警戒閾值":"連 2 季 Power Systems YoY &lt; +10% 或 EBITDA margin &lt; 25% → thesis 削弱；連 4 季 &lt; +5% → thesis 反轉，估值倍數 reset 至 17-18x"}},{"id":"R3","text":"BEV / HFC truck 滲透率突破 + ICE TAM 萎縮（結構性慢變數）","columns":{"對應假設":"H1 H2 H3","時間尺度標記":"🐢 長期（2+ 年慢變數）","監測指標":"BEV Class 8 NA 銷售滲透率（當前 &lt;2%）+ CMI Accelera ROIC + 加氫 / 充電基建擴張節奏","警戒閾值":"BEV Class 8 滲透率 &gt; 10% (3-5 年內) = 結構性威脅升級；需 ≥ 50% 機率才砍倉（避免短期新聞驚嚇）"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🔴","ma":"✅","trap":"🟡","moat_trend":null,"runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":696.53,"archetype":null,"cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"CMI","date":"2026-11-08","schema":"v15.0","contract":"v19","company_name":"Cummins Inc."},"oneliner":"康明斯跌到 450 美元，只有今年 EPS 的 15.2 倍，資料中心發電訂單排到 2028 下半年，生意沒壞；但現價仍要 2030 目標大致達成才有約一成年報酬，2027 年獲利基礎要等 2 月財測，先不接。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CMI_20261108/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CMI_20261108/scenario.json","answers":{"q1_business":{"verdict":"賺的是卡車廠、車隊和資料中心的動力設備與售後錢，獲利正從卡車引擎往發電與經銷移動，錢卡在大型發電機組的產能和全球服務網路這一節。","reasoning":"Q3 營收 94.38 億美元，年增 13%，毛利率 27.7%，GAAP 營益率 15.3%，EBITDA 率 18.9%。分部含內部銷售，加總高於合併數：Engine 31 億美元（+20%，EBITDA 率 13.5%）、Components 29 億（+23%，14.3%）、Distribution 33 億（+4%，13.9%）、Power Systems 23 億（+15%，25.4%）、Accelera 1.03 億（虧損 5,600 萬）。CFO 在 2026-05-21 投資人日說，2025 年 Power Systems 加 Distribution 占 EBITDA 60%，2030 年不低於 50%。單點依賴有兩個：PACCAR 占 2025 年營收 13%（2024 年 16%），是唯一超過 10% 的客戶；資料中心積壓集中在大型超大規模客戶，金額事實表未涵蓋。Q3 EPS 8.25 美元含 7,500 萬美元離散稅項利多（每股 0.54 美元），扣掉後是 7.71 美元。全年指引由營收 +10–13% 收斂到約 +10%，主因是北美皮卡。","fact_refs":["f_kpi0_revenue_gaap","f_kpi1_ebitda_margin_non_gaap","f_kpi2_gaap_operating_income","f_kpi4_guidance_fy2026_revenue_","f_kpi5_guidance_fy2026_ebitda_m"],"verdict_values":{"revenue_quality":"Q3 成長以量為主，發電有正面定價；CFO 說全公司價格減成本、關稅合計略為負值，毛利率改善靠銷量與營運執行。","unit_econ_note":"資料中心案的 EBITDA 金額高於其他用途，因為 Distribution 多賺安裝；但 CEO 說發電專案利潤率低於售後零件，Q3 Distribution EBITDA 率因此由 15.5% 降到 13.9%。","archetype":{"primary":"循環/商品","secondary":"品質複利成長","confidence":"中","fingerprint":"不是商品價格接受者，是需求量循環：卡車段由低點回升，發電段訂單滿載但新增產能 2028 年才大量到位。"},"industry":{"clock_phase":"II","sd_verdict_source":"供給可逆性高。訂單排到 2028 下半年是真的，但緊俏來自產能不足，康明斯自己要把高馬力產能加到 55GW，Caterpillar、Generac 也在擴，2028 年供給大增後定價能否守住沒有證據。時鐘落在擴張期的依據是營收年增由 Q1 3%、Q2 9% 升到 Q3 13%，Q4 指引隱含 15%。","bargaining":{"up":"供應鏈偏緊，Q3 一家供應商出問題就延後約 2 億美元營收，多項關鍵零件單一來源。","down":"大型機組供應商少，對資料中心客戶有定價空間；對 PACCAR 等大型 OEM 議價較弱，供應協議不保證數量。","geo":"中國含合資 Q3 營收 19 億美元，出口管制可能影響收款與現金調回；資料中心訂單國際已與美國持平。"},"profit_pool_dir":"利潤池往 Power Systems 與 Distribution 移動，2025 年合計占 EBITDA 60%；五年前占比事實表未涵蓋。","tam_table":{"expanded":false,"reason":"事實表未涵蓋 TAM 與滲透率。資料中心只有公司自述由約 50 億美元到 2030 年 90 億美元以上，算不出利潤池五年變化，這是已知缺口。"}}}},"q2_moat":{"verdict":"護城河持平（→）：發電端在加寬，卡車端被 PACCAR 自製和中國電動卡車削掉一塊，兩邊相抵。","reasoning":"機制是引擎規模、售後網路與發電機組到安裝的一體化。管理層稱年產約 130 萬具引擎，超過最近對手兩倍；北美活躍公路引擎至少 220 萬具。方向證據：Power Systems EBITDA 率 Q3 升 250 個基點到 25.4%，定價為正，Q3 接單高於公司預期。反面是 PACCAR 占營收由 16% 降到 13%，最大客戶份額下滑就不能判擴大；中國卡車銷量 −15%、產業 −5%，公司歸因於電動卡車。TTM 營業利益率 11.79%，低於 Caterpillar 18.33%、Allison 18.88%，高於 PACCAR 10.75%、Generac 10.37%。執行力 8 分；定價力本來 8 分，扣客戶自製威脅 1 分得 7 分。","fact_refs":["f_peer_cmi_gross_margin_pct","f_peer_cmi_operating_margin_pct","f_peer_cat_operating_margin_pct","f_peer_pcar_operating_margin_pct","f_peer_alsn_operating_margin_pct","f_peer_gnrc_operating_margin_pct"],"verdict_values":{"moat":{"mechanism":"全球引擎規模、售後服務網路，加上發電機組到安裝的一體化供應。","execution":8,"pricing":7,"grade":"B","trend":"→","trend_evidence":"發電端定價與利潤率擴大；卡車端最大客戶占比由 16% 降到 13%，中國銷量跌幅比產業多 10 個百分點。資料中心份額增減沒有一手數據。","competitor_notes":[{"name":"Caterpillar","strategy_note":"大型發電與渦輪都做，營益率高於康明斯，發電銷售增速更快，是資料中心大機組最直接的對手。"},{"name":"PACCAR","strategy_note":"最大客戶，同時在密西西比州擴自製引擎產能，是客戶也是對手。"},{"name":"Allison","strategy_note":"變速箱專業廠，不直接競爭引擎，只當動力總成專業化的利潤率參照。"},{"name":"Generac","strategy_note":"資料中心積壓約 16 億美元，由備援市場往上打；客戶改訂小排量機組時，這一帶的競爭會加劇。"}],"peer_na_reason":"同業 ROIC 事實表未涵蓋，改用 TTM 營業利益率比較。","threats":[{"level":"🟡","text":"Caterpillar 發電銷售成長 72%，Generac 資料中心積壓約 16 億美元，同業擴得比康明斯快。Power Systems Q3 只增 15%，部分受自身產能與供應限制。","p":"35%","evidence_refs":["substitute_technology#2","supply_demand_durability#3"]},{"level":"🔴","text":"PACCAR 擴自製引擎，10-K 也寫明客戶可能自行開發或改向他廠採購；占營收由 16% 降到 13%，週期與自製各占多少事實表無法拆。","p":"40%","evidence_refs":["customer_second_source#0","customer_second_source#1","customer_concentration_credit#0"]},{"level":"🟡","text":"電動與其他替代技術。中國電動卡車已影響銷量，但只限當地公路車；北美重卡滲透率事實表未涵蓋，資料中心本十年仍以柴油備援為主。","p":"30%","evidence_refs":["competitive_share_entrants#1"]}],"roic_durability":{"quadrant":"資料缺口：事實表未涵蓋投入資本，無法算周轉率與象限；稅後營益率約 9.1%（TTM 營益率 11.79%×（1−23%））。","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者是資料中心營運者與車隊，決策者與付款者是超大規模客戶、OEM 與車隊，三環都成立。備援電力延後的代價是停機風險，屬需要不是想要，目前 95% 是備援用途。需求量的波動放在風險段處理。"},{"item":"決策層級","level":"🟡","text":"大型機組供應商少，超大規模客戶簽多年協議，替代性低。卡車端逐台選配，PACCAR 可改用自製引擎，替代性存在。漲價流失率與續約率事實表未涵蓋。"},{"item":"價值鏈分配","level":"🟡","text":"Power Systems EBITDA 率 25.4%，錢目前留在這一節。但買方高度集中，供應鏈限制出貨，CFO 說成本在爬；2028 年全產業擴產後分配可能反轉。"},{"item":"社會容忍度","level":"🟡","text":"分析師已在法說問美國資料中心的能源與環保爭議，CEO 承認有討論。排放端有前科，2024 年付 19 億美元和解；EPA 2027 的 NCP 金額預計 12 月定案。限制備援機組的法案證據事實表未涵蓋。"}],"roiic":"約 47%（代理值，非實測）","reinvest_rate":"約 28%（代理值，非實測）","endo_ceiling":13.2,"formula_note":"投入資本與折舊不在事實表，改用代理：FY2023–25 累計淨利 75.24 億美元減累計 FCF 54.18 億美元，得 21.06 億當淨再投資，占淨利 28%；FY2022→FY2025 營業利益增 12.85 億，稅後（23%）9.9 億，除以 21.06 億得 47%；47%×28%＝13.2%。此數可能高估，因為 2022 年 Meritor 併購款不在分母，金額事實表未列；FY2024 淨利 39.46 億明顯高於前後年，一次性項目也未拆。"}}}},"q3_growth":{"verdict":"成長跑道中等（🟡）：卡車引擎已成熟，第二條曲線是資料中心與主電力天然氣，但 130 公升機組還沒收正式訂單，2029 年才有像樣營收。","reasoning":"成長以量為主，發電有漲價，併購為零，淨回購每年約 1 個百分點。公司目標是 2030 年營收 450–500 億美元（年增 6–9%）、EBITDA 率超過 20%。三年共識 EPS CAGR 由 FY2025A 20.5 美元起算是 25.7%，由 FY2026E 29.59 美元到 FY2028E 40.69 美元是 17.3%；內生上界 13.2%。缺口 12.5 個百分點（FY2026E 起算為 4.1），來源依序是 FY2025 含 Accelera 費用的低基期、利潤率由 17.4% 往 20% 以上擴張、淨回購，沒有收購。Base 五年 EPS 年增 10.2%，在上界內。反例：若增量報酬的代理值高估，上界會更低，Base 也會變吃力。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m"],"verdict_values":{"growth":{"driver_mix":"量為主，發電有漲價，淨回購每年約 1 個百分點，併購為零；利潤率擴張對 EPS 的貢獻大於營收。","runway_years":null,"runway_post_y5":"🟡","endo_ceiling_basis":"沿用護城河段的代理值 13.2%（淨再投資率 28%×增量報酬 47%）；投入資本與折舊事實表未涵蓋。","segments":[{"item":"Power Systems","value":"Q3 營收 23 億美元、+15%、EBITDA 率 25.4%；FY2026 指引 +15–18%、25.1–25.6%。新產能 2027 年開始增加，2028 年增幅較大。"},{"item":"Distribution","value":"Q3 營收 33 億美元、+4%、EBITDA 率 13.9%；FY2026 指引 +10–13%，Q4 指引中點隱含季增 23%。"},{"item":"Engine","value":"Q3 營收 31 億美元、+20%、EBITDA 率 13.5%；FY2026 指引下修到 +8–11%、12.25–12.75%。"},{"item":"Components","value":"Q3 營收 29 億美元、+23%、EBITDA 率 14.3%；FY2026 指引 +8–11%、13.25–13.75%。"},{"item":"Accelera","value":"Q3 營收 1.03 億美元；FY2026 EBITDA 虧損指引 2.6–2.9 億美元，Hydrogenics 停用建議的影響未計入。"}],"decay_signals":[{"signal":"毛利率連 2 季年減","lit":false,"evidence":"Q2 26.1% 對 26.4% 年減，Q3 27.7% 對 25.6% 年增。"},{"signal":"核心市占近 12 個月縮減","lit":true,"evidence":"中國卡車銷量 −15%，產業 −5%；PACCAR 占比下降。北美與資料中心份額無一手數據。"},{"signal":"主力產品提價後銷量下滑","lit":false,"evidence":"皮卡 −16%，公司歸因於柴油價格與利率，不是提價。"},{"signal":"EPS CAGR 高於營收 CAGR 超過 5 個百分點","lit":true,"evidence":"共識 EPS 年增 25.7%，營收兩年年增約 10%，部分是低基期。"},{"signal":"FCF／淨利連 2 年低於 0.75","lit":false,"evidence":"FY2024 0.07（含 19 億美元和解款），FY2025 0.84。"},{"signal":"SBC／營收大於 5% 且上升","lit":null,"evidence":"事實表未涵蓋。"},{"signal":"TAM 萎縮或被替代","lit":false,"evidence":"中國公路車有替代，集團層面尚未看到；TAM 數字事實表未涵蓋。"},{"signal":"產業倍數近 3 年系統性下移","lit":null,"evidence":"事實表未涵蓋產業倍數序列。"},{"signal":"維持性資本支出占 FCF 超過 60%","lit":false,"evidence":"總資本支出指引 13.5–14.5 億美元，TTM FCF 約 34.7 億美元；維持性比例未揭露。"},{"signal":"停止投資新產能且收入下滑","lit":false,"evidence":"仍在加 20GW 產能，FY2026 營收約 +10%。"}],"trap_rating":"價值陷阱風險中等（亮 2 個），長期成長性中等。"}}},"q4_capital":{"verdict":"現金生成改善，回饋紀律清楚，但零排放的併購和投資交了學費，回購價位也還算不出來。","reasoning":"FCF／淨利 FY2025 為 0.84，FY2024 為 0.07，後者含 19 億美元和解付款；TTM FCF 利潤率 9.66%。Q3 營業現金流 14.05 億美元、資本支出 3.03 億、FCF 11.02 億，回購 3.59 億加股息 3 億，約 47% 的營業現金流回給股東；今年累計 16.81 億美元。資本支出指引 13.5–14.5 億美元，併購為零，債務到期結構事實表未涵蓋。淨負債 33.34 億美元，約 FY2026 指引 EBITDA 67 億美元的 0.5 倍。SBC 金額事實表未涵蓋，改用股數判斷。","fact_refs":["f_kpi3_free_cash_flow","f_peer_cmi_fcf_margin_pct","f_net_debt_m","f_shares_diluted_m","f_dividend_yield_ttm"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":true,"passed":false,"input":"Meritor（2022）的已實現報酬事實表未涵蓋。可驗證的是零排放：2025 Q3 Accelera 減損與存貨費用 2.4 億美元，2026 Q1 淨付 1.75 億美元賣掉低壓燃料電池，FY2026 仍預期 EBITDA 虧損 2.6–2.9 億美元，Hydrogenics 電解槽又發出停用建議。"},{"name":"buyback_yield","applicable":true,"passed":null,"input":"Q2 回購 2.25 億、Q3 3.59 億美元；回購均價與 10 年期殖利率事實表未涵蓋，無法判定。現價盈餘殖利率 6.6%（29.59÷450.07）只供參考。"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"SBC 金額事實表未涵蓋。改看股數：稀釋股數由 FY2022 約 1.423 億（淨利÷EPS）降到 FY2025 約 1.387 億，目前流通 1.371 億，淨稀釋為負。"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購：近 12 個月無併購類重大申報，CEO 在投資人日說管線沒有大型項目；回饋節奏已寫在本題判斷中。"}}}},"q5_valuation":{"verdict":"現價要的是 2030 目標大致兌現，我信大半，所以算合理價，不算便宜。","reasoning":"現價 450.07 美元，要 10% 年報酬（股息 1.82%，股價年增 8.2%），五年後要 667 美元；用 14 倍終端本益比，等於 FY2031 EPS 47.6 美元，年增 10%。公司 2030 目標（營收 450–500 億美元、EBITDA 率 20–21%）換算約 41–48 美元，換算用 FY2026E 淨利÷EBITDA 約 60%、2030 年 1.32 億股。市場沒有定價崩盤，定價的是目標大致達成；而共識 FY2028E 40.69 美元已貼近這個區間下緣，比公司目標早兩年。賣方目標價 745–757 美元都是 Q3 前資料，區間 500–894 美元，高低比 1.79 倍，對本次結論沒有參考力。反例：若 2030 目標偏保守，現價其實便宜。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_pe_current","f_pe_percentile","f_ps_current","f_ps_percentile","f_ev_s_current","f_ev_s_percentile","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_3m_fy1_pct"],"verdict_values":{"valuation":{"basis":"Forward P/E（FY2026E 共識 EPS），循環股輔以銷售倍數對照。","tier":"工業動力設備","peers":{"expanded":false,"reason":"事實表只有同業利潤率，沒有同業本益比；終端倍數因此沒有同業現值對照，只用康明斯自身 15.21 倍為錨，這是已知缺口。"},"fwd_pe":15.21,"peg":0.88,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"本益比面偏便宜：今年 15.21 倍、明年 12.93 倍，PEG 0.88（15.21÷FY2026E 到 FY2028E 年增 17.3%）。銷售面不便宜：P/S 1.72 倍在 4 個年度端點的 65 百分位，EV/S 1.81 倍在 60 百分位。五年分位算不出來，事實表只有 4 個年度端點。Base 年報酬約 10%，屬中段。分母有爭議，便宜的論證不算數，所以評中性。短期上檔＝FY2027 Base EPS 33.5 美元×15 倍＝502 美元；中期＝FY2028 Base EPS 38 美元×14.5 倍＝551 美元。","upside_short_pct":11.6,"upside_mid_pct":22.4,"denominator_disputed":true,"denominator_note":"分母是 FY2026E 共識 29.59 美元，利潤率在歷史高位，含 Q1 的 1.99 億美元出售損失與 Q3 每股 0.54 美元稅項利多；11-07 快照未反映 Q3 財測收斂。股價半年跌 33%，FY1 共識三個月只修 −0.24%，爭點就是這個分母守不守得住。"}}},"q6_how_wrong":{"verdict":"最可能看錯的是 2027 年獲利基礎：Q3 實質低於預期，共識還沒動，便宜的本益比可能建立在高點獲利上。","reasoning":"第一種錯法是太保守：Q3 接單高於公司預期，排程到 2028 下半年，股價可能在 2 月財測前就反彈，等待會買貴。第二種是還不夠保守：Bear 的 FY2029 EPS 24 美元只比 FY2026E 低 19%，而 2008 年第四季 EBIT 率曾由 9.2% 降到 3.9%，2019 年 Class 8 產量九個月跌 55%；資料中心和卡車同時下行時，跌幅可能超過 −50%。半年跌 33% 的原因事實表未涵蓋，法說只看到分析師問選舉消息與資料中心能源爭議，不能當成已知原因。RSI 23.81 代表賣壓重，不代表到底。歷史最大回撤與空方論點事實表未涵蓋。","fact_refs":["f_week26_return_pct","f_rsi14","f_ma_state","f_ma_w250","f_consensus_rev_fy1_pct"],"verdict_values":{"trap":{"verdict":"🟡","label":"價值陷阱風險中等：便宜建立在高點利潤率上，衰退信號亮 2 個。"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":29.59,"pe":15.21,"basis":"FY2026E 共識 EPS（FY1），現價 450.07 美元；終端倍數同樣用當年度 EPS 當分母。"},"eps":{"bull":[36.0,43.0,50.0,56.0,62.0],"base":[33.5,38.0,42.0,45.0,48.0],"bear":[30.0,26.5,24.0,26.5,28.5]},"pe":{"bull":17.5,"base":14,"bear":11},"p":{"bull":20,"base":50,"bear":30},"yield_pct":{"dividend":1.82,"net_buyback":1.0},"second_stage":{"bull_cagr_pct":9,"base_cagr_pct":6},"max_dd":{"lo":-50,"hi":-30,"basis":"三個錨：250 週均線 327.19 美元（−27%）；Bear 中途低點 FY2029 EPS 24 美元×11 倍＝264 美元（−41%）；同一 EPS 跌到 9.4 倍＝225 美元（−50%）。下行幅度參考 2008 年第四季 EBIT 率由 9.2% 降到 3.9%、2019 年 Class 8 產量九個月跌 55%。歷史股價最大回撤事實表未涵蓋；股價已自 5 月 696.53 美元跌 35%。","trigger_time":null},"basis":{"bull":"資料中心 2030 年高於 90 億美元，130 公升主電力 2029 年起放量，卡車 2028 年接續成長，EBITDA 率 21% 以上；終端 17.5 倍，同業本益比事實表未涵蓋。","base":"FY2027 低於共識約 4%（切換成本、皮卡弱、卡車持平），2030 年大致達成公司目標；終端 14 倍略低於現值 15.21 倍，因為成長放緩到 7% 左右；五年年增 10.2%，在內生上界 13.2% 以內。","bear":"2028 年供給大增遇上客戶放緩，卡車同時下行，FY2029 EPS 24 美元後部分回復；終端 11 倍，對應成長降到 5–10% 的熄火情境。機率 30%：共識成長超過內生上界，循環股下行有前例，2028 年訂單排程只擋住前兩年。"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"2008 年第四季 EBIT 率由 9.2% 跌到 3.9%，2019 年 Class 8 產量九個月跌 55%；Caterpillar、Generac 同步擴資料中心產能，康明斯 20GW 新產能 2028 年才大量到位。","assumption":"資料中心需求與卡車週期不會同時轉弱，2028 年新增產能仍被消化。","consequence":"五年後虧 50% 最可能的故事：2028 年供給大增時超大規模客戶放緩，卡車同時下行，FY2029 EPS 跌到 24 美元，本益比 9–10 倍，股價約 225 美元。","ruling":"採納，已放進 Bear 機率 30% 與最大跌幅下緣 −50%。這條和唯一致命事件部分重疊，差別在這裡是供需慢慢反轉，唯一致命事件是訂單被取消。","watch":"每季大型機組訂單排程月份、Power Systems 營收年增與 EBITDA 率、ACT 月度卡車訂單。","evidence_refs":["cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#2","supply_demand_durability#3"]},{"view":"論點成功但股東經濟變差","evidence":"Q3 Distribution EBITDA 率由 15.5% 降到 13.9%，CEO 說發電專案利潤率低於售後零件；CFO 說下半年價格減成本略為負值；Q4 Power Systems 隱含約 22.5%；客戶改訂小排量機組，儲能案也在增加。","assumption":"資料中心營收到 2030 年 90 億美元時，增量利潤率維持 25% 以上。","consequence":"營收達標但組合變差，EBITDA 率停在 18–19%，FY2031 EPS 約 40 美元，以 14 倍計年報酬由約 10% 降到約 6%。","ruling":"部分採納。Base 已低於共識，但沒有扣到這麼低，因為 Q3 毛利率創新高，組合惡化還沒出現在全公司數字上。","watch":"Distribution EBITDA 率、Power Systems 增量利潤率，每季看。","evidence_refs":["reg_tariff_export#2"]},{"view":"價格已反映太多","evidence":"跌 33% 後仍要 FY2031 EPS 47.6 美元才有 10% 年報酬，接近 2030 目標換算 41–48 美元的上緣；P/S 仍在 4 個年度端點的 65 百分位。","assumption":"跌這麼多就算便宜。","consequence":"FY2031 EPS 只有 43 美元時，年報酬約 8%，不足以補償循環股的回撤。","ruling":"採納。已跌不是安全邊際，要有 2027 年獲利基礎的確認才算。","watch":"2 月財測後的共識 FY2027 EPS。","evidence_refs":["capital_markets_pricing#0"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟠","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟠","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 696.53 → 本次 450.07（-35.4%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=696.53","side_b":"本次 price_at_dd=450.07","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 696.53 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 696.53 美元：五年期望值 前份未列，基準年化 前份未列，前份未列不對稱比","side_b":"本次情境、股價仍用 696.53 美元：Bull 價 1,085、Bear 價 313.5，五年期望值 −7.1%，基準年化 −0.7%，不對稱比 0.68","ruling":"先換情境、股價不動：五年期望值與基準年化前份未列，無法比較。前份未列不對稱比，本次為 0.68。Bull、Bear 價位與股價無關，只受情境影響。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 696.53 美元：五年期望值 −7.1%，基準年化 −0.7%，不對稱比 0.68","side_b":"本次情境、股價 450.07 美元：五年期望值 +43.8%，基準年化 8.3%，不對稱比 3.1","ruling":"再換股價、情境不動：起點價下跌 35.4%，五年期望值多 50.9 個百分點，基準年化多 9.1 個百分點，不對稱比由 0.68 升到 3.1。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"估值結論變動","cause":"價格變動","prior_field":["val"],"side_a":"前份股價 696.53 美元時評為最貴一級，要等 580–620 美元。","side_b":"本次 450.07 美元、今年 EPS 的 15.2 倍，評為中性。","ruling":"改變的主因是股價跌 35%，FY2026E 共識三個月只修 −0.24%。不升到最便宜一級，因為銷售倍數仍在年度端點的 60–65 百分位，便宜只在本益比上成立，而分母正是爭點。","evidence_level":"事實表數字","settle_metric":"2 月財測後的共識 FY2027 EPS","if_then":["若共識 FY2027 EPS 維持 33 美元以上且財測達標，重跑研究後建首筆，不超過 2%","若共識 FY2027 EPS 低於 33 美元，不建倉"]},{"axis":"前份空白欄位首次填入","cause":"方法變動","prior_field":["moat_trend","runway_post_y5","archetype","cycle_position","p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份這些欄位都是空值：配置結論與角色、護城河方向、成長跑道、公司類型、循環位置、情境機率、最大跌幅。","side_b":"本次首次填入：護城河持平、成長跑道中等、循環股兼品質成長、循環中段、牛 20／基 50／熊 30、最大跌幅 −30%～−50%；配置結論與角色由程式算。","ruling":"這些是新填，不是看法反轉。循環位置判中段：訂單與情緒偏買，存貨與倍數中性，資料中心資本支出偏晚；P/B 事實表未涵蓋，訊號又互相矛盾，反動能檢查沒有全過。","evidence_level":"格式變動","settle_metric":"無","if_then":["若卡車與發電訊號在 2 月後一致偏買，循環位置改判早循環並重跑研究","若 Power Systems 接單放緩，循環位置改判晚循環，不建倉"]},{"axis":"綜合評等與價值陷阱理由更換","cause":"新證據","prior_field":["signal","trap"],"side_a":"前份綜合評等 B、價值陷阱中等，依據是題材真實但估值透支。","side_b":"本次同為 B、價值陷阱中等，依據換成估值已回落，但 Q3 實質低於預期、獲利基礎未確認。","ruling":"評等沒變，理由換了。估值壓力減輕，換成分母風險，兩者互抵。","evidence_level":"公司申報與法說","settle_metric":"FY2027 財測","if_then":["若 2 月財測三項全中，重跑研究後建首筆，不超過 2%","若有一項未達，不建倉，重啟條件順延一季"],"evidence_refs":["capital_markets_pricing#0"]},{"axis":"進場重啟條件變動","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"等 Fwd PE 分位回 60% 區（~$580-620 區）或 NA Class 8 prebuy 真實流入 FY27 EPS 共識上修後再進場","side_b":"2027 年 2 月財測：FY2027 營收成長中點≥7%、EBITDA 率中點≥18.5%，且財測後共識 FY2027 EPS≥33 美元，三項全中才重跑研究","ruling":"舊的價格條件已被跌破，卻沒有對應的基本面確認；管理層 11 月 5 日也說預購有限，舊的事件條件失去依據。進場改看獲利基礎，這是目前唯一的卡點。","evidence_level":"公司法說","settle_metric":"2 月財測三項","if_then":["三項全中，重跑研究後進場，首筆不超過 2%","有一項未達，不進場"]},{"axis":"Single Thing 由空白改為資料中心訂單取消","cause":"方法變動","prior_field":null,"side_a":"前份唯一致命點為空值，未設定。","side_b":"超大規模客戶對大型發電機組出現實質訂單取消或遞延，公司揭露排程由 2028 下半年往前縮短，或多年協議被改約。","ruling":"五年路徑裡敏感度最大的單項是資料中心增量，所以定在這裡，不是定在較戲劇性的法規或訴訟事件。","evidence_level":"估算，輸入來自公司目標","settle_metric":"每季訂單排程月份","if_then":["若事件發生，持有就清倉，未持有就取消重啟條件","若排程延伸到 2029 年以後，Bull 機率上調 5 個百分點並重跑研究"]},{"axis":"減碼與清倉門檻整理","cause":"方法變動","prior_field":null,"side_a":"前份未設砍倉指標；門檻散在風險列：Engine 段 EBITDA margin 連 2 季 < 8% 觸發減倉；連 4 季 Power Systems YoY < +5% → thesis 反轉，估值倍數 reset 至 17-18x。","side_b":"Engine 段 EBITDA 率連 2 季<8% 減碼；Power Systems 年增連 4 季<+5% 或 EBITDA 率連 4 季<22% 清倉；大型機組排程縮短到 2027 年內清倉；保固費用率連 2 季>3% 減碼。","ruling":"原門檻全部保留。只退休 17–18 倍的倍數重設，因為現價已是 15.2 倍。新增項目針對這次才浮現的訂單與新平台保固風險。","evidence_level":"前份紀錄與公司法說","settle_metric":"分部 EBITDA 率與年增率","if_then":["若 Engine 段連 2 季低於 8%，減碼一半","若 Power Systems 連 4 季年增低於 5%，清倉"]},{"axis":"前份卡車與發電門檻修訂","cause":"新證據","prior_field":null,"side_a":"2026 NA Class 8 production ≥ 320,000 units；Power Systems FY26-FY27 EBITDA margin 平均 ≥ 26%。","side_b":"公司預測 2026 年北美重卡 24–25 萬輛、中型 12.5–13 萬輛；FY2026 Power Systems EBITDA 率指引 25.1–25.6%。","ruling":"32 萬輛單看重卡沒達到，含中型是 36.5–38 萬輛，舊口徑本來就不清楚，退休，改成 2027 年重卡產量持平。26% 在全年指引下也達不到，改成 25% 以上，並保留連 2 季低於 25% 就削弱的規則。","evidence_level":"公司法說","settle_metric":"FY2027 重卡產量、Power Systems EBITDA 率","if_then":["若 2027 年重卡產量低於 22 萬輛，Base 的 FY2027 EPS 下調到 32 美元，不建倉","若連 2 季 Power Systems EBITDA 率低於 25%，停止加碼"]},{"axis":"管理層對預購的說法改變","cause":"新證據","prior_field":null,"side_a":"2026-08-04 Rumsey：some prebuy is coming in，中型車財測納入略高的預購；2026-05-21 Engine 總裁：明年第一季會有量的停頓。","side_b":"2026-11-05 Rumsey：pretty limited prebuy，需求是週期低點的真實回升；中型車預測下修到 12.5–13 萬輛，客戶在等 NCP。","ruling":"數字上接受預購有限，中型車下修、客戶在等，確實不像大規模預購。需求回升還沒證實，5 月講過的第一季停頓 11 月也沒有撤回。可調和，是時間差與程度差。","evidence_level":"法說逐字稿","settle_metric":"2027 Q1 北美重卡產量與 Engine 段 EBITDA 率","if_then":["若 2027 Q1 北美重卡產量季減超過 15%，不建倉","若產量持平且 Engine 段 EBITDA 率≥12%，H2 視為成立，可按重啟條件進場"]},{"axis":"Power Systems 利潤率走勢","cause":"新證據","prior_field":null,"side_a":"CFO（2026-11-05）：Q4 約 22.5% 不是往後的水準，軌跡沒有根本改變。","side_b":"前份記 Q1 29.5%，之後 Q2 24.5%、Q3 25.4%、Q4 隱含約 22.5%；小機組需求、儲能案與新產能投入都可能拉低組合。","ruling":"管理層的歸因不採信也不否定，標為未證。預先登記：2027 Q1、Q2 連續低於 24%，就算歸因不成立。","evidence_level":"法說逐字稿，部分為隱含計算","settle_metric":"2027 Q1、Q2 Power Systems EBITDA 率","if_then":["若連續兩季低於 24%，停止加碼並下調 Base 的 2030 年 EBITDA 率假設","若兩季都在 25% 以上，H1 維持"]},{"axis":"Q3 表面達標與實質品質","cause":"新證據","prior_field":null,"side_a":"Q3 EPS 8.25 美元，接近共識 8.28 美元。","side_b":"8.25 美元含每股 0.54 美元離散稅項利多，扣掉是 7.71 美元，低於共識 6.9%；營收 94.4 億美元也低於約 98.7 億美元預期。","ruling":"採後者。Q3 實質上營收和獲利都低於預期，只有利潤率好。共識數字來自聚合摘要，未逐字核對，但方向不受影響。11-07 快照沒反映，FY2027 的 34.81 美元還沒被重新檢驗。","evidence_level":"法說逐字稿＋聚合摘要","settle_metric":"2 月財測後的共識 FY2027 EPS","if_then":["若共識下修到 33 美元以下，不建倉並下調 Base","若共識維持 33 美元以上且財測達標，重跑研究後建首筆"],"evidence_refs":["capital_markets_pricing#0","end_markets#1"]},{"axis":"股價與共識背離、現在就買的最強論證","cause":"價格變動","prior_field":null,"side_a":"現在就買的最強論證：Q3 利潤率創高，接單超預期，排程到 2028 下半年，超大規模客戶有超過訂單期的合約承諾；資料中心訂單國際已與美國持平，可緩衝美國政治風險；股價半年跌 33%，只有今年 EPS 15.2 倍、明年 12.9 倍。","side_b":"不買的理由：跌幅原因事實表未涵蓋；共識還沒反映 Q3；現價要 FY2031 EPS 47.6 美元才有一成年報酬；2027 指引 2 月才出，EPA 規則 12 月才定。","ruling":"先不買。股價先跌、共識後跟是時間差，可調和。等三個月的代價是可能買貴，買錯的代價是在 −30% 到 −50% 的路徑上持有；兩者比較，等待划算。若市場對、共識錯，FY2027 共識會在 2 月下修。","evidence_level":"事實表、法說","settle_metric":"2 月財測三項","if_then":["股價回到 104 週均線 465 美元以上而 2 月財測未出：不追","股價跌到 400 美元以下、12 月 EPA 定案 NCP 可轉嫁、沒有訂單取消：分批反買，首筆不超過 1%","反向條件：2 月財測有一項未達，不建倉，重啟條件順延一季"]},{"axis":"產業態勢","cause":"新證據","prior_field":null,"side_a":"競爭惡化：Caterpillar 發電銷售 +72%，Generac 資料中心積壓約 16 億美元，PACCAR 擴自製引擎。","side_b":"結構轉好：訂單排到 2028 下半年，大型引擎供應商少，EPA 2027 讓每台卡車成本增加約 1 萬美元，多在動力系統。","ruling":"雙向拉鋸。第三軸是法規與替代技術：EPA 2027 即將定案，中國電動卡車正在替代柴油。兩邊都有出處，份額方向沒有一手數據，不能裁成單邊。","evidence_level":"公司申報、媒體與搜尋摘要","settle_metric":"資料中心份額、PACCAR 占比","if_then":["若 PACCAR 占比低於 11% 且北美重卡產量年增，停止加碼","若 X10 帶動重卡份額上升有數據，定價力加回 1 分"],"evidence_refs":["substitute_technology#2","supply_demand_durability#3","customer_second_source#0"]}],"triggers":[{"n":1,"text":"2 月財測確認 2027 年獲利基礎","type":"估值rearm","maps_to":"H3","metric":"FY2027 營收成長與 EBITDA 率指引中點，財測後共識 FY2027 EPS","threshold":"營收成長≥7%、EBITDA 率≥18.5%、共識 EPS≥33 美元，三項全中","action":"重跑研究，通過才建首筆，不超過 2%","source_freq":"Q4 財報與法說，一年一次","date":"2027-02"},{"n":2,"text":"資料中心大型機組訂單被取消或遞延","type":"Single Thing","maps_to":"H1","metric":"大型機組訂單排程與多年協議","threshold":"排程縮短到 2027 年內，或揭露協議取消、遞延","action":"清倉","source_freq":"每季法說","date":null,"evidence_refs":["supply_demand_durability#3"]},{"n":3,"text":"Power Systems 成長或利潤率轉弱","type":"假設驗證","maps_to":"H1","metric":"Power Systems 營收年增與 EBITDA 率","threshold":"連 2 季年增<+10% 或 EBITDA 率<25%","action":"停止加碼","source_freq":"每季 8-K 分部表","date":"2027-02"},{"n":4,"text":"Q4 補出貨沒有兌現，供應鏈的一次性歸因就不成立","type":"風險","maps_to":"R1","metric":"Q4 Distribution 營收、全年營收成長","threshold":"Distribution<38 億美元或全年成長<9.5%","action":"不追","source_freq":"Q4 財報","date":"2027-02","evidence_refs":["end_markets#1","capital_markets_pricing#0"]},{"n":5,"text":"EPA 定案不利","type":"風險","maps_to":"R5","metric":"NCP 金額與過渡安排","threshold":"NCP 無法全額轉嫁，或定案延到 2027 年","action":"不追","source_freq":"EPA 公告","date":"2026-12"},{"n":6,"text":"Engine 段利潤率跌破底線","type":"減碼","maps_to":"R5","metric":"Engine 段 EBITDA 率","threshold":"連 2 季<8%","action":"減碼","source_freq":"每季 8-K 分部表","date":null,"evidence_refs":["cyclical_prior_downcycle_behavior#2"]},{"n":7,"text":"發電論點反轉","type":"清倉","maps_to":"H1","metric":"Power Systems 營收年增與 EBITDA 率","threshold":"連 4 季年增<+5% 或 EBITDA 率<22%","action":"清倉","source_freq":"每季 8-K 分部表","date":null},{"n":8,"text":"新平台保固失控","type":"風險","maps_to":"R6","metric":"保固費用占營收","threshold":"連 2 季>3%（目前約低 2%）","action":"減碼","source_freq":"每季 10-Q","date":null,"evidence_refs":["product_recall_warning#0","product_recall_warning#1","major_events#1","major_events#2"]},{"n":9,"text":"Hydrogenics 電解槽費用超出預期","type":"風險","maps_to":"R9","metric":"停用建議的財務影響","threshold":"單次費用>1 億美元或轉為召回","action":"不追","source_freq":"每季 10-Q","date":"2027-02"},{"n":10,"text":"成本與關稅吸收失敗","type":"風險","maps_to":"R7","metric":"毛利率年增減，CFO 對價格減成本的說法","threshold":"毛利率連 2 季年減","action":"停止加碼","source_freq":"每季財報","date":null,"evidence_refs":["reg_tariff_export#0","reg_tariff_export#2","reg_tariff_export#3","geo_supply_chain#0","geo_supply_chain#1"]},{"n":11,"text":"排放訴訟出現新費用或程序升級","type":"風險","maps_to":"R8","metric":"新增應計、集體認證、刑事程序","threshold":"單筆應計≥2.5 億美元或集體認證且和解不利減碼一半；刑事介入則清倉","action":"減碼","source_freq":"10-Q 訴訟附註","date":null,"evidence_refs":["regulatory_antitrust#0","major_events#3","lawsuit_class_action#0"]},{"n":12,"text":"PACCAR 占比續降","type":"風險","maps_to":"R4","metric":"PACCAR 占合併銷售比","threshold":"<11% 且北美重卡產量年增","action":"停止加碼","source_freq":"10-K，一年一次","date":"2027-02","evidence_refs":["customer_second_source#0","customer_second_source#1","customer_concentration_credit#0"]},{"n":13,"text":"股價先跌、基本面未損時的試單","type":"加碼","maps_to":"H1","metric":"股價、EPA 定案、訂單排程","threshold":"股價≤400 美元，NCP 可轉嫁，無訂單取消","action":"分批反買，首筆不超過 1%，2 月財測前不再加","source_freq":"每日股價、事件","date":null},{"n":14,"text":"2 月財測後複審","type":"複審日期","maps_to":"H1","metric":"三項假設與全部風險列","threshold":"Q4 財報公布","action":"重跑研究","source_freq":"一次","date":"2027-02"}],"kill_metrics":[{"metric":"Power Systems 營收年增","bear_threshold":"連 4 季<+5%","window":"4 季","source":"8-K 分部表","last_status":"ok"},{"metric":"Power Systems EBITDA 率","bear_threshold":"連 2 季<25% 削弱，連 4 季<22% 清倉","window":"2–4 季","source":"8-K 分部表","last_status":"warning"},{"metric":"Engine 段 EBITDA 率","bear_threshold":"連 2 季<8%","window":"2 季","source":"8-K 分部表","last_status":"ok"},{"metric":"全公司 EBITDA 率","bear_threshold":"連 2 季<16.5% 削弱，連 4 季<15% 反轉","window":"2–4 季","source":"8-K","last_status":"ok"},{"metric":"大型機組訂單排程","bear_threshold":"由 2028 下半年縮短到 2027 年內","window":"每季","source":"法說","last_status":"ok"},{"metric":"北美 Class 8 月訂單","bear_threshold":"2027 H1 月訂單<15,000 輛","window":"2027 H1","source":"ACT Research（事實表只到 2026 年 5 月）","last_status":"unknown"},{"metric":"北美 Class 8 電動滲透率","bear_threshold":">10%","window":"3–5 年","source":"事實表未涵蓋，資料缺口","last_status":"unknown"}],"action_conditions":{"rearm_trigger":"2027 年 2 月財測：FY2027 營收成長中點≥7%、EBITDA 率中點≥18.5%，且財測後共識 FY2027 EPS≥33 美元，三項全中才重跑研究","exec_line":"未持有先不動。三項全中後重跑研究，通過才建首筆，不超過 2%；股價跌到 400 美元以下、12 月 EPA 定案 NCP 可轉嫁且無訂單取消，可先試 1%。","holding_cap":"3%"}},"decision_inputs":{"signal":"B","ma":"🟠","cycle_position":"中循環","cycle_verdict":"未觸發","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":false,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等 2027 年 2 月 Q4 財報的 FY2027 指引：營收成長中點≥7%、EBITDA 率中點≥18.5%，且財測後共識 FY2027 EPS≥33 美元。"},"thesis":{"H":[{"id":"H1","text":"資料中心備援電力需求撐住 Power Systems 與 Distribution，資料中心營收由約 50 億美元成長到 2030 年 90 億美元以上，Power Systems EBITDA 率守在 25% 以上。","2y":"FY2027 Power Systems 營收年增≥10%，EBITDA 率≥25%；大型機組訂單排程維持到 2028 下半年之後。","5y":"2030 年資料中心營收≥90 億美元，高馬力產能 55GW 投產後 Power Systems EBITDA 率仍≥25%。","10y":null,"threshold":"2026 年發電營收 +15–25%，Power Systems 營收 +15–18%、EBITDA 率 25.1–25.6%；2030 年資料中心營收 90 億美元以上。","source":"康明斯 8-K 分部表、2026-11-05 法說、2026-05-21 投資人日。","drift_rule":"連 2 季 Power Systems 年增<+10% 或 EBITDA 率<25% 削弱；連 4 季年增<+5% 反轉。"},{"id":"H2","text":"北美卡車由週期低點回升，EPA 2027 分階段切換沒有造成斷層，NCP 轉嫁給客戶，Engine 段利潤率守住。","2y":"2027 年北美重卡產量與 2026 年大致持平（24–25 萬輛）；Engine 段 EBITDA 率≥12%；NCP 全額轉嫁。","5y":"2028 後段新平台脫離約 18 個月的保固提列期後，Engine 段 EBITDA 率高於 FY2026 指引上緣 12.75%；X10 帶動重卡份額上升。","10y":null,"threshold":"FY2026 Engine 段 EBITDA 率指引 12.25–12.75%；北美重卡 24–25 萬輛；中型 12.5–13 萬輛。","source":"康明斯 8-K、季度法說、EPA 定案公告、ACT Research 月度訂單。","drift_rule":"2027 H1 月訂單<15,000 輛削弱；連 2 季新平台上量出問題反轉。"},{"id":"H3","text":"全公司 EBITDA 率由 FY2026 約 18.2% 升到 2030 年 20% 以上，增量利潤率 25% 以上，反映發電組合與營運紀律，不是景氣高點的暫時現象。","2y":"FY2027 EBITDA 率≥18.5%，FY2028≥19%。","5y":"FY2030 EBITDA 率≥20%，營收 450–500 億美元。","10y":null,"threshold":"2030 年 EBITDA 率>20%、營收 450–500 億美元、增量利潤率 25% 以上。","source":"2026-05-21 投資人日、每季 8-K。","drift_rule":"連 2 季全公司 EBITDA 率<16.5% 或 Power Systems<24% 削弱；連 4 季全公司<15% 或 Power Systems<22% 反轉。"}],"R":[{"id":"R1","text":"Q3 延後的出貨在 Q4 補不回來，全年指引再下修。Q4 指引隱含營收年增 15%、Distribution 季增約 23%。","h_ref":"H1","clock":"⚡","threshold":"Q4 Distribution<38 億美元或全年成長<9.5%，供應鏈的一次性歸因就不成立。","evidence_refs":["end_markets#1","capital_markets_pricing#0"]},{"id":"R2","text":"資料中心資本支出暫停，或同業擴產壓縮訂單與定價。","h_ref":"H1","clock":"🔥","threshold":"連 2 季 Power Systems 年增<+10% 或 EBITDA 率<25% 削弱；連 4 季年增<+5% 反轉。","evidence_refs":["supply_demand_durability#3","substitute_technology#2"]},{"id":"R3","text":"電動卡車與其他替代技術壓縮內燃機市場，中國已見影響。","h_ref":"H2","clock":"🐢","threshold":"北美 Class 8 電動滲透率>10%（3–5 年內，事實表未涵蓋現值，資料缺口），且判斷機率≥50% 才砍倉。","evidence_refs":["competitive_share_entrants#1"]},{"id":"R4","text":"PACCAR 提高自製引擎比重，或其他客戶改採自製、他廠。","h_ref":"H2","clock":"🐢","threshold":"PACCAR 占合併銷售<11% 且北美重卡產量年增。","evidence_refs":["customer_second_source#0","customer_second_source#1","customer_concentration_credit#0"]},{"id":"R5","text":"EPA 2027 切換造成需求斷層，或預購後回吐。公司 5 月曾說明年第一季會有量的停頓。","h_ref":"H2","clock":"🔥","threshold":"2026 H2 月訂單<25,000 輛警示（事實表只到 2026 年 5 月，資料缺口）；2027 H1 月訂單<15,000 輛削弱；Engine 段 EBITDA 率連 2 季<8% 減碼。","evidence_refs":["cyclical_prior_downcycle_behavior#2"]},{"id":"R6","text":"新平台上市與召回推高保固。L9 燃油管召回約 39,052 件，PD7000 軟體召回約 411–413 台，金額未揭露。","h_ref":"H3","clock":"🔥","threshold":"保固費用占營收連 2 季>3%（目前約低 2%）。","evidence_refs":["major_events#1","major_events#2","product_recall_warning#0","product_recall_warning#1"]},{"id":"R7","text":"關稅、貨運與單一來源零件推高成本。CFO 說下半年價格減成本略為負值。","h_ref":"H3","clock":"🔥","threshold":"毛利率連 2 季年減，視為吸收失敗。","evidence_refs":["reg_tariff_export#0","reg_tariff_export#2","reg_tariff_export#3","geo_supply_chain#0","geo_supply_chain#1"]},{"id":"R8","text":"排放案的後續監管與證券集體訴訟 Baker v. Cummins，現況未核實，受影響金額與和解日期事實表未涵蓋。","h_ref":"H3","clock":"🐢","threshold":"單筆新增應計≥2.5 億美元，或集體認證且和解不利則減碼一半；刑事介入則清倉。","evidence_refs":["regulatory_antitrust#0","major_events#3","lawsuit_class_action#0"]},{"id":"R9","text":"Hydrogenics 電解槽停用建議的財務影響尚在評估，未計入指引。","h_ref":"H3","clock":"⚡","threshold":"單次費用>1 億美元或轉為召回。"}],"single_thing":{"description":"超大規模客戶對大型發電機組出現實質訂單取消或遞延，公司揭露排程由 2028 下半年往前縮短，或多年協議被改約。","why_fatal":"這是五年路徑裡最大的單一變數。資料中心營收增量 40 億美元，用 Power Systems 25.4% 的 EBITDA 率、23% 稅率、1.3 億股粗算，每股約 6 美元，占 Base 五年 EPS 增量 18.4 美元的三分之一；Distribution 的安裝利潤還沒算，本益比也會同步由 14 倍往 11 倍掉。卡車下行幅度也大，但屬已知週期，已在 Bear 路徑內。","if_happens":"持有就清倉，未持有就取消重啟條件；Base 下移到 Bear 路徑，重跑研究。","how_monitor":"每季法說的大型機組訂單排程月份與多年協議揭露，再對照主要雲端業者的資本支出指引（事實表未涵蓋數字）。","probability":"12–24 個月內約 20%。訂單排到 2028 下半年且部分合約更長，短期取消機率低；但美國資料中心的能源與環保爭議已被法說問及，積壓又集中在少數客戶。"}},"appendix_a":{"growth_durability":6,"quality_score":7,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":12.93,"peg_fy2":0.77,"stress":{"pass":null,"total":null}},"eps_meta":{"base_eps_path":{"FY2025A":20.5,"FY2026E":29.59,"FY2027E":34.81,"FY2028E":40.69},"fy_end_month":12,"eps_basis":"GAAP 稀釋 EPS；FY2025A 含 Accelera 相關費用，共識來自 2026-11-07 Koyfin 快照，尚未反映 Q3 財測收斂，EPS 家數事實表未涵蓋。"},"catalysts":[{"date":"2026-12","date_precision":"month","type":"regulatory","event":"EPA 2027 最終規則預計公布，NCP 金額是主要未知數。","impact":"高","watch":"NCP 能否全額轉嫁，過渡安排是否改變。"},{"date":"2027-01","date_precision":"month","type":"product","event":"X10 與 X15 新平台開始限量生產。","impact":"中","watch":"上量品質、保固提列。"},{"date":"2027-02","date_precision":"month","type":"guidance","event":"Q4 財報與 FY2027 財測。","impact":"高","watch":"營收成長、EBITDA 率、Power Systems 指引、Q4 補出貨。"},{"date":"2027-Q3","date_precision":"quarter","type":"product","event":"X10 全面量產，X15 第四季接續。","impact":"中","watch":"新舊平台切換是否造成訂單斷層。"},{"date":"2028-Q1","date_precision":"quarter","type":"capacity","event":"20GW 新增產能進入較大幅度的上線期，7 公升新引擎 1 月上市。","impact":"高","watch":"新增供給是否被訂單消化，Power Systems 定價。"}],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8(val爭議)","pacing":[],"holding_cap":null,"audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟠'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟡', moat_trend='→', week26=-33.31, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='循環/商品', cycle_position='中循環', moat='B', moat_trend='→', cycle_gates_pass=False"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈機械讀數判定不可用，baseline rows 8/9/9b/10 的估值條件視為不可判 → 落 row8 觀望（保守方向）","hit":true,"basis":"val_denominator_disputed=True, val(機械讀數)='🟡'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"requires_critic":[]}}
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
