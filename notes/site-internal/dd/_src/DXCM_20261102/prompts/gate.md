你是 DD 管線 v20 的判斷層閘（gate），標的 DXCM（20261102）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（41 條）
- `f_kpi0_gaap`（q1_business）｜營收（GAAP）＝1344.5 US$M｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（8-K Ex.99.1，2026-10-29）https://www.sec.gov/Archives/edgar/data/0001093557/000109355726000193/dxcm09302026-exhibit991.htm（numbers.latest_quarter_kpis.items[0]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-29））
- `f_kpi1_non_gaap`（q1_business）｜Non-GAAP 營業利益／利益率＝339.5 US$M（利益率 25.3%）｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（8-K Ex.99.1，2026-10-29）https://www.sec.gov/Archives/edgar/data/0001093557/000109355726000193/dxcm09302026-exhibit991.htm（numbers.latest_quarter_kpis.items[1]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-29））
- `f_kpi2_gaap`（q1_business）｜GAAP 營業利益／利益率＝327.2 US$M（利益率 24.3%）｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（8-K Ex.99.1，2026-10-29）https://www.sec.gov/Archives/edgar/data/0001093557/000109355726000193/dxcm09302026-exhibit991.htm（numbers.latest_quarter_kpis.items[2]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-29））
- `f_kpi5_fy2026`（q1_business）｜管理層全年指引（FY2026）＝營收 $5.20–5.25B（+12–13%）；Non-GAAP 毛利率約 64%（維持）；Non-GAAP 營業利益率約 24%（上調）；Adj. EBITDA 利益率約 32%（上調）｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司 Q3 2026 新聞稿（8-K Ex.99.1，2026-10-29）https://www.sec.gov/Archives/edgar/data/0001093557/000109355726000193/dxcm09302026-exhibit991.htm；Q4 隱含營收中點成長約 10%（CFO 法說稿）（numbers.latest_quarter_kpis.items[5]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-29））
- `f_earnings_recency`（q1_business）｜最近一次財報日＝2026-10-29 date｜期間與口徑：2026-10-29／距今 2 個交易日｜kind：realized
  - 來源：—（numbers.earnings_recency，as_of 2026-10-29）
- `f_peer_dxcm_gross_margin_pct`（q2_moat）｜DXCM 毛利率＝63.42 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.DXCM.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_dxcm_operating_margin_pct`（q2_moat）｜DXCM 營業利益率＝23.98 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.DXCM.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_dxcm_fcf_margin_pct`（q2_moat）｜DXCM FCF 利潤率＝33.93 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.DXCM.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_abt_operating_margin_pct`（q2_moat）｜ABT 營業利益率＝15.9 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ABT.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_abt_fcf_margin_pct`（q2_moat）｜ABT FCF 利潤率＝15.66 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ABT.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_mdt_operating_margin_pct`（q2_moat）｜MDT 營業利益率＝19.04 %｜期間與口徑：TTM ending 2026-07-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MDT.operating_margin_pct，as_of TTM ending 2026-07-31（4季加總））
- `f_peer_mdt_fcf_margin_pct`（q2_moat）｜MDT FCF 利潤率＝16.33 %｜期間與口徑：TTM ending 2026-07-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MDT.fcf_margin_pct，as_of TTM ending 2026-07-31（4季加總））
- `f_peer_podd_gross_margin_pct`（q2_moat）｜PODD 毛利率＝71.08 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.PODD.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_podd_fcf_margin_pct`（q2_moat）｜PODD FCF 利潤率＝8.7 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.PODD.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_tndm_operating_margin_pct`（q2_moat）｜TNDM 營業利益率＝-4.4 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.TNDM.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝2.71 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-10-31）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝3.13 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-10-31）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝3.67 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-10-31）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝5227.38 USD m｜期間與口徑：2026-11-02／yfinance revenue_estimate 0y 平均（27 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-02）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝5772.14 USD m｜期間與口徑：2026-11-02／yfinance revenue_estimate +1y 平均（27 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-02）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi3_fcf`（q4_capital）｜自由現金流（FCF）＝906.2 US$M（2026 年前三季累計＝營業現金流 1,120.4 − capex 214.2）｜期間與口徑：前三季累計至 2026-09-30，10-Q 公告；新聞稿未單列 Q3 FCF／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：SEC 10-Q https://www.sec.gov/Archives/edgar/data/0001093557/000109355726000195/dxcm-20260930.htm；法說稿稱前三季 FCF >$900M（numbers.latest_quarter_kpis.items[3]，as_of 前三季累計至 2026-09-30，10-Q 公告；新聞稿未單列 Q3 FCF）
- `f_kpi4_sbc`（q4_capital）｜SBC 占比＝2.7 % 營收（$36.8M；占 GAAP 營業利益 11.2%）｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（8-K Ex.99.1，2026-10-29）https://www.sec.gov/Archives/edgar/data/0001093557/000109355726000193/dxcm09302026-exhibit991.htm（numbers.latest_quarter_kpis.items[4]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-29））
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝-425.0 USD m｜期間與口徑：2026-11-02／yfinance 最新一季：總債務 1392.9、現金 1817.9（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-02）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝372.95 m shares｜期間與口徑：2026-11-02／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-11-02）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_ev_m`（q5_valuation）｜目前企業價值 EV（市值＋淨負債）＝30265.13 USD m｜期間與口徑：2026-11-02／市值 30690.13 ＋ 淨負債 -425.0｜kind：realized
  - 來源：—（numbers.capital_structure.ev_m，as_of 2026-11-02）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝30.37 x｜期間與口徑：2026-10-31／分母＝FY1 EPS 2.71，分子＝快照價 82.29｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-10-31）
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝82.29 USD｜期間與口徑：2026-10-30（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-10-30（RTH 收盤，UTC））
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝32.4 x｜期間與口徑：2026-10-30（RTH 收盤，UTC）／4 個年度端點內的分位＝0.5｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-10-30（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝0.5 %｜期間與口徑：2026-10-30（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-10-30（RTH 收盤，UTC））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝6.01 x｜期間與口徑：2026-10-30（RTH 收盤，UTC）／4 個年度端點內的分位＝2.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-10-30（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝2.0 %｜期間與口徑：2026-10-30（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-10-30（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝5.93 x｜期間與口徑：2026-10-30（RTH 收盤，UTC）／4 個年度端點內的分位＝0.3｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-10-30（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝0.3 %｜期間與口徑：2026-10-30（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-10-30（RTH 收盤，UTC））
- `f_consensus_rev_fy1_pct`（q5_valuation）｜FY1 共識修正＝1.88 %｜期間與口徑：2026-10-31／兩份 Koyfin 快照之間的 EPS 修正幅度（2.66 → 2.71）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.fy1.revision_pct，as_of 2026-10-31）
- `f_consensus_rev_fy2_pct`（q5_valuation）｜FY2 共識修正＝0.32 %｜期間與口徑：2026-10-31／兩份 Koyfin 快照之間的 EPS 修正幅度（3.12 → 3.13）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.fy2.revision_pct，as_of 2026-10-31）
- `f_ev_s_fwd`（q5_valuation）｜EV/S（EV ÷ FY1 共識營收）＝5.79 x｜期間與口徑：2026-11-02／f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）｜kind：estimate
  - 來源：—（numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m，as_of 2026-11-02）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝34.13 %｜期間與口徑：2026-10-30（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-10-30（RTH 收盤，UTC））
- `f_rsi14`（q5_valuation）｜RSI(14)＝47.75｜期間與口徑：2026-10-30（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-10-30（RTH 收盤，UTC））
- `f_ma_w250`（q5_valuation）｜250 週均線＝92.85 USD｜期間與口徑：2026-11-02／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-02）
- `f_ma_slope_w250_pct`（q5_valuation）｜W250 13 週斜率＝-0.75 %｜期間與口徑：2026-11-02／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-02）
- `f_ma_state`（q5_valuation）｜週線均線六態（decision_inputs.ma 必須等於此值）＝❌｜期間與口徑：2026-11-02／timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-02）
  - 原文：「price 82.29 / W52 72.51 / W104 75.22 / W250 92.85 / W250 13週斜率 -0.75%」

### findings_digest 中方向為負或來源衝突的條目（20 條）
- `competitive_share_entrants#0`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K 點名 Abbott、MiniMed（Guardian Connect、Simplera）、Roche 等為直接對手；Stelo 的直接對手為 Abbott；並提到主要在中國的新興競爭者。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-12）｜affects：moat_trend、decision_inputs.bear
- `competitive_share_entrants#1`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K：非傳統醫材業者（大型上市公司）正開發競品，且 FDA 2026-01-06 的一般健康器材指引可能使其受惠。
  - 來源：SEC EDGAR 10-K FY2025 Item 1 Business（as_of 2026-02-12）｜affects：moat_trend、decision_inputs.bear
- `competitive_share_entrants#2`（competitive_share_entrants｜方向 -｜狀態 ok）：CMS 將 CGM 納入 DMEPOS 競標（2027 簽約、2028-01-01 起付款變更），預期約 10 份 CGM 合約，得標價取第 75 百分位，預期降低 Medicare 給付。
  - 來源：SEC EDGAR 10-K FY2025 Item 1 Business（as_of 2026-02-12）｜affects：valuation、triggers、decision_inputs.bear
- `customer_second_source#0`（customer_second_source｜方向 -｜狀態 ok）：10-K FY2025 風險因子：DXCM 對單一來源零件難以快速建立替代供應商（供應端風險，非客戶端導入第二供應商）；搜尋未見最大客戶（經銷商）導入第二供應商或自製的來源。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-12）｜affects：thesis.R、decision_inputs.bear
- `customer_concentration_credit#0`（customer_concentration_credit｜方向 -｜狀態 ok）：FY2025 10-K：三家客戶（A/B/C，皆>10%）占營收比重分別 55%/35%/46%（2024 為 40%/35%/42%，2023 為 35%/30%/37%）；占應收帳款 24%/20%/24%。營收為扣除費用、折扣、回扣後淨額，回扣付給其他實體者排除，故合計可超過 100%。
  - 來源：SEC EDGAR 10-K FY2025 附註 Concentration of Credit Risk and Significant Customers（as_of 2026-02-12）｜affects：thesis.R、decision_inputs.bear
- `customer_concentration_credit#2`（customer_concentration_credit｜方向 -｜狀態 ok）：2026 Q2 10-Q 顯示經銷商管道為主要營收來源（Q2 經銷商約 $1,102.4M vs 直銷 $206M）
  - 來源：SEC EDGAR 10-Q 2026-06-30（as_of 2026-07-30）｜affects：thesis.R
- `regulatory_antitrust#2`（regulatory_antitrust｜方向 -｜狀態 ok）：FDA 於 2025-03 對 Dexcom 發出 warning letter，指聖地牙哥與 Mesa 廠製造及品質系統不符；G6/G7 感測器未經核准變更。
  - 來源：MassDevice: Dexcom receives FDA warning letter（as_of 2025-03-25）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：FY2025 10-K 列示關稅與貿易政策波動（含更高進口關稅、報復性關稅）與 OFAC／BIS 出口管制為國際營運風險因子；屬一般性風險揭露，未量化
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-12）｜affects：decision_inputs.bear
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：FY2023 10-K：DexCom 依賴單一或唯一來源供應商，例如發射器內的 ASIC 與生物介面膜用的特定聚合物
  - 來源：DexCom Form 10-K FY2023 (SEC)（as_of 2024-02-15）｜affects：decision_inputs.bear、thesis.R
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：風險摘要站稱 DexCom 製造集中於亞利桑那州梅薩與馬來西亞，聖地牙哥有限，替代產能難以快速建立（二手摘要，非 SEC 原文）
  - 來源：policyrisk.com DXCM（as_of 2026-01-01）｜affects：decision_inputs.bear、thesis.R
- `end_markets#1`（end_markets｜方向 -｜狀態 ok）：美國 CGM 市佔 2025 年 GlobalData 模型：Abbott 48.5%、Dexcom 44.7%；歐洲/亞太/中東非洲 Dexcom 市佔遠低於 Abbott。Barclays 以 Abbott Libre 市佔壓力為由給 Underweight、目標價 $71。
  - 來源：Kavout / Munich-startup insights（二手彙整）（as_of 2026-06-01）｜affects：moat_trend、decision_inputs.bear
- `end_markets#2`（end_markets｜方向 -｜狀態 ok）：Mordor Intelligence 指 Stelo 以 USD 89-99 上市及 Abbott 類似 OTC 策略，預期未來兩年感測器價格趨向 USD 60 以下（預測非現行價目）。
  - 來源：Mordor Intelligence US CGM Market（as_of 2026-06-01）｜affects：moat_trend、thesis.R
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：10-K 風險因素：競爭對手快速採用 AI 可能加速創新週期並加劇競爭壓力（未點名具體替代技術）
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-12）｜affects：moat_trend、decision_inputs.bear
- `substitute_technology#3`（substitute_technology｜方向 -｜狀態 ok）：Analysts 指出 Abbott 雙分析物（葡萄糖＋酮體）策略可能在 CGM 市場領先 DexCom
  - 來源：Kavout market lens（as_of 2026-08-01）｜affects：moat_trend、decision_inputs.bear
- `channel_business_model_shift#1`（channel_business_model_shift｜方向 -｜狀態 ok）：Q4 2025 財報電話會議摘要：管理層預期 Q1 2026 營收季減約 6-7%，部分歸因於逐步轉向藥局通路。
  - 來源：MarketBeat, DexCom Q4 earnings call highlights（as_of 2026-02-12）｜affects：valuation、moat_trend
- `major_events#0`（major_events｜方向 -｜狀態 ok）：證券集體訴訟（In re Dexcom Securities Litigation）持續中：2026-01-07 法院准許被告判決於訴狀（附修正許可），2026-02-06 原告提第二次修正訴狀
  - 來源：SEC EDGAR 10-K FY2025 Item 3（as_of 2026-02-12）｜affects：decision_inputs.bear、thesis.R
- `major_events#1`（major_events｜方向 -｜狀態 ok）：G6/G7 使用者集體訴訟：2025-09-29 至 2026-01-08 共六件重疊的集體訴訟起訴
  - 來源：SEC EDGAR 10-K FY2025 Item 3（as_of 2026-02-12）｜affects：decision_inputs.bear、thesis.R
- `lawsuit_class_action#0`（lawsuit_class_action｜方向 -｜狀態 ok）：證券集體訴訟持續，2026-02-06 提第二次修正訴狀
  - 來源：SEC EDGAR 10-K FY2025 Item 3（as_of 2026-02-12）｜affects：decision_inputs.bear、thesis.R
- `lawsuit_class_action#1`（lawsuit_class_action｜方向 -｜狀態 ok）：衍生訴訟（聯邦＋2025-09-25 Delaware Chancery）均暫停待證券訴訟駁回動議
  - 來源：SEC EDGAR 10-K FY2025 Item 3（as_of 2026-02-12）｜affects：decision_inputs.bear
- `lawsuit_class_action#2`（lawsuit_class_action｜方向 -｜狀態 ok）：G6/G7 使用者六件重疊集體訴訟
  - 來源：SEC EDGAR 10-K FY2025 Item 3（as_of 2026-02-12）｜affects：decision_inputs.bear、thesis.R

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 10 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/DXCM_20261102/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":173.6,"bear_5y_price":48.0,"p_bull_pct":25,"p_bear_pct":30,"upside_5y_pct":35.0,"ev5y_pct":31.0,"irr_base_pct":6.2,"asym_ratio":2.2,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":2.71,"pe":30.37,"basis":"FY2026E共識EPS（Koyfin 2026-10-31快照）；終端倍數同樣套在終端年當年度EPS，與現價前瞻倍數同口徑"},"eps":{"bull":[3.25,3.85,4.55,5.35,6.2],"base":[3.1,3.55,4.05,4.55,5.05],"bear":[2.9,2.75,2.8,2.9,3.0]},"pe":{"bull":28,"base":22,"bear":16},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0,"net_buyback":2.5},"second_stage":{"bull_cagr_pct":14,"base_cagr_pct":9},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### DXCM_Q2_2026_Earnings_Call_20260730.md
- 2026-07-30｜CFO｜guidance：全年營收財測上調中點，區間 $5.18–5.25B（原話："an updated range of $5.18 billion to $5.25 billion"）
- 2026-07-30｜CFO｜guidance：匯率對下半年國際營收約 $15M 影響（原話："about a $15 million impact to international revenue"）
- 2026-07-30｜CFO｜guidance：排除匯率後有機成長預期較前次財測上調（原話："an increase in organic growth by more than 50 basis points"）
- 2026-07-30｜CFO｜guidance：全年 non-GAAP 毛利率財測約 64%（原話："gross profit margin guidance to approximately 64%"）
- 2026-07-30｜CFO｜margin：全年 non-GAAP 營業利益率財測 23.5%–24%（原話："operating profit margin guidance to a range of 23.5% to 24%"）
- 2026-07-30｜CFO｜margin：Q2 毛利率較去年同期改善約 400bp（原話："margins improving approximately 400 basis points"）
- 2026-07-30｜CFO｜margin：管理層說明毛利率高點預期在 Q3，Ireland 投產後下降（原話："The expectation was always a peak into Q3 in gross margin"）
- 2026-07-30｜CFO｜margin：毛利率財測上調歸因於產線表現而非油價（原話："the raise is really on underlying performance improvements"）
- 2026-07-30｜CFO｜margin：管理層稱 15 Day 對毛利的幫助為多年期、無單一季度見頂（原話："there's not really 1 quarter where it plateaus"）
- 2026-07-30｜CFO｜margin：營業費用槓桿優於計畫（原話："We've had some operating leverage really ahead of plan"）
- 2026-07-30｜CFO｜margin：Ireland 投產前將有招聘與折舊，Q3 繼續投資（原話："we'll start some depreciation as well"）
- 2026-07-30｜CFO｜guidance：有機營收定義（排除匯率及近12個月併購/出售的非CGM營收）（原話："our definition of organic revenue excludes the impact"）
- 2026-07-30｜CEO｜product：美國客戶 G7 15 Day 年底轉換目標近 50%（原話："convert nearly 50% of our U.S. customer base"）
- 2026-07-30｜CFO｜product：15 Day 全年平均滲透率約 20–25%，明年起點近 50%（原話："you're at 20%, 25%"）
- 2026-07-30｜CEO｜product：Health Canada 為首個核准 G7 15 Day 的海外監管機構（原話："Health Canada became the first international regulator"）
- 2026-07-30｜CEO｜commitment：承諾 2026 下半年將 G7 15 Day 帶到加拿大（原話："bringing G7 15 Day to Canada in the second half of 2026"）
- 2026-07-30｜CEO｜product：G8 時程仍維持，2027 年底至 2028 年初視法規時程（原話："very much on track for that end of 2027, early 2028"）
- 2026-07-30｜CEO｜product：Smart Basal 試點使客戶 3 週達最佳基礎胰島素劑量（原話："reach an optimal basal dose in only 3 weeks on average"）
- 2026-07-30｜CEO｜product：Dexcom 為 FDA TEMPO 試點首家入選公司（原話："first company chosen to participate in the TEMPO"）
- 2026-07-30｜CEO｜product：CONNECT 試驗 A1c 改善 1.6%（原話："1.6% A1c improvement for the Dexcom CGM group"）
- 2026-07-30｜CEO｜customer：四大商業 PBM 已涵蓋所有糖尿病患（原話："across the 4 largest commercial PBMs"）
- 2026-07-30｜CEO｜customer：美國有保險覆蓋但未使用 CGM 者約 900 萬人（原話："approximately 9 million people in the United States"）
- 2026-07-30｜CEO｜guidance：CMS 非胰島素第二型涵蓋決定預計年底前回覆（原話："We do expect to hear back from CMS on that decision"）
- 2026-07-30｜CEO｜commitment：公司計畫中 CMS 涵蓋生效時點為 2027 年中（原話："we've got it taking effect in the middle of 2027"）
- 2026-07-30｜CFO｜capital_allocation：2026 年承諾回購 $10 億股票（原話："a commitment to repurchase $1 billion of stock in 2026"）
- 2026-07-30｜CFO｜capital_allocation：Q2 已回購約 $6 億（原話："repurchased approximately $600 million in the second quarter"）
- 2026-07-30｜CFO｜capital_allocation：上半年自由現金流逾 $6 億（原話："more than $600 million in free cash flow"）
- 2026-07-30｜CFO｜capital_allocation：完成 Nutrisense 收購（原話："we completed the acquisition of Nutrisense"）
- 2026-07-30｜CFO｜capital_allocation：Nutrisense 非 CGM 營收極小（原話："you can count the millions for the year on one hand"）
- 2026-07-30｜CFO｜capital_allocation：資本配置框架含小型併購評估（原話："ongoing assessment of tuck-in M&A"）
- 2026-07-30｜CFO｜customer：新客戶數 Q2 與 Q1 全球紀錄持平（原話："Q2 is in line with the record globally"）
- 2026-07-30｜CFO｜customer：新客戶中美國環比增加、海外下降（原話："This means the OUS patients came down a bit"）
- 2026-07-30｜CEO｜risk：去年 out-of-box 失效率問題曾使客戶不滿（原話："out-of-box failure rates that disrupted things"）
- 2026-07-30｜CEO｜risk：下半年國際比較基期變高（原話："the comps get a little tougher"）
- 2026-07-30｜CFO｜risk：匯率假設：6/30 為 1.14（原話："As of June 30, when we're thinking about it's $1.14"）
- 2026-07-30｜CEO｜customer：真實世界非胰島素第二型使用率逾 80%（原話："not quite at 97%, but well above 80% in this population"）
- 2026-07-30｜CEO｜competition：管理層否認 CMS 將設 A1c 門檻之說（原話："that's not consistent at all with what we hear"）
- 2026-07-30｜CEO｜commitment：長期目標：現金流與利潤率輪廓（原話："one of the more compelling cash flow and margin profiles"）
- 2026-07-30｜CFO｜product：Dexcom Flex 在德國上市（原話："launch of Dexcom Flex in Germany"）

### DXCM_Analyst_Investor_Day_DexCom_Inc_20260514.md
- 2026-05-14｜Jereme Sylvain｜guidance：CFO 表示長期計畫（LRP）至 2030 年每年營收成長 10% 以上（原話："10% plus every year, each year in our LRP through 2030"）
- 2026-05-14｜Jereme Sylvain｜guidance：CFO 澄清 10% 以上不是 CAGR 或平均，而是逐年（原話："It's 10% plus each year every year."）
- 2026-05-14｜Jereme Sylvain｜guidance：CFO 說 LRP 已納入 2028 年起的競標假設（原話："competitive bidding assumptions starting in 2028"）
- 2026-05-14｜Jereme Sylvain｜guidance：CFO 說 LRP 已納入競爭對手新品上市假設（原話："competitor product launches over the course of time"）
- 2026-05-14｜Jereme Sylvain｜guidance：CFO 回答價量組合：價格假設每年約 2% 至 3%（各年不同）（原話："we've typically thought about 2% to 3% price"）
- 2026-05-14｜Jereme Sylvain｜guidance：CFO 對競標的假設：納入名目價格影響（原話："some nominal price impacts associated with it"）
- 2026-05-14｜Jereme Sylvain｜guidance：CFO 說 LRP 中 Medicare 涵蓋時點假設為 2027 年中（原話："for LRP purposes, we put it in the middle of 2027"）
- 2026-05-14｜Jacob Leach｜guidance：CEO 表示公司規劃假設 CMS 涵蓋於明年年中生效（原話："coverage will come the middle of next year"）
- 2026-05-14｜Jon Coleman｜guidance：Coleman 在 Q&A 說 CMS 非胰島素型涵蓋從未預期在 2026 年發生（原話："we never anticipated that to happen in '26"）
- 2026-05-14｜Jon Coleman｜guidance：Coleman 說若 CMS 涵蓋提早，屬上行空間（原話："mid-'27 is when the coverage will actually kick in"）
- 2026-05-14｜Jereme Sylvain｜guidance：CFO 預期全球涵蓋人數 2030 年底約 5200 萬（目前約 2300 萬）（原話："We expect to exit around 52 million"）
- 2026-05-14｜Jereme Sylvain｜guidance：CFO 假設 2030 年第二型滲透率 10% 至 15%（原話："type 2 in the 10% to 15% range"）
- 2026-05-14｜Jereme Sylvain｜guidance：CFO 假設 CMS 涵蓋後滲透速度為 basal 的一半（原話："CMS penetration goes at half the rate of basal"）
- 2026-05-14｜Jereme Sylvain｜guidance：CFO 說明配戴使用率假設沿用網站所列 75% 至 80%（原話："the 75% to 80% utilization"）
- 2026-05-14｜Jereme Sylvain｜guidance：CFO 說留存與使用率提升的上行未放進 LRP（原話："we haven't put any of this into our LRP"）
- 2026-05-14｜Jereme Sylvain｜margin：CFO 預期 LRP 結束時毛利率升至 60% 後段（原話："We expect gross margin to grow into the high 60s"）
- 2026-05-14｜Jereme Sylvain｜margin：CFO 預期 LRP 結束時非 GAAP 營業利益率 29% 至 30%（原話："get to 29% to 30% by the end of the end of the LRP"）
- 2026-05-14｜Jereme Sylvain｜margin：CFO 說營業利益率每年約擴張 150 bp，主要來自毛利率（原話："about 150 basis points a year"）
- 2026-05-14｜Jereme Sylvain｜margin：CFO 預期調整後 EBITDA 利益率升至 36% 至 37%（原話："adjusted EBITDA margin to grow to 36% to 37%"）
- 2026-05-14｜Jereme Sylvain｜margin：CFO 預期 G8 製造成本較 G7 至少低 10%（原話："it costs at least 10% less than it cost to make G7"）
- 2026-05-14｜Jereme Sylvain｜margin：CFO 提及 15 日款保固率可能小幅上升（管理層認為可接受）（原話："the warranty rate may go up a little bit"）
- 2026-05-14｜Jereme Sylvain｜margin：CFO 說近期毛利率機會：今年底美國約近半數用戶轉 15 日款，次年起點更高（原話："approaching 50% of our population moved over"）
- 2026-05-14｜Jereme Sylvain｜margin：CFO 說去年營運費用改善 300 bp，來自 cost to execute 框架（原話："300 basis points of operating expense improvement"）
- 2026-05-14｜Jacob Leach｜margin：CEO 說公司目前營業利益率已超過 20% 且仍有空間（原話："operating at margins of over 20% with additional room to go"）
- 2026-05-14｜Jereme Sylvain｜capital_allocation：CFO 表示 10 億美元回購授權將於 2026 年執行完畢（原話："It will be fully executed in 2026."）
- 2026-05-14｜Jereme Sylvain｜capital_allocation：CFO 提出未來每年至少 50% 自由現金流用於回購（原話："at least 50% of our annual free cash flow to repurchases"）
- 2026-05-14｜Jereme Sylvain｜capital_allocation：CFO 稱股價有落差時要回購（原話："And boy, we see a big one today."）
- 2026-05-14｜Jereme Sylvain｜capital_allocation：CFO 列出支持小型併購為資本配置用途之一（原話："We want to be able to support tuck-in M&A."）
- 2026-05-14｜Jacob Leach｜commitment：CEO 說 G8 預計明年送件，2027 年底或 2028 年初上市（原話："a launch either at the end of '27 or early '28"）
- 2026-05-14｜Jacob Leach｜commitment：CEO 說今年底前轉換近半美國用戶至 G7 15 日款（原話："convert nearly half of our U.S. base over to this product"）
- 2026-05-14｜Jacob Leach｜commitment：CEO 說明年推出醫院連續血糖監測產品（原話："We want to be able to support tuck-in M&A."）
- 2026-05-14｜Jacob Leach｜commitment：CEO 說酮體感測會納入 G8 平台但時程在後（原話："Ketones, it will be part of the G8 platform."）
- 2026-05-14｜Jacob Leach｜commitment：CEO 說 G8 之後將有多分析物版本（原話："right behind that product is a multi-analyte version of G8"）
- 2026-05-14｜Jon Coleman｜commitment：Coleman 表示國際收入願景：LRP 結束時達數十億美元（原話："you'll see multibillions of dollars in international"）
- 2026-05-14｜Jacob Leach｜product：CEO 說 Smart Basal 把達到合適劑量的時間從 12 週以上縮短到 30 天內（原話："from over 12 weeks to fewer than 30 days"）
- 2026-05-14｜Jacob Leach｜product：CEO 說 EHR 直接整合已有逾 320 家醫療系統整合或導入中（原話："We have over 320 health systems"）
- 2026-05-14｜Jacob Leach｜product：CEO 說 G7 產線可改裝生產 G8，支援產能（原話："retrofit the G7 lines to manufacture these G8 systems"）
- 2026-05-14｜Jacob Leach｜product：CEO 承認貼片黏著問題尚未完全解決（原話："the code is definitely not cracked"）
- 2026-05-14｜Jon Coleman｜product：CEO 說 Flex 美國是否推出（另一產品或 App）尚未決定（Coleman 回答）（原話："We've not yet made that decision"）
- 2026-05-14｜Jon Coleman｜competition：Coleman 稱公司相對競爭對手已有留存優勢，並預期差距擴大（原話："We've already got a retention advantage"）
- 2026-05-14｜Jeffrey Johnson｜competition：分析師提到最大競爭對手在酮體上有進展，詢問 Dexcom 路徑（原話："your biggest competitor is still making progress"）
- 2026-05-14｜Jon Coleman｜customer：Coleman 說基層醫療處方份額從 2023 年約 30% 升到 2025 年近 40%（原話："2025 has grown close to 40%"）
- 2026-05-14｜Jon Coleman｜customer：Coleman 說先前擴編美國銷售團隊 40%（原話："expand the sales force in the United States by 40%"）
- 2026-05-14｜Jacob Leach｜customer：CEO 說使用者停用 CGM 的首要原因之一是認為數據不夠可靠（原話："they don't feel that the glucose data is reliable enough"）
- 2026-05-14｜Jacob Leach｜customer：CEO 說非胰島素型第二型患者目前僅 25% 有涵蓋（原話："we're only 25% covered"）
- 2026-05-14｜Jacob Leach｜customer：CEO 說第一季國際成長多數來自新開通涵蓋的市場（原話："most of that growth came from new markets"）
- 2026-05-14｜Jacob Leach｜customer：CEO 提到另一家 PBM 今年起涵蓋所有糖尿病人（原話："another PBM, the next largest, starting to cover CGM"）
- 2026-05-14｜Jacob Leach｜risk：CEO 宣布與 Elliott 合作新增 2 名董事（原話："recruit 2 new Board directors to our Board"）
- 2026-05-14｜Jacob Leach｜risk：CEO 說正在招聘新設的 Chief Product Officer（原話："a brand-new role at Dexcom, a Chief Product Officer"）
- 2026-05-14｜Jacob Leach｜risk：CEO 說董事會目前沒有獨立的醫材董事（原話："We don't have independent med tech directors on our Board"）
- 2026-05-14｜Jereme Sylvain｜risk：CFO 說 CMS 關注點在詐欺性帳單，競標影響有限（原話："CMS is heavily focused on fraud"）

### 問答異常語氣（迴避／改口／保留）
- DXCM_Q2_2026_Earnings_Call_20260730.md｜問：Polark 請管理層就產品表現給具體指標（報廢、保固、退貨、客訴）｜答法：CEO 以 NPS 連三季上升及客訴下降作答，未給報廢/保固/退貨數字；CFO 指向毛利率改善為佐證
- DXCM_Q2_2026_Earnings_Call_20260730.md｜問：Block 詢問毛利率財測上調是否含油價緩衝｜答法：CFO 解釋樹脂成本遞延流入並稱與上季指引大致一致，未明確回答是否仍有油價緩衝
- DXCM_Q2_2026_Earnings_Call_20260730.md｜問：Wuensch 詢問 Nutrisense 收購金額｜答法：CFO 未公開金額，指向 10-Q 現金流量表
- DXCM_Analyst_Investor_Day_DexCom_Inc_20260514.md｜問：Jeffrey Johnson（Baird）追問酮體感測的時程與路徑｜答法：CEO 說酮體會納入 G8 平台，但明說不給任何確切時間表（"I'm not going to give any exact time lines"），改談 G8 準確度優先、臨床工作仍待完成
- DXCM_Analyst_Investor_Day_DexCom_Inc_20260514.md｜問：Larry Biegelsen（Wells Fargo）問銷售與利潤率假設的逐年節奏｜答法：CFO 未給逐年數字，表示 "We don't have a cadence to provide"，留待年度財測
- DXCM_Analyst_Investor_Day_DexCom_Inc_20260514.md｜問：Joanne Wuensch（Citi）問 10% 以上各年哪年較強｜答法：CFO 不分年度給數字，只說 10% 以上是基礎情境，逐年細節留給年度財測，僅提供各年催化劑
- DXCM_Analyst_Investor_Day_DexCom_Inc_20260514.md｜問：Matt O'Brien（Piper Sandler）問 LRP 中美國與國際成長的相對關係｜答法：CEO 以存取擴張時點難控制回答，CFO 說「兩者都不輕忽」，未給美國與國際的成長拆分數字
- DXCM_Analyst_Investor_Day_DexCom_Inc_20260514.md｜問：Rich Newitter（Truist）問國際成長是否高於美國、美國是否需要第二型非胰島素型才能維持雙位數｜答法：CFO 表示未拆分美國與國際，改談涵蓋是成長演算法核心，未直接回答美國單獨是否雙位數
- DXCM_Analyst_Investor_Day_DexCom_Inc_20260514.md｜問：Joanne Wuensch（Citi）問 Flex 是否會帶到美國｜答法：Coleman 表示尚未決定是否為不同產品或 App，不願多談
- DXCM_Analyst_Investor_Day_DexCom_Inc_20260514.md｜問：Chris Pasquale（Nephron）問 G8 上市後的轉換策略｜答法：CEO 說「沒有具體轉換計畫」，只表示希望快速轉換

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 5 | 2 |
| customer_second_source | found | 2 | 2 |
| customer_concentration_credit | found | 3 | 2 |
| supply_demand_durability | found | 4 | 3 |
| regulatory_antitrust | found | 3 | 3 |
| reg_tariff_export | found | 2 | 2 |
| geo_supply_chain | found | 3 | 3 |
| end_markets | found | 5 | 3 |
| substitute_technology | found | 4 | 2 |
| channel_business_model_shift | found | 3 | 2 |
| capital_markets_pricing | found | 5 | 4 |
| major_events | found | 5 | 4 |

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"status":"no_prior_dd"}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"DXCM","date":"2026-11-02","schema":"v15.0","contract":"v19","company_name":"DexCom, Inc."},"oneliner":"CGM兩大廠之一，毛利率回到65%、美國連季拿份額，下一段成長在第二型非胰島素族群；約30倍今年EPS屬合理不便宜，CMS涵蓋決定年底前揭曉，等結果再動","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/DXCM_20261102/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/DXCM_20261102/scenario.json","answers":{"q1_business":{"verdict":"賣CGM感測器耗材，量來自第一型與第二型糖尿病患，錢卡在付款方（PBM處方集、Medicare）與三大經銷商手上；第二型非胰島素涵蓋是下一段成長的關鍵","reasoning":"收錢方式：感測器每10或15天更換一次，屬經常性耗材收入。Q3 2026營收13.445億美元、年增11%，美國9.70億美元（年增14%、約占72%）、國際3.75億美元（年增5%、約占28%）；非GAAP毛利率65.1%、營業利益3.395億美元（25.3%），GAAP營業利益3.272億美元（24.3%），兩者只差約1,230萬美元。全年財測營收52.0–52.5億美元（年增12–13%）、非GAAP營業利益率約24%（上調）。錢卡在哪：Q2經銷通路約占營收84%，前三大經銷商未扣回饋前營收占比55%／35%／46%且三年逐年上升，是本檔最明顯的單點依賴；付款端由PBM處方集與Medicare決定，CVS排他合約流失（CFO Q3法說：占美國營收不到4%）即是例證。產業處於擴張期：CFO稱兩大廠合計美國營收低雙位數成長，全球涵蓋人數預期由約2,300萬升到2030年底約5,200萬。供需屬結構性持久，風險在單價而非需求","fact_refs":["f_kpi0_gaap","f_kpi1_non_gaap","f_kpi2_gaap","f_kpi5_fy2026","f_earnings_recency"],"verdict_values":{"revenue_quality":"經常性耗材收入：感測器定期更換，營收隨活躍用戶累積；美國約72%、國際約28%；經銷通路約84%（Q2 2026 10-Q），前三大經銷商未扣回饋前占比55%／35%／46%（FY2025 10-K）","unit_econ_note":"Q3非GAAP毛利率65.1%（去年同期61.3%），來自製造效率、運費與品質管理及15日款放量；CEO稱活躍用戶年增十幾%上段，但營收只年增11%，每用戶營收在降（15日款年用量較少、國際分級產品、通路組合）","archetype":{"primary":"品質複利成長","secondary":"轉機/特殊情境","confidence":"中","fingerprint":"耗材型經常性營收、毛利率六成以上、營業利益率擴張中、FCF高於淨利；2025年FDA警告信與品質問題後的修復期，股價仍在五年均價之下"},"industry":{"clock_phase":"II","sd_verdict_source":"結構性持久：美國第一型滲透約60–65%已成熟，第二型非胰島素約2,500萬人、商保涵蓋僅約25%、Medicare待決，需求由臨床證據與涵蓋擴張驅動，非景氣循環；壓力在單價不在需求（Baird與MarketBeat彙整、CEO投資人日2026-05-14）","bargaining":{"up":"ASIC與生物介面膜聚合物單一來源（10-K），晶片已向FDA申請Silicon Labs第二來源；供應端議價風險中等","down":"前三大經銷商營收占比55%／35%／46%且逐年上升、應收占比24%／20%／24%；PBM可改排他處方集（CVS案），Medicare 2028年起競標；下游議價力強","geo":"製造在美國Mesa與馬來西亞，Ireland廠2026年Q4起商業生產，三地分散；CFO稱多數產品美國製造、關稅直接衝擊小（2025年Q1法說）"},"profit_pool_dir":"利潤池隨涵蓋擴張變大，但單位價格往下：量往第二型與國際走，OTC與競標壓價；DXCM目前靠成本下降守住毛利率","tam_table":[{"item":"美國第一型CGM滲透率","value":"約60–65%，已成熟（Baird與MarketBeat彙整，2025–2026）"},{"item":"美國第二型非胰島素患者","value":"約2,500萬人，商保涵蓋約25%（CEO，投資人日2026-05-14）；四大商業PBM已涵蓋，Medicare待決"},{"item":"全球涵蓋人數","value":"約2,300萬人→2030年底約5,200萬人（CFO，投資人日）"},{"item":"第二型滲透率假設","value":"2030年10–15%，CMS涵蓋後以basal一半速度滲透（CFO，投資人日）"},{"item":"美國有涵蓋但未用CGM","value":"約900萬人（CEO，Q2法說2026-07-30）"},{"item":"第二型basal市場規模","value":"2030年約40億美元（William Blair 2025-10，採用曲線75%情境）"},{"item":"CGM營收份額2025","value":"全球Abbott 52.83%、DXCM 33.89%、Medtronic 10.10%（Mordor）；美國Abbott 48.5%、DXCM 44.7%（GlobalData）"},{"item":"營業利益池占比5年前→現在","value":"事實表未涵蓋"}]}}},"q2_moat":{"verdict":"護城河持平（→），B級：執行面擴大，定價面小幅縮減","reasoning":"機制：感測器準確度、與多款胰島素幫浦相容的自動給藥系統與Share/Follow家屬分享，讓第一型與胰島素使用者轉換成本高（CEO Q3法說：多款幫浦與對手不相容），再加上一連串隨機試驗堆出的給付證據（CONNECT登上NEJM）。方向：執行面擴大，Q3非GAAP毛利率65.1%、年增約380bp，營業利益率25.3%，美國連續多季拿份額，Q1營收年增15%對Abbott CGM 7.5%，15日款新黏膠讓存活率提高4–5個百分點；定價面小幅縮減，PBM排他合約流失、對手在自費市場降價、OTC價格下探、2028年競標在即。兩者相抵判持平。同業ROIC事實表未涵蓋，改看利潤率：DXCM營業利益率24.0%、FCF利潤率33.9%，高於Abbott 15.9%／15.7%與Medtronic 19.0%／16.3%，但後兩者是多角化集團，只能當方向參考。評分執行8、定價6，B級。報酬持續期四檢查點都落在中間（🟡），主因付款方與政策掌握分配權","fact_refs":["f_peer_dxcm_gross_margin_pct","f_peer_dxcm_operating_margin_pct","f_peer_dxcm_fcf_margin_pct","f_peer_abt_operating_margin_pct","f_peer_abt_fcf_margin_pct","f_peer_mdt_operating_margin_pct","f_peer_mdt_fcf_margin_pct","f_peer_podd_gross_margin_pct","f_peer_podd_fcf_margin_pct","f_peer_tndm_operating_margin_pct","f_kpi1_non_gaap"],"verdict_values":{"moat":{"mechanism":"感測器準確度＋幫浦相容生態（AID整合、Share/Follow）造成第一型與胰島素使用者轉換成本，加上隨機試驗證據推動給付擴張與醫師處方偏好","execution":8,"pricing":6,"grade":"B","trend":"→","trend_evidence":"執行面擴大：毛利率年增約380bp至65.1%、美國多季拿份額（CEO Q3法說）、Q1營收年增15%對Abbott CGM 7.5%；定價面縮減：CVS排他合約流失（占美國營收不到4%）、對手提到自費市場定價逆風、研究機構預測OTC感測器兩年內跌破60美元。全球營收份額仍落後Abbott（2025年33.9%對52.8%），但未見DXCM份額下滑的第三方時間序列，故判持平而非上升","competitor_notes":[{"name":"ABT","strategy_note":"CGM份額第一（2025年全球營收份額52.8%），以規模與低價搶自費及新市場，雙分析物Libre Duo先上市；集團營業利益率15.9%不代表其CGM單一業務"},{"name":"MDT","strategy_note":"MiniMed以自家幫浦綁Simplera與Guardian Connect，份額約10.1%，屬生態內封閉競爭，威脅限於自家幫浦用戶"},{"name":"PODD","strategy_note":"貼片式胰島素幫浦廠，非CGM直接對手；毛利率71.1%但FCF利潤率8.7%，其CGM相容選擇影響DXCM在幫浦用戶的黏著度"},{"name":"TNDM","strategy_note":"胰島素幫浦廠，營業利益率−4.4%仍虧損，議價力弱，屬相容夥伴而非競爭者"}],"peer_na_reason":"同業ROIC與投入資本事實表未涵蓋；Abbott與Medtronic的利潤率為集團整體、非CGM單一業務，PODD與TNDM是胰島素幫浦廠，只能當利潤結構參考","threats":[{"level":"🟡","text":"Abbott份額與規模領先（2025年全球營收份額52.8%對33.9%），雙分析物（葡萄糖＋酮體）Libre Duo先上市；DXCM酮體要等G8之後的多分析物版本，CEO不給時程","p":"40%","evidence_refs":["substitute_technology#3","competitive_share_entrants#0","end_markets#1"]},{"level":"🟡","text":"中國新興廠與醫材以外的大型企業切入一般健康市場，FDA 2026-01-06一般健康器材指引可能降低門檻，加上OTC感測器價格預測兩年內跌破60美元，壓低自費與第二型族群單價；若大型科技業以穿戴生態系切入則升級為生態攻擊","p":"30%","evidence_refs":["competitive_share_entrants#1","end_markets#2","substitute_technology#0"]},{"level":"🟡","text":"PBM處方集改為單一品牌優先（CVS合約流失，CFO於Q3法說2026-10-29稱占美國營收不到4%），若擴散到其他PBM將迫使降價換取共同優先地位；CEO稱2027年處方集已鎖定。來源只有公司法說，屬一方口徑，外部負向資料沒有收錄此事，尚無第三方佐證","p":"20%","evidence_refs":[]}],"roic_durability":{"quadrant":"高利益率（營業利益率24.0%、FCF利潤率33.9%、毛利率63.4%）×周轉率未知（投入資本事實表未涵蓋），先查持續期","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者與決策者兩環已成立：CONNECT隨機試驗6個月A1c較對照組多降0.9個百分點、登上NEJM，真實世界非胰島素第二型配戴率逾80%（CEO Q2法說）。付款者是缺口：非胰島素第二型僅約25%有涵蓋、Medicare決定待定，付款環節不成立前需求轉不成收入"},{"item":"決策層級","level":"🟡","text":"在最小決策單位看替代性分兩群：第一型與幫浦使用者綁自動給藥系統相容與Share/Follow，轉換成本高；第二型非胰島素與OTC族群產品較可比，PBM處方集一紙決定即可換品牌（CVS案）。漲價後流失率與分客群續約率事實表未涵蓋，CFO稱留存與使用率在擴大族群時保持穩定"},{"item":"價值鏈分配","level":"🟡","text":"付款方（Medicare、PBM）與經銷商議價力強：前三大經銷商營收占比55%／35%／46%且逐年上升，Q2經銷通路營收約11.02億美元對直銷約2.06億美元；CMS 2028年起以第75百分位得標價付款。DXCM毛利率仍守在65.1%，代表感測器目前仍是最難取代的環節，但分配正往付款方移動"},{"item":"社會容忍度","level":"🟡","text":"CGM屬必要醫療耗材、價格彈性低，但政策已顯示價格天花板：CMS把CGM納入競標並預期降低Medicare給付，公司長期計畫只假設名目價格影響。Medicare占營收比重事實表未涵蓋，無法量化；此項已列入反證紀錄"}],"roiic":"事實表未涵蓋投入資本與增量資本，無法計算；FY2023→FY2025 GAAP營業利益由約5.98億增至約9.12億美元，增量資本未知","reinvest_rate":"約−29%（FY2025代理算法：再投資率≈（淨利−FCF）÷淨利＝（8.36−10.77）÷8.36；事實表沒有稅後營業利益，以淨利代替）。FCF含SBC加回，若以2026年Q3年化約1.47億美元把SBC當現金成本扣回，約−11%，符號不變。可能看錯的地方：只有一個年度，單年營運資金回收會讓數字偏負。前三季資本支出2.142億美元約占FCF的24%，Ireland擴產已完成","endo_ceiling":null,"formula_note":"內生成長率＝增量ROIC×再投資率。增量ROIC缺投入資本算不出，天花板不給精確數字；但再投資率為負（約−29%，扣回SBC後約−11%），只要增量ROIC為正，天花板就在零以下，不需要增量ROIC的數字也能判定共識EPS成長超出天花板。超出部分來自既有產能與剛投產的Ireland承接涵蓋擴張的量、利益率擴張與回購，不靠新增投入資本"}}}},"q3_growth":{"verdict":"成長跑道寬：第二型非胰島素滲透率低且有A級臨床證據撐涵蓋，但成長以量為主、每用戶營收在降，EPS超額成長靠利益率與回購","reasoning":"共識EPS：FY2025A 2.09（GAAP攤薄）→FY2026E 2.71→FY2027E 3.13→FY2028E 3.67（Koyfin快照，EPS家數事實表未涵蓋；營收共識27位分析師），三年年增約20.6%，排除FY2026利益率修復後FY2026E→FY2028E約16.4%，同期營收約年增11%。內生成長天花板算不出精確數字（投入資本未涵蓋），但FY2025淨利8.36億美元、FCF 10.77億美元，再投資率約−29%（扣回SBC後約−11%），只要增量ROIC為正，天花板就在零以下，共識EPS成長全數超出天花板；超出部分可歸因於營收約11%（既有產能承接涵蓋擴張的量）、利益率擴張（投資人日：營業利益率每年約+150bp）與淨回購（年約2–3%），三項相乘約每年20%上下，共識沒有超過，不屬依賴重估。跑道：美國第一型滲透率已約60–65%，第二型2030年滲透率假設10–15%、非胰島素商保涵蓋25%，以現行速度到30%滲透約需8–10年（推估），加上國際直營化、Stelo自費與前期糖尿病篩檢（CEO Q3法說）等第二曲線，五年後跑道判寬。衰退信號亮2項（EPS成長高於營收逾5個百分點、自身倍數系統性下移），價值陷阱風險中等","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_peer_dxcm_fcf_margin_pct","f_peer_dxcm_operating_margin_pct","f_kpi5_fy2026","f_kpi3_fcf"],"verdict_values":{"growth":{"driver_mix":"量為主：活躍用戶年增十幾%上段、新病患創紀錄（CEO Q3法說）；價為負貢獻：營收年增11%低於用戶增速，每用戶營收下滑；併購僅小型（Nutrisense、歐洲經銷商直營化）；回購補EPS：2026年已買回10億美元，2027年承諾至少50% FCF回購","runway_years":"約8–10年（推估）","runway_post_y5":"🟢","endo_ceiling_basis":"天花板算不出精確數字（增量ROIC缺投入資本），但符號可定：FY2025淨利8.36億美元、FCF 10.77億美元，再投資率約−29%，扣回SBC後約−11%，只要增量ROIC為正，天花板在零以下。交叉核對：共識EPS三年年增約20.6%（FY2025A GAAP 2.09→FY2028E 3.67，Q3 GAAP與調整後營業利益只差約1,230萬美元，口徑近似）、FY2026E→FY2028E約16.4%，全數超出天花板；拆成營收約11%（既有產能與剛投產的Ireland承接涵蓋擴張的量）、利益率擴張（投資人日每年約+150bp，以24%為基期約每年貢獻6%，2030年目標29–30%）與淨回購年約2–3%，三項相乘約每年20%上下，共識16–20%沒有超過，可歸因","segments":[{"item":"美國","value":"Q3 2026營收9.70億美元，年增14%，約占72%；連續多季拿份額，最大增量來自第二型（含非胰島素）"},{"item":"國際","value":"Q3 2026營收3.75億美元，年增5%，約占28%；去年下半年多項給付利多造成高基期，管理層預期2027年初回到較高有機成長；歐洲最大剩餘經銷市場收購直營待2027年完成"},{"item":"通路","value":"Q2 2026經銷通路營收約11.02億美元、直銷約2.06億美元，經銷約占84%"}],"decay_signals":["毛利率連2季年減：未亮（Q3年增約380bp）","核心市占近12個月縮減：未亮（美國連季拿份額，管理層口徑；第三方時間序列未涵蓋）","提價後銷量下滑：未亮","EPS成長顯著高於營收成長：亮（共識FY2026E→FY2028E EPS年增約16.4%對營收約11%）","FCF對淨利低於0.75連2年：未亮（FY2025為1.29倍）","SBC占營收逾5%且上升：未亮（2.7%）","TAM萎縮或被替代：未亮（非侵入式替代技術查無報導）","估值倍數近3年系統性下移：亮（以公司自身為代理，本益比、P/S、EV/S都在近4個年度端點最低處；同業倍數未涵蓋）","維持性資本支出占FCF逾60%：未亮（前三季總資本支出約占FCF 24%）","停止投資新產能且營收下滑：未亮（Ireland剛投產）"],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"現金轉換強、SBC稀釋低，回購積極但以現價換算的報酬偏低","reasoning":"FCF：2026年前三季9.062億美元（營業現金流11.204億減資本支出2.142億），FY2025 FCF 10.77億美元對淨利8.36億美元，轉換率1.29倍；SBC占營收2.7%（Q3 3,680萬美元）；淨現金4.25億美元。現金去向：2026年回購10億美元已完成，董事會2026-10-29再授權10億美元至2027年底，承諾2027年至少50% FCF回購；小型收購Nutrisense（價格未揭露）與歐洲經銷商（簽約未完成）。治理：投資人日宣布與Elliott合作新增2名董事、董事會原無獨立醫材背景董事；CFO於Q3兼任營運長。回購均價、近三年現金去向四分、債務到期結構事實表未涵蓋","fact_refs":["f_kpi3_fcf","f_kpi4_sbc","f_net_debt_m","f_shares_diluted_m","f_ev_m","f_fwd_pe_latest"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":false,"passed":null,"input":"近年無重大併購：Nutrisense價格未揭露、非CGM營收年僅數百萬美元以下，歐洲經銷商收購簽約未完成（2027年完成），無已實現報酬可評"},{"name":"buyback_yield","applicable":true,"passed":false,"input":"回購均價事實表未涵蓋；以現價換算前瞻盈餘殖利率約3.3%（30.4倍）、FY2025 FCF殖利率約3.5%（10.77億÷市值306.9億美元）；10年期公債殖利率事實表未涵蓋，但須低於約1.5%才過，判定不過"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"SBC年化約1.47億美元（Q3 3,680萬×4），約占市值0.5%，且回購使股數淨減，淨稀釋率遠低於1.5%"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購撐：近年只有小型收購（Nutrisense營收極小、歐洲經銷商直營化未完成），資本回饋以回購為主，現金去向已在理由交代；近三年現金去向四分與回購均價事實表未涵蓋"}}}},"q5_valuation":{"verdict":"現價要求五年EPS年增約13%且終端倍數不低於22倍，才有約9%年報酬；EPS成長我信大半，倍數再壓縮的風險還在，合理不便宜","reasoning":"現價82.29美元＝FY2026E共識EPS的30.4倍、FY2027E 26.3倍、FY2028E 22.4倍。要拿到約9%年報酬，需要五年EPS年增約13%（Base 5.05美元）且終端倍數不低於22倍（約等於現價對FY2028E的倍數）。EPS成長我信大半（財測連升、利益率路徑清楚），倍數再壓縮的風險還在（競標、價格戰）。一年目標：FY2028E Base EPS 3.55美元×24.5倍≈87美元，約+6%；五年：5.05×22≈111美元，約+35%，另加回購。賣方均價86.16美元（Q3前，25位），區間65–112美元、最高最低比1.7倍，方向支持合理不便宜的判斷。同業倍數事實表未涵蓋","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_pe_current","f_pe_percentile","f_ps_current","f_ps_percentile","f_ev_s_current","f_ev_s_percentile","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_fy1_pct","f_consensus_rev_fy2_pct","f_ev_s_fwd","f_week26_return_pct","f_rsi14"],"verdict_values":{"valuation":{"basis":"前瞻本益比（FY2026E共識EPS 2.71美元）為主，PEG輔助","tier":"大型醫療器材成長股","peers":{"expanded":false,"reason":"事實表同業對照只有利潤率與研發密度，無同業前瞻本益比，無法做同級倍數錨定；改用自身倍數與FY2028E共識倍數交叉檢查"},"fwd_pe":30.37,"peg":1.47,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"前瞻本益比30.4倍、FY2027E 26.3倍、FY2028E 22.4倍；PEG約1.47（三年EPS年增約20.6%，FY2025基期偏低；只看FY2026E→FY2028E的16.4%則約1.85），落在1–2合理區；五年分位事實表未涵蓋，只有近4個年度端點分位：本益比0.5、P/S 2.0、EV/S 0.3，皆在區間最低處；賣方均價86.16美元僅高於現價約5%；Base五年終端約111美元，含回購年報酬約9%，屬中等，合理不便宜","upside_short_pct":6,"upside_mid_pct":35,"denominator_disputed":false,"denominator_note":"分母為FY2026E共識EPS，已含Ireland投產費用、無一次性扭曲；GAAP與調整後營業利益差距小（Q3約1,230萬美元），分母不是爭點"}}},"q6_how_wrong":{"verdict":"最可能看錯在價格：競標、OTC與PBM排他讓每用戶營收降得比利益率擴張快","reasoning":"最可能看錯的三條路：一是價格壓縮比預期快（2028年競標、OTC價格下探、PBM排他）；二是CMS涵蓋否決或附門檻；三是品質與訴訟復發。歷史最大回撤、空方最強數字與訴訟金額事實表未涵蓋；股價82.29美元仍低於250週均線92.85美元、該均線13週斜率−0.75%，說明過去五年曾在更高價位後長期下跌，26週已反彈34.1%。完整反證見反證紀錄","fact_refs":["f_ma_w250","f_ma_slope_w250_pct","f_price_at_dd","f_week26_return_pct","f_ma_state"],"verdict_values":{"trap":{"verdict":"🟡","label":"中度：EPS成長快於營收、靠利益率與回購撐，自身倍數已系統性下移"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":2.71,"pe":30.37,"basis":"FY2026E共識EPS（Koyfin 2026-10-31快照）；終端倍數同樣套在終端年當年度EPS，與現價前瞻倍數同口徑"},"eps":{"bull":[3.25,3.85,4.55,5.35,6.2],"base":[3.1,3.55,4.05,4.55,5.05],"bear":[2.9,2.75,2.8,2.9,3.0]},"pe":{"bull":28,"base":22,"bear":16},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0,"net_buyback":2.5},"second_stage":{"bull_cagr_pct":14,"base_cagr_pct":9},"max_dd":{"lo":-50,"hi":-35,"basis":"下緣−50%：Bear終點約48美元（3.00美元×16倍）較現價約−42%，CMS否決或品質事件屬單季即可兌現的衝擊，過程中可能先超跌；上緣−35%：倍數壓到約17倍FY2027E共識（約53美元）即達。歷史最大回撤事實表未涵蓋，股價低於250週均線且均線斜率為負，可佐證過去曾有深度下跌","trigger_time":null},"basis":{"bull":"CMS 2027年中涵蓋第二型非胰島素並帶動商保跟進，營收年增11–12%；15日款與G8使毛利率升到60%後段、營業利益率2031年約28–30%（投資人日目標）；淨回購每年2–3%；倍數28倍低於現價30.4倍","base":"CMS通過但2028年競標壓Medicare價格，營收年增約9–10%；營業利益率由24%升到2031年約26%，低於公司目標；淨回購約2%/年；EPS略低於共識（FY2027 3.10對3.13）；終端22倍約等於現價對FY2028E共識倍數，同業倍數事實表未涵蓋","bear":"CMS否決或設限，加上2028年競標與OTC價格戰，每用戶營收年降中個位數，營收年增僅4–5%；營業利益率退回2025年約19.6%水準；EPS五年停在約3美元，倍數以成長熄火情境壓到16倍。機率30%：再投資率為負、內生成長天花板在零以下，EPS靠利益率與回購，且五年內有CMS決定與競標兩個政策事件。淨回購率三情境共用2.5%：Bear的FCF較低，但股價跌得更多（終點約48美元對Base約111美元），若維持至少半數FCF回購，換算成市值的比例不會低於Base，沿用不會高估Bear；淨現金4.25億美元約占市值1.4%，不隨情境調整"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"CMS將CGM納入DMEPOS競標，2028-01-01起以第75百分位得標價付款、預期約10份合約並降低Medicare給付；研究機構預測OTC感測器兩年內跌破60美元；對手在其法說提到自費市場定價逆風（Q3法說分析師轉述）；中國新興廠與醫材以外的大型企業進場；美國份額Abbott 48.5%仍高於DXCM 44.7%","assumption":"公司長期計畫只假設名目價格影響、營業利益率每年約擴張150bp","consequence":"每用戶營收年降中個位數且DXCM被迫跟價，營業利益率退回約19.6%（2025年水準），EPS五年停在約3美元、倍數壓到16倍，股價約48美元，較現價約−42%","ruling":"部分採納：定為Bear情境、機率30%；不採為Base，因為Q3毛利率65.1%是2022年Q4以來最高、CFO稱全球未見定價惡化，2027年處方集已鎖定。與唯一致命點部分重疊（CMS否決會加速這條路），已回補進Bear機率","watch":"非GAAP毛利率（排除Ireland投產）是否連2季低於62%；2027年競標得標價與合約數","evidence_refs":["competitive_share_entrants#2","end_markets#2","competitive_share_entrants#0","competitive_share_entrants#1","end_markets#1","substitute_technology#3"]},{"view":"論點失敗","evidence":"2025-03 FDA警告信（聖地牙哥與Mesa廠製造與品質系統不符、G6/G7感測器未經核准變更）；六件G6/G7使用者集體訴訟、證券集體訴訟（2026-02-06提第二次修正訴狀）與衍生訴訟；ASIC與生物介面膜聚合物單一來源；製造集中Mesa與馬來西亞（二手摘要）","assumption":"品質問題已解決（投資人日CEO承認黏著問題尚未完全解決，Q3稱新黏膠使15日存活率提高4–5個百分點）","consequence":"品質問題復發或訴訟取得集體認證並不利和解，毛利率與份額同時受傷，警告信未結案時新品審查也可能受拖累","ruling":"反駁為主論點：Q3毛利率改善部分來自報廢與品質管理，存貨水準已穩定；Ireland投產讓製造擴到美、歐、亞三地，晶片已向FDA申請第二來源。但訴訟金額、受影響營收與警告信是否結案事實表未涵蓋，標為資料缺口","watch":"FDA警告信結案公告；使用者訴訟集體認證裁定；任何召回或出貨中斷","evidence_refs":["regulatory_antitrust#2","major_events#0","major_events#1","lawsuit_class_action#0","lawsuit_class_action#1","lawsuit_class_action#2","geo_supply_chain#0","geo_supply_chain#1","customer_second_source#0"]},{"view":"論點成功但股東經濟變差","evidence":"CEO稱活躍用戶年增十幾%上段，但Q3營收只年增11%，每用戶營收在降（15日款一年用量較少、國際分級定價、藥局通路轉換曾使Q1營收季減6–7%）；前三大經銷商營收占比55%／35%／46%逐年升；Dexcom Direct與歐洲經銷商直營化都要花錢","assumption":"CMS涵蓋帶來的量讓營收維持10%以上，並帶出營業利益率擴張","consequence":"量起來但落在給付較低的政府與自費通路，營收成長追不上用戶成長，利益率卡在24–25%，EPS只跟營收同速，Base的13%EPS年增變成10%左右","ruling":"部分採納：Base已把營業利益率路徑壓到2031年約26%，低於公司29–30%目標；若FY2027非GAAP營業利益率財測低於25%，再下修Base","watch":"FY2027營業利益率財測（2027年2月）；營收年增與活躍用戶年增的差距","evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#2","channel_business_model_shift#1"]},{"view":"價格已反映太多","evidence":"26週上漲34.1%；前瞻本益比30.4倍；分析師提到2027年共識營收約年增11%已接近公司10%以上的下限；Q4財測隱含年增約10%；Q3前賣方均價86.16美元、區間65–112美元，Barclays目標71美元","assumption":"市場已把CMS通過與利益率擴張大致計入","consequence":"CMS通過只換來小幅上修，股價在26倍FY2027E附近原地踏步；Base五年含回購年報酬約9%，只是中等","ruling":"部分採納：不視為高估（自身倍數在近4個年度端點最低處、Base終端22倍已假設再壓縮），但也不構成便宜，故等事件結果、不追價","watch":"前瞻本益比若升到35倍以上而共識EPS未上修，轉為減碼或不追","evidence_refs":["capital_markets_pricing#2","capital_markets_pricing#3"],"fact_refs":["f_week26_return_pct","f_fwd_pe_latest","f_pe_percentile","f_ps_percentile"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 None → 本次 ❌","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=None","side_b":"本次 ma=❌","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 None → 本次 82.29","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=None","side_b":"本次 price_at_dd=82.29","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"管理層承諾對帳（一致判斷）","cause":null,"prior_field":null,"side_a":"Q2法說（2026-07-30，CFO Jereme Sylvain）：全年營收5.18–5.25B、非GAAP營業利益率23.5–24%、毛利率Q3見高後因Ireland回落；投資人日（2026-05-14）：2026年回購10億美元、年底接近半數美國用戶轉15日款、加拿大下半年上市","side_b":"Q3法說（2026-10-29）：營收財測升至5.20–5.25B、營業利益率升至約24%、Q3毛利率65.1%並預告Q4回落；10億美元回購已完成並再授權10億美元；15日款轉換進度「接近50%」照舊；加拿大11月上市","ruling":"一致：近兩季承諾全部兌現或超前，管理層財測可信度加分；國際年增僅5%在Q2已預告高基期，不算改口","evidence_level":"公司法說逐字稿與8-K","settle_metric":"2027年2月財測營收年增是否≥10%","if_then":["若2027年財測營收年增低於10%，視為投資人日逐年10%以上承諾首度失守，下修Base並暫停任何加碼"],"evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#1","major_events#2"]},{"axis":"定價：管理層稱穩定對外部壓價訊號","cause":null,"prior_field":null,"side_a":"CFO（Q3法說）：全球未見定價惡化，國際按給付分級配產品、價格穩定；Q3非GAAP毛利率65.1%為2022年Q4以來最高","side_b":"對手提到自費市場定價逆風；研究機構預測OTC感測器兩年內跌破60美元；CMS 2028年起競標並預期降低Medicare給付；CVS排他合約流失","ruling":"可調和（時間與市場不同）：現況數據站在管理層這邊，壓價主要落在自費與新進國際市場以及2028年後的Medicare；採管理層現況，把未來壓價放進Bear 30%","evidence_level":"公司財報為硬數據，壓價方為預測與對手口徑","settle_metric":"非GAAP毛利率（排除Ireland）與2027年競標得標價","if_then":["若2027年下半年非GAAP毛利率回不到64%以上且管理層改口承認價格壓力，Bear機率上調到40%並停止加碼","反向：若2027年毛利率站上66%且競標價格降幅低於10%，維持Base並解除價格疑慮"],"evidence_refs":["competitive_share_entrants#2","end_markets#2"]},{"axis":"份額方向","cause":null,"prior_field":null,"side_a":"DXCM在拿份額：Q1營收年增15%對Abbott CGM 7.5%；Q3美國年增14%、連續多季拿份額（CEO）；CFO稱兩大廠合計美國低雙位數成長，DXCM占其中一大塊","side_b":"Abbott份額水準較高（2025年全球52.8%、美國48.5%），分析師認為雙分析物策略可能讓Abbott領先；Barclays以Libre份額壓力給減碼評等、目標71美元","ruling":"可調和（水準對方向）：Abbott份額水準較高、看空方是預測，看多方是已實現成長率；採已實現數據，競爭趨勢判持平而非上升","evidence_level":"已實現季報對第三方預測","settle_metric":"每季DXCM美國營收年增對Abbott糖尿病照護營收年增","if_then":["若DXCM美國營收年增連2季低於Abbott同期，競爭趨勢改判下降，以目前B級護城河即轉為迴避：未建倉不建、已持有清倉","反向：若連4季領先3個百分點以上，可上調執行面評分"],"evidence_refs":["competitive_share_entrants#0","end_markets#1","substitute_technology#3","competitive_share_entrants#3"]},{"axis":"營收成長對用戶成長","cause":null,"prior_field":null,"side_a":"管理層：定價穩定、活躍用戶年增十幾%上段、新病患創紀錄","side_b":"營收只年增11%、Q4財測隱含約10%，每用戶營收下滑","ruling":"可調和：不是單價下跌而是組合轉向（15日款年用量少、第二型非胰島素與國際分級產品單價低、藥局通路）；但這正是利益率擴張被稀釋的路徑，已列入論點成功但股東經濟變差的反證","evidence_level":"管理層口徑與財報推算","settle_metric":"營收年增減活躍用戶年增的差距（公司不定期揭露）","if_then":["若2027年營收年增低於10%而管理層仍稱用戶年增十幾%，視為每用戶營收下滑加速，Base營業利益率路徑再下修1個百分點"],"evidence_refs":["channel_business_model_shift#1","customer_concentration_credit#2"]},{"axis":"PBM合約流失的財務影響","cause":null,"prior_field":null,"side_a":"CFO（Q3法說）：該PBM占美國營收不到4%，轉非優先後病患自付大幅提高、對2027年財務影響不大；CEO稱2027年處方集已鎖定，Dexcom Direct 2027年初上線協助轉醫療給付","side_b":"流失發生在不到一季前，影響尚未進財報；若其他PBM跟進排他模式，價格與量同時受壓","ruling":"管理層歸因不採信也不否定，標為未證、監測；預登記：2027年Q1與Q2美國營收年增若連2季低於10%且公司歸因PBM，視為影響不大的說法證偽","evidence_level":"管理層一方說法","settle_metric":"2027年上半年美國營收年增","if_then":["證偽則減碼一半，或延後建倉到2028年處方集公布"],"evidence_refs":[]},{"axis":"產業態勢三軸","cause":null,"prior_field":null,"side_a":"A軸競爭惡化：中國新興廠與醫材以外業者進場、FDA一般健康器材指引降低門檻、Abbott雙分析物先行、對手用AI加速創新、OTC價格下探","side_b":"B軸結構轉好：CONNECT登上NEJM屬A級證據、四大商業PBM涵蓋所有糖尿病患、CMS決定預期年底前、全球涵蓋人數2030年預期到約5,200萬；C軸其他：CMS競標2028年起、PBM排他、通路轉向藥局、經銷商集中","ruling":"雙向拉鋸：2027年前B軸（涵蓋擴張）占上風，2028年起A軸與C軸的競標壓價轉強；依據為CMS決定預期2026年底、競標付款2028-01-01起變更","evidence_level":"10-K、公司法說與第三方研究","settle_metric":"CMS涵蓋決定與2027年競標得標價","if_then":["若CMS涵蓋通過但競標得標價降幅超過15%，判定C軸壓過B軸，Base營收成長下修到8%"],"evidence_refs":["competitive_share_entrants#1","competitive_share_entrants#2","substitute_technology#0","end_markets#3","supply_demand_durability#1"]},{"axis":"等CMS決定對現在就買","cause":null,"prior_field":null,"side_a":"本判斷：等CMS決定公布再動，因為否決是最大單一敏感度、Base含回購年報酬僅約9%、股價仍在250週均線下方","side_b":"現在就買的最強論證：CONNECT登上NEJM且屬A級證據，CMS通過機率約75–80%；自身倍數在近4年最低處；公司每年至少50% FCF回購；通過消息一出可能跳空，等待成本是錯過重估","ruling":"選等待：通過的上行已部分反映在26週上漲34%與30倍前瞻本益比，否決的下行（Bear約−42%）大於通過的跳空；事件只剩約兩個月，等待成本有限","evidence_level":"情境樹機率與事件時點","settle_metric":"CMS決定內容","if_then":["CMS通過且未設門檻→重跑判斷，首倉以小部位起步","CMS否決或設限→不建倉，等2027年2月財測確認營收年增≥10%再評","價格先走證據未到：決定公布前股價續漲→不追；跌到約70美元但決定未出→仍等決定，不搶跑"],"evidence_refs":["end_markets#3"]}],"triggers":[{"n":1,"text":"CMS第二型非胰島素CGM涵蓋決定（唯一致命點）","type":"Single Thing","maps_to":"single_thing","metric":"CMS決定內容與公布時點","threshold":"否決、附A1c門檻等限制，或2027-03-31前仍未決定","action":"不建倉；已持有則減碼一半，若2027年財測營收年增也低於10%則清倉","source_freq":"CMS公告與公司8-K，事件型","date":"2026-12-31","evidence_refs":["end_markets#3","supply_demand_durability#1"]},{"n":2,"text":"涵蓋通過後重新評估進場","type":"估值rearm","maps_to":"R1","metric":"CMS決定內容","threshold":"通過且未設A1c門檻","action":"重跑判斷，首倉以小部位起步，跳空超過FY2027E 30倍（約94美元）不追","source_freq":"事件型","date":"2026-12-31"},{"n":3,"text":"2027年全年營收財測","type":"假設驗證","maps_to":"H1","metric":"FY2027營收財測年增率","threshold":"≥10%","action":"低於10%：停止加碼、Base營收路徑下修","source_freq":"年度財測","date":"2027-02"},{"n":4,"text":"2027年營業利益率財測","type":"假設驗證","maps_to":"H2","metric":"FY2027非GAAP營業利益率財測","threshold":"≥25%","action":"低於25%：Base利益率路徑下修、Bear機率升到35%","source_freq":"年度財測","date":"2027-02"},{"n":5,"text":"毛利率守不住（含Ireland投產歸因期限）","type":"風險","maps_to":"R2","metric":"非GAAP毛利率","threshold":"2027年Q3仍未回到64%以上（Ireland歸因證偽），或之後連2季低於62%","action":"減碼一半","source_freq":"季報","date":"2027-10","evidence_refs":["competitive_share_entrants#2","end_markets#2","channel_business_model_shift#1"]},{"n":6,"text":"品質、FDA與訴訟里程碑","type":"風險","maps_to":"R3","metric":"FDA警告信結案、召回、使用者訴訟集體認證、證券訴訟和解","threshold":"新警告信或一級召回；使用者訴訟取得集體認證","action":"集體認證加不利和解→減碼一半；刑事或SEC調查介入→清倉","source_freq":"8-K與10-Q，事件型","date":null,"evidence_refs":["regulatory_antitrust#2","major_events#0","major_events#1","lawsuit_class_action#0","lawsuit_class_action#1","lawsuit_class_action#2"]},{"n":7,"text":"關稅與匯率吸收失敗","type":"風險","maps_to":"R2","metric":"公司歸因關稅或匯率的毛利率與營收影響","threshold":"單季歸因關稅使毛利率年減超過100bp，或匯率使全年營收財測下修超過1%","action":"減碼","source_freq":"季報","date":null,"evidence_refs":["reg_tariff_export#0"]},{"n":8,"text":"供貨中斷","type":"風險","maps_to":"R4","metric":"出貨中斷或延遲公告、存貨水準","threshold":"任何因單一來源零件或廠區問題造成的出貨中斷","action":"減碼一半，待恢復出貨且毛利率確認","source_freq":"8-K與季報，事件型","date":null,"evidence_refs":["geo_supply_chain#0","geo_supply_chain#1","customer_second_source#0"]},{"n":9,"text":"經銷商集中度","type":"風險","maps_to":"R5","metric":"最大經銷商營收占比（未扣回饋前）與應收占比","threshold":"營收占比>60%或應收占比>30%","action":"倉位上限下修一級並檢視合約條款","source_freq":"10-K年度","date":"2027-02","evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#2"]},{"n":10,"text":"份額轉向流失","type":"清倉","maps_to":"R6","metric":"DXCM美國營收年增對Abbott糖尿病照護營收年增","threshold":"連2季落後","action":"競爭趨勢改判下降，清倉或不建倉","source_freq":"季報","date":null,"evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1","end_markets#1","substitute_technology#0","substitute_technology#3"]},{"n":11,"text":"估值過熱","type":"減碼","maps_to":"H1","metric":"前瞻本益比","threshold":"≥35倍且FY2027E共識未上修","action":"減碼或不追","source_freq":"每日價格與每月共識","date":null},{"n":12,"text":"Q4 2026財報與2027年財測後重跑判斷","type":"複審日期","maps_to":"H1","metric":"全年財測與CMS進度","threshold":"財報公布","action":"重跑判斷","source_freq":"季報","date":"2027-02"}],"kill_metrics":[{"metric":"CMS第二型非胰島素CGM涵蓋決定","bear_threshold":"否決、附A1c門檻，或2027-03-31前未決定","window":"2026-12～2027-03","source":"CMS公告、公司8-K","last_status":"unknown"},{"metric":"非GAAP毛利率（Ireland投產後）","bear_threshold":"2027年Q3未回到64%，或之後連2季低於62%","window":"2027年Q3起逐季","source":"公司季報新聞稿","last_status":"ok"},{"metric":"全年營收年增率","bear_threshold":"FY2027財測或實績低於10%","window":"2027年2月財測與各季","source":"公司財測與季報","last_status":"warning"},{"metric":"美國營收年增率","bear_threshold":"連2季低於8%或連2季落後Abbott糖尿病照護","window":"逐季","source":"DXCM與Abbott季報","last_status":"ok"},{"metric":"最大經銷商營收占比（未扣回饋前）","bear_threshold":">60%","window":"年度","source":"10-K集中度附註","last_status":"warning"}],"evidence_dismissed":[{"ref":"$.decision_inputs.market_wrong_reason_given","reason":"判斷沒有主張市場看錯，填否是照實：估值結論是合理不便宜，反證紀錄「價格已反映太多」一條部分採納，承認市場已大致計入CMS通過與利益率擴張。報酬來源是EPS年增約13%，終端倍數還從30.4倍壓到22倍，論點不靠倍數往上修，而「市場錯在哪」的具體理由只在論點靠倍數往上修時才需要。觀望是等CMS決定這個事件，不是等市場改正看法，等待條件已寫明通過與否決各自的做法；閘自己也判定輸入互相一致、應降為輕微"},{"ref":"$.answers.q1_business.verdict_values.industry.sd_verdict_source","reason":"這段結論沒有引用閘點名的那條供需資料，依據已逐一寫在欄內：Baird與MarketBeat彙整的第一型滲透率約60–65%、CEO投資人日的第二型非胰島素約2,500萬人與商保涵蓋約25%。該條只在CMS決定時點的三處（產業態勢三軸、唯一致命點觸發、R1）與另一條終端市場資料並列引用，拿掉不影響供需判斷；閘的疑點是附件沒附原文，不是判斷漏接，閘也寫明找不到漏接"}],"action_conditions":{"rearm_trigger":"CMS公布第二型非胰島素CGM涵蓋且未附A1c門檻等限制（預期2026年底前），之後重跑判斷再建首倉","exec_line":"決定公布前不建倉、不搶跑；通過且非GAAP毛利率維持62%以上→重跑判斷，首倉小部位，跳空超過FY2027E 30倍（約94美元）不追；否決或設限→不建倉，等2027年2月財測確認營收年增≥10%再評"}},"decision_inputs":{"signal":"B","ma":"❌","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等CMS第二型非胰島素CGM涵蓋決定（公司預期2026年底前）：通過且未附A1c門檻才重跑判斷建首倉；否決或設限則等2027年2月財測","qc48_result":null,"qc48_note":null,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null},"decision_out":{"role":"追蹤","row_hit":"8w(原9)","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":true,"basis":"ma='❌'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟢', val='🟡', moat_trend='→', week26=34.13, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position=None, moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":false,"basis":"signal='B', val='🟡'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":true,"basis":"signal='B', val='🟡', ma='❌'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟡', ma='❌'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟡', ma='❌'"},{"row":"8w","condition":"判斷者宣告 wait_for_price（價格合理但要等）→ 原 row9 進場改觀望（等價格）","hit":true,"basis":"wait_for_price=True, 等待條件='等CMS第二型非胰島素CGM涵蓋決定（公司預期2026年底前）：通過且未附A1c門檻才重跑判斷建首倉；否決或設限則等2027年2月財測'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":["row4：週線❌，進場節奏強制分批（starter 1/3＋趨勢確認後加碼），頁首掛「⚠️ 週線趨勢未確認，逢回分批勿接刀」"],"holding_cap":null,"requires_critic":[],"verdict":"觀望"},"thesis":{"H":[{"id":"H1","text":"涵蓋擴張（第二型非胰島素、國際新給付、直營化）讓營收維持每年10%以上","2y":"FY2027營收年增≥10%（約57.5億美元以上），CMS涵蓋於2027年中生效","5y":null,"10y":null,"threshold":"FY2027全年營收年增≥10%；美國營收季度年增≥10%","source":"公司季報新聞稿與2027年2月全年財測","drift_rule":"TTM營收年增率連2季低於9.5%＝削弱；連3季低於9%＝反轉"},{"id":"H2","text":"15日感測器普及、Ireland投產成本攤平與G8製造成本較G7低至少10%，推動營業利益率擴張","2y":null,"5y":"FY2030非GAAP營業利益率≥27%（公司目標29–30%）、毛利率回到65%以上","10y":null,"threshold":"FY2027非GAAP營業利益率≥25%、FY2028≥26%；2027年下半年非GAAP毛利率≥64%","source":"公司季報新聞稿；投資人日（2026-05-14，CFO Jereme Sylvain）利益率目標","drift_rule":"TTM非GAAP營業利益率連4季低於當年門檻5%以上＝削弱；連6季低於10%以上＝反轉"},{"id":"H3","text":"CGM成為各型糖尿病標準照護，DXCM維持兩大廠地位","2y":null,"5y":null,"10y":"全球CGM營收份額≥30%（2025年33.89%），G8與多分析物平台如期接棒","threshold":"第三方年度CGM營收份額≥30%；美國營收年增不落後Abbott糖尿病照護同期成長","source":"Mordor與GlobalData年度份額估計；DXCM與Abbott季報","drift_rule":"份額跨2個年度低於30%＝削弱；跨3個年度＝反轉"}],"R":[{"id":"R1","text":"CMS第二型非胰島素涵蓋否決、延後或附A1c門檻，投資人日逐年10%以上營收計畫失去最大增量","h_ref":"H1","clock":"⚡","threshold":"2027-03-31前未公布決定，或決定附A1c門檻等限制","evidence_refs":["end_markets#3","supply_demand_durability#1"]},{"id":"R2","text":"價格壓縮：2028年Medicare競標、PBM排他處方集、OTC與對手在自費市場降價，加上藥局通路轉換壓低每用戶營收","h_ref":"H2","clock":"🔥","threshold":"非GAAP毛利率2027年Q3未回到64%或之後連2季低於62%；競標得標價降幅超過15%","evidence_refs":["competitive_share_entrants#2","end_markets#2","channel_business_model_shift#1"]},{"id":"R3","text":"品質與法律：2025-03 FDA警告信、六件G6/G7使用者集體訴訟、證券集體訴訟與衍生訴訟，品質問題復發會同時傷毛利率與份額","h_ref":"H2","clock":"🔥","threshold":"新警告信或一級召回；使用者訴訟取得集體認證；訴訟金額與受影響營收事實表未涵蓋","evidence_refs":["regulatory_antitrust#2","major_events#0","major_events#1","lawsuit_class_action#0","lawsuit_class_action#1","lawsuit_class_action#2"]},{"id":"R4","text":"供應鏈：ASIC與聚合物單一來源、製造集中Mesa與馬來西亞（二手摘要），替代產能難快速建立；Ireland投產與晶片第二來源申請為緩解","h_ref":"H1","clock":"⚡","threshold":"任何出貨中斷或延遲公告","evidence_refs":["geo_supply_chain#0","geo_supply_chain#1","customer_second_source#0"]},{"id":"R5","text":"經銷商集中：前三大經銷商未扣回饋前營收占比55%／35%／46%且三年逐年上升，議價力往下游移","h_ref":"H2","clock":"🐢","threshold":"最大經銷商營收占比>60%或應收占比>30%（FY2025為55%與24%）","evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#2"]},{"id":"R6","text":"競爭：Abbott規模與雙分析物先行、中國新興廠與醫材以外業者進場、對手用AI加速創新","h_ref":"H3","clock":"🔥","threshold":"美國營收年增連2季落後Abbott糖尿病照護同期，或第三方美國份額跌破40%（2025年44.7%）","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1","end_markets#1","substitute_technology#0","substitute_technology#3"]}],"single_thing":{"description":"CMS對第二型非胰島素患者的CGM涵蓋決定（公司預期2026年底前公布、2027年中生效），結果為否決、延後或附A1c門檻等限制","why_fatal":"第二型非胰島素是唯一的大型增量族群（美國約2,500萬人、商保涵蓋僅約25%），投資人日逐年10%以上的營收計畫把涵蓋時點放在2027年中；否決會讓成長退回現有涵蓋下的低雙位數並逐年下滑，正是Base與Bear的分水嶺","if_happens":"不建倉；若已持有減碼一半，等2027年財測確認營收年增是否仍≥10%；成長跌破10%且毛利率下滑則清倉","how_monitor":"CMS與Medicare承包商醫療主任公告、公司8-K與法說；ADA照護標準更新是否納入CONNECT","probability":"12–24個月內不利結果約20–25%（CONNECT登上NEJM屬A級證據、CEO稱時程未變並否認A1c門檻傳聞；但決定權在CMS，公司說法屬一方之詞）"}},"appendix_a":{"growth_durability":7,"quality_score":7,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":26.3,"peg_fy2":1.6,"stress":{"pass":2,"total":3}},"eps_meta":{"base_eps_path":{"FY2025A":2.09,"FY2026E":2.71,"FY2027E":3.13,"FY2028E":3.67},"fy_end_month":12,"eps_basis":"FY2025A取年度財報GAAP攤薄EPS 2.09（事實表無調整後EPS；Q3 2026 GAAP與調整後營業利益僅差約1,230萬美元，口徑近似）；FY2026E–FY2028E為Koyfin共識（調整後口徑），財年12月底"},"catalysts":[{"date":"2026-12","date_precision":"month","type":"regulatory","event":"CMS第二型非胰島素CGM涵蓋決定（公司預期年底前）","impact":"高","watch":"是否附A1c門檻；生效時點是否仍為2027年中"},{"date":"2026-12","date_precision":"month","type":"regulatory","event":"ADA照護標準更新，是否納入CONNECT","impact":"中","watch":"是否把CGM列為第二型非胰島素的強建議"},{"date":"2026-11","date_precision":"month","type":"product","event":"G7 15 Day加拿大上市","impact":"低","watch":"國際15日款推進節奏"},{"date":"2026-Q4","date_precision":"quarter","type":"capacity","event":"Ireland廠投產，毛利率季減","impact":"中","watch":"Q4毛利率回落幅度與2027年回升速度"},{"date":"2027-02","date_precision":"month","type":"guidance","event":"Q4 2026財報與2027年全年財測","impact":"高","watch":"營收年增是否≥10%、營業利益率是否≥25%"},{"date":"2027-Q1","date_precision":"quarter","type":"product","event":"Dexcom Direct上線、日本G7 15 Day上市","impact":"中","watch":"PBM流失病患的留存"},{"date":"2027-06","date_precision":"quarter","type":"regulatory","event":"CMS涵蓋預定生效","impact":"高","watch":"第二型非胰島素新病患占比"},{"date":"2027","date_precision":null,"type":"regulatory","event":"CMS DMEPOS競標簽約（2028-01-01起付款變更）","impact":"高","watch":"CGM得標價與合約數"},{"date":"2027-Q4","date_precision":"quarter","type":"product","event":"G8上市（2027年底或2028年初，視審查）","impact":"高","watch":"送件與核准時點、轉換策略"}]}
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
