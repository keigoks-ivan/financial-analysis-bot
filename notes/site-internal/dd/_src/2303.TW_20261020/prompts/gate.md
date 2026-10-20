你是 DD 管線 v20 的判斷層閘（gate），標的 2303.TW（20261020）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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
<!-- 2026-10-20 ⑤ 改程式判定，與來源 gate_contract §⑤／critic-gates 的「缺軸即 🔴」不同；重新濃縮時以本卡 ⑤ 為準 -->

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
- `f_kpi0_ifrs`（q1_business）｜合併營收（IFRS）＝68.73 NT$ billion｜期間與口徑：2Q26（季末 2026-06-30，公告於 2026-07-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：UMC 2Q26 新聞稿（BusinessWire／SEC 6-K Ex.99.6）（numbers.latest_quarter_kpis.items[0]，as_of 2Q26（季末 2026-06-30，公告於 2026-07-29））
- `f_kpi1_gaap`（q1_business）｜GAAP 營業利益＝14.95 NT$ billion｜期間與口徑：2Q26（季末 2026-06-30，公告於 2026-07-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：UMC 2Q26 新聞稿（QoQ +32.6%）；絕對值為上半年營業利益 26.23B（6-K Ex.99.1）減 2Q26 後推算，與新聞稿 QoQ 一致（numbers.latest_quarter_kpis.items[1]，as_of 2Q26（季末 2026-06-30，公告於 2026-07-29））
- `f_kpi2_gaap`（q1_business）｜GAAP 營業利益率＝21.8 %｜期間與口徑：2Q26（季末 2026-06-30，公告於 2026-07-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：UMC 2Q26 新聞稿（UMC 依 IFRS 申報，不提供 Non-GAAP 營業利益，故省略該項）（numbers.latest_quarter_kpis.items[2]，as_of 2Q26（季末 2026-06-30，公告於 2026-07-29））
- `f_kpi3`（q1_business）｜毛利率＝32.5 %｜期間與口徑：2Q26（季末 2026-06-30，公告於 2026-07-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：UMC 2Q26 新聞稿（numbers.latest_quarter_kpis.items[3]，as_of 2Q26（季末 2026-06-30，公告於 2026-07-29））
- `f_kpi4_eps`（q1_business）｜歸屬母公司淨利／EPS＝42.26 NT$ billion（EPS NT$3.39）｜期間與口徑：2Q26（季末 2026-06-30，公告於 2026-07-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：UMC 2Q26 新聞稿；含約 NT$30B 投資與股利等業外收益，非本業（numbers.latest_quarter_kpis.items[4]，as_of 2Q26（季末 2026-06-30，公告於 2026-07-29））
- `f_kpi7`（q1_business）｜晶圓出貨量／產能利用率＝85 % 利用率（晶圓出貨 QoQ +10.6%）｜期間與口徑：2Q26（季末 2026-06-30，公告於 2026-07-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：UMC 2Q26 新聞稿／6-K Ex.99（利用率 85%、出貨 QoQ +10.6% 為 CEO 原話）（numbers.latest_quarter_kpis.items[7]，as_of 2Q26（季末 2026-06-30，公告於 2026-07-29））
- `f_kpi8_3q26`（q1_business）｜管理層 3Q26 指引＝晶圓出貨高個位數成長；美元 ASP 持平；毛利率中 30% 區間；產能利用率 90%+；2026 資本支出 US$2.0B｜期間與口徑：2Q26 法說（公告於 2026-07-29），指引期間 3Q26／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：UMC 2Q26 新聞稿 outlook（6-K Ex.99；晶圓出貨高個位數成長、美元 ASP 持平偏穩、毛利率中 30% 區間、利用率 90%+、2026 資本支出 US$2.0B；無數值區間）（numbers.latest_quarter_kpis.items[8]，as_of 2Q26 法說（公告於 2026-07-29），指引期間 3Q26）
- `f_peer_2303_tw_gross_margin_pct`（q2_moat）｜2303.TW 毛利率＝30.6 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.2303.TW.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_2303_tw_operating_margin_pct`（q2_moat）｜2303.TW 營業利益率＝20.13 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.2303.TW.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_2303_tw_fcf_margin_pct`（q2_moat）｜2303.TW FCF 利潤率＝23.64 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.2303.TW.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_gfs_gross_margin_pct`（q2_moat）｜GFS 毛利率＝27.14 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.GFS.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_gfs_operating_margin_pct`（q2_moat）｜GFS 營業利益率＝11.59 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.GFS.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_gfs_fcf_margin_pct`（q2_moat）｜GFS FCF 利潤率＝11.47 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.GFS.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_5347_two_gross_margin_pct`（q2_moat）｜5347.TWO 毛利率＝29.41 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.5347.TWO.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_5347_two_operating_margin_pct`（q2_moat）｜5347.TWO 營業利益率＝17.02 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.5347.TWO.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_5347_two_fcf_margin_pct`（q2_moat）｜5347.TWO FCF 利潤率＝-94.76 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.5347.TWO.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝7.15 TWD/share｜期間與口徑：2026-10-20／yfinance 分析師共識平均（Koyfin 快照無此檔）；幣別同報價｜kind：estimate
  - 來源：yfinance earnings_estimate（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-10-20）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝7.32 TWD/share｜期間與口徑：2026-10-20／yfinance 分析師共識平均（Koyfin 快照無此檔）；幣別同報價｜kind：estimate
  - 來源：yfinance earnings_estimate（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-10-20）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝283759.09 TWD m｜期間與口徑：2026-10-20／yfinance revenue_estimate 0y 平均（21 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-10-20）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝349544.22 TWD m｜期間與口徑：2026-10-20／yfinance revenue_estimate +1y 平均（21 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-10-20）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi5`（q4_capital）｜自由現金流（營業現金流−資本支出）＝24.22 NT$ billion｜期間與口徑：2Q26（季末 2026-06-30，財報公告 2026-07-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：yfinance quarterly_cashflow（營業現金流 33.70B − 資本支出 9.48B）；新聞稿未揭露 FCF（numbers.latest_quarter_kpis.items[5]，as_of 2Q26（季末 2026-06-30，財報公告 2026-07-29））
- `f_kpi6_sbc`（q4_capital）｜SBC 占營業利益＝1.6 %｜期間與口徑：2Q26（季末 2026-06-30，公告於 2026-07-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：yfinance quarterly_cashflow SBC 0.240B ÷ 營業利益 14.95B；新聞稿未揭露 SBC（numbers.latest_quarter_kpis.items[6]，as_of 2Q26（季末 2026-06-30，公告於 2026-07-29））
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝-83941.98 TWD m｜期間與口徑：2026-10-20／yfinance 最新一季：總債務 63449.88、現金 147391.86（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-10-20）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝2.006 %｜期間與口徑：2026-10-20／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-10-20）
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝130.0 TWD｜期間與口徑：2026-10-20（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-10-20（RTH 收盤，UTC））
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝19.73 x｜期間與口徑：2026-10-20（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-10-20（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝100.0 %｜期間與口徑：2026-10-20（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-10-20（RTH 收盤，UTC））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝6.5 x｜期間與口徑：2026-10-20（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-10-20（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝100.0 %｜期間與口徑：2026-10-20（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-10-20（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝6.17 x｜期間與口徑：2026-10-20（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-10-20（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝100.0 %｜期間與口徑：2026-10-20（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-10-20（RTH 收盤，UTC））
- `f_ev_s_fwd`（q5_valuation）｜EV/S（EV ÷ FY1 共識營收）＝5.45 x｜期間與口徑：2026-10-20／f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）｜kind：estimate
  - 來源：—（numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m，as_of 2026-10-20）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝73.52 %｜期間與口徑：2026-10-20（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^TWII｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-10-20（RTH 收盤，UTC））
- `f_rsi14`（q5_valuation）｜RSI(14)＝35.39｜期間與口徑：2026-10-20（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-10-20（RTH 收盤，UTC））
- `f_ma_w52`（q5_valuation）｜52 週均線＝94.0 TWD｜期間與口徑：2026-10-20／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-10-20）
- `f_ma_w250`（q5_valuation）｜250 週均線＝52.23 TWD｜期間與口徑：2026-10-20／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-10-20）

### findings_digest 中方向為負或來源衝突的條目（8 條）
- `competitive_share_entrants#0`（competitive_share_entrants｜方向 -｜狀態 ok）：工商時報報導點名世界先進、中芯持續擴充28~90奈米成熟製程產能，對聯電形成競爭壓力（搜尋摘要轉述，未取得逐字原文）
  - 來源：工商時報 wantrich.chinatimes.com（as_of 2025-12-07）｜affects：moat_trend、decision_inputs.bear
- `competitive_share_entrants#1`（competitive_share_entrants｜方向 -｜狀態 ok）：聯電2026年1月法說會後股價兩日跌逾17%；報導指中國晶圓代工廠競爭讓聯電在漲價上趨保守（搜尋摘要轉述，未取得逐字原文）
  - 來源：TechNews 財經（as_of 2026-02-07）｜affects：moat_trend、valuation
- `competitive_share_entrants#2`（competitive_share_entrants｜方向 -｜狀態 ok）：聯電要求供應商2026年降價至少15%，市場解讀為中芯、華虹、力積電、世界先進擴充28-90奈米造成供過於求
  - 來源：TechNews（as_of 2025-10-02）｜affects：moat_trend、decision_inputs.bear
- `customer_concentration_credit#0`（customer_concentration_credit｜方向 -｜狀態 ok）：114年（2025）年報揭露占營業收入10%以上的客戶僅一家（甲，與發行人無關係），金額28,005,843千元、占營收12%；113年同一欄為24,180,535千元、占10%。營收總額114年237,553,199千元。
  - 來源：公開資訊觀測站電子書件 114年股東會年報 主要銷貨客戶表（PDF第46頁）（as_of 2026-05-06）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：聯電管理層於2025年7月法說指出匯率與美國關稅政策可能變動為近期風險（Benzinga 報導）
  - 來源：Benzinga: United Microelectronics Chief Cautions Currency, Trade Policy Could Dampen Gains（as_of 2025-07-30）｜affects：decision_inputs.bear、thesis.R
- `reg_tariff_export#1`（reg_tariff_export｜方向 -｜狀態 ok）：2018年美國商務部將福建晉華列入實體清單後，聯電暫停與晉華的技術合作開發（出口管制先例）
  - 來源：搜尋結果：聯電晉華案報導（經濟部國貿局函令）（as_of 2018-10-30）｜affects：decision_inputs.bear
- `reg_tariff_export#2`（reg_tariff_export｜方向 -｜狀態 ok）：凱基報告：台積電認為關稅成本應由客戶承擔，聯電表示與客戶密切合作減輕影響；二線代工在232豁免較不利
  - 來源：KGI semiconductor sector 2025-08-07（as_of 2025-08-07）｜affects：decision_inputs.bear、thesis.R
- `capital_markets_pricing#1`（capital_markets_pricing｜方向 -｜狀態 ok）：元大投顧提醒約65%的第二季獲利來自業外收益，折舊費用增加可能侵蝕毛利改善。
  - 來源：工商時報 ctee.com.tw（as_of 2026-07-30）｜affects：valuation、decision_inputs.bear

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 4 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/private/tmp/claude-501/-Users-ivanchang/a978d205-f43a-402f-b092-0cf4aef45f19/scratchpad/wp1-publish/.dd_build/runs/2303.TW_20261020/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":194.4,"bear_5y_price":54.6,"p_bull_pct":25,"p_bear_pct":30,"upside_5y_pct":-19.2,"ev5y_pct":-13.7,"irr_base_pct":-4.2,"asym_ratio":0.7,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":7.15,"pe":18.18,"basis":"FY1（FY2026E）共識 EPS，含上半年業外收益；終端倍數套在 FY2031E 全年 EPS，同為會計年度 IFRS EPS 口徑"},"eps":{"bull":[7.6,8.5,9.3,10.0,10.8],"base":[6.4,6.9,6.0,6.4,7.0],"bear":[5.6,4.6,3.4,3.6,3.9]},"pe":{"bull":18,"base":15,"bear":14},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":2.006,"net_buyback":0},"second_stage":{"bull_cagr_pct":6,"base_cagr_pct":3},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### 2303.TW_Q1_2026_Earnings_Call_20260429.md
- 2026-04-29｜Chi-Tung Liu｜guidance：Q2 出貨成長高個位數（原話："Our wafer shipment will increase by high single digits"）
- 2026-04-29｜Chi-Tung Liu｜guidance：Q2 美元 ASP 成長低個位數（原話："ASP in U.S. dollar terms will increase by low single digits"）
- 2026-04-29｜Chi-Tung Liu｜guidance：Q2 毛利率指引約 30%（原話："Gross margin will be approximately 30%"）
- 2026-04-29｜Chi-Tung Liu｜guidance：全年資本支出維持約 15 億美元（原話："we will maintain around $1.5 billion budget"）
- 2026-04-29｜Chi-Tung Liu｜guidance：下半年將調漲晶圓價格，已發信客戶（原話："wafer price adjustment in the second half of 2026"）
- 2026-04-29｜Chi-Tung Liu｜guidance：Q2 ASP 上升主要來自產品組合（原話："mainly from the mix improvement"）
- 2026-04-29｜Chi-Tung Liu｜guidance：漲價信未寫具體數字（原話："anything numerical in our letter to customers"）
- 2026-04-29｜Chi-Tung Liu｜guidance：下半年 22nm 與嵌入式 HV 較上半年高十幾％成長（原話："where we expect to grow in the high-teen percentage range"）
- 2026-04-29｜Chi-Tung Liu｜guidance：總體半導體產業 2026 預估中十幾％成長（原話："projected now to grow by mid-teens in 2026"）
- 2026-04-29｜Chi-Tung Liu｜guidance：UMC 可服務市場仍為低個位數成長，僅略優於上季預測（原話："still grew by the low single-digit percentage"）
- 2026-04-29｜Chi-Tung Liu｜guidance：定價展望較上季略好（原話："is slightly better than the previous quarter"）
- 2026-04-29｜Chi-Tung Liu｜margin：折舊仍在增加週期高峰（原話："we're still in the peak of our depreciation increase cycle"）
- 2026-04-29｜Chi-Tung Liu｜margin：出貨增加的毛利貢獻被折舊與公用事業成本抵銷（原話："largely offset by the higher depreciation"）
- 2026-04-29｜Chi-Tung Liu｜margin：新加坡廠下半年起實質放量並帶來折舊（原話："fab in Singapore ramp-up will start in meaningful terms"）
- 2026-04-29｜Chi-Tung Liu｜margin：管理層對 EBITDA margin 口徑較有把握，未量化（原話："I will be more comfortable talking about a better upside"）
- 2026-04-29｜Chi-Tung Liu｜margin：Q1 ASP 下滑歸因於 8 吋出貨優於預期（原話："mainly due to a better-than-expected inch wafer shipment"）
- 2026-04-29｜Chi-Tung Liu｜product：22nm 營收創高（原話："22-nanometer revenue now reached another record high"）
- 2026-04-29｜Chi-Tung Liu｜product：年底前超過 50 家客戶完成 22nm 投片（原話："over 50 customers will have complete tape-out"）
- 2026-04-29｜David Wong｜product：先進封裝 2026 預期超過 35 次新投片（原話："we expect more than 35 new tape-outs in 2026"）
- 2026-04-29｜David Wong｜product：先進封裝明年營收預期顯著提高（原話："advanced packaging next year will be significantly higher"）
- 2026-04-29｜David Wong｜product：矽光子 PDK 1.0 預計 2027 交付（原話："we're on track to deliver our PDK 1.0 in 2027"）
- 2026-04-29｜Chi-Tung Liu｜product：Q2 通訊回升由 DDI、網通、FPGA、ISP 帶動（原話："driven by DDI, networking, FPGA and ISP"）
- 2026-04-29｜Chi-Tung Liu｜customer：Q1 消費性成長來自 WiFi 與 DTV 機上盒（原話："mainly driven by WiFi and DTV set-top box segment"）
- 2026-04-29｜Chi-Tung Liu｜competition：降低大宗商品化市場曝險（原話："UMC will certainly try to scale down our exposures"）
- 2026-04-29｜Chi-Tung Liu｜competition：不願被視為投機漲價（原話："being opportunist to take advantage of customers"）
- 2026-04-29｜Chi-Tung Liu｜capital_allocation：12nm 與 Intel 合作：2027 後期起初步商業量產（原話："we will start to see initial commercial production"）
- 2026-04-29｜Chi-Tung Liu｜commitment：12nm 與 Intel 合作 PDK／IP 2026 年交付（原話："remain on schedule to deliver the PDK and associated IP"）
- 2026-04-29｜Chi-Tung Liu｜commitment：承諾 2026 表現優於去年（原話："exceed last year's results"）
- 2026-04-29｜Chi-Tung Liu｜commitment：承諾 2026 成長優於可服務市場（原話："outperform the growth of our addressable market in 2026"）
- 2026-04-29｜Chi-Tung Liu｜commitment：不追逐短期機會（回應記憶體代工傳聞）（原話："we will not do short-term opportunity chase"）
- 2026-04-29｜Chi-Tung Liu｜risk：記憶體短缺與中東衝突為逆風（原話："memory supply shortage and ongoing conflict"）
- 2026-04-29｜Chi-Tung Liu｜risk：8 吋稼動率仍低於公司平均（日本廠偏低）（原話："8-inch average closing still were below corporate average"）
- 2026-04-29｜Chi-Tung Liu｜capital_allocation：新投資的風險分擔形式（是否 LTA）尚未定（原話："it's still a little bit too early to comment"）

### 問答異常語氣（迴避／改口／保留）
- 2303.TW_Q1_2026_Earnings_Call_20260429.md｜問：客戶對下半年漲價的反應、是否有抗拒，並請給漲幅假設｜答法：答「我無法代客戶發言」，改談雙贏與長期支持，未給反應或幅度
- 2303.TW_Q1_2026_Earnings_Call_20260429.md｜問：8 吋緊俏是需求或供給驅動，及 8 吋 Q1 稼動率｜答法：稱難以區分兩者，改談自身競爭力；稼動率只答全公司 79% 與 8 吋低於平均，未給數字
- 2303.TW_Q1_2026_Earnings_Call_20260429.md｜問：TSMC 談 14nm 高壓，驅動 IC 是否持續走向更小製程｜答法：答「不評論競爭對手」，改談自家 22/28 與 FinFET HV
- 2303.TW_Q1_2026_Earnings_Call_20260429.md｜問：是否能量化 EBITDA margin 改善｜答法：僅稱較有把握談上行，未量化；毛利／營業利益率則強調折舊壓力

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 3 | 4 |
| customer_second_source | none | 0 | 3 |
| customer_concentration_credit | found | 1 | 2 |
| supply_demand_durability | found | 6 | 4 |
| regulatory_antitrust | found | 2 | 3 |
| reg_tariff_export | found | 4 | 4 |
| geo_supply_chain | found | 3 | 3 |
| end_markets | found | 4 | 4 |
| substitute_technology | found | 1 | 3 |
| channel_business_model_shift | found | 3 | 3 |
| capital_markets_pricing | found | 6 | 4 |
| major_events | found | 3 | 4 |
| cyclical_supply_discipline_capacity | found | 2 | 3 |
| cyclical_inventory_price_position | found | 3 | 3 |
| cyclical_prior_downcycle_behavior | found | 1 | 2 |

未涵蓋／不適用軸的查詢詞原文（供判相關性）：
- **customer_second_source**（none）：聯電 大客戶 第二供應商 OR 轉單 2026；聯電 客戶 自製 OR 分散供應商；2303.TW United Microelectronics largest customer second source OR in-house 2026

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"status":"no_prior_dd"}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"2303.TW","date":"2026-10-20","schema":"v15.2","contract":"v19","company_name":"聯華電子"},"oneliner":"成熟製程代工正處景氣擴張段，2027 年漲價可期；但現價 130 元對核心獲利約 26–28 倍，共識 EPS 含一次性業外收益，2028 年起自家與中國新產能開出會壓回毛利，加權預期報酬為負，等價格或漲價落地再看。","facts_ref":"/private/tmp/claude-501/-Users-ivanchang/a978d205-f43a-402f-b092-0cf4aef45f19/scratchpad/wp1-publish/.dd_build/runs/2303.TW_20261020/facts.json","scenario_ref":"/private/tmp/claude-501/-Users-ivanchang/a978d205-f43a-402f-b092-0cf4aef45f19/scratchpad/wp1-publish/.dd_build/runs/2303.TW_20261020/scenario.json","answers":{"q1_business":{"verdict":"賺 IC 設計公司與 IDM 的晶圓加工費，主力是 40nm 以下的成熟與特殊製程。錢卡在產能利用率與每片價格兩個節點，折舊是大塊固定成本，所以獲利會跟著景氣放大。","reasoning":"2Q26 合併營收 687.3 億元，毛利率 32.5%，營業利益率 21.8%。利用率由 79% 升到 85%，出貨季增 10.6%。歸屬母公司淨利 422.6 億元、EPS 3.39 元，其中約 300 億元是投資與股利收入（2026-07-29 法說，財務長 Chi-Tung Liu），本業每股獲利遠低於帳面。營收結構（2Q26 法說）：40nm 以下約 52%；22/28nm 占 37%，是最大營收池，其中 22nm 占 17.5%；亞洲約 66%、北美約 22%；IDM 客戶約 15%；特殊製程約占一半營收。最大單一客戶占 114 年營收 12%（113 年 10%），沒有單點客戶依賴，但成熟製程的可替代供給多，下行期議價權在客戶手上。3Q26 指引：出貨高個位數成長、美元 ASP 持平、毛利率中 30% 區間、利用率逾 90%。產業時鐘判為擴張期，依據是營運數字而非股價：利用率連三季回升、2H26 選擇性漲價、管理層預告 2027 年價格調升會更明顯。供需持久度判為週期性將反轉：本輪緊俏來自台積電與三星減產 8 吋、AI 電源需求與庫存正常化，這些供給面因素可逆性高。","fact_refs":["f_kpi0_ifrs","f_kpi1_gaap","f_kpi2_gaap","f_kpi3","f_kpi4_eps","f_kpi7","f_kpi8_3q26"],"verdict_values":{"revenue_quality":"本業是晶圓銷售，客戶分散；但 2026 年帳面獲利含大量業外投資收益，2Q26 約六到七成淨利不是本業","unit_econ_note":"2Q26 出貨 113 萬片 12 吋約當、利用率 85%、混合 ASP 季增低個位數；3Q26 季產能約 132.5 萬片、利用率逾 90%；財務長預告折舊未來至少兩年每年增加十幾%","archetype":{"primary":"循環/商品","secondary":null,"confidence":"高","fingerprint":"成熟製程代工：利用率乘價格驅動、資本密集；2022→2025 年毛利率 45.1%→29.0%，2023 年自由現金流轉負"},"industry":{"clock_phase":"II","sd_verdict_source":"週期性將反轉：緊俏來自台積電與三星減產 8 吋（TrendForce 2026-06-30）、AI 電源需求與庫存正常化；中國與台系同業持續擴充 28–90nm，聯電自己的新加坡 P4 與台南新廠也從 2027 年底至 2028 年初起放量","bargaining":{"up":"對供應商有一定議價力：2025 年 10 月要求供應商 2026 年起降價至少 15%；但能源、矽晶圓與物流成本仍在上升","down":"客戶分散，最大客戶占營收 12%；但成熟製程有多家可替代供給，下行期價格由客戶主導","geo":"以台灣為主，新加坡是最大海外基地，另有廈門與日本三重；北美營收約 22%，232 關稅豁免對沒有美國廠的二線代工較不利"},"profit_pool_dir":"成熟製程利潤池正流向中國在地產能與擁有美國廠的同業；特殊製程（BCD 電源、矽光子、先進封裝）是聯電想搬過去的新利潤池，2028 年後才見量","tam_table":{"expanded":false,"reason":"管理層只說先進封裝可服務市場 2030 年前會翻倍、AI 相關營收 3 年內破 10 億美元，沒有給金額或滲透率；事實表未涵蓋 TAM 數字，硬展開會變成推估"}}}},"q2_moat":{"verdict":"護城河 C 級，方向持平：特殊製程組合與 12 吋矽光子在進步，但成熟製程的定價權被中國與台系擴產結構性壓著，兩者互相抵銷。","reasoning":"機制是製程認證與客戶轉換成本（特殊製程 IP、重新認證週期）加上規模，不是技術領先型。執行面在擴大：22nm 營收創新高，2026 年底前超過 50 家客戶完成 22nm 投片（2026-04-29 法說），首批 12 吋矽光子晶片量產出貨，先進封裝有逾 10 家客戶、35 個以上新產品討論中（2026-07-29 法說）。定價面結構性縮減：毛利率由 2022 年 45.1% 降到 2025 年 29.0%；2026 年 1 月市場解讀中國同業競爭讓聯電漲價趨於保守；中芯、華虹、力積電、世界先進持續擴充 28–90nm。眼前的漲價屬週期性，不是護城河加寬。同業對照：TTM 營業利益率聯電 20.1%、格芯 11.6%、世界先進 17.0%，目前聯電領先，但同業 ROIC 與利差歷史事實表未涵蓋，無法判斷利差方向。","fact_refs":["f_peer_2303_tw_gross_margin_pct","f_peer_2303_tw_operating_margin_pct","f_peer_2303_tw_fcf_margin_pct","f_peer_gfs_gross_margin_pct","f_peer_gfs_operating_margin_pct","f_peer_gfs_fcf_margin_pct","f_peer_5347_two_gross_margin_pct","f_peer_5347_two_operating_margin_pct","f_peer_5347_two_fcf_margin_pct"],"verdict_values":{"moat":{"mechanism":"製程認證與客戶轉換成本（特殊製程 IP、重新認證週期）加上 12 吋成熟製程規模；先進製程只靠 Intel 12nm 合作，2028 年才有意義的量","execution":7,"pricing":5,"grade":"C","trend":"→","trend_evidence":"執行力擴大：22nm 創新高、12 吋矽光子首批量產、先進封裝客戶增加。定價權縮減：2022→2025 年毛利率近乎腰斬，同業持續擴充 28–90nm，2026 年初漲價保守。兩者相抵判持平；目前營業利益率高於格芯與世界先進，但利差歷史事實表未涵蓋","competitor_notes":[{"name":"GFS","strategy_note":"毛利率 27.1%、營業利益率 11.6%，都低於聯電；但有美國本土產能，關稅豁免下是北美客戶的替代選項"},{"name":"5347.TWO","strategy_note":"營業利益率 17.0%，接近聯電；FCF 利潤率 −94.8% 反映正在大舉投資新廠，持續擴充同類成熟製程，是最直接的產能競爭者"},{"name":"0981.HK","strategy_note":"事實表沒有利潤率資料；被點名持續擴充 28–90nm，在中國客戶在地化需求下壓抑成熟製程價格"}],"peer_na_reason":"中芯營收欄缺失，無法算利潤率；同業 ROIC 事實表未涵蓋，改用營業利益率差作可比軸","threats":[{"level":"🔴","text":"中國（中芯、華虹）與台系（世界先進、力積電）持續擴充 28–90nm，造成成熟製程供過於求；這是生態層的價格攻擊，會在 2028 年後聯電自身新產能開出時疊加","p":"40%","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#2"]},{"level":"🟡","text":"中國同業競爭讓聯電在漲價上趨於保守，2026 年 1 月法說後股價兩日跌逾 17%；2027 年合約價若被壓回，週期性漲價也會落空","p":"35%","evidence_refs":["competitive_share_entrants#1"]},{"level":"🟡","text":"美國 232 半導體關稅的豁免條件偏向已在美設廠的一線代工，聯電屬二線，北美客戶（約 22% 營收）有轉單誘因","p":"30%","evidence_refs":["reg_tariff_export#2"]}],"roic_durability":{"quadrant":"高利益率×低周轉","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"電源管理、MCU、感測器、連網晶片屬於需要而非想要，AI 資料中心帶動電源與連網需求；但管理層承認手機、PC、筆電今年年減，非 AI 需求不均，本輪不是全面復甦（2026-07-29 法說）"},{"item":"決策層級","level":"🟡","text":"替代發生在單一產品、單一製程的投片決策：成熟製程換廠要重新認證，有一定成本；特殊製程（BCD、嵌入式高壓、矽光子）的轉換成本較高，占營收約一半。客戶有多少比例另有第二供應來源或自行生產，事實表未涵蓋，所以這一格不判綠也不判紅。定價權給 5 分，依據是 2022→2025 年毛利率由 45.1% 降到 29.0% 的實際結果，不靠這一格；這一軸查不到，不改變護城河 C 級與持平的結論"},{"item":"價值鏈分配","level":"🔴","text":"成熟製程供給者多，下行期利潤流向客戶：2022→2025 年毛利率由 45.1% 降到 29.0%；上游矽晶圓、能源成本又在上升，只能靠要求供應商降價 15% 自保，可見這個環節在價值鏈中最容易被擠壓"},{"item":"社會容忍度","level":"🟢","text":"晶圓代工不是消費必需品，沒有價格管制，也不依賴監管授權；政策風險在關稅與出口管制，已列入風險清單"}],"roiic":"2022→2025 年為負：營業利益由約 1,036 億元降到 437 億元，期間仍持續投資新加坡 12i 新廠；新一輪 50 億美元投資的前瞻增量報酬事實表未涵蓋","reinvest_rate":"毛額上界約 74%：2Q26 資本支出 94.8 億元 ÷ 稅後營業利益約 127.4 億元（營收 687.3 億元×營業利益率 21.8%×（1−15% 稅率假設））。折舊事實表未涵蓋，無法扣成淨再投資，真實淨再投資率低於此值；反方向，2026 年資本支出已由 15 億上修到 20 億美元，下半年單季資本支出可能高於 2Q26。方向上升：董事會核准約 50 億美元於 2026–27 年投入","endo_ceiling":7,"formula_note":"當期 ROIC 粗估約 12%：TTM 營業利益率 20.1%×（1−15% 稅率假設）≈17%，乘投入資本周轉率約 0.7（TTM 營收約 2,510 億元÷投入資本約 3,600 億元；投入資本＝權益 4,439 億＋債務 634 億−現金 1,474 億，權益含長期股權投資，周轉率偏低估）。內生上界＝增量報酬 10–12%×再投資率上界約 74%（2Q26 資本支出 94.8 億元÷稅後營業利益約 127.4 億元）≈7.4–8.9%/年；74% 是未扣折舊的毛額，淨再投資率只會更低，所以取下緣約 7%。稅率、折舊與營運投入資本口徑事實表未涵蓋，屬粗估"}}}},"q3_growth":{"verdict":"五年後跑道中等：成熟製程本身的可服務市場只有低個位數成長（2026-04-29 法說，Chi-Tung Liu）；新曲線是矽光子、先進封裝與 Intel 12nm，管理層目標 AI 相關營收 3 年內破 10 億美元，但要到 2028 年後才有量。","reasoning":"成長來源：2026 年是量（出貨成長、利用率回升）加價（2H26 選擇性漲價，2027 年預告調升更明顯），沒有併購，也沒有回購。共識 EPS：FY2025 實際 3.31 元，FY2026E 7.15 元，FY2027E 7.32 元，兩年年複合 48.7%；FY2028E 事實表未涵蓋，只有兩年。內生上界引護城河題的約 7%/年，缺口約 40 個百分點，可歸因為兩件事：①2025 年谷底毛利率回升，屬週期性的利潤率擴張；②2026 年上半年約 356 億元業外收益墊高了基期後一年。兩者都不會延續，所以共識路徑不能直接外推。跑道給中：成熟製程滲透已高，但滲透率數據事實表未涵蓋；第二曲線有管理層目標，還沒看到營收，AI 相關營收約占 2026 年營收低個位數。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_kpi8_3q26"],"verdict_values":{"growth":{"driver_mix":"量價皆有，以價格週期為主：2026 年出貨成長加 2H26 選擇性漲價，2027 年更廣泛調價；新曲線（矽光子、先進封裝、12nm）2028 年後才有量；無併購、無回購","runway_years":"事實表未涵蓋（無滲透率數據）","runway_post_y5":"🟡","endo_ceiling_basis":"引護城河題的報酬持續期推導：增量報酬約 10–12%×再投資率約 60%≈7%/年（粗估）；共識兩年年複合 48.7% 遠超此上界，缺口來自週期性毛利回升與一次性業外收益","segments":[{"item":"40nm 以下製程營收占比","value":"約 52%（2Q26）"},{"item":"22/28nm 營收占比","value":"37%，其中 22nm 占 17.5%，創新高（2Q26）"},{"item":"特殊製程營收占比","value":"約 50%（2Q26 法說）"},{"item":"AI 相關營收","value":"2026 年約 3 億美元；管理層目標 3 年內超過 10 億美元"},{"item":"地區","value":"亞洲約 66%、北美約 22%（2Q26）"},{"item":"IDM 客戶占比","value":"約 15%（2Q26，上季 14%）"}],"decay_signals":[{"signal":"EPS CAGR 顯著高於營收 CAGR","lit":true,"note":"共識 FY2025→FY2027 EPS 年複合 48.7%，營收年複合 21.3%，差 27 個百分點；來源是週期性毛利回升與 2026 年業外收益，不是持久的經營槓桿"},{"signal":"FCF/NI<0.75 連 2 年","lit":false,"note":"2023、2024 年曾連兩年亮燈（自由現金流 −80.2 億、25.3 億元），2025 年回到約 1.2 倍；下一輪擴產期要防重演"},{"signal":"毛利率連 2 季年減","lit":false,"note":"2026 年上半年毛利率 30.9%，年增逾 3 個百分點"},{"signal":"核心市占縮減","lit":null,"note":"事實表未涵蓋市占數據"},{"signal":"產業估值倍數系統性下移","lit":null,"note":"事實表未涵蓋同業倍數歷史"}],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"資本配置中等：淨現金約 839 億元、SBC 極低、配息穩定；但公司正在景氣上行段加碼資本支出（2026 年 20 億美元，2026–27 年約 50 億美元），要防 2023–24 年擴產期自由現金流幾乎歸零的情況重演。","reasoning":"2Q26 自由現金流 242.2 億元（營業現金流 337.0 億元減資本支出 94.8 億元），TTM 自由現金流率 23.6%；SBC 只占營業利益 1.6%。淨現金約 839 億元，股息殖利率約 2.0%。2022–2025 年自由現金流依序為 629.8 億、−80.2 億、25.3 億、491.3 億元，上一輪擴產讓兩年現金流幾乎歸零。現在利用率剛回到 85–90%，就把 2026 年資本支出從 15 億上修到 20 億美元；2026-04-29 法說時 Chi-Tung Liu 還說維持約 15 億美元。董事會另核准約 50 億美元，在 2026–27 年投入。管理層說會依客戶承諾分階段執行，但新投資的風險分擔形式（是否簽長約），4 月法說時說言之過早，7 月也沒有揭露。沒有併購；回購紀錄與現金去向四分事實表未涵蓋。","fact_refs":["f_kpi5","f_kpi6_sbc","f_net_debt_m","f_dividend_yield_ttm"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":false,"passed":null,"input":"近 12 個月重大訊息無併購類事件，不適用"},{"name":"buyback_yield","applicable":false,"passed":null,"input":"事實表未涵蓋回購紀錄；資金主要用於資本支出與現金股利"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"2Q26 SBC 約 2.4 億元，占營業利益 1.6%；年化約 10 億元，相對市值約 1.63 兆元，稀釋遠低於每年 1.5%"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購；近三年現金去向四分與回購均價事實表未涵蓋"}}}},"q5_valuation":{"verdict":"現價要求兩件事：2027 年核心獲利接近共識的 7.3 元，而且景氣在 2028–29 年新產能開出時不反轉。我不信，估值偏貴。","reasoning":"賣方目標價在 2026 年 7 月法說後落在 125–160 元，現價在中間，既不支持也不否定本次裁決。1 月時偏空外資目標價 50–52.5 元、偏多 100 元，半年內全距與方向都大幅移動，共識是跟著股價走。PEG 0.36 用的是 FY2025→FY2027 共識 EPS 年複合 48.7%：基期是谷底，終點含週期高點獲利，所以便宜的論證不成立。短期上檔用基準情境 FY2027E EPS 6.4 元乘現行約 18 倍，約 115 元（−11%）；中期用五年終點約 105 元（−19%，未含股息）。","fact_refs":["f_price_at_dd","f_consensus_eps_fy1","f_consensus_eps_fy2","f_pe_current","f_pe_percentile","f_ps_current","f_ps_percentile","f_ev_s_current","f_ev_s_percentile","f_ev_s_fwd","f_dividend_yield_ttm"],"verdict_values":{"valuation":{"basis":"前瞻本益比（以核心 EPS 校正）對照自身歷史倍數區間","tier":"成熟／特殊製程晶圓代工","peers":{"expanded":false,"reason":"事實表沒有同業本益比，同業對照只有利潤率；不以不同層級的先進製程代工當錨"},"fwd_pe":18.18,"peg":0.36,"percentile_5y":100,"val_light":"🟠","val_light_derivation":"現價 130 元：trailing 本益比 19.7 倍、P/S 6.5 倍、EV/S 6.2 倍，三者都高於最近 4 個年度端點（不是連續五年序列，樣本少，但現值高於每一個樣本點）。FY1 共識本益比 18.2 倍、FY2 17.8 倍看似不貴，但分母含業外收益。2026 年核心 EPS 粗估 4.6–5.0 元：上半年營業利益 262.3 億元，加下半年依 3Q26 指引粗估約 375 億元，再加一般利息收入，稅率假設 15%。對應本益比 26–28 倍。成熟製程代工在擴張段給這個倍數，等於先付了 2027 年漲價的錢，判偏貴","upside_short_pct":-11,"upside_mid_pct":-19,"denominator_disputed":true,"denominator_note":"FY1 共識 7.15 元含上半年約 356 億元業外收益（2Q26 約 300 億元投資與股利收入）；元大估第二季獲利約 65% 來自業外。扣除後 2026 年核心 EPS 約 4.6–5.0 元，現價對核心獲利約 26–28 倍"}}},"q6_how_wrong":{"verdict":"最可能看錯的地方：這輪漲價週期比我想的長，AI 相關特殊製程讓毛利率站回 40% 以上。","reasoning":"反方最強的數字：利用率 79%→85%→逾 90%；8 月營收年增 30.7%、9 月年增 27.2%；客戶能見度延到年底；台積電與三星減產 8 吋，供給收縮。若 2027 年合約價調幅達高個位數以上，再加上特殊製程組合改善，毛利率可能突破 40%，2027 年 EPS 可到 7.5 元以上，現價只有約 17 倍，那我就看錯了。另一個可能看錯的地方是 AI 相關業務（矽光子、先進封裝、電源）放量速度比管理層說的「3 年 10 億美元」更快。價值陷阱判黃：衰退信號亮一項；股價 26 週已漲 73.5%，RSI 35 顯示近期已回落；倍數在自身區間頂部，週期高點常見「低本益比陷阱」。","fact_refs":["f_week26_return_pct","f_rsi14","f_pe_percentile","f_ps_percentile","f_ma_w52","f_ma_w250"],"verdict_values":{"trap":{"verdict":"🟡","label":"週期高點的低本益比陷阱：共識 EPS 含業外收益，倍數已在自身區間頂部"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":7.15,"pe":18.18,"basis":"FY1（FY2026E）共識 EPS，含上半年業外收益；終端倍數套在 FY2031E 全年 EPS，同為會計年度 IFRS EPS 口徑"},"eps":{"bull":[7.6,8.5,9.3,10.0,10.8],"base":[6.4,6.9,6.0,6.4,7.0],"bear":[5.6,4.6,3.4,3.6,3.9]},"pe":{"bull":18,"base":15,"bear":14},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":2.0,"net_buyback":0},"second_stage":{"bull_cagr_pct":6,"base_cagr_pct":3},"max_dd":{"lo":-65,"hi":-45,"basis":"參照 2022→2023 年的下行段：營收 −20%、毛利率 45%→35%、自由現金流 629.8 億→−80.2 億元。現價 26 週已漲 73.5%，高於 52 週均線 38%；250 週均線在 52 元。2026 年 1 月法說後股價兩日曾跌逾 17%。Bear 終點 −58% 必須涵蓋在範圍內，故取 −45%～−65%","trigger_time":null},"basis":{"bull":"2027 年合約價調升高個位數、利用率維持 90% 以上，特殊製程與 AI 業務放量，毛利率站回 40% 上下；2029 年下行溫和；終端 18 倍","base":"2027 年漲價落地、毛利率 35–37%，核心 EPS 6.4 元；2029 年自家與中國新產能開出，出現一次下行，之後靠特殊製程回到 7 元；終端 15 倍，為成熟代工中循環倍數","bear":"2027 年漲價破局加上客戶庫存修正，2028–29 年新產能疊加中國擴產，利用率回到 70% 段、毛利率回到 2025 年的 29% 以下，EPS 回到 2024–25 年的 3–4 元；終端 14 倍"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"中芯、華虹、力積電、世界先進持續擴充 28–90nm；聯電自己的新加坡 P4 與台南新廠也在 2027 年底至 2028 年初起量產，效益 2028–29 年才顯現","assumption":"多頭假設 AI 帶動的緊俏能延續到新產能開出之後","consequence":"2028–29 年新產能與需求正常化撞在一起，利用率掉到 70% 段，毛利率在更高折舊下跌破 25%，EPS 回到 3.5 元左右；14 倍約 50 元，五年後虧損逾五成","ruling":"採納：這是五年內最可能的虧損路徑，已放進 Bear 30% 機率；與唯一致命點（2027 年合約價）部分重疊，致命點是這條路徑的第一張骨牌","watch":"每月營收年增率、每季利用率指引、同業擴產公告","evidence_refs":["competitive_share_entrants#2","cyclical_supply_discipline_capacity#0"]},{"view":"論點成功但股東經濟變差","evidence":"財務長：折舊未來至少兩年每年增加十幾%，毛利率將取決於折舊曲線；管理層改以 EBITDA 率溝通，4 月法說拒絕量化","assumption":"AI、矽光子、先進封裝成功等於股東賺更多","consequence":"新業務成功但要先燒約 50 億美元，且 2028 年後還看分階段追加；若增量報酬只有 2022→2025 年那種負值，營收長了，每股自由現金流與 ROIC 反而下降","ruling":"部分採納：基準情境不讓毛利率回到 2022 年水準；若揭露客戶預付或長約覆蓋新產能，這條風險才降級","watch":"年度資本支出對董事會核准額、客戶長約或預付款揭露、年度自由現金流","evidence_refs":[]},{"view":"價格已反映太多","evidence":"現價 trailing 本益比、P/S、EV/S 都高於最近 4 個年度端點；26 週漲 73.5%；元大提醒第二季約 65% 獲利來自業外","assumption":"市場用 7.15 元共識 EPS 看出約 18 倍，以為不貴","consequence":"以核心獲利計約 26–28 倍，2027 年漲價已被提前定價；就算漲價落地，股價也可能只是持平","ruling":"採納：這是本次不追的主因","watch":"3Q26、4Q26 業外收益金額；共識 2027 年 EPS 是否下修","evidence_refs":["capital_markets_pricing#1"]},{"view":"論點失敗","evidence":"管理層 2025 年 7 月點名匯率與美國關稅是近期風險；2018 年晉華被列入實體清單後聯電暫停合作；232 豁免偏向已在美設廠的一線代工","assumption":"關稅與出口管制只會影響短期毛利","consequence":"北美客戶（約 22% 營收）轉向有美國廠的代工，或出口管制擴及成熟製程，廈門廠與中國客戶業務受限","ruling":"採納為長期風險，不預測政策；改用公司損益層的指標判斷能否吸收衝擊","watch":"北美營收占比、管理層揭露的關稅毛利影響","evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","reg_tariff_export#2"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 None → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=None","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 None → 本次 130.0","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=None","side_b":"本次 price_at_dd=130.0","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"獲利分母","cause":null,"prior_field":null,"side_a":"共識 2026 年 EPS 7.15 元，本益比約 18 倍，看似合理","side_b":"2Q26 淨利 422.6 億元中約 300 億元是投資與股利收入，元大估約 65% 來自業外；核心 EPS 約 4.6–5.0 元","ruling":"採 B，估值以核心獲利為準；兩者屬口徑差異，可調和","evidence_level":"高：公司新聞稿與法說原話","settle_metric":"3Q26、4Q26 業外收益金額，以及共識 2027 年 EPS 的修正方向","if_then":["若 3Q26 起每季業外收益回到 30 億元以下，而共識 2027 年 EPS 沒有下修，就視共識偏樂觀，維持不追","反向：若 2027 年本業營業利益率 ≥28%、核心 EPS 自己就達 7 元以上，就上修基準情境並重跑研究"],"evidence_refs":["capital_markets_pricing#1"]},{"axis":"定價權","cause":null,"prior_field":null,"side_a":"管理層預告 2027 年價格調升更明顯；花旗稱客戶能見度延到年底；TrendForce 預估成熟製程漲價延續到 2027 年","side_b":"中國與台系同業擴充 28–90nm；2026 年初市場解讀聯電漲價趨於保守；毛利率 2022→2025 年近乎腰斬","ruling":"可調和，兩邊說的是不同時間尺度：未來 4–6 季是週期性緊俏，2028 年起新產能（含聯電自己）開出後，結構壓力會回來。基準情境放進 2027 年漲價，2029 年放一個下行年","evidence_level":"中：產業研究機構與賣方轉述，公司未給數字","settle_metric":"4Q26 法說給出的 2027 年 ASP 指引；1Q27 混合 ASP 季變化","if_then":["若 2027 年 ASP 指引持平或下滑，持有者清倉，未持有者維持不追","反向：若 2027 年 ASP 調升達高個位數且 1Q27 毛利率 ≥38%，重跑研究，考慮分批反買"],"evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1","competitive_share_entrants#2","supply_demand_durability#3","supply_demand_durability#4","supply_demand_durability#5"]},{"axis":"管理層承諾變動：資本支出","cause":null,"prior_field":null,"side_a":"2026-04-29 法說，Chi-Tung Liu：全年資本支出維持約 15 億美元；新投資的風險分擔形式言之過早","side_b":"2026-07-29 法說：上修到 20 億美元，董事會核准約 50 億美元於 2026–27 年投入，依客戶承諾分階段執行","ruling":"可調和但偏負面：在景氣上行中段加碼擴產，是資本支出循環走向後段的典型訊號；分階段執行與客戶承諾是緩衝，但長約形式至今沒有揭露","evidence_level":"高：兩場法說原話","settle_metric":"2027 年資本支出金額；客戶預付款或長約揭露","if_then":["若 2027 年資本支出超過 30 億美元，且沒有揭露客戶預付或長約，Bear 機率上調到 35%，不追","反向：若揭露的預付或長約覆蓋新產能過半，Bear 機率下調到 25%"],"evidence_refs":["cyclical_supply_discipline_capacity#0"]},{"axis":"毛利率天花板","cause":null,"prior_field":null,"side_a":"利用率逾 90% 加上 2027 年漲價，市場期待毛利率回到 2022 年的 40% 以上","side_b":"財務長（2026-07-29）：折舊未來至少兩年每年增加十幾%，毛利率要看折舊曲線，比較有把握的是 EBITDA 率；4 月法說也拒絕量化 EBITDA 率","ruling":"採 B：管理層主動把溝通指標從毛利率換成 EBITDA 率，本身就是天花板訊號；基準情境的毛利率上限設 37%","evidence_level":"高：法說原話","settle_metric":"2027 年各季毛利率","if_then":["若 2027 年任一季毛利率 ≥40%，代表天花板判斷錯，重跑研究","反向：若利用率逾 90% 時毛利率仍低於 34%，下修基準情境"],"evidence_refs":[]},{"axis":"客戶庫存","cause":null,"prior_field":null,"side_a":"CEO Jason Wang（2026-07-29）：庫存還不到需要擔心的程度","side_b":"同一場法說：1Q26 庫存天數略升，手機與消費性庫存同步上升，車用與工業庫存高於歷史平均；分析師指出 IC 設計客戶營收落後於晶圓出貨","ruling":"不可裁決，要等到 1Q27 指引：庫存天數是落後指標，要配合出貨指引一起看","evidence_level":"中：管理層定性說法，沒有數字","settle_metric":"4Q26、1Q27 出貨指引是否轉為季減","if_then":["若連兩季出貨指引季減，而管理層仍稱庫存健康，持有者減碼","反向：若 1Q27 出貨仍成長，且消費性庫存天數下降，這條風險解除"],"evidence_refs":[]},{"axis":"產業態勢三軸","cause":null,"prior_field":null,"side_a":"結構轉好：台積電與三星減產 8 吋，AI 電源需求帶動 8 吋利用率回到約 90%，成熟製程漲價延續到 2027 年","side_b":"競爭惡化：中國與台系擴充 28–90nm；其他結構變數：232 關稅對二線代工較不利","ruling":"雙向拉鋸：未來 4–6 季由結構轉好那一邊主導，2028 年後競爭惡化那一邊回來；關稅屬於其他結構變動，壓在北美營收","evidence_level":"中","settle_metric":"8 吋利用率、2027 年合約價、北美營收占比","if_then":["若 2027 年上半年任一季利用率低於 85%，判為競爭惡化中，不追","反向：若 2027 年全年利用率維持 90% 以上，且同業擴產延後，判為結構轉好中，重跑研究"],"evidence_refs":["supply_demand_durability#4","cyclical_supply_discipline_capacity#1","competitive_share_entrants#2","reg_tariff_export#2"]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"利用率連三季回升；8 月、9 月營收年增約三成；客戶能見度延到年底；2027 年漲價；淨現金約 839 億元；本土投顧目標價最高 160 元","side_b":"股價 26 週已漲 73.5%；倍數高於最近 4 個年度端點；共識 EPS 含業外；加權五年情境預期報酬約 −4%（含股息）","ruling":"反駁：好消息已經在價格裡，買點要靠更低的價格，或漲價實際落地後的上修","evidence_level":"中","settle_metric":"股價相對 85 元；4Q26 法說的 2027 年 ASP 指引","if_then":["若股價續漲，但 2027 年 ASP 指引還沒出來，不追","反向：若股價跌到 85 元以下，而月營收年增仍為正，重跑研究後分批反買"],"evidence_refs":["supply_demand_durability#3","capital_markets_pricing#0","capital_markets_pricing#3"]}],"triggers":[{"n":1,"text":"3Q26 毛利率落在指引 34–36% 內，利用率逾 90%","type":"假設驗證","maps_to":"H1","metric":"季毛利率（IFRS）","threshold":"≥34%","action":"未達就下修 2027 年情境 EPS，維持不追","source_freq":"每季財報新聞稿","date":"2026-10 下旬（依前兩季 4/29、7/29 的法說節奏推估）","evidence_refs":[]},{"n":2,"text":"2027 年度合約價協商結果","type":"Single Thing","maps_to":"single_thing","metric":"管理層給的 2027 年混合 ASP 年變化","threshold":"≤0%","action":"清倉（若持有）；未持有則維持不建倉","source_freq":"4Q26 法說","date":"2027-01 下旬（推估）","evidence_refs":["competitive_share_entrants#1"]},{"n":3,"text":"價格回到加權情境約 8%/年報酬的位置","type":"估值rearm","maps_to":"rearm","metric":"收盤價","threshold":"≤85 元","action":"重跑研究後分批反買","source_freq":"每日","date":null,"evidence_refs":[]},{"n":4,"text":"成熟製程價格戰重啟","type":"風險","maps_to":"R2","metric":"月營收年增率","threshold":"連續 2 個月 <0%","action":"減碼（若持有）；未持有則不追","source_freq":"每月公開資訊觀測站","date":null,"evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#2"]},{"n":5,"text":"客戶庫存修正","type":"減碼","maps_to":"R3","metric":"季度出貨指引","threshold":"連 2 季指引季減","action":"減碼","source_freq":"每季法說","date":null,"evidence_refs":[]},{"n":6,"text":"4Q26 法說後複審","type":"複審日期","maps_to":null,"metric":null,"threshold":null,"action":"重跑研究","source_freq":null,"date":"2027-02-15","evidence_refs":[]}],"kill_metrics":[{"metric":"季毛利率（IFRS）","bear_threshold":"連兩季 <30%","window":"2027Q1–2027Q4","source":"公司季報新聞稿","last_status":"ok"},{"metric":"產能利用率","bear_threshold":"連兩季 <80%","window":"2027Q1–2028Q4","source":"公司法說","last_status":"ok"},{"metric":"月營收年增率","bear_threshold":"連續三個月 <0%","window":"滾動 12 個月","source":"公開資訊觀測站月營收","last_status":"ok"},{"metric":"2027 年混合 ASP 年變化","bear_threshold":"≤0%","window":"2027 全年","source":"4Q26 與 1Q27 法說","last_status":"unknown"}],"evidence_dismissed":[],"action_conditions":{"rearm_trigger":"股價 ≤85 元，或 2027 年 ASP 調升經法說確認且 1Q27 毛利率 ≥38%（任一成立後重跑研究）","exec_line":"未持有：不追。股價 ≤85 元（對應加權五年預期約 8%/年），或 4Q26 法說確認 2027 年 ASP 調升且 1Q27 毛利率 ≥38%，任一成立後重跑研究，再決定是否分批建立。持有者：若 2027 年 ASP 指引持平或下滑就清倉；若連兩季出貨指引季減就減碼。"}},"decision_inputs":{"signal":"C","ma":"🟡","cycle_position":"中循環","cycle_verdict":"等回踩","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場用含業外收益的共識 EPS 看本益比，又把 2027 年週期性漲價當成持久定價權；但折舊至少兩年每年增加十幾%，2028 年起新產能開出，核心獲利高峰會比共識更早到、也更低","momentum_overheated":false,"cycle_gates_pass":false,"qc49_inherit_prior":null,"wait_for_price":null,"wait_for_price_condition":null,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null},"thesis":{"H":[{"id":"H1","text":"2027 年合約價上調，利用率維持 90% 上下；在折舊每年增加十幾%的情況下，毛利率仍守住 34% 以上","2y":"2027 年各季毛利率 ≥34%","5y":null,"10y":null,"threshold":"季毛利率 ≥34%、利用率 ≥88%","source":"公司季報新聞稿與法說指引","drift_rule":"連 2 季毛利率較 34% 低 5% 以上（<32.3%）為削弱；連 3 季低 10% 以上（<30.6%）為反轉"},{"id":"H2","text":"矽光子、先進封裝、電源與 Intel 12nm 形成第二曲線，讓下行年的獲利底部高於上一輪","2y":null,"5y":"2029 年 AI 相關營收 ≥10 億美元（2026 年約 3 億美元），特殊製程占營收 ≥50%","10y":null,"threshold":"AI 相關營收年複合 ≥50%；下行年營業利益率 ≥15%","source":"法說管理層揭露、年報","drift_rule":"連 4 季管理層下修 AI 營收目標或延後時程達 5% 以上為削弱；連 6 季延後，或目標落空 10% 以上為反轉"},{"id":"H3","text":"擴產依客戶承諾分階段執行，整個循環自由現金流不轉負","2y":null,"5y":"2026–2030 年每年自由現金流 >0，下行年不重演 2023 年的 −80 億元","10y":null,"threshold":"每年自由現金流 >0；2026–27 年資本支出合計不超過核准的約 50 億美元","source":"年報現金流量表、法說","drift_rule":"連 4 季 TTM 自由現金流率較 2Q26 的 23.6% 低 5 個百分點以上為削弱；連 6 季轉負為反轉"}],"R":[{"id":"R1","text":"2026 年獲利膨脹來自業外收益，市場把一次性收益當成獲利能力，核心毛利率一旦不如指引，估值就會回落","h_ref":"H1","clock":"⚡","threshold":"3Q26 毛利率 <34%（低於指引下緣）","evidence_refs":["capital_markets_pricing#1"]},{"id":"R2","text":"中國與台系同業擴充 28–90nm，2027 年漲價被壓回，價格戰重啟","h_ref":"H1","clock":"🔥","threshold":"2027 年任一季混合 ASP 季減，或月營收連 2 個月年減","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1","competitive_share_entrants#2"]},{"id":"R3","text":"手機、消費性、車用與工業的客戶庫存偏高，AI 以外需求轉弱時引發砍單","h_ref":"H1","clock":"🔥","threshold":"連 2 季出貨指引季減","evidence_refs":[]},{"id":"R4","text":"232 關稅與出口管制讓二線代工失去北美客戶，或成熟製程被納入管制","h_ref":"H2","clock":"🐢","threshold":"北美營收占比（2Q26 約 22%）連 2 季 <18%，或管理層揭露關稅使毛利率受損 ≥1 個百分點","evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","reg_tariff_export#2"]},{"id":"R5","text":"資本支出在景氣後段持續加碼，新產能報酬低於資金成本","h_ref":"H3","clock":"🐢","threshold":"2027 年資本支出 >30 億美元，且未揭露客戶長約或預付","evidence_refs":["cyclical_supply_discipline_capacity#0"]},{"id":"R6","text":"最大客戶占比由 10% 升到 12%，若持續集中，議價權與信用風險會跟著升高","h_ref":"H1","clock":"🐢","threshold":"年報最大客戶占營收 >20%","evidence_refs":["customer_concentration_credit#0"]}],"single_thing":{"description":"2027 年度合約價協商結果：管理層在 4Q26 法說給出的 2027 年混合 ASP，是否明確上調","why_fatal":"基準情境 2027 年 EPS 6.4 元，有一半以上的增量來自價格。在固定折舊下，ASP 每變動 1% 約放大為營業利益變動 4%；漲價若破局，2027 年 EPS 會回到 5 元附近，現價對應 26 倍以上","if_happens":"基準情境前兩年改用 Bear 路徑；持有者清倉，未持有者維持不建倉","how_monitor":"4Q26 法說（推估 2027 年 1 月下旬）的 ASP 指引；1Q27 季報的混合 ASP 季變化；每月營收年增率","probability":"35%"}},"appendix_a":{"growth_durability":5,"quality_score":6,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":17.76,"peg_fy2":0.36,"stress":{"pass":null,"total":null}},"eps_meta":{"base_eps_path":{"FY2025A":3.31,"FY2026E":7.15,"FY2027E":7.32,"FY2028E":null},"fy_end_month":12,"eps_basis":"IFRS 稀釋 EPS（含業外收益）；FY2028E 共識事實表未涵蓋"},"catalysts":[{"date":"2026-10","date_precision":"month","type":"guidance","event":"3Q26 財報與 4Q26 指引：毛利率是否落在 34–36%","impact":"高","watch":"毛利率、利用率、業外收益金額"},{"date":"2027-01","date_precision":"month","type":"guidance","event":"4Q26 法說：2027 年合約價與全年展望","impact":"高","watch":"2027 年混合 ASP 指引、資本支出"},{"date":"2027-12","date_precision":"quarter","type":"product","event":"Intel 12nm 客戶投片與矽光子平台開放一般客戶使用","impact":"中","watch":"投片家數、2028 年量產時程"},{"date":"2028-03","date_precision":"quarter","type":"capacity","event":"新加坡 P3／P4 與台南 12A 新產能開始爬坡","impact":"中","watch":"利用率是否被新產能稀釋、折舊增幅"}],"decision_out":{"role":"追蹤","row_hit":"6","pacing":[],"holding_cap":null,"audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='C'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='C'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":true,"basis":"signal='C'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場用含業外收益的共識 EPS 看本益比，又把 2027 年週期性漲價當成持久定價權；但折舊至少兩年每年增加十幾%，2028 年起新產能開出，核心獲利高峰會比共識更早到、也更低"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='C', runway='🟡', val='🟠', moat_trend='→', week26=73.52, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='循環/商品', cycle_position='中循環', moat='C', moat_trend='→', cycle_gates_pass=False"},{"row":"6/7/7a-verdict","condition":"Soft Veto 生效 → 觀望（max-severity wins；8a/8b 未能繞過）","hit":true,"basis":"soft_veto_rows=['6']"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"requires_critic":[],"verdict":"觀望"}}
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
