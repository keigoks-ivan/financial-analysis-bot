你是 DD 管線 v20 的判斷層閘（gate），標的 SNDK（20261102）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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
- `f_kpi0_revenue_gaap`（q1_business）｜Revenue (GAAP)＝11031 USD M｜期間與口徑：Q1 FY2027（季末 2026-10-02，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 https://investor.sandisk.com/news-releases/news-release-details/sandisk-reports-fiscal-first-quarter-2027-financial-results（numbers.latest_quarter_kpis.items[0]，as_of Q1 FY2027（季末 2026-10-02，公告於 2026-10-29））
  - 註記：consensus 約 $10.7B（來源：Investing.com Q1 FY27 slides 報導，非 IR）
- `f_kpi1_non_gaap_operating_incom`（q1_business）｜Non-GAAP operating income / margin＝8871 USD M；margin 80.4%｜期間與口徑：Q1 FY2027（季末 2026-10-02，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 https://investor.sandisk.com/news-releases/news-release-details/sandisk-reports-fiscal-first-quarter-2027-financial-results（numbers.latest_quarter_kpis.items[1]，as_of Q1 FY2027（季末 2026-10-02，公告於 2026-10-29））
- `f_kpi2_gaap_operating_income_ma`（q1_business）｜GAAP operating income / margin＝8780 USD M；margin 79.6%（8,780÷11,031，自算）｜期間與口徑：Q1 FY2027（季末 2026-10-02，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 https://investor.sandisk.com/news-releases/news-release-details/sandisk-reports-fiscal-first-quarter-2027-financial-results（numbers.latest_quarter_kpis.items[2]，as_of Q1 FY2027（季末 2026-10-02，公告於 2026-10-29））
- `f_kpi3_free_cash_flow`（q1_business）｜Free cash flow＝6309 USD M；占營收 57.2%（自算）｜期間與口徑：Q1 FY2027（季末 2026-10-02，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 https://investor.sandisk.com/news-releases/news-release-details/sandisk-reports-fiscal-first-quarter-2027-financial-results（numbers.latest_quarter_kpis.items[3]，as_of Q1 FY2027（季末 2026-10-02，公告於 2026-10-29））
- `f_kpi5_guidance_q2_fy2027_reven`（q1_business）｜Guidance Q2 FY2027 revenue＝12,200–12,600 USD M｜期間與口徑：Q1 FY2027（季末 2026-10-02，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司 IR 新聞稿 https://investor.sandisk.com/news-releases/news-release-details/sandisk-reports-fiscal-first-quarter-2027-financial-results（numbers.latest_quarter_kpis.items[5]，as_of Q1 FY2027（季末 2026-10-02，公告於 2026-10-29））
  - 註記：Non-GAAP EPS Q1 實際 $49.51 vs consensus $47.15（Investing.com）
- `f_earnings_recency`（q1_business）｜最近一次財報日＝2026-10-29 date｜期間與口徑：2026-10-29／距今 2 個交易日｜kind：realized
  - 來源：—（numbers.earnings_recency，as_of 2026-10-29）
- `f_peer_sndk_gross_margin_pct`（q2_moat）｜SNDK 毛利率＝76.84 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.SNDK.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_sndk_operating_margin_pct`（q2_moat）｜SNDK 營業利益率＝68.43 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.SNDK.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_sndk_fcf_margin_pct`（q2_moat）｜SNDK FCF 利潤率＝61.63 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.SNDK.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_mu_gross_margin_pct`（q2_moat）｜MU 毛利率＝80.72 %｜期間與口徑：TTM ending 2026-08-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MU.gross_margin_pct，as_of TTM ending 2026-08-31（4季加總））
- `f_peer_mu_operating_margin_pct`（q2_moat）｜MU 營業利益率＝74.59 %｜期間與口徑：TTM ending 2026-08-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MU.operating_margin_pct，as_of TTM ending 2026-08-31（4季加總））
- `f_peer_mu_fcf_margin_pct`（q2_moat）｜MU FCF 利潤率＝44.27 %｜期間與口徑：TTM ending 2026-08-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MU.fcf_margin_pct，as_of TTM ending 2026-08-31（4季加總））
- `f_peer_000660_ks_gross_margin_pct`（q2_moat）｜000660.KS 毛利率＝76.27 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.000660.KS.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_000660_ks_operating_margin_pct`（q2_moat）｜000660.KS 營業利益率＝68.04 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.000660.KS.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_000660_ks_fcf_margin_pct`（q2_moat）｜000660.KS FCF 利潤率＝47.8 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.000660.KS.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_005930_ks_gross_margin_pct`（q2_moat）｜005930.KS 毛利率＝57.48 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.005930.KS.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_005930_ks_operating_margin_pct`（q2_moat）｜005930.KS 營業利益率＝36.88 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.005930.KS.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_005930_ks_fcf_margin_pct`（q2_moat）｜005930.KS FCF 利潤率＝28.95 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.005930.KS.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_wdc_gross_margin_pct`（q2_moat）｜WDC 毛利率＝52.6 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.WDC.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_wdc_operating_margin_pct`（q2_moat）｜WDC 營業利益率＝40.69 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.WDC.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_wdc_fcf_margin_pct`（q2_moat）｜WDC FCF 利潤率＝29.62 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.WDC.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝226.74 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-10-31）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝274.64 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-10-31）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝256.77 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-10-31）
- `f_consensus_rev_fy1_pct`（q5_valuation）｜FY1 共識修正＝5.55 %｜期間與口徑：2026-10-31／兩份 Koyfin 快照之間的 EPS 修正幅度（214.82 → 226.74）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.fy1.revision_pct，as_of 2026-10-31）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝49379.2 USD m｜期間與口徑：2026-11-02／yfinance revenue_estimate 0y 平均（18 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-02）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝60356.3 USD m｜期間與口徑：2026-11-02／yfinance revenue_estimate +1y 平均（20 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-02）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi4_sbc_gaap`（q4_capital）｜SBC 占 GAAP 營業利益＝1.04 %（SBC 91M ÷ GAAP 營業利益 8,780M，自算；占營收 0.83%）｜期間與口徑：Q1 FY2027（季末 2026-10-02，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 https://investor.sandisk.com/news-releases/news-release-details/sandisk-reports-fiscal-first-quarter-2027-financial-results（numbers.latest_quarter_kpis.items[4]，as_of Q1 FY2027（季末 2026-10-02，公告於 2026-10-29））
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝-5005.0 USD m｜期間與口徑：2026-11-02／yfinance 最新一季：總債務 201.0、現金 5206.0（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-02）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝142.29 m shares｜期間與口徑：2026-11-02／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-11-02）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝1150.89 USD｜期間與口徑：2026-10-30（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-10-30（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝5.08 x｜期間與口徑：2026-10-31／分母＝FY1 EPS 226.74，分子＝快照價 1150.89｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-10-31）
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝9.2 x｜期間與口徑：2026-10-30（RTH 收盤，UTC）／1 個年度端點內的分位＝50.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-10-30（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝50.0 %｜期間與口徑：2026-10-30（RTH 收盤，UTC）／**非五年分位**：只用 1 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-10-30（RTH 收盤，UTC））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝5.65 x｜期間與口徑：2026-10-30（RTH 收盤，UTC）／4 個年度端點內的分位＝38.6｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-10-30（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝38.6 %｜期間與口徑：2026-10-30（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-10-30（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝5.48 x｜期間與口徑：2026-10-30（RTH 收盤，UTC）／4 個年度端點內的分位＝37.6｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-10-30（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝37.6 %｜期間與口徑：2026-10-30（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-10-30（RTH 收盤，UTC））
- `f_ev_s_fwd`（q5_valuation）｜EV/S（EV ÷ FY1 共識營收）＝3.22 x｜期間與口徑：2026-11-02／f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）｜kind：estimate
  - 來源：—（numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m，as_of 2026-11-02）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_consensus_rev_fy2_pct`（q5_valuation）｜FY2 共識修正＝3.13 %｜期間與口徑：2026-10-31／兩份 Koyfin 快照之間的 EPS 修正幅度（266.3 → 274.64）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.fy2.revision_pct，as_of 2026-10-31）
- `f_consensus_rev_fy3_pct`（q5_valuation）｜FY3 共識修正＝0.0 %｜期間與口徑：2026-10-31／兩份 Koyfin 快照之間的 EPS 修正幅度（256.77 → 256.77）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.fy3.revision_pct，as_of 2026-10-31）
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝240.04 %｜期間與口徑：2026-07-30 → 2026-10-31／FY1 共識 EPS 66.68 → 226.74（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-10-31）
- `f_ev_m`（q5_valuation）｜目前企業價值 EV（市值＋淨負債）＝158754.41 USD m｜期間與口徑：2026-11-02／市值 163759.41 ＋ 淨負債 -5005.0｜kind：realized
  - 來源：—（numbers.capital_structure.ev_m，as_of 2026-11-02）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝-3.04 %｜期間與口徑：2026-10-30（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-10-30（RTH 收盤，UTC））
- `f_rsi14`（q5_valuation）｜RSI(14)＝32.73｜期間與口徑：2026-10-30（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-10-30（RTH 收盤，UTC））
- `f_ma_state`（q5_valuation）｜週線均線六態（decision_inputs.ma 必須等於此值）＝-｜期間與口徑：2026-11-02／timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-02）
  - 原文：「price 1150.89 / W52 1060.08 / W104 None / W250 None / W250 13週斜率 None%」
- `f_ma_w52`（q5_valuation）｜52 週均線＝1060.08 USD｜期間與口徑：2026-11-02／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-02）

### findings_digest 中方向為負或來源衝突的條目（16 條）
- `competitive_share_entrants#1`（competitive_share_entrants｜方向 -｜狀態 ok）：Counterpoint 2026 Q2 NAND 營收市占：Samsung 28%、SK hynix 19%、Micron 15%、Kioxia 14%、YMTC 14%、SanDisk 11%（較上季降 2pp）；YMTC 為快速上升的中國進入者（Q1 13%，較 2025Q1 的 8% 上升）
  - 來源：Counterpoint Research / 搜尋摘要彙整（technews.tw 2026-09-07 報導）（as_of 2026-09-07）｜affects：moat_trend、decision_inputs.bear
- `customer_second_source#0`（customer_second_source｜方向 -｜狀態 ok）：FY2026 10-K：前十大客戶占營收 44%（FY2025 40%、FY2024 41%），公司自述這些客戶有多家供應商可選；搜尋摘要稱無單一客戶占營收逾 10%。未查到特定最大客戶導入第二供應商或自製的公開報導。
  - 來源：SEC EDGAR 10-K FY2026 Item 1A（as_of 2026-08-17）｜affects：moat_trend、decision_inputs.bear
- `customer_concentration_credit#1`（customer_concentration_credit｜方向 -｜狀態 ok）：2026-07-03 應收帳款淨額 47 億美元，三家客戶分別占約 19%、12%、10%（前一年僅一家占 11%，淨額 11 億美元）；信用損失準備金不重大，一般不要求擔保品。
  - 來源：SEC EDGAR｜Sandisk 10-K FY2026｜Item 8 Customer Concentration and Credit Risk（as_of 2026-08-17）｜affects：thesis.R、decision_inputs.bear
- `supply_demand_durability#0`（supply_demand_durability｜方向 -｜狀態 ok）：TrendForce 2026年7月展望：2026年NAND供給缺口約4–5%，2027年供給成長將超過需求、缺口於2027下半年緩解；主因中國供應商新設備投產擴產與既有產線製程升級。
  - 來源：TrendForce Press Center 2026-07-21（as_of 2026-07-21）｜affects：thesis.R、decision_inputs.bear、valuation
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：10-K 揭露：國際銷售占淨營收 82%（FY2026），暴露於關稅與貿易法規風險。
  - 來源：SEC EDGAR 10-K FY2026 Item 1（as_of 2026-08-17）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#1`（reg_tariff_export｜方向 -｜狀態 ok）：美國 Section 232 與 301 調查進行中，可能影響關稅；目前在美銷售的多數產品免關稅，若失去豁免或加稅將增加銷貨成本、壓縮毛利。
  - 來源：SEC EDGAR 10-K FY2026 Item 7 MD&A（as_of 2026-08-17）｜affects：thesis.R、decision_inputs.bear、valuation
- `reg_tariff_export#2`（reg_tariff_export｜方向 -｜狀態 ok）：10-K 風險因子：供應商可能因關稅、配額、制裁、禁運等貿易限制而無法供貨，導致成本上升與交期拉長。
  - 來源：SEC EDGAR 10-K FY2026 Item 1A（as_of 2026-08-17）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：FY2026 10-K：絕大部分快閃記憶體取自與 Kioxia 的 Flash Ventures 合資，合約條款限制 Sandisk 改變產出或另找貨源的能力
  - 來源：Sandisk Form 10-K FY2026 (SEC)（as_of 2026-07-03）｜affects：decision_inputs.bear、thesis.R
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：FY2026 10-K：幾乎所有產品在海外生產，地緣緊張、貿易戰可能衝擊需求、毛利與產能利用
  - 來源：Sandisk Form 10-K FY2026 (SEC)（as_of 2026-07-03）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#3`（geo_supply_chain｜方向 -｜狀態 ok）：Digitimes 標題：2026-04-20 東北強震震央近 Kioxia 北上（Kitakami）NAND 廠，Sandisk 與群聯暫停報價；未見損害或產出影響的第二來源
  - 來源：Digitimes semiconductors topic（as_of 2026-04-20）｜affects：decision_inputs.bear、thesis.R
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：10-K 風險因子載明：公司對產品的需求日益取決於 NAND 在 AI 基礎設施的使用，可能出現更有效率或減少每單位 AI 運算所需儲存量的新/替代技術，若大規模採用可能快速削弱公司技術的重要性與需求；新產品也可能替代現有產品使其過時。
  - 來源：SEC EDGAR 10-K FY2026 Item 1A（as_of 2026-08-17）｜affects：moat_trend、decision_inputs.bear、thesis.R
- `cyclical_supply_discipline_capacity#0`（cyclical_supply_discipline_capacity｜方向 -｜狀態 ok）：TrendForce：2026 因廠房空間有限且優先擴 DRAM，NAND 供給主要靠製程升級，預估供給短缺 4–5%；2027 因高層數遷移與新廠逐步爬坡，位元供給成長明顯高於 2026，供需預期 2027 下半年轉正、短缺緩解。
  - 來源：TrendForce 研究報告 Global Memory Supply-Demand Divergence (RP260727PO) / iconnect007 轉載（as_of 2026-07-27）｜affects：thesis.R、decision_inputs.bear、valuation
- `cyclical_inventory_price_position#3`（cyclical_inventory_price_position｜方向 -｜狀態 ok）：TrendForce：模組廠庫存因消費需求疲弱、去化放慢而上升；其他買家庫存在可控範圍
  - 來源：CTEE 工商時報（as_of 2026-07-22）｜affects：thesis.R、decision_inputs.bear
- `cyclical_prior_downcycle_behavior#0`（cyclical_prior_downcycle_behavior｜方向 -｜狀態 ok）：上一輪下行（WD 時期 flash 業務）FY2023 營收下滑約 38%、每 GB 平均售價降約 39%；毛利率由 FY2022 的 33.3% 降至 7.1%。
  - 來源：Webull/Motley Fool: Sandisk's Sales Fell 38% in the Last Flash Memory Downturn（as_of 2025-10-20）｜affects：valuation、decision_inputs.bear
- `cyclical_prior_downcycle_behavior#1`（cyclical_prior_downcycle_behavior｜方向 -｜狀態 ok）：TrendForce：NAND 4Q22 合約價下跌 20-25%，3Q22 晶圓合約價預估跌幅由 15-20% 上修至 30-35%；1Q23 跌幅收斂至約 10-15%，2Q23 預期 5-10%。
  - 來源：TrendForce press center 2022-2023（as_of 2023-01-05）｜affects：decision_inputs.bear、valuation
- `cyclical_prior_downcycle_behavior#2`（cyclical_prior_downcycle_behavior｜方向 -｜狀態 ok）：Micron 分析：記憶體前兩輪下行（2010-12、2014-16）以 EBITDA 毛利率衡量分別持續 7 與 9 季；另有評論稱 2021 高點至 2023 低點記憶體營收約降 40%，週期高點到高點約 3-5 年。
  - 來源：Seeking Alpha: Micron: How Low Will It Go? / uncoveralpha: every memory cycle ends the same（as_of 2025-01-01）｜affects：decision_inputs.bear、thesis.R

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 20 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/SNDK_20261102/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":3850,"bear_5y_price":600,"p_bull_pct":20,"p_bear_pct":35,"upside_5y_pct":52.1,"ev5y_pct":53.6,"irr_base_pct":8.7,"asym_ratio":2.8,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":226.74,"pe":5.08,"basis":"FY1（FY2027，約 2027 年 6 月底結束）共識非 GAAP 每股盈餘，拆股前口徑；終端倍數同樣套在當年度每股盈餘上"},"eps":{"bull":[230,285,310,330,350],"base":[218,240,185,150,175],"bear":[205,150,60,35,60]},"pe":{"bull":11,"base":10,"bear":10},"p":{"bull":20,"base":45,"bear":35},"yield_pct":{"dividend":0,"net_buyback":0},"second_stage":{"bull_cagr_pct":10,"base_cagr_pct":5},"valuation_dependent":true}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### SNDK_Q4_2026_Earnings_Call_20260805.md
- 2026-08-05｜CFO Luis Visoso｜guidance：FQ1'27 營收財測 $10.3–10.8B，成長來自 bit 與價格（原話："For the first quarter of fiscal year 2027, we expect revenue between $10.3 billion and $10.8 billion with"）
- 2026-08-05｜CFO Luis Visoso｜guidance：FQ1 成長由 bit 成長與較高價格共同驅動（原話："sequential growth driven by both bit growth and higher pricing."）
- 2026-08-05｜CFO Luis Visoso｜guidance：FQ1 non-GAAP EPS 財測 $44–46，假設 1.55 億稀釋股數（原話："We expect first quarter non-GAAP EPS between $44 and $46"）
- 2026-08-05｜CFO Luis Visoso｜guidance：FQ1 non-GAAP 營業費用財測 $520–540M（原話："non-GAAP operating expenses between $520 million and $540"）
- 2026-08-05｜CFO Luis Visoso｜guidance：管理層估 2026 年 NAND 市場超過 $300B、年增 3 倍（原話："$300 billion in revenue in calendar year 2026, up 3x year-over-year."）
- 2026-08-05｜CFO Luis Visoso｜guidance：管理層估 2027 年 NAND 市場接近 $500B（原話："estimate that the NAND market will approach $500 billion in revenue in calendar year 2027."）
- 2026-08-05｜CFO Luis Visoso｜guidance：管理層稱客戶需求成長快於供給（原話："Demand from our customers is growing faster than our supply."）
- 2026-08-05｜CFO Luis Visoso｜guidance：預期 bit 供給在 2027 曆年之後仍處於配貨狀態（原話："remain on allocation beyond calendar year 2027."）
- 2026-08-05｜CFO Luis Visoso｜guidance：FY27 資本支出金額增加但占營收降至約 6%（原話："relative to revenue will come down to approximately 6%"）
- 2026-08-05｜CFO Luis Visoso｜guidance：FY27 將維持較高庫存天數以支應 NBM 與零組件成本（原話："We plan to operate at higher inventory days"）
- 2026-08-05｜CFO Luis Visoso｜guidance：較高庫存使 FY27 可售 bit 成長降至中段十位數百分比（原話："The higher inventory levels reduce sellable bits to"）
- 2026-08-05｜CEO David Goeckeler｜guidance：Goeckeler 稱智慧型手機與 PC 今年單位量下滑中段十位數百分比（原話："we see units down mid-teens for both smartphones"）
- 2026-08-05｜CEO David Goeckeler｜guidance：預期手機、PC 市場於 2027 曆年恢復成長（原話："We expect these markets to return to growth in calendar"）
- 2026-08-05｜CFO Luis Visoso｜margin：FQ4 non-GAAP 毛利率 84.6%（高於財測 79–81%）（原話："Non-GAAP gross margin for the fourth quarter was 84.6%"）
- 2026-08-05｜CFO Luis Visoso｜margin：FQ4 non-GAAP EPS $39.25（前季 $23.41）（原話："$39.25, up from $23.41 in the prior quarter"）
- 2026-08-05｜CFO Luis Visoso｜margin：FQ4 營收 $8,965M，季增 51%、年增 372%（原話："Revenue for the fourth quarter was $8,965 million, up 51% sequentially and 372% year-over-year."）
- 2026-08-05｜CFO Luis Visoso｜margin：FQ4 營收季增拆解：約 1/3 量、2/3 價（原話："came approximately 1/3 from higher volumes and 2/3"）
- 2026-08-05｜CFO Luis Visoso｜margin：調整後自由現金流 $5,035M（口徑排除 NBM 預付款與保證金）（原話："We generated $5,035 million in adjusted free cash flow"）
- 2026-08-05｜CFO Luis Visoso｜margin：調整後 FCF 排除的 NBM 預付款與存款金額，原文稱仍計入營運現金流（原話："This excludes $1,938 million in NBM prepayments and deposits"）
- 2026-08-05｜CFO Luis Visoso｜margin：CFO 稱 NBM 約維持 80% 毛利率，價格上漲有部分上行空間（原話："we do expect to be around 80% for the new business"）
- 2026-08-05｜CEO David Goeckeler｜margin：CEO 將中 80% 段毛利率描述為合理回報（原話："I think mid-80s gross margin, I would characterize as a fair"）
- 2026-08-05｜CFO Luis Visoso｜margin：CFO 解釋 FQ1 毛利率財測 83–85% 為「略低、略高於」本季實績，含組合與零組件成本假設（原話："So slightly down, slightly up from what we printed"）
- 2026-08-05｜CFO Luis Visoso｜margin：CFO 稱連續 5 季毛利率擴張，終點數字為 86.5%（與稿中 FQ4 84.6% 數字並陳）（原話："starting with 22.7% all the way to 86.5%."）
- 2026-08-05｜CFO Luis Visoso｜customer：自上次財報後新簽 5 筆 NBM（3 筆新客戶、2 筆擴約）（原話："we have signed 5 additional agreements"）
- 2026-08-05｜CFO Luis Visoso｜customer：NBM 預計占 FY27 超過 50% bit、FY28 約 2/3（原話："50% of our bits in fiscal year 2027, and approximately 2/3"）
- 2026-08-05｜CFO Luis Visoso｜customer：已簽 NBM 在地板價假設下最低總營收 $93.9B（原話："is a minimum of $93.9 billion, assuming floor pricing."）
- 2026-08-05｜CFO Luis Visoso｜customer：季末 RPO $59.8B（含季後簽的 2 筆為 $91.1B）（原話："RPO, at the end of the quarter was $59.8 billion"）
- 2026-08-05｜CFO Luis Visoso｜customer：NBM 附現金與金融工具形式的財務保證，總額 $16.5B（原話："financial guarantees through a combination of cash deposits"）
- 2026-08-05｜CFO Luis Visoso｜customer：NBM 定價含固定與浮動部分，浮動部分設有地板與天花板（原話："We expect attractive margins even at"）
- 2026-08-05｜CEO David Goeckeler｜customer：CEO 稱大客戶已回頭要求加量（原話："some of our biggest customers are already coming back"）
- 2026-08-05｜CFO Luis Visoso｜customer：FQ4 消費者營收 $556M，季減 32%（原話："Consumer revenue was $556"）
- 2026-08-05｜CEO David Goeckeler｜customer：CEO 解釋消費端調價難跟上其他市場速度（原話："move the consumer up as much as possible."）
- 2026-08-05｜CEO David Goeckeler｜customer：資料中心占 bit 比重由一年前約 12% 升至本財年末 38%（原話："A year ago, Datacenter represented roughly 12% of our bits."）
- 2026-08-05｜CFO Luis Visoso｜commitment：管理層承諾對新增 NBM 保持高度挑選（原話："Going forward, we will remain highly"）
- 2026-08-05｜CEO David Goeckeler｜commitment：CEO 稱買回執行將維持一致（原話："We expect to be very consistent in our execution of this program."）
- 2026-08-05｜CFO Luis Visoso｜commitment：供給成長維持中到高十位數百分比的承諾（原話："we continue to be committed to grow bits mid- to high teens"）
- 2026-08-05｜CFO Luis Visoso｜commitment：CFO 稱 FY27 長期 bit 成長數字會略低（原話："our ongoing number, will be a little bit lower for 2027."）
- 2026-08-05｜CEO David Goeckeler｜commitment：CEO 稱計畫與市場同步成長（原話："We want to grow with the market, and we plan to grow with the market."）
- 2026-08-05｜CFO Luis Visoso｜capital_allocation：董事會再授權 $14B 買回，剩餘授權合計 $15.5B（原話："an additional $14 billion share repurchase program"）
- 2026-08-05｜CFO Luis Visoso｜capital_allocation：CFO 稱目前以買回作為股東回報方式，並說明情況可能改變（原話："things may change as time goes on"）
- 2026-08-05｜CFO Luis Visoso｜capital_allocation：CFO 以稅務效率為買回理由（原話："more tax efficient and probably the right thing for us to do"）
- 2026-08-05｜CEO David Goeckeler｜product：BiCS 8 已提升至多數 bit 產出（原話："we ramped BiCS 8 to the majority of our bit"）
- 2026-08-05｜CEO David Goeckeler｜product：QLC Stargate 平台本季開始出貨並認列營收（原話："we began shipping our QLC Stargate platform for revenue"）
- 2026-08-05｜CEO David Goeckeler｜product：CEO 談 HBF 出貨與發布時間表，僅說之後再公布（原話："So we'll have more to say as we progress with"）
- 2026-08-05｜CEO David Goeckeler｜product：CEO 稱對 BiCS 10 與 HBF 定價評論為時尚早（原話："it's a little early to talk about pricing on some of those nodes"）
- 2026-08-05｜CEO David Goeckeler｜competition：供給成長主要靠製程節點轉換而非增加晶圓（原話："primarily through nodal transitions rather than wafer additions"）
- 2026-08-05｜CEO David Goeckeler｜competition：被問在 $500B 市場是否維持市占，CEO 稱這一直是目標（原話："It's always our goal, Joe."）
- 2026-08-05｜CEO David Goeckeler｜risk：CEO 提及 $16.5B 保證金的情境：黑天鵝事件（原話："But if some black swan event happens"）
- 2026-08-05｜CEO David Goeckeler｜risk：CEO 說明保證金額度預期不會真的收到（原話："$16.5 billion in aggregate would flow to us"）
- 2026-08-05｜CEO David Goeckeler｜risk：CEO 對比一年前能見度僅 3 個月（敘事轉變：現稱 4 年以上）（原話："we were talking about visibility in this business of 3 months"）

### SNDK_Analyst_Investor_Day_Sandisk_Corporation_20260813.md
- 2026-08-13｜CFO Luis Visoso｜guidance：2028–2030 營收成長目標與位元成長一致（原話："we expect to grow revenue mid- to high teens"）
- 2026-08-13｜CFO Luis Visoso｜margin：2028–2030 non-GAAP 毛利率目標約 80%（原話："We expect non-GAAP gross margin to be around 80%."）
- 2026-08-13｜CFO Luis Visoso｜margin：營業利益率 75% 的拆解：OpEx 約 5% 營收（原話："We expect to spend about 5% in OpEx"）
- 2026-08-13｜CFO Luis Visoso｜guidance：75% 營業利益率之後，調整後自由現金流率 50%（原話："So you get to that 75%. And then you get to 50%"）
- 2026-08-13｜CFO Luis Visoso｜guidance：建模用資本密集度假設為中個位數 % 營收（gross CapEx）（原話："I would assume mid-single-digit capital intensity"）
- 2026-08-13｜CFO Luis Visoso｜guidance：FY27 位元成長中段十幾 %、價格逐季溫和（原話："we expect sequential prices to be modest throughout the year"）
- 2026-08-13｜CEO David Goeckeler｜commitment：承諾位元／出貨量長期中高十幾 % 成長（原話："committed to this grow volume mid- to high teens."）
- 2026-08-13｜CFO Luis Visoso｜commitment：超額現金 100% 還給股東（原話："excess cash -- will go back to shareholders."）
- 2026-08-13｜CFO Luis Visoso｜capital_allocation：董事會再授權 140 億美元庫藏股（原話："the Board authorized another $14 billion program."）
- 2026-08-13｜CFO Luis Visoso｜capital_allocation：無負債、不動用循環信貸（原話："We have no debt. We got rid of the TLB."）
- 2026-08-13｜CFO Luis Visoso｜capital_allocation：信評 BB+，打算持續改善（原話："We're at BB+ overall, and we intend to continue"）
- 2026-08-13｜CEO David Goeckeler｜capital_allocation：延長與 Kioxia 合資，確保 2030–2034 產能（原話："we had production of NAND from 2030 to 2034"）
- 2026-08-13｜CEO David Goeckeler｜capital_allocation：持有 4% 股權，本季認列約 8 億美元收益（原話："we took a 4% equity stake in the company."）
- 2026-08-13｜CEO David Goeckeler｜capital_allocation：該股權投資認列的收益金額（原話："an $800 million gain on that investment."）
- 2026-08-13｜CFO Luis Visoso｜customer：NBM 客戶共 8 家，含 3 家美國超大規模業者（原話："include 3 hyperscalers from the U.S."）
- 2026-08-13｜CFO Luis Visoso｜customer：最早一筆 NBM 僅在今年 1 月簽署（原話："the oldest deal we signed was only in January of this"）
- 2026-08-13｜CFO Luis Visoso｜customer：2 家客戶已回頭擴大合約（原話："2 customers already came back and they said"）
- 2026-08-13｜CEO David Goeckeler｜customer：客戶開始主動提出多年合約（原話："now they're proposing the agreement, not us."）
- 2026-08-13｜CFO Luis Visoso｜commitment：NBM 合約平均期間超過 4 年、最長 5 年（原話："The longest contract is 5 years"）
- 2026-08-13｜CFO Luis Visoso｜customer：NBM 合約帶有固定與變動定價（原話："there are fixed and variable components on pricing."）
- 2026-08-13｜CFO Luis Visoso｜risk：每份 NBM 皆有財務擔保（原話："every single one of these agreements has a financial"）
- 2026-08-13｜CFO Luis Visoso｜margin：NBM 底價情境下毛利率約 80%（原話："around 80% gross margin for the floor pricing."）
- 2026-08-13｜CFO Luis Visoso｜margin：重申底價下 NBM 毛利率不低於約 80%（原話："we don't expect these NBMs to be below 80%"）
- 2026-08-13｜CFO Luis Visoso｜customer：NBM 總合約價值（以底價計）（原話："the $93.9 billion, that's the Total Contract Value, TCV."）
- 2026-08-13｜CFO Luis Visoso｜customer：剩餘履約義務金額（原話："RPO, is $91.1 billion."）
- 2026-08-13｜CFO Luis Visoso｜risk：已取得的財務擔保總額（原話："we have secured $16.5 billion in financial guarantees"）
- 2026-08-13｜CFO Luis Visoso｜risk：客戶存款與信用額度已入帳 25 億美元（原話："$2.5 billion in our bank."）
- 2026-08-13｜CEO David Goeckeler｜guidance：供給有 50% 至 2/3 已在協議下（原話："50% to 2/3 of our supply is under agreements"）
- 2026-08-13｜CFO Luis Visoso｜commitment：對新增 NBM 保持挑選（原話："We'll be very selective going forward to make sure we"）
- 2026-08-13｜CFO Luis Visoso｜margin：FY26 毛利率 71.6%，前一年 30.3%（原話："Gross margin 71.6% -- that's up from 30.3% the year before."）
- 2026-08-13｜CFO Luis Visoso｜margin：FY26 第四季毛利率 84.6%（原話："We closed the year with 84.6% gross margin."）
- 2026-08-13｜CFO Luis Visoso｜margin：自由現金流口徑：排除 NBM 預付款與保證金（原話："And this excludes cash we received from our NBMs as"）
- 2026-08-13｜CFO Luis Visoso｜margin：FY26 自由現金流（不含 NBM 預付款）（原話："We generated $8.7 billion in free cash flow"）
- 2026-08-13｜CEO David Goeckeler｜margin：管理層表示不預期 2023 年那種低谷重現（原話："I don't expect '23 to come back, by the way."）
- 2026-08-13｜CFO Luis Visoso｜guidance：HBF 不在營收預測內（原話："HBF is not in the revenue projections."）
- 2026-08-13｜CEO David Goeckeler｜guidance：澄清 3000 億／5000 億美元是含中國的市場規模，非營收預測（原話："revenue forecast for '27. It wasn't, right? It wasn't."）
- 2026-08-13｜Eric Cherrstrom｜guidance：市場規模預測 2027 年近 5000 億美元（原話："again grow to nearly $500 billion in 2027"）
- 2026-08-13｜Eric Cherrstrom｜risk：邊緣裝置（PC/手機）單位數預期年減中十幾 %（原話："our expectation of unit decline year-over-year"）
- 2026-08-13｜Eric Cherrstrom｜competition：資料中心占 TAM 位元比重（原話："This year, 50% and continues to outpace the market."）
- 2026-08-13｜CTO Alper Ilkbahar｜competition：同業資本支出為公司的 2.66 倍（原話："the industry spent on average, 2.66x more capital"）
- 2026-08-13｜CTO Alper Ilkbahar｜competition：資本效率約為最近競爭對手 2 倍（原話："our capital efficiency is just about 2x that of our nearest"）
- 2026-08-13｜CTO Alper Ilkbahar｜competition：同業新世代功耗效率改善有限（原話："their power efficiency is really not moving a lot better."）
- 2026-08-13｜CEO David Goeckeler｜competition：舊世界（低於邊際成本賣 NAND）已不存在（原話："I think that world has gone, quite frankly."）
- 2026-08-13｜CTO Alper Ilkbahar｜product：BiCS10 1Tb TLC 本月開始送樣（原話："start sampling this die to our customers as of"）
- 2026-08-13｜CTO Alper Ilkbahar｜product：BiCS10 2Tb QLC 密度比 BiCS8 高逾 60%（原話："more than 60% density improvements over BiCS8"）
- 2026-08-13｜CTO Alper Ilkbahar｜product：BiCS9 已進入 NBM 供貨範圍（原話："this product is already as part of our NBMs"）
- 2026-08-13｜CEO David Goeckeler｜product：每年每片晶圓位元產出成長 27%（原話："we can grow output per wafer at a rate of 27% a"）
- 2026-08-13｜CTO Alper Ilkbahar｜product：實際只用掉 27% 生產力的三分之二（原話："we're using only two-thirds of that capability"）
- 2026-08-13｜CTO Alper Ilkbahar｜product：HBF 第一顆記憶體晶粒已 tape-out（原話："we actually taped out our first HBF memory die."）
- 2026-08-13｜CTO Alper Ilkbahar｜product：HBF 預計明年送樣給推論裝置客戶（原話："deliver our first samples to our customers of"）
- 2026-08-13｜CPO Khurram Ismail｜product：KV cache 預估占 2030 年市場 35%（原話："KV cache is going to be 35% of the"）
- 2026-08-13｜CEO David Goeckeler｜commitment：成本下降歸公司所有，價格由市場決定（原話："the market will determine what the price of our product"）
- 2026-08-13｜CEO David Goeckeler｜commitment：不再討論 cost down（原話："We're not talking about cost downs anymore."）
- 2026-08-13｜CEO David Goeckeler｜guidance：去年投資人日對價格轉正的判斷被低估（原話："if anything, we significantly undercalled it."）
- 2026-08-13｜CEO David Goeckeler｜risk：對 NBM 能否撐過下行期，管理層自承無保證（原話："Is it a guarantee? There's no guarantees."）
- 2026-08-13｜CEO David Goeckeler｜risk：管理層承認客戶可能退出合約的說法存在（原話："They could be just a big head-fake. They"）
- 2026-08-13｜CEO David Goeckeler｜customer：資料中心占比將上升，最終目標視情況（原話："Where is the final target? It depends."）
- 2026-08-13｜CFO Luis Visoso｜customer：NBM 占比隨時間調整，未給 FY29 以後上限（原話："that number will keep on evolving."）

### 問答異常語氣（迴避／改口／保留）
- SNDK_Q4_2026_Earnings_Call_20260805.md｜問：Reitzes：若每季買回約 $5B，這是否是該思考的買回規模？｜答法：未給金額或節奏數字，僅稱執行將一致、對現金產生有信心
- SNDK_Q4_2026_Earnings_Call_20260805.md｜問：Schneider：是否考慮股利？｜答法：回答聚焦買回的稅務效率，未直接回應股利問題
- SNDK_Q4_2026_Earnings_Call_20260805.md｜問：Schneider：是否在與已簽之外的大型雲端業者談新協議？｜答法：拒絕揭露個別合約細節，改談關係長期性
- SNDK_Q4_2026_Earnings_Call_20260805.md｜問：Muse：價格上漲但為何毛利率財測較低？｜答法：CEO 先說「你已用第二題回答了第一題」，轉談 durability 與 NBM 結構，未直接解釋差異（CFO 後來由 Curtis 追問時才補組合與成本假設）
- SNDK_Q4_2026_Earnings_Call_20260805.md｜問：Newman：FQ4 量成長拆解與 Q1 財測偏輕的原因（量、價鎖定或保守）｜答法：給了 FQ4 1/3量、2/3價拆解，Q1 僅稱「modest price increases」，未回答是否保守
- SNDK_Q4_2026_Earnings_Call_20260805.md｜問：Mohan：2027 是否預期價格正常化？｜答法：未回答價格是否正常化，改談與市場同步成長、需求訊號，並稱「I don't know what more to say about it」
- SNDK_Q4_2026_Earnings_Call_20260805.md｜問：Rakers 代問：產業供需何時收斂、與三個月前看法差異？｜答法：未給時間點，改稱供需透過客戶與供應商對話匹配
- SNDK_Q4_2026_Earnings_Call_20260805.md｜問：Gibson：HBF 樣品多久出現（1、2、3 年）？｜答法：未給時間，稱下週投資人日再說明
- SNDK_Q4_2026_Earnings_Call_20260805.md｜問：Rakesh：BiCS 10 與 HBF 是否有價格溢價？｜答法：稱定價評論為時尚早，未給數字
- SNDK_Analyst_Investor_Day_Sandisk_Corporation_20260813.md｜問：Newman 問 NBM 占比目標與 FY29 後是否維持三分之二｜答法：CFO 說會『隨時間優化』、與 FY28 數字『一致』但『會持續演變』，未給長期目標占比
- SNDK_Analyst_Investor_Day_Sandisk_Corporation_20260813.md｜問：Moore 問資料中心占比倍增後邊緣業務是否被擠壓、供給不足如何平衡｜答法：CEO 自稱『squishy answer』，以『know it when we see it』回應，未給占比數字
- SNDK_Analyst_Investor_Day_Sandisk_Corporation_20260813.md｜問：Reitzes 問 HBF 若成功，模型要放掉什麼、上檔怎麼算｜答法：CEO 稱『not ready to go there just yet』，改談 NBM 與等一年看客戶需求
- SNDK_Analyst_Investor_Day_Sandisk_Corporation_20260813.md｜問：Rakers 問 HBF 量產後 CapEx／先進封裝資本密集度是否改變｜答法：CTO 表示『let's wait until next year』，改談生產力餘裕，未給資本密集度數字
- SNDK_Analyst_Investor_Day_Sandisk_Corporation_20260813.md｜問：Rakers／Mizuho 問 HBF 定價與資本密集度｜答法：CTO 回『I feel it's priceless』，未給定價；資本密集度改以 27% 生產力餘裕回應
- SNDK_Analyst_Investor_Day_Sandisk_Corporation_20260813.md｜問：Muse 問 NBM 下年度成本下降是否與客戶分享｜答法：CFO 稱『not going to get into pricing in more detail』，只重申底價約 80% 毛利率
- SNDK_Analyst_Investor_Day_Sandisk_Corporation_20260813.md｜問：Feldman 問 BiCS9 及後續 NAND 成本下降幅度｜答法：CEO 表示已不談 cost down，成本下降屬公司，未給數字
- SNDK_Analyst_Investor_Day_Sandisk_Corporation_20260813.md｜問：CEO 追問 CFO 資本密集度承諾，CFO 答『low single digits』｜答法：簡報中 CFO 先前建模假設為『mid-single-digit』，此處口徑改為 low single digits，未說明差異
- SNDK_Analyst_Investor_Day_Sandisk_Corporation_20260813.md｜問：Mohan 問為何本次 NBM 在下行週期會比過去更撐得住、客戶預測能力是否更好｜答法：CEO 以『有信心改變結果』『最可能的結果』回應，未直接回答客戶預測能力，並承認『Maybe not』『no guarantees』
- SNDK_Analyst_Investor_Day_Sandisk_Corporation_20260813.md｜問：Unknown Analyst 問邊緣客戶去庫存與非資料中心需求展望｜答法：CFO 稱『I just can't get into too much details』，未談去庫存，只說物理 AI 有潛力
- SNDK_Analyst_Investor_Day_Sandisk_Corporation_20260813.md｜問：Schneider 問減少 HBM 後需要多少 eSSD／HBF 內容｜答法：CPO 稱視工作負載、『Now could it be reduced by half, one it depends』，未給容量數字

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 2 | 2 |
| customer_second_source | found | 1 | 2 |
| customer_concentration_credit | found | 2 | 0 |
| supply_demand_durability | found | 4 | 2 |
| regulatory_antitrust | found | 2 | 3 |
| reg_tariff_export | found | 3 | 2 |
| geo_supply_chain | found | 4 | 3 |
| end_markets | found | 3 | 3 |
| substitute_technology | found | 3 | 2 |
| channel_business_model_shift | found | 3 | 2 |
| capital_markets_pricing | found | 5 | 4 |
| major_events | found | 3 | 4 |
| cyclical_supply_discipline_capacity | found | 6 | 3 |
| cyclical_inventory_price_position | found | 5 | 2 |
| cyclical_prior_downcycle_behavior | found | 3 | 3 |

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260815","verdict":"觀望","role":"追蹤","H":{"status":"ok","format":"text","text":"核心假設 H1/H2/H3\n\nH1（升級版）：NBM floor 真實可執行，覆蓋範圍已擴大到FY27過半、FY28約2/3位元——RPO $59.8B（含季後協議 $91.1B）、財務擔保 $16.5B、8個客戶（較4月的5個再增3個）。門檻：RPO淨額不下修、財務擔保不縮水。來源：FY26 Q4 法說（2026-08-05）+ Investor Day（2026-08-13）。漂移觸發（較8/6版本強化）：覆蓋率從「FY27過半」進一步升至「FY28約2/3位元」，管理層明言「還在深度對話中」——H1可信度較上版邊際提升，但仍是合約不是護城河（見下方相依性註記）。\nH2（沿用）：AI/資料中心把NAND需求基底從PC+手機換成伺服器+推論耗材，使through-cycle正規化盈餘台階抬升。門檻：資料中心>40%位元需求。現況：Q4 FY26資料中心占營收33.2%（$2.977B/$8.965B）、占bits 38%（較去年同期12%）。Investor Day進一步預告CY2026資料中心占TAM~50%（去年僅~30%）。來源：SanDisk FY26 Q4法說、Investor Day。\nH3（本版更新）：正規化盈餘力估計自$95上修至約$105-115/股（NBM覆蓋率實質擴大的直接推論），through-cycle倍數同步自12-13倍略上修至12.5-13.5倍（反映合約段可見度真實提升，但不到賣方Goldman 20倍）。分子$110（中值）vs Goldman $110（本次巧合持平，方法論仍完全獨立）；倍數13倍vs Goldman 20倍。來源：本報告§10.7自建。\n相依性註記（沿用）：H1與H3不獨立——若NBM floor在下一輪谷底被重議（2017年記憶體長約在崩盤中曾被重議回現貨的先例），正規化盈餘力立刻退回接近FY23形狀（GAAP虧損、售價/成本比逼近1）。機率處理（本版與§10.5情境樹統一為單一組，獨立覆核後修正）：「floors大致守住」Bull 20%/Base 40%；「floors被重議」Bear **40%**（較8/6版本30%**上修**，理由並非NBM本身轉弱，而是本輪新查證到的供給端證據——Kioxia規劃FY2029前wafer產能翻倍、FY26-28年均capex較FY25+66%、四日市/北上現稼動率僅約50%〔大量待裝機空殼產能〕、Samsung V10已排定2026-10全面量產、YMTC全球位元份額已達14%〔全球第三〕——這些是供給側而非NBM條款本身的風險，但供給過剩仍會透過「非NBM段現貨價格轉弱」間接壓迫NBM段外的營收與整體估值倍數，故Bear機率上修並非否定NBM，而是承認NBM保護不了公司的全部）。"},"R":{"status":"unavailable"},"single_thing":null,"kill_metrics":null,"rearm_trigger":"股價回落至正規化盈餘力估值(約$1,485，12.5-13.5x normalized EPS $110-120)以下，或NBM覆蓋率/RPO淨額出現趨勢反轉前維持觀望；NAND合約價連2季QoQ轉負則改列迴避評估。","irr_base_pct":1.3,"ev5y_pct":-9.8,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"追蹤","signal":"C","val":"🟠","ma":"-","trap":"🟡","moat_trend":"→","runway_post_y5":"🟡","asym_ratio":0.6,"ev5y_pct":-9.8,"irr_base_pct":1.3,"max_dd_pct":-78.0,"bull_5y_price":3200.0,"bear_5y_price":350.0,"p_bull_pct":20.0,"p_bear_pct":40.0,"rearm_trigger":"股價回落至正規化盈餘力估值(約$1,485，12.5-13.5x normalized EPS $110-120)以下，或NBM覆蓋率/RPO淨額出現趨勢反轉前維持觀望；NAND合約價連2季QoQ轉負則改列迴避評估。","price_at_dd":1641.11,"archetype":"循環/商品","cycle_position":"晚循環"}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"SNDK","date":"2026-11-02","schema":"v15.0","contract":"v19","company_name":"Sandisk Corporation"},"oneliner":"AI 資料中心把 NAND 毛利率推到 85%，長約鎖住約三分之二 FY2028 位元；股價自八月跌三成後，以正常化盈餘看已屬合理。但週期位置偏晚，長約地板價也還沒經過下行檢驗，要等第一個合約價下跌季驗證後才談進場","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/SNDK_20261102/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/SNDK_20261102/scenario.json","answers":{"q1_business":{"verdict":"公司賺的是 AI 資料中心、手機與 PC 廠的 NAND 錢，錢卡在晶圓供給這一節點：幾乎全部晶圓來自與 Kioxia 的合資廠，缺貨期誰握有晶圓，誰就拿走利潤池。Q1 FY2027 非 GAAP 毛利率 85.1%、營業利益率 80.4%。","reasoning":"Q1 FY2027 營收 110.31 億美元，季增 23%、年增 378%，超過財測上緣 108 億美元。分部（逐字稿 2026-10-29 CFO）：資料中心 48 億美元，占 43.5%，季增 61%；邊緣 58 億美元，占 52.6%，季增 7%，低階手機萎縮，車用與 IoT 成長；消費 3.97 億美元，占 3.6%，季減 29%。營收成長約六成來自位元量、四成來自價格。非 GAAP 營業利益 88.71 億美元（80.4%），GAAP 營業利益 87.80 億美元（79.6%），自由現金流 63.09 億美元，占營收 57.2%。Q2 財測營收 122–126 億美元、非 GAAP 毛利率 84.5–85.5%、拆股前每股盈餘 55–57 美元。單點依賴兩頭都有：上游幾乎全部晶圓來自 Flash Ventures，合約限制公司另找貨源；下游前十大客戶占 44%，沒有單一客戶超過 10%，長約客戶 8 家，含 3 家美國超大規模雲端業者。產業時鐘判在第三階段（過熱），依據是基本面而非股價：毛利率創歷史新高、消費端提價後量縮、十月晶圓合約價停漲進入高檔平台。供需持久性判為週期性將反轉，長約只能緩衝一部分。","fact_refs":["f_kpi0_revenue_gaap","f_kpi1_non_gaap_operating_incom","f_kpi2_gaap_operating_income_ma","f_kpi3_free_cash_flow","f_kpi5_guidance_q2_fy2027_reven","f_earnings_recency","f_peer_sndk_gross_margin_pct"],"verdict_values":{"revenue_quality":"量價並進：Q1 FY2027 營收季增 23%，約六成來自位元量、四成來自價格（前一季是三分之一量、三分之二價）。FY2027 約一半、FY2028 約三分之二位元在多年長約下，附地板價與 165 億美元財務保證，品質比現貨好，但地板還沒經過下行檢驗。","unit_econ_note":"非 GAAP 營業費用 5.13 億美元，占營收 4.7%；毛資本支出 3.78 億美元，占營收 3.4%，產能投資由與 Kioxia 的合資廠分攤；增量營收幾乎全數落到營業利益。地板價下的長約毛利率約 80%（2026-08-13 投資人日 CFO）。","archetype":{"primary":"循環/商品","secondary":null,"confidence":"高","fingerprint":"NAND 記憶體廠；近四個會計年度有三年 GAAP 虧損；年度毛利率從 7.1% 擺到 71.5%（單季 85.1%）；營收主要由位元價格驅動"},"industry":{"clock_phase":"III","sd_verdict_source":"週期性將反轉，部分被長約緩衝：TrendForce 預估 2026 年缺口 4–5%，2027 年位元供給成長超過需求、下半年轉鬆，主要增量來自中國新廠。反方證據是海外新廠 2028 年後才放量，三星與 SK hynix 也在限制 NAND 投資。","bargaining":{"up":"上游幾乎全部晶圓來自 Flash Ventures（與 Kioxia 合資），合約限制改變產出或另找貨源，對供給端議價權低，屬單點依賴；合資已延長到 2034 年底，公司為此支付 11.65 億美元製造服務費。","down":"前十大客戶占營收 44%（FY2025 為 40%），沒有單一客戶超過 10%，客戶有多家供應商可選。缺貨期由公司定價，供給轉鬆後議價權會回到客戶手上。長約客戶 8 家，95% 為投資等級。","geo":"國際銷售占 82%，產品幾乎全在海外生產；美國 232、301 調查若取消現有關稅豁免，會直接壓縮毛利。"},"profit_pool_dir":"利潤池從消費與手機移向 AI 資料中心：資料中心占公司營收由 FY2025 的 13%，升到 FY2026 的 25%、Q1 FY2027 的 43.5%；消費占比降到 3.6%。","tam_table":[{"item":"NAND 產業營收（管理層估，含中國）","value":"CY2026 超過 3,000 億美元、年增約 3 倍；CY2027 接近 5,000 億美元（2026-08-05 CFO；管理層澄清這不是營收預測）"},{"item":"資料中心占產業位元","value":"本十年初約 20%，目前約一半；公司預估 CY2027 超過 55%（2026-10-29 CFO）"},{"item":"AI 資料中心占 NAND 需求（TrendForce）","value":"2026 年 44%、2027 年 51%"},{"item":"資料中心位元需求成長","value":"CY2026 倍增以上，CY2027 約年增 40%（公司）"},{"item":"KV cache 占 AI 資料中心 flash","value":"本十年末約三分之一（公司）；2030 年 35%（投資人日）"},{"item":"公司資料中心占營收","value":"FY2025 13%、FY2026 25%、Q1 FY2027 43.5%"},{"item":"營業利益池占比 5 年前→現在","value":"事實表未涵蓋各環節營業利益池"}]}}},"q2_moat":{"verdict":"護城河 C 級，方向持平。成本與技術執行在進步（資料中心營收一年成長 17 倍、BiCS8 CBA 架構），但定價權來自缺貨與長約，不是結構性的；營收市占季減 2 個百分點、中國對手上升，所以不能判為擴大。","reasoning":"機制是成本與技術執行，加上多年長約。技術面靠 BiCS8 的 CBA 架構支撐資料中心效能；公司在投資人日稱資本效率約為最近對手的 2 倍（2026-08-13 技術長，公司自述，未經第三方驗證）。長約平均超過 4 年，附 165 億美元財務保證，把一半到三分之二的位元轉成有地板價的合約。同業對照（TTM）：毛利率 76.8%，低於美光 80.7%，與 SK hynix 76.3% 相當，高於三星 57.5%；營業利益率 68.4%，美光 74.6%、SK hynix 68.0%；自由現金流率 61.6% 是同業最高，原因是資本支出由合資廠分攤。公司不是利潤率領先者；同業投入資本與 ROIC 事實表未涵蓋，算不出 ROIC 差距。執行力 7 分：近六次財測五次上修，資料中心營收一年成長 17 倍，QLC 平台已過認證放量。定價權 5 分：價格由產業供需決定，長約地板只保護部分位元，供給轉鬆後議價權回到客戶。方向持平：執行面在擴大，份額面在縮減（Counterpoint 2026 Q2 營收市占 11%，季減 2 個百分點），兩者相抵。產業態勢是雙向拉鋸：競爭面惡化（YMTC 份額一年升 6 個百分點，TrendForce 預估 2027 下半年供給轉鬆），結構面轉好（資料中心占產業位元約一半，長約成為主要交易方式），其他結構變數是美國 232、301 關稅調查。報酬持續期方面，當期報酬率高，但來自缺貨價格而非新增投入資本；四項檢查中決策層級與價值鏈分配為黃燈，不能把 85% 毛利率當成可延續的水準。","fact_refs":["f_peer_sndk_gross_margin_pct","f_peer_sndk_operating_margin_pct","f_peer_sndk_fcf_margin_pct","f_peer_mu_gross_margin_pct","f_peer_mu_operating_margin_pct","f_peer_mu_fcf_margin_pct","f_peer_000660_ks_gross_margin_pct","f_peer_000660_ks_operating_margin_pct","f_peer_000660_ks_fcf_margin_pct","f_peer_005930_ks_gross_margin_pct","f_peer_005930_ks_operating_margin_pct","f_peer_005930_ks_fcf_margin_pct","f_peer_wdc_gross_margin_pct","f_peer_wdc_operating_margin_pct","f_peer_wdc_fcf_margin_pct"],"verdict_values":{"moat":{"mechanism":"成本與製程執行（BiCS8 CBA、合資廠分攤資本支出），加上多年長約的地板價；兩者都受產業供需約束，不是結構性定價權","execution":7,"pricing":5,"grade":"C","trend":"→","trend_evidence":"執行面擴大：資料中心營收 48 億美元，季增 61%，高於市場；QLC 平台已通過認證放量。份額面縮減：Counterpoint 2026 Q2 營收市占 11%，季減 2 個百分點；YMTC 一年內由 8% 升到 14%。兩者相抵，判持平。","competitor_notes":[{"name":"MU","strategy_note":"TTM 毛利率 80.7%、營業利益率 74.6%，都高於本公司，靠 DRAM 與 HBM 撐高組合；同時把部分 NAND 產能轉去 DRAM，對 NAND 供給是利多"},{"name":"000660.KS","strategy_note":"毛利率 76.3%，與本公司相當；和本公司合推 HBF 規格，同時是 NAND 大廠，大連二廠是 2026 下半年到 2028 年的主要新增產能之一"},{"name":"005930.KS","strategy_note":"毛利率 57.5%、營業利益率 36.9%，NAND 營收市占第一（28%）；報導指其限制 NAND 投資、轉向 HBM，能否持續是供給紀律的關鍵"},{"name":"WDC","strategy_note":"已是純硬碟公司，毛利率 52.6%；不直接競爭 NAND，但在資料中心容量層與 QLC SSD 互相替代"},{"name":"YMTC","strategy_note":"未上市，財務事實表未涵蓋；營收市占由 2025 Q1 的 8% 升到 2026 Q2 的 14%，是本輪份額成長最快的對手"},{"name":"Kioxia","strategy_note":"既是合資夥伴也是對手，市占 14%；FY2026–28 年均資本支出比 FY2025 多 66%，但仍比 FY2023 高峰低約 10%"}],"peer_na_reason":"YMTC、Kioxia 不在同業財務表內；同業投入資本與 ROIC 事實表未涵蓋，只能比較利潤率","threats":[{"level":"🔴","text":"中國產能擴張（YMTC 三廠、SK hynix 大連二廠）是 2026 下半年到 2028 年的主要新增供給，YMTC 份額一年升 6 個百分點，屬破壞性價格競爭","p":"35%","evidence_refs":["competitive_share_entrants#1","supply_demand_durability#0","cyclical_supply_discipline_capacity#0"]},{"level":"🟡","text":"客戶有多家供應商可選，前十大客戶占營收 44% 且比重上升；供給轉鬆後客戶會用替代來源壓價","p":"30%","evidence_refs":["customer_second_source#0"]},{"level":"🟡","text":"10-K 列出可能降低每單位 AI 運算儲存需求的新技術；三星與 Kioxia 的 XL-Flash、Z-NAND 走另一條路線，目前沒有具名的替代技術","p":"10%","evidence_refs":["substitute_technology#0"]},{"level":"🟡","text":"幾乎全部晶圓來自與 Kioxia 的合資廠，產能集中在日本，合約限制另找貨源","p":"10%","evidence_refs":["geo_supply_chain#0"]}],"roic_durability":{"quadrant":"高利益率×高周轉（推斷：投入資本事實表未涵蓋；TTM 營業利益率 68.4%，資本支出只占營收 3.4%，營收一年成長 175%）","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者是 AI 推論服務，決策者是雲端業者的架構團隊，付款者是長約客戶：95% 為投資等級，合計營業現金流約 1,300 億美元（2026-10-29 CFO）。推論的 KV cache 是剛需，CY2027 資料中心位元需求約年增 40%。消費端例外：提價後營收季減 29%，那一塊是可延後的需求。"},{"item":"決策層級","level":"🟡","text":"客戶在 SSD 平台層做決策，換供應商要重新認證（QLC 平台認證就花了數季），長約平均超過 4 年，短期轉換成本存在。但 10-K 自述前十大客戶有多家供應商可選、可以提出大量要求，市場上有五家以上垂直整合廠可替代，下一輪續約時替代性會回升。"},{"item":"價值鏈分配","level":"🟡","text":"缺貨期利潤池集中在握有晶圓的記憶體廠，毛利率 85%；下游 PC 與手機廠被擠壓（消費營收季減 29%，分析師在電話會提到 Intel 因記憶體成本下修財測）。這是供給稀缺下的暫時分配，2027 下半年供給轉鬆後會部分回吐。資料中心客戶的儲存成本占 AI 資本支出比重小，較能吸收漲價。"},{"item":"社會容忍度","level":"🟡","text":"沒有價格管制，也不依賴監管授權；風險在貿易政治：國際銷售占 82%，產品幾乎全在海外生產，美國 232、301 調查可能取消現有關稅豁免，中國產能擴張也帶政策色彩。目前沒看到針對記憶體價格的監管討論。"}],"roiic":"事實表未涵蓋投入資本，算不出增量報酬率。FY2025→FY2026 營業利益由約 5 億增到約 125 億美元，同期毛資本支出只占營收個位數，增量利潤幾乎全部來自價格而非新投入資本，不能外推為可再投資的報酬","reinvest_rate":"低：FY2027 毛資本支出指引為營收的中個位數百分比，對比約 80% 的營業利益率，再投資率估計不到一成；超額現金 100% 回購（折舊攤銷與營運資金變動事實表未涵蓋）","endo_ceiling":15,"formula_note":"公式本應是增量報酬率×再投資率，但缺投入資本資料；改以公司承諾的位元成長中到高十位數（約 15%）作為量的內生上限，價格不計入"}}}},"q3_growth":{"verdict":"成長跑道中等：資料中心位元需求仍在高成長，但公司的位元成長被產能限制在每年中到高十位數，未來兩年的盈餘成長幾乎全靠價格。HBF 可能成為第二曲線，但還沒進營收模型。","reasoning":"成長來源是量價並進：Q1 量約六成、價約四成。公司承諾位元供給每年成長中到高十位數，靠製程轉換而不是加晶圓（2026-08-05 執行長），所以 FY2027 之後的盈餘成長主要看價格與回購。共識每股盈餘 FY2027 226.74、FY2028 274.64、FY2029 256.77 美元；共識營收 FY2027 493.8 億、FY2028 603.6 億美元。以 FY2026 GAAP 每股盈餘 73.76 美元為基期，三年 CAGR 約 51.6%，遠高於以位元成長推得的內生上限約 15%。約 36.6 個百分點的缺口來自毛利率擴張（價格）加上淨回購（兩季回購約 4% 股數），不是再投資，可以歸因。共識本身已預期 FY2029 盈餘比 FY2028 下滑，FY2027→FY2029 年化只有 6.4%。跑道方面，資料中心占產業位元約一半，AI 資料中心占 NAND 需求 2027 年達 51%（TrendForce），KV cache 與 SLC 等新用途在擴大；HBF 已 tape-out、預計 2027 年送樣，但公司明說沒納入長期模型，還不算已證實的第二曲線，因此五年後跑道判中等。衰退訊號亮兩項（營收市占縮減、每股盈餘成長遠快於營收）；消費端提價後量縮，因屬非主力產品不計入。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_fy1_pct","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m"],"verdict_values":{"growth":{"driver_mix":"量價並進：Q1 FY2027 量約六成、價約四成；位元供給承諾每年中到高十位數，靠製程轉換而非加晶圓；FY2027 以後價格貢獻轉為溫和。每季 50 億美元回購若持續，以現價推算每年可減少約一成股數","runway_years":"5–9","runway_post_y5":"🟡","endo_ceiling_basis":"引用護城河段的報酬持續期：以位元成長中到高十位數（約 15%）作為量的內生上限；缺投入資本資料，增量報酬率×再投資率無法計算，價格不計入","segments":[{"item":"資料中心","value":"Q1 FY2027 營收 48 億美元（43.5%），季增 61%；FY2026 為 51.53 億美元，年增 437%"},{"item":"邊緣（手機、PC、車用、IoT）","value":"Q1 FY2027 營收 58 億美元（52.6%），季增 7%；低階手機萎縮，車用與 IoT 成長；FY2026 為 121.6 億美元，年增 195%"},{"item":"消費","value":"Q1 FY2027 營收 3.97 億美元（3.6%），季減 29%，前一季也季減 32%，高價壓抑需求；FY2026 為 29.35 億美元"}],"decay_signals":[{"signal":"毛利率連兩季年減","lit":false,"note":"非 GAAP 毛利率 85.1%，仍在連續擴張"},{"signal":"核心市占近 12 個月縮減","lit":true,"note":"Counterpoint 2026 Q2 營收市占 11%，季減 2 個百分點；YMTC 一年內由 8% 升到 14%"},{"signal":"主力產品提價後銷量下滑","lit":false,"note":"消費營收提價後季減 29%，但只占 3.6%，不是主力產品"},{"signal":"每股盈餘成長顯著高於營收成長","lit":true,"note":"FY2026 營收成長 175%，每股盈餘由虧損轉為 73.76 美元，盈餘成長來自價格推升毛利率"},{"signal":"自由現金流對淨利連兩年低於 0.75","lit":false,"note":"FY2026 約 1.0 倍"},{"signal":"SBC 占營收超過 5% 且上升","lit":false,"note":"0.8%"},{"signal":"TAM 萎縮或被替代技術壓縮","lit":false,"note":"資料中心需求在擴大；10-K 列有替代技術風險，但沒有具名技術"},{"signal":"產業估值倍數近三年系統性下移","lit":null,"note":"事實表未涵蓋產業倍數序列"},{"signal":"維護性資本支出占自由現金流超過 60%","lit":false,"note":"資本支出約占營收 3.4%"},{"signal":"停止投資新產能且營收三年內下滑","lit":false,"note":"位元成長維持中到高十位數"}],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"資本配置紀律清楚：無負債、超額現金 100% 回購、SBC 不到營收 1%。疑慮在於週期高點用高價買回，本季回購均價比現價高 36%。","reasoning":"自由現金流對淨利的轉換：FY2026 自由現金流 114.94 億美元，淨利 114.33 億美元，約 1.0 倍；Q1 FY2027 自由現金流 63.09 億美元（公司調整後口徑 57 億美元，排除長約預付款）。SBC 9,100 萬美元，占營收 0.8%。資本支出 3.78 億美元，占營收 3.4%，FY2027 指引為中個位數百分比。現金去向：本季回購 50 億美元（約 320 萬股，均價約 1,562 美元），不發股利，無負債（定期貸款已清償），季末現金 51 億美元。另外 FY2026 有南亞科 10 億美元的策略持股，以及延長 Kioxia 合資的 11.65 億美元製造服務費。董事會八月再授權 140 億美元，合計授權 155 億美元，扣掉本季 50 億美元後約剩 105 億美元（推算）。信評 BB+。","fact_refs":["f_kpi3_free_cash_flow","f_kpi4_sbc_gaap","f_net_debt_m","f_shares_diluted_m","f_price_at_dd"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":false,"passed":null,"input":"近一年沒有併購；南亞科約 3.9% 股權（10 億美元）屬策略持股，投資人日稱已認列約 8 億美元收益，Q1 FY2027 另認列 5.13 億美元權益證券收益（主要來自南亞科），不屬於併購報酬"},{"name":"buyback_yield","applicable":true,"passed":true,"input":"Q1 FY2027 回購約 320 萬股、50 億美元，均價約 1,562 美元。以 FY1 共識每股盈餘 226.74 美元計，回購收益率約 14.5%；以正常化每股盈餘 110 美元計約 7.0%。10 年期公債殖利率事實表未涵蓋；以當期盈餘口徑判通過，正常化口徑則接近門檻"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"SBC 9,100 萬美元，占營收 0.8%、占 GAAP 營業利益 1.0%；兩季回購約 600 萬股、約 4% 流通股，淨稀釋為負"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購；資本回報以回購為主，政策是超額現金 100% 回購、不發股利、維持無負債，細節已寫在計分卡三項"}}}},"q5_valuation":{"verdict":"現價隱含的是盈餘在 FY2029 之後腰斬、回到舊週期形狀；以正常化盈餘看落在合理區，表面上的便宜只是高峰盈餘造成的錯覺。我信一半：長約讓下行比 FY2023 淺，但地板價還沒經過考驗。","reasoning":"現價隱含什麼：FY2027–28 共識每股盈餘合計 501.38 美元，扣掉兩年正常化盈餘 220 美元，超出正常水準的部分約 281 美元。現價減去這段後約 870 美元，只有正常化每股盈餘 110 美元的 7.9 倍；換個說法，等於市場用 12 倍在算每股約 72 美元的長期盈餘，接近舊週期形狀，完全沒給長約溢價。我信一半：長約有財務保證，客戶也是投資等級，谷底應比 FY2023 淺；但地板價沒經過任何一次下行，市場的懷疑有道理。共識方面，FY1 近三個月 +240% 是財年切換造成的（推論：七月底快照的 FY1 仍是 FY2026，已知三季非 GAAP 每股盈餘 1.22、23.41、39.25 美元合計 63.88 美元，加上未揭露的一季正好與快照的 66.68 美元相符）；真實修正是 FY1 +5.55%、FY2 +3.13%、FY3 0%。FY1 共識營收 493.8 億美元，要求下半年每季約 130 億美元，而管理層提醒第三季通常最弱，共識偏滿。賣方目標價：FN2 列出 1,400–3,250 美元，最高與最低相差 2.3 倍；MarketBeat 七月平均 1,811 美元。本研究的 12 個月合理價 1,320 美元（+14.7%），五年基準情境 1,750 美元（+52.1%）。淨現金 50 億美元，EV 1,587.5 億美元，forward EV/S 3.22 倍。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_pe_current","f_pe_percentile","f_ps_current","f_ps_percentile","f_ev_s_current","f_ev_s_percentile","f_ev_s_fwd","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_fy1_pct","f_consensus_rev_fy2_pct","f_consensus_rev_fy3_pct","f_consensus_rev_3m_fy1_pct","f_rev_consensus_fy1_m","f_net_debt_m","f_ev_m","f_week26_return_pct","f_rsi14","f_ma_state","f_ma_w52"],"verdict_values":{"valuation":{"basis":"以正常化盈餘×穿越週期本益比為主（每股約 110 美元×12–13.5 倍），forward 本益比只作對照","tier":"記憶體循環股","peers":{"expanded":false,"reason":"事實表的同業對照只有利潤率，沒有同業本益比或股價淨值比，無法列同業倍數；終端倍數以自身現值與前份正常化倍數為錨，同業倍數缺口已在情境基準中註明"},"fwd_pe":5.08,"peg":0.79,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"現價 1,150.89 美元；正常化估值＝每股約 110 美元×12–13.5 倍＝1,320–1,485 美元，現價約為其 78–87%。forward 5.1 倍、trailing 9.2 倍都建在 85% 的高峰毛利率上，分母有爭議，便宜論證不能單獨成立。PEG：以 FY2026 GAAP 為基期的三年 CAGR 51.6% 算得約 0.1，失真；以 FY2027→FY2029 共識年化 6.4% 算得 0.79。五年分位：交易歷史不到兩年，週線兩年均線都算不出來，沒有五年本益比序列（P/S 只有 4 個年度端點，分位 38.6），不填。合看落在合理區。","upside_short_pct":14.7,"upside_mid_pct":52.1,"denominator_disputed":true,"denominator_note":"FY1 每股盈餘 226.74 美元建在 85% 的毛利率上，而過去四個會計年度的年度毛利率在 7.1% 到 71.5% 之間；低本益比來自高峰分母，便宜論證不成立，改用每股約 110 美元的正常化盈餘"}}},"q6_how_wrong":{"verdict":"最可能看錯的地方是長約地板價：若下行期客戶要求重議而公司讓步，正常化盈餘會回到舊週期水準，現價就不便宜。","reasoning":"依據見反證紀錄。最可能的看錯路徑是 2027 下半年供給轉鬆，加上長約地板被重議，五年後股價落在 400–600 美元。衰退訊號亮兩項（營收市占縮減、每股盈餘成長遠快於營收），陷阱風險中等。最大回撤推估 −45%～−65%，起點 1,150.89 美元。","fact_refs":["f_price_at_dd","f_week26_return_pct","f_rsi14"],"verdict_values":{"trap":{"verdict":"🟡","label":"高峰盈餘下的低本益比，陷阱風險中等"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":226.74,"pe":5.08,"basis":"FY1（FY2027，約 2027 年 6 月底結束）共識非 GAAP 每股盈餘，拆股前口徑；終端倍數同樣套在當年度每股盈餘上"},"eps":{"bull":[230,285,310,330,350],"base":[218,240,185,150,175],"bear":[205,150,60,35,60]},"pe":{"bull":11,"base":10,"bear":10},"p":{"bull":20,"base":45,"bear":35},"yield_pct":{"dividend":0,"net_buyback":0},"second_stage":{"bull_cagr_pct":10,"base_cagr_pct":5},"max_dd":{"lo":-65,"hi":-45,"basis":"起點 1,150.89 美元。上一輪下行營收跌 38%、每 GB 售價跌 39%、毛利率由 33% 跌到 7%；記憶體前兩輪下行，毛利率谷底都持續 7–9 季。空頭路徑 FY2030 每股盈餘 35 美元，谷底年本益比 12–15 倍，得 420–525 美元（−54%～−64%）；若長約地板守住約一半，谷底約 630 美元（−45%）。範圍取 −45%～−65%，與前份推估的谷底價位約 360 美元屬同一區間。","trigger_time":null},"basis":{"bull":"長約地板守住並續約，資料中心位元需求每年成長 30–40%，吸收中國新產能；毛利率維持在公司 2028–2030 長期模型的約 80%，每年回購約一成股數。11 倍反映週期性降低","base":"2027 下半年供給轉鬆，非長約位元價格下跌，長約地板大致守住；FY2029–30 毛利率回落到 55–65%，FY2031 隨續約回升。FY2027 略低於共識，因為第三季季節性最弱。回購已反映在每股盈餘，殖利率不另計。10 倍介於現值 trailing 9.2 倍與前份正常化 12.5–13.5 倍之間（同業本益比事實表未涵蓋）","bear":"2027 下半年供給轉為過剩，現貨價格跌四到五成，客戶在下行期迫使重議地板價；FY2030 毛利率跌到 30% 上下，但不至於回到 FY2023 的 7%。10 倍取成長熄火降到 10% 時的情境倍數"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"TrendForce 預估 2027 年位元供給成長超過需求、下半年轉鬆，增量主要來自中國新廠；十月晶圓合約價停漲，模組廠庫存上升。上一輪下行營收跌 38%、每 GB 售價跌 39%、毛利率由 33% 跌到 7%，記憶體下行毛利率谷底持續 7–9 季。客戶有多家供應商可選，前十大占營收 44%","assumption":"長約地板價在現貨下跌時仍可執行","consequence":"地板被重議後，FY2030 每股盈餘約 35 美元，谷底股價 420–525 美元，五年後約 600 美元，虧損近半","ruling":"採納，列為空頭情境，機率 35%。與唯一致命點部分重疊：唯一致命點是觸發事件，本條是完整的下行路徑，已把供給端條件補進空頭路徑","watch":"TrendForce 合約價季變動；每季剩餘履約義務","not_applicable_reason":null,"evidence_refs":["supply_demand_durability#0","cyclical_supply_discipline_capacity#0","cyclical_inventory_price_position#3","cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#1","cyclical_prior_downcycle_behavior#2","customer_second_source#0"],"fact_refs":["f_consensus_eps_fy3","f_price_at_dd"]},{"view":"論點成功但股東經濟變差","evidence":"Q1 回購約 320 萬股、花 50 億美元，均價約 1,562 美元，比現價高 36%；政策是超額現金 100% 回購，等於在週期高點買得最多。應收帳款三家客戶占 41%（前一年只有一家占 11%），淨額 47 億美元。關稅豁免若取消，會直接壓縮毛利","assumption":"回購能創造每股價值","consequence":"即使長約守住、盈餘維持高檔，若高峰期把數百億美元現金用在高於正常化價值的價位回購，股東實得報酬會低於每股盈餘成長","ruling":"部分採納：回購均價高於現價屬於已實現的價值流失，但公司無負債，也沒有舉債回購，傷害有上限。不改裁決，列入追蹤","watch":"每季回購均價對照下一季股價；下行期回購是否放緩；應收帳款集中度","not_applicable_reason":null,"evidence_refs":["customer_concentration_credit#1","reg_tariff_export#1"],"fact_refs":["f_kpi3_free_cash_flow","f_shares_diluted_m","f_price_at_dd"]},{"view":"價格已反映太多","evidence":"賣方 16 則評等中 87.5% 偏多、沒有偏空；FY1 共識近期再上修 5.55%；財報連續超預期","assumption":"市場仍在追逐高峰盈餘","consequence":"若好消息已全部反映，下一季財測只要持平，股價就會跌","ruling":"反駁：2026-08 財報超預期後股價反而下跌，八月中以來累計跌三成，26 週報酬 −3%，RSI 32.7，市場是在提前折現下行；forward 5.1 倍並沒有反映高峰盈餘會延續。真正的風險不是價格反映太多，而是分母本身是高峰值","watch":"股價對財報超預期的反應方向","not_applicable_reason":null,"evidence_refs":["capital_markets_pricing#0"],"fact_refs":["f_week26_return_pct","f_rsi14","f_fwd_pe_latest"]},{"view":"論點失敗","evidence":"10-K 風險因子載明：公司需求越來越依賴 NAND 在 AI 基礎設施的使用，可能出現降低每單位 AI 運算儲存需求的技術","assumption":"AI 推論架構會持續擴大 NAND 用量","consequence":"資料中心需求若被替代，H2 失效，正常化盈餘下移","ruling":"反駁為主要情境：目前沒有具名的替代技術，公司 HBF 與客戶的 SLC 需求反而在擴大 NAND 用途；保留為長期監測","watch":"資料中心營收季增率對照產業企業 SSD 營收","not_applicable_reason":null,"evidence_refs":["substitute_technology#0"],"fact_refs":[]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 - → 本次 -","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=-","side_b":"本次 ma=-","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 1641.11 → 本次 1150.89（-29.9%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=1641.11","side_b":"本次 price_at_dd=1150.89","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 1,641.11 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 1,641.11 美元：Bull 價 3,200、Bear 價 350，五年期望值 −9.8%，基準年化 1.3%，不對稱比 0.6","side_b":"本次情境、股價仍用 1,641.11 美元：Bull 價 3,850、Bear 價 600，五年期望值 +7.7%，基準年化 1.3%，不對稱比 1.21","ruling":"先換情境、股價不動：五年期望值多 17.5 個百分點，基準年化少 0.0 個百分點。不對稱比由 0.6 變為 1.21。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變好。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 1,641.11 美元：五年期望值 +7.7%，基準年化 1.3%，不對稱比 1.21","side_b":"本次情境、股價 1,150.89 美元：五年期望值 +53.6%，基準年化 8.7%，不對稱比 2.8","ruling":"再換股價、情境不動：起點價下跌 29.9%，五年期望值多 45.9 個百分點，基準年化多 7.4 個百分點，不對稱比由 1.21 升到 2.8。合計五年期望值比前份多 63.4 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"前份漂移：股價下跌三成","cause":"價格變動","prior_field":["val","max_dd_pct"],"side_a":"前份 2026-08-15：股價 1,641.11 美元，估值偏貴，裁決觀望，最大回撤 −78%","side_b":"本次股價 1,150.89 美元（−30%），FY1 共識每股盈餘 226.74 美元；估值改為合理，最大回撤 −45%～−65%","ruling":"估值結論由偏貴改為合理，主因是股價下跌，不是盈餘假設轉樂觀：正常化每股盈餘維持約 110 美元，倍數由 12.5–13.5 倍微調為 12–13.5 倍。最大回撤百分比縮小，但推估的谷底價位約 400–630 美元，與前份約 360 美元同一區間，差異來自起點較低。裁決與角色依本次輸入重算","evidence_level":"高：價格為收盤實值","settle_metric":"股價相對正常化估值 1,320–1,485 美元的位置","if_then":["若股價回到 1,485 美元以上，而長約尚未經過下行檢驗→估值改回偏貴，維持不進場","若股價跌破 900 美元，而合約價尚未轉跌→重算空頭情境，下檔已覆蓋大半時改為分批反買，首批 ≤1%"],"evidence_refs":[]},{"axis":"前份漂移：情境機率與路徑重建","cause":"方法變動","prior_field":["p_bull_pct","p_bear_pct"],"side_a":"前份：多頭 20%、基準 40%、空頭 40%；空頭定義為長約地板被重議","side_b":"本次：多頭 20%、基準 45%、空頭 35%；終端年改為 FY2031，回購效果直接反映在每股盈餘、殖利率不另計；空頭定義為 2027 下半年供給過剩加上地板重議","ruling":"空頭機率下調 5 個百分點：本季新揭露長約客戶 95% 為投資等級、合計營業現金流約 1,300 億美元，地板被全面推翻的機率略降。但 TrendForce 預估 2027 下半年轉鬆，共識三年成長率也高於內生上限，空頭仍維持 35%，不低於 30%","evidence_level":"中：長約條款未見原文，供需為第三方預估","settle_metric":"2027 下半年 NAND 合約價方向與同期剩餘履約義務","if_then":["若 2027 年第三季合約價季減，且剩餘履約義務因非出貨原因下修→空頭機率上調到 50%，持有者減碼一半","若到 2027 年底合約價仍未轉跌→空頭機率下調到 30%，重跑情境"],"evidence_refs":["supply_demand_durability#0"]},{"axis":"前份漂移：品質與週期判讀維持","cause":"新證據","prior_field":["signal","trap","moat_trend","runway_post_y5","archetype","cycle_position"],"side_a":"前份：綜合評等 C、陷阱風險中等、護城河方向持平、五年後跑道中等、循環／商品、晚循環","side_b":"本季新證據正反並陳。正面：Q1 營收 110 億美元超過財測上緣，Q2 財測 122–126 億美元，資料中心季增 61%。負面：營收市占季減 2 個百分點，十月晶圓合約價持平，消費營收季減 29%，TrendForce 預估 2027 下半年供給轉鬆","ruling":"六欄維持不變：盈餘仍在上升段，但價格動能已見平台，需求端出現價格彈性破壞，週期位置仍判晚循環；市占下滑使護城河方向不能上調","evidence_level":"中","settle_metric":"合約價季變動與營收市占","if_then":["若邊緣營收出現季減→週期位置改判過熱頂部，持有者減碼一半","若 2027 年上半年合約價仍季增且市占回升到 13% 以上→週期位置改判中循環，重跑研究"],"evidence_refs":["competitive_share_entrants#1","cyclical_inventory_price_position#3","supply_demand_durability#0"]},{"axis":"前份價格重啟線已觸發，改為事件重啟","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"股價回落至正規化盈餘力估值(約$1,485，12.5-13.5x normalized EPS $110-120)以下，或NBM覆蓋率/RPO淨額出現趨勢反轉前維持觀望；NAND合約價連2季QoQ轉負則改列迴避評估。","side_b":"NAND 合約價轉跌的第一個完整季，長約覆蓋率與剩餘履約義務未下修，且非 GAAP 毛利率守住 60% 以上","ruling":"前份價格重啟線已在本次觸發（1,150.89 美元低於 1,485 美元），因此不沿用前份結論，全部重判。但不據此進場，理由有二：一是循環股在高峰毛利率時的低價不等於便宜，正常化估值本身就有約兩成誤差；二是八月後新增的反向證據（市占下滑、合約價見平台、2027 下半年供給轉鬆的預估）讓地板價能否執行成為唯一關鍵。重啟改為事件條件：合約價轉跌時，長約要先通過一季檢驗。前份「合約價連兩季下跌改列迴避」的門檻保留，持有者觸發時減碼","evidence_level":"中","settle_metric":"合約價下跌季的剩餘履約義務與毛利率","if_then":["若重啟條件成立→重跑完整研究，通過才以 ≤3% 首倉起步","若合約價連兩季下跌，且毛利率跌破 60%→改列迴避，持有者清倉"],"evidence_refs":["cyclical_inventory_price_position#3","competitive_share_entrants#1","supply_demand_durability#0"]},{"axis":"Single Thing 新設","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設唯一致命點（空值）","side_b":"任一份多年長約在 NAND 合約價下跌期間被重議地板價、縮量或提前終止，且公司讓步","ruling":"前份把地板重議放在空頭機率裡，沒有單獨列出。本次依「敏感度最大」原則把它列為 Single Thing：長約涵蓋 FY2028 約三分之二位元，地板價決定正常化盈餘落在基準路徑還是空頭路徑。一旦發生即清倉","evidence_level":"中","settle_metric":"剩餘履約義務與地板價條款變動","if_then":["若任一地板價調降，或剩餘履約義務因非出貨原因季減超過 10%→清倉並改列迴避"],"evidence_refs":["customer_second_source#0"]},{"axis":"停損指標新設","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設停損指標（只在重啟條件附帶：NAND 合約價連 2 季 QoQ 轉負則改列迴避評估）","side_b":"本次設五項：合約價連兩季為負；剩餘履約義務非出貨原因季減超過 10%；長約覆蓋 ≥50% 時毛利率跌破 75%；營收市占連兩季低於 10%；資料中心占比在 FY2027 Q4 低於 40%","ruling":"前份唯一的合約價門檻保留不刪；新增四項，把地板價、市占、組合轉型拆成每季可驗證的數字。觸發剩餘履約義務或地板價條件即清倉，觸發其餘條件則減碼","evidence_level":"中","settle_metric":"每季財報與 TrendForce 合約價","if_then":["若剩餘履約義務或地板價條件觸發→清倉","若合約價、毛利率、市占、組合任一條件觸發→持有者減碼一半"],"evidence_refs":["supply_demand_durability#0","competitive_share_entrants#1"]},{"axis":"長約改變週期，還是 2027 下半年供給轉鬆","cause":null,"side_a":"公司說法：長約涵蓋 FY2027 約一半、FY2028 約三分之二位元，地板價下毛利率約 80%，財務保證 165 億美元，95% 客戶為投資等級；需求管線超過供給，一路到本十年末（2026-10-29 CFO Visoso）","side_b":"TrendForce：2027 年位元供給成長超過需求、下半年轉鬆，中國新廠是主要增量。上一輪下行營收跌 38%、毛利率跌到 7%；執行長在 2026-08-13 投資人日自承長約能否撐過下行「沒有保證」","ruling":"可調和，屬程度差異：兩件事可以同時成立，供給轉鬆後現貨價下跌，長約緩衝一半到三分之二位元。裁決時點採 B 側、幅度採 A 側：下行會來，但谷底毛利率會高於上一輪。據此，基準路徑 FY2029–30 每股盈餘降到 150–185 美元，而不是回到虧損","evidence_level":"中：長約條款未見原文，TrendForce 為預估","settle_metric":"2027 下半年合約價方向與同期剩餘履約義務","if_then":["若合約價連兩季下跌，而剩餘履約義務不降、毛利率 ≥60%→長約有效，重跑研究，允許以 ≤3% 首倉進場","若合約價下跌首季即出現地板價調降→清倉並改列迴避"],"evidence_refs":["supply_demand_durability#0","cyclical_supply_discipline_capacity#0","cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#2"]},{"axis":"Steelman：現在就買的最強論證","cause":null,"side_a":"forward 5.1 倍、淨現金 50 億美元、單季自由現金流 63 億美元、每季回購 50 億美元（約市值 3%）；長約鎖住約三分之二 FY2028 位元，地板毛利率約 80%；即使正常化每股盈餘只有 110 美元，現價也只有約 10.5 倍；列出的賣方目標價 1,400–3,250 美元全在現價之上","side_b":"高峰毛利率下的低本益比，是循環股最常見的陷阱；股價在財報超預期後兩個半月跌三成，市場已在折現 2027 下半年的轉折；地板價沒經過任何一次下行","ruling":"不進場。買進論證成立的前提是地板價可執行，這件事再等三到四季就能驗證。等待的代價是可能錯過一段回購推升的漲幅；不等的風險則是買在週期頂部。選擇等驗證","evidence_level":"中","settle_metric":"第一個合約價下跌季的長約表現","if_then":["若 2027 年上半年合約價仍季增，且長約覆蓋升破 75%→重跑研究，允許以 ≤3% 首倉進場","若股價跌破 900 美元，而合約價尚未轉跌→分批反買，首批 ≤1%"],"evidence_refs":[]},{"axis":"管理層承諾對帳","cause":null,"side_a":"2026-08-05 財測：Q1 營收 103–108 億美元、非 GAAP 每股盈餘 44–46 美元、營業費用 5.2–5.4 億美元；CFO 稱會再簽長約；執行長稱回購會維持一致節奏。投資人日 CFO 對資本密集度先說中個位數，問答時改說低個位數","side_b":"Q1 實績：營收 110.3 億美元、每股盈餘 49.51 美元、營業費用 5.13 億美元，全數優於財測；回購 50 億美元照計畫執行；本季重申 FY2027 資本支出為中個位數（實際 3.4%）。但本季新增長約為零（兩份已在八月宣布），長約仍為 8 家，覆蓋率仍是一半／三分之二","ruling":"財務財測兌現度高（近六次財測五次上修），可信度加分。長約擴張進度落後八月的說法，屬時點問題，不是方向逆轉，列入 H1 每季追蹤。資本密集度口徑不一，但金額小，不影響論點","evidence_level":"高：財報實值對照前次財測","settle_metric":"2027 年 1 月財報的新增長約家數","if_then":["若 2027 年 1 月財報仍無新長約→H1 擴張假設降級，基準情境 FY2029 每股盈餘下修一成"],"evidence_refs":[]},{"axis":"需求轉強，還是消費端價格彈性破壞","cause":null,"side_a":"CFO：客戶需求比上季更強；執行長：CY2027 每個 NAND 區塊的位元都會成長（2026-10-29）","side_b":"消費營收連兩季季減（29%、32%），模組廠庫存上升，PC 與手機單位量下滑；分析師在電話會提到 Intel 因記憶體成本下修財測","ruling":"可調和：資料中心的拉力遠大於消費端的流失（消費只占 3.6%），但這代表價格已逼近終端承受上限，支持晚循環的判斷","evidence_level":"中","settle_metric":"邊緣營收季變動","if_then":["若邊緣營收（占 52.6%）出現季減→週期位置改判過熱頂部，持有者減碼一半"],"evidence_refs":["cyclical_inventory_price_position#3"]},{"axis":"資料中心勝出，但整體營收市占下滑","cause":null,"side_a":"資料中心營收季增 61%，高於市場成長（CFO）","side_b":"Counterpoint：2026 Q2 營收市占 11%，季減 2 個百分點；YMTC 升到 14%","ruling":"可調和：公司把位元從消費與低階邊緣移往資料中心，整體市占下滑有一部分來自主動配置；但 YMTC 一年升 6 個百分點是真實的份額流失，護城河方向不能上調","evidence_level":"中：單一第三方來源","settle_metric":"Counterpoint／TrendForce 季度營收市占","if_then":["若營收市占連兩季低於 10%→護城河方向改判縮減，持有者減碼一半"],"evidence_refs":["competitive_share_entrants#1"]}],"triggers":[{"n":1,"text":"每季檢查長約覆蓋率與剩餘履約義務","type":"假設驗證","maps_to":"H1","metric":"長約占位元比（FY2027／FY2028）與剩餘履約義務","threshold":"FY2027 ≥50%、FY2028 ≥67%；剩餘履約義務非出貨原因季減 ≤10%","action":"連兩季低於門檻→H1 削弱，維持不進場；FY2028 覆蓋升破 75% 且新客戶仍為投資等級→H1 上修","source_freq":"每季財報、10-Q","date":"2027-01","evidence_refs":[]},{"n":2,"text":"資料中心占營收比是否持續上升","type":"假設驗證","maps_to":"H2","metric":"資料中心營收占比","threshold":"FY2027 Q4 ≥45%（Q1 為 43.5%）","action":"未達→正常化每股盈餘下修一成並重跑情境","source_freq":"每季財報","date":"2027-08","evidence_refs":[]},{"n":3,"text":"NAND 合約價轉跌","type":"風險","maps_to":"R1","metric":"TrendForce NAND 合約價季變動","threshold":"連續兩季為負","action":"改列迴避；持有者減碼一半","source_freq":"TrendForce 每月／每季","date":null,"evidence_refs":["supply_demand_durability#0","cyclical_supply_discipline_capacity#0","cyclical_inventory_price_position#3"]},{"n":4,"text":"長約地板價被重議或提前終止","type":"Single Thing","maps_to":"Single Thing","metric":"長約地板價條款與剩餘履約義務","threshold":"任一地板價調降、提前終止，或剩餘履約義務因非出貨原因季減超過 10%","action":"清倉並改列迴避","source_freq":"每季 10-Q、財報電話會、8-K","date":null,"evidence_refs":["customer_second_source#0","customer_concentration_credit#1"]},{"n":5,"text":"長約覆蓋仍高時毛利率卻大跌，代表地板保護失效","type":"減碼","maps_to":"H3","metric":"非 GAAP 毛利率","threshold":"長約覆蓋 ≥50% 時，單季低於 75%","action":"持有者減碼到半倉，並暫停任何加碼","source_freq":"每季財報","date":null,"evidence_refs":["cyclical_prior_downcycle_behavior#0"]},{"n":6,"text":"關稅或合資廠中斷衝擊毛利","type":"風險","maps_to":"R3","metric":"管理層歸因於關稅或 Kioxia 合資廠中斷的毛利率變動","threshold":"單季下降 ≥3 個百分點","action":"持有者減碼一半；停止加碼","source_freq":"每季財報、8-K、美國 232／301 調查公告","date":null,"evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","reg_tariff_export#2","geo_supply_chain#0","geo_supply_chain#1","geo_supply_chain#3"]},{"n":7,"text":"應收帳款集中度上升","type":"風險","maps_to":"R2","metric":"單一客戶占應收比與應收天數","threshold":"單一客戶占應收超過 25%，或應收天數較前季增加兩成","action":"停止加碼，檢查客戶信用","source_freq":"10-Q／10-K","date":null,"evidence_refs":["customer_concentration_credit#1"]},{"n":8,"text":"營收市占持續流失","type":"風險","maps_to":"R1","metric":"NAND 營收市占（Counterpoint／TrendForce）","threshold":"連兩季低於 10%","action":"護城河方向改判縮減；持有者減碼一半","source_freq":"每季第三方市占報告","date":null,"evidence_refs":["competitive_share_entrants#1"]},{"n":9,"text":"長約通過第一個跌價季檢驗","type":"估值rearm","maps_to":"重啟條件","metric":"合約價下跌季的長約覆蓋率、剩餘履約義務與毛利率","threshold":"合約價季跌的第一個完整季，覆蓋率與剩餘履約義務不下修，且非 GAAP 毛利率 ≥60%","action":"重跑完整研究，通過才以 ≤3% 首倉起步","source_freq":"每季財報與 TrendForce","date":null,"evidence_refs":[]},{"n":10,"text":"8 比 1 拆股生效，所有每股數字需除以 8 後重算","type":"複審日期","maps_to":null,"metric":"拆股","threshold":"2026-11-20 起以拆股後價格交易","action":"以拆股後口徑重算情境樹與所有每股門檻","source_freq":"一次性","date":"2026-11-20","evidence_refs":[]}],"kill_metrics":[{"metric":"NAND 合約價季變動","bear_threshold":"連續兩季為負","window":"滾動兩季","source":"TrendForce 每月／每季合約價報告","last_status":"warning"},{"metric":"長約剩餘履約義務與地板價","bear_threshold":"非出貨原因季減超過 10%，或任一地板價調降","window":"每季","source":"10-Q 剩餘履約義務附註、財報電話會","last_status":"unknown"},{"metric":"非 GAAP 毛利率","bear_threshold":"長約覆蓋 ≥50% 時低於 75%","window":"單季","source":"公司季報新聞稿","last_status":"ok"},{"metric":"NAND 營收市占","bear_threshold":"連兩季低於 10%","window":"兩季","source":"Counterpoint／TrendForce 季度市占","last_status":"warning"},{"metric":"資料中心占營收比","bear_threshold":"FY2027 Q4 低於 40%","window":"至 2027-08 財報","source":"公司季報分終端市場營收","last_status":"ok"}],"evidence_dismissed":[],"action_conditions":{"rearm_trigger":"NAND 合約價轉跌的第一個完整季，長約覆蓋率與剩餘履約義務未下修，且非 GAAP 毛利率守住 60% 以上","exec_line":"現價不追；重啟條件成立後重跑完整研究，通過才以 ≤3% 首倉起步，分兩到三批，每批間隔一季財報","holding_cap":"≤3%"}},"decision_inputs":{"signal":"C","ma":"-","cycle_position":"晚循環","cycle_verdict":"頂部觀望","thesis_irreconcilable":false,"valuation_dependent":true,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":false,"qc49_inherit_prior":false,"wait_for_price":true,"wait_for_price_condition":"等第一個 NAND 合約價下跌季：長約覆蓋率與剩餘履約義務不下修、非 GAAP 毛利率守在 60% 以上，才重跑進場判斷；股價本身不是等待條件","asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null},"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"6,7a","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='C'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='C'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='-'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":true,"basis":"signal='C'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":true,"basis":"valuation_dependent=True, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='A'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='C', runway='🟡', val='🟡', moat_trend='→', week26=-3.04, valuation_dependent=True"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='循環/商品', cycle_position='晚循環', moat='C', moat_trend='→', cycle_gates_pass=False"},{"row":"6/7/7a-verdict","condition":"Soft Veto 生效 → 觀望（max-severity wins；8a/8b 未能繞過）","hit":true,"basis":"soft_veto_rows=['6', '7a']"},{"row":"QC-49","condition":"qc49_inherit_prior=False，不套用","hit":false,"basis":"qc49_inherit_prior=False"},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":"中期 2-5 年","requires_critic":["QC-50"]},"thesis":{"H":[{"id":"H1","text":"多年長約的地板價可執行，覆蓋範圍還在擴大：FY2027 約一半、FY2028 約三分之二位元在長約下，地板價下毛利率約 80%，財務保證 165 億美元；前份門檻（剩餘履約義務不下修、財務保證不縮水）保留","2y":"FY2028 覆蓋率 ≥三分之二，剩餘履約義務不因非出貨原因下修","5y":"經過至少一次合約價下跌季，地板價未調降","10y":null,"threshold":"FY2027 ≥50%、FY2028 ≥67%；剩餘履約義務非出貨原因季減 ≤10%；財務保證不低於 165 億美元","source":"每季財報新聞稿、10-Q 剩餘履約義務附註、財報電話會","drift_rule":"兩年期：連兩季偏離門檻 ≥5% 為削弱，連三季 ≥10% 為反轉"},{"id":"H2","text":"資料中心成為主要客群，改寫營收結構：資料中心占營收由 FY2025 的 13% 升到 Q1 FY2027 的 43.5%。前份門檻「資料中心占產業位元 >40%」已達成（目前約一半），本次改看公司自身占比","2y":"FY2027 Q4 資料中心占營收 ≥45%，FY2028 ≥50%","5y":"資料中心占營收穩定過半，季增率持續高於產業","10y":null,"threshold":"FY2027 Q4 ≥45%","source":"公司每季分終端市場營收；TrendForce 資料中心需求占比","drift_rule":"兩年期：連兩季低於門檻 5% 為削弱，連三季低於 10% 為反轉"},{"id":"H3","text":"穿越週期的毛利率地板抬高：下一輪下行期非 GAAP 毛利率谷底 ≥40%（上一輪 7%），支撐約 110 美元的正常化每股盈餘（前份估 105–115 美元）","2y":null,"5y":"下一次合約價連兩季下跌期間，非 GAAP 毛利率谷底 ≥40%","10y":null,"threshold":"谷底毛利率 ≥40%；長約覆蓋 ≥50% 時單季毛利率 ≥75%","source":"公司季報毛利率；TrendForce 合約價","drift_rule":"五年期：連四季偏離門檻 ≥5% 為削弱，連六季 ≥10% 為反轉"}],"R":[{"id":"R1","text":"2027 下半年供給轉鬆：TrendForce 預估 2027 年位元供給成長超過需求，中國新廠（YMTC 三廠、SK hynix 大連二廠）是主要增量；十月晶圓合約價已停漲，模組廠庫存上升；YMTC 營收市占一年內由 8% 升到 14%","h_ref":"H3","clock":"🔥","threshold":"TrendForce NAND 合約價連兩季季減","evidence_refs":["supply_demand_durability#0","cyclical_supply_discipline_capacity#0","cyclical_inventory_price_position#3","competitive_share_entrants#1"]},{"id":"R2","text":"長約地板在下行期被重議：客戶有多家供應商可選，前十大客戶占營收 44%；應收帳款三家客戶占 41%；執行長自承長約能否撐過下行沒有保證（2026-08-13 投資人日）","h_ref":"H1","clock":"🐢","threshold":"任一地板價調降，或剩餘履約義務因非出貨原因季減超過 10%","evidence_refs":["customer_second_source#0","customer_concentration_credit#1"]},{"id":"R3","text":"供應單點與地緣風險：幾乎全部晶圓來自與 Kioxia 的合資廠，合約限制另找貨源；產品幾乎全在海外生產，國際銷售占 82%；美國 232、301 調查可能取消關稅豁免；2026-04 北上廠附近強震曾讓公司暫停報價（損害未證實）","h_ref":"H3","clock":"⚡","threshold":"歸因於關稅或合資廠中斷的單季毛利率下降 ≥3 個百分點","evidence_refs":["geo_supply_chain#0","geo_supply_chain#1","geo_supply_chain#3","reg_tariff_export#0","reg_tariff_export#1","reg_tariff_export#2"]},{"id":"R4","text":"下行幅度重演上一輪：FY2023 營收跌 38%、每 GB 售價跌 39%、毛利率由 33% 跌到 7%；2022 Q4 合約價單季跌 20–25%；記憶體前兩輪下行毛利率谷底持續 7–9 季","h_ref":"H3","clock":"🐢","threshold":"非 GAAP 毛利率連兩季低於 60%","evidence_refs":["cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#1","cyclical_prior_downcycle_behavior#2"]},{"id":"R5","text":"AI 架構降低每單位運算的儲存需求：10-K 明列此風險；目前沒有具名技術，公司 HBF 與客戶 SLC 需求反而在擴大 NAND 用途","h_ref":"H2","clock":"🐢","threshold":"資料中心營收季增率連兩季低於產業企業 SSD 營收成長","evidence_refs":["substitute_technology#0"]}],"single_thing":{"description":"任一份多年長約在 NAND 合約價下跌期間被重議地板價、縮量或提前終止，且公司讓步（剩餘履約義務因非出貨原因下修）","why_fatal":"長約涵蓋 FY2027 約一半、FY2028 約三分之二位元，是本輪與 FY2023 虧損谷底之間唯一的結構差異。地板一旦失效，正常化盈餘就落到空頭路徑（FY2030 每股盈餘約 35 美元），終端倍數也會同時壓縮","if_happens":"清倉並改列迴避；空頭機率上調到 50% 以上後重跑研究","how_monitor":"每季 10-Q 的剩餘履約義務與財務保證餘額、財報電話會揭露的長約覆蓋率、8-K 合約變更；TrendForce 合約價轉跌時加密檢查","probability":"15%（12–24 個月內：TrendForce 預估的轉鬆時點落在這個窗口，但重議通常要等現貨跌兩季以後才會出現）"}},"appendix_a":{"growth_durability":5,"quality_score":6,"ai_risk":"🟡","long_term_confidence":"中","fpe_fy2":4.19,"peg_fy2":0.65,"stress":{"pass":2,"total":3}},"eps_meta":{"base_eps_path":{"FY2026A":73.76,"FY2027E":226.74,"FY2028E":274.64,"FY2029E":256.77},"fy_end_month":6,"eps_basis":"共識為非 GAAP 每股盈餘（Koyfin 快照）；基期 FY2026A 73.76 美元為 GAAP 稀釋每股盈餘（yfinance），兩者口徑不完全一致。全部為 8 比 1 拆股前口徑，2026-11-20 起股價與每股數字須除以 8。財年約在 6 月底至 7 月初結束"},"catalysts":[{"date":"2026-11-20","date_precision":null,"type":"other","event":"8 比 1 拆股後開始交易，所有每股數字除以 8","impact":"低","watch":"拆股後重算所有每股門檻"},{"date":"2027-01-31","date_precision":"month","type":"guidance","event":"FQ2 FY2027 財報與 FQ3 財測；觀察是否新簽長約","impact":"高","watch":"長約家數與覆蓋率、FQ3 季減幅度"},{"date":"2027-09-30","date_precision":"quarter","type":"macro","event":"TrendForce 預估 NAND 供需在 2027 下半年轉鬆","impact":"高","watch":"合約價季變動是否轉負"},{"date":"2027-12-31","date_precision":"quarter","type":"product","event":"HBF 首批樣品送交客戶（公司稱 2027 年內）","impact":"中","watch":"客戶整合回饋，以及是否納入財務模型"}]}
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
