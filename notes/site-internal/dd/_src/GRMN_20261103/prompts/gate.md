你是 DD 管線 v20 的判斷層閘（gate），標的 GRMN（20261103）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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
- `f_kpi0_gaap`（q1_business）｜營收（GAAP）＝1986.1 百萬美元｜期間與口徑：Q3 FY2026（季末 2026-09-26，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Garmin Q3 2026 新聞稿（8-K EX-99.1）（numbers.latest_quarter_kpis.items[0]，as_of Q3 FY2026（季末 2026-09-26，公告於 2026-10-28））
  - 註記：未取得
- `f_kpi1_gaap`（q1_business）｜GAAP 營業利益＝611.6 百萬美元｜期間與口徑：Q3 FY2026（季末 2026-09-26，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Garmin Q3 2026 新聞稿（8-K EX-99.1）（numbers.latest_quarter_kpis.items[1]，as_of Q3 FY2026（季末 2026-09-26，公告於 2026-10-28））
  - 註記：未取得
- `f_kpi2_gaap`（q1_business）｜GAAP 營業利益率＝30.8 %｜期間與口徑：Q3 FY2026（季末 2026-09-26，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Garmin Q3 2026 新聞稿（8-K EX-99.1）（numbers.latest_quarter_kpis.items[2]，as_of Q3 FY2026（季末 2026-09-26，公告於 2026-10-28））
  - 註記：未取得
- `f_kpi5_fy2026`（q1_business）｜管理層全年指引（FY2026）＝8150 百萬美元（營收約）｜期間與口徑：Q3 FY2026（公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：Garmin Q3 2026 新聞稿（8-K EX-99.1）：pro forma EPS 約 10.80、營業利益率 29.0%、毛利率 61.0%、稅率 16.5%；未提供下一季單季指引，管理層提醒記憶體成本將壓下半年毛利（numbers.latest_quarter_kpis.items[5]，as_of Q3 FY2026（公告於 2026-10-28））
  - 註記：FY1 EPS 共識 10.49（dd_numbers_extra.py 10-31 快照，指引高於共識）
- `f_kpi6`（q1_business）｜存貨＝2251.7 百萬美元｜期間與口徑：Q3 FY2026（2026-09-26 資產負債表）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：10-Q grmn-20260926（numbers.latest_quarter_kpis.items[6]，as_of Q3 FY2026（2026-09-26 資產負債表））
  - 註記：不適用
- `f_earnings_recency`（q1_business）｜最近一次財報日＝2026-10-28 date｜期間與口徑：2026-10-28／距今 4 個交易日｜kind：realized
  - 來源：—（numbers.earnings_recency，as_of 2026-10-28）
- `f_peer_grmn_gross_margin_pct`（q2_moat）｜GRMN 毛利率＝61.12 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.GRMN.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_grmn_operating_margin_pct`（q2_moat）｜GRMN 營業利益率＝28.82 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.GRMN.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_grmn_fcf_margin_pct`（q2_moat）｜GRMN FCF 利潤率＝18.61 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.GRMN.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_aapl_gross_margin_pct`（q2_moat）｜AAPL 毛利率＝48.65 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.AAPL.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_aapl_operating_margin_pct`（q2_moat）｜AAPL 營業利益率＝33.17 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.AAPL.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_aapl_fcf_margin_pct`（q2_moat）｜AAPL FCF 利潤率＝29.28 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.AAPL.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_logi_gross_margin_pct`（q2_moat）｜LOGI 毛利率＝45.48 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.LOGI.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_logi_operating_margin_pct`（q2_moat）｜LOGI 營業利益率＝17.87 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.LOGI.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_logi_fcf_margin_pct`（q2_moat）｜LOGI FCF 利潤率＝19.25 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.LOGI.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_trmb_gross_margin_pct`（q2_moat）｜TRMB 毛利率＝69.8 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.TRMB.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_trmb_operating_margin_pct`（q2_moat）｜TRMB 營業利益率＝17.68 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.TRMB.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_trmb_fcf_margin_pct`（q2_moat）｜TRMB FCF 利潤率＝20.44 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.TRMB.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝10.49 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-10-31）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝11.35 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-10-31）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝12.74 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-10-31）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝8148.22 USD m｜期間與口徑：2026-11-03／yfinance revenue_estimate 0y 平均（6 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝9136.96 USD m｜期間與口徑：2026-11-03／yfinance revenue_estimate +1y 平均（8 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi3_fcf`（q4_capital）｜自由現金流（FCF）＝293 百萬美元｜期間與口徑：Q3 FY2026（季末 2026-09-26，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Garmin Q3 2026 新聞稿（營業現金流 394）（numbers.latest_quarter_kpis.items[3]，as_of Q3 FY2026（季末 2026-09-26，公告於 2026-10-28））
  - 註記：未取得
- `f_kpi4_sbc_gaap`（q4_capital）｜SBC 占 GAAP 營業利益＝7.3 %｜期間與口徑：Q3 FY2026（季末 2026-09-26，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：10-Q grmn-20260926 股東權益表 Q3 SBC 44.7 百萬美元 ÷ 營業利益 611.6（自行換算）（numbers.latest_quarter_kpis.items[4]，as_of Q3 FY2026（季末 2026-09-26，公告於 2026-10-28））
  - 註記：不適用
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝-2114.98 USD m｜期間與口徑：2026-11-03／yfinance 最新一季：總債務 224.49、現金 2339.47（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝192.7 m shares｜期間與口徑：2026-11-03／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝1.409 %｜期間與口徑：2026-11-03／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-11-03）
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝276.75 USD｜期間與口徑：2026-11-02（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-11-02（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝26.38 x｜期間與口徑：2026-10-31／分母＝FY1 EPS 10.49，分子＝快照價 276.75｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-10-31）
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝26.58 x｜期間與口徑：2026-11-02（RTH 收盤，UTC）／4 個年度端點內的分位＝90.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-11-02（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝90.0 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝6.76 x｜期間與口徑：2026-11-02（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝100.0 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝6.49 x｜期間與口徑：2026-11-02（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝100.0 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-11-02（RTH 收盤，UTC））
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝3.55 %｜期間與口徑：2026-07-30 → 2026-10-31／FY1 共識 EPS 10.13 → 10.49（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-10-31）
- `f_rsi14`（q5_valuation）｜RSI(14)＝45.09｜期間與口徑：2026-11-02（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-11-02（RTH 收盤，UTC））
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝16.95 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-11-02（RTH 收盤，UTC））

### findings_digest 中方向為負或來源衝突的條目（13 條）
- `competitive_share_entrants#0`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K 列出各業務主要對手（健身：Apple、Coros、Huawei、Oura、Whoop 等；航空：Honeywell、Collins 等；船用：Furuno、Raymarine 等），並指出現有與新興對手能複製部分功能，部分 OEM 客戶可能自製，可能造成降價與市占流失。
  - 來源：SEC EDGAR 10-K FY2025 Item 1 / 1A（as_of 2026-02-18）｜affects：moat_trend、decision_inputs.bear
- `customer_second_source#0`（customer_second_source｜方向 -｜狀態 ok）：Garmin 10-K 風險因素揭露：部分 OEM 客戶可能自行開發目前向 Garmin 採購的設備與零組件（in-house）；未點名具體客戶，亦無已發生事件。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-18）｜affects：moat_trend、thesis.R、decision_inputs.bear
- `customer_concentration_credit#1`（customer_concentration_credit｜方向 -｜狀態 ok）：10-K 風險因素：大客戶可能利用議價地位要求更多促銷等措施而壓低毛利率，失去任一大客戶可能對業務、財務與營運結果造成重大不利影響。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A Risk Factors（as_of 2026-02-18）｜affects：thesis.R、decision_inputs.bear
- `supply_demand_durability#2`（supply_demand_durability｜方向 -｜狀態 ok）：Garmin 管理層提及記憶體成本壓力，以漲價、自製與規模抵銷；產業 DRAM 供給緊缺預期延續至2027
  - 來源：the5krunner Garmin price rises could be on the way in 2027（as_of 2026-10-28）｜affects：thesis.R、decision_inputs.bear
- `regulatory_antitrust#2`（regulatory_antitrust｜方向 -｜狀態 ok）：波蘭競爭機關UOKiK於2024年對Garmin Polska涉與經銷商反競爭協議(價格)展開調查並搜索，現況未確認。
  - 來源：UOKiK: Garmin equipment – investigation procedure and searches（as_of 2024-06-19）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：10-K FY2025 揭露 Garmin 在台灣、中國等多地製造與採購，新增或提高關稅／貿易限制可能對業務、財務與營運成果造成重大不利影響；毛利率亦受關稅影響波動
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-18）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#1`（reg_tariff_export｜方向 -｜狀態 ok）：2026 Q1 10-Q：marine 毛利率年減 200bp，主因關稅成本上升
  - 來源：SEC EDGAR 10-Q 2026-03-28（as_of 2026-04-29）｜affects：valuation、decision_inputs.bear
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：Garmin 10-K 摘要：消費性產品主要製造廠位於台灣，暴露於兩岸地緣風險；另在美、歐、中有較小廠區
  - 來源：Stock Titan GRMN 10-K summary (FY2025)（as_of 2026-02-18）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：風險因子摘要：部分半導體、LCD、記憶體、電池、微處理器供應商為單一來源，曾發生短缺；緩解靠安全庫存與垂直整合
  - 來源：TradingView GRMN SEC 10-K report summary（as_of 2025-02-19）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#2`（geo_supply_chain｜方向 -｜狀態 ok）：Q4 2025 法說：為因應記憶體成本壓力刻意建庫存；2026 毛利率指引58.5%，主要風險為記憶體成本與高關稅
  - 來源：Motley Fool Garmin Q4 2025 earnings transcript（as_of 2026-02-18）｜affects：thesis.R、valuation
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：10-K 風險因素：競爭者已能複製部分產品功能或更快回應新技術；部分 OEM 客戶可能自行開發目前向 Garmin 採購的設備與零組件；公司可能無法使新產品適應新興技術。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-18）｜affects：moat_trend、decision_inputs.bear
- `substitute_technology#1`（substitute_technology｜方向 -｜狀態 ok）：10-K 風險因素：多項產品依賴 GNSS 與第三方衛星網路（Iridium、Skylo）；干擾（jamming）與欺騙（spoofing）可能損害定位功能。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-18）｜affects：thesis.R
- `substitute_technology#2`（substitute_technology｜方向 -｜狀態 ok）：車用導航業務因智慧型手機導航普及而喪失優勢；Garmin 靠非車用市場（航空、海事、戶外）多角化存活。
  - 來源：Sure Dividend GRMN 分析報告（as_of 2026-06-03）｜affects：moat_trend

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 2 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/GRMN_20261103/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":481.0,"bear_5y_price":166.5,"p_bull_pct":25,"p_bear_pct":30,"upside_5y_pct":25.6,"ev5y_pct":18.0,"irr_base_pct":4.7,"asym_ratio":1.5,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":10.49,"pe":26.38,"basis":"FY2026E（FY1）Koyfin 共識 EPS 10.49 美元、股價 276.75；終端倍數同用前瞻一年口徑，套在 FY2031E"},"eps":{"bull":[11.8,13.4,15.0,16.7,18.5],"base":[11.3,12.5,13.6,14.7,15.8],"bear":[10.2,9.7,10.1,10.6,11.1]},"pe":{"bull":26,"base":22,"bear":15},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":1.409,"net_buyback":0.1},"second_stage":{"bull_cagr_pct":10,"base_cagr_pct":7},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### GRMN_Q2_2026_Earnings_Call_20260729.md
- 2026-07-29｜CEO｜guidance：CEO 宣布上修 2026 全年營收與 pro forma EPS 財測（原話："We now expect 2026 revenue of approximately $8.05 billion"）
- 2026-07-29｜CFO｜guidance：CFO 說明全年毛利率財測上修，且已納入下半年記憶體成本（原話："increased our gross margin estimate to approximately 59.7%"）
- 2026-07-29｜CFO｜guidance：CFO 給出全年營業利益率約 27%，較前次財測高 150bp（原話："approximately 27%, 150 basis points higher"）
- 2026-07-29｜CFO｜guidance：CFO 將 pro forma 有效稅率財測由 16% 調為 16.5%（原話："effective tax rate of 16.5%"）
- 2026-07-29｜CFO｜guidance：CFO 給出全年自由現金流財測（原話："full year 2026 free cash flow to be approximately $1.4"）
- 2026-07-29｜CEO｜margin：CEO 說毛利率與營業利益率擴張多數來自產品組合，另含 2,100 萬美元關稅退款（原話："Margins also benefited from a $21 million tariff refund"）
- 2026-07-29｜CFO｜margin：CFO 給出 Q2 合併毛利率與年增幅（原話："margin was 62.4%, a 360 basis point increase"）
- 2026-07-29｜CEO｜margin：CEO 說明「mix」的定義：較高毛利的新產品在銷售組合中占比提高（原話："products in our families that come out at higher margins"）
- 2026-07-29｜CFO｜margin：CFO 說明毛利率財測不含 Q2 已認列以外的額外關稅退款（原話："any additional benefit related to tariff refunds"）
- 2026-07-29｜CEO｜margin：CEO 說 Marine 毛利率擴張主因為關稅退款（原話："The primary driver of margin expansion was the tariff refund"）
- 2026-07-29｜CEO｜margin：CEO 說 Auto OEM 毛利率擴張來自年度累計成本回收於本季認列為營收（原話："year-to-date cost recoveries that were recognized as"）
- 2026-07-29｜CEO｜risk：CEO 承認記憶體成本是逆風（原話："we recognize that's a headwind"）
- 2026-07-29｜CEO｜risk：CEO 說記憶體策略性庫存使高價成本尚未進財報，預期下半年開始影響（原話："expect that to start to impact us in the back half"）
- 2026-07-29｜CEO｜risk：CEO 說其他零組件在 AI 需求下也都承壓，但變動較小（原話："certainly under pressure because of the AI demand"）
- 2026-07-29｜CEO｜commitment：CEO 表示將用處理關稅的同一套做法因應記憶體成本（原話："same playbook with memory as we did with tariffs"）
- 2026-07-29｜CEO｜commitment：CEO 表示利潤率策略不倒退（原話："it's never our strategy to go backwards."）
- 2026-07-29｜CEO｜guidance：CEO 預期 Outdoor 下半年營收表現轉強，全年成長優於 2025（原話："stronger revenue performance in the back half of 2026"）
- 2026-07-29｜CEO｜guidance：CEO 表示 Marine 全年成長預期與去年一致（原話："growth that is consistent with that of the prior year"）
- 2026-07-29｜CEO｜guidance：CEO 預期 Fitness 為 2026 合併成長最大貢獻者（原話："continue to expect the Fitness segment will be the strongest"）
- 2026-07-29｜CEO｜customer：CEO 說 Auto OEM 下半年營收將下滑並回到營業虧損，直到 2027 年 Mercedes-Benz 新專案（原話："we are expecting revenue to decline and the return to an"）
- 2026-07-29｜CEO｜customer：CEO 說 BMW 量已達高峰，預期 2027 年 Auto OEM 回到成長（原話："auto OEM would again return to growth"）
- 2026-07-29｜CEO｜product：CEO 稱 CIRQA 上市後反應優於預期（原話："very strong, ahead of our expectations"）
- 2026-07-29｜CEO｜product：CEO 說 CIRQA 內建 Garmin Connect 全部功能，Connect+ 為可加購（原話："They can certainly add the additional features of Connect+"）
- 2026-07-29｜CEO｜product：CEO 對是否進入其他穿戴形態不評論產品路線圖（原話："I won't comment specifically on our product road map."）
- 2026-07-29｜CEO｜product：CEO 稱 AXIS 反應強烈並自述市場上無類似產品（原話："There's really nothing else like it out on the market"）
- 2026-07-29｜CEO｜product：CEO 稱 JL Audio Primacy 屬高度專業產品，拉貨需要時間（原話："going to take some time to really see the pull-through"）
- 2026-07-29｜CEO｜competition：CEO 稱 LiveScope 技術與市場其他產品有區隔（原話："further separating us from others in the market"）
- 2026-07-29｜CEO｜capital_allocation：CEO 宣布收購 TrainingPeaks 與 TrainHeroic，納入 Fitness 部門（原話："strategic acquisition of TrainingPeaks and TrainHeroic"）
- 2026-07-29｜CEO｜capital_allocation：CEO 說收購不考慮傳統綜效，著眼於 360 度使用者體驗（原話："we're really not thinking about any of those"）
- 2026-07-29｜CFO｜capital_allocation：CFO 報告 Q2 股利金額（原話："paid dividends of approximately $202 million"）
- 2026-07-29｜CEO｜capital_allocation：CEO 說明泰國廠首期規模與潛在產能（原話："has a potential of doubling our"）
- 2026-07-29｜CEO｜commitment：CEO 表示泰國廠預計年底前完工、2027 年初啟用（原話："finished towards the end of the year"）
- 2026-07-29｜CEO｜customer：CEO 說明 Truemed HSA 合作為新通路，不按客戶量化（原話："we don't quantify results by customer"）
- 2026-07-29｜CEO｜customer：CEO 稱商務航空 OEM 積壓訂單近乎紀錄（原話："OEMs are sitting on pretty much"）

### GRMN_Shareholder_Analyst_Call_Garmin_Ltd_20260605.md
- 2026-06-05｜CEO Clifton Pemble｜margin：CEO 回顧 2025 全年營收成長 15%、達 72.5 億美元（原話："Revenue increased 15% to $7.25 billion, a new record"）
- 2026-06-05｜CEO Clifton Pemble｜margin：CEO 稱 2025 營業利益率擴張至 25.9%（原話："Operating margin expanded to 25.9%"）
- 2026-06-05｜CEO Clifton Pemble｜guidance：CEO 提及 2026 Q1 營收與營業利益皆雙位數成長（回顧，未提供全年財測）（原話："both revenue and operating income during the opening"）
- 2026-06-05｜CEO Clifton Pemble｜commitment：CEO 表示有信心公司長期成功（原話："I'm confident we are well positioned for long-term success."）
- 2026-06-05｜CEO Clifton Pemble｜product：CEO 提及 Phoenix 8 Pro 獲 MWC 2026 評為最佳連網裝置（原話："recognized as the best connected device"）
- 2026-06-05｜CEO Clifton Pemble｜product：CEO 提及航海電子協會連續第 11 年評為年度製造商（原話："Manufacturer of the Year by the National Marine"）
- 2026-06-05｜CEO Clifton Pemble｜customer：CEO 提及產品支援連續第 22 年排名第一（航空領域）（原話："ranked #1 in product support for the 22nd consecutive year"）
- 2026-06-05｜General Counsel Joshua Maxfield｜capital_allocation：議案 3：每股 4.20 美元現金股利，自資本公積分 4 期支付（原話："$4.20 per outstanding share to be paid out of"）
- 2026-06-05｜Vera Negali (vote counter)｜capital_allocation：議案 3 股利案獲 99.91% 贊成（原話："has been approved with 99.91% of the votes cast."）
- 2026-06-05｜General Counsel Joshua Maxfield｜capital_allocation：截至 2026-05-22 在外流通股數（原話："192,822,422 shares of Garmin Limited issued"）
- 2026-06-05｜General Counsel Joshua Maxfield｜capital_allocation：在外流通股數不含庫藏股 2,078,543 股（原話："excludes 2,078,543 treasury shares"）
- 2026-06-05｜Vera Negali (vote counter)｜risk：董事長 Min Kao 連任得票 93.56%（原話："approved with 93.56% of the votes cast."）
- 2026-06-05｜Vera Negali (vote counter)｜risk：六位董事提名人中最低得票 86.35%（原話："86.35% of the votes cast."）

### 問答異常語氣（迴避／改口／保留）
- GRMN_Q2_2026_Earnings_Call_20260729.md｜問：Erik Woodring 追問 mix 是否為可持續的利潤率順風、未來 1 至 3 年的持續性｜答法：未直接回答持續性或給數字，改談記憶體逆風與 mix 的一般性定義
- GRMN_Q2_2026_Earnings_Call_20260729.md｜問：Erik Woodring 詢問是否擴展到其他穿戴形態｜答法：表明不評論產品路線圖，僅以過往擴張紀錄泛稱

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 3 | 2 |
| customer_second_source | found | 1 | 1 |
| customer_concentration_credit | found | 2 | 0 |
| supply_demand_durability | found | 3 | 2 |
| regulatory_antitrust | found | 3 | 3 |
| reg_tariff_export | found | 3 | 2 |
| geo_supply_chain | found | 3 | 2 |
| end_markets | found | 3 | 2 |
| substitute_technology | found | 4 | 2 |
| channel_business_model_shift | found | 3 | 2 |
| capital_markets_pricing | found | 2 | 2 |
| major_events | found | 3 | 5 |

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260730","verdict":"觀望","role":"追蹤","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"Fitness 段在出貨量收縮的品類裡持續拿高階份額，且成長以有機為主而非併購買來"},{"id":"H2","text":"59% 以上的毛利率是結構性的（組合升級 ＋ 垂直整合 ＋ 泰國廠），不是一次性的（$21M 關稅退款 ＋ 記憶體策略庫存時點）"},{"id":"H3","text":"Auto OEM 熬過 BMW 量峰到 Mercedes 量產之間的空窗後回到成長並轉正"}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"記憶體成本全年攤入 ＋ 無關稅退款 → 毛利率 YoY 轉負。DRAM LPDDR5X 報價漲幅達 89%、DDR4 達 51%（AI／HBM 排擠消費級產能）；TrendForce（2026-07-21）稱 NAND 供給緊張要到 2027 下半年才鬆；Samsung 對 DRAM 合約客戶 2026Q3 調漲約 20%。管理層自承策略性記憶體庫存撐完上半年、下半年開始吃到"},{"id":"R2","text":"Outdoor 段（最高毛利 65.8%）的結構性衰退擴散。Q1 26 −5%、Q2 26 −2%，近四季三負，公司歸因「消費車機與探險錶」；下半年改善承諾與上半年 −3.4% 的算術難以相容"},{"id":"R3","text":"Apple／Samsung 把健康功能免費推給存量機 ＋ Whoop／Oura 佔住恢復力品類 → 高階穿戴 ASP 下滑。Apple watchOS 26 高血壓提示與睡眠分數以軟體更新推給 Series 6+／9+ 存量機；Counterpoint 稱 Apple 在 2026Q1 出貨量收縮的市場中仍擴大份額、並拿下邊緣 AI 手錶約 90% 出貨；Whoop 2025 營收 $1.1B／估值 $10.1B，Oura 2025 約 $1B → 2026E 約 $2B／估值 $11B 且已密件申請 IPO"},{"id":"R4","text":"消費硬體同業倍數收斂。相對「高毛利品牌消費硬體」同 tier（Logitech 16.6x／Amer Sports 22.9x／YETI 15.4x，中位 16.6x）溢價 +78%；相對「高 ROIC 利基複利」tier（Apple 35.0x／TransDigm 29.3x／Honeywell 24.2x，中位 29.3x）折價 −1%。Garmin 的倍數完全取決於市場把它歸在哪一 tier"}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"價格回落至 fwd PE ≤25x（FY27 自建 EPS $11.05 → 約 $276）且 2027-02 給出的 FY27 毛利率指引 ≥59.0%；兩條同時成立才重跑完整 DD","irr_base_pct":3.5,"ev5y_pct":12.9,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"追蹤","signal":"B","val":"🔴","ma":"✅","trap":"🟢","moat_trend":"→","runway_post_y5":"🟡","asym_ratio":1.4,"ev5y_pct":12.9,"irr_base_pct":3.5,"max_dd_pct":-55.0,"bull_5y_price":455.0,"bear_5y_price":160.0,"p_bull_pct":25.0,"p_bear_pct":30.0,"rearm_trigger":"價格回落至 fwd PE ≤25x（FY27 自建 EPS $11.05 → 約 $276）且 2027-02 給出的 FY27 毛利率指引 ≥59.0%；兩條同時成立才重跑完整 DD","price_at_dd":294.83,"archetype":"品質複利成長","cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"GRMN","date":"2026-11-03","schema":"v15.0","contract":"v19","company_name":"Garmin Ltd."},"oneliner":"Garmin 在下滑的穿戴市場持續拿份額、利潤率創高，但 2026 年 61% 毛利率含關稅退款與低價記憶體庫存，管理層已預告 2027 回到歷史區間；現價約 24 倍 FY2027 共識，要 EPS 年增約 12.5% 或倍數不降才有 10% 年報酬，等 230 美元以下或 2027-02 指引再看","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/GRMN_20261103/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/GRMN_20261103/scenario.json","answers":{"q1_business":{"verdict":"賺的是運動、戶外、航空、船用玩家願意為專業功能多付的錢；利潤卡在自有工廠的垂直整合與高階產品組合，Fitness＋Outdoor 貢獻約四分之三營業利益，車用 OEM 是唯一虧損段","reasoning":"Q3 2026 營收 19.86 億美元（+12%），GAAP 營業利益 6.12 億、營業利益率 30.8%，毛利率 63.3%（含 3,300 萬美元關稅退款）。分部：Fitness 6.94 億（+16%，毛利率 63%／營業利益率 33%）、Outdoor 5.97 億（+20%，68%／39%）、Marine 3.10 億（+16%，64%／30%）、Aviation 2.53 億（+5%，78%／26%）、Auto OEM 1.32 億（−20%，毛利率 16%、營業虧損 1,200 萬）。Fitness＋Outdoor 占營收 65%、營業利益約 76%。全年指引：營收約 81.5 億、毛利率 61%、營業利益率 29%、pro forma EPS 約 10.80 美元。客戶不集中：前十大占 20%–25%，無單一客戶超過 10%；直營超過 10%，訂閱與服務仍低於 10%。單點依賴在供給端：消費產品主要在台灣自有工廠製造，記憶體等部分零組件為單一來源，管理層稱產能已到上限，泰國廠 2027Q1 才投產。產業時鐘判 II 擴張：註冊量高於進貨、零售商 Q4 拉貨強，Fitness、Outdoor、Marine 雙位數成長，但 Marine 終端市場偏軟（油價高、買家觀望）。供需持久性：健康與運動穿戴需求屬結構性持久，記憶體成本屬週期性、預期延續到 2027 後可反轉。產業態勢判雙向拉鋸：Garmin 份額上升（Omdia 11%→15%），但對手在補功能、部分 OEM 客戶可能自製，另有關稅與台灣集中兩個結構變數。","fact_refs":["f_kpi0_gaap","f_kpi1_gaap","f_kpi2_gaap","f_kpi5_fy2026","f_kpi6","f_earnings_recency"],"verdict_values":{"revenue_quality":"以硬體一次性銷售為主，訂閱與服務收入仍低於總營收 10%；Q3 註冊量高於進貨，通路沒有塞貨；Q3 毛利含 3,300 萬美元關稅退款，屬一次性","unit_econ_note":"Q3 各段毛利率 63%–78%（車用 OEM 16%），研發占營收 15.3%（TTM，Apple 為 9.2%），台幣走弱與規模壓低產品成本","archetype":{"primary":"品質複利成長","secondary":null,"confidence":"中","fingerprint":"淨現金、營業利益率 29%、營收四年年複合約 14%，但毛利受記憶體等零組件成本循環影響"},"industry":{"clock_phase":"II","sd_verdict_source":"需求面結構性持久（健康與運動穿戴、新用戶占比高、Connect+ 續訂強）；成本面週期性將反轉（記憶體短缺預期延續到 2027，供給可逆性高）。來源：Q3 2026 法說（2026-10-28）與 the5krunner（2026-10-28）","bargaining":{"up":"對上游轉弱：記憶體、半導體、LCD 部分單一來源，AI 需求讓記憶體廠議價力上升，公司以安全庫存與預付款換供給","down":"對下游穩定：前十大客戶占 20%–25%、無單一客戶超過 10%，直營超過 10%；大型零售可要求加碼促銷壓毛利","geo":"消費產品主要在台灣自有工廠製造，泰國廠 2027Q1 投產後分散；APAC 成長 4%，中國市場疲弱"},"profit_pool_dir":"利潤池短期往上游記憶體廠移動（管理層預告 2027 毛利率回到歷史區間）；下游通路分配穩定","tam_table":{"expanded":false,"reason":"事實表未涵蓋穿戴 TAM、滲透率與利潤池占比；只有份額（Omdia 15%、Counterpoint 5.6%，口徑不同），份額已寫進護城河段，滲透率列資料缺口"}}}},"q2_moat":{"verdict":"護城河方向判擴大（執行面）：兩家機構的出貨統計都顯示 Garmin 在下滑的穿戴市場拿份額，主要分部毛利率扣除關稅退款仍擴張；定價權判持平。評分執行 9、定價 7","reasoning":"機制：垂直整合（自有台灣工廠，記憶體短缺期靠安全庫存與預付款保供給，靠全公司規模取得航空用的 PCB 與線材）＋運動戶外專業功能與 Connect 資料累積讓用戶換機留在 Garmin（fēnix 首波需求以跨代換機的舊用戶為主）＋航空認證與改裝存量（G1000 King Air 改裝破 1,000 套、Autoland 2,500 架）＋船用經銷商口碑（NMEA 連 12 年年度製造商）。方向：執行面擴大——Omdia 2Q26 Garmin 份額 11%→15%、Apple 48%→46%，Counterpoint 出貨 +11%；Q3 法說中分析師與管理層都指出 Aviation、Marine（扣除退款）、Outdoor、Fitness 毛利率年增。定價權持平——CEO 把漲價列為抵銷記憶體成本的工具之一但不承諾，毛利擴張主要來自組合、規模與台幣走弱。同業（TTM）：營業利益率 28.8%，高於 LOGI 17.9%、TRMB 17.7%，低於 AAPL 33.2%；毛利率 61.1% 高於 AAPL 48.7%，研發密度 15.3% 也較高。事實表無同業 ROIC，以營業利益率代理；GRMN 自身營業利益率由 2022 年 21.2% 升到 TTM 28.8%，同業歷史值事實表未涵蓋，差距方向無法驗證。當期稅後營業利益率約 24%（28.8%×（1−16.5%）），投入資本周轉率事實表未涵蓋。反例：fēnix 9 屬產品週期，份額上升可能隨換機潮退去；兩家機構口徑差很大（15% 對 5.6%）。","fact_refs":["f_peer_grmn_gross_margin_pct","f_peer_grmn_operating_margin_pct","f_peer_grmn_fcf_margin_pct","f_peer_aapl_gross_margin_pct","f_peer_aapl_operating_margin_pct","f_peer_aapl_fcf_margin_pct","f_peer_logi_gross_margin_pct","f_peer_logi_operating_margin_pct","f_peer_logi_fcf_margin_pct","f_peer_trmb_gross_margin_pct","f_peer_trmb_operating_margin_pct","f_peer_trmb_fcf_margin_pct"],"verdict_values":{"moat":{"mechanism":"垂直整合（自有台灣工廠）＋運動戶外專業功能與 Connect 資料累積的轉換成本＋航空認證與改裝存量＋船用經銷商口碑","execution":9,"pricing":7,"grade":"B","trend":"↑","trend_evidence":"執行面擴大：Omdia 2Q26 份額 11%→15%（Apple 48%→46%），Counterpoint 出貨 +11%，Q3 主要分部毛利率扣除關稅退款仍擴張；定價權持平：管理層把漲價列為工具之一但不承諾。反例：fēnix 9 屬產品週期，首波需求以舊用戶換機為主，2027 下半年換機潮退去後要再驗","competitor_notes":[{"name":"AAPL","strategy_note":"營業利益率 33.2%、FCF 利潤率 29.3% 都高於 GRMN，靠 iPhone 綁定與規模；手錶是 iPhone 配件，Omdia 份額 48%→46% 顯示它沒有在運動戶外高階段擠掉 Garmin"},{"name":"LOGI","strategy_note":"毛利率 45.5%、營業利益率 17.9%，代表一般消費周邊的利潤水準；GRMN 高出約 11pp，說明它不是被當成普通消費硬體在賣"},{"name":"TRMB","strategy_note":"毛利率 69.8% 高於 GRMN，但研發密度 17.3%、營業利益率只有 17.7%；同是定位技術，GRMN 靠消費規模攤薄費用"},{"name":"Huawei","strategy_note":"Counterpoint 2Q26 全球份額 22% 居首；GRMN 的 APAC 只成長 4%，管理層歸因中國市場疲弱，是 Huawei 主場的直接對照"}],"peer_na_reason":"事實表無同業 ROIC 與歷史利潤率，以 TTM 營業利益率代理","threats":[{"level":"🟡","text":"Apple／Samsung／Huawei 以手機生態補齊運動健康功能，Coros、Whoop、Oura 等專業品牌複製部分功能；目前份額數據顯示未造成損害","p":"30%","evidence_refs":["competitive_share_entrants#0","substitute_technology#0"]},{"level":"🟡","text":"OEM 客戶自製目前向 Garmin 採購的設備與零組件（車用 domain controller、航空 OEM）；10-K 未點名客戶、無已發生事件","p":"20%","evidence_refs":["customer_second_source#0"]},{"level":"🟡","text":"大型零售客戶要求更多促銷壓低毛利率，失去任一大客戶會有重大影響；前十大占 20%–25%","p":"25%","evidence_refs":["customer_concentration_credit#1"]}],"roic_durability":{"quadrant":"高利益率（稅後營業利益率約 24%）×周轉率待補（事實表未涵蓋投入資本）","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者、決策者、付款者都是消費者本人，三角色一致；但運動錶屬想要而非需要，可延後購買（Marine 終端偏軟、油價高讓買家觀望）。代理讀數：Q3 註冊量高於進貨、零售商 Q4 拉貨強，健康需求有世代與政策順風，判中性偏正"},{"item":"決策層級","level":"🟢","text":"替代性在個人裝置與機身層級衡量：fēnix 首波買家多為跨一代以上的舊用戶換機，Connect+ 免費期後續訂強；航空端改裝要重新認證（G1000 King Air 改裝破 1,000 套），換供應商成本高。漲價後流失率事實表未涵蓋"},{"item":"價值鏈分配","level":"🟡","text":"自有工廠吃下製造環節利潤，但 AI 需求讓記憶體廠議價力上升，2027 毛利率回到歷史區間就是價值往上游移；下游前十大客戶占 20%–25%、無單一客戶超過 10%，大型零售可要求促銷，判中性"},{"item":"社會容忍度","level":"🟢","text":"非必需品、無價格管制與監管授權依賴，漲價不構成社會或政治議題；相關的只有 FCC 與歐盟產品認證，屬一般性要求"}],"roiic":"代理約 119%（2022→2025 淨利增加 6.9 億美元 ÷ 2023–2025 累計〔淨利−FCF〕5.8 億）；前瞻假設約 50%","reinvest_rate":"代理 2023–2025 約 13%；2026E 約 47%（淨利約 20.8 億−FCF 約 11 億）；前瞻假設約 25%","endo_ceiling":12.0,"formula_note":"內生成長率＝增量報酬×再投資率；再投資率原式＝（資本支出−折舊攤銷＋營運資金變動＋收購淨額）÷稅後營業利益，事實表無折舊攤銷、營運資金變動與投入資本，改用（淨利−FCF）代理淨再投資、淨利代理稅後營業利益，SBC 被加回使再投資低估。歷史代理 119%×13%≈16%，泰國廠與存貨策略墊高再投資、增量報酬應下降，前瞻取 50%×25%≈12%（兩個比率是假設，非事實表數字）"}}}},"q3_growth":{"verdict":"成長跑道判中等：份額還在擴大，CIRQA 與 Connect+ 開出新客群，但滲透率事實表未涵蓋，第二條曲線規模仍小（訂閱與服務低於營收 10%）","reasoning":"成長以量為主：2025 年穿戴成長主要來自量而非價，2026Q1 CEO 稱出貨量帶動份額提升；再加上高階組合。併購（TrainingPeaks／TrainHeroic）不重大，回購可忽略。共識 EPS：FY2025A 8.59→FY2026E 10.49→FY2027E 11.35→FY2028E 12.74，三年年複合 14.0%（Koyfin 快照，EPS 家數事實表未涵蓋）；營收共識 FY2026 81.5 億、FY2027 91.4 億美元（6／8 位分析師）。內生上界約 12%，缺口約 2pp 歸因於利潤率擴張：FY2026 營業利益率由 25.9% 升到指引 29%，已在 FY2026 兌現；FY2026→FY2028 共識年複合 10.2%，落在上界內，不依賴倍數重估。跑道：以份額代理，Omdia 15%、Counterpoint 5.6%；新曲線有 CIRQA（無螢幕手環，擴大可及市場、需求超出預期）、Connect+（成長快於所在分部、免費期後續訂強）、Mercedes domain controller（2027 量產），但規模都還小，判中等。AI 取代風險低：產品長在自有感測器與硬體上，AI 用在 Connect+ 洞察屬強化；AI 資料中心需求推高記憶體價格是成本面的間接衝擊。衰退信號十項亮一項（2022→2025 EPS 年複合高於營收 5.2pp），FCF÷淨利 2026E 約 0.53 列警示。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_kpi5_fy2026"],"verdict_values":{"growth":{"driver_mix":"量為主（穿戴出貨與份額提升）＋高階組合；併購（TrainingPeaks／TrainHeroic）不重大；回購可忽略","runway_years":"事實表未涵蓋滲透率，無法推算；以份額代理：Omdia 智慧手錶 15%、Counterpoint 5.6%","runway_post_y5":"🟡","endo_ceiling_basis":"引護城河段再投資空間：前瞻增量報酬約 50%×再投資率約 25%≈12%；歷史代理值 119%×13%≈16%，因泰國廠與存貨策略墊高再投資、增量報酬應下降，取 12%","segments":[{"item":"Fitness","value":"Q3 6.94 億美元，+16%，毛利率 63%、營業利益率 33%，營業利益 2.31 億"},{"item":"Outdoor","value":"Q3 5.97 億美元，+20%，68%／39%，營業利益 2.33 億"},{"item":"Marine","value":"Q3 3.10 億美元，+16%，64%／30%，營業利益 0.94 億（含關稅退款）"},{"item":"Aviation","value":"Q3 2.53 億美元，+5%，78%／26%，營業利益 0.66 億"},{"item":"Auto OEM","value":"Q3 1.32 億美元，−20%，毛利率 16%，營業虧損 0.12 億；Q4 降幅相近，2027 靠 Mercedes 回到成長"},{"item":"來源","value":"Q3 2026 法說逐字稿（2026-10-28 CEO）與 8-K 新聞稿"}],"decay_signals":[{"item":"毛利率連 2 季年減","lit":false,"evidence":"Q2 +360bp、Q3 +420bp（含關稅退款）；Q4 起記憶體成本是下一個檢查點"},{"item":"核心市占近 12 個月縮減","lit":false,"evidence":"Omdia 2Q26 份額 11%→15%；Counterpoint 出貨 +11%"},{"item":"主力產品提價後銷量下滑","lit":false,"evidence":"事實表無提價與銷量對照；2025 穿戴成長主要來自量"},{"item":"EPS 年複合比營收高 5pp 以上","lit":true,"evidence":"2022→2025 EPS 19.4% 對營收 14.2%，差 5.2pp；前瞻 FY2025→FY2027 差約 2.6pp"},{"item":"FCF÷淨利連 2 年低於 0.75","lit":false,"evidence":"2025 年 0.82；2026E 約 0.53，FY2027 若仍低於 0.75 即亮"},{"item":"SBC÷營收高於 5% 且逐年上升","lit":false,"evidence":"Q3 約 2.3%"},{"item":"TAM 萎縮或被替代技術壓縮","lit":false,"evidence":"Omdia 新聞稿標題稱整體穿戴出貨 −2%，但轉向無螢幕手環與進階運動錶，兩者都是 Garmin 有產品的品類"},{"item":"產業估值倍數近 3 年系統性下移","lit":null,"evidence":"事實表未涵蓋同業倍數歷史"},{"item":"維護性資本支出占 FCF 超過 60%","lit":false,"evidence":"2026 資本支出約 5 億美元，含泰國新廠擴產，總額只占 FCF 約 45%；維護性占比事實表未涵蓋"},{"item":"停止投資新產能且營收 3 年內下滑","lit":false,"evidence":"泰國廠 2027Q1 投產，營收仍雙位數成長"}]}}},"q4_capital":{"verdict":"資本配置穩健但不積極：現金主要用在股利與為記憶體短缺墊高存貨，回購規模小且價位偏貴，股數持平；2026 年 FCF 轉換率跌到約 0.53 是要盯的點","reasoning":"FCF÷淨利：2023 年 0.92、2024 年 0.88、2025 年 0.82；2026 全年 FCF 指引由約 14 億（2026-07-29 CFO）下修到約 11 億美元（2026-10-28 CFO），以 pro forma EPS 10.80×192.7 百萬股≈淨利 20.8 億估算，轉換率約 0.53，原因是存貨（Q3 22.5 億）與記憶體預付款，加上資本支出約 5 億（含泰國廠）。SBC：Q3 4,470 萬美元，占營業利益 7.3%、約占營收 2.3%。現金去向：股利每季約 2.02 億（年 4.20 美元／股，殖利率 1.4%）；Q3 回購 4,100 萬，授權剩 4.07 億到 2028 年 12 月；流通股由 2026-05-22 的 192.82 百萬股到判斷日 192.7 百萬股，持平。淨現金約 21.1 億美元（不含長期有價證券；法說稱現金與有價證券約 41 億）。回購以約 26 倍 Fwd P/E 進行，買入收益率約 3.8%。","fact_refs":["f_kpi3_fcf","f_kpi4_sbc_gaap","f_net_debt_m","f_shares_diluted_m","f_dividend_yield_ttm","f_kpi6"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":false,"passed":null,"input":"TrainingPeaks／TrainHeroic 2026-07-20 完成，條件未揭露、對合併財報影響不重大，沒有可算的已實現報酬"},{"name":"buyback_yield","applicable":true,"passed":false,"input":"Q3 回購 4,100 萬美元，以 Fwd P/E 約 26.4 倍買入，買入收益率約 3.8%；10 年期殖利率事實表未涵蓋，要過門檻需 10 年期低於約 1.8%，判不過"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"流通股 2026-05-22 為 192.82 百萬股、判斷日 192.7 百萬股，淨稀釋約 0%；Q3 SBC 4,470 萬美元，占營業利益 7.3%"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長以有機為主、併購不重大；現金去向集中在股利（每季約 2.02 億美元）、資本支出（全年約 5 億）與存貨預付，回購規模小"}}}},"q5_valuation":{"verdict":"現價約 26 倍 FY2026、24 倍 FY2027 共識，要倍數維持 26 倍、EPS 年增約 9%，或倍數回到 22 倍、EPS 年增約 12.5%，才有 10% 年報酬；我的基本情境是 EPS 年增約 8.5%、終端 22 倍，年報酬約 6%，判偏貴","reasoning":"現價要求什麼：股價 276.75，Fwd P/E 26.4 倍（FY2026 共識 10.49）、24.4 倍（FY2027 共識 11.35）。扣掉約 1.5% 的股息與淨回購，10% 年報酬要五年後股價約 416 美元：倍數 22 倍需 FY2031 EPS 約 18.9（年增約 12.5%），倍數 26 倍需約 16.0（年增約 9%）。基本情境 EPS 年增約 8.5%、終端 22 倍，五年年報酬約 6%（EPS 複利 8.5%、倍數 −3.6%／年、股息與回購 1.5%），我不信現價隱含的組合。分母爭點：FY2026 EPS 含約 5,400 萬美元關稅退款（Q2 2,100 萬＋Q3 3,300 萬）、低價記憶體庫存與台幣走弱的好處，改以 FY2027 共識為主錨。歷史位置：trailing P/E 26.6 倍落在 4 個年度端點第 90 分位，P/S 6.76 倍、EV/S 6.49 倍都在第 100 分位。賣方目標價平均約 284–310 美元（多數早於 Q3 財報、口徑不一），現價低約 3%–11%，最高 370、最低平均 213（4 家、疑為舊資料），全距約 1.7 倍，對等待沒有構成反證。動能：RSI 45、26 週 +17%，未過熱。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_pe_current","f_pe_percentile","f_ps_current","f_ps_percentile","f_ev_s_current","f_ev_s_percentile","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_3m_fy1_pct","f_dividend_yield_ttm","f_rsi14","f_week26_return_pct"],"verdict_values":{"valuation":{"basis":"Fwd P/E（主錨 FY2027 共識 11.35 美元；FY2026 共識含關稅退款與低價記憶體庫存）","tier":"介於高毛利品牌消費硬體與高 ROIC 利基複利之間（前份同業分類）","peers":[{"item":"Logitech（高毛利品牌消費硬體）","value":"16.6 倍（前份 2026-07-30 記載，非本次事實表）"},{"item":"Amer Sports","value":"22.9 倍（同上）"},{"item":"YETI","value":"15.4 倍（同上）"},{"item":"Apple（高 ROIC 利基複利）","value":"35.0 倍（同上）"},{"item":"TransDigm","value":"29.3 倍（同上）"},{"item":"Honeywell","value":"24.2 倍（同上）"},{"item":"GRMN","value":"26.4 倍 FY2026 共識／24.4 倍 FY2027 共識（本次事實表）"}],"fwd_pe":26.38,"peg":1.88,"percentile_5y":null,"val_light":"🟠","val_light_derivation":"Fwd P/E 26.4 倍（FY2026 共識）、24.4 倍（FY2027 共識）；trailing P/E 26.6 倍在 4 個年度端點第 90 分位，P/S、EV/S 在第 100 分位；三年共識 EPS 年複合 14.0%（FY2025A 8.59→FY2028E 12.74），PEG 1.88 屬合理偏貴，若改看 FY2026→FY2028 的 10.2%，PEG 約 2.6。五年分位事實表未涵蓋（只有 4 個年度端點），留空。基本情境五年年報酬約 6%，要 10% 需倍數不降或 EPS 年增約 12.5%，判偏貴、未到極貴。短期以 12 個月後 FY2028E 基本情境 EPS 12.50×22 倍≈275 美元（−0.6%）、中期以 3 年後 FY2030E 14.70×22 倍≈323 美元（+16.9%）計","upside_short_pct":-0.6,"upside_mid_pct":16.9,"denominator_disputed":true,"denominator_note":"FY2026 EPS 含約 5,400 萬美元關稅退款（Q2 2,100 萬＋Q3 3,300 萬）、低價記憶體安全庫存與台幣走弱的好處，管理層已說 2027 毛利率回到歷史區間；便宜與否改看 FY2027 共識 11.35 美元（24.4 倍）"}}},"q6_how_wrong":{"verdict":"最可能看錯的是 FY2027 利潤率：管理層若又一次保守，基本情境偏悲觀；若記憶體短缺拖到 2028，Bear 30% 還不夠","reasoning":"可能看錯的兩個方向。太悲觀：2026 年指引連續上修（EPS 由 10.0 到 10.80，毛利率由年初 58.5% 到 61%），2027 的「回到歷史區間」可能又是保守說法；份額上升代表執行面在擴大。太樂觀：記憶體短缺若延續到 2028，加上 Mercedes 低毛利放量，營業利益率可能跌破 26%。最大回撤 −55%～−35%：事實表未涵蓋歷史最大回撤，下緣用 Bear 第二年 EPS 9.70×13.5 倍≈131 美元（−53%），上緣用 EPS 10.49 不跌但倍數回到約 17.2 倍≈180 美元（−35%）。壓力測試五項過三項：①淨現金約 21 億、總債務 2.2 億，營收急跌也無再融資壓力——過；②年股利約 8.1 億對 2026E FCF 約 11 億，覆蓋 1.36 倍——過；③毛利率回到 2023 年 57.5%、費用率維持 32%，以 FY2027 共識營收 91.4 億、稅率 16.5% 推得 EPS 約 10.1（不計利息收入），仍高於 2025 年 8.59——過；④倍數回到前份記載消費硬體同業 16.6 倍，10.49×16.6≈174 美元，跌 37% 超過 30%——不過；⑤主要製造集中台灣，泰國廠 2027Q1 才投產——不過。價值陷阱判中，依據見反證紀錄中論點失敗與股東經濟變差的條目。","fact_refs":["f_kpi5_fy2026","f_net_debt_m","f_consensus_eps_fy1","f_rev_consensus_fy2_m","f_rsi14","f_week26_return_pct"],"verdict_values":{"trap":{"verdict":"🟡","label":"利潤率高峰風險（EPS 成長快於營收），不是生意衰退型陷阱"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":10.49,"pe":26.38,"basis":"FY2026E（FY1）Koyfin 共識 EPS 10.49 美元、股價 276.75；終端倍數同用前瞻一年口徑，套在 FY2031E"},"eps":{"bull":[11.8,13.4,15.0,16.7,18.5],"base":[11.3,12.5,13.6,14.7,15.8],"bear":[10.2,9.7,10.1,10.6,11.1]},"pe":{"bull":26,"base":22,"bear":15},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":1.41,"net_buyback":0.1},"second_stage":{"bull_cagr_pct":10,"base_cagr_pct":7},"max_dd":{"lo":-55,"hi":-35,"basis":"事實表未涵蓋歷史最大回撤，改由情境樹推：下緣用 Bear 第二年 EPS 9.70×13.5 倍（Bear 15 倍再打九折）≈131 美元，較現價 −53%，取 −55%；上緣用 EPS 10.49 不跌但倍數回到約 17.2 倍（前份記載消費硬體同業中位 16.6 倍附近）≈180 美元，−35%。Bear 五年終點約 166.5 美元（−40%）落在範圍內","trigger_time":null},"basis":{"bull":"穿戴份額續升、Connect+ 與 CIRQA 擴大客群、Mercedes 車用量產與泰國廠擴產，FY2027 起營收年增 11%–13%，記憶體成本 2028 回落讓毛利率守在 60% 附近，EPS 年增約 12%；終端 26 倍，對照前份記載高 ROIC 利基複利同業中位 29.3 倍打九折","base":"營收年增 9%–10% 逐年放慢到 7%–8%，FY2027 毛利率回到約 58.5%、營業利益率約 27% 後持平，EPS 五年年增約 8.5%；終端 22 倍，介於前份記載消費硬體同業 16.6 倍與利基複利 29.3 倍之間（2026-07-30 數字）","bear":"記憶體短缺延續到 2028、消費降溫與手機生態侵蝕，FY2027–FY2028 EPS 回落到 9.7–10.2 美元，之後低速回升，FY2031 只有 11.1；終端 15 倍，對齊前份記載的 YETI 15.4 倍、Logitech 16.6 倍，也是成長熄火到約 5% 的倍數"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"管理層 2026-10-28 預告 2027 毛利率回到歷史區間，記憶體新貨按市價採購；產業 DRAM 緊缺預期延續到 2027；Q4 2025 法說就為記憶體刻意建庫存","assumption":"費用槓桿與垂直整合能抵銷毛利率下滑，營業利益率守在 26% 以上","consequence":"若營業利益率回到 2022–2023 年的約 21%，EPS 停在 9–10 美元，倍數回到 15 倍，股價約 135–150 美元，五年後虧近 50%","ruling":"部分採納：放進 Bear 30% 與唯一致命點；反駁點是 2025 年毛利率 58.7% 時營業利益率已有 25.9%，要回到 21% 得營收停滯、費用率回升","watch":"季度毛利率與營業利益率；2027-02 FY2027 指引","evidence_refs":["supply_demand_durability#2","geo_supply_chain#2"],"fact_refs":["f_kpi5_fy2026","f_kpi2_gaap"]},{"view":"論點失敗","evidence":"10-K 承認對手已能複製部分功能、部分 OEM 客戶可能自製；Garmin 當年的車用導航就是被手機取代","assumption":"運動戶外專業功能（續航、GNSS、耐用）與 Connect 資料累積是手機生態補不齊的","consequence":"高階穿戴被 Apple／Samsung／Huawei 吃下，Fitness＋Outdoor（Q3 占營收 65%）成長歸零，倍數往消費硬體同業靠","ruling":"反駁：Omdia 2Q26 Garmin 份額 11%→15%、Apple 48%→46%，註冊量高於進貨，非 fēnix 產品的新用戶比重高；保留 R2 門檻監測","watch":"Omdia／Counterpoint 季度份額；Fitness 年增率","evidence_refs":["substitute_technology#2","competitive_share_entrants#0","substitute_technology#0","customer_second_source#0"],"fact_refs":["f_kpi0_gaap"]},{"view":"論點成功但股東經濟變差","evidence":"2026 全年 FCF 指引由約 14 億下修到約 11 億美元（存貨與預付款），資本支出約 5 億，Q3 存貨 22.5 億；Mercedes domain controller 放量但車用 OEM 毛利率只有 16%","assumption":"存貨與預付是記憶體短缺期的一次性墊款，2027 後回收","consequence":"營收與 EPS 照基本情境成長，但 FCF÷淨利停在 0.5–0.6，股利成長放緩、每股自由現金流落後 EPS；成長組合偏向低毛利車用，拖累整體報酬率","ruling":"部分採納：把 FY2027 FCF÷淨利 <0.75 設為出場指標；反駁點是 2023–2025 年轉換率 0.82–0.92","watch":"FY2027 現金流量表；季度存貨÷營收","evidence_refs":["geo_supply_chain#2","customer_concentration_credit#1"],"fact_refs":["f_kpi3_fcf","f_kpi6"]},{"view":"價格已反映太多","evidence":"P/S 6.76 倍、EV/S 6.49 倍都在 4 個年度端點最高位，trailing P/E 26.6 倍在第 90 分位，26 週漲 17%；前份記載高毛利消費硬體同業中位 16.6 倍、利基複利 29.3 倍，倍數取決於市場把 Garmin 歸哪一類","assumption":"市場持續給 26 倍並接受 2026 的高峰利潤率","consequence":"即使基本情境（EPS 年增 8.5%）兌現，倍數回到 22 倍的五年報酬只有約 6%／年","ruling":"採納：這是本次唯一卡住的條件","watch":"股價相對 230 美元；FY2027 共識 EPS","evidence_refs":["capital_markets_pricing#1"],"fact_refs":["f_ps_percentile","f_ev_s_percentile","f_pe_percentile","f_fwd_pe_latest","f_week26_return_pct"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 294.83 → 本次 276.75（-6.1%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=294.83","side_b":"本次 price_at_dd=276.75","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 294.83 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 294.83 美元：Bull 價 455、Bear 價 160，五年期望值 +12.9%，基準年化 3.5%，不對稱比 1.4","side_b":"本次情境、股價仍用 294.83 美元：Bull 價 481、Bear 價 166.5，五年期望值 +10.8%，基準年化 3.3%，不對稱比 1.21","ruling":"先換情境、股價不動：五年期望值少 2.1 個百分點，基準年化少 0.2 個百分點。不對稱比由 1.4 變為 1.21。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 294.83 美元：五年期望值 +10.8%，基準年化 3.3%，不對稱比 1.21","side_b":"本次情境、股價 276.75 美元：五年期望值 +18.0%，基準年化 4.7%，不對稱比 1.54","ruling":"再換股價、情境不動：起點價下跌 6.1%，五年期望值多 7.2 個百分點，基準年化多 1.3 個百分點，不對稱比由 1.21 升到 1.54。合計五年期望值比前份多 5.1 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"一致判斷：管理層前一季承諾的兌現度","cause":null,"prior_field":null,"side_a":"2026-07-29 CEO：Outdoor 下半年轉強、全年成長優於 2025；Auto OEM 下半年營收下滑並回到營業虧損；Fitness 是全年最大成長來源","side_b":"2026-10-28：Outdoor +20%（fēnix 9）、Auto OEM −20% 且虧損 1,200 萬美元、Fitness +16% 並重申全年最大貢獻，三項都照說的發生","ruling":"一致：管理層前一季的分部說法全數兌現，指引可信度加分，也代表 2027 毛利率回到歷史區間這句話要當真","evidence_level":"兩場法說逐字稿","settle_metric":"Q4 2026 分部營收","if_then":["若 Q4 2026 Outdoor 年增跌到個位數，表示 fēnix 9 換機潮比預期短，提前檢查 H1 門檻"],"evidence_refs":["end_markets#0"]},{"axis":"2027 毛利率：管理層預告回落 vs 2026 年每季都超出自己的指引","cause":null,"prior_field":null,"side_a":"2026-10-28 CEO／CFO：記憶體新貨按市價採購、Mercedes 放量帶來不利組合，2027 合併毛利率回到歷史區間（2022–2025 年 57.5%–58.7%）","side_b":"2026 年初（2026-02-18）毛利率指引 58.5%，2026-07-29 上修到 59.7%，2026-10-28 再上修到 61%；CEO 在 2026-07-29 說會用處理關稅的同一套做法應對記憶體，利潤率策略「不倒退」","ruling":"可調和、屬程度差異：毛利率會回落，不倒退指的是營業利益率；基本情境取 FY2027 毛利率約 58.5%、營業利益率約 27%，介於兩側之間","evidence_level":"管理層指引與歷史兌現紀錄","settle_metric":"2027-02 的 FY2027 毛利率與營業利益率指引","if_then":["若 FY2027 營業利益率指引 ≥27% 且 EPS 指引 ≥12.0 美元，基本情境改用 Bull 前兩年路徑重算，不必等到 230 美元","若 FY2027 EPS 指引 <10.80 美元，Bear 機率升到 40%，股價到 230 美元也不建首倉，等 2027Q1 實際毛利率"],"evidence_refs":["supply_demand_durability#2","geo_supply_chain#2"]},{"axis":"自由現金流指引下修","cause":null,"prior_field":null,"side_a":"2026-07-29 CFO：全年 FCF 約 14 億美元","side_b":"2026-10-28 CFO：全年 FCF 下修到約 11 億美元，因為現有存貨增加與記憶體預付款；資本支出約 5 億、Q3 存貨 22.5 億","ruling":"可調和：屬記憶體短缺期的保供給墊款，CFO 說預付款是逐家個案談；管理層沒給回收時點，標「未證、監測」，FY2027 FCF÷淨利仍 <0.75 就視為結構性","evidence_level":"兩場法說 CFO 發言","settle_metric":"FY2027 FCF÷淨利","if_then":["若 FY2027 FCF÷淨利 <0.75，H3 判削弱、Bear 機率升到 35%"],"evidence_refs":["geo_supply_chain#2"]},{"axis":"現在就買 vs 等價格（唯一卡住的條件是價格）","cause":null,"prior_field":null,"side_a":"現在就買的最強論證：①2026 年指引連續上修，年初毛利率指引 58.5% 最後做到約 61%，「回到歷史區間」可能又是保守說法；②在下滑的穿戴市場拿份額，泰國廠 2027Q1 解除產能上限；③淨現金約 21 億美元、殖利率 1.4%，股價較前份回落 6%，FY2027 共識只要 24.4 倍","side_b":"等待的理由：基本情境（EPS 年增約 8.5%、終端 22 倍）五年年報酬約 6%，要 10% 需倍數維持 26 倍或 EPS 年增約 12.5%；FY2027 的分母正是爭點，2027-02 指引前沒有可裁決的數據","ruling":"維持等待；卡住的是價格相對正常化後的獲利，不是生意本身。自我攻擊三點（保守指引、份額擴大、淨現金下檔保護）都不改變基本情境報酬低於 8% 的事實","evidence_level":"事實表估值與共識、兩場法說","settle_metric":"股價相對 230 美元；FY2027 EPS 指引","if_then":["若股價跌到 230 美元以下而 FY2027 指引未讓 EPS 年減，屬跌但基本面無損，重跑完整 DD 後首倉 2%，不當停損訊號","若股價先漲到 320 美元以上而 FY2027 指引尚未公布，不追","反向條件：若 FY2027 營業利益率指引 ≥27% 且 EPS 指引 ≥12.0 美元，以新分母重算後首倉 2%"],"evidence_refs":[]},{"axis":"估值與機率（股價 294.83→276.75）","cause":"價格變動","prior_field":["val","p_bull_pct","p_bear_pct"],"side_a":"前份 2026-07-30：股價 294.83，FY2026 共識 EPS 10.13，Fwd P/E 約 29.1 倍，估值判極貴；Bull 25%／Bear 30%；裁決觀望","side_b":"本次：股價 276.75（−6.1%），FY2026 共識上修到 10.49（三個月 +3.55%），Fwd P/E 26.4 倍、FY2027 共識 24.4 倍，估值降一級為偏貴；機率維持 25／45／30；裁決與角色依本次均線與估值輸入重算","ruling":"估值改善約三分之二來自股價回落、三分之一來自 EPS 上修；機率不動，因為 2027 毛利率正常化的新證據抵銷了份額上升的好消息","evidence_level":"事實表價格與共識快照","settle_metric":"Fwd P/E（FY2027 共識）","if_then":["若股價回到 300 美元以上而 FY2027 共識未上修，估值回到極貴一級，不追"],"evidence_refs":[]},{"axis":"護城河方向（穩定→擴大）","cause":"新證據","prior_field":["moat_trend"],"side_a":"前份判穩定：擔心 Apple／Samsung 用軟體更新把健康功能推給存量機、Whoop／Oura 占住恢復力品類、高階穿戴單價下滑","side_b":"本次判擴大：Omdia 2Q26 Garmin 份額 11%→15%、Apple 48%→46%；Counterpoint 出貨 +11%；Q3 Fitness +16%、Outdoor +20%，主要分部毛利率扣除關稅退款仍擴張","ruling":"改判擴大，只限執行面，定價權仍判持平。反例保留：fēnix 9 換機潮屬產品週期，若 2027 下半年 Fitness＋Outdoor 年增連 2 季跌破 5%，改回穩定","evidence_level":"兩家第三方出貨統計＋公司分部數據","settle_metric":"Omdia 季度份額；Fitness＋Outdoor 年增率","if_then":["若 Omdia 份額跌破 12%，護城河方向改回穩定，R2 時鐘改為 ⚡"],"evidence_refs":["competitive_share_entrants#1","competitive_share_entrants#2","end_markets#0","competitive_share_entrants#0"]},{"axis":"價值陷阱風險（低→中）","cause":"新證據","prior_field":["trap"],"side_a":"前份判低：衰退信號未亮","side_b":"本次判中：2022→2025 EPS 年複合 19.4% 高於營收 14.2% 達 5.2pp（利潤率帶動），管理層 2026-10-28 預告 2027 毛利率回到歷史區間；2026E FCF÷淨利約 0.53","ruling":"升到中：不是生意在衰退，而是近年 EPS 成長有一塊來自不會重複的利潤率擴張與關稅退款","evidence_level":"事實表年度財報＋法說","settle_metric":"FY2027 營業利益率；FY2027 FCF÷淨利","if_then":["若 FY2027 FCF÷淨利仍 <0.75，衰退信號亮第二項，維持中並把 Bear 機率升到 35%"],"evidence_refs":["geo_supply_chain#2"]},{"axis":"重新評估條件改寫（重跑完整 DD／首倉）","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"價格回落至 fwd PE ≤25x（FY27 自建 EPS $11.05 → 約 $276）且 2027-02 給出的 FY27 毛利率指引 ≥59.0%；兩條同時成立才重跑完整 DD","side_b":"股價≤230美元（約FY2027共識EPS 20.3倍）即重跑完整DD；或2027-02 FY2027 pro forma EPS指引≥12.0美元時以新分母重算","ruling":"價格腿已到（276.75 約 FY2027 共識 24.4 倍），但毛利率 ≥59.0% 在管理層預告 2027 回到歷史區間（57.5%–58.7%）後幾乎注定不成立，且決定 EPS 的是營業利益率不是毛利率；改成單一價格條件（對應基本情境 10% 年報酬），另開 EPS 指引的替代路徑，重跑通過後首倉 2%","evidence_level":"法說指引＋情境樹","settle_metric":"股價；FY2027 EPS 指引","if_then":["若兩條都未觸發，2027-02 指引公布後仍重跑一次完整 DD"],"evidence_refs":["geo_supply_chain#2"]},{"axis":"Single Thing 新設","cause":"新證據","prior_field":["single_thing"],"side_a":"前份未設唯一致命點（null）","side_b":"FY2027 實際 pro forma EPS 低於 FY2026 的約 10.80 美元（EPS 年減）；2027-02 指引若已低於此數先行預警","ruling":"設立理由：2026-10-28 管理層首次明說 2027 毛利率回到歷史區間，FY2027 利潤率成為五年路徑裡最大的單一敏感項（營業利益率每 100bp 約 0.4 美元 EPS）","evidence_level":"法說指引","settle_metric":"FY2027 pro forma EPS","if_then":["若發生，Bear 機率升到 40%、暫停進場；若已持有則減碼一半"],"evidence_refs":["supply_demand_durability#2"]},{"axis":"減碼／清倉指標新設","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設 kill_metrics（null）","side_b":"FY2027 營業利益率 <26%；Fitness＋Outdoor 合計年增連 2 季 <5%；Omdia 份額 <12%；FY2027 FCF÷淨利 <0.75","ruling":"前份只有進場條件、沒有持有後的出場指標，本次補上；若已持有，第一條觸發減碼一半，第一條加第二條同時觸發清倉","evidence_level":"方法補齊","settle_metric":"四項指標各自的資料來源","if_then":["若任兩項同時觸發，清倉並重跑完整 DD"],"evidence_refs":[]},{"axis":"記憶體風險門檻由毛利率年比轉負改為年減超過 300bp","cause":"新證據","prior_field":null,"side_a":"前份 R1：記憶體成本全年攤入＋無關稅退款→毛利率年比轉負","side_b":"本次 R1：季度毛利率年減 >300bp（扣除關稅退款）連 2 季，或 FY2027 毛利率指引 <57.5%","ruling":"管理層已預告 2027 毛利率回到歷史區間，年比轉負已是基本情境的一部分，不再是風險訊號；門檻移到基本情境之外（58.5% 再低 1pp）。觸發時 Bear 機率升到 35%、價格門檻下修到 210 美元；若已持有則減碼三分之一","evidence_level":"法說指引","settle_metric":"季度毛利率；FY2027 毛利率指引","if_then":["若 FY2027 毛利率指引 <57.5%，價格門檻改為 210 美元"],"evidence_refs":["supply_demand_durability#2","geo_supply_chain#1"]},{"axis":"最大回撤由單點改範圍","cause":"方法變動","prior_field":["max_dd_pct"],"side_a":"前份最大回撤 −55%（單點）","side_b":"本次 −55%～−35%：下緣用 Bear 第二年 EPS 9.70×13.5 倍≈131 美元，上緣用 EPS 不跌但倍數回到約 17 倍≈180 美元","ruling":"下緣不變，改成範圍並寫明推導；事實表未涵蓋歷史最大回撤","evidence_level":"情境樹推估","settle_metric":"實際回撤","if_then":["若股價跌破 180 美元而基本面指標都未觸發，屬深回撤心理準備範圍，重跑 DD 評估分批買進"],"evidence_refs":[]},{"axis":"其餘基本面結論複核後維持","cause":"新證據","prior_field":["signal","runway_post_y5","archetype","cycle_position"],"side_a":"前份：綜合訊號 B、成長跑道中等、品質複利成長、不判循環位置","side_b":"本次維持：品質（淨現金、營業利益率 29%）與動能（RSI 45、未過熱）未改變綜合訊號；份額上升但滲透率仍無資料，跑道維持中等；營收四年年複合約 14% 且淨現金，仍屬品質複利成長；記憶體成本循環影響毛利但不改變公司類型","ruling":"維持；若 FY2027 EPS 年減，要重新檢查是否該按循環股處理","evidence_level":"事實表＋法說","settle_metric":"FY2027 EPS 與營收成長","if_then":["若 FY2027 EPS 年減且營收成長低於 5%，公司類型改按循環股重審"],"evidence_refs":[]},{"axis":"前份 Outdoor 結構性衰退風險退休","cause":"新證據","prior_field":null,"side_a":"前份：Outdoor（最高毛利段）結構性衰退擴散，2026Q1 −5%、Q2 −2%，近四季三負，下半年改善承諾與上半年算術難相容","side_b":"2026-10-28：Outdoor +20% 至 5.97 億美元，fēnix 9 帶動，毛利率 68%、營業利益率 39%；2026-07-29 承諾的下半年轉強已兌現","ruling":"退休：前份把產品週期低谷看成結構衰退。換機潮退去的風險保留：fēnix 首波需求以舊用戶跨代換機為主，改由 Fitness＋Outdoor 合計成長門檻（H1）追蹤","evidence_level":"公司分部數據","settle_metric":"Fitness＋Outdoor 合計營收年增率","if_then":["若 2027 下半年 Outdoor 年增連 2 季為負，重新開立 Outdoor 結構性風險"],"evidence_refs":["end_markets#0"]}],"triggers":[{"n":1,"text":"股價跌到 230 美元以下（約 FY2027 共識 EPS 20.3 倍），對應基本情境約 10% 年報酬","type":"估值rearm","maps_to":"H2","metric":"收盤價","threshold":"≤230 美元","action":"重跑完整 DD，通過後首倉 2%","source_freq":"每日收盤","date":null,"evidence_refs":[]},{"n":2,"text":"FY2027 實際 pro forma EPS 低於 FY2026（約 10.80 美元）；2027-02 指引若已低於此數先行預警","type":"Single Thing","maps_to":"H2","metric":"FY2027 pro forma EPS（指引與實際）","threshold":"<10.80 美元","action":"Bear 機率升到 40%，暫停進場；已持有則減碼一半","source_freq":"2 月年度指引、季度財報","date":"2027-02","evidence_refs":["supply_demand_durability#2"]},{"n":3,"text":"高階穿戴份額與成長的假設檢驗","type":"假設驗證","maps_to":"H1","metric":"Fitness＋Outdoor 合計 TTM 營收相對 10% 年增路徑的偏離","threshold":"低於路徑 5% 以上連 2 季＝削弱；10% 以上連 3 季＝反轉","action":"削弱：護城河方向改回穩定；反轉：Bear 機率升到 40%","source_freq":"季度 8-K","date":null,"evidence_refs":[]},{"n":4,"text":"記憶體與零組件成本吃進毛利率","type":"風險","maps_to":"R1","metric":"季度合併毛利率年變化（扣除關稅退款）","threshold":"年減 >300bp 連 2 季，或 FY2027 毛利率指引 <57.5%","action":"Bear 機率升到 35%，價格門檻下修到 210 美元","source_freq":"季度 8-K","date":null,"evidence_refs":["supply_demand_durability#2","geo_supply_chain#1","geo_supply_chain#2"]},{"n":5,"text":"穿戴份額回落","type":"風險","maps_to":"R2","metric":"Omdia 智慧手錶出貨份額","threshold":"<12%（2Q26 為 15%）","action":"護城河方向改回穩定，Bear 機率升到 35%","source_freq":"Omdia 季度新聞稿","date":null,"evidence_refs":["competitive_share_entrants#0","substitute_technology#0","customer_second_source#0"]},{"n":6,"text":"成長的資本需求未回落","type":"假設驗證","maps_to":"H3","metric":"FCF÷淨利","threshold":"FY2027 <0.75","action":"衰退信號亮第二項，維持價值陷阱風險中並把 Bear 機率升到 35%","source_freq":"年報","date":"2028-02","evidence_refs":[]},{"n":7,"text":"關稅或台灣集中造成的毛利侵蝕（吸收失敗的判準）","type":"風險","maps_to":"R3","metric":"任一分部毛利率中歸因於關稅的年減幅；泰國廠投產時點","threshold":"≥200bp 連 2 季；或投產延後到 2027Q2 以後","action":"Bear 機率升到 35%","source_freq":"季度 10-Q／法說","date":null,"evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","geo_supply_chain#0"]},{"n":8,"text":"波蘭競爭機關對 Garmin Polska 與經銷商價格協議的調查結果","type":"風險","maps_to":"R5","metric":"UOKiK 裁罰或命令","threshold":"公告裁罰（受影響營收事實表未涵蓋）","action":"金額低於全年營業利益 1% 只記錄；若擴及其他歐盟國家的經銷協議，重跑完整 DD","source_freq":"UOKiK 公告；10-K 法律程序","date":null,"evidence_refs":["regulatory_antitrust#2"]},{"n":9,"text":"存貨與通路促銷壓力","type":"風險","maps_to":"R4","metric":"存貨÷當季營收","threshold":">1.3 連 2 季（Q3 2026 為 1.13）","action":"Bear 機率升到 35%","source_freq":"季度 10-Q","date":null,"evidence_refs":["customer_concentration_credit#1"]},{"n":10,"text":"Q4 2026 財報與 FY2027 全年指引","type":"複審日期","maps_to":"H2","metric":"FY2027 營收、毛利率、營業利益率、EPS 指引","threshold":"營業利益率 ≥27% 且 EPS ≥12.0 美元＝替代進場路徑；EPS <10.80 美元＝唯一致命點預警","action":"重跑完整 DD","source_freq":"年度","date":"2027-02","evidence_refs":[]}],"kill_metrics":[{"metric":"FY2027 營業利益率（2027-02 指引與全年實際）","bear_threshold":"<26%（FY2025 為 25.9%）","window":"2027-02 指引；FY2027 全年","source":"Garmin 8-K 新聞稿與法說","last_status":"unknown"},{"metric":"Fitness＋Outdoor 合計營收年增率","bear_threshold":"連 2 季 <5%","window":"季度，2027Q1 起","source":"Garmin 8-K 分部營收","last_status":"ok"},{"metric":"Omdia 智慧手錶出貨份額","bear_threshold":"<12%（2Q26 為 15%）","window":"季度","source":"Omdia 季度新聞稿","last_status":"ok"},{"metric":"FCF÷淨利","bear_threshold":"FY2027 <0.75（連第二年）","window":"FY2027 年報","source":"Garmin 10-K 現金流量表","last_status":"warning"}],"evidence_dismissed":[],"action_conditions":{"rearm_trigger":"股價≤230美元（約FY2027共識EPS 20.3倍）即重跑完整DD；或2027-02 FY2027 pro forma EPS指引≥12.0美元時以新分母重算","exec_line":"現價不追。股價≤230 美元且 FY2027 指引未讓 EPS 年減 → 重跑完整 DD，通過後首倉 2%，2027Q1 實際營業利益率 ≥26% 再補到 4%；FY2027 EPS 指引 <10.80 美元則暫停所有進場"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"現價隱含 2026 的高峰利潤率延續且倍數不降；管理層已預告 2027 毛利率回到歷史區間，正常化後 EPS 年增約 8.5%，配 22 倍終端倍數只有約 6% 年報酬","momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"股價 ≤230 美元，或 2027-02 FY2027 pro forma EPS 指引 ≥12.0 美元","asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null},"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8(val爭議)","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='↑', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=現價隱含 2026 的高峰利潤率延續且倍數不降；管理層已預告 2027 毛利率回到歷史區間，正常化後 EPS 年增約 8.5%，配 22 倍終端倍數只有約 6% 年報酬"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟠', moat_trend='↑', week26=16.95, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position=None, moat='B', moat_trend='↑', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈機械讀數判定不可用，baseline rows 8/9/9b/10 的估值條件視為不可判 → 落 row8 觀望（保守方向）","hit":true,"basis":"val_denominator_disputed=True, val(機械讀數)='🟠'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":null,"requires_critic":[]},"thesis":{"H":[{"id":"H1","text":"高階穿戴（Fitness＋Outdoor）在整體穿戴出貨下滑的市場裡繼續拿份額，成長以新用戶與新品類（CIRQA）為主、不靠併購","2y":"FY2026–FY2027 Fitness＋Outdoor 合計營收每年年增 ≥10%，Omdia 份額 ≥13%","5y":null,"10y":null,"threshold":"Fitness＋Outdoor 合計營收年增 ≥10%；Omdia 智慧手錶份額 ≥13%（2Q26 為 15%）","source":"Garmin 季度 8-K 分部營收；Omdia 季度出貨新聞稿","drift_rule":"兩年期：TTM 合計營收低於 10% 年增路徑 5% 以上連 2 季＝削弱；低 10% 以上連 3 季＝反轉"},{"id":"H2","text":"毛利率回到歷史區間時，靠費用槓桿、規模與垂直整合把營業利益率守在 26% 以上，FY2027 EPS 不倒退","2y":"FY2027 營業利益率 ≥26%、pro forma EPS ≥10.80 美元","5y":null,"10y":null,"threshold":"FY2027 營業利益率 ≥26%（FY2025 為 25.9%，FY2026 指引 29%）","source":"2027-02 全年指引；季度 8-K 損益","drift_rule":"兩年期：TTM 營業利益率低於 26% 達 1.3pp（偏離 5%）以上連 2 季＝削弱；低 2.6pp（偏離 10%）以上連 3 季＝反轉"},{"id":"H3","text":"成長的資本需求可控：泰國廠與記憶體存貨是一次性墊高，FY2027 起 FCF÷淨利回到 0.75 以上，FY2026–FY2031 營收年複合 ≥8% 且以有機為主","2y":null,"5y":"FY2031 營收約 120 億美元以上（FY2026 指引 81.5 億×1.08⁵），FCF÷淨利 ≥0.75","10y":null,"threshold":"FCF÷淨利 ≥0.75（2025 年 0.82、2026E 約 0.53）；營收五年年複合 ≥8%","source":"10-K 現金流量表與損益表；季度 10-Q 存貨","drift_rule":"五年期：TTM 偏離門檻 5% 以上連 4 季＝削弱；10% 以上連 6 季＝反轉"}],"R":[{"id":"R1","text":"記憶體與其他零組件漲價（AI 需求排擠）在 2026Q4–2027 吃進毛利率，部分供應商是單一來源，安全庫存用完後全面反映市價","h_ref":"H2","clock":"⚡","threshold":"季度毛利率年減 >300bp（扣除關稅退款）連 2 季，或 FY2027 毛利率指引 <57.5%","evidence_refs":["supply_demand_durability#2","geo_supply_chain#1","geo_supply_chain#2"]},{"id":"R2","text":"Apple／Samsung／Huawei 用手機生態補齊運動健康功能，Whoop／Oura 等專業品牌複製功能，加上 OEM 客戶自製，侵蝕高階穿戴份額與單價","h_ref":"H1","clock":"🔥","threshold":"Fitness 營收年增連 4 季 <5% 且 Omdia 份額 <12%","evidence_refs":["competitive_share_entrants#0","substitute_technology#0","customer_second_source#0"]},{"id":"R3","text":"消費產品主要在台灣製造，暴露於關稅與兩岸風險；泰國廠 2027Q1 才投產，2026Q1 Marine 毛利率就曾因關稅年減 200bp","h_ref":"H3","clock":"🐢","threshold":"任一分部毛利率因關稅年減 ≥200bp 連 2 季，或泰國廠投產延後到 2027Q2 以後","evidence_refs":["geo_supply_chain#0","reg_tariff_export#0","reg_tariff_export#1"]},{"id":"R4","text":"大型零售客戶要求促銷壓毛利，加上主動墊高存貨（Q3 22.5 億美元），若需求轉弱會變成去化折價","h_ref":"H3","clock":"🔥","threshold":"存貨÷當季營收 >1.3 連 2 季（Q3 2026 為 1.13），或 Fitness／Outdoor 毛利率年減 ≥200bp","evidence_refs":["customer_concentration_credit#1"]},{"id":"R5","text":"監管與技術依賴類尾端風險：波蘭競爭機關 2024 年對 Garmin Polska 與經銷商價格協議的調查未見結果；GNSS 干擾與欺騙可能損害定位功能","h_ref":"H1","clock":"🐢","threshold":"UOKiK 公告裁罰（受影響營收事實表未涵蓋），或 GNSS 干擾導致產品功能停用／召回","evidence_refs":["regulatory_antitrust#2","substitute_technology#1"]}],"single_thing":{"description":"FY2027 實際 pro forma EPS 低於 FY2026 的約 10.80 美元（EPS 年減）；2027-02 公布的全年指引是第一個讀數","why_fatal":"營業利益率每 100bp 約等於 EPS 0.4 美元（約 4%），是五年路徑裡最大的單一敏感項；EPS 年減代表記憶體成本與 Mercedes 低毛利組合吃掉整年營收成長，基本情境 FY2027 的 11.30 不成立，倍數也會往 20 倍以下靠","if_happens":"Bear 機率由 30% 升到 40%，230 美元的價格門檻失效，改等 2027Q1 實際毛利率；若已持有則減碼一半","how_monitor":"2027-02 Q4 法說的 FY2027 指引；在那之前看 Q4 2026 實際毛利率與營業利益率","probability":"約 25%（12–24 個月）：以 FY2026 指引的稅率與非營業收入不變推算，營收照共識成長 12% 時，營業利益率要低於約 25.9% 才會年減；FY2025 在毛利率 58.7% 時營業利益率已有 25.9%，要毛利率跌破歷史區間或營收明顯放慢才會發生"}},"appendix_a":{"growth_durability":6,"quality_score":9,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":24.38,"peg_fy2":1.74,"stress":{"pass":3,"total":5}},"eps_meta":{"base_eps_path":{"FY2025A":8.59,"FY2026E":10.49,"FY2027E":11.35,"FY2028E":12.74},"fy_end_month":12,"eps_basis":"FY2026E–FY2028E 為 Koyfin 共識（2026-10-31 快照，EPS 家數事實表未涵蓋）；FY2025A 用年報稀釋 EPS 8.59（GAAP）。公司 pro forma 口徑 FY2026 指引 10.80、較上年 +26%，回推上年約 8.57，與 GAAP 差異很小"},"catalysts":[{"date":"2027-02","date_precision":"month","type":"guidance","event":"Q4 2026 財報與 FY2027 全年指引","impact":"高","watch":"營業利益率指引是否 ≥27%、pro forma EPS 指引是否 ≥10.80 美元"},{"date":"2027-03","date_precision":"quarter","type":"capacity","event":"泰國新廠開始量產（管理層稱 2027Q1）","impact":"中","watch":"是否如期投產、投產初期對毛利率的拖累"},{"date":"2027-06","date_precision":"quarter","type":"product","event":"Mercedes-Benz 新一代 domain controller 量產（管理層稱 2027 年偏上半年）","impact":"中","watch":"車用 OEM 營收回到成長，以及低毛利組合對合併毛利率的稀釋"},{"date":"2026-12","date_precision":"quarter","type":"other","event":"Omdia／Counterpoint 3Q26 智慧手錶出貨統計","impact":"低","watch":"Garmin 份額是否守住 2Q26 的 15%（Omdia）"}]}
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
