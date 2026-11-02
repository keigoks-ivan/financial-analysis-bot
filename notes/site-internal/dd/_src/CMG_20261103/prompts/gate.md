你是 DD 管線 v20 的判斷層閘（gate），標的 CMG（20261103）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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
- `f_kpi0_total_revenue_gaap`（q1_business）｜Total revenue (GAAP)＝3293.162 USD million；YoY +9.6%（Q3 2025 $3,003.4M）；QoQ -1.65%｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿（8-K Ex.99.1，ir.chipotle.com 發布）https://www.sec.gov/Archives/edgar/data/0001058090/000105809026000103/cmg-20261028xex991.htm（numbers.latest_quarter_kpis.items[0]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-28））
  - 註記：revenue 高於共識（Zacks；具體共識值未取得）
- `f_kpi1_gaap_operating_income`（q1_business）｜GAAP operating income＝451.964 USD million｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿（8-K Ex.99.1，ir.chipotle.com 發布）https://www.sec.gov/Archives/edgar/data/0001058090/000105809026000103/cmg-20261028xex991.htm（numbers.latest_quarter_kpis.items[1]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-28））
- `f_kpi2_gaap_operating_margin`（q1_business）｜GAAP operating margin＝13.7 %（Q3 2025: 15.9%）｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿（8-K Ex.99.1，ir.chipotle.com 發布）https://www.sec.gov/Archives/edgar/data/0001058090/000105809026000103/cmg-20261028xex991.htm（numbers.latest_quarter_kpis.items[2]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-28））
- `f_kpi3_restaurant_level_operati`（q1_business）｜Restaurant level operating margin (non-GAAP)＝23.3 %（Q3 2025: 24.5%）；公司不揭露 non-GAAP 營業利益率，以此替代｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿（8-K Ex.99.1，ir.chipotle.com 發布）https://www.sec.gov/Archives/edgar/data/0001058090/000105809026000103/cmg-20261028xex991.htm（numbers.latest_quarter_kpis.items[3]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-28））
- `f_kpi4_adjusted_diluted_eps_non`（q1_business）｜Adjusted diluted EPS (non-GAAP)＝0.27 USD（Q3 2025: 0.29）｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿（8-K Ex.99.1，ir.chipotle.com 發布）https://www.sec.gov/Archives/edgar/data/0001058090/000105809026000103/cmg-20261028xex991.htm（numbers.latest_quarter_kpis.items[4]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-28））
  - 註記：Zacks 稱 EPS 低於共識（具體值未取得）
- `f_kpi7_guidance_fy2026`（q1_business）｜Guidance FY2026＝— comps 低個位數成長；新店 350–370（含國際夥伴 10–15）；約 80% 新店含 Chipotlane；有效稅率 24–26%；Q4 comps 約 +2%（CFO 口徑，來自媒體轉述）｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司新聞稿（8-K Ex.99.1，ir.chipotle.com 發布）https://www.sec.gov/Archives/edgar/data/0001058090/000105809026000103/cmg-20261028xex991.htm（numbers.latest_quarter_kpis.items[7]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-28））
- `f_kpi8_guidance_fy2027`（q1_business）｜Guidance FY2027＝— 北美公司店新開 340–360；北美以外 15–25｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司新聞稿（8-K Ex.99.1，ir.chipotle.com 發布）https://www.sec.gov/Archives/edgar/data/0001058090/000105809026000103/cmg-20261028xex991.htm（numbers.latest_quarter_kpis.items[8]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-28））
- `f_kpi9_comparable_restaurant_sa`（q1_business）｜Comparable restaurant sales＝2.1 %（客單 +1.3%、交易數 +0.8%）；媒體轉述自新聞稿，共識約 1.5%｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：新聞稿 https://www.sec.gov/Archives/edgar/data/0001058090/000105809026000103/cmg-20261028xex991.htm ；彙整 capital.com／NRN（僅輔助）（numbers.latest_quarter_kpis.items[9]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-28））
  - 註記：共識約 1.5%（媒體轉述）
- `f_earnings_recency`（q1_business）｜最近一次財報日＝2026-10-28 date｜期間與口徑：2026-10-28／距今 4 個交易日｜kind：realized
  - 來源：—（numbers.earnings_recency，as_of 2026-10-28）
- `f_peer_cmg_gross_margin_pct`（q2_moat）｜CMG 毛利率＝23.84 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CMG.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_cmg_operating_margin_pct`（q2_moat）｜CMG 營業利益率＝14.95 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CMG.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_cmg_fcf_margin_pct`（q2_moat）｜CMG FCF 利潤率＝11.88 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CMG.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_mcd_operating_margin_pct`（q2_moat）｜MCD 營業利益率＝45.71 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MCD.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_cava_operating_margin_pct`（q2_moat）｜CAVA 營業利益率＝7.32 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CAVA.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_cava_fcf_margin_pct`（q2_moat）｜CAVA FCF 利潤率＝3.57 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CAVA.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_wing_operating_margin_pct`（q2_moat）｜WING 營業利益率＝27.74 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.WING.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_sbux_operating_margin_pct`（q2_moat）｜SBUX 營業利益率＝10.17 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.SBUX.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_sbux_fcf_margin_pct`（q2_moat）｜SBUX FCF 利潤率＝9.44 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.SBUX.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_kpi5_free_cash_flow_derived`（q1_business）｜Free cash flow (derived, 非公司揭露)＝347.1 USD million；9M OCF 1,922.1 - 9M capex 640.6 再減 H1（OCF 1,332.0 - capex 397.6）自行推算｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿（8-K Ex.99.1，ir.chipotle.com 發布）https://www.sec.gov/Archives/edgar/data/0001058090/000105809026000103/cmg-20261028xex991.htm ；https://www.sec.gov/Archives/edgar/data/0001058090/000105809026000063/cmg-20260729xex991.htm（numbers.latest_quarter_kpis.items[5]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-28））
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝12999.43 USD m｜期間與口徑：2026-11-03／yfinance revenue_estimate 0y 平均（32 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝1.1 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-10-31）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝1.34 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-10-31）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝1.55 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-10-31）
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝14381.87 USD m｜期間與口徑：2026-11-03／yfinance revenue_estimate +1y 平均（32 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi6_sbc_derived`（q4_capital）｜SBC (derived)＝31.9 USD million；占 GAAP 營業利益 7.0%、占營收 0.97%；9M 86.4 - H1 54.5 推算｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿（8-K Ex.99.1，ir.chipotle.com 發布）https://www.sec.gov/Archives/edgar/data/0001058090/000105809026000103/cmg-20261028xex991.htm ；https://www.sec.gov/Archives/edgar/data/0001058090/000105809026000063/cmg-20260729xex991.htm（numbers.latest_quarter_kpis.items[6]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-28））
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝4696.47 USD m｜期間與口徑：2026-11-03／yfinance 最新一季：總債務 5599.03、現金 902.56（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝1264.97 m shares｜期間與口徑：2026-11-03／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_ev_m`（q5_valuation）｜目前企業價值 EV（市值＋淨負債）＝46364.74 USD m｜期間與口徑：2026-11-03／市值 41668.27 ＋ 淨負債 4696.47｜kind：realized
  - 來源：—（numbers.capital_structure.ev_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝32.94 USD｜期間與口徑：2026-11-02（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-11-02（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝29.95 x｜期間與口徑：2026-10-31／分母＝FY1 EPS 1.1，分子＝快照價 32.94｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-10-31）
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝30.79 x｜期間與口徑：2026-11-02（RTH 收盤，UTC）／4 個年度端點內的分位＝0.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-11-02（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝0.0 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝3.28 x｜期間與口徑：2026-11-02（RTH 收盤，UTC）／4 個年度端點內的分位＝0.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝0.0 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝3.65 x｜期間與口徑：2026-11-02（RTH 收盤，UTC）／4 個年度端點內的分位＝0.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝0.0 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-11-02（RTH 收盤，UTC））
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝-2.65 %｜期間與口徑：2026-07-30 → 2026-10-31／FY1 共識 EPS 1.13 → 1.1（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-10-31）
- `f_consensus_rev_fy2_pct`（q5_valuation）｜FY2 共識修正＝-0.74 %｜期間與口徑：2026-10-31／兩份 Koyfin 快照之間的 EPS 修正幅度（1.35 → 1.34）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.fy2.revision_pct，as_of 2026-10-31）
- `f_consensus_rev_fy3_pct`（q5_valuation）｜FY3 共識修正＝-1.27 %｜期間與口徑：2026-10-31／兩份 Koyfin 快照之間的 EPS 修正幅度（1.57 → 1.55）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.fy3.revision_pct，as_of 2026-10-31）
- `f_ma_state`（q5_valuation）｜週線均線六態（decision_inputs.ma 必須等於此值）＝❌｜期間與口徑：2026-11-03／timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）
  - 原文：「price 32.85 / W52 34.42 / W104 42.38 / W250 41.54 / W250 13週斜率 -0.02%」
- `f_ma_w52`（q5_valuation）｜52 週均線＝34.42 USD｜期間與口徑：2026-11-03／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）
- `f_ma_w104`（q5_valuation）｜104 週均線＝42.38 USD｜期間與口徑：2026-11-03／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）
- `f_ma_w250`（q5_valuation）｜250 週均線＝41.54 USD｜期間與口徑：2026-11-03／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）
- `f_ma_slope_w250_pct`（q5_valuation）｜W250 13 週斜率＝-0.02 %｜期間與口徑：2026-11-03／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）
- `f_rsi14`（q5_valuation）｜RSI(14)＝61.03｜期間與口徑：2026-11-02（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-11-02（RTH 收盤，UTC））
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝3.0 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-11-02（RTH 收盤，UTC））

### findings_digest 中方向為負或來源衝突的條目（16 條）
- `competitive_share_entrants#0`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K 風險因素：競爭者（含非傳統參與者如雜貨即食餐、餐盒、幽靈廚房、外送平台）同樣主張高品質原料、無人工添加，可能削弱 CMG 差異化。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-04）｜affects：moat_trend、decision_inputs.bear
- `competitive_share_entrants#1`（competitive_share_entrants｜方向 -｜狀態 ok）：搜尋摘要：CAVA 2026 Q2 同店銷售 +9%、客流 +5.3%；CMG 2026 Q2 comps +2.2%、交易數 +1%，CAVA 成長快於 CMG（摘要轉述，未取得逐字原文）。
  - 來源：Nasdaq/Zacks 與 QSR Magazine 搜尋摘要（as_of 2026-08-01）｜affects：moat_trend、thesis.R
- `supply_demand_durability#0`（supply_demand_durability｜方向 -｜狀態 ok）：Bank of America 報告稱餐飲供給擴張快於消費者需求，單位數成長作為估值訊號的可靠度下降；僅 casual dining 單位數下降並維持低位。
  - 來源：BofA State of the Restaurant Industry 2026（as_of 2026-07-01）｜affects：thesis.R、decision_inputs.bear
- `supply_demand_durability#1`（supply_demand_durability｜方向 -｜狀態 ok）：一項 2026 年 6 月營運商調查：2025 年僅 14% 回報客流成長超過 1.5%，71% 預期 2026 年客流大致持平。
  - 來源：Coleman Report, Main Street Monday: Restaurant Operators Prioritize Catering, M&A, and New Unit Growth for 2026（as_of 2026-06-30）｜affects：thesis.R
- `regulatory_antitrust#0`（regulatory_antitrust｜方向 -｜狀態 ok）：Chipotle 8-K 揭露 FDA 與明尼蘇達衛生部調查與供應鏈相關的沙門氏菌疫情；明州機關無持續疑慮，問題追溯至單一批次墨西哥辣椒並已下架
  - 來源：SEC EDGAR 8-K 2026-08-04（as_of 2026-08-04）｜affects：decision_inputs.bear、thesis.R
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：10-K 載明部分食材（酪梨、番茄、牛肉、豬肉、萊姆、辣椒、香料）、設備與包材來自美國境外（墨西哥、加拿大、中國），可能面臨關稅、貿易制裁或稅負上升。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-04）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#1`（reg_tariff_export｜方向 -｜狀態 ok）：2025 年已實施關稅使食品飲料包材成本占營收比增加 0.2 個百分點，公司估計持續性影響約 15 bps。
  - 來源：SEC EDGAR 10-K FY2025 Item 7 MD&A（as_of 2026-02-04）｜affects：valuation、thesis.R
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：FY2024 10-K 揭露：部分食材（酪梨、番茄、牛肉、豬肉、萊姆、辣椒）、設備與包材來自美國境外（墨西哥、加拿大、中國），可能面臨關稅、貿易制裁或稅負；公司以遠期合約、關鍵供應商夥伴、分散供應基礎與原產國來緩解，但未必能完全避免價格上漲。
  - 來源：Chipotle FY2024 Form 10-K (SEC)（as_of 2025-02-06）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#2`（geo_supply_chain｜方向 -｜狀態 ok）：FY2025 10-K 摘要：2025 年已生效關稅預估持續影響食品、飲料與包材成本約 15 個基點（此為摘要轉述，未核 10-K 原文）。
  - 來源：Chipotle FY2025 Form 10-K (SEC)（as_of 2026-02-01）｜affects：thesis.R、valuation
- `end_markets#1`（end_markets｜方向 -｜狀態 ok）：CMG 2026 計畫漲價約 1%–2%，低於預期成本通膨 3%–4%，擠壓餐廳層級利潤率約 150bp；2025 可比銷售 -1.7%；2026Q2 可比 +2.2%、交易數 +1%。同業 CAVA 2026Q2 同店 +9%（客流 +5.3%），Sweetgreen 同店 -6.2%。
  - 來源：Nasdaq/Zacks: Chipotle's Pricing Lags Inflation; Chipotle Eyes Low-Single-Digit 2026 Comps（as_of 2026-07-30）｜affects：moat_trend、decision_inputs.bear、valuation
- `capital_markets_pricing#3`（capital_markets_pricing｜方向 -｜狀態 ok）：Wells Fargo 把 2026Q4 同店成長預估降至 1%（共識 3.2%）；TD Cowen EPS 預估低於共識（Q4 0.26 vs 0.28）——部分分析師低於共識，共識高於持平的原始 guidance
  - 來源：搜尋摘要（Wells Fargo、TD Cowen 預估修正）（as_of 2026-04-30）｜affects：decision_inputs.bear、valuation
- `capital_markets_pricing#5`（capital_markets_pricing｜方向 -｜狀態 ok）：Seeking Alpha 營收修正：8 上修 vs 24 下修（無日期快照）
  - 來源：Seeking Alpha CMG revisions（as_of 2026-10-24）｜affects：valuation
- `major_events#1`（major_events｜方向 -｜狀態 ok）：2026 年 8 月起沙門氏菌疫情與墨西哥墨西哥辣椒（jalapeño）有關，Chipotle 於 2026-07-20 為受影響店換供應商；供應商層級召回，非 Chipotle 自有產品召回
  - 來源：WGCU News：Fresh jalapenos recalled, link to salmonella cited, FDA investigation ongoing（as_of 2026-08-05）｜affects：thesis.R、decision_inputs.bear
- `major_events#2`（major_events｜方向 -｜狀態 ok）：Stradford v. Chipotle 股東集體訴訟：2025-12-18 法院准許駁回第一修正訴狀（可補件），2026-01-20 原告提第二修正訴狀，公司擬再聲請駁回
  - 來源：SEC EDGAR 10-K FY2025 Item 8（as_of 2026-02-04）｜affects：thesis.R、decision_inputs.bear
- `lawsuit_class_action#0`（lawsuit_class_action｜方向 -｜狀態 ok）：Stradford v. Chipotle 股東集體訴訟仍在審理，第二修正訴狀已提
  - 來源：SEC EDGAR 10-K FY2025 Item 8（as_of 2026-02-04）｜affects：thesis.R、decision_inputs.bear
- `product_recall_warning#0`（product_recall_warning｜方向 -｜狀態 ok）：沙門氏菌疫情關聯進口墨西哥辣椒，Chipotle 於 2026-07-20 換供應商；供應商 Coast Citrus 召回，非 Chipotle 自有召回
  - 來源：WGCU News（as_of 2026-08-05）｜affects：thesis.R、decision_inputs.bear

### 事實表自陳的缺口（2 條）
- q2_moat：evidence.numbers.peer_financials 該欄整欄為 null（常見於未單獨揭露研發的業者），事實表 agent 若能從財報補就補，補不到即為缺口，判斷者不得自行估。
- q6_how_wrong：digest.qa_flags 有 4 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CMG_20261103/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":70.8,"bear_5y_price":24.7,"p_bull_pct":20,"p_bear_pct":30,"upside_5y_pct":42.8,"ev5y_pct":36.9,"irr_base_pct":7.4,"asym_ratio":3.1,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":1.1,"pe":29.95,"basis":"FY2026 共識 EPS 1.10（當年度）；終端倍數同樣乘在終端年當年度的 EPS 上，兩者同口徑"},"eps":{"bull":[1.37,1.6,1.84,2.09,2.36],"base":[1.29,1.45,1.62,1.79,1.96],"bear":[1.14,1.18,1.22,1.26,1.3]},"pe":{"bull":30,"base":24,"bear":19},"p":{"bull":20,"base":50,"bear":30},"yield_pct":{"dividend":0,"net_buyback":0},"second_stage":{"bull_cagr_pct":13,"base_cagr_pct":9},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### CMG_Q2_2026_Earnings_Call_20260729.md
- 2026-07-29｜CFO｜guidance：CFO 表示全年同店銷售成長預期調整為低個位數區間（原話："expect full year comp sales growth in the low single-digit range"）
- 2026-07-29｜CFO｜guidance：CFO 給 Q3 同店約 +1%，並假設約 200bp 影響持續（原話："around a plus 1% in Q3, which does assume a continuation"）
- 2026-07-29｜CFO｜risk：CFO 說 7 月下半月出現約 200bp 的轉弱，與產業的 cyclospora 事件同時（原話："we did see a softening, call it about 200 basis points"）
- 2026-07-29｜CFO｜risk：CFO 提醒 Q3 的比較基期是今年最難的（原話："toughest lap that we have this year"）
- 2026-07-29｜CEO｜risk：CEO 說公司銷售受影響，但菜單不使用牽涉 cyclospora 的產品（原話："we are impacted from a sales perspective"）
- 2026-07-29｜CFO｜guidance：CFO 說 Q2 價格貢獻約 1.6%（原話："On pricing, the impact in Q2 was around 1.6%"）
- 2026-07-29｜CFO｜guidance：CFO 說全年價格貢獻預期落在先前 1%～2% 區間的高端（原話："we expect to land near the high end of the 1% to 2% range"）
- 2026-07-29｜CFO｜margin：Q2 餐廳層級利潤率 25.2%，年減 220bp（原話："Restaurant-level margin was 25.2%, down 220 basis points"）
- 2026-07-29｜CFO｜margin：Q2 銷貨成本率 29.7%，年增約 80bp（原話："were 29.7%, an increase of about 80 basis points"）
- 2026-07-29｜CFO｜margin：Q2 人力成本率 25%，年增約 30bp（原話："were 25%, an increase of about 30 basis points"）
- 2026-07-29｜CFO｜margin：Q2 其他營運成本率 14.9%，年增約 90bp（原話："were 14.9%, an increase of about 90 basis points"）
- 2026-07-29｜CFO｜guidance：Q3 銷貨成本率指引略低於 30%（原話："For Q3, we anticipate cost of sales to be just under 30%"）
- 2026-07-29｜CFO｜guidance：Q3 人力成本率指引在 25% 中段，工資通膨低個位數（原話："be in the mid-25% range with wage inflation in the low single-digit range"）
- 2026-07-29｜CFO｜guidance：Q3 其他營運成本率指引在 15% 中段（原話："For Q3, we anticipate other operating costs to be in the mid-15% range"）
- 2026-07-29｜CFO｜guidance：Q3 非 GAAP G&A 指引約 1.8 億美元（原話："G&A to be around $180 million on a non-GAAP basis"）
- 2026-07-29｜CFO｜guidance：全年有效稅率預估 24%～26%（原話："underlying effective tax rate will be in 24% to 26% range"）
- 2026-07-29｜CFO｜guidance：2026 折舊預期維持約占銷售 3%（原話："For 2026, we expect it to remain around 3% of sales."）
- 2026-07-29｜CFO｜margin：CFO 說價格與通膨的落差在上半年最大，Q3 起縮小，Q4 起預期兩者相當（原話："but from Q4 forward, we expect those 2 to match"）
- 2026-07-29｜CFO｜margin：CFO 預期 Q3 通膨約 3%，價格在 2% 中段（原話："in Q3, I would expect inflation to be closer to about 3%"）
- 2026-07-29｜CFO｜margin：CFO 將價格與通膨的落差描述為時間點因素，並說會續用滾動式調價（原話："That was really just a timing impact."）
- 2026-07-29｜CFO｜margin：CFO 說未來幾年可持續投入 Recipe for Growth 並對 G&A 取得槓桿（原話："we can continue to fuel our Recipe for Growth strategy and"）
- 2026-07-29｜CFO｜margin：Q2 同店成長 2.2% 含 1% 交易數成長（原話："including a transaction comp of 1%"）
- 2026-07-29｜CFO｜margin：Q2 調整後 EPS 0.33 美元，與去年持平（原話："per share was $0.33, flat to last year"）
- 2026-07-29｜CFO｜customer：數位銷售占比由 35.5% 升至 38.3%（原話："38.3% of total sales compared to 35.5% in the prior year"）
- 2026-07-29｜CFO｜capital_allocation：CFO 說 Q2 回購 6.31 億美元，董事會再增授權 13 億美元（原話："the Board authorized an additional $1.3 billion"）
- 2026-07-29｜CFO｜capital_allocation：Q2 回購金額與均價（均價 32.55 美元）（原話："$631 million in the second quarter at an average price"）
- 2026-07-29｜CEO｜commitment：CEO 維持今年約開 350 家公司自營餐廳（原話："expect to open approximately 350 restaurants this year"）
- 2026-07-29｜CEO｜capital_allocation：CEO 說 350 家是團隊認可的開店速度，並提到超過可能的風險（原話："could possibly fracture the base if you get too aggressive"）
- 2026-07-29｜CEO｜capital_allocation：CEO 對 350 家的表態（原話："But I like 350 number. The team likes it."）
- 2026-07-29｜CFO｜capital_allocation：新店生產力與第二年現金投資報酬（原話："restaurant productivity has remained stable in the 80% range"）
- 2026-07-29｜CFO｜capital_allocation：第二年 cash-on-cash 報酬約 60%（原話："year 2 cash-on-cash returns continue to be around 60%"）
- 2026-07-29｜CFO｜capital_allocation：新店對既有店同店的淨影響約 100bp（原話："comparable restaurant sales is approximately 100 basis points"）
- 2026-07-29｜CFO｜commitment：CFO 說對北美至少 7,000 家的營運能力有信心（原話："our ability to operate at least 7,000"）
- 2026-07-29｜CEO｜capital_allocation：CEO 說翻新方案處於階段性驗證，每店試投 10 萬至 30 萬美元（原話："think between $100,000 and $300,000 per"）
- 2026-07-29｜CEO｜capital_allocation：CEO 說西歐續自營、其餘地區以合作夥伴營運（原話："own and operate Western Europe and grow from that base"）
- 2026-07-29｜CEO｜product：HEEP 設備目標年底約 2,000 家餐廳（原話："approximately 2,000 restaurants by year-end"）
- 2026-07-29｜CEO｜commitment：CEO 希望 2027 年內全系統完成 HEEP 安裝（原話："to have the entire portfolio completed sometime in 2027"）
- 2026-07-29｜CEO｜product：CEO 說 HEEP 餐廳尖峰 15 分鐘多出 2～3 份，並說對同店有數百 bp 的改善（原話："translating into hundreds of basis points of improvement in"）
- 2026-07-29｜CEO｜margin：CEO 說 HEEP 每日省 2～4 小時人力，並留在餐廳內再投資（原話："2 to 4 hours of efficiency depending"）
- 2026-07-29｜CFO｜product：CFO 說系統整體 max 15 約在 30 出頭至中段（原話："to mid-30s on our max 15 for each restaurant each day"）
- 2026-07-29｜CEO｜customer：店內交易使用 Rewards 的比例偏低，對比自有數位通路（原話："compared to nearly 90% of owned digital transactions"）
- 2026-07-29｜CEO｜commitment：CEO 說 8 月起試行店內免掃碼的 Rewards（原話："in-restaurant Rewards experience beginning in August"）
- 2026-07-29｜CEO｜customer：Rewards 活躍會員數（原話："With 23 million active members in our"）
- 2026-07-29｜CEO｜customer：CEO 引用品牌追蹤調查，說明價值認知改善（原話："Our affordability scores were better in Q2 than"）
- 2026-07-29｜CFO｜customer：CFO 說年輕與低收入族群改善幅度最大（原話："They really have improved the most"）
- 2026-07-29｜CEO｜competition：CEO 說 2026 年每個月都在搶市占（原話："we have taken share in each month of 2026"）
- 2026-07-29｜CEO｜product：CEO 說 LTO 重推有邊際遞減的可能（原話："think there's a point of diminishing returns"）
- 2026-07-29｜CEO｜product：CEO 說菜單創新量已為數年前的 4 倍（原話："ramped up innovation in menu 4x what it was"）
- 2026-07-29｜CEO｜product：下半年再推兩款限時蛋白質品項（原話："2 additional limited time protein options"）
- 2026-07-29｜CFO｜product：CFO 說 LTO 帶來的交易數提升多數在活動期間持續（原話："we typically see hundreds of basis points of trans lift"）
- 2026-07-29｜CFO｜product：CFO 將 LTO 描述為長期拉升 AUV 的槓桿（原話："we see this as a multiyear lever of increasing our AUVs"）
- 2026-07-29｜CEO｜commitment：CEO 說外帶團膳與 Build-Your-Own 占銷售 2%～3%，目標 2027 年全國推出（原話："national launch in 2027"）
- 2026-07-29｜CEO｜customer：團膳與 Build-Your-Own 目前占銷售比重（原話："represent 2% to 3% of sales today"）
- 2026-07-29｜CEO｜competition：CEO 說新品牌方向不是大轉彎而是 For Real 的演進（原話："it's not a 180 pivot. It's really the next evolution of what"）
- 2026-07-29｜CEO｜commitment：CEO 說新品牌訊息的第一批元素本季稍晚出現（原話："Later this quarter, we will begin to see the first elements of"）
- 2026-07-29｜CEO｜capital_allocation：歐洲各國同店達高個位數成長（原話："each country deliver high single-digit comp sales growth"）
- 2026-07-29｜CEO｜commitment：CEO 說墨西哥市場 2027 年擴展至墨西哥城（原話："Mexico City in 2027"）
- 2026-07-29｜CEO｜commitment：CEO 說今年開首爾店、新加坡接續（原話："Seoul, South Korea this year with Singapore"）
- 2026-07-29｜CEO｜risk：CEO 說中東近期發展取決於地緣政治（原話："near-term development remains dependent on geopolitical"）
- 2026-07-29｜CEO｜commitment：CEO 說計畫進入沙烏地阿拉伯市場（原話："enter the Saudi Arabian market in the near future"）
- 2026-07-29｜CFO｜risk：CFO 說世足賽對整體季度的影響不到 5bp（原話："the impact was less than 5 basis points"）
- 2026-07-29｜CEO｜commitment：CEO 說公司在規劃明年初的投資人活動（原話："we're working on a plan to gather many of the"）

### 問答異常語氣（迴避／改口／保留）
- CMG_Q2_2026_Earnings_Call_20260729.md｜問：Evercore（David Palmer）：如何確信 2027 年動能會增強、而非只是花很多錢換 1%～2% 同店｜答法：CEO 以 green shoots、早期證據、尚在早期等描述回應，沒有給 2027 的數字或量化指標
- CMG_Q2_2026_Earnings_Call_20260729.md｜問：UBS（Dennis Geiger）後 CEO 補述 cyclospora 對公司的影響｜答法：CEO 先說 not impacted，隨即改口 or we are impacted from a sales perspective，再說不涉入該事件
- CMG_Q2_2026_Earnings_Call_20260729.md｜問：Bernstein（Danilo Gargiulo）：餐廳翻新方案的增量資本支出規模與預期銷售提升｜答法：CEO 只給每店 10 萬至 30 萬美元的試驗區間，說 I have nothing to report today，未給 capex 總額與預期銷售提升
- CMG_Q2_2026_Earnings_Call_20260729.md｜問：Stephens（Jim Salera）：LTO 對交易數的貢獻比重與歷史基準｜答法：CFO 說未提供個別 LTO 的細節，改以定性描述與數百 bp 的區間回應，未給占整體交易的比重

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 3 | 2 |
| customer_second_source | not_applicable | 0 | 0 |
| customer_concentration_credit | not_applicable | 0 | 0 |
| supply_demand_durability | found | 5 | 4 |
| regulatory_antitrust | found | 1 | 3 |
| reg_tariff_export | found | 3 | 1 |
| geo_supply_chain | found | 3 | 2 |
| end_markets | found | 3 | 3 |
| substitute_technology | found | 2 | 2 |
| channel_business_model_shift | found | 3 | 2 |
| capital_markets_pricing | found | 6 | 4 |
| major_events | found | 3 | 4 |

未涵蓋／不適用軸的查詢詞原文（供判相關性）：
- **customer_second_source**（not_applicable）：（無查詢記錄）
- **customer_concentration_credit**（not_applicable）：（無查詢記錄）

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260730","verdict":"觀望","role":"追蹤","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"美國同店回到「價量同正」的正循環，且交易量成長可在 MCD／Taco Bell 三美元價格帶戰下維持（最關鍵的結構性假設——它決定 §11 該用複利尺還是成熟連鎖尺）"},{"id":"H2","text":"餐廳層營業利潤率在 FY2026 見底（H1 為 24.4%），並於 FY2028 前回到 26%+（成長兌現的操作性假設——三個成因裡兩個是自選、一個是外生循環）"},{"id":"H3","text":"Y5 之後的成長不必只靠北美開店：國際夥伴店與外燴／Build-Your-Own 構成可量化的第二曲線（估值修復的市場假設——市場願意給幾倍，取決於它相信不相信這條）"}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"成本橋比管理層說的長：牛肉／貨運通膨在 2027 再創新高，迫使菜單提價拉到 3%+，餐廳層利潤率結構性卡在 23-24%。管理層 Q2 明示「Q4 起價格與通膨對齊、之後不再有錯位」，但 USDA 自己的預估是 2027 育肥牛價 $254.25/cwt 高於 2026 的 $251.10、2026 產量 −1.8%、存欄 86.2 百萬頭仍在收縮"},{"id":"R2","text":"零和客流市場裡份額拿不夠：業界整體客流成長 &lt; 1%（Circana 2026），CAVA 客流 +6.8% 對 CMG 的 +1.0%；同時 MCD／Taco Bell 的三美元價格帶戰進入第三年，&lt; $40k 家戶年收入的客群外食頻次與單次消費雙降。CMG 被夾在「向下的價值戰」與「向上的高成長品類」之間"},{"id":"R3","text":"本輪最被前一份報告漏掉的一軸：勞動供給與法規成本的雙重收緊。美國餐飲廚師 37% 為外籍出生、2026 年全國工作場所執法約每日 900-1,000 件逮捕（橘郡 8 週產出損失約 $5,900 萬、洛杉磯部分商業區人流一度 −80%）；加州快餐委員會保留在 $20/小時之上加碼至多 $0.70/小時的裁量權且正在評估；USMCA 2026 聯合檢視期會影響墨西哥生鮮與酪梨的成本基礎。這一軸直接威脅 §7 execution 護城河的支柱（總經理流動率多年新低、HEEP 人工效率）——效率設備省下的工時，需要有人在崗才能被再投入"}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"單一條件：餐廳層營業利潤率連 2 季 YoY 轉正（等價於絕對值連 2 季 ≥ 26.0%）——此一條件同時解除衰退燈、陷阱定性 🔴 與 PEG > 2.0 三個限制。價格回落至 $29.4 只降低進場成本、不解除限制。","irr_base_pct":10.3,"ev5y_pct":43.2,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"追蹤","signal":"C","val":"🟠","ma":"❌","trap":"🔴","moat_trend":"→","runway_post_y5":"🟡","asym_ratio":2.6,"ev5y_pct":43.2,"irr_base_pct":10.3,"max_dd_pct":-48.0,"bull_5y_price":71.5,"bear_5y_price":25.5,"p_bull_pct":20.0,"p_bear_pct":33.0,"rearm_trigger":"單一條件：餐廳層營業利潤率連 2 季 YoY 轉正（等價於絕對值連 2 季 ≥ 26.0%）——此一條件同時解除衰退燈、陷阱定性 🔴 與 PEG > 2.0 三個限制。價格回落至 $29.4 只降低進場成本、不解除限制。","price_at_dd":34.24,"archetype":"品質複利成長","cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"CMG","date":"2026-11-03","schema":"v15.0","contract":"v19","company_name":"Chipotle Mexican Grill"},"oneliner":"交易數連三季為正，但餐廳層利益率還在往下；30 倍本益比已先算進 2027 年利益率回到 24.5%，要先看到連兩季利益率年增轉正，再談進場。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CMG_20261103/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/CMG_20261103/scenario.json","answers":{"q1_business":{"verdict":"向美國偏年輕、中高收入的外食客賣客製化墨西哥快餐，全數自營，營收不必與加盟主分；目前錢卡在餐廳層：定價追不上食材與工資通膨，交易數只微增，第三季餐廳層利益率由 24.5% 降到 23.3%。","reasoning":"第三季營收 32.93 億美元，年增 9.6%。其中同店 +2.1%（客單 +1.3%、交易數 +0.8%），其餘約 7.5 個百分點主要來自新店。同店裡定價貢獻 2.7%，組合效果 −1.4%，原因是忠誠會員兌換讓每單人數變少。成本面：食材 29.5%，年減約 50bp，靠定價與關稅減免抵銷牛肉、運費上漲；人力 25.7%，年增約 50bp；其他營運成本 16.0%，年增約 100bp，來自行銷加碼與外送占比上升。餐廳層利益率 23.3%，GAAP 營業利益率 13.7%（去年 15.9%），調整後 EPS 0.27 美元，年減 7%。全年指引為同店低個位數、新店 350–370 家；第四季同店約 +2%，利益率略低於 22%。本季最關鍵的一句是 CFO 自己說的：在 3% 通膨下，名目同店要到約 4% 才能穩住利益率。單點依賴：沒有客戶集中；供應端酪梨約半數來自墨西哥，其餘來自哥倫比亞、秘魯、多明尼加，但 2026 年 7 月單一批次墨西哥辣椒的沙門氏菌事件，說明單一食材仍可能拖累全系統。產業時鐘判在 III：供給擴張快於需求，2026 年實質銷售預期下修到 +0.8%，客流持平，速食業又在打低價套餐。這是供給過剩的晚段，不是需求崩落。","fact_refs":["f_kpi0_total_revenue_gaap","f_kpi1_gaap_operating_income","f_kpi2_gaap_operating_margin","f_kpi3_restaurant_level_operati","f_kpi4_adjusted_diluted_eps_non","f_kpi7_guidance_fy2026","f_kpi8_guidance_fy2027","f_kpi9_comparable_restaurant_sa","f_earnings_recency"],"verdict_values":{"revenue_quality":"幾乎全部是自營餐廳的餐飲銷售。數位占 38.8%，忠誠會員占銷售逾 33%，創新高；外燴與家庭餐約 3%；國際合作店權利金占比事實表未涵蓋。","unit_econ_note":"新店生產力約 80%，第二年現金回報約 60%，新店對既有店同店拖累約 100bp（2026-07-29 CFO）。HEEP 滿載店尖峰 15 分鐘多出 2 份主餐，同店多約 200bp。交易數要成長約 1 個點才能抵銷新店對利益率的拖累，超過的部分約以 40% 傳導到利益率（2026-10-28 CFO）。","archetype":{"primary":"品質複利成長","secondary":null,"confidence":"中","fingerprint":"全自營展店加同店低個位數成長，利益率處於定價落後通膨之後的修復期"},"industry":{"clock_phase":"III","sd_verdict_source":"供需壓力屬週期性，供給可逆性高。BofA 指出餐飲供給擴張快於需求；2026 年 6 月業者調查有 71% 預期客流持平；NRA 把 2026 年實質銷售預期由 +1.3% 下修到 +0.8%，但 2027 年名目預期回升到 +4.8%。餐廳可以關店退出，過剩供給會在 1–2 年內出清，不是結構性的需求萎縮。","bargaining":{"up":"食材向分散的供應商採購，用遠期合約與多產地分散風險；牛肉與運費通膨只能靠菜單價轉嫁","down":"顧客都是散客，沒有集中客戶；議價壓力來自消費者對漲價的容忍度，以及同業的低價套餐","geo":"酪梨、番茄、牛肉、豬肉、萊姆、辣椒有一部分來自墨西哥與加拿大；2025 年實施的關稅持續影響成本約 15bp，第三季已出現關稅減免"},"profit_pool_dir":"快休閒內部分化：2026 年第二季 CAVA 同店 +9%、CMG +2.2%、Sweetgreen −6.2%；利益池占比的歷史數據事實表未涵蓋","tam_table":{"expanded":false,"reason":"真正承重的是北美展店空間（管理層稱至少 7,000 家）與同店，不是市場規模擴張；國際合作店與外燴還在早期，目前不承重，展店空間在成長題處理"}}}},"q2_moat":{"verdict":"護城河持平（→）：執行力在擴大，定價力在收縮，兩者相抵，綜合 B 級。","reasoning":"護城河的機制是品牌定位加上全自營的展店模式：新店第二年現金回報約 60%，而且不必與加盟主分潤。執行面在改善：HEEP 已裝 1,700 家，滿載店尖峰多 2 份主餐、同店多約 200bp；總經理與員工流動率年減，Taste of Food 分數年增近 1 分。定價面在退步：2026 年定價約 2%，低於 3–4% 的通膨，得靠買一送一與加碼行銷換交易數；分析師在法說上指出行銷支出今年以來年增逾 20%，管理層沒有否認；組合效果 −1.4%。同業比較：CMG 的 TTM 營益率 14.95%，高於 CAVA 的 7.32% 與 SBUX 的 10.17%；低於 MCD 的 45.71% 與 WING 的 27.74%，但後兩家以加盟為主，模式不同，不能直接比。CMG 自身營益率已由 FY2024 的 17.55% 降到 14.95%，與 CAVA 的差距可能在收窄；CAVA 的歷史數據事實表未涵蓋，方向無法驗證。投入資本事實表也未涵蓋，當期 ROIC 只能用新店現金回報代用。","fact_refs":["f_peer_cmg_gross_margin_pct","f_peer_cmg_operating_margin_pct","f_peer_cmg_fcf_margin_pct","f_peer_mcd_operating_margin_pct","f_peer_cava_operating_margin_pct","f_peer_cava_fcf_margin_pct","f_peer_wing_operating_margin_pct","f_peer_sbux_operating_margin_pct","f_peer_sbux_fcf_margin_pct","f_kpi3_restaurant_level_operati","f_kpi5_free_cash_flow_derived","f_rev_consensus_fy1_m"],"verdict_values":{"moat":{"mechanism":"品牌與食材定位，加上全自營的展店模式：新店第二年現金回報約 60%，不必與加盟主分潤；流量靠規模化採購、Chipotlane（已達 1,500 家）與 2,400 萬忠誠會員支撐","execution":8,"pricing":6,"grade":"B","trend":"→","trend_evidence":"執行力在擴大：HEEP 已裝 1,700 家，約一半已滿 2–3 個月，同店效益還在累積；員工流動率年減。定價力在收縮：2026 年定價落後通膨約 100bp，要靠促銷與行銷換交易數，組合效果 −1.4%。兩者相抵，判為持平。對 CAVA 的營益率差距為 7.6 個百分點，但 CMG 自身營益率兩年內掉了 2.6 個百分點，差距可能在收窄。","competitor_notes":[{"name":"MCD","strategy_note":"以加盟收租為主，45.7% 的營益率反映權利金模式，不是單店經濟；對 CMG 的威脅在於用低價套餐爭取價格敏感的客群"},{"name":"CAVA","strategy_note":"營益率 7.3%、自由現金流率 3.6%，經濟體質弱於 CMG；但 2026 年第二季客流 +5.3%，是新品類裡搶增量客流最明顯的一家"},{"name":"WING","strategy_note":"以加盟為主，營益率 27.7%，品類不同，與 CMG 的重疊主要在外送與年輕客群的時段"},{"name":"SBUX","strategy_note":"營益率 10.2%、自由現金流率 9.4%，都低於 CMG；FT 報導它曾評估收購 CMG，但未見正式出價"}],"peer_na_reason":"事實表只有同業的三項利益率，沒有投入資本與 ROIC；只能以營益率差代用，CMG 比 CAVA 高 7.6 個百分點，差距的趨勢無法驗證","threats":[{"level":"🟡","text":"CAVA 等新品類對手搶走增量客流：2026 年第二季 CAVA 客流 +5.3%，CMG 交易數 +1%。屬點對點競爭；CAVA 規模遠小、營益率 7.3%，還沒有威脅到 CMG 的單店經濟","p":"35%","evidence_refs":["competitive_share_entrants#1"]},{"level":"🟡","text":"雜貨即食、餐盒、雲端廚房與外送平台也主打高品質原料、無人工添加，削弱 CMG 的差異化（公司在 10-K 風險因素中自述）","p":"30%","evidence_refs":["competitive_share_entrants#0"]},{"level":"🟡","text":"速食業者的低價套餐拉走價格敏感客群（前份證據，本包沒有更新）；本季公司反而表示低收入客群跑贏高收入客群","p":"25%","evidence_refs":[]}],"roic_durability":{"quadrant":"高利益率×高周轉","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者、決策者與付款者都是消費者本人，屬於想要而不是需要，外食可以延後。產業 2026 年實質銷售預期只有 +0.8%，71% 的業者預期客流持平。CMG 交易數 +0.8%，到訪人次年增 6.0%，高於類別的 1.9%；需求基礎還在，但不是剛需。"},{"item":"決策層級","level":"🟡","text":"替代性要用單餐的決策來看：每一餐都可以換別家，轉換成本只有忠誠點數。正面證據是忠誠會員 2,400 萬、占銷售 33% 創新高，數位占 38.8%；第三季定價 2.7%，交易數仍有 +0.8%。但 2025 年同店 −1.7%，代表上一輪提價時已經碰過定價彈性。"},{"item":"價值鏈分配","level":"🟢","text":"全自營，不與加盟主分潤；食材向分散的供應商採購，靠遠期合約與多產地分散（酪梨約半數來自墨西哥以外）。外送平台是唯一會分走毛利的環節，但外送是本季數位通路中成長最慢的，自取與 Chipotlane 成長最快，價值留在公司手上。"},{"item":"社會容忍度","level":"🟡","text":"平價定位下，消費者對漲價與份量縮水的容忍度低。管理層刻意讓 2026 年定價（約 2%）低於通膨，等於自設了價格天花板；CFO 也說 2027 年不容易回到 2% 的定價。社會對食安的容忍度更低：2026 年 7 月的產業性食安事件，讓同店短暫少了約 200bp。"}],"roiic":"約 35%","reinvest_rate":"約 31%","endo_ceiling":10.8,"formula_note":"再投資率＝（資本支出－折舊）÷ 稅後營業利益。2026 年前三季資本支出 6.41 億美元，年化約 8.5 億；折舊約占營收 3.1%（第三季 1.03 億），以 FY2026 共識營收 130 億計約 4.0 億；淨再投資約 4.5 億。稅後營業利益＝TTM 營益率 14.95% × 130 億 ×（1－25%）≈ 14.6 億，因此再投資率約 31%。餐飲業營運資金為負，且沒有收購，兩項都略去。增量報酬：新店第二年現金回報約 60%（稅前、餐廳層，2026-07-29 CFO），扣 25% 稅後約 45%；再扣新店對既有店約 100bp 的同店蠶食（新店生產力約 80%）與總部費用分攤，保守取 35%。內生成長上限＝35% × 31% ≈ 10.8%/年。投入資本與租賃資本事實表未涵蓋，當期 ROIC 無法以財報口徑精算。"}}}},"q3_growth":{"verdict":"北美展店期在第 5 年之後仍未結束，但已走過一半，第二曲線還在早期，判為中等（🟡）。","reasoning":"成長組成：第三季營收 +9.6%，其中同店 +2.1%，其餘約 7.5 個百分點主要來自新店。同店裡價 +2.7%、量（交易數）+0.8%、組合 −1.4%；沒有併購；回購每年約減少 2–3% 股數。共識三年 EPS 為 FY2025A 1.14、FY2026E 1.10、FY2027E 1.34、FY2028E 1.55，年增約 10.8%（FY2026 共識的分析師家數事實表未涵蓋，Chartmill 同期為 38 家）。這和內生上限 10.8% 幾乎一樣，沒有緩衝。FY2027–28 的跳升靠利益率回到約 24.5% 加上回購，屬於可以歸因的利益率修復，不是靠重新評價。北美展店：管理層稱至少可經營 7,000 家，每年開約 350 家；目前店數事實表未涵蓋，但從 2027 年 340–360 家的指引看，第 5 年後仍在展店。第二曲線：外燴 2027 年第一季全國推出，目標每年多 1–2 個點占比（目前約 3%）；北美以外 2027 年開 15–25 家，全部是合作店，11 國才剛起步；第三季歐洲自營店同店成長在低雙位數。兩者目前都不夠承重，所以不給寬的評等。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_kpi0_total_revenue_gaap","f_kpi9_comparable_restaurant_sa","f_kpi7_guidance_fy2026","f_kpi8_guidance_fy2027","f_kpi6_sbc_derived"],"verdict_values":{"growth":{"driver_mix":"量（新店約 7 個百分點）加價（定價 2–3%）加交易數約 1%，再加上回購每年約 2–3%；沒有併購","runway_years":"事實表未涵蓋目前店數；依管理層至少 7,000 家的北美目標與每年約 350 家的速度，北美展店延伸到第 5 年之後","runway_post_y5":"🟡","endo_ceiling_basis":"增量報酬約 35%（新店第二年現金回報約 60%，扣稅與同店蠶食後保守取值）× 再投資率約 31%（年化資本支出約 8.5 億減折舊約 4.0 億，除以稅後營業利益約 14.6 億）＝約 10.8%；推導見護城河題","segments":{"expanded":false,"reason":"公司只有自營餐廳一個營運分部，國際合作店權利金占比事實表未涵蓋；利潤由單店經濟決定，不由分部組合決定"},"decay_signals":[{"signal":"毛利率連 2 季年減","lit":true,"note":"餐廳層利益率第二季年減 220bp、第三季年減 120bp，第四季指引再年減約 150bp"},{"signal":"核心市占近 12 個月縮減","lit":false,"note":"客流成長落後 CAVA，但到訪人次年增 6.0% 高於類別 1.9%，管理層也稱 2026 年每個月都在拿份額；證據互相衝突，不亮"},{"signal":"主力產品提價後銷量下滑","lit":false,"note":"第三季定價 2.7%，交易數仍 +0.8%，2026 年三季交易數皆為正；2025 年同店 −1.7% 屬於上一輪"},{"signal":"EPS 成長顯著高於營收成長（差距大於 5 個百分點）","lit":true,"note":"FY2022–FY2025 EPS 年增約 21%，營收年增約 11%，差距約 10 個百分點，來自利益率擴張，現在正在回吐"},{"signal":"自由現金流／淨利連 2 年低於 0.75","lit":false,"note":"FY2024 約 0.99、FY2025 約 0.94"},{"signal":"股票酬勞／營收大於 5% 且逐年上升","lit":false,"note":"第三季約 0.97%"},{"signal":"市場規模萎縮或被替代技術壓縮","lit":false,"note":"廚房全自動化只在極高量、少品項的速食店可行；對 CMG 而言是內部的效率工具"},{"signal":"產業估值倍數近 3 年系統性下移","lit":false,"note":"產業倍數事實表未涵蓋；CMG 自身本益比在近 4 個年度端點中最低，但不能代表整個產業"},{"signal":"維護性資本支出占自由現金流大於 60%","lit":false,"note":"資本支出以新店為主；維護與成長的拆分事實表未涵蓋"},{"signal":"停止投資新產能且營收 3 年內下滑","lit":false,"note":"每年仍開約 350 家"}]}}},"q4_capital":{"verdict":"資本配置穩健，但回購報酬偏低：沒有金融負債，自由現金流約等於淨利，現金幾乎全數用在展店與回購；但在約 30 倍本益比回購，每 1 美元只買到約 3 美分的盈餘。","reasoning":"自由現金流轉換率高：FY2024 自由現金流 15.1 億對淨利 15.3 億（約 0.99），FY2025 為 14.5 億對 15.4 億（約 0.94）；第三季推算的自由現金流為 3.47 億。第三季股票酬勞 3,190 萬美元，約占營收 0.97%、GAAP 營業利益 7.0%。資產負債表：現金、受限現金與投資約 10 億美元，沒有金融負債；事實表的淨負債 47.0 億是租賃負債口徑。2026 年前三季的現金去向：營業現金流 19.2 億，資本支出 6.4 億、回購 14 億，股利與併購皆為零，回購略超過自由現金流；近三年完整的四分法事實表未涵蓋。回購方面，今年至今均價 34.32 美元，剩餘授權約 16 億；第二季回購 6.31 億、均價 32.55 美元，董事會另加 13 億授權（2026-07-29 CFO）。以 FY2026 共識 EPS 1.10 計，回購價位的盈餘殖利率約 3.2%。管理層說股價被低估，但在這個價位回購，只是把現金換成每年約 3% 報酬的盈餘。營運槓桿反向：第三季營收 +9.6%，GAAP 營業利益 4.52 億，去年約 4.78 億（15.9% × 30.03 億），約 −5%；兩者差距約 15 個百分點，屬於壓縮，已放進空頭情境。","fact_refs":["f_kpi6_sbc_derived","f_kpi5_free_cash_flow_derived","f_kpi1_gaap_operating_income","f_kpi2_gaap_operating_margin","f_net_debt_m","f_shares_diluted_m","f_ev_m","f_consensus_eps_fy1"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":false,"passed":null,"input":"近年沒有收購，成長全靠自營展店"},{"name":"buyback_yield","applicable":true,"passed":false,"input":"2026 年至今回購 14 億美元、均價 34.32 美元，對應 FY2026 共識 EPS 1.10 的盈餘殖利率約 3.2%；10 年期公債殖利率事實表未涵蓋，但只要殖利率高於 1.2%，就達不到「殖利率加 2 個百分點」的門檻"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"第三季股票酬勞 3,190 萬美元，年化約 1.3 億，約為市值 417 億的 0.3%；同期回購讓股數淨減少，淨稀釋為負"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購；資本回報以回購為主，金額與均價已寫在本題理由"}}}},"q5_valuation":{"verdict":"現價要求五年 EPS 年增約 15%，而且 2031 年仍要給到 24 倍，才有 10% 的年化報酬；我只信得過約 12% 的 EPS 年增，價格偏貴，但不離譜。","reasoning":"前瞻本益比 29.95 倍（FY2026 共識 EPS 1.10），trailing 本益比 30.79 倍；P/S 3.28 倍，EV/營收 3.65 倍。三者都落在近 4 個年度端點的最低位置，但這是年度端點分位，不是五年分位；五年分位事實表未涵蓋。分母方面：FY2026 EPS 比 FY2025 的 1.14 還低，含約 100bp 的定價錯位，常態化後約 1.18，本益比約 28 倍，結論不變。PEG 2.77（以 FY2025A 到 FY2028E 共識年增 10.8% 計）；FY2027 本益比 24.6 倍，PEG 2.28。反推現價：若終端給 24 倍，五年年化 10% 需要 FY2031 EPS 約 2.21 美元，也就是年增約 15%，高於內生上限 10.8% 加回購約 2.5%。我的基本情境 FY2031 EPS 為 1.96、年增約 12%，對應的年化報酬只有個位數。賣方平均目標價約 42.9 美元（2026-08），區間約 35–52 美元，現價低於區間下緣，代表賣方比我樂觀。Starbucks 曾評估收購的報導未見出價，不計入任何情境。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_pe_current","f_pe_percentile","f_ps_current","f_ps_percentile","f_ev_s_current","f_ev_s_percentile","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_3m_fy1_pct","f_consensus_rev_fy2_pct","f_consensus_rev_fy3_pct","f_ev_m","f_net_debt_m"],"verdict_values":{"valuation":{"basis":"前瞻本益比（以 FY2026 共識 EPS 計）與 PEG","peers":{"expanded":false,"reason":"事實表只有同業利益率，沒有同業本益比；終端倍數改以 CMG 自身本益比位置（近 4 個年度端點最低）與成長熄火情境來定錨"},"fwd_pe":29.95,"peg":2.77,"percentile_5y":null,"val_light":"🟠","val_light_derivation":"PEG 2.77（前瞻本益比 29.95 倍 ÷ FY2025A 到 FY2028E 共識 EPS 年增 10.8%），落在大於 2 的偏貴區；FY2027 本益比 24.6 倍、PEG 2.28，仍然偏貴。本益比、P/S、EV/營收都在近 4 個年度端點的最低位置，抵銷一部分，因此判為 🟠（偏貴，但不到極貴）。五年分位事實表未涵蓋，所以不填。","upside_short_pct":12.6,"upside_mid_pct":29.7,"denominator_disputed":false,"denominator_note":"FY2026 EPS 1.10 低於 FY2025 的 1.14，含 CFO 所說約 100bp 的定價落後通膨。以 FY2026 共識營收 130 億計，影響稅前約 1.3 億、每股約 0.08 美元；常態化 EPS 約 1.18，本益比約 28 倍。偏貴的結論不變，所以不列為分母爭議。短期與中期上檔以基本情境 EPS 乘上由 30 倍線性降到 24 倍的路徑計算：一年後 1.29 × 28.8 倍，三年後 1.62 × 26.4 倍。"}}},"q6_how_wrong":{"verdict":"最可能看錯的是利益率修復的速度：交易數若撐不到 +1%，2027 年 EPS 會落在 1.15–1.25，而 30 倍本益比沒有犯錯的空間；尾端風險是源頭在自家餐廳的食安事件。","reasoning":"三視角反證與自我攻擊都寫在反證紀錄。最強的三個反駁點：一、10 月同店轉弱、產業客流持平，第四季同店 +2% 已經是靠牛胸肉檔期與行銷撐出來的；二、管理層把第四季利益率年減的大半歸給禮券基期與行銷時點，但第二、三季利益率已經分別年減 220bp、120bp；三、共識 FY2027 EPS 1.34 隱含 24.5% 的利益率會兌現，而賣方修正方向偏下。產業態勢判為雙向拉鋸：競爭端在惡化（CAVA 客流 +5.3%，同業也打同樣的原料牌），結構端在轉好（CMG 到訪人次年增 6.0%，高於類別的 1.9%；忠誠會員占銷售 33%，創新高）；其他變數中，關稅由壓力轉為緩解（第三季已有關稅減免）。壓力測試四項過三項：沒有金融負債（過）；自由現金流／淨利 FY2024 為 0.99、FY2025 為 0.94（過）；名目同店 2% 時利益率不下滑（不過，CFO 自述要約 4%）；EPS 年增 10%、本益比壓到 20 倍時，五年後股價約 35 美元，不低於現價 30%（過）。技術面：股價低於 52、104、250 週均線，250 週均線 13 週斜率 −0.02%，長線趨勢走平、偏弱；RSI 61，26 週報酬 +3%，沒有過熱。","fact_refs":["f_ma_state","f_ma_w52","f_ma_w104","f_ma_w250","f_ma_slope_w250_pct","f_rsi14","f_week26_return_pct","f_consensus_rev_3m_fy1_pct","f_kpi3_restaurant_level_operati"],"verdict_values":{"trap":{"verdict":"🟡","label":"利益率下行中的半陷阱：便宜的是本益比的歷史位置，不是盈餘"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":1.1,"pe":29.95,"basis":"FY2026 共識 EPS 1.10（當年度）；終端倍數同樣乘在終端年當年度的 EPS 上，兩者同口徑"},"eps":{"bull":[1.37,1.6,1.84,2.09,2.36],"base":[1.29,1.45,1.62,1.79,1.96],"bear":[1.14,1.18,1.22,1.26,1.3]},"pe":{"bull":30,"base":24,"bear":19},"p":{"bull":20,"base":50,"bear":30},"yield_pct":{"dividend":0,"net_buyback":0},"second_stage":{"bull_cagr_pct":13,"base_cagr_pct":9},"max_dd":{"lo":-45,"hi":-30,"basis":"現價已比 104 週均線 42.38 美元低約 22%，回撤已經走了一段。往下看兩層：第一層，交易數轉負、FY2027 EPS 1.15、本益比壓到 20 倍，股價約 23 美元（−30%）；第二層，再疊加源頭在自家餐廳的食安事件，EPS 跌到 1.0、本益比 18 倍，股價約 18 美元（−45%）。","trigger_time":null},"basis":{"bull":"交易數 2027 年 +2–3%，名目同店 5% 以上，HEEP 全面到位、外燴推升同店，餐廳層利益率 FY2028 回到 26%；國際合作店與外燴成為第二曲線。終端 30 倍，約等於現在的前瞻倍數；同業本益比事實表未涵蓋，以自身現值 29.95 倍作為對照。","base":"交易數約 +1%，名目同店約 4%；FY2027 利益率約 24%，低於管理層的 24.5% 基準，之後每年小幅回升；每年開約 350 家。EPS 路徑已含每年約 2–3% 的股數減少，所以淨回購殖利率填 0，避免重複計算。終端 24 倍，對應第 5 年 EPS 年增約 10%。","bear":"交易數轉負，定價卡在 3%，利益率停在 22–23%，展店報酬遞減，EPS 五年只到 1.30（不高於 FY2027 共識的 1.34）。終端 19 倍取自成長熄火情境：第 3 年後成長降到 10% 時約 22 倍，降到 5% 時約 18 倍，取兩者之間偏低的位置。"},"endo_ceiling_exceeded":false},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"業界客流持平（2026 年 6 月的業者調查有 71% 預期客流持平），供給擴張快於需求；CMG 交易數只有 +0.8%，10 月又轉弱","assumption":"本次假設 2027 年交易數可以到 +1%，利益率回到約 24.5%","consequence":"最可能虧掉五成的路徑：交易數在零和市場中轉負，定價卡在 3%，利益率停在 22–23%；這時再碰上一次源頭在自家餐廳的食安事件，EPS 跌破 1.0，本益比壓到 18 倍，股價約 18 美元。這條路與唯一致命點相同。","ruling":"部分採納。食安疊加是低機率的尾部，客流轉負是中機率的主線；空頭情境機率給 30%。不再往上調，是因為交易數已連三季為正，到訪人次年增 6% 也高於類別。","watch":"季度交易數；CDC 與 FDA 的疫情公告","evidence_refs":["supply_demand_durability#0","supply_demand_durability#1","competitive_share_entrants#1"],"fact_refs":["f_kpi9_comparable_restaurant_sa","f_kpi3_restaurant_level_operati"]},{"view":"論點成功但股東經濟變差","evidence":"交易數是靠促銷與行銷買回來的：第三季行銷約占營收 3% 中段，年增約 40bp；忠誠會員兌換讓組合效果 −1.4%，CFO 預期約 −100bp 的組合拖累會持續；2026 年定價約 2%，低於 3–4% 的通膨","assumption":"交易數回升後，會以約 40% 的傳導率轉成利益率","consequence":"交易數可能達標，利益率卻不回升：行銷、會員折扣與外送占比吃掉增量毛利。翻新計畫每店 10–30 萬美元，若擴大到上千家老店，資本支出會上升，回報卻還沒證實。回購在約 30 倍本益比進行，每 1 美元只買到約 3 美分盈餘。","ruling":"採納，作為基本情境打折的依據：基本情境 2027 年 EPS 用 1.29，低於共識的 1.34","watch":"行銷費用率（管理層 2027 年的基準約 3%）、組合效果、翻新資本支出規模（預計在 2027 年第一季法說揭露）","evidence_refs":["end_markets#1"],"fact_refs":["f_kpi3_restaurant_level_operati","f_kpi5_free_cash_flow_derived"]},{"view":"價格已反映太多","evidence":"前瞻本益比 30 倍，但 FY2026 共識 EPS 1.10 低於 FY2025 的 1.14；共識要求 FY2027 成長 22%、FY2028 再成長 16%。賣方修正方向偏下：FY1 共識三個月下修 2.65%，營收修正 8 家上修對 24 家下修，部分券商的第四季同店預估明顯低於共識","assumption":"共識隱含管理層的 24.5% 利益率基準會兌現","consequence":"若 2027 年利益率只到 24%、EPS 落在 1.25–1.29，市場可能把本益比從 30 倍壓到 25 倍，股價落在 31–32 美元，一年報酬接近零","ruling":"採納。這是本次維持觀望的主因；重啟條件改看利益率實績，不看價格","watch":"Koyfin 共識 FY2027 EPS 的月度變化；第四季財報的 2027 年指引","evidence_refs":["capital_markets_pricing#3","capital_markets_pricing#5"],"fact_refs":["f_fwd_pe_latest","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_rev_3m_fy1_pct"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ❌ → 本次 ❌","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=❌","side_b":"本次 ma=❌","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 34.24 → 本次 32.94（-3.8%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=34.24","side_b":"本次 price_at_dd=32.94","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 34.24 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 34.24 美元：Bull 價 71.5、Bear 價 25.5，五年期望值 +43.2%，基準年化 10.3%，不對稱比 2.6","side_b":"本次情境、股價仍用 34.24 美元：Bull 價 70.8、Bear 價 24.7，五年期望值 +31.7%，基準年化 6.6%，不對稱比 2.55","ruling":"先換情境、股價不動：五年期望值少 11.5 個百分點，基準年化少 3.7 個百分點。不對稱比由 2.6 變為 2.55。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 34.24 美元：五年期望值 +31.7%，基準年化 6.6%，不對稱比 2.55","side_b":"本次情境、股價 32.94 美元：五年期望值 +36.9%，基準年化 7.4%，不對稱比 3.06","ruling":"再換股價、情境不動：起點價下跌 3.8%，五年期望值多 5.2 個百分點，基準年化多 0.8 個百分點，不對稱比由 2.55 升到 3.06。合計五年期望值比前份少 6.3 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"管理層前後說法對帳（2026-07-29 對 2026-10-28）","cause":null,"prior_field":null,"side_a":"2026-07-29 CFO：第三季同店約 +1%（已假設約 200bp 的逆風延續）；銷貨成本率略低於 30%，人力成本率 25% 中段，其他營運成本 15% 中段，非 GAAP 一般管理費用約 1.8 億；第四季起定價與通膨對齊。CEO：HEEP 全系統 2027 年內完工","side_b":"2026-10-28 實績與說法：同店 +2.1%、銷貨成本率 29.5%，優於指引；人力 25.7%、其他營運成本 16.0%、非 GAAP 一般管理費用 1.84 億，差於指引（行銷加碼、保險一次性費用）；第四季定價約 3%、通膨約 3%，對齊的承諾兌現。CEO 把 HEEP 改說成 2027 年底前接近完成","ruling":"以一致為主，可以調和：營收端說到做到，成本端拿行銷換交易數，屬程度差異；HEEP 時程小幅延後，同店效益只是遞延，方向沒有改變","evidence_level":"公司法說與新聞稿","settle_metric":"2027 年第一季法說的 HEEP 安裝數與 2027 年同店指引","if_then":["若 2027 年第一季法說再延後 HEEP 時程，或 2027 年同店指引低於 3%：基本情境的 2027 年同店下修 1 個點，EPS 下修到 1.24","反向：若 HEEP 在 2027 年上半年完成，且同店指引 ≥ 4%：多頭機率提高到 25%"],"evidence_refs":[]},{"axis":"第四季利益率年減 150bp 的歸因","cause":null,"prior_field":null,"side_a":"2026-10-28 CFO：約一半來自去年同期 70bp 的禮券收入，約 30bp 是行銷時點移到牛胸肉檔期，其餘才是銷售量","side_b":"第二季利益率已年減 220bp，第三季年減 120bp，非一次性因素在前兩季就已存在；2026 年定價落後通膨約 100bp，也是 CFO 自己說的","ruling":"不採信也不否定，標為未證實。預先登記：2027 年第一季（已沒有禮券基期）餐廳層利益率若仍年減 100bp 以上，就視為一次性歸因不成立","evidence_level":"管理層說法，尚未經下一季驗證","settle_metric":"2027 年第一季餐廳層利益率年增減","if_then":["若 2027 年第一季年減 ≥ 100bp：一次性歸因不成立，H2 改判削弱，空頭情境機率提高到 35%","反向：若 2027 年第一季年增轉正：歸因成立，保留重啟資格"],"evidence_refs":[]},{"axis":"市占：輸給 CAVA，還是贏過產業","cause":null,"prior_field":null,"side_a":"CAVA 2026 年第二季同店 +9%、客流 +5.3%；CMG 同期同店 +2.2%、交易數 +1%","side_b":"Placer.ai：CMG 到訪人次第二、三季分別年增 5.8%、6.0%，高於類別的 2.2%、1.9%；CEO 稱 2026 年每個月都在拿市占（2026-07-29）","ruling":"可以調和，因為分母不同。CMG 在整體快休閒仍在拿份額（到訪人次含新店），但在增量最快的新品類輸給 CAVA。以同店交易數 +0.8% 來看，既有店的份額只是持平略增，撐不起護城河擴大的判斷","evidence_level":"第三方客流資料加媒體轉述","settle_metric":"CMG 交易數成長與 CAVA 客流成長的差距","if_then":["若差距連 2 季擴大到 6 個百分點以上：護城河趨勢改判為向下，並重跑研究","反向：若 CMG 交易數 ≥ +2% 且差距收窄到 3 個百分點以內：保留持平判斷，並把多頭機率提高到 25%"],"evidence_refs":["competitive_share_entrants#1"]},{"axis":"低收入客群：流失還是回流","cause":null,"prior_field":null,"side_a":"前份：年收入低於 4 萬美元的家戶，在三美元價格帶戰下外食頻次與單次消費雙雙下降，CMG 被夾在價值戰與高成長品類之間","side_b":"2026-10-28 CEO：第三季低收入客群首次跑贏高收入客群，而且在促銷最少的 9 月表現最強","ruling":"方向相反，不可調和；裁決採用新證據。公司的錢包份額資料是直接觀察，前份是產業推論；但新證據只有一季，所以低收入流失的分支保留在空頭情境，門檻不刪","evidence_level":"公司自述（不可調和，已裁決）","settle_metric":"2027 年第一季法說是否延續低收入客群跑贏","if_then":["若 2027 年第一季管理層改稱低收入客群轉弱，且交易數 < 0：恢復前份判斷，空頭情境機率提高到 35%","反向：若連兩季維持跑贏，且交易數 ≥ +1%：低收入流失的分支退休"],"evidence_refs":[]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"淨現金、沒有金融負債；公司自認股價被低估，以 34.32 美元均價買回 14 億美元，現價 32.94 美元還低於回購均價。本益比在近 4 個年度端點中最低；交易數連三季為正，9 月同店 +3.8%，預期年底單月可到 3–4%。HEEP 只有約一半門市滿 2–3 個月，同店效益還在累積。若 2027 年利益率回到 24.5%，以共識 1.34 美元計，FY2027 本益比只有 24.6 倍","side_b":"這些都是條件句：利益率回升要靠名目同店約 4%，但 10 月才剛轉弱，產業客流持平；FY2026 EPS 年減，30 倍本益比沒有給錯的空間；基本情境的五年年化報酬只有個位數","ruling":"不買。論證能否成立，關鍵在 2027 年上半年利益率能否年增轉正；第一個證據 2027 年 4 月就會出現，等兩季的機會成本，小於提前押錯的下行","evidence_level":"公司法說與事實表","settle_metric":"2027 年第一、二季餐廳層利益率年增減","if_then":["若 2027 年第一、二季餐廳層利益率都年增為正：重跑研究，可考慮以小倉起步","若股價先漲到 40 美元以上，而利益率證據還沒出現：不追"],"evidence_refs":[]},{"axis":"陷阱定性由 🔴 降為 🟡","cause":"新證據","prior_field":["trap"],"side_a":"前份：陷阱定性 🔴（衰退訊號亮燈多，2025 年同店 −1.7%）","side_b":"本次：衰退訊號亮 2 項（利益率連季年減；過去三年 EPS 成長高於營收成長逾 5 個百分點）。提價後客流下滑這一項不再亮：第三季定價 2.7%，交易數仍 +0.8%，2026 年三季交易數皆為正","ruling":"降一級為 🟡。裁決與角色若因此改列，原因相同","evidence_level":"公司季報","settle_metric":"2027 年上半年交易數","if_then":["若 2027 年上半年交易數連 2 季為負：恢復 🔴"],"evidence_refs":[]},{"axis":"重新檢視後維持不變的欄位","cause":"新證據","prior_field":["signal","val","moat_trend","runway_post_y5","archetype","cycle_position"],"side_a":"前份：綜合評等 C、估值偏貴 🟠、護城河趨勢持平、第 5 年後展店期中等、品質複利成長型、沒有循環位置","side_b":"本次維持：PEG 約 2.8 仍偏貴，但本益比在自身低檔；執行力改善抵銷定價力轉弱；北美展店在第 5 年後仍未結束，但第二曲線未成形；不是循環股","ruling":"新證據不足以改變這六項判斷","evidence_level":"事實表與法說","settle_metric":"2027 年第一季財報","if_then":[],"evidence_refs":[]},{"axis":"情境機率與最大回撤區間","cause":"方法變動","prior_field":["p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份：多頭 20%、空頭 33%，最大回撤 −48%（單點）","side_b":"本次：多頭 20%、基本 50%、空頭 30%；最大回撤改填區間 −45% 至 −30%","ruling":"方法變動：情境終端年改為 FY2031，空頭的終端 EPS 不得高於 FY2027 共識；最大回撤改以兩層事件推導區間。空頭機率下調 3 個點，是因為交易數已連三季為正","evidence_level":"方法調整加公司季報","settle_metric":"2027 年上半年交易數與利益率","if_then":[],"evidence_refs":[]},{"axis":"重啟條件修正（建倉前提）","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"單一條件：餐廳層營業利潤率連 2 季 YoY 轉正（等價於絕對值連 2 季 ≥ 26.0%）——此一條件同時解除衰退燈、陷阱定性 🔴 與 PEG > 2.0 三個限制。價格回落至 $29.4 只降低進場成本、不解除限制。","side_b":"連 2 季餐廳層利益率年增轉正（最早看 2027 年第一、二季財報），不換算成絕對值，價格不作為重啟條件","ruling":"門檻改變。前份把年增轉正等同於絕對值 26%，但年增的比較基期每季不同：2026 年第二季 25.2%、第三季 24.5%、第四季約 23.4%，第一季約 23.6%（由前份上半年 24.4% 與第二季 25.2% 推回）。2027 年上半年要年增轉正，只需高於約 23.6% 與 25.2%。本次只保留年增轉正，刪除絕對值的換算；重啟後須重跑研究，才可建倉","evidence_level":"方法修正","settle_metric":"2027 年第一、二季餐廳層利益率","if_then":["條件成立：重跑研究，通過才以小倉建倉","條件未成立而股價先跌：不提前建倉"],"evidence_refs":[]},{"axis":"Single Thing 設定","cause":"方法變動","prior_field":null,"side_a":"（前份為空白，未設定唯一致命點）","side_b":"CMG 自家餐廳被衛生機關認定為多州食源性疫情的源頭（不是供應商層級，也不是產業性事件）","ruling":"Single Thing 由空白改為食安源頭事件。2026 年已發生兩次產業性食安干擾，而這是單一事件裡對 EPS 與本益比衝擊最大的一項；若發生，已持有者立即減碼一半","evidence_level":"8-K 與媒體報導","settle_metric":"CDC 與 FDA 疫情公告","if_then":["若發生：減碼一半，暫停所有進場條件 6 個月"],"evidence_refs":["regulatory_antitrust#0"]},{"axis":"停損指標新設（清倉與減碼門檻）","cause":"方法變動","prior_field":null,"side_a":"（前份未設停損指標，為空白）","side_b":"交易數連 2 季年減；2027 年任兩季餐廳層利益率年減 ≥ 100bp；源頭在自家餐廳的食安事件；FY2027 共識 EPS 跌破 1.20 美元","ruling":"新設門檻，前份為空白。觸發任兩項時，已持有者減碼一半；三項同時觸發則清倉","evidence_level":"方法補齊","settle_metric":"季報與共識快照","if_then":["觸發兩項：減碼一半","觸發三項：清倉"],"evidence_refs":[]},{"axis":"利益率回升門檻改變（減碼依據）","cause":"新證據","prior_field":null,"side_a":"前份 H2：FY2028 前回到 26% 以上","side_b":"本次 H2：FY2027 約 24.5%，FY2030 前回到 26% 以上","ruling":"CFO 在 2026-10-28 給出 2027 年基準約 24.5%（23.5% 加回 100bp 的定價錯位），並說名目同店要約 4% 才能穩住利益率，因此 26% 的時點延後兩年。若 TTM 利益率連 2 季低於 23.3%，則減碼","evidence_level":"2026-10-28 CFO 法說","settle_metric":"TTM 餐廳層利益率","if_then":["TTM 連 2 季低於 23.3%：已持有者減碼一半"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"交易數驗證：2027 年第一季財報的交易數年增 ≥ +1%","type":"假設驗證","maps_to":"H1","metric":"季度交易數年增率","threshold":"≥ +1.0%（反向：連 2 季 < 0%）","action":"達標則保留重啟資格；連 2 季為負則空頭情境機率提高到 40%","source_freq":"季報（每季）","date":"2027-04","evidence_refs":[]},{"n":2,"text":"利益率驗證：2027 年第一、二季餐廳層利益率都年增為正","type":"假設驗證","maps_to":"H2","metric":"餐廳層利益率年增減","threshold":"兩季皆 > 0bp","action":"成立就重跑研究","source_freq":"季報（每季）","date":"2027-07","evidence_refs":[]},{"n":3,"text":"成本橋：管理層把 2027 年通膨指引上修到中個位數以上，而定價維持在 3% 以下","type":"風險","maps_to":"R1","metric":"季度通膨減定價貢獻","threshold":"差距 ≥ 100bp，連 2 季","action":"2027 年基本情境 EPS 下修到 1.20，多頭機率降到 15%","source_freq":"法說（每季）","date":"2027-02","evidence_refs":["reg_tariff_export#1","geo_supply_chain#2","end_markets#1"]},{"n":4,"text":"客流零和：業界客流持平，而對手搶走增量","type":"風險","maps_to":"R2","metric":"CMG 交易數成長減 CAVA 客流成長","threshold":"差距連 2 季擴大到 −6 個百分點以上","action":"護城河趨勢改判為向下，並重跑研究","source_freq":"季報（每季）","date":"2027-03","evidence_refs":["competitive_share_entrants#1","supply_demand_durability#1"]},{"n":5,"text":"唯一致命點：衛生機關把多州疫情源頭指向 CMG 餐廳","type":"Single Thing","maps_to":"R3","metric":"衛生機關認定的疫情源頭","threshold":"源頭指向 CMG 自家餐廳（不是供應商召回）","action":"已持有者減碼一半；未持有者暫停進場 6 個月","source_freq":"即時（CDC、FDA、公司 8-K）","date":null,"evidence_refs":["regulatory_antitrust#0","major_events#1","product_recall_warning#0"]},{"n":6,"text":"Stradford 股東集體訴訟：法院就第二修正訴狀的駁回聲請作出裁定","type":"風險","maps_to":null,"metric":"訴訟程序里程碑","threshold":"駁回聲請遭否決，進入集體認證","action":"列入空頭情境並估算求償金額（金額事實表未涵蓋）；若出現不利和解，且金額超過一季自由現金流（約 3.5 億美元），則下修持有上限","source_freq":"10-Q 法律程序附註（每季）","date":null,"evidence_refs":["major_events#2","lawsuit_class_action#0"]},{"n":7,"text":"重啟條件：連 2 季餐廳層利益率年增轉正","type":"估值rearm","maps_to":"H2","metric":"餐廳層利益率年增減","threshold":"2027 年第一、二季皆 > 0bp","action":"重跑研究，通過後以小倉起步","source_freq":"季報（每季）","date":"2027-07","evidence_refs":[]},{"n":8,"text":"已持有者：2027 年上半年交易數連 2 季為負，且利益率年減 ≥ 100bp","type":"減碼","maps_to":"R2","metric":"交易數與餐廳層利益率","threshold":"兩項同時成立","action":"減碼一半","source_freq":"季報（每季）","date":"2027-07","evidence_refs":["supply_demand_durability#0"]},{"n":9,"text":"複審：第四季財報與 2027 年全年指引","type":"複審日期","maps_to":null,"metric":"2027 年同店與利益率指引","threshold":"同店指引 < 3%，或利益率指引低於 24%","action":"重跑情境樹","source_freq":"年度指引","date":"2027-02","evidence_refs":[]}],"kill_metrics":[{"metric":"季度交易數年增率","bear_threshold":"連 2 季 < 0%","window":"2027 年第一季至第四季","source":"公司季報新聞稿","last_status":"ok"},{"metric":"餐廳層利益率年增減","bear_threshold":"2027 年任兩季年減 ≥ 100bp","window":"2027 年第一季至第四季","source":"季報新聞稿非 GAAP 調節表","last_status":"warning"},{"metric":"源頭在自家餐廳的食源性疫情","bear_threshold":"CDC 或 FDA 公告的疫情源頭指向 CMG 餐廳","window":"滾動 24 個月","source":"CDC、FDA 公告與公司 8-K","last_status":"ok"},{"metric":"FY2027 共識 EPS","bear_threshold":"跌破 1.20 美元","window":"至 2027 年 7 月","source":"Koyfin 共識快照","last_status":"ok"}],"action_conditions":{"rearm_trigger":"連 2 季餐廳層利益率年增轉正（最早看 2027 年第一、二季財報），不換算成絕對值，價格不作為重啟條件","exec_line":"重啟條件成立後，先重跑完整研究，通過才以小倉起步。條件成立前，股價先漲不追；股價先跌但交易數仍為正，也不提前建倉，只更新情境樹。"}},"decision_inputs":{"signal":"C","ma":"❌","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"賣方平均目標價約 42.9 美元（2026-08），評等偏買進，隱含 FY2027 EPS 1.34 與管理層 24.5% 的利益率基準都會兌現。但 CFO 自己說，在 3% 通膨下名目同店要約 4% 才能穩住利益率；第三季只有 2.1%，10 月又轉弱。共識沒有替這個前提打折；而股價已經跌過一段，本身並不構成安全邊際。","momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":null,"wait_for_price_condition":null,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null},"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"6","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='C'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":true,"basis":"ma='❌'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":true,"basis":"signal='C'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=賣方平均目標價約 42.9 美元（2026-08），評等偏買進，隱含 FY2027 EPS 1.34 與管理層 24.5% 的利益率基準都會兌現。但 CFO 自己說，在 3% 通膨下名目同店要約 4% 才能穩住利益率；第三季只有 2.1%，10 月又轉弱。共識沒有替這個前提打折；而股價已經跌過一段，本身並不構成安全邊際。"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='C', runway='🟡', val='🟠', moat_trend='→', week26=3.0, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position=None, moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"6/7/7a-verdict","condition":"Soft Veto 生效 → 觀望（max-severity wins；8a/8b 未能繞過）","hit":true,"basis":"soft_veto_rows=['6']"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":["row4：週線❌，進場節奏強制分批（starter 1/3＋趨勢確認後加碼），頁首掛「⚠️ 週線趨勢未確認，逢回分批勿接刀」"],"holding_cap":null,"requires_critic":[]},"thesis":{"H":[{"id":"H1","text":"交易數維持正成長，並在 2027 年達到 +1% 以上；名目同店回到約 4%（CFO：3% 通膨下穩住利益率所需）","2y":"2027 年全年交易數 ≥ +1%，名目同店 ≥ 4%","5y":null,"10y":null,"threshold":"2027 年全年交易數 ≥ +1.0%","source":"季報新聞稿與法說（同店、客單、交易數、定價貢獻）","drift_rule":"單季交易數連 2 季低於 +0.5% 為削弱；連 3 季為負為反轉"},{"id":"H2","text":"餐廳層利益率在 FY2026 約 23.5% 見底，FY2027 回到約 24.5%（CFO 給的基準），FY2030 前回到 26% 以上","2y":"FY2027 餐廳層利益率 ≥ 24.5%","5y":"FY2030 ≥ 26%","10y":null,"threshold":"FY2027 全年餐廳層利益率 ≥ 24.5%","source":"季報新聞稿非 GAAP 調節表、CFO 法說的成本指引","drift_rule":"TTM 餐廳層利益率連 2 季低於 23.3%（偏離門檻 5%）為削弱；連 3 季低於 22.1%（偏離 10%）為反轉"},{"id":"H3","text":"北美每年 340–360 家新店的報酬不衰退，且外燴與國際合作店形成第二曲線，讓展店期延伸到第 5 年之後","2y":null,"5y":"新店第二年現金回報 ≥ 50%，外燴與家庭餐占營收 ≥ 5%，北美以外每年開店 ≥ 25 家","10y":"北美店數朝至少 7,000 家推進，國際合作店成為穩定的新增來源","threshold":"新店第二年現金回報跌破 50%，或新店生產力跌破 75%","source":"法說（CFO 的新店經濟更新）、年報店數","drift_rule":"以每次揭露計，現金回報連 4 次低於 57% 為削弱，連 6 次低於 54% 為反轉；外燴占比到 2028 年仍低於 4%，視為第二曲線未成形"}],"R":[{"id":"R1","text":"成本橋拉長：牛肉、運費與關稅讓通膨停在 3% 以上，而菜單價格因客群敏感只能跟到 2–3%，餐廳層利益率卡在 23–24%，到不了管理層講的 24.5% 基準。前份提出的牛價上行在本包沒有更新數據；第三季食材成本率反而年減約 50bp","h_ref":"H2","clock":"🔥","threshold":"2027 年上半年任一季餐廳層利益率年減 ≥ 50bp，且管理層把當季通膨上修到 4% 以上","evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","geo_supply_chain#0","geo_supply_chain#2","end_markets#1"]},{"id":"R2","text":"零和客流：產業客流持平、供給擴張快於需求，CAVA 客流成長遠快於 CMG；同業也打高品質原料的牌，CMG 只能靠促銷與行銷買交易數","h_ref":"H1","clock":"⚡","threshold":"交易數連 2 季年減","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1","supply_demand_durability#0","supply_demand_durability#1"]},{"id":"R3","text":"食安：2026 年 7 月墨西哥辣椒沙門氏菌（供應商層級召回）與同期的產業性 cyclospora 事件，讓 7 月中到 8 月底的同店少了約 200bp。品牌以新鮮食材做差異化，對食安事件的敏感度比同業高","h_ref":"H1","clock":"⚡","threshold":"衛生機關點名 CMG 餐廳為疫情源頭，或單月同店較事件前下滑 ≥ 500bp","evidence_refs":["regulatory_antitrust#0","major_events#1","product_recall_warning#0"]},{"id":"R4","text":"人力成本：第三季人力成本率 25.7%，年增約 50bp，工資通膨在低個位數；前份提出的移民執法與加州加薪裁量權，本包沒有新資料，門檻保留","h_ref":"H2","clock":"🐢","threshold":"人力成本率連 2 季年增 ≥ 100bp","evidence_refs":[]}],"single_thing":{"description":"CMG 自家餐廳被衛生機關認定為多州食源性疫情的源頭（不是供應商層級，也不是產業性事件）","why_fatal":"品牌的差異化建立在新鮮食材上，30 倍本益比又押在交易數回升。源頭在自家餐廳的疫情，會讓交易數轉為兩位數的負成長，利益率依約 40% 的傳導率反向下滑，EPS 與本益比同時下修，是所有變數裡對股價影響最大的一項","if_happens":"已持有者立即減碼一半，等衛生機關結案、單月同店回到事件前水準，再重跑研究；未持有者暫停所有進場條件 6 個月","how_monitor":"CDC 與 FDA 疫情公告、州衛生局新聞稿、公司 8-K；第三方到訪人次資料作輔助（更新頻率事實表未涵蓋）","probability":"12–24 個月約 8%（主觀估計）。2026 年 7 月的墨西哥辣椒沙門氏菌事件只到供應商層級召回，8 月底同店就回到事件前水準，代表供應鏈追溯有效；但 2026 年內已經出現兩次產業性食安干擾"}},"appendix_a":{"growth_durability":6,"quality_score":7,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":24.58,"peg_fy2":2.28,"stress":{"pass":3,"total":4}},"eps_meta":{"base_eps_path":{"FY2025A":1.14,"FY2026E":1.1,"FY2027E":1.34,"FY2028E":1.55},"fy_end_month":12,"eps_basis":"FY2026E 至 FY2028E 為 Koyfin 共識（2026-10-31 快照，分析師家數未揭露；Chartmill 同期 FY2026 為 38 家）；FY2025A 用年報稀釋 EPS 1.14（GAAP），與調整後口徑的差異事實表未涵蓋。三年共識年增約 10.8%"},"catalysts":[{"date":"2026-11","date_precision":"month","type":"product","event":"煙燻牛胸肉限時回歸","impact":"中","watch":"第四季同店能否達到約 +2%，年底單月能否到 3–4%"},{"date":"2027-02","date_precision":"month","type":"guidance","event":"第四季財報與 2027 年同店、利益率指引","impact":"高","watch":"同店指引是否 ≥ 3%，利益率是否確認約 24.5%"},{"date":"2027-03","date_precision":"quarter","type":"product","event":"外燴全國推出","impact":"低","watch":"團體餐占營收能否由約 3% 每年增加 1–2 個點"},{"date":"2027-03","date_precision":"quarter","type":"other","event":"投資人活動（2026-07-29 CEO 稱正在規劃，時點約在明年初）","impact":"中","watch":"長期店數、利益率與國際目標是否上修"},{"date":"2027-04","date_precision":"month","type":"guidance","event":"2027 年第一季財報","impact":"高","watch":"交易數是否 ≥ +1%，餐廳層利益率是否年增轉正"}]}
```

---

## ⑤ 覆蓋面（程式判定，你回的 ⑤ 燈號會被覆寫）

燈號 🟢：核心軸皆有證據或不適用，非核心軸也沒有空軸。核心軸由採證 agent 自報不適用（燈號不變，請看 note 理由）：customer_concentration_credit。

⑤ 的 reason 只需評論：空軸的查詢詞是否切題、判斷有沒有交代缺口對結論的影響。

---

## 尾段：回覆格式

只回一個 JSON 陣列，①–⑧ 每條一個元素，八個全出，不得跳號、不得多列，陣列外不得有任何文字（不加前言、不加 markdown 圍欄、不加附註）：

```json
[{"item": "①", "light": "🔴|🟡|🟢", "judgment_path": "$.路徑", "reason": "一句話"}]
```
