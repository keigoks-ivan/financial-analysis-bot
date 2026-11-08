你是 DD 管線 v20 的判斷層閘（gate），標的 ABNB（20261108）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（34 條）
- `f_kpi0_gaap`（q1_business）｜營收（GAAP）＝4869 百萬美元｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 股東信/新聞稿 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0001559720/000119312526449727/d437988dex991.htm（numbers.latest_quarter_kpis.items[0]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-11-05））
- `f_kpi1_adjusted_ebitda_airbnb_n`（q1_business）｜Adjusted EBITDA（Airbnb 不報 Non-GAAP 營業利益，以此代）＝2509 百萬美元｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 股東信/新聞稿 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0001559720/000119312526449727/d437988dex991.htm（numbers.latest_quarter_kpis.items[1]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-11-05））
- `f_kpi2_gaap`（q1_business）｜GAAP 營業利益＝2021 百萬美元｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 股東信/新聞稿 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0001559720/000119312526449727/d437988dex991.htm（numbers.latest_quarter_kpis.items[2]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-11-05））
- `f_kpi5_q4_2026`（q1_business）｜下一季指引：Q4 2026 營收＝3,220–3,280 百萬美元（指引區間）｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司 Q3 2026 股東信/新聞稿 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0001559720/000119312526449727/d437988dex991.htm（numbers.latest_quarter_kpis.items[5]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-11-05））
- `f_kpi6_nights_and_seats_booked`（q1_business）｜Nights and Seats Booked＝155.0 百萬｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 股東信/新聞稿 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0001559720/000119312526449727/d437988dex991.htm（numbers.latest_quarter_kpis.items[6]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-11-05））
- `f_kpi7_gross_booking_value_gbv`（q1_business）｜Gross Booking Value（GBV）＝27.7 十億美元｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 股東信/新聞稿 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0001559720/000119312526449727/d437988dex991.htm（numbers.latest_quarter_kpis.items[7]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-11-05））
- `f_kpi8_adr`（q1_business）｜ADR＝178.83 美元｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 股東信/新聞稿 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0001559720/000119312526449727/d437988dex991.htm（numbers.latest_quarter_kpis.items[8]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-11-05））
- `f_peer_abnb_gross_margin_pct`（q2_moat）｜ABNB 毛利率＝82.9 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ABNB.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_abnb_operating_margin_pct`（q2_moat）｜ABNB 營業利益率＝20.81 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ABNB.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_abnb_fcf_margin_pct`（q2_moat）｜ABNB FCF 利潤率＝36.93 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ABNB.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_bkng_operating_margin_pct`（q2_moat）｜BKNG 營業利益率＝32.78 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.BKNG.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_bkng_fcf_margin_pct`（q2_moat）｜BKNG FCF 利潤率＝32.84 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.BKNG.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_expe_operating_margin_pct`（q2_moat）｜EXPE 營業利益率＝18.39 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.EXPE.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_expe_fcf_margin_pct`（q2_moat）｜EXPE FCF 利潤率＝23.09 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.EXPE.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_mar_operating_margin_pct`（q2_moat）｜MAR 營業利益率＝15.93 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MAR.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_hlt_operating_margin_pct`（q2_moat）｜HLT 營業利益率＝24.01 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.HLT.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝5.3 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-11-07）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝6.21 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-11-07）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝7.38 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-11-07）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝14384.32 USD m｜期間與口徑：2026-11-08／yfinance revenue_estimate 0y 平均（38 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝16101.96 USD m｜期間與口徑：2026-11-08／yfinance revenue_estimate +1y 平均（41 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi3_fcf`（q4_capital）｜自由現金流（FCF）＝1426 百萬美元｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 股東信/新聞稿 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0001559720/000119312526449727/d437988dex991.htm（numbers.latest_quarter_kpis.items[3]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-11-05））
- `f_kpi4_sbc`（q4_capital）｜股權激勵費用 SBC＝462 百萬美元｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 股東信/新聞稿 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0001559720/000119312526449727/d437988dex991.htm（numbers.latest_quarter_kpis.items[4]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-11-05））
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝-10075.0 USD m｜期間與口徑：2026-11-08／yfinance 最新一季：總債務 2515.0、現金 12590.0（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝596.74 m shares｜期間與口徑：2026-11-08／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝189.99 USD｜期間與口徑：2026-11-06（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-11-06（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝35.85 x｜期間與口徑：2026-11-07／分母＝FY1 EPS 5.3，分子＝快照價 189.99｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-11-07）
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝0.19 %｜期間與口徑：2026-08-13 → 2026-11-07／FY1 共識 EPS 5.29 → 5.3（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-11-07）
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝34.28 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-11-06（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝15.3 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝59.2 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝45.7 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ev_s_fwd`（q5_valuation）｜EV/S（EV ÷ FY1 共識營收）＝7.18 x｜期間與口徑：2026-11-08／f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）｜kind：estimate
  - 來源：—（numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_ev_m`（q5_valuation）｜目前企業價值 EV（市值＋淨負債）＝103300.05 USD m｜期間與口徑：2026-11-08／市值 113375.05 ＋ 淨負債 -10075.0｜kind：realized
  - 來源：—（numbers.capital_structure.ev_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null

### findings_digest 中方向為負或來源衝突的條目（10 條）
- `competitive_share_entrants#0`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K 列出競爭者含 OTA、搜尋引擎、meta-search、連鎖飯店、物業管理公司與體驗平台；並提到擁有既有消費者關係的對手可能打造「super-apps」進入旅遊市場，可能推高獲客成本；部分物業管理者鼓勵直訂繞過平台。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-12）｜affects：moat_trend、thesis.R
- `supply_demand_durability#2`（supply_demand_durability｜方向 -｜狀態 ok）：UK short-term rental supply kept growing YoY through June 2026 while nights reserved (5.8M) were broadly flat vs 2025 and below 2024.
  - 來源：VisitBritain / Lighthouse short-term rental report（as_of 2026-06-30）｜affects：thesis.R
- `regulatory_antitrust#1`（regulatory_antitrust｜方向 -｜狀態 ok）：FY2025 10-K risk factors: European Commission is conducting investigations into preferential tax treatments that may change how foreign operations are taxed; could raise effective tax rate.
  - 來源：SEC EDGAR 10-K FY2025 Item 1A Risk Factors（as_of 2026-02-12）｜affects：thesis.R、valuation
- `regulatory_antitrust#2`（regulatory_antitrust｜方向 -｜狀態 ok）：European Commission proposed Affordable Housing Act giving local authorities a clear legal basis to restrict Airbnb and other short-term rentals; needs approval of member states and Parliament.
  - 來源：Foster Garvey, Duff on Hospitality Law: Europe moves to rein in short-term rentals（as_of 2026-09-16）｜affects：thesis.R、decision_inputs.bear
- `regulatory_antitrust#3`（regulatory_antitrust｜方向 -｜狀態 ok）：Hungarian competition authority opened proceeding against Airbnb Ireland over suspected misleading consumer information.
  - 來源：Portfolio.hu: Hungarian competition watchdog launches investigation into Airbnb（as_of 2025-08-07）｜affects：thesis.R
- `reg_tariff_export#1`（reg_tariff_export｜方向 -｜狀態 ok）：ABNB 10-K 載明須遵守 OFAC 等制裁法規，未來在主要業務地區的制裁可能對業務造成重大影響（制裁，非商品出口管制）。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-12）｜affects：thesis.R
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：Airbnb 以 AWS 為主要平台代管與交付基礎設施（單一雲端供應商依賴）
  - 來源：Airbnb FY2025 10-K（as_of 2026-02-12）｜affects：decision_inputs.bear、thesis.R
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：Airbnb 揭露系統未具完整資料儲存／處理／支付處理備援
  - 來源：Airbnb FY2024 10-K（as_of 2025-02-13）｜affects：decision_inputs.bear、thesis.R
- `geo_supply_chain#2`（geo_supply_chain｜方向 -｜狀態 ok）：2026 Q1 財報：伊朗相關戰事壓低 EMEA 與亞太需求，預期拖累 Q2 夜數成長約 1 個百分點
  - 來源：MarketScreener 'Airbnb flags Middle East war impact on second quarter growth'（as_of 2026-05-07）｜affects：thesis.R、decision_inputs.bear
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：10-K 風險因子：Airbnb 使用第三方授權的 AI/ML 技術，其規模化採用取決於第三方軟體、基礎設施或 AI 模型的取得，公司無法控制其品質、可得性與定價；若不可用或條款不利，產品吸引力可能下降。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-12）｜affects：moat_trend、thesis.R

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 3 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ABNB_20261108/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":386.4,"bear_5y_price":99.2,"p_bull_pct":25,"p_bear_pct":30,"upside_5y_pct":37.7,"ev5y_pct":28.5,"irr_base_pct":6.6,"asym_ratio":1.8,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":5.3,"pe":35.85,"basis":"FY2026E 共識每股盈餘（Koyfin，2026-11-07），與終端倍數同為當年度盈餘口徑"},"eps":{"bull":[6.6,8.0,9.7,11.6,13.8],"base":[6.2,7.3,8.4,9.6,10.9],"bear":[5.6,5.8,5.9,6.0,6.2]},"pe":{"bull":28,"base":24,"bear":16},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0,"net_buyback":0},"second_stage":{"bull_cagr_pct":14,"base_cagr_pct":11},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### ABNB_Q2_2026_Earnings_Call_20260806.md
- 2026-08-06｜CFO｜guidance：Q3 營收財測區間（原話："revenue of $4.69 billion to $4.77 billion"）
- 2026-08-06｜CFO｜guidance：Q3 營收含約 3 個百分點匯率順風（原話："approximate 3 percentage point foreign exchange tailwind"）
- 2026-08-06｜CFO｜guidance：Q3 GBV 年增預期為中段十幾%（原話："We expect year-over-year GBV growth to be in the mid-teens"）
- 2026-08-06｜CFO｜guidance：Q3 財測未假設中東衝突有重大影響（原話："not assuming any significant impact related to the conflict"）
- 2026-08-06｜CFO｜guidance：Q3 調整後 EBITDA 利潤率預期略低於去年同期（原話："margin to be down slightly compared to Q3 2025"）
- 2026-08-06｜CFO｜guidance：全年營收成長上修至至少中段十幾%（原話："revenue growth to improve to at least mid-teens"）
- 2026-08-06｜CFO｜guidance：全年調整後 EBITDA 利潤率上修至至少 35.5%（原話："adjusted EBITDA margin to be at least 35.5%, up from 35%."）
- 2026-08-06｜CFO｜guidance：全年隱含 take rate 預期與 2025 大致持平（原話："our implied take rate to be relatively flat compared to 2025"）
- 2026-08-06｜CFO｜guidance：管理層說若無新業務客戶誘因 take rate 會略高（原話："our implied take rate to be slightly higher during the year"）
- 2026-08-06｜CFO｜guidance：管理層強調下半年較高基期下仍上修全年財測（原話："Even against tougher comps in the back half of the year"）
- 2026-08-06｜CFO｜margin：Q2 調整後 EBITDA 利潤率 35%（原話："an adjusted EBITDA margin of 35%"）
- 2026-08-06｜CFO｜margin：利潤率擴張來源之一：營運支援與產品開發效率（原話："cost efficiencies in operations and support"）
- 2026-08-06｜CFO｜margin：Q2 淨利含 $77 百萬稅務利益（原話："million tax benefit recorded in the current period"）
- 2026-08-06｜CFO｜margin：更新後財測假設全年 AI 支出大幅增加，同時利潤率擴張（原話："increase in terms of the AI spend over the course"）
- 2026-08-06｜CFO｜margin：CFO 稱在吸收 AI 成本下仍擴張利潤率（原話："expanding margins while absorbing that increased cost."）
- 2026-08-06｜CEO｜margin：客服每筆訂單成本年減約 16%（原話："support cost per booking declined about 16% year-over-year"）
- 2026-08-06｜CFO｜margin：CFO 稱不需像過去般增加人力（原話："need to grow our headcount at levels that we did in the past"）
- 2026-08-06｜CFO｜margin：FCF 數字口徑：近 12 個月 $4.8B（原話："generated $4.8 billion of free cash flow"）
- 2026-08-06｜CFO｜margin：未攤銷費用受 Reserve Now Pay Later 遞延影響的口徑（原話："unearned fees would have grown year-over-year in Q2"）
- 2026-08-06｜CFO｜margin：Reserve Now Pay Later 占 Q2 GBV 逾 20%（原話："over 20% of our total"）
- 2026-08-06｜CFO｜commitment：不給 2027 年以後的具體財測（原話："not going to give you a specific guide for '27 and beyond."）
- 2026-08-06｜CFO｜commitment：CFO 稱未來會尋求同樣的成長加利潤率擴張（原話："As we look forward, we're going to seek to do the same."）
- 2026-08-06｜CFO｜commitment：CFO 稱利潤率有相對下限、有機會就加碼投資（原話："floor in our ability to continue to invest against that."）
- 2026-08-06｜CFO｜commitment：單一服務費預計年底前完成推廣（原話："which we expect to be completed by year-end"）
- 2026-08-06｜CEO｜commitment：CEO 稱 AI 搜尋本月開始小流量測試（原話："We are beginning to put it in test this month."）
- 2026-08-06｜CEO｜commitment：AI 語音客服今年稍後推出（原話："Later this year, we will begin introducing AI voice support"）
- 2026-08-06｜CEO｜commitment：CEO 稱未來 1.5 年內可用 Airbnb 規劃完整行程（原話："you will absolutely be able to get to Airbnb"）
- 2026-08-06｜CEO｜commitment：CEO 稱對飯店要加大投入（原話："stepping on the gas given the reception"）
- 2026-08-06｜CEO｜commitment：CEO 稱未來一年聚焦旅遊一站式（原話："focused on the travel phase"）
- 2026-08-06｜CFO｜capital_allocation：Q2 回購 $1.1B（原話："we purchased $1.1 billion of our common stock"）
- 2026-08-06｜CFO｜capital_allocation：回購是資本配置核心之一（原話："Returning capital to shareholders remains a core component"）
- 2026-08-06｜CEO｜capital_allocation：併購策略維持機會主義，偏好自建（原話："our bias is always to grow organically"）
- 2026-08-06｜CEO｜capital_allocation：CEO 稱不需大額資本支出，推論成本相對 ROI 很小（原話："kind of de minimis relative to the ROI"）
- 2026-08-06｜CEO｜capital_allocation：CEO 稱不做 token maxing（原話："token maxing"）
- 2026-08-06｜CEO｜competition：CEO 稱表現優於最大同業（原話："we're outperforming our largest peers in travel"）
- 2026-08-06｜CEO｜competition：CEO 稱 CarTrawler 被 Expedia 收購不影響合作與併購策略（原話："I do not think this has"）
- 2026-08-06｜CEO｜competition：CEO 稱不做白標業務（原話："the white label business"）
- 2026-08-06｜CEO｜risk：CEO 稱 AI 是公司唯一的生存風險（原話："was the only existential risk to this company"）
- 2026-08-06｜CEO｜risk：CEO 稱政策是風險但非生存風險（原話："Now policy is a risk, but it's not an existential risk."）
- 2026-08-06｜CFO｜risk：CFO 稱中東衝突對業務影響低於預期（原話："from the conflict was less than we had anticipated"）
- 2026-08-06｜CEO｜product：CEO 稱飯店進展顯著優於預期（原話："going significantly better than I expected"）
- 2026-08-06｜CEO｜product：飯店夜數成長約為住宅 3 倍（原話："growing approximately 3x faster than our homes business."）
- 2026-08-06｜CEO｜product：首次訂飯店客人約 35% 回來訂住宅（原話："Roughly 35% of first-time hotel guests returned to Airbnb"）
- 2026-08-06｜CFO｜product：飯店供給擴至前 20 城並強調選擇性（原話："supply acquisition efforts to a top 20 number of cities"）
- 2026-08-06｜CFO｜product：飯店篩選標準：增益而非與住宅競爭（原話："inventory that can be accretive to the platform"）
- 2026-08-06｜CEO｜product：AI 搜尋預設仍是原搜尋，需數月重新訓練用戶（原話："months and months to retrain the customer"）
- 2026-08-06｜CEO｜product：CEO 稱定價是最大成長槓桿之一，遠大於 RNPL（原話："one of the biggest single levers for growth that we have"）
- 2026-08-06｜CEO｜product：CEO 稱體驗業務擴到數千市場不是今年（原話："and that's not this year"）
- 2026-08-06｜CEO｜product：CEO 稱租車會是最大的服務品類（原話："car rentals is going to be the biggest one by far"）
- 2026-08-06｜CEO｜product：服務多為夥伴模式，管理層稱成本不高（原話："there'll be much cost because they're partnerships"）
- 2026-08-06｜CEO｜product：CEO 稱 AI 是 Airbnb 發生過最好的事（原話："AI is the best thing to ever happen to Airbnb."）
- 2026-08-06｜CEO｜product：概念到上線時間最多縮短 60%（原話："reduced the time from concept to launch by as much as 60%"）
- 2026-08-06｜CFO｜product：CFO 稱 ADR 中臥室夜數成長是可持續的組成（原話："that component of ADR appreciation that is durable"）
- 2026-08-06｜CEO｜customer：首次訂房者成長加速至 11%（原話："growth among our first-time bookers accelerated to 11%"）
- 2026-08-06｜CEO｜customer：App 訂房夜數年增 23%（原話："Nights booked on our app grew 23% year-over-year"）
- 2026-08-06｜CEO｜customer：美法英澳核心市場成長加速（原話："the U.S., France, U.K. and Australia, all"）
- 2026-08-06｜CEO｜customer：AI 客服約 45% 問題無需真人（原話："Nearly 45% of issues that start with our AI assistant"）
- 2026-08-06｜CEO｜customer：CEO 稱成長可持續而非一次性（原話："This is durable growth."）
- 2026-08-06｜CEO｜customer：CEO 稱動能將延續到未來幾季（原話："we believe that momentum will continue through the"）
- 2026-08-06｜CFO｜competition：CFO 稱單一服務費對價格有下壓效果以維持競爭力（原話："has a kind of downward pressure on pricing"）

### 問答異常語氣（迴避／改口／保留）
- ABNB_Q2_2026_Earnings_Call_20260806.md｜問：Jed Kelly：單一服務費是否推廣到所有房東｜答法：CFO 答覆說年底前整個供給基礎都會用單一服務費；與稿中準備發言「大多數剩餘房東」口徑不同
- ABNB_Q2_2026_Earnings_Call_20260806.md｜問：Eric Sheridan：長期增量利潤率與再投資比例｜答法：CFO 明講不給 2027 年以後財測，改談過往紀錄與「相對下限」，未給數字
- ABNB_Q2_2026_Earnings_Call_20260806.md｜問：Lloyd Walmsley／Justin Post：飯店在哪些市場轉換率改善、規模與時間表｜答法：管理層以「單位數占比、成長 3 倍」等定性回答，未提供轉換率或市場別數字

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 3 | 2 |
| customer_second_source | not_applicable | 0 | 0 |
| customer_concentration_credit | not_applicable | 0 | 1 |
| supply_demand_durability | found | 3 | 2 |
| regulatory_antitrust | found | 4 | 3 |
| reg_tariff_export | found | 2 | 2 |
| geo_supply_chain | found | 3 | 2 |
| end_markets | found | 4 | 2 |
| substitute_technology | found | 3 | 1 |
| channel_business_model_shift | found | 2 | 2 |
| capital_markets_pricing | found | 4 | 3 |
| major_events | found | 2 | 4 |

未涵蓋／不適用軸的查詢詞原文（供判相關性）：
- **customer_second_source**（not_applicable）：（無查詢記錄）
- **customer_concentration_credit**（not_applicable）：Airbnb 10-K 2026 customer concentration no single customer 10% of revenue

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260703","verdict":"進場","role":"條件式核心持倉","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"核心 STR 市集成長維持雙位數、市佔續穩／擴大（網路效應不逆轉）","columns":{"2Y 驗證點":"Nights YoY ≥7%、GBV YoY ≥12%","5Y 驗證點":"營收 CAGR ≥12%、全球 STR 市佔 ≥44%","10Y 驗證點":"核心 GBV 仍為公司主體、市佔未被 Booking 反超","數字門檻":"Nights ≥7% YoY；全球 STR 市佔 ≥44%","來源":"公司 Q1'26 股東信、AirDNA/Yahoo Finance 市佔","漂移觸發":"Nights 連 2 季 &lt;5% → 削弱"}},{"id":"H2","text":"AI-native 直訂 app 抵禦 agentic AI 分發，take rate 不被結構性侵蝕","columns":{"2Y 驗證點":"Direct/app 訂房占比不降、take rate ≥12.5%","5Y 驗證點":"take rate ≥13%、ABNB 為旅客旅宿搜尋的獨立入口而非被比價後端","10Y 驗證點":"Airbnb 在 agentic 時代仍是「品牌直達」而非通用分發下游","數字門檻":"take rate ≥12.5%；直訂占比不連 2 季降","來源":"Chesky 法說（AI-native 策略）、Skift、OpenAI 撤 Buy Now（2026-03）","漂移觸發":"take rate 連 4 季 &lt;12.5% → 削弱（5Y 假設）"}},{"id":"H3","text":"Services＋Experiences 第二曲線兌現，佔營收由 ~1–2% 升至 ~10%","columns":{"2Y 驗證點":"Services/Experiences 顯性化為財報揭露項、flywheel 續存","5Y 驗證點":"Services＋Experiences 營收 ≥$2.5B（FY30）、佔比 ~10%","10Y 驗證點":"第二曲線成為第二成長引擎、Adj EBITDA margin 維持 ≥35%","數字門檻":"FY27 ≥$500M；FY30 ≥$2.5B；EBITDA margin ≥35%","來源":"2026 Summer Release、公司揭露（1/3 experience bookers 90 天內訂住宿）","漂移觸發":"跨 2 年度營收佔比停滯 &lt;3% → 反轉（10Y 假設）"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"短租監管系統性擴散：EU Reg 2024/1028（2026-05-20 全歐生效）＋ 各州登記/資料揭露常態化，抽走頂級城市高 ADR 供給","columns":{"對應假設":"H1","時間尺度":"🐢 長期（2+ 年慢變數）","監測指標":"都會區合規房源數、都會 GBV 占比、被下架房源規模","警戒閾值":"都會 GBV 占比連 2 年下滑 ＋ 供給淨減"}},{"id":"R2","text":"agentic AI 分發繞道：Google AI Mode partner 名單排除 ABNB，旅遊搜尋預設導向 6 家對手，直訂流量被抽","columns":{"對應假設":"H2","時間尺度":"🔥 中期（4–6 季）","監測指標":"Direct/app 訂房占比、take rate、付費行銷占營收比","警戒閾值":"直訂占比連 2 季降 ＋ 行銷/營收比升 &gt;2pp"}},{"id":"R3","text":"第二曲線擴不起來：Services/Experiences 重蹈 2019 覆轍，佔比長期卡在個位數，24.6x fwd PE 的期權價值蒸發","columns":{"對應假設":"H3","時間尺度":"🐢 長期（2+ 年慢變數）","監測指標":"Services＋Experiences 營收與佔比、flywheel（experience→stay 轉換）","警戒閾值":"跨 2 年度營收佔比停滯 &lt;3%"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":9.2,"ev5y_pct":55.0,"drift_watch_prior":{"dca_verdict":"進場","dca_role":"條件式核心持倉","signal":"B","val":"🟡","ma":"🟡","trap":"🟢","moat_trend":"→","runway_post_y5":"🟢","asym_ratio":5.0,"ev5y_pct":55.0,"irr_base_pct":9.2,"max_dd_pct":-55.0,"bull_5y_price":335.0,"bear_5y_price":104.0,"p_bull_pct":30.0,"p_bear_pct":25.0,"rearm_trigger":null,"price_at_dd":148.93,"archetype":null,"cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"ABNB","date":"2026-11-08","schema":"v15.0","contract":"v19","company_name":"Airbnb, Inc."},"oneliner":"Airbnb 重回雙位數成長、份額續升，生意比四個月前更好；但 189.99 美元已是今年預估盈餘 35.85 倍，基準情境五年年化約 6.6%，先不追，等 160 美元以下再評估。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ABNB_20261108/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ABNB_20261108/scenario.json","answers":{"q1_business":{"verdict":"Airbnb 賺旅客與房東成交時的服務費，錢卡在訂房入口：誰掌握旅客的起點，誰就收得到這筆費用。","reasoning":"收入來自房東單一服務費 15.5%，加上旅客保險等附加項；Q3 隱含抽成 17.6%，年減的主因是先訂後付讓 GBV 提前入帳，營收要等入住才認列。Q3 營收 48.69 億美元、年增 19%（不含匯率 16%），GAAP 營業利益 20.21 億美元，利益率 41.5%，這是全年最旺的一季，不能年化；截至 2026-06-30 近四季毛利率 82.9%、營業利益率 20.81%。公司不揭露營收分部，房東與旅客集中度事實表未涵蓋。供需判斷為結構性持久：四大區域夜數都是雙位數成長，美國短租 2026 年供給與需求同為年增 2.7%（AirDNA）。但 Q3 夜數 16% 裡有 3 點來自先訂後付；Q2 夜數 10%，扣掉不超過 2 點的先訂後付只有約 8%，這段加速還沒經過高基期檢驗。","fact_refs":["f_kpi0_gaap","f_kpi1_adjusted_ebitda_airbnb_n","f_kpi2_gaap","f_kpi5_q4_2026","f_kpi6_nights_and_seats_booked","f_kpi7_gross_booking_value_gbv","f_kpi8_adr","f_peer_abnb_gross_margin_pct","f_peer_abnb_operating_margin_pct"],"verdict_values":{"revenue_quality":"營收在入住時認列，比 GBV 慢一拍；Q3 年增 19% 裡有 3 點是匯率，Q4 指引也含約 2 點匯率順風，判斷成長要看不含匯率的數字。","unit_econ_note":"每筆訂單客服成本年減超過 17%，約 40% 客服問題不需真人處理；取消率由約 16% 升到約 19%，是先訂後付的代價。","archetype":{"primary":"品質複利成長","secondary":null,"confidence":"中","fingerprint":"毛利率約 83%、近 12 個月 FCF 利潤率 35%、淨現金 100.75 億美元、營收雙位數成長；投入資本事實表未涵蓋，所以信心給中。"},"industry":{"clock_phase":"II","sd_verdict_source":"線上住宿處於擴張期：Q3 四大區域夜數全部加速，北美低雙位數、EMEA 十幾%、亞太與拉美超過 20%（2026-11-05 股東信）。供需屬結構性持久，英國供給增加而夜數持平是局部過剩。","bargaining":{"up":"上游是 AWS 與第三方 AI 模型。公司以 AWS 為主要雲端，資料與支付處理沒有完整備援，這是單點依賴。","down":"房東常跨平台刊登，但 CEO 稱超過 60% 房源只在 Airbnb，這個比例只有公司口徑；旅客端 App 夜數占 66%。","geo":"外部變數是城市與歐盟短租法規，歐盟住宅法案草案讓地方政府有明確法源限制短租。"},"profit_pool_dir":"五年利潤池占比事實表未涵蓋；方向上份額往 Airbnb 集中，美國專業管理短租營收份額一年內由 36% 升到 43%。","tam_table":[{"item":"飯店市場規模","value":"約 9,000 億美元（CEO 於 2026-11-05 法說的說法，未經第三方驗證）"},{"item":"線上住宿平台份額","value":"42%（Skift Research，2026 年）；2019 年為 26%"},{"item":"美國專業管理短租份額","value":"訂單 51%、營收 43%（KeyData，2026 Q2）；一年前 47%、36%"},{"item":"飯店業務規模","value":"2026-08-06 法說只給單位數占比與成長約為住宅 3 倍的定性口徑"},{"item":"總住宿滲透率、分段年複合成長率、利潤池占比","value":"事實表未涵蓋"}]}}},"q2_moat":{"verdict":"護城河方向向上：雙邊網路加直接流量讓份額繼續擴大，定價力持穩。","reasoning":"機制是雙邊網路加品牌直達：房源獨特、旅客直接開 App，省下買流量的錢。可證方向用份額軸，因為同業 ROIC 差距算不出來：KeyData 顯示 2026 Q2 美國專業管理短租訂單份額由 47% 升到 51%、營收份額由 36% 升到 43%；Skift Research 的線上住宿份額由 2019 年 26% 升到 2026 年 42%。執行面擴大（Q3 上線 50 多項產品、首次訂房者成長 13%、App 夜數年增 29%），定價面穩定（抽成約持平、保險營收年增近 70%，但動態定價會壓低成交價）。可能看錯的地方：近四季營業利益率 20.81%，仍比 Booking 的 32.78% 低約 12 點，兩邊期間差一季；份額證據只來自兩個第三方，其中 KeyData 只看美國專業管理房源；AI 代理的威脅還沒有經過驗證。","fact_refs":["f_peer_abnb_gross_margin_pct","f_peer_abnb_operating_margin_pct","f_peer_abnb_fcf_margin_pct","f_peer_bkng_operating_margin_pct","f_peer_bkng_fcf_margin_pct","f_peer_expe_operating_margin_pct","f_peer_expe_fcf_margin_pct","f_peer_mar_operating_margin_pct","f_peer_hlt_operating_margin_pct"],"verdict_values":{"moat":{"mechanism":"雙邊網路加品牌直達：獨特房源吸引旅客直接打開 App，旅客規模再吸引房東，平台同時掌握預訂、支付與客服。","execution":8,"pricing":7,"grade":"B","trend":"↑","trend_evidence":"兩項第三方份額數據都上升：KeyData 2026 Q2 美國專業管理短租營收份額由 36% 升到 43%，Skift Research 線上住宿份額 42%。利潤率同時上升，2026 年調整後 EBITDA 利潤率指引由至少 35.5% 上修到約 36%，份額不是靠壓低獲利換來的。","competitor_notes":[{"name":"BKNG","strategy_note":"近四季營業利益率 32.78%（截至 2026-09-30，Airbnb 的 20.81% 截至 2026-06-30，差一季），仍是獲利最強的對手；Airbnb 挖來其住宿事業主管進攻飯店，雙方戰線開始重疊。"},{"name":"EXPE","strategy_note":"營業利益率 18.39%，旗下 Vrbo 超過四成訂單來自房東出資促銷，份額較靠花錢維持；Expedia 也買下 Airbnb 的租車夥伴 CarTrawler。"},{"name":"MAR","strategy_note":"營業利益率 15.93%；Airbnb 目前上架的是精品與獨立飯店，連鎖飯店暫時不是正面對手。"},{"name":"HLT","strategy_note":"營業利益率 24.01%、FCF 利潤率 14.49%；飯店業者的直接競爭在短住與商務，這正是 Airbnb 用飯店補的缺口。"}],"peer_na_reason":"事實表只有同業利潤率，沒有投入資本，算不出對 Booking 的 ROIC 差距；ABNB 的近四季截至 2026-06-30，同業截至 2026-09-30，差一季。","threats":[{"level":"🔴","text":"生態攻擊：擁有既有用戶關係的超級 App 與通用 AI 代理切進旅遊，可能拿走發現入口、推高獲客成本。目前通用代理訂單在每日近 50 萬筆訂單中占比非重大，10 月初見高後持平。AI 長在自有的預訂、支付與客服資產上時強化護城河，繞過入口時才是替代，分界年訂 2028 年，屆時看代理訂單占比與行銷費用率。","p":30,"evidence_refs":["competitive_share_entrants#0"]},{"level":"🟡","text":"公司的 AI 功能用到第三方模型與運算資源，品質、供應與定價都不在自己手上；管理層稱推論成本相對報酬很小，但只有定性說法。","p":20,"evidence_refs":["substitute_technology#0"]},{"level":"🟡","text":"Booking 與 Vrbo 的點對點競爭：房東常跨平台刊登，對手也能用促銷換房源曝光。","p":25,"evidence_refs":["competitive_share_entrants#1"]}],"roic_durability":{"quadrant":"高利益率×高周轉","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"旅客同時是使用者與付款者，決策者常是三人以上的同行團體；要解決的問題是有空間、划算的住宿，會因景氣延後，不會消失。讀數：Q3 首次訂房者成長 13%，四區域夜數全為雙位數成長。"},{"item":"決策層級","level":"🟢","text":"替代性要看單一間房與地點，不是看住宿這個品類。CEO 稱超過 60% 房源獨家，只是公司口徑；讀數：90% 旅客會傳訊給房東，App 夜數占 66%。漲價後流失率事實表未涵蓋。"},{"item":"價值鏈分配","level":"🟡","text":"房東拿走大部分交易額，平台隱含抽成 17.6%；房東可跨平台刊登，通用 AI 代理有機會在入口分走一段。CEO 對獨家房源能否換到談判籌碼回答還不確定，雲端與模型也集中在少數外部業者。"},{"item":"社會容忍度","level":"🟡","text":"短租的政治上限可能低於經濟上限：歐盟住宅法案草案要讓地方政府有明確法源限制短租，還需會員國與議會通過。法案通過且頂級城市房源淨減就轉紅。"}],"roiic":"無法計算：事實表未涵蓋投入資本、資本支出、折舊、營運資金變動與收購淨額","reinvest_rate":"無法計算，原因同上；實際再投資多走損益表，研發占營收 18.89%（同業對照表，截至 2026-06-30 近四季）","endo_ceiling":null,"formula_note":"代收款與未賺取費用可能讓投入資本接近零甚至為負，這個公式對平台公司不穩定。當期資本報酬的結論只到象限，沒有數值；內生上界改在成長題用營收成長當代理。"}}}},"q3_growth":{"verdict":"五年後成長跑道寬，第二曲線是飯店，但目前證據多來自管理層，還沒有財報數字。","reasoning":"成長以量為主、價為輔：Q3 夜數年增 16%（扣先訂後付約 13%），ADR 年增 4%，沒有併購貢獻。共識每股盈餘 FY2026E 5.30、FY2027E 6.21、FY2028E 7.38 美元（Koyfin，2026-11-07），兩年年化 18.0%；FY2025 基期的事實表數值有誤，所以不算三年年化。內生上界用資本公式算不出來，改用 FY2027 共識營收成長 11.9% 當代理。FY2026 到 FY2027 每股盈餘成長 17.2%，比營收多 5.2 點，其中淨回購約 1.5 點，其餘約 3.7 點靠利潤率擴張，可以歸因，但管理層說 2027 年把成長放第一，利潤率這段不能全信。飯店夜數成長約為住宅 3 倍（2026-08-06 CEO），CEO 稱未來幾年會有數十億美元營收，但沒有時間表，也沒有揭露數字。總住宿滲透率事實表未涵蓋，年數不換算。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_kpi5_q4_2026","f_kpi6_nights_and_seats_booked","f_kpi8_adr"],"verdict_values":{"growth":{"driver_mix":"量為主、價為輔，沒有併購，淨回購每年再加約 1.5 點每股盈餘。","runway_years":"事實表未涵蓋總住宿滲透率，無法換算","runway_post_y5":"🟢","endo_ceiling_basis":"資本公式缺投入資本與再投資資料，改用 FY2027 共識營收成長 11.9% 當代理上界；FY2026 到 FY2028 共識每股盈餘年化 18.0%，超過這個代理上界。","segments":[{"item":"北美夜數","value":"Q3 2026 低雙位數成長，四年來最快"},{"item":"EMEA 夜數","value":"Q3 2026 十幾%成長"},{"item":"亞太與拉美夜數","value":"Q3 2026 超過 20% 成長；巴西超過 30%，印度超過 60%"},{"item":"飯店","value":"上架 60 多個目的地，成長遠高於主業；2026-08-06 口徑為夜數成長約住宅 3 倍，營收未揭露"},{"item":"服務與體驗","value":"租車為成長最快的服務之一，營收未揭露"}],"decay_signals":[{"signal":"毛利率連 2 季年減","lit":false,"note":"近四季毛利率 82.9%，FY2025 為 82.96%，單季年比事實表未涵蓋"},{"signal":"核心市占近 12 個月縮減","lit":false,"note":"兩項第三方份額上升"},{"signal":"主力產品提價後銷量下滑","lit":false,"note":"ADR 年增 4%，夜數年增 16%"},{"signal":"每股盈餘成長高於營收成長超過 5 點","lit":true,"note":"FY2027 共識每股盈餘年增 17.2%、營收 11.9%，差 5.2 點"},{"signal":"FCF／淨利連 2 年低於 0.75","lit":false,"note":"Q3 單季約 0.75，FY2023～FY2025 年度 FCF 欄事實表為空值"},{"signal":"SBC 占營收超過 5% 且逐年上升","lit":null,"note":"Q3 為 9.5%，逐年趨勢事實表未涵蓋"},{"signal":"TAM 萎縮或被替代技術壓縮","lit":false,"note":"通用代理訂單目前非重大"},{"signal":"產業估值倍數近 3 年系統性下移","lit":null,"note":"事實表未涵蓋"},{"signal":"維護性資本支出占 FCF 超過 60%","lit":false,"note":"資本輕，Q3 資本支出增加 7,500 萬美元來自紐約辦公室"},{"signal":"停止投資新產能且收入 3 年內下滑","lit":false,"note":"營收逐年成長"}],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"資本配置紀律不錯：成長靠自己，回購金額大過股權激勵；回購均價查不到，回購報酬無法驗證。","reasoning":"Q3 FCF 14.26 億美元，對淨利約 19 億美元的比率約 0.75，受先訂後付與紐約辦公室支出影響；近 12 個月 FCF 49 億美元，利潤率 35%。SBC 4.62 億美元，占 Q3 營收 9.5%。Q2、Q3 合計回購 18 億美元，年化約 36 億美元；SBC 年化約 18.5 億美元，淨回購約占市值 1.5%。新授權 120 億美元加上餘額 27 億美元，約占市值 13%。淨現金 100.75 億美元，2026 年 3 月發行 25 億美元優先債。近 12 個月 FCF 殖利率約 4.3%，扣掉 SBC 後約 2.7%。近三年現金去向、債務到期結構、加權利率與回購均價事實表未涵蓋。","fact_refs":["f_kpi0_gaap","f_kpi3_fcf","f_kpi4_sbc","f_net_debt_m","f_shares_diluted_m"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":false,"passed":null,"input":"近 12 個月沒有併購項目，只有約 10% 的 WeRoad 少數股權投資；CEO 說偏好自建。"},{"name":"buyback_yield","applicable":true,"passed":null,"input":"事實表未涵蓋回購均價與十年期公債殖利率，無法判斷；現價的今年盈餘殖利率約 2.8%，FY2027 約 3.3%，FCF 殖利率約 4.3%。"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"Q3 回購 7 億美元大於 SBC 4.62 億美元，Q2 回購 11 億美元，淨股數下降；未扣回購的毛稀釋以 Q3 年化約占市值 1.6%。"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長是內生的，近 12 個月 8-K 沒有併購項目，資本回報靠回購，細節已寫在配置計分項；近三年現金去向與回購均價事實表未涵蓋。"}}}},"q5_valuation":{"verdict":"189.99 美元要賺到年化 10%，得靠五年每股盈餘年化 19.2% 且終端倍數守住 24 倍；成長我信得過，兩件事同時做到我不信。","reasoning":"現價是今年預估盈餘 35.85 倍、FY2027 的 30.59 倍，前瞻 EV/S 7.18 倍。五年後要到 306 美元才有 10% 年化，24 倍下每股盈餘要 12.75 美元，年化 19.2%，高於基準的 15.5%。基準 10.9 美元乘 24 倍是 261.6 美元，年化約 6.6%，全部來自盈餘成長，倍數收縮每年扣約 7.7 點。短期看 FY2027E 6.2 美元乘 30 倍得 186 美元（−2.1%）；中期看 FY2028E 7.3 美元乘 27 倍得 197.1 美元（＋3.7%）。FY1 共識近三個月只上修 0.19%，這段上漲幾乎都是倍數擴張，不過 Koyfin 快照可能還沒反映 11-05 的財報。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_3m_fy1_pct","f_week26_return_pct","f_pe_percentile","f_ps_percentile","f_ev_s_percentile","f_ev_s_fwd","f_ev_m"],"verdict_values":{"valuation":{"basis":"今年預估本益比搭配 PEG，輔以 FCF 殖利率","peers":{"expanded":false,"reason":"事實表沒有同業估值倍數，只有同業利潤率，無法做同業倍數對照；終端倍數改用自身現值與成長率對照。"},"fwd_pe":35.85,"peg":1.99,"percentile_5y":null,"val_light":"🟠","val_light_derivation":"今年預估本益比 35.85 倍，PEG 1.99（35.85 除以 FY2026 到 FY2028 共識年化 18.0%），貼近合理區間上緣；基準報酬年化約 6.6%，屬於弱的區間，所以結論是偏貴、未到極端。PEG 用 Koyfin 共識盈餘，Non-GAAP 口徑事實表未涵蓋。五年分位留空，因為事實表只有 4 個年度端點（trailing 本益比 15.3、P/S 59.2、EV/S 45.7），4 個點不足以當便宜的證據。賣方目標價是 6 月舊資料（均值 156、最高 181 美元）。","upside_short_pct":-2.1,"upside_mid_pct":3.7,"denominator_disputed":false,"denominator_note":"FY1 盈餘含稅務項目（Q2 有 7,700 萬美元稅務利益），快照也可能未更新，但共識即使上修 5%，本益比也只降到約 34 倍，結論不變。FY2025 稀釋每股盈餘 1.03 美元與淨利 25.11 億美元對不起來，本次不用它當基期。"}}},"q6_how_wrong":{"verdict":"最可能看錯的是成長的含金量：高基期後掉速比預期快會虧很多，繼續加速則會錯過一段行情。","reasoning":"成長熄火壓力測試：FY2029 年成長降到 15% 時 8.4 美元乘 25 倍得 210 美元（＋10.5%）；降到 10% 時 8.0 美元乘 16 倍得 128 美元（−32.6%）；降到 5% 時 7.5 美元乘 12 倍得 90 美元（−52.6%），三種裡只有一種守得住現價。產業態勢：競爭面沒有惡化，份額上升；結構面轉好，直接流量與新品類在擴大；法規與 AI 通路兩條在拉扯，裁決為雙向拉鋸。管理層沒有正面回答的項目：不給 2027 年財測，飯店轉換率與規模沒有數字，動態定價沒有數據，獨家房源能否換到談判籌碼也答不確定。歷史最大回撤、空方最強數字、訴訟與監管金額事實表未涵蓋。","fact_refs":["f_week26_return_pct","f_fwd_pe_latest","f_consensus_rev_3m_fy1_pct"],"verdict_values":{"trap":{"verdict":"🟡","label":"一項確定亮燈：每股盈餘成長比營收快 5.2 點；SBC 占營收 9.5%，逐年趨勢沒有資料"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":5.3,"pe":35.85,"basis":"FY2026E 共識每股盈餘（Koyfin，2026-11-07），與終端倍數同為當年度盈餘口徑"},"eps":{"bull":[6.6,8.0,9.7,11.6,13.8],"base":[6.2,7.3,8.4,9.6,10.9],"bear":[5.6,5.8,5.9,6.0,6.2]},"pe":{"bull":28,"base":24,"bear":16},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0,"net_buyback":0},"second_stage":{"bull_cagr_pct":14,"base_cagr_pct":11},"max_dd":{"lo":-53,"hi":-30,"basis":"下緣：Bear 第一年每股盈餘 5.6 美元乘 16 倍得 89.6 美元，較現價 −52.8%。上緣：回到 250 週均線 132.7 美元，較現價 −30.2%。公司歷史最大回撤事實表未涵蓋，未用於推導。","trigger_time":null},"basis":{"bull":"飯店與服務成為第二曲線，夜數維持雙位數，利潤率擴張加回購，FY2031 每股盈餘 13.8 美元，終端 28 倍。","base":"FY2027 營收成長約 12%，之後緩降到 9%，淨利率升到約 26%，股數年減約 1.5%，FY2031 每股盈餘 10.9 美元，終端 24 倍。回購效果已算進每股盈餘，所以淨回購殖利率填 0，實際約 1.5%。事實表未涵蓋同業本益比，倍數只用自身現值 35.85 倍與成長率對照。","bear":"高基期後夜數掉到中個位數，通用代理或法規推高獲客成本，FY2031 每股盈餘 6.2 美元，終端 16 倍。Bear 機率 30% 的依據是目前成長含先訂後付與匯率，且共識每股盈餘成長高於營收成長代理上界。"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"Q3 夜數 16% 有 3 點來自先訂後付，營收 19% 有 3 點來自匯率；CFO 說 Q3 是先訂後付淨效益的高點，取消率已由約 16% 升到約 19%。","assumption":"扣掉這些之後的 13% 夜數成長能撐過 2027 年高基期。","consequence":"五年後虧 50% 最可能的路徑：夜數掉到中個位數，倍數從 35.85 倍打到 16 倍，FY2031 股價約 99 美元。這條和 Single Thing 是同一條因果，Single Thing 是它的第一個驗證點。","ruling":"採納，Bear 機率由 25% 提高到 30%。目前沒有成長轉弱的數據，所以不把它當現況。","watch":"每季夜數年增、先訂後付淨貢獻、取消率。","evidence_refs":["end_markets#2"],"fact_refs":["f_kpi6_nights_and_seats_booked"]},{"view":"論點成功但股東經濟變差","evidence":"飯店要靠效果行銷，CEO 也說飯店是大宗商品；新業務的獎勵與折抵已壓抽成；先訂後付讓 2026 年 FCF 利潤率低於 EBITDA 利潤率；SBC 占 Q3 營收 9.5%；歐盟正在調查優惠稅制，可能拉高有效稅率。","assumption":"第二曲線的利潤率不低於主業，回購能真正縮減股數。","consequence":"營收成功但每股盈餘落後：行銷費用率升 2 點，以 FY2031 營收約 235 億美元、稅率 20% 估，每股盈餘少約 0.7 美元。","ruling":"部分採納：基準情境的 FY2027、FY2028 每股盈餘不高於共識，淨利率只算到約 26%。","watch":"行銷費用占營收比、FCF 與 EBITDA 利潤率差距、有效稅率、SBC 占營收比。","evidence_refs":["regulatory_antitrust#1"],"fact_refs":["f_kpi3_fcf","f_kpi4_sbc"]},{"view":"價格已反映太多","evidence":"26 週上漲 34.28%，今年預估本益比 35.85 倍，近三個月 FY1 共識只上修 0.19%；股價也已高於 6 月賣方最高目標價 181 美元，但那是舊資料。","assumption":"市場願意對 FY2027 約 12% 的營收成長繼續付 30 倍以上。","consequence":"就算基準情境完全做到，五年年化也只有約 6.6%。","ruling":"採納，這是目前的主要限制，結論改成不追，等 160 美元以下。","watch":"股價相對 160 美元、FY2027 共識上修幅度。","evidence_refs":["capital_markets_pricing#3"],"fact_refs":["f_week26_return_pct","f_fwd_pe_latest","f_consensus_rev_3m_fy1_pct"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 🟡 → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=🟡","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 148.93 → 本次 189.99（+27.6%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=148.93","side_b":"本次 price_at_dd=189.99","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]裁決由 dd_decision.py 機械路由：前份 進場 → 本次 觀望","cause":"新證據","prior_field":["dca_verdict"],"side_a":"前份 dca_verdict=進場","side_b":"本次 dca_verdict=觀望","ruling":"裁決是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。沒有單一輸入能還原，屬多欄共同：估值 🟡→🟠、陷阱燈 🟢→🟡、護城河趨勢 →→↑。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]角色由 dd_decision.py 機械路由：前份 條件式核心持倉 → 本次 追蹤","cause":"新證據","prior_field":["dca_role"],"side_a":"前份 dca_role=條件式核心持倉","side_b":"本次 dca_role=追蹤","ruling":"角色是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。沒有單一輸入能還原，屬多欄共同：估值 🟡→🟠、陷阱燈 🟢→🟡、護城河趨勢 →→↑。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 148.93 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 148.93 美元：Bull 價 335、Bear 價 104，五年期望值 +55.0%，基準年化 9.2%，不對稱比 5.0","side_b":"本次情境、股價仍用 148.93 美元：Bull 價 386.4、Bear 價 99.2，五年期望值 +63.9%，基準年化 11.9%，不對稱比 3.98","ruling":"先換情境、股價不動：五年期望值多 8.9 個百分點，基準年化多 2.7 個百分點。不對稱比由 5.0 變為 3.98。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變好。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 148.93 美元：五年期望值 +63.9%，基準年化 11.9%，不對稱比 3.98","side_b":"本次情境、股價 189.99 美元：五年期望值 +28.5%，基準年化 6.6%，不對稱比 1.8","ruling":"再換股價、情境不動：起點價上漲 27.6%，五年期望值少 35.4 個百分點，基準年化少 5.3 個百分點，不對稱比由 3.98 降到 1.8。合計五年期望值比前份少 26.5 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"估值與動作","cause":"價格變動","prior_field":["val","signal"],"side_a":"前份股價 148.93 美元，估值中性，判斷進場。","side_b":"本次股價 189.99 美元，估值偏貴，結論改為等價位，訊號等級維持 B。","ruling":"股價上漲 27.6%，共識盈餘沒有同步上修，安全邊際縮小，是這組變動的主因。情境機率與最大回撤來自情境重建，另列一條歸因。","evidence_level":"高","settle_metric":"股價與基準情境年化報酬","if_then":["若股價跌到 160 美元以下且夜數成長未受損，分批反買","若股價續漲但沒有新證據，不追"],"evidence_refs":[]},{"axis":"護城河方向、價值陷阱與成長跑道","cause":"新證據","prior_field":["moat_trend","trap","runway_post_y5"],"side_a":"前份：護城河持平，價值陷阱風險低，五年後成長跑道寬。","side_b":"本次：護城河向上，價值陷阱風險升到中等，跑道維持寬。","ruling":"KeyData 與 Skift 的份額上升、Q3 加速且利潤率同步上升，支持方向上調。共識每股盈餘比營收快 5.2 點，所以價值陷阱風險上調。飯店進展支持跑道維持，但營收仍未揭露。","evidence_level":"中","settle_metric":"第三方份額、App 夜數占比、飯店定量揭露","if_then":["若份額回落或 App 夜數占比連 2 季下降，護城河方向改回持平並停止加碼","若 FY2027 財報仍無飯店定量數字，跑道下調一級"],"evidence_refs":["competitive_share_entrants#2","end_markets#3","channel_business_model_shift#0"]},{"axis":"公司類型與循環位置欄位","cause":"方法變動","prior_field":["archetype","cycle_position"],"side_a":"前份兩欄皆空。","side_b":"本次公司類型歸為品質複利成長；公司不是循環股，循環位置維持留空。","ruling":"欄位補齊，與基本面變化無關。","evidence_level":"高","settle_metric":"不適用","if_then":[],"evidence_refs":[]},{"axis":"行動門檻：減碼、清倉與重啟","cause":"方法變動","prior_field":["rearm_trigger","kill_metrics"],"side_a":"前份摘要這兩欄為空，沒有減碼、清倉或重啟門檻。","side_b":"減碼：股價 ≥236 美元，或 2027 Q3 夜數年增 <8%；清倉：夜數年增 <5% 且 App 夜數占比連 2 季下降；重啟：股價 ≤160 美元。","ruling":"本次補上可執行門檻。160 美元是基準情境年化回到約 10% 的價位，236 美元約為 FY2027 共識盈餘 38 倍。","evidence_level":"中","settle_metric":"股價、夜數年增、App 夜數占比","if_then":["若觸及減碼門檻，減碼","若同時觸及清倉的兩項條件，清倉"],"evidence_refs":[]},{"axis":"Single Thing 變動","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未記錄唯一致命點，摘要此欄為空。","side_b":"2027 年第三季財報夜數年增低於 8%。","ruling":"先訂後付的高基期是本季新出現的最大敏感度，成長同時決定每股盈餘和倍數，所以定為唯一致命點。","evidence_level":"中","settle_metric":"2027 Q3 夜數年增","if_then":["若低於 8%，持有者減碼至半倉，未持有者取消進場條件","反向：若 ≥10%，Bear 機率下調到 25% 並重跑評估"],"evidence_refs":[]},{"axis":"論點門檻調整","cause":"新證據","prior_field":["thesis.H"],"side_a":"Nights ≥7% YoY；take rate ≥12.5%；FY27 Services＋Experiences ≥$500M、FY30 ≥$2.5B。","side_b":"扣先訂後付後夜數年增 ≥10%；App 夜數占比 ≥66%、全年隱含抽成年減不超過 30 個基點；飯店加服務加體驗營收 FY2028 ≥15 億美元、FY2031 ≥40 億美元。","ruling":"夜數已到雙位數，7% 太鬆；抽成受先訂後付的季度擾動，改看年變化；飯店已成為更大的第二曲線，納入口徑並順延時點。","evidence_level":"中","settle_metric":"每季股東信與法說","if_then":["若連 2 季低於新門檻 5% 以上，論點 H1 視為削弱並停止加碼"],"evidence_refs":[]},{"axis":"成長品質：先訂後付","cause":null,"prior_field":null,"side_a":"CEO：成長是可持續的，公司已重回成長模式。","side_b":"CFO：Q3 夜數有 3 點來自先訂後付，Q3 是淨效益高點，Q4 會下降；Q2 扣除後只有約 8%。","ruling":"可調和，採折衷：加速是真的，幅度要打折。管理層歸因未證，用 2027 年高基期驗證。","evidence_level":"中","settle_metric":"扣先訂後付後夜數年增","if_then":["若 2027 Q1、Q2 連兩季低於 10%，歸因證偽，Bear 機率上調到 35%","反向：若連兩季 ≥12%，基準情境 FY2028 每股盈餘上修"],"evidence_refs":["supply_demand_durability#0"]},{"axis":"AI 代理是威脅還是機會","cause":null,"prior_field":null,"side_a":"2026-08-06 法說，CEO 提到 AI 是公司唯一的生存風險。","side_b":"2026-11-05 法說，CEO 說不把代理看成威脅，代理訂單目前非重大，10 月初見高後持平。","ruling":"兩句可調和：前一句講長期可能性，後一句講當下訂單量；Q2 摘錄只有半句，前後文事實表未涵蓋。當下威脅小，長期未決，機率給 30%。代理訂單占比只有管理層定性說法，證據蓋不到 2028 年的風險窗，不能說風險已解。","evidence_level":"低","settle_metric":"代理訂單占比、App 夜數占比、行銷費用占營收比","if_then":["若 App 夜數占比連 2 季下降且行銷費用占營收比上升超過 2 個百分點，停止加碼並把終端倍數下修到 20 倍重算","反向：若自家代理上線後 App 夜數占比升破 70%，Bear 機率下調到 25%"],"evidence_refs":["substitute_technology#2","channel_business_model_shift#1"]},{"axis":"共識利潤率與管理層再投資","cause":null,"prior_field":null,"side_a":"共識 FY2027 每股盈餘成長 17.2%、營收 11.9%，隱含利潤率擴張。","side_b":"CFO 說 2027 年延續成長動能是第一優先，過去也把超額獲利再投入；Q4 調整後 EBITDA 利潤率指引略降，部分因行銷移到 Q4。","ruling":"可調和：基準情境 FY2027、FY2028 不高於共識。Q3 利潤率上升有部分是行銷時點，未證，用 Q4 驗證。","evidence_level":"中","settle_metric":"FY2027 調整後 EBITDA 利潤率指引","if_then":["若 2027 指引利潤率低於 35%，FY2027 每股盈餘下修到 5.9 美元重算","反向：若指引 ≥37%，FY2027 每股盈餘上修到 6.5 美元"],"evidence_refs":[]},{"axis":"現金流歸因","cause":null,"prior_field":null,"side_a":"CFO：Q3 FCF 只小幅成長，是先訂後付改變入帳時點。","side_b":"符合先訂後付資格的 GBV 已超過 40%，旅客付款延到入住前，過去的預收款優勢可能永久變小。","ruling":"管理層說法未證，繼續監測，先不採信也不否定。","evidence_level":"中","settle_metric":"FY2027 FCF 利潤率與調整後 EBITDA 利潤率差距","if_then":["若 FY2027 差距仍達 3 點以上，時間差的解釋視為證偽，停止加碼","反向：若差距回到 1 點以內，視為時間差成立"],"evidence_refs":[]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"四個區域同時加速；飯店、服務、自家代理三條線同時推進；新回購 120 億美元加上餘額 27 億美元約占市值 13%；淨現金 100.75 億美元；共識盈餘可能還沒反映這一季超預期。","side_b":"基準情境年化約 6.6%，要到年化 10%，五年每股盈餘年化要 19.2% 且倍數守住 24 倍。","ruling":"維持不追。限制只有價格一項，生意本身沒有問題。","evidence_level":"中","settle_metric":"股價相對 160 美元、FY2027 共識每股盈餘","if_then":["若 FY2027 共識每股盈餘上修到 6.8 美元以上且夜數成長仍 ≥12%，進場價同步上調到 175 美元","若股價續漲但證據未到，不追","若股價下跌而夜數成長未受損，分批反買"],"evidence_refs":["end_markets#0","end_markets#1"]},{"axis":"情境機率與最大回撤","cause":"方法變動","prior_field":["p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份情境：Bull 機率 30%、Bear 25%，最大回撤 −55%。","side_b":"本次重建情境：Bull 25%、Bear 30%，最大回撤 −53%～−30%。","ruling":"這三欄的變動來自情境重建，不是股價本身。Bull 機率下調是因為重建後 Bull 價位由 335 美元升到 386.4 美元，要達到的價位變高。Bear 上調的依據是重建時納入的先訂後付新證據：目前成長含先訂後付與匯率，共識每股盈餘成長也高於營收成長代理上界。最大回撤由單一數字改成區間，下緣用 Bear 第一年每股盈餘 5.6 美元乘 16 倍，上緣用 250 週均線 132.7 美元，現價只影響換算出的百分比。","evidence_level":"中","settle_metric":"扣先訂後付後夜數年增","if_then":["若 2027 Q1、Q2 扣先訂後付後夜數年增連兩季低於 10%，Bear 機率上調到 35%","反向：若 2027 Q3 夜數年增 ≥10%，Bear 機率下調到 25% 並重跑評估"],"evidence_refs":["end_markets#2"]}],"triggers":[{"n":1,"text":"股價回到 160 美元以下，基準情境年化回到約 10%，重跑評估後才建首倉。","type":"估值rearm","maps_to":"H1","metric":"股價","threshold":"收盤 ≤160 美元","action":"重跑評估，通過後建首倉","source_freq":"每日收盤價","date":null},{"n":2,"text":"跌到 145 美元以下而夜數成長未受損，分批反買，不當停損處理。","type":"加碼","maps_to":"H1","metric":"股價與扣先訂後付後夜數年增","threshold":"收盤 ≤145 美元，且夜數年增 ≥10%","action":"分批反買","source_freq":"每日收盤價、每季股東信","date":null},{"n":3,"text":"股價達到 FY2027 共識盈餘 38 倍時，持有者開始減碼。","type":"減碼","maps_to":"H1","metric":"股價","threshold":"收盤 ≥236 美元","action":"減碼","source_freq":"每日收盤價","date":null},{"n":4,"text":"2027 年第三季對上先訂後付高基期，夜數年增低於 8%。","type":"Single Thing","maps_to":"H1","metric":"夜數年增","threshold":"<8%","action":"減碼至半倉；未持有者取消進場條件","source_freq":"每季股東信","date":"2027-11-05"},{"n":5,"text":"2026 Q4 夜數是否達到管理層至少低雙位數的指引。","type":"假設驗證","maps_to":"H1","metric":"夜數年增","threshold":"≥10%","action":"未達標則停止加碼","source_freq":"每季股東信","date":"2027-02-15"},{"n":6,"text":"自家 AI 代理上線後，App 入口是否守住。","type":"假設驗證","maps_to":"H2","metric":"App 夜數占比","threshold":"≥66%","action":"未達標則停止加碼","source_freq":"每季法說","date":"2027-08-06"},{"n":7,"text":"飯店或服務是否出現定量揭露。","type":"假設驗證","maps_to":"H3","metric":"飯店加服務加體驗營收","threshold":"FY2027 財報給出定量數字","action":"未揭露則跑道下調一級","source_freq":"年度財報與法說","date":"2028-02-15"},{"n":8,"text":"通用代理開始分走入口並推高行銷費用。","type":"風險","maps_to":"R2","metric":"App 夜數占比、行銷費用占營收比","threshold":"App 占比連 2 季下降，且行銷費用率上升超過 2 個百分點","action":"停止加碼","source_freq":"每季財報","date":null,"evidence_refs":["competitive_share_entrants#0"]},{"n":9,"text":"歐盟住宅法案草案 2026-09 才提出，事實表無法確認賣方是否納入，在首個立法進度前不加碼。","type":"風險","maps_to":"R1","metric":"立法進度、EMEA 夜數成長","threshold":"法案通過，且 EMEA 夜數成長連 2 年低於整體 3 個百分點以上","action":"停止加碼","source_freq":"歐盟立法公告、每季股東信","date":null,"evidence_refs":["regulatory_antitrust#2"]},{"n":10,"text":"取消開始追上訂單，先訂後付的淨效益轉弱。","type":"風險","maps_to":"R4","metric":"取消率","threshold":"≥22%","action":"停止加碼","source_freq":"每季法說","date":null},{"n":11,"text":"戰事或歐洲動盪開始實質壓低需求。公司損益層用 EMEA 夜數判斷吸收是否失敗，不預測地緣事件。","type":"風險","maps_to":"R5","metric":"EMEA 夜數成長與公司量化的拖累","threshold":"EMEA 掉到個位數，且拖累 ≥1 個百分點","action":"停止加碼","source_freq":"每季股東信","date":null,"evidence_refs":["geo_supply_chain#2"]},{"n":12,"text":"成熟市場供給過剩由局部擴散。","type":"風險","maps_to":"R6","metric":"英國短租夜數、美國短租占用率","threshold":"英國夜數連 4 季年減，或美國占用率低於 55%","action":"停止加碼","source_freq":"VisitBritain、AirDNA","date":null,"evidence_refs":["supply_demand_durability#2"]},{"n":13,"text":"成長掉到個位數低段，入口也開始流失，論點失效。","type":"清倉","maps_to":"H1＋H2","metric":"夜數年增、App 夜數占比","threshold":"夜數年增 <5%，且 App 占比連 2 季下降","action":"清倉","source_freq":"每季股東信與法說","date":null},{"n":14,"text":"Q4 財報與 2027 全年展望後複審。","type":"複審日期","maps_to":"H1","metric":"複審","threshold":"2027 年 2 月財報後","action":"重跑評估","source_freq":"一次性","date":"2027-02-15"}],"kill_metrics":[{"metric":"夜數年增（2027 Q3，對上先訂後付高基期）","bear_threshold":"低於 8%","window":"2027 Q3 財報","source":"公司股東信","last_status":"ok"},{"metric":"App 夜數占比","bear_threshold":"連 2 季下降且低於 66%","window":"每季","source":"公司法說","last_status":"ok"},{"metric":"取消率","bear_threshold":"≥22%（2026 Q3 約 19%）","window":"每季","source":"公司法說","last_status":"warning"},{"metric":"行銷費用占營收比","bear_threshold":"年增超過 2 個百分點","window":"連 2 季","source":"公司財報；現值事實表未涵蓋","last_status":"unknown"},{"metric":"全年調整後 EBITDA 利潤率","bear_threshold":"低於 34%（2026 指引約 36%）","window":"年度","source":"公司股東信","last_status":"ok"}],"evidence_dismissed":[{"ref":"reg_tariff_export#1","reason":"這是 10-K 的假設性風險因子樣板文字，未指明受制裁地區、受影響營收或已發生事件，證據本身沒有可驗證內容。"},{"ref":"$.answers.q2_moat.verdict_values.moat.roic_durability","reason":"閘的描述正確，這裡沒有誤讀可指，但這條無法用改欄位處理：事實表沒有投入資本、資本支出、折舊、營運資金變動與收購淨額，增量資本報酬率、再投資率與內生上界都算不出來，填任何數字都是編造，所以維持無法計算與空值。替代做法已寫在成長題：用 FY2027 共識營收成長 11.9% 當代理上界，並寫明共識每股盈餘年化 18.0% 超過這個上界。"}],"action_conditions":{"rearm_trigger":"股價收盤 ≤160 美元（約 FY2027 共識盈餘 26 倍，基準年化回到約 10%），重跑評估後才建首倉","exec_line":"未持有：現價不買，股價到 160 美元以下重跑評估後先建 3% 以內首倉。持有：不加碼，236 美元以上開始減碼。"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":null,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等股價收盤 160 美元以下；若 FY2027 共識每股盈餘上修到 6.8 美元以上且夜數成長仍 ≥12%，等待價位上調到 175 美元。","qc48_result":"fail","qc48_note":"Bull 路徑缺分部量價骨架，歷史實現報酬也不支持；而 runway 的 🟢 沒有滲透率數字，第二曲線只有管理層說法、沒有財報數字，所以這個 Bull 依據站不住。"},"thesis":{"H":[{"id":"H1","text":"扣掉先訂後付的一次性拉抬後，住宿主業夜數仍維持雙位數成長，份額續升","2y":"2027 全年夜數年增 ≥10%，GBV 年增 ≥12%","5y":"FY2031 營收較 FY2026 年化成長 ≥10%","10y":"住宅仍是 GBV 主體，線上住宿份額未被 Booking 反超","threshold":"扣先訂後付後夜數年增 ≥10%（2026 Q3 約 13%）；2027 Q3 對上高基期仍 ≥8%","source":"公司股東信與法說、KeyData 專業管理短租份額、Skift Research","drift_rule":"連 2 季低於門檻 5% 以上視為削弱，連 3 季低於門檻 10% 以上視為反轉"},{"id":"H2","text":"自家 App 與即將上線的旅遊代理維持訂單主入口，通用 AI 代理只做導流，抽成不被結構性侵蝕","2y":"App 夜數占比不低於 66%，通用代理訂單仍非重大，自家代理 2027 上半年上線","5y":"全年隱含抽成不低於 FY2026，行銷費用占營收比上升不超過 2 個百分點","10y":"Airbnb 仍是旅客直接打開的品牌，不是通用代理後面的比價貨架","threshold":"App 夜數占比 ≥66%；全年隱含抽成年減不超過 30 個基點","source":"公司法說與股東信；通用代理訂單量只有管理層定性說法，沒有第三方數據","drift_rule":"連 4 季偏離門檻 5% 以上視為削弱，連 6 季偏離門檻 10% 以上視為反轉"},{"id":"H3","text":"飯店、服務與體驗長成可揭露的第二成長曲線，帶來新客且不拖垮利潤率","2y":"FY2027 財報或法說給出飯店或服務的定量數字，飯店夜數成長仍為住宅 2 倍以上","5y":"飯店加服務加體驗營收 FY2031 ≥40 億美元","10y":"第二曲線成為獨立成長引擎，調整後 EBITDA 利潤率仍 ≥35%","threshold":"FY2028 營收 ≥15 億美元；FY2031 ≥40 億美元；調整後 EBITDA 利潤率 ≥35%","source":"公司股東信與法說；目前飯店與服務營收未揭露","drift_rule":"跨 2 個年度低於門檻視為削弱，跨 3 個年度低於門檻視為反轉"}],"R":[{"id":"R1","text":"短租法規擴散：歐盟住宅法案草案讓地方政府有明確法源限制短租，匈牙利也因消費者資訊問題立案；受影響營收事實表未涵蓋。","h_ref":"H1","clock":"🐢","threshold":"法案通過，且 EMEA 夜數成長連 2 年低於公司整體 3 個百分點以上","evidence_refs":["regulatory_antitrust#2","regulatory_antitrust#3"]},{"id":"R2","text":"通用 AI 代理拿走旅遊發現入口，Airbnb 變成後端貨架，要付費才買得到流量。","h_ref":"H2","clock":"🔥","threshold":"App 夜數占比連 2 季下降，且行銷費用占營收比上升超過 2 個百分點","evidence_refs":["substitute_technology#1","channel_business_model_shift#1"]},{"id":"R3","text":"飯店與服務擴不起來，或規模做大但靠補貼，第二曲線的溢價落空。","h_ref":"H3","clock":"🐢","threshold":"跨 2 個年度沒有定量揭露，或營收占比停在 3% 以下","evidence_refs":["channel_business_model_shift#0"]},{"id":"R4","text":"先訂後付退潮：取消開始追上訂單，2027 年對上高基期。","h_ref":"H1","clock":"⚡","threshold":"取消率 ≥22%，或單季夜數年增低於 10%","evidence_refs":[]},{"id":"R5","text":"戰事與歐洲動盪壓需求：2026 Q1 財報估計伊朗相關戰事拖累 Q2 夜數成長約 1 點，Q4 指引未納入持續性影響。","h_ref":"H1","clock":"⚡","threshold":"EMEA 夜數成長掉到個位數，且公司量化的拖累 ≥1 個百分點","evidence_refs":["geo_supply_chain#2"]},{"id":"R6","text":"成熟市場供給過剩：英國短租供給續增，2026 年 6 月夜數 580 萬晚與 2025 年持平、低於 2024 年，房東收入下滑後可能退場。","h_ref":"H1","clock":"🔥","threshold":"英國夜數連 4 季年減，或美國短租占用率低於 55%（2026 預估 57.4%）","evidence_refs":["supply_demand_durability#2","supply_demand_durability#1"]},{"id":"R7","text":"基礎設施單點：平台主要放在 AWS，資料與支付處理沒有完整備援，重大中斷會同時打到訂單與信任。","h_ref":"H2","clock":"🐢","threshold":"單次中斷超過 24 小時，或公司揭露中斷補償超過單季營收 1%","evidence_refs":["geo_supply_chain#0","geo_supply_chain#1"]}],"single_thing":{"description":"2027 年第三季財報（預計 2027 年 11 月公布）夜數年增低於 8%，也就是對上先訂後付高基期後，成長掉到單位數。","why_fatal":"現價 35.85 倍與共識兩年年化 18% 都假設雙位數成長延續。夜數掉到 8% 以下，市場可能用約 20 倍看 FY2027 每股盈餘 5.9 美元，約 118 美元，較現價 −37.9%。成長同時決定每股盈餘和倍數，是情境樹裡最大的單一敏感度。","if_happens":"持有者減碼至半倉，同季 App 夜數占比也下降則清倉；未持有者取消進場條件，重跑評估。","how_monitor":"每季股東信的夜數年增與先訂後付淨貢獻、法說揭露的取消率，從 2027 年 2 月財報起逐季對照。","probability":"約 30%（12～24 個月內）。依據是 Q2 扣先訂後付約 8%、Q3 約 13%，Q4 指引至少低雙位數，一年後對上高基期掉到 8% 以下並不難。"}},"appendix_a":{"growth_durability":7,"quality_score":8,"ai_risk":"🟡","long_term_confidence":"中","fpe_fy2":30.59,"peg_fy2":1.7,"stress":{"pass":1,"total":3}},"eps_meta":{"base_eps_path":{"FY2025A":null,"FY2026E":5.3,"FY2027E":6.21,"FY2028E":7.38},"fy_end_month":12,"eps_basis":"Koyfin 共識每股盈餘，會計年度 12 月底。FY2025A 留空：事實表的稀釋每股盈餘 1.03 美元與同年淨利 25.11 億美元對不起來（以目前 596.74 百萬股換算約 4.21 美元，僅供對照），疑似資料錯誤，需要從 10-K 補正，三年年化因此未計算。"},"catalysts":[{"date":"2027-02-15","date_precision":"month","type":"guidance","event":"2026 Q4 財報與 2027 全年展望","impact":"高","watch":"夜數年增是否 ≥10%、2027 年利潤率取向"},{"date":"2027-06-30","date_precision":"quarter","type":"product","event":"自家 AI 旅遊代理上線","impact":"高","watch":"App 夜數占比、通用代理訂單占比"},{"date":"2027-11-05","date_precision":"month","type":"other","event":"2027 Q3 財報，對上先訂後付高基期","impact":"高","watch":"夜數年增是否低於 8%"},{"date":null,"type":"regulatory","event":"歐盟住宅法案草案立法進度","impact":"中","watch":"會員國與議會表決、EMEA 夜數成長"}],"decision_out":{"role":"追蹤","row_hit":"8","pacing":[],"holding_cap":null,"audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='↑', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"輸入缺(momentum_overheated=null)，依保守方向處理：不視為觸發","input_gap":["momentum_overheated"]},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":true,"basis":"signal='B', runway='🟢', val='🟠', moat_trend='↑', week26=34.28, valuation_dependent=False"},{"row":"8a-QC48","condition":"row 8a 命中須經 QC-48 爆發候選 Bull 冷讀；critic 未放行（fail／not_run）→ 落 row 8","hit":true,"basis":"qc48_result='fail', 結論='Bull 路徑缺分部量價骨架，歷史實現報酬也不支持；而 runway 的 🟢 沒有滲透率數字，第二曲線只有管理層說法、沒有財報數字，所以這個 Bull 依據站不住。'"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position=None, moat='B', moat_trend='↑', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":true,"basis":"signal='B', val='🟠'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":false,"basis":"signal='B', val='🟠', ma='🟡'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟠', ma='🟡'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟠', ma='🟡'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"requires_critic":[],"verdict":"觀望"}}
```

---

## ⑤ 覆蓋面（程式判定，你回的 ⑤ 燈號會被覆寫）

燈號 🟢：核心軸皆有證據或不適用，非核心軸也沒有空軸。核心軸由採證 agent 自報不適用（燈號不變，請看 note 理由）：customer_concentration_credit。

⑤ 的 reason 只需評論：空軸的查詢詞是否切題、判斷有沒有交代缺口對結論的影響。

---

## 尾段：回覆格式

只回一個 JSON 陣列，①–⑧ 每條一個元素，八個全出，不得跳號、不得多列，陣列外不得有任何文字（不加前言、不加 markdown 圍欄、不加附註）：

```json
[{"item": "①", "light": "🔴|🟡|🟢", "judgment_path": "$.路徑", "reason": "一句話"}]
```
