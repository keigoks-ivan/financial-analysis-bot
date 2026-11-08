你是 DD 管線 v20 的判斷層閘（gate），標的 CELH（20261108）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（45 條）
- `f_kpi0_revenue_gaap`（q1_business）｜Revenue (GAAP)＝847.2 USD m（YoY +16.8%，QoQ +3.6%）｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 8-K Ex.99.1 新聞稿 https://www.sec.gov/Archives/edgar/data/0001341766/000134176626000059/ex9913q2026.htm（numbers.latest_quarter_kpis.items[0]，as_of Q3 2026（季末 2026-09-30，公告於 2026-11-05））
  - 註記：查無共識（新聞稿未載）
- `f_kpi1_adjusted_ebitda_non_gaap`（q1_business）｜Adjusted EBITDA（公司未報 non-GAAP 營業利益，以此代）＝198.6 USD m（利益率 23.4%，YoY −3%）｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 8-K Ex.99.1 新聞稿 https://www.sec.gov/Archives/edgar/data/0001341766/000134176626000059/ex9913q2026.htm（numbers.latest_quarter_kpis.items[1]，as_of Q3 2026（季末 2026-09-30，公告於 2026-11-05））
  - 註記：查無共識（新聞稿未載）
- `f_kpi2_gaap_operating_income`（q1_business）｜GAAP operating income＝172.1 USD m（利益率 20.3%）｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 8-K Ex.99.1 新聞稿 https://www.sec.gov/Archives/edgar/data/0001341766/000134176626000059/ex9913q2026.htm（numbers.latest_quarter_kpis.items[2]，as_of Q3 2026（季末 2026-09-30，公告於 2026-11-05））
  - 註記：查無共識（新聞稿未載）
- `f_kpi5_adjusted_diluted_eps`（q1_business）｜Adjusted diluted EPS＝0.41 USD（GAAP 0.39）｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 8-K Ex.99.1 新聞稿 https://www.sec.gov/Archives/edgar/data/0001341766/000134176626000059/ex9913q2026.htm（numbers.latest_quarter_kpis.items[5]，as_of Q3 2026（季末 2026-09-30，公告於 2026-11-05））
  - 註記：goldesel.de 二手：預期 0.34（未經 IR 證實，僅參考）
- `f_kpi6_gross_margin`（q1_business）｜Gross margin＝46.8 %｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 8-K Ex.99.1 新聞稿 https://www.sec.gov/Archives/edgar/data/0001341766/000134176626000059/ex9913q2026.htm（numbers.latest_quarter_kpis.items[6]，as_of Q3 2026（季末 2026-09-30，公告於 2026-11-05））
  - 註記：查無共識（新聞稿未載）
- `f_peer_celh_gross_margin_pct`（q2_moat）｜CELH 毛利率＝47.95 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CELH.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_celh_operating_margin_pct`（q2_moat）｜CELH 營業利益率＝17.5 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CELH.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_mnst_gross_margin_pct`（q2_moat）｜MNST 毛利率＝55.55 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MNST.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_mnst_operating_margin_pct`（q2_moat）｜MNST 營業利益率＝29.16 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MNST.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_kdp_gross_margin_pct`（q2_moat）｜KDP 毛利率＝48.04 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.KDP.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_kdp_operating_margin_pct`（q2_moat）｜KDP 營業利益率＝14.84 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.KDP.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_pep_operating_margin_pct`（q2_moat）｜PEP 營業利益率＝15.32 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.PEP.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_ko_gross_margin_pct`（q2_moat）｜KO 毛利率＝62.32 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.KO.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_ko_operating_margin_pct`（q2_moat）｜KO 營業利益率＝32.11 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.KO.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝3184.67 USD m｜期間與口徑：2026-11-08／yfinance revenue_estimate 0y 平均（20 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝3450.04 USD m｜期間與口徑：2026-11-08／yfinance revenue_estimate +1y 平均（24 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝1.42 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-11-07）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝1.7 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-11-07）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝1.96 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-11-07）
- `f_kpi4_sbc_gaap`（q4_capital）｜SBC 占 GAAP 營業利益＝5.1 %（SBC 8.7 USD m；占營收 1.0%）｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 8-K Ex.99.1 新聞稿 https://www.sec.gov/Archives/edgar/data/0001341766/000134176626000059/ex9913q2026.htm（numbers.latest_quarter_kpis.items[4]，as_of Q3 2026（季末 2026-09-30，公告於 2026-11-05））
  - 註記：查無共識（新聞稿未載）
- `f_kpi3_free_cash_flow_ocf_capex`（q1_business）｜Free cash flow（OCF−capex，由 10-Q 累計數相減推算）＝127.7 USD m（Q3 OCF 153.9 − capex 26.2）｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：SEC 10-Q Q3 2026 celh-20260930.htm 九個月累計 450.2/51.2 減 10-Q Q2 六個月 296.3/25.0（numbers.latest_quarter_kpis.items[3]，as_of Q3 2026（季末 2026-09-30，公告於 2026-11-05））
  - 註記：查無共識（新聞稿未載）
- `f_peer_celh_fcf_margin_pct`（q2_moat）｜CELH FCF 利潤率＝6.09 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CELH.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝-25.92 USD m｜期間與口徑：2026-11-08／yfinance 最新一季：總債務 674.7、現金 700.62（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝250.56 m shares｜期間與口徑：2026-11-08／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝32.16 USD｜期間與口徑：2026-11-06（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-11-06（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝22.65 x｜期間與口徑：2026-11-07／分母＝FY1 EPS 1.42，分子＝快照價 32.16｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-11-07）
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝36.13 x｜期間與口徑：2026-11-06（RTH 收盤，UTC）／3 個年度端點內的分位＝0.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-11-06（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝0.0 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 3 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝2.54 x｜期間與口徑：2026-11-06（RTH 收盤，UTC）／4 個年度端點內的分位＝0.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝0.0 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝2.53 x｜期間與口徑：2026-11-06（RTH 收盤，UTC）／4 個年度端點內的分位＝0.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝0.0 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ev_s_fwd`（q5_valuation）｜EV/S（EV ÷ FY1 共識營收）＝2.52 x｜期間與口徑：2026-11-08／f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）｜kind：estimate
  - 來源：—（numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_ev_m`（q5_valuation）｜目前企業價值 EV（市值＋淨負債）＝8031.97 USD m｜期間與口徑：2026-11-08／市值 8057.89 ＋ 淨負債 -25.92｜kind：realized
  - 來源：—（numbers.capital_structure.ev_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rsi14`（q5_valuation）｜RSI(14)＝68.01｜期間與口徑：2026-11-06（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-11-06（RTH 收盤，UTC））
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝-0.4 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-11-06（RTH 收盤，UTC））
- `f_consensus_rev_fy1_pct`（q5_valuation）｜FY1 共識修正＝0.0 %｜期間與口徑：2026-11-07／兩份 Koyfin 快照之間的 EPS 修正幅度（1.42 → 1.42）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.fy1.revision_pct，as_of 2026-11-07）
- `f_consensus_rev_fy2_pct`（q5_valuation）｜FY2 共識修正＝0.0 %｜期間與口徑：2026-11-07／兩份 Koyfin 快照之間的 EPS 修正幅度（1.7 → 1.7）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.fy2.revision_pct，as_of 2026-11-07）
- `f_consensus_rev_fy3_pct`（q5_valuation）｜FY3 共識修正＝0.0 %｜期間與口徑：2026-11-07／兩份 Koyfin 快照之間的 EPS 修正幅度（1.96 → 1.96）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.fy3.revision_pct，as_of 2026-11-07）
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝-1.39 %｜期間與口徑：2026-08-13 → 2026-11-07／FY1 共識 EPS 1.44 → 1.42（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-11-07）
- `f_ma_state`（q5_valuation）｜週線均線六態（decision_inputs.ma 必須等於此值）＝❌｜期間與口徑：2026-11-08／timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）
  - 原文：「price 32.16 / W52 36.47 / W104 38.36 / W250 40.93 / W250 13週斜率 0.43%」
- `f_ma_w52`（q5_valuation）｜52 週均線＝36.47 USD｜期間與口徑：2026-11-08／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）
- `f_ma_w104`（q5_valuation）｜104 週均線＝38.36 USD｜期間與口徑：2026-11-08／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）
- `f_ma_w250`（q5_valuation）｜250 週均線＝40.93 USD｜期間與口徑：2026-11-08／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）
- `f_ma_slope_w250_pct`（q5_valuation）｜W250 13 週斜率＝0.43 %｜期間與口徑：2026-11-08／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）

### findings_digest 中方向為負或來源衝突的條目（23 條）
- `competitive_share_entrants#0`（competitive_share_entrants｜方向 -｜狀態 ok）：FY2025 10-K 風險因子：公司自述功能性飲料競爭激烈，可能難以維持營收、市佔；私有品牌與其他健康／運動表現品牌競爭可能加劇，造成價格侵蝕、市佔下降或促銷費用增加
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-03-02）｜affects：decision_inputs.bear、moat_trend
- `competitive_share_entrants#1`（competitive_share_entrants｜方向 -｜狀態 ok）：FY2025 10-K MD&A：公司自述新進入者或採激進定價的競爭者增強，會顯著衝擊市佔與獲利
  - 來源：SEC EDGAR 10-K FY2025 Item 7（as_of 2026-03-02）｜affects：thesis.R、decision_inputs.bear
- `competitive_share_entrants#3`（competitive_share_entrants｜方向 -｜狀態 ok）：Q3 2025 Celsius品牌美元份額年減約0.5點至11.2%（零售額+13%）
  - 來源：Zacks／Metatrader 轉載（as_of 2026-05-08）｜affects：moat_trend
- `customer_concentration_credit#0`（customer_concentration_credit｜方向 -｜狀態 ok）：FY2025 10-K：2025 年對 Pepsi 銷售占總營收 43.2%，Pepsi 應收占總應收 46.2%；失去 Pepsi 可能造成重大不利影響。
  - 來源：SEC EDGAR 10-K FY2025 Item 1（as_of 2026-03-02）｜affects：thesis.R、decision_inputs.bear
- `customer_concentration_credit#1`（customer_concentration_credit｜方向 -｜狀態 ok）：Q3 2026 10-Q：Pepsi 占截至 2026-09-30 九個月營收 61.3%、應收帳款 58.5%。
  - 來源：SEC EDGAR 10-Q 2026-09-30（as_of 2026-11-05）｜affects：thesis.R、decision_inputs.bear
- `supply_demand_durability#2`（supply_demand_durability｜方向 -｜狀態 ok）：Statista 預測全球能量與運動飲料營收成長率2024–2027連續下降，2027年約3.32%（第四年下滑）；各研調機構預測差異大（CAGR 5.7%–7.8%）
  - 來源：Statista, revenue growth energy drinks worldwide（as_of 2026-01-01）｜affects：thesis.R、decision_inputs.bear
- `supply_demand_durability#3`（supply_demand_durability｜方向 -｜狀態 ok）：管理層點出商品與運費波動、品類促銷強度為風險；另有Costco Kirkland能量飲料等競品
  - 來源：Celsius Holdings Q1 2026 results (BusinessWire)（as_of 2026-05-07）｜affects：thesis.R、decision_inputs.bear
- `regulatory_antitrust#1`（regulatory_antitrust｜方向 -｜狀態 ok）：廣告與促銷受 FTC 法及州消費者保護法規範；任何政府或私人訴訟行動可能產生重大不利影響（風險因子，非已發生案件）。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A Risk Factors（as_of 2026-03-02）｜affects：thesis.R
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：10-K：關稅（含鋁）可能提高原料與包裝成本；至今未對營運結果造成重大影響，但價格轉嫁能力受競爭限制。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-03-02）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#1`（reg_tariff_export｜方向 -｜狀態 ok）：10-K MD&A：關稅已影響且可能持續影響供應鏈（含鋁包材成本），未來影響難以合理估計。
  - 來源：SEC EDGAR 10-K FY2025 Item 7 MD&A（as_of 2026-03-02）｜affects：thesis.R、valuation
- `reg_tariff_export#2`（reg_tariff_export｜方向 -｜狀態 ok）：10-K：出口管制／制裁及進出口法規變動可能影響產品出口與國際經銷。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-03-02）｜affects：thesis.R
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：Celsius 不自有工廠，生產外包給第三方 co-packer；FY2023 10-K 稱已建北美 co-packer 與倉儲網路以限制單一區域曝險；FY2024 10-K 稱 12 oz 專有罐只有少數供應商可供，且曾因鋁罐短缺進口海外罐子影響 2021–22 毛利。
  - 來源：Celsius Holdings 10-K FY2022/FY2023/FY2024（搜尋摘要彙整）（as_of 2025-02-28）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：Q1 2026 10-Q 將鋁罐成本列為主要市場風險，公司目前未使用避險工具，且轉嫁成本能力受競爭限制；FY2025 10-K 有獨立的關稅／全球供應鏈中斷風險因子。
  - 來源：Celsius Holdings Form 10-Q Q1 2026 / 10-K FY2025（搜尋摘要）（as_of 2026-05-08）｜affects：thesis.R、valuation
- `end_markets#2`（end_markets｜方向 -｜狀態 ok）：CFO 警告 Q4 因年底促銷時點、整合工作與大客戶現金管理而有雜訊，Alani Nu 在 Pepsi 體系擴大舖貨
  - 來源：Stocktwits（as_of 2026-11-06）｜affects：thesis.R、triggers
- `substitute_technology#1`（substitute_technology｜方向 -｜狀態 ok）：Costco Kirkland 自有品牌能量飲 2026 年 3 月底推出，對 Celsius 股價形成壓力
  - 來源：Fool/Yahoo Finance: Where Will Celsius Stock Be in 5 Years?（as_of 2026-04-26）｜affects：moat_trend、thesis.R
- `substitute_technology#2`（substitute_technology｜方向 -｜狀態 ok）：AlixPartners 模型估 GLP-1 藥物使能量飲與咖啡約 4% 年化下滑
  - 來源：AlixPartners: GLP-1 drugs stir change in the beverage industry（as_of 2025-08-01）｜affects：decision_inputs.bear、thesis.R
- `channel_business_model_shift#2`（channel_business_model_shift｜方向 -｜狀態 ok）：2026Q3 毛利率 46.8%（去年同期 51.3%），10-Q 歸因於通路組合（DSD 比重上升）與鋁、燃料成本；CELSIUS 品牌營收約 -6%，原因含 SKU 優化、庫存再平衡出貨時點與量販（club）通路疲弱。
  - 來源：Celsius 10-Q 2026Q3（經 WebSearch 摘要）（as_of 2026-11-05）｜affects：moat_trend、valuation、decision_inputs.bear
- `capital_markets_pricing#0`（capital_markets_pricing｜方向 -｜狀態 ok）：Chartmill 截至 2026-10-25：FY2026 EPS 共識 $1.47（28 位分析師）；下一季營收預估近 3 個月下修 7.57%，下一財年 EPS 約下修 11%（Q3 財報 11/5 前快照）
  - 來源：Chartmill CELH Earnings & Revenue Estimates（as_of 2026-10-25）｜affects：valuation、decision_inputs.bear
- `capital_markets_pricing#3`（capital_markets_pricing｜方向 -｜狀態 ok）：Morgan Stanley 2026-05 目標價由 $64 降至 $55；Citigroup 2026-04 由 $65 降至 $60 維持買進
  - 來源：MarketBeat Citigroup issues pessimistic forecast for Celsius（as_of 2026-04-15）｜affects：valuation
- `major_events#0`（major_events｜方向 -｜狀態 ok）：FY2025 10-K 揭露仍有重大未決訴訟（證券、衍生、合約爭議）；Ingrao 衍生訴訟 2025-04 和解（律師費 100 萬美元），並於 2025-12-26 新增原專利/配方方版稅訴訟（每箱 10 美分）。
  - 來源：SEC EDGAR 10-K FY2025 Item 3／Note 17（as_of 2026-03-02）｜affects：decision_inputs.bear、thesis.R
- `lawsuit_class_action#0`（lawsuit_class_action｜方向 -｜狀態 ok）：10-K 載明有針對公司的 channel stuffing 集體訴訟、虛假廣告集體訴訟，及重大證券、衍生、合約爭議未決。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A／Item 3（as_of 2026-03-02）｜affects：decision_inputs.bear、thesis.R
- `lawsuit_class_action#1`（lawsuit_class_action｜方向 -｜狀態 ok）：2025-12-26 新增版稅訴訟（每箱 10 美分、自 2021-01-01），公司否認並將抗辯，結果無法預估。
  - 來源：SEC EDGAR 10-K FY2025 Note 17（as_of 2026-03-02）｜affects：decision_inputs.bear
- `lawsuit_class_action#2`（lawsuit_class_action｜方向 -｜狀態 ok）：Pomerantz 於 2026-06 宣布調查 CELH 證券詐欺主張（律所新聞稿，非法院申報）。
  - 來源：Pomerantz Law Firm 新聞稿（Barchart／AccessNewswire）（as_of 2026-06-01）｜affects：decision_inputs.bear

### 事實表自陳的缺口（2 條）
- q2_moat：evidence.numbers.peer_financials 該欄整欄為 null（常見於未單獨揭露研發的業者），事實表 agent 若能從財報補就補，補不到即為缺口，判斷者不得自行估。
- q6_how_wrong：digest.qa_flags 有 5 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CELH_20261108/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":88.8,"bear_5y_price":19.6,"p_bull_pct":20,"p_bear_pct":30,"upside_5y_pct":47.7,"ev5y_pct":47.4,"irr_base_pct":8.1,"asym_ratio":3.0,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":1.42,"pe":22.65,"basis":"FY2026E 共識 EPS（Koyfin 2026-11-07），與終端倍數同為當年度 EPS 口徑"},"eps":{"bull":[1.8,2.25,2.72,3.2,3.7],"base":[1.62,1.85,2.08,2.3,2.5],"bear":[1.3,1.25,1.3,1.35,1.4]},"pe":{"bull":24,"base":19,"bear":14},"p":{"bull":20,"base":50,"bear":30},"yield_pct":{"dividend":0,"net_buyback":0},"second_stage":{"bull_cagr_pct":12,"base_cagr_pct":7},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### CELH_Q2_2026_Earnings_Call_20260806.md
- 2026-08-06｜John Fieldly (CEO)｜guidance：CELSIUS 品牌第三季預期與第二季相近，年底前回到成長（原話："quarter to look a lot like the second quarter, before we"）
- 2026-08-06｜Jarrod Langhans (CFO)｜guidance：第三季毛利率預期與第二季一致、維持高 40% 區間（原話："we would expect the third quarter to be consistent with the"）
- 2026-08-06｜Jarrod Langhans (CFO)｜guidance：第三季銷售與行銷費用預期與第二季大致一致（原話："We would expect sales and marketing in the third quarter"）
- 2026-08-06｜John Fieldly (CEO)｜guidance：CEO 說明第三季 CELSIUS 週銷速率預期大致相近（原話："somewhat similar within the CELSIUS portfolio."）
- 2026-08-06｜John Fieldly (CEO)｜guidance：分析師問第三季持平指的是金額或比率，CEO 答是看掃描資料的金額（原話："Yes. I think we're talking about the dollars, looking at"）
- 2026-08-06｜John Fieldly (CEO)｜guidance：第四季 CELSIUS 恢復的形狀為緩慢累積（原話："So it will be more of a slow build on the CELSIUS portfolio."）
- 2026-08-06｜Jarrod Langhans (CFO)｜guidance：CFO 表示掃描資料不會直接反彈（原話："Wouldn't necessarily look for a direct snapback, but that's"）
- 2026-08-06｜Jarrod Langhans (CFO)｜guidance：CFO 說明第四季帳面基期較軟（原話："we do have a softer comp year-over-year that would be seen"）
- 2026-08-06｜Jarrod Langhans (CFO)｜guidance：第四季 CELSIUS 基期較易、Alani 基期較難，均有新品（原話："So we've got an easier comp with brand CELSIUS plus new"）
- 2026-08-06｜Jarrod Langhans (CFO)｜guidance：2027 新品進貨時程尚未定案，下季財報再提供更多資料（原話："It's not fully baked in."）
- 2026-08-06｜Jarrod Langhans (CFO)｜guidance：CFO 表示下季法說會提供第四季與第一季的更多資料（原話："we'll be able to provide more data on that"）
- 2026-08-06｜Jarrod Langhans (CFO)｜margin：第二季毛利率約 48%（原話："Second quarter gross margin was approximately 48%, in line"）
- 2026-08-06｜Jarrod Langhans (CFO)｜margin：毛利率擴張分三塊來談（原話："As we look towards margin expansion, I think about it in 3"）
- 2026-08-06｜Jarrod Langhans (CFO)｜margin：整合後舊庫存仍使成本有遞延影響（原話："some carryover of higher costs this quarter"）
- 2026-08-06｜Jarrod Langhans (CFO)｜margin：北卡第二條產線下半年開始生產（原話："Our second manufacturing line in North Carolina begins"）
- 2026-08-06｜Jarrod Langhans (CFO)｜margin：大宗商品通膨主要為鋁，運費改善抵銷（原話："commodity inflation, primarily aluminum."）
- 2026-08-06｜Jarrod Langhans (CFO)｜margin：第二季調整後 EBITDA 金額與占比（原話："Adjusted EBITDA was $184 million or approximately 22.5%"）
- 2026-08-06｜Jarrod Langhans (CFO)｜margin：上半年調整後 EBITDA（原話："For the first half, adjusted EBITDA was $380 million"）
- 2026-08-06｜Jarrod Langhans (CFO)｜margin：調整後 SG&A 占營收比（原話："Adjusted SG&A was 28.6% of revenue."）
- 2026-08-06｜Jarrod Langhans (CFO)｜margin：CELSIUS 品牌掃描與帳面差距拆成三項（原話："The gap to reported net sales came from 3 things:"）
- 2026-08-06｜Jarrod Langhans (CFO)｜margin：出貨與消耗差異約占掃描與帳面差距一半（原話："accounted for roughly half of the gap between scanner"）
- 2026-08-06｜Jarrod Langhans (CFO)｜margin：Alani 剔除加拿大與非即飲後的總營收成長口徑（原話："all-in gross revenue growth was approximately 39%."）
- 2026-08-06｜Jarrod Langhans (CFO)｜margin：Alani 第二季淨銷售額（原話："Net sales were approximately $364 million"）
- 2026-08-06｜Jarrod Langhans (CFO)｜margin：Alani 淨銷售成長對照掃描成長（原話："approximately 21% year-over-year, while retail sales grew"）
- 2026-08-06｜Jarrod Langhans (CFO)｜margin：Rockstar 第二季淨銷售額（原話："For Rockstar, net sales were approximately $66 million in"）
- 2026-08-06｜John Fieldly (CEO)｜margin：CELSIUS 品牌每配銷點金額較第一季成長（原話："Dollars per point of distribution are up 16% from the first"）
- 2026-08-06｜Jarrod Langhans (CFO)｜capital_allocation：第二季買回約 1 億美元股票（原話："we repurchased approximately $100 million of stock"）
- 2026-08-06｜Jarrod Langhans (CFO)｜commitment：管理層表示將在今年用完 3 億美元買回授權（原話："We intend to continue utilizing the $300 million"）
- 2026-08-06｜Jarrod Langhans (CFO)｜capital_allocation：7 月降息 25 個基點（原話："We also reduced our interest rate by 25 basis points in July"）
- 2026-08-06｜Jarrod Langhans (CFO)｜capital_allocation：買回股票的理由（原話："The reason why we are leaning into repurchases is"）
- 2026-08-06｜John Fieldly (CEO)｜commitment：海外市場未來五年占營收超過 15%（原話："outside of the U.S. to represent more than 15% of our"）
- 2026-08-06｜John Fieldly (CEO)｜commitment：問答中海外占比說法為 15% 且可能更高（原話："15% over time, that we're looking at, and it could be even"）
- 2026-08-06｜John Fieldly (CEO)｜commitment：2027 年將於部分海外市場推出 Alani Nu（原話："markets in which to introduce Alani Nu in 2027"）
- 2026-08-06｜John Fieldly (CEO)｜commitment：Rockstar 整合依 9 個月時程在 6 月完成（原話："we completed the integration in June"）
- 2026-08-06｜Jarrod Langhans (CFO)｜commitment：下半年已開始導入收益管理，2027 年有更大機會（原話："we see a significantly larger opportunity to drive better"）
- 2026-08-06｜Jarrod Langhans (CFO)｜risk：CELSIUS 與 Alani 的貿易促銷與通路組合影響（原話："we saw some negative mix and channel impact"）
- 2026-08-06｜Jarrod Langhans (CFO)｜risk：俱樂部通路疲軟列為帳面落後原因之一（原話："increased trade and promotional investment, and softness in"）
- 2026-08-06｜Jarrod Langhans (CFO)｜risk：第三季 DC 庫存移轉帶來一次性時點影響（原話："This movement will have some onetime timing"）
- 2026-08-06｜John Fieldly (CEO)｜risk：週轉下調 CELSIUS 品牌剔除 SKU 的影響仍存在，管理層承認剔除過深（原話："We went too deep on the CELSIUS"）
- 2026-08-06｜John Fieldly (CEO)｜competition：Alani 在競爭者更多的品類中成長（原話："more competition than ever before, with more entrants and"）
- 2026-08-06｜John Fieldly (CEO)｜competition：CEO 談到同類模仿者（原話："me-too competition out there."）
- 2026-08-06｜John Fieldly (CEO)｜product：CEO 回顧 SKU 剔除決策，表示不會再剔除這麼多（原話："I definitely would have not cut as many SKUs"）
- 2026-08-06｜John Fieldly (CEO)｜product：新品策略改為以永久新品取代尾端 SKU（原話："new innovation that's permanent throughout the year."）
- 2026-08-06｜John Fieldly (CEO)｜product：16 盎司產品線仍是弱處，2027 年初有新品（原話："Where we still have work is our 16-ounce line, and we have"）
- 2026-08-06｜John Fieldly (CEO)｜product：Fizz-Free 追蹤通路美元銷售較上季成長（原話："growing with dollar sales in tracked channels up over 20%"）
- 2026-08-06｜John Fieldly (CEO)｜product：Purple Cotton Candy 為最暢銷新口味（原話："it quickly became our top-selling new flavor in tracked"）
- 2026-08-06｜John Fieldly (CEO)｜product：Witch's Brew 預計為最大限定口味（原話："biggest LTO in history. We have a comp there."）
- 2026-08-06｜John Fieldly (CEO)｜product：Rockstar 被描述為已穩定（原話："Rockstar has stabilized."）
- 2026-08-06｜John Fieldly (CEO)｜product：Rockstar 銷售符合收購時預期（原話："our sales expectations, which we set upon acquiring the"）
- 2026-08-06｜John Fieldly (CEO)｜customer：零售商提早進行 2027 規劃（原話："retailers are leaning in on 2027 planning earlier than they"）
- 2026-08-06｜Jarrod Langhans (CFO)｜customer：陳列空間取得時程比原預期晚（原話："was a bit off from our initial expectations"）
- 2026-08-06｜John Fieldly (CEO)｜customer：百事年度營運會議對齊 2027 計畫（原話："working on our plans for '27 and aligning on plans and"）

### 問答異常語氣（迴避／改口／保留）
- CELH_Q2_2026_Earnings_Call_20260806.md｜問：Salera：第四季 CELSIUS 回升幅度是否為中個位數、是快速反彈或漸進｜答法：CEO 未給數字，改說「slow build」並轉給 CFO；CFO 也未給幅度，改說下季再提供資訊
- CELH_Q2_2026_Earnings_Call_20260806.md｜問：Teixeira：第四季 Alani 面對高基期怎麼看，以及經銷商相關費用雜訊何時消退｜答法：CFO 表示新品時程「not fully baked in」、下季再提供；未回應費用何時消退
- CELH_Q2_2026_Earnings_Call_20260806.md｜問：Serotta：新品擴張的 SKU 增生防護欄為何｜答法：CEO 以持續優化尾端、用永久新品取代作答，未說明具體防護機制或數字
- CELH_Q2_2026_Earnings_Call_20260806.md｜問：Grom：未來 6 到 9 個月成功長什麼樣、為何有信心｜答法：CEO 以定性描述（品牌健康、零售商會議、2027 新品）作答，未給指標
- CELH_Q2_2026_Earnings_Call_20260806.md｜問：Herzog：SKU 剔除是否正確、第三季是否有更大壓力風險｜答法：CEO 承認剔除過深、會做不同決定，與開場稱此為刻意選擇的框架不同；第三季只答週速率相近、略增

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 4 | 2 |
| customer_second_source | found | 2 | 2 |
| customer_concentration_credit | found | 2 | 1 |
| supply_demand_durability | found | 4 | 3 |
| regulatory_antitrust | found | 2 | 1 |
| reg_tariff_export | found | 3 | 1 |
| geo_supply_chain | found | 2 | 2 |
| end_markets | found | 3 | 2 |
| substitute_technology | found | 3 | 2 |
| channel_business_model_shift | found | 3 | 2 |
| capital_markets_pricing | found | 4 | 4 |
| major_events | found | 2 | 3 |

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260518","verdict":"thesis 仍活 — Q1 26 strong beat(Rev .6M／Adj EPS .41 beat .29 by 41%)、Alani Nu integration ahead of schedule(M synergies)、21% US share(+1000bps YoY)、PepsiCo 11% 戰略持股 + 美加獨家配銷。但 CELSIUS 核心品牌 YoY 僅 +6%(從 +50%+ 大幅減速)、Q1 GM 48.3%(-400bps YoY)、Mgmt FY26 organic Rev guide 僅 +2-4% — 估值🟢(Fwd PE 18.5x／PEG 0.86／分位 <10%) + Pure MA ❌(現價跌穿三條週均)。等 W104 站回或 Q3 26 核心品牌動能回升再建倉 — 訊號 B 觀望，非 C 迴避。","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"CELSIUS 核心品牌雖然減速，但能在 2026-2027 重回雙位數成長（+10% to +15%）— 因 (a) 國際擴張接力 + (b) shelf space gains（Q1 26 已獲 +17% shelf space）+ (c) sugar-free 子賽道結構性順風延續","columns":{"2Y 驗證點":"Q4 26 CELSIUS standalone YoY 重回 +10%+（vs Q1 26 +6%）","5Y 驗證點":"CELSIUS standalone 2030 達 .0B Rev（2024 ~.3B → 2030 .0B = ~7% CAGR）","10Y 驗證點":"2034 CELSIUS standalone 達 .5-.0B（國際 50%+ 占比）","具體數字門檻":"2027 CELSIUS standalone YoY ≥ +10%；國際年率 ≥ 0M（vs 2025 ~0M 年率）","信息來源":"Q1 26 earnings call + Mgmt FY26 guidance + Goldman Sachs / Morgan Stanley reports","漂移觸發條件":"連 2 季 TTM CELSIUS YoY"}},{"id":"H2","text":"Alani Nu 整合執行成功 — 透過 PepsiCo 配銷實現 0M+ synergies（vs 已實現 M），且 Alani Nu standalone 維持 +40% pro forma YoY 連 2 年（2026-2027）","columns":{"2Y 驗證點":"Q4 26 Alani Nu pro forma YoY ≥ +40%；累積 synergies ≥ 0M","5Y 驗證點":"2030 Alani Nu Rev .0-.5B（vs 2024 ~.6B standalone = 2-2.5x）","10Y 驗證點":"2034 Alani Nu 達 .0-.0B（建立完整 Gen Z 女性品牌 ecosystem）","具體數字門檻":"2027 Alani Nu YoY ≥ +40%；synergies 累積 ≥ 0M；GM 回到 50%+","信息來源":"Mgmt Q1 26 earnings call disclosure + Investor presentations","漂移觸發條件":"連 2 季 Alani Nu YoY"}},{"id":"H3","text":"估值倍數修復 — 5Y Fwd PE 從當前 5% 分位（18.5x）回升至中位（25-28x），對應 +35-50% 股價 re-rating 空間。前提：H1/H2 任一兌現 → 市場 derisk thesis 後 re-rate","columns":{"2Y 驗證點":"2027 Fwd FY27 PE 回到 22-25x","5Y 驗證點":"2030 Fwd PE 維持 22-25x 區間","10Y 驗證點":"2034 Fwd PE 落在 18-22x（成熟期合理區間）","具體數字門檻":"FY26 EPS 共識上修至 ≥ .80（vs 當前 .63）；Fwd PE 站回 22x+ 連 4 週","信息來源":"共識 EPS estimate（yfinance / Zacks）+ 5Y PE 歷史區間 28-45x（剔除 hypergrowth 期極端值）","漂移觸發條件":"Fwd PE 連 4 週 10% → 削弱；連 8 週"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"CELSIUS 核心品牌結構性份額流失 — Alani Nu 內部蠶食 + Monster Reign / Red Bull Zero 等大廠 sugar-free SKU 反撲 + Liquid Death 等 functional water 新 entrant 切入","columns":{"對應假設":"H1","時間尺度":"⚡ 短期（1-2 季可觸發）","監測指標":"Nielsen scan CELSIUS standalone 4 週滾動 YoY；CELSIUS Q2 / Q3 standalone YoY","警戒閾值":"Nielsen scan 連 3 個月"}},{"id":"R2","text":"GM 結構性 mix dilution（Alani Nu 永久性稀釋） — Q1 26 GM 48.3%（-400bps YoY），Mgmt guide H2 26 回到 low-50s 若未兌現，估值倍數 derate 15-20%","columns":{"對應假設":"H2","時間尺度":"🔥 中期（4-6 季）","監測指標":"季度 GM 軌跡；Mgmt 法說會 H2 GM guidance 細節","警戒閾值":"Q2 26 GM"}},{"id":"R3","text":"Pepsi 戰略重新評估 / 監管風險 — Pepsi 2027 若啟動飲料業務分拆 / 重議 CELH 配銷條款；或美國 FDA 推 caffeine + minor 法規（18+ purchase）→ 直接砍 TAM 15-25%","columns":{"對應假設":"H1+H3","時間尺度":"🐢 長期（2+ 年慢變數）","監測指標":"Pepsi 公開 IR statements；FDA / California / NY 立法進度","警戒閾值":"Pepsi 公開表態「重新評估飲料業務」；任一州通過 18+ purchase 法案 → 觸發；需 ≥ 50% 機率才考慮砍倉（避免短期新聞驚嚇）"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🟢","ma":"❌","trap":"🟡","moat_trend":null,"runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":30.16,"archetype":null,"cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"CELH","date":"2026-11-08","schema":"v15.0","contract":"v19","company_name":"Celsius Holdings"},"oneliner":"Alani Nu 撐住組合成長，但 CELSIUS 品牌仍在衰退，毛利率 46.8% 比去年少 4.5 個百分點；現價要靠毛利率回升才划算，先等 2027 年上半年的毛利率數字。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CELH_20261108/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CELH_20261108/scenario.json","answers":{"q1_business":{"verdict":"賺美國便利商店與量販通路能量飲消費者的錢，錢卡在 Pepsi 這個配銷節點：第三季 64.6% 營收來自 Pepsi，Alani Nu 的零售成長只有一部分變成公司淨營收。","reasoning":"第三季營收 8.472 億美元，年增 16.8%；Alani Nu 4.101 億（約 +24%）、CELSIUS 3.568 億（約 −6%）、Rockstar 8,030 萬（占 9.5%）。毛利率 46.8%、GAAP 營益率 20.3%、調整後 EBITDA 率 23.4%。單點依賴屬集中度風險，不是護城河證據：Pepsi 占第三季營收 64.6%（去年同期 35.4%）、前九月應收帳款 58.5%，10-K 也寫明 Pepsi 能影響公司的策略決定。產業在擴張期，依據是組合零售額年增 14.7%、份額守在約 21%，管理層稱能量飲仍是飲料裡最強的品類；但全球預測顯示成長逐年放慢。需求結構性持久，供給可逆性高，因為代工外包、新品牌進入成本低。產業態勢判為雙向拉鋸：Alani Nu 帶新客進品類（份額 9.8%，年增近 3 點），同時 CELSIUS 份額由 11.2% 掉到 9.1%，Kirkland 自有品牌也在 2026 年 3 月底進場。第三季帳面含 2,000～2,500 萬美元由第四季提前的出貨，以 46.8% 毛利率換算約貢獻 0.03 美元 EPS（稅率假設 23%，未計額外費用）。","fact_refs":["f_kpi0_revenue_gaap","f_kpi1_adjusted_ebitda_non_gaap","f_kpi2_gaap_operating_income","f_kpi5_adjusted_diluted_eps","f_kpi6_gross_margin"],"verdict_values":{"revenue_quality":"品牌飲料重複消費，但帳面受出貨時點影響大：第三季含 2,000～2,500 萬美元提前出貨，去年第四季另有約 2,500 萬庫存效益不會重複，第四季帳面成長會明顯放慢。","unit_econ_note":"Alani Nu 移入 Pepsi 直送體系後交易投資比重提高，第三季毛利率年減 4.5 個百分點，主因直送組合與鋁、燃料成本。單箱毛利事實表未涵蓋。","archetype":{"primary":"轉機/特殊情境","secondary":"品質複利成長","confidence":"中","fingerprint":"併購整合剛完成，原主力品牌衰退待修復，獲利成長取決於毛利率回升"},"industry":{"clock_phase":"II","sd_verdict_source":"需求結構性持久、供給可逆性高：組合零售額第三季年增 14.7%，管理層稱能量飲仍是飲料最強品類；代工外包使新品牌進入成本低，Statista 預估全球成長到 2027 年放慢至約 3.32%。","bargaining":{"up":"鋁罐與柴油成本上升時轉嫁受競爭限制，公司未避險；12 盎司專用罐供應商少。","down":"Pepsi 占第三季營收 64.6%，公司議價位置弱，轉換配銷安排的彈性受限。","geo":"生產以北美代工與自有北卡產線為主，關稅主要經由鋁進入成本。"},"profit_pool_dir":"事實表未涵蓋五年營業利益池；僅知 CELH TTM 營益率 17.5%，低於 MNST 的 29.16%。","tam_table":[{"item":"海外重點市場即飲能量飲","value":"超過 80 億美元，管理層預期明年雙位數成長（2026-11-05 法說）"},{"item":"美國追蹤通路組合份額","value":"約 20.7%（2026 Q3），Q1 為 20.9%"},{"item":"全球能量與運動飲料成長","value":"Statista 預估 2027 年約 3.32%，各研調 CAGR 5.7%～7.8%，差異大"},{"item":"TAM、SAM、滲透率、營業利益池五年變化","value":"事實表未涵蓋"}]}}},"q2_moat":{"verdict":"護城河大致穩定，方向為→：組合份額守在約 21%，但這是 Alani Nu 補上 CELSIUS 的流失，定價能力仍在下滑。","reasoning":"機制是品牌心智加 Pepsi 直送的貨架與冷櫃覆蓋，沒有轉換成本。同業 ROIC 事實表未涵蓋，改用份額與利潤率比較。份額：組合 2026 Q1 20.9%、Q3 20.7%，Alani Nu 年增近 3 點，CELSIUS 由 11.2% 掉到 9.1%。利潤率：TTM 毛利率 47.95%，比 MNST 低 7.6 個百分點，營益率 17.5% 比 MNST 低 11.66 個百分點（MNST 資料到 2026-06）。執行面給 6 分：整合如期完成、Alani Nu 創紀錄，但 2026 年 SKU 砍過頭是管理層自己承認的失誤（2026-08-06 CEO）。定價面給 5 分：CFO 說定價跟隨品類領導者，毛利率 46.8% 比去年少 4.5 個百分點，交易投資占比第三季仍較第二季上升。方向判→的反例是毛利率下滑若屬結構性，就應判↓；目前拆不開鋁、柴油與直送組合各占多少，所以改判條件寫死：組合份額連兩季低於 20%，或 FY2027 毛利率低於 48%。當期 ROIC、增量 ROIC、再投資率都因投入資本未涵蓋而無法計算；四個持續期檢查點有兩個紅燈，集中在消費者換牌零成本與價值被配銷端分走。","fact_refs":["f_kpi6_gross_margin","f_peer_celh_gross_margin_pct","f_peer_celh_operating_margin_pct","f_peer_mnst_gross_margin_pct","f_peer_mnst_operating_margin_pct","f_peer_kdp_gross_margin_pct","f_peer_kdp_operating_margin_pct","f_peer_pep_operating_margin_pct","f_peer_ko_gross_margin_pct","f_peer_ko_operating_margin_pct"],"verdict_values":{"moat":{"mechanism":"品牌心智加 Pepsi 直送帶來的貨架與冷櫃覆蓋；沒有轉換成本，要靠持續新品與配銷維持。","execution":6,"pricing":5,"grade":"C","trend":"→","trend_evidence":"執行面穩定：組合份額 Q1 20.9%、Q3 20.7%，Alani Nu 9.8%，CELSIUS 9.1%（2025 Q3 為 11.2%）。定價面縮減：毛利率 46.8% 對 51.3%，定價跟隨品類領導者。合併判→而不是↓，因為份額仍守住、毛利率下滑有一部分是鋁與柴油的週期因素。","competitor_notes":[{"name":"MNST","strategy_note":"最直接的能量飲對手，TTM 毛利率 55.55%、營益率 29.16%（資料到 2026-06），是 CELH 毛利率回升論點的上限參照。"},{"name":"PEP","strategy_note":"既是最大客戶與配銷商，也是策略股東；TTM 營益率 15.32% 低於 CELH，談判時有壓低配銷條件的動機。"},{"name":"KO","strategy_note":"TTM 毛利率 62.32%、營益率 32.11%，利潤率在另一個層級，只當上限參考；能量飲份額事實表未涵蓋。"},{"name":"KDP","strategy_note":"毛利率 48.04% 與 CELH 接近、營益率 14.84%，可作為毛利率停在 48% 時飲料公司能賺多少的參照。"}],"spread_notes":null,"peer_na_reason":"同業 ROIC 事實表未涵蓋，以份額與毛利率、營益率差距替代；利潤率只有單一期間，看不出差距擴大或收窄。","threats":[{"level":"🟡","text":"自有品牌與低價新品進場，Costco Kirkland 能量飲 2026 年 3 月底上市；CELSIUS 量販通路第三季已偏弱，點對點壓力最先出現在這裡。","p":"30%","evidence_refs":["substitute_technology#1","competitive_share_entrants#0"]},{"level":"🟡","text":"新進者與激進定價對手增加，CEO 在 2026-08-06 法說提到品類競爭者比以往更多；公司自述這會顯著衝擊份額與獲利。","p":"35%","evidence_refs":["competitive_share_entrants#1"]}],"roic_durability":{"quadrant":null,"checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者、決策者、付款者是同一人，第三季組合零售額年增 14.7%；但能量飲是想要而非需要，Witch's Brew 單一限定款貢獻超過 1.3 億美元零售額，顯示成長有一部分靠新鮮感。"},{"item":"決策層級","level":"🔴","text":"消費者在冷櫃前每次都能換牌，沒有轉換成本；CELSIUS 精簡 SKU 又暫停新品後，份額一年掉 2.1 點，可見少了貨架與新品就流失。回購率事實表未涵蓋。"},{"item":"價值鏈分配","level":"🔴","text":"Pepsi 占第三季營收 64.6%（去年同期 35.4%）；直送比重上升拉高交易投資，Alani Nu 零售額 +58%、淨銷售只有 +24%，價值有一部分留在配銷與促銷環節。"},{"item":"社會容忍度","level":"🟡","text":"目前未見針對未成年購買的已生效限制，但有虛假廣告集體訴訟，前份列出的州級 18 歲購買立法進度事實表未涵蓋，列為資料缺口。"}],"roiic":"事實表未涵蓋","reinvest_rate":"事實表未涵蓋","endo_ceiling":null,"formula_note":"投入資本、折舊攤銷與收購對價都未涵蓋，當期 ROIC 象限、增量 ROIC、再投資率均不估算，不以記憶補數字。"}}}},"q3_growth":{"verdict":"五年後的成長跑道屬中等：組合份額還有空間，但近三季沒有上升，海外第二曲線目前只有管理層目標與高增速，金額未經驗證。","reasoning":"FY2026E 營收 31.85 億美元、FY2027E 34.50 億（+8.3%）；EPS FY2026E→FY2028E 年複合 17.5%（1.42→1.96）。兩者差 9.2 個百分點，歸因於毛利率回升與淨回購（前三季回購 1.69 億美元，年化約市值 2.8%），不靠收購，也不依賴倍數上升。內生天花板因投入資本未涵蓋而算不出，情境按超出處理。跑道判中等：組合份額 21% 低於 35%，但近三季沒有上升（20.9%→20.7%），以現有趨勢到不了 30%；海外第三季年增約 56%、管理層目標五年內占營收 15% 以上，是有來源的第二曲線，但目前金額未涵蓋，還沒有實績可驗。要升為寬，需要海外占營收達 10% 且組合份額達 22%。","fact_refs":["f_kpi0_revenue_gaap","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3"],"verdict_values":{"growth":{"driver_mix":"2026 年成長主要來自併購併表；FY2027 共識營收 +8.3% 靠量與新品，EPS +19.7% 另靠毛利率回升與回購。","runway_years":"無法計算：組合份額近三季未上升，以現有趨勢到不了 30%；品類滲透率事實表未涵蓋。","runway_post_y5":"🟡","endo_ceiling_basis":"投入資本、折舊攤銷與收購對價未涵蓋，內生天花板留空；共識 EPS 年複合 17.5% 高於營收成長 8.3%，缺口 9.2 個百分點歸因於毛利率回升與淨回購。無法證明在天花板內，情境按超出處理，空方機率取 30%。","segments":[{"item":"Alani Nu","value":"第三季淨銷售 4.101 億美元，年增約 24%；追蹤通路零售額 +57.9%，份額 9.8%"},{"item":"CELSIUS","value":"第三季淨銷售 3.568 億美元，年減約 6%；零售額 −7.0%，份額 9.1%"},{"item":"Rockstar","value":"第三季淨銷售 8,030 萬美元；零售額 −13.2%，保留 SKU 較去年少約 1%"},{"item":"海外","value":"第三季年增約 56%，管理層目標五年內占營收 15% 以上；目前金額事實表未涵蓋"}],"decay_signals":[{"signal":"毛利率連續年減","lit":true,"evidence":"Q1 年減 4.0、Q3 年減 4.5 個百分點；Q2 去年同期值未涵蓋，以 TTM 47.95% 低於 FY2025 的 50.39% 佐證。"},{"signal":"主力品牌市占近 12 個月縮減","lit":true,"evidence":"CELSIUS 美元份額由 11.2% 降至 9.1%。"},{"signal":"EPS 成長顯著高於營收成長","lit":true,"evidence":"共識 EPS 年複合 17.5%，FY2027 營收成長 8.3%，差 9.2 個百分點。"}],"trap_rating":"🔴"}}},"q4_capital":{"verdict":"資本配置還不能評高分：股權激勵幾乎沒有稀釋，但併購與回購的報酬無法用現有資料驗證。","reasoning":"股權激勵第三季 870 萬美元，占營收 1.0%，年化約市值 0.43%。前三季 FCF 3.99 億美元（營業現金流 4.502 億減資本支出 5,120 萬），第三季 1.277 億。TTM FCF 利潤率只有 6.09%，低於 FY2025 的 12.86%；用 TTM 營收約 31.75 億回推，2025 年第四季 FCF 約為 −2 億美元，很可能與配銷商終止費的收付時點有關，事實表未拆分。FCF 對淨利 FY2024 約 1.65 倍、FY2025 約 3.0 倍，但 FY2025 淨利偏低，這個比率不能當現金品質變好的證據。前三季現金去向：資本支出 5,120 萬、回購約 1.69 億，近 12 個月無併購完成，還債金額未涵蓋。淨現金 2,592 萬美元（含租賃的總債務 6.747 億、現金 7.006 億）。","fact_refs":["f_kpi4_sbc_gaap","f_kpi3_free_cash_flow_ocf_capex","f_peer_celh_fcf_margin_pct","f_net_debt_m","f_shares_diluted_m"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":true,"passed":null,"input":"營業利益由 FY2024 約 1.56 億增至 TTM 約 5.56 億美元，但收購對價與投入資本事實表未涵蓋，算不出已實現增量報酬。"},{"name":"buyback_yield","applicable":true,"passed":null,"input":"現價對 FY2026E EPS 殖利率 4.4%、FY2027E 5.3%；回購均價與 10 年期殖利率事實表未涵蓋，無法比較。"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"第三季 870 萬美元 × 4 ÷ 市值 80.58 億＝0.43%，低於每年 1.5%；以金額占市值代替淨稀釋率。"}]},"governance":{"capital_returns":[{"item":"2026 年前三季回購","value":"約 1.69 億美元，第三季約 4,500 萬，授權餘額約 9,100 萬（2026-11-05 CFO）"},{"item":"併購","value":"Alani Nu、Rockstar 整合已完成；對價與已實現報酬事實表未涵蓋"},{"item":"股息","value":"普通股股息事實表未涵蓋，情境以 0 計"}]}}},"q5_valuation":{"verdict":"現價 32.16 美元要求 2027～2028 年毛利率回升、EPS 年複合約 17.5%；我只相信一部分，基準 FY2027 EPS 1.62 低於共識 1.70，倍數合理但沒有折扣。","reasoning":"32.16 ÷ FY2026E 1.42＝22.65 倍；÷ FY2027E 1.70＝18.92 倍。共識 EPS 年複合 17.5%，PEG 1.29。要拿到年化 10%，五年後股價要 51.8 美元，以 19 倍算 FY2031 EPS 要 2.73，年複合約 14%；我的基準只有 12%，基準年化約 8%。12 個月：1.62 × 20 倍＝32.4 美元（+0.7%）；36 個月：2.08 × 20 倍＝41.6 美元（+29.4%）。股價低於 52、104、250 週均線（36.47、38.36、40.93），RSI 68.01，四週漲幅事實表未涵蓋。財報後的共識快照 FY1～FY3 修正都是 0%，很可能還沒納入第四季放緩，這是尚未反映的利空，在第一個確認數據出來前不加碼。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_pe_current","f_pe_percentile","f_ps_current","f_ps_percentile","f_ev_s_current","f_ev_s_percentile","f_ev_s_fwd","f_ev_m","f_rsi14","f_week26_return_pct","f_consensus_rev_fy1_pct","f_consensus_rev_fy2_pct","f_consensus_rev_fy3_pct","f_consensus_rev_3m_fy1_pct","f_ma_state","f_ma_w52","f_ma_w104","f_ma_w250","f_ma_slope_w250_pct"],"verdict_values":{"valuation":{"basis":"Fwd P/E，分母為 FY2026E 共識 EPS 1.42，輔以 FY2027E 倍數與 PEG。","tier":"品牌飲料，中型成長","peers":{"expanded":false,"reason":"事實表只有同業利潤率，沒有同業 Fwd P/E 或 EV/S；倍數對照承重但無資料，不自行補值。"},"fwd_pe":22.65,"peg":1.29,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"FY1 倍數 22.65 ÷ EPS 年複合 17.5%＝PEG 1.29，FY2 倍數 18.92 對應 1.08，落在 1～2 的合理區；EV 對 FY1 營收 2.52 倍。Trailing P/E、P/S、EV/S 雖低於僅有的 3～4 個年度端點，但端點少且含高成長期，不能當便宜證據；五年連續分位與同業倍數事實表未涵蓋。","upside_short_pct":0.7,"upside_mid_pct":29.4,"denominator_disputed":false,"denominator_note":"FY1 分母已有九個月實績，第三季調整後 EPS 0.41 與 GAAP 0.39 差距小，爭點在 FY2、FY3。市值與 EV 未含可轉換工具的完整稀釋，本次不以 EV 倍數作為承重依據。"}}},"q6_how_wrong":{"verdict":"最可能看錯的是把 Alani Nu 的強勢當成整個組合的體質，以及把毛利率下滑全歸給鋁價；衰退訊號亮三項，陷阱風險高。","reasoning":"亮燈三項：毛利率連續年減、CELSIUS 份額近 12 個月由 11.2% 掉到 9.1%、共識 EPS 成長比營收成長高 9.2 個百分點。反例是組合份額仍在 20.7%、前三季 FCF 3.99 億美元、資產負債表為淨現金，這不是典型的現金流衰退型陷阱；但三項都是基本面亮燈，不因此減計。歷史最大回撤與訴訟金額事實表未涵蓋。2026-08-06 法說迴避的第四季回升幅度與費用雜訊何時消退，2026-11-05 只部分補上，CELSIUS 回升仍未給幅度。","fact_refs":["f_kpi6_gross_margin","f_peer_celh_gross_margin_pct","f_consensus_rev_3m_fy1_pct","f_fwd_pe_latest","f_price_at_dd"],"verdict_values":{"trap":{"verdict":"🔴","label":"衰退訊號三項亮燈，要靠毛利率回升才解除"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":1.42,"pe":22.65,"basis":"FY2026E 共識 EPS（Koyfin 2026-11-07），與終端倍數同為當年度 EPS 口徑"},"eps":{"bull":[1.8,2.25,2.72,3.2,3.7],"base":[1.62,1.85,2.08,2.3,2.5],"bear":[1.3,1.25,1.3,1.35,1.4]},"pe":{"bull":24,"base":19,"bear":14},"p":{"bull":20,"base":50,"bear":30},"yield_pct":{"dividend":0,"net_buyback":0},"second_stage":{"bull_cagr_pct":12,"base_cagr_pct":7},"max_dd":{"lo":-55,"hi":-35,"basis":"歷史最大回撤事實表未涵蓋，改由情境推：空方 FY2027 EPS 1.30 × 13～16 倍＝16.9～20.8 美元，相對現價 32.16 為 −47%～−35%；再留約 8 個百分點給財報跳空與賣壓，下緣取 −55%。","trigger_time":null},"basis":{"bull":"CELSIUS 2027 年回到中個位數成長，Alani Nu 年增維持 15% 以上，海外提早達標；毛利率 2028 年回到 51%～52%，FY2031 EPS 3.70，年複合 21%；24 倍假設成長仍在中雙位數。","base":"FY2027、FY2028 EPS 低於共識約 5%，因鋁與柴油未回落；毛利率 FY2028 約 50%，FY2031 EPS 2.50，年複合 12%；EPS 路徑已含回購，淨回購殖利率填 0 避免重複計算。19 倍接近現在 FY2 倍數 18.92 倍；同業 Fwd P/E 事實表未涵蓋，無法附同業現值對照。","bear":"CELSIUS 續跌、Alani Nu 限定款效應退去、毛利率停在 45%～47%，EPS 五年大致不成長；14 倍取成長降至 10% 以下的倍數壓縮。空方機率 30%，依據是毛利率目標已延後、主力品牌仍衰退、內生天花板無法證明。"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"CELSIUS 零售額 −7%，管理層把回升時點推到 2027 年；毛利率 46.8%，低 50 目標延後；Alani Nu 第三季靠限定款 Witch's Brew 貢獻超過 1.3 億美元零售額。","assumption":"新品能把 CELSIUS 拉回成長，收益管理能補回直送組合與鋁價的壓力。","consequence":"五年後虧五成最可能的路徑：CELSIUS 持續失血、Alani Nu 限定款效應退潮、毛利率停在 45%～47%，EPS 1.25～1.40、倍數 13 倍左右，股價約 16～18 美元，虧 44%～49%。","ruling":"採納為主要下行路徑，空方機率 30%；與唯一致命點的毛利率部分重疊，CELSIUS 衰退另以觸發器監測。","watch":"每季毛利率、CELSIUS 零售額年增率、Alani Nu 剔除限定款後的零售額年增率。","evidence_refs":["channel_business_model_shift#2","competitive_share_entrants#3"],"fact_refs":["f_kpi6_gross_margin"]},{"view":"論點成功但股東經濟變差","evidence":"Alani Nu 零售額 +58%，淨銷售只有 +24%；Pepsi 占第三季營收 64.6%，去年同期 35.4%；直送比重上升推高交易投資。","assumption":"組合成長的價值會留在公司，而不是被配銷端與促銷分走。","consequence":"營收與份額都達標，但毛利率停在 48% 左右，EPS 增速追不上共識，倍數無法維持。","ruling":"部分採納。CFO 說 2027 年第二季起落差最乾淨，屆時可驗證；在此之前不把零售額成長當作股東經濟改善的證據。","watch":"2027 Q2 Alani Nu 零售額與淨銷售的落差、交易投資占總銷售比。","evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#1"],"fact_refs":["f_kpi0_revenue_gaap"]},{"view":"價格已反映太多","evidence":"FY2026 共識 EPS 由約 1.63 降到 1.42，股價反而由 30.16 漲到 32.16；財報後共識快照修正 0%，第四季放緩可能尚未納入。","assumption":"FY2027 EPS 1.70 站得住，22.65 倍的 FY1 倍數合理。","consequence":"若 FY2027 共識下修 10% 到 1.53，以 FY2 倍數 18.92 倍算約 28.9 美元，較現價低 10%。","ruling":"部分採納。倍數不貴但沒有折扣，下修風險大於上修風險，這也是不追的原因之一。","watch":"2027 年 3 月前 FY2027 共識 EPS。","evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#3"],"fact_refs":["f_fwd_pe_latest","f_consensus_eps_fy2"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ❌ → 本次 ❌","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=❌","side_b":"本次 ma=❌","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 30.16 → 本次 32.16（+6.6%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=30.16","side_b":"本次 price_at_dd=32.16","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 30.16 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 30.16 美元：五年期望值 前份未列，基準年化 前份未列，前份未列不對稱比","side_b":"本次情境、股價仍用 30.16 美元：Bull 價 88.8、Bear 價 19.6，五年期望值 +57.1%，基準年化 9.5%，不對稱比 3.7","ruling":"先換情境、股價不動：五年期望值與基準年化前份未列，無法比較。前份未列不對稱比，本次為 3.7。Bull、Bear 價位與股價無關，只受情境影響。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 30.16 美元：五年期望值 +57.1%，基準年化 9.5%，不對稱比 3.7","side_b":"本次情境、股價 32.16 美元：五年期望值 +47.4%，基準年化 8.1%，不對稱比 3.01","ruling":"再換股價、情境不動：起點價上漲 6.6%，五年期望值少 9.8 個百分點，基準年化少 1.4 個百分點，不對稱比由 3.7 降到 3.01。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"估值結論由偏便宜轉為合理","cause":"新證據","prior_field":["val"],"side_a":"2026-05-18：Fwd P/E 18.5 倍、PEG 0.86，評為便宜。","side_b":"2026-11-08：Fwd P/E 22.65 倍、PEG 1.29，評為合理。","ruling":"採 B 側。股價只漲 6.6%（30.16→32.16），倍數上升大部分來自 FY2026 共識 EPS 下修約 13%（前份 18.5 倍回推約 1.63，現為 1.42）。","evidence_level":"財報與共識快照；前份共識為回推值。","settle_metric":"FY2027 共識 EPS","if_then":["若第四季財報後 FY2027 共識低於 1.50，則不追，且估值結論不因股價下跌而上調。","若 FY2027 共識維持 1.70 以上且毛利率達 49%，則重跑研究。"],"evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#3"]},{"axis":"結論維持觀望，但陷阱風險升高","cause":"新證據","prior_field":["signal","trap"],"side_a":"前份：觀望，陷阱風險中等，前提是 CELSIUS 2027 年恢復 10% 以上成長。","side_b":"本次：仍觀望，衰退訊號亮三項：毛利率連續年減、CELSIUS 份額 11.2%→9.1%、EPS 成長高於營收成長 9.2 個百分點。","ruling":"採 B 側。Alani Nu 與前三季現金流讓論點還活著，所以不改成放棄；但陷阱風險由中等升為高。","evidence_level":"公司財報、10-Q 與法說。","settle_metric":"FY2027 上半年毛利率","if_then":["若 2027 年第一或第二季毛利率達 49% 以上，則重跑研究。","若 FY2027 全年毛利率低於 48%，則清倉，未持有則不建倉。"],"evidence_refs":["channel_business_model_shift#2","competitive_share_entrants#3"]},{"axis":"前份空值欄位首次填寫","cause":"方法變動","prior_field":["moat_trend","runway_post_y5","archetype","cycle_position","max_dd_pct","p_bull_pct","p_bear_pct"],"side_a":"前份這些欄位未填（null）。","side_b":"本次首次填寫：護城河方向→、五年後跑道中等、公司類型為轉機與特殊情境、情境機率 20／50／30、最大回撤 −35%～−55%；週期位置不適用，維持空值。","ruling":"前份沒有可比值，不算結論改變。","evidence_level":"格式差異","settle_metric":null,"if_then":[]},{"axis":"重新建倉條件改為毛利率事件","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"等 W104 站回或 Q3 26 核心品牌動能回升再建倉","side_b":"2027 年第一或第二季毛利率達 49% 以上，且非一次性因素；達成後重跑研究，不直接建倉。","ruling":"舊條件的品牌動能部分已落空（第三季零售額 −7%），均線條件與基本面無關。毛利率是 EPS 敏感度最大的單一項，所以建倉條件改綁毛利率，不設進場價。","evidence_level":"公司財報與法說","settle_metric":"單季毛利率","if_then":["若股價先站上 104 週均線 38.36 而毛利率未回升，則不追。","若股價下跌但毛利率達到 49%，則重跑研究，通過後分批反買。"]},{"axis":"Single Thing 由未設定改為 FY2027 毛利率","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設定唯一致命點（null）。","side_b":"FY2027 全年毛利率低於 48%（2028 年 2～3 月年報揭露），即 TTM 47.95% 沒有改善。","ruling":"Single Thing 首次設定。選毛利率而不選 Pepsi 終止合約，因為後者雖然最戲劇化，但 12～24 個月機率低；毛利率每 1 個百分點約影響 EPS 6%，是敏感度最大的單一項。","evidence_level":"以 FY2027 共識營收推算，稅率為假設值。","settle_metric":"FY2027 全年毛利率","if_then":["若 FY2027 毛利率低於 48%，則清倉。","若 FY2027 毛利率達 49% 以上，則解除此項風險並重估基準情境。"]},{"axis":"清倉與減碼門檻首次設定","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設清倉或減碼門檻（null）。","side_b":"FY2027 毛利率低於 48% 清倉；組合份額連兩季低於 20% 清倉；CELSIUS 零售額 2027 Q2、Q3 皆為負則減碼一半；FY2027 共識 EPS 低於 1.50 減碼一半。","ruling":"前份只有文字警戒，本次改成可量測的門檻。","evidence_level":"格式差異","settle_metric":null,"if_then":[]},{"axis":"前份假設驗證點已失效","cause":"新證據","prior_field":null,"side_a":"前份：Q4 26 CELSIUS 年增重回 10% 以上；2027 年 CELSIUS 年增 ≥10%；Alani Nu 2027 年增 ≥40%；FY26 共識 EPS 上修至約 1.80 以上（前份摘要數字缺首位，依 18.5 倍回推）。","side_b":"第三季 CELSIUS 零售額 −7%，管理層把回升時點推到 2027 年；FY26 共識降到 1.42；Alani Nu 帳面年增約 24%。","ruling":"前份 CELSIUS 與共識上修的門檻已實質失敗，本次重設，不沿用；Alani Nu 零售額達標但帳面未達，改用淨銷售驗證。","evidence_level":"公司財報、法說與共識快照","settle_metric":"CELSIUS 零售額年增率與 Alani Nu 淨銷售年增率","if_then":["若 2027 Q2 CELSIUS 零售額仍為負，則停止加碼。","若 2027 Q3 達 3% 以上，則恢復對該假設的信心並重跑研究。"]},{"axis":"CELSIUS 回到成長的時點","cause":"新證據","prior_field":null,"side_a":"2026-08-06 CEO：第三季與第二季相近，年底前回到成長，第四季是緩慢累積。","side_b":"2026-11-05 CEO：消費轉折要到 2027 年循環過 SKU 精簡後才出現；年底只談週銷維持在 5,000 萬美元區間時部分週次可小幅成長或持平。","ruling":"屬程度差異，可調和。採 B 側時點，驗證點放在 2027 Q2～Q3。管理層把衰退歸因於 SKU 精簡與高基期，列為未證；若 2027 Q2 仍負成長，視為歸因不成立。","evidence_level":"法說原話","settle_metric":"CELSIUS 追蹤通路週銷金額與年增率","if_then":["若 2027 Q2 零售額年增為負，則停止加碼。","若 2027 Q2、Q3 皆為負，則減碼一半。"]},{"axis":"毛利率恢復時程","cause":"新證據","prior_field":null,"side_a":"前份摘要：管理層指引 2026 下半年回到 low 50s。","side_b":"2026-11-05 CFO：全年維持 high 40s，低 50 目標要比一年前預期更久，商品成本沒有改善。","ruling":"採 B 側，管理層已退讓。鋁與柴油、直送組合、整合成本的各自占比拆不開，所以看結果不看歸因。","evidence_level":"法說原話與 10-Q","settle_metric":"單季毛利率、交易投資占總銷售比","if_then":["若 2027 上半年毛利率低於 48%，則不追並下修基準 EPS。","若達 49% 以上，則重跑研究。"],"evidence_refs":["channel_business_model_shift#2"]},{"axis":"Alani Nu 零售成長與帳面落差","cause":"新證據","prior_field":null,"side_a":"第三季零售額 +58%，剔除限定款仍 +50%。","side_b":"淨銷售 +24%，原始落差約 34 個百分點；CFO 說扣除非即飲與合約攤銷後約 24～25 個百分點。","ruling":"可調和，一部分是轉換直送的暫時因素，一部分是交易投資的長期成本；2027 年第二季前無法裁決。","evidence_level":"法說原話","settle_metric":"2027 Q2 零售額與淨銷售年增率落差","if_then":["若 2027 Q2 落差仍大於 15 個百分點，則視為結構性，下修基準毛利率。","若縮到 15 個百分點內，則支持基準情境。"]},{"axis":"回購承諾的步調","cause":"新證據","prior_field":null,"side_a":"2026-08-06 CFO：打算今年用完 3 億美元授權。","side_b":"2026-11-05：第三季只買約 4,500 萬美元（第二季約 1 億），授權餘額約 9,100 萬。","ruling":"尚未違約，但步調放慢，要第四季買滿才算兌現。回購均價未涵蓋，無法評斷買得好不好。","evidence_level":"法說原話","settle_metric":"第四季回購金額","if_then":["若第四季回購低於 9,100 萬美元，則把承諾記為未兌現，基準 EPS 不再上調回購效果。"]},{"axis":"賣方目標價與本次結論","cause":"新證據","prior_field":null,"side_a":"賣方平均目標價 41.10～60.57 美元，各站最高 75、最低 26。","side_b":"本次 12 個月基準約 32.4 美元。","ruling":"本次比賣方悲觀。差異在成長基準：賣方模型仍放 FY2027 EPS 1.70，需要毛利率回升與第四季放緩不影響 2027 年。目標價來源日期不一，全距 75 對 26 為 2.9 倍，超過 2.5 倍，因此不引用為支持，也調低自身機率信心。","evidence_level":"二手聚合站，日期不一致","settle_metric":"第四季財報後目標價與共識修正","if_then":["若財報後共識 FY2027 上修且毛利率達標，則承認判斷過於保守並重跑研究。"],"evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#3"]},{"axis":"現在就買的最強論證","cause":"新證據","prior_field":null,"side_a":"Alani Nu 零售額剔除限定款仍 +50%，整合已完成，2027 新品與收益管理同時啟動；淨現金、前三季 FCF 3.99 億美元，FY2027 倍數 18.92 倍，第四季雜訊可能是最後低點。","side_b":"毛利率尚未回升，共識未反映第四季放緩，CELSIUS 仍衰退，FCF 可能受終止費補償影響，股價低於三條週均線。","ruling":"不買。買方論點成立的關鍵是毛利率，毛利率數據 2027 年上半年就會出來，等待成本低於先買後看錯的成本。","evidence_level":"公司財報與法說","settle_metric":"2027 上半年毛利率","if_then":["若毛利率達 49% 以上，則重跑研究，通過後分批反買。","若股價先漲而毛利率未回升，則不追。"]}],"triggers":[{"n":1,"text":"FY2027 全年毛利率低於 48%","type":"Single Thing","maps_to":"R1","metric":"FY2027 全年毛利率","threshold":"低於 48%","action":"清倉；未持有則不建倉","source_freq":"10-K，每年一次","date":"2028-03"},{"n":2,"text":"2027 年第一或第二季毛利率達 49% 以上，重跑研究","type":"估值rearm","maps_to":"H1","metric":"單季毛利率","threshold":"≥49%","action":"重跑研究，通過後分批反買，首筆不超過正常倉位三分之一","source_freq":"10-Q，每季","date":"2027-08"},{"n":3,"text":"CELSIUS 追蹤通路零售額 2027 Q2 轉正","type":"假設驗證","maps_to":"H2","metric":"CELSIUS 零售額年增率","threshold":"2027 Q2 ≥0%，Q3 ≥3%","action":"未達則停止加碼；連兩季為負則減碼一半","source_freq":"法說與新聞稿，每季","date":"2027-08"},{"n":4,"text":"Alani Nu 淨銷售年增連兩季低於 10%","type":"風險","maps_to":"R3","metric":"Alani Nu 淨銷售年增率","threshold":"連兩季低於 10%","action":"減碼一半","source_freq":"新聞稿，每季","date":"2027-11","evidence_refs":["end_markets#2"]},{"n":5,"text":"FY2027 共識 EPS 跌破 1.50 美元","type":"減碼","maps_to":"R1","metric":"FY2027 共識 EPS","threshold":"低於 1.50","action":"減碼一半；未持有則不追","source_freq":"共識快照，每月","date":"2027-03","evidence_refs":["capital_markets_pricing#0"]},{"n":6,"text":"Pepsi 配銷合約不利修訂或終止","type":"風險","maps_to":"R4","metric":"Pepsi 合約條款","threshold":"公告不利修約或終止","action":"清倉","source_freq":"8-K，事件發生時","date":null,"evidence_refs":["customer_concentration_credit#1"]},{"n":7,"text":"集體訴訟獲認證且不利和解","type":"風險","maps_to":"R6","metric":"訴訟進度與金額","threshold":"獲認證且和解或判賠達 5,000 萬美元","action":"減碼一半","source_freq":"10-Q 法律程序章節，每季","date":null,"evidence_refs":["lawsuit_class_action#0"]},{"n":8,"text":"第四季財報全面複審","type":"複審日期","maps_to":"H1","metric":"第四季帳面營收年增、毛利率、2027 年展望","threshold":"全面複審","action":"重看共識修正與情境機率；股價先漲而毛利率未回升則不追","source_freq":"8-K 新聞稿與法說","date":"2027-03","evidence_refs":["end_markets#2"]},{"n":9,"text":"組合美元份額連兩季低於 20%","type":"清倉","maps_to":"H3","metric":"美國追蹤通路組合份額","threshold":"連兩季低於 20%","action":"改判護城河轉弱，清倉","source_freq":"法說與新聞稿，每季","date":"2027-11"}],"kill_metrics":[{"metric":"FY2027 全年毛利率","bear_threshold":"低於 48% 清倉","window":"2028 年 3 月前年報揭露","source":"公司 10-K 與財報新聞稿","last_status":"warning"},{"metric":"CELSIUS 品牌追蹤通路零售額年增率","bear_threshold":"2027 Q2 與 Q3 皆低於 0% 減碼一半","window":"2027 年 8 月至 11 月財報","source":"公司法說引述掃描數據","last_status":"warning"},{"metric":"Alani Nu 淨銷售年增率","bear_threshold":"連兩季低於 10% 減碼一半","window":"2027 年每季","source":"公司新聞稿品牌別營收","last_status":"ok"},{"metric":"美國追蹤通路組合美元份額","bear_threshold":"連兩季低於 20% 清倉","window":"2027 年每季","source":"公司法說與新聞稿引述追蹤通路數據","last_status":"ok"},{"metric":"FY2027 共識 EPS","bear_threshold":"低於 1.50 美元減碼一半","window":"2027 年 3 月前","source":"Koyfin 共識快照","last_status":"ok"},{"metric":"Pepsi 配銷合約","bear_threshold":"公告不利修約或終止則清倉","window":"持續","source":"SEC 8-K Item 1.01","last_status":"ok"}],"evidence_dismissed":[{"ref":"reg_tariff_export#2","reason":"這是 10-K 的通用風險因子，原文沒有任何已發生的出口管制、受影響市場或金額，事實表也沒有海外營收金額可衡量曝險，無法形成可監測的論點。"},{"ref":"regulatory_antitrust#1","reason":"原文是條件句的風險揭露，未載任何 FTC 或州政府已立案的案件；已知的虛假廣告集體訴訟已另列法律風險，不重複計算。"}],"action_conditions":{"rearm_trigger":"2027 年第一或第二季毛利率達 49% 以上且非一次性因素；達成後重跑研究，不直接建倉","exec_line":"目前不建倉。毛利率條件達成後重跑研究，通過才分批買進，首筆不超過正常倉位三分之一；若已持有，第四季財報前不加碼，FY2027 毛利率低於 48% 清倉。","holding_cap":"未達重啟條件前不建倉；達成後上限 3%"}},"decision_inputs":{"signal":"B","ma":"❌","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":null,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等 2027 年第一或第二季毛利率達 49% 以上，不設進場價；股價先漲而毛利率未回升則不追。"},"thesis":{"H":[{"id":"H1","text":"毛利率能靠收益管理、北卡第二條產線與直接採購回升，FY2027 回到 49% 以上，FY2028 回到 50% 以上。","2y":"FY2027 毛利率 ≥49%，FY2028 ≥50%","5y":"FY2031 毛利率 50%～52%，接近管理層低 50 目標","10y":null,"threshold":"FY2027 全年毛利率 ≥49%（TTM 為 47.95%）","source":"公司 10-Q、10-K 與法說毛利率說明；鋁價與中西部溢價","drift_rule":"TTM 毛利率低於當期路徑，連 2 季差 1 個百分點以上為削弱，連 3 季差 2 個百分點以上為反轉（1 個百分點約等於 EPS 6%）。"},{"id":"H2","text":"CELSIUS 品牌在 2027 年靠新品與主力 SKU 回到成長，而且不是靠加碼促銷買來的。","2y":"2027 Q3 追蹤通路零售額年增 ≥3%","5y":"CELSIUS 美國追蹤通路份額回到 10% 以上（第三季 9.1%）","10y":null,"threshold":"2027 Q2 零售額年增 ≥0%、Q3 ≥3%，同期品牌交易投資占比不上升","source":"公司法說的掃描數據與品牌別營收","drift_rule":"連 2 季低於門檻 5 個百分點以上為削弱，連 3 季低於門檻 10 個百分點以上為反轉。"},{"id":"H3","text":"Alani Nu 在直送與海外擴張帶動下維持高成長，零售與帳面落差在 2027 年第二季後收斂，海外占比朝 15% 前進。","2y":"FY2027 Alani Nu 淨銷售年增 ≥15%；2027 Q2 起零售與帳面落差縮到 15 個百分點內","5y":"2031 年海外營收占比超過 15%（管理層目標）；組合美國份額 ≥22%","10y":null,"threshold":"FY2027 Alani Nu 淨銷售年增 ≥15%","source":"公司季報品牌別營收、法說橋接表","drift_rule":"連 2 季低於門檻 5 個百分點以上為削弱，連 3 季低於門檻 10 個百分點以上為反轉。"}],"R":[{"id":"R1","text":"毛利率回不來：鋁與柴油居高、公司未避險、轉嫁受競爭限制，直送組合持續拉高交易投資，關稅影響也難估。","h_ref":"H1","clock":"🔥","threshold":"2027 上半年毛利率低於 48%","evidence_refs":["channel_business_model_shift#2","geo_supply_chain#1","reg_tariff_export#0","reg_tariff_export#1","supply_demand_durability#3"]},{"id":"R2","text":"CELSIUS 份額持續流失：2025 Q3 已年減 0.5 點至 11.2%，2026 Q3 再降至 9.1%，新品若補不上，SKU 精簡的說法就站不住。","h_ref":"H2","clock":"⚡","threshold":"2027 Q2 追蹤通路零售額年增低於 0%","evidence_refs":["competitive_share_entrants#3"]},{"id":"R3","text":"Alani Nu 成長依賴限定款，CFO 已預告第四季有促銷時點、整合與大客戶現金管理雜訊；高基期出現後帳面可能快速降速。","h_ref":"H3","clock":"⚡","threshold":"Alani Nu 淨銷售年增連 2 季低於 10%","evidence_refs":["end_markets#2"]},{"id":"R4","text":"Pepsi 集中度：2025 年占營收 43.2%，2026 前九月 61.3%，第三季 64.6%。Pepsi 調整配銷條款或策略，公司幾乎沒有替代方案。前份的未成年購買立法風險也保留在此。","h_ref":"H1+H3","clock":"🐢","threshold":"Pepsi 公開重新評估配銷條款，或任一州通過 18 歲以上才可購買能量飲的法案（現況事實表未涵蓋）","evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#1"]},{"id":"R5","text":"品類放緩與 GLP-1：Statista 預估全球成長 2027 年降至約 3.32%，AlixPartners 模型估 GLP-1 使能量飲與咖啡約 4% 年化下滑；研調之間差距大，只列慢變數。","h_ref":"H2+H3","clock":"🐢","threshold":"組合零售額年增連 4 季低於 5%","evidence_refs":["supply_demand_durability#2","substitute_technology#2"]},{"id":"R6","text":"未決訴訟：證券、衍生、channel stuffing 與虛假廣告集體訴訟，以及每箱 10 美分的版稅訴訟，律所也在調查證券詐欺主張；金額與時點事實表未涵蓋，無法估算。","h_ref":"H1","clock":"🐢","threshold":"集體訴訟獲認證且和解或判賠達 5,000 萬美元（約基準 FY2027 淨利 12%）","evidence_refs":["major_events#0","lawsuit_class_action#0","lawsuit_class_action#1","lawsuit_class_action#2"]},{"id":"R7","text":"供應鏈：不完全自有工廠，專用罐供應商少，且供應鏈主管職位目前由代理人選擔任，銜接期出錯會直接反映在毛利率與缺貨。","h_ref":"H1","clock":"🔥","threshold":"任一季因鋁罐短缺或代工中斷使毛利率單季下滑 1 個百分點以上","evidence_refs":["geo_supply_chain#0"]}],"single_thing":{"description":"FY2027 全年毛利率低於 48%（2028 年 2～3 月年報揭露），即 TTM 47.95% 沒有改善。","why_fatal":"這是數學上最大的單一敏感度：以 FY2027 共識營收 34.5 億美元算，毛利率每差 1 個百分點，稅前少 3,450 萬美元，約等於 EPS 0.10～0.11 美元（稅率假設 23%，事實表未涵蓋；股數 2.5056 億），約為共識 1.70 的 6%；同樣影響約要 CELSIUS 品牌營收差 7%（貢獻率假設 35%）。","if_happens":"基準路徑失效，情境落到空方，FY2031 EPS 看 1.40 附近；未持有則不建倉，已持有則清倉。","how_monitor":"每季毛利率與交易投資占總銷售比；鋁價、中西部溢價與柴油；2027 年上半年先看是否達 48.5% 以上。","probability":"約 30%（12～24 個月）"}},"appendix_a":{"growth_durability":5,"quality_score":5,"ai_risk":"🟢","long_term_confidence":"低","fpe_fy2":18.92,"peg_fy2":1.08,"stress":{"pass":null,"total":null}},"eps_meta":{"base_eps_path":{"FY2025A":0.25,"FY2026E":1.42,"FY2027E":1.7,"FY2028E":1.96},"fy_end_month":12,"eps_basis":"FY2026E～FY2028E 為 Koyfin 共識（2026-11-07），研判為調整後口徑（第三季調整後 EPS 0.41，與全年 1.42 量級一致），家數事實表未涵蓋。FY2025A 0.25 為 GAAP 稀釋 EPS，FY2025 調整後 EPS 事實表未涵蓋，兩者口徑不同，不得用來算三年 CAGR；本次成長率只用 FY2026E→FY2028E 年複合 17.5%。"},"catalysts":[{"date":"2026-11-30","date_precision":"month","type":"product","event":"兩款 CELSIUS 新 SKU 於感恩節前後上架，Alani Nu 冬季限定款 11 月底上市","impact":"中","watch":"限定款零售額與 CELSIUS 週銷是否維持 5,000 萬美元區間"},{"date":"2027-01-31","date_precision":"month","type":"product","event":"2027 年第一波新品上市，含 CELSIUS 新口味與新包裝","impact":"高","watch":"鋪貨點數與週銷速度，是否靠加碼促銷"},{"date":"2027-03-31","date_precision":"quarter","type":"guidance","event":"2026 年第四季財報，帳面成長放緩，並說明 2027 年計畫","impact":"高","watch":"第四季毛利率、交易投資占比、FY2027 共識修正"},{"date":"2027-05-31","date_precision":"month","type":"guidance","event":"2027 年第一季財報，第一個收益管理計畫生效後的毛利率讀數","impact":"高","watch":"毛利率是否達 49%"},{"date":"2027-08-31","date_precision":"month","type":"guidance","event":"2027 年第二季財報，CFO 所稱 Alani Nu 零售與帳面對照最乾淨的一季","impact":"高","watch":"Alani Nu 落差、CELSIUS 零售額年增是否轉正"},{"date":"2027-12-31","date_precision":"quarter","type":"product","event":"Alani Nu 於部分海外市場上市","impact":"中","watch":"海外營收金額與占比是否開始揭露"}],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8w(原9)","pacing":["row4：週線❌，進場節奏強制分批（starter 1/3＋趨勢確認後加碼），頁首掛「⚠️ 週線趨勢未確認，逢回分批勿接刀」"],"holding_cap":null,"audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='C'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":true,"basis":"ma='❌'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"輸入缺(momentum_overheated=null)，依保守方向處理：不視為觸發","input_gap":["momentum_overheated"]},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟡', moat_trend='→', week26=-0.4, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='轉機/特殊情境', cycle_position=None, moat='C', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":false,"basis":"signal='B', val='🟡'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":true,"basis":"signal='B', val='🟡', ma='❌'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟡', ma='❌'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟡', ma='❌'"},{"row":"8w","condition":"判斷者宣告 wait_for_price（價格合理但要等）→ 原 row9 進場改觀望（等價格）","hit":true,"basis":"wait_for_price=True, 等待條件='等 2027 年第一或第二季毛利率達 49% 以上，不設進場價；股價先漲而毛利率未回升則不追。'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"requires_critic":[]}}
```

---

## ⑤ 覆蓋面（程式判定，你回的 ⑤ 燈號會被覆寫）

燈號 🟢：核心軸皆有證據或不適用，非核心軸也沒有空軸。plan 時 archetype 為「品質複利成長」、判斷者歸「轉機/特殊情境」，轉機/特殊情境 的專屬核心軸未採證（不計燈號）：turnaround_catalyst_timeline、turnaround_liquidation_floor。

⑤ 的 reason 只需評論：空軸的查詢詞是否切題、判斷有沒有交代缺口對結論的影響。

---

## 尾段：回覆格式

只回一個 JSON 陣列，①–⑧ 每條一個元素，八個全出，不得跳號、不得多列，陣列外不得有任何文字（不加前言、不加 markdown 圍欄、不加附註）：

```json
[{"item": "①", "light": "🔴|🟡|🟢", "judgment_path": "$.路徑", "reason": "一句話"}]
```
