你是 DD 管線 v20 的判斷層閘（gate），標的 QCOM（20261108）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（37 條）
- `f_kpi1_non_gaap`（q1_business）｜Non-GAAP 營收＝10442 USD M｜期間與口徑：Q4 FY2026（季末 2026-09-27，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q4 FY26 新聞稿（Form 8-K Ex.99.1，IR 稿全文）https://www.sec.gov/Archives/edgar/data/0000804328/000080432826000127/qcom092726erex991.htm（numbers.latest_quarter_kpis.items[1]，as_of Q4 FY2026（季末 2026-09-27，公告於 2026-11-04））
  - 註記：公司指引 9.7–10.5B 高端（共識數字未查）
- `f_kpi2_non_gaap`（q1_business）｜Non-GAAP 營業利益／利益率＝2769 USD M（利益率 26.5%，÷non-GAAP 營收 10,442）｜期間與口徑：Q4 FY2026（季末 2026-09-27，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q4 FY26 新聞稿（Form 8-K Ex.99.1，IR 稿全文）https://www.sec.gov/Archives/edgar/data/0000804328/000080432826000127/qcom092726erex991.htm（numbers.latest_quarter_kpis.items[2]，as_of Q4 FY2026（季末 2026-09-27，公告於 2026-11-04））
- `f_kpi3_gaap`（q1_business）｜GAAP 營業利益／利益率＝1356 USD M（利益率 13.1%）｜期間與口徑：Q4 FY2026（季末 2026-09-27，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q4 FY26 新聞稿（Form 8-K Ex.99.1，IR 稿全文）https://www.sec.gov/Archives/edgar/data/0000804328/000080432826000127/qcom092726erex991.htm（numbers.latest_quarter_kpis.items[3]，as_of Q4 FY2026（季末 2026-09-27，公告於 2026-11-04））
- `f_kpi6_qct`（q1_business）｜QCT 手機營收＝5137 USD M｜期間與口徑：Q4 FY2026（季末 2026-09-27，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q4 FY26 新聞稿（Form 8-K Ex.99.1，IR 稿全文）https://www.sec.gov/Archives/edgar/data/0000804328/000080432826000127/qcom092726erex991.htm（numbers.latest_quarter_kpis.items[6]，as_of Q4 FY2026（季末 2026-09-27，公告於 2026-11-04））
- `f_kpi7_qct`（q1_business）｜QCT 車用營收＝1990 USD M｜期間與口徑：Q4 FY2026（季末 2026-09-27，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q4 FY26 新聞稿（Form 8-K Ex.99.1，IR 稿全文）https://www.sec.gov/Archives/edgar/data/0000804328/000080432826000127/qcom092726erex991.htm（numbers.latest_quarter_kpis.items[7]，as_of Q4 FY2026（季末 2026-09-27，公告於 2026-11-04））
- `f_kpi8_qct_iot`（q1_business）｜QCT IoT 營收＝1888 USD M｜期間與口徑：Q4 FY2026（季末 2026-09-27，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q4 FY26 新聞稿（Form 8-K Ex.99.1，IR 稿全文）https://www.sec.gov/Archives/edgar/data/0000804328/000080432826000127/qcom092726erex991.htm（numbers.latest_quarter_kpis.items[8]，as_of Q4 FY2026（季末 2026-09-27，公告於 2026-11-04））
- `f_kpi9_qtl`（q1_business）｜QTL 授權營收＝1304 USD M｜期間與口徑：Q4 FY2026（季末 2026-09-27，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q4 FY26 新聞稿（Form 8-K Ex.99.1，IR 稿全文）https://www.sec.gov/Archives/edgar/data/0000804328/000080432826000127/qcom092726erex991.htm（numbers.latest_quarter_kpis.items[9]，as_of Q4 FY2026（季末 2026-09-27，公告於 2026-11-04））
- `f_kpi10_q1_fy2027`（q1_business）｜指引：Q1 FY2027＝— 營收 10.4–11.2B；QCT 9.0–9.6B；QTL 1.3–1.5B；GAAP EPS 1.03–1.23；non-GAAP EPS 2.15–2.35｜期間與口徑：Q4 FY2026（季末 2026-09-27，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司 Q4 FY26 新聞稿（Form 8-K Ex.99.1，IR 稿全文）https://www.sec.gov/Archives/edgar/data/0000804328/000080432826000127/qcom092726erex991.htm（numbers.latest_quarter_kpis.items[10]，as_of Q4 FY2026（季末 2026-09-27，公告於 2026-11-04））
- `f_kpi11_fy2027`（q1_business）｜指引：FY2027 全年定性＝— 非手機營收 YoY >60%；資料中心營收目標 5B；定價調整效益於 FY27 下半年反映在 QCT 毛利率｜期間與口徑：Q4 FY2026（季末 2026-09-27，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司 Q4 FY26 新聞稿（Form 8-K Ex.99.1，IR 稿全文）https://www.sec.gov/Archives/edgar/data/0000804328/000080432826000127/qcom092726erex991.htm（numbers.latest_quarter_kpis.items[11]，as_of Q4 FY2026（季末 2026-09-27，公告於 2026-11-04））
- `f_peer_qcom_gross_margin_pct`（q2_moat）｜QCOM 毛利率＝53.1 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.QCOM.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_qcom_operating_margin_pct`（q2_moat）｜QCOM 營業利益率＝20.08 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.QCOM.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_2454_tw_gross_margin_pct`（q2_moat）｜2454.TW 毛利率＝46.28 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.2454.TW.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_2454_tw_operating_margin_pct`（q2_moat）｜2454.TW 營業利益率＝15.13 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.2454.TW.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_avgo_operating_margin_pct`（q2_moat）｜AVGO 營業利益率＝48.52 %｜期間與口徑：TTM ending 2026-07-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.AVGO.operating_margin_pct，as_of TTM ending 2026-07-31（4季加總））
- `f_peer_nvda_operating_margin_pct`（q2_moat）｜NVDA 營業利益率＝65.21 %｜期間與口徑：TTM ending 2026-07-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.NVDA.operating_margin_pct，as_of TTM ending 2026-07-31（4季加總））
- `f_peer_nxpi_operating_margin_pct`（q2_moat）｜NXPI 營業利益率＝28.55 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.NXPI.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝10.16 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-11-07）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝12.85 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-11-07）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝17.84 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-11-07）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝45419.02 USD m｜期間與口徑：2026-11-08／yfinance revenue_estimate 0y 平均（25 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝52466.94 USD m｜期間與口徑：2026-11-08／yfinance revenue_estimate +1y 平均（29 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi4_q4`（q4_capital）｜自由現金流（Q4 單季，推算）＝1824 USD M｜期間與口徑：Q4 FY2026（季末 2026-09-27，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q4 FY26 新聞稿（Form 8-K Ex.99.1，IR 稿全文）https://www.sec.gov/Archives/edgar/data/0000804328/000080432826000127/qcom092726erex991.htm（稿內無單季現金流欄；Q4＝全年減前九個月，其中前九個月取自 Q3 稿 https://www.sec.gov/Archives/edgar/data/0000804328/000080432826000085/qcom062826erex991.htm；自行推算）（numbers.latest_quarter_kpis.items[4]，as_of Q4 FY2026（季末 2026-09-27，公告於 2026-11-04））
- `f_kpi5_sbc_non_gaap`（q4_capital）｜SBC 占 non-GAAP 營業利益＝31.5 %（SBC 873M ÷ 2,769M；占 GAAP 營收 8.5%）｜期間與口徑：Q4 FY2026（季末 2026-09-27，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q4 FY26 新聞稿（Form 8-K Ex.99.1，IR 稿全文）https://www.sec.gov/Archives/edgar/data/0000804328/000080432826000127/qcom092726erex991.htm（numbers.latest_quarter_kpis.items[5]，as_of Q4 FY2026（季末 2026-09-27，公告於 2026-11-04））
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝8311.0 USD m｜期間與口徑：2026-11-08／yfinance 最新一季：總債務 15992.0、現金 7681.0（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝2.189 %｜期間與口徑：2026-11-08／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-11-08）
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝1070.0 m shares｜期間與口徑：2026-11-08／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝165.41 USD｜期間與口徑：2026-11-06（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-11-06（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝16.28 x｜期間與口徑：2026-11-07／分母＝FY1 EPS 10.16，分子＝快照價 165.41｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-11-07）
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝13.02 x｜期間與口徑：2026-11-06（RTH 收盤，UTC）／4 個年度端點內的分位＝0.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-11-06（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝0.0 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝4.1 x｜期間與口徑：2026-11-06（RTH 收盤，UTC）／4 個年度端點內的分位＝58.8｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝4.3 x｜期間與口徑：2026-11-06（RTH 收盤，UTC）／4 個年度端點內的分位＝59.4｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝59.4 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ev_s_fwd`（q5_valuation）｜EV/S（EV ÷ FY1 共識營收）＝4.08 x｜期間與口徑：2026-11-08／f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）｜kind：estimate
  - 來源：—（numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝-3.51 %｜期間與口徑：2026-08-13 → 2026-11-07／FY1 共識 EPS 10.53 → 10.16（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-11-07）
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝-23.81 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-11-06（RTH 收盤，UTC））
- `f_rsi14`（q5_valuation）｜RSI(14)＝44.31｜期間與口徑：2026-11-06（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-11-06（RTH 收盤，UTC））

### findings_digest 中方向為負或來源衝突的條目（22 條）
- `competitive_share_entrants#0`（competitive_share_entrants｜方向 -｜狀態 ok）：Counterpoint：Qualcomm 智慧手機晶片出貨份額 Q1 2026 為 23%，較 2025Q1 的 27% 下滑；MediaTek 32%（前年 38%），Apple 19%（前年 15%）。
  - 來源：Counterpoint Research 數據，經 Malaysian Wireless 報導 (MediaTek leads smartphone chipset market Q1 2026)（as_of 2026-06-01）｜affects：moat_trend、thesis.R
- `competitive_share_entrants#1`（competitive_share_entrants｜方向 -｜狀態 ok）：Apple 自研 C1 數據機已上市，Reuters 報導 Qualcomm 在 Apple 數據機的份額預期從 100% 降至最低約 20%。
  - 來源：Reuters 經 Telecoms Tech News (iPhone C1 modem chip to cut Apple's Qualcomm reliance by 80%)（as_of 2026-01-01）｜affects：moat_trend、decision_inputs.bear
- `customer_second_source#0`（customer_second_source｜方向 -｜狀態 ok）：10-K 風險因子：Apple 歷來為 QCOM 最大客戶之一，但公司預期 Apple 今後將主要使用自家內部開發的 modem，而非 QCOM 產品。
  - 來源：SEC EDGAR QCOM 10-K FY2026 Item 1A（as_of 2026-11-04）｜affects：moat_trend、thesis.R、decision_inputs.bear
- `customer_second_source#1`（customer_second_source｜方向 -｜狀態 ok）：10-K：部分最大客戶過去、現在及未來可能使用競爭對手晶片，且已開發或正開發自家積體電路產品（實質成為競爭者）；中國客戶亦有自研或改用競品。
  - 來源：SEC EDGAR QCOM 10-K FY2026 Item 1A（as_of 2026-11-04）｜affects：moat_trend、thesis.R、decision_inputs.bear
- `customer_concentration_credit#0`（customer_concentration_credit｜方向 -｜狀態 ok）：FY2026 10-K：Apple 與 Samsung 各占合併營收 10% 以上；少數客戶/授權對象歷來占營收大部分。
  - 來源：SEC EDGAR 10-K FY2026 Item 1 Business（as_of 2026-11-04）｜affects：decision_inputs.bear、thesis.R
- `customer_concentration_credit#1`（customer_concentration_credit｜方向 -｜狀態 ok）：10-K 風險因子：公司預期 Apple 未來主要使用自研數據機，對 QCT 營收、損益與現金流有重大負面影響；Samsung、小米亦自研晶片。
  - 來源：SEC EDGAR 10-K FY2026 Item 1A（as_of 2026-11-04）｜affects：moat_trend、decision_inputs.bear、thesis.R
- `supply_demand_durability#0`（supply_demand_durability｜方向 -｜狀態 ok）：Counterpoint 預測 2026 智慧型手機出貨 −13.9% 至 10.8 億支、史上最大年減，復甦要到 2027 年底新增記憶體產能上線；IDC 預測 −12.9%。
  - 來源：Counterpoint／IDC（經 thestar.com.my、91mobiles 等轉載）（as_of 2026-09-16）｜affects：decision_inputs.bear、thesis.R
- `supply_demand_durability#1`（supply_demand_durability｜方向 -｜狀態 ok）：三星稱 2027 年供需缺口可能比 2026 更大；SK hynix 預期記憶體緊缺 2027 見頂、延續至 2030；新產能多自 2028 起（來源含轉載，數字不一）。
  - 來源：Tom's Hardware／PhoneArena 報導 Samsung、SK hynix 說法（as_of 2026-06-03）｜affects：decision_inputs.bear、thesis.R
- `supply_demand_durability#2`（supply_demand_durability｜方向 -｜狀態 ok）：高通 FY26 Q1 財報（2026-02）：Q2 營收指引 102–110 億美元低於共識；管理層指記憶體短缺與漲價將影響手機市場整個財年，並可能延到 2027；中國 OEM 削減機型生產與通路庫存。
  - 來源：Qualcomm FY26 Q1 業績（經 The Star／Yahoo Finance 報導）（as_of 2026-02-05）｜affects：thesis.R、valuation、decision_inputs.bear
- `regulatory_antitrust#0`（regulatory_antitrust｜方向 -｜狀態 ok）：QCOM 10-K FY2026 風險因素：公司過去及目前仍受多項政府調查／法律程序，不利結果可能導致降低權利金率、授權晶片商、修改商業做法等補救，且單一國家的處分效力可能延伸至境外。
  - 來源：SEC EDGAR 10-K FY2026 Item 1A Risk Factors（as_of 2026-11-04）｜affects：decision_inputs.bear、thesis.R
- `regulatory_antitrust#1`（regulatory_antitrust｜方向 -｜狀態 ok）：10-K 載明專利授權做法的調查或訴訟可能迫使公司未來改變授權做法。
  - 來源：SEC EDGAR 10-K FY2026 Item 1 Business（as_of 2026-11-04）｜affects：moat_trend、thesis.R
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：QCOM 10-K FY2026 風險因素：美中貿易保護與實體清單等政策已經、目前並可能限制或阻止與中國客戶／供應商交易；因對中國營收集中，進一步限制或中國關稅可能對業務、營運結果、現金流造成重大損害。
  - 來源：SEC EDGAR 10-K FY2026 Item 1A（as_of 2026-11-04）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#1`（reg_tariff_export｜方向 -｜狀態 ok）：10-K MD&A：公司持續監控關稅，影響取決於不確定的後續發展，可能衝擊需求、定價與成本，並導致呆滯庫存或準備金認列。
  - 來源：SEC EDGAR 10-K FY2026 Item 7 MD&A（as_of 2026-11-04）｜affects：thesis.R、valuation
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：FY2026 10-K 風險因素：關鍵晶圓代工與封測夥伴集中在台灣與韓國，RF 製造在中國、德國、新加坡；中台嚴重或長期衝突可能切斷台灣晶片供應，對業務有重大不利影響（依搜尋摘要轉述，未核全文）
  - 來源：SEC EDGAR QUALCOMM Form 10-K FY2026（as_of 2026-11-04）｜affects：decision_inputs.bear、thesis.R
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：FY2025 中國占營收 46%（依客戶總部，Nikkei 經 TrendForce 轉述）；Qualcomm 10-Q 載明美國撤銷對華為出口許可，不再預期華為產品營收，並提及中國資本流動規則可能延遲客戶付款
  - 來源：TrendForce News 2026-06-25 / SEC 10-Q 2026-06-28（as_of 2026-06-25）｜affects：decision_inputs.bear、thesis.R
- `end_markets#0`（end_markets｜方向 -｜狀態 ok）：FY2026 Q4（季末2026-09-27）手機營收約$5.137B、年減26%；車用$1.99B（年增89%）；IoT$1.888B（年增4%）；車用＋IoT合計年增36%。來源為搜尋摘要彙整，未逐字核對
  - 來源：xenospectrum / 247wallst 搜尋摘要（as_of 2026-11-05）｜affects：thesis.R、decision_inputs.bear
- `end_markets#1`（end_markets｜方向 -｜狀態 ok）：2026年7月：CEO稱Apple相關營收自FY Q4起下滑，下一代iPhone的高通份額遠低於先前估計的20%；專利授權至少收到2027年3月
  - 來源：iClarified / MacRumors 報導（as_of 2026-07-30）｜affects：moat_trend、thesis.R、decision_inputs.bear
- `end_markets#3`（end_markets｜方向 -｜狀態 ok）：FY2026 Q4分部營收：手機$5.137B、車用$1.99B、IoT$1.888B
  - 來源：Qualcomm 10-K FY2026（as_of 2026-11-05）｜affects：thesis.R
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：10-K 稱 QCT 面臨客戶內部自研產品的競爭（含最大客戶），並將客戶垂直整合列為風險因子；也與替代通訊技術競爭。
  - 來源：SEC EDGAR 10-K FY2026 Item 1 Business（as_of 2026-11-04）｜affects：moat_trend、decision_inputs.bear
- `substitute_technology#1`（substitute_technology｜方向 -｜狀態 ok）：10-K 風險因子列出「客戶垂直整合（自行開發積體電路產品）可能損害半導體業務」。
  - 來源：SEC EDGAR 10-K FY2026 Item 1 Business（as_of 2026-11-04）｜affects：moat_trend、thesis.R
- `substitute_technology#2`（substitute_technology｜方向 -｜狀態 ok）：Apple 自研 C1 系列數據機已用於 iPhone 16e、iPhone Air、iPad Pro，取代高通晶片；高通稱非 Apple QCT 營收成長 18%。
  - 來源：MacRumors: Qualcomm Now Relies on Android as Apple Modems Roll Out（as_of 2025-11-06）｜affects：moat_trend、thesis.R
- `capital_markets_pricing#1`（capital_markets_pricing｜方向 -｜狀態 ok）：二手報導：財報後盤後股價跌約 6%，因手機晶片營收年減 26%（記憶體成本壓力）、前瞻指引偏弱；單一來源未證實。分析師共識與此指引的落差數字本次搜尋未查到。
  - 來源：AI Weekly: Qualcomm Q4 Revenue Drops 8% to $10.3B, Guides $5B Data-Center Revenue in Fiscal 2027（as_of 2026-11-05）｜affects：valuation、decision_inputs.bear

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 6 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/QCOM_20261108/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":432.0,"bear_5y_price":115.5,"p_bull_pct":22,"p_bear_pct":32,"upside_5y_pct":67.8,"ev5y_pct":57.0,"irr_base_pct":10.9,"asym_ratio":3.7,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":10.16,"pe":16.28,"basis":"FY27 共識 EPS（進行中財年，非 GAAP 口徑），終端倍數同以當年 EPS 為分母。"},"eps":{"bull":[10.4,13.4,18.2,21.2,24.0],"base":[9.85,12.0,15.0,16.8,18.5],"bear":[9.0,9.2,9.6,10.0,10.5]},"pe":{"bull":18,"base":15,"bear":11},"p":{"bull":22,"base":46,"bear":32},"yield_pct":{"dividend":2.189,"net_buyback":0},"second_stage":{"bull_cagr_pct":12,"base_cagr_pct":8},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### QCOM_Q3_2026_Earnings_Call_20260729.md
- 2026-07-29｜CFO｜guidance：CFO 給 FQ4 總營收與非GAAP EPS 財測區間（原話："We are forecasting revenues of $9.7 billion to $10.5 billion"）
- 2026-07-29｜CFO｜guidance：FQ4 QCT 營收與 EBT margin 財測（原話："In QCT, we expect revenues of $8.4 billion to $9 billion and"）
- 2026-07-29｜CFO｜guidance：FQ4 QTL 營收與 EBT margin 財測（原話："In QTL, we estimate revenues of $1.2 billion to $1.4"）
- 2026-07-29｜CFO｜guidance：FQ4 非GAAP 營業費用財測，含 Modular 併入與資料中心投資（原話："we anticipate non-GAAP operating expenses to be"）
- 2026-07-29｜CFO｜guidance：FQ4 車用預期年增約 60%（原話："In QCT automotive, we expect another record quarter with"）
- 2026-07-29｜CFO｜guidance：FQ1 不正式給財測，但定性說 QCT 營收季增小幅，Apple 約減半（原話："we expect it to be slightly up on a sequential basis."）
- 2026-07-29｜CFO｜guidance：FQ1 Apple 營收預期自 9 月季到 12 月季下滑約 50%（原話："we are forecasting approximately 50% decline from September"）
- 2026-07-29｜CFO｜guidance：季節性改變：預期 12 月季到 3 月季營收成長（原話："So we actually expect revenues to grow when we go from the"）
- 2026-07-29｜CFO｜guidance：FY27 非手機營收成長率由 FY26 的 24% 加速至逾 60%（原話："accelerate from 24% in fiscal '26 to greater than 60% in"）
- 2026-07-29｜CFO｜guidance：FY27 手機市場預期年減低十位數，Android 營收年減 20%、EPS 影響逾 1.5 美元（原話："the market will be down low teens relative to '25 to '26."）
- 2026-07-29｜CEO｜guidance：FY27 預期整體營收成長（原話："we expect top line growth for Qualcomm in fiscal '27"）
- 2026-07-29｜CFO｜guidance：FY27 與 FY29 資料中心營收目標及非手機占 QCT 比重（原話："data center revenue growth to $5 billion in fiscal '27 and"）
- 2026-07-29｜CEO｜guidance：車用年化營收出場速率目標由 60 億上調至約 70 億美元（原話："now expect annualized sales of approximately $7 billion"）
- 2026-07-29｜CFO｜guidance：OpEx 走勢：無變動，成長主要來自資料中心投資（原話："no change to the guidance we provided at Investor Day."）
- 2026-07-29｜CFO｜margin：管理層拆解 QCT 毛利率壓力的兩個成因之一：高階產品組合偏弱（原話："the first is a little bit of a weaker mix within premium"）
- 2026-07-29｜CFO｜margin：毛利率壓力第二個成因為供應鏈投入成本上升，漲價將在未來幾季反映（原話："we expect this benefit to show up in our gross margins over"）
- 2026-07-29｜CEO｜margin：CEO 稱 QCT 毛利率短期略低於歷史區間（原話："QCT gross margins, which will be slightly below our"）
- 2026-07-29｜CFO｜margin：基線毛利率區間 48%-50%；資料中心初期以客製晶片為主，對 QCT 加權毛利率拖累 1.5-2 個百分點（原話："that will be a drag of 1.5% to 2% on the weighted average"）
- 2026-07-29｜CFO｜margin：漲價幅度為雙位數，涵蓋多個終端市場，受合約與產品週期影響逐步生效（原話："the scale of the increase that we're looking at is double"）
- 2026-07-29｜CFO｜margin：QTL 版稅有 ASP 上限，價格在上限以下上漲才有部分受惠（原話："there is a cap on the total royalties based on the device"）
- 2026-07-29｜CFO｜competition：管理層稱漲價與同業一致（原話："it's no different than what a lot of the peers in our"）
- 2026-07-29｜CEO｜competition：三星旗艦機約 70% 採用 Snapdragon（原話："Snapdragon powering approximately 70% of their"）
- 2026-07-29｜CFO｜risk：Apple 敘事變化：因供應限制，新機份額預期遠低於先前估的 20%，Apple 營收下滑提前（原話："materially lower than our prior estimate of 20%."）
- 2026-07-29｜CFO｜customer：FY27 Apple 產品營收將低於先前指引的略高於 20 億美元（原話："less than the previous guidance we had given, which was a"）
- 2026-07-29｜CEO｜risk：記憶體價格與投入成本、供應短缺造成手機及消費電子營收下滑（原話："the entire industry continues to be impacted by"）
- 2026-07-29｜CEO｜risk：CEO 承認投資人想看資料中心執行的更多證明（原話："investors want to see more proof points that we can"）
- 2026-07-29｜CEO｜risk：供應鏈全面滿載，CEO 稱有供應執行計畫但沒人真正寬裕（原話："Everything is at 100% utilization, everything."）
- 2026-07-29｜CEO｜risk：美中限制：目前客戶合作不受限（原話："For the engagements we have today, we're not restricted."）
- 2026-07-29｜CFO｜customer：中國 OEM 營收預期 FQ3 為底部，FQ4 回到雙位數季增（原話："reached a bottom in the third fiscal quarter and will return"）
- 2026-07-29｜CFO｜customer：中國 OEM 先前消化通路庫存，現通路庫存已薄，營收回歸市場實際規模（原話："the channel inventory has thinned down that they can't draw"）
- 2026-07-29｜CEO｜customer：與 BMW 簽署擴大協議，成為次世代 ADAS 與數位座艙主要算力矽供應商（原話："lead compute silicon provider for their next-generation ADAS"）
- 2026-07-29｜CEO｜customer：車廠由逐 socket 設計贏單轉向多世代平台合作（原話："Customers are shifting from socket-by-socket design awards"）
- 2026-07-29｜CFO｜customer：兩個客製晶片客戶皆為全球級超大規模雲端業者，已有 PO 並開始投片（原話："we do have POs from these engagements, and so we've already"）
- 2026-07-29｜CEO｜product：HBC Gen 1 已完成 tape-out，首款 HBC 方案預計 2027 年中推出（原話："we have completed the tape-out of HBC Gen 1"）
- 2026-07-29｜CEO｜product：資料中心產品線時程：連接 FY26、客製矽與 AI 加速器 FY27、伺服器 CPU FY28（原話："custom silicon and AI accelerators in fiscal '27 and"）
- 2026-07-29｜CEO｜product：完成收購 Modular，強化資料中心與邊緣 AI 軟體堆疊（原話："we have closed our acquisition of Modular Inc., and"）
- 2026-07-29｜CEO｜product：CEO 稱 HBC 與 CPU 客戶想先看到矽片，晶片實測是下一個里程碑（原話："we needed to see silicon and see how it performs before we"）
- 2026-07-29｜CFO｜product：FQ3 車用營收 16 億美元、年增 61%；非手機 QCT 年增 28%（原話："record quarter with revenues of $1.6 billion, with 61% year-"）
- 2026-07-29｜CEO｜product：工業設計贏單管線逾 70 億美元，本財年已取得逾 35 億美元（原話："our industrial design win pipeline exceeds $7 billion with"）
- 2026-07-29｜CFO｜capital_allocation：FQ3 資本回饋 23 億美元（買回 14 億、股利 9.73 億）（原話："we returned $2.3 billion to stockholders"）
- 2026-07-29｜CFO｜capital_allocation：OpEx 規模納入 Alphawave 與 Modular 收購並持續投資資料中心（原話："it will reflect both obviously Alphawave and now Modular in"）
- 2026-07-29｜CEO｜commitment：CEO 承諾漲價生效後毛利率回到營運模型（原話："as they take effect, we expect to see gross margins realign"）
- 2026-07-29｜CEO｜commitment：兩個近期客製矽案於 12 月季開始貢獻營收（原話："Our 2 near-term custom silicon wins will be revenue"）
- 2026-07-29｜CFO｜commitment：FY27 非手機成長預期取代 FY26 全部 Apple 產品營收（原話："We expect this growth from non-handset revenues in fiscal"）
- 2026-07-29｜CEO｜commitment：FY29 非手機營收目標由 220 億上調至 400 億美元（原話："bringing our total non-handset revenue outlook to $40"）

### QCOM_Analyst_Investor_Day_QUALCOMM_Incorporated_20260624.md
- 2026-06-24｜Akash Palkhiwala (CFO)｜guidance：CFO 給資料中心 FY27 營收目標 50 億美元。（原話："We're targeting $5 billion of revenue in fiscal '27."）
- 2026-06-24｜Akash Palkhiwala (CFO)｜guidance：CFO 給資料中心 FY29 營收目標 150 億美元。（原話："We are targeting $15 billion of revenue in data center"）
- 2026-06-24｜Akash Palkhiwala (CFO)｜guidance：CFO 把 FY29 非手機營收目標由 18 個月前的 220 億上調為 400 億美元。（原話："Our fiscal '29 revenue target is now $40 billion."）
- 2026-06-24｜Akash Palkhiwala (CFO)｜guidance：CFO 給 FY29 EPS 目標高於 18 美元。（原話："Our EPS target is of greater than $18"）
- 2026-06-24｜Akash Palkhiwala (CFO)｜guidance：CFO 說長期有機會把營收規模拉到 1000 億美元。（原話："our revenue to $100 billion"）
- 2026-06-24｜Akash Palkhiwala (CFO)｜guidance：CFO 給車用 FY29 營收目標 100 億美元，並說這是第二次把進度再提前兩年。（原話："We will hit $10 billion of revenue in fiscal '29."）
- 2026-06-24｜Akash Palkhiwala (CFO)｜guidance：CFO 給個人 AI 與運算（PC 等）加工業網通與機器人合計 IoT 目標。（原話："We're going to be over $14 billion across these markets"）
- 2026-06-24｜Akash Palkhiwala (CFO)｜guidance：CFO 給工業網通與機器人 FY29 營收目標 80 億美元。（原話："We are targeting $8 billion in '29 for this business"）
- 2026-06-24｜Akash Palkhiwala (CFO)｜guidance：CFO 預期安卓手機營收溫和成長 5%，並列出前提是記憶體環境不大變、也不含 agentic AI 帶來的升級。（原話："This assumes that the current memory environment"）
- 2026-06-24｜Akash Palkhiwala (CFO)｜guidance：CFO 說 FY29 手機占營收約三分之一（FY27 低於一半）。（原話："handset will be 1/3 of our revenues in '29"）
- 2026-06-24｜Akash Palkhiwala (CFO)｜guidance：CFO 說資料中心長期可及市場約 1 兆美元，目標 5 到 7 年內市占率超過 5%。（原話："we are targeting greater than 5% share in 5 to 7 years"）
- 2026-06-24｜Nakul Duggal｜guidance：車用業務主管說 FY26 結束時年化營收達 60 億美元。（原話："We will exit FY '26 at $6 billion in annualized revenue"）
- 2026-06-24｜Akash Palkhiwala (CFO)｜guidance：CFO 對資料中心 FY27 內容的拆解：兩家超大型雲端客戶各自超過 10 億美元，客製化晶片占最大宗。（原話："who will each be greater than $1 billion"）
- 2026-06-24｜Akash Palkhiwala (CFO)｜guidance：CFO 在簡報中對同一批兩家超大型客戶的 FY27 貢獻說法（年內至少 10 億）。（原話："2 hyperscaler customers that are at global scale"）
- 2026-06-24｜Akash Palkhiwala (CFO)｜margin：CFO 說 QCT（含資料中心）長期營業利益率目標 30%，與先前目標不變。（原話："to be at 30% in the long term"）
- 2026-06-24｜Akash Palkhiwala (CFO)｜margin：CFO 說 QTL 營業利益率維持 70%。（原話："expect QTL to continue to be at 70%"）
- 2026-06-24｜Akash Palkhiwala (CFO)｜margin：CFO 說客製化晶片毛利率會略低於公司整體毛利率。（原話："custom silicon gross margin to be slightly below our"）
- 2026-06-24｜Akash Palkhiwala (CFO)｜margin：CFO 說客製化晶片在營業利益率層級是加分的。（原話："be accretive at the operating margin level"）
- 2026-06-24｜Akash Palkhiwala (CFO)｜margin：CFO 說過去五年營運費用占營收比由 31% 降到 23%。（原話："OpEx as a percent of revenue came down from 31% to 23%"）
- 2026-06-24｜Akash Palkhiwala (CFO)｜margin：CFO 預期營運費用占營收比進一步降到 19% 至 20%。（原話："we expect that to decline further to 19% to 20%"）
- 2026-06-24｜Antonios Pialis｜commitment：資料中心負責人承諾 FY27 起交出數十億美元營收。（原話："we will deliver multiple billions of revenue starting fiscal"）
- 2026-06-24｜Antonios Pialis｜commitment：資料中心負責人宣布贏得兩家超大型雲端客製化晶片案，年底起貢獻營收。（原話："hyperscaler deals that will contribute meaningful revenue"）
- 2026-06-24｜Nakul Duggal｜commitment：車用業務主管表示不打算讓連續兩位數成長中斷。（原話："We don't expect to let you down anytime"）
- 2026-06-24｜Akash Palkhiwala (CFO)｜commitment：CFO 說營收與 EPS 成長速度會比先前告訴投資人的快。（原話："going to grow much faster than what we had told you before"）
- 2026-06-24｜Akash Palkhiwala (CFO)｜capital_allocation：CFO 說資本配置策略不變。（原話："Our capital allocation strategy really is unchanged."）
- 2026-06-24｜Akash Palkhiwala (CFO)｜capital_allocation：CFO 說股息會以中低個位數幅度持續調升。（原話："We're going to keep increasing dividends in mid- to"）
- 2026-06-24｜Akash Palkhiwala (CFO)｜capital_allocation：CFO 說大部分自由現金流會還給股東。（原話："we'll return most of our free cash flow to shareholders"）
- 2026-06-24｜Akash Palkhiwala (CFO)｜capital_allocation：CFO 說過去十年已註銷 30% 股數。（原話："Over the last 10 years, we've retired 30% of our shares"）
- 2026-06-24｜Akash Palkhiwala (CFO)｜capital_allocation：CFO 說過去五年完成 35 筆併購。（原話："we've done 35 acquisitions over the last 5 years"）
- 2026-06-24｜Mark Zuckerberg｜customer：Meta CEO 宣布與高通簽訂多世代合作，由高通供應資料中心 CPU。（原話："we've entered a multigenerational collaboration"）
- 2026-06-24｜Satya Nadella｜customer：微軟 CEO 表示對高通的資料中心高頻寬運算（HBC）創新感到期待。（原話："we are excited about your innovation in the data center"）
- 2026-06-24｜Antonios Pialis｜customer：高通介紹 HUMAIN 為其第一個資料中心客戶。（原話："our first data center customer"）
- 2026-06-24｜Antonios Pialis｜customer：資料中心負責人說連接晶片產品今年通過第一家主要超大型雲端客戶認證。（原話："we are qualified in our first leading major hyperscaler"）
- 2026-06-24｜Akash Palkhiwala (CFO)｜customer：CFO 說資料中心營收來源並不集中。（原話："This is not a concentrated revenue stream."）
- 2026-06-24｜Nakul Duggal｜customer：車用業務主管說車用設計案儲備金額 650 億美元。（原話："We have built a $65 billion design win pipeline."）
- 2026-06-24｜Nakul Duggal｜customer：車用業務主管說 ADAS 客戶已達 25 家車廠。（原話："We are now at 25 OEMs."）
- 2026-06-24｜Cristiano Amon｜customer：CEO 說在中國每家做 agent 的基礎模型公司也成了客戶，傳統手機客戶界線模糊。（原話："I don't know who the mobile customers"）
- 2026-06-24｜Antonios Pialis｜product：資料中心負責人給出第一個 HBC 產品（AI250）上市時點。（原話："of our first HBC product in the middle of 2027"）
- 2026-06-24｜Antonios Pialis｜product：資料中心負責人給出 Oryon 伺服器級 CPU 推出時點（2028 年中）。（原話："the industry's first Oryon server class compute solution"）
- 2026-06-24｜Antonios Pialis｜product：資料中心負責人說 2027 年推出第三代 AI 加速器。（原話："Then in 2027, we are launching our third generation"）
- 2026-06-24｜Antonios Pialis｜product：資料中心負責人引述 C1000 CPU 時脈高於 5GHz、比競品快 30% 以上。（原話："30% faster than any of the competition"）
- 2026-06-24｜Antonios Pialis｜product：資料中心負責人引述 HBC 每瓦頻寬相對 HBM 方案的倍數。（原話："With HBC, we deliver 6x the bandwidth per watt versus"）
- 2026-06-24｜Cristiano Amon｜product：CEO 回顧資料中心營收時點從 FY28 逐步提前到 FY27、FY26 的說法。（原話："we get more traction, we move it to fiscal '27"）
- 2026-06-24｜Akash Palkhiwala (CFO)｜product：CFO 描述公司定位轉變：從裝置公司變成雲端加裝置公司。（原話："being a devices company to being a cloud and device company"）
- 2026-06-24｜Cristiano Amon｜competition：CEO 回應「進資料中心是否太晚」。（原話："Never too late for Qualcomm."）
- 2026-06-24｜Cristiano Amon｜competition：CEO 說推論市場的護城河不如訓練市場強。（原話："not as strong as it has been for training"）
- 2026-06-24｜Tim Davis｜competition：Modular 共同創辦人把自家軟體定位為 NVIDIA 軟體堆疊的可攜替代方案。（原話："NVIDIA's software stack designed from day 1"）
- 2026-06-24｜Cristiano Amon｜risk：CEO 說手機市場正面對記憶體供應狀況的不確定性。（原話："uncertainty of the memory situation"）
- 2026-06-24｜Cristiano Amon｜risk：CEO 說 FY27 的 50 億美元已鎖定產能。（原話："For that revenue, we have secured capacity as well"）
- 2026-06-24｜Cristiano Amon｜risk：CEO 說 FY27 的 50 億美元已備妥晶圓與記憶體。（原話："we have wafers and we have memory"）

### 問答異常語氣（迴避／改口／保留）
- QCOM_Q3_2026_Earnings_Call_20260729.md｜問：Rasgon 問是否刻意「餓死」Apple、把矽片轉供他處｜答法：CFO 否認該說法，歸因部分為供應限制、部分為與 Apple 討論結果，未量化份額（只說「materially less than 20%」），亦未給確切 FY27 Apple 金額
- QCOM_Q3_2026_Earnings_Call_20260729.md｜問：Reitzes 問資料中心除兩客戶外是否有更多客戶、管線如何擴張｜答法：CEO 未直接確認第三家客戶，改談現有客戶線路與「客戶要先看到矽片」的里程碑
- QCOM_Q3_2026_Earnings_Call_20260729.md｜問：Cardoso 問漲價幅度及在需求已受壓的手機市場如何推行｜答法：CFO 只給「雙位數」不拆各市場；CEO 補充以記憶體 BOM 比較，稱不預期高階量有根本改變
- QCOM_Q3_2026_Earnings_Call_20260729.md｜問：Buchalter 問毛利率回到先前水準的時間點｜答法：CFO 只說「未來幾季」、逐步因合約與產品週期，不給具體時點或數字
- QCOM_Analyst_Investor_Day_QUALCOMM_Incorporated_20260624.md｜問：Goldman Sachs 的 Jim Schneider 問 FY27 的 50 億美元是否都已有訂單、以及用現有客戶能否達成 FY29 目標。｜答法：CFO 回答「high confidence in our forecast, and so I'll leave it at that」，未回答訂單是否涵蓋，也未回答現有客戶能否達成 FY29；資料中心負責人補充「幾個吉瓦可達 FY29 數字」，同樣沒給客戶或訂單數字。
- QCOM_Analyst_Investor_Day_QUALCOMM_Incorporated_20260624.md｜問：Wolfe 的 Chris Caso 問 FY27 指引內含哪些產品，以及兩家客戶是不是已公布的 HUMAIN 與微軟。｜答法：CFO 說明產品組合（客製化晶片最大、AI 加速器年底、連接產品），並說兩家客戶是超大型雲端、HUMAIN 是連接產品的重要部分；未直接確認或否認兩家客戶是否為微軟，也未點名。

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 3 | 2 |
| customer_second_source | found | 2 | 0 |
| customer_concentration_credit | found | 3 | 1 |
| supply_demand_durability | found | 5 | 4 |
| regulatory_antitrust | found | 3 | 2 |
| reg_tariff_export | found | 4 | 2 |
| geo_supply_chain | found | 2 | 2 |
| end_markets | found | 5 | 3 |
| substitute_technology | found | 3 | 2 |
| channel_business_model_shift | found | 2 | 3 |
| capital_markets_pricing | found | 4 | 3 |
| major_events | found | 2 | 5 |

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260730","verdict":"進場","role":"衛星","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"非手機引擎（Auto ＋ IoT ＋ 資料中心）FY27 營收成長 &gt; 60% 至約 $210 億，完整取代 FY26 約 $72 億的 Apple 產品營收；FY29 達 $400 億、佔 QCT 約三分之二。"},{"id":"H2","text":"雙位數漲價落地後 QCT 毛利率回到 48-50% 歷史區間，且資料中心客製矽（毛利率約 35%）對加權毛利率的 1.5-2pp 拖累不使其結構性掉出區間。—— 這是本報告新增的假設，取代上一份報告的 H2（QTL 維持），因為法說揭露的毛利率結構問題已經超越授權風險成為第一順位。"},{"id":"H3","text":"QTL 維持約 $54-56 億／年、EBT 率 ≥ 68%，不被裝置 ASP 上限、OEM 拒付、監管處置或華為未續約結構性壓縮。"}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"資料中心從「已下 PO 的兩個客製矽案子」擴不出去：HBC 加速器與 Dragonfly C1000 拿不到商品矽插槽，$50 億（FY27）→ $150 億（FY29）的斜坡斷在第一階。結構原因有三個且互相獨立：① Arm 自製 AGI CPU 已於 2026-03 出貨、Meta 首發、FY27-28 需求逾 $20 億，而 C1000 要 2028 才上市（晚兩年、且付 Arm 授權金）；② hyperscaler 客製矽是多源策略，Broadcom／Marvell／聯發科都在同一張桌上；③ Cristiano 自己說「很多客戶要看到矽才決定」——也就是說目前的 pipeline 大部分還沒轉單。"},{"id":"R2","text":"QCT 毛利率結構性下移：漲價落地慢於組合稀釋，QCT 從 48-50% 的新常態變成 45-47%。四季軌跡已經在走：分部 EBT 率 31%（Q1 FY26）→ 27%（Q2）→ 26%（Q3）→ 指引 23-25%（Q4）。三個壓力來源疊加：台積 &lt;5nm 節點 2026 起漲價 5-10%（2nm 單片 &gt;$30,000、較前代 ＋50%）、OSAT 封測附加費 8-20%、資料中心客製矽稀釋 1.5-2pp。而 premium tier 內部降階（OEM 為了消化記憶體成本改用前代或較低階晶片）是需求側的自主降級——漲價治不了它。"},{"id":"R3","text":"QTL 的三重慢性壓縮同時發作：裝置 ASP 上限使記憶體驅動的手機漲價完全不入袋（Akash 明講上限以上「沒有差別」）＋ 華為授權到期未續且談判無果 ＋ 中國 SAMR 裁決附帶授權行為救濟。QTL 是全公司唯一的 69-72% EBT 率年金，它每流失 $1 都是接近純利。"}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"starter 1/3·帽 3%·加碼＝QCT 毛利率回 48%＋（Q1 FY27 法說）或資料中心單季營收 ≥ $1.0B","irr_base_pct":14.4,"ev5y_pct":76.7,"drift_watch_prior":{"dca_verdict":"進場","dca_role":"衛星","signal":"B","val":"🟡","ma":"🟠","trap":"🟡","moat_trend":"→","runway_post_y5":"🟢","asym_ratio":6.0,"ev5y_pct":76.7,"irr_base_pct":14.4,"max_dd_pct":-45.0,"bull_5y_price":387.0,"bear_5y_price":100.0,"p_bull_pct":22.0,"p_bear_pct":32.0,"rearm_trigger":"starter 1/3·帽 3%·加碼＝QCT 毛利率回 48%＋（Q1 FY27 法說）或資料中心單季營收 ≥ $1.0B","price_at_dd":148.4,"archetype":"品質複利成長","cycle_position":"早循環"}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"QCOM","date":"2026-11-08","schema":"v15.0","contract":"v19","company_name":"QUALCOMM Incorporated"},"oneliner":"授權續約解除最大不確定，車用超標，但手機仍在縮、毛利未修復，資料中心 50 億美元集中在兩家客戶；現價 16 倍看的是非 GAAP 盈餘，先等 3 月季資料中心實績再動手。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/QCOM_20261108/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/QCOM_20261108/scenario.json","answers":{"q1_business":{"verdict":"賺兩種錢：賣晶片給手機、車廠與裝置廠，以及向手機廠收專利授權金。最厚的利潤卡在授權這一節（單季營收約 13 億美元、EBT 率 70%），但未來三年的盈餘要靠資料中心與車用補上 Apple 晶片退場的缺口。","reasoning":"Q4 FY26 非 GAAP 營收 104.4 億美元：手機 51.4 億（49%）、車用 19.9 億（19%）、IoT 18.9 億（18%）、授權 13.0 億（12%），比例為自行計算。非 GAAP 營益率 26.5%，GAAP 只有 13.1%，TTM 毛利率 53.1%。FY27 公司預期非手機 QCT 營收年增逾 60%、占 QCT 逾一半。單點依賴有兩個：Apple 與三星各占合併營收 10% 以上，其中 Apple 晶片正在退場；資料中心 FY27 的 50 億美元大部分來自兩家超大型雲端客戶。供需判斷：手機縮量屬週期性，但反轉時點晚於公司規畫，Counterpoint 預測 2026 年出貨年減 13.9%，復甦要等 2027 年底新記憶體產能，公司則規畫 2027 年持平到小跌。可能看錯之處：若通路庫存確實已薄，公司的持平假設會比第三方準確。","fact_refs":["f_kpi1_non_gaap","f_kpi2_non_gaap","f_kpi3_gaap","f_kpi6_qct","f_kpi7_qct","f_kpi8_qct_iot","f_kpi9_qtl","f_kpi10_q1_fy2027","f_kpi11_fy2027"],"verdict_values":{"revenue_quality":"授權為合約型年金，Apple、華為、傳音已續約，下一輪續約落在 FY2030 至 FY2033；晶片營收受手機週期與客戶自研影響。GAAP 與非 GAAP 差距大：Q1 FY27 指引 GAAP EPS 1.03–1.23 美元，非 GAAP 2.15–2.35 美元。","unit_econ_note":"授權金按裝置售價計但有上限，價格在上限以下上漲才部分受惠（2026-07-29 CFO）；QCT 漲價幅度為雙位數，用來轉嫁投入成本。","archetype":{"primary":"品質複利成長","secondary":"循環/商品","confidence":"中","fingerprint":"授權年金加晶片平台；FY23 到 FY26 GAAP 營業利益幾乎持平，複利要靠新引擎兌現。"},"industry":{"clock_phase":"IV","sd_verdict_source":"手機處於收縮段，依據是 Counterpoint 預測 2026 年出貨年減 13.9%、IDC 預測年減 12.9%，FY26 10-K 也把手機營收下滑歸因於 OEM 因記憶體受限而調降生產計畫；屬週期性將反轉，但時點不早於 2027 年底。","bargaining":{"up":"記憶體與晶圓代工握有議價權：供應鏈滿載（2026-07-29 CEO），公司以雙位數漲價轉嫁，基礎毛利率到 FY27 下半年才回到 48–50% 區間低端。","down":"下游集中：Apple、三星各占 10% 以上營收；三星、小米自研；AWS 合作附平價認股權，顯示大客戶能分走經濟利益。","geo":"FY2025 依客戶總部計中國占營收 46%，晶圓與封測集中台灣與韓國。"},"profit_pool_dir":"手機鏈利潤向記憶體與自研晶片的品牌商移動；資料中心與車用是高通正在切入的新利潤池，但五年營業利益池占比事實表未涵蓋。","tam_table":[{"item":"資料中心","value":"公司稱長期可及市場約 1 兆美元，目標 5 至 7 年份額超過 5%；FY26 營收約 3 億美元，FY27 目標 50 億，FY29 目標 150 億。"},{"item":"車用","value":"FY26 底年化約 80 億美元，FY29 目標 100 億，設計案儲備 650 億美元（2026-06-24）。"},{"item":"IoT 與工業機器人","value":"FY29 目標合計逾 140 億美元，其中工業網通與機器人 80 億。"},{"item":"手機","value":"2026 年出貨預測 10.8 億支、年減 13.9%；公司規畫 2027 年持平到小跌。"},{"item":"未涵蓋項","value":"SAM、滲透率與營業利益池五年變化事實表未涵蓋，無法驗證利潤池流出幅度。"}]}}},"q2_moat":{"verdict":"護城河方向持平：授權續約守住費率、三星份額基準由五成升到七成以上，但 Apple 晶片退場與客戶自研是已經發生的生態攻擊，目前反映在等級折價，尚未構成整體下滑。","reasoning":"機制是專利組合跨世代授權，加上高階 Android 平台的整合能力與 OEM 驗證週期。三個可證方向：一、授權：Apple、華為、傳音完成續約，CFO 稱費率與權利金守住，營收跑率不變。二、最大客戶份額：Apple 已轉向自研；三星 Galaxy 基準由 50% 升到 70% 以上（2026-11-04 CEO）。三、出貨份額：Counterpoint 顯示 2026Q1 由 27% 降到 23%，但最直接的對手聯發科由 38% 降到 32%，份額流向 Apple 的 15% 到 19%，比較像記憶體短缺更傷 Android，而非對手搶單。與聯發科比，TTM 毛利率 53.1% 對 46.3%、營益率 20.1% 對 15.1%；與 NXP 比，營益率 20.1% 低於 28.6%。可能看錯之處：份額資料只到 2026Q1，若中國 OEM 自研比例在 FY27 持續上升，持平就會變成下滑。同業 ROIC 事實表未涵蓋，以利潤率與份額方向代替。","fact_refs":["f_peer_qcom_gross_margin_pct","f_peer_qcom_operating_margin_pct","f_peer_2454_tw_gross_margin_pct","f_peer_2454_tw_operating_margin_pct","f_peer_avgo_operating_margin_pct","f_peer_nvda_operating_margin_pct","f_peer_nxpi_operating_margin_pct"],"verdict_values":{"moat":{"mechanism":"專利跨世代授權年金，加上高階 Android 平台整合與 OEM 驗證週期；車用為多世代平台合約。","execution":8,"pricing":8,"grade":"B","trend":"→","trend_evidence":"execution 穩定：車用 Q4 年增 89%，三星份額基準升到 70% 以上，Apple 流失另列為威脅。pricing power 穩定：授權費率守住，QCT 雙位數漲價目前只夠修補成本。兩項各 8 分，尚未扣威脅。","competitor_notes":[{"name":"2454.TW","strategy_note":"最直接對手，份額同受記憶體短缺拖累；高通 TTM 毛利率與營益率仍高出約 7 與 5 個百分點。"},{"name":"AVGO","strategy_note":"客製矽的主要對手，營益率 48.5%，資料中心案子的規模與議價差距最大。"},{"name":"NVDA","strategy_note":"加速器生態的領先者，營益率 65.2%；高通 CEO 認為推論市場護城河弱於訓練，切入點在推論。"},{"name":"NXPI","strategy_note":"車用老牌對手，營益率 28.6% 高於高通；高通靠算力平台內容增加搶份額。"}],"peer_na_reason":"同業 ROIC 事實表未涵蓋，改用 TTM 利潤率比較與份額方向。","threats":[{"level":"🔴","text":"客戶垂直整合：Apple 已自研數據機，三星與小米也有自研晶片，10-K 明列為風險。機率指三星或主要中國 OEM 在 24 個月內明顯提高自研比例。","p":"35%","evidence_refs":["competitive_share_entrants#1","customer_second_source#0","customer_second_source#1","customer_concentration_credit#1","substitute_technology#0","substitute_technology#1","substitute_technology#2","end_markets#1"]},{"level":"🟡","text":"手機出貨份額推擠：聯發科與 Apple 在記憶體短缺下的份額變化，可能延伸到高階 Android。","p":"30%","evidence_refs":["competitive_share_entrants#0"]},{"level":"🟡","text":"資料中心客製矽多源競爭：博通、邁威爾與客戶自研都在同一張桌上，影響新事業，不傷既有授權與手機平台。","p":"35%","evidence_refs":["competitive_share_entrants#2"]},{"level":"🟡","text":"Arm：陪審團認定 Arm 違約，補救階段未決。CEO 稱對 CPU 路線圖沒有影響，法院裁定前不算解除；Arm 自製 CPU 也是資料中心對手。","p":"20%","evidence_refs":[]},{"level":"🟡","text":"監管：10-K 載明調查或訴訟可能迫使公司改變授權做法，單一國家處分可能延伸至境外。","p":"15%","evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#1"]}],"roic_durability":{"quadrant":"投入資本事實表未涵蓋，無法落象限；授權屬高利益率、輕資產，QCT 為中等利益率。","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者要的是手機與裝置體驗，決策者是 OEM，付款者是消費者。高階手機算力是需要，但記憶體漲價讓消費者延後換機，2026 年出貨預測年減 13.9%。車用與推論由車廠與雲端業者付款，較不受消費者延後影響。"},{"item":"決策層級","level":"🟡","text":"替代性要看 OEM 的平台決策：Apple 已換成自研，三星基準卻由 50% 升到 70% 以上，顯示旗艦 Android 仍不易替代。資料中心以雲端業者為決策單位，客製矽可多源，轉換成本尚未證實；車用已由逐案轉向多世代平台（2026-07-29 CEO）。漲價後流失率事實表未涵蓋。"},{"item":"價值鏈分配","level":"🟡","text":"記憶體與晶圓代工正分走更多利潤：QCT EBT 率由 Q1 FY26 的 31% 降到 Q4 的 24%，公司以雙位數漲價轉嫁，基礎毛利率到 FY27 下半年才回到區間低端。AWS 拿到平價認股權，代表大客戶也在分價值。授權費率守住是少數正面證據。"},{"item":"社會容忍度","level":"🟡","text":"授權模式長期受反壟斷檢視，10-K 列明調查可能迫使改變授權做法；2026 年搜尋未見 DOJ、FTC、EU 對高通的新行動，反壟斷焦點轉向 Arm。中國 SAMR 案最新進度事實表未涵蓋，列為資料缺口。"}],"roiic":"近零（FY23 到 FY26 GAAP 營業利益約 86.5 億到 86.6 億美元；投入資本事實表未涵蓋，無法算精確比率）","reinvest_rate":"事實表未涵蓋（資本支出、折舊、營運資金與收購淨額未入表）","endo_ceiling":null,"formula_note":"內生成長率＝增量 ROIC×再投資率；兩項輸入都缺，不硬算。FY26 同時是手機低點與 Apple 退場年，此窗口偏悲觀。"}}}},"q3_growth":{"verdict":"五年後仍有跑道：車用已是實績曲線（Q4 年增 89%），資料中心 12 月季開始出貨，但資料中心的第二段成長還沒有實績。","reasoning":"成長主要靠量與新品類：資料中心由 FY26 約 3 億美元到 FY27 目標 50 億；車用年化約 80 億美元，比 7 月預期高 10 億。價只用來修補毛利，併購補能力（Alphawave、Modular），淨回購貢獻小。共識 EPS FY27 10.16、FY28 12.85、FY29 17.84 美元，兩年 CAGR 32.5%；FY26 非 GAAP 全年 EPS 事實表未涵蓋，三年 CAGR 無法同口徑計算。FY29 共識已貼近公司目標 18 美元以上，賣方幾乎沒打折。內生上限因投入資本與再投資率缺資料無法量化，FY23 到 FY26 的 GAAP 營業利益近零增長；缺口歸因於營業費用率由 23% 往 19–20% 下降、漲價修補毛利與資料中心新增量。可能看錯之處：FY26 是低基期，若資料中心如期放量，歷史增量報酬的參考性很低。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_kpi11_fy2027"],"verdict_values":{"growth":{"driver_mix":"量為主（資料中心、車用新平台），價用於修補成本，併購補能力，淨回購貢獻小。","runway_years":"資料中心目前份額低於 1%，以公司 5 至 7 年 5% 目標推算，30% 滲透不構成五年內上限。","runway_post_y5":"🟢","endo_ceiling_basis":"事實表未涵蓋投入資本、資本支出與折舊，內生上限留空；以 FY23 到 FY26 GAAP 營業利益近零增長作為歷史參考，判定共識成長超過歷史內生能力。","segments":[{"item":"手機","value":"Q4 51.4 億美元，年減 26%；12 月季預期季減中個位數，Android 成長被 Apple 下滑抵銷。"},{"item":"車用","value":"Q4 19.9 億美元，年增 89%；年化約 80 億，FY29 目標 100 億。"},{"item":"IoT","value":"Q4 18.9 億美元，年增 4%，工業網通與機器人年增 20%。"},{"item":"資料中心","value":"12 月季逾 6.5 億美元，FY27 目標 50 億、年底跑率 70 億，FY29 目標 150 億；客製矽稀釋毛利率、對營益率加分。"},{"item":"授權","value":"Q4 13.0 億美元，EBT 率 70%；續約完成，跑率不變。"}],"decay_signals":[{"item":"毛利率連 2 季 YoY 下滑","lit":true,"text":"FY26 毛利率 53.1%，FY25 為 55.4%；QCT 短期低於歷史區間（2026-07-29 CEO）。單季 YoY 序列事實表未涵蓋。"},{"item":"核心市占近 12 個月縮減","lit":true,"text":"Counterpoint 2026Q1 份額 23%，前年同期 27%。"},{"item":"主力產品提價後銷量下滑","lit":false,"text":"漲價 FY27 第二季才開始反映，尚無資料。"},{"item":"EPS CAGR 高於營收 CAGR 逾 5 個百分點","lit":true,"text":"FY27 到 FY28 共識 EPS 增 26.5%，營收增 15.5%，差 11 個百分點。"},{"item":"FCF／淨利連 2 年低於 0.75","lit":false,"text":"FY26 為 0.63、FY25 為 2.31，僅一年，且 FY26 淨利含非營業或稅務項目。"},{"item":"SBC／營收大於 5% 且逐年上升","lit":null,"text":"Q4 為 8.5%；逐年序列事實表未涵蓋。"},{"item":"TAM 萎縮或被替代技術壓縮","lit":"partial","text":"手機市場縮量、Apple 自研移除一塊可服務市場；車用與資料中心 TAM 擴大。"},{"item":"產業估值倍數近 3 年系統性下移","lit":null,"text":"事實表未涵蓋。"},{"item":"維護性資本支出占 FCF 大於 60%","lit":null,"text":"事實表未涵蓋。"},{"item":"停止投資新產能且收入 3 年內下滑","lit":false,"text":"公司仍大幅投資資料中心，FY23 到 FY26 營收成長。"}],"trap_rating":"🔴"}}},"q4_capital":{"verdict":"資本配置中等：現金大部分還給股東、股本持續縮，但近一輪成長靠併購與股權換取，資本回報還沒有實績。","reasoning":"FY26 自由現金流 86.5 億美元、利潤率 20.1%，FY25 為 128.2 億、29.0%；Q4 單季 18.2 億。FCF／淨利 FY26 為 0.63，但淨利 136.3 億高於營業利益約 86.6 億，含非營業或稅務項目，比率失真，該項目內容事實表未涵蓋。Q4 回饋股東 20 億美元（回購與股利各 10 億），Q3 為 23 億。SBC 單季 8.73 億美元，占非 GAAP 營業利益 31.5%、GAAP 營收 8.5%。以淨利除以 EPS 推算稀釋股數，FY23 約 11.26 億股、FY26 約 10.73 億股，年減約 1.6%。Modular 以 1,783 萬股作價，AWS 合作發平價認股權。淨負債 83.1 億美元。近三年現金去向四分與回購均價事實表未涵蓋。可能看錯之處：Alphawave 與 Modular 剛併入，現在判未過可能太早。","fact_refs":["f_kpi4_q4","f_kpi5_sbc_non_gaap","f_net_debt_m","f_dividend_yield_ttm","f_shares_diluted_m"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":true,"passed":false,"input":"Alphawave、Modular 剛併入，尚無已實現回報；五年 35 筆併購後，FY23 到 FY26 GAAP 營業利益持平，投入資本事實表未涵蓋，暫判未過。"},{"name":"buyback_yield","applicable":true,"passed":null,"input":"回購均價與 10 年期殖利率事實表未涵蓋，無法判定。"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"FY23 到 FY26 稀釋股數年減約 1.6%，扣除 SBC 後仍淨縮股；Modular 的 1,783 萬股與 AWS 認股權需在 FY27 重看。"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長主要不靠併購撐，且事實表只有最近兩季的回購與股利，無法編三年現金去向。"}}}},"q5_valuation":{"verdict":"現價 165.41 美元要求 FY31 EPS 約 16 美元（以 15 倍終端倍數、年報酬 10% 反推），低於公司自己訂的 FY29 目標 18 美元以上。這個要求可信，基本情境 FY31 約 18.5 美元，但便宜的說法不成立，因為分母是非 GAAP。","reasoning":"FY27 共識 EPS 10.16 美元對應 16.3 倍。Trailing 13.0 倍不能用：FY26 GAAP EPS 12.70 美元含非營業或稅務項目，淨利高於營業利益。另一端，Q1 FY27 GAAP EPS 指引中點 1.13 美元，年化約 4.5 美元，對應約 37 倍，兩個口徑相差一倍以上。Q1 非 GAAP 指引中點 2.25 美元，其餘三季要平均 2.64 美元才到 FY1 共識，比 Q1 高 17%。FCF 殖利率 4.9%，EV/S 4.3 倍。FY1 共識近 3 個月下修 3.5%，最近兩份快照沒有變動，11-04 指引可能尚未反映。同業 Forward P/E 事實表未涵蓋。可能看錯之處：若資料中心如期放量，GAAP 與非 GAAP 差距會因營收攤薄而收斂，現在的 37 倍會高估貴的程度。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_pe_current","f_pe_percentile","f_ps_current","f_ev_s_current","f_ev_s_percentile","f_ev_s_fwd","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_3m_fy1_pct","f_kpi10_q1_fy2027"],"verdict_values":{"valuation":{"basis":"FY27 共識非 GAAP EPS 的 Forward P/E，並以 GAAP 指引年化與自由現金流對照。","peers":{"expanded":false,"reason":"同業 Forward P/E 事實表未涵蓋，同業表只有利潤率，無法做倍數對照；終端倍數改以公司自身現值與成長熄火情境定錨。"},"fwd_pe":16.28,"peg":0.5,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"非 GAAP 16.3 倍、PEG 0.50 看似便宜，但成長多為低基期反彈且共識貼著公司目標；GAAP 年化約 37 倍、FCF 殖利率 4.9%、EV/S 4.3 倍居四個年度端點的 59 百分位，兩面相抵落在合理區。PEG 以 FY27 到 FY29 兩年 CAGR 32.5% 計算。事實表只有四個年度端點，不構成五年分位，故留空。","upside_short_pct":8.8,"upside_mid_pct":36.0,"denominator_disputed":true,"denominator_note":"Trailing EPS 含一次性項目，不採用；FY27 非 GAAP EPS 10.16 美元未計單季 8.73 億美元的 SBC 與收購相關費用，Q1 GAAP 指引只有非 GAAP 的一半。分母本身就是爭點，便宜論證不成立。"}}},"q6_how_wrong":{"verdict":"最可能看錯的地方有三個：資料中心只靠兩家客戶撐起斜坡、手機市場比公司規畫更弱、非 GAAP 盈餘高估了股東實際拿到的錢。衰退信號已亮三盞以上，便宜表象不能當安全邊際。","reasoning":"股價 26 週跌 23.8%，RSI 44.3，沒有過熱，但跌幅本身不是安全邊際。共識 FY1 近 3 個月下修 3.5%，下修中的共識會把 Bear 地板往下推，上下行比值不能當進場依據。管理層未正面回答的項目：3 月季營收方向（CFO 由 7 月說會成長改為不給指引）、Apple FY27 確切金額、漲價分市場幅度、毛利率回升的確切時點。FY27 訂單覆蓋已由 6 月的迴避改為 11 月的「healthy order coverage」，仍未給數字。反方向的錯誤：若 3 月季資料中心超過 10 億美元，等待的代價是少賺一段。","fact_refs":["f_week26_return_pct","f_rsi14","f_consensus_rev_3m_fy1_pct"],"verdict_values":{"trap":{"verdict":"🔴","label":"非 GAAP 便宜、GAAP 偏貴，毛利與份額仍在下滑"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":10.16,"pe":16.28,"basis":"FY27 共識 EPS（進行中財年，非 GAAP 口徑），終端倍數同以當年 EPS 為分母。"},"eps":{"bull":[10.4,13.4,18.2,21.2,24.0],"base":[9.85,12.0,15.0,16.8,18.5],"bear":[9.0,9.2,9.6,10.0,10.5]},"pe":{"bull":18,"base":15,"bear":11},"p":{"bull":22,"base":46,"bear":32},"yield_pct":{"dividend":2.19,"net_buyback":0},"second_stage":{"bull_cagr_pct":12,"base_cagr_pct":8},"max_dd":{"lo":-50,"hi":-35,"basis":"Q1 指引中點年化 EPS 9 美元乘以低谷倍數 10 倍得 90 美元，較現價 −46%；股價 26 週已由約 217 美元跌到 165 美元（−23.8%），顯示這種波動真實存在。下緣取 −50% 容納中國或資料中心事件，上緣取 −35%。","trigger_time":null},"basis":{"bull":"公司目標兌現：FY29 EPS 18.2 美元、資料中心 150 億美元，第三家客戶與 HBC 加速器放量；18 倍反映非手機占比提高，同業倍數事實表未涵蓋。","base":"FY29 EPS 15.0 美元，低於公司目標約 17%：資料中心 110 億美元、2027 年手機市場年減約 5%、QCT 基礎毛利率回 48%；之後靠車用與推論放緩成長。EPS 路徑已含小幅縮股，淨回購殖利率填 0 避免重複計算；同業終端倍數對照事實表未涵蓋。","bear":"任一大客戶未續單，資料中心停在 70 億美元以下，手機繼續縮，QCT 毛利率落在 45–46%；FY31 EPS 10.5 美元靠授權與車用撐住，11 倍取自成長降到 10% 的熄火情境。Bear 機率 32%，依據是客製矽多源採購與客戶自研，且成長超過歷史內生能力。"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"FY27 資料中心 50 億美元大部分來自兩家客戶；客製矽向來多源採購，伺服器級 Oryon 要到 2028 年中才推出。","assumption":"兩家客戶的下一代案子會續留高通。","consequence":"資料中心停在 70 億美元以下，FY31 EPS 約 10.5 美元、倍數 11 倍，五年價格約 115 美元，中途可能見 90 美元。","ruling":"採納，與唯一致命事件相同，Bear 機率維持 32%。","watch":"FY28 訂單覆蓋說法、第三家客戶是否轉為實質營收。","evidence_refs":["competitive_share_entrants#2"]},{"view":"論點成功但股東經濟變差","evidence":"客製矽毛利率低於公司平均（2026-06-24 CFO），FY26 自由現金流由 128.2 億降到 86.5 億美元，Q1 FY27 GAAP EPS 指引只有非 GAAP 的一半；AWS 合作發平價認股權，Modular 以 1,783 萬股作價。","assumption":"資料中心營收達標就等於股東賺到錢。","consequence":"EPS 達標但每股自由現金流成長落後，倍數回不到 18 倍以上。","ruling":"採納。Base 終端倍數壓到 15 倍，低於現值 16.3 倍。","watch":"FY27 FCF 利潤率是否回到 24% 以上；GAAP 與非 GAAP EPS 差距是否縮小；CFO 稱 AWS 認股權是例外，若第二家也要求股權就算證偽。","evidence_refs":[]},{"view":"價格已反映太多","evidence":"FY29 共識 17.84 美元幾乎等於公司目標 18 美元以上；Q1 指引中點 2.25 美元，其餘三季要平均 2.64 美元才到 FY1 共識；財報後盤後跌約 6%（單一二手來源，未證實）。股價較前份 148.4 美元高 11.5%。","assumption":"共識路徑可以全額兌現。","consequence":"共識下修會同時壓低 EPS 與倍數，現價的 16.3 倍會變成更高的實際倍數。","ruling":"部分採納：非 GAAP 倍數不算貴，但共識路徑太滿，Base FY29 EPS 15.0 美元，較共識低 16%。","watch":"下一份月度共識快照是否反映 11-04 指引。","evidence_refs":["capital_markets_pricing#1"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 🟠 → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=🟠","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 148.4 → 本次 165.41（+11.5%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=148.4","side_b":"本次 price_at_dd=165.41","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]裁決由 dd_decision.py 機械路由：前份 進場 → 本次 觀望","cause":"新證據","prior_field":["dca_verdict"],"side_a":"前份 dca_verdict=進場","side_b":"本次 dca_verdict=觀望","ruling":"裁決是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。沒有單一輸入能還原，屬多欄共同：均線 🟠→🟡、陷阱燈 🟡→🔴。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]角色由 dd_decision.py 機械路由：前份 衛星 → 本次 追蹤","cause":"新證據","prior_field":["dca_role"],"side_a":"前份 dca_role=衛星","side_b":"本次 dca_role=追蹤","ruling":"角色是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。沒有單一輸入能還原，屬多欄共同：均線 🟠→🟡、陷阱燈 🟡→🔴。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 148.4 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 148.4 美元：Bull 價 387、Bear 價 100，五年期望值 +76.7%，基準年化 14.4%，不對稱比 6.0","side_b":"本次情境、股價仍用 148.4 美元：Bull 價 432、Bear 價 115.5，五年期望值 +75.0%，基準年化 13.3%，不對稱比 5.93","ruling":"先換情境、股價不動：五年期望值少 1.7 個百分點，基準年化少 1.1 個百分點。不對稱比由 6.0 變為 5.93。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 148.4 美元：五年期望值 +75.0%，基準年化 13.3%，不對稱比 5.93","side_b":"本次情境、股價 165.41 美元：五年期望值 +57.0%，基準年化 10.9%，不對稱比 3.67","ruling":"再換股價、情境不動：起點價上漲 11.5%，五年期望值少 18.0 個百分點，基準年化少 2.4 個百分點，不對稱比由 5.93 降到 3.67。合計五年期望值比前份少 19.7 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"手機市場 2027 預期","cause":"新證據","prior_field":null,"side_a":"公司：2027 年手機市場持平到小跌，通路庫存已薄，6 月季是中國 Android 低點（2026-11-04 CFO）。","side_b":"Counterpoint 預測 2026 年年減 13.9%、復甦要等 2027 年底；三星稱 2027 年供需缺口可能更大；Bernstein 分析師指年底出貨跑率可能年減逾兩成。","ruling":"屬程度差異。採第三方方向，基本情境假設 2027 年手機市場年減約 5%，低於公司規畫。","evidence_level":"中","settle_metric":"3 月季 QCT 手機營收，以及公司 2027 年市場預期是否下修。","if_then":["若公司把 2027 年市場預期下修到年減 5% 以上，則停止加碼，並下修 FY28 基本 EPS。","反向：若 3 月季中國 Android 續季增且未見提前拉貨，則基本情境回到持平假設。"],"evidence_refs":["supply_demand_durability#0","supply_demand_durability#1","supply_demand_durability#2","end_markets#0","end_markets#3"]},{"axis":"資料中心營收集中度","cause":"新證據","prior_field":null,"side_a":"2026-06-24 CFO：資料中心營收來源並不集中。","side_b":"2026-11-04 CFO：FY27 的 50 億美元由兩家客戶以大規模貢獻，第三家不在主要斜坡內。","ruling":"採後者。FY27 斜坡按兩家客戶集中看待，這也是致命事件設在客戶續單的原因。","evidence_level":"高","settle_metric":"FY28 營收中第三家客戶的占比。","if_then":["若第三家客戶到 FY28 底仍無實質營收，則停止加碼。","反向：若第三家客戶 FY28 營收達 10 億美元以上，則下調 Bear 機率至 28%。"],"evidence_refs":["competitive_share_entrants#2"]},{"axis":"管理層對 3 月季的說法","cause":"新證據","prior_field":null,"side_a":"2026-07-29 CFO：預期 12 月季到 3 月季營收成長。","side_b":"2026-11-04 CFO：不給 3 月季指引，只說市場的看法合理。","ruling":"屬迴避，尚不構成改口實證。季節性判斷不列入基本情境，FY27 基本 EPS 9.85 美元略低於共識 10.16 美元。","evidence_level":"中","settle_metric":"2027-02 法說的 3 月季營收指引。","if_then":["若 3 月季指引中點低於 12 月季指引中點 108 億美元，則停止加碼，FY27 基本 EPS 下修到 9.5 美元以下。","反向：若指引中點高於 115 億美元，則維持基本路徑。"],"evidence_refs":[]},{"axis":"盈餘分母","cause":"新證據","prior_field":null,"side_a":"FY27 非 GAAP 共識對應 16.3 倍，PEG 約 0.5，看起來便宜。","side_b":"Q1 FY27 GAAP 指引年化約 4.5 美元，對應約 37 倍；SBC 單季 8.73 億美元，占非 GAAP 營業利益 31.5%。","ruling":"屬程度差異，但便宜論證不成立。估值以非 GAAP 為主尺，終端倍數下壓到 15 倍反映品質折價。","evidence_level":"高","settle_metric":"FY27 自由現金流利潤率與 GAAP EPS。","if_then":["若 FY27 FCF 利潤率低於 18%，則停止加碼，基本終端倍數下修到 13 倍。","反向：若回到 24% 以上，則基本終端倍數可回到 16 倍。"],"evidence_refs":[]},{"axis":"現在就買的最強論證","cause":"新證據","prior_field":null,"side_a":"授權已續到 FY30 週期、車用 Q4 年增 89%、資料中心 12 月季開始出貨，股價 26 週跌 23.8%，現價隱含 FY31 EPS 約 16 美元，賣方財報前目標價多在 215 美元上下。","side_b":"毛利與份額仍在下滑，共識可能尚未反映 11-04 指引，賣方目標價都早於財報，第一個硬數據只要再等幾個月。","ruling":"不追。等待的代價是可能少賺一段，但 3 月季資料中心實績能分辨斜坡真假，資訊價值高於現在的價格優勢。","evidence_level":"中","settle_metric":"3 月季資料中心單季營收。","if_then":["若股價在實績前漲到 195 美元以上，則不追。","若股價跌破 135 美元而資料中心與毛利框架未破，則分批反買首倉。","反向：若 3 月季資料中心低於 8 億美元，則減碼已持有部位一半並重做判斷。"],"evidence_refs":["capital_markets_pricing#1","capital_markets_pricing#2","capital_markets_pricing#3"]},{"axis":"共識是否已含最新指引","cause":"新證據","prior_field":null,"side_a":"FY1 共識最近兩份快照都是 10.16 美元，顯示 11-04 指引可能尚未進模型。","side_b":"FY1 近 3 個月已由 10.53 美元下修到 10.16 美元，部分反映記憶體壓力。","ruling":"不可裁決至下一份月度快照。在此之前凍結加碼，倉位不超過首倉。","evidence_level":"低","settle_metric":"2026-12 共識快照的 FY1 與 FY2 EPS。","if_then":["若 FY1 再下修 5% 以上，則停止加碼，Bear 路徑下移。","反向：若 FY1 持平且 FY2 上修，則維持基本路徑。"],"evidence_refs":["capital_markets_pricing#1"]},{"axis":"產業態勢三軸","cause":"新證據","prior_field":null,"side_a":"競爭與客戶結構惡化：手機份額由 27% 降到 23%，Apple 自研，三星與小米自研，中國營收集中。","side_b":"結構轉好：授權續約到 FY30 週期，車用 Q4 年增 89%，資料中心開始出貨，SpaceX 地面 5G 網路 FY28 起貢獻。","ruling":"雙向拉鋸。手機端競爭與客戶結構惡化，非手機端結構轉好；其他結構變數以客戶結構為主，出口管制與關稅維持觀察。","evidence_level":"中","settle_metric":"FY27 非手機占 QCT 比重是否逾一半。","if_then":["若 FY27 非手機占 QCT 低於 45%，則停止加碼。","反向：若逾 55% 且含資料中心的 QCT 毛利率不低於 46%，則加碼至上限 3%。"],"evidence_refs":["competitive_share_entrants#0","customer_second_source#1","regulatory_antitrust#2"]},{"axis":"價值陷阱評級上調","cause":"新證據","prior_field":["trap"],"side_a":"前份為中度風險。","side_b":"本次毛利率下滑、核心份額縮減、EPS 成長遠高於營收三項確定亮燈，手機 TAM 半亮。","ruling":"上調到最高風險級。亮燈中有兩項來自 Apple 與記憶體的已知衝擊，但依亮燈數不能降級；Trailing 倍數的便宜也來自一次性分母。","evidence_level":"中","settle_metric":"FY27 下半年 QCT 毛利率與 FY1 共識方向。","if_then":["若含資料中心的 QCT 毛利率連 2 季低於 46%，則減碼一半。","反向：若扣除資料中心影響的毛利率回到 48% 以上且共識止跌，則風險級下調一檔。"],"evidence_refs":["competitive_share_entrants#0","end_markets#3"]},{"axis":"護城河、跑道、類型與循環位置維持","cause":"新證據","prior_field":["moat_trend","runway_post_y5","archetype","cycle_position"],"side_a":"前份：護城河持平、五年後跑道寬、品質複利成長、早循環。","side_b":"本次四欄不變。授權續約與三星份額支持持平，車用實績支持跑道，公司自述 6 月季為中國 Android 低點。","ruling":"維持，但 FY23 到 FY26 GAAP 營業利益持平，使類型信心降為中；手機市場仍在收縮，早循環只適用於公司自身營收。","evidence_level":"中","settle_metric":"三星份額基準、車用年化營收、中國 Android 季增。","if_then":["若三星份額基準低於 60%，則停止加碼，護城河方向改列下滑重評。","反向：若同業 ROIC 資料補齊且差距擴大，則重評等級。"],"evidence_refs":["competitive_share_entrants#1"]},{"axis":"訊號與估值維持","cause":"價格變動","prior_field":["signal","val"],"side_a":"前份股價 148.4 美元，訊號與估值均為中性。","side_b":"本次股價 165.41 美元，上漲 11.5%，基本面多空互抵，兩欄維持不變。","ruling":"維持。股價上漲吃掉部分空間，授權續約與車用超標抵銷了部分估值壓力。","evidence_level":"中","settle_metric":"FY27 共識 EPS 與股價的相對變化。","if_then":["若股價漲到 195 美元以上而實績未到，則不追。","反向：若股價跌破 135 美元而基本面未破，則分批反買。"],"evidence_refs":[]},{"axis":"機率與最大回撤口徑","cause":"方法變動","prior_field":["p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份 Bull 22%、Bear 32%、最大回撤單點 −45%。","side_b":"本次機率維持 22%、46%、32%，最大回撤改為 −35% 至 −50% 的範圍。","ruling":"授權續約降低下行，手機展望轉弱增加下行，兩者互抵，機率不動；回撤改用範圍表達不確定性。","evidence_level":"中","settle_metric":"3 月季資料中心實績與手機市場預期。","if_then":["若 3 月季資料中心達 10 億美元以上，則重跑判斷並檢討 Bear 機率。","反向：若低於 8 億美元，則 Bear 機率上調到 40%。"],"evidence_refs":[]},{"axis":"裁決與角色","cause":"新證據","prior_field":[],"side_a":"前份進場、衛星。","side_b":"本次結論是不追，等 3 月季資料中心實績。","ruling":"價值陷阱風險上調、分母爭議成立、最新指引可能尚未進共識，三者都由同一個事件驗證，故等事件而非等價格。","evidence_level":"中","settle_metric":"3 月季資料中心單季營收。","if_then":["若達 10 億美元以上，則重跑判斷，過關開首倉三分之一。","反向：若低於 8 億美元，則減碼已持有部位一半。"],"evidence_refs":[]},{"axis":"加碼與進場條件變動","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"starter 1/3·帽 3%·加碼＝QCT 毛利率回 48%＋（Q1 FY27 法說）或資料中心單季營收 ≥ $1.0B","side_b":"3 月季資料中心單季營收 ≥ $10 億（約 2027-04 底法說）→重跑判斷，過關才開首倉 1/3、總倉上限 3%","ruling":"QCT 自 FY27 起納入資料中心，CFO 說基礎毛利率回到區間低端後還會被資料中心拉低，報表值 48% 的門檻即使計畫順利也碰不到，故首要條件改為資料中心實績；毛利加碼條件改用扣除資料中心影響的 48%。","evidence_level":"高","settle_metric":"3 月季資料中心營收與 FY27 下半年毛利率。","if_then":["若資料中心達標，則重跑判斷。","反向：若 FY27 下半年扣除資料中心影響的毛利率仍低於 48%，則不加碼。"],"evidence_refs":[]},{"axis":"Single Thing 補列","cause":"方法變動","prior_field":null,"side_a":"前份摘要未載明 Single Thing（欄位為空）。","side_b":"兩家超大型雲端客製矽客戶中任一家，在 FY28 前把下一代加速器交給其他供應商或自製，使資料中心營收掉到 FY27 年底 70 億美元跑率以下。","ruling":"Single Thing 由本輪補上，依盈餘敏感度選定：資料中心差距每股約 2 美元，大於 Android 營收少一成的約 0.6 美元與毛利率少 2 個百分點的約 0.75 美元（自行估算）。","evidence_level":"中","settle_metric":"FY28 資料中心營收與客戶續單。","if_then":["若事件發生，則清倉。","反向：若兩家都簽下一代合約，則 Bear 機率下調到 28%。"],"evidence_refs":[]},{"axis":"減碼與清倉門檻補列","cause":"方法變動","prior_field":null,"side_a":"前份摘要未載明量化門檻（欄位為空）。","side_b":"資料中心 FY27 低於 40 億美元清倉；含資料中心的 QCT 毛利率連 2 季低於 46% 減碼；QTL 年營收低於 54 億美元或 EBT 率低於 65%、三星份額低於 60%、FCF 利潤率低於 18% 停止加碼。","ruling":"前份門檻散在假設與風險文字中，本輪集中列出，便於逐季對帳。","evidence_level":"中","settle_metric":"各門檻對應的季報數字。","if_then":["若任一清倉門檻觸發，則清倉。","反向：若門檻全部未觸發且資料中心達標，則維持條件。"],"evidence_refs":[]},{"axis":"授權風險降位","cause":"新證據","prior_field":null,"side_a":"前份：裝置售價上限、華為未續約、中國 SAMR 裁決三重壓縮。","side_b":"Apple、華為、傳音已續約，CFO 稱費率守住，下一輪續約落在 FY2030 至 FY2033。","ruling":"華為未續約風險退休；售價上限仍在；SAMR 案本輪事實表未涵蓋，保留為資料缺口。QTL 年營收 54 億美元與 EBT 率 68% 的門檻保留。","evidence_level":"高","settle_metric":"QTL 分部營收與 EBT 率；SAMR 案進度。","if_then":["若 QTL 單季 EBT 率低於 65%，則停止加碼。","反向：若 SAMR 案確認無救濟，則移除該項資料缺口。"],"evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#1"]}],"triggers":[{"n":1,"text":"12 月季資料中心營收達 6.5 億美元以上，並在 2 月法說確認 FY27 目標 50 億美元。","type":"假設驗證","maps_to":"H1","metric":"資料中心單季營收","threshold":"≥6.5 億美元且目標不下修","action":"未達則停止加碼並重做判斷","source_freq":"季報與法說，每季","date":"2027-02"},{"n":2,"text":"3 月季資料中心單季營收達 10 億美元以上，重跑判斷後開首倉三分之一，總倉上限 3%。","type":"估值rearm","maps_to":"H1","metric":"資料中心單季營收","threshold":"≥10 億美元","action":"重跑判斷，過關開首倉三分之一","source_freq":"季報與法說，每季","date":"2027-04"},{"n":3,"text":"FY27 下半年扣除資料中心影響的 QCT 毛利率回到 48% 以上，且 FY27 資料中心目標未下修。","type":"加碼","maps_to":"H2","metric":"扣除資料中心影響的 QCT 毛利率","threshold":"≥48%","action":"加碼至上限 3%","source_freq":"法說毛利率說明，每季","date":"2027-08"},{"n":4,"text":"3 月季資料中心低於 8 億美元，FY27 目標 50 億美元在算術上已難達成。","type":"減碼","maps_to":"R1","metric":"資料中心單季營收","threshold":"<8 億美元","action":"減碼一半並重做判斷","source_freq":"季報與法說，每季","date":"2027-04"},{"n":5,"text":"含資料中心的 QCT 毛利率在 FY27 下半年連 2 季低於 46%。","type":"減碼","maps_to":"R2","metric":"含資料中心的 QCT 毛利率","threshold":"連 2 季 <46%","action":"減碼一半","source_freq":"法說毛利率說明，每季","date":"2027-11"},{"n":6,"text":"公司下修 2027 年手機市場預期至年減 5% 以上，或 QCT 手機營收連 2 季低於指引中點。","type":"風險","maps_to":"R3","metric":"手機市場預期與 QCT 手機營收","threshold":"年減 ≥5% 或連 2 季低於中點","action":"停止加碼","source_freq":"法說，每季","date":"2027-05","evidence_refs":["supply_demand_durability#0","supply_demand_durability#1","supply_demand_durability#2"]},{"n":7,"text":"三星 Galaxy 份額基準跌破 60%，或主要中國 OEM 旗艦改採自研晶片。","type":"風險","maps_to":"R4","metric":"三星份額基準與中國 OEM 旗艦採用","threshold":"<60% 或出現自研旗艦","action":"停止加碼，護城河方向重評","source_freq":"法說與第三方拆機，每半年","date":"2027-03","evidence_refs":["customer_second_source#1","substitute_technology#0"]},{"n":8,"text":"美國新增對中國客戶銷售限制，或貿易政策使 QCT 毛利率單季下降 2 個百分點以上。","type":"風險","maps_to":"R5","metric":"QCT 毛利率與中國營收","threshold":"單季毛利率降 ≥2 個百分點","action":"減碼一半","source_freq":"8-K、10-Q，事件與每季","date":"2027-05","evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","geo_supply_chain#1"]},{"n":9,"text":"兩家客製矽客戶中任一家宣布或被揭露下一代不用高通。","type":"Single Thing","maps_to":"Single Thing","metric":"客製矽下一代合約","threshold":"任一家流失","action":"清倉","source_freq":"法說與公司公告，事件","date":"2028-09"},{"n":10,"text":"FY27 資料中心全年營收低於 40 億美元。","type":"清倉","maps_to":"H1","metric":"資料中心年營收","threshold":"<40 億美元","action":"清倉","source_freq":"10-K，每年","date":"2027-11"},{"n":11,"text":"QTL 單季 EBT 率低於 65%，或年營收低於 54 億美元。","type":"假設驗證","maps_to":"H3","metric":"QTL 營收與 EBT 率","threshold":"EBT 率 <65% 或年營收 <54 億美元","action":"停止加碼並重評授權年金","source_freq":"季報分部資料，每季","date":"2027-05","evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#1"]},{"n":12,"text":"3 月季法說後複審全部假設與門檻。","type":"複審日期","maps_to":"H1","metric":"全部假設","threshold":"到期複審","action":"重跑判斷","source_freq":"一次性","date":"2027-05"}],"kill_metrics":[{"metric":"資料中心年營收","bear_threshold":"FY27 低於 40 億美元","window":"FY27 全年","source":"公司季報與法說","last_status":"unknown"},{"metric":"含資料中心的 QCT 毛利率","bear_threshold":"FY27 下半年連 2 季低於 46%","window":"2027-04 至 2027-11","source":"公司法說毛利率說明","last_status":"unknown"},{"metric":"QTL 年營收與 EBT 率","bear_threshold":"年營收低於 54 億美元或單季 EBT 率低於 65%","window":"每季滾動","source":"公司季報分部資料","last_status":"ok"},{"metric":"三星 Galaxy 高通份額基準","bear_threshold":"低於 60%","window":"下一代 Galaxy 旗艦","source":"公司法說與第三方拆機","last_status":"ok"},{"metric":"自由現金流利潤率","bear_threshold":"FY27 低於 18%","window":"FY27 全年","source":"公司 10-K 現金流量表","last_status":"ok"}],"evidence_dismissed":[],"action_conditions":{"rearm_trigger":"3 月季資料中心單季營收 ≥ $10 億（約 2027-04 底法說）→重跑判斷，過關才開首倉 1/3、總倉上限 3%","exec_line":"未持有：等上述事件，不預先建倉。已持有首倉：續抱不加碼，FY27 下半年毛利達標才加碼到 3%。股價先漲到 195 美元以上而實績未到則不追；跌破 135 美元而資料中心與毛利框架未破則分批反買。","holding_cap":"3%"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":"早循環","cycle_verdict":"未觸發","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場對 FY29 目標打折合理，但把合約鎖到 FY30 週期的授權年金與已實現的車用成長一起打折：現價以 15 倍終端、年報酬 10% 反推，只要求 FY31 EPS 約 16 美元，低於公司 FY29 目標。","momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等 3 月季資料中心單季營收 ≥ 10 億美元的實績（約 2027-04 底法說），達標後重跑判斷。","asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null},"thesis":{"H":[{"id":"H1","text":"資料中心與車用補上 Apple 退場：FY27 非手機 QCT 營收年增逾 60%，其中資料中心達 50 億美元；FY29 非手機至少 320 億美元（公司目標 400 億打八折）。","2y":"FY27 資料中心 ≥50 億美元、年底跑率約 70 億；FY28 資料中心 ≥80 億美元。","5y":"FY29 資料中心 ≥110 億美元；FY31 資料中心占總營收 ≥20%。","10y":null,"threshold":"FY27 資料中心 ≥50 億美元；FY29 非手機 ≥320 億美元。","source":"公司季報與法說分部揭露，每季。","drift_rule":"TTM 較路徑偏離連 2 季 ≥5% 視為削弱，連 3 季 ≥10% 視為反轉。"},{"id":"H2","text":"漲價落地後 QCT 基礎毛利率回到 48% 以上，資料中心對毛利率的稀釋不超過 2 個百分點，QCT 營益率仍能走向 30% 的長期目標。","2y":"FY27 下半年扣除資料中心影響的 QCT 毛利率 ≥48%，含資料中心的報表值 ≥46%。","5y":"FY31 QCT EBT 率 ≥28%。","10y":null,"threshold":"扣除資料中心影響 ≥48%；含資料中心 ≥46%。","source":"法說毛利率說明與分部 EBT 率，每季。","drift_rule":"TTM 較路徑偏離連 2 季 ≥5% 視為削弱，連 3 季 ≥10% 視為反轉。"},{"id":"H3","text":"QTL 年金維持約 54 億美元以上、EBT 率 68% 以上，不被裝置售價上限、監管處置或下一輪續約結構性壓縮。","2y":"年營收 ≥54 億美元、EBT 率 ≥68%。","5y":"FY30 續約週期開始前維持跑率。","10y":"6G 世代費率與 5G 相近，FY33 後年營收 ≥50 億美元。","threshold":"年營收 ≥54 億美元；EBT 率 ≥68%。","source":"QTL 分部營收與 EBT 率，每季；10-K 授權風險揭露，每年。","drift_rule":"跨 2 個年度偏離視為削弱，跨 3 個年度視為反轉。"}],"R":[{"id":"R1","text":"資料中心擴不出兩家客戶：客製矽多源採購，HBC 加速器與 Dragonfly CPU 轉單未經實績驗證，FY29 的 150 億美元斜坡中途停住。","h_ref":"H1","clock":"🔥","threshold":"FY28 資料中心低於 70 億美元，或第三家客戶到 FY28 底仍無實質營收。","evidence_refs":["competitive_share_entrants#2"]},{"id":"R2","text":"QCT 毛利率結構性下移：漲價落地慢於組合稀釋，EBT 率由 Q1 FY26 的 31% 降到 Q4 的 24%，Q1 FY27 指引 20–22%（含資料中心併入影響 3 個百分點）。","h_ref":"H2","clock":"⚡","threshold":"含資料中心的 QCT 毛利率連 2 季低於 46%。","evidence_refs":[]},{"id":"R3","text":"手機市場比公司規畫更弱：記憶體短缺延續到 2027 年以後，FY26 Q4 手機營收已年減 26%，公司的持平到小跌假設落空。","h_ref":"H1","clock":"⚡","threshold":"公司下修 2027 年市場預期至年減 5% 以上，或 QCT 手機營收連 2 季低於指引中點。","evidence_refs":["supply_demand_durability#0","supply_demand_durability#1","supply_demand_durability#2","end_markets#0","end_markets#3"]},{"id":"R4","text":"客戶自研與集中：Apple 已轉自研，下一代 iPhone 份額遠低於先前估計的 20%，Apple 與三星各占 10% 以上營收，三星與小米也在自研。","h_ref":"H1","clock":"🐢","threshold":"三星 Galaxy 份額基準低於 60%，或主要中國 OEM 旗艦改用自研。","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1","customer_second_source#0","customer_second_source#1","customer_concentration_credit#0","customer_concentration_credit#1","end_markets#1","substitute_technology#0","substitute_technology#1","substitute_technology#2"]},{"id":"R5","text":"中國與地緣：依客戶總部計中國占 FY25 營收 46%，出口限制、關稅或台海衝突都可能切斷銷售或供應；華為產品營收已不再預期。","h_ref":"H1","clock":"🔥","threshold":"美國新增對中國客戶銷售限制，或貿易政策使 QCT 毛利率單季下降 2 個百分點以上。","evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","geo_supply_chain#0","geo_supply_chain#1"]},{"id":"R6","text":"監管與授權做法：10-K 載明調查可能迫使降低權利金率或改變授權做法；裝置售價上限仍在；中國 SAMR 案最新進度事實表未涵蓋，列為資料缺口。","h_ref":"H3","clock":"🐢","threshold":"任一主要司法管轄區命令降低權利金率或強制授權晶片商。","evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#1"]}],"single_thing":{"description":"兩家超大型雲端客製矽客戶中任一家，在 FY28 前把下一代加速器交給其他供應商或自製，使資料中心營收掉到 FY27 年底 70 億美元跑率以下。","why_fatal":"資料中心是 FY29 盈餘最大的單一變動項：150 億與 70 億美元相差約 80 億營收，以 30% 營益率、13% 稅率假設計約每股 2 美元，再加上終端倍數由 15 倍降到 11 至 12 倍，合計約三成價值（自行估算）。","if_happens":"資料中心 FY29 路徑下修到 70 億美元以下，基本情境改用 Bear 倍數，持股清倉，等新客戶實績再重做判斷。","how_monitor":"每季法說的資料中心營收與 FY28 訂單覆蓋說法；AWS 合作內容變動；第三家客戶是否轉為實質營收。","probability":"12 至 24 個月約 20%，依據是兩案已有採購訂單且為多世代合作，但客製矽向來多源採購。"}},"appendix_a":{"growth_durability":6,"quality_score":6,"ai_risk":"🟡","long_term_confidence":"中","fpe_fy2":12.87,"peg_fy2":0.4,"stress":{"pass":null,"total":null}},"eps_meta":{"base_eps_path":{"FY2026A":12.7,"FY2027E":10.16,"FY2028E":12.85,"FY2029E":17.84},"fy_end_month":9,"eps_basis":"FY2027E 至 FY2029E 為 Koyfin 共識，與法說指引對照屬非 GAAP 口徑；FY2026A 12.70 美元是 GAAP 稀釋 EPS，含非營業或稅務項目，與共識不同口徑，FY26 非 GAAP 全年 EPS 事實表未涵蓋。"},"catalysts":[{"date":"2027-02","date_precision":"month","type":"guidance","event":"FY27 第一季財報與 3 月季指引","impact":"高","watch":"資料中心是否達 6.5 億美元、3 月季營收指引方向"},{"date":"2027-04","date_precision":"month","type":"guidance","event":"FY27 第二季財報","impact":"高","watch":"資料中心是否達 10 億美元、漲價是否開始反映在毛利率"},{"date":"2027-06","date_precision":"month","type":"product","event":"首款 HBC 產品 AI250 推出","impact":"中","watch":"商品矽客戶是否轉為訂單"},{"date":"2027-09","date_precision":"quarter","type":"product","event":"SpaceX 地面 5G 網路開始貢獻營收","impact":"中","watch":"FY27 年底起的營收規模"},{"date":null,"type":"other","event":"Arm 案補救階段裁定","impact":"中","watch":"是否影響 Oryon CPU 出貨或授權成本"}],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8(val爭議)","pacing":[],"holding_cap":null,"audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場對 FY29 目標打折合理，但把合約鎖到 FY30 週期的授權年金與已實現的車用成長一起打折：現價以 15 倍終端、年報酬 10% 反推，只要求 FY31 EPS 約 16 美元，低於公司 FY29 目標。"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟢', val='🟡', moat_trend='→', week26=-23.81, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position='早循環', moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈機械讀數判定不可用，baseline rows 8/9/9b/10 的估值條件視為不可判 → 落 row8 觀望（保守方向）","hit":true,"basis":"val_denominator_disputed=True, val(機械讀數)='🟡'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"requires_critic":[]}}
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
