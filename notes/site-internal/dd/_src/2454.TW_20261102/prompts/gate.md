你是 DD 管線 v20 的判斷層閘（gate），標的 2454.TW（20261102）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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
- `f_kpi0_gaap_tifrs`（q1_business）｜營收（GAAP/TIFRS）＝168058 NT$百萬｜期間與口徑：3Q26（季末 2026-09-30，公告於 2026-10-30）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：聯發科 IR 新聞稿 3Q26 Press Release（https://www.mediatek.com/hubfs/MediaTek-Assets/Pdfs/Quarterly%20Earnings%20Release/2026/Quarterly%20Earnings%20Release-2026Q3/Press%20Release.pdf）（numbers.latest_quarter_kpis.items[0]，as_of 3Q26（季末 2026-09-30，公告於 2026-10-30））
  - 註記：查無（IR 新聞稿不含共識；未另查證）
- `f_kpi1_gaap`（q1_business）｜毛利率（GAAP）＝46.3 %｜期間與口徑：3Q26（季末 2026-09-30，公告於 2026-10-30）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：聯發科 IR 新聞稿 3Q26 Press Release（https://www.mediatek.com/hubfs/MediaTek-Assets/Pdfs/Quarterly%20Earnings%20Release/2026/Quarterly%20Earnings%20Release-2026Q3/Press%20Release.pdf）（numbers.latest_quarter_kpis.items[1]，as_of 3Q26（季末 2026-09-30，公告於 2026-10-30））
  - 註記：查無（IR 新聞稿不含共識；未另查證）
- `f_kpi3_gaap_tifrs`（q1_business）｜GAAP（TIFRS）營業利益／利益率＝27102 NT$百萬（利益率 16.1%）｜期間與口徑：3Q26（季末 2026-09-30，公告於 2026-10-30）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：聯發科 IR 新聞稿 3Q26 Press Release（https://www.mediatek.com/hubfs/MediaTek-Assets/Pdfs/Quarterly%20Earnings%20Release/2026/Quarterly%20Earnings%20Release-2026Q3/Press%20Release.pdf）（numbers.latest_quarter_kpis.items[3]，as_of 3Q26（季末 2026-09-30，公告於 2026-10-30））
  - 註記：查無（IR 新聞稿不含共識；未另查證）
- `f_kpi4_eps_tifrs`（q1_business）｜淨利／EPS（TIFRS，歸屬母公司）＝17.5 NT$／股（淨利 28,199 百萬，其中非營業收入 6,471 百萬占營收 3.9%）｜期間與口徑：3Q26（季末 2026-09-30，公告於 2026-10-30）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：聯發科 IR 新聞稿 3Q26 Press Release（https://www.mediatek.com/hubfs/MediaTek-Assets/Pdfs/Quarterly%20Earnings%20Release/2026/Quarterly%20Earnings%20Release-2026Q3/Press%20Release.pdf）（numbers.latest_quarter_kpis.items[4]，as_of 3Q26（季末 2026-09-30，公告於 2026-10-30））
  - 註記：查無（IR 新聞稿不含共識；未另查證）
- `f_kpi9_4q26`（q1_business）｜管理層指引：4Q26 營收＝NT$210.1–221.8 十億（約 YoY +40–48%）；毛利率 45% ±1.5pp；2027 全年營業利益率目標約 20% 或略高 NT$｜期間與口徑：4Q26 指引（法說會 2026-10-30）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：二手來源（IR 新聞稿不含指引，指引在法說簡報／逐字稿）：MarketScreener、Investing.com、BigGo 摘要；採用前宜對照 IR 法說簡報（numbers.latest_quarter_kpis.items[9]，as_of 4Q26 指引（法說會 2026-10-30））
  - 註記：查無（IR 新聞稿不含共識；未另查證）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝678630.33 TWD m｜期間與口徑：2026-11-02／yfinance revenue_estimate 0y 平均（19 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-02）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝1199125.91 TWD m｜期間與口徑：2026-11-02／yfinance revenue_estimate +1y 平均（24 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-02）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_peer_2454_tw_gross_margin_pct`（q2_moat）｜2454.TW 毛利率＝46.28 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.2454.TW.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_2454_tw_operating_margin_pct`（q2_moat）｜2454.TW 營業利益率＝15.13 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.2454.TW.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_2454_tw_fcf_margin_pct`（q2_moat）｜2454.TW FCF 利潤率＝13.34 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.2454.TW.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_qcom_gross_margin_pct`（q2_moat）｜QCOM 毛利率＝54.23 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.QCOM.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_qcom_operating_margin_pct`（q2_moat）｜QCOM 營業利益率＝23.28 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.QCOM.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_avgo_gross_margin_pct`（q2_moat）｜AVGO 毛利率＝68.77 %｜期間與口徑：TTM ending 2026-07-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.AVGO.gross_margin_pct，as_of TTM ending 2026-07-31（4季加總））
- `f_peer_avgo_operating_margin_pct`（q2_moat）｜AVGO 營業利益率＝48.52 %｜期間與口徑：TTM ending 2026-07-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.AVGO.operating_margin_pct，as_of TTM ending 2026-07-31（4季加總））
- `f_peer_3661_tw_operating_margin_pct`（q2_moat）｜3661.TW 營業利益率＝24.0 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.3661.TW.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_3443_tw_gross_margin_pct`（q2_moat）｜3443.TW 毛利率＝23.95 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.3443.TW.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝71.0 TWD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；原為美元，已依快照日匯率換算為新台幣（twd (koyfin usd ×32.5669 @ 2026-10-31)）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-10-31）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝150.46 TWD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；原為美元，已依快照日匯率換算為新台幣（twd (koyfin usd ×32.5669 @ 2026-10-31)）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-10-31）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝285.29 TWD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；原為美元，已依快照日匯率換算為新台幣（twd (koyfin usd ×32.5669 @ 2026-10-31)）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-10-31）
- `f_kpi5_ocf`（q4_capital）｜營業活動現金流（OCF）＝-4256 NT$百萬｜期間與口徑：3Q26（季末 2026-09-30，公告於 2026-10-30）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：聯發科 IR 新聞稿 3Q26 Press Release（https://www.mediatek.com/hubfs/MediaTek-Assets/Pdfs/Quarterly%20Earnings%20Release/2026/Quarterly%20Earnings%20Release-2026Q3/Press%20Release.pdf）（現金流量摘要）。單季資本支出新聞稿未揭露（財報 PDF 僅有前九個月累計，PP&E 21,846 百萬），故單季 FCF 不推算（numbers.latest_quarter_kpis.items[5]，as_of 3Q26（季末 2026-09-30，公告於 2026-10-30））
  - 註記：查無（IR 新聞稿不含共識；未另查證）
- `f_kpi6_sbc`（q4_capital）｜SBC 占營業利益＝2.89 %（783 ÷ GAAP 營業利益 27,102；占營收 0.47%）｜期間與口徑：3Q26（季末 2026-09-30，公告於 2026-10-30）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：聯發科 IR 新聞稿 3Q26 Press Release（https://www.mediatek.com/hubfs/MediaTek-Assets/Pdfs/Quarterly%20Earnings%20Release/2026/Quarterly%20Earnings%20Release-2026Q3/Press%20Release.pdf）（Non-TIFRS 調節表 SBC 783 百萬）；占比為自行換算（numbers.latest_quarter_kpis.items[6]，as_of 3Q26（季末 2026-09-30，公告於 2026-10-30））
  - 註記：n/a
- `f_kpi7_archetype`（q1_business）｜存貨週轉天數（硬體 archetype）＝127 天｜期間與口徑：3Q26（季末 2026-09-30，公告於 2026-10-30）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：聯發科 IR 新聞稿 3Q26 Press Release（https://www.mediatek.com/hubfs/MediaTek-Assets/Pdfs/Quarterly%20Earnings%20Release/2026/Quarterly%20Earnings%20Release-2026Q3/Press%20Release.pdf）；期末存貨 153,531 百萬（numbers.latest_quarter_kpis.items[7]，as_of 3Q26（季末 2026-09-30，公告於 2026-10-30））
  - 註記：n/a
- `f_kpi8`（q1_business）｜現金及流動金融資產＝278320 NT$百萬｜期間與口徑：3Q26（季末 2026-09-30，公告於 2026-10-30）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：聯發科 IR 新聞稿 3Q26 Press Release（https://www.mediatek.com/hubfs/MediaTek-Assets/Pdfs/Quarterly%20Earnings%20Release/2026/Quarterly%20Earnings%20Release-2026Q3/Press%20Release.pdf）（numbers.latest_quarter_kpis.items[8]，as_of 3Q26（季末 2026-09-30，公告於 2026-10-30））
  - 註記：n/a
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝-236369.99 TWD m｜期間與口徑：2026-11-02／yfinance 最新一季：總債務 41950.0、現金 278319.99（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-02）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝1.367 %｜期間與口徑：2026-11-02／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-11-02）
- `f_ev_m`（q5_valuation）｜目前企業價值 EV（市值＋淨負債）＝6016393.56 TWD m｜期間與口徑：2026-11-02／市值 6252763.55 ＋ 淨負債 -236369.99｜kind：realized
  - 來源：—（numbers.capital_structure.ev_m，as_of 2026-11-02）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝3915.0 TWD｜期間與口徑：2026-10-30（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-10-30（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝55.14 x｜期間與口徑：2026-10-31／分母＝FY1 EPS 71.0，分子＝快照價 3915.0｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-10-31）
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝64.65 x｜期間與口徑：2026-10-30（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-10-30（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝100.0 %｜期間與口徑：2026-10-30（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-10-30（RTH 收盤，UTC））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝10.09 x｜期間與口徑：2026-10-30（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-10-30（RTH 收盤，UTC））
- `f_ev_s_fwd`（q5_valuation）｜EV/S（EV ÷ FY1 共識營收）＝8.87 x｜期間與口徑：2026-11-02／f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）｜kind：estimate
  - 來源：—（numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m，as_of 2026-11-02）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝6.03 %｜期間與口徑：2026-07-30 → 2026-10-31／FY1 共識 EPS 66.96 → 71.0（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-10-31）
- `f_consensus_rev_fy2_pct`（q5_valuation）｜FY2 共識修正＝0.66 %｜期間與口徑：2026-10-31／兩份 Koyfin 快照之間的 EPS 修正幅度（149.48 → 150.46）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.fy2.revision_pct，as_of 2026-10-31）
- `f_ma_w104`（q5_valuation）｜104 週均線＝2094.86 TWD｜期間與口徑：2026-11-02／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-02）
- `f_ma_w250`（q5_valuation）｜250 週均線＝1316.5 TWD｜期間與口徑：2026-11-02／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-02）
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝50.9 %｜期間與口徑：2026-10-30（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^TWII｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-10-30（RTH 收盤，UTC））

### findings_digest 中方向為負或來源衝突的條目（12 條）
- `competitive_share_entrants#0`（competitive_share_entrants｜方向 -｜狀態 ok）：Counterpoint：2026Q1 全球智慧手機 SoC 聯發科市占 32%（去年同期 38%），高通 23%（27%），蘋果 19%（15%），紫光展銳 14%（10%），三星 7%（5%）；聯發科仍第一但份額下滑，搶份額者為蘋果、紫光展銳、三星
  - 來源：工商時報 2026-06-12／malaysianwireless（Counterpoint Q1 2026）（as_of 2026-06-12）｜affects：moat_trend、thesis.R
- `competitive_share_entrants#1`（competitive_share_entrants｜方向 -｜狀態 ok）：2026-06 高通宣布與 Meta 策略性多世代合作進軍 AI ASIC，聯發科盤中股價一度跌停；聯發科稱目標搶攻 10%～15% 市占（以 2027 年 700～800 億美元潛在市場估算）
  - 來源：自由時報 對手高通搶進AI ASIC市場! 聯發科「嚇」跌摜至跌停（as_of 2026-06-26）｜affects：moat_trend、thesis.R、decision_inputs.bear
- `competitive_share_entrants#2`（competitive_share_entrants｜方向 -｜狀態 ok）：市場傳 Marvell 可能成為 Google 第三家 ASIC 夥伴，對博通與聯發科形成競爭疑慮；法人稱聯發科已取得 Google 下一代 ASIC 訂單、地位穩固，KGI 認為疑慮被過度放大
  - 來源：工商時報 2026-04-26／KGI 報告 2026-04-21（as_of 2026-04-26）｜affects：moat_trend、thesis.R
- `competitive_share_entrants#3`（competitive_share_entrants｜方向 -｜狀態 ok）：亞系券商指出聯發科中低階市場報價與市占承壓，紫光展銳在 4G、高通在 5G 競爭激烈，預期 2026 年 5G SoC 平均售價年減約 10%（發布日期搜尋結果未明確，as_of 為估計）
  - 來源：經濟日報（as_of 2026-01-01）｜affects：moat_trend、valuation
- `customer_second_source#0`（customer_second_source｜方向 -｜狀態 ok）：2026年9月底傳聞 Google 新一代 TPU 供應鏈有變數，TPU v9 可能由邁威爾（Marvell）分食訂單、v8 樣品可能延至2027年Q2；聯發科股價一度重挫逾7%（媒體傳聞，未經公司證實）。
  - 來源：ETtoday 財經／搜尋結果摘要：聯發科發了!搶到Google「TPU大單」 博通重挫12%（同批結果另有 Google TPU 訂單疑慮報導）（as_of 2026-09-30）｜affects：thesis.R、decision_inputs.bear、triggers
- `supply_demand_durability#2`（supply_demand_durability｜方向 -｜狀態 ok）：記憶體缺貨：聯發科高層傳出拜會三星與SK海力士爭取產能，手機業務占比高受影響較大（媒體傳聞，公司未回應）
  - 來源：technews 搜尋摘要（as_of 2026-01-27）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#1`（reg_tariff_export｜方向 -｜狀態 ok）：2018年聯發科曾因國貿局公文要求出口前申請許可而暫停對中興出貨，後取得許可恢復；2025年6月經濟部擴充出口管制實體名單（新增華為、中芯等），搜尋結果未顯示聯發科本身被列入（搜尋摘要轉述，未核原文）
  - 來源：techbang／technews 報導（2018中興案）；worldecr 2025-06 名單擴充（as_of 2018-05-04）｜affects：decision_inputs.bear、triggers
- `end_markets#0`（end_markets｜方向 -｜狀態 ok）：2026Q3 手機營收占比37%，季減1%、年減17%
  - 來源：TechNews 聯發科Q3 EPS 17.5元、毛利率46.3%（as_of 2026-10-30）｜affects：moat_trend、valuation
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：大摩報告提到聯發科 3 奈米 TPU 尚未完成所有工程驗證測試，TPU 出貨量與 T-Glass/基板供應高度相關（搜尋摘要轉述，未讀原頁）
  - 來源：中時 wantrich：大摩、富邦投顧看好聯發科2027年（搜尋摘要）（as_of 2026-01-27）｜affects：thesis.R、decision_inputs.bear
- `substitute_technology#1`（substitute_technology｜方向 -｜狀態 ok）：外資指受記憶體成本上升影響，2026 全球智慧機晶片出貨預估年減約 7%，中國 Android 手機 SoC 2026Q1 出貨可能季減 10%～20%（搜尋摘要轉述）
  - 來源：technews.tw 大摩看好聯發科 AI ASIC（搜尋摘要）（as_of 2026-01-26）｜affects：thesis.R、decision_inputs.bear
- `substitute_technology#2`（substitute_technology｜方向 -｜狀態 ok）：報導：摩根士丹利與高盛示警聯發科毛利率面臨結構性下修風險（台積電先進製程漲價、車用與 AI ASIC 初期毛利低）
  - 來源：經濟日報 聯發科靠ASIC翻轉景氣循環宿命（as_of 2026-09-23）｜affects：valuation、decision_inputs.bear
- `major_events#1`（major_events｜方向 -｜狀態 ok）：2026年5月上旬聯發科被列為處置股（分盤交易），金管會表示將督導交易所檢討注意股制度並評估縮短處置期間；屬交易制度事件，非公司財報或裁罰。
  - 來源：經濟日報／聯合理財網 避免聯發科變處置股重演 金管會將縮短處置時間（as_of 2026-06-10）｜affects：valuation、triggers

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 6 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/2454.TW_20261102/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":10560,"bear_5y_price":1755,"p_bull_pct":25,"p_bear_pct":30,"upside_5y_pct":44.8,"ev5y_pct":46.1,"irr_base_pct":7.7,"asym_ratio":2.6,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":71.0,"pe":55.14,"basis":"起點為 2026 年共識 EPS 71.0 元（只剩第四季），現價 3,915 元對應 55.1 倍；終端倍數同樣套在 2031 年度 EPS 上，同為當年度口徑"},"eps":{"bull":[160,300,370,430,480],"base":[145,240,270,295,315],"bear":[125,135,120,125,135]},"pe":{"bull":22,"base":18,"bear":13},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":1.367,"net_buyback":-0.4},"second_stage":{"bull_cagr_pct":12,"base_cagr_pct":7},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### 2454.TW_Q2_2026_Earnings_Call_20260731.md
- 2026-07-31｜CEO｜guidance：Q3 營收財測區間（匯率 32）（原話："in the range of TWD 152.2 billion to TWD 159.8 billion"）
- 2026-07-31｜CEO｜guidance：Q3 毛利率財測 46% ±1.5pp（原話："Gross margin is forecasted at 46% plus or minus 1.5"）
- 2026-07-31｜CEO｜guidance：全年營收目標改為區間高標（原話："achieve the high end of our full year revenue target range"）
- 2026-07-31｜CEO｜guidance：全年毛利率落在當季財測區間內（原話："we aim to deliver our full year gross"）
- 2026-07-31｜CEO｜guidance：Q3 手機營收預期（原話："flat to decline mid-single-digit percentages sequentially"）
- 2026-07-31｜CEO｜guidance：Q3 Smart Edge 營收預期（原話："Smart Edge Platforms revenue to grow mid- to high"）
- 2026-07-31｜CEO｜guidance：Q3 Power IC 營收預期（原話："Power IC revenue to be flattish sequentially"）
- 2026-07-31｜CEO｜guidance：資料中心 2026 營收預期（原話："data center revenue to exceed $2 billion in 2026"）
- 2026-07-31｜CEO｜guidance：2027 SAM 估計與市占目標上調（原話："we now believe the 2027 SAM to be USD 80 billion"）
- 2026-07-31｜CEO｜guidance：全年智慧手機出貨預期不變（原話："expect the market to decline by about 15% in units this year"）
- 2026-07-31｜CFO｜margin：Q2 毛利率年減原因：去年同期一次性利益（原話："mainly due to a one-time benefit in the year-ago quarter"）
- 2026-07-31｜CEO｜margin：Q2 營收超出財測高標（原話："exceeding the high end of our guidance range"）
- 2026-07-31｜CFO｜margin：漲價目的是轉嫁成本（原話："not trying to actually increase the price to increase"）
- 2026-07-31｜CFO｜margin：毛利率目標為維持而非提高（原話："trying to maintain the gross margin rather than increase the"）
- 2026-07-31｜CFO｜margin：ASIC 各世代毛利率相近（原話："the gross margin generation after generation will be similar"）
- 2026-07-31｜CFO｜margin：ASIC 毛利率對公司平均略稀釋（原話："will be slightly dilutive compared to the current corporate"）
- 2026-07-31｜CFO｜margin：營業利益率規模化後增益（原話："once we start to scale, I think it will be accretive"）
- 2026-07-31｜CFO｜margin：費用金額小幅增加、費用率大降（原話："It will increase slightly. But the ratio will come down"）
- 2026-07-31｜CEO｜margin：費用金額成長但費用率下降（原話："It will grow higher, but the ratio will come down."）
- 2026-07-31｜CEO｜commitment：第二顆 ASIC 2028 年量產（原話："the yield and reliability of the second ASIC are on track"）
- 2026-07-31｜CEO｜commitment：第二顆 ASIC 約 2028 年初量產（原話："you can assume early 2028 for early production"）
- 2026-07-31｜CEO｜commitment：第一顆 ASIC 2026 Q4 量產（原話："scheduled to begin in the fourth quarter of this year"）
- 2026-07-31｜CEO｜commitment：2028 SAM 尚未給數字但稱會更高（原話："our 2028 SAM will be quite a bit higher than 2027"）
- 2026-07-31｜CEO｜commitment：2028 營收區間尚未指引（原話："while we are not ready today to guide the 2028 revenue range"）
- 2026-07-31｜CEO｜commitment：448G SerDes 預計明年下半年就緒（原話："next year, maybe second half of next year"）
- 2026-07-31｜CFO｜commitment：營業利益率增益僅給方向（原話："we probably only provide the directional guidance"）
- 2026-07-31｜CFO｜commitment：供應鏈對今明年營收目標有信心（原話："for next year, I think we feel very comfortable"）
- 2026-07-31｜CEO｜commitment：2nm 旗艦 SoC 第三季推出（原話："we will launch our 2-nanometer SoC in the third quarter"）
- 2026-07-31｜CEO｜capital_allocation：董事會核准 50 億美元融資額度（原話："approved a discretionary USD 5 billion financing budget"）
- 2026-07-31｜CFO｜capital_allocation：CFO 說明為備用彈性（原話："really just optionality, a flexing plan"）
- 2026-07-31｜CFO｜capital_allocation：帳上現金 70 億美元以上（原話："ample cash, $7 billion plus on our balance"）
- 2026-07-31｜CFO｜capital_allocation：確認可用於支持供應商擴產（原話："Yes, yes."）
- 2026-07-31｜CEO｜product：SAM 僅含加速器（原話："Right now, it's accelerator only for now."）
- 2026-07-31｜CEO｜product：SAM 不含 HBM（原話："And no HBM."）
- 2026-07-31｜CEO｜product：與 NVIDIA 合作 RTX Spark（原話："collaboration with NVIDIA on RTX Spark"）
- 2026-07-31｜CEO｜product：子系統整合 NVLink Fusion（原話："incorporating NVLink Fusion connectivity onto the subsystem"）
- 2026-07-31｜CEO｜product：由 IP 供應走向機櫃式整合（原話："moving to not only provide very competitive IPs"）
- 2026-07-31｜CFO｜product：CFO 稱 448G 之後需走光學（原話："for beyond that, most likely we need to go on the optical"）
- 2026-07-31｜CFO｜competition：HBM 仍是主流（回應 LPDDR 替代路線）（原話："I think HBM is still a must"）
- 2026-07-31｜CFO｜competition：超大型客戶要求高效能（原話："hyperscalers who actually require absolutely"）
- 2026-07-31｜CEO｜competition：稱目標為優於公平份額（原話："we will get our hopefully, better than"）
- 2026-07-31｜CEO｜risk：封裝技術具高度挑戰（原話："those technologies are very challenging, we all understand"）
- 2026-07-31｜CEO｜risk：手機需求弱因 BOM 成本上升（原話："weak demand as a result of increasing smartphone BOM costs"）
- 2026-07-31｜CEO｜risk：EMIB-T 良率進展獲確認（原話："Yes, in short, yes, you can."）
- 2026-07-31｜CFO｜risk：封裝交期良率準時交付（原話："we're going to deliver this on time"）
- 2026-07-31｜CEO｜risk：邊緣裝置形態未定（原話："the jury definitely is out, still out"）
- 2026-07-31｜CEO｜customer：深化多家資料中心 ASIC 客戶接觸（原話："deepen our engagement with several customers"）
- 2026-07-31｜CEO｜customer：Smart Edge 季增含 TV SoC 的 DRAM 內容（原話："contribution from DRAM content in TV SoC"）
- 2026-07-31｜CEO｜customer：漲價行動反映供應鏈成本（原話："we are taking pricing actions to ensure these increases are"）
- 2026-07-31｜CFO｜customer：不揭露第三代專案（原話："third generation, actually, we won't be able"）
- 2026-07-31｜CEO｜customer：不揭露新技術會用於哪個客戶（原話："I'm afraid we cannot disclose those details."）

### 問答異常語氣（迴避／改口／保留）
- 2454.TW_Q2_2026_Earnings_Call_20260731.md｜問：JPMorgan：第二顆 ASIC 與 2028 SAM/市占，是否可能成為該客戶多數供應商｜答法：CEO 拒絕正面回答是否成為多數來源，改談專注執行與『better than fair share』
- 2454.TW_Q2_2026_Earnings_Call_20260731.md｜問：BofA：資料中心洽談客戶是否含 Tier 2 與企業客戶｜答法：CFO 稱無法提供細節，待可揭露時再說
- 2454.TW_Q2_2026_Earnings_Call_20260731.md｜問：KGI：三大事業群漲價幅度排序｜答法：CFO 表示無法評論，僅稱各事業群大致公平
- 2454.TW_Q2_2026_Earnings_Call_20260731.md｜問：Morgan Stanley：第三代專案是否回 TSMC CoWoS／大光罩｜答法：CFO 稱無法評論第三代，轉談前兩個專案
- 2454.TW_Q2_2026_Earnings_Call_20260731.md｜問：Goldman：營業利益率增益幅度｜答法：CFO 只給方向，不給數字，稱第三季後再說
- 2454.TW_Q2_2026_Earnings_Call_20260731.md｜問：Citi：新技術用於第二顆 ASIC 或其他客戶、明年市占／營收｜答法：CEO 稱無法揭露，明年市占未給數字，僅稱會滿足需求

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 4 | 4 |
| customer_second_source | found | 4 | 3 |
| customer_concentration_credit | found | 1 | 2 |
| supply_demand_durability | found | 4 | 2 |
| regulatory_antitrust | found | 3 | 3 |
| reg_tariff_export | found | 4 | 4 |
| geo_supply_chain | found | 2 | 3 |
| end_markets | found | 6 | 3 |
| substitute_technology | found | 3 | 3 |
| channel_business_model_shift | found | 4 | 3 |
| capital_markets_pricing | found | 3 | 4 |
| major_events | found | 2 | 4 |

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260711","verdict":"觀望","role":"追蹤","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"ASIC（雲端資料中心）成為第二成長引擎，且不嚴重稀釋整體毛利","columns":{"2Y 驗證點":"2026 Q4 ASIC 單季 ~$2B、2027 資料中心 ~$3.2B","5Y 驗證點":"雲端 ASIC 份額 10-15% 站穩、整體毛利率守 45%+","10Y 驗證點":"ASIC 成第二個 &gt;30% 營收支柱且回報 &gt; WACC","具體數字門檻":"ASIC 2027 營收 ≥ $3B 且合併 GP% ≥ 45%","來源":"公司 Q1 FY26 法說；TrendForce 2026-02；Digitimes 2026-04","漂移觸發":"連 2 季 TTM GP% 偏離 −5% → 削弱"}},{"id":"H2","text":"MediaTek 在 Google TPU 供應鏈的份額不被結構性稀釋","columns":{"2Y 驗證點":"TPU 8i/v7e 量產如期、v9 SerDes 訂單維持","5Y 驗證點":"推論變體 design win 延續到 v8/v9 世代","10Y 驗證點":"成為 Google 長期推論 ASIC 主力之一（非一次性設計費）","具體數字門檻":"2027-28 未出現第三家分食其推論變體份額","來源":"Digitimes 2026-06；TheNextWeb；SemiWiki","漂移觸發":"確認第三家分單 → 反轉"}},{"id":"H3","text":"手機核心業務不硬著陸，旗艦（Dimensity 9500）中國高階份額維持","columns":{"2Y 驗證點":"手機營收年降幅個位數、中國超高階份額 &gt;40%","5Y 驗證點":"手機提供穩定現金流資助 R&D，不拖累整體","10Y 驗證點":"手機成熟但不萎縮，作為 ASIC 的現金牛","具體數字門檻":"手機營收年 YoY 不低於 −10%、中國高階份額不跌破 35%","來源":"Counterpoint Q1 2026；Digitimes 2025-09","漂移觸發":"連 4 季手機營收 YoY &lt; −10% → 削弱"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"ASIC 毛利率稀釋整體獲利——為衝營收接低毛利客製案","columns":{"對應假設":"H1","時間尺度":"🔥 中期（4-6 季）","監測指標":"合併 GP% 趨勢、資料中心 blended 毛利","警戒閾值":"合併 GP% 連 2 季 &lt; 45%"}},{"id":"R2","text":"Google 多元化供應鏈，MediaTek 推論份額被第三家（Marvell）分食","columns":{"對應假設":"H2","時間尺度":"🔥 中期（4-6 季）","監測指標":"Google TPU 分單新聞、design win 世代延續性","警戒閾值":"確認第三家取得推論 TPU 分單"}},{"id":"R3","text":"中國高階手機需求走弱或補貼退場，旗艦 SoC 量價齊縮","columns":{"對應假設":"H3","時間尺度":"⚡ 短期（1-2 季）","監測指標":"中國超高階份額、Dimensity 9500 出貨、手機營收 YoY","警戒閾值":"連 2 季手機營收 YoY &lt; −15%"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"回檔至 FY27 30x（約 $3,150）或 ASIC 量產＋毛利率能見度兌現","irr_base_pct":8.0,"ev5y_pct":36.0,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"追蹤","signal":"B","val":"🔴","ma":"✅","trap":"🟢","moat_trend":"→","runway_post_y5":"🟢","asym_ratio":2.4,"ev5y_pct":36.0,"irr_base_pct":8.0,"max_dd_pct":-60.0,"bull_5y_price":8800,"bear_5y_price":2250,"p_bull_pct":25,"p_bear_pct":30,"rearm_trigger":"回檔至 FY27 30x（約 $3,150）或 ASIC 量產＋毛利率能見度兌現","price_at_dd":3925,"archetype":"品質複利成長","cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"2454.TW","date":"2026-11-02","schema":"v15.0","contract":"v19","company_name":"聯發科"},"oneliner":"聯發科 2027 年靠 Google 客製 AI 晶片讓獲利翻倍，現價約 2027 年預估 26 倍，算合理；真正的賭注是 2028 年第二代專案能否如期量產並守住主力供應，手機本業市占仍在流失。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/2454.TW_20261102/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/2454.TW_20261102/scenario.json","answers":{"q1_business":{"verdict":"賺手機品牌、平板／PC／車用品牌與 Google 的錢：手機與 Smart Edge 靠標準品晶片的出貨量與單價，2026 年第四季起 Google 客製 AI 晶片成為最大單一收入；錢卡在台積電先進製程、先進封裝與載板產能這一節點，聯發科分到的是整合與交付的報酬。","reasoning":"第三季營收 1,681 億元、年增 18%，毛利率 46.3%，GAAP 營業利益率 16.1%，EPS 17.5 元。營收組成：手機 37%（年減 17%）、Smart Edge 58%（年增 63%，含 9 月開始出貨的首顆 AI 加速器）、電源 IC 5%（年增 18%）。第四季營收指引 2,101～2,218 億元、毛利率 45% ±1.5pp、費用率 26%，隱含營業利益率約 19%；第四季 ASIC 約 25 億美元，占當季營收指引三成以上。單點依賴：2025 年前三大客戶合計 38.9%（最大 15.5%），2027 年 Google 專案目標約 160 億美元，約占 2027 年共識營收 1.2 兆元的四成，客戶結構由分散轉為單一客戶主導。議價：上游台積電、載板、HBM 都是瓶頸且在漲價，公司只做成本轉嫁；下游 Google 自有架構能力強，手機品牌逐機型雙供應。產業時鐘：資料中心處擴張期，手機處收縮期（公司預估 2026 年手機出貨年減約 15%），合併判為擴張，依據是第四季季增 25%～32% 由資料中心帶動，與股價無關。產業態勢判為雙向拉鋸：手機競爭惡化中（智慧手機 SoC 市占 38%→32%、5G 單價預估年減約一成），資料中心結構性轉好中（需求與載板、先進封裝瓶頸延續到 2027 年），其他結構變數中出口管制與關稅目前影響有限（美國營收約一成）。","fact_refs":["f_kpi0_gaap_tifrs","f_kpi1_gaap","f_kpi3_gaap_tifrs","f_kpi4_eps_tifrs","f_kpi9_4q26","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m"],"verdict_values":{"revenue_quality":"第三季營收超出財測高標；淨利 282 億元含非營業收入 64.7 億元（占營收 3.9%）；營業現金流 −42.6 億元、存貨 1,535 億元（127 天），本季獲利沒有轉成現金，屬放量前備料，需在第四季與 2027 年上半年回正。","unit_econ_note":"標準品晶片（手機、平板、PC、車用、電視）靠出貨量×單價；客製 AI 晶片單價高、毛利率低於公司平均，但手機累積的 IP 可重複利用、費用增幅小於營收，CFO 稱自第四季起營業利益率高於公司平均。","archetype":{"primary":"品質複利成長","secondary":"循環/商品","confidence":"中","fingerprint":"高研發密度的 IC 設計公司，IP 跨產品重複利用；同時帶手機景氣循環與單一雲端客戶專案的波動"},"industry":{"clock_phase":"II","sd_verdict_source":"週期性但中期持久：AI 加速器需求有雲端資本支出支撐，台積電稱供給短缺可能延續到 2027 年以後，公司稱 2026～2027 年 CoWoS 產能已確保、載板仍是瓶頸；但需求依附少數客戶的資本支出，2027 年後供給可逆性高，空頭機率不壓低。","bargaining":{"up":"台積電（12 奈米到 2 奈米與先進封裝的最重要夥伴）、載板、HBM 與記憶體供應商都是瓶頸且漲價，公司只能轉嫁成本；第二代改用美國 IDM 封裝分散依賴。","down":"手機品牌逐機型雙供應、議價強；Google 自有架構能力強，2027 年約占營收四成；2025 年前三大客戶合計 38.9%。","geo":"生產集中台灣、中國營收比重高；美國營收約一成，關稅影響有限；出口管制曾在 2018 年迫使暫停對中興出貨。"},"profit_pool_dir":"利潤池往資料中心與上游瓶頸環節（先進製程、封裝、載板、HBM）移動，手機 SoC 利潤池因出貨下滑與降價縮小；五年占比數字事實表未涵蓋。","tam_table":[{"item":"2027 年 AI 加速器 ASIC 可服務市場","value":"約 800 億美元，只含加速器、不含 HBM（CEO 2026-07-31）"},{"item":"公司 2027 年份額目標","value":"15%～20%，現瞄準高標約 160 億美元（CEO 2026-10-30）"},{"item":"2028 年可服務市場","value":"公司稱明顯高於 2027 年，未給數字"},{"item":"智慧手機 SoC 份額","value":"2026Q1 32%，去年同期 38%（Counterpoint）"},{"item":"2026 年智慧手機出貨","value":"公司預估年減約 15%"},{"item":"利潤池五年遷移","value":"事實表未涵蓋（各環節營業利益池占比無資料）"}]}}},"q2_moat":{"verdict":"護城河方向穩定：執行力在資料中心擴大，定價力在手機縮減，兩者相抵；等級 B。","reasoning":"機制：手機 SoC 累積的 CPU／GPU／NPU、通訊、低功耗與 SerDes 等 IP 可重複用在 Smart Edge 與資料中心，研發占營收 25.8%，高於高通 22.5% 與博通 13.3%，用規模攤提先進製程研發；資料中心再加上先進封裝、供應鏈調度與 NVLink Fusion 機櫃整合能力。可證方向：營業利益率對最強同業的差距，高通高 8.2 個百分點、博通高 33.4 個百分點，ROIC 差距事實表未涵蓋；自身營業利益率由 2022 年 23.1% 降到 2025 年 17.4%、TTM 15.1%，同業歷史序列事實表未涵蓋，無法判斷差距是否擴大。最大市場份額方向：智慧手機 SoC 市占 38%→32%，因此不給上升。執行力 8 分：連兩季超出財測、首顆 ASIC 如期出貨並把第四季目標由 20 億美元以上上調到 25 億美元、取得第二家客戶，前一季的財測與時程全數兌現。定價力 6 分：漲價只為轉嫁成本、資料中心毛利率低於平均、5G 單價預估年減約一成。三條威脅都是點對點競爭，沒有架構替代。","fact_refs":["f_peer_2454_tw_gross_margin_pct","f_peer_2454_tw_operating_margin_pct","f_peer_2454_tw_fcf_margin_pct","f_peer_qcom_gross_margin_pct","f_peer_qcom_operating_margin_pct","f_peer_avgo_gross_margin_pct","f_peer_avgo_operating_margin_pct","f_peer_3661_tw_operating_margin_pct","f_peer_3443_tw_gross_margin_pct"],"verdict_values":{"moat":{"mechanism":"研發規模＋IP 跨產品重複利用＋先進製程與封裝的整合交付能力","execution":8,"pricing":6,"grade":"B","trend":"→","trend_evidence":"執行力擴大：第三季營收連兩季超出財測高標、首顆 AI 加速器 9 月如期出貨並上調第四季目標、取得第二家客戶。定價力縮減：智慧手機 SoC 市占 38%→32%（Counterpoint 2026Q1）、中低階報價承壓、資料中心毛利率低於公司平均且漲價只轉嫁成本（CFO 2026-07-31）。兩者相抵判為穩定；手機份額下滑，不給上升。","competitor_notes":[{"name":"QCOM","strategy_note":"手機高階 5G 主要對手，2026-06 與 Meta 合作切入 AI ASIC；營業利益率高聯發科約 8 個百分點，手機與雲端兩線都碰得到。"},{"name":"AVGO","strategy_note":"雲端客製晶片龍頭、Google TPU 原主力，利潤率遠高於聯發科並能提供客戶融資，是第二代份額的主要對手。"},{"name":"3661.TW","strategy_note":"台系 ASIC 設計服務，營業利益率高但自由現金流為負，IP 廣度與供應鏈調度規模小於聯發科，競爭集中在中型專案。"},{"name":"3443.TW","strategy_note":"台積電體系設計服務，毛利率約 24%，偏接單設計，不是同層級對手。"},{"name":"Marvell","strategy_note":"傳為 Google 第三家 ASIC 夥伴、可能分食 TPU v9，不在同業對照表內，數字事實表未涵蓋。"}],"threats":[{"level":"🟡","text":"高通 2026-06 與 Meta 多世代合作切入 AI ASIC，在雲端客製晶片與聯發科正面競爭，並有手機 SoC 與資金規模撐腰。","p":30,"evidence_refs":["competitive_share_entrants#1"]},{"level":"🟡","text":"Google 分散供應：博通是原主力，Marvell 傳為第三家、TPU v9 可能分單；第二代改用美國 IDM 封裝，良率爬坡尚未經量產驗證。","p":35,"evidence_refs":["competitive_share_entrants#2","customer_second_source#0"]},{"level":"🟡","text":"手機本業份額流失：蘋果、紫光展銳、三星拿走份額，4G 由紫光展銳、5G 由高通壓價，5G SoC 單價預估年減約一成。","p":50,"evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#3"]}],"roic_durability":{"quadrant":"代理判斷為中等利益率×高周轉：TTM 營業利益率 15.1%，投入資本事實表未涵蓋；無晶圓廠、歷年自由現金流高於淨利，資產輕；2026 年第三季存貨升到 127 天，周轉正在下降。","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"雲端 ASIC 的使用者、決策者、付款者都在 Google 一家，需求急迫但依附單一客戶的資本支出；CEO 稱未來 1～3 年算力需求確定成長、增速會波動。手機端受記憶體漲價墊高 BOM，公司預估 2026 年手機出貨年減約 15%。需求基礎存在，持久性綁在雲端資本支出週期。"},{"item":"決策層級","level":"🟡","text":"替代性要在「每一代 TPU 由誰供應」這個決策單位看：同一代鎖定約 2～3 年，換代時 Google 可重新分配，博通是原主力、Marvell 傳為第三家；手機品牌逐機型雙供應。第二代已部分投片、2028 年第一季量產，代表 2028～2029 年份額大致已定；第三代（2029 年底）定義尚未完成，超過一代的鎖定未證。"},{"item":"價值鏈分配","level":"🔴","text":"價值鏈兩端都比聯發科強勢：上游台積電先進製程與 CoWoS、載板、HBM 都是瓶頸並持續漲價，下游是自己設計架構的單一大客戶。聯發科拿到的是整合與交付的報酬，資料中心毛利率低於公司平均，漲價只為轉嫁成本；毛利率 46.3% 低於高通 54.2%、博通 68.8%，分到的價值較少，營業利益率靠研發攤提拉高。"},{"item":"社會容忍度","level":"🟢","text":"產品是企業對企業的晶片，終端漲價不直接觸及消費者或監管定價，沒有社會價格天花板，也不依賴監管授權；政策風險在出口管制而非定價，已另列長期風險追蹤。"}],"roiic":"事實表未涵蓋（缺投入資本口徑，無法計算增量 ROIC）","reinvest_rate":"約 −30%（FY2025 代理值）","endo_ceiling":null,"formula_note":"內生成長率＝增量 ROIC × 再投資率。投入資本口徑事實表未涵蓋，增量 ROIC 無法計算。以（淨利−自由現金流）÷淨利作再投資率代理：FY2025 為（1,053−1,374）÷1,053≈−30%，FY2024 約 −26%，FY2023 約 −94%，FY2022 約 −6%，歷年皆為負，代表過去成長不靠資本再投資，而靠費用化的研發（占營收 25.8%）。資本口徑的內生上界接近零，對共識三年 EPS 年增約 63% 沒有解釋力，判為超出；2026 年第三季營業現金流轉負，再投資率正在轉正。"}}}},"q3_growth":{"verdict":"五年後跑道寬：資料中心客製晶片是有來源支持的第二條成長曲線，公司 2027 年份額約兩成、可服務市場仍在擴大；但跑道寬度綁在單一客戶的換代決策上。","reasoning":"成長來源以量為主、價為輔：2027 年共識營收約 1.2 兆元，較 2026 年 6,786 億元增約 77%，主要是 Google 專案放量；漲價只為轉嫁成本；無併購、無回購。共識三年 EPS：2025 年 66.03 元→2028 年 285.29 元，年增 62.9%（Koyfin 2026-10-31 快照，美元依當日匯率換算）。內生上界以資本口徑無法解釋這個增速（推導見護城河段），缺口歸因為營業利益率擴張（16.1% 往 2027 年 20% 以上）與新客戶合約營收，不是回購或併購；屬依賴單一專案與利潤率擴張的成長，長期信心上限為中。跑道：2027 年公司在約 800 億美元的 AI 加速器 ASIC 可服務市場中取約兩成，2028 年市場更大，另有第二家客戶 2028 年量產、NVLink Fusion 與機櫃方案；手機已成熟。衰退訊號亮三項，其中毛利率年減與 EPS 增速高於營收兩項來自產品組合轉換，手機市占流失是實質衰退。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_kpi9_4q26","f_peer_2454_tw_operating_margin_pct"],"verdict_values":{"growth":{"driver_mix":"量為主：2027 年 ASIC 量產帶動共識營收年增約 77%；價為輔（成本轉嫁漲價）；無併購、無回購。","runway_years":"≥10 年（資料中心）；手機已成熟","runway_post_y5":"🟢","endo_ceiling_basis":"資本口徑內生上界接近零（歷年自由現金流高於淨利、再投資率代理為負），共識三年 EPS 年增 62.9% 超出；缺口來自營業利益率擴張與新合約營收，靠費用化研發而非資本支出取得。","segments":[{"item":"手機（37%）","value":"第三季季減 1%、年減 17%；2 奈米旗艦 Dimensity 9600 Pro 表現優於預期"},{"item":"Smart Edge（58%）","value":"季增 20%、年增 63%；含 9 月開始出貨的首顆 AI 加速器、新客戶 5G 數據機、AI 平板與 AI PC、車用座艙，電視 SoC 受 DRAM 內含值帶動"},{"item":"電源 IC（5%）","value":"季增 1%、年增 18%，來自資料中心份額提升"},{"item":"資料中心 ASIC","value":"2026 年第四季約 25 億美元；2027 年目標區間高標約 160 億美元，約占 2027 年共識營收四成；第二家客戶 2028 年開始貢獻"}],"decay_signals":[{"signal":"毛利率連兩季年減","lit":true,"note":"第二季年減（CFO 歸因去年同期一次性利益）、第三季 46.3% 對 46.5%；第四季指引 45% 會續降，主因資料中心組合，屬組合轉換副作用，以營業利益率驗證"},{"signal":"核心市占近 12 個月縮減","lit":true,"note":"智慧手機 SoC 市占 38%→32%，屬實質衰退"},{"signal":"主力產品提價後銷量下滑","lit":false,"note":"有成本轉嫁漲價、手機營收年減 17%，但量價拆分事實表未涵蓋，無法歸因於漲價"},{"signal":"EPS 年增顯著高於營收年增","lit":true,"note":"2025→2027 年共識 EPS 年增約 51%、營收約 42%，差 9 個百分點，來自營業槓桿，屬組合轉換副作用"},{"signal":"FCF／淨利連兩年低於 0.75","lit":false,"note":"2022～2025 年皆高於 1；第三季營業現金流轉負，列入追蹤"},{"signal":"SBC／營收高於 5% 且上升","lit":false,"note":"0.47%"},{"signal":"TAM 萎縮或被替代","lit":false,"note":"公司層級可服務市場因資料中心擴大；手機出貨 2026 年預估年減約 15%，屬記憶體成本造成的循環收縮，已列短期風險"},{"signal":"產業估值倍數近 3 年系統性下移","lit":false,"note":"本身倍數位於 4 個年度端點頂端，同業倍數序列事實表未涵蓋"},{"signal":"維持性資本支出占 FCF 高於 60%","lit":false,"note":"無晶圓廠模式，資本支出低"},{"signal":"停止投資新產能且營收 3 年內下滑","lit":false,"note":"不適用，營收成長中"}],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"資本配置中等偏穩：淨現金 2,364 億元、配息為主、SBC 極低、不回購；本季發行 39 億美元可轉債換取客戶入股與關鍵零組件產能，存貨墊高使營業現金流轉負，是放量期的代價，也是要盯的地方。","reasoning":"FCF／淨利：2022～2025 年分別 1.06、1.94、1.26、1.30 倍，歷年現金轉換好；但第三季營業現金流 −42.6 億元、存貨 1,535 億元（127 天），為第四季 ASIC 放量備料，單季資本支出新聞稿未揭露，單季自由現金流不推算。SBC 占營收 0.47%、占營業利益 2.9%，稀釋極低。股東回饋以現金股利為主，殖利率 1.37%，無庫藏股。新資金：39 億美元海外可轉債（NVIDIA、Alphabet 參與），約新台幣 1,248 億元、約市值 2%，轉換價事實表未涵蓋；董事會另核准 50 億美元融資額度，CFO 稱是備用彈性、可支持供應商擴產，並表示必要時會考慮對客戶提供融資。近 12 個月無對外併購，僅集團內子公司簡易合併。現金去向四分（研發、資本支出、股利、併購）近三年比例事實表未涵蓋。","fact_refs":["f_kpi5_ocf","f_kpi6_sbc","f_kpi7_archetype","f_kpi8","f_net_debt_m","f_dividend_yield_ttm","f_ev_m"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":false,"passed":null,"input":"近 12 個月無對外併購，僅集團內子公司簡易合併"},{"name":"buyback_yield","applicable":false,"passed":null,"input":"無庫藏股買回，股東回饋以現金股利為主（殖利率 1.37%）"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"第三季 SBC 7.83 億元，占營收 0.47%，年化約 31 億元、約市值 0.05%；可轉債轉換約 2% 屬一次性，不計入 SBC"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長來自自有研發與客製晶片合約，不靠併購撐；近 12 個月無對外併購，近三年現金去向分配比例事實表未涵蓋"}}}},"q5_valuation":{"verdict":"現價 3,915 元約是 2027 年共識 26 倍、2028 年 13.7 倍，要求 2027 年 ASIC 做到 160 億美元高標、2028 年第二代如期再翻倍；我信 2027 年，2028 年只信一半，判為合理而非便宜。","reasoning":"股價與前份幾乎相同（3,925→3,915），但 2027 年共識 EPS 已到 150.46 元，前份以 30 倍對應約 3,150 元，隱含當時約 105 元，分母上修約四成；FY1 共識近三個月上修 6%。2026 年預估本益比 55.1 倍、Trailing 64.7 倍、股價營收比 10.1 倍都在 4 個年度端點頂端，那是因為分母還停在 2026 年低基期。真正的爭點是 2028 年：13.7 倍的便宜要靠尚未量產的第二代，分母本身有爭議，不能拿來主張便宜。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_pe_current","f_pe_percentile","f_ps_current","f_ev_s_fwd","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_3m_fy1_pct","f_consensus_rev_fy2_pct"],"verdict_values":{"valuation":{"basis":"2027 年共識 Fwd P/E 為主，PEG 為輔","tier":"大型 IC 設計（手機 SoC＋雲端客製晶片）","peers":{"expanded":false,"reason":"同業對照表只有利潤率，同業 Fwd P/E 事實表未涵蓋，無法做倍數對照"},"fwd_pe":55.14,"peg":0.88,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"以 2027 年共識 EPS 150.46 元計 26.0 倍（3,915÷150.46）；2026 年 55.1 倍、Trailing 64.7 倍位於 4 個年度端點頂端（非五年分位，五年分位事實表未涵蓋）。PEG 以 2026 年預估本益比 55.1 倍除以共識三年 EPS 年增 62.9%（66.03→285.29）得 0.88；改用基準情境三年年增 53.7%（66.03→240）得 1.03。分母依賴第二代專案，便宜論證不成立，所以落在合理。短期：2027 年底以 2028 年基準 EPS 240 元×20 倍＝4,800 元，約 +23%；中期：五年基準 315 元×18 倍＝5,670 元，約 +45%。","upside_short_pct":22.6,"upside_mid_pct":44.8,"denominator_disputed":true,"denominator_note":"2027～2028 年 EPS 是否成立正是爭點：2027 年約四成營收來自單一客戶的一代產品，2028 年共識 285 元依賴尚未量產的第二代；以 2028 年 13.7 倍主張便宜不成立。"}}},"q6_how_wrong":{"verdict":"最可能看錯在第二代專案與 Google 份額，其次是 ASIC 放量後現金與毛利率被上下游吃掉；陷阱風險中等。","reasoning":"陷阱風險中：衰退訊號三項亮燈，手機市占流失是實質衰退，毛利率年減與 EPS 增速高於營收是公司刻意改走營業利益率模式的副作用；若 2027 上半年營業利益率沒有升到 19% 以上，這兩項改計為實質衰退，風險升為高。最大回撤估 −45%～−65%：現價距 104 週均線 −46.5%、距 250 週均線 −66.4%；上一輪手機循環 2023 年 EPS 由 74.23 元降到 48.34 元（−35%），再疊加 2027 年倍數由 26 倍壓到 15 倍，跌幅約 −62%；今年 6 月因對手消息跌停、9 月傳聞單日跌逾 7%，事件驅動的急跌常見。論點本身完整（護城河方向穩定、跑道寬、不靠倍數擴張），深回撤時不因波動砍倉，要先有心理準備。","fact_refs":["f_price_at_dd","f_ma_w104","f_ma_w250","f_kpi5_ocf","f_kpi7_archetype","f_consensus_eps_fy2"],"verdict_values":{"trap":{"verdict":"🟡","label":"成長轉換期的中度風險：手機本業衰退，新業務押在單一客戶"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":71.0,"pe":55.14,"basis":"起點為 2026 年共識 EPS 71.0 元（只剩第四季），現價 3,915 元對應 55.1 倍；終端倍數同樣套在 2031 年度 EPS 上，同為當年度口徑"},"eps":{"bull":[160,300,370,430,480],"base":[145,240,270,295,315],"bear":[125,135,120,125,135]},"pe":{"bull":22,"base":18,"bear":13},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":1.37,"net_buyback":-0.4},"second_stage":{"bull_cagr_pct":12,"base_cagr_pct":7},"max_dd":{"lo":-65,"hi":-45,"basis":"現價 3,915 元距 104 週均線 2,095 元為 −46.5%、距 250 週均線 1,316.5 元為 −66.4%；上一輪手機循環 2023 年 EPS 由 74.23 元降到 48.34 元（−35%），再疊加 2027 年倍數由 26 倍壓到 15 倍，跌幅約 −62%；今年 6 月單日跌停、9 月傳聞單日跌逾 7%，顯示事件驅動的急跌","trigger_time":null},"basis":{"bull":"2027 年 ASIC 超出 160 億美元高標，2028 年第二代與第二家客戶同時放量，營業利益率升到 25% 以上；2028 年 EPS 300 元略高於共識，之後隨第三代與 NVLink Fusion 新客戶年增約 15%；終端 22 倍，由 2027 年共識 26 倍下修，同業 Fwd P/E 事實表未涵蓋","base":"2027 年 ASIC 接近高標但毛利率被組合稀釋，EPS 145 元（共識 150.46）；第二代如期但受載板與封裝產能限制，2028 年 240 元（共識 285.29）；之後年增 7%～12%，終端 18 倍；股息以目前殖利率 1.37% 計，39 億美元可轉債轉換約稀釋 2% 股本，以每年 −0.4% 計","bear":"第二代延後兩季以上或主力份額轉移，2028 年後 EPS 停在 120～135 元，終端 13 倍（成長降到 5% 左右的倍數）；機率 30% 的依據：唯一致命點 12～24 個月約 25%，加上雲端資本支出放緩與毛利率結構下修，且共識增速超出資本口徑內生上界"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"9 月傳 Google TPU v9 可能由 Marvell 分食、v8 樣品延到 2027 年第二季（公司未證實）；4 月已傳 Marvell 成為第三家夥伴；6 月高通與 Meta 合作切入 AI ASIC，當日股價跌停；博通仍是 Google 原主力。2027 年 ASIC 約占共識營收四成。","assumption":"第二代如期在 2028 年第一季量產並維持主力份額。","consequence":"第二代延後兩季或份額轉移，2028 年 EPS 停在 120～140 元（對共識 285 元），本益比壓到 13 倍，股價約 1,750 元，五年虧損約 55%。","ruling":"採納為空頭情境，機率 30%；與唯一致命點是同一件事，不另設。","watch":"大晶粒投片、首批樣品、封裝良率的公司說法；Google 供應商消息。","evidence_refs":["customer_second_source#0","competitive_share_entrants#1","competitive_share_entrants#2"],"fact_refs":["f_consensus_eps_fy3","f_rev_consensus_fy2_m"]},{"view":"論點失敗","evidence":"智慧手機 SoC 市占 38%→32%，紫光展銳在 4G、高通在 5G 搶單，5G SoC 單價預估年減約一成；傳高層赴韓爭取記憶體產能；外資預估 2026 年智慧機晶片出貨年減約 7%；第三季手機營收年減 17%。","assumption":"手機在占營收 37% 的情況下仍能提供研發所需的現金流。","consequence":"手機再年減 15% 兩年，約拖累合併營收 5～6 個百分點，旗艦以外的組合惡化會拉低毛利率。","ruling":"部分採納：手機占比已降到 37%，ASIC 放量後衝擊被稀釋，不是致命點；但列為停止加碼條件。","watch":"手機營收年增率、Counterpoint 季度市占。","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#3","supply_demand_durability#2","substitute_technology#1","end_markets#0"],"fact_refs":["f_kpi0_gaap_tifrs"]},{"view":"論點成功但股東經濟變差","evidence":"大摩、高盛示警毛利率結構性下修（台積電漲價、車用與 ASIC 初期毛利低）；大摩稱 TPU 出貨與 T-Glass、載板供應高度相關；第三季營業現金流 −42.6 億元、存貨 1,535 億元（127 天）；發行 39 億美元可轉債、董事會核准 50 億美元融資額度可支持供應商；CFO 稱必要時會考慮對客戶提供融資，對手正用「先買後付」條件搶前沿模型客戶。","assumption":"ASIC 營收放大後，營業利益率升到 20% 以上，現金轉換回到淨利以上。","consequence":"營收翻倍但存貨、預付產能、客戶融資吃掉現金，可轉債轉換稀釋約 2% 股本，每股自由現金流增幅明顯落後 EPS；毛利率若跌破 43%，營業利益率卡在 17%～18%，2027 年 EPS 約 125 元而非 150 元。","ruling":"採納：基準情境 EPS 低於共識約 4%～16%（2027 年 145 元、2028 年 240 元），並設存貨與現金流的減碼條件。","watch":"季度營業現金流、存貨天數、營業利益率、客戶融資揭露。","evidence_refs":["substitute_technology#2","substitute_technology#0"],"fact_refs":["f_kpi5_ocf","f_kpi7_archetype","f_kpi1_gaap"]},{"view":"價格已反映太多","evidence":"26 週上漲 50.9%；Trailing 本益比 64.7 倍、股價營收比 10.1 倍皆位於 4 個年度端點頂端；5 月曾因交易過熱被列處置股；外資最高目標價 10,000 元。","assumption":"2027 年高標與 2028 年再翻倍都已進共識。","consequence":"若 2028 年只做到基準 240 元，2027 年底以 20 倍計約 4,800 元，一年報酬約 23%；若 2028 年能見度轉差，市場把 2027 年 26 倍壓回 20 倍，約 −23%。","ruling":"部分反駁：以 2027 年 26 倍、2027 年 EPS 年增逾一倍看並不極端，Trailing 倍數高是分母停在低基期；但 2028 年 13.7 倍的便宜不能當進場理由。","watch":"2028 年共識 EPS 修正方向；股價對 2028 年共識倍數是否超過 22 倍。","evidence_refs":["major_events#1"],"fact_refs":["f_week26_return_pct","f_pe_current","f_pe_percentile","f_ps_current","f_fwd_pe_latest"]},{"view":"論點失敗","evidence":"摩根士丹利在 2026-10-30 法說追問新雲融資與 ARR 放緩，CEO 承認近幾週市場波動、需求增速可能變動。","assumption":"雲端客戶 2027～2028 年持續擴大 AI 資本支出，且優先投資自研 ASIC。","consequence":"資本支出放緩時客戶可能優先保 GPU，2028 年第二代放量縮小，EPS 落在基準與空頭之間。","ruling":"部分採納：併入空頭情境機率；CEO 的需求判斷是一手但有利害，不單獨調高機率。","watch":"主要雲端客戶年度資本支出指引、公司 2028 年營收方向說法。","evidence_refs":[],"fact_refs":[]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 ✅","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=✅","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 3925 → 本次 3915.0（-0.3%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=3925","side_b":"本次 price_at_dd=3915.0","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 3,925 元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 3,925 元：Bull 價 8,800、Bear 價 2,250，五年期望值 +36.0%，基準年化 8.0%，不對稱比 2.4","side_b":"本次情境、股價仍用 3,925 元：Bull 價 10,560、Bear 價 1,755，五年期望值 +45.7%，基準年化 7.6%，不對稱比 2.55","ruling":"先換情境、股價不動：五年期望值多 9.7 個百分點，基準年化少 0.4 個百分點。不對稱比由 2.4 變為 2.55。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變好。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 3,925 元：五年期望值 +45.7%，基準年化 7.6%，不對稱比 2.55","side_b":"本次情境、股價 3,915 元：五年期望值 +46.1%，基準年化 7.7%，不對稱比 2.56","ruling":"再換股價、情境不動：起點價下跌 0.3%，五年期望值多 0.4 個百分點，基準年化多 0.1 個百分點，不對稱比由 2.55 升到 2.56。合計五年期望值比前份多 10.1 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"管理層承諾與兌現（2026-07-31 對照 2026-10-30）","cause":null,"prior_field":null,"side_a":"2026-07-31 CEO：第三季營收 1,522～1,598 億元、毛利率 46% ±1.5pp、手機季減持平到中個位數、資料中心 2026 年營收逾 20 億美元、第二顆 ASIC 約 2028 年初量產、448G SerDes 明年下半年就緒。","side_b":"2026-10-30：營收 1,681 億元超出高標、毛利率 46.3%、手機季減 1%、資料中心第四季上調到 25 億美元、第二顆 ASIC 重申 2028 年第一季量產、448G SerDes 已投片。","ruling":"一致：前一季各項財測全部達成或超出，時程沒有改口；執行力 8 分據此給。唯一補上的是營業利益率幅度，前一季只給方向，本季才給 2027 年 20% 以上。","evidence_level":"公司逐字稿","settle_metric":"後續各季財測達成率","if_then":["若下一季營收或時程首次低於財測，執行力降為 7 分並停止加碼"],"evidence_refs":[]},{"axis":"第二代專案時程與份額","cause":null,"prior_field":null,"side_a":"CEO／CFO 2026-10-30：第二代如期，數顆晶粒已投片、大晶粒晚 2～3 週；競爭專案效能差很遠；客戶要的是上修量。","side_b":"2026-09 媒體傳 Google TPU v9 可能由 Marvell 分食、v8 樣品延到 2027 年第二季（公司未證實）；4 月已傳 Marvell 成為第三家；6 月高通與 Meta 合作切入 ASIC。","ruling":"方向相反、決勝數據還不存在：公司說法是一手但有利害，媒體說法是二手傳聞。基準情境採公司時程，但不當成事實，裁為不可裁決至 2027-02 法說，以 30% 空頭機率與起步倉定價。現在就賣的最強論證：2027 年約四成營收押在一家客戶的一代產品上，第二代改用尚未量產驗證的美國 IDM 封裝，對手有客戶融資撐腰，而共識已用上高標。","evidence_level":"公司說法對二手傳聞","settle_metric":"第二代大晶粒投片、首批樣品與 2028 年量產時程的公司確認","if_then":["若 2027-02 法說確認第二代全部晶粒投片並重申 2028 年第一季量產，加碼至目標部位三分之二","若公司或客戶證實量產延後超過一季或第三家取得同世代量產單，減碼一半；延後兩季以上則清倉","若股價先漲到 2028 年共識 22 倍以上（約 6,280 元）而第二代尚未確認，不追","若股價因傳聞跌回 104 週均線附近（約 2,095 元）而公司時程未改，分批反買"],"evidence_refs":["customer_second_source#0","competitive_share_entrants#2","competitive_share_entrants#1"]},{"axis":"毛利率稀釋與營業利益率增益","cause":null,"prior_field":null,"side_a":"大摩、高盛示警毛利率結構性下修；第四季毛利率指引降到 45% ±1.5pp，CFO 稱資料中心毛利率仍低於公司平均。","side_b":"CFO：資料中心營業利益率自第四季起高於公司平均，2027 年營業利益率 20% 以上，之後繼續改善。","ruling":"程度差異、可調和：毛利率因組合下滑是公司自己承認的設計，關鍵在營業利益率有沒有跟上。門檻改用營業利益率，毛利率只設 43% 地板。","evidence_level":"公司指引對賣方報告","settle_metric":"2027 上半年 GAAP 營業利益率","if_then":["若 2027 年任兩季營業利益率低於 18%，減碼一半"],"evidence_refs":["substitute_technology#2"]},{"axis":"估值結論與裁決","cause":"新證據","prior_field":["val"],"side_a":"前份（2026-07-11，股價 3,925 元）：估值偏貴，以 2027 年 30 倍、約 3,150 元為重新評估價位，隱含當時 2027 年 EPS 約 105 元；裁決觀望。","side_b":"本次（股價 3,915 元）：2027 年共識 EPS 150.46 元，現價約 26 倍，已低於前份 30 倍門檻；估值改判合理。裁決與角色若因此改變，原因是分母上修而非股價下跌。","ruling":"新證據：股價幾乎沒動，是 2027 年共識在兩次法說後上修約四成，FY1 近三個月上修 6%。分母依賴單一專案，所以只判合理、不判便宜。","evidence_level":"共識快照＋公司指引","settle_metric":"2027 年共識 EPS 修正方向","if_then":["若 2027 年共識回落到 120 元以下，估值改回偏貴並停止加碼"],"evidence_refs":[]},{"axis":"價值陷阱風險","cause":"新證據","prior_field":["trap"],"side_a":"前份：陷阱風險低。","side_b":"本次：中。智慧手機 SoC 市占 38%→32%、手機營收年減 17%、毛利率連兩季年減、EPS 增速高於營收 9 個百分點。","ruling":"三項衰退訊號亮燈，其中毛利率年減與 EPS 增速高於營收兩項來自刻意的產品組合轉換，只計一半；若 2027 上半年營業利益率沒有升到 19% 以上，這兩項改計為實質衰退，陷阱風險升為高並減碼一半。","evidence_level":"第三方市占＋公司財報","settle_metric":"2027 上半年營業利益率、手機市占","if_then":["若 2027 上半年營業利益率低於 19% 且手機市占再降，陷阱風險升為高，減碼一半"],"evidence_refs":["competitive_share_entrants#0","end_markets#0"]},{"axis":"護城河方向、跑道、型態與循環位置","cause":"新證據","prior_field":["signal","moat_trend","runway_post_y5","archetype","cycle_position"],"side_a":"前份：綜合評等 B、護城河方向穩定、五年後跑道寬、品質複利成長型、未設循環位置。","side_b":"本次相同。","ruling":"新證據兩邊都有：首顆 ASIC 如期出貨、第二家客戶入列強化資料中心跑道，手機市占流失削弱定價力，相抵後各欄不變；仍不列為循環股，因成長主軸是合約型客製晶片。","evidence_level":"公司逐字稿＋第三方市占","settle_metric":"資料中心營收與手機市占","if_then":["若手機市占跌破 28% 且第二代延後，護城河方向改為縮減"],"evidence_refs":["competitive_share_entrants#0"]},{"axis":"重新評估條件","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"回檔至 FY27 30x（約 $3,150）或 ASIC 量產＋毛利率能見度兌現","side_b":"第二代 ASIC 全部晶粒投片完成並重申 2028 年第一季量產（預計 2027-02 法說確認）","ruling":"前份兩個條件都已觸發：9 月首顆 ASIC 量產出貨，2027 年本益比因共識上修降到 26 倍。但 26 倍的分母約四成押在單一客戶的一代產品，2028 年還要靠尚未量產的第二代，估值是否合理現在定不了，所以仍是觀望、現價不建倉。要等的是分母被證實，不是等股價回檔；重新評估改綁第二代投片確認，確認前不建倉。","evidence_level":"公司逐字稿＋共識快照","settle_metric":"第二代投片確認","if_then":["若 2027-02 法說確認第二代全部晶粒投片、量產時程不變，且第四季資料中心營收 ≥23 億美元、營業利益率 ≥18%，重跑研究後建到目標部位三分之二"],"evidence_refs":[]},{"axis":"唯一致命點","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設定唯一致命點（Single Thing 欄為空）。","side_b":"Single Thing：第二代 Google 客製 AI 晶片延後兩季以上，或客戶把該世代主力份額交給其他供應商。","ruling":"方法變動：本版要求設唯一致命點。選第二代專案，是因 2028 年共識 EPS 285 元相對 2027 年的增量幾乎全靠它，是數學上最大的單一敏感項；發生即清倉。","evidence_level":"公司逐字稿＋共識","settle_metric":"第二代量產時程","if_then":["若量產晚於 2028 年第二季，清倉"],"evidence_refs":["customer_second_source#0"]},{"axis":"停損指標","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設停損指標。","side_b":"本次五條：第二代量產晚於 2028 年第二季即清倉；2027 年任兩季營業利益率低於 18% 減碼一半；手機營收連兩季年減逾 15% 停止加碼；存貨高於 140 天且營業現金流連兩季為負減碼三分之一；證實第三家取得同世代量產單減碼一半。","ruling":"方法變動：本版要求每條減碼與清倉動作都綁指標、門檻與來源。","evidence_level":"方法","settle_metric":"各指標季度讀數","if_then":["任一條觸發即執行對應的減碼或清倉"],"evidence_refs":[]},{"axis":"情境機率與回撤","cause":"方法變動","prior_field":["p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份：多頭 25%、空頭 30%、最大回撤 −60%（單點）。","side_b":"本次：多頭 25%、基準 45%、空頭 30%；最大回撤改為 −45%～−65% 區間。","ruling":"機率不變；回撤由單點改區間，依 104 週與 250 週均線距離及上一輪手機循環 EPS 跌幅推得。","evidence_level":"方法","settle_metric":"無","if_then":["若第二代確認如期，空頭機率下調到 25%"],"evidence_refs":[]},{"axis":"論點與風險門檻","cause":"新證據","prior_field":["thesis.H1.threshold","thesis.R1.threshold","thesis.R3.threshold","thesis.H3.drift_rule"],"side_a":"前份：H1「ASIC 2027 營收 ≥30 億美元且合併毛利率 ≥45%」；R1「合併毛利率連兩季低於 45%」；R3「手機營收連兩季年減逾 15%」；H3「連 4 季手機營收年減逾 10% 為削弱」。","side_b":"本次：H1「2027 年 ASIC ≥140 億美元且營業利益率 ≥19%」；R1「2027 年任兩季營業利益率低於 18%」即減碼一半；R3 門檻不變，第三季已年減 17%，第二季讀數事實表未涵蓋；H3 改為手機年減不低於 −10%、市占不低於 28%、毛利率不低於 43%。","ruling":"公司明說資料中心毛利率低於平均、營業利益率高於平均，舊毛利率門檻會因組合自動觸發而不是因為生意變差，改用營業利益率；ASIC 規模門檻由 30 億提高到 140 億美元，因公司目標上修約五倍。前份手機假設已在削弱邊緣（第一季年減 15%、第三季年減 17%）。","evidence_level":"公司逐字稿","settle_metric":"2027 年營業利益率、手機營收年增率","if_then":["若手機營收第四季仍年減逾 15%，停止加碼"],"evidence_refs":["substitute_technology#2","end_markets#0"]}],"triggers":[{"n":1,"text":"2026 年第四季資料中心營收與營業利益率驗證首代放量","type":"假設驗證","maps_to":"H1","metric":"第四季資料中心營收（美元）、GAAP 營業利益率","threshold":"資料中心營收 ≥23 億美元且營業利益率 ≥18%","action":"達標續抱起步倉並進入加碼評估；未達標停止加碼","source_freq":"季度法說","date":"2027-02","evidence_refs":[]},{"n":2,"text":"第二代大晶粒投片完成並重申 2028 年第一季量產","type":"加碼","maps_to":"H2","metric":"第二代專案時程","threshold":"公司確認全部晶粒投片且量產時程不變","action":"加碼至目標部位三分之二","source_freq":"季度法說、重大訊息","date":"2027-02","evidence_refs":[]},{"n":3,"text":"2027 上半年營業利益率確認新模式成立","type":"加碼","maps_to":"H1","metric":"GAAP 營業利益率（季）","threshold":"2027 年第一、二季皆 ≥19%","action":"加碼至目標部位上限","source_freq":"季報新聞稿","date":"2027-07","evidence_refs":[]},{"n":4,"text":"第二代專案延後兩季以上或主力份額轉給其他供應商","type":"Single Thing","maps_to":"H2","metric":"第二代量產時程與供應商結構","threshold":"量產晚於 2028 年第二季，或客戶證實主力份額轉移","action":"清倉","source_freq":"季度法說、重大訊息、Google 供應鏈消息","date":"2027-02 起每季","evidence_refs":["customer_second_source#0"]},{"n":5,"text":"Google 證實第三家取得同世代推論 TPU 量產單","type":"減碼","maps_to":"R2","metric":"Google TPU 同世代量產供應商數","threshold":"公司或客戶證實","action":"減碼一半","source_freq":"事件","date":null,"evidence_refs":["competitive_share_entrants#2","competitive_share_entrants#1"]},{"n":6,"text":"營業利益率沒有隨 ASIC 放量上升","type":"減碼","maps_to":"R1","metric":"GAAP 營業利益率（季）","threshold":"2027 年任兩季低於 18%","action":"減碼一半","source_freq":"季報新聞稿","date":"2027-07","evidence_refs":["substitute_technology#2"]},{"n":7,"text":"手機本業量價雙縮","type":"風險","maps_to":"R3","metric":"手機營收年增率","threshold":"連 2 季年減逾 15%","action":"停止加碼","source_freq":"季度法說","date":"2027-02","evidence_refs":["end_markets#0","substitute_technology#1"]},{"n":8,"text":"存貨與營業現金流沒有在放量後回正","type":"減碼","maps_to":"R1","metric":"存貨週轉天數、營業現金流","threshold":"存貨高於 140 天且營業現金流連 2 季為負","action":"減碼三分之一","source_freq":"季報新聞稿","date":"2027-02","evidence_refs":["substitute_technology#0"]},{"n":9,"text":"出口管制擴大到公司或主要中國客戶","type":"風險","maps_to":"R4","metric":"台美出口許可清單","threshold":"公司產品或主要中國客戶被列入許可制","action":"減碼一半","source_freq":"事件","date":null,"evidence_refs":["reg_tariff_export#1"]},{"n":10,"text":"股價先漲、第二代證據未到","type":"估值rearm","maps_to":"H2","metric":"股價÷2028 年共識 EPS","threshold":"高於 22 倍（約 6,280 元）且第二代尚未量產","action":"不追、停止加碼","source_freq":"每日股價、每月共識","date":null,"evidence_refs":[]},{"n":11,"text":"2026 年第四季法說後複審","type":"複審日期","maps_to":null,"metric":"全份論點與觸發條件","threshold":"法說結束","action":"重跑研究","source_freq":"季度","date":"2027-02","evidence_refs":[]}],"kill_metrics":[{"metric":"第二代 ASIC 量產時程（公司法說）","bear_threshold":"量產晚於 2028 年第二季即清倉","window":"2027-02～2028-06","source":"公司季度法說、重大訊息","last_status":"ok"},{"metric":"GAAP 營業利益率（季）","bear_threshold":"2027 年任兩季低於 18% 即減碼一半","window":"2027Q1～2027Q4","source":"公司季報新聞稿","last_status":"ok"},{"metric":"手機營收年增率","bear_threshold":"連 2 季年減逾 15% 即停止加碼","window":"滾動 2 季","source":"公司法說營收分組","last_status":"warning"},{"metric":"存貨週轉天數＋營業現金流","bear_threshold":"存貨高於 140 天且營業現金流連 2 季為負即減碼三分之一","window":"2026Q4～2027Q2","source":"公司季報新聞稿","last_status":"warning"},{"metric":"Google TPU 同世代量產供應商數","bear_threshold":"證實第三家取得量產單即減碼一半","window":"2027～2028","source":"公司法說、Google 供應鏈消息","last_status":"warning"}],"evidence_dismissed":[{"ref":"$.decision_inputs.market_wrong_reason_given","reason":"閘把這欄讀成未填，但這欄填的是『否』，而且是實質答案。本份把估值判為合理、分母未定，沒有主張市場看錯；論點也不靠倍數擴張，所以不需要、也不應該寫市場錯在哪。觀望的原因是 2027～2028 年獲利分母有爭議，等的是第二代投片確認，不是等價格；等價格一欄已改填否，執行線與重新評估條件也已改成現價不建倉，和觀望一致。"},{"ref":"$.answers.q2_moat.verdict_values.moat.roic_durability","reason":"閘列的是資料缺口，不是推導錯誤。事實表沒有投入資本口徑，增量 ROIC 與內生上界算不出來，填任何數字都是編造。現行處理已用（淨利−自由現金流）÷淨利算出 2022～2025 年再投資率代理值（−6%、−94%、−26%、−30%），據此判共識三年 EPS 年增 62.9% 超出內生上界，並把這個超出反映在空頭機率 30% 與長期信心上限為中。等事實表補上投入資本再算。"}],"action_conditions":{"rearm_trigger":"第二代 ASIC 全部晶粒投片完成並重申 2028 年第一季量產（預計 2027-02 法說確認）","exec_line":"裁決觀望，現價不建倉。要等的是 2027～2028 年獲利分母被證實，不是等股價回檔。2027-02 法說若第四季資料中心營收 ≥23 億美元、營業利益率 ≥18%，且確認第二代全部晶粒投片、2028 年第一季量產不變，重跑研究後建到目標部位三分之二（原定現價先建的三分之一順延到此時一併建）；2027 上半年營業利益率皆 ≥19% 再補到上限；確認前任一減碼或停止加碼條件觸發，即不建倉。"}},"decision_inputs":{"signal":"B","ma":"✅","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":false,"wait_for_price_condition":null},"decision_out":{"role":"追蹤","row_hit":"8(val爭議)","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='✅'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟢', val='🟡', moat_trend='→', week26=50.9, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position=None, moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈機械讀數判定不可用，baseline rows 8/9/9b/10 的估值條件視為不可判 → 落 row8 觀望（保守方向）","hit":true,"basis":"val_denominator_disputed=True, val(機械讀數)='🟡'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":null,"requires_critic":[],"verdict":"觀望"},"thesis":{"H":[{"id":"H1","text":"首代 Google 客製 AI 晶片在 2027 年放量到公司目標高標，且公司改走的營業利益率模式成立","2y":"2026 年第四季資料中心營收約 25 億美元；2027 年資料中心 ASIC 約 160 億美元、全年營業利益率 20% 以上","5y":null,"10y":null,"threshold":"2027 年資料中心 ASIC 營收 ≥140 億美元，且 2027 全年 GAAP 營業利益率 ≥19%","source":"公司季度法說（2026-10-30 CEO 稱瞄準 2027 年目標高標約 160 億美元、CFO 稱 2027 年營業利益率 20% 以上）、季報新聞稿","drift_rule":"2 年期：TTM 營收或營業利益率連 2 季偏離目標路徑 ≥5% 為削弱，連 3 季 ≥10% 為反轉"},{"id":"H2","text":"第二代 Google 專案如期量產並維持主力供應，第二家客戶 2028 年開始貢獻，資料中心成為跨世代的事業","2y":"2027 年第一季前完成全部晶粒投片；2027 下半年公司給出 2028 年強勁成長的營收方向","5y":"2031 年前橫跨三代產品、兩家以上客戶，資料中心占營收 40% 以上","10y":null,"threshold":"第二代量產不晚於 2028 年第二季，2028 年營收年增 ≥25%","source":"公司季度法說（2026-07-31、2026-10-30 CEO／CFO）、Google 供應鏈消息、外資供應鏈調查","drift_rule":"時程證實延後 1 季為削弱，延後 2 季以上或主力份額轉移為反轉；5 年期資料中心營收 TTM 連 4 季低於目標路徑 ≥5% 為削弱、連 6 季 ≥10% 為反轉"},{"id":"H3","text":"手機本業不硬著陸、Smart Edge 新品類持續成長，邊緣端維持研發所需的現金流","2y":null,"5y":"手機營收在 2027 年後降幅收斂到個位數，AI PC、車用、平板旗艦等 ASIC 以外的品類持續貢獻成長","10y":null,"threshold":"2027 年起手機營收年增率不低於 −10%，智慧手機 SoC 市占不低於 28%，合併毛利率單季不低於 43%","source":"公司法說營收分組、Counterpoint 季度市占","drift_rule":"5 年期：TTM 手機營收連 4 季偏離門檻 ≥5% 為削弱，連 6 季 ≥10% 為反轉"}],"R":[{"id":"R1","text":"ASIC 放量受載板、先進封裝供應與良率限制，或為爭取份額讓價，毛利率被台積電漲價與初期低毛利拖累，營業利益率到不了 20%","h_ref":"H1","clock":"🔥","threshold":"2027 年任兩季 GAAP 營業利益率低於 18%，或公司下修 2027 年 ASIC 目標","evidence_refs":["substitute_technology#2","substitute_technology#0"]},{"id":"R2","text":"Google 引入第三家或回流博通，第二代主力份額被稀釋；改用美國 IDM 封裝的良率爬坡不如預期，量產延後","h_ref":"H2","clock":"🔥","threshold":"證實第三家取得同世代推論 TPU 量產單，或第二代量產晚於 2028 年第二季","evidence_refs":["customer_second_source#0","competitive_share_entrants#2","competitive_share_entrants#1"]},{"id":"R3","text":"記憶體漲價墊高手機 BOM、出貨下滑，紫光展銳與高通在 4G／5G 搶單壓價，手機量價雙縮","h_ref":"H3","clock":"⚡","threshold":"手機營收連 2 季年減逾 15%（第三季已年減 17%）","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#3","end_markets#0","substitute_technology#1","supply_demand_durability#2"]},{"id":"R4","text":"台美出口管制擴大到公司產品或主要中國手機客戶","h_ref":"H3","clock":"🐢","threshold":"公司產品或主要中國客戶被列入出口許可制","evidence_refs":["reg_tariff_export#1"]},{"id":"R5","text":"雲端與 AI 實驗室資本支出放緩，或客戶要求供應商融資才下單，公司被迫用資產負債表換訂單","h_ref":"H2","clock":"🔥","threshold":"主要雲端客戶下修年度資本支出，或公司揭露提供客戶融資","evidence_refs":[]}],"single_thing":{"description":"第二代 Google 客製 AI 晶片（公司稱 2028 年第一季量產、採美國 IDM 先進封裝）延後兩季以上，或客戶把該世代主力份額交給其他供應商","why_fatal":"2028 年共識 EPS 285 元相對 2027 年 150 元的增量幾乎全靠第二代放量；少了它，2028 年 EPS 約落在 120～140 元，現價對應約 28～33 倍，空頭情境 13 倍下股價約 1,750 元。這是情境樹裡最大的單一敏感項，手機與毛利率的變動都小於它。","if_happens":"清倉；保留研究追蹤，等第三代與第二家客戶（2028 年貢獻）有量產證據再重跑研究。","how_monitor":"大晶粒投片確認（CEO 2026-10-30 稱晚其他晶粒 2～3 週）、2027-02 與 2027-04 法說的時程用語、封裝良率說法、Google 供應商消息、2027 下半年首次給出 2028 年營收方向。","probability":"12～24 個月內約 25%"}},"appendix_a":{"growth_durability":6,"quality_score":7,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":26.02,"peg_fy2":0.41,"stress":{"pass":null,"total":null}},"eps_meta":{"base_eps_path":{"FY2025A":66.03,"FY2026E":71.0,"FY2027E":150.46,"FY2028E":285.29},"fy_end_month":12,"eps_basis":"TIFRS 歸屬母公司稀釋 EPS；共識取 Koyfin 2026-10-31 快照，美元依當日匯率 32.5669 換算新台幣"},"catalysts":[{"date":"2026-11","date_precision":"month","type":"product","event":"第二代 ASIC 大晶粒投片（CEO 稱晚其他晶粒 2～3 週）","impact":"高","watch":"公司或供應鏈確認投片完成"},{"date":"2027-02","date_precision":"month","type":"guidance","event":"2026 年第四季法說：資料中心 25 億美元是否兌現與 2027 年財測","impact":"高","watch":"資料中心營收、營業利益率、第二代時程用語"},{"date":"2027-Q2","date_precision":"quarter","type":"capacity","event":"載板與先進封裝擴產進度、第二代封裝良率","impact":"中","watch":"公司對 2028 年供應的說法"},{"date":"2027-Q3","date_precision":"quarter","type":"guidance","event":"首次給出 2028 年資料中心營收方向","impact":"高","watch":"是否維持強勁成長說法、第二家客戶規模"}]}
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
