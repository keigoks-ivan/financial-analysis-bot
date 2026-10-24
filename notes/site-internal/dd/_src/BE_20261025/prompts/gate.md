你是 DD 管線 v20 的判斷層閘（gate），標的 BE（20261025）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（28 條）
- `f_kpi0_revenue_gaap`（q1_business）｜Revenue (GAAP)＝1235.8 USD m｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-22）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（8-K Ex.99.1）（numbers.latest_quarter_kpis.items[0]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-22））
  - 註記：未取得
- `f_kpi1_non_gaap_operating_incom`（q1_business）｜Non-GAAP operating income / margin＝23.1 %（營業利益 285.7 USD m）｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-22）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（8-K Ex.99.1）（numbers.latest_quarter_kpis.items[1]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-22））
  - 註記：未取得
- `f_kpi2_gaap_operating_income_ma`（q1_business）｜GAAP operating income / margin＝18.2 %（營業利益 225.4 USD m）｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-22）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（8-K Ex.99.1）（numbers.latest_quarter_kpis.items[2]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-22））
  - 註記：未取得
- `f_kpi5_non_gaap_gross_margin`（q1_business）｜Non-GAAP gross margin＝34.5 %｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-22）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（經搜尋摘要）（numbers.latest_quarter_kpis.items[5]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-22））
  - 註記：未取得
- `f_kpi6_management_guidance_fy20`（q1_business）｜Management guidance FY2026（上調）＝營收 4.4–4.6 B USD；non-GAAP 營業利益 960–1,030 USD m；non-GAAP EPS 3.10–3.40；non-GAAP 毛利率約 34% FY2026｜期間與口徑：Q3 FY2026（公告於 2026-10-22）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司 Q3 2026 新聞稿（8-K Ex.99.1）；新聞稿未載 Q4 單季指引與全年 FCF 指引（numbers.latest_quarter_kpis.items[6]，as_of Q3 FY2026（公告於 2026-10-22））
  - 註記：FY1 EPS 共識 3.25（財報後 2026-10-24 快照，來源 consensus_revision）
- `f_earnings_recency`（q1_business）｜最近一次財報日＝2026-10-22 date｜期間與口徑：2026-10-22／距今 2 個交易日｜kind：realized
  - 來源：—（numbers.earnings_recency，as_of 2026-10-22）
- `f_peer_be_gross_margin_pct`（q2_moat）｜BE 毛利率＝31.24 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.BE.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_be_operating_margin_pct`（q2_moat）｜BE 營業利益率＝11.24 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.BE.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_be_fcf_margin_pct`（q2_moat）｜BE FCF 利潤率＝20.07 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.BE.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_gev_operating_margin_pct`（q2_moat）｜GEV 營業利益率＝4.36 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.GEV.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_gev_fcf_margin_pct`（q2_moat）｜GEV FCF 利潤率＝30.07 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.GEV.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_vrt_operating_margin_pct`（q2_moat）｜VRT 營業利益率＝19.4 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.VRT.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_cmi_operating_margin_pct`（q2_moat）｜CMI 營業利益率＝11.14 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CMI.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_fcel_gross_margin_pct`（q2_moat）｜FCEL 毛利率＝-32.39 %｜期間與口徑：TTM ending 2026-07-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.FCEL.gross_margin_pct，as_of TTM ending 2026-07-31（4季加總））
- `f_peer_plug_gross_margin_pct`（q2_moat）｜PLUG 毛利率＝-18.55 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.PLUG.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝3.25 USD/share｜期間與口徑：2026-10-24／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261024.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-10-24）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝5.24 USD/share｜期間與口徑：2026-10-24／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261024.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-10-24）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝8.19 USD/share｜期間與口徑：2026-10-24／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261024.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-10-24）
- `f_consensus_rev_fy2_pct`（q5_valuation）｜FY2 共識修正＝6.07 %｜期間與口徑：2026-10-24／兩份 Koyfin 快照之間的 EPS 修正幅度（4.94 → 5.24）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261024.xlsx（numbers.consensus_revision.fy2.revision_pct，as_of 2026-10-24）
- `f_consensus_rev_fy3_pct`（q5_valuation）｜FY3 共識修正＝3.93 %｜期間與口徑：2026-10-24／兩份 Koyfin 快照之間的 EPS 修正幅度（7.88 → 8.19）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261024.xlsx（numbers.consensus_revision.fy3.revision_pct，as_of 2026-10-24）
- `f_kpi3_free_cash_flow`（q4_capital）｜Free cash flow（營業現金流減資本支出，自算）＝-180.6 USD m｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-22）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿現金流量表：營業現金流 -27.1、PP&E 購置 153.5（numbers.latest_quarter_kpis.items[3]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-22））
  - 註記：未取得
- `f_kpi4_stock_based_compensation`（q1_business）｜Stock-based compensation＝21.0 % of non-GAAP operating income（SBC 60.1 USD m；占營收 4.9%；現金流量表口徑 57.2）｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-22）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿 non-GAAP 調節表（自算占比）（numbers.latest_quarter_kpis.items[4]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-22））
  - 註記：不適用
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝193.3 USD｜期間與口徑：2026-10-23（RTH 收盤，日線 fallback）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-10-23（RTH 收盤，日線 fallback））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝59.48 x｜期間與口徑：2026-10-24／分母＝FY1 EPS 3.25，分子＝快照價 193.3｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-10-24）
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝19.93 %｜期間與口徑：2026-07-30 → 2026-10-24／FY1 共識 EPS 2.71 → 3.25（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261024.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-10-24）
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝-16.38 %｜期間與口徑：2026-10-23（RTH 收盤，日線 fallback）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-10-23（RTH 收盤，日線 fallback））
- `f_rsi14`（q5_valuation）｜RSI(14)＝33.05｜期間與口徑：2026-10-23（RTH 收盤，日線 fallback）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-10-23（RTH 收盤，日線 fallback））
- `f_ma_state`（q5_valuation）｜週線均線六態（decision_inputs.ma 必須等於此值）＝🟢｜期間與口徑：2026-10-25／timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-10-25）
  - 原文：「price 193.3 / W52 194.62 / W104 114.33 / W250 57.06 / W250 13週斜率 6.73%」

### findings_digest 中方向為負或來源衝突的條目（17 條）
- `competitive_share_entrants#1`（competitive_share_entrants｜方向 -｜狀態 ok）：FuelCell Energy 於 FY2026 Q3 簽下首份資料中心容量預留協議（德州 75MW，條款未揭露）
  - 來源：FuelCell Energy FY2026 Q3 新聞稿（as_of 2026-09-09）｜affects：moat_trend、decision_inputs.bear
- `competitive_share_entrants#2`（competitive_share_entrants｜方向 -｜狀態 ok）：Doosan 美國子公司 HyAxiom 簽下資料中心燃料電池供應合約，為其首度進入美國資料中心電力市場（磷酸型，與 Bloom 固態氧化物不同技術）
  - 來源：Hydrogen Fuel News／Doosan 資料中心策略（as_of 2026-09-02）｜affects：moat_trend
- `customer_second_source#1`（customer_second_source｜方向 -｜狀態 ok）：單一客戶占 2026 Q2 營收約 73%，且 FY2025 有 43% 客戶為經 Brookfield 合資的關聯方
  - 來源：sec-api.io：Financial analysis of Bloom Energy Q2 2026 filings（as_of 2026-10-01）｜affects：decision_inputs.bear、thesis.R
- `customer_concentration_credit#0`（customer_concentration_credit｜方向 -｜狀態 ok）：FY2025 前三大客戶占營收約 43%、13%、12%，第一大為關係人；2024 為 23%/16%/14%，2023 兩家 37%/26%。
  - 來源：SEC EDGAR 10-K FY2025 Item 1（as_of 2026-02-09）｜affects：decision_inputs.bear、thesis.R
- `customer_concentration_credit#2`（customer_concentration_credit｜方向 -｜狀態 ok）：2026 Q1 單一關係人客戶約占營收 50%，第二大約 12%（10-Q 搜尋摘要）。
  - 來源：SEC EDGAR 10-Q Q1 2026（經搜尋摘要）（as_of 2026-05-01）｜affects：decision_inputs.bear、thesis.R
- `supply_demand_durability#2`（supply_demand_durability｜方向 -｜狀態 ok）：競爭者進入：搜尋摘要稱資料中心電力短缺吸引新進者，固定式燃料電池競爭加劇；Bloom 前景取決於 AI 基建支出是否持續。
  - 來源：Motley Fool: Bloom Energy vs the grid (2026-07-31)（as_of 2026-07-31）｜affects：thesis.R、decision_inputs.bear
- `regulatory_antitrust#1`（regulatory_antitrust｜方向 -｜狀態 ok）：產業特定監管阻力為地方層級：新墨西哥州 Oracle Project Jupiter 被兩度拒絕、空氣許可待定；Bloom 因 Santa Clara 市對現場發電燃料類型的新限制而提告；俄亥俄州 Hilliard 市挑戰亞馬遜燃料電池專案。（搜尋摘要轉述，未核原文）
  - 來源：Boerse-Express／Data Center Knowledge／Edgen 搜尋結果（as_of 2026-07-18）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：10-K 風險因素：公司預期美國對鋼、鋁、銅及其衍生品課徵的 50% 關稅會對成本造成不利影響；新增關稅或他國報復性關稅可能對業務產生重大不利影響；並設有加州與德拉瓦的外貿區以遞延／避免關稅。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-09）｜affects：decision_inputs.bear、thesis.R
- `reg_tariff_export#1`（reg_tariff_export｜方向 -｜狀態 ok）：10-K 地緣風險：中美貿易緊張可能影響二、三級次組件供應商的稀土與組件取得；產品組件主要由台灣供應。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-09）｜affects：decision_inputs.bear、thesis.R
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：2026-07 下旬有股東集體訴訟，指控 Bloom 低報對中國供應鏈的依賴，特別是氧化鈧（scandium，固態氧化物燃料電池陶瓷電解質用）；賣空報告後股價下跌。
  - 來源：D&O Diary: geopolitical issues lead to securities suit against fuel cell company（as_of 2026-08-02）｜affects：decision_inputs.bear、thesis.R
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：FY2025 10-K：製造集中在少數廠房，總部與 Fremont 廠位於地震、水災等天災易發區；Fremont 擴產至 2 GW 年產能預計 2026 年底完成，風險含地緣不穩、延誤與成本超支。
  - 來源：Bloom Energy Form 10-K FY2025（as_of 2026-02-28）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#3`（geo_supply_chain｜方向 -｜狀態 ok）：第三方研究估計 Bloom 約三分之二的鈧源自中國；中國暫停的稀土出口管制預計 2026-11-10 恢復
  - 來源：longportapp Equity research (Crossroads)（as_of 2026-09-01）｜affects：decision_inputs.bear、thesis.R
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：10-K 風險因子自述：儲能、風、光、水力等替代技術的重大發展，或燃煤／油／燃燒式天然氣／核能的效率或成本改善，可能對公司造成重大不利影響；亦可能出現技術更好的新競爭者。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-09）｜affects：moat_trend、decision_inputs.bear、thesis.R
- `substitute_technology#2`（substitute_technology｜方向 -｜狀態 ok）：Simply Wall St 社群敘事：電池儲能與綠氫進展可能取代 Bloom 現行固態氧化物技術，迫使增加研發或面臨過時風險（第三方使用者意見，非公司或賣方報告）。
  - 來源：Simply Wall St community narrative（as_of 2025-08-23）｜affects：decision_inputs.bear、moat_trend
- `capital_markets_pricing#4`（capital_markets_pricing｜方向 -｜狀態 ok）：2026 年 7 月初有放空機構報告質疑公司供應鏈說法，被某媒體稱為未解決議題；$8B 2029 數字非公司指引，公司僅指引到 2026
  - 來源：Sentisense 摘要（Bloom Energy Revenue Set for Significant Growth）（as_of 2026-08-01）｜affects：thesis.R、decision_inputs.bear
- `major_events#0`（major_events｜方向 -｜狀態 ok）：Nevins v. Bloom Energy（N.D. Cal., No. 26-cv-07944）證券集體訴訟，依 Exchange Act 10(b)/20(a)，class period 2025-02-27 至 2026-07-08；起因為 2026-07-08 Hunterbrook 報告指 Bloom 依賴中國鈧，股價當日跌 5.7% 至 254.29 美元。原告方指控，尚非認定。首席原告申請截止 2026-09-28。
  - 來源：Kessler Topaz（ktmc.com）Bloom Energy Securities Fraud Class Action 通知；Law Offices of Frank R. Cruz 通知（Barchart）（as_of 2026-08-01）｜affects：thesis.R、decision_inputs.bear
- `lawsuit_class_action#0`（lawsuit_class_action｜方向 -｜狀態 ok）：Nevins v. Bloom Energy（N.D. Cal., No. 26-cv-07944）證券集體訴訟，class period 2025-02-27 至 2026-07-08，起因為 2026-07-08 Hunterbrook 報告（中國鈧依賴）；首席原告截止 2026-09-28。為原告指控。
  - 來源：Kessler Topaz（ktmc.com）Bloom Energy Securities Fraud Class Action 通知（as_of 2026-08-01）｜affects：thesis.R、decision_inputs.bear

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 8 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/BE_20261025/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":544.0,"bear_5y_price":50.4,"p_bull_pct":25,"p_bear_pct":30,"upside_5y_pct":41.5,"ev5y_pct":41.9,"irr_base_pct":7.2,"asym_ratio":2.0,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":3.25,"pe":59.48,"basis":"FY2026E 共識 non-GAAP EPS（財報後快照），為當年度口徑；終端 FY2031E 在 2031 年同樣是當年度，分母同源"},"eps":{"bull":[5.9,9.2,12.0,14.6,17.0],"base":[5.1,7.4,9.0,10.3,11.4],"bear":[4.2,4.6,4.2,3.9,3.6]},"pe":{"bull":32,"base":24,"bear":14},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0,"net_buyback":0},"second_stage":{"bull_cagr_pct":20,"base_cagr_pct":12},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### BE_Q2_2026_Earnings_Call_20260728.md
- 2026-07-28｜CFO｜guidance：CFO 上調全年營收財測至 39–42 億美元，中點較 2025 成長 100%（原話："raising our full year revenue outlook to $3.9 billion"）
- 2026-07-28｜CFO｜guidance：財測分兩層：積壓訂單轉換加上年內新訂單，並刻意保留產能給快速交付客戶（原話："Our outlook is built bottoms up in 2 layers."）
- 2026-07-28｜CFO｜guidance：全年 non-GAAP 營業利益財測上調至 8–9 億美元，中點營業利益率約 21%（原話："raising our full year non-GAAP operating income outlook"）
- 2026-07-28｜CFO｜guidance：全年 non-GAAP 稀釋 EPS 財測 2.55–2.85 美元（原話："Full year non-GAAP diluted"）
- 2026-07-28｜CFO｜guidance：CFO 說明財測口徑：季節性已改為依客戶就緒度的交付時點（原話："What was once"）
- 2026-07-28｜CFO｜margin：Q2 營收 10.65 億美元，年增 166%，首度單季破 10 億（原話："Revenue was"）
- 2026-07-28｜CFO｜margin：毛利率 34.3%，年增 604 bps；產品毛利率 37.2%（原話："Gross margin was 34.3%, up 604 basis points year-over-year."）
- 2026-07-28｜CFO｜margin：服務毛利率 22%，認列方式為按期攤銷、成本發生時入帳，電堆更換時點造成季間波動（原話："Service revenue is recognized ratably, net of guarantees"）
- 2026-07-28｜CFO｜margin：CFO 稱毛利率會逐季波動，並維持全年約 34% 的展望（原話："Blended gross margin will move quarter-to-quarter"）
- 2026-07-28｜CFO｜margin：CFO 表示若需在單季毛利與加急交付間取捨，會優先客戶（原話："we are going to prioritize the customer and"）
- 2026-07-28｜CFO｜margin：營業利益 2.4 億美元、營業利益率 22.5%；營收成長 166% 而營業費用僅增 48%（原話："Revenue grew 166%, while operating expenses grew just 48%."）
- 2026-07-28｜CFO｜margin：營運現金流 2.26 億、自由現金流 1.75 億、期末現金 27 億美元（原話："Free cash flow was $175"）
- 2026-07-28｜CFO｜commitment：CFO 承諾營業費用成長維持遠低於營收成長，帶動營業利益率擴張（原話："we expect operating expense growth to remain"）
- 2026-07-28｜CEO｜commitment：CEO 對客戶的承諾：不會成為瓶頸（原話："Bloom will not be your bottleneck."）
- 2026-07-28｜CEO｜commitment：CEO 稱將在訂單簽定前持續以 Copy Exact 增量擴充美國製造產能（原話："ahead of committed orders"）
- 2026-07-28｜CEO｜commitment：CEO 稱產能不會是限制，並對訂單簿現有及未來訂單有信心（原話："Capacity is not going to be our constraint"）
- 2026-07-28｜CEO｜commitment：CEO 稱 2026 營收財測不依賴任何單一專案（原話："not going to have any dependence on any single project"）
- 2026-07-28｜CEO｜customer：CEO 稱所有主要美國超大規模業者及十餘家新雲／AI 實驗室／託管業者已驗證核准其電力方案（原話："all the major U.S. hyperscalers and"）
- 2026-07-28｜CEO｜customer：CEO 稱 Nebius 本季取消燃氣機組訂單改選 Bloom（原話："Nebius did it"）
- 2026-07-28｜CEO｜customer：CEO 稱積壓訂單成長快於營收，且已有未列入去年底積壓的主要客戶本年出貨（原話："backlog growing at a faster pace than revenue"）
- 2026-07-28｜CFO｜customer：CFO 說明營收集中度反映交付時點而非積壓訂單組成；單季可由一兩家客戶主導（原話："that concentration reflects delivery timing"）
- 2026-07-28｜CEO｜customer：CEO 稱 2025 年所接訂單有 80% 來自重複下單客戶（原話："80% of"）
- 2026-07-28｜CEO｜customer：CEO 拒絕拆分已使用、已出貨、已簽約的客戶數（原話："We are not going to split that up"）
- 2026-07-28｜CEO｜capital_allocation：Brookfield 於 6 月將融資承諾由 50 億擴大五倍至 250 億美元（原話："Brookfield expanded its"）
- 2026-07-28｜CEO｜capital_allocation：IDF 聯手 Oaktree、MUFG、Morgan Stanley，累計承諾 26 億美元（原話："total commitment to $2.6 billion"）
- 2026-07-28｜CFO｜capital_allocation：CFO 說明交易結構：多數客戶選擇分期付款，由財務方買斷設備並持有（原話："Since most customers choose to pay over time rather than own"）
- 2026-07-28｜CFO｜capital_allocation：CFO 稱專案若延遲，終端客戶可轉移設備，財務方仍須向 Bloom 收貨（原話："the financier is on the"）
- 2026-07-28｜CFO｜capital_allocation：CFO 解釋自由現金流財測被移除，是因補充簡報中的非正式指標已與正式財測對齊（原話："And so we've"）
- 2026-07-28｜CFO｜capital_allocation：CFO 稱營業利益增額 100% 轉為營運現金流，新基準為 3.75 億美元以上（原話："think about $375 million plus as being our"）
- 2026-07-28｜CEO｜capital_allocation：CEO 稱擴產的投資回收期只要幾個月，只要有需求就持續加產能（原話："the return on investment is going to be a few months"）
- 2026-07-28｜CEO｜competition：CEO 稱資料中心領域的市占率在「90 高段」（原話："very high 90s in terms of our market share"）
- 2026-07-28｜CEO｜competition：CEO 稱客戶比較燃機、引擎與燃料電池時，重點是總成本到 token 營收，而非 LCOE（原話："not LCOE, which is just an absurd construct"）
- 2026-07-28｜CEO｜competition：CEO 稱傳統供應商的四年積壓訂單是供給受限的承認（原話："We think a 4-year backlog is not a trophy."）
- 2026-07-28｜CEO｜competition：CEO 稱現階段各種可快速供電的技術都有空間（原話："every single technology that can"）
- 2026-07-28｜CEO｜product：CEO 稱主要資料中心客戶需要 800V 直流供電、免超額建置、可選址城內外與較快取得許可（原話："Bloom's ability to provide 800-volt DC"）
- 2026-07-28｜CEO｜product：CEO 描述未來 3–4 年產品方向：現場直流發電、熱能利用、碳捕捉，做成像家電的即插即用（原話："like an appliance that you can plug in and get"）
- 2026-07-28｜CEO｜product：CEO 稱 scandium 供應：可取得量足夠，已掌握對應 25 GW 部署的能見度，且不依賴中國（原話："and we are not dependent on China."）
- 2026-07-28｜CEO｜risk：CEO 承認不確定 AI 投資是否持續加速（原話："I do not"）
- 2026-07-28｜CEO｜risk：CEO 稱 2027 年約有 30–40 GW 新 AI 資料中心容量上線，均為新建案且處於不同階段（原話："30 and 40 gigawatts of new AI data center capacity"）
- 2026-07-28｜CEO｜risk：CEO 以傑逢斯悖論回應 token 價格下降與開源模型的疑慮（原話："the total token usage will go up like"）

### 問答異常語氣（迴避／改口／保留）
- BE_Q2_2026_Earnings_Call_20260728.md｜問：Strouse 追問已通過驗證的客戶中有多少正在使用、多少在積壓或管線中｜答法：未給數字，表示由客戶自行說明，三類客戶合併不拆分
- BE_Q2_2026_Earnings_Call_20260728.md｜問：Strouse 追問產能規劃是否隨加速而擴大｜答法：未給產能時程或規模數字，改談 2027 年 30–40 GW 與設備可轉移，僅稱產能不是限制
- BE_Q2_2026_Earnings_Call_20260728.md｜問：Dendrinos 追問 Brookfield 新增 200 億美元額度的執行時程｜答法：未給時程，稱為「財務貨架」，使用速度取決於客戶採用
- BE_Q2_2026_Earnings_Call_20260728.md｜問：Arcaro 追問專案延遲的財務曝險與合約保護｜答法：不評論個別專案，以一般性合約結構回答，未量化曝險
- BE_Q2_2026_Earnings_Call_20260728.md｜問：Arcaro 追問 scandium 用量與可得供應、庫存｜答法：未給用量或庫存數字，引用部落格與 8-K，稱其餘屬專有資訊
- BE_Q2_2026_Earnings_Call_20260728.md｜問：Amicucci 追問自由現金流財測被撤除的原因｜答法：稱屬補充簡報非正式指標、已與正式財測對齊，改以營業利益轉現金流推算 3.75 億以上基準，但不給正式財測
- BE_Q2_2026_Earnings_Call_20260728.md｜問：Ocalan 追問其他燃料電池（如熔融碳酸鹽）的市占率前景｜答法：稱由對手自行說明，僅給「90 高段」市占率，未談未來 12–36 個月
- BE_Q2_2026_Earnings_Call_20260728.md｜問：Rusch 追問定價演進、目標毛利率與替代其他技術的專案數｜答法：未回答定價與目標毛利率，也未給替代專案數，改談服務毛利率轉正與重複訂單

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 3 | 3 |
| customer_second_source | found | 2 | 2 |
| customer_concentration_credit | found | 3 | 1 |
| supply_demand_durability | found | 5 | 3 |
| regulatory_antitrust | found | 3 | 3 |
| reg_tariff_export | found | 3 | 2 |
| geo_supply_chain | found | 4 | 2 |
| end_markets | found | 4 | 3 |
| substitute_technology | found | 3 | 2 |
| channel_business_model_shift | found | 3 | 2 |
| capital_markets_pricing | found | 5 | 4 |
| major_events | found | 2 | 4 |

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260905","verdict":"進場·條件式（爆發候選）","role":"衛星","H":{"status":"unavailable"},"R":{"status":"unavailable"},"single_thing":null,"kill_metrics":null,"rearm_trigger":"已在場（衛星首階）；加碼雙軌：①回檔至 FY2 前瞻本益比 ≤40x（約 $197）且論點無損；②10-K 明示 FEOC 達標＋年化產能 >2.5GW（不論價位，≤60x）","irr_base_pct":-3.8,"ev5y_pct":-9.0,"drift_watch_prior":{"dca_verdict":"進場·條件式（爆發候選）","dca_role":"衛星","signal":"B","val":"🔴","ma":"✅","trap":"🟡","moat_trend":"↑","runway_post_y5":"🟢","asym_ratio":0.96,"ev5y_pct":-9.0,"irr_base_pct":-3.8,"max_dd_pct":-86,"bull_5y_price":502.2,"bear_5y_price":35.8,"p_bull_pct":25,"p_bear_pct":30,"rearm_trigger":"已在場（衛星首階）；加碼雙軌：①回檔至 FY2 前瞻本益比 ≤40x（約 $197）且論點無損；②10-K 明示 FEOC 達標＋年化產能 >2.5GW（不論價位，≤60x）","price_at_dd":252.87,"archetype":"品質複利成長","cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"BE","date":"2026-10-25","schema":"v15.2","contract":"v19","company_name":"Bloom Energy"},"oneliner":"Bloom 以固態氧化物燃料電池吃下電網接不上電的資料中心需求，Q3 營收年增 138%、non-GAAP 營益率 23%；但單季自由現金流 −1.8 億美元、單一客戶占比過高仍未解。現價 FY2 本益比約 37 倍，等 Q4 現金流轉正再加碼","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/BE_20261025/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/BE_20261025/scenario.json","answers":{"q1_business":{"verdict":"賣現場發電設備（產品占 Q3 營收 87%）給資料中心與工商業客戶，賺的是電網接不上電、燃氣渦輪排不到貨的時間差。錢卡在「上電速度＋空氣許可」這一節點；Q3 non-GAAP 毛利率 34.5%、營益率 23.1%","reasoning":"營收分部（Q3 法說）：產品 1,070 百萬美元（87%，交付驗收即認列，毛利率 38.4%）、服務 67.6 百萬美元（毛利率 21.4%）、安裝 84.9 百萬美元（依進度認列，季間波動大）。Q3 總營收 1,235.8 百萬美元，GAAP 營益率 18.2%。全年財測年內第三度上調，營收 4.4–4.6B、non-GAAP EPS 3.10–3.40；2026-07-28 給的 3.9–4.2B 已兌現並超越，管理層財測可信度高。產業位於擴張期：AI 資料中心用電集中且急迫，燃氣渦輪大廠訂單排到 2029–30，燃料電池 55–90 天交期成為替代方案（二手說法）。供需持久度：2028 年前屬結構性，但供給可逆性中等，渦輪產能釋出後時間優勢會收窄，這一點餵給空方機率。單點依賴必答：2026 Q2 單一客戶約占營收 73%、Q1 約 50%，FY2025 前三大 43%／13%／12%，第一大為經 Brookfield 合資的關係人；多數終端客戶付電費，設備由融資方買斷持有。這是集中度風險，不是護城河證據。議價權：下游最大客戶集中度遠超 40%，上游鈧與台灣元件為瓶頸。","fact_refs":["f_kpi0_revenue_gaap","f_kpi1_non_gaap_operating_incom","f_kpi2_gaap_operating_income_ma","f_kpi5_non_gaap_gross_margin","f_kpi6_management_guidance_fy20","f_earnings_recency"],"verdict_values":{"revenue_quality":"營收以產品交付認列，依客戶場地就緒度呈塊狀；2026 Q2 單一客戶占 73%，FY2025 最大客戶為關係人；九個月營收 99% 為直接購買（含第三方購電協議），託管服務僅 1%","unit_econ_note":"Q3 產品毛利率 38.4%（年增 250bp、季增 120bp），服務毛利率 21.4%（連兩季 >20%），安裝毛利率未揭露且拖累總毛利；營業費用年增 26%、營收年增 138%，營運槓桿明顯","archetype":{"primary":"品質複利成長","secondary":"循環/商品","confidence":"低","fingerprint":"高成長、2026 年才轉為 GAAP 獲利、超大客戶集中；若 AI 資本支出轉向，行為會像循環股"},"industry":{"clock_phase":"II","sd_verdict_source":"結構性持久至 2028 前後：資料中心電網互連瓶頸與渦輪訂單排到 2029–30（二手來源）；供給可逆性中等，渦輪與其他現場發電產能釋出後時間溢價收窄","bargaining":{"up":"鈧（陶瓷電解質）與台灣元件為主要上游瓶頸，鋼鋁銅受 50% 關稅","down":"最大單一客戶 2026 Q2 占營收約 73%，且透過融資方付款，買方議價力強","geo":"第三方估鈧約三分之二源自中國，中國稀土出口管制預計 2026-11-10 恢復；元件主要由台灣供應"},"profit_pool_dir":"資料中心電力利潤池由電網與集中式電廠往現場發電移動，Bloom 目前是最大受益者","tam_table":[{"item":"積壓訂單","value":"約 200 億美元（產品 60 億、服務 140 億），2025-10 報導；Q3 法說稱成長快於營收但未給新數字"},{"item":"部署能見度","value":"公司稱對 25 GW 部署有能見度（2026 Q2 後二手摘要）"},{"item":"資料中心全現場發電占比","value":"公司 2026-04 投資人簡報：開發商預期 2030 年全現場發電資料中心占比逐次上調，約三成以上（簡報數字排版不清）"},{"item":"工商業","value":"公司自辦調查：四分之一工商設施預期 2030 年全現場供電，2035 年 35%（Q3 法說，公司自述）"},{"item":"2027 年新增 AI 資料中心容量","value":"CEO 稱約 30–40 GW 新容量上線（2026-07-28 法說）"},{"item":"利潤池占比五年變化","value":"事實表未涵蓋"}]}}},"q2_moat":{"verdict":"護城河方向向上：規模化讓產品毛利率持續擴張，定價據 CFO 稱仍強，新進者規模只有數十 MW。但機制建立在電網與渦輪短缺的時間窗口上，持續期是最大問號","reasoning":"機制：固態氧化物燃料電池不經燃燒，空氣許可較易取得；模組化可分批上電、交期以月計；Fremont 年產能 2026 年底達 2 GW、廠房可擴至約 5 GW，人力不隨產能等比增加，形成成本曲線領先。可證方向：同業 ROIC 事實表未涵蓋，改用利潤率 spread。BE TTM 營益率 11.2%，高於 GEV 4.4%、CMI 11.1%；FCEL、PLUG 毛利為負，同類燃料電池對手無力抗衡。Q3 產品毛利率 38.4%，全年毛利率指引 34%（2025 年 30%、年初指引 32%）；2026-07-28 CEO 稱資料中心市占率在「90 高段」，Nebius 取消燃氣機組改選 Bloom。執行力擴大、定價力穩定偏擴大，判為向上。產業態勢屬雙向拉鋸：結構轉好（渦輪排到 2029–30、現場發電占比預期上升、維吉尼亞州長點名非燃燒燃料電池）對上競爭者進入（FuelCell、Doosan HyAxiom）與地方許可阻力（Santa Clara、新墨西哥、俄亥俄）。當期 ROIC 無法計算：投入資本與 D&A 事實表未涵蓋。","fact_refs":["f_peer_be_gross_margin_pct","f_peer_be_operating_margin_pct","f_peer_be_fcf_margin_pct","f_peer_gev_operating_margin_pct","f_peer_gev_fcf_margin_pct","f_peer_vrt_operating_margin_pct","f_peer_cmi_operating_margin_pct","f_peer_fcel_gross_margin_pct","f_peer_plug_gross_margin_pct","f_kpi5_non_gaap_gross_margin"],"verdict_values":{"moat":{"mechanism":"不燃燒、許可快、交期以月計的模組化現場發電，加上 GW 級產能帶來的成本曲線領先","execution":8,"pricing":7,"grade":"B","trend":"↑","trend_evidence":"產品毛利率 38.4%（年增 250bp、季增 120bp）；全年毛利率指引 34%，2025 年為 30%；CFO 稱定價強、降本持續；Nebius 由燃氣改選 Bloom（2026-07-28 法說）；新進者首份資料中心合約僅 75MW","competitor_notes":[{"name":"GEV","strategy_note":"燃氣渦輪龍頭，TTM 營益率 4.4% 低於 BE，但 FCF 利潤率 30% 靠預收款；訂單排到 2029–30 是 BE 的時間窗口，產能釋出後是最大對手"},{"name":"VRT","strategy_note":"資料中心電力與散熱設備，營益率 19.4% 高於 BE 的 TTM；互補多於競爭，800V 直流架構可能是合作或交鋒點"},{"name":"CMI","strategy_note":"往復式引擎與備用發電，營益率 11.1% 與 BE 相當；燃燒式技術在排放許可上落後"},{"name":"FCEL","strategy_note":"熔融碳酸鹽燃料電池，毛利率 −32%、營益率 −88%，剛簽首份 75MW 資料中心預留協議，規模與成本差距大"},{"name":"PLUG","strategy_note":"氫燃料電池，毛利率 −19%、FCF 利潤率 −75%，財務上無力在固定式大型發電與 BE 競爭"}],"peer_na_reason":"同業 ROIC 事實表未涵蓋，改以毛利率與營益率 spread 代替","threats":[{"level":"🟡","text":"FuelCell 簽首份資料中心容量預留協議（德州 75MW），技術不同、毛利率為負，屬點對點","p":20,"evidence_refs":["competitive_share_entrants#1"]},{"level":"🟡","text":"Doosan 美國子公司 HyAxiom 以磷酸型燃料電池首度進入美國資料中心，屬點對點","p":20,"evidence_refs":["competitive_share_entrants#2"]},{"level":"🟡","text":"燃氣渦輪產能 2029–30 釋出，加上電池儲能與其他現場發電技術追上，時間溢價收窄；目前是窗口期而非新攻擊，但屬破壞性競爭，機率取 35%","p":35,"evidence_refs":["supply_demand_durability#2","substitute_technology#0","substitute_technology#2"]}],"roic_durability":{"quadrant":"高利益率×周轉未知（投入資本事實表未涵蓋）","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者是資料中心營運商，決策者是超大規模業者，付款者多為融資方（Brookfield 承諾擴至 250 億美元）；三角色都成立。需要是真的（CEO 引 NVIDIA：GW 級資料中心延後一季少 100 億美元營收），但急迫性來自電網與渦輪短缺，2029 年後是否持久未證"},{"item":"決策層級","level":"🟡","text":"替代以單一園區、單一區塊為決策單位；新案可改選渦輪或引擎（CEO 也承認各種快速供電技術都有空間），已裝機有服務合約綁定，但設備可轉移，轉換成本只在既有站點"},{"item":"價值鏈分配","level":"🟡","text":"整條鏈的價值主要落在算力營收端；Bloom 拿產品毛利 38%，融資方持有資產拿收益，最大客戶占營收七成以上，買方議價力強；上游鈧與台灣元件集中"},{"item":"社會容忍度","level":"🟡","text":"非燃燒、低水耗獲社區與州長背書；但 Santa Clara 限制現場發電燃料、新墨西哥 Project Jupiter 許可兩度被拒、俄亥俄 Hilliard 挑戰亞馬遜燃料電池案，地方許可是實際上限"}],"roiic":"事實表未涵蓋投入資本；方向證據：Q3 non-GAAP 營業利益 285.7 百萬美元（年增逾 500%），前三季資本支出僅 231 百萬美元（法說），增量報酬方向偏高，但營運資金吸收未拆分，無法給數字","reinvest_rate":"事實表未涵蓋 D&A 與營運資金變動；前三季營業現金流約 273 百萬美元（自由現金流 +42 加資本支出 231，由法說數字推得），多數被擴產與營運資金吃掉","endo_ceiling":null,"formula_note":"內生成長率＝增量 ROIC×再投資率；兩項輸入皆缺，天花板留空，情境樹按超出處理"}}}},"q3_growth":{"verdict":"五年後跑道仍寬：資料中心之外已有具名的第二曲線（AEP 為 Google 建 700MW 碳捕捉案、美國陸軍基地、公用事業表前配置），現場發電占整體用電比例仍低","reasoning":"成長主要靠量（交付 GW 數），其次是價與成本（產品毛利擴張），沒有併購與回購。共識 non-GAAP EPS FY2026 3.25、FY2027 5.24、FY2028 8.19（Koyfin 2026-10-24 快照，家數未載），FY2026→FY2028 年化約 58.7%。同期營收共識據第三方約 65 億、98 億（單位未載明），營收年化約 47%，EPS 成長比營收快約 12pp。缺口主要歸因營業利益率擴張（GAAP 營益率 FY2025 3.6% → Q3 non-GAAP 23.1%），無回購、無收購。內生天花板因投入資本缺而無法算出，共識是否在天花板內無法證明，保守視為超出。衰退信號亮 2 個：EPS 成長顯著快於營收、FCF/NI 2026 年明顯低於 0.75；長期成長性與價值陷阱風險都落在中間。第三方模型與共識對 2027–28 營收相差約 2 倍，公司未給 2027 指引。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_fy2_pct","f_consensus_rev_fy3_pct","f_kpi3_free_cash_flow"],"verdict_values":{"growth":{"driver_mix":"量為主（交付 GW 數），價與降本為輔（產品毛利擴張），無併購、無回購","runway_years":"≥10（現場發電占資料中心與工商業用電比例仍低；精確滲透率事實表未涵蓋）","runway_post_y5":"🟢","endo_ceiling_basis":"投入資本與 D&A 事實表未涵蓋，內生天花板無法算出；共識 FY2026→FY2028 EPS 年化 58.7% 是否在天花板內無法證明，保守視為超出","segments":[{"item":"產品","value":"Q3 營收 1,070 百萬美元（87%），年增 179%，毛利率 38.4%"},{"item":"服務","value":"Q3 營收 67.6 百萬美元，年增 15%，毛利率 21.4%"},{"item":"安裝","value":"Q3 營收 84.9 百萬美元，年增 29%，毛利率未揭露，拖累總毛利"}],"decay_signals":["亮：EPS 成長顯著快於營收（共識 EPS 年化約 59% 對營收約 47%）","亮：FCF/NI 偏低（Q3 自由現金流 −181 百萬美元、前三季 +42 百萬美元，遠低於淨利）","未亮：毛利率仍逐季年增","未亮：SBC 占營收 4.9%，未超過 5% 且非逐年上升","資料缺口：產業估值倍數近三年走勢、核心市占率精確值"],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"自籌擴產型：無回購、無股息、無併購，現金全數投入產能與營運資金；Q3 自由現金流 −181 百萬美元，前三季 +42 百萬美元，期末現金 25 億美元","reasoning":"現金去向：前三季資本支出 231 百萬美元，是 2025 全年的 4 倍，投在 Fremont 與 Newark 機台；營運資金因存貨、合約資產、應收增加而吸收現金；無回購與股息。SBC 單季 60.1 百萬美元，占營收 4.9%、占 non-GAAP 營業利益 21%；股數變化事實表未涵蓋，淨稀釋率無法計算。2026-07-28 CFO 稱營業利益增額 100% 轉為營運現金流、基準 3.75 億美元以上，Q3 營業現金流卻是 −27 百萬美元，承諾與實績落差列入反證。多數客戶經融資方付款，Brookfield 承諾 250 億美元、IDF 26 億美元；專案若延後，融資方仍須收貨（CFO 說法），降低交付風險，但也讓收款節奏取決於融資方。","fact_refs":["f_kpi3_free_cash_flow","f_kpi4_stock_based_compensation"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":false,"passed":null,"input":"近年無併購"},{"name":"buyback_yield","applicable":false,"passed":null,"input":"無回購"},{"name":"sbc_dilution","applicable":true,"passed":null,"input":"SBC 單季 60.1 百萬美元、占營收 4.9%；股數變化事實表未涵蓋，淨稀釋率無法計算"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購撐，無回購與股息；資本全數投入擴產與營運資金"}}}},"q5_valuation":{"verdict":"現價 193.3 美元要求 EPS 照共識在 FY2028 前成長到 8.19 美元、之後仍有雙位數成長，FY2 本益比 36.9 倍才划算。成長我大致相信，但現金轉換與客戶集中尚未驗證，基本情境五年年化約 7%，偏貴不追","reasoning":"FY1 本益比 59.5 倍（3.25 美元），FY2 36.9 倍（5.24 美元），FY3 23.6 倍（8.19 美元）。PEG 以 FY1 本益比除以 FY2026→FY2028 共識 EPS 年化 58.7%，約 1.0，落在合理區；以 FY2 計約 0.6。FY1 共識近三個月上修 19.9%，股價 26 週 −16%，本益比壓縮主要來自股價下跌加 EPS 上修。基本情境：FY2031E EPS 11.4×24 倍≈274 美元，五年 +41.5%，年化約 7%，低於 8%；機率加權終值約 274 美元，與基本情境接近。12 個月：FY2028E 基本 7.4×28 倍≈207 美元，約 +7%。同業前瞻倍數事實表未涵蓋，終端倍數無法附同業現值對照。賣方目標價全距 10–350 美元，分歧極大，自身報酬信心下調。五年分位事實表未涵蓋。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_3m_fy1_pct","f_week26_return_pct","f_rsi14","f_ma_state"],"verdict_values":{"valuation":{"basis":"前瞻本益比（FY1 與 FY2 non-GAAP EPS）","peers":{"expanded":false,"reason":"同業前瞻倍數事實表未涵蓋，只有利潤率對照"},"fwd_pe":59.48,"peg":1.01,"percentile_5y":null,"val_light":"🟠","val_light_derivation":"FY1 本益比 59.5 倍、FY2 36.9 倍；PEG（FY1）約 1.0、（FY2）約 0.6，便宜的一面被現金轉換與集中度風險抵銷；基本情境五年年化約 7%，低於 8% 門檻；五年分位事實表未涵蓋。結論為偏貴而非極貴","upside_short_pct":7.1,"upside_mid_pct":41.5,"denominator_disputed":false,"denominator_note":"分母採 non-GAAP EPS；Q3 GAAP EPS 0.78 對 non-GAAP 0.94，GAAP 口徑倍數約高兩成，SBC 屬經常性成本但不是本次爭點"}}},"q6_how_wrong":{"verdict":"價值陷阱風險中：最可能看錯在「營收長得出來、現金收不回來」，以及最大客戶一旦延後，單季營收會斷崖","reasoning":"空方最強的三點：Q3 自由現金流 −181 百萬美元，與上一季 CFO 承諾相反；單一客戶占 Q2 營收約 73%；鈧供應被指控依賴中國，有集體訴訟在身，且中國出口管制預計 11-10 恢復。三者都在一年內有數據可驗證（Q4 財報、FY2026 10-K）。股價 26 週 −16%、RSI 33，動能不過熱；高波動歷史意味深回撤要先有心理準備。","fact_refs":["f_kpi3_free_cash_flow","f_week26_return_pct","f_rsi14"],"verdict_values":{"trap":{"verdict":"🟡","label":"現金轉換與客戶集中待驗"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":3.25,"pe":59.48,"basis":"FY2026E 共識 non-GAAP EPS（財報後快照），為當年度口徑；終端 FY2031E 在 2031 年同樣是當年度，分母同源"},"eps":{"bull":[5.9,9.2,12.0,14.6,17.0],"base":[5.1,7.4,9.0,10.3,11.4],"bear":[4.2,4.6,4.2,3.9,3.6]},"pe":{"bull":32,"base":24,"bear":14},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0,"net_buyback":0},"second_stage":{"bull_cagr_pct":20,"base_cagr_pct":12},"max_dd":{"lo":-80,"hi":-55,"basis":"空方情境五年終點約 −74%（EPS 3.6×14 倍≈50 美元），下緣取 −80% 覆蓋；上緣 −55% 對應 AI 資本支出降溫但訂單未斷時的中途回檔；前份記錄歷史最大回撤 −86%，2022–2025 年 GAAP 仍虧損，股價屬高貝他，26 週已 −16%","trigger_time":null},"basis":{"bull":"資料中心訂單延續到 2029 年後，公用事業、碳捕捉、國際同時放量，產能擴到 5 GW 以上，營益率升至 25% 以上；FY2027–28 略高於共識","base":"FY2027 略低於共識（5.1 對 5.24），FY2028 7.4 低於共識 8.19：交付塊狀、毛利率持平於 34% 左右；2029 年後渦輪產能釋出，成長降到一成出頭；未計股數稀釋（事實表未涵蓋股數）","bear":"AI 資本支出放緩或最大客戶延後，加上渦輪與新進者分食，FY2028 後 EPS 回落至 4 美元以下，倍數壓到 14 倍"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"燃氣渦輪大廠訂單排到 2029–30，燃料電池短交期是替代方案；新進者（FuelCell 75MW、Doosan HyAxiom）與電池儲能等替代技術在追","assumption":"時間窗口內拿下的客戶會轉成長期服務合約與重複下單（2025 年訂單 80% 來自重複客戶，CEO 說法）","consequence":"若 AI 資本支出放緩或渦輪產能釋出，新訂單出現斷層，EPS 回到 4 美元以下、倍數壓到 14 倍，股價約 50 美元（−74%）","ruling":"採納為空方情境，機率 30%；目前沒有訂單減速的證據，CEO 稱積壓訂單成長快於營收，但拒絕給數字","watch":"2027-02 年度財測與積壓訂單、產品毛利率、競爭者 GW 級合約","evidence_refs":["supply_demand_durability#2","substitute_technology#0","competitive_share_entrants#1","competitive_share_entrants#2"],"fact_refs":["f_kpi5_non_gaap_gross_margin","f_kpi6_management_guidance_fy20"]},{"view":"論點失敗","evidence":"放空報告與集體訴訟指控低報對中國鈧的依賴；第三方估三分之二源自中國；中國稀土出口管制預計 2026-11-10 恢復；製造集中在 Fremont，位於地震帶","assumption":"2026-07-28 CEO 稱鈧可取得量足夠、對應 25 GW 部署、不依賴中國","consequence":"若鈧斷供，交付延誤、毛利率下滑，且訴訟坐實會傷及管理層可信度","ruling":"不可裁決，要等到 FY2026 10-K（2027-02）：公司說法是一手但沒給數字，第三方估計是二手；先列為短期風險","watch":"11-10 之後的交付與毛利率、10-K 對鈧來源的揭露、訴訟駁回動議","evidence_refs":["geo_supply_chain#0","geo_supply_chain#3","geo_supply_chain#1","capital_markets_pricing#4"]},{"view":"論點成功但股東經濟變差","evidence":"Q3 營業現金流 −27 百萬美元、自由現金流 −181 百萬美元，存貨、合約資產、應收增加；多數客戶經融資方分期付款；最大客戶為關係人、占 Q2 營收約 73%；SBC 占 non-GAAP 營業利益 21%","assumption":"營收成長會等比例轉成自由現金流，合約資產會隨帳單里程碑周轉","consequence":"EPS 照共識成長，但現金被營運資金與擴產吃掉，SBC 稀釋股東；大客戶議價壓住毛利，每股價值成長低於 EPS 成長","ruling":"部分採納：不追價、倉位上限下修，等 Q4 現金流驗證；年初至今自由現金流仍為正，尚不構成反轉","watch":"Q4 營業現金流、FCF/NI、合約資產周轉、10-K 客戶占比","evidence_refs":["customer_second_source#1","customer_concentration_credit#0","customer_concentration_credit#2"],"fact_refs":["f_kpi3_free_cash_flow","f_kpi4_stock_based_compensation"]},{"view":"價格已反映太多","evidence":"FY1 本益比 59.5 倍；FY1 共識三個月內上修近 20%，已把年內三次上調財測反映進去；賣方目標價 10–350 美元，分歧極大","assumption":"FY2028 EPS 達 8.19 美元，之後仍維持雙位數成長","consequence":"基本情境五年年化約 7%，即使論點成立，報酬也只是中等","ruling":"部分採納：FY2 36.9 倍不算極端，但基本報酬不足以支撐在現金未驗證前加碼","watch":"FY2 本益比、共識修正方向","evidence_refs":["capital_markets_pricing#2"],"fact_refs":["f_fwd_pe_latest","f_consensus_rev_3m_fy1_pct"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟢","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟢","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 252.87 → 本次 193.3（-23.6%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=252.87","side_b":"本次 price_at_dd=193.3","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]裁決由 dd_decision.py 機械路由：前份 進場·條件式（爆發候選） → 本次 觀望","cause":"價格變動","prior_field":["dca_verdict"],"side_a":"前份 dca_verdict=進場·條件式（爆發候選）","side_b":"本次 dca_verdict=觀望","ruling":"裁決是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。沒有單一輸入能還原，屬多欄共同：估值 🔴→🟠、均線 ✅→🟢。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]角色由 dd_decision.py 機械路由：前份 衛星 → 本次 追蹤","cause":"價格變動","prior_field":["dca_role"],"side_a":"前份 dca_role=衛星","side_b":"本次 dca_role=追蹤","ruling":"角色是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。沒有單一輸入能還原，屬多欄共同：估值 🔴→🟠、均線 ✅→🟢。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 252.87 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 252.87 美元：Bull 價 502.2、Bear 價 35.8，五年期望值 −9.0%，基準年化 −3.8%，不對稱比 0.96","side_b":"本次情境、股價仍用 252.87 美元：Bull 價 544、Bear 價 50.4，五年期望值 +8.5%，基準年化 1.6%，不對稱比 1.2","ruling":"先換情境、股價不動：五年期望值多 17.5 個百分點，基準年化多 5.4 個百分點。不對稱比由 0.96 變為 1.2。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變好。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 252.87 美元：五年期望值 +8.5%，基準年化 1.6%，不對稱比 1.2","side_b":"本次情境、股價 193.3 美元：五年期望值 +41.9%，基準年化 7.2%，不對稱比 2.05","ruling":"再換股價、情境不動：起點價下跌 23.6%，五年期望值多 33.4 個百分點，基準年化多 5.6 個百分點，不對稱比由 1.2 升到 2.05。合計五年期望值比前份多 50.9 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"現金轉換：上一季承諾與本季實績","cause":null,"prior_field":null,"side_a":"2026-07-28 CFO：營業利益增額 100% 轉為營運現金流，新基準 3.75 億美元以上；Q2 自由現金流 175 百萬美元","side_b":"2026-10-22 CFO：Q3 營業現金流 −27 百萬美元、自由現金流 −181 百萬美元，歸因存貨、合約資產、應收增加，稱「不是趨勢的開始」","ruling":"一次性說法不採信也不否定，先列為未證、持續監測；若 Q4 營業現金流仍為負，視為歸因證偽","evidence_level":"一手（兩季法說逐字稿）","settle_metric":"Q4 2026 單季營業現金流與全年自由現金流","if_then":["若 Q4 營業現金流 >0 且全年自由現金流 >0，執行加碼至 3% 上限","若 Q4 營業現金流 <0，減碼一半，凍結加碼至 FY2027 Q2"],"evidence_refs":[]},{"axis":"鈧供應是否依賴中國（不可調和）","cause":null,"prior_field":null,"side_a":"2026-07-28 CEO：鈧可取得量足夠，已掌握對應 25 GW 部署的能見度，且不依賴中國；但未給用量與庫存數字","side_b":"第三方研究估約三分之二源自中國；2026-07-08 放空報告後股價跌 5.7%，Nevins 集體訴訟指控低報依賴；中國出口管制預計 11-10 恢復","ruling":"暫採公司說法，依據是 10-K 稱至今無重大零件短缺，且公司已在法說公開否認；但訴訟仍在、數字未揭露，風險列為短期，不解除","evidence_level":"一手否認對二手估計","settle_metric":"FY2026 10-K 對鈧來源的揭露與 Q4 non-GAAP 毛利率","if_then":["若 10-K 揭露中國來源 >50%，或 11-10 後出現交付延誤，減碼一半","若 10-K 揭露替代來源且 Q4 non-GAAP 毛利率 ≥34%，解除此風險標記"],"evidence_refs":["geo_supply_chain#0","geo_supply_chain#3","capital_markets_pricing#4","major_events#0","lawsuit_class_action#0"]},{"axis":"客戶集中度","cause":null,"prior_field":null,"side_a":"2026-07-28 CEO：2026 營收財測不依賴任何單一專案；CFO：集中度反映交付時點，不代表積壓訂單組成","side_b":"2026 Q2 單一客戶約占營收 73%、Q1 約 50%、FY2025 43%（關係人）；2025 年底前三大占應收 41%／17%／15%","ruling":"可調和、屬程度差異：積壓訂單可能較分散，但營收與應收實際上高度集中，交付時點的解釋只成立一半","evidence_level":"一手（10-K、10-Q）","settle_metric":"FY2026 10-K 最大客戶占年營收","if_then":["若最大客戶占年營收 >50%，停止加碼","若降到 35% 以下且有第二曲線營收揭露，H3 進度確認"],"evidence_refs":["customer_second_source#1","customer_concentration_credit#0","customer_concentration_credit#2"]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"FY2 本益比 36.9 倍、FY2→FY3 共識 EPS 成長約 56%；前份加碼價位已到；RSI 33、26 週 −16%；年內三次上調財測全部兌現","side_b":"Q3 現金流轉負，與上一季承諾相反；單一客戶占比過高；基本情境五年年化約 7%","ruling":"暫不加碼，等 Q4 現金流；價格到位但論點有一項未驗證，現有倉位不動","evidence_level":"事實表與法說","settle_metric":"Q4 營業現金流","if_then":["Q4 現金流轉正且股價維持 FY2 本益比 ≤40 倍，加碼","股價續漲但現金流未驗證，不追"],"evidence_refs":[]},{"axis":"估值、裁決、角色與機率漂移","cause":"價格變動","prior_field":["val","p_bull_pct","p_bear_pct"],"side_a":"前份 2026-09-05：股價 252.87 美元、FY1 本益比約 93 倍（2.71 美元），估值落在最貴一級；裁決為條件式進場，角色衛星；多空機率 25／30","side_b":"本次股價 193.3 美元（−23.6%），FY1 共識上修至 3.25 美元；FY1 本益比 59.5 倍、FY2 36.9 倍，估值下修一級為偏貴；機率維持多 25、基 45、空 30；裁決與角色依新估值與新增的等待條件重新判定","ruling":"倍數下降一半來自股價、一半來自 EPS 上修，以價格變動歸類；機率不動，因為空方情境的依據（渦輪產能、集中度）沒有改變","evidence_level":"事實表","settle_metric":"FY2 本益比","if_then":["FY2 本益比回到 45 倍以上且現金流未驗證，維持不加碼"],"evidence_refs":[]},{"axis":"護城河、跑道、陷阱、訊號、公司類型","cause":"新證據","prior_field":["moat_trend","runway_post_y5","trap","signal","archetype"],"side_a":"前份：護城河向上、成長跑道寬、價值陷阱風險中、綜合訊號 B 級、公司類型為品質複利成長","side_b":"本次五項維持：Q3 產品毛利率 38.4%、財測年內第三度上調、碳捕捉與公用事業第二曲線有具名案例；但新進者首度進入資料中心、Q3 現金轉負，公司類型信心降為低","ruling":"新證據同時強化成長與暴露現金風險，方向不變、信心下調","evidence_level":"一手法說與第三方","settle_metric":"Q4 財報","if_then":["若產品毛利率連 2 季年減，護城河方向改判持平"],"evidence_refs":["competitive_share_entrants#1","competitive_share_entrants#2"]},{"axis":"回撤區間與循環位置","cause":"方法變動","prior_field":["max_dd_pct","cycle_position"],"side_a":"前份最大回撤單點 −86%，循環位置未設","side_b":"本次改為區間 −80%～−55%，由空方情境終點與高波動歷史推出；循環位置仍不設（非循環股，AI 資本支出風險放在空方情境）","ruling":"改用區間以符合現行規格，下緣仍覆蓋空方終點跌幅","evidence_level":"方法","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"加碼條件改寫（前份觸發器已發火）","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"已在場（衛星首階）；加碼雙軌：①回檔至 FY2 前瞻本益比 ≤40x（約 $197）且論點無損；②10-K 明示 FEOC 達標＋年化產能 >2.5GW（不論價位，≤60x）","side_b":"Q4 財報（2027-02）單季營業現金流轉正、FY2026 全年自由現金流為正，且股價維持 FY2 本益比 ≤40 倍（約 210 美元）以內；前份第②軌保留","ruling":"前份第①軌的價格條件已發火（FY2 本益比 36.9 倍、股價 193.3 美元低於 197 美元），但「論點無損」不成立：Q3 現金流與上一季承諾相反，所以加碼暫緩，改把現金流列為必要條件；第②軌外國關注實體規定資料事實表未涵蓋，保留不退休","evidence_level":"事實表與法說","settle_metric":"Q4 營業現金流","if_then":["條件成立，加碼至 3% 上限","Q4 營業現金流為負，減碼一半"],"evidence_refs":[]},{"axis":"Single Thing 新設","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設定唯一致命點","side_b":"最大關係人客戶（經 Brookfield 合資的融資體系）宣布延後或縮減 GW 級部署","ruling":"單一客戶占 Q2 營收約 73%，是數學上最大的單一敏感度，故設為唯一致命點","evidence_level":"一手（10-Q）","settle_metric":"10-Q 客戶占比與客戶公告","if_then":["延後 ≥2 季或縮減 ≥30%，清倉"],"evidence_refs":["customer_second_source#1"]},{"axis":"清倉與減碼門檻新設","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設定清倉門檻","side_b":"non-GAAP 毛利率連 2 季 <31% 清倉；全年自由現金流 <0 減碼；FY2027 營收指引年增 <25% 減碼；最大客戶占年營收 >50% 停止加碼","ruling":"補上可監測的數字門檻，取代前份只有加碼條件、沒有退出條件的缺口","evidence_level":"方法","settle_metric":"季報新聞稿與 10-K","if_then":["任一減碼門檻觸發，減碼一半","毛利率門檻觸發，清倉"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"FY2027 財測是否支撐需求延續","type":"假設驗證","maps_to":"H1","metric":"FY2027 營收指引中點年增率","threshold":"≥30%","action":"達標維持；<25% 減碼一半","source_freq":"Q4 財報，年一次","date":"2027-02","evidence_refs":[]},{"n":2,"text":"Q4 現金流驗證上一季承諾","type":"減碼","maps_to":"R1","metric":"Q4 單季營業現金流與 FY2026 全年自由現金流","threshold":"單季營業現金流 <0 或全年自由現金流 <0","action":"減碼一半，凍結加碼至 FY2027 Q2","source_freq":"季報","date":"2027-02","evidence_refs":[]},{"n":3,"text":"最大客戶延後或縮減 GW 級部署","type":"Single Thing","maps_to":"R2","metric":"公司或客戶揭露的部署時程","threshold":"延後 ≥2 季或縮減 ≥30%","action":"清倉","source_freq":"每季 10-Q 與新聞稿","date":null,"evidence_refs":["customer_second_source#1","customer_concentration_credit#2"]},{"n":4,"text":"中國稀土出口管制恢復後的鈧供應","type":"風險","maps_to":"R3","metric":"交付延誤揭露、non-GAAP 毛利率","threshold":"揭露鈧短缺或交付延誤，或毛利率因材料成本降至 32% 以下","action":"減碼一半","source_freq":"季報與公司公告","date":"2026-11-10","evidence_refs":["geo_supply_chain#3","geo_supply_chain#0"]},{"n":5,"text":"現金流轉正後執行加碼","type":"估值rearm","maps_to":"R1","metric":"Q4 營業現金流、FY2026 自由現金流、FY2 本益比","threshold":"單季營業現金流 >0、全年自由現金流 >0，且 FY2 本益比 ≤40 倍（約 210 美元）","action":"加碼至 3% 上限","source_freq":"Q4 財報","date":"2027-02","evidence_refs":[]},{"n":6,"text":"前份第二軌加碼條件保留","type":"加碼","maps_to":"H1","metric":"10-K 外國關注實體規定揭露、年化產能","threshold":"10-K 明示達標，且年化產能 >2.5GW（外國關注實體規定事實表未涵蓋，屬資料缺口）","action":"加碼至 3% 上限，FY2 本益比 ≤60 倍內不論價位","source_freq":"10-K，年一次","date":"2027-02","evidence_refs":[]},{"n":7,"text":"毛利率崩落代表定價力失守","type":"清倉","maps_to":"H2","metric":"non-GAAP 毛利率","threshold":"連 2 季 <31%","action":"清倉","source_freq":"季報","date":null,"evidence_refs":["supply_demand_durability#2","substitute_technology#0"]},{"n":8,"text":"客戶集中度惡化","type":"風險","maps_to":"R2","metric":"10-K 最大客戶占年營收、前三大占應收","threshold":"最大客戶 >50% 或前三大應收 >75%","action":"停止加碼","source_freq":"10-K，年一次","date":"2027-02","evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#2","customer_second_source#1"]},{"n":9,"text":"證券集體訴訟進度","type":"風險","maps_to":"R3","metric":"Nevins 案程序","threshold":"駁回動議被否決並進入證據開示，或 SEC 介入","action":"減碼一半；SEC 或刑事調查則清倉","source_freq":"法院文件，不定期","date":null,"evidence_refs":["major_events#0","lawsuit_class_action#0"]},{"n":10,"text":"地方許可阻力","type":"風險","maps_to":"R4","metric":"100MW 以上專案許可結果","threshold":"兩個以上專案因許可延後 ≥2 季","action":"停止加碼","source_freq":"新聞與公司揭露","date":null,"evidence_refs":["regulatory_antitrust#1"]},{"n":11,"text":"關稅與台灣供應吸收失敗","type":"風險","maps_to":"R6","metric":"non-GAAP 毛利率與公司歸因","threshold":"毛利率 <32% 且公司歸因關稅或原物料","action":"減碼一半","source_freq":"季報","date":null,"evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","geo_supply_chain#1"]},{"n":12,"text":"Q4 財報與 FY2027 財測後全面複審","type":"複審日期","maps_to":null,"metric":null,"threshold":null,"action":"重跑完整研究","source_freq":"年一次","date":"2027-02","evidence_refs":[]}],"kill_metrics":[{"metric":"non-GAAP 毛利率（季）","bear_threshold":"連 2 季 <31%","window":"FY2027 任兩季","source":"公司季報新聞稿","last_status":"ok"},{"metric":"全年自由現金流","bear_threshold":"FY2026 或 FY2027 全年 <0","window":"2027-02 年報起","source":"公司現金流量表","last_status":"warning"},{"metric":"FY2027 營收指引中點年增率","bear_threshold":"<25%","window":"2027-02 財測","source":"Q4 2026 新聞稿","last_status":"unknown"},{"metric":"最大單一客戶占年營收","bear_threshold":">50%","window":"FY2026 10-K","source":"10-K Item 1","last_status":"warning"}],"evidence_dismissed":[],"action_conditions":{"rearm_trigger":"Q4 財報（2027-02）單季營業現金流轉正、FY2026 全年自由現金流為正，且股價維持 FY2 本益比 ≤40 倍（約 210 美元）以內","exec_line":"現有首階持股不動、不加碼；加碼條件成立後加到 3% 上限；全年自由現金流為負減碼一半；毛利率連 2 季 <31% 或最大客戶延後 GW 級部署則清倉","holding_cap":"≤3%（深回撤風險，上限下修）"}},"decision_inputs":{"signal":"B","ma":"🟢","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":false,"wait_for_price":true,"wait_for_price_condition":"等 2027-02 Q4 財報確認單季營業現金流轉正、全年自由現金流為正再加碼；價格已到前份加碼區不構成理由","asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"qc48_result":"fail","qc48_note":"Bloom 的成長依據有營收實績，但 Bull 路徑沒有量價骨架。第二曲線和滲透率缺少一手來源，同類高估值能源設備股過去 5 年的報酬遠低於 Bull 隱含的每年 23%，而判斷物沒有說明本案為何不同，所以 Bull 依據目前不成立。"},"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='↑', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟢'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":true,"basis":"capalloc_grade='C'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":true,"basis":"signal='B', runway='🟢', val='🟠', moat_trend='↑', week26=-16.38, valuation_dependent=False"},{"row":"8a-QC48","condition":"row 8a 命中須經 QC-48 爆發候選 Bull 冷讀；critic 未放行（fail／not_run）→ 落 row 8","hit":true,"basis":"qc48_result='fail', 結論='Bloom 的成長依據有營收實績，但 Bull 路徑沒有量價骨架。第二曲線和滲透率缺少一手來源，同類高估值能源設備股過去 5 年的報酬遠低於 Bull 隱含的每年 23%，而判斷物沒有說明本案為何不同，所以 Bull 依據目前不成立。'"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position=None, moat='B', moat_trend='↑', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":true,"basis":"signal='B', val='🟠'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":false,"basis":"signal='B', val='🟠', ma='🟢'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟠', ma='🟢'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟠', ma='🟢'"},{"row":"QC-49","condition":"qc49_inherit_prior=False，不套用","hit":false,"basis":"qc49_inherit_prior=False"},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":"中期 2-5 年","requires_critic":[]},"thesis":{"H":[{"id":"H1","text":"AI 資料中心現場供電需求延續，FY2027 EPS 達共識九成以上","2y":"FY2027 non-GAAP EPS ≥4.7 美元、營收年增 ≥30%","5y":null,"10y":null,"threshold":"FY2027 non-GAAP EPS ≥4.7 美元（共識 5.24 美元的九成）","source":"季報新聞稿、2027-02 年度財測","drift_rule":"TTM 營收或 EPS 偏離基本路徑連 2 季 ≥5% 視為削弱，連 3 季 ≥10% 視為反轉"},{"id":"H2","text":"規模化帶來的毛利擴張可以持續，不被加急交付與新產線成本吃掉","2y":"FY2026 全年 non-GAAP 毛利率 ≥34%、FY2027 ≥33%，non-GAAP 營益率 ≥20%","5y":null,"10y":null,"threshold":"non-GAAP 毛利率年度 ≥33%、營益率 ≥20%","source":"季報新聞稿與法說","drift_rule":"TTM 毛利率低於門檻連 2 季 ≥5% 視為削弱，連 3 季 ≥10% 視為反轉"},{"id":"H3","text":"客戶與市場多元化：第二曲線（公用事業、工商業、碳捕捉、國際）讓最大客戶占比下降","2y":null,"5y":"最大單一客戶占年營收 ≤35%，且至少一條第二曲線年營收占比 >10%","10y":null,"threshold":"FY2028 前最大客戶占年營收 ≤35%（FY2025 為 43%）","source":"10-K 客戶集中度與營收分類揭露","drift_rule":"最大客戶占比 TTM 偏離目標路徑連 4 季 ≥5pp 視為削弱，連 6 季 ≥10pp 視為反轉"}],"R":[{"id":"R1","text":"現金轉換失靈：營收與利潤成長，營業現金流卻轉負，與上一季 CFO 承諾相反","h_ref":"H2","clock":"⚡","threshold":"Q4 營業現金流 <0 或 FY2026 全年自由現金流 <0","evidence_refs":[]},{"id":"R2","text":"客戶集中與關係人交易：單一客戶占 Q2 營收約 73%、Q1 約 50%，FY2025 最大客戶為 Brookfield 合資關係人","h_ref":"H3","clock":"🔥","threshold":"FY2026 最大客戶占年營收 >50% 或前三大應收 >75%","evidence_refs":["customer_second_source#1","customer_concentration_credit#0","customer_concentration_credit#2"]},{"id":"R3","text":"鈧供應與中國出口管制，加上放空報告引發的證券集體訴訟","h_ref":"H2","clock":"⚡","threshold":"揭露鈧短缺或交付延誤；訴訟進入證據開示或 SEC 介入","evidence_refs":["geo_supply_chain#0","geo_supply_chain#3","major_events#0","lawsuit_class_action#0","capital_markets_pricing#4"]},{"id":"R4","text":"地方許可阻力：Santa Clara 燃料限制、新墨西哥 Project Jupiter 空氣許可待定、俄亥俄 Hilliard 挑戰","h_ref":"H1","clock":"🔥","threshold":"兩個以上 100MW 級專案因許可延後 ≥2 季","evidence_refs":["regulatory_antitrust#1"]},{"id":"R5","text":"替代技術與新進者：渦輪產能 2029–30 釋出，FuelCell、Doosan 進入資料中心，電池儲能追上","h_ref":"H2","clock":"🐢","threshold":"產品毛利率連 2 季年減，或競爭者拿下 GW 級資料中心合約","evidence_refs":["supply_demand_durability#2","substitute_technology#0","substitute_technology#2","competitive_share_entrants#1","competitive_share_entrants#2"]},{"id":"R6","text":"關稅與供應鏈集中：鋼鋁銅 50% 關稅、元件主要來自台灣、製造集中在 Fremont","h_ref":"H2","clock":"🔥","threshold":"non-GAAP 毛利率 <32% 且公司歸因關稅或原物料","evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","geo_supply_chain#1"]}],"single_thing":{"description":"最大關係人客戶（經 Brookfield 合資的融資體系）宣布延後或縮減 GW 級部署","why_fatal":"單一客戶占 2026 Q2 營收約 73%，FY2027 共識 EPS 年增約六成大部分仰賴這批交付；產品營收在交付驗收時才認列，延後一季就直接少掉數億美元營收","if_happens":"FY2027 EPS 向空方路徑 4 美元附近靠攏，倍數同步壓縮，股價可能腰斬以上；CFO 稱融資方仍須收貨，但只能緩衝、無法抵銷","how_monitor":"10-Q 客戶占比、2027-02 積壓訂單與年度財測、Oracle 與 Brookfield 公開的資本支出與園區進度","probability":"15–20%（12–24 個月）"}},"appendix_a":{"growth_durability":7,"quality_score":6,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":36.9,"peg_fy2":0.63,"stress":{"pass":2,"total":3}},"eps_meta":{"base_eps_path":{"FY2025A":null,"FY2026E":3.25,"FY2027E":5.24,"FY2028E":8.19},"fy_end_month":12,"eps_basis":"non-GAAP 稀釋 EPS 共識（Koyfin 2026-10-24 快照）；FY2025 non-GAAP 實際值事實表未涵蓋（GAAP 為 −0.37），基期留空"},"catalysts":[{"date":"2026-11","date_precision":"month","type":"regulatory","event":"中國暫停的稀土出口管制預計 11-10 恢復，牽動鈧供應","impact":"中","watch":"公司是否揭露鈧庫存或替代來源、交付是否延誤"},{"date":"2026-12","date_precision":"month","type":"capacity","event":"Fremont 年產能擴至 2 GW 預計年底完成","impact":"中","watch":"Q4 法說是否確認完工與良率"},{"date":"2027-02","date_precision":"month","type":"guidance","event":"Q4 財報、FY2027 全年財測與積壓訂單數字","impact":"高","watch":"營業現金流、FY2027 營收年增是否 ≥30%、最大客戶占比"},{"date":null,"date_precision":null,"type":"other","event":"Nevins 證券集體訴訟駁回動議裁定","impact":"低","watch":"是否進入證據開示、有無 SEC 介入"}]}
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
