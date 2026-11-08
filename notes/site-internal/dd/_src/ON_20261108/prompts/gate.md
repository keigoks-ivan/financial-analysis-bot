你是 DD 管線 v20 的判斷層閘（gate），標的 ON（20261108）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（42 條）
- `f_kpi0_gaap`（q1_business）｜營收（GAAP）＝1722.3 USD m｜期間與口徑：Q3 2026（季末 2026-10-02，公告於 2026-11-02）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：onsemi Q3 2026 新聞稿（IR 頁 investor.onsemi.com/news-releases/news-release-details/onsemi-reports-third-quarter-2026-results 回 403，改取同稿 8-K EX-99.1：https://www.sec.gov/Archives/edgar/data/1097864/000114036126041580/ef20084671_ex99-1.htm）（numbers.latest_quarter_kpis.items[0]，as_of Q3 2026（季末 2026-10-02，公告於 2026-11-02））
- `f_kpi2_non_gaap`（q1_business）｜Non-GAAP 營業利益率＝23.2 %｜期間與口徑：Q3 2026（季末 2026-10-02，公告於 2026-11-02）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：onsemi Q3 2026 新聞稿（IR 頁 investor.onsemi.com/news-releases/news-release-details/onsemi-reports-third-quarter-2026-results 回 403，改取同稿 8-K EX-99.1：https://www.sec.gov/Archives/edgar/data/1097864/000114036126041580/ef20084671_ex99-1.htm）（numbers.latest_quarter_kpis.items[2]，as_of Q3 2026（季末 2026-10-02，公告於 2026-11-02））
- `f_kpi4_gaap`（q1_business）｜GAAP 營業利益率＝22.0 %｜期間與口徑：Q3 2026（季末 2026-10-02，公告於 2026-11-02）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：onsemi Q3 2026 新聞稿（IR 頁 investor.onsemi.com/news-releases/news-release-details/onsemi-reports-third-quarter-2026-results 回 403，改取同稿 8-K EX-99.1：https://www.sec.gov/Archives/edgar/data/1097864/000114036126041580/ef20084671_ex99-1.htm）（numbers.latest_quarter_kpis.items[4]，as_of Q3 2026（季末 2026-10-02，公告於 2026-11-02））
- `f_kpi8_cogs_91`（q1_business）｜存貨天數（自算：期末存貨÷季 COGS×91）＝187 天｜期間與口徑：Q3 2026（季末 2026-10-02，公告於 2026-11-02）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：onsemi Q3 2026 新聞稿（IR 頁 investor.onsemi.com/news-releases/news-release-details/onsemi-reports-third-quarter-2026-results 回 403，改取同稿 8-K EX-99.1：https://www.sec.gov/Archives/edgar/data/1097864/000114036126041580/ef20084671_ex99-1.htm）（numbers.latest_quarter_kpis.items[8]，as_of Q3 2026（季末 2026-10-02，公告於 2026-11-02））
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝6607.47 USD m｜期間與口徑：2026-11-08／yfinance revenue_estimate 0y 平均（28 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_peer_on_gross_margin_pct`（q2_moat）｜ON 毛利率＝38.68 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ON.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_txn_gross_margin_pct`（q2_moat）｜TXN 毛利率＝60.24 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.TXN.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_nxpi_gross_margin_pct`（q2_moat）｜NXPI 毛利率＝56.43 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.NXPI.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_mchp_gross_margin_pct`（q2_moat）｜MCHP 毛利率＝60.19 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MCHP.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_stm_gross_margin_pct`（q2_moat）｜STM 毛利率＝33.84 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.STM.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_on_operating_margin_pct`（q2_moat）｜ON 營業利益率＝19.12 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ON.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_txn_operating_margin_pct`（q2_moat）｜TXN 營業利益率＝41.12 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.TXN.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_nxpi_operating_margin_pct`（q2_moat）｜NXPI 營業利益率＝28.55 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.NXPI.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_on_fcf_margin_pct`（q2_moat）｜ON FCF 利潤率＝25.38 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ON.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_txn_fcf_margin_pct`（q2_moat）｜TXN FCF 利潤率＝35.24 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.TXN.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_nxpi_fcf_margin_pct`（q2_moat）｜NXPI FCF 利潤率＝24.16 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.NXPI.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_mchp_fcf_margin_pct`（q2_moat）｜MCHP FCF 利潤率＝21.69 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MCHP.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_stm_fcf_margin_pct`（q2_moat）｜STM FCF 利潤率＝3.22 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.STM.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝3.28 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-11-07）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝4.71 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-11-07）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝6.08 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-11-07）
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝7593.65 USD m｜期間與口徑：2026-11-08／yfinance revenue_estimate +1y 平均（28 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi5_fcf`（q4_capital）｜自由現金流（FCF）＝488.6 USD m｜期間與口徑：Q3 2026（季末 2026-10-02，公告於 2026-11-02）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：onsemi Q3 2026 新聞稿（IR 頁 investor.onsemi.com/news-releases/news-release-details/onsemi-reports-third-quarter-2026-results 回 403，改取同稿 8-K EX-99.1：https://www.sec.gov/Archives/edgar/data/1097864/000114036126041580/ef20084671_ex99-1.htm）（numbers.latest_quarter_kpis.items[5]，as_of Q3 2026（季末 2026-10-02，公告於 2026-11-02））
- `f_kpi6_sbc_gaap`（q4_capital）｜SBC 占 GAAP 營業利益＝9.8 %｜期間與口徑：Q3 2026（季末 2026-10-02，公告於 2026-11-02）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：onsemi Q3 2026 新聞稿（IR 頁 investor.onsemi.com/news-releases/news-release-details/onsemi-reports-third-quarter-2026-results 回 403，改取同稿 8-K EX-99.1：https://www.sec.gov/Archives/edgar/data/1097864/000114036126041580/ef20084671_ex99-1.htm）（numbers.latest_quarter_kpis.items[6]，as_of Q3 2026（季末 2026-10-02，公告於 2026-11-02））
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝340.1 USD m｜期間與口徑：2026-11-08／yfinance 最新一季：總債務 4707.8、現金 4367.7（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝389.28 m shares｜期間與口徑：2026-11-08／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝63.31 USD｜期間與口徑：2026-11-06（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-11-06（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝19.3 x｜期間與口徑：2026-11-07／分母＝FY1 EPS 3.28，分子＝快照價 63.31｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-11-07）
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝37.02 x｜期間與口徑：2026-11-06（RTH 收盤，UTC）／4 個年度端點內的分位＝12.3｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-11-06（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝12.3 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝3.87 x｜期間與口徑：2026-11-06（RTH 收盤，UTC）／4 個年度端點內的分位＝68.9｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝68.9 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝3.92 x｜期間與口徑：2026-11-06（RTH 收盤，UTC）／4 個年度端點內的分位＝65.4｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝65.4 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝2.5 %｜期間與口徑：2026-08-13 → 2026-11-07／FY1 共識 EPS 3.2 → 3.28（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-11-07）
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝-38.65 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-11-06（RTH 收盤，UTC））
- `f_rsi14`（q5_valuation）｜RSI(14)＝34.16｜期間與口徑：2026-11-06（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ma_state`（q5_valuation）｜週線均線六態（decision_inputs.ma 必須等於此值）＝❌｜期間與口徑：2026-11-08／timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）
  - 原文：「price 63.31 / W52 76.51 / W104 63.96 / W250 69.17 / W250 13週斜率 0.15%」
- `f_ma_w52`（q5_valuation）｜52 週均線＝76.51 USD｜期間與口徑：2026-11-08／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）
- `f_ma_w104`（q5_valuation）｜104 週均線＝63.96 USD｜期間與口徑：2026-11-08／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）
- `f_ma_w250`（q5_valuation）｜250 週均線＝69.17 USD｜期間與口徑：2026-11-08／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）
- `f_ev_m`（q5_valuation）｜目前企業價值 EV（市值＋淨負債）＝24985.7 USD m｜期間與口徑：2026-11-08／市值 24645.6 ＋ 淨負債 340.1｜kind：realized
  - 來源：—（numbers.capital_structure.ev_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null

### findings_digest 中方向為負或來源衝突的條目（22 條）
- `competitive_share_entrants#1`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K 風險因子：公司承認 AI 資料中心電源可能無法如預期取得份額，失敗將導致市占流失；且無法保證贏得 design win。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-09）｜affects：decision_inputs.bear、thesis.R
- `competitive_share_entrants#2`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K 風險因子：部分對手獲政府補貼，若公司拿不到相同補助可能影響市占。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-09）｜affects：moat_trend、thesis.R
- `competitive_share_entrants#3`（competitive_share_entrants｜方向 -｜狀態 ok）：TrendForce 報導 onsemi 傳擬在捷克廠裁員最多 300 人，因中國低價 SiC 競爭加劇。
  - 來源：TrendForce News 2026-06-08（as_of 2026-06-08）｜affects：moat_trend、decision_inputs.bear
- `supply_demand_durability#2`（supply_demand_durability｜方向 -｜狀態 ok）：IBS Electronics 研究註記：2026 最可能是分段市場而非全面過剩，中國成熟製程新產能可能使部分品類交期正常化
  - 來源：IBS Electronics: China's mature node chip expansion in 2026（as_of 2026-01-01）｜affects：thesis.R、decision_inputs.bear
- `regulatory_antitrust#1`（regulatory_antitrust｜方向 -｜狀態 ok）：Capitol Forum 報導 onsemi 擬收購 Synaptics（約 $7B）可能受中國市場監管機關嚴格審查
  - 來源：The Capitol Forum（as_of 2026-07-09）｜affects：thesis.R、triggers
- `regulatory_antitrust#2`（regulatory_antitrust｜方向 -｜狀態 ok）：中國商務部對美國類比晶片（含 onsemi）發起反傾銷調查
  - 來源：SemiMedia（as_of 2025-09-22）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：onsemi 10-K 揭露：樂山（中國，持股80%）組裝測試廠可能因美中緊張面臨成本增加或貿易限制；商務部實體清單擴大可能要求對中國客戶申請額外出口許可，且不保證取得；進口零組件關稅可能衝擊獲利。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-09）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：CEO 警告所有地區的地緣不確定性持續造成波動（Benzinga 標題）
  - 來源：Benzinga: auto slowdown hits ON Semiconductor in Q4, Q1 outlook also dim（as_of 2025-02-10）｜affects：thesis.R
- `geo_supply_chain#2`（geo_supply_chain｜方向 -｜狀態 ok）：2026-06 報導 onsemi 捷克 SiC 廠擬裁最多 300 人，起因為中國低價 SiC 競爭；TrendForce 稱中國 SICC、天科合達占 2025 N 型基板銷售約 21.5%、20.1%
  - 來源：TrendForce News 2026-06-08（as_of 2026-06-08）｜affects：moat_trend、thesis.R
- `geo_supply_chain#3`（geo_supply_chain｜方向 -｜狀態 ok）：China 約占 onsemi 營收 30%，並標示地緣與關稅風險
  - 來源：Finterra via Observer-Reporter（as_of 2026-03-06）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#4`（geo_supply_chain｜方向 -｜狀態 ok）：捷克 Rožnov 廠 2026-06 擬裁 200–300 人，與中國 SiC 低價競爭有關；捷克新廠補貼約 €450M
  - 來源：Evertiq 2026-06-09（as_of 2026-06-09）｜affects：moat_trend、thesis.R
- `end_markets#0`（end_markets｜方向 -｜狀態 ok）：Q3 2026 營收 $1.72B，季增 7%、年增 11%；車用約 $777M，季減 1%、年減 1%，管理層稱因把受限產能轉向 AI 資料中心與工業，預期 2027 Q1 車用供給與營收恢復正常。
  - 來源：stockstory/marketbeat Q3 2026 call summaries (search summary)（as_of 2026-11-02）｜affects：thesis.R、decision_inputs.bear
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：10-K 風險因子載明：產品常被技術更先進的替代品取代，競爭對手的產品或技術可能使公司產品過時或失去競爭力。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-09）｜affects：moat_trend、thesis.R
- `substitute_technology#1`（substitute_technology｜方向 -｜狀態 ok）：10-K 載明：競爭對手開發的產品或技術可能使公司產品或技術過時或不具競爭力；競爭壓力可能限制提價能力。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-09）｜affects：moat_trend、decision_inputs.bear
- `substitute_technology#2`（substitute_technology｜方向 -｜狀態 ok）：TrendForce 報導 onsemi 因中國低價 SiC 競爭加劇，擬於捷克廠裁員最多約 300 人。
  - 來源：TrendForce News 2026-06-08（as_of 2026-06-08）｜affects：moat_trend、decision_inputs.bear
- `major_events#2`（major_events｜方向 -｜狀態 ok）：SiC 業務證券集體訴訟（Hubacek v. On Semiconductor）仍在審理中，申訴指控 SiC 業務誤導性陳述。
  - 來源：SEC EDGAR 10-K FY2025 財報附註 Legal Matters（as_of 2026-02-09）｜affects：decision_inputs.bear、thesis.R
- `major_events#3`（major_events｜方向 -｜狀態 ok）：2025-11-13 管理層核准 2–3 億美元非現金減損與加速折舊（製造資產），8-K Item 2.06 於 2025-11-17 申報。
  - 來源：SEC EDGAR 8-K Item 2.06 (2025-11-17)（as_of 2025-11-17）｜affects：thesis.R、valuation
- `cyclical_supply_discipline_capacity#3`（cyclical_supply_discipline_capacity｜方向 -｜狀態 ok）：Power SiC 面臨產能過剩下行，稼動率約 50%(上游)/70%(元件製程),中國為最大資本支出占比
  - 來源：DQ India, Power SiC faces overcapacity downturn（as_of 2026-01-01）｜affects：thesis.R、decision_inputs.bear
- `cyclical_supply_discipline_capacity#4`（cyclical_supply_discipline_capacity｜方向 -｜狀態 ok）：SiC 晶圓產能將於 2026 陸續釋出(TrendForce),Silan 預計 2026 滿產
  - 來源：LEDinside/TrendForce, Wafer Capacity Set to Surge: New Phase for SiC in 2026（as_of 2026-01-01）｜affects：thesis.R、decision_inputs.bear
- `cyclical_prior_downcycle_behavior#0`（cyclical_prior_downcycle_behavior｜方向 -｜狀態 ok）：ON 52週高點108.09(2023年7月)；2025年10月報價的52週區間為31.04–76.06；2025 Q1毛利率年減590bp至約40%，後續季度non-GAAP毛利率37.6%，主因降價與稼動率下滑造成固定成本未吸收（跨來源區間，非單一谷底季）
  - 來源：MarketBeat / Barchart / Tiger 等搜尋摘要（as_of 2025-10-31）｜affects：decision_inputs.bear、valuation
- `cyclical_prior_downcycle_behavior#1`（cyclical_prior_downcycle_behavior｜方向 -｜狀態 ok）：SOX 網路泡沫崩盤 2000/03–2002/10 下跌82%，約2.5年；2004–2026 間七次完成的≥20%回落，幅度約−25%至約−69%
  - 來源：quantflowlab: Semiconductor cycle history（as_of 2026-10-31）｜affects：decision_inputs.bear、thesis.R
- `lawsuit_class_action#0`（lawsuit_class_action｜方向 -｜狀態 ok）：Hubacek v. On Semiconductor 證券集體訴訟（指控 SiC 業務誤導性陳述，§10(b)/20(a)）仍未結案。
  - 來源：SEC EDGAR 10-K FY2025 財報附註 Legal Matters（as_of 2026-02-09）｜affects：decision_inputs.bear、thesis.R

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 4 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ON_20261108/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":210.0,"bear_5y_price":45.6,"p_bull_pct":20,"p_bear_pct":33,"upside_5y_pct":97.1,"ev5y_pct":82.8,"irr_base_pct":14.5,"asym_ratio":5.0,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":3.28,"pe":19.3,"basis":"FY1（FY2026E）共識 EPS 3.28，現價 63.31；終端倍數同樣用當年度 EPS"},"eps":{"bull":[4.95,6.7,8.1,9.4,10.5],"base":[4.45,5.55,6.4,7.15,7.8],"bear":[3.7,3.9,3.2,3.5,3.8]},"pe":{"bull":20,"base":16,"bear":12},"p":{"bull":20,"base":47,"bear":33},"yield_pct":{"dividend":0,"net_buyback":0},"second_stage":{"bull_cagr_pct":12,"base_cagr_pct":8},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### ON_Q2_2026_Earnings_Call_20260803.md
- 2026-08-03｜CFO Thad Trent｜guidance：Q3 營收財測區間（原話："in the range of $1.65 billion to $1.75 billion"）
- 2026-08-03｜CFO Thad Trent｜guidance：Q3 non-GAAP 毛利率財測區間（原話："is expected to be between 40% and 42%"）
- 2026-08-03｜CFO Thad Trent｜guidance：Q3 non-GAAP EPS 財測區間（原話："earnings per share in the range of $0.81 to $0.93."）
- 2026-08-03｜CFO Thad Trent｜guidance：Q3 分部財測：車用小增、工業持平、其他（含 AI 資料中心）高十位數增（原話："we expect auto to be up low single digits"）
- 2026-08-03｜CEO Hassane El-Khoury｜guidance：2026 AI 資料中心營收預期由「翻倍」上調為「超過翻倍」（原話："AI data center revenue to more than double in 2026"）
- 2026-08-03｜CEO Hassane El-Khoury｜guidance：2026 AI 資料中心碳化矽營收預期成長近 60%（原話："AI data center applications to grow nearly 60%"）
- 2026-08-03｜CEO Hassane El-Khoury｜guidance：2026 ESS 營收預期成長約 40%（原話："We expect our ESS revenue to grow approximately 40%"）
- 2026-08-03｜CEO Hassane El-Khoury｜guidance：中國車用碳化矽營收預期成長 60% 至 70%（原話："revenue in that market to increase between 60% and 70%"）
- 2026-08-03｜CFO Thad Trent｜guidance：2026 資本支出占營收預期低於 5%（原話："expenditure for the year to be below 5% of revenue."）
- 2026-08-03｜CFO Thad Trent｜margin：Q2 non-GAAP 毛利率季增 80 bps（原話："Non-GAAP gross margin expanded 80 basis points"）
- 2026-08-03｜CFO Thad Trent｜margin：Q2 毛利率改善來源為製造表現與有利產品組合；稼動率升至 83%（原話："Utilization increased to 83%"）
- 2026-08-03｜CFO Thad Trent｜margin：稼動率每提高一點對應毛利率改善 25 至 30 bps 的口徑（原話："The math is 25 basis points to 30 basis points"）
- 2026-08-03｜CFO Thad Trent｜margin：管理層表示 Q2 漲價對毛利率沒有明顯貢獻（被投入成本抵銷）（原話："wasn't much of a margin impact at all from pricing"）
- 2026-08-03｜CFO Thad Trent｜margin：稼動率約兩季後反映在損益表，Q4 稼動率下滑是 Q2 的逆風（原話："there's about 2 quarter for utilization to hit the P&L"）
- 2026-08-03｜CFO Thad Trent｜margin：Fab Right 出售兩座廠預計貢獻約 50 bps 的 200 bps 毛利率改善（原話："approximately 50 basis points of the 200 basis points"）
- 2026-08-03｜CFO Thad Trent｜margin：出售 Mountain Top 與菲律賓廠年化節省金額（原話："approximately $35 million of annualized savings"）
- 2026-08-03｜CFO Thad Trent｜margin：管理層表示因折舊已進入穩定狀態，且產能已下線約 12%（原話："we took capacity offline about 12%"）
- 2026-08-03｜CFO Thad Trent｜margin：管理層說明稼動率約 92% 至 93% 視為滿載，之後轉往外部代工（原話："in that low 90% with 92%, 93% is fully utilized"）
- 2026-08-03｜CFO Thad Trent｜commitment：管理層承諾營運費用成長慢於營收（原話："increase at a slower pace than revenue"）
- 2026-08-03｜CEO Hassane El-Khoury｜commitment：Synaptics 收購預計 2027 年中完成（原話："We expect the transaction to close in mid-"）
- 2026-08-03｜CFO Thad Trent｜commitment：截至年初累計回饋股東約 105% 的自由現金流（原話："we have returned approximately 105% of free cash flow."）
- 2026-08-03｜CFO Thad Trent｜capital_allocation：Q2 股票回購金額（原話："returned $332 million to shareholders"）
- 2026-08-03｜CFO Thad Trent｜capital_allocation：中期資本支出目標為營收的中個位數百分比（原話："kind of in that mid-single-digit percentage range"）
- 2026-08-03｜CEO Hassane El-Khoury｜commitment：管理層承諾 2026 年將樣品出貨產品數量加倍（原話："We remain on track to double the number of products sampling"）
- 2026-08-03｜CFO Thad Trent｜commitment：非核心營收退出已完成，不再於未來財測中討論（原話："The exits are done. So the $35 million was the Q2 impact."）
- 2026-08-03｜CEO Hassane El-Khoury｜customer：中國車用營收上半年成長 13%（原話："our automotive revenue increased 13% in the first half"）
- 2026-08-03｜CEO Hassane El-Khoury｜customer：擴大在 NVIDIA MGX 生態系角色（原話："We have expanded our role in the NVIDIA MGX ecosystem"）
- 2026-08-03｜CEO Hassane El-Khoury｜customer：取得 Great Wall 兩個電源平台設計案（原話："we secured 2 power supply platform wins with Great Wall"）
- 2026-08-03｜CEO Hassane El-Khoury｜customer：AWS 電源與備援電池設計案（原話："design wins supporting AWS power supply and battery backup"）
- 2026-08-03｜CEO Hassane El-Khoury｜customer：Rivian R2 平台內容（原話："some customers ordering out into '28, trying to lock up supp"）
- 2026-08-03｜CFO Thad Trent｜customer：部分客戶下單至 2028 年以鎖定供給（原話："we prioritized shipments to AI data center"）
- 2026-08-03｜CFO Thad Trent｜customer：AI 資料中心需求排擠車用與工業出貨（敘事新增）（原話："we prioritized shipments to AI data center over"）
- 2026-08-03｜CFO Thad Trent｜customer：通路庫存週數下降，大眾市場營收季增（原話："Rivian's R2 platform"）
- 2026-08-03｜CEO Hassane El-Khoury｜competition：管理層自稱為涵蓋完整 AI 電力樹的唯一美國寬頻功率半導體供應商（原話："the only broad-based U.S. power semiconductor supplier"）
- 2026-08-03｜CEO Hassane El-Khoury｜competition：管理層表示不做多供應商產品，因毛利不吸引（原話："you can imagine the margin is not as exciting"）
- 2026-08-03｜CFO Thad Trent｜competition：管理層拒絕與競爭對手比較稼動率（原話："I don't want to comment about our competitors."）
- 2026-08-03｜CEO Hassane El-Khoury｜product：800V DC 機櫃預期 2027 年底至 2028 年初開始放量（原話："end of '27, beginning of '28, give or take a quarter"）
- 2026-08-03｜CEO Hassane El-Khoury｜product：每機櫃含量高壓成長約 10 倍，中低壓約 5 至 6 倍（原話："one is going up 10x, one is going up like 5x to 6x"）
- 2026-08-03｜CEO Hassane El-Khoury｜product：AI 資料中心 TAM 以 2030 年為基準（原話："the number we're anchoring on is 2030."）
- 2026-08-03｜CEO Hassane El-Khoury｜risk：供應商成本上漲，管理層不預期 2027 年定價轉軟（原話："I'm not expecting a softer pricing environment in '27"）
- 2026-08-03｜CFO Thad Trent｜risk：前置時間由約 27 週拉長（原話："lead times stretched out from about 27 weeks to"）
- 2026-08-03｜CFO Thad Trent｜risk：簽單出貨比數季以來顯著高於 1（原話："book-to-bill ratio has been significantly above 1"）
- 2026-08-03｜CFO Thad Trent｜risk：營收仍有約 25% 至 30% 的成長空間才會碰到產能上限（原話："revenue is still 25%, 30% higher than the run rate today"）
- 2026-08-03｜CFO Thad Trent｜guidance：9 月 16 日將於紐約舉行分析師日（原話："Analyst Day in New York on September 16."）

### ON_Analyst_Investor_Day_ON_Semiconductor_Corporation_20260916.md
- 2026-09-16｜Thad Trent｜guidance：2030 長期營收成長率模型 12–14%，高於前一版模型（原話："you get to about a 12% to 14% growth rate for the company"）
- 2026-09-16｜Thad Trent｜guidance：前一版長期成長模型為 10–12%，本次上調，主因 AI 資料中心（原話："Previous model was 10% to 12%, so we're taking that up"）
- 2026-09-16｜Thad Trent｜guidance：以 2026 年 Street 共識為基礎，2030 年營收略低於 110 億美元（原話："just under $11 billion of revenue in 2030"）
- 2026-09-16｜Thad Trent｜guidance：數字口徑：模型的 2026 基期是 Street 共識，不是公司自己的預估（原話："It's not our estimates, it's actually your estimates."）
- 2026-09-16｜Thad Trent｜guidance：數字口徑：長期模型假設 SAAR 持平，SAAR 上升為額外順風（原話："we're assuming a 0 SAAR"）
- 2026-09-16｜Achyut Shah｜guidance：AI 資料中心 2030 年目標：長期成長至少高於市場 10 個百分點（原話："we are going to grow at least 10% above the market"）
- 2026-09-16｜Achyut Shah｜guidance：舉例：市場 CAGR 40% 時，AIDC 營收由 2026 年 5 億美元基期成長至 2030 年逾 25 億美元（原話："we will deliver over $2.5 billion of revenue just in 2030"）
- 2026-09-16｜Achyut Shah｜guidance：2026 年 AI 資料中心業務預計成長逾一倍（原話："more than double the AI data center part of our business"）
- 2026-09-16｜Achyut Shah｜guidance：對 2027 年 AI 資料中心業務再翻倍表示有能見度（原話："this business is going to double again"）
- 2026-09-16｜Sudhir Gopalswamy｜guidance：車用 2026–2030 年營收成長約 9%/年，假設 SAAR 持平（原話："we'll grow our automotive revenue at about 9% a year"）
- 2026-09-16｜Sudhir Gopalswamy｜guidance：工業市場長期成長目標 10%（原話："allow us to grow by 10% in the industrial market"）
- 2026-09-16｜Thad Trent｜guidance：自由現金流率目標由 25–30% 上調至 30–35%（原話："Our target is going to 30% to 35%."）
- 2026-09-16｜Thad Trent｜guidance：2026 年 Street 共識自由現金流約 16 億美元（原話："about $1.6 billion in free cash flow for 2026"）
- 2026-09-16｜Thad Trent｜guidance：Synaptics 獨立計畫：成長率高於 15%，毛利率高於 55%（原話："We're looking at margins higher than 55%"）
- 2026-09-16｜Thad Trent｜guidance：Synaptics 前 18 個月協同效益 2 億美元，已含股權報酬（原話："$200 million of synergies in this number"）
- 2026-09-16｜Thad Trent｜guidance：數字口徑：長期模型為 onsemi 獨立數字，不含 Synaptics；預期明年完成交易（原話："It has nothing to do with Synaptics."）
- 2026-09-16｜Thad Trent｜margin：毛利率目標維持 53%，未上調（原話："our target remains 53%"）
- 2026-09-16｜Thad Trent｜margin：管理層把 53% 定位為里程碑，達成後再談更高（原話："The 53% is a milestone. It's not a destination."）
- 2026-09-16｜Thad Trent｜margin：毛利率拆解：稼動率貢獻 650 bp（原話："you've got utilization, 650 basis points."）
- 2026-09-16｜Thad Trent｜margin：稼動率口徑：去年底 68%，2026 Q2 約 83%（原話："exited last year at 68%. We're roughly around 83% in Q2"）
- 2026-09-16｜Thad Trent｜margin：毛利率拆解：Fab Right 貢獻 225 bp，比以往說法更高，納入已宣布的出售（原話："On the Fab Right, 225 basis points."）
- 2026-09-16｜Thad Trent｜margin：Fab Right 225 bp 中已有 50 bp 確定，其餘約 18–24 個月內認列（原話："Now 50 of that is already in the bag."）
- 2026-09-16｜Thad Trent｜margin：營收成長 12–14% 搭配 53% 毛利率下，毛利金額成長 22%（原話："gross profit dollars are going to grow by 22%"）
- 2026-09-16｜Thad Trent｜margin：營業利益成長速度為營收的兩倍（原話："Operating income is going to grow 2x revenue."）
- 2026-09-16｜Thad Trent｜margin：2030 模型營業利益率 38%（原話："You get to an operating margin of 38%"）
- 2026-09-16｜Thad Trent｜margin：漲價進入第二輪，用來抵銷已發生的投入成本（原話："We're raising pricing with our customers"）
- 2026-09-16｜Thad Trent｜margin：投入成本逆風已先出現在毛利率，漲價效益尚未跟上（原話："headwind of the input cost hitting the margin line already"）
- 2026-09-16｜Thad Trent｜margin：答分析師：毛利率路徑建議以線性建模，市場快則可更快（原話："I would think about a pretty linear progression."）
- 2026-09-16｜Thad Trent｜margin：與歷史相比，現有晶圓廠成本結構在同稼動下低 17%（原話："the current cost structure is 17% lower"）
- 2026-09-16｜Thad Trent｜capital_allocation：資本支出強度維持約 5%，擴產在既有廠區內（原話："We can do this at about a 5% capital intensity."）
- 2026-09-16｜Thad Trent｜capital_allocation：2023–2026 買回 42 億美元股票，占自由現金流 92%（原話："we bought back $4.2 billion of shares while investing"）
- 2026-09-16｜Thad Trent｜capital_allocation：上述期間股數減少 12%（原話："we've reduced our share count by 12% during that time"）
- 2026-09-16｜Thad Trent｜capital_allocation：現有買回授權尚餘 53 億美元（原話："We've got $5.3 billion left on our existing authorization."）
- 2026-09-16｜Thad Trent｜capital_allocation：股東回饋計畫：扣除其他投資後，自由現金流 100% 回饋股東（原話："100% free cash flow back to shareholders"）
- 2026-09-16｜Thad Trent｜capital_allocation：過去 5 年投入 87 億美元，換得約 810 億美元 TAM 擴張（原話："$8.7 billion for an $81 billion TAM expansion"）
- 2026-09-16｜Thad Trent｜capital_allocation：約 65% 產品仍由外部代工，晶圓廠網路已整併（原話："we'll be manufacturing about 65% externally"）
- 2026-09-16｜Thad Trent｜commitment：承諾預測期間不再增加 brownfield 產能投資（原話："there won't be additional brownfield investment"）
- 2026-09-16｜Thad Trent｜commitment：9 億美元非核心業務退出已全部完成（原話："the exits are now done and behind us"）
- 2026-09-16｜Hassane El-Khoury｜commitment：EPP 量產無須增加資本支出，併入 5% 基線（原話："there is no incremental investment."）
- 2026-09-16｜Sudhir Gopalswamy｜commitment：車用 SiC 下一代將於約兩個月內發表，性能每代提升 25% 以上（原話："increase by 25% or even more by generation"）
- 2026-09-16｜Sudhir Gopalswamy｜commitment：管理層表示打算與客戶分享所創造的價值（原話："we intend to share that value that we create"）
- 2026-09-16｜Achyut Shah｜product：宣布今年贏得主要 Vcore 插槽，營收 2026 年底起認列（原話："we won a major Vcore socket this year"）
- 2026-09-16｜Achyut Shah｜product：每機櫃 onsemi 內容價值由約 1.5 萬美元提升至逾 11.5 萬美元（原話："about $15,000 a rack to over $115,000"）
- 2026-09-16｜Achyut Shah｜product：sidecar 架構 800V 機櫃預計約 12–18 個月內（2027 年底）開始放量（原話："start ramping in the next 12 to 18 months"）
- 2026-09-16｜Achyut Shah｜product：固態變壓器世代預計 2028 年底至 2029 年初開始（原話："sometime in the end of '28, early '29"）
- 2026-09-16｜Hassane El-Khoury｜product：車用乙太網路 10BASE-T1S 區域架構首個車用新客戶量產預計今年底開始（原話："ramp starting actually at the end of this year"）
- 2026-09-16｜Sudhir Gopalswamy｜product：車用每車 onsemi 內容機會最高 2,000 美元（原話："up to $2,000 of onsemi content per vehicle"）
- 2026-09-16｜Sudhir Gopalswamy｜product：實體 AI（不含車用）2030 年對公司 TAM 約 60 億美元（原話："represents a $6 billion TAM for us by 2030"）
- 2026-09-16｜Achyut Shah｜competition：AI 電力樹由格點到核心全覆蓋者只剩兩家（原話："left with just 2 companies onsemi and one more"）
- 2026-09-16｜Achyut Shah｜competition：高壓中段（SiC／GaN）具備規模的競爭者僅 3–4 家（原話："there's just a handful, 3 or 4 competitors"）
- 2026-09-16｜Hassane El-Khoury｜competition：管理層稱垂直 GaN 領先最接近的競爭者約五年（原話："half a decade ahead from the closest competitor"）
- 2026-09-16｜Hassane El-Khoury｜competition：管理層稱 EPP 的優勢是熱與機構面，不只是電氣面（原話："is not electrical. It's thermal and mechanical."）
- 2026-09-16｜Achyut Shah｜competition：管理層承認在 Vcore 較晚進入市場，稱已追上（原話："we came a little later to the market"）
- 2026-09-16｜Achyut Shah｜risk：800V 新架構轉換時程：管理層承認一直存在疑慮，稱與客戶有對應方案（原話："there is always a concern when it comes to a new market"）
- 2026-09-16｜Hassane El-Khoury｜risk：答分析師：800V 滲透不會一次到位，影響成長曲線時間（原話："The 800-volt is not going to go flip the switch"）
- 2026-09-16｜Thad Trent｜customer：無單一 10% 客戶，前 20 大客戶占營收 35%（原話："No 10% customer and our top 20 customers are 35% of revenue."）
- 2026-09-16｜Thad Trent｜customer：客戶總數約 9,000 家（原話："We have 9,000 customers around the globe."）
- 2026-09-16｜Achyut Shah｜customer：管理層稱與所有主要資料中心客戶深度綁定（原話："we are deeply embedded with all of these customers"）

### 問答異常語氣（迴避／改口／保留）
- ON_Q2_2026_Earnings_Call_20260803.md｜問：Quinn Bolton 追問 AI 資料中心營收是否明顯高於上季提到的 5 億美元｜答法：CEO 回答「I'll let you run the numbers」並表示不再進一步拆分，未給數字
- ON_Q2_2026_Earnings_Call_20260803.md｜問：Joe Moore 問稼動率與競爭對手相比及能否搶市占｜答法：CFO 表示不評論競爭對手，改談自身稼動率與彈性
- ON_Q2_2026_Earnings_Call_20260803.md｜問：Jim Schneider 問 2027 年供應商投入成本與定價把握度｜答法：CEO 只給方向（不會下降）與「有可見度」，未給幅度或數字
- ON_Analyst_Investor_Day_ON_Semiconductor_Corporation_20260916.md｜問：Vivek Arya (BofA)：AI 資料中心 2027 年約 10 億美元、2030 年 25 億美元以上，成長明顯減速，是保守嗎？｜答法：Achyut Shah 與 Hassane 皆未直接說明是否保守，改稱數字只反映分析師 4 年預估基線、會高於市場 10 個百分點，並指 800V 滲透需時間；未給 2030 年自家預測

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 5 | 2 |
| customer_second_source | found | 1 | 2 |
| customer_concentration_credit | found | 2 | 1 |
| supply_demand_durability | found | 4 | 2 |
| regulatory_antitrust | found | 3 | 2 |
| reg_tariff_export | found | 3 | 2 |
| geo_supply_chain | found | 5 | 2 |
| end_markets | found | 6 | 4 |
| substitute_technology | found | 4 | 2 |
| channel_business_model_shift | found | 1 | 1 |
| capital_markets_pricing | found | 5 | 4 |
| major_events | found | 4 | 3 |
| cyclical_supply_discipline_capacity | found | 5 | 3 |
| cyclical_inventory_price_position | found | 4 | 3 |
| cyclical_prior_downcycle_behavior | found | 3 | 2 |

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260620","verdict":"B 衛星候選/觀望（深度週期股剛Q1'26 inflect +5%YoY，股價自52W低$44.56已近3倍且跑過分析師均標$106；SiC#2+CIS#1+FCF韌性真實，但EV放緩是SiC結構逆風+Sony CIS競爭+估值🟠+MA🟡觀察池後谷底火箭極伸展；機率加權合理價$71/-42%下行不對稱；等大幅回檔$70-85+SiC/EV復甦確認，長期信心僅中）","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"週期谷底反轉確立 + SiC/汽車復甦（EV 放緩不致命）","columns":{"2Y 驗證點":"FY26-27 營收持續 YoY 正成長、SiC 回正","5Y 驗證點":"FY28-30 營收回 $8B+（前峰）、SiC 重拾成長","10Y 驗證點":"SiC 滲透 EV/工業長坡兌現","數字門檻":"FY27 營收 &gt; $7B","來源":"ON 法說 / SiC 市場報告","漂移觸發":"SiC 連 2 季 YoY 仍負 + PSG QoQ 轉負 → 反轉（2Y，QC-35）"}},{"id":"H2","text":"AI 資料中心電源成新引擎","columns":{"2Y 驗證點":"2026 資料中心營收翻倍（&gt;$500M）","5Y 驗證點":"FY28-30 資料中心成 ON 第三大支柱","10Y 驗證點":"AI 電源結構性需求持續","數字門檻":"2026 資料中心 &gt;$500M","來源":"ON Q1'26 guide（翻倍）","漂移觸發":"資料中心 QoQ 增速明顯放緩 → 削弱（2Y）"}},{"id":"H3","text":"fab-right → 結構性 margin 提升","columns":{"2Y 驗證點":"FY27 非 GAAP GM 回 42%+","5Y 驗證點":"FY30 GM 朝高 40%/50%（前峰 49%）","10Y 驗證點":"fab-right 成本結構固化","數字門檻":"FY27 非 GAAP GM ≥ 42%","來源":"ON 法說 / fab-right 進度","漂移觸發":"GM 連 4 季 &lt; 39% → 削弱（5Y）"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"EV 放緩使 SiC 復甦落空（結構性需求逆風）","columns":{"對應假設":"H1","時間尺度":"🔥 中期（4-6 季）","監測指標":"SiC/汽車營收 YoY、EV 銷量、PSG QoQ","警戒閾值":"SiC 連 2 季 YoY 負 + PSG QoQ 轉負 → 減倉"}},{"id":"R2","text":"Sony CIS 競爭侵蝕 ISG（汽車影像感測）","columns":{"對應假設":"—","時間尺度":"🔥 中期（4-6 季）","監測指標":"ISG 段營收、汽車 CIS 份額","警戒閾值":"ISG 連 2 季衰退 + 份額流失 → 重評"}},{"id":"R3","text":"股價已跑過共識 → 反轉行情退潮","columns":{"對應假設":"H1/估值","時間尺度":"⚡ 短期（1-2 季）","監測指標":"股價 vs 分析師均標 $106、動能","警戒閾值":"股價維持 &gt; 均標 20% + 動能轉弱 → 等回檔"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🟠","ma":"🟡","trap":"🟡","moat_trend":null,"runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":121.62,"archetype":null,"cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"ON","date":"2026-11-08","schema":"v15.0","contract":"v19","company_name":"onsemi"},"oneliner":"功率半導體復甦加上 AI 資料中心放量，現價以 16 倍計只要求 FY27 EPS 約 3.96 美元，比共識低 16%；但約 70 億美元的 Synaptics 併購財務條款未明，車用又連兩季讓路，先等併購槓桿的答案，不追價。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ON_20261108/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/ON_20261108/scenario.json","answers":{"q1_business":{"verdict":"賺汽車、工業和 AI 資料中心的電源與感測零件錢，利潤卡在稼動率和產品組合：Q3 非 GAAP 毛利率 41.2%，離 53% 目標還有 11.8 個百分點。","reasoning":"Q3 營收 17.22 億美元：車用 7.77 億（45%）、工業 4.67 億（27%）、其他 2.99 億（17%）、AI 資料中心 1.80 億（10%）；事業群為 PSG 8.90 億、AMG 5.97 億、ISG 2.35 億。Q3 非 GAAP 營益率 23.2%，GAAP 22.0%。產業時鐘判在擴張早段：2026-08-03 法說稱訂單出貨比明顯高於 1、交期拉長，漲價開始少量進損益；onsemi 自身稼動率 83%，仍低於 92%～93% 的滿載線，FY26 共識營收 66.1 億美元也低於 FY22 的 83.3 億。供需判為週期性偏緊、將會反轉：緊在部分矽製程產線與 AI 排擠，SiC 上游反而過剩。單點依賴：2026-09-16 投資人日 Thad Trent 稱沒有 10% 客戶、前 20 大占 35%；10-K 另揭露一家經銷商占 FY25 營收約 11%，經銷通路占 54%。分部毛利率事實表未涵蓋。","fact_refs":["f_kpi0_gaap","f_kpi2_non_gaap","f_kpi4_gaap","f_kpi8_cogs_91","f_rev_consensus_fy1_m"],"verdict_values":{"revenue_quality":"設計案帶來的重複性零件營收，週期性高；AI 資料中心與工業目前是終端裝機需求，車用補庫存被延後。","unit_econ_note":"每多 1 點稼動率約增 25～30 基點毛利率，約落後兩季反映；Q3 低稼動費用約 450 基點（2026-11-02 法說，Thad Trent）。","archetype":{"primary":"循環/商品","secondary":null,"confidence":"中","fingerprint":"FY22 到 FY25 營收由 83.3 億跌到 60.0 億美元，毛利率由 49.0% 跌到 33.1%，沒有虧損年，資本支出僅占營收 2%～5%，屬需求量循環而非商品價格循環；AI 資料中心另算結構成長。"},"industry":{"clock_phase":"II","sd_verdict_source":"週期性偏緊、將會反轉：Wolfe 的 Chris Caso 認為 2028 前難見全面過剩（2026-07-30，泛半導體），8 吋代工 2026 上半年漲 5%～15%；反方是 SiC 上游稼動率約 50%，中國成熟製程新產能可能使部分品類交期正常化。","bargaining":{"up":"8 吋代工與投入成本上漲，約 65% 產品外部製造（2026-09-16 投資人日），上游目前較強。","down":"車用 OEM 與超大型雲端客戶議價力強；客戶約 9,000 家但經銷占 54%，漲價目前只用來抵銷投入成本。","geo":"中國約占營收 30%（二手來源），樂山封測廠持股 80%，商務部反傾銷調查未結。"},"profit_pool_dir":"利潤池由車用 SiC 往 AI 電源移動；五年占比事實表未涵蓋。","tam_table":{"expanded":false,"reason":"事實表只有管理層口徑的 2030 年 TAM 與 SiC 單點滲透率，沒有五年前基期和利潤池占比，展開只會轉抄公司說法。"}}}},"q2_moat":{"verdict":"護城河方向穩定：AI 電源在擴大，SiC 定價在縮減，毛利率仍比類比同業低約 20 個百分點。","reasoning":"機制是車規認證與長生命週期設計案，加上低壓到高壓的完整電源產品線，AI 資料中心再加系統級方案。ROIC 差距因投入資本缺資料算不出，改用同業利潤率差距。TTM GAAP 毛利率 38.68%，比 TXN 低 21.6 個百分點、比 NXPI 低 17.8、比 MCHP 低 21.5、比 STM 高 4.8；營益率 19.12%，低於 TXN 的 41.12% 與 NXPI 的 28.55%，高於 MCHP 與 STM；FCF 率 25.38%，僅低於 TXN。SiC 份額 55%～60% 是公司自述，沒有第三方驗證。可能看錯的地方：若車用讓路實際造成份額流失，方向應改為 ↓。","fact_refs":["f_peer_on_gross_margin_pct","f_peer_txn_gross_margin_pct","f_peer_nxpi_gross_margin_pct","f_peer_mchp_gross_margin_pct","f_peer_stm_gross_margin_pct","f_peer_on_operating_margin_pct","f_peer_txn_operating_margin_pct","f_peer_nxpi_operating_margin_pct","f_peer_on_fcf_margin_pct","f_peer_txn_fcf_margin_pct","f_peer_nxpi_fcf_margin_pct","f_peer_mchp_fcf_margin_pct","f_peer_stm_fcf_margin_pct"],"verdict_values":{"moat":{"mechanism":"車規認證與長設計週期，加上從高壓到低壓的完整電源產品線；AI 資料中心再以系統級方案和功率密度競爭。","execution":7,"pricing":5,"grade":"C","trend":"→","trend_evidence":"執行面擴大：2026 年 AI 資料中心約 6.2 億美元，年增 140%，非 GAAP 毛利率連升五季，Google 等平台開始量產出貨。定價力在 SiC 縮減、矽與類比穩定，漲價僅抵銷成本。車用份額沒有第三方正反證據。","competitor_notes":[{"name":"TXN","strategy_note":"毛利率 60.24%、營益率 41.12%，是類比獲利標竿；2026 資本支出降到 20～30 億美元，供給紀律有利同業定價。"},{"name":"NXPI","strategy_note":"毛利率 56.43%，車用與工業競爭者；FCF 率 24.16%，略低於 onsemi，表示 onsemi 的現金轉換不輸，但毛利率差距大。"},{"name":"MCHP","strategy_note":"毛利率 60.19%、營益率僅 16.23%，資料截至 2026-06；稱庫存去化接近尾聲，是循環回升的旁證。"},{"name":"STM","strategy_note":"毛利率 33.84%、FCF 率 3.22%，是 SiC 與車用直接對手，獲利明顯弱於 onsemi。"},{"name":"中國 SiC 廠","strategy_note":"SICC 與天科合達合占 2025 年 N 型基板銷售約 41.6%，以低價壓縮 SiC 利潤，是最實際的定價威脅。"},{"name":"Sony","strategy_note":"車用影像感測競爭者；Q3 ISG 年增僅 2%，低於公司整體 11%，份額數字事實表未涵蓋。"}],"spread_notes":null,"peer_na_reason":"事實表只有同業利潤率，沒有投入資本，算不出 ROIC 差距，改用毛利率、營益率與 FCF 率差距。","threats":[{"level":"🔴","text":"中國低價 SiC 與產能過剩壓低價格，onsemi 捷克廠 2025 年裁約 170 人後，2026-06 再傳裁 200～300 人。","p":45,"evidence_refs":["competitive_share_entrants#3","geo_supply_chain#2","geo_supply_chain#4","substitute_technology#2","cyclical_supply_discipline_capacity#3","cyclical_supply_discipline_capacity#4"]},{"level":"🟡","text":"AI 電源份額未必如預期，管理層也承認 Vcore 進場較晚；每代架構都會重開插槽。","p":30,"evidence_refs":["competitive_share_entrants#1"]},{"level":"🟡","text":"對手取得政府補貼，中國成熟製程新產能可能使部分品類交期正常化。","p":30,"evidence_refs":["competitive_share_entrants#2","supply_demand_durability#2"]},{"level":"🟡","text":"10-K 的技術替代與產品過時風險屬通用揭露；目前 800V 牽引逆變器仍全用 SiC，垂直 GaN 則是 onsemi 自有路線。","p":20,"evidence_refs":["substitute_technology#0","substitute_technology#1"]}],"roic_durability":{"quadrant":"暫判低利益率×低周轉：TTM GAAP 營益率 19.12%，存貨約 186 天；投入資本事實表未涵蓋，周轉率無法計算。","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"客戶要解決的是功率密度和電氣化，AI 機櫃的 onsemi 內容由約 1.5 萬美元升到 11.5 萬美元以上（2026-09-16 投資人日，公司說法），延後代價高。公司解法能否勝出放在下一項判斷。"},{"item":"決策層級","level":"🟡","text":"替代性要看單一插槽：車規設計案認證長，2026-08-03 法說稱部分客戶下單到 2028；但 AI 電源每代架構都重開插槽。漲價後流失率與重新認證週期事實表未涵蓋。"},{"item":"價值鏈分配","level":"🟡","text":"最難取代的環節是 GPU 與雲端平台，onsemi 在零件層。漲價目前只抵銷投入成本，管理層也表示要與客戶分享創造的價值，毛利率低於類比同業約 20 個百分點。"},{"item":"社會容忍度","level":"🟡","text":"終端消費者不直接面對這筆成本，限制來自政策：中國反傾銷調查、美中出口管制與各國補貼；onsemi 捷克項目本身也獲歐盟核准 4.5 億歐元補助。"}],"roiic":"事實表未涵蓋投入資本，算不出數字。FY22 到 FY25 營業利益由約 27.6 億降到約 7.5 億美元，歷史增量報酬為負，但這段跨下行循環且含減損，不能外推。","reinvest_rate":"折舊與營運資金事實表未涵蓋，只能算收購項：Ferric 與 Synaptics 合計約 76 億美元，約為近四季稅後營業利益 10 億美元的 7.5 倍。","endo_ceiling":null,"formula_note":"內生成長率需要增量 ROIC 與完整再投資率，兩者輸入不足，留空，不用推估值代替。"}}}},"q3_growth":{"verdict":"五年後仍有成長空間：AI 電源是第二條曲線，SiC 滲透率約 17%；但共識成長主要靠毛利率回升，不是靠再投資。","reasoning":"成長來源：2027 年以量為主，價格只抵銷成本，併購外加，回購暫停。共識營收 FY26 到 FY27 增 14.9%（66.07 億到 75.94 億美元，28 位分析師）；共識 EPS FY26 到 FY28 年化 36.1%（3.28 到 6.08）。以 FY25 GAAP 0.29 為基期的三年 CAGR 約 176%，基期含減損，沒有參考價值。管理層 2027 年框架（AI 翻倍約增 6.2 億、車用 9%、工業 10%，後兩項以 Q3 年化估）合計約增 10.9 億，略高於共識的 9.9 億，所以營收不是爭點，毛利率才是。FY27 共識隱含毛利率約 44.5%～45%（4.71×3.92 億股÷0.85，扣其他收益約 1 億，營業費用假設 13.0～13.4 億）；Q4 指引中點 42.5%，且 Q3、Q4 稼動率都是 83%，按落後兩季計 2027 上半年沒有稼動率推升。因此 Base 的 FY27、FY28 EPS 為 4.45、5.55，各低於共識 5.5%、8.7%。反例：若新品組合與漲價提前進損益，共識就站得住。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m"],"verdict_values":{"growth":{"driver_mix":"量為主；價格抵銷成本；毛利率擴張貢獻 EPS 的大部分增幅；併購外加且未納入公司長期模型；回購在併購完成後讓位給去槓桿。","runway_years":"SiC 目前約占電動車牽引逆變器 17.2%（2026 Q1），年增速事實表未涵蓋，無法推算到 30% 所需年數。","runway_post_y5":"🟢","endo_ceiling_basis":"內生上限算不出：投入資本、折舊與營運資金事實表未涵蓋。2027 年資本支出約占營收 5%，管理層稱預測期間不再增加 brownfield，有機再投資很低，共識年化 36.1% 的主要來源是毛利率擴張，歸因明確。情境樹按超過內生上限處理。","segments":[{"item":"車用","value":"Q3 7.77 億美元，季減 1%、年減 1%；Q4 指引減高個位數；管理層 2027 年回到約 9% 成長。"},{"item":"工業","value":"Q3 4.67 億美元，季增 10%、年增 9%；Q4 指引增低雙位數，主因電網與能源基建。"},{"item":"AI 資料中心","value":"Q3 1.80 億美元，季增 39%、年增 175%；2026 年約 6.2 億，2027 年預期翻倍；2030 年目標 30 億以上，其中 5 億來自 Ferric。"},{"item":"其他","value":"Q3 2.99 億美元，Q4 增高十位數來自外部製造的大客戶專案，2027 年不延續此增速。"}],"decay_signals":["EPS 成長高於營收成長：FY26 到 FY28 EPS 年化 36.1%，FY27 營收增 14.9%，差距超過 5 個百分點；成立，來自谷底回升。","停止擴產且營收三年內下滑：FY23 到 FY25 營收連三年下滑，2026 資本支出約占營收 2%；成立，但營收已轉正。","產業估值倍數三年趨勢：事實表未涵蓋，不計入。","核心市占：管理層稱未流失，第三方份額資料事實表未涵蓋，不計入。"],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"現金創造強，但資金用途正從回購轉向舉債併購，資本配置成績要等 Synaptics 與 Ferric 的實際報酬。","reasoning":"Q3 自由現金流 4.886 億美元，占營收 28%，對 GAAP 淨利 3.14 億的轉換率 1.56 倍；TTM FCF 率 25.38%。Q3 資本支出只占營收 1.6%，2027 年回到約 5%，同樣條件下 FCF 率約少 3.4 個百分點。淨負債 3.4 億美元，Ferric 付現 6 億後約 9.4 億；若 Synaptics 約 70 億全數現金，淨負債約 79 億，是近四季 FCF 約 16 億的 4.9 倍，修訂條款事實表未涵蓋。SBC 約占營收 2.2%。近三年現金去向四分與債務到期結構事實表未涵蓋。","fact_refs":["f_kpi5_fcf","f_kpi6_sbc_gaap","f_net_debt_m","f_shares_diluted_m","f_peer_on_fcf_margin_pct"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":true,"passed":null,"input":"Synaptics、Ferric 尚未完成，沒有已實現報酬；歷史併購報酬事實表未涵蓋。"},{"name":"buyback_yield","applicable":true,"passed":null,"input":"2023～2026 回購 42 億美元、股數淨減 12%，推得均價上限約 79 美元；近四季每股 FCF 約 4.15 美元，收益率至少約 5.3%。10 年期公債殖利率事實表未涵蓋，無法比較。"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"Q3 SBC 占 GAAP 營業利益 9.8%，約 3,700 萬美元，年化約 1.5 億美元，約占市值 0.6%，低於 1.5%；2023～2026 股數淨減 12%。"}]},"governance":{"capital_returns":[{"item":"2023～2026 回購","value":"42 億美元，占 FCF 92%，股數減 12%；剩餘授權 53 億美元（2026-09-16 投資人日）。"},{"item":"2026 Q2 回購","value":"3.32 億美元。"},{"item":"2026 Q3 回購","value":"2,000 萬美元，受 Synaptics 交易限制。"},{"item":"併購後順位","value":"先投資業務，再快速去槓桿，回購改為伺機（2026-11-02 法說，Thad Trent）。"}]}}},"q5_valuation":{"verdict":"現價只要求 FY27 EPS 約 3.96 美元配 16 倍，我相信營運面做得到，但併購後的每股分母還不能確認，便宜的說法暫時不成立。","reasoning":"以 16 倍反推，現價 63.31 只要求 FY27 EPS 約 3.96 美元，比共識 4.71 低 16%。Q3、Q4 指引都高於季節性，即使 FY27 毛利率只到 43%，EPS 仍約 4.4 美元。不確定的是分母：賣方是否納入 Synaptics 事實表未涵蓋，公司長期模型明確不含。各倍數分歧：Trailing P/E 37.02 倍（分母含減損費用）、FY1 19.3 倍、FY2 13.4 倍；P/S 3.87 倍與 EV/S 3.92 倍位於四個年度端點的 69 與 65 百分位。賣方均標 89～113 美元，比現價高 41%～79%，但三個來源日期不一且早於 11-02 財報，只作對照。真正的五年分位事實表未涵蓋，留空。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_pe_current","f_pe_percentile","f_ps_current","f_ps_percentile","f_ev_s_current","f_ev_s_percentile","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_3m_fy1_pct"],"verdict_values":{"valuation":{"basis":"Fwd P/E 與 PEG，分母為 FY2026E 共識 EPS，並對照 FY2027E。同業現值倍數事實表未涵蓋，終端倍數以自身 FY1 19.3 倍與 FY2 13.4 倍對照。","peers":{"expanded":false,"reason":"事實表只有同業利潤率，沒有同業前瞻本益比，無法做倍數對照；同業判讀放在護城河題。"},"fwd_pe":19.3,"peg":0.53,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"63.31÷3.28＝19.3 倍；63.31÷4.71＝13.4 倍；PEG＝19.3÷36.1＝0.53。數字偏低，但銷售倍數在年度端點 65～69 百分位，且 FY27 毛利率和併購後股數都是爭點，因此只判合理，不判便宜。","upside_short_pct":19.5,"upside_mid_pct":40.3,"denominator_disputed":true,"denominator_note":"短期上檔＝FY27 Base EPS 4.45×17 倍，中期上檔＝FY28 Base EPS 5.55×16 倍。FY27 共識隱含毛利率約 44.5%～45%，高於 Q4 指引中點 42.5%；Synaptics 的舉債與發股也可能改變每股分母，修訂條款未收錄。"}}},"q6_how_wrong":{"verdict":"最可能看錯的不是營運，而是併購把資本結構改掉；其次是車用暫時下滑的說法與循環反轉。","reasoning":"以 FY31 Base EPS 7.80 計，毛利率每 100 基點約 0.24 美元（110 億美元×1%×0.85÷3.92 億股），對應終端價約 3.8 美元；新債每 10 億美元按假設利率 6% 約減 0.13 美元；若高槓桿使終端倍數由 16 倍降到 12 倍，終端價少約 31 美元。股價低於 52、104、250 週均線，RSI 34.16，26 週跌 38.65%；下跌原因事實表沒有拆解，時間上與 6 月 25 日簽約重疊，但沒有事件日股價，不能歸因。循環位置判早循環：訂單出貨比大於 1、通路庫存 9.9 週且下降、情緒悲觀偏向買，倍數訊號分歧，AI 資本支出位置事實表未直接涵蓋。P/B 事實表未涵蓋，反動能五項檢查無法全數確認。AI 資料中心屬結構成長，不隨循環賣。管理層有四題未正面回答：AI 營收拆分、與對手比較稼動率、2027 投入成本與定價幅度、AI 目標是否保守。","fact_refs":["f_week26_return_pct","f_rsi14","f_ma_state","f_ma_w52","f_ma_w104","f_ma_w250","f_net_debt_m"],"verdict_values":{"trap":{"verdict":"🟡","label":"循環復甦進行中，不是價值陷阱；但便宜程度取決於併購後的每股分母"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":3.28,"pe":19.3,"basis":"FY1（FY2026E）共識 EPS 3.28，現價 63.31；終端倍數同樣用當年度 EPS"},"eps":{"bull":[4.95,6.7,8.1,9.4,10.5],"base":[4.45,5.55,6.4,7.15,7.8],"bear":[3.7,3.9,3.2,3.5,3.8]},"pe":{"bull":20,"base":16,"bear":12},"p":{"bull":20,"base":47,"bear":33},"yield_pct":{"dividend":0,"net_buyback":0},"second_stage":{"bull_cagr_pct":12,"base_cagr_pct":8},"max_dd":{"lo":-55,"hi":-30,"basis":"上輪由 108.09（2023-07）跌到 31.04（2025 年報價區間低點），跌 71%；本輪由前份研究時的 121.62 跌到 63.31，跌 48%；SOX 2004～2026 七次完成的回落為 −25%～−69%。從現價回到前份所記 52 週低 44.56 是 −30%，回到 31.04 是 −51%，再加併購槓桿緩衝得 −30%～−55%。","trigger_time":null},"basis":{"bull":"AI 資料中心 2030 年達 30 億美元以上，毛利率 2030 年到 53%，Synaptics 綜效兌現且槓桿快速下降；終端 20 倍，接近現行 FY1 倍數。同業現值倍數事實表未涵蓋。","base":"營收年化約 11%，FY31 約 110 億美元，毛利率約 50%，低於管理層 2030 年 53%；併購對 EPS 約中性（條款未知）；終端 16 倍，低於 FY1 的 19.3 倍、高於 FY2 的 13.4 倍。股數假設大致不變，淨回購填 0 以免重複計算。","bear":"機率 33% 的依據：共識成長超過內生上限、併購槓桿未明、SiC 過剩與中國風險並存，上輪股價跌 71%；2028 前難過剩的看法只涵蓋泛半導體，不涵蓋 SiC 與併購。路徑：高槓桿完成併購，2029 循環下行，FY31 EPS 3.80；成長降到 15%／10%／5% 時倍數假設為 15／12／9 倍，取 10% 對應的 12 倍。"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"上輪下行股價由 108.09 跌到 31.04，降價與低稼動使單季非 GAAP 毛利率落到 37.6%；SOX 歷次回落最深 −82%；Synaptics 約占現市值 28%，且可能面臨中國嚴格審查。","assumption":"假設 2027 年起需求續強，併購不會把資本結構壓垮。","consequence":"五年後虧 50% 的最可能路徑：高槓桿完成併購後循環在 2028～2029 反轉，AI 資本支出放緩，SiC 價格戰延續，EPS 停在 3 美元附近，配 10～12 倍，股價 30～40 美元。","ruling":"採納，併入 Bear 33%。與 Single Thing 部分重疊：併購是起點，循環反轉是放大器，所以另設庫存與通路條件。","watch":"併購後淨負債、通路庫存週數、存貨與營收增速差、AI 資料中心季增率。","evidence_refs":["cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#1","regulatory_antitrust#1"],"fact_refs":["f_net_debt_m","f_ev_m","f_week26_return_pct"]},{"view":"論點成功但股東經濟變差","evidence":"AI 資料中心 2027 年預期翻倍，但 Ferric 付現 6 億美元加最多 1.75 億業績獎金，Synaptics 約 70 億；Q3 回購降到 2,000 萬美元，2025-11 又核准 2～3 億美元減損與加速折舊；2030 目標上調的 5 億全來自收購。","assumption":"假設營收與毛利率成功會等比例轉成每股自由現金流。","consequence":"營收與毛利率達標，每股價值卻被併購溢價、利息和新股吃掉；投資人日的 100% 自由現金流回饋在併購後不成立。","ruling":"部分採納。有機部分的資本效率仍佳，資本支出僅 5%；但在併購報酬出現前，不把管理層 30%～35% 的 FCF 目標算進每股價值。","watch":"每股自由現金流、GAAP 與 non-GAAP EPS 差距、併購後回購金額。","evidence_refs":["major_events#3","major_events#0","major_events#1"],"fact_refs":["f_kpi5_fcf","f_shares_diluted_m"]},{"view":"價格已反映太多","evidence":"股價大跌後，P/S 3.87 倍、EV/S 3.92 倍仍在四個年度端點的 69、65 百分位；Trailing P/E 37.02 倍；FY27 共識隱含毛利率約 44.5%～45%。","assumption":"低本益比的結論依賴 FY27 EPS 4.71 能達成。","consequence":"若共識高估，現在看到的 13.4 倍其實不便宜。","ruling":"反駁。即使 FY27 毛利率只有 43%，EPS 仍約 4.4 美元，現價約 14 倍；銷售倍數高是因毛利率仍在谷底回升。真正要防的是併購改變分母，不是營運預期太滿。","watch":"2027 Q1、Q2 非 GAAP 毛利率與共識 FY27 EPS 修正。","evidence_refs":[],"fact_refs":["f_ps_current","f_ps_percentile","f_ev_s_current","f_ev_s_percentile","f_pe_current","f_consensus_eps_fy2"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 🟡 → 本次 ❌","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=🟡","side_b":"本次 ma=❌","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 121.62 → 本次 63.31（-47.9%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=121.62","side_b":"本次 price_at_dd=63.31","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 121.62 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 121.62 美元：五年期望值 前份未列，基準年化 前份未列，前份未列不對稱比","side_b":"本次情境、股價仍用 121.62 美元：Bull 價 210、Bear 價 45.6，五年期望值 −4.9%，基準年化 0.5%，不對稱比 0.7","ruling":"先換情境、股價不動：五年期望值與基準年化前份未列，無法比較。前份未列不對稱比，本次為 0.7。Bull、Bear 價位與股價無關，只受情境影響。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 121.62 美元：五年期望值 −4.9%，基準年化 0.5%，不對稱比 0.7","side_b":"本次情境、股價 63.31 美元：五年期望值 +82.8%，基準年化 14.5%，不對稱比 5.02","ruling":"再換股價、情境不動：起點價下跌 47.9%，五年期望值多 87.6 個百分點，基準年化多 14.0 個百分點，不對稱比由 0.7 升到 5.02。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"估值結論","cause":"價格變動","prior_field":["val"],"side_a":"前份：股價 121.62，估值偏貴（🟠），機率加權合理價 71 美元。","side_b":"本次：股價 63.31，FY1 19.3 倍、FY2 13.4 倍，估值轉為合理（🟡），但分母有爭議。","ruling":"改變主要來自股價下跌 48%，FY1 共識近三個月僅上修 2.5%。","evidence_level":"事實表","settle_metric":"FY27 共識 EPS 與併購後股數","if_then":[],"evidence_refs":[]},{"axis":"評級與陷阱風險","cause":"新證據","prior_field":["signal","trap"],"side_a":"前份：評級 B、陷阱風險 🟡，理由是估值過高，要等回檔到 70～85 美元且 SiC／EV 復甦確認。","side_b":"本次：評級 B、陷阱風險 🟡，價格條件已過，新限制是前份之後才簽的 Synaptics 併購。","ruling":"結果相同但理由換了：貴的問題解除，資本結構的問題出現。","evidence_level":"一手文件（8-K）","settle_metric":"合併文件揭露的融資結構","if_then":[],"evidence_refs":["major_events#0"]},{"axis":"前份空白欄位補齊","cause":"方法變動","prior_field":["moat_trend","runway_post_y5","archetype","cycle_position","p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份這幾欄為空，沒有護城河方向、五年後成長空間、公司類型、循環位置、情境機率與最大回撤。","side_b":"本次補上：護城河方向 →、五年後成長空間 🟢、循環／商品類、早循環、機率 20／47／33、最大回撤 −30%～−55%。","ruling":"這是欄位補齊，不代表基本面由無到有的變化。","evidence_level":"判斷","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"Single Thing 由無到有","cause":"新證據","prior_field":["single_thing"],"side_a":"前份未設唯一致命點，Single Thing 欄為空。","side_b":"Synaptics 併購以高槓桿完成：合併文件或完成後首份財報顯示淨負債高於近四季自由現金流 4 倍，或新發股數超過現有流通股 15%。","ruling":"協議在 2026-06-25 簽訂，晚於前份的 06-20，因此新增。","evidence_level":"一手文件（8-K）加二手估值","settle_metric":"淨負債÷近四季自由現金流；新發股數÷流通股","if_then":["若兩項都未超標或交易終止，重跑完整研究；若超標，已持有者減碼一半，未持有者不進場。"],"evidence_refs":["major_events#0","regulatory_antitrust#1"]},{"axis":"重新進場、減碼與清倉門檻","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"前份未設重新進場條件，也沒有清倉或減碼的數字清單；只寫等回檔到 70～85 美元且 SiC／EV 復甦確認。","side_b":"本次：合併文件顯示完成後淨負債不高於近四季自由現金流 4 倍且新發股數低於 15%才重跑研究；車用 2027 Q1 低於 7.4 億美元減碼一半；併購槓桿與車用同時失守則清倉。","ruling":"價格條件已過，等待對象改為併購條款，因此改用事件條件。","evidence_level":"一手文件與法說","settle_metric":"合併文件融資結構；2027 Q1 車用營收","if_then":["若併購槓桿與車用同時失守，清倉。"],"evidence_refs":["major_events#0","end_markets#0"]},{"axis":"前份假設與風險門檻對帳","cause":"新證據","prior_field":["thesis.H","thesis.R"],"side_a":"前份：FY27 營收高於 70 億美元；2026 資料中心高於 5 億美元；FY27 非 GAAP 毛利率不低於 42%；SiC 連 2 季年減加 PSG 季減則減倉；ISG 連 2 季衰退加份額流失則重評；股價高於均標 20% 加動能轉弱則等回檔。","side_b":"本次：FY27 營收不低於 74 億美元；2027 AI 資料中心不低於 11 億美元；FY27 毛利率不低於 43.5%；SiC／PSG 與 ISG 兩項保留；股價高於均標 20% 一項退休。","ruling":"2026 資料中心預期已達 6.2 億美元，Q4 毛利率指引中點 42.5%，舊門檻已過或將過，所以上調。現價低於各家均標 41%～79%，高於均標的條件不成立，退休。SiC 全年營收與份額事實表未涵蓋，標資料缺口。","evidence_level":"法說與事實表","settle_metric":"各假設對應的季報數字","if_then":[],"evidence_refs":[]},{"axis":"車用下滑是供給調配還是份額流失","cause":null,"prior_field":null,"side_a":"Hassane El-Khoury（2026-11-02）：短期、供給驅動，沒有流失份額，終端需求全數支援，2027 Q1 恢復，全年回到長期目標。","side_b":"Thad Trent（2026-08-03）原本指引 Q3 車用小增，實際季減 1%、年減 1%，Q4 再減高個位數；被延後的正是 OEM 為防缺貨而下的補庫存單。","ruling":"可調和，程度差異。暫採管理層說法但標為未證，預設期限：2027 Q1 車用低於 7.4 億美元，暫時性歸因即告失效。","evidence_level":"管理層說法，無第三方份額","settle_metric":"2027 Q1 車用營收","if_then":["若 2027 Q1 車用不低於 7.8 億美元，維持 H3。","若低於 7.4 億美元，已持有者減碼一半，未持有者不進場。"],"evidence_refs":["end_markets#0"]},{"axis":"2027 毛利率節奏","cause":null,"prior_field":null,"side_a":"Thad Trent（2026-11-02）：2027 年全年毛利率持續擴張。","side_b":"同一場法說：稼動率落後兩季反映，Q3、Q4 都是 83%，代表 2027 上半年損益沒有稼動率推升，只能靠新品組合、漲價和 Fab Right，後兩項效益多在 2027 年後段與 2028 年。","ruling":"可調和。方向採管理層，節奏採保守，所以 Base 的 FY27 低於共識 5.5%。","evidence_level":"法說原文推導","settle_metric":"2027 Q1、Q2 非 GAAP 毛利率","if_then":["若 2027 Q2 毛利率不低於 43%，Base 上調至共識。","若連 2 季低於 42%，已持有者減碼一半。"],"evidence_refs":[]},{"axis":"2030 年 AI 資料中心目標","cause":null,"prior_field":null,"side_a":"管理層把 2030 年目標上調到 30 億美元以上。","side_b":"Hassane El-Khoury 答 Wells Fargo 時說上調的 5 億全來自收購。2026 基期已由 5 億升到 6.2 億，2027 年翻倍約 12.4 億，有機 25 億隱含 2027～2030 年化僅 26%；投資人日被 BofA 問是否保守時也未正面回答。","ruling":"不可裁決至 2028 年。可能是保守，也可能反映 800V 時程和競爭；Base 用 2030 年約 28 億美元。","evidence_level":"法說原文","settle_metric":"2027、2028 年 AI 資料中心營收","if_then":["若 2027 全年高於 14 億美元，Bull 機率上調到 25%。","若低於 10 億美元，停止加碼。"],"evidence_refs":["competitive_share_entrants#4","end_markets#1"]},{"axis":"自由現金流用途","cause":null,"prior_field":null,"side_a":"Thad Trent（2026-09-16 投資人日）：扣除其他投資後 100% 自由現金流回饋股東，模型不含 Synaptics。","side_b":"Thad Trent（2026-11-02）：Synaptics 完成後去槓桿是首要任務，回購伺機；Q3 回購僅 2,000 萬美元。","ruling":"不算改口，但獨立模型不是股東實際會拿到的結果，應以併購後框架為準。","evidence_level":"法說原文","settle_metric":"併購後季度回購金額與淨負債","if_then":[],"evidence_refs":["ma_merger#0"]},{"axis":"客戶集中度口徑","cause":null,"prior_field":null,"side_a":"投資人日：沒有 10% 客戶，前 20 大占 35%。","side_b":"10-K：一家經銷商占 FY25 營收約 11%。","ruling":"可調和，前者應為終端客戶口徑，後者為經銷商；本包沒有原文證實。","evidence_level":"公司文件","settle_metric":"下一份 10-K 客戶揭露","if_then":[],"evidence_refs":["customer_concentration_credit#0"]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"FY27 僅 13.4 倍，FCF 殖利率約 6.6%，Q3 與 Q4 指引優於季節性，FY1 共識三個月上修 2.5%，賣方均標高於現價 41%～79%，價格也低於前份設定的 70～85 美元。","side_b":"併購條款未讀到，股價低於 250 週均線 69.17 美元，車用暫時性尚未驗證；Ferric 與修訂協議都不到一季，是否進入賣方模型未知。","ruling":"觀望，唯一限制是併購財務條款。條款已在 2026-10-01 的 8-K，只是本包未收錄，補讀後可立刻裁決，不必等到完成日。","evidence_level":"事實表與資料缺口","settle_metric":"合併文件的現金股票比例與融資安排","if_then":["若股價先站回 69.17 美元但併購條款未確認，不追。","若條款達標且 Q4 毛利率不低於 42%，股價卻跌破 55 美元，分批反買到 1.5%，2027 Q1 車用確認後加到 3%。","反向條件：若淨負債高於近四季自由現金流 4 倍，已持有者減碼一半；若車用同時低於 7.4 億美元，清倉。"],"evidence_refs":["major_events#0","capital_markets_pricing#1"]},{"axis":"產業態勢三軸","cause":null,"prior_field":null,"side_a":"競爭惡化：中國低價 SiC 與上游過剩；結構轉好：AI 電源需求，IDM 資本支出 2026 年再降 9%，TI 資本支出下降。","side_b":"其他結構變數：中國反傾銷調查未結，Section 232 關稅範圍狹窄，併購改變公司結構，經銷占比升到 54%。","ruling":"雙向拉鋸：矽功率與類比轉好，SiC 惡化，中國政策未定。","evidence_level":"一手文件與產業媒體","settle_metric":"SiC 定價、AI 資料中心營收、反傾銷裁定","if_then":[],"evidence_refs":["cyclical_supply_discipline_capacity#1","cyclical_supply_discipline_capacity#0","reg_tariff_export#2"]}],"triggers":[{"n":1,"text":"併購高槓桿完成","type":"Single Thing","maps_to":"R1","metric":"淨負債÷近四季自由現金流；新發股數÷流通股","threshold":"高於 4 倍，或新發股數高於 15%","action":"已持有者減碼一半，未持有者不進場","source_freq":"8-K、合併文件、10-Q，事件驅動","date":"2027-06","evidence_refs":["regulatory_antitrust#1"]},{"n":2,"text":"併購條款達標後才重跑研究","type":"估值rearm","maps_to":"R1","metric":"同上","threshold":"不高於 4 倍且低於 15%，或交易終止","action":"重跑完整研究，通過後首筆 1.5%","source_freq":"合併文件，事件驅動","date":"2026-12","evidence_refs":["major_events#0"]},{"n":3,"text":"車用暫時性驗證","type":"假設驗證","maps_to":"H3","metric":"車用季營收","threshold":"不低於 7.8 億美元為確認，低於 7.4 億美元為否證","action":"確認則加到 3%；否證則減碼一半","source_freq":"季報","date":"2027-05","evidence_refs":["end_markets#0"]},{"n":4,"text":"毛利率節奏驗證","type":"假設驗證","maps_to":"H2","metric":"非 GAAP 毛利率","threshold":"2027 Q2 不低於 43%","action":"未達則停止加碼","source_freq":"季報","date":"2027-08","evidence_refs":[]},{"n":5,"text":"AI 資料中心放量驗證","type":"假設驗證","maps_to":"H1","metric":"AI 資料中心營收","threshold":"2027 Q1 不低於 2.3 億美元，全年不低於 11 億美元","action":"未達則停止加碼","source_freq":"季報新分部","date":"2027-05","evidence_refs":["competitive_share_entrants#1"]},{"n":6,"text":"中國政策吸收失敗","type":"風險","maps_to":"R3","metric":"反傾銷稅率與非 GAAP 毛利率季變化","threshold":"對 onsemi 課稅不低於 20% 且毛利率季減不低於 100 基點","action":"減碼三分之一","source_freq":"中國商務部公告、季報","date":null,"evidence_refs":["regulatory_antitrust#2","reg_tariff_export#0"]},{"n":7,"text":"循環反轉領先指標","type":"風險","maps_to":"R4","metric":"通路庫存週數；存貨與營收增速差","threshold":"高於 11 週，或存貨增速連 2 季高於營收增速","action":"停止加碼","source_freq":"法說，每季","date":null,"evidence_refs":["cyclical_prior_downcycle_behavior#0"]},{"n":8,"text":"SiC 與 PSG 走弱（前份保留，SiC 全年數字為資料缺口）","type":"風險","maps_to":"H3","metric":"SiC 營收年增率、PSG 季增率","threshold":"SiC 連 2 季年減且 PSG 季減","action":"減碼三分之一","source_freq":"季報與法說","date":null,"evidence_refs":["cyclical_supply_discipline_capacity#3"]},{"n":9,"text":"影像感測走弱（前份保留，份額為資料缺口）","type":"風險","maps_to":"H3","metric":"ISG 季營收與車用影像份額","threshold":"連 2 季衰退且第三方資料顯示份額流失","action":"停止加碼","source_freq":"季報與產業報告","date":null,"evidence_refs":[]},{"n":10,"text":"多項核心假設同時失敗","type":"清倉","maps_to":"H2","metric":"併購槓桿、車用、毛利率、AI 營收","threshold":"槓桿超標且車用低於 7.4 億美元；或毛利率連 2 季低於 42% 且 AI 全年低於 10 億美元","action":"清倉","source_freq":"季報","date":"2027-08","evidence_refs":[]},{"n":11,"text":"SiC 證券集體訴訟","type":"風險","maps_to":"R5","metric":"訴訟程序與和解金額（金額事實表未涵蓋）","threshold":"集體認證通過且和解金高於一季 FCF，約 4.9 億美元","action":"減碼一半；若有刑事介入則清倉","source_freq":"10-Q 法律事項","date":null,"evidence_refs":["lawsuit_class_action#0","major_events#2"]},{"n":12,"text":"Q4 財報複審","type":"複審日期","maps_to":"H2","metric":"Q4 毛利率、2027 Q1 車用指引","threshold":"毛利率不低於 42%，車用指引回到 7.8 億美元附近","action":"未達則不進場","source_freq":"財報","date":"2027-02","evidence_refs":[]}],"kill_metrics":[{"metric":"車用季營收","bear_threshold":"低於 7.4 億美元","window":"2027 Q1 財報","source":"季報與法說","last_status":"warning"},{"metric":"非 GAAP 毛利率","bear_threshold":"連 2 季低於 42%","window":"2027 Q1 起","source":"季報","last_status":"ok"},{"metric":"AI 資料中心年營收","bear_threshold":"2027 全年低於 10 億美元","window":"FY2027","source":"季報新分部","last_status":"ok"},{"metric":"併購後淨負債÷近四季自由現金流","bear_threshold":"高於 4 倍","window":"合併文件至完成後首份財報","source":"8-K、合併文件、10-Q","last_status":"unknown"},{"metric":"新發股數÷現有流通股","bear_threshold":"高於 15%","window":"合併文件至完成日","source":"8-K、合併文件","last_status":"unknown"},{"metric":"通路庫存週數","bear_threshold":"高於 11 週","window":"每季","source":"法說","last_status":"ok"}],"evidence_dismissed":[{"ref":"geo_supply_chain#1","reason":"這是 2025-02 的新聞標題，只有地緣不確定一語，沒有地區、金額或業務別，也早於本輪復甦，指不到可監測的數字；地緣風險已有中國反傾銷與樂山廠兩項較具體的證據。"}],"action_conditions":{"rearm_trigger":"Synaptics 合併文件顯示完成後淨負債不高於近四季自由現金流 4 倍且新發股數低於流通股 15%，或交易終止；達成後重跑研究","exec_line":"未持有不建倉；條件達成後重跑完整研究，首筆 1.5%，2027 Q1 車用達標後加到上限 3%。","holding_cap":"不高於 3%，循環股且併購未決"}},"decision_inputs":{"signal":"B","ma":"❌","cycle_position":"早循環","cycle_verdict":"未觸發","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等事件不等價位：先讀 2026-10-01 修訂合併協議的現金股票比例與融資安排（本包未收錄），確認完成後淨負債不高於近四季自由現金流 4 倍、新發股數低於流通股 15%；2027 Q1 車用營收達 7.8 億美元以上才補足倉位。"},"thesis":{"H":[{"id":"H1","text":"AI 資料中心電源成為第二引擎，靠完整電源產品線和 800V 架構擴大份額。","2y":"2027 年營收約翻倍到 12 億美元以上","5y":"2030 年有機不低於 25 億美元，含 Ferric 不低於 30 億美元","10y":null,"threshold":"2027 全年不低於 11 億美元","source":"季報與 10-Q 新增的 AI 資料中心分部","drift_rule":"近四季累計低於路徑連 2 季達 5% 為削弱，連 3 季達 10% 為反轉。"},{"id":"H2","text":"稼動率、Fab Right 和新品組合把毛利率帶回高 40%。","2y":"2027 全年非 GAAP 毛利率不低於 43.5%，2027 Q4 不低於 45%","5y":"FY31 約 50%，低於管理層 2030 年 53%","10y":null,"threshold":"2027 全年不低於 43.5%","source":"季報與法說的稼動率揭露","drift_rule":"近四季毛利率低於路徑連 2 季達 5% 為削弱，連 3 季達 10% 為反轉。"},{"id":"H3","text":"車用下滑只是供給調配，2027 年回到長期成長，含量增加抵銷 SAAR 持平。","2y":"2027 Q1 車用不低於 7.8 億美元，全年約增 9%","5y":"2030 年車用仍是最大市場，年化約 9%","10y":null,"threshold":"2027 Q1 車用不低於 7.8 億美元，FY27 總營收不低於 74 億美元","source":"季報與法說","drift_rule":"近四季車用營收低於路徑連 2 季達 5% 為削弱，連 3 季達 10% 為反轉。"}],"R":[{"id":"R1","text":"約 70 億美元的 Synaptics 併購：條款已修訂，中國審查可能嚴格，完成後去槓桿取代回購。","h_ref":"H2","clock":"🔥","threshold":"淨負債高於近四季自由現金流 4 倍，或新發股數高於 15%，或 2027 年底前仍未取得中國審批","evidence_refs":["regulatory_antitrust#1"]},{"id":"R2","text":"車用讓路造成份額或補庫存訂單流失。","h_ref":"H3","clock":"⚡","threshold":"2027 Q1 車用低於 7.4 億美元","evidence_refs":["end_markets#0"]},{"id":"R3","text":"中國反傾銷、樂山封測廠與出口管制；中國約占營收 30%（二手來源）。","h_ref":"H3","clock":"🔥","threshold":"對 onsemi 課稅不低於 20% 且毛利率季減不低於 100 基點","evidence_refs":["regulatory_antitrust#2","reg_tariff_export#0","geo_supply_chain#3"]},{"id":"R4","text":"循環反轉：AI 資本支出放緩或補庫存退潮，上輪股價跌 71%。","h_ref":"H1","clock":"🔥","threshold":"通路庫存高於 11 週，或存貨增速連 2 季高於營收增速","evidence_refs":["cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#1"]},{"id":"R5","text":"SiC 證券集體訴訟未結，減損與重組反覆出現，非 GAAP 獲利可能高估真實盈餘。","h_ref":"H2","clock":"🐢","threshold":"集體認證通過且和解金高於約 4.9 億美元，或再核准 2 億美元以上減損","evidence_refs":["lawsuit_class_action#0","major_events#2","major_events#3"]}],"single_thing":{"description":"Synaptics 併購以高槓桿完成：合併文件或完成後首份財報顯示淨負債高於近四季自由現金流 4 倍，或新發股數超過現有流通股 15%。","why_fatal":"這是最大的單一敏感度：毛利率少 500 基點約減 FY31 EPS 1.19 美元、終端價 19 美元；高槓桿同時帶來利息（新債 60 億美元按假設利率 6% 約減 EPS 0.78 美元）和倍數下修（16 倍降到 12 倍），Base 終端價合計少約 40 美元。現有淨負債僅 3.4 億美元，若約 70 億全數現金，淨負債升到約 79 億，是近四季 FCF 的 4.9 倍，此時再遇循環下行，回購支撐也沒有了。","if_happens":"Bear 機率上調到 40% 以上並重做 EPS 路徑；未持有者不進場，已持有者減碼一半，車用同時失守則清倉。","how_monitor":"2026-10-01 的 8-K 與合併文件中的現金股票比例、融資安排；中國審批進度；完成後首份 10-Q 的淨負債。","probability":"約 35%（12～24 個月）。修訂條款未收錄於事實表，這是粗估，讀到條款後應立即改成接近 0 或接近 100。"}},"appendix_a":{"growth_durability":6,"quality_score":6,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":13.44,"peg_fy2":0.46,"stress":{"pass":null,"total":null}},"eps_meta":{"base_eps_path":{"FY2025A":0.29,"FY2026E":3.28,"FY2027E":4.71,"FY2028E":6.08},"fy_end_month":12,"eps_basis":"FY2026E～FY2028E 為 Koyfin 共識（2026-11-07），判斷為 non-GAAP，依據是 Q3 non-GAAP 0.90 加 Q4 指引中點約 1.01 與 3.28 相符。基期 FY2025A 0.29 為 GAAP 稀釋 EPS，含減損與加速折舊；事實表沒有 FY2025 non-GAAP，因此成長率只看 FY2026E 到 FY2028E。"},"catalysts":[{"date":"2026-Q4","date_precision":"quarter","type":"other","event":"Ferric 併購完成（6 億美元現金，另有最多 1.75 億美元業績獎金）","impact":"低","watch":"付現後現金與 2030 目標的有機拆分"},{"date":"2027-02","date_precision":"month","type":"guidance","event":"Q4 2026 財報與 2027 Q1 指引","impact":"高","watch":"車用指引是否回到 7.8 億美元附近，毛利率是否達 42.5%"},{"date":"2027-05","date_precision":"month","type":"guidance","event":"2027 Q1 財報","impact":"高","watch":"車用營收、AI 資料中心營收與上半年毛利率節奏"},{"date":"2027-Q2","date_precision":"quarter","type":"regulatory","event":"Synaptics 併購預計年中完成，須通過中國市場監管審查","impact":"高","watch":"審批進度、融資條款與完成後淨負債"},{"date":"2027-Q4","date_precision":"quarter","type":"product","event":"800V 資料中心機櫃開始放量","impact":"中","watch":"AI 資料中心季增率與垂直 GaN 營收"}],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8(val爭議)","pacing":["row4：週線❌，進場節奏強制分批（starter 1/3＋趨勢確認後加碼），頁首掛「⚠️ 週線趨勢未確認，逢回分批勿接刀」"],"holding_cap":null,"audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='C'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":true,"basis":"ma='❌'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟢', val='🟡', moat_trend='→', week26=-38.65, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='循環/商品', cycle_position='早循環', moat='C', moat_trend='→', cycle_gates_pass=None","input_gap":["cycle_gates_pass"]},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈機械讀數判定不可用，baseline rows 8/9/9b/10 的估值條件視為不可判 → 落 row8 觀望（保守方向）","hit":true,"basis":"val_denominator_disputed=True, val(機械讀數)='🟡'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"requires_critic":[]}}
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
