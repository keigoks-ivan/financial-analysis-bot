你是 DD 管線 v20 的判斷層閘（gate），標的 CRS（20261025）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（36 條）
- `f_kpi0_net_sales_gaap`（q1_business）｜Net sales (GAAP)＝798.2 USD M｜期間與口徑：Q1 FY2027（季末 2026-09-30，公告於 2026-10-22）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q1 FY27 新聞稿（8-K 附件）（numbers.latest_quarter_kpis.items[0]，as_of Q1 FY2027（季末 2026-09-30，公告於 2026-10-22））
  - 註記：未取得
- `f_kpi1_adjusted_operating_margi`（q1_business）｜Adjusted operating margin excl. surcharge＝30.9 %｜期間與口徑：Q1 FY2027（季末 2026-09-30，公告於 2026-10-22）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q1 FY27 新聞稿；公司只揭露此利益率，未揭露 Non-GAAP 營業利益金額（numbers.latest_quarter_kpis.items[1]，as_of Q1 FY2027（季末 2026-09-30，公告於 2026-10-22））
  - 註記：未取得
- `f_kpi2_gaap_operating_income`（q1_business）｜GAAP operating income＝196.4 USD M（營業利益率 24.6%）｜期間與口徑：Q1 FY2027（季末 2026-09-30，公告於 2026-10-22）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q1 FY27 新聞稿（numbers.latest_quarter_kpis.items[2]，as_of Q1 FY2027（季末 2026-09-30，公告於 2026-10-22））
  - 註記：未取得
- `f_kpi7_sao_segment_operating_ma`（q1_business）｜SAO segment operating margin / adj. margin excl. surcharge＝29.6 %（adj. excl. surcharge 37.7%）｜期間與口徑：Q1 FY2027（季末 2026-09-30，公告於 2026-10-22）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q1 FY27 新聞稿；SAO 營收 730.4、營業利益 216.3（numbers.latest_quarter_kpis.items[7]，as_of Q1 FY2027（季末 2026-09-30，公告於 2026-10-22））
  - 註記：未取得
- `f_kpi8_aerospace_defense_end_ma`（q1_business）｜Aerospace & Defense end-market sales＝425.4 USD M｜期間與口徑：Q1 FY2027（季末 2026-09-30，公告於 2026-10-22）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q1 FY27 新聞稿；商用航太結構件／通路訂單 QoQ +23%、YoY +49%（numbers.latest_quarter_kpis.items[8]，as_of Q1 FY2027（季末 2026-09-30，公告於 2026-10-22））
  - 註記：未取得
- `f_peer_crs_gross_margin_pct`（q2_moat）｜CRS 毛利率＝30.58 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CRS.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_crs_operating_margin_pct`（q2_moat）｜CRS 營業利益率＝22.47 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CRS.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_ati_operating_margin_pct`（q2_moat）｜ATI 營業利益率＝15.19 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ATI.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_hwm_operating_margin_pct`（q2_moat）｜HWM 營業利益率＝27.31 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.HWM.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_crs_fcf_margin_pct`（q2_moat）｜CRS FCF 利潤率＝11.6 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CRS.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_kpi6_guidance_fy27_operating_`（q1_business）｜Guidance: FY27 operating income＝850–880 USD M（較 FY26 的 702.0 成長 21–25%，維持不變）｜期間與口徑：Q1 FY2027 新聞稿（公告於 2026-10-22）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司 Q1 FY27 新聞稿；FY29 營業利益目標 1,200–1,300（numbers.latest_quarter_kpis.items[6]，as_of Q1 FY2027 新聞稿（公告於 2026-10-22））
  - 註記：未取得
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝13.38 USD/share｜期間與口徑：2026-10-24／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261024.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-10-24）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝15.96 USD/share｜期間與口徑：2026-10-24／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261024.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-10-24）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝19.2 USD/share｜期間與口徑：2026-10-24／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261024.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-10-24）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝3435.36 USD m｜期間與口徑：2026-10-25／yfinance revenue_estimate 0y 平均（6 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-10-25）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝3790.28 USD m｜期間與口徑：2026-10-25／yfinance revenue_estimate +1y 平均（6 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-10-25）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi3_free_cash_flow`（q1_business）｜Free cash flow＝-24.8 USD M｜期間與口徑：Q1 FY2027（季末 2026-09-30，公告於 2026-10-22）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q1 FY27 新聞稿（營運現金流 52.8，資本支出 77.7，主因 brownfield 擴產）（numbers.latest_quarter_kpis.items[3]，as_of Q1 FY2027（季末 2026-09-30，公告於 2026-10-22））
  - 註記：未取得
- `f_kpi4_sbc`（q4_capital）｜SBC＝6.4 USD M（占 GAAP 營業利益 3.3%，占營收 0.8%）｜期間與口徑：Q1 FY2027（季末 2026-09-30，公告於 2026-10-22）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q1 FY27 新聞稿；占比為 6.4÷196.4、6.4÷798.2 自算（numbers.latest_quarter_kpis.items[4]，as_of Q1 FY2027（季末 2026-09-30，公告於 2026-10-22））
  - 註記：不適用
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝539.8 USD m｜期間與口徑：2026-10-25／yfinance 最新一季：總債務 699.3、現金 159.5（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-10-25）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝49.54 m shares｜期間與口徑：2026-10-25／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-10-25）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝284.66 USD｜期間與口徑：2026-10-23（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-10-23（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝21.28 x｜期間與口徑：2026-10-24／分母＝FY1 EPS 13.38，分子＝快照價 284.66｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-10-24）
- `f_consensus_rev_fy1_pct`（q5_valuation）｜FY1 共識修正＝-0.59 %｜期間與口徑：2026-10-24／兩份 Koyfin 快照之間的 EPS 修正幅度（13.46 → 13.38）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261024.xlsx（numbers.consensus_revision.fy1.revision_pct，as_of 2026-10-24）
- `f_consensus_rev_fy2_pct`（q5_valuation）｜FY2 共識修正＝0.0 %｜期間與口徑：2026-10-24／兩份 Koyfin 快照之間的 EPS 修正幅度（15.96 → 15.96）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261024.xlsx（numbers.consensus_revision.fy2.revision_pct，as_of 2026-10-24）
- `f_consensus_rev_fy3_pct`（q5_valuation）｜FY3 共識修正＝0.42 %｜期間與口徑：2026-10-24／兩份 Koyfin 快照之間的 EPS 修正幅度（19.12 → 19.2）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261024.xlsx（numbers.consensus_revision.fy3.revision_pct，as_of 2026-10-24）
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝26.47 %｜期間與口徑：2026-07-30 → 2026-10-24／FY1 共識 EPS 10.58 → 13.38（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261024.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-10-24）
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝25.1 x｜期間與口徑：2026-10-23（RTH 收盤，UTC）／4 個年度端點內的分位＝0.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-10-23（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝0.0 %｜期間與口徑：2026-10-23（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-10-23（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝39.5 %｜期間與口徑：2026-10-23（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-10-23（RTH 收盤，UTC））
- `f_ev_s_fwd`（q5_valuation）｜EV/S（EV ÷ FY1 共識營收）＝4.26 x｜期間與口徑：2026-10-25／f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）｜kind：estimate
  - 來源：—（numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m，as_of 2026-10-25）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝-33.32 %｜期間與口徑：2026-10-23（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-10-23（RTH 收盤，UTC））
- `f_rsi14`（q5_valuation）｜RSI(14)＝11.08｜期間與口徑：2026-10-23（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-10-23（RTH 收盤，UTC））
- `f_ma_w52`（q5_valuation）｜52 週均線＝418.01 USD｜期間與口徑：2026-10-25／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-10-25）
- `f_ma_w104`（q5_valuation）｜104 週均線＝317.22 USD｜期間與口徑：2026-10-25／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-10-25）
- `f_ma_w250`（q5_valuation）｜250 週均線＝168.26 USD｜期間與口徑：2026-10-25／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-10-25）
- `f_ma_state`（q5_valuation）｜週線均線六態（decision_inputs.ma 必須等於此值）＝🟠｜期間與口徑：2026-10-25／timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-10-25）
  - 原文：「price 284.66 / W52 418.01 / W104 317.22 / W250 168.26 / W250 13週斜率 3.24%」

### findings_digest 中方向為負或來源衝突的條目（9 條）
- `competitive_share_entrants#1`（competitive_share_entrants｜方向 -｜狀態 ok）：社群敘事提到競爭對手（如 ATI）增加產能投資，長期可能帶來較大價格壓力。
  - 來源：Simply Wall St community narrative（as_of 2026-08-15）｜affects：decision_inputs.bear、moat_trend
- `supply_demand_durability#3`（supply_demand_durability｜方向 -｜狀態 ok）：鈦醫療經銷客戶需求疲弱拖累 Performance Engineered Products（Q2 FY2026），管理層稱 1 月訂單為 2025 年最高。
  - 來源：MarketBeat Q2 FY2026 call highlights（搜尋摘要）（as_of 2026-01-29）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#1`（reg_tariff_export｜方向 -｜狀態 ok）：風險因子列示關稅、配額、出口管制與貿易政策變動為國際營運風險，可能對業務重大不利。
  - 來源：SEC EDGAR 10-K FY2026 Item 1A（as_of 2026-08-12）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：10-K 風險因子：部分關鍵原料向政經情勢可能不穩的國家的供應商採購，且供應商漲價或無法供貨時可能沒有替代來源；未點名國家，也未揭露特定單一來源供應商
  - 來源：Carpenter Technology FY2024 Form 10-K (SEC)（as_of 2024-08-15）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：10-K 風險因子：供應商漲價或不願／無法滿足需求時，公司可能沒有替代供應來源
  - 來源：Carpenter Technology FY2024 Form 10-K (SEC)（as_of 2024-08-15）｜affects：thesis.R、decision_inputs.bear
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：公司 10-K 揭露：部分不同產品在某些情況下可替代其成品。
  - 來源：SEC EDGAR 10-K FY2026 Item 1（as_of 2026-08-12）｜affects：moat_trend、decision_inputs.bear
- `substitute_technology#1`（substitute_technology｜方向 -｜狀態 ok）：公司 10-K 風險因子：較低成本替代材料持續可得，客戶可能轉用較低成本替代品，造成業績大幅波動。
  - 來源：SEC EDGAR 10-K FY2026 Item 1A（as_of 2026-08-12）｜affects：thesis.R、decision_inputs.bear
- `channel_business_model_shift#1`（channel_business_model_shift｜方向 -｜狀態 ok）：Latrobe Distribution 報告單位因客戶下單型態下滑，FY2024 Q3 認列 $14.1M 商譽減損（全數商譽），為舊事件，非 2026 通路轉型。
  - 來源：SEC EDGAR 10-K FY2026 Item 7 MD&A（as_of 2026-08-12）｜affects：moat_trend
- `capital_markets_pricing#1`（capital_markets_pricing｜方向 -｜狀態 ok）：Tickflow 彙整（2026-08-01）：15 位分析師共識評級 Buy，共識目標價 $465.80，其引用價 $520.92，目標價低於當時價約 16.4%。
  - 來源：Tickflow CRS forecast（as_of 2026-08-01）｜affects：valuation、decision_inputs.bear

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 5 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CRS_20261025/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":648.0,"bear_5y_price":126.0,"p_bull_pct":25,"p_bear_pct":30,"upside_5y_pct":49.5,"ev5y_pct":37.5,"irr_base_pct":8.4,"asym_ratio":1.9,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":13.38,"pe":21.28,"basis":"FY1＝FY2027E（6 月財年）調整後 EPS 共識；現價與終端都用前瞻一年口徑"},"eps":{"bull":[14.0,17.2,21.0,24.0,27.0],"base":[13.3,15.6,18.6,20.6,22.4],"bear":[12.6,12.8,11.0,9.5,10.5]},"pe":{"bull":24,"base":19,"bear":12},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0.281,"net_buyback":1.5},"second_stage":{"bull_cagr_pct":10,"base_cagr_pct":6},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### CRS_Q4_2026_Earnings_Call_20260730.md
- 2026-07-30｜CFO｜guidance：FY27 Q1 總營業利益財測 1.95–2.00 億美元（原話："operating income of $195 million to $200 million."）
- 2026-07-30｜CFO｜guidance：SAO 部門 FY27 Q1 營業利益財測（原話："income in the range of $218 million to $222 million."）
- 2026-07-30｜CEO｜guidance：FY27 全年營業利益財測（原話："we expect between $850 million"）
- 2026-07-30｜CEO｜guidance：FY29 營業利益目標區間（原話："approximately $1.2 billion to $1.3 billion"）
- 2026-07-30｜CEO｜guidance：FY27 調整後自由現金流財測（原話："we anticipate between $400 million and $430 million of"）
- 2026-07-30｜CFO｜guidance：FY27 Q1 公司費用預期約 2,900 萬（原話："corporate costs of approximately $29 million."）
- 2026-07-30｜CEO｜guidance：管理層對訂定目標的原則（原話："We believe in setting targets"）
- 2026-07-30｜CEO｜guidance：CEO 表示 FY27 財測可視為下限（原話："if you want to consider FY '27 to floor, you won't"）
- 2026-07-30｜CEO｜guidance：CEO 稱 FY29 不是獲利高點（原話："do not believe fiscal year 2029 represents the peak"）
- 2026-07-30｜CEO｜guidance：CEO 預期 FY27 航太明顯更高（原話："we see aerospace being meaningfully higher in FY '27."）
- 2026-07-30｜CFO｜margin：SAO 調整後營業利益率連續第 18 季上升至 37.8%（原話："consecutive quarter to a new record level of 37.8%."）
- 2026-07-30｜CFO｜margin：管理層說明每磅均價受產品組合影響（原話："is highly dependent on the mix of products."）
- 2026-07-30｜CFO｜margin：低價產品毛利水準相當（原話："the lower-priced products often come with comparable"）
- 2026-07-30｜CEO｜margin：CEO 稱 SAO 利潤率不會停在此處（原話："I can tell you now, this isn't the floor for us."）
- 2026-07-30｜CFO｜margin：Q4 有效稅率較低來自一次性稅務利益（原話："discrete tax benefits associated with certain equity awards."）
- 2026-07-30｜CFO｜commitment：擴產案進度與預算（原話："expansion remains on budget and on schedule to be completed"）
- 2026-07-30｜CFO｜commitment：擴產案預計 2030 年增量營業利益約 1.5 億（原話："roughly $150 million of incremental OI."）
- 2026-07-30｜CFO｜commitment：管理層對 1.5 億數字信心提高但維持不變（原話："it's fair to say that we are more confident in those"）
- 2026-07-30｜CEO｜commitment：CEO 解釋不調高 1.5 億的理由（原話："we're not 100% sure of the exact mix of those products."）
- 2026-07-30｜CEO｜commitment：CEO 回任，非過渡，不外找新任 CEO（原話："this is not an interim assignment, and we are not launching"）
- 2026-07-30｜CFO｜capital_allocation：回購累計額度使用情形（原話："the total to $281 million spent to date against the"）
- 2026-07-30｜CEO｜capital_allocation：資本配置哲學不變（原話："allocation philosophy remains unchanged."）
- 2026-07-30｜CEO｜capital_allocation：併購並非排除但排序較低（原話："That's not a no, but it's just a tough one"）
- 2026-07-30｜CEO｜capital_allocation：回購與股息持續（原話："We're always going to have the dividend."）
- 2026-07-30｜CFO｜capital_allocation：資本支出節奏全年平均（原話："it would be fairly ratable throughout the year."）
- 2026-07-30｜CFO｜capital_allocation：自由現金流轉換率 85–90%（原話："we can hit that 85% to 90% type conversion ratio"）
- 2026-07-30｜CEO｜customer：波音預期月產率 47 架（原話："Boeing stated that they expect to achieve rate 47 per month"）
- 2026-07-30｜CEO｜customer：部分結構件客戶下單仍謹慎（原話："structural customers remain cautious in their ordering"）
- 2026-07-30｜CEO｜customer：引擎客戶稱產能比需求更受關注（原話："than the capacity needed to meet that demand."）
- 2026-07-30｜CEO｜customer：結構件成長可能領先（原話："the growth in structural will lead the pack"）
- 2026-07-30｜CEO｜customer：航太緊固件銷售成長（原話："They were up 10% sequentially, 12% year-over-year."）
- 2026-07-30｜CEO｜customer：航太新合約客戶要求更多材料（原話："they ask for more and more material. Not less."）
- 2026-07-30｜CEO｜customer：交期大致穩定，部分產品拉長（原話："lead times are relatively consistent quarter-over-quarter."）
- 2026-07-30｜CEO｜customer：長約將有重大合約待續約（原話："there are a couple of very significant contracts that will"）
- 2026-07-30｜CEO｜customer：仍有疫情前條款長約（原話："yes, there's still 1, maybe 2 that's pre-COVID."）
- 2026-07-30｜CEO｜product：醫療終端本財年首度季增（原話："medical end-use market sales were up sequentially."）
- 2026-07-30｜CEO｜product：IGT 能源銷售季間波動（原話："sales for IGT material will fluctuate due to order timing"）
- 2026-07-30｜CEO｜product：工業消費由半導體帶動（原話："demand from the semiconductor industry, where our"）
- 2026-07-30｜CEO｜product：Dynamet 占比小但視為策略資產（原話："SAO is 95% plus of our segment"）
- 2026-07-30｜CEO｜competition：太空需求可能與航空引擎合金爭用產能（原話："space could potentially compete with aero engine alloys."）
- 2026-07-30｜CEO｜risk：結構件客戶謹慎、低於預期需求下單（原話："structural customers remain cautious in their ordering"）

### 問答異常語氣（迴避／改口／保留）
- CRS_Q4_2026_Earnings_Call_20260730.md｜問：Deutsche Bank 問為何 FY27 財測隱含 EBIT 成長放緩｜答法：CEO 不反駁，改說財測可視為下限，未解釋放緩原因
- CRS_Q4_2026_Earnings_Call_20260730.md｜問：Wells Fargo 問 SAO 增量利潤率｜答法：CEO 拒絕預測季度利潤率，僅稱非下限、等數季後再看，未給數字
- CRS_Q4_2026_Earnings_Call_20260730.md｜問：BTIG 問 FY29 目標隱含的利潤率高點｜答法：CEO 以玩笑帶過，不給模型利潤率
- CRS_Q4_2026_Earnings_Call_20260730.md｜問：TD Cowen 問長約續約占比｜答法：CEO 明言不給確切百分比，只說有幾個大型合約
- CRS_Q4_2026_Earnings_Call_20260730.md｜問：Deutsche Bank 問 2030 年 1.5 億是否偏低｜答法：CFO 稱信心提高、可能更高，但仍維持 1.5 億，未給新數字

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 2 | 2 |
| customer_second_source | found | 1 | 2 |
| customer_concentration_credit | found | 1 | 2 |
| supply_demand_durability | found | 5 | 4 |
| regulatory_antitrust | found | 1 | 3 |
| reg_tariff_export | found | 2 | 2 |
| geo_supply_chain | found | 3 | 2 |
| end_markets | found | 3 | 2 |
| substitute_technology | found | 2 | 2 |
| channel_business_model_shift | found | 2 | 2 |
| capital_markets_pricing | found | 3 | 3 |
| major_events | found | 2 | 3 |

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260901","verdict":"進場","role":"核心","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"SAO 調整後營益率維持 ≥33% 為結構性新常態（非景氣頂峰）","columns":{"2Y 驗證點":"FY27-28 TTM 維持 34-38%","5Y 驗證點":"FY31 Athens 全貢獻後仍 ≥32%","10Y 驗證點":"FY35 跨週期均值 ≥26%","數字門檻":"連 2 季 TTM &lt;33%＝削弱；連 4 季 &lt;30%＝反轉","來源":"Q4 FY26 法說（2026-07-30）；連 18 季擴張紀錄","漂移觸發":"連 2 季 TTM &lt;33%"}},{"id":"H2","text":"航太 A&amp;D 需求動能持續至少到 FY28-29（16,000 架積壓訂單支撐）","columns":{"2Y 驗證點":"Boeing 737 MAX 達 47/月並邁向 52/月；Airbus A320neo 邁向 70-75/月","5Y 驗證點":"FY31 A&amp;D 占營收仍 ≥65%，訂單金額維持正成長","10Y 驗證點":"2035 前窄體機積壓不低於 8,000 架","數字門檻":"連 2 季訂單轉負＝削弱；連 3 季負成長＝反轉","來源":"Q4 FY26 法說；Boeing/Airbus 公開產能指引","漂移觸發":"連 2 季訂單轉負"}},{"id":"H3","text":"Athens AL 擴產（$400M，+9,000噸／+7%）如期於 FY2028 初商轉，且 2030 貢獻增量營益 $150M+","columns":{"2Y 驗證點":"FY27 法說持續確認 on schedule/on budget","5Y 驗證點":"FY30 增量營益達成或超過 $150M 目標","10Y 驗證點":"2030+ 新產能在下一輪週期谷底仍守 ≥60% 稼動率","數字門檻":"延後 &gt;6 個月＝削弱；成本超支 &gt;20%＝削弱","來源":"Q4 FY26 法說：「12 個月後上線」，capex $242.7M FY26 已投入","漂移觸發":"延後 &gt;6 個月"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"Boeing 新一輪品質/FAA 介入事件，737 MAX 月產無法邁向 47→52 目標","columns":{"對應假設":"H2","時間尺度":"⚡ 短期","監測指標":"Boeing 月度交付數據＋FAA 公告","警戒閾值":"連 2 季月產 &lt;38 架削弱；連 3 季 &lt;35 架或再遭限產反轉"}},{"id":"R2","text":"ATI Bakers South VIM（2027H2 投產，9,000 噸、80% 已鎖 LTA）上線後產業提價紀律鬆動，CRS 續約 LTA 提價幅度縮小","columns":{"對應假設":"H1","時間尺度":"🔥 中期","監測指標":"CRS 逐年 LTA 續約提價幅度、SAO 定價事件帳","警戒閾值":"續約提價降至個位數且連 2 次＝削弱；出現折價續約＝反轉"}},{"id":"R3","text":"下一輪航太週期反轉（歷史前例 FY22-23，GAAP 曾轉虧），疊加 Athens 產能適逢景氣谷底上線稀釋利潤率","columns":{"對應假設":"H1+H2","時間尺度":"🐢 長期","監測指標":"全球商用機積壓訂單總量、Boeing/Airbus 訂單淨額","警戒閾值":"積壓訂單/交付比從 ~10 年降至 &lt;6 年開始減倉；&lt;4 年大幅減倉"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"已進場核心角色，無rearm觸發；加碼觸發見§13b","irr_base_pct":8.4,"ev5y_pct":34.7,"drift_watch_prior":{"dca_verdict":"進場","dca_role":"核心","signal":"A","val":"🟡","ma":"✅","trap":"🟢","moat_trend":"↑","runway_post_y5":"🟢","asym_ratio":1.7,"ev5y_pct":34.7,"irr_base_pct":8.4,"max_dd_pct":-68.0,"bull_5y_price":1056.0,"bear_5y_price":187.5,"p_bull_pct":25,"p_bear_pct":30,"rearm_trigger":"已進場核心角色，無rearm觸發；加碼觸發見§13b","price_at_dd":476.42,"archetype":"品質複利成長","cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"CRS","date":"2026-10-25","schema":"v15.0","contract":"v19","company_name":"Carpenter Technology"},"oneliner":"航太鎳基超合金供不應求，長約續約持續漲價，FY27 營業利益指引 850–880 百萬美元維持不變；股價半年跌 33%，前瞻本益比降到約 21 倍，基本面未見破損。利益率處於歷史高點，週期回落風險以 Bear 三成機率計價。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CRS_20261025/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CRS_20261025/scenario.json","answers":{"q1_business":{"verdict":"賺的是航太引擎、緊固件與結構件供應鏈的錢。錢卡在合格的真空熔煉產能與多年材料認證；產能已滿載，利潤擴大靠長約重訂價。","reasoning":"最新一季（Q1 FY27，季末 2026-09-30）營收 798.2 百萬美元（含附加費），GAAP 營業利益 196.4，營益率 24.6%；不含附加費的調整後營益率 30.9%。SAO 部門調整後營益率 37.7%，與上季紀錄持平。分部方面，SAO 營收（不含附加費）573.5、PEP 83.0，SAO 約占九成且貢獻幾乎全部利潤。終端以航太國防為主，FY26 約占營收 65%、年增 15%；醫療 FY26 年減約 21%，運輸年減約 11%。原料成本以附加費轉嫁給客戶。FY24–FY26 無單一客戶占營收或應收帳款 10% 以上。單點依賴在上游：部分關鍵原料來自政經不穩國家，且可能沒有替代來源。產業時鐘在擴張期：主機廠產率由 2026 年約 1,400–1,500 架往 2,100 架以上爬升，積壓訂單逾 16,000 架，客戶下單量仍低於現行產率，尚未過熱。供需持久性屬結構性偏持久：2019 年以來除生產力提升外無實質新增產能，合格鎳基超合金廠很少。反向因素是本公司擴產約 9,000 噸將於 FY28 初上線，ATI 也在加產能，2028 年後供給可逆性屬中等。另外，Q1 有效稅率 15.5% 含一次性股權獎勵稅務利益，單季 EPS 3.25 略被墊高。","fact_refs":["f_kpi0_net_sales_gaap","f_kpi1_adjusted_operating_margi","f_kpi2_gaap_operating_income","f_kpi7_sao_segment_operating_ma","f_kpi8_aerospace_defense_end_ma","f_peer_crs_gross_margin_pct","f_peer_crs_operating_margin_pct"],"verdict_values":{"revenue_quality":"航太業務多數在長約下，原料以附加費轉嫁；客戶分散，FY24–FY26 無單一客戶占營收 10% 以上。","unit_econ_note":"公司本季起停止揭露出貨量，量價拆分無法驗證。Q1 營收（不含附加費）年增 5%，營業利益年增 28%，管理層歸因於生產力、組合與價格。","archetype":{"primary":"品質複利成長","secondary":"循環/商品","confidence":"中","fingerprint":"產能滿載、長約重訂價、附加費轉嫁的特殊合金廠；FY23 營益率僅 5.2%，循環性並未消失。"},"industry":{"clock_phase":"II","sd_verdict_source":"結構性偏持久。Q2 FY26 簡報稱 2019 年以來無實質新增產能、合格供應商少；Q1 FY27 法說 CEO 稱除本公司擴產與少數幾家外沒有新產能上線。反向因素是本公司與 ATI 同步擴產。","bargaining":{"up":"鎳、鈷、鈦等原料部分來自政經不穩國家，供應商漲價時可能沒有替代來源，目前以附加費轉嫁吸收。","down":"客戶最在意保證供貨。長約續約價格大幅上調，客戶都要求更多材料；無單一客戶超過營收 10%。","geo":"關稅經附加費轉嫁，管理層判斷目前無重大影響。國防撥款遲滯壓低國防訂單。"},"profit_pool_dir":"利潤池往材料端移動：本公司營益率 FY23 5.2%，FY26 升到 22.5%。下游鍛造與緊固件商 HWM 營益率仍高於本公司（27.3%）。","tam_table":{"expanded":false,"reason":"不屬低滲透或新品類題材，成長來自既有航太產率爬升與價格；事實表未涵蓋市場規模與份額數據。"}}}},"q2_moat":{"verdict":"→ 穩定：認證門檻與合格供應商稀少的格局未變。目前價格力強，但主要來自供需缺口；份額持平，同業也在同步擴產。","reasoning":"護城河機制：鎳基超合金需逐一料號通過客戶認證，第三方稱新供應商需 18–36 個月（單一廠商報告，未經獨立驗證）；10-K 稱高價值產品的主要競爭者不到十家；航太業務多數在長約下。方向證據：Q1 FY27 法說 CEO 表示長約續約量增，但份額大致不變，沒有搶份額。價格力確實擴大，但來源是 2019 年以來無新增產能的供需缺口，屬可逆來源；本公司擴產約 9,000 噸將於 FY28 初上線，ATI 亦在擴產。同業利潤對照（TTM 至 2026-06）：營益率本公司 22.5%、ATI 15.2%、HWM 27.3%，對最接近的熔煉同業 ATI 高 7.3 個百分點。同業利差的歷史序列事實表未涵蓋，無法判斷擴大或收窄，因此不給擴大。產業態勢分三軸看：競爭面，ATI 與本公司同步加產能，埋下供給轉鬆的種子；結構面，航太積壓逾 16,000 架、產率目標再提高約 50%，結構轉好；其他面，關稅經附加費轉嫁，低價替代材料的風險則常態存在。整體裁決為雙向拉鋸。報酬持續期：當期稅後營業利益約 555 百萬美元（FY26 營業利益 702×(1−21%)）；投入資本事實表未涵蓋，ROIC 無法精算。增量報酬以擴產案估算：約 4 億美元投入換得 FY30 增量營業利益約 1.5 億，稅後約 30%；再投資率代理值約 35%；內生成長上界約 10.5%。","fact_refs":["f_peer_crs_operating_margin_pct","f_peer_ati_operating_margin_pct","f_peer_hwm_operating_margin_pct","f_peer_crs_fcf_margin_pct","f_kpi6_guidance_fy27_operating_","f_kpi7_sao_segment_operating_ma"],"verdict_values":{"moat":{"mechanism":"材料認證轉換成本，加上合格熔煉產能稀缺與多年長約","execution":8,"pricing":7,"grade":"B","trend":"→","trend_evidence":"Q1 FY27 法說：長約份額大致不變、沒有搶份額；價格續漲但來自供需缺口；本公司擴產約 9,000 噸與 ATI 擴產同步進行。營益率較 ATI 高 7.3 個百分點、較 HWM 低 4.8 個百分點；同業利差歷史序列事實表未涵蓋。","competitor_notes":[{"name":"HWM","strategy_note":"下游鍛造與緊固件龍頭，部分是本公司客戶。營益率 27.3%、自由現金流利潤率 19.6%，都高於本公司，代表價值鏈下游仍分走較多利潤。"},{"name":"ATI","strategy_note":"最接近的熔煉同業，營益率 15.2%，正在擴產。新產能上線時點是本公司長約漲幅能否延續的主要變數。"},{"name":"MTRN","strategy_note":"鈹與先進材料利基，營益率 6.4%，與本公司航太超合金重疊有限，不作定價錨。"},{"name":"RS","strategy_note":"金屬通路與加工中心，營益率 7.8%，屬通路角色而非熔煉產能持有者。"}],"threats":[{"level":"🟡","text":"ATI 等同業擴產，加上本公司 FY28 初擴產約 9,000 噸，2028 年後供需缺口可能收斂，長約續約漲幅隨之縮小。","p":"25%","evidence_refs":["competitive_share_entrants#1"]},{"level":"🟡","text":"10-K 揭露部分產品可被替代，低價替代材料可得時客戶可能轉用。航太認證件替代難度高，衝擊集中在工業與消費等不需認證的品項。","p":"10%","evidence_refs":["substitute_technology#0","substitute_technology#1"]}],"roic_durability":{"quadrant":"高利益率×周轉率未知（投入資本事實表未涵蓋）","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者是航空公司，決策者與付款者是引擎與機體供應鏈。沒有合格合金就造不出引擎，屬「需要」而非「想要」。主機廠積壓逾 16,000 架，第三季空中交通量季增 14%，引擎首次大修潮來臨。"},{"item":"決策層級","level":"🟢","text":"替代性要看料號層級的認證：換供應商須重新認證，第三方稱需 18–36 個月；航太業務多數在長約下，長約續約時客戶都要更多量。"},{"item":"價值鏈分配","level":"🟡","text":"材料端分到的利潤正在變多（營益率 FY23 5.2%→FY26 22.5%），但下游 HWM 營益率仍高 4.8 個百分點。上游原料部分來自不穩國家，供應商議價力未知；新產能 2028 年後上線可能把分配推回下游。"},{"item":"社會容忍度","level":"🟢","text":"客戶是企業與國防供應鏈，沒有消費者端的政治漲價上限。國防採購價格審查是潛在上限，但本包證據未見相關討論。"}],"roiic":"約 30%（擴產案：增量營業利益約 150 百萬美元×(1−21%)÷投入約 400 百萬美元）","reinvest_rate":"約 35%（代理值：1−FY26 自由現金流 362.3÷稅後營業利益約 555；折舊與營運資金明細事實表未涵蓋）","endo_ceiling":10.5,"formula_note":"內生成長＝30%×35%≈10.5%。擴產投入約 4 億取自前份判斷引用的 Q4 FY26 法說；1.5 億增量營業利益取自 2026-07-30 Q4 FY26 法說 CFO 原話；稅率 21% 取公司指引區間 20–22% 中值。"}}}},"q3_growth":{"verdict":"🟡 中：五年內成長以價格為主、擴產加量約 7% 為輔；Y5 後的跑道取決於新訂單與第二曲線。","reasoning":"成長組成以價格為主，包括長約重訂與非長約價格續升；量受產能滿載限制，FY28 初擴產約 9,000 噸（約 2019 年出貨量的 7%）帶來加量，另有淨回購。三年共識 EPS 為 FY27 13.38、FY28 15.96、FY29 19.20，自 FY26 調整後 EPS 10.76 起算年化約 21%；共識家數事實表未涵蓋，營收共識來自 6 位分析師。內生上界約 10.5%（見護城河段），缺口約 11 個百分點。缺口歸因：利益率擴張約 8 個百分點（FY29 營業利益目標 1,200–1,300，對比 FY26 的 702，增幅遠高於營收共識的年增約 10%），淨回購約 3 個百分點。缺口可以歸因，但前提是價格續漲。跑道：以目標產率 2,100 架計，16,000 架積壓約可支撐 7–8 年。FY31 後能否續長，取決於新訂單、國防新平台，以及燃氣渦輪、半導體等第二曲線；目前只有管理層口述，沒有量化證據，因此給中。衰退信號亮一項（EPS 成長遠高於營收成長），FCF 轉換率有一年低於 0.75，列為觀察。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_kpi6_guidance_fy27_operating_"],"verdict_values":{"growth":{"driver_mix":"價為主、量為輔（擴產約 +7%），再加淨回購","runway_years":7,"runway_post_y5":"🟡","endo_ceiling_basis":"增量報酬約 30%×再投資率約 35%≈10.5%；共識三年 EPS 年化約 21%，缺口由利益率擴張與淨回購解釋","segments":[{"item":"SAO（Q1 FY27，不含附加費）","value":"營收 573.5 百萬美元，年增 7%；調整後營益率 37.7%；營業利益 216.3"},{"item":"PEP（Q1 FY27，不含附加費）","value":"營收 83.0 百萬美元，年減 5%；營業利益 7.3（去年同期 9.4），鈦醫療走弱"},{"item":"航太國防終端（FY26）","value":"約占營收 65%，年增 15%；醫療年減約 21%、運輸年減約 11%"}],"decay_signals":["EPS 成長遠高於營收成長：亮燈（FY23→FY26 營收年化約 7%，EPS 由 1.14 升至 10.52）","FCF÷淨利：FY26 0.68、FY25 0.76，只有一年低於 0.75，未達連兩年，列觀察","毛利率連 2 季年減：未亮（年度毛利率 13.2%→30.6% 逐年上升）","SBC 占營收：未亮（0.8%）","核心市占縮減：未亮（管理層稱份額持平）","提價後銷量下滑：無法判斷（公司已停止揭露出貨量）","產業估值倍數系統性下移：事實表未涵蓋"],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"現金有一段被擴產吃掉，回購多在高價區執行；資產負債表穩健。","reasoning":"自由現金流÷淨利：FY24 0.96、FY25 0.76、FY26 0.68（年度財報序列），轉換率隨擴產資本支出下滑。Q1 FY27 營運現金流 52.8、資本支出 77.7，自由現金流 −24.8；CFO 說明是存貨季節性累積，下半年會回收，全年自由現金流指引 400–430 維持不變。SBC 6.4，占營收 0.8%。現金去向依序為擴產、回購（Q1 回購 133.9，用完舊的 4 億額度並啟用新的 10 億額度）、股息，最後才是併購（管理層稱優先序低）。淨負債 539.8，淨負債÷EBITDA 0.6 倍，2034 年前沒有債務到期。回購時點方面，Q1 期間股價至少有一段落在 476–521 區間（9/1 前份判斷價與 8/1 引用價），實際均價事實表未涵蓋。以 FY27 共識 EPS 計，買入收益率約 2.6–2.8%，要 10 年期公債殖利率低於約 0.8% 才算過關，因此判不過；若以現價 284.66 回購，收益率升到約 4.7%。","fact_refs":["f_kpi3_free_cash_flow","f_kpi4_sbc","f_net_debt_m","f_shares_diluted_m","f_price_at_dd","f_consensus_eps_fy1"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":false,"passed":null,"input":"近年沒有併購；Q4 FY26 法說 CEO 表示併購不排除，但優先序低。"},{"name":"buyback_yield","applicable":true,"passed":false,"input":"Q1 回購 133.9 百萬美元，期間股價約 476–521，對 FY27 共識 EPS 13.38 的買入收益率約 2.6–2.8%，低於公債殖利率加 2% 的門檻。實際回購均價事實表未涵蓋。"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"SBC 占營收 0.8%、占 GAAP 營業利益 3.3%；回購使股數淨減少，淨稀釋率為負。"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購；現金去向以擴產與回購為主，已在判斷理由中交代。"}}}},"q5_valuation":{"verdict":"中性。現價要求 FY29 營業利益接近管理層目標下緣，且之後利益率不大幅回落；前半我相信，後半只信一半。","reasoning":"現價 284.66，對 FY27 共識 13.38 的前瞻本益比 21.3 倍，對 FY28 為 17.8 倍、對 FY29 為 14.8 倍；PEG 約 1.0（三年共識 EPS 年化約 21%）。我相信前半，因為指引維持、訂單加速；不完全相信後半，因為 FY23 營益率只有 5.2%。近三個月 FY1 上修 26.5% 很可能是財年切換造成：7 月底快照的 FY1 仍是 FY26，10.58 與 FY26 調整後 EPS 10.76 相近，因此不當作上修證據；最近兩份快照之間，FY1 −0.6%、FY2 0%、FY3 +0.4%，共識實際上約持平。歷史分位：P/S 位於 4 個年度端點的 39.5 分位；本益比分位為 0，是因 FY23 盈餘低谷讓早年本益比失真，不採用。短期上檔：FY28 共識 15.96 乘現行前瞻 21 倍約 335，約 +18%。中期上檔：Base 終端約 426，約 +50%。成長熄火測試三案（FY29 後成長降到 15%、10%、5%，終端本益比分別 17、15、12 倍）中，兩案終端價高於現價，一案低於現價。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_fy1_pct","f_consensus_rev_fy2_pct","f_consensus_rev_fy3_pct","f_consensus_rev_3m_fy1_pct","f_pe_current","f_pe_percentile","f_ps_percentile","f_ev_s_fwd"],"verdict_values":{"valuation":{"basis":"前瞻本益比（FY1＝FY2027E 調整後 EPS）與 PEG，P/S 年度端點分位作輔助","tier":"特殊合金／航太材料","peers":{"expanded":false,"reason":"事實表只有同業利潤率，未涵蓋同業本益比，不跨層級借用。"},"fwd_pe":21.28,"peg":1.0,"percentile_5y":39.5,"val_light":"🟡","val_light_derivation":"PEG 約 1.0（21.3 倍÷三年 EPS 年化約 21%），落在合理區下緣。但分母是歷史最高利益率下的盈餘，FY23 營益率只有 5.2%，加上週期折價後結論停在中性。分位採 P/S 年度端點的 39.5（不是五年日頻）；本益比分位 0 因 FY23 盈餘低谷失真，不採用。","upside_short_pct":18,"upside_mid_pct":50,"denominator_disputed":false,"denominator_note":"FY1 分母落在公司指引區間內，不是一次性盈餘；利益率高檔的風險已放進 Bear 情境，不當作分母爭點。"}}},"q6_how_wrong":{"verdict":"🟡：最可能看錯的地方，是把週期高點的價格力當成結構性的。","reasoning":"最強的三個反證詳見反證紀錄。第一，航太週期反轉，疊加本公司與 ATI 的新產能在 FY29–30 上線，長約不再漲價，EPS 退回 FY26 水準。第二，獲利成長，但現金轉換率下滑，回購又在高價區執行。第三，市場半年下殺 33% 的原因事實表未涵蓋，可能有本包看不到的負面資訊。股價已跌破 52 週與 104 週均線（418、317），仍在 250 週均線 168 之上；RSI 11 屬極度超賣，但不構成進場理由。","fact_refs":["f_week26_return_pct","f_rsi14","f_ma_w52","f_ma_w104","f_ma_w250","f_ma_state"],"verdict_values":{"trap":{"verdict":"🟡","label":"利益率高檔的週期風險"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":13.38,"pe":21.28,"basis":"FY1＝FY2027E（6 月財年）調整後 EPS 共識；現價與終端都用前瞻一年口徑"},"eps":{"bull":[14.0,17.2,21.0,24.0,27.0],"base":[13.3,15.6,18.6,20.6,22.4],"bear":[12.6,12.8,11.0,9.5,10.5]},"pe":{"bull":24,"base":19,"bear":12},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0.28,"net_buyback":1.5},"second_stage":{"bull_cagr_pct":10,"base_cagr_pct":6},"max_dd":{"lo":-62,"hi":-42,"basis":"Bear 終端價約 126（EPS 10.5×12 倍），較現價 −56%；自 8/1 引用價 520.92 至今已回撤約 45%。上一輪谷底 FY23 營益率 5.2%、EPS 1.14，若完整重演會比 Bear 更深，因此下緣取 −62%；上緣 −42% 對應國防撥款延宕加商用去庫存的中度修正。","trigger_time":null},"basis":{"bull":"管理層超標：期中選舉後國防補單，長約續約大幅調價，FY29 營業利益超過目標上緣，擴產全數被吸收，終端 24 倍。","base":"FY27–FY29 貼近共識，FY29 營業利益約達管理層目標下緣；FY30–31 擴產加量但漲價放緩，終端 19 倍略低於現行前瞻 21.3 倍。同業現值本益比事實表未涵蓋。EPS 路徑已含部分回購效果，淨回購殖利率只計 1.5% 以免重複。","bear":"國防撥款延宕拉長、商用航太去庫存，本公司擴產與 ATI 新產能在 FY29–30 遇上需求放緩，長約不再漲價，EPS 回落到 FY26 水準；終端 12 倍，取成長熄火降到 5% 的情境。"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"上一輪谷底 FY23 營益率 5.2%、EPS 1.14；同業 ATI 擴產，本公司擴產也在 FY28 初上線。","assumption":"長約漲價與 37% 以上的 SAO 營益率能延續到 FY30 以後。","consequence":"若 FY29–30 航太去庫存疊加新產能上線，長約不再漲價，EPS 回落到 10–11，本益比壓到 12 倍，股價約 126，較現價 −56%。","ruling":"部分採納，已放進 Bear 30%。但 Q1 法說稱除本公司與少數幾家外沒有新產能，積壓訂單逾 16,000 架，週期反轉最快也在 FY29 之後；不採納「一兩年內就反轉」的說法。","watch":"長約續約價格、商用航太訂單年增率、ATI 新產能投產時點","evidence_refs":["competitive_share_entrants#1"],"fact_refs":["f_kpi7_sao_segment_operating_ma","f_peer_ati_operating_margin_pct"]},{"view":"論點成功但股東經濟變差","evidence":"自由現金流÷淨利從 FY24 0.96 降到 FY26 0.68；Q1 自由現金流 −24.8；Q1 回購 133.9 落在 476–521 價位區間；本季起停止揭露出貨量。","assumption":"營業利益成長會等比例轉成每股現金。","consequence":"營業利益達標，但擴產與營運資金吃掉現金，高價回購折損價值，每股自由現金流成長落後 EPS。","ruling":"部分採納。FY27 自由現金流指引 400–430 若達成，對 FY27 淨利約 650（共識 EPS×現股數推估），轉換率約 0.63，仍然偏低。擴產完工後 FY28 起資本支出應回落，轉換率能否回升是可以驗證的。","watch":"FY27 自由現金流是否達 400；FY28 資本支出是否回落","fact_refs":["f_kpi3_free_cash_flow","f_kpi4_sbc","f_consensus_eps_fy1","f_shares_diluted_m"]},{"view":"價格已反映太多","evidence":"8 月初一家聚合站的賣方共識目標價 465.80，低於當時股價 520.92 約 16%；各聚合站共識數字不一致，另一來源為 625.88、區間 540–700。","assumption":"高本益比可以延續。","consequence":"倍數向下修正。","ruling":"反駁。這條證據描述的是 8 月初的狀況，當時以現行 FY27 共識計約 39 倍前瞻本益比；現價 284.66 已比該最低共識目標價再低約 39%，前瞻本益比 21.3 倍，「反映太多」的風險在本輪下殺中已大致釋放。保留的部分：聚合站口徑不一，目標價不作為依據。","watch":"FY2 共識是否開始下修","evidence_refs":["capital_markets_pricing#1"],"fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_week26_return_pct"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟠","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟠","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 476.42 → 本次 284.66（-40.3%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=476.42","side_b":"本次 price_at_dd=284.66","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]角色由 dd_decision.py 機械路由：前份 核心 → 本次 衛星","cause":"方法變動","prior_field":["dca_role"],"side_a":"前份 dca_role=核心","side_b":"本次 dca_role=衛星","ruling":"角色是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。單獨改回前份值即還原前份角色：均線 ✅→🟠。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 476.42 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 476.42 美元：Bull 價 1,056、Bear 價 187.5，五年期望值 +34.7%，基準年化 8.4%，不對稱比 1.7","side_b":"本次情境、股價仍用 476.42 美元：Bull 價 648、Bear 價 126，五年期望值 −17.9%，基準年化 −2.2%，不對稱比 0.41","ruling":"先換情境、股價不動：五年期望值少 52.6 個百分點，基準年化少 10.6 個百分點。不對稱比由 1.7 變為 0.41。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 476.42 美元：五年期望值 −17.9%，基準年化 −2.2%，不對稱比 0.41","side_b":"本次情境、股價 284.66 美元：五年期望值 +37.5%，基準年化 8.4%，不對稱比 1.91","ruling":"再換股價、情境不動：起點價下跌 40.3%，五年期望值多 55.3 個百分點，基準年化多 10.6 個百分點，不對稱比由 0.41 升到 1.91。合計五年期望值比前份多 2.8 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"前份裁決、訊號與估值結論","cause":"價格變動","prior_field":["signal","val","p_bull_pct","p_bear_pct","max_dd_pct","cycle_position"],"side_a":"前份（2026-09-01，股價 476.42）：進場、核心；訊號 A；估值中性；Bull 25%／Bear 30%；最大回撤 −68%；未設循環位置。","side_b":"本次（股價 284.66）：訊號 A 不變；估值結論仍為中性，但前瞻本益比從約 35 倍降到約 21 倍；Bull 25%／Base 45%／Bear 30% 不變；回撤區間改以現價起算 −42% 至 −62%；循環位置仍不設；裁決與部位大小在均線轉弱後重新決定。","ruling":"股價下跌約 40%，但營業利益指引與訂單都沒有轉弱，基本面結論沿用。前份在約 35 倍給中性，本次在 21 倍仍給中性，是因為把利益率位於歷史高點的週期折價納入。回撤改以現價為基準：前份估的 −68%，自 8 月引用價起算已實現約 −45%。","evidence_level":"價格為已實現資料；指引來自公司新聞稿","settle_metric":"Q2 FY27 SAO 營業利益與商用航太訂單","if_then":["若 Q2 FY27 SAO 營業利益≥214 且商用航太訂單續年增，加第二批","若 Q2 FY27 SAO 營業利益<214，停止加碼並把 Bear 機率上調至 35%"],"evidence_refs":[]},{"axis":"護城河方向","cause":"新證據","prior_field":["moat_trend"],"side_a":"前份：擴大（↑）","side_b":"本次：穩定（→）","ruling":"Q1 FY27 法說 CEO 明言長約份額大致不變、沒有搶份額；價格上漲主要來自供需缺口，屬可逆來源；本公司與 ATI 都在擴產。進入門檻（認證、合格供應商少）沒有改變，所以判穩定，而不是縮減。","evidence_level":"法說原話與同業擴產報導","settle_metric":"長約續約價格與同業營益率差距","if_then":["若下一份大型長約續約價格再上調且 ATI 營益率差距維持 7 個百分點以上，可回到擴大","若長約續約價格持平，改判縮減並減碼至半倉"],"evidence_refs":["competitive_share_entrants#1"]},{"axis":"價值陷阱、跑道與類別","cause":"方法變動","prior_field":["trap","runway_post_y5","archetype"],"side_a":"前份：陷阱風險低（🟢）、五年後跑道寬（🟢）、品質複利成長","side_b":"本次：陷阱風險中（🟡）、五年後跑道中（🟡）；主類別仍為品質複利成長，另加註循環性為副類別","ruling":"本次逐項套用衰退信號。EPS 成長遠高於營收成長一項亮燈：FY23→FY26 營收年化約 7%，EPS 由 1.14 升到 10.52；FY26 自由現金流÷淨利 0.68 低於 0.75，但只有一年，列觀察。跑道方面，以目標產率 2,100 架計，16,000 架積壓約 7–8 年，FY31 後的成長取決於新訂單與第二曲線，目前沒有量化證據。","evidence_level":"年度財報序列與法說口述","settle_metric":"FY27 自由現金流÷淨利、主機廠新訂單","if_then":["若 FY27 自由現金流÷淨利再低於 0.75，陷阱風險維持中並停止加碼","若國防或燃氣渦輪營收占比出現可量化的雙位數成長，跑道可回到寬"],"evidence_refs":[]},{"axis":"唯一致命點（Single Thing）","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設定（null）","side_b":"主要航太長約續約價格持平或下調","ruling":"前份把風險分散在三條風險項中；本次依最大單一敏感度的原則，指定價格為唯一致命點。產能滿載下量的成長只有擴產約 7%，利益率擴張幾乎全靠價格。一旦發生即減碼至半倉。","evidence_level":"法說：一份長約已達原則協議、另有兩份談判中","settle_metric":"每季法說的長約續約描述","if_then":["若續約價格持平或下調，減碼至半倉","若三份續約全部上調，維持部位"],"evidence_refs":[]},{"axis":"清倉與減碼門檻","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設清倉指標（null）","side_b":"新設五條：SAO 營益率連 4 季低於 32%、商用航太訂單連 3 季年減、FY27 營業利益低於 850、長約續約不漲價、擴產延後逾 6 個月；前兩條同時發生即清倉，其餘任一發生即減碼。","ruling":"前份只有假設與風險的警戒值，沒有可執行的出場線；本次補上，讓減碼與清倉綁定可觀察的數字。","evidence_level":"公司新聞稿與法說","settle_metric":"SAO 營益率與商用航太訂單","if_then":["SAO 營益率連 4 季低於 32% 且訂單連 3 季年減，清倉","FY27 營業利益低於 850，減碼至半倉"],"evidence_refs":[]},{"axis":"加碼重啟條件","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"已進場核心角色，無rearm觸發；加碼觸發見§13b","side_b":"Q2 FY27 財報（2027-01 下旬）SAO 營業利益≥214 且商用航太訂單續年增，或週收盤站回 104 週均線（約 317），任一成立即恢復正常加碼","ruling":"股價跌破 104 週均線，加碼節奏需要明確的重啟條件；以首個基本面驗證點或趨勢修復二擇一。","evidence_level":"均線與指引為已揭露數字","settle_metric":"Q2 FY27 SAO 營業利益、週收盤價","if_then":["任一條件成立，恢復加碼至目標部位","兩者皆未成立，維持分批節奏，不追價"],"evidence_refs":[]},{"axis":"管理層前季財測與本季實績","cause":"新證據","prior_field":null,"side_a":"2026-07-30 Q4 FY26 法說 CFO：Q1 總營業利益 195–200 百萬美元、SAO 218–222","side_b":"Q1 實績總營業利益 196.4（區間下半）、SAO 216.3（低於區間下緣）；Q2 SAO 指引 214–218，與 Q1 持平；CEO 稱達成 98–99%","ruling":"可調和，屬程度差異：總數達標，SAO 小幅未達。但 Q2 SAO 指引沒有季增，與 CEO「量價皆更強」的說法有落差，列為短期驗證點。","evidence_level":"公司新聞稿與法說原話","settle_metric":"Q2 FY27 SAO 營業利益","if_then":["若 Q2 SAO 營業利益≥218，維持加碼節奏","若 Q2 SAO 營業利益<214，停止加碼"],"evidence_refs":[]},{"axis":"結構件客戶下單","cause":"新證據","prior_field":null,"side_a":"2026-07-30 Q4 FY26 法說 CEO：結構件客戶下單仍謹慎，低於預期需求","side_b":"2026-10-22 Q1 FY27 法說 CEO：結構件與通路訂單季增 23%、年增 49%，客戶庫存下降","ruling":"一致：前季點名的保留項本季轉強，屬兌現而非改口。","evidence_level":"法說口述百分比，未給絕對數","settle_metric":"結構件與通路訂單年增率","if_then":["若 Q2 結構件與通路訂單續年增，維持 H2","若轉為年減，H2 降為削弱並停止加碼"],"evidence_refs":[]},{"axis":"國防需求與國防訂單","cause":"新證據","prior_field":null,"side_a":"CEO：國防終端需求大，與國防部的直接接觸增加，F/A-XX 有實質材料內容","side_b":"國防訂單季減且年減，直接客戶缺撥款無法下單；國防量偏少使產線調度受影響","ruling":"可調和，但時點不確定：需求存在，撥款時點未知。決勝數據要到期中選舉後預算明朗才會出現，在 2027 年上半之前無法裁決。","evidence_level":"法說口述","settle_metric":"國防訂單年增率","if_then":["若 2027 年 3 月前預算明朗且國防訂單轉為年增，維持 Bull 25%","若至 2027 年 6 月國防訂單仍年減，把國防補單從 Bull 假設中移除，Bull 機率降至 20%"],"evidence_refs":[]},{"axis":"量價揭露","cause":"新證據","prior_field":null,"side_a":"管理層稱量、價與需求展望都比上季更強","side_b":"本季起停止揭露出貨量，量價拆分無法從外部驗證（Q1 FY27 法說 CEO 自述）","ruling":"列為未證、持續監測。揭露減少本身是負面訊號；在恢復揭露出貨量或 SAO 營益率連續創高之前，不採信「量也在增」的說法，只採信營業利益。","evidence_level":"法說原話","settle_metric":"SAO 營業利益與營益率","if_then":["若 SAO 營益率連 2 季低於 36% 且仍不揭露出貨量，停止加碼","若恢復揭露且出貨量年增，維持現判"],"evidence_refs":[]},{"axis":"醫療終端","cause":"新證據","prior_field":null,"side_a":"2026-07-30 Q4 FY26 法說 CEO：醫療終端本財年首度季增","side_b":"Q1 FY27 PEP 營收年減 5%，營業利益 7.3（去年同期 9.4），主因鈦醫療銷售下滑；Q2 FY26 時鈦醫療經銷需求已疲弱","ruling":"可調和：醫療占比小，PEP 營業利益不到全公司 4%，不影響主論點；但前季「醫療轉好」的說法本季沒有延續。","evidence_level":"公司新聞稿與法說","settle_metric":"PEP 季營業利益","if_then":["若 PEP 季營業利益連 2 季低於 5 百萬，把醫療從第二曲線清單移除","若 PEP 回到 9 百萬以上，維持現判"],"evidence_refs":["supply_demand_durability#3"]},{"axis":"共識上修訊號","cause":"方法變動","prior_field":null,"side_a":"近三月 FY1 共識上修 26.5%（10.58→13.38）","side_b":"7 月底快照的 FY1 很可能仍是 FY26（10.58 接近 FY26 調整後 EPS 10.76），10 月快照已切換為 FY27；最近兩份快照 FY1 −0.6%、FY2 0%、FY3 +0.4%","ruling":"採 B 側：26.5% 視為財年切換，不當作上修證據；共識實際修正約持平。","evidence_level":"兩份共識快照","settle_metric":"下一次快照的 FY2 共識修正","if_then":["若 FY2 共識下修超過 3%，視為賣方開始下修，停止加碼","若 FY2 上修超過 3%，作為上調 Bull 機率的依據"],"evidence_refs":[]},{"axis":"股價與基本面背離","cause":"價格變動","prior_field":null,"side_a":"市場面：26 週股價 −33%，自 8/1 引用價約 −45%，跌破 52 週與 104 週均線","side_b":"公司面：FY27 指引維持，商用航太訂單年增 25%，CEO 稱需求與價格展望都比上季更強","ruling":"不可調和，需要裁決。現在就賣的最強論證：市場可能先看到航太週期見頂或國防預算遞延的跡象，而本公司訂單資料只有口述百分比，出貨量也停止揭露，外部無法驗證；下殺原因事實表也未涵蓋。裁決：偏向公司資料，但不重押，以分批取代一次建足，並以 Q2 FY27 財報作為第一個決勝點。","evidence_level":"價格為已實現資料；基本面為公司口述","settle_metric":"Q2 FY27 商用航太訂單與 SAO 營業利益","if_then":["若 Q2 訂單續年增且 SAO 營業利益≥214，加第二批","若 Q2 訂單轉為年減或 SAO 營業利益<214，停止加碼並減碼至三分之二","若股價續跌但 Q2 數據完好，按計畫分批反買，不停損"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"SAO 調整後營益率守住 35%","type":"假設驗證","maps_to":"H1","metric":"SAO 調整後營業利益率（不含附加費）","threshold":"連 2 季低於 35%","action":"停止加碼","source_freq":"季報新聞稿，每季","date":"2027-01"},{"n":2,"text":"商用航太訂單維持年增","type":"假設驗證","maps_to":"H2","metric":"商用航太訂單年增率（法說口述）","threshold":"連 2 季年減","action":"停止加碼","source_freq":"法說，每季","date":"2027-01"},{"n":3,"text":"FY27 營業利益指引下緣不下修、擴產如期","type":"假設驗證","maps_to":"H3","metric":"FY27 營業利益指引、擴產進度","threshold":"指引下緣低於 850 或擴產延後逾 6 個月","action":"減碼至三分之二","source_freq":"季報新聞稿，每季","date":"2027-01"},{"n":4,"text":"SAO 營業利益未達指引下緣","type":"風險","maps_to":"R1","metric":"SAO 季營業利益對比當季指引","threshold":"Q2 FY27 低於 214（Q1 已低於原指引下緣 218）","action":"停止加碼","source_freq":"季報新聞稿，每季","date":"2027-01"},{"n":5,"text":"原料或關稅成本轉嫁失效","type":"風險","maps_to":"R4","metric":"SAO 調整後營益率年變動，且公司歸因於原料或關稅","threshold":"年減 3 個百分點以上","action":"減碼至三分之二","source_freq":"季報新聞稿與法說，每季","date":null,"evidence_refs":["geo_supply_chain#0","geo_supply_chain#1","reg_tariff_export#1"]},{"n":6,"text":"主要航太長約續約價格持平或下調","type":"Single Thing","maps_to":"single_thing","metric":"長約續約價格方向","threshold":"任一大型長約持平或下調","action":"減碼至半倉","source_freq":"法說，每季","date":null},{"n":7,"text":"Q2 FY27 財報確認後加第二批","type":"加碼","maps_to":"H1","metric":"SAO 營業利益與商用航太訂單","threshold":"SAO 營業利益≥214 且商用航太訂單續年增","action":"加第二批（目標部位三分之一）","source_freq":"季報新聞稿，每季","date":"2027-01"},{"n":8,"text":"恢復正常加碼節奏","type":"估值rearm","maps_to":"H2","metric":"Q2 FY27 SAO 營業利益與訂單，或週收盤價","threshold":"SAO≥214 且訂單續年增，或週收盤站回 104 週均線（約 317）","action":"恢復加碼至目標部位","source_freq":"季報與週線","date":"2027-01"},{"n":9,"text":"利益率與訂單同時反轉","type":"清倉","maps_to":"H1","metric":"SAO 營益率與商用航太訂單","threshold":"SAO 營益率連 4 季低於 32% 且商用航太訂單連 3 季年減","action":"清倉","source_freq":"季報新聞稿與法說，每季","date":null},{"n":10,"text":"FY27 實際營業利益未達指引下緣","type":"減碼","maps_to":"H3","metric":"FY27 全年營業利益","threshold":"低於 850 百萬美元","action":"減碼至半倉","source_freq":"年度新聞稿","date":"2027-07"},{"n":11,"text":"Q2 FY27 財報後複審","type":"複審日期","maps_to":"H1","metric":"整體論點","threshold":"財報公布後兩週內","action":"重跑判斷","source_freq":"一次","date":"2027-01"}],"kill_metrics":[{"metric":"SAO 調整後營業利益率（不含附加費）","bear_threshold":"連 4 季低於 32%","window":"FY27–FY29 每季","source":"公司季報新聞稿","last_status":"ok"},{"metric":"商用航太訂單年增率（法說口述）","bear_threshold":"連 3 季年減","window":"FY27–FY29 每季","source":"每季法說逐字稿","last_status":"ok"},{"metric":"FY27 全年營業利益","bear_threshold":"低於 850 百萬美元","window":"FY27（約 2027-07 下旬公布）","source":"公司年度新聞稿","last_status":"ok"},{"metric":"主要航太長約續約價格","bear_threshold":"出現持平或下調的續約","window":"2026-10 至 2028-06","source":"每季法說逐字稿","last_status":"ok"},{"metric":"擴產案完工時點","bear_threshold":"延後至 FY28 開始後逾 6 個月","window":"2027-07 至 2028-01","source":"公司新聞稿與法說","last_status":"ok"}],"evidence_dismissed":[{"ref":"channel_business_model_shift#1","reason":"此事件是 FY2024 第三季 Latrobe 經銷單位 14.1 百萬美元商譽全額減損，距今逾兩年半，金額約為 FY26 營業利益的 2%；證據本身也註明不是 2026 年的通路轉型，10-K 同章節描述現行通路沒有結構變動。"}],"action_conditions":{"rearm_trigger":"Q2 FY27 財報（2027-01 下旬）SAO 營業利益≥214 且商用航太訂單續年增，或週收盤站回 104 週均線（約 317），任一成立即恢復正常加碼","exec_line":"既有持股續抱，不因回撤停損。新資金分三批：現價區先建三分之一；Q2 FY27 財報確認 SAO 營業利益≥214 後加第二批；週收盤站回 104 週均線後加第三批。Single Thing 發生即減碼至半倉。"}},"decision_inputs":{"signal":"A","ma":"🟠","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"8–10 月股價下跌約 45%，同期 FY27 營業利益指引維持，商用航太訂單年增 25%、結構件與通路年增 49%，空中交通量季增 14%，管理層對量價與 FY29 目標的信心上升。市場若擔心燃油價格壓抑航空需求，目前訂單資料並不支持；但市場下殺的完整原因事實表未涵蓋。","momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":true,"wait_for_price":null,"wait_for_price_condition":null,"prior_verdict":"進場","prior_role":"核心"},"decision_out":{"verdict":"進場","role":"衛星","row_hit":"9b","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='A'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟠'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='A'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=8–10 月股價下跌約 45%，同期 FY27 營業利益指引維持，商用航太訂單年增 25%、結構件與通路年增 49%，空中交通量季增 14%，管理層對量價與 FY29 目標的信心上升。市場若擔心燃油價格壓抑航空需求，目前訂單資料並不支持；但市場下殺的完整原因事實表未涵蓋。"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='A', runway='🟡', val='🟡', moat_trend='→', week26=-33.32, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position=None, moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":false,"basis":"signal='A', val='🟡'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":false,"basis":"signal='A', val='🟡', ma='🟠'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":true,"basis":"signal='A', val='🟡', ma='🟠'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='A', val='🟡', ma='🟠'"},{"row":"QC-49","condition":"qc49_inherit_prior=True 但前次裁決與矩陣機械輸出方向相同，無需承繼","hit":false,"basis":"prior_verdict='進場', 矩陣機械輸出='進場'"}],"pacing":[],"holding_cap":null,"requires_critic":[]},"thesis":{"H":[{"id":"H1","text":"擴產上線前，SAO 調整後營益率（不含附加費）維持 35% 以上，代表定價來自供給缺口與長約重訂，而不是單季產品組合。","2y":"FY27–FY28 各季≥35%（Q1 FY27 為 37.7%）","5y":"FY31 擴產全數貢獻後≥32%","10y":null,"threshold":"連 2 季低於 35% 為削弱；連 4 季低於 32% 為反轉","source":"季報新聞稿與每季法說（SAO 部門數字）","drift_rule":"連 2 季低於 35%"},{"id":"H2","text":"商用航太下單仍在加速：結構件、通路與引擎訂單持續年增，客戶下單量還沒跟上主機廠產率。","2y":"FY27–FY28 商用航太訂單每季年增（Q1 FY27 年增 25%，結構件與通路 +49%、引擎 +22%）","5y":"FY31 航太國防仍占營收約六成以上，訂單未轉負","10y":null,"threshold":"商用航太訂單年增率連 2 季轉負為削弱；連 3 季轉負為反轉","source":"每季法說口述（公司不揭露絕對金額，且已停止揭露出貨量）","drift_rule":"連 2 季年減"},{"id":"H3","text":"FY27 營業利益 850–880 百萬美元與 FY29 1,200–1,300 百萬美元目標可達，擴產案於 FY28 初如期完工。","2y":"FY27 實際≥850；FY28 初擴產開機","5y":"FY29 營業利益≥1,200；FY30 擴產帶來增量營業利益約 150","10y":null,"threshold":"FY27 指引下緣下修為削弱；FY29 目標下修至 1,100 以下為反轉；擴產延後逾 6 個月為削弱","source":"季報新聞稿與每季法說","drift_rule":"指引下緣下修或擴產延後"}],"R":[{"id":"R1","text":"SAO 營業利益連續低於指引：Q1 已低於 Q4 FY26 法說給的 218–222 下緣，Q2 指引 214–218 也沒有季增。","h_ref":"H1","clock":"⚡","threshold":"連 2 季低於當季指引下緣","evidence_refs":[]},{"id":"R2","text":"ATI 等同業新產能加上本公司擴產，2028 年後產業提價紀律鬆動，長約續約漲幅縮小。","h_ref":"H1","clock":"🔥","threshold":"續約漲幅連 2 次降到個位數為削弱；出現持平或折價續約為反轉","evidence_refs":["competitive_share_entrants#1"]},{"id":"R3","text":"航太週期反轉：主機廠訂單淨額轉弱，積壓訂單相對交付的年數下降，與擴產上線時點撞在一起。","h_ref":"H2","clock":"🐢","threshold":"積壓÷年交付由約 10 年降到 6 年以下開始減碼；降到 4 年以下大幅減碼","evidence_refs":[]},{"id":"R4","text":"關鍵原料部分來自政經不穩國家且可能沒有替代來源，關稅與出口管制變動導致附加費轉嫁失效。","h_ref":"H1","clock":"🔥","threshold":"SAO 營益率年減 3 個百分點以上，且公司歸因於原料或關稅","evidence_refs":["geo_supply_chain#0","geo_supply_chain#1","reg_tariff_export#1"]},{"id":"R5","text":"國防撥款遲滯拖過期中選舉，國防量持續偏少，影響產線調度與產品組合。","h_ref":"H2","clock":"⚡","threshold":"至 2027 年 6 月國防訂單仍年減","evidence_refs":[]}],"single_thing":{"description":"主要航太長約續約（法說稱一份已達原則協議、另有兩份大型合約談判中）出現價格持平或下調。","why_fatal":"情境樹最大的單一敏感度在價格：產能滿載下量的成長受限於擴產約 7%，FY29 目標的利益率擴張幾乎全靠價格；長約占航太業務多數，一份大型長約不漲價，就代表供需缺口論點失效。","if_happens":"減碼至半倉，並把 Base 情境終端本益比由 19 倍降到 15 倍重算。","how_monitor":"每季法說的長約續約描述，以及 SAO 營益率","probability":"約 10%（12–24 個月）"}},"appendix_a":{"growth_durability":7,"quality_score":7,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":17.84,"peg_fy2":0.84,"stress":{"pass":2,"total":3}},"eps_meta":{"base_eps_path":{"FY2026A":10.76,"FY2027E":13.38,"FY2028E":15.96,"FY2029E":19.2},"fy_end_month":6,"eps_basis":"調整後（non-GAAP）EPS，財年結束於 6 月。基期 FY2026A 10.76 取自 FY26 年度結果報導；GAAP 稀釋 EPS 為 10.52。"},"catalysts":[{"date":"2026-11","date_precision":"month","type":"macro","event":"美國期中選舉後國防預算明朗化","impact":"中","watch":"國防訂單是否轉為年增"},{"date":"2027-01","date_precision":"month","type":"guidance","event":"Q2 FY27 財報與法說","impact":"高","watch":"SAO 營業利益是否≥214、商用航太訂單是否年增、長約續約價格"},{"date":"2027-03","date_precision":"quarter","type":"other","event":"大型航太長約續約（一份已達原則協議、兩份談判中）","impact":"高","watch":"續約價格是否再上調"},{"date":"2027-07","date_precision":"month","type":"capacity","event":"擴產案完工，FY28 初開機","impact":"高","watch":"是否如期、在預算內"},{"date":"2027-07","date_precision":"month","type":"guidance","event":"FY27 全年結果與 FY28 指引","impact":"高","watch":"FY27 營業利益是否≥850、自由現金流是否達 400"}]}
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
