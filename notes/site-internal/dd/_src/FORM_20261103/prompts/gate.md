你是 DD 管線 v20 的判斷層閘（gate），標的 FORM（20261103）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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
- `f_kpi0_revenue_gaap`（q1_business）｜Revenue (GAAP)＝280.5 USD million｜期間與口徑：Q3 FY2026（季末 2026-09-26，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 財報新聞稿（SEC 8-K Ex.99.1，2026-10-28） https://www.sec.gov/Archives/edgar/data/0001039399/000103939926000040/ex9901-earningsreleasexq326.htm（numbers.latest_quarter_kpis.items[0]，as_of Q3 FY2026（季末 2026-09-26，公告於 2026-10-28））
  - 註記：高於公司自家指引上緣：Q3 指引 260–280（逐字稿）；外部共識未取得
- `f_kpi1_non_gaap_operating_incom`（q1_business）｜Non-GAAP operating income / margin＝94.1 USD million（margin 33.5%）｜期間與口徑：Q3 FY2026（季末 2026-09-26，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 財報新聞稿（SEC 8-K Ex.99.1，2026-10-28） https://www.sec.gov/Archives/edgar/data/0001039399/000103939926000040/ex9901-earningsreleasexq326.htm（numbers.latest_quarter_kpis.items[1]，as_of Q3 FY2026（季末 2026-09-26，公告於 2026-10-28））
- `f_kpi2_gaap_operating_income_ma`（q1_business）｜GAAP operating income / margin＝81.6 USD million（margin 29.1%）｜期間與口徑：Q3 FY2026（季末 2026-09-26，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 財報新聞稿（SEC 8-K Ex.99.1，2026-10-28） https://www.sec.gov/Archives/edgar/data/0001039399/000103939926000040/ex9901-earningsreleasexq326.htm（numbers.latest_quarter_kpis.items[2]，as_of Q3 FY2026（季末 2026-09-26，公告於 2026-10-28））
- `f_kpi3_free_cash_flow`（q1_business）｜Free cash flow＝64.8 USD million（占營收 23.1%）｜期間與口徑：Q3 FY2026（季末 2026-09-26，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 財報新聞稿（SEC 8-K Ex.99.1，2026-10-28） https://www.sec.gov/Archives/edgar/data/0001039399/000103939926000040/ex9901-earningsreleasexq326.htm（numbers.latest_quarter_kpis.items[3]，as_of Q3 FY2026（季末 2026-09-26，公告於 2026-10-28））
- `f_kpi5_guidance_q4_fy2026_reven`（q1_business）｜Guidance Q4 FY2026 revenue＝285 USD million（±10，區間 275–295）｜期間與口徑：Q3 FY2026（季末 2026-09-26，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司 Q3 2026 財報新聞稿（SEC 8-K Ex.99.1，2026-10-28） https://www.sec.gov/Archives/edgar/data/0001039399/000103939926000040/ex9901-earningsreleasexq326.htm（numbers.latest_quarter_kpis.items[5]，as_of Q3 FY2026（季末 2026-09-26，公告於 2026-10-28））
- `f_kpi6_non_gaap_gross_margin`（q1_business）｜Non-GAAP gross margin＝56.5 %｜期間與口徑：Q3 FY2026（季末 2026-09-26，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 財報新聞稿（SEC 8-K Ex.99.1，2026-10-28） https://www.sec.gov/Archives/edgar/data/0001039399/000103939926000040/ex9901-earningsreleasexq326.htm；基線說明見 Q3 法說會逐字稿（numbers.latest_quarter_kpis.items[6]，as_of Q3 FY2026（季末 2026-09-26，公告於 2026-10-28））
- `f_earnings_recency`（q1_business）｜最近一次財報日＝2026-10-28 date｜期間與口徑：2026-10-28／距今 4 個交易日｜kind：realized
  - 來源：—（numbers.earnings_recency，as_of 2026-10-28）
- `f_peer_form_gross_margin_pct`（q2_moat）｜FORM 毛利率＝44.1 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.FORM.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_form_operating_margin_pct`（q2_moat）｜FORM 營業利益率＝15.95 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.FORM.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_form_fcf_margin_pct`（q2_moat）｜FORM FCF 利潤率＝16.67 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.FORM.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_ter_gross_margin_pct`（q2_moat）｜TER 毛利率＝59.41 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.TER.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_ter_operating_margin_pct`（q2_moat）｜TER 營業利益率＝33.17 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.TER.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_ter_fcf_margin_pct`（q2_moat）｜TER FCF 利潤率＝21.59 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.TER.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_6857_t_gross_margin_pct`（q2_moat）｜6857.T 毛利率＝65.73 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.6857.T.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_6857_t_operating_margin_pct`（q2_moat）｜6857.T 營業利益率＝45.86 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.6857.T.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_6223_two_gross_margin_pct`（q2_moat）｜6223.TWO 毛利率＝56.52 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.6223.TWO.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_6223_two_operating_margin_pct`（q2_moat）｜6223.TWO 營業利益率＝30.26 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.6223.TWO.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_6223_two_fcf_margin_pct`（q2_moat）｜6223.TWO FCF 利潤率＝-11.23 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.6223.TWO.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_cohu_gross_margin_pct`（q2_moat）｜COHU 毛利率＝43.95 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.COHU.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_cohu_operating_margin_pct`（q2_moat）｜COHU 營業利益率＝-6.19 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.COHU.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝3.35 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-10-31）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝4.24 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-10-31）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝5.88 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-10-31）
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝37.3 %｜期間與口徑：2026-07-30 → 2026-10-31／FY1 共識 EPS 2.44 → 3.35（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-10-31）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝1047.97 USD m｜期間與口徑：2026-11-03／yfinance revenue_estimate 0y 平均（10 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝1301.29 USD m｜期間與口徑：2026-11-03／yfinance revenue_estimate +1y 平均（10 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi4_sbc_stock_based_compensa`（q4_capital）｜SBC (stock-based compensation)＝8.8 USD million（占 GAAP 營業利益 10.8%；占營收 3.1%）｜期間與口徑：Q3 FY2026（季末 2026-09-26，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 財報新聞稿（SEC 8-K Ex.99.1，2026-10-28） https://www.sec.gov/Archives/edgar/data/0001039399/000103939926000040/ex9901-earningsreleasexq326.htm（numbers.latest_quarter_kpis.items[4]，as_of Q3 FY2026（季末 2026-09-26，公告於 2026-10-28））
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝-367.65 USD m｜期間與口徑：2026-11-03／yfinance 最新一季：總債務 27.76、現金 395.41（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝78.12 m shares｜期間與口徑：2026-11-03／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_ev_m`（q5_valuation）｜目前企業價值 EV（市值＋淨負債）＝6664.0 USD m｜期間與口徑：2026-11-03／市值 7031.65 ＋ 淨負債 -367.65｜kind：realized
  - 來源：—（numbers.capital_structure.ev_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝90.01 USD｜期間與口徑：2026-11-02（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-11-02（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝26.87 x｜期間與口徑：2026-10-31／分母＝FY1 EPS 3.35，分子＝快照價 90.01｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-10-31）
- `f_consensus_rev_fy1_pct`（q5_valuation）｜FY1 共識修正＝9.84 %｜期間與口徑：2026-10-31／兩份 Koyfin 快照之間的 EPS 修正幅度（3.05 → 3.35）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.fy1.revision_pct，as_of 2026-10-31）
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝41.29 x｜期間與口徑：2026-11-02（RTH 收盤，UTC）／4 個年度端點內的分位＝10.9｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-11-02（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝10.9 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝7.17 x｜期間與口徑：2026-11-02（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝100.0 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝6.8 x｜期間與口徑：2026-11-02（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝100.0 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ev_s_fwd`（q5_valuation）｜EV/S（EV ÷ FY1 共識營收）＝6.36 x｜期間與口徑：2026-11-03／f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）｜kind：estimate
  - 來源：—（numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝-33.01 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-11-02（RTH 收盤，UTC））
- `f_rsi14`（q5_valuation）｜RSI(14)＝35.46｜期間與口徑：2026-11-02（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ma_state`（q5_valuation）｜週線均線六態（decision_inputs.ma 必須等於此值）＝🟡｜期間與口徑：2026-11-03／timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）
  - 原文：「price 89.7 / W52 103.01 / W104 69.3 / W250 50.58 / W250 13週斜率 1.67%」
- `f_ma_w52`（q5_valuation）｜52 週均線＝103.01 USD｜期間與口徑：2026-11-03／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）
- `f_ma_w104`（q5_valuation）｜104 週均線＝69.3 USD｜期間與口徑：2026-11-03／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）
- `f_ma_w250`（q5_valuation）｜250 週均線＝50.58 USD｜期間與口徑：2026-11-03／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）
- `f_ma_slope_w250_pct`（q5_valuation）｜W250 13 週斜率＝1.67 %｜期間與口徑：2026-11-03／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）

### findings_digest 中方向為負或來源衝突的條目（14 條）
- `competitive_share_entrants#0`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K 列出探針卡主要對手含 Technoprobe、JEM、MPI、MJC 等；探針卡市場歷來分散；公司承認競爭加劇已導致或可能導致降價、毛利下降或失去市占。
  - 來源：SEC EDGAR 10-K FY2025 Item 1 / 1A（as_of 2026-02-20）｜affects：moat_trend、decision_inputs.bear
- `competitive_share_entrants#2`（competitive_share_entrants｜方向 -｜狀態 ok）：TrendForce 2026-06 報告：Technoprobe 有望超越 FormFactor 成為全球探針卡第一供應商。
  - 來源：TrendForce, Probe Card Tech Upgrade & Market Reshaped by AI Packaging-Part 2（as_of 2026-06-26）｜affects：moat_trend、decision_inputs.bear
- `customer_concentration_credit#0`（customer_concentration_credit｜方向 -｜狀態 ok）：SK hynix 占 FormFactor FY2025 營收 22.9%（FY2024 為 18.9%）；FY2024 兩大客戶合計 33.5%、FY2023 單一客戶 17.1%。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A/財報附註（as_of 2026-02-20）｜affects：thesis.R、decision_inputs.bear
- `customer_concentration_credit#1`（customer_concentration_credit｜方向 -｜狀態 ok）：SK hynix 單季占比 FY2025 Q1–Q4 為 23.3%、25.0%、24.5%、19.2%；期末應收帳款 FY2025 兩家客戶占 15.8% 與 10.8%，公司通常不要求擔保品。
  - 來源：SEC EDGAR 10-K FY2025 財報附註（as_of 2026-02-20）｜affects：thesis.R
- `customer_concentration_credit#3`（customer_concentration_credit｜方向 -｜狀態 ok）：第三方報導稱 Q1 2026 SK hynix 占 FormFactor 營收 29.5%（去年同期 23.3%），NVIDIA 首次列為 10%+ 客戶（10.2%）；未經一手文件核實。
  - 來源：PhotonCap「formfactors july 29th」（as_of 2026-07-29）｜affects：thesis.R
- `supply_demand_durability#3`（supply_demand_durability｜方向 -｜狀態 ok）：評論指測試需求具週期性，當前強勢集中在AI/HBM與CPO，業績對產品組合變化敏感；另有出口管制、關稅、AI支出持續性不確定。
  - 來源：Barchart: FormFactor's Semiconductor Test Business Confronts the Post-Boom Reality Tomorrow（as_of 2026-04-28）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：FY2025 對中國客戶銷售占營收 7%（FY2024 為 14%），中國為受美國擴大出口許可要求影響的地區之一。
  - 來源：SEC EDGAR 10-K FY2025, Item 1 Business（as_of 2026-02-20）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#1`（reg_tariff_export｜方向 -｜狀態 ok）：FY2025 關稅成本使毛利率受 1.4 個百分點衝擊，探針卡毛利率下降部分因關稅成本增加；下半年毛利率較上半年明顯改善。
  - 來源：SEC EDGAR 10-K FY2025, Item 7 MD&A（as_of 2026-02-20）｜affects：valuation、thesis.R
- `reg_tariff_export#2`（reg_tariff_export｜方向 -｜狀態 ok）：10-K 風險因素：部分零組件來自單一或有限供應商，加徵關稅與貿易壁壘可能加劇供應風險；並提及美中出口管制與貿易緊張可能影響中國市場業務。
  - 來源：SEC EDGAR 10-K FY2025, Item 1A Risk Factors（as_of 2026-02-20）｜affects：decision_inputs.bear、thesis.R
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：FormFactor 10-K 風險因素：依賴單一或有限來源供應商，多數供應商僅採採購單而非長約，單一來源供應商可能漲價拖累毛利
  - 來源：FormFactor 10-K FY2022 (SEC)（as_of 2023-02-28）｜affects：decision_inputs.bear、thesis.R
- `geo_supply_chain#2`（geo_supply_chain｜方向 -｜狀態 ok）：FY2025 10-K 將供應商中斷連結到關稅與貿易壁壘、區域緊張
  - 來源：FormFactor 10-K FY2025 (SEC)（as_of 2026-02-25）｜affects：decision_inputs.bear、thesis.R
- `end_markets#2`（end_markets｜方向 -｜狀態 ok）：TrendForce June 2026 report: FormFactor, Technoprobe and MJC dominate probe cards; Taiwan's CHPT, MPI and WinWay gaining share on AI wave; Technoprobe could overtake FormFactor as top global supplier in 2026.
  - 來源：TrendForce, Probe Card Tech Upgrade & Market Reshaped by AI Packaging-Part 2（as_of 2026-06-26）｜affects：moat_trend、decision_inputs.bear
- `substitute_technology#1`（substitute_technology｜方向 -｜狀態 ok）：10-K 風險因子承認客戶需求隨 AI 相關產品快速變化、技術變遷快，且他人可能獨立開發類似或競爭技術或繞過專利設計
  - 來源：SEC EDGAR 10-K FY2025 Item 1A Risk Factors（as_of 2026-02-20）｜affects：moat_trend、thesis.R、decision_inputs.bear
- `major_events#0`（major_events｜方向 -｜狀態 ok）：2026-01-09 8-K 揭露重整計畫（Item 2.05）與重大減損（Item 2.06）；搜尋摘要稱預計重整費用約 $30–40M，整併 Carlsbad 與 Baldwin Park 製造廠，多數費用落在 FY2026。
  - 來源：SEC EDGAR 8-K（2026-01-09）Item 2.06（as_of 2026-01-09）｜affects：thesis.R、valuation

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 9 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/FORM_20261103/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":234.0,"bear_5y_price":48.0,"p_bull_pct":25,"p_bear_pct":30,"upside_5y_pct":49.3,"ev5y_pct":48.2,"irr_base_pct":8.3,"asym_ratio":2.9,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":3.35,"pe":26.87,"basis":"FY2026E（FY1）非GAAP共識EPS，已過三季接近實現值；終端倍數同為非GAAP本益比"},"eps":{"bull":[4.6,6.2,7.2,8.1,9.0],"base":[4.1,5.2,4.8,5.6,6.4],"bear":[3.5,2.6,2.0,2.5,3.0]},"pe":{"bull":26,"base":21,"bear":16},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0,"net_buyback":0},"second_stage":{"bull_cagr_pct":12,"base_cagr_pct":8},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### FORM_Q2_2026_Earnings_Call_20260729.md
- 2026-07-29｜CFO Aric McKinnis｜guidance：Q3 營收指引 2.7 億美元 ±1,000 萬。（原話："We expect Q3 revenues of $270 million, plus or minus"）
- 2026-07-29｜CFO Aric McKinnis｜guidance：Q3 非 GAAP EPS 指引 0.86 美元 ±0.09。（原話："for Q3 is expected to be $0.86, plus or minus $0.09."）
- 2026-07-29｜CEO Mike Slessor｜guidance：Q3 DRAM 營收與 Q2 相當，但 HBM 轉向 DDR 的結構明顯變動。（原話："but with a significant underlying shift from HBM to DDR."）
- 2026-07-29｜CFO Aric McKinnis｜margin：Q2 非 GAAP 毛利率 53.3% 的改善拆成三分之一持久成本降低、三分之一營收增加、三分之一不會重複的項目。（原話："Approximately 1/3 of the improvement is from baseline cost"）
- 2026-07-29｜CFO Aric McKinnis｜margin：排除一次性項目與產品組合有利後，基準毛利率約 51%。（原話："improved to around 51% at Q2 volumes."）
- 2026-07-29｜CFO Aric McKinnis｜margin：Q3 毛利率指引 54% 的中點高於 51% 基準，主因是 IEEPA 關稅退款（約 300bp，不會重複）。（原話："300 basis points in IEEPA tariff refunds"）
- 2026-07-29｜CFO Aric McKinnis｜margin：Q3 非 GAAP 毛利率指引中點 54%，±150bp。（原話："gross margin of 54%, plus or minus 150 basis points."）
- 2026-07-29｜CFO Aric McKinnis｜margin：Q3 較高營收量的好處預期被 DRAM 較不利的產品組合抵銷。（原話："The benefits of marginally higher Q3 revenue volumes are"）
- 2026-07-29｜CFO Aric McKinnis｜margin：Q2 探針卡部門毛利率 54.4%，歸因於稼動率、支出紀律與良率。（原話："increased to 54.4%, driven primarily by higher factory"）
- 2026-07-29｜CFO Aric McKinnis｜margin：Q2 非 GAAP 營業費用 6,570 萬美元，占營收 25.4%，Q1 為 27.4%。（原話："operating expenses were $65.7 million or 25.4% of revenue"）
- 2026-07-29｜CFO Aric McKinnis｜guidance：Q3 非 GAAP 營業費用指引 7,000 萬 ±200 萬，含約 700 萬 Farmers Branch 預生產租金。（原話："about $7 million in preproduction rent costs"）
- 2026-07-29｜CFO Aric McKinnis｜guidance：2026 年 Farmers Branch 與產能擴充現金資本支出預期 1.4 億至 1.7 億美元，維持不變。（原話："capacity additions will be between $140 million"）
- 2026-07-29｜CFO Aric McKinnis｜guidance：2026 年預生產爬坡成本預期調整為 2,500 萬至 3,000 萬美元。（原話："between $25 million and $30 million in total in 2026."）
- 2026-07-29｜CFO Aric McKinnis｜guidance：Q3 非 GAAP 有效稅率預期 15% 至 19%。（原話："expected to be between the range of 15% to 19%."）
- 2026-07-29｜CEO Mike Slessor｜commitment：Farmers Branch 預計 Q4 上線、2027 年全年爬坡。（原話："site is on track to come online in the fourth quarter"）
- 2026-07-29｜CFO Aric McKinnis｜commitment：2030 目標模型：營收倍增至 16 億、非 GAAP 毛利率 55%、EPS 5 美元。（原話："achieving 55% non-GAAP gross margin and more than doubling"）
- 2026-07-29｜CFO Aric McKinnis｜commitment：Farmers Branch 達初期目標產能（預計 2028 初）後預期對毛利率有增益。（原話："we expect Farmers Branch to be accretive to gross margin."）
- 2026-07-29｜CFO Aric McKinnis｜commitment：管理層表示毛利率增益主要在 2028 年才完整體現，2027 年爬坡有無效率。（原話："primarily counting on matching that sort of improvement"）
- 2026-07-29｜CFO Aric McKinnis｜capital_allocation：Q2 未回購股票，短期現金優先用於 Farmers Branch 爬坡。（原話："During the second quarter, we did not repurchase any shares."）
- 2026-07-29｜CFO Aric McKinnis｜capital_allocation：Farmers Branch 投資主要由獲利與營運現金流自行資助，另有德州 2,420 萬美元補助。（原話："largely self-funding the investment in Farmers Branch"）
- 2026-07-29｜CEO Mike Slessor｜product：CPO 營收原預期達年初 1,000 萬至 2,000 萬區間高端，現預期 Q3 底超越該區間、全年顯著超過 2,000 萬。（原話："We now expect to exceed that range by the end"）
- 2026-07-29｜CEO Mike Slessor｜product：CPO 全年超過 2,000 萬確定，但幅度難以判斷，新技術有加速與消化階段。（原話："The magnitude of that is a little tricky to judge"）
- 2026-07-29｜CEO Mike Slessor｜product：管理層表示 CPO 無顯著提前或改變看法，2027 逐季預測過細。（原話："wouldn't say there's a significant pull in or change in our"）
- 2026-07-29｜CEO Mike Slessor｜product：Q2 HBM 約占 DRAM 營收三分之二，來自兩家客戶採用 SmartMatrix。（原話："HBM comprised approximately 2/3 of our overall DRAM revenue"）
- 2026-07-29｜CEO Mike Slessor｜product：Systems 營收 Q2 季增近一倍，來自工程探針台復甦與 CPO 加速。（原話："Systems revenue nearly doubled sequentially"）
- 2026-07-29｜CEO Mike Slessor｜product：下一代自訂 ASIC（如 Google TPU）預期需要先進 MEMS 探針卡；2026 年無顯著營收貢獻，2027 起放量。（原話："significant revenue contributions here in 2026."）
- 2026-07-29｜CEO Mike Slessor｜customer：Q2 台灣營收季增逾 30%，全球領先晶圓代工廠再度為 10% 客戶。（原話："revenue from Taiwan grew sequentially by more than 30%"）
- 2026-07-29｜CEO Mike Slessor｜customer：Q2 10% 客戶中無 GPU 業務；GPU 預期為下半年事件，已通過認證並於 Q3 出貨量產品。（原話："There really is no component of GPU business in the second"）
- 2026-07-29｜CEO Mike Slessor｜customer：CPU 需求增加來自三組客戶關係：既有 CPU 龍頭、HPC 龍頭擴張、大型無晶圓 XPU 客戶多個設計案。（原話："successful qualification and subsequent multiple design wins"）
- 2026-07-29｜CEO Mike Slessor｜customer：無晶圓 CPU 客戶市占為低個位數，產能受限成為市占成長的限制因素，直到 Farmers Branch 上線。（原話："single-digit market share at this point"）
- 2026-07-29｜CEO Mike Slessor｜competition：HBM 的強勢市占集中在高速堆疊晶粒最終測試，核心晶粒等插入點競爭多。（原話："lots of competition for example, in the core die insertions"）
- 2026-07-29｜CEO Mike Slessor｜competition：第三大 HBM 客戶的市占不如前兩家強。（原話："although our share is stronger at two of them right now."）
- 2026-07-29｜CEO Mike Slessor｜competition：GPU 先進 MEMS 探針卡目前主要是競爭對手的生意，公司剛通過認證。（原話："Right now, it's primarily"）
- 2026-07-29｜CEO Mike Slessor｜risk：DRAM 客戶因 DDR5 價格轉向 DDR，探針卡為裝置專用耗材，公司 DRAM 組合隨之變動。（原話："probe cards are a device-specific consumables"）
- 2026-07-29｜CFO Aric McKinnis｜risk：供應鏈限制在目前生產水準下增加。（原話："we see more constraints across the supply chain"）

### FORM_Analyst_Investor_Day_FormFactor_Inc_20260511.md
- 2026-05-11｜CFO Aric McKinnis｜guidance：2030 目標：市場成長至 $4.5B，FormFactor 營收翻倍至 $1.6B（原話："we're expecting the market to grow to $4.5 billion."）
- 2026-05-11｜CFO Aric McKinnis｜guidance：2030 目標毛利率 55%（原話："55% gross margins at these revenue levels"）
- 2026-05-11｜CFO Aric McKinnis｜guidance：2030 目標非 GAAP EPS $5（原話："a non-GAAP EPS of $5 per share"）
- 2026-05-11｜CFO Aric McKinnis｜guidance：2030 營業費用占營收 23%（原話："operating expense as a percent of revenues of 23%"）
- 2026-05-11｜CFO Aric McKinnis｜guidance：EPS 由 2025 年 $1.27 增至 $5（原話："$1.27 in the baseline year of 2025 to $5 a share"）
- 2026-05-11｜Sudhakar Raman｜guidance：探針卡業務 2030 年營收翻倍（原話："double the probes business revenue by 2030"）
- 2026-05-11｜Jens Klattenhoff｜guidance：Systems 部門 2030 年營收翻倍（原話："planning to double our revenue within the Systems segment"）
- 2026-05-11｜CEO Mike Slessor｜guidance：CPO 2026 營收原預期 $10–20M，上季財報更新至區間高端（原話："we updated that to the high end of that range"）
- 2026-05-11｜CFO Aric McKinnis｜guidance：晶圓級 CPO 測試 2030 年 SAM 約 $300–400M（原話："SAM by 2030, around about $300 million to $400 million"）
- 2026-05-11｜Jens Klattenhoff｜guidance：Jens 稱矽光與 CPO 2030 年對公司為數億美元機會（原話："a multi-hundred million dollar opportunity by 2030"）
- 2026-05-11｜Sudhakar Raman｜guidance：Sudhakar 稱先進探針卡市場至 2030 年成長口徑為 $2.8B 至 $4B（與 CFO 的 TAM $3.1B→$4.5B 口徑不同）（原話："growth of about $2.8 billion to $4 billion by 2030"）
- 2026-05-11｜CFO Aric McKinnis｜guidance：市場 CAGR 約 8%，公司計畫成長速度為其兩倍（原話："about 8% CAGR over this time frame"）
- 2026-05-11｜CFO Aric McKinnis｜margin：2020 年舊目標模型：營收約 $850M、毛利率 47%（原話："targeting around $850 million in revenue, 47% gross margins"）
- 2026-05-11｜CFO Aric McKinnis｜margin：毛利率改善拆解：量能約 600bp（原話："about 600 basis points from volume as we double revenues"）
- 2026-05-11｜CFO Aric McKinnis｜margin：毛利率改善拆解：營運卓越約 500bp（原話："about 500 basis points from operational excellence"）
- 2026-05-11｜CFO Aric McKinnis｜margin：毛利率改善拆解：創新約 400bp（原話："about 400 basis points from innovation"）
- 2026-05-11｜CFO Aric McKinnis｜margin：管理層稱毛利率改善不靠產品組合（原話："we aren't relying on luck"）
- 2026-05-11｜CFO Aric McKinnis｜margin：管理層稱後續改善會比前面困難（原話："Now it's going to get harder as we move"）
- 2026-05-11｜CFO Aric McKinnis｜margin：最近一季毛利率 49%，指引高 50bp；部分因素為暫時性（原話："we guided 50 basis points up from that level"）
- 2026-05-11｜CFO Aric McKinnis｜margin：最近一季探針卡毛利率超過 50%，兩部門毛利率趨同（原話："we exceeded 50% gross margin in the probe card business"）
- 2026-05-11｜CFO Aric McKinnis｜margin：毛利率單期波動正常範圍約正負數百 bp（原話："plus or minus a couple of hundred basis points"）
- 2026-05-11｜CFO Aric McKinnis｜margin：2025 年起至今已有 1,100bp 改善，三大支柱皆有貢獻（原話："the 1,100 basis point improvement that we've generated"）
- 2026-05-11｜CFO Aric McKinnis｜margin：舊目標模型因產品組合轉變對毛利率不利（原話："it was not favorable to our gross margins"）
- 2026-05-11｜CFO Aric McKinnis｜margin：Farmers Branch 爬坡期預期有毛利率逆風，由效率改善抵銷（原話："to be offset by the efficiencies that we're driving"）
- 2026-05-11｜CFO Aric McKinnis｜margin：德州製造成本較加州低（原話："in Texas, a little bit cheaper to manufacture there"）
- 2026-05-11｜Missy Figueroa｜commitment：Farmers Branch 兩條線預計年底前完成驗證，2027 年開始量產爬坡（原話："with initial production ramp starting in 2027"）
- 2026-05-11｜Missy Figueroa｜commitment：Farmers Branch 採模組化擴充，資本投入對應需求（原話："There will be no speculative capacity and no excess volume."）
- 2026-05-11｜CFO Aric McKinnis｜commitment：管理層稱 Farmers Branch 是未來約 1.5 年最優先事項（原話："probably the single most important short-term priority"）
- 2026-05-11｜CFO Aric McKinnis｜commitment：目標模型自我融資（原話："importantly, it's self-funding"）
- 2026-05-11｜CFO Aric McKinnis｜commitment：CFO 稱目標模型已含 Farmers Branch 所需投資（原話："it includes the required investment"）
- 2026-05-11｜CEO Mike Slessor｜capital_allocation：併購以補強型為主，Keystone 為例（原話："It is more tilted towards the tuck-in."）
- 2026-05-11｜CEO Mike Slessor｜capital_allocation：CEO 重申測試與封裝供應鏈需整併（原話："needs to consolidate in the supply chain"）
- 2026-05-11｜CFO Aric McKinnis｜capital_allocation：庫藏股目的為抵銷股權激勵稀釋（原話："The main purpose of that program is to buy back shares"）
- 2026-05-11｜CFO Aric McKinnis｜capital_allocation：長期維持性資本支出約占營收 4–5%（原話："around 4% to 5% of revenues in sustaining capital"）
- 2026-05-11｜Missy Figueroa｜capital_allocation：宣布關閉 Carlsbad A&T 並併入 Farmers Branch（原話："we also announced the site closure of our Carlsbad A&T."）
- 2026-05-11｜CFO Aric McKinnis｜capital_allocation：R&D 優先順序：縮小焦點、避免同時做太多事（原話："You try to do too many things at once"）
- 2026-05-11｜Sudhakar Raman｜competition：客製 ASIC 長期預期為先進 MEMS 且兩家供應商市場（原話："a 2-supplier market in the long term"）
- 2026-05-11｜CEO Mike Slessor｜competition：探針卡供給吃緊，管理層稱各家處境相同（原話："Everybody is in the same constrained situation."）
- 2026-05-11｜CFO Aric McKinnis｜competition：GPU 測試公司過去未參與，預期 2026 下半年起放量（原話："we didn't participate historically in GPU tests."）
- 2026-05-11｜CFO Aric McKinnis｜competition：CPU 部分大廠份額低到幾乎沒有，預期滲透（原話："we have low to nonexistent share"）
- 2026-05-11｜CEO Mike Slessor｜competition：公司稱自己是唯一同時有邏輯與 DRAM 探針卡規模的供應商（原話："We're the only supplier of scale in both foundry and logic"）
- 2026-05-11｜Sudhakar Raman｜product：HBM 世代演進使測試強度提高約 25–30%（原話："increases the test intensity by about 25% to 30%"）
- 2026-05-11｜Sudhakar Raman｜product：客製 HBM 新架構預期 2028 年後實現（原話："coming to fruition more in the 2028 and beyond time frame"）
- 2026-05-11｜Sudhakar Raman｜product：Sudhakar 稱現有產品跟不上下一代 GPU 熱需求，已與客戶共同開發（原話："the current set of products are not able to keep up"）
- 2026-05-11｜Jens Klattenhoff｜product：Jens 稱 2026 為 CPO 轉入量產的轉折年（原話："2026 is an inflection year"）
- 2026-05-11｜Jens Klattenhoff｜product：CPO 第一測試站可降低良品晶粒成本最多 5 倍（原話："reduces cost of good die by up to 5x"）
- 2026-05-11｜CEO Mike Slessor｜product：長期預期 CPO 測試走向拆分的開放生態（原話："we expect CPO as a team to broaden out"）
- 2026-05-11｜CEO Mike Slessor｜customer：HBM 首張探針卡出貨給現第一大客戶（2012）（原話："who's now our #1 customer"）
- 2026-05-11｜CEO Mike Slessor｜customer：客戶對 6 個月預測更投入，產能協議／付費保產能在討論（原話："capacity agreements, paying for capacity"）
- 2026-05-11｜CEO Mike Slessor｜customer：客戶提供超過一季的需求能見度（原話："not visibility, on what customers think they need from us"）
- 2026-05-11｜CFO Aric McKinnis｜customer：商務長稱公司定位已是共同開發夥伴（原話："we are no longer just a supplier"）
- 2026-05-11｜CEO Mike Slessor｜risk：管理層稱產業屬週期性，成長路徑不會線性（原話："I don't expect it to be linear"）
- 2026-05-11｜CEO Mike Slessor｜risk：管理層稱供給吃緊情況將持續一段時間（原話："in an undersupply condition for a while"）
- 2026-05-11｜CFO Aric McKinnis｜risk：管理層稱市場有過熱氛圍，自稱務實（原話："a lot of bubbliness out there in the market right now"）
- 2026-05-11｜CEO Mike Slessor｜risk：DRAM 漲價推升產業金額，探針卡金額強度預期與之脫鉤（原話："going to see a decoupling between the classic probe card"）
- 2026-05-11｜CEO Mike Slessor｜risk：人才招募有挑戰但目前順利（原話："are there challenges with talent? Sure, right?"）
- 2026-05-11｜Missy Figueroa｜risk：營運改善來源為良率與週期時間（原話："squeezing more out of the juice"）

### 問答異常語氣（迴避／改口／保留）
- FORM_Q2_2026_Earnings_Call_20260729.md｜問：Duley 詢問週期時間與良率已改善多少的具體指標（是否已達 60% 週期時間改善的一半）。｜答法：CFO 表示通常不分享這類指標，改以「on track」、Q3 營收年化近 1.1B、毛利率 49%→51% 回應，未給數字。
- FORM_Q2_2026_Earnings_Call_20260729.md｜問：Prisco 詢問 Farmers Branch 營收貢獻時間點與可觀程度。｜答法：CFO 談現有廠區效率與初始產能約等同加州探針卡廠，「to the extent the demand is there」，未給營收貢獻時點或金額。
- FORM_Q2_2026_Earnings_Call_20260729.md｜問：Needham 詢問 CPO 時程是否從 2028 提前、2027 是否放量。｜答法：CEO 稱無顯著提前或改變，但承認短期加速；表示 2027 逐季預測 a bridge too far，未給 2027 數字。
- FORM_Q2_2026_Earnings_Call_20260729.md｜問：Citi 詢問 CPO 全年可做多少營收。｜答法：CEO 稱 Q4 與全年幅度 open question、tricky to judge，只確認高於 2,000 萬。
- FORM_Analyst_Investor_Day_FormFactor_Inc_20260511.md｜問：Craig Ellis 問營運改善是否為近期提前拉貨、Farmers Branch 前還能撐多久｜答法：CEO 轉述 Farmers Branch 不到一年內爬坡，Missy 答「confident」並談良率與週期時間，未給量化產能數字
- FORM_Analyst_Investor_Day_FormFactor_Inc_20260511.md｜問：Matt Prisco 問明年 Q1 德州啟用折舊對毛利率影響｜答法：CEO 只答第二題（份額），Aric 稱爬坡期有逆風但會被效率抵銷，未給 Q1 數字
- FORM_Analyst_Investor_Day_FormFactor_Inc_20260511.md｜問：Yu Shi 問 CPO 量產時點（財報會議提到 2028）是否更新｜答法：CEO 改談 2026 年營收預期更新與 Triton 裝機，未回應 2028 時點
- FORM_Analyst_Investor_Day_FormFactor_Inc_20260511.md｜問：Stifel 分析師問 Farmers Branch 12 個月最大增量營收｜答法：Missy 轉交 Aric，Aric 稱目標模型已含投資，未給增量營收數字
- FORM_Analyst_Investor_Day_FormFactor_Inc_20260511.md｜問：Matt Prisco 問 2030 目標是否錨定半導體營收、預測上修時如何轉換｜答法：CEO 改談 DRAM ASP 上漲與探針卡金額強度脫鉤，Aric 談務實與彈性，未說明目標模型錨定基準

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 5 | 2 |
| customer_second_source | found | 1 | 2 |
| customer_concentration_credit | found | 4 | 2 |
| supply_demand_durability | found | 4 | 4 |
| regulatory_antitrust | none | 0 | 2 |
| reg_tariff_export | found | 4 | 2 |
| geo_supply_chain | found | 3 | 2 |
| end_markets | found | 6 | 4 |
| substitute_technology | found | 4 | 2 |
| channel_business_model_shift | found | 1 | 2 |
| capital_markets_pricing | found | 7 | 4 |
| major_events | found | 2 | 4 |

未涵蓋／不適用軸的查詢詞原文（供判相關性）：
- **regulatory_antitrust**（none）：FormFactor FORM antitrust OR DOJ OR FTC OR export controls investigation 2026；FormFactor regulatory scrutiny semiconductor equipment export restrictions China 2026

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260629","verdict":"觀望","role":"條件式衛星持倉","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"HBM4 結構性 replacement-cycle 驅動 GM/EPS 維持高檔（margin 拐點可持續）","columns":{"2Y 驗證點":"non-GAAP GM 維持 ≥ 46%、DRAM/HBM 段 YoY 雙位數","5Y 驗證點":"HBM4→HBM5 接棒不斷層、GM 站穩 45%+","10Y 驗證點":"探針卡仍是高層數記憶體測試必經環節","具體數字門檻":"non-GAAP GM ≥ 46%；DRAM/HBM 段營收 YoY ≥ +15%","信息來源":"FORM Q1 FY26 法說、8-K（2026-04-29）；probe card 市調（Mordor）","漂移觸發":"連 2 季 GM TTM 偏離 ≥ 5%（"}},{"id":"H2","text":"FORM 守住 HBM probe 領先（sole/primary），並在 F&L networking（Nvidia/AMD）拿份額補 2nm 流失","columns":{"2Y 驗證點":"HBM 維持 sole/primary、F&L networking 段成長 > F&L 整體","5Y 驗證點":"探針卡份額 ≥ 25%、HBM 段無量產 second-source","10Y 驗證點":"SmartMatrix 世代延續領先、IP 護城河擴大","具體數字門檻":"整體探針卡份額 ≥ 25%；HBM 大廠無量產 second-source","信息來源":"市調份額（FORM 26% / TPRO 16.5% / Micronics 10.2%, 2025）；各 HBM 廠認證新聞","漂移觸發":"任一 HBM 廠量產導入 second-source → 反轉"}},{"id":"H3","text":"估值（~50x forward PE）能被 EPS 成長與倍數維持消化，不大幅 de-rate","columns":{"2Y 驗證點":"forward PE 維持 ~45–55x 區間、不破 ~35x","5Y 驗證點":"5Y end PE ≥ ~28x（成熟仍享結構溢價）","10Y 驗證點":"市場持續給予 AI 測試結構溢價","具體數字門檻":"FY27 forward PE 維持 > 35x；5Y end PE ≥ 28x","信息來源":"yfinance/GuruFocus forward PE；§11.1 5Y 分位","漂移觸發":"forward PE 連 2 季"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"HBM4 ramp 時序後移 + 循環峰值 margin 回吐：SK Hynix（最大客戶 22.9%）2026-06 放慢 HBM4 + F&L（PC/server）續軟 → 近端探針卡訂單後移、GM 從 49% 回落","columns":{"對應假設":"H1","時間尺度":"⚡🔥 短中期（已部分觸發，2026H2 顯現）","監測指標":"SK Hynix HBM4 量產進度、non-GAAP GM（季）、F&L probe 訂單 YoY","警戒閾值":"GM 連 2 季"}},{"id":"R2","text":"foundry/HBM 份額流失：Technoprobe（已贏 30% TSMC 2nm）/Micronics（升 primary）擴大，並威脅切入 HBM 量產","columns":{"對應假設":"H2","時間尺度":"🔥 中期（4–6 季）","監測指標":"各 HBM 廠/TSMC 認證新聞、FORM 份額市調","警戒閾值":"任一 HBM 廠量產 second-source → 重評 §6/§7"}},{"id":"R3","text":"估值倍數系統性下移：AI 測試溢價收斂、probe-card tier 整體 de-rate（TPRO 121x PE/FORM 56x 皆為極端）","columns":{"對應假設":"H3","時間尺度":"🐢 長期（2+ 年）","監測指標":"forward PE 5Y 分位、同 tier（TPRO）倍數","警戒閾值":"forward PE 連 2 季"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":3.3,"ev5y_pct":13.0,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"條件式衛星持倉","signal":"B","val":"🟠","ma":"✅","trap":"🟡","moat_trend":"→","runway_post_y5":"🟡","asym_ratio":null,"ev5y_pct":13.0,"irr_base_pct":3.3,"max_dd_pct":-60.0,"bull_5y_price":245.36,"bear_5y_price":60.65,"p_bull_pct":28.0,"p_bear_pct":30.0,"rearm_trigger":null,"price_at_dd":137.84,"archetype":null,"cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"FORM","date":"2026-11-03","schema":"v15.0","contract":"v19","company_name":"FormFactor, Inc."},"oneliner":"探針卡前兩大廠，現有廠房已到產能上限、基準毛利率升到53%；股價一個月跌約四成後FY2027本益比約21倍，但共識FY2028 EPS已超過公司2030年目標，便宜建立在週期高點利潤率上，等德州新廠爬坡期毛利率守住再進場。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/FORM_20261103/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/FORM_20261103/scenario.json","answers":{"q1_business":{"verdict":"賣給晶片廠的設計專用耗材：每顆新晶片設計都要一張專屬探針卡，錢卡在晶圓測試這一關；Q3營收2.805億美元、非GAAP毛利率56.5%（扣一次性約53%），現有廠房已滿載。","reasoning":"收錢方式：探針卡是設計專用耗材，每顆新晶片設計要一張專屬卡，晶片廠在晶圓測試時買卡、磨耗後再買；Systems部門賣工程探針台與TRITON光電測試系統。Q3 FY2026營收2.805億美元，季增9%、年增近四成，幾乎都在同一廠房做出來；其中Systems 5,950萬美元創新高（季增23%），其餘約2.21億為探針卡（逐字稿2026-10-28，CFO McKinnis）。探針卡毛利率55.3%、Systems 61%（約一半是不重複項）。非GAAP毛利率56.5%，含約380bp（1,050萬美元）關稅退款與量子業務零件成本，扣掉後52.5–53%；非GAAP營益率33.5%、GAAP 29.1%。分市場：DRAM與Q2紀錄持平但HBM降、DDR5升；Foundry & Logic季增約10%，動能來自資料中心CPU、首個GPU設計量產與客製ASIC。錢卡在哪：卡在晶圓測試，測試強度隨HBM堆疊、介面速度、先進封裝與光電上升；但每代新設計重新認證，客戶握有比稿權。單點依賴：SK hynix FY2025占22.9%，Q2 2026前三大客戶合計35%（去年同期48%），晶圓代工龍頭與CPU龍頭各約一成；集中度在降，記憶體一家仍是最大單點。產業時鐘在擴張期：SEMI預測設備銷售連五年成長到2028、記憶體供給緊到FY28、探針卡全產業產能吃緊、客戶談付費保產能；同時全產業一起擴產，是擴張後段的訊號。供需持久性：週期性將反轉，時點看2028年記憶體與測試新產能開出。產業態勢雙向拉鋸：需求結構轉好有來源，競爭也在惡化（見反證紀錄）。Q4營收指引2.85億±1,000萬美元，中點只比Q3多1.6%，原因是現有廠已到上限。","fact_refs":["f_kpi0_revenue_gaap","f_kpi1_non_gaap_operating_incom","f_kpi2_gaap_operating_income_ma","f_kpi3_free_cash_flow","f_kpi5_guidance_q4_fy2026_reven","f_kpi6_non_gaap_gross_margin","f_earnings_recency"],"verdict_values":{"revenue_quality":"品質高但有週期：耗材性質讓營收隨設計數與投片量走，不是一次性設備；但DRAM組合每季跟著客戶HBM／DDR投片比例移動，Q3毛利率含約380bp不重複項目，2023年營收曾年減11%。","unit_econ_note":"同一廠房營收年增近四成，靠週期時間、良率與人工效率；非GAAP營業費用占營收由Q2的25.4%降到Q3的23%。擴產前已到上限，德州廠2027年底才有約4億美元年化產能。","archetype":{"primary":"循環/商品","secondary":"品質複利成長","confidence":"中","fingerprint":"設計專用耗材＋半導體資本週期：2022–2025年毛利率39–40%、營益率1.5–7.7%，2023年營收年減11%；2026年營收首度破10億美元、基準毛利率升到53%。"},"industry":{"clock_phase":"II","sd_verdict_source":"SEMI 2026年中預測（設備銷售連五年成長、2028年約2,295億美元）與TrendForce轉述美光看法（記憶體供給緊到FY28、新產能約2028年開出）；判讀：週期性將反轉，時點在2028年新產能開出後。","bargaining":{"up":"部分零件來自單一或有限來源，多數供應商只下採購單、沒有長約，單一供應商漲價會壓毛利；FY2025關稅吃掉1.4個百分點毛利率。","down":"客戶集中：SK hynix FY2025占22.9%，Q2 2026前三大合計35%；短缺期客戶開始為加急與保留產能付費，但管理層說DRAM毛利改善極少來自漲價，議價權仍偏客戶。","geo":"中國營收占比FY2024 14%→FY2025 7%，受美國擴大出口許可影響；德州新廠屬回岸生產，獲德州2,420萬美元補助（2026-07-29法說）。"},"profit_pool_dir":"利潤池往高速與先進封裝測試移動：HBM最終堆疊測試、GPU／客製ASIC先進MEMS卡、CPO光電探針；行動處理器等傳統應用占比下降。5年前→現在的營業利益池占比事實表未涵蓋。","tam_table":[{"item":"探針卡市場規模（CFO，2026-05-11投資人日）","value":"約31億美元→2030年45億美元，年複合約8%；公司目標兩倍於市場成長"},{"item":"先進探針卡口徑（Sudhakar Raman，同場）","value":"28億→2030年40億美元，與CFO口徑不同"},{"item":"晶圓級CPO測試可服務市場（CFO）","value":"2030年約3–4億美元；TRITON 2025年營收0、2026年預期>3,000萬美元"},{"item":"NVIDIA相關潛在市場（德銀2026-10-01，第三方）","value":"約5億美元，2028年最高拿兩成、約2億美元年營收"},{"item":"公司營收","value":"2026年預期首度破10億美元（含Systems），2030目標16億美元"},{"item":"營業利益池占比5年前→現在","value":"事實表未涵蓋"}]}}},"q2_moat":{"verdict":"護城河方向持平：製造效率明顯變強，但定價權沒有跟著變強，全球第一的位置正被Technoprobe追過。","reasoning":"機制：MEMS探針技術加高速高並行測試架構（SmartMatrix），HBM最終堆疊測試最強；每張卡綁一顆設計，量產後整個設計壽命都綁定，但下一代重新比稿。可證方向有三條：一、製造效率變強——同一廠房營收年增近四成，基準毛利率由2022–2025年的39–40%升到53%（投資人日稱2025年起累計改善1,100bp）；二、定價權沒變強——短缺期管理層仍說DRAM毛利改善極少來自漲價，10-K承認競爭已造成降價；三、份額排名下滑——TrendForce預期Technoprobe 2026年超越公司成全球第一，GPU先進MEMS卡目前主要是對手的生意（2026-07-29 CEO Slessor），公司Q3才有第一個GPU設計量產。同業利潤率：公司TTM營益率約16%，低於Teradyne 33%、Advantest 46%、旺矽30%；同業表為GAAP口徑、含公司重整費用，最新一季GAAP營益率29.1%已接近旺矽。投入資本與ROIC事實表未涵蓋，改用利潤率差與份額當可比軸。評分：執行力7（效率與新廠進度都超前）、定價權5（短缺期沒漲價、排名下滑），合計約6分；方向給持平，不給向上。","fact_refs":["f_peer_form_gross_margin_pct","f_peer_form_operating_margin_pct","f_peer_form_fcf_margin_pct","f_peer_ter_gross_margin_pct","f_peer_ter_operating_margin_pct","f_peer_ter_fcf_margin_pct","f_peer_6857_t_gross_margin_pct","f_peer_6857_t_operating_margin_pct","f_peer_6223_two_gross_margin_pct","f_peer_6223_two_operating_margin_pct","f_peer_6223_two_fcf_margin_pct","f_peer_cohu_gross_margin_pct","f_peer_cohu_operating_margin_pct","f_kpi6_non_gaap_gross_margin","f_kpi2_gaap_operating_income_ma"],"verdict_values":{"moat":{"mechanism":"設計專用MEMS探針卡的認證綁定＋高速高並行測試技術（SmartMatrix、HBM最終堆疊測試）＋量產品質；綁定期等於單一設計壽命，下一代重新比稿。","execution":7,"pricing":5,"grade":"C","trend":"→","trend_evidence":"執行力擴大（基準毛利率51%→53%、新廠首張卡提前出貨）；定價權穩定偏弱（短缺期未漲價、10-K承認降價）；份額排名縮減（TrendForce指Technoprobe將成第一）。三者相抵為持平。","competitor_notes":[{"name":"Technoprobe","strategy_note":"最直接對手，TrendForce預期2026年成全球第一，是GPU先進MEMS卡的主要供應商；未在同業財務表內。"},{"name":"TER","strategy_note":"測試機龍頭之一，10月對公司投資3億美元並擴大合作；利潤率高於公司，是夥伴，也是潛在整合者。"},{"name":"6857.T","strategy_note":"Advantest，測試機龍頭，營益率46%遠高於公司；宣布邏輯測試機產能加倍，代表下游需求強，也代表全產業一起擴產。"},{"name":"6223.TWO","strategy_note":"旺矽，台灣探針卡廠，毛利率56.5%、營益率30%高於公司TTM，借AI浪潮拿份額；自由現金流為負，正在燒錢擴產。"},{"name":"COHU","strategy_note":"測試分選設備，營益率為負，是同產業在週期弱勢時的對照：需求一轉弱，固定成本壓垮利潤。"}],"peer_na_reason":"Technoprobe、MJC、中華精測等探針卡同業不在事實表同業財務表；同業ROIC與投入資本未提供。","threats":[{"level":"🟡","text":"Technoprobe與台廠（旺矽、中華精測、穎崴）在AI浪潮拿份額，TrendForce預期Technoprobe 2026年成全球第一；10-K承認競爭已造成降價與毛利下滑。","p":"40%","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#2","end_markets#2"]},{"level":"🟡","text":"對手獨立開發類似技術或繞過專利；每代新設計都重新比稿，技術領先要每一代重新證明。","p":"20%","evidence_refs":["substitute_technology#1"]},{"level":"🟡","text":"測試機大廠入股探針卡廠，若走向測試機加探針卡綁售，開放生態可能被打破；目前Teradyne投資公司並表態支持開放生態。","p":"15%","evidence_refs":["substitute_technology#2"]}],"roic_durability":{"quadrant":"利益率由低轉高（最新一季GAAP營益率29.1%，2022–2025年1.5–7.7%）×投入資本周轉率事實表未涵蓋","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者是客戶測試工程、決策者是客戶品質與產品部門、付款者是晶片廠，三環都成立；每顆新設計都必須做晶圓測試，屬「需要」不是「想要」，HBM每一代測試強度增加約25–30%（投資人日），光電需要已知良品晶粒測試。風險在量隨投片週期起伏，不在需求消失。"},{"item":"決策層級","level":"🟡","text":"替代性在「單一晶片設計×單一測試站」層級決定：設計量產後換卡要重新認證，等於綁定該設計壽命；但下一代設計重新比稿，HBM核心晶粒測試站競爭多，第三家HBM客戶份額較弱（2026-07-29 CEO Slessor）。綁定期短於一個產品世代。"},{"item":"價值鏈分配","level":"🟡","text":"探針卡占晶片成本小、但缺了不能出貨，理論上有定價空間；實際上客戶集中（SK hynix約四分之一營收）、測試機大廠入股探針卡廠，且短缺期公司仍未明顯漲價，只收加急與保產能費用。長期需求存在，不等於這一環能多拿。"},{"item":"社會容忍度","level":"🟢","text":"企業對企業的半導體零組件，沒有民生價格敏感問題，也不靠監管授權；政策風險在出口管制與關稅（中國營收占比已降到7%），列在風險項追蹤。"}],"roiic":35,"reinvest_rate":45,"endo_ceiling":16,"formula_note":"單位：%。增量ROIC約35%：德州廠2026–2027年現金資本支出約2.1億美元（2026年1–1.1億、2027年相近）＋預生產費用約0.3億＋營運資金估約0.75億，換約4億美元年化產能；以Q3非GAAP營益率33.5%、非GAAP稅率17.6%估稅後營業利益約1.1億，1.1÷3.15≈35%。再投資率約45%：擴產資本支出加營運資金增加，約占2027年稅後營業利益四到五成（折舊攤銷事實表未涵蓋，以維持性資本支出約占營收4–5%近似抵銷）。內生成長上界≈35%×45%≈16%。投入資本與當期ROIC事實表未涵蓋，以上依逐字稿數字推估。"}}}},"q3_growth":{"verdict":"後五年跑道中等：探針卡本業市場年增約8%，公司要靠GPU／ASIC份額與光電探針跑出兩倍速；第二曲線已有營收但規模還小。","reasoning":"成長來源以量為主：擴產（德州廠2027年底年化約4億美元探針卡產能）、GPU／客製ASIC／資料中心CPU份額、光電TRITON；價格貢獻小（管理層稱DRAM毛利改善極少來自漲價）；併購小（Keystone Photonics）；回購為零。共識三年EPS：FY2025A非GAAP 1.27美元（投資人日CFO）→FY2028E 5.88美元，年複合66.7%，但基期是低谷；改看FY2026E→FY2028E，年複合32.5%（Koyfin快照，分析師家數事實表未涵蓋）。內生上界約16%（推導見護城河段）。缺口約16.5個百分點，歸因利潤率擴張：毛利率由約40%升到53%、非GAAP營業費用占營收由Q1的27.4%降到Q3的23%——這是一次性台階，不會每年重複，2029年後成長回到內生上界附近。共識FY2028 EPS已高於公司2030年5美元目標，等於假設目標模型提早兩年兌現。跑道：探針卡已全面滲透，滲透率年限不適用；CFO口徑市場2030年45億美元、年增約8%，公司目標兩倍速靠份額。光電可服務市場2030年約3–4億美元，是有來源的第二條曲線，但只有公司目標營收的兩成上下，撐不起五年後的成長，給中等。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_3m_fy1_pct","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_kpi5_guidance_q4_fy2026_reven"],"verdict_values":{"growth":{"driver_mix":"量為主（擴產＋份額）、價為輔（加急與保產能費用）、併購小、回購零","runway_years":"不適用：探針卡已全面滲透，成長來自份額與測試強度","runway_post_y5":"🟡","endo_ceiling_basis":"增量ROIC約35%×再投資率約45%≈16%（德州廠資本支出與產能換算，見護城河段公式說明）","segments":[{"item":"Probe Cards（Q3 FY2026）","value":"約2.21億美元、毛利率55.3%；DRAM與Q2紀錄持平但HBM降、DDR5升；Foundry & Logic季增約10%"},{"item":"Systems（Q3 FY2026）","value":"5,950萬美元創新高、季增23%、毛利率61%（約一半來自不重複項）；TRITON 2026年預期>3,000萬美元，2025年為0"},{"item":"德州Farmers Branch","value":"首張量產卡已出貨，2027年線性爬坡到年化約4億美元探針卡產能，只做Foundry & Logic，騰出Livermore的DRAM產能"},{"item":"2030目標模型","value":"營收16億美元、非GAAP毛利率55%、營業費用占營收23%、EPS 5美元（2026-05-11投資人日）"}],"decay_signals":[{"signal":"毛利率連2季年減","lit":false,"evidence":"Q2、Q3毛利率皆創高"},{"signal":"核心市占近12個月縮減","lit":true,"evidence":"TrendForce預期Technoprobe 2026年超越公司成全球第一，台廠拿份額"},{"signal":"主力產品提價後銷量下滑","lit":false,"evidence":"未見提價"},{"signal":"EPS年複合高於營收年複合5個百分點以上","lit":true,"evidence":"共識FY2025A→FY2028E EPS年複合66.7%，營收FY2025→FY2027約年增29%"},{"signal":"自由現金流對淨利低於0.75連2年","lit":false,"evidence":"2025年0.22、2024年1.14，未連續；2026擴產期要再看"},{"signal":"SBC占營收高於5%且逐年上升","lit":false,"evidence":"Q3為3.1%"},{"signal":"TAM萎縮或被替代技術壓縮","lit":false,"evidence":"市場年增約8%，未見替代技術"},{"signal":"產業估值倍數近3年系統性下移","lit":null,"evidence":"事實表未涵蓋"},{"signal":"維持性資本支出占自由現金流高於60%","lit":null,"evidence":"事實表未涵蓋"},{"signal":"停止投資新產能且收入3年內下滑","lit":false,"evidence":"正在擴產"}],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"資本配置中等：現金先餵擴產，回購停擺，股權激勵稀釋低；Teradyne 3億美元投資的條款待揭露。","reasoning":"自由現金流對淨利：2022–2025年自由現金流6,650萬／860萬／7,910萬／1,170萬美元，淨利5,070萬／8,240萬／6,960萬／5,440萬，轉換率1.31／0.10／1.14／0.22，2023與2025兩年偏低但不連續，2025年低是投入新廠。2026年Q3自由現金流6,480萬美元、占營收23.1%，對GAAP淨利7,380萬約0.88。現金去向四分：一、擴產——新廠2026年現金資本支出1–1.1億美元（原估1.4–1.7億，差額移到2027），2027年相近；二、補強型併購——Keystone Photonics，金額與貢獻事實表未涵蓋；三、回購——2025年4月授權7,500萬美元，季末剩7,090萬，Q2、Q3都沒買，用途只是抵銷股權激勵；四、現金累積——季末現金與投資3.99億美元，總債務約2,800萬（含租賃）。SBC單季880萬美元，占營收3.1%、占GAAP營業利益10.8%，以現市值估年化稀釋約0.5%。Teradyne 10月投資3億美元強化資產負債表，管理層說不改變資本配置優先順序；是否為增資、價格與股數事實表未涵蓋。計分：併購已實現報酬無法計算；回購收益率約0，不過；股權激勵稀釋約0.5%／年，過。","fact_refs":["f_kpi3_free_cash_flow","f_kpi4_sbc_stock_based_compensa","f_net_debt_m","f_shares_diluted_m","f_ev_m"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":true,"passed":null,"input":"Keystone Photonics併購金額與營收貢獻事實表未涵蓋，已實現報酬無法計算"},{"name":"buyback_yield","applicable":true,"passed":false,"input":"Q2、Q3未回購；7,500萬美元授權僅用約410萬，回購收益率約0%"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"SBC單季880萬美元，年化約3,500萬，占市值約0.5%／年（低於1.5%）；Teradyne投資若為增資另計"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長靠內部擴產（德州新廠），不靠併購撐；回購只為抵銷股權激勵且近兩季未執行，展開沒有增量資訊"}}}},"q5_valuation":{"verdict":"現價要求FY2027–28共識大致兌現、毛利率守在53%上下；我只信一半，基準情境五年年化約8%，便宜建立在週期高點利潤率上。","reasoning":"現價90.01美元。FY2026共識EPS 3.35美元→本益比26.9倍；FY2027 4.24美元→21.2倍；FY2028 5.88美元→15.3倍。PEG以FY26→FY28共識年複合32.5%計為0.83；若用FY2025A低基期算三年年複合66.7%，PEG只有0.40，但那是低谷反彈，不採用。歷史位置只有四個年度端點、沒有連續五年分位：落後本益比41.3倍分位10.9%，市銷率7.17倍與EV／營收6.8倍分位100%——本益比看便宜、營收倍數看最貴，差的就是利潤率。現價要求：FY2027–28共識大致兌現，之後倍數不掉到15倍以下。我的基準情境FY2028 EPS 5.2美元（比共識低約12%），2029年小幅回落，FY2031 6.4美元×21倍≈134美元，五年年化約8%；Bear 3.0美元×16倍≈48美元。短期上檔：FY2027基準EPS 4.1×24倍≈98美元（+9%）；三年：FY2029基準4.8×21倍≈101美元（+12%）。成長熄火壓力測試：共識走到FY2028後成長降到15%／10%／5%、倍數壓到22／16／12倍，對應2030年股價約171／114／78美元，兩過一不過。賣方目標價64.64–210美元、平均145.55（2026-10-02，當時股價約149），高低差3.2倍、分歧大且已過時。淨現金約3.7億美元（另有Teradyne投資3億未入帳），EV約66.6億美元。結論：合理偏便宜，但便宜的分母就是爭點。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_fy1_pct","f_consensus_rev_3m_fy1_pct","f_pe_current","f_pe_percentile","f_ps_current","f_ps_percentile","f_ev_s_current","f_ev_s_percentile","f_ev_s_fwd","f_ev_m","f_net_debt_m"],"verdict_values":{"valuation":{"basis":"非GAAP前瞻本益比（FY1＝FY2026E），輔以FY2027E","tier":"半導體測試耗材（探針卡）","peers":{"expanded":false,"reason":"事實表同業對照只有利潤率、沒有倍數；Technoprobe、MJC等同類探針卡廠未收錄，無法做同類倍數對照，終端倍數改以公司自身現值為上限參考"},"fwd_pe":26.87,"peg":0.83,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"FY2026本益比26.9倍、FY2027約21.2倍；以FY26→FY28共識年複合32.5%算PEG 0.83，屬便宜區；但市銷率7.17倍與EV／營收6.8倍在近四個年度端點都是最高，落後本益比分位10.9%卻最低，兩者相反代表利潤率在高檔。五年連續分位事實表未涵蓋。合理偏便宜，但分母有爭議，結論為合理。","upside_short_pct":9,"upside_mid_pct":12,"denominator_disputed":true,"denominator_note":"FY2026非GAAP EPS含Q3約0.09美元關稅退款與Q4約70bp退款；FY2027–28共識建立在毛利率53–55%，而2022–2025年毛利率39–40%。分母是否為週期高點正是本案爭點，本益比便宜不能單獨當買進理由。"}}},"q6_how_wrong":{"verdict":"最可能看錯在把週期高點利潤率當新常態；陷阱風險中等（亮2個信號）。","reasoning":"最可能看錯的三處（詳見反證紀錄）：一、把週期高點毛利率當新常態；二、新廠開出時剛好遇上全產業擴產與記憶體新產能，量價齊跌；三、十月一個月跌約四成的原因不知道，可能是市場先看到我們沒看到的訊息。陷阱信號亮2個（核心市占相對縮減、EPS成長遠快於營收成長），屬中等。歷史最大回撤、空方最強數字：事實表未涵蓋；未見集體訴訟、SEC調查或財報重編，近12個月唯一重大8-K是2026年1月的重整與減損。管理層迴避紀錄：Q2法說未給週期時間與良率改善數字、未給新廠營收貢獻時點與CPO 2027年數字；投資人日未說明目標模型錨定什麼基準。Q3法說補了一部分（2027年底年化約4億美元、線性爬坡），但仍不量化2027年爬坡期毛利率逆風，只說「false sense of precision」。RSI 35、26週報酬−33%，沒有過熱。","fact_refs":["f_week26_return_pct","f_rsi14","f_price_at_dd","f_ma_state","f_ma_w52","f_ma_w104","f_ma_w250","f_ma_slope_w250_pct","f_ps_percentile"],"verdict_values":{"trap":{"verdict":"🟡","label":"週期高點利潤率陷阱風險中等"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":3.35,"pe":26.87,"basis":"FY2026E（FY1）非GAAP共識EPS，已過三季接近實現值；終端倍數同為非GAAP本益比"},"eps":{"bull":[4.6,6.2,7.2,8.1,9.0],"base":[4.1,5.2,4.8,5.6,6.4],"bear":[3.5,2.6,2.0,2.5,3.0]},"pe":{"bull":26,"base":21,"bear":16},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0,"net_buyback":0},"second_stage":{"bull_cagr_pct":12,"base_cagr_pct":8},"max_dd":{"lo":-65,"hi":-40,"basis":"起點90.01美元。Bear路徑谷底FY2029 EPS約2美元×15–20倍＝30–40美元，對應−55%～−67%；9月底到11月初一個月內已由149美元跌到90美元（約−40%），顯示單月就能跌四成；2023年營收年減11%時營益率掉到1.5%。取−40%～−65%。","trigger_time":null},"basis":{"bull":"德州廠2027年如期滿產並續擴下一期、GPU／客製ASIC拿到兩成份額、光電2030年達數億美元；毛利率55%以上，2031年營收約23–24億美元。終端26倍不高於公司現值26.9倍；同業現值倍數事實表未涵蓋（前份記載Technoprobe約121倍屬極端值，不作錨）。","base":"2027–28年貼近但低於共識（FY2028 5.2美元，比共識低約12%），2029年記憶體與測試新產能開出後小幅回落，2030年後回到內生上界附近成長；終端21倍為中循環倍數。","bear":"2027下半年起記憶體與AI測試降溫，全產業新產能同時開出，量價齊跌；2029年谷底營收約10億美元、毛利率約47%，EPS約2美元，2031年回到3美元；終端16倍取成長降到10%的熄火倍數。"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"評論指測試需求有週期性、強勢集中在AI／HBM與CPO；全產業同時擴產：公司新廠加約4億美元年化產能、Advantest宣布邏輯測試機產能加倍、旺矽自由現金流為負仍在擴產；記憶體新產能約2028年開出","assumption":"基準情境假設2028年仍強、2029年只小幅回落","consequence":"若反轉提前到2028年，FY2028 EPS落在2.5–3美元，股價對應40–50美元","ruling":"採納：Bear機率給30%（共識成長超過內生上界、全產業同步擴產、2023年營收年減11%的前例），Bear路徑2029年EPS約2美元。與唯一致命點部分重疊（兩者都打FY2028 EPS），但週期不是單一事件，唯一致命點仍選新廠","watch":"季營收年增率、SEMI年底設備預測是否下修、記憶體客戶資本支出指引","evidence_refs":["supply_demand_durability#3"],"fact_refs":["f_consensus_eps_fy3","f_rev_consensus_fy2_m"]},{"view":"論點失敗","evidence":"9月30日收149.31美元，11月2日90.01美元，26週報酬−33%；Q3優於指引後股價仍在52週均線之下；下跌原因事實表未涵蓋","assumption":"假設下跌是產業估值重估，而不是公司層級的壞消息","consequence":"若原因是客戶砍單、HBM規格下修或Teradyne投資條款不利，基準情境要往Bear移","ruling":"不可裁決至2027年2月Q4財報；在那之前不追價，只有76美元以下的價格條件可以分批","watch":"Q4財報首季指引、10-K揭露的Teradyne投資條款與股數","evidence_refs":["competitive_share_entrants#3"],"fact_refs":["f_price_at_dd","f_week26_return_pct","f_rsi14","f_ma_w52"]},{"view":"論點成功但股東經濟變差","evidence":"2026-01-09 8-K揭露重整與重大減損，重整費用約3,000–4,000萬美元；新廠預生產費用2026年2,500–3,000萬美元；Q3 GAAP EPS 0.93美元對非GAAP 1.04美元；Teradyne 3億美元投資若為增資，價格與股數事實表未涵蓋；7,500萬美元回購授權只用約410萬","assumption":"非GAAP調整項是一次性，股數大致持平","consequence":"若重整與爬坡費用年年出現，股東實拿的EPS比非GAAP低一成到一成五；擴產吃現金、回購停擺，抵不掉增資稀釋","ruling":"部分採納：情境EPS路徑已預留約3–5%股數增加；GAAP與非GAAP EPS差距連兩季超過15%列入警示","watch":"GAAP與非GAAP EPS差距、季末稀釋股數、10-K的Teradyne條款","evidence_refs":["major_events#0"],"fact_refs":["f_kpi1_non_gaap_operating_incom","f_kpi2_gaap_operating_income_ma","f_shares_diluted_m","f_kpi4_sbc_stock_based_compensa"]},{"view":"價格已反映太多","evidence":"市銷率7.17倍、EV／營收6.8倍都在近四個年度端點最高；共識FY2028 EPS 5.88美元已超過公司2030年5美元目標","assumption":"市場與賣方用現在的利潤率外推三年","consequence":"若營益率回到2024年約6%的水準，即使營收守住，合理股價遠低於現價","ruling":"部分採納：本益比看便宜、營收倍數看貴，落差就是利潤率爭點；分母有爭議，便宜論證不單獨成立，基準情境比共識低約12%","watch":"非GAAP毛利率、市銷率、共識修正方向","evidence_refs":[],"fact_refs":["f_ps_current","f_ps_percentile","f_ev_s_current","f_ev_s_percentile","f_pe_percentile","f_consensus_eps_fy3"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 137.84 → 本次 90.01（-34.7%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=137.84","side_b":"本次 price_at_dd=90.01","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]角色由 dd_decision.py 機械路由：前份 條件式衛星持倉 → 本次 追蹤","cause":"價格變動","prior_field":["dca_role"],"side_a":"前份 dca_role=條件式衛星持倉","side_b":"本次 dca_role=追蹤","ruling":"角色是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。沒有單一輸入能還原，屬多欄共同：估值 🟠→🟡、均線 ✅→🟡。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 137.84 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 137.84 美元：Bull 價 245.36、Bear 價 60.65，五年期望值 +13.0%，基準年化 3.3%，前份未列不對稱比","side_b":"本次情境、股價仍用 137.84 美元：Bull 價 234、Bear 價 48，五年期望值 −3.2%，基準年化 −0.5%，不對稱比 0.89","ruling":"先換情境、股價不動：五年期望值少 16.2 個百分點，基準年化少 3.8 個百分點。前份未列不對稱比，本次為 0.89。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 137.84 美元：五年期望值 −3.2%，基準年化 −0.5%，不對稱比 0.89","side_b":"本次情境、股價 90.01 美元：五年期望值 +48.2%，基準年化 8.3%，不對稱比 2.86","ruling":"再換股價、情境不動：起點價下跌 34.7%，五年期望值多 51.4 個百分點，基準年化多 8.9 個百分點，不對稱比由 0.89 升到 2.86。合計五年期望值比前份多 35.2 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"毛利率是結構性改善還是週期高點","cause":null,"prior_field":null,"side_a":"管理層：Q3扣一次性後毛利率52.5–53%，基準由上季51%再升2個百分點，來源是週期時間、良率與人工效率；2027年新廠爬坡期仍維持約53%，2030年目標55%（2026-10-28 CFO McKinnis）","side_b":"四年年報毛利率39–40%；Q2法說CFO自己把改善拆成三分之一成本、三分之一營收量、三分之一不重複（2026-07-29）；市銷率在近四個年度端點最高而本益比分位最低，是典型週期高點組合；FY2025關稅曾吃掉1.4個百分點，Q3的300bp退款只是還回來","ruling":"⚖不可調和（方向相反）。裁決：成本改善部分採信、量能部分不採信——投資人日把目標模型的毛利率改善拆成量能約600bp、營運效率約500bp、創新約400bp，量能那塊在需求下滑時會吐回；基準情境因此在2029年放一次回落，Bear機率維持30%。硬數據點：2027上半年新廠爬坡期毛利率（扣一次性）。","evidence_level":"一手：公司財報與法說原話","settle_metric":"2027年Q1、Q2非GAAP毛利率（扣關稅退款等一次性項目）","if_then":["若2027年Q1、Q2毛利率（扣一次性）皆≥52%且營收季增→採信結構性改善，基準情境FY2028 EPS上調到共識附近，達重啟條件後建首倉（目標部位三分之一）","若連兩季<50%→判定以週期為主，不進場；已有部位減碼至半倉","反向條件：毛利率守住但營收連兩季季減→需求先轉弱，不追，等營收恢復季增"],"evidence_refs":["reg_tariff_export#1"]},{"axis":"觀望或現在就買","cause":null,"prior_field":null,"side_a":"現在就買的最強論證：9月30日收149.31美元，11月2日剩90.01美元，一個月跌約四成，同期FY2026共識EPS三個月上修37%；FY2027本益比約21倍、FY2028約15倍；Q3營收、毛利率、EPS都高於指引上緣；淨現金約3.7億美元，另有Teradyne投資3億美元；新廠首張卡提前出貨","side_b":"等待的理由：下跌原因事實表未涵蓋，可能是市場先看到週期轉折；共識FY2028 EPS 5.88美元已超過公司2030年5美元目標；現有廠到頂，2027年成長全靠新廠；股價在52週均線之下，跌勢未止","ruling":"可調和（程度差異）：便宜是真的，但便宜的分母是週期高點利潤率。卡住進場的單一約束是新廠爬坡期毛利率是否守住，選擇等事件、不等反彈；若價格先跌而證據未到，跌到76美元以下且基本面未受損就分批反買，不當作停損訊號。","evidence_level":"一手價格與財報，下跌原因缺","settle_metric":"2027年2月Q4財報的首季營收與毛利率指引","if_then":["若股價≤76美元且Q4財報毛利率與新廠進度未受損→分批反買第一批（目標部位三分之一）","若股價先反彈站回52週均線但財報證據未到→不追"],"evidence_refs":["competitive_share_entrants#3"]},{"axis":"賣方共識與公司自己的目標","cause":null,"prior_field":null,"side_a":"共識FY2027 EPS 4.24美元、FY2028 5.88美元，FY2026三個月上修37%","side_b":"公司2026-05-11投資人日目標：2030年營收16億美元、毛利率55%、EPS 5美元；Q3法說仍以此為目標","ruling":"可調和（程度差異）：共識把公司目標提早兩年兌現，等於假設新廠一開出就被填滿、價格不掉。基準情境FY2028取5.2美元，比共識低約12%。賣方目標價64.64–210美元，高低差3.2倍，分歧大，信心與倉位角色都往保守調。","evidence_level":"賣方快照與公司目標","settle_metric":"FY2027實際營收對共識約13億美元","if_then":["若FY2027營收≥13億美元且毛利率≥53%→基準情境向共識靠攏","若FY2027營收<12億美元→基準情境降到Bear與Base中間，停止加碼"],"evidence_refs":["capital_markets_pricing#3"]},{"axis":"最大客戶占比：第三方說法與申報數字","cause":null,"prior_field":null,"side_a":"第三方稱Q1 2026 SK hynix占29.5%、NVIDIA 10.2%（未經一手文件核實）","side_b":"Q2 2026 10-Q：前三大客戶合計35%、SK hynix 24%，去年同期前三大48%；FY2025 SK hynix 22.9%","ruling":"採申報數字。集中度在下降，但仍高於FY2025；單一記憶體客戶占比門檻設30%。","evidence_level":"第三方未核實對一手申報","settle_metric":"10-K客戶集中度揭露","if_then":["若單一記憶體客戶占比>30%→風險升級，停止加碼"],"evidence_refs":["customer_concentration_credit#3","customer_concentration_credit#0"]},{"axis":"全球份額排名","cause":null,"prior_field":null,"side_a":"TrendForce 2026-06：Technoprobe可望2026年超越公司成為全球第一；GPU先進MEMS卡目前主要是對手的生意（2026-07-29 CEO Slessor）","side_b":"德銀2026-10-01：公司已是NVIDIA GPU探針卡第二大供應商；Q3已出貨單一GPU設計數百萬美元等級，2027年要大幅拿份額","ruling":"可調和：公司在GPU是從零起步拿份額，但整體排名在掉；護城河方向給持平，不給向上。","evidence_level":"第三方市調與賣方報告","settle_metric":"2027年GPU／客製ASIC量產設計數與Foundry & Logic年增率","if_then":["若2027年底前沒有第二個GPU或ASIC量產設計→基準情境下調，停止加碼"],"evidence_refs":["competitive_share_entrants#2","competitive_share_entrants#3","end_markets#2"]},{"axis":"產業態勢三軸","cause":null,"prior_field":null,"side_a":"結構轉好：HBM每代測試強度增加25–30%、光電需要已知良品晶粒測試；SEMI預測設備銷售連五年成長到2028，測試設備2027年+18.1%","side_b":"競爭惡化：10-K承認競爭已造成降價，TrendForce指Technoprobe將成第一、台廠拿份額；其他結構變數：出口管制使中國占比由14%降到7%，測試機大廠入股探針卡廠","ruling":"雙向拉鋸：需求面結構轉好有來源，競爭面也在惡化，兩者同時成立；護城河給持平，情境上檔不大幅超出公司目標。","evidence_level":"產業協會預測＋10-K＋第三方市調","settle_metric":"公司份額與毛利率同步方向","if_then":["若份額下滑且毛利率回落同時出現→減碼至半倉"],"evidence_refs":["supply_demand_durability#0","competitive_share_entrants#0","substitute_technology#2"]},{"axis":"估值結論與綜合評級（價格下跌）","cause":"價格變動","prior_field":["val","signal"],"side_a":"前份（2026-06-29，股價137.84美元）：估值偏貴、遠期本益比約50倍、綜合評級B級、裁決觀望","side_b":"本次股價90.01美元，跌約35%；FY2026共識EPS三個月由2.44上修到3.35，FY2026本益比降到26.9倍；估值由偏貴改為合理，綜合評級不變，裁決輸入仍是等事件驗證","ruling":"估值改善主因是價格下跌，其次是共識上修；但改善建立在共識利潤率上，分母有爭議，所以不升級為進場，維持等待。","evidence_level":"價格與共識快照","settle_metric":"2027年2月Q4財報","if_then":["若Q4財報達重啟條件→重跑研究後建首倉"],"evidence_refs":[]},{"axis":"護城河方向、陷阱風險、後五年跑道","cause":"新證據","prior_field":["moat_trend","trap","runway_post_y5"],"side_a":"前份：護城河持平、陷阱風險中等、後五年跑道中等","side_b":"本次三項結論不變但依據換新：正面是基準毛利率51%→53%、首個GPU設計量產、TRITON光電2026年>3,000萬美元、新廠首張卡提前出貨；負面是TrendForce指Technoprobe將成全球第一、共識EPS成長遠快於營收成長、現有廠到頂","ruling":"正負新證據互相抵銷，三項結論維持；若2027年底前拿到第二個GPU／ASIC量產設計且光電營收再翻倍，護城河方向才考慮改為向上。","evidence_level":"法說原話＋第三方市調","settle_metric":"2027年份額與光電營收","if_then":["若第二個GPU／ASIC量產設計落地且光電營收翻倍→護城河方向改評向上"],"evidence_refs":["competitive_share_entrants#2"]},{"axis":"公司類型、週期位置與情境機率","cause":"方法變動","prior_field":["archetype","cycle_position","p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份未標公司類型與週期位置；樂觀28%、悲觀30%、最大回撤−60%","side_b":"本次標為週期型（次類型品質成長）、中循環；情境改用FY2026非GAAP共識EPS為起點，基準情境放入2029年回落；樂觀25%、基準45%、悲觀30%；最大回撤區間−40%～−65%","ruling":"方法改變：前份把公司當結構性成長處理，本次依2023年營收年減11%、營益率掉到1.5%的前例改用週期框架；樂觀機率下調，因為共識已上修到公司2030年目標之上，上檔要再超出共識才成立。","evidence_level":"年度財報","settle_metric":"下一次營收年減年度的毛利率","if_then":["若下一次下滑年度毛利率≥47%→週期框架放寬，悲觀機率可下調"],"evidence_refs":[]},{"axis":"重啟條件（進場與加碼）","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"前份未設重啟條件（空白）","side_b":"2027年2月Q4財報首季營收指引中點≥2.85億美元且非GAAP毛利率中點≥52%，並且週收盤站回52週均線","ruling":"前份只有監測項目、沒有行動條件，本次補上。卡住進場的單一約束是新廠爬坡期毛利率是否守住，重啟條件就是它的否定，再加週線趨勢確認；觸發後先重跑研究再建首倉，不直接加碼。","evidence_level":"方法補正","settle_metric":"Q4財報指引與週收盤","if_then":["條件全中→重跑研究，通過後建首倉（目標部位三分之一）"],"evidence_refs":[]},{"axis":"減碼與清倉指標","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設減碼與清倉指標（空白）","side_b":"減碼：非GAAP毛利率（扣一次性）連兩季<50%；清倉：新廠2027年底產能目標低於3億美元或延到2028，或季營收年增連兩季為負且毛利率<48%，或最大記憶體客戶HBM最終測試導入量產第二供應商","ruling":"前份只有監測閾值、沒有對應動作；本次把毛利率基準升到53%後的回落幅度、新廠進度與HBM地位寫成可執行的減碼與清倉線。","evidence_level":"方法補正","settle_metric":"季報毛利率、新廠產能、客戶揭露","if_then":["毛利率連兩季<50%→減碼至半倉","新廠產能目標低於3億美元→清倉"],"evidence_refs":[]},{"axis":"Single Thing唯一致命點","cause":"新證據","prior_field":["single_thing"],"side_a":"前份未設唯一致命點（空白）","side_b":"Single Thing：德州Farmers Branch新廠在2027年底前達不到約4億美元年化探針卡產能","ruling":"Q3法說確認現有廠已到上限、Q4成長明顯放緩，2027–28年成長幾乎全押新廠，新廠成為數學上最大的單一敏感項（約占FY2028營收四分之一）；若發生則清倉。","evidence_level":"法說原話","settle_metric":"每季法說的新廠產能進度","if_then":["若產能目標下修到3億美元以下或延到2028→清倉"],"evidence_refs":[]},{"axis":"假設與風險門檻","cause":"新證據","prior_field":["H","R"],"side_a":"前份：非GAAP毛利率≥46%、DRAM／HBM營收年增≥15%、整體探針卡份額≥25%、FY2027遠期本益比>35倍","side_b":"本次：毛利率（扣一次性）≥51%、FY2027營收≥12.5億美元、最大客戶占比≤25%、下一次下滑年度毛利率≥47%；拿掉本益比門檻","ruling":"毛利率基準已升到53%，46%門檻失去警示作用；前份估值假設（本益比不破35倍）已被打破——本益比由約50倍降到26.9倍，這次改由情境樹處理估值，不再當成論點。份額門檻因缺市調更新，改用客戶與分市場指標。","evidence_level":"法說與共識快照","settle_metric":"2027年各季毛利率與營收","if_then":["若2027年毛利率（扣一次性）連兩季<51%→H1削弱，停止加碼"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"新廠爬坡期毛利率守住","type":"假設驗證","maps_to":"H1","metric":"非GAAP毛利率（扣一次性）","threshold":"2027年Q1、Q2皆≥52%且營收季增","action":"達標→重跑研究，通過後建首倉（目標部位三分之一）","source_freq":"每季財報","date":"2027-05","evidence_refs":[]},{"n":2,"text":"現有廠到頂後營收停滯","type":"風險","maps_to":"R1","metric":"季營收季增率","threshold":"2027年任一季季減","action":"停止加碼、不進場","source_freq":"每季財報","date":null,"evidence_refs":["geo_supply_chain#0","geo_supply_chain#2"]},{"n":3,"text":"新廠產能目標下修","type":"Single Thing","maps_to":"single_thing","metric":"公司公布的2027年底年化探針卡產能","threshold":"低於3億美元或延到2028","action":"清倉（若持有）；未持有則停止重啟條件","source_freq":"每季法說","date":"2027-12","evidence_refs":[]},{"n":4,"text":"2027年2月Q4財報首季營收指引中點≥2.85億美元且非GAAP毛利率中點≥52%，並且週收盤站回52週均線","type":"估值rearm","maps_to":"rearm_trigger","metric":"首季營收與毛利率指引；週收盤對52週均線","threshold":"營收指引中點≥2.85億美元、毛利率中點≥52%、週收盤>52週均線","action":"重跑研究，通過後建首倉（目標部位三分之一）","source_freq":"Q4財報＋每週","date":"2027-02","evidence_refs":[]},{"n":5,"text":"價格先跌、基本面未損時分批","type":"加碼","maps_to":"H2","metric":"股價與最近一季毛利率","threshold":"股價≤76美元且最近一季毛利率（扣一次性）≥51%、新廠進度未下修","action":"分批反買第一批（目標部位三分之一）","source_freq":"每日價格＋每季財報","date":null,"evidence_refs":[]},{"n":6,"text":"毛利率回落","type":"減碼","maps_to":"H3","metric":"非GAAP毛利率（扣一次性）","threshold":"連兩季<50%","action":"減碼至半倉","source_freq":"每季財報","date":null,"evidence_refs":["reg_tariff_export#1"]},{"n":7,"text":"週期反轉或HBM地位失守","type":"清倉","maps_to":"R3","metric":"季營收年增率；HBM最終測試供應地位","threshold":"季營收年增連兩季為負且毛利率<48%，或公司證實最大記憶體客戶導入量產第二供應商","action":"清倉","source_freq":"每季財報與10-Q","date":null,"evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#1"]},{"n":8,"text":"GPU／ASIC份額沒拿到","type":"風險","maps_to":"R2","metric":"GPU與客製ASIC量產設計數；Foundry & Logic年增率","threshold":"2027年底前沒有第二個量產設計，或Foundry & Logic年增<10%","action":"停止加碼，基準情境下調","source_freq":"每季法說","date":"2027-12","evidence_refs":["competitive_share_entrants#2","end_markets#2"]},{"n":9,"text":"關稅與出口管制吸收失敗","type":"風險","maps_to":"R4","metric":"關稅對毛利率的單季衝擊；出口限制涵蓋客戶","threshold":"單季衝擊≥1個百分點，或新限制涵蓋前五大客戶之一","action":"停止加碼","source_freq":"每季財報","date":null,"evidence_refs":["reg_tariff_export#0","reg_tariff_export#2"]},{"n":10,"text":"Q4 FY2026財報後複審","type":"複審日期","maps_to":null,"metric":"全份研究","threshold":"財報公布後一週內","action":"重跑研究","source_freq":"一次","date":"2027-02","evidence_refs":[]}],"kill_metrics":[{"metric":"非GAAP毛利率（扣關稅退款等一次性項目）","bear_threshold":"連兩季<50%→減碼至半倉","window":"2027–2028年各季","source":"公司季報新聞稿與法說會","last_status":"ok"},{"metric":"德州新廠2027年底年化探針卡產能目標","bear_threshold":"低於3億美元或延到2028→清倉","window":"2027年各季法說","source":"公司法說會（CFO McKinnis）","last_status":"ok"},{"metric":"季營收年增率","bear_threshold":"連兩季為負且毛利率<48%→清倉","window":"2027–2029年各季","source":"公司季報","last_status":"ok"},{"metric":"HBM最終堆疊測試供應地位","bear_threshold":"公司證實最大記憶體客戶導入量產第二供應商→清倉","window":"持續","source":"10-Q客戶集中揭露、法說會","last_status":"unknown"}],"evidence_dismissed":[],"action_conditions":{"rearm_trigger":"2027年2月Q4財報首季營收指引中點≥2.85億美元且非GAAP毛利率中點≥52%，並且週收盤站回52週均線","exec_line":"觸發後先重跑研究，通過才建首倉，首倉為目標部位三分之一；未觸發前不追價。另一條路：股價≤76美元且最近一季毛利率（扣一次性）≥51%、新廠進度未下修→分批反買第一批。"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":"中循環","cycle_verdict":"未觸發","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":false,"wait_for_price":true,"wait_for_price_condition":"等2027年2月Q4財報確認新廠爬坡期毛利率守住（首季非GAAP毛利率指引中點≥52%、營收指引中點≥2.85億美元）；或股價≤76美元且最近一季毛利率（扣一次性）≥51%","asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null},"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8(val爭議)","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='C'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟡', moat_trend='→', week26=-33.01, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='循環/商品', cycle_position='中循環', moat='C', moat_trend='→', cycle_gates_pass=False"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈機械讀數判定不可用，baseline rows 8/9/9b/10 的估值條件視為不可判 → 落 row8 觀望（保守方向）","hit":true,"basis":"val_denominator_disputed=True, val(機械讀數)='🟡'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":null,"requires_critic":[]},"thesis":{"H":[{"id":"H1","text":"德州Farmers Branch新廠2027年線性爬坡到年化約4億美元探針卡產能，爬坡期間非GAAP毛利率（扣一次性）守在約53%的基準","2y":"2027年各季毛利率（扣一次性）≥51%、FY2027營收≥12.5億美元、年底產能目標未下修","5y":null,"10y":null,"threshold":"非GAAP毛利率（扣關稅退款等一次性）≥51%；FY2027營收≥12.5億美元","source":"公司季報新聞稿與法說會（CFO每季更新新廠產能、預生產費用與基準毛利率）","drift_rule":"兩年期：TTM毛利率或營收偏離門檻連2季≥5%為削弱，連3季≥10%為反轉"},{"id":"H2","text":"營收從記憶體單腳走向多腳：GPU、客製ASIC、資料中心CPU與光電探針讓最大客戶占比下降，總營收仍成長","2y":null,"5y":"2030年營收≥14億美元（公司目標16億）、最大單一客戶占比≤20%、光電相關營收占比≥8%","10y":null,"threshold":"Foundry & Logic探針卡2027年起年增≥15%；最大單一客戶占營收≤25%","source":"10-K／10-Q客戶集中度揭露、法說會分市場說明、2026-05-11投資人日目標模型","drift_rule":"五年期：TTM偏離門檻連4季≥5%為削弱，連6季≥10%為反轉"},{"id":"H3","text":"毛利率改善有一大塊是結構性的：下一次需求下滑時，非GAAP毛利率不會回到2022–2025年的39–40%","2y":null,"5y":"下一次營收年減的年度，非GAAP毛利率≥47%、非GAAP EPS≥2美元","10y":null,"threshold":"營收年減年度的非GAAP毛利率≥47%；谷底非GAAP EPS≥2美元","source":"年度10-K與季報；對照2023年營收年減11%、營益率1.5%的前例","drift_rule":"五年期：TTM毛利率低於門檻連4季≥5%為削弱，連6季≥10%為反轉"}],"R":[{"id":"R1","text":"擴產卡關：現有廠房已到上限（Q4營收指引中點只季增約1.6%），德州廠若延誤，或單一來源零件、關稅打斷供應，2027上半年營收停滯、毛利率被爬坡成本吃掉","h_ref":"H1","clock":"⚡","threshold":"2027年任一季營收季減，或毛利率（扣一次性）連2季<51%","evidence_refs":["geo_supply_chain#0","geo_supply_chain#2"]},{"id":"R2","text":"份額之戰：TrendForce預期Technoprobe 2026年成全球第一，台廠借AI拿份額；GPU先進MEMS卡至今主要是對手的生意，10-K承認競爭已造成降價","h_ref":"H2","clock":"🔥","threshold":"2027年底前沒有第二個GPU或客製ASIC量產設計；Foundry & Logic年增<10%","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#2","end_markets#2"]},{"id":"R3","text":"記憶體客戶集中加週期：SK hynix FY2025占22.9%、單季最高25%，DRAM組合每季跟著HBM／DDR投片移動；記憶體新產能約2028年開出後需求降溫，探針卡量價齊跌","h_ref":"H3","clock":"🔥","threshold":"季營收年增轉負，或單一記憶體客戶占比>30%","evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#1","customer_concentration_credit#3"]},{"id":"R4","text":"出口管制與關稅：中國營收占比已由14%降到7%，單一來源零件遇上關稅與美中科技限制，可能再打斷供應或市場","h_ref":"H2","clock":"🐢","threshold":"關稅單季衝擊毛利率≥1個百分點，或新出口限制涵蓋前五大客戶之一","evidence_refs":["reg_tariff_export#0","reg_tariff_export#2"]}],"single_thing":{"description":"德州Farmers Branch新廠在2027年底前達不到公司說的約4億美元年化探針卡產能（MEMS前段延誤或良率過不了客戶認證）","why_fatal":"現有廠房已到上限（年化約11.4億美元），FY2028共識EPS 5.88美元需要約15–16億美元營收，缺口幾乎全靠新廠；新廠卡住時固定成本照付、GPU／ASIC份額也出不了貨，FY2028 EPS只剩約3.7–4美元，比共識低三成以上","if_happens":"基準情境改用Bear路徑前兩年；持有者清倉，未持有者停止重啟條件、降為觀察","how_monitor":"每季法說的新廠產能與出貨進度、預生產費用由營業費用轉入營業成本的金額、2027各季營收季增率是否≥5%","probability":"15%（12–24個月）：團隊過去一年半效率紀錄好、首張卡提前出貨，但MEMS前段2027年才導入"}},"appendix_a":{"growth_durability":6,"quality_score":6,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":21.23,"peg_fy2":0.65,"stress":{"pass":2,"total":3}},"eps_meta":{"base_eps_path":{"FY2025A":1.27,"FY2026E":3.35,"FY2027E":4.24,"FY2028E":5.88},"fy_end_month":12,"eps_basis":"非GAAP稀釋EPS（Koyfin共識）；FY2025A 1.27美元取自2026-05-11投資人日CFO原話"},"catalysts":[{"date":"2027-02","date_precision":"month","type":"guidance","event":"Q4 FY2026財報與2027年首季指引；10-K揭露客戶集中度與Teradyne投資條款","impact":"高","watch":"首季營收指引中點≥2.85億美元、非GAAP毛利率中點≥52%"},{"date":"2027-06","date_precision":"quarter","type":"capacity","event":"德州Farmers Branch加入Foundry & Logic的MEMS前段製程","impact":"高","watch":"預生產費用轉入營業成本的進度、年底約4億美元產能是否維持"},{"date":"2027-06","date_precision":"quarter","type":"product","event":"GPU與客製ASIC先進MEMS探針卡第二批量產設計","impact":"中","watch":"法說是否點名新設計量產、Foundry & Logic年增率"},{"date":"2026-12","date_precision":"month","type":"macro","event":"SEMI年底設備銷售預測更新","impact":"中","watch":"2027–2028年測試設備與DRAM設備預測是否下修"},{"date":"2027-09","date_precision":"quarter","type":"product","event":"TRITON／CPO與NPO光電測試2027年營收進度","impact":"中","watch":"2027年光電系統營收是否較2026年的3,000萬美元以上再翻倍"}]}
```

---

## ⑤ 覆蓋面（程式判定，你回的 ⑤ 燈號會被覆寫）

燈號 🟡：非核心軸無證據：regulatory_antitrust（法規／反壟斷）（尾部風險或事件型，不擋）。plan 時 archetype 為「品質複利成長」、判斷者歸「循環/商品」，循環/商品 的專屬核心軸未採證（不計燈號）：cyclical_inventory_price_position、cyclical_supply_discipline_capacity。

⑤ 的 reason 只需評論：空軸的查詢詞是否切題、判斷有沒有交代缺口對結論的影響。

---

## 尾段：回覆格式

只回一個 JSON 陣列，①–⑧ 每條一個元素，八個全出，不得跳號、不得多列，陣列外不得有任何文字（不加前言、不加 markdown 圍欄、不加附註）：

```json
[{"item": "①", "light": "🔴|🟡|🟢", "judgment_path": "$.路徑", "reason": "一句話"}]
```
