你是 DD 管線 v20 的判斷層閘（gate），標的 DASH（20261103）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（45 條）
- `f_kpi0_gaap`（q1_business）｜營收（GAAP）＝4616 USD M｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 ir.doordash.com Q3 2026 financial results（numbers.latest_quarter_kpis.items[0]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-29））
  - 註記：未查得可靠共識數字，不填
- `f_kpi1_gaap`（q1_business）｜GAAP 營業利益 / 利益率＝442 USD M（利益率 9.6%）｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 ir.doordash.com Q3 2026 financial results（numbers.latest_quarter_kpis.items[1]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-29））
  - 註記：未查得，不填
- `f_kpi2_adjusted_ebitda_non_gaap`（q1_business）｜Adjusted EBITDA（公司未報 Non-GAAP 營業利益，以此替代）＝1060 USD M（占 GOV 3.1%）｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 ir.doordash.com Q3 2026 financial results（numbers.latest_quarter_kpis.items[2]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-29））
  - 註記：未查得，不填
- `f_kpi7`（q1_business）｜總訂單數＝993 M｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 ir.doordash.com Q3 2026 financial results（numbers.latest_quarter_kpis.items[7]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-29））
  - 註記：未查得，不填
- `f_kpi8_marketplace_gov`（q1_business）｜Marketplace GOV＝33.9 USD B｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 ir.doordash.com Q3 2026 financial results（numbers.latest_quarter_kpis.items[8]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-29））
  - 註記：未查得，不填
- `f_kpi9_net_revenue_margin_take_`（q1_business）｜Net Revenue Margin（take rate）＝13.6 %｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 ir.doordash.com Q3 2026 financial results（numbers.latest_quarter_kpis.items[9]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-29））
  - 註記：不適用
- `f_kpi5_q4_2026_marketplace_gov`（q1_business）｜Q4 2026 指引：Marketplace GOV＝35.4–36.4 USD B｜期間與口徑：Q3 FY2026 財報（公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司 IR 新聞稿 ir.doordash.com Q3 2026 financial results（numbers.latest_quarter_kpis.items[5]，as_of Q3 FY2026 財報（公告於 2026-10-29））
  - 註記：未查得，不填
- `f_kpi6_q4_2026_adjusted_ebitda`（q1_business）｜Q4 2026 指引：Adjusted EBITDA＝900–1,100 USD M｜期間與口徑：Q3 FY2026 財報（公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司 IR 新聞稿 ir.doordash.com Q3 2026 financial results（numbers.latest_quarter_kpis.items[6]，as_of Q3 FY2026 財報（公告於 2026-10-29））
  - 註記：未查得，不填
- `f_peer_dash_gross_margin_pct`（q2_moat）｜DASH 毛利率＝51.51 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.DASH.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_dash_operating_margin_pct`（q2_moat）｜DASH 營業利益率＝4.05 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.DASH.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_dash_fcf_margin_pct`（q2_moat）｜DASH FCF 利潤率＝11.38 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.DASH.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_uber_gross_margin_pct`（q2_moat）｜UBER 毛利率＝42.31 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.UBER.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_uber_operating_margin_pct`（q2_moat）｜UBER 營業利益率＝12.13 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.UBER.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_uber_fcf_margin_pct`（q2_moat）｜UBER FCF 利潤率＝18.32 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.UBER.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_cart_gross_margin_pct`（q2_moat）｜CART 毛利率＝72.23 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CART.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_cart_operating_margin_pct`（q2_moat）｜CART 營業利益率＝13.88 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CART.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_cart_fcf_margin_pct`（q2_moat）｜CART FCF 利潤率＝29.6 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CART.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝5.79 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-10-31）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝8.09 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-10-31）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝9.93 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-10-31）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝17950.57 USD m｜期間與口徑：2026-11-03／yfinance revenue_estimate 0y 平均（37 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝21692.94 USD m｜期間與口徑：2026-11-03／yfinance revenue_estimate +1y 平均（42 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi4_sbc_gaap`（q4_capital）｜SBC（含部分薪資稅）占營收 / 占 GAAP 營業利益＝269 USD M（占營收 5.8%；占 GAAP 營業利益約 61%）｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 Adjusted EBITDA 調節表（數字含部分薪資稅，非純 SBC；占比為本 agent 以 269/4616、269/442 換算）（numbers.latest_quarter_kpis.items[4]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-29））
  - 註記：不適用
- `f_kpi3_fcf`（q4_capital）｜自由現金流（FCF）＝787 USD M（占營收約 17.0%）｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 ir.doordash.com Q3 2026 financial results（numbers.latest_quarter_kpis.items[3]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-29））
  - 註記：未查得，不填
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝-2684.0 USD m｜期間與口徑：2026-11-03／yfinance 最新一季：總債務 3298.0、現金 5982.0（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝435.98 m shares｜期間與口徑：2026-11-03／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_ev_m`（q5_valuation）｜目前企業價值 EV（市值＋淨負債）＝79857.22 USD m｜期間與口徑：2026-11-03／市值 82541.22 ＋ 淨負債 -2684.0｜kind：realized
  - 來源：—（numbers.capital_structure.ev_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝189.32 USD｜期間與口徑：2026-11-02（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-11-02（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝32.7 x｜期間與口徑：2026-10-31／分母＝FY1 EPS 5.79，分子＝快照價 189.32｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-10-31）
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝78.56 x｜期間與口徑：2026-11-02（RTH 收盤，UTC）／2 個年度端點內的分位＝0.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-11-02（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝0.0 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／**非五年分位**：只用 2 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝4.84 x｜期間與口徑：2026-11-02（RTH 收盤，UTC）／4 個年度端點內的分位＝49.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝49.0 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝4.68 x｜期間與口徑：2026-11-02（RTH 收盤，UTC）／4 個年度端點內的分位＝48.9｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝48.9 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ev_s_fwd`（q5_valuation）｜EV/S（EV ÷ FY1 共識營收）＝4.45 x｜期間與口徑：2026-11-03／f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）｜kind：estimate
  - 來源：—（numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_consensus_rev_fy1_pct`（q5_valuation）｜FY1 共識修正＝-1.36 %｜期間與口徑：2026-10-31／兩份 Koyfin 快照之間的 EPS 修正幅度（5.87 → 5.79）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.fy1.revision_pct，as_of 2026-10-31）
- `f_consensus_rev_fy2_pct`（q5_valuation）｜FY2 共識修正＝-1.94 %｜期間與口徑：2026-10-31／兩份 Koyfin 快照之間的 EPS 修正幅度（8.25 → 8.09）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.fy2.revision_pct，as_of 2026-10-31）
- `f_consensus_rev_fy3_pct`（q5_valuation）｜FY3 共識修正＝-1.88 %｜期間與口徑：2026-10-31／兩份 Koyfin 快照之間的 EPS 修正幅度（10.12 → 9.93）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.fy3.revision_pct，as_of 2026-10-31）
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝3.95 %｜期間與口徑：2026-07-30 → 2026-10-31／FY1 共識 EPS 5.57 → 5.79（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-10-31）
- `f_ma_w104`（q5_valuation）｜104 週均線＝200.5 USD｜期間與口徑：2026-11-03／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）
- `f_ma_w250`（q5_valuation）｜250 週均線＝135.39 USD｜期間與口徑：2026-11-03／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）
- `f_ma_state`（q5_valuation）｜週線均線六態（decision_inputs.ma 必須等於此值）＝🟠｜期間與口徑：2026-11-03／timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）
  - 原文：「price 189.08 / W52 188.7 / W104 200.5 / W250 135.39 / W250 13週斜率 0.62%」
- `f_rsi14`（q5_valuation）｜RSI(14)＝52.29｜期間與口徑：2026-11-02（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-11-02（RTH 收盤，UTC））
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝9.67 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-11-02（RTH 收盤，UTC））

### findings_digest 中方向為負或來源衝突的條目（12 條）
- `competitive_share_entrants#1`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K 風險因子：切換成本低，消費者與商家可多平台並用；競爭壓力已迫使公司調整佣金、費用與促銷，對財務表現造成負面影響。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-18）｜affects：moat_trend、thesis.R
- `competitive_share_entrants#2`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K 風險因子：他業公司正開發自動化／無人機配送技術，可能以此與公司競爭，對手可能先於公司規模化。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-18）｜affects：thesis.R、decision_inputs.bear
- `regulatory_antitrust#0`（regulatory_antitrust｜方向 -｜狀態 ok）：10-K 揭露：2025年2月 Uber 在加州州法院提告，指控 DoorDash 部分商業做法違反競爭法；部分轄區競爭主管機關曾詢問或調查其定價條款，個別轄區已有決定。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-18）｜affects：decision_inputs.bear、thesis.R、moat_trend
- `regulatory_antitrust#1`（regulatory_antitrust｜方向 -｜狀態 ok）：10-K 揭露：加州 EDD 就薪資稅審計並於2023年1月發出不利評定，公司提出上訴並已提列應計；另有多個轄區的政府調查與詢問。
  - 來源：SEC EDGAR 10-K FY2025 Item 3（as_of 2026-02-18）｜affects：thesis.R、decision_inputs.bear
- `regulatory_antitrust#2`（regulatory_antitrust｜方向 -｜狀態 ok）：MLex：DoorDash 約170億美元收購 Instacart 可能遭美國聯邦與州反壟斷機關深度調查
  - 來源：MLex（as_of 2026-10-30）｜affects：thesis.R、decision_inputs.bear、triggers
- `regulatory_antitrust#3`（regulatory_antitrust｜方向 -｜狀態 ok）：DoorDash 若因反壟斷障礙無法完成併購，須付 Instacart 12.5億美元終止費
  - 來源：DoorDash 10-Q (2026-09-30)（as_of 2026-11-01）｜affects：thesis.R、valuation、triggers
- `reg_tariff_export#1`（reg_tariff_export｜方向 -｜狀態 ok）：分析師文章（非公司揭露）稱 2026 年主要逆風為全球關稅，美國有效關稅率 13-17%，壓抑可自由支配支出。
  - 來源：Finterra／FinancialContent：The New Era of Local Commerce: A Deep Dive into DoorDash (DASH) and the Global Tariff Shock（as_of 2026-02-24）｜affects：decision_inputs.bear
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：FY2025 10-K 揭露：部分營運地區鄰近俄羅斯，增加遵循貿易與制裁規範的難度（地緣風險屬法遵面，非實體供應鏈）
  - 來源：DoorDash FY2025 Form 10-K (SEC)（as_of 2026-02-27）｜affects：decision_inputs.bear
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：FY2022 10-K 舉例：哈薩克動亂迫使子公司 Wolt 暫停當地營運
  - 來源：DoorDash FY2022 Form 10-K (SEC)（as_of 2023-02-17）｜affects：decision_inputs.bear
- `end_markets#3`（end_markets｜方向 -｜狀態 ok）：公司指引：2026 Q4 調整後 EBITDA/Marketplace GOV 將季減，主因季節性 Dasher 成本、年度保險費用與全球投資增加（含 Deliveroo，並提示整合風險）；未找到公司 2027 展望。
  - 來源：DoorDash 8-K ex99.1 earnings release（as_of 2026-08-05）｜affects：decision_inputs.bear、triggers
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：10-K 風險因子：資源更多的競爭者可能更快回應新興技術與偏好變化，使 DoorDash 平台吸引力下降或過時；並提及消費者可能採用新出現的替代方案，使市場發展不如預期。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-18）｜affects：moat_trend、thesis.R
- `lawsuit_class_action#0`（lawsuit_class_action｜方向 -｜狀態 ok）：FY2025 10-K 揭露持續面臨 Dasher 獨立承包商分類等訴訟、仲裁與政府調查（含集體訴訟）；搜尋未見證券集體訴訟，僅見消費者／隱私類案件（如 2025-11 資料外洩集體訴訟，未核原文）。
  - 來源：SEC EDGAR 10-K FY2025 Item 3（as_of 2026-02-18）｜affects：decision_inputs.bear、thesis.R

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 6 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/DASH_20261103/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":526.4,"bear_5y_price":128.0,"p_bull_pct":25,"p_bear_pct":30,"upside_5y_pct":76.6,"ev5y_pct":69.3,"irr_base_pct":12.1,"asym_ratio":4.6,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":5.79,"pe":32.7,"basis":"FY2026 共識調整後 EPS（Koyfin，2026-10-31）；終端倍數同樣以當年度調整後 EPS 為分母"},"eps":{"bull":[8.3,10.4,12.9,15.7,18.8],"base":[7.9,9.6,11.4,13.3,15.2],"bear":[7.0,7.3,7.5,7.8,8.0]},"pe":{"bull":28,"base":22,"bear":16},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0,"net_buyback":0},"second_stage":{"bull_cagr_pct":15,"base_cagr_pct":11},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### DASH_Q2_2026_Earnings_Call_20260805.md
- 2026-08-05｜CFO｜commitment：CFO 重申新垂直業務預計下半年毛利轉正（原話："We're on track for that in the second half of the year."）
- 2026-08-05｜CFO｜guidance：CFO 表示下半年利潤率預期落在先前給的 Q3 財測區間內（原話："I would expect us to land inside the range of"）
- 2026-08-05｜CFO｜guidance：CFO 對 take rate 的建模指引：Q3 與 Q2 持平、Q4 較低（原話："so flattish from Q2 to Q3, and lower in Q4."）
- 2026-08-05｜CFO｜margin：CFO 說明 Q2 EBITDA 超標來得晚，沒時間再投資（原話："we just don't have enough time to reinvest back in the"）
- 2026-08-05｜CFO｜margin：CFO 點出單位經濟超預期的兩個來源（原話："Ads was one of them, subtotal was the other one."）
- 2026-08-05｜CFO｜margin：CFO 說明 Deliveroo 在 Q2 貢獻利潤為正（原話："ROO's contribution profit positive"）
- 2026-08-05｜CFO｜margin：CFO 表示不追求單季最後一塊錢的最佳化（原話："We're not trying to optimize the last dollar"）
- 2026-08-05｜CFO｜margin：CFO 解釋 Q1 到 Q2 take rate 上升來自 Dasher 成本季節性（原話："Dasher costs are seasonal for us."）
- 2026-08-05｜CFO｜commitment：CFO 對 Deliveroo 的利潤目標表態（原話："meet the profitability targets that we set out in the last"）
- 2026-08-05｜CFO｜commitment：CFO 稱自主配送、技術堆疊統一、商家服務投資均在預算與計畫內（原話："They're all going on budget and on"）
- 2026-08-05｜CFO｜capital_allocation：CFO 描述效率持續改善、再投資的原則（原話："We're consistently trying to improve efficiency."）
- 2026-08-05｜CFO｜capital_allocation：CFO 說明 AI 支出管控：設上限（原話："We've put caps in place."）
- 2026-08-05｜CEO｜product：CEO 稱單一技術堆疊的更多效益預期在明年初之後（原話："we expect to see even more benefits as time goes on."）
- 2026-08-05｜CEO｜product：CEO 談自動配送：先做到位再擴張（原話："you really have to nail something before you scale it"）
- 2026-08-05｜CEO｜product：CEO 談 DashMart Fulfillment Services 的錯誤率（原話："we're also seeing 10x better error rates"）
- 2026-08-05｜CEO｜product：CEO 介紹下單代理 DoorDash Ask（原話："DoorDash Ask, which is an ordering agent"）
- 2026-08-05｜CEO｜product：CEO 談商家端數位業務規模（原話："that business serves over 150,000 businesses"）
- 2026-08-05｜CFO｜customer：CFO 稱 DashPass 去年新增訂閱者多於前兩年（原話："We added more number of DashPass subscribers in the last"）
- 2026-08-05｜CEO｜customer：CEO 稱代理式流量目前很低（原話："quite low, I think, from some of the agentic partners"）
- 2026-08-05｜CFO｜customer：CFO 談新增距離費對損益影響（原話："I wouldn't expect it to be a massive impact"）
- 2026-08-05｜CEO｜competition：CEO 說國際市場是最小可行規模的生意（原話："And that's because it is a minimum viable scale"）
- 2026-08-05｜CEO｜competition：CEO 稱前十大海外市場為領先者或強勢第二（原話："we are the leader or we are a very strong #2"）
- 2026-08-05｜CFO｜competition：CFO 稱英國市場 Deliveroo 持續搶市占（原話："We're one of the fastest growing in that"）
- 2026-08-05｜CEO｜risk：CEO 對下一步自動配送擴張城市不給時程（原話："We'll share certainly more as time comes"）

### 問答異常語氣（迴避／改口／保留）
- DASH_Q2_2026_Earnings_Call_20260805.md｜問：Morton 問部分雜貨商是否近乎零抽成、能否重新定價｜答法：CEO 稱不評論特定對象，改談成長與多個改善槓桿
- DASH_Q2_2026_Earnings_Call_20260805.md｜問：Helfstein 問 Dot 單位經濟與最新 AOV 數字｜答法：CEO 談願景與營運複雜度未給單位經濟數字；CFO 談籃子變大未給 AOV 數字
- DASH_Q2_2026_Earnings_Call_20260805.md｜問：Youssef Squali 問 2026 年不含 Deliveroo 的 EBITDA 利潤率是否仍高於去年、有無投資遞延｜答法：CFO 只答下半年落在 Q3 財測區間內，未直接答全年年增與遞延
- DASH_Q2_2026_Earnings_Call_20260805.md｜問：Beck 問 Dot 單市場個位數高段滲透的特徵與自動配送占比上限｜答法：CEO 先稱問題太多，改談 Phoenix 與執行力，未給占比上限
- DASH_Q2_2026_Earnings_Call_20260805.md｜問：Sandler 問 Dot 擴到其他城市的速度｜答法：CEO 稱有擴張計畫但之後再說，未給時程
- DASH_Q2_2026_Earnings_Call_20260805.md｜問：Nowak 問新技術堆疊模組可量化的投資報酬｜答法：CEO 以比喻回應並給定性例子（搜尋轉換、客服自動化），未給量化數字

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 5 | 2 |
| customer_second_source | not_applicable | 0 | 1 |
| customer_concentration_credit | found | 2 | 1 |
| supply_demand_durability | found | 2 | 2 |
| regulatory_antitrust | found | 4 | 3 |
| reg_tariff_export | found | 2 | 2 |
| geo_supply_chain | found | 3 | 2 |
| end_markets | found | 5 | 3 |
| substitute_technology | found | 4 | 2 |
| channel_business_model_shift | found | 3 | 2 |
| capital_markets_pricing | found | 6 | 4 |
| major_events | found | 2 | 4 |

未涵蓋／不適用軸的查詢詞原文（供判相關性）：
- **customer_second_source**（not_applicable）：DoorDash merchants in-house delivery OR second source customer concentration 2026

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260518","verdict":"衛星候選 — US local commerce 平台龍頭 thesis 完整但 Pure MA 修正期；估值合理 (Adj Fwd PE 28x / PEG 0.94)；等 MA 回測 W104 $185 站穩 4 週或 Q2 26 Adj EBITDA $820M+ 兌現後分批進場","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"US local commerce flywheel 持續加深：DashPass 訂閱數、orders/MAU、cross-vertical attach rate 三軸同步擴張，US 市佔 56% 至少維持或微升"},{"id":"H2","text":"Operating leverage 兌現 + Adj EBITDA margin 從 19% (FY25) 擴張至 22-25% (FY28E)：投資週期完成後，core platform OPM 應大幅擴張"},{"id":"H3","text":"估值 multiple 修復 + EPS兌現：當前 Adj PE 28x 對 30% CAGR 屬合理偏便宜；2H 2026 投資週期過後，PE 應修復至 32-35x peer-aligned；GAAP EPS Path 從 -$0.04（FY24 normalized）至 FY27 $4.39 = profitability story 兌現"}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"投資週期失控（Capex 持續 ramp + Dot autonomous + 國際整合三軸 + merchant SaaS）→ Adj EBITDA margin 不擴張甚至壓縮"},{"id":"R2","text":"監管全面化（Seattle 模式擴展至 NYC / CA / Chicago / DC）→ Dasher 結構成本 +20-30%，contribution profit per order 結構性壓縮"},{"id":"R3","text":"UBER One $4.99 全面殺價 + Amazon Prime/ Walmart+ 跨平台訂閱競爭 → DashPass 增速放緩或被迫降價"}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🟡","ma":"🟠","trap":"🟢","moat_trend":null,"runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":159.2,"archetype":null,"cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"DASH","date":"2026-11-03","schema":"v15.0","contract":"v19","company_name":"DoorDash, Inc."},"oneliner":"美國本地外送龍頭，網路密度推升份額與利潤率；調整後 EPS 本益比 32.7 倍屬合理，GAAP 口徑偏貴。Instacart 併購審查與 Dasher 身分監管是兩大變數，等週線站回 104 週均線再分批","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/DASH_20261103/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/DASH_20261103/scenario.json","answers":{"q1_business":{"verdict":"賺的是本地交易的過路費：向商家抽佣，向消費者收配送與服務費，再加上 DashPass 訂閱與廣告。錢卡在「本地配送密度」這一節：密度越高，單筆成本越低，利潤才放大","reasoning":"Q3 2026 營收 46.16 億美元，年增 34%（排除 Deliveroo 約 23%）。Marketplace GOV 339 億美元，take rate 13.6%。GAAP 營業利益 4.42 億美元（9.6%），調整後 EBITDA 10.6 億美元（占 GOV 3.1%）。以 9.93 億筆訂單相除，換成單筆訂單：GOV 約 34.1 美元、營收約 4.65 美元、調整後 EBITDA 約 1.07 美元。TTM 毛利率 51.51%，營益率 4.05%。Q4 指引為 GOV 354–364 億美元、調整後 EBITDA 9–11 億美元。10-K 稱絕大多數營收來自 Marketplace 的商家佣金與消費者費用，Drive 等商家自有通路服務則按單收費。單點依賴：2023–2025 年沒有客戶占營收 10% 以上，但有單一實體占應收帳款 12%，身分未揭露。分部營收、單價與量的拆分公司未揭露，事實表未涵蓋。產業時鐘在擴張期：外送仍在滲透，領先者份額上升（刷卡資料 44% → 59%），整併已開始（Deliveroo 完成、Instacart 待審），沒有產能過剩跡象。供需持久性：需求面屬結構性持久；供給面（Dasher）可逆性高，但受勞動法規約束","fact_refs":["f_kpi0_gaap","f_kpi1_gaap","f_kpi2_adjusted_ebitda_non_gaap","f_kpi7","f_kpi8_marketplace_gov","f_kpi9_net_revenue_margin_take_","f_kpi5_q4_2026_marketplace_gov","f_kpi6_q4_2026_adjusted_ebitda","f_peer_dash_gross_margin_pct","f_peer_dash_operating_margin_pct"],"verdict_values":{"revenue_quality":"營收以 Marketplace 佣金與消費者費用為主，訂閱與廣告提高黏性。Q3 營收年增 34%，其中約 11 個百分點來自 Deliveroo 併購。沒有客戶占營收 10% 以上，屬高頻、分散的交易型收入","unit_econ_note":"Q3 2026 每筆訂單 GOV 約 34.1 美元、營收約 4.65 美元、調整後 EBITDA 約 1.07 美元（339 億、46.16 億、10.6 億美元各除以 9.93 億筆）。每 100 美元 GOV 平台拿 13.6 美元營收，留下約 3.1 美元調整後 EBITDA","archetype":{"primary":"品質複利成長","secondary":null,"confidence":"中","fingerprint":"GAAP 由虧轉盈：營益率 FY2022 −15.68% → FY2025 5.29%。毛利率逐年上升（45.5% → TTM 51.51%），營收年增 24–31%，成長靠網路密度與新垂直；SBC 高、併購頻繁，壓低信心"},"industry":{"clock_phase":"II","sd_verdict_source":"結構性持久。Ken Research 估美國線上外送市場 2025→2031 年增約 8.9%（第三方，口徑與公司 GOV 不同）。Q3 2026 美國餐廳 GOV 加速，CFO 稱季增速度為五年多來最快，付費訂閱創新高（管理層口述）。供給端 Dasher 可逆性高，但受勞動法規約束","bargaining":{"up":"上游是商家：餐廳分散、議價力弱；大型超市議價力強。2026-08-05 法說被問到近零抽成的雜貨商能否重新定價，管理層不評論","down":"消費者轉換成本低、可多平台並用，靠 DashPass 訂閱與選擇廣度綁定","geo":"地理營收分布事實表未涵蓋。國際含 Wolt、Deliveroo，CEO 稱前十大海外市場為第一或強勢第二；Wolt 部分市場鄰近俄羅斯，有制裁法遵負擔"},"profit_pool_dir":"利潤池向領先平台集中：DASH 刷卡消費占比 44% → 59%，Instacart 26% → 18%。整併（Deliveroo 已完成、Instacart 待審）延續這個方向；營業利益池占比的量化數字事實表未涵蓋","tam_table":{"expanded":false,"reason":"唯一的市場規模來源（Ken Research）估 2025 年美國線上外送市場 348.8 億美元，比 DASH 單季 GOV 339 億美元乘以 4 還小得多，口徑明顯不同，不能當滲透率分母；外送與雜貨的線上滲透率事實表未涵蓋"}}}},"q2_moat":{"verdict":"護城河在變寬：執行面擴大（份額與毛利率雙升），定價權持平（轉換成本低、監管壓佣金）。綜合列 B 級，方向向上","reasoning":"機制是本地三邊網路密度：消費者需求、商家選擇與 Dasher 供給互相強化，訂單越密，單筆配送越便宜、越快。方向證據用份額軸：Consumer Edge 刷卡資料（AP 轉述）顯示，DASH 在主要外送 app 的消費占比由 2021 Q2 的 44% 升至 2026 Q3 的 59%，同期 Uber Eats 16% → 18%，Instacart 26% → 18%；毛利率 FY2022 45.5% → TTM 51.51%。執行面擴大，給 8 分：同業 ROIC 事實表未涵蓋。DASH TTM 營益率 4.05%，仍低於 UBER 12.13% 與 CART 13.88%；研發密度 10.86% 高於 UBER 6.77%，屬投資期壓低利潤，但沒有 ROIC 驗證，所以不給 9 分。定價權持平，給 6 分：10-K 自承切換容易、消費者會多平台並用，競爭已迫使公司調整佣金與費用；Uber 2025 年 2 月提告指控反競爭，多個轄區查過定價條款。威脅中最重的是反壟斷與他業無人配送。四檢查點：需求成立，決策層級與價值鏈分配屬中性，社會容忍度已到紅區。增量 ROIC 與再投資率缺投入資本、D&A、資本支出與收購金額，算不出，列為資料缺口","fact_refs":["f_peer_dash_gross_margin_pct","f_peer_dash_operating_margin_pct","f_peer_dash_fcf_margin_pct","f_peer_uber_gross_margin_pct","f_peer_uber_operating_margin_pct","f_peer_uber_fcf_margin_pct","f_peer_cart_gross_margin_pct","f_peer_cart_operating_margin_pct","f_peer_cart_fcf_margin_pct","f_kpi9_net_revenue_margin_take_"],"verdict_values":{"moat":{"mechanism":"本地三邊網路密度：消費者需求、商家選擇與 Dasher 供給互相強化，訂單密度越高，單筆配送成本越低、速度越快。DashPass、Wolt+、Deliveroo Plus 會員在 2025 年底逾 3,500 萬，提高回購頻率","execution":8,"pricing":6,"grade":"B","trend":"↑","trend_evidence":"執行面擴大：刷卡消費占比 44% → 59%（2021 Q2 → 2026 Q3，AP 轉述）；Q3 美國餐廳 GOV 季增為五年多來最快（CFO 法說）；毛利率 FY2022 45.5% → TTM 51.51%。定價權穩定：10-K 自承競爭迫使調整佣金與費用，Uber 提告，多轄區查定價條款；Net Revenue Margin 13.6%，歷史序列事實表未涵蓋","competitor_notes":[{"name":"UBER","strategy_note":"營益率 12.13%、FCF 利潤率 18.32%，都高於 DASH，但含叫車業務，外送單獨數字事實表未涵蓋。刷卡消費占比 16% → 18%，是最直接的點對點對手，並已對 DASH 提起反競爭訴訟"},{"name":"CART","strategy_note":"毛利率 72.23%、營益率 13.88%、FCF 利潤率 29.6%，軟體與廣告比重高；但刷卡消費占比 26% → 18% 持續流失，已同意被 DASH 收購"},{"name":"DHER.DE","strategy_note":"事實表無財務資料；10-K 列為國際競爭者，與 Wolt、Deliveroo 在海外市場重疊"},{"name":"Amazon","strategy_note":"10-K 列為競爭者，財務對照事實表未涵蓋；10-K 另提到他業公司正開發無人配送，可能藉此跨入"}],"peer_na_reason":"同業 ROIC 事實表未涵蓋，只有利潤率。DASH GAAP 營益率 4.05% 低於 UBER 與 CART，但研發密度較高、仍在投資期；這個判讀沒有經過 ROIC 驗證","threats":[{"level":"🟡","text":"Uber Eats 與多平台並用：轉換成本低，競爭已迫使公司調整佣金與費用，Uber 另以反競爭為由提告","p":30,"evidence_refs":["competitive_share_entrants#1","regulatory_antitrust#0"]},{"level":"🔴","text":"他業公司以無人車、無人機配送切入，資源更多、可能先規模化，繞過 Dasher 網路","p":15,"evidence_refs":["competitive_share_entrants#2","substitute_technology#0","substitute_technology#1"]},{"level":"🟡","text":"AI 購物代理接手下單入口，削弱 app 流量與廣告收入；目前第三方代理累計只有數百筆訂單","p":15,"evidence_refs":["substitute_technology#2","substitute_technology#3"]},{"level":"🔴","text":"反壟斷：Instacart 交易可能遭聯邦與州深度審查（倡議團體稱合併後掌握近 60% 第三方雜貨外送），市場力量議題可能擴及既有定價條款","p":35,"evidence_refs":["regulatory_antitrust#2","competitive_share_entrants#4"]}],"roic_durability":{"quadrant":"低利益率×高周轉（推斷：TTM GAAP 營益率 4.05%、輕資產撮合；投入資本口徑事實表未涵蓋，周轉率未驗證）","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者（消費者）、決策者（消費者與商家）、付款者（消費者付費、商家付佣）三個角色都成立。Q3 總訂單 9.93 億筆，年增 28%（排除 Deliveroo 17%）；CFO 稱成熟世代的使用頻率與客單持續上升。屬「想要」多於「需要」，景氣差時可以延後，但 2026 Q3 沒有看到延後跡象"},{"item":"決策層級","level":"🟡","text":"替代在單筆訂單層級決定，消費者可同時裝多個 app，10-K 自承切換容易；黏性主要靠 DashPass 訂閱與選擇廣度。漲價後流失率與分客群留存，事實表未涵蓋"},{"item":"價值鏈分配","level":"🟡","text":"價值鏈由商家、平台、Dasher、消費者分配。平台每 100 美元 GOV 拿 13.6 美元營收、約 3.1 美元調整後 EBITDA；大型超市議價力強，管理層不回答近零抽成雜貨商的問題；Dasher 成本受監管左右"},{"item":"社會容忍度","level":"🔴","text":"已碰到政治天花板：Dasher 身分訴訟與政府調查持續，加州 EDD 發出薪資稅不利評定；Uber 指控反競爭，多轄區查定價條款；倡議團體要求擋下 Instacart 交易。佣金與費用的實際上限會先撞到社會與監管上限，碰不到經濟上限"}],"roiic":"事實表未涵蓋（缺投入資本、商譽與收購淨額）","reinvest_rate":"事實表未涵蓋（缺資本支出、D&A、營運資金變動與收購金額）","endo_ceiling":null,"formula_note":"內生成長率＝增量 ROIC × 再投資率；再投資率＝(Capex − D&A ＋ ΔWC ＋ 收購淨額) ÷ NOPAT。本包只有利潤率與 FCF，算不出。Deliveroo 與 Instacart 兩筆併購使 2025–2028 年的再投資率由併購主導，增量報酬要到交割後才能驗"}}}},"q3_growth":{"verdict":"五年後跑道仍寬：外送之外，雜貨與零售、國際、商家軟體已有營收與毛利證據，是看得到的第二條曲線；但共識 EPS 增速約三分之一來自利潤率擴張，不全是量","reasoning":"成長來源以量為主（Q3 總訂單年增 28%，排除 Deliveroo 為 17%），客單與廣告次之，併購第三（Deliveroo 已計入、Instacart 待審），回購不是來源。共識 EPS：FY2026 5.79、FY2027 8.09、FY2028 9.93 美元（Koyfin 快照，家數事實表未涵蓋），兩年年增約 31%。營收共識 FY2026 179.5 億、FY2027 216.9 億美元（37 位與 42 位分析師），年增約 20.8%。兩者差約 10 個百分點，歸因利潤率擴張（調整後 EBITDA 從投資期回升、新垂直接近毛利兩平），不是回購。內生上界因缺投入資本算不出，情境樹按「超過上界」保守處理。跑道：外送與雜貨的線上滲透率事實表未涵蓋，跑道年數算不出。第二曲線的證據：數位點餐服務有 15 萬家商家使用，Q2 2026 營收年增逾 40%；SevenRooms 新簽場館年增逾 100%；新垂直接近毛利兩平；Costco 上架；CEO 2026-08-05 稱國際前十大市場為第一或強勢第二。衰退訊號七項中亮一項（EPS 增速比營收快約 10 個百分點），價值陷阱風險中等。Instacart 是否計入 FY2028 共識不明（快照在簽約後兩天），列資料缺口","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_kpi7","f_kpi8_marketplace_gov","f_kpi4_sbc_gaap"],"verdict_values":{"growth":{"driver_mix":"量為主（排除 Deliveroo 訂單年增 17%），價與組合次之（客單、廣告、訂閱），併購第三（Deliveroo 已計入、Instacart 待審），回購不是成長來源","runway_years":"事實表未涵蓋（缺滲透率）","runway_post_y5":"🟢","endo_ceiling_basis":"內生上界算不出（投入資本事實表未涵蓋）。共識調整後 EPS FY2026→FY2028 年增約 31%（5.79 → 9.93 美元），FY2027 營收年增約 20.8%（179.5 → 216.9 億美元），差約 10 個百分點，歸因利潤率擴張。上界無法驗證，情境樹按超出上界處理，空頭機率取 30%","segments":[{"item":"Q3 2026 營收合計","value":"46.16 億美元，年增 34%"},{"item":"其中 Deliveroo","value":"3.65 億美元（約 7.9%）；訂單年增 28% 中約 11 個百分點來自 Deliveroo"},{"item":"排除 Deliveroo","value":"營收年增約 23%、訂單年增 17%、GOV 年增 23%"},{"item":"揭露變更","value":"自 2026 Q4 起不再揭露排除 Deliveroo 的數字"},{"item":"分部營收","value":"公司不分部揭露，Marketplace 與 Commerce Platform 營收拆分事實表未涵蓋"}],"decay_signals":[{"signal":"EPS 增速顯著高於營收增速（差 >5 個百分點）","lit":true,"evidence":"共識調整後 EPS FY2026→FY2028 年增約 31%，FY2027 共識營收年增約 20.8%，差約 10 個百分點；來源是利潤率從投資期回升"},{"signal":"SBC 占營收 >5% 且逐年上升","lit":false,"evidence":"Q3 2026 為 5.8%，高於 5%；但 2026 年指引由 13–14 億下修到 12–13 億美元，事實表沒有逐年序列證明在上升"},{"signal":"毛利率連 2 季年減","lit":false,"evidence":"毛利率 FY2022 45.5% → FY2025 50.88% → TTM 51.51%"},{"signal":"FCF/淨利 <0.75 連 2 年","lit":false,"evidence":"FY2025 FCF 18.26 億美元、淨利 9.35 億美元，約 1.95 倍"},{"signal":"核心市占近 12 個月縮減","lit":false,"evidence":"刷卡消費占比升至 59%"},{"signal":"TAM 萎縮或被替代技術壓縮","lit":false,"evidence":"第三方 AI 代理累計只有數百筆訂單；自動配送由公司自己投資（Dot、DoorDash Air）"},{"signal":"產業估值倍數近 3 年系統性下移","lit":null,"evidence":"同業倍數歷史事實表未涵蓋"}],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"現金流強，但每股經濟偏弱：FCF 是淨利的近兩倍，可是 SBC 吃掉 GAAP 營益約六成，Instacart 又部分用股票支付，併購報酬尚未驗證","reasoning":"FCF 轉換率高：FY2025 FCF 18.26 億美元、淨利 9.35 億美元，約 1.95 倍；Q3 2026 FCF 7.87 億美元，約占營收 17%。但 FCF 加回了 SBC：Q3 SBC（含部分薪資稅）2.69 億美元，占營收 5.8%、占 GAAP 營益約 61%；2026 年 SBC 指引由 13–14 億下修到 12–13 億美元。公司指引年底商戶付款時點會使 2026 年 FCF 少 7–8 億美元，屬時點差。資產負債表：現金 59.82 億、總債務 32.98 億美元，淨現金 26.84 億美元；2026 年 6 月底遵守信貸條款，循環額度未動用。Instacart 對價為每股 65 美元現金或 0.3372 股，報導總值約 170 億美元：現金部分要動用現金或舉債，股票部分會稀釋；交易被擋須付 12.5 億美元終止費。現金去向四分、債務到期與利率、回購金額與均價，事實表未涵蓋。三項計分：併購報酬待驗、回購收益率不過、SBC 淨稀釋不過","fact_refs":["f_kpi3_fcf","f_kpi4_sbc_gaap","f_kpi1_gaap","f_net_debt_m","f_shares_diluted_m","f_ev_m"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":true,"passed":null,"input":"Deliveroo 2026 年約貢獻 2 億美元調整後 EBITDA（公司指引），Q2 起貢獻利潤轉正；收購價與投入資本事實表未涵蓋，已實現增量報酬算不出。Instacart 尚未交割"},{"name":"buyback_yield","applicable":true,"passed":false,"input":"回購金額與均價事實表未涵蓋，CFO 稱回購保守、伺機。Instacart 部分以每股 0.3372 股支付，交割後淨發行為正，淨回購收益率不可能高於 10 年期殖利率加 2 個百分點"},{"name":"sbc_dilution","applicable":true,"passed":false,"input":"2026 年 SBC 指引 12–13 億美元，約當市值 825 億美元的 1.5%（毛額，回購抵銷事實表未涵蓋）。以年度淨利 ÷ 每股盈餘粗估，股數由 FY2023 約 3.93 億股升至目前約 4.36 億股，年增約 3–4%（含基本與稀釋口徑差，屬粗估），高於 1.5% 門檻"}]},"governance":{"capital_returns":[{"item":"Deliveroo 併購","value":"Q3 2026 貢獻營收 3.65 億美元，2026 年約 2 億美元調整後 EBITDA（公司指引）；收購價事實表未涵蓋"},{"item":"Instacart 併購","value":"每股 65 美元現金或 0.3372 股，可選並按比例分配；報導總值約 170 億美元，預計 2027 年底至 2028 上半年交割；終止費 12.5 億美元"},{"item":"綜效","value":"CFO 稱第一年綜效全數再投資，第三年淨綜效 5 億美元"},{"item":"回購","value":"CFO 稱保守、伺機、過去回購報酬佳；金額事實表未涵蓋"},{"item":"自由現金流","value":"FY2025 18.26 億美元；Q3 2026 7.87 億美元"}]}}},"q5_valuation":{"verdict":"現價要求調整後 EPS 兩年內從 5.79 做到 9.93 美元，且倍數守在二十倍出頭。按調整後口徑屬合理，我大致相信這個成長；但 GAAP 口徑約 72 倍，「便宜」的說法不成立","reasoning":"FY2026 調整後前瞻本益比 32.7 倍，FY2027 為 23.4 倍，FY2028 為 19.1 倍。PEG 約 1.05（FY2026 本益比 ÷ 兩年 EPS 年增 31%）。trailing GAAP 本益比 78.56 倍；P/S 4.84 倍、EV/S 4.68 倍，在 4 個年度端點中約居中（49%）；前瞻 EV/S 4.45 倍。分母爭議：第三方 GAAP 共識 FY2026 為 2.63 美元，與 Koyfin 的 5.79 美元差兩倍以上，差額主要是 SBC 與併購攤銷，便宜論證因此無效。共識方向：最新快照 FY1–FY3 下修 1.36%–1.94%，但 FY1 近 3 個月上修 3.95%。賣方目標價：9 月初 42 位分析師平均 252.30 美元（區間 172–350，當日股價 226.15），高低比約 2.0；股價下跌後目標價可能下調，屬過時資料。基本情境：12 個月看 FY2027 EPS 7.90 × 26 倍＝205 美元（+8.5%），3 年看 FY2029 EPS 11.40 × 24 倍＝274 美元（+44.5%）。反推：以 22 倍計，FY2028 調整後 EPS 只要約 8.6 美元就能撐住現價，低於共識 9.93 美元，所以下檔主要來自監管與交易事件，而非成長落空。五年連續分位事實表未涵蓋","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_pe_current","f_pe_percentile","f_ps_current","f_ps_percentile","f_ev_s_current","f_ev_s_percentile","f_ev_s_fwd","f_ev_m","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_fy1_pct","f_consensus_rev_fy2_pct","f_consensus_rev_fy3_pct","f_consensus_rev_3m_fy1_pct"],"verdict_values":{"valuation":{"basis":"以調整後 EPS 前瞻本益比為主、EV/S 為輔；GAAP 本益比與 SBC 用來檢查分母爭議","peers":{"expanded":false,"reason":"事實表只有同業利潤率（UBER、CART；DHER 無資料），沒有同業前瞻本益比或 EV/S。UBER 含叫車、CART 即將被併入，層級不同，不能當倍數錨；本份以自身調整後 EPS 倍數與成長校準，同業倍數列資料缺口"},"fwd_pe":32.7,"peg":1.05,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"調整後前瞻本益比 32.7 倍 ÷ 兩年 EPS 年增約 31%＝PEG 1.05，落在 1～2 的合理區；FY2027 本益比 23.4 倍。比前份（28 倍、PEG 0.94）變貴，全部來自股價上漲 19%。分母有爭議（GAAP 約 72 倍），不給便宜。五年分位：事實表只有 4 個年度端點的 P/S 分位 49%，不是五年連續分位，留空。結論：合理","upside_short_pct":8.5,"upside_mid_pct":44.5,"denominator_disputed":true,"denominator_note":"Koyfin 共識 FY2026 EPS 5.79 美元，與第三方 GAAP 共識 2.63 美元差兩倍以上，差額主要是 SBC（2026 年指引 12–13 億美元）與併購攤銷。調整後口徑前瞻本益比 32.7 倍，GAAP 約 72 倍（189.32 ÷ 2.63）。情境樹用調整後口徑，但把終端倍數壓到 22 倍來吸收 SBC 成本"}}},"q6_how_wrong":{"verdict":"最可能看錯在監管：Dasher 身分認定與佣金管制直接打單筆利潤，而 GAAP 營益率只有約 4% 的緩衝；其次是 Instacart 交易拖長與股權稀釋","reasoning":"看錯的三條路。第一，監管：Dasher 身分、佣金與費用管制直接壓單筆利潤，是最大的單一敏感度。第二，Instacart 交易：被擋要付 12.5 億美元終止費並耗掉管理層精力；過關則有發股稀釋、整合拉長，而且第一年綜效全數再投資。第三，估值口徑：市場若改用 GAAP 或扣除 SBC 的現金流定價，倍數空間不足。壓力測試四項過三項：Instacart 被擋（約每股 2.9 美元）、FY2027 共識下修 10%、終端倍數壓到 16 倍但 EPS 走基本路徑（15.20 × 16＝243 美元，仍高於現價），這三項都過；Dasher 改認定為員工一項不過。歷史最大回撤、空方最強數字、訴訟金額事實表未涵蓋；法說迴避的題目已列入反證紀錄。價值陷阱風險中等：一項衰退訊號亮（EPS 增速比營收快約 10 個百分點）。動能沒有過熱：RSI 52.29，26 週漲 9.67%","fact_refs":["f_peer_dash_operating_margin_pct","f_kpi4_sbc_gaap","f_ma_w104","f_ma_w250","f_ma_state","f_rsi14","f_week26_return_pct"],"verdict_values":{"trap":{"verdict":"🟡","label":"中等：EPS 增速遠高於營收這一項亮燈，加上併購審查與發股稀釋；還不到陷阱"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":5.79,"pe":32.7,"basis":"FY2026 共識調整後 EPS（Koyfin，2026-10-31）；終端倍數同樣以當年度調整後 EPS 為分母"},"eps":{"bull":[8.3,10.4,12.9,15.7,18.8],"base":[7.9,9.6,11.4,13.3,15.2],"bear":[7.0,7.3,7.5,7.8,8.0]},"pe":{"bull":28,"base":22,"bear":16},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0,"net_buyback":0},"second_stage":{"bull_cagr_pct":15,"base_cagr_pct":11},"max_dd":{"lo":-55,"hi":-35,"basis":"倍數面：若在 FY2026 調整後 EPS 5.79 美元時倍數就壓到空頭的 16 倍，股價為 93 美元（−51%）；空頭 FY2027 EPS 7.00 × 16 倍＝112 美元（−41%）。技術面：250 週均線 135.39 美元（−28.5%）是第一道支撐，現價已在 104 週均線下方。事件面：Instacart 審查或 Dasher 判決可再加 5–10 個百分點的衝擊。合併取 −35%～−55%。歷史最大回撤事實表未涵蓋","trigger_time":null},"basis":{"bull":"Instacart 2028 上半年交割，第三年 5 億美元淨綜效提早達成；美國餐廳維持加速，新垂直與廣告推升利潤率；SBC 占營收降到 5% 以下，市場給 28 倍（仍低於現值 32.7 倍）","base":"FY2027 略低於共識（7.90 對 8.09 美元），之後年增由約 22% 逐年放緩到 14%；Instacart 交割後發股稀釋與綜效大致相抵，每股淨盈餘與自由現金流已反映在每股 EPS 路徑，不另計回購殖利率；終端倍數 22 倍，低於現值以吸收 SBC 成本；同業倍數事實表未涵蓋，無法附同業對照","bear":"Dasher 監管成本上升或佣金受管制，加上 Instacart 被擋、付 12.5 億美元終止費；EPS 停在 7–8 美元，成長熄火到 5–10%，對應 16 倍"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"Dasher 獨立承包商分類的訴訟、仲裁與政府調查持續（含集體訴訟）；加州 EDD 2023 年 1 月發出薪資稅不利評定，公司上訴中。TTM GAAP 營益率只有 4.05%","assumption":"獨立承包商模式在主要市場維持不變","consequence":"若改認定為員工，配送成本結構性上升，調整後 EPS 退回 7–8 美元並停滯，倍數壓到 16 倍，五年跌三到五成","ruling":"採納為最大單一風險，與唯一致命事件是同一件事；機率低但後果重，以清倉條件處理","watch":"每季 10-Q 法律程序段落；加州 EDD 上訴結果；主要州立法","evidence_refs":["lawsuit_class_action#0","regulatory_antitrust#1"],"fact_refs":["f_peer_dash_operating_margin_pct"]},{"view":"論點失敗","evidence":"10-K 自承轉換成本低、消費者會多平台並用，競爭已迫使公司調整佣金、費用與促銷；Uber 2025 年 2 月提告指控反競爭，多個轄區查定價條款","assumption":"take rate 維持在 13.6% 附近","consequence":"take rate 每降 0.5 個百分點，以單季 GOV 339 億美元計，約少 1.7 億美元營收，幾乎直接落到營業利益","ruling":"部分採納：份額數據顯示目前是 DASH 在拿份額，所以論點不翻；但定價權只給持平，不給擴大","watch":"Net Revenue Margin 季度變化與公司歸因","evidence_refs":["competitive_share_entrants#1","regulatory_antitrust#0"],"fact_refs":["f_kpi9_net_revenue_margin_take_","f_kpi8_marketplace_gov"]},{"view":"論點失敗","evidence":"10-K 提到他業公司正開發無人車、無人機配送，資源更多、可能更快回應新技術","assumption":"Dasher 網路與自有 Dot、DoorDash Air 在自動化浪潮中仍是主要通道","consequence":"若他業無人配送先規模化，網路密度優勢被繞過，單筆成本優勢消失","ruling":"反駁為五年內的主情境：第三方 AI 代理累計只有數百筆訂單，公司自己投資地面與空中機器人，Dot 預期年底在最大測試市場占高個位數訂單；列為長期風險監測","watch":"他業無人配送在美國大都會的商轉與訂單占比","evidence_refs":["competitive_share_entrants#2","substitute_technology#0","substitute_technology#1"],"fact_refs":[]},{"view":"論點成功但股東經濟變差","evidence":"Q3 SBC 2.69 億美元，占營收 5.8%、占 GAAP 營益約 61%；Instacart 部分以每股 0.3372 股支付；CFO 稱回購保守、伺機","assumption":"營收與調整後 EPS 的成長能轉成每股價值","consequence":"業務照計畫擴張，但股數上升、SBC 持續，每股 GAAP 盈餘與扣除 SBC 的自由現金流落後調整後數字，倍數難以回升","ruling":"採納：資本配置列最低級、長期信心上限為中，基本情境終端倍數取 22 倍而非現值 32.7 倍","watch":"稀釋股數年增率、SBC 占營收、交割時股票對價比例","evidence_refs":["major_events#0","ma_merger#0"],"fact_refs":["f_kpi4_sbc_gaap","f_shares_diluted_m"]},{"view":"論點成功但股東經濟變差","evidence":"倡議團體稱 DASH 加 Instacart 將掌握近 60% 第三方雜貨外送；MLex 稱交易可能面臨聯邦與州深度審查；DASH 在主要外送 app 消費占比已達 59%","assumption":"份額上升可以轉成定價權","consequence":"份額越高，政治天花板越低：佣金與費用上限、搭售限制、交易附條件；若被擋要付 12.5 億美元","ruling":"採納：社會容忍度列紅，定價權只給 6 分；終止費約占市值 1.5%，不改論點","watch":"FTC、DOJ 與州檢察長動作；交易時程","evidence_refs":["regulatory_antitrust#2","regulatory_antitrust#3","competitive_share_entrants#4"],"fact_refs":["f_ev_m"]},{"view":"價格已反映太多","evidence":"調整後前瞻本益比 32.7 倍，trailing GAAP 本益比 78.56 倍；TTM FCF 利潤率 11.38% 沒有扣除 SBC；最新快照共識 FY1–FY3 下修 1.36%–1.94%","assumption":"市場持續用調整後 EPS 定價","consequence":"若市場改用 GAAP 或扣除 SBC 的現金流定價，股價要靠 2–3 年盈餘成長才撐得住；以 22 倍計，FY2028 調整後 EPS 需約 8.6 美元才能持平現價","ruling":"部分採納：不給便宜，維持合理；基本情境已把終端倍數降到 22 倍","watch":"共識 EPS 修正方向、SBC 占營收","evidence_refs":["capital_markets_pricing#4"],"fact_refs":["f_fwd_pe_latest","f_pe_current","f_peer_dash_fcf_margin_pct","f_consensus_rev_fy2_pct"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 🟠 → 本次 🟠","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=🟠","side_b":"本次 ma=🟠","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 159.2 → 本次 189.32（+18.9%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=159.2","side_b":"本次 price_at_dd=189.32","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 159.2 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 159.2 美元：五年期望值 前份未列，基準年化 前份未列，前份未列不對稱比","side_b":"本次情境、股價仍用 159.2 美元：Bull 價 526.4、Bear 價 128，五年期望值 +101.3%，基準年化 16.0%，不對稱比 9.81","ruling":"先換情境、股價不動：五年期望值與基準年化前份未列，無法比較。前份未列不對稱比，本次為 9.81。Bull、Bear 價位與股價無關，只受情境影響。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 159.2 美元：五年期望值 +101.3%，基準年化 16.0%，不對稱比 9.81","side_b":"本次情境、股價 189.32 美元：五年期望值 +69.3%，基準年化 12.1%，不對稱比 4.58","ruling":"再換股價、情境不動：起點價上漲 18.9%，五年期望值少 32.0 個百分點，基準年化少 4.0 個百分點，不對稱比由 9.81 降到 4.58。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"前份漂移：新增欄位","cause":"方法變動","prior_field":["moat_trend","runway_post_y5","archetype","cycle_position","p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份（2026-05-18）的裁決、角色、護城河方向、五年後跑道、公司類型、循環位置、情境機率與最大回撤皆未填","side_b":"本次：護城河方向向上，五年後跑道寬，公司類型為品質複利成長；非循環股，不判循環位置；情境機率多 25／中 45／空 30，最大回撤 −35%～−55%；裁決與角色依新欄位重算","ruling":"屬格式補齊，不是看法翻轉；前份已寫論點完整，與本次方向一致","evidence_level":"方法","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"前份漂移：評等與估值結論","cause":"價格變動","prior_field":["signal","val"],"side_a":"前份：股價 159.2 美元，調整後前瞻本益比 28 倍、PEG 0.94，評等 B、估值合理","side_b":"本次：股價 189.32 美元（+19%），FY2026 調整後前瞻本益比 32.7 倍、PEG 約 1.05，仍在合理區；品質與護城河沒有轉弱，評等維持 B、估值維持合理","ruling":"倍數上升全部來自股價；同期 FY1 共識近 3 個月上修 3.95%，兩欄維持不變","evidence_level":"價格與共識資料","settle_metric":"FY2027 調整後本益比","if_then":["若股價漲到 FY2027 調整後本益比 35 倍以上（約 283 美元），估值結論降一級並減碼三分之一"],"evidence_refs":[]},{"axis":"前份漂移：價值陷阱風險","cause":"新證據","prior_field":["trap"],"side_a":"前份：價值陷阱風險低","side_b":"本次：中等。新證據有三：2026-10-28 簽約以約 170 億美元收購 Instacart，可能面臨聯邦與州深度審查，被擋須付 12.5 億美元；部分對價用股票；共識 EPS 增速比營收快約 10 個百分點","ruling":"上調一級；業務數字仍在加速，沒有到陷阱，但交易與稀釋使每股價值的不確定性變高","evidence_level":"8-K、10-Q 與媒體","settle_metric":"交易審查結果、FY2027 GAAP 營益率","if_then":["若主管機關起訴阻止且同時總訂單年增跌破 12%，價值陷阱風險升到高並停止加碼","若交易附條件過關且 FY2027 GAAP 營益率 ≥6%，回到低"],"evidence_refs":["regulatory_antitrust#2","regulatory_antitrust#3","major_events#0"]},{"axis":"進場門檻變動","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"等 MA 回測 W104 $185 站穩 4 週或 Q2 26 Adj EBITDA $820M+ 兌現後分批進場","side_b":"週收盤連 4 週站上 104 週均線（約 200.5 美元），且 Q4 2026 調整後 EBITDA ≥9 億美元，才分批進場首筆三分之一","ruling":"舊條件的 EBITDA 一支已兌現（CFO 2026-08-05 稱 Q2 EBITDA 超標），股價一度上漲後跌回 104 週均線下方；104 週均線本身也從 185 美元移到 200.5 美元。新門檻改為技術與財報兩條同時成立，分批進場而非一次建倉","evidence_level":"均線計算與法說","settle_metric":"週收盤價與 Q4 2026 調整後 EBITDA","if_then":["兩條同時成立，分批進場首筆三分之一","股價先站回均線但 Q4 調整後 EBITDA 低於 9 億美元，不追"],"evidence_refs":[]},{"axis":"Single Thing 變動","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份 Single Thing 為空（未設）","side_b":"本次 Single Thing：加州或聯邦層級以判決或立法定讞，把 Dasher 改認定為員工並適用主要市場；發生即清倉","ruling":"前份格式沒有唯一致命事件欄。本次依數學上最大單一敏感度選定：配送人力是最大的變動成本，而 GAAP 營益率只有 4.05%；Instacart 交易成敗（終止費約市值 1.5%）影響小得多","evidence_level":"10-K 法律程序","settle_metric":"加州 EDD 上訴結果與主要州立法","if_then":["定讞改認定為員工並適用主要市場，清倉"],"evidence_refs":["lawsuit_class_action#0","regulatory_antitrust#1"]},{"axis":"陣亡指標變動","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份無陣亡指標（空白）","side_b":"本次四條：總訂單年增連 2 季 <12% 停止加碼；take rate 連 2 季年減 ≥0.5 個百分點減碼三分之一；FY2027 GAAP 營益率 <6% 減碼至半倉；Dasher 改認定員工定讞清倉","ruling":"前份格式沒有此欄，本次補上指標、門檻與資料來源","evidence_level":"方法","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"估值分母：調整後 EPS 與 GAAP EPS","cause":null,"side_a":"調整後口徑：FY2026 共識 EPS 5.79 美元，前瞻本益比 32.7 倍；對照兩年約 31% 的 EPS 年增，PEG 約 1.05，屬合理","side_b":"GAAP 口徑：第三方 FY2026 GAAP 共識 2.63 美元，約 72 倍；trailing GAAP 本益比 78.56 倍；SBC 占 GAAP 營益約 61%","ruling":"不可調和：同一個價格得出合理與昂貴兩個相反結論。裁決：情境樹採調整後口徑，因為共識路徑與倍數同源、可比；但 SBC 是真實成本，不採便宜論點，基本情境終端倍數從 32.7 倍降到 22 倍來吸收。依據：2026 年 SBC 指引 12–13 億美元，約當市值 1.5%","evidence_level":"公司指引與第三方共識","settle_metric":"FY2027 SBC 占營收與 GAAP 營益率","if_then":["若 FY2027 SBC 占營收 ≤5.5% 且 GAAP 營益率 ≥6%，基本情境終端倍數由 22 倍上調到 25 倍，並加碼至目標倉位","反向：若 FY2027 SBC 占營收 >7% 或 GAAP 營益率 <4%，終端倍數降到 18 倍並減碼三分之一"],"evidence_refs":["capital_markets_pricing#2","capital_markets_pricing#4"]},{"axis":"資本配置：管理層說法與交易條款","cause":null,"side_a":"CFO（2026-10-29）：非常看重自家股票、重視稀釋，回購哲學不變、保守且伺機","side_b":"同一週簽約，以每股 65 美元現金或 0.3372 股 DoorDash A 類股收購 Instacart，部分對價用股票","ruling":"可調和（程度差異）：CFO 說明是 Instacart 股東要求參與上檔。以交易條款為準，把發股稀釋放進每股 EPS 路徑；回購收益率不可能過關","evidence_level":"8-K 合約與法說原話","settle_metric":"交割時股票對價比例與交割後 12 個月淨發行股數","if_then":["若交割時股票對價占比 >50% 且 12 個月內沒有回購抵銷，資本配置維持最低級、終端倍數不上調","若交割後 12 個月回購抵銷發行股數一半以上，資本配置升一級，並重新檢討倉位上限"],"evidence_refs":["major_events#0","ma_merger#0"]},{"axis":"管理層承諾：新垂直毛利轉正","cause":null,"side_a":"CFO（2026-08-05）：新垂直業務下半年毛利轉正，進度符合","side_b":"CFO（2026-10-29）：已經很接近毛利兩平，Q3 還沒轉正","ruling":"可調和：承諾期限是 2026 下半年，Q4 還在期限內；但口氣從進度符合變成很接近，標為未證、監測","evidence_level":"管理層口述","settle_metric":"Q4 2026 財報是否宣布新垂直毛利轉正","if_then":["若 Q4 2026 財報沒有宣布轉正，論點三削弱、停止加碼","若宣布轉正且 2027 上半年維持，論點三成立並允許第二筆加碼"],"evidence_refs":[]},{"axis":"管理層迴避的問答","cause":null,"side_a":"2026-08-05 法說有六題迴避：近零抽成雜貨商能否重新定價、Dot 單位經濟與客單數字、全年 EBITDA 利潤率是否年增、自動配送占比上限、擴張時程、技術平台的量化投資報酬","side_b":"同一場 CFO 稱自動配送、技術平台、商家服務投資都在預算與計畫內；2026-10-29 稱技術平台 2027 上半年完工","ruling":"不採信也不否定，標為未證、監測；投資報酬用完工後的 GAAP 營益率驗證","evidence_level":"法說逐字稿","settle_metric":"2027 下半年 GAAP 營益率","if_then":["若技術平台完工後兩季（2027 下半年）GAAP 營益率仍低於 FY2025 的 5.29%，視為投資報酬說法證偽，減碼三分之一","若回到 6% 以上，維持論點二"],"evidence_refs":[]},{"axis":"共識方向：近 3 個月上修與最新快照下修","cause":null,"side_a":"FY1 共識近 3 個月上修 3.95%（5.57 → 5.79 美元）；Q3 營收與調整後 EBITDA 創新高","side_b":"最新快照 FY1–FY3 共識 EPS 下修 1.36%–1.94%；公司指引 Q4 調整後 EBITDA 占 GOV 季減，原因是季節性 Dasher 成本、年度保險與全球投資，並提示 Deliveroo 整合風險","ruling":"可調和，但要到 2027 年 2 月的 Q4 財報才能裁決：小幅下修可能是 Q4 季節性與投資，也可能已開始計入 Instacart。利空出現不到一季，凍結加碼到 Q4 財報","evidence_level":"共識快照與公司指引","settle_metric":"Q4 2026 調整後 EBITDA 與 FY2027 共識","if_then":["若 Q4 2026 調整後 EBITDA ≥9 億美元且 FY2027 共識止跌，解除凍結","若 FY2027 共識再下修 5% 以上，不追並延後首筆"],"evidence_refs":["end_markets#3"]},{"axis":"產業態勢：競爭、結構與其他變數","cause":null,"side_a":"結構轉好：DASH 消費占比 44% → 59%、Instacart 26% → 18%；產業整併（Deliveroo、Instacart）；新垂直接近毛利兩平","side_b":"其他結構變數在惡化：反壟斷（Uber 提告、定價條款調查、Instacart 深度審查），勞動法規（加州 EDD 薪資稅評定、Dasher 身分訴訟），替代技術（他業無人配送）；競爭面 10-K 自承轉換成本低","ruling":"雙向拉鋸：份額與結構在轉好，但份額越高，反壟斷與勞動監管的天花板越近。論點以結構轉好為主，監管列為最大單一風險","evidence_level":"10-K、刷卡資料、媒體","settle_metric":"take rate 與監管事件","if_then":["若 take rate 連 2 季年減 ≥0.5 個百分點且公司歸因監管，裁定轉為競爭與監管惡化中，減碼三分之一"],"evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#1","regulatory_antitrust#2","competitive_share_entrants#1","end_markets#1"]},{"axis":"現在就買與現在就賣的最強論證","cause":null,"side_a":"現在就買：Q3 營收與調整後 EBITDA 創新高，美國餐廳 GOV 加速；股價從 9 月初約 226 美元跌到 189 美元（−16%），FY2027 調整後本益比只有 23.4 倍，對應兩年 31% 的 EPS 年增；Instacart 若被擋，只損失 12.5 億美元（約市值 1.5%）","side_b":"現在就賣：GAAP 本益比 78.56 倍，SBC 吃掉六成營益；股價跌破 104 週均線；Instacart 審查最長拖到 2028 上半年，期間發股與整合都不確定；最新共識小幅下修","ruling":"要到 Q4 財報與審查第一個里程碑才能裁決。先等週線站回 104 週均線且 Q4 守住指引，首筆只建三分之一","evidence_level":"財報、均線、交易條款","settle_metric":"週收盤價、Q4 2026 調整後 EBITDA","if_then":["若股價先站回 104 週均線但 Q4 調整後 EBITDA 低於 9 億美元，不追","若股價跌向 250 週均線（約 135 美元）而訂單年增與指引沒有受損，分批反買"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"總訂單增速守不住","type":"假設驗證","maps_to":"H1","metric":"總訂單年增率","threshold":"連 2 季 <12%","action":"停止加碼；連 4 季則減碼三分之一","source_freq":"季報新聞稿／每季","date":"2027-02"},{"n":2,"text":"營運槓桿沒有反映在 GAAP 利潤率","type":"假設驗證","maps_to":"H2","metric":"FY2027 GAAP 營益率","threshold":"<6%","action":"減碼至半倉","source_freq":"10-K／每年","date":"2028-02"},{"n":3,"text":"新垂直毛利沒有如期轉正","type":"假設驗證","maps_to":"H3","metric":"新垂直業務毛利","threshold":"Q4 2026 財報仍未轉正","action":"停止加碼","source_freq":"季報與法說／每季","date":"2027-02"},{"n":4,"text":"Instacart 交易遭阻或拖延","type":"風險","maps_to":"R1","metric":"交易審查進度","threshold":"主管機關起訴阻止，或 2028-06-30 前未交割","action":"核心業務數字未受損時分批反買；若同時總訂單年增跌破 12%，不追","source_freq":"8-K 與主管機關公告／不定期","date":"2028-06","evidence_refs":["regulatory_antitrust#2","regulatory_antitrust#3"]},{"n":5,"text":"佣金與費用被迫下調","type":"風險","maps_to":"R3","metric":"Net Revenue Margin","threshold":"連 2 季年減 ≥0.5 個百分點","action":"減碼三分之一","source_freq":"季報新聞稿／每季","date":null,"evidence_refs":["competitive_share_entrants#1","regulatory_antitrust#0"]},{"n":6,"text":"Dasher 改認定為員工定讞","type":"Single Thing","maps_to":"Single Thing","metric":"Dasher 身分認定","threshold":"加州或聯邦定讞改認定為員工並適用主要市場","action":"清倉","source_freq":"10-Q 法律程序／每季","date":null,"evidence_refs":["lawsuit_class_action#0","regulatory_antitrust#1"]},{"n":7,"text":"趨勢與財報同時確認後進場","type":"估值rearm","maps_to":"進場","metric":"週收盤價對 104 週均線（約 200.5 美元）；Q4 2026 調整後 EBITDA","threshold":"連 4 週站上，且調整後 EBITDA ≥9 億美元","action":"首筆三分之一","source_freq":"週線／季報","date":"2027-02"},{"n":8,"text":"Q4 季節性利潤率下滑超出指引","type":"風險","maps_to":"R6","metric":"Q4 2026 調整後 EBITDA","threshold":"<9 億美元（指引下緣）","action":"不追，延後首筆","source_freq":"季報／每季","date":"2027-02","evidence_refs":["end_markets#3"]},{"n":9,"text":"可支配支出轉弱（關稅壓力的說法）反映到交易量","type":"風險","maps_to":"H1","metric":"季度 Marketplace GOV 對指引","threshold":"Q4 2026 GOV <354 億美元（指引下緣）","action":"停止加碼","source_freq":"季報／每季","date":"2027-02","evidence_refs":["reg_tariff_export#1"]},{"n":10,"text":"股價跑在盈餘前面","type":"減碼","maps_to":"估值","metric":"FY2027 調整後本益比","threshold":"≥35 倍（約 283 美元）","action":"減碼三分之一","source_freq":"日收盤價與共識／每日","date":null},{"n":11,"text":"交易過關且訂單維持高增速","type":"加碼","maps_to":"H1","metric":"交易審查結果與總訂單年增","threshold":"交易過關（或附條件但不涉佣金上限）且總訂單年增 ≥15%","action":"加碼至目標倉位","source_freq":"8-K 與季報","date":null},{"n":12,"text":"Q4 財報後全面複審","type":"複審日期","maps_to":"全份","metric":"Q4 2026 財報與 2027 展望","threshold":"財報發布後兩週內","action":"重跑判斷","source_freq":"季報","date":"2027-03"}],"kill_metrics":[{"metric":"總訂單年增率","bear_threshold":"連 2 季 <12%","window":"2027 Q1–Q4 季報","source":"季報新聞稿","last_status":"ok"},{"metric":"Net Revenue Margin（take rate）","bear_threshold":"連 2 季年減 ≥0.5 個百分點","window":"每季","source":"季報新聞稿","last_status":"unknown"},{"metric":"GAAP 營益率（年度）","bear_threshold":"FY2027 <6%","window":"FY2027 年報","source":"10-K","last_status":"warning"},{"metric":"Dasher 身分認定","bear_threshold":"加州或聯邦定讞改認定為員工","window":"持續","source":"10-K 與 10-Q 法律程序","last_status":"ok"}],"evidence_dismissed":[],"action_conditions":{"rearm_trigger":"週收盤連 4 週站上 104 週均線（約 200.5 美元），且 Q4 2026 調整後 EBITDA ≥9 億美元","exec_line":"條件成立後先建首筆三分之一。第二筆等 Instacart 審查明朗（不起訴，或附條件但不涉佣金上限）且總訂單年增 ≥15%；第三筆等 FY2027 GAAP 營益率 ≥6%。條件成立前，若股價跌到 250 週均線（約 135 美元）而訂單與指引沒有受損，改為分批反買"}},"decision_inputs":{"signal":"B","ma":"🟠","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":null,"wait_for_price_condition":null,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null},"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8(val爭議)","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='↑', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟠'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":true,"basis":"capalloc_grade='C'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟢', val='🟡', moat_trend='↑', week26=9.67, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position=None, moat='B', moat_trend='↑', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈機械讀數判定不可用，baseline rows 8/9/9b/10 的估值條件視為不可判 → 落 row8 觀望（保守方向）","hit":true,"basis":"val_denominator_disputed=True, val(機械讀數)='🟡'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":"中期 2-5 年","requires_critic":[]},"thesis":{"H":[{"id":"H1","text":"美國本地商務網路密度持續加深，份額不退","2y":"2027 年總訂單年增維持 ≥15%（Q4 2026 起 Deliveroo 已在基期內）","5y":"主要外送 app 刷卡消費占比維持 ≥55%（2026 Q3 為 59%）","10y":null,"threshold":"總訂單年增 ≥12%，且主要外送 app 消費占比 ≥55%","source":"季報新聞稿訂單數；Consumer Edge 刷卡資料（媒體轉述，不定期）","drift_rule":"5 年期：訂單年增連 4 季比門檻低 5% 以上（相對值）為削弱，連 6 季低 10% 以上為反轉"},{"id":"H2","text":"投資期（單一技術平台、自動配送、Deliveroo 整合）結束後，營運槓桿反映在 GAAP 利潤率","2y":"FY2027 GAAP 營益率 ≥6%（FY2025 5.29%、TTM 4.05%）","5y":"FY2030 GAAP 營益率 ≥10%（Instacart 併購攤銷另列）","10y":null,"threshold":"FY2027 GAAP 營益率 ≥6%，FCF 利潤率 ≥11%","source":"年報與季報損益表；CFO 稱技術平台 2027 上半年完工","drift_rule":"2 年期：TTM 營益率連 2 季偏離路徑 5% 以上為削弱，連 3 季偏離 10% 以上為反轉"},{"id":"H3","text":"雜貨、零售與商家軟體成為第二條成長曲線，Instacart 是加速而非拖累","2y":"新垂直業務 2026 年底前毛利轉正（CFO 2026-08-05 承諾，2026-10-29 稱接近兩平）","5y":"Instacart 交割後第三年淨綜效 ≥5 億美元（CFO 2026-10-29）","10y":null,"threshold":"Q4 2026 宣布新垂直毛利轉正；數位點餐營收年增 ≥30%（Q2 2026 逾 40%）","source":"季報、股東信與法說","drift_rule":"2 年期：毛利轉正延後 2 季為削弱，延後 3 季或撤回承諾為反轉；5 年期綜效用交割後的年度揭露檢查"}],"R":[{"id":"R1","text":"Instacart 交易遭聯邦與州深度反壟斷審查，可能拖到 2028 上半年、附帶條件或被擋；被擋要付 12.5 億美元終止費，並占用管理層精力","h_ref":"H3","clock":"🔥","threshold":"主管機關起訴阻止，或 2028-06-30 前未交割","evidence_refs":["regulatory_antitrust#2","regulatory_antitrust#3","competitive_share_entrants#4"]},{"id":"R2","text":"Dasher 身分與勞動成本監管：獨立承包商分類訴訟與政府調查持續，加州 EDD 薪資稅不利評定上訴中","h_ref":"H2","clock":"🐢","threshold":"加州 EDD 評定敗訴定讞，或任一主要州立法要求 Dasher 員工化","evidence_refs":["lawsuit_class_action#0","regulatory_antitrust#1"]},{"id":"R3","text":"轉換成本低，加上反競爭指控，佣金與費用被迫下調","h_ref":"H2","clock":"🔥","threshold":"Net Revenue Margin 連 2 季年減 ≥0.5 個百分點（Q3 2026 為 13.6%），且公司歸因於競爭或監管","evidence_refs":["competitive_share_entrants#1","regulatory_antitrust#0"]},{"id":"R4","text":"他業公司以無人車、無人機配送切入，資源更多、可能先規模化，繞過 Dasher 網路","h_ref":"H1","clock":"🐢","threshold":"他業無人配送在美國前十大都會商轉且訂單占比 ≥5%，而 DASH 的 Dot 仍限於測試市場","evidence_refs":["competitive_share_entrants#2","substitute_technology#0"]},{"id":"R5","text":"國際營運的地緣與制裁法遵：Wolt 部分市場鄰近俄羅斯，2022 年曾因哈薩克動亂暫停當地營運","h_ref":"H1","clock":"🐢","threshold":"單一國家暫停營運，或制裁相關罰款 ≥1 億美元","evidence_refs":["geo_supply_chain#0","geo_supply_chain#1"]},{"id":"R6","text":"Q4 季節性 Dasher 成本、年度保險與全球投資使利潤率季減，Deliveroo 整合有執行風險","h_ref":"H2","clock":"⚡","threshold":"Q4 2026 調整後 EBITDA 低於 9 億美元（指引下緣）","evidence_refs":["end_markets#3"]}],"single_thing":{"description":"加州或聯邦層級以判決或立法定讞，把 Dasher 改認定為員工，並適用公司主要市場","why_fatal":"配送人力是平台最大的變動成本；改成員工要負擔薪資稅、保險、最低工時與福利，單筆成本結構性上升。公司 TTM GAAP 營益率只有 4.05%，每 100 美元 GOV 只賺約 3.1 美元調整後 EBITDA，緩衝很薄；對每股價值的影響遠大於 Instacart 交易成敗（終止費約市值 1.5%）","if_happens":"調整後 EPS 退回空頭路徑（7–8 美元、五年不長），倍數壓到 16 倍以下；清倉","how_monitor":"每季 10-Q 法律程序段落、加州 EDD 薪資稅上訴進度、集體訴訟與仲裁結果、主要州議會立法","probability":"12–24 個月約 5–10%：加州 EDD 已有不利評定但仍在上訴；其他州的立法進度事實表未涵蓋"}},"appendix_a":{"growth_durability":7,"quality_score":7,"ai_risk":"🟡","long_term_confidence":"中","fpe_fy2":23.4,"peg_fy2":1.03,"stress":{"pass":3,"total":4}},"eps_meta":{"base_eps_path":{"FY2025A":null,"FY2026E":5.79,"FY2027E":8.09,"FY2028E":9.93},"fy_end_month":12,"eps_basis":"Koyfin 共識 EPS，推斷為調整後口徑（排除 SBC 與併購攤銷）：同期第三方 GAAP 共識 FY2026 為 2.63 美元，trailing GAAP 本益比 78.56 倍隱含 TTM EPS 約 2.41 美元。FY2025 調整後實際值事實表未涵蓋，基期留空，不混用 GAAP 的 2.13 美元；共識成長率改以 FY2026→FY2028 兩年計"},"catalysts":[{"date":"2027-02","date_precision":"month","type":"guidance","event":"Q4 2026 財報：新垂直毛利是否轉正、Q4 調整後 EBITDA 是否守住 9–11 億美元指引；首次只揭露含 Deliveroo 全期的數字","impact":"高","watch":"Q4 調整後 EBITDA ≥9 億美元；總訂單年增 ≥15%"},{"date":"2027-Q1","date_precision":"quarter","type":"regulatory","event":"Instacart 交易反壟斷審查是否進入深度階段（時點為推估，申報日事實表未涵蓋）","impact":"高","watch":"主管機關是否要求補件或起訴"},{"date":"2027-Q2","date_precision":"quarter","type":"product","event":"單一技術平台完工（CFO 稱 2027 上半年）","impact":"中","watch":"完工後兩季 GAAP 營益率是否回升"},{"date":"2028-Q2","date_precision":"quarter","type":"regulatory","event":"Instacart 預計交割（2027 年底至 2028 上半年）","impact":"高","watch":"交割條件、股票對價比例、終止費是否觸發"}]}
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
