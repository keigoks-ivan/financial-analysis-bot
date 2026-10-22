你是 DD 管線 v20 的判斷層閘（gate），標的 MSCI（20261022）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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
- `f_kpi0_total_operating_revenue_`（q1_business）｜Total operating revenue (GAAP)＝867.0 $M｜期間與口徑：Q2 FY2026（季末 2026-06-30，公告 2026-07-21）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 ir.msci.com「MSCI Reports Financial Results for Second Quarter and Six Months 2026」（numbers.latest_quarter_kpis.items[0]，as_of Q2 FY2026（季末 2026-06-30，公告 2026-07-21））
  - 註記：consensus 約 $864.08M，實際 $867.0M 略勝（來源：web_search 彙整市場預期，非本站 dd_numbers_extra 結構化欄）
- `f_kpi1_adjusted_ebitda_margin_n`（q1_business）｜Adjusted EBITDA margin (non-GAAP)＝62.1 %｜期間與口徑：Q2 FY2026（季末 2026-06-30，公告 2026-07-21）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 ir.msci.com Q2 FY2026 press release（Adjusted EBITDA $538.5M，YoY +13.5%）（numbers.latest_quarter_kpis.items[1]，as_of Q2 FY2026（季末 2026-06-30，公告 2026-07-21））
  - 註記：未查得 sell-side 對 Adj. EBITDA margin 的共識數字
- `f_kpi2_gaap_operating_margin`（q1_business）｜GAAP operating margin＝56.2 %｜期間與口徑：Q2 FY2026（季末 2026-06-30，公告 2026-07-21）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：10-Q（SEC EDGAR msci-20260630.htm）與公司新聞稿一致：營業利益 $487.5M／營收 $867.0M（numbers.latest_quarter_kpis.items[2]，as_of Q2 FY2026（季末 2026-06-30，公告 2026-07-21））
  - 註記：未查得共識數字（GAAP operating margin 非 sell-side 常態追蹤指標）
- `f_kpi3_free_cash_flow_non_gaap`（q1_business）｜Free cash flow (non-GAAP)＝326.4 $M｜期間與口徑：Q2 FY2026（季末 2026-06-30，公告 2026-07-21）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 ir.msci.com Q2 FY2026 press release（numbers.latest_quarter_kpis.items[3]，as_of Q2 FY2026（季末 2026-06-30，公告 2026-07-21））
  - 註記：未查得共識數字
- `f_kpi5_retention_rate`（q1_business）｜Retention Rate＝95.3 %｜期間與口徑：Q2 FY2026（季末 2026-06-30，公告 2026-07-21）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 ir.msci.com Q2 FY2026 press release（numbers.latest_quarter_kpis.items[5]，as_of Q2 FY2026（季末 2026-06-30，公告 2026-07-21））
  - 註記：不適用（公司自報營運指標，非 sell-side 財務預估項目）
- `f_kpi6_index_analytics_organic_`（q1_business）｜Index／Analytics organic recurring subscription Run Rate growth＝Index 11.1% / Analytics 6.6% %｜期間與口徑：Q2 FY2026（季末 2026-06-30，公告 2026-07-21）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 ir.msci.com Q2 FY2026 press release（numbers.latest_quarter_kpis.items[6]，as_of Q2 FY2026（季末 2026-06-30，公告 2026-07-21））
  - 註記：不適用
- `f_earnings_recency`（q1_business）｜最近一次財報日＝2026-10-20 date｜期間與口徑：2026-10-20／距今 2 個交易日｜kind：realized
  - 來源：—（numbers.earnings_recency，as_of 2026-10-20）
- `f_peer_msci_gross_margin_pct`（q2_moat）｜MSCI 毛利率＝82.97 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MSCI.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_msci_operating_margin_pct`（q2_moat）｜MSCI 營業利益率＝55.66 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MSCI.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_msci_fcf_margin_pct`（q2_moat）｜MSCI FCF 利潤率＝44.77 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MSCI.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_spgi_operating_margin_pct`（q2_moat）｜SPGI 營業利益率＝41.56 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.SPGI.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_spgi_fcf_margin_pct`（q2_moat）｜SPGI FCF 利潤率＝34.57 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.SPGI.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_mco_operating_margin_pct`（q2_moat）｜MCO 營業利益率＝46.1 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MCO.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_mco_fcf_margin_pct`（q2_moat）｜MCO FCF 利潤率＝36.36 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MCO.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_fds_operating_margin_pct`（q2_moat）｜FDS 營業利益率＝29.55 %｜期間與口徑：TTM ending 2026-05-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.FDS.operating_margin_pct，as_of TTM ending 2026-05-31（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_fds_fcf_margin_pct`（q2_moat）｜FDS FCF 利潤率＝29.05 %｜期間與口徑：TTM ending 2026-05-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.FDS.fcf_margin_pct，as_of TTM ending 2026-05-31（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝19.52 USD/share｜期間與口徑：2026-10-21／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261021.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-10-21）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝22.35 USD/share｜期間與口徑：2026-10-21／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261021.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-10-21）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝25.35 USD/share｜期間與口徑：2026-10-21／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261021.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-10-21）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝3524.32 USD m｜期間與口徑：2026-10-22／yfinance revenue_estimate 0y 平均（15 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-10-22）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝3838.57 USD m｜期間與口徑：2026-10-22／yfinance revenue_estimate +1y 平均（15 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-10-22）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi4_stock_based_compensation`（q1_business）｜Stock-based compensation as % of revenue（推算）＝2.93 %｜期間與口徑：Q2 FY2026（季末 2026-06-30，公告 2026-07-21，推算值）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：推算：Q2 10-Q 現金流量表揭露 H1 FY2026 SBC 累計 $73.1M，減去 Q1 10-Q（三個月至2026-03-31）揭露的 Q1 SBC $47.7M，得 Q2 單季 SBC ≈ $25.4M；MSCI 10-Q 現金流量表僅揭露年初至今累計數，未單獨揭露單季數字（numbers.latest_quarter_kpis.items[4]，as_of Q2 FY2026（季末 2026-06-30，公告 2026-07-21，推算值））
  - 註記：不適用
- `f_kpi7_fy2026_guidance_q2`（q1_business）｜FY2026 全年財測（管理層 guidance，於Q2財報會議重申／更新）＝Opex $1,535–1,575M；Adjusted EBITDA Expense $1,340–1,370M；Capex $160–170M；Free Cash Flow $1,485–1,545M USD millions（區間）｜期間與口徑：隨 Q2 FY2026 財報發布（2026-07-21）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司新聞稿 ir.msci.com Q2 FY2026 press release（numbers.latest_quarter_kpis.items[7]，as_of 隨 Q2 FY2026 財報發布（2026-07-21））
  - 註記：不適用
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝6191.5 USD m｜期間與口徑：2026-10-22／yfinance 最新一季：總債務 6544.2、現金 352.7（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-10-22）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝72.7 m shares｜期間與口徑：2026-10-22／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-10-22）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝1.315 %｜期間與口徑：2026-10-22／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-10-22）
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝604.46 USD｜期間與口徑：2026-10-21（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-10-21（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝30.97 x｜期間與口徑：2026-10-21／分母＝FY1 EPS 19.52，分子＝快照價 604.46｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-10-21）
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝33.03 x｜期間與口徑：2026-10-21（RTH 收盤，UTC）／4 個年度端點內的分位＝0.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-10-21（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝0.0 %｜期間與口徑：2026-10-21（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-10-21（RTH 收盤，UTC））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝13.18 x｜期間與口徑：2026-10-21（RTH 收盤，UTC）／4 個年度端點內的分位＝0.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-10-21（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝15.04 x｜期間與口徑：2026-10-21（RTH 收盤，UTC）／4 個年度端點內的分位＝0.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-10-21（RTH 收盤，UTC））
- `f_rsi14`（q5_valuation）｜RSI(14)＝69.5｜期間與口徑：2026-10-21（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-10-21（RTH 收盤，UTC））
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝0.13 %｜期間與口徑：2026-10-21（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-10-21（RTH 收盤，UTC））
- `f_consensus_rev_fy1_pct`（q5_valuation）｜FY1 共識修正＝-0.76 %｜期間與口徑：2026-10-21／兩份 Koyfin 快照之間的 EPS 修正幅度（19.67 → 19.52）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261021.xlsx（numbers.consensus_revision.fy1.revision_pct，as_of 2026-10-21）
- `f_consensus_rev_fy2_pct`（q5_valuation）｜FY2 共識修正＝-0.18 %｜期間與口徑：2026-10-21／兩份 Koyfin 快照之間的 EPS 修正幅度（22.39 → 22.35）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261021.xlsx（numbers.consensus_revision.fy2.revision_pct，as_of 2026-10-21）

### findings_digest 中方向為負或來源衝突的條目（13 條）
- `competitive_share_entrants#1`（competitive_share_entrants｜方向 -｜狀態 ok）：風險因子：對手與新進入者可能用 AI 以較低價格推出競爭產品，客戶也可能以 AI 自建客製指數、風險分析等取代 MSCI 產品；競爭可能造成降價或失去份額。
  - 來源：SEC EDGAR MSCI 10-K FY2025 Item 1A Risk Factors（as_of 2026-02-06）｜affects：moat_trend、decision_inputs.bear
- `competitive_share_entrants#2`（competitive_share_entrants｜方向 -｜狀態 ok）：最大客戶之一 BlackRock 同時是競爭者／分銷商，可能終止部分或全部關係。
  - 來源：SEC EDGAR MSCI 10-K FY2025 Item 1A Risk Factors（as_of 2026-02-06）｜affects：decision_inputs.bear、moat_trend
- `customer_second_source#0`（customer_second_source｜方向 -｜狀態 ok）：MSCI's FY2023 10-K discloses BlackRock as its largest client organization by revenue, at 9.8% of consolidated operating revenues, with 95.4% of BlackRock's revenue to MSCI coming from asset-based fees on ETFs/non-ETF products using MSCI indexes — a concentration/single-client dependency risk factor.
  - 來源：MSCI Inc. Form 10-K FY2023 (SEC EDGAR)（as_of 2023-12-31）｜affects：decision_inputs.bear、moat_trend
- `customer_concentration_credit#0`（customer_concentration_credit｜方向 -｜狀態 ok）：BlackRock is MSCI's largest client, accounting for 10.8% of consolidated operating revenues for FY2025; 96.5% of that BlackRock-derived revenue comes from asset-based fees on BlackRock's ETFs and non-ETF products tracking MSCI indexes.
  - 來源：MSCI Inc. 10-K FY2025 (filed 2026)（as_of 2025-12-31）｜affects：thesis.R、decision_inputs.bear、valuation
- `customer_concentration_credit#1`（customer_concentration_credit｜方向 -｜狀態 ok）：MSCI discloses risk that its largest clients (including BlackRock) may negotiate lower asset-based fees, stop using MSCI indexes, or cancel/reduce usage, which could have a material adverse effect on results.
  - 來源：MSCI Inc. 10-K FY2025 (filed 2026), Risk Factors（as_of 2025-12-31）｜affects：thesis.R、decision_inputs.bear
- `customer_concentration_credit#2`（customer_concentration_credit｜方向 -｜狀態 ok）：BlackRock accounted for 18.7% of MSCI's Index segment operating revenues for FY2025 (vs. 17.4% in FY2022), indicating rising within-segment concentration over time.
  - 來源：MSCI Inc. 10-K FY2025 (filed 2026)（as_of 2025-12-31）｜affects：thesis.R、decision_inputs.bear
- `regulatory_antitrust#1`（regulatory_antitrust｜方向 -｜狀態 ok）：MSCI 10-K 揭露：2024 年 11 月歐盟通過 ESG 評等透明度與誠信規範 (EU) 2024/3005，要求在歐盟境內營運的 ESG 評等提供者須於 2026 年 7 月 2 日起取得 ESMA 授權或註冊；MSCI 表示其部分永續與氣候相關產品預期將受此規範管轄。
  - 來源：MSCI Inc. Form 10-K FY2025 (SEC EDGAR)（as_of 2026-02-01）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：MSCI FY2025 10-K 風險因素：關稅、報復性關稅與貿易緊張可能影響投資人配置與客戶預算、延後或取消訂閱；地緣與貿易政策變動可能限制其在特定司法管轄區提供產品、取得營運所需技術，或降低需求；亦受出口管制、制裁等法規約束。
  - 來源：SEC EDGAR｜MSCI 10-K FY2025 Item 1A（as_of 2026-02-06）｜affects：decision_inputs.bear、thesis.R
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：台灣占 MSCI 新興市場指數(EM Index)權重達 24.8%（2026-04-30 資料），為指數內最大權重國家，主因 AI 驅動半導體需求；同期資訊科技板塊權重由 31.8% 升至近 37%。此為 MSCI 旗艦指數產品在地緣風險區域（台灣/中國）的集中曝險。
  - 來源：MSCI - Markets in Motion: Taiwan at the Top, EM Weight Breakdown（as_of 2026-04-30）｜affects：thesis.R、decision_inputs.bear、moat_trend
- `end_markets#4`（end_markets｜方向 -｜狀態 ok）：被動ETF市場2026年估值達$16.8兆，但主動型ETF數量已在2025年6月超越被動型ETF；主動ETF資產達$1.47兆、近三年CAGR 59%，顯示主動策略在ETF資金流結構性搶佔份額，對MSCI核心被動指數授權/資產基礎費成長模型構成潛在逆風。
  - 來源：Active vs. Passive ETFs: How the 2026 Active Surge Changes the Math - etf.com（as_of 2025-12-31）｜affects：thesis.R、decision_inputs.bear、valuation
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：AI/LLM 工具可低成本自動解析企業永續揭露、複製部分 ESG 評等結果；若機構投資人認為 MSCI ESG Ratings 與 AI 生成替代品區隔不足，MSCI 的評等定價溢價可能被侵蝕
  - 來源：PitchGrade Research - "MSCI: Index Licensing and ESG Data Franchises in the Age of AI-Powered Analytics"（as_of 2026-01-29）｜affects：moat_trend、thesis.R、decision_inputs.bear
- `capital_markets_pricing#1`（capital_markets_pricing｜方向 -｜狀態 ok）：MSCI 2026 Q2 財報後上修 2026 全年費用 guidance：營運費用上修至 $1,535M–$1,575M（原 $1,490M–$1,530M），Adjusted EBITDA 費用上修至 $1,340M–$1,370M（原 $1,305M–$1,335M），主因近期併購（含 First Street）及 AUM 動能超過先前假設
  - 來源：MSCI Reports Financial Results for Second Quarter and Six Months 2026 (businesswire/ir.msci.com)（as_of 2026-07-21）｜affects：thesis.R、valuation、decision_inputs.bear
- `capital_markets_pricing#2`（capital_markets_pricing｜方向 -｜狀態 ok）：Q2 2026 財報後，JPMorgan（Alexander Hess）維持 Overweight 但目標價由 $742 下修至 $700；Evercore ISI（David Motemeden）維持 Outperform 但目標價由 $746 下修至 $722，理由是費用上升軌跡導致估值重新校準
  - 來源：BigGo Finance: "MSCI Beats Q2 Estimates but Analysts Slash Price Targets on Rising Costs"（as_of 2026-07-22）｜affects：valuation、thesis.R、triggers

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 4 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MSCI_20261022/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":1264.0,"bear_5y_price":440.0,"p_bull_pct":25,"p_bear_pct":30,"upside_5y_pct":46.2,"ev5y_pct":39.9,"irr_base_pct":7.9,"asym_ratio":3.3,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":19.52,"pe":30.97,"basis":"FY2026 共識 EPS（當年度、調整後口徑）；終端倍數同樣以終端年度 EPS 為分母"},"eps":{"bull":[22.6,26.0,30.0,34.5,39.5],"base":[22.1,25.0,28.0,31.0,34.0],"bear":[20.0,20.3,20.8,21.4,22.0]},"pe":{"bull":32,"base":26,"bear":20},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":1.315,"net_buyback":0},"second_stage":{"bull_cagr_pct":12,"base_cagr_pct":9},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### MSCI_Q2_2026_Earnings_Call_20260721.md
- 2026-07-21｜CFO Andrew Wiechmann｜guidance：永續與氣候合併板塊未來兩季 recurring net new sales 預期約零到小幅為負（原話："roughly zero to slightly negative"）
- 2026-07-21｜CFO Andrew Wiechmann｜guidance：First Street 交割（Q3）後預期增加約 $10M 訂閱 run rate（原話："add about $10 million of subscription run rate"）
- 2026-07-21｜CFO Andrew Wiechmann｜guidance：費用指引上調；4 月曾說會落在高端區間（原話："towards the high end of the expense guidance ranges"）
- 2026-07-21｜CFO Andrew Wiechmann｜margin：費用指引上調原因之一：績效股票薪酬與獎金應計（原話："performance stock-based comp and bonus accruals"）
- 2026-07-21｜CFO Andrew Wiechmann｜margin：利息費用上調歸因於循環信貸餘額上升（原話："driven by the higher revolver balances"）
- 2026-07-21｜CFO Andrew Wiechmann｜margin：自由現金流指引上調歸因於收款增加（原話："it's driven by a pickup in collections"）
- 2026-07-21｜CFO Andrew Wiechmann｜margin：ABF 費率下滑：Q2 主因為資產成長與組合轉移（原話："it was heavily mix shift driven"）
- 2026-07-21｜CFO Andrew Wiechmann｜margin：BlackRock 協議延長後，部分大型產品底價（floor）降低（原話："we do now have lower floors on certain large products"）
- 2026-07-21｜CFO Andrew Wiechmann｜margin：Analytics 利潤率：管理層不看單一板塊或單季利潤率（原話："we don't focus heavily on the margin in any specific segment"）
- 2026-07-21｜CFO Andrew Wiechmann｜margin：Analytics 費用年比受去年或有對價回沖影響（原話："contingent consideration reversal"）
- 2026-07-21｜CEO Henry Fernandez｜capital_allocation：本季至昨日回購 $147M 股份（原話："repurchasing $147 million of MSCI shares"）
- 2026-07-21｜CEO Henry Fernandez｜capital_allocation：管理層稱費用上調是自願加碼投資而非被迫（原話："we voluntarily feel that we will want to invest more"）
- 2026-07-21｜CEO Henry Fernandez｜commitment：CEO 表示對看淡者的賣盤願意接手（原話："we're prepared to put a bid on the other side of that trade"）
- 2026-07-21｜CFO Andrew Wiechmann｜commitment：承諾可彈性調整投資與費用（原話："levers to flex investments up and expenses down"）
- 2026-07-21｜CFO Andrew Wiechmann｜competition：永續市場整合中，MSCI 稱在取得市佔（原話："we are capturing share gains in a consolidating market"）
- 2026-07-21｜CEO Henry Fernandez｜competition：CEO：客戶向 MSCI 集中，將是最後倖存的大型業者（原話："we're going to be the last big entity standing"）
- 2026-07-21｜CFO Andrew Wiechmann｜risk：永續取消（尤其美洲）為顯著逆風（原話："cancels, particularly in the Americas"）
- 2026-07-21｜CEO Henry Fernandez｜risk：CEO 稱永續為長期循環性下行而非結構性（原話："protracted cyclical downturn on the use of sustainability"）
- 2026-07-21｜CEO Henry Fernandez｜risk：CEO 改口：先前預期約兩年（原話："going to be like a couple of year process"）
- 2026-07-21｜CEO Henry Fernandez｜risk：主動型管理人資金流仍受抑（原話："the flows are still muted"）
- 2026-07-21｜CEO Henry Fernandez｜risk：管理層預告逐季變異將增加（原話："there will be more variability quarter-by-quarter"）
- 2026-07-21｜CEO Henry Fernandez｜product：兩季內推出 80 多項新產品（原話："80-plus in the last 2 quarters"）
- 2026-07-21｜CFO Andrew Wiechmann｜product：上半年新產品對新銷售貢獻年增約 40%（原話："it's up around 40% compared to a year ago"）
- 2026-07-21｜CFO Andrew Wiechmann｜product：推出主動 ETF 專用授權（原話："we actually recently launched our active financial product"）
- 2026-07-21｜CFO Andrew Wiechmann｜product：簽下首份模型訓練授權，目前貢獻小（原話："we actually very recently signed our first training license"）
- 2026-07-21｜CEO Henry Fernandez｜product：IndexAI Insights 2 月推出，已逾千客戶使用（原話："We already have over 1,000 clients using IndexAI Insights"）
- 2026-07-21｜CEO Henry Fernandez｜product：與 UBS 的合作目前僅是條款書層級，未計入數字（原話："which is not in the numbers, by the way"）
- 2026-07-21｜CEO Henry Fernandez｜customer：避險基金與交易商 index 新銷售增逾三倍（原話："more than tripled our index recurring net new sales"）
- 2026-07-21｜CEO Henry Fernandez｜customer：避險基金本季為紀錄最佳（原話："best quarter on record with 19% subscription run rate growth"）
- 2026-07-21｜CEO Henry Fernandez｜customer：CEO 稱大型避險基金的指數套利付費偏低（原話："getting paid too little for the index arbitrage"）
- 2026-07-21｜CFO Andrew Wiechmann｜customer：非 ETF 被動型 AUM 約 $5 兆（原話："the non-ETF passive AUM is around $5 trillion as of June 30"）
- 2026-07-21｜CFO Andrew Wiechmann｜customer：價格上調對新銷售貢獻近幾季穩定（原話："the overall contribution has been pretty consistent"）
- 2026-07-21｜CFO Andrew Wiechmann｜customer：Q3 迄今 ETF 資金流仍強（原話："continued to see exceptional cash flows in the ETFs"）
- 2026-07-21｜CEO Henry Fernandez｜customer：CEO 稱避險基金與交易商處於前 2、3 局（原話："the first 2, 3 innings would be my guess"）
- 2026-07-21｜CEO Henry Fernandez｜customer：Analytics 銷售偏弱，CEO 歸因為不規則（原話："It's all lumpiness."）
- 2026-07-21｜CEO Henry Fernandez｜competition：CEO 與一年前口徑對比：當時說情況不佳，現在相反（原話："telling you things were not looking that great"）

### 問答異常語氣（迴避／改口／保留）
- MSCI_Q2_2026_Earnings_Call_20260721.md｜問：Manav Patnaik：本季訂閱銷售略低於預期，前瞻動能如何｜答法：CEO 未直接回應低於預期的數字，轉談新產品管線、過去三季優於共識及逐季變異
- MSCI_Q2_2026_Earnings_Call_20260721.md｜問：Owen Lau：ABF 費率下滑的來源（分級定價 vs 競爭）及未來費率｜答法：CFO 歸因組合轉移與底價調整，稱費率為路徑依賴，未給前瞻費率，也未正面回應競爭因素
- MSCI_Q2_2026_Earnings_Call_20260721.md｜問：Kelsey Zhu：Analytics 利潤率偏軟及下半年軌跡｜答法：CFO 稱不看單季或單板塊利潤率，未提供下半年利潤率軌跡
- MSCI_Q2_2026_Earnings_Call_20260721.md｜問：Toni Kaplan：MCP 資料銷售的牽引力與未來基期波動｜答法：CEO 只談避險基金波動，未回答 MCP 問題

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 3 | 2 |
| customer_second_source | found | 1 | 4 |
| customer_concentration_credit | found | 4 | 4 |
| supply_demand_durability | found | 2 | 4 |
| regulatory_antitrust | found | 3 | 3 |
| reg_tariff_export | found | 1 | 2 |
| geo_supply_chain | found | 1 | 4 |
| end_markets | found | 5 | 6 |
| substitute_technology | found | 2 | 4 |
| channel_business_model_shift | found | 2 | 2 |
| capital_markets_pricing | found | 4 | 4 |
| major_events | found | 3 | 3 |

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260929","verdict":"進場","role":"衛星","H":{"status":"unavailable"},"R":{"status":"unavailable"},"single_thing":null,"kill_metrics":null,"rearm_trigger":"股價回到 474 美元以下（FY1 本益比 24 倍），且 Index 有機訂閱 run rate 年增仍在 10% 以上","irr_base_pct":8.7,"ev5y_pct":45.1,"drift_watch_prior":{"dca_verdict":"進場","dca_role":"衛星","signal":"B","val":"🟡","ma":"🟠","trap":"🟡","moat_trend":"→","runway_post_y5":"🟢","asym_ratio":3.8,"ev5y_pct":45.1,"irr_base_pct":8.7,"max_dd_pct":-45,"bull_5y_price":1185.0,"bear_5y_price":401.4,"p_bull_pct":25,"p_bear_pct":30,"rearm_trigger":"股價回到 474 美元以下（FY1 本益比 24 倍），且 Index 有機訂閱 run rate 年增仍在 10% 以上","price_at_dd":542.72,"archetype":"品質複利成長","cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"MSCI","date":"2026-10-22","schema":"v15.2","contract":"v19","company_name":"MSCI Inc."},"oneliner":"全球股票基準與投資分析的標準制定者，Q3 淨新銷售創紀錄、留存回升；但 FY1 本益比 31 倍，管理層明言不擴張利潤率，五年基準年化約 9%。生意好，價格只算合理，等 536 美元以下再加碼。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MSCI_20261022/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MSCI_20261022/scenario.json","answers":{"q1_business":{"verdict":"向資產管理商、ETF 發行商、避險基金與資產擁有者收錢：訂閱占大宗，另按掛鉤 MSCI 指數的資產規模抽基點費（Q3 資產費 run rate 近 10 億美元，創紀錄）。錢卡在「投資標竿」這一節點：基金合約與公開說明書寫死比較基準，換掉要改文件、重新對投資人揭露。","reasoning":"Q2 FY2026 營收 8.67 億美元，調整後 EBITDA 利潤率 62.1%，GAAP 營益率 56.2%，季自由現金流 3.26 億。年度財報：FY2025 營收 31.3 億，FY2022–FY2025 年複合約 11.7%，營益率維持在 53.5%～54.8%。Q3 法說（2026-10-20 CEO）：總營收 +12.4%，資產費營收 +25%，訂閱營收 +8%，調整後 EPS +14%。分部為 Index、Analytics、Sustainability and Climate、All Other–Private Assets，各分部營收占比事實表未涵蓋。單點依賴：BlackRock 占 FY2025 合併營收 10.8%、Index 分部 18.7%（FY2022 為 17.4%），其中 96.5% 是資產費。這既是集中度風險，也是護城河證據：2026-01 修約，期限延至 2035-03-31。產業時鐘判 II（擴張）：被動化與 ETF 資金流仍在擴張，Q3 股票 ETF 淨流入 760 億美元，對標資產近 23 兆。供需耐久性：訂閱端屬結構性持久，留存率 95.3%，年增 0.9pp；資產費端隨股市週期起落，股市反轉時會先掉。","fact_refs":["f_kpi0_total_operating_revenue_","f_kpi1_adjusted_ebitda_margin_n","f_kpi2_gaap_operating_margin","f_kpi3_free_cash_flow_non_gaap","f_kpi5_retention_rate","f_kpi6_index_analytics_organic_","f_earnings_recency"],"verdict_values":{"revenue_quality":"高：以訂閱為主，留存率 95.3%；資產費部分隨股市市值與 ETF 資金流波動，是主要的週期性來源","unit_econ_note":"TTM 毛利率 83.0%、FCF 利潤率 44.8%；新產品與新客群建在既有指數與因子模型基礎設施上，邊際成本低","archetype":{"primary":"品質複利成長","secondary":null,"confidence":"高","fingerprint":"高留存訂閱加資產費，毛利率 83%，FCF 對淨利轉換率約 1.2 倍"},"industry":{"clock_phase":"II","sd_verdict_source":"結構性持久（訂閱端）：留存率 95.3%（前一年 94.4%），Index 留存逾 97%；資產費端屬週期性，隨股市反轉（Q2 新聞稿、2026-10-20 CFO）","bargaining":{"up":"上游是資料與雲端供應商，可替代，議價權在 MSCI","down":"下游大型資產管理商可壓資產費基點：H1 掛鉤 ETF 平均基點下滑，BlackRock 修約後部分大型產品底價降低（2026-07-21 CFO）","geo":"營收跨三大區；Q3 淨新銷售 EMEA +74%、亞太 +36%、美洲 +26%"},"profit_pool_dir":"利潤池往客製指數、交易生態（避險基金、券商、做市商）與私募資料移動，MSCI 有跟上：客製指數訂閱 run rate +26%、私募資本方案 +19%","tam_table":{"expanded":false,"reason":"事實表未涵蓋 TAM 與滲透率；利潤池遷移改用分部 run rate 成長代理，見成長題分部表"}}}},"q2_moat":{"verdict":"→：執行力在擴大（留存率回升，Q3 Index、Analytics、私募資本方案淨新銷售創紀錄），定價權穩中略鬆（資產費基點下滑、BlackRock 底價調降），兩者相抵，判為穩定。","reasoning":"機制是基準標準加轉換成本：基金合約、績效考核與交易生態都綁在 MSCI 指數上，掛鉤的產品越多越難換。對同業的利潤率差：營益率 55.7%，對 MCO 46.1%、SPGI 41.6%、FDS 29.6%，最強同業差 9.6pp；FCF 利潤率 44.8%，對 36.4%／34.6%／29.1%。同業 ROIC 與歷史趨勢事實表未涵蓋，只能用單期利潤率差替代，無法判斷差距在擴大還是收窄。評分：執行力 9（留存升、淨新銷售創紀錄、員工數持平下完成四筆收購）；定價權 8（年度調價貢獻穩定，但最大客戶拿到較低底價、資產費基點下滑）。屬訂閱型資料業，以綜合分加敘述評 A，依據是轉換成本落在決策最小單位（基金合約層）。三項威脅都屬點對點，不扣分。","fact_refs":["f_peer_msci_gross_margin_pct","f_peer_msci_operating_margin_pct","f_peer_msci_fcf_margin_pct","f_peer_spgi_operating_margin_pct","f_peer_spgi_fcf_margin_pct","f_peer_mco_operating_margin_pct","f_peer_mco_fcf_margin_pct","f_peer_fds_operating_margin_pct","f_peer_fds_fcf_margin_pct","f_kpi5_retention_rate"],"verdict_values":{"moat":{"mechanism":"全球股票基準標準：基金合約、公開說明書與績效考核綁定 MSCI 指數，資產費與訂閱兩頭收；避險基金、券商的交易生態圍繞指數建立，掛鉤產品越多越難換","execution":9,"pricing":8,"grade":"A","trend":"→","trend_evidence":"留存率 95.3%（前一年 94.4%），Q3 約 95%、年增 30bp，Index 留存逾 97%；但掛鉤 ETF 平均基點下滑（H1 新聞稿），BlackRock 修約後部分產品底價降低（2026-07-21 CFO）","competitor_notes":[{"name":"SPGI","strategy_note":"S&P 道瓊指數是美國基準的主要對手；SPGI 營益率 41.6%，比 MSCI 低約 14pp，但指數業務未拆分，無法逐業務線比較"},{"name":"MCO","strategy_note":"主力是信評與風險分析，與 MSCI 在私募信用、風險資料有交集；營益率 46.1%，是利潤率最接近的同業"},{"name":"FDS","strategy_note":"在投組分析上與 MSCI Analytics 正面競爭（10-K 列名）；營益率 29.6%，利潤率差距說明 MSCI 分析產品依附在指數與因子模型上，而不是單賣工具"}],"spread_notes":null,"peer_na_reason":"同業 ROIC 與投入資本事實表未涵蓋，以營益率與 FCF 利潤率差替代","threats":[{"level":"🟡","text":"AI 讓對手以低價推出替代品，客戶也可能自建客製指數與風險分析；ESG 評等最容易被 AI 複製。目前留存率仍在上升，客戶偏好透過 MSCI 自家應用直連（2026-10-20 Munari），屬點對點威脅","p":30,"evidence_refs":["competitive_share_entrants#1","substitute_technology#0","substitute_technology#1"]},{"level":"🟡","text":"BlackRock 同時是最大客戶、股東與競爭者，可壓資產費，或把產品換到自家／他家指數；合約延至 2035 年，短期機率低","p":15,"evidence_refs":["competitive_share_entrants#2","customer_concentration_credit#1"]},{"level":"🟡","text":"主動型 ETF 數量已超過被動型，資金若持續由被動轉主動，資產費成長會變慢；但主動 ETF 也在採用 MSCI 的主動 ETF 授權與投組工具","p":25,"evidence_refs":["end_markets#4"]}],"roic_durability":{"quadrant":"高利益率×高周轉","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者（投資組合經理、風控）、決策者（投資長、產品委員會）、付款者（資產管理商、ETF 發行商）三方一致：基準是募資與績效考核的必需品，延後購買的代價高；對標資產近 23 兆，留存率 95.3%"},{"item":"決策層級","level":"🟢","text":"替代性要在基金合約層衡量：換基準要改公開說明書，並經董事會與投資人揭露；Index 留存逾 97%、資產管理客戶 98%（2026-10-20 CFO），BlackRock 合約延至 2035-03-31"},{"item":"價值鏈分配","level":"🟡","text":"ETF 發行商自身面臨費率壓縮，會向上游壓指數費：掛鉤 ETF 平均基點下滑，BlackRock 修約後部分產品底價降低；最大客戶同時是競爭者，有自建能力"},{"item":"社會容忍度","level":"🟡","text":"歐美監管者與媒體高度關注指數業；MSCI Limited 為英國 FCA 授權的基準管理機構，EU ESG 評等規範自 2026-07-02 起要求 ESMA 授權。資產費若推到經濟上限容易招來監管，實際做法是讓基點逐步下滑來換規模"}],"roiic":"事實表未涵蓋投入資本與折舊攤銷，無法照公式精算。替代讀數：FY2022→FY2025 營業利益由約 12.1 億增至約 17.1 億（營收×營益率），增加約 5.1 億；同期資本支出年約 1.6–1.7 億（FY2026 指引）加小型收購，增量報酬極高但不可精算","reinvest_rate":"低：成長投資多以營業費用列帳，而非資本化。FY2026 資本支出指引中值 1.65 億，對 FY2025 自由現金流 14.6 億約 11%，其餘現金用於股利與回購","endo_ceiling":11,"formula_note":"「增量報酬×再投資率」在此不適用：成長投資多走營業費用（CEO 2026-10-20 表示，AI 在既有業務省下的費用全數再投入新產品），資本化投入資本很小。改以「營收有機成長×利潤率持平」作內生上界，約 11%：FY2022–FY2025 營收年複合 11.7%，取略低值，反映資產費正處週期高點"}}}},"q3_growth":{"verdict":"🟢：Index 訂閱加速（Q3 有機 11.7%），私募資本方案 +19%，客製指數 +26%；避險基金、資產擁有者、財富管理與做市商等新客群構成第二、三條曲線，Y5 之後跑道寬。","reasoning":"成長來源以量為主（ETF 資產規模、新客群），價為輔：調價對新銷售的貢獻近幾季穩定（2026-07-21 CFO）。EPS 另有回購減股加成。共識 EPS FY2026→FY2028 由 19.52 升至 25.35 美元，年增約 14.0%（事實表無分析師家數）；共識營收 FY2027 +8.9%。內生上界約 11%，缺口約 3pp，歸因兩項：一是淨回購，Q3 回購 6.27 億美元，2024 年以來累計 44 億、近 800 萬股；二是 FY2026 一次性費用的基期效應，包括遣散費多 1,000–1,500 萬、績效股票應計多 1,500–2,000 萬、收購費用約 2,000 萬（2026-10-20 CFO）。缺口不是靠倍數重評。滲透率事實表未涵蓋；跑道判斷依據是：對標資產 23 兆中只有約 8 兆是被動管理，做市商尚未滲透、還沒進數字（2026-10-20 CEO），私募與財富管理正在放量。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_kpi6_index_analytics_organic_","f_kpi5_retention_rate"],"verdict_values":{"growth":{"driver_mix":"量為主（ETF 資產規模、避險基金與資產擁有者等新客群），價為輔（年度調價貢獻穩定），EPS 另靠回購減股約 2–3pp","runway_years":"≥10","runway_post_y5":"🟢","endo_ceiling_basis":"營收有機成長約 11%，在利潤率持平下直接轉為營業利益成長（FY2022–FY2025 營收年複合 11.7%）；成長投資多費用化，公式值不適用，詳見護城河題的報酬持續期段","segments":[{"item":"Index 有機訂閱 run rate 年增（Q3）","value":"11.7%（Q2 11.1%，逐季加速）"},{"item":"資產費 run rate（Q3）","value":"近 10 億美元，創紀錄；H1 資產費營收 +26.6%，但平均基點下滑"},{"item":"Analytics 有機訂閱 run rate 年增（Q3）","value":"7.5%（Q2 6.6%）"},{"item":"私募資本方案訂閱 run rate 年增（Q3）","value":"19%"},{"item":"Real Assets 有機訂閱 run rate 年增（Q3）","value":"2%"},{"item":"Climate run rate 年增（Q3，不含 First Street）","value":"8%；永續取消偏高，Q4 淨新銷售預期持平到小幅正"}],"decay_signals":[{"signal":"EPS 成長顯著高於營收成長（差＞5pp）","lit":true,"evidence":"共識 FY2027 EPS +14.5%，營收 +8.9%，差 5.6pp"},{"signal":"產業估值倍數近 3 年系統性下移","lit":true,"evidence":"trailing 本益比、P/S、EV/S 皆落在近四個年度端點最低；同業倍數事實表未涵蓋"},{"signal":"TAM 萎縮或被替代技術壓縮","lit":false,"evidence":"永續評等需求受壓、AI 替代風險存在，但只限單一分部，且 Climate run rate 仍 +8%，未亮"},{"signal":"毛利率連 2 季年減","lit":false,"evidence":"TTM 毛利率 83.0%，高於 FY2025 的 82.4%"},{"signal":"FCF／淨利＜0.75 連 2 年","lit":false,"evidence":"FY2025 約 1.21 倍"},{"signal":"SBC／營收＞5% 且逐年上升","lit":false,"evidence":"Q2 推算約 2.9%"}],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"現金轉換極佳，但回購價格偏高、且靠舉債支撐：FY2025 自由現金流對淨利約 1.21 倍，SBC 約占營收 2.9%；Q3 回購均價 562 美元，換算盈餘殖利率只有約 3.5%，資金部分來自循環信貸。","reasoning":"現金去向：FY2026 自由現金流指引 14.85–15.45 億、資本支出 1.6–1.7 億，股息殖利率約 1.3%，回購是最大去向（2026-07-01 至 10-19 回購 6.27 億）。淨負債 61.9 億，以 Q2 調整後 EBITDA 5.385 億年化約 21.5 億計算，約 2.9 倍；Q3 法說上調利息費用指引，原因是循環信貸餘額增加以支應回購，Q3 現金利息多付 5,000 萬美元以上。CEO 個人 2024 年以來買進 5.7 萬股、3,010 萬美元，利益與股東一致。收購都是小型補強。","fact_refs":["f_kpi3_free_cash_flow_non_gaap","f_kpi4_stock_based_compensation","f_kpi7_fy2026_guidance_q2","f_net_debt_m","f_shares_diluted_m","f_dividend_yield_ttm"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":false,"passed":null,"input":"2026 年三筆收購（Compass Financial、ApeVue、First Street 現金 1.2 億美元）皆遠小於市值 5%，已實現增量報酬事實表未涵蓋，不計分"},{"name":"buyback_yield","applicable":true,"passed":false,"input":"Q3 回購均價 562 美元，對 FY2026 共識 EPS 19.52 美元，盈餘殖利率約 3.5%；10 年期公債殖利率事實表未涵蓋，但 10 年期要低於 1.5% 才會過門檻，判不過"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"上半年 SBC 7,310 萬美元，年化約 1.5 億，對市值約 439 億，毛稀釋約 0.3%／年；回購使股數淨減"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長主要來自有機訂閱與資產費，2026 年三筆收購屬小型補強，不承重；回購影響已寫在現金去向與 EPS 缺口歸因"}}}},"q5_valuation":{"verdict":"現價 604 美元要求未來五年調整後 EPS 年增約 11–12%，終端還要守住 26 倍以上，才換得年化約 9%。EPS 部分我相信，倍數擴張我不信，結論是合理偏貴，不追價。","reasoning":"FY1 本益比 30.97 倍；FY2 約 27.0 倍（604.46÷22.35）。PEG＝30.97÷14.0≈2.2，屬偏貴。trailing 本益比 33.0 倍、P/S 13.2 倍、EV/S 15.0 倍，都是近四個年度端點中最低，顯示市場已在折價 AI 替代與永續風險；但只有四個點，不是五年分位。基準情境：五年 EPS 34 美元×26 倍＝884 美元，較現價 +46%，年化約 8%，加股息約 9%。Bull 1,264 美元，Bear 440 美元。賣方平均目標約 692 美元（2026-09 彙整），高於現價，方向上支持持有，不支持追價；Q2 後 JPM、Evercore 已下修目標價。同業前瞻倍數事實表未涵蓋，終端倍數無法用同業現值校準，只能以自身倍數區間定錨。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_pe_current","f_pe_percentile","f_ps_current","f_ev_s_current","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_dividend_yield_ttm"],"verdict_values":{"valuation":{"basis":"前瞻本益比與 PEG（品質複利型）","tier":"高品質金融資料與指數商","peers":{"expanded":false,"reason":"事實表的同業資料只有利潤率，沒有同業前瞻本益比，無法用倍數跨公司定錨"},"fwd_pe":30.97,"peg":2.22,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"FY1 本益比 31 倍、PEG 約 2.2，偏貴；但 trailing 本益比為近四個年度端點最低，五年基準年化約 9%，落在中段，兩者相抵判黃。五年分位：事實表只有四個年度端點，不外推","upside_short_pct":2.4,"upside_mid_pct":46.2,"denominator_disputed":false,"denominator_note":"共識 EPS 為調整後口徑，與 FY2025 GAAP 稀釋 EPS 15.69 美元口徑不同；本益比分母一律用共識前瞻值，不影響結論"}}},"q6_how_wrong":{"verdict":"🟡：兩項衰退信號亮燈（共識 EPS 跑贏營收逾 5pp、自身倍數下移）；不構成陷阱，但看錯的路徑很清楚：股市空頭打資產費，同時倍數壓縮。","reasoning":"最可能看錯的三處都寫在反證紀錄：資產費的市場風險、再投資吃掉經營槓桿、價格已先走。動能面：RSI 69.5，接近但未過 70；26 週報酬只有 +0.13%，四週漂移事實表未涵蓋，不判過熱。共識 FY1 EPS 近期小幅下修 0.76%，與 Q3 數字超預期方向相反，原因是費用上修。","fact_refs":["f_rsi14","f_week26_return_pct","f_consensus_rev_fy1_pct","f_consensus_rev_fy2_pct","f_pe_percentile"],"verdict_values":{"trap":{"verdict":"🟡","label":"倍數下移與 EPS 跑贏營收兩項亮燈"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":19.52,"pe":30.97,"basis":"FY2026 共識 EPS（當年度、調整後口徑）；終端倍數同樣以終端年度 EPS 為分母"},"eps":{"bull":[22.6,26.0,30.0,34.5,39.5],"base":[22.1,25.0,28.0,31.0,34.0],"bear":[20.0,20.3,20.8,21.4,22.0]},"pe":{"bull":32,"base":26,"bear":20},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":1.3,"net_buyback":0},"second_stage":{"bull_cagr_pct":12,"base_cagr_pct":9},"max_dd":{"lo":-45,"hi":-30,"basis":"較淺端：Bear 情境第一年 EPS 20 美元×20 倍＝400 美元，約 −34%。較深端：股市空頭時倍數超跌到 18 倍×19.5 美元≈351 美元，約 −42%，再加恐慌超跌取 −45%。資產費占比高，股市回檔會同時打 EPS 與倍數。歷史最大回撤事實表未涵蓋","trigger_time":null},"basis":{"bull":"Index 訂閱維持 12% 以上，私募與 Analytics 新客群放量，資產費搭上股市與被動化續升，EPS 年增約 15%；市場續給 32 倍","base":"共識前兩年略打折：第一年 22.1 美元，低於共識 22.35，反映 CEO 表明不擴張利潤率；之後年增 11%～10%；終端 26 倍，低於現值 31 倍；每股 EPS 已含回購減股，淨回購殖利率填 0，避免重複計算","bear":"股市空頭壓縮資產費、BlackRock 壓費、永續持續流失、利息上升，EPS 五年只到 22 美元；倍數壓到 20 倍（成長熄火降至 10% 的情境）"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"資產費隨股市市值與 ETF 資金流起落：H1 掛鉤股票 ETF 資產 +34.6%，但平均基點下滑；主動 ETF 三年資產年複合 59%；新興市場指數台灣權重 24.8%，地緣與關稅可能抑制資金配置與客戶預算","assumption":"股市長期上行、被動化持續，基點下滑被資產成長抵消","consequence":"股市空頭一年、資產規模縮水 25–30%，再加 BlackRock 壓費：資產費營收下滑，EPS 回到 19–20 美元，倍數同時壓到 20 倍，股價約 400–440 美元","ruling":"部分採納：資產費的市場風險已放進 Bear 情境（30% 機率、終端 20 倍）。結構性部分反駁：主動 ETF 轉型反而在採用 MSCI 的主動 ETF 專用授權與投組工具（2026-07-21 CFO、2026-10-20 Munari），Index 訂閱仍在加速","watch":"資產費 run rate 年增是否轉負；掛鉤 ETF 平均基點費率年降幅","evidence_refs":["end_markets#4","geo_supply_chain#0","reg_tariff_export#0","customer_concentration_credit#1"],"fact_refs":["f_kpi6_index_analytics_organic_"]},{"view":"論點失敗","evidence":"AI 讓對手低價推出替代品、客戶自建分析；ESG 評等可被 AI 複製；EU ESG 評等規範自 2026-07-02 起要求 ESMA 授權，增加合規成本；Q3 永續出現一筆大額縮單","assumption":"MSCI 的資料、模型與基準地位無法被 AI 低成本複製","consequence":"總留存率跌破 93%，調價能力失效，倍數下修","ruling":"多數反駁：Q3 留存約 95%、年增 30bp，Index 逾 97%；客戶透過 MSCI 自家應用使用內容的比例高於第三方連接器（2026-10-20 Munari）。風險集中在永續分部，已放進 Bear","watch":"總留存率；永續與氣候分部淨新銷售","evidence_refs":["competitive_share_entrants#1","substitute_technology#0","regulatory_antitrust#1"],"fact_refs":["f_kpi5_retention_rate"]},{"view":"論點成功但股東經濟變差","evidence":"CEO 2026-10-20 明言不擴張利潤率，增量經營槓桿全數再投資；2026 費用指引在 Q2 上修，Q3 再說會落在上緣；利息費用指引上調，因為循環信貸增加以支應回購；回購均價 562 美元，約 FY1 的 29 倍；Q3 超預期，自由現金流指引卻未上調","assumption":"再投資報酬如 CEO 所說很高，回購價格合理","consequence":"營收照長，但 EPS 成長降到 8–10%；以高倍數加槓桿回購會消耗股東資本","ruling":"採納為監測：Base 第一年 EPS 已低於共識，並設全年調整後 EPS 年增＜8% 為停止加碼條件","watch":"調整後 EPS 年增；淨負債對 EBITDA 倍數；FY2027 費用指引","evidence_refs":["capital_markets_pricing#1"],"fact_refs":["f_kpi7_fy2026_guidance_q2","f_net_debt_m"]},{"view":"價格已反映太多","evidence":"FY1 本益比 31 倍、PEG 約 2.2；股價自前份 542.72 漲到 604.46 美元（+11%），RSI 69.5，價格在 52／104／250 週均線之上；Q2 後賣方下修目標價（JPM 742→700、Evercore 746→722）；共識 FY1 EPS 近期下修 0.76%","assumption":"市場會持續給品質溢價","consequence":"若 EPS 只符合共識、倍數回到 26 倍，五年年化約 9%，一年報酬接近零","ruling":"採納：不追價，等 536 美元以下（FY2027 共識 24 倍）","watch":"FY2 本益比；共識修正方向","evidence_refs":["capital_markets_pricing#2"],"fact_refs":["f_fwd_pe_latest","f_rsi14","f_consensus_rev_fy1_pct","f_price_at_dd"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 🟠 → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=🟠","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 542.72 → 本次 604.46（+11.4%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=542.72","side_b":"本次 price_at_dd=604.46","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]裁決由 dd_decision.py 機械路由：前份 進場 → 本次 觀望","cause":"方法變動","prior_field":["dca_verdict"],"side_a":"前份 dca_verdict=進場","side_b":"本次 dca_verdict=觀望","ruling":"裁決是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。沒有單一輸入能還原，屬多欄共同：均線 🟠→🟡。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]角色由 dd_decision.py 機械路由：前份 衛星 → 本次 追蹤","cause":"方法變動","prior_field":["dca_role"],"side_a":"前份 dca_role=衛星","side_b":"本次 dca_role=追蹤","ruling":"角色是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。沒有單一輸入能還原，屬多欄共同：均線 🟠→🟡。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 542.72 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 542.72 美元：Bull 價 1,185、Bear 價 401.4，五年期望值 +45.1%，基準年化 8.7%，不對稱比 3.8","side_b":"本次情境、股價仍用 542.72 美元：Bull 價 1,264、Bear 價 440，五年期望值 +55.8%，基準年化 10.2%，不對稱比 5.85","ruling":"先換情境、股價不動：五年期望值多 10.7 個百分點，基準年化多 1.5 個百分點。不對稱比由 3.8 變為 5.85。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變好。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 542.72 美元：五年期望值 +55.8%，基準年化 10.2%，不對稱比 5.85","side_b":"本次情境、股價 604.46 美元：五年期望值 +39.9%，基準年化 7.9%，不對稱比 3.34","ruling":"再換股價、情境不動：起點價上漲 11.4%，五年期望值少 15.9 個百分點，基準年化少 2.4 個百分點，不對稱比由 5.85 降到 3.34。合計五年期望值比前份少 5.2 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"前份基本面結論欄","cause":"新證據","prior_field":["signal","val","trap","moat_trend","runway_post_y5","archetype","cycle_position"],"side_a":"前份：綜合訊號 B、估值黃燈、陷阱黃燈、護城河方向穩定、Y5 後跑道寬、品質複利成長、非循環股","side_b":"本次全數維持","ruling":"Q3 新證據（Index 訂閱加速至 11.7%、三條產品線淨新銷售創紀錄、留存年增 30bp）強化護城河與跑道判斷，但同時出現永續大額縮單、費用上修，正反相抵，結論不變","evidence_level":"公司新聞稿與法說原話","settle_metric":"Q4 Index 有機訂閱 run rate 年增","if_then":["若 Q4 Index 有機訂閱 run rate 年增 ≥11% 且總留存率 ≥95%，護城河方向轉 ↑ 的執行面條件成立，再看資產費基點是否止跌","若 Index 有機訂閱 run rate 年增跌破 10%，跑道改評中等、停止加碼"],"evidence_refs":[]},{"axis":"前份裁決、角色、情境機率與回撤","cause":"價格變動","prior_field":["p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份：股價 542.72 美元時進場；Bull／Bear 機率 25%／30%；最大回撤 −45%","side_b":"本次：股價 604.46 美元（+11%），基本面未變而價格先走，改為不追、等 536 美元以下；Bull／Bear 機率維持 25%／30%；最大回撤改為 −30%～−45% 的範圍","ruling":"漲幅來自價格而非證據（共識 EPS 反而小幅下修），依「價格先走、證據未到就不追」處理","evidence_level":"價格與共識快照","settle_metric":"FY2 本益比","if_then":["若股價回到 536 美元以下且 Index 有機訂閱 run rate 年增 ≥10%，分批加碼首筆三分之一","若股價續漲到 700 美元以上而共識 EPS 未上修，不追，持有者不加碼"],"evidence_refs":[]},{"axis":"估值重啟加碼門檻","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"股價回到 474 美元以下（FY1 本益比 24 倍），且 Index 有機訂閱 run rate 年增仍在 10% 以上","side_b":"股價回到 536 美元以下（FY2027 共識 EPS 24 倍），且 Index 有機訂閱 run rate 年增仍 ≥10%","ruling":"加碼門檻的分母由 FY2026 滾動到 FY2027：FY2026 已過三季，前瞻一年改用 FY2027 共識 22.35 美元；倍數 24 倍不變，價位由 474 升至 536 美元","evidence_level":"共識快照","settle_metric":"股價對 FY2027 共識 EPS 倍數","if_then":["若股價 ≤536 美元且 Index 有機訂閱 run rate 年增 ≥10%，分批加碼"],"evidence_refs":[]},{"axis":"清倉與減碼門檻","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設清倉或減碼指標","side_b":"本次設四條：Index 有機訂閱 run rate 年增＜8% 連 2 季則減碼；總留存率＜93% 連 2 季則減碼；BlackRock 旗艦產品改用他家指數則清倉重評；全年調整後 EPS 年增＜8% 則停止加碼","ruling":"前份缺門檻屬方法缺漏，本次補上；門檻取 Q2–Q3 實際值往下留緩衝","evidence_level":"公司新聞稿","settle_metric":"各季新聞稿營運指標","if_then":["若任一減碼條件成立，減碼一半","若 BlackRock 轉換指數成立，清倉並重跑研究"],"evidence_refs":[]},{"axis":"Single Thing 唯一致命點","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設 Single Thing","side_b":"BlackRock 把掛鉤 MSCI 指數的主要 ETF 改用他家或自家指數，或要求大幅降低資產費","ruling":"這是數學上最大的單一離散敏感項：BlackRock 占營收 10.8%，其中 96.5% 是高利潤的資產費；合約延至 2035 年，機率低，但發生即清倉重評","evidence_level":"10-K 與 8-K","settle_metric":"SEC 申報中的 BlackRock 合約與營收占比","if_then":["若 BlackRock 宣布主要產品轉換指數，清倉並重跑研究"],"evidence_refs":["customer_concentration_credit#0"]},{"axis":"不擴張利潤率對上共識 EPS 跑贏營收","cause":"新證據","prior_field":null,"side_a":"CEO 2026-10-20：不擴張利潤率，經營槓桿全數再投資；2026 費用落在指引上緣","side_b":"共識 FY2027 EPS +14.5%、營收 +8.9%，隱含利潤率擴張或大幅減股","ruling":"可調和（程度差異）：FY2026 一次性遣散、績效股票應計與收購費用在基期回落，加上回購減股，可解釋約 3–4pp；其餘要靠利潤率上升，與 CEO 說法衝突，所以 Base 第一年 EPS 取 22.1 美元，略低於共識","evidence_level":"法說原話與共識","settle_metric":"FY2027 費用指引（2027-01 Q4 法說）","if_then":["若 FY2027 調整後 EBITDA 費用指引年增 ≥ 營收共識增速，下修 Base EPS 並停止加碼","若費用指引年增 ≤6%，共識 EPS 可信，維持 Base"],"evidence_refs":["capital_markets_pricing#1","capital_markets_pricing#2"]},{"axis":"管理層前後說法：永續與 Analytics","cause":"新證據","prior_field":null,"side_a":"2026-07-21 CFO：永續與氣候未來兩季淨新銷售約零到小幅負；CEO：Analytics 偏弱「都是不規則」","side_b":"2026-10-20：Q3 永續取消偏高，有一筆大額縮單，Q4 改說持平到小幅正；Analytics 淨新銷售年增 63%，創紀錄","ruling":"Analytics 的不規則歸因已獲驗證；永續的說法有兌現，但仍在下行，加上 EU ESG 評等新規增加合規成本，暫時採信、不加分","evidence_level":"兩季法說原話","settle_metric":"Q4 永續與氣候淨新銷售","if_then":["若 Q4 永續與氣候淨新銷售轉負，管理層的永續說法證偽，Bear 機率上調至 35%","若 Q4 轉正且 Climate run rate 含 First Street 後 ≥12%，永續拖累見底"],"evidence_refs":["regulatory_antitrust#1"]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"不追：FY1 本益比 31 倍、PEG 2.2、RSI 69.5，價格比前份高 11%","side_b":"現在買：trailing 本益比為近四個年度端點最低；Q3 是基本面最強的一季（淨新銷售創紀錄、留存回升）；CEO 個人 2024 年以來買進 3,010 萬美元，公司以 562 美元回購 6.27 億；等價可能等不到","ruling":"不可調和（方向相反），選等價。依據：基準年化約 9%，落在中段；價格漲幅大於證據增強幅度。硬數據點是 FY2 本益比 27 倍","evidence_level":"價格、共識與法說","settle_metric":"FY2 本益比與 Q4 Index 訂閱成長","if_then":["若股價 ≤536 美元，分批加碼首筆三分之一","若 Q4 財報 Index 有機訂閱 run rate ≥12% 且 FY2027 共識 EPS 上修 ≥3%，不等價，以現價分批加碼首筆三分之一","反向：若股價續漲但共識下修，不加碼"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"驗證 Index 訂閱主引擎","type":"假設驗證","maps_to":"H1","metric":"Index 有機訂閱 run rate 年增","threshold":"≥10%；連 2 季＜8% 則減碼","action":"連 2 季＜8% 減碼一半","source_freq":"季報新聞稿／每季","date":"2027-01","evidence_refs":[]},{"n":2,"text":"BlackRock 主要 ETF 改用他家或自家指數","type":"Single Thing","maps_to":"single_thing","metric":"BlackRock 掛鉤 MSCI 指數的主要產品","threshold":"任一旗艦產品宣布轉換指數或重議資產費","action":"清倉並重跑研究","source_freq":"SEC 8-K、BlackRock 公告／事件","date":null,"evidence_refs":["customer_concentration_credit#0","competitive_share_entrants#2"]},{"n":3,"text":"AI 替代是否侵蝕客戶黏著","type":"風險","maps_to":"R2","metric":"總留存率","threshold":"＜93% 連 2 季","action":"減碼一半","source_freq":"季報新聞稿／每季","date":"2027-01","evidence_refs":["competitive_share_entrants#1","substitute_technology#0"]},{"n":4,"text":"費用上修吃掉獲利成長","type":"風險","maps_to":"R3","metric":"調整後 EBITDA 利潤率；全年調整後 EPS 年增","threshold":"利潤率＜58% 連 2 季，或全年 EPS 年增＜8%","action":"停止加碼","source_freq":"季報新聞稿／每季","date":"2027-01","evidence_refs":["capital_markets_pricing#1"]},{"n":5,"text":"資產費隨股市轉弱","type":"風險","maps_to":"R4","metric":"資產費 run rate 年增","threshold":"連 2 季轉負","action":"若留存與訂閱成長守住，視為市場波動，分批加碼；若訂閱同步轉弱，減碼","source_freq":"季報新聞稿／每季","date":null,"evidence_refs":["end_markets#4","geo_supply_chain#0"]},{"n":6,"text":"價格回到合理區","type":"估值rearm","maps_to":null,"metric":"股價對 FY2027 共識 EPS 倍數","threshold":"股價 ≤536 美元（24 倍）且 Index 有機訂閱 run rate 年增 ≥10%","action":"分批加碼首筆三分之一","source_freq":"每日股價","date":null,"evidence_refs":[]},{"n":7,"text":"倍數過熱","type":"減碼","maps_to":null,"metric":"股價對 FY2027 共識 EPS 倍數","threshold":"＞36 倍（約 805 美元）","action":"減碼三分之一","source_freq":"每日股價","date":null,"evidence_refs":[]},{"n":8,"text":"Q4 財報與 FY2027 指引後複審","type":"複審日期","maps_to":null,"metric":"FY2027 費用指引、Q4 淨新銷售","threshold":"財報公布","action":"重跑研究","source_freq":"一次","date":"2027-01","evidence_refs":[]}],"kill_metrics":[{"metric":"Index 有機訂閱 run rate 年增","bear_threshold":"＜8% 連 2 季","window":"2 季","source":"MSCI 季報新聞稿","last_status":"ok"},{"metric":"總留存率","bear_threshold":"＜93% 連 2 季","window":"2 季","source":"MSCI 季報新聞稿","last_status":"ok"},{"metric":"BlackRock 主要 ETF 是否改用他家指數","bear_threshold":"任一旗艦產品宣布轉換","window":"12 個月","source":"SEC 8-K、BlackRock 公告","last_status":"ok"},{"metric":"全年調整後 EPS 年增","bear_threshold":"＜8%","window":"1 個會計年度","source":"MSCI Q4 新聞稿與年報","last_status":"ok"}],"evidence_dismissed":[],"action_conditions":{"rearm_trigger":"股價回到 536 美元以下（FY2027 共識 EPS 24 倍），且 Index 有機訂閱 run rate 年增仍 ≥10%","exec_line":"已持有者續抱、不加碼；新資金等 536 美元以下分三筆買，每筆間隔至少一季財報；若 Q4 Index 訂閱 ≥12% 且 FY2027 共識上修 ≥3%，可不等價先買首筆"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場以 AI 替代與永續下滑為由壓低倍數（trailing 本益比為近四個年度端點最低），但 Q3 Index 訂閱加速到 11.7%、留存率升到約 95%，替代效應還沒出現在留存數字上","momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":true,"wait_for_price":true,"wait_for_price_condition":"等股價回到 536 美元以下（FY2027 共識 EPS 24 倍），且 Index 有機訂閱 run rate 年增仍 ≥10%","prior_verdict":"進場","prior_role":"衛星"},"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8w(原9)","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='A'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場以 AI 替代與永續下滑為由壓低倍數（trailing 本益比為近四個年度端點最低），但 Q3 Index 訂閱加速到 11.7%、留存率升到約 95%，替代效應還沒出現在留存數字上"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟢', val='🟡', moat_trend='→', week26=0.13, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position=None, moat='A', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":false,"basis":"signal='B', val='🟡'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":true,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"8w","condition":"判斷者宣告 wait_for_price（價格合理但要等）→ 原 row9 進場改觀望（等價格）","hit":true,"basis":"wait_for_price=True, 等待條件='等股價回到 536 美元以下（FY2027 共識 EPS 24 倍），且 Index 有機訂閱 run rate 年增仍 ≥10%'"},{"row":"QC-49","condition":"qc49_inherit_prior=True 但判斷者宣告 wait_for_price：不得把觀望承繼回進場（只往保守方向）","hit":false,"basis":"wait_for_price=True, prior_verdict='進場', 矩陣機械輸出='觀望'"},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":null,"requires_critic":[]},"thesis":{"H":[{"id":"H1","text":"Index 訂閱是主引擎，有機訂閱 run rate 維持兩位數成長","2y":null,"5y":"年增 ≥10%","10y":null,"threshold":"Index 有機訂閱 run rate 年增 ≥10%（Q3 為 11.7%）","source":"MSCI 季報新聞稿與法說","drift_rule":"連 4 季低於 9.5% 為削弱，連 6 季低於 9% 為反轉"},{"id":"H2","text":"客戶黏著不被 AI 與自建侵蝕：總留存率守住、訂閱整體穩定成長","2y":null,"5y":"總留存率 ≥94.5%，訂閱 run rate 年增 ≥8%","10y":null,"threshold":"總留存率 ≥94.5%（Q3 約 95%）；訂閱 run rate 年增 ≥8%（Q3 為 9%）","source":"MSCI 季報新聞稿","drift_rule":"連 4 季偏離門檻 ≥5% 為削弱，連 6 季偏離 ≥10% 為反轉"},{"id":"H3","text":"經營槓桿不被再投資全部吃光，每股獲利維持雙位數成長","2y":"調整後 EPS 年增 ≥12%","5y":null,"10y":null,"threshold":"FY2026、FY2027 調整後 EPS 年增 ≥12%（Q3 為 14%）","source":"MSCI 季報新聞稿與年度指引","drift_rule":"連 2 季偏離門檻 ≥5% 為削弱，連 3 季偏離 ≥10% 為反轉"}],"R":[{"id":"R1","text":"BlackRock 集中度上升且擁有議價權：占合併營收由 FY2023 的 9.8% 升至 FY2025 的 10.8%，占 Index 分部 18.7%，同時是競爭者；修約後部分大型產品底價降低（2026-07-21 CFO）","h_ref":"H2","clock":"🐢","threshold":"BlackRock 占 Index 分部營收升破 20%，同時掛鉤 ETF 平均基點年降逾 10%","evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#1","customer_concentration_credit#2","customer_second_source#0","competitive_share_entrants#2"]},{"id":"R2","text":"AI 讓對手低價替代、客戶自建指數與分析，ESG 評等首當其衝","h_ref":"H2","clock":"🔥","threshold":"總留存率＜93% 連 2 季","evidence_refs":["competitive_share_entrants#1","substitute_technology#0"]},{"id":"R3","text":"費用指引連續上修，管理層明言不擴張利潤率，EPS 成長可能低於共識","h_ref":"H3","clock":"⚡","threshold":"調整後 EBITDA 利潤率＜58% 連 2 季","evidence_refs":["capital_markets_pricing#1"]},{"id":"R4","text":"資產費是股市 beta：股市空頭、主動 ETF 分流、新興市場地緣與關稅衝擊，會同時壓資產規模與基點","h_ref":"H3","clock":"🔥","threshold":"資產費 run rate 年增連 2 季轉負","evidence_refs":["end_markets#4","geo_supply_chain#0","reg_tariff_export#0"]},{"id":"R5","text":"永續與氣候分部需求下行，加上 EU ESG 評等新規的授權與合規成本","h_ref":"H2","clock":"🐢","threshold":"永續與氣候分部淨新銷售連 2 季為負","evidence_refs":["regulatory_antitrust#1"]}],"single_thing":{"description":"BlackRock 宣布把掛鉤 MSCI 指數的主要 ETF 改用他家或自家指數，或要求大幅降低資產費","why_fatal":"BlackRock 占 FY2025 營收 10.8%、Index 分部 18.7%，其中 96.5% 是資產費，幾乎全數落到利潤；其他發行商也會跟著議價，基準不可替代的敘事被打破，倍數同步下修","if_happens":"清倉並重跑研究；EPS 約少一成，倍數往 20 倍靠攏","how_monitor":"SEC 8-K 重大合約項目、BlackRock 產品公告、10-K 最大客戶占比","probability":"約 3%（ETF 授權合約 2026-01 已延至 2035-03-31）"}},"appendix_a":{"growth_durability":8,"quality_score":9,"ai_risk":"🟡","long_term_confidence":"高","fpe_fy2":27.05,"peg_fy2":1.94,"stress":{"pass":4,"total":4}},"eps_meta":{"base_eps_path":{"FY2025A":15.69,"FY2026E":19.52,"FY2027E":22.35,"FY2028E":25.35},"fy_end_month":12,"eps_basis":"共識為調整後 EPS（Koyfin 快照）；FY2025A 只有年報 GAAP 稀釋 EPS 15.69，與共識口徑不同，以此為基期算的三年成長會被高估；可比的共識成長以 FY2026→FY2028 年增約 14.0% 為準"},"catalysts":[{"date":"2027-01","date_precision":"month","type":"guidance","event":"Q4 2026 財報與 FY2027 費用、資本支出指引","impact":"高","watch":"FY2027 調整後 EBITDA 費用年增對營收共識 +8.9%；Q4 淨新銷售與永續分部"},{"date":"2027-02","date_precision":"month","type":"other","event":"FY2026 年報揭露 BlackRock 營收占比與資產費結構","impact":"中","watch":"BlackRock 占合併與 Index 分部營收比是否續升"}]}
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
