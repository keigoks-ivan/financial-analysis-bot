你是 DD 管線 v20 的判斷層閘（gate），標的 FIX（20261013）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（31 條）
- `f_kpi0_gaap`（q1_business）｜營收（GAAP）＝3265.656 USD M｜期間與口徑：Q2 FY2026（季末 2026-06-30，公告於 2026-07-23）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 8-K Ex.99.1（numbers.latest_quarter_kpis.items[0]，as_of Q2 FY2026（季末 2026-06-30，公告於 2026-07-23））
  - 註記：查無（未取得該季共識）
- `f_kpi2_gaap`（q1_business）｜GAAP 營業利益／利益率＝557.966 USD M（利益率 17.1%）｜期間與口徑：Q2 FY2026（季末 2026-06-30，公告於 2026-07-23）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 8-K Ex.99.1（numbers.latest_quarter_kpis.items[2]，as_of Q2 FY2026（季末 2026-06-30，公告於 2026-07-23））
  - 註記：查無
- `f_kpi6_backlog`（q1_business）｜Backlog（在手訂單）＝14060 USD M｜期間與口徑：Q2 FY2026（季末 2026-06-30，公告於 2026-07-23）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 8-K Ex.99.1；same-store 13,700M（numbers.latest_quarter_kpis.items[6]，as_of Q2 FY2026（季末 2026-06-30，公告於 2026-07-23））
  - 註記：查無
- `f_peer_fix_gross_margin_pct`（q2_moat）｜FIX 毛利率＝25.66 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.FIX.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_kpi5`（q1_business）｜管理層指引＝— n/a｜期間與口徑：Q2 FY2026（公告於 2026-07-23）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司新聞稿 8-K Ex.99.1（numbers.latest_quarter_kpis.items[5]，as_of Q2 FY2026（公告於 2026-07-23））
  - 註記：無數字指引；僅定性：optimistic about our results for the remainder of 2026 and well into 2027
- `f_peer_fix_operating_margin_pct`（q2_moat）｜FIX 營業利益率＝16.45 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.FIX.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_fix_fcf_margin_pct`（q2_moat）｜FIX FCF 利潤率＝19.24 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.FIX.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_eme_gross_margin_pct`（q2_moat）｜EME 毛利率＝19.43 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.EME.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_eme_operating_margin_pct`（q2_moat）｜EME 營業利益率＝9.6 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.EME.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_iesc_operating_margin_pct`（q2_moat）｜IESC 營業利益率＝12.38 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.IESC.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_pwr_operating_margin_pct`（q2_moat）｜PWR 營業利益率＝6.12 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.PWR.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝49.01 USD/share｜期間與口徑：2026-10-08／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261008.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-10-08）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝60.18 USD/share｜期間與口徑：2026-10-08／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261008.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-10-08）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝73.85 USD/share｜期間與口徑：2026-10-08／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261008.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-10-08）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝12982.38 USD m｜期間與口徑：2026-10-13／yfinance revenue_estimate 0y 平均（10 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-10-13）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝15446.4 USD m｜期間與口徑：2026-10-13／yfinance revenue_estimate +1y 平均（10 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-10-13）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi3_fcf`（q4_capital）｜自由現金流（FCF）＝999.32 USD M｜期間與口徑：Q2 FY2026（季末 2026-06-30，公告於 2026-07-23）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 8-K Ex.99.1（營業現金流 1,139.4M − 資本支出 141.4M）（numbers.latest_quarter_kpis.items[3]，as_of Q2 FY2026（季末 2026-06-30，公告於 2026-07-23））
  - 註記：查無
- `f_kpi4_sbc`（q4_capital）｜SBC 占營業利益＝1.65 %｜期間與口徑：Q2 FY2026（季末 2026-06-30，公告於 2026-07-23）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：SBC 9.206M 取自 yfinance quarterly_cashflow（新聞稿未揭露），÷ 新聞稿 GAAP 營業利益 557.97M；占營收約 0.28%（numbers.latest_quarter_kpis.items[4]，as_of Q2 FY2026（季末 2026-06-30，公告於 2026-07-23））
  - 註記：n/a
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝-1536.49 USD m｜期間與口徑：2026-10-13／yfinance 最新一季：總債務 369.91、現金 1906.4（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-10-13）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝0.183 %｜期間與口徑：2026-10-13／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-10-13）
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝35.19 m shares｜期間與口徑：2026-10-13／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-10-13）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝1638.05 USD｜期間與口徑：2026-10-12（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-10-12（RTH 收盤，UTC））
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝40.31 x｜期間與口徑：2026-10-12（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-10-12（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝100.0 %｜期間與口徑：2026-10-12（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-10-12（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝35.01 x｜期間與口徑：2026-10-08／分母＝FY1 EPS 49.01，分子＝快照價 1715.69｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-10-08）
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝12.33 %｜期間與口徑：2026-07-16 → 2026-10-08／FY1 共識 EPS 43.63 → 49.01（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261008.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-10-08）
- `f_consensus_rev_fy1_pct`（q5_valuation）｜FY1 共識修正＝0.0 %｜期間與口徑：2026-10-08／兩份 Koyfin 快照之間的 EPS 修正幅度（49.01 → 49.01）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261008.xlsx（numbers.consensus_revision.fy1.revision_pct，as_of 2026-10-08）
- `f_ps_current`（q5_valuation）｜P/S（現值）＝5.13 x｜期間與口徑：2026-10-12（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-10-12（RTH 收盤，UTC））
- `f_ev_s_fwd`（q5_valuation）｜EV/S（EV ÷ FY1 共識營收）＝4.32 x｜期間與口徑：2026-10-13／f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）｜kind：estimate
  - 來源：—（numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m，as_of 2026-10-13）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rsi14`（q5_valuation）｜RSI(14)＝46.42｜期間與口徑：2026-10-12（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-10-12（RTH 收盤，UTC））
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝0.72 %｜期間與口徑：2026-10-12（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-10-12（RTH 收盤，UTC））

### findings_digest 中方向為負或來源衝突的條目（10 條）
- `competitive_share_entrants#1`（competitive_share_entrants｜方向 -｜狀態 ok）：Zacks 文章列出 FIX 風險包含專案延遲、勞動成本通膨、競爭加劇與執行風險；未量化份額
  - 來源：Nasdaq/Zacks: Comfort Systems Stock Trading at a Premium: Buy, Hold or Fold?（as_of 2026-08-31）｜affects：decision_inputs.bear、thesis.R
- `customer_concentration_credit#0`（customer_concentration_credit｜方向 -｜狀態 ok）：FY2025 10-K：最大單一客戶占 2025 合併營收 12.8%、占 2025/12/31 應收帳款 10.2%；信用風險主要來自總承包商、業主/開發商、商業與工業公司，公司對工程有留置權
  - 來源：SEC EDGAR Comfort Systems USA Form 10-K FY2025 (concentration of credit risk note)，經搜尋摘要轉述，未讀全文（as_of 2026-02-26）｜affects：decision_inputs.bear、thesis.R
- `customer_concentration_credit#2`（customer_concentration_credit｜方向 -｜狀態 ok）：科技（資料中心）相關工程占營收比重：Nasdaq/Zacks 文稱 40%（前一年 31%），另一第三方摘要稱 2025 年約 45%，兩數字口徑不一致
  - 來源：Nasdaq/Zacks: Comfort Systems' Tech and Data Push: Growth or Concentration Risk?（as_of 2025-12-31）｜affects：decision_inputs.bear、thesis.R
- `supply_demand_durability#3`（supply_demand_durability｜方向 -｜狀態 ok）：含資料中心工作的承包商 backlog 比其他承包商長約四個月；2026 年 4 月 backlog 增幅幾乎全來自有資料中心業務的大型承包商，其他規模公司 backlog 皆低於去年；非住宅民間營建支出已連續七個月下滑
  - 來源：contractorplus.app Construction Backlog Indicator April 2026 / Wiss 2026 outlook（as_of 2026-04-30）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：Motley Fool 報導：FIX 在財報風險章節明確點出關稅風險（泛指關稅，非 Section 232 專指）；搜尋摘要另稱公司倚賴鋼、鋁、銅與進口零組件。
  - 來源：Motley Fool, Why Comfort Systems USA Stock Slid 17% Last Month（as_of 2025-03-07）｜affects：decision_inputs.bear、valuation
- `reg_tariff_export#2`（reg_tariff_export｜方向 -｜狀態 ok）：PwC（2026-02-26）：最高法院駁回 IEEPA 關稅後，政府改以其他授權宣布新全球關稅；E&C 產業核心問題是政策波動。摘要稱 2026 年 4 月時鋼鋁銅製品 50%、衍生品 25%、含此類金屬的工業電氣設備（變壓器、配電盤、導管系統）15%，全球基準 10% 至 2026 年 7 月；之後是否變動未確認。
  - 來源：PwC, Building in uncertainty（as_of 2026-02-26）｜affects：decision_inputs.bear、valuation
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：10-K 風險因素：公司、供應商與客戶自外國供應商進口部分原料、零組件與產品；貿易政策變動可能帶來關稅與貿易障礙。
  - 來源：Comfort Systems USA Form 10-K FY2025 (SEC)（as_of 2026-02-20）｜affects：decision_inputs.bear、thesis.R
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：10-K（FY2024）風險因素：若無法將關稅成本轉嫁客戶，經營結果可能受重大不利影響。
  - 來源：Comfort Systems USA Form 10-K FY2024 (SEC)（as_of 2025-02-20）｜affects：decision_inputs.bear、thesis.R
- `geo_supply_chain#2`（geo_supply_chain｜方向 -｜狀態 ok）：公司依賴第三方分包商與設備／材料供應商；供應商未如期履約會損及執行與獲利（一般性依賴，未點名單一供應商或地區）。
  - 來源：Comfort Systems USA Form 10-K FY2025 (SEC)（as_of 2026-02-20）｜affects：decision_inputs.bear、moat_trend
- `geo_supply_chain#3`（geo_supply_chain｜方向 -｜狀態 ok）：風險摘要稱商用 HVAC 設備、配電開關設備、大型發電機交期最長，常超過六個月（第三方彙整 SEC 揭露，非 10-K 原頁讀取）。
  - 來源：policyrisk.com FIX company risk summary（as_of 2026-02-20）｜affects：thesis.R、decision_inputs.bear

### 事實表自陳的缺口（2 條）
- q2_moat：evidence.numbers.peer_financials 該欄整欄為 null（常見於未單獨揭露研發的業者），事實表 agent 若能從財報補就補，補不到即為缺口，判斷者不得自行估。
- q6_how_wrong：digest.qa_flags 有 1 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/FIX_20261013/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":3042.0,"bear_5y_price":640.0,"p_bull_pct":25,"p_bear_pct":30,"upside_5y_pct":8.8,"ev5y_pct":7.1,"irr_base_pct":1.7,"asym_ratio":1.2,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":49.01,"pe":33.42,"basis":"FY2026 共識 EPS 49.01（Koyfin 2026-10-08），現價 1,638.05÷49.01＝33.42 倍；終端倍數同以當年度 EPS 為分母"},"eps":{"bull":[64.0,80.0,94.0,106.0,117.0],"base":[60.2,71.0,75.0,78.0,81.0],"bear":[56.0,47.0,38.0,36.0,40.0]},"pe":{"bull":26,"base":22,"bear":16},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0.183,"net_buyback":0.25},"second_stage":{"bull_cagr_pct":10,"base_cagr_pct":6},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### FIX_Q1_2026_Earnings_Call_20260424.md
- 2026-04-24｜William George, CFO｜guidance：Management guided full-year 2026 same-store revenue growth to a mid-to-high 20% percentage range.（原話："in the mid to high 20% range."）
- 2026-04-24｜William George, CFO｜guidance：CFO guided full-year effective tax rate to approximately 23%.（原話："our full year effective tax rate to be around 23%."）
- 2026-04-24｜William George, CFO｜margin：CFO stated Q1 2026 gross profit percentage rose to 26.3% versus prior year.（原話："gross profit percentage grew to 26.3% this quarter"）
- 2026-04-24｜William George, CFO｜margin：CFO said gross profit margins are expected to continue at recent averaged levels.（原話："We currently expect that gross profit margins will"）
- 2026-04-24｜William George, CFO｜margin：CFO reported SG&A fell to 9.4% of revenue in Q1 2026 versus prior year.（原話："SG&A as a percentage of revenue was 9.4% this quarter"）
- 2026-04-24｜Brian Lane, CEO｜competition：CEO cited the company's traveling workforce as an advantage for serving data centers across dispersed geographies.（原話："we have a significant traveling workforce."）
- 2026-04-24｜Brian Lane, CEO｜capital_allocation：CEO announced a quarterly dividend increase to $0.80 per share.（原話："another increase to our quarterly dividend to $0.80"）
- 2026-04-24｜William George, CFO｜capital_allocation：CFO guided full-year CapEx to about 5% of revenue.（原話："CapEx will be in the range of 5% of revenue."）
- 2026-04-24｜William George, CFO｜capital_allocation：CFO described the pending electrical contractor acquisition as expected to carry EBITDA margins of 8-10%.（原話："EBITDA margins in the 8% to 10% range."）
- 2026-04-24｜Trent McKenna, President & COO｜product：COO said the company is on track to reach 4 million square feet of modular capacity by year-end.（原話："We are on track to have 4 million square feet"）
- 2026-04-24｜Samuel Kusswurm, Analyst (William Blair)｜risk：Analyst raised the risk of state-level data center bans or power access restrictions in regions the company serves.（原話："data center bans or even limiting access to power."）
- 2026-04-24｜William George, CFO｜risk：CFO identified labor availability as the persistent constraint on the company's growth.（原話："it's always and forever for us, it's labor."）
- 2026-04-24｜William George, CFO｜customer：CFO said the company now has stronger ability to select which counterparties/customers it works with.（原話："we have a much stronger ability to pick our counterparties"）
- 2026-04-24｜William George, CFO｜commitment：CFO said the company requires customers to make multiyear volume commitments as a condition of committing modular capacity.（原話："insisting as a condition of us committing our capacity"）
- 2026-04-24｜Brian Lane, CEO｜commitment：CEO reiterated commitment to consistently rewarding shareholders while maintaining balance sheet strength.（原話："remain committed to consistently rewarding our shareholders"）

### 問答異常語氣（迴避／改口／保留）
- FIX_Q1_2026_Earnings_Call_20260424.md｜問：Analyst asked for the geography and core end markets of the pending electrical acquisition.｜答法：CFO declined to give specifics, saying he 'can't get too specific' until the deal is announced because the target company's own people don't yet know.

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 3 | 3 |
| customer_second_source | found | 2 | 2 |
| customer_concentration_credit | found | 3 | 3 |
| supply_demand_durability | found | 4 | 3 |
| regulatory_antitrust | found | 2 | 3 |
| reg_tariff_export | found | 4 | 4 |
| geo_supply_chain | found | 5 | 2 |
| end_markets | found | 3 | 3 |
| substitute_technology | none | 0 | 2 |
| channel_business_model_shift | none | 0 | 4 |
| capital_markets_pricing | found | 7 | 4 |
| major_events | found | 2 | 5 |

未涵蓋／不適用軸的查詢詞原文（供判相關性）：
- **substitute_technology**（none）：Comfort Systems USA technology disruption risk data center cooling liquid cooling modular prefabrication 2026；mechanical contractors data center construction alternative technology immersion cooling reduces HVAC piping demand 2026
- **channel_business_model_shift**（none）：Comfort Systems USA distribution channel disruption OR shift 2026；FIX Comfort Systems USA business model transition subscription OR platform 2026；Engineering & Construction channel disintermediation D2C 2026；Comfort Systems USA go-to-market change 2026

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260906","verdict":"觀望","role":"追蹤","H":{"status":"unavailable"},"R":{"status":"unavailable"},"single_thing":null,"kill_metrics":null,"rearm_trigger":"股價 ≤ $1,050（FY27 共識 EPS 17.5x）；或 Q4 FY26 訂單 ≥ $16B 且四大雲端 2028 資本支出口徑不低於 2027 → 重跑 DD、條件式上限 $1,400","irr_base_pct":0.6,"ev5y_pct":-0.9,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"追蹤","signal":"B","val":"🔴","ma":"-","trap":"🟡","moat_trend":"↑","runway_post_y5":"🟡","asym_ratio":0.9,"ev5y_pct":-0.9,"irr_base_pct":0.6,"max_dd_pct":-65,"bull_5y_price":2730.0,"bear_5y_price":570.0,"p_bull_pct":25,"p_bear_pct":30,"rearm_trigger":"股價 ≤ $1,050（FY27 共識 EPS 17.5x）；或 Q4 FY26 訂單 ≥ $16B 且四大雲端 2028 資本支出口徑不低於 2027 → 重跑 DD、條件式上限 $1,400","price_at_dd":1610.34,"archetype":"品質複利成長","cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"FIX","date":"2026-10-13","schema":"v15.2","contract":"v19","company_name":"Comfort Systems USA"},"oneliner":"資料中心機電施工龍頭，訂單與利潤率同創新高；現價約 27 倍明年獲利，已把建設高峰的利潤率延伸到 2028 年後，基本情境五年報酬有限，等股價回到約 1,200 美元或訂單續創新高再談。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/FIX_20261013/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/FIX_20261013/scenario.json","answers":{"q1_business":{"verdict":"賺超大規模雲端業者與工業客戶的機電施工錢，科技（資料中心）占上半年營收 58%；錢卡在技工與模組化產能這一節點。","reasoning":"第二季營收 32.66 億美元，營業利益 5.58 億美元（利益率 17.1%），毛利率 25.9%（去年同期 23.5%）。分部：機械營收年增 40%、毛利率 25.6%；電氣年增 81%、毛利率 26.4%。終端市場：上半年工業占 75%，其中科技 58%（去年同期 40%），機構 17%，商業 8%；施工占 90%（新建 75%、既有建物 15%），服務 10%。錢卡在技工與模組化產能：CFO 在 2026-04-24 法說稱成長的限制「永遠是人力」，客戶以多年期量承諾與預付款鎖住模組化產能。單點依賴：最大單一客戶占 2025 年營收 12.8%（2023 年 13.8%）、占應收 10.2%，模組化量承諾只來自兩家超大規模業者——這是集中度風險，不是護城河證據。供需持久性：週期性將反轉的風險高於結構性——技工短缺是結構性，但需求高度依賴資料中心資本支出，資料中心以外的民間非住宅支出已連 7 個月下滑。在手訂單 140.6 億美元，CFO 稱施工部分多在 18–24 個月內消化。管理層未給數字指引，只給全年同店營收增幅中至高 30% 區間。","fact_refs":["f_kpi0_gaap","f_kpi2_gaap","f_kpi6_backlog","f_peer_fix_gross_margin_pct","f_kpi5"],"verdict_values":{"revenue_quality":"高：在手訂單 140.6 億美元，施工部分多在 18–24 個月內消化，模組化排程更遠；客戶預付款提升現金品質。扣分項：第二季估計變動使營收增加約 7.7%，約為一年前兩倍，第一季另有 4,300 萬美元一次性變更單利益。","unit_econ_note":"施工端以人力為主，SG&A 占營收由 9.7% 降到 8.8%，營運槓桿為正；模組化需自有廠房（近期一棟約 1 億美元），CFO 稱回本 1–2 年；併購的 Hunt Electric 預期 EBITDA 利潤率 8–10%，低於公司整體約 18%。","archetype":{"primary":"品質複利成長","secondary":"循環/商品","confidence":"中","fingerprint":"高利潤率機電承包商＋客戶預付形成的負營運資金＋資料中心訂單驅動；CFO 稱自 2005 年起每年專案估計淨利得皆為正"},"industry":{"clock_phase":"III","sd_verdict_source":"產業時鐘 III 過熱：資料中心機電工程的訂單、定價（客戶預付款、付款條件）與利潤率同創新高，技工是瓶頸，且同時出現客戶引入其他廠商擴產、地方暫停令兩種過熱訊號；資料中心以外的非住宅建築偏收縮。供需持久性判為週期性將反轉：供給端技工不易擴，需求端可逆。","bargaining":{"up":"上游：變壓器、配電開關、大型發電機交期常逾 6 個月，供應商有定價力；鋼鋁銅關稅推高材料成本，大案多在早期鎖價。","down":"下游：客戶為鎖產能預付款、付款條件佳，CFO 稱議價力極強；但買方是少數資本雄厚的超大規模業者，景氣反轉時議價力會回流。","geo":"營運集中美國（27 州約 190 據點），部分原料與零組件進口，關稅是主要地緣變數；未見中國或台灣供應鏈曝險。"},"profit_pool_dir":"利潤池正流向稀缺技工與模組化產能端（本公司營業利益率遠高於同業），持續期取決於技工缺口與資料中心建設強度，兩者都非公司可控。","tam_table":{"expanded":false,"reason":"事實表未涵蓋資料中心機電工程市場規模、滲透率與份額；只有公司自述科技占營收 58%，無法推得滲透率，五年後跑道判讀改用第二曲線證據。"}}}},"q2_moat":{"verdict":"護城河 B 級、方向向上：技工規模與模組化共同設計產能讓客戶預付款鎖產能，但定價力有一段來自景氣。","reasoning":"機制是技工規模加模組化產能：可跨州調度的技工隊伍、與客戶共同設計的模組，以及客戶用預付款與多年期量承諾鎖產能。執行力 9 分：在手訂單年增 73%，扣除第一季一次性利益後毛利率由 25.2% 升到 25.9%，CFO 稱自 2005 年起每年專案估計淨利得為正。定價力 7 分：預付款與付款條件證明現在有議價力，但這段隨技工與資料中心景氣而變，景氣反轉時會先失去。合併 8 分，B 級。可比軸改用營業利益率差距（ROIC 所需投入資本事實表未涵蓋）：TTM 16.45%，高於 EMCOR 9.6%、IESC 12.38%、Quanta 6.12%；同業歷史利潤率事實表未涵蓋，擴大方向只能以自身由 2022 年 6.09% 升到 2025 年 14.42% 佐證。方向判向上：執行端擴大（模組化產能往 500 萬平方英尺擴、前沿實驗室與主機代管試點），定價端目前擴大但屬景氣成分。最大客戶占營收比下降是因本公司營收成長較快，該客戶貢獻金額仍上升，不是份額流失。當期 ROIC 屬高利益率×高周轉：營運資金為負，投入資本主要是自有模組化廠房，數值因投入資本缺資料無法算出。","fact_refs":["f_peer_fix_gross_margin_pct","f_peer_fix_operating_margin_pct","f_peer_fix_fcf_margin_pct","f_peer_eme_gross_margin_pct","f_peer_eme_operating_margin_pct","f_peer_iesc_operating_margin_pct","f_peer_pwr_operating_margin_pct"],"verdict_values":{"moat":{"mechanism":"技工與模組化產能的稀缺：約 2.5 萬名員工、可跨州調度的技工、與客戶共同設計的模組化廠房（2026 年底逾 400 萬平方英尺、2027 年夏末約 500 萬），客戶以多年期量承諾與預付款鎖產能。","execution":9,"pricing":7,"grade":"B","trend":"↑","trend_evidence":"TTM 營業利益率 16.45% 高於 EMCOR、IESC、Quanta；自身營業利益率由 2022 年 6.09% 升到 2025 年 14.42%，第二季 17.1%；在手訂單年增 73%，模組化當季淨增訂單約 5 億美元且已排到更遠期；同業歷史利潤率事實表未涵蓋，擴大方向以自身序列佐證。","competitor_notes":[{"name":"EMCOR（EME）","strategy_note":"最直接對手，規模大、服務範圍廣（含設施維護與更廣的電氣足跡），搶多據點超大規模大單有優勢；利潤率與現金轉換明顯較低，顯示本公司的領先在挑案與執行，不在規模。"},{"name":"IESC","strategy_note":"毛利率與本公司相當，但營業利益率與自由現金流率較低，落差主要在費用槓桿與現金轉換。"},{"name":"Quanta（PWR）","strategy_note":"偏電網與公用事業的間接對手，利潤率結構不同，不在同一客戶池做直接價格競爭。"},{"name":"Sterling Infrastructure（STRL）","strategy_note":"資料中心與半導體場址工程的次要對手；事實表無其財務數字，無法比較。"}],"peer_na_reason":"同業投入資本與 ROIC 事實表未涵蓋，可比軸改用營業利益率與自由現金流率。","threats":[{"level":"🟡","text":"模組化新進者：客戶引導其他廠商生產與本公司共同設計的模組，CFO 稱是客戶要的量超過本公司產能而非取代；目前屬點對點，若產能過剩會轉為價格競爭。","p":"25%","evidence_refs":["competitive_share_entrants#1","competitive_share_entrants#2"]},{"level":"🟡","text":"EMCOR 規模與服務範圍較廣，利於爭取多據點超大規模客戶的整包大單。","p":"20%","evidence_refs":["competitive_share_entrants#2"]},{"level":"🟡","text":"分包商與設備供應商依賴：交期逾 6 個月的設備延誤會削弱準時交付的口碑優勢。","p":"20%","evidence_refs":["geo_supply_chain#2","geo_supply_chain#3"]}],"roic_durability":{"quadrant":"高利益率×高周轉","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者、決策者、付款者都是超大規模業者與主機代管商，三者一致；機電工程是蓋好資料中心的必要環節（需要而非想要），但急迫性來自 AI 資本支出週期，不等於持久性。代理變數：科技占營收由 40% 升到 58%、在手訂單年增 73%。"},{"item":"決策層級","level":"🟡","text":"模組化以多年期量承諾與預付款鎖產能，產品與客戶共同設計，換廠成本高；現場施工逐案招標，單一專案層級的替代性仍高。代理變數：預付款約占第二季自由現金流三分之一（CFO 估）、與兩家超大規模業者的多年量承諾。"},{"item":"價值鏈分配","level":"🟡","text":"本公司目前拿到技工稀缺的租金（毛利率 25.66% 對 EMCOR 19.43%）；上游變壓器、配電開關與發電機交期逾 6 個月，供應商同樣有定價力；買方高度集中且資本雄厚，技工缺口一旦緩解，分配會往買方回流。未見客戶自建機電施工或導入第二供應商取代的報導。"},{"item":"社會容忍度","level":"🟡","text":"資料中心在地反對與州級暫停令（紐約州）升溫，分析師連兩季追問；營運長稱會改址而非取消、現有在手訂單多已取得許可。影響的是需求落點與時程，不是本公司報價；優勢不依賴監管授權，政策風險屬間接。"}],"roiic":50,"reinvest_rate":29,"endo_ceiling":14.6,"formula_note":"增量 ROIC 50%：CFO 稱模組化產能 1–2 年回本，稅前年報酬 50–100%，保守取稅後約 50%（管理層說法，未經查證）；全公司有機營運資金為負（2023–2025 年自由現金流合計約 23.1 億美元高於淨利合計約 18.7 億美元），嚴格說增量 ROIC 不可定義。再投資率 29%＝（資本支出約營收 5% − 折舊攤提約 1.3%〔第二季 EBITDA 6.0 億減營業利益 5.58 億〕）÷ 稅後營業利益率約 12.7%（TTM 營業利益率 16.45%×（1−23%）），不含負營運資金與價格未揭露的併購。內生天花板＝50%×29%≈14.6%。"}}}},"q3_growth":{"verdict":"五年後跑道中等：未來兩年有在手訂單撐，之後要靠服務與模組化新客戶，兩者都還在試點。","reasoning":"成長以量為主（第二季同店營收 +44%），價次之（毛利率提升），併購補強（Hunt Electric 年化約 2.5 億美元營收；Feyen Zylstra 與 Meisner 合計約 2.0–2.4 億美元），淨回購每年約 0.25% 可忽略。共識 EPS 由 FY2025 實際 28.88 到 FY2028 73.85，三年年複合約 36.7%（Koyfin 共識，家數未揭露）。內生天花板約 14.6%，缺口約 22 個百分點，可歸因：主要是利潤率擴張（FY2025 營業利益率 14.42%→第二季 17.1%；FY2026 共識 EPS 年增 70%，共識營收年增 43%），其次是客戶預付款支應的負營運資金成長（公式未計入），再次為補強併購，不靠回購。也就是共識高成長有一大段是利潤率一次性抬升，抬完之後成長回到營收成長，FY2027 共識營收年增已降到約 19%。五年後跑道判中：服務營收年增 7%、占營收 10%，模組化新客戶仍是試點，第二曲線尚無證據。十類衰退訊號只亮 1 項（EPS 成長遠高於營收成長），長期成長性中等。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_kpi6_backlog","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m"],"verdict_values":{"growth":{"driver_mix":"量為主（同店營收 +44%）、價次之（毛利率 23.5%→25.9%）、補強併購（Hunt 年化約 2.5 億美元營收）、淨回購可忽略。","runway_years":"約 2 年可見度（在手訂單消化 18–24 個月）；滲透率事實表未涵蓋","runway_post_y5":"🟡","endo_ceiling_basis":"引護城河段：增量 ROIC 50%×再投資率 29%≈14.6%；共識 FY2025 實際→FY2028 EPS 年複合 36.7%，缺口約 22 個百分點，歸因利潤率擴張為主、負營運資金成長與補強併購為次。","segments":[{"item":"機械","value":"第二季營收年增 40%，毛利率 25.6%（去年 22.9%）；2025 年前九月營收 48.5 億美元（+19.0%）"},{"item":"電氣","value":"第二季營收年增 81%，毛利率 26.4%（去年 25.3%）；2025 年前九月營收 16.0 億美元（+47.9%）；含 Hunt Electric（年化約 2.5 億美元）"},{"item":"終端市場","value":"2026 上半年：工業 75%（其中科技 58%，去年同期 40%）、機構 17%、商業 8%"},{"item":"工程型態","value":"施工 90%（新建 75%、既有建物 15%），服務 10%（年增 7%）；模組化占年初至今營收 17%，計入新建"},{"item":"模組化產能","value":"現有逾 350 萬平方英尺，2026 年底逾 400 萬，2027 年夏末約 500 萬，主要供既有客戶與既有訂單"}],"decay_signals":[{"item":"毛利率連 2 季年減","lit":false,"evidence":"第二季 25.9% 對去年 23.5%"},{"item":"核心市占近 12 個月縮減","lit":false,"evidence":"事實表無份額數據；在手訂單年增 73% 不支持縮減"},{"item":"主力產品提價後銷量下滑","lit":false,"evidence":"未見"},{"item":"EPS 成長顯著高於營收成長（差距逾 5 個百分點）","lit":true,"evidence":"FY2022→FY2025 EPS 年複合約 62%，營收約 30%"},{"item":"自由現金流對淨利低於 0.75 連 2 年","lit":false,"evidence":"2023–2025 年為 1.68、1.41、1.01"},{"item":"SBC 占營收逾 5% 且上升","lit":false,"evidence":"約 0.28%"},{"item":"市場萎縮或被替代技術壓縮","lit":false,"evidence":"事實表未涵蓋市場規模，未見替代技術證據"},{"item":"產業估值倍數近 3 年系統性下移","lit":false,"evidence":"本公司倍數處年度端點高點"},{"item":"維護性資本支出占自由現金流逾 60%","lit":false,"evidence":"資本支出以擴產為主"},{"item":"停止投資新產能且營收 3 年內下滑","lit":false,"evidence":"仍在擴產"}],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"現金轉換與資產負債表一流、資本配置保守；併購與回購的報酬因價格未揭露無法驗證。","reasoning":"自由現金流轉換極強：2023–2025 年自由現金流對淨利為 1.68、1.41、1.01 倍；第二季自由現金流 9.99 億美元約為淨利 2.5 倍，CFO 估約三分之一是客戶預付款，景氣反轉時會回吐。SBC 占營業利益 1.65%、占營收約 0.28%；稀釋股數由去年第二季約 3,537 萬股降到 3,528 萬股（以淨利÷EPS 推算），淨稀釋為負。現金去向：資本支出約營收 5%（買下模組化廠房、機器人與噴塗設備，CFO 稱回本 1–2 年）、股息調升到每季 0.90 美元（殖利率約 0.2%）、回購今年放慢（去年大買之後）、補強併購（Hunt、Feyen Zylstra、Meisner，價格未揭露）；各項金額事實表未涵蓋。淨現金約 15.4 億美元。營運槓桿為正：第二季營收年增約 50%、營業利益年增 86%。Hunt 預期 EBITDA 利潤率 8–10%（2026-04-24 法說，CFO George），會稀釋整體利潤率。","fact_refs":["f_kpi3_fcf","f_kpi4_sbc","f_net_debt_m","f_dividend_yield_ttm","f_peer_fix_fcf_margin_pct","f_shares_diluted_m"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":true,"passed":null,"input":"Hunt Electric、Feyen Zylstra、Meisner 收購價未揭露（2026-04-24 法說 CFO 亦拒談細節），已實現報酬無法計算"},{"name":"buyback_yield","applicable":true,"passed":null,"input":"去年大量回購但均價事實表未涵蓋；以現價計 FY2026 共識盈餘殖利率約 3.0%，10 年期公債殖利率事實表未涵蓋"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"SBC 約占營收 0.28%；稀釋股數年減約 0.25%，淨稀釋為負"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長以同店為主：在手訂單一年增加 59 億美元中 56 億美元屬同店，併購為小型補強，不靠併購撐成長"}}}},"q5_valuation":{"verdict":"現價要 2028 年後資料中心建設不降溫、營業利益率守在 17% 附近，才划算；本案不把這當基本情境，估值偏貴。","reasoning":"現價 1,638.05 美元對 FY2026 共識 EPS 49.01 為 33.4 倍、FY2027 60.18 為 27.2 倍、FY2028 73.85 為 22.2 倍；trailing 本益比 40.3 倍，處 4 個年度端點最高（非連續五年序列）。FY1 共識近 3 個月上修 12.3%（43.63→49.01），最近一次快照則持平；賣方目標價平均約 1,974–2,114 美元。反推：若 2028 年後成長降到中個位數、營業利益率回到 15% 左右，FY2031 EPS 約 81、倍數 22 倍，終點約 1,782 美元，五年只比現價高約 9%。要拿到年化 10% 以上，需 FY2031 EPS 超過 110 且倍數守 24 倍以上，等於多頭路徑。PEG 以三年共識年複合 36.7% 計約 0.91 看似便宜，但分母含利潤率一次性抬升與估計變動利益，這個便宜論證不成立；改用 FY2026→FY2028 兩年年複合約 22.8% 對 FY2027 本益比，約 1.2。","fact_refs":["f_price_at_dd","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_pe_current","f_pe_percentile","f_fwd_pe_latest","f_consensus_rev_3m_fy1_pct","f_consensus_rev_fy1_pct","f_ps_current","f_ev_s_fwd"],"verdict_values":{"valuation":{"basis":"前瞻本益比（FY2026／FY2027 共識 EPS），輔以 PEG","peers":{"expanded":false,"reason":"事實表未涵蓋同業前瞻本益比，同業只有利潤率對照；終端倍數改以本身現值（FY2027 27.2 倍）為上緣參考"},"fwd_pe":33.4,"peg":0.91,"percentile_5y":100,"val_light":"🔴","val_light_derivation":"前瞻 33.4 倍（FY2026）／27.2 倍（FY2027），trailing 40.3 倍處 4 個年度端點最高（非連續五年序列）；基本情境（FY2031 EPS 81×22 倍）五年約 +9%，三情境加權約 +7%，只有多頭路徑能給年化 10% 以上，判偏貴，結論與前份相同。","upside_short_pct":-8.1,"upside_mid_pct":8.8,"denominator_disputed":true,"denominator_note":"FY2026 共識 EPS 含第一季約 4,300 萬美元一次性專案利益（約每股 0.9 美元）與偏高的估計變動利益（第二季約占營收 7.7%，約為一年前兩倍），且處資料中心建設高峰利潤率；以此為分母的低 PEG 不能當便宜證據。"}}},"q6_how_wrong":{"verdict":"最可能看錯的方向是把資料中心建設高峰的利潤率與訂單當常態；反方向的錯是低估模組化與服務的延續性。","reasoning":"反證集中寫在反證紀錄，三個視角各一條以上，核心是資料中心消化期（科技占營收 58%）與利潤率回歸。陷阱判中等：十類衰退訊號只亮 EPS 成長遠高於營收成長一項。歷史最大回撤、空方最強數字與訴訟金額事實表未涵蓋；監管面只有承包商執照與聯邦工程稽核的一般風險，管理層稱訴訟個別與合計皆不重大。2026-04-24 法說 CFO 對待併購電氣公司的地區與終端市場不願細談，之後揭露為 Hunt Electric（猶他州，年化約 2.5 億美元營收），收購價至今未揭露。管理層指引歷來偏保守（第一季給同店中至高 20%，第二季上調到中至高 30%），本身不是警訊。動能不過熱：RSI 46.4、26 週報酬 +0.7%。","fact_refs":["f_peer_fix_operating_margin_pct","f_kpi6_backlog","f_rsi14","f_week26_return_pct"],"verdict_values":{"trap":{"verdict":"🟡","label":"利潤率高峰型（衰退訊號亮 1 項）"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":49.01,"pe":33.42,"basis":"FY2026 共識 EPS 49.01（Koyfin 2026-10-08），現價 1,638.05÷49.01＝33.42 倍；終端倍數同以當年度 EPS 為分母"},"eps":{"bull":[64.0,80.0,94.0,106.0,117.0],"base":[60.2,71.0,75.0,78.0,81.0],"bear":[56.0,47.0,38.0,36.0,40.0]},"pe":{"bull":26,"base":22,"bear":16},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0.18,"net_buyback":0.25},"second_stage":{"bull_cagr_pct":10,"base_cagr_pct":6},"max_dd":{"lo":-65,"hi":-45,"basis":"空頭終點 EPS 40×16 倍＝640 美元（約 −61%）為下緣參考；途中最深點可能落在 2028–2029 年：EPS 由約 57 降到 36、倍數由 33 倍壓到 16 倍→約 576 美元（−65%）；倍數只壓到 20 倍→約 720 美元（−56%）；溫和版 EPS 降約 20% 到 46、倍數 20 倍→約 920 美元（−44%）。取 −45% 至 −65%；歷史最大回撤事實表未涵蓋，不作依據。","trigger_time":null},"basis":{"bull":"資料中心建設延續到 2030 年，模組化擴到 500 萬平方英尺以上並把前沿實驗室、主機代管由試點轉量產，服務成第二曲線；營業利益率守 17% 以上，FY2027–2028 高於共識；終端 26 倍（現價 FY2027 為 27.2 倍）。","base":"FY2027 照共識 60.2，FY2028 略低於共識（71 對 73.85，第四季高基期、一次性利益不再）；2029 年起資料中心建設趨緩，營收年增降到中個位數，營業利益率由約 17% 回落到 15% 左右；終端 22 倍，低於現價 FY2027 的 27.2 倍以反映成長降速；同業現值倍數事實表未涵蓋。","bear":"2027 年資料中心訂單轉弱，2028–2029 年營收下滑、營業利益率回到 2024 年約 11% 水準，EPS 跌到 36 後小幅回升到 40；終端 16 倍取自成長熄火（三年後成長降到 5%）的倍數錨。"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"科技占上半年營收 58%（去年同期 40%）；資料中心以外的承包商在手訂單低於去年、民間非住宅支出連 7 個月下滑；第三方對 2025 年科技占比有 40% 與 45% 兩種口徑。","assumption":"超大規模業者的資料中心建設在 2028 年後仍維持高檔。","consequence":"2027 年訂單轉弱，2028–2029 年營收下滑、利潤率回到約 11%，EPS 由約 57 跌到 36，倍數壓到 16 倍，股價約 576–640 美元（−61%～−65%）。","ruling":"採納：列為空頭情境，機率 30%；與唯一致命點是同一個故事。","watch":"同店在手訂單季環比；科技類占營收比","evidence_refs":["supply_demand_durability#3","customer_concentration_credit#2"],"fact_refs":["f_kpi6_backlog"]},{"view":"論點成功但股東經濟變差","evidence":"客戶引導其他廠商生產共同設計的模組；2026 年鋼鋁銅製品關稅 50%、含金屬電氣設備 15%；設備交期常逾 6 個月；10-K 稱無法轉嫁關稅可能重大不利；資本支出升到營收 5% 並改買廠房；併購標的利潤率 8–10% 低於本公司。","assumption":"需求延續時，本公司仍能維持現在的定價與預付條件。","consequence":"營收照預期成長，但新標案利潤率下滑、預付款回吐使自由現金流低於淨利，自有廠房在景氣反轉時變閒置資產，EPS 成長落後營收。","ruling":"部分採納：CFO 稱客戶引入他廠是要更多產能而非取代，且廠房只在有多年量承諾時才擴；但預付款屬景氣條件，基本情境已把營業利益率降到 15% 左右。","watch":"季毛利率；年度自由現金流對淨利；模組化淨訂單","evidence_refs":["competitive_share_entrants#1","reg_tariff_export#2","geo_supply_chain#1","geo_supply_chain#3"],"fact_refs":["f_peer_fix_gross_margin_pct","f_kpi3_fcf"]},{"view":"價格已反映太多","evidence":"前瞻本益比 33.4 倍（FY2026）、27.2 倍（FY2027）；trailing 40.3 倍與 P/S 5.13 倍都處 4 個年度端點最高。","assumption":"市場在 2028 年後仍願意給 25 倍以上。","consequence":"即使 EPS 照共識走到 FY2028 的 73.85，倍數回到 22 倍，股價約 1,625 美元，兩年多原地踏步。","ruling":"採納：這是觀望的主約束。","watch":"股價對 FY2027 共識 EPS 倍數；1,200 美元重啟價","evidence_refs":[],"fact_refs":["f_fwd_pe_latest","f_pe_current","f_pe_percentile","f_ps_current"]},{"view":"論點失敗","evidence":"紐約州資料中心暫停令；分析師在 2026-04-24 與 2026-07-24 兩場法說連續追問州級禁令與電力取得。","assumption":"資料中心會改址而不取消。","consequence":"新案延後、模組化計畫性選址受阻，在手訂單轉化變慢。","ruling":"部分反駁：營運長稱現有在手訂單多已取得許可，模組化屬計畫性選址受影響較小；列為長期風險，不另加情境機率。","watch":"公司揭露的專案延期或取消","evidence_refs":[],"fact_refs":[]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 - → 本次 ✅","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=-","side_b":"本次 ma=✅","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 1610.34 → 本次 1638.05（+1.7%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=1610.34","side_b":"本次 price_at_dd=1638.05","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 1,610.34 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 1,610.34 美元：Bull 價 2,730、Bear 價 570，五年期望值 −0.9%，基準年化 0.6%，不對稱比 0.9","side_b":"本次情境、股價仍用 1,610.34 美元：Bull 價 3,042、Bear 價 640，五年期望值 +8.9%，基準年化 2.0%，不對稱比 1.23","ruling":"先換情境、股價不動：五年期望值多 9.8 個百分點，基準年化多 1.4 個百分點。不對稱比由 0.9 變為 1.23。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變好。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 1,610.34 美元：五年期望值 +8.9%，基準年化 2.0%，不對稱比 1.23","side_b":"本次情境、股價 1,638.05 美元：五年期望值 +7.1%，基準年化 1.7%，不對稱比 1.17","ruling":"再換股價、情境不動：起點價上漲 1.7%，五年期望值少 1.8 個百分點，基準年化少 0.3 個百分點，不對稱比由 1.23 降到 1.17。合計五年期望值比前份多 8.0 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"前份漂移：價格與估值結論","cause":"價格變動","prior_field":["signal","val"],"side_a":"前份（2026-09-06）：股價 1,610.34 美元，FY2027 共識 EPS 約 60（由 1,050 美元＝17.5 倍反推），估值偏貴，結論觀望。","side_b":"本次：股價 1,638.05 美元（+1.7%），FY2027 共識 60.18，FY2027 本益比由約 26.8 倍升到 27.2 倍；估值結論仍偏貴，時機評等維持 B。","ruling":"價格小幅變動不改估值結論；裁決與角色由程式依本次輸入重算，預期維持觀望。","evidence_level":"高（價格與共識皆為事實表數字）","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"前份漂移：護城河方向、陷阱、五年後跑道","cause":"新證據","prior_field":["moat_trend","trap","runway_post_y5"],"side_a":"前份：護城河向上、陷阱中等、五年後跑道中等。","side_b":"本次三欄維持；新納入第二季法說的模組化新進者證據（客戶引導其他廠商生產共同設計的模組）、科技占營收升到 58%、非資料中心民間非住宅支出連 7 個月下滑。","ruling":"新證據同時加強需求集中風險與執行領先，兩者互相抵銷，三欄不改；新進者若在產能過剩時轉為價格競爭，護城河方向改判持平。","evidence_level":"中","settle_metric":"季毛利率；模組化淨訂單","if_then":["若季毛利率連 2 季 < 23.5% 且管理層提及模組化競爭 → 護城河方向改判持平並重跑 DD","反向：若模組化新增具多年量承諾客戶 ≥ 1 家 → 方向維持向上"],"evidence_refs":["supply_demand_durability#3","competitive_share_entrants#1"]},{"axis":"前份漂移：情境機率與最大回撤","cause":"方法變動","prior_field":["p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份：多頭 25%、空頭 30%、最大回撤 −65%（單點）。","side_b":"本次：多頭 25%、基本 45%、空頭 30%；最大回撤改為區間 −45% 至 −65%。","ruling":"機率不變（共識成長超過內生天花板，空頭機率維持 30% 下限）；回撤改用區間表示並寫出推導，空頭終點 EPS 40×16 倍＝640 美元。","evidence_level":"中","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"前份漂移：公司類型與景氣位置","cause":"方法變動","prior_field":["archetype","cycle_position"],"side_a":"前份：品質複利成長，未標景氣位置。","side_b":"本次：主類型維持品質複利成長，加註副類型循環/商品；景氣位置標為晚循環。","ruling":"本輪改為明示景氣位置：資料中心機電工程的訂單、定價、利潤率同創新高，客戶開始引入其他供應商擴產，地方暫停令出現，屬晚循環特徵；主類型不改，因 CFO 稱自 2005 年起每年專案估計淨利得為正，跨景氣仍賺錢。","evidence_level":"中","settle_metric":"同店在手訂單年增率","if_then":["若同店在手訂單年增率轉負 → 景氣位置改判過熱頂部，已持有者減碼一半"],"evidence_refs":["supply_demand_durability#3"]},{"axis":"重啟條件門檻變動（估值rearm）","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"股價 ≤ $1,050（FY27 共識 EPS 17.5x）；或 Q4 FY26 訂單 ≥ $16B 且四大雲端 2028 資本支出口徑不低於 2027 → 重跑 DD、條件式上限 $1,400","side_b":"股價 ≤ $1,200（FY27 共識 EPS 約 20 倍）且在手訂單未環比下滑；或 2026Q4 在手訂單 ≥ $16B 且股價 ≤ $1,400 → 重跑 DD","ruling":"價格錨由 17.5 倍改為 20 倍：本輪情境樹在 1,200 美元時基本情境五年年化約 8%、空頭跌幅約 47%，報酬風險才轉為偏正；前份 1,050 美元未附情境推導。四大雲端資本支出口徑不在本輪證據包，改用公司自報的在手訂單環比作代理；16B 訂單與 1,400 美元上限原樣保留，不刪門檻。","evidence_level":"中","settle_metric":"股價；季末在手訂單","if_then":["若股價 ≤ $1,200 且最近一季在手訂單未環比下滑 → 重跑 DD，通過後首倉 ≤ 2%","若股價先到 $1,200 但在手訂單已環比下滑 → 不進場，重啟價改為 $1,000"],"evidence_refs":[]},{"axis":"Single Thing 設定（前份未設）","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設定唯一致命點","side_b":"同店在手訂單首次出現環比下滑，且下滑來自科技類（資料中心）訂單","ruling":"本輪要求唯一致命點須為數學上最大的敏感度項：科技占營收 58%，在手訂單是其領先指標；發生時已持有者先減碼一半，再降一季則清倉。","evidence_level":"中","settle_metric":"同店在手訂單季環比","if_then":["若發生 → 已持有者減碼一半，下一季再降則清倉"],"evidence_refs":["supply_demand_durability#3"]},{"axis":"出場指標門檻設定（前份未設）","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設定出場指標","side_b":"在手訂單連 2 季環比下滑；季毛利率 < 23.5% 連 2 季；最大客戶占營收 > 15%；自由現金流對淨利 < 0.75 連 2 年","ruling":"新設四條出場指標：觸及任一條減碼一半，前兩條同時觸及清倉。","evidence_level":"中","settle_metric":null,"if_then":["若在手訂單與毛利率兩條同時觸及 → 清倉"],"evidence_refs":[]},{"axis":"資料中心需求：管理層「毫無放緩」對產業數據","cause":null,"side_a":"管理層（2026-07-24 法說，CFO George）：直接賣給超大規模業者，看到的是完全沒有放緩跡象，專案管線處歷史高檔。","side_b":"產業數據（2026 年 4 月）：在手訂單增幅幾乎全來自有資料中心業務的大型承包商，其他承包商在手訂單低於去年，民間非住宅支出連 7 個月下滑；本公司科技占營收由 40% 升到 58%（第三方對 2025 年占比口徑不一）。","ruling":"可調和（程度差異）：兩邊量的是不同市場，資料中心強、其他弱同時成立；但這代表本公司成長只剩一具引擎，採 B 側的集中風險，空頭機率維持 30%。","evidence_level":"中（產業數據為第三方彙整）","settle_metric":"非科技類（機構＋商業）營收年增率；科技占營收比","if_then":["若科技占營收升破 65% 且非科技營收年減 → 已持有者減碼一半","反向：若非科技營收年增 ≥ 10% 連 2 季 → 空頭機率下調到 25% 並重跑 DD"],"evidence_refs":["supply_demand_durability#3","customer_concentration_credit#2"]},{"axis":"利潤率品質：結構抬升對估計變動利益","cause":null,"side_a":"CFO（2026-07-24）：扣除第一季一次性利益後毛利率由 25.2% 升到 25.9%，預期維持近幾季平均的強勁區間；機械毛利率 22.9%→25.6%。","side_b":"10-Q：估計變動使第二季營收增加約 7.7%，約為一年前兩倍；第一季另有 4,300 萬美元一次性變更單利益；CFO 自承大型案件風險較大。","ruling":"可調和（程度差異）：兩邊都對，差在結構成分多大。基本情境把營業利益率由約 17% 降到 15% 左右，依據是估計變動貢獻已是一年前兩倍、屬景氣順風；不採全數回歸，因扣除一次性後毛利率仍逐季上升。","evidence_level":"中","settle_metric":"10-Q 估計變動對營收貢獻比例；季毛利率","if_then":["若估計變動貢獻回到 ≤ 4% 而季毛利率仍 ≥ 24.5% → 結構成分證實，重跑 DD 上調基本情境利潤率","若估計變動貢獻回落且季毛利率 < 23.5% 連 2 季 → 已持有者減碼一半"],"evidence_refs":["competitive_share_entrants#1"]},{"axis":"關稅與材料成本：已緩解對轉嫁風險","cause":null,"side_a":"管理層（2026 年 5 月法說摘要）：設備端供應鏈與關稅風險已透過合約緩解；大型案成本多在早期鎖定、供應商固定報價。","side_b":"10-K 風險因素：無法轉嫁關稅成本時經營結果可能受重大不利影響，公司與供應商進口部分原料與零組件；2026 年鋼鋁銅製品關稅 50%、含金屬電氣設備 15%，政策反覆。","ruling":"可調和：已簽約的在手訂單受保護，風險落在新標案報價與利潤率；不寫政策預測，以季毛利率作吸收失敗的判定。","evidence_level":"中","settle_metric":"季毛利率","if_then":["若季毛利率 < 23.5% 連 2 季且管理層歸因材料成本 → 已持有者減碼一半","反向：季毛利率守 ≥ 24.5% → 關稅維持背景監測"],"evidence_refs":["reg_tariff_export#0","reg_tariff_export#2","geo_supply_chain#0","geo_supply_chain#1"]},{"axis":"管理層指引紀錄：前一季對本季","cause":null,"side_a":"2026-04-24 法說（CFO George）：全年同店營收增幅中至高 20%；毛利率維持近期平均；營運長稱模組化年底達 400 萬平方英尺。","side_b":"2026-07-24 法說：全年同店上調到中至高 30%；扣除一次性後毛利率上升；年底逾 400 萬、2027 年夏末約 500 萬；CFO 提醒第四季基期很高。","ruling":"可調和：管理層兌現並超越前季承諾，指引偏保守有紀錄；但上調後下半年隱含同店增幅降到約高 20% 至低 30%，2027 年成長率下台階是已知事實。","evidence_level":"高（兩場法說原話）","settle_metric":"第三、四季同店營收增幅","if_then":["若第三季同店增幅 < 25% → H1 削弱，停止加碼","反向：若全年同店 ≥ 40% → 重跑 DD 上調 FY2027 基本情境"],"evidence_refs":[]},{"axis":"產業態勢三軸","cause":null,"side_a":"結構轉好：技工缺口（ABC 估 2026 年需淨增約 34.9 萬名營建工人、2027 年 45.6 萬）、資料中心需求，在手訂單年增 73%。","side_b":"其他結構變數：鋼鋁銅關稅、州級資料中心暫停令；競爭：客戶引導其他廠商生產共同設計的模組化產品。","ruling":"雙向拉鋸：結構轉好仍占上風（需求與技工稀缺），競爭面尚屬點對點，關稅與暫停令屬其他結構變動中；依據為第二季訂單與兩場法說內容。","evidence_level":"中","settle_metric":"在手訂單與季毛利率","if_then":["若在手訂單續增但毛利率連 2 季下滑 → 改判競爭惡化中，停止加碼"],"evidence_refs":["competitive_share_entrants#1","reg_tariff_export#2"]},{"axis":"現在就買的最強論證（對觀望的反方）","cause":null,"side_a":"買方：第二季 EPS 12.53 美元大幅優於共識約 10.4，連四季優於共識；FY1 共識 3 個月上修 12.3%；在手訂單 140.6 億美元年增 73%；自由現金流率 19.2%、淨現金約 15.4 億美元；賣方目標價平均約 2,000 美元，高於現價約 20%。","side_b":"本案：這些都是建設高峰的數字，現價 FY2027 本益比 27.2 倍已把高峰利潤率延伸到 2028 年後；基本情境五年報酬約 +9%。","ruling":"⚖ 不可調和（方向相反），採觀望。依據是基本情境終點 81×22 倍＝1,782 美元，只有多頭路徑能給年化 10% 以上；買方若證實為對（2026 年第四季在手訂單 ≥ 160 億美元且季毛利率 ≥ 25%），改走條件式進場，上限 1,400 美元。","evidence_level":"中","settle_metric":"2026 年第四季在手訂單與季毛利率","if_then":["若 2026Q4 在手訂單 ≥ $16B 且季毛利率 ≥ 25% → 重跑 DD，股價 ≤ $1,400 時首倉 ≤ 2%","反向：若股價續漲而訂單與毛利率未創新高 → 不追"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"在手訂單守住 140 億美元，證明 2027 年營收可見度","type":"假設驗證","maps_to":"H1","metric":"季末在手訂單","threshold":"≥ $14.0B；連 2 季 < $13.3B 為削弱","action":"削弱時停止加碼、不追","source_freq":"公司季報新聞稿／每季","date":"2026-10"},{"n":2,"text":"毛利率跌破去年同期水準，代表估計變動利益回歸或關稅成本吸收失敗","type":"風險","maps_to":"R2","metric":"季毛利率","threshold":"< 23.5% 連 2 季","action":"已持有者減碼一半；未持有者不追","source_freq":"公司季報新聞稿／每季","date":null,"evidence_refs":["reg_tariff_export#0","geo_supply_chain#1","competitive_share_entrants#1"]},{"n":3,"text":"同店在手訂單首次環比下滑且來自科技類訂單","type":"Single Thing","maps_to":"Single Thing","metric":"同店在手訂單季環比與科技類訂單","threshold":"首次環比下滑","action":"已持有者減碼一半，再降一季清倉；重啟價改為 $1,000","source_freq":"公司季報新聞稿與法說／每季","date":null,"evidence_refs":["supply_demand_durability#3"]},{"n":4,"text":"價格回到 FY2027 共識約 20 倍","type":"估值rearm","maps_to":"H1","metric":"股價","threshold":"≤ $1,200 且在手訂單未環比下滑","action":"重跑 DD，通過後首倉 ≤ 2%","source_freq":"每日收盤","date":null},{"n":5,"text":"訂單續創新高，資料中心建設延續到 2027 年後","type":"估值rearm","maps_to":"H1","metric":"2026Q4 季末在手訂單","threshold":"≥ $16B 且股價 ≤ $1,400","action":"重跑 DD，條件式進場上限 $1,400","source_freq":"公司季報新聞稿","date":"2027-02"},{"n":6,"text":"第二曲線成形：服務與模組化新客戶","type":"假設驗證","maps_to":"H3","metric":"服務營收年增率；模組化具多年量承諾客戶數","threshold":"服務年增 ≥ 10% 且客戶 ≥ 3 家","action":"五年後跑道改判寬，重跑 DD 更新終端倍數","source_freq":"法說會／每季","date":null},{"n":7,"text":"客戶集中度升高","type":"風險","maps_to":"R3","metric":"最大單一客戶占營收／占應收","threshold":"> 15% 營收或 > 20% 應收","action":"已持有者減碼至半倉","source_freq":"10-K／每年","date":"2027-02","evidence_refs":["customer_concentration_credit#0"]},{"n":8,"text":"設備交期或分包延誤拖累認列","type":"風險","maps_to":"R4","metric":"季營收對共識落差","threshold":"低於共識 ≥ 5% 且管理層歸因設備交期或分包","action":"停止加碼","source_freq":"公司季報／每季","date":null,"evidence_refs":["geo_supply_chain#2","geo_supply_chain#3"]},{"n":9,"text":"價格已預支多頭路徑時減碼","type":"減碼","maps_to":"H2","metric":"股價對 FY2028 共識 EPS 倍數","threshold":"≥ 30 倍（約 $2,215）","action":"已持有者減碼三分之一","source_freq":"每日收盤","date":null},{"n":10,"text":"第四季財報後全面複審","type":"複審日期","maps_to":null,"metric":"2027 年指引與在手訂單","threshold":"財報發布","action":"重跑 DD","source_freq":"一次","date":"2027-02"}],"kill_metrics":[{"metric":"同店在手訂單季環比","bear_threshold":"連 2 季環比下滑","window":"2026Q3–2028Q4 每季","source":"公司季報新聞稿","last_status":"ok"},{"metric":"季毛利率","bear_threshold":"< 23.5% 連 2 季","window":"每季","source":"公司季報新聞稿","last_status":"ok"},{"metric":"最大單一客戶占營收比","bear_threshold":"> 15%（或占應收 > 20%）","window":"每年 10-K","source":"10-K 信用風險集中附註","last_status":"ok"},{"metric":"自由現金流對淨利（年度）","bear_threshold":"< 0.75 連 2 年","window":"每年","source":"年度現金流量表","last_status":"ok"}],"evidence_dismissed":[],"action_conditions":{"rearm_trigger":"股價 ≤ $1,200（FY27 共識 EPS 約 20 倍）且在手訂單未環比下滑；或 2026Q4 在手訂單 ≥ $16B 且股價 ≤ $1,400 → 重跑 DD","exec_line":"現價不建倉、不追；重啟條件成立才重跑 DD，首倉 ≤ 2%；已持有者以季毛利率與同店在手訂單兩條線管理，觸及任一出場指標減碼一半。","holding_cap":"重啟後首倉 ≤ 2%"}},"decision_inputs":{"signal":"B","ma":"✅","cycle_position":"晚循環","cycle_verdict":"等回踩","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"賣方目標價平均約 2,000 美元，隱含以 FY2027–2028 EPS 給約 27–33 倍，等於把資料中心建設高峰的營業利益率（約 17%）與訂單成長延伸到 2028 年後；本案認為估計變動利益已是一年前兩倍、科技占營收 58% 的單引擎結構，利潤率回落的機率被低估。","momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":true,"wait_for_price":true,"wait_for_price_condition":"等股價 ≤ $1,200（FY27 共識 EPS 約 20 倍）且在手訂單未環比下滑；或 2026Q4 在手訂單 ≥ $16B 時股價 ≤ $1,400","asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null,"prior_verdict":"觀望","prior_role":"追蹤"},"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8(val爭議)","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='↑', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='✅'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=賣方目標價平均約 2,000 美元，隱含以 FY2027–2028 EPS 給約 27–33 倍，等於把資料中心建設高峰的營業利益率（約 17%）與訂單成長延伸到 2028 年後；本案認為估計變動利益已是一年前兩倍、科技占營收 58% 的單引擎結構，利潤率回落的機率被低估。"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🔴', moat_trend='↑', week26=0.72, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position='晚循環', moat='B', moat_trend='↑', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈機械讀數判定不可用，baseline rows 8/9/9b/10 的估值條件視為不可判 → 落 row8 觀望（保守方向）","hit":true,"basis":"val_denominator_disputed=True, val(機械讀數)='🔴'"},{"row":"QC-49","condition":"qc49_inherit_prior=True 但前次裁決與矩陣機械輸出方向相同，無需承繼","hit":false,"basis":"prior_verdict='觀望', 矩陣機械輸出='觀望'"},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":null,"requires_critic":[]},"thesis":{"H":[{"id":"H1","text":"資料中心與工業在手訂單撐住 2026–2027 年營收：在手訂單維持 140 億美元以上，2026 年同店營收增幅落在管理層指引的中至高 30% 區間。","2y":"2027 年底前每季在手訂單 ≥ $14.0B；2027 年營收不低於共識 $15.4B 的 95%","5y":null,"10y":null,"threshold":"季末在手訂單 ≥ $14.0B；FY2026 同店營收增幅 ≥ 35%","source":"公司季報新聞稿（在手訂單、同店營收）；法說會 CFO 指引","drift_rule":"在手訂單連 2 季低於 $13.3B（偏離 ≥5%）為削弱；連 3 季低於 $12.6B（偏離 ≥10%）為反轉"},{"id":"H2","text":"營業利益率的抬升有一半以上是結構性（模組化、技工調度、客戶預付條件），建設降溫後 FY2028–FY2030 仍守 13% 以上。","2y":null,"5y":"FY2030 年度營業利益率 ≥ 13%（FY2024 10.62%、FY2025 14.42%）","10y":null,"threshold":"滾動四季營業利益率 ≥ 13%","source":"年度與季度財報；同業利潤率對照","drift_rule":"滾動四季營業利益率連 4 季低於 12.4%（偏離 ≥5%）削弱；連 6 季低於 11.7%（偏離 ≥10%）反轉"},{"id":"H3","text":"成長第二曲線成形：資料中心安裝基數帶出服務營收，模組化客戶由兩家超大規模業者擴到前沿實驗室與主機代管。","2y":null,"5y":"2028 年前服務營收年增 ≥ 10%，模組化具多年量承諾客戶 ≥ 3 家","10y":null,"threshold":"服務營收年增 ≥ 10%（目前 +7%，占營收 10%）","source":"法說會營運長揭露；10-K 客戶與營收組成","drift_rule":"自 2027 年起服務營收年增連 4 季低於 9.5% 削弱；連 6 季低於 9% 反轉"}],"R":[{"id":"R1","text":"資料中心資本支出進入消化期：科技占上半年營收 58%（去年同期 40%），是單一需求引擎；資料中心以外的民間非住宅支出已連 7 個月下滑，沒有替補。","h_ref":"H1","clock":"🔥","threshold":"同店在手訂單年增轉負，或科技類營收占比連 2 季下滑且總在手訂單環比下滑","evidence_refs":["customer_concentration_credit#2","supply_demand_durability#3"]},{"id":"R2","text":"利潤率回歸：估計變動利益（第二季約占營收 7.7%，約為一年前兩倍）不可持續，加上鋼鋁銅關稅、進口零組件成本、勞動成本通膨與競爭加劇，新標案利潤率先降。","h_ref":"H2","clock":"⚡","threshold":"季毛利率 < 23.5% 連 2 季","evidence_refs":["competitive_share_entrants#1","reg_tariff_export#0","reg_tariff_export#2","geo_supply_chain#0","geo_supply_chain#1"]},{"id":"R3","text":"客戶集中：最大單一客戶占 2025 年營收 12.8%、應收 10.2%；模組化擴產只對兩家超大規模業者有量承諾。","h_ref":"H1","clock":"🔥","threshold":"最大客戶占營收 > 15% 或占應收 > 20%；或任一模組化大客戶不續多年期量承諾","evidence_refs":["customer_concentration_credit#0"]},{"id":"R4","text":"供應鏈與分包執行：變壓器、配電開關、大型發電機交期常逾 6 個月，分包商與設備供應商延誤會拖專案進度與認列。","h_ref":"H1","clock":"⚡","threshold":"季營收低於共識 ≥ 5% 且管理層歸因設備交期或分包","evidence_refs":["geo_supply_chain#2","geo_supply_chain#3"]},{"id":"R5","text":"社會容忍度：資料中心暫停令（紐約州）與在地反對升溫，影響新案選址與電力取得。","h_ref":"H3","clock":"🐢","threshold":"公司主要營運州出現暫停令且公司揭露在手專案延期或取消","evidence_refs":[]}],"single_thing":{"description":"同店在手訂單首次出現環比下滑，且下滑來自科技類（資料中心）訂單。","why_fatal":"在手訂單是 18–24 個月後營收的領先指標；科技占營收 58%，訂單少於消化量代表 2028 年營收與定價力同時轉弱。現價以 FY2027 共識約 27 倍計價，市場會先把倍數壓向 16–20 倍：60×18＝1,080 美元，約 −34%，尚未計入 EPS 下修。","if_happens":"已持有者先減碼一半，下一季再降則清倉；未持有者重啟價改為 1,000 美元並重跑 DD。","how_monitor":"每季財報新聞稿的在手訂單與同店在手訂單；法說會揭露的科技類訂單與模組化淨訂單（第二季約 5.1 億美元）。","probability":"約 30%（12–24 個月）：在手訂單年增 73%、管線處歷史高檔壓低近期機率，但營收消化速度加快，使在手訂單持平的門檻逐季升高。"}},"appendix_a":{"growth_durability":6,"quality_score":8,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":27.2,"peg_fy2":1.2,"stress":{"pass":1,"total":3}},"eps_meta":{"base_eps_path":{"FY2025A":28.88,"FY2026E":49.01,"FY2027E":60.18,"FY2028E":73.85},"fy_end_month":12,"eps_basis":"GAAP 稀釋 EPS（公司無非 GAAP 調整，第二季 GAAP 與市場口徑同為 12.53）；FY2025A 取年度財報，FY2026E 起取 Koyfin 共識（2026-10-08）"},"catalysts":[{"date":"2026-10","date_precision":"month","type":"guidance","event":"第三季財報：同店營收、在手訂單、全年同店指引","impact":"高","watch":"在手訂單是否 ≥ $14B、季毛利率是否 ≥ 24.5%"},{"date":"2026-12","date_precision":"month","type":"capacity","event":"模組化產能逾 400 萬平方英尺","impact":"中","watch":"新增產能是否已有多年量承諾"},{"date":"2027-02","date_precision":"month","type":"guidance","event":"第四季財報與 2027 年指引","impact":"高","watch":"在手訂單是否 ≥ $16B、2027 同店指引與第四季高基期"},{"date":"2027-Q3","date_precision":"quarter","type":"capacity","event":"模組化產能約 500 萬平方英尺","impact":"中","watch":"是否新增前沿實驗室或主機代管量產合約"},{"date":"2026-Q4","date_precision":"quarter","type":"macro","event":"鋼鋁銅與電氣設備關稅調整","impact":"低","watch":"新標案毛利率"}]}
```

---

## 尾段：回覆格式

只回一個 JSON 陣列，①–⑧ 每條一個元素，八個全出，不得跳號、不得多列，陣列外不得有任何文字（不加前言、不加 markdown 圍欄、不加附註）：

```json
[{"item": "①", "light": "🔴|🟡|🟢", "judgment_path": "$.路徑", "reason": "一句話"}]
```
