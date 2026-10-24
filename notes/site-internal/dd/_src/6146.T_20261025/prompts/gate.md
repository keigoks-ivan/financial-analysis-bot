你是 DD 管線 v20 的判斷層閘（gate），標的 6146.T（20261025）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（24 條）
- `f_kpi0_gaap_jgaap`（q1_business）｜營收（GAAP/JGAAP，單季）＝1428 億日圓｜期間與口徑：FY2027 Q2（7–9月，會計年度 2026-04～2027-03，公告於 2026-10-22）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司決算短信（日本基準）https://www.disco.co.jp/jp/ir/library/doc/fr/fr20261022.pdf；決算補足説明資料 https://www.disco.co.jp/jp/ir/library/doc/film/20261022.pdf（numbers.latest_quarter_kpis.items[0]，as_of FY2027 Q2（7–9月，會計年度 2026-04～2027-03，公告於 2026-10-22））
- `f_kpi1_jgaap`（q1_business）｜營業利益（JGAAP，單季）＝676 億日圓｜期間與口徑：FY2027 Q2（7–9月，會計年度 2026-04～2027-03，公告於 2026-10-22）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司決算短信（日本基準）https://www.disco.co.jp/jp/ir/library/doc/fr/fr20261022.pdf；決算補足説明資料 https://www.disco.co.jp/jp/ir/library/doc/film/20261022.pdf（numbers.latest_quarter_kpis.items[1]，as_of FY2027 Q2（7–9月，會計年度 2026-04～2027-03，公告於 2026-10-22））
- `f_kpi2_jgaap`（q1_business）｜營業利益率（JGAAP，單季）＝47.4 %｜期間與口徑：FY2027 Q2（7–9月，會計年度 2026-04～2027-03，公告於 2026-10-22）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司決算短信（日本基準）https://www.disco.co.jp/jp/ir/library/doc/fr/fr20261022.pdf；決算補足説明資料 https://www.disco.co.jp/jp/ir/library/doc/film/20261022.pdf（numbers.latest_quarter_kpis.items[2]，as_of FY2027 Q2（7–9月，會計年度 2026-04～2027-03，公告於 2026-10-22））
- `f_kpi3_shipments`（q1_business）｜出貨額（shipments，單季，歷史新高）＝1486 億日圓｜期間與口徑：FY2027 Q2（7–9月，會計年度 2026-04～2027-03，公告於 2026-10-22）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司決算短信（日本基準）https://www.disco.co.jp/jp/ir/library/doc/fr/fr20261022.pdf；決算補足説明資料 https://www.disco.co.jp/jp/ir/library/doc/film/20261022.pdf（numbers.latest_quarter_kpis.items[3]，as_of FY2027 Q2（7–9月，會計年度 2026-04～2027-03，公告於 2026-10-22））
- `f_kpi6_fy2027_q3_10_12`（q1_business）｜管理層指引：FY2027 Q3（10–12月）單季＝營收億 1324；營業利益億 581；營業利益率% 43.9；出貨額億 1496；假設匯率 US$151 円 億日圓｜期間與口徑：指引對象 Q3 FY2027（10–12月）；公告於 2026-10-22／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司決算短信（日本基準）https://www.disco.co.jp/jp/ir/library/doc/fr/fr20261022.pdf；決算補足説明資料 https://www.disco.co.jp/jp/ir/library/doc/film/20261022.pdf（numbers.latest_quarter_kpis.items[6]，as_of 指引對象 Q3 FY2027（10–12月）；公告於 2026-10-22）
- `f_kpi7_4_12`（q1_business）｜管理層指引：4–12月累計（首度揭露）＝營收百萬円 389500；營業利益百萬円 174700；經常利益百萬円 173400；純利百萬円 121900；出貨額億 4342｜期間與口徑：FY2027 4–12月累計指引；公告於 2026-10-22／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司決算短信（日本基準）https://www.disco.co.jp/jp/ir/library/doc/fr/fr20261022.pdf；決算補足説明資料 https://www.disco.co.jp/jp/ir/library/doc/film/20261022.pdf（numbers.latest_quarter_kpis.items[7]，as_of FY2027 4–12月累計指引；公告於 2026-10-22）
- `f_earnings_recency`（q1_business）｜最近一次財報日＝2026-10-22 date｜期間與口徑：2026-10-22／距今 2 個交易日｜kind：realized
  - 來源：—（numbers.earnings_recency，as_of 2026-10-22）
- `f_kpi4_cf_cf`（q4_capital）｜自由現金流（公司定義＝營業CF＋投資CF，上半期累計）＝568.93 億日圓｜期間與口徑：FY2027 上半期累計（2026-04-01～09-30，公告於 2026-10-22）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司決算短信（日本基準）https://www.disco.co.jp/jp/ir/library/doc/fr/fr20261022.pdf；決算補足説明資料 https://www.disco.co.jp/jp/ir/library/doc/film/20261022.pdf（numbers.latest_quarter_kpis.items[4]，as_of FY2027 上半期累計（2026-04-01～09-30，公告於 2026-10-22））
- `f_kpi5`（q4_capital）｜營運現金流（上半期累計）＝1117.08 億日圓｜期間與口徑：FY2027 上半期累計（2026-04-01～09-30，公告於 2026-10-22）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司決算短信（日本基準）https://www.disco.co.jp/jp/ir/library/doc/fr/fr20261022.pdf；決算補足説明資料 https://www.disco.co.jp/jp/ir/library/doc/film/20261022.pdf（numbers.latest_quarter_kpis.items[5]，as_of FY2027 上半期累計（2026-04-01～09-30，公告於 2026-10-22））
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝1733.88 USD/share｜期間與口徑：2026-10-25／yfinance 分析師共識平均（Koyfin 快照無此檔）；幣別同報價｜kind：estimate
  - 來源：yfinance earnings_estimate（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-10-25）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝2184.95 USD/share｜期間與口徑：2026-10-25／yfinance 分析師共識平均（Koyfin 快照無此檔）；幣別同報價｜kind：estimate
  - 來源：yfinance earnings_estimate（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-10-25）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝566167.79 JPY m｜期間與口徑：2026-10-25／yfinance revenue_estimate 0y 平均（16 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-10-25）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝676783.41 JPY m｜期間與口徑：2026-10-25／yfinance revenue_estimate +1y 平均（21 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-10-25）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝-342410.99 JPY m｜期間與口徑：2026-10-25／yfinance 最新一季：總債務 0.0、現金 342410.99（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-10-25）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝108.47 m shares｜期間與口徑：2026-10-25／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-10-25）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝1.14 %｜期間與口徑：2026-10-25／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-10-25）
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝49290.0 USD｜期間與口徑：2026-10-23（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-10-23（RTH 收盤，UTC））
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝33.52 x｜期間與口徑：2026-10-23（RTH 收盤，UTC）／4 個年度端點內的分位＝30.5｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-10-23（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝30.5 %｜期間與口徑：2026-10-23（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-10-23（RTH 收盤，UTC））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝10.71 x｜期間與口徑：2026-10-23（RTH 收盤，UTC）／4 個年度端點內的分位＝40.1｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-10-23（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝10.02 x｜期間與口徑：2026-10-23（RTH 收盤，UTC）／4 個年度端點內的分位＝39.7｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-10-23（RTH 收盤，UTC））
- `f_ev_s_fwd`（q5_valuation）｜EV/S（EV ÷ FY1 共識營收）＝8.84 x｜期間與口徑：2026-10-25／f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）｜kind：estimate
  - 來源：—（numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m，as_of 2026-10-25）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝-31.02 %｜期間與口徑：2026-10-23（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-10-23（RTH 收盤，UTC））
- `f_rsi14`（q5_valuation）｜RSI(14)＝33.67｜期間與口徑：2026-10-23（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-10-23（RTH 收盤，UTC））

### findings_digest 中方向為負或來源衝突的條目（3 條）
- `competitive_share_entrants#0`（competitive_share_entrants｜方向 -｜狀態 ok）：Morningstar 熊市論述：中國半導體自給政策可能讓當地設備商快速進步，削弱 DISCO 產業領導地位並威脅份額；屬通用風險論述，非已記錄的對手拿單事件。Morningstar 估 DISCO 在切割／研磨設備約 60%-70% 份額（2025）。
  - 來源：Morningstar Disco Corp 6146 quote page（as_of 2025-12-31）｜affects：moat_trend、decision_inputs.bear
- `geo_supply_chain#2`（geo_supply_chain｜方向 -｜狀態 ok）：第三方 SWOT 稱中國市場約占營收 35%、製造產能逾 80% 在日本（二手資料，未核對公司申報）
  - 來源：dcf-analysis.com DISCO SWOT（as_of 2026-04-01）｜affects：decision_inputs.bear、thesis.R
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：DISCO風險揭露：若出現取代精密鑽石刀輪（主力產品）的新加工技術，可能影響業績；公司持續開發雷射與電漿加工技術因應
  - 來源：envalith DISCO 6146 risks（as_of 2026-06-30）｜affects：moat_trend、decision_inputs.bear

### 事實表自陳的缺口（1 條）
- q2_moat：evidence.numbers.peer_financials 無資料，護城河同業數字整張缺——事實表 agent 須補，補不到時判斷者要在 moat.peer_na_reason 說明為何沒有可比同業。

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/6146.T_20261025/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":122500,"bear_5y_price":36000,"p_bull_pct":20,"p_bear_pct":35,"upside_5y_pct":36.3,"ev5y_pct":36.6,"irr_base_pct":6.4,"asym_ratio":3.1,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":1733.88,"pe":28.43,"basis":"FY1（2027 年 3 月期）共識 EPS，現價前瞻倍數；終端倍數同為前瞻一年口徑"},"eps":{"bull":[1800,2350,2750,3100,3500],"base":[1650,1950,2050,2200,2400],"bear":[1550,1300,1450,1650,1800]},"pe":{"bull":35,"base":28,"bear":20},"p":{"bull":20,"base":45,"bear":35},"yield_pct":{"dividend":1.14,"net_buyback":0},"second_stage":{"bull_cagr_pct":12,"base_cagr_pct":8},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

[本次無舊逐字稿摘錄]

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 2 | 3 |
| customer_second_source | none | 0 | 2 |
| customer_concentration_credit | found | 1 | 2 |
| supply_demand_durability | found | 4 | 3 |
| regulatory_antitrust | found | 1 | 3 |
| reg_tariff_export | found | 2 | 4 |
| geo_supply_chain | found | 3 | 2 |
| end_markets | found | 3 | 4 |
| substitute_technology | found | 1 | 2 |
| channel_business_model_shift | none | 0 | 2 |
| capital_markets_pricing | found | 3 | 4 |
| major_events | none | 0 | 5 |

未涵蓋／不適用軸的查詢詞原文（供判相關性）：
- **customer_second_source**（none）：6146.T DISCO largest customer second-source OR in-house 2026；DISCO Corporation dicing grinding competitor customer diversify supplier second source 2026
- **channel_business_model_shift**（none）：DISCO Corporation 6146 distribution channel OR business model shift 2026；DISCO Corp semiconductor equipment direct sales subscription OR platform OR "go-to-market" 2026
- **major_events**（none）：6146.T DISCO acquisition merger 2025 2026；6146.T DISCO class action lawsuit securities fraud；6146.T DISCO clinical trial FDA approval 2025 2026；6146.T DISCO product launch recall warning letter；6146.T DISCO SEC investigation restatement

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260522","verdict":"A 級核心候選：FY25 actual +11.1% revenue / +10.9% OI / OPM 42.3% 六連年創高；FY26 cumulative shipment ¥438B guide + Q1 FY26 +14% YoY 加速；S 級護城河 10/10、dicing/grinding 65% 近壟斷 + 耗材 40% recurring；估值 PEG 3.07 (cycle base 偏差)盲點 1 救援後 🟡 合理；建議分批進場，等回測 BB 中軌 ¥68,377 或 W52 ¥53,225 後加碼。","role":null,"H":{"status":"ok","format":"text","text":"B｜三個核心假設 + 三層時間軸（v12.3 強化 sourced floor + 漂移觸發條件）\n\nH1：TSMC CoWoS 2026 年底達 130K wafer/mo 擴產 + HBM4 量產帶動 DISCO 訂單 ≥ ¥100B/季（sourced floor）\n\n2Y 驗證點：FY27 (FY26+1) DISCO 季 orders ≥ ¥100B + book-to-bill ≥ 1.0；TSMC CoWoS 達 130K wafer/mo target\n5Y 驗證點：CoWoS 進一步擴至 200K wafer/mo（FY29-30）+ DISCO 配套訂單 ≥ ¥130B/季\n10Y 驗證點：先進封裝（chiplet + glass + 3D 整合）TAM 從 $5B → $12B+\n具體數字門檻：DISCO 季 orders ≥ ¥100B + 4Q 滾動 YoY ≥ +10%\n信息來源：TSMC Q1-Q2 26 法說 CoWoS roadmap + DISCO 季 IR + TrendForce CoWoS 擴產追蹤\n漂移觸發條件：連 2 季 TSMC CoWoS 量 &lt; 110K/mo 或 DISCO 季 orders &lt; ¥90B → 削弱；連 2 季 &lt; ¥80B → 反轉（QC-35 2Y 假設分級）\n\nH2：GM 維持 ≥ 58% 全年；耗材占比維持 40%+（razor-blade 飛輪持續）\n\n2Y 驗證點：FY26-27 GM ≥ 58%，耗材占比 ≥ 40%\n5Y 驗證點：5Y 滾動均 GM ≥ 58%（穿越 cycle 仍維持高位）\n10Y 驗證點：耗材占比擴大至 45%+（recurring 比例強化）\n具體數字門檻：GM ≥ 58%（FY25 actual 60%+）；耗材 ≥ 40%\n信息來源：DISCO 季 IR + Annual Securities Report\n漂移觸發條件：單季 GM &lt; 55% → 削弱；連 2 季 &lt; 52% → 反轉（QC-34/35 季節性過濾 + 漂移分級）\n\nH3：Glass cutting / CoPoS 2027-2028 首批商業訂單（LPKF LIDE + 自研結合）\n\n2Y 驗證點：2027-Q2 DISCO 首批 glass cutting 商業訂單（per LPKF + 自研 roadmap）\n5Y 驗證點：FY28-30 glass cutting 達 ¥30-50B/年 revenue\n10Y 驗證點：FY32+ glass cutting + 後 AI 架構整合測試達 ¥100B+/年\n具體數字門檻：2027-Q4 前首批商業訂單金額 ≥ ¥10B\n信息來源：TSMC CoPoS roadmap + Intel Foveros-B 採用 + LPKF LIDE 授權進展 + DISCO 法說 \"2027+ glass-friendly cutting\"\n漂移觸發條件：2027-Q4 後仍無 glass cutting 首批商業訂單 → 反轉（QC-35 5Y 假設分級）"},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"ATE / packaging 週期回調（2023 曾 OPM -7pp）","columns":{"對應假設":"H1","時間尺度":"⚡ 短期","監測指標":"DISCO 季 orders + book-to-bill；4 大 hyperscaler capex","警戒閾值":"連 2 季 orders &lt; ¥90B 或 book-to-bill &lt; 0.9 → 預警"}},{"id":"R2","text":"中國需求下修（15-20% 營收 + geopolitical 風險）","columns":{"對應假設":"H1","時間尺度":"🔥 中期","監測指標":"中國季營收 YoY；export control 升級","警戒閾值":"連 2 季中國 YoY &lt; 0%"}},{"id":"R3","text":"Glass cutting 技術未商業化（LPKF 授權限制或 TSMC 採用替代）","columns":{"對應假設":"H3","時間尺度":"🐢 長期","監測指標":"glass cutting 商業訂單 + 競爭對手動態","警戒閾值":"2027-Q4 後仍無 glass cutting 首批訂單"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"A","val":"🟡","ma":"✅","trap":"🟢","moat_trend":"↑","runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":65860,"archetype":null,"cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"6146.T","date":"2026-10-25","schema":"v15.0","contract":"v19","company_name":"DISCO Corporation"},"oneliner":"DISCO 切割研磨設備約六到七成份額，最新一季營業利益率 47.4%、出貨額創新高；但股價半年跌 31% 後前瞻本益比仍約 28 倍，1–3 月共識偏高、現金轉換偏弱，等 2027 年 1 月實績確認再動手。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/6146.T_20261025/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/6146.T_20261025/scenario.json","answers":{"q1_business":{"verdict":"DISCO 賺的是晶圓廠與封測廠「把晶圓磨薄、切開」這一步的錢，收入來自切割、研磨、拋光設備，加上隨用量消耗的刀片與砂輪。錢卡在後段薄化與切割這個節點；AI、HBM 與先進封裝讓這一步工序變多、難度變高。","reasoning":"最新一季（2026 年 7–9 月）營收 1,428 億日圓，營業利益 676 億，營業利益率 47.4%，出貨額 1,486 億創單季新高。公司指引 10–12 月營收 1,324 億、營業利益 581 億、利益率 43.9%、出貨額 1,496 億，也就是營收與利益季減，出貨仍創高。營收在客戶驗收後才認列，出貨額才反映客戶的投資意願。年度面（financial_history，FY2023→FY2026）：營收由 2,841 億增至 4,369 億，毛利率由 64.9% 升至 70.2%，營業利益率由 38.9% 升至 42.3%。營運槓桿很高：依指引，10–12 月營收季減 104 億，營業利益季減 95 億，向下時利益掉得比營收快。產業時鐘判在擴張期，依據是出貨額連季創高，以及 SEMI 預估晶圓製造設備 2027 年增 21.8%、2028 年增 14.1%，不是看股價。供需持久度判為結構性持久到 2028 年：Wolfe 與 ASML 都指出新廠房還沒蓋好，2028 年前難見過剩；但這仍是週期性擴張，2028 年後供給可逆性高。設備與耗材的分部占比事實表未涵蓋。單點依賴：第一大客戶 TSMC 約占 FY2026 營收 11%，中國約占 35%，兩者都是二手資料、未對照申報；製造產能八成以上在日本。","fact_refs":["f_kpi0_gaap_jgaap","f_kpi1_jgaap","f_kpi2_jgaap","f_kpi3_shipments","f_kpi6_fy2027_q3_10_12","f_kpi7_4_12","f_earnings_recency"],"verdict_values":{"revenue_quality":"設備營收依驗收認列，季度波動大；刀片與砂輪耗材隨裝機量重複購買，構成底盤，但耗材占比事實表未涵蓋","unit_econ_note":"毛利率約七成，營業利益率 42–47%。依公司指引，10–12 月營收季減 104 億、利益季減 95 億，邊際利益率近九成，下行時獲利彈性同樣大","archetype":{"primary":"品質複利成長","secondary":"循環/商品","confidence":"中","fingerprint":"設備加耗材雙引擎，份額六成以上，營業利益率四成以上，需求隨半導體資本支出循環"},"industry":{"clock_phase":"II","sd_verdict_source":"結構性持久到 2028 年：Wolfe 稱 2028 年前難見過剩，ASML 稱 2027–2028 年產能不足，SEMI 預估設備支出成長到 2028 年；2028 年後供給可逆性高","bargaining":{"up":"供應商集中度事實表未涵蓋","down":"第一大客戶 TSMC 約占 11%（二手資料），未見單一客戶超過四成；份額六到七成，對客戶議價強","geo":"中國約占營收 35%、產能八成以上在日本（二手資料），出口管制是最大的地緣議價風險"},"profit_pool_dir":"AI 封裝讓後段薄化與切割的工序增加，利潤池往這個節點流入；這是方向判斷，利潤池占比數字事實表未涵蓋","tam_table":{"expanded":false,"reason":"切割研磨設備的市場規模、滲透率與分段成長率事實表都未涵蓋；份額只有 Morningstar 60–70% 一個點估計，無法建時序表"}}}},"q2_moat":{"verdict":"護城河趨勢持平：份額與利益率都在高檔，但沒有同業數字能證明領先還在擴大。","reasoning":"機制有三層：一是切割研磨設備約六到七成份額（Morningstar 2025 年估計）；二是刀片與砂輪耗材隨裝機量重複購買；三是製程經客戶驗證後，換供應商要重新認證。執行面判穩定：FY2025、FY2026 年度營業利益率 42.4%、42.3% 持平，最新一季 47.4% 屬週期高點，不能當成結構性擴大。定價面判穩定：毛利率 FY2025 70.6%、FY2026 70.2% 持平，較 FY2023 的 64.9% 已上一層。同業財務對照整張缺，無法驗證報酬率差距是否擴大，所以不給最高級，給 A，執行與定價各 9 分。威脅：中國自給政策可能扶植本土設備商，屬通用論述，尚無拿單紀錄；雷射與電漿加工可能取代刀輪，但兩者都在 DISCO 自家研發線上，屬點對點威脅，不扣分。再投資報酬用代理值估算：FY2023→FY2026 淨利增 526 億；同期留存再投資（淨利減自由現金流）合計 1,106 億，增量報酬約 48%；三年淨利合計 3,436 億，再投資率約 32%；內生成長上界約 48%×32%≈15.3%。淨利增幅大多來自週期上行與利益率提升，增量報酬偏高估。","fact_refs":["f_kpi2_jgaap","f_kpi3_shipments","f_kpi4_cf_cf","f_kpi5"],"verdict_values":{"moat":{"mechanism":"份額六到七成加耗材重複購買加製程驗證換線成本","execution":9,"pricing":9,"grade":"A","trend":"→","trend_evidence":"年度營業利益率 FY2025 42.4%、FY2026 42.3%，毛利率 70.6%、70.2%，兩項都持平；份額只有單點估計，同業數字缺，無擴大證據，也無份額流失紀錄","competitor_notes":[{"name":"中國本土半導體設備商（未具名）","strategy_note":"靠自給政策與國內客戶試用切入，目前只有通用風險論述，未見在先進封裝客戶取得量產驗證的紀錄"}],"peer_na_reason":"事實表同業財務整張缺，無法算報酬率差距；改用自身利益率軌跡與第三方份額估計判斷方向","threats":[{"level":"🟡","text":"中國自給政策扶植本土切割研磨設備商，可能侵蝕中國份額（約占營收 35%）","p":"20%","evidence_refs":["competitive_share_entrants#0","geo_supply_chain#2"]},{"level":"🟡","text":"雷射、電漿等新加工技術取代鑽石刀輪；公司兩條技術線都在自研，屬自我替代","p":"15%","evidence_refs":["substitute_technology#0"]}],"roic_durability":{"quadrant":"高利益率×周轉率待補（投入資本事實表未涵蓋，只能以營業利益率 42–47% 推定為高報酬）","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"每片晶片都要經過薄化與切割，客戶延後購買等於延後量產；生成式 AI 相關出貨額由約 550 億增至約 750 億，最新一季出貨額 1,486 億創高"},{"item":"決策層級","level":"🟢","text":"替代性要在客戶產線的製程驗證層級衡量：設備一旦通過驗證，換廠就得重新認證，耗材也綁住裝機；換約流失率與認證週期的代理數字事實表未涵蓋"},{"item":"價值鏈分配","level":"🟡","text":"切割研磨占客戶設備支出比例小但不可少，DISCO 拿到四成以上利益率；但第一大客戶約占 11%，中國約占 35%，本土替代與大客戶壓價會重新分配這段利潤"},{"item":"社會容忍度","level":"🟡","text":"沒有價格管制問題，但半導體設備是出口管制熱點；2026 年 8 月公司已出面否認新管制傳聞，中國商務部也把 20 家日本實體列入關注名單（是否包含 DISCO 未知），政治上限可能比經濟上限先到"}],"roiic":"約 48%（代理值）","reinvest_rate":"約 32%（代理值）","endo_ceiling":15.3,"formula_note":"增量報酬＝(FY2026 淨利 1,355 億−FY2023 淨利 829 億)÷FY2024–FY2026 留存再投資合計（淨利−自由現金流）1,106 億≈48%；再投資率＝1,106÷三年淨利合計 3,436≈32%；內生上界＝48%×32%≈15.3%。以淨利代替稅後營業利益，投入資本缺，所以是代理值，週期上行使它偏高估"}}}},"q3_growth":{"verdict":"五年後跑道中等：份額已有六到七成，成長要靠市場本身擴大而非滲透，本包內也沒有有來源的第二條成長曲線。","reasoning":"成長以量為主（AI、HBM、封測廠帶動出貨），價格次之；沒有併購，也沒有回購貢獻。共識兩年 EPS 由 FY2026 實際 1,249.84 增至 FY2028E 2,184.95，年複合約 32.2%；FY2029 共識事實表未涵蓋。內生上界約 15.3%（見護城河段），缺口約 17pp，歸因於利益率擴張（營業利益率由 42.3% 升到最新一季 47.4%）加上週期性出貨量放大，不靠回購或收購，也不靠倍數重估。週期回落時這段缺口會反向。衰退信號亮一盞：自由現金流÷淨利 FY2025 0.43、FY2026 0.73，連兩年低於 0.75。其餘：季度毛利率事實表未涵蓋；FY2023–FY2026 EPS 與營收年複合 17.9% 對 15.4%，差 2.5pp，未亮；替代技術由公司自研，未亮。前份提的玻璃切割第二曲線，本包沒有任何證據，不採計。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_kpi3_shipments"],"verdict_values":{"growth":{"driver_mix":"量為主（AI／HBM／封測廠擴產帶動出貨），價次之，無併購、無回購貢獻","runway_years":"事實表未涵蓋市場規模，無法換算年數","runway_post_y5":"🟡","endo_ceiling_basis":"增量報酬約 48%×再投資率約 32%≈15.3%（代理值，週期上行偏高估）；共識兩年 CAGR 32.2% 超出上界，缺口歸因於利益率擴張與週期量能","segments":{"expanded":false,"reason":"設備、耗材、服務的分部營收與地區營收事實表未涵蓋；耗材占比是承重項，但無來源可展開，列為資料缺口"},"decay_signals":["自由現金流÷淨利連兩年低於 0.75（FY2025 0.43、FY2026 0.73）：亮","毛利率連兩季年減：季度毛利率事實表未涵蓋","EPS 年複合高於營收逾 5pp：FY2023–FY2026 為 17.9% 對 15.4%，未亮","替代技術壓縮市場：雷射與電漿由公司自研，未亮"],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"資本配置中等：股數三年持平沒有稀釋，但幾乎不回購，淨現金約 3,424 億閒置，現金轉換兩年偏弱。","reasoning":"稀釋股數由 FY2023 約 108.64 百萬股（淨利 828.91 億÷EPS 762.98）變為 FY2026 約 108.43 百萬股（1,355.21 億÷1,249.84），三年幾乎不變，沒有稀釋，但也等於沒有淨回購。自由現金流÷淨利 FY2023 0.81、FY2024 0.97、FY2025 0.43、FY2026 0.73，後兩年偏低，推測與擴產資本支出有關，但資本支出明細事實表未涵蓋。本年度上半期營運現金流 1,117 億，公司口徑自由現金流 569 億。總債務為零，淨現金 3,424 億，約占市值 6%。股息殖利率 1.14%，現金去向四分與回購均價事實表未涵蓋。","fact_refs":["f_kpi4_cf_cf","f_kpi5","f_net_debt_m","f_shares_diluted_m","f_dividend_yield_ttm"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":false,"passed":null,"input":"事實表無併購事件"},{"name":"buyback_yield","applicable":true,"passed":false,"input":"FY2023→FY2026 稀釋股數 108.64→108.43 百萬股，淨回購每年約 0.06%，遠低於門檻"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"三年稀釋股數未增加，淨稀釋率≤0"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購（事實表無併購事件）；現金去向四分、股息總額與回購紀錄事實表未涵蓋"}}}},"q5_valuation":{"verdict":"現價要求 FY2027、FY2028 兩年每股盈餘照共識各增三成左右，營業利益率守在四成以上。需求面我相信；共識隱含的 1–3 月營收跳升我不全信。估值合理，不便宜。","reasoning":"前瞻本益比＝股價 49,290÷FY1 共識 1,733.88≈28.4 倍；FY2 為 22.6 倍；trailing 33.5 倍，位於 4 個年度端點的 30.5% 分位（不是五年連續分位）。PEG 以兩年共識年複合 32.2% 計約 0.88，表面便宜，但分母有爭議：FY1 共識營收 5,662 億減公司 4–12 月指引 3,895 億，隱含 1–3 月單季營收約 1,767 億，比 10–12 月指引 1,324 億高 33%。若 FY1 EPS 落在 1,550，前瞻本益比就是 31.8 倍。賣方平均目標價 76,600–84,600 日圓多為 7 月以前的舊快照，最高與最低差 3.8 倍，參考價值低。基準情境：一年後 FY2028E EPS 1,950×28 倍≈54,600（+10.8%）；五年後 FY2031E 2,400×28 倍≈67,200（+36.3%）。同業對照事實表缺，改以自身歷史倍數為錨。","fact_refs":["f_price_at_dd","f_consensus_eps_fy1","f_consensus_eps_fy2","f_pe_current","f_pe_percentile","f_ps_current","f_ev_s_current","f_ev_s_fwd","f_rev_consensus_fy1_m","f_kpi7_4_12","f_kpi6_fy2027_q3_10_12"],"verdict_values":{"valuation":{"basis":"前瞻本益比（FY1 共識）","peers":{"expanded":false,"reason":"事實表同業財務整張缺，無法建同 tier 對照；改以自身 trailing 本益比年度端點為錨"},"fwd_pe":28.4,"peg":0.88,"percentile_5y":30.5,"val_light":"🟡","val_light_derivation":"前瞻 28.4 倍、trailing 33.5 倍位於年度端點 30.5% 分位、PEG 0.88；但 FY1 分母隱含 1–3 月營收比 10–12 月指引高 33%，且最新一季利益率在週期高點，便宜論證不成立，判合理","upside_short_pct":10.8,"upside_mid_pct":36.3,"denominator_disputed":true,"denominator_note":"FY1 共識營收 5,662 億減 4–12 月指引 3,895 億，隱含 1–3 月營收 1,767 億，比 10–12 月指引 1,324 億高 33%；共識可能還沒反映 10 月 22 日的指引，前瞻本益比可能被低估"}}},"q6_how_wrong":{"verdict":"最可能看錯的地方，是把週期高點的利益率與共識當成常態。","reasoning":"陷阱風險中等，依據見反證紀錄：衰退信號亮一盞（自由現金流轉換連兩年偏弱）；FY1 分母有爭議；10–12 月指引營收與利益季減；中國約占營收 35% 且是出口管制熱點。反方向的證據：出貨額仍創新高，2028 年前產業供需偏緊，無份額流失紀錄。","fact_refs":["f_kpi6_fy2027_q3_10_12","f_week26_return_pct","f_rsi14","f_kpi4_cf_cf"],"verdict_values":{"trap":{"verdict":"🟡","label":"週期高檔利益率加現金轉換偏弱"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":1733.88,"pe":28.43,"basis":"FY1（2027 年 3 月期）共識 EPS，現價前瞻倍數；終端倍數同為前瞻一年口徑"},"eps":{"bull":[1800,2350,2750,3100,3500],"base":[1650,1950,2050,2200,2400],"bear":[1550,1300,1450,1650,1800]},"pe":{"bull":35,"base":28,"bear":20},"p":{"bull":20,"base":45,"bear":35},"yield_pct":{"dividend":1.14,"net_buyback":0},"second_stage":{"bull_cagr_pct":12,"base_cagr_pct":8},"max_dd":{"lo":-50,"hi":-30,"basis":"Bear 谷底年 EPS 1,300 乘以谷底倍數 20–26 倍，得 26,000–33,800，對現價 −47%～−31%；250 週均線 35,868 對現價約 −27%；過去 26 週已跌 31%，顯示單一循環段內可再疊加同量級跌幅；營運槓桿高（邊際利益率近九成），利益下修會快於營收","trigger_time":null},"basis":{"bull":"AI 與 HBM 封裝工序持續增加，出貨額每年增兩成以上到 2029 年，營業利益率守在 45% 以上，倍數回到 35 倍","base":"FY2027 略低於共識（1–3 月不如共識跳升），2028 年後隨設備循環放緩至一成左右成長，營業利益率回到 42–44%，倍數 28 倍略降","bear":"2028 年前後設備循環反轉，加上中國份額或管制受損，FY2028 EPS 跌回 1,300，之後緩慢修復，倍數壓到 20 倍；同業對照缺，以自身 trailing 端點下緣為錨"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"中國約占營收 35%、產能八成以上在日本；中國自給政策可能扶植本土設備商；美國 232 關稅涵蓋半導體設備的可能性已被提及","assumption":"中國需求與份額可以維持，出口管制不會涵蓋切割研磨設備","consequence":"五年後虧損 50% 最可能的劇本：2028 年循環反轉，同時中國營收被管制或本土替代砍掉一截，營業利益率跌回三成多，倍數由 28 倍壓到 18 倍","ruling":"部分採納：熊市機率提高到 35%，出口管制列為唯一致命點；但目前沒有任何對手拿單紀錄，管制傳聞已被公司向經產省確認不實，不採為主情境","watch":"地區別營收中國占比、日美出口管制公告、中國本土設備商在先進封裝客戶的驗證消息","evidence_refs":["geo_supply_chain#2","competitive_share_entrants#0"],"fact_refs":["f_kpi0_gaap_jgaap"]},{"view":"論點成功但股東經濟變差","evidence":"自由現金流÷淨利 FY2025 0.43、FY2026 0.73；三年股數不變、幾乎不回購；淨現金 3,424 億","assumption":"需求兌現後現金會回到股東手上","consequence":"淨利照論點成長，但擴產吃掉現金、現金堆在帳上，每股自由現金流成長落後淨利，報酬率被現金稀釋","ruling":"採納：資本配置只給中等，長期信心上限設為中","watch":"FY2027 年報自由現金流÷淨利、股東回饋政策是否改變","evidence_refs":[],"fact_refs":["f_kpi4_cf_cf","f_kpi5","f_net_debt_m"]},{"view":"價格已反映太多","evidence":"前瞻 28.4 倍建立在 FY1 共識上，而共識隱含 1–3 月營收約 1,767 億，比 10–12 月指引高 33%；最新一季營業利益率 47.4% 是週期高點","assumption":"共識分母正確，週期高點利益率可以延續","consequence":"FY1 EPS 若只有 1,550，真實前瞻倍數約 31.8 倍；利益率回到 42% 時，現價隱含的成長就要多撐一年以上","ruling":"採納：判定要等 1 月實績確認分母再進場；但股價已跌 31%，不採「價格已大幅高估」","watch":"2027-01 下旬 10–12 月實績與 1–3 月指引、FY1 共識修正幅度","evidence_refs":[],"fact_refs":["f_consensus_eps_fy1","f_rev_consensus_fy1_m","f_kpi7_4_12"]},{"view":"論點失敗","evidence":"公司風險揭露：若出現取代精密鑽石刀輪的新加工技術，業績可能受影響","assumption":"刀輪耗材的重複營收不會被雷射或電漿加工取代","consequence":"耗材底盤縮小，循環下行時沒有緩衝","ruling":"反駁為主：替代技術由 DISCO 自研，屬自我替代，份額未必流失；但耗材組成可能轉向利益率不同的產品，保留觀察","watch":"耗材營收占比與雷射切割設備出貨（事實表未涵蓋，需補）","evidence_refs":["substitute_technology#0"],"fact_refs":[]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟠","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟠","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 65860 → 本次 49290.0（-25.2%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=65860","side_b":"本次 price_at_dd=49290.0","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 65,860重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 65,860：五年期望值 前份未列，基準年化 前份未列，前份未列不對稱比","side_b":"本次情境、股價仍用 65,860：Bull 價 122,500、Bear 價 36,000，五年期望值 +2.2%，基準年化 0.4%，不對稱比 1.08","ruling":"先換情境、股價不動：五年期望值與基準年化前份未列，無法比較。前份未列不對稱比，本次為 1.08。Bull、Bear 價位與股價無關，只受情境影響。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 65,860：五年期望值 +2.2%，基準年化 0.4%，不對稱比 1.08","side_b":"本次情境、股價 49,290：五年期望值 +36.6%，基準年化 6.4%，不對稱比 3.15","ruling":"再換股價、情境不動：起點價下跌 25.2%，五年期望值多 34.4 個百分點，基準年化多 6.0 個百分點，不對稱比由 1.08 升到 3.15。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"前份漂移：評級、陷阱風險、護城河趨勢","cause":"新證據","prior_field":["signal","trap","moat_trend"],"side_a":"前份（2026-05-22）：評級 A、陷阱風險低、護城河趨勢向上","side_b":"本次：評級 B、陷阱風險中、護城河趨勢持平","ruling":"三項下修都來自新證據：FY2025、FY2026 自由現金流÷淨利連兩年低於 0.75；FY2026 年度毛利率與營業利益率和 FY2025 持平，找不到擴大證據；FY1 共識隱含的 1–3 月營收比公司指引高 33%，分母有爭議","evidence_level":"公司決算與年度財報","settle_metric":"2027-01 下旬公布的 10–12 月實績與 1–3 月指引","if_then":["若 10–12 月出貨額≥1,496 億且 1–3 月營收指引≥1,550 億，評級回到 A 的條件成立","若 FY2027 自由現金流÷淨利回到 0.85 以上，陷阱風險降回低"],"evidence_refs":[]},{"axis":"前份漂移：估值","cause":"價格變動","prior_field":["val"],"side_a":"前份股價 65,860 日圓，估值合理","side_b":"本次股價 49,290 日圓（−25%），估值仍合理","ruling":"股價下跌本來會讓估值轉便宜，但 FY1 分母偏高、利益率處於週期高點，兩者抵銷，估值結論不變","evidence_level":"事實表股價與共識","settle_metric":"FY1 共識修正後的前瞻本益比","if_then":["若 FY1 共識下修後前瞻本益比仍低於 26 倍，估值改判便宜"],"evidence_refs":[]},{"axis":"前份漂移：前份空白欄位補上","cause":"方法變動","prior_field":["runway_post_y5","archetype","cycle_position","p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份這些欄位都是空白","side_b":"本次補上：五年後跑道中等、品質複利成長帶循環屬性、中循環、多頭 20%／熊市 35%、最大回撤 −30%～−50%；定期定額本次未執行，仍空白","ruling":"屬方法補齊，不是基本面變化；熊市機率 35% 是因為共識成長超出內生上界","evidence_level":"方法","settle_metric":"無","if_then":["若下份研究共識成長回到內生上界以內，熊市機率可降到 25%"],"evidence_refs":[]},{"axis":"唯一致命點","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設唯一致命點","side_b":"日本或美國公告出口管制，涵蓋 DISCO 切割研磨設備對中國出貨","ruling":"Single Thing 新設：中國約占營收 35%，是單一事件中衝擊最大的一項；2026 年 8 月的管制傳聞雖經公司確認不實，但顯示市場已在交易這個風險。發生時減碼至半倉並重跑研究","evidence_level":"二手地區占比與公司公告","settle_metric":"經產省或美國商務部公告","if_then":["若公告涵蓋切割研磨設備，減碼至半倉並重跑研究","若一年內無管制且中國占比持穩，致命點機率降到 10%"],"evidence_refs":["geo_supply_chain#2"]},{"axis":"行動門檻改寫","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"連 2 季 orders < ¥90B 或 book-to-bill < 0.9 → 預警；GM < 55% 削弱、連 2 季 < 52% 反轉","side_b":"單季出貨額連兩季低於 1,100 億 → 減碼一半；營業利益率連兩季低於 38% → 減碼；出口管制落地 → 減碼至半倉，管制擴大到耗材則清倉","ruling":"公司不公布訂單額與訂單出貨比，改用公司實際公布的出貨額；前份毛利率門檻 52–58% 遠低於實際的 70%，失去警示力，改用營業利益率","evidence_level":"方法","settle_metric":"每季出貨額與營業利益率","if_then":["若出貨額連兩季低於 1,100 億，減碼一半"],"evidence_refs":[]},{"axis":"重啟進場條件","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"前份未設；只寫等回測 BB 中軌 ¥68,377 或 W52 ¥53,225 後加碼","side_b":"2027-01 下旬實績：10–12 月出貨額≥1,496 億，且 1–3 月營收指引≥1,550 億","ruling":"前份的兩個價格錨都已跌破，但同時出現指引季減與分母爭議，所以改成事件錨，不再用價格錨","evidence_level":"公司指引","settle_metric":"2027-01 下旬決算","if_then":["若兩項同時達標，首筆小倉位 2%"],"evidence_refs":[]},{"axis":"出貨創新高，股價半年跌 31%","cause":null,"prior_field":null,"side_a":"現在就買的最強論證：出貨額 1,486 億創高，10–12 月再指引 1,496 億；2028 年前產業供需偏緊；淨現金 3,424 億；股價已跌 31%，RSI 33.7，前瞻倍數已比 trailing 低 5 倍","side_b":"10–12 月營收與營業利益指引季減 7% 與 14%，利益率由 47.4% 降到 43.9%；FY1 共識隱含 1–3 月營收跳升 33%；營運槓桿向下時同樣大","ruling":"⚖ 不可調和的是時點，方向本身可以調和。選擇等待：硬數據點是 1 月實績能否證明 1–3 月營收真的跳升。股價先走、證據未到，不追","evidence_level":"公司指引與共識","settle_metric":"2027-01 下旬 10–12 月實績、1–3 月指引","if_then":["若 10–12 月出貨額≥1,496 億且 1–3 月營收指引≥1,550 億，首筆小倉位 2%","若股價跌到 250 週均線附近（約 35,900）而出貨額仍≥1,300 億，分批反買","反向：若出貨額連兩季低於 1,300 億，不追，停止任何加碼計畫"],"evidence_refs":["supply_demand_durability#0","supply_demand_durability#3"]},{"axis":"產業態勢三軸","cause":null,"prior_field":null,"side_a":"結構轉好：Wolfe 與 ASML 都指 2028 年前供給偏緊，SEMI 預估設備支出成長到 2028 年","side_b":"其他結構變數：中國約占 35%，本土替代論述與出口管制關注名單並存；競爭惡化目前只有通用論述，沒有拿單紀錄","ruling":"雙向拉鋸：需求結構轉好與地緣結構風險同時存在，競爭面靜態","evidence_level":"第三方產業預測與二手地區資料","settle_metric":"中國營收占比、管制公告","if_then":["若中國營收連兩季年減且占比下降超過 5pp，停止加碼"],"evidence_refs":["competitive_share_entrants#0","geo_supply_chain#2","supply_demand_durability#2"]},{"axis":"賣方目標價與現價","cause":null,"prior_field":null,"side_a":"賣方平均目標價 76,600–84,600 日圓，最低 68,000，都高於現價","side_b":"這些多是 7 月以前的快照，最高與最低差 3.8 倍","ruling":"目標價方向支持多方，但已過時而且分歧大，不作為進場依據，自身信心也不因此上調","evidence_level":"二手共識頁","settle_metric":"10 月決算後的目標價修正","if_then":["若決算後平均目標價下修超過 15%，熊市機率再加 5pp"],"evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#1"]}],"triggers":[{"n":1,"text":"10–12 月出貨額是否達公司指引","type":"假設驗證","maps_to":"H1","metric":"單季出貨額","threshold":"≥1,496 億日圓","action":"達標維持論點；低於 1,350 億列為削弱","source_freq":"公司季度決算","date":"2027-01","evidence_refs":["supply_demand_durability#3"]},{"n":2,"text":"重啟進場：出貨達標且 1–3 月營收指引證明共識分母成立","type":"估值rearm","maps_to":"H1","metric":"10–12 月出貨額與 1–3 月營收指引","threshold":"出貨額≥1,496 億且營收指引≥1,550 億","action":"首筆小倉位 2%","source_freq":"公司季度決算","date":"2027-01","evidence_refs":[]},{"n":3,"text":"價格先跌、基本面無損時分批反買","type":"加碼","maps_to":"H1","metric":"股價對 250 週均線，以及單季出貨額","threshold":"股價≤36,000 且出貨額≥1,300 億","action":"分批反買，每次 1%，上限 3%","source_freq":"每週","date":null,"evidence_refs":[]},{"n":4,"text":"日本或美國出口管制涵蓋切割研磨設備對中國出貨","type":"Single Thing","maps_to":"R2","metric":"經產省或美國商務部公告","threshold":"公告涵蓋 DISCO 產品","action":"減碼至半倉並重跑研究","source_freq":"事件","date":null,"evidence_refs":["geo_supply_chain#2"]},{"n":5,"text":"中國本土設備商在先進封裝客戶取得切割或研磨量產驗證","type":"風險","maps_to":"R3","metric":"本土設備商量產驗證消息","threshold":"任一主要封測廠或晶圓廠公開採用","action":"停止加碼","source_freq":"事件","date":null,"evidence_refs":["competitive_share_entrants#0","substitute_technology#0"]},{"n":6,"text":"週期利益率失守","type":"減碼","maps_to":"H2","metric":"單季營業利益率","threshold":"連兩季低於 38%","action":"減碼一半","source_freq":"公司季度決算","date":null,"evidence_refs":[]},{"n":7,"text":"年報複審現金轉換","type":"複審日期","maps_to":"R4","metric":"年度自由現金流÷淨利","threshold":"低於 0.6","action":"資本配置降級並重跑研究","source_freq":"年報","date":"2027-04","evidence_refs":[]}],"kill_metrics":[{"metric":"單季出貨額（公司公布）","bear_threshold":"連兩季低於 1,100 億日圓","window":"2027-01 至 2027-10 各季決算","source":"DISCO 決算短信與補足說明資料","last_status":"ok"},{"metric":"單季營業利益率","bear_threshold":"連兩季低於 38%","window":"未來四季","source":"DISCO 決算短信","last_status":"ok"},{"metric":"年度自由現金流÷淨利","bear_threshold":"FY2027 低於 0.6","window":"FY2027 年報（2027-04）","source":"年度現金流量表","last_status":"warning"},{"metric":"對中國出口管制","bear_threshold":"日本或美國公告涵蓋切割研磨設備","window":"持續","source":"經產省、美國商務部公告","last_status":"ok"}],"evidence_dismissed":[],"action_conditions":{"rearm_trigger":"2027-01 下旬實績：10–12 月出貨額≥1,496 億，且 1–3 月營收指引≥1,550 億","exec_line":"等 1 月實績：兩項都達標就建首筆 2%；股價跌到 250 週均線附近且出貨≥1,300 億，分批反買；出貨連兩季低於 1,300 億則不追"}},"decision_inputs":{"signal":"B","ma":"🟠","cycle_position":"中循環","cycle_verdict":"未觸發","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":false,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等 2027-01 下旬實績：10–12 月出貨額≥1,496 億，且 1–3 月營收指引≥1,550 億，證明 FY1 共識分母成立","asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null},"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8(val爭議)","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='A'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟠'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟡', moat_trend='→', week26=-31.02, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position='中循環', moat='A', moat_trend='→', cycle_gates_pass=False"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈機械讀數判定不可用，baseline rows 8/9/9b/10 的估值條件視為不可判 → 落 row8 觀望（保守方向）","hit":true,"basis":"val_denominator_disputed=True, val(機械讀數)='🟡'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":null,"requires_critic":[]},"thesis":{"H":[{"id":"H1","text":"AI、HBM 與封測廠擴產讓單季出貨額維持在 1,300 億以上直到 FY2028","2y":"FY2028 前四季滾動出貨額≥5,200 億，年增≥10%","5y":null,"10y":null,"threshold":"四季滾動出貨額≥5,200 億，年增≥10%","source":"DISCO 季度出貨額公告與決算補足說明資料","drift_rule":"四季滾動出貨額連兩季偏離門檻 5% 以上為削弱，連三季偏離 10% 以上為反轉"},{"id":"H2","text":"份額與耗材讓營業利益率在完整循環內守在 40% 以上","2y":null,"5y":"五年滾動年度營業利益率≥40%","10y":null,"threshold":"年度營業利益率≥40%","source":"DISCO 決算短信與年報","drift_rule":"十二個月滾動營業利益率連四季低於門檻 5% 以上為削弱，連六季低於 10% 以上為反轉"},{"id":"H3","text":"切割研磨份額守住六成以上，雷射與電漿由自家吸收，不被本土廠取代","2y":null,"5y":null,"10y":"第三方份額估計≥60%，且中國本土廠未在先進封裝客戶量產","threshold":"份額估計≥60%","source":"第三方產業份額估計、公司地區別營收","drift_rule":"份額估計跨兩個年度下滑為削弱，跨三個年度下滑為反轉"}],"R":[{"id":"R1","text":"設備循環反轉：10–12 月營收與利益已指引季減，營運槓桿向下時利益掉得比營收快","h_ref":"H1","clock":"⚡","threshold":"單季出貨額連兩季年減","evidence_refs":[]},{"id":"R2","text":"中國約占營收 35%，出口管制或需求下修會直接砍掉一截營收","h_ref":"H1","clock":"🔥","threshold":"中國營收連兩季年減且占比下降超過 5pp，或管制公告","evidence_refs":["geo_supply_chain#2"]},{"id":"R3","text":"中國本土設備商在自給政策扶植下取得份額，或新加工技術取代刀輪耗材","h_ref":"H3","clock":"🐢","threshold":"主要客戶公開採用本土設備量產","evidence_refs":["competitive_share_entrants#0","substitute_technology#0"]},{"id":"R4","text":"現金轉換偏弱、淨現金閒置，每股價值成長落後淨利","h_ref":"H2","clock":"🔥","threshold":"年度自由現金流÷淨利低於 0.6","evidence_refs":[]}],"single_thing":{"description":"日本或美國公告出口管制，涵蓋 DISCO 切割研磨設備對中國出貨","why_fatal":"中國約占營收 35%（二手資料），營運槓桿又高（邊際利益率近九成），營收少一成五到兩成就可能讓利益少三成以上，同時打破份額與耗材底盤","if_happens":"減碼至半倉並重跑研究；若管制擴及耗材則清倉","how_monitor":"經產省與美國商務部公告、公司公告、季度地區別營收","probability":"15%"}},"appendix_a":{"growth_durability":7,"quality_score":9,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":22.56,"peg_fy2":0.87,"stress":{"pass":null,"total":null}},"eps_meta":{"base_eps_path":{"FY2026A":1249.84,"FY2027E":1733.88,"FY2028E":2184.95},"fy_end_month":3,"eps_basis":"日本基準稀釋 EPS；共識取 yfinance 平均，FY2029 共識事實表未涵蓋，只有兩年"},"catalysts":[{"date":"2027-01","date_precision":"month","type":"guidance","event":"10–12 月決算與 1–3 月指引","impact":"高","watch":"出貨額是否≥1,496 億、1–3 月營收指引是否≥1,550 億"},{"date":"2027-04","date_precision":"month","type":"guidance","event":"FY2027 年度決算與新年度指引","impact":"高","watch":"自由現金流÷淨利、營業利益率、股東回饋政策"},{"date":"2026-12","date_precision":"month","type":"macro","event":"SEMI 年末設備市場預測更新","impact":"中","watch":"2027、2028 年晶圓製造設備成長率是否下修"},{"date":null,"date_precision":null,"type":"regulatory","event":"日美對中國半導體設備出口管制動向","impact":"高","watch":"是否涵蓋切割研磨設備或耗材"}]}
```

---

## ⑤ 覆蓋面（程式判定，你回的 ⑤ 燈號會被覆寫）

燈號 🟡：非核心軸無證據：channel_business_model_shift（通路／商業模式轉移）、customer_second_source（客戶 second-source 與 in-house）、major_events（重大事件（QC-19））（尾部風險或事件型，不擋）。

⑤ 的 reason 只需評論：空軸的查詢詞是否切題、判斷有沒有交代缺口對結論的影響。

---

## 尾段：回覆格式

只回一個 JSON 陣列，①–⑧ 每條一個元素，八個全出，不得跳號、不得多列，陣列外不得有任何文字（不加前言、不加 markdown 圍欄、不加附註）：

```json
[{"item": "①", "light": "🔴|🟡|🟢", "judgment_path": "$.路徑", "reason": "一句話"}]
```
