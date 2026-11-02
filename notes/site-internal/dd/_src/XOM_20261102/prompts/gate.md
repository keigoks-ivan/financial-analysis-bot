你是 DD 管線 v20 的判斷層閘（gate），標的 XOM（20261102）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（43 條）
- `f_kpi0_adjusted_earnings_identi`（q1_business）｜Adjusted earnings（排除 identified items）＝17505 USD m（每股 $4.23）｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-30）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 https://investor.exxonmobil.com/company-information/press-releases/detail/1213/exxonmobil-announces-third-quarter-2026-results（numbers.latest_quarter_kpis.items[0]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-30））
- `f_kpi1_gaap_earnings_attributab`（q1_business）｜GAAP earnings attributable to ExxonMobil＝15413 USD m（稀釋每股 $3.72）｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-30）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 https://investor.exxonmobil.com/company-information/press-releases/detail/1213/exxonmobil-announces-third-quarter-2026-results（numbers.latest_quarter_kpis.items[1]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-30））
- `f_kpi5_upstream_adjusted_earnin`（q1_business）｜Upstream adjusted earnings＝7300 USD m｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-30）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 https://investor.exxonmobil.com/company-information/press-releases/detail/1213/exxonmobil-announces-third-quarter-2026-results（numbers.latest_quarter_kpis.items[5]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-30））
- `f_kpi6_energy_products_adjusted`（q1_business）｜Energy Products adjusted earnings＝9100 USD m｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-30）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 https://investor.exxonmobil.com/company-information/press-releases/detail/1213/exxonmobil-announces-third-quarter-2026-results（numbers.latest_quarter_kpis.items[6]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-30））
- `f_kpi7_chemical_products_adjust`（q1_business）｜Chemical Products adjusted earnings＝725 USD m｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-30）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 https://investor.exxonmobil.com/company-information/press-releases/detail/1213/exxonmobil-announces-third-quarter-2026-results（numbers.latest_quarter_kpis.items[7]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-30））
- `f_kpi8`（q1_business）｜產量＝4496 koebd｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-30）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 https://investor.exxonmobil.com/company-information/press-releases/detail/1213/exxonmobil-announces-third-quarter-2026-results（numbers.latest_quarter_kpis.items[8]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-30））
- `f_peer_xom_gross_margin_pct`（q2_moat）｜XOM 毛利率＝20.63 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.XOM.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_xom_operating_margin_pct`（q2_moat）｜XOM 營業利益率＝10.72 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.XOM.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_xom_fcf_margin_pct`（q2_moat）｜XOM FCF 利潤率＝8.46 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.XOM.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_cvx_operating_margin_pct`（q2_moat）｜CVX 營業利益率＝12.37 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CVX.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_cvx_fcf_margin_pct`（q2_moat）｜CVX FCF 利潤率＝12.94 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CVX.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_shel_operating_margin_pct`（q2_moat）｜SHEL 營業利益率＝14.36 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.SHEL.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_shel_fcf_margin_pct`（q2_moat）｜SHEL FCF 利潤率＝11.63 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.SHEL.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_tte_operating_margin_pct`（q2_moat）｜TTE 營業利益率＝16.25 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.TTE.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_tte_fcf_margin_pct`（q2_moat）｜TTE FCF 利潤率＝10.5 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.TTE.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_cop_operating_margin_pct`（q2_moat）｜COP 營業利益率＝21.92 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.COP.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_cop_fcf_margin_pct`（q2_moat）｜COP FCF 利潤率＝15.89 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.COP.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝13.46 USD/share｜期間與口徑：2026-11-02／yfinance 分析師共識平均（Koyfin 快照無此檔）；幣別同報價｜kind：estimate
  - 來源：yfinance earnings_estimate（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-11-02）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝12.01 USD/share｜期間與口徑：2026-11-02／yfinance 分析師共識平均（Koyfin 快照無此檔）；幣別同報價｜kind：estimate
  - 來源：yfinance earnings_estimate（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-11-02）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝409366.33 USD m｜期間與口徑：2026-11-02／yfinance revenue_estimate 0y 平均（3 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-02）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝420143.61 USD m｜期間與口徑：2026-11-02／yfinance revenue_estimate +1y 平均（11 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-02）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi4_cash_capex`（q1_business）｜Cash capex＝7002 USD m｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-30）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 https://investor.exxonmobil.com/company-information/press-releases/detail/1213/exxonmobil-announces-third-quarter-2026-results（numbers.latest_quarter_kpis.items[4]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-30））
- `f_kpi2_cash_flow_from_operation`（q1_business）｜Cash flow from operations＝25650 USD m｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-30）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 https://investor.exxonmobil.com/company-information/press-releases/detail/1213/exxonmobil-announces-third-quarter-2026-results（numbers.latest_quarter_kpis.items[2]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-30））
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝4079.0 m shares｜期間與口徑：2026-11-02／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-11-02）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi3_fcf`（q4_capital）｜自由現金流（FCF，公司定義）＝19109 USD m｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-30）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 https://investor.exxonmobil.com/company-information/press-releases/detail/1213/exxonmobil-announces-third-quarter-2026-results（numbers.latest_quarter_kpis.items[3]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-30））
- `f_kpi9`（q1_business）｜股東回饋：股利＋買回＝9400 USD m（股利 4.3B＋買回 5.1B）｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-30）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 https://investor.exxonmobil.com/company-information/press-releases/detail/1213/exxonmobil-announces-third-quarter-2026-results（numbers.latest_quarter_kpis.items[9]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-30））
- `f_kpi10_net_debt`（q1_business）｜Net debt＝22100 USD m（總債務 34.3B－現金 12.2B）｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-30）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 https://investor.exxonmobil.com/company-information/press-releases/detail/1213/exxonmobil-announces-third-quarter-2026-results（numbers.latest_quarter_kpis.items[10]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-30））
- `f_kpi11`（q1_business）｜管理層指引＝2027 年買回 $20B（假設市況合理）；Q4 股利 $1.07/股（12/10 發放，11/16 登記）。新聞稿未提供 Q4／全年產量或 capex 指引 —｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-10-30）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司 IR 新聞稿 https://investor.exxonmobil.com/company-information/press-releases/detail/1213/exxonmobil-announces-third-quarter-2026-results（numbers.latest_quarter_kpis.items[11]，as_of Q3 2026（季末 2026-09-30，公告於 2026-10-30））
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝2.2 %｜期間與口徑：2026-11-02／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-11-02）
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝19.26 x｜期間與口徑：2026-10-30（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-10-30（RTH 收盤，UTC））
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝187.25 USD｜期間與口徑：2026-10-30（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-10-30（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝100.0 %｜期間與口徑：2026-10-30（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-10-30（RTH 收盤，UTC））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝1.97 x｜期間與口徑：2026-10-30（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-10-30（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝100.0 %｜期間與口徑：2026-10-30（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-10-30（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝2.02 x｜期間與口徑：2026-10-30（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-10-30（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝100.0 %｜期間與口徑：2026-10-30（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-10-30（RTH 收盤，UTC））
- `f_ev_s_fwd`（q5_valuation）｜EV/S（EV ÷ FY1 共識營收）＝1.92 x｜期間與口徑：2026-11-02／f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）｜kind：estimate
  - 來源：—（numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m，as_of 2026-11-02）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_ev_m`（q5_valuation）｜目前企業價值 EV（市值＋淨負債）＝785889.79 USD m｜期間與口徑：2026-11-02／市值 763792.79 ＋ 淨負債 22097.0｜kind：realized
  - 來源：—（numbers.capital_structure.ev_m，as_of 2026-11-02）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝22097.0 USD m｜期間與口徑：2026-11-02／yfinance 最新一季：總債務 34250.0、現金 12153.0（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-02）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝24.22 %｜期間與口徑：2026-10-30（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-10-30（RTH 收盤，UTC））
- `f_ma_w52`（q5_valuation）｜52 週均線＝146.01 USD｜期間與口徑：2026-11-02／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-02）
- `f_ma_w104`（q5_valuation）｜104 週均線＝126.01 USD｜期間與口徑：2026-11-02／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-02）
- `f_ma_w250`（q5_valuation）｜250 週均線＝107.43 USD｜期間與口徑：2026-11-02／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-02）

### findings_digest 中方向為負或來源衝突的條目（16 條）
- `supply_demand_durability#0`（supply_demand_durability｜方向 -｜狀態 ok）：IEA June 2026 first 2027 balances: supply up ~8 mb/d to 110.3 mb/d vs demand 105.3 mb/d, implying ~5 mb/d surplus, tied to Gulf production recovery and OPEC+ higher targets
  - 來源：The Logic / Argus Media: IEA cuts 2026 demand forecast, sees huge 2027 surplus（as_of 2026-06-11）｜affects：thesis.R、decision_inputs.bear、valuation
- `supply_demand_durability#1`（supply_demand_durability｜方向 -｜狀態 ok）：EIA expects 2027 global oil balance surplus of ~3.7 MMBbl/d, driven by UAE output outside OPEC quotas and softer demand
  - 來源：Aegis Hedging: EIA outlook points to oversupplied oil market by 2027（as_of 2026-07-01）｜affects：thesis.R、decision_inputs.bear
- `regulatory_antitrust#0`（regulatory_antitrust｜方向 -｜狀態 ok）：Clean Hydrogen Works 在德州商業法院把 Exxon 加為被告，指控 Exxon 封鎖對手使用 CO2 管線網路後啟動自家潔淨能源專案（反壟斷主張）；為私人訴訟，非政府調查。
  - 來源：Bloomberg Government - Exxon Pulled Into Pipeline Monopoly Spat in Texas Business Court（as_of 2026-02-01）｜affects：decision_inputs.bear、thesis.R
- `regulatory_antitrust#1`（regulatory_antitrust｜方向 -｜狀態 ok）：密西根州指控 ExxonMobil、Chevron 等石油大廠合謀減緩能源轉型、壓低再生能源產出（Sherman Act 第 1 條等）；被告已聲請駁回，搜尋結果未確認後續狀態。
  - 來源：WebSearch 摘要（Global Competition Review / 新聞聚合）（as_of 2026-01-01）｜affects：decision_inputs.bear、thesis.R
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：Exxon CEO Woods called Venezuela 'uninvestable' after Maduro's removal, citing two prior expropriations; Guyana Stabroek (Exxon 45%) has ~30% acreage unexplored due to Guyana-Venezuela territorial dispute.
  - 來源：Reuters via BOE Report: Geopolitics loom large over Big Oil earnings as investors seek Venezuela details（as_of 2026-01-29）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：Two Qatar LNG trains (S4, S6) at ExxonMobil-QatarEnergy JV damaged amid Hormuz disruption; ~3% of Exxon global production, multi-year repair; Golden Pass Texas started LNG March 2026.
  - 來源：Exxon Mobil FY2026 Q1 earnings summary (fn2.ai)（as_of 2026-07-28）｜affects：thesis.R、decision_inputs.bear、valuation
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：IEA Global EV Outlook 2026 稱2025年EV已替代全球約170萬桶/日石油消費（2020年為40萬），2025全球EV銷量約2,000萬輛、占新車四分之一；預期2030年替代量近三倍至約500萬桶/日。2026Q1全球EV銷量因中美政策放緩年減8%。
  - 來源：ThisDay, Report: Electric Vehicles Cut Global Oil Demand by 1.7m bpd as Sales Top 20m (引IEA Global EV Outlook 2026)（as_of 2026-06-01）｜affects：moat_trend、thesis.R、decision_inputs.bear
- `substitute_technology#1`（substitute_technology｜方向 -｜狀態 ok）：IEA分析：中東戰爭致油價波動，至4月EV駕駛人運行成本節省提高20%-45%，為EV替代提供助力
  - 來源：S&P Global / Hellenic Shipping News, Global oil shock offers boost for EV switching, fossil phaseout: IEA（as_of 2026-07-30）｜affects：moat_trend、thesis.R
- `major_events#2`（major_events｜方向 -｜狀態 ok）：加州檢察總長就 Exxon 先進塑膠回收計畫起訴，指其誤導大眾（頁面日期 2026-06-23）。
  - 來源：Energy Intelligence：California Sues Exxon Over Plastics Recycling（as_of 2026-06-23）｜affects：thesis.R、decision_inputs.bear
- `cyclical_supply_discipline_capacity#1`（cyclical_supply_discipline_capacity｜方向 -｜狀態 ok）：Energy Intelligence：XOM計畫至2027年新增50萬boe/d，Chevron預期年產量成長超過3%；多數majors上游產量持續成長，成長來自Ballymore、Uaru等新專案（產能擴張而非收縮）。
  - 來源：Energy Intelligence, No End in Sight for Oil Majors' Upstream Growth（as_of 2026-01-01）｜affects：thesis.R、decision_inputs.bear
- `cyclical_inventory_price_position#1`（cyclical_inventory_price_position｜方向 -｜狀態 ok）：JPMorgan下修Brent預測：2026Q3均價約86美元、Q4約80美元、年底78美元、2027均價64美元（價格預期走低方向）。
  - 來源：KuCoin News: JPMorgan downgrades Brent crude outlook for 2026 and 2027（as_of 2026-07-01）｜affects：valuation、decision_inputs.bear
- `cyclical_prior_downcycle_behavior#0`（cyclical_prior_downcycle_behavior｜方向 -｜狀態 ok）：XOM 2020 全年虧損 224 億美元（主因資產減損），為 1999 合併以來首次年度虧損；扣除減損約虧 14 億，2019 同口徑盈 96 億
  - 來源：abc17news (AP) ExxonMobil reports its first annual loss since its merger（as_of 2021-02-02）｜affects：decision_inputs.bear、thesis.R
- `cyclical_prior_downcycle_behavior#1`（cyclical_prior_downcycle_behavior｜方向 -｜狀態 ok）：XOM 股價 2020 年下跌約 40.9%（S&P Global Market Intelligence）
  - 來源：Motley Fool, Why Exxon Mobil stock lost more than 40% in 2020（as_of 2021-01-05）｜affects：decision_inputs.bear、valuation
- `cyclical_prior_downcycle_behavior#2`（cyclical_prior_downcycle_behavior｜方向 -｜狀態 ok）：2014–2016 週期：2015 年 XOM 全年獲利約 162 億美元，約為 2014 年 325 億的一半；2015Q4 獲利年減 58% 至 28 億，為 2002 年以來最低單季
  - 來源：IndustryWeek, ExxonMobil Profits Drop 58% in 4Q（as_of 2016-01-29）｜affects：decision_inputs.bear、thesis.R
- `cyclical_prior_downcycle_behavior#3`（cyclical_prior_downcycle_behavior｜方向 -｜狀態 ok）：Brent 2014 下半年跌約 50%；2016 年初較 2014 高點（逾 $100）低約 70%，跌破 $30
  - 來源：Motley Fool, Big problems ahead for Big Oil in 2016（as_of 2015-12-20）｜affects：decision_inputs.bear、thesis.R
- `lawsuit_class_action#1`（lawsuit_class_action｜方向 -｜狀態 ok）：加州檢察總長就塑膠回收計畫起訴 Exxon（頁面日期 2026-06-23）。
  - 來源：Energy Intelligence：California Sues Exxon Over Plastics Recycling（as_of 2026-06-23）｜affects：thesis.R

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 4 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/XOM_20261102/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":228.8,"bear_5y_price":96.2,"p_bull_pct":20,"p_bear_pct":35,"upside_5y_pct":-11.1,"ev5y_pct":-17.6,"irr_base_pct":-2.3,"asym_ratio":0.3,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":13.46,"pe":13.91,"basis":"FY2026E 共識 EPS 13.46（當年度，Q4 尚未公布），起點本益比＝187.25÷13.46；終端倍數同樣套在終端年 FY2031E 當年度 EPS，分母同口徑"},"eps":{"bull":[13.0,12.4,12.9,13.6,14.3],"base":[11.4,10.0,10.3,10.7,11.1],"bear":[9.6,7.0,6.6,7.0,7.4]},"pe":{"bull":16,"base":15,"bear":13},"p":{"bull":20,"base":45,"bear":35},"yield_pct":{"dividend":2.2,"net_buyback":2.6},"second_stage":{"bull_cagr_pct":4,"base_cagr_pct":2},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### XOM_Q2_2026_Earnings_Call_20260731.md
- 2026-07-31｜Neil Hansen｜guidance：CFO 稱 2030 年 Guyana 自由現金流將為 2025 年的 2 倍（原話："we're going to see 2x the level of free cash flow in 2030 than we saw in 2025"）
- 2026-07-31｜Neil Hansen｜commitment：結構性成本節省累計目標 2030 年達 200 億美元（原話："we plan to get to $20 billion by 2030"）
- 2026-07-31｜Darren Woods｜margin：結構性成本節省自 2019 年累計達 163 億美元（原話："Cumulative structural cost savings have increased to $16.3 billion since 2019"）
- 2026-07-31｜Darren Woods｜margin：排除生產稅與能源價格後，現金成本年增持平（原話："we're basically holding cash costs flat"）
- 2026-07-31｜Darren Woods｜risk：Q2 暫時損失約 10% 上游產量（中東衝突）（原話："approximately 10% of our upstream production"）
- 2026-07-31｜Darren Woods｜margin：化學品利潤相較 Q1 增約 180%（原話："roughly 180% increase in chemical product margins"）
- 2026-07-31｜Neil Hansen｜margin：Energy Products 占各事業線獲利比重五年由約 9% 升至約 23%（原話："it's gone from about 9% to about 23% in the last 5 years"）
- 2026-07-31｜Darren Woods｜guidance：CEO 預期煉油市場維持高利潤（原話："a very robust refining market with very high margins"）
- 2026-07-31｜Neil Hansen｜margin：CFO 回應煉油獲利低於市場預期：歸因於變數多，稱無根本疑慮（原話："no underlying concerns with how that business has performed"）
- 2026-07-31｜Darren Woods｜product：第五艘 FPSO Errea Wittu 預計年底前投產（原話："remains on track for start-up by the end of the year"）
- 2026-07-31｜Darren Woods｜product：Longtail 朝最終投資決策推進（原話："Longtail is on the path toward final investment decision"）
- 2026-07-31｜Darren Woods｜capital_allocation：正在評估第九艘 FPSO；計畫將於年底定案（原話："we are evaluating the potential for a ninth FPSO"）
- 2026-07-31｜Darren Woods｜guidance：Guyana 成本回收提前，產量權益（entitlement）將調整並反映在 2030 計畫（原話："our volume entitlements will change"）
- 2026-07-31｜Neil Hansen｜guidance：CFO 說明 Guyana 已回收 550 億美元投資，稱此為自由現金流轉折點（原話："we fully recovered the $55 billion of investment"）
- 2026-07-31｜Neil Hansen｜guidance：回應分析師框架提問：CFO 同意是自由現金流轉折而非單純權益下降（原話："That's very much an inflection into free cash flow."）
- 2026-07-31｜Darren Woods｜product：Guyana 去飽和（desaturation）時點因價格與執行而提前，原預期為今年稍晚或明年初（原話："that's obviously come forward now with where prices have been"）
- 2026-07-31｜Darren Woods｜product：Guyana 長期探勘仍有潛力，AI 工具辨識新探勘機會（原話："the tape hasn't run out on this play yet"）
- 2026-07-31｜Darren Woods｜product：Permian 單季產量創紀錄，超過 180 萬油當量桶/日（原話："more than 1.8 million oil equivalent barrels per day"）
- 2026-07-31｜Darren Woods｜competition：CEO 稱技術組合接近 2018 年提出的「採收率倍增」目標（原話："we're getting really close to that objective"）
- 2026-07-31｜Darren Woods｜guidance：Permian 新增外送管線後，CEO 認為驅動力是無瓶頸外送與最大化油產（原話："the real driver will be unconstrained takeaway capacity"）
- 2026-07-31｜Neil Hansen｜competition：管理層自稱大型專案數量約為最近 IOC 對手的兩倍（原話："twice the number of mega projects in our nearest IOC"）
- 2026-07-31｜Darren Woods｜capital_allocation：新機會的投資門檻：須相對同業具備優勢（原話："have an advantage versus what others in the industry can do"）
- 2026-07-31｜Neil Hansen｜competition：Permian 逾 3 英里長水平井數量為對手的數倍（原話："we have 1,200 wells"）
- 2026-07-31｜Darren Woods｜product：管理層稱將持續擴大餾分油（distillate）、航煤與基礎油產量，墨西哥灣沿岸有專案開發中（原話："continue to grow distillate, jet, and basestock production"）
- 2026-07-31｜Neil Hansen｜margin：今年歲修相較上一輪成本與工期的改善幅度（原話："a 30% improvement in cost and a 60% improvement in duration"）
- 2026-07-31｜Darren Woods｜risk：歐洲暴利稅：CEO 稱上次課徵後公司取消了對歐洲的規劃投資（原話："So we canceled investments that we had planned for Europe"）
- 2026-07-31｜Darren Woods｜risk：荷莫茲海峽：CEO 預期即使清除阻礙後航運恢復仍需時間（原話："there's going to be a continued inhibition for movement"）
- 2026-07-31｜Darren Woods｜risk：CEO 表示無法預測海峽何時恢復通行（原話："I can't really predict when it will happen"）
- 2026-07-31｜Darren Woods｜commitment：與卡達能源討論協助修復受損 LNG 產線（原話："We're in discussions with QE about that."）
- 2026-07-31｜Darren Woods｜risk：LNG 中東曝險：不把當前事件外推為長期區域穩定性改變（原話："we're not extrapolating current events"）
- 2026-07-31｜Darren Woods｜guidance：Mozambique LNG 目標今年稍晚做最終投資決策（原話："we hope to FID that project later this year"）
- 2026-07-31｜Darren Woods｜commitment：管理層稱未來尋找新機會時不會迴避中東地區（原話："we won't shy away from the region"）
- 2026-07-31｜Darren Woods｜margin：Specialty Products 基礎油利潤創高（原話："best ever basestock margins"）
- 2026-07-31｜Darren Woods｜product：Proxxima 產能擴建：下一階段摻配廠今年稍早已 FID，管理層稱滲透需時（原話："FID-ed the next large step in our Proxxima blending plant"）
- 2026-07-31｜Darren Woods｜capital_allocation：本季資本支出約 70 億美元（原話："Cash capital expenditures were roughly $7 billion"）
- 2026-07-31｜Darren Woods｜capital_allocation：本季透過股息與回購回饋股東超過 90 億美元（原話："we returned more than $9 billion to shareholders"）
- 2026-07-31｜Darren Woods｜guidance：全公司流程與數據平台轉型，大規模部署排在 2027（原話："larger rollouts in 2027"）
- 2026-07-31｜Darren Woods｜commitment：上游併入全球營運組織後，管理層預期改善利潤（原話："we expect to deliver improved margins"）
- 2026-07-31｜James Chapman｜commitment：公司預告 9 月發布年度全球展望（原話："we plan to publish our annual global outlook in September"）
- 2026-07-31｜Darren Woods｜customer：供應鏈調度避免約 7.5 億美元年化中斷成本（原話："helped avoid roughly $750 million in annual disruption cost"）
- 2026-07-31｜Darren Woods｜risk：Kashagan 擴建討論：管理層稱仍處早期（原話："we're too early in that process"）

### 問答異常語氣（迴避／改口／保留）
- XOM_Q2_2026_Earnings_Call_20260731.md｜問：Arun Jayaram（JPMorgan）問荷莫茲海峽現況與 7 月情形｜答法：CEO 表示沒有太多額外的現場觀點，轉述媒體已報導，並改談市場影響與航運意願，未給 7 月具體情況
- XOM_Q2_2026_Earnings_Call_20260731.md｜問：Neil Mehta（Goldman）問煉油獲利低於獨立煉廠預期，以及 Q3 走勢｜答法：CEO 與 CFO 以產品組合差異、變數多、預測難度解釋，未提供 Q3 數字或具體時點/營運因素拆解
- XOM_Q2_2026_Earnings_Call_20260731.md｜問：Biraj Borkhataria（RBC）問歐洲暴利稅發生的可能性及與決策者的討論｜答法：CEO 以政策批評作答，說「不確定是否能阻止他們」，未給出可能性判斷或對公司影響數字
- XOM_Q2_2026_Earnings_Call_20260731.md｜問：Bob Brackett（Bernstein）問歲修延後與把握高價機會的取捨｜答法：CFO 說「若能安全延後則納入考量」，改談歲修成本與工期改善，未說明本年實際延後的規模

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 3 | 2 |
| customer_second_source | not_applicable | 0 | 0 |
| customer_concentration_credit | found | 1 | 2 |
| supply_demand_durability | found | 6 | 4 |
| regulatory_antitrust | found | 3 | 3 |
| reg_tariff_export | none | 0 | 3 |
| geo_supply_chain | found | 3 | 2 |
| end_markets | found | 3 | 3 |
| substitute_technology | found | 2 | 2 |
| channel_business_model_shift | found | 1 | 2 |
| capital_markets_pricing | found | 4 | 3 |
| major_events | found | 3 | 4 |
| cyclical_supply_discipline_capacity | found | 3 | 3 |
| cyclical_inventory_price_position | found | 3 | 2 |
| cyclical_prior_downcycle_behavior | found | 4 | 2 |

未涵蓋／不適用軸的查詢詞原文（供判相關性）：
- **customer_second_source**（not_applicable）：（無查詢記錄）
- **reg_tariff_export**（none）：ExxonMobil tariff section 232 steel 2026；ExxonMobil export control OR entity list OR sanctions 2026；ExxonMobil China tariff OR trade restriction 2026

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"status":"no_prior_dd"}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"XOM","date":"2026-11-02","schema":"v15.0","contract":"v19","company_name":"ExxonMobil Holdings Corporation"},"oneliner":"XOM 體質比上個循環好（成本節省、Guyana 與 Permian 放量、債少），但 187 美元買到的是荷莫茲中斷期的高峰獲利：FY2026 共識 EPS 13.46 約為去年 6.70 的兩倍，以近三年實際 EPS 平均計約 24 倍；2027 原油過剩在前，不追，等約 145 美元或價差正常化後再評","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/XOM_20261102/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/XOM_20261102/scenario.json","answers":{"q1_business":{"verdict":"賺油價與煉油價差的錢：上游賣原油、天然氣與 LNG，下游煉油、化工與特用品；本季錢卡在煉油節點，Energy Products 調整後盈餘 91 億美元，占全公司 175 億的一半以上，屬中斷期的超額價差","reasoning":"分部：事實表未涵蓋分部營收，以 Q3 2026 分部調整後盈餘代替。Upstream 73 億（較 Q2 下滑，原油價格走低）、Energy Products 91 億（Q2 約 41 億）、Chemical Products 7.25 億（Q2 約 12 億）、Specialty Products 約 13 億；全公司調整後 175 億（每股 4.23）、GAAP 154 億（稀釋每股 3.72）。利潤率：最新一季毛利率與營益率事實表未涵蓋，TTM 到 2026-06 毛利率 20.6%、營益率 10.7%。產業時鐘判 III 過熱：荷莫茲受阻、中東煉廠受襲、俄羅斯約一半煉能下線，煉油價差因此創高（Q3 法說 Woods）；原油價格本季已回落，IEA 與 EIA 都預估 2027 年供給過剩。供需持久度：週期性將反轉。成品油短缺取決於停火與修復，管理層估至少延續到明年；原油端 2027 年過剩 370 至 500 萬桶/日。議價：錢卡在煉油與上游資源兩個節點；客戶端沒有集中度（美國品牌站點約 1 萬個），商品化產品沒有定價權。單點依賴：Guyana Stabroek（XOM 45%）是量與現金流轉折的主軸，約 30% 面積因委內瑞拉邊界爭議擱置；本季獲利的另一個依賴是中斷期價差。產業態勢：雙向拉鋸。競爭面在惡化，majors 上游持續擴產（XOM 2027 年前加 50 萬桶油當量/日、CVX 年增逾 3%），加上 2027 年過剩；另一面，Rystad 估非 OPEC 產量 2027 年見頂，天然遞減率約 15%/年（公司展望），支撐中期投資需求","fact_refs":["f_kpi0_adjusted_earnings_identi","f_kpi1_gaap_earnings_attributab","f_kpi5_upstream_adjusted_earnin","f_kpi6_energy_products_adjusted","f_kpi7_chemical_products_adjust","f_kpi8","f_peer_xom_gross_margin_pct","f_peer_xom_operating_margin_pct"],"verdict_values":{"revenue_quality":"營收由商品價格決定（price-taker）。FY2023 至 FY2025 營收連三年持平到下滑（年報 −16.1%、+1.4%、−4.5%）；FY2026 共識營收回升到 4,094 億，主因是價格，不是量","unit_econ_note":"Q3 2026：營業現金流 256.5 億、現金資本支出 70 億、公司定義自由現金流 191 億；產量 449.6 萬桶油當量/日；股利 43 億＋回購 51 億","archetype":{"primary":"循環/商品","secondary":null,"confidence":"高","fingerprint":"整合型油氣，獲利跟著油價與價差擺動：2020 年度虧損 224 億、2015 年獲利約為 2014 年一半；EPS 由 FY2022 13.26 降到 FY2025 6.70，再被中斷期推回 FY2026 共識 13.46"},"industry":{"clock_phase":"III","sd_verdict_source":"週期性將反轉。IEA 2026 年 6 月首份 2027 平衡表估供給增約 800 萬桶/日、過剩約 500 萬桶/日，與波斯灣產量恢復、OPEC+ 提高目標連動；EIA 估 2027 過剩約 370 萬桶/日；成品油緊張取決於荷莫茲復航與俄羅斯煉廠修復","bargaining":{"up":"上游的對手是資源國。Guyana 已回收 550 億美元投資，權益量將調整（Q2 法說），分成往政府端移","down":"賣給批發、零售與工業客戶，產品可完全替代，價差由全球供需決定，沒有議價權","geo":"卡達 LNG 兩列受損、阿聯產量出口受阻（Q3 法說）；Guyana 與委內瑞拉有邊界爭議"},"profit_pool_dir":"中斷期利潤池移向煉油環節（Energy Products 由 Q2 約 41 億升到 Q3 91 億）；常態化後回流上游，長期往資源國與低碳替代移","tam_table":{"expanded":false,"reason":"成熟商品市場，不是低滲透或份額擴張的故事；需求總量改看 IEA、EIA、OPEC 機構預測，已寫進供需判讀；本季利潤池移向煉油屬週期性，不是結構性遷移"}}}},"q2_moat":{"verdict":"護城河 B 級、趨勢穩定：優勢在規模、上下游整合與低成本資源（Guyana、Permian），定價權有限；同業利潤率對照證明不了差距在擴大","reasoning":"機制是成本與規模：全球最大非國營煉油商、Permian 自動化鑽機與長水平井、專案執行（管理層稱大型專案數為最近對手兩倍、成本低 20%、工期快 20%，Q3 法說 Hansen），以及整合價值鏈下的交易調度。可證方向：同業 ROIC 事實表未涵蓋，改用利潤率。TTM 營業利益率 XOM 10.7%，低於 CVX 12.4%、SHEL 14.4%、TTE 16.3%、COP 21.9%；FCF 利潤率 8.5% 也是五家最低。這組對照被兩件事扭曲：XOM 營收含大量煉油銷售（每日賣 570 萬桶產品），壓低比率；而且 XOM 期間到 2026-06，SHEL 與 TTE 到 2026-09，含 Q3 高價差季。評分：執行力 8 分，依據是成本節省 169 億、Energy Products 單位盈餘自 2019 三倍、Guyana 11 年產出 10 億桶。定價權 6 分，原油與成品油是價格接受者，只有特用品、潤滑油品牌與 LNG 長約有部分議價。合併 7 分，屬 B 級。執行在擴大、定價持穩，但缺同業報酬差距可證，趨勢只給穩定。報酬持續期：決策層級與社會容忍度兩項紅燈，本季超額報酬撐不久。增量報酬只有管理層個案（Beaumont 擴建約 3 年回本、Pioneer 綜效由每年 20 億升到 40 億）；投入資本與折舊事實表未涵蓋，算不出全公司增量 ROIC","fact_refs":["f_peer_xom_gross_margin_pct","f_peer_xom_operating_margin_pct","f_peer_xom_fcf_margin_pct","f_peer_cvx_operating_margin_pct","f_peer_cvx_fcf_margin_pct","f_peer_shel_operating_margin_pct","f_peer_shel_fcf_margin_pct","f_peer_tte_operating_margin_pct","f_peer_tte_fcf_margin_pct","f_peer_cop_operating_margin_pct","f_peer_cop_fcf_margin_pct","f_kpi6_energy_products_adjusted"],"verdict_values":{"moat":{"mechanism":"規模與成本：全球最大非國營煉油網路，加上低成本上游資源（Guyana、Permian），以及集中式專案、技術與營運組織；在整合價值鏈上用交易調度放大資產價值","execution":8,"pricing":6,"grade":"B","trend":"→","trend_evidence":"執行面在進步：結構成本節省 Q2 163 億、Q3 169 億，Permian 單季創紀錄逾 180 萬桶油當量/日，Golden Pass 第一列接近銘牌產能。但同業 TTM 營業利益率與 FCF 利潤率 XOM 都是五家最低，同業差距擴大沒有獨立證據，定價權也沒有變化，判穩定","competitor_notes":[{"name":"CVX","strategy_note":"經 Hess 持有 Stabroek 30%，與 XOM 共享 Guyana 成長，是同一資產上最直接的對手；TTM 利潤率高於 XOM"},{"name":"SHEL","strategy_note":"分析師稱歐洲大廠 2030 年前成長偏弱；利潤率期間到 2026-09，含 Q3 高價差季，不能直接比"},{"name":"TTE","strategy_note":"毛利率與營業利益率高於 XOM，期間同樣到 2026-09，含高價差季"},{"name":"COP","strategy_note":"純上游，沒有低利潤率的煉油營收；利潤率最高反映業務結構不同，不代表成本優勢"}],"peer_na_reason":"同業 ROIC 與 ROCE 事實表未涵蓋，只能用利潤率對照；利潤率又受煉油營收比重與期間不同扭曲（XOM、CVX、COP 到 2026-06；SHEL、TTE 到 2026-09）","threats":[{"level":"🟡","text":"電動車替代：IEA 估 2025 年已替代約 170 萬桶/日、2030 年約 500 萬桶/日，油價衝擊讓電動車使用成本優勢擴大 20% 至 45%。衝擊的是全產業需求天花板，不改 XOM 對同業的相對位置，屬點對點","p":"35%","evidence_refs":["substitute_technology#0","substitute_technology#1"]},{"level":"🟡","text":"地緣資產：卡達 LNG 兩列受損，約占全球產量 3%，修復需數年；Stabroek 約 30% 面積因委內瑞拉邊界爭議未探勘；Q4 仍有約 35 萬桶/日的中東影響","p":"40%","evidence_refs":["geo_supply_chain#0","geo_supply_chain#1"]},{"level":"🟡","text":"法律與政策：加州塑膠回收訴訟、密西根指控合謀延緩能源轉型、德州 CO2 管線反壟斷私人訴訟；另有歐洲暴利稅與甲烷法規（後者已延後 3 年）","p":"25%","evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#1","major_events#2","lawsuit_class_action#1"]},{"level":"🟡","text":"同業共享成長資產：CVX 經 Hess 持有 Stabroek 30%，Guyana 成長不是 XOM 獨享；歐洲大廠 2030 年前成長偏弱，反而是相對優勢","p":"20%","evidence_refs":[]}],"roic_durability":{"quadrant":"低利益率×低周轉（TTM 營業利益率 10.7%；投入資本周轉率事實表未涵蓋，依資產密集度暫判）","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"油氣是需要不是想要，延後購買的代價高。但 IEA 估電動車 2025 年已替代約 170 萬桶/日、2030 年約 500 萬桶/日，油價衝擊又讓電動車省下的使用成本增 20% 至 45%，需求基礎值被侵蝕的速度在加快；公司自家展望稱 2050 年前油需仍高於 1 億桶/日，屬公司來源"},{"item":"決策層級","level":"🔴","text":"在最小決策單位（一桶原油、一加侖柴油）上完全可替代，客戶沒有轉換成本，本季的超額價差不受任何客戶鎖定保護；只有 LNG 長約、CCS 合約（8 家客戶、每年 1,100 萬噸，Q3 法說）與潤滑油品牌有合約年限"},{"item":"價值鏈分配","level":"🟡","text":"本季利潤池移向煉油（Energy Products 由 Q2 約 41 億升到 91 億），XOM 以全球最大非國營煉油商的身分（每日 360 萬桶）吃到。上游端資源國分成在上升：Guyana 已回收 550 億投資，權益量將調整（Q2 法說 Hansen、Woods），價值鏈分配長期往資源國移"},{"item":"社會容忍度","level":"🔴","text":"高必需又高敏感。CEO 自承高油價衝擊民生（Q3 法說）；歐洲上次課暴利稅後，公司取消了歐洲投資，對下一次能否擋住則說不確定（Q2 法說）。加州塑膠回收、密西根反壟斷兩案在進行。中斷期創高的煉油價差，正是政治上限最先壓下來的部分"}],"roiic":"事實表未涵蓋投入資本與折舊，算不出全公司數字。管理層個案：Beaumont 20 億擴建約 3 年回本（Q3 法說 Woods）、Pioneer 綜效由每年 20 億升到 40 億（Q3 法說 Hansen）；這些是自報個案，不能當全公司增量報酬","reinvest_rate":"事實表未涵蓋 NOPAT 與折舊；現金口徑：Q3 資本支出 70 億÷營業現金流 256.5 億，約 27%","endo_ceiling":null,"formula_note":"內生成長率＝增量 ROIC×再投資率，兩個輸入都缺，故不給數字。成長題改用產量計畫當代理（2027 年前加 50 萬桶油當量/日，對 449.6 萬的基數約年增 5%），只作合理性對照，不當天花板"}}}},"q3_growth":{"verdict":"成長跑道中等（黃燈）：量的成長看得到 2030（Guyana、Permian、LNG），之後的第二曲線管理層還沒公開；FY2026 的 EPS 翻倍來自價格，不是成長","reasoning":"成長組成：FY2025 實際 EPS 6.70 到 FY2027 共識 12.01，兩年年複合約 34%；同期共識營收由 3,239 億到 4,201 億，年複合約 14%。EPS 比營收快約 20 個百分點，來源是價差擴大，也就是價格，不是量。三年共識：FY2028 共識事實表未涵蓋，只能算兩年。內生上界：增量 ROIC 與再投資率算不出（見護城河題），改用代理，產量計畫約年增 5% 加每年約 2.6% 的回購，定價不變下每股約 5% 至 8%。共識與代理之間的缺口歸因於利潤率擴張（中斷期價差），可以歸因，但不能外推。跑道：Permian 計畫年增 9% 到 2030；Guyana 2030 年 170 萬桶/日（八個開發案）；Golden Pass 第二列 12 月實質完工、第三列 2027 年中機械完工；Rovuma 目標年底做最終投資決策。2030 之後，管理層稱有清楚的專案組合，但要等到有承諾的信心才公開（Q3 法說 Woods），屬未證的第二曲線，所以給黃燈，不給綠燈。衰退訊號亮兩項：EPS 成長遠快於營收（價差驅動），以及替代技術壓縮需求天花板（電動車）","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_kpi8","f_kpi4_cash_capex","f_kpi2_cash_flow_from_operation","f_shares_diluted_m"],"verdict_values":{"growth":{"driver_mix":"內生部分是量（Guyana、Permian、LNG）、結構成本節省與回購；FY2026 至 FY2027 的跳升來自價格與價差","runway_years":"約 4 年（以 2030 產量計畫的可見度計；油氣不適用滲透率口徑）","runway_post_y5":"🟡","endo_ceiling_basis":"增量 ROIC×再投資率的輸入缺（事實表未涵蓋投入資本與折舊），改以產量計畫約年增 5% 加回購約 2.6% 為代理，定價不變下每股約 5% 至 8%/年；兩年共識 EPS 年複合約 34%，遠超此代理，缺口歸因中斷期價差","segments":[{"item":"Upstream（Q3 2026 調整後盈餘）","value":"73 億美元，較 Q2 下滑（原油價格走低）；量靠 Permian、Guyana 成長"},{"item":"Energy Products","value":"91 億美元（Q2 約 41 億），來自中斷期煉油價差"},{"item":"Chemical Products","value":"7.25 億美元（Q2 約 12 億），化工價差下滑"},{"item":"Specialty Products","value":"約 13 億美元，基礎油價差走高"}],"decay_signals":[{"signal":"EPS CAGR 顯著高於營收 CAGR","lit":true,"evidence":"FY2025 到 FY2027 共識 EPS 年複合約 34%，營收約 14%"},{"signal":"TAM 被替代技術壓縮","lit":true,"evidence":"IEA：電動車替代 2025 年約 170 萬桶/日、2030 年約 500 萬桶/日"},{"signal":"FCF/NI<0.75 連 2 年","lit":false,"evidence":"FY2024 約 0.91、FY2025 約 0.82（年報）"},{"signal":"停止投資新產能且收入 3 年內下滑","lit":false,"evidence":"營收 FY2023 至 FY2025 下滑，但每季仍投資約 70 億擴產"},{"signal":"毛利率連 2 季 YoY 下滑","lit":null,"evidence":"季度毛利率事實表未涵蓋；年度毛利率由 FY2022 25.9% 降到 FY2025 22.0%"},{"signal":"maintenance capex 占 FCF>60%","lit":null,"evidence":"維持性資本支出事實表未涵蓋"}],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"資本配置紀律穩：本季降債逾 90 億、股利連 44 年增、回購穿越週期不隨油價調整；扣分在固定 200 億回購正好買在高點倍數，常態價格下要靠資產負債表補","reasoning":"轉換率：FCF 對淨利 FY2022 1.05、FY2023 0.93、FY2024 0.91、FY2025 0.82（年報）；Q3 2026 自由現金流 191 億，GAAP 淨利 154 億。轉換健康，但連三年下滑。SBC 對營收事實表未涵蓋。Q3 現金去向：營業現金流 256.5 億，分成資本支出 70 億、股利 43 億、回購 51 億，其餘約 90 億降債（CFO 稱淨負債降逾 90 億）。股數：以年報淨利÷稀釋 EPS 推得 FY2025 平均約 43.05 億股，現在 40.79 億股，回購確實在縮股。壓力：2027 年股利（每季 1.07×目前股數）約 175 億，加回購 200 億，合計約 375 億；FY2025 自由現金流只有 236 億。若價格回到 2025 年水準，每年缺口約 140 億，以目前淨負債 221 億計約 1.6 年翻倍。管理層明說谷底會用資產負債表補（Q3 法說 Woods）。併購：Pioneer 綜效倍增到每年 40 億，但收購後實際增量報酬事實表未涵蓋。回購買入收益率：以 trailing 19.3 倍計約 5.2%，以 FY2027 共識 15.6 倍計約 6.4%；10 年期公債殖利率事實表未涵蓋，無法判斷是否過門檻","fact_refs":["f_kpi3_fcf","f_kpi2_cash_flow_from_operation","f_kpi4_cash_capex","f_kpi9","f_kpi10_net_debt","f_kpi11","f_shares_diluted_m","f_dividend_yield_ttm","f_pe_current"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":true,"passed":null,"input":"Pioneer 綜效由每年 20 億升到 40 億（Q3 法說 Hansen）；收購後實際增量報酬與資金成本事實表未涵蓋，無法判斷"},{"name":"buyback_yield","applicable":true,"passed":null,"input":"回購買入收益率 trailing 約 5.2%、FY2027 共識約 6.4%；10 年期公債殖利率事實表未涵蓋，無法對門檻"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"平均股數由 FY2025 約 43.05 億（年報淨利÷稀釋 EPS）降到目前 40.79 億，淨縮股；SBC 金額事實表未涵蓋，但淨稀釋率為負"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購撐，量來自 Guyana、Permian、LNG 自建專案。回購與股利是承重項，但近三年現金去向與回購均價事實表未涵蓋，只能用 Q3 一季與年報 FCF 推算，已寫在理由"}}}},"q5_valuation":{"verdict":"偏貴：現價要 FY2027 之後 EPS 穩在 12 以上，或市場長期給 17 倍以上才划算；我不信，因為分母是中斷期高峰","reasoning":"現價 187.25 對 FY2026 共識 13.46 是 13.9 倍，對 FY2027 共識 12.01 是 15.6 倍，看似合理。但 FY2026 EPS 約為 FY2025 實際 6.70 的兩倍，是荷莫茲受阻、卡達 LNG 受損、俄羅斯煉能下線堆出來的價差；以 FY2023 至 FY2025 實際 EPS 平均 7.81 計是 24 倍。trailing 本益比 19.3 倍、P/S 1.97、EV/S 2.02 都在近四個年度端點的最高位（不是五年連續分位）。賣方聚合目標價均值 158 至 170 美元，都低於現價；10 月個別調整中只有 Barclays 的 200 美元高於現價，Wells Fargo 已降評。同業倍數事實表未涵蓋，無法在同層級對錨。Base 情境一年後（FY2027 EPS 11.4×15 倍）為 171 美元，三年後（FY2029 EPS 10.3×15 倍）為 155 美元，都低於現價","fact_refs":["f_price_at_dd","f_consensus_eps_fy1","f_consensus_eps_fy2","f_pe_current","f_pe_percentile","f_ps_current","f_ps_percentile","f_ev_s_current","f_ev_s_percentile","f_ev_s_fwd","f_ev_m","f_net_debt_m","f_dividend_yield_ttm","f_week26_return_pct"],"verdict_values":{"valuation":{"basis":"本益比，以 FY2026 共識、FY2027 共識與 FY2023 至 FY2025 實際 EPS 平均三種分母對照","tier":"整合型油氣大廠","peers":{"expanded":false,"reason":"事實表同業對照只有利潤率，未涵蓋同業前瞻本益比或股價淨值比，無法在同層級對錨"},"fwd_pe":13.91,"peg":null,"percentile_5y":null,"val_light":"🔴","val_light_derivation":"商品循環股優先看股價淨值比，但事實表未涵蓋。改用三種分母：FY2026E 13.9 倍、FY2027E 15.6 倍、FY2023 至 FY2025 實際平均 24 倍；trailing 19.3 倍與 P/S、EV/S 都在年度端點最高。五年連續分位事實表未涵蓋；PEG 不適用，因為 FY2026 到 FY2027 共識 EPS 下滑，且沒有 FY2028 共識。分母正是爭點，便宜的論證不成立；Base 一年與三年目標都低於現價，判偏貴（紅）","upside_short_pct":-8.7,"upside_mid_pct":-17.5,"denominator_disputed":true,"denominator_note":"FY2026E 共識 13.46 含中斷期超額煉油價差（Energy Products Q3 91 億、Q2 41 億）與高油價，約為 FY2025 實際 6.70 的兩倍；用它當分母算出的 13.9 倍不代表便宜。常態化分母約 10（Base FY2028）時，現價約 19 倍"}}},"q6_how_wrong":{"verdict":"最可能看錯的地方是把中斷期獲利當常態；價值陷阱風險中等（兩項衰退訊號亮燈），下檔可達 −35% 至 −55%","reasoning":"反方最強的數字：2015 年獲利約為 2014 年一半、2020 年全年虧損 224 億、股價 2020 年跌 40.9%、Brent 2014 至 2016 年由逾 100 美元跌破 30。現價較 52 週均線 146 高約 28%，較 250 週均線 107 高約 74%；回到 104 週均線約 −33%，回到 250 週均線約 −43%。壓力測試五項過三：淨負債低於單季營業現金流（過）；信評 AA- 與 Aa2（過，來源為第三方網站）；FCF 對淨利連兩年 ≥0.75（過）；常態價格下 FCF 覆蓋股利加回購（不過，每年缺口約 140 億）；前兩次下行年度沒有虧損（不過，2020 年虧損）。訴訟：證券集體訴訟 2026-05 由陪審團判公司全勝，約 30 億求償解除；加州塑膠回收、密西根反壟斷、德州 CO2 管線三案的求償金額與時點事實表未涵蓋。法說迴避：Q2 對荷莫茲現況、煉油獲利拆解、歐洲暴利稅可能性、歲修延後規模都沒有正面回答","fact_refs":["f_price_at_dd","f_ma_w52","f_ma_w104","f_ma_w250","f_kpi10_net_debt","f_kpi2_cash_flow_from_operation","f_kpi3_fcf","f_kpi9"],"verdict_values":{"trap":{"verdict":"🟡","label":"高峰獲利陷阱：前瞻本益比被中斷期價差壓低"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":13.46,"pe":13.91,"basis":"FY2026E 共識 EPS 13.46（當年度，Q4 尚未公布），起點本益比＝187.25÷13.46；終端倍數同樣套在終端年 FY2031E 當年度 EPS，分母同口徑"},"eps":{"bull":[13.0,12.4,12.9,13.6,14.3],"base":[11.4,10.0,10.3,10.7,11.1],"bear":[9.6,7.0,6.6,7.0,7.4]},"pe":{"bull":16,"base":15,"bear":13},"p":{"bull":20,"base":45,"bear":35},"yield_pct":{"dividend":2.2,"net_buyback":2.6},"second_stage":{"bull_cagr_pct":4,"base_cagr_pct":2},"max_dd":{"lo":-55,"hi":-35,"basis":"現價 187.25 較 52 週均線 146 高約 28%，較 250 週均線 107 高約 74%；回到 104 週均線 126 約 −33%，回到 250 週均線約 −43%。2020 年股價全年跌 40.9%，2015 年獲利約腰斬，Brent 2014 至 2016 年跌約 70%。Bear 終點約 −49%，下檔區間取 −35% 至 −55%","trigger_time":null},"basis":{"bull":"煉油緊張延續到 2028（俄羅斯煉廠修復慢、中東要先停火才修），卡達 LNG 修復期間 LNG 價高，Guyana、Golden Pass、Permian 的量照計畫；常態年 EPS 13 至 14，市場給穿越週期派息的溢價 16 倍","base":"2027 上半年價差仍高、下半年原油過剩壓價，2028 年回到常態；之後靠產量年增約 3% 至 5%、結構成本節省與每年約 2.6% 的回購（EPS 為每股，已含縮股），EPS 由 10 回升到 11；倍數 15 倍，介於現價對 FY2026 的 13.9 倍與對 FY2027 共識的 15.6 倍之間","bear":"荷莫茲復航與 2027 年 370 至 500 萬桶/日過剩同時發生，重演 2015 年獲利腰斬：2028 年 EPS 約 7，之後量的成長被低價抵銷；倍數 13 倍，因為低盈餘年倍數通常不會壓到 12 以下，取現價 FY2026 倍數略下"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"IEA 估 2027 年供給增約 800 萬桶/日、過剩約 500 萬桶/日，EIA 估約 370 萬桶/日，JPMorgan 估 2027 年 Brent 均價 64 美元；majors 上游持續擴產。前兩次下行：2015 年獲利約為 2014 年一半，2020 年全年虧損 224 億、股價跌 40.9%，Brent 2014 至 2016 年跌約 70%","assumption":"共識假設 FY2027 EPS 只比 FY2026 少一成（13.46 降到 12.01），中斷期價差緩慢退場","consequence":"荷莫茲復航撞上 2027 年過剩，FY2028 EPS 落到 7 附近，倍數壓到 13 倍，股價回到 100 美元左右，五年後虧近半","ruling":"採納：這是 Bear 35% 機率與下檔 −35% 至 −55% 的來源，也是不追的主因。它與 Single Thing 是同一條因果鏈，復航就是觸發點，兩者重疊，不另立","watch":"IEA、EIA 月報的 2027 平衡表、Upstream 季盈餘、公司揭露的中東影響量","evidence_refs":["supply_demand_durability#0","supply_demand_durability#1","cyclical_supply_discipline_capacity#1","cyclical_inventory_price_position#1","cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#1","cyclical_prior_downcycle_behavior#2","cyclical_prior_downcycle_behavior#3"]},{"view":"論點成功但股東經濟變差","evidence":"2027 年回購固定 200 億，谷底用資產負債表補（Q3 法說 Woods）；以 trailing 19.3 倍買回，收益率約 5.2%。Guyana 成本回收完成後權益量將調整（Q2 法說）。社會容忍度紅燈：上次歐洲暴利稅後公司取消歐洲投資，CEO 對能否擋下一次說不確定（Q2 法說）；加州、密西根、德州三案進行中","assumption":"產量與成本目標達成，超額價差留在股東手上","consequence":"量的成長與成本下降都兌現，但回購買在高點倍數，資源國分成上升，暴利稅分走價差，每股盈餘成長低於產量成長","ruling":"部分採納：回購穿越週期的紀律本身合理，不改 Base EPS 路徑；但 Base 終端倍數不給高於 15 倍，法律與暴利稅列為風險觸發","watch":"歐美暴利稅立法、三案判決或和解金額、Guyana 權益量調整（2030 計畫更新）、回購執行價對常態化 EPS 的倍數","evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#1","major_events#2","lawsuit_class_action#1"]},{"view":"價格已反映太多","evidence":"26 週漲 24.2%，現價較 52 週均線高約 28%；trailing 本益比 19.3 倍、P/S 1.97、EV/S 2.02 都在近四個年度端點最高；賣方聚合目標價均值 158 至 170 美元，都低於現價","assumption":"市場把中斷期獲利當成新常態","consequence":"即使 FY2027 共識 12.01 兌現，15.6 倍也沒有重估空間；價差一回落就直接反映在股價","ruling":"採納：估值結論偏貴，等價格回落或價差正常化後再評","watch":"股價與 52 週均線的距離、FY2027 共識的修正方向","evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#1"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 None → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=None","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 None → 本次 187.25","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=None","side_b":"本次 price_at_dd=187.25","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"煉油緊張延續多久","cause":null,"prior_field":null,"side_a":"管理層：全球成品油短缺約三分之一來自中東出口受阻，俄羅斯約一半煉能下線，恢復平衡至少要到明年之後，可能更久（Q3 法說 Woods）","side_b":"IEA、EIA 預估 2027 年原油過剩 370 至 500 萬桶/日；JPMorgan 估 2027 年 Brent 均價 64 美元","ruling":"可調和，屬程度差異：兩邊講的是不同市場，原油過剩與成品油緊張可以同時成立，FY2027 上游先走弱、煉油晚一步。Base 照這個順序排，FY2027 EPS 11.4，低於共識 12.01","evidence_level":"管理層前瞻說法對機構預測，兩邊都還沒實現","settle_metric":"Upstream 與 Energy Products 2027 Q1、Q2 調整後盈餘","if_then":["若 2027 上半年 Energy Products 低於 50 億且 Upstream 低於 55 億：Bear 機率上調到 40%，維持不追","反向：若 2027 上半年兩者都不低於 2026 Q3，且 FY2027 共識上修到 13 以上：重跑判斷，評估分批建立首倉 2%"],"evidence_refs":["supply_demand_durability#0","supply_demand_durability#1","end_markets#1"]},{"axis":"結構改善對同業利潤率","cause":null,"prior_field":null,"side_a":"管理層：Energy Products 單位盈餘自 2019 三倍、結構成本節省 169 億、專案成本低 20%、工期快 20%（Q3 法說）","side_b":"事實表 TTM 營業利益率與 FCF 利潤率，XOM 在五家同業中最低","ruling":"可調和：XOM 煉油營收比重高，壓低比率，且期間不同（XOM 到 2026-06，SHEL 與 TTE 到 2026-09）。但這也表示「優於同業」目前只有公司自述，護城河趨勢判穩定，不判擴大","evidence_level":"公司自述對第三方財報數據，口徑不一","settle_metric":"同期間 ROCE 或 ROIC 對照（事實表未涵蓋）","if_then":["若補到同期間資料仍顯示 XOM 營業利益率低於 CVX：執行分維持 8，不上調","反向：若 ROCE 顯示 XOM 領先最強同業 3 個百分點以上且連 2 年擴大：趨勢改判擴大，護城河等級上調一級"],"evidence_refs":[]},{"axis":"固定回購對週期現金流","cause":null,"prior_field":null,"side_a":"管理層：2027 年回購維持 200 億、股利不會砍，谷底用資產負債表補（Q3 法說 Woods、Hansen）","side_b":"FY2025 自由現金流 236 億，低於 2027 年股利約 175 億加回購 200 億；常態價格下每年缺口約 140 億，淨負債 221 億約 1.6 年翻倍","ruling":"可調和：本季已降債逾 90 億，緩衝撐得過兩年常態價格；第三年若仍是低價，回購勢必縮減，列入 H3 與減碼觸發","evidence_level":"年報與季報實績對管理層承諾","settle_metric":"淨負債、信評、回購執行額","if_then":["若淨負債超過 400 億美元或信評遭降：持有者減碼一半","反向：若常態價格下連 2 季自由現金流覆蓋股利加回購：H3 確認，移除壓力測試該項扣分"],"evidence_refs":[]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"買方：FY2026 13.9 倍、FY2027 15.6 倍不算貴；俄羅斯煉廠要先停火才能修，卡達 LNG 要修 3 至 5 年，緊張可能延續到 2028；Uaru 2026 Q4 投產、Golden Pass 第二列 12 月完工，量在成長；股利 44 年連增、200 億回購與 AA- 信評給下檔支撐","side_b":"賣方：FY2026 EPS 已是 FY2025 的兩倍，任一中斷因素消失就會回落；現價高於多數賣方目標價，trailing 倍數在年度端點最高","ruling":"採賣方側：買方情境我給 20% 機率（Bull 終點約 229 美元），不足以在年度端點最高的倍數追價。分歧核心在中斷期獲利是不是新常態，依據是 IEA、EIA 的 2027 過剩預測，以及管理層自己對正常化時點的描述","evidence_level":"機構預測與公司自述，2027 上半年季報可以裁決","settle_metric":"FY2027 共識 EPS 修正方向與 2027 Q1 分部盈餘","if_then":["若股價續漲而 FY2027 共識沒有上修：不追","若股價回到約 145 美元而 FY2027 共識仍 ≥10：重跑判斷，評估分批建立首倉 2%","反向：若 2027 Q1 分部盈餘證實價差延續，且 FY2027 共識上修到 13 以上：Bull 機率上調到 30%，重跑判斷"],"evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#1"]}],"triggers":[{"n":1,"text":"股價回到常態化估值區：約 145 美元以下，且 FY2027 共識 EPS 仍 ≥10","type":"估值rearm","maps_to":"H2","metric":"週收盤價、FY2027 共識 EPS","threshold":"股價 ≤145 且 FY2027 共識 ≥10","action":"重跑判斷，通過後分批建立首倉 2%","source_freq":"每週收盤、每月共識","date":null},{"n":2,"text":"荷莫茲全面復航、中東出口恢復","type":"Single Thing","maps_to":"R1","metric":"公司揭露的中東影響量、海峽航運狀況","threshold":"中東影響量低於 10 萬桶/日，或海峽正式恢復通行","action":"持有者分批了結一半；未持有者不追，等正常化後第一季數字出來再重跑","source_freq":"季報、每週航運新聞","date":null,"evidence_refs":["geo_supply_chain#1","supply_demand_durability#0"]},{"n":3,"text":"量的里程碑：Uaru 投產、Golden Pass 第二列完工","type":"假設驗證","maps_to":"H1","metric":"專案投產公告","threshold":"Uaru 於 2026 Q4 投產，Golden Pass 第二列 2026 年 12 月實質完工","action":"延遲超過一季：H1 削弱，Base 2028 EPS 下調 0.3 後重算","source_freq":"季報、公司新聞稿","date":"2026-12"},{"n":4,"text":"上游盈餘跌破常態，2027 原油過剩兌現","type":"風險","maps_to":"R2","metric":"Upstream 單季調整後盈餘","threshold":"連 2 季低於 55 億美元","action":"Bear 機率上調到 40%，維持不追；持有者減碼到 1.5% 以下","source_freq":"季報","date":null,"evidence_refs":["supply_demand_durability#0","supply_demand_durability#1","cyclical_inventory_price_position#1"]},{"n":5,"text":"法律判決或暴利稅落地","type":"風險","maps_to":"R4","metric":"判決、和解金額、立法","threshold":"單案超過 10 億美元，或通過針對煉油的暴利稅","action":"Base 終端倍數由 15 倍降到 14 倍重算；持有者停止加碼","source_freq":"法院公告、新聞","date":null,"evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#1","major_events#2","lawsuit_class_action#1"]},{"n":6,"text":"資產負債表被回購撐破","type":"減碼","maps_to":"H3","metric":"淨負債、信評","threshold":"淨負債超過 400 億美元，或信評遭降","action":"持有者減碼一半","source_freq":"季報、信評公告","date":null},{"n":7,"text":"2027 規劃新聞稿與 Q4 財報複審","type":"複審日期","maps_to":"H2","metric":"2027 規劃指標、Q4 調整後 EPS、中東影響量","threshold":"規劃指標與本次 Base 假設（量年增 3%、回購 200 億）對照","action":"重跑判斷","source_freq":"一次性","date":"2027-01"}],"kill_metrics":[{"metric":"Energy Products 單季調整後盈餘","bear_threshold":"低於 50 億美元","window":"2027 Q1 至 Q2","source":"公司季報新聞稿","last_status":"ok"},{"metric":"Upstream 單季調整後盈餘","bear_threshold":"連 2 季低於 55 億美元","window":"2027 全年","source":"公司季報新聞稿","last_status":"ok"},{"metric":"淨負債","bear_threshold":"超過 400 億美元","window":"滾動 4 季","source":"公司季報資產負債表","last_status":"ok"},{"metric":"FY2027 共識 EPS","bear_threshold":"低於 10 美元","window":"2027 Q2 前","source":"yfinance 分析師共識","last_status":"ok"}],"evidence_dismissed":[],"action_conditions":{"rearm_trigger":"股價≤145 美元（常態化 EPS 約 10×14.5 倍）且 FY2027 共識 EPS 仍 ≥10：重跑判斷，評估分批建立首倉","exec_line":"未持有：不追；價格先漲而證據未到，也不追。觸發重評後首倉 2%，第二批等價差正常化後的第一季數字確認 FY2027 共識沒有跌破 10 再加。已持有者在荷莫茲全面復航時分批了結一半","holding_cap":"≤3%（循環股，晚循環期間不新建）"}},"decision_inputs":{"signal":"C","ma":"🟡","cycle_position":"晚循環","cycle_verdict":"頂部觀望","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場把中斷期獲利當常態：FY2027 共識只比 FY2026 少一成（13.46 降到 12.01），但 IEA 與 EIA 預估 2027 年原油過剩 370 至 500 萬桶/日，JPMorgan 預估 2027 年 Brent 均價 64 美元，而管理層自己也說價差正常化要看荷莫茲復航與煉廠修復","momentum_overheated":null,"cycle_gates_pass":false,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等股價回到約 145 美元（常態化 EPS 約 10×14.5 倍），或價差正常化後的第一季數字出爐、FY2027 共識仍 ≥10，再重評","asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null},"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"6","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='C'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"輸入缺(momentum_overheated=null)，依保守方向處理：不視為觸發","input_gap":["momentum_overheated"]},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":true,"basis":"signal='C'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場把中斷期獲利當常態：FY2027 共識只比 FY2026 少一成（13.46 降到 12.01），但 IEA 與 EIA 預估 2027 年原油過剩 370 至 500 萬桶/日，JPMorgan 預估 2027 年 Brent 均價 64 美元，而管理層自己也說價差正常化要看荷莫茲復航與煉廠修復"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='C', runway='🟡', val='🔴', moat_trend='→', week26=24.22, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='循環/商品', cycle_position='晚循環', moat='B', moat_trend='→', cycle_gates_pass=False"},{"row":"6/7/7a-verdict","condition":"Soft Veto 生效 → 觀望（max-severity wins；8a/8b 未能繞過）","hit":true,"basis":"soft_veto_rows=['6']"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":null,"requires_critic":[]},"thesis":{"H":[{"id":"H1","text":"上游量成長兌現：Permian、Guyana、LNG 帶動產量（扣除中東影響）每年增 3% 以上","2y":null,"5y":"2030 年 Guyana 約 170 萬桶/日、Permian 年增 9% 的計畫照進度；扣除中東影響的總產量 2030 年較 2026 年增 15% 以上","10y":null,"threshold":"扣除中東影響的產量年增 ≥3%；Uaru 2026 Q4 投產，Golden Pass 第二列 2026 年 12 月實質完工、第三列 2027 年中機械完工","source":"公司季報產量揭露與法說","drift_rule":"5 年期：TTM 產量成長低於門檻，偏離連 4 季 ≥5% 判削弱，連 6 季 ≥10% 判反轉"},{"id":"H2","text":"常態價差下 EPS 站上 10 美元：結構成本節省 2030 年達 200 億、Energy Products 單位盈餘結構性提升、回購縮股，使中循環 EPS 高於 FY2023 至 FY2025 實際平均 7.81","2y":null,"5y":"FY2030 調整後 EPS 在常態價格下 ≥10.5","10y":null,"threshold":"價差正常化後第一個完整年度（預估 FY2028）EPS ≥9.5；結構成本節省 2027 年底 ≥180 億","source":"公司季報、法說與年度規劃新聞稿","drift_rule":"5 年期：TTM EPS 偏離 Base 路徑連 4 季 ≥5% 判削弱，連 6 季 ≥10% 判反轉"},{"id":"H3","text":"股東回饋穿越週期而不傷資產負債表：2027 年回購 200 億、股利續增，淨負債與信評守住","2y":"2027 至 2028 年淨負債 ≤400 億美元，信評維持 AA- 與 Aa2","5y":null,"10y":null,"threshold":"淨負債 ≤400 億美元且信評不降","source":"季報資產負債表、信評機構公告","drift_rule":"2 年期：淨負債偏離門檻連 2 季 ≥5% 判削弱，連 3 季 ≥10% 判反轉"}],"R":[{"id":"R1","text":"煉油價差正常化快於預期：荷莫茲復航、中東煉廠修復、中國提高成品油出口，Energy Products 盈餘回到 Q2 水準","h_ref":"H2","clock":"⚡","threshold":"Energy Products 單季調整後盈餘低於 50 億美元（Q2 約 41 億、Q3 91 億）","evidence_refs":["end_markets#0"]},{"id":"R2","text":"2027 原油供給過剩：IEA 估約 500 萬桶/日、EIA 約 370 萬桶/日，majors 與 OPEC+ 同時擴產，JPMorgan 估 2027 年 Brent 均價 64 美元；前兩次下行，2015 年獲利腰斬、2020 年虧損","h_ref":"H2","clock":"🔥","threshold":"Upstream 單季調整後盈餘連 2 季低於 55 億美元（Q3 73 億）","evidence_refs":["supply_demand_durability#0","supply_demand_durability#1","cyclical_supply_discipline_capacity#1","cyclical_inventory_price_position#1","cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#2","cyclical_prior_downcycle_behavior#3"]},{"id":"R3","text":"電動車替代壓低需求天花板與終端倍數","h_ref":"H1","clock":"🐢","threshold":"IEA 估電動車替代量在 2028 年前超過 350 萬桶/日，或全球油需連 2 年下滑","evidence_refs":["substitute_technology#0","substitute_technology#1"]},{"id":"R4","text":"法律與政治吃掉超額價差：暴利稅、加州塑膠回收訴訟、密西根反壟斷訴訟、德州 CO2 管線反壟斷訴訟","h_ref":"H3","clock":"🔥","threshold":"任一案件不利判決或和解超過 10 億美元，或歐美通過針對煉油的暴利稅","evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#1","major_events#2","lawsuit_class_action#1"]},{"id":"R5","text":"地緣資產受損拖慢量的成長：卡達 LNG 兩列要修數年、Stabroek 30% 面積卡在邊界爭議、Q4 中東影響量仍有 35 萬桶/日","h_ref":"H1","clock":"🔥","threshold":"2027 年中中東影響量仍超過 30 萬桶/日，或邊界爭議波及已開發區塊","evidence_refs":["geo_supply_chain#0","geo_supply_chain#1"]}],"single_thing":{"description":"荷莫茲海峽全面復航，中東煉能與出口恢復（含卡達以外的波斯灣產量回流）","why_fatal":"FY2026 與 FY2027 共識（13.46、12.01）建立在中斷期價差上。管理層估全球成品油短缺約三分之一來自中東出口受阻，IEA 的 2027 年約 500 萬桶/日過剩也以波斯灣產量恢復為前提。復航會同時打掉煉油超額價差、放出原油供給，是 EPS 最大的單一敏感項","if_happens":"Energy Products 單季盈餘回到 Q2 約 41 億附近，Upstream 跟著油價下滑，FY2027 EPS 落到 Base 的 11 以下，甚至 Bear 的 9 至 10；持有者分批了結，未持有者不追，等價格到重評條件","how_monitor":"公司每季揭露的中東影響量（Q4 指引 35 萬桶/日）、海峽航運恢復新聞、EIA 週度成品油庫存、Energy Products 季盈餘","probability":"12 至 24 個月內約 55%：管理層自承無法預測時點（Q2 法說），但 IEA 的 2027 平衡表已假設恢復"}},"appendix_a":{"growth_durability":5,"quality_score":7,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":15.59,"peg_fy2":-1,"stress":{"pass":3,"total":5},"fy2_valuation_basis":"PEG 依 Koyfin 共識（2026-11-02）"},"eps_meta":{"base_eps_path":{"FY2025A":6.7,"FY2026E":13.46,"FY2027E":12.01,"FY2028E":null},"fy_end_month":12,"eps_basis":"FY2025A 為年報 GAAP 稀釋 EPS；FY2026E、FY2027E 為 yfinance 分析師共識平均，口徑可能偏調整後；FY2028E 共識事實表未涵蓋，留空"},"catalysts":[{"date":"2026-12","date_precision":"month","type":"guidance","event":"2027 年規劃指標新聞稿，取代 12 月的企業計畫說明會","impact":"高","watch":"產量、資本支出、成本節省目標是否與 Base 假設一致"},{"date":"2026-12","date_precision":"quarter","type":"capacity","event":"Guyana 第五個開發案 Uaru 投產","impact":"中","watch":"投產時點與爬坡速度"},{"date":"2026-12","date_precision":"month","type":"capacity","event":"Golden Pass 第二列實質完工","impact":"中","watch":"是否如期完工、試車進度"},{"date":"2026-12","date_precision":"quarter","type":"capacity","event":"Rovuma LNG 最終投資決策","impact":"低","watch":"能否在年底前完成"},{"date":"2027-01","date_precision":"month","type":"guidance","event":"Q4 2026 財報與法說","impact":"高","watch":"Energy Products 價差走向、中東影響量、2027 規劃細節"},{"date":null,"date_precision":null,"type":"macro","event":"荷莫茲海峽全面復航","impact":"高","watch":"航運恢復狀況與公司中東影響量"},{"date":"2027-06","date_precision":"quarter","type":"capacity","event":"Golden Pass 第三列機械完工","impact":"低","watch":"時程是否延誤"}]}
```

---

## ⑤ 覆蓋面（程式判定，你回的 ⑤ 燈號會被覆寫）

燈號 🟡：非核心軸無證據：reg_tariff_export（關稅／出口管制）（尾部風險或事件型，不擋）。

⑤ 的 reason 只需評論：空軸的查詢詞是否切題、判斷有沒有交代缺口對結論的影響。

---

## 尾段：回覆格式

只回一個 JSON 陣列，①–⑧ 每條一個元素，八個全出，不得跳號、不得多列，陣列外不得有任何文字（不加前言、不加 markdown 圍欄、不加附註）：

```json
[{"item": "①", "light": "🔴|🟡|🟢", "judgment_path": "$.路徑", "reason": "一句話"}]
```
