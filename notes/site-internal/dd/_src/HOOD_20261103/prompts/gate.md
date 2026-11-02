你是 DD 管線 v20 的判斷層閘（gate），標的 HOOD（20261103）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（52 條）
- `f_kpi0_gaap_total_net_revenues`（q1_business）｜營收（GAAP total net revenues）＝1424 USD m｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-27）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 https://investors.robinhood.com/news-releases/news-release-details/robinhood-reports-third-quarter-2026-results（數字經 8-K/A 修訂版 ex99.1 核對）（numbers.latest_quarter_kpis.items[0]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-27））
  - 註記：未取得（無可靠共識來源，不填造）
- `f_kpi1_gaap`（q1_business）｜營業利益（GAAP，營收減總營業費用，衍生值）＝685 USD m｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-27）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 https://investors.robinhood.com/news-releases/news-release-details/robinhood-reports-third-quarter-2026-results（數字經 8-K/A 修訂版 ex99.1 核對）；營業利益由營收1,424−opex 739衍生（numbers.latest_quarter_kpis.items[1]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-27））
  - 註記：未取得（無可靠共識來源，不填造）
- `f_kpi2_gaap`（q1_business）｜營業利益率（GAAP，衍生）＝48.1 %｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-27）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 https://investors.robinhood.com/news-releases/news-release-details/robinhood-reports-third-quarter-2026-results（數字經 8-K/A 修訂版 ex99.1 核對）；衍生（numbers.latest_quarter_kpis.items[2]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-27））
  - 註記：未取得（無可靠共識來源，不填造）
- `f_kpi3_adjusted_ebitda_gaap_non`（q1_business）｜Adjusted EBITDA（非 GAAP，公司未報 non-GAAP 營業利益）＝808 USD m｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-27）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 https://investors.robinhood.com/news-releases/news-release-details/robinhood-reports-third-quarter-2026-results（數字經 8-K/A 修訂版 ex99.1 核對）（numbers.latest_quarter_kpis.items[3]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-27））
  - 註記：未取得（無可靠共識來源，不填造）
- `f_kpi4_adjusted_ebitda_margin`（q1_business）｜Adjusted EBITDA margin＝57 %｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-27）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 https://investors.robinhood.com/news-releases/news-release-details/robinhood-reports-third-quarter-2026-results（數字經 8-K/A 修訂版 ex99.1 核對）（numbers.latest_quarter_kpis.items[4]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-27））
  - 註記：未取得（無可靠共識來源，不填造）
- `f_kpi5_gaap`（q1_business）｜淨利（GAAP）＝476 USD m｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-27）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 https://investors.robinhood.com/news-releases/news-release-details/robinhood-reports-third-quarter-2026-results（數字經 8-K/A 修訂版 ex99.1 核對）（numbers.latest_quarter_kpis.items[5]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-27））
  - 註記：未取得（無可靠共識來源，不填造）
- `f_kpi11_funded_customers`（q1_business）｜Funded Customers＝28.7 M｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-27）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 https://investors.robinhood.com/news-releases/news-release-details/robinhood-reports-third-quarter-2026-results（數字經 8-K/A 修訂版 ex99.1 核對）（numbers.latest_quarter_kpis.items[11]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-27））
  - 註記：未取得（無可靠共識來源，不填造）
- `f_kpi12_arpu`（q1_business）｜ARPU（年化）＝200 USD｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-27）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 https://investors.robinhood.com/news-releases/news-release-details/robinhood-reports-third-quarter-2026-results（數字經 8-K/A 修訂版 ex99.1 核對）（numbers.latest_quarter_kpis.items[12]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-27））
  - 註記：未取得（無可靠共識來源，不填造）
- `f_kpi13_total_platform_assets`（q1_business）｜Total Platform Assets＝396 USD B｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-27）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 https://investors.robinhood.com/news-releases/news-release-details/robinhood-reports-third-quarter-2026-results（數字經 8-K/A 修訂版 ex99.1 核對）（numbers.latest_quarter_kpis.items[13]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-27））
  - 註記：未取得（無可靠共識來源，不填造）
- `f_kpi14_net_deposits`（q1_business）｜Net Deposits＝15.7 USD B｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-27）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 https://investors.robinhood.com/news-releases/news-release-details/robinhood-reports-third-quarter-2026-results（數字經 8-K/A 修訂版 ex99.1 核對）（numbers.latest_quarter_kpis.items[14]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-27））
  - 註記：未取得（無可靠共識來源，不填造）
- `f_earnings_recency`（q1_business）｜最近一次財報日＝2026-10-27 date｜期間與口徑：2026-10-27／距今 5 個交易日｜kind：realized
  - 來源：—（numbers.earnings_recency，as_of 2026-10-27）
- `f_peer_hood_gross_margin_pct`（q2_moat）｜HOOD 毛利率＝81.44 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.HOOD.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_hood_operating_margin_pct`（q2_moat）｜HOOD 營業利益率＝45.65 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.HOOD.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_hood_fcf_margin_pct`（q2_moat）｜HOOD FCF 利潤率＝58.44 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.HOOD.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_ibkr_gross_margin_pct`（q2_moat）｜IBKR 毛利率＝89.97 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.IBKR.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_ibkr_operating_margin_pct`（q2_moat）｜IBKR 營業利益率＝86.25 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.IBKR.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_ibkr_fcf_margin_pct`（q2_moat）｜IBKR FCF 利潤率＝135.66 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.IBKR.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_schw_fcf_margin_pct`（q2_moat）｜SCHW FCF 利潤率＝52.27 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.SCHW.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_coin_gross_margin_pct`（q2_moat）｜COIN 毛利率＝71.01 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.COIN.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_coin_operating_margin_pct`（q2_moat）｜COIN 營業利益率＝5.68 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.COIN.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_coin_fcf_margin_pct`（q2_moat）｜COIN FCF 利潤率＝68.4 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.COIN.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_kpi10_2026_adjusted_opex_sbc`（q4_capital）｜指引：2026 全年 Adjusted opex＋SBC＝2,675–2,750 USD m｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-27）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司 IR 新聞稿 https://investors.robinhood.com/news-releases/news-release-details/robinhood-reports-third-quarter-2026-results（數字經 8-K/A 修訂版 ex99.1 核對）；區間 2,675–2,750m（上緣下調 25m）；公司無 2026 營收／2027 指引（numbers.latest_quarter_kpis.items[10]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-27））
  - 註記：未取得（無可靠共識來源，不填造）
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝2.42 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-10-31）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝3.39 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-10-31）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝4.37 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-10-31）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝5317.03 USD m｜期間與口徑：2026-11-03／yfinance revenue_estimate 0y 平均（27 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝6870.72 USD m｜期間與口徑：2026-11-03／yfinance revenue_estimate +1y 平均（28 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi8_sbc`（q4_capital）｜SBC＝80 USD m｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-27）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 https://investors.robinhood.com/news-releases/news-release-details/robinhood-reports-third-quarter-2026-results（數字經 8-K/A 修訂版 ex99.1 核對）（numbers.latest_quarter_kpis.items[8]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-27））
  - 註記：未取得（無可靠共識來源，不填造）
- `f_kpi7_ocf_1_225_capex_21`（q4_capital）｜自由現金流（OCF 1,225 − capex 21，衍生，公司未報）＝1204 USD m｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-27）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 https://investors.robinhood.com/news-releases/news-release-details/robinhood-reports-third-quarter-2026-results（數字經 8-K/A 修訂版 ex99.1 核對）；衍生（numbers.latest_quarter_kpis.items[7]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-27））
  - 註記：未取得（無可靠共識來源，不填造）
- `f_kpi9_sbc`（q4_capital）｜SBC 占營業利益（衍生）＝11.7 %｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-27）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 https://investors.robinhood.com/news-releases/news-release-details/robinhood-reports-third-quarter-2026-results（數字經 8-K/A 修訂版 ex99.1 核對）；衍生（numbers.latest_quarter_kpis.items[9]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-27））
  - 註記：未取得（無可靠共識來源，不填造）
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝-2277.0 USD m｜期間與口徑：2026-11-03／yfinance 最新一季：總債務 22552.0、現金 24829.0（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝900.49 m shares｜期間與口徑：2026-11-03／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝86.27 USD｜期間與口徑：2026-11-02（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-11-02（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝35.64 x｜期間與口徑：2026-10-31／分母＝FY1 EPS 2.42，分子＝快照價 86.24｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-10-31）
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝39.74 x｜期間與口徑：2026-11-02（RTH 收盤，UTC）／2 個年度端點內的分位＝44.6｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-11-02（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝44.6 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／**非五年分位**：只用 2 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝15.28 x｜期間與口徑：2026-11-02（RTH 收盤，UTC）／4 個年度端點內的分位＝54.2｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝54.2 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝14.83 x｜期間與口徑：2026-11-02（RTH 收盤，UTC）／4 個年度端點內的分位＝55.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ev_s_fwd`（q5_valuation）｜EV/S（EV ÷ FY1 共識營收）＝14.17 x｜期間與口徑：2026-11-03／f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）｜kind：estimate
  - 來源：—（numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_ev_m`（q5_valuation）｜目前企業價值 EV（市值＋淨負債）＝75367.86 USD m｜期間與口徑：2026-11-03／市值 77644.86 ＋ 淨負債 -2277.0｜kind：realized
  - 來源：—（numbers.capital_structure.ev_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_consensus_rev_fy1_pct`（q5_valuation）｜FY1 共識修正＝2.11 %｜期間與口徑：2026-10-31／兩份 Koyfin 快照之間的 EPS 修正幅度（2.37 → 2.42）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.fy1.revision_pct，as_of 2026-10-31）
- `f_consensus_rev_fy2_pct`（q5_valuation）｜FY2 共識修正＝3.35 %｜期間與口徑：2026-10-31／兩份 Koyfin 快照之間的 EPS 修正幅度（3.28 → 3.39）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.fy2.revision_pct，as_of 2026-10-31）
- `f_consensus_rev_fy3_pct`（q5_valuation）｜FY3 共識修正＝4.55 %｜期間與口徑：2026-10-31／兩份 Koyfin 快照之間的 EPS 修正幅度（4.18 → 4.37）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.fy3.revision_pct，as_of 2026-10-31）
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝4.76 %｜期間與口徑：2026-07-30 → 2026-10-31／FY1 共識 EPS 2.31 → 2.42（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-10-31）
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝12.66 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-11-02（RTH 收盤，UTC））
- `f_rsi14`（q5_valuation）｜RSI(14)＝31.48｜期間與口徑：2026-11-02（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ma_state`（q5_valuation）｜週線均線六態（decision_inputs.ma 必須等於此值）＝🟠｜期間與口徑：2026-11-03／timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）
  - 原文：「price 85.18 / W52 97.15 / W104 86.17 / W250 43.43 / W250 13週斜率 2.86%」
- `f_ma_w52`（q5_valuation）｜52 週均線＝97.15 USD｜期間與口徑：2026-11-03／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）
- `f_ma_w104`（q5_valuation）｜104 週均線＝86.17 USD｜期間與口徑：2026-11-03／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）
- `f_ma_w250`（q5_valuation）｜250 週均線＝43.43 USD｜期間與口徑：2026-11-03／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）
- `f_kpi6_adjusted_eps_gaap_8_k_a`（q1_business）｜Adjusted EPS（新揭露非 GAAP 指標，8-K/A 修訂版）＝0.6 USD｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-27）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 https://investors.robinhood.com/news-releases/news-release-details/robinhood-reports-third-quarter-2026-results（數字經 8-K/A 修訂版 ex99.1 核對）（numbers.latest_quarter_kpis.items[6]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-27））
  - 註記：未取得（無可靠共識來源，不填造）

### findings_digest 中方向為負或來源衝突的條目（20 條）
- `competitive_share_entrants#0`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K 列示競爭來源包括既有券商、金融科技、銀行、加密交易所與科技平台，多數對手營運歷史更長、資本更大；部分新興對手受較少監管。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-18）｜affects：moat_trend、decision_inputs.bear
- `competitive_share_entrants#2`（competitive_share_entrants｜方向 -｜狀態 ok）：預測市場領域競爭加劇：Interactive Brokers、Coinbase 等進入，Tenev 預期產業將整併；2026 年已有 10 家向 CFTC 申請 DCM。
  - 來源：ingame.com: Robinhood CEO expect consolidation（搜尋摘要）（as_of 2026-07-01）｜affects：moat_trend、decision_inputs.bear
- `supply_demand_durability#1`（supply_demand_durability｜方向 -｜狀態 ok）：FM Intelligence：2026Q2 美國活躍散戶帳戶 739 萬，季減 0.4%、年增 30%；配對月成交量季減 7.3%，每帳戶成交量下降。
  - 來源：Finance Magnates datalab: retail broker accounts hold at 7.4 million as volume per account falls 7%（as_of 2026-08-01）｜affects：thesis.R
- `regulatory_antitrust#0`（regulatory_antitrust｜方向 -｜狀態 ok）：FY2025 10-K 風險因子：公司目前並預期未來持續受 DOJ、SEC、FINRA、CFTC、NFA、CFPB、州監管機關及英國 FCA 等國際監管機關的調查與檢查，可能導致禁令、罰款、和解。屬一般性揭露，未點名反壟斷調查。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A Risk Factors（as_of 2026-02-18）｜affects：thesis.R、decision_inputs.bear
- `regulatory_antitrust#2`（regulatory_antitrust｜方向 -｜狀態 ok）：10-Q 提及 Rule 605 修正案自 2026-08 起適用於 RHF/RHS，可能壓縮 PFOF 收入
  - 來源：SEC EDGAR 10-Q Q3 2026（as_of 2026-10-31）｜affects：valuation、thesis.R
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：10-K 風險因素：關稅與貿易政策變動被列為影響市場波動、進而影響營運結果的外部因素（間接、屬市場情緒面），未見產品或供應鏈的直接關稅暴露。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-18）｜affects：decision_inputs.bear
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：FY2025 10-K 披露公司主要倚賴 AWS 提供平台服務（雲端單一主要供應商依賴）；無實體製造，無台灣/中國曝險之來源
  - 來源：Robinhood Markets Form 10-K FY2025（as_of 2026-02-27）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：10-K 風險因子：倚賴第三方（清算系統、做市商、交易所系統等），這些供應商有營運、技術與資安弱點
  - 來源：Robinhood Markets Form 10-K FY2021 (risk factor wording, reiterated in later 10-Ks)（as_of 2022-02-24）｜affects：thesis.R、decision_inputs.bear
- `end_markets#1`（end_markets｜方向 -｜狀態 ok）：Q3 2026 淨利息收入年減 9% 至 $4.15 億，主因證券餘額下降；其他營收年增 61% 至 $1.42 億（Trump Account 服務與 Gold 訂閱）
  - 來源：Robinhood Q3 2026 results (investors.robinhood.com)（as_of 2026-10-27）｜affects：thesis.R、decision_inputs.bear
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：10-K 風險因子：新興科技公司不受同等監管，可能更快創新、承擔更多風險，使 HOOD 處於競爭劣勢；競爭者包含加密貨幣交易所與科技平台。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-18）｜affects：moat_trend、decision_inputs.bear
- `substitute_technology#1`（substitute_technology｜方向 -｜狀態 ok）：10-K 風險因子：HOOD 自述若跟不上快速演進的 AI 技術，競爭地位與經營結果可能受損。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-18）｜affects：moat_trend、thesis.R
- `substitute_technology#2`（substitute_technology｜方向 -｜狀態 ok）：10-K 風險因子：金融服務業面臨快速技術變革（證券交易方式與加密貨幣的發展），HOOD 需推出包含事件合約等缺乏經驗的新技術產品。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-18）｜affects：moat_trend、thesis.R
- `substitute_technology#3`（substitute_technology｜方向 -｜狀態 ok）：分析師稱 Hyperliquid 等加密原生去中心化平台為 HOOD 商業模式的潛在威脅；亦有分析師認為零售客群為護城河。
  - 來源：Stocktwits 新聞：HOOD Stock Drops Amid Market Sell-Off（as_of 2026-07-01）｜affects：moat_trend、decision_inputs.bear
- `substitute_technology#4`（substitute_technology｜方向 -｜狀態 ok）：10-Q 指競爭者可能放棄 PFOF，對 HOOD 的 PFOF 安排形成下行壓力。
  - 來源：SEC EDGAR 10-Q 2026-09-30（as_of 2026-10-30）｜affects：moat_trend、thesis.R
- `capital_markets_pricing#1`（capital_markets_pricing｜方向 -｜狀態 ok）：Q3 EPS 與營收略低於市場預期：Decrypt 報導營收略低於約 $1.43B 預期，EPS $0.51 vs 預期 $0.55（各來源預期值不一致，另有來源稱 $0.55–0.64）。
  - 來源：Decrypt: Robinhood misses Q3 earnings（as_of 2026-10-27）｜affects：valuation、decision_inputs.bear
- `major_events#2`（major_events｜方向 -｜狀態 ok）：Cash sweep 集體訴訟（Dey、Deeney）進行中，2025-04-28 法院部分駁回動議
  - 來源：SEC EDGAR 10-K FY2025 Item 8（as_of 2026-02-18）｜affects：decision_inputs.bear、thesis.R
- `financial_capital_credit_cycle#0`（financial_capital_credit_cycle｜方向 -｜狀態 ok）：Q3 2026 總提列信用損失 $71M，去年同期 $26M（+173%）；信用卡相關 $23M→$61M，券商相關 $3M→$10M；前九個月 $163M vs $78M，部分被較低準備率抵銷。
  - 來源：Robinhood Form 10-Q 期間 2026-09-30（SEC）（as_of 2026-10-29）｜affects：thesis.R、decision_inputs.bear
- `financial_capital_credit_cycle#1`（financial_capital_credit_cycle｜方向 -｜狀態 ok）：財報稱因信用卡放款簿擴張，信用損失提列增加推高費用；公司不提供 2026 總營運費用展望，因提列與監管費用可能有重大影響。
  - 來源：Robinhood Reports Third Quarter 2026 Results（as_of 2026-10-29）｜affects：thesis.R、valuation
- `financial_capital_credit_cycle#2`（financial_capital_credit_cycle｜方向 -｜狀態 ok）：二手來源稱信用卡 90 天以上逾期率自 2025 年底約 2% 升至 6%（未對照一手 10-Q，待核）。
  - 來源：Panabee: Robinhood Earnings: Subscription Growth Meets Rising Credit Stress（as_of 2026-10-30）｜affects：thesis.R、decision_inputs.bear
- `lawsuit_class_action#0`（lawsuit_class_action｜方向 -｜狀態 ok）：Cash sweep 集體訴訟（Dey v. Robinhood、Deeney）進行中，求償金額未明
  - 來源：SEC EDGAR 10-K FY2025 Item 8（as_of 2026-02-18）｜affects：decision_inputs.bear、thesis.R

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 7 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/HOOD_20261103/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":222.0,"bear_5y_price":44.2,"p_bull_pct":25,"p_bear_pct":30,"upside_5y_pct":43.3,"ev5y_pct":44.2,"irr_base_pct":7.5,"asym_ratio":2.7,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":2.42,"pe":35.65,"basis":"FY1（FY2026E）共識 EPS 2.42美元，現價86.27美元；終端倍數套在 FY2031 當年 EPS，與起點同為當年度口徑"},"eps":{"bull":[3.4,4.4,5.4,6.4,7.4],"base":[3.0,3.55,4.1,4.65,5.15],"bear":[2.05,2.15,2.4,2.7,2.95]},"pe":{"bull":30,"base":24,"bear":15},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0,"net_buyback":1.0},"second_stage":{"bull_cagr_pct":15,"base_cagr_pct":10},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### HOOD_Q2_2026_Earnings_Call_20260729.md
- 2026-07-29｜Shiv Verma｜guidance：CFO 稱調降並收窄 2026 全年 adjusted OpEx 與 SBC 展望，區間 26.75 億至 27.75 億美元（原話："and SBC to a range of $2.675 billion to $2.775 billion."）
- 2026-07-29｜Shiv Verma｜guidance：CFO 給 7 月淨入金追蹤約 40 億美元，並說明尚未含 Trump Accounts 入金（原話："July net deposits are tracking towards the $4 billion area"）
- 2026-07-29｜Shiv Verma｜guidance：7 月股票、選擇權、預測市場日均量與 Q2 相近（原話："July, the ADVs for equities, options and prediction markets"）
- 2026-07-29｜Shiv Verma｜guidance：7 月加密貨幣交易量初步比 Q2 稍慢（原話："In terms of crypto, it's probably a little bit slower"）
- 2026-07-29｜Shiv Verma｜guidance：7 月 take rate 與 Q2 平均相近，建議以此為起點（原話："they're in a similar area to what we saw for the Q2 average"）
- 2026-07-29｜Shiv Verma｜margin：管理層對 take rate 的口徑：視為輸出指標，股票與選擇權受組合、波動度、合約類型影響（原話："take rates are an output"）
- 2026-07-29｜Shiv Verma｜margin：Q2 adjusted EBITDA 7.41 億美元，年增 35%，利潤率 57%（原話："adjusted EBITDA was $741 million, up 35% year-over-year"）
- 2026-07-29｜Shiv Verma｜margin：Q2 EPS 0.62 美元，年增 48%（原話："earnings per share was $0.62, up 48% year-over-year"）
- 2026-07-29｜Shiv Verma｜margin：Q2 adjusted OpEx 與 SBC 為 6.41 億美元，低於先前展望區間，且含兩項新業務成本（原話："adjusted OpEx and SBC was $641 million"）
- 2026-07-29｜Shiv Verma｜margin：管理層說明 Rothera 與 WonderFi 新增成本由內部效率自行吸收（原話："allowing us to both self-fund Rothera and WonderFi costs"）
- 2026-07-29｜Shiv Verma｜margin：回答費用三桶（新產品、核心、併購）演變時，稱節省來自三者，且新併購未納入原展望（原話："The short answer is the savings are coming from all of"）
- 2026-07-29｜Shiv Verma｜margin：新併購成本未納入原先費用展望，由公司自行吸收（原話："So we fully self-funded those."）
- 2026-07-29｜Shiv Verma｜margin：管理層新增的衡量口徑：Rule of 40，並稱已是 Rule of 80 公司（原話："more than a Rule of 80 company for the past few"）
- 2026-07-29｜Shiv Verma｜capital_allocation：6 月募資 22 億美元，稱零票息（原話："In June, we opportunistically raised $2.2"）
- 2026-07-29｜Shiv Verma｜capital_allocation：該筆融資條件：0% 票息、股價超過 300 美元前無淨稀釋（原話："with both a 0% coupon and no net dilution until"）
- 2026-07-29｜Shiv Verma｜capital_allocation：年初至今買回 750 萬股、6.64 億美元（原話："we've repurchased 7.5 million shares for $664 million"）
- 2026-07-29｜Shiv Verma｜commitment：重申財務北極星為最大化每股盈餘與每股自由現金流（原話："our financial North Star remains the same, maximize earnings"）
- 2026-07-29｜Shiv Verma｜commitment：計畫在未來一年增加更多年化營收 1 億美元級業務（目前 13 項）（原話："add even more $100 million ARR businesses"）
- 2026-07-29｜Shiv Verma｜commitment：CFO 提到有投資人反映難以判斷該看哪些成長指標，因此提出三項衡量指標（淨入金、Rule of 40、1 億美元 ARR 業務）（原話："we've also heard from some investors"）
- 2026-07-29｜Vladimir Tenev｜commitment：CEO 稱目標在本季底前將 Robinhood Social 開放給所有人（原話："The goal is to get it out to everyone"）
- 2026-07-29｜Shiv Verma｜commitment：CFO 稱未來十年業務規模可望擴大 10 倍（原話："10x the business over the next 10 years"）
- 2026-07-29｜Shiv Verma｜commitment：CFO 稱淨入金年化 20% 為目標，並表示不解讀單月波動（原話："So our goal, as we said, is 20% on an annualized basis."）
- 2026-07-29｜Shiv Verma｜commitment：CFO 稱累積幾季後會更細拆 Robinhood Chain 的變現（原話："quarters, we'll break it down more specifically."）
- 2026-07-29｜Shiv Verma｜customer：Q2 新增近 100 萬名資金帳戶客戶，為上市近 5 年來單季最多（原話："1 million funded customers, the most we've added"）
- 2026-07-29｜Shiv Verma｜customer：CFO 列舉新客成長來源之一：併購帶來數十萬帳戶（原話："which provided a couple of hundred thousand accounts"）
- 2026-07-29｜Shiv Verma｜customer：CFO 稱新客戶訂閱 Gold 比例約 40% 至 50%（原話："New customers still sign up for Gold about 40% to"）
- 2026-07-29｜Shiv Verma｜customer：預測市場使用者數由上次揭露的約 150 萬升至接近 200 萬（原話："number is now closer to 2 million"）
- 2026-07-29｜Shiv Verma｜customer：CFO 稱客戶於下跌日或下跌月傾向淨買進（原話："down days or down months, we tend to see really strong net"）
- 2026-07-29｜Shiv Verma｜customer：CFO 稱 PDT 規則取消使公司因客戶帳戶較小而受惠高於同業（原話："benefit relative to our peers given our customers"）
- 2026-07-29｜Shiv Verma｜customer：CFO 對 PDT 後續貢獻表示尚難量化（原話："it's too early to tell what's exactly going to be"）
- 2026-07-29｜Vladimir Tenev｜customer：Trump Accounts 已有 700 萬名兒童註冊（原話："So 7 million children have signed up."）
- 2026-07-29｜Vladimir Tenev｜customer：銀行帳戶直接存款的附掛情況：約 40% 客戶已設定（原話："we just give you 3.5% automatically on every account"）
- 2026-07-29｜Vladimir Tenev｜product：Gold Card 年化消費額超過 170 億美元（原話："driving over $17 billion in annualized purchase volume"）
- 2026-07-29｜Vladimir Tenev｜product：Robinhood Chain 上線後 DEX 交易量超過 120 億美元（原話："we saw over $12 billion in DEX volume"）
- 2026-07-29｜Vladimir Tenev｜product：Robinhood Earn 提供 7% APY，數週內入金超過 2 億美元（原話："now it allows customers to earn 7% APY"）
- 2026-07-29｜Vladimir Tenev｜product：Agentic Trading 已有逾 10 萬人整合並開立帳戶（原話："We've had over 100,000 people actually"）
- 2026-07-29｜Vladimir Tenev｜product：CEO 列出 Agentic 的使用摩擦之一：模型不熟悉被用於交易（原話："the models themselves aren't familiar with"）
- 2026-07-29｜Shiv Verma｜product：Robinhood Chain 變現口徑：每筆交易收數個基點，非按交易量（原話："per transaction, we make a few basis points"）
- 2026-07-29｜Shiv Verma｜product：Chain 收入約一半與 Arbitrum 分潤（原話："we do share approximately half of it with Arbitrum"）
- 2026-07-29｜Vladimir Tenev｜product：CEO 表示外國股票在產品路線圖上（原話："Obviously, it's on our road map."）
- 2026-07-29｜Vladimir Tenev｜product：新加坡等地擴張策略的說法：希望一次推出更多產品，而非逐項上線（原話："it's better to get more at once rather than"）
- 2026-07-29｜Shiv Verma｜competition：預測市場流量部分：預期近中期多數或相當部分走 Rothera（原話："a good portion will flow through Rothera"）
- 2026-07-29｜Vladimir Tenev｜competition：CEO 稱預測市場採多交易所連接，不依賴單一對手方（原話："and we're not reliant on any one individual counterparty."）
- 2026-07-29｜Vladimir Tenev｜competition：被問美國永續合約時，CEO 稱不提供具體時間表（原話："I just don't like giving time lines on earnings."）
- 2026-07-29｜Vladimir Tenev｜risk：CEO 談 Clarity Act：希望產業在美國有穩定的法規基礎（原話："the foundation of the industry in the U.S. to be durable"）
- 2026-07-29｜Vladimir Tenev｜risk：CEO 稱即使 Clarity Act 延後，公司認為仍會沒問題（原話："So we think we'll be good regardless."）

### HOOD_Shareholder_Analyst_Call_Robinhood_Markets_Inc_20260602.md
- 2026-06-02｜Vladimir Tenev｜product：CEO 稱 Trump Accounts 已有近 600 萬名兒童註冊，符合資格者逾 6000 萬（原話："Nearly 6 million American children are already signed up."）
- 2026-06-02｜Vladimir Tenev｜product：CEO 稱首檔 Robinhood Ventures 基金 RVI 3 月 IPO，市值已超過 10 億美元，並在籌備後續基金（原話："The response so far has been very strong."）
- 2026-06-02｜Vladimir Tenev｜capital_allocation：CEO 稱 RVI 已投資 OpenAI 7500 萬美元（原話："invested $75 million in OpenAI."）
- 2026-06-02｜Vladimir Tenev｜capital_allocation：CEO 表示在私募市場產品上大幅投入（原話："We're investing big here."）
- 2026-06-02｜Vladimir Tenev｜product：CEO 稱 Agentic Trading 上週推出，當時約推到一半客戶，目標本週底全面開放（原話："Trading is rolled out to about half of our customers"）
- 2026-06-02｜Vladimir Tenev｜commitment：CEO 表示 agentic finance 會定期更新、持續擴充（原話："you should expect to see regular updates."）
- 2026-06-02｜Vladimir Tenev｜product：CEO 給出預測市場年化營收數字（口徑：event contracts 年化營收）（原話："generating over $400 million in annualized revenues"）
- 2026-06-02｜Vladimir Tenev｜product：CEO 稱 2026 年迄今預測市場成交合約數已超過 150 億（2025 全年逾 120 億）（原話："more than $15 billion already traded in 2026"）
- 2026-06-02｜Vladimir Tenev｜product：CEO 介紹與 Susquehanna 合資的 Rothera（交易所與清算所）（原話："Rothera, which is our new joint venture with Susquehanna"）
- 2026-06-02｜Lucas Moskowitz｜risk：法務長對預測市場全面禁令的看法（原話："we think a categorical ban on prediction markets is unlikely"）
- 2026-06-02｜Lucas Moskowitz｜risk：法務長稱體育類合約是主要爭議點，公司與 CFTC 立場一致認為屬聯邦監管商品，結果待觀察（原話："that these are federally regulated products"）
- 2026-06-02｜Lucas Moskowitz｜risk：法務長稱正與監管者討論放寬散戶進入私募市場的規則（原話："productive discussions in Washington with regulators and"）
- 2026-06-02｜Vladimir Tenev｜customer：CEO 稱 Robinhood Banking 薪資直存附加率（口徑：直存客戶占有資金帳戶客戶）（原話："40% direct deposit attach rate"）
- 2026-06-02｜Vladimir Tenev｜customer：CEO 稱 Banking 自年底推出以來存款逾 25 億美元、有資金客戶逾 17 萬（原話："deposits from over 170,000 funded customers since launch"）
- 2026-06-02｜Vladimir Tenev｜commitment：CEO 對 Zelle 需求稱無具體資訊，但承諾之後會有更新（原話："rest assured, we hear the feedback"）
- 2026-06-02｜Vladimir Tenev｜commitment：CEO 稱股息追蹤功能目前內部測試中，預告即將推出（原話："is actually in internal testing now"）
- 2026-06-02｜Vladimir Tenev｜competition：CEO 談 Early Dividends 功能時對競爭對手的說法（原話："I'd be shocked if our competitors aren't scrambling"）
- 2026-06-02｜Vladimir Tenev｜competition：CEO 稱客戶可透 Robinhood 參與 SpaceX IPO，並與其他平台比較無最低帳戶門檻（原話："there's no minimum account size to do so"）
- 2026-06-02｜Vladimir Tenev｜product：CEO 稱國際客戶已突破 100 萬（原話："we now have crossed 1 million international customers"）
- 2026-06-02｜Vladimir Tenev｜capital_allocation：CEO 稱已完成 WonderFi 收購（進入加拿大）（原話："our acquisition of WonderFi"）
- 2026-06-02｜Vladimir Tenev｜commitment：CEO 稱預計年內完成印尼券商與加密貨幣收購（原話："planned brokerage and crypto acquisitions in Indonesia"）
- 2026-06-02｜Vladimir Tenev｜product：CEO 稱獲新加坡金管局原則性核准提供綜合券商服務（原話："in-principle approval from the Monetary Authority of"）
- 2026-06-02｜Vladimir Tenev｜product：CEO 陳述 Robinhood Chain 的目標定位（原話："make it the best chain to trade real-world assets."）
- 2026-06-02｜Vladimir Tenev｜margin：CEO 以營收規模口徑說明業務多元化：年營收達 1 億美元的業務線數量（原話："11 business lines generating $100 million in annual revenue"）
- 2026-06-02｜Vladimir Tenev｜customer：CEO 稱股票交易量前一日創歷史新高（會議前一日）（原話："yesterday was all-time record in equities trading"）
- 2026-06-02｜Vladimir Tenev｜commitment：CEO 稱 PDT 規則已改，下一個推動目標是合格投資人認證門檻（原話："now that the PDT rule has been has been improved"）
- 2026-06-02｜Vladimir Tenev｜product：CEO 重申三大策略支柱之二：下一代錢包份額第一（原話："number two, we want to be #1 in wallet share for the next"）

### 問答異常語氣（迴避／改口／保留）
- HOOD_Q2_2026_Earnings_Call_20260729.md｜問：Steven Chubak (Wolfe)：年初費用成長 18%（10% 新產品、5% 核心、3% 併購）的三桶如何隨新展望演變｜答法：CFO 稱節省來自三桶、強調自行吸收、仍是成長公司，但未給各桶新數字
- HOOD_Q2_2026_Earnings_Call_20260729.md｜問：Craig Maurer (FT Partners)：7 月淨入金約 40 億美元為今年最低，有何說明｜答法：CFO 改談年化 20% 目標與年初至今仍遠高於此，稱不解讀單月，未解釋 7 月數字下滑原因
- HOOD_Q2_2026_Earnings_Call_20260729.md｜問：James Yaro (Goldman) 與 Patrick Moley (Piper)：美國永續合約何時推出、為何不更積極｜答法：CEO 稱與 CFTC 溝通具建設性但不給具體時程，轉談其他產品路線圖，並說不喜歡在財報給時程
- HOOD_Q2_2026_Earnings_Call_20260729.md｜問：Brian Bedell (Deutsche)：Rothera 是否推出 Cboe 公司財務 KPI 合約，以及事件合約轉移 Rothera 的計畫｜答法：CEO 稱不確定 Rothera 是否近期推出；CFO 只說「多數或相當部分」將走 Rothera，未給比例或時程
- HOOD_Shareholder_Analyst_Call_Robinhood_Markets_Inc_20260602.md｜問：RVI 是否會投資 Anthropic？｜答法：未直接回答，稱無法具體說明正在看哪些公司，改談一般投資原則
- HOOD_Shareholder_Analyst_Call_Robinhood_Markets_Inc_20260602.md｜問：Robinhood Banking 會不會有 Zelle 與帳單支付？｜答法：先談存款與直存數字，Zelle 部分稱無具體資訊可分享，未給時程
- HOOD_Shareholder_Analyst_Call_Robinhood_Markets_Inc_20260602.md｜問：若預測市場因立法被迫下架，有何替代收入計畫？｜答法：未提供替代收入的數字或具體計畫；法務長談監管對話，CEO 轉而強調多元化與股票交易量創高

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 3 | 2 |
| customer_second_source | not_applicable | 0 | 0 |
| customer_concentration_credit | not_applicable | 0 | 0 |
| supply_demand_durability | found | 4 | 3 |
| regulatory_antitrust | found | 3 | 1 |
| reg_tariff_export | found | 3 | 1 |
| geo_supply_chain | found | 3 | 2 |
| end_markets | found | 4 | 3 |
| substitute_technology | found | 5 | 2 |
| channel_business_model_shift | found | 2 | 2 |
| capital_markets_pricing | found | 4 | 3 |
| major_events | found | 3 | 3 |
| financial_capital_credit_cycle | found | 3 | 2 |
| financial_regulatory_capital_rules | found | 2 | 2 |

未涵蓋／不適用軸的查詢詞原文（供判相關性）：
- **customer_second_source**（not_applicable）：（無查詢記錄）
- **customer_concentration_credit**（not_applicable）：（無查詢記錄）

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260714","verdict":"觀望","role":"追蹤","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"加密收入在 FY26 觸底，正常化盈餘軌跡重建（非幣別引擎接棒）","columns":{"2Y 驗證點":"某季加密 −40% 而交易性總收入仍成長","5Y 驗證點":"FY28 非 GAAP EPS ≥ $3.60、加密收入占比降到","10Y 驗證點":"加密收入長期波動但均值 ~$300M+ 為 base","具體數字門檻":"Q2 非加密交易性收入 YoY >+20%；FY28 EPS ≥ $3.66（Excel 6/23）","來源":"公司月度營運數據 + Excel/共識","漂移觸發":"連 2 季非加密交易性收入 YoY"}},{"id":"H2","text":"有資金帳戶 + 淨存款持續複利（用戶資產飛輪）","columns":{"2Y 驗證點":"有資金帳戶 30M+（5 月 27.7M）","5Y 驗證點":"FY30 帳戶 40M+ + 平台資產 $500B+","10Y 驗證點":"成為「complete fintech super-app」，跨世代留存","具體數字門檻":"淨存款年化 +20%+（TTM 27%）；帳戶 YoY +6.7%（5 月 +1.76M）","來源":"2026-05 月度營運數據（sourced）","漂移觸發":"連 2 月淨存款年化"}},{"id":"H3","text":"M&A + 新線多元化 → 降低加密單引擎依賴","columns":{"2Y 驗證點":"事件合約收入 FY26E ~$586M（Bernstein，+286%）；WonderFi/Bitstamp/TradePMR 整合貢獻","5Y 驗證點":"FY30 財管/銀行/預測市場合計收入 ≥ 加密收入","10Y 驗證點":"多線使加密占比","具體數字門檻":"Q1 事件合約 other trading +320% 到 $147M；銀行 >$2B 淨存款、Gold 4.3M","來源":"Q1 FY26 財報 + 公司揭露","漂移觸發":"任一新線整合受挫（減損/高層離職）或事件合約遭監管禁令 → 削弱"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"加密結構性 deflation：BTC/ETH 進入 multi-year 熊，加密收入與相關量能長期低迷，拖累交易活躍度與情緒","columns":{"對應假設":"H1","時間尺度":"⚡ 短期（1-2 季）","監測指標":"加密收入 YoY、BTC 價位、加密 ADV","警戒閾值":"連 2 季加密收入 YoY"}},{"id":"R2","text":"預測市場（事件合約）監管風險：多州訴訟（Wisconsin 等）+ CFTC 管轄權戰使這條 +320% 引擎被限縮或按州下架","columns":{"對應假設":"H3","時間尺度":"🔥 中期（4-6 季）","監測指標":"訴訟程序里程碑、CFTC 表態、事件合約可用州數","警戒閾值":"集體禁令或關鍵州下架 → §3.F 觸發，重評 H3"}},{"id":"R3","text":"take rate / PFOF 壓縮 + 競爭：Coinbase/Kalshi/SoFi/Schwab 在各垂直分食，零佣金結構下 ARPU 天花板","columns":{"對應假設":"H2/H3","時間尺度":"🐢 長期（2+ 年）","監測指標":"ARPU、各線 take rate、活躍戶留存","警戒閾值":"ARPU 連 4 季 YoY 走弱且無新線補 → 砍倉檢討"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"Q2（7/29）確認非加密交易性收入不靠加密回補 且 事件合約監管未惡化（Wisconsin 等禁令未擴大），或回檔至 $90-95（Fwd PE≈30x）；則轉進場·衛星 starter","irr_base_pct":9.1,"ev5y_pct":47.0,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"追蹤","signal":"B","val":"🟠","ma":"✅","trap":"🟡","moat_trend":"↑","runway_post_y5":"🟡","asym_ratio":2.8,"ev5y_pct":47.0,"irr_base_pct":9.1,"max_dd_pct":-60.0,"bull_5y_price":264.0,"bear_5y_price":64.0,"p_bull_pct":25.0,"p_bear_pct":30.0,"rearm_trigger":"Q2（7/29）確認非加密交易性收入不靠加密回補 且 事件合約監管未惡化（Wisconsin 等禁令未擴大），或回檔至 $90-95（Fwd PE≈30x）；則轉進場·衛星 starter","price_at_dd":109.86,"archetype":"金融","cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"HOOD","date":"2026-11-03","schema":"v15.0","contract":"v19","company_name":"Robinhood Markets, Inc."},"oneliner":"Robinhood 淨入金與產品速度仍強，但Q3 淨利年減14%、信用卡提列翻倍、take rate 走低；現價對 FY2 共識約25倍，我的基本情境低於共識、五年年化約8%，等73美元以下或2027上半年盈餘證實再進場。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/HOOD_20261103/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/HOOD_20261103/scenario.json","answers":{"q1_business":{"verdict":"賺美國散戶交易與客戶資產的錢：Q3 營收14.24億美元，交易性收入約61%、淨利息約29%、訂閱與其他約10%。錢卡在散戶委託單流量與客戶資產這一節點，上游靠做市商付款，下游零佣金，黏著度靠 Gold 綑綁銀行與信用卡撐起。","reasoning":"最小交付：Q3 營收14.24億美元（年增12%）。交易性收入8.67億美元，其中選擇權3.99億（＋31%）、股票1.21億（＋41%）、事件合約1.73億、加密1.20億（−55%）；淨利息4.15億美元（−9%）；其他1.42億美元（＋61%）。GAAP 營業利益6.85億美元、營業利益率48.1%，Adjusted EBITDA 8.08億美元、利潤率57%，淨利4.76億美元、年減14%。單位經濟：資金客戶2,870萬、年化 ARPU 200美元、平台資產3,960億美元（每戶約1.38萬美元）。產業時鐘判擴張期：股票、選擇權、融資餘額與事件合約量創新高，淨入金創年度紀錄；但業界每帳戶交易量季減7%、加密交易量年減38%，屬擴張後段。供需持久性：週期性為主、基準線結構性墊高。LSEG 研究指散戶流量隨景氣循環但基準線永久上移；淨入金年化17%屬結構性，交易量屬週期性，這是悲觀機率不低於30%的依據之一。單點依賴：股票與選擇權收入約占營收36.5%，主要以委託單流量付款向做市商收取，Rule 605 自2026-08起適用；營運上主要倚賴 AWS 與第三方清算、做市商系統。產業態勢屬雙向拉鋸：一邊是競爭惡化（預測市場2026年已有10家申請 DCM，IBKR 與 Coinbase 進場），一邊是結構轉好（近12個月淨入金710億美元、平台資產年增19%），另有監管這個結構變數（Rule 605、預測市場州級爭議）。","fact_refs":["f_kpi0_gaap_total_net_revenues","f_kpi1_gaap","f_kpi2_gaap","f_kpi3_adjusted_ebitda_gaap_non","f_kpi4_adjusted_ebitda_margin","f_kpi5_gaap","f_kpi11_funded_customers","f_kpi12_arpu","f_kpi13_total_platform_assets","f_kpi14_net_deposits","f_earnings_recency"],"verdict_values":{"revenue_quality":"交易性收入約六成，隨市場熱度與 take rate 波動；淨利息與訂閱等約四成較穩，但淨利息對利率敏感，管理層估算每升降一碼約影響營收1.5%","unit_econ_note":"年化 ARPU 200美元、資金客戶2,870萬；Q3 營業利益率48.1%、Adjusted EBITDA 利潤率57%；管理層稱每員工營收近200萬美元","archetype":{"primary":"金融","secondary":"品質複利成長","confidence":"中","fingerprint":"線上券商加上事件合約交易所與消費金融（信用卡、銀行），利潤率高，但交易收入循環性強"},"industry":{"clock_phase":"II","sd_verdict_source":"週期性為主、基準線結構性墊高：LSEG 研究指散戶流量隨景氣循環但基準線永久上移；HOOD 淨入金年化17%屬結構性，交易量屬週期性","bargaining":{"up":"上游做市商以委託單流量付款支付股票與選擇權收入。Rule 605 自2026-08起適用，同業也可能放棄 PFOF，議價權偏向監管與做市商","down":"下游散戶在零佣金下轉戶成本低，公司靠 Gold、銀行直存與信用卡把轉換成本拉到家戶層","geo":"國際客戶逾100萬，英國、歐盟、加拿大、杜拜、新加坡擴張中；國際營收占比事實表未涵蓋"},"profit_pool_dir":"利潤池由加密交易移向選擇權、事件合約、訂閱與放款；事件合約改走自有 Rothera 交易所，取回原本付給 Kalshi 的交易所層經濟","tam_table":[{"item":"預測市場規模（Bernstein 預估2028年）","value":"17億美元"},{"item":"Rothera 營收（高盛預估2027年）","value":"3.07億美元；高盛的預測市場預估高於共識10%（2027）與14%（2028）"},{"item":"Trump Account 合格兒童","value":"約7,000萬名，Dell 基金會為其中2,500萬名各投入250美元"},{"item":"Gold 滲透率","value":"約17–18%（500萬÷2,870萬），當季新客約40%"},{"item":"美國散戶可投資資產、HOOD 份額與各段利潤池占比五年變化","value":"事實表未涵蓋"}]}}},"q2_moat":{"verdict":"護城河方向持平，屬窄護城河：產品速度與淨入金顯示份額仍在擴大，但 take rate 與委託單流量付款承壓，兩者相抵。","reasoning":"機制：低成本獲客加上產品速度累積散戶資產，再用 Gold 會員把交易、銀行、信用卡綁在一起。執行力8分：HOOD Summit 一次推出17項產品，年化逾1億美元的業務線增至14條，全年 Adjusted opex＋SBC 展望上緣由27.75億降至27.5億美元。定價力5分：管理層把 take rate 視為結果而非目標，Q3 take rate 低於多數分析師預期，10月價差再收窄；事件合約改動態定價後讓利客戶，但維持整體 take rate。同業對照：HOOD 營業利益率45.7%，遠低於 IBKR 的86.3%，利差為負；高於 COIN 的5.7%。威脅：委託單流量付款與 take rate 的結構壓力列生態層級（扣1分）；預測市場進入者、加密原生平台、大型券商與 AI 落後風險列點對點。合計約5.5分，等級 C。報酬持續期：以資產負債表計屬高利益率×低周轉，四個檢查點皆為中性，最弱一環是價值鏈分配。再投資：資本支出近乎零，成長來源是客戶資產，內生上限以淨入金年化17%代理。","fact_refs":["f_peer_hood_gross_margin_pct","f_peer_hood_operating_margin_pct","f_peer_hood_fcf_margin_pct","f_peer_ibkr_gross_margin_pct","f_peer_ibkr_operating_margin_pct","f_peer_ibkr_fcf_margin_pct","f_peer_schw_fcf_margin_pct","f_peer_coin_gross_margin_pct","f_peer_coin_operating_margin_pct","f_peer_coin_fcf_margin_pct","f_kpi14_net_deposits","f_kpi10_2026_adjusted_opex_sbc"],"verdict_values":{"moat":{"mechanism":"產品速度與低成本獲客累積散戶資產，再以 Gold 會員把交易、銀行、信用卡綁在一起，提高家戶層轉換成本；事件合約自建 Rothera 交易所，取得交易所層經濟","execution":8,"pricing":5,"grade":"C","trend":"→","trend_evidence":"執行力擴大：淨入金年化17%、平台資產年增19%、Gold 500萬、14條年化逾1億美元業務線；定價力縮減：Q3 take rate 低於預期、10月價差收窄、Rule 605 自2026-08起適用。兩者相抵，判持平","competitor_notes":[{"name":"IBKR","strategy_note":"營業利益率86.3%，FCF 利潤率遠高於 HOOD，成本與自動化優勢明顯，且已進入預測市場；HOOD 勝在年輕散戶獲客與產品介面，不在成本"},{"name":"SCHW","strategy_note":"FCF 利潤率52.3%，與 HOOD 的58.4%相近，其餘利潤率事實表缺；代表傳統大型券商在財富管理與資產規模上的守勢，HOOD 以銀行、退休帳戶與 Strategies 搶錢包份額"},{"name":"COIN","strategy_note":"營業利益率僅5.7%、加密單引擎；HOOD 加密收入年減55%仍守住約46%營業利益率，多元化較佳，但兩家同受去中心化平台擠壓"}],"spread_notes":null,"peer_na_reason":"同業 ROIC 與投入資本不在事實表，改以營業利益率代替：HOOD 45.7%對 IBKR 86.3%利差為負，對 COIN 5.7%為正","threats":[{"level":"🔴","text":"委託單流量付款與 take rate 的結構壓力：Rule 605 新揭露自2026-08起適用，同業可能放棄 PFOF；Q3 take rate 低於預期，10月價差再收窄","p":"35%","evidence_refs":["regulatory_antitrust#2","substitute_technology#4"]},{"level":"🟡","text":"預測市場進入者：IBKR、Coinbase 進場，2026年已有10家申請 DCM；HOOD 以自有 Rothera 及入股 Crypto.com 與 OG.com 應對","p":"40%","evidence_refs":["competitive_share_entrants#2"]},{"level":"🟡","text":"加密原生去中心化平台（如 Hyperliquid）與受較少監管的新創可更快推出產品；HOOD 以自有 Robinhood Chain 對沖","p":"30%","evidence_refs":["substitute_technology#3","substitute_technology#0","substitute_technology#2"]},{"level":"🟡","text":"既有券商、銀行與科技平台營運歷史更長、資本更大","p":"30%","evidence_refs":["competitive_share_entrants#0"]},{"level":"🟡","text":"跟不上 AI 技術演進的風險；目前 HOOD 在代理交易領先，代理帳戶資產逾2.5億美元","p":"30%","evidence_refs":["substitute_technology#1"]}],"roic_durability":{"quadrant":"高利益率×低周轉（TTM 營業利益率45.7%；資產負債表含客戶融資與現金，周轉低）","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者、決策者、付款者都是散戶本人，三個角色一致；但交易屬「想要」而非「需要」，LSEG 研究指散戶流量隨景氣循環、只是基準線墊高。銀行直存（附加率約40%）與信用卡較接近「需要」，比重仍小。"},{"item":"決策層級","level":"🟡","text":"在交易層轉戶成本低（零佣金、帳戶可轉移），但在家戶財務層正在上升：Gold 會員500萬、當季新客約40%加入，Robinhood Banking 未全面開放即成為券商客戶第一大提款去向。漲價後流失率與分客群留存率事實表未涵蓋。"},{"item":"價值鏈分配","level":"🟡","text":"股票與選擇權的錢主要由做市商以委託單流量付款支付，Rule 605 與同業放棄 PFOF 的可能性使這段分配偏向監管與做市商；事件合約改走自有 Rothera，取回原本付給 Kalshi 的交易所層經濟；鏈上收入約一半分給 Arbitrum。"},{"item":"社會容忍度","level":"🟡","text":"預測市場體育合約有州級爭議，委託單流量付款長期受監管檢視，向年輕客群發卡伴隨提列上升，cash sweep 集體訴訟仍在進行。法務長6月表示全面禁令不太可能，但這個判斷依賴 CFTC 的聯邦管轄認定，屬政策風險。"}],"roiic":"事實表未涵蓋：券商增量投入資本（監管淨資本、信用卡放款）的口徑缺，無法計算","reinvest_rate":"近乎零：Q3 資本支出2,100萬美元，對營業現金流12.25億美元；實際的再投資在信用卡放款與監管淨資本，金額事實表未涵蓋","endo_ceiling":17,"formula_note":"券商的成長來源是客戶資產而非股東資本，因此以淨入金年化率（Q3 年化17%、近12個月21%）代理內生成長上限，取低值17%；增量 ROIC×再投資率的標準公式因投入資本口徑缺而無法計算"}}}},"q3_growth":{"verdict":"五年後仍有寬跑道：Gold 滲透率約18%，銀行尚未全面開放，Trump Account 約7,000萬名合格兒童，國際客戶剛破百萬，第二條曲線有來源佐證。但共識三年 EPS 年複合約28.7%，高於以淨入金代理的內生上限17%，差距主要靠利潤率擴張補。","reasoning":"成長以量為主：淨入金、交易量與事件合約放量；價（take rate）為負貢獻；併購小（WonderFi 約30萬客戶）；淨回購約1個百分點。共識三年 EPS 年複合＝（4.37÷2.05）^(1/3)−1＝28.7%，即 FY2025A 2.05美元到 FY2028E 4.37美元；EPS 共識家數事實表未涵蓋，營收共識為27–28位。內生上限以淨入金年化17%代理，缺口約11.7個百分點。缺口主要歸因於利潤率擴張（共識 FY2027 EPS 年增40%、營收年增29%），淨回購約1個百分點，其餘來自新業務的營運槓桿，無法逐項歸因，因此長期信心上限為中。五年後跑道判寬：Gold 滲透率約18%，低於35%；且下一條曲線有來源佐證，包括 Rothera 首個完整季即達年化1億美元、Trump Account 完成自動開戶、Robinhood Banking 成為券商客戶第一大提款去向、國際客戶逾100萬並取得杜拜授權。衰退訊號亮1個（共識 EPS 增速顯著高於營收）、半亮1個（SBC 占營收5.6%），長期成長性中等。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_kpi14_net_deposits","f_kpi13_total_platform_assets","f_kpi11_funded_customers","f_kpi8_sbc"],"verdict_values":{"growth":{"driver_mix":"量為主（淨入金、交易量、事件合約），價為負（take rate 下行），併購小（WonderFi），淨回購約1個百分點","runway_years":"事實表未涵蓋（美國散戶可投資資產與開戶滲透率的分母缺）","runway_post_y5":"🟢","endo_ceiling_basis":"以淨入金年化率代理：Q3 年化17%、近12個月21%，取低值17%；券商收入隨客戶資產規模走，股東資本再投資不是成長來源","segments":[{"item":"交易性收入","value":"8.67億美元，年增19%（選擇權3.99億＋31%、股票1.21億＋41%、事件合約1.73億、加密1.20億−55%），約占營收61%"},{"item":"淨利息收入","value":"4.15億美元，年減9%，主因證券借貸餘額下降，約占營收29%"},{"item":"其他收入","value":"1.42億美元，年增61%（Gold 訂閱與 Trump Account 服務），約占營收10%"}],"decay_signals":[{"signal":"毛利率連2季年減","status":"資料缺口","note":"只有年度與 TTM：TTM 81.4%對 FY2025 83.3%，季度序列事實表未涵蓋"},{"signal":"核心市占近12個月縮減","status":"未亮","note":"管理層稱股票、選擇權、加密、融資市占皆雙位數成長，但無第三方數據"},{"signal":"主力產品提價後銷量下滑","status":"未亮","note":"事件合約改動態定價後未見量縮，10月日均量較Q3增約10%"},{"signal":"EPS 年複合顯著高於營收年複合","status":"亮","note":"共識 FY2027 EPS 年增40%、營收年增29%，差距逾5個百分點，倚賴利潤率擴張"},{"signal":"FCF/NI 低於0.75連2年","status":"未亮","note":"FY2024 為負、FY2025 約0.84，未連2年"},{"signal":"SBC 占營收超過5%且逐年上升","status":"半亮","note":"Q3 為5.6%，超過5%；逐年趨勢事實表未涵蓋"},{"signal":"TAM 萎縮或被替代技術壓縮","status":"未亮","note":"加密收入年減55%屬循環；去中心化平台威脅列入觀察"},{"signal":"產業估值倍數近3年系統性下移","status":"資料缺口","note":"同業倍數序列事實表未涵蓋"},{"signal":"維持性資本支出占 FCF 超過60%","status":"未亮","note":"Q3 資本支出2,100萬美元，對 FCF 12.04億美元"},{"signal":"停止投資且收入3年內下滑","status":"未亮","note":"營收 FY2022–2025 由13.6億增至44.7億美元"}],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"資本配置中等：自由現金流充沛，SBC 已降到營收約5.6%；但回購在本益比35倍附近進行，買入盈餘殖利率僅約2.7%。","reasoning":"最小交付：Q3 營業現金流12.25億美元、資本支出2,100萬美元，FCF 12.04億美元，約為淨利的2.5倍；券商現金流含客戶餘額變動，季度雜訊大。年度 FCF/NI：FY2024 為負，FY2025 約0.84。SBC 8,000萬美元，占營收5.6%、占營業利益11.7%。淨現金約22.8億美元。現金去向四分：回購（年初至Q2 買回750萬股、6.64億美元，均價約88.5美元）；併購（WonderFi 約1.8億美元）；信用卡放款與監管資本（金額事實表未涵蓋）；另於6月發行22億美元、0%票息、2029年到期的可轉債，股價300美元前無淨稀釋。計分：併購報酬無法驗證；回購盈餘殖利率約2.7%（FY1 共識 EPS 2.42美元÷均價88.5美元），低於10年期殖利率加2個百分點（10年期殖利率事實表未涵蓋，但在任何合理水準下都過不了）；SBC 以金額計每年約占市值0.4%，回購金額更大，淨稀釋應低於1.5%，惟歷年股數序列事實表未涵蓋。","fact_refs":["f_kpi7_ocf_1_225_capex_21","f_kpi8_sbc","f_kpi9_sbc","f_kpi10_2026_adjusted_opex_sbc","f_kpi5_gaap","f_net_debt_m","f_shares_diluted_m","f_consensus_eps_fy1"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":true,"passed":null,"input":"WonderFi 全現金約1.8億美元（2026-06），帶入約30萬資金客戶；併購後報酬事實表未涵蓋，無法驗證"},{"name":"buyback_yield","applicable":true,"passed":false,"input":"年初至Q2 買回750萬股、6.64億美元，均價約88.5美元；對 FY1 共識 EPS 2.42美元的盈餘殖利率約2.7%，低於10年期殖利率加2個百分點"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"Q3 SBC 8,000萬美元，年化約3.2億、占市值約0.4%；回購金額年化約13億美元，淨稀釋應低於1.5%；歷年股數序列事實表未涵蓋"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長主要來自自有產品與淨入金，併購金額小（WonderFi 約1.8億美元，不到市值0.3%），成長不靠併購撐"}}}},"q5_valuation":{"verdict":"現價要求2027年 EPS 接近共識3.39美元（年增40%），並維持25倍上下的倍數。我不完全相信：基本情境 FY2027 EPS 3.00美元，五年年化約8%，價格合理但不便宜。","reasoning":"現價86.27美元，對 FY1 共識 EPS 2.42美元為35.6倍，對 FY2 3.39美元為25.4倍，對 FY3 4.37美元為19.7倍。要划算，2027年 EPS 須接近共識（年增40%），且市場續給約25倍。共識方向有利：FY1 近3個月上修4.8%，FY2 與 FY3 近期各上修3.4%與4.6%。但Q3 GAAP EPS 0.51美元、年減16%，年化僅約2.0美元（調整後0.60美元，年化約2.4美元），離3.39美元的差距要靠利潤率擴張補。賣方平均目標價134.56美元（Koyfin 31位），範圍68–170美元，高低比2.5倍，分歧大，財報後未見修正，不作為支持。估值歷史只有2–4個年度端點（本益比分位44.6、P/S 分位54.2），沒有五年序列。結論是合理不便宜：12個月以 FY2027 基本情境 EPS 3.00美元×29倍估約87美元（＋1%）；3年以 FY2029 4.10美元×26倍估約107美元（＋24%）。技術面：RSI 31.5，股價低於52週均線97.15美元、貼近104週均線86.17美元，動能不過熱。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_pe_current","f_pe_percentile","f_ps_current","f_ps_percentile","f_ev_s_current","f_ev_s_fwd","f_ev_m","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_fy1_pct","f_consensus_rev_fy2_pct","f_consensus_rev_fy3_pct","f_consensus_rev_3m_fy1_pct","f_week26_return_pct","f_rsi14","f_ma_state","f_ma_w52","f_ma_w104"],"verdict_values":{"valuation":{"basis":"本益比為主（FY1 35.6倍、FY2 25.4倍）；金融業常用的 P/TBV 與 ROTCE 事實表未涵蓋","tier":"高成長券商","peers":{"expanded":false,"reason":"事實表的同業對照只有利潤率，沒有 SCHW、IBKR、COIN 的本益比或 P/TBV，無法做倍數對照；改以 HOOD 自身 FY2 與 FY3 共識本益比（25.4倍、19.7倍）作終端倍數的對照"},"fwd_pe":35.64,"peg":1.24,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"FY1 本益比35.6倍偏高，但 FY2 為25.4倍；以共識三年 EPS 年複合28.7%計，PEG 1.24，落在合理區。本益比只有2個年度端點（分位44.6），P/S 有4個端點（分位54.2），沒有五年序列。我的基本情境 EPS 低於共識，五年年化報酬約8%，屬中段，因此判合理偏中性，不到便宜。","upside_short_pct":1,"upside_mid_pct":24,"denominator_disputed":false,"denominator_note":"公司本季新增調整後 EPS（0.60美元，排除投資評價損失每股0.07美元等非營業項目），GAAP 為0.51美元，共識口徑未標明。差距約15%，但估值論證以 FY2 與 FY3 為主，分母口徑不是這次判斷的爭點；驗證一律以 GAAP 為準。"}}},"q6_how_wrong":{"verdict":"最可能看錯的地方，是把營收成長當成盈餘成長：本季營收年增12%，淨利卻年減14%，信用卡提列翻倍。價值陷阱風險中等。","reasoning":"三個可能看錯的方向。一、論點失敗：散戶交易下行，疊加委託單流量付款或事件合約受限、信用損失上升，悲觀情境五年終點約44美元（−49%），機率30%。二、論點成功但股東經濟變差：信用卡、Trump Account（全年約1億美元投入）、Robinhood Chain（約一半收入分給 Arbitrum）帶動營收卻壓低每股盈餘，Q3 已是實例。三、價格已反映太多：共識 FY2027 EPS 年增40%尚無證據。最大回撤：TIKR 2026-05 報導股價曾自高點下跌52%，悲觀終點跌幅約49%，持有期間最深回撤估在−45%至−65%，屬深回撤，要有心理準備；論點未破時不因波動砍倉。壓力測試五項，以單項衝擊下 FY2027 EPS 是否仍高於2.0美元判定：降息一碼、加密收入再腰斬、信用損失翻倍、事件合約禁令四項過（禁令後約2.04美元，屬勉強過）；交易性收入年減30%不過（約1.7美元）。衰退訊號亮1個、半亮1個，價值陷阱風險中等。","fact_refs":["f_kpi5_gaap","f_kpi1_gaap","f_kpi2_gaap","f_rsi14","f_week26_return_pct","f_ma_w52","f_ma_w104","f_ma_w250","f_earnings_recency"],"verdict_values":{"trap":{"verdict":"🟡","label":"營收成長、盈餘衰退的階段，不是典型價值陷阱，但盈餘品質待驗"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":2.42,"pe":35.65,"basis":"FY1（FY2026E）共識 EPS 2.42美元，現價86.27美元；終端倍數套在 FY2031 當年 EPS，與起點同為當年度口徑"},"eps":{"bull":[3.4,4.4,5.4,6.4,7.4],"base":[3.0,3.55,4.1,4.65,5.15],"bear":[2.05,2.15,2.4,2.7,2.95]},"pe":{"bull":30,"base":24,"bear":15},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0,"net_buyback":1.0},"second_stage":{"bull_cagr_pct":15,"base_cagr_pct":10},"max_dd":{"lo":-65,"hi":-45,"basis":"TIKR 2026-05 報導股價曾自高點下跌52%；散戶交易收入週期性高（LSEG 研究）；悲觀情境五年終點跌幅約49%。據此估持有期間最深回撤在−45%至−65%","trigger_time":null},"basis":{"bull":"共識路徑兌現：事件合約、信用卡、銀行與國際擴張放量，2027–28年 EPS 貼近共識3.39與4.37美元，之後年增約16%；倍數30倍（成長近20%、PEG 約1.5）","base":"營收年增約20%，但 take rate 與提列吃掉部分利潤率，FY2027 EPS 3.00美元（低於共識約12%），之後年增11–18%；終端24倍，介於現價 FY2 25倍與 FY3 20倍之間（同業本益比事實表未涵蓋）","bear":"散戶交易進入下行，委託單流量付款或事件合約受限，信用損失上升；FY2027 EPS 回落至2.05美元，五年後僅2.95美元；成長熄火至約10%，倍數15倍"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"Q3 淨利年減14%、淨利息收入年減9%；信用損失提列年增173%；業界每帳戶交易量季減7%；Rule 605 可能壓縮委託單流量付款","assumption":"淨利息、訂閱與銀行收入構成的經常性底盤能撐住交易下行","consequence":"五年後虧50%最可能的故事：散戶交易進入下行，委託單流量付款受限，信用卡損失擴大，EPS 停在約2.95美元，倍數壓到15倍，股價約44美元","ruling":"部分採納：悲觀機率定為30%。與唯一致命點部分重疊（委託單流量付款受限是這個故事的一環），已回補進觸發條件。不採納存續危機版本：券商子公司淨資本超額約37億美元，營業利益率48%","watch":"淨入金年化、信用損失提列占營收、選擇權與股票 take rate","evidence_refs":["end_markets#1","financial_capital_credit_cycle#0","supply_demand_durability#1","regulatory_antitrust#2"],"fact_refs":["f_kpi5_gaap","f_kpi2_gaap","f_kpi14_net_deposits"]},{"view":"論點成功但股東經濟變差","evidence":"Q3 營收年增12%，但 GAAP EPS 年減16%；信用卡放款擴張推高提列，公司不給 GAAP 總費用展望；Trump Account 全年約1億美元投入；Robinhood Chain 約一半收入分給 Arbitrum；公司新增排除投資評價損失的調整後 EPS","assumption":"新業務的營收成長能轉成每股盈餘","consequence":"用戶與資產照計畫成長，但每股盈餘落在悲觀與基本情境之間，倍數同步下修","ruling":"採納：本季就是營收成長、盈餘衰退的實例；驗證一律以 GAAP EPS 為準，調整後口徑只作參考","watch":"GAAP EPS 年增率減營收年增率的差距，連2季為負即下修基本情境","evidence_refs":["financial_capital_credit_cycle#1","financial_capital_credit_cycle#2","end_markets#1"],"fact_refs":["f_kpi5_gaap","f_kpi6_adjusted_eps_gaap_8_k_a","f_kpi0_gaap_total_net_revenues"]},{"view":"價格已反映太多","evidence":"FY1 本益比35.6倍；共識 FY2027 EPS 3.39美元需年增40%，而Q3 GAAP 年化僅約2.0美元；Q3 EPS 0.51美元，低於市場預期約0.55美元","assumption":"利潤率擴張與新業務放量能在一年內補上差距","consequence":"若2027年 EPS 只到3.00美元，現價對應約29倍，報酬全靠倍數維持","ruling":"採納一半：股價已比7月低21%，FY2 本益比25倍不算過高；但基本情境五年年化約8%，不足以追，進場價定在73美元","watch":"FY2027 共識修正方向與2027上半年 GAAP EPS","evidence_refs":["capital_markets_pricing#1"],"fact_refs":["f_fwd_pe_latest","f_consensus_eps_fy2","f_consensus_rev_fy2_pct","f_price_at_dd"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟠","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟠","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 109.86 → 本次 86.27（-21.5%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=109.86","side_b":"本次 price_at_dd=86.27","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 109.86 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 109.86 美元：Bull 價 264、Bear 價 64，五年期望值 +47.0%，基準年化 9.1%，不對稱比 2.8","side_b":"本次情境、股價仍用 109.86 美元：Bull 價 222、Bear 價 44.25，五年期望值 +13.2%，基準年化 2.4%，不對稱比 1.42","ruling":"先換情境、股價不動：五年期望值少 33.8 個百分點，基準年化少 6.7 個百分點。不對稱比由 2.8 變為 1.42。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 109.86 美元：五年期望值 +13.2%，基準年化 2.4%，不對稱比 1.42","side_b":"本次情境、股價 86.27 美元：五年期望值 +44.2%，基準年化 7.5%，不對稱比 2.69","ruling":"再換股價、情境不動：起點價下跌 21.5%，五年期望值多 31.0 個百分點，基準年化多 5.1 個百分點，不對稱比由 1.42 升到 2.69。合計五年期望值比前份少 2.8 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"盈餘品質：管理層說法對照 GAAP 結果","cause":null,"prior_field":null,"side_a":"CFO（2026-10-27 法說）稱核心業務全面發動，營收與 Adjusted EBITDA 創新高","side_b":"同季淨利4.76億美元、年減14%，稀釋 EPS 0.51美元、年減16%；淨利息收入年減9%，信用損失提列年增173%，另有每股0.07美元的投資評價損失","ruling":"可調和（程度差異）：營收端屬實，盈餘端被淨利息、提列與評價損失侵蝕；判斷一律以 GAAP 為準，調整後 EPS 只作參考","evidence_level":"公司新聞稿與10-Q（一手）","settle_metric":"Q4 2026 GAAP EPS 年增率","if_then":["若 Q4 2026 GAAP EPS 年增轉正，且信用損失提列占營收低於6%，基本情境 FY2027 EPS 上調至3.20美元，進場價隨之上移至約78美元","若 Q4 GAAP EPS 續年減且營收年增低於10%，維持不追，進場價下修至65美元"],"evidence_refs":["end_markets#1","capital_markets_pricing#1","financial_capital_credit_cycle#0"]},{"axis":"淨入金目標的達成方式","cause":null,"prior_field":null,"side_a":"CFO（2026-07-29 法說）稱年化20%為目標、不解讀單月；當時7月約40億美元為年內最低，未解釋原因","side_b":"Q3 淨入金157億美元，年化17%，低於目標；10月逾130億美元中含 Dell 家族一次性60億美元，剔除後約70億美元；公司宣布年度目標已達成","ruling":"可調和：年度目標達成有一部分靠一次性捐贈；H1 以剔除 Trump Account 捐贈後的年化率監測","evidence_level":"公司法說與新聞稿（一手）","settle_metric":"剔除一次性捐贈後的季度淨入金年化率","if_then":["若 Q4 剔除一次性捐贈後年化率不低於15%，維持 H1 判斷","若連2季低於10%，H1 降為削弱，並暫停任何加碼"],"evidence_refs":["supply_demand_durability#2"]},{"axis":"信用卡信用品質","cause":null,"prior_field":null,"side_a":"公司稱提列增加是因放款簿擴張（Q3 新聞稿）；CFO 稱信用卡要先把單位經濟與信用風險做對才放量","side_b":"信用卡相關提列由2,300萬增至6,100萬美元；二手來源稱90天以上逾期率由約2%升至6%，未與一手10-Q 對照","ruling":"不可裁決，要到2027年2月的10-K 才能定：決勝數據（一手逾期率）不在證據包內。在此之前以提列占營收作代理，Q3 約5%，列為警示","evidence_level":"提列為一手；逾期率為二手待核","settle_metric":"10-K 揭露的信用卡90天以上逾期率","if_then":["若10-K 揭露逾期率不低於5%，持有部位減碼一半，並把悲觀機率升至35%","若逾期率低於3%，且提列占營收回落到4%以下，移除這條減碼條件"],"evidence_refs":["financial_capital_credit_cycle#0","financial_capital_credit_cycle#1","financial_capital_credit_cycle#2"]},{"axis":"take rate 走向：前一季說法對照本季結果","cause":null,"prior_field":null,"side_a":"CFO（2026-07-29 法說）稱7月 take rate 與Q2 平均相近，建議以此為起點","side_b":"Q3 take rate 低於多數分析師預期（Truist 提問）；CFO 歸因於穩定幣產品 Robinhood Earn 變現較低與事件合約改動態定價；10月價差再收窄","ruling":"可調和但方向不利：屬組合與價差因素，未見管理層失信；但與 Rule 605 生效、同業可能放棄 PFOF 疊加，是護城河改判持平的主要依據","evidence_level":"公司法說（一手）＋10-Q","settle_metric":"選擇權與股票每單位成交收入","if_then":["若 Q4 選擇權與股票 take rate 季減超過15%，減碼三分之一","若 take rate 回穩且交易量維持Q3 水準，維持現有判斷"],"evidence_refs":["substitute_technology#4","regulatory_antitrust#2"]},{"axis":"管理層承諾兌現","cause":null,"prior_field":null,"side_a":"6月與7月法說迴避的問題：Zelle 類功能時程、美國永續合約時程、Rothera 承接比例、預測市場若下架的替代收入","side_b":"Q3 已示範點對點轉帳（有限開放），推出永續合約，宣布年底前絕大多數事件合約流量走 Rothera 與 Crypto.com；預測市場下架時的替代收入仍未回答","ruling":"一致為主：產品承諾大致兌現；唯一仍未回答的是監管下架情境，保留在 R3","evidence_level":"法說逐字稿（一手）","settle_metric":"事件合約可交易州數與收入","if_then":["若事件合約遭主要州禁令，而公司仍未提出替代收入，事件合約相關營收從基本情境剔除"],"evidence_refs":[]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"RSI 31.5，接近超賣；股價比7月低21%，已在前份進場區下方；FY3 共識本益比19.7倍；共識近3個月上修；淨入金與平台資產創紀錄，Gold 500萬；利率回升是收入順風，管理層估每升一碼約增營收1.5%","side_b":"Q3 盈餘年減、提列翻倍、take rate 下行，共識 FY2027 EPS 年增40%尚無證據；基本情境五年年化約8%","ruling":"不採納現在進場：約束條件是基本情境報酬不足12%。否定條件為股價跌到73美元以下，或2027上半年 GAAP EPS 證實共識路徑","evidence_level":"綜合","settle_metric":"2027上半年 GAAP EPS","if_then":["若股價續跌但 Q4 財報顯示營收年增不低於15%、提列占營收低於6%（基本面無損），在73美元以下分批建倉","若股價先反彈到100美元以上但盈餘證據未到，不追"],"evidence_refs":[]},{"axis":"前份風險門檻的處置","cause":"新證據","prior_field":null,"side_a":"前份風險：加密收入連2季年減即觸發；ARPU 連4季年減且無新線補即砍倉檢討","side_b":"加密門檻退休：Q3 加密收入年減55%，但交易性收入年增19%，前份「加密−40%而交易總收入仍成長」的驗證點已通過，加密占營收降至約8%。ARPU 門檻保留（資料來源為季報，Q3 年化200美元），改為連4季年減且淨入金年化低於15%才減碼","ruling":"加密不再是單一致命變數；ARPU 單獨下滑可能來自國際與年輕客群（管理層說法），須搭配淨入金判斷","evidence_level":"公司新聞稿（一手）","settle_metric":"ARPU 年增率與淨入金年化率","if_then":["若 ARPU 連4季年減且淨入金年化低於15%，減碼三分之一"],"evidence_refs":["end_markets#0"]},{"axis":"估值結論與裁決的漂移","cause":"價格變動","prior_field":["val"],"side_a":"前份（2026-07-14，股價109.86美元）估值偏貴，裁決觀望","side_b":"本次股價86.27美元，下跌21%；FY1 共識 EPS 近3個月由2.31上修至2.42，FY2 本益比25.4倍，估值改判合理；裁決與角色依本輪輸入重新推導","ruling":"估值結論改變的主因是股價下跌，不是基本面改善；本季基本面反而偏弱，因此不把較低價格直接當成進場理由","evidence_level":"市場價格與共識快照","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"護城河方向的漂移","cause":"新證據","prior_field":["moat_trend"],"side_a":"前份判護城河擴大","side_b":"本次判持平：份額與淨入金仍在擴大，但Q3 take rate 低於預期、10月價差再收窄、Rule 605 自2026-08起適用，預測市場2026年已有10家申請 DCM","ruling":"執行力擴大與定價力縮減相抵；若連2季 take rate 回穩且事件合約維持份額，可回到擴大","evidence_level":"公司法說（一手）＋10-Q＋產業報導","settle_metric":"選擇權與股票 take rate、事件合約份額","if_then":["若連2季 take rate 季增，且事件合約非體育占比續升，護城河方向回調為擴大","若 take rate 季減超過15%，減碼三分之一"],"evidence_refs":["regulatory_antitrust#2","competitive_share_entrants#2","substitute_technology#4"]},{"axis":"五年後成長跑道的漂移","cause":"新證據","prior_field":["runway_post_y5"],"side_a":"前份判中等跑道","side_b":"本次判寬：Trump Account 約7,000萬名合格兒童完成自動開戶；Robinhood Banking 未全面開放即成為券商客戶第一大提款去向；Rothera 首個完整季達年化1億美元；國際客戶逾100萬並取得杜拜授權","ruling":"第二條曲線有來源佐證，Gold 滲透率約18%，低於35%；但新曲線尚未貢獻盈餘，信心維持中","evidence_level":"公司法說（一手）＋賣方預估","settle_metric":"非交易收入占營收、Gold 滲透率","if_then":["若2027年非交易收入占比跌破35%，跑道回調為中等"],"evidence_refs":["supply_demand_durability#2","end_markets#3"]},{"axis":"進場條件的漂移","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"Q2（7/29）確認非加密交易性收入不靠加密回補 且 事件合約監管未惡化（Wisconsin 等禁令未擴大），或回檔至 $90-95（Fwd PE≈30x）；則轉進場·衛星 starter","side_b":"股價≤73美元（基本情境年化報酬約12%），或2027上半年 GAAP EPS 合計≥1.50美元且信用損失提列占營收<6%；觸發後建試探倉","ruling":"舊進場條件的價格段已經觸及（現價86.27美元，低於90–95美元），Q2 非加密交易收入也確實成長；但Q3 出現淨利年減14%與提列翻倍的新證據，基本情境 EPS 下修，因此進場價下移到73美元，並加上盈餘驗證分支。進場動作仍是建試探倉","evidence_level":"公司新聞稿與10-Q（一手）","settle_metric":"收盤價；2027上半年 GAAP EPS","if_then":["若股價跌到73美元以下且未出現監管禁令，建試探倉，不超過1.5%"],"evidence_refs":["end_markets#1","financial_capital_credit_cycle#0"]},{"axis":"重檢後維持的欄位","cause":"新證據","prior_field":["signal","trap","archetype","cycle_position"],"side_a":"前份：綜合評等 B、價值陷阱風險中等、金融型、不適用循環位置","side_b":"本次重檢後四項維持：B、中等、金融型（券商加消費金融）、不適用循環位置","ruling":"本季正負證據並存（營收與淨入金創高，盈餘與信用轉弱），淨效果不足以改變這四項","evidence_level":"公司新聞稿與10-Q（一手）","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"情境機率與回撤的漂移","cause":"方法變動","prior_field":["p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份機率樂觀25%、悲觀30%，最大回撤單點−60%","side_b":"本次機率維持樂觀25%、基本45%、悲觀30%；最大回撤改為區間−45%至−65%（方法要求區間）","ruling":"共識三年 EPS 年複合28.7%超過以淨入金代理的內生上限17%，悲觀機率不得低於30%，因此維持30%；回撤改用區間表達，中點與前份相近","evidence_level":"情境假設","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"Single Thing 設定","cause":"方法變動","prior_field":null,"side_a":"前份未設定唯一致命點（null）","side_b":"Single Thing：美國監管（SEC 規則或州層級執法）實質禁止或限制股票與選擇權的委託單流量付款（PFOF）","ruling":"Single Thing 須是數學上最大的單一敏感項：選擇權加股票交易收入約占營收36.5%，大於事件合約（約12%）與加密（約8%）；發生時減碼至半倉","evidence_level":"公司新聞稿與10-Q（一手）","settle_metric":"SEC 公告、10-Q 風險措辭","if_then":["若 SEC 正式採納禁止或實質限制 PFOF 的規則，減碼至半倉"],"evidence_refs":["regulatory_antitrust#2","substitute_technology#4"]},{"axis":"減碼與清倉門檻設定","cause":"方法變動","prior_field":null,"side_a":"前份未設定減碼與清倉門檻（null）","side_b":"新設六項：淨入金年化連2季低於10%；信用損失提列占營收連2季超過7%；選擇權加股票交易收入連2季年減；事件合約收入季減超過30%或禁令生效；GAAP 營業利益率連2季低於35%；ARPU 連4季年減且淨入金年化低於15%。觸發即減碼；近12個月淨入金連6季低於5%則清倉","ruling":"把前份散在風險表的門檻集中成可監測的減碼與清倉條件，資料來源皆為公司季報與10-Q","evidence_level":"方法","settle_metric":null,"if_then":["任一減碼門檻觸發即減碼；淨入金連6季低於5%則清倉"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"股價回落至73美元以下且未出現監管禁令，建試探倉","type":"估值rearm","maps_to":"H2","metric":"收盤價","threshold":"≤73美元（基本情境五年年化報酬約12%）","action":"建試探倉，不超過組合1.5%","source_freq":"每日收盤","date":null,"evidence_refs":[]},{"n":2,"text":"2027年上半年盈餘證實共識路徑","type":"假設驗證","maps_to":"H2","metric":"2027年Q1＋Q2 GAAP EPS 合計；信用損失提列占營收","threshold":"EPS 合計≥1.50美元，且提列占營收<6%","action":"建試探倉；已持有則加碼至3%","source_freq":"季報","date":"2027-08","evidence_refs":[]},{"n":3,"text":"信用卡損失擴大","type":"風險","maps_to":"R2","metric":"信用損失提列占營收；10-K 信用卡90天以上逾期率","threshold":"提列占營收連2季>7%，或逾期率≥5%","action":"持有部位減碼一半，悲觀機率升至35%","source_freq":"季報與年報","date":"2027-02","evidence_refs":["financial_capital_credit_cycle#0","financial_capital_credit_cycle#1","financial_capital_credit_cycle#2"]},{"n":4,"text":"監管實質禁止或限制股票與選擇權的委託單流量付款","type":"Single Thing","maps_to":"Single Thing","metric":"SEC 規則或州層級執法結果","threshold":"正式採納禁止或實質限制 PFOF 的規則或命令","action":"減碼至半倉，以悲觀路徑重估 FY2027–28 EPS","source_freq":"SEC 公告、10-Q","date":null,"evidence_refs":["regulatory_antitrust#2","substitute_technology#4"]},{"n":5,"text":"事件合約遭禁令或收入急縮","type":"風險","maps_to":"R3","metric":"事件合約收入；可交易州數","threshold":"季減>30%，或主要州及聯邦層級禁令生效","action":"減碼三分之一，重評 H3 新業務占比","source_freq":"季報、CFTC 與法院公告","date":null,"evidence_refs":["competitive_share_entrants#2","regulatory_antitrust#0"]},{"n":6,"text":"cash sweep 集體訴訟進入不利階段","type":"風險","maps_to":"R5","metric":"Dey 與 Deeney 案的程序與金額","threshold":"集體認證通過，且和解或判決金額超過一季淨利（約4.76億美元）","action":"減碼一半","source_freq":"10-Q 與10-K 訴訟附註","date":null,"evidence_refs":["major_events#2","lawsuit_class_action#0"]},{"n":7,"text":"平台或第三方服務中斷","type":"風險","maps_to":"H1","metric":"平台中斷事件（AWS、清算、做市商系統）","threshold":"單次中斷超過1個完整交易日，或引發監管調查與客戶賠償","action":"停止加碼，複審第三方依賴","source_freq":"事件發生時、8-K","date":null,"evidence_refs":["geo_supply_chain#0","geo_supply_chain#1"]},{"n":8,"text":"用戶資產飛輪反轉","type":"清倉","maps_to":"H1","metric":"近12個月淨入金成長率","threshold":"連6季<5%","action":"清倉","source_freq":"季報","date":null,"evidence_refs":[]},{"n":9,"text":"Q4 2026 財報與2027年費用展望","type":"複審日期","maps_to":"H2","metric":"2027年 Adjusted opex＋SBC 展望增幅，對照營收共識增幅","threshold":"費用展望增幅高於營收共識增幅","action":"複審基本情境 EPS 與進場價","source_freq":"季報","date":"2027-02","evidence_refs":[]}],"kill_metrics":[{"metric":"季度淨入金年化成長率（剔除 Trump Account 一次性捐贈）","bear_threshold":"連2季<10%（Q3 為17%）","window":"每季，2027全年","source":"公司季報新聞稿與月度營運數據","last_status":"ok"},{"metric":"信用損失提列占營收","bear_threshold":"連2季>7%（Q3 約5.0%，去年同期約2%）","window":"每季","source":"10-Q 損益表","last_status":"warning"},{"metric":"選擇權加股票交易收入年增率","bear_threshold":"連2季年減","window":"每季","source":"季報收入分項","last_status":"ok"},{"metric":"事件合約收入","bear_threshold":"季減>30%，或主要州及聯邦層級禁令生效","window":"12個月","source":"季報收入分項、CFTC 與州法院公告","last_status":"ok"},{"metric":"GAAP 營業利益率","bear_threshold":"連2季<35%（Q3 為48.1%）","window":"每季","source":"季報損益表","last_status":"ok"},{"metric":"年化 ARPU","bear_threshold":"連4季年減，且淨入金年化<15%","window":"4季","source":"公司季報","last_status":"unknown"}],"evidence_dismissed":[{"ref":"reg_tariff_export#0","reason":"這條是10-K 的通用風險措辭，只說關稅透過市場波動間接影響，本身就註明沒有產品或供應鏈的直接關稅暴露；同軸另一條新聞顯示關稅消息日股價單日僅跌約1.6%，證據沒有指出任何 HOOD 特有的損益傳導路徑"}],"action_conditions":{"rearm_trigger":"股價≤73美元（基本情境年化報酬約12%），或2027上半年 GAAP EPS 合計≥1.50美元且信用損失提列占營收<6%","exec_line":"觸發後先建試探倉，不超過1.5%，不追高；跌到73美元以下、但同時出現委託單流量付款或事件合約禁令時，不進場","holding_cap":"首倉≤1.5%，盈餘驗證後上限3%"}},"decision_inputs":{"signal":"B","ma":"🟠","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等股價≤73美元，或2027年上半年 GAAP EPS 合計≥1.50美元且信用損失提列占營收<6%","asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null},"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8w(原9b)","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='C'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟠'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟢', val='🟡', moat_trend='→', week26=12.66, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='金融', cycle_position=None, moat='C', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":false,"basis":"signal='B', val='🟡'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":false,"basis":"signal='B', val='🟡', ma='🟠'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":true,"basis":"signal='B', val='🟡', ma='🟠'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟡', ma='🟠'"},{"row":"8w","condition":"判斷者宣告 wait_for_price（價格合理但要等）→ 原 row9b 進場改觀望（等價格）","hit":true,"basis":"wait_for_price=True, 等待條件='等股價≤73美元，或2027年上半年 GAAP EPS 合計≥1.50美元且信用損失提列占營收<6%'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":null,"requires_critic":[]},"thesis":{"H":[{"id":"H1","text":"用戶資產飛輪：淨入金維持兩位數成長，帶動平台資產與交易量複利","2y":null,"5y":"2031年前平台資產達8,000億美元、資金客戶達3,500萬","10y":null,"threshold":"季度淨入金年化≥15%（剔除 Trump Account 一次性捐贈），且資金客戶年增≥5%；Q3 為年化17%、資金客戶年增7%","source":"公司季報新聞稿與月度營運數據","drift_rule":"近12個月淨入金成長率連4季低於門檻5個百分點以上（即<10%）為削弱；連6季低於門檻10個百分點以上（即<5%）為反轉"},{"id":"H2","text":"非加密交易與新業務撐起盈餘，2027年 GAAP EPS 接近共識","2y":"FY2027 GAAP EPS ≥3.05美元（共識3.39美元的九成）","5y":null,"10y":null,"threshold":"FY2027 GAAP EPS ≥3.05美元；扣除加密後的交易性收入年增≥20%（Q3 選擇權＋31%、股票＋41%）","source":"季報 GAAP 損益表與交易性收入分項","drift_rule":"近12個月 GAAP EPS 對門檻路徑連2季落後5%以上為削弱，連3季落後10%以上為反轉"},{"id":"H3","text":"訂閱、銀行與信用卡讓收入由交易驅動轉向經常性，交易淡年仍維持高利潤","2y":null,"5y":null,"10y":"2036年前非交易收入（淨利息加其他）占營收≥45%；任一交易量年減的年度，GAAP 營業利益率≥30%","threshold":"Gold 滲透率（訂戶÷資金客戶）≥18%且逐年上升；非交易收入占營收≥39%（Q3 為39%）","source":"年報與季報收入分項、Gold 訂戶數","drift_rule":"跨2個年度 Gold 滲透率或非交易收入占比下滑為削弱，跨3個年度為反轉"}],"R":[{"id":"R1","text":"交易熱度與 take rate 同步回落：Q3 營收與 EPS 略低於預期，淨利息收入年減9%、淨利年減14%；10月股票、選擇權、加密日均量較Q3 低約5%，價差收窄；業界每帳戶交易量季減7%","h_ref":"H2","clock":"⚡","threshold":"營收年增連2季<10%，或交易性收入連2季季減>10%","evidence_refs":["capital_markets_pricing#1","end_markets#1","supply_demand_durability#1"]},{"id":"R2","text":"信用卡放款擴張帶來信用風險：Q3 信用損失提列7,100萬美元，去年同期2,600萬；二手來源稱90天以上逾期率由約2%升至6%（未經一手核對）","h_ref":"H3","clock":"🔥","threshold":"信用損失提列占營收連2季>7%（Q3 約5%），或10-K 揭露信用卡90天以上逾期率≥5%","evidence_refs":["financial_capital_credit_cycle#0","financial_capital_credit_cycle#1","financial_capital_credit_cycle#2"]},{"id":"R3","text":"監管壓力集中在收費點：Rule 605 新揭露自2026-08起適用，可能壓縮委託單流量付款；預測市場體育合約有州級爭議，2026年已有10家申請 DCM 加入競爭；公司也持續面臨多個監管機關的調查與檢查；管理層6月被問到預測市場若下架的替代收入時，未給出計畫","h_ref":"H2","clock":"🔥","threshold":"選擇權與股票合計 take rate 季減>15%，或事件合約收入季減>30%，或主要州及聯邦層級禁令生效","evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#2","competitive_share_entrants#2"]},{"id":"R4","text":"替代者與新進者：受較少監管的科技公司與加密原生平台（如 Hyperliquid）可更快推出產品，大型券商與銀行資本更厚，AI 演進也可能改變競爭位置；HOOD 以自建 Robinhood Chain 與代理交易對沖","h_ref":"H1","clock":"🐢","threshold":"資金客戶年增連4季<3%，且管理層停止揭露或改口份額成長","evidence_refs":["substitute_technology#0","substitute_technology#1","substitute_technology#2","substitute_technology#3","competitive_share_entrants#0"]},{"id":"R5","text":"法律訴訟：cash sweep 集體訴訟（Dey、Deeney）在2025-04部分駁回後續行，求償金額未明，涉及淨利息收入所依賴的 sweep 安排","h_ref":"H3","clock":"🐢","threshold":"集體認證通過，且和解或判決金額超過一季淨利（約4.76億美元）","evidence_refs":["major_events#2","lawsuit_class_action#0"]}],"single_thing":{"description":"美國監管（SEC 規則或州層級執法）實質禁止或限制股票與選擇權的委託單流量付款（PFOF）","why_fatal":"選擇權加股票交易收入Q3 合計5.2億美元，約占營收36.5%，主要以 PFOF 收取，是單一最大的敏感項（事件合約約12%、加密約8%）。零佣金模式一旦失去主要收費點，只能改收佣金或拉寬價差，客戶數與 take rate 會同時受壓","if_happens":"減碼至半倉，改用悲觀路徑重估 FY2027–28 EPS；公司公布替代收費結構並有一季實績之前不加碼","how_monitor":"SEC 規則提案與公告、Rule 605 實施後的執行品質揭露、紐約州檢察長自2023-07起的調查進度、10-Q 風險措辭、每季選擇權與股票 take rate","probability":"12–24個月約10%：證據包內只見 Rule 605 新揭露規則生效與紐約州檢察長調查，未見禁令提案"}},"appendix_a":{"growth_durability":7,"quality_score":6,"ai_risk":"🟡","long_term_confidence":"中","fpe_fy2":25.4,"peg_fy2":0.88,"stress":{"pass":4,"total":5}},"eps_meta":{"base_eps_path":{"FY2025A":2.05,"FY2026E":2.42,"FY2027E":3.39,"FY2028E":4.37},"fy_end_month":12,"eps_basis":"Koyfin 共識（FY1–FY3），GAAP 或調整後口徑未標明；Q3 市場預期約0.55美元，介於 GAAP 0.51美元與調整後0.60美元之間；FY2025A 取年報稀釋 EPS 2.05美元"},"catalysts":[{"date":"2027-02","date_precision":"month","type":"guidance","event":"Q4 2026 財報與2027年費用展望","impact":"高","watch":"2027年 Adjusted opex＋SBC 增幅對照營收增幅；信用損失提列"},{"date":"2027-02","date_precision":"month","type":"regulatory","event":"10-K 揭露信用卡逾期率與 cash sweep 訴訟進度","impact":"高","watch":"90天以上逾期率是否≥5%；集體認證進度"},{"date":"2026-12","date_precision":"month","type":"product","event":"全天候股票交易上線","impact":"中","watch":"上線後股票日均量與新開戶"},{"date":"2026-12","date_precision":"month","type":"product","event":"Robinhood Banking 點對點轉帳擴大開放；財報與公司 KPI 事件合約上線","impact":"中","watch":"銀行存款；事件合約非體育占比（Q3 約30%）"},{"date":"2027-03","date_precision":"quarter","type":"macro","event":"聯準會利率決策","impact":"中","watch":"管理層估算每升一碼約增營收1.5%"}]}
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
