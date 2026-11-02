你是 DD 管線 v20 的判斷層閘（gate），標的 SIMO（20261103）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（47 條）
- `f_kpi0_gaap`（q1_business）｜營收（GAAP）＝560.2 US$M｜期間與口徑：Q3 2026（季末 2026-09-30，公告 2026-10-29 新聞稿日期；earnings_recency 記 10-28 盤後）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 6-K Ex.99.1 新聞稿 https://www.sec.gov/Archives/edgar/data/0001329394/000119312526436478/d135156dex991.htm（numbers.latest_quarter_kpis.items[0]，as_of Q3 2026（季末 2026-09-30，公告 2026-10-29 新聞稿日期；earnings_recency 記 10-28 盤後））
  - 註記：查無（consensus_revision 僅有 EPS 預估修正，無營收／利益率共識）
- `f_kpi1_non_gaap`（q1_business）｜Non-GAAP 營業利益＝180.0 US$M｜期間與口徑：Q3 2026（季末 2026-09-30，公告 2026-10-29 新聞稿日期；earnings_recency 記 10-28 盤後）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 6-K Ex.99.1 新聞稿 https://www.sec.gov/Archives/edgar/data/0001329394/000119312526436478/d135156dex991.htm（numbers.latest_quarter_kpis.items[1]，as_of Q3 2026（季末 2026-09-30，公告 2026-10-29 新聞稿日期；earnings_recency 記 10-28 盤後））
  - 註記：查無（consensus_revision 僅有 EPS 預估修正，無營收／利益率共識）
- `f_kpi2_non_gaap`（q1_business）｜Non-GAAP 營業利益率＝32.1 %｜期間與口徑：Q3 2026（季末 2026-09-30，公告 2026-10-29 新聞稿日期；earnings_recency 記 10-28 盤後）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 6-K Ex.99.1 新聞稿 https://www.sec.gov/Archives/edgar/data/0001329394/000119312526436478/d135156dex991.htm（numbers.latest_quarter_kpis.items[2]，as_of Q3 2026（季末 2026-09-30，公告 2026-10-29 新聞稿日期；earnings_recency 記 10-28 盤後））
  - 註記：查無（consensus_revision 僅有 EPS 預估修正，無營收／利益率共識）
- `f_kpi3_gaap`（q1_business）｜GAAP 營業利益＝162.6 US$M｜期間與口徑：Q3 2026（季末 2026-09-30，公告 2026-10-29 新聞稿日期；earnings_recency 記 10-28 盤後）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 6-K Ex.99.1 新聞稿 https://www.sec.gov/Archives/edgar/data/0001329394/000119312526436478/d135156dex991.htm（numbers.latest_quarter_kpis.items[3]，as_of Q3 2026（季末 2026-09-30，公告 2026-10-29 新聞稿日期；earnings_recency 記 10-28 盤後））
  - 註記：查無（consensus_revision 僅有 EPS 預估修正，無營收／利益率共識）
- `f_kpi4_gaap`（q1_business）｜GAAP 營業利益率＝29.0 %｜期間與口徑：Q3 2026（季末 2026-09-30，公告 2026-10-29 新聞稿日期；earnings_recency 記 10-28 盤後）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 6-K Ex.99.1 新聞稿 https://www.sec.gov/Archives/edgar/data/0001329394/000119312526436478/d135156dex991.htm（numbers.latest_quarter_kpis.items[4]，as_of Q3 2026（季末 2026-09-30，公告 2026-10-29 新聞稿日期；earnings_recency 記 10-28 盤後））
  - 註記：查無（consensus_revision 僅有 EPS 預估修正，無營收／利益率共識）
- `f_kpi5_non_gaap`（q1_business）｜Non-GAAP 毛利率＝53.7 %｜期間與口徑：Q3 2026（季末 2026-09-30，公告 2026-10-29 新聞稿日期；earnings_recency 記 10-28 盤後）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 6-K Ex.99.1 新聞稿 https://www.sec.gov/Archives/edgar/data/0001329394/000119312526436478/d135156dex991.htm（numbers.latest_quarter_kpis.items[5]，as_of Q3 2026（季末 2026-09-30，公告 2026-10-29 新聞稿日期；earnings_recency 記 10-28 盤後））
  - 註記：查無（consensus_revision 僅有 EPS 預估修正，無營收／利益率共識）
- `f_kpi10_q4_2026`（q1_business）｜Q4 2026 營收指引＝588–616 US$M｜期間與口徑：Q3 2026（季末 2026-09-30，公告 2026-10-29 新聞稿日期；earnings_recency 記 10-28 盤後）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司 6-K Ex.99.1 新聞稿 https://www.sec.gov/Archives/edgar/data/0001329394/000119312526436478/d135156dex991.htm（numbers.latest_quarter_kpis.items[10]，as_of Q3 2026（季末 2026-09-30，公告 2026-10-29 新聞稿日期；earnings_recency 記 10-28 盤後））
  - 註記：查無（consensus_revision 僅有 EPS 預估修正，無營收／利益率共識）
- `f_kpi11`（q1_business）｜全年指引（定性）＝2026 營收創新高、年增 >100% text｜期間與口徑：Q3 2026（季末 2026-09-30，公告 2026-10-29 新聞稿日期；earnings_recency 記 10-28 盤後）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司 6-K Ex.99.1 新聞稿 https://www.sec.gov/Archives/edgar/data/0001329394/000119312526436478/d135156dex991.htm（numbers.latest_quarter_kpis.items[11]，as_of Q3 2026（季末 2026-09-30，公告 2026-10-29 新聞稿日期；earnings_recency 記 10-28 盤後））
  - 註記：查無（consensus_revision 僅有 EPS 預估修正，無營收／利益率共識）
- `f_earnings_recency`（q1_business）｜最近一次財報日＝2026-10-28 date｜期間與口徑：2026-10-28／距今 4 個交易日｜kind：realized
  - 來源：—（numbers.earnings_recency，as_of 2026-10-28）
- `f_peer_simo_gross_margin_pct`（q2_moat）｜SIMO 毛利率＝50.54 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.SIMO.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_simo_operating_margin_pct`（q2_moat）｜SIMO 營業利益率＝21.3 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.SIMO.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_simo_fcf_margin_pct`（q2_moat）｜SIMO FCF 利潤率＝-24.9 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.SIMO.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_8299_two_gross_margin_pct`（q2_moat）｜8299.TWO 毛利率＝56.85 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.8299.TWO.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_8299_two_operating_margin_pct`（q2_moat）｜8299.TWO 營業利益率＝30.89 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.8299.TWO.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_8299_two_fcf_margin_pct`（q2_moat）｜8299.TWO FCF 利潤率＝-8.12 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.8299.TWO.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_mrvl_gross_margin_pct`（q2_moat）｜MRVL 毛利率＝52.21 %｜期間與口徑：TTM ending 2026-07-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MRVL.gross_margin_pct，as_of TTM ending 2026-07-31（4季加總））
- `f_peer_mrvl_operating_margin_pct`（q2_moat）｜MRVL 營業利益率＝16.81 %｜期間與口徑：TTM ending 2026-07-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MRVL.operating_margin_pct，as_of TTM ending 2026-07-31（4季加總））
- `f_peer_mrvl_fcf_margin_pct`（q2_moat）｜MRVL FCF 利潤率＝18.23 %｜期間與口徑：TTM ending 2026-07-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MRVL.fcf_margin_pct，as_of TTM ending 2026-07-31（4季加總））
- `f_peer_sndk_gross_margin_pct`（q2_moat）｜SNDK 毛利率＝76.84 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.SNDK.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_sndk_operating_margin_pct`（q2_moat）｜SNDK 營業利益率＝68.43 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.SNDK.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_sndk_fcf_margin_pct`（q2_moat）｜SNDK FCF 利潤率＝61.63 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.SNDK.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_ev_m`（q5_valuation）｜目前企業價值 EV（市值＋淨負債）＝6943.21 USD m｜期間與口徑：2026-11-03／市值 6662.63 ＋ 淨負債 280.58｜kind：realized
  - 來源：—（numbers.capital_structure.ev_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝4.25 x｜期間與口徑：2026-11-02（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-11-02（RTH 收盤，UTC））
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝13.6 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-10-31）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝19.61 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-10-31）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝22.73 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-10-31）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝1957.4 USD m｜期間與口徑：2026-11-03／yfinance revenue_estimate 0y 平均（11 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝2746.91 USD m｜期間與口徑：2026-11-03／yfinance revenue_estimate +1y 平均（12 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi6`（q4_capital）｜營業現金流＝-256.1 US$M｜期間與口徑：Q3 2026（季末 2026-09-30，公告 2026-10-29 新聞稿日期；earnings_recency 記 10-28 盤後）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 6-K Ex.99.1 新聞稿 https://www.sec.gov/Archives/edgar/data/0001329394/000119312526436478/d135156dex991.htm（numbers.latest_quarter_kpis.items[6]，as_of Q3 2026（季末 2026-09-30，公告 2026-10-29 新聞稿日期；earnings_recency 記 10-28 盤後））
  - 註記：查無（consensus_revision 僅有 EPS 預估修正，無營收／利益率共識）
- `f_kpi7_ocf_capex_23_0`（q4_capital）｜自由現金流（OCF－capex 23.0，推算）＝-279.1 US$M｜期間與口徑：Q3 2026（季末 2026-09-30，公告 2026-10-29 新聞稿日期；earnings_recency 記 10-28 盤後）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 6-K Ex.99.1 新聞稿 https://www.sec.gov/Archives/edgar/data/0001329394/000119312526436478/d135156dex991.htm（numbers.latest_quarter_kpis.items[7]，as_of Q3 2026（季末 2026-09-30，公告 2026-10-29 新聞稿日期；earnings_recency 記 10-28 盤後））
  - 註記：查無（consensus_revision 僅有 EPS 預估修正，無營收／利益率共識）
- `f_kpi8_sbc`（q4_capital）｜SBC＝17.3 US$M｜期間與口徑：Q3 2026（季末 2026-09-30，公告 2026-10-29 新聞稿日期；earnings_recency 記 10-28 盤後）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 6-K Ex.99.1 新聞稿 https://www.sec.gov/Archives/edgar/data/0001329394/000119312526436478/d135156dex991.htm（numbers.latest_quarter_kpis.items[8]，as_of Q3 2026（季末 2026-09-30，公告 2026-10-29 新聞稿日期；earnings_recency 記 10-28 盤後））
  - 註記：查無（consensus_revision 僅有 EPS 預估修正，無營收／利益率共識）
- `f_kpi9`（q1_business）｜期末現金（含受限）＝953.6 US$M｜期間與口徑：Q3 2026（季末 2026-09-30，公告 2026-10-29 新聞稿日期；earnings_recency 記 10-28 盤後）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 6-K Ex.99.1 新聞稿 https://www.sec.gov/Archives/edgar/data/0001329394/000119312526436478/d135156dex991.htm（numbers.latest_quarter_kpis.items[9]，as_of Q3 2026（季末 2026-09-30，公告 2026-10-29 新聞稿日期；earnings_recency 記 10-28 盤後））
  - 註記：查無（consensus_revision 僅有 EPS 預估修正，無營收／利益率共識）
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝280.58 USD m｜期間與口徑：2026-11-03／yfinance 最新一季：總債務 1126.51、現金 845.93（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝33.91 m shares｜期間與口徑：2026-11-03／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝1.018 %｜期間與口徑：2026-11-03／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-11-03）
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝196.49 USD｜期間與口徑：2026-11-02（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-11-02（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝14.45 x｜期間與口徑：2026-10-31／分母＝FY1 EPS 13.6，分子＝快照價 196.49｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-10-31）
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝21.13 x｜期間與口徑：2026-11-02（RTH 收盤，UTC）／4 個年度端點內的分位＝36.8｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-11-02（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝36.8 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝100.0 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝100.0 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-11-02（RTH 收盤，UTC））
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝56.14 %｜期間與口徑：2026-07-30 → 2026-10-31／FY1 共識 EPS 8.71 → 13.6（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-10-31）
- `f_ev_s_fwd`（q5_valuation）｜EV/S（EV ÷ FY1 共識營收）＝3.55 x｜期間與口徑：2026-11-03／f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）｜kind：estimate
  - 來源：—（numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝-13.15 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-11-02（RTH 收盤，UTC））
- `f_rsi14`（q5_valuation）｜RSI(14)＝38.07｜期間與口徑：2026-11-02（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ma_state`（q5_valuation）｜週線均線六態（decision_inputs.ma 必須等於此值）＝🟡｜期間與口徑：2026-11-03／timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）
  - 原文：「price 189.82 / W52 192.76 / W104 128.6 / W250 90.31 / W250 13週斜率 2.1%」
- `f_ma_w52`（q5_valuation）｜52 週均線＝192.76 USD｜期間與口徑：2026-11-03／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）

### findings_digest 中方向為負或來源衝突的條目（15 條）
- `competitive_share_entrants#0`（competitive_share_entrants｜方向 -｜狀態 ok）：20-F FY2025 列出主要競爭者為 Microchip、Phison、客戶內部自研與中國小型控制器廠；稱中國競爭者受惠於政府半導體在地化政策，預期競爭加劇，並預期未來有新興或既有公司、客戶可能取得顯著份額
  - 來源：SEC EDGAR 20-F FY2025 Item 4 Competition（as_of 2026-04-30）｜affects：moat_trend、decision_inputs.bear
- `competitive_share_entrants#1`（competitive_share_entrants｜方向 -｜狀態 ok）：20-F 風險因素：部分快閃記憶體客戶可能自行開發產品取代對公司產品的需求；中國競爭者受在地化政策受益
  - 來源：SEC EDGAR 20-F FY2025 Item 4 Competition（as_of 2026-04-30）｜affects：moat_trend、thesis.R
- `customer_second_source#0`（customer_second_source｜方向 -｜狀態 ok）：20-F 披露：所有主要 NAND 原廠都有內部自製（captive）控制器；若原廠擴大自製，merchant 市場可能縮小，過去 SIMO 營運結果曾因客戶自製而受負面影響。
  - 來源：SEC EDGAR 20-F FY2025 Item 3.D（as_of 2026-04-30）｜affects：thesis.R、decision_inputs.bear、moat_trend
- `customer_second_source#1`（customer_second_source｜方向 -｜狀態 ok）：20-F 披露客戶集中：前五大客戶占 2025 年營收約 66%，>10% 客戶合計 58%（PHISEMI、Kioxia、AFASTOR、Micron）；未點名單一最大客戶正在導入第二供應商。
  - 來源：SEC EDGAR 20-F FY2025 Item 3.D（as_of 2026-04-30）｜affects：thesis.R、decision_inputs.bear
- `customer_concentration_credit#0`（customer_concentration_credit｜方向 -｜狀態 ok）：FY2025 前五大客戶占營收約66%（2023:61%、2024:66%）；>10%客戶合計58%（四家：PHISEMI、Kioxia、AFASTOR、Micron）；前十大客戶82%。
  - 來源：SEC EDGAR 20-F FY2025 Item 3 / 財報附註（as_of 2026-04-30）｜affects：thesis.R、decision_inputs.bear
- `supply_demand_durability#4`（supply_demand_durability｜方向 -｜狀態 ok）：Silicon Motion被分析師指出：控制器廠不像NAND原廠直接受惠NAND漲價，且NAND景氣為劇烈榮枯循環，營收可能隨循環反轉快速下滑。
  - 來源：Nasdaq/Walnut Invest 摘要（SIMO bull-bear）（as_of 2026-06-01）｜affects：decision_inputs.bear、thesis.R
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：SIMO 20-F 揭露國際營運面臨政府貿易限制、實體清單、制裁、關稅與配額風險；川普政府已對公司營運所在的部分東亞國家加徵關稅，關稅可能衝擊需求與成本；NAND 等原料供應亦受貿易限制與關稅影響。
  - 來源：SEC EDGAR 20-F FY2025 Item 3 風險因素（as_of 2026-04-30）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：SIMO 為無晶圓廠，晶圓由兩家外部晶圓代工廠製造，主要為台積電、次要為中芯（SMIC）；與這些代工廠及次承包商無長期合約，依客戶訂單與預測下單。
  - 來源：Silicon Motion Form 20-F FY2025 (SEC)（as_of 2026-04-30）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：FY2025 20-F 提示基板（substrate）供應若吃緊，可能造成交貨延遲與毛利壓力。
  - 來源：Silicon Motion Form 20-F FY2025 (SEC)（as_of 2026-04-30）｜affects：thesis.R
- `geo_supply_chain#2`（geo_supply_chain｜方向 -｜狀態 ok）：SIMO 總部與核心研發位於台灣；其申報文件承認因兩岸區域地緣緊張而在台灣營運有重大風險（二手 PESTLE 分析轉述）。
  - 來源：dcf-analysis.com SIMO PESTLE Analysis [Apr-2026]（as_of 2026-04-01）｜affects：thesis.R、decision_inputs.bear
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：20-F 風險因子：若固態儲存改用 NAND 以外的非揮發記憶體而公司無具競爭力的控制器技術，控制器可及市場可能縮小；NAND 演進可能帶來公司相對不利的新型儲存裝置與市場區隔。
  - 來源：SEC EDGAR 20-F FY2025 Item 3.D（as_of 2026-04-30）｜affects：moat_trend、decision_inputs.bear
- `substitute_technology#1`（substitute_technology｜方向 -｜狀態 ok）：20-F 風險因子：市場競爭激烈、技術快速變遷，中國競爭對手受惠於政府半導體在地化政策。
  - 來源：SEC EDGAR 20-F FY2025 Item 4（as_of 2026-04-30）｜affects：moat_trend
- `channel_business_model_shift#1`（channel_business_model_shift｜方向 -｜狀態 ok）：Computex 2026：公司副總稱零售 SSD 市場上半年近乎消失，量直接流向 PC 品牌與模組廠
  - 來源：Geeknetic：Silicon Motion confirma un giro en el mercado SSD（as_of 2026-06-16）｜affects：moat_trend、thesis.R
- `major_events#1`（major_events｜方向 -｜狀態 ok）：2023-08-31 起的 Water Island 證券集體訴訟（S.D. Cal.）於 2024-09 修訂訴狀，新增 SIMO 與兩位高管為被告，主張 10b-5 與 20(a)；20-F 未預期重大不利影響。
  - 來源：SEC EDGAR 20-F FY2025 Item 8 Legal Proceedings（as_of 2026-04-30）｜affects：decision_inputs.bear
- `lawsuit_class_action#0`（lawsuit_class_action｜方向 -｜狀態 ok）：Water Island 證券集體訴訟仍在 S.D. Cal. 審理，SIMO 與兩位高管為被告。
  - 來源：SEC EDGAR 20-F FY2025（as_of 2026-04-30）｜affects：decision_inputs.bear

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 5 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/SIMO_20261103/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":480.0,"bear_5y_price":104.5,"p_bull_pct":20,"p_bear_pct":30,"upside_5y_pct":35.4,"ev5y_pct":32.5,"irr_base_pct":6.2,"asym_ratio":2.1,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":13.6,"pe":14.45,"basis":"FY2026E 共識每 ADS EPS 13.6（Koyfin 2026-10-31）；現價 $196.49 ÷ 13.6 ＝ 14.45 倍；終端倍數同樣以當年度 EPS 為分母"},"eps":{"bull":[21.5,24.0,26.0,28.0,30.0],"base":[19.0,19.0,15.5,17.0,19.0],"bear":[17.0,9.5,6.5,8.0,9.5]},"pe":{"bull":16,"base":14,"bear":11},"p":{"bull":20,"base":50,"bear":30},"yield_pct":{"dividend":1.018,"net_buyback":-0.5},"second_stage":{"bull_cagr_pct":8,"base_cagr_pct":5},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### SIMO_Q2_2026_Earnings_Call_20260730.md
- 2026-07-30｜CFO Jason Tsai｜guidance：CFO 給 Q3 2026 營收指引：季增 15–20%，$519–541 百萬。（原話："we now expect revenue to grow 15% to 20% sequentially"）
- 2026-07-30｜CFO Jason Tsai｜guidance：Q3 毛利率指引 50–51%，理由為產品組合（MonTitan、PCIe 5 控制器貢獻增加）。（原話："increase sequentially to 50% to 51% in the September quarter"）
- 2026-07-30｜CFO Jason Tsai｜guidance：Q3 營業利益率指引 27.5–28.5%。（原話："grow substantially to 27.5% to 28.5%"）
- 2026-07-30｜CFO Jason Tsai｜guidance：CFO 稱年底退出時營業利益率可超過 30%。（原話："our operating margins can exceed 30% exiting this year"）
- 2026-07-30｜CEO Wallace Kou｜guidance：CEO 預期 2026 全年營收創高、年增逾 100%。（原話："record revenue in 2026, up more than 100% year-over-year"）
- 2026-07-30｜CEO Wallace Kou｜guidance：CEO 仍預期 2026 年智慧手機出貨下滑 10–15%，但自家行動業務預期強勁成長。（原話："smartphone unit to be down 10% to 15% in 2026"）
- 2026-07-30｜CFO Jason Tsai｜guidance：CFO 表示年底退出時 MonTitan 占營收 5–10%（分析師問的是 10%）。（原話："getting to that 5% to 10% coming from MonTitan"）
- 2026-07-30｜CFO Jason Tsai｜guidance：CFO 表示只指引未來一季，不評論 2027。（原話："We're not going to comment on '27 yet at this time."）
- 2026-07-30｜CFO Jason Tsai｜guidance：CFO 對 Ferri＋Boot Drive 2027 年占營收至少 1/3 的說法，答稱有此可能。（原話："I think that's certainly a possibility."）
- 2026-07-30｜CFO Jason Tsai｜margin：Q2 毛利率 50.2%，高於指引區間 48.5–49.5%，歸因新產品導入。（原話："as we capitalize on new product introductions."）
- 2026-07-30｜CFO Jason Tsai｜margin：Q2 營業利益率 23.1%，高於指引 21–22%，歸因營收與毛利率高於預期。（原話："margin was 23.1% and exceeded our guided range of 21% to 22%"）
- 2026-07-30｜CFO Jason Tsai｜margin：Q2 營收年增 127%、超出指引高標（$393–411 百萬）。（原話："coming in well above the high end of our guided range"）
- 2026-07-30｜CFO Jason Tsai｜margin：Q2 營業費用季增至 $122.1 百萬，原因為新控制器與解決方案開發、tape-out 費用、人力。（原話："Operating expenses increased sequentially to $122.1 million"）
- 2026-07-30｜CFO Jason Tsai｜margin：管理層對毛利率拆解：MonTitan 毛利率為加分（accretive），抵銷解決方案業務的毛利壓力。（原話："offset some of the margin pressure that we see from the"）
- 2026-07-30｜CFO Jason Tsai｜margin：長期毛利率目標維持 48–50%，Q2、Q3 因組合暫時高於此區間。（原話："I think we're still comfortable with the 48% to 50%."）
- 2026-07-30｜CFO Jason Tsai｜margin：CFO 提醒解決方案（Boot Drive）為控制器加 NAND，ASP 比純控制器高；MonTitan ASP 較低。（原話："it's controller plus NAND."）
- 2026-07-30｜CEO Wallace Kou｜margin：Ferri＋Boot Drive 解決方案 Q2 季增逾一倍，占總營收近 30%（去年同期 4%）。（原話："more than doubled sequentially and represent near 30%"）
- 2026-07-30｜CEO Wallace Kou｜commitment：CEO 表示有信心達成今年 MonTitan 營收目標，並預期 2027 年顯著成長。（原話："I expect to see significant growth in 2027 and beyond"）
- 2026-07-30｜CEO Wallace Kou｜commitment：CEO 預期 MonTitan 2026 下半年再增五家 Tier 1 客戶量產。（原話："ramp five additional Tier 1 customers in the second half"）
- 2026-07-30｜CEO Wallace Kou｜commitment：PCIe Gen 6 4nm 控制器預定今年 8 月完成 tape-out。（原話："completing the tape-out of our next-generation 4-nanometer"）
- 2026-07-30｜CEO Wallace Kou｜commitment：CEO 表示 Gen 6 控制器預期為 2028 年重要成長動能。（原話："we're going to ramp much more revenue growth than this year."）
- 2026-07-30｜CEO Wallace Kou｜commitment：CEO 表示 MonTitan 明年營收成長將明顯高於今年。（原話："we're definitely going to see much stronger growth in 2027."）
- 2026-07-30｜CEO Wallace Kou｜commitment：CEO 稱 R&D 資源吃緊但會持續投資，2027 年成長將更強。（原話："proceeding more slowly than we anticipated 6 months"）
- 2026-07-30｜CEO Wallace Kou｜product：PCIe 4 到 PCIe 5 的轉換比六個月前預期的慢（OEM 以新 NAND 搭 PCIe 4 降 BOM）。（原話："QLC to become more meaningful until probably late '27"）
- 2026-07-30｜CEO Wallace Kou｜product：Edge SSD Q2 年增 40–45%。（原話："delivering 40% to 45% year-over-year growth."）
- 2026-07-30｜CFO Jason Tsai｜product：CFO 稱 QLC 要到 2027 年底至 2028 年才變得有份量，等 2Tb die 成本下降。（原話："This is an industry availability issue of the NAND."）
- 2026-07-30｜CFO Jason Tsai｜product：CFO 稱 QLC 延遲是 NAND 供應問題，非控制器問題。（原話："more than a dozen Tier 1 customers waiting for MonTitan"）
- 2026-07-30｜CEO Wallace Kou｜product：CEO 稱有逾十二家 Tier 1 客戶等待 MonTitan Gen 6 樣品。（原話："we set the market just a minimum 15% to 20%"）
- 2026-07-30｜CEO Wallace Kou｜product：被問 Gen 6 可觸及市場比例，CEO 答初始設定至少 15–20%。（原話："the opportunity in robotics may be larger"）
- 2026-07-30｜CEO Wallace Kou｜product：CEO 稱機器人的機會初步看可能大於車用；明年量仍小，2029–2030 才放大。（原話："the opportunity in robotics may be larger"）
- 2026-07-30｜CEO Wallace Kou｜competition：CEO 稱目前未見 NAND 原廠進入 Boot Drive 市場競爭。（原話："We do not see more competition and really to"）
- 2026-07-30｜CEO Wallace Kou｜competition：CEO 稱也未見模組廠進入競爭。（原話："we also don't see the competition from module maker either."）
- 2026-07-30｜CEO Wallace Kou｜competition：CEO 稱 NAND 原廠沒有 DRAM-less PCIe SSD 控制器，也不太可能為小市場投入研發。（原話："they do not have DRAM-less PCIe SSD controller"）
- 2026-07-30｜CEO Wallace Kou｜customer：CEO 稱 NVIDIA BlueField 的 Boot Drive 供應份額相當大，BlueField-4 時程不評論。（原話："a pretty large share for BlueField supply for the Boot"）
- 2026-07-30｜CEO Wallace Kou｜customer：CEO 稱 Boot Drive 客戶不只一家，與領先 GPU 公司的業務將更強。（原話："But definitely with the leading GPU company, it will go even"）
- 2026-07-30｜CEO Wallace Kou｜customer：CEO 稱低階智慧機份額不高，中國手機疲弱對自家影響相對小。（原話："That's why the impact for our business is relatively small."）
- 2026-07-30｜CEO Wallace Kou｜risk：CEO 預期 NAND 供給稀缺持續到約 2028 年新廠投產。（原話："We expect this scarcity to persist likely until 2028"）
- 2026-07-30｜CEO Wallace Kou｜risk：CEO 稱中國智慧手機市場因 LPDDR5 與儲存漲價而相當艱困。（原話："China smartphone market is very challenging due to the price"）
- 2026-07-30｜CEO Wallace Kou｜risk：CEO 表示 Boot Drive 成長的前提是能確保 NAND 供應。（原話："as long as we can secure the NAND supply"）
- 2026-07-30｜CFO Jason Tsai｜capital_allocation：Q2 現金由 $210.9 百萬降至 $181.8 百萬，原因含股利 $16.9 百萬與存貨增加。（原話："dividend payments of $16.9 million and an increase in"）
- 2026-07-30｜CFO Jason Tsai｜capital_allocation：CFO 稱新市場讓公司較不受消費性景氣循環影響。（原話："less subject to consumer cyclicality as these new wins scale"）

### 問答異常語氣（迴避／改口／保留）
- SIMO_Q2_2026_Earnings_Call_20260730.md｜問：Neil Young 問 Q2 Boot Drive 與 Ferri 的營收拆分及 Q3 指引內含比重｜答法：CFO 明說不提供該細節，改談兩者都強勁與 backlog、訂單狀況
- SIMO_Q2_2026_Earnings_Call_20260730.md｜問：Neil Young 問是否仍指引 MonTitan 年底 10% 營收 run rate｜答法：CFO 答仍在軌道上，但改述為 5% 至 10%，未直接確認 10%
- SIMO_Q2_2026_Earnings_Call_20260730.md｜問：Sebastien Naji 問 Q2/Q3 是否已有 BlueField-4 貢獻｜答法：CEO 稱無法評論具體時程，只說跟隨客戶公布、對 BlueField 供應份額大
- SIMO_Q2_2026_Earnings_Call_20260730.md｜問：Matthew Bryson 問 MonTitan 成功是否應上調長期毛利率（約 48–50%）｜答法：CFO 說仍 comfortable 於 48–50%，未鬆口上調，稱近期因組合高於此區間
- SIMO_Q2_2026_Earnings_Call_20260730.md｜問：Suji Desilva 問 2027–2028 年季節性是否趨緩｜答法：CFO 稱不評論 2027，只指引一季

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 5 | 2 |
| customer_second_source | found | 2 | 2 |
| customer_concentration_credit | found | 3 | 1 |
| supply_demand_durability | found | 5 | 3 |
| regulatory_antitrust | found | 2 | 1 |
| reg_tariff_export | found | 1 | 1 |
| geo_supply_chain | found | 3 | 2 |
| end_markets | found | 4 | 2 |
| substitute_technology | found | 4 | 2 |
| channel_business_model_shift | found | 2 | 2 |
| capital_markets_pricing | found | 4 | 2 |
| major_events | found | 2 | 3 |

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260710","verdict":"觀望","role":"衛星","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"NAND 結構性短缺推動的高盈餘可延續至 2027–2028，且 SIMO GM 由 controller mix（非純 NAND 價）驅動、可守 48%+","columns":{"2Y 驗證點":"Q2–Q4 26 GM ≥ 48.5%（guide 中位）；契約價續漲","5Y 驗證點":"2027–2028 GM 未跌破 44%（正規化底）","具體數字門檻":"Q2 26 guide GM 48.5–49.5% 已上修；契約價 1H26 +100%、Q2 +70–75% QoQ","信息來源":"SIMO Q1 26 earnings call；TrendForce 2026-06；Phison CEO（2026 產能售罄）","漂移觸發":"連 2 季 GM &lt; 47% 且歸因 NAND 價回落 → 削弱；連 4 季 &lt; 46% → 反轉"}},{"id":"H2","text":"MonTitan 企業 eSSD 成為第二成長曲線，退出 2026 占營收 5–10%、2027–2028 放大","columns":{"2Y 驗證點":"Q3–Q4 26 enterprise SSD 占比爬坡","5Y 驗證點":"2028 MonTitan + boot drive 貢獻具規模、Gen6 客戶鎖定","具體數字門檻":"退出 2026 ≥ 5% floor；5 家 CSP 量產爬坡","信息來源":"Q1 26 call；SM8366/SM8388 產品頁；NVIDIA BlueField boot 設計贏","漂移觸發":"Q3 26 占比 &lt; 3% 連 2 季，或口徑改「2028 才有意義規模」→ 削弱"}},{"id":"H3","text":"市場維持成長股倍數（Fwd PE &gt; 25x）不 de-rate 回週期股倍數（Phison ~11x）","columns":{"2Y 驗證點":"Fwd PE FY+2 維持 ≥ 20x","5Y 驗證點":"倍數未收斂至歷史 7–22x 中樞","具體數字門檻":"FPE FY+2 ≥ 20x = 仍以 AI 儲存成長股定價","信息來源":"yfinance forward PE；分析師目標價追蹤","漂移觸發":"FPE FY+2 連 2 個月 &lt; 18x → 削弱（市場改以週期股定價）"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"循環反轉 × 倍數壓縮：NAND 新產能 2027–2028 放量 → SIMO EPS 與 GM 回落 ＋ 市場改以週期股倍數定價（雙殺）","columns":{"對應假設":"H1 / H3","時間尺度":"🔥 中期（4–6 季，2027–2028）","監測指標":"TrendForce NAND ASP 月報、契約 vs 現貨價差；Fwd PE 相對歷史","警戒閾值":"NAND 現貨價領先鬆動 ＋ FPE FY+2 &lt; 18x 連 2 月"}},{"id":"R2","text":"客戶端量價背離：PC 出貨 −11.3%、機型降規 + OEM 庫存去化壓縮 client controller 出貨量","columns":{"對應假設":"H1","時間尺度":"⚡ 短期（1–2 季，2026H2）","監測指標":"client controller 出貨量 QoQ；OEM SSD 庫存週數；NB 出貨","警戒閾值":"client controller 出貨量連 2 季 QoQ 下滑"}},{"id":"R3","text":"中國自製化 × 出口管制：Maxio/InnoGrit 份額侵蝕 + 中國品牌轉本土控制器 + YMTC 實體清單合規風險","columns":{"對應假設":"H1 / H2","時間尺度":"🐢 長期（2+ 年，2027–2030）","監測指標":"中國客戶群份額；InnoGrit Gen6 進展；YMTC 出口管制狀態","警戒閾值":"任一大客戶 in-house/轉本土 ≥ 30% SIMO 份額；或 YMTC 供貨受出口管制限制"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"Fwd PE FY27 回落至 ≤18x（約 $180）；或 MonTitan 退出 2026 占營收 ≥7% 且 FY27 共識續上修確認第二曲線；或 through-cycle EPS 站穩 $10+","irr_base_pct":-4.9,"ev5y_pct":-16.8,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"衛星","signal":"B","val":"🔴","ma":"✅","trap":"🟡","moat_trend":"→","runway_post_y5":"🟡","asym_ratio":0.6,"ev5y_pct":-16.8,"irr_base_pct":-4.9,"max_dd_pct":-70.0,"bull_5y_price":480.0,"bear_5y_price":120.0,"p_bull_pct":25.0,"p_bear_pct":30.0,"rearm_trigger":"Fwd PE FY27 回落至 ≤18x（約 $180）；或 MonTitan 退出 2026 占營收 ≥7% 且 FY27 共識續上修確認第二曲線；或 through-cycle EPS 站穩 $10+","price_at_dd":324.26,"archetype":"品質複利成長","cycle_position":"晚循環"}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"SIMO","date":"2026-11-03","schema":"v15.0","contract":"v19","company_name":"Silicon Motion Technology Corporation"},"oneliner":"營收一年翻倍、Q3 毛利率 53.7%，但現價只給 FY2027 共識約 10 倍，市場把它當 NAND 週期高點定價；Q3 營業現金流 −2.56 億美元，盈餘還沒變成現金，現在不追，等現金流連兩季轉正或股價 ≤$145。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/SIMO_20261103/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/SIMO_20261103/scenario.json","answers":{"q1_business":{"verdict":"賺的是 NAND 原廠、模組廠、車廠與伺服器廠的控制器與小容量儲存方案錢。錢卡在 NAND 供給這一節：控制器靠設計導入收費，解決方案把 NAND 包進去賣，毛利與存貨都跟著 NAND 價格走。","reasoning":"營收結構：Q3 2026 營收 5.602 億美元，季增 24%、年增 131%，高於 Q2 法說給的指引上緣 5.41 億。CEO 口頭揭露控制器約占 60%，解決方案（Ferri 車用＋企業開機碟）約占 40%，後者季增逾 75%。CEO 說 2027 年兩者可能各半；Q2 法說時 CFO 還只說解決方案占「至少三分之一」有可能。獲利：Non-GAAP 毛利率 53.7%、營業利益率 32.1%，GAAP 營業利益率 29.0%。Q4 指引營收 5.88–6.16 億、毛利率 54–55%、營業利益率 36–37%，全年營收年增逾 100%。產業時鐘判第三期（過熱），依據有四點：NAND 價格一年大漲；消費端已出現需求破壞，包括手機出貨預期 −10～15%、PC 降規、零售 SSD 通路上半年近乎消失；CEO 說 Q3、Q4 合約價差不多，明年季漲幅降到個位數；原廠 2028 年新廠已規劃。供需持久性判週期性將反轉：TrendForce 看 2027 年供給成長超過需求、2H27 緩解，管理層與美光看緊到 2028，兩邊時點差約一年。議價權：上游晶圓主要靠台積電，NAND 向原廠採購，兩者都沒有長期合約；下游前五大客戶約占 66%，四家 >10% 客戶合計 58%（PHISEMI、Kioxia、AFASTOR、Micron）。單點依賴在 NAND 取得能力。CEO 在 Q2 法說說，開機碟成長的前提是能確保 NAND 供應。這項能力一面是護城河（跟多家原廠都有關係），一面是集中度風險，因為原廠同時是供應商、客戶與潛在自製者。","fact_refs":["f_kpi0_gaap","f_kpi1_non_gaap","f_kpi2_non_gaap","f_kpi3_gaap","f_kpi4_gaap","f_kpi5_non_gaap","f_kpi10_q4_2026","f_kpi11","f_earnings_recency"],"verdict_values":{"revenue_quality":"量價混合：約四成營收含 NAND 轉嫁，營收規模隨 NAND 價格放大；控制器部分由份額與 ASP 升級帶動","unit_econ_note":"控制器按顆計價，PCIe 5、UFS 4.1／5 升級拉高 ASP。解決方案每 6 個月議價一次，目標約兩季把存貨轉成現金。車用專案 3–5 年，價格與供貨在專案開始時談定","archetype":{"primary":"循環/商品","secondary":"品質複利成長","confidence":"中","fingerprint":"盈餘隨 NAND 週期大幅擺動：2023 年營收 −32%、EPS −69%；本輪營業利益率由 2025 年 10.5% 升到 Q3 GAAP 29.0%，現價對 FY2027 共識只有約 10 倍"},"industry":{"clock_phase":"III","sd_verdict_source":"週期性將反轉。TrendForce（2026-07、2026-09）預期 2027 年供給成長超過需求、2H27 趨於平衡；SIMO 管理層、美光 CEO 與分析師 Kuo 則看緊到 2028。2028 年新廠投產是供給可逆的依據","bargaining":{"up":"晶圓主要靠台積電、次要中芯，都沒有長期合約；NAND 向多家原廠採購，缺貨期供應商議價力強；基板吃緊","down":"前五大客戶約 66%、前十大 82%；四家 >10% 客戶合計 58%；解決方案每 6 個月議價一次","geo":"總部與研發在台灣；中國有 YMTC 與受政策扶持的在地控制器廠，公司在中國擴研發以服務當地客戶"},"profit_pool_dir":"流向 NAND 原廠：同業對照中，原廠的營業利益率約為 SIMO 的三倍；SIMO 靠解決方案進入原廠讓出的小容量市場","tam_table":[{"item":"企業開機碟市場","value":"2026 年約 30 億美元，2030 年逾 50 億（管理層估計，Q3 2026 法說）"},{"item":"近 CPU 含 DRAM 開機碟","value":"2030 年至少 100 億美元（管理層估計）；SIMO 預計 2H27 量產，模組廠夥伴可能 2027Q2 先出貨"},{"item":"PC 端 PCIe 5 滲透率","value":"目前約 10%，2027 年底 20–25%（管理層估計）"},{"item":"PCIe 6 MonTitan 可觸及份額","value":"初始設定至少 15–20%（Q2 2026 法說，CEO）"},{"item":"利潤池占比五年變化與第三方份額","value":"事實表未涵蓋"}]}}},"q2_moat":{"verdict":"護城河方向持平。執行面因企業與車用新產品而擴大；定價權仍跟著 NAND 週期走，對最接近的同業也沒有利潤率優勢。兩者相抵。","reasoning":"機制：二十年的韌體與控制器設計經驗，加上相容多家 NAND 原廠顆粒的能力，轉成設計導入的黏性。具體例子有三：車用 3–5 年的認證專案、NVIDIA BlueField 開機碟的主要供應地位、MonTitan 七家已公布客戶 2026 年開始商業量產。方向證據：事實表沒有同業 ROIC，改比營業利益率。SIMO TTM 21.3%，低於群聯 30.9%（群聯資料期間到 2026-06）；毛利率 50.5% 也低於群聯 56.9%，所以沒有利潤率領先。份額只有管理層說法（持續取得份額、原廠轉向外部控制器），沒有第三方數字。評分：執行 8，理由是 Q3 營收、毛利率、營益率全部高於 Q2 法說指引上緣，PCIe 6 也已流片。定價權 6，理由是毛利率上升與 NAND 漲價同步；Q2 法說 CFO 還說長期毛利率 48–50%，一季後改口為 2027 年 low-to-mid 50%，新框架是在價格最高的一季上調的，不能當成議價力的證據。三項威脅都屬點對點或低機率，未扣分。增量報酬：ROIIC 約 30%，但再投資率約 246%，超過盈餘的部分靠可轉債支應，而且這組數字落在週期高點。持續期四項中，價值鏈分配判紅。","fact_refs":["f_peer_simo_gross_margin_pct","f_peer_simo_operating_margin_pct","f_peer_simo_fcf_margin_pct","f_peer_8299_two_gross_margin_pct","f_peer_8299_two_operating_margin_pct","f_peer_8299_two_fcf_margin_pct","f_peer_mrvl_gross_margin_pct","f_peer_mrvl_operating_margin_pct","f_peer_mrvl_fcf_margin_pct","f_peer_sndk_gross_margin_pct","f_peer_sndk_operating_margin_pct","f_peer_sndk_fcf_margin_pct","f_kpi5_non_gaap","f_ev_m","f_ev_s_current"],"verdict_values":{"moat":{"mechanism":"韌體加上跨多家 NAND 原廠的相容經驗，形成設計導入黏性（車用認證、平台型開機碟、企業級控制器）","execution":8,"pricing":6,"grade":"B","trend":"→","trend_evidence":"執行面擴大：Q3 營收、毛利率、營益率全部高於指引上緣，企業與車用設計導入增加。定價權持平：營業利益率仍低於群聯（兩者期間差一季）；毛利率上升與 NAND 漲價同步，無法證明是議價力提升。兩者合併為持平","competitor_notes":[{"name":"群聯（8299.TWO）","strategy_note":"最直接的同業，同樣是控制器加模組雙軌；TTM 毛利率與營業利益率都高於 SIMO，SIMO 在利潤率上沒有領先"},{"name":"Marvell（MRVL）","strategy_note":"事實表列為對照的大型 fabless 同業，營業利益率低於 SIMO，但自由現金流為正；對照之下，SIMO 的負現金流來自存貨，不是本業虧損"},{"name":"SanDisk（SNDK）","strategy_note":"NAND 供應端的代表，這一輪的利潤大多落在這一端；原廠類型的公司同時是 SIMO 的供應來源與潛在自製者"},{"name":"Microchip","strategy_note":"20-F 點名的競爭者，事實表沒有它的財務數字"},{"name":"中國在地控制器廠","strategy_note":"受政府在地化政策扶持，20-F 預期競爭加劇；管理層說它們難取得台積電 12nm 以下製程，在企業級市場還不構成威脅。事實表沒有份額數字"}],"peer_na_reason":"事實表沒有同業 ROIC，以營業利益率差代替；同業資料期間不一致（群聯截至 2026-06、Marvell 截至 2026-07）","threats":[{"level":"🟡","text":"NAND 原廠自製控制器：所有主要原廠都有自製能力，過去原廠收回自製曾傷害營運。目前方向相反，原廠正轉向外部控制器，並把小容量市場讓出","p":"20%","evidence_refs":["customer_second_source#0","competitive_share_entrants#1"]},{"level":"🟡","text":"中國在地化控制器廠受政策扶持，加上群聯、Microchip 的點對點競爭。管理層稱中國廠難取得先進製程，企業級暫無威脅","p":"30%","evidence_refs":["competitive_share_entrants#0","substitute_technology#1"]},{"level":"🟡","text":"替代架構：固態儲存若改用 NAND 以外的非揮發記憶體，或新規格把控制功能整合進其他晶粒，控制器可及市場會縮小；目前沒有量產時程","p":"10%","evidence_refs":["substitute_technology#0"]}],"roic_durability":{"quadrant":"高利益率×低周轉（存貨墊高投入資本）","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"控制器是每顆 SSD、eMMC／UFS 的必要元件。NAND 缺貨時，SSD 廠寧可降容量也要維持出貨量，控制器需求不減反增（2026-06 公司說法）。使用者（伺服器、車廠）、決策者（模組廠、原廠）、付款者（模組廠）三個角色都成立。消費端屬於延後購買，企業與車用則是真正的需要"},{"item":"決策層級","level":"🟡","text":"車用是 3–5 年的認證專案，價格與供貨在專案開始時談定，替換成本高；企業開機碟靠平台設計導入。消費性控制器則每一代產品重新選，模組廠可以在 SIMO、群聯與中國廠之間切換，單一型號層級的替代性就很高"},{"item":"價值鏈分配","level":"🔴","text":"這一輪週期的利潤主要留在 NAND 原廠，同業對照中原廠的營業利益率約為 SIMO 的三倍。原廠同時是 SIMO 的供應商、>10% 客戶（Kioxia、Micron）與潛在自製者。解決方案的成長來自原廠讓出小容量市場，這是原廠自己的分配選擇，週期反轉後可能收回"},{"item":"社會容忍度","level":"🟢","text":"儲存控制器不是受監管或政治敏感的民生必需品，沒有社會面的價格上限；關稅與出口管制屬貿易政策風險，另列在風險項"}],"roiic":"約 30%（增量稅後營業利益約 2.04 億 ÷ 估計增量投入資本約 6.85 億；週期高點數字）","reinvest_rate":"約 246%（估計再投資額約 6.85 億 ÷ TTM 稅後營業利益約 2.78 億；超過 100% 的部分由可轉債支應）","endo_ceiling":30,"formula_note":"TTM 營收約 16.3 億美元（EV 69.43 億 ÷ trailing EV/S 4.25）。TTM 稅後營業利益 ≈ 16.3 億 × 營業利益率 21.3% × (1−20%) ≈ 2.78 億；FY2025 為 8.856 億 × 10.51% × 0.8 ≈ 0.745 億，增量約 2.04 億。再投資額以稅後營業利益減自由現金流估算：TTM 自由現金流 ≈ 16.3 億 × −24.9% ≈ −4.07 億，所以再投資額 ≈ 2.78 + 4.07 ≈ 6.85 億，再投資率約 246%。ROIIC ≈ 2.04 ÷ 6.85 ≈ 30%。內生成長上界把再投資率上限設為 100%，等於 30%。這是週期高點利益率下的數字，正規化後會明顯較低。稅率 20% 取 Q4 指引的有效稅率；投入資本存量事實表未涵蓋，當期 ROIC 無法直接算"}}}},"q3_growth":{"verdict":"成長跑道中等。消費性控制器已是業界標準，滲透率高；企業級與車用是第二曲線，但還在早期，量化證據多半是管理層估計。","reasoning":"成長來源是量、價與組合：解決方案把 NAND 包進營收（價格成分），控制器靠份額與 PCIe 5、UFS 4.1 升級拉高 ASP；沒有併購，也沒有淨回購。三年共識 EPS：FY2026E 13.6、FY2027E 19.61、FY2028E 22.73（Koyfin），FY2026E 到 FY2028E 年化 29.3%。若以 FY2025A GAAP 3.64 為基期，年化 84%，但基期口徑不同，數字偏高。營收共識有 11–12 位分析師（yfinance），EPS 家數事實表未涵蓋。內生上界約 30%，推導見護城河題的增量報酬：共識兩年 CAGR 落在上界附近，三年口徑則超出。缺口可以歸因於利益率擴張，營業利益率由 2025 年 10.5% 升到 Q3 GAAP 29.0%，不屬於依賴重新評價。我的基本情境 FY2026E 到 FY2031E 年化約 6.9%，在上界內。成長跑道：企業級（MonTitan、開機碟）份額低、正在導入，但時程與 TAM 多是管理層估計；PCIe 6 要到 2027Q1 才送樣，近 CPU 開機碟 2H27 才量產。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_kpi11","f_kpi10_q4_2026","f_peer_simo_operating_margin_pct","f_peer_simo_fcf_margin_pct"],"verdict_values":{"growth":{"driver_mix":"量＋價＋組合：解決方案含 NAND 轉嫁（價格成分），控制器靠份額與規格升級；無併購，股數微增","runway_years":"5–9（企業級與車用滲透率低；消費性控制器已是業界標準）","runway_post_y5":"🟡","endo_ceiling_basis":"增量 ROIC 約 30% × 再投資率上限 100%（實際約 246%，超過的部分靠可轉債），推導見護城河題；這是週期高點的數字，正規化後應更低","segments":[{"item":"控制器（eMMC／UFS、SSD 含 MonTitan）","value":"Q3 約占營收 60%（CEO 口頭揭露）。SSD 控制器季增、年增都強，Q4 指引持平到小降；eMMC／UFS Q3 小幅季減，短期持平"},{"item":"解決方案（Ferri 車用、企業開機碟）","value":"Q3 逾 40%，季增逾 75%；Q2 約 30%，一年前同期約 4%。2027 年可能到 50%，營收含 NAND"},{"item":"MonTitan 企業級","value":"Q2 法說稱 2026 年底占營收 5–10%，Q3 未更新占比；PCIe 6 已流片，2027Q1 送樣"},{"item":"分部毛利率","value":"事實表未涵蓋；管理層稱車用毛利率優於預期，MonTitan 拉高毛利"}],"decay_signals":[{"item":"EPS 成長顯著高於營收成長（差 >5pp）","lit":true,"note":"FY2025A 到 FY2026E 營收約 +121%，EPS 由 3.64 到 13.6（基期為 GAAP，數字偏高）；成長主要來自利益率擴張"},{"item":"FCF／淨利 <0.75 連 2 年","lit":true,"note":"2024 年 0.37、2025 年 0.05；2026Q3 自由現金流 −2.79 億美元"},{"item":"毛利率連 2 季年減","lit":false,"note":"Q2 50.2%、Q3 53.7%，高於 2025 全年 48.3%"},{"item":"核心市占近 12 個月縮減","lit":false,"note":"沒有第三方份額數據；管理層稱持續取得份額"},{"item":"SBC／營收 >5% 且逐年上升","lit":false,"note":"Q3 約 3.1%"},{"item":"TAM 萎縮或被替代技術壓縮","lit":false,"note":"替代記憶體與新架構都還沒有量產時程"},{"item":"產業估值倍數近 3 年系統性下移","lit":false,"note":"事實表未涵蓋產業倍數；SIMO 自身 FY+2 本益比近四個月由 25 倍以上降到約 10 倍，期間太短，不計入"},{"item":"其餘三項（提價後銷量下滑、維持性資本支出占 FCF、停止投資新產能）","lit":false,"note":"不適用或事實表未涵蓋；FCF 為負，維持性資本支出占比無法計算"}],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"資本配置中等。股利持續調升、稀釋低，但成長完全靠舉債養存貨，現金轉換是本輪最弱的一環。","reasoning":"FCF／淨利：2022 年 0.30、2023 年 1.87、2024 年 0.37、2025 年 0.05（年度財報）；2026Q3 營業現金流 −2.56 億美元，自由現金流 −2.79 億。SBC／營收：Q3 為 1,730 萬 ÷ 5.602 億，約 3.1%。Q3 現金去向：可轉債淨入 11.27 億美元，流出到營運資金（存貨）、股利與償還短期銀行借款，期末現金含受限為 9.536 億；未見回購，也沒有併購。股利由每 ADS 每年 $2.00 調到 $2.30。可轉債利率 0%、轉換價 $380.50，股價高於轉換價時約有 302 萬股潛在稀釋（約 9%）。目前淨負債 2.81 億（含租賃），等於用借來的錢養存貨。CFO 的目標是約兩季把 NAND 存貨轉成現金，並說這次募資足夠支應未來幾年的營運資金。三項計分：併購不適用；回購不適用；SBC 淨稀釋約 0.7%，通過。營運槓桿為正，營業利益成長快於營收，沒有壓縮。","fact_refs":["f_kpi6","f_kpi7_ocf_capex_23_0","f_kpi8_sbc","f_kpi9","f_net_debt_m","f_shares_diluted_m","f_dividend_yield_ttm"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":false,"passed":null,"input":"近三年沒有併購；MaxLinear 案中 SIMO 是被併方，且該案已終止"},{"name":"buyback_yield","applicable":false,"passed":null,"input":"法說把回購列為伺機而為，Q2、Q3 現金去向未見回購；回購均價事實表未涵蓋"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"稀釋股數由 2025 年約 3,369 萬（淨利 1.226 億 ÷ EPS 3.64）到目前 3,391 萬，約 +0.7%，低於每年 1.5%；可轉債轉換價 $380.50 之上另有約 302 萬股潛在稀釋，尚未發生"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長來自自有產品與新市場，不靠併購；資本回報以股利為主（年股利由每 ADS $2.00 調升到 $2.30），近期未見回購，現金主要投入 NAND 存貨"}}}},"q5_valuation":{"verdict":"合理、不便宜。現價等於假設盈餘高點過後回到每股約 14 美元、給 14 倍；我認為這個假設大致公允，安全邊際不足。","reasoning":"現價 $196.49。對 FY2026E 13.6 是 14.45 倍，對 FY2027E 19.61 約 10 倍，對 FY2028E 22.73 約 8.6 倍。FY1 共識三個月上修 56%，股價同期卻比前份判斷日低 39%，26 週報酬 −13%，表示盈餘上修全被倍數壓縮吃掉，市場在用週期股的方式定價。這個價格要求的是：2027–2028 年盈餘在 NAND 轉平後回到 13–15 美元，而不是延續成長。盈餘若守在 19 美元以上，現價便宜；若重演 2023 年的下修，現價仍然貴。我的基本情境是 2028 年持平、2029 年回落約兩成、2031 年回到 19 美元，終端 14 倍約 $266。上行空間的口徑：短期指 12 個月，以 FY2027E 基本情境 19.0 × 11 倍 ≈ $209，約 +6.4%；中期指五年基本情境終點，約 +35.4%。年化約 6–7%，偏弱。週線價格 189.82 低於 52 週均線 192.76，RSI 38，動能不熱也不弱。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_pe_current","f_pe_percentile","f_ps_percentile","f_ev_s_percentile","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_3m_fy1_pct","f_dividend_yield_ttm","f_ev_m","f_net_debt_m","f_ev_s_fwd","f_week26_return_pct","f_rsi14","f_ma_state","f_ma_w52"],"verdict_values":{"valuation":{"basis":"Forward 本益比（FY2026E、FY2027E 共識）為主，對照正規化盈餘","tier":"循環型儲存半導體","peers":{"expanded":false,"reason":"事實表的同業對照只有利潤率，沒有同業本益比；終端倍數改以公司自身歷史區間（前份記載 7–22 倍）與現值 14.45 倍對照"},"fwd_pe":14.45,"peg":0.49,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"Forward 本益比 14.45 倍（FY2026E），對 FY2027E 約 10 倍、FY2028E 約 8.6 倍。FY2026E 到 FY2028E 共識年化 29.3%，PEG 0.49，表面上便宜。但分母落在 NAND 週期高點、有爭議，便宜的論證不成立。改看現價要求什麼：$196.49 ＝ 正規化 EPS 14 美元 × 14 倍，大約落在我基本情境 2029 年谷底到 2031 年之間，所以判合理。五年連續分位事實表未涵蓋；四個年度端點內，trailing 本益比分位 36.8，P/S 與 EV/S 分位 100。後兩者因營收含 NAND 轉嫁，跨年不可比","upside_short_pct":6.4,"upside_mid_pct":35.4,"denominator_disputed":true,"denominator_note":"FY2027E 19.61、FY2028E 22.73 建立在 NAND 吃緊延續與解決方案維持高毛利兩個前提上；Q3 營業現金流 −2.56 億美元，盈餘還沒被現金驗證。週期反轉時這組分母會大幅下修，2023 年 EPS 曾 −69%"}}},"q6_how_wrong":{"verdict":"最可能看錯的是把 NAND 高點的盈餘當成新常態；反方向的錯則是低估車用與企業級合約的黏性。陷阱風險中等。","reasoning":"衰退信號十項亮兩項：EPS 成長遠高於營收成長（由利益率擴張帶動），以及 FCF／淨利連兩年低於 0.75（2024 年 0.37、2025 年 0.05）。陷阱風險與長期成長性都判中。壓力測試五項：NAND 合約價轉跌、最大客戶流失、存貨不轉現金而需再融資、消費性出貨再降 15%、台海或關稅造成供應中斷。只吸收得了兩項：單一客戶流失（每家 >10% 客戶約占一到兩成營收，期末現金 9.5 億撐得住），以及消費性再降（控制器占比正降到五成）。NAND 轉跌與再融資兩項正中弱點。最大回撤範圍 −40%～−65%，依據見情境樹。管理層迴避紀錄：Q2 法說不拆 Ferri 與開機碟、把 MonTitan 目標由 10% 改述為 5–10%、不評論季節性；Q3 法說仍不給分部細節，季節性與 2027 年營業費用延到 1 月再談，仲裁也沒有更新。這些迴避集中在最能檢驗盈餘品質的分部數字上。","fact_refs":["f_kpi6","f_kpi7_ocf_capex_23_0","f_kpi9","f_consensus_eps_fy2","f_week26_return_pct","f_rsi14","f_ma_state"],"verdict_values":{"trap":{"verdict":"🟡","label":"週期高點的低本益比"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":13.6,"pe":14.45,"basis":"FY2026E 共識每 ADS EPS 13.6（Koyfin 2026-10-31）；現價 $196.49 ÷ 13.6 ＝ 14.45 倍；終端倍數同樣以當年度 EPS 為分母"},"eps":{"bull":[21.5,24.0,26.0,28.0,30.0],"base":[19.0,19.0,15.5,17.0,19.0],"bear":[17.0,9.5,6.5,8.0,9.5]},"pe":{"bull":16,"base":14,"bear":11},"p":{"bull":20,"base":50,"bear":30},"yield_pct":{"dividend":1.17,"net_buyback":-0.5},"second_stage":{"bull_cagr_pct":8,"base_cagr_pct":5},"max_dd":{"lo":-65,"hi":-40,"basis":"以下行週期回推。2023 年營收 −32%、EPS −69%（年度財報）；若 NAND 轉跌使 EPS 落到 7–9.5 美元，市場給 10–12 倍，股價約 $70–$115，相對現價約 −40%～−65%。股價自前份判斷日 $324.26 已跌到 $196.49（−39%），部分下行已經發生，所以高端取 −40%，而不是更淺","trigger_time":null},"basis":{"bull":"NAND 吃緊延續到 2028，解決方案議價守住，PCIe 6 MonTitan 與近 CPU 開機碟 2028 年放量。FY2027 為 21.5 美元，略高於 Q4 指引年化的約 20.7，之後每年 +8～10%。股價高於 $380.50 後可轉債轉換、股數多約 9%，已扣入。終端 16 倍，取公司歷史區間上半段","base":"FY2027 接近共識（19.0）。2H27 起 NAND 走平，2028 年持平；2029 年合約價下跌，EPS 回落約兩成到 15.5；2030–2031 年靠企業與車用回升到 19。終端 14 倍，取歷史 7–22 倍中段，也接近現價對 FY2026E 的 14.45 倍。股息殖利率以新年股利每 ADS $2.30 計，約 1.17%","bear":"NAND 合約價 2H27 轉跌，解決方案營收隨價格縮水並提列存貨跌價。2028 年 EPS 腰斬到 9.5，2029 年再降到 6.5（2023 年曾 −69%），之後緩慢回到 9.5。終端 11 倍，對應成長熄火到 10% 以下的倍數，介於歷史低端 7 倍與中段之間；前份記載群聯約 11 倍，同業現值事實表未涵蓋"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"2023 年營收 −32%、營業利益率 6.4%、EPS 1.58（年度財報）。TrendForce 預期 2027 年供給成長超過需求、2H27 緩解。有分析師指出控制器廠不像原廠直接受惠 NAND 漲價，營收可能隨週期反轉快速下滑。分析師在 Q3 法說指出存貨已到約 8 億美元，CFO 沒有否認","assumption":"解決方案的高毛利來自合約與認證，不是 NAND 價差","consequence":"NAND 合約價在 2H27–2028 轉跌，解決方案營收縮水並提列存貨跌價，2028–2029 年 EPS 落到 6.5–9.5 美元。市場給 10–12 倍，股價約 $70–$115，相對現價約 −40%～−65%。五年虧 50% 最可能就是這條路","ruling":"採納，作為空頭情境（30%）的主軸。這條與唯一致命點是同一件事，兩者對得上，不另改","watch":"TrendForce 合約價；SIMO 季毛利率、存貨與營業現金流","evidence_refs":["supply_demand_durability#4"],"fact_refs":["f_kpi5_non_gaap","f_kpi6","f_consensus_eps_fy2"]},{"view":"論點成功但股東經濟變差","evidence":"Q3 營業現金流 −2.56 億美元，自由現金流 −2.79 億；公司以 0% 利率發行 11.5 億美元可轉債，轉換價 $380.50；2025 年 FCF 只有 630 萬美元，FCF／淨利 0.05","assumption":"營收成長會轉成股東的現金","consequence":"即使 2027 年營收 +40%，存貨也會跟著營收放大，現金流可能繼續為負。股價若漲過 $380.50，可轉債轉換稀釋約 9%，多頭情境的每股盈餘被攤薄。利潤也可能在議價中被 NAND 原廠拿回","ruling":"部分採納：多頭情境的 EPS 已扣約 9% 稀釋，並把現金流轉正列為重啟進場條件","watch":"營業現金流、存貨、股數","evidence_refs":[],"fact_refs":["f_kpi6","f_kpi7_ocf_capex_23_0","f_shares_diluted_m","f_net_debt_m"]},{"view":"價格已反映太多","evidence":"P/S 與 EV/S 在四個年度端點中都是最高（分位 100）；FY2028E 共識 EPS 成長降到 +16%；上一輪 2022 年高點 EPS 只有 5.17","assumption":"現價 10 倍 FY2027 已經夠便宜","consequence":"如果正規化 EPS 只有 12–14 美元，現價等於正規化盈餘的 14–16 倍，並不便宜","ruling":"部分採納：估值結論定為合理而非便宜。但 P/S 偏高有一部分是營收含 NAND 轉嫁造成的，跨年不可比，這條不是全部的故事","watch":"1 月指引後 FY2027 共識是否下修","evidence_refs":[],"fact_refs":["f_ps_percentile","f_ev_s_percentile","f_consensus_eps_fy3","f_pe_current"]},{"view":"論點失敗","evidence":"前五大客戶約 66%，>10% 客戶合計 58%；所有主要原廠都有自製控制器能力；中國競爭者受在地化政策扶持","assumption":"原廠會持續外包、客戶結構穩定","consequence":"任一家大客戶轉自製或換供應商，就是一成以上的營收缺口，而且多半發生在週期反轉、原廠產能鬆動的時候","ruling":"反駁它是主要致命路徑：原廠目前反向外包（Q1 2026 法說），中國廠難取得先進製程。保留為長期風險","watch":"年報 >10% 客戶名單、單季營收季減幅度","evidence_refs":["customer_concentration_credit#0","competitive_share_entrants#0","customer_second_source#1"],"fact_refs":["f_kpi0_gaap"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 324.26 → 本次 196.49（-39.4%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=324.26","side_b":"本次 price_at_dd=196.49","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]裁決由 dd_decision.py 機械路由：前份 觀望 → 本次 迴避","cause":"價格變動","prior_field":["dca_verdict"],"side_a":"前份 dca_verdict=觀望","side_b":"本次 dca_verdict=迴避","ruling":"裁決是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。沒有單一輸入能還原，屬多欄共同：估值 🔴→🟡、均線 ✅→🟡。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]角色由 dd_decision.py 機械路由：前份 衛星 → 本次 不持有","cause":"價格變動","prior_field":["dca_role"],"side_a":"前份 dca_role=衛星","side_b":"本次 dca_role=不持有","ruling":"角色是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。沒有單一輸入能還原，屬多欄共同：估值 🔴→🟡、均線 ✅→🟡。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 324.26 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 324.26 美元：Bull 價 480、Bear 價 120，五年期望值 −16.8%，基準年化 −4.9%，不對稱比 0.6","side_b":"本次情境、股價仍用 324.26 美元：Bull 價 480、Bear 價 104.5，五年期望值 −19.7%，基準年化 −3.9%，不對稱比 0.47","ruling":"先換情境、股價不動：五年期望值少 2.9 個百分點，基準年化多 1.0 個百分點。不對稱比由 0.6 變為 0.47。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 324.26 美元：五年期望值 −19.7%，基準年化 −3.9%，不對稱比 0.47","side_b":"本次情境、股價 196.49 美元：五年期望值 +32.5%，基準年化 6.2%，不對稱比 2.05","ruling":"再換股價、情境不動：起點價下跌 39.4%，五年期望值多 52.2 個百分點，基準年化多 10.1 個百分點，不對稱比由 0.47 升到 2.05。合計五年期望值比前份多 49.3 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"盈餘是結構性還是週期高點","cause":null,"prior_field":null,"side_a":"管理層、美光與 Kuo：NAND 供給吃緊到 2028。公司 6 個月議價、車用 3–5 年合約，毛利率可守在 50% 中段，2027 年營收至少 +40%","side_b":"TrendForce 與市場：2027 年供給成長超過需求、2H27 緩解；控制器廠不直接受惠 NAND 漲價，營收會隨週期反轉；現價只給 FY2027 共識約 10 倍","ruling":"不可調和，兩邊方向相反。採 B 側作為基本情境的方向：2028 年盈餘持平，2029 年回落約兩成。依據有三：Q3 營業現金流 −2.56 億美元，高毛利還沒變成現金；2023 年營收 −32%、EPS −69%，是這家公司上一輪的實際紀錄；獨立來源（TrendForce）看到的平衡時點比管理層早約一年。A 側的證據要等 2027 上半年的現金流才看得到","evidence_level":"中：雙方都有獨立來源，決勝數據 2027Q2 才會出現","settle_metric":"2027Q1–Q2 營業現金流與存貨；NAND 合約價首度季減那一季的毛利率","if_then":["若 2027 上半年營業現金流連兩季轉正、存貨下降且季毛利率 ≥52%，改採 A 側，重跑研究後以 2% 首倉分兩批建立","若 NAND 合約價首度季減且當季毛利率 <50%，維持不碰，空頭機率上調至 40%","若股價先漲但現金流證據未到，不追","若股價跌破 $145，而毛利率與現金流沒有惡化，分批反買，首批 1%"],"evidence_refs":["supply_demand_durability#4"]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"Q4 指引營業利益率 36–37%，推算單季年化 EPS 約 20.7 美元，已超過 FY2027 共識 19.61。FY1 共識三個月上修 56%，股價卻比前份低 39%。賣方目標價均值 $370（2026-09）與 $251（2026-08）都在現價之上","side_b":"這正是週期股在盈餘高點的典型樣子：本益比最低的時候，往往最該小心。營業現金流為負，賣方目標價 $230–$450，分布很散","ruling":"反駁，但保留一條路：現金流證據若提前出現，A 側成立，現價就是便宜。我比賣方共識悲觀，是因為共識 FY2028 仍有 +16%，等於假設 NAND 平衡後解決方案毛利不降，這與 TrendForce 的時點衝突。股價已比前份低 39%，不等於有安全邊際。目標價全距比值約 2 倍，未超過 2.5 倍，不因此下調信心；但兩份資料都在 Q3 財報前，沒有反映最新上修","evidence_level":"中","settle_metric":"季營業現金流與存貨","if_then":["若 Q4 2026 營業現金流已轉正，提前重跑研究，不必等兩季"],"evidence_refs":[]},{"axis":"產業態勢：競爭、結構、其他","cause":null,"prior_field":null,"side_a":"競爭：20-F 點名群聯、Microchip、原廠自製與受政策扶持的中國廠，預期競爭加劇。其他：關稅、實體清單、零售 SSD 通路消失、替代記憶體","side_b":"結構：原廠把小容量與開機碟市場讓出、轉向外部控制器；車用與企業級的認證週期長","ruling":"雙向拉鋸。結構面短期轉好（Q2、Q3 法說：原廠退出小容量市場），競爭面在中國持續惡化（20-F）。淨效果在 NAND 吃緊期偏正，週期反轉後原廠可能回頭，方向不穩","evidence_level":"中","settle_metric":"原廠是否重回開機碟與小容量市場","if_then":["若原廠在 NAND 鬆動後重新推出開機碟產品，結構面改判轉弱，空頭機率上調至 40%"],"evidence_refs":["competitive_share_entrants#0","substitute_technology#0","reg_tariff_export#0","channel_business_model_shift#1"]},{"axis":"管理層說法前後對照","cause":null,"prior_field":null,"side_a":"2026-07-30 Q2 法說，CFO Jason Tsai：長期毛利率仍是 48–50%；解決方案 2027 年占營收至少三分之一「有可能」","side_b":"2026-10-29 Q3 法說，CFO Jason Tsai：2027 年毛利率 low-to-mid 50%。CEO Wallace Kou：解決方案 2027 年可能到 50%","ruling":"可調和，屬程度差異。財測一路超標，Q3 營收、毛利率、營益率都高於指引上緣，可信度加分。但毛利率框架是在 NAND 價格最高的一季上調的，而解決方案占比加速上升代表 NAND 價格曝險變大；兩件事同時發生，所以不把新框架當成正規化水準","evidence_level":"高","settle_metric":"NAND 走平後的季毛利率","if_then":["若 NAND 走平兩季後毛利率仍 ≥52%，接受新框架，基本情境 2028 年 EPS 上調到共識附近"],"evidence_refs":[]},{"axis":"估值結論","cause":"新證據","prior_field":["val"],"side_a":"前份：估值偏貴。現價 $324.26，依前份重啟條件「18 倍約 $180」反推 FY2027 共識約 10 美元，等於 30 倍以上","side_b":"本次：合理。現價 $196.49，FY2027 共識上修到 19.61，約 10 倍；但分母在週期高點，有爭議","ruling":"改判的主因是新證據：Q3 大幅超標，加上 2027 年至少 +40% 的指引，讓 FY2027 共識約翻倍。股價同期下跌 39% 是次因。因為分母有爭議，只升到合理，不判便宜","evidence_level":"高：共識數字與股價都是事實表數據","settle_metric":"1 月法說後 FY2027 共識是否守在 19 美元以上","if_then":["若 1 月指引後 FY2027 共識下修超過 15%，估值結論退回偏貴"],"evidence_refs":[]},{"axis":"公司類型","cause":"新證據","prior_field":["archetype"],"side_a":"前份：品質複利成長","side_b":"本次：循環/商品為主，品質複利成長為輔","ruling":"新證據是營收結構改變。解決方案（含 NAND）由去年同期約 4% 升到 Q3 逾 40%，2027 年可能到 50%；Q3 營業現金流 −2.56 億美元，存貨約 8 億美元，NAND 價格曝險已經進入損益表與資產負債表，Q3 法說分析師 Naji 的提問問的就是這點。控制器本業仍有複利性質，所以列為次要","evidence_level":"高","settle_metric":"NAND 合約價走平後的毛利率與現金流","if_then":["若 NAND 合約價走平兩季後毛利率仍 ≥52% 且營業現金流轉正，類型改回以品質複利成長為主"],"evidence_refs":[]},{"axis":"維持不變的判斷","cause":"新證據","prior_field":["signal","trap","moat_trend","runway_post_y5","cycle_position"],"side_a":"前份：綜合訊號 B、陷阱風險中、護城河持平、五年後成長跑道中等、晚循環","side_b":"本次：與前份相同","ruling":"新證據逐項檢查後維持。綜合訊號：估值改善，被週線轉弱與盈餘品質疑慮抵銷。陷阱風險：衰退信號亮兩項（EPS 成長遠高於營收、FCF／淨利連兩年 <0.75），仍屬中。護城河：執行面擴大、定價權未證，合併為持平。成長跑道：企業級第二曲線有設計導入，但份額與 TAM 仍是管理層估計。景氣位置：合約價 Q3 到 Q4 走平、消費端需求破壞、新廠 2028 年規劃，仍是晚循環","evidence_level":"中","settle_metric":"各項對應的觸發條件","if_then":["若 NAND 合約價首度季減，景氣位置改判進入下行，陷阱風險升為高"],"evidence_refs":[]},{"axis":"最大回撤範圍","cause":"價格變動","prior_field":["max_dd_pct"],"side_a":"前份：−70%（自 $324.26 起算）","side_b":"本次：−40%～−65%（自 $196.49 起算）","ruling":"股價已跌 39%，部分下行已經發生。以空頭盈餘 7–9.5 美元 × 10–12 倍回推，地板約 $70–$115，換算的回撤比前份淺，但仍可能超過 −50%","evidence_level":"中","settle_metric":"NAND 合約價與季毛利率","if_then":["若 NAND 合約價首度季減，以下緣 −65% 做準備，持股上限不超過 3%"],"evidence_refs":[]},{"axis":"情境機率","cause":"方法變動","prior_field":["p_bull_pct","p_bear_pct"],"side_a":"前份：多頭 25%、空頭 30%","side_b":"本次：多頭 20%、基本 50%、空頭 30%","ruling":"情境樹改以 FY2031 為終端。空頭路徑明確以 NAND 合約價轉跌加存貨跌價建模，多頭路徑扣入可轉債轉換約 9% 的稀釋。多頭需要 NAND 吃緊延續到 2028，與 TrendForce 的時點衝突，所以降到 20%。空頭維持 30%，因為共識成長超過內生上界，下限就是 30%","evidence_level":"中","settle_metric":"2H27 合約價","if_then":["若 TrendForce 改口 2028 年仍短缺，多頭機率回到 25%"],"evidence_refs":[]},{"axis":"重啟進場條件","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"Fwd PE FY27 回落至 ≤18x（約 $180）；或 MonTitan 退出 2026 占營收 ≥7% 且 FY27 共識續上修確認第二曲線；或 through-cycle EPS 站穩 $10+","side_b":"2027 上半年營業現金流連兩季轉正且存貨下降；或股價 ≤$145 而季毛利率仍 ≥50%","ruling":"前份第一條已經成立：FY2027 本益比約 10 倍，低於 18 倍，但成立的方式是共識 EPS 翻倍，而不是股價跌到 $180，本次就是依此重跑研究。第二條：本季法說沒給 MonTitan 占比，無法驗證。第三條：週期平均 EPS 是否站穩 10 美元，要經過一次下行才看得到。本輪的約束是盈餘還沒變成現金、分母落在週期高點，所以重啟進場改綁現金流證據，或綁一個足以吸收空頭情境的價格","evidence_level":"高","settle_metric":"季營業現金流、存貨；股價","if_then":["若任一新條件成立，重跑研究後首倉 1–2%","若股價先漲而現金流未轉正，不追"],"evidence_refs":[]},{"axis":"Single Thing（唯一致命點）","cause":"新證據","prior_field":null,"side_a":"前份為空（null），未設唯一致命點","side_b":"NAND 合約價在 2027–2028 年首度轉為季減","ruling":"新增 Single Thing：解決方案已占營收四成以上，並持有約 8 億美元存貨，NAND 價格方向成為 EPS 最大的單一敏感項。若發生，空頭機率上調至 40%，持有者減碼至半倉","evidence_level":"中","settle_metric":"TrendForce 合約價季變動","if_then":["若合約價首度季減，減碼至半倉；未持有則不進場"],"evidence_refs":["supply_demand_durability#4"]},{"axis":"減碼與清倉指標","cause":"新證據","prior_field":null,"side_a":"前份為空（null），未設減碼或清倉指標","side_b":"季毛利率連 2 季 <50% 減碼、連 3 季 <45% 清倉；2027Q2 營業現金流仍為負且存貨續增；NAND 合約價首度季減；任一 >10% 客戶退出名單","ruling":"新增。本輪公司類型改為以循環為主，需要可量測的減碼與清倉指標；門檻取自 H1、H2 與唯一致命點","evidence_level":"中","settle_metric":"季報與 TrendForce","if_then":["若毛利率連 3 季 <45%，清倉"],"evidence_refs":[]},{"axis":"裁決與角色","cause":"新證據","prior_field":[],"side_a":"前份：觀望","side_b":"本次輸入：估值改為合理、公司類型改為以循環為主、景氣位置晚循環、要等價格或現金流證據","ruling":"最終裁決與角色由下游依本次輸入計算。輸入面的變動全部來自 Q3 財報與法說的新證據，方向仍是不追、等條件","evidence_level":"中","settle_metric":"重啟進場條件","if_then":["若重啟進場條件成立，重跑研究"],"evidence_refs":[]},{"axis":"前份假設：市場維持成長股倍數","cause":"新證據","prior_field":null,"side_a":"前份 H3：FPE FY+2 ≥ 20x，連 2 個月 <18x 即削弱","side_b":"本次：FY2027 本益比約 10 倍，遠低於 18 倍","ruling":"前份 H3 已反轉，市場改用週期股倍數定價。前份 R1 的兩半：倍數壓縮已經發生；NAND 現貨鬆動還沒發生，CEO 說 Q3、Q4 合約價持平。本次不再把倍數維持當成假設，改把盈餘能否變成現金當成主假設","evidence_level":"高","settle_metric":"NAND 合約價","if_then":["若 NAND 價格也開始鬆動，前份 R1 完整成立，依唯一致命點處理"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"2027 年 1 月 Q4 法說給出 2027 全年指引：營收年增是否 ≥40%、毛利率是否在 50% 中段","type":"假設驗證","maps_to":"H1","metric":"FY2027 營收指引年增率；Q1 2027 毛利率指引","threshold":"營收 ≥+40% 且毛利率指引 ≥52%","action":"符合即列為重啟條件之一，但仍需現金流確認；低於 +40% 則 H1 削弱，維持不碰","source_freq":"季報法說（每季）","date":"2027-01","evidence_refs":[]},{"n":2,"text":"NAND 合約價首度轉為季減","type":"Single Thing","maps_to":"R1","metric":"NAND 合約價季變動（TrendForce）","threshold":"首度季減","action":"空頭機率上調至 40%；觀望期間不進場；若已持有，減碼至半倉","source_freq":"TrendForce 月報與季報","date":null,"evidence_refs":["supply_demand_durability#4"]},{"n":3,"text":"營業現金流與存貨：存貨能否約兩季周轉回現金","type":"假設驗證","maps_to":"H2","metric":"季營業現金流、存貨","threshold":"2027Q1–Q2 營業現金流連兩季 >0 且存貨季減","action":"達標即重跑研究，首倉 2%；2027Q2 仍為負且存貨續增，則 H2 削弱，維持不碰","source_freq":"季報（每季）","date":"2027-07","evidence_refs":[]},{"n":4,"text":"價格跌到足以吸收空頭情境","type":"估值rearm","maps_to":null,"metric":"股價與季毛利率","threshold":"≤$145（約 FY2027 共識 7.4 倍）且季毛利率 ≥50%","action":"重跑研究後分批反買，首批 1%，第二批等下一季現金流","source_freq":"每日收盤","date":null,"evidence_refs":[]},{"n":5,"text":"大客戶流失或轉自製","type":"風險","maps_to":"R3","metric":">10% 客戶名單（20-F）；單季營收季減","threshold":"任一 >10% 客戶退出名單，或單季營收季減 ≥15% 且歸因於客戶","action":"若持有，減碼至半倉；未持有，重啟條件延後一季","source_freq":"年報（每年 4 月）加季報","date":"2027-04","evidence_refs":["customer_second_source#1","customer_concentration_credit#0"]},{"n":6,"text":"關稅、基板或代工成本吸收失敗","type":"風險","maps_to":"R4","metric":"季毛利率變動與管理層歸因","threshold":"單季毛利率下滑 ≥2pp，且明確歸因於關稅、基板或代工","action":"若持有，減碼一半；未持有，不進場","source_freq":"季報","date":null,"evidence_refs":["reg_tariff_export#0","geo_supply_chain#1","geo_supply_chain#0"]},{"n":7,"text":"Water Island 證券集體訴訟（S.D. Cal.）進展，SIMO 與兩位高管為被告；受影響金額與審結日期事實表未涵蓋","type":"風險","maps_to":null,"metric":"集體認證裁定、和解金額","threshold":"集體認證通過，且出現金額 ≥ 期末現金 10%（約 9,500 萬美元）的不利和解","action":"若持有，減至半倉；若檢方或 SEC 介入，清倉","source_freq":"年報法律程序章節、法院公告","date":null,"evidence_refs":["major_events#1","lawsuit_class_action#0"]},{"n":8,"text":"Q4 2026 財報後複審","type":"複審日期","maps_to":null,"metric":"全份研究重跑","threshold":"日期到","action":"重跑研究","source_freq":"一次","date":"2027-02-15","evidence_refs":[]},{"n":9,"text":"再融資或稀釋","type":"風險","maps_to":"R5","metric":"新增股權或可轉債融資公告","threshold":"2027 年內再發行股權類融資","action":"重啟條件作廢並重寫；若持有，減碼","source_freq":"6-K 公告","date":null,"evidence_refs":[]}],"kill_metrics":[{"metric":"季 Non-GAAP 毛利率","bear_threshold":"連 2 季 <50%（NAND 合約價走平或季減時）減碼；連 3 季 <45% 清倉","window":"2027Q1–2028Q4","source":"公司季報新聞稿（6-K）","last_status":"ok"},{"metric":"季營業現金流","bear_threshold":"2027Q2 仍為負且存貨續增","window":"2026Q4–2027Q2","source":"季報現金流量表","last_status":"warning"},{"metric":"NAND 合約價季變動","bear_threshold":"首度季減","window":"2027–2028","source":"TrendForce 合約價報告","last_status":"ok"},{"metric":">10% 客戶名單","bear_threshold":"任一家退出名單","window":"每年 20-F（4 月）","source":"SEC 20-F 客戶集中揭露","last_status":"ok"}],"evidence_dismissed":[],"action_conditions":{"rearm_trigger":"2027 上半年營業現金流連兩季轉正且存貨下降；或股價 ≤$145 而季毛利率仍 ≥50%","exec_line":"任一條件成立先重跑研究；首倉 1–2%，分兩批，第二批等下一季現金流確認；續漲但證據未到不追","holding_cap":"≤3%（循環股，深回撤可能超過 −50%）"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":"晚循環","cycle_verdict":"頂部觀望","thesis_irreconcilable":true,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":false,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"股價 ≤$145（約 FY2027 共識 7.4 倍）且季毛利率仍 ≥50%；或 2027 上半年營業現金流連兩季轉正且存貨下降","qc48_result":null,"qc48_note":null,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null},"decision_out":{"verdict":"迴避","role":"不持有","row_hit":"2","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":true,"basis":"thesis_irreconcilable=True"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]}],"pacing":[],"holding_cap":null,"requires_critic":[]},"thesis":{"H":[{"id":"H1","text":"企業開機碟、Ferri 車用與 MonTitan 讓 2027 年營收再成長至少 40%，毛利率守在 50% 以上；消費性出貨衰退不改變成長方向","2y":"FY2027 營收 ≥ FY2026 的 1.4 倍，各季毛利率 ≥50%","5y":null,"10y":null,"threshold":"FY2027 營收年增 ≥40%（管理層 Q3 2026 法說）；季 Non-GAAP 毛利率 ≥50%（Q3 為 53.7%，Q4 指引 54–55%）","source":"公司季報新聞稿（6-K）、2027 年 1 月法說的全年指引","drift_rule":"季毛利率連 2 季比 50% 低 5% 以上（約 <47.5%）削弱；連 3 季低 10% 以上（約 <45%）反轉；1 月法說全年營收指引低於 +40% 即削弱"},{"id":"H2","text":"解決方案的高毛利來自 6 個月議價與車用多年合約，不是 NAND 漲價帶來的存貨利得；存貨約兩季周轉回現金，營業現金流在 2027 上半年轉正","2y":"2027Q1–Q2 營業現金流轉正，存貨停止季增","5y":null,"10y":null,"threshold":"營業現金流 >0 連 2 季（Q3 2026 為 −2.56 億美元）；NAND 合約價走平後的那一季，季毛利率仍 ≥50%","source":"季報現金流量表與資產負債表；TrendForce 合約價報告","drift_rule":"2027Q2 營業現金流仍為負且存貨續增，削弱；NAND 合約價走平或季減後，毛利率連 3 季 <45%，反轉"},{"id":"H3","text":"MonTitan 企業級控制器與近 CPU 開機碟成為第二條成長曲線，讓控制器業務在 2028–2030 年 NAND 週期下行時仍能成長","2y":null,"5y":"2028 年即使 NAND 合約價下跌，控制器營收仍年增；PCIe 6 MonTitan 2027Q1 送樣、2028 年量產","10y":null,"threshold":"PCIe 6 MonTitan 2027Q1 開始送樣；近 CPU 開機碟 2H27 開始出貨；2028 年控制器業務年增 ≥10%","source":"法說的產品進度與管理層口頭揭露的控制器／解決方案比重","drift_rule":"送樣或量產時程延後連 4 季削弱；延後連 6 季，或 2028 年控制器營收年減 ≥10%，反轉"}],"R":[{"id":"R1","text":"NAND 週期反轉：2H27 起供需平衡、合約價轉跌，解決方案營收與毛利一起下滑並出現存貨跌價，盈餘下修幅度接近 2023 年","h_ref":"H2","clock":"🔥","threshold":"NAND 合約價首度季減，且 SIMO 季毛利率 <50%","evidence_refs":["supply_demand_durability#4"]},{"id":"R2","text":"消費端量縮：PC 與手機因記憶體漲價而降規，零售 SSD 通路上半年近乎消失；eMMC／UFS 持平，SSD 控制器 Q4 指引持平到小降","h_ref":"H1","clock":"⚡","threshold":"控制器業務連 2 季季減（依管理層口頭揭露）","evidence_refs":["channel_business_model_shift#1"]},{"id":"R3","text":"客戶集中：前五大客戶約占 2025 年營收 66%，四家 >10% 客戶合計 58%；其中 Kioxia、Micron 同時是 NAND 供應商與潛在自製者，任一家轉自製或換供應商，就是一成以上的營收缺口","h_ref":"H1","clock":"🔥","threshold":"任一 >10% 客戶在年報名單中消失，或單季營收季減 ≥15% 且管理層歸因於客戶","evidence_refs":["customer_second_source#1","customer_concentration_credit#0","customer_second_source#0"]},{"id":"R4","text":"供應鏈與地緣：總部與研發在台灣；晶圓主要靠台積電、次要中芯，且沒有長期合約；基板吃緊；關稅與實體清單風險同時存在","h_ref":"H1","clock":"🐢","threshold":"單季毛利率因關稅或基板成本下滑 ≥2pp 且管理層明確歸因；或任一代工來源受出口管制限制","evidence_refs":["geo_supply_chain#0","geo_supply_chain#1","geo_supply_chain#2","reg_tariff_export#0"]},{"id":"R5","text":"營運資金吃掉盈餘：Q3 營業現金流 −2.56 億美元、存貨約 8 億美元，靠 11.5 億美元零息可轉債支撐。存貨兩季周轉不成就要再融資；股價若高於轉換價 $380.50，另有約 9% 稀釋","h_ref":"H2","clock":"⚡","threshold":"2027Q2 營業現金流仍為負，或公司宣布新一輪股權或可轉債融資","evidence_refs":[]}],"single_thing":{"description":"NAND 合約價在 2027–2028 年首度轉為季減（TrendForce 合約價報告）","why_fatal":"解決方案已占營收四成以上，存貨約 8 億美元是在高價期買進的。NAND 價格轉跌時，含 NAND 轉嫁的營收與毛利會同步下滑，再加上存貨跌價，2023 年營收 −32%、EPS −69% 的情況可能重演。這是 EPS 最大的單一敏感項","if_happens":"空頭機率由 30% 上調到 40%；若持有，減碼至半倉；觀望期間不進場","how_monitor":"TrendForce 每月與每季的 NAND 合約價；SIMO 季報的毛利率、存貨與營業現金流；法說對 6 個月議價合約的說法","probability":"12–24 個月內約 40%：TrendForce 看 2H27 平衡，管理層、美光、Kuo 看緊到 2028，兩邊抵銷後略偏向會發生"}},"appendix_a":{"growth_durability":6,"quality_score":6,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":10.0,"peg_fy2":0.34,"stress":{"pass":2,"total":5}},"eps_meta":{"base_eps_path":{"FY2025A":3.64,"FY2026E":13.6,"FY2027E":19.61,"FY2028E":22.73},"fy_end_month":12,"eps_basis":"每 ADS 盈餘。FY2026E–FY2028E 為 Koyfin 共識（2026-10-31），事實表未標 GAAP 或 Non-GAAP；量級與 Q3 法說 Non-GAAP 每 ADS 4.35 美元一致，推定為 Non-GAAP。FY2025A 3.64 取年度財報 GAAP 稀釋 EPS（Non-GAAP 基期事實表未涵蓋），基期口徑不同，用它算的三年 CAGR 偏高"},"catalysts":[{"date":"2027-01-31","date_precision":"month","type":"guidance","event":"Q4 2026 財報與 2027 全年指引（管理層說 1 月會給更完整的 2027 財測）","impact":"高","watch":"2027 年營收年增是否 ≥40%、毛利率與營業費用指引、Q1 季節性"},{"date":"2027-03-31","date_precision":"quarter","type":"product","event":"PCIe 6 MonTitan（4nm）開始送樣","impact":"中","watch":"送樣客戶數、是否如期"},{"date":"2027-06-30","date_precision":"quarter","type":"macro","event":"NAND 合約價走勢：TrendForce 預期 2H27 供需平衡","impact":"高","watch":"合約價是否首度季減"},{"date":"2027-09-30","date_precision":"quarter","type":"product","event":"近 CPU 含 DRAM 開機碟開始量產出貨（模組廠夥伴可能 Q2 先出貨）","impact":"中","watch":"首批客戶與營收貢獻"},{"date":"2027-04-30","date_precision":"month","type":"other","event":"FY2026 20-F 揭露客戶集中度與競爭者","impact":"中","watch":">10% 客戶名單與前五大占比"},{"date":null,"date_precision":null,"type":"other","event":"MaxLinear 仲裁終局裁決（求償 1.6 億美元終止費及損害賠償），聽證已於 2026-03 結束","impact":"中","watch":"裁決金額與收款時程；1.6 億美元約等於每 ADS 4.7 美元"}]}
```

---

## ⑤ 覆蓋面（程式判定，你回的 ⑤ 燈號會被覆寫）

燈號 🟢：核心軸皆有證據或不適用，非核心軸也沒有空軸。plan 時 archetype 為「品質複利成長」、判斷者歸「循環/商品」，循環/商品 的專屬核心軸未採證（不計燈號）：cyclical_inventory_price_position、cyclical_supply_discipline_capacity。

⑤ 的 reason 只需評論：空軸的查詢詞是否切題、判斷有沒有交代缺口對結論的影響。

---

## 尾段：回覆格式

只回一個 JSON 陣列，①–⑧ 每條一個元素，八個全出，不得跳號、不得多列，陣列外不得有任何文字（不加前言、不加 markdown 圍欄、不加附註）：

```json
[{"item": "①", "light": "🔴|🟡|🟢", "judgment_path": "$.路徑", "reason": "一句話"}]
```
