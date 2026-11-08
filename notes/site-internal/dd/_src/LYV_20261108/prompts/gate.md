你是 DD 管線 v20 的判斷層閘（gate），標的 LYV（20261108）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（28 條）
- `f_kpi0_revenue_gaap`（q1_business）｜Revenue (GAAP)＝10105.0 USD M｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 https://news.livenationentertainment.com/news/live-nation-entertainment-reports-third-quarter-2026-results（numbers.latest_quarter_kpis.items[0]，as_of Q3 2026（季末 2026-09-30，公告於 2026-11-05））
  - 註記：查無（新聞稿未列；未另抓第二來源）
- `f_kpi1_non_gaap_operating_incom`（q1_business）｜Non-GAAP operating income (AOI)＝1179.3 USD M｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 https://news.livenationentertainment.com/news/live-nation-entertainment-reports-third-quarter-2026-results（numbers.latest_quarter_kpis.items[1]，as_of Q3 2026（季末 2026-09-30，公告於 2026-11-05））
  - 註記：查無（新聞稿未列；未另抓第二來源）
- `f_kpi2_gaap_operating_income`（q1_business）｜GAAP operating income＝892.0 USD M｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 https://news.livenationentertainment.com/news/live-nation-entertainment-reports-third-quarter-2026-results（numbers.latest_quarter_kpis.items[2]，as_of Q3 2026（季末 2026-09-30，公告於 2026-11-05））
  - 註記：查無（新聞稿未列；未另抓第二來源）
- `f_kpi5_management_guidance_fy20`（q1_business）｜Management guidance FY2026＝fan attendance approach 180M; Concerts & Sponsorship AOI double-digit growth; Ticketing AOI up high single-digits text｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司新聞稿 https://news.livenationentertainment.com/news/live-nation-entertainment-reports-third-quarter-2026-results（numbers.latest_quarter_kpis.items[5]，as_of Q3 2026（季末 2026-09-30，公告於 2026-11-05））
  - 註記：查無（新聞稿未列；未另抓第二來源）
- `f_kpi6_event_related_deferred_r`（q1_business）｜Event-related deferred revenue＝3818.3 USD M｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 https://news.livenationentertainment.com/news/live-nation-entertainment-reports-third-quarter-2026-results（numbers.latest_quarter_kpis.items[6]，as_of Q3 2026（季末 2026-09-30，公告於 2026-11-05））
  - 註記：查無（新聞稿未列；未另抓第二來源）
- `f_peer_lyv_gross_margin_pct`（q2_moat）｜LYV 毛利率＝25.78 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.LYV.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_lyv_operating_margin_pct`（q2_moat）｜LYV 營業利益率＝2.94 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.LYV.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_msge_operating_margin_pct`（q2_moat）｜MSGE 營業利益率＝17.31 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MSGE.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_sphr_operating_margin_pct`（q2_moat）｜SPHR 營業利益率＝-1.68 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.SPHR.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_tko_operating_margin_pct`（q2_moat）｜TKO 營業利益率＝21.71 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.TKO.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_wmg_operating_margin_pct`（q2_moat）｜WMG 營業利益率＝16.11 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.WMG.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝-0.46 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-11-07）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝1.9 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-11-07）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝2.9 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-11-07）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝28534.92 USD m｜期間與口徑：2026-11-08／yfinance revenue_estimate 0y 平均（18 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝30976.6 USD m｜期間與口徑：2026-11-08／yfinance revenue_estimate +1y 平均（24 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi3_free_cash_flow_adjusted`（q1_business）｜Free cash flow—adjusted＝934.4 USD M｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 https://news.livenationentertainment.com/news/live-nation-entertainment-reports-third-quarter-2026-results（numbers.latest_quarter_kpis.items[3]，as_of Q3 2026（季末 2026-09-30，公告於 2026-11-05））
  - 註記：查無（新聞稿未列；未另抓第二來源）
- `f_kpi4_stock_based_compensation`（q1_business）｜Stock-based compensation＝47.3 USD M｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-11-05）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 https://news.livenationentertainment.com/news/live-nation-entertainment-reports-third-quarter-2026-results（numbers.latest_quarter_kpis.items[4]，as_of Q3 2026（季末 2026-09-30，公告於 2026-11-05））
  - 註記：查無（新聞稿未列；未另抓第二來源）
- `f_peer_lyv_fcf_margin_pct`（q2_moat）｜LYV FCF 利潤率＝5.23 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.LYV.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝175.25 USD｜期間與口徑：2026-11-06（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ev_m`（q5_valuation）｜目前企業價值 EV（市值＋淨負債）＝44953.53 USD m｜期間與口徑：2026-11-08／市值 41305.82 ＋ 淨負債 3647.71｜kind：realized
  - 來源：—（numbers.capital_structure.ev_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_ev_s_fwd`（q5_valuation）｜EV/S（EV ÷ FY1 共識營收）＝1.58 x｜期間與口徑：2026-11-08／f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）｜kind：estimate
  - 來源：—（numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝1.61 x｜期間與口徑：2026-11-06（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝100.0 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝100.0 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝3647.71 USD m｜期間與口徑：2026-11-08／yfinance 最新一季：總債務 11905.18、現金 8257.47（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝235.7 m shares｜期間與口徑：2026-11-08／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝4.55 %｜期間與口徑：2026-08-13 → 2026-11-07／FY1 共識 EPS -0.44 → -0.46（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-11-07）

### findings_digest 中方向為負或來源衝突的條目（18 條）
- `competitive_share_entrants#0`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K FY2025 指出自助售票系統與場館自行售票的競爭「顯著且增加」，並列出 SeatGeek、Fever、CTS Eventim 等票務對手，且大型科技／電商公司可能進入。
  - 來源：SEC EDGAR 10-K FY2025 Item 1（as_of 2026-02-19）｜affects：moat_trend、decision_inputs.bear
- `competitive_share_entrants#1`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K FY2025 風險因素：自助售票與客戶自售可能使票務量下降。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-19）｜affects：moat_trend、thesis.R
- `competitive_share_entrants#2`（competitive_share_entrants｜方向 -｜狀態 ok）：美國司法部反壟斷陪審團審判於2026年3月開始；政府主張5至7年長約使場館無法選擇對手。
  - 來源：ABC7 News 報導 Antitrust trial begins（as_of 2026-03-09）｜affects：moat_trend、thesis.R
- `competitive_share_entrants#3`（competitive_share_entrants｜方向 -｜狀態 ok）：2026年分析稱 Eventim 積極擴張美國業務挑戰 Live Nation
  - 來源：Mammoth Times / Finterra（as_of 2026-03-09）｜affects：moat_trend
- `regulatory_antitrust#0`（regulatory_antitrust｜方向 -｜狀態 ok）：10-K 揭露：2024-05 DOJ 與州政府提告反壟斷，求償含剝離 Ticketmaster、取消部分票務合約、禁止反競爭行為與金錢賠償；原定 2026-03-02 開審。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-19）｜affects：moat_trend、thesis.R、decision_inputs.bear
- `regulatory_antitrust#1`（regulatory_antitrust｜方向 -｜狀態 ok）：搜尋摘要：DOJ 於 2026-03-09 開審後與 Live Nation 和解（2.8 億美元基金、剝離至多 13 座圓形劇場、費用上限 15%，不要求剝離 Ticketmaster，待 Tunney Act 法院核准）；拒絕和解的各州續訴，2026-04-15 陪審團認定 Live Nation 在主要票務市場違反反壟斷法。Live Nation 稱將重提 JMOL 並上訴，結構性救濟待法院裁定；估計州方三倍賠償可達 4.5 億美元。資料只到約 2026-05，後續狀態未確認。
  - 來源：WebSearch 摘要（Thompson Coburn、The Ticketing Business 等）（as_of 2026-04-15）｜affects：moat_trend、thesis.R、decision_inputs.bear、valuation、triggers
- `regulatory_antitrust#2`（regulatory_antitrust｜方向 -｜狀態 ok）：陪審團認定 Live Nation／Ticketmaster 違反反壟斷法
  - 來源：The Ticketing Business（as_of 2026-04-16）｜affects：moat_trend、thesis.R
- `end_markets#3`（end_markets｜方向 -｜狀態 ok）：2026 年 3 月起 DOJ 與各州反壟斷審判；紐約州律師稱 Ticketmaster 每張票平均留 $7.58；法官 2 月駁回部分壟斷主張（含票價推高論）；結果報導互相矛盾，未確認；FTC 另有轉售訴訟
  - 來源：NPR/TPR 2026-03-03 'The Live Nation trial could reshape the music industry'（as_of 2026-03-03）｜affects：decision_inputs.bear、thesis.R
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：10-K 風險因子提及來自自助票務系統業者及大型科技/電商公司進入票務市場的競爭
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-19）｜affects：moat_trend、thesis.R
- `channel_business_model_shift#0`（channel_business_model_shift｜方向 -｜狀態 ok）：報導稱 DOJ 和解要求 Ticketmaster 開放第三方使用其技術系統售票（二手報導，需 Tunney Act 核准）
  - 來源：tdp-frontend.pages.dev 轉載文章 2026-03-09（as_of 2026-03-09）｜affects：moat_trend、decision_inputs.bear
- `channel_business_model_shift#1`（channel_business_model_shift｜方向 -｜狀態 ok）：同報導稱和解將 Live Nation 長期獨家合約上限訂為四年
  - 來源：tdp-frontend.pages.dev 轉載文章 2026-03-09（as_of 2026-03-09）｜affects：moat_trend、decision_inputs.bear
- `capital_markets_pricing#1`（capital_markets_pricing｜方向 -｜狀態 ok）：Q1 2026 後 Zacks 稱共識 EPS 估計一個月內下修 36.01%；Q1 調整後每股虧損 32 美分，劣於共識虧損 27 美分
  - 來源：Zacks（經搜尋摘要）Q1 2026 earnings 報導（as_of 2026-05-29）｜affects：valuation、decision_inputs.bear
- `capital_markets_pricing#4`（capital_markets_pricing｜方向 -｜狀態 ok）：Q3 2026 10-Q 九個月營業利益減少 $350.5M，歸因主要為 Governmental Investigations and Litigation（非 guidance 變動）
  - 來源：Live Nation 10-Q 2026-09-30（as_of 2026-11-01）｜affects：decision_inputs.bear、valuation
- `major_events#0`（major_events｜方向 -｜狀態 ok）：2026-04-15 紐約聯邦陪審團認定 Live Nation／Ticketmaster 違反聯邦與州反壟斷法（33 州＋DC 起訴，DOJ 審理中途和解）；救濟與損害賠償由法官另行決定，states 要求最高約 7 億美元並求分拆 Ticketmaster，Live Nation 表示將上訴。
  - 來源：Axios／Music Business Worldwide 等報導（搜尋摘要）（as_of 2026-04-15）｜affects：decision_inputs.bear、thesis.R、moat_trend、valuation
- `major_events#1`（major_events｜方向 -｜狀態 ok）：FTC 與七州 2025 年 9 月對 Live Nation／Ticketmaster 提起消費者保護訴訟（價格欺騙、購票限制、經紀商轉售），公司 2026 年 1 月提出駁回動議。
  - 來源：SEC EDGAR 10-K FY2025 Item 8（as_of 2026-02-19）｜affects：decision_inputs.bear、thesis.R
- `lawsuit_class_action#0`（lawsuit_class_action｜方向 -｜狀態 ok）：2026-04-15 陪審團認定違反反壟斷法，損害賠償與救濟待法官裁定，公司將上訴。
  - 來源：Axios（as_of 2026-04-15）｜affects：decision_inputs.bear、thesis.R、valuation
- `lawsuit_class_action#1`（lawsuit_class_action｜方向 -｜狀態 ok）：FTC＋七州 2025-09 消費者保護訴訟，公司 2026-01 提駁回動議。
  - 來源：SEC EDGAR 10-K FY2025 Item 8（as_of 2026-02-19）｜affects：decision_inputs.bear、thesis.R
- `lawsuit_class_action#2`（lawsuit_class_action｜方向 -｜狀態 ok）：證券集體訴訟（C.D. Cal.，涵蓋 2022-02-23 至 2023-11-20 買入者）為既有案件，搜尋未見近12個月新結果。
  - 來源：Robbins LLP／law-firm 公告（搜尋摘要）（as_of 2023-08-04）｜affects：decision_inputs.bear

### 事實表自陳的缺口（2 條）
- q2_moat：evidence.numbers.peer_financials 該欄整欄為 null（常見於未單獨揭露研發的業者），事實表 agent 若能從財報補就補，補不到即為缺口，判斷者不得自行估。
- q6_how_wrong：digest.qa_flags 有 3 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/LYV_20261108/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":365.0,"bear_5y_price":103.3,"p_bull_pct":22,"p_bear_pct":30,"upside_5y_pct":36.0,"ev5y_pct":28.8,"irr_base_pct":6.3,"asym_ratio":1.9,"scenario_tree":{"terminal_label":"FY2031E","valuation_basis":"sales_multiple","start":{"rev":28534.92,"ev_s":1.58,"basis":"起點用 FY2026E 共識營收，EV÷FY2026E 營收；終端 EV/S 同樣用終端時點 EV÷FY2031E 營收。"},"rev":{"bull":[31800,35600,39700,43800,47800],"base":[30900,33400,36100,38900,41600],"bear":[29800,30400,31200,32400,33800]},"ev_s":{"bull":1.9,"base":1.5,"bear":0.95},"net_debt_y5":{"bull":2500,"base":4000,"bear":6500},"shares_y5":{"bull":242,"base":245,"bear":248},"net_debt_now":3647.71,"shares_now":235.7,"p":{"bull":22,"base":48,"bear":30},"yield_pct":{"dividend":0,"net_buyback":0},"second_stage":null,"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### LYV_Q2_2026_Earnings_Call_20260730.md
- 2026-07-30｜Joe Berchtold｜guidance：CFO 說全年演唱會財測上調，預期全年粉絲數雙位數成長，帶動營收與 AOI 雙位數成長及利潤率擴張（原話："I think we've stepped up our expectation now"）
- 2026-07-30｜Joe Berchtold｜guidance：CFO 說美國粉絲成長全部落在下半年（上半年受體育場檔期影響）（原話："all the fan growth in the U.S. will be in the second half"）
- 2026-07-30｜Joe Berchtold｜guidance：CFO 說 Ticketmaster 全年 AOI 成長預期上調至中個位數（原話："increased our expectation for AOI growth for the full year"）
- 2026-07-30｜Joe Berchtold｜guidance：CFO 說露天劇場約 70% 的全年成長集中在下半年（原話："mainly back half, 70% focused in terms of the"）
- 2026-07-30｜Michael Rapino｜guidance：CEO 說 2027 年預訂量已有大比例到位，各場館類型看來仍強（原話："We already have a big percentage of our bookings in"）
- 2026-07-30｜Joe Berchtold｜margin：CFO 解釋利潤率擴張的基礎：自營場館粉絲數成長快於第三方場館（原話："the foundation of what sets us up for margin expansion."）
- 2026-07-30｜Joe Berchtold｜margin：CFO 對自營場館成長較快的口徑：Live Nation 只經營少數場館，自營端有更多可著力的環節（原話："We run a small minority of venues."）
- 2026-07-30｜Joe Berchtold｜margin：CFO 提供 Ticketmaster 收費票數成長口徑（高個位數）（原話："fee-bearing ticket count by high single digits"）
- 2026-07-30｜Joe Berchtold｜margin：CFO 說現場人均消費全面上升（原話："per caps on-site spending is up."）
- 2026-07-30｜Michael Rapino｜customer：CEO 說至今未見消費者購買端問題（原話："we've seen no consumer issues to date in terms"）
- 2026-07-30｜Michael Rapino｜customer：CEO 說取消率 1.1%，低於歷史平均 1.6%（原話："at 1.1% cancellations versus 1.6% average."）
- 2026-07-30｜Michael Rapino｜customer：CEO 說酒類消費年增，未見消費者減少飲酒（原話："Liquor is up year-over-year"）
- 2026-07-30｜Michael Rapino｜competition：CEO 說不把 Spotify 視為票務競爭者，Spotify Reserved 為付費取得預售票額的傳統合作（原話："we don't look at Spotify as a ticketing"）
- 2026-07-30｜Michael Rapino｜competition：CEO 說 Spotify 配額在全球規模上很小（原話："small allocation on a global basis"）
- 2026-07-30｜Joe Berchtold｜competition：CFO 說二級市場票務占全球 GTV 低雙位數（原話："Secondary now on a global GTV basis is below teens."）
- 2026-07-30｜Joe Berchtold｜competition：CFO 說演唱會二級市場票約占全球 GTV 5%（原話："probably 5% of our global GTV."）
- 2026-07-30｜Michael Rapino｜competition：CEO 說日本市場自家占有率很小，90% 為本地業務（原話："We have a very small market share today."）
- 2026-07-30｜Joe Berchtold｜product：CFO 說 Ticketmaster 已進入 6 個拉美與 6 個亞太市場（原話："now in 6 Latin America markets, 6 Asia Pacific markets"）
- 2026-07-30｜Joe Berchtold｜product：CFO 說用 AI 輔助 Ticketmaster 的程式開發（原話："we're using AI to help power our coding and"）
- 2026-07-30｜Michael Rapino｜product：CEO 說 Spotify Reserved 於 5 月以 Role Model 巡演首度上線（原話："We launched Spotify in May with Role Model"）
- 2026-07-30｜Joe Berchtold｜capital_allocation：CFO 說今年已完成 3 座場館收購（原話："we've completed the acquisition of 3 arenas so far"）
- 2026-07-30｜Joe Berchtold｜capital_allocation：CFO 說 2027 年底前預計再有 4 至 5 座收購（原話："probably 4 or 5 in that period"）
- 2026-07-30｜Joe Berchtold｜capital_allocation：CFO 說資本支出增加的效益要到 2028 年才明顯（原話："probably '28 before we really start seeing the impact"）
- 2026-07-30｜Joe Berchtold｜commitment：CFO 說明年資本支出為漸進增加，不會倍增（原話："we're not doubling, tripling. We're not leaping."）
- 2026-07-30｜Joe Berchtold｜commitment：CFO 說會繼續淘汰報酬不達標的專案（原話："turning down a lot of projects that don't."）
- 2026-07-30｜Michael Rapino｜risk：CEO 說拉美仍在早期，巴西等大型場館尚未營運（原話："we're in the second kind of inning of the 9-inning game"）
- 2026-07-30｜Michael Rapino｜risk：CEO 說約九成演出不會完售，需靠分銷夥伴協助（原話："90% of shows don't sell out"）

### 問答異常語氣（迴避／改口／保留）
- LYV_Q2_2026_Earnings_Call_20260730.md｜問：Steven Cahall 問新增 1,500 萬粉絲產能是否意味 2027 年再度雙位數粉絲成長｜答法：CFO 未回答是否雙位數，表示現在談明年與 1,500 萬運行速率如何流入「還太早」（原文 'premature to talk specifically about next year'）
- LYV_Q2_2026_Earnings_Call_20260730.md｜問：Peter Henderson 問 2027 早期巡演管線與 2026 相比如何｜答法：CEO 未給比較數字，改談一貫的全球擴張策略，僅說「已有大比例預訂」「仍早但令人鼓舞」
- LYV_Q2_2026_Earnings_Call_20260730.md｜問：Robert Fishman 問 2027 年資本支出更新｜答法：CFO 稱規劃仍在早期不給具體數字，只說會是漸進增加

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 4 | 2 |
| customer_second_source | found | 1 | 3 |
| customer_concentration_credit | found | 2 | 2 |
| supply_demand_durability | found | 5 | 3 |
| regulatory_antitrust | found | 3 | 1 |
| reg_tariff_export | none | 0 | 2 |
| geo_supply_chain | found | 1 | 1 |
| end_markets | found | 5 | 3 |
| substitute_technology | found | 1 | 2 |
| channel_business_model_shift | found | 4 | 1 |
| capital_markets_pricing | found | 6 | 4 |
| major_events | found | 4 | 5 |

未涵蓋／不適用軸的查詢詞原文（供判相關性）：
- **reg_tariff_export**（none）：Live Nation Entertainment tariff 2026；Live Nation tariffs touring artists visas export control China trade restriction 2026

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260518","verdict":"觀望 — thesis 完整（Concerts +11%、Sponsorship +21%）但估值🔴過熱（PEG 2.6 + 5Y 80% 分位）+ Subramanian remedy 二元未明。等 5 或裁決明朗化","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"監管衝擊有限：DOJ remedy phase 不強制 Ticketmaster + Concerts 結構性分拆，僅 behavioral remedy（15% fee cap、開放 SeatGeek/StubHub），對集團 AOI 影響 &lt; 5%。","columns":{"2Y 驗證點（至 2028）":"2027 Judge Subramanian remedy 公布；若 behavioral-only → H1 ✓；若 structural break-up → H1 ✗。Ticketmaster Q AOI margin 維持 ≥ 32%。","5Y 驗證點（至 2031）":"上訴階段（若有）2030 結案，遠端 Ticketmaster 護城河仍在；fee cap 後 Ticketmaster Revenue 仍 +6-8% 年成長。","10Y 驗證點（至 2036）":"監管常態化後 Ticketmaster ARR 仍佔集團 25-30% AOI，垂直整合 synergies 保留。","驗證指標":"(1) Judge Subramanian 裁決文本；(2) Ticketmaster AOI margin（門檻 ≥ 32%）；(3) 集團 AOI YoY ≥ +8%"}},{"id":"H2","text":"Concerts 結構性需求延續：Gen Z + Millennial 體驗消費偏好不變，Stadium 大型 show 需求 5 年內維持雙位數成長，Concerts AOI 累積至 ~.5B（5Y CAGR +18%）。","columns":{"2Y 驗證點（至 2028）":"FY 2027-2028 Concerts attendance ≥ 175M（vs 2025 159M），AOI ≥ 0M（vs 2025 7M）。","5Y 驗證點（至 2031）":"FY 2031 Concerts attendance ≥ 220M，AOI ≥ B（margin 升至 4.5%）。","10Y 驗證點（至 2036）":"FY 2036 Concerts revenue ≥ B（vs 2025 B），全球 Stadium tier penetration 30%+。","驗證指標":"(1) 年度 fan attendance；(2) Concerts AOI margin（門檻 ≥ 3.5%）；(3) 大型 show pipeline YoY"}},{"id":"H3","text":"Sponsorship + Ticketing 高毛利雙引擎延續：Sponsorship AOI 5 年 CAGR ≥ +12%、Ticketing AOI 即使受 fee cap 影響仍 ≥ +5% 年成長。","columns":{"2Y 驗證點（至 2028）":"FY 2027 Sponsorship AOI ≥ B（vs 2025 5M），Ticketing AOI ≥ .15B。","5Y 驗證點（至 2031）":"FY 2031 Sponsorship AOI ≥ .5B，Ticketing AOI ≥ .3B（已吸收 fee cap 衝擊）。","10Y 驗證點（至 2036）":"FY 2036 高毛利兩段合計 AOI 占集團 75%+。","驗證指標":"(1) Sponsorship YoY；(2) Ticketing 138M fee-bearing tix 是否續成長；(3) take rate after fee cap"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"Judge Subramanian remedy 強制結構性分拆（拆分 Ticketmaster / Concerts，或剝離 venue 業務）","columns":{"對應假設":"H1","時間尺度":"🐢 中期（18-24 個月，2027-2028 期）","監測指標":"(1) Subramanian 公開裁決，(2) DOJ 補充 motion，(3) 26 states+DC 立場","警戒閾值":"若 remedy 包含「強制業務分拆」或「強制資產出售」中任一 → R1 觸發 → 立即減倉 2/3"}},{"id":"R2","text":"Concerts artist take rate 失控（大牌 artist 拿走 95%+ 收入，Concerts AOI margin 跌穿 2.5%）","columns":{"對應假設":"H2","時間尺度":"⚡ 短期（4-8 季）","監測指標":"(1) 季度 Concerts AOI margin；(2) 大型 show（Stadium tour）占比變化；(3) 法律 fees 是否擠壓 margin","警戒閾值":"連 2 季 Concerts AOI margin &lt; 2.5% → R2 觸發 → 重評 H2"}},{"id":"R3","text":"估值倍數均值回歸（市場開始用 30-40x PE 而非 78x 定價 LYV，無外部催化也能下行 -40%）","columns":{"對應假設":"H1/H3","時間尺度":"🔥 中短期（6-18 個月）","監測指標":"(1) 5Y NTM PE 分位；(2) 同業 EV/EBITDA 趨勢；(3) CTS Eventim relative valuation","警戒閾值":"5Y NTM PE 分位 &gt; 90% 持續 4 週 或 同業 PE 收斂 +20% → R3 已實現"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🔴","ma":"✅","trap":"🟡","moat_trend":null,"runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":168.87,"archetype":null,"cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"LYV","date":"2026-11-08","schema":"v15.0","contract":"v19","company_name":"Live Nation Entertainment"},"oneliner":"全年粉絲近 1.8 億、票務財測上修，需求論點成立；但州方反壟斷救濟未定，現價的基準五年年化報酬只有約 6%，等價格與救濟結果再談。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/LYV_20261108/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/LYV_20261108/scenario.json","answers":{"q1_business":{"verdict":"賺粉絲與品牌的錢，利潤卡在票務與贊助兩個節點，演唱會負責導流。","reasoning":"Q3 營收 101.05 億美元，AOI 11.79 億，GAAP 營業利益 8.92 億，營業利益率 8.8%，AOI 利潤率 11.7%。票務營收約 8.8 億（由年增 7,270 萬、+9% 反推）、AOI 3.157 億；贊助營收 5.057 億、AOI 3.502 億。兩者合計占營收約 14%，占合併 AOI 約 56%，這是演唱會旺季的單季比重，全年結構事實表未涵蓋。其餘約 87 億營收來自演唱會，扣公司費用後 AOI 約 5.1 億。近 12 個月毛利率 25.78%，單季毛利率事實表未涵蓋。產業時鐘在擴張期：2026 全年粉絲近 1.8 億，Q3 單季逾 6,000 萬、近 +20%，CFO 說售完率高於去年、取消率更低。供需判斷為結構性持久，但 2026 有檔期推升，Q3 北美增幅有一部分是世界盃造成的體育場檔期後移。單點依賴不在客戶，10-K 揭露無單一客戶占營收超過 10%；集中度在頭部藝人的巡演檔期，事實表未量化。事實表財務歷史欄顯示 FY2025 淨利 4.96 億美元卻對應稀釋每股盈餘 −0.24 美元，差距成因事實表未涵蓋，所以每股盈餘不能直接拿來判斷本業。","fact_refs":["f_kpi0_revenue_gaap","f_kpi1_non_gaap_operating_incom","f_kpi2_gaap_operating_income","f_kpi5_management_guidance_fy20","f_kpi6_event_related_deferred_r","f_peer_lyv_gross_margin_pct"],"verdict_values":{"revenue_quality":"預收型：Q3 底事件遞延收入 38.18 億美元，年增 8%；Q2 底為 64 億、年增 25%，Q3 增速放緩有一部分是下半年檔期已經演出。","unit_econ_note":"CFO 說自營場館粉絲的每人利潤高於第三方場館，體育場票價高但利潤率低。每位粉絲的金額事實表未涵蓋。","archetype":{"primary":"品質複利成長","secondary":"轉機/特殊情境","confidence":"中","fingerprint":"場館與票務平台靠規模擴張，短期每股盈餘被訴訟費用壓低，救濟結果未定"},"industry":{"clock_phase":"II","sd_verdict_source":"結構性持久。依據是 2026-07-30 CEO 稱取消率 1.1%、低於歷史均值 1.6%，2026-11-05 CFO 稱售完率高於去年，Goldman Sachs 2026 音樂報告看法相同。","bargaining":{"up":"頭部藝人議價力最強，演唱會利潤薄反映這點。","down":"對場館靠票務長約，對粉絲靠票源獨家，兩者正是訴訟焦點。","geo":"Q3 國際粉絲 +29%，拉美、歐洲、亞洲都至少 +15%；CEO 說拉美仍在早期，日本份額很小。"},"profit_pool_dir":"往自營場館、贊助與國際移動。","tam_table":{"expanded":false,"reason":"事實表沒有 TAM 與滲透率資料，全年近 1.8 億人次只能描述規模，無法算份額；成長論點靠場館產能與國際擴張，等投資人日資料再展開。"}}}},"q2_moat":{"verdict":"護城河方向為穩定：執行面擴大，定價與合約面被法律縮減，兩者相抵；救濟若擴大就轉為縮減。","reasoning":"機制是三段飛輪：演唱會帶票務、場館合約綁票務、粉絲規模帶贊助。Q3 票務 AOI 年增 10%，收費票數 9,830 萬張對 8,910 萬，今年至今新增淨客戶票量逾 2,000 萬張，CFO 也說預期中的二級市場逆風沒有出現，目前沒有失血跡象。縮減端是法律：陪審團 2026-04-15 認定主要票務市場違法，DOJ 和解報導含四年獨家上限、開放第三方使用票務系統、剝離至多 13 座圓形劇場與 15% 費用上限。事實表的法律進度只到約 2026-05，此後狀態未確認，方向判斷的信心偏低。可能看錯的地方：合約年限縮短要到續約才反映在數字，現在的量價數據無法排除這個遞延效應。同業 ROIC 差距事實表未涵蓋，這裡改看票量軸；列表同業利潤率較高，但業態不同，不構成比較。","fact_refs":["f_kpi1_non_gaap_operating_incom","f_peer_lyv_gross_margin_pct","f_peer_lyv_operating_margin_pct","f_peer_msge_operating_margin_pct","f_peer_sphr_operating_margin_pct","f_peer_tko_operating_margin_pct","f_peer_wmg_operating_margin_pct"],"verdict_values":{"moat":{"mechanism":"演唱會帶票務、場館長約綁票務、粉絲規模帶贊助的三段飛輪。定價分只反映票務與場館端，演唱會端藝人拿走大部分；法律衝擊只記在威脅扣分，不重複計入定價分。","execution":8,"pricing":8,"grade":"B","trend":"→","trend_evidence":"執行面擴大：今年新增淨客戶票量逾 2,000 萬張，Q3 收費票數 +10%。定價與合約面縮減：陪審團判決與和解條款限制獨家年限。兩者相抵判為穩定；若法院命令剝離或把獨家限制擴大，改判縮減。","competitor_notes":[{"name":"MSGE","strategy_note":"自有場館、單一市場，營業利益率 17.31% 反映資產稀缺，不是票務平台的直接對手。"},{"name":"SPHR","strategy_note":"重資產場館，營業利益率 −1.68%，可作新場館投入期成本的反面參照。"},{"name":"TKO","strategy_note":"賺轉播權利金，營業利益率 21.71%，與演唱會分潤模式不同。"},{"name":"WMG","strategy_note":"在藝人上游，營業利益率 16.11%，拿的是版權端的分配。"},{"name":"CTS Eventim","strategy_note":"報導稱積極擴張美國，事實表沒有份額與倍數。"},{"name":"SeatGeek","strategy_note":"10-K 列為票務對手，事實表沒有份額資料。"}],"peer_na_reason":"事實表只有同業利潤率，沒有投入資本與 ROIC，且同業業態不同，無法計算報酬差距。","threats":[{"level":"🔴","text":"反壟斷救濟：州方求分拆 Ticketmaster 與最高約 7 億美元；DOJ 和解條款含四年獨家上限、開放第三方使用系統、剝離至多 13 座圓形劇場。","p":"30%","evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#1","regulatory_antitrust#2","major_events#0","lawsuit_class_action#0","competitive_share_entrants#2","end_markets#3","channel_business_model_shift#0","channel_business_model_shift#1"]},{"level":"🟡","text":"自助售票、場館自售、SeatGeek、Fever 與 Eventim 美國擴張，10-K 也點名大型科技與電商可能進入；目前淨客戶票量仍增加。","p":"30%","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1","competitive_share_entrants#3","substitute_technology#0"]}],"roic_durability":{"quadrant":"低利益率×高周轉（周轉率事實表未涵蓋，由預收票款模式推定）","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"粉絲是使用者也是付款者，全年近 1.8 億人次；取消率 1.1% 低於歷史均值 1.6%。演出可以延後，但目前沒有延後跡象。"},{"item":"決策層級","level":"🟡","text":"票務決策單位是場館，長約原本 5 至 7 年，和解報導把獨家上限訂為四年，決策頻率會提高；今年新增淨客戶票量逾 2,000 萬張，目前仍在贏。"},{"item":"價值鏈分配","level":"🟡","text":"近 12 個月毛利率 25.78%，藝人拿走演唱會大部分價值；紐約州律師稱 Ticketmaster 每張票平均留 7.58 美元。自營場館讓公司多拿現場消費與贊助，但要投入資本。"},{"item":"社會容忍度","level":"🔴","text":"陪審團認定違法，33 州與華府起訴，FTC 另告消費者保護，費用上限 15% 已進和解條款。實際定價上限現在由政治與法律決定。"}],"roiic":"事實表未涵蓋投入資本，無法計算增量報酬。","reinvest_rate":"事實表未涵蓋折舊、營運資金與收購淨額，無法按公式計算；粗看 2026 資本支出指引 11 至 12 億美元，約等於 FY2025 營業利益 12.3 億的九成以上。","endo_ceiling":null,"formula_note":"FY2025 營業利益由 4.89%×252.01 億美元算出，只作規模參照，不是再投資率。CFO 2026-07-30 說效益要到 2028 年才明顯。"}}}},"q3_growth":{"verdict":"五年後的跑道為中等：場館與國際還有空間，但事實表沒有滲透率，無法給到寬。","reasoning":"成長以量為主，2026 粉絲增量約 2,000 萬人次，人均消費與價其次，併購補場館，淨回購為零。三年共識每股盈餘年複合無法計算，因為 FY2025 基期 −0.24 美元與 FY2026E −0.46 美元都是負值；FY2027E 1.9 到 FY2028E 2.9 美元增 52.6%，是從被壓低的基期反彈，不是成長率。共識營收 FY2026E 285.35 億、FY2027E 309.77 億，年增 13.2% 與 8.6%。內生上界因投入資本缺資料而留空，缺口歸因為無法歸因，依賴re-rate 的疑慮保留，長期信心上限為中。CFO 2026-07-30 說資本支出效益要到 2028 年才明顯，FY2027 成長多半仍靠既有場館與檔期；當時問到 2027 是否再有雙位數粉絲成長，CFO 說還太早，Q3 也沒有給。","fact_refs":["f_kpi5_management_guidance_fy20","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m"],"verdict_values":{"growth":{"driver_mix":"量為主（人次與收費票數），人均消費與價其次，併購補場館，淨回購為零。","runway_years":"事實表未涵蓋滲透率，無法計算","runway_post_y5":"🟡","endo_ceiling_basis":"事實表未涵蓋投入資本、折舊、營運資金與收購淨額，增量報酬與再投資率都算不出來，內生上界留空；無法驗證時保守視同共識成長超出上界。","segments":[{"item":"票務（Q3 2026）","value":"營收約 8.8 億美元（由年增 7,270 萬、+9% 反推），AOI 3.157 億、年增 10%，收費票數 9,830 萬張對 8,910 萬。"},{"item":"贊助與廣告（Q3 2026）","value":"營收 5.057 億美元、+14%，AOI 3.502 億、+12%，國際占成長 65%。"},{"item":"演唱會含公司費用（Q3 2026，由合併數倒減）","value":"營收約 87 億美元，AOI 約 5.1 億；粉絲逾 6,000 萬、近 +20%。"}],"decay_signals":[{"name":"毛利率連 2 季年減","lit":false,"note":"事實表只有 TTM 與年度，單季資料缺口。"},{"name":"核心市占近 12 個月縮減","lit":false,"note":"今年新增淨客戶票量逾 2,000 萬張。"},{"name":"提價後銷量下滑","lit":false,"note":"售完率高於去年。"},{"name":"每股盈餘成長高於營收成長逾 5 個百分點","lit":true,"note":"FY2027E 到 FY2028E 每股盈餘 +52.6%，主因基期被壓低。"},{"name":"FCF／淨利低於 0.75 連 2 年","lit":false,"note":"FY2025 0.61 倍、FY2024 1.17 倍，只有一年。"},{"name":"SBC／營收高於 5% 且上升","lit":false,"note":"Q3 為 0.47%。"},{"name":"TAM 萎縮或被替代","lit":false,"note":"未見證據。"},{"name":"產業倍數近 3 年系統性下移","lit":false,"note":"同業倍數資料缺口。"},{"name":"維護性資本支出占 FCF 逾 60%","lit":false,"note":"2026 指引扣掉 8 至 8.5 億擴建後約 3 億上下，精確值事實表未涵蓋。"},{"name":"停止投資且收入下滑","lit":false,"note":"場館管線擴張中。"}]}}},"q4_capital":{"verdict":"資本配置暫時看不清：稀釋低、沒有回購，錢主要投場館，報酬要等投資人日。","reasoning":"事實表財務歷史欄的 FCF 除以淨利：FY2024 1.17 倍、FY2025 0.61 倍；FY2025 FCF 僅 3.05 億美元、利潤率 1.21%，近 12 個月回到 5.23%。Q3 SBC 4,730 萬美元，占營收 0.47%。2026 資本支出指引 11 至 12 億美元，其中 8 至 8.5 億用於場館擴建。現金去向四分、債務到期與加權利率事實表未涵蓋。CFO 2026-07-30 說會持續拒絕報酬不達標的專案，但夥伴出資比例與投資報酬在 Q3 法說被推到投資人日。2026 年收購金額未揭露，併購報酬無法驗證。","fact_refs":["f_kpi3_free_cash_flow_adjusted","f_kpi4_stock_based_compensation","f_peer_lyv_fcf_margin_pct"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":true,"passed":null,"input":"2026 年多筆場館收購金額未揭露，投入資本事實表未涵蓋，無法驗證。"},{"name":"buyback_yield","applicable":false,"passed":null,"input":"事實表沒有回購資料；管理層指引 2026 年股數大致不變。"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"Q3 SBC 4,730 萬美元，年化約 1.9 億，約占市值 0.46%，低於每年 1.5% 上限；可轉債與選擇權的完整稀釋未計。"}]},"governance":{"capital_returns":{"expanded":false,"reason":"2026 年收購金額未揭露，事實表也沒有現金去向四分，無法算併購報酬；場館投資報酬與夥伴出資比例要等投資人日。"}}}},"q5_valuation":{"verdict":"現價要求五年營收年複合約 8% 且倍數只小降，才有約 6% 年化；成長我相信，但這個回報付不起救濟風險。","reasoning":"EV 449.5 億美元除以 FY2026E 共識營收 285.35 億得 1.58 倍，在四個年度端點中最高；這不是五年分位，五年分位事實表未涵蓋。本益比只能看遠期：FY2027E 92.2 倍、FY2028E 60.4 倍，都建立在被壓低的基期。基準情境終端每股約 238 美元，五年 +36%。短期以 FY2027E 基準營收 309 億、維持 1.58 倍、淨負債約 37 億、股數 238 百萬股估約 190 美元，+8%。敏感度：終端 EV/S 每 0.1 倍約 17 美元，終端營收每 5% 約 13 美元，終端淨負債每 10 億美元約 4 美元。賣方均值目標 191 至 202 美元，比現價高 9% 至 15%，最低 145、最高 222，全距不大；我比賣方保守的地方在救濟風險，賣方目標沒有揭露這部分機率，我也沒有主張市場看錯。共識修正要小心讀：事實表的近 3 月 FY1 修正寫 +4.55%，實際是 −0.44 美元變 −0.46 美元、虧損擴大，正負號被負分母反轉；11-07 的快照也可能尚未反映 Q3 財報。","fact_refs":["f_price_at_dd","f_ev_m","f_ev_s_fwd","f_ev_s_current","f_ev_s_percentile","f_ps_percentile","f_net_debt_m","f_shares_diluted_m","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_3m_fy1_pct","f_kpi6_event_related_deferred_r"],"verdict_values":{"valuation":{"basis":"前瞻 EV/S，因 FY2026E 共識每股盈餘為負。","peers":{"expanded":false,"reason":"事實表的同業欄只有利潤率，沒有倍數；MSGE、SPHR、TKO、WMG 的業態也與票務加演唱會不同，終端倍數只能用自身現值錨定，缺同業對照。"},"fwd_pe":92.2,"peg":null,"percentile_5y":null,"val_light":"🟠","val_light_derivation":"基準五年年化約 6%，低於 8%；EV/S 為四個年度端點最高；FY2027E 本益比 92 倍但基期被壓低，沒有極端高估的證據，定為偏貴。三年 PEG 因基期為負無法計算，五年分位資料缺口。","upside_short_pct":8.2,"upside_mid_pct":36.0,"denominator_disputed":true,"denominator_note":"每股盈餘被訴訟費用壓低，FY2026E 為負，不能當分母；EV 的現金 82.57 億內有事件遞延收入 38.18 億，屬未履約的預收票款，扣除後 EV/S 由 1.58 倍升到 1.71 倍。本次情境沿用 1.58 倍口徑，不把低倍數當便宜的論據。"}}},"q6_how_wrong":{"verdict":"最可能看錯在救濟力道與時點，不在需求。","reasoning":"法律進度資料停在約 2026-05，Q3 法說也沒有人問到救濟進度。歷史最大回撤與空方最強數字事實表未涵蓋。法說迴避紀錄有兩組：2026-11-05 CFO 沒有拆解 Q4 演唱會 AOI 的隱含改善，場館併購進度與夥伴資本支出延到投資人日；2026-07-30 對 2027 雙位數粉絲成長、2027 巡演管線對比與 2027 資本支出都沒有給數字。三個反方視角的裁定見反證紀錄。","fact_refs":["f_kpi2_gaap_operating_income","f_kpi5_management_guidance_fy20","f_ev_s_fwd"],"verdict_values":{"trap":{"verdict":"🟡","label":"訴訟未定，商業面未見衰退"}}}},"scenario_inputs":{"valuation_basis":"sales_multiple","terminal_label":"FY2031E","start":{"rev":28534.92,"ev_s":1.58,"basis":"起點用 FY2026E 共識營收，EV÷FY2026E 營收；終端 EV/S 同樣用終端時點 EV÷FY2031E 營收。"},"rev":{"bull":[31800,35600,39700,43800,47800],"base":[30900,33400,36100,38900,41600],"bear":[29800,30400,31200,32400,33800]},"ev_s":{"bull":1.9,"base":1.5,"bear":0.95},"net_debt_y5":{"bull":2500,"base":4000,"bear":6500},"shares_y5":{"bull":242,"base":245,"bear":248},"p":{"bull":22,"base":48,"bear":30},"yield_pct":{"dividend":0,"net_buyback":0},"max_dd":{"lo":-55,"hi":-35,"basis":"Bear 終點約 −41%，路徑低點通常比終點再深 10 至 15 個百分點，救濟裁定不利加消費下行可到 −55%；單獨估值修正約 −35%，約 114 美元，接近 250 週均線 116.07 美元。歷史最大回撤事實表未涵蓋，這個範圍沒有歷史校準。","trigger_time":null},"basis":{"bull":"只有範圍有限的行為救濟，場館提早貢獻、國際擴張，營收年複合約 10.9%，自營場館提升利潤率，倍數 1.9 倍。","base":"行為救濟收場，粉絲與場館按既定管線成長，營收年複合約 7.8%，倍數小降到 1.5 倍；事實表沒有同業 EV/S 可對照，只能對照自身現值 1.58 倍。淨負債計入賠償、場館與夥伴權益支出後約 40 億美元。","bear":"救濟力道重或票務份額流失，加上 2027 檔期回落，營收年複合約 3.4%，倍數 0.95 倍，淨負債計入和解基金與州方賠償後約 65 億美元。機率 30%：強制剝離約 15% 至 20%，其餘來自重度行為救濟與需求回落；內生上界無法驗證也要求不低於 30%。"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"陪審團 2026-04-15 認定違法，33 州與華府求分拆 Ticketmaster 與最高約 7 億美元；DOJ 和解條款若落地，長約鎖定效果會縮短。","assumption":"基準假設救濟止於行為面，Ticketmaster 留在集團，票務 AOI 利潤率維持 32% 以上。","consequence":"若法院命令剝離或擴大獨家限制，票務與演唱會的交叉導流斷開，Bear 情境每股約 103 美元、較現價 −41%；跌 50% 需要再加上消費下行。","ruling":"部分採納。這條與唯一致命點部分重疊，剝離只是其中一條路徑。救濟結果在裁定公布前不可裁決，只能用機率處理；社會容忍度已是紅色，不把現有量價數字當成風險已解。","watch":"法院救濟裁定、Tunney Act 核准、票務 AOI 利潤率、客戶續約年限。","evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#1","regulatory_antitrust#2","major_events#0","lawsuit_class_action#0"]},{"view":"論點失敗","evidence":"事實表的法律資料只到約 2026-05，救濟程序、JMOL、Tunney Act 的最新狀態都未確認，Q3 逐字稿也沒有相關問答。","assumption":"這六個月沒有發生足以改變機率的裁定。","consequence":"若已有裁定，本次 Bear 機率與 Single Thing 機率都可能過時。","ruling":"採納為資料缺口。下一輪研究必須先補法院文件與 Q3 10-Q 法律附註，再更新機率。","watch":"Q3 10-Q 法律附註全文、法院案件紀錄。","evidence_refs":["regulatory_antitrust#1","end_markets#3"]},{"view":"論點成功但股東經濟變差","evidence":"FY2025 FCF 利潤率 1.21%，淨利 4.96 億美元卻每股 −0.24 美元；CFO 2026-11-05 說體育場利潤率較低、開幕前費用未來幾年上升；2026 資本支出指引 11 至 12 億美元，效益要到 2028 年。","assumption":"粉絲成長能轉成每股現金。","consequence":"粉絲與 AOI 都達標，但資本支出、夥伴分成與非控制權益分走利潤，每股價值增幅低於營收，基準的 245 百萬股與 40 億淨負債會偏樂觀。","ruling":"採納為主要保留。H2 門檻加上 FCF 利潤率，投資人日揭露夥伴出資比例與投資報酬之前，資本報酬檢查維持未知。","watch":"投資人日場館投資報酬與夥伴出資比例、FY2027 FCF 利潤率、開幕前費用。","evidence_refs":["capital_markets_pricing#4"],"fact_refs":["f_peer_lyv_fcf_margin_pct"]},{"view":"價格已反映太多","evidence":"EV/S 1.58 倍為四個年度端點最高，FY2027E 本益比 92.2 倍，賣方均值目標只比現價高 9% 至 15%。","assumption":"現價已把行為救濟當基準，也計入 2026 的檔期高點。","consequence":"基準五年年化約 6%，機率加權約 5%，好消息的上檔有限。","ruling":"採納，這是本次不進場的主因。即使裁定只有行為救濟，上修 Bull 機率後仍需要價格配合。","watch":"EV/S、股價相對 150 美元、賣方目標。","fact_refs":["f_ev_s_fwd","f_ev_s_percentile","f_consensus_eps_fy2"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 168.87 → 本次 175.25（+3.8%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=168.87","side_b":"本次 price_at_dd=175.25","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 168.87 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 168.87 美元：五年期望值 前份未列，基準年化 前份未列，前份未列不對稱比","side_b":"本次情境、股價仍用 168.87 美元：Bull 價 364.96、Bear 價 103.27，五年期望值 +33.6%，基準年化 7.1%，不對稱比 2.19","ruling":"先換情境、股價不動：五年期望值與基準年化前份未列，無法比較。前份未列不對稱比，本次為 2.19。Bull、Bear 價位與股價無關，只受情境影響。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 168.87 美元：五年期望值 +33.6%，基準年化 7.1%，不對稱比 2.19","side_b":"本次情境、股價 175.25 美元：五年期望值 +28.8%，基準年化 6.3%，不對稱比 1.93","ruling":"再換股價、情境不動：起點價上漲 3.8%，五年期望值少 4.9 個百分點，基準年化少 0.8 個百分點，不對稱比由 2.19 降到 1.93。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"反壟斷救濟力道","cause":null,"prior_field":null,"side_a":"陪審團認定違法，州方求分拆 Ticketmaster，等於否定垂直整合的合法性。","side_b":"DOJ 和解不要求剝離，公司將提 JMOL 並上訴；2026 年票務與粉絲數據沒有受損。","ruling":"方向相反，屬不可調和。基準選和解路徑，依據是 DOJ 和解已明定不要求剝離，事實表也未見法院朝分拆方向裁定。決勝資料是救濟裁定，現在不存在，裁定公布前不可裁決。","evidence_level":"中：判決與和解多為二手報導，進度只到約 2026-05。","settle_metric":"法院救濟裁定文本","if_then":["若法院命令剝離 Ticketmaster，清倉並重跑研究。","若裁定只有行為救濟且獨家上限不短於四年，Bull 機率上調到 30%，股價到 150 美元以下才分批反買。","反向條件：若上訴推翻陪審團認定，Bear 機率下修到 20% 並重跑研究。"],"evidence_refs":["regulatory_antitrust#1","major_events#0","lawsuit_class_action#0"]},{"axis":"Q3 強勁的持續性","cause":null,"prior_field":null,"side_a":"2026-07-30 CFO 給票務 AOI 中個位數成長，2026-11-05 上修到高個位數；全年粉絲上修到近 1.8 億，2027 預付廣告雙位數成長。","side_b":"Evercore 分析師 2026-11-05 指出前 9 月演唱會 AOI 只 +4%；Q3 北美增幅部分來自體育場檔期後移，事件遞延收入年增由 Q2 的 25% 降到 Q3 的 8%。","ruling":"可調和，屬程度差異。管理層上修屬實，2026-07-30 說的美國粉絲成長集中下半年也兌現，但 Q3 不能外推；CFO 未拆解 Q4 隱含的演唱會 AOI 改善。基準 FY2027 營收成長 8.3%，略低於共識 8.6%。","evidence_level":"高：新聞稿與逐字稿。","settle_metric":"FY2026 演唱會 AOI 年增","if_then":["若 FY2026 演唱會 AOI 年增低於 10%，Bear 機率上調到 35%，不追。","反向條件：若 FY2027 開年事件遞延收入年增回到 15% 以上，Bull 機率上調 3 個百分點。"]},{"axis":"共識每股盈餘方向","cause":null,"prior_field":null,"side_a":"近 3 個月 FY1 修正顯示 +4.55%，字面像上修。","side_b":"實際是虧損由 0.44 美元擴大到 0.46 美元；Q1 財報後一個月共識曾下修 36%。","ruling":"讀為小幅下修。+4.55% 的正負號被負分母反轉，不作動能證據。36% 下修建立在接近零的基期且來自轉載站，只保留方向。","evidence_level":"低：快照可能尚未反映 Q3 財報。","settle_metric":"Q3 財報後首份完整共識快照","if_then":["若下一份快照 FY2027E 每股盈餘下修超過 10%，視為訴訟成本尚未計入，不追。"],"evidence_refs":["capital_markets_pricing#1"]},{"axis":"訴訟費用是否一次性","cause":null,"prior_field":null,"side_a":"Q3 AOI 11.79 億美元，管理層以 AOI 呈現本業。","side_b":"前 9 月營業利益減少 3.505 億美元，主因政府調查與訴訟；FY2026E 每股盈餘為負。","ruling":"未證、監測。不採信也不否定一次性歸因，州方賠償與 FTC 訴訟都還沒落地。","evidence_level":"高：10-Q。","settle_metric":"FY2027 政府調查與訴訟費用","if_then":["若 FY2027 這項費用仍超過 1 億美元，一次性歸因不成立，情境改用含訴訟成本的利潤率，不追。"],"evidence_refs":["capital_markets_pricing#4"]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"全年粉絲近 1.8 億，2027 預付廣告雙位數成長，Harry Styles、Bruno Mars、Oasis、Metallica 已開賣，票務財測上修；賣方 20 買 3 持有 2 賣，均值目標 202 美元，投資人日就在下週。","side_b":"基準五年年化約 6%，救濟未定，Bear 情境 −41%。","ruling":"不買。最強論證成立在需求，不成立在價格。","evidence_level":"中","settle_metric":"股價相對 150 美元、救濟裁定","if_then":["若股價先漲到 215 美元以上而證據未到，不追。","若股價跌到 150 美元以下且未見剝離命令，重跑研究，通過後分批反買。"]},{"axis":"產業態勢三軸","cause":null,"prior_field":null,"side_a":"競爭軸：10-K 稱自助售票競爭增加，Eventim 擴張美國；今年新增淨客戶票量逾 2,000 萬張，暫未見惡化。結構軸：live 需求持久，場館管線 25 座以上。","side_b":"其他軸：反壟斷改變票務合約規則，獨家年限、系統開放與費用都在變動。","ruling":"裁決為其他結構變動中，指反壟斷這一軸。","evidence_level":"中","settle_metric":"救濟裁定與票務續約年限","if_then":["若票務 AOI 利潤率連 2 季低於 32%，改判競爭惡化中，減碼。"],"evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#3"]},{"axis":"前份空白欄位","cause":"方法變動","prior_field":["moat_trend","runway_post_y5","archetype","cycle_position","p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份這些欄位都是空值。","side_b":"本次依新格式補上：護城河方向穩定、跑道中等、以品質複利成長為主、情境機率 22／48／30、最大回撤 −35% 至 −55%。","ruling":"前份沒有對照值，不算立場變動。","evidence_level":"高"},{"axis":"估值結論","cause":"方法變動","prior_field":["val"],"side_a":"前份以 PEG 2.6 加五年 80% 分位判為最貴一級。","side_b":"FY2026E 共識每股盈餘為負，PEG 無法算，五年分位也缺資料，改用 EV/S 與情境報酬，判為偏貴。","ruling":"股價只比前份高 3.8%，沒有變便宜，結論變動來自尺度更換。","evidence_level":"中"},{"axis":"評級與價值陷阱判斷","cause":"新證據","prior_field":["signal","trap"],"side_a":"前份評級 B，價值陷阱中度。","side_b":"本次評級與價值陷阱判斷都不變。","ruling":"新證據往兩邊走：Q3 票務與粉絲上修支持論點，救濟仍未定，兩者相抵。","evidence_level":"中"},{"axis":"重啟條件","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"前份未設重啟條件，裁決句只寫等 5 或裁決明朗化，數字在前份已缺損。","side_b":"股價≤150 美元，且法院未命令剝離 Ticketmaster；兩者同時成立才重跑研究。","ruling":"本次改成具體價格加事件；法院命令剝離則清倉，不適用重啟。","evidence_level":"中"},{"axis":"Single Thing 唯一致命點","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份唯一致命點為空。","side_b":"法院最終救濟命令 Live Nation 剝離 Ticketmaster。","ruling":"Single Thing 由前份第一項風險的分拆部分收斂而來，發生即清倉。","evidence_level":"中"},{"axis":"第一項風險門檻（減碼改清倉）","cause":"新證據","prior_field":["R1"],"side_a":"若 remedy 包含「強制業務分拆」或「強制資產出售」中任一 → R1 觸發 → 立即減倉 2/3","side_b":"法院命令剝離 Ticketmaster 即清倉；DOJ 和解的至多 13 座圓形劇場剝離不觸發減碼，改看票務 AOI 利潤率連 2 季低於 32%。","ruling":"舊文字會被和解的圓形劇場剝離碰到，但該條款是協議、仍待 Tunney Act 核准且規模有限，所以把資產出售拆開，分拆門檻提高到清倉。","evidence_level":"中","evidence_refs":["regulatory_antitrust#1"]},{"axis":"估值回歸門檻（減碼）","cause":"方法變動","prior_field":["R3"],"side_a":"5Y NTM PE 分位 > 90% 持續 4 週 或 同業 PE 收斂 +20% → R3 已實現","side_b":"前瞻 EV/S 高於 1.9 倍（股價約 215 美元）且救濟與場館報酬都沒有新證據，持有者減碼，未持有者不追。","ruling":"每股盈餘為負，NTM 本益比分位失去意義，舊門檻退休，改用 EV/S。","evidence_level":"中"}],"triggers":[{"n":1,"text":"股價回到 150 美元以下，且法院沒有命令剝離 Ticketmaster，重跑研究。","type":"估值rearm","maps_to":"H1","metric":"股價與救濟裁定","threshold":"≤150 美元且無剝離命令","action":"重跑研究，通過後分批反買","source_freq":"每日股價；法院文件不定期","date":null},{"n":2,"text":"法院最終救濟命令剝離 Ticketmaster。","type":"Single Thing","maps_to":"R1","metric":"救濟裁定","threshold":"裁定含剝離","action":"清倉，重跑研究","source_freq":"法院文件、10-Q 法律附註","date":null,"evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#2","major_events#0"]},{"n":3,"text":"投資人日揭露場館投資報酬與夥伴出資比例。","type":"假設驗證","maps_to":"H2","metric":"場館投資報酬、2027 資本支出","threshold":"投資報酬低於 12%，或 2027 資本支出超過 14 億美元","action":"不追；Bear 機率上調到 35% 並更新情境","source_freq":"投資人日簡報","date":"2026-11"},{"n":4,"text":"FY2026 演唱會 AOI 未達雙位數成長。","type":"風險","maps_to":"R3","metric":"FY2026 演唱會 AOI 年增","threshold":"低於 10%","action":"不追","source_freq":"Q4 財報","date":"2027-02"},{"n":5,"text":"票務 AOI 利潤率連 2 季低於 32%。","type":"減碼","maps_to":"R2","metric":"票務 AOI 利潤率","threshold":"連 2 季低於 32%","action":"減碼，未持有者不追","source_freq":"每季分部資料","date":null,"evidence_refs":["channel_business_model_shift#0","channel_business_model_shift#1"]},{"n":6,"text":"前瞻 EV/S 高於 1.9 倍，而救濟與場館報酬都沒有新證據。","type":"減碼","maps_to":"R6","metric":"前瞻 EV/S","threshold":"高於 1.9 倍（股價約 215 美元）","action":"減碼，未持有者不追","source_freq":"每日","date":null},{"n":7,"text":"FTC 訴訟、州方賠償與和解累計現金超過 Bear 假設。","type":"風險","maps_to":"R5","metric":"累計現金賠償","threshold":"超過 10 億美元","action":"停止加碼","source_freq":"10-Q 法律附註","date":null,"evidence_refs":["major_events#1","lawsuit_class_action#1","lawsuit_class_action#2"]},{"n":8,"text":"Q4 財報後複審。","type":"複審日期","maps_to":"H2","metric":"全年粉絲、演唱會 AOI、事件遞延收入","threshold":"定期複審","action":"更新情境與機率","source_freq":"Q4 財報","date":"2027-02"}],"kill_metrics":[{"metric":"法院是否命令剝離 Ticketmaster","bear_threshold":"裁定含剝離","window":"2028 年底前","source":"法院文件、10-Q 法律附註","last_status":"unknown"},{"metric":"票務 AOI 利潤率","bear_threshold":"連 2 季低於 32%","window":"每季","source":"季報分部資料","last_status":"ok"},{"metric":"演唱會 AOI 利潤率","bear_threshold":"連 2 季低於 2.5%","window":"每季","source":"季報分部資料；事實表未涵蓋，資料缺口","last_status":"unknown"},{"metric":"集團 AOI 年增","bear_threshold":"全年低於 8%","window":"FY2027","source":"年度財報；事實表只有 Q3 單季 AOI，資料缺口","last_status":"unknown"},{"metric":"全年粉絲年增","bear_threshold":"低於 5%","window":"FY2027","source":"季報與新聞稿","last_status":"ok"},{"metric":"事件遞延收入年增","bear_threshold":"連 2 季年減","window":"每季","source":"新聞稿","last_status":"ok"},{"metric":"FCF 利潤率","bear_threshold":"全年低於 3%","window":"FY2027","source":"年度財報","last_status":"ok"}],"evidence_dismissed":[],"action_conditions":{"rearm_trigger":"股價≤150 美元，且法院未命令剝離 Ticketmaster；兩者同時成立才重跑研究。","exec_line":"現在不建倉。股價先漲而證據未到就不追；跌到 150 美元以下且基本面無損，重跑研究，通過後分批買進；法院命令剝離則清倉。"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":true,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等股價≤150 美元，且法院未命令剝離 Ticketmaster。150 美元對應基準五年年化約 9.7%，也接近 104 週均線 152.64 美元。"},"thesis":{"H":[{"id":"H1","text":"反壟斷以行為救濟收場，Ticketmaster 留在集團。","2y":"2028 年底前最終救濟不含剝離；票務 AOI 利潤率不低於 32%（Q3 2026 約 36%，由反推營收算出）。","5y":"上訴結束後票務仍在集團，FY2031 票務 AOI 五年年複合不低於 5%。","10y":null,"threshold":"不含剝離；票務 AOI 利潤率不低於 32%；集團 AOI 年增不低於 8%。","source":"法院文件、10-Q 法律附註、季度分部資料。","drift_rule":"票務 AOI 利潤率 TTM 低於門檻 5% 連 2 季為削弱，低於 10% 連 3 季為反轉；裁定含剝離直接反轉。"},{"id":"H2","text":"粉絲與場館管線延續，自營場館提高每位粉絲的利潤，並轉成現金。","2y":"FY2028 粉絲不低於 2 億、自營場館粉絲不低於 9,000 萬（2026 約 7,500 萬）；FCF 利潤率不低於 4%。","5y":"FY2031 粉絲不低於 2.35 億，營收不低於 416 億美元。","10y":null,"threshold":"FY2028 粉絲 2 億、自營 9,000 萬、FCF 利潤率 4%。","source":"季報、新聞稿、投資人日簡報。","drift_rule":"粉絲或 FCF 利潤率 TTM 低於路徑 5% 連 2 季為削弱，低於 10% 連 3 季為反轉。"},{"id":"H3","text":"贊助與票務兩個高利潤段持續成長。","2y":"FY2028 贊助 AOI 兩年年複合不低於 10%，票務 AOI 兩年年複合不低於 5%（已吸收費用上限）。","5y":"FY2031 贊助 AOI 五年年複合不低於 10%。","10y":null,"threshold":"贊助 AOI 年複合 10%；票務 AOI 年複合 5%。","source":"季度分部資料。","drift_rule":"TTM 成長低於門檻 5% 連 2 季為削弱，低於 10% 連 3 季為反轉。"}],"R":[{"id":"R1","text":"法院命令剝離 Ticketmaster，票務與演唱會的交叉導流斷開。","h_ref":"H1","clock":"🔥","threshold":"裁定含剝離即清倉。屬民事案件，受影響的票務 Q3 營收約 8.8 億美元；裁定日期未知。","evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#1","regulatory_antitrust#2","major_events#0","lawsuit_class_action#0","competitive_share_entrants#2","end_markets#3"]},{"id":"R2","text":"行為救濟逐年侵蝕：獨家年限縮短、系統開放、費用上限，加上自助售票與新對手。","h_ref":"H1","clock":"🐢","threshold":"票務 AOI 利潤率連 2 季低於 32%，或新增淨客戶票量轉負。","evidence_refs":["channel_business_model_shift#0","channel_business_model_shift#1","competitive_share_entrants#0","competitive_share_entrants#1","competitive_share_entrants#3","substitute_technology#0"]},{"id":"R3","text":"Q4 演唱會 AOI 未兌現全年雙位數成長，2026 檔期紅利在 2027 回落。","h_ref":"H2","clock":"⚡","threshold":"FY2026 演唱會 AOI 年增低於 10%；FY2027 粉絲年增低於 5%。"},{"id":"R4","text":"場館資本支出報酬不達標；CFO 2026-07-30 說效益要到 2028 年，夥伴出資與投資報酬尚未揭露。","h_ref":"H2","clock":"🔥","threshold":"場館投資報酬低於 12%，或 FY2027 FCF 利潤率低於 3%。"},{"id":"R5","text":"FTC 與七州消費者保護訴訟、證券集體訴訟與州方賠償持續消耗現金。","h_ref":"H1","clock":"🔥","threshold":"累計現金賠償超過 10 億美元。","evidence_refs":["major_events#1","lawsuit_class_action#1","lawsuit_class_action#2"]},{"id":"R6","text":"倍數回落：EV/S 位於四個年度端點最高，每股盈餘基期被壓低。","h_ref":"H3","clock":"🔥","threshold":"前瞻 EV/S 高於 1.9 倍且無新證據時減碼；低於 1.3 倍且基本面無損時重跑研究。"}],"single_thing":{"description":"法院最終救濟命令 Live Nation 剝離 Ticketmaster。","why_fatal":"Q3 票務 AOI 占合併 27%，票務也是飛輪的連接點；基準與 Bull 都以票務留在集團為前提，終端 EV/S 每 0.1 倍約 17 美元，是情境中最大的敏感項。","if_happens":"清倉，現有三情境作廢，分拆後兩家公司重跑研究。","how_monitor":"法院救濟程序、JMOL 與上訴、Tunney Act 核准、10-Q 法律附註。","probability":"12 至 24 個月內約 15% 至 20%；事實表法律進度只到約 2026-05，這個機率信心低。"}},"appendix_a":{"growth_durability":6,"quality_score":6,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":92.2,"peg_fy2":1.75,"stress":{"pass":null,"total":null}},"eps_meta":{"base_eps_path":{"FY2025A":-0.24,"FY2026E":-0.46,"FY2027E":1.9,"FY2028E":2.9},"fy_end_month":12,"eps_basis":"FY2025A 為年度財報稀釋每股盈餘；FY2026E 至 FY2028E 為 Koyfin 2026-11-07 共識，事實表未標明 GAAP 或調整後，數值方向與 GAAP 接近。"},"catalysts":[{"date":"2026-11","date_precision":"month","type":"guidance","event":"投資人日，管理層承諾說明場館時程、資本支出與夥伴出資、AI 影響","impact":"高","watch":"場館投資報酬、2027 資本支出、開幕前費用"},{"date":null,"date_precision":null,"type":"regulatory","event":"法院對州方案的救濟裁定與 JMOL 結果","impact":"高","watch":"是否含剝離 Ticketmaster、獨家年限、賠償金額"},{"date":null,"date_precision":null,"type":"regulatory","event":"DOJ 和解的 Tunney Act 核准","impact":"中","watch":"圓形劇場剝離座數、費用上限範圍"},{"date":"2027-02","date_precision":"month","type":"guidance","event":"FY2026 Q4 財報","impact":"中","watch":"演唱會 AOI 是否雙位數成長、事件遞延收入"}],"decision_out":{"verdict":"迴避","role":"不持有","row_hit":"2","pacing":[],"holding_cap":null,"audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":true,"basis":"thesis_irreconcilable=True"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]}],"requires_critic":[]}}
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
