你是 DD 管線 v20 的判斷層閘（gate），標的 NOW（20261102）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（41 條）
- `f_kpi0_total_revenues_gaap`（q1_business）｜Total revenues (GAAP)＝4106 USD m｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 https://s205.q4cdn.com/916135447/files/content_files/ServiceNow-Reports-Third-Quarter-2026-Financial-Results.pdf（numbers.latest_quarter_kpis.items[0]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-28））
- `f_kpi1_subscription_revenues_ga`（q1_business）｜Subscription revenues (GAAP)＝3988 USD m｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 https://s205.q4cdn.com/916135447/files/content_files/ServiceNow-Reports-Third-Quarter-2026-Financial-Results.pdf（numbers.latest_quarter_kpis.items[1]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-28））
- `f_kpi2_non_gaap_operating_incom`（q1_business）｜Non-GAAP operating income / margin＝1338 USD m｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 https://s205.q4cdn.com/916135447/files/content_files/ServiceNow-Reports-Third-Quarter-2026-Financial-Results.pdf（numbers.latest_quarter_kpis.items[2]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-28））
- `f_kpi3_gaap_operating_income_ma`（q1_business）｜GAAP operating income / margin＝385 USD m｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 https://s205.q4cdn.com/916135447/files/content_files/ServiceNow-Reports-Third-Quarter-2026-Financial-Results.pdf（numbers.latest_quarter_kpis.items[3]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-28））
- `f_kpi4_free_cash_flow_non_gaap`（q1_business）｜Free cash flow (non-GAAP)＝822 USD m｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 https://s205.q4cdn.com/916135447/files/content_files/ServiceNow-Reports-Third-Quarter-2026-Financial-Results.pdf（numbers.latest_quarter_kpis.items[4]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-28））
- `f_kpi5_sbc`（q4_capital）｜SBC＝633 USD m｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 https://s205.q4cdn.com/916135447/files/content_files/ServiceNow-Reports-Third-Quarter-2026-Financial-Results.pdf（numbers.latest_quarter_kpis.items[5]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-28））
- `f_kpi8_crpo`（q1_business）｜cRPO＝13650 USD m｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 https://s205.q4cdn.com/916135447/files/content_files/ServiceNow-Reports-Third-Quarter-2026-Financial-Results.pdf（numbers.latest_quarter_kpis.items[8]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-28））
- `f_kpi9_rpo`（q1_business）｜RPO＝29700 USD m｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 https://s205.q4cdn.com/916135447/files/content_files/ServiceNow-Reports-Third-Quarter-2026-Financial-Results.pdf（numbers.latest_quarter_kpis.items[9]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-28））
- `f_kpi10_customers_5m_acv`（q1_business）｜Customers >$5M ACV＝680 count｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 https://s205.q4cdn.com/916135447/files/content_files/ServiceNow-Reports-Third-Quarter-2026-Financial-Results.pdf（numbers.latest_quarter_kpis.items[10]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-28））
- `f_kpi11_subscription_gross_margi`（q1_business）｜Subscription gross margin (non-GAAP)＝80 %｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 https://s205.q4cdn.com/916135447/files/content_files/ServiceNow-Reports-Third-Quarter-2026-Financial-Results.pdf（numbers.latest_quarter_kpis.items[11]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-28））
- `f_earnings_recency`（q1_business）｜最近一次財報日＝2026-10-28 date｜期間與口徑：2026-10-28／距今 3 個交易日｜kind：realized
  - 來源：—（numbers.earnings_recency，as_of 2026-10-28）
- `f_peer_now_gross_margin_pct`（q2_moat）｜NOW 毛利率＝73.08 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.NOW.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_now_operating_margin_pct`（q2_moat）｜NOW 營業利益率＝9.68 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.NOW.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_now_fcf_margin_pct`（q2_moat）｜NOW FCF 利潤率＝30.78 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.NOW.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_crm_operating_margin_pct`（q2_moat）｜CRM 營業利益率＝21.52 %｜期間與口徑：TTM ending 2026-07-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CRM.operating_margin_pct，as_of TTM ending 2026-07-31（4季加總））
- `f_peer_msft_operating_margin_pct`（q2_moat）｜MSFT 營業利益率＝47.1 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MSFT.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_pltr_operating_margin_pct`（q2_moat）｜PLTR 營業利益率＝42.8 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.PLTR.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_ddog_operating_margin_pct`（q2_moat）｜DDOG 營業利益率＝0.43 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.DDOG.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝3.97 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-10-31）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝4.83 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-10-31）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝5.92 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-10-31）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝16233.51 USD m｜期間與口徑：2026-11-02／yfinance revenue_estimate 0y 平均（39 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-02）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝19268.01 USD m｜期間與口徑：2026-11-02／yfinance revenue_estimate +1y 平均（46 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-02）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝0.0 %｜期間與口徑：2026-10-30（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-10-30（RTH 收盤，UTC））
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝3808.0 USD m｜期間與口徑：2026-11-02／yfinance 最新一季：總債務 8415.0、現金 4607.0（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-02）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝1037.92 m shares｜期間與口徑：2026-11-02／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-11-02）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝26.48 x｜期間與口徑：2026-10-31／分母＝FY1 EPS 3.97，分子＝快照價 105.12｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-10-31）
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝105.12 USD｜期間與口徑：2026-10-30（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-10-30（RTH 收盤，UTC））
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝75.63 x｜期間與口徑：2026-10-30（RTH 收盤，UTC）／4 個年度端點內的分位＝0.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-10-30（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝0.0 %｜期間與口徑：2026-10-30（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-10-30（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝0.0 %｜期間與口徑：2026-10-30（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-10-30（RTH 收盤，UTC））
- `f_ev_s_fwd`（q5_valuation）｜EV/S（EV ÷ FY1 共識營收）＝6.96 x｜期間與口徑：2026-11-02／f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）｜kind：estimate
  - 來源：—（numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m，as_of 2026-11-02）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_ev_m`（q5_valuation）｜目前企業價值 EV（市值＋淨負債）＝112913.84 USD m｜期間與口徑：2026-11-02／市值 109105.84 ＋ 淨負債 3808.0｜kind：realized
  - 來源：—（numbers.capital_structure.ev_m，as_of 2026-11-02）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_consensus_rev_fy1_pct`（q5_valuation）｜FY1 共識修正＝-2.46 %｜期間與口徑：2026-10-31／兩份 Koyfin 快照之間的 EPS 修正幅度（4.07 → 3.97）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.fy1.revision_pct，as_of 2026-10-31）
- `f_consensus_rev_fy2_pct`（q5_valuation）｜FY2 共識修正＝-3.4 %｜期間與口徑：2026-10-31／兩份 Koyfin 快照之間的 EPS 修正幅度（5.0 → 4.83）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.fy2.revision_pct，as_of 2026-10-31）
- `f_consensus_rev_fy3_pct`（q5_valuation）｜FY3 共識修正＝-2.15 %｜期間與口徑：2026-10-31／兩份 Koyfin 快照之間的 EPS 修正幅度（6.05 → 5.92）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.fy3.revision_pct，as_of 2026-10-31）
- `f_rsi14`（q5_valuation）｜RSI(14)＝26.86｜期間與口徑：2026-10-30（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-10-30（RTH 收盤，UTC））
- `f_ma_state`（q5_valuation）｜週線均線六態（decision_inputs.ma 必須等於此值）＝❌｜期間與口徑：2026-11-02／timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-02）
  - 原文：「price 105.12 / W52 123.36 / W104 157.76 / W250 134.41 / W250 13週斜率 0.2%」
- `f_ma_w52`（q5_valuation）｜52 週均線＝123.36 USD｜期間與口徑：2026-11-02／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-02）
- `f_ma_w104`（q5_valuation）｜104 週均線＝157.76 USD｜期間與口徑：2026-11-02／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-02）
- `f_ma_w250`（q5_valuation）｜250 週均線＝134.41 USD｜期間與口徑：2026-11-02／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-02）

### findings_digest 中方向為負或來源衝突的條目（15 條）
- `competitive_share_entrants#1`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K 風險因素：雲端與 AI 原生廠商可能開發更多商業應用與 AI 自動化方案與公司競爭；系統記錄廠商可能阻擋整合、對手可能捆綁降價。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A Risk Factors（as_of 2026-01-29）｜affects：moat_trend、decision_inputs.bear
- `competitive_share_entrants#2`（competitive_share_entrants｜方向 -｜狀態 ok）：The Register 評論：Salesforce 推出對 ServiceNow 迄今最可信的威脅（Agentforce ITSM）。
  - 來源：The Register: Salesforce has come up with the most credible threat yet to ServiceNow（as_of 2025-12-05）｜affects：moat_trend、decision_inputs.bear
- `customer_concentration_credit#2`（customer_concentration_credit｜方向 -｜狀態 ok）：2026 Q2 10-Q：同一聯邦通路夥伴占 2026 年 6/30 應收帳款 12%，占當季及上半年營收 13%（去年同期 11%），集中度上升；信用評估仍無收款問題。
  - 來源：SEC EDGAR 10-Q 2026-06-30（as_of 2026-07-29）｜affects：thesis.R、decision_inputs.bear
- `supply_demand_durability#2`（supply_demand_durability｜方向 -｜狀態 ok）：Bloomberg Intelligence 預期 AI agent 將把應用軟體定價由 seat 轉向用量／成果計價，利潤率可能壓縮 100–900bp；Global X 稱 seat-based 為最受衝擊模式。
  - 來源：Bloomberg Intelligence Agentic AI Deep Dive / Global X ETFs（as_of 2026-03-01）｜affects：decision_inputs.bear、thesis.R、moat_trend
- `regulatory_antitrust#0`（regulatory_antitrust｜方向 -｜狀態 ok）：10-K 揭露：公司向美國政府機關通報內部調查（Army CIO 聘用案）並配合司法部（DOJ）自行展開的調查；公司無法預測時程、結果或影響。
  - 來源：SEC EDGAR 10-K FY2025 Item 7 MD&A（as_of 2026-01-29）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：NOW 10-K FY2025 風險因子：受海關法管轄，部分情況須自付美國及他國進口關稅，較高進口關稅會提高營運成本；亦受出口管制與經濟制裁法約束，俄烏衝突下可能有更廣的制裁與出口限制。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-01-29）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：ServiceNow Q1 2026 稱中東衝突使數筆大型地端交易延後，約拖累訂閱營收成長 75 bps
  - 來源：CFO Dive: ServiceNow CFO says Iran conflict delayed large deals（as_of 2026-04-23）｜affects：thesis.R、decision_inputs.bear
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：公司 10-K 風險因子自述：AI、低程式碼/無程式碼等能力日益重要，公司正與替代方案與做法競爭，且預期隨產品進入新鄰近市場會有更多競爭。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A Risk Factors（as_of 2026-01-29）｜affects：moat_trend、thesis.R、decision_inputs.bear
- `substitute_technology#2`（substitute_technology｜方向 -｜狀態 ok）：二手評論稱 AI 工具（如 Claude Code）降低軟體開發門檻，企業可能自建內部工作流工具；且 agent 取代人力可能減少座位授權。
  - 來源：247WallSt: ServiceNow was the SaaS stock AI was supposed to kill（as_of 2026-07-06）｜affects：moat_trend、decision_inputs.bear
- `substitute_technology#3`（substitute_technology｜方向 -｜狀態 ok）：Seeking Alpha 文章稱 ServiceNow 為 SaaSpocalypse 主要受害者，涉及座位制軟體模式受 AI agent 衝擊。
  - 來源：Seeking Alpha: ServiceNow Is The Main Victim Of The SaaSpocalypse（as_of 2026-03-01）｜affects：moat_trend、valuation
- `capital_markets_pricing#3`（capital_markets_pricing｜方向 -｜狀態 ok）：2026 年春季目標價下修：Goldman 216→188、BTIG 200→185（BTIG 標題指 FY26 營收成長 guidance 受質疑）、Citi 177→154（4/23）；之後 Capital One 105→120（5/5）、Needham 115→155、BTIG 150→170（後兩者日期未載）。
  - 來源：Yahoo Finance: ServiceNow Price Target Cut to $185 by BTIG / Placera telegram（as_of 2026-04-08）｜affects：valuation、decision_inputs.bear
- `capital_markets_pricing#4`（capital_markets_pricing｜方向 -｜狀態 ok）：Citi 目標價由 $177 調降至 $154，維持買進
  - 來源：Placera telegram（as_of 2026-04-23）｜affects：valuation
- `major_events#3`（major_events｜方向 -｜狀態 ok）：10-K 與 2026 年三份 10-Q 揭露 DOJ 對一項政府合約合規問題的調查（前美軍 CIO 聘僱案），公司無法預測時程與結果。
  - 來源：SEC EDGAR｜10-K FY2025 / 10-Q FY2026（經搜尋摘要轉述）（as_of 2026-01-29）｜affects：decision_inputs.bear、thesis.R
- `ma_merger#1`（ma_merger｜方向 -｜狀態 ok）：Armis 收購部分現金對價由 2026-04-17 的 40 億美元定期貸款支應。
  - 來源：SEC EDGAR｜8-K 2026-04-22 Item 1.01（as_of 2026-04-22）｜affects：valuation、decision_inputs.bear
- `lawsuit_class_action#1`（lawsuit_class_action｜方向 -｜狀態 ok）：2026-10 原告律所 Levi & Korsinsky（經 SueWallSt）發出對 NOW 的投資人調查通告；搜尋未見已提起之集體訴訟。
  - 來源：Placera｜ServiceNow Investigation Notice: SueWallSt Notifies Investors（as_of 2026-10-30）｜affects：decision_inputs.bear

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 9 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/NOW_20261102/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":278.2,"bear_5y_price":72.0,"p_bull_pct":25,"p_bear_pct":30,"upside_5y_pct":76.8,"ev5y_pct":66.3,"irr_base_pct":12.1,"asym_ratio":4.4,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":3.97,"pe":26.48,"basis":"FY2026E 共識 non-GAAP 稀釋 EPS（Koyfin 2026-10-31）；判斷日距年度結束只剩一季，與終端 FY2031E 同為當年度口徑"},"eps":{"bull":[4.95,6.15,7.5,9.0,10.7],"base":[4.75,5.7,6.7,7.75,8.85],"bear":[4.35,4.5,4.62,4.72,4.8]},"pe":{"bull":26,"base":21,"bear":15},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0,"net_buyback":0},"second_stage":{"bull_cagr_pct":15,"base_cagr_pct":10},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### NOW_Q2_2026_Earnings_Call_20260722.md
- 2026-07-22｜CFO｜guidance：Q3 訂閱營收財測區間（原話："we expect subscription revenues between $3.975 billion and"）
- 2026-07-22｜CFO｜guidance：Q3 cRPO 成長財測 20%（固定匯率）（原話："We expect cRPO growth of 20% on a constant"）
- 2026-07-22｜CFO｜guidance：Q3 營業利益率財測 31%（原話："We expect operating margin of 31%"）
- 2026-07-22｜CFO｜guidance：全年訂閱營收財測中點上調 1,500 萬美元（原話："we're raising our subscription revenues by $15 million"）
- 2026-07-22｜CFO｜guidance：全年營業利益率財測 31.5%（原話："We expect operating margin of 31.5% and free cash"）
- 2026-07-22｜CFO｜margin：全年訂閱毛利率財測 81%（原話："subscription gross margin of 81%"）
- 2026-07-22｜CFO｜margin：Q2 非 GAAP 營業利益率 29.5%，高於財測 300bp（原話："Non-GAAP operating margin was 29.5%, 300 basis points above"）
- 2026-07-22｜CFO｜margin：管理層說明 Q2 利益率超標原因含行銷支出時點（原話："timing of spend, primarily in marketing"）
- 2026-07-22｜CFO｜margin：毛利率短期承壓原因：hyperscaler 與 AI 消耗；營業利益率持平（原話："both good reasons for a little bit of short-term pressure"）
- 2026-07-22｜CFO｜margin：毛利率承壓下營業利益率持平（原話："even though we had a little pressure on gross margin,"）
- 2026-07-22｜Amit Zavery｜margin：管理層稱不擔心 token 使用對利益率的影響（原話："we are not really worried about the margin impact"）
- 2026-07-22｜CFO｜guidance：Q2 超標部分來自聯邦在地部署營收由 Q3 提前（原話："Part of that outperformance was due to strong U.S. federal"）
- 2026-07-22｜CFO｜guidance：CFO 稱 Q3 與全年財測有信心（原話："I'm very confident in our Q3 and full year"）
- 2026-07-22｜CFO｜guidance：CFO 說明約一半超標為 on-prem 提前認列（原話："a pull forward of on-prem for a quarter, right?"）
- 2026-07-22｜CFO｜guidance：CFO 說明全年上調對應淨新增 ACV 超標部分（原話："we passed along all of the net new ACV overachievement"）
- 2026-07-22｜CFO｜guidance：CFO 表示下半年財測採審慎（原話："being prudent for back half as most would expect"）
- 2026-07-22｜CFO｜guidance：CFO 稱採保守審慎財測（原話："at a conservative prudent guide, right?"）
- 2026-07-22｜CEO｜commitment：McDermott 承諾 2026 年底人數回到收購前水準（原話："exact same headcount before we did the acquisitions"）
- 2026-07-22｜CEO｜commitment：管理層重申 2030 年營收目標 320 億美元（原話："we set a course to $32 billion in revenue in 2030"）
- 2026-07-22｜CFO｜commitment：CFO 重申 2030 年 Rule of 60 路徑（原話："well on our way to the Rule of 60 by 2030"）
- 2026-07-22｜CEO｜commitment：AI ACV 目標 15 億美元（2026 年底）（原話："target of $1.5 billion ACV by the end of 2026."）
- 2026-07-22｜CFO｜commitment：AI 占 ACV 30%（2030）目標，稱追蹤領先（原話："we're already tracking ahead of our target for AI to reach"）
- 2026-07-22｜CEO｜product：ServiceNow AI ACV 突破 10 億美元（原話："surpassing $1 billion, keeping us on track to beat our"）
- 2026-07-22｜CFO｜product：新 AI 原生 SKU 升級帶來價格提升 20%-30%（原話："our new AI native SKUs are driving price uplift in"）
- 2026-07-22｜CFO｜product：Pro Plus SKU 價格提升（原話："Our pricing uplift for our Pro Plus SKUs continues to"）
- 2026-07-22｜Amit Zavery｜product：L1 AI 專員客戶使用成果（原話："close to 80% to 85% of the service requests"）
- 2026-07-22｜Amit Zavery｜product：AI Control Tower 客戶數（原話："more than 500-plus customers already live"）
- 2026-07-22｜CEO｜product：預告新的 AI 原生產品與商業模式（原話："a business model evolution that expands our TAM"）
- 2026-07-22｜CEO｜product：新產品形態：對話式服務台（原話："a conversational service desk experience, no tickets"）
- 2026-07-22｜CEO｜product：新產品鎖定客群（原話："we're targeting the Fortune 500,000"）
- 2026-07-22｜Amit Zavery｜product：混合定價結構（授權加用量）（原話："where it's a combination of license and usage"）
- 2026-07-22｜Amit Zavery｜competition：管理層稱競爭對手與 LLM 無法取得其情境資料（原話："our competitors don't get access to it"）
- 2026-07-22｜CEO｜competition：管理層稱 seat 壓縮不是問題（原話："we worried about seat compression? Not at all."）
- 2026-07-22｜CEO｜competition：新增業務中非 seat 計價占比（原話："our net new business is already non-seat-based."）
- 2026-07-22｜CEO｜competition：管理層稱自建成本遠高於採用其平台（原話："it will cost 5 to 10x to build an agent versus run one"）
- 2026-07-22｜CEO｜competition：管理層談資安排名與目標（原話："move up the leaderboard from a #8 company to"）
- 2026-07-22｜CEO｜competition：管理層將 Mythos 事件定位為對公司有利（原話："Mythos was a gift to the"）
- 2026-07-22｜Amit Zavery｜competition：管理層稱 LLM 商品化（原話："There is no reason for using some of these most expensive"）
- 2026-07-22｜CEO｜risk：被問銷售週期是否受影響，管理層答無（原話："I have not. In fact, the key here, Gregg,"）
- 2026-07-22｜CEO｜risk：合約年限拉長（原話："they're actually elongating, and you see that in the cRPO"）
- 2026-07-22｜CFO｜customer：Q2 續約率 98%（原話："Our renewal rate was a best-in-class 98% in Q2"）
- 2026-07-22｜CFO｜customer：年 ACV 逾 500 萬美元客戶數（原話："658 customers generating over $5 million in ACV"）
- 2026-07-22｜CEO｜customer：Q2 百萬美元以上淨新增 ACV 交易數（原話："We had 123 deals greater than $1 million in net new ACV"）
- 2026-07-22｜CFO｜customer：RPO 與 cRPO 口徑（原話："approximately $29 billion, representing 22% year-over-year"）
- 2026-07-22｜CEO｜customer：Experian 五年期合約（原話："In a 5-year deal and many deals are going longer"）
- 2026-07-22｜CEO｜customer：Maybank 五年期合約（原話："another 5-year deal, so much for deal shortening, right?"）
- 2026-07-22｜CFO｜capital_allocation：銷售人力增加的原因含併購（原話："So it's all three."）
- 2026-07-22｜CFO｜capital_allocation：管理層預期下半年銷售人力續增（原話："As you would expect, you'll see more sales heads as a"）
- 2026-07-22｜CEO｜capital_allocation：管理層談去年底收購遭批評（原話："took some criticism for"）

### NOW_Analyst_Investor_Day_ServiceNow_Inc_20260504.md
- 2026-05-04｜William McDermott｜guidance：CEO 表示 2030 年前訂閱營收承諾為 300 億美元以上。（原話："a sub revenue $30 billion plus commit between now and 2030"）
- 2026-05-04｜Gina Mastantuono｜guidance：CFO 表示以目前動能，2030 年訂閱營收可達 2026 年 150 億目標的兩倍。（原話："Our momentum puts us on pace to double that target in 2030."）
- 2026-05-04｜Gina Mastantuono｜guidance：CFO 另給出較高情境：自 2026 年財測起算的 CAGR 逾 20%，2030 年訂閱營收 320 億美元；並說明不要求投資人現在就以此估值。（原話："$32 billion of subscription revenue in 2030"）
- 2026-05-04｜Gina Mastantuono｜guidance：CFO 說明三大成長動能（資安、資料、AI）合計 2030 年前年成長率超過 25%。（原話："these three vectors compound at over 25% growth"）
- 2026-05-04｜Gina Mastantuono｜guidance：CFO 表示長期目標已內含較成熟產品成長放緩的假設。（原話："this does prudently bake in a deceleration"）
- 2026-05-04｜Gina Mastantuono｜guidance：CFO 將 2026 年 AI ACV 目標由 10 億美元調升至 15 億美元。（原話："we're raising our 2026 AI ACV target from $1"）
- 2026-05-04｜Gina Mastantuono｜guidance：CFO 設定 2030 年 AI 產品占 ACV 比重 30% 的目標。（原話："by 2030, we expect 30% of our ACV from ServiceNow AI"）
- 2026-05-04｜Gina Mastantuono｜guidance：CFO 預告 2027 年恢復正常化利潤率擴張（含 Armis）。（原話："return to normalized margin expansion in 2027"）
- 2026-05-04｜Gina Mastantuono｜commitment：CFO 承諾 2027 年 non-GAAP 營業利益率與自由現金流利潤率各擴張 100 bps（同段話口徑含 Armis）。（原話："100 basis points of free cash flow margin expansion"）
- 2026-05-04｜Gina Mastantuono｜commitment：CFO 宣布股票薪酬占營收低於 10% 的時間點為 2029 年。（原話："Today we'll tell you when, 2029."）
- 2026-05-04｜Gina Mastantuono｜commitment：CFO 表示 2030 年達成 Rule of 60+（營收成長加自由現金流利潤率）。（原話："achieving the Rule of 60+ by 2030."）
- 2026-05-04｜William McDermott｜margin：CEO 說明目前成長率加自由現金流利潤率合計 56，目標 60 以上。（原話："Right now, it's 56, it's going to 60-plus"）
- 2026-05-04｜William McDermott｜commitment：CEO 提出 AI 上線 100 天內的滿意度保證，並說明次日 Knowledge 大會會正式推出。（原話："A total satisfaction guarantee on AI go-lives"）
- 2026-05-04｜Gina Mastantuono｜margin：CFO 說明 AI 推理僅占服務成本不到 10%，用以回應推理成本壓縮毛利率的疑慮。（原話："AI reasoning is less than 10% of our cost to serve."）
- 2026-05-04｜Gina Mastantuono｜margin：CFO 表示訂閱毛利率將維持 80% 以上，同時承認轉向超大型雲端業者短期壓抑毛利率。（原話："our move to hyperscalers is impacting gross margins"）
- 2026-05-04｜Gina Mastantuono｜margin：CFO 說明 2026 年自身導入代理式 AI 的年化成本節省口徑：2026 年新增 2 億、2025 年 1 億，合計 3 億美元。（原話："$300 million in expected annualized cost savings"）
- 2026-05-04｜William McDermott｜margin：CEO 表示今年年底員工人數將與年初相同。（原話："leave this year with the exact headcount that we"）
- 2026-05-04｜Gina Mastantuono｜margin：CFO 說明 AI ACV 的計算口徑：只計增量，基本訂閱不算入。（原話："We are only counting that incremental."）
- 2026-05-04｜Gina Mastantuono｜margin：CFO 補充 AI 營收口徑：不像部分同業把全部營收都算成 AI。（原話："we're not counting every single dollar of revenue as AI"）
- 2026-05-04｜Gina Mastantuono｜guidance：CFO 說明新 AI 原生封裝下，客戶購買較高階套裝的平均價格提升幅度。（原話："we expect to see an average price lift of 20% to 30%"）
- 2026-05-04｜Gina Mastantuono｜guidance：CFO 回答 Prime 滲透速度：模型內建與 Pro 相近的保守爬坡，實際略快。（原話："building in a similar ramp with our AI that we had with Pro."）
- 2026-05-04｜Gina Mastantuono｜guidance：CFO 說明 Prime 定價與 Pro Plus 相同，漲價來自低階客戶往上升級。（原話："we're not increasing pricing in our most"）
- 2026-05-04｜Gina Mastantuono｜product：CFO 揭露 Now Assist ACV 於 Q1 突破 7.5 億美元。（原話："momentum carried into Q1 with ACV crossing $750 million"）
- 2026-05-04｜Jon Sigler｜product：產品長表示 Action Fabric 讓外部 AI 代理呼叫平台時消耗 Assist 額度而計費。（原話："the flywheel is going to spin faster"）
- 2026-05-04｜Jon Sigler｜product：Sigler 說明 Now Assist 目前規模與年底預期。（原話："This will be $1.5 billion by the end of the year."）
- 2026-05-04｜Amit Zavery｜product：Amit 表示 CRM 業務 ACV 將突破 20 億美元。（原話："which will help our CRM business cross $2 billion in ACV"）
- 2026-05-04｜Gina Mastantuono｜product：CFO 揭露 2025 年資安與風險新增 ACV 成長 40%。（原話："net new ACV grew 40% year-on-year"）
- 2026-05-04｜Amit Zavery｜product：Amit 表示資料分析產品線預計成為十億美元事業。（原話："data analytics is on track to be a billion-dollar business"）
- 2026-05-04｜Pat Casey｜product：Pat Casey 說明首個自主 AI 員工（L1 服務台）目前的試點客戶數。（原話："I've got 6 live pilot customers"）
- 2026-05-04｜Amit Zavery｜product：Amit 說明為中型市場打造的 AI 原生服務管理產品，採純消耗型計價。（原話："entirely consumption-based and conversation first"）
- 2026-05-04｜Gina Mastantuono｜customer：CFO 說明 2025 年更新的既有 Now Assist 客戶 ACV 平均擴張幅度。（原話："their ACV by an average of over 3x"）
- 2026-05-04｜Gina Mastantuono｜customer：CFO 揭露 2025 年新增 ACV 中來自五個以上產品交易的占比。（原話："91% of our net new ACV came from deals with 5 or more"）
- 2026-05-04｜Gina Mastantuono｜customer：CFO 以 20 人客服團隊為例，說明客戶總成本與 ServiceNow 支出的變化。（原話："ServiceNow spend grows over 5x."）
- 2026-05-04｜Gina Mastantuono｜customer：CFO 推算 IT 事件管理一個用例的 ACV 機會，假設 75% 事件由自主勞動力處理。（原話："can be processed by an autonomous workforce"）
- 2026-05-04｜Gina Mastantuono｜customer：CFO 說明客戶 AI 旅程第五年預計支出為起始 Assist 授權量的倍數。（原話："this AI customer would be spending 4.5x the initial Assist"）
- 2026-05-04｜Bhavin Shah｜customer：Bhavin Shah 說明 Moveworks 整合後的管線成長。（原話："we've seen a 10x pipeline build"）
- 2026-05-04｜Gina Mastantuono｜capital_allocation：CFO 說明 2026 年 Q1 的 ASR 規模。（原話："In Q1 alone, the $2 billion ASR"）
- 2026-05-04｜Gina Mastantuono｜capital_allocation：CFO 預期 2026 年稀釋淨中性，並說明剩餘買回額度。（原話："We expect to be dilution net neutral for 2026."）
- 2026-05-04｜Gina Mastantuono｜capital_allocation：CFO 列出剩餘買回授權額度。（原話："$4.2 billion in authorization remaining"）
- 2026-05-04｜Gina Mastantuono｜capital_allocation：CFO 表述資本配置第二順位：以開拓新 TAM 或加速產品路線圖的小型併購為主。（原話："with a focus on tuck-ins that open new TAMs"）
- 2026-05-04｜William McDermott｜capital_allocation：CEO 表示 300 億與 320 億的長期目標未納入大型併購。（原話："we did not put large-scale M&A in there."）
- 2026-05-04｜William McDermott｜capital_allocation：CEO 為 Moveworks、Veza、Armis 的收購辯護，稱非為買營收成長。（原話："We were buying a ticket to a bright future."）
- 2026-05-04｜Paul Fipps｜competition：Paul Fipps 回應同業稱搶走份額的說法。（原話："We just don't see them in the competitive stack."）
- 2026-05-04｜William McDermott｜competition：CEO 對同業言論表達不滿。（原話："we're getting a little annoyed"）
- 2026-05-04｜Amit Zavery｜competition：Amit 主張企業市場沒有能同時提供平台、資料、資安與自主勞動力的競爭者。（原話："In the enterprise space, there's nobody like us."）
- 2026-05-04｜Amit Zavery｜competition：Amit 引用 Gartner 預測，用於主張未受治理的 AI 專案會失敗。（原話："40% of agenetic AI projects will fail by 2027"）
- 2026-05-04｜Amit Zavery｜competition：Amit 針對自建對購買主張，稱自建 LLM 方案成本更高。（原話："customers building their own LLM-based solution"）
- 2026-05-04｜Gina Mastantuono｜competition：CFO 回應 AI 取代平台、座位壓縮的疑慮，定位為單一類別。（原話："we are in a category of one"）
- 2026-05-04｜William McDermott｜competition：CEO 表示將平台下沉至中型市場。（原話："take a platform down market a bit"）
- 2026-05-04｜Gina Mastantuono｜risk：CFO 點名市場疑慮之一：座位壓縮是否侵蝕營收。（原話："Will seat compression shrink revenue?"）
- 2026-05-04｜William McDermott｜risk：CEO 說明活躍使用者數未下降，作為座位壓縮疑慮的回應。（原話："our active users aren't going down because we go east"）
- 2026-05-04｜William McDermott｜risk：CEO 提到客戶對模型 token 化計價造成預算超支感到意外。（原話："surprised on the tokenization of models"）
- 2026-05-04｜Bhavin Shah｜risk：Bhavin Shah 承認並非所有流程都會立即代理化。（原話："not everything will be agentified immediately."）
- 2026-05-04｜Gina Mastantuono｜guidance：CFO 說明非座位計價占新增 ACV 的比重。（原話："half of our net new ACV has already shifted"）
- 2026-05-04｜Gina Mastantuono｜guidance：CFO 回答非座位占比長期走向：預期持續上升但不會到 100%。（原話："I don't think it'll ever be 100%."）
- 2026-05-04｜Amit Zavery｜product：Amit 宣稱座位制計價無法反映 AI 價值，公司已轉向混合計價。（原話："seat-based pricing does not reflect the value of AI"）
- 2026-05-04｜Amit Zavery｜product：Amit 揭露混合與消耗型計量在過去一年新增業務中的占比。（原話："hybrid and consumptive meters accounted for more than"）
- 2026-05-04｜Gina Mastantuono｜commitment：CFO 回答兩種 2030 情境差異：因市場不確定而給區間，對 320 億有高度信心。（原話："prudent to give a range in not just one number"）
- 2026-05-04｜Gina Mastantuono｜guidance：CFO 說明 2026 年財測高於 155 億美元，並稱有機超越 2021 年所訂 150 億目標 5 億美元。（原話："I know the guide is higher than $15.5 billion."）
- 2026-05-04｜Gina Mastantuono｜customer：CFO 揭露來自公有雲夥伴的新增 ACV 成長。（原話："net new ACV from public cloud partners nearly tripled"）

### 問答異常語氣（迴避／改口／保留）
- NOW_Q2_2026_Earnings_Call_20260722.md｜問：Gabriela Borges 問 L1 ITSM 產品週期中客戶加碼支出的幅度｜答法：Zavery 與 Mastantuono 回以處理率、AI ACV 總量與 30% 目標，未給客戶加碼支出數字
- NOW_Q2_2026_Earnings_Call_20260722.md｜問：Michael Turrin 問 Q3 財測是否因聯邦遞延影響而偏審慎｜答法：Mastantuono 回稱管線良好；McDermott 轉談資安，未直接回答 Q3 財測審慎程度
- NOW_Q2_2026_Earnings_Call_20260722.md｜問：Brad Zelnick 問 AI 消耗與 token 價格對毛利率的上下行風險｜答法：Mastantuono 與 Zavery 談中期壓力減輕與模型組合，未提供毛利率量化區間
- NOW_Q2_2026_Earnings_Call_20260722.md｜問：Tyler Radke 問全年上調幅度相對 Q2 超標偏小的原因｜答法：Mastantuono 稱約半數為 on-prem 提前，並稱下半年審慎，同時說仍有上行空間
- NOW_Analyst_Investor_Day_ServiceNow_Inc_20260504.md｜問：Zukin（Wolfe）問：同業說正在搶 ServiceNow 份額，競爭格局與資安如何推高目標。｜答法：Fipps 未給份額或贏率數字，稱同業在其競爭名單中看不到；McDermott 另以情緒語氣（'getting a little annoyed'）回應，未提供量化資料。
- NOW_Analyst_Investor_Day_ServiceNow_Inc_20260504.md｜問：Weiss（Morgan Stanley）問：開放平台讓第三方代理接入時，相對自家自主員工 5 倍提升的增量是多少。｜答法：Gina 只回答第一題 Prime 爬坡；Amit 回答開放架構與計量機制，未提供第三方代理的增量倍數或金額。
- NOW_Analyst_Investor_Day_ServiceNow_Inc_20260504.md｜問：Bhatia（William Blair）問：何時多數營收（非僅新增 ACV）會轉為消耗型／非座位制。｜答法：Gina 稱未給時間表，只說 50% 會續升但不會到 100%。
- NOW_Analyst_Investor_Day_ServiceNow_Inc_20260504.md｜問：未具名分析師問：30% AI ACV 隱含非 AI 部分 CAGR 約 10% 以下，這是否令人擔憂。｜答法：Gina 稱這樣想是 '100% the wrong way'，改談 AI 拉動核心與 Pro 先例，未給非 AI 部分的成長數字。
- NOW_Analyst_Investor_Day_ServiceNow_Inc_20260504.md｜問：Samana（Jefferies）問：30% AI ACV（約 90 億美元）中，現有產品與路線圖各占多少。｜答法：Gina 只回答定價與滲透假設，未拆分現有產品與路線圖的貢獻。

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 3 | 2 |
| customer_second_source | found | 1 | 1 |
| customer_concentration_credit | found | 3 | 1 |
| supply_demand_durability | found | 4 | 2 |
| regulatory_antitrust | found | 3 | 3 |
| reg_tariff_export | found | 2 | 1 |
| geo_supply_chain | found | 2 | 2 |
| end_markets | found | 4 | 3 |
| substitute_technology | found | 5 | 2 |
| channel_business_model_shift | found | 4 | 2 |
| capital_markets_pricing | found | 5 | 4 |
| major_events | found | 4 | 5 |

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260723","verdict":"進場","role":"核心","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"工作流治理護城河（CMDB + Context Engine + agent 治理）抵禦 agentic 侵蝕，ITSM 份額不流失、有機成長守住中位數以上"},{"id":"H2","text":"消費/非座位計量新價格模型（Foundation/Advanced/Prime，>50% 新 ACV 非座位）驅動 AI 變現、抵銷座位去化——且 AI ACV 淨於 Gartner 40% 取消率後仍複利"},{"id":"H3","text":"19x 的品類 de-rating 已過度；但裁決不靠 re-rate——在 19x 上 EPS 自身複利即 carry return，倍數維持平至微降亦達標，re-rate 到 25-30x 是選擇權非論點"}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"有機成長結構性減速：headline cRPO 21.5% 中 ~125bps 為 Armis 無機（MS 拆分），有機 ~17%；UBS 預測 EOY26 降至 16%；estimate-cut treadmill 使「便宜」因 E 還在被下修"},{"id":"R2","text":"agentic-workflow 新預算之爭（非古典 ITSM 座位）：Salesforce Agentforce（Benioff 稱其 IT 版為「ServiceNow killer」）/ Microsoft Copilot・Agent 365 / AI-native（Sierra $15.8B、Decagon $4.5B）競逐 NOW 尚未捕獲的增量 agentic 預算；CRM/ITSM/ERP 邊界溶解"},{"id":"R3","text":"三條獨立慢變數：(a) agentic 架構性繞過工作流層（⛔ 級，§3.F）；(b) 座位重定價在 2027-28 續約潮向下侵蝕 NRR（renewal 為滯後）；(c) 聯邦/公部門 15-17% 營收＋DOGE 2026 剪支＋兩次政府停擺（1/31-2/3、2/14-4/30）——惟 Q2 聯邦反而強（部分為 on-prem 時點前移）"}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"加碼＝站回 W104($164) 或有機 cRPO cc ≥18% 連 2 季；減碼＝有機 cRPO <16%（UBS 路徑）連 2 季或 AI ACV 淨增轉負","irr_base_pct":11.2,"ev5y_pct":70.5,"drift_watch_prior":{"dca_verdict":"進場","dca_role":"核心","signal":"B","val":"🟢","ma":"❌","trap":"🟡","moat_trend":"→","runway_post_y5":"🟢","asym_ratio":5.7,"ev5y_pct":70.5,"irr_base_pct":11.2,"max_dd_pct":-40.0,"bull_5y_price":265.0,"bear_5y_price":68.0,"p_bull_pct":28.0,"p_bear_pct":30.0,"rearm_trigger":"加碼＝站回 W104($164) 或有機 cRPO cc ≥18% 連 2 季；減碼＝有機 cRPO <16%（UBS 路徑）連 2 季或 AI ACV 淨增轉負","price_at_dd":95.46,"archetype":"品質複利成長","cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"NOW","date":"2026-11-02","schema":"v15.0","contract":"v19","company_name":"ServiceNow, Inc."},"oneliner":"ServiceNow 向大企業收工作流平台訂閱費，續約率 98%，AI 合約價值目標一年內兩度上調；現價約 21.8 倍明年共識 EPS，估值合理但不便宜，成敗看 2027 年 1 月的財測能否守住 18% 訂閱成長。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/NOW_20261102/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/NOW_20261102/scenario.json","answers":{"q1_business":{"verdict":"賺大型企業 IT、資安與員工服務流程的訂閱錢，訂閱占營收 97%；錢卡在企業工作流的系統記錄層，AI 代理要在企業裡動手做事，多半得經過這一層。","reasoning":"2026 年第三季總營收 41.06 億美元，其中訂閱 39.88 億美元，占 97%。非 GAAP 營業利益 13.38 億美元（約 32.6%），GAAP 營業利益 3.85 億美元（約 9.4%），兩者的差距主要是股票薪酬 6.33 億美元；非 GAAP 訂閱毛利率 80%。收費方式是多年期訂閱，部分 AI 與資料方案在超出點數後按用量計價。RPO 297 億美元、cRPO 136.5 億美元，續約率 98%，年 ACV 逾 500 萬美元的客戶有 680 家。公司沒有揭露超過營收 10% 的產品分部。單點依賴落在客戶端：一家美國聯邦通路夥伴兼系統整合商占 2026 上半年營收 13%（2025 年為 11%），直銷占營收 78%。產業時鐘在擴張期，依據是企業應用軟體支出 2026 年年增 13.9%，2030 年估 8,126 億美元（Gartner，經第三方轉述）。產業態勢分三面看：競爭面，Salesforce 與微軟以 AI 代理切入 IT 服務管理，屬惡化；結構面，企業 AI 從試驗走到上線，需要治理與執行層，屬轉好，公司 AI ACV 年底目標已兩度上調到 17 億美元；其他面，座位制轉用量計價與企業自建都在變動。綜合裁決為雙向拉鋸。","fact_refs":["f_kpi0_total_revenues_gaap","f_kpi1_subscription_revenues_ga","f_kpi2_non_gaap_operating_incom","f_kpi3_gaap_operating_income_ma","f_kpi4_free_cash_flow_non_gaap","f_kpi5_sbc","f_kpi8_crpo","f_kpi9_rpo","f_kpi10_customers_5m_acv","f_kpi11_subscription_gross_margi","f_earnings_recency"],"verdict_values":{"revenue_quality":"高。訂閱占營收 97%，多為多年期合約，續約率 98%；RPO 297 億美元，約為今年共識營收的 1.8 倍。瑕疵有兩項：一是部分大單把導入服務的價值從訂閱移到專業服務（第三季約 25bp、第四季約 50bp）；二是聯邦地端交易讓季度數字起伏。","unit_econ_note":"非 GAAP 訂閱毛利率 80%（全年財測 81%），非 GAAP 營益率 32.5%。扣掉占營收 15.4% 的股票薪酬後，GAAP 營益率只有約 9.4%。第三季自由現金流 8.22 億美元，屬季節性偏低，全年財測利潤率 36%。","archetype":{"primary":"品質複利成長","secondary":null,"confidence":"中","fingerprint":"訂閱占營收 97%、續約率 98%、訂閱成長約 20%（固定匯率）、全年非 GAAP 營益率 31.5%、自由現金流利潤率 36%、股票薪酬占營收約 15%"},"industry":{"clock_phase":"II","sd_verdict_source":"需求屬結構性持久。企業 AI 從試驗走向上線，治理與流程執行是必要支出，RPO 年增 22.5% 且合約年期在拉長（CFO 2026-10-28）。不過定價模式正由座位轉向用量，利潤怎麼分配還在變動；彭博行業研究估計應用軟體利潤率可能因此壓縮 100–900bp。","bargaining":{"up":"上游是超大型雲端與模型商。公司轉向超大型雲端，短期壓低了毛利率（CFO 2026-05-04、2026-07-22）；管理層稱模型已商品化、可以改用較便宜的模型（Zavery 2026-07-22）。上游議價力判為中等。","down":"下游是大型企業與政府。年 ACV 逾 500 萬美元的客戶 680 家，續約率 98%；單一聯邦通路夥伴占營收 13%，但這家夥伴背後是多個聯邦機關。","geo":"中東衝突曾讓 2026 年第一季的大型地端交易延後；公司與 Aramco Digital 簽有橫跨 50 多國的協議；出口管制與關稅屬制式風險揭露。"},"profit_pool_dir":"利潤池正往 AI 模型與算力層移動，公司想當代理的受治理執行層來接住這部分。目前的證據是外部代理經 Action Fabric 呼叫公司平台時仍按次計費，但利潤池往哪邊走尚未定案。","tam_table":[{"item":"企業應用軟體支出 2026 年","value":"4,963 億美元，年增 13.9%（美元）、12.7%（固定匯率）；Gartner 2026 第三季預測，經第三方部落格轉述"},{"item":"企業應用軟體支出 2030 年","value":"8,126 億美元；2026–2030 年隱含年複合成長約 13.1%（8,126÷4,963 開四次方）"},{"item":"公司滲透率（營收÷支出）","value":"2026 年約 3.3%（今年共識營收 162.3 億÷4,963 億）；若 2030 年達到公司訂閱目標 300–320 億美元，約 3.7–3.9%"},{"item":"SAM 與分段成長率","value":"事實表未涵蓋（IT 服務管理、資安、CRM 各段的市場規模都未收錄）"},{"item":"營業利益池占比（5 年前到現在）","value":"事實表未涵蓋，無法判斷利益池是否淨流出 5 個百分點以上"},{"item":"預測下修訊號","value":"Gartner 把 2027 年總額較上一季預測下修 25 億美元，相對 4,963 億美元的規模不到 1%"}]}}},"q2_moat":{"verdict":"護城河持平。工作流系統記錄層的轉換成本還在：續約率 98%、合約年期拉長、大客戶數持續增加，AI 新方案漲價 20–30% 也抵銷了座位壓力。但 GAAP 毛利率下滑，加上 Salesforce 與微軟以捆綁方式進攻，定價權沒有擴大。","reasoning":"機制：CMDB、工作流資料加上 20 多年的營運脈絡，讓客戶把 IT、資安、HR 流程跑在同一個平台上；第三季前 20 大交易中有 19 筆包含 6 項以上產品，要換供應商就得搬資料、重建流程並重新訓練員工。方向的證據：同業 ROIC 事實表未涵蓋，改看留存與價格兩條軸。續約率在 2026 年第二、三季都是 98%；年 ACV 逾 500 萬美元的客戶由第二季 658 家增到第三季 680 家；AI 原生方案平均漲價 20–30%（CFO 2026-05-04、2026-07-22）。反向證據：TTM GAAP 毛利率 73.08%，低於 2025 年的 77.53%；GAAP 營益率 9.68%，在同業中只高於 DDOG（CRM 21.52%、MSFT 47.1%、PLTR 42.8%）；第三季起公司為大單附上導入服務，這是讓利，不是漲價。評分：執行力 9 分，第二、三季的營收、cRPO、營益率全數超過財測上緣，做完三筆收購後人數不增反減；定價權 7 分，漲價成立，但成本端被雲端與推論分走一部分。扣掉一項生態攻擊後評為 B。報酬持續期：投入資本事實表未涵蓋，當期 ROIC 無法計算。四個檢查點兩綠兩黃，黃燈在決策層級（AI 導入代理讓搬遷時間縮短）與價值鏈分配（前端模型商與雲端拿走一部分）。","fact_refs":["f_peer_now_gross_margin_pct","f_peer_now_operating_margin_pct","f_peer_now_fcf_margin_pct","f_peer_crm_operating_margin_pct","f_peer_msft_operating_margin_pct","f_peer_pltr_operating_margin_pct","f_peer_ddog_operating_margin_pct","f_kpi9_rpo","f_kpi10_customers_5m_acv","f_kpi11_subscription_gross_margi"],"verdict_values":{"moat":{"mechanism":"工作流系統記錄層的轉換成本（CMDB、工作流資料、代理治理），再加上多產品綁定","execution":9,"pricing":7,"grade":"B","trend":"→","trend_evidence":"執行力在擴大：連續超過財測，吸收併購稀釋後營益率仍擴張 50bp。定價權穩定偏弱：AI 方案漲價 20–30%，但毛利率下滑，又以導入服務讓利。兩者合計判持平。","competitor_notes":[{"name":"CRM","strategy_note":"以 Agentforce 推 IT 服務管理，正面切入公司本業，還能和既有 CRM 捆綁銷售；GAAP 營益率 21.52%，高於公司，打價格戰的承受力較強。公司則反向用 Sweep 把 CRM 導入縮短到 30–60 天，去搶對方客戶。"},{"name":"MSFT","strategy_note":"把 Copilot 與代理平台捆綁進既有企業授權，是最大的捆綁威脅；但同時也是合作方，公司的 Control Tower 可以通知 Azure AI Foundry 切斷代理權限。"},{"name":"PLTR","strategy_note":"爭奪企業 AI 營運層的預算，營益率 42.8%、自由現金流利潤率 54.55%，都遠高於公司；和公司流程系統記錄層的重疊有限，屬預算競爭，不是直接替換。"},{"name":"DDOG","strategy_note":"可觀測性領域與公司的 ITOM、AIOps 重疊；研發密度 43.69%、營益率 0.43%，仍在投入期，對公司屬點對點競爭。"}],"peer_na_reason":"同業 ROIC 與投入資本事實表未涵蓋，只有毛利率、營益率、自由現金流利潤率與研發密度","threats":[{"level":"🔴","text":"生態攻擊：Salesforce 推出 Agentforce IT 服務管理，切入公司本業；微軟以 Copilot 與代理平台捆綁銷售。10-K 自述，系統記錄廠商可能阻擋整合，或以捆綁降價施壓。公司在投資人日稱競爭名單裡看不到這些對手（2026-05-04），但沒有提供贏率數字；第三季前 20 大交易中，IT 服務管理仍占 11 筆。","p":30,"evidence_refs":["competitive_share_entrants#1","competitive_share_entrants#2"]},{"level":"🟡","text":"點對點替代：AI 原生的點解決方案，以及企業用 AI 寫程式工具自建流程；10-K 自述公司正與替代做法競爭。本次沒有列為架構替代，理由是外部代理（ChatGPT、Gemini）經 Action Fabric 呼叫時，工作仍在公司平台內執行並按次計費，附著點長在公司的 CMDB 與工作流上。升級條件：若 Action Fabric 用量停止揭露，或訂閱毛利率連 2 季低於 78%，就升為架構替代並重評論點。","p":30,"evidence_refs":["substitute_technology#0","substitute_technology#2","substitute_technology#3"]},{"level":"🟡","text":"定價模式轉換：座位制改為用量或成果計價。彭博行業研究估計應用軟體利潤率可能壓縮 100–900bp；CFO 稱客戶完全沒有要求成果計價（2026-10-28），但一半新增 ACV 已經不是座位計價。這項風險已反映在定價權評分，不另扣分。","p":40,"evidence_refs":["supply_demand_durability#2"]}],"roic_durability":{"quadrant":"推定為高利益率×高周轉：非 GAAP 營益率約 32%，訂閱預收款讓營運資金為負。投入資本事實表未涵蓋；計入併購商譽後，周轉率會下降。","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者（員工與 IT 人員）、決策者（CIO、CEO）、付款者（企業預算）三方一致。IT 服務、資安與 AI 代理治理是營運必要支出，延後購買的代價是停機與資安事件。代理變數：續約率 98%、RPO 年增 22.5%。"},{"item":"決策層級","level":"🟡","text":"替代與否在企業平台層決定。搬遷要移走 CMDB、重建流程、重新訓練員工，合約年期也拉長到 5 年（Experian、Maybank，2026-07-22）。但 AI 導入代理讓搬遷變快：公司自稱用 Sweep 把 CRM 導入縮短到 30–60 天，同樣的工具對手也能拿來搬走公司的客戶。"},{"item":"價值鏈分配","level":"🟡","text":"價值鏈上游是模型商與超大型雲端，前端是 ChatGPT、Gemini 等介面。公司以 Action Fabric 讓外部代理在平台內執行並按次計費，目前拿得到錢；但 TTM GAAP 毛利率由 77.53% 降到 73.08%，顯示成本端分走了一部分。CFO 稱 AI 推論成本不到服務成本的 10%（2026-05-04）。"},{"item":"社會容忍度","level":"🟢","text":"屬企業對企業軟體，沒有監管授權形成的價格上限。敏感點在政府採購：DOJ 正在調查政府合約合規問題，單一聯邦通路夥伴占營收 13%；這屬於事件風險，不構成定價天花板。"}],"roiic":"事實表未涵蓋投入資本與收購後營業利益，無法計算增量 ROIC","reinvest_rate":"2026 年被併購墊高：Armis 約 77.5 億美元現金對價，已超過第三季非 GAAP 營業利益的年化值約 53.5 億美元（13.38 億×4，未稅）。資本支出、折舊與營運資金變動事實表未涵蓋。","endo_ceiling":20,"formula_note":"內生成長率＝增量 ROIC×再投資率，兩項數字都缺，改以有機訂閱成長作為上界代理。2026 年全年訂閱成長約 21%（固定匯率），扣除 Armis 提前併入的約 1.25 個百分點後約 19.75%，取整為 20%。"}}}},"q3_growth":{"verdict":"五年後的成長空間仍寬：公司營收只占 2026 年企業應用軟體支出約 3.3%，AI、資安、CRM 三條第二曲線都已有營收規模。但共識 EPS 年增約 22%，比有機營收成長多出約 2 個百分點，這段要靠利潤率擴張來補。","reasoning":"成長來源以量為主、價為輔，併購約貢獻 1.25 個百分點。跑道：公司營收約占 2026 年企業應用軟體支出的 3.3%，而這塊支出 2026–2030 年本身約年增 13%；以目前約 20% 的成長速度，要幾十年才會碰到 30% 滲透率，跑道在 10 年以上。第二條 S 曲線有來源可證：AI ACV 年底目標由 10 億、15 億一路上調到 17 億美元，第三季淨增 65%；資產管理 ACV 突破 10 億美元；CEO 稱已有 6 個事業的年化營收超過 10 億美元。AI 是否真的是淨增量：AI ACV 只計增量（CFO 2026-05-04），但被蠶食的座位收入沒有揭露。投資人日有分析師指出，2030 年 AI 占 ACV 30% 隱含非 AI 部分年增不到 10%，CFO 沒有給數字。所以淨增量只能用總訂閱成長來驗證，分界年是 2027 年（Armis 滿一年後）。附著點：外部代理經 Action Fabric 在公司資產上執行並計費，屬於強化，分界年是 2028 年（座位續約潮）。十年延伸：基礎情境第 6–10 年 EPS 年增 10%，多頭 15%。十項衰退信號亮兩項（GAAP 毛利率下滑、自身倍數下移），長期成長性評為中等。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_kpi1_subscription_revenues_ga","f_kpi8_crpo","f_peer_now_gross_margin_pct","f_pe_percentile"],"verdict_values":{"growth":{"driver_mix":"量為主：既有大客戶的多產品擴張（前 20 大交易有 19 筆含 6 項以上產品）與 AI 新方案。價次之：AI 原生方案平均漲價 20–30%。併購約 1.25 個百分點（Armis）。回購只抵銷稀釋，不貢獻每股成長。","runway_years":"≥10","runway_post_y5":"🟢","endo_ceiling_basis":"沿用護城河段的內生上界 20%（以有機訂閱成長為代理，增量 ROIC 無法計算）。共識 EPS 2026→2028 年年複合約 22.1%（5.92÷3.97 開根號）；三年期算法需要 2025 年非 GAAP 實際值，事實表未涵蓋。缺口約 2.1 個百分點，歸因於利潤率擴張：CFO 承諾 2027 年非 GAAP 營益率擴張 100bp（2026-05-04），淨回購為零（稀釋中性）。共識營收 2026→2027 年約年增 18.7%（192.68÷162.34）。","segments":{"expanded":false,"reason":"公司只分訂閱與專業服務兩類，訂閱占第三季營收 97%。產品線（IT、資安、CRM、AI）的營收拆分事實表未涵蓋，只有 ACV 與交易數，無法做分部三年成長。利潤由訂閱毛利決定，不取決於產品組合。"},"decay_signals":[{"signal":"毛利率連 2 季年減","lit":true,"evidence":"TTM GAAP 毛利率 73.08%，低於 2025 年的 77.53%；第三季非 GAAP 訂閱毛利率 80%，低於全年財測 81%；CFO 在 2026-07-22 承認轉向超大型雲端與 AI 用量帶來短期壓力"},{"signal":"核心市占近 12 個月縮減","lit":false,"evidence":"沒有來源可證份額流失；IT 服務管理仍出現在前 20 大交易中的 11 筆；競爭者份額數字事實表未涵蓋"},{"signal":"主力產品提價後銷量下滑","lit":false,"evidence":"AI 原生方案漲價 20–30%，CEO 稱活躍使用者沒有下降（2026-05-04），續約率 98%"},{"signal":"EPS 成長率比營收成長率高 5 個百分點以上","lit":false,"evidence":"共識 EPS 2026→2028 年約年增 22.1%，營收 2026→2027 年約年增 18.7%，差距約 3.4 個百分點"},{"signal":"自由現金流÷淨利低於 0.75 連 2 年","lit":false,"evidence":"2025 年自由現金流 45.33 億美元÷淨利 17.48 億美元，約 2.6 倍，由股票薪酬與預收款墊高"},{"signal":"股票薪酬占營收超過 5% 且逐年上升","lit":false,"evidence":"第三季占營收 15.4%，遠高於 5%；但逐年趨勢事實表未涵蓋，公司目標是 2029 年降到 10% 以下。暫不計為亮燈，列入監測"},{"signal":"TAM 萎縮或被替代技術壓縮","lit":false,"evidence":"企業應用軟體支出 2026 年年增 13.9%；替代技術壓縮市場的說法只有評論，沒有數字"},{"signal":"產業估值倍數近 3 年系統性下移","lit":true,"evidence":"公司本益比、股價營收比、EV/S 都落在四個年度端點中的最低點；市場以「SaaS 末日」形容整個類股。產業整體倍數事實表未涵蓋"},{"signal":"維持性資本支出占自由現金流超過 60%","lit":false,"evidence":"CFO 稱資本支出下降，自由現金流利潤率上調到 36%"},{"signal":"停止投資新產能且營收 3 年內下滑","lit":false,"evidence":"營收 2023–2025 年每年成長 20% 以上"}],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"資本配置中等。回購只夠抵銷股票薪酬帶來的稀釋，2026 年靠舉債完成大型收購，報酬尚未驗證；自由現金流轉換能力強。","reasoning":"自由現金流÷淨利：2025 年約 2.6 倍（45.33÷17.48 億美元）。轉換能力強，但主因是股票薪酬與預收款，不是利潤本身。股票薪酬第三季 6.33 億美元，占營收 15.4%；CFO 承諾 2029 年降到 10% 以下（2026-05-04）。現金去向只能列出 2026 年已知部分，三年四分法事實表未涵蓋：收購 Armis 約 77.5 億美元現金，另有 Veza（金額未知），2025 年底收購 Moveworks 約 28.5 億美元；2026 年第一季 20 億美元加速回購，尚餘 42 億美元授權；股息沒有資料；淨負債 38.08 億美元，含 40 億美元定期貸款與租賃負債。CEO 稱長期目標不含大型併購（2026-05-04），CFO 同日也把開拓新 TAM 的小型收購列為資本配置第二順位；Armis 已屬大型收購，之後若再做單筆逾 50 億美元的收購，就與這套說法衝突。營運槓桿：全年營益率財測 31.5%，較去年擴張 50bp，吸收併購稀釋後仍在擴張。","fact_refs":["f_kpi5_sbc","f_kpi0_total_revenues_gaap","f_kpi4_free_cash_flow_non_gaap","f_net_debt_m","f_shares_diluted_m","f_fwd_pe_latest"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":true,"passed":null,"input":"12 個月內完成 Moveworks（約 28.5 億美元）、Veza、Armis（約 77.5 億美元現金，其中 40 億美元為定期貸款）三筆收購；收購後的營收與利潤貢獻事實表未涵蓋，Armis 到 2026-04-20 才完成，已實現報酬還無法計算"},{"name":"buyback_yield","applicable":true,"passed":false,"input":"2026 年第一季 20 億美元加速回購，尚餘 42 億美元授權；回購均價事實表未涵蓋。以現價推算，今年共識 EPS 收益率約 3.8%（1÷26.48），自由現金流收益率約 5.4%（36%×162.3 億÷1,091 億市值）；十年期公債殖利率只要高於 3.4%，就達不到「殖利率加 2 個百分點」的門檻。回購主要是在抵銷股票薪酬"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"CFO 在 2026-05-04 稱 2026 年淨稀釋為中性；全年 GAAP 稀釋加權股數財測 10.4 億股，第四季 10.5 億股。代價是第三季股票薪酬 6.33 億美元、占營收 15.4%，要靠現金回購抵銷"}]},"governance":{"capital_returns":[{"item":"收購現金","value":"Armis 約 77.5 億美元（2026-04-20 完成，部分以 40 億美元定期貸款支應）；Moveworks 約 28.5 億美元（2025-12-15 完成）；Veza（2026-03-02 完成，金額事實表未涵蓋）"},{"item":"回購","value":"2026 年第一季 20 億美元加速回購，剩餘授權 42 億美元；目標 2026 年稀釋中性"},{"item":"股票薪酬","value":"第三季 6.33 億美元，占營收 15.4%；公司目標 2029 年降到 10% 以下"},{"item":"淨負債","value":"38.08 億美元（總債務 84.15 億美元、現金 46.07 億美元，含租賃負債）"},{"item":"股息","value":"事實表未涵蓋，未見股息資料"}]}}},"q5_valuation":{"verdict":"現價要求未來五年 EPS 年增約 15% 以上，而且倍數不再大幅下降。今年共識 26.5 倍、明年 21.8 倍，PEG 約 1.2。我相信基礎情境的 EPS 複利，但共識還在下修，所以估值判為合理、不便宜。","reasoning":"現價 105.12 美元。今年（FY2026）共識 non-GAAP EPS 3.97，對應 26.5 倍；明年 4.83，對應 21.8 倍。GAAP 本益比 75.6 倍，差距來自股票薪酬。反推市場要求：若要五年拿到 10% 年報酬，且五年後市場給 21 倍，2031 年 EPS 需要約 8.06，年增約 15.2%（105.12×1.1 的 5 次方÷21）。基礎情境是 8.85，年增約 17.4%。我相信這個量級：前兩年有 RPO 297 億美元與 98% 續約率撐住，後面靠利潤率承諾。我不相信的是倍數會回到前幾年的水準：公司三種倍數雖然都在四個年度端點中的最低點，但整個產業正在降評，這不能當成便宜的理由。賣方方面，2026-08 聚合站的平均目標價約 140 美元，區間 72–248 美元（未驗證），高低差 3.4 倍，本次不採用賣方目標價。上檔推算：短期一年，2027 年基礎 EPS 4.75×25 倍約 118.75 美元，約 +13.0%；中期兩年，2028 年 5.70×23 倍約 131.1 美元，約 +24.7%（倍數由 26.5 倍線性降向終端的 21 倍）。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_pe_current","f_pe_percentile","f_ps_percentile","f_ev_s_percentile","f_ev_s_fwd","f_ev_m","f_rev_consensus_fy1_m","f_consensus_rev_fy1_pct","f_consensus_rev_fy2_pct","f_consensus_rev_fy3_pct"],"verdict_values":{"valuation":{"basis":"以 FY2026E 與 FY2027E 共識 non-GAAP EPS 計算的前瞻本益比搭配 PEG 為主尺，扣除股票薪酬後的自由現金流收益率作交叉檢查","tier":"大型企業軟體平台（訂閱成長約 20%）","peers":{"expanded":false,"reason":"事實表的同業表只有利潤率，沒有同業前瞻本益比，無法做倍數對照；改用公司自身的四個年度端點與 PEG"},"fwd_pe":26.48,"peg":1.2,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"今年共識 non-GAAP EPS 3.97，前瞻 26.5 倍；明年 4.83，21.8 倍。FY2026→FY2028 共識 EPS 年複合約 22.1%（5.92÷3.97 開根號），PEG 約 1.2（以明年計約 0.98），落在合理區間。公司本益比、股價營收比、EV/S 都在四個年度端點中的最低點；這不是五年分位，五年分位事實表未涵蓋。扣除股票薪酬後的自由現金流收益率約 3%：36%×162.3 億−6.33 億×4，約 33 億美元，再除以 1,091 億美元市值。結論：合理，不便宜。","upside_short_pct":13.0,"upside_mid_pct":24.7,"denominator_disputed":false,"denominator_note":"判斷便宜與否用的是 non-GAAP EPS，沒有扣除股票薪酬（占營收約 15%）。股票薪酬是經常性成本，不是一次性項目，所以不改用前瞻錨定，而是用扣除股票薪酬後約 3% 的自由現金流收益率交叉檢查，結論同樣是合理、不便宜。"}}},"q6_how_wrong":{"verdict":"最可能看錯的地方：AI 代理把座位制改成用量計價後，營收照樣成長，但毛利與定價權被前端模型商與雲端分走。價值陷阱風險中等。","reasoning":"空方最強的數字有三個：TTM GAAP 毛利率 73.08%（2025 年 77.53%）；三年共識 EPS 三個月內分別下修 2.2–3.4%；第四季 cRPO 財測 18.5%，低於第三季的 21%。管理層每季都有一次性說明：第二季是聯邦地端提前認列，第三季是提前續約（約占 cRPO 超標的一半），第四季是 T4C 條款約 50bp 加上導入服務。對這類一次性歸因，不採信也不否定，標為「未證、監測」，並事先登記驗證條件：2027 年第一、二季 cRPO 固定匯率成長若都沒有回到 19% 以上，就認定這套說明不成立。訴訟與監管：DOJ 政府合約調查的金額與時點都未揭露；原告律所在 2026-10 發出投資人調查通告，但還沒有正式提起訴訟。動能：RSI 26.86，股價低於 W52、W104、W250，屬超賣，不是過熱。歷史最大回撤數字事實表未涵蓋，回撤區間由空頭路徑推得。","fact_refs":["f_peer_now_gross_margin_pct","f_consensus_rev_fy1_pct","f_consensus_rev_fy2_pct","f_consensus_rev_fy3_pct","f_kpi8_crpo","f_rsi14","f_ma_state","f_ma_w52","f_ma_w104","f_ma_w250","f_kpi5_sbc"],"verdict_values":{"trap":{"verdict":"🟡","label":"中等：十項衰退信號亮兩項（GAAP 毛利率下滑、自身倍數下移），股票薪酬偏高列入監測"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":3.97,"pe":26.48,"basis":"FY2026E 共識 non-GAAP 稀釋 EPS（Koyfin 2026-10-31）；判斷日距年度結束只剩一季，與終端 FY2031E 同為當年度口徑"},"eps":{"bull":[4.95,6.15,7.5,9.0,10.7],"base":[4.75,5.7,6.7,7.75,8.85],"bear":[4.35,4.5,4.62,4.72,4.8]},"pe":{"bull":26,"base":21,"bear":15},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0,"net_buyback":0},"second_stage":{"bull_cagr_pct":15,"base_cagr_pct":10},"max_dd":{"lo":-45,"hi":-30,"basis":"上緣 −30%：空頭終端 4.80×15 倍＝72 美元，約 −31.5%，取整。下緣 −45%：空頭 EPS 改配 12 倍（比空頭終端倍數再低 20%，模擬情緒超跌），約 57.6 美元，約 −45%。2026 年第一季財報後單日跌約 17.8%，顯示單一財報日就可能跌掉近兩成。","trigger_time":null},"basis":{"bull":"AI 用量計價在 2027 年帶動訂閱成長回升到 22% 以上（管理層稱 2027 年才會真正加速），營益率每年擴張超過 100bp；終端 26 倍，仍略低於現值 26.5 倍","base":"訂閱成長由約 20% 緩降到 2031 年約 14%，營益率照承諾擴張，EPS 比共識低約 2–4%，反映下修循環；終端 21 倍，對應五年後約 14% 成長配 PEG 1.5。同業前瞻倍數事實表未涵蓋，改以自身現值 26.5 倍、以及成長降到 15% 情境下約 22 倍作對照","bear":"2027–28 年續約潮出現座位縮減，代理繞過與用量計價把利潤率壓縮約 300bp（彭博行業研究估 100–900bp），2028 年後成長掉到 5% 以下，EPS 近乎持平；終端 15 倍，低於成長降到 10% 情境的 17 倍"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"2026-05-04 投資人日，CFO 設定 2030 年 AI 占 ACV 30% 的目標；分析師追問這是否隱含非 AI 部分年增不到 10%，CFO 只說這樣想是錯的，沒有給數字。二手評論指出，AI 寫程式工具讓企業能自建流程，代理取代人力也會減少座位。本季訂閱成長連續三季停在 20.5–21%（固定匯率），AI 加速沒有帶動總成長。","assumption":"AI 增量足以抵銷既有產品的放緩，總訂閱成長守在 18% 以上","consequence":"五年後虧損 50% 最可能的劇本：2027–28 年續約潮出現座位縮減，前端模型商拿走使用者介面，公司淪為按次計費的後端；成長掉到個位數，利潤率被用量計價壓縮，倍數落到 12–15 倍（空頭路徑 4.80×12 倍約 58 美元）","ruling":"部分採納。空頭機率維持 30%，但不放進基礎情境，因為續約率 98%、RPO 年增 22.5% 且合約年期拉長，未來一年內看不到需求流失。不過非 AI 部分的成長數字至今沒有揭露，這是論點最大的缺口。此劇本與 Single Thing 部分重疊：2027 年財測就是它的第一個驗證數字。","watch":"2027 年訂閱營收財測、Armis 滿一年後的 cRPO 固定匯率成長、續約率","evidence_refs":["substitute_technology#0","substitute_technology#2","substitute_technology#3"],"fact_refs":["f_kpi1_subscription_revenues_ga","f_kpi9_rpo","f_kpi8_crpo"]},{"view":"論點失敗","evidence":"單一聯邦通路夥伴占 2026 上半年營收 13%（2025 年 11%）。DOJ 針對政府合約合規問題（前陸軍資訊長聘用案）展開調查，公司已通報陸軍停權除名辦公室，並表示無法預測結果。","assumption":"聯邦業務不受調查影響；CFO 稱第四季聯邦淨新增 ACV 還會再加速（2026-10-28）","consequence":"若公司遭停權，經這家夥伴的 13% 營收與其他聯邦合約都會受威脅，營收與 EPS 可能一次下移一成以上","ruling":"反駁，判為低機率事件，12–24 個月內約 5%。10-K 稱訴訟合計不會造成重大不利影響，與這家通路夥伴之間也沒有收款異常。但這屬事件風險，不能用機率平均掉，因此另設清倉條件。","watch":"10-Q 與 8-K 中的調查進度、該夥伴的營收與應收帳款占比","evidence_refs":["regulatory_antitrust#0","major_events#3","customer_concentration_credit#2"],"fact_refs":[]},{"view":"論點成功但股東經濟變差","evidence":"第三季股票薪酬 6.33 億美元，占營收 15.4%。12 個月內完成三筆收購，Armis 77.5 億美元現金對價中有 40 億美元靠定期貸款，淨負債 38 億美元。TTM GAAP 毛利率 73.08%（2025 年 77.53%）。第三季起為大單免費附上導入服務，把部分價值從訂閱移到專業服務。自由現金流扣除股票薪酬後，只剩營收的約 15–21%。","assumption":"利潤率照承諾每年擴張 100bp，股票薪酬在 2029 年降到營收 10% 以下，之後不再做大型收購","consequence":"AI 成功了，但錢流向股票薪酬、利息與收購溢價，每股盈餘年增落在 15% 以下，基礎情境的 IRR 掉到個位數","ruling":"採納為監測項。目前利潤率承諾有在兌現：全年營益率財測維持 31.5%，自由現金流利潤率上調到 36%，人數略降。但併購報酬還沒驗證；若再宣布逾 50 億美元的收購，就下修資本配置結論。","watch":"2027 年營益率財測、股票薪酬占營收比、收購公告","evidence_refs":["ma_merger#1"],"fact_refs":["f_kpi5_sbc","f_net_debt_m","f_peer_now_gross_margin_pct","f_peer_now_fcf_margin_pct"]},{"view":"價格已反映太多","evidence":"股價由前份的 95.46 美元升到 105.12 美元（+10.1%），同期明年共識 EPS 由 5.0 降到 4.83（−3.4%），前瞻倍數上升約 14%。2026 年春季 Goldman、BTIG、Citi 都下修了目標價；賣方目標價區間 72–248 美元，高低差 3.4 倍。","assumption":"基礎情境 EPS 已放在共識下方（2027 年 4.75、2028 年 5.70），終端 21 倍也低於現值 26.5 倍","consequence":"共識若再下修 5%，今年口徑的倍數會由 26.5 倍變成約 28 倍，估值由合理轉為偏貴，上檔空間被吃掉","ruling":"大致反駁。基礎情境不需要倍數回升，報酬來自 EPS 複利。但在共識連續下修期間，空頭錨會跟著往下移，所以報酬不對稱比不作為加碼依據。","watch":"FY2027 共識 EPS 是否跌破 4.60","evidence_refs":["capital_markets_pricing#3","capital_markets_pricing#4"],"fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_consensus_rev_fy2_pct","f_consensus_eps_fy2"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ❌ → 本次 ❌","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=❌","side_b":"本次 ma=❌","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 95.46 → 本次 105.12（+10.1%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=95.46","side_b":"本次 price_at_dd=105.12","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]角色由 dd_decision.py 機械路由：前份 核心 → 本次 衛星","cause":"價格變動","prior_field":["dca_role"],"side_a":"前份 dca_role=核心","side_b":"本次 dca_role=衛星","ruling":"角色是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。沒有單一輸入能還原，屬多欄共同：估值 🟢→🟡。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 95.46 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 95.46 美元：Bull 價 265、Bear 價 68，五年期望值 +70.5%，基準年化 11.2%，不對稱比 5.7","side_b":"本次情境、股價仍用 95.46 美元：Bull 價 278.2、Bear 價 72，五年期望值 +83.1%，基準年化 14.3%，不對稱比 6.49","ruling":"先換情境、股價不動：五年期望值多 12.6 個百分點，基準年化多 3.1 個百分點。不對稱比由 5.7 變為 6.49。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變好。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 95.46 美元：五年期望值 +83.1%，基準年化 14.3%，不對稱比 6.49","side_b":"本次情境、股價 105.12 美元：五年期望值 +66.3%，基準年化 12.1%，不對稱比 4.35","ruling":"再換股價、情境不動：起點價上漲 10.1%，五年期望值少 16.8 個百分點，基準年化少 2.2 個百分點，不對稱比由 6.49 降到 4.35。合計五年期望值比前份少 4.2 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"估值結論由偏便宜轉為合理","cause":"價格變動","prior_field":["val"],"side_a":"前份（2026-07-23）：股價 95.46 美元、明年共識 EPS 5.0，約 19 倍，判為偏便宜","side_b":"本次：股價 105.12 美元（+10.1%）、明年共識 EPS 4.83（−3.4%），約 21.8 倍；今年口徑 26.5 倍、PEG 約 1.2，判為合理","ruling":"估值結論降一級。倍數上升約 14%，其中約四分之三來自股價上漲，約四分之一來自共識下修。進場結論與部位角色依本次輸入重新推出。","evidence_level":"事實表數字","settle_metric":"明年共識 EPS 與股價","if_then":["若股價回到 95 美元以下，且明年共識 EPS 守在 4.60 以上→估值回到偏便宜，分批加碼","若明年共識 EPS 跌破 4.60 而股價沒跌→估值轉貴，停止加碼"],"evidence_refs":[]},{"axis":"基本面欄位經本季證據檢驗後維持","cause":"新證據","prior_field":["signal","trap","moat_trend","runway_post_y5","archetype","cycle_position"],"side_a":"前份：綜合訊號 B、價值陷阱 🟡、護城河方向持平、五年後成長空間 🟢、屬品質複利成長、景氣位置不適用","side_b":"本次維持同值：綜合訊號 B；價值陷阱 🟡（亮兩項：GAAP 毛利率下滑、自身倍數下移）；護城河持平（續約率 98%、AI 漲價抵銷座位壓力，但毛利率下滑抵消了擴大的可能）；成長空間 🟢（只占企業應用軟體支出約 3.3%）；仍屬品質複利成長；非景氣循環股","ruling":"用新證據檢驗後不改。可能看錯的地方：毛利率若再連 2 季下降，價值陷阱升為 🔴，護城河方向改為下降。","evidence_level":"公司公布數字＋法說","settle_metric":"非 GAAP 訂閱毛利率、續約率","if_then":["若非 GAAP 訂閱毛利率連 2 季低於 78%→護城河方向改為下降並重評論點","若續約率維持 98% 且 AI ACV 達 17 億美元→維持"],"evidence_refs":[]},{"axis":"機率與回撤口徑","cause":"方法變動","prior_field":["max_dd_pct","p_bull_pct","p_bear_pct"],"side_a":"前份：最大回撤填單點 −40%；多頭機率 28%、空頭 30%","side_b":"本次：最大回撤改填區間 −45%～−30%；多頭 25%、基礎 45%、空頭 30%","ruling":"回撤改填區間（寬 15 個百分點），下緣由空頭 EPS 配 12 倍推得。多頭機率降 3 個百分點，反映三個月內共識 EPS 下修 2–3%，以及第四季 cRPO 財測降速。空頭 30% 不變：共識 EPS 成長已超過有機營收上界，空頭機率不得低於 30%。","evidence_level":"情境假設","settle_metric":"2027 年訂閱營收財測","if_then":["若 2027 年財測 ≥18% 且共識止跌→多頭機率回調到 28%","若財測 <18%→空頭機率上調到 40% 以上"],"evidence_refs":[]},{"axis":"加碼與減碼門檻改寫","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"加碼＝站回 W104($164) 或有機 cRPO cc ≥18% 連 2 季；減碼＝有機 cRPO <16%（UBS 路徑）連 2 季或 AI ACV 淨增轉負","side_b":"加碼＝週收站回 W104（現約 158）或 2027 年第二季起 cRPO 固定匯率 ≥18% 連 2 季；減碼＝cRPO 固定匯率 <17.5% 連 2 季或 AI ACV 淨增轉負","ruling":"加碼的價格條件不變，仍是週收站回 W104，只是均線本身由 164 移到約 158。有機 cRPO 改用公司直接公布的 cRPO 固定匯率成長，因為公司沒有揭露有機拆分，前份用的是券商估算。Armis 在 2027 年第二季滿一年之前，公布值含約 1.25 個百分點的無機貢獻，所以加碼只看滿一年後的 18%，與舊門檻相同。減碼門檻 17.5%：滿一年前約等於有機 16.25%，滿一年後就是 17.5%，兩段都比舊的 16% 嚴格。AI ACV 淨增轉負的減碼條件保留。","evidence_level":"方法說明","settle_metric":"cRPO 固定匯率年增","if_then":["若 2027 年第二季起 cRPO 固定匯率 ≥18% 連 2 季→加碼一級","若 cRPO 固定匯率 <17.5% 連 2 季→減碼至半倉"],"evidence_refs":[]},{"axis":"Single Thing 新設","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設唯一致命點（空值）","side_b":"Single Thing：2027 年 1 月第四季財報給出的 2027 年訂閱營收財測，固定匯率成長低於 18%；一旦發生即減碼至半倉","ruling":"前份留空。本次依敏感度挑選營收成長財測：它是 EPS 路徑裡敏感度最大的一項，而且三個月內就會有答案。","evidence_level":"方法說明","settle_metric":"2027 年訂閱營收財測","if_then":["若財測 <18%→減碼至半倉並重跑研究","若財測 ≥18%→補第二批"],"evidence_refs":[]},{"axis":"停損指標新設","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設停損指標（空值），門檻散在加碼、減碼條件裡","side_b":"cRPO 固定匯率 <17.5% 連 2 季→減碼；FY2027 共識 EPS <4.60→停止加碼；續約率 <97% 連 2 季→停止加碼；2027 年訂閱營收財測 <18%→減碼至半倉；非 GAAP 訂閱毛利率 <78% 連 2 季→重評；遭起訴或收到停權通知→減碼，停權確定→清倉","ruling":"本次把停損指標獨立成表，數字都取公司或共識資料直接公布的值，不用推估的有機拆分。","evidence_level":"方法說明","settle_metric":"各指標每季更新","if_then":["任一減碼門檻觸發→減碼至半倉","停權確定→清倉"],"evidence_refs":[]},{"axis":"代理繞過威脅的分級","cause":"新證據","prior_field":null,"side_a":"前份把「代理在架構上繞過工作流層」列為最高級威脅（架構替代）","side_b":"本次降為點對點觀察項：外部代理經 Action Fabric 在公司平台內執行並按次計費，Assist 用量不到 30 天成長 500%（CEO 2026-10-28）；與 OpenAI、Google 的合作也把執行環節留在公司平台","ruling":"附著點的證據目前站在「強化」這一側，但來源全是管理層。設升級條件：訂閱毛利率連 2 季低於 78%，或 Action Fabric 用量停止揭露，就升回最高級並重評論點。","evidence_level":"管理層說法（未經第三方驗證）","settle_metric":"非 GAAP 訂閱毛利率、Action Fabric 用量揭露","if_then":["若訂閱毛利率連 2 季低於 78%→升回架構替代，停止加碼","若 2027 年仍持續揭露代理用量且毛利率守住 80%→維持點對點分級"],"evidence_refs":["substitute_technology#2"]},{"axis":"AI 加速與 cRPO 降速","cause":"新證據","prior_field":null,"side_a":"管理層（2026-10-28 法說，CFO Mastantuono）說明第四季 cRPO 財測 18.5% 的原因：提前續約移到第三季（約占第三季 100bp 超標的一半）、聯邦地端比重上升（約 25bp）、T4C 條款排除約 50bp、導入服務小幅影響。CEO McDermott 稱 2027 年才會看到真正的加速。","side_b":"數字面：AI 淨新增 ACV 年增 65%、AI 消耗量成長 13 倍，但訂閱營收連續三季停在 20.5–21%（固定匯率）；cRPO 成長由第一季約 22.5% 降到第三季 21%，第四季財測 18.5%。第二季（2026-07-22）CFO 也用聯邦地端提前認列解釋超標，一次性說明一再出現。","ruling":"可調和，屬程度差異，不是方向相反。AI ACV 是增量，總成長持平代表 AI 正在補既有產品的放緩，與 H2 一致，但還沒有看到加速。對管理層的會計說明不採信也不否定，標為「未證、監測」。","evidence_level":"公司公布數字＋管理層說法","settle_metric":"2027 年第一、二季 cRPO 固定匯率成長","if_then":["若 2027 年第一、二季 cRPO 固定匯率成長都沒有回到 19% 以上→認定一次性說明不成立，停止加碼","若 Armis 滿一年後 cRPO 固定匯率 ≥18% 連 2 季→加碼一級","反向：若 cRPO 固定匯率 <17.5% 連 2 季→減碼至半倉"],"evidence_refs":[]},{"axis":"管理層承諾與兌現（對照舊逐字稿）","cause":"新證據","prior_field":null,"side_a":"承諾：CFO Mastantuono 在 2026-05-04 投資人日承諾，2027 年非 GAAP 營益率與自由現金流利潤率各擴張 100bp，2029 年股票薪酬占營收降到 10% 以下，2026 年稀釋中性。CEO McDermott 在 2026-05-04 與 2026-07-22 兩度表示年底人數會回到收購前水準。2026 年 AI ACV 目標 15 億美元。","side_b":"兌現：第三季 AI ACV 目標再上調到 17 億美元，全年營益率財測維持 31.5%，自由現金流利潤率財測由 35% 上調到 36%，CEO 稱總人數略降（2026-10-28）。新變數是第三季起為大單附上導入服務，第三季約 25bp、第四季約 50bp 的訂閱營收移到專業服務，會壓到 2027 年的毛利結構。另外，第二、三季的全年訂閱營收都只上調 1,500 萬美元，只傳遞了一半超標。","ruling":"目前言行一致，承諾沒有改口。風險在導入服務會不會變成常態（CFO 稱不會長期做），用 2027 年財測驗證。","evidence_level":"逐字稿原話","settle_metric":"2027 年非 GAAP 營益率財測","if_then":["若 2027 年營益率財測擴張 ≥100bp 且導入服務的影響沒有擴大→維持部位並補第二批","若營益率擴張 <50bp，或導入服務延伸到 2027 年下半年→停止加碼，並上調股東經濟變差情境的空頭機率"],"evidence_refs":[]},{"axis":"公司超標上調與共識下修","cause":"新證據","prior_field":null,"side_a":"公司：第三季營收、cRPO、營益率、自由現金流全數超過財測上緣，並上調全年訂閱營收與自由現金流利潤率","side_b":"賣方：2026-07-30 到 2026-10-31，FY2026、FY2027、FY2028 共識 EPS 分別下修 2.46%、3.4%、2.15%；2026 年春季 Goldman、BTIG、Citi 下修目標價；目標價區間 72–248 美元，高低差 3.4 倍","ruling":"分歧在事實層。下修原因事實表未涵蓋（可能是利息、併購稀釋，或導入服務改變了利潤結構），不能假設賣方是錯的，所以基礎情境 EPS 放在共識下方 2–4%。目標價分歧超過 2.5 倍，降低對報酬不對稱比的信心；共識連續下修期間，不對稱比不作為加碼依據。","evidence_level":"Koyfin 共識快照與賣方報告摘要（各目標價聚合站的數字彼此不一致，未驗證）","settle_metric":"FY2027 共識 EPS","if_then":["若 FY2027 共識 EPS 跌破 4.60→停止加碼","若跌破 4.35→減碼","若第四季財報後共識止跌回升→補第二批"],"evidence_refs":["capital_markets_pricing#3","capital_markets_pricing#4"]},{"axis":"現在就賣的最強論證","cause":"新證據","prior_field":null,"side_a":"賣方論證：同一季全面超標、AI 目標再上調，股價盤後仍下跌（Zukin 在 2026-10-28 法說提問時點出），共識 EPS 三個月連續下修；股價跌破 W52、W104、W250 三條週線均線，W250 的 13 週斜率只剩 0.2%；一次性說明連續三季出現（第二季聯邦地端提前、第三季提前續約、第四季 T4C 與導入服務），全年上調也都只傳遞一半超標","side_b":"持有論證：基礎情境不需要倍數回升（終端 21 倍低於現值 26.5 倍）；續約率 98%，RPO 297 億美元、年增 22.5%；AI ACV 一年內兩度上調，本季淨增 65%；自由現金流利潤率財測上調到 36%","ruling":"持有，第二批等財測再補。賣方最強的一點是一次性說明連續出現，這要用 2027 年第一、二季 cRPO 驗證；以現在的數字，還推不翻論點。","evidence_level":"公司公布數字＋逐字稿","settle_metric":"2027 年訂閱營收財測與 2027 年第一、二季 cRPO","if_then":["若 2027 年財測訂閱營收固定匯率成長 ≥18%，且營益率擴張 ≥100bp→補第二批","若財測 <18%→減碼至半倉","若股價先漲回 W52（約 123 美元）但財測還沒公布→不追","若股價再跌 15%，而續約率與 cRPO 都沒有受損→分批反買"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"續約率與大客戶擴張守住","type":"假設驗證","maps_to":"H1","metric":"季度續約率；年 ACV 逾 500 萬美元客戶數","threshold":"續約率 ≥97%；大客戶數年增 ≥8%（2026 第三季 680 家）","action":"任一項連 2 季未達→停止加碼並重跑研究","source_freq":"公司季報新聞稿與法說，每季","date":"2027-01"},{"n":2,"text":"AI 合約價值達標，且總成長不掉","type":"假設驗證","maps_to":"H2","metric":"AI ACV 年底值；訂閱營收固定匯率年增","threshold":"2026 年底 AI ACV ≥17 億美元；2027 年第二季起訂閱營收固定匯率 ≥18%","action":"AI ACV 未達標→停止加碼；兩項都達標→補第二批","source_freq":"第四季財報與之後每季法說","date":"2027-01"},{"n":3,"text":"利潤率承諾兌現、股票薪酬下降","type":"假設驗證","maps_to":"H3","metric":"2027 年非 GAAP 營業利益率財測；股票薪酬÷營收","threshold":"營益率財測較 2026 年 31.5% 擴張 ≥100bp；股票薪酬占營收 ≤14%","action":"營益率擴張 <50bp→停止加碼","source_freq":"第四季財報（年度財測）與每季新聞稿","date":"2027-01"},{"n":4,"text":"2027 年訂閱營收財測","type":"Single Thing","maps_to":"Single Thing","metric":"2027 年訂閱營收財測的固定匯率成長","threshold":"<18%","action":"減碼至半倉並重跑研究","source_freq":"2026 年第四季財報，一次性","date":"2027-01"},{"n":5,"text":"明年共識 EPS 持續下修","type":"風險","maps_to":"R1","metric":"FY2027 共識 non-GAAP 稀釋 EPS","threshold":"<4.60（2026-10-31 為 4.83）；<4.35 再升一級","action":"<4.60→停止加碼；<4.35→減碼","source_freq":"Koyfin 共識快照，每月","date":null,"evidence_refs":["capital_markets_pricing#3","capital_markets_pricing#4"]},{"n":6,"text":"DOJ 政府合約調查升級","type":"風險","maps_to":"R3","metric":"10-Q、8-K 中的調查揭露","threshold":"公司遭起訴，或收到停權、除名通知","action":"遭起訴或收到停權通知→減碼至半倉；停權確定→清倉","source_freq":"10-Q 每季、8-K 即時","date":null,"evidence_refs":["regulatory_antitrust#0","major_events#3"]},{"n":7,"text":"聯邦通路夥伴集中度上升","type":"風險","maps_to":"R3","metric":"單一聯邦通路夥伴占營收與應收帳款的比重","threshold":"占營收 >15%，或揭露收款問題","action":"停止加碼","source_freq":"10-Q、10-K，每季","date":null,"evidence_refs":["customer_concentration_credit#2"]},{"n":8,"text":"原告律所調查轉為正式集體訴訟","type":"風險","maps_to":"R3","metric":"證券集體訴訟進度","threshold":"正式提起並獲集體認證，且出現不利和解","action":"減碼至半倉","source_freq":"10-Q 法律程序段，每季","date":null,"evidence_refs":["lawsuit_class_action#1"]},{"n":9,"text":"訂閱毛利率續降，價值被前端與雲端分走","type":"風險","maps_to":"R2","metric":"非 GAAP 訂閱毛利率","threshold":"<78% 連 2 季（第三季 80%、全年財測 81%）","action":"停止加碼，並把代理繞過威脅升為最高級後重評","source_freq":"公司季報新聞稿，每季","date":null,"evidence_refs":["supply_demand_durability#2","substitute_technology#3"]},{"n":10,"text":"再做大型收購","type":"風險","maps_to":"R4","metric":"收購公告金額","threshold":"單筆 >50 億美元","action":"停止加碼，並下修資本配置結論","source_freq":"8-K，即時","date":null,"evidence_refs":["ma_merger#1"]},{"n":11,"text":"價格或成長確認後加碼","type":"加碼","maps_to":"H2","metric":"週收盤相對 W104；cRPO 固定匯率年增","threshold":"週收站回 W104（現約 158），或 2027 年第二季起 cRPO 固定匯率 ≥18% 連 2 季","action":"加碼一級","source_freq":"週線、每季","date":null},{"n":12,"text":"成長跌破下限","type":"減碼","maps_to":"R1","metric":"cRPO 固定匯率年增；AI ACV 季度淨增","threshold":"cRPO 固定匯率 <17.5% 連 2 季，或 AI ACV 淨增轉負","action":"減碼至半倉","source_freq":"公司季報，每季","date":null},{"n":13,"text":"留存崩壞","type":"清倉","maps_to":"R2","metric":"續約率；訂閱營收固定匯率年增","threshold":"續約率 <95% 連 2 季，或訂閱營收固定匯率 <12%","action":"清倉","source_freq":"公司季報，每季","date":null,"evidence_refs":["competitive_share_entrants#2"]},{"n":14,"text":"第四季財報後重跑研究","type":"複審日期","maps_to":null,"metric":"2027 年財測與第四季實績","threshold":"財報公布","action":"重跑研究，決定第二批是否補進","source_freq":"一次性","date":"2027-01"},{"n":15,"text":"Armis 滿一年後的第一個乾淨 cRPO","type":"複審日期","maps_to":"H2","metric":"cRPO 固定匯率年增","threshold":"2027 年第二季財報公布","action":"重跑研究，檢驗一次性說明是否成立","source_freq":"一次性","date":"2027-07"}],"kill_metrics":[{"metric":"cRPO 固定匯率年增（公司公布值）","bear_threshold":"<17.5% 連 2 季","window":"2026 第四季至 2027 第四季","source":"公司季報新聞稿","last_status":"ok"},{"metric":"FY2027 共識 non-GAAP 稀釋 EPS","bear_threshold":"<4.60（2026-10-31 為 4.83，近 3 個月 −3.4%）","window":"至 2027 年第二季財報","source":"Koyfin 共識快照","last_status":"warning"},{"metric":"季度續約率","bear_threshold":"<97% 連 2 季","window":"每季","source":"公司法說","last_status":"ok"},{"metric":"2027 年訂閱營收財測的固定匯率成長","bear_threshold":"<18%","window":"2027 年 1 月第四季財報","source":"公司財測","last_status":"unknown"},{"metric":"非 GAAP 訂閱毛利率","bear_threshold":"<78% 連 2 季","window":"每季","source":"公司季報新聞稿","last_status":"ok"},{"metric":"DOJ 政府合約調查","bear_threshold":"遭起訴或收到停權通知","window":"持續","source":"10-Q、8-K","last_status":"unknown"}],"evidence_dismissed":[{"ref":"reg_tariff_export#0","reason":"這是 10-K 的制式風險揭露，沒有金額、受影響營收或時點；同一份 10-K 的 MD&A 寫明未因總體事件影響流動性與營運。公司 97% 營收是訂閱軟體，關稅只涉及營運相關的進口，這筆證據本身對應不到任何損益數字。"}],"action_conditions":{"rearm_trigger":"加碼＝週收站回W104（現約158）或2027Q2起cRPO固定匯率≥18%連2季；減碼＝cRPO固定匯率<17.5%連2季或AI ACV淨增轉負","exec_line":"分兩批進場：現價先建一半。另一半等 2027 年 1 月第四季財報：2027 年訂閱營收財測固定匯率成長 ≥18%，且 FY2027 共識 EPS ≥4.60，才補進；若財測 <18%，不補，並減碼至半倉。","holding_cap":"單檔上限 5%；共識持續下修期間不超過 4%"}},"decision_inputs":{"signal":"B","ma":"❌","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場把 ServiceNow 當成會被 AI 代理吃掉的座位制軟體來定價，公司自身倍數落在四個年度端點的最低點。但本季數字指向相反方向：續約率 98%，RPO 297 億美元、年增 22.5% 且合約年期拉長，一半新增 ACV 已不是座位計價，外部代理經 Action Fabric 呼叫仍按次計費。市場錯在把定價模式轉換當成需求流失。若 Armis 滿一年後 cRPO 固定匯率成長連 2 季低於 17.5%，這個理由就被證偽。","momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":null,"wait_for_price_condition":null},"decision_out":{"verdict":"進場","role":"衛星","row_hit":"9（MA❌例外）","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":true,"basis":"ma='❌'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場把 ServiceNow 當成會被 AI 代理吃掉的座位制軟體來定價，公司自身倍數落在四個年度端點的最低點。但本季數字指向相反方向：續約率 98%，RPO 297 億美元、年增 22.5% 且合約年期拉長，一半新增 ACV 已不是座位計價，外部代理經 Action Fabric 呼叫仍按次計費。市場錯在把定價模式轉換當成需求流失。若 Armis 滿一年後 cRPO 固定匯率成長連 2 季低於 17.5%，這個理由就被證偽。"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟢', val='🟡', moat_trend='→', week26=15.31, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position=None, moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":false,"basis":"signal='B', val='🟡'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":true,"basis":"signal='B', val='🟡', ma='❌'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟡', ma='❌'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟡', ma='❌'"},{"row":"9-verdict","condition":"命中 row9 → 進場","hit":true,"basis":"MA=❌ 但 signal≥B 且 val≤🟡 且無 Veto：依「baseline rows 9/9b/10 的 MA 條件字面不含 ❌ 時，該組合不落空、不降觀望——按對應 val 燈 baseline row 裁決，MA❌ 僅作 row4 節奏調節」推論，verdict=進場（row4 pacing 已疊加，見上）"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]}],"pacing":["row4：週線❌，進場節奏強制分批（starter 1/3＋趨勢確認後加碼），頁首掛「⚠️ 週線趨勢未確認，逢回分批勿接刀」"],"holding_cap":null,"requires_critic":[]},"thesis":{"H":[{"id":"H1","text":"工作流系統記錄層（CMDB、工作流資料、代理治理）讓大企業留下來：AI 代理要在企業裡動手，仍得經過 ServiceNow，續約與大客戶擴張不會退","2y":null,"5y":"2031 年前續約率維持 97% 以上，年 ACV 逾 500 萬美元的客戶數每年增加 8% 以上（2026 第三季 680 家、第二季 658 家）","10y":null,"threshold":"續約率 ≥97%；大客戶數年增 ≥8%","source":"公司季度新聞稿與法說（續約率、大客戶數）","drift_rule":"五年期：門檻偏離連 4 季 ≥5% 判削弱，連 6 季 ≥10% 判反轉"},{"id":"H2","text":"AI 與用量計價是淨增量：AI ACV 的成長補得上座位制放緩，Armis 滿一年後，訂閱營收固定匯率成長仍守在 18% 以上","2y":null,"5y":"2030 年 AI 占 ACV 約 30%（CFO 2026-05-04 設定的目標），訂閱營收朝 300 億美元以上前進","10y":null,"threshold":"2026 年底 AI ACV ≥17 億美元；2027 年第二季起訂閱營收固定匯率 ≥18%","source":"第四季財報與每季法說（AI ACV、訂閱營收固定匯率成長）","drift_rule":"五年期：門檻偏離連 4 季 ≥5% 判削弱，連 6 季 ≥10% 判反轉"},{"id":"H3","text":"股東經濟同步改善：利潤率照承諾擴張、股票薪酬占比下降，EPS 複利不需要倍數回升","2y":"2027 年非 GAAP 營益率較 2026 年的 31.5% 擴張至少 100bp（CFO 2026-05-04 承諾），股票薪酬占營收降到 14% 以下（2026 第三季為 15.4%），FY2027 EPS 不低於 4.60","5y":null,"10y":null,"threshold":"營益率擴張 ≥100bp；股票薪酬占營收 ≤14%；FY2027 EPS ≥4.60","source":"第四季財報的年度財測、每季新聞稿、Koyfin 共識","drift_rule":"兩年期：連 2 季偏離 ≥5% 判削弱，連 3 季 ≥10% 判反轉"}],"R":[{"id":"R1","text":"成長減速與共識下修循環：第四季 cRPO 財測 18.5%，低於前三季；三年共識 EPS 三個月內各降 2–3%，看起來便宜，有一部分是因為分母在降","h_ref":"H2","clock":"🔥","threshold":"cRPO 固定匯率 <17.5% 連 2 季；FY2027 共識 EPS <4.60","evidence_refs":["capital_markets_pricing#3","capital_markets_pricing#4"]},{"id":"R2","text":"AI 代理與競爭重劃預算：Salesforce Agentforce IT 服務管理、微軟捆綁銷售、企業用 AI 工具自建，加上座位制轉用量計價，可能把應用軟體利潤率壓縮 100–900bp（彭博行業研究）；要到 2027–28 年續約潮才看得到結果","h_ref":"H1","clock":"🐢","threshold":"續約率 <97% 連 2 季，或非 GAAP 訂閱毛利率 <78% 連 2 季","evidence_refs":["competitive_share_entrants#1","competitive_share_entrants#2","substitute_technology#0","substitute_technology#2","substitute_technology#3","supply_demand_durability#2"]},{"id":"R3","text":"聯邦與事件風險：單一聯邦通路夥伴占營收升到 13%（2025 年 11%）；DOJ 調查政府合約合規問題，公司已通報陸軍停權除名辦公室，無法預測結果；中東衝突曾讓 2026 年第一季大型地端交易延後，拖累訂閱成長約 75bp","h_ref":"H1","clock":"⚡","threshold":"遭起訴或收到停權通知；該夥伴占營收 >15%","evidence_refs":["customer_concentration_credit#2","regulatory_antitrust#0","major_events#3","geo_supply_chain#0"]},{"id":"R4","text":"舉債併購的報酬未驗證：Armis 約 77.5 億美元現金收購，部分以 40 億美元定期貸款支應，淨負債 38 億美元；12 個月內完成三筆收購","h_ref":"H3","clock":"🔥","threshold":"2027 年營益率擴張 <50bp，或再宣布單筆 >50 億美元收購","evidence_refs":["ma_merger#1"]}],"single_thing":{"description":"2027 年 1 月下旬第四季財報給出的 2027 年訂閱營收財測，固定匯率成長低於 18%","why_fatal":"基礎情境 2027–2028 年 EPS 年增約 20%，靠的是約 19–20% 的訂閱營收成長加上利潤率擴張。財測低於 18%，等於公司自己承認 AI 沒能補上座位制的放緩。營收成長率是 EPS 路徑裡敏感度最大的一項，倍數也會跟著往空頭的 15 倍靠攏。","if_happens":"減碼至半倉並重跑研究；空頭機率由 30% 上調到 40% 以上，停止一切加碼，直到 Armis 滿一年後的 cRPO 證明成長守住 17.5%","how_monitor":"看第四季財報新聞稿與法說中的年度財測。事前先看兩件事：第四季 cRPO 實際值是否高於財測的 18.5%，以及 FY2027 共識營收（目前 192.68 億美元，隱含約 18.7% 成長）有沒有變動","probability":"約 25%（12–24 個月內）。管理層 2026 年兩次都只把一半超標傳遞到全年，財測偏保守；但第四季 cRPO 財測已經降到 18.5%"}},"appendix_a":{"growth_durability":7,"quality_score":6,"ai_risk":"🟡","long_term_confidence":"中","fpe_fy2":21.76,"peg_fy2":0.98,"stress":{"pass":2,"total":3}},"eps_meta":{"base_eps_path":{"FY2025A":null,"FY2026E":3.97,"FY2027E":4.83,"FY2028E":5.92},"fy_end_month":12,"eps_basis":"non-GAAP 稀釋 EPS（Koyfin 共識，與 2026 第三季非 GAAP 稀釋 EPS 1.00 同口徑）；分析師家數事實表未涵蓋。FY2025 非 GAAP 實際值事實表未涵蓋；GAAP 的 1.67 口徑不同，不代入"},"catalysts":[{"date":"2026-12","date_precision":"quarter","type":"product","event":"AIOps、HRSD、CRM 的 AI 專員預計在第四季全面上市","impact":"中","watch":"上市後是否揭露用量與 Assist 消耗"},{"date":"2027-01","date_precision":"month","type":"guidance","event":"2026 年第四季財報與 2027 年全年財測","impact":"高","watch":"2027 年訂閱營收固定匯率成長是否 ≥18%、營益率擴張是否 ≥100bp、AI ACV 年底是否 ≥17 億美元"},{"date":"2027-07","date_precision":"quarter","type":"other","event":"2027 年第二季財報：Armis 滿一年後第一個不含無機貢獻的 cRPO","impact":"高","watch":"cRPO 固定匯率成長是否 ≥18%"},{"date":null,"date_precision":null,"type":"regulatory","event":"DOJ 政府合約合規調查","impact":"中","watch":"10-Q、8-K 是否揭露起訴、和解或停權通知"}]}
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
