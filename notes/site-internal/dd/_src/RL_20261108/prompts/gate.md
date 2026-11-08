你是 DD 管線 v20 的判斷層閘（gate），標的 RL（20261108）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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
- `f_kpi0_net_revenue_gaap`（q1_business）｜Net revenue (GAAP)＝2193.3 USD m｜期間與口徑：Q2 FY2027（季末 2026-09-26，公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q2 FY27 新聞稿（8-K Ex.99.1，2026-11-05）https://www.sec.gov/Archives/edgar/data/0001037038/000162828026070619/rl-20260926ex991xpressrele.htm（numbers.latest_quarter_kpis.items[0]，as_of Q2 FY2027（季末 2026-09-26，公告於 2026-11-05））
- `f_kpi1_adjusted_operating_incom`（q1_business）｜Adjusted operating income / margin＝15.7 %｜期間與口徑：Q2 FY2027（季末 2026-09-26，公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q2 FY27 新聞稿（8-K Ex.99.1，2026-11-05）https://www.sec.gov/Archives/edgar/data/0001037038/000162828026070619/rl-20260926ex991xpressrele.htm（numbers.latest_quarter_kpis.items[1]，as_of Q2 FY2027（季末 2026-09-26，公告於 2026-11-05））
- `f_kpi2_gaap_operating_income_ma`（q1_business）｜GAAP operating income / margin＝16.6 %｜期間與口徑：Q2 FY2027（季末 2026-09-26，公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q2 FY27 新聞稿（8-K Ex.99.1，2026-11-05）https://www.sec.gov/Archives/edgar/data/0001037038/000162828026070619/rl-20260926ex991xpressrele.htm（numbers.latest_quarter_kpis.items[2]，as_of Q2 FY2027（季末 2026-09-26，公告於 2026-11-05））
- `f_kpi9_adjusted_gross_margin`（q1_business）｜Adjusted gross margin＝70.5 %｜期間與口徑：Q2 FY2027（季末 2026-09-26，公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q2 FY27 新聞稿（8-K Ex.99.1，2026-11-05）https://www.sec.gov/Archives/edgar/data/0001037038/000162828026070619/rl-20260926ex991xpressrele.htm（numbers.latest_quarter_kpis.items[9]，as_of Q2 FY2027（季末 2026-09-26，公告於 2026-11-05））
- `f_kpi5_guidance_q3_fy2027`（q1_business）｜Guidance Q3 FY2027＝固定匯率營收 +3% 至 +4% text｜期間與口徑：Q2 FY2027（季末 2026-09-26，公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司 Q2 FY27 新聞稿（8-K Ex.99.1，2026-11-05）https://www.sec.gov/Archives/edgar/data/0001037038/000162828026070619/rl-20260926ex991xpressrele.htm（numbers.latest_quarter_kpis.items[5]，as_of Q2 FY2027（季末 2026-09-26，公告於 2026-11-05））
- `f_kpi6_guidance_full_year_fy202`（q1_business）｜Guidance full-year FY2027 (53 週)＝固定匯率營收 +6% 至 +7%（上調自 +5% 至 +6%） text｜期間與口徑：Q2 FY2027（季末 2026-09-26，公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司 Q2 FY27 新聞稿（8-K Ex.99.1，2026-11-05）https://www.sec.gov/Archives/edgar/data/0001037038/000162828026070619/rl-20260926ex991xpressrele.htm（numbers.latest_quarter_kpis.items[6]，as_of Q2 FY2027（季末 2026-09-26，公告於 2026-11-05））
- `f_peer_rl_gross_margin_pct`（q2_moat）｜RL 毛利率＝71.0 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.RL.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_rl_operating_margin_pct`（q2_moat）｜RL 營業利益率＝17.16 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.RL.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_tpr_gross_margin_pct`（q2_moat）｜TPR 毛利率＝78.31 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.TPR.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_tpr_operating_margin_pct`（q2_moat）｜TPR 營業利益率＝24.53 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.TPR.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_pvh_operating_margin_pct`（q2_moat）｜PVH 營業利益率＝8.05 %｜期間與口徑：TTM ending 2026-07-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.PVH.operating_margin_pct，as_of TTM ending 2026-07-31（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_levi_operating_margin_pct`（q2_moat）｜LEVI 營業利益率＝11.75 %｜期間與口徑：TTM ending 2026-08-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.LEVI.operating_margin_pct，as_of TTM ending 2026-08-31（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_cpri_gross_margin_pct`（q2_moat）｜CPRI 毛利率＝63.28 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CPRI.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_cpri_operating_margin_pct`（q2_moat）｜CPRI 營業利益率＝2.74 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CPRI.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝18.94 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-11-07）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝20.9 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-11-07）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝22.84 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-11-07）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝8726.85 USD m｜期間與口徑：2026-11-08／yfinance revenue_estimate 0y 平均（16 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝9179.85 USD m｜期間與口徑：2026-11-08／yfinance revenue_estimate +1y 平均（16 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi4_sbc_six_months`（q4_capital）｜SBC (six months)＝64.3 USD m｜期間與口徑：Six months FY2027（截至 2026-09-26，公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q2 FY27 新聞稿（8-K Ex.99.1，2026-11-05）https://www.sec.gov/Archives/edgar/data/0001037038/000162828026070619/rl-20260926ex991xpressrele.htm（numbers.latest_quarter_kpis.items[4]，as_of Six months FY2027（截至 2026-09-26，公告於 2026-11-05））
- `f_kpi3_free_cash_flow_derived_s`（q1_business）｜Free cash flow (derived, six months)＝504.0 USD m｜期間與口徑：Six months FY2027（截至 2026-09-26，公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q2 FY27 新聞稿（8-K Ex.99.1，2026-11-05）https://www.sec.gov/Archives/edgar/data/0001037038/000162828026070619/rl-20260926ex991xpressrele.htm（numbers.latest_quarter_kpis.items[3]，as_of Six months FY2027（截至 2026-09-26，公告於 2026-11-05））
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝1.016 %｜期間與口徑：2026-11-08／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-11-08）
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝59.1 m shares｜期間與口徑：2026-11-08／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝1181.0 USD m｜期間與口徑：2026-11-08／yfinance 最新一季：總債務 3002.8、現金 1821.8（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝376.56 USD｜期間與口徑：2026-11-06（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-11-06（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝19.88 x｜期間與口徑：2026-11-07／分母＝FY1 EPS 18.94，分子＝快照價 376.56｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-11-07）
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝21.62 x｜期間與口徑：2026-11-06（RTH 收盤，UTC）／4 個年度端點內的分位＝85.5｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-11-06（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝85.5 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝96.5 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝97.6 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_consensus_rev_fy1_pct`（q5_valuation）｜FY1 共識修正＝0.0 %｜期間與口徑：2026-11-07／兩份 Koyfin 快照之間的 EPS 修正幅度（18.94 → 18.94）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.fy1.revision_pct，as_of 2026-11-07）
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝0.21 %｜期間與口徑：2026-08-13 → 2026-11-07／FY1 共識 EPS 18.9 → 18.94（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-11-07）
- `f_rsi14`（q5_valuation）｜RSI(14)＝47.64｜期間與口徑：2026-11-06（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-11-06（RTH 收盤，UTC））
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝5.61 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ma_state`（q5_valuation）｜週線均線六態（decision_inputs.ma 必須等於此值）＝🟡｜期間與口徑：2026-11-08／timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）
  - 原文：「price 376.56 / W52 364.61 / W104 312.69 / W250 202.87 / W250 13週斜率 2.24%」
- `f_ma_w250`（q5_valuation）｜250 週均線＝202.87 USD｜期間與口徑：2026-11-08／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）
- `f_ma_w104`（q5_valuation）｜104 週均線＝312.69 USD｜期間與口徑：2026-11-08／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）
- `f_ma_w52`（q5_valuation）｜52 週均線＝364.61 USD｜期間與口徑：2026-11-08／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）
- `f_kpi8_inventory`（q1_business）｜Inventory＝1151.2 USD m｜期間與口徑：Q2 FY2027（季末 2026-09-26，公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q2 FY27 新聞稿（8-K Ex.99.1，2026-11-05）https://www.sec.gov/Archives/edgar/data/0001037038/000162828026070619/rl-20260926ex991xpressrele.htm（numbers.latest_quarter_kpis.items[8]，as_of Q2 FY2027（季末 2026-09-26，公告於 2026-11-05））

### findings_digest 中方向為負或來源衝突的條目（5 條）
- `competitive_share_entrants#0`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K 風險因子：零售業進入門檻低，新競爭者與產品快速進場，加上數位通路轉移；競爭加劇或應對失敗可能導致市占或銷售下滑（為風險揭露，未指名具體新進入者）。
  - 來源：SEC EDGAR 10-K FY2026 Item 1A（as_of 2026-05-21）｜affects：moat_trend、thesis.R
- `supply_demand_durability#2`（supply_demand_durability｜方向 -｜狀態 ok）：USFIA 2026 調查：85%受訪者稱關稅損害財務表現（2025為78%）；僅約10%增加美國製造採購；越南、孟加拉、印尼、印度、柬埔寨占美國服飾進口50.6%（疫情前37.1%）；美國紡織稼動率低於75%。
  - 來源：Textalks: US apparel tariffs raise costs but deliver little reshoring, USFIA survey finds（as_of 2026-10-01）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：約96%產品在美國境外生產，越南約21%、柬埔寨16%、印度11%；關稅或貿易限制重大變動可能使產品成本顯著上升，且不保證能以提價或供應鏈調整抵銷。
  - 來源：SEC EDGAR 10-K FY2026 Item 1A（as_of 2026-05-21）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#4`（reg_tariff_export｜方向 -｜狀態 ok）：FY27指引假設上半年關稅率較低、下半年在現行減免期結束後關稅逆風較上半年增加（假設稅率升至10%以上），且指引未計入任何關稅退款。
  - 來源：just-style，Ralph Lauren Q1 FY27（搜尋摘要）（as_of 2026-08-01）｜affects：valuation、triggers
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：10-K 風險因子指出技術進步與零售業低進入門檻使新競爭者與新產品快速出現
  - 來源：SEC EDGAR 10-K FY2026（as_of 2026-05-21）｜affects：moat_trend

### 事實表自陳的缺口（2 條）
- q2_moat：evidence.numbers.peer_financials 該欄整欄為 null（常見於未單獨揭露研發的業者），事實表 agent 若能從財報補就補，補不到即為缺口，判斷者不得自行估。
- q6_how_wrong：digest.qa_flags 有 3 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/RL_20261108/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":751.8,"bear_5y_price":252.2,"p_bull_pct":25,"p_bear_pct":30,"upside_5y_pct":41.5,"ev5y_pct":33.7,"irr_base_pct":7.2,"asym_ratio":2.5,"scenario_tree":{"terminal_label":"FY2032E","start":{"eps":18.94,"pe":19.88,"basis":"FY1（FY2027E，2027 年 3 月底結束）調整後共識 EPS；五年後同樣以當時進行中的年度 FY2032E 當分母，口徑一致。"},"eps":{"bull":[22.2,25.0,28.2,31.8,35.8],"base":[21.1,23.1,25.2,27.4,29.6],"bear":[18.6,17.8,18.1,18.7,19.4]},"pe":{"bull":21,"base":18,"bear":13},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":1.016,"net_buyback":0},"second_stage":{"bull_cagr_pct":10,"base_cagr_pct":7},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### RL_Q1_2027_Earnings_Call_20260806.md
- 2026-08-06｜CFO｜guidance：FY27 固定匯率營收成長上調至 5%–6%，原 4%–5%（原話："now centered around 5% to 6%, up from 4% to 5%"）
- 2026-08-06｜CFO｜guidance：FY27 營業利益率擴張上調至 60–80bp，原 40–60bp（原話："up from our prior guidance of 40 to 60 basis points"）
- 2026-08-06｜CFO｜guidance：FY27 毛利率擴張上調至 50–70bp，原為小幅擴張（原話："gross margin outlook to roughly 50 to 70 basis points"）
- 2026-08-06｜CFO｜guidance：Q2 營業利益率預期擴張 80–100bp（原話："operating margin to expand approximately 80 to 100"）
- 2026-08-06｜CFO｜guidance：Q2 固定匯率營收預期中個位數成長（原話："currency revenue to increase approximately mid-single"）
- 2026-08-06｜CFO｜guidance：Q2 稅率 19%–20%（原話："second quarter tax rate to be in the range of 19% to 20%"）
- 2026-08-06｜CFO｜guidance：FY27 亞洲營收預期上調至高個位數到低雙位數（原話："high single to low double digits"）
- 2026-08-06｜CFO｜guidance：FY27 北美營收維持低個位數成長（原話："America revenue to grow approximately low single digits"）
- 2026-08-06｜CFO｜guidance：FY27 歐洲營收維持低到中個位數成長（原話："Europe revenue to increase approximately low to mid-single"）
- 2026-08-06｜CFO｜guidance：FY27 AUR 預期中到高個位數成長（原話："mid- to high single-digit AUR growth for the full year"）
- 2026-08-06｜CEO｜guidance：FY27 中國預期約中十位數成長，管理層表示不能期待每季 40%（原話："I don't know that we can count on 40% every quarter"）
- 2026-08-06｜CFO｜guidance：毛利與營業利益率擴張預期集中於上半年（原話："expansion to be weighted toward the first half of the fiscal"）
- 2026-08-06｜CFO｜guidance：Q2 北美預期中個位數成長（原話："balanced mid-single-digit growth quarter"）
- 2026-08-06｜CFO｜guidance：Q2 亞洲預期領先成長中十位數（原話："Asia is going to lead growing mid-teens"）
- 2026-08-06｜CFO｜margin：Q1 調整後毛利率擴張 130bp 至 73.6%（原話："adjusted gross margin expanded 130 basis points to 73.6%"）
- 2026-08-06｜CFO｜margin：Q1 調整後營業利益率擴張 150bp 至 18.5%（原話："adjusted operating margin expanded 150 basis points to 18.5%"）
- 2026-08-06｜CFO｜margin：Q1 行銷費用占營收 8.2%，去年 7.5%（原話："Marketing increased to 8.2% of sales compared to 7.5%"）
- 2026-08-06｜CFO｜margin：管理層稱毛利率擴張由結構性、可持續因素支撐（原話："underpinned by structural durable drivers"）
- 2026-08-06｜CFO｜margin：關稅假設：上半年約 10%，下半年回到高十位數互惠稅率（原話："reciprocal rates in the high teens during the second half"）
- 2026-08-06｜CFO｜margin：關稅假設上半年維持約 10%（原話："approximately 10% tariff rates through the first half"）
- 2026-08-06｜CFO｜commitment：管理層重申 FY27 行銷占營收約 8%（原話："step up to approximately 8% in fiscal '27"）
- 2026-08-06｜CEO｜commitment：CEO 對 8% 行銷投入表示維持（原話："remain comfortable with the 8% marketing investment"）
- 2026-08-06｜CFO｜commitment：CFO 對三年期 7.5%–8.5% 行銷指引表示維持（原話："feel good about the 7.5% to 8.5%, 3-year guide"）
- 2026-08-06｜CFO｜commitment：行銷比例不設上限（原話："But as Patrice always talked about, it's not a ceiling."）
- 2026-08-06｜CEO｜commitment：三年期歐洲中個位數成長目標不變（原話："deliver mid-single digit for the full 3-year period"）
- 2026-08-06｜CEO｜commitment：預期 DTC 占比未來略高於 70%（原話："probably a little more than 70% DTC moving forward"）
- 2026-08-06｜CFO｜capital_allocation：Q1 透過股息與買回向股東返還逾 3 億美元（原話："we returned more than $300 million to shareholders through"）
- 2026-08-06｜CFO｜capital_allocation：關稅退款不納入調整後非 GAAP，若有相關款項計畫再投資（原話："we expect to reinvest any related"）
- 2026-08-06｜CFO｜risk：指引排除關稅退款影響（原話："guidance continues to exclude the impact of tariff refunds"）
- 2026-08-06｜CFO｜risk：歐洲風險：中東夥伴銷售與旅遊中斷（原話："disruption to Middle East partner sales and tourism"）
- 2026-08-06｜CFO｜risk：歐洲客流整體承壓，以轉換率與客單價抵銷（原話："traffic, as you know, has been broadly pressured across"）
- 2026-08-06｜CFO｜risk：北美批發 Q1 受出貨時點與恢復出貨墊高約 15 點（原話："contributed approximately 15 points of growth in"）
- 2026-08-06｜CFO｜risk：歐洲批發 Q1 含約 5 點出貨提前效應（原話："a roughly 5-point benefit from earlier timing of shipments"）
- 2026-08-06｜CEO｜customer：Q1 新增 150 萬 DTC 新客（原話："we added 1.5 million new customers to our DTC businesses"）
- 2026-08-06｜CFO｜customer：北美批發下半年加速縮減 off-price 與低階門市（原話："exit of lower-tier full-price stores in the back half"）
- 2026-08-06｜CEO｜customer：批發重整大致完成（原話："most of the reset is complete"）
- 2026-08-06｜CEO｜product：核心產品占營收逾 70%，Q1 成長中十位數（原話："Core product sales grew mid-teens in the first quarter."）
- 2026-08-06｜CEO｜product：高潛力品類（女裝、外套、手袋）Q1 成長逾 20%（原話："increased more than 20% for the quarter,"）
- 2026-08-06｜CFO｜product：管理層稱 AUR 是策略的結果而非目標（原話："AUR is an outcome of our strategy."）
- 2026-08-06｜CFO｜product：管理層稱定價架構保留彈性（原話："built flexibility into our pricing architecture"）
- 2026-08-06｜CEO｜competition：管理層稱更健康的奢侈品市場對公司是順風（原話："a healthier luxury market would be a tailwind for us"）
- 2026-08-06｜CEO｜competition：管理層稱自身定位為 inclusive luxury（原話："what we call inclusive luxury, spanning categories"）
- 2026-08-06｜CEO｜competition：管理層稱許多奢侈品競爭者中國滲透率更高（原話："many of our luxury competitors have much greater China"）

### 問答異常語氣（迴避／改口／保留）
- RL_Q1_2027_Earnings_Call_20260806.md｜問：Jay Sole 問近期／季至今趨勢｜答法：CFO 表示通常不評論季至今趨勢，改以 Q2 指引的區域成長拆解回應
- RL_Q1_2027_Earnings_Call_20260806.md｜問：Brooke Roach 問歐洲夏季各月趨勢如何演變｜答法：CEO 表示不評論當季，轉而談品牌資產指標與先前說法，未給夏季趨勢
- RL_Q1_2027_Earnings_Call_20260806.md｜問：Michael Binetti 問行銷是否朝 FY28 指引中高端或高端｜答法：未回答具體目標點，重申 7.5%–8.5% 指引與「非上限」

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 2 | 1 |
| customer_second_source | not_applicable | 0 | 0 |
| customer_concentration_credit | found | 2 | 1 |
| supply_demand_durability | found | 4 | 4 |
| regulatory_antitrust | found | 2 | 3 |
| reg_tariff_export | found | 5 | 2 |
| geo_supply_chain | found | 1 | 2 |
| end_markets | found | 4 | 3 |
| substitute_technology | found | 1 | 2 |
| channel_business_model_shift | found | 2 | 2 |
| capital_markets_pricing | found | 3 | 3 |
| major_events | found | 3 | 4 |

未涵蓋／不適用軸的查詢詞原文（供判相關性）：
- **customer_second_source**（not_applicable）：（無查詢記錄）

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260522","verdict":"B（衛星候選，Post-Q4 FY26 結構性 thesis 強化但時機過熱）：Q4 大 beat（Rev +17%、Asia +28%、China +50%+、AUR 持續高雙、$2.0B Q rev/$8.1B FY），股價 5/21 +13.9% gap up 至 $374.90（漂移 +15%/2 日，QC-22 觸發）。長期 thesis 強化（China +Asia 雙引擎、$700M+ 資本回饋、ROIC 25%），但 Fwd PE FY28 20.8x（5Y 56%ile）+ PEG 1.43 + 接近 BB 上軌 $394.65（95.5%ile），短期 R:R 0.15x 失效。建議等回測 BB 中軌 $356 或 W52 $328 分批，FY27 guidance +4-5% CC 偏保守暗示成長放緩，需觀察 H2 FY27 關稅執行成效。","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"Asia / China 結構成長持續：Polo 在中國中產階級渗透率仍處 S 曲線中段","columns":{"2Y 驗證點":"Asia revenue +20% 以上連續 4 季；China +35%+ 連續 4 季","5Y 驗證點":"Asia 占整體營收從 21% → 30%；OM 從 31.8% 維持 28%+","10Y 驗證點":"Asia 占整體營收 40%+；China 單獨破 $1.5B","數字門檻":"Q4 FY26 actual: Asia +28%, China +50%+；H1 FY27 預期 Asia +20%+, China +30%+","信息來源":"RL Q4 FY26 法說會（2026-05-21）+ Bernstein luxury report 2026Q1","漂移觸發":"TTM 連 2 季 Asia"}},{"id":"H2","text":"Pricing Power 持續、Brand Elevation 不退色：AUR 維持高位成長 + GM 維持 68%+","columns":{"2Y 驗證點":"AUR +5%+ 連續 6 季；Adjusted GM ≥ 68% 連續 6 季","5Y 驗證點":"AUR 從基期累積 +30%；GM 維持 ≥ 67%","10Y 驗證點":"Polo Fwd PE 與 Tapestry 之溢價 stabilize 至 +15%+","數字門檻":"Q4 FY26: AUR 高雙位數連續 5 季；Adjusted GM 69%（+40bps）","信息來源":"RL Q4 FY26 8-K + earnings call + Investor's Business Daily 2026-05-21","漂移觸發":"TTM 連 4 季 GM YoY 收縮 > 100bps → 削弱；連 6 季 → 反轉"}},{"id":"H3","text":"資本回饋 + ROIC 維持頂尖：股東回饋 ≥ FCF 的 70%，ROIC 維持 22%+","columns":{"2Y 驗證點":"FY27/28 股東回饋累計 $1.5B+；ROIC ≥ 22%","5Y 驗證點":"$2B 三年資本回饋計畫如期執行；ROIC 維持 ≥ 22%","10Y 驗證點":"$3B 五年累計回饋；ROIC ≥ 20%（成熟期）","數字門檻":"FY26 actual: $700M+ 回饋；ROIC 25% (yfinance, KoalaGains)；dividend +10%","信息來源":"RL Q4 FY26 8-K capital allocation + Macrotrends ROIC history","漂移觸發":"TTM 連 2 季 ROIC"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"中國地產 / 消費結構性收縮：中國中產階級財富萎縮，Polo 在中國從 +50% → +10% 或更低","columns":{"對應假設":"H1","時間尺度":"🔥 中期（4-6 季）","監測指標":"中國國家統計局：城鎮居民可支配收入 YoY；LVMH/Hermes/RL 中國同店銷售 YoY","警戒閾值":"連 2 季 RL Asia"}},{"id":"R2","text":"關稅升級 + 製造成本壓縮：H2 FY27 關稅實際 GM hit 超預期","columns":{"對應假設":"H2","時間尺度":"⚡ 短期（1-2 季）","監測指標":"Q2/Q3 FY27 Adjusted GM YoY change；RL 法說會關於 sourcing diversification 進度","警戒閾值":"Q2/Q3 FY27 GM 連 2 季 YoY 收縮 > 150bps 警戒"}},{"id":"R3","text":"奢侈消費結構大轉向：「炫耀消費」過時，quiet luxury（Brunello 模式）勝出","columns":{"對應假設":"H2","時間尺度":"🐢 長期（2+ 年）","監測指標":"Brunello Cucinelli / Loro Piana 同店增長 vs RL；社群媒體「logo fatigue」discourse 趨勢；GenZ luxury preference 調查","警戒閾值":"跨年度結構性翻轉確認（≥ 50% 機率轉向時需減倉）"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🟡","ma":"✅","trap":"🟢","moat_trend":null,"runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":374.9,"archetype":null,"cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"RL","date":"2026-11-08","schema":"v15.0","contract":"v19","company_name":"Ralph Lauren Corporation"},"oneliner":"品牌升級與亞洲成長仍在兌現，FY27 指引連兩季上調；現價 FY1 19.9 倍下 Base 年化約 8%，低於 10% 門檻，不追，等 346 美元以下再分批。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/RL_20261108/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/RL_20261108/scenario.json","answers":{"q1_business":{"verdict":"賺的是全球中高收入族群為品牌與生活方式付的全價溢價，錢卡在品牌與直營通路這一節，不在製造。","reasoning":"Q2 FY27 營收 21.933 億美元，北美 8.85 億（約 40%）、歐洲 6.96 億（約 32%）、亞洲 5.71 億（約 26%），三區都超過一成。直營過半，CEO 在 2026-08-06 說未來略高於 70%；前三大批發客占 FY26 營收 11%，沒有單一客戶依賴。調整後毛利率 70.5%、調整後營業利益率 15.7%。GAAP 營業利益率 16.6% 反而高於調整後，和法說稱關稅退款不計入調整後的說法方向一致，但差額明細事實表未涵蓋。單點依賴只有 Ralph Lauren 這個品牌本身；製造端約 300 家供應商、單一不超過 5%，不構成依賴。行業環境偏低速，McKinsey 預測 2026 全球時尚低個位數成長，RL 靠單價與組合跑贏；份額提升沒有獨立資料，CEO 在 2026-11-05 也承認產業份額數據不理想。供需持久性：品牌段需求屬結構性持久，上游成本紅利的供給可逆性高。","fact_refs":["f_kpi0_net_revenue_gaap","f_kpi1_adjusted_operating_incom","f_kpi2_gaap_operating_income_ma","f_kpi9_adjusted_gross_margin","f_kpi5_guidance_q3_fy2027","f_kpi6_guidance_full_year_fy202"],"verdict_values":{"revenue_quality":"品質在提升：全價銷售比重上升，主動退出低階批發門市與 off-price；但 Q2 北美批發含約 4 點出貨時點效益，下半年會回吐。","unit_econ_note":"Q2 AUR 年增 9%，同店年增 10%，新增 DTC 客戶 170 萬；行銷占營收 8.6%（去年 7.8%），毛利率擴張有一部分重新投回品牌。","archetype":{"primary":"品質複利成長","secondary":null,"confidence":"中","fingerprint":"毛利率 FY23 到 FY26 由 64.65% 升到 69.87%，股數年減約 3%，資本輕，靠定價與組合，不靠併購。"},"industry":{"clock_phase":"II","sd_verdict_source":"品牌段需求屬結構性持久（亞洲 Q2 年增 28%、核心品項年增 10%）；成本端來自上游過剩與較低產品成本，供給可逆性高。來源為 2026-11-05 法說與 Fibre2Fashion 轉述（未核原文）；擴張判斷依據是公司營收與利潤率，非股價。","bargaining":{"up":"對上游強：約 300 家供應商、單一不超過 5%，公司沒有自有工廠。","down":"對下游偏強：直營過半；前三大批發客占營收 11%，但占應收帳款毛額 29%。","geo":"約 96% 產品在美國境外生產，越南 21%、柬埔寨 16%、印度 11%，美國關稅直接壓在進口成本。"},"profit_pool_dir":"事實表未涵蓋產業利潤池五年資料；公司毛利率上升只能證明公司自身改善，不能證明利潤池方向。","tam_table":{"expanded":false,"reason":"事實表沒有 TAM、滲透率與利潤池序列，只有行業低個位數成長一句，展開只能靠猜；亞洲占比與中國城市數改放成長分部判讀。"}}}},"q2_moat":{"verdict":"護城河方向向上，但速度在放慢；品牌定價力擴大，維護成本也在上升。","reasoning":"機制只有一條：把生活方式形象變成全價成交。可證的比較軸是單價，不是份額：Q2 DTC AUR 年增 9%，基期是去年 +12%；FY23 到 FY26 毛利率升 5.22 個百分點，營業利益率升 4.24 個百分點，毛利擴張多數留住。對最強同業 TPR，營業利益率仍低 7.37 個百分點；對 PVH、LEVI、CPRI 分別高 9.11、5.41、14.42 個百分點。同業 ROIC 與歷史利潤率事實表未涵蓋，差距是否擴大無法直接證明，所以綜合分壓在 8 以下。反例：歐洲 Q2 零售同店 −1%，CFO 說歐洲促銷環比升高；行銷由營收 3%–4% 升到 8.6%，管理層說沒有上限。投入資本、資本支出、折舊都不在事實表，當期 ROIC 無法計算，前份 25% 是外部來源，本輪無法複核。FY24–FY26 累計 FCF 為淨利的 1.13 倍，帳面再投資接近零；FY23 到 FY26 營業利益增加約 5.40 億美元幾乎不靠新資本，真正的再投資走在損益表的行銷費用裡。","fact_refs":["f_peer_rl_gross_margin_pct","f_peer_rl_operating_margin_pct","f_peer_tpr_gross_margin_pct","f_peer_tpr_operating_margin_pct","f_peer_pvh_operating_margin_pct","f_peer_levi_operating_margin_pct","f_peer_cpri_gross_margin_pct","f_peer_cpri_operating_margin_pct","f_kpi9_adjusted_gross_margin"],"verdict_values":{"moat":{"mechanism":"把生活方式品牌形象轉成全價成交：核心經典品項占七成以上，直營過半讓公司自己掌握定價與折扣。","execution":8,"pricing":7,"grade":"B","trend":"↑","trend_evidence":"比較軸採單價與毛利率：Q2 AUR +9%（基期 +12%），FY23–FY26 毛利率 +5.22 個百分點。執行力擴大，定價力在亞洲與北美擴大、歐洲穩定。反例：同業 ROIC 差距沒有資料，份額沒有獨立來源，AUR 下半年回到中個位數。AUR 連 2 季年減或歐洲促銷擴散到北美，就改標向右。","competitor_notes":[{"name":"TPR","strategy_note":"毛利率與營業利益率都高於 RL，是本組最強對手，也說明 RL 不是業內定價最強者；RL 的手袋擴張正面對上它的主場。"},{"name":"PVH","strategy_note":"同屬生活方式服飾，利潤率明顯較低，是 RL 退出低階通路後拉開的對照組。"},{"name":"LEVI","strategy_note":"單一品類品牌，利潤率低於 RL，單價與品類延伸空間較窄。"},{"name":"CPRI","strategy_note":"毛利率仍有六成以上，營業利益率卻只有 2.74%，說明毛利率高不保證營業利潤留得住。"}],"peer_na_reason":"同業 ROIC 與投入資本事實表未涵蓋，只能用毛利率、營業利益率、FCF 利潤率比較。","threats":[{"level":"🟡","text":"低進入門檻與數位通路讓新品牌快速出現，可能搶份額；來源是 10-K 通用風險揭露，未點名對手，按點對點處理。","p":30,"evidence_refs":["competitive_share_entrants#0"]},{"level":"🟡","text":"技術進步讓新產品更快進場，大模型成為新的發現入口；公司已在 OpenAI 平台擴大廣告，目前屬通路變化，不是品牌替代。","p":20,"evidence_refs":["substitute_technology#0"]},{"level":"🟡","text":"品牌熱度退潮的風險：同樣高毛利的 CPRI 營業利益率只有 2.74%，一旦單價與全價銷售回吐，營業槓桿會反向。","p":20,"evidence_refs":[]}],"roic_durability":{"quadrant":"高利益率×周轉率未知（投入資本事實表未涵蓋）","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者、決策者、付款者多半同一人，需求成立；但服飾是想要不是需要，延後購買幾乎沒有代價。讀數：Q2 同店 +10%、核心品項 +10%、新客 170 萬；歐洲 outlet 客流已受通膨壓力。"},{"item":"決策層級","level":"🟡","text":"替代發生在每一次購買，沒有合約也沒有轉換成本，可觀察的只有漲價後銷量。讀數：AUR +9% 同時同店 +10%，單位沒有掉；但 CFO 已假設歐洲下半年有單位彈性，留存率數字事實表未涵蓋。"},{"item":"價值鏈分配","level":"🟢","text":"品牌端拿走最多：約 300 家供應商、單一不超過 5%，調整後毛利率 70.5%；直營過半，前三大批發客 11%。關稅是價值鏈上新的分食者，公司假設 FY27 Q4 起回到高十幾 %。"},{"item":"社會容忍度","level":"🟢","text":"非必需品，漲價沒有政治或社會上限，也不靠監管授權。合規面要留意強迫勞動相關進口法規，事實表未見違規報導。"}],"roiic":"無法計算：投入資本、資本支出、折舊事實表未涵蓋。FY23→FY26 營業利益增加約 5.40 億美元，帳面增量資本接近零，比率沒有意義。","reinvest_rate":"代理值約 −12.8%（FY24–FY26 累計（淨利−FCF）÷淨利）；公式所需資本支出、折舊、營運資金變動未涵蓋。","endo_ceiling":null,"formula_note":"行銷投入走費用不資本化，用公式會低估真實再投資；上界留空，不用推估值代替。"}}}},"q3_growth":{"verdict":"五年後仍有空間，但不算寬，屬中度。","reasoning":"成長組合：單價中個位數（CFO 說 AUR 回到長期中個位數）加低個位數銷量，區域與品類組合再加分，併購為零，回購每年縮股約 2%–3%。三年共識 EPS CAGR 14.8%（FY26 GAAP 15.11 到 FY29 22.84，Koyfin，基期不是調整後口徑，有高估風險）；從 FY27 起算只有 9.8%，營收 FY27→FY28 共識 +5.19%。內生上界因資料缺口算不出，帳面再投資接近零，缺口可歸因於利潤率擴張與淨回購，不靠併購，也不依賴倍數上升。亞洲 Q2 占營收約 26%，中國只在前六大城，女裝、外套、手袋 Q2 低雙位數成長；這些第二曲線主要是管理層說法，滲透率事實表未涵蓋，公司底層成長也只有中個位數，所以不給寬的評等。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_kpi5_guidance_q3_fy2027","f_kpi6_guidance_full_year_fy202"],"verdict_values":{"growth":{"driver_mix":"量價並進、價為主；併購為零；回購每年貢獻約 2 至 3 個百分點 EPS 成長。","runway_years":null,"runway_post_y5":"🟡","endo_ceiling_basis":"公式所需投入資本、資本支出、折舊事實表未涵蓋，上界留空；FY24–FY26 FCF 大於淨利，帳面再投資接近零，保守視為共識超過上界，缺口歸因於利潤率擴張與淨回購。","segments":[{"item":"北美","value":"Q2 8.85 億美元，年增 6%；FY27 指引低到中個位數；Q2 批發含約 4 點時點效益，下半年加速退出低階門市。"},{"item":"歐洲","value":"Q2 6.96 億美元，固定匯率年增 3%；零售同店 −1%；FY27 指引由低到中個位數下修為低個位數。"},{"item":"亞洲","value":"Q2 5.71 億美元，年增 28%，中國逾 35%；Q3 指引高個位數到低雙位數，FY27 低十幾 %，中國中到高十幾 %。"},{"item":"品類","value":"核心品項逾 70%，Q2 年增 10%（Q1 中十幾 %）；高潛力品類 Q2 低雙位數（Q1 逾 20%），兩者都放慢。"}],"decay_signals":[{"signal":"毛利率連 2 季年減","lit":false,"note":"Q2 調整後毛利率固定匯率年增 220bp"},{"signal":"核心市占近 12 個月縮減","lit":false,"note":"無獨立份額資料，管理層稱上升"},{"signal":"主力產品提價後銷量下滑","lit":false,"note":"同店 +10%、AUR +9%；歐洲下半年假設單位彈性，列監測"},{"signal":"EPS CAGR 高於營收 CAGR 超過 5 個百分點","lit":true,"note":"FY26→FY29 EPS 14.8%，FY26→FY28 營收 6.4%，差 8.4 個百分點，靠利潤率與回購"},{"signal":"FCF／淨利連 2 年低於 0.75","lit":false,"note":"FY26 0.749、FY25 1.37，只有一年"},{"signal":"SBC 占營收超過 5% 且上升","lit":false,"note":"年化約 1.5%"},{"signal":"TAM 萎縮或被替代","lit":false,"note":"未見證據，行業低個位數成長"},{"signal":"產業估值倍數近 3 年系統性下移","lit":null,"note":"事實表未涵蓋"},{"signal":"維護性資本支出占 FCF 超過 60%","lit":null,"note":"事實表未涵蓋"},{"signal":"停止投資新產能且收入下滑","lit":false,"note":"Q2 新開 22 家店，營收成長"}],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"資本配置穩健：沒有併購，回購與股息持續，稀釋低；但回購均價不可得，回購是否划算無法驗證。","reasoning":"FCF／淨利 FY23 0.37、FY24 1.40、FY25 1.37、FY26 0.75，四年累計 0.99；FY26 偏低和關稅墊高庫存方向一致（CFO 2026-11-05 說去年基期庫存因關稅偏高），FY27 上半年 FCF 5.04 億美元已回升。SBC 年化約占營收 1.5%。FY27 上半年回購 5 億美元，全年回購計畫已完成；三年 Drive 計畫回饋逾 20 億美元。股息 TTM 殖利率 1.02%，回購加股息約占市值 3.3%。季末現金及短投 18 億美元、債務 12 億美元（法說口徑，不含租賃；事實表淨負債 11.81 億美元含租賃）。近三年現金去向四分、債務到期結構、加權利率、回購均價事實表未涵蓋。關稅退款 CFO 說主要再投資與投入公益方向，股東不要算進去。","fact_refs":["f_kpi4_sbc_six_months","f_kpi3_free_cash_flow_derived_s","f_dividend_yield_ttm","f_shares_diluted_m","f_net_debt_m"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":false,"passed":null,"input":"近 12 個月 8-K 無併購項目；更早的併購事實表未涵蓋。"},{"name":"buyback_yield","applicable":true,"passed":null,"input":"FY27 上半年回購 5 億美元；回購均價與 10 年公債殖利率事實表未涵蓋，無法比較。現價 FY1 盈餘收益率約 5.03%。"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"上半年 SBC 6430 萬美元；由淨利÷稀釋 EPS 反推股數，FY23 約 68.96M 到 FY26 約 62.28M，年減約 3.3%，淨稀釋為負。"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購，資本回饋只有股息與回購兩項；事實表沒有近三年現金去向與債務到期資料，展開也只有 FY27 一期。"}}}},"q5_valuation":{"verdict":"現價要 FY32 EPS 約 29.6 美元且倍數仍有 18 倍，才有約 8% 年化；EPS 我信，倍數不再往上，所以價格合理但不便宜。","reasoning":"FY1 19.88 倍、FY2 18.02 倍。trailing P/E 21.62 倍在 4 個年度端點的 85.5 分位，P/S 96.5 分位、EV/S 97.6 分位；只有 4 個點，只能說目前偏高，而且利潤率上升本來就會推高 P/S。要 10% 年化總報酬，扣 1.02% 股息後五年股價需到約 579 美元，以 18 倍計要 FY32 EPS 32.2 美元，相當於 FY27 起算 CAGR 11.2%，高於共識 FY27→FY29 的 9.8%，也高於我的 Base 9.3%。終端倍數從 18 改成 20，年化由約 8.2% 升到約 10.4%，結論對倍數敏感。賣方目標價各站 352.93 到 430.79 美元、日期不一，現價落在區間內，不支持也不否定本結論。同業倍數事實表未涵蓋，終端倍數沒有同業對照。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_pe_current","f_pe_percentile","f_ps_percentile","f_ev_s_percentile","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_fy1_pct","f_consensus_rev_3m_fy1_pct","f_dividend_yield_ttm","f_rsi14","f_week26_return_pct","f_ma_state"],"verdict_values":{"valuation":{"basis":"FY1 Forward P/E，分母為 Koyfin 調整後共識 EPS。","peers":{"expanded":false,"reason":"事實表只有同業利潤率，沒有同業倍數，無法橫向比較；以自身現值倍數當錨，並在結論中標明此缺口。"},"fwd_pe":19.88,"peg":1.34,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"FY1 19.88 倍；PEG 1.34（三年 CAGR 14.8%，基期為 GAAP）；只看 FY27→FY29 的 9.8%，PEG 為 2.03。Base 年化約 8%；短期上行 6.5%（FY28 EPS 21.1×19 倍），三年上行 23.8%（FY30 EPS 25.2×18.5 倍）。結論為合理偏貴。連續五年高低點事實表未涵蓋，五年分位留空，不用 4 個年度端點代替。","upside_short_pct":6.5,"upside_mid_pct":23.8,"denominator_disputed":false,"denominator_note":"FY1 EPS 各站 18.12 到 19.48 美元，Koyfin 18.94 在 Q2 財報後兩天未變，可能尚未更新；FY1 倍數區間 19.3 到 20.8 倍，不改變結論。真正爭點是 FY29 以後的利潤率，已放進情境。"}}},"q6_how_wrong":{"verdict":"最可能看錯在把利潤率高點當常態；衰退信號亮一項，陷阱風險中等。","reasoning":"最大的錯會出在把 FY27 約 17% 的營業利益率當成常態。五年敏感度（以 Base FY32 為基準）：營業利益率每差 100bp，EPS 差約 1.63 美元、終值差約 29 美元；營收 CAGR 每差 1 個百分點，終值差約 26 美元；股數年減每差 1 個百分點，終值差約 27 美元；終端倍數每差 1 倍，終值差約 30 美元。十類衰退信號亮一項，是 EPS 成長明顯高於營收成長；另兩項因資料缺口未判。庫存尚健康，Q2 淨庫存固定匯率年減 8%，剔除關稅影響年減約 2%。歷史最大回撤與空方最強數字事實表未涵蓋。法說迴避紀錄有三條，集中在季至今趨勢與行銷目標點；本季 CFO 仍不評論季至今趨勢，CEO 則明說 8.6% 不是上限。訴訟方面只有律所徵案，未見已提起的集體訴訟。","fact_refs":["f_ma_w250","f_ma_w104","f_ma_w52","f_pe_percentile","f_consensus_eps_fy2","f_kpi8_inventory"],"verdict_values":{"trap":{"verdict":"🟡","label":"利潤率驅動的成長"}}}},"scenario_inputs":{"terminal_label":"FY2032E","start":{"eps":18.94,"pe":19.88,"basis":"FY1（FY2027E，2027 年 3 月底結束）調整後共識 EPS；五年後同樣以當時進行中的年度 FY2032E 當分母，口徑一致。"},"eps":{"bull":[22.2,25.0,28.2,31.8,35.8],"base":[21.1,23.1,25.2,27.4,29.6],"bear":[18.6,17.8,18.1,18.7,19.4]},"pe":{"bull":21,"base":18,"bear":13},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":1.02,"net_buyback":0},"second_stage":{"bull_cagr_pct":10,"base_cagr_pct":7},"max_dd":{"lo":-46,"hi":-30,"basis":"四個錨：FY1 EPS 打九折×15.5 倍約 264 美元（−30%）；Bear 終值 252 美元（−33%）；Bear 低谷 EPS 17.8×13 倍約 231 美元（−39%）；250 週均線 202.87 美元（−46%）。歷史最大回撤事實表未涵蓋，範圍由這四個錨推出。","trigger_time":null},"basis":{"bull":"FY27 到 FY32 營收年增 7%、營業利益率升到 19.5%、股數年減 2.5%、稅率 22%；亞洲占比破三成，女裝與手袋成第二曲線；21 倍，略高於現值，因成長與利潤率都超預期。","base":"營收年增 5%、營業利益率由約 17% 升到 18.2%、股數年減 2%、稅率 22%；FY32 EPS 29.6 美元，18 倍。EPS 已含回購，淨回購殖利率填 0 避免重複。同業倍數事實表未涵蓋，終端倍數用自身 FY1 19.88 倍依成長放慢折價。","bear":"營收年增 2%、營業利益率回到約 14%、股數年減 1.5%；關稅與促銷吃掉單價，中國放慢。13 倍來自成長由約 9% 降到約 5% 的倍數壓縮（我的判斷，無同業對照）。機率 30%：內生上界算不出，保守視為超出；FY28 也是第一個可能全年承受高十幾 % 關稅的年度。"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"歐洲 Q2 零售同店 −1%，CFO 在 2026-11-05 說歐洲促銷環比升高、下半年假設單位彈性；AUR 下半年由雙位數回到中個位數；公司假設 FY27 Q4 關稅回到高十幾 %。","assumption":"全價銷售的進步來自品牌力，而不是這幾年剛好有利的組合與較低產品成本。","consequence":"FY32 EPS 19.4 美元、13 倍，約 252 美元，−33%；倍數到 10 倍才接近虧 50%。","ruling":"部分採納：納入 30% Bear，但不當主線，歐洲以外的同店與 AUR 都未轉弱。和 Single Thing 重疊，都落在營業利益率能否年年上升。","watch":"歐洲零售同店、北美促銷、調整後毛利率年變動。","evidence_refs":["competitive_share_entrants#0"],"fact_refs":["f_kpi9_adjusted_gross_margin"]},{"view":"論點成功但股東經濟變差","evidence":"CEO 在 2026-11-05 說行銷由營收 3%–4% 升到 8.6%，8.6% 不是上限；FY27 行銷指引由約 8% 上調到 8%–8.5%，而 2026-08-06 CEO 才說維持 8%。關稅退款主要再投資與投入公益方向。","assumption":"每增加一點行銷都有足夠報酬，且毛利率擴張能持續蓋過它。","consequence":"若毛利率增量全數投回行銷、營業利益率停在 17%，Base EPS 複利由 9.3% 降到約 7.9%，FY32 EPS 少約 7%。","ruling":"採納為監測項，暫不扣分：Q2 毛利率 +220bp、費用率 +70bp，營業利益率仍 +140bp。","watch":"行銷占比超過 9% 且營業利益率未擴張。","evidence_refs":[],"fact_refs":["f_kpi1_adjusted_operating_incom"]},{"view":"價格已反映太多","evidence":"FY1 19.88 倍，trailing P/E 在年度端點 85.5 分位，P/S 96.5 分位；股價高於 250 週均線約 86%。","assumption":"倍數維持 18 倍以上，市場繼續把 RL 當高品質複利公司，而不是服飾循環股。","consequence":"倍數每少 1 倍，終值少約 30 美元；EPS 達 Base 但倍數到 13 倍，只值約 385 美元，五年幾乎零報酬。","ruling":"採納：這是不追的主因，進場價定在 346 美元。","watch":"FY1 倍數與 FY28 共識 EPS 修正。","evidence_refs":[],"fact_refs":["f_fwd_pe_latest","f_pe_percentile","f_ps_percentile","f_ma_w250"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 374.9 → 本次 376.56（+0.4%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=374.9","side_b":"本次 price_at_dd=376.56","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 374.9 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 374.9 美元：五年期望值 前份未列，基準年化 前份未列，前份未列不對稱比","side_b":"本次情境、股價仍用 374.9 美元：Bull 價 751.8、Bear 價 252.2，五年期望值 +34.3%，基準年化 7.3%，不對稱比 2.56","ruling":"先換情境、股價不動：五年期望值與基準年化前份未列，無法比較。前份未列不對稱比，本次為 2.56。Bull、Bear 價位與股價無關，只受情境影響。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 374.9 美元：五年期望值 +34.3%，基準年化 7.3%，不對稱比 2.56","side_b":"本次情境、股價 376.56 美元：五年期望值 +33.7%，基準年化 7.2%，不對稱比 2.51","ruling":"再換股價、情境不動：起點價上漲 0.4%，五年期望值少 0.6 個百分點，基準年化少 0.1 個百分點，不對稱比由 2.56 降到 2.51。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"毛利率是結構性還是高點","cause":null,"prior_field":null,"side_a":"CFO 在 2026-08-06 與 2026-11-05 都說毛利率擴張由結構性、可持續因素支撐，FY27 營業利益率不是上限。","side_b":"同場 CFO 也說擴張集中在上半年、AUR 回到中個位數，FY27 Q4 關稅假設回到高十幾 %，歐洲促銷升高。","ruling":"可調和，屬程度差異：單價與組合的改善多半留得住，上半年的速度留不住。Base 只給到 FY32 營業利益率 18.2%。","evidence_level":"公司法說，未經第三方驗證。","settle_metric":"FY28 營業利益率指引與 FY27 Q4 調整後毛利率。","if_then":["如果 FY28 指引仍要求營業利益率年增且 FY27 Q4 毛利率未年減，Bear 機率降到 25%。","如果 FY27 Q4 起調整後毛利率連 2 季年減超過 150bp，減碼一半並取消進場價。"],"evidence_refs":["reg_tariff_export#4"]},{"axis":"下半年減速是時點還是需求","cause":null,"prior_field":null,"side_a":"CFO 在 2026-11-05 歸因於批發出貨時點、off-price 縮減與較難基期，底層仍是中個位數。","side_b":"Q3 指引只有 3%–4%，較 Q2 的 10% 大幅放慢；Q1、Q2 北美批發分別含約 15 點與 4 點時點效益；歐洲指引已下修。","ruling":"未證、監測，不採信也不否定時點歸因。預先登記：FY27 Q3 與 Q4 剔除時點影響的固定匯率成長連 2 季低於 4%，時點說法視為不成立。","evidence_level":"公司說法，兩季內可驗證。","settle_metric":"FY27 Q3、Q4 固定匯率營收成長加回時點影響。","if_then":["如果連 2 季低於 4%，Base 營收 CAGR 由 5% 下修到 3.5%，停止加碼。","如果連 2 季高於 5%，維持 Base，進場價不變。"],"evidence_refs":[]},{"axis":"管理層口徑變動","cause":null,"prior_field":null,"side_a":"2026-08-06：CEO 表示維持 8% 行銷投入，三年歐洲中個位數目標不變；CFO 指引 FY27 歐洲低到中個位數。","side_b":"2026-11-05：FY27 行銷上調到 8%–8.5%，歐洲下修為低個位數；CFO 說歐洲仍領先三年目標。","ruling":"可調和：行銷上調有毛利率超額支撐，但三個月內改口，代表 8.5% 也不能當上限。歐洲領先三年目標的說法，要看 FY28 是否回到中個位數。","evidence_level":"兩場法說逐字對照。","settle_metric":"FY27 全年行銷占比、FY28 歐洲指引。","if_then":["如果 FY27 行銷占比超過 8.5% 且營業利益率擴張低於 80bp，停止加碼。","如果 FY28 歐洲指引仍只有低個位數，不再採信三年中個位數目標。"],"evidence_refs":[]},{"axis":"現在就買或等","cause":null,"prior_field":null,"side_a":"現在就買的最強論證：股價 5 月 22 日到現在幾乎沒動（374.90 到 376.56），FY27 指引卻連兩次上調，Q2 EPS 4.64 美元高於賽前 4.35 美元，Koyfin 共識財報後兩天未更新，RSI 47.64 不熱。","side_b":"Base 年化約 8%，低於 10%；下半年營收放慢、毛利擴張變小，FY28 可能第一次吃滿高十幾 % 關稅。","ruling":"等價格，約束只有價格一項。到 346 美元，同一組 Base 假設的年化總報酬回到約 10%。","evidence_level":"情境推算，對終端倍數敏感。","settle_metric":"收盤價與 FY28 共識 EPS。","if_then":["如果股價續漲而 FY28 共識 EPS 沒有上調，不追。","如果股價跌到 346 美元以下且基本面無損，分批反買第一批。","如果 FY28 共識 EPS 上修到 22.5 美元以上，進場價同比例上調到約 372 美元。"],"evidence_refs":[]},{"axis":"產業態勢三軸","cause":null,"prior_field":null,"side_a":"競爭：10-K 提到低門檻但未點名對手，RL 自稱份額上升。結構：亞洲、直營與全價比重上升，利潤結構轉好。","side_b":"其他變數：美國關稅假設回到高十幾 %，業界調查 85% 受訪者稱關稅傷害財務，歐洲客流轉弱。","ruling":"雙向拉鋸：公司層面結構轉好，外部環境在關稅與歐洲轉弱。依據是 2026-11-05 法說、FY2026 10-K 與 USFIA 2026 調查。","evidence_level":"第一手文件加行業調查。","settle_metric":"調整後毛利率與歐洲零售同店。","if_then":["如果關稅回升後毛利率連 2 季年減超過 150bp，減碼一半。","如果關稅回升後毛利率仍年增，Bear 機率降到 25%。"],"evidence_refs":["supply_demand_durability#2"]},{"axis":"訊號與估值結論維持","cause":"新證據","prior_field":["signal","val"],"side_a":"前份：訊號 B、估值合理偏貴，股價 374.90，Fwd 倍數 20.8 倍（隱含 EPS 約 18.02 美元，前份年度標示可能和本次不同）。","side_b":"本次：訊號 B、估值合理偏貴，股價 376.56，FY1 倍數 19.88 倍。","ruling":"結論不變：指引上調讓倍數下降，但 Base 年化仍只有約 8%。","evidence_level":"公司財報與共識快照。","settle_metric":"FY1 倍數與 Base 年化報酬。","if_then":["如果 Base 年化回到 10% 以上，改為分批買進。"],"evidence_refs":[]},{"axis":"陷阱風險由綠轉黃","cause":"方法變動","prior_field":["trap"],"side_a":"前份：陷阱風險綠。","side_b":"本次：陷阱風險黃，逐項檢查十類衰退信號後，EPS 成長高出營收成長超過 5 個百分點亮一項。","ruling":"不是基本面轉差，是檢查方法更完整。","evidence_level":"年度財務史與共識。","settle_metric":"衰退信號亮燈數。","if_then":["如果亮燈數升到 3 項，停止加碼。"],"evidence_refs":[]},{"axis":"前份空白欄位補值","cause":"方法變動","prior_field":["moat_trend","runway_post_y5","archetype","cycle_position","max_dd_pct","p_bull_pct","p_bear_pct"],"side_a":"前份這些欄位為空值。","side_b":"本次：護城河方向向上、五年後空間中等、公司類型為品質複利、下行範圍 −46% 到 −30%、多空機率 25 比 30；週期位置不適用，裁決與角色由矩陣產生。","ruling":"屬格式補齊，不代表判斷翻轉。","evidence_level":"本次判斷。","settle_metric":"下次複審時比較同一組欄位。","if_then":["如果下次護城河方向改為向右，重算 Bull 機率。"],"evidence_refs":[]},{"axis":"進場條件變動（分批買進）","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"前份文字：等回測 BB 中軌 $356 或 W52 $328 分批；結構化欄位為空。","side_b":"收盤價 ≤346 美元（FY1 約 18.3 倍，Base 年化總報酬回到約 10%）；FY28 共識 EPS 上修時進場價同比例上調。","ruling":"由技術位改為報酬反推，進場價和基本面連動。","evidence_level":"情境推算。","settle_metric":"收盤價。","if_then":["如果收盤 ≤346 美元且基本面無損，分批反買第一批。"],"evidence_refs":[]},{"axis":"減碼與清倉門檻新增","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設（空值），減碼與清倉沒有量化門檻。","side_b":"FY27 Q4 起調整後毛利率連 2 季年減超過 150bp 減碼一半；FY28 營業利益率指引持平或下降、亞洲連 2 季低於 5%、DTC 同店連 2 季轉負，三項中兩項成立就清倉。","ruling":"補上可執行的門檻，毛利率 150bp 沿用前份警戒值。","evidence_level":"公司季度揭露可取得。","settle_metric":"季度財報。","if_then":["如果三項中兩項成立，清倉。"],"evidence_refs":[]},{"axis":"Single Thing 變動","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設（空值）。","side_b":"2027 年 5 月給 FY28 指引時，公司不再要求營業利益率年增（持平或下降）。","ruling":"Single Thing 由空值改為營業利益率指引，因為它是 EPS 最大的單一敏感度。","evidence_level":"情境敏感度推算。","settle_metric":"FY28 營業利益率指引。","if_then":["如果發生，已持有減碼一半，未持有取消進場價。"],"evidence_refs":[]},{"axis":"論點與風險門檻重設","cause":"新證據","prior_field":["thesis.H","thesis.R"],"side_a":"前份：亞洲 +20% 以上連 4 季、中國 +35% 以上連 4 季；毛利率連 2 季年減超過 150bp 警戒；奢侈風格轉向機率 ≥50% 時減倉。","side_b":"本次：亞洲改為 Q3 不低於高個位數、TTM 偏離路徑計；毛利率 150bp 保留；風格轉向併入 R3，Brunello、Loro Piana 同店資料列資料缺口。","ruling":"CFO 已指引 Q3 亞洲高個位數到低雙位數，舊門檻會被基期與主動控速誤觸發，所以重設。","evidence_level":"2026-11-05 法說。","settle_metric":"亞洲固定匯率成長。","if_then":["如果亞洲連 2 季低於 5%，減碼一半。"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"股價收盤到 346 美元以下，Base 年化總報酬回到約 10%，買進第一批。","type":"估值rearm","maps_to":"H2","metric":"收盤價","threshold":"≤346 美元","action":"分批反買","source_freq":"每日收盤","date":null},{"n":2,"text":"FY27 Q3 財報驗證下半年利潤率。","type":"假設驗證","maps_to":"H2","metric":"Q3 固定匯率營業利益率擴張","threshold":"≥50bp（指引下緣）","action":"未達標則停止加碼","source_freq":"每季財報","date":"2027-02"},{"n":3,"text":"FY27 Q3 財報驗證亞洲成長。","type":"假設驗證","maps_to":"H1","metric":"亞洲固定匯率年增","threshold":"不低於高個位數","action":"未達標則停止加碼","source_freq":"每季財報","date":"2027-02"},{"n":4,"text":"關稅回升後公司吸收失敗。","type":"減碼","maps_to":"R1","metric":"調整後毛利率年變動","threshold":"FY27 Q4 起連 2 季年減超過 150bp","action":"減碼","source_freq":"每季財報","date":"2027-08","evidence_refs":["reg_tariff_export#0","reg_tariff_export#4"]},{"n":5,"text":"FY28 指引不再要求營業利益率年增。","type":"Single Thing","maps_to":"H2","metric":"FY28 營業利益率指引","threshold":"持平或下降","action":"減碼","source_freq":"年度指引","date":"2027-05"},{"n":6,"text":"三項中兩項成立就退出：FY28 營業利益率指引持平或下降、亞洲連 2 季低於 5%、DTC 同店連 2 季轉負。","type":"清倉","maps_to":"H2","metric":"三項基本面條件","threshold":"三項中兩項成立","action":"清倉","source_freq":"每季財報","date":null},{"n":7,"text":"共識上修後進場價同比例上調。","type":"加碼","maps_to":"H2","metric":"FY28 共識 EPS 與收盤價","threshold":"EPS ≥22.5 美元且股價 ≤372 美元","action":"分批反買","source_freq":"每月共識快照","date":null},{"n":8,"text":"行銷拉高但利潤率不再擴張。","type":"風險","maps_to":"R3","metric":"行銷占營收與營業利益率","threshold":"行銷超過 9% 且營業利益率連 2 年未擴張","action":"停止加碼","source_freq":"年度財報","date":null},{"n":9,"text":"FY27 Q3 財報後重新審視整份判斷。","type":"複審日期","maps_to":"H1","metric":"整體論點","threshold":"財報後一週內","action":"停止加碼直到複審完成","source_freq":"每季","date":"2027-02"}],"kill_metrics":[{"metric":"調整後毛利率年變動","bear_threshold":"連 2 季年減超過 150bp","window":"FY27 Q4 起連續 2 季","source":"公司季度新聞稿","last_status":"ok"},{"metric":"FY28 營業利益率指引","bear_threshold":"持平或下降","window":"2027 年 5 月 FY27 Q4 財報","source":"公司年度指引與法說","last_status":"unknown"},{"metric":"亞洲營收固定匯率年增","bear_threshold":"連 2 季低於 5%","window":"FY27 Q4 起連續 2 季","source":"公司季度新聞稿","last_status":"ok"},{"metric":"全球 DTC 同店成長","bear_threshold":"連 2 季轉負","window":"每季","source":"公司季度法說","last_status":"ok"},{"metric":"行銷占營收與營業利益率","bear_threshold":"行銷超過 9% 且營業利益率連 2 年未擴張","window":"FY28 至 FY29","source":"公司年度財報與法說","last_status":"ok"}],"action_conditions":{"rearm_trigger":"收盤價 ≤346 美元（FY1 約 18.3 倍，Base 年化總報酬回到約 10%）；FY28 共識 EPS 上修時進場價同比例上調。","exec_line":"現價不追。到 346 美元以下分三批：第一批觸價，第二批等 FY27 Q3 調整後毛利率未年減，第三批等 FY28 營業利益率指引仍年增；任一批後觸發減碼或清倉條件就停止。"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"收盤價 ≤346 美元，約等於 Base 年化總報酬 10%。"},"thesis":{"H":[{"id":"H1","text":"亞洲仍是最大增量，中國從前六大城往外擴，帶動營收與毛利率組合。","2y":"FY29 亞洲固定匯率年增維持 10% 以上；同季占營收由 Q2 FY27 的 26% 升到 28% 以上。","5y":"FY32 Q2 亞洲占營收 32% 以上。","10y":null,"threshold":"FY27 亞洲低十幾 %、中國中到高十幾 %；Q3 FY27 亞洲不低於高個位數。","source":"公司季度新聞稿分區營收與 2026-11-05 法說分區指引。","drift_rule":"亞洲 TTM 營收偏離路徑 5% 以上連 2 季為削弱，偏離 10% 以上連 3 季為反轉。"},{"id":"H2","text":"全價銷售與單價提升留得住，FY32 營業利益率比 FY27 高。","2y":"FY29 調整後毛利率 70% 以上，營業利益率每年高於前一年。","5y":"FY32 調整後營業利益率 18% 以上。","10y":null,"threshold":"FY27 固定匯率毛利率與營業利益率各擴張 80–100bp；FY28 指引仍要求營業利益率年增。","source":"公司季度新聞稿、年度指引與法說。","drift_rule":"TTM 營業利益率偏離路徑 5% 以上連 4 季為削弱，偏離 10% 以上連 6 季為反轉；2 年目標按連 2 季、連 3 季計。"},{"id":"H3","text":"行銷加碼後仍有營業槓桿，現金持續回到股東手上並縮股。","2y":"三年 Drive 計畫回饋逾 20 億美元如期完成；FY29 行銷占比 9% 以下，或營業利益率仍擴張。","5y":"FY32 股數由目前 59.1M 降到 53.5M 以下；五年累計 FCF／淨利 0.9 以上。","10y":null,"threshold":"FY27 行銷占營收 8%–8.5%；FY27 上半年回購 5 億美元已完成全年計畫。","source":"公司季度新聞稿、現金流量表與法說。","drift_rule":"TTM FCF／淨利或股數偏離路徑 5% 以上連 2 季為削弱，偏離 10% 以上連 3 季為反轉。"}],"R":[{"id":"R1","text":"關稅吸收失敗：約 96% 產品在美國境外生產，公司假設 FY27 Q4 起關稅回到高十幾 %，FY28 可能第一次吃滿全年；業界調查 85% 受訪者稱關稅傷害財務。","h_ref":"H2","clock":"⚡","threshold":"FY27 Q4 起調整後毛利率連 2 季年減超過 150bp。","evidence_refs":["reg_tariff_export#0","reg_tariff_export#4","supply_demand_durability#2"]},{"id":"R2","text":"中國與亞洲放慢：FY27 Q4 是中國最難基期，法說有分析師提到其他奢侈品牌在中國轉弱，公司回應是主動控速。","h_ref":"H1","clock":"🔥","threshold":"亞洲固定匯率年增連 2 季低於 5%。","evidence_refs":[]},{"id":"R3","text":"品牌熱度或風格轉向，行銷投入報酬下降：行銷沒有上限，若風格轉向，單價與行銷效率會同時變差。","h_ref":"H3","clock":"🐢","threshold":"行銷超過營收 9% 且營業利益率連 2 年未擴張；風格轉向機率 ≥50% 時減倉，Brunello、Loro Piana 同店對照為資料缺口。","evidence_refs":[]},{"id":"R4","text":"歐洲客流壓力擴散到全價通路：目前壓力集中在 outlet，CFO 已說歐洲促銷環比升高。","h_ref":"H2","clock":"🔥","threshold":"歐洲零售同店連 2 季 ≤−3%，或公司說明北美促銷升高。","evidence_refs":[]}],"single_thing":{"description":"2027 年 5 月給 FY28 指引時，公司不再要求營業利益率年增（持平或下降）。","why_fatal":"營業利益率是 EPS 最大的單一敏感度：每 100bp 約等於 FY32 EPS 5.5%。Bear 與 Bull 的利益率差 5.3 個百分點，對應約 29% EPS；CFO 在 2026-11-05 說長期計畫每年都預期擴張，一旦失守，18 倍的理由也會動搖。","if_happens":"已持有減碼一半；未持有取消 346 美元進場價，Bear 機率升到 40% 重算。","how_monitor":"FY27 Q3、Q4 調整後毛利率與費用率，FY28 指引，行銷占營收。","probability":"約 25%（12–24 個月）；理由是 FY28 要吃滿較高關稅並回測第 53 週，但管理層連續上調指引的紀錄較好。"}},"appendix_a":{"growth_durability":6,"quality_score":9,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":18.02,"peg_fy2":1.22,"stress":{"pass":null,"total":null}},"eps_meta":{"base_eps_path":{"FY2026A":15.11,"FY2027E":18.94,"FY2028E":20.9,"FY2029E":22.84},"fy_end_month":3,"eps_basis":"FY2026A 為 GAAP 稀釋 EPS（事實表沒有調整後基期）；FY2027E–FY2029E 為 Koyfin 調整後共識，家數事實表未涵蓋。基期與預估口徑不同，三年 CAGR 可能高估。"},"catalysts":[{"date":"2027-01","date_precision":"month","type":"regulatory","event":"公司假設美國關稅由約 10% 回到高十幾 %（FY27 Q4 起）","impact":"高","watch":"FY27 Q4 調整後毛利率年變動"},{"date":"2027-02","date_precision":"month","type":"guidance","event":"FY27 Q3 財報","impact":"高","watch":"營業利益率擴張是否達 50–70bp、亞洲是否高個位數以上、剔除時點的成長是否中個位數"},{"date":"2027-05","date_precision":"month","type":"guidance","event":"FY27 Q4 財報與 FY28 指引（月份依前一年公告時間推估）","impact":"高","watch":"FY28 營業利益率指引是否仍年增"}],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8w(原9)","pacing":[],"holding_cap":null,"audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='↑', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟡', moat_trend='↑', week26=5.61, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position=None, moat='B', moat_trend='↑', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":false,"basis":"signal='B', val='🟡'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":true,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"8w","condition":"判斷者宣告 wait_for_price（價格合理但要等）→ 原 row9 進場改觀望（等價格）","hit":true,"basis":"wait_for_price=True, 等待條件='收盤價 ≤346 美元，約等於 Base 年化總報酬 10%。'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"requires_critic":[]}}
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
