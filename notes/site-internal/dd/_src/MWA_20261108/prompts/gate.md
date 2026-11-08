你是 DD 管線 v20 的判斷層閘（gate），標的 MWA（20261108）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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
- `f_kpi0_net_sales_gaap`（q1_business）｜Net sales（GAAP）＝376.5 USD M｜期間與口徑：Q4 FY2026（季末 2026-09-30，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 https://ir.muellerwaterproducts.com/press-releases/2026/11-04-2026-211024211（同文 8-K Ex.99.1）（numbers.latest_quarter_kpis.items[0]，as_of Q4 FY2026（季末 2026-09-30，公告於 2026-11-04））
  - 註記：未查得（本次未取得可靠共識值，不填造）
- `f_kpi1_adjusted_operating_margi`（q1_business）｜Adjusted operating margin（Non-GAAP）＝21.9 %｜期間與口徑：Q4 FY2026（季末 2026-09-30，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 https://ir.muellerwaterproducts.com/press-releases/2026/11-04-2026-211024211（同文 8-K Ex.99.1）（numbers.latest_quarter_kpis.items[1]，as_of Q4 FY2026（季末 2026-09-30，公告於 2026-11-04））
  - 註記：未查得（本次未取得可靠共識值，不填造）
- `f_kpi2_gaap_operating_margin`（q1_business）｜GAAP operating margin＝19.4 %｜期間與口徑：Q4 FY2026（季末 2026-09-30，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 https://ir.muellerwaterproducts.com/press-releases/2026/11-04-2026-211024211（同文 8-K Ex.99.1）（numbers.latest_quarter_kpis.items[2]，as_of Q4 FY2026（季末 2026-09-30，公告於 2026-11-04））
  - 註記：未查得（本次未取得可靠共識值，不填造）
- `f_kpi5_fy2027_guidance_metering`（q1_business）｜FY2027 guidance（不含 metering，FY2026 metering 銷售約 $40M）＝Net sales 1,440–1,470；Adj. EBITDA 378–388（中位 margin 26.3%，+110bps） USD M｜期間與口徑：Q4 FY2026（季末 2026-09-30，公告於 2026-11-04），新聞稿給 FY2027 指引／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司 IR 新聞稿 https://ir.muellerwaterproducts.com/press-releases/2026/11-04-2026-211024211（同文 8-K Ex.99.1）；其他：capex 60–70、FCF >80% adj. net income、SG&A 228–233、利息淨支出 3–5、稅率 24–26%、D&A 48–52（numbers.latest_quarter_kpis.items[5]，as_of Q4 FY2026（季末 2026-09-30，公告於 2026-11-04），新聞稿給 FY2027 指引）
  - 註記：yfinance FY 營收共識 1,502.85（4 位分析師，期別標籤不確定、含 metering，不可直接比較）
- `f_peer_mwa_gross_margin_pct`（q2_moat）｜MWA 毛利率＝38.24 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MWA.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_mwa_operating_margin_pct`（q2_moat）｜MWA 營業利益率＝21.54 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MWA.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_wts_gross_margin_pct`（q2_moat）｜WTS 毛利率＝48.87 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.WTS.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_wts_operating_margin_pct`（q2_moat）｜WTS 營業利益率＝19.73 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.WTS.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_xyl_gross_margin_pct`（q2_moat）｜XYL 毛利率＝39.79 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.XYL.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_xyl_operating_margin_pct`（q2_moat）｜XYL 營業利益率＝16.06 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.XYL.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_zws_gross_margin_pct`（q2_moat）｜ZWS 毛利率＝50.41 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ZWS.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_zws_operating_margin_pct`（q2_moat）｜ZWS 營業利益率＝22.52 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ZWS.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_bmi_gross_margin_pct`（q2_moat）｜BMI 毛利率＝41.64 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.BMI.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_bmi_operating_margin_pct`（q2_moat）｜BMI 營業利益率＝18.76 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.BMI.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝1.57 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-11-07）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝1.59 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-11-07）
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝0.0 %｜期間與口徑：2026-08-13 → 2026-11-07／FY1 共識 EPS 1.57 → 1.57（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-11-07）
- `f_kpi3_free_cash_flow_q4`（q1_business）｜Free cash flow（Q4 單季）＝96.7 USD M｜期間與口徑：Q4 FY2026（季末 2026-09-30，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 https://ir.muellerwaterproducts.com/press-releases/2026/11-04-2026-211024211（同文 8-K Ex.99.1）（numbers.latest_quarter_kpis.items[3]，as_of Q4 FY2026（季末 2026-09-30，公告於 2026-11-04））
  - 註記：未查得（本次未取得可靠共識值，不填造）
- `f_kpi4_sbc_gaap_fy2026`（q4_capital）｜SBC 占 GAAP 營業利益（FY2026 全年）＝4.7 %｜期間與口徑：FY2026 全年（截至 2026-09-30，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 https://ir.muellerwaterproducts.com/press-releases/2026/11-04-2026-211024211（同文 8-K Ex.99.1）；SBC 全年 13.7M ÷ GAAP op income 290.8M（計算值）；單季 SBC 新聞稿未揭露（numbers.latest_quarter_kpis.items[4]，as_of FY2026 全年（截至 2026-09-30，公告於 2026-11-04））
  - 註記：不適用
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝-112.2 USD m｜期間與口徑：2026-11-08／yfinance 最新一季：總債務 453.8、現金 566.0（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝155.5 m shares｜期間與口徑：2026-11-08／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝24.05 USD｜期間與口徑：2026-11-06（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-11-06（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝15.32 x｜期間與口徑：2026-11-07／分母＝FY1 EPS 1.57，分子＝快照價 24.05｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-11-07）
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝17.06 x｜期間與口徑：2026-11-06（RTH 收盤，UTC）／4 個年度端點內的分位＝0.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-11-06（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝0.0 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝81.2 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝71.2 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ev_m`（q5_valuation）｜目前企業價值 EV（市值＋淨負債）＝3627.6 USD m｜期間與口徑：2026-11-08／市值 3739.8 ＋ 淨負債 -112.2｜kind：realized
  - 來源：—（numbers.capital_structure.ev_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝1.164 %｜期間與口徑：2026-11-08／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-11-08）
- `f_rsi14`（q5_valuation）｜RSI(14)＝63.8｜期間與口徑：2026-11-06（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-11-06（RTH 收盤，UTC））
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝-8.31 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ma_state`（q5_valuation）｜週線均線六態（decision_inputs.ma 必須等於此值）＝🟠｜期間與口徑：2026-11-08／timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）
  - 原文：「price 24.05 / W52 25.46 / W104 25.03 / W250 18.53 / W250 13週斜率 0.87%」

### findings_digest 中方向為負或來源衝突的條目（14 條）
- `competitive_share_entrants#1`（competitive_share_entrants｜方向 -｜狀態 ok）：FY2025 10-K 風險因子：除北美對手外，亦面臨北美以外廠商競爭，強度受匯率、運費與貿易救濟影響。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2025-11-19）｜affects：decision_inputs.bear、moat_trend
- `customer_concentration_credit#0`（customer_concentration_credit｜方向 -｜狀態 ok）：兩大經銷商合計占毛銷售約 37%（FY2025）、38%（FY2024）、35%（FY2023），且無長期合約。
  - 來源：SEC EDGAR 10-K FY2025 Item 1（as_of 2025-11-19）｜affects：thesis.R、decision_inputs.bear
- `customer_concentration_credit#1`（customer_concentration_credit｜方向 -｜狀態 ok）：最大客戶占毛銷售 20%（FY2025、FY2024）、18%（FY2023），應收 $56.5M；第二大客戶 17%，應收 $42.4M。
  - 來源：SEC EDGAR 10-K FY2025 財報附註（as_of 2025-11-19）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：FY2025 10-K 風險因子：美國對 MWA 所有供應國及鋼、鋁、銅等原料課關稅；若再擴大或遭報復，可能須漲價並流失客戶。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2025-11-19）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#1`（reg_tariff_export｜方向 -｜狀態 ok）：MD&A：以色列製產品進口關稅壓抑毛利；Repair 與 Specialty Valve 產品線承擔多數成本；漲價動作預期大致抵銷關稅金額但稀釋毛利率。
  - 來源：SEC EDGAR 10-K FY2025 Item 7（as_of 2025-11-19）｜affects：thesis.R、valuation
- `reg_tariff_export#2`（reg_tariff_export｜方向 -｜狀態 ok）：FY2026 預期直接關稅成本約占銷貨成本 3%，續推高通膨壓力。
  - 來源：SEC EDGAR 10-K FY2025 Item 7 Outlook（as_of 2025-11-19）｜affects：valuation、thesis.R
- `reg_tariff_export#5`（reg_tariff_export｜方向 -｜狀態 ok）：FY2026 Q3 10-Q（2026-06-30）稱 Section 232 關稅升至 50% 對進口零組件與原料（含 Krausz 修理產品）造成實質上行成本壓力，預期於 FY2026 餘期持續負面影響。
  - 來源：SEC EDGAR 10-Q 季度 2026-06-30（as_of 2026-07-30）｜affects：thesis.R、valuation
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：Section 232 steel and aluminum tariffs rose to 50%, putting upward pressure on purchased components and raw material costs, mostly in Repair and Specialty Valve lines
  - 來源：Mueller Water Products Form 10-Q (quarter ended 2026-06-30)（as_of 2026-08-01）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#2`（geo_supply_chain｜方向 -｜狀態 ok）：Ariel, Israel facility had production delays in 2023 after the war; the company added suppliers to mitigate
  - 來源：Mueller Water Products Form 10-K FY2025（as_of 2025-11-01）｜affects：thesis.R、decision_inputs.bear
- `end_markets#0`（end_markets｜方向 -｜狀態 ok）：Water Flow Solutions FY26 Q4 銷售年減3.0%至$210.9M，因量減、價格部分抵銷；全年$817.5M vs $824.9M
  - 來源：Mueller Water Products FY2026 Q4 earnings release (8-K Ex.99.1)（as_of 2026-11-04）｜affects：moat_trend、thesis.H
- `substitute_technology#1`（substitute_technology｜方向 -｜狀態 ok）：10-K 風險因子提及競爭對手若更有效運用 AI 改進營運或創造新產品，MWA 有競爭劣勢風險
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2025-11-19）｜affects：decision_inputs.bear、thesis.R
- `substitute_technology#2`（substitute_technology｜方向 -｜狀態 ok）：10-K 風險因子：運輸成本高，高運輸成本可能使產品相對競爭者的類似或替代產品較不具競爭力
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2025-11-19）｜affects：thesis.R
- `major_events#0`（major_events｜方向 -｜狀態 ok）：2026-11-04 8-K：與 ZENNER USA 簽約，將計量（metering）業務移轉給 ZENNER，預計一次性稅前費用約 $26M，多數在 FY2027 Q1 認列；為業務退出而非收購。
  - 來源：SEC EDGAR 8-K Item 2.05 (2026-11-04)（as_of 2026-11-04）｜affects：thesis.R、decision_inputs.bear
- `ma_merger#0`（ma_merger｜方向 -｜狀態 ok）：2026-11-04 與 ZENNER USA 簽約移轉計量業務（業務退出，非收購），預計一次性稅前費用約 $26M。
  - 來源：SEC EDGAR 8-K Item 2.05 (2026-11-04)（as_of 2026-11-04）｜affects：thesis.R、valuation

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 3 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MWA_20261108/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":50.0,"bear_5y_price":16.9,"p_bull_pct":20,"p_bear_pct":30,"upside_5y_pct":38.4,"ev5y_pct":31.9,"irr_base_pct":6.7,"asym_ratio":2.4,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":1.48,"pe":16.25,"basis":"FY26 調整後 EPS 1.57 扣除關稅退款與 i2O 稅務利益合計 0.09 後的 1.48，屬過去四季實績口徑，與終端年實績本益比同口徑。"},"eps":{"bull":[1.64,1.87,2.1,2.37,2.63],"base":[1.59,1.69,1.83,1.96,2.08],"bear":[1.5,1.39,1.33,1.37,1.41]},"pe":{"bull":19,"base":16,"bear":12},"p":{"bull":20,"base":50,"bear":30},"yield_pct":{"dividend":1.164,"net_buyback":0},"second_stage":{"bull_cagr_pct":8,"base_cagr_pct":5},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### MWA_Q3_2026_Earnings_Call_20260806.md
- 2026-08-06｜Melissa Rasmussen (CFO)｜guidance：CFO 將 FY2026 淨銷售成長財測收窄至 2.8%–3.5%（原話："we are narrowing our consolidated net sales growth guidance to a range of 2.8%"）
- 2026-08-06｜Melissa Rasmussen (CFO)｜guidance：CFO 上調全年 adjusted EBITDA 財測至 $367–372 百萬（原話："we are raising our annual adjusted EBITDA guidance to a new range of"）
- 2026-08-06｜Melissa Rasmussen (CFO)｜guidance：財測中點對應 adjusted EBITDA margin 25.1%（原話："adjusted EBITDA margin of 25.1%, which would represent another annual record for the company"）
- 2026-08-06｜Melissa Rasmussen (CFO)｜guidance：SG&A 財測下修至 $241–245 百萬；稅率財測降至 21%–23%（原話："we are lowering our effective tax rate guidance to between 21% and 23%"）
- 2026-08-06｜Melissa Rasmussen (CFO)｜guidance：重申 capex $60–65 百萬與自由現金流轉換率超過 70% 的展望（原話："continue to expect our free cash flow conversion"）
- 2026-08-06｜Paul McAndrew (CEO)｜guidance：CEO 指出已連續第三季上調全年 adjusted EBITDA 財測（原話："I'm pleased for the third"）
- 2026-08-06｜Paul McAndrew (CEO)｜guidance：CEO 說明收窄銷售財測的原因：訂單出貨預期、住宅建設放緩、去年 Q4 關稅調價的基期（原話："We're also lapping tariff price"）
- 2026-08-06｜Melissa Rasmussen (CFO)｜guidance：WFS 第四季 adjusted EBITDA 預期高於去年同期，但較 Q3 季減（原話："For the WFS segment, we are expecting adjusted EBITDA to be above prior year due to gross margin"）
- 2026-08-06｜Melissa Rasmussen (CFO)｜guidance：WMS 第四季利潤率預期低於去年同期與前一季，因消防栓積壓訂單正常化（原話："For WMS, we're expecting to see lower margins versus the prior year and sequentially."）
- 2026-08-06｜Melissa Rasmussen (CFO)｜guidance：第四季價格實現略低，因基期含去年 Q4 起的關稅調價；仍預期價格成本為正（原話："We have been price/cost positive and continue to expect that, that"）
- 2026-08-06｜Paul McAndrew (CEO)｜guidance：FY2027 財測要到下次財報才給（原話："We don't give our guidance for 2027 until the next earnings call."）
- 2026-08-06｜Melissa Rasmussen (CFO)｜margin：Q3 毛利率 39.4%，年增 110bp，含關稅退款與 i2O 退出成本（原話："gross margin expanding 110 basis points to 39.4%."）
- 2026-08-06｜Melissa Rasmussen (CFO)｜margin：排除前期關稅退款與投資組合優化成本後，調整後毛利率僅比去年 38.3% 高約 30bp（原話："adjusted gross margin was approximately 30 basis points higher than the prior year's gross margin of 38.3%,"）
- 2026-08-06｜Melissa Rasmussen (CFO)｜margin：Q3 adjusted EBITDA $107.4M，margin 27.1%，年增 440bp，驅動為調價、關稅退款與 SG&A（原話："Adjusted EBITDA margin expanded 440 basis points year-over-year to a record 27.1%."）
- 2026-08-06｜Melissa Rasmussen (CFO)｜margin：關稅退款對 Q3 合併貢獻 150bp，WFS 約 140bp、WMS 約 170bp（原話："we had 150 basis point benefit overall for the tariff"）
- 2026-08-06｜Melissa Rasmussen (CFO)｜margin：Q3 稅率 15.7%，含 i2O 退出的一次性稅務利益，約貢獻每股 $0.06（原話："approximately $0.06 per diluted share during the quarter."）
- 2026-08-06｜Melissa Rasmussen (CFO)｜margin：WMS 淨銷售年增 10.3%、adjusted EBITDA margin 年增 650bp 至 28.1%（原話："expanded 650 basis points to a record 28.1% compared with 21.6% in the prior year period."）
- 2026-08-06｜Melissa Rasmussen (CFO)｜margin：WFS 淨銷售年減 0.6%，margin 34.1% 對去年 31%（原話："Net sales were $215.3 million, declining"）
- 2026-08-06｜Melissa Rasmussen (CFO)｜margin：Q3 營收成長主因為調價，量略減（原話："driven primarily by higher pricing across most product lines,"）
- 2026-08-06｜Melissa Rasmussen (CFO)｜risk：IEEPA 關稅退款被更高的 Section 232 關稅取代（影響 Krausz），且不預期再有退款（原話："And we do not expect to have any further tariff refunds."）
- 2026-08-06｜Paul McAndrew (CEO)｜risk：CEO 結語提到需求、關稅與通膨的外部環境不確定性升高，必要時採取行動（原話："We will stay focused"）
- 2026-08-06｜Melissa Rasmussen (CFO)｜risk：CFO 預期第四季新住宅建設更弱，市政維修汰換仍具韌性（原話："While we anticipate softer new residential construction activity during the fourth"）
- 2026-08-06｜Paul McAndrew (CEO)｜risk：聯邦資金退場影響：聯邦占市政投資不到 5%，未來 1–3 年預期無重大變化（原話："we don't see any meaningful change then from the federal funding impact."）
- 2026-08-06｜Melissa Rasmussen (CFO)｜risk：營運資金因庫存投資、通膨與關稅仍偏高（原話："While working capital remains elevated due to inventory investments, inflation and tariffs,"）
- 2026-08-06｜Paul McAndrew (CEO)｜product：specialty valves 占積壓訂單多數，為近年成長最快類別（原話："So specialty valve makes up the majority of our backlog then."）
- 2026-08-06｜Paul McAndrew (CEO)｜product：已推出消防栓更新系統，客戶試用回饋正面，內含漏水檢測功能（原話："We continue to get very positive customer feedback from"）
- 2026-08-06｜Paul McAndrew (CEO)｜product：完成 i2O 北美以外壓力監測業務出售給 GWF AG（原話："we completed the exit of the i2O pressure monitoring business outside of North"）
- 2026-08-06｜Paul McAndrew (CEO)｜customer：資料中心相關工業用水 specialty valves 為成長最快之一，但規模相對小（原話："It's relatively small in the overall size of the business for us, Jeff."）
- 2026-08-06｜Paul McAndrew (CEO)｜customer：資料中心通路為經銷加投資團隊取得核准製造商名單（AML），開始看到進展（原話："We sell through distribution."）
- 2026-08-06｜Paul McAndrew (CEO)｜competition：管理層稱品牌強、定價權佳，有能力抵銷通膨或關稅成本（原話："we have very strong brands and very good pricing power."）
- 2026-08-06｜Melissa Rasmussen (CFO)｜capital_allocation：期末現金 $495M、總債務 $453M，2029 年 6 月前無到期債務（原話："We ended the quarter with $495 million of cash and cash equivalents and $453 million of total debt."）
- 2026-08-06｜Melissa Rasmussen (CFO)｜capital_allocation：前九個月自由現金流 $110.6M，占調整後淨利 59%；capex 前九個月 $43.6M（去年 $32.8M），投入鑄造廠（原話："free cash flow increased $7.6 million to"）
- 2026-08-06｜Paul McAndrew (CEO)｜capital_allocation：本季透過股息與回購回饋股東約 $21M（原話："returning approximately $21 million to shareholders through our quarterly dividend"）
- 2026-08-06｜Melissa Rasmussen (CFO)｜capital_allocation：管理層稱流動性可支應有機投資並尋求有吸引力的收購機會（原話："positioning us well to execute our strategic priorities and pursue attractive"）
- 2026-08-06｜Paul McAndrew (CEO)｜commitment：管理層列出優先事項：高於市場的銷售成長、持續擴大利潤率、紀律性資本配置（原話："drive above-market sales growth, continued expanding margins and maintain disciplined capital"）
- 2026-08-06｜Paul McAndrew (CEO)｜commitment：管理層稱將在有機投資、目標性收購與股東回饋間紀律性配置資本（原話："Finally, we will remain disciplined in allocating capital across organic investments,"）
- 2026-08-06｜Paul McAndrew (CEO)｜commitment：CEO 稱將以 Mueller Operating System 降低複雜度、擴大利潤率並產生現金（原話："reduce complexity, improve business processes, expand margins and generate cash to fund growth"）
- 2026-08-06｜Paul McAndrew (CEO)｜commitment：CEO 稱住宅建設不會永遠低迷，市政與商業策略可抵銷住宅疲弱，住宅回升將是順風（原話："residential construction cannot stay depressed"）

### 問答異常語氣（迴避／改口／保留）
- MWA_Q3_2026_Earnings_Call_20260806.md｜問：FY27 若住宅持續疲弱，市政與 specialty valves 能否支撐成長？（Goldman 代表）｜答法：未回答 FY27 數字，稱 2027 財測下次財報才給；以『相信可抵銷』與住宅終將反彈的定性說法回應
- MWA_Q3_2026_Earnings_Call_20260806.md｜問：資料中心業務目前規模多大？（RBC）｜答法：未給數字，僅答『relatively small』
- MWA_Q3_2026_Earnings_Call_20260806.md｜問：消防栓更新系統的商業化進度與預期營收貢獻？（RBC）｜答法：只談客戶回饋與產品特性，未回答營收貢獻

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 2 | 2 |
| customer_second_source | found | 1 | 2 |
| customer_concentration_credit | found | 3 | 2 |
| supply_demand_durability | found | 2 | 3 |
| regulatory_antitrust | found | 2 | 2 |
| reg_tariff_export | found | 6 | 2 |
| geo_supply_chain | found | 3 | 2 |
| end_markets | found | 4 | 2 |
| substitute_technology | found | 3 | 2 |
| channel_business_model_shift | found | 2 | 2 |
| capital_markets_pricing | found | 4 | 4 |
| major_events | found | 3 | 4 |

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260524","verdict":"A","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"美國水基建結構性需求 + IIJA 政策順風延續：fire hydrant + iron gate valve duopoly 維持 + IIJA 9/30/26 reauthorization 成功或部分延續","columns":{"2Y 驗證點":"FY27 全年 sales ≥ $1.55B (+5%)；IIJA reauthorization 至少 50% 規模延續","5Y 驗證點":"FY30 sales ~$1.85-2.0B（含 IIJA 完整週期 + 鉛水管 $15B 完成）","10Y 驗證點":"FY35 sales ~$2.4-2.7B（含後續政策週期 + 老化基建剛性需求）","具體數字門檻":"FY27 sales ≥ $1.55B；IIJA 9/30/26 reauthorization ≥ 50% 原規模","信息來源":"5/5/26 Q2 法說、IIJA funding tracker","漂移觸發條件":"連 2 季 sales YoY &lt; 2% → 削弱；連 3 季 &lt; 0% → 反轉"}},{"id":"H2","text":"Adj EBITDA margin 結構性擴張至 26-28%：brass foundry 整合完成 + EchoShore mix shift + pricing power 維持","columns":{"2Y 驗證點":"FY27 全年 adj EBITDA margin ≥ 25%；FY27 adj EBITDA ≥ $390M","5Y 驗證點":"FY30 adj EBITDA margin ≥ 26%；EBITDA ≥ $480M","10Y 驗證點":"FY35 adj EBITDA margin ≥ 27%；EBITDA ≥ $650M","具體數字門檻":"FY27 adj EBITDA margin ≥ 25%；EchoShore subscription 年化 &gt; $100M","信息來源":"FY26 Q2 法說（margin 25.3% +210bps）","漂移觸發條件":"連 2 季 adj EBITDA margin &lt; 23% → 削弱；連 3 季 &lt; 21% → 反轉"}},{"id":"H3","text":"Fwd PE 從 17x 維持或微升至 20-22x：基本面持續驗證 + IIJA 政策確定性提升 + smart water 占比擴大支撐 multiple expansion","columns":{"2Y 驗證點":"FY27 末 trailing PE ~20-22x（股價適度上漲 + EPS 兌現）","5Y 驗證點":"FY30 trailing PE 20x（成長放緩至 8-10% CAGR 對應）","10Y 驗證點":"FY35 PE 18-20x（mature 公用事業相關等級）","具體數字門檻":"FY27 末 trailing PE ≥ 20x 且 EBITDA margin ≥ 25%","信息來源":"歷史對標 WTS 2018-2023 倍數軌跡","漂移觸發條件":"5Y 假設，連 4 季 TTM 偏離 ≥ 5% 才削弱（QC-35）"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"Brass / 銅 / 鋼 tariff outpace pricing power — Trump 2.0 升級 232 條款 + raw material 成本 +20%，MWA 無法完全 pass through，GM 從 36% 跌至 33%","columns":{"對應假設":"H2","時間尺度":"⚡ 短期（1-2 季可觸發）","監測指標":"季度 GM YoY 連 2 季 -1pp+；管理層 guide 提到 tariff pass-through 困難","警戒閾值":"連 2 季 GM &lt; 34% 或 adj EBITDA margin &lt; 23%"}},{"id":"R2","text":"IIJA 9/30/26 reauthorization 失敗或大幅縮水 — Trump 2.0 政府優先 defense / oil & gas，FY27-28 sales 從 +5% 降至 -2%","columns":{"對應假設":"H1","時間尺度":"🔥 中期（4-6 季）","監測指標":"9/30/2026 reauthorization 公告；FY27 sales YoY 連 2 季 &lt; 1%","警戒閾值":"reauthorization &lt; 50% 原規模 或 sales 連 2 季 &lt; 0%"}},{"id":"R3","text":"競爭格局蠶食 — McWane / American Cast Iron 在 fire hydrant 取得單一大都市 design win，MWA 市佔從 45% 跌至 40%","columns":{"對應假設":"H1","時間尺度":"🐢 長期（2+ 年慢變數）","監測指標":"單一大都市 spec 變化公告；MWA 季報市佔提到「losses」","警戒閾值":"主要市佔指標 -3pp 或 management 法說承認「losing market share」"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"A","val":"🟡","ma":"🟢","trap":"🟢","moat_trend":null,"runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":25.31,"archetype":null,"cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"MWA","date":"2026-11-08","schema":"v15.0","contract":"v19","company_name":"Mueller Water Products"},"oneliner":"美國水管閥門與消防栓的置換需求很穩，三年利潤率多了 940 基點，但銷量在降，明年價格成本對利潤率只剩持平；現價約 15 倍 FY27 獲利，算合理，關鍵是第二季那次尚未公告的漲價留不留得住。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MWA_20261108/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MWA_20261108/scenario.json","answers":{"q1_business":{"verdict":"賺市政自來水系統更換老舊閥門與消防栓的錢，貨經由兩大經銷商出去，利潤留在北美寡占的規格與品牌這一節；現階段營收成長全靠漲價，銷量在降。","reasoning":"FY26 營收約 14.75 億美元，Water Flow Solutions 8.175 億（55%，年減 0.9%），Water Management Solutions 6.575 億（45%，年增 8.7%，含消防栓積壓訂單出清）。2026-11-05 法說明講全年是價格抵銷銷量下滑。Q4 營收 3.765 億年減 1.1%，毛利率 37.0%，調整後營益率 21.9%，GAAP 營益率 19.4%。終端約 60–65% 市政維修汰換、25–30% 新建住宅、約 10% 天然氣公用事業（2026-06-30 10-Q）。單點依賴是通路：兩大經銷商占毛銷售 37%，最大一家 20%，無長期合約（FY2025 10-K）。產業態勢屬雙向拉鋸：關稅與市政預算壓力，對上國內產能需求與 2027-11-01 起過渡的鉛管規則。可能看錯的地方：若銷量下滑其實是份額流失，置換需求穩定就保護不了利潤，份額資料事實表未涵蓋。","fact_refs":["f_kpi0_net_sales_gaap","f_kpi1_adjusted_operating_margi","f_kpi2_gaap_operating_margin","f_kpi5_fy2027_guidance_metering"],"verdict_values":{"revenue_quality":"中等偏好：六成以上來自維修汰換，可延後但不會消失；FY26 成長全來自價格，FY27 指引還含一次尚未公告的漲價，價格部分的能見度低於過去。","unit_econ_note":"價格每 1 個百分點約 1,455 萬美元，假設幾乎全落到 EBITDA，約等於 FY27 每股盈餘的 4.4%（1,455 萬×75%÷約 1.57 億股÷1.59）。","archetype":{"primary":"受監管公用/穩定內需","secondary":"轉機/特殊情境","confidence":"中","fingerprint":"需求來自市政維修汰換，客戶受預算與水費約束；近四年盈餘成長主要來自利潤率修復，而不是量的成長。"},"industry":{"clock_phase":"IV","sd_verdict_source":"需求屬結構性持久，老舊管網維修汰換占六成以上（2026-06-30 10-Q）；短期量縮屬週期性，FY26 新建住宅雙位數下滑、FY27 再跌低個位數，市政採購轉謹慎（2026-11-05 法說）。產業位置依銷量判為收縮段，不看股價。","bargaining":{"up":"上游是鋼、鋁、銅與進口零組件，Section 232 關稅 50% 主要壓在 Krausz 修理產品與 Specialty Valve 線；供應商集中度事實表未涵蓋。","down":"兩大經銷商占毛銷售 37%，最大一家 20%，非獨家且無長期合約；目前錢仍留在製造端，FY26 調整後 EBITDA margin 25.2%。","geo":"以色列 Ariel 廠與中國荊門廠是關稅與地緣的單點，國內鑄造投資是對策。"},"profit_pool_dir":"事實表未涵蓋","tam_table":{"expanded":false,"reason":"事實表沒有 TAM、滲透率與利潤池資料；核心產品是置換需求，滲透率不是主要成長變數。"}}}},"q2_moat":{"verdict":"護城河持平：定價與規格黏性還在，營運改善擴大了利潤，但這不等於護城河變寬。","reasoning":"機制是市政工程規格與用戶習慣，加上寡占結構：FY2025 10-K 稱閥門市場成熟、終端用戶不易換品牌，鐵閘閥與消防栓主要對手只有 McWane 和 American Cast Iron Pipe。同業 ROIC 事實表未涵蓋，改看利潤率。TTM 營益率 21.54%，高於 WTS 19.73%、BMI 18.76%、XYL 16.06%，低於 ZWS 22.52%；毛利率 38.24% 卻是五家最低，代表優勢主要在費用率與工廠效率，不是產品溢價。同業產品組合不同，這個比較只能看方向。可能看錯的地方：若 FY27 新漲價未獲對手跟進，定價面要改判縮減，整體方向轉為向下。","fact_refs":["f_peer_mwa_gross_margin_pct","f_peer_mwa_operating_margin_pct","f_peer_wts_gross_margin_pct","f_peer_wts_operating_margin_pct","f_peer_xyl_gross_margin_pct","f_peer_xyl_operating_margin_pct","f_peer_zws_gross_margin_pct","f_peer_zws_operating_margin_pct","f_peer_bmi_gross_margin_pct","f_peer_bmi_operating_margin_pct"],"verdict_values":{"moat":{"mechanism":"市政規格與用戶品牌習慣，加上鐵閘閥與消防栓的少數競爭者結構，經由區域與全國水務經銷商觸達。","execution":8,"pricing":7,"grade":"B","trend":"→","trend_evidence":"執行面擴大：調整後 EBITDA margin 三年多 940 基點。定價面穩定：FY26 漲價仍帶動營收，但 2026-11-05 Morgan 說 FY27 價格成本金額為正、利潤率持平，比 2026-08-06 Rasmussen 說的價格成本為正保守。份額資料事實表未涵蓋；銷量下滑可由新建住宅與消防栓基期解釋，目前沒有證據指向份額流失，也沒有證據能排除。","competitor_notes":[{"name":"McWane","strategy_note":"10-K 點名的主要對手，份額與定價事實表未涵蓋；FY27 漲價留不留得住，要看它跟不跟。"},{"name":"American Cast Iron Pipe","strategy_note":"同屬少數主要對手，資料同樣未涵蓋，是定價紀律的另一半。"},{"name":"WTS","strategy_note":"毛利率高出約 10 個百分點，產品偏建築與工業，是 specialty valves 轉向工業時可參考的組合。"},{"name":"XYL","strategy_note":"營益率較低、有研發揭露，走的是技術與數據路線，正是公司退出計量後不再競爭的方向。"},{"name":"ZWS","strategy_note":"毛利率與 FCF 利潤率都更高，代表水處理產品組合能到的上限，公司靠工廠效率追近營益率但毛利差距仍大。"},{"name":"BMI","strategy_note":"計量專業廠，毛利率高於公司，對照公司計量業務銷售萎縮且 EBITDA 為負，說明這塊規模不足。"}],"peer_na_reason":"同業 ROIC 與投入資本事實表未涵蓋，改以營益率與毛利率比較方向。","threats":[{"level":"🟡","text":"進口與北美以外對手：競爭強度隨匯率、運費與貿易救濟波動，目前關稅反而提供保護，關稅退場或運費下降時保護會消失。","p":"20%","evidence_refs":["competitive_share_entrants#1","substitute_technology#2"]},{"level":"🟡","text":"新漲價若未獲兩家主要對手跟進，定價紀律會鬆動；對手定價資料事實表未涵蓋。","p":"25%","evidence_refs":[]},{"level":"🟡","text":"退出計量後公司不再掌握用水數據端，只留漏水偵測；若水務客戶改以計量平台整合採購，硬體綁定會鬆動。事實表沒有這種轉向的證據，只列觀察。","p":"10%","evidence_refs":["major_events#0"]}],"roic_durability":{"quadrant":"高利益率，周轉率未知（投入資本事實表未涵蓋）","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者是水務單位與承包商，決策者是市政工程人員，付款者是市政預算與水費。維修汰換是需要不是想要，可以延後但不會消失；六成以上營收屬此類（2026-06-30 10-Q）。"},{"item":"決策層級","level":"🟡","text":"替代性要看市政規格這一層，10-K 稱終端用戶不易換品牌，但這是公司自述。漲價後流失率、規格變更次數事實表未涵蓋，而銷量正在下滑，因此不給綠燈。"},{"item":"價值鏈分配","level":"🟡","text":"下游兩大經銷商占 37% 且無長期合約，上游承受關稅；目前製造端拿到的份額處於高點，FY27 價格成本對利潤率已轉持平，再多拿的空間變小。"},{"item":"社會容忍度","level":"🟡","text":"客戶是受預算與水費約束的市政單位，公司連年靠漲價成長，2026-11-05 法說已提到市政因通膨壓力採購謹慎；公司本身不受費率監管，但實際定價上限受市政預算限制。"}],"roiic":"無法計算：投入資本與營運資金變動事實表未涵蓋。FY23 到 FY26 稅前營業利益增加約 1.53 億，主要來自利潤率修復，不是新投入資本的報酬，不能當增量報酬。","reinvest_rate":"約 6%（不含營運資金與收購）","endo_ceiling":null,"formula_note":"再投資率＝（FY27 資本支出中位 65－折舊攤銷中位 50）÷稅後營業利益（（EBITDA 中位 383－50）×75%≈250）＝15÷250＝6%，單位百萬美元。"}}}},"q3_growth":{"verdict":"成長後勁中等：核心是成熟的置換市場，第二曲線 specialty valves 在長但規模未揭露，五年成長主要靠價格、利潤率與回購。","reasoning":"FY26 營收年增 3.2% 全由價格帶動；FY27 指引排除計量後持平到 +2.5%，價格低至中個位數，排除約 2 個百分點的消防栓基期後銷量持平。共識只有兩年：Koyfin FY1 1.57、FY2 1.59，第三年事實表未涵蓋，三年共識複合成長無法算出。FY26 的 1.57 含 0.09 一次性，扣除後 1.48，到 FY27 的 1.59 是 +7.4%，未扣除只有 +1.3%。再投資率約 6%，要單靠再投資達到 7.4% 需要增量報酬超過 120%，不合理，所以缺口歸因利潤率擴張與回購，不是內生成長。Base 五年 EPS 年複合約 7.0%，約一半來自營收（含價格），其餘來自利潤率與股數減少。可能看錯的地方：specialty valves 若占比已高且持續雙位數，後勁會比這裡判的好，占比事實表未涵蓋。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_kpi5_fy2027_guidance_metering","f_consensus_rev_3m_fy1_pct"],"verdict_values":{"growth":{"driver_mix":"FY26 為價格正、量負；FY27 指引價格低至中個位數，量在排除消防栓基期後持平；EPS 成長主要靠利潤率、計量退出與回購。","runway_years":"不適用：置換型需求沒有滲透率概念，滲透率資料事實表未涵蓋","runway_post_y5":"🟡","endo_ceiling_basis":"內生上界無法算出，投入資本事實表未涵蓋。再投資率約 6%，共識由乾淨基期 1.48 到 1.59 的 +7.4% 明顯高於這個再投資率能支撐的水準，按超出處理，缺口歸因利潤率擴張與回購。","segments":[{"item":"Water Flow Solutions","value":"FY26 銷售 8.175 億（年減 0.9%），調整後 EBITDA margin 33.0%；FY27 指引低至中個位數成長，margin 小幅上升（排除關稅退款）。"},{"item":"Water Management Solutions","value":"FY26 銷售 6.575 億（年增 8.7%），margin 24.6%；FY27 指引高個位數下滑（計量退出與消防栓基期），margin 明顯擴張。"}],"decay_signals":["亮：主力產品提價後銷量下滑——FY26 與 Q4 都是價格抵銷銷量，鐵閘閥與 service brass 銷量下滑，部分來自新建住宅。","亮：EPS 成長遠高於營收成長——FY23 到 FY25 稀釋 EPS 年複合約 49%，營收約 5.9%（事實表 financial_history）。","未亮：毛利率連 2 季年減——Q3 排除一次性 +30 基點，Q4 −100 基點，目前只有一季，FY27 第一季決定是否亮起。","未亮：FCF／淨利連 2 年低於 0.75——FY25 約 0.90，FY26 為調整後淨利 84%。","未亮：SBC 占營收超過 5%——FY26 約 0.93%。","未亮：維護性資本支出占 FCF 超過 60%——維護性金額未揭露，總資本支出僅占 FCF 約 27%。","未亮：停止投資新產能——FY27 資本支出升到 6,000–7,000 萬，投入鑄造廠。","資料缺口：核心市占近 12 個月變化，事實表未涵蓋。","資料缺口：TAM 是否萎縮，事實表未涵蓋；目前沒有替代技術證據。","資料缺口：產業倍數近 3 年是否系統性下移，事實表未涵蓋。"],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"資本配置中等：資產負債表很強、稀釋很低，但現金累積快於配發，併購紀錄是要打折的部分。","reasoning":"FY26 自由現金流 2.073 億，為調整後淨利 84%；配發 7,400 萬，約占 36%；SBC 1,370 萬，占營收 0.93%。現金 5.66 億、債務 4.54 億，最近到期 2029 年 6 月，票息 4%。新增回購授權 3 億、季配息調升 14.3% 到 0.08。現金去向：資本支出 5,560 萬，配發 7,400 萬，併購金額事實表未涵蓋，其餘留在帳上。FCF 超預期主因是營運資金有利與資本支出低於 2026-08-06 重申的 6,000–6,500 萬，不能全算經營成果。可能看錯的地方：管理層若把 3 億授權用足，回購會比這裡假設的更有貢獻。","fact_refs":["f_kpi3_free_cash_flow_q4","f_kpi4_sbc_gaap_fy2026","f_net_debt_m","f_shares_diluted_m"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":true,"passed":false,"input":"完整併購帳事實表未涵蓋；可驗證的部分為負：計量銷售近 4–5 年年減約 10%、EBITDA 為負，退出還要付約 2,600 萬，i2O 北美以外業務也已出售。"},{"name":"buyback_yield","applicable":true,"passed":null,"input":"回購均價與十年期公債殖利率事實表未涵蓋，無法判定；以現價計 FY27 盈餘殖利率約 6.6%（1.59÷24.05）。"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"FY26 SBC 1,370 萬÷市值約 37.4 億＝0.37%，低於 1.5%；以金額換算，不是實際股數變動。"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購支撐；三年現金去向與回購均價事實表未涵蓋，無法展開成完整表格。"}}}},"q5_valuation":{"verdict":"現價 24.05 約 15.1 倍 FY27 獲利，大致等於基準情境；要賺 10% 年化得把 margin 推到近 30%，目前不信。","reasoning":"要賺 10% 年化，扣掉約 1.3% 股息，股價年增需約 8.7%，FY31 目標約 36.5 美元；以 16 倍計需要 EPS 約 2.28，比 Base 的 2.08 高約 10%，換算 EBITDA margin 近 30%。2026-11-05 Bryan Blair 問中期利潤率是否 3 開頭，McAndrew 沒有回答。賣方目標價多在 28–31 美元、個別 25–34，多為 2026 年中以前，不能當支持。FY27 EV/EBITDA 約 9.5 倍（36.3 億÷3.83 億），FCF 殖利率約 5.5%。可能看錯的地方：淨現金加上 FCF 若全數回購，EPS 可高於 Base，倍數也可能回升。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_consensus_eps_fy1","f_consensus_eps_fy2","f_pe_current","f_pe_percentile","f_ps_percentile","f_ev_s_percentile","f_ev_m","f_dividend_yield_ttm","f_rsi14","f_week26_return_pct","f_ma_state"],"verdict_values":{"valuation":{"basis":"以 FY27 共識 EPS 1.59 為前瞻分母，現價對應 15.13 倍；起點改用扣除 0.09 一次性後的 FY26 實績 1.48，對應 16.25 倍。","peers":{"expanded":false,"reason":"事實表只有同業利潤率，沒有同業本益比，無法做倍數對照。"},"peg":2.04,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"FY27 本益比 15.13 倍，PEG 約 2.0（15.13÷7.43），FY27 EV/EBITDA 約 9.5 倍，FCF 殖利率約 5.5%，基準年化約 8%，屬合理區間。五年分位事實表未涵蓋，只有四個年度端點：本益比分位 0、P/S 分位 81，兩者方向相反，不能只用本益比主張便宜。四週漲幅事實表未涵蓋。","upside_short_pct":5.8,"upside_mid_pct":21.7,"denominator_disputed":true,"denominator_note":"FY1 共識 1.57 與 FY26 實際相同，且 90 天零修正，快照應未滾動，1.57 實為剛結束的 FY26。它含 0.09 一次性，扣除後 1.48。前瞻分母改用 FY27 的 1.59；但 1.59 建立在歷史最高的利潤率上，便宜的說法不成立。"}}},"q6_how_wrong":{"verdict":"最可能看錯在把歷史最高的利潤率當常態，陷阱風險中等。","reasoning":"容易看錯的有三處：把高點利潤率當常態、把一次性好處當經營成果、把第二曲線當已證實。衰退信號十項亮兩項，主力產品提價後銷量下滑、EPS 成長遠高於營收成長，另有三項是資料缺口。若 FY27 價格達標且銷量止跌，第一項會熄掉，結論可上調。空方最強數字與歷史最大回撤事實表未涵蓋。訴訟方面，Cobb County 1,500 萬和解預期由第三方補償，資安集體訴訟上限 28.5 萬，都不構成主要風險。","fact_refs":["f_kpi1_adjusted_operating_margi","f_pe_percentile","f_ps_percentile"],"verdict_values":{"trap":{"verdict":"🟡","label":"利潤率高點、量縮靠價"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":1.48,"pe":16.25,"basis":"FY26 調整後 EPS 1.57 扣除關稅退款與 i2O 稅務利益合計 0.09 後的 1.48，屬過去四季實績口徑，與終端年實績本益比同口徑。"},"eps":{"bull":[1.64,1.87,2.1,2.37,2.63],"base":[1.59,1.69,1.83,1.96,2.08],"bear":[1.5,1.39,1.33,1.37,1.41]},"pe":{"bull":19,"base":16,"bear":12},"p":{"bull":20,"base":50,"bear":30},"yield_pct":{"dividend":1.33,"net_buyback":0},"second_stage":{"bull_cagr_pct":8,"base_cagr_pct":5},"max_dd":{"lo":-42,"hi":-28,"basis":"Bear 谷底 EPS 1.33（FY29）乘 10.5 到 13 倍，得 13.97 到 17.29 美元，距現價 −42% 到 −28%。歷史最大回撤事實表未涵蓋；250 週均線 18.53 約低於現價 23%，是第一個技術支撐。","trigger_time":null},"basis":{"bull":"營收 FY31 約 18.2 億（年增約 5%），EBITDA margin 升到 30.5%，specialty valves 與工業放量，股數年減約 2.3%；終端 19 倍。同業本益比事實表未涵蓋。","base":"FY27 取共識 1.59（指引隱含約 1.57–1.58）；營收 FY31 約 16.9 億（年增約 4%），margin 升到 27.5%，股數年減約 1.4%；回購效果已含在 EPS，淨回購殖利率填 0 避免重算；終端 16 倍，略低於現行 16.25 倍。同業本益比事實表未涵蓋。","bear":"漲價留不住、市政預算緊縮，margin 回到 FY25 約 23% 的水準，FY29 EPS 谷底 1.33，FY31 為 1.41；終端 12 倍。機率 30%，依據是銷量已下滑、FY27 價格成本對利潤率持平、共識成長高於再投資能支撐的水準。"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"2026-11-05 法說：Q4 排除一次性項目後毛利率年減 100 基點；SG&A 年減 940 萬美元，主因之一是激勵獎金下降，金額大於調整後 EBITDA 約 370 萬的增幅；FY27 價格成本對利潤率持平，指引卻要擴張 110 基點。","assumption":"FY27 的 26.3% 是可維持的新基準。","consequence":"價格留不住時 margin 回到 FY25 的約 23%，Bear EPS 1.33 到 1.41，乘 11 到 12 倍股價約 15 到 17 美元，虧 30–39%。五年虧 50% 的路徑是 margin 20%、EPS 約 1.18、10 倍本益比，股價約 11.8 美元。","ruling":"採納為 Bear，機率 30%。它和唯一致命點同源，五年虧 50% 的故事就是漲價失敗後利潤率回吐，兩者對帳一致。不納入 Base，因為製造改善與計量退出（約 800 萬 EBITDA）不靠價格。","watch":"FY27 Q1 與 Q2 調整後毛利率年變化、價格實現與 SG&A 金額。","evidence_refs":["reg_tariff_export#5","end_markets#0"],"fact_refs":["f_kpi1_adjusted_operating_margi"]},{"view":"論點失敗","evidence":"2026-08-06 法說的財務長是 Melissa Rasmussen，2026-11-05 改由 10-28 到職的 Mike Morgan 發言，約 11-19 接任，離任原因事實表未涵蓋。同一場首度把尚未公告的漲價放進指引，RBC 當場指出與過去做法不同。","assumption":"指引編製紀律與調整項定義不變。","consequence":"新任財務長可能重設調整項或基期，FY27 指引的可信度低於過去三次上調時的水準。","ruling":"部分採納：不改 Base，但把財務長交接列入風險，FY27 Q1 是第一個檢查點。","watch":"FY26 10-K 的調整項定義、FY27 Q1 指引是否維持、中期目標發布時間。","evidence_refs":[]},{"view":"論點成功但股東經濟變差","evidence":"FY26 底現金 5.66 億、流動性 7.31 億，法說提到尋求現有與相鄰市場併購；同一時間公司正在退出 i2O 與計量，計量銷售 4–5 年年減約 10%、EBITDA 為負，退出要付約 2,600 萬，且保留既有硬體合約與保固義務。RBC 問有沒有對價與後續負債，CEO 沒有正面回答。","assumption":"margin 與現金流達標後，現金會用在報酬高於資金成本的地方。","consequence":"一筆 5 億美元、稅後報酬 4% 的併購，相比同額回購（盈餘殖利率約 6.6%）每年少約 1,300 萬獲利，約每股 0.09，是 Base FY31 EPS 的 4%。","ruling":"部分採納：不改 Base，併購列為行動條件；單筆超過 3 億美元且未揭露報酬目標時停止加碼。","watch":"併購金額與揭露的投資報酬，回購實際金額對 3 億授權的比例。","evidence_refs":["major_events#0","ma_merger#0"]},{"view":"價格已反映太多","evidence":"本益比 17.06 是四個年度端點的最低，但 P/S 2.54 在 81 百分位，EV/S 2.46 在 71 百分位。股價已為更高的利潤率付錢，只是獲利長得更快。基準情境年化約 8%。","assumption":"本益比在低檔代表便宜。","consequence":"以銷售倍數衡量，現價已反映大部分利潤率修復，要有超額報酬必須 margin 繼續上升；10% 年化需要 FY31 EPS 約 2.28，對應 margin 近 30%。","ruling":"採納：不主張便宜，估值結論為合理。","watch":"新任財務長預告的中期利潤率目標，及 FY27 全年 margin 是否達 26.3%。","evidence_refs":[],"fact_refs":["f_pe_percentile","f_ps_percentile","f_ev_s_percentile"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 🟢 → 本次 🟠","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=🟢","side_b":"本次 ma=🟠","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 25.31 → 本次 24.05（-5.0%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=25.31","side_b":"本次 price_at_dd=24.05","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 25.31 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 25.31 美元：五年期望值 前份未列，基準年化 前份未列，前份未列不對稱比","side_b":"本次情境、股價仍用 25.31 美元：Bull 價 49.97、Bear 價 16.92，五年期望值 +25.3%，基準年化 5.6%，不對稱比 1.96","ruling":"先換情境、股價不動：五年期望值與基準年化前份未列，無法比較。前份未列不對稱比，本次為 1.96。Bull、Bear 價位與股價無關，只受情境影響。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 25.31 美元：五年期望值 +25.3%，基準年化 5.6%，不對稱比 1.96","side_b":"本次情境、股價 24.05 美元：五年期望值 +31.9%，基準年化 6.7%，不對稱比 2.42","ruling":"再換股價、情境不動：起點價下跌 5.0%，五年期望值多 6.6 個百分點，基準年化多 1.1 個百分點，不對稱比由 1.96 升到 2.42。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"訊號與陷阱判斷下修","cause":"新證據","prior_field":["signal","trap"],"side_a":"前份給偏正面訊號、陷阱風險低，依據包括 FY27 營收 ≥15.5 億、EBITDA ≥3.9 億。","side_b":"FY27 指引營收 14.4–14.7 億（不含約 4,000 萬計量），EBITDA 3.78–3.88 億，兩者都低於前份門檻；銷量下滑，價格成本對利潤率轉持平。","ruling":"採新證據：訊號降一級，陷阱風險由低升到中。方向相反，以公司正式指引為準。","evidence_level":"一手：2026-11-04 新聞稿與 2026-11-05 法說","settle_metric":"FY27 排除計量營收與調整後 EBITDA","if_then":["若 FY27 第二季價格實現達低個位數以上且銷量持平，訊號回升一級","若連 2 季調整後毛利率年減 ≥100 基點，減碼一半"],"evidence_refs":["end_markets#0"]},{"axis":"估值結論","cause":"價格變動","prior_field":["val"],"side_a":"前份股價 25.31，結論為合理。","side_b":"現價 24.05，較前份低約 5%，結論仍為合理。","ruling":"價格變動幅度不足以改變結論；FY27 獲利預期也未上升。","evidence_level":"事實表價格與共識","settle_metric":"FY27 本益比","if_then":["若 FY27 第二季驗證達標，且股價仍在 15 倍附近，可建小量首倉","若股價先漲過 28 美元而價格證據未到，不追"]},{"axis":"前份未填欄位補上","cause":"方法變動","prior_field":["moat_trend","runway_post_y5","p_bull_pct","p_bear_pct","max_dd_pct","archetype","cycle_position"],"side_a":"前份這些欄位皆未填。","side_b":"本次補上：護城河持平、成長後勁中等、情境機率 20／50／30、最大回撤 −28% 到 −42%、公司類型為穩定內需；非循環股不填景氣位置，裁決與角色由程式產生。","ruling":"屬格式改版後的新增判斷，不代表基本面變化。","evidence_level":"方法說明"},{"axis":"Single Thing 設定","cause":"方法變動","prior_field":null,"side_a":"前份未設唯一致命點（null）。","side_b":"FY27 第二季那次尚未公告的年度漲價，公告與留存是否達到全年低個位數以上的價格實現。","ruling":"Single Thing 依數學上最大的單一敏感度選定，價格每 1 個百分點約影響 FY27 EPS 4.4%，大於失去單一經銷商的直接可估影響。","evidence_level":"2026-11-05 法說與本次試算","settle_metric":"FY27 全年價格實現"},{"axis":"清倉與減碼門檻、重新進場條件","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"前份 kill_metrics 與重新進場條件皆未設（null）。","side_b":"減碼：連 2 季調整後毛利率年減 ≥100 基點，或 TTM 調整後 EBITDA margin 低於 24%。清倉：TTM margin 低於 23% 且價格實現低於低個位數。重新進場：第二季確認價格實現達低個位數以上且排除基期後銷量不低於持平。","ruling":"舊版沒有這些欄位，本次新設，門檻綁定價格與利潤率這個最大敏感度。","evidence_level":"方法說明與本次試算","settle_metric":"季度毛利率、EBITDA margin、價格實現"},{"axis":"舊風險門檻調整（減碼條件）","cause":"新證據","prior_field":null,"side_a":"連 2 季 GM < 34% 或 adj EBITDA margin < 23%；reauthorization < 50% 原規模 或 sales 連 2 季 < 0%；主要市佔指標 -3pp 或 management 法說承認 losing market share。","side_b":"連 2 季調整後毛利率年減 ≥100 基點或 TTM margin 低於 24% 時減碼；排除計量後營收連 2 季年減；主要份額指標 −3 個百分點或管理層承認份額流失（份額為資料缺口）。","ruling":"Q4 毛利率 37.0%、margin 25.4%，舊門檻太鬆。聯邦法案結果事實表未涵蓋，2026-08-06 McAndrew 稱聯邦占市政投資不到 5%、未來 1–3 年無重大變化，不再作為減碼條件，仍保留監測。銷售門檻改排除計量口徑，避免機械誤觸。","evidence_level":"一手：法說與新聞稿；聯邦法案為資料缺口","settle_metric":"季度調整後毛利率、排除計量營收","if_then":["若連 2 季調整後毛利率年減 ≥100 基點，減碼一半","若聯邦資金變動使 FY27 指引下修，停止加碼"],"evidence_refs":["reg_tariff_export#1"]},{"axis":"舊論點門檻失效","cause":"新證據","prior_field":null,"side_a":"FY27 sales ≥ $1.55B；FY27 adj EBITDA ≥ $390M；EchoShore subscription 年化 > $100M；FY27 末 trailing PE ≥ 20x。","side_b":"FY27 排除計量營收 ≥14.4 億、EBITDA margin ≥26.0%；specialty valves 持續雙位數成長；倍數不再列為假設。","ruling":"FY27 指引中位加回約 4,000 萬計量後約 14.95 億，仍低於 15.5 億；EBITDA 指引上緣 3.88 億也低於 3.9 億。公司退出計量，智慧水務占比擴大的說法失去依據，門檻全部重設。","evidence_level":"一手：2026-11-04 新聞稿","settle_metric":"FY27 全年營收與 margin"},{"axis":"市政需求說法不一致","cause":null,"side_a":"2026-11-04 新聞稿：Municipal repair and replacement demand remains resilient；2026-08-06 Rasmussen 同樣說具韌性。","side_b":"2026-11-05 McAndrew 在 FY27 展望中提到市政單位 cautious purchasing behavior，且因通膨壓力預算謹慎。","ruling":"可調和，屬程度差異：需求還在，採購時點往後，Base 採排除基期後銷量持平，不採復甦。","evidence_level":"一手：新聞稿與法說","settle_metric":"排除消防栓基期後銷量","if_then":["若連 2 季銷量年減，減碼一半","若連 2 季銷量年增，維持持有並解除停止加碼"]},{"axis":"利潤率結構性或階段性","cause":null,"side_a":"McAndrew：三年 940 基點，FY27 中位達四年 1,150 基點；Morgan：營運系統才剛上軌道，還有空間。","side_b":"Q4 排除一次性毛利率年減 100 基點，SG&A 下降含獎金減少；FY26 含關稅退款；2026-08-06 Rasmussen 說價格成本為正，2026-11-05 Morgan 改口金額為正、利潤率持平。","ruling":"部分結構、部分階段性。Base 取 26–27.5%，不給 30%；管理層把獎金與關稅退款歸入成果的部分未證實，以 FY27 兩季數據檢驗。","evidence_level":"一手法說，獎金金額未揭露","settle_metric":"FY27 Q1、Q2 調整後毛利率與 SG&A 金額","if_then":["若股價先漲過 28 美元（約 17.6 倍 FY27 獲利）而價格證據未到，不追","若股價下跌而第二季價格實現達標，分批反買","若 FY27 全年 margin 達 26.3% 且毛利率年增，Base 上調到 28%"]},{"axis":"第二曲線規模不透明","cause":null,"side_a":"McAndrew：specialty valves 雙位數成長、占積壓訂單多數，資料中心為成長最快之一。","side_b":"2026-08-06 問資料中心規模只答 relatively small，問消防栓更新系統的營收貢獻未答；2026-11-05 問中期利潤率也未答。","ruling":"第二曲線最多支撐後勁中等，不支撐倍數提升；不可裁決至公司揭露占比。","evidence_level":"法說定性描述，無金額","settle_metric":"specialty valves 營收占比","if_then":["若揭露占比且連續兩年雙位數，成長後勁上調一級","若連續四季未揭露占比，維持中等且不給倍數溢價"]},{"axis":"現在就買的最強論證","cause":null,"side_a":"淨現金約 1.12 億、FY27 EV/EBITDA 約 9.5 倍、FCF 殖利率約 5.5%，指引已含量縮，賣方目標價多在 28–31 美元。","side_b":"目標價多為 2026 年中以前；扣除一次性後 FY27 EPS 成長僅 7%，且全靠利潤率；關鍵漲價半年後才揭曉，新財務長尚未給中期框架。","ruling":"等到第二季的代價是可能少賺一段，可以接受，因為基準年化只有約 8%。結論卡在價格實現這個事件，不是股價。","evidence_level":"事實表與法說","settle_metric":"FY27 第二季價格實現","if_then":["若第二季達標，建小量首倉","若第二季未達標，不建倉"]},{"axis":"自由現金流資料不一致","cause":null,"side_a":"事實表同業對照的 TTM FCF 利潤率 10.07%。","side_b":"公司 FY26 FCF 2.073 億÷營收 14.75 億＝14.05%，前九個月 1.106 億加 Q4 0.967 億相符。","ruling":"採公司揭露數字，資料商的 TTM 應有期別或定義問題，同業比較中此欄不採用。","evidence_level":"一手：法說與新聞稿","settle_metric":"FY26 10-K 現金流量表"}],"triggers":[{"n":1,"text":"第二季漲價落地驗證","type":"Single Thing","maps_to":"Single Thing","metric":"FY27 全年價格實現（指引低至中個位數）","threshold":"第二季財報時全年價格實現低於低個位數，或公司撤回新漲價","action":"減碼一半，下一季仍未回升則清倉","source_freq":"季度新聞稿與法說","date":"2027-05"},{"n":2,"text":"毛利率連續下滑","type":"風險","maps_to":"R1","metric":"調整後毛利率年變化","threshold":"連 2 季年減 ≥100 基點，Q4 已出現一季","action":"減碼一半","source_freq":"季度新聞稿與法說","date":"2027-02","evidence_refs":["reg_tariff_export#0","reg_tariff_export#2","reg_tariff_export#5","geo_supply_chain#0"]},{"n":3,"text":"銷量是否止跌","type":"假設驗證","maps_to":"H1","metric":"排除計量營收、排除消防栓基期後銷量","threshold":"FY27 排除計量營收 ≥14.4 億且銷量不低於持平","action":"未達標則停止加碼","source_freq":"季度新聞稿與法說","date":"2027-11","evidence_refs":["end_markets#0"]},{"n":4,"text":"全年利潤率達標","type":"假設驗證","maps_to":"H2","metric":"調整後 EBITDA margin","threshold":"FY27 ≥26.0%","action":"未達標則停止加碼","source_freq":"季度新聞稿與法說","date":"2027-11"},{"n":5,"text":"經銷商集中度上升","type":"風險","maps_to":"R3","metric":"兩大經銷商占毛銷售","threshold":"合計 ≥42% 或最大一家 ≥25%","action":"停止加碼","source_freq":"10-K，每年一次","date":"2026-11","evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#1"]},{"n":6,"text":"進場條件成立","type":"估值rearm","maps_to":"H1","metric":"全年價格實現與排除基期後銷量","threshold":"第二季財報確認價格實現達低個位數以上，且銷量不低於持平","action":"建小量首倉，低於目標倉位三分之一","source_freq":"季度新聞稿與法說","date":"2027-05"},{"n":7,"text":"利潤率跌破減碼線","type":"減碼","maps_to":"R1","metric":"TTM 調整後 EBITDA margin","threshold":"低於 24%","action":"減碼一半","source_freq":"季度新聞稿","date":"2027-05"},{"n":8,"text":"利潤率回吐且定價失效","type":"清倉","maps_to":"H2","metric":"TTM 調整後 EBITDA margin 與價格實現","threshold":"TTM margin 低於 23% 且價格實現低於低個位數","action":"清倉","source_freq":"季度新聞稿與法說","date":"2027-11"},{"n":9,"text":"第二曲線與中期目標揭露","type":"加碼","maps_to":"H3","metric":"specialty valves 營收占比與中期 margin 目標","threshold":"揭露占比、中期目標 ≥28%，且 FY27 全年 margin ≥26.3%","action":"加碼至目標倉位","source_freq":"法說或投資人日","date":"2027-11"},{"n":10,"text":"計量退出費用超支","type":"風險","maps_to":"R5","metric":"計量退出總費用與時程","threshold":"總費用超過 3,100 萬美元，或轉移拖到 FY28 下半","action":"停止加碼","source_freq":"季度新聞稿與法說","date":"2027-11","evidence_refs":["major_events#0","ma_merger#0"]},{"n":11,"text":"份額與進口競爭","type":"風險","maps_to":"R4","metric":"主要份額指標與管理層說法","threshold":"份額下滑 3 個百分點或管理層承認流失（份額為資料缺口）","action":"減碼一半","source_freq":"法說、10-K","date":"2027-11","evidence_refs":["competitive_share_entrants#1","substitute_technology#2"]},{"n":12,"text":"全面複審","type":"複審日期","maps_to":"H1","metric":"第二季財報後重跑研究","threshold":"2027-05 財報發布後兩週內","action":"重跑本研究並更新情境","source_freq":"一次","date":"2027-05-15"}],"kill_metrics":[{"metric":"FY27 全年價格實現","bear_threshold":"低於低個位數，或撤回新漲價","window":"FY27 Q2 至 Q4","source":"季度新聞稿與法說","last_status":"unknown"},{"metric":"調整後毛利率年變化","bear_threshold":"連 2 季年減 ≥100 基點","window":"連續 2 季","source":"季度新聞稿與法說","last_status":"warning"},{"metric":"TTM 調整後 EBITDA margin","bear_threshold":"減碼低於 24%；清倉低於 23%","window":"每季","source":"季度新聞稿","last_status":"ok"},{"metric":"排除計量與消防栓基期後銷量","bear_threshold":"連 2 季年減","window":"連續 2 季","source":"季度新聞稿與法說","last_status":"unknown"},{"metric":"兩大經銷商占毛銷售","bear_threshold":"合計 ≥42% 或最大一家 ≥25%","window":"每年","source":"10-K","last_status":"ok"},{"metric":"計量退出總費用","bear_threshold":"超過 3,100 萬美元或拖到 FY28 下半","window":"FY27 全年","source":"季度新聞稿與法說","last_status":"unknown"}],"evidence_dismissed":[{"ref":"substitute_technology#1","reason":"這條是 10-K 通用風險條款，未指名任何對手、產品或金額，證據本身沒有可驗證的事實，也沒有說明 AI 如何影響鑄鐵閥門與消防栓這類產品。"}],"action_conditions":{"rearm_trigger":"FY27 第二季財報確認全年價格實現達低個位數以上，且排除消防栓基期後銷量不低於持平","exec_line":"現價不追；已持有者續抱不加碼，等 FY27 第二季財報驗證漲價。股價先漲但證據未到不追；股價下跌而價格實現達標則分批反買。"}},"decision_inputs":{"signal":"B","ma":"🟠","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":null,"cycle_gates_pass":null,"wait_for_price":true,"wait_for_price_condition":"等 FY27 第二季財報（約 2027-05）確認年度漲價已落地，全年價格實現達低個位數以上，且排除消防栓基期後銷量不低於持平；這是事件條件，不設進場價。"},"thesis":{"H":[{"id":"H1","text":"價格帶動、銷量止跌：排除計量後營收守住指引，之後銷量回到持平以上。","2y":"FY28 排除計量營收 ≥15.0 億美元（FY27 指引中位 14.55 億再加約 3%）","5y":"FY31 營收 ≥16.9 億美元（年複合約 3.9%）","10y":null,"threshold":"FY27 排除計量營收 ≥14.4 億，且排除消防栓基期後銷量不低於持平","source":"公司季度新聞稿與法說","drift_rule":"2 年期：連 2 季偏離門檻 ≥5% 削弱，連 3 季 ≥10% 反轉；5 年期：連 4 季 ≥5% 削弱，連 6 季 ≥10% 反轉"},{"id":"H2","text":"調整後 EBITDA margin 守住 26% 以上，靠製造效率與業務組合清理，不靠關稅退款。","2y":"FY28 ≥26.5%","5y":"FY31 ≥27.5%","10y":null,"threshold":"FY27 ≥26.0%（指引中位 26.3%）","source":"公司季度新聞稿與法說","drift_rule":"2 年期：連 2 季偏離門檻 ≥5% 削弱，連 3 季 ≥10% 反轉；5 年期：連 4 季 ≥5% 削弱，連 6 季 ≥10% 反轉"},{"id":"H3","text":"specialty valves 成為第二條成長線：雙位數成長延續，公司開始揭露規模。","2y":"到 FY28 連續兩年雙位數成長，仍占積壓訂單多數，並揭露營收占比","5y":"FY31 占營收 ≥20%（目前占比事實表未涵蓋）","10y":null,"threshold":"FY27 雙位數成長，且 FY28 前揭露營收占比","source":"法說、投資人日、10-K","drift_rule":"連續兩年未達雙位數即削弱；連續三年未達或未揭露占比即反轉"}],"R":[{"id":"R1","text":"關稅與成本壓過定價：Section 232 鋼鋁關稅 50% 壓在 Krausz 修理產品與 Specialty Valve 線，不再有關稅退款，FY27 價格成本對利潤率只剩持平；以色列與中國廠也是地緣單點。","h_ref":"H2","clock":"⚡","threshold":"連 2 季調整後毛利率年減 ≥100 基點，或 TTM 調整後 EBITDA margin 低於 24%","evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","reg_tariff_export#2","reg_tariff_export#5","geo_supply_chain#0","geo_supply_chain#2"]},{"id":"R2","text":"銷量下滑比公司假設的久：2026-08-06 McAndrew 說住宅不會一直低迷，市政與商業策略可抵銷；2026-11-05 的 FY27 指引仍假設住宅再跌低個位數、市政謹慎。","h_ref":"H1","clock":"🔥","threshold":"排除計量與消防栓基期後銷量連 2 季年減，或排除計量後營收連 2 季年減","evidence_refs":["end_markets#0"]},{"id":"R3","text":"通路議價：兩大經銷商占毛銷售 37%，最大一家 20%，非獨家且無長期合約，應收帳款也集中。","h_ref":"H2","clock":"🔥","threshold":"兩大合計 ≥42% 或最大一家 ≥25%","evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#1"]},{"id":"R4","text":"份額被對手或進口吃掉：寡占規格黏性是公司自述，份額資料缺失，運費與關稅變動會改變進口競爭力。","h_ref":"H1","clock":"🐢","threshold":"主要份額指標下滑 3 個百分點，或管理層承認流失份額（份額為資料缺口）","evidence_refs":["competitive_share_entrants#1","substitute_technology#2"]},{"id":"R5","text":"財務長交接與計量退出同時發生：2026-08-06 的財務長 Melissa Rasmussen，到 2026-11-05 已改由 Mike Morgan 發言，離任原因事實表未涵蓋；計量退出約 2,600 萬費用，保固義務留在公司，CEO 未正面回答有無對價。","h_ref":"H2","clock":"🔥","threshold":"計量退出總費用超過 3,100 萬美元、轉移拖到 FY28 下半，或調整項定義變更","evidence_refs":["major_events#0","ma_merger#0"]}],"single_thing":{"description":"FY27 第二季那次尚未公告的年度漲價，未能公告或留不住，使全年價格實現低於低個位數。","why_fatal":"價格是營收成長與利潤率擴張最可重複的來源，也是最大的單一敏感度：每 1 個百分點約影響 FY27 EPS 4.4%。FY27 價格成本對利潤率已只剩持平，這次沒守住就代表定價權到頂。","if_happens":"Base 轉向 Bear，margin 往 23% 回吐，EPS 往 1.33 到 1.41，股價約 15 到 17 美元；先減碼一半，下一季仍未回升則清倉。","how_monitor":"看 2027-02 第一季法說是否公告漲價，及 2027-05 第二季財報的全年價格實現、銷量與調整後毛利率；同時看對手是否跟進。","probability":"25%"}},"appendix_a":{"growth_durability":6,"quality_score":7,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":15.13,"peg_fy2":2.04,"stress":{"pass":null,"total":null}},"eps_meta":{"base_eps_path":{"FY2025A":1.31,"FY2026E":1.57,"FY2027E":1.59,"FY2028E":null},"fy_end_month":9,"eps_basis":"調整後每股盈餘。FY2025A 由 FY26 的 1.57 與年增 19.8% 反推。Koyfin FY1 未滾動，對應剛結束的 FY2026（公司已報實際 1.57，含 0.09 一次性，扣除後 1.48）；FY2 的 1.59 對應 FY2027，與指引隱含約 1.57–1.58 相符。FY2028 無共識，留空。若 FY1 實為 FY2027，則 FY2028 共識為 1.59，結論更保守。"},"catalysts":[{"date":"2026-11","date_precision":"month","type":"other","event":"FY26 10-K 發布，Mike Morgan 約 11-19 接任財務長","impact":"中","watch":"調整項定義、經銷商占比、財務長交接說明"},{"date":"2027-02","date_precision":"month","type":"guidance","event":"FY27 第一季財報","impact":"高","watch":"調整後毛利率是否連 2 季年減 ≥100 基點，是否公告新漲價，計量退出費用進度"},{"date":"2027-05","date_precision":"month","type":"guidance","event":"FY27 第二季財報","impact":"高","watch":"全年價格實現是否達低個位數以上，排除基期後銷量"},{"date":"2027-11","date_precision":"month","type":"regulatory","event":"鉛管規則改善版自 2027-11-01 起過渡，水務單位更新清冊與更換計畫","impact":"中","watch":"對市政維修汰換預算的實際帶動"}],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8(val爭議)","pacing":[],"holding_cap":null,"audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟠'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"輸入缺(momentum_overheated=null)，依保守方向處理：不視為觸發","input_gap":["momentum_overheated"]},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟡', moat_trend='→', week26=-8.31, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='受監管公用/穩定內需', cycle_position=None, moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈機械讀數判定不可用，baseline rows 8/9/9b/10 的估值條件視為不可判 → 落 row8 觀望（保守方向）","hit":true,"basis":"val_denominator_disputed=True, val(機械讀數)='🟡'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"requires_critic":[]}}
```

---

## ⑤ 覆蓋面（程式判定，你回的 ⑤ 燈號會被覆寫）

燈號 🟢：核心軸皆有證據或不適用，非核心軸也沒有空軸。plan 時 archetype 為「品質複利成長」、判斷者歸「受監管公用/穩定內需」，受監管公用/穩定內需 的專屬核心軸未採證（不計燈號）：regulated_rate_case_roe。

⑤ 的 reason 只需評論：空軸的查詢詞是否切題、判斷有沒有交代缺口對結論的影響。

---

## 尾段：回覆格式

只回一個 JSON 陣列，①–⑧ 每條一個元素，八個全出，不得跳號、不得多列，陣列外不得有任何文字（不加前言、不加 markdown 圍欄、不加附註）：

```json
[{"item": "①", "light": "🔴|🟡|🟢", "judgment_path": "$.路徑", "reason": "一句話"}]
```
