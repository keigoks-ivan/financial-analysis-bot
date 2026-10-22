你是 DD 管線 v20 的判斷層閘（gate），標的 MMM（20261022）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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
- `f_kpi0_net_sales_gaap`（q1_business）｜Net sales (GAAP)＝6584 USD million｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-20）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：3M Q3 2026 earnings release（SEC 8-K Ex.99.1）（numbers.latest_quarter_kpis.items[0]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-20））
  - 註記：consensus 約 $6.61B，略低於預期（來源：web_search）
- `f_kpi1_adjusted_operating_margi`（q1_business）｜Adjusted operating margin (Non-GAAP)＝26.2 %｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-20）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：3M Q3 2026 earnings release（SEC 8-K Ex.99.1）；調整後營業利益 $1,726M；新口徑把收購無形資產攤銷列為特殊項目（numbers.latest_quarter_kpis.items[1]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-20））
  - 註記：無查得
- `f_kpi2_operating_margin_gaap`（q1_business）｜Operating margin (GAAP)＝23.7 %｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-20）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：3M Q3 2026 earnings release（SEC 8-K Ex.99.1）；GAAP 營業利益 $1,558M（numbers.latest_quarter_kpis.items[2]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-20））
  - 註記：無查得
- `f_kpi3_adjusted_free_cash_flow`（q1_business）｜Adjusted free cash flow＝1197 USD million｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-20）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：3M Q3 2026 earnings release；營業現金流 $486M（web_search 引 Investing/StockTitan 之 $1.197B）（numbers.latest_quarter_kpis.items[3]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-20））
  - 註記：無查得
- `f_kpi4_adjusted_eps`（q1_business）｜Adjusted EPS＝2.5 USD｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-20）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：3M Q3 2026 earnings release（SEC 8-K Ex.99.1）；GAAP EPS $2.63（numbers.latest_quarter_kpis.items[4]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-20））
  - 註記：consensus $2.39（來源：web_search），超預期
- `f_kpi5_fy2026_guidance_manageme`（q1_business）｜FY2026 guidance（management）＝調整後 EPS $9.10–$9.15 USD｜期間與口徑：Q3 2026 公告（2026-10-20）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：3M Q3 2026 earnings release（SEC 8-K Ex.99.1）；調整後總銷售成長 >4.5%、有機 >3.5%、調整後 FCF 約 $4.8B（營業現金流約 $5.9B）、調整後營業利潤率約 24.6%、稅率約 20%（numbers.latest_quarter_kpis.items[5]，as_of Q3 2026 公告（2026-10-20））
  - 註記：FY1 共識 EPS 8.98（財報前快照，來源 consensus_revision）
- `f_peer_mmm_gross_margin_pct`（q2_moat）｜MMM 毛利率＝39.4 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MMM.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_earnings_recency`（q1_business）｜最近一次財報日＝2026-10-20 date｜期間與口徑：2026-10-20／距今 2 個交易日｜kind：realized
  - 來源：—（numbers.earnings_recency，as_of 2026-10-20）
- `f_peer_mmm_operating_margin_pct`（q2_moat）｜MMM 營業利益率＝20.36 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MMM.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_mmm_fcf_margin_pct`（q2_moat）｜MMM FCF 利潤率＝15.83 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MMM.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_hon_gross_margin_pct`（q2_moat）｜HON 毛利率＝36.57 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.HON.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_hon_operating_margin_pct`（q2_moat）｜HON 營業利益率＝16.58 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.HON.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_hon_fcf_margin_pct`（q2_moat）｜HON FCF 利潤率＝11.1 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.HON.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_itw_gross_margin_pct`（q2_moat）｜ITW 毛利率＝44.16 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ITW.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_itw_operating_margin_pct`（q2_moat）｜ITW 營業利益率＝26.5 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ITW.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_itw_fcf_margin_pct`（q2_moat）｜ITW FCF 利潤率＝17.74 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ITW.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_emr_gross_margin_pct`（q2_moat）｜EMR 毛利率＝53.16 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.EMR.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_emr_operating_margin_pct`（q2_moat）｜EMR 營業利益率＝20.69 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.EMR.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_emr_fcf_margin_pct`（q2_moat）｜EMR FCF 利潤率＝18.57 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.EMR.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝8.98 USD/share｜期間與口徑：2026-10-21／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261021.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-10-21）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝9.82 USD/share｜期間與口徑：2026-10-21／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261021.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-10-21）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝10.56 USD/share｜期間與口徑：2026-10-21／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261021.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-10-21）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝25429.25 USD m｜期間與口徑：2026-10-22／yfinance revenue_estimate 0y 平均（14 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-10-22）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝26610.61 USD m｜期間與口徑：2026-10-22／yfinance revenue_estimate +1y 平均（14 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-10-22）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝2.98 %｜期間與口徑：2026-07-16 → 2026-10-21／FY1 共識 EPS 8.72 → 8.98（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261021.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-10-21）
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝7857.0 USD m｜期間與口徑：2026-10-22／yfinance 最新一季：總債務 13160.0、現金 5303.0（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-10-22）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝515.72 m shares｜期間與口徑：2026-10-22／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-10-22）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝1.757 %｜期間與口徑：2026-10-22／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-10-22）
- `f_ev_m`（q5_valuation）｜目前企業價值 EV（市值＋淨負債）＝97974.34 USD m｜期間與口徑：2026-10-22／市值 90117.34 ＋ 淨負債 7857.0｜kind：realized
  - 來源：—（numbers.capital_structure.ev_m，as_of 2026-10-22）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝174.74 USD｜期間與口徑：2026-10-21（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-10-21（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝19.46 x｜期間與口徑：2026-10-21／分母＝FY1 EPS 8.98，分子＝快照價 174.74｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-10-21）
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝26.08 x｜期間與口徑：2026-10-21（RTH 收盤，UTC）／3 個年度端點內的分位＝97.1｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-10-21（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝97.1 %｜期間與口徑：2026-10-21（RTH 收盤，UTC）／**非五年分位**：只用 3 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-10-21（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝100.0 %｜期間與口徑：2026-10-21（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-10-21（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝100.0 %｜期間與口徑：2026-10-21（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-10-21（RTH 收盤，UTC））
- `f_ma_w104`（q5_valuation）｜104 週均線＝151.03 USD｜期間與口徑：2026-10-22／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-10-22）
- `f_ma_w250`（q5_valuation）｜250 週均線＝116.58 USD｜期間與口徑：2026-10-22／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-10-22）
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝16.53 %｜期間與口徑：2026-10-21（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-10-21（RTH 收盤，UTC））
- `f_rsi14`（q5_valuation）｜RSI(14)＝59.92｜期間與口徑：2026-10-21（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-10-21（RTH 收盤，UTC））

### findings_digest 中方向為負或來源衝突的條目（13 條）
- `regulatory_antitrust#1`（regulatory_antitrust｜方向 -｜狀態 ok）：3M 2026 年 10-Q 稱 PFAS 法規在美加歐亞持續擴張，限值逐步下修，並可能涵蓋 3M 已不再製造的化合物；CERCLA 將 PFOA／PFOS 列為有害物質後，3M 可能需額外調查與整治。
  - 來源：SEC EDGAR 10-Q 2026-06-30（as_of 2026-07-30）｜affects：decision_inputs.bear、thesis.R
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：FY2025 10-K：3M 2025 年約 56% 營收來自美國以外，並明列美中貿易緊張升級可能對業務造成重大不利影響。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A Risk Factors（as_of 2026-02-03）｜affects：decision_inputs.bear、thesis.R
- `reg_tariff_export#1`（reg_tariff_export｜方向 -｜狀態 ok）：FY2025 10-K：美國及其他政府已實施並擬再實施出口管制與關稅，可能造成供應鏈中斷（含稀土取得受限）、生產成本與產品定價上升。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A Risk Factors（as_of 2026-02-03）｜affects：decision_inputs.bear、thesis.R
- `reg_tariff_export#2`（reg_tariff_export｜方向 -｜狀態 ok）：FY2025 10-K MD&A：2025 年銷貨成本率上升部分來自關稅；營業利益率受關稅衝擊部分抵銷。
  - 來源：SEC EDGAR 10-K FY2025 Item 7 MD&A（as_of 2026-02-03）｜affects：valuation、decision_inputs.bear
- `reg_tariff_export#4`（reg_tariff_export｜方向 -｜狀態 ok）：2025 年 4 月 3M 估計年化關稅衝擊約 8.5 億美元（美中關稅占 6.75 億），中國約占進口 10%、出口略高於 10%。
  - 來源：Manufacturing Dive：3M Q1 2025 tariff impact（as_of 2025-04-25）｜affects：valuation、decision_inputs.bear
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：3M 於 2026-01 警告美歐（格陵蘭爭端）貿易緊張可能衝擊 2026 獲利，評估關稅曝險
  - 來源：Seeking Alpha: 3M flags tariff risk tied to Europe dispute; shares fall（as_of 2026-01-20）｜affects：decision_inputs.bear
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：2025 年中國約占 3M 全球營收 10%，進口約 10%、出口略高於 10%；關稅年化衝擊預估 8.5 億美元（美中 6.75 億）
  - 來源：Manufacturing Dive: 3M Q1 2025 $850 million tariff impact（as_of 2025-04-25）｜affects：decision_inputs.bear、valuation
- `end_markets#2`（end_markets｜方向 -｜狀態 ok）：Consumer 部門需求疲弱，美國零售客流未回升
  - 來源：Chartmill: Weak Demand Weighs on 3M's Consumer Unit（as_of 2026-05-01）｜affects：thesis.R、decision_inputs.bear
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：10-K 風險因子：產品需求受競爭產品推出、客戶偏好（含偏好不含第三方製造 PFAS 的產品）及客戶設計變動影響，並提及人工智慧等顛覆性技術。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-03）｜affects：moat_trend、thesis.R
- `substitute_technology#1`（substitute_technology｜方向 -｜狀態 ok）：3M 已於 2025 年底完成退出 PFAS 製造；Novec/Fluorinert 供應 2025-12-31 結束，競爭對手已推出直接替代流體。
  - 來源：The Engineer／廠商頁：Novec 淘汰與 ProSolv 直接替代（as_of 2025-01-01）｜affects：moat_trend
- `substitute_technology#2`（substitute_technology｜方向 -｜狀態 ok）：3M 退出 PFAS 後，市占重分配預期推升替代技術需求；Intel 等成立聯盟因應含氟化學品停供。
  - 來源：Kline Group：Evolving Landscape of PFAS Regulations and Industry Response（as_of 2025-04-13）｜affects：moat_trend
- `major_events#1`（major_events｜方向 -｜狀態 ok）：FY2025 10-K 揭露 AFFF MDL（PFAS）仍有個人、公共水system、集體成員、州政府等原告；Rome/Floyd County 集體訴訟尚未排審。
  - 來源：SEC EDGAR 10-K FY2025 Item 8（as_of 2026-02-03）｜affects：decision_inputs.bear、valuation
- `lawsuit_class_action#0`（lawsuit_class_action｜方向 -｜狀態 ok）：AFFF MDL 含集體成員等原告；Rome/Floyd County 水費集體訴訟 2025-12 提出簡易判決動議，尚無審理日。
  - 來源：SEC EDGAR 10-K FY2025 Item 8（as_of 2026-02-03）｜affects：decision_inputs.bear、valuation

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MMM_20261022/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":286.0,"bear_5y_price":135.8,"p_bull_pct":25,"p_bear_pct":30,"upside_5y_pct":25.0,"ev5y_pct":20.5,"irr_base_pct":4.6,"asym_ratio":2.4,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":8.98,"pe":19.46,"basis":"FY2026E 共識調整後 EPS（財報前快照）÷ 判斷日股價；終端倍數同樣套在終端年的調整後 EPS"},"eps":{"bull":[10.0,11.0,12.1,13.2,14.3],"base":[9.85,10.6,11.35,12.1,12.85],"bear":[9.3,9.0,9.2,9.5,9.7]},"pe":{"bull":20,"base":17,"bear":14},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":1.757,"net_buyback":2.0},"second_stage":{"bull_cagr_pct":8.0,"base_cagr_pct":5.5},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### MMM_Q2_2026_Earnings_Call_20260721.md
- 2026-07-21｜CFO｜guidance：全年有機成長指引由 3% 上調至 >3.5%（原話："We are raising our organic growth expectations from 3% to"）
- 2026-07-21｜CFO｜guidance：EPS 指引上調至 $8.80–8.95，中點增 $0.27（原話："EPS guidance is increasing from a range of $8.50 to $8.70"）
- 2026-07-21｜CFO｜guidance：自由現金流指引上調 $1 億至 $47–49 億，轉換率 >100%（原話："we have increased our free cash flow guidance by $100"）
- 2026-07-21｜CFO｜guidance：指引隱含下半年有機成長與利潤率擴張幅度（原話："The updated guidance implies second half organic sales"）
- 2026-07-21｜CFO｜guidance：Madison Fire & Rescue 合資未納入本次指引，Q3 財報再納入；稅率約 20%（原話："we'll incorporate that in our third quarter call. And just"）
- 2026-07-21｜CEO｜guidance：下半年消費品預期持平至小幅成長（原話："help us in the back half of consumer to be flat to up"）
- 2026-07-21｜CFO｜margin：Q2 調整後營業利益率 24.9%，比預期高 40bp，來自量與生產力（原話："So we finished the quarter at 24.9% margin, which is the"）
- 2026-07-21｜CFO｜margin：營業利潤增額拆解：成長與生產力 +2.4 億，投資 -3,000 萬，關稅與滯留成本 -1.1 億（原話："Operating profit increased $110 million or $0.16, including"）
- 2026-07-21｜CFO｜margin：油價相關通膨預估由 1.25 億升至 1.5–1.75 億，金額中性但壓低利潤率 20bp（原話："Though oil price cost"）
- 2026-07-21｜CEO｜margin：毛利率目前接近 45% 中段，長期可達高 40%（原話："On gross margins, we're tracking to -- close to mid-40s"）
- 2026-07-21｜CEO｜margin：管理層表示長期有能力把毛利率拉到高 40%（原話："with an ability to hit the high 40s over time."）
- 2026-07-21｜CEO｜margin：油價成本將以定價逐元抵銷，油價面價格成本中性、整體略正（原話："So price cost on oil is"）
- 2026-07-21｜CFO｜margin：滯留成本全年 1.5 億、投資 2.25 億，皆下半年較重；生產力較佳（原話："Just on the stranded cost, it's still $150"）
- 2026-07-21｜CFO｜margin：尚未收到任何關稅退款（原話："We have not received any tariff refunds to date."）
- 2026-07-21｜CEO｜margin：Q2 價格貢獻 1.6%，下半年約 2%，全年約 1.5 點（原話："Q2, our price was at 1.6%. So it was about in line with"）
- 2026-07-21｜CFO｜margin：下半年 EPS 成長約 $0.30，Q3、Q4 平均，季節性正常（原話："So I would say it's normal seasonality with the EPS growing"）
- 2026-07-21｜CFO｜margin：FCF 轉換率 107%，庫存天數改善 7 天，主因營運表現（原話："Our inventories improved by 7 days year-over-year. So just"）
- 2026-07-21｜CFO｜commitment：管理層稱進度領先投資人日承諾（超額成長、約 25% 利潤率、雙位數 EPS CAGR）（原話："we are tracking ahead of Investor Day commitments across"）
- 2026-07-21｜CFO｜commitment：高於總體的成長額預期超過 10 億承諾（原話："is on track to exceed the $1"）
- 2026-07-21｜CFO｜commitment：利潤率領先 2027 年約 25% 的目標（原話："are tracking ahead of the"）
- 2026-07-21｜CEO｜commitment：今年高於總體成長約 4.5 億，高於上季的約 3.4–3.5 億；原計畫三年為 1.25 億／3.26 億／6.27 億（原話："We think we'll be about $450 million above macro in the"）
- 2026-07-21｜CEO｜commitment：股東回饋承諾：2025 起累計 86 億，目標 2027 前 100 億以上（原話："against our commitment to return $10 billion plus through"）
- 2026-07-21｜CEO｜commitment：新產品目標：2027 年前推出逾 1,000 項，開發週期縮短約 20%（原話："launch more than 1,000 products by 2027, while reducing"）
- 2026-07-21｜CFO｜capital_allocation：上半年回購約 30 億，均價約 153 美元，超過年初 25 億預期，下半年「機會式」（原話："We've done about $3 billion at an average price of about"）
- 2026-07-21｜CEO｜capital_allocation：7/1 完成 Madison Fire & Rescue 與 Scott SCBA 合併為多數持股合資，收現金 7 億（原話："receiving $700 million in cash as part of the transaction."）
- 2026-07-21｜CEO｜capital_allocation：合資體營收 8 億、高單位數成長、利潤率高於公司平均（原話："This JV generates revenue of $800 million,"）
- 2026-07-21｜CEO｜capital_allocation：將財務、人資、客服整合為全球共享服務並委外給外部供應商（轉型下一步）（原話："partnering with an external provider to run them at scale"）
- 2026-07-21｜CEO｜product：Microsoft 成為首家部署 EBO 的超大規模業者（Azure）（原話："Microsoft, who will become the first hyperscaler to"）
- 2026-07-21｜CEO｜product：EBO 今年營收 4,000–5,000 萬，數年內可達 4–5 倍以上（原話："The revenue this year was in the"）
- 2026-07-21｜CEO｜product：EBO 今年 TAM 約 10 億，2028 年約 20 億；3M 目前份額小（原話："But the TAM this year for EBO technologies is around $1"）
- 2026-07-21｜CEO｜product：EBO 產能今年翻倍、未來 18 個月再翻倍，仍遠低於市場需求（原話："double our capacity on"）
- 2026-07-21｜CEO｜product：Q2 推出 92 項新產品（+44%），上半年 176 項，全年預計 350 項以上（原話："we launched 92 new products, up 44% versus last year"）
- 2026-07-21｜CEO｜product：新產品中 Class 3 約 75%、Class 4/5 約 25%，長期升至 30% 以上（原話："But Class 3 for us is running around 75% of the launches."）
- 2026-07-21｜CEO｜product：新品活力指數今年中段十幾%，明年 20%；五年內新品銷售約 40 億（原話："new product vitality index climbing to the mid-teens this"）
- 2026-07-21｜CEO｜competition：EBO 有約 100 項專利、50 項申請中；但 3M 不會是唯一供應商，已授權並組成 44 家多供應商協議（原話："we will not be successful as a sole provider here."）
- 2026-07-21｜CEO｜competition：成長倍數由大致等同市場提升到 2 倍（原話："improving from roughly in line to 2x and with businesses"）
- 2026-07-21｜CEO｜competition：管理層將成長歸因於內部表現而非總體順風（原話："It's not really macro tailwind."）
- 2026-07-21｜CEO｜customer：SIBG 客戶流失率改善約 200bp，仍偏高（原話："We've seen about 200 basis points of improvement in"）
- 2026-07-21｜CEO｜customer：交叉銷售已訂 1.1 億、另有 1.2 億在管線，超前投資人日目標（原話："$110 million of opportunities booked and another $120"）
- 2026-07-21｜CFO｜customer：Q2 訂單約 +10%、積壓訂單年增近 20%；75% 為即訂即出貨（原話："So our orders were up about 10% for the quarter and backlog"）
- 2026-07-21｜CFO｜customer：Q3 前兩週訂單與積壓訂單良好（原話："But so far, the first 2 weeks, orders and backlog look good."）
- 2026-07-21｜CEO｜customer：中國 Q2 雙位數成長、上半年約 8%，內銷與出口各半（原話："In the second quarter, we were double-digit growth, first"）
- 2026-07-21｜CFO｜customer：消費品 Q2 -2.1%；六月下旬數家零售商壓低庫存抵銷了 POS 動能（原話："tightening of inventory levels"）
- 2026-07-21｜CEO｜risk：觀察項：下半年消費電子裝置產量預期下滑高十幾%，與記憶體短缺與成本有關（原話："expected to be"）
- 2026-07-21｜CEO｜risk：汽車與售後市場仍弱，美國消費者保守、重視價值（原話："the U.S. consumer remains cautious"）
- 2026-07-21｜CEO｜risk：整體產能利用率約 63.5–64%，個別資產如 New Ulm 受限（原話："It's running around 63.5%, 64%."）


---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 1 | 2 |
| customer_second_source | none | 0 | 2 |
| customer_concentration_credit | found | 2 | 2 |
| supply_demand_durability | found | 2 | 2 |
| regulatory_antitrust | found | 2 | 3 |
| reg_tariff_export | found | 5 | 2 |
| geo_supply_chain | found | 3 | 3 |
| end_markets | found | 4 | 3 |
| substitute_technology | found | 3 | 2 |
| channel_business_model_shift | found | 2 | 2 |
| capital_markets_pricing | found | 3 | 3 |
| major_events | found | 4 | 5 |

未涵蓋／不適用軸的查詢詞原文（供判相關性）：
- **customer_second_source**（none）：3M largest customer second source OR in-house 2026；3M single-source risk customer diversify supplier

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260722","verdict":"觀望","role":"追蹤","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"Brown margin 改革兌現且可延續：adj OM 從 24.9% 續升（FY27 25%+ 目標上修、gross margin mid-40s→high-40s），驅動 EPS 從 FY26 $8.88 至 FY28 $10.19","columns":{"2Y 驗證點":"adj OM 續升 + FY27 目標正式上修至 >25%；FY27 EPS ≥ $9.5","5Y 驗證點":"OM 站穩 26-28% + gross margin 逼近 high-40s","10Y 驗證點":"OM 進入頂級工業區間（ITW ~26%+）並維持","數字門檻":"adj OM FY26 >24% / FY27 目標 >25% / FY28 EPS ≥ $10","來源":"Q2 26 adj OM 24.9%（+40bp，史上最高）、FY26 EPS guide 升至 $8.80-8.95","漂移觸發":"OM 連 2 季停滯/倒退 → 削弱；FY27 目標未上修 → 改革紅利封頂"}},{"id":"H2","text":"organic 成長維持「2x macro」（3.5-5%）：commercial excellence + NPI vitality + EBO 資料中心 + 中國/印度份額，非依賴工業週期","columns":{"2Y 驗證點":"organic 維持 >3.5%；orders/backlog 不轉負；NPVI 升向 20%","5Y 驗證點":"organic 站穩 3-4% 穿越週期；EBO 貢獻可見","10Y 驗證點":"NPI 引擎使 3M 長期跑贏工業 IPI","數字門檻":"organic >3.5% / orders 正 / NPVI 升","來源":"Q2 organic +5.4%（H1 +3.3%）、orders +10%/backlog +20%、NPI +44%、EBO $40-50M→$2B TAM by 2028","漂移觸發":"organic 連 2 季"}},{"id":"H3","text":"估值：市場為改革兌現 + Dividend King 給 ~18x，且此溢價可維持（不 de-rate）；PFAS 法律尾部可控不失控","columns":{"2Y 驗證點":"Fwd PE 維持 17-18x；PFAS 現金流出如排程（不新增大額）","5Y 驗證點":"倍數隨改革兌現後成長放緩自然回落至 5Y 中位 ~16x（re-rate 為拖累）","10Y 驗證點":"倍數收斂至成熟工業 15-17x","數字門檻":"Fwd PE ≥ 16x（不跌破 5Y 中位）；PFAS 年流出可控","來源":"賣方共識 avg $172.94（+3%）、中位 $165（","漂移觸發":"PFAS 新增大額求償 或 organic 熄火 → 倍數重設（進場窗開）"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"工業週期回落 + 改革紅利兌現封頂：CE H2 down high-teens（記憶體短缺）+ auto build 續降 → organic 掉回","columns":{"對應假設":"H1/H2","時間尺度":"🔥 中期（4-6 季）","監測指標":"季度 organic、orders/backlog、adj OM、FY27 目標","警戒閾值":"organic 連 2 季"}},{"id":"R2","text":"估值均值回歸：Fwd PE 自 70 分位 / 18x 下修回 5Y 中位 ~16x（即使 EPS 續增，倍數壓縮吞報酬）；分析師中位 $165 已","columns":{"對應假設":"H3","時間尺度":"🔥 中期（4-6 季）","監測指標":"Fwd PE 5Y 分位、共識 EPS 修正、賣方目標 vs 現價","警戒閾值":"PE 跌破 16x 且 EPS 未同步上修 → de-rating 進行中"}},{"id":"R3","text":"PFAS / 法律尾部復燃：耳塞（$6B/至 2029，~半已付）+ 供水（$10.5-12.5B/13 年）為已知排程；但州 AG（NJ $450M）+ 人身傷害求償是開放式尾部——若新增大額求償或新提列，壓 FCF/回購/股息。注意：Q2 法說全程未提法律，須從 10-Q/8-K/docket 追","columns":{"對應假設":"H3","時間尺度":"🐢 長期（2+ 年慢變數）","監測指標":"10-Q 法律附註、8-K、州 AG docket、新提列","警戒閾值":"新增州 AG/人身傷害大額求償 或 FCF 因法律流出"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"回檔 $150-155（Fwd PE ~16x，5Y 中位）或 FY27 OM 目標正式上修（現 24.9% 已達 ~25%，上修將重評 FY27/28 EPS）；或回測 W52 $157","irr_base_pct":6.5,"ev5y_pct":15.0,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"追蹤","signal":"B","val":"🟠","ma":"🟡","trap":"🟡","moat_trend":"→","runway_post_y5":"🟡","asym_ratio":1.7,"ev5y_pct":15.0,"irr_base_pct":6.5,"max_dd_pct":-35.0,"bull_5y_price":234.0,"bear_5y_price":126.0,"p_bull_pct":30.0,"p_bear_pct":25.0,"rearm_trigger":"回檔 $150-155（Fwd PE ~16x，5Y 中位）或 FY27 OM 目標正式上修（現 24.9% 已達 ~25%，上修將重評 FY27/28 EPS）；或回測 W52 $157","price_at_dd":170.76,"archetype":"品質複利成長","cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"MMM","date":"2026-10-22","schema":"v15.0","contract":"v19","company_name":"3M Company"},"oneliner":"改革第三年，利潤率、訂單和新品都在改善，但同口徑財測只上調約 1%，前瞻倍數比前份還貴，PFAS 人身傷害和解金額也還沒封頂；等倍數回到約 17 倍，或 FY27 指引超標再動手","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MMM_20261022/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MMM_20261022/scenario.json","answers":{"q1_business":{"verdict":"3M 賺的是工業、安全、電子與消費客戶的材料和耗材錢。安全與工業加上運輸與電子約占八成營收，消費約占兩成。Q3 營收 $6,584M，調整後營益率 26.2%（GAAP 23.7%）。獲利卡在「產品被寫進客戶製程規格與配方」這一環，價格靠服務水準、交期和新品撐住","reasoning":"最新一季：營收 $6,584M，略低於約 $6.61B 的預期；調整後 EPS $2.50，高於預期的 $2.39；調整後營益率 26.2%，年增 110bp；調整後 FCF $1,197M。全年指引調整後 EPS $9.10–9.15（新口徑），有機成長 >3.5%，調整後 FCF 約 $4.8B。分部方面，安全與工業 Q3 有機 +7%；運輸與電子 +0.5%，其中消費電子約 −15%，其餘 +5%；消費持平。產業時鐘判在擴張期：Q3 訂單 +7%，積壓訂單 +18%，美國工業生產略好於 7 月的預期，但汽車產量與消費電子仍弱。供需屬週期性、可逆，沒有結構性短缺。單點依賴：10-K 稱客戶基礎分散，無重大信用集中，因此無單一客戶風險。集中度風險改落在地區：約 56% 營收在美國以外，中國約占一成","fact_refs":["f_kpi0_net_sales_gaap","f_kpi1_adjusted_operating_margi","f_kpi2_operating_margin_gaap","f_kpi3_adjusted_free_cash_flow","f_kpi4_adjusted_eps","f_kpi5_fy2026_guidance_manageme","f_peer_mmm_gross_margin_pct","f_earnings_recency"],"verdict_values":{"revenue_quality":"Q3 有機 +3.3%。下半年價格貢獻略高於 2%，其餘是量。美加 +7%，為疫情後最高；中國衰退高個位數；美國零售通路去庫存，拖累消費品的進貨","unit_econ_note":"Q3 毛利率年增 230bp，來自採購節省、產能利用率提升與停機減少。CFO 稱增量利潤率接近 40%。油價轉嫁金額中性，但稀釋利潤率約 20bp","archetype":{"primary":"品質複利成長","secondary":"轉機/特殊情境","confidence":"中","fingerprint":"大型材料平台進入改革第三年：利潤率靠自助擴張，再加上回購；PFAS 法律尾部仍在"},"industry":{"clock_phase":"II","sd_verdict_source":"週期性、將隨工業週期反轉：需求擴張來自工業與資料中心（Q3 訂單 +7%、積壓訂單 +18%），汽車與消費電子仍在收縮，供給端無結構性稀缺","bargaining":{"up":"原料端的關稅與油價推高成本，靠議價合約與規模抵銷；2026 年價格已全額覆蓋約 $185M 的油價通膨","down":"客戶分散。漲價靠服務水準與新品，但 2025 年的關稅成本沒能全額轉嫁給客戶","geo":"約 56% 營收在美國以外；中國約占進口一成、出口略高於一成"},"profit_pool_dir":"資料中心、半導體、航太的利潤池在擴大，消費電子 LCD 與零售消費在縮小。3M 的曝險正往前者移動，但資料中心 2026 年營收約 $700M，不到總營收 3%","tam_table":{"expanded":false,"reason":"3M 不是低滲透或新品類的故事。唯一的新品類 EBO 2026 年營收約 $40M，管理層估 2028 年市場規模約 $2B，相對約 $25B 的營收不承重"}}}},"q2_moat":{"verdict":"護城河方向持平，等級 B。執行力在擴大：新品活力指數由 2024 年的 11% 升到十幾%，毛利率年增 230bp。定價力穩定：今年油價全額轉嫁，去年關稅沒有全轉。另外，PFAS 退出讓出了部分氟化學利基","reasoning":"護城河機制是材料科學平台加上被寫進客戶規格的產品，再加上經銷通路的覆蓋。最強同業 ITW 的 TTM 營益率 26.5%，3M 為 20.4%，落後約 6pp。3M Q3 新口徑調整後已到 26.2%，但口徑不同，不能直接比。同業 ROIC 差距的時間序列事實表未涵蓋，無法證明差距在擴大，所以不標上升。產業態勢判為其他結構變動中：法規軸有 PFAS 法規擴張與 CERCLA 指定，關稅軸有美中、美歐關稅；競爭軸靜態，10-K 未點名新進入者或份額流失事件","fact_refs":["f_peer_mmm_gross_margin_pct","f_peer_mmm_operating_margin_pct","f_peer_mmm_fcf_margin_pct","f_peer_hon_gross_margin_pct","f_peer_hon_operating_margin_pct","f_peer_hon_fcf_margin_pct","f_peer_itw_gross_margin_pct","f_peer_itw_operating_margin_pct","f_peer_itw_fcf_margin_pct","f_peer_emr_gross_margin_pct","f_peer_emr_operating_margin_pct","f_peer_emr_fcf_margin_pct"],"verdict_values":{"moat":{"mechanism":"材料科學平台（膠帶、薄膜、研磨、個人防護）的產品被客戶寫進製程與配方，加上全球經銷通路與交叉銷售。新品活力指數回升，代表平台還能產出新規格","execution":8,"pricing":7,"grade":"B","trend":"→","trend_evidence":"執行面在擴大：Q3 推出 87 項新品（+24%），成本品質改善 40bp，客戶流失率改善約 200bp，但 2026-07-21 法說 CEO 自稱仍偏高。定價面穩定：下半年價格貢獻略高於 2%，全額覆蓋油價；但 2025 年關稅未全額轉嫁。Novec 等氟化液已被競品直接替代。兩面合併判持平","competitor_notes":[{"name":"ITW","strategy_note":"營益率 26.5%、FCF 利潤率 17.7%，是利潤率標竿；3M 的改革目標其實就是追上 ITW 式的成本紀律"},{"name":"HON","strategy_note":"營益率 16.6%、FCF 利潤率 11.1%，都低於 3M；不是利潤率上的威脅"},{"name":"EMR","strategy_note":"毛利率 53.2% 偏高，來自自動化軟體組合；營益率 20.7% 與 3M 相近，業務重疊有限"}],"peer_na_reason":"同業 ROIC 與前瞻倍數事實表未涵蓋，只有 TTM 利潤率","threats":[{"level":"🟡","text":"PFAS 退出後，Novec 等氟化液已由競品推出直接替代流體，半導體客戶另組聯盟找替代方案；這是點對點失地，不扣分","p":"已發生","evidence_refs":["substitute_technology#1","substitute_technology#2"]},{"level":"🟡","text":"10-K 把客戶偏好不含 PFAS 的產品、客戶設計變更、AI 等顛覆技術列為需求風險；目前沒有具名的份額流失事件","p":"20%","evidence_refs":["substitute_technology#0"]},{"level":"🟡","text":"消費電子的 LCD 顯示膜需求下滑，中國手機品牌市場大跌；高階品牌約占該業務七成，3M 自稱表現與市場相當或略好","p":"30%","evidence_refs":[]}],"roic_durability":{"quadrant":"高利益率；周轉率因投入資本口徑缺而未知（事實表未涵蓋）","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"產品多為重複採購的耗材與防護用品，使用者、決策者、付款者在工業客戶端同一條線上；Q3 訂單 +7%、積壓訂單 +18%，客戶基礎分散，無信用集中"},{"item":"決策層級","level":"🟡","text":"黏著劑與電子薄膜在客戶設計層級認證，換料要重新驗證，漲價 2% 後量仍成長；但 Novec 退出後替代流體能直接上線，說明部分品類替代成本不高"},{"item":"價值鏈分配","level":"🟡","text":"3M 在客戶物料成本中占比小，有議價空間；但在 EBO 這條新鏈上，超大規模業者要求多來源供應，3M 開放多方協議（已 63 家），又給 Amazon 約 0.6% 股權的認股權證，新價值的一部分讓給了客戶與生態系"},{"item":"社會容忍度","level":"🔴","text":"PFAS 已耗盡社會容忍度：AFFF 多區訴訟仍有個人、公共供水、州政府等原告，CERCLA 指定後可能追加調查整治，法規在美加歐亞持續收緊"}],"roiic":"事實表未涵蓋（缺投入資本口徑，無法算增量報酬）","reinvest_rate":"約 4%（推估：NOPAT ≈ FY26 共識營收 $25,429M × 調整後營益率 24.6% × (1−20%) ≈ $5.0B；調整後 FCF 約 $4.8B；差額約 $0.2B。未含 Madison 合資的淨額，3M 交出 Scott Safety 並收回 $700M 現金）","endo_ceiling":3.5,"formula_note":"再投資率很低，ROIIC 又無法計算，所以內生上界不用乘法算出，改用有機成長 >3.5% 代理。管理層自稱成長以自助為主，幾乎不靠新增資本。高報酬、低再投資的組合下，多餘現金應配回股東，3M 的做法也是如此：2025 年起累計回饋 $9.3B"}}}},"q3_growth":{"verdict":"第五年後的延伸空間中等。成長主要來自價（約 1.5–2%）加量（約 2%），EPS 另有利潤率擴張與回購兩股力量。資料中心、航太、EBO 是新曲線，但規模還小，撐不起第二條 S 曲線","reasoning":"共識三年 EPS：FY26E $8.98、FY27E $9.82、FY28E $10.56（Koyfin 快照）。基期 FY25 調整後約 $8.18，由新口徑指引 $9.10–9.15 與年增 11–12% 反推。據此三年 CAGR 約 8.9%，內生上界 3.5%，缺口約 5.4pp。缺口可歸因：營益率每年擴張約 80bp，在 25% 的基數上貢獻 EPS 約 3pp；淨回購每年約 2pp；Madison 併購 EPS 中性。合計約 5pp，基本可歸因，不依賴重估。共識營收 FY26 到 FY27 +4.6%（14 位分析師），EPS 與營收成長差約 4.3pp，未超過 5pp","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_kpi5_fy2026_guidance_manageme","f_consensus_rev_3m_fy1_pct"],"verdict_values":{"growth":{"driver_mix":"價格約 1.5–2%，量約 2%，合為有機 >3.5%；EPS 再加營益率擴張約 3pp 與淨回購約 2pp；併購（Madison）EPS 中性","runway_years":"事實表未涵蓋滲透率；成熟多品類，沒有單一滲透率可算","runway_post_y5":"🟡","endo_ceiling_basis":"有機成長 >3.5% 作內生上界代理：再投資率約 4%，ROIIC 因投入資本口徑缺而無法計算","segments":[{"item":"安全與工業","value":"Q3 有機 +7%，年初至今 +6.1%，訂單與積壓訂單雙位數成長；電氣市場（資料中心接頭）雙位數"},{"item":"運輸與電子","value":"Q3 +0.5%；消費電子約 −15%，其餘（半導體、航太、商業標示）約 +5%；積壓訂單雙位數，管理層預期 Q4 加速"},{"item":"消費（約兩成營收）","value":"Q3 持平；美國 POS +2% 以上，但數家零售商去庫存，使進貨低個位數衰退；國際中個位數成長"},{"item":"資料中心（跨分部）","value":"2026 年約 $700M，2025 年約 $550M；EBO 2026 年約 $40M，2027 年約 $80–100M"}],"decay_signals":["GAAP FCF／淨利連 2 年 <0.75（2024 年 0.15、2025 年 0.43；PFAS 付款與分拆影響，調整後轉換率約 100%）","替代技術壓縮部分品類：Novec 氟化液被直接替代，LCD 顯示膜需求萎縮"],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"資本配置以回購與股息為主軸：2025 年起累計回饋 $9.3B，年初至今 $4.4B（股息 $1.2B、回購 $3.2B）；Madison 合資 EPS 中性；三項計分只能部分確認","reasoning":"FY26 調整後 FCF 約 $4.8B；調整後淨利約 $9.125 × 515.7M 股 ≈ $4.7B，轉換率約 100%。GAAP 口徑的 FCF／淨利 2024 年 0.15、2025 年 0.43，受 PFAS 付款拖累。淨負債 $7,857M，信評 A3／BBB+／A-，循環信貸 $4.25B 未動用。上半年回購均價約 $153（2026-07-21 法說 CFO），低於現價；Q3 只回購 $200M，回購轉為看價格出手。Amazon 認股權證最多 3.2M 股（約 0.6%），分 7 年依里程碑授予。SBC 金額與近三年現金去向四分，事實表未涵蓋","fact_refs":["f_kpi3_adjusted_free_cash_flow","f_net_debt_m","f_shares_diluted_m","f_dividend_yield_ttm","f_ev_m"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":true,"passed":null,"input":"Madison Fire & Rescue 交易 $1.95B，2026-07-01 完成，3M 持 50.1%；CFO 稱 2026–27 年 EPS 中性（營業利益被利息與少數股權吃掉）；已實現報酬只有一季，無法判斷"},{"name":"buyback_yield","applicable":true,"passed":null,"input":"上半年均價約 $153，對應 FY26 指引中點 EPS $9.125，盈餘收益率約 6.0%；10 年期公債殖利率事實表未涵蓋，無法比對門檻"},{"name":"sbc_dilution","applicable":true,"passed":null,"input":"SBC 金額事實表未涵蓋；股數在淨回購下減少；Amazon 認股權證 7 年約 0.6%，年化約 0.1%"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購撐：Madison 合資 EPS 中性；股東回饋的數字已寫在判斷句"}}}},"q5_valuation":{"verdict":"現價要成立，需要調整後 EPS 每年約 9% 成長，同時守住 19 倍上下的前瞻倍數，年化報酬才到 8% 以上。我信成長，因為成長能拆到利潤率與回購；但不信倍數守得住，因為改革成熟後倍數該往 16–17 倍走","reasoning":"前瞻本益比 19.5 倍，以財報前 FY26 共識 $8.98 計；以新口徑指引中點 $9.125 計約 19.2 倍，都高於前份的約 18 倍。FY27 共識 $9.82 對應 17.8 倍。trailing 本益比 26.1 倍，在 3 個年度端點內居 97 分位；P/S、EV/S 在 4 個年度端點內居 100 分位。真正的五年分位事實表未涵蓋。PEG 以三年 CAGR 8.9% 計約 2.2，偏貴。賣方均價 $165，低於現價約 6%；JPM 10 月把目標由 $205 降到 $185，各家分布不一","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_pe_current","f_pe_percentile","f_ps_percentile","f_ev_s_percentile","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_dividend_yield_ttm","f_kpi5_fy2026_guidance_manageme"],"verdict_values":{"valuation":{"basis":"前瞻本益比（FY26 共識調整後 EPS），並以 PEG 輔助","tier":"大型多元工業","peers":{"expanded":false,"reason":"事實表只有同業利潤率，沒有同業前瞻倍數，無法做倍數對照；終端倍數改以自身五年中位約 16 倍（前份判斷記載）為錨"},"fwd_pe":19.46,"peg":2.19,"percentile_5y":null,"val_light":"🟠","val_light_derivation":"前瞻本益比 19.5 倍，高於前份約 18 倍與自身五年中位約 16 倍；PEG 約 2.2；trailing 倍數在年度端點內居 97–100 分位；五年連續分位事實表未涵蓋。綜合為偏貴但未到極端","upside_short_pct":1.5,"upside_mid_pct":25.0,"denominator_disputed":false,"denominator_note":"共識 $8.98 為財報前快照，可能部分仍是舊口徑（新口徑每年多加回約 $0.16 攤銷）；換用新口徑指引中點 $9.125，倍數差約 0.3 倍，不改結論"}}},"q6_how_wrong":{"verdict":"最可能看錯在兩處：一是 AFFF 人身傷害和解金額遠超預期，回購停擺；二是工業週期轉弱時，利潤率擴張比管理層說的更早停下","reasoning":"現價高於 250 週均線約 50%（$174.74 對 $116.58），回到 104 週均線約 −14%。26 週已漲 16.5%。2023 年 GAAP 淨利 −$6,995M，EPS −12.63，說明法律提列可以一次吃掉整年獲利。依據見反證紀錄","fact_refs":["f_price_at_dd","f_ma_w104","f_ma_w250","f_week26_return_pct","f_rsi14"],"verdict_values":{"trap":{"verdict":"🟡","label":"成長大半靠利潤率與回購，法律尾部未封頂"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":8.98,"pe":19.46,"basis":"FY2026E 共識調整後 EPS（財報前快照）÷ 判斷日股價；終端倍數同樣套在終端年的調整後 EPS"},"valuation_basis":"eps_pe","eps":{"bull":[10.0,11.0,12.1,13.2,14.3],"base":[9.85,10.6,11.35,12.1,12.85],"bear":[9.3,9.0,9.2,9.5,9.7]},"pe":{"bull":20,"base":17,"bear":14},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":1.76,"net_buyback":2.0},"second_stage":{"bull_cagr_pct":8.0,"base_cagr_pct":5.5},"max_dd":{"lo":-40,"hi":-22,"basis":"現價高於 104 週均線約 14%、高於 250 週均線約 33%；工業轉弱時回到 250 週均線，再疊加 PFAS 消息衝擊約 5–7pp，得下緣 −40%；上緣取 Bear 終點跌幅約 −22%","trigger_time":null},"basis":{"bull":"有機 4–5%、營益率每年 +100bp 往 28% 走、EBO 依 Amazon 里程碑放量、回購每年 2% 以上；倍數守在 20 倍","base":"有機約 3.5–4%、營益率每年 +60–80bp 到 FY31 約 27%、淨回購約 2%；倍數回落到 17 倍，略高於自身五年中位 16 倍","bear":"工業衰退加 AFFF 人身傷害和解，FY28 EPS 回落、回購暫停，五年後才回到約 $9.7；倍數取成長熄火到 5% 時的 14 倍"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"AFFF 多區訴訟仍有個人、公共供水、集體成員、州政府等原告；Rome／Floyd 集體訴訟待簡易判決；CERCLA 指定後可能追加調查整治；Q3 法說稱正與法院指定調解人處理人身傷害案","assumption":"PFAS 付款照既有排程，人身傷害和解金額可由 FCF 分年吸收","consequence":"若和解總額達市值 15% 以上，回購停擺，倍數降到 14 倍以下；加上工業衰退，五年後股價可能腰斬","ruling":"採納：列為唯一致命點，Bear 機率 30%；社會容忍度判紅，不給法律尾部估值折扣以外的寬容","watch":"每季 10-Q 法律附註、8-K、調解進度與新提列","evidence_refs":["major_events#1","lawsuit_class_action#0","regulatory_antitrust#1"],"fact_refs":["f_net_debt_m","f_kpi3_adjusted_free_cash_flow"]},{"view":"論點成功但股東經濟變差","evidence":"利潤率擴張的同時，新價值被分走：Madison 合資 49.9% 歸 Bain，營業利益被利息與少數股權抵掉；EBO 要多來源供應，還給 Amazon 約 0.6% 認股權證；2025 年關稅推高銷貨成本且未全額轉嫁，CFO 稱投資人日後關稅成本約 $280M","assumption":"營益率每增加 1pp，大部分都落到每股盈餘","consequence":"營益率照計畫升，但每股盈餘成長低於 8%，Base 報酬掉到年化 5% 左右","ruling":"部分採納：Base 路徑只用每年 +60–80bp，不用管理層暗示的 100bp；EBO 不進 Base","watch":"每季調整後 EPS 成長與營益率擴張的差距、少數股權損益、關稅成本揭露","evidence_refs":["reg_tariff_export#2","reg_tariff_export#4"],"fact_refs":["f_kpi1_adjusted_operating_margi","f_kpi4_adjusted_eps"]},{"view":"價格已反映太多","evidence":"前瞻本益比 19.5 倍，高於前份約 18 倍；trailing 倍數在年度端點內居 97–100 分位；同口徑財測只上調約 1%；賣方均價 $165，低於現價","assumption":"改革兌現後市場會繼續給 19 倍以上","consequence":"即使 EPS 照 Base 走，倍數回到 17 倍，年化報酬約 7%，未達 8%","ruling":"採納：不追價，等前瞻本益比回到 17 倍以下約 $155，或 FY27 指引超標","watch":"前瞻本益比、1 月 FY27 指引","evidence_refs":[],"fact_refs":["f_fwd_pe_latest","f_pe_percentile","f_price_at_dd"]},{"view":"論點失敗","evidence":"約 56% 營收在美國以外；美中貿易緊張、美歐格陵蘭爭端引發關稅疑慮；出口管制可能限制稀土取得；中國約占進出口一成，2025 年 4 月公司估未抵銷的關稅年化約 $850M","assumption":"關稅與地緣成本能靠價格與生產力完全吸收","consequence":"價格成本轉負，營益率擴張停下，H1 削弱","ruling":"部分採納：不預測關稅走向，改用公司損益指標當作吸收失敗的判定（營益率年增連 2 季 ≤0，且管理層歸因關稅）","watch":"每季價格貢獻、關稅成本揭露、調整後營益率年增","evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","geo_supply_chain#0","geo_supply_chain#1"],"fact_refs":["f_kpi1_adjusted_operating_margi"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 🟡 → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=🟡","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 170.76 → 本次 174.74（+2.3%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=170.76","side_b":"本次 price_at_dd=174.74","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 170.76 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 170.76 美元：Bull 價 234、Bear 價 126，五年期望值 +15.0%，基準年化 6.5%，不對稱比 1.7","side_b":"本次情境、股價仍用 170.76 美元：Bull 價 286、Bear 價 135.8，五年期望值 +23.3%，基準年化 5.0%，不對稱比 2.75","ruling":"先換情境、股價不動：五年期望值多 8.3 個百分點，基準年化少 1.5 個百分點。不對稱比由 1.7 變為 2.75。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變好。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 170.76 美元：五年期望值 +23.3%，基準年化 5.0%，不對稱比 2.75","side_b":"本次情境、股價 174.74 美元：五年期望值 +20.5%，基準年化 4.6%，不對稱比 2.38","ruling":"再換股價、情境不動：起點價上漲 2.3%，五年期望值少 2.8 個百分點，基準年化少 0.5 個百分點，不對稱比由 2.75 降到 2.38。合計五年期望值比前份多 5.5 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"財測上調的實際幅度","cause":"新證據","prior_field":null,"side_a":"外界摘要寫成 EPS 指引由 7 月的 $8.80–8.95 升到 $9.10–9.15","side_b":"新口徑每季加回攤銷約 $0.04；7 月區間換算新口徑為 $8.95–9.10，同口徑只上調中點 $0.10（約 1%）","ruling":"採 B 側：實質上調約 1%，Q3 的超預期大多已反映在 7 月以來共識 +3% 的修正裡；不據此上修 Base 斜率","evidence_level":"公司法說原話（2026-10-20 CFO）","settle_metric":"1 月 FY27 正式指引的同口徑成長率","if_then":["若 FY27 EPS 指引中點 ≥$10.0（新口徑）→ Bull 機率上調 5pp、重跑估值","若 FY27 EPS 指引中點 <$9.7 → 不建倉，Base 路徑下修"],"evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#1"]},{"axis":"利潤率目標有沒有上修","cause":"方法變動","prior_field":null,"side_a":"前份要求 FY27 營益率目標正式上修到 25% 以上","side_b":"本季目標改寫為新口徑 25.4%，等於舊口徑約 25% 再加回 40bp；管理層只說會超過，沒給新數字","ruling":"可調和，屬程度差異：方向成立，但沒有正式上修，不當作進場條件已達成","evidence_level":"公司法說原話（2026-10-20 CFO）","settle_metric":"1 月 FY27 營益率指引","if_then":["若 FY27 營益率指引 ≥26%（新口徑）→ 視為上修成立，重跑估值","若 FY27 營益率指引 <25.4% → H1 削弱，不建倉"],"evidence_refs":[]},{"axis":"消費業務轉正時點","cause":"新證據","prior_field":null,"side_a":"2026-07-21 法說 CEO 稱下半年消費持平到小幅成長；本季 CEO 承認原以為 Q3 會轉正","side_b":"Q3 消費持平，美國進貨低個位數衰退；本季改口 Q4 小幅轉正","ruling":"管理層對消費的判斷連兩季說早了，Q4 轉正列為可信度小測驗；消費約占兩成，不改 H2","evidence_level":"兩場法說對照","settle_metric":"Q4 消費有機成長","if_then":["若 Q4 消費仍負且 2027 年 Q1 未轉正 → H2 的消費權重歸零，管理層指引打九五折看待","若 Q4 消費轉正 → 維持原判"],"evidence_refs":["end_markets#2"]},{"axis":"中國成長方向","cause":"新證據","prior_field":null,"side_a":"2026-07-21 法說 CEO：中國 Q2 雙位數成長，上半年約 +8%","side_b":"Q3 中國衰退高個位數，主因消費電子需求疲弱","ruling":"方向相反，但屬產品組合波動，不是份額流失；併入關稅與地緣風險監測","evidence_level":"兩場法說對照","settle_metric":"Q4 與 2027 年 Q1 中國區成長","if_then":["若中國連 3 季衰退且擴及工業品 → R3 升級，Base 有機成長下修 0.5pp","若中國回到正成長 → 維持原判"],"evidence_refs":["geo_supply_chain#1"]},{"axis":"運輸與電子的加速承諾","cause":"新證據","prior_field":null,"side_a":"Q2 運輸與電子營收 +6.2%","side_b":"Q3 只 +0.5%，消費電子約 −15%；管理層以雙位數的積壓訂單擔保 Q4 再加速","ruling":"未證、監測：若 Q4 運輸與電子沒有高於 Q3，下修資料中心與半導體對 H2 的支撐權重","evidence_level":"法說原話與季報","settle_metric":"Q4 運輸與電子有機成長","if_then":["若 Q4 運輸與電子 ≤1% → H2 削弱，Bear 機率加 5pp","若 Q4 ≥4% → 維持原判"],"evidence_refs":[]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"訂單 +7%；積壓訂單 +18%，約占營收 25%；增量利潤率近 40%；Amazon 認股權證掛鉤 7 年 $6B 的光連接與資料中心銷售。19 倍買 9% EPS 成長，加 1.8% 股息，不算貴","side_b":"同口徑上調僅 1%；倍數已高於前份；Amazon 協議沒有採購承諾；PFAS 人身傷害金額未知。Base 年化報酬約 7%，未過 8%","ruling":"不可調和處在倍數，選 B 側：現價已把改革成功的大半定價，等價格或 FY27 指引其中一個先到","evidence_level":"法說、8-K 摘要、事實表倍數","settle_metric":"前瞻本益比；FY27 營益率指引","if_then":["若前瞻本益比回到 17 倍以下（約 $155）且 H1、H2 未削弱 → 首倉 2%","若股價先漲過 $190 而 FY27 指引未達 26% 營益率 → 不追"],"evidence_refs":[]},{"axis":"前份漂移：估值結論","cause":"價格變動","prior_field":["val"],"side_a":"前份 🟠：股價 $170.76，前瞻本益比約 18 倍","side_b":"本次維持 🟠：股價 $174.74，前瞻本益比 19.5 倍（共識）／約 19.2 倍（新口徑指引中點）","ruling":"股價上漲與 EPS 上修大致抵銷，倍數略升，結論不變","evidence_level":"事實表價格與共識","settle_metric":"前瞻本益比","if_then":["若前瞻本益比回到 17 倍以下 → 估值結論改為偏中性"],"evidence_refs":[]},{"axis":"前份漂移：機率與回撤範圍","cause":"方法變動","prior_field":["p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份 Bull 30%、Bear 25%，最大回撤約 −35%","side_b":"本次 Bull 25%、Bear 30%，最大回撤 −22%～−40%","ruling":"共識三年 EPS 成長 8.9% 超過內生上界 3.5%，依規則 Bear 至少 30%；回撤改用與 250 週均線的距離加法律消息衝擊推出範圍，不用單點","evidence_level":"本次情境推導","settle_metric":"無","if_then":["若 PFAS 人身傷害和解金額落定且低於 $5B → Bear 機率回到 25%"],"evidence_refs":[]},{"axis":"前份漂移：基本面判讀各欄","cause":"新證據","prior_field":["signal","trap","moat_trend","runway_post_y5","archetype","cycle_position"],"side_a":"前份：訊號 B、價值陷阱 🟡、護城河持平、延伸空間中等、品質複利成長、無循環定位、觀望","side_b":"Q3 新證據（毛利率 +230bp、訂單 +7%、新品活力指數十幾%、Amazon 合作）強化執行面；但同口徑財測只上調 1%、PFAS 調解進行中，各欄維持。裁決與角色交由程式依本次輸入重算","ruling":"維持原判：新證據多在執行面，沒有翻轉護城河方向、延伸空間或陷阱判斷","evidence_level":"法說與季報","settle_metric":"1 月 FY27 指引","if_then":["若 FY27 營益率指引 ≥26% 且有機 ≥4% → 護城河定價面改判擴大、重跑"],"evidence_refs":[]},{"axis":"進場首倉條件改寫","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"回檔 $150-155（Fwd PE ~16x，5Y 中位）或 FY27 OM 目標正式上修（現 24.9% 已達 ~25%，上修將重評 FY27/28 EPS）；或回測 W52 $157","side_b":"前瞻本益比（新口徑全年指引中點）≤17 倍，約 $155；或 1 月 FY27 指引營益率 ≥26% 且有機 ≥4%；觸發即重跑估值、首倉 2%","ruling":"估值 rearm 的首倉門檻改寫。EPS 改用新口徑後，同一價位對應的倍數變了：$155 由前份的約 16 倍改成約 17 倍。FY27 營益率條件由「正式上修」改為具體的 26%，因為本季的目標只是改口徑。52 週均線條件退休，因均線已升到 $160.67，與估值錨重疊。風險項的倍數門檻也由 16 倍改為 17 倍，理由相同","evidence_level":"法說原話與事實表","settle_metric":"前瞻本益比；FY27 指引","if_then":["若觸發 → 首倉 2%，加碼要等 FY27 第一季營益率年增 ≥50bp"],"evidence_refs":[]},{"axis":"唯一致命點新設","cause":"新證據","prior_field":["single_thing"],"side_a":"前份未設 Single Thing（null）","side_b":"AFFF 人身傷害 MDL 以總額 ≥$13.5B（約市值 15%）和解，或首批判決大幅不利","ruling":"Q3 法說首次明講與法院指定調解人處理人身傷害案，金額成為最大的單一敏感項，新設 Single Thing；觸發即清倉或不建倉","evidence_level":"法說原話（2026-10-20 CEO）與 10-K 法律附註","settle_metric":"和解總額與付款年期","if_then":["若和解 ≥$13.5B → 清倉／不建倉","若和解 <$5B 且分 10 年以上付款 → Bear 機率降 5pp"],"evidence_refs":["major_events#1","lawsuit_class_action#0"]},{"axis":"撤退指標新設","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設量化撤退指標（null）","side_b":"新設四條：有機成長連 2 季 <2%、營益率年增連 2 季 ≤0、AFFF 和解 ≥$13.5B、FY27 調整後 FCF <$4.3B；觸發即減碼或清倉","ruling":"補齊前份缺口；前份 R1 的有機成長門檻、R3 的法律求償門檻都保留，並量化成上面的數字","evidence_level":"本次判斷","settle_metric":"各季季報","if_then":["任一條觸發 → 減碼一半；和解條件觸發 → 清倉"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"FY27 正式指引的營益率與有機成長","type":"假設驗證","maps_to":"H1","metric":"FY27 調整後營益率指引（新口徑）","threshold":"≥26% 且有機 ≥4%","action":"達標 → 重跑估值、首倉 2%；營益率 <25.4% → H1 削弱、不建倉","source_freq":"Q4 財報（年一次）","date":"2027-01","evidence_refs":[]},{"n":2,"text":"季度有機成長與訂單","type":"假設驗證","maps_to":"H2","metric":"季度有機成長、訂單年增","threshold":"有機 <2% 連 2 季，或訂單年增轉負","action":"減碼一半（若持有）；未持有則 Bear 機率加 5pp","source_freq":"每季財報","date":null,"evidence_refs":["end_markets#2"]},{"n":3,"text":"AFFF 人身傷害 MDL 和解或判決金額","type":"Single Thing","maps_to":"R2","metric":"和解總額","threshold":"≥$13.5B（約市值 15%）","action":"清倉／不建倉，等付款排程確定後重跑","source_freq":"10-Q 法律附註、8-K（不定期）","date":null,"evidence_refs":["major_events#1","lawsuit_class_action#0","regulatory_antitrust#1"]},{"n":4,"text":"關稅與地緣成本吸收失敗","type":"風險","maps_to":"R3","metric":"調整後營益率年增，加上管理層的價格成本說明","threshold":"營益率年增 ≤0 連 2 季，且歸因關稅或地緣","action":"減碼一半；未持有則延後首倉","source_freq":"每季財報","date":null,"evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","geo_supply_chain#0"]},{"n":5,"text":"倍數回到合理區","type":"估值rearm","maps_to":"R4","metric":"前瞻本益比（新口徑全年指引中點）","threshold":"≤17 倍（約 $155）","action":"H1、H2 未削弱時首倉 2%","source_freq":"每日價格","date":null,"evidence_refs":[]},{"n":6,"text":"Q4 財報與 FY27 指引後複審","type":"複審日期","maps_to":"H1","metric":"整份判斷","threshold":"到期","action":"重跑整份判斷","source_freq":"一次","date":"2027-01","evidence_refs":[]}],"kill_metrics":[{"metric":"季度有機成長率","bear_threshold":"連 2 季 <2%","window":"2027 年 Q1–Q4","source":"3M 季報新聞稿","last_status":"ok"},{"metric":"調整後營業利益率年增（新口徑）","bear_threshold":"連 2 季 ≤0bp","window":"2027 年全年","source":"3M 季報新聞稿","last_status":"ok"},{"metric":"AFFF 人身傷害 MDL 和解總額","bear_threshold":"≥$13.5B（約市值 15%）","window":"至 2028-12","source":"10-Q 法律附註、8-K","last_status":"unknown"},{"metric":"調整後自由現金流","bear_threshold":"FY27 <$4.3B","window":"FY2027","source":"3M 年報與第四季新聞稿","last_status":"ok"}],"evidence_dismissed":[],"action_conditions":{"rearm_trigger":"前瞻本益比（新口徑全年指引中點）≤17 倍約 $155，或 1 月 FY27 指引營益率 ≥26% 且有機 ≥4%","exec_line":"不追；兩條件任一觸發且 H1、H2 未削弱 → 首倉 2%，FY27 第一季營益率年增 ≥50bp 再加碼到 3%","holding_cap":"未建倉；首倉 2%，上限 3%"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"前瞻本益比（新口徑全年指引中點 $9.125）回到 17 倍以下約 $155，或 1 月 FY27 指引營益率 ≥26% 且有機 ≥4%","asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null},"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":true,"basis":"capalloc_grade='C'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟠', moat_trend='→', week26=16.53, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position=None, moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":true,"basis":"signal='B', val='🟠'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":false,"basis":"signal='B', val='🟠', ma='🟡'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟠', ma='🟡'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟠', ma='🟡'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":"中期 2-5 年","requires_critic":[]},"thesis":{"H":[{"id":"H1","text":"利潤率自助擴張可延續：調整後營益率（新口徑）由 FY26 約 24.6% 升到 FY27 超過 25.4%；毛利率由接近 45% 往高 40% 區間走","2y":"FY27 調整後營益率 ≥25.6%（新口徑），FY27 EPS ≥$9.8","5y":"營益率站穩 26–28%，毛利率 ≥47%","10y":null,"threshold":"FY27 營益率 ≥25.6%；各季營益率年增 ≥50bp","source":"2026-10-20 法說 CFO：FY27 營益率會超過投資人日目標 25.4%（新口徑），增量利潤率接近 40%；CEO：毛利率四到五年內可到高 40%","drift_rule":"以近四季營益率對門檻的偏離計：連 2 季年增 <0 為削弱；連 3 季年減 ≥50bp 為反轉"},{"id":"H2","text":"有機成長維持 3.5% 以上，動力來自新品、交叉銷售與資料中心、半導體、航太，不只靠工業週期","2y":"FY27 有機 ≥3.5%，訂單年增不轉負","5y":"有機成長穿越週期站穩 3–4%，新品活力指數 ≥20%","10y":null,"threshold":"季度有機 ≥3%，訂單年增 >0","source":"2026-10-20 法說：Q3 有機 +3.3%、訂單 +7%、積壓訂單 +18%、新品活力指數十幾%，Q4 有機略高於 4%","drift_rule":"以近四季有機成長對 3.5% 計：連 2 季低於 3.3% 為削弱；連 3 季低於 3.15% 為反轉"},{"id":"H3","text":"法律尾部下現金回饋仍可持續：調整後 FCF 約 $4.8B，撐得起股息加每年 $2B 左右的回購；PFAS 付款照既有排程","2y":"2027 年底累計回饋超過 $10B，FY27 調整後 FCF ≥$4.8B","5y":"淨縮股每年 ≥1.5%，股息不降","10y":null,"threshold":"FY27 調整後 FCF ≥$4.8B；回購年額 ≥$1.5B","source":"2026-10-20 法說 CFO：2025 年起已回饋 $9.3B，FY26 調整後 FCF 約 $4.8B；Q3 10-Q：信評 A3／BBB+／A-，循環信貸未動用","drift_rule":"FCF 連 2 季年減 ≥5% 為削弱；全年 FCF 低於門檻 10% 以上或暫停回購為反轉"}],"R":[{"id":"R1","text":"工業週期轉弱，加上消費與消費電子續弱，有機成長掉回 2% 以下；Q3 消費持平、消費電子約 −15%、中國衰退高個位數","h_ref":"H2","clock":"🔥","threshold":"季度有機 <2% 連 2 季","evidence_refs":["end_markets#2"]},{"id":"R2","text":"PFAS 法律與法規尾部：AFFF 人身傷害 MDL 調解中，Rome／Floyd 集體訴訟待判，CERCLA 指定後可能追加調查整治；金額事實表未涵蓋","h_ref":"H3","clock":"🐢","threshold":"單一和解或判決 ≥$5B，或新增提列使年度 FCF 低於 $4.3B","evidence_refs":["regulatory_antitrust#1","major_events#1","lawsuit_class_action#0"]},{"id":"R3","text":"關稅與地緣：約 56% 營收在美國以外，面對美中、美歐關稅與出口管制；2025 年關稅推高銷貨成本且未全額轉嫁","h_ref":"H1","clock":"🔥","threshold":"管理層揭露價格成本轉負，且調整後營益率年增 ≤0 連 2 季","evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","reg_tariff_export#2","reg_tariff_export#4","geo_supply_chain#0","geo_supply_chain#1"]},{"id":"R4","text":"倍數回落：前瞻本益比 19.5 倍高於前份約 18 倍；若成長回到 3%、倍數回到 16–17 倍，EPS 的增長會被倍數壓縮吃掉","h_ref":"H1","clock":"🔥","threshold":"前瞻本益比跌破 17 倍，且共識 EPS 未同步上修","evidence_refs":[]}],"single_thing":{"description":"AFFF 人身傷害 MDL 以總額 ≥$13.5B（約市值 15%）和解，或首批判決大幅不利","why_fatal":"金額約等於近三年的調整後 FCF。回購是 Base 情境每年約 2pp 的 EPS 來源，會先停；尾部風險重新打開，倍數會下修到 14 倍以下","if_happens":"不建倉；若已持有則清倉，等付款排程確定後重跑","how_monitor":"每季 10-Q 法律附註、8-K、法院指定調解人的進度、新提列","probability":"15%（12–24 個月內；依據：已進入法院指定調解，金額事實表未涵蓋）"}},"appendix_a":{"growth_durability":6,"quality_score":7,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":17.79,"peg_fy2":2.0,"stress":{"pass":null,"total":null}},"eps_meta":{"base_eps_path":{"FY2025A":8.18,"FY2026E":8.98,"FY2027E":9.82,"FY2028E":10.56},"fy_end_month":12,"eps_basis":"調整後 EPS。FY2025A 由新口徑指引 $9.10–9.15 與年增 11–12% 反推，約 $8.18；FY2026E–FY2028E 為 Koyfin 共識快照，可能部分仍是舊口徑（每年約差 $0.16）"},"catalysts":[{"date":"2027-01","date_precision":"month","type":"guidance","event":"Q4 財報與 FY27 正式指引","impact":"高","watch":"營益率是否 ≥26%（新口徑）、有機是否 ≥4%"},{"date":null,"date_precision":null,"type":"regulatory","event":"AFFF 人身傷害 MDL 調解結果","impact":"高","watch":"和解總額與付款年期"},{"date":"2027-09","date_precision":"quarter","type":"product","event":"Amazon EBO 出貨爬坡（管理層稱明年下半年開始）","impact":"中","watch":"EBO 年營收是否達 $80–100M"}]}
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
