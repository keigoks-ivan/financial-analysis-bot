你是 DD 管線 v20 的判斷層閘（gate），標的 CRWV（20261012）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

⑤ 覆蓋面掃描（強制）——facts.json 逐軸點名 status="none"／"not_applicable" 的每一軸：理由站得住嗎？查詢是否切題且足以支撐該軸結論（不以查詢次數計）？**缺軸本身即 🔴，不需先證明結論錯**。[gate_contract §⑤]

⑥ 量化模組完整性抽查（強制）——(i) `moat.roic_durability.reinvest_rate`／`.roiic` 有沒有 `.formula_note` 真算（寫「估計約 X%」無算式＝🔴）；`.endo_ceiling` 是否與共識 EPS CAGR（facts.json）交叉檢查，天花板 < CAGR 且 `reasoning` 未處理＝🔴。(ii) `scenario_inputs` 的 Bull/Base/Bear EPS 是否有實質價差（Bull 幾乎等於 Base、只靠倍數撐估值＝退化，🔴）；`scenario_inputs.valuation_basis`＝`sales_multiple`（虧損公司，程式決定）時改查 Bull/Base 的營收路徑（`rev`）：Bull 終端營收須實質高於 Base、Bull 前兩年不得與 Base 相同，只靠終端 EV/S 撐價差＝退化，🔴；並看 Bear 的 `net_debt_y5`／`shares_y5` 是否反映該情境的融資缺口與稀釋（債重公司 Bear 沿用目前淨負債與股數＝樂觀，🟡）。(iii) `decision_inputs.irr_base_pct`／`ev5y_pct`／`asym_ratio` 缺省或 null 合法（程式回填），但 ROIIC 缺輸入、口徑或算式仍為實質問題。[gate_contract §⑥]

⑦ 數字新鮮度——`judgment.json` 引用的每個營運指標，是否不比 facts.json 的 `latest_quarter_kpis[].as_of` 對應項目舊？有一個更舊即 🔴。`decision_inputs.consensus_rev_3m_pct` 若依附 `stale=true` 來源，確認未被當唯一依據；引用摘要內容的欄位須標「來源：摘要」。[gate_contract §⑦]

⑧ 前份漂移歸因（QC-49）——facts.json 的 `prior_dd` 存在時，`drift_watch` 20 欄中有變動的每一欄是否都映射到 `contradictions[]` 一個帶 `cause` 的條目（可多欄共用一條目）、且主因站得住；**裁決／核心假設／情境方法變更不得併入純價格原因**；漏欄或無歸因＝🔴；前份該欄本身空或缺欄者不計，給 🟡 或 🟢。無前份時填 🟢 並註「無前份」。[gate_contract §⑧]
  - `axis` 以 `[程式歸因]` 開頭的條目是程式算的（均線、現價、期望報酬拆解、裁決、角色）。「期望報酬拆解」兩條是程式用本次情境先換情境、再換股價算出的數字（asym_ratio／ev5y_pct／irr_base_pct／bull_5y_price／bear_5y_price），視為已歸因，其中「價格變動」只是股價效果，不適用「不得併入純價格原因」。裁決／角色條目是反事實結果（逐一把矩陣輸入改回前份值重算），視為已歸因；其中「價格變動」是反事實證明估值燈單獨改變了裁決，不適用上面「不得併入純價格原因」，不要為此給 🔴（2026-09-24）。
  - QC-49 承繼（90 天內翻面須引前次已發火觸發器）只比方向：進場／觀望／迴避。「進場」與「進場·條件式」同方向，角色（核心／衛星）變動也不在 QC-49 範圍；判斷者答 `decision_inputs.qc49_inherit_prior`，前次裁決與角色由程式帶入。

## (a)(b) 兩項強制職責（2026-08-06 拍板，不得因精簡拿掉）

(a) 覆蓋面掃描：逐軸點名「哪一軸整個沒查」，做法同 checklist ⑤，缺軸本身即 🔴。
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

### 判斷檔 `fact_refs` 引到的事實（32 條）
- `f_kpi0_revenue_gaap`（q1_business）｜Revenue (GAAP)＝2575 USD M｜期間與口徑：Q2 2026（季末 2026-06-30，公告於 2026-08-11）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 https://investors.coreweave.com/news/news-details/2026/CoreWeave-Reports-Strong-Second-Quarter-2026-Results/default.aspx（numbers.latest_quarter_kpis.items[0]，as_of Q2 2026（季末 2026-06-30，公告於 2026-08-11））
  - 註記：未取得 consensus（查無）
- `f_kpi1_non_gaap_adjusted_operat`（q1_business）｜Non-GAAP (adjusted) operating income＝128 USD M（利益率 5.0%）｜期間與口徑：Q2 2026（季末 2026-06-30，公告於 2026-08-11）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 https://investors.coreweave.com/news/news-details/2026/CoreWeave-Reports-Strong-Second-Quarter-2026-Results/default.aspx（numbers.latest_quarter_kpis.items[1]，as_of Q2 2026（季末 2026-06-30，公告於 2026-08-11））
  - 註記：未取得 consensus（查無）
- `f_kpi2_gaap_operating_income_lo`（q1_business）｜GAAP operating income (loss)＝-49 USD M（利益率 -1.9%）｜期間與口徑：Q2 2026（季末 2026-06-30，公告於 2026-08-11）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 https://investors.coreweave.com/news/news-details/2026/CoreWeave-Reports-Strong-Second-Quarter-2026-Results/default.aspx（numbers.latest_quarter_kpis.items[2]，as_of Q2 2026（季末 2026-06-30，公告於 2026-08-11））
  - 註記：未取得 consensus（查無）
- `f_kpi5_guidance_q3_2026`（q1_business）｜Guidance Q3 2026＝營收 3,450–3,600；adjusted operating income 200–260；利息費用 860–940；capex 11,500–13,500 USD M｜期間與口徑：Q3 2026 指引（2026-08-11 法說會）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：新聞稿未載指引；取自 MarketBeat 法說會摘要 https://www.marketbeat.com/instant-alerts/coreweave-q2-earnings-call-highlights-2026-08-11/（二手，需對照逐字稿）（numbers.latest_quarter_kpis.items[5]，as_of Q3 2026 指引（2026-08-11 法說會））
  - 註記：未取得
- `f_kpi6_guidance_fy2026`（q1_business）｜Guidance FY2026（上調）＝營收 12,400–13,200；adjusted operating income 960–1,150；capex 35,000–39,000；年底年化營收 18,500–19,500；年底 active power >1.85 GW（前 >1.7 GW） USD M｜期間與口徑：FY2026 指引（2026-08-11 法說會）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：同上 MarketBeat（二手）（numbers.latest_quarter_kpis.items[6]，as_of FY2026 指引（2026-08-11 法說會））
  - 註記：未取得
- `f_kpi7_revenue_backlog`（q1_business）｜Revenue backlog＝104 USD B（不含早 Q3 新增逾 25B 承諾）｜期間與口徑：Q2 2026（季末 2026-06-30，公告於 2026-08-11）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 https://investors.coreweave.com/news/news-details/2026/CoreWeave-Reports-Strong-Second-Quarter-2026-Results/default.aspx（numbers.latest_quarter_kpis.items[7]，as_of Q2 2026（季末 2026-06-30，公告於 2026-08-11））
  - 註記：n/a
- `f_kpi8_active_power_contracted_`（q1_business）｜Active power／Contracted power＝1.5 GW／約 3.7 GW｜期間與口徑：Q2 2026（季末 2026-06-30，公告於 2026-08-11）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 https://investors.coreweave.com/news/news-details/2026/CoreWeave-Reports-Strong-Second-Quarter-2026-Results/default.aspx（numbers.latest_quarter_kpis.items[8]，as_of Q2 2026（季末 2026-06-30，公告於 2026-08-11））
  - 註記：n/a
- `f_peer_crwv_gross_margin_pct`（q2_moat）｜CRWV 毛利率＝67.42 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CRWV.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝12869.75 USD m｜期間與口徑：2026-10-12／yfinance revenue_estimate 0y 平均（40 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-10-12）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_peer_crwv_operating_margin_pct`（q2_moat）｜CRWV 營業利益率＝-3.04 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CRWV.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_crwv_fcf_margin_pct`（q2_moat）｜CRWV FCF 利潤率＝-179.92 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CRWV.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_nbis_gross_margin_pct`（q2_moat）｜NBIS 毛利率＝74.26 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.NBIS.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_nbis_operating_margin_pct`（q2_moat）｜NBIS 營業利益率＝-50.48 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.NBIS.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_orcl_operating_margin_pct`（q2_moat）｜ORCL 營業利益率＝34.23 %｜期間與口徑：TTM ending 2026-08-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ORCL.operating_margin_pct，as_of TTM ending 2026-08-31（4季加總））
- `f_peer_iren_operating_margin_pct`（q2_moat）｜IREN 營業利益率＝-53.57 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.IREN.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_kpi3_free_cash_flow_679_capex`（q4_capital）｜Free cash flow（營運現金流 679 減 capex 6,422，自算）＝-5743 USD M｜期間與口徑：Q2 2026（季末 2026-06-30，公告於 2026-08-11）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 https://investors.coreweave.com/news/news-details/2026/CoreWeave-Reports-Strong-Second-Quarter-2026-Results/default.aspx（OCF 679、purchase of PP&E 6,422；公司未報 FCF，此為自算）（numbers.latest_quarter_kpis.items[3]，as_of Q2 2026（季末 2026-06-30，公告於 2026-08-11））
  - 註記：n/a
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝26295.93 USD m｜期間與口徑：2026-10-12／yfinance revenue_estimate +1y 平均（40 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-10-12）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝-3.94 USD/share｜期間與口徑：2026-10-08／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261008.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-10-08）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝-1.81 USD/share｜期間與口徑：2026-10-08／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261008.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-10-08）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝1.25 USD/share｜期間與口徑：2026-10-08／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261008.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-10-08）
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝7.65 %｜期間與口徑：2026-07-16 → 2026-10-08／FY1 共識 EPS -3.66 → -3.94（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261008.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-10-08）
- `f_kpi4_sbc`（q4_capital）｜SBC 占營收＝6.4 %（SBC 165 USD M ÷ 營收 2,575；GAAP 營業利益為負故以營收為分母）｜期間與口徑：Q2 2026（季末 2026-06-30，公告於 2026-08-11）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 https://investors.coreweave.com/news/news-details/2026/CoreWeave-Reports-Strong-Second-Quarter-2026-Results/default.aspx（numbers.latest_quarter_kpis.items[4]，as_of Q2 2026（季末 2026-06-30，公告於 2026-08-11））
  - 註記：n/a
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝46074.0 USD m｜期間與口徑：2026-10-12／yfinance 最新一季：總債務 51613.0、現金 5539.0（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-10-12）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝551.54 m shares｜期間與口徑：2026-10-12／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-10-12）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝82.08 USD｜期間與口徑：2026-10-09（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-10-09（RTH 收盤，UTC））
- `f_ev_m`（q5_valuation）｜目前企業價值 EV（市值＋淨負債）＝91344.12 USD m｜期間與口徑：2026-10-12／市值 45270.12 ＋ 淨負債 46074.0｜kind：realized
  - 來源：—（numbers.capital_structure.ev_m，as_of 2026-10-12）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝12.03 x｜期間與口徑：2026-10-09（RTH 收盤，UTC）／4 個年度端點內的分位＝0.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-10-09（RTH 收盤，UTC））
- `f_ev_s_fwd`（q5_valuation）｜EV/S（EV ÷ FY1 共識營收）＝7.1 x｜期間與口徑：2026-10-12／f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）｜kind：estimate
  - 來源：—（numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m，as_of 2026-10-12）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝0.0 %｜期間與口徑：2026-10-09（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-10-09（RTH 收盤，UTC））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝5.96 x｜期間與口徑：2026-10-09（RTH 收盤，UTC）／4 個年度端點內的分位＝0.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-10-09（RTH 收盤，UTC））
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝-19.53 %｜期間與口徑：2026-10-09（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-10-09（RTH 收盤，UTC））
- `f_rsi14`（q5_valuation）｜RSI(14)＝43.71｜期間與口徑：2026-10-09（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-10-09（RTH 收盤，UTC））

### findings_digest 中方向為負或來源衝突的條目（29 條）
- `customer_second_source#0`（customer_second_source｜方向 -｜狀態 ok）：CoreWeave 2026 Q2 10-Q 表示預期少數大客戶集中度將持續（合約長期性），且大客戶需求或履約意願的不利變化會衝擊業績；未見其揭露最大客戶導入第二供應商或自製。
  - 來源：CoreWeave Form 10-Q (period ended 2026-06-30), SEC EDGAR（as_of 2026-06-30）｜affects：decision_inputs.bear、thesis.R
- `customer_second_source#2`（customer_second_source｜方向 -｜狀態 ok）：OpenAI 與 Broadcom 宣布 10GW 自研加速器合作，2026 下半年起部署、2029 年底完成；晶片初期用於 OpenAI 自家資料中心。報導無 CoreWeave 專屬資訊，亦未確認 2026 出貨進度。
  - 來源：Capital Brief / Yahoo Finance / Outlook Business 報導 OpenAI-Broadcom 10GW deal（as_of 2025-10-13）｜affects：decision_inputs.bear、triggers
- `customer_concentration_credit#2`（customer_concentration_credit｜方向 -｜狀態 ok）：Q2 2026 10-Q 風險語言：預期因長約，營收仍將集中於少數大客戶；這些客戶需求或履約能力的負面變化會損害業績
  - 來源：SEC EDGAR CoreWeave 10-Q 期間 2026-06-30（經搜尋摘要轉述）（as_of 2026-06-30）｜affects：thesis.R、decision_inputs.bear
- `customer_concentration_credit#4`（customer_concentration_credit｜方向 -｜狀態 ok）：OpenAI（主要非超大規模客戶）無公開信用評等；第三方報導稱截至 2026-03-31 無負債但採購承諾約 $6,650 億（未審計、非公開文件），2026 年初單季燒現金約 $37 億；IFR 估計供應商帳單到期將出現約 $200 億缺口
  - 來源：Vested Finance community / IFR 'OpenAI faces financial crunch point as huge supplier bills start to come due'（二手報導）（as_of 2026-03-31）｜affects：thesis.R、decision_inputs.bear
- `supply_demand_durability#3`（supply_demand_durability｜方向 -｜狀態 ok）：Spheron (GPU-cloud vendor) says GPU availability has improved over the past 18 months with neo-clouds and resellers offering H100/H200/Blackwell capacity; scarce input shifting from GPUs to grid connections. Vendor-biased source; no independent 2027 price forecast found.
  - 來源：Spheron blog: AI data center power constraints 2026（as_of 2026-01-01）｜affects：decision_inputs.bear、moat_trend
- `regulatory_antitrust#1`（regulatory_antitrust｜方向 -｜狀態 ok）：10-Q 提及聯邦與州層級 AI 法規、跨轄區規則衝突，可能放慢客戶對平台的需求。
  - 來源：CoreWeave Form 10-Q FY2026 (period ended 2026-06-30), SEC（as_of 2026-06-30）｜affects：thesis.R、decision_inputs.bear
- `regulatory_antitrust#2`（regulatory_antitrust｜方向 -｜狀態 ok）：Blockspace 報導：CEO Intrator 稱地方資料中心禁建令會改變建設地點而非減少需求；紐約州行政命令暫停大型新資料中心（≥50MW）部分環評核准最長一年。報導日期未能核實。
  - 來源：Blockspace Media, 'CoreWeave shifts data center sites amid moratoriums'（as_of 2026-08-12）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#1`（reg_tariff_export｜方向 -｜狀態 ok）：商務部長須於 2026-07-01 前提交美國資料中心用半導體市場更新，作為調整關稅制度依據；本軸未查到該更新內容。總統保留日後擴大課稅權限。
  - 來源：White & Case, President Trump orders narrowly targeted 25% Section 232 tariff on certain advanced semiconductor articles（as_of 2026-01-15）｜affects：decision_inputs.bear、thesis.R
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：FY2025 10-K 一般性風險因素把中國與台灣緊張、關稅、貿易管制列為可能壓抑需求與定價的總體地緣因素；摘要未顯示公司在兩地有直接營運或供應商。
  - 來源：CoreWeave Form 10-K FY2025 (SEC)（as_of 2026-02-28）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：2025 年底第三方資料中心供應商未如期交付，致 CoreWeave 下修全年營收預測；管理層稱延遲多數於 2026 年 Q1 解決。
  - 來源：Bisnow: Data Center Delays Trigger Sell-Off Of AI Cloud Firm CoreWeave（as_of 2025-11-10）｜affects：thesis.R、triggers
- `geo_supply_chain#2`（geo_supply_chain｜方向 -｜狀態 ok）：2026 年 3 月會議摘要：供應鏈執行『極其困難』，並區分電網可得性與實際送達機櫃的可用電力。
  - 來源：MarketBeat: CoreWeave conference, 2026 compute capacity broadly sold out（as_of 2026-03-08）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#3`（geo_supply_chain｜方向 -｜狀態 ok）：2026 年 1 月報導：川普對數個歐洲國家的關稅威脅衝擊 CoreWeave 股價，因其在挪威、瑞典、英國等地興建資料中心。
  - 來源：Finviz: What's happening with CoreWeave stock this week（as_of 2026-01-20）｜affects：thesis.R
- `end_markets#4`（end_markets｜方向 -｜狀態 ok）：Contrary Research（2026-06）認為受融資與需求規模要求，許多較小 neocloud 難以存活。
  - 來源：Contrary Research, 'why 20% of neoclouds won't survive the AI boom'（as_of 2026-06-30）｜affects：thesis.R、decision_inputs.bear
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：Hyperscaler custom AI ASICs（Google TPU、AWS Trainium3、Meta MTIA 等）擴張中；Broadcom 稱 2027 年 AI 晶片營收有超過 1000 億美元的能見度、已揭露 730 億美元 AI 積壓訂單；TPU v6e 在 Google Cloud 按需 $2.70／chip-hour（價格效能為 Google 自家基準）
  - 來源：Tom's Hardware, The custom AI ASIC state of play (May 2026)（as_of 2026-05-31）｜affects：moat_trend、decision_inputs.bear
- `substitute_technology#1`（substitute_technology｜方向 -｜狀態 ok）：第三方部落格（Introl, 2026-02）預測客製 ASIC CAGR 約 44.6%、主攻推論，並稱 Nvidia 推論市占 2028 年可能由 90%+ 降至 20–30%；屬二手預測，來源權威性較低
  - 來源：Introl, The Custom Silicon Inflection Point (Feb 2026)（as_of 2026-02-28）｜affects：moat_trend、decision_inputs.bear
- `substitute_technology#2`（substitute_technology｜方向 -｜狀態 ok）：CoreWeave 以六年（2023 年前為五年）折舊 GPU；批評者（含 Burry）認為 Nvidia 年度換代使舊硬體 2–3 年即經濟性過時；公司反駁稱 H100 到期後以原價 95% 再簽約。日期為文章發布日未確認，來源多為評論／電子報
  - 來源：Yahoo Finance / Electroneconomics Substack 等評論（搜尋摘要彙整）（as_of 2026-01-01）｜affects：decision_inputs.bear、valuation、thesis.R
- `capital_markets_pricing#2`（capital_markets_pricing｜方向 -｜狀態 ok）：2026 capex 指引由 $31–35B 上調至 $35–39B；Q3 營收指引 $3.45–3.6B（二手來源）。公司表示後續投資可能需額外債務與/或股權融資。
  - 來源：CoreWeave Q2 2026 earnings summaries (channelchek / indmoney / quartr)（as_of 2026-08-11）｜affects：thesis.R、decision_inputs.bear
- `major_events#0`（major_events｜方向 -｜狀態 ok）：2025-07-07 CoreWeave 宣布以全股票方式收購 Core Scientific（約 $9B，換股比 0.1235 CRWV/CORZ）；2025-10-30 因 Core Scientific 股東未批准而終止合併，維持商業合作。
  - 來源：TipRanks: CoreWeave terminates merger with Core Scientific（as_of 2025-10-30）｜affects：thesis.R、decision_inputs.bear
- `major_events#1`（major_events｜方向 -｜狀態 ok）：聯邦證券集體訴訟 Masaitis v. CoreWeave（D.N.J., No. 2:26-cv-00355），class period 2025-03-28 至 2025-12-15，指控高估滿足客戶需求能力、低估對單一第三方資料中心供應商（Denton, TX）依賴之風險；主理原告截止日 2026-03-13。為原告律所新聞稿所述指控，非裁決。
  - 來源：Berger Montague: CoreWeave securities fraud（as_of 2026-01-13）｜affects：decision_inputs.bear、thesis.R
- `major_events#2`（major_events｜方向 -｜狀態 ok）：2025-11-10 Q3 結果下修 2025 年營收指引，原因為第三方資料中心開發商進度落後。
  - 來源：Glancy Prongay Murray (BusinessWire): Securities Fraud Investigation Into CoreWeave（as_of 2026-01-14）｜affects：thesis.R、valuation
- `unprofitable_dilution_trajectory#0`（unprofitable_dilution_trajectory｜方向 -｜狀態 ok）：年度稀釋加權股數：2023 約403.7M、2024 404.4M、2025 436.0M（+7.8% YoY）；AlphaQuery 獨立列示 FY2025 為436.00M
  - 來源：AlphaQuery / tickerleague 彙整（weighted average shares outstanding diluted）（as_of 2025-12-31）｜affects：decision_inputs.bear、valuation
- `unprofitable_dilution_trajectory#1`（unprofitable_dilution_trajectory｜方向 -｜狀態 ok）：聚合站Digrin列示SBC約每季$144M–$165M（2025Q3至2026Q2）；2025全年SBC約$630M，2024為$31.49M（聚合站數字，未對照10-K）
  - 來源：Digrin CRWV Financials；tickerleague SBC expense（第三方彙整）（as_of 2026-06-30）｜affects：decision_inputs.bear、valuation
- `unprofitable_dilution_trajectory#3`（unprofitable_dilution_trajectory｜方向 -｜狀態 ok）：TIKR稱CoreWeave併購Core Scientific（$9B全股票）完成時將顯著稀釋既有股東；是否已完成未查證
  - 來源：TIKR blog：CoreWeave (NASDAQ: CRWV) stock tanks over 10% as investors are worried about narrowing margins（as_of 2026-01-01）｜affects：decision_inputs.bear、triggers
- `unprofitable_path_to_profitability#1`（unprofitable_path_to_profitability｜方向 -｜狀態 ok）：2026 資本支出指引上調至 $35–39B（原 $31–35B）；Q2 capex $9.4B，Q3 指引 $11.5–13.5B。
  - 來源：MarketBeat, CoreWeave Q2 earnings call highlights (2026-08-11)（as_of 2026-08-11）｜affects：decision_inputs.bear、thesis.R
- `unprofitable_path_to_profitability#2`（unprofitable_path_to_profitability｜方向 -｜狀態 ok）：Q2 2026 調整後營業利益 $128M（5% 利潤率），淨損 $626M，利息費用 $640M；Q3 利息費用指引 $860–940M。管理層預期調整後營業利益率逐季擴張，Q4 達低十位數百分比（low-teens）。
  - 來源：MarketBeat, CoreWeave Q2 earnings call highlights (2026-08-11)（as_of 2026-08-11）｜affects：thesis.R、decision_inputs.bear、triggers
- `unprofitable_path_to_profitability#3`（unprofitable_path_to_profitability｜方向 -｜狀態 ok）：2025 年 FCF 約 -$7.25B（營運現金流 $3.1B、capex $10.3B）；『FCF 轉正』為第三方分析預期，非公司目標。
  - 來源：DefiLlama dashboard, CRWV revenue streams and P/E（as_of 2026-08-31）｜affects：valuation、decision_inputs.bear
- `unprofitable_path_to_profitability#4`（unprofitable_path_to_profitability｜方向 -｜狀態 ok）：2025 年底總債務約 $29.82B；管理層稱燒錢屬刻意前置、已鎖定約 300bp 較低借款成本，但有分析稱年度數字尚未印證。
  - 來源：TIKR, CoreWeave's $640M interest bill is growing faster than its $128M profit（as_of 2026-08-15）｜affects：thesis.R、decision_inputs.bear
- `ma_merger#0`（ma_merger｜方向 -｜狀態 ok）：2025-07-07 宣布全股票收購 Core Scientific（約 $9B）；2025-10-30 因 CORZ 股東否決而終止。搜尋未見 2026 年新的併購協議。
  - 來源：TipRanks: CoreWeave terminates merger with Core Scientific（as_of 2025-10-30）｜affects：thesis.R、decision_inputs.bear
- `lawsuit_class_action#0`（lawsuit_class_action｜方向 -｜狀態 ok）：Masaitis v. CoreWeave（D.N.J. 2:26-cv-00355）證券詐欺集體訴訟，class period 2025-03-28~2025-12-15，Section 10(b)/20(a)；另有第二件類似訴狀；主理原告截止 2026-03-13。屬指控非裁決。
  - 來源：Berger Montague: CoreWeave securities fraud（as_of 2026-01-13）｜affects：decision_inputs.bear、thesis.R

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 4 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CRWV_20261012/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":272.9,"bear_5y_price":0.0,"p_bull_pct":20,"p_bear_pct":30,"upside_5y_pct":25.6,"ev5y_pct":29.3,"irr_base_pct":4.7,"asym_ratio":1.5,"scenario_tree":{"terminal_label":"FY2031E","valuation_basis":"sales_multiple","start":{"rev":12869.75,"ev_s":7.1,"basis":"起點營收取FY2026（當年度）共識；EV/S＝目前EV÷FY2026共識營收。終端EV/S同樣用終端年EV÷當年度營收，路徑Y1到Y5對應FY2027到FY2031"},"rev":{"bull":[28000,42000,56000,68000,78000],"base":[25000,34000,43000,50000,55000],"bear":[21000,25000,27000,26000,24000]},"ev_s":{"bull":4.5,"base":3.5,"bear":2.5},"net_debt_y5":{"bull":160000,"base":110000,"bear":80000},"shares_y5":{"bull":700,"base":800,"bear":900},"net_debt_now":46074.0,"shares_now":551.54,"p":{"bull":20,"base":50,"bear":30},"yield_pct":{"dividend":0,"net_buyback":0},"second_stage":null,"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### CRWV_Q1_2026_Earnings_Call_20260507.md
- 2026-05-07｜Nitin Agrawal (CFO)｜guidance：重申全年營收 $12–13B（原話："reaffirming our full year guidance of $12"）
- 2026-05-07｜Nitin Agrawal (CFO)｜guidance：重申全年調整後營業利益 $0.9–1.1B（原話："$900 million to $1.1 billion of adjusted operating income"）
- 2026-05-07｜Nitin Agrawal (CFO)｜guidance：Q2 營收指引 $2.45–2.6B（原話："revenue in the range of $2.45 billion to $2.6 billion"）
- 2026-05-07｜Nitin Agrawal (CFO)｜guidance：Q2 調整後營業利益 $30–90M，利潤率自 Q1 低點回升（原話："of $30 million to $90 million as margins start to expand"）
- 2026-05-07｜Nitin Agrawal (CFO)｜guidance：Q2 利息費用指引 $650–730M（原話："in the range of $650 million to $730 million"）
- 2026-05-07｜Nitin Agrawal (CFO)｜guidance：全年 CapEx 指引 $31–35B（原話："we now expect CapEx of $31 billion to $35 billion"）
- 2026-05-07｜Nitin Agrawal (CFO)｜guidance：CapEx 下緣上調歸因於零組件價格上漲（原話："increases in component pricing"）
- 2026-05-07｜Nitin Agrawal (CFO)｜guidance：2026 年底年化營收 run-rate 預期 $18–19B，下緣上調 $1B（原話："$18 billion to $19 billion of annualized run rate revenue"）
- 2026-05-07｜Nitin Agrawal (CFO)｜guidance：2027 年底 run-rate 逾 $30B，其中逾 75% 已簽約（不含未行使續約）（原話："more than 75% of which is already contracted,"）
- 2026-05-07｜Nitin Agrawal (CFO)｜margin：管理層稱利潤率壓力屬時間性而非經濟性（原話："This margin dynamic is timing based, not economic."）
- 2026-05-07｜Nitin Agrawal (CFO)｜margin：新部署成熟後貢獻利潤率約落在 20% 中段（原話："contribution margins normalizing in the mid-20s"）
- 2026-05-07｜Nitin Agrawal (CFO)｜margin：Q4 調整後營業利益率回到低雙位數（原話："returning to low double digits by Q4."）
- 2026-05-07｜Nitin Agrawal (CFO)｜margin：Q1 調整後營業利益率 1%，管理層稱為低點（原話："Our Q1 adjusted operating margin was 1%"）
- 2026-05-07｜Nitin Agrawal (CFO)｜margin：Q1 調整後 EBITDA 利益率 56%（原話："Our adjusted EBITDA margin was 56%."）
- 2026-05-07｜Michael Intrator (CEO)｜margin：毛利率受相對於既有裝機量的新增規模影響，管理層稱已近逃逸速度（原話："when I say that they're achieving escape velocity"）
- 2026-05-07｜Nitin Agrawal (CFO)｜margin：收入於交付客戶後按合約期直線認列（原話："we start recognizing revenue on a straight-line basis"）
- 2026-05-07｜Michael Intrator (CEO)｜margin：零組件與電力成本於簽約時以轉嫁方式處理（原話："it is effectively passed through"）
- 2026-05-07｜Michael Intrator (CEO)｜margin：管理層稱大致不受部分零組件通膨影響（原話："we are insulated from the price inflation on some of the"）
- 2026-05-07｜Nitin Agrawal (CFO)｜customer：積壓訂單 $99.4B（原話："Revenue backlog for the quarter ended at $99.4 billion"）
- 2026-05-07｜Nitin Agrawal (CFO)｜customer：積壓訂單認列時程：24 個月內 36%（原話："expected to be recognized in the next 24 months"）
- 2026-05-07｜Nitin Agrawal (CFO)｜customer：非投資等級 AI 原生與基礎模型實驗室占積壓訂單比重（原話："foundation labs now represents less than 30% of our"）
- 2026-05-07｜Nitin Agrawal (CFO)｜customer：新增容量加權平均合約年限約 5 年（原話："new capacity remaining at approximately 5 years"）
- 2026-05-07｜Michael Intrator (CEO)｜customer：Q1 新增 Anthropic 為客戶（原話："we added Anthropic as a"）
- 2026-05-07｜Michael Intrator (CEO)｜customer：Meta 簽訂多筆新單，含 $21B 協議（原話："the $21 billion agreement announced in early April"）
- 2026-05-07｜Michael Intrator (CEO)｜customer：金融服務垂直領域積壓訂單近 $100 億（原話："approaching $10 billion in our revenue backlog"）
- 2026-05-07｜Michael Intrator (CEO)｜customer：10 家客戶承諾至少 $1B 支出（原話："10 customers committed to spending at"）
- 2026-05-07｜Michael Intrator (CEO)｜customer：A100/H100/H200/L40s 平均價格季增（原話："all increased quarter-over-quarter"）
- 2026-05-07｜Nitin Agrawal (CFO)｜customer：2026 年容量大致售罄（原話："we remain largely sold out of our 2026 capacity"）
- 2026-05-07｜Michael Intrator (CEO)｜customer：管理層估算推論占算力已大幅逾 50%（原話："materially in excess of 50% of our compute is"）
- 2026-05-07｜Michael Intrator (CEO)｜customer：H100 售罄（原話："We are sold out in our H100s."）
- 2026-05-07｜Michael Intrator (CEO)｜customer：管理層以「配置」描述客戶分配（原話："I think the word allocate is probably accurate."）
- 2026-05-07｜Michael Intrator (CEO)｜product：推出 Flex Reservation 與 Spot 定價（原話："Both offerings were immediately oversubscribed."）
- 2026-05-07｜Michael Intrator (CEO)｜product：開始提供 CoreWeave Omni（客戶自有資料中心部署）（原話："we are beginning to offer CoreWeave Omni"）
- 2026-05-07｜Michael Intrator (CEO)｜product：軟體、CPU、網路業務年底各預期逾 $100M ARR（原話："$100 million of ARR by the end of the year."）
- 2026-05-07｜Michael Intrator (CEO)｜product：NVIDIA 將 CoreWeave 軟體方案列為參考架構（原話："software solution as a reference architecture for them"）
- 2026-05-07｜Michael Intrator (CEO)｜commitment：2026 年底活躍電力目標逾 1.7GW（原話："our target of more than 1.7 gigawatts by the end of 2026"）
- 2026-05-07｜Michael Intrator (CEO)｜commitment：2030 年活躍電力目標逾 8GW（原話："reaching more than 8 gigawatts of active power by 2030"）
- 2026-05-07｜Michael Intrator (CEO)｜commitment：首個自建站點預計今年稍晚上線（原話："We expect our first self-build site to come"）
- 2026-05-07｜Nitin Agrawal (CFO)｜commitment：承諾下半年調整後營業利益成長快於營收（原話："accelerate faster than revenue growth"）
- 2026-05-07｜Michael Intrator (CEO)｜commitment：2026 大部分零組件已鎖定（原話："The overwhelming majority of it is locked in already"）
- 2026-05-07｜Michael Intrator (CEO)｜capital_allocation：DDTL 4.0 為首個 HPC 基礎設施投資等級貸款（原話："first ever investment-grade Delayed Draw Term Loan"）
- 2026-05-07｜Michael Intrator (CEO)｜capital_allocation：DDTL 4.0 隱含成本低於 6%（原話："implying a cost of less than 6%"）
- 2026-05-07｜Michael Intrator (CEO)｜capital_allocation：加權平均債務成本 2023–2025 年降約 600 bp（原話："weighted average cost of debt by approximately 600 basis"）
- 2026-05-07｜Nitin Agrawal (CFO)｜capital_allocation：2029 年前無債務到期（自償合約債與 OEM 融資除外）（原話："no debt maturities until 2029"）
- 2026-05-07｜Nitin Agrawal (CFO)｜capital_allocation：Q1 因 NVIDIA 關係擴大募集 $20 億股權（原話："we raised $2 billion of equity"）
- 2026-05-07｜Nitin Agrawal (CFO)｜capital_allocation：Jane Street 策略投資 $10 億（原話："$1 billion strategic investment we received from Jane Street"）
- 2026-05-07｜Nitin Agrawal (CFO)｜capital_allocation：定價第五筆 DDTL，涵蓋 OpenAI 與 Cohere 合約（原話："we priced our fifth DDTL Facility"）
- 2026-05-07｜Michael Intrator (CEO)｜capital_allocation：新增電力全數以長期租賃取得，並加速自建（原話："We added more than 400 megawatts of contracted power in Q1"）
- 2026-05-07｜Michael Intrator (CEO)｜competition：管理層描述在高度競爭市場中的多面向擴張策略（原話："positions CoreWeave to grow in a highly competitive"）
- 2026-05-07｜Michael Intrator (CEO)｜competition：新增 5GW 與 NVIDIA 關係：管理層稱可獨立取得電力（原話："independent of any support from NVIDIA or anyone else"）
- 2026-05-07｜Michael Intrator (CEO)｜risk：管理層承認近 6–9 個月零組件嚴重短缺（原話："an acute shortage of certain components"）
- 2026-05-07｜Michael Intrator (CEO)｜risk：管理層稱限制因素不只電力，還有勞力、記憶體、儲存（原話："limiting factor isn't just power, it's labor, it's memory"）
- 2026-05-07｜Michael Intrator (CEO)｜risk：單一資料中心供應商不超過活躍基礎設施 17%（原話："no single data center provider that delivers more than 17%"）

### CRWV_Goldman_Sachs_Communacopia_Technology_Conference_2026_20260908.md
- 2026-09-08｜CEO｜competition：說明自家雲端從創立起專為 AI 打造，而非改裝舊環境（原話："it's like the minivan versus the F1, right?"）
- 2026-09-08｜CEO｜guidance：管理層重申對算力供需的看法：需求持續壓過供給（原話："wildly overwhelmed by the delivery and demand"）
- 2026-09-08｜CEO｜customer：大型客戶對資源的需求量持續擴大（原話："consumers are demanding ever larger amounts of resources"）
- 2026-09-08｜CEO｜customer：舉 Caterpillar 為企業客戶新進場的例子（原話："a company like Caterpillar comes and starts to use us"）
- 2026-09-08｜CEO｜risk：指出社區對資料中心的反對在增加（原話："increased resistance to data centers going into communities"）
- 2026-09-08｜CEO｜risk：預期選舉前資料中心議題聲量最大（原話："it's going to be a maximum volume"）
- 2026-09-08｜CEO｜capital_allocation：美國以外已簽約電力超過 1 GW，作為分散資料中心組合（原話："over 1 gigawatt of power contracted outside of the U.S."）
- 2026-09-08｜CEO｜margin：說明向下整合資料中心的兩個理由之一是回收毛利，並稱其為較次要者（原話："you can recapture some margin, right?"）
- 2026-09-08｜CEO｜commitment：表示自建資料中心已開始啟動前 2-3 座（原話："starting to see the first 2 or 3 of our self-builds spin up"）
- 2026-09-08｜CEO｜competition：談產業結構：資本密集產業會有擴張與整併期（原話："they will tend towards periods of consolidation"）
- 2026-09-08｜CEO｜risk：回應供需正常化後超大規模客戶是否收回外包（原話："We do not believe that they are going to pull back, right?"）
- 2026-09-08｜CEO｜customer：談合約屆期後客戶去留（原話："some of those contracts may come back to us"）
- 2026-09-08｜CEO｜margin：談規模帶來的經濟效益與毛利（原話："ways of driving economics and driving margin"）
- 2026-09-08｜CEO｜product：產品附加率：75% 客戶使用三項服務（原話："75% of our clients are using 3 different services"）
- 2026-09-08｜CEO｜product：NVIDIA 將其軟體堆疊指定為參考架構（原話："NVIDIA designated our software stack as a reference"）
- 2026-09-08｜CEO｜product：Omni 軟體層可在他人資產負債表上取得槓桿（原話："allows us to get some leverage on other balance sheets"）
- 2026-09-08｜CEO｜capital_allocation：最大融資引擎在 SPV 層級（原話："largest engine of our borrowing is occurring at an SPV"）
- 2026-09-08｜CEO｜capital_allocation：最近一次債務結構由貸方承擔續約風險（原話："now the lenders are taking renewal risk"）
- 2026-09-08｜CEO｜capital_allocation：曾以 A- 信用等級取得借款（原話："we were able to borrow at A- credit"）
- 2026-09-08｜CEO｜commitment：表示產品範圍聚焦 AI 工作流，不跨出此範圍（原話："And then we don't wander too far from it, right?"）
- 2026-09-08｜CEO｜customer：對開源與閉源模型採中立態度（原話："more demand for compute is better for our business"）

### 問答異常語氣（迴避／改口／保留）
- CRWV_Q1_2026_Earnings_Call_20260507.md｜問：Mark Murphy：Q1 營收超預期，為何不把上調帶入全年營收指引｜答法：未直接解釋，改談 2026 年容量售罄、年底 ARR 下緣上調與 2027 ARR 已簽約比例
- CRWV_Q1_2026_Earnings_Call_20260507.md｜問：Brent Thill：上半年與下半年營業利益差距大，下半年獲利憑什麼成立｜答法：重申軌跡與指引符合先前說法、Q1 為低點，未提供上下半年逐項拆解數字
- CRWV_Q1_2026_Earnings_Call_20260507.md｜問：Nehal Chokshi：每季可新增多少電力｜答法：明言無法給出每季兆瓦數，改述管線龐大與過去 12 個月合計 2GW
- CRWV_Goldman_Sachs_Communacopia_Technology_Conference_2026_20260908.md｜問：供需正常化後，超大規模客戶收回外包的看空論點，長期如何看待｜答法：CEO 先自稱前一題答案是最政治正確的答案，未提供正常化後的數字，改談客戶續約、事業規模與自有產品需求；稱部分合約可能回來、部分不會

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 4 | 4 |
| customer_second_source | found | 3 | 3 |
| customer_concentration_credit | found | 5 | 3 |
| supply_demand_durability | found | 5 | 4 |
| regulatory_antitrust | found | 3 | 3 |
| reg_tariff_export | found | 4 | 4 |
| geo_supply_chain | found | 4 | 2 |
| end_markets | found | 7 | 4 |
| substitute_technology | found | 3 | 4 |
| channel_business_model_shift | found | 2 | 2 |
| capital_markets_pricing | found | 5 | 3 |
| major_events | found | 3 | 5 |
| unprofitable_nrr_rule40_band | none | 0 | 3 |
| unprofitable_dilution_trajectory | found | 5 | 3 |
| unprofitable_path_to_profitability | found | 5 | 3 |

未涵蓋／不適用軸的查詢詞原文（供判相關性）：
- **unprofitable_nrr_rule40_band**（none）：CoreWeave net revenue retention NRR 2026；CoreWeave Rule of 40 peers comparison 2026；AI cloud neocloud NRR benchmark 2026 Nebius Oracle peers

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260523","verdict":"B 衛星候選：Q1'26 Rev $2.08B +112%/adj EBITDA margin 56%/Backlog $99.4B (+49% QoQ) 但 Q2 指引偏低觸發 -10%；Microsoft 67% 客戶集中度極端 + Debt $25-29B D/E 4.5x；EV/Rev FY27 4.3x 同 tier 略折價；MA 🟠 中段消化（從 peak $187 -42%）；等 $90-95 分批進。","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"CRWV 兌現 FY26 Revenue $12-13B + FY27 $19-20B 共識路徑，並在 FY28 首次達 GAAP 盈利","columns":{"2Y 驗證點":"FY26 Revenue $12.5B mid 兌現","5Y 驗證點":"FY28 GAAP EPS +$2.14 共識兌現","10Y 驗證點":"FY30 Revenue ≥ $45B + GAAP margin > 5%","數字門檻":"FY26 Revenue ≥ $12B 否則 thesis 削弱","來源":"CRWV Q1'26 法說 5/7 + guidance","漂移觸發":"連 2 季 Revenue YoY"}},{"id":"H2","text":"Microsoft 集中度從 67% 逐步降至","columns":{"2Y 驗證點":"FY26 EOY Microsoft 占比","5Y 驗證點":"FY28 Microsoft 占比","10Y 驗證點":"FY30 Microsoft 占比","數字門檻":"2027 全年 Microsoft ≥ 65% → 反轉","來源":"backlog 結構 + 10 個 $1B+ 客戶 ramp","漂移觸發":"連 2 季 Microsoft 比例上升 → 削弱"}},{"id":"H3","text":"Debt $25-29B 對應的 Debt/EBITDA 從 ~3-4x 改善至","columns":{"2Y 驗證點":"FY27 H1 Debt/EBITDA","5Y 驗證點":"FY28 Debt/EBITDA","10Y 驗證點":"FY30 Debt/EBITDA","數字門檻":"FY28 仍 > 3.5x → 反轉","來源":"Bank covenant + Q1'26 balance sheet","漂移觸發":"新 debt 大規模 issue → 削弱"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"Microsoft Maia v2/v3 量產 + Azure AI workload 50%+ 遷移至 in-house","columns":{"對應假設":"H2","時間尺度":"🔥 中期（4-6 季）","監測指標":"Microsoft 季法說 Maia deployment 進度","警戒閾值":"Microsoft Q3-Q4 2026 公開 Maia v2 mass deployment → 警戒；公開 50%+ 遷移計劃 → 反轉"}},{"id":"R2","text":"Debt $25-29B 在利率上行或 customer payment delay 引發流動性 / covenant 危機","columns":{"對應假設":"H1, H3","時間尺度":"🐢 長期（2+ 年）","監測指標":"季度 Debt / EBITDA 比率 + Q1'26 OCF $2.98B 持續性","警戒閾值":"FY27 H1 Debt/EBITDA > 4x → 反轉"}},{"id":"R3","text":"OpenAI 自建 ASIC（與 Broadcom 合作）2027-28 量產，$22.4B 合約縮減","columns":{"對應假設":"H1, H2","時間尺度":"⚡ 短期（1-2 季可觸發）","監測指標":"OpenAI compute supply 公開動態 + Broadcom ASIC 進度","警戒閾值":"OpenAI 公告任何 CRWV 合約縮減 → 即刻削弱"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🟡","ma":"🟠","trap":"🟡","moat_trend":"→","runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":107.58,"archetype":null,"cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"CRWV","date":"2026-10-12","schema":"v15.2","contract":"v19","company_name":"CoreWeave, Inc."},"oneliner":"需求與合約都是真的：積壓訂單1,042億美元，Q2營收年增112%。但淨負債約461億美元，Q3利息費用指引約為調整後營業利益的四倍，股東排在債權人之後。現價大致只反映基準情境，要等利息覆蓋率翻轉。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CRWV_20261012/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CRWV_20261012/scenario.json","answers":{"q1_business":{"verdict":"這門生意收的是AI實驗室與超大規模雲端的算力租金：用約五年期的照付不議長約出租NVIDIA整櫃系統。錢卡在電力與機櫃交付這一環，利潤則先被折舊與利息分走。","reasoning":"收錢方式：客戶簽約五年左右的照付不議合約租用整櫃GPU算力，交付後按合約期直線認列。另有儲存、CPU、網路與軟體（Weights & Biases等）ARR逾4億美元；託管推論的訂約ARR從100萬美元升到逾1億（Q2法說）。最新一季（Q2 2026）營收25.75億美元，年增112%；調整後營業利益1.28億（5.0%），GAAP營業損失0.49億（−1.9%）；TTM毛利率67.4%。積壓訂單1,042億美元，另有Q3初逾250億新承諾尚未計入。活躍電力1.5GW，已簽電力約3.7GW（法說當日為4.2GW）。公司未揭露分部營收。單點依賴：前兩大客戶約占上半年營收40%與23%，加速器幾乎全數來自NVIDIA；兩端都是集中度風險，不是護城河證據。產業時鐘判在過熱期，依據有三：新舊世代GPU售罄並調價、零組件短缺、資本支出年增八成且大量靠債務支應；賣方也已預期2027至2028年增速急降。供需持久度：屬週期性偏緊，電力約束可撐到約2028年，GPU本身的供給可逆性高。","fact_refs":["f_kpi0_revenue_gaap","f_kpi1_non_gaap_adjusted_operat","f_kpi2_gaap_operating_income_lo","f_kpi5_guidance_q3_2026","f_kpi6_guidance_fy2026","f_kpi7_revenue_backlog","f_kpi8_active_power_contracted_","f_peer_crwv_gross_margin_pct","f_rev_consensus_fy1_m"],"verdict_values":{"revenue_quality":"合約型、能見度高但高度集中。積壓訂單逾半已開始交付，公司預期年底超過三分之二。收入在交付後按合約期直線認列。前兩大客戶約占上半年營收六成三。","unit_econ_note":"單一合約的經濟是前重後輕：資本支出在前，靠資產層級債務融資，並在合約期內還清該筆債務。管理層稱新簽合約的貢獻利潤率比前幾季高5至10個百分點，成熟後的貢獻利潤率落在20%中段。Q2調整後EBITDA利潤率59%，調整後營業利益率卻只有5%，差額主要是折舊；再扣利息後，股東端是大幅虧損（淨損6.26億美元）。","archetype":{"primary":"未獲利高成長","secondary":"循環/商品","confidence":"中","fingerprint":"重資產算力出租，GAAP虧損，自由現金流深度為負，產能擴張靠債務與增資"},"industry":{"clock_phase":"III","sd_verdict_source":"週期性偏緊，可延續到約2028年。Goldman估計供需在2028年前難以再平衡，電力是綁定約束。但GPU本身的供給已在改善；UBS估計超大規模雲端資本支出增速由2026年的76%降到2027年25%、2028年6%。供給可逆性高，2028年後反轉風險上升。","bargaining":{"up":"上游議價權強：加速器幾乎全數來自NVIDIA這一家供應商，記憶體與零組件漲價需要轉嫁。機殼與電力多由第三方資料中心提供，單一供應商不超過活躍基礎設施的17%（Q1法說）。","down":"下游集中：前兩大客戶約占上半年營收40%與23%。長約與照付不議條款鎖住營收，但大客戶有自建與第二供應商的選項。","geo":"美國以外已簽電力逾1GW（含印尼360MW）。地方禁建令與歐洲關稅威脅，主要影響選址與成本。"},"profit_pool_dir":"利潤池目前集中在NVIDIA，雲端算力這一環的超額報酬靠短缺撐著。短缺緩解後，利潤池有回流上游或流向客戶自建的風險。","tam_table":[{"item":"超大規模雲端前五大2026年資本支出","value":"約7,530億美元（年增83%），2027年約9,220億（KGI，2026-07）"},{"item":"2027年超大規模資本支出情境","value":"Goldman基準約1.1兆、樂觀1.4兆；Morgan Stanley 1.2兆；UBS估增速2027年25%、2028年6%"},{"item":"Neocloud GPU即服務營收（2030）","value":"約2,500億美元，推論占80%（ABI Research）"},{"item":"其他TAM估計","value":"定義不一：AI基礎設施2030年約3,945億（MarketsandMarkets）或約1,239億（Lucintel）；GPU即服務約266億。各家口徑不同，不能直接比較"},{"item":"公司相對位置","value":"FY2026共識營收約128.7億美元，約為ABI 2030年neocloud營收估計的5%；營業利益池占比的五年前與現在對照，事實表未涵蓋"}]}}},"q2_moat":{"verdict":"護城河方向持平（→），等級C。交付速度與融資能力在擴大，但定價權建立在算力短缺上，客製晶片與大客戶自建正從另一端侵蝕。","reasoning":"機制：大規模、快速把NVIDIA新世代整櫃系統上線的能力，加上配套的資產層級融資與軟體層（Mission Control、Weights & Biases）。可證方向改用規模與利潤率對照，因為同業ROIC與投入資本事實表未涵蓋。Q2營收約25.8億美元，Nebius約5.8億、IREN約1.4億；單季新增近500MW活躍電力。TTM毛利率：CRWV 67.4%、NBIS 74.3%、IREN 62.3%、ORCL 64.0%；營業利益率：CRWV −3.0%，NBIS −50.5%，IREN −53.6%，ORCL 34.2%。執行面在擴大：首家驗證Vera Rubin NVL72，ClusterMAX評為Platinum。定價面目前偏強：公開牌價H100每GPU時6.16美元，比Nebius高約六成；管理層稱舊世代以原價約95%續約，A100新約延到2029年。但這份定價權來自短缺，客製加速器擴張後可能鬆動。兩者相抵，方向判持平。當期ROIC為負：稅後營業利益率為負，周轉率事實表未涵蓋。增量報酬不高於零、再投資率超過100%，不靠外部資金的內生成長上界取0。","fact_refs":["f_peer_crwv_gross_margin_pct","f_peer_crwv_operating_margin_pct","f_peer_crwv_fcf_margin_pct","f_peer_nbis_gross_margin_pct","f_peer_nbis_operating_margin_pct","f_peer_orcl_operating_margin_pct","f_peer_iren_operating_margin_pct","f_kpi3_free_cash_flow_679_capex","f_kpi8_active_power_contracted_"],"verdict_values":{"moat":{"mechanism":"規模化交付速度（電力、液冷、整櫃上線）加上資產層級融資能力與AI軟體層，讓客戶以較低總持有成本取得最新世代算力","execution":8,"pricing":6,"grade":"C","trend":"→","trend_evidence":"執行力擴大（Q2新增近500MW，首家上線Vera Rubin），定價力目前偏強但靠短缺支撐；客製加速器與超大規模自建在侵蝕可服務市場，兩者相抵","competitor_notes":[{"name":"NBIS","strategy_note":"毛利率74.3%高於CRWV，但營業利益率−50.5%，規模約為CRWV四分之一；用低價搶量，是市場的價格錨。"},{"name":"ORCL","strategy_note":"對照組裡唯一獲利者（營業利益率34.2%），但同樣在重資產擴張，自由現金流利潤率−40%；有既有雲端與資料庫事業可以補貼。"},{"name":"IREN","strategy_note":"由礦場轉型，強項是電力取得，已拿下Microsoft 97億美元合約；營業利益率−53.6%，仍在燒錢擴張期。"}],"peer_na_reason":"同業ROIC與投入資本事實表未涵蓋，改用營收規模與利潤率對照","threats":[{"level":"🔴","text":"客製加速器與超大規模自建：Google TPU、AWS Trainium3、Meta MTIA都在擴張，Broadcom稱2027年AI晶片營收能見度逾1,000億美元；OpenAI與Broadcom的10GW自研加速器自2026下半年起部署在其自家資料中心。這直接打到以NVIDIA整櫃為唯一產品的出租模式。","p":"35%","evidence_refs":["substitute_technology#0","substitute_technology#1","customer_second_source#2"]},{"level":"🟡","text":"Neocloud價格競爭：Nebius H100按需牌價約低四成，IREN拿下Microsoft合約。小型業者受融資約束可能出清，對公司是雙面影響。","p":"50%","evidence_refs":["end_markets#4"]},{"level":"🟡","text":"GPU經濟壽命可能短於六年折舊年限：若舊世代續約價大幅下滑，折舊與資產殘值都要重估。","p":"30%","evidence_refs":["substitute_technology#2","supply_demand_durability#3"]}],"roic_durability":{"quadrant":"低利益率×低周轉","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者（模型研究員、推論服務）、決策者（實驗室與雲端的基礎設施主管）和付款者（同一法人）三者一致，需求以照付不議長約落地，積壓訂單1,042億美元。問題在付款能力：主要非超大規模客戶OpenAI沒有信用評等，採購承諾約6,650億美元，單季燒現金約37億美元。急迫性高，不代表持久。"},{"item":"決策層級","level":"🟡","text":"替代性要在單一叢集合約的層級衡量。五年期合約、違約條款與SPV債務綁在一起，合約期內轉換成本高；到期時客戶可以自建、改用客製晶片或轉向其他neocloud。在Goldman會議上被問到供需正常化後超大規模客戶是否收回外包，CEO沒有給數字。"},{"item":"價值鏈分配","level":"🔴","text":"價值鏈中最難取代的是NVIDIA（加速器唯一來源）與電網接入。公司TTM毛利率67.4%看似不低，但營業利益率−3.0%，Q2調整後營業利益率只有5%；大部分價值在折舊（付給NVIDIA與零組件商）與利息（付給債權人）階段就被分走了。"},{"item":"社會容忍度","level":"🟡","text":"地方資料中心禁建令增加，紐約州暫停50MW以上新資料中心部分環評核准，最長一年。CEO預期選舉前聲量最大，並稱禁建只會改變建在哪裡，不會減少需求。公司自付電網升級費用以降低政治阻力，等於付了一筆保費。"}],"roiic":"≤0（TTM GAAP營業利益率−3.04%；投入資本口徑事實表未涵蓋，無法算出精確值）","reinvest_rate":">100%（Q2營運現金流6.79億美元對資本支出64.22億；FY2025營運現金流約31億對資本支出約103億）","endo_ceiling":0,"formula_note":"內生成長＝增量報酬×再投資率。增量營業報酬不高於零，所以不靠外部資金的內生成長上界取0，實際成長全部來自債務、客戶預付與增資。當期ROIC＝稅後營業利益率（為負）×投入資本周轉率（事實表未涵蓋），結果為負。"}}}},"q3_growth":{"verdict":"後五年跑道中等（🟡）：2030年8GW目標有電力合約撐腰，但成長幾乎全靠外部資金，第二條曲線（託管推論與軟體）仍然很小。","reasoning":"成長來源以量為主（活躍電力由1.5GW到年底逾1.85GW，已簽4.2GW，另有約1.5GW土地與意向書選項），價格其次（Blackwell與Vera Rubin定價創新高，CFO稱7月跨SKU調價約25%），再加上產品組合轉向推論與軟體。沒有併購驅動，也沒有回購。共識營收FY2026約128.7億美元、FY2027約263億（年增約104%）。共識EPS由FY2025實際−2.81到FY2028E 1.25，基期為負，三年CAGR無法計算；近三個月FY2026共識EPS從−3.66下修到−3.94。內生上界取0（見護城河段），所以共識成長與內生上界的缺口全部來自外部融資與預期中的利潤率擴張，不能歸因於回購或收購，信心上限為中。跑道：滲透率事實表未涵蓋；以年底年化營收185至195億、對應1.85GW推算，每GW約年營收100億，走到8GW約需5年。2030年後的關鍵是2024至2026年所簽合約的續約價。第二曲線有來源但很小：託管推論目標年底ARR至少2.5億美元，軟體與其他服務ARR逾4億，合計不到年化營收的3%。","fact_refs":["f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_3m_fy1_pct","f_kpi6_guidance_fy2026","f_kpi8_active_power_contracted_"],"verdict_values":{"growth":{"driver_mix":"量（GW產能）為主，價（合約價上調）其次，加上產品組合轉向推論與軟體；無併購、無回購","runway_years":"約5（以2030年8GW目標換算；滲透率事實表未涵蓋）","runway_post_y5":"🟡","endo_ceiling_basis":"引護城河段：增量報酬不高於零、再投資率超過100%，內生上界取0。共識FY2027營收年增約104%全部超出上界，屬外部融資驅動。","segments":{"expanded":false,"reason":"公司未揭露分部營收。GPU以外的儲存、CPU、網路與軟體ARR逾4億美元，託管推論訂約ARR逾1億，合計不到年底年化營收（185至195億）的3%，目前還不決定利潤；託管推論ARR超過10億時再展開"},"decay_signals":["毛利率下滑：FY2024 74.3%、FY2025 71.7%、TTM 67.4%（年度與TTM口徑；季度年對年連續資料事實表未涵蓋）","替代技術壓縮可服務市場：客製加速器擴張，OpenAI自研10GW","未亮：SBC占營收Q2為6.4%，高於5%，但FY2025約12%降到2026年約6%，並非逐年上升"]}}},"q4_capital":{"verdict":"資本配置偏弱：沒有回購也沒有股息，股數持續稀釋，資本支出靠債務與增資支應；計分卡三項沒有一項通過。","reasoning":"淨利為負，自由現金流對淨利的轉換率沒有意義。Q2自由現金流−57.4億美元（營運現金流6.79億減購置固定資產64.22億；法說口徑的總資本支出為94億）。SBC 1.65億，占營收6.4%。現金去向四分：資本支出壓倒性為主；收購次之（2025年Weights & Biases約10.29億，另有OpenPipe、Monolith、Marimo）；回購為零；股息為零。融資面：Q2透過債務、可轉債與股權募集約180億美元，累計取得逾320億；加權債務成本一年降近300個基點（約每年省11億利息）；Q1法說稱2029年前沒有到期債務（自償合約債與OEM融資除外）。稀釋：稀釋加權股數2024年4.044億股到2025年4.36億股，年增7.8%。營運槓桿為負：Q2營收年增112%，調整後營業利益卻年減36%（2.00億到1.28億），差距遠大於3個百分點，主因是新產能的爬坡成本，列入成長熄火觀察。2025年曾提出約90億美元全股票收購Core Scientific，後被對方股東否決，顯示管理層願意用股票做大額交易。","fact_refs":["f_kpi3_free_cash_flow_679_capex","f_kpi4_sbc","f_net_debt_m","f_shares_diluted_m"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":true,"passed":null,"input":"Weights & Biases約10.29億美元（2025-05完成）等軟體收購，已實現增量報酬事實表未涵蓋"},{"name":"buyback_yield","applicable":false,"passed":null,"input":"無回購，反而持續發行股權與可轉債"},{"name":"sbc_dilution","applicable":true,"passed":false,"input":"稀釋加權股數2025年增7.8%（4.044億到4.36億股），遠高於每年1.5%"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長來自自有產能擴建，不靠併購撐；無股息、無回購，股東報酬為負（淨發行）"}}}},"q5_valuation":{"verdict":"現價要求公司在2031年做到約550億美元營收、終端EV/S約3.5倍，淨負債壓在約1,100億以內，股東才拿得到約年化5%。這就是基準情境本身，沒有安全邊際。我信營收會到，不信股東能分到夠多。","reasoning":"EV約913億美元，由市值約453億加淨負債約461億組成。EV/S的TTM口徑為12.0倍，對FY2026共識營收為7.1倍，對FY2027共識營收約3.5倍（913÷263）。股權只占EV約一半，所以EV每變動10%，股價約變動20%。基準情境：2031年營收550億、EV/S 3.5倍，扣淨負債1,100億，除以8億股，約103美元，比現價82.08美元高26%，年化約4.7%。機率加權約106美元，年化約5%。賣方31家平均目標價140美元（9月初快照），隱含的是接近樂觀情境的假設。PEG不適用：三年EPS基期為負。同業倍數事實表未涵蓋；終端倍數改以自身調整後EBITDA利潤率約58%換算EV/EBITDA約6倍來校準，對照重資產租賃業的常見區間。不主張市場看錯。","fact_refs":["f_price_at_dd","f_ev_m","f_net_debt_m","f_shares_diluted_m","f_ev_s_current","f_ev_s_fwd","f_ev_s_percentile","f_ps_current","f_rev_consensus_fy2_m"],"verdict_values":{"valuation":{"basis":"EV/S（前瞻，EV÷FY2026共識營收），終端扣除淨負債","tier":"未獲利重資產算力租賃","peers":{"expanded":false,"reason":"事實表同業對照只有利潤率，沒有同業EV/S或EV/毛利現值，無法做同類倍數錨；終端倍數改以自身EBITDA利潤率換算EV/EBITDA約6倍校準"},"fwd_pe":null,"peg":null,"percentile_5y":null,"val_light":"🟠","val_light_derivation":"基準情境5年終端價約103美元，對現價82.08美元年化約4.7%，機率加權年化約5%，都低於8%的弱門檻。EV對FY2027營收約3.5倍看似不貴，但股權只占EV一半，淨負債會隨資本支出擴張，倍數便宜不等於股權便宜。TTM EV/S落在上市以來四個年度端點的最低點，但上市未滿兩年，沒有五年分位。","upside_short_pct":-11,"upside_mid_pct":26,"denominator_disputed":false,"denominator_note":"營收口徑沒有一次性項目；真正的爭點在分子端的淨負債路徑，不在分母。一年期推估：FY2027基準營收250億×5.0倍（成長放緩後當年度EV/S由7.1倍收斂）＝1,250億，扣淨負債約810億（資本支出續燒的粗估），除以約6億股，約73美元"}}},"q6_how_wrong":{"verdict":"最可能看錯的地方，是把合約能見度當成股東報酬能見度：營收大概率兌現，但利息、折舊與稀釋可能讓股權長期分不到剩餘價值。反方向的錯，是低估舊世代GPU續約帶來的現金流。","reasoning":"股價自2026年高點約187美元（前份摘要）跌到現價，回撤約56%；26週報酬−19.5%，RSI 43.7。股權只占EV約一半，回撤會被槓桿放大。已知事件：2025年11月因第三方資料中心延遲下修指引，引來證券集體訴訟（目前是指控，尚未裁決）。管理層在幾個關鍵問題上迴避：拒絕拆解上下半年營業利益、拒絕給每季新增兆瓦數、被問到供需正常化後的情境時沒有給數字。衰退信號亮2項，陷阱風險中等，依據見反證紀錄。","fact_refs":["f_price_at_dd","f_week26_return_pct","f_rsi14","f_net_debt_m","f_ev_m"],"verdict_values":{"trap":{"verdict":"🟡","label":"槓桿型成長：營收真實，股東剩餘價值存疑"}}}},"scenario_inputs":{"valuation_basis":"sales_multiple","terminal_label":"FY2031E","start":{"rev":12869.75,"ev_s":7.1,"basis":"起點營收取FY2026（當年度）共識；EV/S＝目前EV÷FY2026共識營收。終端EV/S同樣用終端年EV÷當年度營收，路徑Y1到Y5對應FY2027到FY2031"},"rev":{"bull":[28000,42000,56000,68000,78000],"base":[25000,34000,43000,50000,55000],"bear":[21000,25000,27000,26000,24000]},"ev_s":{"bull":4.5,"base":3.5,"bear":2.5},"net_debt_y5":{"bull":160000,"base":110000,"bear":80000},"shares_y5":{"bull":700,"base":800,"bear":900},"p":{"bull":20,"base":50,"bear":30},"yield_pct":{"dividend":0,"net_buyback":0},"max_dd":{"lo":-100,"hi":-55,"basis":"股價已從2026年高點約187美元跌到82.08美元，實際回撤約56%。股權只占EV約一半，EV每跌25%股價約跌50%，所以一般修正的較淺端取−55%。空頭情境終端淨負債約800億美元，大於終端EV約600億，股權歸零，較深端取−100%。屬深回撤路徑。","trigger_time":null},"basis":{"bull":"短缺延續到2028年後，2030年8GW全數到位且每GW年營收維持約100億；推論與軟體占比提高，終端EV/S 4.5倍（約EV/EBITDA 8倍）。產能擴張更大，淨負債升到約1,600億，但增資價格較高，股數約7億","base":"FY2027約250億（略低於共識263億），2031年約550億、約6GW；續約價溫和下滑，終端EV/S 3.5倍（約EV/EBITDA 6倍）。累計自由現金流約−750億，部分以增資補足，淨負債約1,100億，股數約8億","bear":"2028年起超大規模資本支出增速趨近零，客製晶片擴大、舊世代續約價崩落；營收在約270億見頂後下滑到240億。已承諾的2027年資本支出把淨負債推上高點，之後僅能小幅償還（約800億），並折價增資到約9億股；終端EV/S 2.5倍，股權歸零"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"UBS估超大規模資本支出增速2027年25%、2028年6%；GPU供給改善，稀缺轉向電網；客製加速器在擴張；研究機構認為不少小型neocloud撐不過融資與規模門檻。","assumption":"需求在2028年前不降溫，舊世代續約價不崩","consequence":"2028年後新約與續約價格下跌，營收停在260億至300億附近，終端EV/S壓到2.5倍，淨負債約800億美元時股權歸零","ruling":"採納：這是空頭情境的主體，配30%機率，終端價歸零","watch":"超大規模雲端2027年資本支出指引、Hopper續約價、每季新簽承諾金額","evidence_refs":["supply_demand_durability#3","substitute_technology#0","substitute_technology#1","end_markets#4"],"fact_refs":["f_net_debt_m"]},{"view":"論點成功但股東經濟變差","evidence":"Q2利息6.4億美元對調整後營業利益1.28億；Q3利息指引8.6億至9.4億，對調整後營業利益2億至2.6億。稀釋股數2025年增7.8%，SBC每季約1.4億至1.65億。曾提出約90億美元全股票收購Core Scientific，被對方股東否決。全年資本支出上調後，公司表示可能需要額外債務或股權融資。","assumption":"營收照管理層路徑在2030年走到8GW","consequence":"營收翻四倍，但淨負債同步擴張到約1,100億、股數增到約8億，每股價值成長被吃掉；基準情境5年年化只有約5%","ruling":"採納：這是本輪下調評級的主因","watch":"調整後營業利益÷利息費用、淨負債÷年化調整後EBITDA、每季股數","evidence_refs":["unprofitable_path_to_profitability#2","unprofitable_path_to_profitability#4","unprofitable_dilution_trajectory#0","unprofitable_dilution_trajectory#1","major_events#0","ma_merger#0","capital_markets_pricing#2"],"fact_refs":["f_net_debt_m","f_kpi4_sbc","f_shares_diluted_m"]},{"view":"價格已反映太多","evidence":"EV約913億美元，已是FY2026共識營收的7.1倍；基準情境終端價約103美元，只比現價高26%。賣方平均目標價140美元，隱含的是接近樂觀情境的假設。","assumption":"市場用賣方目標價看待這檔股票","consequence":"想拿到樂觀情境的報酬，必須押注2030年8GW全部到位，而且終端倍數維持4.5倍以上；任何一項落空，報酬就退回基準或更差","ruling":"部分採納：現價不是泡沫，但只付得起基準情境。股價下跌不是安全邊際，因為股權只占EV一半","watch":"利息覆蓋率與淨負債路徑、賣方目標價的下修幅度","evidence_refs":[],"fact_refs":["f_ev_s_fwd","f_ev_m","f_price_at_dd","f_week26_return_pct"]},{"view":"論點失敗","evidence":"管理層在關鍵問題上迴避：Q1法說拒絕拆解上下半年營業利益、拒絕給每季新增兆瓦數；Goldman會議上被問到供需正常化後大客戶收回外包，CEO先說自己前一題答得最政治正確，之後沒有給數字。","assumption":"正常化之後大客戶仍然續約","consequence":"若正常化後大客戶收回外包，2029至2031年到期合約的續約量與價格同時下滑","ruling":"部分採納：Q2實績已兌現上半年承諾，迴避本身不算證據；但正常化情境的數字缺口，正是空頭機率不下調的理由","watch":"2027年起每季揭露的續約量與續約價","evidence_refs":[],"fact_refs":[]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 🟠 → 本次 -","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=🟠","side_b":"本次 ma=-","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 107.58 → 本次 82.08（-23.7%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=107.58","side_b":"本次 price_at_dd=82.08","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 107.58 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 107.58 美元：五年期望值 前份未列，基準年化 前份未列，前份未列不對稱比","side_b":"本次情境、股價仍用 107.58 美元：Bull 價 272.86、Bear 價 0，五年期望值 −1.3%，基準年化 −0.8%，不對稱比 1.02","ruling":"先換情境、股價不動：五年期望值與基準年化前份未列，無法比較。前份未列不對稱比，本次為 1.02。Bull、Bear 價位與股價無關，只受情境影響。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 107.58 美元：五年期望值 −1.3%，基準年化 −0.8%，不對稱比 1.02","side_b":"本次情境、股價 82.08 美元：五年期望值 +29.3%，基準年化 4.7%，不對稱比 1.55","ruling":"再換股價、情境不動：起點價下跌 23.7%，五年期望值多 30.6 個百分點，基準年化多 5.5 個百分點，不對稱比由 1.02 升到 1.55。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"一致判斷：管理層承諾兌現度","cause":null,"prior_field":null,"side_a":"Q1法說（2026-05-07，CFO）：Q2營收24.5億至26億、調整後營業利益0.3億至0.9億、利息6.5億至7.3億；2026年底活躍電力逾1.7GW","side_b":"Q2實際（2026-08-11）：營收25.75億、調整後營業利益1.28億、利息6.4億；年底電力指引上調到逾1.85GW，全年營收指引上調到124億至132億","ruling":"一致：上半年承諾全數兌現或超越，執行面不是爭點","evidence_level":"一手（法說會逐字稿、公司新聞稿）","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"矛盾：資本支出一再上調，營收指引只小幅上調","cause":null,"prior_field":null,"side_a":"Q1法說：全年資本支出310億至350億，下緣因零組件漲價上調","side_b":"Q2法說：全年資本支出上調到350億至390億，中點增加40億；全年營收中點只增加約3億","ruling":"可調和（程度差異）：新增資本支出主要用在2027年交付與新簽大單，Q3初逾250億新承諾可以解釋。但全年資本支出約為年底年化營收的兩倍，股東要等到合約後段才看得到現金。以2027年營收能否跟上為準","evidence_level":"一手","settle_metric":"FY2027營收對240億門檻；2027年資本支出指引","if_then":["若2027年資本支出指引再上調而調整後營業利益率沒有擴張，維持不建倉，空頭機率上調到35%","反向：若2027上半年調整後營業利益÷利息費用連兩季≥60%，重跑判斷並允許小額首倉"],"evidence_refs":["capital_markets_pricing#2","unprofitable_path_to_profitability#1"]},{"axis":"矛盾：利潤率擴張與利息擴張","cause":null,"prior_field":null,"side_a":"管理層：利潤率壓力是時間性而非經濟性（Q1法說，CFO）；新約貢獻利潤率高5至10個百分點，Q4調整後營業利益率可達十位數低段；加權債務成本一年降近300個基點","side_b":"Q2利息6.4億是調整後營業利益1.28億的5倍。Q3指引中點利息9億對調整後營業利益2.3億，比值約26%；Q2到Q3利息增加約2.6億，營業利益只增加約1億","ruling":"可調和（時間差），但數據出來前偏向空方：管理層談的是合約層級的報酬，股權層級要等利潤率增量追上利息增量才成立。執行上不建倉，等比值翻轉","evidence_level":"一手指引數字","settle_metric":"季度調整後營業利益÷利息費用（Q2 2026為20%）","if_then":["若2027上半年連兩季比值≥60%，且全年資本支出未再上調，重跑判斷，允許小額首倉","若2027下半年比值仍<40%，持有者清倉，未持有者停止追蹤","反向：若2026年第四季比值就超過50%，提前重跑判斷"],"evidence_refs":["unprofitable_path_to_profitability#2","unprofitable_path_to_profitability#4"]},{"axis":"矛盾：7月調價約25%與公開牌價未變","cause":null,"prior_field":null,"side_a":"CFO（Q2法說2026-08-11）：7月跨SKU調價約25%，營業利益率的改善還發生在調價之前","side_b":"第三方牌價追蹤：公開按需牌價7月到8月未變，H100每GPU時6.16美元","ruling":"可調和：調價可能落在合約價與新簽約上，不會反映在公開按需牌價；第三方來源是競品部落格。不作為評級依據，以Q3、Q4的每兆瓦營收驗證","evidence_level":"一手對二手","settle_metric":"季度營收÷平均活躍電力","if_then":["若Q4 2026的季營收÷平均活躍電力沒有比Q2提高，視為調價未落地，空頭機率維持30%、不下調"],"evidence_refs":["end_markets#5"]},{"axis":"產業態勢：競爭、結構與其他變數","cause":null,"prior_field":null,"side_a":"結構轉好：電力是綁定約束，Goldman估供需在2028年前難以再平衡，新電網核准要24至36個月；公司已簽電力4.2GW","side_b":"競爭與替代惡化：Nebius牌價低約四成，IREN拿下Microsoft合約，客製加速器在擴張。其他結構變數：地方禁建令擴散，AI法規跨轄區衝突","ruling":"雙向拉鋸：電力稀缺短期內保護既有產能的定價，但客製晶片與自建會在2028年後侵蝕可服務市場。小型業者出清對公司份額有利，同時也提醒融資市場對整個族群的耐心有限","evidence_level":"多為二手預測","settle_metric":"2027年超大規模資本支出實際增速；公司新簽約價","if_then":["若2027年超大規模資本支出增速低於15%，空頭機率上調到35%，維持不建倉"],"evidence_refs":["end_markets#4","supply_demand_durability#3","regulatory_antitrust#1"]},{"axis":"方法：未獲利成長股的現金流門檻","cause":null,"prior_field":null,"side_a":"營收成長加自由現金流利潤率：112%加約−180%，遠低於20，且連兩季成立，照這把尺應直接拒絕","side_b":"重資產長約租賃的自由現金流反映的是產能預建，資本支出對應已簽的照付不議合約；現金跑道由已取得的逾320億美元融資支應（Q2法說），這把尺對這類業務失真","ruling":"不直接拒絕，改給弱評級，並把融資取得失敗列為清倉條件。若這把尺證實為對，判斷依據是：2027年6月前，新一輪資產層級融資的成本明顯高於現行，或出現大額折價增資","evidence_level":"一手","settle_metric":"新債成本相對現行加權成本、單次增資規模","if_then":["若2027年6月前新債成本比現行加權成本高200個基點以上，或單次增資超過流通股10%，清倉並停止追蹤"],"evidence_refs":["unprofitable_path_to_profitability#3"]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"積壓訂單1,042億，加上Q3初逾250億新承諾；舊世代以原價約95%續約，A100新約延到2029年；新約貢獻利潤率高5至10個百分點；債務成本一年降近300個基點；股價自高點跌逾一半，EV對FY2027營收約3.5倍","side_b":"以上全是合約層級的好消息；股權層級看，淨負債約461億且隨資本支出擴大，利息增量大於營業利益增量","ruling":"不採納為進場理由，但列入重新評估條件：只要利息覆蓋率翻轉，這些好消息就會直接流到股東","evidence_level":"一手","settle_metric":"季度調整後營業利益÷利息費用","if_then":["若Q4 2026調整後營業利益率≥13%，且利息費用季增不超過10%，提前重跑判斷"],"evidence_refs":[]},{"axis":"客戶集中度的兩種讀法","cause":null,"prior_field":null,"side_a":"10-Q（Q1 2026）：前兩大客戶約占營收65%；Q2 10-Q預期集中度會因長約而持續","side_b":"第三方分析：最大客戶占比由Q1的45%降到Q2的36%；前兩大約占上半年營收40%與23%","ruling":"可調和：最大客戶占比確實在下降（去年同期為72%），但前兩大合計仍約六成。前份「Microsoft占比逐步下降」的方向成立，程度還不夠","evidence_level":"一手對第三方","settle_metric":"10-Q前兩大客戶合計占比","if_then":["若2027年全年前兩大合計占比≥65%，客戶風險升為主要風險，空頭機率上調到35%"],"evidence_refs":["customer_concentration_credit#2","customer_second_source#0"]},{"axis":"前份漂移：評級、陷阱風險、護城河方向","cause":"新證據","prior_field":["signal","trap","moat_trend"],"side_a":"前份（2026-05-23）：評級B、陷阱風險🟡、護城河→","side_b":"本次：評級C、陷阱風險🟡、護城河→","ruling":"評級下調來自新證據：Q2財報後全年資本支出再上調40億，Q3利息指引8.6億至9.4億約為調整後營業利益的四倍，淨負債約461億。陷阱風險維持，衰退信號仍為2項。護城河方向維持，交付優勢擴大與客製晶片侵蝕相抵","evidence_level":"一手","settle_metric":"季度調整後營業利益÷利息費用","if_then":[],"evidence_refs":["capital_markets_pricing#2","unprofitable_path_to_profitability#2"]},{"axis":"前份漂移：估值結論與情境方法","cause":"方法變動","prior_field":["val","runway_post_y5","archetype","cycle_position","p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份：估值🟡（以FY2027 EV/營收4.3倍、同類略折價判斷）；成長跑道、公司類型、循環位置、情境機率與最大回撤都未填","side_b":"本次：估值🟠（營收路徑×終端EV/S，並扣除終端淨負債）；成長跑道🟡；公司類型為未獲利高成長；非循環股，不判循環位置；機率樂觀20、基準50、空頭30；最大回撤−55%至−100%","ruling":"方法變動：前份沒有扣除淨負債路徑。股價雖從107.58美元跌到82.08美元，但淨負債擴張後股權價值降得更多，估值結論反而轉弱。其餘欄位由空白改為有值，同屬方法補齊","evidence_level":"方法","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"前份漂移：假設與風險門檻","cause":"新證據","prior_field":["thesis.H","thesis.R"],"side_a":"前份：H2以Microsoft占比67%逐步下降、2027年全年≥65%為反轉；H3以債務/EBITDA在FY2028>3.5倍為反轉；R1為Microsoft自研晶片，R3為OpenAI自研晶片","side_b":"本次：集中度門檻沿用（前兩大合計2027年≥65%），移到風險項；債務/EBITDA門檻原樣保留在清倉條件；兩項自研晶片風險合併為客製加速器風險，並擴及全部大客戶；新增利息覆蓋與舊世代續約兩條假設","ruling":"新證據：最大客戶占比已由去年72%降到約36%至45%，只盯Microsoft已不是最準確的描述；新財報暴露出來的承重變數是利息與續約價","evidence_level":"一手","settle_metric":null,"if_then":[],"evidence_refs":["customer_concentration_credit#2"]},{"axis":"門檻變動：清倉與減碼條件","cause":"新證據","prior_field":["kill_metrics"],"side_a":"前份沒有設清倉或減碼門檻，只有警戒閾值「FY27 H1 Debt/EBITDA > 4x → 反轉」","side_b":"本次：淨負債÷年化調整後EBITDA在2027上半年>4倍或2028全年>3.5倍則清倉（前份門檻原樣保留，現值約7.7倍）；調整後營業利益÷利息費用在2027下半年<40%則清倉；FY2026營收<124億則減碼；前兩大客戶縮減承諾則清倉","ruling":"新證據：Q2的利息與資本支出指引讓股權報酬取決於覆蓋率，所以把前份的警戒值升格為清倉門檻，並補上覆蓋率與營收的減碼條件。現值依Q2調整後EBITDA 15億年化計算","evidence_level":"一手","settle_metric":"淨負債÷年化調整後EBITDA；調整後營業利益÷利息費用","if_then":[],"evidence_refs":["unprofitable_path_to_profitability#2"]},{"axis":"門檻變動：重新評估條件","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"前份未設重新評估條件（裁決文字為等90至95美元分批進）","side_b":"季度調整後營業利益÷利息費用連兩季≥60%（Q2 2026為20%），且全年資本支出指引未再上調","ruling":"由價格條件改為事件條件：股價已跌破90至95美元區間，但本輪的約束是利息覆蓋率而不是價格，價格再低也取代不了覆蓋率翻轉","evidence_level":"一手","settle_metric":"季度調整後營業利益÷利息費用","if_then":[],"evidence_refs":["unprofitable_path_to_profitability#2"]},{"axis":"Single Thing 變動","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設唯一致命點（Single Thing為空）","side_b":"前兩大客戶任一縮減、延後或違約已簽的算力承諾","ruling":"Single Thing為本次新設：前份沒有填。依對終端股價的敏感度排序，客戶承諾大於任何單一技術或政策事件；一旦發生即清倉","evidence_level":"一手","settle_metric":"8-K重大合約變更、10-Q客戶集中揭露","if_then":[],"evidence_refs":["customer_concentration_credit#4"]}],"triggers":[{"n":1,"text":"Q3 2026財報營收對指引","type":"假設驗證","maps_to":"H1","metric":"Q3 2026營收","threshold":"<34.5億美元（指引下緣）","action":"不追；H1列為削弱，維持不建倉","source_freq":"季報","date":"2026-11","evidence_refs":[]},{"n":2,"text":"利息覆蓋率翻轉（重新評估條件）","type":"估值rearm","maps_to":"H2","metric":"季度調整後營業利益÷利息費用","threshold":"連兩季≥60%，且全年資本支出未再上調（Q2 2026為20%）","action":"重跑判斷；通過後首倉以小額試探倉為上限","source_freq":"季報","date":"2027-05","evidence_refs":["unprofitable_path_to_profitability#2"]},{"n":3,"text":"前兩大客戶縮減或違約","type":"Single Thing","maps_to":"Single Thing","metric":"8-K重大合約變更與10-Q客戶集中揭露","threshold":"任一客戶縮減、延後或違約已簽承諾","action":"清倉","source_freq":"即時（8-K）與季報","date":null,"evidence_refs":["customer_concentration_credit#4","customer_second_source#0"]},{"n":4,"text":"利潤率擴張沒有落地","type":"風險","maps_to":"R2","metric":"Q4 2026調整後營業利益率","threshold":"<10%（管理層承諾為十位數低段）","action":"停止加碼；空頭機率上調到35%","source_freq":"季報","date":"2027-02","evidence_refs":["unprofitable_path_to_profitability#2","capital_markets_pricing#2"]},{"n":5,"text":"交付延遲重演","type":"風險","maps_to":"R4","metric":"全年營收或活躍電力指引","threshold":"任一季因第三方資料中心延遲而下修","action":"減碼","source_freq":"季報","date":null,"evidence_refs":["geo_supply_chain#1","major_events#2"]},{"n":6,"text":"融資條件惡化","type":"清倉","maps_to":"R2","metric":"新債成本與增資規模","threshold":"新債成本比現行加權成本高200個基點以上，或單次增資超過流通股10%","action":"清倉","source_freq":"即時（8-K）","date":null,"evidence_refs":["unprofitable_path_to_profitability#4","unprofitable_dilution_trajectory#0"]},{"n":7,"text":"舊世代GPU續約價","type":"假設驗證","maps_to":"H3","metric":"Hopper與Ampere到期續約價相對原約","threshold":"<80%","action":"減碼","source_freq":"法說會","date":"2027–2029","evidence_refs":["substitute_technology#2"]},{"n":8,"text":"槓桿警戒（前份門檻沿用）","type":"清倉","maps_to":"H2","metric":"淨負債÷年化調整後EBITDA","threshold":"2027上半年>4倍，或2028全年>3.5倍（現值約7.7倍）","action":"清倉","source_freq":"季報","date":"2027-08","evidence_refs":["unprofitable_path_to_profitability#4"]},{"n":9,"text":"財報後複審","type":"複審日期","maps_to":null,"metric":"Q3 2026財報與指引","threshold":"財報公布後","action":"重跑判斷","source_freq":"季報","date":"2026-11","evidence_refs":[]}],"kill_metrics":[{"metric":"淨負債÷年化調整後EBITDA","bear_threshold":"2027上半年>4倍或2028全年>3.5倍（前份門檻沿用，現值約7.7倍）","window":"2027上半年至2028年底","source":"公司季報新聞稿與10-Q","last_status":"warning"},{"metric":"季度調整後營業利益÷利息費用","bear_threshold":"2027下半年仍<40%（Q2 2026為20%）","window":"2027年第3至第4季","source":"公司季報新聞稿","last_status":"warning"},{"metric":"前兩大客戶已簽承諾","bear_threshold":"任一縮減、延後或違約","window":"滾動","source":"10-Q客戶集中揭露與8-K","last_status":"ok"},{"metric":"FY2026營收對指引下緣","bear_threshold":"<124億美元","window":"2027-02財報","source":"公司年報新聞稿","last_status":"ok"},{"metric":"稀釋股數年增率","bear_threshold":">10%","window":"滾動四季","source":"10-Q","last_status":"unknown"},{"metric":"舊世代GPU續約價相對原約","bear_threshold":"<80%","window":"2027至2029年","source":"法說會揭露","last_status":"unknown"}],"evidence_dismissed":[{"ref":"unprofitable_dilution_trajectory#3","reason":"這條證據的前提是Core Scientific全股票併購完成，但同一證據包的重大事件紀錄顯示，該案已在2025-10-30因對方股東否決而終止，所述稀釋不會發生。管理層願意用股票做大額交易的傾向，已另記在股東經濟的反證中"}],"action_conditions":{"rearm_trigger":"季度調整後營業利益÷利息費用連兩季≥60%（Q2 2026為20%），且全年資本支出指引未再上調","exec_line":"未持有者不建倉，也不因價格下跌接刀；重新評估條件達成後重跑判斷，首倉以總資產1%試探為上限。持有者遇到清倉條件即全數出清","holding_cap":"≤2%"}},"decision_inputs":{"signal":"C","ma":"-","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等的是事件不是價格：季度調整後營業利益÷利息費用連兩季≥60%，且全年資本支出未再上調"},"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"6","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='C'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='C'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='-'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":true,"basis":"signal='C'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":true,"basis":"capalloc_grade='C'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='C', runway='🟡', val='🟠', moat_trend='→', week26=-19.53, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='未獲利高成長', cycle_position=None, moat='C', moat_trend='→', cycle_gates_pass=None"},{"row":"6/7/7a-verdict","condition":"Soft Veto 生效 → 觀望（max-severity wins；8a/8b 未能繞過）","hit":true,"basis":"soft_veto_rows=['6']"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":"中期 2-5 年","requires_critic":[]},"thesis":{"H":[{"id":"H1","text":"合約營收如期兌現：FY2026營收落在指引124億至132億美元之內，FY2027達到240億美元以上（管理層稱2027年底年化營收逾300億，其中逾75%已簽約）","2y":"FY2026營收≥124億；FY2027≥240億","5y":null,"10y":null,"threshold":"FY2026營收<124億美元或FY2027<220億美元即削弱","source":"公司季報新聞稿與法說會（Q1 2026-05-07、Q2 2026-08-11）","drift_rule":"以指引中點為基準，連2季偏離≥5%為削弱，連3季≥10%為反轉"},{"id":"H2","text":"利潤率擴張跑贏利息：Q4 2026調整後營業利益率達十位數低段，2028年調整後營業利益至少等於利息費用","2y":"2027下半年調整後營業利益÷利息費用≥60%","5y":"FY2028調整後營業利益≥利息費用，且淨負債÷調整後EBITDA≤3.5倍","10y":null,"threshold":"Q2 2026比值為20%；2027下半年仍<40%即反轉","source":"季報新聞稿（調整後營業利益、利息費用）、10-Q債務明細","drift_rule":"TTM比值連4季低於路徑5%以上為削弱，連6季低於10%以上為反轉"},{"id":"H3","text":"舊世代GPU合約到期後能以接近原價續約，證明六年折舊與資產殘值站得住（管理層：H100到期以原價約95%續約，A100新約延到2029年）","2y":null,"5y":"2027至2029年到期的Hopper與Ampere叢集續約價≥原約80%，使用率維持","10y":"2030年後Blackwell叢集到期續約價≥原約70%","threshold":"續約價<原約80%，或大量轉入短期現貨並出現閒置，即削弱","source":"法說會續約揭露、10-K折舊政策與減損","drift_rule":"跨2個年度續約價低於門檻為削弱，跨3個年度為反轉"}],"R":[{"id":"R1","text":"客戶集中與交易對手信用：前兩大客戶約占上半年營收63%，10-Q預期集中會持續；OpenAI沒有信用評等、仍在燒現金，並與Broadcom自研10GW加速器","h_ref":"H1","clock":"🔥","threshold":"前兩大客戶合計占比2027年全年≥65%（沿用前份門檻），或任一客戶延後付款、縮減承諾","evidence_refs":["customer_second_source#0","customer_concentration_credit#2","customer_concentration_credit#4","customer_second_source#2"]},{"id":"R2","text":"利息與稀釋吃掉股東經濟：Q2利息6.4億美元是調整後營業利益1.28億的5倍，Q3利息指引8.6億至9.4億；FY2026資本支出兩度上調到350億至390億，公司表示後續可能需要額外債務或股權融資","h_ref":"H2","clock":"⚡","threshold":"Q4 2026調整後營業利益率未達10%，或單季利息費用超過10億而營業利益率沒有同步擴張","evidence_refs":["capital_markets_pricing#2","unprofitable_path_to_profitability#1","unprofitable_path_to_profitability#2","unprofitable_path_to_profitability#3","unprofitable_path_to_profitability#4","unprofitable_dilution_trajectory#0","unprofitable_dilution_trajectory#1"]},{"id":"R3","text":"替代技術與GPU經濟壽命：客製加速器擴張、GPU供給改善；若舊世代租金崩落，六年折舊與殘值都不成立","h_ref":"H3","clock":"🐢","threshold":"任一主要客戶公開把50%以上推論工作移到自研晶片（沿用前份Microsoft門檻，並擴及全部大客戶），或舊世代續約價<原約80%","evidence_refs":["substitute_technology#0","substitute_technology#1","substitute_technology#2","supply_demand_durability#3"]},{"id":"R4","text":"交付與在地阻力：2025年底第三方資料中心延遲曾導致下修指引，並引來證券集體訴訟；供應鏈執行仍被形容為極其困難，地方禁建令在擴散","h_ref":"H1","clock":"⚡","threshold":"任一季因交付延遲而下修全年營收或活躍電力指引","evidence_refs":["geo_supply_chain#1","geo_supply_chain#2","regulatory_antitrust#2","major_events#1","major_events#2","lawsuit_class_action#0"]},{"id":"R5","text":"政策與地緣：資料中心用晶片的關稅豁免可能調整，AI法規跨轄區衝突，歐洲關稅威脅衝擊海外據點","h_ref":"H1","clock":"🐢","threshold":"資料中心用半導體的關稅豁免取消，或海外據點遭課稅，使單季毛利率年減超過3個百分點","evidence_refs":["reg_tariff_export#1","regulatory_antitrust#1","geo_supply_chain#0","geo_supply_chain#3"]}],"single_thing":{"description":"前兩大客戶任一縮減、延後或違約已簽的算力承諾","why_fatal":"兩家約占上半年營收63%，資產層級債務以這些合約為擔保。股權只占EV約一半，排在約461億美元淨負債之後；失去一家，營收與融資能力會同時斷裂，是數學上對終端股價最敏感的單一變數。","if_happens":"清倉；未持有者停止追蹤，直到重跑判斷。","how_monitor":"每季10-Q的客戶集中揭露、8-K重大合約變更、OpenAI與Microsoft的融資與資本支出動向、Meta與OpenAI承諾的交付進度","probability":"約10%（12至24個月）"}},"appendix_a":{"growth_durability":6,"quality_score":6,"ai_risk":"🟡","long_term_confidence":"低","fpe_fy2":null,"peg_fy2":null,"stress":{"pass":2,"total":5}},"eps_meta":{"base_eps_path":{"FY2025A":-2.81,"FY2026E":-3.94,"FY2027E":-1.81,"FY2028E":1.25},"fy_end_month":12,"eps_basis":"GAAP稀釋EPS（Koyfin共識；基期取年度財報稀釋EPS），曆年制；共識口徑事實表未明標，推定為GAAP"},"catalysts":[{"date":"2026-11","date_precision":"month","type":"guidance","event":"Q3 2026財報與Q4指引","impact":"高","watch":"利息費用對調整後營業利益的比值，以及2027年資本支出的初步指引"},{"date":"2026-11","date_precision":"month","type":"regulatory","event":"美國期中選舉前後的資料中心議題","impact":"中","watch":"地方禁建令與州級環評暫停是否擴散"},{"date":"2026-Q4","date_precision":"quarter","type":"capacity","event":"首座自建資料中心上線","impact":"中","watch":"自建站點的每兆瓦成本與毛利"},{"date":"2027-02","date_precision":"month","type":"guidance","event":"FY2026財報與FY2027指引","impact":"高","watch":"FY2027營收與資本支出指引，年底活躍電力是否超過1.85GW"}]}
```

---

## 尾段：回覆格式

只回一個 JSON 陣列，①–⑧ 每條一個元素，八個全出，不得跳號、不得多列，陣列外不得有任何文字（不加前言、不加 markdown 圍欄、不加附註）：

```json
[{"item": "①", "light": "🔴|🟡|🟢", "judgment_path": "$.路徑", "reason": "一句話"}]
```
