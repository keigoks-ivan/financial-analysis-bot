你是 DD 管線 v20 的判斷層閘（gate），標的 NVMI（20261012）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

⑥ 量化模組完整性抽查（強制）——(i) `moat.roic_durability.reinvest_rate`／`.roiic` 有沒有 `.formula_note` 真算（寫「估計約 X%」無算式＝🔴）；`.endo_ceiling` 是否與共識 EPS CAGR（facts.json）交叉檢查，天花板 < CAGR 且 `reasoning` 未處理＝🔴。(ii) `scenario_inputs` 的 Bull/Base/Bear EPS 是否有實質價差（Bull 幾乎等於 Base、只靠倍數撐估值＝退化，🔴）。(iii) `decision_inputs.irr_base_pct`／`ev5y_pct`／`asym_ratio` 缺省或 null 合法（程式回填），但 ROIIC 缺輸入、口徑或算式仍為實質問題。[gate_contract §⑥]

⑦ 數字新鮮度——`judgment.json` 引用的每個營運指標，是否不比 facts.json 的 `latest_quarter_kpis[].as_of` 對應項目舊？有一個更舊即 🔴。`decision_inputs.consensus_rev_3m_pct` 若依附 `stale=true` 來源，確認未被當唯一依據；引用摘要內容的欄位須標「來源：摘要」。[gate_contract §⑦]

⑧ 前份漂移歸因（QC-49）——facts.json 的 `prior_dd` 存在時，`drift_watch` 20 欄中有變動的每一欄是否都映射到 `contradictions[]` 一個帶 `cause` 的條目（可多欄共用一條目）、且主因站得住；**裁決／核心假設／情境方法變更不得併入純價格原因**；漏欄或無歸因＝🔴；前份該欄本身空或缺欄者不計，給 🟡 或 🟢。無前份時填 🟢 並註「無前份」。[gate_contract §⑧]
  - `axis` 以 `[程式歸因]` 開頭的條目是程式算的（均線、現價、裁決、角色）。裁決／角色條目是反事實結果（逐一把矩陣輸入改回前份值重算），視為已歸因；其中「價格變動」是反事實證明估值燈單獨改變了裁決，不適用上面「不得併入純價格原因」，不要為此給 🔴（2026-09-24）。
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

### 判斷檔 `fact_refs` 引到的事實（38 條）
- `f_kpi0_revenue_gaap`（q1_business）｜Revenue (GAAP)＝254.96 USD M｜期間與口徑：Q2 2026（季末 2026-06-30，公告於 2026-08-06）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 Nova Reports Record Q2 2026 Financial Results（https://www.prnewswire.com/il/news-releases/nova-reports-record-second-quarter-2026-financial-results-302844852.html）（numbers.latest_quarter_kpis.items[0]，as_of Q2 2026（季末 2026-06-30，公告於 2026-08-06））
  - 註記：未取得共識對照
- `f_kpi1_non_gaap_operating_incom`（q1_business）｜Non-GAAP operating income＝85.25 USD M｜期間與口徑：Q2 2026（季末 2026-06-30，公告於 2026-08-06）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 Nova Reports Record Q2 2026 Financial Results（https://www.prnewswire.com/il/news-releases/nova-reports-record-second-quarter-2026-financial-results-302844852.html）（numbers.latest_quarter_kpis.items[1]，as_of Q2 2026（季末 2026-06-30，公告於 2026-08-06））
  - 註記：未取得共識對照
- `f_kpi2_non_gaap_operating_margi`（q1_business）｜Non-GAAP operating margin＝33 %｜期間與口徑：Q2 2026（季末 2026-06-30，公告於 2026-08-06）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 Nova Reports Record Q2 2026 Financial Results（https://www.prnewswire.com/il/news-releases/nova-reports-record-second-quarter-2026-financial-results-302844852.html）（numbers.latest_quarter_kpis.items[2]，as_of Q2 2026（季末 2026-06-30，公告於 2026-08-06））
  - 註記：未取得共識對照
- `f_kpi3_gaap_operating_income`（q1_business）｜GAAP operating income＝76.19 USD M｜期間與口徑：Q2 2026（季末 2026-06-30，公告於 2026-08-06）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 Nova Reports Record Q2 2026 Financial Results（https://www.prnewswire.com/il/news-releases/nova-reports-record-second-quarter-2026-financial-results-302844852.html）（numbers.latest_quarter_kpis.items[3]，as_of Q2 2026（季末 2026-06-30，公告於 2026-08-06））
  - 註記：未取得共識對照
- `f_kpi4_gaap_operating_margin`（q1_business）｜GAAP operating margin＝30 %｜期間與口徑：Q2 2026（季末 2026-06-30，公告於 2026-08-06）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 Nova Reports Record Q2 2026 Financial Results（https://www.prnewswire.com/il/news-releases/nova-reports-record-second-quarter-2026-financial-results-302844852.html）（numbers.latest_quarter_kpis.items[4]，as_of Q2 2026（季末 2026-06-30，公告於 2026-08-06））
  - 註記：未取得共識對照
- `f_kpi7_guidance_q3_2026`（q1_business）｜Guidance Q3 2026 營收＝277～287 USD M｜期間與口徑：Q2 2026（季末 2026-06-30，公告於 2026-08-06）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司新聞稿 Nova Reports Record Q2 2026 Financial Results（https://www.prnewswire.com/il/news-releases/nova-reports-record-second-quarter-2026-financial-results-302844852.html）（numbers.latest_quarter_kpis.items[7]，as_of Q2 2026（季末 2026-06-30，公告於 2026-08-06））
  - 註記：未取得共識對照
- `f_kpi8_guidance_q3_2026_non_gaa`（q1_business）｜Guidance Q3 2026 non-GAAP diluted EPS＝2.7～2.85 USD｜期間與口徑：Q2 2026（季末 2026-06-30，公告於 2026-08-06）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司新聞稿 Nova Reports Record Q2 2026 Financial Results（https://www.prnewswire.com/il/news-releases/nova-reports-record-second-quarter-2026-financial-results-302844852.html）（numbers.latest_quarter_kpis.items[8]，as_of Q2 2026（季末 2026-06-30，公告於 2026-08-06））
  - 註記：未取得共識對照
- `f_earnings_recency`（q1_business）｜最近一次財報日＝2026-08-06 date｜期間與口徑：2026-08-06／距今 47 個交易日｜kind：realized
  - 來源：—（numbers.earnings_recency，as_of 2026-08-06）
- `f_peer_nvmi_gross_margin_pct`（q2_moat）｜NVMI 毛利率＝57.12 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.NVMI.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_nvmi_operating_margin_pct`（q2_moat）｜NVMI 營業利益率＝28.97 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.NVMI.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_nvmi_fcf_margin_pct`（q2_moat）｜NVMI FCF 利潤率＝20.24 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.NVMI.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_klac_gross_margin_pct`（q2_moat）｜KLAC 毛利率＝61.3 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.KLAC.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_klac_operating_margin_pct`（q2_moat）｜KLAC 營業利益率＝41.69 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.KLAC.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_klac_fcf_margin_pct`（q2_moat）｜KLAC FCF 利潤率＝27.74 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.KLAC.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_onto_gross_margin_pct`（q2_moat）｜ONTO 毛利率＝50.36 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ONTO.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_onto_operating_margin_pct`（q2_moat）｜ONTO 營業利益率＝13.81 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ONTO.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_onto_fcf_margin_pct`（q2_moat）｜ONTO FCF 利潤率＝22.54 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ONTO.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_camt_gross_margin_pct`（q2_moat）｜CAMT 毛利率＝50.05 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CAMT.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_camt_operating_margin_pct`（q2_moat）｜CAMT 營業利益率＝23.19 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CAMT.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝10.67 USD/share｜期間與口徑：2026-10-08／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261008.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-10-08）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝13.66 USD/share｜期間與口徑：2026-10-08／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261008.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-10-08）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝16.59 USD/share｜期間與口徑：2026-10-08／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261008.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-10-08）
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝1.72 %｜期間與口徑：2026-07-16 → 2026-10-08／FY1 共識 EPS 10.49 → 10.67（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261008.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-10-08）
- `f_kpi5_free_cash_flow_40_92_cap`（q4_capital）｜Free cash flow（推算＝營運現金流 40.92 − capex 2.49；公司未揭露 FCF）＝38.42 USD M｜期間與口徑：Q2 2026（季末 2026-06-30，公告於 2026-08-06）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 Nova Reports Record Q2 2026 Financial Results（https://www.prnewswire.com/il/news-releases/nova-reports-record-second-quarter-2026-financial-results-302844852.html）；FCF 為依新聞稿現金流量表推算（numbers.latest_quarter_kpis.items[5]，as_of Q2 2026（季末 2026-06-30，公告於 2026-08-06））
  - 註記：未取得共識對照
- `f_kpi6_sbc_gaap`（q4_capital）｜SBC 占 GAAP 營業利益＝8.9 %｜期間與口徑：Q2 2026（季末 2026-06-30，公告於 2026-08-06）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 Nova Reports Record Q2 2026 Financial Results（https://www.prnewswire.com/il/news-releases/nova-reports-record-second-quarter-2026-financial-results-302844852.html）（numbers.latest_quarter_kpis.items[6]，as_of Q2 2026（季末 2026-06-30，公告於 2026-08-06））
  - 註記：未取得共識對照
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝353.0 USD｜期間與口徑：2026-10-09（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-10-09（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝33.08 x｜期間與口徑：2026-10-08／分母＝FY1 EPS 10.67，分子＝快照價 353.0｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-10-08）
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝44.12 x｜期間與口徑：2026-10-09（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-10-09（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝100.0 %｜期間與口徑：2026-10-09（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-10-09（RTH 收盤，UTC））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝11.98 x｜期間與口徑：2026-10-09（RTH 收盤，UTC）／4 個年度端點內的分位＝88.1｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-10-09（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝88.1 %｜期間與口徑：2026-10-09（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-10-09（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝11.74 x｜期間與口徑：2026-10-09（RTH 收盤，UTC）／4 個年度端點內的分位＝78.2｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-10-09（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝78.2 %｜期間與口徑：2026-10-09（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-10-09（RTH 收盤，UTC））
- `f_consensus_rev_fy1_pct`（q5_valuation）｜FY1 共識修正＝0.0 %｜期間與口徑：2026-10-08／兩份 Koyfin 快照之間的 EPS 修正幅度（10.67 → 10.67）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261008.xlsx（numbers.consensus_revision.fy1.revision_pct，as_of 2026-10-08）
- `f_consensus_rev_fy2_pct`（q5_valuation）｜FY2 共識修正＝0.0 %｜期間與口徑：2026-10-08／兩份 Koyfin 快照之間的 EPS 修正幅度（13.66 → 13.66）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261008.xlsx（numbers.consensus_revision.fy2.revision_pct，as_of 2026-10-08）
- `f_consensus_rev_fy3_pct`（q5_valuation）｜FY3 共識修正＝0.0 %｜期間與口徑：2026-10-08／兩份 Koyfin 快照之間的 EPS 修正幅度（16.59 → 16.59）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261008.xlsx（numbers.consensus_revision.fy3.revision_pct，as_of 2026-10-08）
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝-28.84 %｜期間與口徑：2026-10-09（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-10-09（RTH 收盤，UTC））
- `f_rsi14`（q5_valuation）｜RSI(14)＝40.13｜期間與口徑：2026-10-09（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-10-09（RTH 收盤，UTC））

### findings_digest 中方向為負或來源衝突的條目（12 條）
- `customer_concentration_credit#3`（customer_concentration_credit｜方向 -｜狀態 ok）：客戶信用：搜尋僅得 Intel（客戶身分推測未經 Nova 確認，客戶未具名）2025 年遭 Fitch 降至 BBB 負向展望、S&P 降至 BBB；未找到 2026 年評等動作。Nova 客戶實際身分未於本軸證實。
  - 來源：Fitch/S&P Intel downgrade coverage (bondblox, tweaktown)（as_of 2025-01-01）｜affects：decision_inputs.bear
- `supply_demand_durability#4`（supply_demand_durability｜方向 -｜狀態 ok）：風險面：分析師指出若先進封裝投資放緩，WMC／Prism 等工具可能利用率不足；另有先進節點大客戶撤單的集中度風險；NAND 仍處長期下行。
  - 來源：Quartr — Nova Citi 2026 TMT summary／搜尋摘要（as_of 2026-09-30）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：Nova FY2025 20-F 風險因素：貿易限制、關稅變動與進出口許可可能使受影響國家的銷售大幅減少；主要客戶位於台灣、日本、南韓、中國與美國。
  - 來源：NOVA LTD. Form 20-F FY2025 (SEC)（as_of 2026-01-01）｜affects：decision_inputs.bear、thesis.R
- `reg_tariff_export#1`（reg_tariff_export｜方向 -｜狀態 ok）：中國占 Nova 營收約 35%（2025 上半年），2024 年為 39%；管理層預期中國占比下降。來源為第三方 PESTLE 分析（2026-04 更新），非公司文件。
  - 來源：dcf-analysis.com Nova Ltd. (NVMI) PESTLE Analysis [Apr-2026 Updated]（as_of 2026-04-01）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#4`（reg_tariff_export｜方向 -｜狀態 ok）：Section 122 全球替代關稅 10%、後升至 15%，自 2026-02-24 生效，可能波及半導體供應鏈（出自 SEALSQ 424B5，非 Nova 專屬）。
  - 來源：SEALSQ Corp Form 424B5 FY2026 (SEC)（as_of 2026-02-24）｜affects：thesis.R
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：Nova 2025 20-F 摘要列出營運集中於以色列、美國、德國的製造設施，並提及對中國晶片廠銷售受出口管制與關稅影響。
  - 來源：StockTitan, Nova Ltd 20-F annual report summary（as_of 2026-03-01）｜affects：decision_inputs.bear、thesis.R
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：Nova 2026年8月（Q2 2026）投資人簡報風險項列有依賴有限數量供應商，以及每條產品線依賴單一製造設施；FY2024 20-F 亦稱對有限供應商、部分情況為唯一供應商。
  - 來源：Nova investor presentation Q2 2026 / Nova 20-F FY2024 (SEC)（as_of 2026-08-01）｜affects：decision_inputs.bear、thesis.R
- `geo_supply_chain#2`（geo_supply_chain｜方向 -｜狀態 ok）：中國占 Nova 營收：2024年約39%（分析師於法說會提問）；第三方稱2025上半年約35%，預期占比下降但名目仍小幅成長（二手來源）。
  - 來源：fintool.com NVMI research; dcf-model.com PESTLE（as_of 2025-11-01）｜affects：decision_inputs.bear、valuation
- `geo_supply_chain#3`（geo_supply_chain｜方向 -｜狀態 ok）：Nova Q1 2026 前瞻聲明列示外國政治經濟風險，含供應鏈困難及可能限制營運的制裁與出口限制。
  - 來源：Nova Q1 2026 call date PDF / VCP Scanner NVMI（as_of 2026-04-01）｜affects：thesis.R
- `end_markets#2`（end_markets｜方向 -｜狀態 ok）：Q2 2026 毛利率 56.5%，低於 Q1 2026 的 57.7% 與 Q2 2025 的 57.8%。
  - 來源：Nova Q2 2026 results (2026-08-06), 搜尋彙整（as_of 2026-08-06）｜affects：moat_trend、decision_inputs.bear
- `substitute_technology#1`（substitute_technology｜方向 -｜狀態 ok）：Onto 的 Atlas G6 OCD 系統（2025-09 發表）瞄準第二代 GAA 邏輯與 HBM 用垂直閘 DRAM，已取得多家邏輯與記憶體廠量產訂單；光學量測仍是主流路線，同業在同一賽道推新平台。
  - 來源：Business Wire：Onto Innovation Launches Next Generation OCD Metrology Platform to Enable Process Control for Advanced AI Devices（as_of 2025-09-09）｜affects：moat_trend、decision_inputs.bear
- `capital_markets_pricing#2`（capital_markets_pricing｜方向 -｜狀態 ok）：Benzinga 2026-09-03 快照：10 位分析師平均目標價約 491，高 640、低 240（Jefferies）；Citigroup 8/10 由 595 降至 550，Needham 8/7 由 640 降至 570
  - 來源：Benzinga NVMI sentiment page（as_of 2026-09-03）｜affects：valuation、decision_inputs.bear

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 7 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/NVMI_20261012/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":770.0,"bear_5y_price":234.0,"p_bull_pct":25,"p_bear_pct":30,"upside_5y_pct":46.2,"ev5y_pct":40.2,"irr_base_pct":7.9,"asym_ratio":2.9,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":10.67,"pe":33.08,"basis":"FY2026E 共識非 GAAP EPS（Koyfin 2026-10-08），股價 353 美元；終端倍數同樣採「股價÷當年度 EPS」口徑"},"eps":{"bull":[14.8,18.5,21.0,24.0,27.5],"base":[13.66,16.59,17.0,19.0,21.5],"bear":[12.0,10.5,11.0,12.0,13.0]},"pe":{"bull":28,"base":24,"bear":18},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0,"net_buyback":0.6},"second_stage":{"bull_cagr_pct":14,"base_cagr_pct":10},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### NVMI_Q1_2026_Earnings_Call_20260514.md
- 2026-05-14｜CFO｜guidance：CFO 給 Q2 營收指引區間 2.45–2.55 億美元（原話："between $245 million and $255 million."）
- 2026-05-14｜CFO｜guidance：CFO 給 Q2 non-GAAP EPS 指引 2.34–2.48 美元（原話："Non-GAAP earnings per diluted share to range from $2.34 to"）
- 2026-05-14｜CEO｜guidance：CEO 表示客戶排程考量使上半年偏高、下半年預期更高（原話："we expect the second half to run higher"）
- 2026-05-14｜CEO｜guidance：CEO 讀 WFE 今年中十位數成長，高於 2 月看法，預期 Nova 表現優於此數（原話："we expect WFE to reach mid-teens growth"）
- 2026-05-14｜CFO｜margin：CFO 說明 Q1 毛利率與其驅動因素（產品組合與服務成長）（原話："blended gross margins were 57.7% on a GAAP basis"）
- 2026-05-14｜CFO｜margin：CFO 稱 Q1 營業利益率超過目標模型上緣 28%–33%（原話："reached 30% on a GAAP basis and 34% on a non-GAAP basis"）
- 2026-05-14｜CFO｜margin：CFO 答全年毛利率會落在與上半年指引相同的區間、可持續（原話："we see gross margins for 2026 will be within the same rate"）
- 2026-05-14｜CFO｜margin：CFO 解釋 Q2 毛利率指引 59% 較 Q1 低的口徑：指引通常上下 1%（原話："guiding, it's plus/minus 1%. So it's within the same"）
- 2026-05-14｜CFO｜margin：CFO 給 Q2 費用與稅率指引：non-GAAP 營業費用增至約 6,600 萬美元、稅率約 15%（原話："Effective tax rate is expected to be approximately 15%."）
- 2026-05-14｜CEO｜commitment：CEO 重申 2027 年營收 10 億美元的策略目標仍在軌道上，且不提供更遠指引（原話："we are on track, of course, to reach this"）
- 2026-05-14｜CEO｜commitment：CEO 重申 GAA 累計 5 億美元營收目標在軌道上，並稱 2027 年 GAA 投資較今年成長（原話："we're on track for the forecasted $500 million cumulative"）
- 2026-05-14｜CEO｜customer：CEO 稱客戶更早規劃，部分已下單並規劃 2027 年交貨，能見度提高（原話："we do have improved visibility towards next year"）
- 2026-05-14｜CEO｜customer：CEO 稱有拉貨使上半年高於原預期，交貨時點由客戶需求結構決定（原話："We do see some pull-ins, by the way, driving the first half"）
- 2026-05-14｜CFO｜customer：CFO 揭露 Q1 營收組合 Logic/Foundry 約 66%、Memory 約 34%（原話："Revenue mix was approximately 66% from Logic and Foundry"）
- 2026-05-14｜CEO｜customer：CEO 預期今年 Memory 占比較去年更高，由先進 DRAM 投資帶動（原話："I expect Memory to become more dominant this year"）
- 2026-05-14｜CEO｜customer：CEO 稱中國占營收比重預期下降，長期穩定在 25%–30%，今年較上季有正向動能（原話："we expect China to stabilize in the range of 25% to 30%"）
- 2026-05-14｜CEO｜customer：CEO 稱 Nova 獲 Intel EPIC 供應商獎（原話："Nova was awarded the Intel EPIC"）
- 2026-05-14｜CFO｜customer：CFO 稱有 4 家客戶與 5 個地區各占產品營收逾 10%（原話："4 customers and 5 geographic regions, each"）
- 2026-05-14｜CEO｜competition：CEO 引 Gartner 報告稱膜厚與 CD 量測市占再增 400 bp，為第二大供應商（原話："an additional 400 basis points share gain"）
- 2026-05-14｜CEO｜competition：CEO 承認 XPS 與材料量測出現競爭，含中國本土廠商與其他潛在新進者（原話："We are also seeing emerging XPS and material metrology"）
- 2026-05-14｜CEO｜competition：CEO 稱中國市場競爭激烈，Nova 以產品與擁有成本作為差異化（原話："China is also a very competitive market, as you know."）
- 2026-05-14｜CEO｜competition：CEO 稱交期仍短於部分同業（原話："Our lead times are still shorter than some of our peers"）
- 2026-05-14｜CEO｜product：CEO 稱先進封裝已接近產品營收的 20% 中段，多數來自 Logic（原話："advanced packaging for Nova is edging towards the mid-20s"）
- 2026-05-14｜CEO｜product：CEO 稱先進 DRAM 約占 Memory 業務 2/3，Metrion 平台創紀錄（原話："approximately 2/3 of our memory business"）
- 2026-05-14｜CEO｜product：CEO 稱混合鍵合採用速度快於預期，量測密集度高（原話："Adoption is progressing faster than expected"）
- 2026-05-14｜CEO｜product：CEO 稱部分客戶（尤其 Memory）對混合鍵合有拉貨（原話："We do see some pull-ins for hybrid bonding"）
- 2026-05-14｜CEO｜product：CEO 稱服務營收創紀錄，連續第 13 季季增（原話："marking the 13th consecutive"）
- 2026-05-14｜CEO｜capital_allocation：CEO 稱亞洲新廠預計 2026 年底前後投產，目標擴產、優化成本、區域負載平衡（原話："The new facility is expected to become operational"）
- 2026-05-14｜CEO｜risk：CEO 承認供應鏈有壓力並正與數家供應商協調（原話："We see, I would say, some pressure on the"）
- 2026-05-14｜CEO｜risk：CEO 稱供應商端出現成本壓力，主因晶片價格上漲，以成本管理因應（原話："some cost pressure at the supplier level, mainly tied to the"）
- 2026-05-14｜CEO｜risk：CEO 答分析師質疑製程管制強度時稱今年製程管制表現尚難判斷（原話："it's too early to say how process control looks like"）
- 2026-05-14｜CFO｜risk：CFO 稱 Q1 稅率約 17%，略高於指引，預期正常化（原話："We expect this dynamic to normalize as the year"）

### NVMI_Citi_s_2026_Global_TMT_Conference_20260908.md
- 2026-09-08｜Guy Kizner (CFO)｜guidance：CFO 稱 WFE 數字依賴外部共識，2026 年 WFE 成長將高於 20%，無法給確切數字（原話："when we're looking on the WFE, it will be above 20%."）
- 2026-09-08｜Guy Kizner (CFO)｜competition：管理層說明 2026 年未見慣常的優於 WFE 表現（敘事與先前「2x WFE」框架相比有變）（原話："we don't see the same outperformance that we usually used"）
- 2026-09-08｜Guy Kizner (CFO)｜product：NAND 因多為升級而非新增產能，Nova 尚未受惠，希望 2027 出現（原話："Hopefully, we will see some of it happening in 2027."）
- 2026-09-08｜Guy Kizner (CFO)｜margin：DRAM 的量測密集度低於邏輯，長期模型為邏輯 60／其餘 40（原話："metrology intensity in DRAM is lower compared to the logic"）
- 2026-09-08｜Guy Kizner (CFO)｜risk：AI 客戶仍用 3nm／5nm（N-1）並大舉擴充產能，未轉 GAA，使 2026 量測密集度下降（原話："the metrology intensity went down because of the spending"）
- 2026-09-08｜Guy Kizner (CFO)｜guidance：管理層預期 2027 邏輯端組合偏向 2nm 與 GAA，量測密集度回升（原話："we will see much more metrology intensity going up"）
- 2026-09-08｜Guy Kizner (CFO)｜guidance：DRAM 2027 預期不會有量測密集度顯著提升，要到 4F square 的 2028 年之後（原話："it will happen in '28 and going forward"）
- 2026-09-08｜Guy Kizner (CFO)｜customer：管理層描述訂單能見度優於過往上行週期：積存訂單較高、客戶遵守交期、提前給預測（原話："it's higher versus the previous up cycles"）
- 2026-09-08｜Guy Kizner (CFO)｜customer：客戶提供約一年以上的預測（原話："they are giving you a forecast, say, 1 year ahead"）
- 2026-09-08｜Guy Kizner (CFO)｜customer：被問訂金時，管理層稱交期與條款未改變（原話："we are not changing the terms and conditions"）
- 2026-09-08｜Guy Kizner (CFO)｜product：ELIPSON／METRION 現階段重點是增加應用與搭載率，客戶回購但屬漸進過程（原話："we see repeat buys from leading customers"）
- 2026-09-08｜Guy Kizner (CFO)｜product：WMC 平台一年前推出，近期再宣布一項客戶採用（原話："just recently, we announced another win with this platform"）
- 2026-09-08｜Guy Kizner (CFO)｜product：先進封裝占比由 2025 年約 20% 升至第二季 25%；材料量測尚未切入封裝，被視為下一個成長引擎（原話："we reached a level of 25% of contribution"）
- 2026-09-08｜Guy Kizner (CFO)｜product：混合鍵合 2027 年並非量產大題，目前重點是驗證（原話："the capacity is not a big story in 2027"）
- 2026-09-08｜Guy Kizner (CFO)｜margin：上半年毛利率 59%，第三季財測亦為 59%，管理層稱已處於目標模型高端（原話："In the third quarter guidance, we also guided at 59%."）
- 2026-09-08｜Guy Kizner (CFO)｜margin：毛利率驅動因素：規模經濟、技術進步帶動 ASP；客戶規模越大折扣越高；成本面有材料與人力上升（原話："the bigger customer, the higher discounts"）
- 2026-09-08｜Guy Kizner (CFO)｜margin：產品毛利率高於服務；服務屬人力密集，但隨裝機規模有槓桿（原話："So the gross margins on the service side are lower."）
- 2026-09-08｜Guy Kizner (CFO)｜commitment：新目標模型將於 2027 年初投資人日公布，涵蓋未來五年市場、技術與財務模型（原話："planning to do an Investor Day in the beginning of 2027"）
- 2026-09-08｜Guy Kizner (CFO)｜guidance：第二季達到 2022 年目標模型的營收run rate，比預定時程早約一年；預期營運槓桿持續增加（原話："we should expect operation leverage keep increasing."）
- 2026-09-08｜Guy Kizner (CFO)｜capital_allocation：現金逾 17 億美元，首要優先仍為併購，並維持紀律（增益、符合財務模型、明確綜效）（原話："top priority for us is inorganic growth"）
- 2026-09-08｜Guy Kizner (CFO)｜capital_allocation：先前 1 億美元回購已完成，新增最多 2 億美元授權，視市場條件與估值執行（原話："an additional authorization up to $200 million"）
- 2026-09-08｜Guy Kizner (CFO)｜capital_allocation：併購目標領域不限於封裝或光子，核心篩選是綜效（原話："If we have not identified synergies"）
- 2026-09-08｜Guy Kizner (CFO)｜commitment：擴產：美國產線加倍、德國新無塵室、年底首度在亞洲開無塵室；2027 年 CapEx 仍聚焦基礎設施（原話："by the end of this year for the first time in Asia"）
- 2026-09-08｜Guy Kizner (CFO)｜risk：供應鏈瓶頸被視為關注點，管理層讓供應商看到需求並尋找備援供應商（原話："if there is a bottleneck in specific vendor"）
- 2026-09-08｜Guy Kizner (CFO)｜guidance：中國營收占約 30%；今年原預期持平至略降，現預期名目金額仍成長，占比續降（原話："another growth year for China for us on a nominal basis"）
- 2026-09-08｜Guy Kizner (CFO)｜competition：中國本土廠商正在追趕；管理層視為風險，目前仍有技術差距，策略是加大 R&D（原話："We are not dismissing any competition"）
- 2026-09-08｜Guy Kizner (CFO)｜commitment：對中國本土競爭的策略承諾：持續以高比例營收投入研發（原話："Our goal is to run faster."）

### 問答異常語氣（迴避／改口／保留）
- NVMI_Q1_2026_Earnings_Call_20260514.md｜問：Needham 問中國今年預期（前次為持平到小增）是否改變｜答法：未直接回答是否調整先前說法，也未給數字，改談中國占比下降、長期 25–30%、封裝新客戶及「some potential growth」
- NVMI_Q1_2026_Earnings_Call_20260514.md｜問：Morgan Stanley 問今年製程管制強度偏低下如何優於 WFE｜答法：稱「too early to call」，未給優於 WFE 的幅度，改談製程與製程管制兩條成長線
- NVMI_Q1_2026_Earnings_Call_20260514.md｜問：Barclays 問 Q2 毛利率指引較 Q1 下降的原因｜答法：未說明驅動因素，僅稱指引通常上下 1%、屬同一量級
- NVMI_Q1_2026_Earnings_Call_20260514.md｜問：BofA 問全年成長相對 WFE 與 Memory/Logic 組合｜答法：未給全年成長數字，僅稱預期優於 WFE 並重申 2027 年 10 億美元目標
- NVMI_Citi_s_2026_Global_TMT_Conference_20260908.md｜問：分析師問 2026／2027 WFE 規模與五月「中位數十幾%」框架如何演變｜答法：稱自己無內部 WFE 預測、只引用共識，僅說高於 20%，明說很難給確切數字
- NVMI_Citi_s_2026_Global_TMT_Conference_20260908.md｜問：分析師問是否仍對「2x WFE」的優於大盤表現有信心｜答法：未直接重申 2x；改談 2026 年投資組合不利並說 2027 組合改善，語氣轉為「well positioned」
- NVMI_Citi_s_2026_Global_TMT_Conference_20260908.md｜問：分析師問如何達到目標模型毛利率高端／是否有價值定價重新定價空間｜答法：未給具體路徑數字，以定性因素回答；定價題以「價值導向」籠統帶過，未回答是否重新定價

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 3 | 4 |
| customer_second_source | none | 0 | 2 |
| customer_concentration_credit | found | 4 | 3 |
| supply_demand_durability | found | 5 | 3 |
| regulatory_antitrust | none | 0 | 3 |
| reg_tariff_export | found | 5 | 4 |
| geo_supply_chain | found | 4 | 4 |
| end_markets | found | 10 | 4 |
| substitute_technology | found | 4 | 4 |
| channel_business_model_shift | none | 0 | 2 |
| capital_markets_pricing | found | 4 | 4 |
| major_events | none | 0 | 4 |

未涵蓋／不適用軸的查詢詞原文（供判相關性）：
- **customer_second_source**（none）：Nova Ltd NVMI largest customer second-source OR in-house 2026；Nova NVMI single-source risk customer concentration TSMC Samsung Intel metrology competitor win 2026
- **regulatory_antitrust**（none）：Nova Ltd NVMI antitrust OR monopoly investigation 2026；Nova Ltd regulation OR regulatory scrutiny semiconductor metrology export controls 2026；Nova Ltd NVMI DOJ OR FTC OR EU competition 2026
- **channel_business_model_shift**（none）：Nova Ltd NVMI business model recurring revenue services subscription 2026；Nova NVMI go-to-market change distribution channel 2026 metrology
- **major_events**（none）：Nova Ltd NVMI acquisition merger 2025 2026；Nova Ltd NVMI class action lawsuit securities fraud；Nova Ltd NVMI SEC investigation restatement；Nova Ltd NVMI product launch recall warning letter export license

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260515","verdict":"B 觀望（v12.3 unchanged）— 護城河 8/10（execution 8 + pricing power 7，二維 divergence：execution ↑ widening / pricing power → stable）+ 體質 veto 0/5 → B 級；FPE 54x 5Y 分位 95-100% + PEG 2.43 + 同業 metrology tier 中位 +54% 溢價無支撐 → 估值🔴；MA ✅ 但 BB 上軌觸及 → 短期動能透支；QC-31 規則 5「估值🔴 + thesis 完整 → 落 B 等修復」決定 final_signal = B。等 BB 中軌~$461 或 FPE 修復至 35-40x（~$362-$415）再評估進場。","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"GAA + 先進封裝帶動 metrology intensity 結構性提升","columns":{"2Y 驗證點":"Nova Rev YoY ≥ WFE YoY + 10%p 連續 8 季","5Y 驗證點":"Metrology TAM 5Y CAGR ≥ 10% vs WFE CAGR ≤ 7%","10Y 驗證點":"1.4nm CFET 量產時 metrology 步驟 / 晶圓 ≥ 5nm 的 1.5 倍","驗證指標":"Rev / WFE 比、metrology 步驟數","資料來源":"2Y: §6 季財報 / 5Y: §8 A Runway / 10Y: §11 TAM 路線圖"}},{"id":"H2","text":"Nova 三平台架構讓全球前 5 大代工廠 / IDM 必選","columns":{"2Y 驗證點":"FY26 先進封裝佔產品營收 ≥ 25%（vs FY25 20%）","5Y 驗證點":"市佔率從 ~4-5% 提升至 6%+（隱含 Nova Rev CAGR &gt; TAM CAGR ≥ 5%p）","10Y 驗證點":"三平台中至少兩個成為 1.4nm GAA generation 的 standard reference tool","驗證指標":"產品營收結構、市佔","資料來源":"2Y: 季財報 / 5Y: 年報 §1 strategic / 10Y: 客戶 design win 公告"}},{"id":"H3","text":"估值修復至合理區間後支持 5Y 翻倍報酬","columns":{"2Y 驗證點":"FPE 從 54x 修復至 35-40x 後再從這個 base 出發","5Y 驗證點":"FY30 EPS ≥ $22.0 + PE 25x → 股價 $550 區（vs 現價 持平 = 5Y 報酬 0%）","10Y 驗證點":"FY35 EPS ≥ $40 + PE 22x → 股價 $880 區（vs 現價 +58%）","驗證指標":"FPE 軌跡、EPS 兌現","資料來源":"2Y: §13.1 / 5Y: §13.5 / 10Y: §8 E 壓測"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"WFE 2027 進入長 cycle 消化期（HBM capex 過峰 + 中國 over-build）","columns":{"對應假設":"H1","時間尺度":"🔥 中期（4-6 季可觸發）","監測指標":"全球 WFE YoY、SEMI World Fab Forecast；Nova vs WFE YoY 差距（TTM）","警戒閾值":"WFE YoY &lt; 0% 連 2 季 = 警戒；連 4 季 = 大動作減倉；Nova vs WFE 差距 &lt; 8pp 連 2 季 = H1 削弱"}},{"id":"R2","text":"KLA 推出整合三平台方案在 GAA 首次取單（生態攻擊型 — QC-23 🔴）","columns":{"對應假設":"H2","時間尺度":"🐢 長期結構（2-5 年慢變數；事件觸發型）","監測指標":"KLA 新品發佈、Nova 客戶集中度變化、SEMI 大會 metrology 整合相關公告","警戒閾值":"KLA 三平台整合工具公告 + Nova 季 Rev 連 2 季 −（雙條件，避免單一新聞噪音）"}},{"id":"R3","text":"估值壓縮（PE 修復過程，獨立於基本面；ASML 2021/Q3 路徑風險）","columns":{"對應假設":"H3","時間尺度":"⚡ 短期（1-2 季可觸發；需快速響應）","監測指標":"Fwd P/E 趨勢、Bollinger Band 位置、共識 EPS 90d 變化","警戒閾值":"Fwd P/E &lt; 35x = 進場觸發；&gt; 60x = 減倉觸發；連 90d 共識下修 &gt; 5% = 重評"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🔴","ma":"✅","trap":"🟢","moat_trend":null,"runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":556.11,"archetype":null,"cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"NVMI","date":"2026-10-12","schema":"v15.2","contract":"v19","company_name":"Nova Ltd."},"oneliner":"量測設備第二大廠：財報創紀錄、共識 EPS 沒有下修，半年跌 29% 全部來自倍數收縮。FY2 本益比 25.8 倍已回到合理區間，但 2027 年量測密集度回升目前只有管理層說法，等第四季財報與投資人日證實再進場。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/NVMI_20261012/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/NVMI_20261012/scenario.json","answers":{"q1_business":{"verdict":"Nova 賺的是先進邏輯、DRAM 與先進封裝晶圓廠資本支出裡的量測預算，錢卡在每一層新製程的量產指定機台。本輪處於擴張期，結構性成分真實存在，但今年量測密集度反而下降。","reasoning":"收入分兩塊。產品第二季 2.015 億美元，其中邏輯／代工 73%、記憶體與其他 27%；服務 0.535 億美元，連續創紀錄，含既有機台升級。產品的錢來自晶圓廠擴產與新製程導入：第二季先進邏輯營收季增一倍以上，先進封裝接近產品營收的四分之一。第二季營收 2.55 億美元，落在財測上緣，GAAP 營益率 30%、非 GAAP 33%。第三季財測營收 2.77–2.87 億美元、非 GAAP EPS 2.70–2.85 美元，高於當時共識。錢卡在每一層新製程的量產指定機台：選上之後隨客戶擴產複製出貨，再收服務與升級費。單點依賴方面，第二季有兩家客戶各占產品營收 10% 以上（第一季是四家）；20-F 摘要顯示最大客戶占比從 2021 年 31% 降到 2024 年 18%（2025 年數字未取得），集中度在下降，不構成單點。最大的依賴是地理，中國約占 30%。供需持久性：以週期性擴張為主。結構性成分（GAA、先進封裝提高量測次數）是真的，但今年被 AI 客戶擴充舊製程稀釋；客戶可以延後擴產，所以供給可逆性高。產業時鐘判在擴張期，依據是 WFE 2026 年成長逾 20%、SEMI 估 2027 年再成長 21.8%，加上供應鏈吃緊、交期 4–12 個月、客戶已提前下 2027 年訂單。","fact_refs":["f_kpi0_revenue_gaap","f_kpi1_non_gaap_operating_incom","f_kpi2_non_gaap_operating_margi","f_kpi3_gaap_operating_income","f_kpi4_gaap_operating_margin","f_kpi7_guidance_q3_2026","f_kpi8_guidance_q3_2026_non_gaa","f_earnings_recency"],"verdict_values":{"revenue_quality":"產品約 79%、服務約 21%（第二季 2.015 億／0.535 億美元）。產品隨晶圓廠擴產與製程轉換起落；服務隨裝機量累積、連續創紀錄，是週期裡的穩定墊。","unit_econ_note":"第二季 GAAP 毛利率 56.5%、營益率 30%，非 GAAP 營益率 33%，落在目標模型 28–33% 的上緣。研發約占營收 15–16%，資本支出約占營收 1%，屬資本輕型。","archetype":{"primary":"品質複利成長","secondary":"循環/商品","confidence":"中","fingerprint":"毛利率四年都在 55.5–57.6%；2023 年下行時營收減 9.3%，EPS 只從 4.40 降到 4.28。但營收方向仍由晶圓廠資本支出決定。"},"industry":{"clock_phase":"II","sd_verdict_source":"以週期性擴張為主、結構性成分為輔。花旗會議上財務長說 WFE 2026 年成長高於 20%，SEMI 估 2027 年 +21.8%、2028 年 +14.1%。結構面是 GAA 與先進封裝讓量測次數增加（Yole），但 2026 年 AI 客戶多在擴充 3／5 奈米舊製程，量測密集度下降。客戶拉貨與「能見度前所未見」這類說法屬於擴張中後段的訊號；客戶可以延後擴產，供給可逆性高。","bargaining":{"up":"供應商家數有限，部分零件只有唯一供應商，每條產品線只有單一製造點；記憶體等零組件漲價，但財務長說占物料成本比重不大。","down":"客戶是少數巨型晶圓廠，第二季有兩家各占產品營收 10% 以上；財務長承認客戶越大折扣越高。","geo":"中國約占營收 30%，主要客戶分布在台、日、韓、中、美；營運集中在以色列、美國、德國。"},"profit_pool_dir":"量測與檢測約占 WFE 14%，並隨製程複雜度上升（Yole）。池內利潤 KLA 拿走最多；Nova 份額在上升，但利潤率仍低於 KLA。","tam_table":[{"item":"WFE 2026","value":"SEMI 估 1,439 億美元（+23.1%）；Yole 上修至約 1,620 億美元（兩者定義不同）"},{"item":"WFE 2027–2028","value":"SEMI 估 +21.8%、+14.1%；Yole 估至 2031 年年化約 9%"},{"item":"量測與檢測市場 2025","value":"逾 180 億美元，年增 15%，約占 WFE 14%（Yole）"},{"item":"製程控制設備 TAM","value":"GMI：2025 年 126 億→2026 年 135 億美元；TBRC：82.9 億→88.2 億美元；定義不同，不可直接比較"},{"item":"Nova 份額","value":"第三方估製程控制約 18%、KLA 約 55%（無方法論、未驗證）；Gartner 子市場連兩年增約 400 個基點（管理層轉述）"},{"item":"利潤池五年變化","value":"事實表未涵蓋各環節營業利益池占比"}]}}},"q2_moat":{"verdict":"護城河方向判穩定（→），等級 B。份額仍在增加，但第二代 GAA 正在重新招標、毛利率年減、中國本土廠在追趕，今年看不到護城河擴大的價格證據。","reasoning":"機制：量測靠物理模型加機器學習模型綁進客戶製程。每一層製程選定量產指定機台後，同一世代內換供應商要重做模型與認證。Nova 再用 XPS 材料量測、ancosys 化學量測、WMC 封裝量測，把每座廠的機台數往上疊；第二季法說提到 GAA 廠每座廠的 VeraFlex 台數在增加。方向證據：Gartner 報告顯示 Nova 連兩年份額增約 400 個基點，是子市場第二大（管理層轉述，非整體份額）；Onto 的 10-K 也把 KLA 與 Nova 列為薄膜與 OCD 量測的主要對手。同業利潤差（投入資本口徑缺，暫以營益率代替 ROIC）：Nova 29.0%，落後 KLA 的 41.7% 共 12.7 個百分點，領先 Onto 的 13.8% 共 15.2 個百分點、領先 CAMT 的 23.2% 共 5.8 個百分點。這組數字只有單一 TTM 時點，差距走向事實表未涵蓋，所以合併分不給到 8。執行力給 8 分：連兩季落在財測上緣，2022 年目標模型的營收提早約一年達成，ELIPSON 與 WMC 拿到頂級代工廠的量產指定。定價權給 7 分：毛利率 2022–2025 年都在 55.5–57.6%，2023 年下行時仍有 56.6%；但第二季 GAAP 56.5% 低於前一季與去年同季，財務長承認客戶越大折扣越高，被問到重新定價時沒有正面回答。綜合來看，執行力仍在擴大、定價權穩定；再加上 Onto 新平台已在第二代 GAA 與 HBM 拿到量產單、中國本土廠在追趕，整體判穩定。","fact_refs":["f_peer_nvmi_gross_margin_pct","f_peer_nvmi_operating_margin_pct","f_peer_nvmi_fcf_margin_pct","f_peer_klac_gross_margin_pct","f_peer_klac_operating_margin_pct","f_peer_klac_fcf_margin_pct","f_peer_onto_gross_margin_pct","f_peer_onto_operating_margin_pct","f_peer_onto_fcf_margin_pct","f_peer_camt_gross_margin_pct","f_peer_camt_operating_margin_pct"],"verdict_values":{"moat":{"mechanism":"量測模型與配方綁進客戶每一層製程的量產指定機台，同一世代內轉換成本高；再用材料、化學、封裝量測擴大每座廠的機台數。","execution":8,"pricing":7,"grade":"B","trend":"→","trend_evidence":"份額：Gartner 子市場連兩年增約 400 個基點（第一季法說轉述），代表執行力仍在擴大。價格：毛利率 2022–2025 年落在 55.5–57.6%，第二季 GAAP 56.5% 年減 1.3 個百分點，代表定價權穩定、略弱。對手：Onto 新平台在第二代 GAA 拿到量產單，中國本土廠在追趕。三者合併判穩定。","competitor_notes":[{"name":"KLAC","strategy_note":"全產品線龍頭，TTM 營益率 41.7%、毛利率 61.3%，都高於 Nova；研發占營收 11.3%，低於 Nova 的 16.1%，可見 Nova 是用更高的研發投入換份額。"},{"name":"ONTO","strategy_note":"OCD 與整合量測的直接對手，TTM 營益率 13.8%。新 OCD 平台已拿到第二代 GAA 與 HBM 量產單，並與 Rigaku 合作做 X 光混合量測，是下一世代招標的主要挑戰者。"},{"name":"CAMT","strategy_note":"以先進封裝檢測為主，TTM 營益率 23.2%；與 Nova 的 WMC 在封裝量測有重疊，先進封裝放緩時兩家會同時受影響。"},{"name":"中國本土量測廠","strategy_note":"管理層承認對方正在追趕，目前仍有技術差距；對方以擁有成本與在地供應搶中國市場。"}],"threats":[{"level":"🟡","text":"Onto 新一代 OCD 平台已在第二代 GAA 邏輯與 HBM 用 DRAM 拿到多家量產訂單，並與 Rigaku 合作 X 光加光學的混合量測。下一世代招標屬點對點競爭。","p":"40%","evidence_refs":["substitute_technology#1"]},{"level":"🟡","text":"中國本土量測廠在追趕，花旗會議上的財務長與第一季法說的執行長都承認這一點；中國約占營收 30%，目前仍有技術差距。","p":"35%","evidence_refs":["geo_supply_chain#2","reg_tariff_export#1"]},{"level":"🟡","text":"KLA 可能以全產品線綑綁供貨。本期沒有新證據，維持前份的監測門檻：出現整合方案公告，且 Nova 營收連兩季季減。","p":"15%","evidence_refs":[]}],"roic_durability":{"quadrant":"高利益率×高周轉（周轉為推斷：資本支出約占營收 1%，投入資本口徑事實表未涵蓋）","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者是製程工程師，決策者是晶圓廠的製程整合與良率團隊，付款者是晶圓廠資本支出，三個角色都成立。GAA、先進封裝、混合鍵合讓每片晶圓的量測次數增加（Yole：2025 年量測與檢測成長 15%，約占 WFE 14%）。這是「需要」而不是「想要」，沒有量測就過不了良率門檻；但付款時點跟著資本支出週期走、可以延後，所以需求持久但不平穩。"},{"item":"決策層級","level":"🟡","text":"替代性要在「每一層製程的量產指定機台」這個層級衡量。一旦選定，換供應商要重做模型與認證，同一世代內很少換；但每個新世代都會重新招標，而 Onto 的新 OCD 平台已在第二代 GAA 與 HBM 拿到量產單。代理變數：Nova 自報 ELIPSON、WMC 獲頂級代工廠量產指定，交期 4–12 個月。"},{"item":"價值鏈分配","level":"🟡","text":"量測與檢測約占 WFE 14%，Nova 排在 KLA 之後居第二。客戶是少數巨型晶圓廠，第二季有兩家各占產品營收 10% 以上，財務長也承認客戶越大折扣越高。Nova 營益率 29%、KLA 42%，同一個價值鏈環節裡，利潤多數被龍頭拿走。"},{"item":"社會容忍度","level":"🟡","text":"量測設備不是民生品，沒有社會面的定價天花板；真正的上限在政治面。中國約占營收 30%，出口許可與關稅可以直接切掉這塊市場（20-F 風險因素）；營運又集中在以色列、美國、德國。"}],"roiic":"代理值約 3.2 倍：FY2022→FY2025 淨利增加 1.19 億美元，除以 FY2022–FY2024 淨利中未轉成自由現金流的累計 0.377 億美元","reinvest_rate":"代理值約 11%：FY2022–FY2025 自由現金流 6.41 億美元除以淨利 7.20 億美元＝0.89，未轉成現金的 11% 視為再投入（研發約占營收 16%，屬費用化，不在此式內）","endo_ceiling":35,"formula_note":"內生成長＝增量報酬×再投資率。投入資本與折舊攤銷事實表未涵蓋，改用淨利與自由現金流代理。淨利含 17 億美元現金的利息收入，會高估增量報酬；2023 年淨利基期偏低也會放大結果。因此只取方向性結論：成長受需求限制而非資本限制，天花板不構成約束。"}}}},"q3_growth":{"verdict":"第五年後跑道判寬（🟢）。先進封裝已從近乎零長到產品營收約四分之一，混合鍵合與面板級封裝還在認證中，材料量測尚未進入封裝。但 2026 年的成長靠 WFE 的量，不是靠量測密集度。","reasoning":"成長組成：以量為主（晶圓廠擴產），份額為輔，再由營運槓桿放大；回購規模小，併購尚未發生。共識 EPS：FY2026 10.67、FY2027 13.66、FY2028 16.59（Koyfin 2026-10-08；分析師家數事實表未涵蓋），FY1→FY3 年化 24.7%。若以 FY2025 GAAP 7.96 為基期，三年年化是 27.7%；但基期是 GAAP、共識判為非 GAAP，口徑不一會高估。內生天花板代理值約 35%（見護城河段），共識落在天花板內，不需要靠估值重評。不過其中營運槓桿占了一大塊：第二季非 GAAP 營益率 33%，FY2025 GAAP 只有 28.8%，再往上的空間受目標模型 28–33% 上緣限制，所以 FY2028 之後 EPS 成長會回到營收成長附近。跑道：量測約占 WFE 14%、Nova 份額約 18%（未驗證），不是滲透率故事，跑道年數改看 WFE 成長加份額。Yole 估 WFE 至 2031 年年化約 9%，Nova 若每年多 3–5 個百分點，5 年後仍有雙位數成長。衰退訊號只亮一個：FY2022→FY2025 EPS 年化 21.9%、營收 15.6%，差 6.3 個百分點，來自營運槓桿加現金利息收入。毛利率年減目前只有第二季一季，尚未連兩季。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_3m_fy1_pct","f_kpi7_guidance_q3_2026","f_kpi2_non_gaap_operating_margi"],"verdict_values":{"growth":{"driver_mix":"以量為主（晶圓廠擴產與製程轉換），份額為輔，營運槓桿放大；回購與併購目前貢獻很小","runway_years":"不適用滲透率口徑：份額約 18%（未驗證），以 WFE 年化約 9% 加份額增長估算，5 年後仍有雙位數成長","runway_post_y5":"🟢","endo_ceiling_basis":"引用護城河段的代理值約 35%。共識 FY1→FY3 EPS 年化 24.7%，低於天花板，不存在缺口；但成長主要來自 WFE 的量與營運槓桿（第二季非 GAAP 營益率 33%，對比 FY2025 GAAP 28.8%），屬週期順風，不是再投資的成果。","segments":[{"item":"產品營收（第二季）","value":"2.015 億美元；邏輯／代工 73%、記憶體與其他 27%"},{"item":"服務營收（第二季）","value":"0.535 億美元，連續創紀錄；毛利率低於產品，但隨裝機規模有槓桿"},{"item":"先進封裝","value":"約占第二季產品營收 25%；2025 年約 20%，當年年增逾 60%"},{"item":"記憶體","value":"今年約占 30%，以 DRAM 為主；NAND 以升級為主，量測需求偏弱；長期模型為邏輯 60、記憶體 40"},{"item":"中國","value":"約占營收 30%，名目金額仍成長，占比下滑；管理層預期長期落在 25–30%"}],"decay_signals":["EPS 成長高於營收成長逾 5 個百分點：FY2022→FY2025 EPS 年化 21.9%、營收 15.6%（亮）","毛利率年減：第二季 GAAP 56.5% 對去年同季 57.8%，目前只有一季（未亮，監測第三季）","核心市占：Gartner 子市場連兩年增約 400 個基點（未亮）","自由現金流／淨利：FY2022 0.70、FY2023 0.78、FY2024 1.19、FY2025 0.84，沒有連兩年低於 0.75（未亮）","SBC 約占營收 2.7%（未亮）","產業估值倍數三年走勢：事實表未涵蓋"],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"現金堆得高，配置成效待證。17 億美元現金的首要用途是併購，但沒有已實現報酬可以驗證；回購新授權最多 2 億美元；SBC 稀釋輕。第二季自由現金流只有營業利益的一半，屬擴產期的營運資金墊款。","reasoning":"自由現金流／淨利：FY2022 0.70、FY2023 0.78、FY2024 1.19、FY2025 0.84，四年合計 0.89。第二季推算自由現金流 3,842 萬美元（營業現金流 4,092 萬減資本支出 249 萬），只有 GAAP 營業利益 7,619 萬的約五成，原因是營收季增 8% 時墊了營運資金，需要第三、四季回補。SBC 占 GAAP 營業利益 8.9%，每季約 678 萬美元，約占營收 2.7%。以 FY2025 淨利 2.59 億美元除以稀釋 EPS 7.96 推得約 3,260 萬股、市值約 115 億美元，年化 SBC 稀釋約 0.24%，低於 1.5% 門檻。近三年現金去向的四項金額（研發、資本支出、併購、回購）事實表未涵蓋。先前 1 億美元回購已完成，但執行均價未揭露；新授權 2 億美元視估值執行，約占市值 1.7%。併購是首要用途，但收購對價與收購後的報酬事實表未涵蓋，無法驗證。事實表也未見股息。","fact_refs":["f_kpi5_free_cash_flow_40_92_cap","f_kpi6_sbc_gaap","f_kpi3_gaap_operating_income"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":true,"passed":null,"input":"財務長在花旗會議稱併購是首要用途；過去收購（ancosys 等）的對價與收購後利潤貢獻事實表未涵蓋，只能證明 ancosys 營收創紀錄"},{"name":"buyback_yield","applicable":true,"passed":null,"input":"前一筆 1 億美元回購的均價未揭露；以現價計，FY1 盈餘殖利率約 3.0%（10.67÷353）、FY2 約 3.9%。10 年期殖利率事實表未涵蓋，無法判斷是否過關"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"SBC 每季約 678 萬美元（GAAP 營業利益 7,619 萬 × 8.9%），年化約 2,700 萬；對推算市值約 115 億美元，稀釋約 0.24%／年，低於 1.5%。股數為淨利除以 EPS 的推算值"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購或回購撐：營收成長來自晶圓廠資本支出，回購授權約占市值 1.7%；近三年現金去向金額事實表未涵蓋"}}}},"q5_valuation":{"verdict":"353 美元的價格要求三件事：FY2027–28 共識兌現、2029 年後不出現深度衰退、終端仍給 24 倍以上，這樣才有約 8–9% 的年化報酬。這是合理價，不是便宜價。我只信一半，因為 2027 年量測密集度回升還沒有證據。","reasoning":"現價 353 美元相當於 FY1 共識 10.67 的 33.1 倍、FY2 13.66 的 25.8 倍、FY3 16.59 的 21.3 倍。追蹤本益比 44.1 倍、P/S 12.0 倍、EV/S 11.7 倍，在近四個年度端點裡分別位於 100%、88%、78% 分位（不是五年分位）。共識 FY1→FY3 年化 24.7%，PEG 為 1.34（FY1）與 1.05（FY2），落在合理區間。反推來看：要拿到 10% 年化，FY2031 EPS 要到約 22 美元並給 26 倍，等於 FY2028 共識兌現後還要再年化成長約 10% 三年，而且中間沒有像樣的衰退年。我的基準情境是 21.5 美元、24 倍，對應年化約 8–9%。半年跌 29% 的期間，FY1 共識反而上修 1.7%，FY2、FY3 沒有變，所以這次下跌是倍數收縮：市場正在把它從「兩倍 WFE 的成長股」改估成「跟著 WFE 走的循環股」。9 月花旗會議上管理層自己不再重申超額成長，所以這次改估有根據。賣方目標價平均約 491 美元，最高 640、最低 240，全距 2.7 倍，分歧出在估值框架，我不據此給溢價。同業本益比事實表未涵蓋。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_pe_current","f_pe_percentile","f_ps_current","f_ps_percentile","f_ev_s_current","f_ev_s_percentile","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_fy1_pct","f_consensus_rev_fy2_pct","f_consensus_rev_fy3_pct","f_consensus_rev_3m_fy1_pct","f_week26_return_pct"],"verdict_values":{"valuation":{"basis":"Fwd P/E 與 PEG（FY1、FY2）；同業倍數資料缺","tier":"量測設備第二大廠","peers":{"expanded":false,"reason":"同業本益比事實表未涵蓋，只有同業利潤率，因此無法展開。終端倍數改以自身倍數區間為錨，並參考前份所述量測同業中位數約 35 倍（2026-05 的舊數）；此缺口已回報"},"fwd_pe":33.08,"peg":1.34,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"FY1 本益比 33.1 倍、FY2 25.8 倍；PEG 1.34（FY1，對應 FY1→FY3 年化 24.7%）落在 1–2 的合理區間。追蹤本益比仍是近四個年度端點的最高值，五年連續分位事實表未涵蓋，所以判合理偏貴（🟡），不是便宜。短期上檔 8.4%＝FY2027 共識 13.66 × 28 倍（一年後倍數從今天的 33 倍收斂）÷353−1；中期上檔 20.4%＝基準情境 FY2029 的 17.0 × 25 倍 ÷353−1（三年）。","upside_short_pct":8.4,"upside_mid_pct":20.4,"denominator_disputed":false,"denominator_note":"分母是共識非 GAAP EPS。第二季 GAAP EPS 2.20、非 GAAP 2.51，差約 12%；營業利益差額 906 萬美元中，SBC 約占 678 萬，屬常態調整，不構成爭點"}}},"q6_how_wrong":{"verdict":"最可能看錯的地方，是把週期順風當成結構成長。2026 年量測密集度已經下降，2027 年回升只有管理層的說法；價值陷阱風險判黃。","reasoning":"有三種可能看錯的方式。第一是週期：WFE 已經連兩年有 20% 以上的擴張預測，客戶拉貨、「能見度前所未見」、供應鏈吃緊，都是擴張中後段的說法；2023 年下行時營收只跌 9.3%，但那只是單一年度樣本，不代表下一次的跌幅。第二是中國：約占營收 30%，出口限制或本土替代任一發生，都是唯一致命點等級的衝擊。第三是毛利率與定價：第二季毛利率年減，大客戶折扣較高，重新定價的問題管理層沒有回答。最大回撤推導：下行年 EPS 10.5–11 美元，乘以 18–21 倍，得 190–231 美元，較現價跌 35% 到 46%；區間取 −35%～−50%，把極端情況也涵蓋進去。韌性方面：2023 年下行時 GAAP 營益率仍有 25.5%、自由現金流利潤率 20.5%，手上還有 17 億美元現金。五項體質檢查過了四項：下行年自由現金流為正、淨現金、下行年毛利率穩定、下行年營益率 ≥25%；沒過的是中國占比 30%。衰退訊號只亮一個（EPS 成長高於營收逾 5 個百分點），因此判黃。","fact_refs":["f_week26_return_pct","f_price_at_dd","f_rsi14","f_kpi4_gaap_operating_margin"],"verdict_values":{"trap":{"verdict":"🟡","label":"營運槓桿與利息收入墊高 EPS，週期位置偏中後段"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":10.67,"pe":33.08,"basis":"FY2026E 共識非 GAAP EPS（Koyfin 2026-10-08），股價 353 美元；終端倍數同樣採「股價÷當年度 EPS」口徑"},"eps":{"bull":[14.8,18.5,21.0,24.0,27.5],"base":[13.66,16.59,17.0,19.0,21.5],"bear":[12.0,10.5,11.0,12.0,13.0]},"pe":{"bull":28,"base":24,"bear":18},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0,"net_buyback":0.6},"second_stage":{"bull_cagr_pct":14,"base_cagr_pct":10},"max_dd":{"lo":-50,"hi":-35,"basis":"下行年 EPS 10.5–11 美元（Bear 路徑的 2028–29 年）乘以 18–21 倍，得 190–231 美元，較現價跌 35% 到 46%。上緣取 −35%，下緣取 −50%，涵蓋倍數壓到 17 倍的極端情況。股價半年已跌 29%、較前份判斷時的價格低 36.5%，這裡的回撤是從已經下跌後的位置再往下算。","trigger_time":null},"basis":{"bull":"2027 年 2 奈米與 GAA 讓量測密集度回升，先進封裝與混合鍵合放量，營收成長持續高於 WFE 5 個百分點以上；2029 年只放緩不衰退，新目標模型上移營益率；終端 28 倍。","base":"FY2027–28 用共識 13.66、16.59。2029 年 WFE 經過三年擴張後進入消化，EPS 只增 2.5%；2030–31 年隨 WFE 約 9% 的成長加上份額，回到 12–13% 成長。終端 24 倍，低於今天的 33 倍（FY1），約是前份所述量測同業中位數約 35 倍的七成；同業現值倍數事實表未涵蓋。","bear":"2027 年量測密集度沒有回升，中國本土替代加速；2028 年 WFE 進入消化，EPS 跌回 10.5 美元，之後緩慢回升，2031 年 13.0 美元仍低於 FY2027 共識。終端 18 倍，對應成長熄火、降至 10% 情境下的倍數。"},"endo_ceiling_exceeded":false},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"2026 年量測密集度下降，NAND 長期低迷；若先進封裝投資放緩，WMC 與 Prism 的利用率會不足。中國約占 30% 營收，同時面對本土替代與出口限制。","assumption":"2027 年 2 奈米與 GAA 的組合讓量測密集度回升，且 WFE 擴張延續到 2028 年。","consequence":"如果 2028–29 年 WFE 消化與中國替代同時發生，EPS 會回到 10–11 美元、倍數 18 倍，股價約 190–200 美元，較現價跌約 45%。","ruling":"採納，Bear 機率給 30%。這條與唯一致命點部分重疊（中國）；中國以外的週期風險，另由 WFE 門檻監測。","watch":"WFE 季度年增、中國營收占比、FY2027 共識修正","evidence_refs":["supply_demand_durability#4","reg_tariff_export#1","geo_supply_chain#2"]},{"view":"論點成功但股東經濟變差","evidence":"17 億美元現金的首要用途是併購，篩選標準只講綜效；大客戶折扣較高，材料與人力成本上升；第二季自由現金流 3,842 萬美元，只有 GAAP 營業利益 7,619 萬的一半。","assumption":"成長兌現的同時，現金會以不低於自有業務的報酬再投入，或回饋給股東。","consequence":"如果以高倍數收購稀釋報酬，或毛利率被大客戶議價壓到 57% 以下，EPS 仍會成長，但每股價值的成長會落後。","ruling":"採納。資本配置三項檢查中只有 SBC 一項確定過關；併購公告金額若超過市值 5%，就重做這份判斷。","watch":"併購公告金額與付出的倍數、非 GAAP 毛利率、回購執行均價","evidence_refs":["end_markets#2"]},{"view":"論點成功但股東經濟變差","evidence":"第一季法說提到 Nova 獲 Intel 供應商獎，可以證明 Intel 是客戶，但占比未揭露。Intel 在 2025 年被兩家評等機構降到 BBB。","assumption":"GAA 大客戶的財務狀況足以支撐 2027 年的產能計畫。","consequence":"大客戶財務吃緊時，會延後 GAA 產能或壓價，Nova 的成長會被遞延、毛利率受壓。","ruling":"部分採納。占比未知，不改情境假設，只設觸發條件。","watch":"占營收 10% 以上客戶的先進製程資本支出指引","evidence_refs":["customer_concentration_credit#3"]},{"view":"價格已反映太多","evidence":"追蹤本益比 44.1 倍，仍是近四個年度端點的最高值；P/S 12 倍。賣方目標價下修（花旗 595→550、Needham 640→570），最低 240 美元（Jefferies）。","assumption":"FY2027–28 共識 EPS 13.66、16.59 能兌現，且倍數不再往循環股的估法壓縮。","consequence":"如果市場改用循環股估法（尖峰 EPS 給 15–18 倍），FY2028 16.59 × 18 約 299 美元，較現價跌 15%。","ruling":"部分反駁：FY2 本益比 25.8 倍、PEG 約 1.3，已經不算高估。但賣方目標價全距 640 比 240 是 2.7 倍，超過 2.5 倍，代表分歧出在估值框架（成長股還是循環股），所以不給溢價，也不加大倉位。","watch":"賣方目標價中位數、FY2028 共識","evidence_refs":["capital_markets_pricing#2"],"fact_refs":["f_pe_current","f_pe_percentile"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 556.11 → 本次 353.0（-36.5%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=556.11","side_b":"本次 price_at_dd=353.0","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"一致判斷：短期需求","cause":null,"prior_field":null,"side_a":"管理層：第三季財測高於共識，2027 年仍是成長年","side_b":"SEMI 與 Yole：2026–2028 年 WFE 連續成長","ruling":"兩邊一致：短期需求沒有爭議。真正的爭點在 Nova 能不能跑贏 WFE，以及週期何時轉折。","evidence_level":"公司財測加上兩家第三方產業預測","settle_metric":"第三、四季營收落在財測區間的哪個位置","if_then":[],"evidence_refs":["end_markets#3","supply_demand_durability#2"]},{"axis":"2026–2027 年相對 WFE 的超額成長","cause":null,"prior_field":null,"side_a":"2026-05-14 第一季法說，執行長預期 WFE 中雙位數成長，Nova 表現會優於這個數字","side_b":"2026-09-08 花旗會議，財務長說今年看不到慣常的超額表現；第二季法說摩根士丹利分析師依財測算出產品成長約 20% 出頭，低於 WFE","ruling":"⚖ 不可調和，採 B 側：時間較新、出自財務長，也與財測算術一致；2027 年回升只是管理層預期，沒有訂單數字佐證。現在就買的最強論證是：共識 EPS 三個月上修 1.7%、FY2 本益比 25.8 倍、價格已低於前份的進場區。但這個論證押的正是尚未證實的 2027 年回升，所以不採。","evidence_level":"管理層前後說法加上財測算術","settle_metric":"FY2026 全年營收年增對 WFE 年增；2027 年投資人日公布的成長目標","if_then":["若第四季財報（2027-02）與投資人日給出 2027 年營收成長高於 WFE 5 個百分點以上 → 首倉 2%","若 2027 年上半年營收年增仍落後 WFE → 不建倉，H1 判削弱，Bear 機率升至 35%","若價格先漲回 450 美元以上而證據未到 → 不追"],"evidence_refs":["supply_demand_durability#0","end_markets#6"]},{"axis":"訂單能見度","cause":null,"prior_field":null,"side_a":"第二季法說：執行長稱本輪能見度與客戶親密度前所未見，部分 2027 年訂單已經入帳","side_b":"花旗會議：被問到訂金時，財務長說交期與條款都沒改；公司也不揭露在手訂單","ruling":"可調和，屬程度差異。能見度改善是真的，但沒有量化，只能當軟證據，不據此上調任何情境的 EPS。","evidence_level":"管理層定性說法，沒有在手訂單數字","settle_metric":"第三、四季營收是否落在財測上半部；公司是否開始揭露在手訂單","if_then":["若第四季營收財測中點低於 3.0 億美元 → 能見度說法降級，取消首倉計畫","若第三、四季營收都落在財測上半部 → 維持基準情境，不上調機率"],"evidence_refs":[]},{"axis":"毛利率與定價權","cause":null,"prior_field":null,"side_a":"財務長：57–60% 的毛利率模型完好，第三季財測非 GAAP 59%","side_b":"第二季 GAAP 毛利率 56.5%，低於第一季 57.7% 與去年同季 57.8%；非 GAAP 58% 比財測低約 90 個基點。花旗會議上管理層也承認大客戶折扣較高、材料與人力成本上升，並且沒有正面回答定價問題","ruling":"可調和：單季差異屬產品組合因素。但大客戶折扣是結構性的，納入第三、四季的毛利率監測。","evidence_level":"財報實績加上管理層說法","settle_metric":"第三季非 GAAP 毛利率","if_then":["若第三季非 GAAP 毛利率 ≥58.5% → 判為單季組合因素，定價權維持 7 分","若第三、四季非 GAAP 毛利率都低於 57% → 減碼至半倉（若已持有），定價權降至 6 分"],"evidence_refs":["end_markets#2"]},{"axis":"產業態勢三軸","cause":null,"prior_field":null,"side_a":"競爭面在惡化：Onto 新平台拿到第二代 GAA 與 HBM 量產單，中國本土廠在追趕","side_b":"結構面在轉好：GAA 與先進封裝讓量測次數增加，量測約占 WFE 14%；另有其他結構變數：出口限制與關稅會直接影響約 30% 的中國營收","ruling":"判雙向拉鋸：結構面轉好有 Yole 的市場數字佐證，競爭惡化有 Onto 量產訂單佐證，兩者同時成立，所以護城河判穩定，不判擴大。","evidence_level":"第三方產業報告加上同業公告","settle_metric":"2027 年第二代 GAA 的量產指定機台歸屬","if_then":[],"evidence_refs":["supply_demand_durability#3","substitute_technology#1","reg_tariff_export#1"]},{"axis":"估值結論與訊號等級漂移","cause":"價格變動","prior_field":["val","signal","ev5y_pct","irr_base_pct","asym_ratio","bull_5y_price","bear_5y_price"],"side_a":"前份（2026-05-15）：股價 556.11 美元、Fwd P/E 54 倍、PEG 2.43，估值判為最貴一級，等級 B","side_b":"本次：股價 353 美元（−36.5%）、Fwd P/E 33.1 倍（FY1）、25.8 倍（FY2），共識 EPS 沒有下修，估值改判合理偏貴；等級維持 B。情境樹的報酬與上下檔價格因起點價格改變全部重算","ruling":"估值改善完全來自股價下跌，基本面判斷不變，所以等級不動。","evidence_level":"價格與共識快照","settle_metric":"FY2 本益比","if_then":[],"evidence_refs":[]},{"axis":"判斷方法補齊","cause":"方法變動","prior_field":["trap","runway_post_y5","archetype","cycle_position","p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份價值陷阱判綠，沒有填成長跑道、公司類型、週期位置、情境機率與最大回撤；定期定額判斷為空","side_b":"本次逐項掃描十類衰退訊號：FY2022→FY2025 EPS 年化 21.9%、營收 15.6%，差 6.3 個百分點，亮一燈，陷阱改判黃。跑道判綠（先進封裝是第二條曲線）；類型判品質複利成長兼循環；週期在中段；情境機率 25／45／30；最大回撤 −35%～−50%。定期定額判斷由程式另算","ruling":"陷阱由綠轉黃不是新的負面事實，而是改用逐項掃描的結果；所依據的年度數字前份就已存在。","evidence_level":"年度財報","settle_metric":"第三季毛利率是否形成連兩季年減","if_then":[],"evidence_refs":[]},{"axis":"護城河走向","cause":"新證據","prior_field":["moat_trend"],"side_a":"前份：執行力擴大、定價權穩定（兩個維度分歧），KLA 整合三平台列為生態攻擊","side_b":"本次合併判穩定：份額仍在增加（Gartner 連兩年），但 Onto 新平台拿到第二代 GAA 與 HBM 量產單，中國本土廠在追趕，第二季毛利率年減，2026 年也沒有跑贏 WFE","ruling":"採 B 側。KLA 整合攻擊從前份的紅色降為黃色，因為本期證據裡沒有任何 KLA 整合方案的消息；監測門檻保留在 R3。","evidence_level":"同業公告、財報、管理層說法","settle_metric":"2027 年第二代 GAA 的量產指定機台歸屬、非 GAAP 毛利率","if_then":[],"evidence_refs":["substitute_technology#1","end_markets#2"]},{"axis":"進場條件改錨","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"等 BB 中軌約 461 美元，或 FPE 修復至 35–40 倍（約 362–415 美元）再評估進場","side_b":"第四季財報或 2027 年投資人日證實 2027 年營收成長高於 WFE 5 個百分點以上，且非 GAAP 毛利率 ≥58% 時進場首倉","ruling":"前份的價格條件已經觸發（Fwd P/E 33.1 倍、價格 353 美元低於 362 美元）。但花旗會議透露今年沒有超額成長，真正卡住進場的約束變成「2027 年量測密集度回升未獲證實」，而不是價格，所以進場條件從價格錨改為事件錨。","evidence_level":"價格快照加上管理層說法","settle_metric":"2027 年營收成長對 WFE 成長","if_then":[],"evidence_refs":[]},{"axis":"Single Thing 設定","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設 Single Thing（唯一致命點為空）","side_b":"美國或以色列把量測設備對中國的出口納入全面許可或禁售，Nova 中國營收（約 30%）在一年內大幅萎縮；一旦發生即清倉或取消建倉","ruling":"中國是數學上最大的單一敏感度：約占營收 30%，在營益率約 30% 的槓桿下，對 EPS 的衝擊超過任何單一競爭事件。","evidence_level":"20-F 風險因素加上第三方營收結構估計","settle_metric":"出口管制公告、每季中國營收占比","if_then":[],"evidence_refs":["reg_tariff_export#0"]},{"axis":"減碼與清倉門檻","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份風險表：WFE 年增 <0% 連四季大動作減倉；Fwd P/E >60 倍減倉；90 天共識下修 >5% 重評","side_b":"本次：WFE 年增連兩季 <0% 警戒、連四季減碼至半倉；非 GAAP 毛利率連兩季 <57% 減碼至半倉；FY2027 共識 EPS 90 天下修 >5% 取消首倉計畫；中國量測設備全面禁售即清倉；WFE 連四季負成長且 Nova 營益率 <25% 即清倉","ruling":"Fwd P/E >60 倍的減倉門檻退休：倍數已從 54 倍降到 33 倍，離門檻太遠，失去作用。改用毛利率與共識修正這兩個基本面門檻；WFE 與共識修正兩條保留，前者的「重評」改成具體動作。","evidence_level":"門檻設計變更","settle_metric":"各門檻每季檢查","if_then":[],"evidence_refs":[]},{"axis":"假設門檻改寫","cause":"新證據","prior_field":["thesis.H"],"side_a":"前份 H1：Nova 營收年增 ≥ WFE 年增加 10 個百分點，連續 8 季","side_b":"本次 H1：FY2027 營收年增 ≥ WFE 年增加 5 個百分點；FY2026 落後 WFE 記為削弱起點","ruling":"管理層已不再重申兩倍 WFE，2026 年實績也低於 WFE，舊門檻實質上沒有達到；沿用舊門檻就等於宣告 H1 反轉。改用可驗證的 2027 年單年門檻，並把 2026 年未達標如實記為削弱。","evidence_level":"管理層說法加上財測算術","settle_metric":"FY2027 營收年增對 WFE 年增","if_then":[],"evidence_refs":[]}],"triggers":[{"n":1,"text":"第三季財報：檢查非 GAAP 毛利率與第四季財測","type":"複審日期","maps_to":"R4","metric":"非 GAAP 毛利率；第四季營收財測中點","threshold":"毛利率 ≥58%，第四季財測中點 ≥3.0 億美元","action":"兩項都達標且沒有新增出口限制 → 列為首倉候選；任一未達 → 維持觀望","source_freq":"季報","date":"2026-11"},{"n":2,"text":"2027 年投資人日與第四季財報，驗證 2027 年量測密集度回升","type":"假設驗證","maps_to":"H1","metric":"2027 年營收成長指引或目標對 WFE 成長","threshold":"FY2027 營收年增 ≥ WFE 年增加 5 個百分點","action":"成立 → 首倉 2%；不成立 → 不建倉，H1 判削弱","source_freq":"一次性事件加季報","date":"2027-03"},{"n":3,"text":"價格先跌、基本面沒有受損時的分批反買","type":"估值rearm","maps_to":"H1","metric":"股價；FY2027 共識 EPS 90 天修正","threshold":"股價 <300 美元（FY2 本益比約 22 倍），且共識下修不超過 5%","action":"分批反買首倉 1%，其餘等第 2 條觸發","source_freq":"每日價格、月度共識快照","date":null},{"n":4,"text":"2027 年上半年驗證第二條成長曲線","type":"加碼","maps_to":"H2","metric":"上半年營收年增對 WFE；先進封裝占產品營收","threshold":"營收年增高於 WFE，且先進封裝占比 ≥25%","action":"加碼至 4%","source_freq":"季報","date":"2027-08"},{"n":5,"text":"共識下修","type":"減碼","maps_to":"R1","metric":"FY2027 共識 EPS 90 天修正","threshold":"下修逾 5%","action":"取消首倉計畫；已持有則減碼至半倉","source_freq":"月度共識快照","date":null},{"n":6,"text":"關稅或零組件成本吸收失敗","type":"風險","maps_to":"R4","metric":"非 GAAP 毛利率","threshold":"連兩季 <57%，且管理層歸因於關稅或零組件成本","action":"減碼至半倉","source_freq":"季報","date":null,"evidence_refs":["end_markets#2","reg_tariff_export#4"]},{"n":7,"text":"中國出口全面限制","type":"Single Thing","maps_to":"Single Thing","metric":"美國或以色列對中國的量測設備出口規定","threshold":"全面許可制或禁售公告涵蓋 Nova 主要產品","action":"清倉或取消建倉，重跑情境樹","source_freq":"事件","date":null,"evidence_refs":["reg_tariff_export#0"]},{"n":8,"text":"中國營收占比急降","type":"風險","maps_to":"R2","metric":"中國營收占比（單季）","threshold":"<20%，且管理層歸因於出口限制或本土替代","action":"減碼至半倉","source_freq":"季報","date":null,"evidence_refs":["reg_tariff_export#1","geo_supply_chain#2"]},{"n":9,"text":"供應鏈卡住出貨","type":"風險","maps_to":"R5","metric":"單季營收對財測下緣","threshold":"任一季低於財測下緣，且歸因於供應","action":"停止加碼一季","source_freq":"季報","date":null,"evidence_refs":["geo_supply_chain#0","geo_supply_chain#1","geo_supply_chain#3"]},{"n":10,"text":"GAA 量產指定機台被換掉","type":"風險","maps_to":"R3","metric":"前四大 GAA 客戶的量產指定機台","threshold":"任一家公告改用 Onto 或 KLA，且產品營收連兩季季減","action":"減碼至半倉，並重評護城河","source_freq":"事件加季報","date":null,"evidence_refs":["substitute_technology#1"]},{"n":11,"text":"大客戶削減資本支出","type":"風險","maps_to":"R1","metric":"占營收 10% 以上客戶的先進製程資本支出","threshold":"任一家宣布下修 ≥20%","action":"停止加碼","source_freq":"客戶財報","date":null,"evidence_refs":["customer_concentration_credit#3","supply_demand_durability#4"]},{"n":12,"text":"週期下行加上營益率失守","type":"清倉","maps_to":"H3","metric":"全球 WFE 年增；Nova GAAP 營益率","threshold":"WFE 連四季負成長，且 Nova 營益率 <25%","action":"清倉","source_freq":"季報；SEMI","date":null}],"kill_metrics":[{"metric":"非 GAAP 毛利率（單季）","bear_threshold":"連兩季 <57%（目標模型 57–60% 下緣）","window":"2026Q3–2027Q2","source":"公司季度財報新聞稿","last_status":"ok"},{"metric":"FY2027 共識 EPS 90 天修正","bear_threshold":"下修逾 5%","window":"滾動 90 天","source":"Koyfin 共識快照","last_status":"ok"},{"metric":"Nova 營收年增減 WFE 年增（TTM）","bear_threshold":"連兩季落後 5 個百分點以上","window":"2026Q4–2027Q4","source":"公司財報；SEMI WFE 統計","last_status":"warning"},{"metric":"中國營收占比（單季）","bear_threshold":"<20%，且管理層歸因於出口限制或本土替代","window":"2026Q4–2028Q4","source":"公司法說；20-F","last_status":"ok"},{"metric":"全球 WFE 年增（季）","bear_threshold":"連兩季 <0% 警戒；連四季減碼至半倉","window":"2027–2029","source":"SEMI","last_status":"ok"}],"evidence_dismissed":[],"action_conditions":{"rearm_trigger":"第四季財報或 2027 年投資人日證實 2027 年營收成長高於 WFE 5 個百分點以上，且非 GAAP 毛利率 ≥58%","exec_line":"觀望。證據到位後首倉 2%；2027 年上半年營收年增高於 WFE 且先進封裝占比 ≥25%，再加至 4%。價格先漲回 450 美元以上而證據未到，不追；跌破 300 美元且 FY2027 共識下修不超過 5%，可分批反買首倉 1%。","holding_cap":"≤4%（週期股、護城河 B、賣方分歧出在估值框架）"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":"中循環","cycle_verdict":"未觸發","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"不等價格，等事件：2027 年投資人日或第四季財報證實 2027 年營收成長高於 WFE。若價格跌破 300 美元且共識下修不超過 5%，可先買 1%。","asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null},"thesis":{"H":[{"id":"H1","text":"2027 年邏輯端轉向 2 奈米與 GAA，量測密集度回升，Nova 營收成長重新跑贏 WFE","2y":"FY2027 營收年增高於 WFE 年增 5 個百分點以上","5y":null,"10y":null,"threshold":"FY2027 營收年增減 WFE 年增 ≥ +5 個百分點；FY2026 落後 WFE 記為削弱起點","source":"公司季報與 2027 年第一季投資人日；SEMI 年度 WFE 統計","drift_rule":"TTM 營收年增落後 WFE 年增達 5 個百分點、連兩季＝削弱；落後達 10 個百分點、連三季＝反轉"},{"id":"H2","text":"先進封裝與化學、材料量測把可服務市場往後段延伸，成為第二條成長曲線","2y":null,"5y":"FY2030 先進封裝營收維持在產品營收 25% 以上，混合鍵合或面板級封裝取得量產訂單，材料量測切入封裝","10y":null,"threshold":"FY2026 全年先進封裝占產品營收 ≥23%；2028 年底前公告混合鍵合量產訂單","source":"季度法說的營收結構；公司的量產指定機台公告","drift_rule":"先進封裝占比連四季比門檻低 5% 以上＝削弱；連六季低 10% 以上＝反轉"},{"id":"H3","text":"穩住 KLA 之後第二大量測供應商的位置，跨一個完整週期守住非 GAAP 毛利率 57–60% 與營益率 25% 以上","2y":null,"5y":null,"10y":"下一個 WFE 衰退年 GAAP 營益率不低於 25%（2023 年實績 25.5%），份額不輸給 Onto 與中國本土廠","threshold":"年度非 GAAP 毛利率 ≥57%；衰退年 GAAP 營益率 ≥25%","source":"年度財報；Gartner 份額報告（目前為管理層轉述，需第三方交叉驗證）","drift_rule":"跨兩個年度非 GAAP 毛利率低於 57%＝削弱；跨三個年度＝反轉"}],"R":[{"id":"R1","text":"經過三年擴張，WFE 在 2028 年後進入消化期，先前的拉貨回吐，NAND 長期低迷","h_ref":"H1","clock":"🔥","threshold":"全球 WFE 年增連兩季 <0%＝警戒；連四季＝減碼至半倉；FY2027 共識 EPS 90 天下修逾 5%＝取消首倉計畫","evidence_refs":["supply_demand_durability#4"]},{"id":"R2","text":"中國約占營收 30%：本土量測廠追趕加上出口限制，名目金額仍成長，但占比下滑可能加速","h_ref":"H3","clock":"🔥","threshold":"中國單季營收占比 <20%，且管理層歸因於限制或本土替代＝H3 削弱","evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","geo_supply_chain#2"]},{"id":"R3","text":"第二代 GAA 與 HBM 的 OCD 重新招標：Onto 新平台已拿到量產單，KLA 也可以綑綁全產品線","h_ref":"H3","clock":"🐢","threshold":"前四大 GAA 客戶任一家公告改換量產指定機台，且產品營收連兩季季減","evidence_refs":["substitute_technology#1"]},{"id":"R4","text":"毛利率被大客戶折扣與零組件成本侵蝕：第二季 GAAP 56.5%，低於前一季與去年同季","h_ref":"H3","clock":"⚡","threshold":"非 GAAP 毛利率連兩季 <57%","evidence_refs":["end_markets#2"]},{"id":"R5","text":"供應鏈與營運集中：工廠在以色列、美國、德國，每條產品線只有單一製造點，部分零件只有唯一供應商；供應吃緊時，交期與出貨會受限","h_ref":"H1","clock":"🔥","threshold":"任一季營收落在財測下緣以下，且管理層歸因於供應","evidence_refs":["geo_supply_chain#0","geo_supply_chain#1","geo_supply_chain#3"]}],"single_thing":{"description":"美國或以色列把量測設備對中國的出口納入全面許可或禁售，Nova 的中國營收（約 30%）在一年內大幅萎縮","why_fatal":"中國約占營收 30%，在營益率約 30% 的營運槓桿下，EPS 可能少三成以上；空出來的市場會由本土廠接手，事後很難收復","if_happens":"清倉或取消建倉；重跑情境樹，Bear 機率升至 45%","how_monitor":"美國商務部的出口管制公告；每季法說的中國營收占比；20-F 風險因素的措辭變化","probability":"約 15%（12–24 個月）"}},"appendix_a":{"growth_durability":7,"quality_score":9,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":25.8,"peg_fy2":1.05,"stress":{"pass":4,"total":5}},"eps_meta":{"base_eps_path":{"FY2025A":7.96,"FY2026E":10.67,"FY2027E":13.66,"FY2028E":16.59},"fy_end_month":12,"eps_basis":"FY2025A 為 GAAP 稀釋 EPS（年度財報）；FY2026E–FY2028E 為 Koyfin 共識，依第二季非 GAAP 2.51 加第三季財測中點 2.775 的推算判為非 GAAP 口徑。兩者口徑不一，非 GAAP 基期事實表未涵蓋"},"catalysts":[{"date":"2026-11","date_precision":"month","type":"guidance","event":"第三季財報與第四季財測","impact":"高","watch":"非 GAAP 毛利率是否回到 58% 以上；第四季財測中點是否 ≥3.0 億美元"},{"date":"2026-12","date_precision":"month","type":"capacity","event":"亞洲首座無塵室投產","impact":"中","watch":"新廠爬坡是否拖累毛利率；交期是否縮短"},{"date":"2027-Q1","date_precision":"quarter","type":"guidance","event":"投資人日公布新的五年目標模型","impact":"高","watch":"營收成長目標相對 WFE 的倍數；毛利率與營益率區間是否上移"},{"date":"2027-Q1","date_precision":"quarter","type":"macro","event":"SEMI 更新 2027 年 WFE 預測","impact":"中","watch":"2027 年 WFE 成長是否維持在 20% 左右"}],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8w(原9)","pacing":[],"holding_cap":null,"audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟢', val='🟡', moat_trend='→', week26=-28.84, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position='中循環', moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":false,"basis":"signal='B', val='🟡'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":true,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"8w","condition":"判斷者宣告 wait_for_price（價格合理但要等）→ 原 row9 進場改觀望（等價格）","hit":true,"basis":"wait_for_price=True, 等待條件='不等價格，等事件：2027 年投資人日或第四季財報證實 2027 年營收成長高於 WFE。若價格跌破 300 美元且共識下修不超過 5%，可先買 1%。'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"requires_critic":[]}}
```

---

## 尾段：回覆格式

只回一個 JSON 陣列，①–⑧ 每條一個元素，八個全出，不得跳號、不得多列，陣列外不得有任何文字（不加前言、不加 markdown 圍欄、不加附註）：

```json
[{"item": "①", "light": "🔴|🟡|🟢", "judgment_path": "$.路徑", "reason": "一句話"}]
```
