你是 DD 管線 v20 的判斷層閘（gate），標的 GOOGL（20261103）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（49 條）
- `f_kpi0_gaap`（q1_business）｜營收（GAAP）＝127.577 USD bn｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Alphabet Q3 2026 earnings release（IR：https://s206.q4cdn.com/479360582/files/doc_financials/2026/q3/2026q3-alphabet-earnings-release.pdf；8-K Ex.99.1：https://www.sec.gov/Archives/edgar/data/0001652044/000165204426000080/googexhibit991q32026.htm）（numbers.latest_quarter_kpis.items[0]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-28））
  - 註記：未查得 Q3 單季共識營收；媒體稱 EPS 與營收低於預期，未採（非 IR 來源）
- `f_kpi1_gaap`（q1_business）｜GAAP 營業利益＝40.576 USD bn｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Alphabet Q3 2026 earnings release（IR：https://s206.q4cdn.com/479360582/files/doc_financials/2026/q3/2026q3-alphabet-earnings-release.pdf；8-K Ex.99.1：https://www.sec.gov/Archives/edgar/data/0001652044/000165204426000080/googexhibit991q32026.htm）（numbers.latest_quarter_kpis.items[1]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-28））
  - 註記：未查得
- `f_kpi2_gaap`（q1_business）｜GAAP 營業利益率＝31.8 %｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Alphabet Q3 2026 earnings release（IR：https://s206.q4cdn.com/479360582/files/doc_financials/2026/q3/2026q3-alphabet-earnings-release.pdf；8-K Ex.99.1：https://www.sec.gov/Archives/edgar/data/0001652044/000165204426000080/googexhibit991q32026.htm）；Q3 2026 earnings call 逐字稿 2026-10-28（numbers.latest_quarter_kpis.items[2]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-28））
  - 註記：未查得
- `f_kpi3_non_gaap`（q1_business）｜Non-GAAP 營業利益／利益率＝— %｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Alphabet Q3 2026 earnings release（IR：https://s206.q4cdn.com/479360582/files/doc_financials/2026/q3/2026q3-alphabet-earnings-release.pdf；8-K Ex.99.1：https://www.sec.gov/Archives/edgar/data/0001652044/000165204426000080/googexhibit991q32026.htm）（numbers.latest_quarter_kpis.items[3]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-28））
  - 註記：不適用
- `f_kpi6_google_cloud`（q1_business）｜Google Cloud 營收＝30.7 USD bn｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Alphabet Q3 2026 earnings release（IR：https://s206.q4cdn.com/479360582/files/doc_financials/2026/q3/2026q3-alphabet-earnings-release.pdf；8-K Ex.99.1：https://www.sec.gov/Archives/edgar/data/0001652044/000165204426000080/googexhibit991q32026.htm）；Q3 2026 earnings call 逐字稿 2026-10-28（numbers.latest_quarter_kpis.items[6]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-28））
  - 註記：未查得
- `f_kpi7_google_cloud`（q1_business）｜Google Cloud 營業利益／利益率＝11.121 USD bn（利益率 36.2%）｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Alphabet Q3 2026 earnings release（IR：https://s206.q4cdn.com/479360582/files/doc_financials/2026/q3/2026q3-alphabet-earnings-release.pdf；8-K Ex.99.1：https://www.sec.gov/Archives/edgar/data/0001652044/000165204426000080/googexhibit991q32026.htm）；Q3 2026 earnings call 逐字稿 2026-10-28（numbers.latest_quarter_kpis.items[7]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-28））
  - 註記：未查得
- `f_kpi8_google_cloud_backlog`（q1_business）｜Google Cloud backlog＝561 USD bn｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Q3 2026 earnings call 逐字稿 2026-10-28（CFO 發言）（numbers.latest_quarter_kpis.items[8]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-28））
  - 註記：未查得
- `f_kpi9_capex`（q1_business）｜資本支出（capex）＝51.355 USD bn｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Alphabet Q3 2026 earnings release（IR：https://s206.q4cdn.com/479360582/files/doc_financials/2026/q3/2026q3-alphabet-earnings-release.pdf；8-K Ex.99.1：https://www.sec.gov/Archives/edgar/data/0001652044/000165204426000080/googexhibit991q32026.htm）（numbers.latest_quarter_kpis.items[9]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-28））
  - 註記：媒體稱共識約 55.09bn（非 IR 來源，僅供參考）
- `f_kpi10`（q1_business）｜管理層指引＝2026 全年 capex 195–205bn（維持不變） text｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：Q3 2026 earnings call 逐字稿 2026-10-28（CFO outlook）（numbers.latest_quarter_kpis.items[10]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-28））
  - 註記：不適用
- `f_peer_googl_gross_margin_pct`（q2_moat）｜GOOGL 毛利率＝60.86 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.GOOGL.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_earnings_recency`（q1_business）｜最近一次財報日＝2026-10-28 date｜期間與口徑：2026-10-28／距今 4 個交易日｜kind：realized
  - 來源：—（numbers.earnings_recency，as_of 2026-10-28）
- `f_peer_googl_operating_margin_pct`（q2_moat）｜GOOGL 營業利益率＝33.32 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.GOOGL.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_googl_fcf_margin_pct`（q2_moat）｜GOOGL FCF 利潤率＝4.19 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.GOOGL.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_msft_gross_margin_pct`（q2_moat）｜MSFT 毛利率＝67.66 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MSFT.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_msft_operating_margin_pct`（q2_moat）｜MSFT 營業利益率＝47.1 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MSFT.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_msft_fcf_margin_pct`（q2_moat）｜MSFT FCF 利潤率＝17.31 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MSFT.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_amzn_operating_margin_pct`（q2_moat）｜AMZN 營業利益率＝12.36 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.AMZN.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_amzn_fcf_margin_pct`（q2_moat）｜AMZN FCF 利潤率＝-0.82 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.AMZN.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_aapl_operating_margin_pct`（q2_moat）｜AAPL 營業利益率＝33.17 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.AAPL.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_aapl_fcf_margin_pct`（q2_moat）｜AAPL FCF 利潤率＝29.28 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.AAPL.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_meta_gross_margin_pct`（q2_moat）｜META 毛利率＝81.03 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.META.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_meta_operating_margin_pct`（q2_moat）｜META 營業利益率＝32.86 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.META.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_meta_fcf_margin_pct`（q2_moat）｜META FCF 利潤率＝11.86 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.META.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝16.55 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-10-31）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝15.14 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-10-31）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝18.26 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-10-31）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝499593.88 USD m｜期間與口徑：2026-11-03／yfinance revenue_estimate 0y 平均（45 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝634498.64 USD m｜期間與口徑：2026-11-03／yfinance revenue_estimate +1y 平均（49 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi4`（q4_capital）｜自由現金流（單季）＝-9.065 USD bn｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Alphabet Q3 2026 earnings release（IR：https://s206.q4cdn.com/479360582/files/doc_financials/2026/q3/2026q3-alphabet-earnings-release.pdf；8-K Ex.99.1：https://www.sec.gov/Archives/edgar/data/0001652044/000165204426000080/googexhibit991q32026.htm）；Q3 2026 earnings call 逐字稿 2026-10-28（numbers.latest_quarter_kpis.items[4]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-28））
  - 註記：未查得
- `f_kpi5_sbc_gaap`（q4_capital）｜SBC 占 GAAP 營業利益＝21.3 %｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：Alphabet Q3 2026 earnings release（IR：https://s206.q4cdn.com/479360582/files/doc_financials/2026/q3/2026q3-alphabet-earnings-release.pdf；8-K Ex.99.1：https://www.sec.gov/Archives/edgar/data/0001652044/000165204426000080/googexhibit991q32026.htm）（SBC 8,630m ÷ 營業利益 40,576m；占營收 6.8%）（numbers.latest_quarter_kpis.items[5]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-28））
  - 註記：不適用
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝-114767.0 USD m｜期間與口徑：2026-11-03／yfinance 最新一季：總債務 150331.0、現金 265098.0（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝0.304 %｜期間與口徑：2026-11-03／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-11-03）
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝12294.0 m shares｜期間與口徑：2026-11-03／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_ps_current`（q5_valuation）｜P/S（現值）＝7.38 x｜期間與口徑：2026-11-02（RTH 收盤，UTC）／4 個年度端點內的分位＝60.8｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-11-02（RTH 收盤，UTC））
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝282.98 USD｜期間與口徑：2026-11-02（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-11-02（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝17.1 x｜期間與口徑：2026-10-31／分母＝FY1 EPS 16.55，分子＝快照價 282.97｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-10-31）
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝14.77 x｜期間與口徑：2026-11-02（RTH 收盤，UTC）／4 個年度端點內的分位＝0.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-11-02（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝0.0 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝60.8 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝7.14 x｜期間與口徑：2026-11-02（RTH 收盤，UTC）／4 個年度端點內的分位＝55.5｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝55.5 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ev_s_fwd`（q5_valuation）｜EV/S（EV ÷ FY1 共識營收）＝6.73 x｜期間與口徑：2026-11-03／f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）｜kind：estimate
  - 來源：—（numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_consensus_rev_fy1_pct`（q5_valuation）｜FY1 共識修正＝39.19 %｜期間與口徑：2026-10-31／兩份 Koyfin 快照之間的 EPS 修正幅度（11.89 → 16.55）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.fy1.revision_pct，as_of 2026-10-31）
- `f_consensus_rev_fy2_pct`（q5_valuation）｜FY2 共識修正＝-0.33 %｜期間與口徑：2026-10-31／兩份 Koyfin 快照之間的 EPS 修正幅度（15.19 → 15.14）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.fy2.revision_pct，as_of 2026-10-31）
- `f_consensus_rev_fy3_pct`（q5_valuation）｜FY3 共識修正＝-0.87 %｜期間與口徑：2026-10-31／兩份 Koyfin 快照之間的 EPS 修正幅度（18.42 → 18.26）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.fy3.revision_pct，as_of 2026-10-31）
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝-19.58 %｜期間與口徑：2026-07-30 → 2026-10-31／FY1 共識 EPS 20.58 → 16.55（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-10-31）
- `f_ev_m`（q5_valuation）｜目前企業價值 EV（市值＋淨負債）＝3363705.88 USD m｜期間與口徑：2026-11-03／市值 3478472.88 ＋ 淨負債 -114767.0｜kind：realized
  - 來源：—（numbers.capital_structure.ev_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝-26.09 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-11-02（RTH 收盤，UTC））
- `f_rsi14`（q5_valuation）｜RSI(14)＝24.06｜期間與口徑：2026-11-02（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-11-02（RTH 收盤，UTC））

### findings_digest 中方向為負或來源衝突的條目（20 條）
- `competitive_share_entrants#1`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K 風險因素承認新進入者可能提供相似或更好的體驗，消費者可能改變取得資訊的方式，進而降低既有產品效用
  - 來源：SEC EDGAR 10-K FY2025 Item 1A Risk Factors（as_of 2026-02-05）｜affects：moat_trend、decision_inputs.bear
- `competitive_share_entrants#2`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K 指出 AI 加速器（含 GPU 與自研 TPU）供給產能競爭激烈，競爭者若先搶下產能可能使 Alphabet 成本上升、供給受限
  - 來源：SEC EDGAR 10-K FY2025 Item 1A Risk Factors（as_of 2026-02-05）｜affects：decision_inputs.bear、thesis.R
- `customer_concentration_credit#2`（customer_concentration_credit｜方向 -｜狀態 ok）：10-K 風險因子：國際營收約占 2025 年合併營收 52%，部分國家付款週期較長、信用風險與付款詐欺較高。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A Risk Factors（as_of 2026-02-05）｜affects：decision_inputs.bear
- `supply_demand_durability#2`（supply_demand_durability｜方向 -｜狀態 ok）：EMARKETER 預測美國媒體廣告 2026 年增 15.6%、2027 年僅增 9.4%，部分來自世足賽與期中選舉等週期因素；IAB 亦提醒 2027 放緩
  - 來源：EMARKETER: IAB raises ad spending forecast for 2026, but marketers should brace for 2027 slowdown（as_of 2026-06-01）｜affects：thesis.R、decision_inputs.bear
- `regulatory_antitrust#0`（regulatory_antitrust｜方向 -｜狀態 ok）：搜尋案：2025-12 地方法院作出最終判決，限制搜尋分發並要求與特定競爭對手分享搜尋資料與提供syndication；Alphabet 2026-01 上訴，DOJ 與各州 2026-02 亦上訴。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-05）｜affects：moat_trend、thesis.R、decision_inputs.bear
- `regulatory_antitrust#1`（regulatory_antitrust｜方向 -｜狀態 ok）：廣告技術案：2025-04 判決混合（出版商工具排擠對手、廣告主工具與併購不違法）；DOJ 的補救方案含結構性補救，2025-11 結案辯論後待最終判決（截至 10-K）。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-05）｜affects：thesis.R、decision_inputs.bear、valuation
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：Alphabet 10-K FY2025 風險因素：供應短缺、漲價、交期拉長可能由關稅、制裁與出口管制、貿易爭端驅動；部分資料中心與裝置元件僅單一或有限來源；國際營收約占 52%，關稅與進出口管制可能增加成本、限制需求或元件取得。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-05）｜affects：decision_inputs.bear、thesis.R
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：Alphabet FY2025 10-K 風險因素：地緣緊張、制裁、關稅與武裝衝突可能限制其取得零組件或成品的能力
  - 來源：Alphabet Inc. Form 10-K FY2025 (SEC)（as_of 2026-02-05）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：Alphabet 10-K 揭露其倚賴他公司製造多數成品與設計部分零組件，部分零組件僅來自單一或少數來源（FY2021 10-K）
  - 來源：Alphabet Inc. Form 10-K FY2021 (SEC)（as_of 2022-02-01）｜affects：thesis.R
- `geo_supply_chain#2`（geo_supply_chain｜方向 -｜狀態 ok）：報導指 Google 所有 TPU 由 TSMC 製造（Ironwood 用 N3P，下一代 N2），Broadcom 負責設計、MediaTek 協調
  - 來源：Jon Peddie Research: Ironwood, Broadcom, MediaTek and TSMC（as_of 2025-12-01）｜affects：thesis.R、decision_inputs.bear
- `end_markets#3`（end_markets｜方向 -｜狀態 ok）：美國搜尋市佔：WebFX 報告 Google 美國市佔 12 個月內由 87.28% 降至 84.17%，Bing 達 10.48% 創高；全球 StatCounter 約 90%；Google 付費搜尋點擊 2026 Q1 年增 14%，分析師指出 Q2 放緩。
  - 來源：WebFX Google vs Bing; Search Engine Journal（as_of 2026-06-01）｜affects：moat_trend、thesis.R
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：10-K 競爭章節列出『AI model developers and providers of AI products and services』為競爭對手之一，並稱業務特徵為快速變化與新型顛覆性技術。
  - 來源：SEC EDGAR 10-K FY2025 Item 1 Business（as_of 2026-02-05）｜affects：moat_trend、thesis.R
- `substitute_technology#1`（substitute_technology｜方向 -｜狀態 ok）：10-K 風險因素自述：新技術可能使競爭者提供相似或更好的體驗，消費者可能改變取得資訊的方式，降低現有產品效用與使用量。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A Risk Factors（as_of 2026-02-05）｜affects：moat_trend、thesis.R、decision_inputs.bear
- `substitute_technology#2`（substitute_technology｜方向 -｜狀態 ok）：MarketBeat 報導 Alphabet 仍居美國搜尋 88% 市占，同時有資料顯示網站點擊下降 8.9%，並提及年輕用戶轉向 AI 聊天機器人的疑慮。
  - 來源：MarketBeat: AI takes over search, is Google's dominance at risk（as_of 2026-03-01）｜affects：moat_trend、decision_inputs.bear
- `channel_business_model_shift#3`（channel_business_model_shift｜方向 -｜狀態 ok）：Apple Safari 搜尋量下滑證詞與 AI 瀏覽器（Atlas 等）被視為對 Google 預設通路的威脅；Google 公開否認 Safari 搜尋量下降。
  - 來源：SAN: Apple, Google $20 billion search deal at risk amid rise of AI（as_of 2025-05-08）｜affects：moat_trend、decision_inputs.bear
- `capital_markets_pricing#2`（capital_markets_pricing｜方向 -｜狀態 ok）：Q2 後 Alphabet 將 FY2026 capex guidance 上調至 $195–205B（原 $180–190B），高於 Visible Alpha 事前共識 $187.8B；分析師隨後上修 FY26 營收 2% 至 $497.9B、FY26 capex 估計 +7.5%
  - 來源：S&P Global Market Intelligence / w.media（as_of 2026-07-24）｜affects：valuation、decision_inputs.bear
- `major_events#1`（major_events｜方向 -｜狀態 ok）：證券集體訴訟 Stewart v. Alphabet（N.D. Cal., No. 26-cv-11290）：指控就 Gemini 3.5 Pro 時程誤導投資人，class period 2026-05-19 至 2026-07-16；7/16 股價跌 4.4%。另有 2023 年起的舊案（3:23-CV-01186）仍在進行。為原告律所主張，尚非判決。
  - 來源：PRNewswire 律所公告（2026-07-27）（as_of 2026-07-27）｜affects：decision_inputs.bear、triggers
- `major_events#2`（major_events｜方向 -｜狀態 ok）：反壟斷：廣告科技案 2025-04 判決部分不利，DOJ 提出結構性救濟，2025-11 結案辯論，待最終判決；Google Play 州檢察長和解 2025-11 初步核准。
  - 來源：SEC EDGAR 10-K FY2025 Item 8（as_of 2026-02-05）｜affects：decision_inputs.bear、thesis.R
- `lawsuit_class_action#0`（lawsuit_class_action｜方向 -｜狀態 ok）：Stewart v. Alphabet（N.D. Cal., No. 26-cv-11290）證券詐欺集體訴訟，class period 2026-05-19～2026-07-16；為原告主張，未判決。
  - 來源：PRNewswire 律所公告（as_of 2026-07-27）｜affects：decision_inputs.bear、triggers
- `lawsuit_class_action#1`（lawsuit_class_action｜方向 -｜狀態 ok）：DOJ／州檢察長反壟斷案（廣告科技、搜尋、Android／Play）仍在進行，廣告科技案待最終判決。
  - 來源：SEC EDGAR 10-K FY2025 Item 8（as_of 2026-02-05）｜affects：decision_inputs.bear、thesis.R

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 4 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/GOOGL_20261103/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":724.5,"bear_5y_price":195.0,"p_bull_pct":25,"p_bear_pct":30,"upside_5y_pct":67.3,"ev5y_pct":60.0,"irr_base_pct":10.8,"asym_ratio":4.2,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":16.55,"pe":17.1,"basis":"FY2026E 共識 EPS（Koyfin 2026-10-31 快照），終端倍數同樣以當年度 EPS 為分母；FY2026E 含持股未實現損益，所以起點倍數偏低"},"eps":{"bull":[16.2,19.8,23.5,27.3,31.5],"base":[15.14,18.26,20.8,23.5,26.3],"bear":[13.8,13.2,13.6,14.3,15.0]},"pe":{"bull":23,"base":18,"bear":13},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0.304,"net_buyback":-0.5},"second_stage":{"bull_cagr_pct":14,"base_cagr_pct":10},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### GOOGL_Q2_2026_Earnings_Call_20260722.md
- 2026-07-22｜CFO｜guidance：CFO 將 2026 全年 CapEx 指引上調（區間起點）（原話："full year 2026 CapEx guidance range to $195 billion to"）
- 2026-07-22｜CFO｜guidance：CFO 說明上調前的舊區間（原話："previous estimate of $180 billion to $190 billion"）
- 2026-07-22｜CFO｜guidance：CFO 表示 2027 CapEx 將顯著增加，細節稍後提供（原話："expect our CapEx to increase significantly in 2027"）
- 2026-07-22｜CFO｜guidance：CFO 預期 Q3 有輕微匯率逆風（Q2 為 1 個百分點順風）（原話："we would expect a slight FX headwind to our consolidated"）
- 2026-07-22｜CFO｜guidance：CFO 指出 Q3 起開始對比去年 Search 加速的高基期（原話："we will begin lapping an acceleration in Search performance"）
- 2026-07-22｜CFO｜guidance：CFO 表示 TPU 系統銷售合約絕大多數營收在 2027 認列（原話："We anticipate the vast majority of the revenues from these"）
- 2026-07-22｜CFO｜guidance：CFO 預期自由現金流持續承壓（原話："we expect the free cash flow will remain under pressure"）
- 2026-07-22｜CFO｜guidance：CFO 說明折舊與資料中心營運成本將壓抑損益（原話："in the form of higher depreciation expense and"）
- 2026-07-22｜CFO｜margin：Cloud 營業利益率由 20.7% 升至 35.6%（原話："operating margin increased from 20.7% in the second quarter"）
- 2026-07-22｜CFO｜margin：Google Services 營業利益率 41.8%（原話："operating margin was 41.8%"）
- 2026-07-22｜CFO｜margin：集團營業利益 30% 成長至 $40.8B，營業利益率 34%（原話："Operating income increased 30% to $40.8 billion"）
- 2026-07-22｜CFO｜margin：其他營收成本成長的拆解含 TPU 系統銷售的存貨成本（原話："inventory costs, primarily from the sales of TPU systems to"）
- 2026-07-22｜CFO｜margin：CFO 表示 Q3 擴大第三方容量將使 Cloud 營業利益率承壓（原話："will put some pressure on operating margins for"）
- 2026-07-22｜CFO｜margin：CFO 提到 Wiz 整合在 2026 近期造成利潤率逆風（原話："the integration of Wiz does create some"）
- 2026-07-22｜CFO｜margin：CFO 不拆分 TPU 等個別產品的利潤率（原話："we don't break out margins for any specific products"）
- 2026-07-22｜CFO｜margin：G&A 成長含法律等相關費用（原話："charges for certain legal and other"）
- 2026-07-22｜CFO｜margin：OI&E 大增主要來自權益證券未實現利得（原話："unrealized gains in our equity securities portfolio"）
- 2026-07-22｜CFO｜product：Cloud 營收 +82% 至 $24.8B（原話："Cloud revenues were up 82% to $24.8 billion"）
- 2026-07-22｜CFO｜product：Search and Other 營收 +17% 至 $63.3B（原話："other advertising revenues increased by 17% to $63.3 billion"）
- 2026-07-22｜CFO｜product：Network 廣告營收年減 1%（原話："Network advertising revenues of $7.3 billion were down 1%."）
- 2026-07-22｜CEO｜product：CEO 說明模型 API 每分鐘處理 token 量（原話："approximately 22 billion tokens per minute"）
- 2026-07-22｜CEO｜product：CEO 說明 Gemini app 月活（原話："950 million monthly active users"）
- 2026-07-22｜CEO｜product：CEO 說明 AI Mode 月活突破 10 億（原話："we have surpassed 1 billion monthly active users"）
- 2026-07-22｜CEO｜product：CEO 說明 AI Mode 回應成本降至上線以來最低（原話："reduced the cost of AI Mode responses to its lowest level"）
- 2026-07-22｜CEO｜product：CEO 表示已啟動 Gemini 4 最大規模預訓練（原話："ambitious pretraining run yet for Gemini 4"）
- 2026-07-22｜CEO｜product：CEO 說明 3.6 Flash 在 DeepSWE 進步（原話："compared to 3.5 Flash jumped over 10 points in"）
- 2026-07-22｜CBO｜product：YouTube 訂閱業務成長快於廣告（原話："is growing faster than ads"）
- 2026-07-22｜CBO｜product：AI Max 採用者平均轉換或價值增幅（原話："AI Max or PMax see an average of 15% more"）
- 2026-07-22｜CEO｜customer：Cloud 現有客戶用量超出承諾 50% 以上（原話："their commitments by more than 50%"）
- 2026-07-22｜CEO｜customer：近 90% 財星百大使用 Gemini Enterprise（原話："nearly 90% of Fortune 100 are using Gemini Enterprise"）
- 2026-07-22｜CFO｜customer：CFO 說明 Cloud 積壓訂單中約一半 24 個月內認列（原話："to recognize just over 50% of the total backlog as revenue"）
- 2026-07-22｜CEO｜risk：CEO 表示持續供給受限（原話："we continue to be supply constrained"）
- 2026-07-22｜CEO｜competition：CEO 承認 coding／agentic coding 需改進（原話："Coding and agentic coding is an example of that"）
- 2026-07-22｜CEO｜competition：CEO 說明下一代前沿需要更大基礎模型（原話："we will need Gemini 4 as a larger base model to compete"）
- 2026-07-22｜CEO｜competition：CEO 回答護城河：模型只是解決方案的一環（原話："the model is just an ingredient in those solutions"）
- 2026-07-22｜CBO｜competition：CBO 說明對 AI Overviews 查詢的變現表現（原話："We continue to be encouraged with monetization performance"）
- 2026-07-22｜CEO｜commitment：CEO 承諾加快模型發布節奏至近月更（原話："releasing models almost at a monthly cadence"）
- 2026-07-22｜CFO｜commitment：CFO 表示只要有吸引人的回報就持續投資（原話："our goal is to invest as long as we see an attractive"）
- 2026-07-22｜CFO｜commitment：CFO 表示不再回到股權市場（ATM 為稅負 SBC 用途除外）（原話："we're not planning to go back to the equity markets"）
- 2026-07-22｜CFO｜capital_allocation：CFO 說明負債由約 $16B 擴增至約 $100B（原話："we went to about $100 billion across multiple currencies"）
- 2026-07-22｜CFO｜capital_allocation：CapEx 本季 $44.9B（原話："CapEx was $44.9 billion in the second quarter"）
- 2026-07-22｜CEO｜capital_allocation：CEO 說明橋接交易的投報評估（原話："is highly ROI positive"）
- 2026-07-22｜CEO｜capital_allocation：CEO 說明算力分配的基準（原話："what it takes to continue AGI development at the frontier"）
- 2026-07-22｜CEO｜capital_allocation：CEO 提到與 Blackstone 的 TPU 放置專案（原話："like the project we are doing with Blackstone"）
- 2026-07-22｜CEO｜capital_allocation：CEO 談 ROIC 看法（原話："we've gotten more bullish on the opportunities ahead"）
- 2026-07-22｜CEO｜capital_allocation：CEO 談 2027 投資的需求訊號（原話："the dynamics look healthier than where we were"）
- 2026-07-22｜CFO｜capital_allocation：Other Bets 營收與營業虧損（原話："operating loss was $1.8 billion as we continue"）
- 2026-07-22｜CEO｜capital_allocation：CEO 談 Waymo 目前聚焦（原話："We're really focused on scaling the business"）

### 問答異常語氣（迴避／改口／保留）
- GOOGL_Q2_2026_Earnings_Call_20260722.md｜問：Sheridan／Nathanson：TPU 系統銷售的利潤率（增量或較低）｜答法：CFO 表示不拆分個別產品利潤率，改談 TAM 擴張與 Cloud 整體 35.6%，未回答 TPU 是否較低利潤率
- GOOGL_Q2_2026_Earnings_Call_20260722.md｜問：Khajuria：TPU 長期是否發展成商用晶片事業｜答法：CEO 表示不想預測太遠，改談依需求與供給限制擴張
- GOOGL_Q2_2026_Earnings_Call_20260722.md｜問：Gawrelski：Waymo 在何種條件下可能移出 Alphabet 結構｜答法：CEO 未回答結構條件，改說聚焦執行與擴大規模
- GOOGL_Q2_2026_Earnings_Call_20260722.md｜問：Nowak：2027 CapEx 預算哲學與限制如何改變｜答法：CFO 未給 2027 數字，改談供給受限、全端效率與有吸引力回報就投資

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 7 | 4 |
| customer_second_source | not_applicable | 0 | 2 |
| customer_concentration_credit | found | 3 | 0 |
| supply_demand_durability | found | 4 | 2 |
| regulatory_antitrust | found | 3 | 1 |
| reg_tariff_export | found | 2 | 2 |
| geo_supply_chain | found | 3 | 2 |
| end_markets | found | 5 | 4 |
| substitute_technology | found | 4 | 2 |
| channel_business_model_shift | found | 4 | 2 |
| capital_markets_pricing | found | 4 | 2 |
| major_events | found | 5 | 5 |

未涵蓋／不適用軸的查詢詞原文（供判相關性）：
- **customer_second_source**（not_applicable）：Alphabet Google largest customer second source OR in-house custom chip supplier 2026；Alphabet single-source risk customer diversify supplier advertisers

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260723","verdict":"進場","role":"核心","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"搜尋廣告挺過 AI 轉型（AI Mode/AI Overviews 貨幣化不劣於傳統搜尋，本次冷讀後下修信心語氣）","columns":{"2Y 驗證點":"搜尋廣告營收續成長 >10%、AI Mode 貨幣化不使每查詢營收結構下滑","5Y 驗證點":"搜尋仍是最大利潤池、「答案引擎」貨幣化 ≥ 連結搜尋","10Y 驗證點":"意圖層貨幣化在 AI 介面完成遷移","具體數字門檻":"搜尋 YoY ≥ 10%（Q2'26 +17%）且貨幣化不惡化","來源":"公司財報分部；AI Mode 1B MAU（法說）；零點擊 93%/CTR 1.76%→0.61%（web）","漂移觸發":"連 2 季 TTM 偏離 ≥ 5%（季節性/漂移分級）"}},{"id":"H2","text":"Google Cloud 維持 30%+ 成長 + margin 擴張，成第二利潤支柱","columns":{"2Y 驗證點":"Cloud 成長 >30%、OM >30%","5Y 驗證點":"Cloud 營收 >$200B、OM >35%（Q2 已達 35.6%）","10Y 驗證點":"Cloud 成主要利潤來源之一","具體數字門檻":"Cloud YoY ≥ 30%（Q2'26 +82%）、backlog 續增","來源":"公司法說（backlog $514B，QoQ +$50B）","漂移觸發":"連 2 季"}},{"id":"H3","text":"$195-205B capex 賺回資金成本（AI 基建 ROI）、FCF 於 ~2027 復原","columns":{"2Y 驗證點":"Cloud 產能轉營收、TPU 外售起量；FCF 於 ~2027Q1 越過谷底","5Y 驗證點":"FCF 復原至 >$60B、ROIC 不結構下滑","10Y 驗證點":"capex 強度回落、FCF margin 回 >12%","具體數字門檻":"FCF 復原軌跡 + ROIC > WACC","來源":"公司 capex guide（FY26 $195-205B）；FCF crossover ~2027Q1（web）","漂移觸發":"2027 全年 FCF 仍負 + Cloud OM 回落"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"搜尋每查詢貨幣化結構下滑（AI Mode 零點擊自我蠶食 + 外部 AI 助理分流資訊型查詢）","columns":{"對應假設":"H1","時間尺度":"🔥 中期（4-6 季）","監測指標":"搜尋營收 YoY vs 查詢量增；AI Mode 滲透率","警戒閾值":"搜尋 YoY"}},{"id":"R2","text":"AI capex 週期 digestion / overbuild（產業性需求放緩 → Cloud margin 擴張反轉 + 大型科技倍數壓縮，GOOGL 為最大 capex 部署者的相關性曝險）","columns":{"對應假設":"H2/H3","時間尺度":"🔥 中期（4-6 季）","監測指標":"Cloud 增速、Cloud OM、產業 capex/需求增速比","警戒閾值":"Cloud YoY"}},{"id":"R3","text":"反壟斷結構分拆（AdX/DFP 或 Chrome/Android）+ 折舊會計正常化壓 margin","columns":{"對應假設":"H1/H3","時間尺度":"🐢 長期（2+ 年慢變數）＋ AdX 為 binary tail","監測指標":"AdX 裁決 docket；折舊政策揭露","警戒閾值":"強制分拆生效；或折舊年限縮短 → EPS 下修 >10%"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"加碼觸發：AdX 裁決明朗（結構 vs 行為）或回檔 $300-320 或 2027 capex 指引與 Cloud ROI 對得上","irr_base_pct":8.5,"ev5y_pct":51.0,"drift_watch_prior":{"dca_verdict":"進場","dca_role":"核心","signal":"A","val":"🟡","ma":"✅","trap":"🟢","moat_trend":"→","runway_post_y5":"🟢","asym_ratio":4.7,"ev5y_pct":51.0,"irr_base_pct":8.5,"max_dd_pct":-50.0,"bull_5y_price":718.0,"bear_5y_price":246.0,"p_bull_pct":30.0,"p_bear_pct":25.0,"rearm_trigger":"加碼觸發：AdX 裁決明朗（結構 vs 行為）或回檔 $300-320 或 2027 capex 指引與 Cloud ROI 對得上","price_at_dd":342.09,"archetype":"品質複利成長","cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"GOOGL","date":"2026-11-03","schema":"v15.0","contract":"v19","company_name":"Alphabet Inc."},"oneliner":"Cloud 年增 103%、利益率 36% 證明 AI 投資開始變現，但搜尋增速由 17% 降到 12%、單季自由現金流轉負，2027 年資本支出還要大增；股價 26 週跌 26% 後估值中性，成敗看 2028 年自由現金流能否轉正。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/GOOGL_20261103/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/GOOGL_20261103/scenario.json","answers":{"q1_business":{"verdict":"賺廣告主與企業 IT 預算的錢：搜尋廣告仍是最大利潤池，Cloud 已是第二支柱；錢卡在使用者查詢意圖與 AI 算力兩個節點，而算力這一端正在吃掉搜尋產生的現金。","reasoning":"Q3 營收 1,276 億美元，年增 25%；GAAP 營業利益率 31.8%，TTM 毛利率 60.9%。分部（Q3）：搜尋及其他 633 億美元（約 50%，+12%）、Cloud 307 億美元（約 24%，+103%，營業利益率 36.2%）、訂閱平台裝置 143 億美元（約 11%，+11%）、YouTube 廣告 112 億美元（約 9%，+9%）、Network 75 億美元（約 6%，+1%）。Services 營業利益 392 億美元，利益率 40.7%（Q2 為 41.8%）；Cloud 營業利益 111 億美元，占兩大部門營業利益約 22%。供需持久性：算力需求屬結構性持久，Cloud backlog 由 Q2 的 5,140 億美元增到 5,610 億美元，管理層稱供給受限會持續；廣告需求屬週期性，美國媒體廣告增速預測由 2026 年 15.6% 降到 2027 年 9.4%。產業態勢判為雙向拉鋸。競爭面，美國搜尋份額 12 個月降 3.1 個百分點，AI 模型商被列為競爭者；結構面，算力供不應求；其他結構變數方面，搜尋反壟斷補救仍在上訴，廣告科技案 2026-09 只判行為補救。單點依賴有兩處：TPU 全由台積電代工；Cloud backlog 有一部分與 Anthropic 相關，集中度數字事實表未涵蓋。公司未提供 Non-GAAP 營業利益，此項不適用。","fact_refs":["f_kpi0_gaap","f_kpi1_gaap","f_kpi2_gaap","f_kpi3_non_gaap","f_kpi6_google_cloud","f_kpi7_google_cloud","f_kpi8_google_cloud_backlog","f_kpi9_capex","f_kpi10","f_peer_googl_gross_margin_pct","f_earnings_recency"],"verdict_values":{"revenue_quality":"廣告約占營收七成，經常性高，沒有單一客戶占營收超過 10%。Cloud backlog 5,610 億美元提供能見度，約 55% 會在 24 個月內認列。TPU 系統銷售是硬體一次認列，品質低於 GCP 用量收入，公司也不揭露其利潤率。","unit_econ_note":"Q3 TAC 164 億美元，年增 10%，略低於廣告營收增速；其他營收成本 351 億美元，年增 32%，快於營收，來源是 TPU 硬體成本、折舊與內容成本。","archetype":{"primary":"品質複利成長","secondary":null,"confidence":"中","fingerprint":"高利益率廣告平台正轉向重資產算力供應商，資本密度兩年內急升"},"industry":{"clock_phase":"II","sd_verdict_source":"Q3 法說會：CEO 與 CFO 說明供給受限、Q4 擴大使用第三方算力；EMARKETER／IAB 對 2027 年廣告放緩的預測","bargaining":{"up":"上游議價力偏強：TPU 全由台積電代工，AI 加速器產能要搶；Q4 起動用第三方算力，橋接成本壓 Cloud 利益率；未來採購承諾 9,240 億美元","down":"下游分散：沒有單一客戶占營收超過 10%，廣告主依投報率投放；Cloud 端 backlog 部分與 Anthropic 相關，屬單點依賴","geo":"國際營收約占 52%，Q3 匯率是搜尋減速的最大因素"},"profit_pool_dir":"利潤池由連結式搜尋移往 AI 介面與算力層。Alphabet 兩端都有部位，但 AI 介面每查詢的變現仍低於傳統搜尋。","tam_table":[{"item":"全球搜尋廣告 2026（WARC）","value":"2,957 億美元，年增 14.2%；2027 年預測 +8.8%"},{"item":"全球廣告 2026（WARC）","value":"1.34 兆美元，+11.9%；Alphabet、Amazon、Meta 合占不含中國市場的 59.7%"},{"item":"美國網路廣告集中度（IAB/PwC）","value":"十家公司拿走 2025 年 84.1%，自 2022 年逐年上升"},{"item":"全球雲端基礎設施份額 Q3 2026（Synergy）","value":"Amazon 26%、Microsoft 19%、Google 16%"},{"item":"Google Cloud backlog","value":"5,610 億美元，約 55% 於 24 個月內認列"},{"item":"利潤池占比 5 年前對現在","value":"事實表未涵蓋"}]}}},"q2_moat":{"verdict":"護城河持平：Cloud 與模型層在擴大，搜尋的定價力在收縮，兩邊互相抵銷。","reasoning":"機制分兩塊。搜尋靠使用者習慣、預設分發與廣告主競價形成的雙邊網路效應；Cloud 靠自研 TPU 的全端成本優勢與多年期合約。同業投入資本報酬率事實表未涵蓋，方向改用份額與利益率代理。擴大的證據：Cloud 全球份額 16%（Amazon 26%、Microsoft 19%），Q3 營收年增 103%，利益率由 23.7% 升到 36.2%；Gemini 網頁流量份額上升，ChatGPT 降到 2023 年以來低點。收縮的證據：美國搜尋份額 12 個月由 87.28% 降到 84.17%，Bing 升到 10.48% 創新高；CBO 承認 AI Mode 變現較低，拖累 Q3 搜尋增速。TTM 營業利益率 33.3%，與 META 32.9%、AAPL 33.2% 相當，落後 MSFT 47.1%；FCF 利潤率 4.2% 是五家中第二低，差距擴大反映的是資本密度上升，不是定價力流失。執行力給 8：Gemini 4 與 TPU 領先，但 Gemini 3.5 Pro 時程失誤，Q4 還要靠第三方算力橋接。定價力給 8：算力供不應求，TAC 增速低於營收；搜尋端 AI Mode 的變現仍待證明。扣除 AI 介面分流這項生態攻擊後落在 B 級。當期報酬屬高利益率，但投入資本周轉率因資本支出而下滑，投入資本口徑事實表未涵蓋。","fact_refs":["f_peer_googl_gross_margin_pct","f_peer_googl_operating_margin_pct","f_peer_googl_fcf_margin_pct","f_peer_msft_gross_margin_pct","f_peer_msft_operating_margin_pct","f_peer_msft_fcf_margin_pct","f_peer_amzn_operating_margin_pct","f_peer_amzn_fcf_margin_pct","f_peer_aapl_operating_margin_pct","f_peer_aapl_fcf_margin_pct","f_peer_meta_gross_margin_pct","f_peer_meta_operating_margin_pct","f_peer_meta_fcf_margin_pct","f_kpi7_google_cloud","f_kpi9_capex"],"verdict_values":{"moat":{"mechanism":"搜尋＝使用習慣＋預設分發＋廣告主競價網路效應；Cloud＝自研 TPU 全端成本優勢＋多年期合約","execution":8,"pricing":8,"grade":"B","trend":"→","trend_evidence":"擴大面：Cloud 份額 16%，Q3 營收 +103%，利益率由 23.7% 升到 36.2%；Gemini 流量份額上升。收縮面：美國搜尋份額 12 個月由 87.28% 降到 84.17%，AI Mode 變現低於傳統搜尋，拖累 Q3 搜尋增速。沒有單一客戶占營收超過 10%，改以份額代理；搜尋份額下滑，所以不判擴大。","competitor_notes":[{"name":"MSFT","strategy_note":"TTM 營益率 47.1%、FCF 利潤率 17.3%，資本密度上升得比 GOOGL 慢；Azure 份額 19% 高於 Google Cloud 的 16%，是企業 AI 的直接對手。"},{"name":"AMZN","strategy_note":"雲端份額 26% 居首，TTM FCF 利潤率 −0.8%，同樣在大舉投資算力；對 Google Cloud 的威脅在價格與產能，不在技術。"},{"name":"AAPL","strategy_note":"TTM 營益率 33.2%，與 GOOGL 持平；它既是搜尋預設分發的夥伴，也在最新一代 TPU 上預訓練自家模型；Safari 搜尋量證詞是通路風險的來源。"},{"name":"META","strategy_note":"毛利率 81% 為五家最高，營益率 32.9% 與 GOOGL 相近；在廣告預算上直接競爭，同時與 Google 合作 TorchTPU。"}],"peer_na_reason":"同業投入資本報酬率與投入資本事實表未涵蓋，只有利潤率，因此以營業利益率與 FCF 利潤率代理。","threats":[{"level":"🔴","text":"AI 助理與代理型介面分流高意圖查詢，屬生態攻擊：模型商直接接觸使用者，AI 瀏覽器挑戰 Safari 與 Chrome 的預設通路；10-K 自承新進者可能提供更好的體驗。","p":"30%","evidence_refs":["substitute_technology#0","substitute_technology#1","substitute_technology#2","competitive_share_entrants#1","channel_business_model_shift#3"]},{"level":"🟡","text":"Bing 美國搜尋份額升到 10.48% 創新高，屬點對點競爭。","p":"20%","evidence_refs":["end_markets#3"]},{"level":"🟡","text":"AI 加速器產能爭奪：競爭者若先鎖定 GPU 與代工產能，Alphabet 的成本會上升、供給會受限。","p":"25%","evidence_refs":["competitive_share_entrants#2"]}],"roic_durability":{"quadrant":"高利益率×低周轉（周轉率因資本支出下滑中）","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者（免費查詢者）、決策者與付款者（廣告主）三個角色都成立：查詢成長率是近 5 年最高，AI Mode 查詢多為增量。Cloud 端付款者是企業與 AI 實驗室，backlog 5,610 億美元。客戶要解決的問題（找資訊、找客戶、要算力）不會消失，風險在 Google 的解法被替代，而不是需求消失。"},{"item":"決策層級","level":"🟡","text":"替代發生在單次查詢層級，其他產品「一鍵之遙」；美國搜尋份額 12 個月降 3.1 個百分點。Cloud 端轉換成本高：多年期合約，遷移需要改寫程式。TorchTPU 正在降低 PyTorch 移植的門檻，對 Google 是雙面刃。漲價後流失率與分客群續約率事實表未涵蓋。"},{"item":"價值鏈分配","level":"🟡","text":"廣告價值鏈向平台集中：十家公司拿走 2025 年美國網路廣告的 84.1%，TAC 增速低於營收。算力價值鏈則在上游收斂：TPU 全由台積電代工，AI 加速器產能要搶，Q4 動用第三方算力會壓低 Cloud 利益率。未來採購承諾 9,240 億美元，顯示上游議價力不弱。"},{"item":"社會容忍度","level":"🟡","text":"政治上限已經在起作用：搜尋案最終判決限制分發方式，並要求分享搜尋資料，雙方都已上訴；歐盟廣告科技罰款 30 億歐元仍在上訴，Q3 另支付 2018 年歐盟罰款 52 億美元。最壞的結構分拆已在 2026-09 被法院駁回，目前的約束是行為補救，所以判黃而不是紅。"}],"roiic":"約 18%（粗估，方向下滑）","reinvest_rate":"約 80%（淨額估計；毛額為 TTM 資本支出約 1,599 億美元 ÷ 營業現金流 1,796 億美元＝89%，折舊事實表未涵蓋）","endo_ceiling":14,"formula_note":"增量報酬：TTM 營業利益約 1,570 億美元（市值 ÷ 市銷率 7.38 得 TTM 營收約 4,713 億美元，× 33.3%），比 FY2024 的 1,124 億美元多約 446 億美元，除以 TTM 單年資本支出約 1,599 億美元，約 28%。這是未調整值，有三處偏差：一是稅前；二是分子為 FY2024 到 TTM 約七季的增量，分母只算最近一年的投入；三是分母用資本支出毛額，沒扣維持性支出。前兩項使報酬高估，第三項使報酬低估。稅率、前一年資本支出與折舊事實表都未涵蓋，三項都無法精算，18% 是判斷折減，不是算式結果。內生成長上限＝18% × 80% ≈ 14%。若不折減，上限＝28% × 80% ≈ 22%，高於共識 19.1%，所以「共識超出內生上限」取決於折減幅度，信心有限；這組數字只用來和共識成長比較，不作精算。"}}}},"q3_growth":{"verdict":"五年後跑道寬：搜尋已高滲透，但 Cloud（份額 16%、backlog 5,610 億美元）與外售 TPU 系統是有實據的第二、第三條曲線。","reasoning":"成長以量為主（查詢量、Cloud 用量、TPU 系統出貨），價為輔（算力稀缺），併購與回購的貢獻接近零：本季未提回購，Wiz 等併購約占市值 1%。共識三年 EPS 複合成長 19.1%（FY2025A 10.81 美元到 FY2028E 18.26 美元，Koyfin 快照，家數未收），但 FY2025A 與 FY2026E 都含持股未實現損益，FY2027E 的 15.14 美元反而低於 FY2026E。內生上限約 14%，缺口約 5 個百分點。缺口主要來自 Cloud 利益率擴張，以及 TPU 系統 2027 年放量帶來的營運槓桿；剩下的部分找不到來源，因此長期信心最高只給中。跑道方面，Cloud 份額 16%，市場總成長事實表未涵蓋，粗估 5–9 年；搜尋份額約 90%，已過高滲透。第二曲線有出處：TPU 系統外售（近 100 家客戶，與 Oracle、Crux AI 合作），Waymo 營運城市擴到 15 個。AI 曝險的分界年定在 2028：AI Mode 廣告全球化後，若 2028 年搜尋仍維持雙位數成長，AI 曝險就轉為淨加分。衰退信號亮了 2 項：美國搜尋份額縮減，自由現金流對淨利比連 2 年低於 0.75。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_kpi6_google_cloud","f_kpi8_google_cloud_backlog","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m"],"verdict_values":{"growth":{"driver_mix":"量為主、價為輔；併購與回購貢獻接近零","runway_years":"5–9（粗估）","runway_post_y5":"🟢","endo_ceiling_basis":"引用競爭優勢段的增量報酬率 × 再投資率，粗估 14%；共識三年 EPS 複合成長 19.1%，超出約 5 個百分點，主要歸因 Cloud 利益率擴張與 TPU 系統放量，其餘無法歸因","segments":[{"item":"Google 搜尋及其他","value":"Q3 633 億美元，年增 12%（Q2 +17%）"},{"item":"YouTube 廣告","value":"112 億美元，+9%"},{"item":"Network","value":"75 億美元，+1%"},{"item":"訂閱、平台與裝置","value":"143 億美元，+11%"},{"item":"Google Cloud","value":"307 億美元，+103%，營業利益率 36.2%"},{"item":"Google Services 營業利益","value":"392 億美元，利益率 40.7%（Q2 41.8%）"},{"item":"Other Bets","value":"營收 3.72 億美元，營業虧損 20 億美元"}],"decay_signals":["核心市占近 12 個月縮減：美國搜尋份額由 87.28% 降到 84.17%（WebFX）","自由現金流對淨利比連 2 年低於 0.75：FY2024 0.73、FY2025 0.55，TTM 進一步惡化"],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"資本配置轉向重資產：本季沒提回購，ATM 與強制可轉換特別股打開了增資的門，資本支出吃掉近九成營業現金流。","reasoning":"現金轉換：自由現金流對淨利 FY2024 為 0.73、FY2025 為 0.55（事實表年度財務史，yfinance 年度財報）；Q3 單季自由現金流 −91 億美元，TTM 197 億美元。Q3 的數字還包含 TPU 系統存貨增加（Cloud 執行長稱只在簽約後備料）與 52 億美元歐盟罰款支付。現金去向：TTM 營業現金流 1,796 億美元中，資本支出約 1,599 億美元，占 89%；股息每季每股 0.22 美元，殖利率 0.3%；併購 Wiz 約 295 億美元、Intersect 約 59 億美元（2026-03 完成）；Q3 法說未提回購，回購金額事實表未涵蓋。融資：2026-06 推出 400 億美元 ATM 與 6.25% 強制可轉換特別股，2026-08 發行 250 億美元優先債；長期債務 1,251 億美元，現金與有價證券 2,651 億美元（其中有價權益證券 904 億美元），淨現金約 1,148 億美元。CFO 在 2026-07-22 表示不打算再回股權市場，ATM 用於 SBC 稅負的部分除外。SBC 占營收 6.8%、占營業利益 21.3%。營運槓桿為正：營收 +25%，營業利益 +30%。債務到期結構與加權利率事實表未涵蓋。","fact_refs":["f_kpi4","f_kpi5_sbc_gaap","f_kpi9_capex","f_net_debt_m","f_dividend_yield_ttm","f_shares_diluted_m","f_ps_current"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":false,"passed":null,"input":"Wiz 與 Intersect 在 2026-03 完成，合計約 354 億美元，約占市值 1%；完成未滿一年，沒有已實現的增量報酬資料"},{"name":"buyback_yield","applicable":true,"passed":false,"input":"Q3 法說未提回購，另設 400 億美元 ATM 與強制可轉換特別股，回購收益率無法達到 10 年期殖利率加 2 個百分點"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"SBC 占營收 6.8% ÷ 市銷率 7.38 倍，約等於每年毛稀釋 0.9%，低於 1.5%；強制可轉換特別股的轉換股數事實表未涵蓋，計入後可能超標"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購撐：Wiz 與 Intersect 合計約占市值 1%，成長主要來自自建算力"}}}},"q5_valuation":{"verdict":"現價要求 FY2028E 每股盈餘 18.26 美元兌現，並維持 15–19 倍本益比；這點我大致相信。但用自由現金流計價偏貴，估值結論中性。","reasoning":"現價 282.98 美元。前瞻本益比：對 FY2026E 為 17.1 倍，對 FY2027E 為 18.7 倍，對 FY2028E 為 15.5 倍。FY2026E 分母含持股未實現損益，所以改以 FY2027E 錨定。PEG 約 0.98（18.7 ÷ 三年共識成長 19.1%）。trailing 本益比 14.77 倍低於四個年度端點的全部數值，但分母同樣受營業外損益影響；市銷率 7.38 倍位於 60.8 分位，EV/S 7.14 倍位於 55.5 分位，兩者都不是五年連續序列。前瞻 EV/S 6.73 倍。自由現金流殖利率約 0.6%（TTM 197 億美元 ÷ 市值約 3.48 兆美元）。短期上檔：FY2028E 18.26 美元 × 18 倍 ≈ 329 美元，+16.2%。中期上檔：FY2030E 基本情境 23.5 美元 × 18 倍 ≈ 423 美元，+49.5%。賣方平均目標價 391–433 美元，區間 220–515 美元，最高與最低相差 2.3 倍，未超過 2.5 倍。現價比均值低約 3 成，方向上支持估值不貴，但目標價多在 Q3 前定的，還沒反映 2027 年資本支出上調。同業前瞻本益比事實表未涵蓋，終端倍數無法附同業現值對照，改用自身年度端點校準。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_pe_current","f_pe_percentile","f_ps_current","f_ps_percentile","f_ev_s_current","f_ev_s_percentile","f_ev_s_fwd","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_fy1_pct","f_consensus_rev_fy2_pct","f_consensus_rev_fy3_pct","f_consensus_rev_3m_fy1_pct","f_dividend_yield_ttm","f_ev_m","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m"],"verdict_values":{"valuation":{"basis":"前瞻本益比（以 FY2027E 共識 EPS 錨定）","tier":"大型平台","peers":{"expanded":false,"reason":"事實表的同業對照只有利潤率，沒有同業前瞻本益比；本次估值結論不靠同業倍數，終端倍數以自身四個年度端點本益比與成長率校準"},"fwd_pe":17.1,"peg":0.98,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"本益比面偏便宜：FY2027E 18.7 倍、PEG 約 0.98，trailing 14.77 倍低於四個年度端點的全部數值。但分母有爭議，FY2026E 含持股未實現損益。市銷率 7.38 倍位於年度端點 60.8 分位，EV/S 位於 55.5 分位，自由現金流殖利率約 0.6%。三把尺互相抵銷，結論中性。五年連續分位事實表未涵蓋，只有四個年度端點，因此五年分位留空。","upside_short_pct":16.2,"upside_mid_pct":49.5,"denominator_disputed":true,"denominator_note":"FY2026E 共識 16.55 美元含 Q2 權益證券未實現利得，以及 Q3 SpaceX 未實現損失約 82 億美元；FY2027E 15.14 美元反而較低。FY1 共識在兩份快照間由 11.89 跳到 16.55，近 3 個月又由 20.58 降到 16.55，擺盪來自營業外損益而非營運。trailing 14.77 倍同樣受影響。改以 FY2027E 錨定，得 18.7 倍，便宜的論證不成立。"}}},"q6_how_wrong":{"verdict":"最可能看錯的是資本支出回報的時點：Cloud 已經證明需求，但自由現金流轉正一延再延，市場可能改用自由現金流而不是盈餘來計價。","reasoning":"歷史最大回撤事實表未涵蓋。回撤範圍推導：熊市路徑 FY2028E 每股盈餘低點 13.2 美元 × 13 倍 ≈ 172 美元，比現價低 39%；加上情緒超調，深端取 −45%；淺端取 −30%，大致對應熊市終點的跌幅。股價 26 週已跌 26%，RSI 24，部分下行已經發生。成長熄火壓力測試以 FY2028E 18.26 美元為三年後基數：之後成長 15%、給 20 倍，約 365 美元，通過；成長 10%、給 15 倍，約 274 美元，−3%，未過；成長 5%、給 12 倍，約 219 美元，−23%，未過。三項只過一項。空方最強的數字：自由現金流利潤率由 FY2022 的 21.2% 降到 TTM 4.2%，未來採購承諾 9,240 億美元。訴訟方面，搜尋案雙方上訴中，時程事實表未涵蓋；證券集體訴訟是原告主張，索賠金額未揭露。法說迴避題：2026-07-22 CFO 未回答 TPU 系統利潤率是否較低，2026-10-28 CFO 與 Cloud 執行長再次不拆分；Q3 也沒有給 2027 年資本支出數字。","fact_refs":["f_kpi4","f_week26_return_pct","f_rsi14","f_consensus_eps_fy3","f_peer_googl_fcf_margin_pct","f_price_at_dd"],"verdict_values":{"trap":{"verdict":"🟡","label":"中度：美國搜尋份額縮減、現金轉換率偏低，兩項亮起"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":16.55,"pe":17.1,"basis":"FY2026E 共識 EPS（Koyfin 2026-10-31 快照），終端倍數同樣以當年度 EPS 為分母；FY2026E 含持股未實現損益，所以起點倍數偏低"},"valuation_basis":"eps_pe","eps":{"bull":[16.2,19.8,23.5,27.3,31.5],"base":[15.14,18.26,20.8,23.5,26.3],"bear":[13.8,13.2,13.6,14.3,15.0]},"pe":{"bull":23,"base":18,"bear":13},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0.3,"net_buyback":-0.5},"second_stage":{"bull_cagr_pct":14,"base_cagr_pct":10},"max_dd":{"lo":-45,"hi":-30,"basis":"熊市路徑 FY2028E 每股盈餘低點 13.2 美元 × 熊市倍數 13 倍 ≈ 172 美元，比現價低 39%，加上情緒超調到 −45%；淺端 −30% 大致對應熊市終點跌幅 −31%。歷史最大回撤事實表未涵蓋；股價 26 週已跌 26%。","trigger_time":null},"basis":{"bull":"TPU 系統外售 2027 年起放量，AI Mode 廣告國際化後搜尋回到 12–15% 成長，2028 年後折舊增速低於營收，利益率擴張；終端 23 倍，低於四個年度端點中的較高值","base":"FY2027E、FY2028E 照共識 15.14、18.26 美元，之後成長 14%、13%、12% 逐年遞減；終端 18 倍，接近現價對 FY2027E 的 18.7 倍。淨回購為 −0.5%，因為回購未見、ATM 與強制可轉換特別股會稀釋，實際值事實表未涵蓋","bear":"AI 介面分流使搜尋零成長，2027–2028 年算力供過於求壓低 Cloud 利益率，折舊吃掉營業利益，EPS 停在 13–15 美元；終端 13 倍，取成長熄火到 5% 的倍數"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"美國搜尋份額 12 個月由 87.28% 降到 84.17%；有報導指網站點擊下降 8.9%，年輕用戶轉向 AI 聊天機器人；Q3 法說承認 AI Mode 變現較低；10-K 自承新進者可能提供更好的體驗。","assumption":"AI 介面帶來的增量查詢最終能以接近傳統搜尋的單價變現，而且 2027–2028 年算力不會供過於求。","consequence":"五年後虧掉一半最可能的故事是這樣：代理型助理把高意圖查詢移出搜尋框，搜尋營收轉為零成長；同期算力供過於求，引發 Cloud 價格戰，利益率回到 20% 以下，2027 年起的巨額折舊吃掉營業利益。結果每股盈餘停在 13–15 美元，倍數 10–13 倍，股價落在 130–195 美元。","ruling":"部分採納：寫進熊市路徑，熊市機率定為 30%。目前證據是增速放緩而不是衰退（Q3 搜尋 +12%，查詢量是 5 年最高），所以不調降基本情境。這條與唯一致命點在 Cloud 那一半重疊，搜尋那一半由第一項假設的門檻監測。","watch":"搜尋及其他營收年增、美國搜尋份額、AI Mode 國際廣告上線後的變現說明","evidence_refs":["substitute_technology#2","end_markets#3","competitive_share_entrants#1"],"fact_refs":["f_kpi7_google_cloud","f_kpi8_google_cloud_backlog"]},{"view":"論點失敗","evidence":"EMARKETER 預測美國媒體廣告 2026 年增 15.6%，2027 年只增 9.4%，部分來自世足賽與期中選舉；IAB 也提醒 2027 年放緩。Q3 法說已經點名世足賽預算提前到 Q2，使媒體娛樂類在 Q3 回落。","assumption":"AI 廣告工具帶來的投報率提升，足以抵銷廣告週期放緩。","consequence":"2027 年 YouTube 與 Network 增速再降，搜尋基期效應與週期疊加，第一項假設的 10% 門檻有被打穿的風險。","ruling":"採納為短期風險，但不當成結構性失敗：週期性放緩在預測範圍內，熊市路徑已經涵蓋；以 YouTube 廣告增速作為早期訊號。","watch":"YouTube 廣告年增、Network 年增、WARC 與 EMARKETER 對 2027 年預測的修正","evidence_refs":["supply_demand_durability#2"],"fact_refs":["f_kpi0_gaap"]},{"view":"論點成功但股東經濟變差","evidence":"自由現金流利潤率由 FY2022 的 21.2% 降到 TTM 4.2%；Q3 自由現金流 −91 億美元；未來採購承諾 9,240 億美元，尚未開始的租約與其他義務 1,520 億美元。資本支出指引上調後高於事前共識，2027 年還會大幅增加。本季未提回購，另有 400 億美元 ATM 與強制可轉換特別股。","assumption":"資本支出強度在 2028 年後回落，自由現金流隨折舊回收而回升。","consequence":"Cloud 與 AI 都贏了，但每股自由現金流多年不成長；回購停擺再加上稀釋，股東拿到的是更大的公司，而不是更多的每股現金。市場一旦改用自由現金流殖利率定價，倍數就會壓縮。","ruling":"採納為主要約束。資本回報假設的門檻改為 2028 全年自由現金流轉正，未達就減碼至半倉；2027-02 資本支出指引公布前不加到滿。","watch":"季度自由現金流、資本支出占營業現金流比、稀釋後股數、TPU 系統存貨","evidence_refs":["capital_markets_pricing#2"],"fact_refs":["f_kpi4","f_kpi9_capex","f_peer_googl_fcf_margin_pct","f_kpi5_sbc_gaap"]},{"view":"價格已反映太多","evidence":"FY2027E 共識 EPS 15.14 美元低於 FY2026E 的 16.55 美元，FY1 共識近 3 個月由 20.58 下修到 16.55；FY2028E 共識 18.26 美元隱含年增 21%。以 FY2027E 計，本益比 18.7 倍；賣方平均目標價 391–433 美元多是 Q3 前的資料。","assumption":"FY2028E 每股盈餘 18.26 美元能兌現。","consequence":"若 2027 年的折舊與第三方算力成本使 FY2028E 再下修 15%，現價對應約 18 倍，就不再便宜。","ruling":"反駁：trailing 本益比低於四個年度端點全部，市銷率位於中段，26 週已跌 26%，股價沒有反映太多。但以自由現金流計價偏貴，所以估值結論定為中性，不是便宜。","watch":"FY2027E、FY2028E 共識 EPS 的修正方向","evidence_refs":[],"fact_refs":["f_fwd_pe_latest","f_pe_percentile","f_ps_percentile","f_consensus_rev_3m_fy1_pct","f_consensus_eps_fy2"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 342.09 → 本次 282.98（-17.3%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=342.09","side_b":"本次 price_at_dd=282.98","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]裁決由 dd_decision.py 機械路由：前份 進場 → 本次 觀望","cause":"新證據","prior_field":["dca_verdict"],"side_a":"前份 dca_verdict=進場","side_b":"本次 dca_verdict=觀望","ruling":"裁決是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。沒有單一輸入能還原，屬多欄共同：訊號 A→B、均線 ✅→🟡、陷阱燈 🟢→🟡。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]角色由 dd_decision.py 機械路由：前份 核心 → 本次 追蹤","cause":"新證據","prior_field":["dca_role"],"side_a":"前份 dca_role=核心","side_b":"本次 dca_role=追蹤","ruling":"角色是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。沒有單一輸入能還原，屬多欄共同：訊號 A→B、均線 ✅→🟡、陷阱燈 🟢→🟡。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 342.09 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 342.09 美元：Bull 價 718、Bear 價 246，五年期望值 +51.0%，基準年化 8.5%，不對稱比 4.7","side_b":"本次情境、股價仍用 342.09 美元：Bull 價 724.5、Bear 價 195，五年期望值 +32.3%，基準年化 6.7%，不對稱比 2.17","ruling":"先換情境、股價不動：五年期望值少 18.7 個百分點，基準年化少 1.8 個百分點。不對稱比由 4.7 變為 2.17。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 342.09 美元：五年期望值 +32.3%，基準年化 6.7%，不對稱比 2.17","side_b":"本次情境、股價 282.98 美元：五年期望值 +60.0%，基準年化 10.8%，不對稱比 4.18","ruling":"再換股價、情境不動：起點價下跌 17.3%，五年期望值多 27.6 個百分點，基準年化多 4.1 個百分點，不對稱比由 2.17 升到 4.18。合計五年期望值比前份多 9.0 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"陷阱風險與整體評等下修","cause":"新證據","prior_field":["signal","trap"],"side_a":"前份：評等 A，陷阱風險低（當時股價 342.09 美元）","side_b":"本次：評等 B，陷阱風險中。新證據包括 Q3 自由現金流 −91 億美元，FY2024 與 FY2025 自由現金流對淨利分別為 0.73、0.55，美國搜尋份額 12 個月降 3.1 個百分點，護城河等級評為 B","ruling":"採 B 側：兩項衰退信號都有出處，方向一致，評等下修一級；護城河方向沒有轉弱，所以不再往下調","evidence_level":"公司財報＋第三方份額資料","settle_metric":"2027 年季度自由現金流、美國搜尋份額","if_then":["若 2027 Q2 起季度自由現金流連 2 季轉正，且美國搜尋份額回到 86% 以上，則評等回升並加碼至目標部位","若美國搜尋份額跌破 80%，則減碼三分之一"],"evidence_refs":["end_markets#3"]},{"axis":"護城河方向、成長跑道與公司類型","cause":"新證據","prior_field":["moat_trend","runway_post_y5","archetype","cycle_position"],"side_a":"前份：護城河持平，五年後跑道寬，類型為品質複利成長，非循環股","side_b":"本次：Cloud 營收 +103%、backlog 增到 5,610 億美元、Gemini app 達 10 億用戶，屬擴大證據；AI Mode 變現較低、美國份額下滑，屬收縮證據。兩邊抵銷，四欄維持不變；類型信心給中，因為資本密度急升使公司更像算力供應商","ruling":"維持：新證據兩個方向都有，淨方向不足以改判。跑道寬的依據由單看 backlog 改為 backlog 加外售 TPU 系統","evidence_level":"公司財報＋法說","settle_metric":"Cloud backlog、美國搜尋份額","if_then":["若 Cloud backlog 連 2 季下降，則跑道判斷降為中並停止加碼"],"evidence_refs":[]},{"axis":"估值結論與回撤範圍","cause":"價格變動","prior_field":["val","max_dd_pct"],"side_a":"前份：股價 342.09 美元，估值中性，最大回撤 −50%","side_b":"本次：股價 282.98 美元，跌 17%。估值仍判中性：FY2027E 本益比 18.7 倍、PEG 約 0.98 偏便宜，但分母有爭議，自由現金流殖利率約 0.6%。最大回撤範圍為 −30% 到 −45%，因為 26 週已跌 26%","ruling":"股價下跌的效果被分母爭議與自由現金流轉負抵銷，估值結論不變；回撤深端由 −50% 收窄到 −45%，因為部分下行已經發生。現在就買的最強論證：營業利益仍年增 30%，Cloud 利益率 36%，淨利下滑來自 SpaceX 持股未實現損失，RSI 24 已超賣","evidence_level":"市場價格＋共識預估","settle_metric":"FY2027E 共識 EPS 修正方向","if_then":["若股價跌到 230 美元以下而搜尋年增仍 ≥10%，則分批反買，每次三分之一","若 FY2027E 共識 EPS 再下修超過 10%，則停止加碼"],"evidence_refs":[]},{"axis":"情境機率與裁決重算","cause":"方法變動","prior_field":["p_bull_pct","p_bear_pct"],"side_a":"前份：牛市 30%，熊市 25%；裁決為進場","side_b":"本次：牛市 25%，基本 45%，熊市 30%。共識三年 EPS 複合成長 19.1% 超出內生上限約 14%，熊市機率下限因此提高到 30%；裁決與部位角色依本次輸入重算","ruling":"採 B 側：共識成長超出內生上限，缺口只有部分能歸因於利益率擴張，熊市機率必須上調","evidence_level":"方法規則＋共識預估","settle_metric":"2027 年 Cloud 營業利益率與全年自由現金流","if_then":["若 2027 全年 Cloud 利益率 ≥35% 且自由現金流轉正，則熊市機率回到 25%"],"evidence_refs":[]},{"axis":"加碼條件改寫","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"加碼觸發：AdX 裁決明朗（結構 vs 行為）或回檔 $300-320 或 2027 capex 指引與 Cloud ROI 對得上","side_b":"加碼：2027-02 法說後 Cloud backlog 季增 ≥500 億美元且 Cloud 營業利益率 ≥30%；或股價 ≤230 美元而搜尋年增仍 ≥10%","ruling":"舊加碼條件三項中已有兩項發生：2026-09 廣告科技案法院駁回結構分拆，只判行為補救；股價已低於 300 美元。剩下的資本支出與 Cloud 回報條件保留並量化，另加價格條件","evidence_level":"10-Q 法律事項＋市場價格","settle_metric":"2027-02 資本支出指引、Cloud backlog","if_then":["若兩項加碼條件都未達成而資本支出指引超過 3,000 億美元，則停止加碼"],"evidence_refs":["regulatory_antitrust#1","major_events#2"]},{"axis":"Single Thing 設定","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設唯一致命點（空值）","side_b":"2027 年 Cloud 營收年增跌破 40%，而同年資本支出超過 3,000 億美元","ruling":"前份格式沒有要求，本次補設。選這一項是因為它同時打穿 Cloud 與資本回報兩個假設；一旦發生就減碼至半倉","evidence_level":"方法變動","settle_metric":"2027 全年 Cloud 年增與資本支出","if_then":["若 2028-02 確認發生，則減碼至半倉；若同時美國搜尋份額低於 80%，則清倉"],"evidence_refs":[]},{"axis":"減碼與清倉門檻設定","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設（空值）","side_b":"搜尋及其他營收連 2 季年增 <8%；Cloud 利益率連 2 季 <25%；2028 全年自由現金流 ≤0；美國搜尋份額 <80%；Cloud backlog 連 2 季季減","ruling":"前份只有警戒指標，沒有門檻，本次補上。任一項觸發就減碼三分之一，三項以上同時觸發則清倉","evidence_level":"方法變動","settle_metric":"上列五項指標","if_then":["任一項觸發則減碼三分之一","三項以上同時觸發則清倉"],"evidence_refs":[]},{"axis":"資本回報假設的時點","cause":"新證據","prior_field":["H3"],"side_a":"FCF 於 ~2027Q1 越過谷底；漂移觸發：2027 全年 FCF 仍負 + Cloud OM 回落","side_b":"2028 全年自由現金流轉正且 Cloud 營業利益率 ≥30%；2028 全年仍 ≤0 即反轉","ruling":"Q3 自由現金流 −91 億美元，CFO 說 2027 年資本支出會大幅增加，TPU 系統存貨要先付現，2027 年轉正已不實際，門檻延後一年。只延這一次，再延就視為假設失敗","evidence_level":"公司財報＋法說","settle_metric":"2028 全年自由現金流","if_then":["若 2028 全年自由現金流仍 ≤0，則減碼至半倉"],"evidence_refs":["capital_markets_pricing#2"]},{"axis":"反壟斷風險門檻","cause":"新證據","prior_field":["R3"],"side_a":"強制分拆生效；或折舊年限縮短 → EPS 下修 >10%","side_b":"搜尋案上訴維持資料分享與分發限制，且美國搜尋份額跌破 80%","ruling":"2026-09 廣告科技案法院駁回 DOJ 的結構分拆，改判互通、資料存取與競價行為補救，結構分拆的尾部風險已經移除，風險重心轉到搜尋案補救對份額的影響。伺服器折舊年限目前為 6 年，沒有縮短，改由資本回報條目監測","evidence_level":"10-Q 法律事項＋10-K","settle_metric":"搜尋案上訴判決、美國搜尋份額","if_then":["若上訴維持補救且美國搜尋份額跌破 80%，則減碼三分之一"],"evidence_refs":["regulatory_antitrust#1","major_events#2"]},{"axis":"資本支出回報：管理層稱報酬高於資金成本，現金流卻轉負","cause":"新證據","prior_field":null,"side_a":"CFO（2026-10-28）：整個投資週期 ROIC 會明顯高於資金成本；Cloud 營業利益年增超過 3 倍，利益率 36.2%，今年到目前為止 AI 營收達數百億美元","side_b":"Q3 自由現金流 −91 億美元，TTM 197 億美元；未來採購承諾 9,240 億美元；2027 年資本支出會大幅增加，單一來源報導將超過 3,000 億美元；TPU 系統利潤率連兩季拒答","ruling":"性質可調和（時點差異），但要到 2028 年報才能裁決。先選 B 側作為部位約束，理由是報酬目前只有管理層口頭保證，沒有可驗證的增量報酬數字，而現金流出已是事實。硬數據點：2028 全年自由現金流與 Cloud 營業利益率。現在就賣的最強論證：資本密度永久上升，回購停擺且開始增資，0.6% 的自由現金流殖利率沒有安全邊際。反駁：營業利益仍年增 30%，現金流轉負的一部分是已簽約的 TPU 存貨與一次性罰款","evidence_level":"公司財報＋管理層說法","settle_metric":"2028 全年自由現金流；Cloud 營業利益率","if_then":["若 2027-02 指引資本支出超過 3,000 億美元，且 Cloud backlog 季增低於 300 億美元，則停止加碼並把部位上限降到原目標一半","若 2027 全年 Cloud 年增 ≥50% 且利益率 ≥30%，則加碼至目標部位","反向：若 2028 全年自由現金流仍 ≤0，則減碼至半倉"],"evidence_refs":["capital_markets_pricing#2"]},{"axis":"查詢量創五年新高，搜尋營收增速卻放緩","cause":"新證據","prior_field":null,"side_a":"CEO（2026-10-28）：查詢年成長率是近 5 年最高，AI Mode 查詢大多是增量","side_b":"搜尋及其他營收增速由 Q2 的 +17% 降到 Q3 的 +12%；CBO 承認 AI Mode 變現較低是原因之一。CFO 預告 Q4 還會受約 2 點基期效應與匯率拖累，而國際營收約占 52%","ruling":"可調和（程度差異）：查詢量與每查詢變現走相反方向，淨效果仍是正成長。管理層把放緩主要歸因於匯率、垂直產業與基期，屬一次性歸因，不採信也不否定，先標為未證、監測。2027 Q1 基期效應消失後，若搜尋年增連 2 季低於 10%，一次性歸因即被證偽","evidence_level":"管理層說法＋分部營收","settle_metric":"2027 Q1–Q2 搜尋及其他營收年增","if_then":["若 2027 Q1、Q2 搜尋年增都低於 10%，則停止加碼並把熊市機率上調到 35%","若 AI Mode 國際廣告上線後 2027 Q1 搜尋年增回到 13% 以上，則維持部位，視為變現落差收斂"],"evidence_refs":["customer_concentration_credit#2","supply_demand_durability#2"]},{"axis":"管理層前後說法：Q2 預告 Cloud 利益率承壓","cause":"新證據","prior_field":null,"side_a":"CFO（2026-07-22）：Q3 擴大第三方容量會使 Cloud 營業利益率承壓","side_b":"Q3 Cloud 利益率反而升到 36.2%；CFO（2026-10-28）說明第三方算力直到 Q3 最後才上線，壓力移到 Q4","ruling":"可調和：只是時點延後，不是預測錯誤。Q4 利益率才是真正的檢驗，Q3 的高利益率不能外推","evidence_level":"法說逐字稿","settle_metric":"Q4 2026 Cloud 營業利益率","if_then":["若 Q4 Cloud 利益率仍 ≥30%，則 Cloud 假設維持不變","若 Q4 Cloud 利益率跌破 25%，則停止加碼，直到 2027 Q1 回升"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"搜尋及其他營收 TTM 年增跌破 10%","type":"假設驗證","maps_to":"H1","metric":"搜尋及其他營收年增（TTM）","threshold":"低於 10%，連 2 季","action":"停止加碼；連 3 季則減碼三分之一","source_freq":"公司季報，每季","date":"2027-04","evidence_refs":[]},{"n":2,"text":"Cloud 年增或營業利益率跌破 30%","type":"假設驗證","maps_to":"H2","metric":"Google Cloud 營收年增、營業利益率","threshold":"任一項低於 30%，連 2 季","action":"減碼三分之一","source_freq":"公司季報，每季","date":"2027-04","evidence_refs":[]},{"n":3,"text":"2028 全年自由現金流沒有轉正","type":"假設驗證","maps_to":"H3","metric":"全年自由現金流","threshold":"≤0","action":"減碼至半倉","source_freq":"公司年報，每年","date":"2029-02","evidence_refs":[]},{"n":4,"text":"2027 年 Cloud 年增跌破 40%，而同年資本支出超過 3,000 億美元","type":"Single Thing","maps_to":"Single Thing","metric":"Cloud 營收年增；全年資本支出","threshold":"Cloud 低於 40%，且資本支出超過 3,000 億美元","action":"減碼至半倉並重跑完整研究","source_freq":"公司年報，每年","date":"2028-02","evidence_refs":[]},{"n":5,"text":"2027 年資本支出指引大幅上調，backlog 增速沒跟上","type":"風險","maps_to":"R2","metric":"2027 年資本支出指引；Cloud backlog 季增","threshold":"指引超過 3,000 億美元，且 backlog 季增低於 300 億美元","action":"停止加碼","source_freq":"Q4 法說會","date":"2027-02","evidence_refs":["capital_markets_pricing#2","competitive_share_entrants#2"]},{"n":6,"text":"搜尋反壟斷上訴維持資料分享與分發限制","type":"風險","maps_to":"R3","metric":"上訴判決內容；美國搜尋份額","threshold":"補救維持，且美國搜尋份額低於 80%","action":"減碼三分之一","source_freq":"法院判決；WebFX 與 StatCounter 月資料","date":null,"evidence_refs":["regulatory_antitrust#0","lawsuit_class_action#1"]},{"n":7,"text":"證券集體訴訟（Gemini 3.5 Pro 時程揭露）取得集體認證","type":"風險","maps_to":"無對應假設（管理層揭露的可信度）","metric":"加州北區聯邦法院 26-cv-11290 案程序進度","threshold":"集體認證通過，且出現 SEC 調查","action":"減碼一半；只有集體認證則不動","source_freq":"法院案卷、8-K","date":null,"evidence_refs":["major_events#1","lawsuit_class_action#0"]},{"n":8,"text":"TPU 交付被代工、關稅或出口管制卡住","type":"風險","maps_to":"R4","metric":"管理層對 TPU 系統交付與第三方算力的說明","threshold":"交付延後一季以上","action":"停止加碼","source_freq":"季報法說，每季","date":null,"evidence_refs":["geo_supply_chain#0","geo_supply_chain#1","geo_supply_chain#2","reg_tariff_export#0","competitive_share_entrants#2"]},{"n":9,"text":"2027 年廣告週期放緩壓到 YouTube 與 Network","type":"風險","maps_to":"R1","metric":"YouTube 廣告年增","threshold":"低於 5%，連 2 季","action":"停止加碼","source_freq":"公司季報，每季","date":"2027-07","evidence_refs":["supply_demand_durability#2","customer_concentration_credit#2"]},{"n":10,"text":"股價跌到 FY2027E 約 15 倍，基本面未破","type":"估值rearm","maps_to":"H1","metric":"股價；搜尋及其他營收年增","threshold":"股價 ≤230 美元，且搜尋年增 ≥10%","action":"分批反買，每次三分之一","source_freq":"每日股價、季報","date":null,"evidence_refs":[]},{"n":11,"text":"資本支出與 Cloud 回報對得上","type":"加碼","maps_to":"H3","metric":"Cloud backlog 季增、Cloud 營業利益率","threshold":"backlog 季增 ≥500 億美元，且利益率 ≥30%","action":"加碼至目標部位","source_freq":"Q4 法說會","date":"2027-02","evidence_refs":[]},{"n":12,"text":"Q4 2026 法說會後複審","type":"複審日期","maps_to":null,"metric":"2027 年資本支出指引、Cloud backlog、Q4 Cloud 利益率","threshold":"法說會公布日","action":"重跑完整研究","source_freq":"Q4 法說會","date":"2027-02","evidence_refs":[]}],"kill_metrics":[{"metric":"搜尋及其他營收單季年增率","bear_threshold":"連 2 季低於 8%","window":"2027 Q1–Q4","source":"公司季報分部營收","last_status":"ok"},{"metric":"Google Cloud 營業利益率","bear_threshold":"連 2 季低於 25%","window":"2027 全年","source":"公司季報 Cloud 分部損益","last_status":"ok"},{"metric":"Alphabet 全年自由現金流","bear_threshold":"2028 全年 ≤0","window":"FY2028","source":"公司年報現金流量表","last_status":"warning"},{"metric":"美國搜尋份額","bear_threshold":"低於 80%","window":"滾動 12 個月","source":"WebFX、StatCounter","last_status":"warning"},{"metric":"Google Cloud backlog","bear_threshold":"連 2 季季減","window":"2027 全年","source":"季度法說會 CFO 揭露","last_status":"ok"}],"evidence_dismissed":[],"action_conditions":{"rearm_trigger":"加碼：2027-02 法說後 Cloud backlog 季增 ≥500 億美元且 Cloud 營業利益率 ≥30%；或股價 ≤230 美元而搜尋年增仍 ≥10%","exec_line":"現價不建倉，先列追蹤：FY2026E 每股盈餘含持股未實現損益，估值分母有爭議，現價便宜與否無法判定。建倉條件二擇一：2027-02 法說後 Cloud backlog 季增 ≥500 億美元且 Cloud 營業利益率 ≥30%，可一次建到目標部位；或股價 ≤230 美元而搜尋年增仍 ≥10%，分三批進場，每批三分之一。"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場把 Q3 淨利下滑與單季自由現金流轉負讀成獲利力轉弱。實際上淨利下滑來自 SpaceX 持股未實現損失約 82 億美元，屬營業外，營業利益仍年增 30%；自由現金流轉負有一部分來自已簽約的 TPU 系統存貨，以及 52 億美元歐盟罰款的一次性支付。不過市場對資本密度上升的擔憂是對的，所以只認定市場部分看錯。","momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":null,"wait_for_price_condition":null},"decision_out":{"role":"追蹤","row_hit":"8(val爭議)","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場把 Q3 淨利下滑與單季自由現金流轉負讀成獲利力轉弱。實際上淨利下滑來自 SpaceX 持股未實現損失約 82 億美元，屬營業外，營業利益仍年增 30%；自由現金流轉負有一部分來自已簽約的 TPU 系統存貨，以及 52 億美元歐盟罰款的一次性支付。不過市場對資本密度上升的擔憂是對的，所以只認定市場部分看錯。"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟢', val='🟡', moat_trend='→', week26=-26.09, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position=None, moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈機械讀數判定不可用，baseline rows 8/9/9b/10 的估值條件視為不可判 → 落 row8 觀望（保守方向）","hit":true,"basis":"val_denominator_disputed=True, val(機械讀數)='🟡'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":null,"requires_critic":[],"verdict":"觀望"},"thesis":{"H":[{"id":"H1","text":"搜尋在 AI 介面轉型中守住變現：AI Overviews 與 AI Mode 廣告擴大到國際市場與多輪對話後，搜尋營收增速維持雙位數","2y":"2027 全年搜尋及其他營收年增 ≥10%，基期效應消失後的 2027 Q1–Q2 也不低於 10%","5y":"搜尋仍是集團最大利潤池，代理型購物能用廣告或交易抽成變現","10y":null,"threshold":"搜尋及其他營收 TTM 年增 ≥10%（Q3 單季 +12%，Q2 +17%）","source":"公司季報分部營收；法說會對 AI Mode 廣告擴張與變現的說明","drift_rule":"TTM 增速連 2 季低於門檻且偏離 ≥5% 為削弱，連 3 季偏離 ≥10% 為反轉"},{"id":"H2","text":"Google Cloud 的成長與利益率同時守住，算力 backlog 按時程轉成營收，成為與搜尋並列的利潤支柱","2y":"2027 全年 Cloud 年增 ≥30%，營業利益率 ≥30%（含第三方算力成本）","5y":"Cloud 營業利益接近 Services 營業利益的一半，TPU 系統外售成為穩定收入","10y":null,"threshold":"Cloud 年增 ≥30%、營業利益率 ≥30%、backlog 不低於 5,610 億美元","source":"公司季報 Cloud 分部；法說會揭露的 backlog 與認列時程（約 55% 於 24 個月內）","drift_rule":"任一指標連 2 季低於門檻且偏離 ≥5% 為削弱，連 3 季偏離 ≥10% 為反轉"},{"id":"H3","text":"AI 基建投資賺回資金成本：2027 年資本支出大增後，2028 年自由現金流轉正並開始回升","2y":"2028 全年自由現金流大於 0，資本支出占營業現金流降到 80% 以下","5y":"自由現金流利潤率回到 12% 以上","10y":null,"threshold":"2028 全年自由現金流大於 0，且 Cloud 營業利益率 ≥30%","source":"公司年報現金流量表；法說會資本支出指引（2027 年數字在 2027-02 Q4 法說公布）","drift_rule":"TTM 自由現金流連 4 季低於上年同期為削弱；2028 全年仍 ≤0 即反轉"}],"R":[{"id":"R1","text":"搜尋每查詢變現結構性下滑：AI Mode 單價偏低，AI 助理與 AI 瀏覽器分流高意圖查詢，美國份額被 Bing 侵蝕","h_ref":"H1","clock":"🔥","threshold":"搜尋及其他營收單季年增連 2 季低於 8%，或美國搜尋份額低於 80%","evidence_refs":["competitive_share_entrants#1","substitute_technology#0","substitute_technology#1","substitute_technology#2","end_markets#3","channel_business_model_shift#3"]},{"id":"R2","text":"AI 資本支出過度建置：2027 年資本支出大增，而 Cloud 需求或價格轉弱，折舊與第三方算力成本壓低利益率，自由現金流轉正延後","h_ref":"H3","clock":"🔥","threshold":"2027 年資本支出超過 3,000 億美元且 Cloud backlog 季增低於 300 億美元，或 Cloud 利益率連 2 季低於 25%","evidence_refs":["capital_markets_pricing#2","competitive_share_entrants#2"]},{"id":"R3","text":"搜尋反壟斷補救：上訴若維持分發限制，以及向競爭者分享搜尋資料、提供 syndication，使用者的轉換門檻會下降","h_ref":"H1","clock":"🐢","threshold":"上訴判決維持補救，且美國搜尋份額低於 80%","evidence_refs":["regulatory_antitrust#0","lawsuit_class_action#1"]},{"id":"R4","text":"AI 晶片供應鏈單點：TPU 全由台積電代工，部分元件只有單一來源，地緣衝突、關稅或出口管制可能卡住交付","h_ref":"H2","clock":"🐢","threshold":"管理層說明 TPU 系統交付延後一季以上，或第三方算力使用延長到 2027 下半年","evidence_refs":["geo_supply_chain#0","geo_supply_chain#1","geo_supply_chain#2","reg_tariff_export#0"]},{"id":"R5","text":"Cloud 客戶集中：backlog 增量有一部分來自單一 AI 實驗室（Anthropic），TPU 系統存貨依簽約備料，大客戶融資轉弱會同時打到 backlog 與存貨","h_ref":"H2","clock":"⚡","threshold":"backlog 季減，或管理層揭露主要客戶合約調整","evidence_refs":["end_markets#2"]}],"single_thing":{"description":"2027 年 Cloud 營收年增跌破 40%，而同年資本支出超過 3,000 億美元","why_fatal":"資本支出約為 2026 年的 1.5 倍。若 Cloud 增速同時腰斬，新增折舊與第三方算力成本會使 FY2028E 每股盈餘低於共識的 18.26 美元，自由現金流轉正延到 2029 年以後。資本回報與 Cloud 兩個假設會同時失效，倍數也失去現金支撐。","if_happens":"2028-02 Q4 法說確認後減碼至半倉，並重跑完整研究；若同時美國搜尋份額低於 80%，則清倉","how_monitor":"2027-02 Q4 法說的資本支出指引；每季 Cloud 年增、backlog、資本支出與折舊","probability":"約 15%：backlog 5,610 億美元中約 55% 會在 24 個月內認列，加上 TPU 系統 2027 年放量，Cloud 增速要跌破 40%，需要大客戶縮單或價格戰"}},"appendix_a":{"growth_durability":6,"quality_score":6,"ai_risk":"🟡","long_term_confidence":"中","fpe_fy2":18.69,"peg_fy2":0.98,"stress":{"pass":1,"total":3}},"eps_meta":{"base_eps_path":{"FY2025A":10.81,"FY2026E":16.55,"FY2027E":15.14,"FY2028E":18.26},"fy_end_month":12,"eps_basis":"GAAP 稀釋 EPS；FY2025A 淨利 1,322 億美元高於營業利益約 1,290 億美元，FY2026E 也含持股未實現損益（營業外）；推定 FY2027E 起的共識不含市值變動"},"catalysts":[{"date":"2027-02","date_precision":"month","type":"guidance","event":"Q4 2026 法說會：2027 年資本支出指引與 Cloud backlog","impact":"高","watch":"資本支出是否超過 3,000 億美元，backlog 季增是否 ≥500 億美元"},{"date":"2026-Q4","date_precision":"quarter","type":"product","event":"AI Mode 廣告擴展到國際市場，美國推出多輪對話廣告","impact":"中","watch":"Q4 與 2027 Q1 搜尋增速能否回升"},{"date":null,"date_precision":null,"type":"regulatory","event":"搜尋反壟斷案上訴判決（Alphabet 與 DOJ、各州都已上訴）","impact":"高","watch":"資料分享、syndication 與分發限制是否維持"},{"date":"2027-Q1","date_precision":"quarter","type":"capacity","event":"TPU 系統銷售 2027 年放量，第三方算力使用擴大","impact":"中","watch":"Cloud 利益率在第三方算力成本下能否守住 30%"},{"date":"2026-Q4","date_precision":"quarter","type":"product","event":"Gemini 代理功能推向 Gemini app 的 10 億用戶","impact":"中","watch":"代理型查詢能否帶來廣告或交易抽成"}]}
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
