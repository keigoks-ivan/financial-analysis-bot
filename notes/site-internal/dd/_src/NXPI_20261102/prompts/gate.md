你是 DD 管線 v20 的判斷層閘（gate），標的 NXPI（20261102）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（49 條）
- `f_kpi0_revenue_gaap`（q1_business）｜Revenue (GAAP)＝3786 USD m｜期間與口徑：Q3 2026（季末 2026-09-27，公告於 2026-10-27）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 NXP Q3 2026 press release https://media.nxp.com/news-releases/news-release-details/nxp-semiconductors-reports-third-quarter-2026-results（SEC 8-K Ex.99.1 同文：https://www.sec.gov/Archives/edgar/data/0001413447/000141344726000057/nxp3q26exhibit991.htm）（numbers.latest_quarter_kpis.items[0]，as_of Q3 2026（季末 2026-09-27，公告於 2026-10-27））
- `f_kpi1_non_gaap_operating_incom`（q1_business）｜Non-GAAP operating income＝1406 USD m｜期間與口徑：Q3 2026（季末 2026-09-27，公告於 2026-10-27）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 NXP Q3 2026 press release https://media.nxp.com/news-releases/news-release-details/nxp-semiconductors-reports-third-quarter-2026-results（SEC 8-K Ex.99.1 同文：https://www.sec.gov/Archives/edgar/data/0001413447/000141344726000057/nxp3q26exhibit991.htm）（numbers.latest_quarter_kpis.items[1]，as_of Q3 2026（季末 2026-09-27，公告於 2026-10-27））
- `f_kpi2_non_gaap_operating_margi`（q1_business）｜Non-GAAP operating margin＝37.1 %｜期間與口徑：Q3 2026（季末 2026-09-27，公告於 2026-10-27）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 NXP Q3 2026 press release https://media.nxp.com/news-releases/news-release-details/nxp-semiconductors-reports-third-quarter-2026-results（SEC 8-K Ex.99.1 同文：https://www.sec.gov/Archives/edgar/data/0001413447/000141344726000057/nxp3q26exhibit991.htm）（numbers.latest_quarter_kpis.items[2]，as_of Q3 2026（季末 2026-09-27，公告於 2026-10-27））
- `f_kpi3_gaap_operating_income`（q1_business）｜GAAP operating income＝1228 USD m｜期間與口徑：Q3 2026（季末 2026-09-27，公告於 2026-10-27）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 NXP Q3 2026 press release https://media.nxp.com/news-releases/news-release-details/nxp-semiconductors-reports-third-quarter-2026-results（SEC 8-K Ex.99.1 同文：https://www.sec.gov/Archives/edgar/data/0001413447/000141344726000057/nxp3q26exhibit991.htm）（numbers.latest_quarter_kpis.items[3]，as_of Q3 2026（季末 2026-09-27，公告於 2026-10-27））
- `f_kpi4_gaap_operating_margin`（q1_business）｜GAAP operating margin＝32.4 %｜期間與口徑：Q3 2026（季末 2026-09-27，公告於 2026-10-27）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 NXP Q3 2026 press release https://media.nxp.com/news-releases/news-release-details/nxp-semiconductors-reports-third-quarter-2026-results（SEC 8-K Ex.99.1 同文：https://www.sec.gov/Archives/edgar/data/0001413447/000141344726000057/nxp3q26exhibit991.htm）（numbers.latest_quarter_kpis.items[4]，as_of Q3 2026（季末 2026-09-27，公告於 2026-10-27））
- `f_kpi7_guidance_q4_2026_revenue`（q1_business）｜Guidance Q4 2026 revenue＝3,750–3,950 USD m｜期間與口徑：Q3 2026（季末 2026-09-27，公告於 2026-10-27）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司新聞稿 NXP Q3 2026 press release https://media.nxp.com/news-releases/news-release-details/nxp-semiconductors-reports-third-quarter-2026-results（SEC 8-K Ex.99.1 同文：https://www.sec.gov/Archives/edgar/data/0001413447/000141344726000057/nxp3q26exhibit991.htm）（numbers.latest_quarter_kpis.items[7]，as_of Q3 2026（季末 2026-09-27，公告於 2026-10-27））
- `f_kpi8_dio`（q1_business）｜DIO（庫存天數）＝148 days｜期間與口徑：Q3 2026（季末 2026-09-27，公告於 2026-10-27）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 NXP Q3 2026 press release https://media.nxp.com/news-releases/news-release-details/nxp-semiconductors-reports-third-quarter-2026-results（SEC 8-K Ex.99.1 同文：https://www.sec.gov/Archives/edgar/data/0001413447/000141344726000057/nxp3q26exhibit991.htm）（numbers.latest_quarter_kpis.items[8]，as_of Q3 2026（季末 2026-09-27，公告於 2026-10-27））
- `f_kpi9_channel_inventory`（q1_business）｜Channel inventory＝11 weeks｜期間與口徑：Q3 2026（季末 2026-09-27，公告於 2026-10-27）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 NXP Q3 2026 press release https://media.nxp.com/news-releases/news-release-details/nxp-semiconductors-reports-third-quarter-2026-results（SEC 8-K Ex.99.1 同文：https://www.sec.gov/Archives/edgar/data/0001413447/000141344726000057/nxp3q26exhibit991.htm）（numbers.latest_quarter_kpis.items[9]，as_of Q3 2026（季末 2026-09-27，公告於 2026-10-27））
- `f_earnings_recency`（q1_business）｜最近一次財報日＝2026-10-27 date｜期間與口徑：2026-10-27／距今 4 個交易日｜kind：realized
  - 來源：—（numbers.earnings_recency，as_of 2026-10-27）
- `f_peer_nxpi_gross_margin_pct`（q2_moat）｜NXPI 毛利率＝56.43 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.NXPI.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_nxpi_operating_margin_pct`（q2_moat）｜NXPI 營業利益率＝28.55 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.NXPI.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_nxpi_fcf_margin_pct`（q2_moat）｜NXPI FCF 利潤率＝24.16 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.NXPI.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_txn_gross_margin_pct`（q2_moat）｜TXN 毛利率＝60.24 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.TXN.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_txn_operating_margin_pct`（q2_moat）｜TXN 營業利益率＝41.12 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.TXN.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_txn_fcf_margin_pct`（q2_moat）｜TXN FCF 利潤率＝35.24 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.TXN.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_adi_gross_margin_pct`（q2_moat）｜ADI 毛利率＝65.8 %｜期間與口徑：TTM ending 2026-07-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ADI.gross_margin_pct，as_of TTM ending 2026-07-31（4季加總））
- `f_peer_adi_operating_margin_pct`（q2_moat）｜ADI 營業利益率＝35.72 %｜期間與口徑：TTM ending 2026-07-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ADI.operating_margin_pct，as_of TTM ending 2026-07-31（4季加總））
- `f_peer_adi_fcf_margin_pct`（q2_moat）｜ADI FCF 利潤率＝35.57 %｜期間與口徑：TTM ending 2026-07-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ADI.fcf_margin_pct，as_of TTM ending 2026-07-31（4季加總））
- `f_peer_stm_gross_margin_pct`（q2_moat）｜STM 毛利率＝33.84 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.STM.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_stm_operating_margin_pct`（q2_moat）｜STM 營業利益率＝6.64 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.STM.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_stm_fcf_margin_pct`（q2_moat）｜STM FCF 利潤率＝3.77 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.STM.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_on_gross_margin_pct`（q2_moat）｜ON 毛利率＝37.72 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ON.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_on_operating_margin_pct`（q2_moat）｜ON 營業利益率＝18.05 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ON.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_on_fcf_margin_pct`（q2_moat）｜ON FCF 利潤率＝24.21 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ON.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝15.16 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-10-31）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝18.32 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-10-31）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝21.48 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-10-31）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝14314.09 USD m｜期間與口徑：2026-11-02／yfinance revenue_estimate 0y 平均（24 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-02）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝16023.45 USD m｜期間與口徑：2026-11-02／yfinance revenue_estimate +1y 平均（28 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-02）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝0.53 %｜期間與口徑：2026-07-30 → 2026-10-31／FY1 共識 EPS 15.08 → 15.16（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-10-31）
- `f_kpi5_non_gaap_free_cash_flow`（q1_business）｜Non-GAAP free cash flow＝1206 USD m｜期間與口徑：Q3 2026（季末 2026-09-27，公告於 2026-10-27）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 NXP Q3 2026 press release https://media.nxp.com/news-releases/news-release-details/nxp-semiconductors-reports-third-quarter-2026-results（SEC 8-K Ex.99.1 同文：https://www.sec.gov/Archives/edgar/data/0001413447/000141344726000057/nxp3q26exhibit991.htm）（numbers.latest_quarter_kpis.items[5]，as_of Q3 2026（季末 2026-09-27，公告於 2026-10-27））
- `f_kpi6_sbc`（q4_capital）｜SBC＝114 USD m｜期間與口徑：Q3 2026（季末 2026-09-27，公告於 2026-10-27）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 NXP Q3 2026 press release https://media.nxp.com/news-releases/news-release-details/nxp-semiconductors-reports-third-quarter-2026-results（SEC 8-K Ex.99.1 同文：https://www.sec.gov/Archives/edgar/data/0001413447/000141344726000057/nxp3q26exhibit991.htm）（numbers.latest_quarter_kpis.items[6]，as_of Q3 2026（季末 2026-09-27，公告於 2026-10-27））
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝7035.0 USD m｜期間與口徑：2026-11-02／yfinance 最新一季：總債務 10978.0、現金 3943.0（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-02）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝1.562 %｜期間與口徑：2026-11-02／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-11-02）
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝252.05 m shares｜期間與口徑：2026-11-02／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-11-02）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_ev_m`（q5_valuation）｜目前企業價值 EV（市值＋淨負債）＝72470.47 USD m｜期間與口徑：2026-11-02／市值 65435.47 ＋ 淨負債 7035.0｜kind：realized
  - 來源：—（numbers.capital_structure.ev_m，as_of 2026-11-02）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝17.12 x｜期間與口徑：2026-10-31／分母＝FY1 EPS 15.16，分子＝快照價 259.61｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-10-31）
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝259.61 USD｜期間與口徑：2026-10-30（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-10-30（RTH 收盤，UTC））
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝20.43 x｜期間與口徑：2026-10-30（RTH 收盤，UTC）／4 個年度端點內的分位＝47.2｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-10-30（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝47.2 %｜期間與口徑：2026-10-30（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-10-30（RTH 收盤，UTC））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝4.74 x｜期間與口徑：2026-10-30（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-10-30（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝100.0 %｜期間與口徑：2026-10-30（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-10-30（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝5.25 x｜期間與口徑：2026-10-30（RTH 收盤，UTC）／4 個年度端點內的分位＝97.8｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-10-30（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝97.8 %｜期間與口徑：2026-10-30（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-10-30（RTH 收盤，UTC））
- `f_ev_s_fwd`（q5_valuation）｜EV/S（EV ÷ FY1 共識營收）＝5.06 x｜期間與口徑：2026-11-02／f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）｜kind：estimate
  - 來源：—（numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m，as_of 2026-11-02）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_consensus_rev_fy1_pct`（q5_valuation）｜FY1 共識修正＝0.0 %｜期間與口徑：2026-10-31／兩份 Koyfin 快照之間的 EPS 修正幅度（15.16 → 15.16）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.fy1.revision_pct，as_of 2026-10-31）
- `f_consensus_rev_fy2_pct`（q5_valuation）｜FY2 共識修正＝0.0 %｜期間與口徑：2026-10-31／兩份 Koyfin 快照之間的 EPS 修正幅度（18.32 → 18.32）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.fy2.revision_pct，as_of 2026-10-31）
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝-11.37 %｜期間與口徑：2026-10-30（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-10-30（RTH 收盤，UTC））
- `f_rsi14`（q5_valuation）｜RSI(14)＝63.84｜期間與口徑：2026-10-30（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-10-30（RTH 收盤，UTC））

### findings_digest 中方向為負或來源衝突的條目（11 條）
- `competitive_share_entrants#0`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K 載明 NXP 與眾多 IDM 及無晶圓廠對手競爭，部分對手比 NXP 大、資源更多，可能造成銷量下滑或價格下降。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-19）｜affects：moat_trend、decision_inputs.bear
- `competitive_share_entrants#2`（competitive_share_entrants｜方向 -｜狀態 ok）：Goldman Sachs 2026 會議摘要：NXP 承認中國本土晶片商在資訊娛樂與低階 MCU 構成競爭，策略鎖定客戶架構而非低階產品；查無 2026 年中國供應商取代高階車用 MCU 的直接證據。
  - 來源：Quartr, NXP Goldman Sachs Communacopia + Technology Conference 2026 summary（as_of 2026-09-01）｜affects：moat_trend、decision_inputs.bear
- `customer_concentration_credit#2`（customer_concentration_credit｜方向 -｜狀態 ok）：風險因子揭露：營收相當比重來自前幾大客戶（含經銷商），主要客戶大幅減量會有重大不利影響。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-19）｜affects：thesis.R、decision_inputs.bear
- `supply_demand_durability#1`（supply_demand_durability｜方向 -｜狀態 ok）：MITRE: significant legacy-chip capacity expansion outside China not expected to begin until 2027; a European procurement source notes Chinese foundries account for nearly 70% of new mature-node capacity expansion in 2026 (relevant to NXP's mature-node/analog exposure).
  - 來源：MITRE, Current and Future State of Legacy Semiconductor Manufacturing Capacity; globx.eu semiconductor shortage 2026（as_of 2024-05-01）｜affects：thesis.R、decision_inputs.bear
- `regulatory_antitrust#0`（regulatory_antitrust｜方向 -｜狀態 ok）：南韓公平交易委員會於2026-07-08對NXP啟動審議：指控其透過Ship & Debit計畫給予經銷商事實上的獨家經銷權並預先設定經銷商利潤；審查官建議改正命令與罰款（上限約相關銷售額4%），NXP相關銷售額約8.8億美元。
  - 來源：Seoul Economic Daily: Global Chipmakers NXP, ADI Face Korea Antitrust Scrutiny（as_of 2026-07-08）｜affects：decision_inputs.bear、thesis.R
- `regulatory_antitrust#2`（regulatory_antitrust｜方向 -｜狀態 ok）：南韓KFTC對NXP、ADI進入審議，NXP被指經銷獨家權與利潤固定
  - 來源：MLex: NXP, Analog Devices face South Korean antitrust deliberations（as_of 2026-07-08）｜affects：decision_inputs.bear
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：NXP FY2025 10-K 風險因子：美國商務部 2025-04 啟動半導體 Section 232 調查，結果未明但預期帶來額外關稅與貿易限制，可能不利其業務；關稅也可能推高原料與設備成本。
  - 來源：SEC EDGAR NXP 10-K FY2025 Item 1A（as_of 2026-02-19）｜affects：decision_inputs.bear、thesis.R
- `reg_tariff_export#1`（reg_tariff_export｜方向 -｜狀態 ok）：NXP 10-K 載明 2020 年因美國政府規定停止對華為出貨（待出口許可），且出口法規趨嚴，客戶或供應商受制裁可能影響需求。
  - 來源：SEC EDGAR NXP 10-K FY2025 Item 1A（as_of 2026-02-19）｜affects：decision_inputs.bear、thesis.R
- `geo_supply_chain#2`（geo_supply_chain｜方向 -｜狀態 ok）：NXP 的 8 吋晶圓廠 SSMC（新加坡）與 TSMC 合資；20-F 並警示 just-in-time 採購使其暴露於供應鏈中斷風險。
  - 來源：NXP Form 20-F FY2018 (SEC)（as_of 2019-02-01）｜affects：decision_inputs.bear、thesis.R
- `capital_markets_pricing#0`（capital_markets_pricing｜方向 -｜狀態 ok）：NXP 2026Q3 財報（10/28-29）給 Q4 營收指引 3.75–3.95 億（應為十億美元）即 $3.75B–$3.95B，中點 $3.85B，年增約 15%、季增約 2%；報導稱略低於分析師預期，盤後股價跌近 8%，分析師點出車用需求趨緩的不確定性。
  - 來源：capital.com / itiger 新聞（NXP Reports Third Quarter 2026 Results；Dips After-Hours...）（as_of 2026-10-29）｜affects：valuation、thesis.R、decision_inputs.bear
- `capital_markets_pricing#4`（capital_markets_pricing｜方向 -｜狀態 ok）：Q4 指引 $3.75B–$3.95B，略低於預期，盤後跌近 8%
  - 來源：itiger 新聞（as_of 2026-10-29）｜affects：valuation、thesis.R

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 6 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/NXPI_20261102/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":660.0,"bear_5y_price":188.5,"p_bull_pct":20,"p_bear_pct":30,"upside_5y_pct":63.7,"ev5y_pct":54.5,"irr_base_pct":10.4,"asym_ratio":3.8,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":15.16,"pe":17.12,"basis":"FY2026E non-GAAP共識EPS 15.16美元（Koyfin 2026-10-31快照），259.61÷15.16＝17.1倍；終端倍數同以當年度non-GAAP EPS為分母；同業前瞻本益比事實表未涵蓋，終端倍數以本公司現值前瞻17.1倍、trailing 20.4倍為錨；EPS路徑已含回購減股，淨回購殖利率不另計以免重複"},"eps":{"bull":[19.0,23.0,26.5,30.0,33.0],"base":[18.3,21.2,21.0,23.0,25.0],"bear":[17.0,15.0,12.5,13.5,14.5]},"pe":{"bull":20,"base":17,"bear":13},"p":{"bull":20,"base":50,"bear":30},"yield_pct":{"dividend":1.562,"net_buyback":0.0},"second_stage":{"bull_cagr_pct":12,"base_cagr_pct":8},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### NXPI_Q2_2026_Earnings_Call_20260728.md
- 2026-07-28｜CFO｜guidance：Q3 營收指引 $3.75B ±$100M。（原話："We expect revenue of $3.75 billion, plus or minus $100"）
- 2026-07-28｜CFO｜guidance：Q3 non-GAAP 毛利率指引 58.5% ±50bp。（原話："We expect non-GAAP gross margin of 58.5%, plus or minus"）
- 2026-07-28｜CFO｜guidance：Q3 營業費用指引 $810M ±$10M。（原話："operating expenses of $810 million, plus or minus"）
- 2026-07-28｜CFO｜guidance：Q3 non-GAAP EPS 中點指引 $4.11。（原話："implies Q3 non-GAAP earnings per share of $4.11"）
- 2026-07-28｜CEO｜guidance：CEO 稱展望優於 90 天前預期。（原話："our outlook is better than we anticipated 90 days ago"）
- 2026-07-28｜CEO｜guidance：Q3 手機業務指引年減中個位數。（原話："Mobile is expected to be down in the mid-single-digit"）
- 2026-07-28｜CEO｜guidance：車用 Q3 指引口徑：年增數字說法自我更正，並稱高於模型。（原話："is a high teens -- is a mid-teens growth year-on-year"）
- 2026-07-28｜CFO｜margin：Q2 營業利益率 35.1%，年增 310bp。（原話："35.1%, expanding 310 basis points year-on-year"）
- 2026-07-28｜CFO｜margin：CFO 將毛利率擴張歸因於產品組合、稼動率、營運槓桿。（原話："driven by product mix, factory utilization discipline"）
- 2026-07-28｜CFO｜margin：毛利率 2027 目標沒變，CFO 對 60% 目標表示有信心。（原話："There's no change of what we previously said."）
- 2026-07-28｜CFO｜margin：晶圓代工漲價尚未出現，預期最早 Q4、主要在 2027 新合約。（原話："haven't seen that play out yet."）
- 2026-07-28｜CFO｜margin：晶圓代工新合約時點在 2027。（原話："but more in 2027 when we enter into new agreement with our"）
- 2026-07-28｜IR｜margin：IR 稱後段（零件、基板、貴金屬）有通膨成本。（原話："we did see inflationary input costs on back-end type of"）
- 2026-07-28｜CEO｜margin：價格：Q2 約持平，Q3 指引已含估計。（原話："In Q3, our guide already incorporates an estimate"）
- 2026-07-28｜CEO｜margin：價格調整為選擇性、非全面性。（原話："These adjustments are not across the board."）
- 2026-07-28｜CFO｜margin：年初稱價格降幅低個位數，CFO 稱年底可能略好於此。（原話："In the beginning of this year, we said we'd be down in the"）
- 2026-07-28｜CFO｜margin：CFO 稱年底更新時價格 probably 略好。（原話："We'll probably be a bit better, I would say"）
- 2026-07-28｜CFO｜commitment：管理層稱有信心兌現財務承諾。（原話："We remain confident that we will deliver on our financial"）
- 2026-07-28｜CEO｜commitment：CEO 對 2027 的表述，不給 Q4 數字。（原話："it only translates to a strong 2027."）
- 2026-07-28｜CEO｜commitment：結語稱毛利/利潤率擴張為結構性。（原話："Margin expansion is structural"）
- 2026-07-28｜CFO｜capital_allocation：Q2 股東回饋 $360M。（原話："In Q2, we returned $360 million to our"）
- 2026-07-28｜CFO｜capital_allocation：Q2 末總債務與現金。（原話："$10.98 billion in total debt and $3.2 billion in cash."）
- 2026-07-28｜CFO｜capital_allocation：VSMC/ESMC 累計投資占計畫承諾比重。（原話："about 70% of the total planned commitment"）
- 2026-07-28｜CFO｜capital_allocation：Q2 自由現金流 $791M。（原話："cash flow of $791 million or approximately 23% of revenue"）
- 2026-07-28｜CEO｜product：資料中心 2025 約 $200M，2026 預期超過 $500M。（原話："2025 revenue was approximately $200 million, and we expect"）
- 2026-07-28｜CEO｜product：資料中心定位在 AI 基礎設施控制平面。（原話："Our position is squarely in the control plane of AI"）
- 2026-07-28｜CEO｜product：加速 Layerscape 藍圖。（原話："Hence, we are accelerating our Layerscape road map"）
- 2026-07-28｜CEO｜product：工業與 IoT AI 處理器占比預估。（原話："approximately 15% of industrial and IoT processor revenue"）
- 2026-07-28｜CEO｜product：S32K5 等新品尚未開始放量。（原話："they haven't even begun ramping yet."）
- 2026-07-28｜CEO｜product：新一代多Gb乙太網路交換器獲設計案。（原話："next-generation multi-gigabit Ethernet switches"）
- 2026-07-28｜CEO｜product：正與客戶討論獨立 NPU。（原話："engage with customers on a discrete NPU"）
- 2026-07-28｜CFO｜customer：Kinara 設計案漏斗上季 >$1B，本季 >$1.5B。（原話："this quarter, it's sitting over $1.5 billion in the funnel."）
- 2026-07-28｜IR｜customer：漏斗涵蓋客戶數。（原話："$1.5 billion pipeline represents over 200 unique and"）
- 2026-07-28｜CEO｜customer：公司稱車用未看到補庫存。（原話："we actually see no restocking, right?"）
- 2026-07-28｜CFO｜customer：西方 Tier 1 未見補庫存。（原話："but we have not seen the restocking effect specifically with"）
- 2026-07-28｜CFO｜customer：通路庫存週數。（原話："It was 11 weeks last quarter"）
- 2026-07-28｜CFO｜customer：車用公司特定成長驅動預期明年向 50% 靠近。（原話："we expect that 47% to grow towards 50% next year."）
- 2026-07-28｜CEO｜risk：交期拉長、能見度改善。（原話："lead times are stretching out and visibility has improved"）
- 2026-07-28｜CFO｜risk：CFO 稱訂單積壓可見度達 18 個月。（原話："So we have a signal of 18 months out."）
- 2026-07-28｜CFO｜risk：客戶升級（escalation）數量翻倍。（原話："have doubled since last quarter"）
- 2026-07-28｜CFO｜risk：交期大於 16 週的產品範圍擴大。（原話："it's greater than 16 weeks"）
- 2026-07-28｜CEO｜risk：記憶體短缺：部分客戶受影響。（原話："So in pockets, we see."）
- 2026-07-28｜CEO｜competition：CEO 稱同業收購（Synaptics、Hailo）印證策略。（原話："the acquisitions that I think you mentioned"）
- 2026-07-28｜CEO｜product：結語：實體 AI 為十年期採用週期。（原話："we're entering a decade-long adoption of"）

### 問答異常語氣（迴避／改口／保留）
- NXPI_Q2_2026_Earnings_Call_20260728.md｜問：Vivek Arya 問 2027 展望是否因資料中心上調、並問 Q4 季節性｜答法：CEO 稱「we're not going to give you a Q4 number」，改談動能與訂單，未給 2027 數字調整。
- NXPI_Q2_2026_Earnings_Call_20260728.md｜問：Chris Caso 問價格影響幅度與 Q3 指引假設、是否對毛利率中性｜答法：CEO 把問題重新框為定價是策略工具；CFO 稱年底再更新，未給 Q3 價格貢獻幅度。
- NXPI_Q2_2026_Earnings_Call_20260728.md｜問：Matthew Prisco 問價格對 Q3 指引的影響程度｜答法：答 Q2 約持平、Q3 指引已含估計，但稱「we won't know the exact impact until much later」，未給數字。
- NXPI_Q2_2026_Earnings_Call_20260728.md｜問：Francois Bouvignies 問 SDV 營收是否可量化｜答法：未給 SDV 營收數字，重述加速成長驅動 +22% 及新品尚未放量。
- NXPI_Q2_2026_Earnings_Call_20260728.md｜問：Francois Bouvignies 問車用 Q3 季增中個位數是否顯示復甦不足｜答法：CEO 改以年增看待；口述 'high teens -- is a mid-teens' 自我更正，未直接回應季增疑問。
- NXPI_Q2_2026_Earnings_Call_20260728.md｜問：Joshua Buchalter 問稼動率與晶圓存取費對 Q3 毛利率影響｜答法：CFO 稱尚未看到，預期 Q4 起、主要 2027；稼動率回答語句不完整，未重述低 80s 到中 80s 具體數字。

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 3 | 3 |
| customer_second_source | found | 2 | 2 |
| customer_concentration_credit | found | 3 | 1 |
| supply_demand_durability | found | 5 | 4 |
| regulatory_antitrust | found | 3 | 2 |
| reg_tariff_export | found | 3 | 2 |
| geo_supply_chain | found | 5 | 2 |
| end_markets | found | 5 | 4 |
| substitute_technology | found | 2 | 2 |
| channel_business_model_shift | found | 4 | 2 |
| capital_markets_pricing | found | 5 | 4 |
| major_events | found | 1 | 3 |

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260729","verdict":"進場","role":"衛星","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"SDV 架構轉換使 NXP 單車價值結構性上升——公司特定成長引擎（S32 SDV／雷達／電氣化／連接）由汽車營收 47% 走向 50%+，且新一代 S32N/K5 順利接棒"},{"id":"H2","text":"工業／IoT ＋ 資料中心成為第二引擎，且不是一次性循環回補——邊緣 AI 內容驅動而非庫存回補"},{"id":"H3","text":"margin 擴張是結構性的，60% 毛利率目標可達且守得住——組合、稼動率、混合製造（VSMC/ESMC）三者共同驅動，而非單純循環稼動"}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"2027 循環回落 ＋ wafer 成本墊高雙擊——管理層已明言晶圓代工成本壓力「主要落在 2027 年重簽新約時」，若同期需求轉弱，60% 毛利率目標與 EPS 軌跡同時跳票"},{"id":"R2","text":"兩個新戰場同時湧入強敵——Infineon 以 $2.5B 買下 Marvell Brightlane 車用乙太網路（2025-08 完成，年營收 $2.25–2.5 億、2030 設計導入管線約 $40 億），直取 NXP 剛宣布拿下 design award 的多 Gb 車載乙太網路交換器；Microchip 於 2026-07-24 簽約併購邊緣 AI 處理器商 Hailo（Hailo-8/10/15，100+ 客戶、10,000+ 開發者）；onsemi 以約 $70 億全股票併購 Synaptics 進軍實體 AI"},{"id":"R3","text":"中國車用晶片國產化政策執行到位——政策目標 2027 年 100% 國產；上汽／長安／長城／比亞迪／理想／吉利已備妥全國產晶片車型；疊加美中關稅休戰 2026-11-10 到期"}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"starter 1/3；加碼＝S32N 或 S32K5 宣告量產時點，或回落 $230 以下","irr_base_pct":10.0,"ev5y_pct":53.6,"drift_watch_prior":{"dca_verdict":"進場","dca_role":"衛星","signal":"B","val":"🟢","ma":"🟡","trap":"🟢","moat_trend":"→","runway_post_y5":"🟢","asym_ratio":3.4,"ev5y_pct":53.6,"irr_base_pct":10.0,"max_dd_pct":-50.0,"bull_5y_price":600.0,"bear_5y_price":143.0,"p_bull_pct":25.0,"p_bear_pct":28.0,"rearm_trigger":"starter 1/3；加碼＝S32N 或 S32K5 宣告量產時點，或回落 $230 以下","price_at_dd":259.12,"archetype":"品質複利成長","cycle_position":"早循環"}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"NXPI","date":"2026-11-02","schema":"v15.0","contract":"v19","company_name":"NXP Semiconductors N.V."},"oneliner":"SDV在汽車平產量下撐起車用扣感測器+17%、Q3營益率37%創高，FY2027本益比約14倍不貴；但交期拉長與客戶催貨顯示已進循環中段，最大風險是2027–28年訂單反轉。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/NXPI_20261102/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/NXPI_20261102/scenario.json","answers":{"q1_business":{"verdict":"賺車廠與工業客戶的錢，錢卡在處理器／MCU的設計導入節點：車用約55%、工業與IoT 21%、通訊基建13%、手機11%；Q3 non-GAAP毛利率58.6%、營益率37.1%。","reasoning":"收錢方式：賣處理器、MCU、類比與連接晶片給車廠／Tier 1與工業客戶，約59%經通路出貨（Q3經銷營收22.44億美元），Avnet一家占2025年營收23%，無直接客戶超過10%。錢卡在設計導入節點：車規與功能安全認證加S32軟體平台，綁定整個車型週期。Q3營收37.86億美元年增19%，non-GAAP毛利率58.6%、營益率37.1%（GAAP 32.4%），Q4指引38.5億美元±1億、毛利率59%。分部：車用約20.7億美元（以總營收扣其他三段推算，扣感測器年增17%）、工業與IoT 8.02億（+39%）、通訊基建與其他5.03億（+54%）、手機4.11億（−4%）。產業時鐘在擴張期：營收連四季雙位數成長、交期超過16週的產品由一年前25%升至80%、2026年價格由預期下滑轉持平，依據是訂單與定價而非股價。供需：週期性將反轉，後段產能吃緊、前段2027年轉緊，但新廠2027–28年陸續開出，中國占2026年成熟製程新增產能近七成。單點依賴：Avnet 23%屬通路集中而非終端客戶集中，南韓公平會正審議Ship & Debit經銷安排。產業態勢三軸：競爭面惡化（中國低階MCU、同業以併購切入車載乙太網路與邊緣AI）、結構面轉好（SDV每車價值2–3倍、邊緣AI，持久性中等）、其他結構變數（南韓反壟斷、232關稅、2027年分部重分類）；裁決為雙向拉鋸，結構轉好暫占上風。","fact_refs":["f_kpi0_revenue_gaap","f_kpi1_non_gaap_operating_incom","f_kpi2_non_gaap_operating_margi","f_kpi3_gaap_operating_income","f_kpi4_gaap_operating_margin","f_kpi7_guidance_q4_2026_revenue","f_kpi8_dio","f_kpi9_channel_inventory","f_earnings_recency"],"verdict_values":{"revenue_quality":"Q3營收37.86億美元年增19%（扣已出售MEMS感測器22%），四段中三段雙位數成長、各區域皆雙位數；約59%經通路（經銷營收22.44億美元，年增20.3%），通路庫存11週持平，庫存天數148天含約13天工廠整併預建庫存；Q4指引38.5億美元±1億、年增15%。","unit_econ_note":"SDV與xEV每車半導體價值為傳統架構2–3倍；2026年定價由年初預期低個位數下滑改為全年持平（Q3、Q4各約+1%，只轉嫁成本）；工廠稼動率中80%、2027年預期高80%，毛利率2027年達60%、2028年VSMC放量後再往上。","archetype":{"primary":"品質複利成長","secondary":"循環/商品","confidence":"中","fingerprint":"高毛利車用／工業晶片商，GAAP營益率2022–2025年維持24.7%–28.7%，但營收2024、2025年連兩年下滑後2026年反彈，帶明顯庫存週期"},"industry":{"clock_phase":"II","sd_verdict_source":"週期性將反轉：後段封測產能極緊、CFO預期前段2027年轉緊，但VSMC／ESMC／馬來西亞新廠與同業新廠2027–28年陸續開出，中國占2026年成熟製程新增產能近七成；Wolfe Research認為供過於求最早2028年，TechInsights提示2027下半年至2028上半年可能再現搶貨（Q3財報會議、第三方研究）","bargaining":{"up":"對上游弱：前段多仰賴台積電體系（SSMC、VSMC、ESMC合資）與外部代工，2027年代工存取費重簽有漲價壓力；後段材料通膨以選擇性漲價轉嫁","down":"對下游中等：Avnet一家占2025年營收23%且逐年微升，無直接客戶超過10%；車廠開始直接提供需求預測，交期超過16週的產品占80%，短期議價偏向NXP","geo":"中國本土晶片商在資訊娛樂與低階MCU競爭；美國232半導體關稅（2026-01-15起對特定先進晶片課25%，工業與消費用途豁免）與出口管制（2020年曾停止對華為出貨）"},"profit_pool_dir":"車用與工業半導體利潤池往區域／中央運算、邊緣AI處理器與資料中心控制平面移動，每車半導體價值2–3倍，NXP位於移入端；5年營業利益池占比數字事實表未涵蓋","tam_table":{"expanded":false,"reason":"事實表未涵蓋TAM／SAM／滲透率與利潤池數字；SDV以公司揭露的年化營收（超過15億美元→2027年20億美元）與每車價值2–3倍代理，資料中心以2025年約2億→2026年超過5億→約2028年超過10億美元代理"}}}},"q2_moat":{"verdict":"護城河B級、方向穩定：車規設計導入與S32軟體平台綁定車型週期，SDV執行面轉強，但定價力與利潤率仍落後TXN、ADI。","reasoning":"機制：車用處理器／MCU的設計導入轉換成本，車規與功能安全認證加S32平台軟體生態，綁定3–5年車型週期；福斯與Rivian合資的RV Tech宣布兩家區域平台統一採S32K5，福斯集團也選S32K5作為各品牌區域控制共用元件。執行面8分：SDV年化營收超過15億美元、北美與亞太有S32N設計案、首個人形機器人設計案、資料中心目標由5億上調至約2028年超過10億美元。定價面7分：2026年價格中性，Q3、Q4各約+1%只轉嫁成本；執行長稱年降價模式會緩和，但尚未見到。對同業：TTM毛利率56.4%、營益率28.6%，低於TXN（60.2%／41.1%）與ADI（65.8%／35.7%），高於STM（33.8%／6.6%）與ON（37.7%／18.1%）；投入資本資料缺，報酬差以營益率差代理，對最強同業仍為負且未見收斂，故不給A。方向：執行面擴大、定價面持平，合判穩定；升級需等S32K5實際出貨與份額證據。ROIC：TTM GAAP營益率28.6%×（1−18%稅率）≈稅後23.4%，周轉率事實表未涵蓋。四檢查點：需求基礎值綠、決策層級綠、價值鏈分配黃、社會容忍度黃。","fact_refs":["f_peer_nxpi_gross_margin_pct","f_peer_nxpi_operating_margin_pct","f_peer_nxpi_fcf_margin_pct","f_peer_txn_gross_margin_pct","f_peer_txn_operating_margin_pct","f_peer_txn_fcf_margin_pct","f_peer_adi_gross_margin_pct","f_peer_adi_operating_margin_pct","f_peer_adi_fcf_margin_pct","f_peer_stm_gross_margin_pct","f_peer_stm_operating_margin_pct","f_peer_stm_fcf_margin_pct","f_peer_on_gross_margin_pct","f_peer_on_operating_margin_pct","f_peer_on_fcf_margin_pct"],"verdict_values":{"moat":{"mechanism":"車用處理器／MCU的設計導入轉換成本：車規與功能安全認證、S32平台與CoreRide軟體生態綁定3–5年車型週期；RV Tech與福斯集團把S32K5定為跨品牌區域平台共用元件","execution":8,"pricing":7,"grade":"B","trend":"→","trend_evidence":"執行面擴大（RV Tech／福斯區域平台標準化S32K5、北美與亞太S32N設計案、首個人形機器人設計案），定價面持平（2026年價格中性、只轉嫁成本）；對最強同業營益率差距未收斂：TTM營益率28.6%對TXN 41.1%、ADI 35.7%","competitor_notes":[{"name":"TXN","strategy_note":"營益率41.1%、FCF率35.2%皆高於NXP，靠自有12吋廠與通用類比廣度；車用處理器正面重疊有限，是成本與利潤率標竿"},{"name":"ADI","strategy_note":"毛利率65.8%為同業最高，高效能類比與混合訊號定價力強，在車用電池管理與連接部分重疊；同樣被南韓公平會審議"},{"name":"STM","strategy_note":"營益率6.6%、FCF率3.8%，車用MCU直接對手但處獲利谷底，低稼動下有降價搶單誘因，是價格紀律的風險來源"},{"name":"ON","strategy_note":"營益率18.1%，主力在功率與影像感測，與NXP處理器重疊小；併購Synaptics切入實體AI，成為邊緣AI新對手"},{"name":"Infineon","strategy_note":"車用MCU主要對手，買下Marvell車用乙太網路業務直攻NXP多Gb車載交換器；本包同業財務表未收錄"}],"threats":[{"level":"🟡","text":"中國本土晶片商在資訊娛樂與低階MCU競爭，中國占2026年成熟製程新增產能近七成；NXP自承並改以鎖定客戶架構因應，查無高階車用MCU被取代的直接證據","p":30,"evidence_refs":["competitive_share_entrants#2","supply_demand_durability#1"]},{"level":"🟡","text":"規模更大、資源更多的IDM與無晶圓廠對手可能壓量或壓價（10-K自述，屬點對點競爭）","p":25,"evidence_refs":["competitive_share_entrants#0"]},{"level":"🟡","text":"同業以併購切入NXP新戰場：Infineon買Marvell車用乙太網路、Microchip買Hailo、onsemi併Synaptics，分別攻車載交換器與邊緣AI，屬產品線層級攻擊","p":30,"evidence_refs":[]}],"roic_durability":{"quadrant":"高利益率×周轉率未知：TTM GAAP營益率28.6%、稅後約23.4%；投入資本事實表未涵蓋，無法判周轉","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者是駕駛與工廠設備、決策者是車廠與Tier 1架構團隊、付款者是Tier 1／通路，三環節都成立；區域／中央運算是架構換代的需要而非想要，xEV滲透率由2025年約41%升至2026年約47.5%、2027年預估50–55%，每車半導體價值2–3倍"},{"item":"決策層級","level":"🟢","text":"替代性要在車型平台層衡量：RV Tech與福斯集團把S32K5定為跨品牌區域平台共用元件，換供應商需重做車規與功能安全認證、改寫軟體，綁定整個車型週期；代理變數＝平台標準化範圍與設計案年限，漲價後流失率事實表未涵蓋"},{"item":"價值鏈分配","level":"🟡","text":"執行長稱半導體占系統價值比重上升、年降價將緩和，但目前漲價只轉嫁成本；上游前段集中在台積電體系合資廠，2027年代工存取費重簽；下游Avnet占23%；毛利率56.4%低於TXN、ADI，這段價值鏈NXP拿得比類比龍頭少"},{"item":"社會容忍度","level":"🟡","text":"車用晶片是政治敏感品：疫情期與2025年荷蘭接管Nexperia的斷料經驗使車廠與政府對大幅漲價容忍度低；南韓公平會已審議經銷利潤預設，232關稅與出口管制屬政策風險；未見針對NXP定價的立法，故非紅燈"}],"roiic":"無法計算（投入資本序列事實表未涵蓋）；以邊際利潤率代理：Q3年增營收約6.0億美元、non-GAAP營業利益增約3.3億美元，邊際利潤率約55%，屬循環營運槓桿，不等於可持續增量ROIC","reinvest_rate":"事實表未涵蓋折舊與收購金額，淨再投資率無法計算；毛投資＝2027年資本支出約營收5%加VSMC／ESMC合資注資，約為2027年稅後盈餘的20–30%（毛額，未扣折舊）","endo_ceiling":null,"formula_note":"ROIC＝稅後營業利益率×投入資本周轉率；內生成長＝增量ROIC×再投資率，兩項輸入皆缺，上界改在成長題以有機營收成長代理"}}}},"q3_growth":{"verdict":"跑道寬：區域／中央運算2027年才首批出貨、2028年全面放量，資料中心與工業邊緣AI是有出處的第二曲線；共識EPS兩年年化19%高於營收約12%，差距由毛利率擴張與回購解釋。","reasoning":"成長＝量（每車內容）為主、價為輔、回購加成。共識EPS：FY2026E 15.16、FY2027E 18.32、FY2028E 21.48美元（Koyfin快照，家數事實表未涵蓋；營收共識FY1 24位、FY2 28位分析師），兩年年化19.0%；FY2027共識營收年增約11.9%。內生上界：增量ROIC×再投資率無法由事實表算出，以有機營收成長約10–12%代理；缺口約7pp歸因毛利率擴張與營業費用槓桿約4–5pp、淨回購約2–3pp，可歸因，不依賴估值重評。跑道：區域／中央運算2027年首批出貨、2028年全面放量，管理層稱仍在早期；第二曲線有出處：資料中心控制平面2025年約2億→2026年超過5億→約2028年超過10億美元，工業AI處理器占比翻倍至約15%，首個人形機器人設計案，獨立NPU Ara 2028年量產。五年後滲透率推估仍不超過35%（滲透率數字事實表未涵蓋，依量產時程推估），判寬。衰退信號十項亮1項、2項資料缺口。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_consensus_rev_3m_fy1_pct","f_kpi0_revenue_gaap"],"verdict_values":{"growth":{"driver_mix":"量為主（每車內容2–3倍、工業AI處理器、資料中心新品放量）＋價（2026年中性、2027年轉嫁成本與SDV組合提升平均售價）＋回購（63億美元授權）；併購屬補強（Kinara、TTTech Auto），金額事實表未涵蓋","runway_years":"8–10（推估：2028年全面放量後至2030年代中期達30%滲透；事實表無滲透率數據）","runway_post_y5":"🟢","endo_ceiling_basis":"增量ROIC與再投資率無法由事實表計算（缺投入資本、折舊、收購金額）；以管理層2027年營收雙位數成長指引、FY2027共識營收年增約11.9%作有機成長代理，內生上界約10–12%；共識EPS（FY2026E→FY2028E）年化19.0%超出部分歸因毛利率由58.6%擴至60%以上與費用槓桿約4–5pp、淨回購（63億美元授權約市值10%）約2–3pp","segments":[{"item":"車用","value":"約20.7億美元（推算），扣感測器年增17%，占約55%；SDV年化超過15億美元；Q4指引年增低雙位數、扣感測器高十位數"},{"item":"工業與IoT","value":"8.02億美元，年增39%；工業部分近+50%、占該段約70%；Q4指引年增高20%區間"},{"item":"通訊基建與其他","value":"5.03億美元，年增54%，資料中心與安全卡帶動；2026年底數位網路占比超過30%、射頻功率低於20%"},{"item":"手機","value":"4.11億美元，年減4%；Q4指引年減中十位數"}],"decay_signals":["毛利率連2季年減：未亮（Q3 non-GAAP毛利率年增160bp）","核心市占近12個月縮減：資料缺口（份額數據事實表未涵蓋）","主力產品提價後銷量下滑：未亮（漲價只轉嫁成本，營收年增19%）","EPS成長高於營收超過5pp：亮（共識EPS兩年年化19.0%對FY2027營收約11.9%；Q3 EPS年增35%對營收19%）","FCF/淨利連2年低於0.75：未亮（2023–2025年0.90、0.76、1.13）","SBC/營收超過5%且上升：未亮（Q3約3.0%）","TAM萎縮或被替代：未亮（區域架構採用NXP，屬受益方）","產業估值倍數近3年系統性下移：資料缺口（同業倍數歷史事實表未涵蓋）","維護性資本支出占FCF超過60%：未亮（資本支出約營收2%，FCF約25%）","停止投資新產能且營收3年內下滑：未亮（VSMC、ESMC、馬來西亞新廠投資中）"],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"現金轉換穩定、回購轉為加速：TTM自由現金流約營收25%，新增50億美元回購；收購報酬與回購收益率比對缺資料。","reasoning":"自由現金流：Q3 12.06億美元（約營收32%），TTM約35億美元、營收25%；年度FCF/淨利2023年0.90、2024年0.76、2025年1.13，轉換穩定。SBC季1.14億美元、占營收約3.0%，年化約市值0.7%。現金去向（TTM）：股東回饋17億美元（股息＋回購），其餘用於去槓桿、策略收購與VSMC／ESMC合資注資（Q3 2.18億美元，年底完成逾75%）；三年四分去向事實表未涵蓋。淨負債70.35億美元、淨槓桿1.3倍。董事會新增50億美元回購，總授權約63億美元約市值10%，CFO稱Q4與2027年加速回購、長期配回100%超額自由現金流。2027年資本支出升至約營收5%（後段擴產、馬來西亞新廠），自由現金流率將短暫下滑。計分：收購已實現報酬事實表未涵蓋；回購買入收益率以前瞻盈餘殖利率5.8%（FY1）／7.1%（FY2）計，10年期公債殖利率事實表未涵蓋無法比對；SBC毛稀釋約0.7%/年，通過。","fact_refs":["f_kpi5_non_gaap_free_cash_flow","f_kpi6_sbc","f_net_debt_m","f_dividend_yield_ttm","f_shares_diluted_m","f_ev_m","f_fwd_pe_latest"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":true,"passed":null,"input":"近期收購（Kinara、TTTech Auto）金額與後續報酬事實表未涵蓋"},{"name":"buyback_yield","applicable":true,"passed":null,"input":"現價前瞻盈餘殖利率5.8%（FY1）／7.1%（FY2）；10年期公債殖利率與歷史回購均價事實表未涵蓋"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"季SBC 1.14億美元，年化約4.6億美元，約市值654億美元的0.7%（毛稀釋；淨股數變化事實表未涵蓋）"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購撐：營收成長來自車用與工業內容提升，近期收購金額事實表未涵蓋且非成長主力；資本回饋方向以63億美元回購授權與長期100%超額自由現金流配回為準"}}}},"q5_valuation":{"verdict":"現價只要求FY2027 EPS約18.3美元兌現且倍數守住14倍，我們相信；估值偏便宜，風險在2028年後的循環而非現值。","reasoning":"現價259.61美元＝FY2026E 17.1倍、FY2027E 14.2倍、FY2028E 12.1倍。反推：要讓現價合理，只需FY2027 EPS約18.3美元兌現且倍數不跌破14倍；Q4指引EPS 4.36美元年化已達17.4，加上2027年雙位數營收成長與毛利率60%，達成機率高。真正的問題是2028年之後是否循環回落，這點放進空頭機率而非現值。trailing本益比20.4倍在4個年度端點分位47；P/S與EV/S處端點頂部，是利潤率回升而非倍數擴張。賣方目標價（皆早於Q3財報）均值約296–314美元，各來源全距約2.0–2.5倍，接近分歧門檻，降低對自身目標價的信心。短期上檔：FY2027E 18.32×17倍≈311美元（+20%）；中期：基準路徑FY2028E 21.2×17倍≈360美元（+39%）。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_pe_current","f_pe_percentile","f_ps_current","f_ps_percentile","f_ev_s_current","f_ev_s_percentile","f_ev_s_fwd","f_dividend_yield_ttm","f_consensus_rev_3m_fy1_pct","f_consensus_rev_fy1_pct","f_consensus_rev_fy2_pct"],"verdict_values":{"valuation":{"basis":"前瞻本益比與PEG（品質成長型優先尺）；P/S與EV/S因利潤率回升處於年度端點高位，僅作對照","peers":{"expanded":false,"reason":"事實表同業表只有利潤率與研發密度，未收同業前瞻本益比，無法做倍數對照；終端倍數改以本公司現值前瞻17.1倍、trailing 20.4倍為錨"},"fwd_pe":17.12,"peg":0.9,"percentile_5y":null,"val_light":"🟢","val_light_derivation":"前瞻本益比17.1倍（FY2026E）、14.2倍（FY2027E），PEG 0.90（以FY2026E→FY2028E共識年化19.0%計，低於1.0屬便宜）；trailing本益比20.4倍位於4個年度端點分位47，非五年分位，五年高低點事實表未涵蓋故五年分位留空；P/S 4.74倍、EV/S 5.25倍位於年度端點頂部，反映利潤率回升而非倍數擴張","upside_short_pct":20.0,"upside_mid_pct":38.8,"denominator_disputed":false,"denominator_note":"FY2026E EPS含稼動率回升（中80%）的循環成分，但營收僅回到2022年約1.08倍、利潤率擴張有VSMC與產品組合的結構來源，非一次性；分母不列爭點，循環回落風險放進空頭機率30%"}}},"q6_how_wrong":{"verdict":"最可能看錯在把稼動率與交期帶來的循環利潤當成結構成長；陷阱風險中等。","reasoning":"最可能看錯：把稼動率中80%、交期拉長帶來的毛利率與營收當成結構成長。26週股價−11.4%而EPS年增35%，市場已在定價循環頂部；我們的分歧在於認為SDV內容成長能讓下一次去化比市場想像淺，但不否認循環成分。陷阱風險中：衰退信號亮1項（EPS成長快於營收超過5pp），來源是利潤率擴張與回購，屬良性但需監測；庫存天數148天含13天預建庫存、通路11週，尚未膨脹。依據全文見反證紀錄。","fact_refs":["f_week26_return_pct","f_kpi8_dio","f_kpi9_channel_inventory","f_ps_percentile","f_rsi14"],"verdict_values":{"trap":{"verdict":"🟡","label":"循環中段利潤率外推"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":15.16,"pe":17.12,"basis":"FY2026E non-GAAP共識EPS 15.16美元（Koyfin 2026-10-31快照），259.61÷15.16＝17.1倍；終端倍數同以當年度non-GAAP EPS為分母；同業前瞻本益比事實表未涵蓋，終端倍數以本公司現值前瞻17.1倍、trailing 20.4倍為錨；EPS路徑已含回購減股，淨回購殖利率不另計以免重複"},"eps":{"bull":[19.0,23.0,26.5,30.0,33.0],"base":[18.3,21.2,21.0,23.0,25.0],"bear":[17.0,15.0,12.5,13.5,14.5]},"pe":{"bull":20,"base":17,"bear":13},"p":{"bull":20,"base":50,"bear":30},"yield_pct":{"dividend":1.56,"net_buyback":0.0},"second_stage":{"bull_cagr_pct":12,"base_cagr_pct":8},"max_dd":{"lo":-50,"hi":-33,"basis":"Bear路徑谷底2029年EPS 12.5美元×谷底倍數12–14倍＝150–175美元，對應現價−33%～−42%；再加風險趨避時估值超跌約8pp，下緣取−50%；歷史最大回撤事實表未涵蓋，無法以實績校準","trigger_time":null},"basis":{"bull":"SDV與資料中心雙放量：營收年增約13%至2031年，毛利率2028年後超過61%（VSMC自製省代工加價），營益率40%上下，回購每年減股約2%；終端20倍","base":"2027–28年貼近共識（18.3、約21.2），2029年庫存修正持平，之後回到約9%成長（含回購）；終端17倍，約等於現值前瞻倍數","bear":"2027年下半年重複下單反轉，2028–29年車用與工業去化，新廠折舊與代工費同時墊高，EPS 2029年落到12.5；中國成熟製程產能壓價，終端13倍"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"交期超過16週的產品占比由一年前25%升至80%、客戶催貨季增明顯、部分OEM討論安全庫存；中國占2026年成熟製程新增產能近七成；2028年VSMC、ESMC、馬來西亞封測廠同時開出；Q4指引略低於預期後盤後跌近8%，賣方點出車用需求趨緩","assumption":"管理層所說未見補庫存、需求是真的成立，2027年雙位數成長之後不會有明顯去化","consequence":"2028–29年營收回落10–15%，遞減利潤率約50%下EPS回到12–13美元，倍數壓到12–13倍，股價約150–170美元（−35%～−42%），五年虧損最可能的故事","ruling":"採納為空頭情境：已放進30%空頭機率與−50%回撤下緣；不加碼到更悲觀的理由是公司自管約四成車用通路、通路庫存11週未膨脹，上一輪（2024–25年）營收只年減5%與3%，Bear假設已比上一輪嚴重","watch":"book-to-bill、通路庫存週數、扣預建庫存天數、交期超過16週占比轉降","evidence_refs":["supply_demand_durability#1","capital_markets_pricing#0"],"fact_refs":["f_kpi8_dio","f_kpi9_channel_inventory","f_kpi7_guidance_q4_2026_revenue"]},{"view":"論點成功但股東經濟變差","evidence":"2027年資本支出由約營收2%升至約5%、合資注資（Q3 2.18億美元）、2027年代工存取費重簽；前段產能集中在台積電體系合資廠（SSMC、VSMC、ESMC），公司自述即時採購暴露斷鏈風險；Avnet占23%營收且逐年微升，主要客戶減量有重大影響","assumption":"SDV與資料中心成長的果實留在NXP，不被代工、通路與新產能投資吃掉","consequence":"營收照計畫成長，但自由現金流率由TTM約25%降至20%上下，回購節奏放慢，每股價值成長落後營收","ruling":"部分採納：2027年自由現金流率下滑幾乎確定（資本支出+3pp），但VSMC 2028年起省下代工加價、毛利率超過60%是回收來源；以TTM自由現金流率低於20%為警戒","watch":"TTM自由現金流率、2028年毛利率是否超過60%、季度回購金額","evidence_refs":["geo_supply_chain#2","customer_concentration_credit#2"],"fact_refs":["f_kpi5_non_gaap_free_cash_flow","f_peer_nxpi_fcf_margin_pct"]},{"view":"價格已反映太多","evidence":"P/S 4.74倍位於4個年度端點最高、EV/S 5.25倍位於分位97.8，營業利益率處紀錄高點","assumption":"FY2027 EPS 18.32美元可達且之後不回落","consequence":"若2027年即是峰值，現價等於峰值盈餘14倍，峰值倍數下跌時跌幅可達三成","ruling":"反駁：營收倍數高是利潤率回升造成，前瞻本益比17.1倍、trailing本益比位於年度端點分位47，26週股價−11.4%而同期EPS年增35%，市場已在折價循環風險，不構成價格過度反映","watch":"FY2027共識下修幅度與股價反應；股價超過400美元（約FY2027共識22倍）","evidence_refs":[],"fact_refs":["f_ps_current","f_ps_percentile","f_ev_s_percentile","f_fwd_pe_latest","f_week26_return_pct","f_pe_percentile"]},{"view":"論點失敗","evidence":"中國本土供應商在資訊娛樂與低階MCU競爭；美國232半導體關稅可能擴大、出口管制趨嚴（2020年曾停止對華為出貨）；前份引述的中國車用晶片2027年國產化目標，本包事實表未收來源","assumption":"S32K5與S32N在中國照時程導入，中國車廠高階控制器仍採用外商方案","consequence":"中國車用營收流失、S32K5中國首批出貨（最早2027年Q1）延後，SDV 20億美元目標落後","ruling":"部分採納：屬慢變量，列為長期風險；目前證據顯示高階車用MCU未被取代，且S32K5在中國有POC與首批出貨規劃","watch":"S32K5中國出貨是否如期、公司揭露的中國區營收、232第二階段範圍","evidence_refs":["competitive_share_entrants#2","reg_tariff_export#0","reg_tariff_export#1"],"fact_refs":[]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 🟡 → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=🟡","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 259.12 → 本次 259.61（+0.2%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=259.12","side_b":"本次 price_at_dd=259.61","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 259.12 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 259.12 美元：Bull 價 600、Bear 價 143，五年期望值 +53.6%，基準年化 10.0%，不對稱比 3.4","side_b":"本次情境、股價仍用 259.12 美元：Bull 價 660、Bear 價 188.5，五年期望值 +54.8%，基準年化 10.4%，不對稱比 3.78","ruling":"先換情境、股價不動：五年期望值多 1.2 個百分點，基準年化多 0.4 個百分點。不對稱比由 3.4 變為 3.78。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變好。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 259.12 美元：五年期望值 +54.8%，基準年化 10.4%，不對稱比 3.78","side_b":"本次情境、股價 259.61 美元：五年期望值 +54.5%，基準年化 10.4%，不對稱比 3.75","ruling":"再換股價、情境不動：起點價上漲 0.2%，五年期望值少 0.3 個百分點，基準年化少 0.0 個百分點，不對稱比由 3.78 降到 3.75。合計五年期望值比前份多 0.9 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"需求性質：結構成長或循環補庫存","cause":null,"prior_field":null,"side_a":"管理層：未見車用補庫存，需求由SDV、實體AI、資料中心轉型驅動，與疫情期不同；車用通路約四成由公司自管，有補庫存一定看得到","side_b":"交期超過16週產品由25%升至80%、客戶催貨季增明顯、部分OEM討論安全庫存、後段產能極緊；Q4指引略低於預期、盤後跌近8%，賣方點出車用需求趨緩","ruling":"可調和（程度差異）：兩者同時成立。Q3公司特有成長動能年增30%而車用產量持平，結構成分是真的；但交期與催貨是循環中段信號，未來2–4季的成長有一部分是借未來。裁定：持有理由站在結構面，倉位與加碼節奏按循環面管理，空頭機率提高到30%。現在就賣的最強論證：股價回到前份位置，但循環從早段走到中段、利潤率處紀錄高點，風險報酬比變差","evidence_level":"中（管理層口述加第三方報導，訂單數字未量化）","settle_metric":"book-to-bill（口述）、2027年Q1營收季減幅（歷史季節性約−5%）、通路庫存週數","if_then":["若2027年Q1營收季減優於−5%且book-to-bill仍高於1→維持持有，按加碼條件執行","若book-to-bill跌破1或通路庫存超過13週→減碼至半倉並停止加碼","反向：若股價先漲過330美元而訂單證據未更新→不追"],"evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#4","supply_demand_durability#1"]},{"axis":"Q4指引：低於預期或高於預期","cause":null,"prior_field":null,"side_a":"財報後報導：Q4營收指引中點38.5億美元略低於分析師預期，盤後跌近8%","side_b":"Q4 EPS指引中點4.36美元高於7月下旬共識4.25美元，毛利率指引59%創高；FY1共識EPS近3個月上修0.53%，最新兩份快照持平","ruling":"可調和：市場失望的是營收季增只有2%與車用季增低個位數，不是獲利；共識未下修，賣方模型沒有因此降評。裁定此次跌幅屬價格面，不改盈餘假設","evidence_level":"中（新聞報導未給共識數字，共識快照只到2026-10-31）","settle_metric":"下一份共識快照FY2027 EPS修正幅度","if_then":["若FY2027共識下修超過5%而股價未跌→停止加碼，終端倍數下調一級","若共識持平而股價跌破230美元→分批加碼"],"evidence_refs":["capital_markets_pricing#4","capital_markets_pricing#0"]},{"axis":"前份欄位延續（股價持平）","cause":"價格變動","prior_field":["signal","val","moat_trend","runway_post_y5","archetype"],"side_a":"前份（2026-07-29，股價259.12）：進場；品質B；估值偏便宜；護城河方向穩定；五年後跑道寬；品質複利成長型","side_b":"本次（股價259.61，+0.2%）：品質、估值、護城河方向、跑道、公司類型判斷皆維持；裁決與角色由程式依本次輸入重算","ruling":"股價幾乎沒動，FY1共識近3個月小幅上修0.53%，估值結論不變；Q3新證據（RV Tech區域平台標準化、資料中心目標上調至超過10億美元）強化但未跨越護城河方向升級門檻（需實際出貨證據），故以上欄位不改","evidence_level":"高（價格與共識皆為事實表數字）","settle_metric":"S32K5實際出貨、FY2027共識修正","if_then":["若S32K5出貨確認且份額證據出現→護城河方向改為擴大","若FY2027共識下修超過10%→估值結論降一級"],"evidence_refs":[]},{"axis":"循環位置","cause":"新證據","prior_field":["cycle_position"],"side_a":"前份：早循環","side_b":"本次：中循環","ruling":"交期超過16週占比80%（一年前25%）、book-to-bill各市場皆遠高於1、客戶催貨季增、2026年價格由預期低個位數下滑轉為持平、稼動率中80%且2027年預期高80%，訂單與定價都已越過早段特徵；但OEM未補庫存、通路11週，尚未到晚段","evidence_level":"中（Q3財報會議CFO與執行長口述）","settle_metric":"book-to-bill、通路庫存週數、價格是否出現供需型漲價","if_then":["若出現供需型漲價或通路庫存超過13週→改判晚循環，減碼1/3","若2027年Q1季減優於季節性且庫存不升→維持中循環判斷"],"evidence_refs":["supply_demand_durability#1"]},{"axis":"陷阱風險、情境機率與回撤區間","cause":"方法變動","prior_field":["trap","p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份：價值陷阱風險低；多頭機率25%、空頭28%；最大回撤−50%","side_b":"本次：價值陷阱風險中（十項衰退信號亮1項：EPS成長高於營收超過5pp）；多頭20%、基準50%、空頭30%；最大回撤區間−33%～−50%","ruling":"改用十項衰退信號逐條計數，共識EPS兩年年化19.0%對營收約11.9%差距超過5pp亮燈，雖屬利潤率擴張與回購的良性來源，仍按計數給中風險；共識成長超過內生上界，空頭機率不低於30%，並把循環中段的下行風險從多頭機率扣出5pp；回撤改為區間表達","evidence_level":"高（數字取自事實表共識與年度財報）","settle_metric":"FY2027實際EPS對營收成長差、衰退信號亮燈數","if_then":["若亮燈數升至3項以上→陷阱風險改高，減碼至半倉","若2028年EPS成長回到與營收同步且利潤率守住→陷阱風險回低"],"evidence_refs":[]},{"axis":"加碼條件（前份觸發器已發火）","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"starter 1/3；加碼＝S32N 或 S32K5 宣告量產時點，或回落 $230 以下","side_b":"加碼＝S32K5量產出貨經財報確認（最早2027年Q1），或股價≤$230且book-to-bill仍>1；前份「宣告量產時點」已在Q3法說觸發，改以實際出貨為準","ruling":"前份加碼條件「宣告量產時點」在Q3財報會議文字上已觸發：執行長宣告S32K5最早2027年Q1在中國首批出貨、S32N 2027年底初步放量、2028年全面放量。但宣告時點不等於出貨，且循環已進中段，本次不據此加碼，把加碼條件收緊為實際出貨經財報確認；價格條件維持230美元並加上訂單未反轉的前提","evidence_level":"高（Q3財報會議逐字稿）","settle_metric":"S32K5出貨確認、股價、book-to-bill","if_then":["若2027年Q1或Q2財報確認S32K5出貨→加碼至目標倉位2/3","若股價跌破230美元且book-to-bill仍高於1→分批加碼"],"evidence_refs":[]},{"axis":"出場門檻（減碼／清倉）","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設出場指標（null）","side_b":"book-to-bill跌破1或通路庫存超過13週→減碼至半倉；non-GAAP毛利率連2季低於57%且SDV 20億美元目標下修→清倉；股價超過400美元且共識未上修→減碼1/3","ruling":"前份缺可量化的減碼與清倉門檻，本次補上；門檻取自循環領先指標與毛利率假設底線","evidence_level":"中","settle_metric":"各季財報","if_then":["任一減碼門檻觸發→減碼至半倉","清倉兩條件同時成立→清倉"],"evidence_refs":[]},{"axis":"唯一致命點（Single Thing）","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份Single Thing未設（null）","side_b":"2027年內任一季，管理層在財報會議揭露整體book-to-bill跌破1（訂單由催貨轉為取消或延後）","ruling":"依敏感度選定Single Thing：訂單反轉使營收約−15%、EPS約−20%以上，遠大於毛利率每1pp約3%的影響，且會同時撞上新產能折舊起跑","evidence_level":"中","settle_metric":"book-to-bill口述","if_then":["若發生→減碼至半倉並停止加碼","若同季通路庫存超過13週或毛利率指引低於57%→清倉"],"evidence_refs":[]},{"axis":"假設與風險改寫","cause":"方法變動","prior_field":["H","R"],"side_a":"前份三假設（SDV單車價值、工業／資料中心第二引擎、毛利率結構性擴張）與三風險（2027循環回落加晶圓成本、新戰場強敵併購、中國國產化）","side_b":"本次假設方向不變，改寫為帶數字門檻、資料來源與漂移觸發的版本；風險擴為五條，新增通路集中與南韓反壟斷審議、上游代工價值鏈分配兩條","ruling":"假設沒有被推翻，Q3數據（車用扣感測器+17%、工業近+50%、資料中心目標上調）是支持證據；改寫原因是補足門檻與來源，並把前份未處理的通路與監管風險納入","evidence_level":"高","settle_metric":"各假設門檻","if_then":["任一假設達反轉級→停止加碼並減碼1/3","兩條假設同時反轉→清倉"],"evidence_refs":["customer_concentration_credit#2","regulatory_antitrust#0"]}],"triggers":[{"n":1,"text":"SDV年化營收達20億美元並確認S32K5首批出貨","type":"假設驗證","maps_to":"H1","metric":"SDV年化營收；S32K5出貨","threshold":"2027年Q4財報SDV年化≥20億美元","action":"達標維持；未達或目標延後則停止加碼","source_freq":"季報與財報會議（每季）","date":"2028-02"},{"n":2,"text":"資料中心營收朝10億美元前進","type":"假設驗證","maps_to":"H2","metric":"資料中心營收（2027年新分部揭露）","threshold":"2027年≥7億美元、2028年≥10億美元","action":"連兩次更新延後則停止加碼","source_freq":"季報與投資人日","date":"2027-03-03"},{"n":3,"text":"毛利率60%目標","type":"假設驗證","maps_to":"H3","metric":"non-GAAP毛利率","threshold":"2027年任一季≥60%；2027年Q2仍低於59%即落後","action":"落後則停止加碼","source_freq":"季報新聞稿（每季）","date":"2027-07"},{"n":4,"text":"整體book-to-bill跌破1","type":"Single Thing","maps_to":"R1","metric":"book-to-bill（財報會議口述）","threshold":"低於1","action":"減碼至半倉並停止加碼","source_freq":"每季財報會議","date":null,"evidence_refs":["capital_markets_pricing#4"]},{"n":5,"text":"通路與資產負債表庫存升溫","type":"風險","maps_to":"R1","metric":"通路庫存週數；扣預建庫存天數","threshold":"通路超過13週，或扣預建庫存天數連2季超過140天","action":"減碼1/3","source_freq":"每季","date":null,"evidence_refs":["supply_demand_durability#1"]},{"n":6,"text":"南韓公平會裁決Ship & Debit經銷安排","type":"風險","maps_to":"R4","metric":"罰款金額與改正命令範圍","threshold":"罰款超過約3,500萬美元（相關銷售額8.8億美元的4%）或要求改變經銷機制，或歐美主管機關跟進調查","action":"僅罰款不動作；機制改變或跟進調查則停止加碼至下一季財報量化影響","source_freq":"南韓公平會公告（不定期）","date":null,"evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#2"]},{"n":7,"text":"關稅與出口管制吸收失敗","type":"風險","maps_to":"R2","metric":"non-GAAP毛利率指引","threshold":"因關稅或出口限制下修≥100bp","action":"減碼1/3","source_freq":"季報指引","date":null,"evidence_refs":["reg_tariff_export#0","reg_tariff_export#1"]},{"n":8,"text":"S32K5量產出貨經財報確認","type":"加碼","maps_to":"H1","metric":"S32K5出貨確認","threshold":"財報或新聞稿確認量產出貨","action":"加碼至目標倉位2/3","source_freq":"季報","date":"2027-04"},{"n":9,"text":"股價回到230美元以下且訂單未反轉","type":"估值rearm","maps_to":"R1","metric":"股價；book-to-bill","threshold":"股價≤230美元（約FY2027共識12.6倍）且book-to-bill仍高於1","action":"分批加碼","source_freq":"每日股價＋每季財報","date":null},{"n":10,"text":"估值過熱","type":"減碼","maps_to":null,"metric":"股價對FY2027共識EPS本益比","threshold":"股價超過400美元（約FY2027共識22倍）且共識未同步上修","action":"減碼1/3","source_freq":"每日股價＋共識快照","date":null},{"n":11,"text":"毛利率與SDV雙破","type":"清倉","maps_to":"H3","metric":"non-GAAP毛利率；SDV目標","threshold":"毛利率連2季低於57%且SDV 20億美元目標下修","action":"清倉","source_freq":"季報","date":null},{"n":12,"text":"Q4財報與投資人日後重跑完整研究","type":"複審日期","maps_to":null,"metric":"2027年指引、長期財務模型、新分部口徑","threshold":"日期到達","action":"重跑完整研究","source_freq":"公司公告","date":"2027-03-03"}],"kill_metrics":[{"metric":"整體book-to-bill（財報會議口述）","bear_threshold":"跌破1","window":"2026Q4–2028Q4各季財報","source":"NXP季度財報會議逐字稿","last_status":"ok"},{"metric":"non-GAAP毛利率","bear_threshold":"連2季低於57%","window":"2027–2028年","source":"NXP季報新聞稿（SEC 8-K Ex.99.1）","last_status":"ok"},{"metric":"通路庫存週數","bear_threshold":"超過13週","window":"每季","source":"NXP財報會議與新聞稿","last_status":"ok"},{"metric":"SDV年化營收","bear_threshold":"2027年Q4低於18億美元或20億目標下修","window":"至2028年2月","source":"NXP財報會議","last_status":"ok"},{"metric":"車用營收年增率（扣感測器）","bear_threshold":"連2季低於5%","window":"2027–2028年","source":"NXP季報新聞稿","last_status":"ok"}],"evidence_dismissed":[],"action_conditions":{"rearm_trigger":"加碼＝S32K5量產出貨經財報確認（最早2027年Q1），或股價≤$230且book-to-bill仍>1；前份「宣告量產時點」已在Q3法說觸發，改以實際出貨為準","exec_line":"首倉1/3可於現價建立或維持，不追高；加碼兩條件擇一（S32K5出貨經財報確認／股價≤230美元且訂單未反轉）；book-to-bill跌破1或通路庫存超過13週減碼至半倉；毛利率連2季低於57%且SDV目標下修清倉；股價超過400美元且共識未上修減碼1/3"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":"中循環","cycle_verdict":"右側可追蹤","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場把循環高點與結構成長混為一談：26週股價−11.4%而同期non-GAAP EPS年增35%、FY2027本益比僅14倍，隱含利潤率將大幅回落；我們認為SDV內容提升在汽車平產量下仍貢獻車用扣感測器+17%，下一次去化應淺於市場定價","momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":null,"wait_for_price_condition":null,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null},"thesis":{"H":[{"id":"H1","text":"SDV區域／中央運算轉換讓NXP每車價值在汽車平產量下持續上升，S32K5／S32N依時程接棒","2y":"2027年SDV年化營收≥20億美元，S32K5於2027年上半年開始出貨","5y":"2028年起區域與中央運算全面放量，車用營收年增率連續高於全球汽車產量年增率至少8pp","10y":null,"threshold":"SDV年化營收2027年Q4≥20億美元；車用營收（扣感測器）年增≥10%","source":"公司季報新聞稿與財報會議（SDV年化營收、車用分部營收）；2027年起分部重分類需以新口徑對照","drift_rule":"車用TTM年增率連2季落後門檻至少5%為削弱，連3季落後至少10%為反轉；SDV目標下修即削弱"},{"id":"H2","text":"工業與IoT加資料中心控制平面成為第二引擎，成長來自邊緣AI處理器內容而非庫存回補","2y":"資料中心2026年超過5億美元、2028年≥10億美元；工業與IoT 2027年年增≥15%","5y":"AI處理器占工業與IoT處理器營收由2026年約15%升至至少30%","10y":null,"threshold":"資料中心營收2028年≥10億美元；工業與IoT 2027年年增≥15%","source":"財報會議資料中心營收更新、2027年新分部揭露、2027-03-03投資人日","drift_rule":"工業與IoT TTM年增率連2季低於門檻至少5%為削弱、連3季至少10%為反轉；資料中心10億美元目標延後至2029年以後即削弱"},{"id":"H3","text":"毛利率擴張是結構性的：稼動率、產品組合與VSMC自製（12吋取代8吋、免代工加價）共同推升，2027年達60%、2028年再往上","2y":"2027年任一季non-GAAP毛利率≥60%，全年≥59%","5y":"VSMC量產後2028–2030年non-GAAP毛利率維持≥60%，含一次景氣修正時谷底不低於57%","10y":null,"threshold":"non-GAAP毛利率2027年達60%、谷底不低於57%","source":"季報新聞稿non-GAAP毛利率與CFO指引","drift_rule":"季毛利率連2季低於門檻至少3pp（約5%）為削弱，連3季至少6pp（約10%）為反轉"}],"R":[{"id":"R1","text":"重複下單在2027年下半年反轉：交期拉長、催貨增加、OEM討論安全庫存，2028年遇上新廠產能開出與中國成熟製程擴產，車用與工業去化","h_ref":"H1,H3","clock":"🔥","threshold":"book-to-bill低於1，或通路庫存超過13週，或扣預建庫存天數連2季超過140天","evidence_refs":["supply_demand_durability#1","capital_markets_pricing#0","capital_markets_pricing#4"]},{"id":"R2","text":"中國本土化與美中貿易限制：中國車廠改用本土MCU，加上232半導體關稅第二階段與出口管制","h_ref":"H1","clock":"🐢","threshold":"公司揭露中國區營收年減，或232第二階段關稅涵蓋車用／工業晶片且毛利率指引因此下修≥100bp","evidence_refs":["competitive_share_entrants#2","reg_tariff_export#0","reg_tariff_export#1"]},{"id":"R3","text":"價值鏈被上游吃掉：2027年代工存取費重簽，前段多仰賴台積電體系合資廠，即時採購模式暴露供應中斷；資本支出由約2%升至約5%","h_ref":"H3","clock":"🔥","threshold":"2027年non-GAAP毛利率未達59%，或TTM自由現金流率低於20%","evidence_refs":["geo_supply_chain#2"]},{"id":"R4","text":"通路集中與監管：Avnet占23%營收且逐年微升，南韓公平會審議Ship & Debit獨家經銷與利潤預設，若改正命令擴大可能動到通路定價機制","h_ref":"H1,H2","clock":"🔥","threshold":"南韓裁罰超過約3,500萬美元或要求改變經銷機制，或歐美主管機關跟進調查，或單一通路商占比超過25%","evidence_refs":["customer_concentration_credit#2","regulatory_antitrust#0","regulatory_antitrust#2"]},{"id":"R5","text":"規模更大的對手與併購新進者：Infineon買Marvell車用乙太網路、Microchip買Hailo、onsemi併Synaptics，攻NXP的車載交換器與邊緣AI","h_ref":"H2","clock":"🐢","threshold":"NXP失去多Gb乙太網路交換器或S32N主要設計案，或公司特有車用成長動能年增率低於10%","evidence_refs":["competitive_share_entrants#0"]}],"single_thing":{"description":"2027年內任一季，管理層在財報會議揭露整體book-to-bill跌破1（訂單由催貨轉為取消或延後）","why_fatal":"情境樹中基準與空頭自2028年分岔，來源就是訂單反轉：營收約−15%在約50%遞減利潤率下使EPS約−20%以上，且同時撞上VSMC／ESMC／馬來西亞新產能折舊起跑，毛利率60%目標與回購節奏一起失效；毛利率每1pp只影響EPS約3%，敏感度小一個量級","if_happens":"減碼至半倉並停止所有加碼；若同季通路庫存超過13週或毛利率指引低於57%，清倉","how_monitor":"每季財報會議的book-to-bill口述、交期超過16週產品占比（目前80%）、客戶催貨數、通路庫存週數（目前11週）、扣預建庫存天數","probability":"約35%（12–24個月）：後段產能吃緊與OEM安全庫存討論是典型中後段信號；第三方推估供過於求最早2028年，訂單反轉通常領先營收2–4季"}},"appendix_a":{"growth_durability":7,"quality_score":7,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":14.17,"peg_fy2":0.74,"stress":{"pass":7,"total":10}},"eps_meta":{"base_eps_path":{"FY2025A":null,"FY2026E":15.16,"FY2027E":18.32,"FY2028E":21.48},"fy_end_month":12,"eps_basis":"non-GAAP稀釋EPS（Koyfin共識，2026-10-31快照）；FY2025A non-GAAP全年實績事實表未涵蓋，GAAP稀釋EPS 7.95口徑不同不採用；共識年化以FY2026E→FY2028E兩年19.0%計"},"catalysts":[{"date":"2027-02","date_precision":"month","type":"guidance","event":"Q4 2026財報與2027年Q1指引，首度以新分部口徑揭露","impact":"高","watch":"Q1營收季減是否優於−5%、book-to-bill是否仍高於1"},{"date":"2027-03-03","date_precision":null,"type":"guidance","event":"波士頓投資人日，更新策略與長期財務模型","impact":"高","watch":"長期毛利率目標是否超過60%、資料中心投資與回購規模"},{"date":"2027-Q1","date_precision":"quarter","type":"product","event":"S32K5最早在中國首批出貨","impact":"中","watch":"是否如期出貨並在財報確認"},{"date":"2027-Q3","date_precision":"quarter","type":"capacity","event":"VSMC 12吋首批NXP產品產出（第一批技術驗證中）","impact":"中","watch":"2028年毛利率超過60%的路徑是否成立"},{"date":null,"date_precision":null,"type":"regulatory","event":"南韓公平會對Ship & Debit經銷安排的裁決","impact":"低","watch":"罰款是否超過相關銷售額4%（約3,500萬美元）及改正命令範圍"}],"decision_out":{"verdict":"進場","role":"衛星","row_hit":"9","pacing":[],"holding_cap":null,"audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場把循環高點與結構成長混為一談：26週股價−11.4%而同期non-GAAP EPS年增35%、FY2027本益比僅14倍，隱含利潤率將大幅回落；我們認為SDV內容提升在汽車平產量下仍貢獻車用扣感測器+17%，下一次去化應淺於市場定價"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟢', val='🟢', moat_trend='→', week26=-11.37, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position='中循環', moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":false,"basis":"signal='B', val='🟢'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":true,"basis":"signal='B', val='🟢', ma='🟡'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟢', ma='🟡'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟢', ma='🟡'"},{"row":"9-verdict","condition":"命中 row9 → 進場","hit":true,"basis":"row_hit=9"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]}],"requires_critic":[]}}
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
