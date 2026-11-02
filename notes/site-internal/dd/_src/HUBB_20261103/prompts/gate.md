你是 DD 管線 v20 的判斷層閘（gate），標的 HUBB（20261103）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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
- `f_kpi0_net_sales_gaap`（q1_business）｜Net sales (GAAP)＝1872.5 USD M（YoY +24.6%，其中 organic +11.3%、併購約 +13pp；QoQ +9.4%）｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-27）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（SEC 8-K Ex.99.1）（numbers.latest_quarter_kpis.items[0]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-27））
  - 註記：未取得
- `f_kpi1_adjusted_non_gaap_operat`（q1_business）｜Adjusted (Non-GAAP) operating income / margin＝25.5 %（調整後營業利益 476.8 USD M；上年同期 23.9%，+160bps）｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-27）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（SEC 8-K Ex.99.1）；分部：Utility 26.0%（+30bps）、Electrical 24.8%（+400bps）（numbers.latest_quarter_kpis.items[1]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-27））
  - 註記：未取得
- `f_kpi2_gaap_operating_income_ma`（q1_business）｜GAAP operating income / margin＝21.8 %（營業利益 408.7 USD M；上年同期 22.0%，-20bps）｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-27）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（SEC 8-K Ex.99.1）（numbers.latest_quarter_kpis.items[2]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-27））
  - 註記：未取得
- `f_kpi3_free_cash_flow`（q1_business）｜Free cash flow＝280.4 USD M（營運現金流 322.6、資本支出 42.2；上年同期 253.8，YoY +10%；前九個月 539.2 vs 485.9）｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-27）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（SEC 8-K Ex.99.1）（numbers.latest_quarter_kpis.items[3]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-27））
  - 註記：未取得
- `f_kpi5_guidance_fy2026`（q1_business）｜Guidance FY2026（本次上調）＝Adj. diluted EPS $20.40–$20.60；GAAP EPS $17.30–$17.50；總營收成長 18–19%；organic 10–11% 區間｜期間與口徑：Q3 FY2026（公告於 2026-10-27）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司 Q3 2026 新聞稿（SEC 8-K Ex.99.1）；另載 adjusted tax rate 22.0–22.5%、FCF 約為 adj. 淨利 90%、重組約 $20M；未提供 Q4 單季指引與全年利益率目標（numbers.latest_quarter_kpis.items[5]，as_of Q3 FY2026（公告於 2026-10-27））
  - 註記：媒體稱上調後僅與市場預期相當（TIKR，未驗證，不採為數字）；本站快照 FY1 EPS 共識 20.59（consensus_revision），落在區間內
- `f_kpi6_backlog_archetype`（q1_business）｜Backlog（硬體/設備 archetype，僅定性）＝未揭露金額；管理層稱 orders 強勁、backlog 續增（continued backlog build） 定性｜期間與口徑：Q3 FY2026（公告於 2026-10-27）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿 CEO 引言（numbers.latest_quarter_kpis.items[6]，as_of Q3 FY2026（公告於 2026-10-27））
  - 註記：不適用
- `f_earnings_recency`（q1_business）｜最近一次財報日＝2026-10-27 date｜期間與口徑：2026-10-27／距今 5 個交易日｜kind：realized
  - 來源：—（numbers.earnings_recency，as_of 2026-10-27）
- `f_peer_hubb_gross_margin_pct`（q2_moat）｜HUBB 毛利率＝35.36 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.HUBB.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_hubb_operating_margin_pct`（q2_moat）｜HUBB 營業利益率＝20.21 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.HUBB.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_hubb_fcf_margin_pct`（q2_moat）｜HUBB FCF 利潤率＝14.07 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.HUBB.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_etn_operating_margin_pct`（q2_moat）｜ETN 營業利益率＝17.71 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ETN.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_nvt_operating_margin_pct`（q2_moat）｜NVT 營業利益率＝17.1 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.NVT.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_ayi_operating_margin_pct`（q2_moat）｜AYI 營業利益率＝15.89 %｜期間與口徑：TTM ending 2026-08-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.AYI.operating_margin_pct，as_of TTM ending 2026-08-31（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_abbn_sw_operating_margin_pct`（q2_moat）｜ABBN.SW 營業利益率＝17.6 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ABBN.SW.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_abbn_sw_gross_margin_pct`（q2_moat）｜ABBN.SW 毛利率＝40.12 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ABBN.SW.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_ayi_gross_margin_pct`（q2_moat）｜AYI 毛利率＝50.64 %｜期間與口徑：TTM ending 2026-08-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.AYI.gross_margin_pct，as_of TTM ending 2026-08-31（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝20.59 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-10-31）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝23.05 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-10-31）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝25.49 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-10-31）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝6920.26 USD m｜期間與口徑：2026-11-03／yfinance revenue_estimate 0y 平均（15 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝7682.7 USD m｜期間與口徑：2026-11-03／yfinance revenue_estimate +1y 平均（15 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi4_stock_based_compensation`（q1_business）｜Stock-based compensation（前九個月累計）＝30.0 USD M（9M 累計；上年同期 27.0）。新聞稿未揭露單季 SBC 及九個月營業利益，故無法精確算占營業利益 %｜期間與口徑：前九個月 FY2026（截至 2026-09-30，公告於 2026-10-27）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（SEC 8-K Ex.99.1）現金流量表（numbers.latest_quarter_kpis.items[4]，as_of 前九個月 FY2026（截至 2026-09-30，公告於 2026-10-27））
  - 註記：不適用
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝4951.6 USD m｜期間與口徑：2026-11-03／yfinance 最新一季：總債務 5306.6、現金 355.0（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝1.322 %｜期間與口徑：2026-11-03／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-11-03）
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝52.84 m shares｜期間與口徑：2026-11-03／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_ev_m`（q5_valuation）｜目前企業價值 EV（市值＋淨負債）＝27647.15 USD m｜期間與口徑：2026-11-03／市值 22695.55 ＋ 淨負債 4951.6｜kind：realized
  - 來源：—（numbers.capital_structure.ev_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝429.56 USD｜期間與口徑：2026-11-02（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-11-02（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝20.86 x｜期間與口徑：2026-10-31／分母＝FY1 EPS 20.59，分子＝快照價 429.55｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-10-31）
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝25.19 x｜期間與口徑：2026-11-02（RTH 收盤，UTC）／4 個年度端點內的分位＝44.4｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-11-02（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝44.4 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝4.19 x｜期間與口徑：2026-11-02（RTH 收盤，UTC）／4 個年度端點內的分位＝82.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝82.0 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-11-02（RTH 收盤，UTC））
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝0.73 %｜期間與口徑：2026-07-30 → 2026-10-31／FY1 共識 EPS 20.44 → 20.59（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-10-31）
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝-16.24 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-11-02（RTH 收盤，UTC））
- `f_rsi14`（q5_valuation）｜RSI(14)＝36.8｜期間與口徑：2026-11-02（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ma_state`（q5_valuation）｜週線均線六態（decision_inputs.ma 必須等於此值）＝🟠｜期間與口徑：2026-11-03／timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）
  - 原文：「price 432.91 / W52 476.49 / W104 438.92 / W250 345.74 / W250 13週斜率 1.19%」
- `f_ma_w52`（q5_valuation）｜52 週均線＝476.49 USD｜期間與口徑：2026-11-03／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）
- `f_ma_w104`（q5_valuation）｜104 週均線＝438.92 USD｜期間與口徑：2026-11-03／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）
- `f_ma_w250`（q5_valuation）｜250 週均線＝345.74 USD｜期間與口徑：2026-11-03／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）

### findings_digest 中方向為負或來源衝突的條目（8 條）
- `competitive_share_entrants#1`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K 風險因子：競爭者行為與價格壓力可能使漲價無法完全抵銷成本；AI 等技術採用可能造成長期競爭劣勢。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-12）｜affects：moat_trend、decision_inputs.bear
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：10-K FY2025 風險因子：Hubbell 使用的鋼、鋁、銅及零組件、成品來自加拿大、中國、墨西哥與歐洲；進口關稅已或可能推高成本，並可能引發他國報復性關稅，影響需求與利潤。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-12）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#1`（reg_tariff_export｜方向 -｜狀態 ok）：10-K FY2025 MD&A：2025 年毛利率擴張中，材料與其他成本通膨（含關稅費用）造成約三個百分點的收縮，被價格與生產力抵銷。
  - 來源：SEC EDGAR 10-K FY2025 Item 7 MD&A（as_of 2026-02-12）｜affects：valuation、decision_inputs.bear
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：Hubbell 10-K FY2025 揭露：部分電子元件（螺線管、印刷電路板、IC 晶片、電源線組）來自數量有限的供應商；公司在多國製造與採購，供應中斷會影響營運結果（搜尋摘要為轉述，未取得逐字原文）
  - 來源：Hubbell 10-K FY2025 (SEC EDGAR)（as_of 2026-02-01）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：Hubbell 2026 年 10-Q 風險因素列出美國、中國、墨西哥間關稅與貿易措施不確定性，並提及 IEEPA 關稅退款時程
  - 來源：Hubbell 10-Q Q3 2026 (SEC)（as_of 2026-10-28）｜affects：thesis.R、decision_inputs.bear
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：MIT Technology Review 報導 NYPA/EPRI 於 2026-08 測試 1MW 固態變壓器，開發商目前主攻資料中心，較高電壓應用仍需工程工作
  - 來源：MIT Technology Review - solid state transformers（as_of 2026-10-27）｜affects：moat_trend、thesis.R
- `major_events#1`（major_events｜方向 -｜狀態 ok）：2026-06-02 為併購融資發行三檔共 19 億美元優先債（5 億 2031、7 億 2033、7 億 2036），另有 9 億美元定期貸款協議
  - 來源：SEC EDGAR 8-K Item 1.01（2026-06-08）（as_of 2026-06-08）｜affects：valuation、decision_inputs.bear
- `ma_merger#1`（ma_merger｜方向 -｜狀態 ok）：9 億美元無擔保定期貸款用於 NSI 收購融資
  - 來源：SEC EDGAR 8-K Item 1.01（2026-05-15）（as_of 2026-05-15）｜affects：valuation、decision_inputs.bear

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 2 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/HUBB_20261103/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":876.0,"bear_5y_price":330.0,"p_bull_pct":25,"p_bear_pct":30,"upside_5y_pct":46.7,"ev5y_pct":40.0,"irr_base_pct":8.0,"asym_ratio":3.7,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":20.59,"pe":20.86,"basis":"FY2026E 調整後稀釋 EPS 共識（Koyfin 2026-10-31）；終端倍數同樣用調整後 EPS，套在 FY2031E"},"eps":{"bull":[23.8,27.0,30.2,33.4,36.5],"base":[23.0,25.2,27.3,29.4,31.5],"bear":[22.2,20.5,19.0,20.5,22.0]},"pe":{"bull":24,"base":20,"bear":15},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":1.322,"net_buyback":0.0},"second_stage":{"bull_cagr_pct":9,"base_cagr_pct":6},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### HUBB_Q2_2026_Earnings_Call_20260728.md
- 2026-07-28｜CEO Gerben Bakker｜guidance：CEO 宣布上調 2026 全年財測（原話："We are raising our full year 2026 guidance this morning"）
- 2026-07-28｜CFO Joe Capozzoli｜guidance：全年調整後 EPS 財測由 19.30–19.85 上調至 20.25–20.55（原話："from a range of $19.30 to $19.85 to a range of $20.25"）
- 2026-07-28｜CFO Joe Capozzoli｜guidance：全年調整後營業利益率財測 23.1%–23.4%（原話："we anticipate adjusted operating margins of 23.1% to 23.4%"）
- 2026-07-28｜CFO Joe Capozzoli｜guidance：全年銷售成長財測由 +8–11% 上調至 +16–18%（含 NSI 5 點）（原話："plus 8% to 11% to plus 16% to 18%"）
- 2026-07-28｜CFO Joe Capozzoli｜guidance：Utility Solutions 有機成長財測上調至 +7–9%（原話："Utility Solutions organic growth outlook to plus 7% to 9%"）
- 2026-07-28｜CFO Joe Capozzoli｜guidance：Electrical Solutions 有機成長財測上調至 +12–14%（原話："growth outlook to plus 12% to 14%, driven by our increased"）
- 2026-07-28｜CFO Joe Capozzoli｜guidance：全年資料中心成長預期約 50%（原話："approximately 50% for the full year"）
- 2026-07-28｜CFO Joe Capozzoli｜guidance：財測含 $20M 價格成本淨效益，主要來自 IEEPA 退款（原話："net benefit of $20 million"）
- 2026-07-28｜CFO Joe Capozzoli｜guidance：全年淨利息費用 $1.7 億，來自 NSI 借款（原話："increased net interest expense of $170 million"）
- 2026-07-28｜CFO Joe Capozzoli｜guidance：Q3 調整後稅率預期較高約 24%（原話："rate of approximately 24% in the third quarter"）
- 2026-07-28｜CFO Joe Capozzoli｜guidance：FCF 轉換率未來幾年約維持 90%（原話："pacing around 90% for the next couple of years"）
- 2026-07-28｜CFO Joe Capozzoli｜guidance：Grid Infrastructure 全年營收約雙位數成長，Q4 基期較高（原話："Grid Infrastructure revenue pacing around double digits"）
- 2026-07-28｜CFO Joe Capozzoli｜guidance：Utility 下半年有機成長預期較上半年小幅改善（原話："where we expect organic growth to improve"）
- 2026-07-28｜CFO Joe Capozzoli｜margin：Q2 Electrical 調整後營業利益率 21.2%，年減 130bps（原話："operating margins of 21.2% were down 130 basis points"）
- 2026-07-28｜CFO Joe Capozzoli｜margin：Q2 Electrical 利潤率受約 60bps 較高重組投資影響（原話："60 basis points of higher restructuring investment"）
- 2026-07-28｜CFO Joe Capozzoli｜margin：利潤率橋：淨關稅 30bps、NSI 40bps（原話："30 bps from net tariff, the 40 bps on NSI squares up"）
- 2026-07-28｜CFO Joe Capozzoli｜margin：下半年利潤率擴張預期偏 Q3 較集中（關稅退款）（原話："it is going to be a little more front-loaded"）
- 2026-07-28｜CFO Joe Capozzoli｜margin：關稅效益約一半一半分攤 Electrical 與 Utility（原話："we would split that roughly half and half between electrical"）
- 2026-07-28｜CFO Joe Capozzoli｜margin：IEEPA 退款全數預期落在 Q3（原話："the refund we're anticipating in the guide is all in the"）
- 2026-07-28｜CFO Joe Capozzoli｜margin：Q2 價格/生產力與成本通膨（原話："productivity actions are keeping pace"）
- 2026-07-28｜CFO Joe Capozzoli｜margin：重組：下半年仍偏重（原話："pretty heavily loaded with restructuring-related"）
- 2026-07-28｜CFO Joe Capozzoli｜margin：全年重組約 $2,000 萬，上半年已花過半（原話："million of restructuring related in the full year"）
- 2026-07-28｜CFO Joe Capozzoli｜margin：價格：4 月調價後 7 月再度追加，全年約 3–4 點（原話："3 to 4 points for the full year"）
- 2026-07-28｜CFO Joe Capozzoli｜margin：管理層稱關稅變動影響小、環境仍通膨（原話："nothing of any substance one way or another"）
- 2026-07-28｜CEO Gerben Bakker｜risk：管理層稱環境仍屬高通膨（原話："it's still a very inflationary environment"）
- 2026-07-28｜CEO Gerben Bakker｜risk：Transmission/substation Q2 偏低歸因專案時點（原話："there's really nothing to read into this beyond"）
- 2026-07-28｜CFO Joe Capozzoli｜risk：非住宅市場：不確定是否持續加速（原話："We're a little cautious to say that that's going to"）
- 2026-07-28｜CFO Joe Capozzoli｜commitment：Electrical 下半年（Q3、Q4）利潤率回到擴張（原話："we do see electrical margin returning to expansion"）
- 2026-07-28｜CFO Joe Capozzoli｜commitment：未來 24–30 個月降槓桿還債（原話："pay down significant portions of debt and deleverage"）
- 2026-07-28｜CFO Joe Capozzoli｜commitment：資本配置：股利成長與小額回購（原話："dividend growth and modest share repurchases"）
- 2026-07-28｜CFO Joe Capozzoli｜commitment：NSI 預期 2026 EPS 增益約 $0.20（原話："adjusted earnings accretion of approximately $0.20 in 2026"）
- 2026-07-28｜CFO Joe Capozzoli｜commitment：NSI 銷售協同 2–3%（原話："2% to 3% sales synergies from increased channel"）
- 2026-07-28｜CFO Joe Capozzoli｜commitment：NSI 成本協同 3–5%（原話："approximately 3% to 5% cost synergies from leveraging"）
- 2026-07-28｜CEO Gerben Bakker｜commitment：預告投資人日時間地點（原話："Centralia, Missouri, on March 4, 2027"）
- 2026-07-28｜CFO Joe Capozzoli｜capital_allocation：NSI 收購後預估槓桿約 2.9x（原話："leverage moves to approximately 2.9x net debt to EBITDA"）
- 2026-07-28｜CFO Joe Capozzoli｜capital_allocation：2026 CapEx 預估 $175–190M（原話："roughly $175 million to $190 million of CapEx"）
- 2026-07-28｜CFO Joe Capozzoli｜capital_allocation：CapEx 占營收提高至 2.5–3%（原話："we're now pacing at 2.5% to 3% of sales"）
- 2026-07-28｜CFO Joe Capozzoli｜capital_allocation：每季新增約 $25M 產能（原話："bringing on roughly $25 million of new capacity-ish"）
- 2026-07-28｜CFO Joe Capozzoli｜customer：Utility 上半年 book-to-bill 約 1.2x（原話："first half book-to-bill ratio of approximately 1.2x"）
- 2026-07-28｜CEO Gerben Bakker｜customer：訂單開始排入 2027（輸配電）（原話："We are seeing orders starting to be booked into 2027"）
- 2026-07-28｜CFO Joe Capozzoli｜customer：Q2 資料中心銷售約 +65%（原話："Data center sales were up approximately 65%"）
- 2026-07-28｜CEO Gerben Bakker｜customer：配電成長部分反映去庫存後低基期（原話："the comps are still somewhat easy to lap"）
- 2026-07-28｜CEO Gerben Bakker｜customer：配電長期預期為中個位數以上市場（原話："for this to be a mid-single-digit plus market"）
- 2026-07-28｜CEO Gerben Bakker｜customer：Aclara 於 muni/co-op 專案流改善（原話："particularly in the muni and co-op space"）
- 2026-07-28｜CFO Joe Capozzoli｜customer：資料中心 content 增加稱「more of the same」（原話："I would call it more of the same"）
- 2026-07-28｜CEO Gerben Bakker｜product：高壓：首個 765kV 訂單 2027 開始出貨（原話："will start shipping in '27"）
- 2026-07-28｜CEO Gerben Bakker｜product：高壓傳輸機會約 $15 億/10 年（原話："about $1.5 billion opportunity over the next 10 years"）
- 2026-07-28｜CEO Gerben Bakker｜product：該機會約帶來 1 點額外成長（原話："it's about 1 point of additional growth"）
- 2026-07-28｜CEO Gerben Bakker｜product：新 Pin & Sleeve 產品面向 800V 基礎設施（原話："our new Pin & Sleeve devices"）
- 2026-07-28｜CFO Joe Capozzoli｜product：Grid Automation 回到年增（原話："we were pleased to return to year-over-year growth"）
- 2026-07-28｜CEO Gerben Bakker｜competition：報價量約兩年前兩倍（原話："about doubled in the last couple of years"）
- 2026-07-28｜CEO Gerben Bakker｜competition：大型專案勝率與過往相近（原話："similar to what we've seen traditionally"）
- 2026-07-28｜CEO Gerben Bakker｜competition：管理層稱在輸配電市場為領導地位（原話："leading position with the installed base, with spec position"）
- 2026-07-28｜CEO Gerben Bakker｜competition：模組化/捆綁趨勢（原話："absolutely a trend going on where you're bundling more"）

### 問答異常語氣（迴避／改口／保留）
- HUBB_Q2_2026_Earnings_Call_20260728.md｜問：Nigel Coe：扣除 Q3 關稅退款後 Electrical 利潤率是否仍擴張｜答法：IR 回覆「hard to reconcile right now」並請會後再談，未給答案
- HUBB_Q2_2026_Earnings_Call_20260728.md｜問：Alexander Virgo：1.2x book-to-bill 約 $2.4B 中多少會在下半年交貨｜答法：CEO 稱「hard to exactly do all the math」，只給定性說法（短週期、部分排入 2027），未給拆分數字

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 3 | 2 |
| customer_second_source | found | 2 | 2 |
| customer_concentration_credit | found | 2 | 1 |
| supply_demand_durability | found | 6 | 4 |
| regulatory_antitrust | found | 3 | 2 |
| reg_tariff_export | found | 5 | 2 |
| geo_supply_chain | found | 2 | 2 |
| end_markets | found | 4 | 3 |
| substitute_technology | found | 1 | 2 |
| channel_business_model_shift | found | 2 | 2 |
| capital_markets_pricing | found | 6 | 4 |
| major_events | found | 4 | 4 |

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260518","verdict":"A（核心候選進場，Fwd PE 22x 5Y 分位 0% + post-earnings -13% drop 創 5 年難得 entry，是 PWR 同 thesis 便宜替代品）","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"Utility Solutions（特別是 Grid Infrastructure）持續 mid-to-high single-digit 組織成長","columns":{"2Y 驗證點":"Q2-Q4 26：Grid Infrastructure YoY ≥ 10%","5Y 驗證點":"2027-30：Utility Solutions 段營收從 FY25 $3.7B 至 $5.5-6.0B（mgmt 7-9% 組織 CAGR + bolt-on）","10Y 驗證點":"2030-34：765kV ultra-HV 顯著貢獻（mgmt $1.5B 10Y opportunity 兌現 50%+）","數字門檻":"Grid Infrastructure YoY ≥ 8%（2Y）","來源":"Q1 26 法說 4/30/26 + StockStory 整理","漂移觸發":"連 2 季 YoY &lt; 5% → 削弱；連 3 季 &lt; 2% → 反轉"}},{"id":"H2","text":"Adj OPM 維持並擴張至 FY26 22.7%+ → FY28-30 23-24%","columns":{"2Y 驗證點":"FY26 Adj OPM ≥ 22.7%（mgmt 大約 +20bps 中位）","5Y 驗證點":"FY28 Adj OPM ≥ 23%；FY30 Adj OPM 23.5-24%","10Y 驗證點":"長期 24% 區間穩定","數字門檻":"Adj OPM 連 4 季 ≥ 22.5%（2Y）","來源":"FY25 法說 + Q1 26 法說","漂移觸發":"連 4 季 TTM Adj OPM &lt; 21.5% → 削弱；連 6 季 &lt; 20.5% → 反轉"}},{"id":"H3","text":"Data center 段（Electrical Solutions 內）持續 20%+ YoY 成長","columns":{"2Y 驗證點":"FY26 data center growth 25%+（mgmt 已上修）；連 4 季 ≥ 20%","5Y 驗證點":"FY28-30：data center 段年化 15-20% 成長","10Y 驗證點":"長期 data center segment 占 Electrical Solutions 50%+","數字門檻":"Data center QoQ growth ≥ 5% 連 4 季","來源":"Q1 26 mgmt 法說、Hubbell investor presentation 2026","漂移觸發":"連 2 季 data center YoY &lt; 15% → 削弱"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"大型 utility 客戶 capex 推遲 1-2 季","columns":{"對應假設":"H1","時間尺度":"⚡ 短期（1-2 季可觸發）","監測指標":"季度 Grid Infrastructure 揭露 + utility capex commentary","警戒閾值":"Grid Infrastructure YoY 連 2 季 &lt; 5%"}},{"id":"R2","text":"Systems Control 整合 margin 拖累 — Aclara 2018-20 重演 dilutive period","columns":{"對應假設":"H2","時間尺度":"🔥 中期（4-6 季）","監測指標":"Utility Solutions 段 Adj OPM TTM trend / Systems Control segment 貢獻揭露","警戒閾值":"Utility Solutions Adj OPM 連 4 季 &lt; 20%"}},{"id":"R3","text":"Data center 段 cycle peak / hyperscaler capex 結構性 plateau","columns":{"對應假設":"H3","時間尺度":"🔥 中期（4-6 季）","監測指標":"每季 data center growth 揭露 / hyperscaler combined capex consensus","警戒閾值":"Data center YoY 連 2 季 &lt; 20%"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"A","val":"🟡","ma":"✅","trap":"🟢","moat_trend":null,"runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":479.97,"archetype":null,"cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"HUBB","date":"2026-11-03","schema":"v15.0","contract":"v19","company_name":"Hubbell Incorporated"},"oneliner":"Hubbell：被公用事業與資料中心指定規格的電網元件商，EPS 財測再上調、Utility 在手訂單年初至今約增三成，但產能執行與營益率財測小降；前瞻 20.9 倍合理不便宜，等 392 美元（FY2027E 共識 17 倍）再進場。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/HUBB_20261103/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/HUBB_20261103/scenario.json","answers":{"q1_business":{"verdict":"賺公用事業輸配電與資料中心／工業配電的錢：Utility 段約占 Q3 銷售 55%、調整後營業利益 56%，錢卡在「被公用事業工程師與電氣承包商指定規格的短週期元件」這一節點。","reasoning":"收錢方式：連接器、套管、避雷器、開關、配線器材、Pin & Sleeve 等多 SKU 元件，經電氣經銷商或直售公用事業，短週期出貨。Q3 FY2026 銷售 18.73 億美元（年增 24.6%，有機 11.3%、併購約 13 點），調整後營益率 25.5%（年增 160bps），GAAP 營益率 21.8%（年減 20bps，差距主要是併購無形資產攤銷）。分部：Utility 10.28 億美元（有機 +5%，營益率 26.0%）、Electrical 8.45 億美元（有機 +22%，NSI 貢獻 29 點，營益率 24.8%）；資料中心 Q3 有機 >80%，2026 年底約占 Electrical 營收 15%。產業時鐘判 II 擴張：Utility 在手訂單年初至今增 5 億美元以上，管理層稱輸配電在多年投資周期早期，變壓器交期仍 2–3 年；尚未見供給大量釋出或價格回落，但重工業偏軟、Eaton 與 Hitachi Energy 擴產 2027 年投產。供需持久度：輸配電段偏結構性持久（老化電網、負載成長、資料中心併網），資料中心段週期性較高，供給可逆性中等。單點依賴：無單一客戶依賴，十大客戶約占 42%（通路以經銷商為主）；供給端部分電子元件供應商有限，Q3 電表代工廠缺料使約 1500 萬美元營收遞延到 Q4，是集中度風險的實例。Q2 法說兩題未正面回答（扣除關稅退款後 Electrical 利益率、book-to-bill 下半年交貨拆分），記為資料缺口。","fact_refs":["f_kpi0_net_sales_gaap","f_kpi1_adjusted_non_gaap_operat","f_kpi2_gaap_operating_income_ma","f_kpi3_free_cash_flow","f_kpi5_guidance_fy2026","f_kpi6_backlog_archetype","f_earnings_recency"],"verdict_values":{"revenue_quality":"公用事業資本支出（經費率基礎回收、受監管）＋電氣經銷商通路；短週期、SKU 廣、無單一客戶依賴；2026 年底在手訂單能見度高於常態","unit_econ_note":"Q3 調整後營益率 25.5%、全年財測 23.0–23.2%；長期增量利潤率框架 25–30%；價格成本生產力美元約中性，漲價主要用來抵銷通膨","archetype":{"primary":"品質複利成長","secondary":null,"confidence":"中","fingerprint":"電網元件指定規格＋短週期多 SKU；GAAP 營益率由 2022 年 14.3% 升到 2025 年 20.7%，價格成本與公用事業資本支出周期使獲利有明顯波動"},"industry":{"clock_phase":"II","sd_verdict_source":"結構性持久（偏）：變壓器與高壓斷路器交期仍至少 2–3 年（Rystad，2026-05，二手摘要）、Utility 在手訂單年初至今約 +30%、GE Vernova 稱需求強勁且持久；供給可逆性中等（Eaton、Hitachi Energy 2027 年擴產投產），資料中心段週期性較高","bargaining":{"up":"鋼、鋁、銅與電子元件；部分電子元件（螺線管、電路板、IC、電源線組）供應商有限，Q3 電表代工缺料即一例；靠每年約 3–4 點漲價轉嫁","down":"公用事業與電氣經銷商，十大客戶約 42%，無單一客戶依賴；指定規格讓轉換成本高，但公用事業支出受費率監管約束","geo":"原料與成品部分來自加拿大、中國、墨西哥與歐洲，關稅推高成本；IEEPA 關稅遭最高法院判違法後，Q3 入帳退款 3000 萬美元，後續退款時點不確定"},"profit_pool_dir":"利潤池往輸配電與資料中心配電移動（兩段 Q3 營益率 24.8%–26.0%），重工業偏軟、非住宅持平","tam_table":{"expanded":false,"reason":"事實表未涵蓋 TAM 與滲透率；HUBB 主力為成熟電網元件，成長來自公用事業資本支出周期與資料中心配電含量提升，份額變化改以分部有機成長代理（見成長段分部表）"}}}},"q2_moat":{"verdict":"護城河方向持平（→）：機制是「指定規格＋安裝基礎＋多 SKU 經銷通路」，執行力在擴大、定價力只是穩定；營業利益率 20.2% 為五家同業最高，但只有單點對照，無法證明差距在擴大。","reasoning":"機制：公用事業與承包商在設計圖上指定品牌料號，換供應商要重新做設計測試（765kV 新品需內部與第三方測試，Q3 法說），換掉的成本遠高於元件占專案成本。方向證據：執行力擴大（資料中心有機 +80% 遠超市場，靠含量提升、新品與擴產；Electrical 營益率年增 400bps；大型專案勝率與過去相近，Q2 法說）；定價力穩定（漲價約 3–4 點只抵銷成本通膨，價格成本生產力美元中性，FY2026 營益率財測由 23.1–23.4% 降到 23.0–23.2%；10-K 自承競爭價格壓力可能使漲價無法完全抵銷成本）。同業 TTM 營業利益率：HUBB 20.2%、ETN 17.7%、ABB 17.6%、NVT 17.1%、AYI 15.9%；同業 ROIC 事實表未涵蓋，差距是否擴大無法驗證，因此合併分不給到 8。評分：執行力 8、定價力 7，等級 B。四檢查點：需求基礎值與決策層級正面，價值鏈分配（經銷商集中、系統捆綁趨勢）與社會容忍度（電價政治壓力）中性。增量報酬：投入資本事實表未涵蓋，有機擴產管理層稱報酬最高，NSI 30 億美元已實現報酬未滿一年；內生成長上界估約 9%。","fact_refs":["f_peer_hubb_gross_margin_pct","f_peer_hubb_operating_margin_pct","f_peer_hubb_fcf_margin_pct","f_peer_etn_operating_margin_pct","f_peer_nvt_operating_margin_pct","f_peer_ayi_operating_margin_pct","f_peer_abbn_sw_operating_margin_pct","f_peer_abbn_sw_gross_margin_pct","f_peer_ayi_gross_margin_pct","f_kpi1_adjusted_non_gaap_operat"],"verdict_values":{"moat":{"mechanism":"指定規格＋安裝基礎＋多 SKU 經銷與直售通路；替換需重新設計測試與上線認證","execution":8,"pricing":7,"grade":"B","trend":"→","trend_evidence":"執行力擴大：資料中心有機 +80% 遠超市場、Electrical 營益率年增 400bps、大型專案勝率與過往相近；定價力穩定：價格成本生產力美元中性，FY2026 營益率財測由 23.1–23.4% 小降到 23.0–23.2%；TTM 營業利益率 HUBB 20.2% 領先 ETN 17.7%、ABB 17.6%、NVT 17.1%、AYI 15.9%（同業期間截至 2026-06／08，不完全一致），只有單點無法判斷差距擴大，合併為穩定","competitor_notes":[{"name":"ETN","strategy_note":"規模更大、從元件做到開關設備與變壓器，南卡變壓器廠 2027 年投產；在資料中心配電是系統級競爭，營業利益率 17.7% 低於 HUBB"},{"name":"NVT","strategy_note":"資料中心機櫃、散熱與電氣連接件與 HUBB Electrical 正面重疊，營業利益率 17.1%"},{"name":"AYI","strategy_note":"照明與建築控制為主，毛利率 50.6% 最高但營業利益率 15.9%，與 HUBB 重疊在非住宅，不是輸配電對手"},{"name":"ABBN.SW","strategy_note":"全球電網與配電設備龍頭，毛利率 40.1%、營業利益率 17.6%，在變電站與高壓設備與 Utility 段競爭，資源遠大於 HUBB"}],"peer_na_reason":"事實表同業對照只有毛利率、營業利益率、FCF 利潤率，未涵蓋同業 ROIC 與投入資本；以營業利益率代理，且同業期間（2026-06／08）與 HUBB（2026-09）不一致","threats":[{"level":"🟡","text":"競爭價格壓力與成本通膨：10-K 稱漲價可能無法完全抵銷成本；2025 年材料與關稅通膨約吃掉 3 個百分點毛利率，靠價格與生產力抵銷；10-K 另提 AI 等技術採用可能造成長期劣勢（未具體化）","p":"30%","evidence_refs":["competitive_share_entrants#1","reg_tariff_export#1"]},{"level":"🟡","text":"固態變壓器：NYPA 與 EPRI 2026-08 測試 1MW 機型，主攻資料中心；它吸收整流與變流功能，主要衝擊傳統變壓器，HUBB 的連接器、套管、避雷器多數仍需要，屬點對點替代","p":"10%","evidence_refs":["substitute_technology#0"]},{"level":"🟡","text":"模組化與捆綁趨勢（Q2 法說 CEO）：大型業者整套出貨可能把元件議價權移到系統商；HUBB 以控制屋與跨品牌組合應對","p":"20%","evidence_refs":[]}],"roic_durability":{"quadrant":"高利益率×周轉率待證：營業利益率 20.2% 為同業最高，但 NSI 收購後商譽墊高投入資本，資產負債表事實表未涵蓋，無法計算當期 ROIC","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者（線路工、承包商）、決策者（公用事業工程師）、付款者（公用事業，經費率基礎回收）三方都成立；電網老化、負載成長、資料中心併網屬「需要」而非「想要」，延後的代價是可靠度與併網排隊；Utility 在手訂單年初至今約 +30%、NEMA 六個月展望 73.9 仍遠高於 50；資料中心段需求急迫但持久性較低"},{"item":"決策層級","level":"🟢","text":"替代性要在料號規格層衡量：公用事業指定料號後，換供應商需重新設計測試與上線認證（765kV 新品例）；代理變數為大型專案勝率與過往相近、漲價 3–4 點後量仍成長（Utility 有機 +5%、變電站零組件 >20%）"},{"item":"價值鏈分配","level":"🟡","text":"元件占專案成本低，有利定價；但十大客戶約 42% 以經銷商為主、系統捆綁趨勢可能把議價權移往系統商；價格成本只維持美元中性，顯示 HUBB 目前沒有從價值鏈多拿"},{"item":"社會容忍度","level":"🟡","text":"公用事業的資本支出最終轉成電價，電價上漲受監管機關與民意審視；HUBB 漲價幅度溫和（每年約 3–4 點），未逼近經濟上限；事實表未涵蓋費率案或電價政治化的具體證據"}],"roiic":"事實表未涵蓋投入資本，無法直接計算；代理：有機擴產每季新增約 2500 萬美元營收產能（2026）→約 5000 萬美元（2027），管理層稱是報酬最高的投資；NSI 30 億美元已實現報酬未滿一年；有機增量報酬約 40%、併購約 10% 為判斷假設","reinvest_rate":"有機約 10%（FCF 約為調整後淨利 90%）；含併購 2026 年約 240%（NSI 30 億美元 ÷ 調整後稅後營業利益約 12.4 億美元），2027–28 去槓桿期併購暫停，五年平均取約 50%","endo_ceiling":9.0,"formula_note":"內生成長＝增量報酬×再投資率：有機 40%×10%≈4pp＋併購 10%×50%≈5pp，合計約 9%；調整後稅後營業利益＝FY2026E 共識營收 69.2 億美元×財測營益率中點 23.1%×(1−22.25%)≈12.4 億美元。兩個增量報酬是判斷假設，結論對假設敏感"}}}},"q3_growth":{"verdict":"五年後成長空間中等（🟡）：輸配電多年周期與 765kV、800V 資料中心新品撐得住中個位數以上有機成長，但核心元件份額已高、第二曲線規模只約 1 點成長，第五年後回到周期驅動。","reasoning":"成長組成：2026 年有機 10–11%（量為主、價格約 3–4 點）、NSI 約 7.5 點、DMC Power 約 4 點（Utility 段）；2027 年管理層稱有機至少中個位數、價格成本中性至正、增量利潤率 25–30%，加上去槓桿利息節省與 NSI 協同（成本 3–5%、銷售 2–3%）。共識三年 EPS 年增 11.8%（FY2025A 調整後約 18.22 美元→FY2028E 25.49 美元；基期由 FY2026 財測年增 12–13% 回推），營收 FY2025 58.4 億→FY2026E 69.2 億（+18.4%）→FY2027E 76.8 億（+11.0%）。內生上界約 9%（見護城河段推導），缺口約 2.8pp，歸因於營益率擴張（Electrical 利益率計畫、增量利潤率高於平均利益率）與去槓桿（淨利息費用增加約 1.7 億美元，兩年內還債），屬可歸因，不依賴倍數重估；Base 情境 EPS 年增 8.9% 落在上界內。成長空間：管理層稱輸配電在多年周期早期，765kV 約 10 年 15 億美元機會（約 1 點成長）、Pin & Sleeve 800V 新品；事實表未涵蓋滲透率，核心元件已是領先供應商，五年後成長回到公用事業資本支出周期，判中等。衰退信號十類亮 1 項：FY2022–25 GAAP EPS 年增 20.6% 遠高於營收 5.7%（差 15pp），來自 2022 年利益率低點回升；前瞻兩年營收增速已高於 EPS，屬歷史性亮燈。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_kpi5_guidance_fy2026","f_kpi6_backlog_archetype","f_kpi0_net_sales_gaap","f_kpi4_stock_based_compensation"],"verdict_values":{"growth":{"driver_mix":"量為主（有機）＋併購（2026 年 NSI 約 7.5 點、DMC 約 4 點於 Utility）＋價格約 3–4 點；回購貢獻小","runway_years":"5–9","runway_post_y5":"🟡","endo_ceiling_basis":"沿用護城河段：有機（再投資率約 10%×增量報酬約 40%）約 4pp＋併購（五年平均再投資率約 50%×增量報酬約 10%）約 5pp，合計約 9%；兩個增量報酬皆為判斷假設，投入資本事實表未涵蓋","segments":[{"item":"Utility Solutions（Q3）","value":"銷售 10.28 億美元，年增 9%（有機 5%、DMC 4 點）；調整後營業利益 2.67 億、營益率 26.0%（+30bps）；FY2026 有機財測 6–7%（Q2 時 7–9%）"},{"item":"Grid Infrastructure／Grid Automation（Q3）","value":"Grid Infrastructure 有機 +8%（變電站零組件 >20%、控制屋季持平）；Grid Automation 有機 −4%（電表代工缺料，約 1500 萬美元移到 Q4，管理層預期 Q4 雙位數成長）"},{"item":"Electrical Solutions（Q3）","value":"銷售 8.45 億美元，年增 51%（有機 22%、NSI 29 點）；調整後營業利益 2.10 億、營益率 24.8%（+400bps）；FY2026 有機財測 17–18%（Q2 時 12–14%）"},{"item":"資料中心","value":"Q3 有機 >80%（Q2 約 65%）；2026 年底約占 Electrical 營收 15%；管理層預期 2027 年在更高基期上仍有吸引人的成長"},{"item":"小型終端市場","value":"天然氣、電信、電表與 AMI 約占組合 20%，管理層預期成長較溫和；Aclara 占 Utility 營收 <10%"}],"decay_signals":[{"signal":"毛利率連 2 季年減","lit":false,"evidence":"季度毛利率事實表未涵蓋；TTM 35.4% 與 FY2025 35.3% 持平"},{"signal":"核心市占近 12 個月縮減","lit":false,"evidence":"無來源顯示份額流失；資料中心有機 +80% 屬份額提升"},{"signal":"主力產品提價後銷量下滑","lit":false,"evidence":"漲價 3–4 點後兩段有機量仍成長"},{"signal":"EPS 年增顯著高於營收（差 >5pp）","lit":true,"evidence":"FY2022–25 GAAP EPS 年增 20.6% vs 營收 5.7%；前瞻 FY2025–27 營收年增約 14.7% 已高於 EPS 12.5%"},{"signal":"FCF／淨利 <0.75 連 2 年","lit":false,"evidence":"2024 年 104%、2025 年 99%"},{"signal":"SBC／營收 >5% 且上升","lit":false,"evidence":"前九個月 SBC 3000 萬美元，年化約占營收 0.6%"},{"signal":"TAM 萎縮或被替代技術壓縮","lit":false,"evidence":"固態變壓器仍在 1MW 測試階段"},{"signal":"產業估值倍數近 3 年系統性下移","lit":false,"evidence":"同業倍數事實表未涵蓋，無法判斷"},{"signal":"維持性資本支出占 FCF >60%","lit":false,"evidence":"2026 年資本支出 1.75–1.90 億美元，2025 年 FCF 8.75 億美元"},{"signal":"停止投資新產能且營收 3 年內下滑","lit":false,"evidence":"擴產加速：每季新增產能由約 2500 萬美元營收提高到約 5000 萬美元"}],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"資本配置中等：現金轉換率高（2025 年 FCF／淨利 99%，2026 年指引約為調整後淨利 90%），但 2026 年以約 28 億美元新債撐起 30 億美元 NSI 收購，報酬尚待驗證，未來兩年現金優先還債。","reasoning":"現金去向：股利（TTM 殖利率 1.32%，持續成長）、併購（NSI 30 億美元，2026-06-09 交割；DMC Power 金額事實表未涵蓋）、資本支出（2026 年 1.75–1.90 億美元，占營收 2.5–3%）、回購（去槓桿期只做小額）。債務：19 億美元優先債（2031 年 4.65%、2033 年 4.90%、2036 年 5.15%）＋9 億美元定期貸款，淨負債 49.5 億美元，收購後淨負債／EBITDA 約 2.9 倍，管理層承諾 24–30 個月內大幅去槓桿。SBC 前九個月 3000 萬美元，年化約占營收 0.6%，稀釋股數因過去回購略降。營運槓桿：Q3 營收年增 24.6%、調整後營業利益年增 33%，未見壓縮；GAAP 營業利益年增約 24%，與營收差約 1pp。計分：併購增量報酬未滿一年無法判定；回購以現價盈餘殖利率約 4.8% 計，需 10 年期殖利率低於 2.8% 才過，判不過（10 年期殖利率事實表未涵蓋）；SBC 稀釋過。","fact_refs":["f_kpi3_free_cash_flow","f_kpi4_stock_based_compensation","f_net_debt_m","f_dividend_yield_ttm","f_shares_diluted_m","f_ev_m"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":true,"passed":null,"input":"NSI 30 億美元 2026-06 交割，已實現報酬未滿一年；管理層預估 2026 年 EPS 增益約 0.20 美元、整合超前；融資成本 4.65–5.15%；投入資本與 WACC 事實表未涵蓋"},{"name":"buyback_yield","applicable":true,"passed":false,"input":"去槓桿期只做小額回購；以前瞻本益比 20.86 倍計盈餘殖利率約 4.8%，需 10 年期殖利率 <2.8% 才過；10 年期殖利率事實表未涵蓋"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"前九個月 SBC 3000 萬美元，年化約占市值 0.18%；Q3 稀釋股數因過去回購略降"}]},"governance":{"capital_returns":[{"item":"股利","value":"TTM 殖利率 1.32%；管理層：股利持續成長"},{"item":"併購","value":"NSI 30 億美元現金（2026-06-09 交割，約市值 13%）；DMC Power 金額事實表未涵蓋"},{"item":"融資","value":"19 億美元優先債（4.65% 2031、4.90% 2033、5.15% 2036）＋9 億美元定期貸款；淨負債 49.5 億美元，淨負債／EBITDA 約 2.9 倍"},{"item":"去槓桿","value":"Q2 法說：24–30 個月內償還大部分債務；Q3 法說重申兩年去槓桿，並稱將帶來 2027 年 EPS 增益"},{"item":"資本支出","value":"2026 年 1.75–1.90 億美元，占營收 2.5–3%，擴產每季新增約 2500 萬美元營收產能"},{"item":"回購","value":"去槓桿期只做小額；Q3 稀釋股數因過去回購略降"}]}}},"q5_valuation":{"verdict":"現價 429.56 美元要求未來五年調整後 EPS 年增約 9%、本益比守在 20 倍左右，才換得約 9% 年報酬（含股息）；EPS 這半我信，但價格只算合理，不夠便宜到值得在 2027 財測前搶進。","reasoning":"前瞻本益比 20.86 倍（FY2026E 20.59 美元）、FY2027E 18.6 倍；PEG 1.76（三年 EPS 年增 11.8%），落在合理區。trailing P/E 25.2 倍在 4 個年度端點中位於 44 分位、EV/S 4.19 倍在 82 分位（NSI 舉債墊高 EV），五年連續分位事實表未涵蓋，前份「五年分位 0%」無法驗證。成長熄火測試（以 FY2028E 25.49 美元為起點，第 4 年成長降到 15%／10%／5%，倍數 22／18／15 倍）→ 645／505／401 美元，相對現價 +50%／+18%／−7%，三項過兩項；Bear 倍數 15 倍取自降到 5% 那一格。賣方目標價：Benzinga 14 位均值 504 美元（325–600）、MarketBeat 554 美元，高於現價 17–29%，與本次「等價」方向相反，但全距 1.85 倍、聚合站數字不一（另一來源約 443 美元），不調高信心。分母：FY2026 調整後 EPS 含 IEEPA 關稅退款淨效益約 2000 萬美元（約每股 0.3 美元、占 1.5%），不構成爭議。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_pe_current","f_pe_percentile","f_ev_s_current","f_ev_s_percentile","f_dividend_yield_ttm","f_consensus_rev_3m_fy1_pct","f_kpi5_guidance_fy2026"],"verdict_values":{"valuation":{"basis":"Fwd P/E（FY2026E 調整後 EPS 共識）＋PEG；EV/S 與 trailing P/E 年度端點分位輔助","tier":"美國電氣與電網設備品質股","peers":{"expanded":false,"reason":"事實表同業對照只有利益率，未涵蓋同業前瞻本益比或 EV/S，無法建倍數對照；終端倍數以自身前瞻倍數與成長熄火測試錨定"},"fwd_pe":20.86,"peg":1.76,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"PEG 1.76 落 1–2 合理區；前瞻 20.9 倍、FY2027E 18.6 倍；Base 五年年報酬約 9%（中段）；五年連續分位資料不足（只有 4 個年度端點：P/E 44 分位、EV/S 82 分位）→ 合理，不便宜也不貴。短期上行＝FY2027E Base EPS 23.0 美元×20 倍＝460 美元（+7.1%）；中期＝FY2029E 27.3 美元×20 倍＝546 美元（+27.1%）","upside_short_pct":7.1,"upside_mid_pct":27.1,"denominator_disputed":false,"denominator_note":"FY2026 調整後 EPS 含 IEEPA 關稅退款淨效益約 2000 萬美元（Q2 法說，稅後約每股 0.3 美元、占約 1.5%）；GAAP 與調整後差距（17.30–17.50 vs 20.40–20.60）主要為併購無形資產攤銷，屬常規調整，不是爭點"}}},"q6_how_wrong":{"verdict":"看錯的最可能方式是周期：把多年輸配電與資料中心順風當成永久，2028 年後公用事業資本支出放緩，EPS 回落、倍數同步收縮；陷阱風險低度（🟡）。","reasoning":"反證三視角見反證紀錄（論點失敗：公用事業周期轉向；股東經濟變差：併購舉債與成本通膨稀釋；價格已反映：EV/S 分位偏高）。衰退信號亮 1 項（歷史 EPS 增速遠高於營收，來自利益率回升），判低度陷阱。最大回撤推估 −30%～−43%：上緣＝EPS 停在 FY2027E 約 23 美元、倍數壓到 13 倍（約 299 美元）；下緣＝Bear 路徑 EPS 低點 FY2029E 19.0 美元×13 倍（約 247 美元）；事實表未涵蓋歷史最大回撤，但 2022 年 GAAP 營益率曾低至 14.3%，顯示獲利波動真實存在。動能：26 週 −16.2%、RSI 36.8，股價低於 52 與 104 週均線但高於 250 週均線，非過熱。","fact_refs":["f_week26_return_pct","f_rsi14","f_ma_state","f_ma_w52","f_ma_w104","f_ma_w250","f_kpi2_gaap_operating_income_ma"],"verdict_values":{"trap":{"verdict":"🟡","label":"低度陷阱：歷史 EPS 增速靠利益率回升，前瞻已與營收同步"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":20.59,"pe":20.86,"basis":"FY2026E 調整後稀釋 EPS 共識（Koyfin 2026-10-31）；終端倍數同樣用調整後 EPS，套在 FY2031E"},"eps":{"bull":[23.8,27.0,30.2,33.4,36.5],"base":[23.0,25.2,27.3,29.4,31.5],"bear":[22.2,20.5,19.0,20.5,22.0]},"pe":{"bull":24,"base":20,"bear":15},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":1.32,"net_buyback":0.0},"second_stage":{"bull_cagr_pct":9,"base_cagr_pct":6},"max_dd":{"lo":-43,"hi":-30,"basis":"上緣 −30%：EPS 停在 FY2027E 約 23 美元、倍數壓到 13 倍（約 299 美元）；下緣 −43%：Bear 路徑 EPS 低點 FY2029E 19.0 美元×13 倍（約 247 美元）。事實表未涵蓋歷史最大回撤，範圍由情境推估","trigger_time":null},"basis":{"bull":"輸配電與資料中心周期延續到 2030 年後，Utility 有機 8–9%、Electrical 利益率計畫持續、去槓桿後再做增值併購，EPS 年增約 12%；終端 24 倍，同業現值倍數事實表未涵蓋，以 HUBB trailing 25.2 倍為上方參照","base":"2027–28 接近共識（23.0／25.2 美元），之後有機中個位數＋營益率每年擴張約 20bps＋利息節省，EPS 年增 7–8%；終端 20 倍約等於現價前瞻倍數，報酬幾乎全來自 EPS 複利","bear":"2028 年起公用事業資本支出放緩、資料中心消化、價格成本轉負：EPS 2029 年回落到 19 美元後緩升到 22 美元；終端 15 倍取自成長熄火降到 5% 那一格；機率 30%：輸配電訂單證據偏結構性，但共識成長高於內生上界，且 2022 年利益率曾跌到 14% 顯示周期真實存在"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"Utility 有機財測年內由 7–9% 降到 6–7%，控制屋擴產不順、電表代工缺料；2022 年 GAAP 營益率曾低至 14.3%、EPS 9.43 美元","assumption":"在手訂單（年初至今 +5 億美元）能在 2027–28 轉成營收，公用事業不因電價壓力延後資本支出","consequence":"2028 年起 Utility 有機轉負、EPS 回落到約 19 美元、倍數 15 倍，五年後股價約 285–330 美元（−23%～−34%）","ruling":"部分採納：Q3 下修主因在供給端，訂單仍創高；但周期性真實存在，Bear 機率定 30%，與唯一致命點是同一件事","watch":"Utility 有機成長、book-to-bill、2027-01 財測","evidence_refs":["geo_supply_chain#0","end_markets#1"],"fact_refs":["f_kpi0_net_sales_gaap"]},{"view":"論點成功但股東經濟變差","evidence":"NSI 30 億美元（約市值 13%）以 19 億美元優先債（4.65–5.15%）＋9 億美元定期貸款支付，淨利息費用增加約 1.7 億美元；GAAP 營益率 Q3 年減 20bps；2025 年材料與關稅通膨吃掉約 3 個百分點毛利率；原料與成品來自加中墨歐，有關稅與報復關稅風險","assumption":"NSI 增量報酬高於融資成本，價格可持續轉嫁通膨與關稅","consequence":"營收高成長但利息、攤銷與成本通膨稀釋每股盈餘，FCF 兩年優先還債，股東回報延後","ruling":"部分採納：NSI 整合超前且提升營益率（Q3 法說），但已實現報酬未滿一年；資本配置只評中等，不給溢價倍數，Base 終端 20 倍","watch":"淨負債／EBITDA、NSI 營益率、價格成本生產力","evidence_refs":["major_events#1","ma_merger#1","reg_tariff_export#0","reg_tariff_export#1","geo_supply_chain#1"],"fact_refs":["f_net_debt_m","f_kpi2_gaap_operating_income_ma"]},{"view":"價格已反映太多","evidence":"EV/S 4.19 倍在 4 個年度端點中位於 82 分位；Q3 財測上調僅與共識相當，財報當日跌約 6%","assumption":"市場會繼續給 20 倍左右的前瞻本益比","consequence":"若市場把 HUBB 當周期高點的電氣設備股，倍數回到 15–17 倍，即使 EPS 達共識，三年報酬接近零","ruling":"部分採納：前瞻 20.9 倍、PEG 1.76 只是合理，因此等 17 倍；但 trailing P/E 44 分位不支持嚴重高估，且股價已較 52 週均線低約 10%","watch":"前瞻本益比、共識修正","evidence_refs":["capital_markets_pricing#0"],"fact_refs":["f_ev_s_percentile","f_pe_percentile","f_fwd_pe_latest","f_ma_w52"]},{"view":"論點失敗","evidence":"固態變壓器 2026-08 已做 1MW 測試、主攻資料中心；10-K 稱 AI 等技術採用可能造成長期競爭劣勢；系統捆綁趨勢","assumption":"HUBB 的元件在新架構中仍被需要","consequence":"若資料中心配電改走固態與直流整合，Pin & Sleeve 與部分配線元件含量下降，資料中心成長熄火","ruling":"暫時反駁：固態變壓器較高電壓應用仍需工程工作，HUBB 已推 800V 直流用 Pin & Sleeve；屬 10 年尺度風險","watch":"資料中心含量、主要客戶固態變壓器試點是否轉量產","evidence_refs":["substitute_technology#0","competitive_share_entrants#1"],"fact_refs":[]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟠","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟠","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 479.97 → 本次 429.56（-10.5%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=479.97","side_b":"本次 price_at_dd=429.56","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 479.97 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 479.97 美元：五年期望值 前份未列，基準年化 前份未列，前份未列不對稱比","side_b":"本次情境、股價仍用 479.97 美元：Bull 價 876、Bear 價 330，五年期望值 +25.3%，基準年化 5.6%，不對稱比 2.2","ruling":"先換情境、股價不動：五年期望值與基準年化前份未列，無法比較。前份未列不對稱比，本次為 2.2。Bull、Bear 價位與股價無關，只受情境影響。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 479.97 美元：五年期望值 +25.3%，基準年化 5.6%，不對稱比 2.2","side_b":"本次情境、股價 429.56 美元：五年期望值 +40.0%，基準年化 8.0%，不對稱比 3.74","ruling":"再換股價、情境不動：起點價下跌 10.5%，五年期望值多 14.7 個百分點，基準年化多 2.4 個百分點，不對稱比由 2.2 升到 3.74。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"產業態勢三軸（一致判斷）","cause":null,"prior_field":null,"side_a":"A 競爭：大型專案勝率與過往相近（Q2 法說），HUBB 營業利益率為同業最高，未見惡化；C 其他：IEEPA 關稅退款入帳但美中墨關稅仍在、NSI 重大併購、系統捆綁與固態變壓器","side_b":"B 結構與持久度：Utility 在手訂單年初至今約 +30%、變壓器與高壓斷路器交期仍 2–3 年、GE Vernova 稱需求強勁且持久","ruling":"結構性轉好中（B 軸），C 軸關稅與併購屬成本與資本結構的拉鋸，不改方向","evidence_level":"一手法說＋二手產業摘要","settle_metric":"Utility book-to-bill 與在手訂單","if_then":["若 2027 上半年 Utility book-to-bill 仍 >1.0：維持結構性轉好判斷","若 book-to-bill <1.0 連兩季：改判雙向拉鋸並把 Bear 機率調到 40%"],"evidence_refs":["supply_demand_durability#0","supply_demand_durability#5","end_markets#2","reg_tariff_export#0"]},{"axis":"Utility 需求與財測下修","cause":null,"prior_field":null,"side_a":"Q3（2026-10-27，CFO Capozzoli）Utility 有機財測降到 6–7%，Q2（2026-07-28，CFO）為 7–9%；Grid Automation −4%、控制屋季持平","side_b":"同場 CEO Bakker：在手訂單年初至今增 5 億美元以上（約 +30%），變電站零組件 >20%，下修主因是電表代工缺料與控制屋擴產爬坡","ruling":"可調和（程度差異）：需求未轉弱，問題在供給與產能執行；管理層「一次性、暫時」的歸因不採信也不否定，標未證並設期限；下修距今不到一季、FY2027 共識 23.05 美元未變，可能尚未完全反映，加碼凍結到 2027-01 財測","evidence_level":"一手逐字稿","settle_metric":"2026 Q4 Grid Automation 成長、2027 上半年 Utility 有機成長","if_then":["若 2026 Q4 Grid Automation 未達管理層所說的雙位數成長：缺料一次性歸因證偽，Bear 機率上調 5 點","若 2027 上半年 Utility 有機連 2 季 <3%：減碼一半","反向：若 2027 上半年 Utility 有機 ≥7%：Base 機率維持、解除加碼凍結"],"evidence_refs":["geo_supply_chain#0","end_markets#1"]},{"axis":"營益率財測與 Q2 承諾","cause":null,"prior_field":null,"side_a":"Q2（2026-07-28，CFO）：全年調整後營益率 23.1–23.4%，下半年 Electrical 利益率回到擴張","side_b":"Q3（2026-10-27，CFO）：全年 23.0–23.2%，Q4 Utility 營益率年減（價格成本中性、成長投資、約 500 萬美元 IEEPA 客戶補償遞延）；Electrical Q3 +400bps 有兌現","ruling":"可調和：EPS 財測仍由 20.25–20.55 上調到 20.40–20.60，營益率小降來自通膨與成長投資；記為營益率假設削弱的早期警示，不改方向","evidence_level":"一手逐字稿","settle_metric":"FY2027 調整後營益率財測（2027-01）","if_then":["若 FY2027 財測營益率 ≥23.3%：營益率假設維持","若 <23.0%：營益率假設削弱，Base EPS 下修 3% 並停止加碼"],"evidence_refs":["reg_tariff_export#1","competitive_share_entrants#1"]},{"axis":"現在就買 vs 等 392 美元（裁決）","cause":null,"prior_field":null,"side_a":"現在就買的最強論證：EPS 財測年內兩度上調，FY2027E 只要 18.6 倍；在手訂單創高、資料中心 +80%、2027 擴產翻倍到每季約 5000 萬美元營收、去槓桿帶來 EPS 增益；賣方目標價均值 504–554 美元；等 17 倍可能等不到","side_b":"等價的理由：Base 五年年報酬約 9% 只在中段；股價在 52 與 104 週均線之下；Utility 執行不順、Q4 營益率年減；距 17 倍只差約 9%，進場價改善可把 Base 年報酬推到約 11%","ruling":"不可調和（方向相反），選等價：依據是 Base 報酬落在中段、Bear 機率 30%，價格改善 9% 對報酬的影響大於錯過的成本","evidence_level":"情境推估＋一手財測","settle_metric":"股價 vs 392 美元；2027-01 財測","if_then":["若股價 ≤392 美元且 Utility 有機未連 2 季 <3%：重跑分析後建首倉（正常部位一半）","若股價續跌但基本面無損（訂單仍增）：分批反買，不停損","反向：若 2027-01 財測 Utility 有機 ≥6%、價格成本為正而股價 ≤450 美元：直接建首倉，不再等 392 美元","若股價先漲到 480 美元以上但財測未出：不追"],"evidence_refs":["capital_markets_pricing#4"]},{"axis":"前份進場評級與估值依據","cause":"方法變動","prior_field":["signal"],"side_a":"前份（2026-05-18，股價 479.97 美元）：評級 A，依據為前瞻本益比約 22 倍、五年分位 0%、財報後急跌","side_b":"本次評級 B：事實表只有 4 個年度端點（trailing P/E 44 分位、EV/S 82 分位）與 2026-05 起的前瞻短窗，五年分位 0% 無法驗證；改用五年情境樹後，Base 年報酬約 9%（以前份價位算約 7%），屬中段","ruling":"採本次：股價雖跌 10.5%、三項假設皆未破，但前份的便宜論據缺證據；評級降一級是方法所致，不是基本面轉壞","evidence_level":"事實表估值歷史","settle_metric":"前瞻本益比 vs FY2027E 17 倍","if_then":["若股價 ≤392 美元：評級回到可進場並重跑分析"],"evidence_refs":[]},{"axis":"估值結論","cause":"價格變動","prior_field":["val"],"side_a":"前份估值結論：合理（🟡），股價 479.97 美元，前份所述前瞻約 22 倍","side_b":"本次：合理（🟡），股價 429.56 美元（−10.5%），前瞻本益比 20.9 倍、PEG 1.76","ruling":"價格下跌改善報酬但未跨出合理區，估值結論不變","evidence_level":"事實表","settle_metric":"前瞻本益比","if_then":["若 FY2027E 本益比 ≤17 倍：估值改判偏便宜"],"evidence_refs":[]},{"axis":"陷阱風險","cause":"方法變動","prior_field":["trap"],"side_a":"前份：陷阱風險低（🟢）","side_b":"本次：低度（🟡），十類衰退信號逐項檢查亮 1 項（FY2022–25 EPS 年增 20.6% vs 營收 5.7%）","ruling":"差異來自逐項檢查而非新利空；該信號源自 2022 年利益率低點回升，前瞻已收斂","evidence_level":"事實表財務歷史","settle_metric":"前瞻兩年營收與 EPS 增速差","if_then":["若 FY2027 EPS 增速再高於營收增速 5pp 以上：維持低度並檢查利益率持續性"],"evidence_refs":[]},{"axis":"前份未記錄欄位","cause":"方法變動","prior_field":["moat_trend","runway_post_y5","archetype","cycle_position","p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份這些欄位皆為空（未記錄）","side_b":"本次：護城河方向持平（→）、五年後成長空間中等（🟡）、類型品質複利成長、中循環、機率 25／45／30、最大回撤 −30%～−43%","ruling":"新增欄位是格式變動，不是判斷翻轉","evidence_level":"方法","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"行動門檻：清倉、減碼與重新進場條件","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"前份未設（kill_metrics 與 rearm_trigger 皆為空）","side_b":"清倉：Utility 有機成長轉負且半年 book-to-bill <1.0；減碼：Grid Infrastructure 有機連 2 季 <5%，或價格成本連 2 季為負且營益率年減 ≥100bps；重新進場：股價 ≤392 美元（FY2027E 共識 17 倍）","ruling":"前份只有風險描述沒有行動門檻，本次補上；門檻取自本次情境與分部揭露","evidence_level":"方法","settle_metric":null,"if_then":["若任一清倉條件成立：清倉並重跑分析","若任一減碼條件成立：減碼一半"],"evidence_refs":[]},{"axis":"Single Thing 唯一致命點","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設唯一致命點（null）","side_b":"公用事業輸配電訂單周期轉向：Utility 段有機成長轉負且半年 book-to-bill 低於 1.0","ruling":"新設；Utility 約占銷售 55%、調整後營業利益 56%，是 EPS 最大單一敏感項，與反證「論點失敗」視角一致","evidence_level":"一手分部揭露","settle_metric":"Utility 有機成長、book-to-bill","if_then":["若發生：清倉並重跑分析"],"evidence_refs":[]},{"axis":"風險減碼門檻調整","cause":"新證據","prior_field":["thesis.R"],"side_a":"前份：R1 Grid Infrastructure 年增連 2 季 <5%；R2 Utility 調整後營益率連 4 季 <20%；R3 資料中心年增連 2 季 <20%（三項至今皆未觸發：Q3 Grid Infrastructure 有機 +8%、Utility 營益率 26.0%、資料中心 +80%）","side_b":"本次：R1 門檻不變但改看有機（剔除 DMC 併購）；R2 改為價格成本連 2 季為負且營益率年減 ≥100bps 即減碼；R3 改為資料中心年增連 2 季 <15% 停止加碼","ruling":"R2：Utility 營益率 26.0% 距 20% 太遠形同不會觸發，Q3 法說顯示通膨與價格成本才是利益率主風險；R3：資料中心 Q3 有機 +80%、基期大增，20% 會因比較基期機械觸發，改用前份資料中心假設自己的削弱線 15%","evidence_level":"一手逐字稿","settle_metric":"季報分部揭露","if_then":["若 R2 新門檻成立：減碼一半","若 R3 新門檻成立：停止加碼"],"evidence_refs":["reg_tariff_export#1"]}],"triggers":[{"n":1,"text":"股價回到 FY2027E 共識 EPS 的 17 倍","type":"估值rearm","maps_to":"H1","metric":"收盤價","threshold":"≤392 美元","action":"重跑分析，通過即建首倉（正常部位一半）","source_freq":"每日收盤","date":null,"evidence_refs":[]},{"n":2,"text":"2027 年全年財測驗證輸配電周期","type":"假設驗證","maps_to":"H1","metric":"FY2027 Utility 有機成長財測","threshold":"≥6%；<4% 視為警訊","action":"≥6% 且價格成本為正：股價 ≤450 美元可直接建首倉；<4%：停止加碼並上調唯一致命點機率","source_freq":"年度財測","date":"2027-01","evidence_refs":[]},{"n":3,"text":"營益率擴張驗證","type":"假設驗證","maps_to":"H2","metric":"FY2027 調整後營益率財測","threshold":"≥23.3%","action":"<23.0%：營益率假設削弱，Base EPS 下修 3%","source_freq":"年度財測","date":"2027-01","evidence_refs":["reg_tariff_export#1"]},{"n":4,"text":"公用事業資本支出延後或自身產能跟不上","type":"風險","maps_to":"R1","metric":"Grid Infrastructure 有機成長","threshold":"連 2 季 <5%","action":"減碼一半","source_freq":"季報","date":null,"evidence_refs":[]},{"n":5,"text":"成本通膨快於漲價","type":"風險","maps_to":"R2","metric":"價格成本生產力美元淨額；調整後營益率年變化","threshold":"連 2 季為負且營益率年減 ≥100bps","action":"減碼一半","source_freq":"季報法說","date":null,"evidence_refs":["reg_tariff_export#1","competitive_share_entrants#1"]},{"n":6,"text":"資料中心周期見頂","type":"風險","maps_to":"R3","metric":"資料中心銷售年增","threshold":"連 2 季 <15%","action":"停止加碼；連 3 季 <10% 減碼三分之一","source_freq":"季報法說","date":null,"evidence_refs":[]},{"n":7,"text":"去槓桿延後或 NSI 整合失速","type":"風險","maps_to":"R4","metric":"淨負債／EBITDA；NSI 營益率","threshold":"2027 年底 >2.5 倍，或 NSI 營益率低於 Electrical 段平均","action":"停止加碼；兩者同時成立減碼一半","source_freq":"年報、季報法說","date":"2027-12","evidence_refs":["major_events#1","ma_merger#1"]},{"n":8,"text":"關稅或零件短缺吸收失敗","type":"風險","maps_to":"R5","metric":"零件短缺遞延營收；管理層揭露的關稅淨成本","threshold":"單季遞延 ≥3000 萬美元，或關稅淨成本使營益率年減 ≥50bps","action":"停止加碼；連 2 季成立減碼三分之一","source_freq":"季報法說","date":null,"evidence_refs":["geo_supply_chain#0","geo_supply_chain#1","reg_tariff_export#0"]},{"n":9,"text":"公用事業輸配電訂單周期轉向","type":"Single Thing","maps_to":"Single Thing","metric":"Utility 有機成長；半年 book-to-bill","threshold":"有機轉負且 book-to-bill <1.0","action":"清倉並重跑分析","source_freq":"季報法說","date":null,"evidence_refs":[]},{"n":10,"text":"投資人日更新長期目標（Centralia, Missouri）","type":"複審日期","maps_to":"H1","metric":"長期有機成長與營益率目標","threshold":"有機目標維持或上調到中個位數以上","action":"重跑分析","source_freq":"一次性","date":"2027-03-04","evidence_refs":[]},{"n":11,"text":"替代技術或系統捆綁繞過元件","type":"風險","maps_to":"R6","metric":"主要客戶固態變壓器量產採用；大型專案勝率","threshold":"管理層揭露勝率低於過往，或主要客戶試點轉量產","action":"停止加碼並重評護城河","source_freq":"法說","date":null,"evidence_refs":["substitute_technology#0"]}],"kill_metrics":[{"metric":"Utility 段季度有機成長＋半年 book-to-bill","bear_threshold":"有機轉負且 book-to-bill <1.0（清倉）","window":"2027Q1–2028Q4","source":"季報新聞稿分部表、法說","last_status":"ok"},{"metric":"Grid Infrastructure 有機成長","bear_threshold":"連 2 季 <5%（減碼一半）","window":"逐季，至 2028Q4","source":"季報法說","last_status":"ok"},{"metric":"全公司調整後營益率年變化＋價格成本生產力","bear_threshold":"連 2 季年減 ≥100bps 且價格成本為負（減碼一半）","window":"逐季","source":"季報新聞稿、法說","last_status":"warning"},{"metric":"淨負債／EBITDA","bear_threshold":"2027-12 仍 >2.5 倍（停止加碼）","window":"至 2027-12","source":"10-K、法說","last_status":"unknown"},{"metric":"資料中心銷售年增","bear_threshold":"連 2 季 <15%（停止加碼）","window":"2027 全年","source":"季報法說","last_status":"ok"}],"evidence_dismissed":[],"action_conditions":{"rearm_trigger":"收盤 ≤392 美元（FY2027E 共識 EPS 23.05×17 倍）且 Utility 有機成長未連 2 季 <3%，重跑分析後建首倉","exec_line":"首倉為正常部位一半，392 美元與 368 美元（16 倍）各一批；跌破但基本面無損就分批反買，不停損；加碼須等 2027-01 財測確認"}},"decision_inputs":{"signal":"B","ma":"🟠","cycle_position":"中循環","cycle_verdict":"等回踩","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場把 Utility 有機財測下修（7–9%→6–7%）與 Q4 營益率年減讀成需求轉弱；但下修來自電表代工缺料與控制屋產能爬坡，Utility 在手訂單年初至今增 5 億美元以上（約 +30%），變電站零組件成長 >20%","momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"價格錨：收盤 ≤392 美元（FY2027E 共識 EPS 23.05 美元×17 倍，Base 年報酬升到約 11%）才建首倉；例外：2027-01 財測證實 Utility 有機 ≥6% 且價格成本為正時，股價 ≤450 美元也可建首倉；其餘情況不追"},"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8w(原9b)","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟠'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場把 Utility 有機財測下修（7–9%→6–7%）與 Q4 營益率年減讀成需求轉弱；但下修來自電表代工缺料與控制屋產能爬坡，Utility 在手訂單年初至今增 5 億美元以上（約 +30%），變電站零組件成長 >20%"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟡', moat_trend='→', week26=-16.24, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position='中循環', moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":false,"basis":"signal='B', val='🟡'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":false,"basis":"signal='B', val='🟡', ma='🟠'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":true,"basis":"signal='B', val='🟡', ma='🟠'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟡', ma='🟠'"},{"row":"8w","condition":"判斷者宣告 wait_for_price（價格合理但要等）→ 原 row9b 進場改觀望（等價格）","hit":true,"basis":"wait_for_price=True, 等待條件='價格錨：收盤 ≤392 美元（FY2027E 共識 EPS 23.05 美元×17 倍，Base 年報酬升到約 11%）才建首倉；例外：2027-01 財測證實 Utility 有機 ≥6% 且價格成本為正時，股價 ≤450 美元也可建首倉；其餘情況不追'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":null,"requires_critic":[]},"thesis":{"H":[{"id":"H1","text":"公用事業輸配電投資周期延續，Utility 段 2027–2028 有機成長維持中高個位數，在手訂單轉為營收","2y":"FY2027 Utility 有機成長 ≥6%；Grid Infrastructure 有機 ≥8%","5y":"FY2031 Utility 段營收年複合 ≥6%（含 765kV 約 10 年 15 億美元機會，約貢獻 1 點）","10y":null,"threshold":"Utility TTM 有機成長 ≥5%","source":"季報新聞稿分部表、法說在手訂單與 book-to-bill 評論","drift_rule":"TTM 有機成長 <5% 連 2 季＝削弱；<3% 連 3 季＝反轉"},{"id":"H2","text":"調整後營益率在 FY2026 約 23.1% 基礎上擴張：價格成本生產力中性偏正、Electrical 利益率計畫與 NSI 成本協同 3–5%","2y":"FY2027 調整後營益率 ≥23.3%","5y":"FY2030 調整後營益率 ≥23.8%","10y":null,"threshold":"TTM 調整後營益率 ≥23.1%","source":"季報新聞稿；Q3 法說（2027 價格成本中性至正、增量利潤率 25–30%）","drift_rule":"TTM 較 23.1% 偏離 ≥5%（<21.9%）連 4 季＝削弱；偏離 ≥10%（<20.8%）連 6 季＝反轉"},{"id":"H3","text":"資料中心與擴產帶動 Electrical 份額提升：資料中心銷售 2027 年仍維持 20% 以上成長，占 Electrical 營收比重由約 15% 上升","2y":"FY2027 資料中心銷售年增 ≥20%；Electrical 有機 ≥8%","5y":"FY2030 資料中心占 Electrical 營收 ≥22%","10y":null,"threshold":"資料中心銷售年增 ≥20%","source":"季報法說資料中心揭露","drift_rule":"連 2 季 <15%＝削弱；連 3 季 <10%＝反轉"}],"R":[{"id":"R1","text":"大型公用事業延後輸配電資本支出，或 HUBB 自身產能（控制屋、變電站元件）跟不上，使在手訂單轉營收落後","h_ref":"H1","clock":"⚡","threshold":"Grid Infrastructure 有機成長連 2 季 <5%","evidence_refs":[]},{"id":"R2","text":"成本通膨與關稅快於漲價：價格成本生產力轉負，營益率擴張中斷（2025 年材料與關稅通膨曾吃掉約 3 個百分點毛利率）","h_ref":"H2","clock":"🔥","threshold":"價格成本生產力美元淨額連 2 季為負，且調整後營益率年減 ≥100bps","evidence_refs":["reg_tariff_export#1","competitive_share_entrants#1"]},{"id":"R3","text":"資料中心建置周期見頂、超大規模業者資本支出進入消化","h_ref":"H3","clock":"🔥","threshold":"資料中心銷售年增連 2 季 <15%","evidence_refs":[]},{"id":"R4","text":"重大併購與槓桿：NSI 30 億美元（約市值 13%）以 19 億美元優先債＋9 億美元定期貸款融資，若整合失速或去槓桿延後，利息與攤銷吃掉 EPS 增益","h_ref":"H2","clock":"🔥","threshold":"淨負債／EBITDA 2027 年底 >2.5 倍，或 NSI 營益率低於 Electrical 段平均","evidence_refs":["major_events#1","ma_merger#1"]},{"id":"R5","text":"供應鏈與貿易政策：部分電子元件供應商有限（Q3 電表代工缺料即一例），美中墨關稅與報復關稅推高成本","h_ref":"H2","clock":"⚡","threshold":"單季零件短缺遞延營收 ≥3000 萬美元，或管理層揭露關稅淨成本使營益率年減 ≥50bps","evidence_refs":["geo_supply_chain#0","geo_supply_chain#1","reg_tariff_export#0"]},{"id":"R6","text":"替代技術與捆綁：固態變壓器整合整流與變流功能、系統商整套出貨，可能繞過單一元件供應商","h_ref":"H1","clock":"🐢","threshold":"管理層揭露大型專案勝率低於過往，或主要公用事業客戶固態變壓器試點轉量產","evidence_refs":["substitute_technology#0"]}],"single_thing":{"description":"公用事業輸配電訂單周期轉向：Utility 段有機成長轉負且半年 book-to-bill 低於 1.0","why_fatal":"Utility 約占銷售 55%、調整後營業利益 56%，是 EPS 最大單一敏感項；轉負代表輸配電假設反轉，EPS 路徑落到 Bear（FY2029E 約 19 美元），倍數同步壓到 13–15 倍，股價約 250–330 美元","if_happens":"已持有即清倉並重跑分析；未持有則取消 392 美元建倉計畫","how_monitor":"每季新聞稿 Utility 有機成長、法說 book-to-bill 與在手訂單；2027-01 全年財測","probability":"12–24 個月約 15%（在手訂單年初至今約 +30%，短期轉負需要訂單快速崩落）"}},"appendix_a":{"growth_durability":6,"quality_score":7,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":18.64,"peg_fy2":1.57,"stress":{"pass":2,"total":3}},"eps_meta":{"base_eps_path":{"FY2025A":18.22,"FY2026E":20.59,"FY2027E":23.05,"FY2028E":25.49},"fy_end_month":12,"eps_basis":"調整後稀釋 EPS（排除併購無形資產攤銷等）；FY2025A 18.22 美元由 FY2026 財測 20.40–20.60 對應年增 12–13%（Q3 法說）回推，事實表 GAAP 稀釋 EPS 為 16.54；FY2026–28E 為 Koyfin 2026-10-31 共識，家數未載（營收共識 15 位）；三年年增 11.8%"},"catalysts":[{"date":"2027-01","date_precision":"month","type":"guidance","event":"Q4 2026 財報與 FY2027 全年財測（含資料中心與 Utility 有機成長）","impact":"高","watch":"Utility 有機 ≥6%、價格成本為正、營益率 ≥23.3%"},{"date":"2027-03-04","date_precision":null,"type":"guidance","event":"投資人日（Centralia, Missouri），更新長期成長與利益率框架","impact":"中","watch":"長期有機目標是否上調"},{"date":"2027-03","date_precision":"quarter","type":"capacity","event":"擴產節奏由每季約 2500 萬美元營收翻倍到約 5000 萬美元","impact":"中","watch":"控制屋與變電站元件出貨季增"},{"date":"2027-03","date_precision":"quarter","type":"product","event":"首個 765kV 專案出貨","impact":"低","watch":"765kV 管線與指定規格進度"}]}
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
