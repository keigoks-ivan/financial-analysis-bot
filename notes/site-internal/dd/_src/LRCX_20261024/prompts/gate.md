你是 DD 管線 v20 的判斷層閘（gate），標的 LRCX（20261024）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（32 條）
- `f_kpi0_gaap`（q1_business）｜營收（GAAP）＝8219.4 百萬美元｜期間與口徑：季末 2026-09-27 季度（公告 2026-10-21）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 newsroom.lamresearch.com 2026-10-21（numbers.latest_quarter_kpis.items[0]，as_of 季末 2026-09-27 季度（公告 2026-10-21））
  - 註記：上季指引 8.1B±0.4B，實績高於中點；共識數字未查
- `f_kpi1_non_gaap`（q1_business）｜Non-GAAP 營業利益率＝40.2 %｜期間與口徑：季末 2026-09-27 季度（公告 2026-10-21）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 newsroom.lamresearch.com 2026-10-21（numbers.latest_quarter_kpis.items[1]，as_of 季末 2026-09-27 季度（公告 2026-10-21））
  - 註記：未查
- `f_kpi2_gaap`（q1_business）｜GAAP 營業利益率＝40.0 %｜期間與口徑：季末 2026-09-27 季度（公告 2026-10-21）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 newsroom.lamresearch.com 2026-10-21（numbers.latest_quarter_kpis.items[2]，as_of 季末 2026-09-27 季度（公告 2026-10-21））
  - 註記：未查
- `f_kpi5_2026_12`（q1_business）｜下一季指引（2026-12 季）：營收＝8,600±400 百萬美元 百萬美元｜期間與口徑：季末 2026-09-27 季度公告（2026-10-21）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司新聞稿 newsroom.lamresearch.com 2026-10-21（numbers.latest_quarter_kpis.items[5]，as_of 季末 2026-09-27 季度公告（2026-10-21））
  - 註記：未查
- `f_kpi6_eps`（q1_business）｜下一季指引：毛利率／營業利益率／EPS＝毛利率 52.5%±1%；營業利益率 40.5%±1%；EPS $2.33±0.15（GAAP 與 non-GAAP 同）｜期間與口徑：季末 2026-09-27 季度公告（2026-10-21）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司新聞稿 newsroom.lamresearch.com 2026-10-21（numbers.latest_quarter_kpis.items[6]，as_of 季末 2026-09-27 季度公告（2026-10-21））
  - 註記：未查
- `f_kpi7`（q1_business）｜遞延收入＝2660 百萬美元｜期間與口徑：季末 2026-09-27（公告 2026-10-21）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿；不含日本客戶出貨（numbers.latest_quarter_kpis.items[7]，as_of 季末 2026-09-27（公告 2026-10-21））
  - 註記：不適用
- `f_earnings_recency`（q1_business）｜最近一次財報日＝2026-10-21 date｜期間與口徑：2026-10-21／距今 3 個交易日｜kind：realized
  - 來源：—（numbers.earnings_recency，as_of 2026-10-21）
- `f_peer_lrcx_gross_margin_pct`（q2_moat）｜LRCX 毛利率＝50.47 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.LRCX.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_lrcx_operating_margin_pct`（q2_moat）｜LRCX 營業利益率＝35.29 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.LRCX.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_lrcx_fcf_margin_pct`（q2_moat）｜LRCX FCF 利潤率＝21.05 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.LRCX.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_amat_operating_margin_pct`（q2_moat）｜AMAT 營業利益率＝31.09 %｜期間與口徑：TTM ending 2026-07-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.AMAT.operating_margin_pct，as_of TTM ending 2026-07-31（4季加總））
- `f_peer_asml_operating_margin_pct`（q2_moat）｜ASML 營業利益率＝35.42 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ASML.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_klac_operating_margin_pct`（q2_moat）｜KLAC 營業利益率＝41.69 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.KLAC.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_kpi3`（q4_capital）｜自由現金流（營業現金流減資本支出，自算；公司未報）＝3240.0 百萬美元｜期間與口徑：季末 2026-09-27 季度（公告 2026-10-21）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿現金流量表：營業現金流 3,497.7、資本支出含無形資產 257.7；FCF 為自算（numbers.latest_quarter_kpis.items[3]，as_of 季末 2026-09-27 季度（公告 2026-10-21））
  - 註記：未查
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝9.63 USD/share｜期間與口徑：2026-10-24／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261024.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-10-24）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝12.15 USD/share｜期間與口徑：2026-10-24／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261024.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-10-24）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝14.44 USD/share｜期間與口徑：2026-10-24／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261024.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-10-24）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝35389.96 USD m｜期間與口徑：2026-10-24／yfinance revenue_estimate 0y 平均（29 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-10-24）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝42680.21 USD m｜期間與口徑：2026-10-24／yfinance revenue_estimate +1y 平均（28 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-10-24）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝16.87 %｜期間與口徑：2026-07-30 → 2026-10-24／FY1 共識 EPS 8.24 → 9.63（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261024.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-10-24）
- `f_kpi4_sbc_gaap`（q4_capital）｜SBC 占 GAAP 營業利益＝3.5 %｜期間與口徑：季末 2026-09-27 季度（公告 2026-10-21）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：新聞稿 equity-based compensation 114.7 百萬美元 ÷ GAAP 營業利益 3,283.7（自算）；占營收 1.4%（numbers.latest_quarter_kpis.items[4]，as_of 季末 2026-09-27 季度（公告 2026-10-21））
  - 註記：不適用
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝-3701.94 USD m｜期間與口徑：2026-10-24／yfinance 最新一季：總債務 3735.44、現金 7437.38（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-10-24）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝0.482 %｜期間與口徑：2026-10-24／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-10-24）
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝1251.42 m shares｜期間與口徑：2026-10-24／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-10-24）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝230.1 USD｜期間與口徑：2026-10-23（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-10-23（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝23.89 x｜期間與口徑：2026-10-24／分母＝FY1 EPS 9.63，分子＝快照價 230.1｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-10-24）
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝34.29 x｜期間與口徑：2026-10-23（RTH 收盤，UTC）／4 個年度端點內的分位＝37.8｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-10-23（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝37.8 %｜期間與口徑：2026-10-23（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-10-23（RTH 收盤，UTC））
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝-13.92 %｜期間與口徑：2026-10-23（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-10-23（RTH 收盤，UTC））
- `f_rsi14`（q5_valuation）｜RSI(14)＝24.56｜期間與口徑：2026-10-23（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-10-23（RTH 收盤，UTC））
- `f_ev_s_fwd`（q5_valuation）｜EV/S（EV ÷ FY1 共識營收）＝8.03 x｜期間與口徑：2026-10-24／f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）｜kind：estimate
  - 來源：—（numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m，as_of 2026-10-24）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_ps_current`（q5_valuation）｜P/S（現值）＝11.02 x｜期間與口徑：2026-10-23（RTH 收盤，UTC）／4 個年度端點內的分位＝44.1｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-10-23（RTH 收盤，UTC））

### findings_digest 中方向為負或來源衝突的條目（21 條）
- `competitive_share_entrants#1`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K 指出中國本土設備商可能因在地化政策加劇競爭，且美國出口管制使不受限的國際對手取得優勢。
  - 來源：SEC EDGAR 10-K FY2026 Item 1 Business（as_of 2026-08-07）｜affects：moat_trend、decision_inputs.bear
- `competitive_share_entrants#2`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K 風險因子：若無法跟上 AI 需求擴產，可能流失市占。
  - 來源：SEC EDGAR 10-K FY2026 Item 1A Risk Factors（as_of 2026-08-07）｜affects：thesis.R、decision_inputs.bear
- `competitive_share_entrants#4`（competitive_share_entrants｜方向 -｜狀態 ok）：NAURA 2025 年全球設備銷售排名升至第五，中國本土蝕刻/沉積業者擴張。
  - 來源：China Daily via SSE: Three Chinese firms enter world semiconductor industry top 20（as_of 2026-02-04）｜affects：moat_trend、decision_inputs.bear
- `customer_second_source#0`（customer_second_source｜方向 -｜狀態 ok）：10-K 風險因素：Lam 銷售集中於少數大客戶，大客戶可能談判降價、增加成本、壓低毛利並限制技術分享；未見客戶導入第二供應商或自製的具體披露。
  - 來源：SEC EDGAR 10-K FY2026 Item 1A（as_of 2026-08-07）｜affects：decision_inputs.bear、moat_trend
- `customer_concentration_credit#0`（customer_concentration_credit｜方向 -｜狀態 ok）：FY2026 四家客戶分別占總營收約16%、15%、12%、12%；FY2025 兩家約17%、15%；FY2024 一家約17%。
  - 來源：SEC EDGAR LRCX 10-K FY2026 Item 8（as_of 2026-08-07）｜affects：decision_inputs.bear、thesis.R
- `customer_concentration_credit#1`（customer_concentration_credit｜方向 -｜狀態 ok）：2026-06-28 應收帳款五家客戶分別占約20%、16%、15%、11%、10%；呆帳備抵金額不重大。
  - 來源：SEC EDGAR LRCX 10-K FY2026 Item 8（as_of 2026-08-07）｜affects：decision_inputs.bear
- `customer_concentration_credit#3`（customer_concentration_credit｜方向 -｜狀態 ok）：中國區占營收約34%（FY2026）、34%（FY2025）、42%（FY2024），受出口管制影響。
  - 來源：SEC EDGAR LRCX 10-K FY2026 Item 1A（as_of 2026-08-07）｜affects：decision_inputs.bear
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：FY2026 10-K：中國區營收約占總營收 34%（FY2026）、34%（FY2025）、42%（FY2024）；出口許可要求擴大已限制市場、影響營收，未來可能更嚴重。
  - 來源：SEC EDGAR 10-K FY2026 Item 1A（as_of 2026-08-07）｜affects：thesis.R、decision_inputs.bear、valuation
- `reg_tariff_export#1`（reg_tariff_export｜方向 -｜狀態 ok）：FY2026 10-K：美國對鋼、鋁進口課關稅推高 FY2026 製造成本，壓低毛利；部分國際銷售依賴取得出口許可。
  - 來源：SEC EDGAR 10-K FY2026 Item 1A（as_of 2026-08-07）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#2`（reg_tariff_export｜方向 -｜狀態 ok）：FY2026 10-K：客戶及下游業者亦可能受關稅、出口管制影響，進而衝擊對公司產品的需求。
  - 來源：SEC EDGAR 10-K FY2026 Item 1A（as_of 2026-08-07）｜affects：thesis.R、triggers
- `reg_tariff_export#3`（reg_tariff_export｜方向 -｜狀態 ok）：2026 年 4 月美國國會推進 MATCH Act，擬收緊對中國晶片廠的先進蝕刻／沉積設備出口管制，Lam 被點名於討論中。
  - 來源：Simply Wall St 轉述（as_of 2026-05-18）｜affects：thesis.R、triggers
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：FY2015 10-K 揭露：部分元件與次組件僅能向單一或少數供應商採購（歷史揭露，非最新）
  - 來源：Lam Research Form 10-K FY2015 (SEC)（as_of 2015-08-01）｜affects：decision_inputs.bear、thesis.R
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：中國相關營收約占 34%，美國出口許可限制已影響營收並加劇外國競爭
  - 來源：Lam Research Form 10-Q (SEC)（as_of 2026-10-22）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#2`（geo_supply_chain｜方向 -｜狀態 ok）：公司預期 2026 年中國占比降至 30% 以下，因新增對部分中國客戶出貨限制
  - 來源：Zacks（as_of 2026-01-30）｜affects：thesis.R、valuation
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：Lam 10-K 列出技術快速變遷為風險：公司須持續開發新產品以因應製程技術變化，產品若在市場失敗或不及競品改良版，可能損失市占；10-K 未點名具體替代技術。
  - 來源：SEC EDGAR 10-K FY2026 Item 1A Risk Factors（as_of 2026-08-07）｜affects：moat_trend、decision_inputs.bear
- `substitute_technology#1`（substitute_technology｜方向 -｜狀態 ok）：10-K 產品集中風險項下列有「技術變化我們無法因應」與「競爭對手改良版產品」等情境。
  - 來源：SEC EDGAR 10-K FY2026 Item 1A Risk Factors（as_of 2026-08-07）｜affects：moat_trend、decision_inputs.bear
- `cyclical_supply_discipline_capacity#2`（cyclical_supply_discipline_capacity｜方向 -｜狀態 ok）：同業 Applied Materials CFO 稱目標 2028 年前將季度半導體系統產出倍增，並規劃進一步擴產以支應至 2030 年需求；Tokyo Electron 2026 年 1 月報導 FY26 資本支出上調 48% 創高。搜尋未找到任何明示『供給紀律』的陳述。
  - 來源：Dow Jones via iTiger; TrendForce News（as_of 2026-01-31）｜affects：decision_inputs.bear、thesis.R
- `cyclical_supply_discipline_capacity#3`（cyclical_supply_discipline_capacity｜方向 -｜狀態 ok）：Tokyo Electron FY26 資本支出上調 48%
  - 來源：TrendForce News（as_of 2026-01-09）｜affects：decision_inputs.bear
- `cyclical_prior_downcycle_behavior#0`（cyclical_prior_downcycle_behavior｜方向 -｜狀態 ok）：SEMI：2001 年全球設備出貨額 281 億美元，較 2000 年 477 億美元下滑約 41%
  - 來源：SEMI: Worldwide equipment market dropped $28 billion in 2001 (Semiconductor Digest)（as_of 2002-03-01）｜affects：decision_inputs.bear、valuation
- `cyclical_prior_downcycle_behavior#1`（cyclical_prior_downcycle_behavior｜方向 -｜狀態 ok）：Lam 2023 年 3 月季 GAAP 毛利率 41.5%（去年同期 44.7%），為該輪下行低點；FY2023 全年 44.6%，FY2022 45.7%
  - 來源：Motley Fool 2023-04-25；Lam 10-K FY2023（as_of 2023-08-15）｜affects：decision_inputs.bear、valuation
- `cyclical_prior_downcycle_behavior#3`（cyclical_prior_downcycle_behavior｜方向 -｜狀態 ok）：Lam 出貨量 2000 年 12 月至 2001 年 12 月下滑 80%；設備營收 1998-2002 峰谷下滑 67%
  - 來源：Machine Design, Semicon West show conditions much worse than 2001（as_of 2001-07-01）｜affects：decision_inputs.bear

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 4 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/LRCX_20261024/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":516.0,"bear_5y_price":142.5,"p_bull_pct":25,"p_bear_pct":30,"upside_5y_pct":26.0,"ev5y_pct":31.4,"irr_base_pct":4.7,"asym_ratio":2.7,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":9.63,"pe":23.89,"basis":"FY1（2027 年 6 月年度）共識 EPS；終端倍數同樣以前瞻一年的年度 EPS 為分母"},"eps":{"bull":[10.2,14.0,17.0,19.0,21.5],"base":[9.6,12.0,13.2,12.0,14.5],"bear":[9.0,9.0,6.5,7.5,9.5]},"pe":{"bull":24,"base":20,"bear":15},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0.482,"net_buyback":2.0},"second_stage":{"bull_cagr_pct":10,"base_cagr_pct":6},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### LRCX_Q4_2026_Earnings_Call_20260729.md
- 2026-07-29｜CFO｜guidance：9月季營收財測 81 億美元，區間正負 4 億（原話："$8.1 billion, plus or minus $400 million"）
- 2026-07-29｜CFO｜guidance：9月季毛利率財測 52%（正負 1 個百分點）（原話："gross margin of 52%, plus or minus 1 percentage point"）
- 2026-07-29｜CFO｜guidance：9月季營業利益率財測 39.5%（原話："operating margins of 39.5%, plus or minus 1 percentage point"）
- 2026-07-29｜CFO｜guidance：9月季 EPS 財測 2.15 美元（原話："earnings per share of $2.15, plus or minus $0.15"）
- 2026-07-29｜CFO｜guidance：9月季費用成長速度低於營收成長（原話："albeit at a much slower rate than the growth in revenue"）
- 2026-07-29｜CEO｜guidance：2026 年 WFE 展望為 1,500 億美元出頭（原話："WFE, to be in the low $150 billion range"）
- 2026-07-29｜CEO｜guidance：澄清：本季 WFE 展望未再說有上檔偏向（原話："We didn't say upside bias for this current outlook."）
- 2026-07-29｜CFO｜guidance：2027 年不給數字，只說看起來是很好的一年（原話："quantification around what '27 is going to be."）
- 2026-07-29｜CEO｜guidance：2027 年成長動能排序：DRAM、先進邏輯、NAND（原話："we still see DRAM being the fastest grower"）
- 2026-07-29｜CEO｜guidance：先進封裝 2026 年成長預期超過 70%（原話："deliver greater than 70% year-on-year growth"）
- 2026-07-29｜CFO｜guidance：稅率預期 9 月季升至中段十幾個百分點（原話："rate will be in the mid-teens in the September quarter"）
- 2026-07-29｜CFO｜guidance：服務事業下季輪廓與本季相近，不給數字（原話："similar profile of what we saw this quarter"）
- 2026-07-29｜CFO｜margin：FY2026 營收 232 億美元創高（原話："record revenue of $23.2 billion"）
- 2026-07-29｜CFO｜margin：本季毛利率超出財測上緣，原因含調價（原話："a myriad of factors, including pricing actions"）
- 2026-07-29｜CFO｜margin：管理層稱近期毛利率可維持 51%–52%（原話："we're in that 51%, 52% range right now"）
- 2026-07-29｜CFO｜margin：長期目標：毛利率中 50% 水準（原話："we intend to drive gross margins to the mid-50% level"）
- 2026-07-29｜CFO｜margin：達成中 50% 毛利率需數年（原話："take several years, I think, to get to those levels"）
- 2026-07-29｜CFO｜margin：SAM 占 WFE 比重今年約 36%–36.5%（原話："36%, 36.5% this year, something like that"）
- 2026-07-29｜CEO｜product：SAM 比 2025 投資人日設定的時程更快接近高 30%（原話："faster than what we had outlined at our 2025 Investor Day"）
- 2026-07-29｜CEO｜product：NAND 每片晶圓 SAM 由 128 層到 500 層以上將倍增（原話："SAM per wafer in NAND to double from the 128-layer node"）
- 2026-07-29｜CEO｜product：Akara 裝機量逐年倍增（原話："Akara's installed base has doubled every year"）
- 2026-07-29｜CEO｜product：VECTOR 硬遮罩方案對客戶成本節省（原話："offers over 20% cost savings to customers"）
- 2026-07-29｜CEO｜product：今年將出貨首台 310x310 毫米面板設備（原話："we will also ship our first 310x310-millimeter panel tool"）
- 2026-07-29｜CFO｜customer：NAND 營收季增超過一倍（原話："NAND revenue dollars more than doubled sequentially"）
- 2026-07-29｜CFO｜customer：遞延收入增加主因是客戶預付款（原話："the largest of which was customer downpayments"）
- 2026-07-29｜CFO｜customer：中國整體 WFE 持平到微升（原話："China overall WFE is flat to slightly up"）
- 2026-07-29｜CEO｜customer：美國新邏輯客戶：僅表示有接洽（原話："we're engaged"）
- 2026-07-29｜CEO｜customer：客戶已在談 2027 年以後的設備訂位（原話："the discussions are now out in the '27 and beyond"）
- 2026-07-29｜CEO｜risk：交期具挑戰性（原話："lead times are challenging"）
- 2026-07-29｜CEO｜risk：NAND 2028 年展望：認為現在談還太早（原話："I think it's a little early on 2028"）
- 2026-07-29｜CFO｜risk：產業供給仍不足，延續到明年（原話："the industry is undersupplied this year"）
- 2026-07-29｜CFO｜competition：資料中心資本支出對應 WFE 的比率比先前估計高（原話："trending, I don't know, $1 billion or $2 billion higher"）
- 2026-07-29｜CEO｜competition：清潔設備：不回答是否為第一（原話："I don't know about the #1 player"）
- 2026-07-29｜CFO｜capital_allocation：資本支出管理在營收 4%–5%（原話："manage the company to 4% to 5% of revenue"）
- 2026-07-29｜CFO｜capital_allocation：股東回饋承諾：至少 85% 自由現金流（原話："plans remain to return at least 85% of free"）
- 2026-07-29｜CEO｜commitment：連續第三年優於 WFE（原話："third consecutive year of relative outperformance to WFE"）
- 2026-07-29｜CFO｜commitment：不提供逐季指引（原話："not going to guide you quarter by quarter through next year"）

### 問答異常語氣（迴避／改口／保留）
- LRCX_Q4_2026_Earnings_Call_20260729.md｜問：Malik：NAND 明年是否有供過於求跡象｜答法：未直接回答是否供過於求，改談 2028 還早、Lam 不只靠 NAND
- LRCX_Q4_2026_Earnings_Call_20260729.md｜問：Rasgon：產能不受限下 2027 能否給數字／逐季成長｜答法：兩次都拒絕給數字，只說每季都感覺更好
- LRCX_Q4_2026_Earnings_Call_20260729.md｜問：Blayne Curtis／Schneider：同類產品的調價狀況｜答法：不談同類比較的價格，只重述調價是多項因素之一
- LRCX_Q4_2026_Earnings_Call_20260729.md｜問：Pajjuri：WFE 1,500 億是否有上檔偏向｜答法：修正自己準備稿的說法：本季未再說上檔偏向

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 5 | 2 |
| customer_second_source | found | 1 | 2 |
| customer_concentration_credit | found | 4 | 1 |
| supply_demand_durability | found | 5 | 4 |
| regulatory_antitrust | found | 1 | 3 |
| reg_tariff_export | found | 4 | 1 |
| geo_supply_chain | found | 3 | 2 |
| end_markets | found | 4 | 4 |
| substitute_technology | found | 2 | 2 |
| channel_business_model_shift | none | 0 | 2 |
| capital_markets_pricing | found | 5 | 4 |
| major_events | found | 1 | 5 |
| cyclical_supply_discipline_capacity | found | 4 | 3 |
| cyclical_inventory_price_position | found | 2 | 3 |
| cyclical_prior_downcycle_behavior | found | 4 | 3 |

未涵蓋／不適用軸的查詢詞原文（供判相關性）：
- **channel_business_model_shift**（none）：Lam Research business model shift services subscription OR platform OR channel 2026；Lam Research go-to-market change distribution 2026

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260730","verdict":"進場","role":"衛星","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"AI 驅動的晶圓廠設備支出上行延續至 CY2027，且 DRAM 與 NAND 需分開承保——DRAM 結構性緊、NAND 有轉鬆風險"},{"id":"H2","text":"Lam 的可服務市場占產業設備支出比重持續上升，第三／第四年連續跑贏產業——蝕刻與沉積強度隨 3D 化結構性上行"},{"id":"H3","text":"倍數正常化「部分完成」，但未完成——盈餘成長須跑贏仍在進行中的估值下修"}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"NAND 供需 2027 轉鬆，帶動記憶體設備支出見頂——TrendForce 於 2026-07-27 明確預估 2027 NAND 轉向寬鬆、價格承壓，主因新產能上線疊加超高層數轉換，而終端消費需求疲弱。Lam 本季 NAND 系統營收季增逾一倍、占系統營收 23%（自 12%），正是最曝險的一段。"},{"id":"R2","text":"中國出口管制在 Lam 自己的品項上收緊——50% 關聯方規則（2025-09-29 實施）已實證造成 2025 年 12 月季約 $200M 營收衝擊，其一年暫緩約於 2026-10-30 到期；MATCH Act 2026 修訂針對低溫蝕刻設備（Lam 核心品項），現收窄為五家具名中國實體。同時中國國產設備在成熟節點持續替代：中微被稱全球第二大蝕刻商，中國廠商合計占全球設備市場自 2024 年 5.6% 升至 2025 年 6.5%。"},{"id":"R3","text":"倍數繼續向中樞回歸而盈餘未同步成長——30.85x 相對長窗中位 19.1x 溢價 61%（近五年中位 16.9x，溢價 83%）。若 2027 設備支出僅持平而非成長，倍數與盈餘同時修正即為戴維斯雙殺。"}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"加碼待兩約束同時解除：10月法說CY2027 WFE≥$180B且NAND合約價未連2季跌；且關聯方規則到期處置明朗（衝擊<$150M/季）。獨立分支：價格≤$200且R1未觸發","irr_base_pct":7.4,"ev5y_pct":32.9,"drift_watch_prior":{"dca_verdict":"進場","dca_role":"衛星","signal":"B","val":"🟡","ma":"✅","trap":"🟡","moat_trend":"↑","runway_post_y5":"🟢","asym_ratio":2.0,"ev5y_pct":32.9,"irr_base_pct":7.4,"max_dd_pct":-60.0,"bull_5y_price":553.5,"bear_5y_price":119.0,"p_bull_pct":26.0,"p_bear_pct":30.0,"rearm_trigger":"加碼待兩約束同時解除：10月法說CY2027 WFE≥$180B且NAND合約價未連2季跌；且關聯方規則到期處置明朗（衝擊<$150M/季）。獨立分支：價格≤$200且R1未觸發","price_at_dd":252.35,"archetype":"循環/商品","cycle_position":"中循環"}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"LRCX","date":"2026-10-24","schema":"v15.2","contract":"v19","company_name":"Lam Research"},"oneliner":"AI 推動 2027 年晶圓設備支出逾 2,000 億美元，Lam 蝕刻沉積強度與份額同步上升；股價半年跌 14% 而共識上修 17%，但利潤率已在循環高檔，出口管制與 2028 年降溫是兩大風險。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/LRCX_20261024/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/LRCX_20261024/scenario.json","answers":{"q1_business":{"verdict":"賺晶圓廠擴產與製程升級的錢：蝕刻與沉積設備約七成、裝機服務與升級約三成；錢卡在每一代 3D 結構與先進封裝都需要更多蝕刻沉積步驟這一節點。","reasoning":"9 月季營收 82.2 億美元（季增 22%、年增 54%），non-GAAP 毛利率 52.4%、營業利益率 40.2%，均創新高；12 月季指引 86 億±4 億美元、EPS 2.33 美元，CFO 表示零組件吃緊壓低指引，延後的出貨移到 3 月季。系統營收組合：記憶體 46%（NAND 26%、DRAM 20%）、晶圓代工 46%、邏輯及其他 8%；地區：中國 35%、韓國 20%、台灣 18%。服務事業單季近 25 億美元、年增 40%。景氣處擴張期：公司估 CY2026 WFE 約 1,550 億美元、CY2027 逾 2,000 億美元，客戶需求能見度到 2028 年，今年受潔淨室限制、明年再加上零組件。產業態勢為雙向拉鋸：結構面轉好（3D 化、先進封裝、背面供電推高蝕刻沉積強度），對上競爭面（應材目標倍增產出、東京威力擴產、中國本土廠升級）與出口管制。單點依賴：前四大客戶 FY2026 占營收約 55%，中國約 34%，屬集中度風險，不當護城河證據。","fact_refs":["f_kpi0_gaap","f_kpi1_non_gaap","f_kpi2_gaap","f_kpi5_2026_12","f_kpi6_eps","f_kpi7","f_earnings_recency"],"verdict_values":{"revenue_quality":"設備營收隨客戶資本支出循環，屬一次性；約三成服務、零件與升級收入跟裝機量和稼動率連動，較穩定（CY2026 預期成長逾 30%、CY2027 逾 15%）。遞延收入 26.6 億美元，季增 2.27 億，但客戶預付款減少。","unit_econ_note":"毛利率 52.4% 來自客戶與產品組合、新產品（Akara、Aether）、就近客戶製造與調價；稅率由 6 月季 11% 升至 16.5% 並將延續，每股盈餘多一層壓力。","archetype":{"primary":"循環/商品","secondary":"品質複利成長","confidence":"中","fingerprint":"營收隨 WFE 擺動（FY2024 年減 14.5%），但近四年無虧損、2023 年谷底毛利率仍有 41.5%，裝機服務收入提供底部。"},"industry":{"clock_phase":"II","sd_verdict_source":"週期性將反轉，但本輪被潔淨室與零組件供給限制拉長：SEMI 估 WFE 2027 年增 21.8%、2028 年增 14.1%，成長率 2028 年起放緩；設備同業大幅擴產，下一輪供給可逆性高。","bargaining":{"up":"零組件供應商短期議價力上升：12 月季指引因供給吃緊而保守，分析師指出應付帳款增加約 13 億美元。","down":"四家客戶占 FY2026 營收約 55%，10-K 明言大客戶可壓價並限制技術分享。","geo":"中國占營收 34%–35%，出貨須取得美國出口許可，管制擴大會直接縮小可服務市場。"},"profit_pool_dir":"利潤池往蝕刻沉積移動：3D NAND、背面供電、先進封裝與乾式光阻使 Lam 的 SAM 占 WFE 過去幾年擴大約 4 個百分點。","tam_table":[{"item":"CY2026 WFE（公司展望）","value":"約 1,550 億美元（2026-10-21 法說；7 月為 1,500 億出頭）"},{"item":"CY2027 WFE（公司初步）","value":"逾 2,000 億美元，成長以 DRAM 領先，其次先進邏輯與 NAND；為供給受限下的數字"},{"item":"SEMI 2028 設備總銷售","value":"2,295 億美元；WFE 2027 年增 21.8%、2028 年增 14.1%"},{"item":"Lam SAM 占 WFE","value":"2025 年約 35%，2026 年約 36%–36.5%，目標接近 40%"},{"item":"先進封裝","value":"2026 年成長逾 70%；面板級電鍍設備已出貨逾 20 家客戶"}]}}},"q2_moat":{"verdict":"護城河擴大（↑）：蝕刻龍頭、NAND 最大裝機量，SAM 占比與份額同步上升，連續第三年跑贏 WFE；等級 B，威脅集中在中國本土替代與同業擴產。","reasoning":"機制是製程指定機台：新節點的蝕刻沉積步驟一旦在客戶產線驗證通過便進入量產配方，換供應商要重新認證；裝機量再帶出升級、零件與服務收入。方向證據：SAM 占 WFE 擴大約 4 個百分點，2026 年為連續第三年跑贏 WFE；本季在一家領先客戶的背面供電四項產品全拿下指定機台，乾式光阻累計營收預期上調約 10 億美元至約 25 億美元（2026-10-21 法說，CEO）。事實表只有同業利潤率，無 ROIC 差距：Lam 營業利益率高於應材、與 ASML 相當、低於 KLA。執行力給 8 分（連五季營收新高、指引全數達成），定價力給 7 分（毛利率新高且有調價，但四家客戶占營收過半、可壓價）。當期報酬：高利益率、低資本支出強度；增量報酬約 138%、再投資率約 11.5%，內生成長上界約 16%。","fact_refs":["f_peer_lrcx_gross_margin_pct","f_peer_lrcx_operating_margin_pct","f_peer_lrcx_fcf_margin_pct","f_peer_amat_operating_margin_pct","f_peer_asml_operating_margin_pct","f_peer_klac_operating_margin_pct","f_kpi1_non_gaap","f_kpi3"],"verdict_values":{"moat":{"mechanism":"製程指定機台綁定：每一代 3D 結構的蝕刻沉積配方在客戶產線驗證後難以替換，加上業界最大的 NAND 裝機量帶來升級與零件服務收入。","execution":8,"pricing":7,"grade":"B","trend":"↑","trend_evidence":"SAM 占 WFE 擴大約 4 個百分點、2026 年連續第三年跑贏 WFE；背面供電四項產品在一家領先客戶取得指定機台；乾式光阻已在 HBM 量產並上調累計營收預期約 10 億美元（2026-10-21 法說，CEO）。事實表未見最大客戶份額下滑的證據。","competitor_notes":[{"name":"Applied Materials","strategy_note":"沉積與蝕刻的主要對手，產品線最廣；CFO 目標 2028 年前季度系統產出倍增，是擴產最積極的一家，下行時價格競爭會從這裡開始。"},{"name":"Tokyo Electron","strategy_note":"蝕刻正面對手，押注 DRAM 蝕刻需求、FY26 資本支出上調 48%；DRAM 是 2027 年成長最快的一段，衝突最直接。"},{"name":"ASM International","strategy_note":"ALD／PECVD 對手，閘極全環繞世代 ALD 份額的主要競爭者，Lam 稱在這一段取得份額。"},{"name":"NAURA（北方華創）","strategy_note":"2025 年全球設備銷售升至第五，受在地化政策支持，在中國成熟節點蝕刻沉積逐步替代 Lam。"},{"name":"KLA","strategy_note":"檢測量測為主，與 Lam 不直接競爭；利潤率為同業最高，作為設備業利潤率上限的參照。"}],"peer_na_reason":"事實表只有同業利潤率，沒有投入資本口徑，ROIC 差距無法計算；以營業利益率代替比較。東京威力營收缺漏，無法算利潤率。","threats":[{"level":"🟡","text":"中國本土設備商在在地化政策下擴張，NAURA 升至全球第五；在中國成熟節點逐項產品替代，屬區域點對點競爭，尚未進入先進節點。","p":"35%","evidence_refs":["competitive_share_entrants#1","competitive_share_entrants#4"]},{"level":"🟡","text":"同業大舉擴產（應材產出倍增、東京威力資本支出上調 48%），景氣下行時設備供給過剩，價格與份額競爭加劇。","p":"30%","evidence_refs":["cyclical_supply_discipline_capacity#2"]},{"level":"🟡","text":"製程技術快速變遷，若新世代機台不及對手改良版會失去份額；10-K 未點名具體替代技術，目前 3D 化方向反而推升蝕刻沉積強度。","p":"15%","evidence_refs":["substitute_technology#0","substitute_technology#1"]}],"roic_durability":{"quadrant":"高利益率×高周轉（周轉率事實表未涵蓋，以低資本支出強度與自由現金流利潤率推斷）","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者是晶圓廠製程工程、決策者是客戶資本支出委員會、付款者同為晶片廠，三角色一致；製程升級是需要而非想要，但時點可延後：FY2024 營收年減 14.5%、2023 年谷底毛利率 41.5%，顯示需求會遞延。公司引述每週 token 用量 18 個月約增 250 倍，支撐需求基礎值。"},{"item":"決策層級","level":"🟢","text":"替代性要在單一製程步驟衡量：新節點的蝕刻沉積步驟選定機台後即寫入量產配方，換供應商要重新認證；本季在一家領先客戶的背面供電四項產品全拿下指定機台，乾式光阻在 HBM 量產被指定。"},{"item":"價值鏈分配","level":"🟡","text":"四家客戶占 FY2026 營收約 55%、五家占應收帳款約 72%，買方集中可壓價；但毛利率升至 52.4% 且有調價，現階段 Lam 分到的比重在增加。上游零組件吃緊，供應商短期議價力上升。"},{"item":"社會容忍度","level":"🟡","text":"價格不是社會議題，政治上限在出口：中國營收約 34% 依賴美國出口許可，法源為出口管制規則與國會法案（MATCH Act 討論中點名 Lam），政策可在短時間改變可服務市場。"}],"roiic":"約 138%（FY2023→FY2026 營業利益增加約 29.8 億美元，以 11%–16.5% 稅率計稅後約 25–27 億；同期累計再投資約 18.9 億美元）","reinvest_rate":"約 11.5%（三年累計再投資 18.9 億÷累計淨利 164.5 億美元）","endo_ceiling":16,"formula_note":"事實表未涵蓋投入資本口徑。再投資以每年淨利減自由現金流近似（含資本支出減折舊與營運資金變動，三年無併購），淨利代替稅後營業利益（淨現金公司差異小）。上行段營運槓桿讓增量報酬偏高，不代表下一輪；內生上界約 16%。"}}}},"q3_growth":{"verdict":"跑道寬（🟢）：WFE 2027 年逾 2,000 億美元，另有先進封裝、背面供電、面板級封裝、NAND 分層儲存等新曲線；但共識三年 EPS 年複合約 36%，遠高於內生上界約 16%，差距靠循環上行的營運槓桿與利潤率擴張。","reasoning":"成長以量為主（WFE 擴張加 SAM 占比上升），價與組合為輔（毛利率朝中 50% 推進、調價），淨回購每年約 2%（稀釋股數由 FY2023 約 13.6 億降至 FY2026 約 12.6 億，以淨利÷EPS 推得）。共識三年 EPS 年複合：FY2026A 5.76 美元→FY2029E 14.44 美元，(14.44÷5.76)^(1/3)−1≈35.9%。缺口約 20 個百分點：營業利益率由 TTM 35.3% 升到指引 40.5% 與循環量能是主因，淨回購貢獻約 2 個百分點，其餘屬循環性、無法歸給可延續的再投資，長期信心上限為中。衰退訊號亮 1 個：共識 FY2026→FY2028 EPS 年複合約 45% 高於營收年複合約 35.5%，差距約 10 個百分點；FY2026 自由現金流÷淨利 0.67 只一年，未亮。長期成長性 🟡、價值陷阱風險 🟡。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_consensus_rev_3m_fy1_pct"],"verdict_values":{"growth":{"driver_mix":"量（WFE 擴張＋SAM 占比上升）為主、價與組合為輔、淨回購每年約 2%，無併購。","runway_years":"不適用（以 SAM 占 WFE 比重衡量，非滲透率）","runway_post_y5":"🟢","endo_ceiling_basis":"引護城河段：增量報酬約 138%×再投資率約 11.5%≈16%；本輪營運槓桿灌水，下一輪不保證。","segments":[{"item":"記憶體系統營收","value":"9 月季占系統 46%，金額年增 120%；NAND 季增約 40%（轉 256 層以上、初步 384 層），DRAM 創新高"},{"item":"晶圓代工","value":"占系統 46%，創新高；先進節點、先進封裝與中國成熟節點帶動"},{"item":"邏輯及其他","value":"占系統 8%，以先進節點為主"},{"item":"服務事業（CSBG）","value":"單季近 25 億美元、年增 40%；CY2026 成長逾 30%、CY2027 逾 15%"}],"decay_signals":[{"signal":"毛利率連 2 季年減","lit":false,"note":"9 月季 52.4% 創新高"},{"signal":"核心市占近 12 個月縮減","lit":false,"note":"SAM 占比與份額上升"},{"signal":"提價後銷量下滑","lit":false,"note":"量價齊升"},{"signal":"EPS 年複合高於營收年複合逾 5 個百分點","lit":true,"note":"共識 FY2026→FY2028 EPS 約 45%、營收約 35.5%"},{"signal":"自由現金流÷淨利 <0.75 連 2 年","lit":false,"note":"FY2026 0.67、FY2025 1.01，僅一年"},{"signal":"SBC÷營收 >5% 且上升","lit":false,"note":"約 1.4%"},{"signal":"TAM 萎縮或被替代","lit":false,"note":"WFE 擴張中"},{"signal":"產業倍數近 3 年系統性下移","lit":false,"note":"事實表未涵蓋"},{"signal":"維持性資本支出占自由現金流 >60%","lit":false,"note":"9 月季資本支出 2.58 億對自由現金流 32.4 億"},{"signal":"停止投資新產能且收入 3 年內下滑","lit":false,"note":"持續擴廠與研發實驗室"}],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"資本配置中上：無併購、股權酬勞稀釋極低、股數逐年下降；但 9 月季只回饋自由現金流 41%，現金累積到 75 億美元。","reasoning":"9 月季自由現金流 32.4 億美元創新高（營業現金流 35.0 億減資本支出 2.58 億），回購約 10 億、股息 3.25 億，另進行中的加速回購延續到 12 月季；年初至今回饋 59%，並償還 7.5 億到期債。股權酬勞單季 1.15 億美元，占營收 1.4%，對 2,880 億美元市值每年稀釋約 0.16%，遠低於 1.5%；稀釋股數 FY2023→FY2026 約減 7%。回購買入收益率無法驗：回購均價與 10 年期殖利率事實表未涵蓋，以現價計前瞻盈餘殖利率約 4.2%。近 12 個月無併購。淨現金約 37 億美元。FY2026 自由現金流÷淨利 0.67（存貨與擴產），9 月季已回升。","fact_refs":["f_kpi3","f_kpi4_sbc_gaap","f_net_debt_m","f_dividend_yield_ttm","f_shares_diluted_m"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":false,"passed":null,"input":"近 12 個月 8-K 無併購項目，搜尋亦無 2025–2026 併購"},{"name":"buyback_yield","applicable":true,"passed":null,"input":"回購均價與 10 年期殖利率事實表未涵蓋；現價前瞻盈餘殖利率約 4.2%（9.63÷230.1）"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"股權酬勞年化約 4.6 億美元÷市值約 2,880 億≈0.16%/年，且稀釋股數逐年下降"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購，近 12 個月無併購；股東回饋以回購與股息為主，已在計分卡與理由段交代，現金去向四分（回購、股息、償債、增加現金）見理由段。"}}}},"q5_valuation":{"verdict":"現價要求 FY2028 年 EPS 站上 12 美元且下一輪下行不深於 2023 年；2027 年我們相信，2028 年後的循環深度不確定，估值中性。","reasoning":"股價 230.1 美元，前瞻本益比 23.9 倍（FY1 EPS 9.63）、FY2 約 18.9 倍、trailing 34.3 倍；26 週跌 13.9%、RSI 24.6，同期 FY1 共識三個月上修 16.9%，倍數壓縮全數抵銷盈餘上修。trailing 本益比在 4 個年度端點內分位 37.8%，非五年分位，五年分位事實表未涵蓋。PEG 以共識三年 EPS 年複合 35.9% 計約 0.67，但這是循環回升的成長率，不能當便宜依據；改用 FY1→FY3 年複合約 22.5% 則約 1.06。分母處循環高檔、利潤率創新高，前瞻倍數對近峰盈餘不算便宜。基準 5 年終端 20 倍×FY2031E 14.5 美元≈290 美元，較現價約 +26%；一年以 FY2 12.15 美元×20 倍≈243 美元，約 +5.6%。同業本益比事實表未涵蓋，終端倍數只能對照自身現值 23.9 倍。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_pe_current","f_pe_percentile","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_3m_fy1_pct","f_week26_return_pct","f_rsi14","f_ev_s_fwd","f_ps_current"],"verdict_values":{"valuation":{"basis":"前瞻本益比（FY1，2027 年 6 月年度）","tier":"大型前段設備龍頭","peers":{"expanded":false,"reason":"事實表只有同業利潤率，無同業本益比或目標價的結構化數字，無法做倍數對照；終端倍數以自身前瞻 23.9 倍為對照。"},"fwd_pe":23.89,"peg":0.67,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"前瞻 23.9 倍、FY2 約 18.9 倍；利潤率歷史最高、盈餘處循環上段，倍數對近峰盈餘不算便宜，也未過熱。五年分位事實表未涵蓋，僅 4 個年度端點分位 37.8%。基準 5 年約 +26%、一年約 +6%，報酬中等偏弱，結論中性。","upside_short_pct":5.6,"upside_mid_pct":26.0,"denominator_disputed":false,"denominator_note":"分母無一次性項目：稅率升至 16.5% 已反映在指引，12 月季供給延後屬時點移轉。循環高檔盈餘的風險放在空頭機率與終端倍數處理，不靠分母修正。"}}},"q6_how_wrong":{"verdict":"最可能看錯在循環轉折時點：2027 年是供給受限下的高點，2028 年 WFE 成長放緩、同業大舉擴產，一旦記憶體客戶縮手，EPS 與倍數會同時下修。","reasoning":"設備業下行史：2001 年全球設備出貨年減 41%，Lam 出貨峰谷跌 80%；2023 年谷底毛利率 41.5%。本輪客戶擠潔淨室、提前專案（CFO 原話），2027 年部分需求是提前拉貨。第二條路是中國：9 月季中國占 35%，12 月季將明顯下降，出口管制擴大會把這塊直接拿掉。第三條是倍數：前瞻 23.9 倍若在 2027 年 WFE 持平時回到循環中段，股價與盈餘同跌。陷阱評估 🟡：不是價值陷阱，而是高點陷阱風險。","fact_refs":["f_kpi5_2026_12","f_kpi6_eps","f_fwd_pe_latest","f_week26_return_pct"],"verdict_values":{"trap":{"verdict":"🟡","label":"循環高點風險：獲利在高檔，非價值陷阱"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":9.63,"pe":23.89,"basis":"FY1（2027 年 6 月年度）共識 EPS；終端倍數同樣以前瞻一年的年度 EPS 為分母"},"eps":{"bull":[10.2,14.0,17.0,19.0,21.5],"base":[9.6,12.0,13.2,12.0,14.5],"bear":[9.0,9.0,6.5,7.5,9.5]},"pe":{"bull":24,"base":20,"bear":15},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0.48,"net_buyback":2.0},"second_stage":{"bull_cagr_pct":10,"base_cagr_pct":6},"max_dd":{"lo":-60,"hi":-40,"basis":"設備業下行史：2001 年全球設備出貨年減 41%、Lam 出貨峰谷跌 80%；2023 年谷底毛利率 41.5%。淺循環：EPS 自高點回落約 20%、前瞻倍數由 23.9 倍壓到 18 倍，股價約 −40%；深循環：EPS 回落約 40%、倍數壓到 15 倍，約 −62%。取 −40%～−60%。","trigger_time":null},"basis":{"bull":"WFE 2027 年逾 2,100 億、2028 年續增，SAM 占比接近 40%，毛利率到中 50%，下行淺；FY2031E EPS 21.5 美元、終端 24 倍（約等於現價前瞻倍數）。","base":"2027–28 年大致依共識成長，FY2030 出現一次約 −9% 的循環修正後回升；FY2031E EPS 14.5 美元、終端 20 倍（低於現價，循環中段倍數）。","bear":"供給受限與中國管制壓縮 2027–28 年，2029 年記憶體與代工同時縮手，EPS 跌回約 6.5 美元後部分回升；終端 15 倍。"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"SEMI 估 WFE 2028 年成長放緩至 14.1%；應材目標產出倍增、東京威力資本支出上調 48%；2001 年設備出貨年減 41%、Lam 出貨峰谷跌 80%，2023 年谷底毛利率 41.5%。","assumption":"2027 年逾 2,000 億美元的 WFE 中有客戶提前拉貨與擠潔淨室的成分，AI 資本支出一旦放緩，2028–29 年 WFE 下修 20%–30%。","consequence":"EPS 自高點回落 30%–40%、倍數壓到 15 倍，股價較現價跌 50%–60%，五年後仍虧損。","ruling":"採納為空頭情境主軸，空頭機率 30%；與唯一致命點（出口管制）不同源，屬獨立的第二條失敗路徑。","watch":"每季營收指引中點是否季減、SEMI 2028 年預測修正方向、記憶體客戶資本支出指引。","evidence_refs":["cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#3","cyclical_supply_discipline_capacity#2","cyclical_supply_discipline_capacity#3"],"fact_refs":["f_kpi5_2026_12"]},{"view":"論點失敗","evidence":"10-K 列出若無法跟上 AI 需求擴產可能流失份額；12 月季指引因零組件吃緊而保守；FY2015 年報揭露部分元件只能向單一或少數供應商採購（舊揭露，本季法說證實零組件仍是瓶頸）。","assumption":"零組件瓶頸持續到 2027 年，客戶轉向有貨的對手。","consequence":"份額論點受損，跑贏 WFE 的紀錄中斷。","ruling":"暫時反駁：CEO 稱與疫情短缺不可比、很快追上，延後出貨移到 3 月季；但列為短期風險，3 月季驗證。","watch":"3 月季營收是否高於 12 月季實績、存貨與應付帳款變化。","evidence_refs":["competitive_share_entrants#2","geo_supply_chain#0"],"fact_refs":["f_kpi5_2026_12"]},{"view":"論點成功但股東經濟變差","evidence":"鋼鋁關稅推高 FY2026 製造成本；稅率由 11% 升至 16.5% 並延續；營業費用增加主因獎酬；FY2026 自由現金流利潤率由 29.4% 降至 21.1%；大客戶可壓價；未來五年逾 30 億美元研發實驗室與 15 億美元奧勒岡擴建。","assumption":"營收照預期成長，但成本、稅率與擴產資本吃掉一部分盈餘與現金。","consequence":"每股盈餘與自由現金流成長低於營收，回饋率低於 85% 目標。","ruling":"部分採納：稅率已進指引，9 月季自由現金流 32.4 億創新高；但 9 月季回饋率只 41%，若 FY2027 全年 <70% 即屬股東經濟變差。","watch":"FY2027 自由現金流÷淨利 ≥0.85、全年回饋率、毛利率是否守 51%。","evidence_refs":["reg_tariff_export#1","customer_second_source#0"],"fact_refs":["f_kpi3","f_kpi4_sbc_gaap"]},{"view":"價格已反映太多","evidence":"前瞻 23.9 倍對應的是歷史最高利潤率；FY1 共識三個月已上修 16.9%；賣方 22 位中 21 位買進，8 月均目標價 342 美元。","assumption":"共識已把 2027 年高點寫進去，再上修空間小，倍數向循環中段回歸。","consequence":"盈餘照預期，股價仍因倍數壓縮而停滯。","ruling":"部分反駁：股價 26 週已跌 13.9%、倍數由前份約 30 倍壓到 23.9 倍，價格先修了一段；但基準報酬約年 7%，不支撐追價加碼。","watch":"前瞻倍數 >28 倍且共識未再上修時視為過熱。","evidence_refs":[],"fact_refs":["f_fwd_pe_latest","f_consensus_rev_3m_fy1_pct","f_week26_return_pct"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟢","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟢","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 252.35 → 本次 230.1（-8.8%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=252.35","side_b":"本次 price_at_dd=230.1","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 252.35 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 252.35 美元：Bull 價 553.5、Bear 價 119，五年期望值 +32.9%，基準年化 7.4%，不對稱比 2.0","side_b":"本次情境、股價仍用 252.35 美元：Bull 價 516、Bear 價 142.5，五年期望值 +19.8%，基準年化 2.8%，不對稱比 2.0","ruling":"先換情境、股價不動：五年期望值少 13.1 個百分點，基準年化少 4.6 個百分點。不對稱比由 2.0 變為 2.0。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 252.35 美元：五年期望值 +19.8%，基準年化 2.8%，不對稱比 2.0","side_b":"本次情境、股價 230.1 美元：五年期望值 +31.4%，基準年化 4.7%，不對稱比 2.72","ruling":"再換股價、情境不動：起點價下跌 8.8%，五年期望值多 11.6 個百分點，基準年化多 1.9 個百分點，不對稱比由 2.0 升到 2.72。合計五年期望值比前份少 1.5 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"股價與基本面背離","cause":null,"side_a":"股價 26 週跌 13.9%、RSI 24.6；法說當日一家記憶體大廠稱優先 3D DRAM 而非 4F²，股價下跌，市場在折現循環高點與 DRAM 路線疑慮。","side_b":"同期 FY1 共識三個月上修 16.9%，CY2027 WFE 由不給數字變成逾 2,000 億美元；CEO 稱跳到 3D DRAM 只會讓蝕刻沉積強度更早上升。","ruling":"可調和（程度差異）：市場提前折現 2028 年降溫，CEO 對 3D DRAM 的說法採信但未證。偏基本面側，持有不追價。","evidence_level":"公司法說＋共識快照","settle_metric":"1 月法說 CY2027 WFE 定案數字與 3 月季營收指引","if_then":["若 1 月法說 CY2027 WFE ≥1,900 億美元且股價 ≤200 美元，分兩批加碼至衛星上限","反向：若 WFE 展望下修至 1,800 億美元以下，停止加碼並把空頭機率上調至 35%"],"evidence_refs":[]},{"axis":"中國營收占比","cause":null,"side_a":"2026-01 公司預期 CY2026 中國占比降至 30% 以下（Zacks 轉述）。","side_b":"9 月季中國占 35%（6 月季 26%），CFO 稱完全如預期；12 月季將明顯下降，主因中國本土客戶。","ruling":"可調和：季度波動，全年仍可能接近 30%。9 月季本土客戶拉貨是否為管制到期前搶出貨屬推論、未證，12 月季的落差就是驗證。","evidence_level":"公司法說＋10-K 地區營收","settle_metric":"12 月季 10-Q 中國營收占比與總營收","if_then":["若 12 月季中國占比降到 20% 以下但總營收仍達指引下緣 82 億美元，視為已吸收，維持持有","反向：若中國下滑拖累總營收低於 82 億美元，停止加碼"],"evidence_refs":["geo_supply_chain#2","customer_concentration_credit#3"]},{"axis":"管理層前後說法對照","cause":null,"side_a":"2026-07-29 CFO 指引 9 月季營收 81 億±4 億、毛利率 52%、營業利益率 39.5%、EPS 2.15 美元；CEO 稱 CY2026 WFE 1,500 億出頭、2027 年不給數字；當時遞延收入增加主因客戶預付款。","side_b":"9 月季實績 82.2 億、52.4%、40.2%、2.20 美元，全數高於中點；WFE 上修為約 1,550 億，2027 年首度給出逾 2,000 億；本季遞延收入增加來自銷量，客戶預付款反而減少。","ruling":"一致：說到做到，未見改口。唯一的退步訊號是客戶預付款減少，可能是急迫性降溫，也可能只是銷量放大，未證。","evidence_level":"兩季法說逐字稿","settle_metric":"下一季遞延收入與預付款變化","if_then":["若 12 月季預付款續降且遞延收入轉為季減，停止加碼並提前檢視減碼門檻","反向：若預付款回升，維持"],"evidence_refs":[]},{"axis":"股東回饋承諾與實際","cause":null,"side_a":"長期承諾回饋自由現金流 85%（7 月法說說至少 85%）。","side_b":"9 月季只回饋 41%、年初至今 59%；現金由 56 億增至 75 億美元，另償還 7.5 億到期債。","ruling":"可調和：加速回購在 12 月季續執行，增加現金是為支應擴產與營運規模；FY2027 全年回饋率 <70% 才算偏離。","evidence_level":"公司法說","settle_metric":"FY2027 全年回饋率","if_then":["若 FY2027 回饋率 <70% 且現金續增，資本配置評估下修一級","反向：若 12 月季回購加速、回饋率回到 85% 以上，維持"],"evidence_refs":[]},{"axis":"現在就賣的最強論證","cause":null,"side_a":"賣方：利潤率歷史最高、同業大舉擴產、共識三個月已上修 17%，2027 年是受限下的高點且含提前拉貨，設備業歷史下行可達 −41%；現在賣在盈餘高點、倍數尚未壓到循環中段。","side_b":"持有方：股價已跌 13.9%、倍數由約 30 倍壓到 23.9 倍；客戶需求能見度到 2028 年，CFO 稱明年 10 座一線新廠上線，不受限需求高於 2,000 億；份額連三年上升。","ruling":"不賣、不追高加碼：2027 年盈餘能見度高，賣點留給營收指引連兩季季減或唯一致命點發生。","evidence_level":"公司法說＋SEMI 預測＋設備業下行史","settle_metric":"每季營收指引中點方向","if_then":["若連續兩季營收指引中點季減，減碼一半","反向：若 1 月法說 WFE ≥1,900 億且價格 ≤200 美元，加碼"],"evidence_refs":[]},{"axis":"前份漂移：價格變動","cause":"價格變動","prior_field":["signal","val"],"side_a":"前份（2026-07-30，股價 252.35，前瞻約 30 倍）：綜合評級 B、估值中性 🟡、裁決進場、角色衛星。","side_b":"本次（股價 230.1，前瞻 23.9 倍）：綜合評級 B、估值中性 🟡；裁決與角色由程式依本次輸入重算。","ruling":"股價跌約 9%、前瞻倍數明顯壓縮，但盈餘處循環高檔、利潤率創新高，估值結論與綜合評級不變。","evidence_level":"價格與共識快照","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"前份漂移：新證據確認","cause":"新證據","prior_field":["moat_trend","runway_post_y5","trap","archetype","cycle_position"],"side_a":"前份：護城河趨勢 ↑、五年後跑道 🟢、陷阱風險 🟡、循環/商品型、中循環。","side_b":"本次全部維持：SAM 占比上升、連三年跑贏 WFE、背面供電與乾式光阻新增指定機台（護城河 ↑）；先進封裝 2026 年成長逾 70%、面板級封裝出貨逾 20 家（跑道 🟢）；衰退訊號亮 1 個（陷阱 🟡）；WFE 2027 年仍增 30%、2028 年放緩，同業擴產（中循環）。","ruling":"新一季證據強化原判斷，五欄皆不變；中循環維持，若 1 月法說後 2028 年展望轉弱則改判晚循環。","evidence_level":"2026-10-21 法說＋SEMI 預測","settle_metric":"1 月法說 2028 年展望","if_then":["若 2028 年 WFE 展望持平或下修，循環位置改判晚循環並停止加碼"],"evidence_refs":[]},{"axis":"前份漂移：機率與回撤口徑","cause":"方法變動","prior_field":["p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份機率多頭 26%、空頭 30%，最大回撤單點 −60%。","side_b":"本次多頭 25%、基準 45%、空頭 30%；最大回撤改填範圍 −40%～−60%。","ruling":"回撤改填範圍並依設備業下行史推導；共識成長超過內生上界，空頭機率須守 30%；多頭下調 1 個百分點反映零組件供給限制。","evidence_level":"方法調整","settle_metric":null,"if_then":[],"evidence_refs":[]},{"axis":"前份漂移：加碼條件","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"加碼待兩約束同時解除：10月法說CY2027 WFE≥$180B且NAND合約價未連2季跌；且關聯方規則到期處置明朗（衝擊<$150M/季）。獨立分支：價格≤$200且R1未觸發","side_b":"加碼待兩條件之一：①關聯方規則到期後12月季中國衝擊<1.5億美元且1月法說CY2027 WFE≥1,900億美元；②價格≤200美元且季營收指引未季減","ruling":"加碼條件改寫：10 月法說已給出逾 2,000 億，原 1,800 億門檻已過，新門檻改看 1 月定案數字 1,900 億；NAND 合約價事實表未涵蓋，改用公司營收指引方向這個可觀察指標；關聯方規則門檻 1.5 億美元保留。","evidence_level":"2026-10-21 法說","settle_metric":"1 月法說 WFE、12 月季中國營收","if_then":["兩條件任一成立即分兩批加碼至衛星上限"],"evidence_refs":[]},{"axis":"前份漂移：Single Thing","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設唯一致命點（空值）。","side_b":"美國出口管制擴大至 Lam 在中國的核心蝕刻沉積品項（MATCH Act 立法或新規涵蓋在華跨國廠），12–24 個月機率約 25%。","ruling":"本輪補上 Single Thing：中國占營收約 34%，是數學上最大的單一敏感度；前份把它放在風險 R2，未獨立成唯一致命點。發生即減碼至半倉。","evidence_level":"10-K 與 10-Q 風險因子","settle_metric":"商務部與國會公告","if_then":["發生且只涵蓋中國本土客戶：減碼至半倉","發生且涵蓋在華跨國廠：清倉"],"evidence_refs":["reg_tariff_export#0","reg_tariff_export#3"]},{"axis":"前份漂移：退出指標","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設退出指標（空值）。","side_b":"營收指引連兩季季減；毛利率連兩季 <50%；1 月法說 CY2027 WFE <1,800 億美元；出口新規後中國占比 <20% 且總營收季減。","ruling":"本輪補上四條可觀察門檻，分別對應減碼一半、停止加碼與清倉的動作，取代前份只寫在加碼條件裡的隱含門檻。","evidence_level":"方法調整","settle_metric":null,"if_then":[],"evidence_refs":[]}],"triggers":[{"n":1,"text":"1 月法說 CY2027 WFE 展望定案","type":"假設驗證","maps_to":"H1","metric":"公司 CY2027 WFE 展望","threshold":"≥1,900 億美元維持；<1,800 億美元視為削弱","action":"<1,800 億則停止加碼、空頭機率升至 35%","source_freq":"每季法說","date":"2027-01"},{"n":2,"text":"出口管制關聯方規則暫緩到期處置","type":"風險","maps_to":"R2","metric":"12 月季中國營收中屬管制造成的減少額","threshold":"管制衝擊 ≥1.5 億美元／季，或規則擴大到 Lam 核心蝕刻沉積品項","action":"停止加碼","source_freq":"聯邦公報＋10-Q","date":"2026-10-30","evidence_refs":["reg_tariff_export#2","reg_tariff_export#3"]},{"n":3,"text":"美國出口管制擴大至 Lam 在中國的核心蝕刻沉積品項","type":"Single Thing","maps_to":"single_thing","metric":"出口新規適用範圍","threshold":"MATCH Act 立法或新規涵蓋中國本土以外的在華跨國廠","action":"減碼至半倉；涵蓋跨國廠則清倉","source_freq":"國會與商務部公告（事件）","date":null,"evidence_refs":["reg_tariff_export#3","geo_supply_chain#1"]},{"n":4,"text":"價格回落加碼分支","type":"估值rearm","maps_to":"H1","metric":"股價與季營收指引中點","threshold":"價格 ≤200 美元且最新季營收指引中點未季減","action":"分兩批加碼至衛星上限","source_freq":"每日價格＋每季指引","date":null},{"n":5,"text":"循環轉折：營收指引連續季減","type":"減碼","maps_to":"R1","metric":"下一季營收指引中點相對當季實績","threshold":"連續兩季指引中點季減","action":"減碼一半","source_freq":"每季財報","date":null,"evidence_refs":["cyclical_supply_discipline_capacity#2","cyclical_prior_downcycle_behavior#0"]},{"n":6,"text":"份額論點反轉","type":"清倉","maps_to":"H2","metric":"Lam 年度營收成長率減 WFE 成長率","threshold":"連續兩年跑輸 WFE 且毛利率連兩季 <49%","action":"清倉","source_freq":"年度法說","date":null},{"n":7,"text":"零組件供給吃緊是否在 3 月季解除","type":"風險","maps_to":"R5","metric":"3 月季營收相對 12 月季實績","threshold":"3 月季營收低於 12 月季實績","action":"停止加碼","source_freq":"每季財報","date":"2027-04","evidence_refs":["competitive_share_entrants#2"]},{"n":8,"text":"1 月法說後重跑完整判斷","type":"複審日期","maps_to":null,"metric":null,"threshold":null,"action":"重跑完整判斷","source_freq":"一次","date":"2027-01-31"}],"kill_metrics":[{"metric":"下一季營收指引中點相對當季實績","bear_threshold":"連續兩季季減→減碼一半","window":"2027-01 至 2027-07 法說","source":"公司新聞稿與 8-K","last_status":"ok"},{"metric":"單季 non-GAAP 毛利率","bear_threshold":"連兩季 <50%→停止加碼；<49% 且跑輸 WFE→清倉","window":"2026-12 季起四季","source":"公司新聞稿","last_status":"ok"},{"metric":"公司 CY2027 WFE 展望","bear_threshold":"1 月法說 <1,800 億美元→停止加碼","window":"2027-01 法說","source":"法說逐字稿","last_status":"ok"},{"metric":"出口新規後中國營收占比與總營收","bear_threshold":"中國占比 <20% 且總營收季減→減碼至半倉","window":"2026-11 至 2027-06","source":"10-Q 地區營收","last_status":"unknown"}],"evidence_dismissed":[],"action_conditions":{"rearm_trigger":"加碼待兩條件之一：①關聯方規則到期後12月季中國衝擊<1.5億美元且1月法說CY2027 WFE≥1,900億美元；②價格≤200美元且季營收指引未季減","exec_line":"持有不追高；條件①或②成立分兩批加碼；連兩季營收指引中點季減減碼一半；Single Thing 發生減碼至半倉；管制擴及在華跨國廠或份額轉跌則清倉。"}},"decision_inputs":{"signal":"B","ma":"🟢","cycle_position":"中循環","cycle_verdict":"未觸發","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場把 2027 年當循環頂點並對 DRAM 架構路線反應過度；但 2027 年逾 2,000 億美元是供給受限下的數字（CFO 稱不受限需求更高），客戶需求能見度到 2028 年，且跳到 3D DRAM 只會讓蝕刻沉積強度更早上升。","momentum_overheated":false,"cycle_gates_pass":false,"qc49_inherit_prior":true,"wait_for_price":null,"wait_for_price_condition":null,"prior_verdict":"進場","prior_role":"衛星"},"decision_out":{"verdict":"進場","role":"衛星","row_hit":"9","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='↑', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟢'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場把 2027 年當循環頂點並對 DRAM 架構路線反應過度；但 2027 年逾 2,000 億美元是供給受限下的數字（CFO 稱不受限需求更高），客戶需求能見度到 2028 年，且跳到 3D DRAM 只會讓蝕刻沉積強度更早上升。"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟢', val='🟡', moat_trend='↑', week26=-13.92, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='循環/商品', cycle_position='中循環', moat='B', moat_trend='↑', cycle_gates_pass=False"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":false,"basis":"signal='B', val='🟡'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":true,"basis":"signal='B', val='🟡', ma='🟢'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟡', ma='🟢'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟡', ma='🟢'"},{"row":"9-verdict","condition":"命中 row9 → 進場","hit":true,"basis":"row_hit=9"},{"row":"QC-49","condition":"qc49_inherit_prior=True 但前次裁決與矩陣機械輸出方向相同，無需承繼","hit":false,"basis":"prior_verdict='進場', 矩陣機械輸出='進場'"}],"pacing":[],"holding_cap":null,"requires_critic":[]},"thesis":{"H":[{"id":"H1","text":"AI 帶動的晶圓設備支出上行延續至 CY2027，WFE 逾 2,000 億美元、DRAM 領先，Lam 系統營收成長高於 WFE。","2y":"CY2027 WFE ≥1,900 億美元，且 Lam CY2027 營收成長率高於 WFE 成長率","5y":null,"10y":null,"threshold":"1 月法說 CY2027 WFE ≥1,900 億美元；季營收不低於共識路徑 5%","source":"公司每季法說、SEMI 年中與年底預測","drift_rule":"季營收 TTM 低於共識路徑連 2 季 ≥5% 為削弱、連 3 季 ≥10% 為反轉"},{"id":"H2","text":"蝕刻沉積強度隨 3D 化、背面供電、先進封裝與乾式光阻上升，Lam 的 SAM 占 WFE 比重接近 40%，連續第四、五年跑贏 WFE。","2y":"2027 年連續第四年跑贏 WFE","5y":"2030 年前 SAM 占 WFE 接近 40%，先進封裝與面板級封裝成為第二成長曲線","10y":null,"threshold":"Lam 年度營收成長率高於 WFE 成長率；SAM 占 WFE ≥37%（2027）","source":"公司法說與投資人日 SAM 揭露","drift_rule":"TTM 營收成長率低於 WFE 成長率連 4 季差距 ≥5 個百分點為削弱，連 6 季差距 ≥10 個百分點為反轉"},{"id":"H3","text":"利潤結構上移：毛利率朝中 50% 推進、營業利益率 2027 年守 40%，下一輪下行谷底毛利率不低於 45%（2023 年谷底 41.5%）。","2y":null,"5y":"毛利率中 50%，下一輪谷底毛利率 ≥45%","10y":null,"threshold":"2027 年單季 non-GAAP 毛利率 ≥51%","source":"公司每季新聞稿","drift_rule":"毛利率較 52% 基準偏離連 4 季 ≥5% 為削弱、連 6 季 ≥10% 為反轉"}],"R":[{"id":"R1","text":"循環轉折：2027 年含提前拉貨與擠潔淨室成分，SEMI 估 2028 年 WFE 成長放緩至 14.1%，同業大舉擴產；NAND 2027 下半年隨新產能放鬆。設備業歷史下行：2001 年出貨年減 41%、Lam 出貨峰谷跌 80%，2023 年谷底毛利率 41.5%。","h_ref":"H1","clock":"🔥","threshold":"連續兩季營收指引中點季減，或 NAND 占系統營收降至 15% 以下且記憶體金額季減","evidence_refs":["cyclical_prior_downcycle_behavior#0","cyclical_prior_downcycle_behavior#1","cyclical_prior_downcycle_behavior#3","cyclical_supply_discipline_capacity#2","cyclical_supply_discipline_capacity#3"]},{"id":"R2","text":"中國出口管制與在地化：中國占 FY2026 營收約 34%、9 月季 35%，出貨依賴出口許可；前份記載關聯方規則一年暫緩約 2026-10-30 到期，MATCH Act 討論中點名 Lam 的蝕刻沉積設備；客戶與下游同樣受關稅與管制影響；NAURA 升至全球第五，本土廠在成熟節點替代。","h_ref":"H1","clock":"⚡","threshold":"12 月季管制衝擊 ≥1.5 億美元，或新規涵蓋在華跨國廠","evidence_refs":["reg_tariff_export#0","reg_tariff_export#2","reg_tariff_export#3","geo_supply_chain#1","customer_concentration_credit#3","competitive_share_entrants#1","competitive_share_entrants#4"]},{"id":"R3","text":"倍數繼續向循環中段回歸而盈餘未同步成長：前份前瞻約 30.85 倍、本次 23.9 倍；長窗中位數事實表未涵蓋（前份所記 19.1 倍）。若 2027 年 WFE 只持平，倍數與盈餘同時下修。","h_ref":"H1","clock":"🔥","threshold":"CY2027 WFE 展望 <1,800 億美元且前瞻本益比仍 >20 倍","evidence_refs":[]},{"id":"R4","text":"客戶集中：四家客戶占 FY2026 營收約 55%（16%、15%、12%、12%），五家占應收帳款約 72%；大客戶可壓價、限制技術分享，單一記憶體客戶縮手影響不成比例。","h_ref":"H3","clock":"🐢","threshold":"營收成長中毛利率連兩季 <51%（壓價訊號），或單一客戶 >20% 營收","evidence_refs":["customer_second_source#0","customer_concentration_credit#0","customer_concentration_credit#1"]},{"id":"R5","text":"擴產跟不上：零組件吃緊已壓低 12 月季指引，10-K 列出跟不上 AI 需求可能流失份額；部分元件歷來只能向單一或少數供應商採購。","h_ref":"H2","clock":"⚡","threshold":"3 月季營收低於 12 月季實績","evidence_refs":["competitive_share_entrants#2","geo_supply_chain#0"]}],"single_thing":{"description":"美國出口管制擴大至 Lam 在中國的核心蝕刻沉積品項（MATCH Act 立法，或關聯方規則到期後全面恢復且不給豁免、涵蓋在華跨國廠）。","why_fatal":"中國占 FY2026 營收約 34%、9 月季 35%，是最大的單一敏感度；被拿掉的營收不會回來，還會加速本土設備商在中國的替代。","if_happens":"只涵蓋中國本土客戶：減碼至半倉；涵蓋在華跨國廠：清倉後重跑判斷。","how_monitor":"國會法案進度、商務部聯邦公報、公司 8-K 與 10-Q 地區營收占比、法說對中國的指引。","probability":"25%"}},"appendix_a":{"growth_durability":7,"quality_score":9,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":18.9,"peg_fy2":0.84,"stress":{"pass":2,"total":3}},"eps_meta":{"base_eps_path":{"FY2026A":5.76,"FY2027E":9.63,"FY2028E":12.15,"FY2029E":14.44},"fy_end_month":6,"eps_basis":"Koyfin 共識 EPS（以 non-GAAP 為主）；基期 FY2026A 取年報稀釋 EPS 5.76（GAAP），公司 GAAP 與 non-GAAP 差距小。"},"catalysts":[{"date":"2026-10","date_precision":"month","type":"regulatory","event":"出口管制關聯方規則一年暫緩到期（前份判斷記載約 10-30）","impact":"高","watch":"是否延長暫緩或擴大適用；12 月季中國營收衝擊是否 <1.5 億美元"},{"date":"2027-01","date_precision":"month","type":"guidance","event":"12 月季財報與 CY2027 WFE 定案展望","impact":"高","watch":"WFE ≥1,900 億美元；3 月季營收指引是否補回延後出貨"},{"date":"2027-04","date_precision":"month","type":"capacity","event":"3 月季財報：零組件供給吃緊是否解除","impact":"中","watch":"營收是否高於 12 月季實績、存貨與應付帳款變化"}]}
```

---

## ⑤ 覆蓋面（程式判定，你回的 ⑤ 燈號會被覆寫）

燈號 🟡：非核心軸無證據：channel_business_model_shift（通路／商業模式轉移）（尾部風險或事件型，不擋）。

⑤ 的 reason 只需評論：空軸的查詢詞是否切題、判斷有沒有交代缺口對結論的影響。

---

## 尾段：回覆格式

只回一個 JSON 陣列，①–⑧ 每條一個元素，八個全出，不得跳號、不得多列，陣列外不得有任何文字（不加前言、不加 markdown 圍欄、不加附註）：

```json
[{"item": "①", "light": "🔴|🟡|🟢", "judgment_path": "$.路徑", "reason": "一句話"}]
```
