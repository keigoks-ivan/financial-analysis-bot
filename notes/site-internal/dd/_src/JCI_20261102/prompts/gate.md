你是 DD 管線 v20 的判斷層閘（gate），標的 JCI（20261102）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（36 條）
- `f_kpi0_gaap`（q1_business）｜營收（GAAP）＝7113 USD m｜期間與口徑：Q4 FY2026（季末 2026-09-30，公告於 2026-10-27）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q4/FY26 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000833444/000083344426000101/q4exh991xq4fy26earningsrel.htm（numbers.latest_quarter_kpis.items[0]，as_of Q4 FY2026（季末 2026-09-30，公告於 2026-10-27））
- `f_kpi1_adjusted_ebit`（q1_business）｜調整後營業利益（Adjusted EBIT）＝1299 USD m｜期間與口徑：Q4 FY2026（季末 2026-09-30，公告於 2026-10-27）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q4/FY26 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000833444/000083344426000101/q4exh991xq4fy26earningsrel.htm（numbers.latest_quarter_kpis.items[1]，as_of Q4 FY2026（季末 2026-09-30，公告於 2026-10-27））
- `f_kpi2_segment_ebita`（q1_business）｜調整後 Segment EBITA 利益率＝20.6 %｜期間與口徑：Q4 FY2026（季末 2026-09-30，公告於 2026-10-27）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q4/FY26 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000833444/000083344426000101/q4exh991xq4fy26earningsrel.htm（numbers.latest_quarter_kpis.items[2]，as_of Q4 FY2026（季末 2026-09-30，公告於 2026-10-27））
- `f_kpi3_gaap_consolidated_ebit`（q1_business）｜GAAP 營業利益（Consolidated EBIT）＝1145 USD m｜期間與口徑：Q4 FY2026（季末 2026-09-30，公告於 2026-10-27）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q4/FY26 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000833444/000083344426000101/q4exh991xq4fy26earningsrel.htm（numbers.latest_quarter_kpis.items[3]，as_of Q4 FY2026（季末 2026-09-30，公告於 2026-10-27））
- `f_kpi6_eps`（q1_business）｜調整後 EPS＝1.66 USD｜期間與口徑：Q4 FY2026（季末 2026-09-30，公告於 2026-10-27）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q4/FY26 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000833444/000083344426000101/q4exh991xq4fy26earningsrel.htm（numbers.latest_quarter_kpis.items[6]，as_of Q4 FY2026（季末 2026-09-30，公告於 2026-10-27））
- `f_kpi7_organic_orders_yoy`（q1_business）｜訂單（Organic orders YoY）＝44 %｜期間與口徑：Q4 FY2026（季末 2026-09-30，公告於 2026-10-27）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q4/FY26 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000833444/000083344426000101/q4exh991xq4fy26earningsrel.htm（numbers.latest_quarter_kpis.items[7]，as_of Q4 FY2026（季末 2026-09-30，公告於 2026-10-27））
- `f_kpi8_backlog`（q1_business）｜Backlog＝23.0 USD bn｜期間與口徑：Q4 FY2026（季末 2026-09-30，公告於 2026-10-27）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q4/FY26 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000833444/000083344426000101/q4exh991xq4fy26earningsrel.htm（numbers.latest_quarter_kpis.items[8]，as_of Q4 FY2026（季末 2026-09-30，公告於 2026-10-27））
- `f_peer_jci_gross_margin_pct`（q2_moat）｜JCI 毛利率＝36.65 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.JCI.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_jci_operating_margin_pct`（q2_moat）｜JCI 營業利益率＝14.45 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.JCI.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_tt_operating_margin_pct`（q2_moat）｜TT 營業利益率＝17.92 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.TT.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_jci_fcf_margin_pct`（q2_moat）｜JCI FCF 利潤率＝6.64 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.JCI.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_tt_fcf_margin_pct`（q2_moat）｜TT FCF 利潤率＝16.43 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.TT.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_carr_operating_margin_pct`（q2_moat）｜CARR 營業利益率＝8.05 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CARR.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_lii_operating_margin_pct`（q2_moat）｜LII 營業利益率＝19.94 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.LII.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_hon_operating_margin_pct`（q2_moat）｜HON 營業利益率＝16.2 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.HON.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝6.32 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-10-31）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝7.4 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-10-31）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝8.49 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-10-31）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝28330.51 USD m｜期間與口徑：2026-11-02／yfinance revenue_estimate 0y 平均（18 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-02）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝30680.49 USD m｜期間與口徑：2026-11-02／yfinance revenue_estimate +1y 平均（17 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-02）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi4_fcf`（q4_capital）｜自由現金流（FCF）＝1078 USD m｜期間與口徑：Q4 FY2026（季末 2026-09-30，公告於 2026-10-27）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q4/FY26 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000833444/000083344426000101/q4exh991xq4fy26earningsrel.htm（numbers.latest_quarter_kpis.items[4]，as_of Q4 FY2026（季末 2026-09-30，公告於 2026-10-27））
- `f_kpi5_sbc_equity_based_compens`（q4_capital）｜SBC（equity-based compensation）＝29 USD m｜期間與口徑：Q4 FY2026（季末 2026-09-30，公告於 2026-10-27）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q4/FY26 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000833444/000083344426000101/q4exh991xq4fy26earningsrel.htm（numbers.latest_quarter_kpis.items[5]，as_of Q4 FY2026（季末 2026-09-30，公告於 2026-10-27））
- `f_peer_lii_fcf_margin_pct`（q2_moat）｜LII FCF 利潤率＝15.34 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.LII.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝8659.0 USD m｜期間與口徑：2026-11-02／yfinance 最新一季：總債務 9277.0、現金 618.0（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-02）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝0.805 %｜期間與口徑：2026-11-02／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-11-02）
- `f_ma_w52`（q5_valuation）｜52 週均線＝135.46 USD｜期間與口徑：2026-11-02／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-02）
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝149.03 USD｜期間與口徑：2026-10-30（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-10-30（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝23.58 x｜期間與口徑：2026-10-31／分母＝FY1 EPS 6.32，分子＝快照價 149.03｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-10-31）
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝27.16 %｜期間與口徑：2026-07-30 → 2026-10-31／FY1 共識 EPS 4.97 → 6.32（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-10-31）
- `f_consensus_rev_fy1_pct`（q5_valuation）｜FY1 共識修正＝0.0 %｜期間與口徑：2026-10-31／兩份 Koyfin 快照之間的 EPS 修正幅度（6.32 → 6.32）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.fy1.revision_pct，as_of 2026-10-31）
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝31.57 x｜期間與口徑：2026-10-30（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-10-30（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝100.0 %｜期間與口徑：2026-10-30（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-10-30（RTH 收盤，UTC））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝3.52 x｜期間與口徑：2026-10-30（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-10-30（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝3.85 x｜期間與口徑：2026-10-30（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-10-30（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝100.0 %｜期間與口徑：2026-10-30（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-10-30（RTH 收盤，UTC））
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝605.74 m shares｜期間與口徑：2026-11-02／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-11-02）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null

### findings_digest 中方向為負或來源衝突的條目（9 條）
- `competitive_share_entrants#1`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K 風險因子指出 AI 技術快速演進，若未跟上，競爭地位與經營結果可能受損。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A Risk Factors（as_of 2025-11-14）｜affects：moat_trend、thesis.R
- `regulatory_antitrust#2`（regulatory_antitrust｜方向 -｜狀態 ok）：香港競爭事務委員會對 Johnson Controls Hong Kong、其母公司及一名前員工提起第二宗競爭審裁處程序，指控 2015-12 至 2018-06 空調工程定價、分割市場及圍標，違反第一行為守則，涉案工程逾 HK$3 billion。
  - 來源：The Standard (HK) - Poon company in hot water again over alleged cartel（as_of 2023-05-24）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：FY2025 10-K：關稅與對等關稅推升原物料成本，公司至今大致能抵銷已實施關稅的影響；若新增關稅，可能因銷量下降與銷貨成本上升而衝擊營收成長與利潤率。
  - 來源：SEC EDGAR 10-K FY2025 Item 1（as_of 2025-11-14）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：JCI 10-K風險因素：關鍵零件（半導體、含稀土零件）來自單一或少數供應商，另有關稅涵蓋中國、墨西哥等
  - 來源：JCI Form 10-K FY2025, SEC（as_of 2025-11-05）｜affects：thesis.R、decision_inputs.bear
- `end_markets#2`（end_markets｜方向 -｜狀態 ok）：Mixed demand outside data centers and concern about durability of data-center cooling boom and new competitors
  - 來源：Nasdaq, JCI Q3 earnings call highlights（as_of 2026-07-30）｜affects：thesis.R、decision_inputs.bear
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：JCI 10-K 風險因子：若無法敏捷回應新產品/技術（能效、液冷、AI/ML）的顛覆，業務與財務可能受不利影響
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2025-11-14）｜affects：moat_trend、thesis.R
- `substitute_technology#1`（substitute_technology｜方向 -｜狀態 ok）：Nvidia CEO 於 2026 年 1 月稱次世代晶片可能大幅降低資料中心冷卻需求；資料中心占 JCI 銷售比重有限
  - 來源：Webull news（as_of 2026-01-15）｜affects：thesis.R、decision_inputs.bear
- `major_events#1`（major_events｜方向 -｜狀態 ok）：AFFF（消防泡沫）PFAS 訴訟：Chemguard 與 Tyco Fire Products 被列為 49 件待審聯邦集體訴訟被告，另有 7 件加拿大集體訴訟
  - 來源：SEC EDGAR 10-K FY2025 Note 20（as_of 2025-11-14）｜affects：decision_inputs.bear、thesis.R
- `lawsuit_class_action#1`（lawsuit_class_action｜方向 -｜狀態 ok）：AFFF PFAS 集體訴訟 49 件待審（美）＋7 件加拿大
  - 來源：SEC EDGAR 10-K FY2025 Note 20（as_of 2025-11-14）｜affects：decision_inputs.bear、thesis.R

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 9 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/JCI_20261102/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":292.5,"bear_5y_price":99.0,"p_bull_pct":25,"p_bear_pct":30,"upside_5y_pct":37.4,"ev5y_pct":30.8,"irr_base_pct":6.6,"asym_ratio":2.4,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":6.32,"pe":23.58,"basis":"FY2027 共識調整後 EPS（下一個完整財年，前瞻口徑）；終端倍數同為前瞻口徑，視為對 FY2031 EPS 的前瞻倍數，五年報酬因此略保守。"},"eps":{"bull":[6.45,7.75,9.1,10.4,11.7],"base":[6.25,7.2,8.1,8.95,9.75],"bear":[6.05,6.0,5.85,6.2,6.6]},"pe":{"bull":25,"base":21,"bear":15},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0.805,"net_buyback":2.0},"second_stage":{"bull_cagr_pct":12,"base_cagr_pct":8},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### JCI_Q3_2026_Earnings_Call_20260729.md
- 2026-07-29｜CFO｜guidance：FY26 有機營收成長財測由約 6% 上調至約 8%（原話："expect organic revenue growth of approximately 8%, up from"）
- 2026-07-29｜CFO｜guidance：Q4 財測：有機營收成長與營運槓桿區間（原話："organic revenue growth of 9% to 10%, operating leverage of"）
- 2026-07-29｜CFO｜guidance：FY26 調整後 EPS 財測上調（原話："raising our adjusted EPS guidance to approximately $5.05"）
- 2026-07-29｜CFO｜guidance：FY26 自由現金流轉換率維持約 100%（原話："adjusted free cash flow conversion of approximately 100%"）
- 2026-07-29｜CFO｜guidance：FY27 具體財測留待下次法說（原話："too early to provide real specific fiscal year '27 guidance"）
- 2026-07-29｜CFO｜guidance：Q4 EMEA 預期極低個位數至持平（原話："EMEA land in very low single digit to flat in Q4"）
- 2026-07-29｜CEO｜guidance：中東假設近幾季情況無重大改變（原話："we can't predict the Middle East any better than you can"）
- 2026-07-29｜CFO｜margin：Q3 調整後 EBIT margin 擴張 260bp（原話："while adjusted EBIT margin expanded 260"）
- 2026-07-29｜CFO｜margin：管理層說明營運槓桿未來 12–24 個月仍高於 30%（原話："higher than 30% operating leverage over the next 12 to 18"）
- 2026-07-29｜CFO｜margin：資料中心系統占比提高造成設備組合 margin 小幅逆風（原話："a smaller equipment mix margin, a small headwind"）
- 2026-07-29｜CFO｜commitment：重申長期算式：營收高個位數成長、增量至少 30%（原話："top line growth and at least 30% of incremental"）
- 2026-07-29｜CEO｜commitment：Gemba Day 長期算式含營運槓桿、EPS 與 FCF 轉換（原話："operating leverage of more than 30%, double-digit adjusted"）
- 2026-07-29｜CFO｜commitment：資料中心營收占比 3–5 年內成為公司三分之一（原話："becoming 1/3 of the company from a revenue standpoint"）
- 2026-07-29｜CFO｜commitment：服務目標回到中至高個位數成長（原話："returning to mid- to higher single-digit growth is the focus"）
- 2026-07-29｜CEO｜commitment：Armada 相關機會預告未來幾季再談（原話："within the next couple of quarters, we'll be able to talk"）
- 2026-07-29｜CEO｜customer：訂單與積壓訂單：動能超過 25%、積壓創高（原話："backlog grew more than 30% to a record $21 billion"）
- 2026-07-29｜CFO｜customer：系統訂單成長 40%（原話："Systems order grew 40%"）
- 2026-07-29｜CFO｜customer：FY26 資料中心占營收比重預估（原話："land in the high teens as a mix of percentage of revenue"）
- 2026-07-29｜CEO｜customer：對 AI 需求可持續性的看法（原話："the output of the data centers is going to continue to grow"）
- 2026-07-29｜CEO｜customer：資料中心客戶未見需求受新聞影響（原話："seen any impact on demand at all from what you see in"）
- 2026-07-29｜CFO｜product：CDU 預計本季開始出貨（原話："We are going to start shipping actually this quarter."）
- 2026-07-29｜CFO｜product：CDU 商機 pipeline 達 10 億美元（原話："has now reached $1 billion"）
- 2026-07-29｜CEO｜product：取得 NVIDIA 認證（原話："we had the recent NVIDIA certification as well"）
- 2026-07-29｜CEO｜product：吸收式冷卻機參考設計可降低冷卻用電約 44%（原話："reduce cooling electrical demand by approximately 44%"）
- 2026-07-29｜CEO｜product：持續提高每百萬瓦的營收含量（原話："continue to work on increasing our dollars per megawatt"）
- 2026-07-29｜CEO｜product：管理層看法：冷水機需求下降之說影響極小（原話："going to be a very, very nominal impact, if any"）
- 2026-07-29｜CEO｜competition：稱在其聚焦類別中正在取得市占（原話："We think we are for the categories that we focus on."）
- 2026-07-29｜CEO｜competition：大型資料中心客戶很少只選單一夥伴（原話："rarely just pick one partner that they design in with"）
- 2026-07-29｜CFO｜competition：安全業務差異化較低，出現競爭性量壓力（原話："a little bit less differentiated than, for example, our HVAC"）
- 2026-07-29｜CFO｜competition：安全業務競爭性量壓力（原話："created a little bit of a competitive volume pressure"）
- 2026-07-29｜CFO｜risk：美洲服務積壓訂單下滑歸因於安全業務定價與轉向成長（原話："pivoting towards growth and the dynamic of price"）
- 2026-07-29｜CFO｜risk：Fire & Security 市場被描述為非高成長市場（原話："a high single-digit or double-digit growth market"）
- 2026-07-29｜CEO｜risk：供應鏈偶有瓶頸、仰賴外部供應商（原話："we depend on external vendors as well"）
- 2026-07-29｜CEO｜risk：產能：Applied HVAC 爬坡略快於預期，仍需新增實體產能（原話："we're also going to have to add some new physical"）
- 2026-07-29｜CFO｜capital_allocation：淨負債比降至 1.9x，低於長期目標區間（原話："Net debt declined to 1.9x, below our long-term target range"）
- 2026-07-29｜CFO｜capital_allocation：現金狀況使公司更能投資業務（原話："We are now better positioned to invest in the business"）
- 2026-07-29｜CEO｜capital_allocation：電力端可能以夥伴或外科手術式併購擴充（原話："surgically expand our capabilities there"）
- 2026-07-29｜CEO｜capital_allocation：策略檢討進展但無時程（原話："we continue to make progress, and we will keep you posted"）
- 2026-07-29｜CFO｜capital_allocation：持續出售住宅訂閱業務（原話："we have a few more to go"）

### JCI_Shareholder_Analyst_Call_Johnson_Controls_International_plc_20260601.md
- 2026-06-01｜CFO Marc Vandiepenbeeck｜guidance：長期有機成長目標由中個位數提高到高個位數（原話："a clear path to a high single-digit organic growth overall"）
- 2026-06-01｜CFO Marc Vandiepenbeeck｜guidance：舊長期算式的有機成長口徑為中個位數（原話："pegged around mid-single digit"）
- 2026-06-01｜CFO Marc Vandiepenbeeck｜guidance：營運槓桿（增量利潤率）長期口徑為 30% 以上（原話："leverage at 30-plus percent from where we were"）
- 2026-06-01｜CFO Marc Vandiepenbeeck｜guidance：未來 12–18 個月增量利潤率預期高於 30%（原話："the next 12 or 18 months, where we will do better than 30%"）
- 2026-06-01｜CFO Marc Vandiepenbeeck｜guidance：CFO 對分析師提出的 50% 增量利潤率說難以辯護（原話："50% is going to be hard to defend at this stage"）
- 2026-06-01｜CFO Marc Vandiepenbeeck｜guidance：資料中心 2025 年約占營收 12%（原話："Data center last year in 2025 was about 12% of our revenue"）
- 2026-06-01｜CFO Marc Vandiepenbeeck｜guidance：預期五年內資料中心約占公司三分之一（原話："it will be about 1/3 of the company within the next 5 years"）
- 2026-06-01｜CFO Marc Vandiepenbeeck｜guidance：服務業務過去中至高個位數成長，目標提高到更高的個位數（原話："through a better productization of our service offering"）
- 2026-06-01｜CFO Marc Vandiepenbeeck｜commitment：仍承諾 EPS 雙位數成長（原話："double-digit growth in our EPS"）
- 2026-06-01｜CFO Marc Vandiepenbeeck｜commitment：維持 95%–100% 自由現金流轉換率（原話："performing between 95% and 100% free cash flow conversion"）
- 2026-06-01｜CFO Marc Vandiepenbeeck｜commitment：承諾將 100% 自由現金流還給股東（原話："we are committed to returning 100% of our free cash flow"）
- 2026-06-01｜CFO Marc Vandiepenbeeck｜capital_allocation：管理層稱已讓資本支出與營收成長脫鉤（原話："we have decoupled the need for capital expenditure"）
- 2026-06-01｜CFO Marc Vandiepenbeeck｜capital_allocation：管理層稱未來某時點仍需要實體（hard）產能（原話："at some point, hard capacity will be needed"）
- 2026-06-01｜CFO Marc Vandiepenbeeck｜capital_allocation：併購管線健康（原話："We have a very healthy pipeline of M&A opportunities"）
- 2026-06-01｜CEO Joakim Weidemanis｜capital_allocation：補齊熱管理鏈不需大筆資本投入，可能有收購（原話："we don't need any major capital deployment"）
- 2026-06-01｜CEO Joakim Weidemanis｜capital_allocation：投資組合無新說法，維持股東導向評估（原話："we don't have any new news versus what we've spoken about"）
- 2026-06-01｜CFO Marc Vandiepenbeeck｜margin：服務利潤率有機會從 40% 多再往上（原話："from a 40s percent margin to something greater over time"）
- 2026-06-01｜CFO Marc Vandiepenbeeck｜margin：庫存改善帶來的利潤與現金效益（原話："overall, it's hundreds of basis points"）
- 2026-06-01｜CFO Marc Vandiepenbeeck｜margin：ACE 工廠準時交貨率由 43% 到 100%（原話："43% on-time delivery 4 months ago, 100% on-time delivery"）
- 2026-06-01｜CFO Marc Vandiepenbeeck｜margin：ACE 工廠改善所需資本支出很少（原話："very little CapEx required to achieve that"）
- 2026-06-01｜CEO Joakim Weidemanis｜margin：ACE 工廠產能提升至四倍（原話："we're now able to quadruple the capacity of that"）
- 2026-06-01｜CEO Joakim Weidemanis｜margin：管理層稱不需要 44 座工廠（原話："probably not going to need 44 plants in the future"）
- 2026-06-01｜CEO Joakim Weidemanis｜margin：銷售與服務端仍會增員，G&A 不增（原話："We'll continue to add people in some functions"）
- 2026-06-01｜CFO Marc Vandiepenbeeck｜margin：現場業務賣方與客戶相處時間倍增（原話："we managed to double the time those sellers are able"）
- 2026-06-01｜CEO Joakim Weidemanis｜customer：訂單與積壓訂單創新高（原話："Our backlog is at record levels"）
- 2026-06-01｜CFO Marc Vandiepenbeeck｜customer：資料中心客戶週期汰換速度較快（原話："churn time of a data center customer is about 60% faster"）
- 2026-06-01｜CEO Joakim Weidemanis｜customer：資料中心服務合約初始附加率高於產業平均（原話："the initial attach rate of service contracts is much"）
- 2026-06-01｜CEO Joakim Weidemanis｜customer：主要資料中心客戶每週派工程師共同創新（原話："we have a major data center customer, hyperscaler or colo"）
- 2026-06-01｜CEO Joakim Weidemanis｜customer：目前沒有客戶從晶片端整套採購熱管理（原話："I couldn't think of a single example where somebody"）
- 2026-06-01｜CEO Joakim Weidemanis｜product：Alloy 技術將用於差異化 CDU，預計一年內上市（原話："That will happen within the next year in terms of when it"）
- 2026-06-01｜CFO Marc Vandiepenbeeck｜product：每台冷卻器能耗與客戶成本的下降幅度（原話："chiller that provide 50% less consumption, that are 25%"）
- 2026-06-01｜CEO Joakim Weidemanis｜product：液冷資料中心仍加裝更多空氣處理設備（原話："there are even more air handling"）
- 2026-06-01｜CEO Joakim Weidemanis｜competition：現場團隊規模為多數競爭對手兩倍以上（原話："twice the field footprint than many of the other people"）
- 2026-06-01｜CFO Marc Vandiepenbeeck｜competition：風冷與水冷冷卻器市場結構與18個月前預期不同（原話："people anticipated water to grow as a bigger share"）
- 2026-06-01｜CEO Joakim Weidemanis｜risk：全面導入需時，不能六個月內複製到各處（原話："can't copy paste and do everything in 6 months"）
- 2026-06-01｜CEO Joakim Weidemanis｜risk：CEO 自認過去未能快速釋放潛力（原話："have we really unlocked that at speed over the last years?"）
- 2026-06-01｜CEO Joakim Weidemanis｜risk：全公司約十萬人，轉型需時（原話："if you have 100,000 people, it takes a little while"）
- 2026-06-01｜CEO Joakim Weidemanis｜risk：CEO 稱成果已開始反映在損益表（原話："results are already starting to show up in the P&L"）

### 問答異常語氣（迴避／改口／保留）
- JCI_Q3_2026_Earnings_Call_20260729.md｜問：Ritchie：FY27 已有多少積壓訂單確定會在 FY27 出貨｜答法：CFO 回答資料中心占比與長期占比，未給 FY27 出貨比例數字
- JCI_Q3_2026_Earnings_Call_20260729.md｜問：Obin：Armada 模組產品的 TAM 與是否墊高 margin｜答法：CEO 稱 TAM 形成中而不給數字，未回答 margin 是否增厚
- JCI_Q3_2026_Earnings_Call_20260729.md｜問：Obin：策略檢討的時程｜答法：CEO 只說持續進展、會再通知，未給時程
- JCI_Q3_2026_Earnings_Call_20260729.md｜問：Mehrotra：Applied HVAC 能否進一步加速｜答法：CEO 談 pipeline 與產能，未直接給成長數字
- JCI_Q3_2026_Earnings_Call_20260729.md｜問：Snyder：冷水機、空氣處理、CDU 各自含量變動幅度｜答法：CEO 談方向，未提供各項幅度數字
- JCI_Shareholder_Analyst_Call_Johnson_Controls_International_plc_20260601.md｜問：Julian Mitchell：高個位數有機成長是否意味不需大型divest｜答法：回覆「沒有新消息」，改談投資組合像運動隊各有角色，未正面回答
- JCI_Shareholder_Analyst_Call_Johnson_Controls_International_plc_20260601.md｜問：Julian Mitchell：液冷如何影響設備汰換率｜答法：CEO 稱需要再想想，反問分析師看法，未給答案
- JCI_Shareholder_Analyst_Call_Johnson_Controls_International_plc_20260601.md｜問：Amit Mehrotra：增量利潤率30%是否保守｜答法：未給新數字，稱長期算式有「+」，近12–18個月會更好，未量化
- JCI_Shareholder_Analyst_Call_Johnson_Controls_International_plc_20260601.md｜問：Joe Ritchie：訂單轉成長的能見度｜答法：回覆訂單與積壓創新高、整體看好，未給轉換節奏或數字

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 3 | 3 |
| customer_second_source | found | 1 | 1 |
| customer_concentration_credit | found | 2 | 2 |
| supply_demand_durability | found | 3 | 3 |
| regulatory_antitrust | found | 3 | 3 |
| reg_tariff_export | found | 4 | 1 |
| geo_supply_chain | found | 2 | 2 |
| end_markets | found | 3 | 3 |
| substitute_technology | found | 2 | 1 |
| channel_business_model_shift | found | 2 | 2 |
| capital_markets_pricing | found | 5 | 3 |
| major_events | found | 4 | 4 |

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260518","verdict":"A 觀望偏進場·thesis 完整但短 R:R 0.5x 偏緊，建議分批 / 等 BB 中軌 $132 或 Fwd PE 24x ~$135 回測","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"Data Center thermal chain attach rate 結構性上升 + JCI share gain","columns":{"2Y 驗證點":"FY27 backlog 仍 > $22B + Applied HVAC 業務段 organic +15%/年","5Y 驗證點":"FY29 Adj EPS > $7.5（5Y CAGR 14%+）；ROIC 站回 10%+","10Y 驗證點":"FY35 Adj EPS > $14；ROIC stably > 13%","具體數字門檻":"Applied HVAC 業務段 organic growth ≥ 15%/年 至 FY27；Data Center 在 Applied HVAC 占比逐季提升","信息來源":"JCI 法說會 Q2/Q3 FY26 + Goldman Sachs Industrial 研究 ($154 PT，2026 Mar)","漂移觸發條件":"連 2 季 Applied HVAC organic"}},{"id":"H2","text":"Weidemanis 重整兌現：3 段式 operating model 重組釋放 efficiency","columns":{"2Y 驗證點":"FY27 Operating Margin > 13.5%（FY25 12.0% → FY26 estimate 13.0%）","5Y 驗證點":"FY29 ROIC > 10%；Adj FCF conversion > 100% sustained","10Y 驗證點":"FY35 ROIC > 13%（Danaher track 對標）","具體數字門檻":"FY26 Operating Margin guidance ≥ 13%；FY27 ROIC ≥ 8.5%","信息來源":"FY26 Q2 法說會 Weidemanis 重整進度 + Danaher 過去 5 年 track（10-K）","漂移觸發條件":"FY27 ROIC"}},{"id":"H3","text":"估值維持 5Y 中位區間（Fwd PE 24-28x），不被市場壓縮回 peer 19x","columns":{"2Y 驗證點":"NTM Fwd PE 在 24-30x 區間 sustained（不下破 23x）","5Y 驗證點":"5Y Fwd PE 中位仍 ≥ 25x","10Y 驗證點":"—（10Y 估值難以預測）","具體數字門檻":"NTM Fwd PE 不破 23x（vs peer 中位 19x，溢價 ≥ 20%）","信息來源":"Macrotrends 5Y PE 歷史 + Trefis 同業比較研究（2026 Feb）","漂移觸發條件":"連 2 季 Fwd PE"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"Data Center capex cycle 提前見頂（GPU 供應飽和、power 約束限制新建、AI 投資 ROI 質疑）","columns":{"對應假設":"H1","時間尺度":"🔥 中期（4-6 季）","監測指標":"Hyperscaler capex 季度 YoY、JCI 訂單 Applied HVAC 業務段 organic growth","警戒閾值":"JCI Applied HVAC organic"}},{"id":"R2","text":"Weidemanis 三段式重整卡關（中層抵制、文化錯位、執行延期）","columns":{"對應假設":"H2","時間尺度":"🐢 長期（2+ 年慢變數）","監測指標":"季度 Adj EPS Beat/Miss、Operating Margin 軌跡、ROIC 滾動值","警戒閾值":"FY27 Operating Margin"}},{"id":"R3","text":"估值溢價收斂回 peer 中位（同業 TT/CARR 也搶 AI 順風股，JCI 失去獨特性）","columns":{"對應假設":"H3","時間尺度":"⚡ 短期（1-2 季）","監測指標":"JCI vs TT/CARR Fwd PE 差距、買方 sell-side downgrade 數量","警戒閾值":"JCI Fwd PE 跌至 22x 以下 + sell-side downgrade ≥ 3 家"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"A","val":"🟡","ma":"✅","trap":"🟢","moat_trend":"→","runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":143.08,"archetype":null,"cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"JCI","date":"2026-11-02","schema":"v15.0","contract":"v19","company_name":"Johnson Controls International plc"},"oneliner":"資料中心冷卻訂單年增44%、積壓230億美元，FY2027指引EPS再成長約兩成；生意在變好，但前瞻本益比約23.6倍已反映大半，資料中心占比升高也讓獲利更像景氣循環，不追，等135美元附近且積壓仍年增再分批。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/JCI_20261102/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/JCI_20261102/scenario.json","answers":{"q1_business":{"verdict":"賺商用建築與資料中心業主的錢：先賣冷卻機、控制與消防保全系統（Q4 有機 +13%），再靠裝機基礎收服務費（+8%）；錢卡在資料中心熱管理這一節點，冷卻機五大子系統自製，是 FY2026 利潤率擴張的主力。","reasoning":"分部（Q4 FY2026，公司新聞稿 2026-10-27）：美洲營收 49.30 億美元、有機 +14%、Segment EBITA 利益率 22%；EMEA 13.12 億美元、有機 +3%、16.4%；APAC 8.71 億美元、+12%、19%；合計 71.13 億美元。調整後 EBIT 12.99 億美元、利益率約 18%（+300bp），GAAP EBIT 11.45 億美元；最新一季毛利率事實表未涵蓋，近四季毛利率 36.65%（財務長稱正常約 37%）。資料中心占營收：FY2025 約 12%（2026-06-01 投資人日財務長）、FY2026 高十幾%（2026-07-29 法說），目標三到五年三分之一。單點依賴：無單一客戶超過 10%（FY2025 10-K），但終端需求越來越集中在資料中心資本支出，且半導體與稀土零件有單一或少數供應商。景氣時鐘 II（擴張）：Q4 有機訂單 +44%、三區利潤率同步擴張、JCI 與同業開始擴產（FY2027 資本支出約 9 億美元），尚未看到產能過剩或價格戰。產業態勢三軸：A 競爭——資料中心新進者與客戶多供應商策略，未見份額流失；B 結構——資料中心、半導體、生技等關鍵任務需求轉好；C 其他——液冷等替代技術與關稅。裁決：雙向拉鋸（B 軸轉好對 C 軸替代技術），依據為 Q4 訂單數據與 FY2025 10-K 風險因子。","fact_refs":["f_kpi0_gaap","f_kpi1_adjusted_ebit","f_kpi2_segment_ebita","f_kpi3_gaap_consolidated_ebit","f_kpi6_eps","f_kpi7_organic_orders_yoy","f_kpi8_backlog","f_peer_jci_gross_margin_pct","f_peer_jci_operating_margin_pct"],"verdict_values":{"revenue_quality":"系統（按專案認列）＋服務（續約型）；Q4 系統有機 +13%、服務 +8%，組合往系統偏；積壓訂單 230 億美元，管理層預估 70–80% 在 12 個月內轉營收；無單一客戶占比超過 10%。","unit_econ_note":"核心單位是每百萬瓦含量：冷卻機為主，加上 CDU、冷板、控制與模組化資料中心；管理層稱模組化的每百萬瓦含量高於大型園區，未量化。價格/成本為正但通膨回收稀釋毛利率（財務長 Q4 法說）。","archetype":{"primary":"品質複利成長","secondary":"循環/商品","confidence":"中","fingerprint":"訂單與積壓領先營收、營運槓桿逾 30% 驅動 EPS、資料中心資本支出占比升高"},"industry":{"clock_phase":"II","sd_verdict_source":"供需 durability：兩年內結構性持久（積壓 230 億美元、管理層稱需求延伸到 FY2027 以後、客戶提前一年下單），五年以上屬週期性、可能反轉；供給可逆性中（JCI 與同業同步擴產）。來源：Q4 FY2026 新聞稿與法說。","bargaining":{"up":"上游鋼、銅、鋁與半導體、稀土零件；冷卻機五大子系統自製、控制銷貨成本，但半導體與稀土零件有單一或少數供應商（FY2025 10-K），議價力中等偏強。","down":"超大型雲端與託管業者議價力強、很少只選一家（Q3 法說），但無單一客戶占比超過 10%；交貨時程受客戶電力與電氣基礎設施限制主導。","geo":"區域內生產供應區域；美洲占 Q4 營收 69%、占積壓約 77%；已實施關稅大致抵銷（2026-03 季報），中東 2026 年受擾。"},"profit_pool_dir":"利潤池往資料中心熱管理移動：冷卻機之外延伸到 CDU、冷板、控制與模組化；消防保全利潤池停滯，住宅類已出售。","tam_table":{"expanded":false,"reason":"TAM、滲透率與利潤池占比事實表未涵蓋；管理層只給資料中心占營收比重（FY2025 約 12%、FY2026 高十幾%、三到五年三分之一）與 CDU 商機約 10 億美元，不足以展開五年利潤池表，這個缺口限制了跑道判斷的信心。"}}}},"q2_moat":{"verdict":"護城河 C 級、方向穩定：冷卻機子系統自製加上大規模現場服務網，執行力在變強，但近四季 GAAP 營業利益率仍比 TT 低約 3.5pp、FCF 利潤率低約 10pp，定價力只是穩定，晶片端改變散熱架構則是生態層威脅。","reasoning":"機制：冷卻機五大子系統自製（Q4 法說），供應吃緊時交期與品質是優勢；約 5 萬人現場銷售與技師，管理層稱是多數對手兩倍（2026-06-01 投資人日）；資料中心服務附加率高於平均。可證方向：對最強同業 TT，近四季 GAAP 營業利益率 14.45% 對 17.92%，FCF 利潤率 6.64% 對 16.43%；JCI 自己的營業利益率由 FY2022 9.75% 升到近四季 14.45%，但同業歷史值與投入資本事實表未涵蓋，無法證明差距收斂。執行力 8：Q4 三區利潤率全面擴張、有機成長加速到 12%、前一季財測全數兌現，但執行長自承過去幾年沒有快速釋放潛力；定價力 6：價格/成本為正但稀釋毛利率，保全業務差異化低、出現競爭性量壓（Q3 法說），資料中心大客戶很少只選一家。兩項平均 7，晶片端改變散熱架構屬生態層威脅扣 1 分，得 6，對應 C 級。升級路徑：與 TT 的 GAAP 營業利益率差距兩年內縮到 2pp 以內，且 CDU 與冷板商機轉成實際訂單。","fact_refs":["f_peer_jci_operating_margin_pct","f_peer_tt_operating_margin_pct","f_peer_jci_fcf_margin_pct","f_peer_tt_fcf_margin_pct","f_peer_carr_operating_margin_pct","f_peer_lii_operating_margin_pct","f_peer_hon_operating_margin_pct","f_peer_jci_gross_margin_pct","f_kpi2_segment_ebita","f_kpi7_organic_orders_yoy","f_kpi8_backlog"],"verdict_values":{"moat":{"mechanism":"冷卻機五大子系統自製的垂直整合＋約 5 萬人現場銷售與技師網＋大型裝機基礎帶來的服務續約；資料中心服務附加率高於平均。","execution":8,"pricing":6,"grade":"C","trend":"→","trend_evidence":"執行力擴大：Q4 三區利潤率全面擴張（美洲 22%、EMEA 16.4%、APAC 19%），調整後 EBIT 利益率 +300bp，前一季財測全數兌現；定價力穩定：價格/成本為正但稀釋毛利率，保全業務出現競爭性量壓；相對最強同業 TT 的 GAAP 營業利益率與 FCF 利潤率差距仍為負，同業歷史值事實表未涵蓋，無法證明差距收斂，故方向判穩定。","competitor_notes":[{"name":"TT","strategy_note":"商用 HVAC 最強對手，GAAP 營業利益率高約 3.5pp、FCF 利潤率高約 10pp，是 JCI 利潤率收斂的標竿。"},{"name":"CARR","strategy_note":"營業利益率約 8%、毛利率約 25%，同業最低；資料中心冷卻是直接競爭點，但獲利體質弱於 JCI。"},{"name":"LII","strategy_note":"以北美住宅與輕商用為主，營業利益率約 20% 最高，但 JCI 已出售住宅業務，重疊有限。"},{"name":"HON","strategy_note":"在建築自動化與控制層競爭，FCF 利潤率約 5% 低於 JCI；冷卻機不重疊。"},{"name":"Vertiv","strategy_note":"FY2025 10-K 點名的資料中心熱管理與電力對手，是液冷與晶片端參考設計的主要競爭者；財務數字事實表未涵蓋。"}],"threats":[{"level":"🔴","text":"散熱架構改變：液冷與次世代晶片可能降低冷卻機需求（NVIDIA 執行長 2026-01 說法、GTC Berlin 影片），JCI 10-K 自承若跟不上液冷變化會受不利影響；公司以 CDU、冷板、模組化擴大含量對沖。","p":"30%","evidence_refs":["substitute_technology#0","substitute_technology#1"]},{"level":"🟡","text":"技術步調：10-K 風險因子稱若跟不上 AI 技術快速演進，競爭地位與經營結果可能受損。","p":"20%","evidence_refs":["competitive_share_entrants#1"]},{"level":"🟡","text":"資料中心冷卻新進者與客戶多供應商策略；資料中心以外需求分化（Q3 法說報導）。","p":"30%","evidence_refs":["end_markets#2"]},{"level":"🟡","text":"保全業務差異化低、出現競爭性量壓，服務積壓下滑（Q3 法說財務長）。","p":"25%","evidence_refs":[]}],"roic_durability":{"quadrant":"高利益率×低周轉（判斷）：調整後 EBIT 利益率約 18%、GAAP 近四季 14.45%；Tyco 合併留下大量商譽壓低周轉。投入資本與當期 ROIC 事實表未涵蓋，象限為推斷。","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者（資料中心營運者）、決策者（設計與工程團隊）、付款者（業主）三角色都成立，散熱是需要不是想要，延後就無法上線算力；Q4 訂單 +44%、積壓 230 億美元。但急迫性不等於持久性：要解決的問題（散熱）會長期存在，公司目前的方案（冷卻機）可能被液冷改變組合，故給黃。"},{"item":"決策層級","level":"🟡","text":"替代性在單一資料中心設計案層級衡量：大型客戶很少只選一家（Q3 法說），NVIDIA 認證是入場券不是鎖定；轉換成本來自設計規格、交期與裝機後服務合約，但新案每次重新比價，漲價後流失率與續約率事實表未涵蓋。"},{"item":"價值鏈分配","level":"🟡","text":"晶片與電力是價值鏈最稀缺環節，散熱參考設計由晶片端主導，互補品往單一供應商收斂會壓縮散熱商定價空間；JCI 靠子系統自製控制成本，價格/成本為正但通膨回收稀釋毛利率（Q4 法說），分到的份額沒有變多。"},{"item":"社會容忍度","level":"🟡","text":"商用設備不受漲價的社會天花板限制，耗水爭議管理層稱閉迴路設計已解決；但消防泡沫 PFAS 集體訴訟（美國 49 件、加拿大 7 件，FY2025 10-K）顯示舊產品的社會與法律容忍度風險仍在。"}],"roiic":"事實表未涵蓋（缺投入資本、折舊攤銷、Alloy 收購金額）；判斷區間 30%–100%：低端＝一般新建產能，高端＝精實改造的軟性產能（管理層稱一座工廠產能四倍、不增資本）。","reinvest_rate":"約 10%：FY2027 指引調整後 FCF 轉換約 95%，隱含資本支出與營運資金淨再投資約占調整後淨利 5%，加補強型併購約 5%；管理層承諾 100% FCF 回饋，再投資空間受限。","endo_ceiling":6.0,"formula_note":"內生成長率＝增量報酬×再投資率＝30%–100%×約 10%＝約 3%–10%，取中段約 6%（單位：%/年）；以調整後淨利近似 NOPAT。不論取區間哪一端，共識三年 EPS 年複合約 18% 都超過天花板。"}}}},"q3_growth":{"verdict":"五年後跑道中等：資料中心占比三到五年走到三分之一，CDU、冷板、模組化與歐洲是第二段，但都綁同一個資料中心資本支出，不是獨立曲線；共識三年 EPS 年複合約 18% 遠高於內生天花板約 6%，缺口主要靠利潤率擴張與回購。","reasoning":"成長來源：量為主（資料中心冷卻機、CDU、模組化；Q4 有機訂單 +44%、積壓 230 億美元），組合與成本次之（FY2027 指引營運槓桿逾 30%、第一輪重組年化節省比 5 億美元目標多 1–1.5 億美元、第二輪 FY2029 年化約 6 億美元），價格只略正，淨回購約每年 2%。共識：FY2027 6.32、FY2028 7.40、FY2029 8.49（Koyfin 2026-10-31，EPS 家數事實表未涵蓋），自 FY2026 調整後約 5.16 起算三年年複合約 18%；前瞻 GAAP EPS 事實表未涵蓋。營收共識 FY2027 283.3 億、FY2028 306.8 億美元（18／17 位分析師），FY2028 營收 +8.3% 對 EPS +17%。內生天花板約 6%（見護城河段推導），缺口約 12pp：利潤率擴張約 8pp、淨回購約 2pp，其餘約 2pp 是既有產能吃滿資料中心訂單的週期貢獻，無法歸因於再投資，部分依賴 re-rate 不下修。跑道：雙位數成長約 3–5 年（管理層稱 FY2027–28 擴產目標是維持雙位數，但不代表永遠雙位數），TAM 與滲透率事實表未涵蓋。衰退訊號亮 1 個（EPS 成長高於營收逾 5pp），價值陷阱風險與長期成長性皆為中等。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_kpi7_organic_orders_yoy","f_kpi8_backlog","f_kpi6_eps"],"verdict_values":{"growth":{"driver_mix":"量（資料中心冷卻與液冷含量）為主；利潤率擴張（營運槓桿逾 30%、兩輪重組）次之；淨回購約 2%/年；價格略正但稀釋毛利率；併購僅補強型。","runway_years":"事實表未涵蓋 TAM 與滲透率；以資料中心占比三到五年到三分之一推，雙位數成長跑道約 3–5 年。","runway_post_y5":"🟡","endo_ceiling_basis":"內生天花板約 6%/年（區間 3–10%）＝增量報酬 30–100%×再投資率約 10%；共識三年 EPS 年複合約 18%（FY2026 調整後約 5.16 → FY2029 共識 8.49），缺口約 12pp：利潤率擴張約 8pp、淨回購約 2pp，約 2pp 屬資料中心週期帶來的產能利用率，無法歸因於再投資。","segments":[{"item":"美洲（Q4 FY2026）","value":"營收 49.30 億美元，有機 +14%；Segment EBITA 利益率 22%（+210bp）；訂單 +58%；積壓約 178 億美元（約占全公司 77%）。"},{"item":"EMEA","value":"營收 13.12 億美元，報表 −2%、有機 +3%；利益率 16.4%（+80bp）；消防保全比重高，中東 2026 年受擾，資料中心與半導體起步較晚。"},{"item":"APAC","value":"營收 8.71 億美元，+12%；利益率 19%（+110bp）；近兩季資料中心與半導體驅動力轉強。"},{"item":"系統對服務","value":"系統有機 +13%（資料中心冷卻機為主）；服務 +8%，保全服務仍在調整，管理層稱還需 1–2 季。"},{"item":"資料中心占比","value":"FY2025 約 12% → FY2026 高十幾% → 管理層目標三到五年三分之一；CDU 商機 10 億美元以上，只有一小部分轉成訂單。"}],"decay_signals":[{"signal":"毛利率連兩季年減","lit":false,"note":"近四季毛利率 36.65% 高於 FY2025 的 36.41%；最新一季毛利率事實表未涵蓋。"},{"signal":"核心市占近 12 個月縮減","lit":false,"note":"未見來源證實的份額下滑；保全業務有競爭量壓但非核心。"},{"signal":"主力產品提價後銷量下滑","lit":false,"note":"冷卻機訂單仍強，Q4 有機訂單 +44%。"},{"signal":"EPS 成長顯著高於營收","lit":true,"note":"共識 FY2028 EPS +17%（6.32→7.40）對營收 +8.3%（283.3→306.8 億美元），差約 9pp；FY2027 指引 EPS +21% 對有機營收 +11–12%。"},{"signal":"FCF/淨利 <0.75 連兩年","lit":false,"note":"FY2025 GAAP 0.29 受出售住宅業務利益墊高淨利；FY2022–24 為 0.94–0.98；FY2026 調整後轉換 103%。需盯 FY2027 GAAP 數字。"},{"signal":"SBC/營收 >5% 且上升","lit":false,"note":"Q4 SBC 2900 萬美元，約營收 0.4%。"},{"signal":"TAM 被替代技術壓縮","lit":false,"note":"液冷與次世代晶片降低冷卻機需求的說法尚未反映在訂單，列為觀察。"},{"signal":"產業估值倍數近 3 年系統性下移","lit":false,"note":"JCI 本益比與 EV/S 在近四個年度端點最高。"},{"signal":"維護性資本支出占 FCF >60%","lit":false,"note":"維護與成長資本支出拆分事實表未涵蓋，屬資料缺口。"},{"signal":"停止投資新產能且收入 3 年內下滑","lit":false,"note":"FY2027 資本支出升到約 9 億美元。"}],"trap_rating":"價值陷阱風險 🟡、長期成長性 🟡（亮 1 個）"}}},"q4_capital":{"verdict":"資本配置中等：SBC 幾乎不稀釋、回購照做但買在約 21–24 倍前瞻本益比不便宜；FY2026 回饋 25 億美元只占調整後 FCF 約 78%，低於投資人日 100% 的承諾；FY2027 資本支出升到約 9 億美元，GAAP FCF 利潤率仍遠落後同業。","reasoning":"FCF/淨利轉換：FY2026 調整後自由現金流 32 億美元、轉換 103%（Q4 法說）；GAAP 口徑 FY2022–24 為 0.94–0.98，FY2025 為 0.29（淨利含出售住宅業務利益）；近四季 GAAP FCF 利潤率 6.64%，TT 16.43%、LII 15.34%，調整後與 GAAP 落差大，拆解事實表未涵蓋。Q4 FCF 10.78 億美元。SBC：Q4 2900 萬美元，約營收 0.4%，年化約 1.2 億美元、約市值 0.13%。現金去向：FY2026 回購加股息 25 億美元，約調整後 FCF 的 78%，其餘用於降槓桿（淨負債比 1.8 倍，低於長期目標區間）與 Alloy 收購；投資人日（2026-06-01）財務長承諾 100% 自由現金流還給股東，FY2026 未達。FY2027 資本支出約 9 億美元、重組費用 FY2027–28 約 4 億美元、FCF 轉換降到約 95%。現金去向四分與債務到期結構事實表未涵蓋。計分卡三項：併購已實現報酬——Alloy 金額未揭露，無法計算；回購收益率——未過；SBC 淨稀釋——過。","fact_refs":["f_kpi4_fcf","f_kpi5_sbc_equity_based_compens","f_peer_jci_fcf_margin_pct","f_peer_tt_fcf_margin_pct","f_peer_lii_fcf_margin_pct","f_net_debt_m","f_dividend_yield_ttm","f_ma_w52","f_consensus_eps_fy1"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":true,"passed":null,"input":"Alloy Enterprises 收購（2026-05 完成）金額未揭露，已實現報酬無法計算；事實表未涵蓋。"},{"name":"buyback_yield","applicable":true,"passed":false,"input":"以 52 週均線 135.46 美元代理回購均價，FY2027 共識 EPS 6.32 計盈餘殖利率約 4.7%；十年期公債殖利率事實表未涵蓋，須低於約 2.7% 才過門檻，判未過。"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"Q4 SBC 2900 萬美元，年化約 1.2 億美元，約市值 0.13%，遠低於 1.5%，且有淨回購。"}],"grade":null},"governance":{"capital_returns":{"expanded":false,"reason":"成長以有機為主（FY2027 指引有機 11–12%），近一年唯一收購 Alloy 金額未揭露且屬補強型，成長不靠併購撐；FY2026 回購加股息 25 億美元已寫入理由，逐年回購均價與現金去向四分事實表未涵蓋。"}}}},"q5_valuation":{"verdict":"現價要求 FY2027 照指引成長約兩成、FY2028–29 維持中雙位數，且本益比守在 21 倍以上；前半段我信，後半段只信一半——資料中心占比升高會讓獲利更像景氣循環，倍數該往下修不是往上。合理偏滿，不追，等 135 美元附近。","reasoning":"前瞻本益比 23.58 倍＝149.03 ÷ FY2027 共識 6.32；FY2028 共識 7.40 對應約 20.1 倍。PEG＝23.58 ÷ 三年 EPS 年複合約 18%≈1.3，落在合理帶。歷史位置：trailing 本益比 31.6 倍、P/S 3.52 倍、EV/S 3.85 倍都在近四個年度端點的最高點（只有四點，不是五年分位，五年分位事實表未涵蓋）。同業前瞻倍數事實表未涵蓋，不做跨口徑對照。賣方目標價（2026-08 前後，各站日期不一）平均 144.9–162.1 美元，現價落在區間內，尚未反映 Q4 財報。共識修正：近三個月 FY1 由 4.97 升到 6.32（+27%）主要是財年滾動（FY1 由 FY2026 換成 FY2027），不是真實上修；財報後兩次快照 FY1–FY3 都沒變。情境：Base 終端 21 倍×FY2031 EPS 9.75≈205 美元；機率加權五年價格約 +31%，加股息與回購年化約 8%，屬中段。分母：調整後 EPS 排除兩輪重組，新一輪 FY2027–28 約 4 億美元，稅前每年每股約 0.33 美元，約 FY2027 EPS 的 5%，不構成分母爭議。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_3m_fy1_pct","f_consensus_rev_fy1_pct","f_pe_current","f_pe_percentile","f_ps_current","f_ev_s_current","f_ev_s_percentile","f_dividend_yield_ttm","f_shares_diluted_m"],"verdict_values":{"valuation":{"basis":"前瞻本益比（FY2027 共識調整後 EPS）＋PEG","peers":{"expanded":false,"reason":"同業前瞻本益比事實表未涵蓋（同業表只有毛利率、營業利益率、FCF 利潤率），不以跨口徑數字當估值錨。"},"fwd_pe":23.58,"peg":1.3,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"前瞻 23.6 倍、PEG 約 1.3 屬合理帶；但倍數在自身近四年最高、賣方均值目標與現價相近、機率加權年化約 8% → 合理偏滿。短期上檔＝FY2028 Base EPS 7.20×21.5 倍≈155 美元（+4%）；中期（三年）＝FY2030 Base EPS 8.95×21 倍≈188 美元（+26%）。五年分位事實表未涵蓋。","upside_short_pct":4,"upside_mid_pct":26,"denominator_disputed":false,"denominator_note":"調整後 EPS 排除重組與併購攤銷；新一輪重組 FY2027–28 約 4 億美元（稅前每股約 0.33 美元/年），約 FY2027 EPS 的 5%；連續兩輪重組代表這是半經常性成本，但幅度不足以推翻估值結論。"}}},"q6_how_wrong":{"verdict":"最可能看錯的地方：把資料中心兩三年的建置潮當成長期結構，同時付了接近自身歷史高點的倍數；生意沒有變壞，但 EPS 跑贏營收靠的是利潤率與景氣，價值陷阱風險中等。","reasoning":"反證三視角（見反證紀錄）：論點失敗——資料中心訂單消化、積壓轉年減，EPS 停在 6 美元附近、倍數壓到 15 倍；論點成功但股東經濟變差——資料中心占比升高讓獲利更景氣化，GAAP 現金流落後同業，PFAS 訴訟尾巴未量化；價格已反映太多——前瞻 23.6 倍在自身最高、賣方均值目標接近現價。衰退訊號亮 1 個（EPS 成長高於營收逾 5pp）。成長熄火測試：Base FY2029 EPS 8.10 之後成長降到 15%／10%／5%，給 22／18／14 倍 → 約 205／160／119 美元，對現價 +38%／+7%／−20%，三個裡兩個過。歷史最大回撤、PFAS 求償金額事實表未涵蓋。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_peer_jci_fcf_margin_pct","f_kpi8_backlog","f_pe_current","f_fwd_pe_latest"],"verdict_values":{"trap":{"verdict":"🟡","label":"EPS 跑贏營收＋資料中心集中度上升"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":6.32,"pe":23.58,"basis":"FY2027 共識調整後 EPS（下一個完整財年，前瞻口徑）；終端倍數同為前瞻口徑，視為對 FY2031 EPS 的前瞻倍數，五年報酬因此略保守。"},"eps":{"bull":[6.45,7.75,9.1,10.4,11.7],"base":[6.25,7.2,8.1,8.95,9.75],"bear":[6.05,6.0,5.85,6.2,6.6]},"pe":{"bull":25,"base":21,"bear":15},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0.8,"net_buyback":2.0},"second_stage":{"bull_cagr_pct":12,"base_cagr_pct":8},"max_dd":{"lo":-45,"hi":-30,"basis":"下緣 −45%：FY2028 EPS 跌到約 5.9（低於共識 7.40 約 20%）×前瞻 14 倍≈83 美元；上緣 −30%：FY2027 EPS 6.05（低於指引下緣）×17 倍≈103 美元。極端情境（15 倍×0.8＝12 倍、EPS 6.32×0.9×0.85≈4.8）約 58 美元屬尾部，不入範圍。歷史最大回撤事實表未涵蓋。","trigger_time":null},"basis":{"bull":"資料中心建置延續到 FY2030 以後，CDU、冷板、模組化放大每百萬瓦含量，歐洲跟上；有機營收年增 12–14%、營運槓桿維持逾 30%；終端 25 倍參照目前 23.6 倍加品質溢價。","base":"FY2027 照指引（中值 6.225）略高，FY2028 起資料中心成長放緩到高個位數，Intrusion 出售年化稀釋約 0.15 美元；重組節省兌現；終端 21 倍＝成長降到約 9% 的合理前瞻倍數，比現值低約 2.6 倍。","bear":"FY2028–29 資料中心訂單消化、積壓年減，營運槓桿反轉；重組節省撐住部分利潤；終端 15 倍＝成長熄火到約 5% 的前瞻倍數。"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"資料中心以外需求分化、市場擔心資料中心冷卻熱潮能否持續與新競爭者（Q3 法說報導）；管理層自己說客戶受電力與電氣基礎設施限制、交貨時程由客戶決定；積壓 230 億美元、訂單年增 44% 已是極高基期。","assumption":"資料中心建置在 FY2028 前不會進入消化期。","consequence":"FY2028–29 訂單轉負、積壓年減，營運槓桿反轉，EPS 停在 6 美元附近、本益比壓到 15 倍，五年後約 99 美元（−34%）；與唯一致命點同源，已併入。","ruling":"部分採納：給 Bear 30% 機率；但 FY2027 有積壓 70–80% 轉換的能見度，12 個月內發生機率低。","watch":"每季積壓訂單金額與有機年增率、有機訂單年增率。","evidence_refs":["end_markets#2","supply_demand_durability#2"],"fact_refs":["f_kpi7_organic_orders_yoy","f_kpi8_backlog"]},{"view":"論點成功但股東經濟變差","evidence":"資料中心占比由 FY2025 約 12% 往三分之一走；FY2027 資本支出升到約 9 億美元、重組費用約 4 億美元；近四季 GAAP FCF 利潤率 6.64% 對 TT 16.43%；價格/成本為正但稀釋毛利率；10-K 稱關稅若加碼會壓營收成長與利潤率；關鍵半導體與稀土零件依賴單一或少數供應商。","assumption":"營收與 EPS 成長會等比例變成股東拿得到的現金，倍數不因組合變化而下修。","consequence":"論點兌現、資料中心變成三分之一，但獲利跟著超大型客戶資本支出起伏，市場改給循環股倍數（16–18 倍）；新增產能在下行期變固定成本，GAAP 現金流持續落後，回購能力打折。","ruling":"採納：這是 Base 終端倍數從 23.6 倍降到 21 倍的理由；不加 Bear 機率，改反映在倍數。","watch":"GAAP 營業現金流減資本支出÷營收（目標 ≥10%）；資料中心占營收比重；調整後 Segment EBITA 利益率年變動。","evidence_refs":["reg_tariff_export#0","geo_supply_chain#1"],"fact_refs":["f_peer_jci_fcf_margin_pct","f_peer_tt_fcf_margin_pct","f_kpi4_fcf"]},{"view":"論點成功但股東經濟變差","evidence":"Chemguard 與 Tyco Fire Products 在美國 49 件聯邦集體訴訟、加拿大 7 件 AFFF 消防泡沫 PFAS 訴訟中為被告（FY2025 10-K 附註 20）；求償與準備金額事實表未涵蓋。","assumption":"PFAS 責任可控，不會吃掉多年自由現金流。","consequence":"和解若達數十億美元，等於一到兩年的回購額度，調整後 EPS 不受影響，但每股價值與回饋縮水。","ruling":"採納為監測項，不入機率：金額與時程無資料，不可裁決至公司揭露和解或判決金額為止。","watch":"10-K／10-Q 法律附註的和解金額與準備金；任何單筆或累計超過 10 億美元的和解或判決。","evidence_refs":["major_events#1","lawsuit_class_action#1"],"fact_refs":[]},{"view":"價格已反映太多","evidence":"前瞻本益比 23.6 倍、trailing 31.6 倍，本益比與 EV/S 在近四個年度端點最高；FY2027 共識 6.32 已略高於指引上緣 6.30；賣方平均目標價約 145–162 美元，與現價差不多。","assumption":"FY2027 之後仍能維持中雙位數 EPS 成長，倍數不下修。","consequence":"只要 FY2029 之後成長回到 10% 左右、倍數回到 18 倍，股價約 160 美元，三年報酬只剩個位數。","ruling":"採納：不追價，等 135 美元附近（FY2027 約 21.4 倍）且積壓仍年增再分批。","watch":"股價對 FY2027 共識的前瞻本益比；季報後 FY2028 共識是否上修。","evidence_refs":["capital_markets_pricing#3"],"fact_refs":["f_fwd_pe_latest","f_pe_current","f_pe_percentile","f_consensus_eps_fy1"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 143.08 → 本次 149.03（+4.2%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=143.08","side_b":"本次 price_at_dd=149.03","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 143.08 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 143.08 美元：五年期望值 前份未列，基準年化 前份未列，前份未列不對稱比","side_b":"本次情境、股價仍用 143.08 美元：Bull 價 292.5、Bear 價 99，五年期望值 +36.3%，基準年化 7.4%，不對稱比 2.82","ruling":"先換情境、股價不動：五年期望值與基準年化前份未列，無法比較。前份未列不對稱比，本次為 2.82。Bull、Bear 價位與股價無關，只受情境影響。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 143.08 美元：五年期望值 +36.3%，基準年化 7.4%，不對稱比 2.82","side_b":"本次情境、股價 149.03 美元：五年期望值 +30.8%，基準年化 6.6%，不對稱比 2.39","ruling":"再換股價、情境不動：起點價上漲 4.2%，五年期望值少 5.4 個百分點，基準年化少 0.9 個百分點，不對稱比由 2.82 降到 2.39。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"一致判斷：前一季承諾的兌現","cause":null,"prior_field":null,"side_a":"Q3 法說（2026-07-29，財務長）：Q4 有機成長 9–10%、FY2026 調整後 EPS 約 5.05、未來 12–18 個月營運槓桿高於 30%、服務回到中高個位數。","side_b":"Q4 實績（2026-10-27）：Q4 有機 +12%、Q4 EPS 1.66 高於指引約 1.55、FY2027 指引營運槓桿逾 30%、服務 +8%。","ruling":"一致：管理層連續上修並交付，FY2027 指引視為偏保守的下限。","evidence_level":"公司一手（法說逐字稿、新聞稿）","settle_metric":"Q1 FY2027 有機營收是否落在 12–14%","if_then":["若 Q1 FY2027 有機營收低於 12% 且全年指引未上調，則把指引可信度降一級、停止加碼"],"evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#1"]},{"axis":"資本回饋與資本支出承諾 vs 實際","cause":null,"prior_field":null,"side_a":"投資人日（2026-06-01，財務長）：承諾 100% 自由現金流還給股東；稱已讓資本支出與營收成長脫鉤。","side_b":"FY2026 回饋 25 億美元，約調整後 FCF 32 億美元的 78%，淨負債比降到 1.8 倍；FY2027 資本支出升到約 9 億美元，FCF 轉換降到約 95%。","ruling":"可調和（程度差異）：承諾在財年後段才提出，差額用於降槓桿與 Alloy 收購；但脫鉤說法已被 FY2027 實體產能投資部分推翻，財務長 6 月也承認終究需要實體產能。","evidence_level":"公司一手","settle_metric":"FY2027 回購加股息÷調整後自由現金流","if_then":["若 FY2027 回饋低於調整後 FCF 的 85% 且淨負債比仍低於目標區間，則資本配置評語降一級","若 FY2027 回饋達 95% 以上，則恢復對承諾的信任"],"evidence_refs":[]},{"axis":"冷卻機長期需求：管理層 vs 晶片端說法","cause":null,"prior_field":null,"side_a":"NVIDIA 執行長 2026-01 稱次世代晶片可能大幅降低資料中心冷卻需求；GTC Berlin 影片再度呈現無冷卻機設計（Q4 法說分析師轉述）；JCI 10-K 自承若跟不上液冷與 AI 技術變化會受不利影響。","side_b":"JCI 執行長（Q4 法說）：客戶以冗餘與尖峰條件設計，實務上沒有少用冷卻機，邊際上也許少 1–2 台；Q3 法說稱影響非常小；Q4 訂單年增 44%、風冷/水冷組合未變。","ruling":"⚖ 不可調和（方向相反），選管理層這邊、期限兩年：依據是硬數據——Q4 有機訂單年增 44%、冷卻機仍是最大產品線，且 JCI 已把產品延伸到 CDU、冷板（Alloy）與模組化，降低單押冷卻機的風險；晶片端說法目前只有新聞轉述，沒有訂單數據支撐。五年以上不排除晶片端說法成立，已放進 Bear 機率與護城河扣分。","evidence_level":"一手訂單數據＋管理層說法 vs 二手新聞轉述","settle_metric":"資料中心冷卻機訂單方向（法說定性揭露）；CDU／冷板訂單占資料中心訂單成長比重","if_then":["若管理層揭露資料中心冷卻機訂單年減，或主要超大型客戶公開量產無冷卻機設計，則減碼至半倉並重跑研究","反向：若 10 億美元以上的 CDU 商機有一半轉成訂單、資料中心營收占比續升，則恢復加碼權限"],"evidence_refs":["substitute_technology#1","substitute_technology#0","competitive_share_entrants#1"]},{"axis":"現金流品質：調整後 vs GAAP","cause":null,"prior_field":null,"side_a":"調整後自由現金流 FY2026 32 億美元、轉換 103%（Q4 法說）。","side_b":"近四季（至 2026-06）GAAP FCF 利潤率 6.64%，低於 TT 16.43%、LII 15.34%；FY2025 GAAP FCF 9.65 億美元、利潤率 4.09%。","ruling":"可調和（口徑差異）：GAAP 口徑可能含出售住宅業務的稅款與重組現金等一次性項目，但拆解事實表未涵蓋，視為未證，以 FY2027 GAAP 數字驗證。","evidence_level":"公司調整後口徑 vs 資料商 GAAP 口徑","settle_metric":"FY2027 GAAP 營業現金流減資本支出÷營收","if_then":["若 FY2027 GAAP FCF 利潤率低於 8%，則不再採信調整後轉換率、品質評語降一級"],"evidence_refs":[]},{"axis":"共識上修幅度是否真實","cause":null,"prior_field":null,"side_a":"近三個月 FY1 共識 EPS 由 4.97 升到 6.32（+27%）；德國財經網站標題稱 FY2027 EPS 指引顯著高於共識。","side_b":"4.97 接近 90 天前的 FY2026 指引（約 5.05），6.32 是 FY2027；財報後兩次快照 FY1–FY3 都沒變，且 6.32 已略高於指引上緣 6.30。","ruling":"可調和：+27% 主要是財年滾動造成，不是真實上修；高於共識是對財報前的舊共識而言。共識動能視為中性，不作加分。","evidence_level":"資料商快照（口徑問題）","settle_metric":"下一次快照 FY2027 與 FY2028 共識的變動","if_then":["若 Q1 FY2027 財報後 FY2028 共識上修 ≥5%，才視為真實上修"],"evidence_refs":["capital_markets_pricing#2"]},{"axis":"積壓訂單數字口徑","cause":null,"prior_field":null,"side_a":"公司 Q4 KPI：積壓訂單 230 億美元、有機年增 43%。","side_b":"同一份新聞稿另一段：訂單年增 58%、積壓 178 億美元年增 54%。","ruling":"可調和：178 億美元搭配訂單 +58%，與美洲訂單 +58% 吻合，判讀為美洲分部數字；全公司以 230 億美元為準。美洲約占積壓 77%，高於其營收占比 69%，集中度在升高。","evidence_level":"公司一手（同一份新聞稿不同段落）","settle_metric":"下一季新聞稿分部積壓揭露","if_then":["若確認 178 億美元為全公司口徑，則重算積壓年增與轉換假設"],"evidence_refs":["supply_demand_durability#1","end_markets#0"]},{"axis":"現在就買的最強論證 vs 等回踩","cause":null,"prior_field":null,"side_a":"現在就買：指引連續上修且每季超標；積壓 230 億美元，若客戶電力限制鬆動，FY2027 營收有上修空間（財務長 Q4 法說）；第二輪重組再省 6 億美元；FY2028 共識 7.40 對應只有約 20 倍。","side_b":"等：倍數在自身近四年最高、賣方均值目標接近現價、機率加權年化約 8%；資料中心占比升高讓獲利更景氣化。","ruling":"選等：基本面好，差的是價格不是證據。","evidence_level":"公司一手＋資料商估值","settle_metric":"股價對 FY2027 共識的前瞻本益比；Q1 FY2027 有機營收與全年指引","if_then":["若股價先漲到 165 美元以上而 Q1 FY2027 尚未上調指引，則不追","若股價回到 135 美元以下且積壓仍年增，則分批反買第一批","若 Q1 FY2027 有機營收 ≥12% 且全年 EPS 指引上調到 6.30 以上，即使價格未回落也買第一批"],"evidence_refs":[]},{"axis":"估值結論沿革","cause":"價格變動","prior_field":["val"],"side_a":"前份：合理（股價 143.08，前瞻基期為 FY2026）。","side_b":"本次：合理偏滿（股價 149.03，前瞻基期滾到 FY2027 共識 6.32，前瞻本益比約 23.6 倍）。","ruling":"估值結論不變：股價上漲約 4%，但 EPS 基期上移約兩成，兩者大致抵銷；前份等的 135 美元在 FY2027 基期下約 21.4 倍。","evidence_level":"事實表價格與共識","settle_metric":"前瞻本益比","if_then":["若前瞻本益比升到 28 倍以上而共識未同步上修，則減碼三分之一"],"evidence_refs":[]},{"axis":"價值陷阱風險上調","cause":"新證據","prior_field":["trap"],"side_a":"前份：價值陷阱風險低。","side_b":"本次：中——共識 FY2028 EPS +17% 對營收 +8.3%，差逾 5pp；FY2027 指引 EPS +21% 對有機營收 +11–12%；資料中心占比升高。","ruling":"採新證據：EPS 成長大幅跑贏營收、靠利潤率與景氣，亮一個衰退訊號，調為中等。","evidence_level":"公司指引＋資料商共識","settle_metric":"FY2028 營收與 EPS 成長差距","if_then":["若 FY2028 EPS 成長回到與營收差距 5pp 以內，則調回低風險"],"evidence_refs":[]},{"axis":"品質評級降一級","cause":"方法變動","prior_field":["signal"],"side_a":"前份：品質評級 A，護城河未計分。","side_b":"本次：B——護城河改用執行力／定價力計分並扣生態層威脅，對最強同業利潤率差距為負，得 C 級，連帶品質評級降一級；基本面本身轉強，不是變差。","ruling":"方法變動導致，不是生意變差：Q4 與 FY2027 指引都優於前份預期。","evidence_level":"同業利潤率對照＋法說","settle_metric":"與 TT 的 GAAP 營業利益率差距","if_then":["若兩年內差距縮到 2pp 以內且 CDU 商機轉成訂單，則品質評級回到 A"],"evidence_refs":[]},{"axis":"護城河方向維持","cause":"新證據","prior_field":["moat_trend"],"side_a":"前份：方向穩定。","side_b":"本次：方向穩定——執行力證據轉強（三區利潤率擴張、訂單 +44%），但替代技術與多供應商的反證同時增加，相對最強同業的差距未證明收斂。","ruling":"正反新證據互相抵銷，方向不變。","evidence_level":"公司一手＋二手新聞","settle_metric":"與 TT 的 GAAP 營業利益率差距；資料中心冷卻機訂單方向","if_then":["若差距收斂到 2pp 以內則調為擴大；若冷卻機訂單轉年減則調為縮減"],"evidence_refs":["substitute_technology#1","end_markets#2"]},{"axis":"新格式補齊欄位","cause":"方法變動","prior_field":["runway_post_y5","archetype","cycle_position","p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份未填：五年後跑道、公司類型、景氣位置、情境機率、最大回撤範圍、裁決與角色欄皆空白。","side_b":"本次依新格式補齊：五年後跑道中等、類型為品質複利成長（次類循環）、景氣位置中段、情境機率 25／45／30、最大回撤 −30%～−45%；裁決與角色由程式從本次輸入算出。","ruling":"純格式補齊，非判斷翻轉。","evidence_level":"方法","settle_metric":"無","if_then":["若資料中心占比超過 30% 且訂單波動加大，則類型改為循環主類並改用循環紀律"],"evidence_refs":[]},{"axis":"重新進場條件由空白改設","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"前份未設重新進場欄；裁決文字寫等 BB 中軌 $132 或 Fwd PE 24x ~$135 回測。","side_b":"股價 ≤135 美元（約 FY2027 共識 21.4 倍）且最近一季積壓訂單仍年增，啟動第一批。","ruling":"價位相近，但改成價格與積壓訂單雙條件：前份 24 倍是舊基期，同一價位在 FY2027 基期只剩 21.4 倍，價格錨不必放寬；加上基本面條件，避免在景氣反轉時接刀。","evidence_level":"方法","settle_metric":"股價；積壓訂單年增率","if_then":["若股價到 135 美元但積壓已轉年減，則不進場、改重跑研究"],"evidence_refs":[]},{"axis":"Single Thing 由空白改設","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設唯一致命點。","side_b":"Single Thing：積壓訂單轉為年減（資料中心訂單進入消化期的第一個硬訊號）。","ruling":"積壓訂單是情境樹中敏感度最大的單一變數：Base 的 FY2028–29 EPS 有一半以上靠積壓轉營收與營運槓桿。","evidence_level":"方法＋公司一手","settle_metric":"每季積壓訂單有機年增率","if_then":["若積壓轉年減，則減碼一半；若隔季有機訂單仍年減逾 10% 且全年指引下修，則清倉"],"evidence_refs":[]},{"axis":"減碼與清倉門檻由空白改設","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設清倉與減碼指標。","side_b":"積壓轉年減→減碼一半；有機訂單連兩季年減逾 10% 且全年指引下修→清倉；利益率連兩季年減 ≥100bp→停止加碼；FY2027 GAAP FCF 利潤率 <8%→品質評語降一級。","ruling":"新增可量化的減碼與清倉門檻，取代前份的文字描述。","evidence_level":"方法","settle_metric":"見各指標","if_then":["若任一清倉條件觸發，則清倉並重跑研究"],"evidence_refs":[]},{"axis":"論點門檻改寫（H1–H3、R1–R3）","cause":"新證據","prior_field":["thesis.H","thesis.R"],"side_a":"前份：H1 FY27 積壓 >220 億美元且 Applied HVAC 有機 ≥15%；H2 FY27 營業利益率 >13.5%、ROIC ≥8.5%；H3 前瞻本益比不破 23 倍；R3 前瞻本益比跌破 22 倍且賣方降評 ≥3 家。","side_b":"本次：H1 FY2028 有機營收 ≥10%、積壓 ≥230 億美元；H2 FY2027 調整後 EBIT 利益率擴張 ≥100bp、FY2031 GAAP 營業利益率 ≥18%；H3 改為 GAAP FCF 利潤率 ≥10%；估值門檻移到行動條件；新增 PFAS 與擴產過度兩條風險。","ruling":"前份 H1 的 220 億美元已在 FY2026 Q4 達到（230 億），門檻上移；Applied HVAC 分部數字與 ROIC 投入資本本包未涵蓋，改用可驗證的公司層數字；估值不是生意假設，移出論點，改由重新進場與減碼條件處理。","evidence_level":"公司一手","settle_metric":"各假設門檻","if_then":["若 FY2027 有機營收低於 10%，則 H1 判削弱、停止加碼"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"積壓與有機成長驗證兩年需求","type":"假設驗證","maps_to":"H1","metric":"積壓訂單金額；有機營收年增率","threshold":"積壓 ≥230 億美元且 FY2027 有機營收 ≥10%","action":"未達則停止加碼","source_freq":"每季財報新聞稿","date":"2027-02"},{"n":2,"text":"積壓訂單轉為年減","type":"Single Thing","maps_to":"H1","metric":"積壓訂單有機年增率","threshold":"<0%","action":"減碼一半、停止加碼","source_freq":"每季財報新聞稿","date":null},{"n":3,"text":"資料中心訂單消化","type":"風險","maps_to":"R1","metric":"有機訂單年增率","threshold":"連兩季 <−10%","action":"減碼至半倉","source_freq":"每季","date":null,"evidence_refs":["end_markets#2"]},{"n":4,"text":"冷卻機被散熱架構改變取代","type":"風險","maps_to":"R2","metric":"資料中心冷卻機訂單方向；主要客戶設計規格","threshold":"管理層揭露資料中心冷卻機訂單年減，或主要客戶量產無冷卻機設計","action":"減碼至半倉、重跑研究","source_freq":"每季法說；晶片商產品發表","date":null,"evidence_refs":["substitute_technology#0","substitute_technology#1","competitive_share_entrants#1"]},{"n":5,"text":"關稅與零件成本吸收失敗","type":"風險","maps_to":"R3","metric":"調整後 Segment EBITA 利益率年變動","threshold":"連兩季年減 ≥100bp","action":"停止加碼","source_freq":"每季","date":null,"evidence_refs":["reg_tariff_export#0","geo_supply_chain#1"]},{"n":6,"text":"PFAS 訴訟金額落地","type":"風險","maps_to":"R4","metric":"AFFF 和解或判決金額","threshold":"單筆或累計 >10 億美元","action":"減碼三分之一","source_freq":"10-K／10-Q 法律附註","date":null,"evidence_refs":["major_events#1","lawsuit_class_action#1"]},{"n":7,"text":"價格回到合理區","type":"估值rearm","maps_to":"H1","metric":"股價；積壓訂單年增率","threshold":"股價 ≤135 美元（FY2027 共識約 21.4 倍）且積壓仍年增","action":"分批第一批","source_freq":"每日股價＋每季","date":null},{"n":8,"text":"基本面證實更強","type":"加碼","maps_to":"H2","metric":"Q1 FY2027 有機營收；全年 EPS 指引","threshold":"有機 ≥12% 且全年指引上調到 6.30 美元以上","action":"加碼一批","source_freq":"季報","date":"2027-02"},{"n":9,"text":"倍數過熱","type":"減碼","maps_to":null,"metric":"前瞻本益比（股價÷FY1 共識）","threshold":"≥28 倍（以 FY2027 6.32 約 177 美元）且共識未同步上修","action":"減碼三分之一","source_freq":"每日","date":null},{"n":10,"text":"景氣反轉確認","type":"清倉","maps_to":"H1","metric":"有機訂單年增率；全年 EPS 指引","threshold":"積壓年減後，下一季有機訂單仍 <−10% 且全年指引下修","action":"清倉","source_freq":"每季","date":null},{"n":11,"text":"擴產過度","type":"風險","maps_to":"R5","metric":"資本支出；有機營收成長","threshold":"FY2028 資本支出 ≥9 億美元而有機營收 <5%","action":"停止加碼","source_freq":"年度","date":null},{"n":12,"text":"Q1 FY2027 財報複審","type":"複審日期","maps_to":null,"metric":"全面複審","threshold":"財報公布後一週內","action":"重跑研究","source_freq":"季報","date":"2027-02"}],"kill_metrics":[{"metric":"積壓訂單有機年增率","bear_threshold":"<0%（轉為年減）","window":"任一季，FY2027–FY2028","source":"公司季報新聞稿","last_status":"ok"},{"metric":"有機訂單年增率","bear_threshold":"連兩季 <−10%","window":"連續兩季","source":"公司季報新聞稿","last_status":"ok"},{"metric":"FY2027 調整後 EPS 指引中值","bear_threshold":"下修至 <6.00 美元","window":"FY2027 各季法說","source":"法說會","last_status":"ok"},{"metric":"調整後 Segment EBITA 利益率年變動","bear_threshold":"連兩季年減 ≥100bp","window":"連續兩季","source":"公司季報新聞稿","last_status":"ok"},{"metric":"GAAP 自由現金流÷營收","bear_threshold":"FY2027 全年 <8%","window":"FY2027 全年","source":"10-K 現金流量表","last_status":"warning"}],"evidence_dismissed":[{"ref":"regulatory_antitrust#2","reason":"證據為 2023-05 的香港報紙報導，指控行為期間 2015-12 至 2018-06，報導未載明罰款、判決結果或對公司的財務影響；HK$30 億是涉案工程總額，不是求償或罰款金額；FY2025 10-K 法律程序未列此案，無法量化也沒有後續進度。"}],"action_conditions":{"rearm_trigger":"股價 ≤135 美元（約 FY2027 共識 21.4 倍）且最近一季積壓訂單仍年增，啟動第一批","exec_line":"現價不追；135 美元以下且積壓仍年增→第一批；Q1 FY2027 有機 ≥12% 且指引上調→第二批；積壓年減→減碼一半；隔季有機訂單 <−10% 且指引下修→清倉"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":"中循環","cycle_verdict":"等回踩","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"股價回到 135 美元以下（FY2027 共識約 21.4 倍、貼近 52 週均線 135.46）且最近一季積壓訂單仍年增"},"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8w(原9)","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='C'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟡', moat_trend='→', week26=3.3, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position='中循環', moat='C', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":false,"basis":"signal='B', val='🟡'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":true,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"8w","condition":"判斷者宣告 wait_for_price（價格合理但要等）→ 原 row9 進場改觀望（等價格）","hit":true,"basis":"wait_for_price=True, 等待條件='股價回到 135 美元以下（FY2027 共識約 21.4 倍、貼近 52 週均線 135.46）且最近一季積壓訂單仍年增'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":null,"requires_critic":[]},"thesis":{"H":[{"id":"H1","text":"資料中心與關鍵任務設施的熱管理需求，加上每百萬瓦含量擴大（CDU、冷板、模組化），撐住兩年雙位數有機成長。","2y":"FY2028 有機營收年增 ≥10%；積壓訂單每季 ≥230 億美元","5y":null,"10y":null,"threshold":"FY2027 有機營收 ≥10%（指引 11–12%）；積壓訂單不轉年減","source":"公司季報新聞稿、法說會積壓與訂單揭露","drift_rule":"有機營收成長連兩季低於門檻 5% 以上＝削弱；連三季低於 10% 以上＝反轉"},{"id":"H2","text":"營運系統（80/20、精實）與兩輪重組把利潤率推近同業頂部。","2y":null,"5y":"FY2031 GAAP 營業利益率 ≥18%（近四季 14.45%），與 TT 差距 ≤2pp","10y":null,"threshold":"FY2027 調整後 EBIT 利益率擴張 ≥100bp；第二輪重組 FY2029 年化節省約 6 億美元兌現","source":"季報、10-K、法說會重組進度","drift_rule":"GAAP 營業利益率連四季低於路徑 5% 以上＝削弱；連六季低於 10% 以上＝反轉"},{"id":"H3","text":"成長轉成股東拿得到的現金：GAAP 自由現金流率回到兩位數，回饋接近 100% FCF。","2y":null,"5y":"FY2028 起 GAAP FCF÷營收 ≥10%，調整後轉換 ≥95%","10y":"服務附加率提高，FCF 利潤率接近 TT 目前的約 16%","threshold":"FY2027 GAAP FCF 利潤率 ≥8%、回饋 ≥85% 調整後 FCF","source":"10-K 現金流量表、法說會資本回饋","drift_rule":"五年期：連四季偏離 5% 以上削弱、連六季 10% 以上反轉；十年期：跨兩個年度未改善削弱、跨三個年度反轉"}],"R":[{"id":"R1","text":"資料中心建置進入消化期，訂單與積壓轉負。","h_ref":"H1","clock":"🔥","threshold":"有機訂單連兩季年減逾 10%，或積壓訂單年減","evidence_refs":["end_markets#2"]},{"id":"R2","text":"液冷與次世代晶片降低冷卻機需求，或公司跟不上 AI 與冷卻技術變化。","h_ref":"H1","clock":"🐢","threshold":"管理層揭露資料中心冷卻機訂單年減，或資料中心營收占比連兩年停在 20% 以下","evidence_refs":["substitute_technology#0","substitute_technology#1","competitive_share_entrants#1"]},{"id":"R3","text":"關稅加碼與單一來源零件（半導體、稀土）推高成本，價格轉嫁不足。","h_ref":"H2","clock":"⚡","threshold":"調整後 Segment EBITA 利益率連兩季年減 ≥100bp","evidence_refs":["reg_tariff_export#0","geo_supply_chain#1"]},{"id":"R4","text":"AFFF 消防泡沫 PFAS 集體訴訟和解或判決吃掉多年自由現金流。","h_ref":"H3","clock":"🐢","threshold":"單筆或累計和解／判決 >10 億美元","evidence_refs":["major_events#1","lawsuit_class_action#1"]},{"id":"R5","text":"FY2027 約 9 億美元擴產在需求轉弱時變成過剩產能。","h_ref":"H3","clock":"🔥","threshold":"FY2028 資本支出 ≥9 億美元而有機營收成長 <5%","evidence_refs":[]}],"single_thing":{"description":"積壓訂單轉為年減（資料中心訂單進入消化期的第一個硬訊號）。","why_fatal":"Base 的 FY2028–29 EPS 7.20–8.10 美元有一半以上靠積壓轉營收與營運槓桿；積壓年減代表 FY2028 有機成長掉到個位數、營運槓桿反轉，EPS 與本益比同時下修（23.6 倍→15–18 倍），股價落在 90–110 美元，是情境樹中敏感度最大的單一變數。","if_happens":"減碼一半、停止加碼；若隔季有機訂單仍年減逾 10% 且全年指引下修則清倉。","how_monitor":"每季財報新聞稿的積壓訂單金額與有機年增率；法說會資料中心訂單與客戶電力限制的說法。","probability":"12–24 個月約 20%：FY2026 Q4 訂單年增 44%，FY2027 下半年起比較基期墊高，但管理層稱需求延伸到 FY2027 以後。"}},"appendix_a":{"growth_durability":6,"quality_score":6,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":20.14,"peg_fy2":1.11,"stress":{"pass":2,"total":3}},"eps_meta":{"base_eps_path":{"FY2026A":5.16,"FY2027E":6.32,"FY2028E":7.4,"FY2029E":8.49},"fy_end_month":9,"eps_basis":"調整後 EPS（Non-GAAP）；財年 10 月至隔年 9 月，FY1＝FY2027；FY2026A 5.16 取自單一二手來源，與法說指引中值成長 21% 反推約 5.14 相符"},"catalysts":[{"date":"2027-02","date_precision":"month","type":"guidance","event":"Q1 FY2027 財報：指引有機營收 +12～14%、調整後 EPS 1.15～1.20 美元，看積壓訂單與全年指引是否上調","impact":"高","watch":"積壓是否 ≥230 億美元、全年 EPS 指引是否高於 6.30"},{"date":"2027-03","date_precision":"quarter","type":"other","event":"Global Intrusion 出售預計 FY2027 第二季末完成（年營收約 5 億美元，年化稀釋約 0.15 美元/股）","impact":"低","watch":"完成時點與出售款用途（回購或併購）"},{"date":"2027-06","date_precision":"quarter","type":"capacity","event":"約 9 億美元資本支出的新產能與三區 CDU 擴產陸續到位；與 Armada 合作的 500MW 模組化資料中心在 2027 年出貨","impact":"中","watch":"交期縮短、營運槓桿是否守住 30% 以上"}]}
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
