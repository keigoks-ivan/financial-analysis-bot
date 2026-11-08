你是 DD 管線 v20 的判斷層閘（gate），標的 SHOP（20261108）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（46 條）
- `f_kpi0_gaap`（q1_business）｜營收（GAAP）＝3742 百萬美元｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-11-03）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0001594805/000159480526000067/exhibit991pressreleaseq320.htm（numbers.latest_quarter_kpis.items[0]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-11-03））
  - 註記：未取得
- `f_kpi1_non_gaap_gaap_149`（q1_business）｜Non-GAAP 營業利益（新聞稿未單列，GAAP 營業利益＋調整項 149 自算）＝717 百萬美元（利益率約19.2%）｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-11-03）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 8-K Ex.99.1；717＝568＋149 為自算，非公司揭露（numbers.latest_quarter_kpis.items[1]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-11-03））
  - 註記：未取得
- `f_kpi2_gaap`（q1_business）｜GAAP 營業利益＝568 百萬美元（利益率15.2%，自算）｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-11-03）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 8-K Ex.99.1（numbers.latest_quarter_kpis.items[2]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-11-03））
  - 註記：未取得
- `f_kpi6_gmv`（q1_business）｜GMV＝119145 百萬美元（YoY +29%，固定匯率+30%）｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-11-03）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 8-K Ex.99.1（numbers.latest_quarter_kpis.items[6]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-11-03））
  - 註記：未取得
- `f_kpi7_mrr`（q1_business）｜MRR＝230 百萬美元｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-11-03）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 8-K Ex.99.1（numbers.latest_quarter_kpis.items[7]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-11-03））
  - 註記：未取得
- `f_kpi5_q4_fy2026`（q1_business）｜管理層指引（Q4 FY2026）＝營收年增低30%段；毛利金額年增高20%段；營業費用占營收29%–30%；SBC 155百萬美元；FCF 利益率與2025Q4相當 文字區間｜期間與口徑：Q3 FY2026（公告於 2026-11-03）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司新聞稿 8-K Ex.99.1（numbers.latest_quarter_kpis.items[5]，as_of Q3 FY2026（公告於 2026-11-03））
  - 註記：未取得
- `f_peer_shop_gross_margin_pct`（q2_moat）｜SHOP 毛利率＝47.49 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.SHOP.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_shop_operating_margin_pct`（q2_moat）｜SHOP 營業利益率＝18.07 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.SHOP.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_shop_fcf_margin_pct`（q2_moat）｜SHOP FCF 利潤率＝18.08 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.SHOP.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_wix_gross_margin_pct`（q2_moat）｜WIX 毛利率＝66.64 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.WIX.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_wix_operating_margin_pct`（q2_moat）｜WIX 營業利益率＝-8.5 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.WIX.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_wix_fcf_margin_pct`（q2_moat）｜WIX FCF 利潤率＝19.24 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.WIX.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_amzn_operating_margin_pct`（q2_moat）｜AMZN 營業利益率＝12.89 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.AMZN.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_amzn_fcf_margin_pct`（q2_moat）｜AMZN FCF 利潤率＝-6.38 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.AMZN.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_gddy_operating_margin_pct`（q2_moat）｜GDDY 營業利益率＝26.05 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.GDDY.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_gddy_fcf_margin_pct`（q2_moat）｜GDDY FCF 利潤率＝33.66 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.GDDY.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_kpi4_sbc_gaap`（q4_capital）｜SBC（含相關稅）占 GAAP 營業利益＝25.9 %（SBC 及相關稅147；占營收約3.9%；現金流量表 SBC 140）｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-11-03）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 8-K Ex.99.1；比率自算（numbers.latest_quarter_kpis.items[4]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-11-03））
  - 註記：不適用
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝1.89 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-11-07）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝2.44 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-11-07）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝3.17 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-11-07）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝15314.83 USD m｜期間與口徑：2026-11-08／yfinance revenue_estimate 0y 平均（44 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝19374.41 USD m｜期間與口徑：2026-11-08／yfinance revenue_estimate +1y 平均（51 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi3_fcf`（q4_capital）｜自由現金流（FCF）＝816 百萬美元（FCF 利益率22%）｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-11-03）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 8-K Ex.99.1（numbers.latest_quarter_kpis.items[3]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-11-03））
  - 註記：未取得
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝-4539.0 USD m｜期間與口徑：2026-11-08／yfinance 最新一季：總債務 188.0、現金 4727.0（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝1286.52 m shares｜期間與口徑：2026-11-08／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝148.91 USD｜期間與口徑：2026-11-06（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-11-06（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝78.79 x｜期間與口徑：2026-11-07／分母＝FY1 EPS 1.89，分子＝快照價 148.91｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-11-07）
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝91.36 x｜期間與口徑：2026-11-06（RTH 收盤，UTC）／3 個年度端點內的分位＝3.2｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-11-06（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝3.2 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 3 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝13.52 x｜期間與口徑：2026-11-06（RTH 收盤，UTC）／4 個年度端點內的分位＝55.2｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝55.2 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝13.2 x｜期間與口徑：2026-11-06（RTH 收盤，UTC）／4 個年度端點內的分位＝52.7｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝52.7 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ev_s_fwd`（q5_valuation）｜EV/S（EV ÷ FY1 共識營收）＝12.21 x｜期間與口徑：2026-11-08／f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）｜kind：estimate
  - 來源：—（numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_ev_m`（q5_valuation）｜目前企業價值 EV（市值＋淨負債）＝187037.0 USD m｜期間與口徑：2026-11-08／市值 191576.0 ＋ 淨負債 -4539.0｜kind：realized
  - 來源：—（numbers.capital_structure.ev_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_consensus_rev_fy1_pct`（q5_valuation）｜FY1 共識修正＝0.0 %｜期間與口徑：2026-11-07／兩份 Koyfin 快照之間的 EPS 修正幅度（1.89 → 1.89）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.fy1.revision_pct，as_of 2026-11-07）
- `f_consensus_rev_fy2_pct`（q5_valuation）｜FY2 共識修正＝-0.41 %｜期間與口徑：2026-11-07／兩份 Koyfin 快照之間的 EPS 修正幅度（2.45 → 2.44）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.fy2.revision_pct，as_of 2026-11-07）
- `f_consensus_rev_fy3_pct`（q5_valuation）｜FY3 共識修正＝-0.63 %｜期間與口徑：2026-11-07／兩份 Koyfin 快照之間的 EPS 修正幅度（3.19 → 3.17）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.fy3.revision_pct，as_of 2026-11-07）
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝-0.53 %｜期間與口徑：2026-08-13 → 2026-11-07／FY1 共識 EPS 1.9 → 1.89（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-11-07）
- `f_rsi14`（q5_valuation）｜RSI(14)＝42.76｜期間與口徑：2026-11-06（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-11-06（RTH 收盤，UTC））
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝34.87 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ma_state`（q5_valuation）｜週線均線六態（decision_inputs.ma 必須等於此值）＝🟡｜期間與口徑：2026-11-08／timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）
  - 原文：「price 148.91 / W52 135.07 / W104 127.21 / W250 86.4 / W250 13週斜率 0.91%」
- `f_ma_w52`（q5_valuation）｜52 週均線＝135.07 USD｜期間與口徑：2026-11-08／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）
- `f_ma_w104`（q5_valuation）｜104 週均線＝127.21 USD｜期間與口徑：2026-11-08／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）
- `f_ma_w250`（q5_valuation）｜250 週均線＝86.4 USD｜期間與口徑：2026-11-08／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）
- `f_ma_slope_w250_pct`（q5_valuation）｜W250 13 週斜率＝0.91 %｜期間與口徑：2026-11-08／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）

### findings_digest 中方向為負或來源衝突的條目（12 條）
- `competitive_share_entrants#1`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K 風險因子：對手有更長歷史、更大客群與資源，可能以更積極定價或整合競爭平台；定價決策可能導致失去市占。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-11）｜affects：thesis.R、decision_inputs.bear
- `competitive_share_entrants#3`（competitive_share_entrants｜方向 -｜狀態 ok）：評論稱 AI 平台（OpenAI／Google）若接管結帳，Shopify 商家關係護城河可能受挑戰；OpenAI 於 2026-03 撤下 ChatGPT Instant Checkout。
  - 來源：fudge.ai State of Shopify AI 2026（as_of 2026-06-24）｜affects：moat_trend、decision_inputs.bear
- `regulatory_antitrust#0`（regulatory_antitrust｜方向 -｜狀態 ok）：Sezzle 私人反壟斷訴訟（D. Minn. 25-cv-2395）：2026-05 法院部分駁回 Shopify 撤案動議，Sherman Act 第 2 條壟斷與意圖壟斷主張繼續審理，搭售主張無損害駁回；非責任認定。
  - 來源：Sezzle 新聞稿轉載 / Finviz：Sezzle Provides Update on Antitrust Case Against Shopify（as_of 2026-05-12）｜affects：thesis.R、decision_inputs.bear、moat_trend
- `regulatory_antitrust#2`（regulatory_antitrust｜方向 -｜狀態 ok）：Sezzle 反壟斷案獲法官准許核心壟斷主張進入審理
  - 來源：Shopifreaks（as_of 2026-05-13）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：10-K 風險因子：Shopify 的中小商家客戶易受關稅、進出口許可與管制要求等貿易保護措施影響，進而可能衝擊 Shopify 業務（間接暴露，非自身供應鏈）
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-11）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#1`（reg_tariff_export｜方向 -｜狀態 ok）：10-K 提及關稅等總經因素過去已影響買家信心與消費，可能使商家倒閉或停用服務、減少平台交易量
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-11）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：FY2025 10-K risk factors cite reliance on third parties for key services including cloud hosting and Shopify Payments
  - 來源：SEC EDGAR Shopify Form 10-K FY2025（as_of 2026-02-12）｜affects：thesis.R、decision_inputs.bear
- `substitute_technology#1`（substitute_technology｜方向 -｜狀態 ok）：10-K 風險因子：大型科技平台可能整合競爭功能或限制第三方存取其用戶資料，影響商家行銷與銷售及平台需求。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-11）｜affects：moat_trend、decision_inputs.bear
- `substitute_technology#2`（substitute_technology｜方向 -｜狀態 ok）：Baillie Gifford 評論：AI 代理接手搜尋比較購買時，靠發現與客戶旅程變現的平台面臨被顛覆風險，對他者則是機會。
  - 來源：Baillie Gifford Monthly commentary 2026 Q1（as_of 2026-04-01）｜affects：moat_trend、decision_inputs.bear
- `major_events#1`（major_events｜方向 -｜狀態 ok）：加州聯邦法官駁回 Shopify 對 Briskin v. Shopify（結帳頁蒐集個資的消費者集體訴訟）的駁回動議，案件續行。
  - 來源：Top Class Actions，Shopify class action lawsuit survives motion to dismiss（as_of 2026-08-17）｜affects：decision_inputs.bear、thesis.R
- `lawsuit_class_action#0`（lawsuit_class_action｜方向 -｜狀態 ok）：Briskin v. Shopify（N.D. Cal., 21-cv-06269）隱私集體訴訟經駁回動議後續行；未查到 2026 年證券詐欺集體訴訟。
  - 來源：Top Class Actions（as_of 2026-08-17）｜affects：decision_inputs.bear、thesis.R
- `lawsuit_class_action#1`（lawsuit_class_action｜方向 -｜狀態 ok）：FY2025 10-K 風險因素稱 CIPA／CCPA 允許集體訴訟，且訴訟數量與重要性隨規模增加。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-11）｜affects：thesis.R

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 2 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/SHOP_20261108/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":296.4,"bear_5y_price":52.8,"p_bull_pct":25,"p_bear_pct":30,"upside_5y_pct":17.9,"ev5y_pct":13.4,"irr_base_pct":3.3,"asym_ratio":1.3,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":1.89,"pe":78.79,"basis":"FY2026E 共識 EPS（FY1），現價 148.91 美元；終端倍數同樣用當年度 EPS。"},"eps":{"bull":[2.55,3.5,4.7,6.15,7.8],"base":[2.44,3.17,4.0,4.9,5.85],"bear":[2.15,2.25,2.32,2.36,2.4]},"pe":{"bull":38,"base":30,"bear":22},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0,"net_buyback":0},"second_stage":{"bull_cagr_pct":18,"base_cagr_pct":13},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### SHOP_Q2_2026_Earnings_Call_20260805.md
- 2026-08-05｜CFO｜guidance：CFO 給 Q3 營收年增低 30 幾%（原話："We expect Q3 revenue growth in the low 30s year-over-year."）
- 2026-08-05｜CFO｜guidance：CFO 給 Q3 毛利金額年增中高 20%（原話："gross profit dollars to grow in the mid- to high 20s"）
- 2026-08-05｜CFO｜guidance：CFO 給 Q3 營業費用占營收 33%–34%，並對照去年 Q3 的 37%（原話："operating expenses in Q3 to be 33% to 34% of revenue"）
- 2026-08-05｜CFO｜guidance：CFO 給 Q3 自由現金流率區間，含不到 1 點商業預支款會計變更的順風（原話："cash flow margin to be in the high teens to low 20s"）
- 2026-08-05｜CFO｜guidance：CFO 表示 Q3 無重大匯率影響（原話："We do not expect any significant FX impact."）
- 2026-08-05｜CFO｜margin：Q2 營業費用占營收 34%，較去年同期改善近 4 點（原話："operating expenses, which were 34% of revenue"）
- 2026-08-05｜CFO｜margin：Q2 自由現金流率略高於 18%，高於先前展望（原話："our Q2 free cash flow margin was just over 18%"）
- 2026-08-05｜CFO｜margin：排除商業預支款會計變更後，自由現金流率年增約 1.5 點（原話："roughly 1.5 points of year-over-year margin expansion"）
- 2026-08-05｜CFO｜margin：商家解決方案毛利率微幅高於去年，支付量增加的壓力被高毛利收入抵銷（原話："Margin pressure from increased payments volume"）
- 2026-08-05｜CFO｜margin：國際市場支付毛利率通常較高，理由是簽帳卡比例高、交換費低（原話："payments gross margins are generally higher in international"）
- 2026-08-05｜CFO｜margin：訂閱解決方案毛利率略低於 80%，與 Q1 持平；Sidekick 的 AI 成本多數落在此處（原話："gross margins just under 80%"）
- 2026-08-05｜CFO｜margin：Sidekick 使用量放大的同時，訂閱毛利率季對季維持相近水準（原話："hold gross margins at a relatively consistent level"）
- 2026-08-05｜CFO｜margin：銷售與行銷費用占營收低於 14%，年減約 160 基點（原話："Sales and marketing in Q2 was less than 14% of revenue"）
- 2026-08-05｜CFO｜margin：內部 AI 支出多數歸在研發費用（原話："the majority of our internal AI spend is allocated here"）
- 2026-08-05｜CFO｜margin：交易貸款與損失占營收 3.9%，Capital 為本季較大推手（原話："Transaction loans and losses came in at 3.9% of revenue."）
- 2026-08-05｜CFO｜margin：支付與信貸損失率處於正常水準，Capital 為較大推手（原話："Capital was a larger driver this quarter"）
- 2026-08-05｜CFO｜commitment：CFO 重申毛利率若承壓，會以營業費用成效超額抵銷（原話："any pressure we see on gross margin, we'll more than"）
- 2026-08-05｜CFO｜commitment：CFO 表示 AI 策略為最大槓桿搭配成本管理（原話："Maximum leverage paired with thoughtful cost"）
- 2026-08-05｜President｜commitment：Harley 表示代理式交易沿用與網店交易相同的經濟模型，無新增費用（原話："There's no new fees. There's no separate pricing."）
- 2026-08-05｜President｜commitment：被問 Sidekick 是否直接收費時，管理層保留彈性、未承諾（原話："we reserve the right to wake up smarter every single day"）
- 2026-08-05｜CFO｜commitment：R&D 持續維持費用紀律（原話："we'll continue to be disciplined in managing the spend."）
- 2026-08-05｜CFO｜product：Q2 營收年增 34%，超出預期（原話："Q2 revenue grew 34% or 33% on a constant currency basis"）
- 2026-08-05｜CFO｜product：支付滲透率年增 3 點至 68%（原話："payments penetration, which grew 3 points year-over-year"）
- 2026-08-05｜CFO｜product：Shop Pay GMV 年增 53%（原話："Shop Pay GMV grew 53% year-over-year."）
- 2026-08-05｜CFO｜product：Q2 MRR 年增 19%（原話："Q2 MRR grew 19% year-over-year"）
- 2026-08-05｜President｜product：Sidekick 日活躍商家年增 3.6 倍（Q&A 中同一指標講成 3x）（原話："daily active merchants using Sidekick were up 3.6x"）
- 2026-08-05｜President｜product：Sidekick 建立自訂應用數從 Q1 的 12,000 增至 36,000（原話："36,000 custom apps, up from 12,000 in Q1."）
- 2026-08-05｜President｜product：Catalog 驅動的 AI 搜尋轉換率為爬取資料的兩倍（原話："AI searches powered by Catalog converted twice the rate"）
- 2026-08-05｜President｜product：Shop app 自有 GMV 年增逾 70%（原話："Shop app's native GMV grew over 70%"）
- 2026-08-05｜President｜product：內部使用蒸餾模型，大模型教小模型處理特定任務（原話："we now have a number of distilled models"）
- 2026-08-05｜President｜competition：代理式流量與訂單年增三倍（原話："AI-driven traffic and also orders to Shopify stores tripled"）
- 2026-08-05｜President｜competition：傳統搜尋工作階段仍在成長，管理層稱 AI 為搜尋的補充（原話："AI as a complement to search rather than a substitute"）
- 2026-08-05｜President｜competition：管理層回應上季關於代理式是否取代搜尋的疑問，稱搜尋成長良好（原話："but search is growing incredibly well"）
- 2026-08-05｜President｜competition：OpenAI、Google、Meta、Microsoft 為合作夥伴（原話："like OpenAI, Google, Meta, and Microsoft, have"）
- 2026-08-05｜President｜competition：AI 歸因訂單 75% 來自前 100 大品類之外（原話："with 75% of AI-attributed orders in the second quarter"）
- 2026-08-05｜CFO｜competition：CFO 引用 eMarketer，稱 Shopify 商家取得美國電商增量近半（原話："Shopify merchants have captured nearly half of all"）
- 2026-08-05｜CFO｜competition：CFO 將電商加速或長尾價值視為基本情境之外的上行因素（原話："is upside to our underlying growth story"）
- 2026-08-05｜CFO｜customer：$25M 以上級距成長最快，基期較小（原話："The $25 million in greater band is the fastest-growing"）
- 2026-08-05｜CFO｜customer：各區域固定匯率 GMV 成長：北美 28%、歐洲 34%（原話："North America GMV grew 28%, and Europe grew 34%"）
- 2026-08-05｜CFO｜customer：線下 GMV 年增 32%、B2B GMV 年增 76%（原話："Offline GMV was up 32%. B2B GMV grew 76%"）
- 2026-08-05｜CFO｜customer：年 GMV 達 100 萬美元的商家五年留存率 92%（原話："$1 million in annual GMV had a 92% retention"）
- 2026-08-05｜President｜customer：大型複雜零售商為成長最快的區塊（原話："particularly strong momentum with large complex retailers"）
- 2026-08-05｜President｜customer：國際 GMV 年增 37%（原話："International GMV grew 37% in the quarter"）
- 2026-08-05｜President｜customer：Harley 稱較大商家選擇 Shopify 的速度加快（原話："Larger merchants are now choosing"）
- 2026-08-05｜President｜customer：Harley 稱全球零售銷售占比不到 1%，國際市場滲透不足（原話："I think we've captured less than 1% of global retail sales."）
- 2026-08-05｜President｜risk：Harley 承認少數商業模式目前不適合完整遷移（原話："There are some merchants that just"）
- 2026-08-05｜President｜risk：Harley 強調代理式量體相對 GMV 仍小、仍屬早期（原話："Look, it is early and"）
- 2026-08-05｜CFO｜capital_allocation：營運槓桿提供持續投資平台與內部 AI 能力的彈性（原話："This operating leverage provides the financial flexibility"）

### 問答異常語氣（迴避／改口／保留）
- SHOP_Q2_2026_Earnings_Call_20260805.md｜問：CIBC 問自由現金流率約 20% 是否為新常態、槓桿來自哪裡｜答法：CFO 不正面回答是否為新常態，改指向 Q3 財測並說持續創造槓桿
- SHOP_Q2_2026_Earnings_Call_20260805.md｜問：Morgan Stanley 問 Sidekick 對留存、GMV 成長、產品附加率的數據，以及未來是間接或直接變現｜答法：Harley 未提供留存／GMV／附加率數字，改談使用量與案例；變現部分只說保留彈性、模式建立在商家成功上

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 4 | 2 |
| customer_second_source | not_applicable | 0 | 0 |
| customer_concentration_credit | found | 2 | 1 |
| supply_demand_durability | found | 2 | 2 |
| regulatory_antitrust | found | 3 | 3 |
| reg_tariff_export | found | 4 | 1 |
| geo_supply_chain | found | 1 | 2 |
| end_markets | found | 5 | 4 |
| substitute_technology | found | 3 | 1 |
| channel_business_model_shift | found | 5 | 2 |
| capital_markets_pricing | found | 2 | 2 |
| major_events | found | 3 | 3 |

未涵蓋／不適用軸的查詢詞原文（供判相關性）：
- **customer_second_source**（not_applicable）：（無查詢記錄）

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260808","verdict":"觀望","role":"追蹤","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"US／全球電商份額持續擴大（跑道未走完，SHOP 是主要收割者之一）","columns":{"可證偽門檻":"US 份額 YoY 連 2 季不再上升；或 B2B GMV YoY 增速降至 &lt;40%","本次狀態":"成立：US 份額 14%（YoY +2pp）、B2B GMV +76%（101%→84%→76% 減速軌跡，證偽門檻＜40% 尚遠）、Q2'26 GMV +32%（連 5 季 &gt;30%）"}},{"id":"H2","text":"Take rate 持續擴張（monetization 是結構性的，非一次性）","columns":{"可證偽門檻":"Take rate 連 2 季 QoQ 不再上升；或 Payments 滲透率連 2 季不再上升","本次狀態":"成立：2.84%→3.05%→3.14% 軌跡向上；Payments 滲透 68.0%（YoY +3pp）"}},{"id":"H3","text":"現價已合理反映成長減速路徑（62× 不是為「維持今天成長率不變」定價）","columns":{"可證偽門檻":"FY+2 共識 EPS 上修 ≥33%（使 PEG 回落至 1.0）；或股價回檔 ≥20%","本次狀態":"不成立：目前無跡象顯示分母端會以此速度追上；此假設是本檔判觀望的直接原因"}}]},"R":{"status":"unavailable"},"single_thing":null,"kill_metrics":null,"rearm_trigger":"股價回檔至 $70–90 區間（$70≈PEG 1.0 對應 FY+1 共識成長 29.2%；上緣 $90 保留予國際 take rate 收斂槓桿〔Payments 僅covers~40國〕兌現空間）；或終端倍數假設站上同業現值上緣（NOW 28x）之後仍具正 EV；觸發後首階 1/3 分批建倉","irr_base_pct":-3.1,"ev5y_pct":-2.3,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"追蹤","signal":"B","val":"🔴","ma":"🟡","trap":"🟢","moat_trend":"↑","runway_post_y5":"🟢","asym_ratio":1.3,"ev5y_pct":-2.3,"irr_base_pct":-3.1,"max_dd_pct":-58.0,"bull_5y_price":243.8,"bear_5y_price":67.0,"p_bull_pct":30.0,"p_bear_pct":25.0,"rearm_trigger":"股價回檔至 $70–90 區間（$70≈PEG 1.0 對應 FY+1 共識成長 29.2%；上緣 $90 保留予國際 take rate 收斂槓桿〔Payments 僅covers~40國〕兌現空間）；或終端倍數假設站上同業現值上緣（NOW 28x）之後仍具正 EV；觸發後首階 1/3 分批建倉","price_at_dd":151.57,"archetype":"品質複利成長","cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"SHOP","date":"2026-11-08","schema":"v15.0","contract":"v19","company_name":"Shopify Inc."},"oneliner":"Shopify 商家拿走美國電商增量近半，GMV 年增 29.5%，護城河仍在變寬；但現價是 FY2026E 的 79 倍，EPS 五年複合 25% 加終端 30 倍也只換來年化約 3%，不追，等 110 美元以下或共識明顯上修。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/SHOP_20261108/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/SHOP_20261108/scenario.json","answers":{"q1_business":{"verdict":"賺商家成交額的抽成：每 100 美元 GMV 收 3.14 美元，78% 營收來自支付等商家解決方案，錢卡在結帳與支付節點。","reasoning":"Q3 FY2026 營收 37.42 億美元，年增 32%。商家解決方案 29.06 億美元，占 77.7%，年增 35%，自算毛利率 38.5%；訂閱解決方案 8.36 億美元，占 22.3%，年增 20%，毛利率 79%（2026-11-03 8-K 與法說）。整體毛利率 47.6%，GAAP 營益率 15.2%，自算非 GAAP 營益率 19.2%。GMV 1,191 億美元，支付滲透率 68%，年增 3 個百分點，所以成長先靠成交量，再靠支付附著。單點依賴有兩處，雲端代管與支付夥伴（FY2025 10-K 風險因子），集中度數字事實表未涵蓋；客戶端沒有集中，沒有單一商家曾超過營收 5%（FY2024 10-K）。供需判斷為結構性持久：Shopify 美國商家線上銷售三年年複合 23%，美國電商整體 8%（2026-11-03 Hoffmeister）。可能看錯的地方是這組數字由公司自行統計，而且商家解決方案會跟著消費循環走。","fact_refs":["f_kpi0_gaap","f_kpi1_non_gaap_gaap_149","f_kpi2_gaap","f_kpi6_gmv","f_kpi7_mrr","f_kpi5_q4_fy2026"],"verdict_values":{"revenue_quality":"訂閱占 22%，屬經常性；商家解決方案占 78%，屬交易型，隨 GMV 與消費循環波動。MRR 2.30 億美元，年增 19%，Plus 占 34%。","unit_econ_note":"商家解決方案毛利率約 38.5%，低於訂閱的 79%，支付占比上升會壓整體毛利率；但商家解決方案毛利金額年增 37%。","archetype":{"primary":"品質複利成長","secondary":null,"confidence":"高","fingerprint":"固定匯率 GMV 連六季約 30%，TTM FCF 利潤率約 18%，SBC 約占營收 3.9%，淨現金約 45 億美元。"},"industry":{"clock_phase":"II","sd_verdict_source":"結構性持久。全球電商 2026–2027 年增約 7.2%（二手彙整引 EMARKETER），Shopify GMV 增速約為其四倍，擴張來自份額轉移。","bargaining":{"up":"對支付夥伴有議價力，Q3 商家解決方案毛利率年增來自與支付生態夥伴談到的節省（2026-11-03 Hoffmeister）；雲端依賴第三方，集中度事實表未涵蓋。","down":"對中小商家定價有上限，追蹤站記錄 2026-10 年繳牌價上調後隔日回復，此後無持續性漲價。","geo":"固定匯率 GMV 北美年增 28%、歐洲 33%；國際 GMV 年增 32%，國際支付毛利率通常較高（2026-08-05 Hoffmeister）。"},"profit_pool_dir":"利潤池往結帳與支付層集中，AI 代理入口是新的爭奪者；五年營業利益池占比事實表未涵蓋。","tam_table":[{"item":"全球電商規模 2026 年","value":"約 6.88 兆美元，年增 7.2%（二手彙整引 EMARKETER，非一手）"},{"item":"全球電商規模 2027 年","value":"約 7.375 兆美元，各來源區間 7.1–8.0 兆"},{"item":"Shopify 占全球電商（粗算）","value":"Q3 GMV 1,191 億美元×4 約 4,766 億美元，約 6.9%；未做季節調整，屬自算"},{"item":"美國電商份額","value":"約 14%（公司自揭，Census 與內部 GMV 估計）"},{"item":"全球零售占比","value":"不到 1%（2026-08-05 Finkelstein）"},{"item":"五年營業利益池占比變化","value":"事實表未涵蓋"}]}}},"q2_moat":{"verdict":"護城河仍在變寬（↑）：商家份額持續上升，結帳與 Shop Pay 買家網路把商家和買家綁在同一層，但定價權只算穩定。","reasoning":"機制是統一商務作業系統加 Shop Pay 買家網路：商家換平台要重做線上店、門市、B2B、支付與平均 8 個應用程式的整合，買家端有 4 億名 Shop 與 Shop Pay 使用者。同業 ROIC 事實表未涵蓋，方向改用份額判斷：美國電商份額約 14%，2025 年以來拿走美國增量近半，三年前近五分之一，歐洲份額三年翻倍（2026-11-03 Hoffmeister）。執行面擴大：Lululemon 北美線上店導入 Shop Pay，門店數年增 52%，新導入 POS 的商家有 55% 是 Shopify 新客。定價權穩定：2026-08-05 Finkelstein 說代理式交易沒有新費用，牌價沒有持續上調，訂閱營收年增 20% 低於 GMV。同業利潤率對照不算突出，TTM FCF 利潤率 18.08% 低於 GoDaddy 33.66%。可能看錯的地方是份額數字多為公司自揭，第三方爬蟲資料口徑不一。","fact_refs":["f_peer_shop_gross_margin_pct","f_peer_shop_operating_margin_pct","f_peer_shop_fcf_margin_pct","f_peer_wix_gross_margin_pct","f_peer_wix_operating_margin_pct","f_peer_wix_fcf_margin_pct","f_peer_amzn_operating_margin_pct","f_peer_amzn_fcf_margin_pct","f_peer_gddy_operating_margin_pct","f_peer_gddy_fcf_margin_pct","f_kpi6_gmv"],"verdict_values":{"moat":{"mechanism":"統一商務作業系統的轉換成本，加上 Shop Pay 與 Shop 買家網路的雙邊效應。","execution":9,"pricing":7,"grade":"B","trend":"↑","trend_evidence":"執行面擴大、定價權穩定。美國增量占比由三年前近五分之一升至近半，前份記錄美國份額年增 2 個百分點，Shop Pay GMV 年增 50%。反向證據是代理式交易的分潤尚未定案。","competitor_notes":[{"name":"WIX","strategy_note":"TTM 毛利率 66.64%，營益率 −8.5%，FCF 利潤率 19.24%；毛利高但營業利益為負，事實表沒有其商務 GMV，無法判斷份額方向。"},{"name":"BIGC","strategy_note":"財務資料事實表無值，無法對照。"},{"name":"AMZN","strategy_note":"TTM 營益率 12.89%，FCF 利潤率 −6.38%；屬 10-K 所述可用更大客群與通路競價的大型對手類型。"},{"name":"GDDY","strategy_note":"TTM 營益率 26.05%、FCF 利潤率 33.66% 都高於 Shopify，獲利較高，但事實表沒有其成長與商務份額資料。"}],"spread_notes":{"basis":"份額替代 ROIC 差距","note":"同業 ROIC 事實表未涵蓋；美國電商份額約 14%，第三方爬蟲稱店家數占比 42.6%（2022 年 31.8%），單一來源且口徑不同。"},"peer_na_reason":"同業投入資本與 ROIC 事實表未涵蓋，BIGC 財務資料缺失，所以改用份額與利潤率對照。","threats":[{"level":"🔴","text":"AI 代理接管買家入口、代付與錢包預設，Shopify 從買家關係的擁有者退成後台。2026-03 OpenAI 撤下 Instant Checkout 是反例，但代理代購在 Q3 才開始出現。","p":30,"evidence_refs":["competitive_share_entrants#3","substitute_technology#1","substitute_technology#2"]},{"level":"🟡","text":"大型對手以更大客群與通路壓價，可能讓 Shopify 流失潛在銷售或被迫降價。目前份額仍在上升，屬點對點壓力。","p":20,"evidence_refs":["competitive_share_entrants#1"]},{"level":"🟡","text":"Sezzle 反壟斷案的壟斷主張進入審理，若 Shop Pay 分期的綁定受限，支付附著率會受影響；目前不是責任認定，受影響營收事實表未涵蓋。","p":15,"evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#2"]}],"roic_durability":{"quadrant":"無法驗算，投入資本事實表未涵蓋；TTM 營益率 18.07%、FCF 利潤率 18.08%，資本輕，方向偏高周轉。","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者與付款者都是商家，開店、收款、出貨是營運必需，延後代價高。年 GMV 達 100 萬美元的商家五年留存率 92%（2026-08-05 Hoffmeister），Q3 GMV 年增 29.5%。"},{"item":"決策層級","level":"🟡","text":"換平台要一起動線上店、門市、支付與平均 8 個應用程式，大型商家轉換成本高；小商家遷移容易，AI 建站也會降低門檻。分客群留存與漲價後流失事實表未涵蓋。"},{"item":"價值鏈分配","level":"🟡","text":"結帳與支付層目前仍在 Shopify 手上，商家解決方案毛利金額年增 37%；但代理平台握有買家入口。2026-11-03 Hoffmeister 只確認導流到商家網站時經濟模型相同，代理代購是否分潤沒有回答。"},{"item":"社會容忍度","level":"🟢","text":"收費約占 GMV 的 3.14%，事實表未見價格監管；搜尋未見 DOJ、FTC 或歐盟調查，目前是 Sezzle 與 Briskin 等民事訴訟。"}],"roiic":"事實表未涵蓋，缺投入資本；替代讀數為 FY2023 到 FY2025 增量營益率約 40%（營業利益增 18.1 億美元÷營收增 44.96 億美元，事實表 financial_history）。","reinvest_rate":"事實表未涵蓋，缺資本支出、折舊、營運資金與併購淨額。","endo_ceiling":null,"formula_note":"內生成長率＝增量 ROIC×再投資率，兩項輸入都缺，不推估。這家公司的再投資主要走損益表（TTM 研發占營收 12.49%，2026 第二季行銷不到 14%），資產負債表口徑會低估真實再投資。"}}}},"q3_growth":{"verdict":"跑道寬（🟢）：美國份額約 14%、全球零售不到 1%，B2B 和線下是已經量化的下一條曲線。","reasoning":"成長以量為主：GMV 年增 29.5%，新商家與同店貢獻各半；價次之，支付滲透率年增 3 個百分點，營收÷GMV 3.14%；併購幾乎沒有，回購事實表未涵蓋。共識 EPS FY2026E 到 FY2028E 年複合 29.5%，營收 FY2027E 年增 26.5%，差距約 3 個百分點來自利潤率擴張。FY2025A 的 0.94 美元是 GAAP，含大額營業外損益，不拿來算三年 CAGR。內生天花板缺投入資本無法驗算，共識與天花板的缺口歸為無法歸因，加註依賴 re-rate，信心上限為中。美國份額由 14% 到 30%，用公司揭露的相對增速（商家 23% 對市場 8%）約 6 年，用前份年增 2 個百分點約 8 年。十項衰退信號只有毛利率年比下滑亮燈：Q3 47.6% 對去年同期自算 48.9%，第四季指引毛利金額增速仍低於營收，來源是支付占比上升，商家解決方案毛利率連三季年增。其餘未亮或無資料：EPS 與營收增速差小於 5 個百分點，FY2025 FCF／淨利 1.63 倍，SBC 占營收 3.9%；產業倍數走勢事實表未涵蓋。反例是 GMV 報表增速為近五季最慢，訂閱營收年增由 22% 降至 20%。","fact_refs":["f_kpi6_gmv","f_kpi0_gaap","f_kpi7_mrr","f_kpi4_sbc_gaap","f_kpi5_q4_fy2026","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m"],"verdict_values":{"growth":{"driver_mix":"量為主（GMV），支付附著次之，併購與回購不構成驅動。","runway_years":"美國線上約 6–8 年到 30%；全球零售不到 1%，國際更長","runway_post_y5":"🟢","endo_ceiling_basis":"事實表缺投入資本、資本支出與營運資金，增量 ROIC 與再投資率都算不出，天花板留空；情境樹保守視為共識超過天花板，Bear 機率取 30%。","segments":[{"item":"訂閱解決方案","value":"8.36 億美元，年增 20%，毛利率 79%"},{"item":"商家解決方案","value":"29.06 億美元，年增 35%，自算毛利率 38.5%，毛利金額年增 37%"},{"item":"線下 GMV","value":"年增 30%，累計突破 2,000 億美元"},{"item":"B2B GMV","value":"年增 74%，上季 76%"},{"item":"國際 GMV","value":"年增 32%，上季 37%"},{"item":"代理式交易","value":"AI 流量 2.6 倍、訂單 3.3 倍，量體仍小，公司未揭露占 GMV 比重"}],"decay_signals":[{"signal":"毛利率連 2 季年比下滑","status":"亮燈","note":"Q3 年減約 1.3 個百分點，第四季指引延續；Q2 為 47.6% 左右，去年同期數字事實表未涵蓋，FY2025 48.07% 與 TTM 47.49% 同方向。"}],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"現金紀律佳但無法完整評分：SBC 稀釋低、淨現金約 45 億美元，回購與併購資料不足。","reasoning":"FY2025 FCF 20.07 億美元，FCF／淨利 1.63 倍，FY2024 為 0.79 倍（事實表 financial_history）；淨利受營業外損益影響，兩年都不適合單獨當轉換率。TTM FCF 利潤率 18.08%。Q3 的 22% 中，CFO 只把約 150 個基點的年增歸為結構性，其餘來自行銷測試、稅款時點與商家預支款會計變更。SBC 及相關稅占營收 3.9%，占 GAAP 營業利益 25.9%。現金流量表 SBC 140 百萬美元年化÷市值 1,915.76 億美元，稀釋約 0.3%／年，實際股數變動事實表未涵蓋。總債務 1.88 億美元，現金 47.27 億美元。現金去向四分、回購均價與債務到期事實表未涵蓋。已知最大的資本動作是 shop.com 約 1 億美元（2026-11-03 RBC 分析師提問所述金額，未見公司揭露），相對現金很小。","fact_refs":["f_kpi3_fcf","f_kpi4_sbc_gaap","f_net_debt_m","f_shares_diluted_m","f_peer_shop_fcf_margin_pct"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":false,"passed":null,"input":"近 12 個月未見大型併購；shop.com 約 1 億美元，報酬尚不可見。"},{"name":"buyback_yield","applicable":false,"passed":null,"input":"回購資料事實表未涵蓋。"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"現金流量表 SBC 140 百萬美元×4÷市值 191,576 百萬美元，約 0.3%／年，低於 1.5%；實際股數變動事實表未涵蓋。"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長靠內生，近 12 個月未見大型併購；回購、股利與現金去向事實表未涵蓋，無法展開。"}}}},"q5_valuation":{"verdict":"現價要求 EPS 五年年複合 25% 且五年後仍有 30 倍，才換得年化約 3%；我相信生意會成長，不接受這個價格的報酬。","reasoning":"現價 148.91 美元，FY2026E 本益比 78.79 倍，FY2027E 61.0 倍，EV／FY2026E 營收 12.21 倍。共識 FY2026E 到 FY2028E EPS 年複合 29.5%，PEG 2.67，FY2027E 口徑 2.07，都高於 2。反推：要在現價拿到年化 10%，五年後股價要約 240 美元，以 30 倍算 FY2031E EPS 要 8.0 美元，高於多頭路徑 7.80 美元。連續五年分位事實表未涵蓋，只有年度端點：P/S 分位 55.2，EV/S 分位 52.7；trailing P/E 分位 3.2 只有 3 點，早年獲利極低，不具參考性。共識修正偏平：FY2027E −0.41%，FY2028E −0.63%，FY2026E 近 3 個月 −0.53%。賣方平均目標價 157.58 至 174.57 美元，高於現價 6% 至 17%，全距 120 至 231 美元，來源日期不一，這些是 12 個月倍數延續假設，不反駁五年報酬的計算。動能未過熱：RSI 42.76，26 週報酬 34.87%，4 週漂移事實表未涵蓋。反例：連續超預期時 EPS 可能遠高於共識，FY2028E 上修到 3.95 美元以上，基礎情境年化可回到 8% 左右。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_pe_current","f_pe_percentile","f_ps_current","f_ps_percentile","f_ev_s_current","f_ev_s_percentile","f_ev_s_fwd","f_ev_m","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_fy1_pct","f_consensus_rev_fy2_pct","f_consensus_rev_fy3_pct","f_consensus_rev_3m_fy1_pct","f_rsi14","f_week26_return_pct","f_ma_state","f_ma_w52","f_ma_w104","f_ma_w250","f_ma_slope_w250_pct"],"verdict_values":{"valuation":{"basis":"前瞻本益比與 PEG 為主，EV／營收對照。","tier":"高成長商務平台","peers":{"expanded":false,"reason":"本包沒有同業倍數，同業表只有利潤率；唯一可用的是前份摘要的 NOW 28 倍，屬 2026-08 舊值，不足以展開。"},"fwd_pe":78.79,"peg":2.67,"percentile_5y":null,"val_light":"🔴","val_light_derivation":"FY2026E 本益比 78.79÷FY2026E–FY2028E 共識 EPS 年複合 29.5%，PEG 2.67；FY2027E 口徑 2.07，都高於 2。基礎情境五年年化約 3%，低於 8%，判最貴一級。短期上行指 12 個月，FY2027E EPS 2.44 美元×65 倍約 158.6 美元；中期指 3 年，FY2029E EPS 4.00 美元×44 倍約 176 美元。","upside_short_pct":6.5,"upside_mid_pct":18.2,"denominator_disputed":false,"denominator_note":"FY2025 GAAP EPS 受營業外損益扭曲，改用前瞻共識當分母。FY2026E 1.89 美元的口徑事實表未標明，由季度共識量級推斷為調整後；若扣 SBC，倍數更高，不改變結論。"}}},"q6_how_wrong":{"verdict":"最可能看錯兩件事：代理式交易把支付經濟分走，以及 79 倍的倍數收斂得比 EPS 複利快。","reasoning":"價值陷阱風險判中等，依據見反證紀錄：十項衰退信號亮一項。偏多時最可能錯在代理式交易的分潤，偏空時最可能錯在低估 EPS 上修幅度。法說有兩題沒有正面回答：2026-08-05 CIBC 問 FCF 利潤率約 20% 是否新常態，CFO 只指向下季指引；同場 Morgan Stanley 問 Sidekick 對留存與 GMV 的數據，Finkelstein 沒給數字。2026-11-03 只補了開店與轉換指南帶來的 8% 與 3% 提升，留存數字仍缺。歷史最大回撤、空方最強數字事實表未涵蓋。","fact_refs":["f_fwd_pe_latest","f_kpi6_gmv","f_kpi3_fcf"],"verdict_values":{"trap":{"verdict":"🟡","label":"毛利率年比下滑亮燈，來自支付占比上升，需求沒有轉弱。"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":1.89,"pe":78.79,"basis":"FY2026E 共識 EPS（FY1），現價 148.91 美元；終端倍數同樣用當年度 EPS。"},"eps":{"bull":[2.55,3.5,4.7,6.15,7.8],"base":[2.44,3.17,4.0,4.9,5.85],"bear":[2.15,2.25,2.32,2.36,2.4]},"pe":{"bull":38,"base":30,"bear":22},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0,"net_buyback":0},"second_stage":{"bull_cagr_pct":18,"base_cagr_pct":13},"max_dd":{"lo":-65,"hi":-45,"basis":"三個錨：250 週均線 86.4 美元對應 −42%；FY2029E EPS 4.00 美元在成長降到 10% 時給 22 倍為 88 美元，對應 −41%，成長降到 5% 時給 15 倍為 60 美元，對應 −60%；Bear 終點 52.8 美元對應 −64.5%。倍數收斂時回撤常超過基本面，上緣取 −45%，下緣取 −65%。歷史最大回撤事實表未涵蓋。","trigger_time":null},"basis":{"bull":"GMV 年複合約 28%，代理式帶來增量且不分潤，FY2031E 營收約 510 億美元、淨利率約 20%；終端 38 倍，高於前份記錄的 NOW 28 倍，對應當時 EPS 年增約 25%。","base":"FY2027E、FY2028E 照共識，之後增速由 26% 降到 19%，FY2031E 營收約 420 億美元、淨利率約 19%；終端 30 倍，略高於前份記錄的同業上緣 NOW 28 倍（2026-08 舊值，本包沒有新值）。","bear":"營收增速降到 10% 左右，AI 與支付成本把淨利率由約 16% 壓到約 12%，FY2031E EPS 2.40 美元；終端 22 倍取成長熄火至 10% 的倍數。機率 30%，依據是內生天花板無法驗算、毛利率年比下滑、代理分潤未定。"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"個人代理在 Q3 開始替使用者下單；2026-11-03 Wolfe 問代理是否分潤時，Hoffmeister 只回答導流到商家網站的情況。Baillie Gifford 與 10-K 都點出平台整合與資料限制的風險。","assumption":"Shopify 能守住結帳層，並讓 Shop Pay 成為代理內的常用錢包。","consequence":"代理平台若拿走入口與錢包，支付滲透率 68% 會下滑；營收÷GMV 每掉 30 個基點，營收約少 10%，倍數同時下移，五年虧 50% 以上最可能從這裡來。","ruling":"部分採納。AI 流量 2.6 倍、訂單 3.3 倍，量體仍小，OpenAI 2026-03 撤下 Instant Checkout 表示結帳層不易取代；分潤未定，保留在 30% 的 Bear 機率，與唯一致命點是同一件事。","watch":"代理式訂單的經濟模型揭露、支付滲透率、Shop Pay GMV 年增。","evidence_refs":["competitive_share_entrants#3","substitute_technology#1","substitute_technology#2"],"fact_refs":["f_kpi0_gaap","f_kpi6_gmv"]},{"view":"論點成功但股東經濟變差","evidence":"Q3 營收年增 32%，毛利金額只增 28%，整體毛利率 47.6%，去年同期自算 48.9%；訂閱毛利率 79%，連兩季低於 80% 趨勢線，代管與 Sidekick 成本增加；Q3 FCF 年增大部分屬暫時。第三方雲端依賴也讓成本不全在公司手上。","assumption":"GMV 持續成長，利潤也等比增加。","consequence":"大型商家占比升高，價值更多落在低毛利支付；AI 功能不直接收費；營業費用率下降空間縮小後，EPS 複利會低於預期。","ruling":"部分反駁。商家解決方案毛利率連三季年增，Sidekick 總成本 Q2 到 Q3 下降 18%，支付端沒有侵蝕；訂閱毛利率下滑採納為監測項。","watch":"毛利金額年增與營收年增的落差、訂閱毛利率、營業費用占營收。","evidence_refs":["geo_supply_chain#0"],"fact_refs":["f_kpi0_gaap","f_kpi3_fcf","f_kpi5_q4_fy2026"]},{"view":"價格已反映太多","evidence":"FY2026E 本益比 78.79 倍，PEG 2.67，EV／FY2026E 營收 12.21 倍。","assumption":"市場五年後仍願給 30 倍以上，且 EPS 年複合 25%。","consequence":"基礎情境年化約 3%；EPS 達標時，股東報酬仍可能被倍數收斂吃掉。","ruling":"採納，這是本次不追的主因。要年化 10%，FY2031E EPS 需約 8.0 美元，高於多頭路徑。","watch":"股價是否到 110 美元以下；FY2028E 共識 EPS 是否到 3.95 美元以上。","evidence_refs":[],"fact_refs":["f_fwd_pe_latest","f_ev_s_fwd","f_consensus_eps_fy1","f_consensus_eps_fy3"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 🟡 → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=🟡","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 151.57 → 本次 148.91（-1.8%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=151.57","side_b":"本次 price_at_dd=148.91","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 151.57 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 151.57 美元：Bull 價 243.8、Bear 價 67，五年期望值 −2.3%，基準年化 −3.1%，不對稱比 1.3","side_b":"本次情境、股價仍用 151.57 美元：Bull 價 296.4、Bear 價 52.8，五年期望值 +11.4%，基準年化 3.0%，不對稱比 1.22","ruling":"先換情境、股價不動：五年期望值多 13.7 個百分點，基準年化多 6.1 個百分點。不對稱比由 1.3 變為 1.22。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變好。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 151.57 美元：五年期望值 +11.4%，基準年化 3.0%，不對稱比 1.22","side_b":"本次情境、股價 148.91 美元：五年期望值 +13.4%，基準年化 3.3%，不對稱比 1.28","ruling":"再換股價、情境不動：起點價下跌 1.8%，五年期望值多 2.0 個百分點，基準年化多 0.4 個百分點，不對稱比由 1.22 升到 1.28。合計五年期望值比前份多 15.7 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"估值與裁決維持","cause":"價格變動","prior_field":["val","signal"],"side_a":"前份：股價 151.57 美元，估值最貴一級，訊號 B，觀望，追蹤。","side_b":"本次：股價 148.91 美元，跌約 1.8%，估值仍是最貴一級，訊號 B，結論仍是不追。","ruling":"股價幾乎沒動，EPS 共識也沒有明顯上修，估值結論不變。","evidence_level":"事實表股價與共識快照","settle_metric":"股價與 FY2028E 共識 EPS","if_then":["若股價跌到 110 美元以下且基本面無損，則分批反買，首倉 1/3。","若股價續漲而共識未上修，則不追。"],"evidence_refs":[]},{"axis":"價值陷阱風險上調","cause":"新證據","prior_field":["trap"],"side_a":"前份：風險低（🟢）。","side_b":"本次：風險中等（🟡），毛利率年比下滑亮燈，Q3 47.6% 對去年同期 48.9%，第四季指引毛利金額增速仍低於營收。","ruling":"上調一級但不升到高風險，毛利率下滑來自支付占比，商家解決方案毛利率連三季年增。","evidence_level":"一手，8-K 與法說","settle_metric":"商家解決方案毛利率與毛利金額增速","if_then":["若訂閱毛利率連 4 季低於 77%，則持有者減碼至半倉。","若毛利金額增速連 2 季追上營收增速，則風險回到低。"],"evidence_refs":[]},{"axis":"護城河、跑道與公司類型維持","cause":"新證據","prior_field":["moat_trend","runway_post_y5","archetype","cycle_position"],"side_a":"前份：護城河向上，跑道寬，品質複利成長，未標循環位置。","side_b":"本次：相同。新證據是美國增量占比近半、歐洲份額三年翻倍、B2B GMV 年增 74%、線下 GMV 年增 30%。","ruling":"維持。Q3 數字支持份額繼續上升，代理式風險放在威脅與情境機率，不提前下調方向。","evidence_level":"一手為主，份額由公司自揭","settle_metric":"美國增量占比、固定匯率 GMV","if_then":["若美國份額年增連 2 季不再上升，則方向改為穩定並停止加碼。","若第三方資料也確認份額上升，則維持。"],"evidence_refs":[]},{"axis":"情境機率與回撤幅度","cause":"方法變動","prior_field":["p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份：多頭 30%，空頭 25%，最大回撤 −58%。","side_b":"本次：多頭 25%，空頭 30%，最大回撤 −45% 至 −65%。","ruling":"內生天花板缺投入資本無法驗算時採保守處理，空頭定在 30%；回撤由單點改成區間。","evidence_level":"判斷","settle_metric":"投入資本與增量 ROIC 補齊後重算","if_then":["若補齊資料後共識低於內生天花板，則空頭機率可回到 25%。","若高於天花板，則維持 30% 且信心不上調。"],"evidence_refs":[]},{"axis":"進場首倉門檻舊→新（估值 rearm）","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"股價回檔至 $70–90 區間（$70≈PEG 1.0 對應 FY+1 共識成長 29.2%；上緣 $90 保留予國際 take rate 收斂槓桿〔Payments 僅covers~40國〕兌現空間）；或終端倍數假設站上同業現值上緣（NOW 28x）之後仍具正 EV；觸發後首階 1/3 分批建倉","side_b":"股價≤110 美元（基礎情境年化約 10%），或 FY2028E 共識 EPS≥3.95 美元且股價未同步上漲；觸發後重跑研究，首倉上限 1/3","ruling":"進場錨由 PEG 1.0 改成基礎情境年化約 10%，終端年滾到 FY2031E。舊的 70–90 美元等於要求年化 14% 至 20%；110 美元對應 FY2027E 口徑 PEG 約 1.5。前份 FY+2 共識上修≥33%、回檔≥20% 的條件同時改為本次兩個條件。","evidence_level":"判斷，由情境樹反推","settle_metric":"股價、FY2028E 共識 EPS","if_then":["若股價≤110 美元且固定匯率 GMV 仍高於 27%，則重跑研究，通過後首倉 1/3。","若到價但 H1 或 H2 已削弱，則不進場。"],"evidence_refs":[]},{"axis":"減碼與清倉指標新設","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設，值為 null。","side_b":"本次新設：固定匯率 GMV 連 2 季低於 24%；營收÷GMV 連 2 季年比不再上升；支付滲透率連 2 季不再上升；訂閱毛利率連 4 季低於 77%；毛利金額增速落後營收超過 5 個百分點連 4 季；揭露代理分潤。","ruling":"前份沒有獨立的減碼與清倉條件，本次補上；前份 H1、H2 的份額、B2B 與貨幣化門檻保留在論點門檻內。","evidence_level":"判斷","settle_metric":"季報與法說","if_then":["若單一指標成立，則持有者減碼至半倉。","若 H1 與 H2 同時反轉，則清倉。"],"evidence_refs":[]},{"axis":"Single Thing 唯一致命點舊→新","cause":"新證據","prior_field":["single_thing"],"side_a":"前份未設，值為 null。","side_b":"前三大個人代理之一把自家錢包設為預設或向商家收通路抽成，且 Shopify 首次揭露代理式交易的支付附著低於網店。","ruling":"Q3 是代理代購首次出現，分潤問題在法說被問到但沒有回答，所以本次設為唯一致命點。","evidence_level":"一手法說，事件尚未發生","settle_metric":"代理式交易的支付附著與分潤揭露","if_then":["若事件發生，則持有者減碼至半倉，未持有者取消進場條件。","若連 4 季支付滲透率續升且無分潤揭露，則機率下調至 10%。"],"evidence_refs":["competitive_share_entrants#3","substitute_technology#1","substitute_technology#2"]},{"axis":"貨幣化門檻由季比改年比","cause":"方法變動","prior_field":["thesis.H2.threshold"],"side_a":"Take rate 連 2 季 QoQ 不再上升；或 Payments 滲透率連 2 季不再上升","side_b":"營收÷GMV 連 2 季年比不再上升；支付滲透率連 2 季不再上升；揭露向代理平台分潤。","ruling":"第四季 GMV 季節性放大，季比容易誤觸，所以改年比。沿用季比來看，Q3 3.14% 與前份記錄持平，記一季未升。","evidence_level":"一手，8-K","settle_metric":"營收÷GMV","if_then":["若連 2 季年比不再上升，則 H2 標削弱並停止加碼。","若年比恢復上升，則解除。"],"evidence_refs":[]},{"axis":"成長是否減速","cause":null,"prior_field":null,"side_a":"報表面：GMV 年增 29%，近五季最慢；訂閱營收年增由 22% 降至 20%；國際 GMV 由 37% 降到 32%，線下由 32% 降到 30%。","side_b":"管理層（2026-11-03 Hoffmeister）：固定匯率 30%，連六季相近，北美 28% 持平，第四季指引低 30% 段。","ruling":"可調和，屬程度差異。固定匯率減速幅度小，還不是趨勢反轉。","evidence_level":"一手，8-K 與法說","settle_metric":"固定匯率 GMV 年增率","if_then":["若連 2 季低於 24%，則 H1 標削弱，持有者停止加碼。","若回到 30% 以上，則維持。"],"evidence_refs":[]},{"axis":"代理式交易的經濟歸屬","cause":null,"prior_field":null,"side_a":"2026-08-05 Finkelstein：代理式交易沒有新費用、沒有另外定價。2026-11-03 Finkelstein：代理是新前門，其餘都是 Shopify。","side_b":"2026-11-03 Wolfe 問是否與代理分潤，Hoffmeister 只答導流到商家網站時相同，代理代購沒有回答；Jefferies 問 Shop Pay 與 Meta Pay 的經濟差異也沒有數字。外部評論認為 AI 平台可能接管結帳。","ruling":"方向相反，屬不可調和矛盾。目前選管理層一側，依據是代理式交易接的仍是商家結帳，且 OpenAI 撤下 Instant Checkout；決勝數據今天不存在，不可裁決至 2027 年底。","evidence_level":"一手法說，分潤數據不存在","settle_metric":"代理式訂單支付附著率與分潤揭露","if_then":["若揭露代理平台抽成或代理訂單支付附著低於網店，則持有者減碼至半倉，未持有者取消首倉條件。","若連 4 季代理訂單年增至少 2 倍且支付滲透率持續上升，則多頭機率上調 5 個百分點，但不追價。"],"evidence_refs":["competitive_share_entrants#3","substitute_technology#2"]},{"axis":"訂閱毛利率 80% 趨勢線","cause":null,"prior_field":null,"side_a":"2026-08-05 Hoffmeister：訂閱毛利率略低於 80%，Sidekick 放量下季對季維持相近。","side_b":"2026-11-03：79%，季減，主因代管成本；被問 80% 趨勢線時回答沒有改變，但沒有時間表，第四季還有基礎建設支出。","ruling":"可調和，但管理層說法偏樂觀。Sidekick 總成本季減 18% 屬實，壓力轉到代管。標為未證、監測。","evidence_level":"一手法說","settle_metric":"訂閱毛利率","if_then":["若 2027 上半年沒有回到 79% 以上，則視為結構性成本，Bear 機率不下調。","若連 2 季回到 80%，則解除此項監測。"],"evidence_refs":["geo_supply_chain#0"]},{"axis":"FCF 改善有多少是結構性","cause":null,"prior_field":null,"side_a":"2026-11-03 Hoffmeister：年增約 150 個基點屬結構性；2026-08-05 也說扣除會計變更年增約 1.5 點。","side_b":"第四季指引 FCF 利潤率只與去年相當；Q3 其餘年增來自三項暫時因素；2026-08-05 被問 20% 是否新常態時未正面回答。","ruling":"不採信也不否定，標未證、監測。預先設定：FY2027 前兩季 FCF 利潤率平均年增低於 100 個基點，結構性說法視為不成立。","evidence_level":"一手法說","settle_metric":"FCF 利潤率年增","if_then":["若 FY2027 前兩季平均年增低於 100 個基點，則 H3 標削弱，持有者停止加碼。","若平均年增達 150 個基點以上，則採信結構性說法。"],"evidence_refs":[]},{"axis":"賣方共識與本次看法","cause":null,"prior_field":null,"side_a":"賣方：一源稱 51 位中 38 位正面，平均目標價 157.58 至 174.57 美元，Citi 216、RBC 200、Cantor 158。","side_b":"本次：基礎情境五年年化約 3%，不追。","ruling":"分歧在框架層，事實層沒有爭議。賣方用 12 個月倍數延續，本次用五年終端 30 倍。市場可能錯在倍數體制，把多年 30% 成長當成不會收斂。目標價全距 120 至 231 美元，約 1.9 倍，未大到要再下調信心。","evidence_level":"二手彙整，日期不一","settle_metric":"FY2028E 共識 EPS 上修幅度","if_then":["若 FY2028E 共識 EPS 上修至 3.95 美元以上且股價未同步上漲，則重跑研究。","若股價續漲而共識未上修，則不追。"],"evidence_refs":[]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"現在就買：加上第四季指引將連七季營收年增低 30 段，美國份額才 14%，費用率還在降；EPS 持續超預期時 79 倍會很快被消化；股價只高於 52 週均線約 10%，RSI 42.76。","side_b":"不買：即使 EPS 年複合 25%，五年年化仍只有約 3%，要年化 10% 須超過多頭路徑。","ruling":"選不買。約束條件是價格，生意本身沒有問題；這個結論在 FY2028E 共識明顯上修時會被推翻。","evidence_level":"事實表與情境樹","settle_metric":"股價、FY2028E 共識 EPS","if_then":["若股價跌到 110 美元以下且固定匯率 GMV 仍高於 27%，則分批反買，首倉 1/3。","若 FY2028E 共識 EPS 達 3.95 美元以上且股價未同步上漲，則重跑研究。"],"evidence_refs":[]},{"axis":"產業態勢三軸","cause":null,"prior_field":null,"side_a":"競爭面：10-K 提到大型對手可能積極定價，平台可能限制資料存取；代理入口是新的競爭層。","side_b":"結構面：Shopify 商家拿走美國增量近半，全球電商仍年增約 7%。其他結構變數：Sezzle 反壟斷案繼續審理，未見 DOJ、FTC 或歐盟調查。","ruling":"雙向拉鋸。份額轉移目前有利 Shopify，代理入口與訴訟是未定的反向力量。","evidence_level":"一手 10-K、法說，訴訟為二手","settle_metric":"美國增量占比、支付滲透率、訴訟里程碑","if_then":["若份額與支付滲透率同時下行，則改判競爭惡化中，持有者減碼至半倉。","若代理訂單放量且支付滲透率續升，則改判結構性轉好中。"],"evidence_refs":["competitive_share_entrants#1","substitute_technology#1","regulatory_antitrust#0"]}],"triggers":[{"n":1,"text":"GMV 成長跌破論點下限","type":"假設驗證","maps_to":"H1","metric":"固定匯率 GMV 年增率","threshold":"連 2 季低於 24%","action":"不追；持有者停止加碼","source_freq":"季報與法說，每季","date":"2027-02"},{"n":2,"text":"貨幣化不再上升","type":"假設驗證","maps_to":"H2","metric":"營收÷GMV、支付滲透率","threshold":"連 2 季年比不再上升，或支付滲透率連 2 季不再上升","action":"停止加碼；持有者標削弱","source_freq":"8-K 與法說，每季","date":"2027-02"},{"n":3,"text":"營運槓桿吸收不了 AI 成本","type":"假設驗證","maps_to":"H3","metric":"FCF 利潤率、毛利金額增速減營業費用增速","threshold":"FY2027 FCF 利潤率低於 18%，或增速差連 2 季低於 5 個百分點","action":"停止加碼；下修基礎情境 EPS 後重算","source_freq":"8-K，每季","date":"2027-05"},{"n":4,"text":"訂閱毛利率持續下滑","type":"風險","maps_to":"R2","metric":"訂閱毛利率","threshold":"連 4 季低於 77%","action":"持有者減碼至半倉","source_freq":"8-K，每季","date":null,"evidence_refs":["geo_supply_chain#0"]},{"n":5,"text":"關稅與消費的衝擊吸收失敗","type":"風險","maps_to":"R3","metric":"北美固定匯率 GMV 年增率、交易與貸款損失占營收","threshold":"北美連 2 季低於 22%，或損失占營收高於 5%","action":"停止加碼；連 4 季成立則減碼至半倉","source_freq":"法說與 10-Q，每季","date":null,"evidence_refs":["reg_tariff_export#0","reg_tariff_export#1"]},{"n":6,"text":"訴訟進入不利階段","type":"風險","maps_to":"R4","metric":"Sezzle 反壟斷案、Briskin 隱私集體訴訟進度","threshold":"集體認證加不利和解，或判賠與和解超過 8 億美元；刑事介入","action":"不利和解則減碼至半倉；刑事介入則清倉","source_freq":"法院文件與 10-Q，事件驅動","date":null,"evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#2","major_events#1","lawsuit_class_action#0","lawsuit_class_action#1"]},{"n":7,"text":"代理平台改寫支付經濟","type":"Single Thing","maps_to":"Single Thing","metric":"代理錢包預設、通路抽成、代理訂單支付附著率","threshold":"前三大個人代理之一發生，且 Shopify 揭露支付附著低於網店","action":"持有者減碼至半倉，未持有者取消進場條件","source_freq":"法說、8-K、代理平台條款，事件驅動","date":null,"evidence_refs":["competitive_share_entrants#3","substitute_technology#1","substitute_technology#2"]},{"n":8,"text":"價格或上修達到進場條件","type":"估值rearm","maps_to":"H1、H2、H3","metric":"股價、FY2028E 共識 EPS","threshold":"股價≤110 美元，或 FY2028E 共識 EPS≥3.95 美元且股價未同步上漲","action":"重跑研究，通過後首倉 1/3","source_freq":"日收盤、共識快照每月","date":null},{"n":9,"text":"股價先漲、證據沒跟上","type":"減碼","maps_to":"估值","metric":"股價÷FY2027E 共識 EPS","threshold":"達 80 倍（約 195 美元）且共識未上修","action":"不追；持有者減碼至半倉","source_freq":"日收盤、共識快照每月","date":null},{"n":10,"text":"成長與貨幣化同時反轉","type":"清倉","maps_to":"H1、H2","metric":"固定匯率 GMV、營收÷GMV","threshold":"GMV 偏離路徑連 3 季達 10%，且營收÷GMV 連 3 季年比下降","action":"清倉","source_freq":"8-K，每季","date":null},{"n":11,"text":"第四季財報複審","type":"複審日期","maps_to":"H3","metric":"FCF 利潤率、毛利金額年增","threshold":"FCF 利潤率與 2025 第四季相當；毛利金額年增高 20% 段","action":"未達則把 150 個基點的結構性說法列為存疑，重跑研究","source_freq":"季報","date":"2027-02"}],"kill_metrics":[{"metric":"固定匯率 GMV 年增率","bear_threshold":"連 2 季低於 24%","window":"2 季","source":"8-K 與法說","last_status":"ok"},{"metric":"營收÷GMV 年比","bear_threshold":"連 2 季年比不再上升","window":"2 季","source":"8-K，營收與 GMV 自算","last_status":"ok"},{"metric":"支付滲透率","bear_threshold":"連 2 季不再上升","window":"2 季","source":"法說","last_status":"warning"},{"metric":"訂閱毛利率","bear_threshold":"連 4 季低於 77%","window":"4 季","source":"8-K 自算、法說","last_status":"warning"},{"metric":"毛利金額年增減營收年增","bear_threshold":"落後超過 5 個百分點，連 4 季","window":"4 季","source":"8-K 與法說","last_status":"warning"},{"metric":"代理式交易分潤與支付附著","bear_threshold":"揭露向代理平台分潤，或代理訂單支付附著低於網店","window":"12–24 個月","source":"法說、8-K、代理平台條款","last_status":"unknown"}],"evidence_dismissed":[],"action_conditions":{"rearm_trigger":"股價≤110 美元（基礎情境年化約 10%），或 FY2028E 共識 EPS≥3.95 美元且股價未同步上漲；觸發後重跑研究，首倉上限 1/3","exec_line":"目前不追。到價或共識上修後先重跑研究，通過後首倉 1/3，其餘兩段分別等下一季與再下一季財報驗證。"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等股價≤110 美元，或 FY2028E 共識 EPS 上修到≥3.95 美元且股價未同步上漲。","qc48_result":"fail","qc48_note":"Bull 情境的 EPS 路徑只有總量層級的算術，缺少分部的量乘價，關鍵假設也沒有來源。再看實際報酬：Shopify 自己 2021 年高估值進場後，5 年年化只有約 0%～3.5%，遠低於 Bull 隱含的 +14.8%/年，判斷物沒有交代本案為何不同，所以這個 Bull 依據不成立。"},"thesis":{"H":[{"id":"H1","text":"Shopify 商家持續拿到遠高於份額的電商增量，GMV 成長維持在市場三倍以上。","2y":"FY2027–FY2028 固定匯率 GMV 年增不低於 24%。","5y":"FY2031E 美國電商份額達 20% 以上，營收年複合約 22%。","10y":null,"threshold":"固定匯率 GMV 年增連 2 季低於 24%；美國份額年增連 2 季不再上升；B2B GMV 年增低於 40%（後兩項沿用前份）。","source":"季報 8-K、法說、公司引 Census 與 eMarketer 的份額揭露，每季。","drift_rule":"2 年期：TTM 偏離路徑連 2 季達 5% 為削弱，連 3 季達 10% 為反轉；5 年期：連 4 季達 5% 為削弱，連 6 季達 10% 為反轉。"},{"id":"H2","text":"支付與 Shop Pay 的貨幣化繼續上升，代理式交易不稀釋每筆 GMV 的收入。","2y":"到 FY2028 營收÷GMV 年比持續上升，支付滲透率不低於 71%。","5y":null,"10y":null,"threshold":"營收÷GMV 連 2 季年比不再上升；支付滲透率連 2 季不再上升；揭露向代理平台分潤。","source":"季報 8-K 的營收與 GMV，法說的支付滲透率與代理經濟說明，每季。","drift_rule":"2 年期：TTM 偏離路徑連 2 季達 5% 為削弱，連 3 季達 10% 為反轉。"},{"id":"H3","text":"AI 與基礎建設成本被營運槓桿吸收，FCF 利潤率站穩 20%。","2y":"FY2027 FCF 利潤率不低於 19%，FY2028 不低於 20%；毛利金額增速高於營業費用增速至少 5 個百分點。","5y":"FY2031E 淨利率接近 19%。","10y":null,"threshold":"FY2027 FCF 利潤率低於 18%；訂閱毛利率連 4 季低於 77%；毛利金額增速減營業費用增速連 2 季低於 5 個百分點（現約 12 個百分點）。","source":"季報 8-K、現金流量表、法說，每季。","drift_rule":"2 年期：TTM 偏離路徑連 2 季達 5% 為削弱，連 3 季達 10% 為反轉；5 年期：連 4 季達 5% 為削弱，連 6 季達 10% 為反轉。"}],"R":[{"id":"R1","text":"AI 代理接管買家入口與錢包預設，支付經濟被分走。","h_ref":"H2","clock":"🐢","threshold":"揭露向代理平台分潤，或支付滲透率連 2 季年比下降。","evidence_refs":["competitive_share_entrants#3","substitute_technology#1","substitute_technology#2"]},{"id":"R2","text":"AI 與代管成本持續上升，訂閱毛利率回不到 80%，毛利金額增速長期落後營收。","h_ref":"H3","clock":"🔥","threshold":"訂閱毛利率連 4 季低於 77%，或毛利金額增速落後營收超過 5 個百分點連 4 季。","evidence_refs":["geo_supply_chain#0"]},{"id":"R3","text":"關稅與消費轉弱打到中小商家，GMV 下行、商家流失與貸款損失上升。","h_ref":"H1","clock":"⚡","threshold":"北美固定匯率 GMV 連 2 季低於 22%，或交易與貸款損失占營收高於 5%（2026 第二季 3.9%）。","evidence_refs":["reg_tariff_export#0","reg_tariff_export#1"]},{"id":"R4","text":"Sezzle 反壟斷案與 Briskin 結帳隱私集體訴訟進入實質階段，Shop Pay 綁定或資料蒐集受限。兩案都是民事，受影響營收與結案時點事實表未涵蓋。","h_ref":"H2","clock":"🔥","threshold":"集體認證加不利和解，或判賠與和解超過 8 億美元（約一季 FCF）。","evidence_refs":["regulatory_antitrust#0","regulatory_antitrust#2","major_events#1","lawsuit_class_action#0","lawsuit_class_action#1"]},{"id":"R5","text":"大型對手用更大客群與通路壓價，Plus 與企業客戶擴張變慢。","h_ref":"H1","clock":"🔥","threshold":"Plus MRR 年增連 4 季低於 10%（Q3 為 18%）。","evidence_refs":["competitive_share_entrants#1"]},{"id":"R6","text":"倍數收斂快於 EPS 複利，營運達標時股東報酬仍不足。","h_ref":"H1","clock":"🐢","threshold":"FY2027E 本益比跌破 35 倍且共識同時下修。","evidence_refs":[]}],"single_thing":{"description":"前三大個人代理之一把自家錢包設為預設或向商家收通路抽成，且 Shopify 首次揭露代理式交易的支付附著低於網店。","why_fatal":"在單一事件能改變的變數裡，這項敏感度最大：商家解決方案占營收 78%，營收÷GMV 3.14%，每掉 30 個基點營收約少 10%，五年 EPS 複利與終端倍數會一起下修。","if_happens":"持有者減碼至半倉，未持有者取消進場條件，Bear 機率上調至 40%，重做情境。","how_monitor":"每季看法說對代理經濟的說明、支付滲透率、Shop Pay GMV 年增；事件面看 8-K 與代理平台條款公告。","probability":"12–24 個月約 15%。"}},"appendix_a":{"growth_durability":8,"quality_score":6,"ai_risk":"🟡","long_term_confidence":"中","fpe_fy2":61.03,"peg_fy2":2.07,"stress":{"pass":0,"total":3}},"eps_meta":{"base_eps_path":{"FY2025A":0.94,"FY2026E":1.89,"FY2027E":2.44,"FY2028E":3.17},"fy_end_month":12,"eps_basis":"FY2025A 為 GAAP 稀釋 EPS，含大額營業外損益；FY2026E–FY2028E 為 Koyfin 共識，口徑事實表未標明，由季度共識量級推斷為調整後。兩者口徑不同，成長率以 FY2026E 為基期。"},"catalysts":[{"date":"2026-11","date_precision":"month","type":"other","event":"黑色星期五與網路星期一檔期","impact":"中","watch":"GMV 動能、平台穩定度、Shop Pay 與代理式訂單的揭露。"},{"date":"2027-02","date_precision":"month","type":"guidance","event":"Q4 FY2026 財報與 FY2027 首季指引，日期未公告","impact":"高","watch":"固定匯率 GMV、毛利金額年增、FCF 利潤率、訂閱毛利率。"},{"date":"2027-05","date_precision":"month","type":"guidance","event":"Q1 FY2027 財報，日期未公告","impact":"高","watch":"FCF 利潤率年增是否達 100 個基點以上，支付滲透率是否續升。"},{"date":null,"type":"regulatory","event":"Sezzle 反壟斷案與 Briskin 隱私集體訴訟進度，時點事實表未涵蓋","impact":"中","watch":"集體認證、和解金額、對 Shop Pay 綁定的限制。"},{"date":null,"type":"product","event":"個人代理的錢包與分潤條款變動","impact":"高","watch":"代理式訂單的支付附著率，以及是否出現向代理平台分潤。"}],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8","pacing":[],"holding_cap":null,"audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='↑', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":true,"basis":"signal='B', runway='🟢', val='🔴', moat_trend='↑', week26=34.87, valuation_dependent=False"},{"row":"8a-QC48","condition":"row 8a 命中須經 QC-48 爆發候選 Bull 冷讀；critic 未放行（fail／not_run）→ 落 row 8","hit":true,"basis":"qc48_result='fail', 結論='Bull 情境的 EPS 路徑只有總量層級的算術，缺少分部的量乘價，關鍵假設也沒有來源。再看實際報酬：Shopify 自己 2021 年高估值進場後，5 年年化只有約 0%～3.5%，遠低於 Bull 隱含的 +14.8%/年，判斷物沒有交代本案為何不同，所以這個 Bull 依據不成立。'"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position=None, moat='B', moat_trend='↑', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":true,"basis":"signal='B', val='🔴'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":false,"basis":"signal='B', val='🔴', ma='🟡'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🔴', ma='🟡'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🔴', ma='🟡'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"requires_critic":[]}}
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
