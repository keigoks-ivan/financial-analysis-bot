你是 DD 管線 v20 的判斷層閘（gate），標的 COIN（20261103）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（44 條）
- `f_kpi0_total_revenue_gaap`（q1_business）｜Total revenue (GAAP)＝1215.6 USD M（YoY -35%，QoQ -0.4%）｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：SEC 8-K Q3 2026 earnings deck https://www.sec.gov/Archives/edgar/data/0001679788/000167978826000121/q326earningsdeck_vsec.htm（IR 新聞稿 investor.coinbase.com 未直接取得）（numbers.latest_quarter_kpis.items[0]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-29））
  - 註記：無共識數據（未查）
- `f_kpi1_net_revenue`（q1_business）｜Net revenue＝1160.5 USD M（YoY -34%，QoQ +1%）｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：SEC 8-K Q3 2026 earnings deck https://www.sec.gov/Archives/edgar/data/0001679788/000167978826000121/q326earningsdeck_vsec.htm（IR 新聞稿 investor.coinbase.com 未直接取得）（numbers.latest_quarter_kpis.items[1]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-29））
  - 註記：無共識數據（未查）
- `f_kpi2_gaap_operating_income`（q1_business）｜GAAP operating income＝61.7 USD M｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：SEC 8-K Q3 2026 earnings deck https://www.sec.gov/Archives/edgar/data/0001679788/000167978826000121/q326earningsdeck_vsec.htm（IR 新聞稿 investor.coinbase.com 未直接取得）（numbers.latest_quarter_kpis.items[2]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-29））
  - 註記：無共識數據（未查）
- `f_kpi3_gaap_operating_margin`（q1_business）｜GAAP operating margin＝5.1 %（對 total revenue 61.7/1215.6）｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：SEC 8-K Q3 2026 earnings deck https://www.sec.gov/Archives/edgar/data/0001679788/000167978826000121/q326earningsdeck_vsec.htm（IR 新聞稿 investor.coinbase.com 未直接取得）（numbers.latest_quarter_kpis.items[3]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-29））
  - 註記：無共識數據（未查）
- `f_kpi4_net_income_gaap`（q1_business）｜Net income (GAAP)＝718.7 USD M（diluted EPS 2.51；含約715M 持有加密資產評價利益，該數字來自第三方未驗證）｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：SEC 8-K Q3 2026 earnings deck https://www.sec.gov/Archives/edgar/data/0001679788/000167978826000121/q326earningsdeck_vsec.htm（IR 新聞稿 investor.coinbase.com 未直接取得）（numbers.latest_quarter_kpis.items[4]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-29））
  - 註記：無共識數據（未查）
- `f_kpi6_stock_based_compensation`（q1_business）｜Stock-based compensation＝233.0 USD M（占 GAAP 營業利益約 378%；占營收 19.2%）｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：SEC 8-K Q3 2026 earnings deck https://www.sec.gov/Archives/edgar/data/0001679788/000167978826000121/q326earningsdeck_vsec.htm（IR 新聞稿 investor.coinbase.com 未直接取得）（numbers.latest_quarter_kpis.items[6]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-29））
  - 註記：無共識數據（未查）
- `f_kpi7_subscription_services_re`（q1_business）｜Subscription & services revenue＝570.2 USD M（QoQ +3%，YoY -20%）｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：SEC 8-K Q3 2026 earnings deck https://www.sec.gov/Archives/edgar/data/0001679788/000167978826000121/q326earningsdeck_vsec.htm（IR 新聞稿 investor.coinbase.com 未直接取得）（numbers.latest_quarter_kpis.items[7]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-29））
  - 註記：無共識數據（未查）
- `f_kpi8_transaction_revenue`（q1_business）｜Transaction revenue＝590.2 USD M（QoQ -1%，YoY -44%）｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：SEC 8-K Q3 2026 earnings deck https://www.sec.gov/Archives/edgar/data/0001679788/000167978826000121/q326earningsdeck_vsec.htm（IR 新聞稿 investor.coinbase.com 未直接取得）（numbers.latest_quarter_kpis.items[8]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-29））
  - 註記：無共識數據（未查）
- `f_kpi10_guidance_q4_2026`（q1_business）｜Guidance Q4 2026＝550-630 subscription & services rev 550–630M；Adjusted Expenses 1,007–1,157M；SBC 約240M；Q4 transaction rev QTD至10-25約165M（公司提醒勿外推）｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：SEC 8-K Q3 2026 earnings deck https://www.sec.gov/Archives/edgar/data/0001679788/000167978826000121/q326earningsdeck_vsec.htm（IR 新聞稿 investor.coinbase.com 未直接取得）（numbers.latest_quarter_kpis.items[10]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-29））
  - 註記：無共識數據（未查）
- `f_peer_coin_gross_margin_pct`（q2_moat）｜COIN 毛利率＝71.01 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.COIN.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_coin_operating_margin_pct`（q2_moat）｜COIN 營業利益率＝5.68 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.COIN.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_hood_operating_margin_pct`（q2_moat）｜HOOD 營業利益率＝45.65 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.HOOD.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_ibkr_operating_margin_pct`（q2_moat）｜IBKR 營業利益率＝86.25 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.IBKR.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_cme_operating_margin_pct`（q2_moat）｜CME 營業利益率＝65.66 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CME.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_hood_gross_margin_pct`（q2_moat）｜HOOD 毛利率＝81.44 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.HOOD.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_ibkr_gross_margin_pct`（q2_moat）｜IBKR 毛利率＝89.97 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.IBKR.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_cme_gross_margin_pct`（q2_moat）｜CME 毛利率＝86.63 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CME.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_coin_fcf_margin_pct`（q2_moat）｜COIN FCF 利潤率＝68.4 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.COIN.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_hood_fcf_margin_pct`（q2_moat）｜HOOD FCF 利潤率＝58.44 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.HOOD.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_ibkr_fcf_margin_pct`（q2_moat）｜IBKR FCF 利潤率＝135.66 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.IBKR.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_schw_fcf_margin_pct`（q2_moat）｜SCHW FCF 利潤率＝52.27 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.SCHW.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_cme_fcf_margin_pct`（q2_moat）｜CME FCF 利潤率＝62.15 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CME.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝-1.69 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-10-31）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝3.02 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-10-31）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝4.83 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-10-31）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝5235.02 USD m｜期間與口徑：2026-11-03／yfinance revenue_estimate 0y 平均（32 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝6654.33 USD m｜期間與口徑：2026-11-03／yfinance revenue_estimate +1y 平均（32 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi9_assets_on_platform`（q1_business）｜Assets on platform＝377 USD B（QoQ +53%）｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：SEC 8-K Q3 2026 earnings deck https://www.sec.gov/Archives/edgar/data/0001679788/000167978826000121/q326earningsdeck_vsec.htm（IR 新聞稿 investor.coinbase.com 未直接取得）（numbers.latest_quarter_kpis.items[9]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-29））
  - 註記：無共識數據（未查）
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝-1935.19 USD m｜期間與口徑：2026-11-03／yfinance 最新一季：總債務 6885.69、現金 8820.88（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝264.76 m shares｜期間與口徑：2026-11-03／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_ev_m`（q5_valuation）｜目前企業價值 EV（市值＋淨負債）＝35227.0 USD m｜期間與口徑：2026-11-03／市值 37162.19 ＋ 淨負債 -1935.19｜kind：realized
  - 來源：—（numbers.capital_structure.ev_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝140.39 USD｜期間與口徑：2026-11-02（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ev_s_fwd`（q5_valuation）｜EV/S（EV ÷ FY1 共識營收）＝6.73 x｜期間與口徑：2026-11-03／f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）｜kind：estimate
  - 來源：—（numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝6.47 x｜期間與口徑：2026-11-02（RTH 收盤，UTC）／4 個年度端點內的分位＝45.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝45.0 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝6.83 x｜期間與口徑：2026-11-02（RTH 收盤，UTC）／4 個年度端點內的分位＝43.9｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝43.9 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-11-02（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝128.79 x｜期間與口徑：2026-07-16／分母＝FY1 EPS 1.22，分子＝快照價 157.12｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-07-16）
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝-30.78 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-11-02（RTH 收盤，UTC））
- `f_rsi14`（q5_valuation）｜RSI(14)＝30.69｜期間與口徑：2026-11-02（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-11-02（RTH 收盤，UTC））
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝238.0 %｜期間與口徑：2026-07-30 → 2026-10-31／FY1 共識 EPS -0.5 → -1.69（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-10-31）
- `f_ma_state`（q5_valuation）｜週線均線六態（decision_inputs.ma 必須等於此值）＝❌｜期間與口徑：2026-11-03／timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）
  - 原文：「price 140.14 / W52 190.25 / W104 237.62 / W250 170.29 / W250 13週斜率 -0.67%」
- `f_ma_w52`（q5_valuation）｜52 週均線＝190.25 USD｜期間與口徑：2026-11-03／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）
- `f_ma_w250`（q5_valuation）｜250 週均線＝170.29 USD｜期間與口徑：2026-11-03／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）

### findings_digest 中方向為負或來源衝突的條目（20 條）
- `competitive_share_entrants#0`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K FY2025 列出競爭類別含傳統券商/fintech、加密原生、機構點狀方案、DEX、非USDC穩定幣；因新增股票與預測市場，競爭集合擴大，並預期美國監管明朗後來自美國公司的競爭增加。
  - 來源：SEC EDGAR 10-K FY2025 Item 1 Business（as_of 2026-02-12）｜affects：moat_trend、thesis.R
- `competitive_share_entrants#1`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K 風險因子：DEX 交易量多次媲美自家平台，預期競爭加劇。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-12）｜affects：moat_trend、decision_inputs.bear
- `competitive_share_entrants#2`（competitive_share_entrants｜方向 -｜狀態 ok）：TokenInsight資料：Binance Q2 2026總市佔由32.77%升至35.34%，為最大增幅。
  - 來源：Landbase blog（as_of 2024-05-01）｜affects：moat_trend
- `supply_demand_durability#1`（supply_demand_durability｜方向 -｜狀態 ok）：William Blair cut estimates; expects Coinbase total trading volume to fall ~44% in 2026 to $669B, then rebound >32% in 2027; earnings trough 2H26 and recover 2027.
  - 來源：Crypto Briefing: William Blair sees Coinbase and Circle benefiting from crypto recovery despite slashing estimates（as_of 2026-09-22）｜affects：valuation、decision_inputs.bear
- `supply_demand_durability#2`（supply_demand_durability｜方向 -｜狀態 ok）：Analysts cut Coinbase 2026/2027 estimates; Barclays Underweight expects forecasts to fall unless trading rebounds; Moderate Buy consensus.
  - 來源：BrokerChooser: Analysts See Opportunity in Coinbase's Slide, Despite Slashed Forecasts（as_of 2026-05-15）｜affects：valuation、decision_inputs.bear
- `regulatory_antitrust#0`（regulatory_antitrust｜方向 -｜狀態 ok）：FY2025 10-K 揭露：Coinbase 已收到多個州機關與檢察長、各監管機構的調查傳票與要求函，涉及上架流程、資產分類、質押計畫、穩定幣與收益產品；公司表示將配合。
  - 來源：SEC EDGAR 10-K FY2025 Item 3 Legal Proceedings（as_of 2026-02-12）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#1`（reg_tariff_export｜方向 -｜狀態 ok）：10-K FY2025 風險因子指出，隨國際擴張，公司可能面臨涉及制裁、出口管制與反洗錢的調查或執法。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A Risk Factors（as_of 2026-02-12）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：2026-05-07 AWS US-EAST-1 資料中心過熱導致 Coinbase 交易中斷逾兩小時；主交易系統為降延遲跑在單一可用區，備援未如預期運作；為約七個月內第二次 AWS 相關中斷（前次 2025-10）
  - 來源：paymentexpert.com / thenextweb.com 報導（搜尋摘要）（as_of 2026-05-11）｜affects：decision_inputs.bear、thesis.R
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：FY2025 10-K 揭露依賴第三方支付、金融機構及雲端運算與資料中心服務，且不直接營運這些供應商設施，面臨停電、人為錯誤、天災等中斷風險
  - 來源：Coinbase FY2025 Form 10-K（as_of 2026-02-01）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#2`（geo_supply_chain｜方向 -｜狀態 ok）：Coinbase 2026-05 AWS 中斷，主系統單一可用區
  - 來源：The Next Web（as_of 2026-05-08）｜affects：thesis.R
- `end_markets#0`（end_markets｜方向 -｜狀態 ok）：Q3 2026 交易營收 $590.2M，年減 44%，機構現貨成交量年減 53%
  - 來源：Coinbase 10-Q (period 2026-09-30)（as_of 2026-10-29）｜affects：thesis.R、valuation
- `end_markets#3`（end_markets｜方向 -｜狀態 ok）：William Blair 預估 Coinbase 平台 2026 成交量年減約 44% 至 $669B，2027 反彈逾 32%
  - 來源：CryptoBriefing: William Blair sees Coinbase and Circle benefiting from crypto recovery（as_of 2026-06-30）｜affects：valuation、thesis.R
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：Coinbase 10-K FY2025 risk factors say new services/technologies (decentralized networks, generative AI) may be superior to or render obsolete its current products and may fundamentally alter use of its services in unpredictable ways.
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-12）｜affects：moat_trend、thesis.R
- `substitute_technology#1`（substitute_technology｜方向 -｜狀態 ok）：Artemis data cited in early Feb 2026: on-chain perp exchange Hyperliquid processed ~$2.6T notional volume in 2025 vs ~$1.4T for Coinbase.
  - 來源：Whale Alert, Hyperliquid processes $2.6T in 2025 notional volume—surpasses Coinbase（as_of 2026-02-10）｜affects：moat_trend、thesis.R、decision_inputs.bear
- `capital_markets_pricing#0`（capital_markets_pricing｜方向 -｜狀態 ok）：TIKR：共識目標價約 $212，較一年前約 $380 下修，8 月低點 $195
  - 來源：TIKR Coinbase Stock at $158 Against a $309 Target（as_of 2026-10-08）｜affects：valuation、decision_inputs.bear
- `capital_markets_pricing#2`（capital_markets_pricing｜方向 -｜狀態 ok）：Zacks：Q2 後 FY2026 共識 EPS 大幅下修至約 -$0.05
  - 來源：Nasdaq/Zacks Bear of the Day: Coinbase Global（as_of 2026-08-15）｜affects：valuation、decision_inputs.bear
- `major_events#0`（major_events｜方向 -｜狀態 ok）：2026-05-05 8-K Item 2.05：宣布重組，裁員約 700 人（約 14%），預估重組費用 $50–60 百萬，多數於 2026Q2 認列。
  - 來源：SEC EDGAR 8-K Item 2.05 (2026-05-05)（as_of 2026-05-05）｜affects：thesis.R、decision_inputs.bear
- `major_events#2`（major_events｜方向 -｜狀態 ok）：FY2025 10-K：公司收到多個州機關與監管機關的調查傳票與要求函，涉及上架流程、質押、穩定幣與收益產品；管理層認為無其他重大不利訴訟。
  - 來源：SEC EDGAR 10-K FY2025 Item 3（as_of 2026-02-12）｜affects：thesis.R、decision_inputs.bear
- `lawsuit_class_action#0`（lawsuit_class_action｜方向 -｜狀態 ok）：FY2025 10-K 披露 Underwood 等集體訴訟等重大訴訟（Note 21）；公司稱曾、現正面臨集體訴訟，結果無法確定。另搜尋顯示 D.N.J. 證券集體訴訟（2021 直接上市相關，AP7 為首席原告）法院駁回第三次駁回動議，裁定日期未見。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A / Note 21；Kessler Topaz 案件頁（as_of 2026-02-12）｜affects：thesis.R、decision_inputs.bear
- `sec_investigation_restatement#0`（sec_investigation_restatement｜方向 -｜狀態 ok）：FY2025 10-K 披露收到多個州與聯邦監管機關調查傳票；未見重編財報（8-K 清單無 Item 4.02）。2025-05 另有 SEC 調查過往用戶數揭露（早於12個月窗口）。
  - 來源：SEC EDGAR 10-K FY2025 Item 3（as_of 2026-02-12）｜affects：thesis.R、decision_inputs.bear

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 4 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/COIN_20261103/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":341.1,"bear_5y_price":48.7,"p_bull_pct":20,"p_bear_pct":30,"upside_5y_pct":22.8,"ev5y_pct":20.4,"irr_base_pct":4.2,"asym_ratio":1.5,"scenario_tree":{"terminal_label":"FY2031E","valuation_basis":"sales_multiple","start":{"rev":5235.02,"ev_s":6.73,"basis":"起點營收取 FY2026 共識（2026年度，32位分析師平均），EV/S＝目前 EV÷FY2026 營收；終端 EV/S 以 FY2031 當年營收為分母，同為當年度口徑"},"rev":{"bull":[7600,9400,10500,11500,12500],"base":[6400,7200,7800,8400,9000],"bear":[4600,4400,4700,5000,5200]},"ev_s":{"bull":7.0,"base":5.0,"bear":3.0},"net_debt_y5":{"bull":-8000,"base":-5000,"bear":1000},"shares_y5":{"bull":280,"base":290,"bear":300},"net_debt_now":-1935.19,"shares_now":264.76,"p":{"bull":20,"base":50,"bear":30},"yield_pct":{"dividend":0,"net_buyback":0},"second_stage":null,"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### COIN_Q2_2026_Earnings_Call_20260730.md
- 2026-07-30｜Brian Armstrong｜risk：CEO 表示若 CLARITY 法案未過，對 Coinbase 而言大致照常營運，受損的是美國消費者（原話："I think Coinbase would be fine."）
- 2026-07-30｜Brian Armstrong｜risk：CEO 稱法案通過仍較佳，因其提供跨政府任期的持久性（原話："So we still think on margin, it's better if the CLARITY Act passes."）
- 2026-07-30｜Alesia Haas｜competition：CFO 稱與 Circle 的合約續約條件已達成，將以相同條款續約（原話："we have already met the conditions for the Circle contract to renew"）
- 2026-07-30｜Brian Armstrong｜competition：CEO 說明加入 Open USD 的理由是多穩定幣平台定位（原話："the short reason is that we're a multi-stablecoin platform."）
- 2026-07-30｜Brian Armstrong｜risk：CEO 被問及多位高階主管離職，稱策略沒有改變（原話："There's nothing that's changing about the strategy."）
- 2026-07-30｜Alesia Haas｜risk：CFO 稱高階主管異動皆為個別決定（原話："these were all individual decisions."）
- 2026-07-30｜Brian Armstrong｜customer：CEO 回應 AI agent 無品牌忠誠度的問題，稱信任在 agent 時代仍重要（原話："I think trust will continue to be important in that world."）
- 2026-07-30｜Brian Armstrong｜product：CEO 引述 Base 的費用與結算速度作為對 agent 的價格競爭力（原話："actually delivers like sub $0.01 and sub 1-second settlement."）
- 2026-07-30｜Alesia Haas｜margin：CFO 說明成長行銷回收期的基準與近期表現（原話："seeing a 1-year payback on growth marketing efforts, but recently, we've outperformed this benchmark."）
- 2026-07-30｜Alesia Haas｜product：CFO 稱新產品（如預測市場）早期訊號顯示帶動額外現貨交易量而非互相蠶食（原話："These early days are actually indicating that we're seeing incremental trading coming"）
- 2026-07-30｜Brian Armstrong｜customer：CEO 說明以資產存放量階層誘因（Coinbase One Card 回饋率）鼓勵客戶存放更多資產（原話："you can get a higher rate on Coinbase One Card, the more that"）
- 2026-07-30｜Alesia Haas｜customer：CFO 稱本季付費 Coinbase One 訂閱戶創歷史新高，且發生在交易量下滑的市場（原話："we saw an all-time high in paid"）
- 2026-07-30｜Brian Armstrong｜product：CEO 談比特幣相關交易占比下降，並稱比特幣會回來（原話："And I think Bitcoin will come back in a big way, too, by the way."）
- 2026-07-30｜Brian Armstrong｜guidance：CEO 表示 agentic finance 目前不提供具體數字或預測（原話："have any specific numbers or forecast to share on that at the moment."）
- 2026-07-30｜Brian Armstrong｜commitment：CEO 稱預先 IPO 永續合約開放美國客戶在路線圖上，將持續推動（原話："In terms of U.S. access, that is on the road map, and we'll keep pushing on that."）
- 2026-07-30｜Brian Armstrong｜competition：CEO 預期 Robinhood、Stripe 等自建區塊鏈後，區塊鏈也會出現類似穩定幣的整併（原話："So my guess is we're going to see something similar happen with blockchains."）
- 2026-07-30｜Brian Armstrong｜commitment：CEO 承諾持續投資 Base 並開放給所有人建置（原話："to continue to invest in Base. We're going to make sure everyone can build on top of it."）
- 2026-07-30｜Alesia Haas｜capital_allocation：CFO 對 Hyperliquid 合作表示願意分享 USDC 經濟利益以推動網路效應（原話："we're happy to share economics to drive this network effect."）
- 2026-07-30｜Brian Armstrong｜commitment：CEO 承諾持續投資 USDC 成長（原話："we're going to keep investing in USDC to keep growing it."）
- 2026-07-30｜Alesia Haas｜margin：CFO 被問 Coinbase One 單位交易收益是否壓縮，稱整體淨單位經濟為正，但收入會在損益表間轉移（原話："So I think overall, this will be more net unit economic positive to us."）
- 2026-07-30｜Alesia Haas｜margin：CFO 稱若會員普及，收入將在損益表各項目間轉移（原話："But you will see the revenue shift through the P&L if we"）

### 問答異常語氣（迴避／改口／保留）
- COIN_Q2_2026_Earnings_Call_20260730.md｜問：Coinbase One 會員每交易一美元的營收是高於或低於非會員（增益或 take rate 壓縮）｜答法：CFO 自稱給「不令人滿意的答案」，未給出每單位營收數字，只稱平均單位經濟較高、邊緣有例外
- COIN_Q2_2026_Earnings_Call_20260730.md｜問：多位高階主管本季離職，策略為何｜答法：CEO 與 CFO 皆以人才深度與接班規劃回應，未說明離職原因，稱皆為個別決定
- COIN_Q2_2026_Earnings_Call_20260730.md｜問：Hyperliquid 合作顯示第三方持有足夠 USDC 即可取得多數 USDC 經濟利益，如何保護長期經濟利益｜答法：CFO 與 CEO 談網路效應與願意分享經濟利益，未回應如何保護長期經濟利益或給出分潤比例
- COIN_Q2_2026_Earnings_Call_20260730.md｜問：agentic commerce 的營收規模與規劃｜答法：CEO 稱仍很早期，不提供具體數字或預測

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 4 | 2 |
| customer_second_source | not_applicable | 0 | 0 |
| customer_concentration_credit | not_applicable | 0 | 0 |
| supply_demand_durability | found | 4 | 2 |
| regulatory_antitrust | found | 3 | 1 |
| reg_tariff_export | found | 2 | 1 |
| geo_supply_chain | found | 3 | 2 |
| end_markets | found | 4 | 3 |
| substitute_technology | found | 2 | 1 |
| channel_business_model_shift | found | 3 | 2 |
| capital_markets_pricing | found | 4 | 2 |
| major_events | found | 3 | 5 |
| financial_capital_credit_cycle | found | 2 | 3 |
| financial_regulatory_capital_rules | found | 2 | 2 |

未涵蓋／不適用軸的查詢詞原文（供判相關性）：
- **customer_second_source**（not_applicable）：（無查詢記錄）
- **customer_concentration_credit**（not_applicable）：（無查詢記錄）

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260525","verdict":"B","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"Take rate 壓縮可被 transaction volume 成長與 mix 升級（衍生品）抵銷，blended transaction revenue 維持 5-15% CAGR","columns":{"2Y 驗證點":"FY26-27 transaction revenue YoY 從 -25% 回升至 ≥ +10%（FY27）","5Y 驗證點":"FY28-30 transaction revenue 累計成長 ≥ 60%（Deribit 整合 + cycle peak）","10Y 驗證點":"FY35 transaction revenue $5B+（vs FY25 ~$3.5B）","具體數字門檻":"2Y：FY27 transaction rev ≥ $3.8B（Q1 26 是 $755.8M，年化 ≥ $3.0B 為下限）；5Y：accumulated transaction rev FY28-30 ≥ $13B","信息來源":"Q1 2026 8-K + FY24 10-K + Deribit 整合披露","漂移觸發條件":"連 2 季 TTM transaction rev YoY 偏離 -10%（相對 baseline）→ 削弱；連 4 季 → 反轉"}},{"id":"H2","text":"USDC + Base + Subscription 形成「平台基礎設施第二曲線」，subscription revenue 維持 25%+ CAGR 並在 FY28 占比 ≥ 45%","columns":{"2Y 驗證點":"FY26 subscription revenue YoY ≥ +5%（Q1 26 已 $583.5M，年化 ~$2.4B）","5Y 驗證點":"FY28 subscription revenue ≥ $3.5B（含 USDC 50%+ + Base sequencer + Coinbase One + staking）","10Y 驗證點":"FY30 subscription revenue ≥ $5B","具體數字門檻":"2Y：FY27 subscription rev ≥ $2.6B；USDC on-platform AUM ≥ $30B；5Y：subscription / total revenue ratio ≥ 45%","信息來源":"Q1 2026 8-K 揭露 $305M stablecoin rev + Q4 2025 $19M Base sequencer rev + Coinbase 法說會","漂移觸發條件":"連 2 季 USDC AUM YoY 偏離 -15%（vs +35% baseline）→ 削弱；連 4 季 → 反轉"}},{"id":"H3","text":"監管環境（GENIUS Act 規則化 + SEC 訴訟和解）走向「Coinbase 規範性護城河強化」而非「intermediary loyalty rewards 被禁」","columns":{"2Y 驗證點":"FY26-27 Treasury 對 GENIUS Act 的 implementation guidance 不擴大解釋「intermediary」","5Y 驗證點":"FY28-30 SEC 訴訟和解，Coinbase 在 staking / DeFi 等業務獲明確 safe harbor","10Y 驗證點":"FY30+ US 成為全球 crypto 監管 gold standard，Coinbase 為主要規範性 fiat-crypto 介面","具體數字門檻":"2Y：Treasury Final Rule 不擴大解釋 intermediary loyalty rewards 為 stablecoin issuer 行為；5Y：SEC 訴訟和解或勝訴；無新 enforcement action 重大事件","信息來源":"Coinbase 2025-11 Treasury ANPRM 回應 + GENIUS Act 法條原文","漂移觸發條件":"單一監管事件即足以削弱（不需連續）：Treasury 廣義解釋 OR 新 SEC charges → 反轉"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"BTC 進入新一輪結構性熊市（cycle 30-50% drawdown），平台交易量崩盤","columns":{"對應假設":"H1","時間尺度":"⚡ 短期（1-2 季可觸發）","監測指標":"Spot trading volume YoY；BTC price 6 個月 drawdown","警戒閾值":"連 2 季 spot volume YoY -30%+ AND BTC drawdown -40% → 減倉 1/3"}},{"id":"R2","text":"GENIUS Act Treasury Final Rule 廣義禁止 intermediary loyalty rewards，USDC 收益分潤模式被擊穿","columns":{"對應假設":"H3","時間尺度":"🔥 中期（4-6 季）","監測指標":"Treasury rule draft 公告；Coinbase 法律部對外發言調性","警戒閾值":"Final Rule 廣義解釋 → 立即 reduce thesis confidence + thesis 重估"}},{"id":"R3","text":"DEX 主流化（Hyperliquid + Uniswap）+ HOOD 零佣 + Binance.US restructure 三面夾擊，blended take rate 加速壓縮","columns":{"對應假設":"H1","時間尺度":"🐢 長期（2+ 年慢變數）","監測指標":"Blended transaction take rate（季度）；CEX 整體 spot market share；DEX 占 spot 比例","警戒閾值":"連 4 季 blended take rate YoY -10%+ AND CEX spot 比例下降 → 護城河重估，可能砍倉"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🟡","ma":"🟠","trap":"🟡","moat_trend":null,"runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":184.99,"archetype":null,"cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"COIN","date":"2026-11-03","schema":"v15.0","contract":"v19","company_name":"Coinbase Global, Inc."},"oneliner":"加密交易量谷底疊加費率被DEX與多資產券商侵蝕；訂閱與服務營收撐住一半，但營業利益率僅5%、SBC占營收19%，現價已預支循環回升，基本情境五年年化約4%，不追。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/COIN_20261103/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/COIN_20261103/scenario.json","answers":{"q1_business":{"verdict":"Coinbase 賺兩筆錢：一是向散戶與機構抽交易手續費（Q3 5.9億美元，年減44%），二是替 Circle 分銷 USDC 換取準備金利息分潤，加上質押與會員費（Q3 5.7億美元，年減20%）。錢卡在美國合規入金口與託管這一節點，但交易費這段正被 DEX、多資產券商與美國新進者分食，谷底期營業利益率只剩5.1%。","reasoning":"收入分兩塊：Q3 2026 總營收12.156億美元（年減35%、季減0.4%），其中交易營收5.902億（年減44%、季減1%）、訂閱與服務5.702億（年減20%、季增3%），兩者幾乎各半，其餘約0.55億為其他營收（總營收減兩塊相減推得）。交易營收按成交額抽成，量隨加密幣價循環；衍生品與預測市場合占交易營收約25%（Q3 法說2026-10-29 Alesia Haas）。訂閱與服務以 USDC 準備金利息分潤為主（管理層稱拿約50%經濟利益、平台持有約30%流通量），另有質押、Coinbase One 與 Base 排序費。獲利面：Q3 GAAP 營業利益0.617億、營業利益率5.1%，SBC 2.33億是營業利益的3.8倍；GAAP 淨利7.187億幾乎全來自持有加密資產評價（約7.15億，第三方數字未驗證），不代表本業。TTM 毛利率71.0%、營業利益率5.7%；單季毛利率事實表未涵蓋。單點依賴有二：USDC 分潤協議（Q2 法說2026-07-30 CFO 稱已達續約條件、相同條款）與 AWS 單一可用區（2026-05 中斷逾兩小時，七個月內第二次）。產業時鐘判為IV收縮：William Blair 預估2026平台成交量年減約44%、2027反彈逾32%；Q3 現貨量季減10%；第四季至10-25 交易營收約1.65億美元（公司提醒勿外推），量能尚未回升。供需持久性：週期性將反轉，但供給可逆性高，DEX 與多資產券商能快速擴充交易場所，回升時費率不一定跟著回來。產業態勢雙向拉鋸：競爭惡化（10-K 自承競爭集合擴大，並預期美國監管明朗後新進者增加）對上法規轉好（GENIUS Act 已成法、SEC 與 CFTC 合作，CFTC 為 Coinbase 相關爭議起訴紐約州）。","fact_refs":["f_kpi0_total_revenue_gaap","f_kpi1_net_revenue","f_kpi2_gaap_operating_income","f_kpi3_gaap_operating_margin","f_kpi4_net_income_gaap","f_kpi6_stock_based_compensation","f_kpi7_subscription_services_re","f_kpi8_transaction_revenue","f_kpi10_guidance_q4_2026","f_peer_coin_gross_margin_pct","f_peer_coin_operating_margin_pct"],"verdict_values":{"revenue_quality":"約一半為交易手續費，高度循環且費率受壓；一半為訂閱與服務，主體是 USDC 準備金利息分潤，對 USDC 流通量與分潤條款敏感，利率敏感度事實表未涵蓋。GAAP 淨利由持有加密資產評價主導，Q3 約7.15億美元評價利益對營業利益0.617億，本業獲利薄。","unit_econ_note":"Q3 GAAP 營業利益率5.1%，SBC 2.33億美元為營業利益的3.8倍、占營收19.2%；TTM 營業利益率5.7%，同期 HOOD 45.7%、CME 65.7%。ARPU、活躍戶、費率等交易所單位經濟事實表未涵蓋。","archetype":{"primary":"金融","secondary":"循環/商品","confidence":"中","fingerprint":"收入＝加密成交額×費率＋USDC 準備金分潤；營收隨幣價循環大幅擺動（FY2024 年增111%、2026 Q3 年減35%）"},"industry":{"clock_phase":"IV","sd_verdict_source":"週期性將反轉、供給可逆性高：William Blair 估2026平台成交量年減約44%、2027反彈逾32%；交易場所供給可由 DEX 與券商快速擴充，回升時費率不保證回來。","bargaining":{"up":"上游為雲端（AWS）、銀行與支付通路、USDC 發行商 Circle；Circle 同時是夥伴，也在支付基礎設施上與 Coinbase 競爭，分潤條款是最大的上游議價點。","down":"散戶可同時開多家帳戶，DEX 只需自有錢包，轉換成本低；機構看費率與流動性，衍生品面對 CME 等受監管場所競爭。","geo":"美國以外主要對手為 Binance（第三方資料稱 Q2 2026 總市占35.3%）；國際擴張帶來制裁、出口管制與反洗錢執法風險。"},"profit_pool_dir":"交易手續費利潤池由中心化現貨交易所流向衍生品、鏈上永續與多資產券商；穩定幣利潤池擴大，但在發行商與分銷夥伴之間重新切分。","tam_table":{"expanded":false,"reason":"TAM、滲透率與利潤池占比事實表未涵蓋；本次論點承重在交易量循環與穩定幣分潤，新品類滲透不承重，故不展開。Q3 法說 Armstrong 稱金融科技合計僅占金融服務營收5–10%，屬口頭估計，無法核實。"}}}},"q2_moat":{"verdict":"護城河趨勢向下、評級C：託管規模與 USDC 分潤仍是真優勢，但零售交易費的定價力在縮減。10-K 自承競爭集合擴大，鏈上永續成交量已超過自家平台，TTM 營業利益率5.7% 對 HOOD 45.7%。","reasoning":"機制：美國合規入金口與最大加密託管人地位，加上 USDC 分潤協議，以及零售、機構、開發者三類客戶共用一套平台的攤提效益。方向證據：同業 ROIC 與投入資本事實表未涵蓋，以營業利益率差距代替；COIN TTM 5.7%，HOOD 45.7%、CME 65.7%、IBKR 86.3%，差距為負且大。COIN 自身 FY2024 34.1%、FY2025 20.3%，同期同業序列事實表未涵蓋，無法判斷差距是否擴大。執行力7分：預測市場2月上線，Q3 年化營收破2億美元；Deribit 整合成全球統一衍生品交易所；代幣化股票上線後成交30億美元。扣分在七個月兩次 AWS 相關中斷、Q2 多位高階主管離職（管理層只答是個別決定）與裁員14%。定價力5分：零售交易費面對 HOOD 與 DEX；Coinbase One 會員讓收入在損益表項目間移動，CFO 拒答會員每交易美元營收；USDC 分潤方面，管理層表態願與夥伴分享經濟利益。趨勢判讀：執行穩定、定價力縮減，合併為向下。反例：公司自報 Q2 加密成交量市占創紀錄10.3%，Q2 付費 Coinbase One 會員創新高；但市占分母與涵蓋範圍未揭露，不足以推翻第三方數據與10-K 自身揭露的方向。報酬持續期：當期落在低利益率象限，投入資本、增量報酬與再投資率皆缺，內生天花板無法計算。","fact_refs":["f_peer_coin_operating_margin_pct","f_peer_hood_operating_margin_pct","f_peer_ibkr_operating_margin_pct","f_peer_cme_operating_margin_pct","f_peer_coin_gross_margin_pct","f_peer_hood_gross_margin_pct","f_peer_ibkr_gross_margin_pct","f_peer_cme_gross_margin_pct","f_peer_coin_fcf_margin_pct","f_peer_hood_fcf_margin_pct","f_peer_ibkr_fcf_margin_pct","f_peer_schw_fcf_margin_pct","f_peer_cme_fcf_margin_pct"],"verdict_values":{"moat":{"mechanism":"美國合規入金口與最大加密託管人地位＋USDC 分潤協議＋零售、機構、開發者三類客戶共用平台的攤提效益","execution":7,"pricing":5,"grade":"C","trend":"↓","trend_evidence":"定價力縮減、執行穩定：10-K 自承競爭集合擴大，並預期美國監管明朗後新進者增加；DEX 成交量多次媲美自家平台；Artemis 資料顯示 Hyperliquid 2025 名目成交約2.6兆美元，高於 Coinbase 約1.4兆；管理層對第三方分走 USDC 經濟利益只答願意分享；TTM 營業利益率5.7% 對 HOOD 45.7%。反例是公司自報市占創紀錄，但分母未揭露。","competitor_notes":[{"name":"HOOD","strategy_note":"多資產零售券商加做加密、預測市場，是 Everything Exchange 的正面對手；TTM 營業利益率45.7%，成本結構遠優於 COIN。"},{"name":"IBKR","strategy_note":"低費率全球券商，營業利益率86.3%；若擴大加密現貨將以費率壓價，其加密成交規模事實表未涵蓋。"},{"name":"SCHW","strategy_note":"傳統券商，監管明朗後可能開放加密現貨，威脅在大客戶資產不必再移到加密專門平台；利潤率資料事實表不全。"},{"name":"CME","strategy_note":"受監管加密期貨主場，與 Coinbase 衍生品（含 Deribit）爭機構客戶；營業利益率65.7%。"},{"name":"Hyperliquid","strategy_note":"鏈上永續合約，2025 名目成交約2.6兆美元超過 Coinbase，直接繞過託管與帳戶，是架構層面的替代。"},{"name":"Binance","strategy_note":"全球最大中心化交易所，第三方資料稱 Q2 2026 總市占升至35.3%，主要威脅在美國以外市場。"},{"name":"Circle","strategy_note":"USDC 發行夥伴，同時自建穩定幣支付基礎設施，屬競合關係；分潤條款決定 COIN 訂閱與服務營收的最大一塊。"}],"peer_na_reason":"同業 ROIC 與投入資本事實表未涵蓋，以 TTM 營業利益率差距代替 ROIC 差距；同業 EV/S 與本益比亦未涵蓋。","threats":[{"level":"🔴","text":"DEX 與鏈上永續（Hyperliquid）分走衍生品與現貨成交；Coinbase 經 Base 與 DEX 整合部分接住流量，故列生態攻擊而非完全架構替代","p":"40%","evidence_refs":["competitive_share_entrants#1","substitute_technology#0","substitute_technology#1"]},{"level":"🟡","text":"多資產券商（HOOD）與監管明朗後的美國新進者以多資產帳戶與低費率爭零售交易","p":"50%","evidence_refs":["competitive_share_entrants#0"]},{"level":"🟡","text":"Binance 全球份額上升；來源為部落格轉述 TokenInsight，標注日期與內容年份不一致，權重降低","p":"30%","evidence_refs":["competitive_share_entrants#2"]},{"level":"🟡","text":"USDC 經濟利益被分銷夥伴與 Circle 自建通路分食；Q2 法說管理層未答如何保護長期分潤","p":"35%","evidence_refs":[]}],"roic_durability":{"quadrant":"低利益率象限（谷底期）：TTM 營業利益率5.7%，投入資本周轉率事實表未涵蓋","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者、決策者、付款者多為同一交易者；交易需求屬想要而非需要，隨幣價大幅擺動（Q3 交易營收年減44%、機構現貨年減53%）；穩定幣支付與託管的需求較剛性。"},{"item":"決策層級","level":"🔴","text":"替代在單筆交易層級發生，轉換成本低：散戶可多開帳戶，DEX 只需自有錢包；10-K 承認 DEX 成交量多次媲美自家平台。漲價後流失率等代理變數事實表未涵蓋。"},{"item":"價值鏈分配","level":"🟡","text":"穩定幣價值鏈中 Circle 發行、Coinbase 分銷，拿約50%經濟利益；但 Q2 法說對第三方持有 USDC 即可取得分潤的問題未正面回答，分配有向分銷夥伴傾斜的跡象。交易價值鏈則被 DEX 與做市商分食。"},{"item":"社會容忍度","level":"🟡","text":"高度依賴監管授權（州牌照、紐約州金融服務署協議、GENIUS Act）；多州與聯邦機關傳票涉及上架、質押與收益產品；監管轉向友善，但穩定幣回饋仍可能被立法限制，屬政策風險。"}],"roiic":"事實表未涵蓋（投入資本口徑、Deribit 收購金額均缺）","reinvest_rate":"事實表未涵蓋（資本支出、折舊攤銷、收購淨額缺；FY2024–2025 FCF 為空值）","endo_ceiling":null,"formula_note":"內生成長率＝增量ROIC×再投資率；兩項輸入皆缺，天花板無法計算。不以 TTM FCF 利潤率68.4% 代替，因其與營業利益率5.7% 嚴重背離，疑含客戶資金或加密資產流動，未驗證。"}}}},"q3_growth":{"verdict":"成長跑道中等：未來五年的成長主要靠加密循環回升帶來的量與利潤率修復；第二曲線（預測市場、代幣化股票、代理人支付）有據可查，但目前僅占營收約4%，且對手同步進入。","reasoning":"成長來源以量（加密交易量循環）為主，價（費率）為負貢獻，新品類為增量；回購金額事實表未涵蓋。三年共識：GAAP EPS 由 FY2025A 4.45 到 FY2028E 4.83，年化約2.8%（(4.83÷4.45)^(1/3)−1），中間 FY2026E −1.69 是谷底；營收共識 FY2026 52.35億、FY2027 66.54億美元（32位分析師），FY2028 營收共識事實表未涵蓋。內生天花板無法計算（增量報酬與再投資率缺）；共識成長的來源是循環回升帶動的利潤率擴張，不是再投資，而且 EPS 含加密資產評價，基期本身有爭議。跑道判中等：第二曲線有據可查（預測市場年化2億美元，Cantor 估2028年最多可占毛利三成；代幣化股票上線後成交30億美元；代理人交易量週增約20%但規模仍小），但目前僅占營收約4%（2億÷52.35億），HOOD 等對手同步進入；滲透率資料事實表未涵蓋，年數無法推算。衰退信號二項亮燈、二項待證，見衰退信號清單。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_kpi7_subscription_services_re","f_kpi8_transaction_revenue","f_kpi10_guidance_q4_2026","f_kpi6_stock_based_compensation"],"verdict_values":{"growth":{"driver_mix":"量（加密交易量循環）為主；價（費率）為負貢獻；新品類（預測市場、衍生品、代幣化股票）為增量；併購（Deribit）已併入；回購無資料","runway_years":"事實表未涵蓋滲透率，無法推算","runway_post_y5":"🟡","endo_ceiling_basis":"引護城河段：增量ROIC與再投資率皆缺，天花板無法計算；共識三年EPS年化約2.8%，幾乎全來自循環回升的利潤率擴張，而非再投資","segments":[{"item":"交易營收","value":"Q3 5.902億美元（年減44%、季減1%）；衍生品＋預測市場約占25%"},{"item":"訂閱與服務營收","value":"Q3 5.702億美元（年減20%、季增3%），約占淨營收49%；Q4 指引5.5–6.3億"},{"item":"預測市場","value":"2026年2月上線，Q3 年化營收破2億美元"},{"item":"其他營收","value":"約0.55億美元（12.156億−5.902億−5.702億推得）"}],"decay_signals":["SBC 占營收逾5%且上升：Q3 19.2%，Q4 SBC 指引約2.4億美元高於Q3，同期營收年減——亮燈","替代技術壓縮：Hyperliquid 2025 名目成交約2.6兆美元高於 Coinbase 約1.4兆，10-K 自承 DEX 成交量多次媲美——亮燈","毛利率下滑：TTM 71.0% 低於 FY2025 的74.6%，單季連續序列事實表未涵蓋——待證","核心市占縮減：公司自報上升、第三方顯示對手擴張，方向分歧——待證","FCF／淨利：FY2024–2025 FCF 為空值，TTM FCF 利潤率68.4% 與營業利益率背離，無法判讀——資料缺口","提價後銷量下滑、維護性資本支出占比、停止投資新產能：不適用"],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"資本配置偏弱：SBC 吃掉營收近兩成且還在升，回購與併購報酬無資料可證；淨現金約19億美元只解決谷底期的生存，不解決每股價值稀釋。","reasoning":"現金：總債務68.86億美元、現金及短投88.21億，淨現金約19.35億，谷底期無流動性壓力；債務到期結構與利率事實表未涵蓋。FCF 轉換：TTM FCF 利潤率68.4% 遠高於營業利益率5.7%，FY2024–2025 FCF 為空值，疑含客戶資金或加密資產流動，未驗證，不作品質證據；淨利又由加密評價主導，FCF／淨利比無意義。SBC：Q3 2.33億占營收19.2%，Q4 指引約2.4億；以現市值371.6億計，年化毛稀釋約2.5%（2.33×4÷371.6），回購金額事實表未涵蓋，淨稀釋無法算。現金去向：CEO 稱持續買進比特幣至第18,000枚，部分現金換成加密資產，放大損益波動；已收購 Deribit（金額與時點事實表未涵蓋），另有 Vector、The Clearing Company 小型收購。交易所應看的 ARPU、託管資產、費率、活躍戶，除平台資產3,770億美元（季增53%，組成未拆）外皆事實表未涵蓋。","fact_refs":["f_kpi6_stock_based_compensation","f_kpi10_guidance_q4_2026","f_kpi4_net_income_gaap","f_kpi9_assets_on_platform","f_net_debt_m","f_shares_diluted_m","f_ev_m","f_peer_coin_fcf_margin_pct"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":true,"passed":null,"input":"事實表未涵蓋 Deribit 收購金額與其後營業利益貢獻；管理層稱整合良好，衍生品＋預測市場占交易營收約25%，但無法算出已實現報酬"},{"name":"buyback_yield","applicable":null,"passed":null,"input":"回購金額與均價事實表未涵蓋"},{"name":"sbc_dilution","applicable":true,"passed":false,"input":"Q3 SBC 2.33億美元，年化約9.3億，對現市值371.6億約2.5%毛稀釋；回購資料缺，無證據顯示淨稀釋≤1.5%"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購支撐；回購、股利與現金去向四分事實表未涵蓋，僅知持續買進比特幣"}}}},"q5_valuation":{"verdict":"現價要求2027–2028年加密交易量回到前高附近、營業利益率回升到20%以上，且費率不被侵蝕。前兩項我接受，第三項不信；基本情境五年年化約4%，低於8%門檻。","reasoning":"現價140.39美元、EV 352.3億美元，前瞻 EV/S 6.73倍（trailing 6.47倍，位於4個年度端點的中位附近）。GAAP EPS 不能用：FY2026 共識−1.69，FY2027 3.02（約46倍）、FY2028 4.83（約29倍），且含加密評價。現價要求的三件事中，量能回升我接受（William Blair 也估2027量反彈逾32%），利潤率回到20%以上有條件接受，費率不被侵蝕不信。情境：Bull 20%（FY2031 營收125億、EV/S 7倍，每股約341美元）、Base 50%（90億、5倍，約172美元）、Bear 30%（52億、3倍、淨負債10億，約49美元）；基本情境五年年化約4%，機率加權終值約169美元、年化約3.8%，都低於8%。賣方共識目標價約212美元，方向與本判斷相反，差在終端利潤率與倍數。","fact_refs":["f_price_at_dd","f_ev_m","f_ev_s_fwd","f_ev_s_current","f_ev_s_percentile","f_ps_current","f_ps_percentile","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_fwd_pe_latest","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_net_debt_m","f_shares_diluted_m"],"verdict_values":{"valuation":{"basis":"EV/S（前瞻，EV÷FY2026 共識營收）；GAAP EPS 受持有加密資產評價主導，本益比與PEG 不採用","tier":"加密交易所／多資產零售券商","peers":{"expanded":false,"reason":"同業 EV/S 與本益比事實表未涵蓋，只有利潤率；以營業利益率對照（HOOD 45.7%、CME 65.7%）支撐終端倍數，不做跨業倍數錨"},"fwd_pe":null,"peg":null,"percentile_5y":null,"val_light":"🟠","val_light_derivation":"前瞻 EV/S 6.73倍、trailing 6.47倍落在4個年度端點的45分位（非五年分位，五年高低點事實表未涵蓋，故五年分位留空）；分母是谷底營收、營業利益率5.7%，看似中位實則不便宜。以 FY2027 共識EPS 計本益比約46倍（140.39÷3.02）、FY2028 約29倍（140.39÷4.83）。短期上檔+8%：一年後 Base 營收64億×EV/S 6倍＋淨現金約25億，除以約270百萬股，約151.5美元；中期上檔+19%：三年後78億×5.5倍＋淨現金約38億，除以約280百萬股，約166.8美元。基本情境五年年化約4%，低於8%，判偏貴。","upside_short_pct":8,"upside_mid_pct":19,"denominator_disputed":true,"denominator_note":"GAAP EPS 含持有加密資產評價損益：Q3 淨利7.187億美元中約7.15億為評價利益（第三方數字未驗證），營業利益僅0.617億；FY2025A 基期與 FY2026 共識−1.69 亦受評價影響。改以營收與營業利益率估值，便宜論證不以EPS 成立。"}}},"q6_how_wrong":{"verdict":"可能看錯在三處：循環回升比預期更快更強、預測市場與衍生品成為真正的第二曲線、監管明朗讓合規龍頭吸走份額而不是降低門檻。","reasoning":"最可能看錯的三處：一是循環回升比預期快，FY2023→FY2024 營收年增111%，上一輪回升一年翻倍；二是第二曲線放大，預測市場八個月做到年化2億美元；三是監管明朗讓合規龍頭吸走份額。三者都設了推翻條件，見觸發與矛盾裁定。最大回撤：下緣−80%、上緣−60%，依據為 Bear 終點約−65%；FY2022 營業利益率−61%、淨損26.2億美元，顯示寒冬時本業可深度虧損；近一年股價已跌約56%、26週−30.8%，RSI 30.7 接近超賣但未見反轉。壓力測試五項（交易量再降30%、穩定幣分潤減半、穩定幣回饋禁令、DEX 份額倍增、重大託管事故），以年度 GAAP 營業利益仍為正為過關標準，只有回饋禁令一項可能過關（回饋支出同步消失），計1／5。法說問答有四處迴避（Q2：會員每交易美元營收、高階主管離職原因、USDC 長期經濟保護、代理人商務規模），本輪未取得答案，列為監測缺口。","fact_refs":["f_week26_return_pct","f_rsi14","f_consensus_rev_3m_fy1_pct","f_kpi8_transaction_revenue","f_kpi4_net_income_gaap","f_ma_state","f_ma_w52","f_ma_w250"],"verdict_values":{"trap":{"verdict":"🟡","label":"循環谷底疊加費率侵蝕：跌價不是安全邊際"}}}},"scenario_inputs":{"valuation_basis":"sales_multiple","terminal_label":"FY2031E","start":{"rev":5235.02,"ev_s":6.73,"basis":"起點營收取 FY2026 共識（2026年度，32位分析師平均），EV/S＝目前 EV÷FY2026 營收；終端 EV/S 以 FY2031 當年營收為分母，同為當年度口徑"},"rev":{"bull":[7600,9400,10500,11500,12500],"base":[6400,7200,7800,8400,9000],"bear":[4600,4400,4700,5000,5200]},"ev_s":{"bull":7.0,"base":5.0,"bear":3.0},"net_debt_y5":{"bull":-8000,"base":-5000,"bear":1000},"shares_y5":{"bull":280,"base":290,"bear":300},"p":{"bull":20,"base":50,"bear":30},"yield_pct":{"dividend":0,"net_buyback":0},"max_dd":{"lo":-80,"hi":-60,"basis":"下緣−80%：Bear 情境終點約49美元（較現價−65%），循環谷底常見超跌再加一段；FY2022 營業利益率−61%、淨損26.2億美元，顯示寒冬時本業可深度虧損；近一年股價已跌約56%、26週−30.8%。上緣−60%：對應回升延後一年、EV/S 壓到3–4倍的中途回撤。","trigger_time":null},"basis":{"bull":"2027–2028 加密循環強回升，衍生品、預測市場、代幣化股票與穩定幣支付成第二曲線；FY2031 營收125億美元、營業利益率約35%，終端 EV/S 7倍（約20倍 EV/EBIT），淨現金80億美元，股數年增約1%","base":"2027 交易量回升但費率續降；FY2031 營收90億美元（FY2026 起年化約11%）、營業利益率約25%，終端 EV/S 5倍（約20倍 EV/EBIT，低於現值6.73倍）；SBC 稀釋使股數增至290百萬，稀釋已反映在股數，故淨回購殖利率填0","bear":"加密寒冬延長至2028，DEX 與多資產券商壓縮費率，穩定幣回饋受限；FY2031 營收52億美元、營業利益率約10%，終端 EV/S 3倍；虧損與資產購入消耗現金，轉為淨負債10億美元，股數增至300百萬"},"endo_ceiling_exceeded":false},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"William Blair 預估2026平台成交量年減約44%、2027反彈逾32%；Q3 交易營收年減44%、機構現貨年減53%；第四季至10-25 交易營收約1.65億美元（公司提醒勿外推）；Hyperliquid 2025 名目成交已高於 Coinbase。","assumption":"基本情境假設2027年交易量回升、營業利益率回到20%以上。","consequence":"若回升延後到2028年以後，且費率同時被壓縮，營收卡在50億美元上下、營業利益率在零附近，加上 SBC 稀釋，五年後股價可能只剩40–50美元，虧損約65%。","ruling":"採納：Bear 機率定30%，最大回撤下緣設−80%。","watch":"2026Q4、2027Q1 交易營收是否回到6億美元以上","evidence_refs":["supply_demand_durability#1","end_markets#0","end_markets#3","substitute_technology#1"],"fact_refs":["f_kpi8_transaction_revenue","f_kpi10_guidance_q4_2026"]},{"view":"論點成功但股東經濟變差","evidence":"Q3 SBC 2.33億美元、占營收19.2%，Q4 指引約2.4億；2026-05 裁員約700人（14%）後 SBC 不降；CEO 稱持續買進比特幣至第18,000枚；Q2 法說 CFO 稱願與夥伴分享 USDC 經濟利益。","assumption":"營收回升時每股價值同步回升。","consequence":"營收回到中循環，但股數每年增加約1–2.5%、USDC 分潤被夥伴分食、資產負債表加密曝險放大損益波動，每股價值成長落後營收。","ruling":"採納：終端股數基本情境設290百萬股（目前264.76百萬）。","watch":"SBC 占營收、季末稀釋股數、平台 USDC 占流通量","evidence_refs":["major_events#0"],"fact_refs":["f_kpi6_stock_based_compensation","f_shares_diluted_m"]},{"view":"價格已反映太多","evidence":"以 FY2027 共識EPS 3.02 計約46倍本益比、FY2028E 4.83 約29倍；前瞻 EV/S 6.73倍建立在谷底營收上；賣方目標價一年由約380降至約212美元；Zacks 在Q2 後大幅下修 FY2026 EPS；Barclays 減碼，並預期除非交易回升否則預估再降。","assumption":"市場以循環回升後的前高利潤率定價。","consequence":"回升如期，報酬也只剩低個位數年化；回升延後，倍數與盈餘雙殺。","ruling":"採納：基本情境終端 EV/S 5倍，低於現值6.73倍。","watch":"FY2027 共識EPS 是否續降","evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#2","supply_demand_durability#2"],"fact_refs":["f_ev_s_fwd","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_3m_fy1_pct"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 🟠 → 本次 ❌","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=🟠","side_b":"本次 ma=❌","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 184.99 → 本次 140.39（-24.1%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=184.99","side_b":"本次 price_at_dd=140.39","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 184.99 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 184.99 美元：五年期望值 前份未列，基準年化 前份未列，前份未列不對稱比","side_b":"本次情境、股價仍用 184.99 美元：Bull 價 341.07、Bear 價 48.67，五年期望值 −8.6%，基準年化 −1.4%，不對稱比 0.76","ruling":"先換情境、股價不動：五年期望值與基準年化前份未列，無法比較。前份未列不對稱比，本次為 0.76。Bull、Bear 價位與股價無關，只受情境影響。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 184.99 美元：五年期望值 −8.6%，基準年化 −1.4%，不對稱比 0.76","side_b":"本次情境、股價 140.39 美元：五年期望值 +20.4%，基準年化 4.2%，不對稱比 1.46","ruling":"再換股價、情境不動：起點價下跌 24.1%，五年期望值多 29.0 個百分點，基準年化多 5.6 個百分點，不對稱比由 0.76 升到 1.46。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"一致判斷：2026是交易量谷底年","cause":null,"side_a":"管理層：Q3 現貨量季減10%，靠預測市場與衍生品把交易營收撐平（2026-10-29 Alesia Haas）","side_b":"賣方與數據：William Blair 估2026平台成交量年減約44%、2027反彈逾32%；Q3 交易營收年減44%","ruling":"一致：谷底判斷成立；分歧不在有沒有回升，而在回升後費率與利潤率能回到哪裡","evidence_level":"高","settle_metric":"2026Q4 與2027Q1 交易營收","if_then":["若2027Q1 交易營收年增≥20%，谷底確認，改看費率是否同步回升","反向：若2027Q1 交易營收仍年減≥20%，谷底延後，Bear 機率升至35%"],"evidence_refs":["end_markets#3","supply_demand_durability#1"]},{"axis":"預測市場與衍生品是增量還是填補","cause":null,"side_a":"Q3 法說（2026-10-29 Alesia Haas）：預測市場與衍生品屬增量、不蠶食現貨，二者合占交易營收約25%，預測市場年化營收破2億美元；Q2 法說（2026-07-30 Haas）也稱新產品帶來額外現貨交易","side_b":"交易營收仍年減44%、季減1%，現貨量季減10%，增量只把季營收撐平；Q2 法說被問 Coinbase One 會員每交易美元營收時，CFO 自稱答案不令人滿意、未給數字","ruling":"可調和（程度差異）：增量屬實，但規模不足以改變年度方向；不蠶食的說法管理層連兩季一致但沒有數據，標未證、持續監測","evidence_level":"中","settle_metric":"扣除衍生品與預測市場後的現貨交易營收年增率","if_then":["若2026Q4 起連2季交易營收季增≥10%且衍生品＋預測市場占比≥30%，H1 判為成立並重算情境","反向：若交易營收連2季<5億美元，Bear 機率升至40%，持有者減碼至1%以下"],"evidence_refs":["end_markets#0"]},{"axis":"市占方向：公司自報上升對第三方顯示對手擴張","cause":null,"side_a":"公司自報 Q2 2026 加密成交量市占創紀錄10.3%（Q1 9.1%）；Bernstein 2025年估美國市占66%；Q3 法說分析師稱 Coinbase 為美國現貨第一","side_b":"10-K 自承 DEX 成交量多次媲美自家平台；Artemis 資料 Hyperliquid 2025 名目成交約2.6兆美元、Coinbase 約1.4兆；CryptoRank 4月中心化交易所現貨市占5.3%居第四；Binance Q2 總市占升至35.3%（來源標注日期與內容年份不一致，權重降低）","ruling":"不可調和（方向相反）。裁決選第三方一側：公司市占的分母與涵蓋市場未揭露，而第三方數據與公司自己10-K 的風險揭露方向一致；硬數據點＝Hyperliquid 名目成交高於 Coinbase。這是本次迴避的綁定約束，未持有者不建倉","evidence_level":"中","settle_metric":"公司自報加密成交量市占與交易營收年增率","if_then":["若自報市占連2季≥10%且交易營收年增率轉正，護城河趨勢改判持平並重跑DD，首筆不超過1%","反向：若自報市占連2季<9%，持有者清倉"],"evidence_refs":["competitive_share_entrants#1","competitive_share_entrants#2","substitute_technology#1"]},{"axis":"USDC 分潤守不守得住","cause":null,"side_a":"Q2 法說（2026-07-30 Alesia Haas）：Circle 合約續約條件已達成、以相同條款續約；Q3 法說：拿約50%整體經濟利益、平台持有約30%流通量","side_b":"Q2 法說被問第三方只要持有足夠 USDC 即可取得多數經濟利益（Hyperliquid 合作）時，CFO 只說願意分享經濟利益推動網路效應，未答如何保護、未給分潤比例；Q3 法說 Armstrong 承認雙方都在建穩定幣支付基礎設施","ruling":"可調和（時間差）：短期靠續約守得住，長期分配向分銷夥伴傾斜，列為定價力縮減的證據之一","evidence_level":"中","settle_metric":"平台平均持有 USDC 占流通量","if_then":["若平台 USDC 占比連2季<25%，定價力再扣1分、Bear 機率加5個百分點","反向：若占比連4季≥30%且訂閱與服務年增率轉正，定價力評分回升"],"evidence_refs":[]},{"axis":"淨利與營業利益背離","cause":null,"side_a":"Q3 GAAP 淨利7.187億美元、稀釋EPS 2.51","side_b":"營業利益僅0.617億；約7.15億來自持有加密資產評價（第三方數字未驗證）；CEO 稱剛買進第18,000枚比特幣，資產負債表加密曝險上升；TTM FCF 利潤率68.4% 與營業利益率5.7% 背離","ruling":"採營業利益一側：估值改以營收與營業利益率為準，GAAP EPS 與 FCF 利潤率不作便宜或品質證據","evidence_level":"高","settle_metric":"10-Q 現金流量表中客戶資金與加密資產項目","if_then":["若10-Q 顯示扣除客戶資金後 FCF 利潤率仍≥30%，品質分上調","反向：若扣除後 FCF 為負，資本配置評級維持最低"],"evidence_refs":[]},{"axis":"共識修正的方向","cause":null,"side_a":"共識近3個月修正數值顯示+238%，字面像上修","side_b":"實際是 FY2026 EPS 由−0.5 下修到−1.69（7月中快照還是+1.22）；Zacks 在Q2 後大幅下修 FY2026 EPS；賣方目標價一年由約380降至約212美元；Barclays 減碼並預期除非交易回升否則預估再降","ruling":"以方向為準：共識正在下修，下修中的 Bear 錨不穩，不對稱比不作進場依據","evidence_level":"高","settle_metric":"下一份快照 FY2027 共識EPS 是否低於3.02","if_then":["若 FY2027 共識EPS 再下修≥15%，Bear 營收路徑再下移","反向：若 FY2027 共識上修≥10%且交易營收回升，重算情境"],"evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#2","supply_demand_durability#2"]},{"axis":"現在就買的最強論證","cause":null,"side_a":"Q3 很可能就是谷底：預測市場八個月做到年化2億美元、衍生品＋預測市場占交易營收25%、訂閱與服務季增3%、平台資產季增53%至3,770億美元、淨現金約19億美元；RSI 30.7 接近超賣，比特幣 ETF 本季大量流入；賣方買進評等一年由12家增至19家，Citizens JMP 目標價280美元；上一輪 FY2023→FY2024 營收年增111%","side_b":"回升會來，但現價以 FY2027 共識EPS 計約46倍；回升後要面對 HOOD（營業利益率45.7%）與鏈上永續的費率競爭；SBC 每季約2.3億美元持續稀釋；賣方共識目標價一年由約380降至約212美元","ruling":"不可調和（方向相反）。裁決選不買：基本情境五年終值約172美元、年化約4%，即使循環回升也只拿到8%門檻的一半；硬數據點＝FY2027 本益比約46倍","evidence_level":"中","settle_metric":"交易營收年增率、營業利益率","if_then":["若股價跌至100美元以下且交易營收連2季年增率轉正，重跑DD，首筆不超過1%","反向（證實我錯）：若2027Q2 前交易營收連2季年增≥30%且營業利益率≥15%，承認低估回升力道，重算情境並等回檔進場"],"evidence_refs":["capital_markets_pricing#0"]},{"axis":"裁員與SBC：成本紀律有沒有回到股東","cause":null,"side_a":"2026-05 宣布裁員約700人（14%），重組費用5,000–6,000萬美元","side_b":"Q3 SBC 2.33億美元、Q4 指引約2.4億美元，不降反升，是Q3 營業利益的3.8倍","ruling":"可調和但對股東不利：裁員省下現金成本，股票報酬照發，每股價值仍被稀釋；終端股數已按年約1–2.5% 增加反映","evidence_level":"高","settle_metric":"SBC 占營收","if_then":["若 SBC 占營收連2季>20%，長期信心維持低、不建倉","反向：若 SBC 占營收連2季≤12%，H3 進度確認，品質分上調"],"evidence_refs":["major_events#0"]},{"axis":"監管明朗是護城河還是降低門檻","cause":null,"side_a":"GENIUS Act 已成法，SEC 與 CFTC 合作推動美國開放（Q3 法說 Armstrong）；CFTC 為 Coinbase 相關爭議起訴紐約州","side_b":"10-K 預期美國監管明朗後來自美國公司的競爭增加；多州機關與監管機關傳票仍涉及上架、質押、穩定幣與收益產品","ruling":"可調和：對託管與衍生品偏正（Deribit 可對美國開放），對零售交易費率偏負（合規不再稀缺）；淨效果使交易費率這段護城河變窄","evidence_level":"中","settle_metric":"美國主要券商上線加密現貨後的公司自報市占","if_then":["若主要券商上線加密現貨後兩季內自報市占仍≥10%，監管淨效果改判中性","反向：若監管機關對質押或收益產品正式執法，持有者減碼一半"],"evidence_refs":["competitive_share_entrants#0","regulatory_antitrust#0"]},{"axis":"綜合評等、估值結論與護城河趨勢變動","cause":"新證據","prior_field":["signal","val","moat_trend"],"side_a":"前份（2026-05-25，股價184.99美元）：綜合評等B、估值中性、護城河趨勢未評","side_b":"本次（股價140.39美元）：綜合評等C、估值偏貴、護城河趨勢向下","ruling":"股價跌24%本應讓估值變便宜，但同期分母下滑更多：FY2026 共識EPS 由7月快照的+1.22轉為−1.69，Q3 交易營收年減44%、訂閱與服務年減20%；護城河向下來自10-K 自承競爭集合擴大與 Hyperliquid 成交量超越等新證據，不是價格造成","evidence_level":"高","settle_metric":"FY2027 共識EPS 與交易營收年增率","if_then":["若交易營收連2季年增率轉正且自報市占≥10%，護城河趨勢改判持平並重跑","反向：若 FY2027 共識EPS 再下修≥15%，維持C並把 Bear 機率升至35%"],"evidence_refs":["end_markets#0","competitive_share_entrants#0"]},{"axis":"價值陷阱風險不變","cause":"價格變動","prior_field":["trap"],"side_a":"前份（股價184.99美元）：價值陷阱風險中等","side_b":"本次（股價140.39美元）：仍為中等","ruling":"股價下跌沒有改變判斷：SBC 占營收上升與替代技術壓縮兩項亮燈，毛利率與市占兩項待證；跌價只把同樣的風險搬到較低價位，不構成安全邊際","evidence_level":"中","settle_metric":"衰退信號亮燈數","if_then":["若待證兩項證實亮燈，價值陷阱風險升為高"],"evidence_refs":[]},{"axis":"格式補欄（前份空值）","cause":"方法變動","prior_field":["runway_post_y5","archetype","cycle_position","p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份：成長跑道、公司類型、循環位置、定期定額裁決與角色、情境機率與最大回撤皆為空值（舊格式未要求或情境樹未跑）","side_b":"本次：成長跑道中等、類型為金融（交易所）兼循環、循環位置深谷、情境機率牛20%／基準50%／熊30%、最大回撤−60%至−80%；定期定額裁決與角色由程式產出","ruling":"屬格式補欄，不是判斷翻轉；與前份沒有可比基準","evidence_level":"高","settle_metric":"不適用","if_then":["若下一份判斷這些欄位變動，依原因逐欄歸因"],"evidence_refs":[]},{"axis":"重新進場條件變動","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"前份未設重新進場條件（原文為空值）","side_b":"交易營收連2季年增率轉正、自報加密成交量市占連2季≥10%、FY2027 共識EPS 停止下修，三者皆成立才重跑DD，首筆進場不超過1%","ruling":"本次結論改為迴避，綁定約束是費率侵蝕證據，重新進場條件即該約束的否定；三條件以「且」連接，避免只靠股價反彈就進場","evidence_level":"中","settle_metric":"季報交易營收與市占","if_then":["三條件皆成立：重跑DD，首筆不超過1%","反向：任一條件連2季未達，維持不建倉"],"evidence_refs":[]},{"axis":"減碼與清倉指標新設","cause":"新證據","prior_field":["kill_metrics"],"side_a":"前份未設減碼與清倉指標（原文為空值）","side_b":"交易營收連2季<5億美元→減碼；訂閱與服務單季<5億美元→減碼一半；平台 USDC 占流通量連2季<25%、TTM 營業利益率連2季<0%、SBC 占營收連2季>20%→信心降級；自報市占連2季<9%→清倉","ruling":"谷底期營業利益率僅5.1%，前份沒有對應的減碼與清倉數字，本次補上以營收與市占為主的指標","evidence_level":"中","settle_metric":"每季財報","if_then":["任一減碼指標觸發：持有者減碼至1%以下","清倉指標觸發：清倉"],"evidence_refs":[]},{"axis":"Single Thing 變動","cause":"新證據","prior_field":["single_thing"],"side_a":"前份未設 Single Thing（原文為空值）","side_b":"美國市場結構法或財政部規則明文禁止交易平台對穩定幣持有者支付回饋，USDC 在平台存放規模與分潤收入同步下滑","ruling":"穩定幣分潤是訂閱與服務中最大、利潤率最高的一塊，谷底期營業利益率僅5%，這一刀的敏感度大於任何單一產品；前份把同類風險放在監管假設裡但未設唯一致命點，本次獨立列出，觸發即清倉","evidence_level":"中","settle_metric":"立法條文與財政部規則","if_then":["禁令定案：持有者清倉","反向：條文明確允許平台回饋，Single Thing 降級並重估訂閱與服務底盤"],"evidence_refs":[]},{"axis":"風險門檻改寫（減碼與清倉條件）","cause":"方法變動","prior_field":["R1","R2","R3"],"side_a":"前份：R1 連2季現貨成交量年減30%以上且BTC 回撤40%→減倉三分之一；R2 財政部最終規則廣義解釋→重估論點；R3 連4季綜合費率年減10%以上且中心化交易所現貨占比下降→護城河重估、可能砍倉","side_b":"本次：R1 交易營收連2季<5億美元→減碼至1%以下；R2 自報加密成交量市占連2季<9%→清倉；R3 監管罰款或和解≥5億美元或停止美國收益產品→減碼一半；另增營運中斷、USDC 占比、SBC 三條","ruling":"改用公司每季直接揭露的營收與市占數字當門檻，因為費率與BTC 回撤不在公司揭露或事實表內；前份R1 的成交量條件大致已觸發（Q2 消費者成交量258億美元對前年415億、年減38%；Q3 機構現貨年減53%），BTC 回撤條件事實表未涵蓋，故改以交易營收門檻接手","evidence_level":"中","settle_metric":"季交易營收、自報市占","if_then":["若交易營收連2季<5億美元，持有者減碼至1%以下","反向：若交易營收連2季≥7億美元且市占≥10%，撤銷減碼條件並重跑"],"evidence_refs":["end_markets#0"]},{"axis":"論點改寫：前份訂閱與服務成長假設落空","cause":"新證據","prior_field":["H1","H2","H3"],"side_a":"前份 H2 的2年驗證點：FY2026 訂閱與服務營收年增≥5%；H1：FY2027 交易營收≥38億美元","side_b":"Q3 2026 訂閱與服務年減20%、交易營收年減44%（單季5.9億美元，年化約24億）；本次 H1 改為 FY2027 交易營收≥30億美元，H2 改為單季不低於5.5億美元且 FY2027≥24億美元，新增 H3 成本紀律","ruling":"前份 H2 的2年驗證點已確定落空；H1 門檻在現有量能下需年增約27%才能達到。下修門檻不是放寬，而是承認谷底比前份假設更深；不延用前份論點","evidence_level":"高","settle_metric":"FY2027 交易營收與訂閱與服務營收","if_then":["若 FY2027 交易營收<24億美元（與2026Q3 年化持平），H1 判為反轉，持有部位清倉","反向：若 FY2027 交易營收≥38億美元（前份門檻），回升強於本次假設，重算情境並上調 Bull 機率"],"evidence_refs":["end_markets#0"]}],"triggers":[{"n":1,"text":"2026Q4 財報驗證交易營收是否見底","type":"假設驗證","maps_to":"H1","metric":"季交易營收與衍生品＋預測市場占比","threshold":"≥6億美元且衍生品＋預測市場占比≥25%","action":"成立則持續觀察並準備重跑；不成立則 Bear 機率升至35%","source_freq":"季報8-K／每季","date":"2027-02"},{"n":2,"text":"交易量谷底延長","type":"風險","maps_to":"R1","metric":"季交易營收","threshold":"連2季<5億美元","action":"持有者減碼至1%以下；未持有者不建倉","source_freq":"季報8-K／每季","date":null,"evidence_refs":["end_markets#0","end_markets#3","supply_demand_durability#1"]},{"n":3,"text":"訂閱與服務底盤破裂","type":"減碼","maps_to":"H2","metric":"季訂閱與服務營收","threshold":"單季<5億美元（Q4 指引下緣5.5億美元再低約9%）","action":"持有者減碼一半","source_freq":"季報8-K／每季","date":null},{"n":4,"text":"穩定幣回饋禁令定案","type":"Single Thing","maps_to":"Single Thing","metric":"美國市場結構法或財政部規則條文","threshold":"明文禁止交易平台對穩定幣持有者支付回饋或收益","action":"持有者清倉；未持有者維持迴避至重跑","source_freq":"立法與規則公告／事件","date":null},{"n":5,"text":"監管與訴訟升級為執法","type":"風險","maps_to":"R3","metric":"州或聯邦對質押、穩定幣收益產品的正式執法與訴訟結果","threshold":"任一案罰款或和解≥5億美元，或命令停止美國收益產品","action":"持有者減碼一半並重估 H2","source_freq":"8-K 與10-Q 法律程序附註／事件","date":null,"evidence_refs":["regulatory_antitrust#0","major_events#2","sec_investigation_restatement#0","lawsuit_class_action#0","reg_tariff_export#1"]},{"n":6,"text":"營運中斷復發","type":"風險","maps_to":"R4","metric":"全平台交易中斷次數","threshold":"12個月內第3次≥1小時中斷","action":"護城河執行分下修1分，持有者減碼至1%以下","source_freq":"公司狀態頁與新聞／事件","date":null,"evidence_refs":["geo_supply_chain#0","geo_supply_chain#1","geo_supply_chain#2"]},{"n":7,"text":"重新進場評估條件","type":"估值rearm","maps_to":"R2","metric":"交易營收年增率、公司自報加密成交量市占、FY2027 共識EPS","threshold":"交易營收連2季年增率轉正、自報市占連2季≥10%、FY2027 共識EPS 停止下修，三者皆成立","action":"重跑DD，若通過首筆不超過1%","source_freq":"季報與共識快照／每季","date":null},{"n":8,"text":"費率侵蝕證實","type":"清倉","maps_to":"R2","metric":"公司自報加密成交量市占","threshold":"連2季<9%","action":"持有者清倉","source_freq":"季報投影片／每季","date":null,"evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1","substitute_technology#1"]},{"n":9,"text":"定期複審","type":"複審日期","maps_to":null,"metric":"2026Q4 財報與 FY2027 指引","threshold":"財報公布後一週內","action":"重跑判斷","source_freq":"季報","date":"2027-02"}],"kill_metrics":[{"metric":"季交易營收","bear_threshold":"連2季<5億美元","window":"2026Q4–2027Q3","source":"季報8-K","last_status":"warning"},{"metric":"季訂閱與服務營收","bear_threshold":"單季<5億美元","window":"每季","source":"季報8-K","last_status":"ok"},{"metric":"平台平均持有 USDC 占流通量","bear_threshold":"連2季<25%","window":"每季","source":"法說會與財報投影片","last_status":"ok"},{"metric":"TTM GAAP 營業利益率","bear_threshold":"連2季<0%","window":"每季","source":"10-Q","last_status":"warning"},{"metric":"SBC 占營收","bear_threshold":"連2季>20%","window":"每季","source":"季報8-K","last_status":"warning"},{"metric":"公司自報加密成交量市占","bear_threshold":"連2季<9%","window":"每季","source":"季報投影片","last_status":"unknown"}],"evidence_dismissed":[],"action_conditions":{"rearm_trigger":"交易營收連2季年增率轉正、自報加密成交量市占連2季≥10%、FY2027共識EPS停止下修，三者皆成立才重跑DD，首筆不超過1%","exec_line":"未持有：不建倉。持有者：上限3%；交易營收連2季<5億美元減碼至1%以下；訂閱與服務單季<5億美元減碼一半；穩定幣回饋禁令定案或自報市占連2季<9%清倉。","holding_cap":"≤3%"}},"decision_inputs":{"signal":"C","ma":"❌","cycle_position":"深谷投降","cycle_verdict":"未觸發","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"賣方與市場以前一循環高點的利潤率（FY2024 營業利益率34%）為錨推算復甦，沒有扣除 DEX、多資產券商與美國新進者對交易費率的結構性壓縮，也沒有扣除 USDC 分潤被分銷夥伴分食與 SBC 稀釋。","momentum_overheated":false,"cycle_gates_pass":false,"qc49_inherit_prior":null,"wait_for_price":null},"decision_out":{"verdict":"迴避","role":"不持有","row_hit":"3","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='C'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":true,"basis":"moat_trend='↓', moat='C'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":true,"basis":"ma='❌'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]}],"pacing":["row4：週線❌，進場節奏強制分批（starter 1/3＋趨勢確認後加碼），頁首掛「⚠️ 週線趨勢未確認，逢回分批勿接刀」"],"holding_cap":null,"requires_critic":[]},"thesis":{"H":[{"id":"H1","text":"交易營收隨加密循環回升，衍生品與預測市場占比提高，讓費率下滑由產品組合抵銷","2y":"FY2027 交易營收≥30億美元（Q3 2026 單季5.9億美元，年化約24億）","5y":"FY2031 交易營收≥45億美元，衍生品＋預測市場占比≥35%","10y":null,"threshold":"2年：FY2027 交易營收≥30億美元，且衍生品＋預測市場占交易營收≥30%（Q3 約25%）","source":"季報8-K 交易營收與法說會揭露的產品組合","drift_rule":"TTM 交易營收較門檻路徑連2季偏離≥5%為削弱、連3季≥10%為反轉"},{"id":"H2","text":"訂閱與服務營收是跨循環底盤：USDC 分潤、質押、Coinbase One 與 Base 合計每季不低於5.5億美元，FY2027 占淨營收≥45%","2y":"FY2027 訂閱與服務≥24億美元且占淨營收≥45%（Q3 約49%）","5y":"FY2031 訂閱與服務≥35億美元","10y":null,"threshold":"2年：單季不低於5.5億美元（Q4 指引下緣），FY2027≥24億美元","source":"季報8-K、法說會揭露的 USDC 占流通量與分潤比例","drift_rule":"TTM 訂閱與服務較門檻連2季偏離≥5%為削弱、連3季≥10%為反轉"},{"id":"H3","text":"成本紀律：中循環年度 GAAP 營業利益率回到20%以上，SBC 占營收降到10%以下，縮小與多資產券商的利潤率差距","2y":"FY2027 GAAP 營業利益率≥15%、SBC 占營收≤12%（Q3 為5.1%與19.2%）","5y":"FY2029–FY2031 平均營業利益率≥22%","10y":null,"threshold":"2年：FY2027 營業利益率≥15%且 SBC 占營收≤12%","source":"10-K／10-Q 損益表","drift_rule":"5年：TTM 營業利益率連4季低於門檻路徑5個百分點為削弱、連6季10個百分點為反轉"}],"R":[{"id":"R1","text":"加密交易量谷底延長到2027年之後，交易營收無法回升","h_ref":"H1","clock":"⚡","threshold":"交易營收連2季<5億美元：持有者減碼至1%以下","evidence_refs":["end_markets#0","end_markets#3","supply_demand_durability#1","supply_demand_durability#2"]},{"id":"R2","text":"DEX 與鏈上永續、多資產券商、美國新進者三面侵蝕交易費率與份額","h_ref":"H1","clock":"🔥","threshold":"公司自報加密成交量市占連2季<9%（Q2 紀錄10.3%）：清倉","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1","competitive_share_entrants#2","substitute_technology#0","substitute_technology#1"]},{"id":"R3","text":"州與聯邦對上架、質押、穩定幣收益產品的調查升級為執法，或集體訴訟不利判決，制裁與反洗錢執法隨國際擴張增加","h_ref":"H2","clock":"🔥","threshold":"任一案罰款或和解≥5億美元，或命令停止美國收益產品：減碼一半並重估 H2","evidence_refs":["regulatory_antitrust#0","reg_tariff_export#1","major_events#2","sec_investigation_restatement#0","lawsuit_class_action#0"]},{"id":"R4","text":"雲端單點依賴造成交易中斷，侵蝕機構與高頻客戶信任","h_ref":"H1","clock":"⚡","threshold":"12個月內第3次≥1小時全平台交易中斷：護城河執行分下修1分、持有者減碼至1%以下","evidence_refs":["geo_supply_chain#0","geo_supply_chain#1","geo_supply_chain#2"]},{"id":"R5","text":"USDC 經濟利益被分銷夥伴與 Circle 自建通路分食","h_ref":"H2","clock":"🐢","threshold":"平台平均持有 USDC 占流通量連2季<25%（Q3 約30%）：定價力扣1分、Bear 機率加5個百分點","evidence_refs":[]},{"id":"R6","text":"SBC 居高不下，營收回升創造的價值被股數稀釋吃掉","h_ref":"H3","clock":"🔥","threshold":"SBC 占營收連2季>20%（Q3 為19.2%）：長期信心維持低、不建倉","evidence_refs":["major_events#0"]}],"single_thing":{"description":"美國市場結構法或財政部規則明文禁止交易平台對穩定幣持有者支付回饋，USDC 在平台存放規模與分潤收入同步下滑","why_fatal":"穩定幣分潤是訂閱與服務中最大、利潤率最高的一塊（前份摘要引 Q1 2026 8-K，單季約3.05億美元，約為當季訂閱與服務營收5.835億的一半）；谷底期營業利益率僅5%，失去這塊等於拿掉跨循環底盤，H2 失效","if_happens":"持有者清倉；H2 改寫，Bear 機率升至40%以上並重跑情境","how_monitor":"國會市場結構法條文中回饋與收益的定義、財政部 GENIUS Act 施行規則、每季法說揭露的平台平均 USDC 持有量與占流通量比重（Q3 約30%）","probability":"15%（12–24個月）：Q2 法說 CEO 稱法案不過公司照常營運，顯示管理層認為現行回饋模式不依賴新法；風險在立法條文尚未定案"}},"appendix_a":{"growth_durability":4,"quality_score":6,"ai_risk":"🟡","long_term_confidence":"低","fpe_fy2":46.5,"peg_fy2":null,"stress":{"pass":1,"total":5}},"eps_meta":{"base_eps_path":{"FY2025A":4.45,"FY2026E":-1.69,"FY2027E":3.02,"FY2028E":4.83},"fy_end_month":12,"eps_basis":"GAAP 稀釋EPS（Koyfin 共識快照；含持有加密資產評價損益，基期與 FY2026 皆受影響）"},"catalysts":[{"date":"2027-02","date_precision":"month","type":"guidance","event":"2026年第四季財報與2027年第一季訂閱與服務指引","impact":"高","watch":"交易營收是否≥6億美元、訂閱與服務是否守住5.5億美元"},{"date":null,"date_precision":null,"type":"regulatory","event":"美國市場結構法（CLARITY）立法進度與穩定幣回饋條款","impact":"高","watch":"條文是否禁止交易平台支付穩定幣回饋"},{"date":null,"date_precision":null,"type":"product","event":"Coinbase Pro 進階交易平台重新上線、Deribit 對美國客戶開放","impact":"中","watch":"衍生品與預測市場占交易營收是否升到30%"}]}
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
