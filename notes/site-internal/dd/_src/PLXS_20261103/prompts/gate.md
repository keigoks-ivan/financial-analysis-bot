你是 DD 管線 v20 的判斷層閘（gate），標的 PLXS（20261103）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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
- `f_kpi0_revenue_gaap`（q1_business）｜Revenue (GAAP)＝1426.6 USD M；YoY +34.8%（Q4 FY25 1,058.4）、QoQ +9.3%｜期間與口徑：Q4 FY2026（季末 2026-10-03，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q4 FY26 earnings release（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000785786/000078578626000062/plxsf26q4earningsrelease-e.htm（numbers.latest_quarter_kpis.items[0]，as_of Q4 FY2026（季末 2026-10-03，公告於 2026-10-28））
  - 註記：查無共識數字
- `f_kpi1_non_gaap_operating_incom`（q1_business）｜Non-GAAP operating income / margin＝95.8 USD M；margin 6.7%｜期間與口徑：Q4 FY2026（季末 2026-10-03，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q4 FY26 earnings release（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000785786/000078578626000062/plxsf26q4earningsrelease-e.htm（numbers.latest_quarter_kpis.items[1]，as_of Q4 FY2026（季末 2026-10-03，公告於 2026-10-28））
  - 註記：查無共識數字
- `f_kpi2_gaap_operating_income_ma`（q1_business）｜GAAP operating income / margin＝86.3 USD M；margin 6.0%｜期間與口徑：Q4 FY2026（季末 2026-10-03，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q4 FY26 earnings release（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000785786/000078578626000062/plxsf26q4earningsrelease-e.htm（numbers.latest_quarter_kpis.items[2]，as_of Q4 FY2026（季末 2026-10-03，公告於 2026-10-28））
  - 註記：查無共識數字
- `f_kpi5_guidance_q1_fy2027_2027_`（q1_business）｜Guidance Q1 FY2027（季末 2027-01-02）＝營收 1,410–1,460 USD M；GAAP op margin 5.5–5.9%、non-GAAP 6.0–6.4%；GAAP EPS 2.16–2.32、non-GAAP EPS 2.46–2.62；FY27 營收成長中高個位至高十位數（mid-to-upper teens）｜期間與口徑：Q4 FY2026（季末 2026-10-03，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司 Q4 FY26 earnings release（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000785786/000078578626000062/plxsf26q4earningsrelease-e.htm（numbers.latest_quarter_kpis.items[5]，as_of Q4 FY2026（季末 2026-10-03，公告於 2026-10-28））
  - 註記：查無共識數字
- `f_kpi6_inventory_days`（q1_business）｜Inventory days＝119 天；cash cycle 62 天｜期間與口徑：Q4 FY2026（季末 2026-10-03，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q4 FY26 earnings release（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000785786/000078578626000062/plxsf26q4earningsrelease-e.htm（numbers.latest_quarter_kpis.items[6]，as_of Q4 FY2026（季末 2026-10-03，公告於 2026-10-28））
  - 註記：查無共識數字
- `f_peer_plxs_gross_margin_pct`（q2_moat）｜PLXS 毛利率＝10.08 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.PLXS.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_earnings_recency`（q1_business）｜最近一次財報日＝2026-10-28 date｜期間與口徑：2026-10-28／距今 4 個交易日｜kind：realized
  - 來源：—（numbers.earnings_recency，as_of 2026-10-28）
- `f_peer_plxs_operating_margin_pct`（q2_moat）｜PLXS 營業利益率＝5.02 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.PLXS.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_plxs_fcf_margin_pct`（q2_moat）｜PLXS FCF 利潤率＝-1.0 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.PLXS.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_sanm_gross_margin_pct`（q2_moat）｜SANM 毛利率＝9.01 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.SANM.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_sanm_operating_margin_pct`（q2_moat）｜SANM 營業利益率＝5.49 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.SANM.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_sanm_fcf_margin_pct`（q2_moat）｜SANM FCF 利潤率＝4.66 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.SANM.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_bhe_gross_margin_pct`（q2_moat）｜BHE 毛利率＝10.38 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.BHE.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_bhe_operating_margin_pct`（q2_moat）｜BHE 營業利益率＝4.25 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.BHE.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_bhe_fcf_margin_pct`（q2_moat）｜BHE FCF 利潤率＝4.61 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.BHE.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_flex_gross_margin_pct`（q2_moat）｜FLEX 毛利率＝9.5 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.FLEX.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_flex_operating_margin_pct`（q2_moat）｜FLEX 營業利益率＝5.44 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.FLEX.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_flex_fcf_margin_pct`（q2_moat）｜FLEX FCF 利潤率＝3.32 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.FLEX.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_jbl_gross_margin_pct`（q2_moat）｜JBL 毛利率＝9.23 %｜期間與口徑：TTM ending 2026-08-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.JBL.gross_margin_pct，as_of TTM ending 2026-08-31（4季加總））
- `f_peer_jbl_operating_margin_pct`（q2_moat）｜JBL 營業利益率＝5.11 %｜期間與口徑：TTM ending 2026-08-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.JBL.operating_margin_pct，as_of TTM ending 2026-08-31（4季加總））
- `f_peer_jbl_fcf_margin_pct`（q2_moat）｜JBL FCF 利潤率＝3.82 %｜期間與口徑：TTM ending 2026-08-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.JBL.fcf_margin_pct，as_of TTM ending 2026-08-31（4季加總））
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝10.33 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-10-31）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝11.79 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-10-31）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝5872.32 USD m｜期間與口徑：2026-11-03／yfinance revenue_estimate 0y 平均（5 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝6423.12 USD m｜期間與口徑：2026-11-03／yfinance revenue_estimate +1y 平均（5 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi3_free_cash_flow`（q1_business）｜Free cash flow＝6.4 USD M（OCF 29.2 − capex 22.8）；FY26 全年 −28.9｜期間與口徑：Q4 FY2026（季末 2026-10-03，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q4 FY26 earnings release（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000785786/000078578626000062/plxsf26q4earningsrelease-e.htm（numbers.latest_quarter_kpis.items[3]，as_of Q4 FY2026（季末 2026-10-03，公告於 2026-10-28））
  - 註記：查無共識數字
- `f_kpi4_sbc_gaap`（q4_capital）｜SBC（占 GAAP 營業利益／占營收）＝9.6 USD M；占 GAAP 營業利益 11.1%、占營收 0.67%（含 1.1 高階主管退休加速認列）｜期間與口徑：Q4 FY2026（季末 2026-10-03，公告於 2026-10-28）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q4 FY26 earnings release（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000785786/000078578626000062/plxsf26q4earningsrelease-e.htm（numbers.latest_quarter_kpis.items[4]，as_of Q4 FY2026（季末 2026-10-03，公告於 2026-10-28））
  - 註記：查無共識數字
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝10.81 USD m｜期間與口徑：2026-11-03／yfinance 最新一季：總債務 291.99、現金 281.18（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝26.65 m shares｜期間與口徑：2026-11-03／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝214.32 USD｜期間與口徑：2026-11-02（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-11-02（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝20.75 x｜期間與口徑：2026-10-31／分母＝FY1 EPS 10.33，分子＝快照價 214.32｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-10-31）
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝28.92 x｜期間與口徑：2026-11-02（RTH 收盤，UTC）／3 個年度端點內的分位＝66.8｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-11-02（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝66.8 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／**非五年分位**：只用 3 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝1.15 x｜期間與口徑：2026-11-02（RTH 收盤，UTC）／3 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝100.0 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／**非五年分位**：只用 3 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝1.15 x｜期間與口徑：2026-11-02（RTH 收盤，UTC）／3 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝100.0 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／**非五年分位**：只用 3 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ev_s_fwd`（q5_valuation）｜EV/S（EV ÷ FY1 共識營收）＝0.97 x｜期間與口徑：2026-11-03／f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）｜kind：estimate
  - 來源：—（numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_consensus_rev_fy1_pct`（q5_valuation）｜FY1 共識修正＝2.08 %｜期間與口徑：2026-10-31／兩份 Koyfin 快照之間的 EPS 修正幅度（10.12 → 10.33）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.fy1.revision_pct，as_of 2026-10-31）
- `f_consensus_rev_fy2_pct`（q5_valuation）｜FY2 共識修正＝3.42 %｜期間與口徑：2026-10-31／兩份 Koyfin 快照之間的 EPS 修正幅度（11.4 → 11.79）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.fy2.revision_pct，as_of 2026-10-31）
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝25.52 %｜期間與口徑：2026-07-30 → 2026-10-31／FY1 共識 EPS 8.23 → 10.33（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-10-31）
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝-18.37 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-11-02（RTH 收盤，UTC））
- `f_rsi14`（q5_valuation）｜RSI(14)＝37.11｜期間與口徑：2026-11-02（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ma_w52`（q5_valuation）｜52 週均線＝223.15 USD｜期間與口徑：2026-11-03／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）
- `f_ma_w104`（q5_valuation）｜104 週均線＝181.11 USD｜期間與口徑：2026-11-03／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）
- `f_ma_w250`（q5_valuation）｜250 週均線＝133.19 USD｜期間與口徑：2026-11-03／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）
- `f_ma_state`（q5_valuation）｜週線均線六態（decision_inputs.ma 必須等於此值）＝🟡｜期間與口徑：2026-11-03／timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）
  - 原文：「price 211.96 / W52 223.15 / W104 181.11 / W250 133.19 / W250 13週斜率 1.54%」

### findings_digest 中方向為負或來源衝突的條目（12 條）
- `competitive_share_entrants#1`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K 風險因素：製造流程缺乏重大專利保護，資源更大的公司可能進入市場；客戶亦可能自製；競爭加劇可能導致降價或失去客戶／份額。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2025-11-14）｜affects：moat_trend、decision_inputs.bear、thesis.R
- `customer_second_source#1`（customer_second_source｜方向 -｜狀態 ok）：Q2 FY2026 前十大客戶占營收54%（FY2025為49%），客戶集中度上升
  - 來源：SEC 8-K Q2 FY2026 earnings exhibit（as_of 2026-04-29）｜affects：thesis.R、decision_inputs.bear
- `customer_concentration_credit#0`（customer_concentration_credit｜方向 -｜狀態 ok）：FY2025 10-K：無單一客戶占營收逾10%（FY2025、FY2024皆然）；前10大客戶占營收49.1%（FY2024為47.8%）。
  - 來源：SEC EDGAR 10-K FY2025 Item 7 MD&A（as_of 2025-11-14）｜affects：thesis.R、decision_inputs.bear
- `customer_concentration_credit#2`（customer_concentration_credit｜方向 -｜狀態 ok）：FY2026 Q2財報稿稱前10大客戶占該季營收54%（搜尋摘要轉述）。
  - 來源：Plexus 8-K Q2 FY2026 earnings release（as_of 2026-04-22）｜affects：thesis.R、decision_inputs.bear
- `customer_concentration_credit#3`（customer_concentration_credit｜方向 -｜狀態 ok）：FY2026 Q4財報稿：FY2026前10大客戶占營收54%，較FY2025上升。
  - 來源：Plexus 8-K Q4 FY2026 earnings release（as_of 2026-10-28）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：10-K FY2025 揭露：墨西哥廠在 IMMEX 保稅計畫下營運（降低關稅），計畫變動或不合規會造成不利影響；關稅、出口管制與貿易保護措施可能影響成本、零組件供應與需求。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2025-11-14）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#1`（reg_tariff_export｜方向 -｜狀態 ok）：10-K FY2025 揭露：出口規範與制裁可能限制在中國使用或生產特定技術／產品，或銷售最終運往中國的零組件；貿易法規涉及先進半導體，可能限制對中國客戶出貨、支援中國營運專案與採購零組件。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2025-11-14）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#2`（reg_tariff_export｜方向 -｜狀態 ok）：10-K FY2025 揭露：客戶合約多允許季度性價格調整，但公司過去及未來可能承擔調價之間的零組件漲價風險，回收調價對營業利益率有稀釋效果。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2025-11-14）｜affects：thesis.R、valuation
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：FY2025 10-K：美國以外營運占淨銷售與營業利益多數，且特別集中在馬來西亞；墨西哥廠在 IMMEX 計畫下營運，貿易政策／關稅變動為風險。
  - 來源：Plexus Form 10-K FY2025（as_of 2025-11-01）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：10-K 提及中美關稅與出口管制可能影響中國採購零組件的成本與可得性。
  - 來源：Plexus Form 10-K FY2022（as_of 2022-11-15）｜affects：thesis.R
- `ems_utilization_capex_cycle#2`（ems_utilization_capex_cycle｜方向 -｜狀態 ok）：Penang 馬來西亞第六廠：Q2 FY26 略低於損益兩平，預期財年末轉盈；Q3 摘要稱新增逾 $500M 產能（新產能稀釋 ROIC 風險點）
  - 來源：MarketBeat Plexus Q3 earnings call highlights（as_of 2026-07-30）｜affects：decision_inputs.bear、valuation
- `clinical_fda#0`（clinical_fda｜方向 -｜狀態 ok）：2025-01-22 有FDA 483檢查紀錄（第三方彙整站），涉及心臟監測Class II器材的陶瓷電容破裂調查與客訴紀錄風險評估缺漏；為檢查缺失，非警告信。
  - 來源：globalkeysolutions.net FDA 483 - Plexus Corp.（as_of 2025-01-22）｜affects：decision_inputs.bear

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 1 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/PLXS_20261103/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":409.2,"bear_5y_price":131.3,"p_bull_pct":25,"p_bear_pct":30,"upside_5y_pct":27.7,"ev5y_pct":23.6,"irr_base_pct":5.0,"asym_ratio":2.0,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":10.33,"pe":20.75,"basis":"FY1＝FY2027E 非GAAP 共識 EPS（Koyfin 2026-10-31 快照）÷ 現價 214.32；終端倍數同樣以下一年度預估 EPS 為分母"},"eps":{"bull":[11.2,13.2,15.0,16.8,18.6],"base":[10.33,11.79,13.0,14.1,15.2],"bear":[9.8,9.0,8.7,9.4,10.1]},"pe":{"bull":22,"base":18,"bear":13},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0,"net_buyback":1.0},"second_stage":{"bull_cagr_pct":10,"base_cagr_pct":7},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### PLXS_Q3_2026_Earnings_Call_20260730.md
- 2026-07-30｜CEO｜guidance：FQ4 營收財測區間（原話："We are guiding revenue of $1.33 billion to $1.38 billion"）
- 2026-07-30｜CEO｜guidance：FQ4 非GAAP營益率與EPS財測（原話："non-GAAP EPS of $2.47 to $2.63."）
- 2026-07-30｜CEO｜guidance：FY2026 營收成長預期（原話："deliver more than 20% revenue growth for fiscal 2026"）
- 2026-07-30｜CEO｜guidance：FY2027 營收成長潛力高於長期目標（原話："generate revenue growth in excess of our 9% to 12% goal"）
- 2026-07-30｜CFO｜guidance：FQ4 毛利率財測區間（原話："range of 10% to 10.3%. At the midpoint, gross margin will"）
- 2026-07-30｜CFO｜guidance：FY2027 非GAAP稅率初步看法（原話："between 16% and 18%"）
- 2026-07-30｜CFO｜guidance：FY2026 資本支出預期不變（原話："forecast is unchanged at $100 million to $120 million"）
- 2026-07-30｜CFO｜guidance：FQ4 自由現金流預期（原話："breakeven or a slight usage of cash"）
- 2026-07-30｜IR VP｜guidance：A&D 本季預期持平（原話："approximately flat versus our fiscal third quarter"）
- 2026-07-30｜IR VP｜guidance：A&D FY2027 成長高於長期目標（原話："should well exceed our 9% to 12% goal"）
- 2026-07-30｜IR VP｜guidance：HLS FY2026 成長預期（原話："we now anticipate revenue to increase in the high teens"）
- 2026-07-30｜CFO｜margin：S&A 槓桿口徑：扣除股權報酬與高管退休費用後的槓桿（原話："gained nearly 50 basis points of leverage compared to our"）
- 2026-07-30｜CFO｜margin：管理層對營益率目標的表述（原話："delivering non-GAAP operating margin at or above 6%"）
- 2026-07-30｜CFO｜margin：FY2027 營益率擴張，細節留待下季說明（原話："including future expectations for operating margin"）
- 2026-07-30｜CEO｜margin：新增產能預期對毛利影響（原話："we wouldn't expect it to have a meaningful impact"）
- 2026-07-30｜CFO｜margin：現金循環天數成果（原話："We delivered a 62-day cash cycle in the fiscal third"）
- 2026-07-30｜CFO｜margin：年底現金循環天數預期（原話："cash cycle days in the low to mid-60s"）
- 2026-07-30｜CEO｜commitment：FY2027 營益率擴張承諾（原話："we anticipate delivering operating margin expansion"）
- 2026-07-30｜CFO｜commitment：FY2027 自由現金流承諾（原話："free cash flow generation in excess of $100 million"）
- 2026-07-30｜CFO｜commitment：FY2027 資本支出維持營收2–3%（原話："range of 2% to 3% of revenue."）
- 2026-07-30｜CFO｜capital_allocation：FQ3 股票回購金額（原話："We repurchased $20.6 million of our stock"）
- 2026-07-30｜CFO｜capital_allocation：八月與董事會討論新回購授權（原話："We will discuss our next share repurchase authorization"）
- 2026-07-30｜CFO｜capital_allocation：馬來西亞擴產決定（原話："we've made the decision to expand"）
- 2026-07-30｜CEO｜capital_allocation：新增產能規模（原話："somewhere north of $0.5 billion of"）
- 2026-07-30｜IR VP｜capital_allocation：現有產能可支撐營收規模（原話："close to $6 billion of revenue"）
- 2026-07-30｜IR VP｜competition：半導體設備營收預期優於WFE（原話："we would expect to outgrow WFE again next year"）
- 2026-07-30｜CEO｜competition：份額成長與新專案為成長來源（原話："market share gains and support of disruptive"）
- 2026-07-30｜CFO｜risk：管理層承認供應鏈有吃緊點（原話："But there are tight spots. We're not going to gloss"）
- 2026-07-30｜CEO｜risk：預置庫存由客戶資金支應（原話："typically funding those replacements."）
- 2026-07-30｜IR VP｜product：HLS FY2027 短期成長趨緩（原話："we expect short-term growth moderation as activity"）
- 2026-07-30｜CEO｜product：資料中心策略funnel規模（原話："funnel that's conservatively somewhere around $0.5 billion"）
- 2026-07-30｜CEO｜customer：本季新專案贏單（原話："we secured 31 new manufacturing programs with $255 million"）
- 2026-07-30｜CEO｜customer：合格機會funnel創高（原話："opportunities expanded to a record $4.5 billion"）
- 2026-07-30｜IR VP｜customer：工業部門本季季增（原話："revenue increased 23% sequentially"）

### 問答異常語氣（迴避／改口／保留）
- PLXS_Q3_2026_Earnings_Call_20260730.md｜問：Ruben Roy 追問 A&D 與工業要達到強勁雙位數所需的成長與市場/份額拆分｜答法：Shawn Harrison 未給 A&D FY2027 成長百分比，回「I'll let you do the math to back into what the percentage must be」

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 3 | 3 |
| customer_second_source | found | 2 | 1 |
| customer_concentration_credit | found | 4 | 2 |
| supply_demand_durability | found | 5 | 3 |
| regulatory_antitrust | none | 0 | 3 |
| reg_tariff_export | found | 3 | 2 |
| geo_supply_chain | found | 2 | 2 |
| end_markets | found | 4 | 2 |
| substitute_technology | found | 1 | 1 |
| channel_business_model_shift | found | 1 | 2 |
| capital_markets_pricing | found | 6 | 4 |
| major_events | found | 2 | 4 |
| ems_utilization_capex_cycle | found | 4 | 3 |
| ems_roic_asset_turnover_benchmark | found | 4 | 3 |

未涵蓋／不適用軸的查詢詞原文（供判相關性）：
- **regulatory_antitrust**（none）：PLXS Plexus antitrust OR monopoly investigation 2026；Plexus regulation OR regulatory scrutiny Electronics Manufacturing Services Healthcare Defense 2026；PLXS Plexus DOJ OR FTC OR EU competition 2026

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260524","verdict":"B","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"FCF margin 從 FY26 1.5% 改善至 FY28+ 4%+（working capital 正常化）","columns":{"2Y 驗證點":"FY26 H2 FCF $50M+","5Y 驗證點":"FY28 FCF $300M+（margin 5%）","10Y 驗證點":"FY30 FCF $400M+","具體門檻":"FY26 全年 FCF","來源":"公司 quarterly FCF 揭露","漂移觸發":"連 2 季 FCF margin"}},{"id":"H2","text":"Non-GAAP OpMargin 維持在 6%+ 並向 7% 進階","columns":{"2Y 驗證點":"FY26 全年 6.0-6.5%","5Y 驗證點":"FY28 6.5-7.0%","10Y 驗證點":"FY30 7.0%+","具體門檻":"連 2 季","來源":"quarterly earnings","漂移觸發":"連 2 季 Non-GAAP OpMargin"}},{"id":"H3","text":"healthcare/Life Sciences 段 YoY 維持 +12%+ 為 group 主成長引擎","columns":{"2Y 驗證點":"FY26-27 平均 +12%+","5Y 驗證點":"FY28-29 +10%+","10Y 驗證點":"FY30 +8%+","具體門檻":"連 2 季 YoY","來源":"segment quarterly disclosure","漂移觸發":"連 2 季 healthcare YoY"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"FCF margin 持續無法改善（working capital 結構性問題）","columns":{"時間尺度":"🔥 中期（4-6 季）","監測指標":"季度 FCF margin","警戒閾值":"FY26 全年 FCF"}},{"id":"R2","text":"healthcare 段成長率 mean revert 至 mid-single-digit（COVID 後特殊週期結束）","columns":{"時間尺度":"🔥 中期","監測指標":"healthcare segment YoY","警戒閾值":"連 2 季"}},{"id":"R3","text":"EMS sector valuation mean reversion（CLS sentiment peak 退潮）","columns":{"時間尺度":"🐢 長期（2+ 年）","監測指標":"CLS / JBL / SANM Fwd PE 倍數","警戒閾值":"CLS Fwd PE 跌至"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🔴","ma":"✅","trap":"🟡","moat_trend":"→","runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":265.72,"archetype":null,"cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"PLXS","date":"2026-11-03","schema":"v15.0","contract":"v19","company_name":"Plexus Corp."},"oneliner":"EMS 裡執行力上乘的一家：FY26 營收 +23%、ROIC 15.8% 近十年新高，FY27 指引再成長中高十位數；但成長有一大塊來自半導體設備順週期，現金轉換在同業墊底，FY27E 20.75 倍已反映前兩年，等 175 美元附近再談。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/PLXS_20261103/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/PLXS_20261103/scenario.json","answers":{"q1_business":{"verdict":"賺的是工業、半導體設備、醫療與國防 OEM 的高組合低量外包製造費：錢卡在客戶議價與零組件成本轉嫁之間，公司只拿約 10% 毛利、6% 營益率，超額報酬來自營運資金周轉，不是定價權。","reasoning":"FY26 營收 49.65 億美元，年增 23%；分部為工業 21.85 億（44%）、醫療與生命科學 19.33 億（39%）、航太國防 8.47 億（17%）（Q4 FY26 財報新聞稿分部表，2026-10-28）。最新一季營收 14.27 億美元，年增 34.8%；毛利率 10.2%（CFO，2026-10-29 法說），非GAAP營益率 6.7%、GAAP 6.0%。Q1 FY27 指引營收 14.1–14.6 億、非GAAP營益率 6.0–6.4%。單點依賴：FY25 無單一客戶達 10%，但前十大客戶由 FY25 49% 升到 FY26 54%、Q4 56%；工業部門的成長主要來自半導體設備（FY26 該子段 +50%）。產業時鐘判擴張期：北美 EMS 2026 年 6 月 book-to-bill 1.33，限制在產能與交期而非需求；公司機會漏斗 49 億美元、年增 33%；尚未見產能過剩或降價。供需持久度：國防與太空屬結構性持久，半導體設備屬週期性、終將反轉，醫療在 FY26 消化後回到高個位數。產業態勢三軸：競爭面靜態（管理層 10-29 稱競爭環境沒有變化，10-K 承認製程無專屬保護）；需求結構轉好（歐洲國防是 EMS 最強的結構性需求、北美訂單出貨比大於 1）；其他結構變數在關稅與出口管制（馬來西亞集中、墨西哥 IMMEX）。裁決：雙向拉鋸，需求結構轉好與貿易政策風險並存。","fact_refs":["f_kpi0_revenue_gaap","f_kpi1_non_gaap_operating_incom","f_kpi2_gaap_operating_income_ma","f_kpi5_guidance_q1_fy2027_2027_","f_kpi6_inventory_days","f_peer_plxs_gross_margin_pct","f_earnings_recency"],"verdict_values":{"revenue_quality":"合約製造、按出貨認列；多數合約可每季依零組件價格調價，但調價空檔的漲價由公司吸收；贏單金額是滿產後的年化值，量產爬坡需數季，不是保證營收。","unit_econ_note":"每 1 美元增量營收約需 0.15–0.20 美元營運資金（CFO，2026-10-29）；增量營收的營業利益流通率目標 8–12%，FY27 預期在低端；資本支出長期占營收 2–3%，FY27 偏上緣。","archetype":{"primary":"EMS/ODM","secondary":null,"confidence":"高","fingerprint":"毛利率約 10%、營益率 5–7%、資本支出占營收 2–3%、未揭露研發、前十大客戶過半、按專案量產爬坡認列"},"industry":{"clock_phase":"II","sd_verdict_source":"北美 EMS 2026 年 6 月 book-to-bill 1.33、出貨 +6.7%，產業協會稱限制在產能與交期；歐洲 EMS 以國防為最強結構性需求（Evertiq，2026-03）；半導體設備管理層只看得到 FY27、自承有週期（2026-10-29 法說）。合判：國防結構性持久，半導體設備週期性將反轉。","bargaining":{"up":"上游零組件吃緊（COO 10-29 稱材料環境受限），漲價在調價空檔由公司吸收，對上游議價力弱。","down":"下游是大型 OEM，前十大占 54–56%；客戶可自製或換廠，價格與組合對營益率的貢獻管理層自稱有限，議價力在客戶手上。","geo":"美國以外營運占營收與營業利益多數，集中在馬來西亞；墨西哥廠依 IMMEX 保稅計畫運作；另有中國廈門廠。"},"profit_pool_dir":"事實表未涵蓋 EMS 利潤池五年分布；同業營益率集中在 4.3%–5.5%，看不出利潤往 EMS 環節移動。","tam_table":{"expanded":false,"reason":"事實表沒有 EMS 外包滲透率與 TAM 資料；公司成長來自份額與新專案爬坡，不是低滲透或新品類故事，TAM 不是估值的承重假設"}}}},"q2_moat":{"verdict":"護城河方向穩定：機制是受監管、高組合低量產品的製造執行與再認證轉換成本，不是定價權；ROIC 15.8% 對 WACC 9% 有 6.8 個百分點利差、創近十年新高，但毛利率與營益率只在同業中段、自由現金流率同業最差，改善有相當部分來自半導體設備順週期的稼動率。","reasoning":"機制：醫療 Class III 器材、飛行加油系統、太空電子這類受監管、高組合低量產品，換廠要重新認證，形成專案層級的轉換成本；再加上現金循環 62 天的營運資金效率，把約 5% 的營益率放大成 15.8% 的 ROIC。評分：執行 7（上行期仍拿份額、ROIC 由 Q1 13.2% 升到 Q4 15.8%、FY26 贏單 12 億美元年化），定價 5（毛利率 10.08% 與 SANM、FLEX、JBL、BHE 的 9.0%–10.4% 同區間，營益率 5.02% 居中，FCF 率 −1.0% 同業最差）。對最強同業：第三方彙整站 ROIC 顯示 CLS 39.5%、JBL 29.8%、FLEX 19.2% 都高於 PLXS 的 18.7%（2026 Q1 口徑），只贏 SANM 11.3%；對自身 WACC 9% 的利差 6.8 個百分點且在擴大。報酬持續期：當期屬低利益率、高周轉，15.8% 約等於稅後營益率 5.1%（非GAAP 6.2% 扣 17% 稅）乘投入資本周轉約 3.1 倍（推算）；四檢查點三黃一綠；增量 ROIC 約 12%–20%，FY27 再投資率約 65%，內生成長上限約每年 10%。","fact_refs":["f_peer_plxs_gross_margin_pct","f_peer_plxs_operating_margin_pct","f_peer_plxs_fcf_margin_pct","f_peer_sanm_gross_margin_pct","f_peer_sanm_operating_margin_pct","f_peer_sanm_fcf_margin_pct","f_peer_bhe_gross_margin_pct","f_peer_bhe_operating_margin_pct","f_peer_bhe_fcf_margin_pct","f_peer_flex_gross_margin_pct","f_peer_flex_operating_margin_pct","f_peer_flex_fcf_margin_pct","f_peer_jbl_gross_margin_pct","f_peer_jbl_operating_margin_pct","f_peer_jbl_fcf_margin_pct","f_kpi6_inventory_days"],"verdict_values":{"moat":{"mechanism":"受監管、高組合低量產品（醫療 Class III、航太國防、太空）的製造執行與再認證轉換成本，加上營運資金周轉效率；不是專利或定價權。","execution":7,"pricing":5,"grade":"C","trend":"→","trend_evidence":"執行面擴大：上行期仍拿到份額（IR 副總稱上行期拿份額少見）、ROIC 由 Q1 13.2% 升到 Q4 15.8%、現金循環 69→64→62 天。定價面穩定：毛利率 10.08% 與同業 9.0%–10.4% 同一區間，CFO 稱價格與組合影響相當有限。兩面合計，執行改善有一部分來自半導體設備順週期與年底固定成本槓桿，故方向判穩定而非擴大。","competitor_notes":[{"name":"SANM","strategy_note":"營益率 5.49%、FCF 率 4.66% 都高於 PLXS，同樣做高組合工業與國防，是現金轉換最直接的對照；第三方 ROIC 11.3% 則低於 PLXS。"},{"name":"JBL","strategy_note":"營益率 5.11% 與 PLXS 相近，FCF 率 3.82%；第三方 ROIC 29.8% 遠高於 PLXS，差距主要在資產周轉（1.6 倍對 1.3 倍）。"},{"name":"FLEX","strategy_note":"營益率 5.44%、FCF 率 3.32%；第三方 ROIC 19.2% 略高於 PLXS，同樣押資料中心與電力。"},{"name":"BHE","strategy_note":"毛利率 10.38% 略高於 PLXS，但營益率只有 4.25%，是同一高組合低量定位裡費用效率較差的對手，PLXS 在此對照中領先。"},{"name":"CLS","strategy_note":"不在事實表同業對照內；第三方資料顯示 ROIC 39.5%、營益率 8.9%，靠 AI 資料中心組合拿到 EMS 少見的超額利潤，PLXS 未進入同一利潤層級。"}],"peer_na_reason":"事實表同業對照只有利潤率，沒有 ROIC 與投入資本；同業 ROIC 只能引第三方彙整站口徑，與公司自報口徑不同，僅作方向參考。","threats":[{"level":"🟡","text":"製程無專利保護，資源更大的同業或客戶自製可能帶來降價與丟單（10-K 風險因素）；管理層 10-29 稱競爭環境目前沒有變化。","p":"20%","evidence_refs":["competitive_share_entrants#1","competitive_share_entrants#2","customer_second_source#0"]},{"level":"🟡","text":"零組件漲價在合約調價空檔由公司吸收，回收調價又稀釋營益率；COO 稱目前材料環境吃緊。","p":"30%","evidence_refs":["reg_tariff_export#2"]},{"level":"🟡","text":"醫療品質事件：第三方彙整站記錄 2025-01 一份 FDA 483 檢查缺失（心臟監測器材），不是警告信，之後未見召回紀錄；品質是公司主打賣點，若升級為警告信或召回，會直接傷到占營收 39% 的醫療部門贏單。","p":"10%","evidence_refs":["clinical_fda#0"]}],"roic_durability":{"quadrant":"低利益率×高周轉","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者是病患、國防單位與晶圓廠，決策與付款者是 OEM；外包製造是『需要』而非『想要』，延後的代價是 OEM 自建產能。國防與太空需求結構性成長，但工業部門（44%）的主力半導體設備屬週期性，管理層只看得到 FY27，故給黃燈。"},{"item":"決策層級","level":"🟡","text":"替代性要在單一專案層級看：醫療 Class III 心臟除顫器、飛行加油系統、太空電子換廠需重新認證，轉換成本高；但每個新專案都重新比稿，10-K 承認製程無專屬保護、客戶可自製。漲價後流失率與續約率事實表未涵蓋，只看得到贏單多來自既有客戶擴大份額。"},{"item":"價值鏈分配","level":"🟡","text":"價值鏈的利潤主要留在 OEM 品牌與晶片零組件端，EMS 只拿約 10% 毛利；前十大客戶占比升到 54–56%、上游材料吃緊，兩頭議價都不在公司手上。但毛利率由 FY22 9.1% 緩升到 FY26 10.1%，分配比例沒有惡化。"},{"item":"社會容忍度","level":"🟢","text":"製造服務費占終端產品成本小，沒有社會對漲價敏感的問題，也不靠監管授權取得優勢；政策面風險是關稅與出口管制，屬成本與營運風險，不是定價上限，已列入長期風險。"}],"roiic":"約 12%–20%（推算）","reinvest_rate":"FY26 逾 100%；FY27 約 65%（推算）","endo_ceiling":10,"formula_note":"內生上限＝增量 ROIC 約 15%（區間中值）× FY27 再投資率約 65% ≈ 每年 10%。增量 ROIC：FY25→FY26 營業利益增量 GAAP 約 4,200 萬、非GAAP 約 7,000 萬美元（營益率×營收推算），扣 17% 稅後，除以新增營運資金約 2.5 億（CFO 2026-10-29）加資本支出淨額（折舊事實表未涵蓋，以 FY26 資本支出指引 1.0–1.2 億近似上限）。再投資率：FY27 非GAAP稅後營業利益約 3 億（營收成長中高十位數、增量營益率 8%、稅率 16–18% 推算）減 FCF 目標 1 億。均為推算，非公司公布。"}}}},"q3_growth":{"verdict":"五年後成長空間黃燈：未來兩年有中高十位數的指引、創新高的 49 億美元機會漏斗與 12 億美元年化贏單支撐；但 Y5 之後沒有可量化的滲透率或已成形的第二條曲線，半導體設備有週期，長期回到公司 9–12% 的長期營收目標附近較合理。","reasoning":"成長來源以量為主：新專案量產爬坡、既有客戶份額提升與終端需求，價格與組合貢獻 CFO 稱相當有限；無併購；回購每年約 1 億美元（約市值 1.75%）。共識：FY27E 10.33、FY28E 11.79，以 FY26 推算基期 9.10 計兩年 EPS 年化約 13.8%（只有兩年，第三年共識事實表未涵蓋）。內生上限約 10%（增量 ROIC 約 15% × 再投資率約 65%），缺口約 3.8 個百分點，可歸因於營益率由 6.2% 走向 6.5–7% 目標（每年約 2–3 個百分點）與淨回購（約 1 個百分點），不依賴倍數上調。五年後：事實表沒有外包滲透率，無法換算達 30% 滲透的年數；第二條曲線有雛形（國防與太空、資料中心電力機會漏斗約 5 億美元，CEO 2026-07-30），但尚未成為可量化營收，故判黃燈。衰退訊號亮 1 個、接近 1 個：EPS 成長長期快於營收（FY23→FY25 營收年減約 2%、GAAP EPS 年增約 12.5%）；FCF 對淨利轉換偏低（FY26 為負，FY27 指引 1 億美元只約稅後利潤三分之一），FY27 若照指引即連 2 年亮燈。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_kpi5_guidance_q1_fy2027_2027_","f_kpi3_free_cash_flow"],"verdict_values":{"growth":{"driver_mix":"量為主：新專案爬坡、既有客戶份額提升與終端需求；價格與組合貢獻 CFO 稱相當有限；無併購；回購約每年 1 億美元。","runway_years":"事實表未涵蓋外包滲透率，無法換算","runway_post_y5":"🟡","endo_ceiling_basis":"引用護城河段報酬持續期：增量 ROIC 約 15% × FY27 再投資率約 65% ≈ 每年 10%，共識兩年 EPS 年化 13.8% 超出約 3.8 個百分點，缺口由營益率擴張與淨回購解釋。","segments":[{"item":"工業（FY26 21.85 億美元，44%）","value":"FY26 +27%（半導體設備 +50%）；Q4 年增約 50%；FY27 指引 >20%；Q1 FY27 預估季減低個位數"},{"item":"醫療與生命科學（19.33 億，39%）","value":"FY26 +19%；FY27 高個位數（7 月時說短期放緩，10 月上調）；Q1 季增低個位數"},{"item":"航太國防（8.47 億，17%）","value":"FY26 +23%；FY27 >20%；FY26 贏單 4.9 億美元，超過 FY23–FY25 合計；Q4 季減 4%，管理層歸因材料時點"}],"decay_signals":[{"item":"毛利率連 2 季年減","lit":false,"note":"FY26 TTM 10.08% 與 FY25 相同，Q4 10.2%"},{"item":"核心市占近 12 個月縮減","lit":false,"note":"管理層稱上行期仍拿份額；第三方份額數據事實表未涵蓋"},{"item":"提價後銷量下滑","lit":false,"note":"不適用，EMS 價格隨零組件調整"},{"item":"EPS 成長顯著快於營收（差 >5 個百分點）","lit":true,"note":"FY23→FY25 營收年減約 2%、GAAP EPS 年增約 12.5%"},{"item":"FCF 對淨利 <0.75 連 2 年","lit":false,"note":"FY25 約 0.89；FY26 為負；FY27 指引隱含約 0.35，若兌現即亮燈"},{"item":"SBC 占營收 >5% 且上升","lit":false,"note":"0.67%"},{"item":"TAM 萎縮或被替代技術壓縮","lit":false,"note":"10-K 未點名替代技術"},{"item":"產業估值倍數近 3 年系統性下移","lit":null,"note":"事實表未涵蓋"},{"item":"維持性資本支出占 FCF >60%","lit":null,"note":"FCF 接近零，維持性資本支出事實表未涵蓋，無法判定"},{"item":"停止投資新產能且營收 3 年內下滑","lit":false,"note":"檳城第六廠擴產中"}],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"資本配置中等：回購有紀律、SBC 稀釋輕，但 FY26 自由現金流為負，回購靠的是資產負債表而不是當年現金。","reasoning":"FCF 對淨利轉換偏弱：FY26 全年 FCF −2,890 萬美元，Q4 為營業現金流 2,920 萬減資本支出 2,280 萬＝640 萬；TTM FCF 率 −1.0%，同業 3.3%–4.7%。原因是營收年增 23% 需要約 2.5 億美元營運資金（CFO 2026-10-29：每 1 美元增量營收約需 0.15–0.20 美元）。SBC 占營收 0.67%，稀釋輕。現金去向：FY26 回購計畫執行完畢（Q4 約 2,100 萬美元），FY27 新授權 1 億美元已開始；無併購；事實表未見股息。資產負債：事實表淨負債 1,081 萬美元（含租賃負債），公司口徑為淨現金；循環額度動用 1.59 億、可再借逾 3.4 億，2026-06 新信用協議到期 2031 年。近三年現金四分去向與債務利率事實表未涵蓋。","fact_refs":["f_kpi3_free_cash_flow","f_kpi4_sbc_gaap","f_net_debt_m","f_shares_diluted_m","f_peer_plxs_fcf_margin_pct"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":false,"passed":null,"input":"近 12 個月 8-K 無併購項目，成長不靠併購，不適用。"},{"name":"buyback_yield","applicable":true,"passed":false,"input":"回購均價事實表未涵蓋；以現價計 FY27E 盈餘殖利率約 4.8%（10.33 ÷ 214.32），10 年期公債殖利率事實表未涵蓋，但即使只有 3%，門檻也要 5%，判不過；FY26 回購期間 FCF 為負。"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"Q4 SBC 960 萬美元（含 110 萬高階主管退休加速認列），占營收 0.67%；年化約 3,500 萬，約市值 0.6%，每年 1 億美元回購抵銷有餘，淨稀釋為負。"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購，資本回饋只有回購（FY26 計畫已執行完畢，FY27 新授權 1 億美元已開始）；近三年現金四分去向、回購均價與債務利率事實表未涵蓋，無法展開。"}}}},"q5_valuation":{"verdict":"現價要求 FY27–FY28 共識（10.33／11.79 美元）兌現、之後每年仍有約 10% 成長、倍數守在 18 倍左右，五年年化才約 6%；前兩年我信，半導體設備高峰 EPS 配現行倍數我不信，估值偏滿。","reasoning":"現價 214.32 美元＝FY27E 20.75 倍、FY28E 18.2 倍、EV 對 FY27E 營收 0.97 倍。Trailing P/E 28.92 倍在近三個年度端點的 66.8 分位，P/S 1.15、EV/S 1.15 在三點中最高；五年分位事實表只有三個年度端點，無法計算。PEG 約 1.5。現價隱含：FY27–FY28 共識兌現、之後每年仍有約 10% 成長、終端倍數守在 18 倍左右，基本情境五年年化約 6%（含約 1% 淨回購）。我信前兩年（指引、漏斗、贏單都支持），不信半導體設備高峰 EPS 配現行倍數。需求量循環五訊號判中循環。賣方目標價 8 月前後 247–308 美元（多來源，均非 11 月最新）全在現價之上，最高與最低（150–330）相差 2.2 倍，未到需下修信心的 2.5 倍。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_consensus_eps_fy1","f_consensus_eps_fy2","f_pe_current","f_pe_percentile","f_ps_current","f_ps_percentile","f_ev_s_current","f_ev_s_percentile","f_ev_s_fwd","f_consensus_rev_fy1_pct","f_consensus_rev_fy2_pct","f_consensus_rev_3m_fy1_pct"],"verdict_values":{"valuation":{"basis":"Forward P/E（FY27E 非GAAP 共識）為主，EV/S 0.97 倍與 P/S 作交叉檢查","tier":"中型 EMS（高組合低量）","peers":{"expanded":false,"reason":"事實表同業對照只有利潤率，沒有同業本益比或 EV/S，倍數無法做同業對照；這是資料缺口，不是不承重"},"fwd_pe":20.75,"peg":1.5,"percentile_5y":null,"val_light":"🟠","val_light_derivation":"FY27E 本益比 20.75 倍、PEG 約 1.5（20.75 ÷ FY26 推算基期到 FY28E 兩年 EPS 年化 13.8%），在合理區上緣；P/S 1.15、EV/S 1.15 是近三個年度端點最高；基本情境五年年化約 6%（含約 1% 淨回購），低於 8%。一年目標以 FY28E 11.79 × 19 倍（現行與終端倍數之間）約 224 美元，上檔約 4.5%；五年基本情境 15.2 × 18 倍約 274 美元，約 +27.7%。判偏滿：不到紅燈，因股價已較前份跌約 19% 且 FY27 共識財報後再上修。","upside_short_pct":4.5,"upside_mid_pct":27.7,"denominator_disputed":false,"denominator_note":"分母採 FY27E 非GAAP 共識（排除 SBC 等），GAAP 與非GAAP 每季約差 0.3 美元；FY1 共識『近三個月 +25.5%』可能混入財年換檔，真實上修以財報後 +2.1% 為準。分母本身不是爭點。"}}},"q6_how_wrong":{"verdict":"最可能看錯的地方是把半導體設備高峰的成長與營益率當常態；其次是成長吃掉現金，EPS 好看但股東拿不到現金。陷阱風險黃燈。","reasoning":"三個視角的反證已寫在反證段，這裡只交結論：衰退訊號亮 1 個（EPS 長期快於營收），另 1 個接近（FCF 對淨利轉換，FY27 若照指引將連 2 年偏低），陷阱風險黃燈。價格面已先反映一部分：股價較前份 265.72 美元跌約 19%、26 週 −18.4%、RSI 37，週線位於 52 週均線 223 美元之下、104 週均線 181 美元之上；250 週均線 133 美元在空頭情境價位附近。歷史最大回撤、空方最強數字事實表未涵蓋。上一季法說的迴避（A&D FY27 成長率）本季已補上 >20%，這個缺口已關閉。","fact_refs":["f_kpi3_free_cash_flow","f_peer_plxs_fcf_margin_pct","f_week26_return_pct","f_rsi14","f_ma_w52","f_ma_w104","f_ma_w250","f_ma_state"],"verdict_values":{"trap":{"verdict":"🟡","label":"週期高峰 EPS 加上現金轉換偏弱"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":10.33,"pe":20.75,"basis":"FY1＝FY2027E 非GAAP 共識 EPS（Koyfin 2026-10-31 快照）÷ 現價 214.32；終端倍數同樣以下一年度預估 EPS 為分母"},"eps":{"bull":[11.2,13.2,15.0,16.8,18.6],"base":[10.33,11.79,13.0,14.1,15.2],"bear":[9.8,9.0,8.7,9.4,10.1]},"pe":{"bull":22,"base":18,"bear":13},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0,"net_buyback":1.0},"second_stage":{"bull_cagr_pct":10,"base_cagr_pct":7},"max_dd":{"lo":-55,"hi":-37,"basis":"空頭路徑谷底 FY28 EPS 約 9.0 × 下行期 12–15 倍＝108–135 美元，對現價約 −50%～−37%；尾端情境（EPS 回到約 7.5、13 倍）約 98 美元、−55%，作為下緣。250 週均線 133 美元落在區間內。事實表未涵蓋歷史最大回撤，故以估值推算；股價自前份 265.72 美元已跌約 19%，一年內兩成以上的回撤對這檔是常態。","trigger_time":null},"basis":{"bull":"Q4 非GAAP EPS 2.84 年化 11.36 已高於 FY27 共識；FY27 照指引上緣、營益率提前進入 6.5–7%；國防太空與資料中心電力接棒半導體設備，FY29–FY31 每年約 11–14%；終端 22 倍。機率 25%。","base":"FY27–FY28 採共識 10.33／11.79；FY29–FY31 每年約 8–10%，接近公司 9–12% 長期營收目標下緣加小幅營益率擴張，股數假設不變（回購另計 1%）；終端 18 倍低於現行 20.75 倍，反映成長回到個位數高段。同業本益比事實表未涵蓋，無法附同業倍數對照。機率 45%。","bear":"半導體設備在 FY27 下半年轉弱、醫療再度消化，FY27 EPS 9.8 未達共識；FY28–FY29 工業部門負成長、稼動率下滑，EPS 8.7–9.0 見底，FY30 起隨國防與醫療回升到約 10；終端 13 倍取成長熄火錨（三年後成長降到 15%／10%／5% 對應約 20／17／13 倍，取 5% 那一檔）。機率 30%：共識成長超過內生上限，且管理層自承只看得到 FY27。"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"工業部門占 FY26 營收 44%，半導體設備子段 FY26 +50%；CEO 10-29 只願對 FY27 表態，IR 副總自承半導體設備有週期；Q1 FY27 工業部門預估季減低個位數。","assumption":"基本情境假設半導體設備溫和正常化，FY29 起公司成長仍有 8–10%。","consequence":"若 FY28 半導體設備進入下行，工業部門由 +27% 轉負，營業槓桿反向，營益率回到 5% 附近，EPS 回到約 7.5 美元、倍數 13 倍，股價約 98 美元，較現價約 −55%。","ruling":"採納為空頭路徑與回撤下緣（空頭 30% 內約三分之一是這個尾端），但不當基本情境：上行期仍拿份額、國防贏單 4.9 億美元超過前三年合計，可緩衝；此視角與唯一致命點重疊，維持不動。","watch":"工業部門季營收年增率、北美 EMS book-to-bill、FY27 營收指引","evidence_refs":["end_markets#3","supply_demand_durability#0","competitive_share_entrants#1"],"fact_refs":["f_kpi5_guidance_q1_fy2027_2027_","f_ma_w250"]},{"view":"論點成功但股東經濟變差","evidence":"FY26 營收 +23%，但全年 FCF −2,890 萬美元、TTM FCF 率 −1.0%，同業 3.3%–4.7%；CFO 說每 1 美元增量營收要 0.15–0.20 美元營運資金；檳城第六廠新增逾 5 億美元營收產能，Q2 FY26 仍略低於損益兩平；10-K 承認零組件漲價在調價空檔由公司吸收。","assumption":"成長放緩前，營運資金效率與新廠稼動能讓 FCF 轉正並守住 ROIC 15%。","consequence":"若成長再超預期，營運資金吃掉更多現金，FY27 FCF 達不到 1 億美元；新產能閒置則 ROIC 回落到 13% 以下，EPS 成長但股東拿不到現金，回購只能靠借款。","ruling":"部分採納：低 FCF 主要是成長期營運資金投入，現金循環 62 天創紀錄、客戶分攤部分存貨，屬時點問題；但把 FY27 FCF ≥1 億美元設為驗證門檻，未達即品質分降一級。","watch":"季度 FCF、現金循環天數、ROIC、檳城新廠損益","evidence_refs":["ems_utilization_capex_cycle#2","reg_tariff_export#2","ems_roic_asset_turnover_benchmark#2"],"fact_refs":["f_kpi3_free_cash_flow","f_peer_plxs_fcf_margin_pct","f_kpi6_inventory_days"]},{"view":"價格已反映太多","evidence":"FY27E 本益比 20.75 倍、FY28E 約 18.2 倍；P/S 1.15、EV/S 1.15 在近三個年度端點最高；FY1 共識『近三個月 +25.5%』可能混入財年換檔，財報後真實上修只有 +2.1%（FY1）與 +3.4%（FY2）。","assumption":"市場給的倍數反映的是可持續的成長，而不是半導體設備高峰。","consequence":"若市場把 FY27 EPS 視為週期高點，倍數回到 15–17 倍，即使 EPS 兌現，一年後股價也只有約 177–200 美元。","ruling":"採納：判估值偏滿，現價不追，等 175 美元附近；但股價已較前份跌約 19%，不是泡沫，不給紅燈。","watch":"財報後共識修正方向、FY27E 本益比","evidence_refs":["capital_markets_pricing#4","capital_markets_pricing#3"],"fact_refs":["f_fwd_pe_latest","f_ps_percentile","f_ev_s_percentile","f_consensus_rev_3m_fy1_pct","f_consensus_rev_fy1_pct","f_consensus_rev_fy2_pct"]},{"view":"論點失敗","evidence":"10-K FY2025：美國以外營運占營收與營業利益多數、集中在馬來西亞；墨西哥廠依 IMMEX 保稅計畫降關稅；出口管制可能限制對中國出貨、在中國生產與採購先進半導體零組件；另有中國廈門廠。","assumption":"關稅與貿易措施的成本能透過合約調價轉嫁。","consequence":"若無法轉嫁，毛利率掉 0.5–1 個百分點就吃掉營益率由 6.2% 走向 6.5–7% 的全部空間。","ruling":"列為長期風險，不放進基本情境；不預測政策，只以單季毛利率 <9.5% 且管理層歸因關稅作為吸收失敗的判定。","watch":"單季毛利率、法說中關稅損益歸因、IMMEX 規則","evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","geo_supply_chain#0","geo_supply_chain#1"],"fact_refs":["f_peer_plxs_gross_margin_pct"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 265.72 → 本次 214.32（-19.3%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=265.72","side_b":"本次 price_at_dd=214.32","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 265.72 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 265.72 美元：五年期望值 前份未列，基準年化 前份未列，前份未列不對稱比","side_b":"本次情境、股價仍用 265.72 美元：Bull 價 409.2、Bear 價 131.3，五年期望值 −0.3%，基準年化 0.6%，不對稱比 0.89","ruling":"先換情境、股價不動：五年期望值與基準年化前份未列，無法比較。前份未列不對稱比，本次為 0.89。Bull、Bear 價位與股價無關，只受情境影響。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 265.72 美元：五年期望值 −0.3%，基準年化 0.6%，不對稱比 0.89","side_b":"本次情境、股價 214.32 美元：五年期望值 +23.6%，基準年化 5.0%，不對稱比 1.96","ruling":"再換股價、情境不動：起點價下跌 19.3%，五年期望值多 23.9 個百分點，基準年化多 4.4 個百分點，不對稱比由 0.89 升到 1.96。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"客戶集中度","cause":null,"prior_field":null,"side_a":"CEO Todd Kelsey（2026-10-29）：56% 是長期常見水準，49% 偏低，公司沒有變得結構性集中。","side_b":"10-K 與財報：前十大占比 FY24 47.8%、FY25 49.1%、FY26 54%、Q4 56%，Q4 年增 7 個百分點；FY23 GE Healthcare 單一客戶 10.3%。","ruling":"可調和（程度差異）：事實表沒有 FY23 以前的前十大占比，無法驗證『歷史常態』，但 FY23 有單一客戶超過 10%，顯示過去集中度也不低；趨勢向上且與大型專案爬坡同步，列為中期風險，不當作論點失效。","evidence_level":"一手（10-K、8-K）對照管理層口述","settle_metric":"前十大客戶季占比、年報單一客戶是否 ≥10%","if_then":["若 FY27 任一季前十大 ≥60% 或年報揭露單一客戶 ≥10%，倉位上限降一級，該風險時鐘改為一到兩季","若前十大回落到 52% 以下且營收成長未放緩，降為觀察項"],"evidence_refs":["customer_second_source#1","customer_concentration_credit#0","customer_concentration_credit#1","customer_concentration_credit#2","customer_concentration_credit#3"]},{"axis":"成長與現金","cause":null,"prior_field":null,"side_a":"FY26 營收 +23%、ROIC 15.8% 近十年最高、現金循環 62 天創紀錄。","side_b":"同一年 FCF −2,890 萬美元、TTM FCF 率 −1.0% 為同業最差；FY27 FCF 目標 1 億美元只約稅後利潤三分之一。","ruling":"可調和：兩者同時成立，因為高成長要先墊營運資金與產能；關鍵是 FY27 成長放緩到中高十位數時 FCF 能否回到 1 億美元以上。","evidence_level":"一手（財報新聞稿、法說）","settle_metric":"FY27 全年 FCF、現金循環天數","if_then":["若 Q2 FY27（約 2027-04）累計 FCF 仍為負且現金循環 >70 天，品質分降一級，重啟價位由 175 下調到 160 美元","若 FY27 FCF ≥1 億美元且現金循環 60–65 天，本矛盾撤銷"],"evidence_refs":["ems_utilization_capex_cycle#2","ems_roic_asset_turnover_benchmark#2"]},{"axis":"半導體設備能見度","cause":null,"prior_field":null,"side_a":"COO Oliver Mihm（2026-10-29）：半導體設備曆年成長會比 FY26 的 50% 更強；分析師引述同業已看到 2029–2030 年的預測。","side_b":"CEO Todd Kelsey 同場：只對 FY27 有把握，不願往後看；IR 副總 Shawn Harrison：半導體設備有週期，採保守假設。","ruling":"可調和：近一年強、更遠不可見，兩者並存。基本情境 FY29 起成長降到 8–10%，空頭機率 30% 承擔週期反轉，不採信長天期預測。","evidence_level":"管理層口述（同場）","settle_metric":"工業部門季營收年增率、北美 EMS book-to-bill","if_then":["若工業部門連 2 季年減，持有部位減碼一半並把空頭機率提到 40%","若 FY27 下半年工業部門仍年增 >20% 且 FY28 指引延續成長，多頭機率由 25% 提到 30%"],"evidence_refs":["supply_demand_durability#0","supply_demand_durability#2","supply_demand_durability#4"]},{"axis":"管理層前後說法","cause":null,"prior_field":null,"side_a":"2026-07-30 法說：CEO 給 Q4 營收 13.3–13.8 億、FY26 成長逾 20%；CFO 說 Q4 FCF 約損益兩平或小幅用現金；IR 副總說 A&D Q4 約與 Q3 相當、醫療 FY27 短期放緩，且不肯給 A&D FY27 成長率。","side_b":"2026-10-29 法說：Q4 營收 14.27 億超過上緣、FY26 成長 23%、Q4 FCF +640 萬；醫療 FY27 上調為高個位數、A&D 給出 >20%；但 A&D Q4 季減 4%，COO 歸因材料時點並稱 Q1 會補回。","ruling":"大致兌現或超標，管理層可信度加分。A&D 的材料時點歸因不採信也不否定，列為未證：若 Q1 FY27 A&D 未見高個位數季增，此歸因判為不成立，國防這條成長腿降級。","evidence_level":"一手（兩場法說逐字稿）","settle_metric":"Q1 FY27 航太國防季增率","if_then":["若 Q1 FY27 航太國防季增 <5%，H1 的國防腿降級，多頭機率降到 20%","若 Q1 FY27 航太國防季增 ≥8%，歸因成立，不調整"],"evidence_refs":["end_markets#1","capital_markets_pricing#0","end_markets#3"]},{"axis":"共識修正口徑","cause":null,"prior_field":null,"side_a":"FY1 共識 EPS 近三個月由 8.23 升到 10.33（+25.5%）。","side_b":"財報前後兩份快照只從 10.12 升到 10.33（+2.1%），FY2 由 11.40 升到 11.79（+3.4%）；7 月時的 FY1 很可能仍是 FY26（Chartmill 10-18 的 FY26 共識 8.87 與 8.23 同一量級），10 月底已換成 FY27。","ruling":"採後者：近三個月 +25.5% 大部分是財年換檔，不是分析師大幅上修；真實上修幅度以財報後 +2.1%／+3.4% 為準，動能判讀不應引用 +25.5%。","evidence_level":"推論（兩份快照未標財年）","settle_metric":"下一份快照的 FY27 共識三個月變化","if_then":["若 2027-01 快照 FY27 共識較 10-31 再上修 ≥5%，多頭機率由 25% 提到 30%","若 FY27 共識下修 ≥5%，空頭機率提到 35% 並暫停重啟評估"],"evidence_refs":["capital_markets_pricing#3"]},{"axis":"循環位置","cause":null,"prior_field":null,"side_a":"偏買：股價 26 週 −18.4%、RSI 37，賣方目標價高於現價；北美 EMS book-to-bill 1.33，限制在產能而非需求；公司機會漏斗年增 33%。","side_b":"偏賣：P/S、EV/S 在近三個年度端點最高；半導體設備 FY26 +50% 且管理層只看得到 FY27；存貨天數 119 天；Q1 FY27 營收只季增約 1%、工業部門季減。","ruling":"五個需求量訊號多數決判中循環：需求仍向上但動能放緩、倍數貼近自身近年高點，客戶庫存狀況事實表未涵蓋。中循環對應持有不加；倍數貼高點，新建立部位的條件不成立，交易面等回踩。","evidence_level":"產業協會＋公司數字","settle_metric":"北美 EMS book-to-bill、工業部門季營收","if_then":["若北美 EMS book-to-bill 跌破 1 且工業部門連 2 季季減，改判晚循環，不建立任何部位","若股價回到 104 週均線 181 美元以下而工業部門仍年增 >15%，改判中循環偏早，進入首倉評估"],"evidence_refs":["supply_demand_durability#2","capital_markets_pricing#4"]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"現在就買：Q4 非GAAP EPS 2.84 年化 11.36，已高於 FY27 共識 10.33；股價較前份跌約 19%、26 週 −18.4%、RSI 37，賣方 8 月目標價 247–308 美元都在現價之上；財報後 FY27、FY28 共識仍上修，ROIC 近十年最高、機會漏斗 49 億美元創新高。若 FY27 EPS 落在 11 以上，現價只有約 19 倍。","side_b":"觀望：Q4 有年底固定成本槓桿與材料拉貨，管理層自己把 Q1 營益率指引壓到 6.0–6.4%、EPS 2.46–2.62，年化 Q4 會高估；基本情境五年年化約 6%，低於 8%；成長有一大塊來自週期性的半導體設備。","ruling":"採觀望：綁定約束是估值，不是論點；論點完整，等價格。","evidence_level":"一手數字＋推算","settle_metric":"Q1 FY27 非GAAP EPS 與全年指引","if_then":["若 Q1 FY27 非GAAP EPS ≥2.62 且全年營收指引上調，基本情境 FY27 EPS 上修到 11，重啟價位由 175 上調到 190 美元","若股價先漲回 250 美元以上而 Q1 數據未到，不追"],"evidence_refs":["capital_markets_pricing#4"]},{"axis":"估值結論漂移","cause":"價格變動","prior_field":["val"],"side_a":"前份估值紅燈（股價 265.72 美元）。","side_b":"本次偏滿（股價 214.32 美元，FY27E 20.75 倍、FY28E 18.2 倍）。","ruling":"股價下跌約 19% 為主因，同期 FY27 共識財報後再上修 2.1%；只降一級到偏滿，因為 P/S 仍在三個年度端點最高、基本情境五年年化約 6%。","evidence_level":"事實表數字","settle_metric":"FY27E 本益比","if_then":["若股價 ≤175 美元而 FY27 共識不變，估值結論改為合理"],"evidence_refs":[]},{"axis":"品質與競爭方向結論","cause":"新證據","prior_field":["signal","trap","moat_trend"],"side_a":"前份：訊號等級 B、陷阱風險黃燈、護城河方向穩定。","side_b":"本次：三者結論不變。","ruling":"新證據兩面互抵：ROIC 15.8% 近十年新高、上行期仍拿份額、管理層財測大致兌現（正）；前十大客戶 49%→54%、FY26 FCF 為負、毛利率未見溢價（負）。結論維持，理由更新。","evidence_level":"一手（財報、法說、10-K）","settle_metric":"FY27 FCF、前十大客戶占比、ROIC","if_then":["若 FY27 FCF ≥1 億美元且 ROIC ≥15%，陷阱風險改為綠燈","若前十大 ≥60% 或 FCF 未達，護城河方向改判縮減並重評等級"],"evidence_refs":["ems_roic_asset_turnover_benchmark#2","customer_concentration_credit#3","competitive_share_entrants#0"]},{"axis":"前份空白欄位補齊","cause":"方法變動","prior_field":["runway_post_y5","archetype","cycle_position","max_dd_pct","p_bull_pct","p_bear_pct"],"side_a":"前份未填情境機率、最大回撤、五年後成長空間、公司類型、循環位置，也沒有定期定額結論。","side_b":"本次：情境機率多頭 25／基本 45／空頭 30；最大回撤 −37%～−55%；五年後成長空間黃燈；類型 EMS/ODM；循環位置中循環；定期定額結論由程式依本次輸入另算。","ruling":"方法變動，不是基本面改變；前份這些欄為空，沒有可比較的漂移。","evidence_level":"方法","settle_metric":null,"if_then":["若下一份判斷的循環位置改為晚循環，不建立任何部位"],"evidence_refs":[]},{"axis":"唯一致命點 Single Thing","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設唯一致命點。","side_b":"FY27 內半導體設備需求反轉，公司把全年營收成長指引由中高十位數下修到 13% 以下。","ruling":"方法變動：Single Thing 取情境樹裡對 EPS 與倍數同時影響最大的單一事件；工業部門占營收 44%、半導體設備是成長與營業槓桿的最大來源，發生即清倉。","evidence_level":"一手（分部營收、法說）","settle_metric":"FY27 營收成長指引","if_then":["若指引下修到 13% 以下，清倉並改走空頭路徑","若 FY27 全年指引維持或上調，維持基本情境"],"evidence_refs":["end_markets#3"]},{"axis":"清倉與減碼門檻","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設清倉或減碼指標。","side_b":"工業部門營收連 2 季年減；FY27 營收指引下修到 13% 以下；非GAAP營益率連 2 季 <5.8%；FY27 FCF <1 億美元；前十大客戶 ≥60% 或單一客戶 ≥10%。","ruling":"方法變動：本版每條風險配可量測門檻。指引下修到 13% 以下單項即清倉；工業部門連 2 季年減或營益率連 2 季 <5.8% 單項減碼一半；後兩項觸發則停止加碼並降品質分。","evidence_level":"方法","settle_metric":"上列五項","if_then":["任一清倉條件觸發即清倉，不等下一份判斷","減碼條件觸發後兩季內未恢復，再減碼剩餘的一半"],"evidence_refs":[]},{"axis":"重啟條件","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"前份未設重啟條件。","side_b":"股價 ≤175 美元（基本情境五年年化約 10%）且 FY27 營收成長指引未下修到 13% 以下。","ruling":"方法變動：本次觀望的綁定約束是估值（現價基本情境五年年化約 6%），重啟條件就是這個約束的否定；到價後重跑研究、分批建立首倉，之後才談加碼。","evidence_level":"推算","settle_metric":"股價、FY27 指引","if_then":["若股價 ≤175 美元且指引未下修，重跑研究後分三批建立首倉","若 Q1 FY27 優於指引上緣且全年上調，重啟價位上調到 190 美元"],"evidence_refs":[]},{"axis":"假設與風險門檻改寫","cause":"新證據","prior_field":["thesis.H","thesis.R"],"side_a":"前份：H1 FCF 率由 FY26 1.5% 升到 FY28 4% 以上（FY26 下半年 FCF 5,000 萬美元以上）；H2 非GAAP營益率 6% 以上向 7%；H3 醫療年增 12% 以上；風險為 FCF 率無法改善、醫療回落中個位數、EMS 估值均值回歸。","side_b":"本次：H1 FY27 營收 ≥57 億美元；H2 FY27 非GAAP營益率 ≥6.3% 且 ROIC ≥15%；H3 FY27 FCF ≥1 億美元；風險改為半導體設備反轉、客戶集中、關稅地緣、擴產吃現金。","ruling":"新證據：FY26 全年 FCF −2,890 萬、Q4 只有 640 萬（Q3 數字事實表未涵蓋），前份 FCF 方向未兌現，改用公司自己承諾的 1 億美元當門檻；前份營益率驗證點 FY26 6.0–6.5% 已達成（6.2%），門檻上移；醫療 FY26 +19% 已過前份門檻，但 FY27 只看高個位數，主引擎換成工業與國防；股價較前份已跌約 19%，前份估值均值回歸風險部分兌現，改由估值結論處理。","evidence_level":"一手（財報、法說）","settle_metric":"FY27 營收、營益率、FCF","if_then":["若 FY27 三項門檻有兩項未達，假設整組重寫並改判陷阱風險紅燈","若三項全達，維持論點並把重啟價位上調 10%"],"evidence_refs":["end_markets#0","ems_roic_asset_turnover_benchmark#2"]}],"triggers":[{"n":1,"text":"Q1 FY27 營收低於指引下緣","type":"假設驗證","maps_to":"H1","metric":"季營收","threshold":"<14.1 億美元","action":"H1 判削弱，重啟價位下移到 150 美元，等 Q2 再看","source_freq":"季報（每季）","date":"2027-01","evidence_refs":[]},{"n":2,"text":"工業部門營收連 2 季年減","type":"風險","maps_to":"R1","metric":"工業部門營收年增率","threshold":"連 2 季 <0%","action":"若持有減碼一半；未持有停止首倉評估","source_freq":"季報（每季）","date":null,"evidence_refs":["end_markets#3"]},{"n":3,"text":"FY27 全年營收成長指引下修到 13% 以下（半導體設備需求反轉）","type":"Single Thing","maps_to":"Single Thing","metric":"FY27 營收成長指引","threshold":"<13%","action":"清倉；未持有則至少等下修後兩季再重跑研究","source_freq":"季報與法說","date":null,"evidence_refs":["supply_demand_durability#0"]},{"n":4,"text":"股價回到 175 美元以下，且 FY27 營收指引未下修","type":"估值rearm","maps_to":"H1","metric":"股價","threshold":"≤175 美元","action":"重跑研究後分三批建立首倉","source_freq":"每日收盤","date":null,"evidence_refs":[]},{"n":5,"text":"客戶集中度越線","type":"風險","maps_to":"R2","metric":"前十大客戶營收占比","threshold":"單季 ≥60% 或年報單一客戶 ≥10%","action":"倉位上限降一級，停止加碼","source_freq":"季報、10-K","date":null,"evidence_refs":["customer_second_source#1","customer_concentration_credit#3"]},{"n":6,"text":"關稅或貿易措施吸收失敗","type":"風險","maps_to":"R3","metric":"單季毛利率","threshold":"<9.5% 且管理層歸因關稅或貿易措施","action":"減碼三分之一，H2 判削弱","source_freq":"季報（每季）","date":null,"evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","geo_supply_chain#0","geo_supply_chain#1"]},{"n":7,"text":"成長吃掉現金","type":"風險","maps_to":"R4","metric":"上半年累計 FCF 與現金循環天數","threshold":"Q2 FY27 累計 FCF <0 且現金循環 >70 天","action":"停止加碼；FY27 全年 FCF <1 億美元確認後減碼三分之一","source_freq":"季報（每季）","date":"2027-04","evidence_refs":["ems_utilization_capex_cycle#2"]},{"n":8,"text":"跌深而基本面無損","type":"加碼","maps_to":"H1","metric":"股價","threshold":"≤150 美元（約 FY28E 13 倍）且 H1–H3 無一失效","action":"分批反買，不停損","source_freq":"每日收盤","date":null,"evidence_refs":[]},{"n":9,"text":"股價先跑在 EPS 前面","type":"減碼","maps_to":"H2","metric":"FY28E 本益比","threshold":"股價 ≥300 美元而 FY28 共識未上修 10% 以上","action":"減碼三分之一","source_freq":"每日收盤、月度共識","date":null,"evidence_refs":[]},{"n":10,"text":"Q1 FY27 財報後複審","type":"複審日期","maps_to":null,"metric":"Q1 FY27 營收、營益率、航太國防季增、全年指引","threshold":null,"action":"重跑判斷","source_freq":"一次性","date":"2027-02-05","evidence_refs":[]}],"kill_metrics":[{"metric":"工業部門營收年增率（季）","bear_threshold":"連 2 季 <0%","window":"FY27–FY28","source":"公司季報分部營收表","last_status":"ok"},{"metric":"FY27 全年營收成長指引","bear_threshold":"下修到 13% 以下","window":"FY27 每季財報","source":"公司財報新聞稿與法說","last_status":"ok"},{"metric":"非GAAP營益率（季）","bear_threshold":"連 2 季 <5.8%","window":"FY27–FY28","source":"公司季報","last_status":"ok"},{"metric":"FY27 全年自由現金流","bear_threshold":"<1 億美元","window":"FY27 年底（2027-10）","source":"公司季報現金流量表","last_status":"warning"},{"metric":"前十大客戶營收占比","bear_threshold":"單季 ≥60% 或單一客戶 ≥10%","window":"FY27","source":"公司季報、10-K","last_status":"warning"}],"action_conditions":{"rearm_trigger":"股價 ≤175 美元（基本情境五年年化約 10%）且 FY27 營收成長指引未下修到 13% 以下","exec_line":"現價觀望不追，綁定約束是估值；股價 ≤175 美元且 FY27 營收指引未下修時重跑研究，首倉分三批；跌破 150 美元而 H1–H3 無失效則分批反買，不設停損；唯一致命點發生則清倉。","holding_cap":null}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":"中循環","cycle_verdict":"等回踩","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":false,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"股價回到 175 美元以下（基本情境五年年化約 10%），且 FY27 營收成長指引未下修到 13% 以下","qc48_result":null,"qc48_note":null,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null},"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='C'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟠', moat_trend='→', week26=-18.37, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='EMS/ODM', cycle_position='中循環', moat='C', moat_trend='→', cycle_gates_pass=False"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":true,"basis":"signal='B', val='🟠'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":false,"basis":"signal='B', val='🟠', ma='🟡'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟠', ma='🟡'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟠', ma='🟡'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":null,"requires_critic":[]},"thesis":{"H":[{"id":"H1","text":"FY27 營收照新指引成長中高十位數，由航太國防與工業各 >20% 帶動，不是只靠半導體設備。","2y":"FY27 營收 ≥57 億美元（FY26 49.65 億 × 1.15）","5y":"FY31 營收 ≥75 億美元（FY28 共識 64 億後每年約 6% 以上）","10y":null,"threshold":"FY27 營收 ≥57 億美元，且航太國防與工業至少一個年增 >20%","source":"公司季報新聞稿分部營收表、法說會指引","drift_rule":"以 TTM 營收對照年度路徑：連 2 季落後 ≥5% 判削弱，連 3 季落後 ≥10% 判反轉"},{"id":"H2","text":"營收槓桿與自動化效率讓非GAAP營益率走向公司新目標 6.5–7%，ROIC 守在 15% 以上。","2y":"FY27 非GAAP營益率 ≥6.3%、ROIC ≥15%","5y":"FY29–FY31 非GAAP營益率平均落在 6.5–7%","10y":null,"threshold":"FY27 非GAAP營益率 ≥6.3%；任一季 <5.8% 為警訊","source":"公司季報非GAAP營益率與 ROIC 揭露","drift_rule":"5 年論點：營益率較路徑連 4 季偏離 ≥5%（約 0.3 個百分點）判削弱，連 6 季偏離 ≥10% 判反轉"},{"id":"H3","text":"成長期也能把利潤轉成現金：營運資金效率維持，FY27 自由現金流超過 1 億美元。","2y":"FY27 FCF >1 億美元、年底現金循環 60–65 天","5y":"FY28–FY31 FCF 對淨利轉換 ≥0.75","10y":null,"threshold":"FY27 FCF ≥1 億美元；現金循環 ≤68 天（Q1 季節性 66–70 天除外）","source":"公司季報現金流量表與現金循環天數","drift_rule":"2 年論點：累計 FCF 對年度路徑連 2 季落後 ≥5% 判削弱、連 3 季 ≥10% 判反轉；Q1 管理層已預告用現金，不計入"}],"R":[{"id":"R1","text":"半導體設備週期反轉，工業部門由高成長轉為衰退，營業槓桿反向。","h_ref":"H1","clock":"🔥","threshold":"工業部門營收連 2 季年減，或 FY27 營收指引下修到 13% 以下","evidence_refs":["end_markets#3","supply_demand_durability#0"]},{"id":"R2","text":"客戶集中度持續上升，任一大客戶轉單、自製或砍單的衝擊被放大。","h_ref":"H1","clock":"🔥","threshold":"前十大客戶單季占比 ≥60%，或年報出現單一客戶 ≥10%","evidence_refs":["customer_second_source#1","customer_concentration_credit#0","customer_concentration_credit#2","customer_concentration_credit#3"]},{"id":"R3","text":"關稅、出口管制或墨西哥 IMMEX 規則改變，成本無法轉嫁，吃掉營益率擴張空間。","h_ref":"H2","clock":"🐢","threshold":"單季毛利率 <9.5% 且管理層歸因關稅或貿易措施","evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","geo_supply_chain#0","geo_supply_chain#1"]},{"id":"R4","text":"擴產與營運資金投入跑在獲利前面：檳城新廠稼動不足、FY27 FCF 不到 1 億美元，ROIC 跌回 15% 以下。","h_ref":"H3","clock":"⚡","threshold":"Q2 FY27 累計 FCF 仍為負且現金循環 >70 天，或單季 ROIC <14%","evidence_refs":["ems_utilization_capex_cycle#2"]}],"single_thing":{"description":"FY27 內半導體設備需求反轉，公司把全年營收成長指引由中高十位數下修到 13% 以下。","why_fatal":"工業部門占營收 44%，FY26 半導體設備 +50% 是成長與營業槓桿的最大來源；營益率目標靠營收槓桿（增量營益率 8–12%）達成，營收一轉弱，槓桿反向，FY28 EPS 由共識 11.79 掉到空頭路徑約 9，倍數同時壓到 13–15 倍，是情境樹裡對股價影響最大的單一項。","if_happens":"改走空頭路徑，價位約 117–135 美元；持有則清倉，未持有則至少等下修後兩季、確認工業部門止跌再重跑研究。","how_monitor":"每季工業部門營收與管理層對半導體設備的曆年展望；北美 EMS 月度 book-to-bill（跌破 1 為預警）；FY27 營收成長指引。","probability":"約 20%（12–24 個月）：管理層對 FY27 有約一年能見度、產業預測仍在上修，但半導體設備屬週期且已連續高成長。"}},"appendix_a":{"growth_durability":6,"quality_score":6,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":18.18,"peg_fy2":1.29,"stress":{"pass":2,"total":3}},"eps_meta":{"base_eps_path":{"FY2026A":9.1,"FY2027E":10.33,"FY2028E":11.79,"FY2029E":null},"fy_end_month":9,"eps_basis":"非GAAP 稀釋 EPS；財年在 9 月底至 10 月初結束（FY26 季末 2026-10-03）。FY2026A 9.10 為推算：Chartmill 2026-10-18 的 FY26 共識 8.87 內含 Q4 預估 2.61，換成實際 Q4 非GAAP EPS 2.84（2026-10-29 法說），不是公司公布的全年數。FY2029E 共識事實表未涵蓋（只有兩個年度）。"},"catalysts":[{"date":"2026-11","date_precision":"month","type":"other","event":"FY2026 10-K 申報","impact":"中","watch":"前十大客戶占比、是否出現單一客戶 ≥10%、馬來西亞集中與 IMMEX 風險描述是否改寫"},{"date":"2026-11","date_precision":"month","type":"other","event":"Baird 工業論壇（11-11）","impact":"低","watch":"管理層對半導體設備能見度與 FY27 指引的說法是否改變"},{"date":"2027-01","date_precision":"month","type":"guidance","event":"Q1 FY2027 財報（季末 2027-01-02）","impact":"高","watch":"營收是否落在 14.1–14.6 億美元、非GAAP營益率 6.0–6.4%、航太國防季增是否 ≥8%、FY27 全年指引"},{"date":"2027-04","date_precision":"month","type":"guidance","event":"Q2 FY2027 財報","impact":"中","watch":"營益率是否如 CFO 所說季節性不降、上半年累計 FCF、現金循環天數"}]}
```

---

## ⑤ 覆蓋面（程式判定，你回的 ⑤ 燈號會被覆寫）

燈號 🟡：非核心軸無證據：regulatory_antitrust（法規／反壟斷）（尾部風險或事件型，不擋）。

⑤ 的 reason 只需評論：空軸的查詢詞是否切題、判斷有沒有交代缺口對結論的影響。

---

## 尾段：回覆格式

只回一個 JSON 陣列，①–⑧ 每條一個元素，八個全出，不得跳號、不得多列，陣列外不得有任何文字（不加前言、不加 markdown 圍欄、不加附註）：

```json
[{"item": "①", "light": "🔴|🟡|🟢", "judgment_path": "$.路徑", "reason": "一句話"}]
```
