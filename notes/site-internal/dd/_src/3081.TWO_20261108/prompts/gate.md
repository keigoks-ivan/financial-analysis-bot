你是 DD 管線 v20 的判斷層閘（gate），標的 3081.TWO（20261108）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（31 條）
- `f_kpi0`（q1_business）｜營收（合併）＝1221.2 百萬 TWD｜期間與口徑：Q2 2026（季末 2026-06-30，法說 2026-08-12）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：yfinance quarterly_income_stmt；優分析法說報導 https://uanalyze.com.tw/articles/6110153300（numbers.latest_quarter_kpis.items[0]，as_of Q2 2026（季末 2026-06-30，法說 2026-08-12））
  - 註記：查無
- `f_kpi1`（q1_business）｜毛利率＝57.45 %｜期間與口徑：Q2 2026（季末 2026-06-30，法說 2026-08-12）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：yfinance（毛利 701.6／營收 1221.2）；優分析報導 57%（numbers.latest_quarter_kpis.items[1]，as_of Q2 2026（季末 2026-06-30，法說 2026-08-12））
  - 註記：查無
- `f_kpi2_gaap_non_gaap`（q1_business）｜營業利益／利益率（GAAP；台股無 Non-GAAP 口徑，兩者同）＝572.6 百萬 TWD（利益率 46.9%）｜期間與口徑：Q2 2026（季末 2026-06-30，法說 2026-08-12）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：yfinance quarterly_income_stmt；優分析報導 營益率約 47%（numbers.latest_quarter_kpis.items[2]，as_of Q2 2026（季末 2026-06-30，法說 2026-08-12））
  - 註記：查無
- `f_kpi6`（q1_business）｜管理層指引＝無數字指引：矽光需求「非常強勁」，未來數季出貨續增；2027 年產能約為 2026 年 2.5 倍；近三季已公告資本支出近 60 億元，今年另有追加支出待董事會核准 定性｜期間與口徑：Q2 2026 法說會（2026-08-12）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：優分析法說報導 https://uanalyze.com.tw/articles/6110153300（numbers.latest_quarter_kpis.items[6]，as_of Q2 2026 法說會（2026-08-12））
  - 註記：未給 Q3／全年營收或 EPS 區間
- `f_kpi7_datacom`（q1_business）｜產品組合（DataCom 占營收）＝80–85%（矽光為最大塊；電信 5–10%，其他約 5%）；1.6T 已量產、3.2T 與客戶開發中 占營收｜期間與口徑：Q2 2026 法說會（2026-08-12）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：優分析法說報導 https://uanalyze.com.tw/articles/6110153300（numbers.latest_quarter_kpis.items[7]，as_of Q2 2026 法說會（2026-08-12））
  - 註記：不適用
- `f_earnings_recency`（q1_business）｜最近一次財報日＝2026-10-28 date｜期間與口徑：2026-10-28／距今 8 個交易日｜kind：realized
  - 來源：—（numbers.earnings_recency，as_of 2026-10-28）
- `f_peer_3081_two_gross_margin_pct`（q2_moat）｜3081.TWO 毛利率＝55.99 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.3081.TWO.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_3081_two_operating_margin_pct`（q2_moat）｜3081.TWO 營業利益率＝44.48 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.3081.TWO.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_3081_two_fcf_margin_pct`（q2_moat）｜3081.TWO FCF 利潤率＝3.45 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.3081.TWO.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_lite_gross_margin_pct`（q2_moat）｜LITE 毛利率＝45.91 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.LITE.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_lite_operating_margin_pct`（q2_moat）｜LITE 營業利益率＝23.35 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.LITE.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_2455_tw_gross_margin_pct`（q2_moat）｜2455.TW 毛利率＝37.27 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.2455.TW.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_2455_tw_operating_margin_pct`（q2_moat）｜2455.TW 營業利益率＝21.72 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.2455.TW.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_kpi4`（q4_capital）｜自由現金流（營業現金流 − 資本支出）＝-479.3 百萬 TWD｜期間與口徑：Q2 2026（季末 2026-06-30，yfinance 季度現金流量表）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：yfinance quarterly_cashflow（OCF 268.6 百萬、Capex 748.0 百萬）（numbers.latest_quarter_kpis.items[4]，as_of Q2 2026（季末 2026-06-30，yfinance 季度現金流量表））
  - 註記：不適用
- `f_ev_m`（q5_valuation）｜目前企業價值 EV（市值＋淨負債）＝160152.98 TWD m｜期間與口徑：2026-11-08／市值 161905.25 ＋ 淨負債 -1752.27｜kind：realized
  - 來源：—（numbers.capital_structure.ev_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_ps_current`（q5_valuation）｜P/S（現值）＝37.39 x｜期間與口徑：2026-11-06（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-11-06（RTH 收盤，UTC））
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝20.6 TWD/share｜期間與口徑：2026-11-08／yfinance 分析師共識平均（Koyfin 快照無此檔）；幣別同報價｜kind：estimate
  - 來源：yfinance earnings_estimate（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-11-08）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝40.72 TWD/share｜期間與口徑：2026-11-08／yfinance 分析師共識平均（Koyfin 快照無此檔）；幣別同報價｜kind：estimate
  - 來源：yfinance earnings_estimate（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-11-08）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝5492.13 TWD m｜期間與口徑：2026-11-08／yfinance revenue_estimate 0y 平均（7 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝10117.8 TWD m｜期間與口徑：2026-11-08／yfinance revenue_estimate +1y 平均（10 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi5_sbc`（q4_capital）｜SBC 占營業利益＝1.6 %｜期間與口徑：Q2 2026（SBC 9.06 百萬 ÷ 營業利益 572.6 百萬；占營收 0.7%）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：yfinance quarterly_cashflow SBC；自算（numbers.latest_quarter_kpis.items[5]，as_of Q2 2026（SBC 9.06 百萬 ÷ 營業利益 572.6 百萬；占營收 0.7%））
  - 註記：不適用
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝-1752.27 TWD m｜期間與口徑：2026-11-08／yfinance 最新一季：總債務 3170.65、現金 4922.92（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝0.171 %｜期間與口徑：2026-11-08／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-11-08）
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝1750.0 TWD｜期間與口徑：2026-11-06（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-11-06（RTH 收盤，UTC））
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝111.54 x｜期間與口徑：2026-11-06（RTH 收盤，UTC）／2 個年度端點內的分位＝75.7｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝100.0 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝100.0 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ev_s_fwd`（q5_valuation）｜EV/S（EV ÷ FY1 共識營收）＝29.16 x｜期間與口徑：2026-11-08／f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）｜kind：estimate
  - 來源：—（numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝92.52 m shares｜期間與口徑：2026-11-08／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝-26.4 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^TWII｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-11-06（RTH 收盤，UTC））
- `f_rsi14`（q5_valuation）｜RSI(14)＝28.01｜期間與口徑：2026-11-06（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-11-06（RTH 收盤，UTC））

### findings_digest 中方向為負或來源衝突的條目（8 條）
- `customer_concentration_credit#0`（customer_concentration_credit｜方向 -｜狀態 ok）：Quartr 摘要稱 2025 年底三家客戶占應收帳款 74%（為應收集中度，非營收占比）；2025 年銷售市場為中國 71%、美國 21%、台灣 3%。
  - 來源：Quartr, LandMark Optoelectronics (3081) Q4 2025 earnings summary（as_of 2026-03-01）｜affects：decision_inputs.bear、thesis.R
- `supply_demand_durability#3`（supply_demand_durability｜方向 -｜狀態 ok）：InP 基板供應仍緊；中國出口管制若延續至 8 月後且無新增來源，中長期供應風險仍須關注（聯亞已建庫存）
  - 來源：聯亞(3081)外資報告報導（搜尋摘要）（as_of 2026-08-10）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#2`（geo_supply_chain｜方向 -｜狀態 ok）：Marketscreener 頁面於2026-06-11有標題指中國對磷化銦出口管制威脅AI資料中心建置（產業層級，未說明對聯亞影響）
  - 來源：Marketscreener LandMark 頁面（as_of 2026-06-11）｜affects：thesis.R
- `cyclical_supply_discipline_capacity#3`（cyclical_supply_discipline_capacity｜方向 -｜狀態 ok）：高盛2026年3月報告提示風險：矽光子滲透率可能慢於預期、競爭加劇、IDM自行供應磊晶。
  - 來源：uanalyze/搜尋彙整（高盛報告）（as_of 2026-03-01）｜affects：thesis.R、decision_inputs.bear
- `cyclical_inventory_price_position#2`（cyclical_inventory_price_position｜方向 -｜狀態 ok）：InP基板供應仍緊；外資稱中國出口管制短期不衝擊產出因已有緩衝，但若限制延續至8月後且無新供應來源，中長期供應風險仍須關注
  - 來源：聯亞逆勢大盤而漲停 外資點名這麼說（udn money）（as_of 2026-03-26）｜affects：thesis.R、decision_inputs.bear
- `cyclical_prior_downcycle_behavior#0`（cyclical_prior_downcycle_behavior｜方向 -｜狀態 ok）：聯亞上一輪下行（2023–1H24）毛利率低點約8–10%：1H24毛利率10%（前年同期16%），9M24為16%（前年同期8%），Q4 2023約20%
  - 來源：Quartr LandMark Optoelectronics (3081) earnings summaries (Q2 2024／Q3 2024／Q4 2023)（as_of 2024-11-01）｜affects：decision_inputs.bear、thesis.R
- `cyclical_prior_downcycle_behavior#1`（cyclical_prior_downcycle_behavior｜方向 -｜狀態 ok）：2023年7月營收年減74.2%（消費性需求疲弱、中國基建標案未回溫），分析認為股價有下壓；2023-10-26盤中一度跌7.36%至98.2元
  - 來源：CMoney 投資快訊：聯亞(3081)公告7月營收大幅衰退7成不如預期；聯亞(3081-TW)26日股價報98.2元（as_of 2023-10-26）｜affects：decision_inputs.bear、valuation
- `cyclical_prior_downcycle_behavior#2`（cyclical_prior_downcycle_behavior｜方向 -｜狀態 ok）：2023年每股虧損2.31元，主因中國電信客戶幾乎消失、訂單大減、產能利用率低提列閒置損失；2024年8月起股價急漲達3倍
  - 來源：優分析 uanalyze：聯亞(3081)2023年每股虧損2.31元，但Q4毛利率開始優於預期；CPO & 矽光子|聯亞股價大漲（as_of 2024-12-31）｜affects：decision_inputs.bear、thesis.R

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/3081.TWO_20261108/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":3904,"bear_5y_price":468,"p_bull_pct":25,"p_bear_pct":30,"upside_5y_pct":-23.2,"ev5y_pct":-1.6,"irr_base_pct":-5.1,"asym_ratio":1.4,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":20.6,"pe":84.95,"basis":"FY2026E 共識 EPS（當年度），終端倍數同樣套在當年度 EPS 上。"},"eps":{"bull":[45,70,88,104,122],"base":[37,50,47,52,56],"bear":[31,28,16,20,26]},"pe":{"bull":32,"base":24,"bear":18},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0.171,"net_buyback":0},"second_stage":{"bull_cagr_pct":15,"base_cagr_pct":8},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

[本次無舊逐字稿摘錄]

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 2 | 2 |
| customer_second_source | none | 0 | 3 |
| customer_concentration_credit | found | 3 | 3 |
| supply_demand_durability | found | 6 | 3 |
| regulatory_antitrust | found | 2 | 1 |
| reg_tariff_export | found | 2 | 4 |
| geo_supply_chain | found | 3 | 2 |
| end_markets | found | 5 | 3 |
| substitute_technology | found | 2 | 2 |
| channel_business_model_shift | found | 2 | 3 |
| capital_markets_pricing | found | 4 | 3 |
| major_events | found | 1 | 4 |
| cyclical_supply_discipline_capacity | found | 4 | 3 |
| cyclical_inventory_price_position | found | 4 | 3 |
| cyclical_prior_downcycle_behavior | found | 4 | 3 |

未涵蓋／不適用軸的查詢詞原文（供判相關性）：
- **customer_second_source**（none）：聯亞 大客戶 第二供應商 OR 轉單 2026；聯亞 客戶 自製 OR 分散供應商；3081.TWO LandMark Optoelectronics largest customer second source OR in-house 2026

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20261012","verdict":"觀望","role":"追蹤","H":{"status":"unavailable"},"R":{"status":"unavailable"},"single_thing":null,"kill_metrics":null,"rearm_trigger":"股價回落至 FY2027 共識 EPS 35 倍以下（約 1,380 元）且單季毛利率仍 ≥50%","irr_base_pct":-14.3,"ev5y_pct":-40.2,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"追蹤","signal":"C","val":"🔴","ma":"✅","trap":"🟡","moat_trend":"→","runway_post_y5":"🟡","asym_ratio":0.4,"ev5y_pct":-40.2,"irr_base_pct":-14.3,"max_dd_pct":-85,"bull_5y_price":4140,"bear_5y_price":484,"p_bull_pct":25,"p_bear_pct":30,"rearm_trigger":"股價回落至 FY2027 共識 EPS 35 倍以下（約 1,380 元）且單季毛利率仍 ≥50%","price_at_dd":3025.0,"archetype":"循環/商品","cycle_position":"晚循環"}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"3081.TWO","date":"2026-11-08","schema":"v15.0","contract":"v19","company_name":"聯亞光電"},"oneliner":"資料中心矽光帶動的 InP 磊晶缺貨股。一個月跌 42% 後，現價約等於機率加權價值，仍要 FY2027 獲利翻倍且 2028 年後毛利率不崩才站得住。等約 1,425 元且單季毛利率守住 50% 再談進場。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/3081.TWO_20261108/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/3081.TWO_20261108/scenario.json","answers":{"q1_business":{"verdict":"聯亞賺資料中心光模組與雲端業者的錢，錢卡在 InP 磊晶片與 CW 雷射的產能這一節。","reasoning":"Q2 2026 營收 12.21 億元，毛利率 57.45%，營業利益率 46.9%。DataCom 占 80–85%，以矽光為大宗，電信 5–10%。供需判斷是週期性將反轉，時間點約在 2028 年前後：短缺目前是真的，但 Coherent 報導將兩度倍增 InP 產線，聯亞自己 2027 年產能也放大 2.5 倍，供給回得來。產業位置判第三階段（過熱），依據是毛利率為事實表四個年度內最高，上下游同時漲價與擴產。單點依賴屬於風險：矽光是最大產品，2025 年銷售 71% 在中國，三家客戶占應收帳款 74%。單一客戶營收占比事實表未涵蓋。10-28 公布的第三季財報內容也未涵蓋，單季數字最新只到 Q2。","fact_refs":["f_kpi0","f_kpi1","f_kpi2_gaap_non_gaap","f_kpi6","f_kpi7_datacom","f_earnings_recency"],"verdict_values":{"revenue_quality":"毛利率 57.45% 裡有多少是缺貨漲價、多少是產品組合，事實表無法拆分。Q2 資本支出占營收 61%，自由現金流為負。","unit_econ_note":"單價與出貨量的結構化數字事實表未涵蓋，只知基板自 2025 年第四季漲三次、磊晶片漲兩次，來源為未具名業界人士。","archetype":{"primary":"循環/商品","secondary":null,"confidence":"高","fingerprint":"2023、2024 連兩年虧損；毛利率由 13.08% 到 57.45%，擺幅約 44 個百分點；Q2 資本支出占營收 61%。"},"industry":{"clock_phase":"III","sd_verdict_source":"週期性將反轉，約在 2028 年前後。依據 TrendForce 的新產能時程與公司法說的 2027 年產能指引。","bargaining":{"up":"上游 InP 基板吃緊，已漲三次，第四季考慮再漲逾一成。住友電工 2026–2030 年長約降低斷料風險，是否鎖價事實表未涵蓋。","down":"缺貨期由聯亞議價，磊晶片已漲兩次。客戶增至 10 家以上，但 2025 年底三家客戶占應收帳款 74%。","geo":"2025 年銷售市場中國占 71%、美國 21%。基板受中國出口管制影響，美系雲端直接訂單是分散的方向。"},"profit_pool_dir":"缺貨期利潤往 InP 磊晶與雷射環節集中，五年利潤池占比事實表未涵蓋。","tam_table":{"expanded":false,"reason":"TAM、SAM、滲透率與利潤池占比事實表都未涵蓋，只有 800G 以上出貨量由 2,400 萬增至 6,300 萬一筆二手資料，組不成表。"}}}},"q2_moat":{"verdict":"護城河穩定，評 B 級，來自開放式 InP 磊晶的份額與客戶驗證，看不出跨週期的定價權。","reasoning":"當期 ROIC 算不出，因為投入資本與折舊事實表未涵蓋。持續期四項檢查是三項中等、一項良好：需求真實但付款者集中，客戶驗證有黏著但合約年限未知，聯亞毛利率高過客戶級同業，反而提高對方自製的誘因。新增資本報酬估約 25%，再投資率約 90%，內生成長上界約 22.5%。毛利率領先 LITE 約 10 個百分點，但這是缺貨期的讀數，同業 ROIC 差距與歷史趨勢都查無，所以不標擴大。反例是 2023 年毛利率 13.08%，當時需求一消失，定價能力也跟著消失。","fact_refs":["f_peer_3081_two_gross_margin_pct","f_peer_3081_two_operating_margin_pct","f_peer_3081_two_fcf_margin_pct","f_peer_lite_gross_margin_pct","f_peer_lite_operating_margin_pct","f_peer_2455_tw_gross_margin_pct","f_peer_2455_tw_operating_margin_pct","f_kpi4","f_kpi6","f_ev_m","f_ps_current"],"verdict_values":{"moat":{"mechanism":"開放式 InP 磊晶片的量產規模與客戶驗證週期。單一市場報告稱開放式市場份額逾 60%，未經第二來源確認。","execution":8,"pricing":6,"grade":"B","trend":"→","trend_evidence":"執行面穩定：1.6T 已量產、3.2T 驗證中，客戶由 7–8 家增至 10 家以上，住友基板長約到位。定價權穩定：現在能漲價，但 2023 年毛利率 13.08%，看不出跨週期定價權。TTM 毛利率領先 LITE 約 10 個百分點、營業利益率領先約 21 個百分點；同業 ROIC 差距與歷史趨勢事實表未涵蓋，所以不標擴大。","competitor_notes":[{"name":"LITE","strategy_note":"雷射同業，TTM 毛利率 45.91%、營業利益率 23.35%，都低於聯亞。雷射產能據稱訂到 2028 年，短期印證需求，長期是擴產與自製的對手。"},{"name":"2455.TW","strategy_note":"TTM 截至 2026-06，毛利率 37.27%、營業利益率 21.72%，獲利能力差聯亞一截。期間比聯亞早一季，比較略偏向聯亞有利。"},{"name":"IQE.L","strategy_note":"事實表沒有財務數字，無法比較。"},{"name":"Coherent","strategy_note":"報導將在今年及 2027 年底前兩度倍增德州 Sherman 的 InP 產線，是 2027 年後新增供給的主要來源之一，財務數字事實表未涵蓋。"}],"peer_na_reason":"IQE.L 無季度財報資料，Coherent 不在同業表內。","threats":[{"level":"🟡","text":"IDM 自行供應磊晶，加上同業擴產，壓縮開放式磊晶的份額與價格。目前只有賣方提示，沒有具體客戶轉自製的報導。","p":"30%","evidence_refs":["cyclical_supply_discipline_capacity#3","cyclical_supply_discipline_capacity#2"]},{"level":"🟡","text":"InP 基板受中國出口管制影響，庫存緩衝原本只看到 2026 年第三季。","p":"25%","evidence_refs":["supply_demand_durability#3","cyclical_inventory_price_position#2","geo_supply_chain#2"]},{"level":"🟡","text":"客戶與地區集中，三家客戶占應收帳款 74%，銷售 71% 在中國，少數客戶改單就會直接影響營收。","p":"25%","evidence_refs":["customer_concentration_credit#0"]}],"roic_durability":{"quadrant":"高利益率×低周轉","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"需求真實，Lumentum 稱出貨短缺客戶需求逾 30%，800G 以上出貨量大增。付款者集中在雲端資本支出，少數決策點就能延後採購。"},{"item":"決策層級","level":"🟡","text":"1.6T 已量產、3.2T 驗證中，換供應商要重新驗證，有黏著度。合約年限、重新認證週期與漲價後流失率事實表未涵蓋。"},{"item":"價值鏈分配","level":"🟡","text":"缺貨期聯亞拿到高分配，毛利率 55.99% 高過 LITE 的 45.91%。上游基板連續漲價，下游有擴產與自製能力，這個分配不穩固。"},{"item":"社會容忍度","level":"🟢","text":"企業間零組件，沒有消費者定價壓力；公平會處分 0 筆，反競爭訴訟損失為 0。出口管制另列為供應風險。"}],"roiic":25,"reinvest_rate":90,"endo_ceiling":22.5,"formula_note":"單位為百分比，皆為估算。投入資本與折舊事實表未涵蓋，象限由 Q2 資本支出占營收 61%、自由現金流為負推定。增量 ROIC：設備預算約 82.7 億元（近三季公告近 60 億元加上限 22.7 億元）。低案用共識 FY2027 較 FY2026 新增營收 46.3 億元×稅後 30%＝13.9 億元，得 17%；高案用產能 2.5 倍滿載新增 82.4 億元×稅後 34%＝28.0 億元，得 34%，取中間約 25%。再投資率：TTM 營收以市值 1,619 億元÷P/S 37.39 反推約 43.3 億元，自由現金流約 1.5 億元，稅後營業利益約 15.8 億元，1−0.09≈90%。內生上界＝25%×90%＝22.5%。90% 的再投資率難維持五年，此上界偏樂觀。"}}}},"q3_growth":{"verdict":"五年後仍有成長，但空間只能判中等：份額已高，下一段需求要靠 CPO，時程沒有數字。","reasoning":"現階段成長是量為主、價格助攻，沒有併購與回購。共識 FY2025 到 FY2027 EPS 年化 211%，營收年化 114%，差 97 個百分點來自利潤率擴張與低基期。第三年共識事實表未涵蓋，三年年化算不出。內生上界 22.5%，共識兩年年化與上界相差約 188 個百分點，歸因為利潤率擴張與產能利用率回升，不是再投資複利，不能外推。Base 路徑 FY2026E 到 FY2031E 年化 22.1%，在上界以內。滲透率事實表未涵蓋；3.2T 與 CPO 是下一段需求的來源，但沒有量化時程，不足以判寬。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_kpi6","f_kpi7_datacom"],"verdict_values":{"growth":{"driver_mix":"量為主、價為輔，無併購與回購貢獻。","runway_years":null,"runway_post_y5":"🟡","endo_ceiling_basis":"增量 ROIC 25%×再投資率 90%＝22.5%，推導見護城河段；缺口歸因為利潤率擴張。","segments":[{"item":"DataCom（矽光為大宗）","value":"約 80–85%"},{"item":"Telecom","value":"約 5–10%"},{"item":"其他","value":"約 5%"}],"decay_signals":[{"item":"EPS 成長顯著高於營收成長","value":"亮燈：共識 FY2025–FY2027 EPS 年化 211%，營收年化 114%，差 97 個百分點。"},{"item":"自由現金流對淨利低於 0.75 倍連兩年","value":"未亮但要盯：FY2025 為 1.46 倍，TTM 約 0.1 倍，再一個年度低於門檻就亮燈。"},{"item":"其餘八類","value":"未亮或事實表未涵蓋，市占變化、維護性資本支出與產業倍數趨勢都查無資料。"}]}}},"q4_capital":{"verdict":"資金全押在擴產，回饋股東不是重點，風險在設備預算大於帳上現金。","reasoning":"FY2025 自由現金流 6.27 億元，是淨利 4.28 億元的 1.46 倍。TTM 截至 2026-09 的自由現金流利潤率只剩 3.45%，對淨利約 0.1 倍；Q2 單季為 −4.79 億元。SBC 占營業利益 1.6%，年化約占市值 0.02%，不是問題。淨現金 17.5 億元（現金 49.2 億元、債務 31.7 億元），對約 82.7 億元設備預算不夠，差額要靠未來營業現金流或對外籌資。近三年現金去向、債務到期結構與回購紀錄事實表未涵蓋。","fact_refs":["f_kpi4","f_kpi5_sbc","f_peer_3081_two_fcf_margin_pct","f_net_debt_m","f_dividend_yield_ttm","f_kpi6"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":false,"passed":null,"input":"近 12 個月重大訊息未見併購事件，沒有可評估的併購報酬。"},{"name":"buyback_yield","applicable":false,"passed":null,"input":"回購紀錄事實表未涵蓋。"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"Q2 SBC 906 萬元，年化約 3,600 萬元，約占市值 0.02%，低於每年 1.5% 的上限。"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購，回購資料查無，股息殖利率 0.171% 不影響估值結論。"}}}},"q5_valuation":{"verdict":"現價 1,750 元要求 FY2027 獲利翻倍，而且 2028 年後毛利率不崩。前半我相信，後半現在不值得先付錢。","reasoning":"現價對 FY2026 共識 EPS 約 85 倍，對 FY2027 約 43 倍，trailing 111.54 倍，前瞻 EV/S 29.16 倍。P/S 與 EV/S 在 4 個年底端點中都是最高。情境樹 Bull 3,904 元、Base 1,344 元、Bear 468 元，機率加權約 1,720 元，比現價低約 2%。上份 3,025 元時約 77 倍，估值改善全部來自股價下跌。循環股本應看股價淨值比，但事實表未涵蓋；同業倍數也未涵蓋。","fact_refs":["f_price_at_dd","f_consensus_eps_fy1","f_consensus_eps_fy2","f_pe_current","f_ps_current","f_ps_percentile","f_ev_s_percentile","f_ev_s_fwd","f_ev_m","f_shares_diluted_m"],"verdict_values":{"valuation":{"basis":"FY2027 共識本益比。循環股的股價淨值比與同業倍數事實表未涵蓋。","tier":"高成長循環零組件","peers":{"expanded":false,"reason":"事實表只有同業利潤率，沒有同業倍數，不能用不同口徑的數字當錨。"},"fwd_pe":42.98,"peg":3.94,"percentile_5y":null,"val_light":"🟠","val_light_derivation":"現價約為 FY2027 共識 EPS 的 43 倍，機率加權五年價值約 1,720 元，沒有安全邊際，所以仍偏貴；相較上份約 77 倍已明顯回落，降一檔。五年分位事實表未涵蓋，只有年度端點。PEG 用 FY2027 本益比 42.98 倍除以 Base FY2027–FY2031 年化 10.9%。若用共識 FY2026 到 FY2027 成長 97.7% 計算 PEG 為 0.87，那是產能爆發的一次性跳升，不採用。短期目標 1,500 元＝FY2028 Base EPS 50 元×30 倍；中期目標 1,316 元＝FY2029 Base EPS 47 元×28 倍。","upside_short_pct":-14.3,"upside_mid_pct":-24.8,"denominator_disputed":true,"denominator_note":"FY2027 EPS 40.72 元建立在缺貨期利潤率與產能 2.5 倍上，用它得出 43 倍不能當便宜的論據。股數也有疑義：事實表 92.52 百萬股，由 Q2 淨利 468.5 百萬元÷EPS 4.62 元反推約 101.4 百萬股，差約一成，市值與 EV/S 可能低估約一成，本益比不受影響。"}}},"q6_how_wrong":{"verdict":"成長是真的，風險在價格用的是缺貨期的利潤率，而這波大跌的原因我手上沒有。","reasoning":"偏多看錯的路徑：2028 年新產能與自製同時到位，毛利率往 2023 年的方向走。偏空看錯的路徑：3.2T 與 CPO 放量早於預期，缺貨延長，毛利率維持 55% 以上，Bull 的 3,904 元約為現價 2.2 倍，此時等 1,425 元會買不到。最大的資料缺口是 10-12 到 11-06 跌 42% 的原因，期間包含 10-28 的第三季財報，內容事實表未涵蓋。歷史最大回撤序列與放空方數字也未涵蓋。","fact_refs":["f_price_at_dd","f_week26_return_pct","f_rsi14","f_earnings_recency","f_kpi1"],"verdict_values":{"trap":{"verdict":"🟡","label":"成長是真的，價格用的是缺貨期利潤率"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":20.6,"pe":84.95,"basis":"FY2026E 共識 EPS（當年度），終端倍數同樣套在當年度 EPS 上。"},"eps":{"bull":[45,70,88,104,122],"base":[37,50,47,52,56],"bear":[31,28,16,20,26]},"pe":{"bull":32,"base":24,"bear":18},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0.171,"net_buyback":0},"second_stage":{"bull_cagr_pct":15,"base_cagr_pct":8},"max_dd":{"lo":-85,"hi":-65,"basis":"Bear 路徑 FY2029 EPS 16 元×18–25 倍＝288–400 元，相對現價 −84%～−77%；較輕情況 EPS 20 元×30 倍＝600 元，約 −66%。上一輪下行毛利率落到 13.08%，連兩年虧損；本輪 10-12 到 11-06 已跌 42%。歷史回撤序列事實表未涵蓋。","trigger_time":null},"basis":{"bull":"產能 2027 年到位後繼續擴，CPO 放量，FY2031 營收約 288 億元、淨利率約 44%、股數約 104 百萬股。終端 32 倍，同業倍數事實表未涵蓋，以自身 FY2027 共識約 43 倍打折為錨。","base":"FY2027 EPS 低於共識約一成，反映基板與爬坡損耗；FY2029 因新產能到位而回落；FY2031 營收約 165 億元、淨利率約 35%、股數約 103 百萬股。終端 24 倍，同業倍數事實表未涵蓋。","bear":"2028 年後供給到位，疊加自製與雲端資本支出放緩，FY2029 EPS 16 元，FY2031 回到 26 元。終端 18 倍為三年後成長降至 10% 的本益比。機率 30% 依據毛利率位於高點、2023 年前例與內生上界低於共識；短缺報導的時間窗只到 2027–2028 年，與此路徑的轉折時點不衝突。"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"2023 年毛利率 13.08%、EPS −2.1 元，2024 年續虧；賣方提示 IDM 自行供應磊晶與矽光滲透慢於預期。","assumption":"新產能到位後毛利率仍守在 45% 以上。","consequence":"五年後虧損過半最可能的路徑是 2028 年起價格鬆動，毛利率往 30% 走，EPS 16–26 元、18 倍，股價約 468 元。與唯一致命點同一件事。","ruling":"採納，列 30% 機率。上一輪是中國電信客戶消失，這一輪換成雲端客戶，型態不同，但少數客戶決定營收的結構相同。","watch":"單季毛利率、磊晶片報價、月營收年增率。","evidence_refs":["cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#1","cyclical_prior_downcycle_behavior#2","cyclical_supply_discipline_capacity#3"],"fact_refs":["f_kpi1"]},{"view":"論點失敗","evidence":"股價 10-12 到 11-06 由 3,025 元跌到 1,750 元，期間有 10-28 第三季財報。基板庫存原本只看到 2026 年第三季。","assumption":"FY2027 共識 EPS 未下修，由前份門檻換算約 39.4 元升至 40.72 元，所以跌的是倍數。共識快照可能落後實際。","consequence":"若實際原因是基板斷料或毛利率下滑，本次所有路徑都偏高。","ruling":"不可裁決，要到補讀第三季財報與法說才能定。補讀前不做任何進場動作。","watch":"第三季單季毛利率、10 月至 12 月營收、公司對基板供應的說明。","evidence_refs":["supply_demand_durability#3","cyclical_inventory_price_position#2","geo_supply_chain#2"],"fact_refs":["f_earnings_recency","f_price_at_dd","f_consensus_eps_fy2"]},{"view":"論點成功但股東經濟變差","evidence":"Q2 自由現金流 −4.79 億元，設備預算約 82.7 億元，現金 49.2 億元、債務 31.7 億元。基板再漲逾一成。","assumption":"擴產資金來自營業現金流，股本不擴大。","consequence":"營收照預期翻倍，股東仍可能因增資或可轉債稀釋而少賺；每股路徑還受股數口徑 92.5 到 101.4 百萬股的影響。","ruling":"採納部分。Base 股數已用約 103 百萬股，若再對外籌資，每股路徑要下修。","watch":"淨現金、股本變動、籌資公告。","evidence_refs":["end_markets#3","cyclical_supply_discipline_capacity#0"],"fact_refs":["f_kpi4","f_net_debt_m","f_shares_diluted_m"]},{"view":"價格已反映太多","evidence":"現價約為 FY2027 共識 EPS 的 43 倍、trailing 111.54 倍，P/S 37.39 倍在 4 個年底端點中最高。","assumption":"一個月跌 42% 已提供足夠保護。","consequence":"機率加權五年價值約 1,720 元，低於現價，Base 年化約 −5%，跌幅沒有轉成安全邊際。","ruling":"採納。跌幅只修正了上份的過高定價，還沒補償 30% 的 Bear 路徑。","watch":"股價對 FY2027 共識 EPS 的倍數。","evidence_refs":["capital_markets_pricing#0"],"fact_refs":["f_pe_current","f_ps_current","f_ps_percentile","f_consensus_eps_fy2"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟢","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟢","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 3025.0 → 本次 1750.0（-42.1%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=3025.0","side_b":"本次 price_at_dd=1750.0","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 3,025 元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 3,025 元：Bull 價 4,140、Bear 價 484，五年期望值 −40.2%，基準年化 −14.3%，不對稱比 0.4","side_b":"本次情境、股價仍用 3,025 元：Bull 價 3,904、Bear 價 468，五年期望值 −43.1%，基準年化 −15.0%，不對稱比 0.29","ruling":"先換情境、股價不動：五年期望值少 2.9 個百分點，基準年化少 0.7 個百分點。不對稱比由 0.4 變為 0.29。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 3,025 元：五年期望值 −43.1%，基準年化 −15.0%，不對稱比 0.29","side_b":"本次情境、股價 1,750 元：五年期望值 −1.6%，基準年化 −5.1%，不對稱比 1.4","ruling":"再換股價、情境不動：起點價下跌 42.1%，五年期望值多 41.5 個百分點，基準年化多 9.8 個百分點，不對稱比由 0.29 升到 1.4。合計五年期望值比前份多 38.6 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"缺貨延續與循環晚期的時間窗","cause":null,"prior_field":null,"side_a":"TrendForce 等來源稱 InP 短缺延續到 2027 年之後，Lumentum 據稱雷射產能訂到 2028 年。","side_b":"毛利率 57.45% 為事實表四個年度內最高，Coherent 將兩度倍增產線，聯亞 2027 年產能放大 2.5 倍，2023 年毛利率曾落到 13.08%。","ruling":"可調和，屬時間窗差異。2027 年以前採信缺貨，2028 年以後採信供給回補，所以 Base 在 FY2029 回落，Bear 機率維持 30%。","evidence_level":"中，缺貨多為二手轉述，歷史財務為一手資料。","settle_metric":"單季毛利率與磊晶片報價。","if_then":["若 2027 年底前單季毛利率仍 ≥55% 且磊晶片續漲，Bear 機率下調至 25%","若任一季毛利率跌破 45%，已持有者清倉，未持有者取消進場條件"],"evidence_refs":["supply_demand_durability#0","supply_demand_durability#5","cyclical_supply_discipline_capacity#2","cyclical_prior_downcycle_behavior#0"]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"一個月跌 42%，RSI 28.01，股價貼著 52 週線且在 104 週線之上。FY2027 共識本益比由約 77 倍降到約 43 倍，共識 EPS 沒有下修。Bull 五年 3,904 元，約為現價 2.2 倍。","side_b":"現價略高於機率加權價值約 1,720 元，Base 年化約 −5%。下跌原因與 10-28 財報內容都不在手上，不能把跌幅當安全邊際。","ruling":"選等價位。超賣只說明賣壓，不說明價值。本判斷比賣方悲觀，但認為目前股價大致合理，不主張市場看錯。","evidence_level":"中，第三季資料缺口未補。","settle_metric":"第三季單季毛利率與 FY2027 共識 EPS。","if_then":["價格先走、證據未到：股價回到 2,000 元以上而第三季毛利率仍未確認，不追","跌到約 1,425 元以下且單季毛利率 ≥50%，重做研究後分批反買，首倉不超過 3%","反向條件：股價未跌到 1,425 元，但 FY2027 共識 EPS 上修至 55 元以上且毛利率 ≥55%，重做情境樹，進場價按 35 倍上移"],"evidence_refs":["capital_markets_pricing#2","end_markets#4"]},{"axis":"賣方目標價與本判斷","cause":null,"prior_field":null,"side_a":"Investing.com 10 位分析師平均目標價 3,136 元，最高 4,500 元、最低 900 元，最新評等動作在 8 月。","side_b":"本判斷 Base 五年 1,344 元，機率加權約 1,720 元。","ruling":"分歧在框架層。平均目標價約等於 FY2027 共識 EPS 的 77 倍，等於把缺貨期利潤率當常態，再給成長股倍數。高低目標價相差 5 倍，快照也早於這波下跌，不拿來當支撐。","evidence_level":"低，快照日期不明，TradingView 另一組 469 元疑為過期資料。","settle_metric":"FY2027 共識 EPS 與實際毛利率。","if_then":["若賣方在第三季財報後下修 FY2027 EPS 逾 10%，Base 路徑同步下移，進場價按 35 倍重算"],"evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#3"]},{"axis":"產業態勢三軸","cause":null,"prior_field":null,"side_a":"競爭：IDM 自製與 Coherent、Lumentum 擴產，壓力在 2027 年後上升。","side_b":"結構：資料中心矽光需求推動 InP 短缺，客戶數增至 10 家以上。其他：基板出口管制與報價上漲。","ruling":"雙向拉鋸。需求結構轉好與未來供給增加同時成立，目前證據不足以判哪邊先到。","evidence_level":"中。","settle_metric":"客戶數、磊晶片報價、自製相關報導。","if_then":["若 2027 年客戶數低於 10 家或傳出主要客戶自製，改判競爭惡化中，Bull 機率降到 15%"],"evidence_refs":["cyclical_supply_discipline_capacity#3","competitive_share_entrants#0","supply_demand_durability#3"]},{"axis":"估值結論因股價下跌而改善","cause":"價格變動","prior_field":["val","max_dd_pct","p_bull_pct","p_bear_pct"],"side_a":"前份：3,025 元，約 FY2027 共識 EPS 77 倍，估值最貴一檔，Bull 25%、Bear 30%、最大回撤 −85%。","side_b":"本次：1,750 元，約 43 倍，估值降一檔到偏貴，Bull 25%、Bear 30% 不變，最大回撤範圍 −85%～−65%。","ruling":"改善全部來自價格，基本面假設沒有變，所以機率不動。","evidence_level":"高，價格與共識為事實表數字。","settle_metric":"股價對 FY2027 共識 EPS 的倍數。","if_then":["若股價回到 FY2027 共識 EPS 60 倍以上（約 2,440 元），估值回到最貴一檔，已持有者減碼一半"],"evidence_refs":[]},{"axis":"基本面判斷維持不變","cause":"新證據","prior_field":["signal","trap","moat_trend","runway_post_y5","archetype","cycle_position"],"side_a":"前份：觀望，循環晚期，護城河穩定，五年後空間中等，陷阱風險中等。","side_b":"本次資料：Q2 毛利率 57.45%，FY2027 共識 EPS 由約 39.4 元升至 40.72 元，客戶數增至 10 家以上，2027 年產能 2.5 倍；同時 Q2 自由現金流為負，第三季內容缺漏。","ruling":"新證據方向互抵，沒有一項足以改判，這八欄全部維持。循環位置看毛利率與供給，不看股價，所以跌 42% 不會讓位置提前。","evidence_level":"中。","settle_metric":"第三季毛利率與 2027 年產能進度。","if_then":["若第三季毛利率低於 50%，陷阱風險升到最高一檔並重做研究"],"evidence_refs":["competitive_share_entrants#0","cyclical_supply_discipline_capacity#0"]},{"axis":"重新進場門檻（首倉進場）更新","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"股價回落至 FY2027 共識 EPS 35 倍以下（約 1,380 元）且單季毛利率仍 ≥50%","side_b":"股價回落至 FY2027 共識 EPS 35 倍以下（約 1,425 元）且單季毛利率仍 ≥50%","ruling":"倍數與毛利率條件不變，只因 FY2027 共識 EPS 上升，換算進場價上移約 45 元。前份門檻至今未觸發，現價 1,750 元仍高出新門檻約 23%。","evidence_level":"高。","settle_metric":"收盤價、FY2027 共識 EPS、單季毛利率。","if_then":["達到新門檻時先重做研究再分批進場，不直接建倉"],"evidence_refs":[]},{"axis":"Single Thing 與清倉指標首次明列","cause":"方法變動","prior_field":["single_thing","kill_metrics"],"side_a":"前份摘要此欄為 null，無原文。","side_b":"任一季毛利率跌破 45%，而當季營收仍年增。","ruling":"前份摘要沒有這兩欄可比，本次新訂，無法判斷是否比前份放寬。","evidence_level":"不適用。","settle_metric":"單季毛利率。","if_then":["發生時已持有者清倉，未持有者取消進場條件"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"補讀 10-28 的第三季財報與法說，確認毛利率、基板供應與這波下跌的原因。","type":"假設驗證","maps_to":"H1","metric":"2026 年第三季單季毛利率","threshold":"≥50% 維持現有判斷，<50% 重做研究","action":"補齊資料前不做任何進場動作","source_freq":"公開資訊觀測站季報，一次性","date":"2026-11-30","evidence_refs":["cyclical_inventory_price_position#2"]},{"n":2,"text":"股價回到 FY2027 共識 EPS 35 倍以下，且單季毛利率仍在 50% 以上。","type":"估值rearm","maps_to":"H2","metric":"股價÷FY2027 共識 EPS；單季毛利率","threshold":"≤35 倍（約 1,425 元）且毛利率 ≥50%","action":"重做研究後分批反買，首倉不超過 3%","source_freq":"收盤價每日，毛利率每季","date":null},{"n":3,"text":"下半年營收要達到全年共識所需的水準。","type":"假設驗證","maps_to":"H1","metric":"2026 下半年累計營收","threshold":"≥33.7 億元（全年共識 54.9 億元減上半年 21.26 億元）","action":"低於門檻則下調 FY2027 Base EPS 並重算進場價","source_freq":"月營收，每月","date":"2027-01-10"},{"n":4,"text":"任一季毛利率跌破 45%，而當季營收仍年增。","type":"Single Thing","maps_to":"Single Thing","metric":"單季毛利率","threshold":"<45% 且當季營收年增","action":"已持有者清倉，未持有者取消進場條件","source_freq":"季報，每季","date":null,"evidence_refs":["cyclical_prior_downcycle_behavior#0"]},{"n":5,"text":"基板斷料影響出貨。","type":"風險","maps_to":"R1","metric":"單季營收季增率與公司對基板的說明","threshold":"季減 ≥10% 且公司歸因基板","action":"已持有者減碼一半，未持有者不進場","source_freq":"月營收與法說","date":null,"evidence_refs":["supply_demand_durability#3","geo_supply_chain#2"]},{"n":6,"text":"擴產資金轉為對外籌資或淨現金轉負。","type":"風險","maps_to":"R5","metric":"淨現金與股本變動","threshold":"淨現金 <0，或股本年增 ≥5%","action":"每股路徑按新股本下修，已持有者停止加碼","source_freq":"季報與重大訊息","date":null},{"n":7,"text":"股價回升到過高倍數而毛利率沒有再上行。","type":"減碼","maps_to":"H2","metric":"股價÷FY2027 共識 EPS；單季毛利率","threshold":"≥60 倍（約 2,440 元）且毛利率未創新高","action":"已持有者減碼一半","source_freq":"收盤價每日，毛利率每季","date":null},{"n":8,"text":"3.2T 量產與客戶廣度驗證。","type":"假設驗證","maps_to":"H3","metric":"3.2T 量產進度與客戶家數","threshold":"2027 年底前未量產，或客戶低於 10 家","action":"Bull 機率由 25% 降到 15%","source_freq":"法說，每季","date":"2027-12-31"},{"n":9,"text":"FY2026 年報與第四季法說後複審。","type":"複審日期","maps_to":"H1","metric":"全份判斷","threshold":"屆期必做","action":"重跑情境樹並更新進場價","source_freq":"年報","date":"2027-03-31"}],"kill_metrics":[{"metric":"單季毛利率","bear_threshold":"<45%","window":"任一季","source":"公開資訊觀測站季報與法說","last_status":"ok"},{"metric":"FY2027 共識 EPS","bear_threshold":"<35 元","window":"3 個月內","source":"yfinance 分析師共識","last_status":"ok"},{"metric":"月營收年增率","bear_threshold":"連 3 個月 <30%","window":"連續 3 個月","source":"公開資訊觀測站月營收","last_status":"ok"},{"metric":"淨現金","bear_threshold":"<0","window":"連 2 季","source":"季報資產負債表","last_status":"ok"},{"metric":"2027 年產能倍數","bear_threshold":"<2 倍（指引 2.5 倍）","window":"2027 年底前","source":"公司法說","last_status":"unknown"}],"evidence_dismissed":[],"action_conditions":{"rearm_trigger":"股價回落至 FY2027 共識 EPS 35 倍以下（約 1,425 元）且單季毛利率仍 ≥50%","exec_line":"未持有：不追，等約 1,425 元且單季毛利率 ≥50%，重做研究後分三批進場。已持有：不加碼，反彈到約 2,440 元減碼一半，單季毛利率跌破 45% 清倉。","holding_cap":"首倉不超過 3%"}},"decision_inputs":{"signal":"C","ma":"🟢","cycle_position":"晚循環","cycle_verdict":"等回踩","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":false,"qc49_inherit_prior":true,"wait_for_price":true,"wait_for_price_condition":"股價回落至 FY2027 共識 EPS 35 倍以下（約 1,425 元）且單季毛利率 ≥50%；達到後先重做研究再分批。","prior_verdict":"觀望","prior_role":"追蹤"},"thesis":{"H":[{"id":"H1","text":"2027 年產能放大能兌現成獲利，FY2027 營收與 EPS 接近共識。","2y":"FY2027 營收 ≥90 億元、EPS ≥35 元","5y":null,"10y":null,"threshold":"FY2027 營收 ≥90 億元且 EPS ≥35 元（共識 101.2 億元、40.72 元）","source":"公開資訊觀測站月營收與季報，法說的產能進度","drift_rule":"TTM 營收對本路徑連 2 季偏離 ≥5% 為削弱，連 3 季偏離 ≥10% 為反轉"},{"id":"H2","text":"新產能到位後毛利率守得住，證明不是單純的缺貨行情。","2y":null,"5y":"FY2029 至 FY2031 年度毛利率 ≥45%","10y":null,"threshold":"年度毛利率 ≥45%（Q2 2026 為 57.45%，2023 年為 13.08%）","source":"季報與年報","drift_rule":"連 4 季低於門檻 5 個百分點以上為削弱，連 6 季低於 10 個百分點以上為反轉"},{"id":"H3","text":"開放式 InP 磊晶片龍頭地位與客戶廣度維持，3.2T 順利接棒。","2y":null,"5y":"開放式磊晶份額 ≥50%，客戶 ≥10 家，3.2T 進入量產","10y":null,"threshold":"份額 ≥50%（目前單一報告稱逾 60%）且客戶 ≥10 家","source":"Digitimes 等產業報告、公司法說","drift_rule":"連 4 季未見 3.2T 量產或客戶數下降為削弱，連 6 季份額資料低於 50% 為反轉"}],"R":[{"id":"R1","text":"InP 基板斷料：中國出口管制延續，庫存緩衝原本只看到 2026 年第三季。","h_ref":"H1","clock":"⚡","threshold":"單季營收季減 ≥10% 且公司歸因基板，或單季毛利率 <50%","evidence_refs":["supply_demand_durability#3","cyclical_inventory_price_position#2","geo_supply_chain#2"]},{"id":"R2","text":"新產能與自製同時到位：同業擴產、IDM 自行供應磊晶，矽光滲透慢於預期。","h_ref":"H2","clock":"🔥","threshold":"磊晶片報價轉跌，或單季毛利率連 2 季年減","evidence_refs":["cyclical_supply_discipline_capacity#3"]},{"id":"R3","text":"上一輪下行重演：中國電信客戶幾乎消失時，月營收年減 74%，毛利率落到 13%，連兩年虧損。","h_ref":"H2","clock":"🔥","threshold":"月營收連 3 個月年增低於 30%","evidence_refs":["cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#1","cyclical_prior_downcycle_behavior#2"]},{"id":"R4","text":"客戶與地區集中：2025 年底三家客戶占應收帳款 74%，銷售市場中國占 71%。","h_ref":"H3","clock":"🔥","threshold":"前三大客戶占應收 ≥80%，或出現主要客戶轉第二來源的報導","evidence_refs":["customer_concentration_credit#0"]},{"id":"R5","text":"擴產資金壓力：Q2 自由現金流 −4.79 億元，設備預算約 82.7 億元，高於帳上現金 49.2 億元。","h_ref":"H1","clock":"🔥","threshold":"淨現金轉為淨負債，或股本年增 ≥5%","evidence_refs":[]}],"single_thing":{"description":"任一季毛利率跌破 45%，而當季營收仍年增，代表是價格鬆動，不是需求消失。","why_fatal":"終端 EPS 對毛利率最敏感：FY2031 Base 營收約 165 億元，毛利率每少 5 個百分點，稅後少約 6.8 億元，EPS 少約 6.6 元，約占 12%。同時市場會改用循環股倍數，Base 的 24 倍往 Bear 的 18 倍靠。","if_happens":"已持有者清倉；未持有者取消進場條件，等毛利率連兩季回升再重做研究。","how_monitor":"每季財報毛利率、每月營收、基板與磊晶片報價的產業報導。","probability":"12–24 個月內約 25%"}},"appendix_a":{"growth_durability":5,"quality_score":6,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":42.98,"peg_fy2":3.94,"stress":{"pass":1,"total":3}},"eps_meta":{"base_eps_path":{"FY2025A":4.21,"FY2026E":20.6,"FY2027E":40.72,"FY2028E":null},"fy_end_month":12,"eps_basis":"FY2025A 為 yfinance 稀釋 EPS，FY2026E、FY2027E 為 yfinance 分析師共識平均；FY2028 共識事實表未涵蓋，留空，不自行推估。"},"catalysts":[{"date":"2026-11-10","date_precision":"month","type":"other","event":"10 月營收公告，為第四季第一個數據點","impact":"中","watch":"年增率與月增率，對照下半年 33.7 億元的需求"},{"date":"2026-12-31","date_precision":"quarter","type":"other","event":"InP 基板第四季是否再漲逾一成，磊晶片是否第三度漲價","impact":"中","watch":"漲價能否完全轉嫁，毛利率方向"},{"date":"2027-03-31","date_precision":"quarter","type":"guidance","event":"FY2026 年報與第四季法說","impact":"高","watch":"毛利率、2027 年產能進度、資本支出與籌資安排"},{"date":"2027-12-31","date_precision":"quarter","type":"capacity","event":"2027 年產能達 2026 年 2.5 倍的指引驗收","impact":"高","watch":"實際產能倍數、產能利用率、報價是否鬆動"},{"date":null,"date_precision":null,"type":"product","event":"3.2T 進入量產，公司未給時程","impact":"中","watch":"法說揭露的客戶驗證進度"}],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"6","pacing":[],"holding_cap":null,"audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='C'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟢'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":true,"basis":"signal='C'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='C', runway='🟡', val='🟠', moat_trend='→', week26=-26.4, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='循環/商品', cycle_position='晚循環', moat='B', moat_trend='→', cycle_gates_pass=False"},{"row":"6/7/7a-verdict","condition":"Soft Veto 生效 → 觀望（max-severity wins；8a/8b 未能繞過）","hit":true,"basis":"soft_veto_rows=['6']"},{"row":"QC-49","condition":"qc49_inherit_prior=True 但前次裁決與矩陣機械輸出方向相同，無需承繼","hit":false,"basis":"prior_verdict='觀望', 矩陣機械輸出='觀望'"},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"requires_critic":[]}}
```

---

## ⑤ 覆蓋面（程式判定，你回的 ⑤ 燈號會被覆寫）

燈號 🟡：非核心軸無證據：customer_second_source（客戶 second-source 與 in-house）（尾部風險或事件型，不擋）。

⑤ 的 reason 只需評論：空軸的查詢詞是否切題、判斷有沒有交代缺口對結論的影響。

---

## 尾段：回覆格式

只回一個 JSON 陣列，①–⑧ 每條一個元素，八個全出，不得跳號、不得多列，陣列外不得有任何文字（不加前言、不加 markdown 圍欄、不加附註）：

```json
[{"item": "①", "light": "🔴|🟡|🟢", "judgment_path": "$.路徑", "reason": "一句話"}]
```
