你是 DD 管線 v20 的判斷層閘（gate），標的 ALV（20261024）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（33 條）
- `f_kpi0_net_sales_gaap`（q1_business）｜Net sales (GAAP)＝2693 USD M｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-23）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001034670/000119312526429404/alv-ex99_1.htm（numbers.latest_quarter_kpis.items[0]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-23））
- `f_kpi1_adjusted_operating_incom`（q1_business）｜Adjusted operating income / margin (non-GAAP)＝9.7 %｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-23）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿 https://www.sec.gov/Archives/edgar/data/0001034670/000119312526429404/alv-ex99_1.htm（numbers.latest_quarter_kpis.items[1]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-23））
- `f_kpi2_gaap_operating_income_ma`（q1_business）｜GAAP operating income / margin＝9.4 %｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-23）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿 https://www.sec.gov/Archives/edgar/data/0001034670/000119312526429404/alv-ex99_1.htm（numbers.latest_quarter_kpis.items[2]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-23））
- `f_kpi5_management_guidance_fy20`（q1_business）｜Management guidance FY2026＝adj. operating margin 約 10.5%；organic 約 0%；OCF 約 $1.2B｜期間與口徑：Q3 2026（公告於 2026-10-23）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司 Q3 2026 新聞稿 https://www.sec.gov/Archives/edgar/data/0001034670/000119312526429404/alv-ex99_1.htm（numbers.latest_quarter_kpis.items[5]，as_of Q3 2026（公告於 2026-10-23））
- `f_peer_alv_gross_margin_pct`（q2_moat）｜ALV 毛利率＝19.22 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ALV.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_alv_operating_margin_pct`（q2_moat）｜ALV 營業利益率＝9.18 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ALV.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_earnings_recency`（q1_business）｜最近一次財報日＝2026-10-23 date｜期間與口徑：2026-10-23／距今 1 個交易日｜kind：realized
  - 來源：—（numbers.earnings_recency，as_of 2026-10-23）
- `f_peer_alv_fcf_margin_pct`（q2_moat）｜ALV FCF 利潤率＝6.83 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ALV.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_600699_ss_gross_margin_pct`（q2_moat）｜600699.SS 毛利率＝18.12 %｜期間與口徑：TTM ending 2026-03-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.600699.SS.gross_margin_pct，as_of TTM ending 2026-03-31（4季加總））
- `f_peer_600699_ss_operating_margin_pct`（q2_moat）｜600699.SS 營業利益率＝5.81 %｜期間與口徑：TTM ending 2026-03-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.600699.SS.operating_margin_pct，as_of TTM ending 2026-03-31（4季加總））
- `f_peer_600699_ss_fcf_margin_pct`（q2_moat）｜600699.SS FCF 利潤率＝0.64 %｜期間與口徑：TTM ending 2026-03-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.600699.SS.fcf_margin_pct，as_of TTM ending 2026-03-31（4季加總））
- `f_peer_mga_operating_margin_pct`（q2_moat）｜MGA 營業利益率＝5.48 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MGA.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_mga_fcf_margin_pct`（q2_moat）｜MGA FCF 利潤率＝7.52 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MGA.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_lea_operating_margin_pct`（q2_moat）｜LEA 營業利益率＝3.67 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.LEA.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_lea_fcf_margin_pct`（q2_moat）｜LEA FCF 利潤率＝3.58 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.LEA.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝10.32 USD/share｜期間與口徑：2026-10-24／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261024.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-10-24）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝11.59 USD/share｜期間與口徑：2026-10-24／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261024.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-10-24）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝13.19 USD/share｜期間與口徑：2026-10-24／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261024.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-10-24）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝11101.11 USD m｜期間與口徑：2026-10-24／yfinance revenue_estimate 0y 平均（12 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-10-24）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝11371.0 USD m｜期間與口徑：2026-10-24／yfinance revenue_estimate +1y 平均（20 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-10-24）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi3_free_operating_cash_flow`（q1_business）｜Free operating cash flow＝124 USD M｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-23）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿 https://www.sec.gov/Archives/edgar/data/0001034670/000119312526429404/alv-ex99_1.htm（numbers.latest_quarter_kpis.items[3]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-23））
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝1891.0 USD m｜期間與口徑：2026-10-24／yfinance 最新一季：總債務 2088.0、現金 197.0（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-10-24）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝72.01 m shares｜期間與口徑：2026-10-24／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-10-24）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝2.276 %｜期間與口徑：2026-10-24／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-10-24）
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝114.67 USD｜期間與口徑：2026-10-23（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-10-23（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝11.11 x｜期間與口徑：2026-10-24／分母＝FY1 EPS 10.32，分子＝快照價 114.67｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-10-24）
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝13.78 x｜期間與口徑：2026-10-23（RTH 收盤，UTC）／4 個年度端點內的分位＝45.4｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-10-23（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝45.4 %｜期間與口徑：2026-10-23（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-10-23（RTH 收盤，UTC））
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝1.88 %｜期間與口徑：2026-07-30 → 2026-10-24／FY1 共識 EPS 10.13 → 10.32（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261024.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-10-24）
- `f_consensus_rev_fy2_pct`（q5_valuation）｜FY2 共識修正＝-0.43 %｜期間與口徑：2026-10-24／兩份 Koyfin 快照之間的 EPS 修正幅度（11.64 → 11.59）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261024.xlsx（numbers.consensus_revision.fy2.revision_pct，as_of 2026-10-24）
- `f_ev_s_fwd`（q5_valuation）｜EV/S（EV ÷ FY1 共識營收）＝0.91 x｜期間與口徑：2026-10-24／f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）｜kind：estimate
  - 來源：—（numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m，as_of 2026-10-24）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝-1.23 %｜期間與口徑：2026-10-23（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-10-23（RTH 收盤，UTC））
- `f_rsi14`（q5_valuation）｜RSI(14)＝48.21｜期間與口徑：2026-10-23（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-10-23（RTH 收盤，UTC））

### findings_digest 中方向為負或來源衝突的條目（22 條）
- `competitive_share_entrants#2`（competitive_share_entrants｜方向 -｜狀態 ok）：中國本土車廠佔 Autoliv 中國銷售由 2022 年 22% 升至 2025 年 44%；BYD 高度垂直整合，被動安全由子公司 FinDreams 供應，Autoliv 僅供應零件（主要為氣體產生器）
  - 來源：SEC EDGAR 10-K FY2025 Item 7 MD&A（as_of 2026-02-19）｜affects：moat_trend、decision_inputs.bear
- `competitive_share_entrants#3`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K 風險因素：亞洲（中國、韓國、印度）競爭激烈，預期有更多國際與本土競爭者進入，可能導致降價、毛利下降與無法維持份額
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-19）｜affects：moat_trend、thesis.R
- `customer_second_source#1`（customer_second_source｜方向 -｜狀態 ok）：10-Q 稱 BYD 高度垂直整合，被動安全系統由子公司 FinDreams 供應（Autoliv 供應氣體產生器）；Toyota 關係企業（Toyota Gosei）與 Hyundai Mobis 取得母廠大部分業務。
  - 來源：SEC EDGAR 10-Q 2026-06-30（as_of 2026-07-24）｜affects：moat_trend、decision_inputs.bear
- `supply_demand_durability#0`（supply_demand_durability｜方向 -｜狀態 ok）：Autoliv 2026年5月宣布逐步關閉土耳其廠（方向盤、氣囊、安全帶），管理層判斷EMEA產能超過未來需求；全面關廠預計2028上半年，重組費用約1.42億美元，2027起年化稅前節省4,000萬美元、2028達滿額
  - 來源：Autoliv press release 'Autoliv to Discontinue Manufacturing Operations in Türkiye' (PRNewswire) / Q3 2026 8-K（as_of 2026-05-08）｜affects：moat_trend、decision_inputs.bear
- `regulatory_antitrust#0`（regulatory_antitrust｜方向 -｜狀態 ok）：EC 反壟斷調查已於 2019 年結案；目前仍有一名客戶在德國提起的民事反壟斷訴訟（涉及十多年前的指控），未來其他允許民事求償的國家也可能出現類似訴訟
  - 來源：SEC EDGAR 10-K FY2025 Item 1A Risk Factors（as_of 2026-02-19）｜affects：decision_inputs.bear、thesis.R
- `regulatory_antitrust#2`（regulatory_antitrust｜方向 -｜狀態 ok）：BMW 在德國對 Autoliv 提起損害賠償訴訟，求償 6,300 萬歐元加利息（合計約 9,500 萬歐元），源自 EC 調查所涉行為
  - 來源：SEC EDGAR 10-Q 2026Q3（as_of 2026-10-23）｜affects：decision_inputs.bear、valuation
- `reg_tariff_export#1`（reg_tariff_export｜方向 -｜狀態 ok）：FY2025 10-K風險因子：半導體與感測器採購依賴全球電子供應鏈，受出口管制、實體清單限制與制裁影響；關稅成本在固定價或終身定價合約下可能無法完全轉嫁。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A Risk Factors（as_of 2026-02-19）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：10-Q 風險因子：單一小型零組件缺貨即可迫使公司停產某產品、可能持續很久；列舉原因含供應商停工與貿易限制，並提到氣體產生器推進劑可能遇進出口許可問題
  - 來源：Autoliv 10-Q (period 2026-09-30), SEC（as_of 2026-10-23）｜affects：decision_inputs.bear、thesis.R
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：Q3 2026 財報：客戶拉貨準確度轉差，歸因中國發展；關稅成本已回收逾 80%，每季淨影響約 6–7 百萬美元
  - 來源：Autoliv 8-K Q3 2026 earnings release（as_of 2026-10-23）｜affects：decision_inputs.bear、thesis.R
- `capital_markets_pricing#0`（capital_markets_pricing｜方向 -｜狀態 ok）：Q3 2026 發布的全年指引：有機成長約 0%、匯率約 +2.5%、調整後營業利益率約 10.5%、營運現金流約 $1.2B；7 月指引為 10.5-11%，即利益率落在原區間下緣
  - 來源：Autoliv 8-K Ex99.1 (Q3 2026 earnings release)（as_of 2026-10-23）｜affects：valuation、thesis.R
- `capital_markets_pricing#1`（capital_markets_pricing｜方向 -｜狀態 ok）：Q3 2026 銷售 $2,693M（-0.5%），有機 -1.1%，調整後營業利益率 9.7%，稀釋 EPS $2.13（-6.8%）
  - 來源：Autoliv 8-K Ex99.1 (Q3 2026 earnings release)（as_of 2026-10-23）｜affects：valuation
- `capital_markets_pricing#3`（capital_markets_pricing｜方向 -｜狀態 ok）：TD Cowen 於 2026-09-08 由 Buy 降至 Hold，目標價 $148→$137；BofA 於 Q2 後目標價 $140→$134 維持 Buy
  - 來源：Benzinga / Investing.com 彙整（as_of 2026-09-08）｜affects：valuation
- `major_events#0`（major_events｜方向 -｜狀態 ok）：2026-05-11 8-K 含 Item 2.05（退出/處分成本）與 2.06（重大減損）；公司 2026-05-08 宣布逐步退出土耳其製造，EMEA 產能調整最終稅前費用約 $142M（搜尋摘要所述，未逐字核對原文）
  - 來源：SEC EDGAR 8-K（2026-05-11，Item 2.06）（as_of 2026-05-11）｜affects：thesis.R、valuation
- `major_events#1`（major_events｜方向 -｜狀態 ok）：Autoliv 為 ARC 安全氣囊氣體產生器產品責任集體訴訟（MDL 3051）被告之一，公司否認指控，已判定損失為 reasonably possible，未計提且無法估計區間，程序仍在進行
  - 來源：SEC EDGAR 10-K FY2025 Item 8 Contingent Liabilities（as_of 2026-02-19）｜affects：thesis.R、decision_inputs.bear
- `cyclical_supply_discipline_capacity#4`（cyclical_supply_discipline_capacity｜方向 -｜狀態 ok）：Joyson Safety Systems 匈牙利 Miskolc 工廠擴建，總投資 HUF 16 billion（補助 4.9 billion），稱將成全球最大被動安全工廠。
  - 來源：autopro.hu（as_of 2025-01-01）｜affects：thesis.R、decision_inputs.bear
- `cyclical_inventory_price_position#0`（cyclical_inventory_price_position｜方向 -｜狀態 ok）：Q3 2026 10-Q：2026 全年原物料漲價毛衝擊估約 1.2 億美元（Q1 時估約 0.9 億），公司預期以降本、材料組合與客戶／供應商談判抵銷大部分
  - 來源：Autoliv Form 10-Q (period ended 2026-09-30)（as_of 2026-10-23）｜affects：valuation、decision_inputs.bear
- `cyclical_inventory_price_position#1`（cyclical_inventory_price_position｜方向 -｜狀態 ok）：Q4 2025 財報電話會：部分 OEM 因管理庫存而短通知或無通知停產
  - 來源：Autoliv Q4 2025 earnings call transcript（as_of 2026-01-30）｜affects：thesis.R
- `cyclical_prior_downcycle_behavior#0`（cyclical_prior_downcycle_behavior｜方向 -｜狀態 ok）：2008-09 下行：Autoliv 全年營業利益率由 2007 年 7.4% 降至 2008 年 4.7%、2009 年 1.3%；2009 營業利益 6,900 萬美元，較 2008 年 3.06 億美元降 78%；2009 銷售 51.2 億美元年減 21%，毛利率 16.6%（搜尋摘要轉述，未核原文）。
  - 來源：SEC Form 10-K FY2009 exhibit 13 (Autoliv Inc)（as_of 2010-02-01）｜affects：decision_inputs.bear、thesis.R
- `cyclical_prior_downcycle_behavior#1`（cyclical_prior_downcycle_behavior｜方向 -｜狀態 ok）：2020 疫情：第二季銷售年減 51%，營業利益由第一季 1.7 億美元轉為第二季虧損 2.34 億美元；毛利率年減 17.2 個百分點；下半年因降本與銷售回升獲益，公司取消股利（搜尋摘要轉述，未核原文）。
  - 來源：SEC Form 8-K Q2 2020 / Form 10-K FY2020 (Autoliv Inc)（as_of 2020-07-17）｜affects：decision_inputs.bear、thesis.R
- `cyclical_prior_downcycle_behavior#2`（cyclical_prior_downcycle_behavior｜方向 -｜狀態 ok）：2022 供應鏈／原料成本壓力：全年調整後營業利益率 6.8%（2021 為 8.3%）；第一季調整後僅 3.2%，主因原料成本、供應鏈中斷與輕型車產量波動（搜尋摘要轉述，未核原文）。
  - 來源：SEC Form 10-K FY2022 (Autoliv Inc)（as_of 2023-02-01）｜affects：decision_inputs.bear
- `lawsuit_class_action#0`（lawsuit_class_action｜方向 -｜狀態 ok）：ARC Inflator 產品責任集體訴訟（MDL 3051，N.D. Georgia）仍在進行，公司否認指控、未計提；搜尋未見 2026 年針對 Autoliv 的證券集體訴訟
  - 來源：SEC EDGAR 10-K FY2025 Item 8（as_of 2026-02-19）｜affects：thesis.R、decision_inputs.bear
- `lawsuit_class_action#1`（lawsuit_class_action｜方向 -｜狀態 ok）：10-K 風險因素提及與墨西哥稅務機關就當地製造活動的爭議處於早期階段，不利結果可能對營運與財務有重大負面影響
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-19）｜affects：thesis.R、decision_inputs.bear

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 6 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ALV_20261024/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":249.8,"bear_5y_price":97.2,"p_bull_pct":20,"p_bear_pct":30,"upside_5y_pct":54.4,"ev5y_pct":46.2,"irr_base_pct":9.1,"asym_ratio":5.2,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":10.32,"pe":11.11,"basis":"FY2026E共識EPS（FY1）與判斷日收盤114.67美元；終端倍數同樣套在當年度預估EPS"},"eps":{"bull":[11.8,13.5,15.2,16.8,18.5],"base":[11.3,12.5,13.5,14.5,15.4],"bear":[9.6,7.8,9.0,10.0,10.8]},"pe":{"bull":13.5,"base":11.5,"bear":9.0},"p":{"bull":20,"base":50,"bear":30},"yield_pct":{"dividend":2.276,"net_buyback":6.0},"second_stage":{"bull_cagr_pct":7,"base_cagr_pct":5},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### ALV_Q2_2026_Earnings_Call_20260717.md
- 2026-07-17｜Mikael Bratt｜guidance：CEO 重申 2026 全年有機銷售持平的財測。（原話："we reiterate our full year 2026 guidance of flat organic sales with"）
- 2026-07-17｜Mikael Bratt｜guidance：全年調整後營業利益率維持約 10.5% 至 11%。（原話："We continue to expect an adjusted operating margin of around 10.5% to 11%."）
- 2026-07-17｜Mikael Bratt｜guidance：財測假設原物料毛逆風約 1.1 億美元。（原話："a gross raw material headwind of approximately USD 110"）
- 2026-07-17｜Mikael Bratt｜guidance：全年預期優於輕型車產量約 2.5 個百分點（有機持平、產量降 2.5%）。（原話："outperform light vehicle production by around 2.5"）
- 2026-07-17｜Mikael Bratt｜guidance：全年營運現金流約 12 億美元。（原話："cash flow is expected to be around USD 1.2 billion"）
- 2026-07-17｜Mikael Bratt｜guidance：全年資本支出低於銷售的 5%。（原話："we expect CapEx to be below 5% of"）
- 2026-07-17｜Mikael Bratt｜guidance：全年稅率預期約 30%。（原話："We expect a tax rate around 30%."）
- 2026-07-17｜Mikael Bratt｜guidance：第三季調整後營業利益率預期與上半年相近。（原話："to be similar to the first half year level"）
- 2026-07-17｜Mikael Bratt｜guidance：客戶補償與工程收入偏重第四季，第四季獲利大幅跳升。（原話："a significant step-up in profitability in the fourth"）
- 2026-07-17｜Mikael Bratt｜guidance：管理層對利益率區間內偏上或偏下端不作表態。（原話："we haven't expressed upper or lower end"）
- 2026-07-17｜Mikael Bratt｜margin：第二季調整後營業利益率 9.6%，年增 30 bp。（原話："The adjusted operating margin was 9.6%, 30 basis points higher."）
- 2026-07-17｜Mikael Bratt｜margin：毛利率下滑，管理層拆解為供應商補償回沖加土耳其資產減損，合計約 80 bp。（原話："which combined reduces gross margin by almost 80"）
- 2026-07-17｜Monika Grama｜margin：第二季美國關稅回收率約 83%（不含 IEEPA），年初至今 78%。（原話："we recovered approximately 83% of our U.S. tariffs"）
- 2026-07-17｜Mikael Bratt｜margin：管理層說明下半年利益率擴張的支撐來源。（原話："we expect margin expansion to be supported by FX, engineering income"）
- 2026-07-17｜Mikael Bratt｜margin：原物料漲價抵銷分三條路：向供應商爭取、內部降本、與客戶議價。（原話："the third leg is then the price adjustments with our customers"）
- 2026-07-17｜Mikael Bratt｜margin：對客戶的價格調整細到零組件層級，並非統一百分比。（原話："It's not a general percentage adjustment"）
- 2026-07-17｜Monika Grama｜margin：IEEPA 退款：從政府拿回約 1,200 萬美元，其中約 900 萬轉給客戶，淨留 300 萬。（原話："we got back around $12 million from the government"）
- 2026-07-17｜Mikael Bratt｜commitment：決定逐步關閉土耳其製造據點，產能移轉至 EMEA 現有工廠。（原話："discontinue our manufacturing operations in Turkey"）
- 2026-07-17｜Mikael Bratt｜commitment：土耳其重組總費用約 1.42 億美元，其中 9,000 萬已於第二季認列。（原話："total restructuring charges of approximately USD 142 million"）
- 2026-07-17｜Mikael Bratt｜commitment：土耳其案預期年化稅前節省約 4,000 萬美元，2027 起顯現、2028 達滿額。（原話："annual pretax savings of approximately USD 40 million"）
- 2026-07-17｜Mikael Bratt｜commitment：土耳其工廠預計 2028 上半年完全關閉，影響約 2,200 名員工。（原話："complete closure anticipated during the first half of 2028"）
- 2026-07-17｜Monika Grama｜commitment：CFO 稱現金流與資產負債表支持持續高水準股東回報。（原話："supports our continued commitment to a high level of"）
- 2026-07-17｜Mikael Bratt｜capital_allocation：第二季買回逾 160 萬股、金額 2 億美元。（原話："repurchasing over 1.6 million shares for USD 200 million"）
- 2026-07-17｜Monika Grama｜capital_allocation：槓桿比率由 1.3x 降至 1.2x，同期股東回報合計 2.64 億美元。（原話："leverage ratio improved from 1.3 to 1.2x during the quarter"）
- 2026-07-17｜Monika Grama｜capital_allocation：近 12 個月現金轉換率 119%，高於至少 80% 的目標。（原話："months was 119% and exceeding our target of at least 80%"）
- 2026-07-17｜Mikael Bratt｜customer：中國區銷售中，中國 OEM 占比由去年 40% 升至 55%。（原話："the Chinese OEMs accounted for 55% of our sales in"）
- 2026-07-17｜Mikael Bratt｜customer：Q&A 中管理層說 2022 年以來對中國 OEM 銷售占中國區比重的提升（此處數字為 65%）。（原話："grown from 22% of our China sales in '22 to 65% China sales"）
- 2026-07-17｜Mikael Bratt｜customer：與長城汽車、小鵬簽署策略合作協議。（原話："we signed strategic cooperation agreements"）
- 2026-07-17｜Mikael Bratt｜customer：印度有機銷售成長 36%。（原話："In India, we grew sales by 36% organically"）
- 2026-07-17｜Mikael Bratt｜customer：美洲表現為負，部分歸因於關稅補償減少與低含量的南美市場成長帶來的不利組合。（原話："The negative performance in the Americas can partly"）
- 2026-07-17｜Mikael Bratt｜customer：管理層對訂單（order intake）不揭露細節，只稱有支持市占的活動。（原話："we don't disclose any details around the current order intake"）
- 2026-07-17｜Mikael Bratt｜competition：歐洲產量展望弱，提到可負擔性問題與中國進口車競爭加劇。（原話："increasing competition from Chinese imports"）
- 2026-07-17｜Mikael Bratt｜competition：管理層對守住市占表達信心。（原話："I think we are in good shape here to"）
- 2026-07-17｜Mikael Bratt｜product：新車上市多在中國，每車含量提升由前中央氣囊帶動。（原話："Higher CPV is driven by Front Center Airbags on"）
- 2026-07-17｜Mikael Bratt｜product：2026 年下半年新車上市數多，主要來自中國 OEM，抵銷美歐較少的上市。（原話："we expect a high number of new product launches"）
- 2026-07-17｜Mikael Bratt｜product：管理層提及零重力座椅作為未來內裝安全機會。（原話："So we call it the zero gravity seat"）
- 2026-07-17｜Mikael Bratt｜risk：波斯灣緊張情勢被列為汽車價值鏈風險。（原話："political tension in the Persian Gulf continue to increase risks"）
- 2026-07-17｜Mikael Bratt｜risk：S&P 自一月起將中國輕型車產量預測下修。（原話："lowered its outlook for China light vehicle production"）
- 2026-07-17｜Mikael Bratt｜risk：公司不直接採購原物料，漲價透過供應鏈傳導。（原話："we don't buy raw materials directly"）
- 2026-07-17｜Mikael Bratt｜risk：利益率區間反映市場波動與通膨壓力是否長期的不確定。（原話："the interval here reflects the"）
- 2026-07-17｜Mikael Bratt｜guidance：敘事變化：全年獲利節奏由年初預期的正常序列改為偏後段，原因是波斯灣帶來的通膨壓力。（原話："more back-end loaded is because we see the inflationary"）
- 2026-07-17｜Mikael Bratt｜customer：管理層稱與客戶就通膨補償的對話與 23–25 年相比沒有改善也沒有惡化。（原話："no change either improved or deteriorated"）
- 2026-07-17｜Mikael Bratt｜product：資本市場日的成長框架（LVP 與含量各 1–2%）管理層稱仍成立，但組合效應使含量成長未達全潛力。（原話："convey that at Capital Markets Day definitely still holds there"）

### 問答異常語氣（迴避／改口／保留）
- ALV_Q2_2026_Earnings_Call_20260717.md｜問：Colin Langan：利益率節奏先前說較線性，現在需要 Q4 約 15% 才達中點，變了什麼？｜答法：承認由年初的正常節奏改為偏後段，歸因於波斯灣帶來的成本壓力與議價時滯；未給 Q3 原物料數字。
- ALV_Q2_2026_Earnings_Call_20260717.md｜問：Colin Langan：原物料是否幾乎 100% 回收？｜答法：回答「No」後改談自助、內部降本、客戶價格調整三個槓桿，未給回收比例。
- ALV_Q2_2026_Earnings_Call_20260717.md｜問：Itay Michaeli：全年利益率區間有無偏上或偏下端？｜答法：不表態，稱最佳判斷就是落在區間內。
- ALV_Q2_2026_Earnings_Call_20260717.md｜問：Itay Michaeli：訂單（order intake）趨勢與對美歐超越市場的影響？｜答法：稱不揭露細節，改以「感覺舒適」「活動水準尚可」概括，未給數字。
- ALV_Q2_2026_Earnings_Call_20260717.md｜問：Agnieszka Vilela：中國 OEM 占比提高對含量與獲利率影響？｜答法：稱獲利率細節不能談、依平台專案而定，改談成長機會與創新。
- ALV_Q2_2026_Earnings_Call_20260717.md｜問：（準備稿與 Q&A 對照）中國 OEM 占中國區銷售比重｜答法：準備稿稱本季 55%（去年 40%），Q&A 中同一指標說成 65%；逐字稿內兩處數字不一致。

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 6 | 2 |
| customer_second_source | found | 2 | 2 |
| customer_concentration_credit | found | 4 | 1 |
| supply_demand_durability | found | 3 | 3 |
| regulatory_antitrust | found | 3 | 2 |
| reg_tariff_export | found | 5 | 2 |
| geo_supply_chain | found | 2 | 2 |
| end_markets | found | 5 | 3 |
| substitute_technology | found | 2 | 2 |
| channel_business_model_shift | found | 3 | 2 |
| capital_markets_pricing | found | 5 | 3 |
| major_events | found | 3 | 5 |
| cyclical_supply_discipline_capacity | found | 5 | 3 |
| cyclical_inventory_price_position | found | 2 | 3 |
| cyclical_prior_downcycle_behavior | found | 3 | 3 |

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260524","verdict":"B｜衛星候選｜分批進場（建議第一批 50% 現價，第二批待 Pure MA ✅ 或拉回 W52 $115 區間加碼）","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"全球市佔結構性擴大（competitor exit + 中國本土化勝出）","columns":{"2Y 驗證":"2026/2027 中國 OEM organic outperform LVP &gt; +30 ppts/yr","5Y 驗證":"全球市佔 2024 ~44% → 2030 ≥ 47%","10Y 驗證":"2035 ≥ 50%（接近 self-imposed cap）","數字門檻":"Q-on-Q 中國 outperform &gt; 30 ppts；年度市佔 ≥ 47% by 2030","信息來源":"Capital Markets Day 2025-06；公司 Investor Presentation","漂移觸發":"連 2 季中國 outperform 收斂至 &lt; +10 ppts → 削弱（2Y）"}},{"id":"H2","text":"Adj OPM 結構提升至 12% mid-cycle","columns":{"2Y 驗證":"FY 2027 Adj OPM ≥ 11.5%（FY 25 ~10.0% → 26 公司目標 10.5-11% → 27 目標 12%）","5Y 驗證":"5Y 平均 Adj OPM ≥ 11.5%","10Y 驗證":"OPM 維持 11-12% range（無 mean reversion 至 9%）","數字門檻":"FY26 ≥ 10.5% / FY27 ≥ 11.5% / FY28 ≥ 12%","信息來源":"2025-06 CMD slide deck；Q1 26 earnings call","漂移觸發":"連 4 季 OPM &lt; 9.5% → 削弱（5Y 假設）"}},{"id":"H3","text":"Fwd PE re-rate 至 13-14x（PEG ~1.2-1.3）","columns":{"2Y 驗證":"2026/2027 Fwd PE 達 12-13x（觸發 sector re-rate）","5Y 驗證":"5Y 維持 Fwd PE ≥ 12x median","10Y 驗證":"無 secular de-rate 至 8-9x（commodity 化情境）","數字門檻":"NTM Fwd PE 進入 12-14x 區間 ≥ 6 個月","信息來源":"sector 比較 GNTX / LEA Fwd PE 平均 10x；ALV 隱含 fair value 13x","漂移觸發":"連 4 季 Fwd PE &lt; 9x → 反轉（2Y 假設）"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"NA / EU LVP 持續下行（衰退）拖累整體 organic 至負值","columns":{"對應假設":"H1 / H2","時間尺度":"⚡ 短期（1-2 季可觸發）","監測指標":"S&amp;P Global LVP 月報（NA / EU 區）","警戒閾值":"連 2 季 NA + EU 合計 LVP &lt; -3% → 削弱（公司 -1% LVP 假設不再成立）"}},{"id":"R2","text":"中國本土供應商搶單（Joyson、Denso-BYD JV、Toyoda Gosei 中國組 share gain）","columns":{"對應假設":"H1","時間尺度":"🔥 中期（4-6 季）","監測指標":"China outperform vs LVP gap（Q-on-Q）","警戒閾值":"連 4 季 China outperform 從 +43 ppts 收斂至 &lt; +10 ppts → 中國組 share 流失"}},{"id":"R3","text":"ARC airbag MDL 訴訟賠付 + 可能擴大 recall（類似 Takata 模式）","columns":{"對應假設":"H3（無資本損害）","時間尺度":"🐢 長期（2+ 年慢變數）","監測指標":"10-K / 10-Q 法律準備金科目 / MDL 件數變化","警戒閾值":"累積準備金 &gt; $500M 或 NHTSA 強制 recall 數量 &gt; 10M 件 → 跨年度監控；單一新增 case 不觸發"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🟢","ma":"🟡","trap":"🟢","moat_trend":null,"runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":122.73,"archetype":null,"cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"ALV","date":"2026-10-24","schema":"v15.2","contract":"v19","company_name":"Autoliv, Inc."},"oneliner":"全球被動安全龍頭（份額約44%），靠回購與利益率撐每股盈餘；12%利益率目標未兌現、2027原物料壓力延續，預估本益比約11倍屬合理，等1月底2027指引再決定","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ALV_20261024/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ALV_20261024/scenario.json","answers":{"q1_business":{"verdict":"賺全球車廠被動安全採購的錢（氣囊與方向盤約三分之二、安全帶約三分之一）；錢卡在車型平台定點與成本補償談判兩個節點，量跟著汽車產量走","reasoning":"第三季淨銷售26.93億美元（年減0.5%），有機−1.1%，優於全球輕型車產量−1.9%；毛利率18.4%（去年同期19.3%，約一半來自去年一次性供應商補償），調整後營業利益率9.7%、GAAP 9.4%（2026-10-23新聞稿與法說）。營收分部：區域上美洲34%、中國20%、亞洲（不含中國）20%、EMEA 26%（第三季，含暑休）；產品上氣囊與方向盤約67%、安全帶約33%（Moody's 2026-06）。收錢方式是車型平台定點後依實際產量出貨，沒有保底量，原物料與關稅靠事後補償談判回收。單點依賴：無單一客戶超過營收10%，最大單一合約約2%，前五大約44%、前十大約70%，客戶集中度不構成單點風險；真正的單點是汽車產量景氣。產業時鐘判收縮期：全球輕型車產量2026年預估−1.9%、第四季−4.5%、中國第四季−9%，2027預估+1.55%。全年指引：有機約0%、調整後利益率約10.5%、營運現金流約12億美元。","fact_refs":["f_kpi0_net_sales_gaap","f_kpi1_adjusted_operating_incom","f_kpi2_gaap_operating_income_ma","f_kpi5_management_guidance_fy20","f_peer_alv_gross_margin_pct","f_peer_alv_operating_margin_pct","f_earnings_recency"],"verdict_values":{"revenue_quality":"依客戶車型實際產量出貨、無保底量，隨輕型車產量循環；原物料與關稅成本靠補償回收，有一到兩季落後","unit_econ_note":"單車安全內容由前中央氣囊、行人保護與印度安全規範拉升（印度第三季有機成長近30%）；產品單價走勢事實表未涵蓋","archetype":{"primary":"循環/商品","secondary":"品質複利成長","confidence":"中","fingerprint":"營收綁汽車產量、毛利率約19%、2009年營業利益曾年減78%；但全球份額約44%、調整後投入資本報酬約24%"},"industry":{"clock_phase":"IV","sd_verdict_source":"供需持久性：需求是週期性（輕型車產量2026年約−1.9%、2027預估+1.55%）疊加結構性單車內容成長；供給端Autoliv關閉土耳其廠收縮EMEA產能，Joyson在匈牙利擴產，供給可逆性中等；判週期性，下一段反轉向上但幅度小","bargaining":{"up":"不直接買原物料，漲價經供應鏈傳導（2026毛衝擊估約1.2億美元）；半導體與感測器受出口管制影響，上游議價中等","down":"車廠議價強：前五大客戶約44%，關稅回收約八成，物流成本幾乎無法轉嫁，價格調整細到零組件逐項談","geo":"中國本土車廠占Autoliv中國銷售由2022年22%升到本季58%；比亞迪自製被動安全，日韓系車廠多由集團關係企業供貨"},"profit_pool_dir":"利潤池往中國本土車廠與印度移動；Autoliv跟得上量，但本土車廠業務的利潤率管理層不揭露","tam_table":{"expanded":false,"reason":"被動安全已是成熟市場（Autoliv份額約44%、前氣囊數量年增約1.3%），論點不靠滲透率或新品類；成長來源在成長題以量、單車內容、回購拆解"}}}},"q2_moat":{"verdict":"護城河持平：規模與認證讓Autoliv利益率高於同業3～5個百分點，份額長期升到約44%，但管理層目標已改成守住份額，中國垂直整合壓著定價力","reasoning":"份額由1997年27%升到2025年約44%，歐洲52%、美洲47%、中國33%（10-K、Moody's）。同業利潤率（TTM）：Autoliv營業利益率9.18%、FCF利潤率6.83%；Joyson 5.81%、0.64%；Magna 5.48%、7.52%；Lear 3.67%、3.58%，差距是規模優勢的可觀察證據，同業ROIC事實表未涵蓋。方向判持平：執行面擴大（直接人工生產力持續改善，第三季在新增成本逆風下利益率優於預期），定價面持平（關稅回收約八成、原物料與物流部分自行吸收）。2026-10-23法說CEO說全球份額目標是守住現有份額，不是擴張；中國本土車廠占比快速上升，Autoliv跟得上，但比亞迪自製、只向Autoliv買氣體產生器。當期報酬屬低利益率×高周轉，四檢查點見下，內生成長上界約2.4%。","fact_refs":["f_peer_alv_gross_margin_pct","f_peer_alv_operating_margin_pct","f_peer_alv_fcf_margin_pct","f_peer_600699_ss_gross_margin_pct","f_peer_600699_ss_operating_margin_pct","f_peer_600699_ss_fcf_margin_pct","f_peer_mga_operating_margin_pct","f_peer_mga_fcf_margin_pct","f_peer_lea_operating_margin_pct","f_peer_lea_fcf_margin_pct"],"verdict_values":{"moat":{"mechanism":"規模加安全認證：每個車型平台要通過碰撞驗證並承諾整個車型週期供貨，約44%全球份額帶來成本與工程攤提優勢；換供應商通常只在新車型招標時發生","execution":8,"pricing":6,"grade":"B","trend":"→","trend_evidence":"執行力擴大（生產力提升、利益率高於同業），定價力持平（關稅回收約八成、原物料與物流部分吸收）；管理層份額目標為守住，中國區份額33%低於歐美","competitor_notes":[{"name":"Joyson（600699.SS）","strategy_note":"毛利率接近Autoliv，但營業利益率與現金流明顯較低；匈牙利擴建全球最大被動安全廠，代表在歐洲以產能搶單"},{"name":"ZF","strategy_note":"Moody's列為主要對手之一，未在同業表內，無數字可比"},{"name":"Toyoda Gosei（7282.T）","strategy_note":"取得豐田體系多數被動安全業務，同業表營收缺值無法比較，是日系客戶的天花板"},{"name":"比亞迪弗迪科技","strategy_note":"比亞迪自製被動安全，Autoliv只供氣體產生器，代表中國垂直整合的上限"},{"name":"MGA","strategy_note":"車身與座椅零件為主，非直接被動安全對手，只作利潤率參考"},{"name":"LEA","strategy_note":"座椅與電子為主，利潤率最低，只作利潤率參考"}],"peer_na_reason":"同業ROIC事實表未涵蓋，以營業利益率與FCF利潤率差距代理；ZF未上市不在表內","threats":[{"level":"🟡","text":"中國本土車廠垂直整合（比亞迪自製）與日韓系車廠由集團關係企業供貨，限制Autoliv在成長最快客群的份額與價格","p":"30%","evidence_refs":["competitive_share_entrants#2","customer_second_source#1"]},{"level":"🟡","text":"中國、韓國、印度預期有更多本土與國際競爭者進入，可能帶來降價與毛利下滑","p":"30%","evidence_refs":["competitive_share_entrants#3"]},{"level":"🟡","text":"Joyson在匈牙利擴產而EMEA整體產能過剩（Autoliv自己關閉土耳其廠），歐洲價格壓力上升","p":"30%","evidence_refs":["cyclical_supply_discipline_capacity#4","supply_demand_durability#0"]}],"roic_durability":{"quadrant":"低利益率×高周轉","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者是乘客、決策者是車廠、付款者是買車的人，三者都成立；安全配備受法規與碰撞評等強制，是需要不是想要，印度單車內容上升也來自安全規範（2026-10-23法說）"},{"item":"決策層級","level":"🟡","text":"替代性要在單一車型平台招標這一層看：一旦定點通常供貨整個車型週期，期間換供應商要重做碰撞驗證；但每次新車型都重新招標，最大單一合約只占約2%，轉換成本只在週期內有效"},{"item":"價值鏈分配","level":"🟡","text":"車廠拿走大部分議價：關稅只回收約八成、物流成本難轉嫁、原物料補償有落後；比亞迪自製證明大型車廠有能力把這一環收回自己做，Autoliv毛利率約19%反映這個分配"},{"item":"社會容忍度","level":"🟡","text":"安全產品社會支持度高，但不容許聯合定價與品質瑕疵：曾因歐盟反壟斷認罪，BMW仍在德國求償約9,500萬歐元，ARC氣體產生器集體訴訟未結；價格上限受這兩條約束"}],"roiic":"約17%（以調整後投入資本報酬24%扣30%稅率代理；增量值事實表未涵蓋）","reinvest_rate":"約14%（FY2023–FY2025（淨利−自由現金流）÷淨利）","endo_ceiling":2.4,"formula_note":"投入資本報酬24%為公司調整後口徑（2026第三季法說CFO），扣約30%稅率得稅後約17%；再投資率以三年（淨利−自由現金流）÷淨利＝（79＋166＋19）÷1,869百萬美元≈14%代理資本支出減折舊加營運資金增加；內生成長≈17%×14%≈2.4%"}}}},"q3_growth":{"verdict":"五年後跑道中等：份額已約44%、前氣囊數量年增約1.3%，成長靠單車內容與守份額；電池安全開關等新業務還在起步，不算第二條曲線","reasoning":"成長拆解：量（全球輕型車產量長期約0～2%）＋單車內容（資本市場日框架1～2%，2026-07-17法說CEO說仍成立，但組合效應讓含量成長沒發揮全部潛力）＋回購（每年縮股約5%）；價格以補償為主，不是成長來源。共識三年EPS：FY2025A 9.55到FY2028E 13.19，年化約11.4%（Koyfin共識，家數事實表未涵蓋；基期是GAAP、共識多為調整後口徑，可能略高估）。內生上界約2.4%，缺口約9個百分點，歸因：淨回購約5～6個百分點、利益率由約10%走向12%約3～4個百分點，大致可完全歸因，不靠估值重評。營收共識FY2026約111億、FY2027約114億美元（年增約2.4%）。衰退信號亮兩項，長期成長性與陷阱風險都判中等。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m"],"verdict_values":{"growth":{"driver_mix":"量（輕型車產量約0～2%）＋單車內容（約1～2%，印度與前中央氣囊）＋回購（約5%/年）；價格補償不算成長","runway_years":"不適用滲透率換算：份額約44%已成熟，成長來自單車內容與守住份額","runway_post_y5":"🟡","endo_ceiling_basis":"報酬持續期推導：稅後投入資本報酬約17%×再投資率約14%≈2.4%","segments":{"expanded":false,"reason":"公司只有被動安全單一業務，氣囊與安全帶的分產品利潤率未揭露，組合變化不是決定利潤的主因；區域組合影響已在毛利率與議價段處理"},"decay_signals":["毛利率連兩季年減：亮（第二季含土耳其減損與補償回沖約80基點，第三季18.4%對19.3%）","EPS成長高於營收成長逾5個百分點：亮（2022–2025年EPS年化約25%、營收約7%；前瞻約11%對約2.4%）","核心市占近12個月縮減：未亮（全球仍超越產量，但EMEA第三季落後3.7個百分點要追蹤）","FCF／淨利連兩年低於0.75：未亮（2024約0.74、2025約0.97）","提價後銷量下滑：未亮","SBC占營收超過5%：未亮（股數五年減約18%）","TAM萎縮或被替代：未亮（前氣囊數量2026–2033年增約1.3%）","產業倍數三年系統性下移：事實表未涵蓋","維護性資本支出占FCF超過60%：事實表未涵蓋","停止投資新產能且營收下滑：未亮（蕪湖新氣囊廠2027投產）"],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"資本配置良好：現金轉換達標、持續縮股、槓桿低，回購價格對應的盈餘殖利率約8%","reasoning":"FCF／淨利：2023約0.84、2024約0.74、2025約0.97；第三季自由營運現金流1.24億美元、現金轉換率80%（目標至少80%）。現金去向：資本支出約占營收4%（2026指引由低於5%下調，管理層說是時點與優先高回收專案），股息每季約0.63億美元，回購第二季2億、第三季1.5億美元，近12個月回饋股東約7.6億美元、近五年29億美元並縮股約18%；無併購。槓桿1.3倍（上季1.2倍），淨負債約18.9億美元，剩餘回購授權約19億美元。營運槓桿：第三季營收年減0.5%、調整後營業利益年減3%，差2.5個百分點，未到壓縮警戒。SBC金額事實表未涵蓋，但股數淨減少。","fact_refs":["f_kpi3_free_operating_cash_flow","f_net_debt_m","f_shares_diluted_m","f_dividend_yield_ttm","f_consensus_eps_fy1"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":false,"passed":null,"input":"近12個月無併購完成（8-K未見併購完成項目），不適用"},{"name":"buyback_yield","applicable":true,"passed":true,"input":"第二、三季回購均價約125美元（2億÷160萬股、1.5億÷120萬股），對FY1共識EPS 10.32的盈餘殖利率約8.3%；10年期公債殖利率事實表未涵蓋，需高於約6.3%才不過，判過但未直接驗證"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"近五年流通股數約減18%（2026-10-23法說CFO），淨稀釋為負；SBC金額事實表未涵蓋"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購，近12個月無併購；股東回報以回購和股息為主，已在本題理由與計分項列出"}}}},"q5_valuation":{"verdict":"現價要的是利益率守住10.5%、回購每年縮股約5%，換年化約10%的報酬，這個我信；要多賺得靠12%利益率兌現，這部分現價沒有給折扣，判合理不判便宜","reasoning":"現價114.67美元，FY1共識EPS 10.32，預估本益比11.1倍；FY2共識11.59對應約9.9倍。歷史本益比只有4個年度端點，現值分位約45%，不是五年分位，五年分位留空。PEG以三年共識EPS年化約11.4%計約0.97，但其中5～6個百分點靠回購，扣掉後成長約6%，實質PEG約1.9。FY1共識近三個月上修1.9%，最新一次FY2下修0.43%。股息殖利率約2.3%。賣方目標價均值約131～135美元（都是第三季財報前資料）。基準情境（利益率約11%、本益比11.5倍）含股息年化約11%，屬中等；多頭要靠利益率到12%加本益比回到13.5倍。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_pe_current","f_pe_percentile","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_3m_fy1_pct","f_consensus_rev_fy2_pct","f_dividend_yield_ttm","f_ev_s_fwd"],"verdict_values":{"valuation":{"basis":"預估本益比（FY1共識）為主，PEG與自身年度端點為輔；同業本益比事實表未涵蓋","peers":{"expanded":false,"reason":"事實表同業對照只有利潤率、沒有同業本益比，不能拿來當估值錨"},"fwd_pe":11.11,"peg":0.97,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"預估本益比11.1倍、年度端點分位約45%（只有4點，非五年分位）、帳面PEG約0.97看似便宜；但三年EPS成長約11%裡有5～6個百分點來自回購，扣掉後實質PEG約1.9；基準情境年化約11%屬中等，故判合理而非便宜","upside_short_pct":13,"upside_mid_pct":25,"denominator_disputed":false,"denominator_note":"FY1分母含工程收入時點與關稅補償，但沒有單一大額一次性；FY2025基期為GAAP、共識為調整後口徑，差異小，不構成爭點。短期上檔以FY2027基準EPS 11.3×11.5倍計，中期以FY2028基準EPS 12.5×11.5倍計"}}},"q6_how_wrong":{"verdict":"最可能看錯在：汽車景氣下行與利益率目標落空同時發生，回購撐不住每股盈餘","reasoning":"空方最強數字：2009年營業利益年減78%、2020年第二季銷售年減51%並轉虧且取消股利、2022首季調整後利益率只剩3.2%。法說迴避紀錄：2026-07-17法說不揭露訂單、不談本土車廠利潤率，準備稿說中國本土車廠占中國銷售55%、問答說成65%，前後不一（以本季新聞稿58%為準）。未決訴訟：ARC氣體產生器集體訴訟未提列且無法估計區間，BMW求償約9,500萬歐元，墨西哥稅務爭議在初期。最大回撤估−35%～−50%，依據見情境假設；各視角反證見反證紀錄。","fact_refs":["f_week26_return_pct","f_rsi14","f_kpi1_adjusted_operating_incom"],"verdict_values":{"trap":{"verdict":"🟡","label":"兩項衰退信號亮燈：毛利率連兩季年減、每股盈餘成長遠高於營收成長"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":10.32,"pe":11.11,"basis":"FY2026E共識EPS（FY1）與判斷日收盤114.67美元；終端倍數同樣套在當年度預估EPS"},"eps":{"bull":[11.8,13.5,15.2,16.8,18.5],"base":[11.3,12.5,13.5,14.5,15.4],"bear":[9.6,7.8,9.0,10.0,10.8]},"pe":{"bull":13.5,"base":11.5,"bear":9.0},"p":{"bull":20,"base":50,"bear":30},"yield_pct":{"dividend":2.28,"net_buyback":6.0},"second_stage":{"bull_cagr_pct":7,"base_cagr_pct":5},"max_dd":{"lo":-50,"hi":-35,"basis":"汽車供應商下行期營運跌幅極深：2009年營業利益年減78%、2020年第二季銷售年減51%並轉虧、2022首季調整後利益率3.2%；股價歷史回撤事實表未涵蓋，以本益比由11倍壓到8倍（約−27%）乘EPS下修25～35%推得約−45%～−53%，取−35%～−50%","trigger_time":null},"basis":{"bull":"2027原物料壓力解除、2028達12%利益率，份額守住並隨本土車廠與印度成長，股數每年減約5%；本益比回到13.5倍（前份合理區間上緣，同業本益比事實表未涵蓋）","base":"利益率停在約11%（低於12%目標），有機成長年約2%，股數年減約4～5%；本益比維持11.5倍，與現值11.1倍相近；EPS路徑已含縮股，回購殖利率只供拆解，不應重複計入報酬","bear":"2027–2028汽車下行：全球產量年減5%以上、利益率掉到7～8%（比照2022年調整後6.8%），2028年EPS約7.8後緩慢修復；本益比壓到9倍（成長熄火、商品化錨）"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"2009營業利益年減78%、利益率1.3%；2020第二季銷售年減51%並轉虧、取消股利；2022首季調整後利益率3.2%；2025第四季部分車廠無預警停產調庫存","assumption":"汽車景氣只是溫和下行（2026全球產量約−1.9%）","consequence":"若2027–2028出現實質衰退，EPS掉三成以上、本益比壓到8倍，股價可腰斬","ruling":"採納：放進熊市情境30%機率與最大回撤−35%～−50%；與唯一致命點部分重疊（都經由利益率），衰退是外部觸發，2027利益率指引是能觀察的關口","watch":"S&P Global Mobility季度產量、車廠停產公告","evidence_refs":["cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#1","cyclical_prior_downcycle_behavior#2","cyclical_inventory_price_position#1"]},{"view":"論點失敗","evidence":"單一小零件缺貨可迫使產品停產且可能持續很久；半導體與感測器受出口管制；固定價合約下關稅可能無法轉嫁","assumption":"供應鏈中斷是一次性","consequence":"類似2021–2022晶片短缺時利益率掉到6.8%","ruling":"部分採納：已含在熊市利益率假設中，不另加機率","watch":"關稅回收率、財報中缺料停產揭露","evidence_refs":["geo_supply_chain#0","reg_tariff_export#1"]},{"view":"論點成功但股東經濟變差","evidence":"中國本土車廠占中國銷售58%且仍升；比亞迪自製、Autoliv只供氣體產生器；管理層不談本土車廠利潤率；BMW求償約9,500萬歐元、ARC集體訴訟未提列","assumption":"跟著本土車廠成長的營收和原有營收一樣賺錢","consequence":"份額守住、營收成長，但利益率卡在10～11%，法律支出吃掉部分回購","ruling":"採納：基準情境利益率用11%，不給12%","watch":"中國區利益率（若揭露）、法律提列","evidence_refs":["competitive_share_entrants#2","customer_second_source#1","regulatory_antitrust#2","major_events#1"]},{"view":"價格已反映太多","evidence":"全年利益率指引收窄到下緣；第三季稀釋EPS年減6.8%；TD Cowen降至持有、目標價148降到137；三年共識EPS成長約11%裡回購占5～6個百分點","assumption":"預估本益比11倍就是便宜","consequence":"若利益率停在10.5%，EPS成長只剩回購，11倍只是合理價","ruling":"採納：估值判合理而非便宜，不追價","watch":"FY2共識EPS修正方向","evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#3","capital_markets_pricing#1"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 🟡 → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=🟡","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 122.73 → 本次 114.67（-6.6%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=122.73","side_b":"本次 price_at_dd=114.67","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 122.73 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 122.73 美元：五年期望值 前份未列，基準年化 前份未列，前份未列不對稱比","side_b":"本次情境、股價仍用 122.73 美元：Bull 價 249.75、Bear 價 97.2，五年期望值 +36.6%，基準年化 7.6%，不對稱比 3.32","ruling":"先換情境、股價不動：五年期望值與基準年化前份未列，無法比較。前份未列不對稱比，本次為 3.32。Bull、Bear 價位與股價無關，只受情境影響。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 122.73 美元：五年期望值 +36.6%，基準年化 7.6%，不對稱比 3.32","side_b":"本次情境、股價 114.67 美元：五年期望值 +46.2%，基準年化 9.1%，不對稱比 5.15","ruling":"再換股價、情境不動：起點價下跌 6.6%，五年期望值多 9.6 個百分點，基準年化多 1.5 個百分點，不對稱比由 3.32 升到 5.15。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"利益率能否走向12%","cause":null,"side_a":"管理層：第三季9.7%優於先前預期，第四季隱含約14%，12%中期目標不變，新技術可帶來更大幅生產力提升（2026-10-23法說，CEO）","side_b":"全年指引由10.5～11%收窄到下緣10.5%，年初以來新增成本逆風170～180基點，2027原物料壓力與2026相當，物流成本難轉嫁（同場CEO與CFO）；2026-07-17法說已把獲利節奏改為偏後段","ruling":"不可調和，採B側當基準：情境基準利益率用約11%而非12%；依據是全年兩度靠第四季補償與工程收入撐場","evidence_level":"公司指引與法說原話","settle_metric":"2027-01-29公布的2027利益率指引與2026第四季實際利益率","if_then":["若2027指引≥11%且2026全年實際≥10.3%→首倉2%","若第四季實際<12%或2027指引<10.5%→不建倉，熊市權重升到40%","反向：若指引前股價先漲到130美元以上→不追"],"evidence_refs":["capital_markets_pricing#0","cyclical_inventory_price_position#0"]},{"axis":"現在就買的最強論證","cause":null,"side_a":"股息殖利率約2.3%加回購約6%，總股東回報約8%；預估本益比11.1倍；前份第二批加碼價位（52週均線約115美元）已到","side_b":"第四季全球產量預估年減4.5%，下行期營業利益曾一年跌78%；等三個月看指引的機會成本約2%","ruling":"不採納現在買：等事件的代價小，下行尾巴長","evidence_level":"財報與法說","settle_metric":"2027-01-29指引","if_then":["若指引前股價跌到100美元以下且第四季利益率≥13%→分批反買首倉1%","若指引達標→照首倉2%執行"]},{"axis":"中國超越幅度與份額論點","cause":"新證據","side_a":"前份：中國區超越產量超過30個百分點、警戒線低於10個百分點；2030全球份額≥47%","side_b":"本季中國區整體只超越約1個百分點（本土車廠超越近20個百分點、對全球車廠銷售年減約29%）；2026-10-23法說CEO說全球份額目標是守住","ruling":"前份中國警戒線本季已觸及一次；本土車廠占比升到58%後，整體超越幅度被全球車廠在華衰退拖累，改用中國區相對產量連續落後季數與本土車廠超越幅度判讀；份額擴張到47%的論點撤回，改成守住約44%","evidence_level":"新聞稿與法說","settle_metric":"中國區有機成長減中國產量的連續季數","if_then":["若中國區連4季落後產量→減碼一半","若本土車廠超越幅度回到20個百分點以上且中國區轉正→恢復份額論點"],"evidence_refs":["competitive_share_entrants#2"]},{"axis":"利益率門檻","cause":"新證據","side_a":"前份：FY2026≥10.5%、FY2027≥11.5%、FY2028≥12%","side_b":"本次：FY2026≥10.3%、FY2027≥11%、FY2028≥11.5%","ruling":"2026指引收窄到下緣、2027原物料壓力延續，門檻下調約半個百分點；12%目標管理層仍維持，但不當基準","evidence_level":"公司指引"},{"axis":"估值論點","cause":"方法變動","side_a":"前份第三個論點押本益比重評到13～14倍","side_b":"本次不把重評當論點，改成現金轉換支撐的縮股","ruling":"同業本益比事實表未涵蓋，無法佐證13倍合理值；報酬改由EPS複利與股息構成，不依賴估值重評","evidence_level":"方法"},{"axis":"綜合評級","cause":"價格變動","prior_field":["signal"],"side_a":"前份評級B，股價122.73美元","side_b":"本次評級B，股價114.67美元（約−6.6%）","ruling":"股價下跌、FY1共識三個月上修1.9%讓估值變便宜一些，但同期利益率指引收窄到下緣、衰退信號亮兩項，兩邊抵銷，評級維持B","evidence_level":"價格與共識"},{"axis":"估值結論","cause":"新證據","prior_field":["val"],"side_a":"前份判便宜（以13倍為合理本益比）","side_b":"本次判合理","ruling":"扣除回購後EPS成長約6%，實質PEG約1.9；2026利益率指引落在下緣、第三季稀釋EPS年減6.8%、FY2共識小幅下修、TD Cowen降評","evidence_level":"新聞稿與賣方評等","evidence_refs":["capital_markets_pricing#1"]},{"axis":"價值陷阱風險","cause":"新證據","prior_field":["trap"],"side_a":"前份判陷阱風險低","side_b":"本次判中等","ruling":"毛利率第二、三季連續年減，EPS成長遠高於營收成長，兩項衰退信號亮燈","evidence_level":"財報"},{"axis":"首次填入欄位","cause":"方法變動","prior_field":["moat_trend","runway_post_y5","archetype","cycle_position","max_dd_pct","p_bull_pct","p_bear_pct"],"side_a":"前份這些欄位是空值（前份結論文字為分批進場）","side_b":"本次首次填入：護城河方向持平、五年後跑道中等、歸類循環型、位於中循環、最大回撤−35%～−50%、多頭20%／熊市30%","ruling":"這些變動來自新流程首次要求填欄，不代表基本面轉變；結論由分批進場轉為等指引，原因見利益率那條","evidence_level":"方法"},{"axis":"加碼條件","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"前份未設重啟條件，只寫第二批待週線均線轉強或拉回52週均線115美元區間加碼","side_b":"2027-01-29指引調整後營業利益率≥11%且2026全年實際≥10.3%","ruling":"加碼條件由價格錨改成事件錨：利益率路徑未決時不設進場價；價格已到前份加碼區但證據沒到","evidence_level":"方法"},{"axis":"減碼與清倉門檻","cause":"方法變動","side_a":"前份未設減碼或清倉量化門檻，只有風險表警戒值","side_b":"新設：全年利益率<9.5%、全年有機超越<0、中國區連4季落後、ARC提列或和解>3億美元或強制召回令→清倉、槓桿>2倍","ruling":"把前份風險警戒值改成可執行的減碼與清倉條件","evidence_level":"方法"},{"axis":"Single Thing","cause":"方法變動","side_a":"前份未設唯一致命點（Single Thing為空）","side_b":"2027-01-29公布的2027調整後營業利益率指引中位數低於11%","ruling":"Single Thing改成數學上最大的敏感項：利益率每差1個百分點，EPS約差一成","evidence_level":"方法"},{"axis":"ARC訴訟門檻","cause":"方法變動","side_a":"前份：累積準備金超過5億美元或強制召回超過1,000萬件","side_b":"累計提列或和解超過3億美元，或NHTSA對Autoliv產品下強制召回令→清倉","ruling":"3億美元約等於半年回購、市值約3.6%，足以打斷縮股論點；召回改看有沒有強制令，因件數揭露時點落後","evidence_level":"方法","evidence_refs":["lawsuit_class_action#0"]},{"axis":"產業態勢三軸","cause":null,"side_a":"競爭軸惡化：Joyson在匈牙利擴產、中國垂直整合、亞洲新進者","side_b":"結構軸轉好：EMEA關廠收縮產能、印度與中國單車內容上升、關稅回收約八成；其他軸：反壟斷民事求償、ARC訴訟、出口管制","ruling":"雙向拉鋸：份額守得住，但定價力沒有變強","evidence_level":"10-K、新聞稿、產業報導","evidence_refs":["cyclical_supply_discipline_capacity#4","supply_demand_durability#0"]}],"triggers":[{"n":1,"text":"2027調整後營業利益率指引中位數低於11%","type":"Single Thing","maps_to":"H2","metric":"2027全年調整後營業利益率指引","threshold":"低於11%","action":"不建倉；已持有者減碼一半","source_freq":"年度（第四季法說）","date":"2027-01-29"},{"n":2,"text":"利益率路徑獲確認","type":"估值rearm","maps_to":"H2","metric":"2027利益率指引與2026全年實際","threshold":"指引≥11%且2026實際≥10.3%","action":"首倉2%","source_freq":"年度","date":"2027-01-29"},{"n":3,"text":"全年有機成長領先全球產量幅度不足","type":"假設驗證","maps_to":"H1","metric":"全年有機成長減全球輕型車產量","threshold":"低於1個百分點","action":"停止加碼","source_freq":"年度","date":"2027-01-29"},{"n":4,"text":"中國區連續落後產量","type":"風險","maps_to":"R2","metric":"中國區有機成長減中國輕型車產量","threshold":"連2季低於0","action":"減碼一半","source_freq":"季","date":null,"evidence_refs":["competitive_share_entrants#3","customer_second_source#1"]},{"n":5,"text":"第四季利益率未達隱含水準","type":"減碼","maps_to":"R1","metric":"2026第四季調整後營業利益率","threshold":"低於12%（全年指引隱含約14%）","action":"減碼一半","source_freq":"季","date":"2027-01-29","evidence_refs":["cyclical_inventory_price_position#0"]},{"n":6,"text":"ARC氣體產生器案惡化","type":"清倉","maps_to":"R3","metric":"累計提列或和解金額；NHTSA召回令","threshold":"超過3億美元或強制召回令","action":"清倉","source_freq":"季報或有負債附註","date":null,"evidence_refs":["major_events#1","lawsuit_class_action#0"]},{"n":7,"text":"首倉後價格回落且利益率改善","type":"加碼","maps_to":"H3","metric":"股價與季度利益率","threshold":"股價≤100美元且季度利益率年增","action":"分批加碼到4%","source_freq":"季","date":null},{"n":8,"text":"估值先走而利益率沒跟上","type":"減碼","maps_to":"H2","metric":"FY2共識預估本益比","threshold":"≥13倍（約150美元）且利益率仍低於11%","action":"減碼到2%","source_freq":"日","date":null},{"n":9,"text":"汽車產量實質衰退","type":"風險","maps_to":"R4","metric":"全球輕型車產量年增率","threshold":"連2季低於−5%","action":"停止加碼","source_freq":"S&P Global Mobility月報","date":null,"evidence_refs":["cyclical_prior_downcycle_behavior#0","geo_supply_chain#1"]},{"n":10,"text":"上海投資人日檢查中國業務與中期目標","type":"複審日期","maps_to":"H1","metric":"本土車廠業務利潤率與中期目標","threshold":"是否更新12%目標與中國份額","action":"重跑研究","source_freq":"一次","date":"2027-04-26"}],"kill_metrics":[{"metric":"全年調整後營業利益率","bear_threshold":"2027全年低於9.5%","window":"FY2027","source":"公司財報新聞稿","last_status":"ok"},{"metric":"全年有機成長減全球輕型車產量","bear_threshold":"低於0個百分點","window":"FY2026–FY2027","source":"財報新聞稿與S&P Global Mobility","last_status":"ok"},{"metric":"中國區有機成長減中國輕型車產量","bear_threshold":"連4季落後","window":"2026Q4–2027Q3","source":"財報新聞稿","last_status":"warning"},{"metric":"ARC氣體產生器案累計提列或和解","bear_threshold":"超過3億美元或NHTSA強制召回令","window":"持續","source":"10-Q與10-K或有負債附註","last_status":"ok"},{"metric":"淨負債÷調整後EBITDA","bear_threshold":"高於2.0倍","window":"任一季","source":"季報槓桿比率","last_status":"ok"}],"action_conditions":{"rearm_trigger":"2027-01-29指引調整後營業利益率≥11%，且2026全年實際≥10.3%","exec_line":"條件成立後首倉2%；下一季利益率年增再加到4%；任一清倉條件觸發即出場","holding_cap":"4%"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":"中循環","cycle_verdict":"未觸發","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":false,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等2027-01-29法說：2027調整後營業利益率指引≥11%且2026全年實際≥10.3%","asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null},"thesis":{"H":[{"id":"H1","text":"靠中國本土車廠與印度單車內容，Autoliv持續跑贏全球輕型車產量並守住約44%份額","2y":"2026、2027年有機成長領先全球產量至少1.5個百分點（2026指引約2個百分點）","5y":null,"10y":"全球被動安全份額維持約44%以上","threshold":"年度領先至少1.5個百分點；本土車廠銷售成長領先中國產量至少10個百分點","source":"季度財報新聞稿、S&P Global Mobility產量、10-K份額揭露","drift_rule":"領先幅度連2季低於門檻削弱，連3季轉為落後反轉"},{"id":"H2","text":"調整後營業利益率由約10.5%走向11%以上，12%為上檔","2y":"FY2027至少11%","5y":"FY2028–FY2031平均至少11.5%","10y":null,"threshold":"FY2026至少10.3%、FY2027至少11%、FY2028至少11.5%","source":"公司指引與季度新聞稿；土耳其關廠自2027起年省約4,000萬美元","drift_rule":"TTM利益率連4季低於路徑值5%以上（約低於10.4%）削弱，連6季低於10%以上（約低於9.9%）反轉"},{"id":"H3","text":"現金轉換率至少80%支撐每年約4～5%股數縮減，槓桿不超過1.5倍","2y":null,"5y":"2031年稀釋股數不超過約59百萬股（現約72百萬股）","10y":null,"threshold":"年度股數減少至少4%、淨負債÷EBITDA不超過1.5倍、現金轉換率至少80%","source":"10-Q股數、季報槓桿比率與現金轉換率","drift_rule":"連4季回購金額低於前4季一半或槓桿超過1.5倍削弱；回購暫停或股利刪減反轉"}],"R":[{"id":"R1","text":"原物料與物流成本回收不足，利益率指引再下修","h_ref":"H2","clock":"⚡","threshold":"2026全年調整後營業利益率低於10.2%，或2026第四季低於12%","evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#1","cyclical_inventory_price_position#0"]},{"id":"R2","text":"中國本土車廠垂直整合、亞洲新競爭者與Joyson擴產侵蝕份額或價格","h_ref":"H1","clock":"🔥","threshold":"中國區有機成長連4季落後中國產量，或本土車廠超越幅度連2季低於5個百分點","evidence_refs":["competitive_share_entrants#2","competitive_share_entrants#3","customer_second_source#1","cyclical_supply_discipline_capacity#4"]},{"id":"R3","text":"法律與稅務負債：ARC氣體產生器集體訴訟、BMW反壟斷求償、德國民事訴訟、墨西哥稅務爭議","h_ref":"H3","clock":"🐢","threshold":"累計提列或和解超過3億美元，或NHTSA對Autoliv產品下強制召回令","evidence_refs":["major_events#1","lawsuit_class_action#0","regulatory_antitrust#0","regulatory_antitrust#2","lawsuit_class_action#1"]},{"id":"R4","text":"汽車產量衰退與車廠臨時停產，EMEA產能過剩","h_ref":"H2","clock":"⚡","threshold":"全球輕型車產量連2季年減超過5%，或EMEA有機成長連2季落後產量超過3個百分點","evidence_refs":["cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#1","cyclical_prior_downcycle_behavior#2","cyclical_inventory_price_position#1","supply_demand_durability#0","major_events#0","geo_supply_chain#1"]},{"id":"R5","text":"供應鏈與出口管制：半導體、推進劑缺料或關稅無法轉嫁","h_ref":"H2","clock":"🔥","threshold":"關稅回收率連2季低於70%，或財報揭露缺料停產","evidence_refs":["reg_tariff_export#1","geo_supply_chain#0"]}],"single_thing":{"description":"2027-01-29第四季法說公布的2027調整後營業利益率指引中位數低於11%","why_fatal":"利益率是EPS最大的單一敏感項：營收約111億美元下每差1個百分點，稅後約0.78億美元、每股約1.08美元，約占FY1 EPS一成；指引低於11%等於12%路徑延後，EPS成長只剩回購","if_happens":"基準EPS路徑下修約一成，熊市機率升到40%；不建倉，已持有者減碼一半","how_monitor":"2026第四季實際利益率（全年10.5%隱含約14%）、2027指引、原物料補償進度與工程收入","probability":"約35%（管理層已說2027原物料壓力與2026相當）"}},"appendix_a":{"growth_durability":5,"quality_score":7,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":9.89,"peg_fy2":0.87,"stress":{"pass":2,"total":3}},"eps_meta":{"base_eps_path":{"FY2025A":9.55,"FY2026E":10.32,"FY2027E":11.59,"FY2028E":13.19},"fy_end_month":12,"eps_basis":"FY2025A為GAAP稀釋EPS（年報）；FY2026E–FY2028E為Koyfin共識，多為調整後口徑，基期口徑混用可能略高估三年成長率"},"catalysts":[{"date":"2027-01-29","date_precision":null,"type":"guidance","event":"第四季財報與2027全年指引","impact":"高","watch":"2027調整後利益率指引是否至少11%"},{"date":"2027-04-26","date_precision":null,"type":"other","event":"上海投資人日（兩天，含上海車展）","impact":"中","watch":"本土車廠業務利潤率與中期目標是否更新"},{"date":"2028-06","date_precision":"quarter","type":"capacity","event":"土耳其工廠完全關閉，年省約4,000萬美元達滿額","impact":"低","watch":"重組費用是否超出約1.42億美元"}],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8w(原9)","pacing":[],"holding_cap":null,"audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='A'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟡', moat_trend='→', week26=-1.23, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='循環/商品', cycle_position='中循環', moat='B', moat_trend='→', cycle_gates_pass=False"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":false,"basis":"signal='B', val='🟡'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":true,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"8w","condition":"判斷者宣告 wait_for_price（價格合理但要等）→ 原 row9 進場改觀望（等價格）","hit":true,"basis":"wait_for_price=True, 等待條件='等2027-01-29法說：2027調整後營業利益率指引≥11%且2026全年實際≥10.3%'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"requires_critic":[]}}
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
