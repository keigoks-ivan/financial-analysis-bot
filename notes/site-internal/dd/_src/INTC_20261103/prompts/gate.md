你是 DD 管線 v20 的判斷層閘（gate），標的 INTC（20261103）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（50 條）
- `f_kpi0_gaap`（q1_business）｜營收（GAAP）＝16.513 USD B｜期間與口徑：Q3 FY2026（季末 2026-09-26，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 https://www.intc.com/news-events/press-releases/detail/1786/intel-reports-third-quarter-2026-financial-results（numbers.latest_quarter_kpis.items[0]，as_of Q3 FY2026（季末 2026-09-26，公告於 2026-10-29））
  - 註記：未查得
- `f_kpi1_non_gaap`（q1_business）｜Non-GAAP 營業利益率＝19.6 %｜期間與口徑：Q3 FY2026（季末 2026-09-26，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 https://www.intc.com/news-events/press-releases/detail/1786/intel-reports-third-quarter-2026-financial-results（numbers.latest_quarter_kpis.items[1]，as_of Q3 FY2026（季末 2026-09-26，公告於 2026-10-29））
  - 註記：未查得
- `f_kpi2_gaap`（q1_business）｜GAAP 營業利益率＝15.3 %｜期間與口徑：Q3 FY2026（季末 2026-09-26，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 https://www.intc.com/news-events/press-releases/detail/1786/intel-reports-third-quarter-2026-financial-results（numbers.latest_quarter_kpis.items[2]，as_of Q3 FY2026（季末 2026-09-26，公告於 2026-10-29））
  - 註記：未查得
- `f_kpi5_q4_fy2026`（q1_business）｜Q4 FY2026 指引＝營收 $15.0–16.0B；non-GAAP 毛利率 38.0%（GAAP 37.1%）；non-GAAP EPS $0.25（GAAP $0.10）｜期間與口徑：Q3 FY2026（季末 2026-09-26，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司 IR 新聞稿 https://www.intc.com/news-events/press-releases/detail/1786/intel-reports-third-quarter-2026-financial-results（numbers.latest_quarter_kpis.items[5]，as_of Q3 FY2026（季末 2026-09-26，公告於 2026-10-29））
  - 註記：未查得
- `f_kpi6_dcai_foundry_ccpg`（q1_business）｜分部營收 DCAI／Foundry／CCPG＝DCAI $7.3B（YoY +78%）；Foundry $6.7B（+58%）；CCPG $8.1B（-5%）｜期間與口徑：Q3 FY2026（季末 2026-09-26，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 https://www.intc.com/news-events/press-releases/detail/1786/intel-reports-third-quarter-2026-financial-results（numbers.latest_quarter_kpis.items[6]，as_of Q3 FY2026（季末 2026-09-26，公告於 2026-10-29））
  - 註記：未查得
- `f_earnings_recency`（q1_business）｜最近一次財報日＝2026-10-29 date｜期間與口徑：2026-10-29／距今 3 個交易日｜kind：realized
  - 來源：—（numbers.earnings_recency，as_of 2026-10-29）
- `f_peer_intc_gross_margin_pct`（q2_moat）｜INTC 毛利率＝38.73 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.INTC.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_intc_operating_margin_pct`（q2_moat）｜INTC 營業利益率＝7.95 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.INTC.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_intc_fcf_margin_pct`（q2_moat）｜INTC FCF 利潤率＝6.25 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.INTC.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_amd_gross_margin_pct`（q2_moat）｜AMD 毛利率＝53.2 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.AMD.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_amd_operating_margin_pct`（q2_moat）｜AMD 營業利益率＝15.71 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.AMD.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_amd_fcf_margin_pct`（q2_moat）｜AMD FCF 利潤率＝20.34 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.AMD.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_2330_tw_gross_margin_pct`（q2_moat）｜2330.TW 毛利率＝65.85 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.2330.TW.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_2330_tw_operating_margin_pct`（q2_moat）｜2330.TW 營業利益率＝57.98 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.2330.TW.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_2330_tw_fcf_margin_pct`（q2_moat）｜2330.TW FCF 利潤率＝29.58 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.2330.TW.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_005930_ks_gross_margin_pct`（q2_moat）｜005930.KS 毛利率＝57.48 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.005930.KS.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_005930_ks_operating_margin_pct`（q2_moat）｜005930.KS 營業利益率＝36.88 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.005930.KS.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_005930_ks_fcf_margin_pct`（q2_moat）｜005930.KS FCF 利潤率＝28.95 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.005930.KS.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_gfs_gross_margin_pct`（q2_moat）｜GFS 毛利率＝27.14 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.GFS.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_gfs_operating_margin_pct`（q2_moat）｜GFS 營業利益率＝11.59 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.GFS.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_gfs_fcf_margin_pct`（q2_moat）｜GFS FCF 利潤率＝11.47 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.GFS.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝1.48 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-10-31）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝2.1 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-10-31）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝3.2 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-10-31）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝61848.8 USD m｜期間與口徑：2026-11-03／yfinance revenue_estimate 0y 平均（45 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝69350.92 USD m｜期間與口徑：2026-11-03／yfinance revenue_estimate +1y 平均（46 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi3_adjusted_fcf`（q4_capital）｜調整後自由現金流（Adjusted FCF）＝1.639 USD B｜期間與口徑：Q3 FY2026（季末 2026-09-26，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 https://www.intc.com/news-events/press-releases/detail/1786/intel-reports-third-quarter-2026-financial-results（numbers.latest_quarter_kpis.items[3]，as_of Q3 FY2026（季末 2026-09-26，公告於 2026-10-29））
  - 註記：未查得
- `f_kpi4_sbc_non_gaap`（q4_capital）｜SBC 占 Non-GAAP 營業利益＝18.1 %｜期間與口徑：Q3 FY2026（季末 2026-09-26，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 https://www.intc.com/news-events/press-releases/detail/1786/intel-reports-third-quarter-2026-financial-results（SBC $586M；占比為自算 586/3,234；占營收 3.5%）（numbers.latest_quarter_kpis.items[4]，as_of Q3 FY2026（季末 2026-09-26，公告於 2026-10-29））
  - 註記：不適用
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝-3871.0 USD m｜期間與口徑：2026-11-03／yfinance 最新一季：總債務 50134.0、現金 54005.0（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝5315.0 m shares｜期間與口徑：2026-11-03／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝0.0 %｜期間與口徑：2026-11-03／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-11-03）
  - 註記：近365天無股息除息紀錄（可能為新掛牌配息股或已停止配息）
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝62.9 USD｜期間與口徑：2026-11-02（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-11-02（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝42.5 x｜期間與口徑：2026-10-31／分母＝FY1 EPS 1.48，分子＝快照價 62.9｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-10-31）
- `f_consensus_rev_fy1_pct`（q5_valuation）｜FY1 共識修正＝-3.9 %｜期間與口徑：2026-10-31／兩份 Koyfin 快照之間的 EPS 修正幅度（1.54 → 1.48）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.fy1.revision_pct，as_of 2026-10-31）
- `f_consensus_rev_fy2_pct`（q5_valuation）｜FY2 共識修正＝-3.67 %｜期間與口徑：2026-10-31／兩份 Koyfin 快照之間的 EPS 修正幅度（2.18 → 2.1）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.fy2.revision_pct，as_of 2026-10-31）
- `f_consensus_rev_fy3_pct`（q5_valuation）｜FY3 共識修正＝0.0 %｜期間與口徑：2026-10-31／兩份 Koyfin 快照之間的 EPS 修正幅度（3.2 → 3.2）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.fy3.revision_pct，as_of 2026-10-31）
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝-2.63 %｜期間與口徑：2026-07-30 → 2026-10-31／FY1 共識 EPS 1.52 → 1.48（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-10-31）
- `f_ps_current`（q5_valuation）｜P/S（現值）＝5.58 x｜期間與口徑：2026-11-02（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝100.0 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝5.52 x｜期間與口徑：2026-11-02（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝100.0 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ev_s_fwd`（q5_valuation）｜EV/S（EV ÷ FY1 共識營收）＝5.34 x｜期間與口徑：2026-11-03／f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）｜kind：estimate
  - 來源：—（numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_ev_m`（q5_valuation）｜目前企業價值 EV（市值＋淨負債）＝330415.91 USD m｜期間與口徑：2026-11-03／市值 334286.91 ＋ 淨負債 -3871.0｜kind：realized
  - 來源：—（numbers.capital_structure.ev_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝-34.32 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-11-02（RTH 收盤，UTC））
- `f_rsi14`（q5_valuation）｜RSI(14)＝23.99｜期間與口徑：2026-11-02（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ma_state`（q5_valuation）｜週線均線六態（decision_inputs.ma 必須等於此值）＝🟡｜期間與口徑：2026-11-03／timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）
  - 原文：「price 61.26 / W52 77.25 / W104 50.62 / W250 40.7 / W250 13週斜率 1.06%」
- `f_ma_w52`（q5_valuation）｜52 週均線＝77.25 USD｜期間與口徑：2026-11-03／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）
- `f_ma_w104`（q5_valuation）｜104 週均線＝50.62 USD｜期間與口徑：2026-11-03／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）
- `f_ma_w250`（q5_valuation）｜250 週均線＝40.7 USD｜期間與口徑：2026-11-03／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）
- `f_ma_slope_w250_pct`（q5_valuation）｜W250 13 週斜率＝1.06 %｜期間與口徑：2026-11-03／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）

### findings_digest 中方向為負或來源衝突的條目（19 條）
- `competitive_share_entrants#0`（competitive_share_entrants｜方向 -｜狀態 ok）：Mercury Research Q2 2026: Intel x86 share fell below 70% (~69.3%) for the first time since 1995; AMD record ~30.7%; AMD server share 34.5% ex-IoT (Intel 65.5%).
  - 來源：Mercury Research via CPU Market Share Q2 2026 (basic-tutorials.com)（as_of 2026-08-01）｜affects：moat_trend、decision_inputs.bear
- `competitive_share_entrants#1`（competitive_share_entrants｜方向 -｜狀態 ok）：Q1 2026: AMD EPYC took 46.2% of server x86 revenue; Intel server unit share 66.8% vs 72.8% a year earlier; ARM server unit share 17.7% vs 11.5% (UBS).
  - 來源：Tom's Hardware: AMD reaches 46% of server x86 CPU revenue（as_of 2026-05-15）｜affects：moat_trend、decision_inputs.bear
- `customer_second_source#0`（customer_second_source｜方向 -｜狀態 ok）：ByteDance 報導正開發自家 Arm 與 RISC-V 伺服器 CPU，理由含 Intel/AMD 漲價與交期變長（早期階段）
  - 來源：aiweekly.co - ByteDance designs custom Arm and RISC-V server CPUs（as_of 2026-05-29）｜affects：moat_trend、decision_inputs.bear
- `customer_concentration_credit#0`（customer_concentration_credit｜方向 -｜狀態 ok）：INTC 三大客戶合計占 2025 淨營收 43%（2024 為 45%、2023 為 40%）；預期少數客戶仍將占大宗。
  - 來源：SEC EDGAR 10-K FY2025（as_of 2026-01-23）｜affects：decision_inputs.bear、thesis.R
- `supply_demand_durability#3`（supply_demand_durability｜方向 -｜狀態 ok）：TrendForce 預估 NAND 2026 供給短缺 4–5%，2027 下半年供給位元成長將超過需求成長。
  - 來源：thefpsreview, New Report Suggests That NAND Supply Growth Could Once Again Exceed Demand in 2027（引 TrendForce）（as_of 2026-07-21）｜affects：decision_inputs.bear、triggers
- `regulatory_antitrust#0`（regulatory_antitrust｜方向 -｜狀態 ok）：MLex 報導（2026-03-03）：Intel 就歐盟長期處理器案再度向歐盟最高法院上訴；去年12月判決已將罰款由3.76億歐元降至2.37億歐元，歐盟執委會未再挑戰該判決（付費牆，未讀全文）。
  - 來源：MLex 報導（搜尋摘要轉述）（as_of 2026-03-03）｜affects：decision_inputs.bear、valuation
- `regulatory_antitrust#1`（regulatory_antitrust｜方向 -｜狀態 ok）：2026年3月美國跨黨派議員對 Intel 測試 ACM Research 晶片設備（該公司與中國及受制裁實體有關）提出國安疑慮；Intel 稱僅為測試用途、尚未量產（二手轉述）。
  - 來源：TradingKey, market movers INTC 2026-03-06（as_of 2026-03-06）｜affects：thesis.R
- `reg_tariff_export#1`（reg_tariff_export｜方向 -｜狀態 ok）：BIS 撤銷 Intel、Samsung、SK Hynix 向中國晶圓廠出口美製設備的授權，自 2026-01-01 起不得再供應新機台。
  - 來源：heise, Intel, Samsung, SK Hynix: No more US exports for Chinese fabs（as_of 2025-08-30）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#2`（reg_tariff_export｜方向 -｜狀態 ok）：Intel 於 2025-04 告知中國客戶部分 AI 晶片（Gaudi 等）出口需許可證；搜尋結果未說明 2026 年是否仍有效。
  - 來源：silicon.co.uk, Intel Tells Chinese Clients Some AI Chips To Require Licence（as_of 2025-04-01）｜affects：thesis.R
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：Intel 10-K/ARS 揭露：中國與台灣緊張升高、戰事風險上升，且許多產品依賴台灣供應商提供關鍵零組件（含各類 compute die）
  - 來源：Intel FY2025 Form 10-K / ARS (SEC)（as_of 2026-01-30）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：Intel 2026 年 10-Q 風險因素新增中東衝突、俄烏戰爭，以及含外部晶圓代工的複雜全球供應鏈
  - 來源：Intel Form 10-Q (quarter ended 2026-09-26, SEC)（as_of 2026-10-30）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#2`（geo_supply_chain｜方向 -｜狀態 ok）：Intel 10-K：美中緊張導致關稅與出口管制，中國為最大市場之一；2025 年美國管制擴大導致額外銷售減少
  - 來源：Intel FY2025 Form 10-K (SEC)（as_of 2026-01-30）｜affects：thesis.R、valuation
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：NoobFeed 報導（引 GF Securities 分析師預期）稱 Nvidia 以 Arm 架構 Vera CPU 切入企業 CPU，直接挑戰 Intel/AMD 的 x86；若成為次世代 AI 系統首選 CPU 夥伴，x86 長期壓力將加速。屬部落格級來源。
  - 來源：NoobFeed: NVIDIA Vera CPUs Signal a Massive Threat to Intel and AMD's x86 Dominance（as_of 2026-05-01）｜affects：moat_trend、decision_inputs.bear
- `substitute_technology#1`（substitute_technology｜方向 -｜狀態 ok）：Borecraft 報導：Intel 14A 後續路線取決於能否取得外部晶圓代工客戶；據稱 Intel 曾告知投資人，若無重要外部客戶與里程碑達成，可能暫停或終止 14A 及後續先進節點；14A 首次量產導入 High-NA EUV。
  - 來源：Borecraft: Intel's post-18A roadmap hangs on landing 14A foundry customers（as_of 2026-06-17）｜affects：thesis.R、decision_inputs.bear、triggers
- `capital_markets_pricing#4`（capital_markets_pricing｜方向 -｜狀態 ok）：報導稱 Intel 2026-10-29 提供 Q4 指引營收 $15–16B、non-GAAP EPS 0.25、毛利率 38%，低於分析師預期約 $17.07B／0.43，盤後股價大跌（未核實）。
  - 來源：tech-insider.org, Intel plunges 25% Q4 guidance $15-16 billion PC slump 2026（as_of 2026-10-30）｜affects：valuation、thesis.R、decision_inputs.bear
- `major_events#1`（major_events｜方向 -｜狀態 ok）：FY2025 10-K 揭露：2024 年 5 月於北加州聯邦法院提起的證券集體訴訟（涉及分部報告與內部代工模式），2025 年 7 月第二次修正訴狀被駁回並判被告勝訴，原告已上訴。
  - 來源：SEC EDGAR 10-K FY2025 財報附註（申報 2026-01-23）（as_of 2026-01-23）｜affects：decision_inputs.bear、thesis.R
- `turnaround_liquidation_floor#0`（turnaround_liquidation_floor｜方向 -｜狀態 ok）：Intel Q3 2026 10-Q：2026 年前九個月資產減損為 39 億美元非現金商譽減損（Q1 認列，與 Mobileye 相關）
  - 來源：SEC Form 10-Q FY2026 (period ending 2026-09-26)（as_of 2026-09-26）｜affects：valuation、decision_inputs.bear
- `lawsuit_class_action#0`（lawsuit_class_action｜方向 -｜狀態 ok）：證券集體訴訟（2024 年 5 月，分部報告／內部代工模式）已被駁回並判被告勝訴，原告上訴中。
  - 來源：SEC EDGAR 10-K FY2025 財報附註（as_of 2026-01-23）｜affects：decision_inputs.bear、thesis.R
- `lawsuit_class_action#1`（lawsuit_class_action｜方向 -｜狀態 ok）：Spectre／Meltdown／Downfall 消費者集體訴訟在美加仍在進行。
  - 來源：SEC EDGAR 10-K FY2025 財報附註（as_of 2026-01-23）｜affects：decision_inputs.bear

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 6 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/INTC_20261103/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":144.0,"bear_5y_price":22.1,"p_bull_pct":20,"p_bear_pct":35,"upside_5y_pct":13.0,"ev5y_pct":9.0,"irr_base_pct":2.5,"asym_ratio":1.1,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":1.48,"pe":42.5,"basis":"FY2026E 共識 non-GAAP EPS（FY1），與終端倍數同為當年度前瞻口徑；Y1–Y5 為 FY2027–FY2031"},"eps":{"bull":[2.3,3.5,4.4,5.2,6.0],"base":[1.9,2.7,3.2,3.6,3.95],"bear":[1.3,1.6,1.4,1.5,1.7]},"pe":{"bull":24,"base":18,"bear":13},"p":{"bull":20,"base":45,"bear":35},"yield_pct":{"dividend":0.0,"net_buyback":0.0},"second_stage":{"bull_cagr_pct":10,"base_cagr_pct":6},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### INTC_Q2_2026_Earnings_Call_20260723.md
- 2026-07-23｜CFO｜guidance：Q3 營收財測區間（原話："we're guiding Q3 revenue to a range of $15.8 billion"）
- 2026-07-23｜CFO｜guidance：Q3 財測中點毛利率與稅率（non-GAAP）（原話："we forecast gross margin of 42%, a tax rate of 11%"）
- 2026-07-23｜CFO｜guidance：2026 全年 PC 消費預期（原話："down low double digits percent for all of 2026"）
- 2026-07-23｜CFO｜guidance：伺服器 CPU 產業單位成長預期（原話："strong double-digit unit growth for the industry"）
- 2026-07-23｜CFO｜guidance：全年 non-GAAP 營業費用目標（原話："non-GAAP operating expenses to roughly $16.5 billion"）
- 2026-07-23｜CFO｜guidance：下季 CCPG 與 client 營收展望（原話："it's going to be kind of flattish for us"）
- 2026-07-23｜CFO｜guidance：伺服器供給線性偏向 Q3 末與 Q4（原話："near-term linearity of our supply growth is more skewed"）
- 2026-07-23｜CFO｜guidance：Q4 仍追不上需求（原話："We will be behind in the fourth quarter"）
- 2026-07-23｜CFO｜capital_allocation：2026 資本支出上調（原話："expect our CapEx to be more than $20 billion"）
- 2026-07-23｜CFO｜capital_allocation：2027 資本支出將顯著高於 2026（原話："expenditures to be significantly above the 2026 levels"）
- 2026-07-23｜CFO｜capital_allocation：2027 資本支出數字尚未定案（原話："I purposely didn't mention the number for 2027"）
- 2026-07-23｜CFO｜capital_allocation：2026 設備支出增幅（原話："We'll increase tooling in '26 by 40% relative to '25"）
- 2026-07-23｜CFO｜capital_allocation：投資稅額抵減比例（原話："getting $0.35 on the dollar back from the investment"）
- 2026-07-23｜CFO｜capital_allocation：約 100 億美元非核心資產可變現（原話："$10 billion of what I call noncore assets"）
- 2026-07-23｜CFO｜capital_allocation：可能需要資本市場融資（原話："we may need to tap the capital markets to drive some more"）
- 2026-07-23｜CFO｜capital_allocation：客戶願意共同投資（原話："our customers willing to invest with us"）
- 2026-07-23｜CFO｜commitment：14A 風險試產與 2028 量產承諾（原話："committed high-volume ramps in 2028"）
- 2026-07-23｜CEO｜commitment：14A PDK 0.9 時程（原話："0.9 for 14A is on track for October"）
- 2026-07-23｜CFO｜commitment：資本支出與客戶需求配合（原話："matching our expenditures with customer demand"）
- 2026-07-23｜CEO｜commitment：資本支出前提條件（良率、IP、客戶參與）（原話："I don't put CapEx unless I see the yield"）
- 2026-07-23｜CFO｜commitment：每季毛利率維持在 40% 以上（原話："comfortably into the 40s in every quarter"）
- 2026-07-23｜CFO｜commitment：不在客戶承諾前下注（原話："careful around making bets ahead of customer commitments"）
- 2026-07-23｜CFO｜margin：Q2 毛利率超標原因（原話："better yields, and higher ASPs due to mix and pricing"）
- 2026-07-23｜CFO｜margin：CCPG 庫存減損說明（原話："stranded inventory, we wrote that down"）
- 2026-07-23｜CFO｜margin：新產品毛利仍低於公司平均（原話："they're still below the corporate average"）
- 2026-07-23｜CFO｜margin：毛利增量落差（fall-through）區間（原話："we'd expect that to be somewhat the fall-through"）
- 2026-07-23｜CFO｜margin：Panther Lake 成本下降（原話："driven down the cost of our primary Panther"）
- 2026-07-23｜CFO｜margin：CCPG 營業利益率（原話："CCPG was $2.3 billion, 26% of revenue"）
- 2026-07-23｜CFO｜margin：晶圓代工營業虧損（原話："operating loss in Q2 was $2.1 billion and $348 million"）
- 2026-07-23｜CFO｜margin：外部晶圓代工營收（原話："External foundry revenue was $293 million in the quarter"）
- 2026-07-23｜CFO｜margin：Client 營收強勁主因為 ASP（原話："I would say it was largely ASP"）
- 2026-07-23｜CFO｜customer：AI 相關業務成長（原話："our AI-driven businesses grew greater than 70%"）
- 2026-07-23｜CEO｜customer：新增策略客戶與長期合約（原話："outlook with the additional strategic customer wins"）
- 2026-07-23｜CFO｜product：18A 產出高於目標（原話："output approximately 25% above target and up more than"）
- 2026-07-23｜CEO｜product：14A 良率與缺陷密度進度（原話："the yield for 256 SRAM and the defect density"）
- 2026-07-23｜CEO｜product：伺服器年增率（原話："year-over-year server growth was the strongest on record"）
- 2026-07-23｜CFO｜product：ASIC／客製晶片營收規模（原話："at least approaching a $2 billion run rate"）
- 2026-07-23｜CFO｜product：ASIC 營收目標規模（原話："we'll be at a $4 billion run rate for that business"）
- 2026-07-23｜CFO｜product：伺服器營收成長預期（原話："double-digit CAGR for us in terms of growth rate"）
- 2026-07-23｜CFO｜competition：CPU 對 GPU 比例（原話："we're almost in parity at this point"）
- 2026-07-23｜CEO｜competition：競爭地位自述（原話："Some areas we are still behind, but we are catching up"）
- 2026-07-23｜CFO｜risk：封裝材料與記憶體為供給瓶頸（原話："procuring all of that is also a bit of a choke point"）
- 2026-07-23｜CFO｜risk：後端投資可能拖累明年現金流（原話："That could be a drag to gross -- to cash flow next year"）

### 問答異常語氣（迴避／改口／保留）
- INTC_Q2_2026_Earnings_Call_20260723.md｜問：Rasgon：庫存減損多大？剔除後 Q3 毛利率指引是否實質下滑｜答法：先反問對方指的哪項庫存，說明為 match set 未完成而減損，未給金額，僅稱指引持平
- INTC_Q2_2026_Earnings_Call_20260723.md｜問：Arcuri：Q4 是否因產能上線而大幅成長｜答法：以只給一季指引回應，僅說供給改善會帶來提升但仍落後需求，未給數字
- INTC_Q2_2026_Earnings_Call_20260723.md｜問：Arya：外部晶圓代工客戶何時公告；明年資本支出增幅｜答法：未回答客戶公告時點；資本支出稱 2027 數字還需一到兩季才定案，只說會上升
- INTC_Q2_2026_Earnings_Call_20260723.md｜問：Moore：伺服器市占率與對 AMD、ARM 的奪回前景｜答法：未談市占數字，轉談需求強與供給限制及產品路線圖，承認部分領域仍落後
- INTC_Q2_2026_Earnings_Call_20260723.md｜問：Reitzes：競爭對手提出 2030 CPU TAM 2,200 億美元，是否認同｜答法：表明不給數字，稱無人能精準預測，只說市場會顯著成長
- INTC_Q2_2026_Earnings_Call_20260723.md｜問：Rakers：ASIC 業務年化約 12 億美元之後的成長與毛利率結構｜答法：CFO 回覆目前接近 20 億美元年化、未來 40 億美元，未回答毛利率部分

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 3 | 2 |
| customer_second_source | found | 2 | 2 |
| customer_concentration_credit | found | 2 | 2 |
| supply_demand_durability | found | 6 | 4 |
| regulatory_antitrust | found | 3 | 3 |
| reg_tariff_export | found | 3 | 2 |
| geo_supply_chain | found | 4 | 4 |
| end_markets | found | 4 | 3 |
| substitute_technology | found | 3 | 2 |
| channel_business_model_shift | found | 1 | 3 |
| capital_markets_pricing | found | 5 | 4 |
| major_events | found | 3 | 5 |
| turnaround_catalyst_timeline | found | 3 | 3 |
| turnaround_liquidation_floor | found | 3 | 3 |

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260724","verdict":"觀望","role":"追蹤","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"Intel Foundry 成為可外賣的外部代工業務（外部營收占比實質上升、至少 1 個 tier-1 14A design win 轉 commitment）","columns":{"2Y 驗證點":"FY27 外部 foundry 營收占比 ≥ 10%；≥1 個具名 tier-1（Apple/QCOM/AMD/NVDA/MSFT）公開 commit 14A wafer","5Y 驗證點":"FY28-29 14A 外部營收 ≥ $5B；≥2 個 tier-1 公開 commit","10Y 驗證點":"FY30+ 外部營收 ≥ $15B（≈ TSMC 10% 規模）","具體數字門檻":"外部占比 ≥ 10% FY27；14A ≥ 2 tier-1 FY28-29","信息來源":"Q2'26 法說（外部 $293M）+ BofA + 8-K","漂移觸發":"連 2 季外部占比未升 / 1H27 仍零具名"}},{"id":"H2","text":"財務結構性轉正（foundry breakeven、FCF 由負轉正）","columns":{"2Y 驗證點":"Foundry exit-2027 breakeven 如期；FY27 GAAP NI &gt; 0","5Y 驗證點":"FY28-29 FCF margin &gt; 8%；GAAP ROIC &gt; WACC","10Y 驗證點":"FY30+ FCF margin &gt; 15%；ROIC 穩定 &gt; WACC ~10%","具體數字門檻":"Foundry breakeven 2027；FCF 轉正 2028","信息來源":"Q2'26 法說（foundry −$2.1B 收斂）+ BofA（exit-2027）","漂移觸發":"breakeven 滑出 2027 / FCF 連 2 季無改善"}},{"id":"H3","text":"當前估值（P/B 5.5x 五年頂、Fwd PE FY26 90x）由轉機兌現支撐、不崩","columns":{"2Y 驗證點":"P/B 維持 &gt; 4x 需外部客戶落地佐證","5Y 驗證點":"倍數由「optionality premium」轉為「earnings-backed」","10Y 驗證點":"normalized ROE 回到 12%+ 支撐 P/B","具體數字門檻":"不因單一利多回檔破 P/B 3x","信息來源":"GuruFocus P/B 五年區間 0.9-5.1x","漂移觸發":"FY1/FY2 EPS 共識連 2 月下修 ≥ 5%"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"外部 foundry 客戶始終不來：客戶「等成熟良率」的觀望被證明對，14A 2028 才量產給了他們等待理由","columns":{"對應假設":"H1","時間尺度":"🔥 中期（4-6 季）","監測指標":"外部占比 / 具名 commitment 數","警戒閾值":"1H2027 前零具名 tier-1 → thesis 嚴重削弱"}},{"id":"R2","text":"伺服器份額續失於 AMD（ASP/mix 問題）：AMD 46.2% x86 伺服器營收份額 record，且 Diamond Rapids 砍 SMT、滑到 2027（Tan 自認「less competitive」）","columns":{"對應假設":"H1/H3","時間尺度":"⚡ 短期（1-2 季）","監測指標":"AMD 伺服器營收份額 / Intel 高 ASP mix","警戒閾值":"AMD &gt; 50% → DCAI 反彈為單季事件"}},{"id":"R3","text":"資本黑洞 + 治理干預：capex 再升需增資稀釋；Delaware 訴訟 + 國家股使資本配置受政治干預","columns":{"對應假設":"H2","時間尺度":"🐢 長期（2+ 年）","監測指標":"FCF TTM / 增資動作 / 訴訟進展","警戒閾值":"被迫 tap 資本市場稀釋 / 訴訟判治理瑕疵"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"首個具名 tier-1 外部客戶 14A/18A 晶圓 commitment（把 >$15B pipeline 轉成經常性營收）；或 foundry 2027 exit breakeven 如期兌現且外部營收占 foundry 比 ≥ 10%","irr_base_pct":1.9,"ev5y_pct":9.5,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"追蹤","signal":"C","val":"🔴","ma":"✅","trap":"🟡","moat_trend":"→","runway_post_y5":"🟡","asym_ratio":1.3,"ev5y_pct":9.5,"irr_base_pct":1.9,"max_dd_pct":-65.0,"bull_5y_price":180.0,"bear_5y_price":50.0,"p_bull_pct":25.0,"p_bear_pct":30.0,"rearm_trigger":"首個具名 tier-1 外部客戶 14A/18A 晶圓 commitment（把 >$15B pipeline 轉成經常性營收）；或 foundry 2027 exit breakeven 如期兌現且外部營收占 foundry 比 ≥ 10%","price_at_dd":100.23,"archetype":"轉機/特殊情境","cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"INTC","date":"2026-11-03","schema":"v15.0","contract":"v19","company_name":"Intel Corporation"},"oneliner":"伺服器 CPU 短缺讓 Intel 量價齊揚，但份額持續流向 AMD 與 ARM，2027 自由現金流仍為負且已增資 230 億美元；現價要 2028 年共識獲利全數兌現才勉強持平，先避開，等份額止跌與 14A 第二家客戶。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/INTC_20261103/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/INTC_20261103/scenario.json","answers":{"q1_business":{"verdict":"Intel 賺 PC 品牌廠與雲端業者買 x86 CPU 的錢；伺服器的錢卡在 Intel 3 晶圓與 EMIB 載板產能，PC 的錢卡在記憶體漲價吃掉終端預算，代工部門仍在虧損","reasoning":"Q3 營收 165 億美元；non-GAAP 營益率 19.6%、GAAP 15.3%，non-GAAP 毛利率 44.1%（2026-10-29 法說，CFO）。分部：DCAI 73 億美元（年增 78%，營益率 42%）、CCPG 81 億美元（年減 5%，營益率 28%）、代工 67 億美元（多為內部，外部 4.11 億美元，營業虧損 19 億美元）。Q4 指引營收 150–160 億美元、毛利率 38%、EPS 0.25，其中以色列廠事故約影響 3 億美元營收與 200 個基點毛利率。產業時鐘判 III：伺服器 CPU 與記憶體同時缺貨，Intel 與 AMD 伺服器 CPU 季漲 10–35%、中國客戶交期拉長到六個月，全產業擴產（Intel 設備訂單季增近 40%），PC 端已先進入收縮。單點依賴：前三大客戶占 2025 營收 43%，屬集中度風險而非護城河證據；上游先進有機載板是另一個單點瓶頸。","fact_refs":["f_kpi0_gaap","f_kpi1_non_gaap","f_kpi2_gaap","f_kpi5_q4_fy2026","f_kpi6_dcai_foundry_ccpg","f_earnings_recency"],"verdict_values":{"revenue_quality":"伺服器量價齊揚，但價格來自短缺（報導稱 2026Q2 伺服器 CPU 平均售價年增約 48%），屬可逆；PC 正在做客戶庫存修正，Q4 CCPG 指引季減逾 20%；外部代工 4.11 億美元含非經常性專案；GAAP 與 non-GAAP 營益率相差 4.3 個百分點（15.3% 對 19.6%）","unit_econ_note":"Intel 3 單位成本較 Q1 降約 15%、18A 降約 40%；Granite Rapids 毛利已高於公司平均，Panther Lake 仍低於；客製晶片毛利低於公司平均（2026-10-29 法說，CFO）；增量營收的毛利落差目標 40–60%","archetype":{"primary":"轉機/特殊情境","secondary":"循環/商品","confidence":"中","fingerprint":"重整第二年、GAAP 仍在低谷、伺服器短缺帶動獲利回升、以增資支應擴產、代工轉型待證"},"industry":{"clock_phase":"III","sd_verdict_source":"週期性將反轉：伺服器短缺由 AI 建置與產能不足造成，CFO 預期供給吃緊到 2027 並延續進 2028，Wolfe 認為供過於求最早 2028 年才會出現；但全產業同步擴產，TrendForce 預估 NAND 2027 下半年供給成長將超過需求，短缺定價屬可逆","bargaining":{"up":"上游議價強：先進有機載板全產業短缺，卡住 EMIB 封裝出貨（CEO 親赴日本爭取配額）；記憶體缺貨推高 PC 整機價格；許多產品的 compute die 依賴台灣供應商（10-K）","down":"下游集中：前三大客戶占 2025 營收 43%、占應收帳款 47%（⚑單點依賴＝集中度風險）；短缺期 Intel 能漲價，短缺結束後議價權回到客戶，且超大雲端已在自研或改用 ARM","geo":"中國是最大市場之一，美國出口管制已造成銷售減少；身為美國唯一先進製程代工帶來政策支持；中台緊張與台灣供應依賴是雙向風險"},"profit_pool_dir":"流出：x86 份額流向 AMD，伺服器架構流向 ARM 與客戶自研；先進製程代工利潤集中在台積電（營益率 58%），Intel 代工仍虧損。五年營業利益池占比變化事實表未涵蓋","tam_table":[{"item":"伺服器 CPU 市場規模（管理層估）","value":"目前約 400 億美元，5 年內可能到 2,000 億美元以上（CEO，2026-10-29 法說；未經第三方證實）"},{"item":"產業伺服器 CPU 出貨量","value":"2026、2027 年各成長 30% 以上，供給足夠會更高（CFO，2026-10-29）"},{"item":"PC 出貨量","value":"2026 年約 −12%（下半年 −20% 以上），2027 年約 −10%（CFO，2026-10-29）"},{"item":"x86 份額（Mercury 2026Q2）","value":"Intel 約 69.3%、AMD 約 30.7%；伺服器（不含 IoT）Intel 65.5%、AMD 34.5%"},{"item":"伺服器營收與出貨份額（2026Q1）","value":"AMD EPYC 占 x86 伺服器營收 46.2%；Intel 伺服器出貨份額 66.8%（一年前 72.8%）；ARM 伺服器出貨份額 17.7%（一年前 11.5%）"},{"item":"全球半導體市場（WSTS）","value":"2026 年約 1.51 兆美元、2027 年約 1.9 兆美元，主要由記憶體帶動"},{"item":"營業利益池占比五年變化","value":"事實表未涵蓋，無法計算五年淨流出"}]}}},"q2_moat":{"verdict":"護城河走弱：x86 相容性仍是主要機制，但份額持續流向 AMD 與 ARM，等級 C、方向向下","reasoning":"機制是 x86 的軟體相容與既有部署，加上美國唯一先進製程代工與 EMIB 封裝。方向用份額證明：Mercury 2026Q2 Intel x86 份額 69.3%，1995 年後首度低於七成；伺服器出貨份額由一年前 72.8% 降到 66.8%，同期 ARM 由 11.5% 升到 17.7%，AMD 伺服器營收份額 46.2%。對最強同業的利潤差距：毛利率 38.7% 對 AMD 53.2%（−14.5 個百分點）、營益率 7.95% 對 15.71%（−7.8）、FCF 利潤率 6.25% 對 20.34%（−14.1）；對台積電營益率差 50 個百分點。同業 ROIC 事實表未涵蓋，以利潤率代替；只有單期數字，看不出差距在擴大或收斂，這是本結論可能錯的地方：Intel 自身營益率已由 FY2025 −0.04% 回到 TTM 7.95%，若差距實際在收斂，方向可能只是持平。評分：執行力 6（18A 良率雙位數改善、連八季優於指引，但供給跟不上、以色列廠事故），定價力 6（短缺下漲價成功，但客戶用自研與換架構分流）；ARM 生態攻擊扣 1 分，合計約 5，等級 C。當期 ROIC 個位數低段，屬低利益率×低周轉。","fact_refs":["f_peer_intc_gross_margin_pct","f_peer_intc_operating_margin_pct","f_peer_intc_fcf_margin_pct","f_peer_amd_gross_margin_pct","f_peer_amd_operating_margin_pct","f_peer_amd_fcf_margin_pct","f_peer_2330_tw_gross_margin_pct","f_peer_2330_tw_operating_margin_pct","f_peer_2330_tw_fcf_margin_pct","f_peer_005930_ks_gross_margin_pct","f_peer_005930_ks_operating_margin_pct","f_peer_005930_ks_fcf_margin_pct","f_peer_gfs_gross_margin_pct","f_peer_gfs_operating_margin_pct","f_peer_gfs_fcf_margin_pct"],"verdict_values":{"moat":{"mechanism":"x86 指令集的軟體相容與既有部署（伺服器與 PC 主流架構），加上美國唯一先進製程代工與 EMIB 先進封裝","execution":6,"pricing":6,"grade":"C","trend":"↓","trend_evidence":"執行力擴大（18A 良率雙位數改善、Intel 3 成本較 Q1 降約 15%、18A 降約 40%），定價力縮減（漲價靠短缺，伺服器出貨份額一年少 6 個百分點、ARM 多 6 個百分點、客戶自研分流）。份額是可量測的結果，成本改善尚未轉成份額，取向下","competitor_notes":[{"name":"AMD","strategy_note":"同為 x86 的點對點競爭者，伺服器營收份額已達 46.2%，毛利率 53.2% 高出 Intel 14.5 個百分點；法說中分析師提及 AMD 指引營收成長 70%，供給彈性看起來比 Intel 大"},{"name":"2330.TW","strategy_note":"先進製程代工利潤池的主導者，營益率 58%、FCF 利潤率 30%；Intel 代工每季仍虧約 19 億美元、外部營收 4.11 億美元，兩者不在同一量級"},{"name":"005930.KS","strategy_note":"法說稱全球僅三家先進製程代工廠，三星為其一；TTM 營益率 36.9% 主要受記憶體週期帶動，代工分部數字事實表未拆"},{"name":"GFS","strategy_note":"成熟製程代工，毛利率 27%、營益率 12%，代表不做先進製程的代工報酬水準，可當 Intel 代工轉正後的保守參照"}],"spread_notes":{"對AMD":"毛利率 −14.5、營益率 −7.8、FCF 利潤率 −14.1 個百分點（Intel TTM 至 2026-09，AMD TTM 至 2026-06）","對台積電":"營益率 −50.0 個百分點","趨勢":"只有單期 TTM，差距擴大或收斂無法判斷"},"peer_na_reason":"同業 ROIC 與投入資本事實表未涵蓋，以利潤率差距代替","threats":[{"level":"🔴","text":"ARM 生態攻擊：Nvidia 以 Arm 架構 Vera CPU 切入企業與 AI 系統，字節跳動因 Intel 與 AMD 漲價、交期拉長而自研 Arm／RISC-V 伺服器 CPU；ARM 伺服器出貨份額一年由 11.5% 升到 17.7%","p":"45%","evidence_refs":["substitute_technology#0","customer_second_source#0"]},{"level":"🟡","text":"AMD 點對點競爭：x86 伺服器營收份額 46.2%，Intel 自承市占取決於供給，2027 上半年供給仍吃緊","p":"60%","evidence_refs":["competitive_share_entrants#1"]},{"level":"🟡","text":"代工端：台積電主導先進製程利潤池，客戶等 14A 良率成熟才下決定，外部代工營收仍小","p":"50%","evidence_refs":[]}],"roic_durability":{"quadrant":"低利益率×低周轉","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"伺服器 CPU 需求有 10-Q 背書（AI 基礎建設帶動、延續到 Q4 以後），付款者是雲端與企業；但急迫性來自 AI 資本支出週期，不等於持久。PC 屬可延後購買，記憶體漲價已讓 2026 出貨約 −12%、2027 約 −10%"},{"item":"決策層級","level":"🔴","text":"在客戶最小決策單位（單一伺服器機型、單一 AI 機櫃）上，x86 已可被 AMD 與 Arm 取代：ARM 伺服器出貨份額一年增 6 個百分點，字節跳動因漲價與交期自研；Intel 自己也表示願替客戶代工任何架構的 CPU，等於承認架構轉換成本在下降"},{"item":"價值鏈分配","level":"🔴","text":"價值鏈利潤落在台積電（營益率 58%）、缺貨中的記憶體與載板供應商，以及握有份額選擇權的客戶端；Intel 代工每季仍虧約 19 億美元，前三大客戶占營收 43%，短缺結束後議價權回到客戶"},{"item":"社會容忍度","level":"🟡","text":"身為美國唯一先進製程代工，政策支持度高；但美中出口管制已造成銷售減少、美國撤銷對中國晶圓廠出口美製設備授權，國會對 Intel 測試與中國有關的設備提出疑慮，政策是雙向變數"}],"roiic":"已實現為負（2022–2025 自由現金流累計約 −443 億美元，同期營收由 631 億降至 529 億美元）；管理層目標每個節點至少 20% 未證，保守取 5%","reinvest_rate":"超過 100%，內生部分以 100% 封頂（2026 毛資本支出 200 億美元對 TTM 稅後營業利益約 42 億美元，超出部分靠 8 月增資 230 億美元）","endo_ceiling":5,"formula_note":"內生成長上界＝增量報酬 5% × 再投資率 100%＝約 5%。TTM 營業利益＝營益率 7.95% × TTM 營收約 599 億美元（市值 3,343 億 ÷ P/S 5.58）≈ 48 億美元，稅率 11% 後約 42 億美元。投入資本事實表未涵蓋，以 FY2025 總資產 2,114 億美元估資產周轉約 0.28 倍，當期 ROIC 個位數低段"}}}},"q3_growth":{"verdict":"五年後跑道中等：成長主要靠伺服器量價與客製晶片，第二曲線（外部代工、先進封裝）尚未證實","reasoning":"成長來源：2026–27 以伺服器量價（短缺定價）為主、客製晶片為輔，PC 量縮；不回購、股本稀釋，Classiq 併購金額小。共識 EPS：FY2026 1.48、FY2027 2.10、FY2028 3.20，兩年年化約 47%（FY2025 GAAP 為 −0.06，無法當基期）。內生上界約 5%（見競爭優勢題），缺口約 42 個百分點，歸因為毛利率從低谷回升（FY2025 34.8% → Q3 non-GAAP 44.1%）與短缺定價，可歸因但可逆。x86 份額已約七成，不適用滲透率跑道；五年後要看伺服器市場成長與外部代工能否成形。衰退信號亮四項，長期成長性評為弱。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_kpi6_dcai_foundry_ccpg","f_kpi5_q4_fy2026"],"verdict_values":{"growth":{"driver_mix":"2026–27 以伺服器量價（短缺定價）為主、客製晶片為輔（管理層稱過去三年成長三倍、未來三年再三倍）；PC 量縮；不回購、股本稀釋；併購金額小","runway_years":"不適用：x86 份額已約七成，跑道看伺服器市場成長與外部代工能否成形","runway_post_y5":"🟡","endo_ceiling_basis":"引用競爭優勢題的報酬持續期推導：內生上界約 5%；共識 FY2026→FY2028 EPS 年化約 47%（1.48→3.20），缺口約 42 個百分點，歸因為毛利率回升與短缺定價，不是再投資報酬","segments":[{"item":"DCAI（資料中心與 AI，含客製晶片）","value":"Q3 營收 73 億美元、年增 78%、季增 17%；營業利益 30 億美元（42%）；Q4 指引季增約十幾個百分點；客製晶片季增逾 50%、年增逾一倍"},{"item":"CCPG（PC 與邊緣）","value":"Q3 營收 81 億美元、年減 5%、季減 9%；營業利益 23 億美元（28%）；Q4 指引季減逾 20%"},{"item":"Intel Foundry","value":"Q3 營收 67 億美元（多為內部），外部 4.11 億美元含非經常性專案；營業虧損 19 億美元，季改善 2.36 億美元"},{"item":"利潤結構","value":"DCAI 與 CCPG 營業利益合計約 53 億美元，代工虧損 19 億美元吃掉其中約三分之一；成長與利潤都押在 DCAI"}],"decay_signals":[{"signal":"毛利率連 2 季年減","lit":false,"evidence":"Q3 non-GAAP 44.1%；去年同期數字事實表未涵蓋，Q4 指引 38% 需待年比"},{"signal":"核心市占近 12 個月縮減","lit":true,"evidence":"伺服器出貨份額 72.8%→66.8%，x86 份額首度跌破七成"},{"signal":"主力產品提價後銷量下滑","lit":false,"evidence":"PC CPU 自 2025 年底第三次調價、CCPG 年減 5%，但量縮主因為記憶體漲價（CEO），暫列觀察"},{"signal":"EPS 成長顯著高於營收成長","lit":true,"evidence":"共識 FY2027 EPS 年增 42%、營收年增 12%"},{"signal":"自由現金流對淨利轉換偏低連 2 年","lit":true,"evidence":"淨利為負時比率失真，但自由現金流 FY2022–2025 連四年為負，CFO 稱 2027 也不會轉正"},{"signal":"SBC 占營收逾 5% 且上升","lit":false,"evidence":"Q3 為 3.5%"},{"signal":"TAM 萎縮或被替代技術壓縮","lit":true,"evidence":"PC 出貨 2026 約 −12%、2027 約 −10%；ARM 在伺服器替代 x86"},{"signal":"產業估值倍數近 3 年系統性下移","lit":false,"evidence":"事實表未涵蓋"},{"signal":"維持性資本支出占自由現金流逾 60%","lit":false,"evidence":"事實表未拆維持性資本支出"},{"signal":"停止投資新產能且收入下滑","lit":false,"evidence":"資本支出仍在擴大"}],"trap_rating":"🔴：價值陷阱風險高（亮四項），長期成長性亦弱"}}},"q4_capital":{"verdict":"資本配置偏弱：不配息不回購，以增資與舉債支應擴產，併購有減損紀錄；SBC 稀釋可控","reasoning":"現金：季末現金及短投約 540 億美元、總債務 501 億美元，淨現金約 39 億美元，另有 150 億美元循環額度。來源：8 月增資 230 億美元、Altera 51% 出售（稅前利得 56 億美元）、Fab 34 過橋貸款 65 億美元。去向：2026 毛資本支出約 200 億美元、買回 Fab 34 合資 49% 權益 142 億美元、Classiq 約 19 億美元；股息與回購為零。Q3 調整後自由現金流 16.4 億美元，TTM FCF 利潤率 6.25%，但 CFO 表示 2027 不太可能有正自由現金流。SBC 單季 5.86 億美元，占營收 3.5%、占 non-GAAP 營業利益 18.1%。合資夥伴少數股權利益 2027、2028 年各約 11 億美元，是每股盈餘的固定扣項。完整三年現金去向四分與債務到期結構事實表未涵蓋。","fact_refs":["f_kpi3_adjusted_fcf","f_kpi4_sbc_non_gaap","f_net_debt_m","f_shares_diluted_m","f_peer_intc_fcf_margin_pct","f_dividend_yield_ttm"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":true,"passed":false,"input":"2026 前九月認列 Mobileye 相關商譽減損 39 億美元；Classiq 約 19 億美元尚無報酬紀錄"},{"name":"buyback_yield","applicable":false,"passed":null,"input":"近一年無回購、無股息；8 月反向增資 230 億美元"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"Q3 SBC 5.86 億美元，年化約 23 億美元，按現價約 3,700 萬股、占流通股約 0.7%（不含 8 月增資）"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購：Classiq 約 19 億美元、Fab 34 少數股權買回 142 億美元屬資本結構調整（低於市值 5%），現金去向已寫在本題理由"}}}},"q5_valuation":{"verdict":"現價要 2028 年 EPS 達到共識 3.20 並維持約 20 倍才划算；我們 Base 只到 2.70，不信，估值偏貴","reasoning":"現價 62.9 美元對 FY2026 共識 1.48 為 42.5 倍、對 FY2027 2.10 約 30 倍、對 FY2028 3.20 約 19.7 倍；EV/S 5.5 倍（前瞻 5.3 倍），高於近四個年度端點。等於市場要 2028 年獲利翻倍且倍數維持約 20 倍。本判斷 Base FY2028 2.70（比共識少 16%），對應約 23 倍；五年 Base 終值 71 美元，年化約 2.5%。共識近 3 個月 FY1 下修 2.6%，最近一次 FY1、FY2 各下修約 4%。券商目標價區間約 65–200 美元，高低差逾 2.5 倍且多數在 Q4 指引前，參考性有限。同業前瞻本益比事實表未涵蓋，終值倍數只能以 Intel 自身現值對照。轉機型以正常化獲利錨定，PEG 不作主錨。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_fy1_pct","f_consensus_rev_fy2_pct","f_consensus_rev_fy3_pct","f_consensus_rev_3m_fy1_pct","f_ps_current","f_ps_percentile","f_ev_s_current","f_ev_s_percentile","f_ev_s_fwd","f_ev_m","f_net_debt_m","f_shares_diluted_m","f_dividend_yield_ttm"],"verdict_values":{"valuation":{"basis":"前瞻本益比為主、EV/S 為輔；轉機型以 FY2027–2028 正常化獲利錨定","peers":{"expanded":false,"reason":"事實表同業對照只有利潤率，沒有同業前瞻本益比或 EV/S，無法做倍數對照；利潤率差距已寫在競爭優勢題"},"fwd_pe":42.5,"peg":null,"percentile_5y":null,"val_light":"🟠","val_light_derivation":"前瞻本益比 42.5 倍（FY2026）、約 30 倍（FY2027）、約 19.7 倍（FY2028 共識）；EV/S 5.5 倍高於近四個年度端點全部（四點內分位 100，非五年分位，故五年分位留空）。以本判斷 Base FY2028 2.70 計約 23 倍；Base 五年終值 71 美元，年化約 2.5%，低於 8%。轉機型 PEG 不適用，留空。結論偏貴；前份為極貴，差異來自股價下跌 37%","upside_short_pct":-6,"upside_mid_pct":13,"denominator_disputed":true,"denominator_note":"FY2026 分母含以色列廠事故（約 3 億美元營收、200 個基點毛利率）與 PC 庫存修正，FY2025 GAAP 為虧損；改以 FY2027–2028 前瞻錨定，而 FY2028 共識 3.20 能否兌現正是爭點，因此不採用任何「便宜」論證。短期目標＝FY2028 Base 2.70 × 22 倍＝59.4 美元；中期目標＝五年 Base 終值 71.1 美元"}}},"q6_how_wrong":{"verdict":"最可能看錯的地方是把短缺帶來的量價當成份額修復；價值陷阱風險高","reasoning":"反證三視角見反證紀錄：論點失敗（份額續失加上 14A 暫停，五年跌 55–68%）、股東經濟變差（價值被供應商、客戶、合資夥伴與稀釋分走）、價格已反映太多（現價要 2028 共識兌現）。衰退信號亮四項：核心份額縮減、EPS 成長遠高於營收、自由現金流連年為負、PC 萎縮與 ARM 替代。壓力測試五項過兩項：流動性（現金 540 億美元加循環額度 150 億美元，對 2027 負自由現金流）與 PC 再跌 10% 通過；伺服器短缺 2028 年解除、14A 暫停、台海或出口管制升級三項未過。回撤區間 −70% 至 −45%：Bear 終點約 −65%，股價半年已跌 34%、RSI 24，週線跌破 52 週均線（77.25 美元）但仍在 104 週均線（50.62 美元）之上，PC 修正延到 2027 上半年。","fact_refs":["f_week26_return_pct","f_rsi14","f_ma_state","f_ma_w52","f_ma_w104","f_ma_w250","f_ma_slope_w250_pct","f_net_debt_m"],"verdict_values":{"trap":{"verdict":"🔴","label":"價值陷阱風險高：核心份額縮減、EPS 成長遠高於營收成長、自由現金流連年為負、PC 萎縮與 ARM 替代四項亮燈"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":1.48,"pe":42.5,"basis":"FY2026E 共識 non-GAAP EPS（FY1），與終端倍數同為當年度前瞻口徑；Y1–Y5 為 FY2027–FY2031"},"eps":{"bull":[2.3,3.5,4.4,5.2,6.0],"base":[1.9,2.7,3.2,3.6,3.95],"bear":[1.3,1.6,1.4,1.5,1.7]},"pe":{"bull":24,"base":18,"bear":13},"p":{"bull":20,"base":45,"bear":35},"yield_pct":{"dividend":0.0,"net_buyback":0.0},"second_stage":{"bull_cagr_pct":10,"base_cagr_pct":6},"max_dd":{"lo":-70,"hi":-45,"basis":"Bear 終點 FY2031 EPS 1.70 × 13 倍＝22.1 美元，較現價約 −65%，下限取 −70% 覆蓋；上限 −45%：股價半年已跌 34%、RSI 24，PC 庫存修正延到 2027 上半年、2027 自由現金流為負，若份額或 14A 出事，路徑上先見 −45% 以上的機率高","trigger_time":null},"basis":{"bull":"伺服器 CPU 市場照管理層說法高速擴張，Intel 供給鬆綁後份額穩在五成以上，客製晶片再成長三倍，14A 取得多家客戶、代工 2029 年轉正；FY2031 EPS 6.0、24 倍","base":"伺服器需求延續到 2028 後短缺緩解、份額緩降，代工虧損收斂但外賣有限，毛利率回到 40% 中段；FY2027 1.90、FY2028 2.70（低於共識），FY2031 3.95、18 倍。股數以 54.4 億股以上計，SBC 稀釋已含在每股路徑，淨回購填 0。同業前瞻本益比事實表未涵蓋，18 倍以 Intel 自身現值對照（FY2028 共識約 19.7 倍）","bear":"2028 年短缺結束、平均售價回落，ARM 與 AMD 份額續增，14A 暫停並減損，少數股權利益與稀釋壓縮每股盈餘；FY2031 EPS 1.70、13 倍"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"x86 份額首度跌破七成、伺服器出貨份額一年少 6 個百分點、ARM 伺服器出貨份額升到 17.7%；報導稱 Intel 曾表示若沒有重要外部客戶可能暫停 14A 及後續節點","assumption":"2027 下半年供給鬆綁後，Clearwater Forest 與 Diamond Rapids 能把份額拿回，14A 拿到足夠客戶","consequence":"若份額續失且 14A 暫停，FY2031 EPS 停在 1.5–2 美元、倍數 12–14 倍，股價約 20–28 美元，較現價跌 55–68%","ruling":"採納：空頭機率定 35%。與唯一致命點部分重疊：致命點只取 14A 暫停這一個二元事件，份額流失另列主要風險","watch":"每季伺服器出貨份額、14A 第二家具名客戶","evidence_refs":["competitive_share_entrants#1","substitute_technology#1"]},{"view":"論點成功但股東經濟變差","evidence":"伺服器需求成立，但增量價值被載板與記憶體供應商、前三大客戶（占營收 43%）、合資夥伴少數股權利益（2027、2028 年各約 11 億美元，約每股 0.2 美元）與增資稀釋分走；併購端已有 39 億美元商譽減損，又再買 Classiq","assumption":"營收成長能等比例落到每股盈餘","consequence":"營收達到 Base，但 EPS 只落在 Bear 與 Base 之間","ruling":"採納：Base 路徑低於共識（FY2027 1.90 對 2.10、FY2028 2.70 對 3.20）","watch":"增量毛利落差是否低於 40%、少數股權利益、稀釋後股數","evidence_refs":["customer_concentration_credit#0","turnaround_liquidation_floor#0"]},{"view":"價格已反映太多","evidence":"股價已跌 34%，但前瞻本益比仍 42.5 倍（FY2026）、約 30 倍（FY2027），EV/S 5.5 倍高於近四個年度端點；Q4 指引營收 150–160 億美元、EPS 0.25，低於市場預期約 171 億美元與 0.43；TrendForce 預估 2027 下半年 NAND 供給成長超過需求，記憶體上行期可能結束","assumption":"市場相信 2028 共識 3.20 會兌現且倍數維持約 20 倍","consequence":"若 2028 年 EPS 只有 2.7，現價對應約 23 倍，五年報酬年化約 2–3%","ruling":"採納：現價沒有安全邊際，股價大跌不等於便宜","watch":"FY2027 與 FY2028 共識修正、伺服器 CPU 交期","evidence_refs":["capital_markets_pricing#4","supply_demand_durability#3"]},{"view":"論點失敗","evidence":"10-K 揭露許多產品的 compute die 依賴台灣供應商、中台緊張升高；美國出口管制已減少對中國銷售，部分 AI 晶片出口需許可","assumption":"地緣風險五年內不實現","consequence":"台海或出口管制升級會同時打擊供給與中國需求","ruling":"部分採納：列為長期風險，不單獨調整機率","watch":"10-Q 風險因素更新、出口許可變動","evidence_refs":["geo_supply_chain#0","reg_tariff_export#2"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 100.23 → 本次 62.9（-37.2%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=100.23","side_b":"本次 price_at_dd=62.9","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]裁決由 dd_decision.py 機械路由：前份 觀望 → 本次 迴避","cause":"新證據","prior_field":["dca_verdict"],"side_a":"前份 dca_verdict=觀望","side_b":"本次 dca_verdict=迴避","ruling":"裁決是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。沒有單一輸入能還原，屬多欄共同：估值 🔴→🟠、均線 ✅→🟡、陷阱燈 🟡→🔴、護城河趨勢 →→↓。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]角色由 dd_decision.py 機械路由：前份 追蹤 → 本次 不持有","cause":"新證據","prior_field":["dca_role"],"side_a":"前份 dca_role=追蹤","side_b":"本次 dca_role=不持有","ruling":"角色是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。沒有單一輸入能還原，屬多欄共同：估值 🔴→🟠、均線 ✅→🟡、陷阱燈 🟡→🔴、護城河趨勢 →→↓。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 100.23 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 100.23 美元：Bull 價 180、Bear 價 50，五年期望值 +9.5%，基準年化 1.9%，不對稱比 1.3","side_b":"本次情境、股價仍用 100.23 美元：Bull 價 144、Bear 價 22.1，五年期望值 −31.6%，基準年化 −6.6%，不對稱比 0.32","ruling":"先換情境、股價不動：五年期望值少 41.1 個百分點，基準年化少 8.5 個百分點。不對稱比由 1.3 變為 0.32。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 100.23 美元：五年期望值 −31.6%，基準年化 −6.6%，不對稱比 0.32","side_b":"本次情境、股價 62.9 美元：五年期望值 +9.0%，基準年化 2.5%，不對稱比 1.14","ruling":"再換股價、情境不動：起點價下跌 37.2%，五年期望值多 40.6 個百分點，基準年化多 9.1 個百分點，不對稱比由 0.32 升到 1.14。合計五年期望值比前份少 0.5 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"競爭地位方向（份額）","cause":"新證據","prior_field":["moat_trend","trap"],"side_a":"管理層（2026-10-29 法說）：明年伺服器份額取決於供給，Coral Rapids 對 AMD 有競爭力、下一代會領先；Nova Lake 讓 PC 進入份額回升期。前份判斷走勢持平、陷阱風險中等","side_b":"第三方數據：Mercury 2026Q2 Intel x86 份額首度跌破七成（69.3%），伺服器出貨份額一年由 72.8% 降到 66.8%，ARM 由 11.5% 升到 17.7%；分析師提及 AMD 指引營收成長 70%；CFO 稱 2027 自由現金流為負","ruling":"不可調和（方向相反）。採 B 側：份額是可量測的結果，管理層說法是路線圖承諾；2026-07-23 法說 CEO 已承認部分領域仍落後，本季被問份額仍未給數字。走勢由持平改為向下，陷阱風險由中等升為高（亮四項衰退信號），整體結論隨之由觀望轉為迴避","evidence_level":"第三方季度份額（Mercury、UBS）與公司法說","settle_metric":"Intel x86 伺服器出貨份額（每季）","if_then":["若 2027 下半年供給鬆綁後 Intel 伺服器出貨份額連兩季回升到 65% 以上，走勢改回持平並重跑研究","若份額跌破 60% 或 AMD 伺服器營收份額超過 50%，維持迴避且不設進場價；若持有則減碼一半","反向條件：若份額回升但同期毛利率跌破 38%（以價換量），不視為護城河修復"],"evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1"]},{"axis":"估值結論（價格變動）","cause":"價格變動","prior_field":["val","signal","runway_post_y5","archetype","cycle_position"],"side_a":"前份（2026-07-24，股價 100.23 美元）：估值極貴","side_b":"本次股價 62.9 美元（−37%）：前瞻本益比 42.5 倍（FY2026）、約 30 倍（FY2027）、約 19.7 倍（FY2028 共識），估值由極貴降為偏貴；同期 FY1、FY2 共識各下修約 4%，Q4 指引低於預期","ruling":"可調和。估值結論只因股價下跌改善一級；品質評級維持 C、五年後跑道維持中等、轉機型歸類不變、循環位置仍不適用（非循環型），這些欄不因股價變動而改","evidence_level":"事實表股價與共識快照","settle_metric":"FY2027 前瞻本益比","if_then":["若股價續跌而 FY2027 與 FY2028 共識不再下修，估值可再降一級，但份額與 14A 條件未成立前仍不進場","若共識再下修 5% 以上，估值改善被抵銷，維持偏貴"],"evidence_refs":["capital_markets_pricing#4"]},{"axis":"情境機率與回撤","cause":"方法變動","prior_field":["p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份：多頭 25%、空頭 30%、最大回撤 −65%","side_b":"本次：多頭 20%、空頭 35%、最大回撤區間 −70% 至 −45%","ruling":"可調和。本次改以報酬持續期推導內生成長上界（約 5%），Base EPS 年化約 22% 明顯超過上界，空頭機率至少 30%；再加上份額走勢轉弱與 2027 負自由現金流，空頭取 35%；回撤改給區間並覆蓋 Bear 終點約 −65%","evidence_level":"情境推導","settle_metric":"FY2027 實際 EPS 對 Base 1.90","if_then":["若 FY2027 EPS 達 2.10 以上且份額止跌，空頭機率回調到 30%","若 FY2027 EPS 低於 1.50，空頭機率上調到 45% 以上"],"evidence_refs":[]},{"axis":"重啟研究條件（進場前提）","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"首個具名 tier-1 外部客戶 14A/18A 晶圓 commitment（把 >$15B pipeline 轉成經常性營收）；或 foundry 2027 exit breakeven 如期兌現且外部營收占 foundry 比 ≥ 10%","side_b":"伺服器出貨份額連兩季回升、除 Tesla 外第二家具名 14A 客戶承諾、2028 自由現金流指引轉正，三項同時成立才重跑研究","ruling":"門檻改變。前份只看代工，用「或」連接；本次份額轉弱成為主要約束，改成三項同時成立才在進場前重跑研究，首倉從小倉位開始，不直接加碼。理由：8 月增資 230 億美元已觸發前份的稀釋警戒，CFO 確認 2027 自由現金流為負，份額數據續弱","evidence_level":"法說原話與第三方份額","settle_metric":"三項重啟條件是否同時成立","if_then":["三項同時成立：進場前重跑研究，首倉從小倉位開始","只成立一兩項：維持迴避，不加碼也不建倉"],"evidence_refs":[]},{"axis":"Single Thing（唯一致命點）","cause":"方法變動","prior_field":null,"side_a":"前份未設 Single Thing（null）","side_b":"2027 年中前 14A 外部客戶不足，Intel 宣布暫停或無限期延後 14A","ruling":"新增 Single Thing。轉機型的唯一致命點取轉機能否成立的二元事件；14A 是 2028 年伺服器 CPU 製程與代工轉正的唯一路徑，多頭與空頭終值的差距大半繫於此。若發生則不進場，若持有則清倉","evidence_level":"公司說法與二手報導","settle_metric":"14A 具名外部客戶數","if_then":["若 2027-06-30 前公司宣布暫停 14A，則若持有就清倉、空頭機率上調到 50% 以上","若第二家具名客戶在 2027 上半年公告，計為重啟條件之一成立"],"evidence_refs":[]},{"axis":"清倉與減碼門檻","cause":"方法變動","prior_field":null,"side_a":"前份未設清倉與減碼門檻（null）","side_b":"新設五項：伺服器出貨份額低於 60%；2027 上半年任一季 DCAI 低於 80 億美元；2027 年任兩季毛利率低於 38%；2027-06-30 前無第二家 14A 客戶或宣布暫停；淨負債超過 150 億美元或再增資","ruling":"新增。前份只有漂移觸發，沒有可執行的清倉或減碼數字；本次每項附資料來源與時窗，若持有則觸發即減碼或清倉","evidence_level":"方法調整","settle_metric":"五項門檻","if_then":["份額或 DCAI 門檻觸發：若持有則減碼一半","14A 或融資門檻觸發：若持有則清倉"],"evidence_refs":[]},{"axis":"前份風險警戒已發生（稀釋）","cause":"新證據","prior_field":null,"side_a":"前份（2026-07-24）風險三：被迫進資本市場稀釋即為警戒","side_b":"2026 年 8 月完成 230 億美元增資，Q4 稀釋後股數 54.4 億股（CFO）；2026-07-23 法說 CFO 已預告可能需要進資本市場","ruling":"已發生，採納。增資是預告後執行，資金用於擴產而非周轉；但代表 2027 負自由現金流期間仍可能再融資，列入新的再融資風險門檻","evidence_level":"法說原話","settle_metric":"2027 年股權融資與淨現金","if_then":["若 2027 年再做股權融資，若持有則減碼","若 2028 上半年自由現金流轉正且無新增資，此風險降級"],"evidence_refs":[]},{"axis":"管理層指引可信度","cause":"新證據","prior_field":null,"side_a":"2026-07-23 法說 CFO：毛利率每季「舒適地維持在 40% 以上」；CCPG 下季大致持平","side_b":"2026-10-29：Q3 CCPG 季減 9%、低於公司預期；Q4 毛利率指引 38%（扣以色列廠事故約 200 個基點後為 40%），Q4 營收與 EPS 指引低於市場預期","ruling":"可調和（程度差異）：主因是記憶體漲價與以色列廠事故兩個外部衝擊，但說明 PC 能見度不到一季；Base 路徑因此低於共識，管理層的 2027 毛利說法打折","evidence_level":"法說原話對照","settle_metric":"2027Q1 毛利率與 CCPG 營收","if_then":["若 2027Q1 毛利率回到 40% 以上，指引可信度回復","若 2027Q1 毛利率仍低於 38% 且非一次性項目，Base 路徑再下修"],"evidence_refs":["capital_markets_pricing#4"]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"股價半年跌 34%、RSI 24 超賣；DCAI 年增 78%，伺服器需求到 2028 仍大於供給；18A 良率已到業界水準，Intel 3 成本降 15%、18A 降 40%；現金 540 億美元加 150 億美元循環額度；以 2028 共識計約 20 倍；7 月多家券商目標價 115–160 美元","side_b":"現價對 2027 共識仍約 30 倍；2027 自由現金流為負；份額續失；Q4 指引低於預期且 PC 修正延到 2027 上半年；券商目標價多在指引前，區間約 65–200 美元，分歧大","ruling":"可調和。買方論證成立的前提是 2028 共識 3.20 兌現且倍數維持；本判斷 Base 為 2.70，現價對應五年年化約 2–3%，不足以補償 35% 的空頭機率。超賣只代表價格先走、基本面證據未到，不追","evidence_level":"事實表估值與法說","settle_metric":"FY2028 共識與份額","if_then":["若價格續跌但份額與 DCAI 達標（基本面無損），在重啟條件成立後分批買進，不一次建倉","若價格反彈但份額未止跌，不追"],"evidence_refs":[]},{"axis":"產業態勢三軸","cause":null,"prior_field":null,"side_a":"結構轉好：伺服器 CPU 產業出貨 2026、2027 年各增 30% 以上（CFO），Gartner 稱 2Q26 晶片庫存進入中度短缺並持續到 2027，WSTS 預估 2027 半導體再成長約 27%","side_b":"競爭惡化：x86 份額首度跌破七成、ARM 伺服器份額一年增 6 個百分點、Nvidia Vera 與客戶自研 CPU；其他結構變數：美國撤銷對中國晶圓廠出口設備授權、AI 晶片 25% 關稅（有豁免）、PC 受記憶體漲價壓縮","ruling":"雙向拉鋸：需求結構轉好，但 Intel 分到的是短缺帶來的量價而非份額；競爭惡化的證據是實際份額數字，需求轉好的證據是產業預測，前者對 Intel 長期報酬的影響更直接","evidence_level":"第三方份額與產業預測","settle_metric":"伺服器出貨份額對產業出貨成長","if_then":["若 Intel DCAI 成長追上產業 30% 出貨成長且份額止跌，改判結構性轉好","若產業成長而 Intel 份額續降，維持競爭惡化判讀"],"evidence_refs":["competitive_share_entrants#0","reg_tariff_export#1"]},{"axis":"前份門檻保留與退休","cause":"方法變動","prior_field":null,"side_a":"前份假設門檻：2027 外部代工占比 10% 以上、代工 2027 年底損益兩平、股價淨值比維持 4 倍以上、共識連兩月下修 5% 以上為漂移","side_b":"本次：外部代工占比 10% 與代工虧損收斂保留在代工假設；共識下修門檻保留為風險觸發；股價淨值比門檻退休","ruling":"股價淨值比門檻退休：本次事實表沒有帳面價值，無法追蹤，估值改用前瞻本益比與 EV/S。代工 2027 年底損益兩平：Q3 代工仍虧 19 億美元、CFO 稱要持續獲利還有很多工作，保留門檻但預期不會達成","evidence_level":"事實表覆蓋範圍","settle_metric":"代工單季營業損益","if_then":["若代工單季虧損 2027 年底前收斂到 10 億美元以內，代工假設維持","若 2027 年底代工單季虧損仍超過 15 億美元，代工假設削弱並上調空頭機率"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"14A 外部客戶與時程","type":"Single Thing","maps_to":"H3／R3","metric":"14A 具名外部客戶數與 14A 是否續行","threshold":"2027-06-30 前除 Tesla 外無第二家具名客戶，或公司宣布暫停或延後 14A","action":"維持不進場；若持有則清倉","source_freq":"8-K 與每季法說","date":"2027-06-30","evidence_refs":["substitute_technology#1"]},{"n":2,"text":"伺服器新增產能能否轉成營收","type":"假設驗證","maps_to":"H1","metric":"DCAI 季營收","threshold":"2027Q1、Q2 每季 85 億美元以上","action":"連兩季達標才納入重跑研究；未達標維持迴避","source_freq":"每季財報","date":"2027-07-31"},{"n":3,"text":"毛利率與自由現金流","type":"假設驗證","maps_to":"H2","metric":"non-GAAP 毛利率、調整後自由現金流","threshold":"2027 年任兩季毛利率低於 38%，或 2028 上半年自由現金流仍為負","action":"維持迴避並下修 Base 路徑","source_freq":"每季財報","date":"2028-07-31"},{"n":4,"text":"伺服器份額續失","type":"風險","maps_to":"R2","metric":"Intel 伺服器出貨份額、AMD 伺服器營收份額、ARM 伺服器出貨份額","threshold":"Intel 低於 60%、AMD 高於 50%、ARM 高於 25% 任一成立","action":"維持迴避、不設進場價；若持有則減碼一半","source_freq":"Mercury Research、UBS 每季","date":null,"evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1","customer_second_source#0","substitute_technology#0"]},{"n":5,"text":"半導體循環轉向","type":"風險","maps_to":"H1","metric":"記憶體供需、伺服器 CPU 交期","threshold":"TrendForce 或 WSTS 顯示 2027 下半年記憶體供給成長超過需求，且公司不再稱伺服器供不應求","action":"空頭機率上調 5 個百分點、維持迴避","source_freq":"TrendForce、WSTS 季報與公司法說","date":"2027-10-31","evidence_refs":["supply_demand_durability#3"]},{"n":6,"text":"再融資與稀釋","type":"風險","maps_to":"R4","metric":"淨現金、股權融資","threshold":"2027 年再做股權融資，或淨負債超過 150 億美元","action":"若持有則減碼；維持迴避","source_freq":"10-Q、8-K","date":"2027-12-31"},{"n":7,"text":"地緣與出口管制","type":"風險","maps_to":"R5","metric":"公司揭露的出口管制、關稅或台灣供應衝擊","threshold":"單季營收影響 5 億美元以上","action":"空頭機率上調；若持有則減碼","source_freq":"10-Q 風險因素、8-K","date":null,"evidence_refs":["geo_supply_chain#0","geo_supply_chain#1","geo_supply_chain#2","reg_tariff_export#1","reg_tariff_export#2"]},{"n":8,"text":"訴訟與監管","type":"風險","maps_to":"H2","metric":"歐盟處理器案上訴、證券集體訴訟上訴、Spectre 系列消費者訴訟、國會對設備採購的質疑","threshold":"任一案出現不利裁決或和解金額 10 億美元以上，或主管機關限制 Intel 採購特定設備","action":"金額 10 億美元以上則若持有減碼一半；涉刑事則清倉","source_freq":"10-K、10-Q 法律附註與 8-K","date":null,"evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#1","major_events#1","lawsuit_class_action#0","lawsuit_class_action#1"]},{"n":9,"text":"重啟研究條件","type":"估值rearm","maps_to":"H1／H3","metric":"伺服器出貨份額、14A 具名客戶、2028 自由現金流指引","threshold":"伺服器出貨份額連兩季回升、除 Tesla 外第二家具名 14A 客戶承諾、2028 自由現金流指引轉正，三項同時成立","action":"三項同時成立才重跑研究；首倉從小倉位開始","source_freq":"每季","date":null},{"n":10,"text":"Q4 FY2026 財報複審","type":"複審日期","maps_to":null,"metric":"CCPG 庫存修正深度、2027 資本支出數字、1.0 PDK 時程、DCAI Q1 展望","threshold":"CCPG Q4 季減逾 25%，或 2027 資本支出超過 350 億美元","action":"依結果更新情境路徑","source_freq":"季報","date":"2027-01-31"},{"n":11,"text":"共識下修","type":"風險","maps_to":"H1","metric":"FY2027 共識 EPS（Koyfin 快照）","threshold":"連兩次快照合計下修 5% 以上（最新一次 2.18→2.10，−3.67%）","action":"Base 路徑再下修、維持迴避","source_freq":"每月快照","date":null}],"kill_metrics":[{"metric":"Intel x86 伺服器出貨份額","bear_threshold":"低於 60%（2026Q1 為 66.8%）","window":"每季，至 2027 年底","source":"Mercury Research、UBS","last_status":"warning"},{"metric":"DCAI 季營收","bear_threshold":"2027 上半年任一季低於 80 億美元","window":"2027Q1 至 Q2","source":"公司季報","last_status":"unknown"},{"metric":"non-GAAP 毛利率","bear_threshold":"2027 年任兩季低於 38%","window":"2027 全年","source":"公司季報","last_status":"warning"},{"metric":"14A 具名外部客戶","bear_threshold":"2027-06-30 前除 Tesla 外為零，或公司宣布暫停 14A","window":"至 2027-06-30","source":"8-K、法說","last_status":"unknown"},{"metric":"淨現金與股權融資","bear_threshold":"淨負債超過 150 億美元，或 2027 年再做股權融資","window":"至 2027-12-31","source":"10-Q 資產負債表、8-K","last_status":"ok"}],"evidence_dismissed":[],"action_conditions":{"rearm_trigger":"伺服器出貨份額連兩季回升、除 Tesla 外第二家具名 14A 客戶承諾、2028 自由現金流指引轉正，三項同時成立才重跑研究","exec_line":"現在不買、不設進場價；三項重啟條件同時成立後重跑研究，首倉從小倉位開始。若已持有，14A 或融資門檻觸發即清倉，份額門檻觸發先減碼一半"}},"decision_inputs":{"signal":"C","ma":"🟡","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":true,"valuation_dependent":false,"market_wrong_reason_given":"市場以 2028 共識 EPS 3.20 定價（現價約 19.7 倍）；我們認為該數字隱含伺服器短缺定價延續到 2028，可能未充分反映折舊上升、每年約 11 億美元少數股權利益、客製晶片毛利較低與 2027 負自由現金流下的稀釋風險；第三方份額數據顯示 Intel 吃到的是短缺而非份額，Base 取 2.70","momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":null,"wait_for_price_condition":null,"qc48_result":null,"qc48_note":null,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null},"thesis":{"H":[{"id":"H1","text":"AI 帶動的伺服器 CPU 需求，能被 Intel 新增的晶圓與載板產能轉成營收與利潤","2y":"FY2027 DCAI 營收 340 億美元以上、營業利益率 35% 以上","5y":null,"10y":null,"threshold":"DCAI 季營收 2027 上半年每季 85 億美元以上、下半年每季 95 億美元以上","source":"每季財報與法說；2026-10-29 法說 CFO 認同以 Q4 DCAI 約 85 億美元年化當 2027 起點，並稱下半年載板增量與 Oregon Intel 3 產能到位","drift_rule":"DCAI TTM 營收對上述路徑連 2 季落後 5% 以上為削弱、連 3 季落後 10% 以上為反轉"},{"id":"H2","text":"毛利率與現金流回到能自籌擴產的水準，不再依賴增資","2y":"FY2027 non-GAAP 毛利率全年 41% 以上；FY2028 調整後自由現金流轉正","5y":null,"10y":null,"threshold":"2027 年沒有任兩季 non-GAAP 毛利率低於 38%；2028 全年調整後自由現金流大於 0；2027 年不再做股權融資","source":"每季財報與 10-Q 現金流量表；2026-10-29 法說 CFO：2027 不太可能有正自由現金流，增量營收毛利落差目標 40–60%","drift_rule":"毛利率 TTM 低於路徑連 2 季 5% 以上為削弱、連 3 季 10% 以上為反轉；2028 上半年自由現金流仍為負即為削弱"},{"id":"H3","text":"Intel 代工拿到足夠外部客戶，14A 照時程 2028 年試產、2029 年量產並走向損益兩平","2y":null,"5y":"FY2029 外部代工營收 50 億美元以上、代工部門營業損益轉正","10y":null,"threshold":"2027-06-30 前除 Tesla 外至少再一家具名 14A 客戶；FY2027 外部代工占代工營收 10% 以上（Q3 約 6%）；代工單季虧損 2027 年底前收斂到 10 億美元以內","source":"8-K 與法說；2026-10-29 CEO：0.9 PDK 已釋出、1.0 PDK 預計 2027Q1、不揭露客戶；Q3 外部代工 4.11 億美元含非經常性專案，代工虧損 19 億美元","drift_rule":"外部代工 TTM 營收對路徑連 4 季落後 5% 以上為削弱、連 6 季落後 10% 以上為反轉；公司宣布暫停 14A 直接視為反轉"}],"R":[{"id":"R1","text":"PC 庫存修正比指引更深，延續到 2027 下半年，固定成本吸收不足壓低毛利","h_ref":"H2","clock":"⚡","threshold":"CCPG 季營收連 2 季低於 60 億美元，或 CCPG 營業利益率跌破 15%（Q3 為 28%）"},{"id":"R2","text":"伺服器份額續失給 AMD 與 ARM 陣營，短缺結束後 Intel 量價同時回落","h_ref":"H1","clock":"🔥","threshold":"Intel 伺服器出貨份額低於 60%，或 AMD 伺服器營收份額高於 50%，或 ARM 伺服器出貨份額高於 25%","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1","customer_second_source#0","substitute_technology#0"]},{"id":"R3","text":"14A 外部客戶不足，公司依先前說法暫停或延後 14A 及後續節點","h_ref":"H3","clock":"🔥","threshold":"2027-06-30 前除 Tesla 外無第二家具名客戶，或 1.0 PDK 未於 2027Q1 釋出","evidence_refs":["substitute_technology#1"]},{"id":"R4","text":"2027 資本支出大增、自由現金流為負，需要再融資或再增資而稀釋","h_ref":"H2","clock":"🔥","threshold":"2027 年再做股權融資，或淨負債超過 150 億美元"},{"id":"R5","text":"地緣與出口管制：產品依賴台灣供應商的 compute die，美中管制已減少對中國銷售，美國撤銷 Intel 等公司對中國晶圓廠出口美製設備的授權","h_ref":"H1","clock":"🐢","threshold":"公司揭露單季因出口管制、關稅或台灣供應中斷造成營收影響 5 億美元以上","evidence_refs":["geo_supply_chain#0","geo_supply_chain#1","geo_supply_chain#2","reg_tariff_export#1","reg_tariff_export#2"]},{"id":"R6","text":"客戶集中：前三大客戶占營收 43%，短缺結束後議價權回到客戶","h_ref":"H2","clock":"🐢","threshold":"前三大客戶占比 45% 以上且同年毛利率下滑","evidence_refs":["customer_concentration_credit#0"]}],"single_thing":{"description":"2027 年中前 14A 外部客戶不足，Intel 宣布暫停或無限期延後 14A","why_fatal":"14A 是 2028 年 Coral Rapids 伺服器 CPU 的製程，也是代工轉正的唯一路徑；一旦暫停，Intel 退回依賴外部代工的設計公司，代工資產與在建工程面臨減損，自有製程的轉機論點失效。多頭終值 144 美元與空頭 22 美元的差距大半繫於此","if_happens":"不進場；若持有則清倉；空頭機率上調到 50% 以上並重做情境","how_monitor":"每季法說的 14A 客戶進度、1.0 PDK 是否 2027Q1 如期釋出、8-K 客戶公告、資本支出指引中的 14A 設備訂單","probability":"約 20%（12–24 個月）：Tesla 已確認、0.9 PDK 如期、CEO 稱多家潛在客戶積極參與，但除 Tesla 外皆未證實，且報導稱公司曾表示沒有外部客戶可能停止 14A"}},"appendix_a":{"growth_durability":4,"quality_score":6,"ai_risk":"🟡","long_term_confidence":"低","fpe_fy2":30.0,"peg_fy2":0.64,"stress":{"pass":2,"total":5},"fy2_valuation_basis":"PEG 依 Koyfin 共識（2026-10-31）"},"eps_meta":{"base_eps_path":{"FY2025A":-0.06,"FY2026E":1.48,"FY2027E":2.1,"FY2028E":3.2},"fy_end_month":12,"eps_basis":"FY2026E–FY2028E 為 Koyfin 2026-10-31 快照的 non-GAAP 稀釋 EPS 共識；FY2025A 基期取年度財報 GAAP 稀釋 EPS −0.06（事實表沒有 non-GAAP 基期），口徑不同且為負，三年 CAGR 改以 FY2026E 為起點計算"},"catalysts":[{"date":"2027-01","date_precision":"month","type":"guidance","event":"Q4 FY2026 財報、2027 資本支出定案與 Q1 指引","impact":"高","watch":"CCPG 庫存修正深度、資本支出是否超過 300 億美元、DCAI Q1 展望"},{"date":"2027-01","date_precision":"month","type":"product","event":"CES 發表 Nova Lake（首款 18A-P PC 處理器）","impact":"中","watch":"設計案數量是否約為 Panther Lake 的兩倍"},{"date":"2027-Q1","date_precision":"quarter","type":"product","event":"14A 1.0 PDK 釋出","impact":"高","watch":"是否如期、客戶是否轉為量產承諾"},{"date":"2027-Q2","date_precision":"quarter","type":"other","event":"先進封裝外部客戶公告（CEO 稱未來兩季內）","impact":"中","watch":"客戶名稱與金額"},{"date":"2027-06","date_precision":"month","type":"product","event":"14A 客戶決定窗口結束（2026 下半年至 2027 上半年）","impact":"高","watch":"除 Tesla 外是否有具名客戶"},{"date":"2027-Q3","date_precision":"quarter","type":"capacity","event":"Oregon Intel 3 產能投產、載板增量到位","impact":"中","watch":"DCAI 季營收是否突破 95 億美元"}],"decision_out":{"verdict":"迴避","role":"不持有","row_hit":"2","pacing":[],"holding_cap":null,"audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='C'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":true,"basis":"thesis_irreconcilable=True"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":true,"basis":"moat_trend='↓', moat='C'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]}],"requires_critic":[]}}
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
