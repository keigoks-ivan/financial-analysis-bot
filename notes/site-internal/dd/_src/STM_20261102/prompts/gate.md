你是 DD 管線 v20 的判斷層閘（gate），標的 STM（20261102）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（52 條）
- `f_kpi0_net_revenues_gaap`（q1_business）｜Net revenues (GAAP)＝3757 US$M｜期間與口徑：Q3 2026（季末 2026-09-26，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 6-K 新聞稿（PR C3419C，SEC 存檔）https://www.sec.gov/Archives/edgar/data/0000932787/000093278726000086/c3419c-q326earningspressre.htm；IR 入口 https://investors.st.com（numbers.latest_quarter_kpis.items[0]，as_of Q3 2026（季末 2026-09-26，公告於 2026-10-29））
- `f_kpi1_non_gaap_operating_incom`（q1_business）｜Non-GAAP operating income / margin＝429 US$M（利益率 11.4%）｜期間與口徑：Q3 2026（季末 2026-09-26，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 6-K 新聞稿（PR C3419C，SEC 存檔）https://www.sec.gov/Archives/edgar/data/0000932787/000093278726000086/c3419c-q326earningspressre.htm；IR 入口 https://investors.st.com（numbers.latest_quarter_kpis.items[1]，as_of Q3 2026（季末 2026-09-26，公告於 2026-10-29））
- `f_kpi2_gaap_operating_income_ma`（q1_business）｜GAAP operating income / margin＝367 US$M（利益率 9.8%）｜期間與口徑：Q3 2026（季末 2026-09-26，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 6-K 新聞稿（PR C3419C，SEC 存檔）https://www.sec.gov/Archives/edgar/data/0000932787/000093278726000086/c3419c-q326earningspressre.htm；IR 入口 https://investors.st.com（numbers.latest_quarter_kpis.items[2]，as_of Q3 2026（季末 2026-09-26，公告於 2026-10-29））
- `f_kpi3_free_cash_flow_non_gaap`（q1_business）｜Free cash flow (non-GAAP)＝351 US$M（營運現金流 1,020；淨資本支出 643）｜期間與口徑：Q3 2026（季末 2026-09-26，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 6-K 新聞稿（PR C3419C，SEC 存檔）https://www.sec.gov/Archives/edgar/data/0000932787/000093278726000086/c3419c-q326earningspressre.htm；IR 入口 https://investors.st.com（numbers.latest_quarter_kpis.items[3]，as_of Q3 2026（季末 2026-09-26，公告於 2026-10-29））
- `f_kpi4_gross_margin_gaap`（q1_business）｜Gross margin (GAAP)＝37.3 %｜期間與口徑：Q3 2026（季末 2026-09-26，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 6-K 新聞稿（PR C3419C，SEC 存檔）https://www.sec.gov/Archives/edgar/data/0000932787/000093278726000086/c3419c-q326earningspressre.htm；IR 入口 https://investors.st.com（numbers.latest_quarter_kpis.items[4]，as_of Q3 2026（季末 2026-09-26，公告於 2026-10-29））
- `f_kpi5_inventory_days_dsi`（q1_business）｜Inventory days (DSI)＝126 days（存貨 US$3.25B）｜期間與口徑：Q3 2026（季末 2026-09-26，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 6-K 新聞稿（PR C3419C，SEC 存檔）https://www.sec.gov/Archives/edgar/data/0000932787/000093278726000086/c3419c-q326earningspressre.htm；IR 入口 https://investors.st.com（numbers.latest_quarter_kpis.items[5]，as_of Q3 2026（季末 2026-09-26，公告於 2026-10-29））
- `f_kpi6_guidance_q4_2026_revenue`（q1_business）｜Guidance Q4 2026 revenue (midpoint)＝4150 US$M（±350bps，約 4,005–4,295 為區間推算）｜期間與口徑：Q3 2026（季末 2026-09-26，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司 6-K 新聞稿（PR C3419C，SEC 存檔）https://www.sec.gov/Archives/edgar/data/0000932787/000093278726000086/c3419c-q326earningspressre.htm；IR 入口 https://investors.st.com（numbers.latest_quarter_kpis.items[6]，as_of Q3 2026（季末 2026-09-26，公告於 2026-10-29））
  - 註記：Q4 共識營收約 4.10B（來源：web_search 報導引 LSEG，未直接核對）
- `f_kpi7_guidance_q4_2026_gross_m`（q1_business）｜Guidance Q4 2026 gross margin (midpoint)＝39.0 %（±200bps，含約 40bps 閒置產能費用）｜期間與口徑：Q3 2026（季末 2026-09-26，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司 6-K 新聞稿（PR C3419C，SEC 存檔）https://www.sec.gov/Archives/edgar/data/0000932787/000093278726000086/c3419c-q326earningspressre.htm；IR 入口 https://investors.st.com（numbers.latest_quarter_kpis.items[7]，as_of Q3 2026（季末 2026-09-26，公告於 2026-10-29））
- `f_kpi8_guidance_fy2026_revenue`（q1_business）｜Guidance FY2026 revenue＝14500 US$M（約，YoY +22.8%；毛利率 GAAP 約 36.4%／non-GAAP 約 36.6%）｜期間與口徑：Q3 2026（季末 2026-09-26，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司 6-K 新聞稿（PR C3419C，SEC 存檔）https://www.sec.gov/Archives/edgar/data/0000932787/000093278726000086/c3419c-q326earningspressre.htm；IR 入口 https://investors.st.com（numbers.latest_quarter_kpis.items[8]，as_of Q3 2026（季末 2026-09-26，公告於 2026-10-29））
- `f_peer_stm_gross_margin_pct`（q2_moat）｜STM 毛利率＝33.84 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.STM.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_stm_operating_margin_pct`（q2_moat）｜STM 營業利益率＝6.64 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.STM.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_stm_fcf_margin_pct`（q2_moat）｜STM FCF 利潤率＝3.77 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.STM.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
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
- `f_peer_on_gross_margin_pct`（q2_moat）｜ON 毛利率＝37.72 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ON.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_on_operating_margin_pct`（q2_moat）｜ON 營業利益率＝18.05 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ON.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_on_fcf_margin_pct`（q2_moat）｜ON FCF 利潤率＝24.21 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ON.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_adi_gross_margin_pct`（q2_moat）｜ADI 毛利率＝65.8 %｜期間與口徑：TTM ending 2026-07-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ADI.gross_margin_pct，as_of TTM ending 2026-07-31（4季加總））
- `f_peer_adi_operating_margin_pct`（q2_moat）｜ADI 營業利益率＝35.72 %｜期間與口徑：TTM ending 2026-07-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ADI.operating_margin_pct，as_of TTM ending 2026-07-31（4季加總））
- `f_peer_adi_fcf_margin_pct`（q2_moat）｜ADI FCF 利潤率＝35.57 %｜期間與口徑：TTM ending 2026-07-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ADI.fcf_margin_pct，as_of TTM ending 2026-07-31（4季加總））
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝1.34 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-10-31）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝2.7 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-10-31）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝3.79 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-10-31）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝14497.18 USD m｜期間與口徑：2026-11-02／yfinance revenue_estimate 0y 平均（9 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-02）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝17372.99 USD m｜期間與口徑：2026-11-02／yfinance revenue_estimate +1y 平均（16 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-02）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_consensus_rev_fy2_pct`（q5_valuation）｜FY2 共識修正＝1.5 %｜期間與口徑：2026-10-31／兩份 Koyfin 快照之間的 EPS 修正幅度（2.66 → 2.7）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.fy2.revision_pct，as_of 2026-10-31）
- `f_consensus_rev_fy3_pct`（q5_valuation）｜FY3 共識修正＝0.26 %｜期間與口徑：2026-10-31／兩份 Koyfin 快照之間的 EPS 修正幅度（3.78 → 3.79）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.fy3.revision_pct，as_of 2026-10-31）
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝-2106.0 USD m｜期間與口徑：2026-11-02／yfinance 最新一季：總債務 3206.0、現金 5312.0（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-02）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝894.41 m shares｜期間與口徑：2026-11-02／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-11-02）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝0.77 %｜期間與口徑：2026-11-02／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-11-02）
- `f_ev_m`（q5_valuation）｜目前企業價值 EV（市值＋淨負債）＝39698.95 USD m｜期間與口徑：2026-11-02／市值 41804.95 ＋ 淨負債 -2106.0｜kind：realized
  - 來源：—（numbers.capital_structure.ev_m，as_of 2026-11-02）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝46.74 USD｜期間與口徑：2026-10-30（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-10-30（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝34.88 x｜期間與口徑：2026-10-31／分母＝FY1 EPS 1.34，分子＝快照價 46.74｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-10-31）
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝82.0 x｜期間與口徑：2026-10-30（RTH 收盤，UTC）／4 個年度端點內的分位＝51.8｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-10-30（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝51.8 %｜期間與口徑：2026-10-30（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-10-30（RTH 收盤，UTC））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝3.06 x｜期間與口徑：2026-10-30（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-10-30（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝100.0 %｜期間與口徑：2026-10-30（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-10-30（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝2.9 x｜期間與口徑：2026-10-30（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-10-30（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝100.0 %｜期間與口徑：2026-10-30（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-10-30（RTH 收盤，UTC））
- `f_ev_s_fwd`（q5_valuation）｜EV/S（EV ÷ FY1 共識營收）＝2.74 x｜期間與口徑：2026-11-02／f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）｜kind：estimate
  - 來源：—（numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m，as_of 2026-11-02）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝-1.47 %｜期間與口徑：2026-07-30 → 2026-10-31／FY1 共識 EPS 1.36 → 1.34（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-10-31）
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝-15.92 %｜期間與口徑：2026-10-30（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-10-30（RTH 收盤，UTC））
- `f_rsi14`（q5_valuation）｜RSI(14)＝43.92｜期間與口徑：2026-10-30（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-10-30（RTH 收盤，UTC））
- `f_ma_state`（q5_valuation）｜週線均線六態（decision_inputs.ma 必須等於此值）＝🟡｜期間與口徑：2026-11-02／timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-02）
  - 原文：「price 46.74 / W52 44.9 / W104 35.15 / W250 37.73 / W250 13週斜率 -0.01%」
- `f_ma_w52`（q5_valuation）｜52 週均線＝44.9 USD｜期間與口徑：2026-11-02／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-02）
- `f_ma_slope_w250_pct`（q5_valuation）｜W250 13 週斜率＝-0.01 %｜期間與口徑：2026-11-02／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-02）
- `f_ma_w250`（q5_valuation）｜250 週均線＝37.73 USD｜期間與口徑：2026-11-02／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-02）
- `f_ma_w104`（q5_valuation）｜104 週均線＝35.15 USD｜期間與口徑：2026-11-02／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-02）

### findings_digest 中方向為負或來源衝突的條目（20 條）
- `competitive_share_entrants#0`（competitive_share_entrants｜方向 -｜狀態 ok）：ST 20-F 自述：競爭激烈，產業整併可能侵蝕市占；小型利基業者與（特別在亞洲的）晶圓代工業者участations明顯擴張。
  - 來源：SEC EDGAR 20-F FY2025 Item 4 Competition（as_of 2026-02-26）｜affects：moat_trend、decision_inputs.bear
- `competitive_share_entrants#1`（competitive_share_entrants｜方向 -｜狀態 ok）：ST 20-F 風險因子：整併可能導致市占流失，並需重組營運。
  - 來源：SEC EDGAR 20-F FY2025 Item 3 Risk Factors（as_of 2026-02-26）｜affects：moat_trend、thesis.R
- `competitive_share_entrants#3`（competitive_share_entrants｜方向 -｜狀態 ok）：中國本土 OEM（BYD、Nio、Geely、Xiaomi）擴大 SiC 布局，本土競爭升溫，ST 走在地化合資
  - 來源：Astute Group（as_of 2025-04-15）｜affects：moat_trend、decision_inputs.bear
- `customer_second_source#0`（customer_second_source｜方向 -｜狀態 ok）：STM 20-F FY2025 揭露：最大客戶 Apple 占 2025 年營收 17.7%；近年部分客戶垂直整合，可能影響業務，失去關鍵客戶或重要 socket 會有不利影響。
  - 來源：SEC EDGAR 20-F FY2025 Item 3 Risk Factors（as_of 2026-02-26）｜affects：thesis.R、decision_inputs.bear
- `customer_second_source#1`（customer_second_source｜方向 -｜狀態 ok）：20-F 競爭章節列明競爭者包括自行開發 IC 產品與晶圓廠營運的客戶，部分競爭者同時是客戶或供應商。
  - 來源：SEC EDGAR 20-F FY2025 Item 4（as_of 2026-02-26）｜affects：moat_trend
- `customer_second_source#2`（customer_second_source｜方向 -｜狀態 ok）：Bloomberg 報導（經 Finanzaonline 轉述）：Apple 招募工程師自研無線/RF 晶片，Equita 分析師認為對 Apple 供應鏈含 STM 為負面，STM 股價當日跌近 3%。
  - 來源：Finanzaonline: STMicroelectronics in caduta a Piazza Affari, Apple potrebbe sviluppare chip internamente（as_of 2026-01-01）｜affects：thesis.R、decision_inputs.bear
- `customer_concentration_credit#0`（customer_concentration_credit｜方向 -｜狀態 ok）：2025 年最大客戶 Apple 占 STM 營收 17.7%（2024 年 14.5%、2023 年 12.3%），逐年上升；公司稱不依賴單一客戶，但失去關鍵客戶或重要 socket 會有不利影響
  - 來源：SEC EDGAR 20-F FY2025 Item 3 / Item 5（as_of 2026-02-26）｜affects：thesis.R、decision_inputs.bear
- `regulatory_antitrust#1`（regulatory_antitrust｜方向 -｜狀態 ok）：產業監管：美國商務部依 232 條款對進口半導體啟動國安調查，可能帶來額外關稅與貿易限制。
  - 來源：SEC EDGAR 20-F FY2025 Item 3 Risk Factors（as_of 2026-02-26）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：STM 20-F 風險因子載明：美中關稅、出口限制與實體清單已限制或可能限制其與部分中國客戶／供應商交易；並點名美國威脅的 100% 晶片關稅與中國相關出口管制。
  - 來源：SEC EDGAR 20-F FY2025 Item 3.D（as_of 2026-02-26）｜affects：decision_inputs.bear、thesis.R
- `reg_tariff_export#1`（reg_tariff_export｜方向 -｜狀態 ok）：20-F 載明 2025 年 4 月美國商務部啟動半導體及設備進口的 Section 232 國安調查，可能帶來額外關稅與貿易限制。
  - 來源：SEC EDGAR 20-F FY2025 Item 3.D（as_of 2026-02-26）｜affects：decision_inputs.bear、thesis.R
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：ST 申報文件將地緣與軍事衝突列為其、客戶或供應商所在地區營運風險，並將關稅、貿易壁壘與制裁列為需求風險（屬一般性風險語言，非特定廠區評估）
  - 來源：STMicroelectronics Form 6-K Q2 2026 (SEC)（as_of 2026-07-23）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#2`（geo_supply_chain｜方向 -｜狀態 ok）：ST 20-F 揭露其依賴少數供應商取得材料、設備與授權技術，部分材料僅來自單一地區少數供應商（摘要轉述自歷年 20-F，未核 FY2025 頁面原文）
  - 來源：STMicroelectronics Form 20-F FY2025 (SEC)（as_of 2026-02-01）｜affects：thesis.R、decision_inputs.bear
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：STM 20-F 自述半導體產業技術變動快、產品週期短、價格侵蝕大，公司財務表現取決於能否掌握 AI、量子等新技術機會；未點名具體替代技術。
  - 來源：SEC EDGAR 20-F FY2025 Item 3.D Risk Factors（as_of 2026-02-26）｜affects：moat_trend、thesis.R
- `capital_markets_pricing#2`（capital_markets_pricing｜方向 -｜狀態 ok）：Q2 財報（2026-07-23）後 Q3 營收指引中點約 37 億美元，被報導為低於分析師預期，股價下跌；Barclays 於 2026-07-24 將目標價降至 $60。
  - 來源：goldesel.de / GuruFocus 引述 / Barclays 調整（as_of 2026-07-24）｜affects：valuation、decision_inputs.bear
- `major_events#1`（major_events｜方向 -｜狀態 ok）：SDNY 證券集體訴訟（2024-08-23 起，涵蓋期間擴至 2023-03-14～2025-01-29，指控 10(b)/20(a)）；法院 2025-09-15 駁回公司撤銷訴訟聲請，公司稱將積極抗辯。
  - 來源：SEC EDGAR 20-F FY2025 Note 26（as_of 2026-02-26）｜affects：decision_inputs.bear、thesis.R
- `major_events#2`（major_events｜方向 -｜狀態 ok）：Purdue University 專利侵權案：2024-06-07 法院判決公司賠 3,200 萬美元，公司提出審後動議，風險評為 possible，估計損失 3,200 萬美元。
  - 來源：SEC EDGAR 20-F FY2025 Note 26（as_of 2026-02-26）｜affects：thesis.R、decision_inputs.bear
- `cyclical_prior_downcycle_behavior#0`（cyclical_prior_downcycle_behavior｜方向 -｜狀態 ok）：STM 毛利率 2023 年 47.9% → 2024 年 39.3% → 2025 年 33.9%，2025 年降幅主因製造效率下降
  - 來源：STMicroelectronics Form 20-F FY2025（as_of 2026-02-01）｜affects：valuation、decision_inputs.bear
- `cyclical_prior_downcycle_behavior#2`（cyclical_prior_downcycle_behavior｜方向 -｜狀態 ok）：半導體族群上一輪下行：SOXX ETF 2021-12-27 至 2022-10-14 約跌 46%；另一來源稱 2022 全年約跌 35%（兩者不一致）
  - 來源：247wallst / Yahoo Finance: SOXL Lost 90 Percent in 2022 While Semiconductors Themselves Fell 35 Percent（as_of 2026-05-26）｜affects：valuation、decision_inputs.bear
- `lawsuit_class_action#0`（lawsuit_class_action｜方向 -｜狀態 ok）：SDNY 證券集體訴訟撤銷聲請於 2025-09-15 被駁回，案件續審。
  - 來源：SEC EDGAR 20-F FY2025 Note 26（as_of 2026-02-26）｜affects：decision_inputs.bear、thesis.R
- `lawsuit_class_action#1`（lawsuit_class_action｜方向 -｜狀態 ok）：Purdue 專利案判賠 3,200 萬美元，審後動議進行中。
  - 來源：SEC EDGAR 20-F FY2025 Note 26（as_of 2026-02-26）｜affects：thesis.R

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 15 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/STM_20261102/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":114.0,"bear_5y_price":28.8,"p_bull_pct":30,"p_bear_pct":30,"upside_5y_pct":34.8,"ev5y_pct":45.6,"irr_base_pct":6.2,"asym_ratio":3.7,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":1.34,"pe":34.88,"basis":"FY1（FY2026E，當年度）共識 EPS 1.34 美元，對判斷日股價 46.74 美元；終端倍數同樣套在終端年當年度的 EPS（FY2031E），分母同口徑"},"eps":{"bull":[2.95,4.3,4.8,5.4,6.0],"base":[2.55,3.4,3.3,3.8,4.2],"bear":[2.2,2.4,1.6,2.0,2.4]},"pe":{"bull":19,"base":15,"bear":12},"p":{"bull":30,"base":40,"bear":30},"yield_pct":{"dividend":0.77,"net_buyback":0.4},"second_stage":{"bull_cagr_pct":8,"base_cagr_pct":5},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### STM_Q2_2026_Earnings_Call_20260723.md
- 2026-07-23｜Jean-Marc Chery｜guidance：CEO 給 Q3 毛利率指引約 37%（原話："We expect our gross margin to be about 37%"）
- 2026-07-23｜Jean-Marc Chery｜guidance：CEO 預期 Q4 營收高於 40 億美元（原話："We expect Q4 revenues to be above $4 billion"）
- 2026-07-23｜Jean-Marc Chery｜guidance：資料中心 2026 營收預期上調至逾 10 億美元（原話："We now expect revenues above $1 billion in 2026"）
- 2026-07-23｜Jean-Marc Chery｜guidance：資料中心 2027 營收預期遠高於 20 億美元（原話："well above $2 billion in 2027"）
- 2026-07-23｜Lorenzo Grandi｜guidance：Q3 non-GAAP 營業費用預期約 9.8 億美元（原話："net OpEx to stand at about $980 million"）
- 2026-07-23｜Lorenzo Grandi｜guidance：2026 淨資本支出預期落在 20–22 億區間高端（原話："2026 net CapEx to be at the high end"）
- 2026-07-23｜Jean-Marc Chery｜guidance：Q3 展望不含進一步關稅變動（原話："does not include any impact for potential further"）
- 2026-07-23｜Jean-Marc Chery｜guidance：個人電子 Q3 成長低於正常季節性（原話："below normal seasonality in Q3"）
- 2026-07-23｜Jean-Marc Chery｜guidance：通訊設備與電腦周邊 Q4 年增約 90%（原話："we will be about 90% growth"）
- 2026-07-23｜Marco Cassis｜guidance：SiC 2026 營收預期雙位數成長（原話："we should grow the silicon carbide revenues double digit"）
- 2026-07-23｜Remi El-Ouazzane｜guidance：太空/LEO 2026–2028 累計營收預期逾 30 億美元（原話："we stick to well above $3 billion over '26, '27, '28"）
- 2026-07-23｜Lorenzo Grandi｜margin：Q2 毛利率含製造重整一次性成本負面影響約 60bp（原話："about 60 basis points of negative impact"）
- 2026-07-23｜Lorenzo Grandi｜margin：Q4 毛利率較 Q3 的 37% 環比改善，但有暫時性逆風（原話："I confirm that in Q4, there will be an"）
- 2026-07-23｜Lorenzo Grandi｜margin：Q4 匯率效果中性，不再如 Q3 有助益（原話："It will be neutral"）
- 2026-07-23｜Lorenzo Grandi｜margin：資料中心產品組合對毛利率正貢獻（原話："product mix is contributing in a positive way"）
- 2026-07-23｜Lorenzo Grandi｜margin：毛利率 40% 以上模型需等製造重整完成，預計 2027 年底（原話："we confirm our model to be, let's say, above 40%"）
- 2026-07-23｜Lorenzo Grandi｜margin：Power & Discrete 部門 Q2 non-GAAP 營業利益率為負 21.4%（原話："Power & Discrete at minus 21.4%"）
- 2026-07-23｜Lorenzo Grandi｜margin：漲價與投入成本上漲目前大致互抵（原話："the 2 impacts are more or less offsetting each other"）
- 2026-07-23｜Jean-Marc Chery｜commitment：確認 2028 年營收 180 億美元目標（原話："confidence level to reach $18 billion in 2028"）
- 2026-07-23｜Jean-Marc Chery｜commitment：200 億美元目標暫不討論，先達成 180 億（原話："let's reach together the $18 billion"）
- 2026-07-23｜Lorenzo Grandi｜commitment：製造重整計畫預計 2027 年底完成（原話："it will be at the end of 2027, not before"）
- 2026-07-23｜Jean-Marc Chery｜commitment：2026 資料中心訂單 100% 已覆蓋（原話："Backlog for this year, 100% coverage."）
- 2026-07-23｜Jean-Marc Chery｜risk：部分產品供給吃緊、交期拉長（原話："some tension on the supply"）
- 2026-07-23｜Jean-Marc Chery｜risk：傳統類比產線 Q2 爬坡延遲影響 Q3 供貨（原話："pure legacy analog technologies"）
- 2026-07-23｜Remi El-Ouazzane｜risk：其他星座業者近期遇到問題（原話："Other constellation have faced a bit of a snag"）
- 2026-07-23｜Lorenzo Grandi｜risk：閒置產能費用 Q4 不會明顯下降（原話："will not change significantly in Q4"）
- 2026-07-23｜Jean-Marc Chery｜customer：Q2 book-to-bill 接近 2（原話："book-to-bill close to 2 overall"）
- 2026-07-23｜Jean-Marc Chery｜customer：Q2 訂單超過半數為明年（原話："well above 50% were for next year"）
- 2026-07-23｜Jean-Marc Chery｜customer：在手訂單約相當 4.5–5 個季度營收（原話："4.5 to 5 quarters of Q2 average revenue"）
- 2026-07-23｜Remi El-Ouazzane｜customer：資料中心營收分布與超大規模業者市占相近（原話："quite confident about the composition of our revenue"）
- 2026-07-23｜Jean-Marc Chery｜customer：Q1 2027 訂單負載良好（原話："Q1 is today on the dynamic to be well loaded"）
- 2026-07-23｜Remi El-Ouazzane｜product：矽光子不受產能擴充限制（原話："we are not right now gated by capacity expansion"）
- 2026-07-23｜Jean-Marc Chery｜product：Crolles 產能將達每週 15,000 片（原話："Crolles will reach 15,000 wafer per week"）
- 2026-07-23｜Lorenzo Grandi｜competition：對選定產品漲價（原話："we're increasing the prices on selected"）
- 2026-07-23｜Lorenzo Grandi｜capital_allocation：發行 15 億美元可轉債（原話："ST issued a new $1.5 billion dual tranche"）
- 2026-07-23｜Jean-Marc Chery｜product：中國製造夥伴 14nm 製程已認證，中國供中國策略（原話："China for China strategy that will start to pay back"）
- 2026-07-23｜Jean-Marc Chery｜customer：通訊設備與電腦周邊 Q3 年增近 60%（原話："this segment will grow very similarly"）

### STM_Shareholder_Analyst_Call_STMicroelectronics_N_V_20260309.md
- 2026-03-09｜Remi El-Ouazzane｜guidance：管理層上調資料中心營收預期：2026 年明顯高於 5 億美元、2027 年遠高於 10 億美元（含光互連與 AI 伺服器電源/類比）（原話："nicely above $500 million of revenue in 2026"）
- 2026-03-09｜Remi El-Ouazzane｜guidance：管理層預期 800V 架構於 2027 年開始放量，效益延伸至 2027 年之後（原話："volt architecture to start to ramp in '27"）
- 2026-03-09｜Remi El-Ouazzane｜guidance：管理層表示 NPO 將自 2027 下半年起在 AI 叢集出現（原話："you will start to see NPO from second half '27"）
- 2026-03-09｜Remi El-Ouazzane｜guidance：管理層個人看法：scale-up 機架於 2030 年達 100% 光學化（原話："100% coverage in 2030 is my opinion."）
- 2026-03-09｜Remi El-Ouazzane｜margin：管理層以每 GW 資料中心基礎設施約 2.3 億美元的 SAM 作為市場口徑（而非總市場金額）（原話："We see around $230 million."）
- 2026-03-09｜Remi El-Ouazzane｜margin：該 SAM 由約 400 款產品支撐（原話："backed up by about 400 products"）
- 2026-03-09｜Remi El-Ouazzane｜margin：管理層說明 2.3 億美元 SAM 僅以可插拔光學為基礎，NPO 成長尚未計入（原話："it's only based on pluggable optics."）
- 2026-03-09｜Remi El-Ouazzane｜margin：管理層說明 NPO 成長不在 2.3 億美元內，將疊加其上（原話："We have not included the growth of NPO."）
- 2026-03-09｜Remi El-Ouazzane｜margin：管理層明言不拆分 5 億/10 億美元的光子與電源組成（原話："but we have decided actually not to break it down"）
- 2026-03-09｜Remi El-Ouazzane｜margin：管理層解釋刻意不給總 SAM 金額，因 GW 部署量持續變動（原話："it's on purpose we've not done it."）
- 2026-03-09｜Remi El-Ouazzane｜commitment：矽光子產能擴張超過四倍（2027 年對比現況）（原話："more than quadruple our output by '27"）
- 2026-03-09｜Remi El-Ouazzane｜commitment：產能擴張由客戶長期產能預留承諾支撐（原話："fully backed by long-term capacity reservation commitments"）
- 2026-03-09｜Remi El-Ouazzane｜commitment：與 AWS 的多年期、數十億美元商業合作（原話："multibillion dollar commercial engagement"）
- 2026-03-09｜Remi El-Ouazzane｜commitment：管理層稱到今年產品供應可涵蓋整個 2.3 億美元 SAM（原話："By this year, we can cover the entire $230 million"）
- 2026-03-09｜Remi El-Ouazzane｜capital_allocation：資本支出維持 20～22 億美元區間但重新配置以加速矽光子（原話："billion to $2.2 billion envelope, but remixing it"）
- 2026-03-09｜Remi El-Ouazzane｜capital_allocation：管理層不提供絕對 CapEx 金額（原話："CapEx number dollar to share with you."）
- 2026-03-09｜Remi El-Ouazzane｜capital_allocation：目前新增矽光子產能 100% 在前段製程（原話："Today, these announcement is 100% front-end."）
- 2026-03-09｜Remi El-Ouazzane｜product：PIC100 於 300mm 進入量產，供應主要超大規模客戶（原話："PIC100 in 300 millimeter for leading hyperscalers."）
- 2026-03-09｜Remi El-Ouazzane｜product：800V DC 架構尚未進入量產（原話："it's not involved in volume production yet."）
- 2026-03-09｜Remi El-Ouazzane｜product：局部轉換 50V 轉 12V 已與主要客戶量產（原話："in production with key customers on the 50-volt to 12-volt"）
- 2026-03-09｜Remi El-Ouazzane｜product：管理層認為 NPO 將是未來五年主流（原話："NPO will be the winner for the 5 years to come."）
- 2026-03-09｜Remi El-Ouazzane｜product：Crolles 以閘道分批加產能，客戶無需重新認證（原話："copy exact of the previous gateway."）
- 2026-03-09｜Remi El-Ouazzane｜competition：管理層承認 ST 在 54V 架構的電源市場過去僅是邊緣角色（原話："we have been actually marginal as the players."）
- 2026-03-09｜Remi El-Ouazzane｜competition：管理層稱 EIC 已是市場領導者；PIC 目標為市場領導（以 30% 起算）（原話："We are the market leader today."）
- 2026-03-09｜Remi El-Ouazzane｜competition：PIC 方面管理層表示想成為市場領導者（原話："we want to become the market leader."）
- 2026-03-09｜Remi El-Ouazzane｜competition：客戶通常採最佳組合方式採購 MCU/EIC/PIC，非必須同一供應商（原話："is more a best-of-breed approach."）
- 2026-03-09｜Remi El-Ouazzane｜risk：管理層預期未來 2～3 年相關技術供應吃緊（原話："there will be a lot of supply challenges in the industry."）
- 2026-03-09｜Remi El-Ouazzane｜risk：管理層稱銅與光學之爭是時間問題而非是否發生（原話："So I think it's a question of when, not a question of if."）
- 2026-03-09｜Remi El-Ouazzane｜risk：管理層說明 1.6T 轉換加速，光子將成為明日瓶頸（原話："the transition to 1.6T is completely accelerating"）
- 2026-03-09｜Remi El-Ouazzane｜customer：長期產能預留客戶分散，涵蓋晶片、模組與超大規模業者（原話："It's actually more diversified thing, Amelia."）

### STM_Shareholder_Analyst_Call_STMicroelectronics_N_V_20260504.md
- 2026-05-04｜Remi El-Ouazzane｜guidance：管理層回應提問時重申 2026–2028 太空業務（LEO 加傳統太空）累計營收目標遠高於 30 億美元（原話："cumulative revenues of well above $3 billion for space as a"）
- 2026-05-04｜Remi El-Ouazzane｜guidance：管理層表示 2026 年太空營收可能已接近 10 億美元（原話："we may already be close to $1 billion"）
- 2026-05-04｜Remi El-Ouazzane｜guidance：ST 對 LEO 寬頻電子 SAM 的估計：2028 年約 20 億美元（原話："growing to roughly $2 billion in 2028"）
- 2026-05-04｜Remi El-Ouazzane｜guidance：管理層說明上述數字不含太空資料中心的潛在上行（原話："do not include any potential upside coming from data"）
- 2026-05-04｜Remi El-Ouazzane｜guidance：2026 年之後成長取決於星座部署節奏，火箭運載被列為首要關鍵路徑（原話："rocket launcher is at the top of the list"）
- 2026-05-04｜Remi El-Ouazzane｜guidance：ST 估計新增訂戶 2030 年前可超過 2 億，目前約 1,000 萬（原話："could exceed 200 million by 2030 from about 10 million"）
- 2026-05-04｜Remi El-Ouazzane｜margin：數字口徑：LEO 業務 2025 年營收約 6 億美元（2021 年約 1.75 億）（原話："reaching approximately $600 million in '25"）
- 2026-05-04｜Remi El-Ouazzane｜margin：數字口徑：ST 的 LEO RF 市占估計約 90%（2025）（原話："estimate our RF market share for LEO at about 90% in '25"）
- 2026-05-04｜Remi El-Ouazzane｜margin：數字口徑：每顆 Starlink 衛星的 ST 料件價值自 V1.5 到 V3 增為 8 倍，達數萬美元（原話："material was multiplied by 8x between the V1.5"）
- 2026-05-04｜Remi El-Ouazzane｜margin：數字口徑：每個用戶終端的 ST 內容約數十美元（原話："reached down to only several tens of USD per user terminal"）
- 2026-05-04｜Remi El-Ouazzane｜margin：數字口徑：用戶終端為最大營收貢獻者，管理層拒絕給細項（原話："we are not going to give any breakdown"）
- 2026-05-04｜Remi El-Ouazzane｜margin：數字口徑：軍用應用不含在約 10 億美元內，且金額微不足道（原話："its completely marginal"）
- 2026-05-04｜Remi El-Ouazzane｜commitment：管理層承諾將 ST 維持為新太空領域的領先半導體供應商（原話："we are and we intend to"）
- 2026-05-04｜Remi El-Ouazzane｜commitment：與 SpaceX 合作持續，聚焦量產中設計與下一代衛星與終端共同架構（原話："the collaboration continues with a focus on ramping up"）
- 2026-05-04｜Remi El-Ouazzane｜competition：管理層稱預測已納入主要客戶的市占流失（原話："some market share loss for our main customer"）
- 2026-05-04｜Remi El-Ouazzane｜competition：管理層不認為超過 90% 的市占可以維持（原話："is exceeding 90% is something that we can keep as is"）
- 2026-05-04｜Remi El-Ouazzane｜competition：預期到 2030 年市占仍偏高，但低於 90%（原話："pretty oversized market share, clearly, lower"）
- 2026-05-04｜Remi El-Ouazzane｜competition：市場以 35% CAGR 成長，新供應商會來搶份額，已計入預測（原話："try to gain share, which we have factored in our numbers"）
- 2026-05-04｜Remi El-Ouazzane｜competition：管理層承認 BiCMOS 前端模組市場會有競爭，但自認技術差異化強（原話："will have competition. But we feel quite strong as well"）
- 2026-05-04｜Remi El-Ouazzane｜competition：管理層描述潛在競爭者輪廓：IDM、做 BiCMOS、具大規模封裝並掌握 PLP（原話："has huge assembly capabilities and is able to master PLP"）
- 2026-05-04｜Remi El-Ouazzane｜competition：管理層解釋為何競爭者需為 IDM：後段封裝與前段同等重要（原話："the back-end, end up being as important as front-end"）
- 2026-05-04｜Remi El-Ouazzane｜product：每顆衛星的矽含量預期持續增加（原話："I do believe that silicon content will continue to increase"）
- 2026-05-04｜Remi El-Ouazzane｜product：Ku 頻段用戶終端的含量預期接近高原（原話："we're going to soon reach a plateau"）
- 2026-05-04｜Remi El-Ouazzane｜product：用戶終端經濟面為軟著陸，Ka 頻段被視為助力（原話："we are going to a soft landing in terms of the economics"）
- 2026-05-04｜Remi El-Ouazzane｜product：用戶終端產品世代週期約一年多一個月（原話："are for user terminal a year and roughly a month"）
- 2026-05-04｜Remi El-Ouazzane｜customer：ST 已在另一家主要業者通過驗證（原話："we have already been qualified at another"）
- 2026-05-04｜Remi El-Ouazzane｜customer：未來五年客戶數預期不超過 10 家（原話："I don't see more than 10 players"）
- 2026-05-04｜Remi El-Ouazzane｜customer：中國方面：因出口管制無法參與衛星端，只聚焦用戶終端（原話："we cannot be in any satellite technology happening in China"）
- 2026-05-04｜Remi El-Ouazzane｜customer：中國用戶終端目前未揭露具體進展（原話："we have not yet disclosed anything specifically happening"）

### 問答異常語氣（迴避／改口／保留）
- STM_Q2_2026_Earnings_Call_20260723.md｜問：Menon 追問 Q4 毛利率方向與 2027 走勢｜答法：只確認 Q4 環比改善並列舉逆風，未給幅度，也未回答 2027
- STM_Q2_2026_Earnings_Call_20260723.md｜問：Menon 追問營收跳升是否代表毛利率跳升也更大｜答法：重申會改善但強調閒置費用與匯率逆風，未給量化
- STM_Q2_2026_Earnings_Call_20260723.md｜問：Ghilotti 詢問 40 億營收是否仍對應 40% 毛利率｜答法：改口補上第二條件（製造重整完成、2027 年底），Q4 達 40 億不足以到 40%
- STM_Q2_2026_Earnings_Call_20260723.md｜問：Didier 詢問 45%/180 億與 50%/200 億模型是否仍成立｜答法：確認 180 億，200 億明確擱置，毛利率目標附加條件（重整準時、匯率）
- STM_Q2_2026_Earnings_Call_20260723.md｜問：Buchalter 詢問 2027 資料中心是否因產能受限而高於 20 億｜答法：未直接回答是否高於 20 億，轉談成長驅動與矽光子產能無瓶頸
- STM_Q2_2026_Earnings_Call_20260723.md｜問：Bluestone 詢問漲價順風與何時影響營收｜答法：只說投入成本與漲價大致互抵，未給時間與金額
- STM_Shareholder_Analyst_Call_STMicroelectronics_N_V_20260309.md｜問：Joshua Buchalter (TD Cowen)：請拆分 5 億/10 億美元中矽光子與電源及各電壓級的組成｜答法：回答「Not really」，僅描述各產品量產狀態，明言不拆分
- STM_Shareholder_Analyst_Call_STMicroelectronics_N_V_20260309.md｜問：Sandeep Deshpande (JPMorgan)：2.3 億美元 SAM 中 ST 目前已佔多少份額｜答法：先答「We have not documented that」，被追問後改談產品供應涵蓋度而非份額
- STM_Shareholder_Analyst_Call_STMicroelectronics_N_V_20260309.md｜問：Adithya Metuku (HSBC)：EIC 市佔率具體多少｜答法：不給數字，回「I still have the same definition, I just gave you」
- STM_Shareholder_Analyst_Call_STMicroelectronics_N_V_20260309.md｜問：Gianmarco Bonacina (Banca Akros)：2027 與 2030 的總 SAM 金額（十億美元）｜答法：明言刻意不給，請分析師自行依 GW 部署建模
- STM_Shareholder_Analyst_Call_STMicroelectronics_N_V_20260309.md｜問：Stephane Houri (ODDO BHF)：成長所需 CapEx 增量及各市場規模與份額（對照 Infineon）｜答法：不給絕對 CapEx 金額與分市場規模/份額，僅重申 20～22 億美元區間重新配置
- STM_Shareholder_Analyst_Call_STMicroelectronics_N_V_20260309.md｜問：Adithya Metuku (HSBC)：納入 scale-up 後 SAM 是否為 4.6 億美元｜答法：表示無法回答，因未給 2.3 億美元的拆分，僅說 NPO 將疊加其上
- STM_Shareholder_Analyst_Call_STMicroelectronics_N_V_20260504.md｜問：Buchalter 追問市占下滑中有多少來自 SpaceX 自身占比下降、多少來自雙供應商｜答法：明說不直接回答，改談總 SAM 以 SpaceX 為大宗、ST 數字取決於在 SpaceX 的市占
- STM_Shareholder_Analyst_Call_STMicroelectronics_N_V_20260504.md｜問：Scemama 要求 2025 與 2028 用戶終端／閘道／衛星的營收拆分｜答法：拒絕給精確數字，只給排序（終端最大、衛星次之、閘道最小）
- STM_Shareholder_Analyst_Call_STMicroelectronics_N_V_20260504.md｜問：Houri 與 Bonacina 追問 2026–2028 營收軌跡及 2028／2030 市占水準｜答法：只重述「遠高於 30 億」與市占「低於 90% 但仍偏高」，未給逐年數字或市占百分比

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 4 | 2 |
| customer_second_source | found | 3 | 1 |
| customer_concentration_credit | found | 3 | 1 |
| supply_demand_durability | found | 5 | 4 |
| regulatory_antitrust | found | 3 | 1 |
| reg_tariff_export | found | 4 | 1 |
| geo_supply_chain | found | 3 | 3 |
| end_markets | found | 3 | 3 |
| substitute_technology | found | 1 | 1 |
| channel_business_model_shift | found | 3 | 2 |
| capital_markets_pricing | found | 4 | 3 |
| major_events | found | 3 | 4 |
| cyclical_supply_discipline_capacity | found | 4 | 3 |
| cyclical_inventory_price_position | found | 4 | 3 |
| cyclical_prior_downcycle_behavior | found | 4 | 3 |

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260724","verdict":"觀望","role":"追蹤","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"車用/工業補庫存升循環為結構性、非脈衝，STM 營收與利用率持續爬升","columns":{"2Y 驗證點":"2026-27 book-to-bill 守 >1、GM 序列改善","5Y 驗證點":"2028 營收向 $18B 模型靠攏","具體數字門檻":"Q3 GM ~37%→2027 持續升；2026 全年營收 ~$14.3B（共識）","來源":"Q2 法說 guidance、Bernstein 升循環判定","漂移觸發":"連 2 季 TTM 營收偏離 ≥5% 或 book-to-bill"}},{"id":"H2","text":"毛利率恢復到「40% @ $4B／45% @ $18B」模型（依賴製造重整 2027 末完成）","columns":{"2Y 驗證點":"Q4 2026 GM 淨向 40% 軌道","5Y 驗證點":"2028 GM ~45%","具體數字門檻":"Q3 37%±200bps → Q4 序列改善 → 2027 末重整完成","來源":"Q2 法說 Grandi/Chery 明確「須完成重整、2027 末、不早於」","漂移觸發":"連 4 季 TTM GM 偏離模型 ≥5% → 削弱（此為多頭核心賭注）"}},{"id":"H3","text":"估值修復＝谷底 EPS 恢復（FY26 $1.32→FY27 $2.68→FY28 $3.85）兌現、倍數不再進一步壓縮","columns":{"2Y 驗證點":"共識 EPS 不再下修、股價守住循環中段倍數","5Y 驗證點":"2028 EPS ~$3.85 × ~18x = ~$69","具體數字門檻":"FY27 Fwd PE 20x（$2.68）、FY28 13.9x（$3.85）","來源":"Excel snapshot 2026-07-16 normalized consensus（USD）","漂移觸發":"共識 FY27/28 EPS 連 2 季下修 ≥10% → 反轉"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"毛利率恢復停滯：製造重整延後 / 新產能折舊超前量能 / 傳統類比 legacy 產能爬坡卡關（法說已承認 Q2 legacy 類比 ramp 延遲）","columns":{"對應假設":"H2","時間尺度":"🔥 中期（4-6 季）","監測指標":"季度 GM vs 40% 模型軌道；unused capacity charges 走勢","警戒閾值":"連 4 季 GM 停在 37% 以下且無序列改善"}},{"id":"R2","text":"需求空窗：補庫存脈衝退潮後現需求不接棒（S&P 車銷 −2%、PE 記憶體漲價擠壓低階手機）","columns":{"對應假設":"H1","時間尺度":"⚡ 短期（1-2 季）","監測指標":"book-to-bill、分銷 POS、DSI 是否止跌回升","警戒閾值":"book-to-bill"}},{"id":"R3","text":"車用 MCU 份額結構性讓 Infineon AURIX：SDV 高內容段被生態綁定通吃","columns":{"對應假設":"H1/H3","時間尺度":"🐢 長期（2+ 年）","監測指標":"SDV MCU design-win、AURIX vs STM32 車規內容比","警戒閾值":"連續財季車用 MCU 內容/份額流失，≥50% 機率結構化"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"事件錨：Q4 GM 淨向 40% 模型軌道確認＋製造重整如期＋分銷去化未反轉；或估值回踩至 EV/EBITDA 正常化（約 $42-45）","irr_base_pct":7.0,"ev5y_pct":36.0,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"追蹤","signal":"B","val":"🟠","ma":"🟡","trap":"🟡","moat_trend":"→","runway_post_y5":"🟢","asym_ratio":2.6,"ev5y_pct":36.0,"irr_base_pct":7.0,"max_dd_pct":-55.0,"bull_5y_price":110.0,"bear_5y_price":31.0,"p_bull_pct":30.0,"p_bear_pct":30.0,"rearm_trigger":"事件錨：Q4 GM 淨向 40% 模型軌道確認＋製造重整如期＋分銷去化未反轉；或估值回踩至 EV/EBITDA 正常化（約 $42-45）","price_at_dd":53.49,"archetype":"循環/商品","cycle_position":"早循環"}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"STM","date":"2026-11-02","schema":"v15.0","contract":"v19","company_name":"STMicroelectronics N.V."},"oneliner":"循環早段加上資料中心與 LEO 第二曲線，Q3 基本面變好；但毛利率仍在同業墊底，2028 共識已含重整完整效益，Base 年化約 7%，等 41 美元以下或 1 月法說確認再分批進場","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/STM_20261102/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/STM_20261102/scenario.json","answers":{"q1_business":{"verdict":"賺車用與工業客戶（近六成營收），以及 Apple、SpaceX、雲端業者的錢；錢卡在製造端：Q3 毛利率 37.3%，比 NXP、TI、ADI 低 20 個百分點以上，獲利修復要靠關舊廠與產品組合，不是靠訂價","reasoning":"營收結構：Q3 營收 37.6 億美元，年增 17.9%。分部為類比/MEMS/感測 15.6 億（+8.8%，營益率 14.1%）、嵌入式處理 12.1 億（+24.1%，營益率 23.1%）、射頻與光通訊 5.0 億（+46.2%，營益率 26.2%）、功率與分離式 4.8 億（+11.3%，營益率 −17.1%）。依 Q4 指引中點，車用約占 35%、工業 22–24%、通訊設備與電腦周邊略高於 20%、個人電子約 22%。獲利：GAAP 毛利率 37.3%，非 GAAP 營益率 11.4%；Q4 指引毛利率約 39%，2026 全年營收約 145 億美元（+22.8%）。產業時鐘判 I（復甦）：營收仍比 2023 年高峰低約 16%，毛利率仍接近自身谷底區，分銷庫存低於標準目標；但 book-to-bill 遠高於 2，公司已開始選擇性漲價，正往 II 移動。供需持久性判週期性將反轉：類比/MCU 的吃緊來自補庫存與交期拉長，供給可逆性高；記憶體以外的晶片價格已大致正常化，2026–27 年的產業成長多來自價格。只有資料中心矽光子與 LEO 有長期產能預留支撐，比較持久。單點依賴：最大客戶 Apple 占 2025 年營收 17.7%，連三年上升（2023 年為 12.3%）；LEO 營收集中在單一主客戶。這兩點是集中度風險，不是護城河證據。","fact_refs":["f_kpi0_net_revenues_gaap","f_kpi1_non_gaap_operating_incom","f_kpi2_gaap_operating_income_ma","f_kpi3_free_cash_flow_non_gaap","f_kpi4_gross_margin_gaap","f_kpi5_inventory_days_dsi","f_kpi6_guidance_q4_2026_revenue","f_kpi7_guidance_q4_2026_gross_m","f_kpi8_guidance_fy2026_revenue"],"verdict_values":{"revenue_quality":"成長主力是工業（Q3 年增 40%）與通訊設備/電腦周邊（+64%，來自 AI 資料中心與 LEO），車用只 +5%，個人電子 −4%。分銷約占營收 28–29%，OEM 約 72%。Q3 FCF 3.51 億美元（營運現金流 10.2 億，淨資本支出 6.43 億）","unit_econ_note":"Q3 毛利率 37.3%，含閒置產能約 60 基點與重整一次性成本約 40 基點；Q4 指引 39%，含閒置 40 基點與一次性成本 30 基點。各分部營益率差距大：射頻與光通訊 26.2%、嵌入式 23.1%、類比/MEMS 14.1%、功率與分離式 −17.1%，組合往前兩者移動就會拉高毛利率","archetype":{"primary":"循環/商品","secondary":"轉機/特殊情境","confidence":"中","fingerprint":"營收與獲利隨車用/工業庫存循環大幅擺動：2023→2025 年營收 −32%，稀釋 EPS 由 4.46 美元降到 0.18 美元，毛利率掉 14 個百分點；另有關閉 4 座舊廠的製造重整，屬循環谷底加上重整"},"industry":{"clock_phase":"I","sd_verdict_source":"週期性將反轉。依據：記憶體以外晶片價格已大致正常化（TechInsights 等彙整）；工業半導體正從極低庫存回補（BNP Paribas，2026-06）；管理層自述需求超過供給、交期拉長。有長約支撐的只有矽光子產能預留（2026-03-09 投資人日）","bargaining":{"up":"上游：部分材料只來自單一地區的少數供應商（20-F）；投入成本上漲與漲價大致互抵（2026-07-23 Grandi）。對上游議價偏弱","down":"下游：Apple 占營收 17.7%，LEO 主客戶、超大規模雲端業者與歐洲 Tier 1 都採年度議價。車用合約價格由大客戶主導，經銷通路與 STM32 比較容易漲價（2026-07 法說）","geo":"地緣：在中國以三安合資與華虹代工做在地化；美國有 232 條款調查與 100% 晶片關稅威脅；因出口管制，無法參與中國衛星端"},"profit_pool_dir":"舊利潤池（車用/工業類比、SiC）受到中國本土化與產業整併擠壓；新利潤池（AI 光互連、LEO 射頻）流向少數具備 300mm 矽光子與 BiCMOS 量產能力的業者，ST 目前在其中。產業利潤池分布的量化數字，事實表未涵蓋","tam_table":[{"item":"資料中心營收（ST）","value":"2026 年約 13 億美元（2026-10-29 法說）；管理層稱 2027 年將遠高於翻倍。3 月投資人日的 SAM 口徑為每 GW 約 2.3 億美元，只算可插拔光學，不含 NPO"},{"item":"低軌衛星（LEO）","value":"ST 的 LEO 營收 2025 年約 6 億美元，2026 年接近 10 億美元；LEO 寬頻電子 SAM 在 2028 年約 20 億美元。ST 2025 年 RF 市占約 90%，管理層預期會降到 90% 以下（2026-05-04 投資人日）"},{"item":"營收結構（Q4 2026 指引中點）","value":"車用約 35%、工業 22–24%、通訊設備與電腦周邊略高於 20%、個人電子約 22%"},{"item":"全球半導體市場","value":"WSTS 春季預測 2026 年約 1.51 兆美元、2027 年約 2.1 兆美元。成長由記憶體帶動，與 ST 的類比/MCU 市場不同步"},{"item":"營業利益池占比（5 年前→現在）","value":"產業利潤池分布事實表未涵蓋。只知 ST 營益率由 2022 年 26.5% 降到 TTM 6.6%，同業 TTM 為 18–41%"}]}}},"q2_moat":{"verdict":"→ 穩定：執行面在資料中心、LEO 與設計案上擴大，但訂價面仍明顯落後同業，大客戶也在垂直整合，兩者抵銷；評等 C","reasoning":"機制：產品組合廣的 IDM，加上車用/工業設計案的多年認證轉換成本與 STM32 生態，新加入 300mm 矽光子與 BiCMOS 射頻的製程領先。可證方向：對同業的利潤差距仍大。TTM 毛利率 33.8%，NXP 56.4%、TI 60.2%、ADI 65.8%、onsemi 37.7%；FCF 率 3.8%，同業為 24–36%，與最強同業的報酬差是深負值。ST 自身毛利率由 2023 年 47.9% 降到 TTM 33.8%，其中一部分來自舊廠效率差（20-F 自述 2025 年降幅主因是製造效率），不完全是訂價力流失。執行面給 6 分：近期財測都兌現，7 月說 Q3 毛利率約 37%，實際 37.3%；7 月說 Q4 營收逾 40 億，實際指引 41.5 億。資料中心 2026 年營收預期由 3 月的逾 5 億、7 月的逾 10 億，上修到約 13 億；客戶稱矽光子良率是業界新標準。訂價面給 5 分：只對部分產品漲價，2027 年預期持平到小漲，且被投入成本上漲抵銷；最大客戶 Apple 傳出減單與自研 RF，LEO 主客戶市占管理層也自承會從 90% 以上下降，所以不能判擴大。當期 ROIC 屬低利益率×低周轉（TTM 營益率 6.6%，投入資本事實表未涵蓋）。四檢查點：需求 🟢、決策層級 🟡、價值鏈分配 🔴、社會容忍度 🟡。再投資：2022–2025 年累計淨再投資約 71 億美元（淨利 98.9 億減 FCF 27.5 億），但共識 2028 年淨利約 34 億美元，仍低於 2023 年的 42 億，峰對峰增量報酬接近零或為負。","fact_refs":["f_peer_stm_gross_margin_pct","f_peer_stm_operating_margin_pct","f_peer_stm_fcf_margin_pct","f_peer_nxpi_gross_margin_pct","f_peer_nxpi_operating_margin_pct","f_peer_nxpi_fcf_margin_pct","f_peer_txn_gross_margin_pct","f_peer_txn_operating_margin_pct","f_peer_txn_fcf_margin_pct","f_peer_on_gross_margin_pct","f_peer_on_operating_margin_pct","f_peer_on_fcf_margin_pct","f_peer_adi_gross_margin_pct","f_peer_adi_operating_margin_pct","f_peer_adi_fcf_margin_pct"],"verdict_values":{"moat":{"mechanism":"寬產品組合 IDM，加上車用/工業設計案的多年認證轉換成本與 STM32 軟體生態；新加入 300mm 矽光子與 BiCMOS 射頻的製程與良率領先","execution":6,"pricing":5,"grade":"C","trend":"→","trend_evidence":"執行面擴大：資料中心 2026 年營收預期由 3 月的逾 5 億、7 月的逾 10 億上修到約 13 億美元；book-to-bill 在所有終端市場都高於 1；近期財測都兌現。訂價面縮減：TTM 毛利率 33.8%，同業為 37.7–65.8%；漲價只限部分產品，且被投入成本抵銷；最大客戶 Apple 減單並自研 RF。兩者抵銷，判穩定，不判擴大","competitor_notes":[{"name":"NXPI","strategy_note":"車用 MCU/處理器的主要對手，TTM 毛利率 56.4%、營益率 28.6%，毛利率比 ST 高約 22 個百分點；它把 MEMS 感測器業務賣給 ST，顯示正在收斂到高毛利產品"},{"name":"TXN","strategy_note":"自有 300mm 類比產能加直銷，營益率 41.1%、FCF 率 35.2%，是 ST 轉 300mm 想追的成本結構；但 ST 重整完成後的 44–46% 毛利率模型，仍遠低於 TI 的 60.2%"},{"name":"ON","strategy_note":"SiC 與功率的最直接對手，毛利率 37.7% 與 ST 相近，但 FCF 率 24.2%（ST 為 3.8%），資本支出紀律較好；ST 的功率與分離式分部仍在虧損"},{"name":"ADI","strategy_note":"高階類比與混合訊號，毛利率 65.8%，與 ST 類比分部（營益率 14.1%）不在同一價格帶，不作直接對標"}],"threats":[{"level":"🔴","text":"中國本土化：比亞迪、蔚來、吉利、小米擴大 SiC 布局，本土業者競爭升溫。ST 以三安 SiC 合資與華虹車用 MCU 代工因應，等於拿利潤分給夥伴來換份額","p":"40%","evidence_refs":["competitive_share_entrants#3","competitive_share_entrants#0"]},{"level":"🟡","text":"最大客戶垂直整合：Apple 占 2025 年營收 17.7%（2023 年 12.3%），傳出自研無線/RF 晶片；20-F 也承認部分客戶自己做 IC 與晶圓廠","p":"35%","evidence_refs":["customer_second_source#0","customer_second_source#1","customer_second_source#2","customer_concentration_credit#0"]},{"level":"🟡","text":"LEO 新供應商進場：管理層自承主客戶市占不會維持在 90% 以上，到 2030 年仍偏高但會下降（2026-05-04 投資人日）","p":"60%","evidence_refs":[]},{"level":"🟡","text":"產業整併、小型利基業者與亞洲代工擴張，20-F 自述可能侵蝕市占並迫使重組營運","p":"30%","evidence_refs":["competitive_share_entrants#1"]},{"level":"🟡","text":"技術變動快、產品週期短、價格侵蝕大（20-F 一般性風險語言，未點名替代技術）；銅轉光反而是 ST 的順風","p":"30%","evidence_refs":["substitute_technology#0"]}],"roic_durability":{"quadrant":"低利益率×低周轉","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者（車廠、工業設備商、雲端業者）、決策者（Tier 1 與系統設計者）、付款者三個角色都成立；車用與工業晶片是需要而非想要，延後採購的代價是產線停擺。代理變數：Q3 book-to-bill 遠高於 2，工業與通訊設備高於 3，分銷庫存仍低於標準目標（2026-10-29 法說）。但這是補庫存期的讀數，持久性要看 2027 年的終端銷售"},{"item":"決策層級","level":"🟡","text":"替代性在設計案層級衡量：車用與工業設計一旦採用，重新認證要好幾年，轉換成本高，STM32 也有軟體生態。反面是資料中心客戶以最佳組合分開買 MCU、EIC、PIC，不必綁同一家（2026-03-09 El-Ouazzane）；舊廠轉移同樣需要客戶重新認證，4 座中仍有 1 座在談"},{"item":"價值鏈分配","level":"🔴","text":"價值往兩端被拿走。上游部分材料只來自少數地區的少數供應商，投入成本上漲與漲價大致互抵（2026-07-23 Grandi）；下游 Apple 占 17.7%，LEO 主客戶與超大規模業者議價力強，Apple 還在自研 RF。ST 毛利率 33.8%，同業為 37.7–65.8%，顯示 ST 在價值鏈中拿到的份額偏低"},{"item":"社會容忍度","level":"🟡","text":"晶片被各國當成戰略物資：美國有 232 條款調查與 100% 關稅威脅，中國有出口管制，ST 也因出口管制無法參與中國衛星端（2026-05-04）。價格天花板主要來自大客戶年度議價，不是社會壓力；政策風險在關稅與出口許可"}],"roiic":"峰對峰為負。2022–2025 年累計淨再投資約 71 億美元，但共識 2028 年淨利約 34 億美元（3.79 美元×8.94 億股），仍低於 2023 年的 42 億。從谷底到 2028 年的增量報酬看起來很高，但那是產能利用率回升，不是新投資帶來的報酬","reinvest_rate":72,"endo_ceiling":3,"formula_note":"再投資率＝（淨利−FCF）÷淨利，以 2022–2025 年累計淨利 98.9 億、FCF 27.5 億計，約 72%；以淨利代替 NOPAT（折舊、營運資金與投入資本事實表未涵蓋）。峰對峰增量報酬約為 0 或負，內生成長上界取 0–5% 的中間，約每年 3%。這只是循環正常化的口徑，不是谷底反彈率"}}}},"q3_growth":{"verdict":"🟢 寬：資料中心矽光子（2027 年產能擴 4 倍以上，有長期產能預留）與 LEO（訂戶 2030 年前可由約 1,000 萬增至 2 億）是有訂單支撐的第二曲線；但 2026→2028 年的 EPS 跳升主要來自毛利率回升，不是再投資複利","reasoning":"成長組成以量為主（補庫存，加上 AI 資料中心與 LEO 出貨）。價格自 2026 下半年起對部分產品調漲，2027 年預期持平到小漲。NXP MEMS 併購（2024 年營收約 3 億美元）約貢獻 2 個百分點，回購可忽略。共識三年 EPS：FY2025 實際 0.18 美元是谷底，到 FY2028 的 3.79 美元等於年化約 176%，沒有參考意義。改看 FY2026→FY2028，由 1.34 美元到 3.79 美元，年化約 68%；營收共識 FY2026→FY2027 約 +20%。內生上界引護城河段的每年約 3%，缺口約 65 個百分點，歸因於毛利率擴張（產能利用率回升、重整 400 基點、產品組合），不是淨回購或收購，所以這段成長取決於重整能否準時完成。跑道：滲透率事實表未涵蓋，以管理層 2028 年 180 億美元營收目標推算，2026→2028 年營收年增約 11%。第二曲線有來源支撐：資料中心 2026 年約 13 億美元，2027 年遠高於翻倍；LEO 2026–2028 年累計逾 30 億美元，因此判寬。衰退訊號亮 2 個（EPS 成長遠高於營收、FCF/淨利連兩年為負），長期成長性 🟡。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_kpi8_guidance_fy2026_revenue","f_consensus_rev_fy2_pct","f_consensus_rev_fy3_pct"],"verdict_values":{"growth":{"driver_mix":"量為主（補庫存，加上資料中心與 LEO 出貨）；價格自 2026 下半年起選擇性調漲，2027 年持平到小漲；併購約貢獻 2 個百分點（NXP MEMS）；回購可忽略","runway_years":"滲透率事實表未涵蓋；以 2028 年 180 億美元營收目標推算，2026→2028 年營收年增約 11%","runway_post_y5":"🟢","endo_ceiling_basis":"引護城河段：峰對峰增量報酬接近零（2022–2025 年累計淨再投資約 71 億美元，共識 2028 年淨利仍低於 2023 年），內生上界約每年 3%。2026→2028 年共識 EPS 年增約 68%，幾乎全部來自毛利率回升與產能利用率修復，屬於循環與重整，不是再投資複利，因此取決於重整能否兌現","segments":[{"item":"類比、MEMS 與感測","value":"Q3 營收 15.60 億美元，年增 8.8%；營益率 14.1%，營收成長下營益率仍年減（舊廠轉移成本）"},{"item":"功率與分離式（含 SiC）","value":"Q3 營收 4.77 億美元，年增 11.3%；營益率 −17.1%（Q2 為 −21.4%）。管理層稱 2026 年 SiC 成長約 20%"},{"item":"嵌入式處理（STM32 等）","value":"Q3 營收 12.12 億美元，年增 24.1%；營益率 23.1%"},{"item":"射頻與光通訊","value":"Q3 營收 5.04 億美元，年增 46.2%；營益率 26.2%。資料中心與 LEO 的營收主要在這裡"},{"item":"終端市場（Q3 年增）","value":"通訊設備與電腦周邊 +64%、工業 +40%、車用 +5%、個人電子 −4%"}],"decay_signals":[{"item":"毛利率連 2 季年減","lit":false,"note":"Q3 毛利率年增 410 基點"},{"item":"核心市占近 12 個月縮減","lit":false,"note":"市占數字事實表未涵蓋；LEO 份額下降是管理層預期，尚未發生"},{"item":"主力產品提價後銷量下滑","lit":false,"note":"選擇性漲價期間 book-to-bill 仍遠高於 2"},{"item":"EPS 成長顯著高於營收成長（差距超過 5 個百分點）","lit":true,"note":"共識 FY2026→2028 年 EPS 年增約 68%，營收約 +11～20%，屬谷底營運槓桿"},{"item":"FCF/淨利連 2 年低於 0.75","lit":true,"note":"2024、2025 年 FCF 都為負"},{"item":"SBC/營收超過 5% 且逐年上升","lit":false,"note":"SBC 事實表未涵蓋"},{"item":"TAM 萎縮或被替代技術壓縮","lit":false,"note":"銅轉光對 ST 是順風"},{"item":"產業估值倍數近 3 年系統性下移","lit":false,"note":"同業倍數歷史事實表未涵蓋"},{"item":"維持性資本支出占 FCF 超過 60%","lit":false,"note":"維持性資本支出事實表未涵蓋"},{"item":"停止投資新產能且營收 3 年內下滑","lit":false,"note":"矽光子產能擴 4 倍以上，Crolles 正在擴產"}],"trap_rating":"🟡（亮 2 個：EPS 成長遠高於營收、FCF/淨利連兩年為負）"}}},"q4_capital":{"verdict":"現金撐得住擴產，但股東回報薄：淨現金約 21 億美元，Q3 FCF 才轉正到 3.5 億，回購的盈餘殖利率過不了門檻，SBC 與完整稀釋事實表未涵蓋","reasoning":"FCF 轉換：Q3 FCF 3.51 億美元，約為 GAAP 淨利 2.91 億的 1.2 倍；但 2024、2025 年 FCF 都為負（−2.16 億、−0.52 億），TTM FCF 率 3.8%。Q3 現金去向：淨資本支出 6.43 億、股利 0.83 億、回購 0.91 億；2026 全年淨資本支出約 22 億美元（區間高端）。資產負債：流動性 53.1 億、金融負債 32.1 億，淨現金約 21 億。7 月新發 15 億美元雙檔可轉債；2027 年到期的 7.5 億可轉債提前贖回，以現金 7.5 億加約 420 萬股庫藏股交割。三年現金去向四分與 SBC 金額，事實表未涵蓋。計分：併購報酬還無法驗證（NXP MEMS 2026-02 才交割）；以判斷日股價對 FY1 共識 EPS 計，回購的盈餘殖利率約 2.9%，過不了 10 年期殖利率加 2 個百分點；SBC 淨稀釋率沒有資料。","fact_refs":["f_kpi3_free_cash_flow_non_gaap","f_net_debt_m","f_shares_diluted_m","f_dividend_yield_ttm","f_ev_m","f_peer_stm_fcf_margin_pct"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":true,"passed":null,"input":"NXP MEMS 收購最高 9.5 億美元（交割 9 億，加 5,000 萬里程碑款），2026-02 交割，2024 年營收約 3 億美元；Q3 只揭露收購價分攤 700 萬美元，已實現報酬事實表未涵蓋，目前無法判斷"},{"name":"buyback_yield","applicable":true,"passed":false,"input":"Q3 回購 9,100 萬美元；以判斷日股價對 FY1 共識 EPS 計，盈餘殖利率約 2.9%。只要 10 年期殖利率高於 0.9% 就過不了門檻（10 年期殖利率事實表未涵蓋）"},{"name":"sbc_dilution","applicable":true,"passed":null,"input":"SBC 金額事實表未涵蓋；可轉債轉換交付約 420 萬股庫藏股（約股本 0.5%），7 月新發 15 億美元可轉債另有潛在稀釋"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購支撐：NXP MEMS 收購最高 9.5 億美元，約為判斷日市值的 2.3%。股東回報以每季股利約 8,300 萬美元與回購約 9,100 萬美元為主，金額小，不是承重項"}}}},"q5_valuation":{"verdict":"現價 46.74 美元要求 2028 年 EPS 接近共識的 3.79 美元，市場再給 12–15 倍；我只相信到約 3.4 美元，Base 情境 5 年年化約 7%，價格合理但不夠便宜","reasoning":"現價對 FY2026 共識是 34.9 倍，對 FY2027 是 17.3 倍，對 FY2028 是 12.3 倍；trailing 82 倍落在谷底盈餘上。EV/S 2.9 倍、P/S 3.06 倍都在自身 4 個年度端點的最高（谷底營收會拉高這兩個倍數，參考性有限），五年分位事實表未涵蓋。在循環股的看法下，EV 倍數貼近自身高點就不新建部位，要等回踩。分母是爭點：FY2028 共識已含重整 400 基點以上的完整效益，若效益延到 2028 下半年，EPS 約少 10–18%。各聚合站的賣方目標價落在 26–98 美元，高低差超過 3 倍，因此調低對自己情境的信心。Base 情境（2031 年 EPS 4.2 美元×15 倍）終值約 63 美元，加上股息與回購，年化約 7%；要年化 10%，進場價約 41 美元。動能：26 週 −15.9%，RSI 43.9，不過熱；週線均線 🟡，股價高於 W52 的 44.9，W250 斜率約為 0。FY1 共識近 3 個月 −1.5%，FY2、FY3 在本次快照小幅上修。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_pe_current","f_pe_percentile","f_ps_current","f_ps_percentile","f_ev_s_current","f_ev_s_percentile","f_ev_s_fwd","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_3m_fy1_pct","f_week26_return_pct","f_rsi14","f_ma_state","f_ma_w52","f_ma_slope_w250_pct"],"verdict_values":{"valuation":{"basis":"前瞻本益比：起點用 FY1（當年度）EPS，終端用 FY2031 當年度 EPS，兩者同口徑","peers":{"expanded":false,"reason":"事實表的同業對照只有毛利率、營益率、FCF 率與研發密度，沒有同業本益比或 EV/S，無法做倍數對照；終端倍數只能以 STM 自身的前瞻倍數當參照"},"fwd_pe":34.88,"peg":0.51,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"現價對 FY2027 共識 17.3 倍、FY2028 共識 12.3 倍，表面不貴；但 FY1 的 34.9 倍與 trailing 82 倍都落在谷底盈餘上，EV/S 與 P/S 在自身 4 個年度端點的最高，FY2028 共識又已含重整的完整效益。Base 情境年化約 7%，低於 10% 門檻，所以落在合理與偏貴之間，判 🟡。比前份的偏貴結論改善，原因是股價下跌 12.6%，而共識大致持平。五年分位事實表未涵蓋（只有 4 個年度端點）","upside_short_pct":3.7,"upside_mid_pct":34.8,"denominator_disputed":true,"denominator_note":"trailing 82 倍與 FY1 34.9 倍都以谷底盈餘當分母；FY2028 共識 3.79 美元又含製造重整 400 基點以上的毛利率跳升，分母本身就是爭點。PEG 0.51（FY1 本益比 34.9 倍除以 FY2026→2028 年 EPS 年增約 68%）來自循環反彈，不能當成便宜的證據。短期上行＝FY2027 Base EPS 2.55 美元×19 倍，約 48.5 美元；中期上行＝5 年 Base 終值約 63 美元"}}},"q6_how_wrong":{"verdict":"最可能看錯在兩件事疊加：book-to-bill 遠高於 2 其實是交期拉長下的重複下單，以及重整的 400 基點延到 2028 下半年以後；價值陷阱風險 🟡，路徑回撤 −40%～−60%","reasoning":"三個視角的反證見反證紀錄：論點失敗（需求反轉加上重整延誤）、股東經濟變差（擴產吃掉 FCF、大客戶拿走議價空間）、價格已反映（2028 共識已含完整重整效益）。最強的三個反駁：①book-to-bill 遠高於 2，正是上一輪高點前會出現的讀數；②共識 2028 年淨利仍低於 2023 年，代表過去約 71 億美元的再投資，峰對峰沒有賺到錢；③毛利率在同業墊底，重整只是追到中期模型，仍然低於 NXP 與 TI。路徑回撤：半導體族群上一輪約跌 46%，ST 自身盈餘在 2023→2025 年幾乎歸零，範圍取 −40%～−60%。論點本身不算脆弱（護城河趨勢穩定、跑道寬、Base 報酬不靠倍數擴張），所以深回撤時不因波動砍倉，但進場前要先做好深回撤的心理準備，單檔上限 3%。訴訟：證券集體訴訟續審與 Purdue 案 3,200 萬美元判決已列入風險與觸發器；金額相對 21 億美元淨現金可以承受，影響主要在管理層可信度。","fact_refs":["f_week26_return_pct","f_ma_w250","f_ma_w104","f_net_debt_m","f_kpi4_gross_margin_gaap","f_kpi7_guidance_q4_2026_gross_m"],"verdict_values":{"trap":{"verdict":"🟡","label":"循環谷底反彈，不是價值陷阱；但 FCF 與資本報酬還沒證明"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":1.34,"pe":34.88,"basis":"FY1（FY2026E，當年度）共識 EPS 1.34 美元，對判斷日股價 46.74 美元；終端倍數同樣套在終端年當年度的 EPS（FY2031E），分母同口徑"},"eps":{"bull":[2.95,4.3,4.8,5.4,6.0],"base":[2.55,3.4,3.3,3.8,4.2],"bear":[2.2,2.4,1.6,2.0,2.4]},"pe":{"bull":19,"base":15,"bear":12},"p":{"bull":30,"base":40,"bear":30},"yield_pct":{"dividend":0.77,"net_buyback":0.4},"second_stage":{"bull_cagr_pct":8,"base_cagr_pct":5},"max_dd":{"lo":-60,"hi":-40,"basis":"上一輪半導體族群（SOXX）在 2021-12 至 2022-10 約跌 46%；ST 自身 2023→2025 年 EPS 由 4.46 美元降到 0.18 美元，毛利率掉 14 個百分點，個股振幅大於族群。現價比 W250（37.73）高約 24%，跌回 W104（35.15）就是約 −25%。若 2028 年需求反轉疊加重整延誤，在到達 Bear 終值 28.8 美元（−38%）之前，路徑上的低點可能更深，因此範圍取 −40%～−60%；21 億美元淨現金讓下緣不太可能深過 −70%","trigger_time":null},"basis":{"bull":"資料中心 2027 年營收逾 30 億美元並持續成長，LEO 產能放量，重整如期，產品組合讓毛利率超過 46%；2031 年 EPS 6.0 美元，給 19 倍。同業現值倍數事實表未涵蓋，只能對照 STM 自身 FY2027 隱含的 17.3 倍","base":"2027–2028 年跟著共識但打折（重整效益部分延到 2028 下半年，加上投入成本上漲），2029 年循環小幅修正後恢復，2031 年 EPS 4.2 美元。15 倍介於自身 FY2027 隱含的 17.3 倍與 FY2028 隱含的 12.3 倍之間，代表循環中後段的當年度盈餘倍數","bear":"需求其實是重複下單，2028 年訂單反轉；重整延誤使毛利率卡在 38–40%，Apple 與 LEO 份額也流失。2029 年 EPS 回到 1.6 美元，2031 年 2.4 美元；12 倍是成長熄火到約 10% 時的倍數。機率 30% 的依據：共識成長超過內生上界，賣方目標價高低差超過 2.5 倍；有長約支撐的只有矽光子，不足以壓低 Bear 機率"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"重複下單的訊號已經齊備：book-to-bill 遠高於 2、交期拉長、開始漲價。上一輪半導體族群從高點約跌 46%。ST 毛利率在 2023→2025 年由 47.9% 降到 33.9%，EPS 由 4.46 美元降到 0.18 美元（事實表年度財報段）","assumption":"book-to-bill 反映的是終端需求；重整會在 2028 上半年前完成","consequence":"2028 年訂單反轉與重整延誤同時發生：毛利率卡在 38–40%，2029 年 EPS 回到約 1.6 美元，股價跌到 25–30 美元，5 年虧損 40% 以上","ruling":"部分採納：Bear 機率定為 30%，路徑回撤下緣取 −60%。本條與唯一致命點部分重疊（重整延誤），這裡補上需求反轉的另一半","watch":"book-to-bill、分銷庫存相對標準目標的位置、閒置產能費用基點","not_applicable_reason":null,"evidence_refs":["cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#2"],"fact_refs":["f_kpi4_gross_margin_gaap","f_kpi7_guidance_q4_2026_gross_m"]},{"view":"論點成功但股東經濟變差","evidence":"TTM FCF 率 3.8%，同業為 24–36%；2024–2025 年 FCF 為負。2022–2025 年累計淨再投資約 71 億美元，共識 2028 年淨利約 34 億美元，仍低於 2023 年的 42 億。7 月新發 15 億美元可轉債，舊可轉債轉換交付約 420 萬股；矽光子產能要擴 4 倍以上，Crolles 擴產決定也在即；上游部分材料只來自單一地區的少數供應商","assumption":"營收成長與毛利率回升，會轉成 FCF 與每股盈餘","consequence":"營收到 180 億美元，但擴產吃掉現金、投入成本吃掉漲價、大客戶拿走議價空間，每股價值的成長遠低於營收","ruling":"採納：這是終端倍數只給 15 倍、資本配置評分偏弱的原因","watch":"2027 年 FCF 率是否 ≥10%、淨資本支出占營收比重、股數變化","not_applicable_reason":null,"evidence_refs":["geo_supply_chain#2"],"fact_refs":["f_peer_stm_fcf_margin_pct","f_kpi3_free_cash_flow_non_gaap","f_shares_diluted_m"]},{"view":"價格已反映太多","evidence":"FY2028 共識 3.79 美元已含重整完整效益；EV/S 2.9 倍、P/S 3.06 倍都在自身 4 個年度端點的最高；賣方目標價 26–98 美元，高低差超過 3 倍。7 月的 Q3 指引低於預期後股價下跌，Barclays 把目標價降到 60 美元","assumption":"市場以 2028 年共識為定價錨","consequence":"若 2028 年 EPS 只有 3.0 美元、倍數 14 倍，2028 年股價約 42 美元，比現價還低","ruling":"部分採納：股價沒有過熱（RSI 43.9，26 週 −16%），但安全邊際不夠，等 41 美元以下再進場","watch":"FY2028 共識 EPS 的修正方向、1 月法說給的 2028 指引","not_applicable_reason":null,"evidence_refs":["capital_markets_pricing#2"],"fact_refs":["f_ev_s_current","f_ev_s_percentile","f_ps_percentile","f_consensus_eps_fy3","f_rsi14"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 🟡 → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=🟡","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 53.49 → 本次 46.74（-12.6%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=53.49","side_b":"本次 price_at_dd=46.74","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 53.49 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 53.49 美元：Bull 價 110、Bear 價 31，五年期望值 +36.0%，基準年化 7.0%，不對稱比 2.6","side_b":"本次情境、股價仍用 53.49 美元：Bull 價 114、Bear 價 28.8，五年期望值 +27.2%，基準年化 3.3%，不對稱比 2.45","ruling":"先換情境、股價不動：五年期望值少 8.8 個百分點，基準年化少 3.7 個百分點。不對稱比由 2.6 變為 2.45。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 53.49 美元：五年期望值 +27.2%，基準年化 3.3%，不對稱比 2.45","side_b":"本次情境、股價 46.74 美元：五年期望值 +45.6%，基準年化 6.2%，不對稱比 3.75","ruling":"再換股價、情境不動：起點價下跌 12.6%，五年期望值多 18.4 個百分點，基準年化多 2.8 個百分點，不對稱比由 2.45 升到 3.75。合計五年期望值比前份多 9.6 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"前份漂移：估值結論與裁決角色","cause":"價格變動","prior_field":["val"],"side_a":"前份（2026-07-24，股價 53.49 美元）估值判偏貴（🟠），裁決觀望","side_b":"本次股價 46.74 美元（−12.6%）；FY2027、FY2028 共識 EPS 由 2.68、3.85 美元變為 2.70、3.79 美元，大致持平。估值改判合理（🟡），但 Base 年化仍只有約 7%","ruling":"估值改善全部來自股價下跌，不是盈餘上修，所以估值結論只往前調一格，不改觀望方向；裁決與角色依本輪輸入重新決定","evidence_level":"事實表股價與共識快照","settle_metric":"股價對應的 Base 年化報酬","if_then":["若股價 ≤41 美元，且毛利率守住指引下緣→分批建立首倉","若股價先漲回 53 美元以上，但 1 月法說尚未給出 2027 資料中心目標→不追"],"evidence_refs":["capital_markets_pricing#2"]},{"axis":"前份漂移：基本面欄位","cause":"新證據","prior_field":["signal","trap","moat_trend","runway_post_y5","archetype","cycle_position"],"side_a":"前份：綜合訊號 B、價值陷阱 🟡、護城河趨勢 →、五年後成長跑道 🟢、循環/商品、早循環","side_b":"Q3 財報（2026-10-29）：營收高於指引中點；毛利率 37.3%，高於約 37% 的指引；Q4 指引 41.5 億美元，高於 7 月說的逾 40 億；資料中心 2026 年營收由逾 10 億上修到約 13 億美元；book-to-bill 由接近 2 升到遠高於 2。另一面，功率與分離式仍虧損，類比/MEMS 營益率年減，Apple 傳出減單","ruling":"新證據強化論點，但沒有改變方向，六欄全部維持前份值。循環位置仍判早循環：毛利率 37% 仍接近自身谷底區，營收比 2023 年高峰低約 16%；但 book-to-bill 與漲價已出現中段訊號，等 1 月法說再確認","evidence_level":"公司 6-K 與法說原文","settle_metric":"2027 上半年的 book-to-bill 與毛利率","if_then":["若 2027Q2 book-to-bill 仍 >1.5 且毛利率 ≥40%→循環位置改判中循環，停止加碼"],"evidence_refs":[]},{"axis":"前份漂移：情境機率與回撤","cause":"方法變動","prior_field":["p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份 Bull、Bear 機率各 30%，Max DD 為單點 −55%","side_b":"本次 Bull/Base/Bear 為 30/40/30，Max DD 改給範圍 −40%～−60%；情境終端年改為 FY2031E，倍數一律套在當年度 EPS","ruling":"機率不變：Q3 讓 2027 年的需求更確定，但共識成長超過內生上界，賣方目標價高低差也超過 2.5 倍，Bear 不能低於 30%。回撤由單點改成範圍是方法調整；中點 −50% 比前份略淺，因為 21 億美元淨現金與約 5 季的在手訂單，降低了近一年的流動性壓力","evidence_level":"判斷","settle_metric":"2027 上半年的 book-to-bill","if_then":["若 2027 上半年 book-to-bill 跌破 1→Bear 機率上調到 40%，減碼"],"evidence_refs":[]},{"axis":"行動門檻變動：進場重啟條件","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"事件錨：Q4 GM 淨向 40% 模型軌道確認＋製造重整如期＋分銷去化未反轉；或估值回踩至 EV/EBITDA 正常化（約 $42-45）","side_b":"股價 ≤41 美元（Base 年化約 10%）且最近一季毛利率不低於公司指引下緣；毛利率跌破指引下緣則取消","ruling":"前份的事件條件已兌現一半（Q4 毛利率指引約 39%，分銷庫存仍低於目標），剩下的約束是價格：在現價下，Base 年化只有約 7%。改用 Base 年化 10% 反推出約 41 美元的價位，取代 EV/EBITDA 區間；事件條件只保留毛利率不破指引下緣。進場後若毛利率跌破指引下緣就減碼，若重整確認失敗就清倉","evidence_level":"法說原文與情境推算","settle_metric":"股價與季度毛利率","if_then":["若股價跌到 41 美元以下且毛利率守住→分批反買，首倉 1/3","若毛利率跌破指引下緣→取消進場條件，已持有者減碼"],"evidence_refs":[]},{"axis":"Single Thing 變動：唯一致命點由空白改為製造重整完成時點","cause":"新證據","prior_field":["single_thing"],"side_a":"（前份為空，未設唯一致命點）","side_b":"製造重整的 4 座舊廠關閉與產品轉移（轉 300mm 矽、200mm SiC），能否在 2028 上半年前完成並取得客戶接受；目前 3 座已在掌握，1 座仍在談（2026-10-29 Grandi）","ruling":"前份把重整放在假設與風險裡，但沒有指定單一致命事件。本次依數學敏感度挑選：400 基點×約 180 億美元營收，約等於稅前 7.2 億美元，約占 2028 年共識 EPS 的 18%，是單一最大項。一旦發生就清倉","evidence_level":"法說原文","settle_metric":"第 4 座舊廠的客戶接受進度、毛利率階梯","if_then":["若公司宣布結構性改善延到 2028 下半年之後→清倉"],"evidence_refs":[]},{"axis":"行動門檻變動：淘汰指標","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"（前份未設淘汰指標）","side_b":"毛利率 2027Q3 <39%｜book-to-bill 連 2 季 <1｜2027 年資料中心營收 <26 億美元｜Apple 占比年降 ≥4 個百分點｜功率與分離式 2027 年營益率仍低於 −10%","ruling":"前份只有風險項的警戒值；本次落成五條可量測的門檻，任一觸發就減碼，毛利率與重整兩條同時觸發則清倉","evidence_level":"判斷","settle_metric":"各指標","if_then":["若兩條以上同時觸發→清倉"],"evidence_refs":[]},{"axis":"需求真偽：終端需求，還是交期拉長下的重複下單","cause":null,"prior_field":null,"side_a":"管理層：book-to-bill 遠高於 2，工業與通訊設備高於 3；在手訂單逾 200 億美元，約 5 季營收；個人電子 Q3 不是提前拉貨；即使 Q1 只有 86 天，仍有把握達到共識（2026-10-29 Chery）","side_b":"重複下單的典型組合同時出現：需求超過供給、交期拉長、選擇性漲價、分銷庫存低於目標。上一輪半導體族群從高點約跌 46%，ST 毛利率在 2023→2025 年掉了 14 個百分點","ruling":"不可調和（方向相反：一邊說 2027 年營收可持續，一邊說 2028 年會回吐）。⚖ 2027 年選管理層這一側：約 5 季的在手訂單加上對 Q1 共識的背書，短期證據較硬。2028 年以後不採信，以 Bear 30% 定價。關鍵數據點是每季 book-to-bill，以及分銷庫存相對標準目標的位置","evidence_level":"管理層口述加歷史類比；終端銷售資料事實表未涵蓋","settle_metric":"2027 上半年的 book-to-bill、分銷庫存、訂單取消率","if_then":["若 book-to-bill 跌到 1.2 以下而交期仍長（取消潮）→已持有者減碼一半，未持有者不進場","反向：若 2027 年中分銷庫存回到標準目標，且 book-to-bill 仍 >1.5→需求屬實，觸發後分批加碼到 3%"],"evidence_refs":["cyclical_prior_downcycle_behavior#2","cyclical_prior_downcycle_behavior#0"]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"早循環，在手訂單約 5 季，管理層對 Q1 共識有把握；現價只有 FY2028 共識的 12.3 倍；淨現金 21 億美元；26 週跌 16%，但基本面變好；賣方平均目標價 56–75 美元；資料中心與 LEO 帶來 2023 年沒有的第二曲線","side_b":"FY2028 共識已含重整 400 基點的完整效益；毛利率在同業墊底；EV/S 在自身 4 年的最高；共識 2028 年淨利 34 億美元仍低於 2023 年的 42 億，資本報酬峰對峰為負；賣方目標價高低差超過 3 倍","ruling":"可調和（程度差異）：買進論證在 2027 年成立，但現價要求 2028 年全部兌現。不在 46.74 美元買，等 41 美元或 1 月法說確認後再分批","evidence_level":"事實表與法說","settle_metric":"1 月法說給的 2027 資料中心目標與 Q4 毛利率","if_then":["若 1 月法說給出 2027 年資料中心 ≥30 億美元，且 Q4 毛利率 ≥40%→上調 Base，重算進場價（可能高於 41 美元）"],"evidence_refs":[]},{"axis":"產業態勢三軸","cause":null,"prior_field":null,"side_a":"競爭惡化：中國本土 SiC 與車用 MCU 自主化、產業整併、亞洲代工擴張（20-F 自述）","side_b":"結構轉好：AI 資料中心銅轉光、低軌衛星訂戶 2030 年前可達 2 億、800V 架構 2027 年放量（管理層口述）。其他結構變數：美國 232 條款與 100% 關稅威脅、中國出口管制","ruling":"雙向拉鋸：ST 在新利潤池（光互連、LEO）的位置轉好，在舊利潤池（中國車用、SiC）則受本土化擠壓；關稅是額外的不確定項","evidence_level":"20-F 與法說","settle_metric":"車用營收成長相對市場、資料中心營收","if_then":["若車用營收連 4 季落後市場 ≥5 個百分點→改判競爭惡化中，上調 Bear 機率"],"evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#3","regulatory_antitrust#1","reg_tariff_export#0"]},{"axis":"管理層前後說法對照","cause":null,"prior_field":null,"side_a":"2026-07-23 Chery、Grandi：Q3 毛利率約 37%、Q4 營收逾 40 億、2026 年資料中心逾 10 億，毛利率 40% 以上要等 2027 年底重整完成，並確認 2028 年 180 億美元營收目標。2026-05-04 El-Ouazzane：LEO 主客戶市占不會維持在 90% 以上","side_b":"2026-10-29：Q3 毛利率 37.3%、Q4 指引 41.5 億、資料中心約 13 億；中期毛利率模型 44–46%，結構性 400 基點在 2027 年底或 2028 年初出現。LEO 2027 年受產能限制而非需求限制，且「沒有技術接近」","ruling":"可調和：近期財測都兌現或略超，可信度加分。但 2028 年 180 億美元的營收目標，本次法說沒有重提，200 億在 7 月就已擱置。LEO 的說法從承認份額流失轉為強調領先，屬語氣差異，份額下降已計入客戶集中風險","evidence_level":"逐字稿","settle_metric":"1 月法說是否重申 2028 年 180 億美元","if_then":["若 1 月法說下修或不再提 2028 年 180 億美元→削弱營收與毛利率兩項假設，Bull 機率降到 20%"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"Q4 2026 財報與 2027 年資料中心目標（預計 2027 年 1 月）","type":"假設驗證","maps_to":"H3","metric":"2027 年資料中心營收目標","threshold":"<26 億美元（未達 2026 年約 13 億的翻倍）","action":"削弱第二曲線假設；暫停首倉計畫，重算 Bull 機率","source_freq":"年度目標，1 月法說","date":"2027-01"},{"n":2,"text":"季度毛利率是否走在重整路徑上","type":"假設驗證","maps_to":"H2","metric":"GAAP 季度毛利率","threshold":"Q4 2026 <37%，或 2027Q3 <39%","action":"已持有者減碼一半；未持有者取消進場條件","source_freq":"每季 6-K","date":"2027-01"},{"n":3,"text":"需求是否仍高於出貨","type":"假設驗證","maps_to":"H1","metric":"整體 book-to-bill 與在手訂單季數","threshold":"book-to-bill 連 2 季 <1，或在手訂單 <4 季營收","action":"減碼到半倉，停止加碼","source_freq":"每季法說","date":null,"evidence_refs":["cyclical_prior_downcycle_behavior#2"]},{"n":4,"text":"製造重整 4 座舊廠的關閉與客戶轉移","type":"Single Thing","maps_to":"H2","metric":"舊廠關閉與客戶接受進度","threshold":"公司宣布第 4 座舊廠的客戶轉移無法在 2028 上半年前完成，或結構性 400 基點改善延到 2028 下半年之後","action":"清倉；未持有者撤回進場條件，Base 改用 41% 毛利率重算","source_freq":"每季法說與年報","date":"2027-07"},{"n":5,"text":"最大客戶占比與自研進度","type":"風險","maps_to":"R3","metric":"Apple 占營收比重與 RF 自研進度","threshold":"20-F 揭露 Apple 占比年降 ≥4 個百分點，且確認 Apple 自研 RF 量產","action":"減碼三分之一","source_freq":"年度 20-F（約 2 月底）","date":"2027-02","evidence_refs":["customer_concentration_credit#0"]},{"n":6,"text":"關稅與出口管制的吸收能力","type":"風險","maps_to":"R5","metric":"公司歸因於關稅或出口管制的毛利率或營收影響","threshold":"單季 ≥100 基點毛利率，或 ≥3% 營收","action":"減碼三分之一，不追","source_freq":"每季法說","date":null,"evidence_refs":["reg_tariff_export#1"]},{"n":7,"text":"證券集體訴訟與專利案的里程碑","type":"風險","maps_to":"R6","metric":"SDNY 集體訴訟與 Purdue 專利案進度","threshold":"集體認證通過，且和解或判決 ≥2 億美元；或 Purdue 案審後動議敗訴，且賠償擴大","action":"集體認證通過加上不利和解→減碼一半","source_freq":"20-F 附註、半年報","date":"2027-02","evidence_refs":["major_events#1","major_events#2","lawsuit_class_action#0","lawsuit_class_action#1"]},{"n":8,"text":"價格回到 Base 年化 10% 的位置","type":"估值rearm","maps_to":"H1","metric":"股價與最近一季毛利率","threshold":"股價 ≤41 美元，且最近一季毛利率不低於指引下緣","action":"分批建立首倉，第一批 1/3","source_freq":"每日收盤","date":null},{"n":9,"text":"重整效益提前兌現","type":"加碼","maps_to":"H2","metric":"2027Q3 毛利率與舊廠轉移進度","threshold":"毛利率 ≥41%，且 4 座舊廠轉移都已取得客戶接受","action":"加碼第二批，總倉位不超過 3%","source_freq":"每季","date":"2027-10"},{"n":10,"text":"全面複審","type":"複審日期","maps_to":null,"metric":"Q4 2026 財報與 2027 年資料中心目標","threshold":"資料公布後","action":"重跑完整研究","source_freq":"一次","date":"2027-01"}],"kill_metrics":[{"metric":"GAAP 季度毛利率","bear_threshold":"2027Q3 <39%，或結構性改善延到 2028 下半年之後","window":"2026Q4–2027Q4","source":"公司 6-K 季報與法說","last_status":"ok"},{"metric":"整體 book-to-bill","bear_threshold":"連 2 季 <1","window":"每季","source":"法說口述","last_status":"ok"},{"metric":"資料中心營收","bear_threshold":"2027 年 <26 億美元","window":"FY2027（1 月法說給目標）","source":"法說與年報","last_status":"unknown"},{"metric":"Apple 占營收比重","bear_threshold":"年降 ≥4 個百分點，且確認自研 RF 量產","window":"年度","source":"20-F 客戶揭露","last_status":"warning"},{"metric":"功率與分離式分部營益率","bear_threshold":"2027 全年仍低於 −10%","window":"FY2027","source":"季報分部資料","last_status":"warning"}],"evidence_dismissed":[],"action_conditions":{"rearm_trigger":"股價 ≤41 美元（Base 年化約 10%）且最近一季毛利率不低於公司指引下緣；毛利率跌破指引下緣則取消","exec_line":"觸發後分三批：第一批 1/3；1 月法說確認 2027 年資料中心 ≥26 億美元後，進第二批；2027Q3 毛利率 ≥41% 後，進第三批。路徑回撤可能到 −60%，單檔上限 3%","holding_cap":"3%（循環股，路徑回撤可能深於 −50%）"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":"早循環","cycle_verdict":"等回踩","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":false,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等股價 ≤41 美元（Base 情境年化約 10%）；現價 46.74 美元只對應約 7%，且 EV/S 貼近自身 4 年高點","asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null},"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8(val爭議)","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='C'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":true,"basis":"capalloc_grade='C'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟢', val='🟡', moat_trend='→', week26=-15.92, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='循環/商品', cycle_position='早循環', moat='C', moat_trend='→', cycle_gates_pass=False"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈機械讀數判定不可用，baseline rows 8/9/9b/10 的估值條件視為不可判 → 落 row8 觀望（保守方向）","hit":true,"basis":"val_denominator_disputed=True, val(機械讀數)='🟡'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":"中期 2-5 年","requires_critic":[]},"thesis":{"H":[{"id":"H1","text":"車用/工業補庫存加上 AI 資料中心與 LEO，讓 2027 年營收再成長約兩成，循環不在 2027 年見頂","2y":"2027 年營收 ≥165 億美元（共識約 174 億），且每季 book-to-bill >1","5y":null,"10y":null,"threshold":"2027 年營收 ≥165 億美元；每季 book-to-bill >1；在手訂單 ≥4 季營收（Q3 約 5 季，逾 200 億美元）","source":"公司季報 6-K 與法說（2026-10-29 Chery）","drift_rule":"TTM 營收連 2 季偏離門檻路徑 ≥5% 為削弱，連 3 季 ≥10% 為反轉"},{"id":"H2","text":"製造重整（關閉 4 座舊廠，轉 300mm 矽與 200mm SiC）在 2027 年底至 2028 年初帶來 400 基點以上的結構性毛利率改善，2028 年毛利率進入 44–46% 的中期模型","2y":"Q4 2026 毛利率約 39%；2027Q3 ≥40%（閒置與一次性成本約 70 基點，在 2027 下半年大致消失）","5y":"2028 全年毛利率 ≥44%","10y":null,"threshold":"Q4 2026 ≥37%（指引下緣）；2027Q3 ≥40%；2028 全年 ≥44%","source":"2026-10-29 法說 Grandi：4 座舊廠中 3 座的客戶接受已在掌握，1 座仍在談；結構性改善會以階梯方式出現","drift_rule":"季度毛利率連 4 季低於門檻路徑 ≥5%（相對值）為削弱，連 6 季 ≥10% 為反轉"},{"id":"H3","text":"資料中心（矽光子、電子 IC、MCU、電源）與 LEO 成為第二條成長曲線，並延續到 2028 年以後","2y":"2027 年資料中心營收 ≥26 億美元；LEO 營收不低於 2026 年","5y":"通訊設備與電腦周邊占營收 ≥25%（Q4 2026 指引略高於 20%）","10y":null,"threshold":"資料中心 2026 年約 13 億→2027 年 ≥26 億美元；矽光子產能 2027 年如期擴 4 倍以上","source":"2026-10-29 法說 Chery、El-Ouazzane；2027 年 1 月法說將給出 2027 數字與 2028 指引","drift_rule":"連 4 季低於路徑 ≥5% 為削弱，連 6 季 ≥10% 為反轉；1 月給的 2027 目標若低於 26 億美元，直接視為削弱"}],"R":[{"id":"R1","text":"重整延誤或效益縮水：第 4 座舊廠的客戶轉移沒談妥；類比/MEMS 分部營收成長，營益率卻仍年減；投入成本上漲吃掉漲價","h_ref":"H2","clock":"🔥","threshold":"2027Q3 毛利率 <39%，或公司把結構性改善延到 2028 下半年之後","evidence_refs":["cyclical_prior_downcycle_behavior#0"]},{"id":"R2","text":"重複下單退潮：交期拉長、漲價、book-to-bill 遠高於 2，是循環過熱前的典型組合；若 2027 年出現取消潮，營收與毛利率會同時回落","h_ref":"H1","clock":"⚡","threshold":"book-to-bill 連 2 季 <1，或分銷庫存回到標準目標以上，同時訂單下滑","evidence_refs":["cyclical_prior_downcycle_behavior#2"]},{"id":"R3","text":"客戶集中與垂直整合：Apple 占 2025 年營收 17.7%，連三年上升，並傳出自研無線/RF 晶片、削減 iPhone 18 Pro 訂單；LEO 主客戶市占管理層自承會降到 90% 以下；資料中心客戶以最佳組合分開採購","h_ref":"H3","clock":"🐢","threshold":"Apple 占比年降 ≥4 個百分點，且確認自研 RF 量產；或 2027 年 LEO 營收低於 2026 年","evidence_refs":["customer_concentration_credit#0","customer_second_source#0","customer_second_source#1","customer_second_source#2"]},{"id":"R4","text":"中國本土化與產業整併侵蝕份額：比亞迪、蔚來、吉利、小米擴大 SiC 布局，ST 以三安合資與華虹代工因應；20-F 自述整併與亞洲代工擴張可能侵蝕市占","h_ref":"H1","clock":"🐢","threshold":"車用營收年增率連 4 季落後公司所稱的市場成長（2026 年約 10%）≥5 個百分點","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1","competitive_share_entrants#3"]},{"id":"R5","text":"關稅、出口管制與地緣：美國 232 條款半導體調查、100% 晶片關稅威脅、中國出口管制；部分材料只來自單一地區的少數供應商","h_ref":"H1","clock":"🔥","threshold":"任一季公司把 ≥100 基點的毛利率變動或 ≥3% 的營收變動，歸因於關稅或出口限制","evidence_refs":["regulatory_antitrust#1","reg_tariff_export#0","reg_tariff_export#1","geo_supply_chain#1","geo_supply_chain#2"]},{"id":"R6","text":"管理層可信度與訴訟：SDNY 證券集體訴訟（涵蓋 2023-03 至 2025-01）的撤銷聲請遭駁回，案件續審；Purdue 專利案判賠 3,200 萬美元，審後動議進行中。毛利率模型是毛利率假設的支柱，若訴訟揭露財測程序有問題，會折損這項承諾的可信度","h_ref":"H2","clock":"🐢","threshold":"集體認證通過，且和解或判決 ≥2 億美元；或法院認定揭露不實","evidence_refs":["major_events#1","major_events#2","lawsuit_class_action#0","lawsuit_class_action#1"]}],"single_thing":{"description":"製造重整的 4 座舊廠關閉與產品轉移（轉 300mm 矽、200mm SiC），能否在 2028 上半年前完成並取得客戶接受；目前 3 座已在掌握，1 座仍在談（2026-10-29 Grandi）","why_fatal":"這是 2028 年盈餘最大的單一敏感項：400 基點×約 180 億美元營收，約等於稅前 7.2 億美元，約占 2028 年共識 EPS 的 18%。少了它，毛利率會停在約 41%，44–46% 的中期模型與追上同業的說法都不成立，倍數也會被壓縮","if_happens":"2028 年 EPS 比共識少約 0.7 美元（到約 3.1 美元），Base 終值降到約 50 美元，年化報酬只剩約 2%；已持有者清倉，未持有者撤回進場條件","how_monitor":"每季法說的閒置產能費用與一次性成本基點、類比/MEMS 與功率分部營益率、第 4 座舊廠的客戶接受進度；1 月法說與 2027 年中的時程更新","probability":"約 30%（12–24 個月內宣布延後或效益縮水）"}},"appendix_a":{"growth_durability":6,"quality_score":5,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":17.31,"peg_fy2":0.43,"stress":{"pass":2,"total":3}},"eps_meta":{"base_eps_path":{"FY2025A":0.18,"FY2026E":1.34,"FY2027E":2.7,"FY2028E":3.79},"fy_end_month":12,"eps_basis":"Koyfin 共識（以公司調整後口徑為主）；FY2025A 用年報 GAAP 稀釋 EPS 0.18 美元（含減損與重整費用），基期與共識口徑不完全一致，三年 CAGR 參考性低"},"catalysts":[{"date":"2026-11-18","date_precision":null,"type":"product","event":"STM32 分析師電話會議（接在 11-03 STM32 Summit 之後）","impact":"低","watch":"MCU 新品，以及資料中心 MCU 2027 年翻倍的細節"},{"date":"2026-12","date_precision":"month","type":"capacity","event":"Crolles 300mm 擴產決定（CEO 稱年底前做出）","impact":"中","watch":"擴產規模，以及資本支出是否超出 20–22 億美元區間"},{"date":"2027-01","date_precision":"month","type":"guidance","event":"Q4 2026 財報：公布 2027 年資料中心營收數字、2028 指引與新分部架構","impact":"高","watch":"資料中心 2027 年 ≥26 億美元、Q4 毛利率約 39%、是否重申 2028 年 180 億美元"},{"date":"2027-02","date_precision":"month","type":"other","event":"FY2026 20-F：Apple 占營收比重與訴訟附註","impact":"中","watch":"Apple 占比是否從 17.7% 下降、集體訴訟進度"},{"date":"2027-12","date_precision":"quarter","type":"capacity","event":"舊廠關閉與重整帶來的結構性毛利率改善（2027 年底至 2028 年初）","impact":"高","watch":"第 4 座舊廠的客戶接受、毛利率是否階梯式上升"},{"date":null,"date_precision":null,"type":"regulatory","event":"美國 232 條款半導體關稅的後續","impact":"中","watch":"公司是否把毛利率或營收變動歸因於關稅"}]}
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
