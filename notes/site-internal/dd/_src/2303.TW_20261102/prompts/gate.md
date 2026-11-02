你是 DD 管線 v20 的判斷層閘（gate），標的 2303.TW（20261102）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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
- `f_earnings_recency`（q1_business）｜最近一次財報日＝2026-10-28 date｜期間與口徑：2026-10-28／距今 3 個交易日｜kind：realized
  - 來源：—（numbers.earnings_recency，as_of 2026-10-28）
- `f_peer_2303_tw_gross_margin_pct`（q2_moat）｜2303.TW 毛利率＝31.71 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.2303.TW.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_2303_tw_operating_margin_pct`（q2_moat）｜2303.TW 營業利益率＝21.83 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.2303.TW.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_2303_tw_fcf_margin_pct`（q2_moat）｜2303.TW FCF 利潤率＝25.76 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.2303.TW.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
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
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝7.38 TWD/share｜期間與口徑：2026-11-02／yfinance 分析師共識平均（Koyfin 快照無此檔）；幣別同報價｜kind：estimate
  - 來源：yfinance earnings_estimate（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-11-02）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝7.16 TWD/share｜期間與口徑：2026-11-02／yfinance 分析師共識平均（Koyfin 快照無此檔）；幣別同報價｜kind：estimate
  - 來源：yfinance earnings_estimate（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-11-02）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝281100.5 TWD m｜期間與口徑：2026-11-02／yfinance revenue_estimate 0y 平均（19 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-02）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝346616.62 TWD m｜期間與口徑：2026-11-02／yfinance revenue_estimate +1y 平均（24 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-02）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi5`（q4_capital）｜自由現金流（營業現金流−資本支出）＝24.22 NT$ billion｜期間與口徑：2Q26（季末 2026-06-30，財報公告 2026-07-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：yfinance quarterly_cashflow（營業現金流 33.70B − 資本支出 9.48B）；新聞稿未揭露 FCF（numbers.latest_quarter_kpis.items[5]，as_of 2Q26（季末 2026-06-30，財報公告 2026-07-29））
- `f_kpi6_sbc`（q4_capital）｜SBC 占營業利益＝1.6 %｜期間與口徑：2Q26（季末 2026-06-30，公告於 2026-07-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：yfinance quarterly_cashflow SBC 0.240B ÷ 營業利益 14.95B；新聞稿未揭露 SBC（numbers.latest_quarter_kpis.items[6]，as_of 2Q26（季末 2026-06-30，公告於 2026-07-29））
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝-71936.84 TWD m｜期間與口徑：2026-11-02／yfinance 最新一季：總債務 79640.26、現金 151577.1（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-02）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝2.339 %｜期間與口徑：2026-11-02／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-11-02）
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝12538.97 m shares｜期間與口徑：2026-11-02／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-11-02）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝111.5 TWD｜期間與口徑：2026-10-30（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-10-30（RTH 收盤，UTC））
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝16.64 x｜期間與口徑：2026-10-30（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-10-30（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝100.0 %｜期間與口徑：2026-10-30（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-10-30（RTH 收盤，UTC））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝5.26 x｜期間與口徑：2026-10-30（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-10-30（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝100.0 %｜期間與口徑：2026-10-30（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-10-30（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝4.99 x｜期間與口徑：2026-10-30（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-10-30（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝100.0 %｜期間與口徑：2026-10-30（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-10-30（RTH 收盤，UTC））
- `f_ev_s_fwd`（q5_valuation）｜EV/S（EV ÷ FY1 共識營收）＝4.72 x｜期間與口徑：2026-11-02／f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）｜kind：estimate
  - 來源：—（numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m，as_of 2026-11-02）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rsi14`（q5_valuation）｜RSI(14)＝27.64｜期間與口徑：2026-10-30（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-10-30（RTH 收盤，UTC））
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝46.71 %｜期間與口徑：2026-10-30（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^TWII｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-10-30（RTH 收盤，UTC））

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
- q6_how_wrong：digest.qa_flags 有 5 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/2303.TW_20261102/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":168.0,"bear_5y_price":50.6,"p_bull_pct":25,"p_bear_pct":30,"upside_5y_pct":-20.7,"ev5y_pct":-13.0,"irr_base_pct":-4.5,"asym_ratio":0.8,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":7.38,"pe":15.11,"basis":"FY2026E 共識 EPS（當年度口徑，與終端 FY2031 當年 EPS 同口徑）。含約 2.4 元業外一次性，經常性約 5.0 元，起點本益比因此看起來偏低。"},"eps":{"bull":[7.4,8.0,8.8,9.8,10.5],"base":[6.6,6.2,6.5,7.0,6.8],"bear":[5.8,4.5,3.8,4.2,4.6]},"pe":{"bull":16,"base":13,"bear":11},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":2.339,"net_buyback":0},"second_stage":{"bull_cagr_pct":6,"base_cagr_pct":3},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### 2303.TW_Q2_2026_Earnings_Call_20260729.md
- 2026-07-29｜Jason Wang｜guidance：CEO 給 Q3 2026 財測：出貨高個位數成長、美元 ASP 持平、毛利率約 30% 中段、產能利用率大於 90%。（原話："Gross margin will be in the mid-30% range."）
- 2026-07-29｜Jason Wang｜capital_allocation：2026 資本支出預算由 15 億美元上修至 20 億美元，用於矽光子與先進封裝。（原話："the 2026 CapEx will be raised to USD 2 billion"）
- 2026-07-29｜Chi-Tung Liu｜capital_allocation：董事會核准約 50 億美元擴產，橫跨 2026 與 2027，2028 視分期擴張而定。（原話："today's Board meeting approved nearly USD 5 billion already."）
- 2026-07-29｜Jason Wang｜capital_allocation：董事會核准擴建新加坡 P4 無塵室並在台南新建廠，分階段執行並強調資本紀律。（原話："construct a new fab in Tainan, Taiwan."）
- 2026-07-29｜Jason Wang｜commitment：每一階段擴產以市場驗證與客戶承諾為前提，提供客戶產能保證與 UMC 稼動保護。（原話："market validation, this alignment and customer commitment"）
- 2026-07-29｜Chi-Tung Liu｜margin：CFO 說明折舊未來至少兩年每年成長約低十位數百分比，新廠與無塵室改變原先折舊曲線。（原話："depreciation to increase by low teens"）
- 2026-07-29｜Chi-Tung Liu｜margin：CFO 稱毛利率取決於折舊曲線，聚焦 EBITDA margin，不與歷史毛利率比較。（原話："we really don't compare ourselves to the historical data."）
- 2026-07-29｜Chi-Tung Liu｜margin：CFO 將 Q3 毛利率指引上升主要歸因於稼動率由 85% 升至 90% 以上，另列 ASP、產品組合、匯率、折舊等因素。（原話："is mainly attributed to the higher utilization rate."）
- 2026-07-29｜Chi-Tung Liu｜margin：Q2 財務數字：營收 687.3 億元、毛利率 32.5%、稼動率 85%。（原話："Consolidated revenue was TWD 68.73 billion"）
- 2026-07-29｜Chi-Tung Liu｜margin：CFO 說明 Q2 業外收入（投資與股利）達 300 億元，墊高稅後淨利，屬口徑拆解。（原話："investment and dividend income together reached"）
- 2026-07-29｜Jason Wang｜guidance：CEO 預期 2027 年定價改善幅度更明顯，且今年價格趨勢優於原預期。（原話："we're even expecting more meaningful pricing uplift in 2027."）
- 2026-07-29｜Jason Wang｜guidance：AI 相關營收今年約 3 億美元，三年內預計超過 10 億美元。（原話："we expect the AI exposure to exceed USD 1 billion"）
- 2026-07-29｜Jason Wang｜margin：管理層對 AI 營收的定義：以 AI 為終端產品的解決方案，含連接與電源管理，矽光子歸入連接。（原話："the solution associated with AI as end product"）
- 2026-07-29｜Jason Wang｜risk：CEO 表示非 AI 需求不均，不視為全面復甦，消費端手機與 PC 今年仍年減。（原話："we will not categorize the current environment as"）
- 2026-07-29｜Jason Wang｜risk：客戶庫存天數小幅上升，消費與手機庫存同步上升，管理層稱謹慎但不到擔憂程度。（原話："we're not to the level that we need to be worried"）
- 2026-07-29｜Jason Wang｜product：首次 12 吋光子 IC 量產出貨，矽光子平台預計 2027 年開放一般客戶。（原話："first mass production delivery of a 12-inch photonics IC"）
- 2026-07-29｜Jason Wang｜product：先進封裝有 10 家以上活躍客戶、35 項以上新產品洽談，預計 2026 至 2027 年初 tape-out。（原話："more than 10 active customers now and over 35 new products"）
- 2026-07-29｜Jason Wang｜product：CEO 明說先進封裝不做 CoWoS。（原話："but not to the CoWoS solution"）
- 2026-07-29｜Jason Wang｜commitment：新擴產建設前置期超過 20 個月，產能貢獻落在 2028 至 2029 年，細節稍後回報。（原話："somewhere greater than 20 months in terms of lead time"）
- 2026-07-29｜Jason Wang｜commitment：與 Intel 12nm 合作：2027 年 tape-out、量產意義較大在 2028 年，並稱對現有財務屬加分模式。（原話："The production will probably be more meaningful in 2028."）
- 2026-07-29｜Jason Wang｜competition：CEO 稱先進封裝領先同業。（原話："we believe we are ahead of our peers in advanced packaging"）
- 2026-07-29｜Jason Wang｜competition：更先進製程策略：先交付 12nm，成功後再探索更先進節點。（原話："we have to execute the 12nm and then we will explore beyond."）
- 2026-07-29｜Jason Wang｜customer：Q3 出貨成長由電源管理 IC、感測器與微控制器需求帶動，8 吋明顯回升。（原話："strong demand of power management IC, sensors"）
- 2026-07-29｜Jason Wang｜customer：特殊製程約占營收 50%。（原話："the specialty offering today is representing 50%"）

### 問答異常語氣（迴避／改口／保留）
- 2303.TW_Q2_2026_Earnings_Call_20260729.md｜問：Gokul Hariharan 與 Katherine Yu 追問毛利率能否超越 2022 年高點、是否能高於 40%｜答法：CFO 未給毛利率目標或區間，改談 EBITDA margin 與折舊曲線，稱不與歷史比較。
- 2303.TW_Q2_2026_Earnings_Call_20260729.md｜問：Sunny Lin 追問先進封裝可服務市場規模、營收軌跡與新加坡 P3 產能目標｜答法：CEO 未給 TAM 數字或產能目標，只說有更具體資料時再回報。
- 2303.TW_Q2_2026_Earnings_Call_20260729.md｜問：Haas Liu 要求量化毛利率改善中稼動率、價格、匯率各自貢獻｜答法：CFO 只說主要因稼動率，並列出多項因素，未給量化拆解。
- 2303.TW_Q2_2026_Earnings_Call_20260729.md｜問：Haas Liu 問電源 IC 占營收比重｜答法：CEO 未回答電源 IC 比重，改答特殊製程整體占 50%。
- 2303.TW_Q2_2026_Earnings_Call_20260729.md｜問：Katherine Yu 問 7nm 以下是否在 2028 年之後｜答法：CEO 未給時程，稱有討論才有更明確里程碑；CFO 稱目前只聚焦 12nm。

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
{"date":"20261020","verdict":"觀望","role":"追蹤","H":{"status":"unavailable"},"R":{"status":"unavailable"},"single_thing":null,"kill_metrics":null,"rearm_trigger":"股價 ≤85 元，或 2027 年 ASP 調升經法說確認且 1Q27 毛利率 ≥38%（任一成立後重跑研究）","irr_base_pct":-4.2,"ev5y_pct":-13.7,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"追蹤","signal":"C","val":"🟠","ma":"🟡","trap":"🟡","moat_trend":"→","runway_post_y5":"🟡","asym_ratio":0.7,"ev5y_pct":-13.7,"irr_base_pct":-4.2,"max_dd_pct":-65,"bull_5y_price":194.4,"bear_5y_price":54.6,"p_bull_pct":25,"p_bear_pct":30,"rearm_trigger":"股價 ≤85 元，或 2027 年 ASP 調升經法說確認且 1Q27 毛利率 ≥38%（任一成立後重跑研究）","price_at_dd":130.0,"archetype":"循環/商品","cycle_position":"中循環"}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"2303.TW","date":"2026-11-02","schema":"v15.0","contract":"v19","company_name":"聯華電子（UMC）"},"oneliner":"3Q26 法說確認 2027 年混合 ASP 年增約 10%，但利用率 92% 下毛利率只有 34%，董事會又加碼約 32 億美元擴產。111.5 元已先反映漲價，基準情境五年後約 88 元；等 1Q27 毛利率 ≥38% 或股價 ≤85 元再重跑研究。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/2303.TW_20261102/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/2303.TW_20261102/scenario.json","answers":{"q1_business":{"verdict":"聯電做的是成熟與特殊製程晶圓代工，客戶以 IC 設計公司為主（約 86%）。獲利取決於產能利用率和每片晶圓單價：2Q26 毛利率 32.5%、營益率 21.8%；3Q26 利用率升到 92%，毛利率 34%。2026 年單價持平，2027 年才轉為漲價。","reasoning":"營收結構（3Q26 法說）：22／28 奈米約 35%，其中 22 奈米占晶圓銷售 18.3%，創新高；40 奈米約 16%，65 奈米約 19%。應用別方面，消費約 32%，通訊與電腦季持平；IDM 客戶約 14%；特殊製程約占營收一半（2Q26 法說）。單位經濟：3Q26 營收 742.4 億元，出貨逾 120 萬片 12 吋約當，每片約 6 萬元出頭。2026 年成長來自量與利用率（85%→92%）；2027 年管理層改說由價帶動，混合 ASP 年增約 10%（含同規格漲價與組合改善），出貨則受產能限制。獲利品質：2Q26 歸母淨利 422.6 億元、EPS 3.39 元，其中約 300 億元是投資與股利業外收益，元大估約 65% 獲利來自業外，所以 FY2026 EPS 不能當經常性獲利看。單點依賴：最大客戶占 2025 年營收 12%（前一年 10%），集中度低，列入風險追蹤，不當護城河證據。產業時鐘判在過熱段：利用率 92%、多座 12 吋廠滿載，電源管理與 FPGA 訂單積壓，2027 年 8 吋與 12 吋都漲價，董事會再加約 32 億美元資本支出。不過 PC 與中低階手機需求轉弱，緊俏集中在 AI 相關製程。供需持久度判為週期性、會反轉，供給可逆性高：中芯、華虹、力積電、世界先進持續擴充 28–90 奈米，聯電自己的新產能也從 2028 年底起陸續開出。","fact_refs":["f_kpi0_ifrs","f_kpi1_gaap","f_kpi2_gaap","f_kpi3","f_kpi4_eps","f_kpi7","f_kpi8_3q26","f_earnings_recency"],"verdict_values":{"revenue_quality":"晶圓代工按片計價。2026 年量增、價平；2027 年轉為價增（混合 ASP 年增約 10%），量受產能限制。FY2026 EPS 含約 300 億元業外一次性收益。","unit_econ_note":"3Q26 每片 12 吋約當營收約 6 萬元出頭（742.4 億元 ÷ 逾 120 萬片）。利用率上升帶來的毛利率貢獻，正被新加坡新廠折舊抵銷。","archetype":{"primary":"循環/商品","secondary":null,"confidence":"高","fingerprint":"成熟製程晶圓代工：毛利率由 2022 年 45.1% 降到 2025 年 29.0%，EPS 由 6.87 元降到 3.27 元；資本支出占營收逾 15%，獲利跟著利用率與 ASP 大幅擺動。"},"industry":{"clock_phase":"III","sd_verdict_source":"週期性，會反轉。這波緊俏來自 AI 電源需求，加上台積電、三星減少 8 吋產能（TrendForce）；供給端中國與台系二線廠都在擴 28–90 奈米，聯電自己的新產能 2028 年底起開出，供給可逆性高。","bargaining":{"up":"對設備與材料商議價強：2025 年 10 月要求供應商 2026 年起降價至少 15%。但矽晶圓、能源等投入成本上升，CFO 表示需要努力抵銷。","down":"客戶以 IC 設計公司為主（IDM 約 14%），最大客戶占 12%，集中度低。漲價能力取決於產能緊俏程度：2026 年初因中國對手競爭而保守，2027 年才全面調價。","geo":"新加坡是台灣以外最大生產基地，政治中立、受客戶青睞，另有廈門與日本廠。美國 232 關稅豁免偏向已在美設廠的一線廠。"},"profit_pool_dir":"成熟製程標準邏輯的利潤池往中國廠流出，聯電則往特殊製程、矽光子、先進封裝等高附加價值段移動。五年營業利益池占比數字事實表未涵蓋。","tam_table":{"expanded":false,"reason":"矽光子、DTC、TFLN 屬新品類，但事實表與逐字稿都沒有 TAM、SAM 或滲透率數字；2Q26 法說分析師追問先進封裝市場規模時，管理層也沒有給，屬資料缺口。"}}}},"q2_moat":{"verdict":"護城河持平（→），等級 C。執行面在變強：利用率 92%、22 奈米營收創新高，矽光子平台通過多家雲端大廠驗證。定價面則只是跟著週期轉好，2026 年初仍因中國對手競爭而漲價保守。","reasoning":"機制：特殊製程組合（22／28 奈米、BCD 電源、高壓顯示驅動、RF），加上換廠必須重新設計與認證，車用與顯示驅動的客戶黏著度較高；標準 28–90 奈米邏輯則可被中芯、華虹、世界先進替代。可證方向：TTM 營益率 21.8%，比 GFS（11.6%）高約 10pp、比世界先進（17.0%）高約 5pp，FCF 利潤率 25.8% 也領先；但事實表沒有同業歷年利差，無法確認利差是否在擴大。執行分 7：利用率由 85% 升到 92%，出貨創新高，矽光子良率達量產水準，TFLN 完成 1.6T 系統驗證。定價分 5：2025 年上半年毛利率 27.7%，較 2022 年 45.1% 幾乎腰斬；2025 年得要求供應商降價 15% 來保毛利；2026 年 ASP 持平；2027 年的 +10% 有一部分來自成本轉嫁與產品組合。中國擴產屬生態層級的價格攻擊，合併後約 5–6 分，等級 C。報酬持續期：當期 ROIC 粗估約 12%（稅後），屬高利益率×低周轉；週期內增量報酬為負，新產能的報酬要到 2028–2030 年才能驗證。","fact_refs":["f_peer_2303_tw_gross_margin_pct","f_peer_2303_tw_operating_margin_pct","f_peer_2303_tw_fcf_margin_pct","f_peer_gfs_gross_margin_pct","f_peer_gfs_operating_margin_pct","f_peer_gfs_fcf_margin_pct","f_peer_5347_two_gross_margin_pct","f_peer_5347_two_operating_margin_pct","f_peer_5347_two_fcf_margin_pct"],"verdict_values":{"moat":{"mechanism":"特殊製程組合、換廠重新認證成本，以及台灣以外的新加坡產能","execution":7,"pricing":5,"grade":"C","trend":"→","trend_evidence":"執行面擴大：利用率 85%→92%，22 奈米占晶圓銷售 18.3% 創新高，12 吋 PIC 平台獲多家雲端大廠驗證 1.6T。定價面持平：2026 年 ASP 持穩，2027 年混合 ASP 才轉為 +10%；2026 年初因中國對手競爭漲價保守，2025 年還得逼供應商降價 15%。營益率領先 GFS 約 10pp、領先世界先進約 5pp，但沒有歷年同業利差可確認方向，所以不標擴大。","competitor_notes":[{"name":"GFS","strategy_note":"營益率 11.6%、FCF 利潤率 11.5%，約只有聯電一半；美國本土產能在 232 關稅豁免上占優，是聯電爭取美系客戶的直接對手。"},{"name":"5347.TWO","strategy_note":"世界先進營益率 17.0%，FCF 利潤率 −94.8%，正處大規模擴產期；它在 8 吋與成熟製程的擴產，是聯電 2026 年漲價保守的原因之一。"},{"name":"0981.HK","strategy_note":"中芯事實表缺營收，無法比較利潤率；新聞點名它持續擴充 28–90 奈米，是成熟製程價格競爭的主要來源。"}],"peer_na_reason":"中芯（0981.HK）營收資料缺失，無法計算利潤率","threats":[{"level":"🔴","text":"中國（中芯、華虹）與台系（力積電、世界先進）持續擴充 28–90 奈米。2026 年初聯電因此漲價保守，1 月法說後兩日股價跌逾 17%；屬生態層級的價格攻擊。","p":40,"evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1","competitive_share_entrants#2"]},{"level":"🟡","text":"美國 232 半導體關稅 25%，豁免偏向已在美設廠的一線廠，二線代工較不利；管理層 2025 年 7 月已點名關稅與匯率風險。2018 年晉華案也顯示，出口管制可以直接切斷合作。","p":25,"evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","reg_tariff_export#2"]},{"level":"🟡","text":"矽光子與先進封裝起步晚於同業，同業也在擴產；管理層稱 PIC 傳播損耗等參數優於同業，但沒有第三方數字佐證。","p":30,"evidence_refs":[]},{"level":"🟡","text":"客戶轉單、找第二供應商或自建產能：三組查詢都沒有找到聯電客戶轉單或自建產能的事例，這一軸沒有證據。客戶以 IC 設計公司為主（IDM 約 14%），自建產能的能力低；最大客戶占 12%，單一客戶轉走的衝擊有限。標準邏輯製程被轉到中芯、華虹的風險，已算進第一條中國擴產。查無資料不改變護城河 C 的判斷，但「特殊製程換廠成本高」這個說法也因此少了反面檢驗。","p":15,"evidence_refs":[]}],"roic_durability":{"quadrant":"高利益率×低周轉","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"這是剛性需求：電源管理、顯示驅動、車用雷達、Wi-Fi 晶片都要用成熟製程，AI 電源與 FPGA 訂單還在積壓。但付款者是 IC 設計公司，終端 PC 與中低階手機需求轉弱（3Q26 CEO），消費約占營收 32%；需求急迫，持久度卻跟著週期走。"},{"item":"決策層級","level":"🟡","text":"替代性要在單一晶片的製程認證層看：特殊製程換廠須重新設計與驗證，車用最久，22 奈米新 tape-out 持續增加。標準 28–90 奈米邏輯則有中芯、華虹、世界先進可替代，2026 年初聯電因中國對手而漲價保守，就是直接讀數。"},{"item":"價值鏈分配","level":"🟡","text":"成熟製程這個環節長期分得少：2022→2025 年毛利率由 45% 降到 29%。目前產能緊俏讓價值暫時往代工端移（2027 年 ASP +10%），但聯電要求設備與材料商降價 15%，顯示自己也被上下游擠壓。客戶分散（最大客戶 12%），客戶自建產能的能力低。"},{"item":"社會容忍度","level":"🟡","text":"晶圓價格沒有社會天花板，但地緣政策會壓低經濟上限：美國 232 半導體關稅 25%，豁免偏向在美設廠的一線廠。新加坡廠因政治中立受客戶青睞，算是部分對沖。"}],"roiic":"週期內為負：2022 年營業利益約 1,036 億元，TTM 約 580 億元，期間資本支出沒有停（2023 年 FCF −80 億元）。新產能的增量報酬要到 2028–2030 年才能驗證。","reinvest_rate":"約 50%，取 2023–2025 年一個完整循環的中間值。事實表未涵蓋折舊攤銷，無法用（資本支出 − 折舊 ＋ 營運資金增加）÷ 稅後營業利益直接算，改用現金流反推：淨利 − FCF 約等於資本支出 − 折舊 ＋ 營運資金增加，所以再投資率 ≈ 1 − FCF／淨利。2024 年 1 − 0.05 ＝ 95%；2025 年 1 − 1.22 ＝ −22%；2023 年 FCF −80 億元、淨利為正，比率超過 100%。2024–2025 兩年平均約 37%，三年平均至少約 58%（2023 年以下限 100% 計），50% 取兩者中間；乘上增量 ROIC 約 10%，內生上界約 3.7%–5.8%，取 5%。TTM 口徑（1 − FCF 利潤率 25.8% ÷ 稅後營益率約 18.5%）約 −39%，是谷底期資本支出偏低的讀數，不拿來外推。往後會偏高：2026 年資本支出 20 億美元，董事會累計核准約 82 億美元分年投入，2027–2028 年會落在區間上緣。限制：淨利或營業現金流含業外收益的年度，這個比率會失真。","endo_ceiling":5.0,"formula_note":"ROIC＝稅後營業利益率×投入資本周轉率。TTM 營益率 21.8% ×（1−稅率約 15%，稅率事實表未涵蓋）× 周轉約 0.67（TTM 營收約 2,658 億元 ÷ 投入資本約 3,980 億元；投入資本＝權益 4,700 億＋債務 796 億−現金 1,516 億）≈ 12%。權益含長期投資部位，實際營運 ROIC 會偏高。內生成長上界＝增量 ROIC 約 10%（低於當期，因新廠前兩年折舊重）× 再投資率約 50% ≈ 每年 5%。"}}}},"q3_growth":{"verdict":"跑道中等（🟡）：2026 年靠量，2027 年靠價，2028 年底以前沒有新產能補量。矽光子、DTC、TFLN 是有客戶驗證的第二曲線，但 2030 年才到規模，2027 年貢獻小。","reasoning":"成長拆解：2026 年 1–9 月營收 2,040 億元，年增 16.1%，來自出貨與利用率。4Q26 指引出貨低個位數成長、ASP 持穩。2027 年管理層指引混合 ASP 年增約 10%，出貨受產能限制，CEO 對明年產能成長只說『不夠』。共識 FY2027 營收 3,466 億元，年增約 23%，高於「價 +10%、量低個位數成長」可推出的約 12–16%，這是本研究基準 EPS 低於共識的主因。共識 EPS 路徑：FY2025A 3.27 元 → FY2026E 7.38 元 → FY2027E 7.16 元，兩年年化約 48%；但基期是週期谷底，FY2026 又含約 2.4 元業外一次性，扣除後 FY2026 經常性 EPS 約 5.0 元。內生上界約每年 5%（推導見護城河段）。共識與上界的缺口，來自毛利率週期回升與一次性業外，屬利潤率擴張，不是再投資或回購帶來的。第二曲線：12 吋 PIC 平台獲多家雲端大廠驗證 1.6T；月產能目標為矽光子 1.8 萬片、DTC 2.2 萬片、TFLN 2 萬片，2028 年底開始爬坡，2030 年到規模。AI 相關營收 2026 年約 3 億美元，管理層稱三年後占營收逾四分之一，但定義涵蓋電源、連接、FPGA，口徑偏寬。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_kpi8_3q26"],"verdict_values":{"growth":{"driver_mix":"2026 年靠量（出貨增加、利用率 85%→92%）；2027 年以價為主（混合 ASP +10%，含產品組合），量受產能限制；2028 年底起才有新產能補量（矽光子、DTC、TFLN 月產能合計 6 萬片）。無併購，回購事實表未涵蓋。","runway_years":"5–9（成熟製程不適用滲透率框架；以新產能 2030 年到規模、之後仍受週期支配估算）","runway_post_y5":"🟡","endo_ceiling_basis":"內生上界約每年 5%＝增量 ROIC 約 10% × 再投資率約 50%（推導見護城河段）。共識 FY2025A→FY2027E EPS 年化約 48%，缺口來自毛利率週期回升（29%→34%，2027 年漲價再往上推）與 FY2026 約 300 億元一次性業外，屬利潤率擴張與一次性收益。","segments":[{"item":"22／28 奈米","value":"約 35% 營收（3Q26）；22 奈米占晶圓銷售 18.3%，創新高，主要用於顯示驅動、車用雷達、Wi-Fi"},{"item":"40 奈米","value":"約 16% 營收（3Q26）"},{"item":"65 奈米","value":"約 19% 營收（3Q26）"},{"item":"特殊製程合計","value":"約 50% 營收（2Q26 法說）"},{"item":"AI 相關（電源、連接、FPGA、矽光子、先進封裝）","value":"2026 年約 3 億美元；管理層目標三年後占營收逾 25%"},{"item":"消費應用","value":"約 32% 營收；PC 與中低階手機需求轉弱"}],"decay_signals":[{"signal":"EPS 成長顯著高於營收成長（差距逾 5pp）","lit":true,"note":"FY2026 共識 EPS 年增逾一倍、營收年增約 18%，但主要來自業外一次性，非經常性"},{"signal":"FCF／淨利連 2 年低於 0.75","lit":false,"note":"2023–2024 年曾連 2 年低於 0.75，2025 年回到 1.22；2027–2028 年擴產後可能再亮"},{"signal":"毛利率連 2 季年減","lit":false,"note":"3Q26 毛利率 34%，高於 2025 年全年的 29%"},{"signal":"產業估值倍數近 3 年系統性下移","lit":false,"note":"本益比與股價營收比都在四個年度端點中最高"}],"trap_rating":"價值陷阱風險 🟡（亮 1 項）；長期成長性 🟡"}}},"q4_capital":{"verdict":"現金用途正從配息轉向擴產。TTM FCF 利潤率 25.8%，淨現金約 719 億元；但董事會累計核准約 82 億美元擴產，2027–2028 年 FCF 會明顯收縮。股東回報以現金股利為主（殖利率 2.34%），SBC 稀釋可以忽略。","reasoning":"FCF／淨利：2023 年為負，2024 年 0.05，2025 年 1.22（FCF 491 億元、淨利 404 億元），跟著資本支出週期大幅波動。2Q26 FCF 242 億元（營業現金流 337 億元−資本支出 95 億元）。SBC 每季約 2.4 億元，占營業利益 1.6%，換算每年稀釋不到市值的 0.1%。現金去向四分（研發、資本支出、配息、回購）的完整拆分，以及回購紀錄，事實表都未涵蓋。擴產依客戶承諾分階段投入，方向合理，但會壓低未來兩年的 FCF 與股利成長空間。2026 年 6 月因交換公司債轉換，處分聯詠持股約 17 億元，資產端仍有可變現的投資部位。","fact_refs":["f_kpi5","f_kpi6_sbc","f_net_debt_m","f_dividend_yield_ttm","f_shares_diluted_m"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":false,"passed":null,"input":"近 12 個月重大訊息沒有併購類事件，成長靠自建產能"},{"name":"buyback_yield","applicable":false,"passed":null,"input":"事實表未涵蓋回購金額與均價；股東回報以現金股利為主（殖利率 2.34%）"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"2Q26 SBC 約 2.4 億元，占營業利益 1.6%；年化約 10 億元，對市值約 1.4 兆元的稀釋約 0.07%／年，低於 1.5%"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長靠自建產能，沒有靠併購撐；股東回報以現金股利為主，回購金額事實表未涵蓋"}}}},"q5_valuation":{"verdict":"現價要求三件事同時成立：2027 年漲價全數落地、毛利率在折舊高峰中仍往上走、下一輪下行不重演 2023–2025 年的獲利腰斬。我不相信第三點，估值偏貴。","reasoning":"111.5 元對 FY2027 共識 EPS 7.16 元是 15.6 倍，對 FY2026 共識 7.38 元是 15.1 倍；但 7.38 元裡約 2.4 元是業外一次性，換成經常性 EPS 約 5.0 元，本益比約 22 倍。本益比 16.6 倍、股價營收比 5.26 倍、企業價值營收比 4.99 倍，都在四個年度端點中最高（不是五年連續分位）。PEG 以經常性 EPS 約 5.0 元到基準情境 FY2029 6.5 元的三年年化約 9% 計，15.6 ÷ 9 ≈ 1.7；若直接用共識 FY2025A→FY2027E 的 48% 會得出 0.3，但基期是谷底，不採用。基準情境 FY2031 EPS 6.8 元 × 13 倍＝88 元，較現價低約 21%；FY2027 基準 EPS 6.6 元 × 15 倍＝99 元，較現價低約 11%。賣方目標價分歧很大：2026 年 1 月高盛、大摩、小摩約 50–52.5 元，7 月本土投顧最高 160 元，9 月花旗 125 元，最高與最低相差逾 3 倍，不能當錨。同業本益比事實表未涵蓋，終端倍數只能對照自身歷史與前瞻倍數。","fact_refs":["f_price_at_dd","f_pe_current","f_pe_percentile","f_ps_current","f_ps_percentile","f_ev_s_current","f_ev_s_percentile","f_consensus_eps_fy1","f_consensus_eps_fy2","f_rev_consensus_fy2_m","f_ev_s_fwd","f_dividend_yield_ttm","f_rsi14"],"verdict_values":{"valuation":{"basis":"FY2027E 共識本益比（FY2026 含業外一次性，改用前瞻年度；週期股同時對照經常性 EPS）","tier":"成熟製程二線純晶圓代工","peers":{"expanded":false,"reason":"事實表同業對照只有利潤率，沒有同業本益比或股價淨值比，無法建立同層級倍數錨；中芯營收資料也缺失"},"fwd_pe":15.6,"peg":1.7,"percentile_5y":100,"val_light":"🟠","val_light_derivation":"偏貴：前瞻本益比 15.6 倍、經常性約 22 倍，股價營收比與企業價值營收比都在四個年度端點中最高（只有 4 個年度端點，不是五年連續分位）。基準情境五年後約 88 元、一年後約 99 元，都低於現價。股價兩週內由 130 元跌到 111.5 元，RSI 27.6 屬短線超賣，但不改變五年的算術。","upside_short_pct":-11.2,"upside_mid_pct":-20.7,"denominator_disputed":true,"denominator_note":"FY2026 EPS 7.38 元含 2Q26 約 300 億元投資與股利業外收益（約每股 2.4 元），元大估 2Q26 約 65% 獲利來自業外。15.1 倍與 16.6 倍兩個本益比都因此被壓低，經常性本益比約 22 倍，便宜論點不成立。"}}},"q6_how_wrong":{"verdict":"最可能看錯的地方有兩個：一是把 2027 年漲價當成新常態，二是低估矽光子、DTC 讓聯電從純成熟製程代工轉型成有第二曲線的公司。前者是主要風險。","reasoning":"判為中度陷阱。衰退信號只亮 1 項（EPS 成長被業外收益墊高），但有三件事讓陷阱風險不低：FY2026 EPS 約三分之一是一次性；倍數已在四個年度端點中最高；利用率 92% 下毛利率只有 34%，CFO 明說未來兩年折舊與原物料會壓毛利，不會接近前高。反方向看錯的可能：若 1Q27 毛利率衝上 38% 以上、2027 年 AI 相關營收翻倍，基準 EPS 要上調到共識 7.16 元以上。依據見反證紀錄三條。","fact_refs":["f_kpi4_eps","f_pe_current","f_pe_percentile","f_week26_return_pct","f_rsi14","f_kpi3"],"verdict_values":{"trap":{"verdict":"🟡","label":"週期高檔、一次性收益墊高 EPS 的中度陷阱"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":7.38,"pe":15.11,"basis":"FY2026E 共識 EPS（當年度口徑，與終端 FY2031 當年 EPS 同口徑）。含約 2.4 元業外一次性，經常性約 5.0 元，起點本益比因此看起來偏低。"},"eps":{"bull":[7.4,8.0,8.8,9.8,10.5],"base":[6.6,6.2,6.5,7.0,6.8],"bear":[5.8,4.5,3.8,4.2,4.6]},"pe":{"bull":16,"base":13,"bear":11},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":2.3,"net_buyback":0},"second_stage":{"bull_cagr_pct":6,"base_cagr_pct":3},"max_dd":{"lo":-62,"hi":-40,"basis":"從 111.5 元跌回 104 週均線 68.3 元約 −39%，跌回 250 週均線 52.5 元約 −53%。上一輪 2022→2025 年 EPS 由 6.87 元降到 3.27 元（−52%），毛利率由 45% 降到 29%。空頭情境終點 50.6 元（−55%）。下緣取 −62%，涵蓋跌破 250 週均線的過衝；上緣 −40% 對應只跌回 104 週均線。","trigger_time":null},"basis":{"bull":"2027 年漲價全數落地，AI 相關營收 2029 年占營收逾四分之一且毛利率高於公司平均，折舊高峰過後毛利率升到 38–40%；EPS 由 7.4 元升到 10.5 元。終端 16 倍約等於現在的本益比 16.6 倍。","base":"2027 年 ASP 漲約 10%，但量受產能限制，折舊與原物料吃掉一部分，EPS 6.6 元；2028 年折舊高峰加上消費端偏弱，回落到 6.2 元；2029 年起新產能與 AI 業務補回，2031 年在中循環位置約 6.8 元。終端 13 倍低於四個年度端點的最高值（現值 16.6 倍）；同業本益比事實表未涵蓋。","bear":"2027 年漲價只部分落地；2028–2029 年中國與台系新產能加上聯電自己的擴產同時開出，利用率回到 70% 區間，EPS 跌到 3.8 元後小幅回升到 4.6 元。終端 11 倍，取成長降到 10% 以下時的倍數壓縮。"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"上一輪 2022→2025 年 EPS 由 6.87 元降到 3.27 元，毛利率由 45.1% 降到 29.0%。中芯、華虹、力積電、世界先進持續擴充 28–90 奈米，聯電 2025 年得要求供應商降價 15% 來保毛利。","assumption":"本輪漲價是 AI 電源需求加上台積電、三星減少 8 吋產能造成的週期性緊俏，供給可逆。","consequence":"2028–2029 年中國與台系新產能和聯電約 82 億美元擴產同時開出，又碰上 AI 基建放緩與消費電子量縮：利用率回到 70% 區間、毛利率跌破 30%、EPS 回到 4 元上下、倍數 11 倍，股價約 45–50 元，五年虧損約 55%。","ruling":"採納，對應空頭情境 30% 機率。這個故事與 Single Thing 部分重疊：漲價落空會是它最早出現的訊號，已回補進觸發條件。","watch":"利用率連 2 季低於 85%、混合 ASP 季減、月營收年增轉負","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#2"],"fact_refs":["f_kpi7","f_kpi3"]},{"view":"論點成功但股東經濟變差","evidence":"2026-10-28 CFO：折舊至少連兩年增加，加上原物料上漲，未來兩年毛利率受壓，不會接近前高。董事會在約 50 億美元之外，再核准約 32 億美元。2026-07-29 CFO 也說只看 EBITDA 利潤率，不與歷史毛利率比較。","assumption":"矽光子、DTC、TFLN 都成功，AI 營收照管理層路徑成長。","consequence":"成長靠大量資本堆出來：2027–2028 年 FCF 利潤率由 25.8% 降到個位數，股利成長停滯。新產能報酬若低於現有約 12% 的 ROIC，每股價值不升反降。管理層改口只談 EBITDA，本身也是警訊。","ruling":"採納。基準情境 FY2028 EPS 由 6.6 元回落到 6.2 元，就是在反映折舊高峰；股利殖利率維持 2.3%，不上調。","watch":"2027 年折舊成長率、資本支出指引、TTM FCF 利潤率","evidence_refs":[],"fact_refs":["f_kpi5","f_peer_2303_tw_fcf_margin_pct"]},{"view":"價格已反映太多","evidence":"本益比 16.6 倍、股價營收比 5.26 倍、企業價值營收比 4.99 倍，都在四個年度端點中最高；26 週漲 46.7%。2Q26 約 65% 獲利來自業外，經常性本益比約 22 倍。","assumption":"市場已把 2027 年漲價和 AI 第二曲線都算進股價。","consequence":"即使 2027 年 EPS 達到共識 7.16 元，給 13 倍也只值 93 元；倍數一回到中期水準，就有約 15–20% 下行空間。","ruling":"採納。反方的論點是股價兩週內已由 130 元跌到 111.5 元，RSI 27.6 超賣，短線可能反彈；但這不改變五年的算術，不追反彈。","watch":"前瞻本益比是否回到 12 倍以下（對應約 85 元）","evidence_refs":["capital_markets_pricing#1"],"fact_refs":["f_pe_current","f_ps_current","f_ev_s_current","f_week26_return_pct","f_rsi14"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 🟡 → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=🟡","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 130.0 → 本次 111.5（-14.2%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=130.0","side_b":"本次 price_at_dd=111.5","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 130 元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 130 元：Bull 價 194.4、Bear 價 54.6，五年期望值 −13.7%，基準年化 −4.2%，不對稱比 0.7","side_b":"本次情境、股價仍用 130 元：Bull 價 168、Bear 價 50.6，五年期望值 −25.4%，基準年化 −7.4%，不對稱比 0.4","ruling":"先換情境、股價不動：五年期望值少 11.7 個百分點，基準年化少 3.2 個百分點。不對稱比由 0.7 變為 0.4。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 130 元：五年期望值 −25.4%，基準年化 −7.4%，不對稱比 0.4","side_b":"本次情境、股價 111.5 元：五年期望值 −13.0%，基準年化 −4.5%，不對稱比 0.77","ruling":"再換股價、情境不動：起點價下跌 14.2%，五年期望值多 12.4 個百分點，基準年化多 2.9 個百分點，不對稱比由 0.4 升到 0.77。合計五年期望值比前份多 0.7 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"現在就買 vs 觀望","cause":null,"prior_field":null,"side_a":"現在就買的最強論證：2027 年混合 ASP 年增約 10%，1Q27 起生效，管理層稱談判已到後期；利用率在低 90% 區間，多座廠滿載，電源與 FPGA 訂單積壓；矽光子平台通過多家雲端大廠驗證，AI 相關營收三年後占逾四分之一且毛利率高於平均。FY2027 共識本益比只有 15.6 倍，賣方近期目標價 125–160 元；股價兩週跌 14%，RSI 27.6 已超賣。","side_b":"利用率 92% 下毛利率只有 34%，CFO 說未來兩年折舊與原物料會壓毛利，不會接近前高。董事會再加約 32 億美元資本支出，2028 年後將與中國、台系新產能同時開出。FY2026 EPS 約 2.4 元是業外一次性，經常性本益比約 22 倍。基準情境五年後約 88 元，機率加權五年報酬約 −13%（未含股息）。","ruling":"選觀望。依據是基準情境終值低於現價；卡住進場的是估值，不是公司品質。決勝數據是 1Q27 毛利率與混合 ASP 季變化，約 2027 年 4 月底揭曉。若漲價落地且毛利率 ≥38%，基準 EPS 會上調到共識附近，屆時重跑研究。","evidence_level":"法說原話＋年度財報＋事實表估值","settle_metric":"1Q27 毛利率、1Q27 混合 ASP 季變化","if_then":["若 1Q27 毛利率 ≥38% 且混合 ASP 季增，則重跑研究，把基準 FY2027 EPS 上調到 7 元以上再決定倉位","若股價 ≤85 元且 4Q26 毛利率 ≥33%，則重跑研究，通過後首倉不超過 3%","反向：若 1Q27 混合 ASP 未季增或利用率跌破 85%，則空頭機率上調到 35% 以上，維持不碰","價格先走、證據未到：股價回到 130 元以上但 1Q27 數據還沒出來，不追"],"evidence_refs":[]},{"axis":"管理層 AI 營收目標一季內上修","cause":null,"prior_field":null,"side_a":"2026-07-29 Jason Wang：AI 相關營收今年約 3 億美元，三年內超過 10 億美元","side_b":"2026-10-28 Jason Wang：三年後 AI 曝險可能超過營收四分之一；同場又說 2027 年受產能限制，新廠大部分 2028 年底才開出","ruling":"不採信也不否定，標為未證、持續監測。以 2026 年營收規模計，四分之一約 700 億元，明顯大於上一季講的 10 億美元目標；只隔一季就大幅上修，而且 AI 定義包含電源管理、連接、FPGA，口徑偏寬。預先登記：2027 年 AI 相關營收若未達 6 億美元（2026 年的兩倍），上修目標視為證偽，H2 降為削弱。","evidence_level":"法說原話（兩場）","settle_metric":"2027 年 AI 相關營收（4Q27 法說揭露）","if_then":["若 2027 年 AI 相關營收 ≥6 億美元，則維持 H2 並把多頭機率檢討上調","若未達 6 億美元，則 H2 降為削弱，多頭機率降到 20%"],"evidence_refs":[]},{"axis":"折舊成長口徑","cause":null,"prior_field":null,"side_a":"2026-07-29 Chi-Tung Liu：折舊未來至少兩年每年成長約低十位數百分比","side_b":"2026-10-28 Chi-Tung Liu：逐字稿寫 2027 年折舊『低個位數成長』、2028 年可能更多，同時又說這是需要抵銷的『大數字』","ruling":"不採信為下修。同場追加約 32 億美元資本支出，CFO 也說折舊是『大數字』、毛利率未來兩年受壓，與低個位數成長方向矛盾，較可能是聽打誤差。基準情境仍按低十位數成長計入，等 4Q26 法說確認。","evidence_level":"法說原話（兩場），逐字稿可能有誤","settle_metric":"2027 年折舊指引（4Q26 法說）","if_then":["若 4Q26 法說確認 2027 年折舊只是低個位數成長，則基準 FY2027–2028 EPS 上調約 0.3 元"],"evidence_refs":[]},{"axis":"3Q26 毛利率指引與實績","cause":null,"prior_field":null,"side_a":"2026-07-29 管理層指引 3Q26 毛利率在 30% 中段（媒體報導 34–36%），利用率逾 90%","side_b":"3Q26 實績毛利率 34%，利用率 92%；4Q26 指引毛利率與 3Q26 相當","ruling":"達標，但落在區間下緣。利用率超過指引、毛利率卻只到區間底部，表示新加坡廠折舊與成本上升已吃掉利用率紅利；這是基準情境 FY2028 EPS 回落的依據之一。","evidence_level":"法說指引對照實績","settle_metric":"4Q26 毛利率是否維持 34% 左右","if_then":["若 4Q26 毛利率低於 33%，則基準 FY2027 EPS 下修到 6.2 元"],"evidence_refs":[]},{"axis":"共識 2027 年營收 vs 產能限制","cause":null,"prior_field":null,"side_a":"共識 FY2027 營收 3,466 億元，較 FY2026 共識 2,811 億元年增約 23%","side_b":"管理層：2027 年混合 ASP 年增約 10%，出貨受產能限制，產能成長『不夠』；新廠 2028 年底才開出","ruling":"採用管理層口徑。價 +10% 加上低個位數量增，約可推出 12–16% 營收成長，共識高出約 6–10%。本研究基準 FY2027 EPS 6.6 元，比共識 7.16 元低約 8%，這也是本研究比賣方悲觀的主要理由。","evidence_level":"法說原話對照共識","settle_metric":"1Q27 營收指引、2027 年 1–3 月月營收年增率","if_then":["若 2027 年 1–3 月月營收年增率平均高於 20%，則基準營收與 EPS 往共識靠攏"],"evidence_refs":[]},{"axis":"FY2026 EPS 品質","cause":null,"prior_field":null,"side_a":"2Q26 EPS 3.39 元，1–9 月 EPS 6.00 元，FY2026 共識 7.38 元","side_b":"2Q26 投資與股利業外收益約 300 億元，元大估約 65% 獲利來自業外","ruling":"採納後者：FY2026 EPS 不當估值分母，改用 FY2027 共識，並對照經常性 EPS 約 5.0 元。","evidence_level":"新聞稿＋法說原話＋賣方報告","settle_metric":"4Q26 業外收益是否回到正常水準","if_then":["若 4Q26 再出現大額業外處分利益，則同樣從經常性 EPS 中扣除"],"evidence_refs":["capital_markets_pricing#1"]},{"axis":"產業態勢三軸","cause":null,"prior_field":null,"side_a":"結構轉好：TrendForce 估 8 吋稼動率 2026 年接近 90%、1H27 仍逾 80%，成熟製程 2027 年漲價難以避免；聯電 2027 年 8 吋、12 吋都漲價","side_b":"競爭惡化：中芯、華虹、力積電、世界先進持續擴充 28–90 奈米，2026 年初聯電因中國對手而漲價保守。其他結構變數：美國 232 關稅 25%，豁免偏向在美設廠的一線廠","ruling":"雙向拉鋸。到 1H27 為止結構轉好占上風，2028 年起新產能到位後競爭惡化占上風；關稅屬其他結構變動，以毛利率吸收能力追蹤，不做預測。","evidence_level":"第三方研究＋新聞＋券商報告","settle_metric":"季利用率、2H27 混合 ASP 季變化","if_then":["若 2H27 混合 ASP 轉為季減，則判定競爭惡化已占上風，空頭機率上調到 35%"],"evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#2","reg_tariff_export#2"]},{"axis":"前份漂移：股價與情境機率","cause":"價格變動","prior_field":["max_dd_pct","p_bull_pct","p_bear_pct"],"side_a":"前份：股價 130 元；多頭 25%、空頭 30%；最大回撤 −65%","side_b":"本次：股價 111.5 元；多頭 25%、基準 45%、空頭 30% 不變；最大回撤改為 −40%～−62% 區間（起點較低，跌到 250 週均線的幅度縮小）；裁決與角色依新價格重算","ruling":"機率不動。3Q26 法說有正面消息（2027 年 ASP +10%），也有負面消息（毛利率停在 34%、資本支出再加碼），兩者大致抵銷。","evidence_level":"事實表股價＋法說","settle_metric":"1Q27 毛利率","if_then":[],"evidence_refs":[]},{"axis":"前份漂移：循環位置","cause":"新證據","prior_field":["cycle_position"],"side_a":"中循環","side_b":"晚循環","ruling":"依據 3Q26 法說：利用率 92%、多座廠滿載，2027 年出貨受產能限制，成長改由價帶動，董事會再加約 32 億美元資本支出。由量轉價、產能滿載、擴產加速，都是晚循環的特徵。","evidence_level":"法說原話","settle_metric":"2027 年資本支出指引、利用率","if_then":["若 2027 年利用率回落到 85% 以下且資本支出延後，則重新判斷是否已進入下行"],"evidence_refs":[]},{"axis":"前份漂移：基本面結論維持","cause":"新證據","prior_field":["signal","val","trap","moat_trend","runway_post_y5","archetype"],"side_a":"前份：評級 C、估值偏貴、中度陷阱、護城河持平、五年後跑道中等、循環商品型","side_b":"本次相同：用 3Q26 法說與 8–9 月營收（年增 30.7%、27.2%）重新檢視後，正負證據互相抵銷","ruling":"維持。股價下跌 14% 仍沒有把估值拉回合理區間：前瞻本益比 15.6 倍，經常性約 22 倍。","evidence_level":"法說＋月營收＋事實表估值","settle_metric":"1Q27 毛利率","if_then":[],"evidence_refs":[]},{"axis":"前份漂移：重啟條件","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"股價 ≤85 元，或 2027 年 ASP 調升經法說確認且 1Q27 毛利率 ≥38%（任一成立後重跑研究）","side_b":"股價 ≤85 元，或 1Q27 毛利率 ≥38% 且混合 ASP 季增（任一成立後重跑研究）","ruling":"3Q26 法說已確認 2027 年混合 ASP 年增約 10%，舊條件中『法說確認』那一半已經被消化，改看 1Q27 實際季增，避免把指引當成實現。重跑研究、進場首倉的價格門檻 85 元不變：基準終值降到約 88 元後，85 元以下的多空機率加權比約 2 倍，才開始有進場的不對稱。","evidence_level":"法說原話＋情境樹","settle_metric":"1Q27 毛利率、混合 ASP 季變化、收盤價","if_then":[],"evidence_refs":[]},{"axis":"前份漂移：停損指標","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設停損指標","side_b":"利用率連 2 季低於 85%、1Q27 混合 ASP 未季增、季毛利率低於 32%、月營收年增連 3 個月為負；觸發後如已持有則減碼或清倉，研究轉為迴避","ruling":"本次補設，讓觀望期間也有可驗證的空方門檻；前份沒有可比的門檻。","evidence_level":"方法補強","settle_metric":"季利用率、季毛利率、月營收","if_then":[],"evidence_refs":[]},{"axis":"前份漂移：Single Thing","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設唯一致命點","side_b":"2027 年合約漲價落空：1Q27 混合 ASP（美元）沒有季增","ruling":"Single Thing 由空白改為 2027 年漲價是否落地，這是 FY2027 EPS 最大的單一敏感項（約每股 1.8–1.9 元）。若發生，已持有者清倉，研究維持不碰。","evidence_level":"法說原話＋情境敏感度","settle_metric":"1Q27 混合 ASP 季變化","if_then":[],"evidence_refs":[]}],"triggers":[{"n":1,"text":"股價收盤 ≤85 元時重跑研究，通過後首倉不超過 3%","type":"估值rearm","maps_to":"重啟條件","metric":"收盤價","threshold":"≤85 元","action":"重跑研究；通過後首倉 ≤3%","source_freq":"每日收盤","date":null,"evidence_refs":[]},{"n":2,"text":"1Q27 混合 ASP（美元）沒有季增，2027 年漲價落空","type":"Single Thing","maps_to":"Single Thing","metric":"1Q27 混合 ASP 季變化","threshold":"≤0%","action":"空頭機率升到 40%；研究維持不碰，如已持有則清倉","source_freq":"每季法說","date":"2027-04","evidence_refs":[]},{"n":3,"text":"1Q27 毛利率 ≥38% 且混合 ASP 季增，代表漲價確實轉成毛利","type":"假設驗證","maps_to":"H1","metric":"1Q27 毛利率","threshold":"≥38%","action":"重跑研究，基準 FY2027 EPS 上調到 7 元以上","source_freq":"每季法說","date":"2027-04","evidence_refs":[]},{"n":4,"text":"利用率連 2 季跌破 85%，價格競爭回來","type":"風險","maps_to":"R2","metric":"季產能利用率","threshold":"<85%，連 2 季","action":"空頭機率升到 35% 以上並下修基準 EPS；重啟條件的價格門檻同步下調","source_freq":"每季法說","date":null,"evidence_refs":["competitive_share_entrants#1"]},{"n":5,"text":"2027 年 AI 相關營收達 6 億美元以上","type":"假設驗證","maps_to":"H2","metric":"AI 相關營收（管理層揭露）","threshold":"≥6 億美元","action":"未達則 H2 降為削弱，多頭機率降到 20%","source_freq":"年度（4Q27 法說）","date":"2028-01","evidence_refs":[]},{"n":6,"text":"2027 年資本支出指引高於 40 億美元，或 TTM FCF 利潤率跌破 5%","type":"風險","maps_to":"R3","metric":"年度資本支出指引、TTM FCF 利潤率","threshold":"高於 40 億美元，或低於 5%","action":"下修基準 FY2028–2029 EPS 與股利假設","source_freq":"每季法說","date":"2027-01","evidence_refs":[]},{"n":7,"text":"關稅或匯率讓單季毛利率低於指引下緣 2pp 以上","type":"風險","maps_to":"R4","metric":"季毛利率對照指引","threshold":"低於指引下緣 ≥2pp","action":"視為吸收失敗，空頭機率上調 5pp","source_freq":"每季法說","date":null,"evidence_refs":["reg_tariff_export#0","reg_tariff_export#2"]},{"n":8,"text":"4Q26 法說：檢視 1Q27 ASP 指引、2027 年折舊與資本支出","type":"複審日期","maps_to":"H1","metric":"1Q27 ASP 指引、2027 年折舊成長率","threshold":"ASP 季增指引 ≥5%","action":"複審情境樹；低於門檻則提前下修","source_freq":"單次","date":"2027-01","evidence_refs":[]}],"kill_metrics":[{"metric":"季產能利用率","bear_threshold":"連續 2 季低於 85%","window":"4Q26–4Q27","source":"聯電季度法說與新聞稿","last_status":"ok"},{"metric":"季度混合 ASP（美元）","bear_threshold":"1Q27 未季增，或 2027 年全年年增低於 5%","window":"1Q27–4Q27","source":"聯電季度法說","last_status":"unknown"},{"metric":"季毛利率","bear_threshold":"低於 32%（跌破 2Q26 的 32.5%）","window":"4Q26–4Q27","source":"聯電季度新聞稿","last_status":"ok"},{"metric":"月營收年增率","bear_threshold":"連續 3 個月為負","window":"2026-11 至 2027-12","source":"公開資訊觀測站月營收","last_status":"ok"}],"evidence_dismissed":[],"action_conditions":{"rearm_trigger":"股價 ≤85 元，或 1Q27 毛利率 ≥38% 且混合 ASP 季增（任一成立後重跑研究）","exec_line":"不追。重跑研究通過、且循環位置不在晚循環以後，首倉不超過 3%；股價續漲但 1Q27 數據未出，不追。","holding_cap":"重跑研究前 0%；通過後 ≤3%"}},"decision_inputs":{"signal":"C","ma":"🟡","cycle_position":"晚循環","cycle_verdict":"頂部觀望","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"共識 FY2027 營收年增約 23%，高於管理層「價 +10%、量受產能限制」可推出的 12–16%；部分賣方又把含業外一次性收益的 FY2026 EPS 當分母。本研究基準 FY2027 EPS 6.6 元，低於共識 7.16 元。","momentum_overheated":false,"cycle_gates_pass":false,"qc49_inherit_prior":true,"wait_for_price":true,"wait_for_price_condition":"股價 ≤85 元，或 1Q27 毛利率 ≥38% 且混合 ASP 季增","prior_verdict":"觀望","prior_role":"追蹤"},"decision_out":{"role":"追蹤","row_hit":"6","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='C'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='C'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":true,"basis":"signal='C'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=共識 FY2027 營收年增約 23%，高於管理層「價 +10%、量受產能限制」可推出的 12–16%；部分賣方又把含業外一次性收益的 FY2026 EPS 當分母。本研究基準 FY2027 EPS 6.6 元，低於共識 7.16 元。"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='C', runway='🟡', val='🟠', moat_trend='→', week26=46.71, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='循環/商品', cycle_position='晚循環', moat='C', moat_trend='→', cycle_gates_pass=False"},{"row":"6/7/7a-verdict","condition":"Soft Veto 生效 → 觀望（max-severity wins；8a/8b 未能繞過）","hit":true,"basis":"soft_veto_rows=['6']"},{"row":"QC-49","condition":"qc49_inherit_prior=True 但前次裁決與矩陣機械輸出方向相同，無需承繼","hit":false,"basis":"prior_verdict='觀望', 矩陣機械輸出='觀望'"},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":null,"requires_critic":[],"verdict":"觀望"},"thesis":{"H":[{"id":"H1","text":"成熟製程漲價週期成立：2027 年混合 ASP 年增約 10%，毛利率在折舊增加下仍升到 37% 以上","2y":"FY2027 毛利率 ≥37%，混合 ASP 年增 ≥8%","5y":null,"10y":null,"threshold":"1Q27 毛利率 ≥36%；FY2027 混合 ASP 年增 ≥8%","source":"聯電季度法說與新聞稿","drift_rule":"季毛利率連 2 季低於門檻 5% 以上為削弱，連 3 季低於門檻 10% 以上為反轉"},{"id":"H2","text":"AI 相關業務（矽光子、DTC、TFLN、電源、連接）2029 年占營收 20% 以上，且毛利率高於公司平均","2y":null,"5y":"2029 年 AI 相關營收占比 ≥20%","10y":null,"threshold":"2027 年 AI 相關營收 ≥6 億美元；2029 年占比 ≥20%","source":"法說管理層揭露（每年第四季法說）","drift_rule":"連 4 季落後門檻路徑 5% 以上為削弱，連 6 季落後 10% 以上為反轉"},{"id":"H3","text":"下一次下行期獲利不再腰斬：谷底年度營業利益率守住 18%（2025 年谷底為 18.4%），利用率谷底不低於 75%","2y":null,"5y":"2027–2031 年每年營業利益率 ≥18%","10y":null,"threshold":"年度營業利益率 ≥18%；季利用率 ≥75%","source":"年度財報、季度法說","drift_rule":"TTM 營業利益率連 4 季低於 18% 達 5% 以上為削弱，連 6 季低於 10% 以上為反轉"}],"R":[{"id":"R1","text":"2027 年漲價沒有轉成毛利：原物料、能源與新廠折舊吃掉 ASP 漲幅","h_ref":"H1","clock":"⚡","threshold":"1Q27 毛利率低於 34%（不高於 3Q26）","evidence_refs":[]},{"id":"R2","text":"中國與台系二線廠擴充 28–90 奈米，價格競爭回來、利用率回落","h_ref":"H3","clock":"🔥","threshold":"利用率連 2 季低於 85%，或 2H27 混合 ASP 季減","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#2"]},{"id":"R3","text":"約 82 億美元擴產遇上 AI 基建投資放緩，2029–2030 年新產能閒置，折舊壓垮毛利","h_ref":"H2","clock":"🐢","threshold":"2028 年矽光子或 DTC 客戶承諾延後，或 2029 年利用率低於 80%","evidence_refs":[]},{"id":"R4","text":"美國 232 關稅與出口管制偏向在美設廠的一線廠，二線代工得自行吸收關稅或流失美系客戶","h_ref":"H3","clock":"🔥","threshold":"關稅相關因素讓單季毛利率低於指引下緣 2pp 以上","evidence_refs":["reg_tariff_export#0","reg_tariff_export#2","reg_tariff_export#1"]},{"id":"R5","text":"最大客戶占比由 10% 升到 12%，集中度若持續上升，議價權會往客戶移動","h_ref":"H3","clock":"🐢","threshold":"單一客戶占年營收超過 20%","evidence_refs":["customer_concentration_credit#0"]}],"single_thing":{"description":"2027 年合約漲價落空：1Q27 混合 ASP（美元）沒有季增","why_fatal":"基準 FY2027 EPS 6.6 元裡，ASP 年增約 10% 貢獻約 280 億元營收（2026 年共識營收 2,811 億元 × 10%），幾乎全數落到稅前，稅後約每股 1.8–1.9 元，是 FY2027 EPS 最大的單一敏感項。漲價落空，EPS 就回到 5 元上下，前瞻倍數也會往 12 倍以下收縮。","if_happens":"空頭機率升到 40%，研究維持不碰，重啟條件只保留股價門檻、取消事件那一半；如已持有則清倉。","how_monitor":"4Q26 法說（2027 年 1 月底）CFO 已承諾會給 1Q27 ASP 指引；1Q27 法說（2027 年 4 月底）公布實績；同時看 2027 年 1–3 月月營收年增率是否明顯跳升。","probability":"20%：管理層稱談判已到後期、信心高；但 PC 與中低階手機量縮、中國對手擴產，可能讓部分客戶延後接受漲價。"}},"appendix_a":{"growth_durability":5,"quality_score":6,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":15.6,"peg_fy2":1.7,"stress":{"pass":2,"total":5}},"eps_meta":{"base_eps_path":{"FY2025A":3.27,"FY2026E":7.38,"FY2027E":7.16,"FY2028E":null},"fy_end_month":12,"eps_basis":"IFRS 稀釋 EPS（台幣，歸屬母公司）；FY2026E 含 2Q26 約 300 億元業外一次性收益，約每股 2.4 元；FY2028E 共識事實表未涵蓋"},"catalysts":[{"date":"2027-01","date_precision":"month","type":"guidance","event":"4Q26 法說：1Q27 ASP 指引與 2027 年資本支出、折舊","impact":"高","watch":"ASP 季增幅度；折舊成長是否為低十位數"},{"date":"2027-04","date_precision":"month","type":"guidance","event":"1Q27 法說：漲價後第一季實績","impact":"高","watch":"毛利率是否 ≥38%；混合 ASP 是否季增"},{"date":"2027-Q4","date_precision":"quarter","type":"product","event":"與英特爾合作的 12 奈米 tape-out，矽光子 12 吋平台對一般客戶開放（2027 年內）","impact":"中","watch":"首批客戶 tape-out 與營收認列時點"},{"date":"2028-Q4","date_precision":"quarter","type":"capacity","event":"新加坡矽光子、台南 DTC、8 吋 TFLN 新產能開始爬坡","impact":"中","watch":"客戶承諾是否延後；新產能利用率"}]}
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
