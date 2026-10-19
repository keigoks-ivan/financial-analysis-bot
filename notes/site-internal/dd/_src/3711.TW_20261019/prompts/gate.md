你是 DD 管線 v20 的判斷層閘（gate），標的 3711.TW（20261019）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（29 條）
- `f_kpi0_gaap`（q1_business）｜營收（GAAP，合併）＝191064 NT$百萬｜期間與口徑：2Q26（季末 2026-06-30，公告於 2026-07-30）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：日月光投控 2Q26 財報新聞稿（SEC 6-K 備份）https://www.sec.gov/Archives/edgar/data/0001122411/000095010326011351/dp250868_6k.htm（numbers.latest_quarter_kpis.items[0]，as_of 2Q26（季末 2026-06-30，公告於 2026-07-30））
  - 註記：未取得
- `f_kpi1`（q1_business）｜毛利率＝21.0 %｜期間與口徑：2Q26（季末 2026-06-30，公告於 2026-07-30）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：日月光投控 2Q26 財報新聞稿（SEC 6-K 備份）https://www.sec.gov/Archives/edgar/data/0001122411/000095010326011351/dp250868_6k.htm（numbers.latest_quarter_kpis.items[1]，as_of 2Q26（季末 2026-06-30，公告於 2026-07-30））
  - 註記：未取得
- `f_kpi2_gaap`（q1_business）｜GAAP 營業利益／利益率＝21134 NT$百萬（利益率 11.1%）｜期間與口徑：2Q26（季末 2026-06-30，公告於 2026-07-30）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：日月光投控 2Q26 財報新聞稿（SEC 6-K 備份）https://www.sec.gov/Archives/edgar/data/0001122411/000095010326011351/dp250868_6k.htm（numbers.latest_quarter_kpis.items[2]，as_of 2Q26（季末 2026-06-30，公告於 2026-07-30））
  - 註記：未取得
- `f_kpi3`（q1_business）｜歸屬母公司淨利＝21068 NT$百萬｜期間與口徑：2Q26（季末 2026-06-30，公告於 2026-07-30）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：日月光投控 2Q26 財報新聞稿（SEC 6-K 備份）https://www.sec.gov/Archives/edgar/data/0001122411/000095010326011351/dp250868_6k.htm（numbers.latest_quarter_kpis.items[3]，as_of 2Q26（季末 2026-06-30，公告於 2026-07-30））
  - 註記：未取得
- `f_kpi6_3q26`（q1_business）｜管理層指引：3Q26＝合併營收 QoQ +21%～22%；毛利率 20.5%～21.5%；營業利益率 11.5%～12.5%；ATM 營收 QoQ +11%～13%、毛利率 28%～29%；EMS 營收 QoQ 約 +40%、營業利益率 3.2%～3.4%｜期間與口徑：2Q26（季末 2026-06-30，公告於 2026-07-30）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：日月光投控 2Q26 法說簡報（SEC 6-K）https://www.sec.gov/Archives/edgar/data/0001122411/000095010326011353/dp250875_6k.htm（匯率假設 US$1=NT$31.9）（numbers.latest_quarter_kpis.items[6]，as_of 2Q26（季末 2026-06-30，公告於 2026-07-30））
  - 註記：未取得
- `f_kpi7_2026`（q1_business）｜管理層指引：2026 全年＝ATM 營收年增約 35%（美元）；一般業務年增 20%（原 13%）；LEAP 服務營收「高於先前 US$35 億指引」｜期間與口徑：2Q26（季末 2026-06-30，公告於 2026-07-30）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：日月光投控 2Q26 法說簡報（SEC 6-K）https://www.sec.gov/Archives/edgar/data/0001122411/000095010326011353/dp250875_6k.htm（numbers.latest_quarter_kpis.items[7]，as_of 2Q26（季末 2026-06-30，公告於 2026-07-30））
  - 註記：未取得
- `f_peer_3711_tw_gross_margin_pct`（q2_moat）｜3711.TW 毛利率＝19.49 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.3711.TW.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_3711_tw_operating_margin_pct`（q2_moat）｜3711.TW 營業利益率＝9.89 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.3711.TW.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_3711_tw_fcf_margin_pct`（q2_moat）｜3711.TW FCF 利潤率＝-6.15 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.3711.TW.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_amkr_gross_margin_pct`（q2_moat）｜AMKR 毛利率＝15.51 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.AMKR.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_amkr_operating_margin_pct`（q2_moat）｜AMKR 營業利益率＝8.64 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.AMKR.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_6239_tw_operating_margin_pct`（q2_moat）｜6239.TW 營業利益率＝12.9 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.6239.TW.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_2449_tw_operating_margin_pct`（q2_moat）｜2449.TW 營業利益率＝26.86 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.2449.TW.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_2449_tw_fcf_margin_pct`（q2_moat）｜2449.TW FCF 利潤率＝-32.27 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.2449.TW.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝18.83 TWD/share｜期間與口徑：2026-10-19／yfinance 分析師共識平均（Koyfin 快照無此檔）；幣別同報價｜kind：estimate
  - 來源：yfinance earnings_estimate（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-10-19）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝29.22 TWD/share｜期間與口徑：2026-10-19／yfinance 分析師共識平均（Koyfin 快照無此檔）；幣別同報價｜kind：estimate
  - 來源：yfinance earnings_estimate（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-10-19）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝840390.43 TWD m｜期間與口徑：2026-10-19／yfinance revenue_estimate 0y 平均（17 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-10-19）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝1050397.31 TWD m｜期間與口徑：2026-10-19／yfinance revenue_estimate +1y 平均（17 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-10-19）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi4`（q4_capital）｜自由現金流（推算）＝-32835 NT$百萬｜期間與口徑：2Q26（季末 2026-06-30，公告於 2026-07-30）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：日月光投控 2Q26 財報新聞稿（SEC 6-K 備份）https://www.sec.gov/Archives/edgar/data/0001122411/000095010326011351/dp250868_6k.htm；營業現金流 47,014 減 PP&E 淨支出 79,849，由查證者推算，公司未自報 FCF（numbers.latest_quarter_kpis.items[4]，as_of 2Q26（季末 2026-06-30，公告於 2026-07-30））
  - 註記：未取得
- `f_kpi5`（q1_business）｜設備資本支出＝1695 US$百萬｜期間與口徑：2Q26（季末 2026-06-30，公告於 2026-07-30）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：日月光投控 2Q26 財報新聞稿（SEC 6-K 備份）https://www.sec.gov/Archives/edgar/data/0001122411/000095010326011351/dp250868_6k.htm（numbers.latest_quarter_kpis.items[5]，as_of 2Q26（季末 2026-06-30，公告於 2026-07-30））
  - 註記：未取得
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝190149.15 TWD m｜期間與口徑：2026-10-19／yfinance 最新一季：總債務 295792.41、現金 105643.26（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-10-19）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝0.983 %｜期間與口徑：2026-10-19／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-10-19）
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝670.0 TWD｜期間與口徑：2026-10-19（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-10-19（RTH 收盤，UTC））
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝51.26 x｜期間與口徑：2026-10-19（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-10-19（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝100.0 %｜期間與口徑：2026-10-19（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-10-19（RTH 收盤，UTC））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝4.14 x｜期間與口徑：2026-10-19（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-10-19（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝100.0 %｜期間與口徑：2026-10-19（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-10-19（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝4.41 x｜期間與口徑：2026-10-19（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-10-19（RTH 收盤，UTC））
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝46.51 %｜期間與口徑：2026-10-19（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^TWII｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-10-19（RTH 收盤，UTC））

### findings_digest 中方向為負或來源衝突的條目（7 條）
- `competitive_share_entrants#3`（competitive_share_entrants｜方向 -｜狀態 ok）：對手Amkor 2026年Q2營收創高約19億美元、年增26%，7月宣布與NVIDIA多年期15億美元美國封測合作；Intel EMIB-T在高階封裝積壓訂單增加（Zacks/Nasdaq 轉述）
  - 來源：Nasdaq/Zacks: Can ASE Technology Sustain Its Recent Margin Expansion?（as_of 2026-08-01）｜affects：decision_inputs.bear、moat_trend
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：玉山投顧 2025 年 4 月分析：台廠中日月光美國比重最高、製造據點分布最廣；預期先進封測客戶可能以代購設備換取封測價格持穩，傳統封測則可能被要求降價以分擔客戶關稅成本（分析師預期，非公司公告）
  - 來源：玉山證券 esunsec.com.tw 研究文章（as_of 2025-04-30）｜affects：decision_inputs.bear、valuation
- `geo_supply_chain#2`（geo_supply_chain｜方向 -｜狀態 ok）：2026年股東會：集團採「台灣優先」原則，先在台灣把封測整合與自動化做成熟再複製海外；2024年股東會曾稱不排除在美國、日本、墨西哥增加先進封裝產能；未找到越南、泰國的2026年產能資訊
  - 來源：自由時報 日月光「卯足全力」擴產 今年啟動15座擴廠計畫（as_of 2026-06-01）｜affects：decision_inputs.bear、thesis.R
- `geo_supply_chain#3`（geo_supply_chain｜方向 -｜狀態 ok）：日月光高層（黃義從）於SEMICON談話稱部分材料由少數廠商主導、甚至握有全球8、9成市占，替代供應商產能有限；部分特殊氣體與原物料集中於特定國家或地區；任一供應商出問題封裝端可能無法出貨
  - 來源：鉅亨/UAnalyze 〈SEMICON〉日月光：材料聯盟要「築高牆」（as_of 2025-09-01）｜affects：decision_inputs.bear、thesis.R
- `substitute_technology#2`（substitute_technology｜方向 -｜狀態 ok）：搜尋摘要提及：客戶自建或英特爾晶圓代工加封測一條龍可能壓低封測價格、分流AI測試訂單，但短期英特爾基板良率偏低、實質影響有限（來源網址未能對應到單一篇，僅作線索）
  - 來源：搜尋結果彙整（未對應單一網址）（as_of 2026-08-04）｜affects：decision_inputs.bear
- `cyclical_prior_downcycle_behavior#0`（cyclical_prior_downcycle_behavior｜方向 -｜狀態 ok）：搜尋摘要稱 2023 年第一季日月光投控毛利率降至 14.8%，為四年來低點，因客戶庫存調整、稼動率降溫；2022Q4 封裝、測試稼動率降至 75-80%（僅搜尋摘要，未讀原文頁面）
  - 來源：鉅亨網／中央社日月光法說報導（搜尋結果）（as_of 2023-04-27）｜affects：decision_inputs.bear、thesis.R
- `cyclical_prior_downcycle_behavior#1`（cyclical_prior_downcycle_behavior｜方向 -｜狀態 ok）：搜尋摘要稱 2023 年全年營收 5,819.14 億元、年減 13%，全年毛利率 15.8%，較 2022 年減少 4.4 個百分點；2022 全年毛利率 20.1%；2023Q4 毛利率 16%（摘要轉述，未讀原文）
  - 來源：TechNews 日月光投控 2023 EPS 7.39 元報導（搜尋結果）（as_of 2024-02-01）｜affects：decision_inputs.bear、valuation

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 4 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/3711.TW_20261019/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":1210.0,"bear_5y_price":312.0,"p_bull_pct":25,"p_bear_pct":30,"upside_5y_pct":0.7,"ev5y_pct":4.5,"irr_base_pct":0.1,"asym_ratio":1.3,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":18.83,"pe":35.58,"basis":"FY2026E 共識 EPS（FY1）；終端倍數同樣套在當年度 EPS 上，口徑一致"},"eps":{"bull":[31.0,37.0,43.0,49.0,55.0],"base":[28.5,30.5,32.5,35.0,37.5],"bear":[24.0,20.0,18.0,21.0,24.0]},"pe":{"bull":22,"base":18,"bear":13},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0.983,"net_buyback":0},"second_stage":{"bull_cagr_pct":10,"base_cagr_pct":6},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### 3711.TW_Q1_2026_Earnings_Call_20260429.md
- 2026-04-29｜CFO｜guidance：CFO 表示 2026 年 LEAP 服務營收預期較先前財測上調約 10%，超過 35 億美元（原話："reaching over USD 3.5 billion"）
- 2026-04-29｜CFO｜guidance：CFO 表示 2027 年 LEAP 增量營收預期比今年更強（原話："even stronger incremental revenue growth than this year"）
- 2026-04-29｜CFO｜guidance：CFO 給 Q2 合併營收季增 7%~9% 的財測（原話："consolidated second quarter revenue should grow by 7% to 9%"）
- 2026-04-29｜CFO｜guidance：CFO 給 Q2 ATM 營收季增 9%~11% 的財測（原話："should grow by 9% to 11% quarter-over-quarter"）
- 2026-04-29｜CFO｜guidance：CFO 給 Q2 ATM 毛利率 26%~27% 的財測（原話："second quarter gross margin should be between 26% to 27%"）
- 2026-04-29｜CFO｜guidance：CFO 給 EMS Q2 營收年增至少 10% 的財測（原話："should grow at least 10% year-over-year"）
- 2026-04-29｜CFO｜guidance：CFO 維持一般（非 LEAP）封測營收成長約 13%，與去年相同（原話："repeat of last year's growth rate of about 13%"）
- 2026-04-29｜CFO｜capital_allocation：CFO 表示調升今年資本支出，機台部分增加 6 億美元（原話："an incremental USD 0.6 billion in machinery"）
- 2026-04-29｜CFO｜capital_allocation：CFO 說明新增資本支出三分之二用於建物與廠房（原話："2/3 of the increase of our CapEx is for building"）
- 2026-04-29｜CFO｜capital_allocation：CFO 說明新增機台支出中約 6 億用於晶圓針測，產能明年開出（原話："NTD 600 million worth of the CapEx is really for wafer sort"）
- 2026-04-29｜CFO｜capital_allocation：CFO 表示明年可能又是資本支出偏重的一年（原話："next year could be another CapEx heavy year for us"）
- 2026-04-29｜CFO｜capital_allocation：CFO 表示今年資金缺口主要以新增借款補足（原話："will mostly be funded by additional borrowing"）
- 2026-04-29｜CFO｜capital_allocation：CFO 不排除今年再度上調資本支出（原話："I wouldn't preclude that there will be a further need"）
- 2026-04-29｜CFO｜capital_allocation：管理層說明馬來西亞向 ADI 買下的廠房作為海外緩衝產能（原話："we've acquired a factory from ADI"）
- 2026-04-29｜CFO｜margin：CFO 表示 ATM Q1 毛利率 26% 高於原先預期的 24.5%（原話："ahead of our original expectation of 24.5%"）
- 2026-04-29｜IR｜margin：IR 說明今年折舊成長快於營收，因 LEAP 投資（原話："we see our depreciation rising faster than revenues"）
- 2026-04-29｜IR｜margin：IR 說明合併毛利率季增主因為新台幣貶值（原話："primarily due to NT dollar depreciation"）
- 2026-04-29｜IR｜margin：IR 表示 ATM 毛利率預期逐季上升，年底達結構性區間高端（原話："reach the higher end of our structural margins"）
- 2026-04-29｜CFO｜margin：CFO 說明 LEAP 機台大批裝機，爬坡期對毛利率造成壓力（原話："normally creates a some of -- some pressure on the margin"）
- 2026-04-29｜CFO｜margin：CFO 表示不調升結構性毛利率區間，待情況穩定再檢視（原話："we will rather wait until things are more settled"）
- 2026-04-29｜CFO｜margin：CFO 表示尚未提供折舊稀釋的量化，下季可能提供（原話："Maybe we can have that for you next quarter."）
- 2026-04-29｜IR｜margin：IR 揭露 ATM 占合併營收 65%、占營業利益 91%（原話："represented 65% of our consolidated holding company revenue"）
- 2026-04-29｜CFO｜commitment：CFO 結語承諾明年情況較穩定時檢視結構性毛利率區間（原話："we will be reviewing our structural margin range"）
- 2026-04-29｜CFO｜commitment：CFO 表示會持續投資、不吝於擴充產能與研發（原話："we're certainly not going to be shy"）
- 2026-04-29｜CFO｜product：CFO 說明 LEAP 組成約七成五為封裝、兩成五為測試（原話："about 75% in assembly and 25% in tests"）
- 2026-04-29｜CFO｜product：CFO 表示 full process 今年營收仍預期達 3 億元（原話："reach this NTD 300 million revenue mark for this year"）
- 2026-04-29｜CFO｜product：CFO 表示 full process 理論上對 LEAP 毛利有加成（原話："in theory, it should be accretive to LEAP"）
- 2026-04-29｜CFO｜product：CFO 表示面板級封裝已有全自動試產線送客戶驗證（原話："a fully automated pilot line for customer qualification"）
- 2026-04-29｜CFO｜product：CFO 表示 CPO 尚無營收數字（原話："Right now, we don't have a number for it."）
- 2026-04-29｜CFO｜product：CFO 表示 CPO 何時、多少營收貢獻現在說還太早（原話："it's a bit premature to say when and how much"）
- 2026-04-29｜CFO｜product：CFO 表示測試資源聚焦晶圓針測而非 final test（原話："focusing our resources in wafer sort at this point"）
- 2026-04-29｜CFO｜product：CFO 表示兩棟新取得廠房皆供 LEAP，明年初起逐步爬坡（原話："ramping up progressively starting from early next year"）
- 2026-04-29｜CFO｜customer：CFO 表示多家客戶要求 full process 產能（原話："multiple customers requesting for this kind of capacity"）
- 2026-04-29｜IR｜customer：IR 表示客戶偏好製造確定性（原話："customers prefer manufacturing certainty"）
- 2026-04-29｜CFO｜customer：CFO 表示 Q1 營收並非客戶提前拉貨所致（原話："I don't think it's because of the customers' early pull-in"）
- 2026-04-29｜CFO｜competition：CFO 表示不直接回答是否漲價，但成本上升可完全轉嫁（原話："those can be fully passed through"）
- 2026-04-29｜CFO｜risk：CFO 表示 PC 與手機市場疲弱持續（原話："PC and cellphone market softness continues"）
- 2026-04-29｜IR｜risk：IR 表示產能與上游晶圓代工夥伴產能有限（原話："finite with limited ability to be pulled forward"）

### 問答異常語氣（迴避／改口／保留）
- 3711.TW_Q1_2026_Earnings_Call_20260429.md｜問：Haas Liu 追問可否量化新技術爬坡成本對 Q1、Q2 及下半年毛利率的稀釋（如 50~100bp）｜答法：CFO 未給數字，只說有折舊占比擴大、尚未能量化，改說下季可能提供
- 3711.TW_Q1_2026_Earnings_Call_20260429.md｜問：Gokul Hariharan 追問既然毛利率已達結構區間高端，為何不上調結構性毛利率區間｜答法：CFO 未直接回答是否上調，改說事情變動快、等穩定後明年再看
- 3711.TW_Q1_2026_Earnings_Call_20260429.md｜問：Charlie Chan 追問是否主動漲價｜答法：CFO 表示無法直接回答是否漲價，只說會依毛利要求訂價、成本可轉嫁
- 3711.TW_Q1_2026_Earnings_Call_20260429.md｜問：Gokul Hariharan 追問 2027 年 LEAP 增量是否至少 20 億元以上、是否達 55 億｜答法：CFO 不給具體數字，只說 20 億是基準、動能會更強

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 4 | 4 |
| customer_second_source | found | 2 | 3 |
| customer_concentration_credit | found | 3 | 3 |
| supply_demand_durability | found | 5 | 4 |
| regulatory_antitrust | none | 0 | 3 |
| reg_tariff_export | found | 3 | 4 |
| geo_supply_chain | found | 4 | 3 |
| end_markets | found | 5 | 3 |
| substitute_technology | found | 3 | 3 |
| channel_business_model_shift | found | 4 | 3 |
| capital_markets_pricing | found | 5 | 4 |
| major_events | none | 0 | 5 |
| cyclical_supply_discipline_capacity | found | 4 | 3 |
| cyclical_inventory_price_position | found | 3 | 3 |
| cyclical_prior_downcycle_behavior | found | 3 | 3 |

未涵蓋／不適用軸的查詢詞原文（供判相關性）：
- **regulatory_antitrust**（none）：日月光投控 公平會 結合 OR 處分 OR 調查；日月光投控 反壟斷 OR 反托拉斯 2026；3711.TW ASE Technology Holding antitrust OR competition investigation 2026
- **major_events**（none）：日月光投控 併購 OR 合併 OR 公開收購 OR 私募 2025 2026；日月光投控 訴訟 OR 專利侵權 OR 投保中心；日月光投控 召回 OR 品質異常 OR 停產；日月光投控 金管會 OR 證交所 OR 櫃買中心 處分 OR 財報重編 OR 保留意見；日月光投控 召回 OR 品質異常 OR 停產 OR 火災 OR 停工

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"status":"no_prior_dd"}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"3711.TW","date":"2026-10-19","schema":"v15.2","contract":"v19","company_name":"日月光投控"},"oneliner":"AI 先進封裝供不應求，封測毛利率可望突破 30%，但 670 元已貼近法人目標價下緣，按 2027 年尖峰獲利仍要 23 倍；勝負在 2028 年產能大增後的稼動率，等回到約 500 元或毛利證明是結構性再談。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/3711.TW_20261019/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/3711.TW_20261019/scenario.json","answers":{"q1_business":{"verdict":"賺的是 AI 晶片封裝測試的產能稀缺錢：錢卡在「把晶圓變成可出貨晶片」這一節，封測部門以 66% 營收拿走 94% 營業利益。","reasoning":"2Q26 合併營收 1,911 億元、季增 10%、年增 27%，毛利率 21.0%、營業利益率 11.1%，歸屬母公司淨利 211 億元。其中約 57 億元是投資評價與匯率避險利益，公司自己說可能不會重複，約合每股 1.1 元，判讀核心獲利時要扣掉。第三季指引合併營收季增 21%～22%，但 EMS 季增約 40% 主要來自記憶體零件漲價轉嫁，屬於低毛利的過路營收，實質成長要看封測（季增 11%～13%、毛利率 28%～29%）。產業時鐘在擴張期：管理層說限制在裝機與蓋廠速度而不是需求，混合稼動率 80%～85%，打線、測試都接近滿載。供需持久度：需求面到 2027 年能見度高，但供給可逆性高，公司同時進行 13 個新建、8 個改建工程，法人估日月光 CoWoS 類月產能 2027 年底會是 2026 年底的數倍，2028 年後供給可能追上需求。循環位置讀數：資本支出約為折舊三倍、稼動率近滿，偏賣方；訂單能見度領先資本支出、量價齊升，偏買方；客戶集中但信用強、股價貼近法人目標價，屬中性，整體判在中段，持有不加。長期成長部分（LEAP 先進封測）另計，不隨循環賣出。單點依賴：前五大客戶占 44%，另有單一客戶占比超過一成，且未具名；與主要晶圓代工夥伴的委外分工是 LEAP 成長來源，這是集中度風險，也是護城河的一部分。","fact_refs":["f_kpi0_gaap","f_kpi1","f_kpi2_gaap","f_kpi3","f_kpi6_3q26","f_kpi7_2026"],"verdict_values":{"revenue_quality":"2Q26 合併營收 1,911 億元，封測占 66%、貢獻 94% 營業利益（一年前為 61%／87%）；第三季 EMS 季增約 40% 主要是記憶體零件漲價轉嫁，合併營收成長會高估實質成長。","unit_econ_note":"2Q26 封測毛利率 27.3%、營業利益率 15.7%；EMS 毛利率 8.9%、營業利益率 2.4%；合併毛利率 21.0%、營業利益率 11.1%。","archetype":{"primary":"循環/商品","secondary":"品質複利成長","confidence":"中","fingerprint":"資本支出建設型循環：資本支出約為折舊三倍、稼動率近滿、毛利率位於自身區間上緣；另有 LEAP 先進封測屬長期成長部分"},"industry":{"clock_phase":"II","sd_verdict_source":"供給可逆性高：需求到 2027 年能見度高（管理層稱需求不是問題、限制在執行），但公司同時進行約 20 個廠房工程，且法人估 OSAT 端 CoWoS 類產能 2027 年底較 2026 年底大幅增加，2028 年後供給可能追上需求。","bargaining":{"up":"關鍵材料（基板、特殊氣體）由少數供應商主導，部分握有全球八、九成市占，上游議價偏弱。","down":"前五大客戶占 44%、單一客戶逾一成；目前供不應求，管理層稱材料成本可完全轉嫁，下游議價暫時偏強，但屬週期性。","geo":"產能以台灣為主，美國只有研發、測試開發與小型廠；同業 Amkor 已擴大美國產能，客戶在地化要求升高。"},"profit_pool_dir":"利潤池小幅由晶圓代工往封裝端移動（封裝往系統架構上移），但最難取代的前段仍在晶圓代工夥伴手上。","tam_table":{"expanded":false,"reason":"事實表未涵蓋先進封裝 TAM、滲透率與利潤池占比的歷史數字；屬承重項但證據包沒有，標為資料缺口。"}}}},"q2_moat":{"verdict":"↑：先進封裝執行力與定價在擴大，但定價改善有相當部分來自供不應求，未經下行驗證。","reasoning":"機制是規模與台灣群聚、全自動產線，加上與主要晶圓代工夥伴的委外分工位置；純封測代工不與客戶、晶圓廠或基板廠競爭，管理層把多年累積的客戶信任列為先行者優勢。可證方向：TTM 毛利率 19.5% 高於 Amkor 15.5%，營業利益率 9.9% 高於 Amkor 8.6%（合併數字含 EMS 稀釋，封測單看 2Q26 為 15.7%）；封測毛利率一年內上升 5.4 個百分點，封測占營業利益由 87% 升至 94%。投入資本報酬的同業差距事實表未涵蓋，只能用利潤率代替。執行力評 8：LEAP 2026 年高於 35 億美元並有 2027 倍增的產能能見度，Full process 與面板級封裝依進度推進。定價力評 6：漲價與毛利率突破結構上限是真的，但管理層自己把近期成長限制歸因於產能，下行時這部分會回吐；2023 年毛利率曾掉到 15.8%。產業態勢屬雙向拉鋸：結構轉好（AI 先進封裝供不應求，法人稱 2027 年仍滿載）與競爭變動（Amkor 取得 NVIDIA 美國多年期合約、Intel EMIB 積壓訂單增加、客戶在地化）同時發生。","fact_refs":["f_peer_3711_tw_gross_margin_pct","f_peer_3711_tw_operating_margin_pct","f_peer_3711_tw_fcf_margin_pct","f_peer_amkr_gross_margin_pct","f_peer_amkr_operating_margin_pct","f_peer_6239_tw_operating_margin_pct","f_peer_2449_tw_operating_margin_pct","f_peer_2449_tw_fcf_margin_pct","f_kpi1"],"verdict_values":{"moat":{"mechanism":"規模與台灣群聚＋全自動產線＋與主要晶圓代工夥伴的委外分工位置；純封測代工不與生態系任何一方競爭，累積多年認證與客戶信任。","execution":8,"pricing":6,"grade":"B","trend":"↑","trend_evidence":"封測毛利率 2Q25→2Q26 上升 5.4 個百分點、封測占營業利益 87%→94%；TTM 毛利率與營業利益率皆高於 Amkor；但價格面改善部分來自供不應求，尚未經過下行循環檢驗。","competitor_notes":[{"name":"AMKR","strategy_note":"毛利率與營業利益率皆低於日月光，但拿到 NVIDIA 美國多年期 15 億美元合作，是在地化產能這條路上的主要對手。"},{"name":"6239.TW","strategy_note":"力成營業利益率 12.9% 高於日月光合併數字，但以記憶體封測為主，與日月光的 AI 邏輯先進封裝重疊有限。"},{"name":"2449.TW","strategy_note":"京元電是測試專業廠，營業利益率 26.9% 最高，但 FCF 利潤率 -32% 顯示擴產最激進，AI 測試訂單上是直接對手。"}],"threats":[{"level":"🟡","text":"Amkor 2Q26 營收年增 26%，並與 NVIDIA 簽美國多年期 15 億美元封測合作，美國在地產能可能分走最大客戶的新增訂單。","p":30,"evidence_refs":["competitive_share_entrants#3"]},{"level":"🟡","text":"Intel EMIB-T 高階封裝積壓訂單增加，晶圓代工加封裝一條龍可能分流部分 AI 封裝需求；管理層稱也在配合 EMIB，非零和。","p":25,"evidence_refs":["competitive_share_entrants#3"]},{"level":"🟡","text":"客戶在地化：公司採台灣優先，美國只有研發與測試廠；分析師預期傳統封測可能被要求降價分攤客戶關稅成本。","p":25,"evidence_refs":["geo_supply_chain#2","reg_tariff_export#0"]},{"level":"🟡","text":"關鍵材料由少數供應商主導、替代產能有限，任一供應商出問題封裝端可能無法出貨。","p":15,"evidence_refs":["geo_supply_chain#3"]}],"roic_durability":{"quadrant":"低利益率×低周轉（當期投入資本報酬率約 9.3%，貼近資金成本上緣）","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者是晶片設計公司、付款最終來自雲端業者的 AI 資本支出；客戶目前要的是產能而非價格，需求急迫，但持久性取決於 AI 資本支出週期，管理層自己也把它分成技術十五到二十年、生意約四季的能見度。"},{"item":"決策層級","level":"🟡","text":"替代性要看單一產品的封裝認證：換封測廠要重新認證，先行者有優勢；但客戶已同時下單 Amkor，Intel EMIB 也在爭取，最小決策單位上已有兩到三家可選。"},{"item":"價值鏈分配","level":"🟡","text":"價值鏈裡最難取代的是晶圓代工前段，封測拿到的是代工夥伴分出來的部分；管理層稱封裝正往系統架構上移，但結構毛利上限 30% 仍遠低於晶圓代工，分配位置在改善但仍居次。"},{"item":"社會容忍度","level":"🟢","text":"企業對企業的中間服務，終端消費者看不到封測價格，沒有社會面的漲價天花板；政策面的壓力來自地緣政治與在地化要求，已列入威脅。"}],"roiic":"前瞻隱含約 19%（2027 共識淨利增量約 457 億元 ÷ 2026 年淨資本支出約 2,360 億元）；已實現值事實表未涵蓋；跨循環取 12%","reinvest_rate":"約 285%（2026 年資本支出 105 億美元×31.9 ≈ 3,350 億元，減年化折舊約 990 億元，除以 2026 共識淨利約 828 億元）；超過 100% 的部分靠借款","endo_ceiling":12,"formula_note":"當期報酬：TTM 營業利益率 9.89%×(1−18% 稅率) ≈ 8.1%；投入資本 ≈ 淨負債 1,988 億元＋權益約 4,230 億元（淨負債÷權益 47% 反推，2Q26 法說資產負債頁）≈ 6,220 億元；TTM 營收 ≈ 市值 29,464 億元 ÷ P/S 4.14 ≈ 7,117 億元，周轉 1.14 倍，報酬率約 9.3%。折舊以 2Q26 EBITDA 458 億元減營業利益 211 億元約 247 億元／季推估。內生成長＝增量報酬 12%×自有資金再投資率上限 100%＝12%；借款支應可暫時拉到約 24%，不屬內生。"}}}},"q3_growth":{"verdict":"後五年跑道中等：先進封裝已占封測營收近半，CPO 與面板級封裝是下一條曲線，但目前沒有營收數字。","reasoning":"成長來源是量（新產能開出）、價（漲價與成本轉嫁）與組合（LEAP 占比上升），沒有併購或回購。共識 EPS 由 2025 年 8.89 元到 2026 年 18.83 元、2027 年 29.22 元，兩年年化約 81%；同期營收共識只成長約三成與兩成五，第三年共識事實表未涵蓋。內生天花板 12%（借款支應約 24%），缺口主要歸因於利潤率擴張：營業利益率由 2025 年 8.0% 升到 2Q26 11.1%，第三季指引 11.5%～12.5%，屬營運槓桿與稼動率，循環性成分高。跑道：先進封裝（凸塊、覆晶、晶圓級、系統級）2025 年第三季已占封測營收 48%，落在 35%～70% 區間；CPO 年底初期生產、面板級全自動線 2027 年第一季量產，屬有來源的下一條曲線，但 CPO 管理層說要再兩季才給數字，尚未能算進主要跑道。衰退訊號亮兩項：EPS 成長遠高於營收成長；自由現金流÷淨利連兩年低於 0.75。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_kpi7_2026","f_kpi6_3q26"],"verdict_values":{"growth":{"driver_mix":"量（新產能）＋價（漲價與轉嫁）＋組合（LEAP 占比上升）；無併購、無回購","runway_years":"事實表未涵蓋滲透率序列；先進封裝約占封測營收 48%（2025 年第三季），已過三成","runway_post_y5":"🟡","endo_ceiling_basis":"增量報酬跨循環取 12%（前瞻共識隱含約 19% 打折、當期約 9.3%）×自有資金再投資率上限 100%；共識兩年 EPS 年化約 81%，遠超天花板，缺口歸因利潤率擴張。","segments":[{"item":"封測（ATM）","value":"2Q26 營收 1,261 億元（含內部交易）、毛利率 27.3%、營業利益率 15.7%；2026 年美元營收預估年增約 35%"},{"item":"其中 LEAP 先進封測","value":"2026 年高於 35 億美元、2027 年目標倍增；約七成設備資本支出投入此處"},{"item":"EMS 電子代工","value":"2Q26 營收 658 億元、毛利率 8.9%、營業利益率 2.4%；2026 全年成長低於 20%"}],"decay_signals":["亮：EPS 成長遠高於營收成長（2026 共識 EPS 年增約一倍、營收約三成）","亮：自由現金流÷淨利連兩年低於 0.75（2024 年約 0.28、2025 年為負）","未亮：毛利率連兩季年減、核心市占縮減、提價後銷量下滑、替代技術壓縮市場、產業倍數系統性下移、停止投資新產能"],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"處於重投資期：營業現金流與新增借款全部投入擴產，自由現金流為負，股息殖利率約 1%，沒有回購。","reasoning":"2Q26 營業現金流 470 億元，廠房設備淨支出 798 億元，推算自由現金流 -328 億元；TTM 自由現金流利潤率 -6.15%。年度看，2024 年自由現金流 91 億元對淨利 324 億元（約 0.28），2025 年 -236 億元對淨利 400 億元。2026 年資本支出三度上修到 105 億美元（廠房 40 億、設備 65 億），4 月時財務長說資金缺口主要靠新增借款，7 月說負現金流會持續一段時間。淨負債約 1,901 億元，2Q26 淨負債÷權益 47%，未動用額度 3,962 億元，短期資金無虞。現金去向：擴產遠大於股息，無回購、無大型併購（購入既有廠房屬資本支出）。員工股票酬勞事實表未涵蓋。","fact_refs":["f_kpi4","f_kpi5","f_net_debt_m","f_dividend_yield_ttm"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":false,"passed":null,"input":"近期無超過市值 5% 的併購；擴產以自建與購入既有廠房為主，金額事實表未涵蓋"},{"name":"buyback_yield","applicable":false,"passed":null,"input":"未見回購；股息殖利率約 1%"},{"name":"sbc_dilution","applicable":true,"passed":null,"input":"事實表未涵蓋員工股票酬勞；2Q26 稀釋 EPS 4.61 元對基本 EPS 4.80 元，差約 4%，來源未拆分"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長靠自建產能與購入既有廠房，不是靠併購撐；無回購，股東回報只有約 1% 股息，無須展開。"}}}},"q5_valuation":{"verdict":"670 元要求 2027 年共識 EPS 29 元兌現，而且 2028 年後產能大增時毛利率不回吐、倍數維持 20 倍以上；前半我大致信，後半不信。","reasoning":"現價對 2026 共識 EPS 18.83 元是 35.6 倍，對 2027 共識 29.22 元是 22.9 倍；trailing 本益比 51 倍、股價營收比 4.14 倍、EV/S 4.41 倍都在近四個年度端點的最高。法人目標價 685～835 元，現價已在區間下緣附近。我的 Base：2027 年 EPS 28.5 元給 22 倍約 627 元，短期約 -6%；五年後 EPS 37.5 元給 18 倍約 675 元，中期幾乎持平。2027 年 EPS 本身建立在稼動率近滿、毛利率破結構上限的尖峰假設上，2Q26 淨利還含約每股 1.1 元的一次性利益，用它算出來的 23 倍不構成便宜的理由。","fact_refs":["f_price_at_dd","f_pe_current","f_pe_percentile","f_ps_current","f_ps_percentile","f_ev_s_current","f_consensus_eps_fy1","f_consensus_eps_fy2","f_week26_return_pct"],"verdict_values":{"valuation":{"basis":"前瞻本益比（FY1／FY2 共識 EPS）","tier":"台灣大型封測（對照 Amkor、力成、京元電）","peers":{"expanded":false,"reason":"事實表只有同業利潤率，沒有同業前瞻本益比與目標價，無法做倍數對照。"},"fwd_pe":35.58,"peg":2.4,"percentile_5y":null,"val_light":"🟠","val_light_derivation":"前瞻一年 35.6 倍、2027 共識 22.9 倍；trailing 本益比、股價營收比、EV/S 皆為近四個年度端點最高（只有四點，非五年分位，故五年分位留空）；PEG 以 Base 情境 2026→2031 年 EPS 年化約 14.8% 計為 2.4，若用共識兩年 81% 計只有 0.4，但後者來自循環底部基期與利潤率擴張，不採用；Base 五年目標約 675 元，上檔幾乎為零。","upside_short_pct":-6,"upside_mid_pct":1,"denominator_disputed":true,"denominator_note":"2Q26 淨利含約 57 億元評價與避險利益（約每股 1.1 元），2027 共識 EPS 又建立在稼動率近滿、毛利率破結構上限的尖峰假設上；分母本身就是爭點，按 2027 年 23 倍算便宜的說法不成立。"}}},"q6_how_wrong":{"verdict":"最可能看錯在把尖峰毛利當常態：2028 年產能大增若碰上 AI 資本支出消化，稼動率與毛利率會像 2023 年那樣回吐，而這次折舊基數更大。","reasoning":"三個視角都寫在反證紀錄。論點失敗的故事有歷史先例：2022→2023 年營收年減 13%、毛利率 20.1%→15.8%、稀釋 EPS 13.81→7.18 元；本輪資本支出是過去的數倍，自由現金流已為負、淨負債約 1,901 億元。價格已反映太多：26 週已漲 46.5%，trailing 51 倍。兩項衰退訊號亮燈，屬中度陷阱風險；主要擔心的不是生意變差，而是在循環高點付出成長股的倍數。","fact_refs":["f_week26_return_pct","f_pe_current","f_kpi4","f_net_debt_m"],"verdict_values":{"trap":{"verdict":"🟡","label":"獲利率在循環高點、自由現金流為負，倍數按尖峰獲利仍偏高"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":18.83,"pe":35.58,"basis":"FY2026E 共識 EPS（FY1）；終端倍數同樣套在當年度 EPS 上，口徑一致"},"eps":{"bull":[31.0,37.0,43.0,49.0,55.0],"base":[28.5,30.5,32.5,35.0,37.5],"bear":[24.0,20.0,18.0,21.0,24.0]},"pe":{"bull":22,"base":18,"bear":13},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0.98,"net_buyback":0},"second_stage":{"bull_cagr_pct":10,"base_cagr_pct":6},"max_dd":{"lo":-60,"hi":-45,"basis":"2023 年下行循環稀釋 EPS 由 13.81 元跌到 7.18 元（約 -48%），毛利率由 20.1% 降到 15.8%；本輪起點倍數更高（前瞻 35.6 倍、trailing 51 倍），獲利回落三成加倍數收縮到 13～15 倍，推得 -45% 到 -60%；Bear 終點約 -53% 落在區間內。","trigger_time":null},"basis":{"bull":"2027 年 LEAP 倍增並超過共識，封測毛利率站穩 30% 以上，Full process 與面板級封裝、CPO 2028 年起貢獻，2028 年後產能被需求吸收","base":"2027 年略低於共識（產能開出時間延誤與 EMS 稀釋），2028～2029 年 OSAT 先進封裝產能大增使價格與稼動率正常化，之後以約 7% 成長；倍數回到循環股中段 18 倍","bear":"2027 年產能如期開出但 AI 資本支出進入消化，2028～2029 年稼動率跌破 75%、毛利率回到 2023 年式低點，新增折舊壓縮獲利，倍數回到 13 倍"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"2023 年下行時營收年減 13%、毛利率由 20.1% 跌到 15.8%、EPS 腰斬；法人估日月光 CoWoS 類月產能 2027 年底是 2026 年底的數倍，公司另有約 15 個新廠為 2029～2030 年需求準備。","assumption":"AI 先進封裝需求在 2028 年後仍能吸收全部新增產能。","consequence":"若需求消化，稼動率跌破 75%，更大的折舊基數讓毛利率掉得比 2023 年更深，EPS 回到約 18～20 元、倍數 13 倍，股價約 250～300 元。","ruling":"採納：作為 Bear 情境，機率 30%；管理層自己說產能工程足以撐到 2028～2029 年，代表產能是按需求高峰在蓋。","watch":"混合稼動率、封測毛利率、月營收年增率","evidence_refs":["cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#1","cyclical_supply_discipline_capacity#3","cyclical_supply_discipline_capacity#1"],"fact_refs":["f_kpi1","f_net_debt_m"]},{"view":"論點成功但股東經濟變差","evidence":"自由現金流 2025 年 -236 億元、2Q26 單季 -328 億元，財務長說負現金流會持續一段時間；公司採台灣優先，客戶在地化壓力升高，分析師預期傳統封測可能被要求分攤關稅。","assumption":"LEAP 倍增帶來的利潤足以覆蓋 105 億美元級的年度資本支出，並在 2028 年轉正。","consequence":"營收與 EPS 都達標，但現金被持續擴產與海外高成本產能吃掉，淨負債上升、股東拿到的現金報酬很少，倍數難以維持。","ruling":"部分採納：短期資金無虞（未動用額度 3,962 億元），但把 2028 年自由現金流轉正列為 H3 的驗證點。","watch":"淨負債÷權益、2027 年資本支出指引、美國產能規劃","evidence_refs":["geo_supply_chain#2","reg_tariff_export#0"],"fact_refs":["f_kpi4","f_net_debt_m"]},{"view":"價格已反映太多","evidence":"現價 670 元，前瞻一年 35.6 倍、2027 共識 22.9 倍，trailing 倍數在近四個年度端點最高；法人目標價 685～835 元，26 週已漲 46.5%。","assumption":"市場會持續用成長股倍數看待一個循環高點的封測廠。","consequence":"即使 2027 年達標，只要市場開始按 2028 年正常化獲利定價，股價就沒有上檔。","ruling":"採納：Base 五年上檔約 1%，不追，等價格或毛利證據擇一先到。","watch":"股價對 2027 共識 EPS 的倍數、法人目標價調整方向","evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#2"],"fact_refs":["f_pe_current","f_pe_percentile","f_week26_return_pct","f_consensus_eps_fy2"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 None → 本次 ✅","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=None","side_b":"本次 ma=✅","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 None → 本次 670.0","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=None","side_b":"本次 price_at_dd=670.0","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"毛利率是結構性還是週期性","cause":null,"prior_field":null,"side_a":"管理層：第四季封測毛利率很可能突破 30% 結構上限，將檢討上調結構區間，材料成本可完全轉嫁（2026-07-30 財務長董宏思）。","side_b":"2023 年下行時合併毛利率由 20.1% 跌到 15.8%；本輪 OSAT 端先進封裝產能 2027 年底預估大增，新增折舊大量進場，管理層也承認近期成長受限於產能而非需求。","ruling":"不可調和（方向相反）。估值採 B 側：終端倍數用 18 倍，Bear 機率 30%；依據是毛利改善有相當部分來自稼動率與供不應求，這部分在下行時會回吐，管理層的結構區間至今只經過上行期。","evidence_level":"管理層指引＋歷史年報＋法人產能估計","settle_metric":"2027 年四季封測毛利率與混合稼動率","if_then":["若 4Q26 封測毛利率 ≥30%，且 2027 年稼動率回落到 80% 以下時毛利率仍 ≥28%，則 Base 終端倍數上調到 21 倍重算，股價 ≤600 元時建立 2% 首倉","反向：若封測毛利率連兩季 <26%，則維持不碰、Bear 機率升到 40%，已持有者減碼一半"],"evidence_refs":["cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#1","cyclical_supply_discipline_capacity#3","end_markets#0"]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"報導稱第三季營收優於指引，2027 年 LEAP 倍增有產能與客戶能見度，毛利率可能再上修；按 2027 共識只要 23 倍，RSI 46 不過熱，法人目標價最高 835 元。","side_b":"670 元已在法人目標價區間下緣附近；前瞻一年 35.6 倍、尖峰獲利 23 倍；自由現金流為負、淨負債上升；26 週已漲 46.5%。","ruling":"可調和（程度差異）：生意變好是真的，但價格已先反映 2027 年；不追，等價格或毛利證據擇一先到。","evidence_level":"二手報導＋法人報告摘要＋事實表估值","settle_metric":"股價對 2027 共識 EPS 倍數、4Q26 封測毛利率","if_then":["若股價續漲而 2027 LEAP 指引與毛利率證據未上修，則不追","若股價跌到 500 元以下而封測毛利率仍 ≥27%、LEAP 指引未下修，則重跑研究後分批反買"],"evidence_refs":["cyclical_inventory_price_position#1","capital_markets_pricing#0","capital_markets_pricing#2"]},{"axis":"管理層前後說法對照","cause":null,"prior_field":null,"side_a":"2026-04-29 財務長：一般業務成長約 13%、暫不調結構毛利區間要等明年；折舊對毛利的稀釋下季可能量化；不排除再上調資本支出。","side_b":"2026-07-30：一般業務上修到約 20%，第四季就要檢討上調結構區間，資本支出再加 20 億美元到 105 億美元；折舊稀釋仍未量化，2027 年資本支出規模拒答。","ruling":"可調和：營運數字兌現且優於前一季說法，可信度加分；但折舊量化承諾未兌現、2027 年資本支出不答，資本強度這一面透明度不足，列入觀察。","evidence_level":"兩場法說逐字稿","settle_metric":"下次法說是否揭露折舊占營收比與 2027 年資本支出範圍","if_then":["若 4Q26 法說仍不給 2027 年資本支出範圍且資本支出再上修，則把 H3 視為削弱，倉位上限維持 3%"],"evidence_refs":[]},{"axis":"合併營收成長品質","cause":null,"prior_field":null,"side_a":"第三季合併營收指引季增 21%～22%。","side_b":"其中 EMS 季增約 40%，財務長說主要是記憶體零件漲價轉嫁，扣除後是正常季節性，EMS 營業利益率約 3.7%～3.8%。","ruling":"可調和：判斷成長改看封測營收（季增 11%～13%）與營業利益，不用合併營收。","evidence_level":"2Q26 法說逐字稿","settle_metric":"封測營收季增率","if_then":["若封測營收季增率連兩季低於 5% 而合併營收仍高成長，則視為成長品質惡化，H2 削弱"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"4Q26 封測毛利率是否突破 30%","type":"假設驗證","maps_to":"H1","metric":"封測（ATM）毛利率","threshold":"4Q26 ≥29.5%","action":"達標則上調 Base 終端倍數重算；未達標維持觀望","source_freq":"公司季度法說／每季","date":"2027-02","evidence_refs":["end_markets#0"]},{"n":2,"text":"2027 年 LEAP 倍增指引是否維持","type":"假設驗證","maps_to":"H2","metric":"LEAP 營收指引與實際","threshold":"2027 年約 70 億美元以上","action":"下修到成長五成以下即走唯一致命點流程","source_freq":"公司季度法說／每季","date":"2027-02","evidence_refs":["supply_demand_durability#3"]},{"n":3,"text":"資本支出高峰後自由現金流是否轉正","type":"假設驗證","maps_to":"H3","metric":"全年自由現金流與淨負債÷權益","threshold":"2028 年自由現金流 >0 且淨負債÷權益 ≤60%","action":"未達標則倉位上限維持 3%","source_freq":"年報／每年","date":"2029-03","evidence_refs":[]},{"n":4,"text":"產能大增後稼動率跌破下行門檻","type":"風險","maps_to":"R1","metric":"混合稼動率","threshold":"<75%","action":"已持有者減碼一半","source_freq":"法說管理層口述／每季","date":null,"evidence_refs":["cyclical_supply_discipline_capacity#3","cyclical_prior_downcycle_behavior#0"]},{"n":5,"text":"競爭對手與在地化分走主要客戶訂單","type":"風險","maps_to":"R2","metric":"前五大客戶營收占比","threshold":"單季下降 ≥3 個百分點且管理層未說明","action":"減碼一半並重跑研究","source_freq":"季報新聞稿／每季","date":null,"evidence_refs":["competitive_share_entrants#3","geo_supply_chain#2","reg_tariff_export#0"]},{"n":6,"text":"公司明確下修 2027 年 LEAP 倍增指引","type":"Single Thing","maps_to":"single_thing","metric":"2027 年 LEAP 營收指引","threshold":"由倍增下修到成長五成以下","action":"已持有者清倉；未持有者不碰","source_freq":"公司季度法說／每季","date":null,"evidence_refs":["supply_demand_durability#3"]},{"n":7,"text":"價格回到合理區且毛利未破","type":"估值rearm","maps_to":null,"metric":"股價與封測毛利率","threshold":"股價 ≤500 元且封測毛利率 ≥27%","action":"重跑研究後考慮 2% 首倉","source_freq":"每日股價＋每季法說","date":null,"evidence_refs":[]},{"n":8,"text":"股價跑到 2027 共識 EPS 30 倍以上而獲利未上修","type":"減碼","maps_to":null,"metric":"股價÷2027 共識 EPS","threshold":"≥30 倍（約 880 元）","action":"已持有者減碼一半","source_freq":"每日股價","date":null,"evidence_refs":[]},{"n":9,"text":"4Q26 法說後全面複審","type":"複審日期","maps_to":null,"metric":"結構毛利區間、2027 年資本支出、LEAP 指引","threshold":null,"action":"重跑研究","source_freq":"一次","date":"2027-02-15","evidence_refs":[]}],"kill_metrics":[{"metric":"封測（ATM）毛利率","bear_threshold":"連兩季低於 25%","window":"2027～2028 年","source":"公司季度法說簡報","last_status":"ok"},{"metric":"合併月營收年增率","bear_threshold":"連三個月轉負","window":"每月公告","source":"公開資訊觀測站月營收","last_status":"ok"},{"metric":"混合產能稼動率","bear_threshold":"低於 75%","window":"每季","source":"法說會管理層口述","last_status":"ok"},{"metric":"淨負債÷權益","bear_threshold":"高於 80%","window":"每季","source":"季報資產負債表","last_status":"ok"},{"metric":"2027 年 LEAP 營收指引","bear_threshold":"由倍增下修到成長五成以下","window":"2027 年各季法說","source":"公司季度法說","last_status":"unknown"}],"evidence_dismissed":[{"ref":"substitute_technology#2","reason":"搜尋摘要無法對應到單一來源網址，屬未具名線索，且同一摘要自述英特爾基板良率偏低、短期實質影響有限；英特爾一條龍的威脅已由具名來源的同業條目處理，不重複計入。"}],"action_conditions":{"rearm_trigger":"股價≤500 元（約 2027 共識 EPS 17 倍）且封測毛利率仍≥27%、LEAP 倍增指引未下修","exec_line":"現價不建倉。觸發價格條件後重跑研究，再考慮 2% 首倉；已持有者不加碼，封測毛利率連兩季低於 25% 或稼動率跌破 75% 減碼一半，LEAP 倍增指引明確下修則清倉。","holding_cap":"3%"}},"decision_inputs":{"signal":"B","ma":"✅","cycle_position":"中循環","cycle_verdict":"等回踩","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":false,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等股價回到約 500 元以下（約 2027 共識 EPS 17 倍），且封測毛利率仍 ≥27%、2027 年 LEAP 倍增指引未下修"},"thesis":{"H":[{"id":"H1","text":"AI 先進封裝帶動封測毛利率突破過去 26%～30% 的結構區間，並在 2027 年守住。","2y":"4Q26 封測毛利率 ≥29.5%，2027 年四季平均 ≥28%","5y":null,"10y":null,"threshold":"2027 年封測毛利率四季平均 ≥28%","source":"公司季度法說簡報封測損益頁","drift_rule":"實際值連兩季低於門檻 5% 以上（約 26.6%）＝削弱；連三季低於 10% 以上（約 25.2%）＝反轉"},{"id":"H2","text":"2027 年 LEAP 營收倍增，新廠與設備如期開出。","2y":"2027 年 LEAP 營收約 70 億美元以上（以 2026 年超過 35 億美元為基）","5y":null,"10y":null,"threshold":"2027 年 LEAP 營收 ≥70 億美元","source":"公司季度法說指引與年度實際","drift_rule":"季度進度連兩季落後倍增路徑 5% 以上＝削弱；連三季落後 10% 以上或指引下修＝反轉"},{"id":"H3","text":"資本支出高峰過後，新產能報酬足以讓自由現金流轉正、投入資本報酬率維持在 10% 以上。","2y":null,"5y":"2028 年全年自由現金流轉正，淨負債÷權益 ≤60%，投入資本報酬率 ≥10%","10y":null,"threshold":"2028 年自由現金流 >0 且淨負債÷權益 ≤60%","source":"年報現金流量表與季報資產負債表","drift_rule":"淨負債÷權益連四季高於路徑 5% 以上＝削弱；連六季高於 10% 以上＝反轉"}],"R":[{"id":"R1","text":"2028 年起 OSAT 端先進封裝產能大增，若碰上 AI 資本支出消化，稼動率與毛利率重演 2023 年下行，且折舊基數更大。","h_ref":"H1","clock":"🔥","threshold":"混合稼動率 <75% 或封測毛利率連兩季 <25%","evidence_refs":["cyclical_supply_discipline_capacity#3","cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#1"]},{"id":"R2","text":"Amkor 取得 NVIDIA 美國多年期合作、Intel EMIB 積壓訂單增加，而公司採台灣優先；客戶在地化與關稅分攤可能分走新增訂單或壓低傳統封測價格。","h_ref":"H2","clock":"🔥","threshold":"前五大客戶占比單季下降 ≥3 個百分點，或 2027 年 LEAP 指引下修","evidence_refs":["competitive_share_entrants#3","geo_supply_chain#2","reg_tariff_export#0"]},{"id":"R3","text":"資本強度失控：資本支出再上修、自由現金流負值延長，淨負債持續累積。","h_ref":"H3","clock":"🐢","threshold":"淨負債÷權益 >80%","evidence_refs":[]},{"id":"R4","text":"關鍵材料由少數供應商主導、替代產能有限，任一斷供即無法出貨。","h_ref":"H2","clock":"⚡","threshold":"單季營收因材料短缺低於指引下緣","evidence_refs":["geo_supply_chain#3"]}],"single_thing":{"description":"主要晶圓代工夥伴或最大 AI 客戶削減委外，公司明確下修 2027 年 LEAP 倍增指引。","why_fatal":"2026 年 105 億美元資本支出中約七成設備投向 LEAP；倍增落空時新增折舊落在空產能上，封測毛利率回到 24%～26%，2027 年 EPS 由共識 29 元降到約 22 元，同時倍數收縮，是 Base 終端 EPS 最大的單一敏感項。","if_happens":"已持有者清倉；未持有者不碰，等稼動率回到 80% 以上再重跑研究。","how_monitor":"每季法說的 LEAP 指引、主要晶圓代工夥伴對委外的說法、月營收年增率。","probability":"約 20%：管理層稱需求不是問題、限制在執行，但 2028 年 OSAT 端產能預估大增，客戶自做與替代技術也在推進。"}},"appendix_a":{"growth_durability":6,"quality_score":6,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":22.93,"peg_fy2":0.42,"stress":{"pass":8,"total":10}},"eps_meta":{"base_eps_path":{"FY2025A":8.89,"FY2026E":18.83,"FY2027E":29.22,"FY2028E":null},"fy_end_month":12,"eps_basis":"基期為年報稀釋 EPS；共識為 yfinance 分析師平均，未註明基本或稀釋；FY2028E 事實表未涵蓋"},"catalysts":[{"date":"2026-10","date_precision":"month","type":"guidance","event":"3Q26 正式法說與第四季指引（報導稱第三季營收已優於指引，待原文確認）","impact":"高","watch":"第四季封測毛利率指引是否接近 30%"},{"date":"2026-12","date_precision":"month","type":"product","event":"CPO 初期小量生產","impact":"中","watch":"頻寬、散熱與良率的初步數據"},{"date":"2027-02","date_precision":"month","type":"guidance","event":"4Q26 法說：結構毛利區間是否上調、2027 年資本支出與 LEAP 指引","impact":"高","watch":"資本支出規模與 LEAP 倍增是否維持"},{"date":"2027-03","date_precision":"quarter","type":"capacity","event":"310×310 面板級封裝全自動線量產","impact":"中","watch":"客戶採用與良率"}],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8(val爭議)","pacing":[],"holding_cap":"中期 2-5 年","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='↑', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='✅'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":true,"basis":"capalloc_grade='C'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟠', moat_trend='↑', week26=46.51, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='循環/商品', cycle_position='中循環', moat='B', moat_trend='↑', cycle_gates_pass=False"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈機械讀數判定不可用，baseline rows 8/9/9b/10 的估值條件視為不可判 → 落 row8 觀望（保守方向）","hit":true,"basis":"val_denominator_disputed=True, val(機械讀數)='🟠'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"requires_critic":[]}}
```

---

## 尾段：回覆格式

只回一個 JSON 陣列，①–⑧ 每條一個元素，八個全出，不得跳號、不得多列，陣列外不得有任何文字（不加前言、不加 markdown 圍欄、不加附註）：

```json
[{"item": "①", "light": "🔴|🟡|🟢", "judgment_path": "$.路徑", "reason": "一句話"}]
```
