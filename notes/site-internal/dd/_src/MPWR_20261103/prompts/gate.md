你是 DD 管線 v20 的判斷層閘（gate），標的 MPWR（20261103）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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
- `f_kpi0_revenue_gaap`（q1_business）｜Revenue (GAAP)＝1202.4 USD M｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001280452/000162828026068202/mpwr-20260930xexx991.htm（numbers.latest_quarter_kpis.items[0]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-29））
- `f_kpi1_non_gaap_operating_incom`（q1_business）｜Non-GAAP operating income＝464.5 USD M｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001280452/000162828026068202/mpwr-20260930xexx991.htm（numbers.latest_quarter_kpis.items[1]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-29））
- `f_kpi2_non_gaap_operating_margi`（q1_business）｜Non-GAAP operating margin＝38.6 %｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001280452/000162828026068202/mpwr-20260930xexx991.htm（numbers.latest_quarter_kpis.items[2]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-29））
- `f_kpi3_gaap_operating_income`（q1_business）｜GAAP operating income＝357.7 USD M｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001280452/000162828026068202/mpwr-20260930xexx991.htm（numbers.latest_quarter_kpis.items[3]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-29））
- `f_kpi4_gaap_operating_margin`（q1_business）｜GAAP operating margin＝29.7 %｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001280452/000162828026068202/mpwr-20260930xexx991.htm（numbers.latest_quarter_kpis.items[4]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-29））
- `f_kpi5_sbc_and_related_expenses`（q4_capital）｜SBC and related expenses＝106.3 USD M｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001280452/000162828026068202/mpwr-20260930xexx991.htm（numbers.latest_quarter_kpis.items[5]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-29））
- `f_kpi9_inventory_days`（q1_business）｜Inventory days（以當季營收計）＝130 days｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001280452/000162828026068202/mpwr-20260930xexx991.htm（numbers.latest_quarter_kpis.items[9]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-29））
- `f_kpi10_q4_fy2026_guidance_reven`（q1_business）｜Q4 FY2026 guidance: revenue＝1315～1385 USD M｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司 Q3 2026 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001280452/000162828026068202/mpwr-20260930xexx991.htm（numbers.latest_quarter_kpis.items[10]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-29））
- `f_peer_mpwr_gross_margin_pct`（q2_moat）｜MPWR 毛利率＝55.22 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MPWR.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_mpwr_operating_margin_pct`（q2_moat）｜MPWR 營業利益率＝29.38 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MPWR.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_mpwr_fcf_margin_pct`（q2_moat）｜MPWR FCF 利潤率＝15.31 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MPWR.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_adi_gross_margin_pct`（q2_moat）｜ADI 毛利率＝65.8 %｜期間與口徑：TTM ending 2026-07-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ADI.gross_margin_pct，as_of TTM ending 2026-07-31（4季加總））
- `f_peer_adi_operating_margin_pct`（q2_moat）｜ADI 營業利益率＝35.72 %｜期間與口徑：TTM ending 2026-07-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ADI.operating_margin_pct，as_of TTM ending 2026-07-31（4季加總））
- `f_peer_adi_fcf_margin_pct`（q2_moat）｜ADI FCF 利潤率＝35.57 %｜期間與口徑：TTM ending 2026-07-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.ADI.fcf_margin_pct，as_of TTM ending 2026-07-31（4季加總））
- `f_peer_txn_gross_margin_pct`（q2_moat）｜TXN 毛利率＝60.24 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.TXN.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_txn_operating_margin_pct`（q2_moat）｜TXN 營業利益率＝41.12 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.TXN.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_txn_fcf_margin_pct`（q2_moat）｜TXN FCF 利潤率＝35.24 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.TXN.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_vicr_gross_margin_pct`（q2_moat）｜VICR 毛利率＝60.57 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.VICR.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_vicr_operating_margin_pct`（q2_moat）｜VICR 營業利益率＝24.9 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.VICR.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_vicr_fcf_margin_pct`（q2_moat）｜VICR FCF 利潤率＝9.07 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.VICR.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_ifx_de_gross_margin_pct`（q2_moat）｜IFX.DE 毛利率＝39.42 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.IFX.DE.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_ifx_de_operating_margin_pct`（q2_moat）｜IFX.DE 營業利益率＝14.9 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.IFX.DE.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝-1091.23 USD m｜期間與口徑：2026-11-03／yfinance 最新一季：總債務 0.0、現金 1091.23（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝27.55 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-10-31）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝35.27 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-10-31）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝41.1 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-10-31）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝4335.75 USD m｜期間與口徑：2026-11-03／yfinance revenue_estimate 0y 平均（15 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝6425.61 USD m｜期間與口徑：2026-11-03／yfinance revenue_estimate +1y 平均（16 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi8_non_gaap_diluted_eps`（q1_business）｜Non-GAAP diluted EPS＝8.19 USD｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001280452/000162828026068202/mpwr-20260930xexx991.htm（numbers.latest_quarter_kpis.items[8]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-29））
- `f_kpi6_operating_cash_flow`（q1_business）｜Operating cash flow＝289.9 USD M｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001280452/000162828026068202/mpwr-20260930xexx991.htm（numbers.latest_quarter_kpis.items[6]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-29））
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝0.583 %｜期間與口徑：2026-11-03／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-11-03）
- `f_ev_m`（q5_valuation）｜目前企業價值 EV（市值＋淨負債）＝62115.39 USD m｜期間與口徑：2026-11-03／市值 63206.62 ＋ 淨負債 -1091.23｜kind：realized
  - 來源：—（numbers.capital_structure.ev_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝48.79 m shares｜期間與口徑：2026-11-03／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝1296.22 USD｜期間與口徑：2026-11-02（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-11-02（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝47.02 x｜期間與口徑：2026-10-31／分母＝FY1 EPS 27.55，分子＝快照價 1295.43｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-10-31）
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝71.02 x｜期間與口徑：2026-11-02（RTH 收盤，UTC）／4 個年度端點內的分位＝96.4｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-11-02（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝96.4 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝16.91 x｜期間與口徑：2026-11-02（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝100.0 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝16.62 x｜期間與口徑：2026-11-02（RTH 收盤，UTC）／4 個年度端點內的分位＝100.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ev_s_fwd`（q5_valuation）｜EV/S（EV ÷ FY1 共識營收）＝14.33 x｜期間與口徑：2026-11-03／f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）｜kind：estimate
  - 來源：—（numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝13.98 %｜期間與口徑：2026-07-30 → 2026-10-31／FY1 共識 EPS 24.17 → 27.55（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-10-31）
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝-17.34 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-11-02（RTH 收盤，UTC））
- `f_rsi14`（q5_valuation）｜RSI(14)＝53.74｜期間與口徑：2026-11-02（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ma_state`（q5_valuation）｜週線均線六態（decision_inputs.ma 必須等於此值）＝🟡｜期間與口徑：2026-11-03／timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）
  - 原文：「price 1271.73 / W52 1241.74 / W104 972.4 / W250 719.04 / W250 13週斜率 1.77%」
- `f_kpi7_gaap_diluted_eps`（q1_business）｜GAAP diluted EPS＝5.51 USD｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0001280452/000162828026068202/mpwr-20260930xexx991.htm（numbers.latest_quarter_kpis.items[7]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-29））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝100.0 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-11-02（RTH 收盤，UTC））

### findings_digest 中方向為負或來源衝突的條目（17 條）
- `competitive_share_entrants#1`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K 風險因素：對手規模與資源多數大於公司，且因公司為 fabless 不適用 CHIPS Act 補助，對手藉補助擴產、縮短交期並取得份額。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-27）｜affects：moat_trend、thesis.R、decision_inputs.bear
- `competitive_share_entrants#2`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K 風險因素：競爭者數量因公司所處細分市場擴張而增加，公司承認無法保證產品持續勝出。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-27）｜affects：moat_trend、thesis.R
- `competitive_share_entrants#3`（competitive_share_entrants｜方向 -｜狀態 ok）：CSIMarket 稱 MPWR 在 Q2 2026 於某區隔份額下滑（儘管整體營收成長 47.68%），區隔與方法論不明。
  - 來源：CSIMarket MPWR Competitors（as_of 2026-08-01）｜affects：moat_trend
- `customer_second_source#0`（customer_second_source｜方向 -｜狀態 ok）：10-K 風險因子：公司可能面臨客戶內部自行開發產品的競爭，且未來銷售前景取決於客戶接受第三方供應來源取代自製；客戶可能增加自製元件使用。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A Risk Factors（as_of 2026-02-27）｜affects：decision_inputs.bear、moat_trend
- `customer_second_source#1`（customer_second_source｜方向 -｜狀態 ok）：10-K 載明公司與 OEM/ODM 客戶無採購承諾，即使取得 design win 也不保證客戶持續採用其 IC。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A Risk Factors（as_of 2026-02-27）｜affects：decision_inputs.bear、moat_trend
- `customer_second_source#3`（customer_second_source｜方向 -｜狀態 ok）：Edgewater 稱 MPWR VRM 效能問題可能大幅限縮或消除其 Nvidia Blackwell 配額，Renesas 與 Infineon 被視為取得 B200/GB200 配額。
  - 來源：TipRanks/The Fly: Monolithic Power slides as Edgewater says allocation in Blackwell at risk（as_of 2025-06-01）｜affects：decision_inputs.bear、moat_trend
- `customer_concentration_credit#0`（customer_concentration_credit｜方向 -｜狀態 ok）：FY2025 三大客戶（皆為經銷商）占營收 26%、18%、10%；2024 年兩家占 31%、20%；2023 年三家占 26%、19%、10%。
  - 來源：SEC EDGAR 10-K FY2025 Item 1 Business（as_of 2026-02-27）｜affects：decision_inputs.bear、thesis.R
- `customer_concentration_credit#1`（customer_concentration_credit｜方向 -｜狀態 ok）：前三大客戶（皆經銷商）合計占營收 2025 年 54%、2024 年 61%、2023 年 55%；10-K 風險因子明載集中度提高對其信用狀況、庫存作法的曝險。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A Risk Factors（as_of 2026-02-27）｜affects：decision_inputs.bear、thesis.R
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：MPWR 10-K FY2025：2025 年營收 92% 來自亞洲客戶，風險因子列明貿易法規變動、出口許可、關稅與中美報復性關稅風險。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-27）｜affects：decision_inputs.bear、thesis.R
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：FY2025 10-K風險因子列出中國生產營運風險、美中關稅與出口管制、台灣與香港緊張局勢，以及倚賴中國關鍵供應商之產能短缺風險
  - 來源：MPWR Form 10-K FY2025 (SEC)（as_of 2026-02-27）｜affects：thesis.R、decision_inputs.bear
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：10-K FY2025 風險因子：客戶可能自行開發或收購與本公司產品類似或可替代的元件／技術，對業務與經營結果構成重大不利影響；未列出特定新興替代技術。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-27）｜affects：moat_trend、thesis.R
- `substitute_technology#1`（substitute_technology｜方向 -｜狀態 ok）：10-K FY2025 Item 1：公司預期現有競爭者及新進者持續競爭，不保證產品持續具競爭力。
  - 來源：SEC EDGAR 10-K FY2025 Item 1（as_of 2026-02-27）｜affects：moat_trend
- `major_events#0`（major_events｜方向 -｜狀態 ok）：2025-02-04 證券集體訴訟（Waterford Twp. v. MPWR, W.D. Wash.）指控公司與高管違反 10(b)/20(a)；衍生訴訟已合併並暫停；公司稱訴訟無理由。
  - 來源：SEC EDGAR 10-K FY2025 Item 3（as_of 2026-02-27）｜affects：decision_inputs.bear、thesis.R
- `major_events#1`（major_events｜方向 -｜狀態 ok）：2026-02-26 審計委員會判定 FY2024 10-K 與 2025 各季 10-Q 不可再信賴並重編（外國租稅優惠遞延所得稅處理錯誤）；8-K Item 4.02 於 2026-02-27 申報。
  - 來源：SEC EDGAR 8-K Item 4.02（as_of 2026-02-27）｜affects：decision_inputs.bear、thesis.R
- `lawsuit_class_action#0`（lawsuit_class_action｜方向 -｜狀態 ok）：2025-02-04 證券集體訴訟與兩件衍生訴訟（已合併為 Miller v. Hsing，暫停）。
  - 來源：SEC EDGAR 10-K FY2025 Item 3（as_of 2026-02-27）｜affects：decision_inputs.bear、thesis.R
- `sec_investigation_restatement#0`（sec_investigation_restatement｜方向 -｜狀態 ok）：2026-02-27 8-K Item 4.02：FY2024 與 2025 各季財報重編；搜尋結果未見 SEC 調查。
  - 來源：SEC EDGAR 8-K Item 4.02（as_of 2026-02-27）｜affects：decision_inputs.bear、thesis.R
- `sec_investigation_restatement#1`（sec_investigation_restatement｜方向 -｜狀態 ok）：10-K 風險因子指出重編原因為外國一次性租稅優惠的遞延所得稅處理不當，並提示訴訟與監管詢問風險升高。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-27）｜affects：decision_inputs.bear、thesis.R

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 6 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MPWR_20261103/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":3344,"bear_5y_price":660,"p_bull_pct":25,"p_bear_pct":30,"upside_5y_pct":43.5,"ev5y_pct":44.3,"irr_base_pct":7.5,"asym_ratio":2.7,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":27.55,"pe":47.05,"basis":"FY2026E 非 GAAP 共識 EPS（已過三季加 Q4 指引，接近實現）；終端倍數同樣套在終端年當年非 GAAP EPS"},"eps":{"bull":[46,55,66,77,88],"base":[40,44,50,56,62],"bear":[33,26,27,30,33]},"pe":{"bull":38,"base":30,"bear":20},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0.583,"net_buyback":0.4},"second_stage":{"bull_cagr_pct":14,"base_cagr_pct":10},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### MPWR_Q2_2026_Earnings_Call_20260730.md
- 2026-07-30｜Tony Balow｜guidance：Enterprise Data 全年下限由 85% 上調至 130%（管理層用語 raise the floor）（原話："willing to raise the floor for that particular end market"）
- 2026-07-30｜Tony Balow｜guidance：Q2 營收創單季新高 $981M（原話："record quarterly revenue of $981 million"）
- 2026-07-30｜Tony Balow｜guidance：Enterprise Data 單季成長 45%（原話："with Enterprise Data growing 45%"）
- 2026-07-30｜Tony Balow｜guidance：Auto 全年預期年增約中段十幾%（原話："could be in the mid-teens kind of year-over-year."）
- 2026-07-30｜Tony Balow｜guidance：Auto 上半年持平、下半年爬坡的說法延續（原話："we thought the first half would be flat"）
- 2026-07-30｜Tony Balow｜guidance：RCD 不會是 2026 年營收的關鍵（原話："that's not going to be a needle-mover in 2026 for"）
- 2026-07-30｜Robert Dean｜margin：Rob 稱強勁訂單讓毛利率指引小幅上調（原話："incrementally expand our guidance"）
- 2026-07-30｜Robert Dean｜margin：毛利率仍在目標區間低端，但對 Q3 有信心（原話："but we're feeling comfortable about where we're at for Q3."）
- 2026-07-30｜Michael R. Hsing｜margin：Hsing 稱毛利率仍在模型內但在低端（原話："we're still in the model, although in the low end"）
- 2026-07-30｜Michael R. Hsing｜margin：Hsing 稱近期毛利率大致持平或略高（原話："in the near future, we'll probably stay similar or"）
- 2026-07-30｜Tony Balow｜margin：Tony 說明營收提高後費用難以同步擴張，帶來營業利益率槓桿（原話："difficult to keep the levels of spending up to that model"）
- 2026-07-30｜Tony Balow｜margin：Tony 說明漲價的三類情境之一，與維持毛利有關（原話："We have raised some prices, but it's primarily"）
- 2026-07-30｜Michael R. Hsing｜margin：Hsing 否認本季成長來自漲價（原話："gouges prices when the supply chain is tight."）
- 2026-07-30｜Tony Balow｜commitment：宣布增加 $500M 庫藏股授權，總額 $1B（原話："additional $500 million for stock repurchases"）
- 2026-07-30｜Tony Balow｜commitment：產能目標擴大至遠超 $6B（原話："extended our capacity goals significantly beyond $6 billion"）
- 2026-07-30｜Michael R. Hsing｜commitment：Hsing 稱提到的新事業歷來都會變成營收（原話："when we mention something, it will turn into a revenue."）
- 2026-07-30｜Michael R. Hsing｜commitment：Hsing 稱 RCD 有信心轉成營收（原話："we're confident that it will be turning to a revenue"）
- 2026-07-30｜Michael R. Hsing｜commitment：Hsing 稱建築控制軟體預計今年底前完成（原話："we should be able to complete it, complete everything"）
- 2026-07-30｜Michael R. Hsing｜commitment：Hsing 稱持續追求穩定成長（原話："investors a very consistent way of growing MPS."）
- 2026-07-30｜Tony Balow｜product：DDR5 記憶體元件取得初期訂單，預期擴大 SAM（原話："which we expect to grow our SAM into next year."）
- 2026-07-30｜Tony Balow｜product：DDR5 營收爬坡時點管理層不給（原話："early for us to call any kind of revenue ramp on our side."）
- 2026-07-30｜Tony Balow｜product：開始送樣 800V 資料中心高壓 AC-DC 產品（原話："We began sampling high-voltage AC to DC products"）
- 2026-07-30｜Michael R. Hsing｜product：800V 方案營收時點管理層不給（原話："when, we don't know -- we know as much as you know."）
- 2026-07-30｜Michael R. Hsing｜product：Hsing 承認先前不看好 GaN，現已自研（原話："I openly say I don't believe GaN"）
- 2026-07-30｜Michael R. Hsing｜product：48V 垂直電源模組客戶超過兩家（原話："Well, it's more than a couple of customers."）
- 2026-07-30｜Tony Balow｜product：Tony 說明 Comms 成長來自光模組與交換器兩塊，光模組較大（原話："the bigger portion just because it's had a longer runway"）
- 2026-07-30｜Michael R. Hsing｜product：建築自動化軟體尚落後（原話："we're still lagging of the software."）
- 2026-07-30｜Michael R. Hsing｜product：Hsing 稱建築自動化市場規模 $40–50B（原話："it's about $40 billion to $50 billion."）
- 2026-07-30｜Tony Balow｜product：Tony 稱模組後段製程更複雜（原話："a more complicated back-end process as well."）
- 2026-07-30｜Tony Balow｜customer：Auto 今年已出貨超過 1,500 個新 socket（原話："we have shipped products for over 1,500 new sockets"）
- 2026-07-30｜Tony Balow｜customer：Enterprise Data 通路庫存仍很低（原話："that remains very low, so we believe that's continuing"）
- 2026-07-30｜Tony Balow｜customer：book-to-bill 本輪週期明顯大於 1（原話："cycle was again well above 1."）
- 2026-07-30｜Tony Balow｜customer：2027 年數字管理層不給（原話："it's too early to put a number on it."）
- 2026-07-30｜Michael R. Hsing｜customer：Hsing 稱不把貨硬塞給客戶，雖有 NCNR（原話："even though we have NCNR"）
- 2026-07-30｜Michael R. Hsing｜customer：Hsing 稱 CPU 市占已超過自設 30% 門檻（原話："we're comfortable there now. We're past that."）
- 2026-07-30｜Tony Balow｜customer：Tony 稱難以區分純 AI 與 CPU 銷售（原話："separate sometimes a pure AI sale from a CPU sale"）
- 2026-07-30｜Tony Balow｜customer：Tony 稱 ED 以外業務去年 Q2 雙位數成長（原話："the rest of the businesses saw double-digit"）
- 2026-07-30｜Tony Balow｜customer：Tony 稱資料中心相關曝險未細分儲存與筆電（原話："we haven't broken out Storage and Compute versus notebook"）
- 2026-07-30｜Michael R. Hsing｜competition：Hsing 稱功率密度全球最高（原話："we're the highest power density company in the world now"）
- 2026-07-30｜Tony Balow｜competition：Tony 稱光模組市占不給確切數字（原話："quote the exact percentage of share at this time."）
- 2026-07-30｜Tony Balow｜competition：Tony 稱 Comms 仍有成長空間（原話："there's still room for us to grow."）
- 2026-07-30｜Michael R. Hsing｜risk：Industrial 偏弱（原話："Industrial is kind of lagging a little bit"）
- 2026-07-30｜Tony Balow｜risk：Tony 對 Consumer 與筆電端儲存/運算持謹慎（原話："Compute, we'll continue to remain cautious on that one"）
- 2026-07-30｜Tony Balow｜risk：Industrial 今年定位為設計導入年（原話："we've primarily said that's a design win"）
- 2026-07-30｜Michael R. Hsing｜capital_allocation：新增產能多在既有節點（原話："I think it's mostly the existing."）
- 2026-07-30｜Michael R. Hsing｜capital_allocation：產能地理分布比重尚難估計（原話："what is the percentage in the end, it's hard."）
- 2026-07-30｜Tony Balow｜capital_allocation：持續擴充並分散全球供應鏈（原話："continuously expand and diversify our global supply chain"）

### MPWR_Shareholder_Analyst_Call_Monolithic_Power_Systems_Inc_20260611.md
- 2026-06-11｜Saria Tseng｜commitment：股東會議程：提名兩位董事（Victor Lee、Jeff Zhou）任期至 2029 年股東會（純程序性陳述，非財務承諾）（原話："nominated by the Board of Directors, Victor Lee"）
- 2026-06-11｜Saria Tseng｜commitment：兩位董事獲連任（原話："Both directors are reelected."）
- 2026-06-11｜Saria Tseng｜risk：董事會指派 Ernst & Young 審計 2026 會計年度財報，交付股東追認（治理程序）（原話："appointed Ernst & Young independent auditors to audit"）
- 2026-06-11｜Saria Tseng｜risk：會計師追認案獲 4,540 萬股贊成（原話："45.4
million shares were in favor of the appointment."）
- 2026-06-11｜Saria Tseng｜risk：薪酬諮詢投票（say-on-pay）通過，4,220 萬股贊成（出席 4,540 萬股）（原話："The executive compensation is approved."）
- 2026-06-11｜Saria Tseng｜risk：Jeff Zhou 獲 4,110 萬股贊成（同場 Victor Lee 為 3,930 萬股）（原話："41.1 million shares were in favor of the appointment"）
- 2026-06-11｜Saria Tseng｜risk：出席股數 4,540 萬股，占記錄日流通股 92%（原話："comprising
92% of the outstanding common stock"）
- 2026-06-11｜Unknown Executive｜risk：開放提問時無人提問（原話："Saria, there's no question."）

### 問答異常語氣（迴避／改口／保留）
- MPWR_Q2_2026_Earnings_Call_20260730.md｜問：Buchalter 問 ED 有無庫存堆積與可見度｜答法：Hsing 先談過去工業缺貨，未直接回答庫存；Tony 補上通路庫存低與上調下限
- MPWR_Q2_2026_Earnings_Call_20260730.md｜問：Buchalter 問 DDR5 控制器 SAM 擴大幅度｜答法：Tony 稱太早、不給營收爬坡數字
- MPWR_Q2_2026_Earnings_Call_20260730.md｜問：Svanberg 問 800V 營收時點｜答法：Hsing 稱不知道，由資料中心轉換時點決定
- MPWR_Q2_2026_Earnings_Call_20260730.md｜問：Bolton 問光模組市占與競爭對手｜答法：Hsing 改談功率密度；Tony 不給市占百分比
- MPWR_Q2_2026_Earnings_Call_20260730.md｜問：Bolton 問新增產能中國與非中國比重｜答法：Hsing 稱尚未定、難估；Tony 改談後段製程
- MPWR_Q2_2026_Earnings_Call_20260730.md｜問：Chia 問 ED 2027 展望｜答法：Tony 稱 2027 太遠不給數字；Hsing 補述不推貨給客戶

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 4 | 4 |
| customer_second_source | found | 4 | 2 |
| customer_concentration_credit | found | 2 | 1 |
| supply_demand_durability | found | 6 | 4 |
| regulatory_antitrust | found | 2 | 1 |
| reg_tariff_export | found | 3 | 2 |
| geo_supply_chain | found | 2 | 2 |
| end_markets | found | 3 | 4 |
| substitute_technology | found | 3 | 2 |
| channel_business_model_shift | found | 2 | 2 |
| capital_markets_pricing | found | 6 | 4 |
| major_events | found | 3 | 3 |

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260731","verdict":"進場","role":"衛星","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"企業數據段的成長是「分散客戶 × 內容價值躍升」的結構性成長，不是單一 socket 押注"},{"id":"H2","text":"模組化（chip → semiconductor-based solution）提升每個 socket 的內容價值，且不以毛利率為代價"},{"id":"H3","text":"市場願意為「EPS 從 $27.51 複利到 $68」付出 30x 以上的終端倍數，倍數壓縮幅度不超過 47.4x → 32x"}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"旗艦 AI 插槽二度失守：繼 Blackwell B200／GB200 主要配額落入 Infineon（60–70%）與 Renesas 之後，Vera Rubin（VR200）再度失守。"},{"id":"R2","text":"AI capex 消化期：企業數據段 +164% 的年增基期在 2027 變成高基期，若 hyperscaler capex 增速由 +100% 降到 +20%，本段成長可能一次掉到個位數，且 TAM 遮羞布撤走後暴露真實份額。"},{"id":"R3","text":"定價權自願放棄的長期代價：管理層政策性不趁緊俏漲價，加上模組化把電感、電容等外購料帶進成本結構，毛利率由 58.4%（2022）走到 55.2%（2025），若續探則「高毛利無晶圓廠類比 IC」的估值框架不再適用。"},{"id":"R4","text":"同業溢價收斂：本檔 Fwd PE 47.4x 相對同 tier 中位 25.6x 溢價 +85%，遠超 50% 門檻。若對手（TXN／ADI）在 AI 電源上補上、或本檔成長率向同業靠攏，溢價收斂本身即可造成 −23% 的價格衝擊（§11.4 情境 B），與基本面惡化無關。疊加 headline 脆弱性：本檔對「NVIDIA 插槽份額」類新聞極度敏感，過去一年曾因單一 sell-side 份額傳言單日重挫近 9–10%，re-rate 可在無財報的情況下被消息面逆轉。"}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"已建 starter 1/2；加碼觸發＝Rubin VR200 插槽定案，或企業數據單季 YoY ≥+80% 連兩季","irr_base_pct":9.2,"ev5y_pct":54.7,"drift_watch_prior":{"dca_verdict":"進場","dca_role":"衛星","signal":"A","val":"🟡","ma":"✅","trap":"🟢","moat_trend":"→","runway_post_y5":"🟢","asym_ratio":4.3,"ev5y_pct":54.7,"irr_base_pct":9.2,"max_dd_pct":-60.0,"bull_5y_price":3458.0,"bear_5y_price":889.0,"p_bull_pct":30.0,"p_bear_pct":25.0,"rearm_trigger":"已建 starter 1/2；加碼觸發＝Rubin VR200 插槽定案，或企業數據單季 YoY ≥+80% 連兩季","price_at_dd":1450.0,"archetype":"品質複利成長","cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"MPWR","date":"2026-11-03","schema":"v15.0","contract":"v19","company_name":"Monolithic Power Systems"},"oneliner":"AI 資料中心電源模組放量，Q3 營收年增 63%、非 GAAP 營益率升到 38.6%；現價約 FY2026 共識 47 倍、FY2027 約 37 倍，已計入高成長，回檔才加、不追價；最大風險是旗艦平台供電份額被分走，以及 2028 年擴產後的需求回落","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MPWR_20261103/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/MPWR_20261103/scenario.json","answers":{"q1_business":{"verdict":"賺 AI 加速器、網通與車用客戶的電源轉換錢：無晶圓廠設計高密度電源 IC 與模組，經經銷商出貨，錢卡在旗艦平台供電插槽的設計導入與代工產能","reasoning":"Q3 營收 12.02 億美元（季增 22%、年增 63%），分市場：企業數據 5.07 億（占 42.1%，年增 164.6%）、儲存與運算 1.92 億（年增 3.0%）、通訊 1.87 億（年增 134.7%）、車用 1.81 億（占 15.0%，年增 19.2%）、工業 0.71 億（年增 29.0%）、消費 0.64 億（年減 11.6%）。非 GAAP 營益率 38.6%、GAAP 29.7%，兩者差額 1.07 億幾乎等於 SBC 1.063 億；最新一季毛利率事實表未涵蓋，TTM 55.2%，管理層稱 Q3 季增 10bps、Q4 指引中值再加 10bps。Q4 營收指引 13.15～13.85 億。單點依賴：企業數據占四成以上且集中在少數 GPU／ASIC 平台（各平台占比事實表未涵蓋）；2025 年前兩大經銷商合計 44%、前三大 54%，公司與 OEM／ODM 無採購承諾。產業時鐘在擴張期：營收加速、book-to-bill 高於 1、通路庫存在 5～8 週區間低端、公司存貨天數隨營收放大而下降、產能由 60 億擴到 2027 下半年 80 億。供需：需求端屬結構性（功率上升逼出模組化與垂直供電），但當前增速含 AI 資本支出的週期成分；供給端可逆性高，公司自己與受 CHIPS 補助的同業都在擴產，2028 年起供過於求的機率要計入 Bear。產業態勢三軸：競爭軸惡化中（補助擴產、旗艦平台多供應商、整合式穩壓新對手）；結構軸轉好中（模組含量、48V／800V、光模組 1.6T，第三方預估缺貨延續至 2027）；其他軸有關稅、出口管制與通路集中；裁決為雙向拉鋸。","fact_refs":["f_kpi0_revenue_gaap","f_kpi1_non_gaap_operating_incom","f_kpi2_non_gaap_operating_margi","f_kpi3_gaap_operating_income","f_kpi4_gaap_operating_margin","f_kpi5_sbc_and_related_expenses","f_kpi9_inventory_days","f_kpi10_q4_fy2026_guidance_reven","f_peer_mpwr_gross_margin_pct"],"verdict_values":{"revenue_quality":"量驅動為主：管理層稱漲價不是成長的顯著來源，只用來守毛利率；成長來自客戶擴散、模組含量提升與新平台。約 88% 經經銷商（二手摘要，未對公司文件核實），2025 年前三大經銷商占 54%，營收能見度依賴通路庫存紀律","unit_econ_note":"Q3 非 GAAP 營益率 38.6%，管理層稱營益率近乎每季升 1 個百分點；毛利率模型 55～60%，每季擴 10～20bps，刻意不在缺貨時漲價。GAAP 與非 GAAP 營益差約 8.9 個百分點，主要是 SBC（占營收 8.8%）","archetype":{"primary":"品質複利成長","secondary":"循環/商品","confidence":"中","fingerprint":"無晶圓廠類比電源 IC，營收 2022 年 17.9 億到 2026E 約 43.4 億，毛利率 55～58% 穩定、營益率擴張、淨現金零負債；企業數據占四成使營收帶有 AI 資本支出週期"},"industry":{"clock_phase":"II","sd_verdict_source":"需求面：Gartner 2Q26 半導體庫存指數中度缺貨並延續至 2027、Wolfe Research 認為 2028 前難供過於求、Q2 法說 book-to-bill 明顯高於 1、Q3 法說通路庫存在區間低端；供給面：10-K 稱補助對手擴產縮短交期、公司產能 2027 下半年達 80 億美元。結論：至 2027 年偏結構性，2028 年起供給可逆性高","bargaining":{"up":"上游為晶圓代工與封測，代工漲價公司吸收一部分、與客戶分攤（Q3 法說）；代工來源分散在韓、台、新加坡、中國，2022 年加入 VIS 8 吋廠","down":"2025 年三大經銷商占 26%、18%、10%，前兩大合計 44%；終端議價權在 GPU／ASIC 平台廠，旗艦平台可在一代內換供應商（2025 年 Blackwell 前例）；與 OEM／ODM 無採購承諾","geo":"2025 年 92% 營收來自亞洲客戶，中國有生產營運與關鍵供應商；美中關稅、出口管制與台海、香港局勢列於風險因子；Section 232 半導體關稅是否適用本公司產品事實表未涵蓋"},"profit_pool_dir":"資料中心供電利潤池由分離式元件往高密度模組、垂直供電與 48V／800V 架構遷移，公司站在流入端；若整合式穩壓普及，最後一級轉換的價值可能移進封裝，流向轉為不確定","tam_table":{"expanded":false,"reason":"事實表未涵蓋電源 IC 的 TAM、SAM 與滲透率；唯一的規模數字是管理層自述的建築自動化 400～500 億美元，未經第三方，且公司自承尚不知如何轉成營收，不足以組成表；成長跑道改用分市場營收與產能上限判讀"}}}},"q2_moat":{"verdict":"護城河持平：靠功率密度與設計速度贏插槽，不靠定價；毛利率低於 ADI、TXN、VICR，旗艦平台份額可在一代內被換掉，但已用多客戶與多市場分散","reasoning":"機制：自研製程與封裝把電源做到高密度，加上 6,000 多個產品的長尾覆蓋與快速設計週轉，讓公司在功率密度要求最高的插槽拿到設計導入；轉換成本只存在於單一平台週期內。方向證據：①份額：2025 年 Blackwell 主要配額落到 Infineon 與 Renesas，2026-07 KeyBanc 估 VR200／R200 平台約七成，失而復得，但證明可被換；②利潤率：TTM 毛利率 55.2%，低於 ADI 65.8%、TXN 60.2%、VICR 60.6%，高於 Infineon 39.4%；TTM 營益率 29.4%，低於 TXN 41.1%、ADI 35.7%，同業歷史序列事實表未涵蓋，價差方向無法判定；本檔營益率由 FY2025 的 26.1% 升到 TTM 29.4%，毛利率由 FY2022 58.4% 降到 FY2025 55.2% 後持平。執行力 9：Q3 首次單季破 10 億、產能一年內堆到 60 億且不改資本結構、通訊與車用同步起量；定價力 7：缺貨時刻意不漲價，代工漲價與客戶分攤後毛利率仍每季擴 10bps，但不及類比大廠。執行力擴大、定價力穩定；因 2025 年旗艦平台份額曾下滑，不得判擴大，合判持平。整合式穩壓列一項生態級威脅。ROIC：稅後營益率可得，投入資本事實表未涵蓋，周轉率無法計算；帳面再投資接近零，使增量報酬公式失去解釋力，見持續期欄。","fact_refs":["f_peer_mpwr_gross_margin_pct","f_peer_mpwr_operating_margin_pct","f_peer_mpwr_fcf_margin_pct","f_peer_adi_gross_margin_pct","f_peer_adi_operating_margin_pct","f_peer_adi_fcf_margin_pct","f_peer_txn_gross_margin_pct","f_peer_txn_operating_margin_pct","f_peer_txn_fcf_margin_pct","f_peer_vicr_gross_margin_pct","f_peer_vicr_operating_margin_pct","f_peer_vicr_fcf_margin_pct","f_peer_ifx_de_gross_margin_pct","f_peer_ifx_de_operating_margin_pct","f_kpi9_inventory_days","f_net_debt_m"],"verdict_values":{"moat":{"mechanism":"功率密度與設計速度：自研製程與模組封裝做出高功率密度（管理層自述全球最高），加上 6,000 多個產品長尾覆蓋，在 AI 加速器、光模組、車用 48V 等高功率插槽拿設計導入；轉換成本僅在單一平台週期內有效","execution":9,"pricing":7,"grade":"B","trend":"→","trend_evidence":"旗艦平台份額 2025 年失守、2026 年 KeyBanc 估回到約七成；毛利率 FY2025 55.18% 到 TTM 55.22% 持平，Q3 季增 10bps；營益率 TTM 29.4% 高於 FY2025 26.1%。執行力擴大、定價力穩定、份額曾下滑，合判持平","competitor_notes":[{"name":"ADI","strategy_note":"毛利率 65.8%、FCF 利潤率 35.6% 都高於本檔，透過收購 Empower 切入整合式穩壓，是下一代 AI 供電最該盯的對手"},{"name":"TXN","strategy_note":"營益率 41.1% 為同業最高，自有晶圓廠可領 CHIPS 補助擴產、縮短交期，在工業與車用通用電源以成本和交期競爭"},{"name":"VICR","strategy_note":"毛利率 60.6% 但營益率 24.9%、FCF 利潤率 9.1%，同走 48V 高密度模組路線，規模小且資料中心單點集中"},{"name":"IFX.DE","strategy_note":"毛利率 39.4%、營益率 14.9% 遠低於本檔，卻拿到 Blackwell 主要配額，證明旗艦平台會在一代內換供應商"},{"name":"Renesas","strategy_note":"不在同業數字表內；與 Infineon 一起被報導取得 Blackwell 配額，是旗艦平台的第二來源"}],"threats":[{"level":"🟡","text":"Infineon、Renesas 在旗艦 GPU 平台當第二來源，2025 年曾拿走 Blackwell 主要配額；CSIMarket 稱 Q2 2026 某區隔份額下滑，但區隔與方法不明","p":"35%","evidence_refs":["customer_second_source#3","competitive_share_entrants#3"]},{"level":"🟡","text":"對手規模較大且可領 CHIPS 補助擴產、縮短交期，公司為無晶圓廠不符資格；細分市場擴張使對手數量增加","p":"40%","evidence_refs":["competitive_share_entrants#1","competitive_share_entrants#2"]},{"level":"🟡","text":"大客戶自研或收購可替代元件，10-K 列為重大不利風險，尚無具體事件","p":"15%","evidence_refs":["customer_second_source#0","substitute_technology#0"]},{"level":"🔴","text":"ADI 收購 Empower 切入整合式穩壓，可能把最後一級供電移入封裝，並以大廠產品組合綁售；公司拒評他廠、稱有自有方案；若旗艦平台採第三方整合式穩壓而排除本公司，升為架構替代並重評論點","p":"30%","evidence_refs":["substitute_technology#1"]}],"roic_durability":{"quadrant":"高利益率×周轉率未定（稅後營益率可得；投入資本事實表未涵蓋，無晶圓廠與淨現金推定周轉偏高，但存貨 130 天拉低周轉）","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者是資料中心與車廠，決策者是 GPU／ASIC 與系統設計廠，付款者經 ODM 與經銷商；要解決的問題是把數百安培低電壓電流有效送進晶片，屬需要不是想要，且隨功率上升而加深。急迫性來自 AI 資本支出，持久性來自功率密度的物理限制；問題持久，公司目前的模組方案未必持久"},{"item":"決策層級","level":"🟡","text":"替代性要在單一平台插槽衡量：每代平台重新決定供應商，週期約一年；Blackwell 一代就換成 Infineon、Renesas 為主，10-K 也載明無採購承諾。重新認證成本存在，但只鎖住一個平台週期"},{"item":"價值鏈分配","level":"🟡","text":"價值鏈利潤主要被 GPU／ASIC 平台廠拿走，平台廠刻意維持多供應商；公司吃到的是高密度溢價，但毛利率 55% 低於類比大廠，代工漲價只能部分轉嫁；前三大經銷商占 54% 增加通路端議價。各環節價值占比事實表未涵蓋"},{"item":"社會容忍度","level":"🟡","text":"產品非民生必需，沒有價格天花板問題，優勢也不靠監管授權；但 92% 營收在亞洲、中國有生產，出口管制、關稅與台海局勢可快速改變可售範圍，屬政策風險而非價格容忍度風險"}],"roiic":"事實表未涵蓋投入資本、折舊攤提與營運資金分項，無法計算；帳面上 2023 年 FCF 5.81 億高於淨利 4.27 億、2025 年 FCF 6.63 億高於淨利 6.21 億，淨再投資接近零，增量報酬在帳面上趨近無限大，不具解釋力","reinvest_rate":"近零到轉正：2023、2025 年 FCF 高於淨利；TTM FCF 利潤率 15.3% 低於 FY2025 的 23.8%，擴產與存貨開始吃現金（營運資金分項事實表未涵蓋）","endo_ceiling":null,"formula_note":"無晶圓廠模式的主要再投資是費用化研發與代工產能承諾，不進資產負債表，增量報酬乘再投資率的公式不適用；改用實體上限：2027 下半年 80 億美元年化營收產能、長期 100 億"}}}},"q3_growth":{"verdict":"跑道寬：企業數據之外，通訊與車用 48V 已實際出貨，800V 與記憶體介面排在 2027～2028；2027 年有 80 億產能撐量，2028 年企業數據高基期是第一個考驗","reasoning":"成長以量為主：企業數據的客戶擴散與模組含量、通訊的光模組與交換器、車用 48V 首批訂單；價格不是顯著貢獻；營益率擴張是第二來源；Q3 回購逾 4.5 億美元，淨回購貢獻小。共識 EPS：FY2026E 27.55、FY2027E 35.27、FY2028E 41.1（Koyfin 快照），兩年 CAGR 22.1%；但 FY2027 共識營收 64.26 億（年增 48%，16 位分析師）與 EPS 共識互相矛盾：以 Q3 非 GAAP 營業利益 4.645 億對應 EPS 8.19 的換算比、Q4 指引中值 13.5 億與 38.6% 營益率估算，Q4 單季 EPS 約 9.2、年化約 36.8，已高於 FY2027 EPS 共識，代表 EPS 共識隱含 2027 年營收不再成長，較可能是快照未更新。內生上界：帳面再投資公式不適用，改以產能上限檢核，Base 路徑 2031 年營收約 88 億，在公司 100 億產能目標內。缺口歸因：無法用公式量化，拆成量（主）、營益率擴張（次）、淨回購（小）。跑道：滲透率事實表未涵蓋，以已出貨的第二曲線判讀為寬。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_kpi0_revenue_gaap","f_kpi1_non_gaap_operating_incom","f_kpi2_non_gaap_operating_margi","f_kpi8_non_gaap_diluted_eps","f_kpi10_q4_fy2026_guidance_reven"],"verdict_values":{"growth":{"driver_mix":"量為主（客戶擴散、模組含量、新平台）加營益率擴張為輔、淨回購小；漲價非顯著來源；無併購","runway_years":"約 10（推定：企業數據以外分市場合計占營收約 58%，且有 48V、800V、記憶體介面三條待放量曲線；滲透率事實表未涵蓋）","runway_post_y5":"🟢","endo_ceiling_basis":"帳面公式不適用（研發費用化、產能靠代工承諾），以產能作實體上限：現有 60 億美元年化營收產能、2027 下半年 80 億、長期目標 100 億；Base 路徑 2027 年營收約 58～60 億、2031 年約 88 億，皆在上限內","segments":[{"item":"企業數據","value":"Q3 5.07 億，占 42.1%，季增 33.2%、年增 164.6%；2026 全年成長下限由 130% 上調到 150%"},{"item":"儲存與運算","value":"Q3 1.92 億，年增 3.0%；DDR5 PMIC 與儲存強、筆電受記憶體缺貨拖累，全年約持平到小增"},{"item":"通訊","value":"Q3 1.87 億，年增 134.7%、季增 43%；光模組加交換器，管理層稱全年成長第二快"},{"item":"車用","value":"Q3 1.81 億，占 15.0%，年增 19.2%；48V 首批訂單，48V 與區域架構設計導入驅動 2027"},{"item":"工業","value":"Q3 0.71 億，年增 29.0%；機器人開始放量，2026 年以累積設計導入為主"},{"item":"消費","value":"Q3 0.64 億，年減 11.6%"}],"decay_signals":["毛利率連 2 季年減：未亮（TTM 55.22% 與 FY2025 55.18% 持平，Q3 季增 10bps）","核心市占近 12 個月縮減：未亮（Blackwell 失守在 2025 年中，已超過 12 個月；CSIMarket 區隔份額下滑方法不明，不計）","提價後銷量下滑：不適用（未主動提價）","EPS CAGR 高於營收 CAGR 逾 5 個百分點：未亮（共識 FY2027 營收增 48%、EPS 增 28%）","FCF／淨利連 2 年低於 0.75：未亮（2023 年 1.36、2025 年 1.07；2024 年受一次性稅務利益扭曲；TTM 轉弱列監測）","SBC／營收高於 5% 且逐年上升：半亮（Q3 為 8.8%，逐年趨勢事實表未涵蓋，營收高成長下比率上升可能性低，暫不計入）","TAM 萎縮或被替代技術壓縮：未亮（整合式穩壓列監測）","產業估值倍數近 3 年系統性下移：事實表未涵蓋","維護性資本支出占 FCF 逾 60%：事實表未涵蓋","停止投資新產能且收入 3 年內下滑：未亮（產能擴張中）"],"trap_rating":"價值陷阱風險🟢（0 項亮燈、1 項半亮）；長期成長性🟢"}}},"q4_capital":{"verdict":"資本配置穩健但不出色：零負債、淨現金 10.9 億，股息加回購回饋股東；SBC 占營收 8.8% 偏高，回購在高倍數價位進行，收益率偏低","reasoning":"FCF／淨利：2023 年 1.36、2025 年 1.07；2024 年淨利含外國一次性租稅優惠的遞延所得稅（已因此重編），不可比。TTM FCF 利潤率 15.3%，低於 FY2025 的 23.8% 與 ADI、TXN 的 35%；Q3 營業現金流 2.90 億只有非 GAAP 營業利益 4.645 億的六成，擴產期存貨與營運資金吃現金。SBC：Q3 1.063 億、占營收 8.8%，年化約 4.25 億，約市值 632 億的 0.7%。回購：Q3 逾 4.5 億美元（Q3 法說），Q2 法說加碼 5 億授權至總額 10 億；Q3 單季回購約占市值 632 億的 0.7%（未年化）；以現價 1,296 對 FY2026 共識 EPS 27.55 計，盈餘殖利率約 2.1%，這是回購的買入報酬，不是回購收益率。併購：最近一次為 2024 年 2 月 Axign，無重大併購。現金去向四分事實表未涵蓋，公司無負債。Tony Balow 於 Q3 法說首度以財務長身分出席，發生在 2026-02 財報重編之後，前任去向事實表未涵蓋。","fact_refs":["f_kpi5_sbc_and_related_expenses","f_kpi6_operating_cash_flow","f_kpi1_non_gaap_operating_incom","f_peer_mpwr_fcf_margin_pct","f_net_debt_m","f_dividend_yield_ttm","f_ev_m","f_shares_diluted_m","f_consensus_eps_fy1","f_price_at_dd"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":false,"passed":null,"input":"近 12 個月無重大併購，最近一次為 2024 年 2 月 Axign，規模未揭露"},{"name":"buyback_yield","applicable":true,"passed":false,"input":"Q3 回購逾 4.5 億美元，約占市值 632 億的 0.7%（單季，未年化），回購均價未揭露；回購的買入報酬以現價 1,296 對 FY2026 共識 EPS 27.55 的盈餘殖利率代理，約 2.1%；10 年期殖利率事實表未涵蓋，但門檻為殖利率加 2%，以常態利率判不過"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"SBC 年化約 4.25 億美元（Q3 1.063 億乘 4）除以市值 632 億約 0.7%／年，未扣回購已低於 1.5%"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購支撐，資本回饋以股息（殖利率 0.58%）與回購為主；近三年現金去向分項事實表未涵蓋，展開只會剩管理層口述數字"}}}},"q5_valuation":{"verdict":"現價要 FY2027 EPS 做到約 40、之後每年一成以上成長並維持 30 倍上下才划算；我相信 FY2027 會高於 35.27 的共識，但 PEG 約 2.1，不追價","reasoning":"現價 1,296 對 FY2026 共識 EPS 27.55 為 47.0 倍（前份 47.4 倍），對 FY2027 共識 35.27 為 36.8 倍；trailing P/E 71.0 倍、P/S 16.9 倍分別在近四個年度端點的 96.4% 與 100% 分位（非五年分位，五年高低點事實表未涵蓋）。PEG 以 FY2026E 到 FY2028E 兩年共識 CAGR 22.1% 計為 2.13，偏貴；若 FY2027 EPS 實際約 40，FY2027 倍數降到 32 倍。股價 26 週跌 17.3%、RSI 53.7，無過熱。賣方均價目標 1,829.54（15 位，StockAnalysis），高於現價約 41%，目標價日期未標，不作承重。同業倍數事實表未涵蓋，終端倍數參照前份同業中位 25.6 倍。估值結論：中性偏貴，但有盈餘上修空間，維持中間檔。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_pe_current","f_pe_percentile","f_ps_current","f_ps_percentile","f_ev_s_current","f_ev_s_fwd","f_consensus_rev_3m_fy1_pct","f_week26_return_pct","f_rsi14","f_ma_state"],"verdict_values":{"valuation":{"basis":"Fwd P/E（FY2026E 非 GAAP 共識，已過三季加 Q4 指引，接近實現）為主、PEG 為輔","tier":"高成長無晶圓廠類比電源","peers":{"expanded":false,"reason":"事實表同業對照只有利潤率與研發密度，沒有同業倍數；前份（2026-07-31）同業中位 Fwd P/E 25.6 倍只作終端倍數參照，本次未重新取得，不可當現值錨"},"fwd_pe":47.02,"peg":2.13,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"Fwd P/E 47.0 倍、PEG 2.13 偏貴，P/S 在近四年端點最高；但 FY2026 分母接近實現、FY2027 共識有上修空間（Q4 指引年化 EPS 約 36.8 已超過 FY2027 共識），Base 情境終端 30 倍下五年年化約 7.5% 加股東回饋約 1%，落在中間區，判中間檔。短期上檔＝一年後以 FY2028 Base EPS 44 乘 32 倍得 1,408（+8.6%）；中期＝三年後以 FY2030 Base EPS 56 乘 30 倍得 1,680（+29.6%）","upside_short_pct":8.6,"upside_mid_pct":29.6,"denominator_disputed":false,"denominator_note":"FY2026 分母已過三季，非爭點；FY2027 有兩個來源互相矛盾：EPS 共識 35.27（年增 28%，Koyfin 快照財報前後未變）對營收共識 64.26 億（年增 48%），以 Q3 利潤結構換算，營收共識對應的 EPS 約 44～45。本判斷 Base 取 40，不依賴便宜論證"}}},"q6_how_wrong":{"verdict":"最可能看錯在 2027～2028：旗艦平台份額再被分走、或全產業擴產後 AI 資本支出消化，企業數據高基期回落，倍數同時向同業收斂，Bear 五年約 −49%","reasoning":"反證與依據集中在反證紀錄：論點失敗兩條（份額加消化、整合式穩壓）、股東經濟變差一條（SBC 與現金轉換）、價格反映過多一條。財報可信度：2026-02 重編 FY2024 與 2025 各季財報、證券集體訴訟仍在進行，之後財務長換人。成長熄火測試：以 FY2028 共識 EPS 41.1 為底，只測 FY2029 一年降速，增速取 15%、10%、5%，倍數分別給 30、22、16 倍，FY2029 年底股價約 1,418、994、691，只有 15% 情境不虧，壓力測試三過一。歷史最大回撤與空方數字事實表未涵蓋；Max DD 以 Bear 路徑推為 −45%～−65%。十項衰退訊號 0 亮 1 半亮，主要風險是週期與估值，不是價值陷阱。","fact_refs":["f_week26_return_pct","f_ps_percentile","f_pe_percentile","f_kpi5_sbc_and_related_expenses","f_peer_mpwr_fcf_margin_pct","f_consensus_eps_fy3"],"verdict_values":{"trap":{"verdict":"🟢","label":"衰退訊號 0 亮 1 半亮；風險在週期與估值，不在價值陷阱"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":27.55,"pe":47.05,"basis":"FY2026E 非 GAAP 共識 EPS（已過三季加 Q4 指引，接近實現）；終端倍數同樣套在終端年當年非 GAAP EPS"},"eps":{"bull":[46,55,66,77,88],"base":[40,44,50,56,62],"bear":[33,26,27,30,33]},"pe":{"bull":38,"base":30,"bear":20},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0.58,"net_buyback":0.4},"second_stage":{"bull_cagr_pct":14,"base_cagr_pct":10},"max_dd":{"lo":-65,"hi":-45,"basis":"Bear 終點約 −49%（EPS 33 乘 20 倍得 660），路徑中通常超跌：①2028 年 EPS 退到 26 而倍數同時壓到 20 倍，股價約 520，距現價 −60%；②旗艦平台份額傳言曾讓股價單日重挫近一成（前份紀錄）；③P/S 16.9 倍、trailing P/E 71 倍位於近四個年度端點最高或接近最高，沒有估值墊。歷史最大回撤事實表未涵蓋，取 −45%～−65%","trigger_time":null},"basis":{"bull":"企業數據 2027 年在 80 億產能支撐下續增，FY2027 營收接近共識 64 億、非 GAAP 營益率 40% 以上（EPS 46）；2028 年起通訊、車用 48V、800V、記憶體介面接棒，2031 年仍有中雙位數成長，市場保留成長溢價給 38 倍（約前份同業中位 25.6 倍的 1.5 倍）","base":"FY2027 營收約 58～60 億（Q4 指引年化 54 億再小幅成長），EPS 40；2028 年 AI 資本支出消化使 EPS 只增一成，之後靠新曲線每年一成出頭，2031 年 EPS 62、營收約 88 億，終端 30 倍（較前份同業中位 25.6 倍溢價約一成七）","bear":"2027 年旗艦平台份額被分走、企業數據停滯（產業仍缺貨，與第三方缺貨延續至 2027 的預估並存），EPS 33；2028 年全產業擴產到位、AI 資本支出消化，EPS 回到 26，之後緩升到 33；倍數向同業以下的 20 倍收斂（成長熄火降至一成的情境約 22 倍，再打九折）"},"endo_ceiling_exceeded":false},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"2025 年 Blackwell 主要配額落到 Infineon 與 Renesas；10-K 載明與 OEM／ODM 無採購承諾、對手可領補助擴產；公司產能 2027 下半年到 80 億、長期 100 億","assumption":"企業數據的多客戶擴散與模組含量提升，足以抵銷單一平台份額波動與 2028 年資本支出消化","consequence":"五年虧 50% 最可能的故事：2027 年旗艦平台份額被分走，2028 年全產業擴產到位、AI 資本支出消化，企業數據腰斬，EPS 回到約 26 後緩升到 33，倍數收斂到 20 倍，終點約 660","ruling":"部分採納：Bear 機率取 30%、Max DD 下緣 −65%；不全面採納，因企業數據全年下限剛上調到 150%、通路庫存在區間低端、第三方預估缺貨延續到 2027。與 Single Thing 部分重疊，本條另含資本支出消化","watch":"企業數據季營收、book-to-bill、通路庫存週數","evidence_refs":["customer_second_source#3","customer_second_source#1","competitive_share_entrants#1"],"fact_refs":["f_kpi0_revenue_gaap","f_kpi9_inventory_days"]},{"view":"論點失敗","evidence":"Q3 法說分析師點名 ADI 收購 Empower 的整合式穩壓，Hsing 拒評他廠、稱公司有自有方案但在營收確定前不公開；10-K 稱對手新產品與新進者可能讓產品失去競爭力","assumption":"下一代 GPU 的最後一級供電仍以垂直模組為主，或公司能提供同等整合式方案","consequence":"若旗艦平台改採第三方整合式穩壓，企業數據每顆加速器含量下降，模組化論點失效，護城河趨勢改判下滑","ruling":"不可裁決至 2027 年下一代平台物料清單公布；先列威脅、機率 30%，不改 Base","watch":"旗艦平台供電架構、公司是否公開整合式穩壓產品","evidence_refs":["substitute_technology#0","substitute_technology#1"],"fact_refs":[]},{"view":"論點成功但股東經濟變差","evidence":"Q3 SBC 1.063 億、占營收 8.8%；TTM FCF 利潤率 15.3%，低於 FY2025 的 23.8%，也遠低於 ADI 35.6%、TXN 35.2%；Q3 營業現金流 2.90 億只有非 GAAP 營業利益的六成","assumption":"營收照計畫成長時，自由現金流會跟上淨利","consequence":"營收與非 GAAP EPS 達標，但擴產存貨、代工預付與 SBC 吃掉現金，每股自由現金流落後 EPS 複利；Q3 GAAP EPS 5.51 對非 GAAP 8.19，以 GAAP 計的倍數高約五成","ruling":"部分採納：Base 淨回購只取 0.4%，不把 Q3 的 4.5 億回購當常態；FCF／淨利列減碼門檻","watch":"年度 FCF／GAAP 淨利、SBC／營收、存貨天數","evidence_refs":[],"fact_refs":["f_kpi5_sbc_and_related_expenses","f_peer_mpwr_fcf_margin_pct","f_kpi6_operating_cash_flow","f_kpi7_gaap_diluted_eps","f_kpi8_non_gaap_diluted_eps"]},{"view":"價格已反映太多","evidence":"P/S 16.9 倍、EV/S 16.6 倍皆在近四個年度端點的 100% 分位，trailing P/E 71 倍在 96.4% 分位；PEG 2.13；賣方均價目標 1,829.54 隱含市場已預期 2027 年續高成長","assumption":"FY2027 EPS 約 40，高於 35.27 的共識","consequence":"若 FY2027 只做到 Q4 指引年化的約 36.8，FY2027 倍數約 35 倍，Base 五年報酬降到年化約 6～7%","ruling":"部分採納：不追價，加碼要等價格或指引；反駁全面迴避，因 26 週已跌 17.3%，Fwd P/E 由前份 47.4 倍降到 47.0 倍，盈餘上修仍在進行","watch":"FY2027 EPS 共識修正、Fwd P/E","evidence_refs":["capital_markets_pricing#4"],"fact_refs":["f_ps_percentile","f_pe_percentile","f_ev_s_percentile","f_fwd_pe_latest","f_week26_return_pct"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 1450.0 → 本次 1296.22（-10.6%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=1450.0","side_b":"本次 price_at_dd=1296.22","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]裁決由 dd_decision.py 機械路由：前份 進場 → 本次 觀望","cause":"方法變動","prior_field":["dca_verdict"],"side_a":"前份 dca_verdict=進場","side_b":"本次 dca_verdict=觀望","ruling":"裁決是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。沒有單一輸入能還原，屬多欄共同：均線 ✅→🟡。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]角色由 dd_decision.py 機械路由：前份 衛星 → 本次 追蹤","cause":"方法變動","prior_field":["dca_role"],"side_a":"前份 dca_role=衛星","side_b":"本次 dca_role=追蹤","ruling":"角色是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。沒有單一輸入能還原，屬多欄共同：均線 ✅→🟡。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 1,450 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 1,450 美元：Bull 價 3,458、Bear 價 889，五年期望值 +54.7%，基準年化 9.2%，不對稱比 4.3","side_b":"本次情境、股價仍用 1,450 美元：Bull 價 3,344、Bear 價 660，五年期望值 +29.0%，基準年化 5.1%，不對稱比 2.0","ruling":"先換情境、股價不動：五年期望值少 25.7 個百分點，基準年化少 4.1 個百分點。不對稱比由 4.3 變為 2.0。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 1,450 美元：五年期望值 +29.0%，基準年化 5.1%，不對稱比 2.0","side_b":"本次情境、股價 1,296.22 美元：五年期望值 +44.3%，基準年化 7.5%，不對稱比 2.68","ruling":"再換股價、情境不動：起點價下跌 10.6%，五年期望值多 15.3 個百分點，基準年化多 2.4 個百分點，不對稱比由 2.0 升到 2.68。合計五年期望值比前份少 10.4 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"管理層前後說法（Q2 2026-07-30 對 Q3 2026-10-29）","cause":null,"prior_field":null,"side_a":"Q2：Tony Balow 將企業數據全年下限由 85% 上調到 130%；Hsing 稱 800V 營收時點不知道、建築自動化軟體今年底前可完成","side_b":"Q3：Tony Balow 再將下限上調到 150%；800V 時點改說 2027 年底到 2028 年；Hsing 對建築自動化改稱專案剛開始、還不知道怎麼走到 500 億營收","ruling":"一致為主、可調和：核心業務承諾都兌現並上修；非核心的建築自動化說法明顯後退，屬管理層對新事業過度樂觀的紀錄，不影響 Base，但 Hsing 所稱「提到的新事業歷來都會變成營收」不採為證據","evidence_level":"高（逐字稿）","settle_metric":"Q4 法說對 800V 與建築自動化的口徑","if_then":["若 800V 在 2028 年仍無可揭露營收：H3 削弱，Bull 機率降到 20%","反向：若 800V 在 2027 年底前出貨：H3 驗證，Bull 機率回到 30%"],"evidence_refs":[]},{"axis":"FY2027 盈餘分母：EPS 共識與營收共識方向相反","cause":null,"prior_field":null,"side_a":"FY2027 EPS 共識 35.27（Koyfin，Q3 財報前後快照未變），以 Q3 利潤結構換算隱含 2027 年營收約 51～52 億，低於 Q4 指引年化 54 億，等於 2027 年要季減","side_b":"FY2027 營收共識 64.26 億（16 位分析師，年增 48%），換算 EPS 約 44～45；管理層稱看不到放緩、產能 2027 下半年到 80 億","ruling":"不可調和（一個隱含衰退、一個隱含加速），選 B 側方向但打折：Base 取 FY2027 EPS 40（營收約 58～60 億），Bull 才用 64 億營收。硬數據點是 Q4 指引中值 13.5 億與 Q3 非 GAAP 營益率 38.6%，年化已超過 EPS 共識；A 側快照未反映 Q3 財報的可能性高","evidence_level":"中（兩個資料源口徑未對齊，換算比用單季）","settle_metric":"2027-02 Q4 財報給的 Q1 2027 營收指引中值，及之後一個月的 FY2027 EPS 共識","if_then":["若 Q1 2027 營收指引中值 ≥14 億美元且 FY2027 EPS 共識上修到 ≥38：維持 Base，股價回到 1,150 以下時加碼第二批","反向：若 Q1 2027 指引中值低於 13 億（低於 Q4 指引中值）：Base 的 FY2027 EPS 下修到 35、停止加碼，Bear 機率提高到 35%"],"evidence_refs":["capital_markets_pricing#2","capital_markets_pricing#3"]},{"axis":"現在就賣的最強論證","cause":null,"prior_field":null,"side_a":"賣：P/S 16.9 倍與 trailing P/E 71 倍在近四年端點最高；企業數據年增 164.6% 讓 2027 下半年起面對極高基期；全產業與公司自己都在擴產，2028 年供過於求的機率不低；TTM FCF 利潤率只有 15.3%，獲利品質不及類比大廠；年初才重編財報、集體訴訟未結、財務長剛換","side_b":"留：Q4 指引年化 EPS 已超過 FY2027 共識，盈餘上修尚未完成；26 週已跌 17.3%、RSI 53.7 不過熱；成長來源跨通訊、車用、工業，不只企業數據；淨現金零負債","ruling":"留但不追：賣方論點多屬估值與 2028 年週期，時間上晚於 2027 上半年的盈餘上修窗口；以 Q1 2027 指引作分界","evidence_level":"中","settle_metric":"Q1 2027 營收指引中值與 FY2027 共識修正","if_then":["若 Q1 2027 指引中值低於 13 億且股價仍在 1,250 以上：減碼三分之一","反向：若指引中值 ≥14 億：保留全部並依加碼條件執行"],"evidence_refs":["competitive_share_entrants#1","sec_investigation_restatement#0"]},{"axis":"前份漂移：基本面判斷欄","cause":"新證據","prior_field":["signal","trap","moat_trend","runway_post_y5","archetype","cycle_position"],"side_a":"前份（2026-07-31）：訊號 A、價值陷阱🟢、護城河趨勢→、五年後跑道🟢、品質複利成長、循環位置未填","side_b":"本次：訊號 A、價值陷阱🟢、護城河趨勢→、五年後跑道🟢、品質複利成長、循環位置未填（主類型非循環股）","ruling":"六欄皆維持。新證據兩面：正面是 Q3 營收 12.02 億、企業數據全年下限由 130% 上調到 150%、車用 48V 首批訂單、產能目標上看 80 億；負面是 TTM FCF 利潤率滑到 15.3%、Q3 法說被問到 ADI 收購 Empower 的整合式穩壓、財務長換人。正負都沒有改變跑道或護城河方向的程度","evidence_level":"高（公司新聞稿與法說）","settle_metric":"2027 年前兩季企業數據營收與旗艦平台份額","if_then":["若旗艦平台確認改由他廠為主供應：護城河趨勢改判下滑並減碼至觀察倉","反向：若 800V 或車用 48V 在 2027 年出現可揭露營收：維持跑道判斷，不因企業數據高基期回落而減碼"],"evidence_refs":["end_markets#0","substitute_technology#2"]},{"axis":"前份漂移：估值結論","cause":"價格變動","prior_field":["val"],"side_a":"前份股價 1,450、Fwd P/E 47.4 倍，估值中間檔","side_b":"本次股價 1,296（跌 10.6%）、Fwd P/E 47.0 倍，估值中間檔","ruling":"維持。股價下跌被 FY2026 共識 EPS 三個月上修 14.0%（24.17 到 27.55）抵銷，倍數幾乎不變","evidence_level":"高","settle_metric":"Fwd P/E 與 FY2027 共識修正","if_then":["若 FY2027 共識上修到 ≥40 而股價不動：FY2027 倍數降到約 32 倍，估值改判偏便宜一檔","反向：若股價回到 1,600 以上而共識不動：Fwd P/E 超過 58 倍，停止加碼"],"evidence_refs":[]},{"axis":"前份漂移：情境機率、回撤範圍與裁決角色","cause":"方法變動","prior_field":["p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份 Bull 30%、Bear 25%，最大回撤單點 −60%；裁決進場，角色由前份矩陣給出","side_b":"本次 Bull 25%、Bear 30%，最大回撤範圍 −45%～−65%；裁決與角色由決策矩陣依本次輸入重算，本判斷不直接指定","ruling":"方法變動三處：①內生成長上限無法用帳面再投資公式推得，改用產能上限檢核，依保守原則 Bear 取 30%；②終端年改為 FY2031，Bear 終端 EPS 須低於 FY2027 共識 35.27，Bear 路徑因此納入 2028 年擴產後的消化期；③最大回撤由單點改為範圍。股價較前份低 10.6%，對機率無影響","evidence_level":"中","settle_metric":"2028 年企業數據營收年增率","if_then":["若 2027 年底 book-to-bill 仍高於 1 且同業未見庫存堆積：Bear 機率回到 25%","反向：若 2027 年任一季 book-to-bill 跌破 1：Bear 機率提高到 35% 並減碼三分之一"],"evidence_refs":["supply_demand_durability#0","supply_demand_durability#5"]},{"axis":"加碼門檻變動","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"已建 starter 1/2；加碼觸發＝Rubin VR200 插槽定案，或企業數據單季 YoY ≥+80% 連兩季","side_b":"加碼：Q1 2027 營收指引中值 ≥14 億美元且旗艦平台份額未失守；或股價 ≤1,150 而企業數據季營收未季減","ruling":"舊加碼條件的第二項已在 Q3 成立（企業數據年增 164.6%，全年下限 150%），門檻失去鑑別力；新加碼條件改看 2027 年 Q1 指引是否延續成長，並加價格條件，避免在 47 倍追價；1,150 對 Base 終值約為年化一成以上","evidence_level":"高","settle_metric":"Q1 2027 營收指引中值","if_then":["若條件成立：加碼第二批至目標倉位","反向：若 Q1 2027 指引中值低於 13 億：取消加碼，並提前檢查清倉條件"],"evidence_refs":["end_markets#0"]},{"axis":"Single Thing 變動","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設唯一致命點（null）","side_b":"Nvidia 下一代旗艦平台（Vera Rubin，VR200／R200）量產時，主供電份額由 KeyBanc 估的約七成降到 30% 以下，改由 Infineon、Renesas 或整合式穩壓方案為主","ruling":"前份把旗艦平台失守列為風險而未單列；本次依最大單一敏感度補設 Single Thing：企業數據占營收 42.1%，二手報導估旗艦平台約 15% 營收受影響，是單一事件中對 EPS 與倍數衝擊最大者","evidence_level":"中（份額數字來自賣方，未經公司證實）","settle_metric":"旗艦平台量產後的企業數據季營收","if_then":["若確認失守：減碼至觀察倉並重跑判斷","反向：若 2027 年中企業數據仍季增：維持倉位，Single Thing 機率下修到 10%"],"evidence_refs":["customer_second_source#3","end_markets#2"]},{"axis":"清倉與減碼門檻新設","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設 kill_metrics（null）","side_b":"企業數據季減 ≥15% 或連 2 季低於 5.07 億則減碼；毛利率連 2 季低於 54% 則減碼；旗艦平台份額確認低於 30% 則清倉檢查；通路庫存超過 8 週則停止加碼；FCF／淨利連 2 年低於 0.75 則減碼","ruling":"前份只有加碼條件，沒有清倉與減碼門檻，本次補齊；門檻取自管理層自己的模型區間（毛利率 55～60%、通路 5～8 週）與本季實績","evidence_level":"高","settle_metric":"每季新聞稿與法說","if_then":["若兩項以上門檻同季觸發：清倉","反向：若門檻全數未觸發而股價跌破 1,150：分批反買，不視為停損"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"企業數據 2026 全年年增是否達管理層下限 150%","type":"假設驗證","maps_to":"H1","metric":"企業數據全年年增率","threshold":"≥150%","action":"未達：H1 削弱、停止加碼","source_freq":"季報新聞稿，每季","date":"2027-02","evidence_refs":["end_markets#0"]},{"n":2,"text":"旗艦 AI 平台主供電份額被他廠取得","type":"Single Thing","maps_to":"Single Thing","metric":"旗艦平台供電份額","threshold":"公司或主要客戶確認降至 30% 以下","action":"減碼至觀察倉並重跑判斷","source_freq":"法說與賣方通路調查，每季","date":null,"evidence_refs":["customer_second_source#3","end_markets#2"]},{"n":3,"text":"Q1 2027 指引延續成長或價格回到合理區時加碼","type":"加碼","maps_to":"H1","metric":"Q1 2027 營收指引中值；股價","threshold":"指引中值 ≥14 億美元且旗艦份額未失守；或股價 ≤1,150 且企業數據季營收未季減","action":"加碼第二批至目標倉位","source_freq":"Q4 財報，一次","date":"2027-02","evidence_refs":[]},{"n":4,"text":"毛利率跌出管理層模型","type":"減碼","maps_to":"H2","metric":"毛利率","threshold":"連 2 季低於 54%","action":"減碼一半","source_freq":"季報新聞稿，每季","date":null,"evidence_refs":[]},{"n":5,"text":"企業數據高基期回落加上需求轉弱","type":"清倉","maps_to":"R2","metric":"企業數據季營收與 book-to-bill","threshold":"企業數據連 2 季季減 ≥15% 且 book-to-bill 低於 1","action":"清倉","source_freq":"季報與法說，每季","date":null,"evidence_refs":["competitive_share_entrants#1","competitive_share_entrants#2"]},{"n":6,"text":"財報可信度與訴訟里程碑","type":"風險","maps_to":"R5","metric":"集體訴訟程序、內控與重編","threshold":"集體認證通過且不利和解；或再一次重編、內控重大缺失","action":"前者減碼一半；後者清倉","source_freq":"8-K／10-Q，不定期","date":null,"evidence_refs":["major_events#0","major_events#1","lawsuit_class_action#0","sec_investigation_restatement#0","sec_investigation_restatement#1"]},{"n":7,"text":"關稅與出口管制吸收失敗","type":"風險","maps_to":"R4","metric":"毛利率與營收指引","threshold":"管理層歸因關稅或出口管制使單季毛利率下修 ≥100bps，或營收指引因管制下修","action":"減碼三分之一","source_freq":"季報與 8-K","date":null,"evidence_refs":["reg_tariff_export#0","geo_supply_chain#0"]},{"n":8,"text":"通路與客戶集中失衡","type":"風險","maps_to":"R3","metric":"通路庫存週數、單一經銷商占比","threshold":"通路庫存超過 8 週，或單一經銷商超過 35%","action":"停止加碼；若同時毛利率低於 54% 則減碼一半","source_freq":"法說每季；10-K 每年","date":null,"evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#1","customer_second_source#1"]},{"n":9,"text":"Q4 財報後複審","type":"複審日期","maps_to":null,"metric":"Q1 2027 指引、FY2027 共識、800V 與車用 48V 進度","threshold":null,"action":"重跑判斷","source_freq":"一次","date":"2027-02","evidence_refs":[]},{"n":10,"text":"現金轉換率是否回升","type":"假設驗證","maps_to":"R6","metric":"年度 FCF／GAAP 淨利","threshold":"連 2 年低於 0.75","action":"減碼三分之一","source_freq":"10-K，每年","date":"2027-02","evidence_refs":[]}],"kill_metrics":[{"metric":"企業數據季營收","bear_threshold":"季減 ≥15%，或連 2 季低於 Q3 2026 的 5.07 億美元","window":"2027 年逐季","source":"公司季報新聞稿分市場營收","last_status":"ok"},{"metric":"毛利率","bear_threshold":"連 2 季低於 54%（管理層模型 55～60% 下緣再扣 1 個百分點）","window":"任兩季","source":"公司季報新聞稿","last_status":"ok"},{"metric":"旗艦 AI 平台供電份額","bear_threshold":"公司或主要客戶確認降至 30% 以下","window":"12～24 個月","source":"法說、賣方通路調查","last_status":"unknown"},{"metric":"通路庫存週數","bear_threshold":"超過 8 週（管理層常態區間上限）","window":"任一季","source":"法說會管理層口徑","last_status":"ok"},{"metric":"年度 FCF／GAAP 淨利","bear_threshold":"連 2 個會計年度低於 0.75","window":"FY2026～FY2027","source":"10-K 現金流量表","last_status":"unknown"}],"action_conditions":{"rearm_trigger":"加碼：Q1 2027 營收指引中值 ≥14 億美元且旗艦平台份額未失守；或股價 ≤1,150 而企業數據季營收未季減","exec_line":"不追價；依前份紀錄已建首批，加碼只在上述條件成立時做第二批；減碼與清倉依觸發器門檻；股價跌破 1,150 而基本面無損時分批反買，不視為停損"},"evidence_dismissed":[{"ref":"$.answers.q2_moat.verdict_values.moat.roic_durability","reason":"此欄的空白是資料缺口，不是漏算：事實表沒有投入資本、折舊攤提與營運資金分項，增量資本報酬算不出來，內生成長上限只能留空，填單一百分比等於編造。替代檢核已寫在同層說明：以 2027 下半年 80 億美元、長期 100 億美元的產能上限對帳，Base 路徑 2031 年營收約 88 億，在上限內。"}]},"decision_inputs":{"signal":"A","ma":"🟡","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場用 FY2027 EPS 共識 35.27 定價，該數隱含 2027 年營收低於 Q4 指引年化水準；以 Q4 指引中值 13.5 億與 Q3 非 GAAP 營益率 38.6% 換算，年化 EPS 約 36.8 已超過共識。股價 26 週跌 17.3% 反映 AI 資本支出見頂疑慮，而公司剛把企業數據全年下限上調到 150%","momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"現價不加碼，首批依前份紀錄已建、續抱。回檔條件：股價 ≤1,150 且企業數據季營收未季減；另一條非價格路徑為 Q1 2027 營收指引中值 ≥14 億美元且旗艦平台份額未失守，兩者成立其一才做第二批","asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null},"decision_out":{"role":"追蹤","row_hit":"8w(原10)","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='A'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='A'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場用 FY2027 EPS 共識 35.27 定價，該數隱含 2027 年營收低於 Q4 指引年化水準；以 Q4 指引中值 13.5 億與 Q3 非 GAAP 營益率 38.6% 換算，年化 EPS 約 36.8 已超過共識。股價 26 週跌 17.3% 反映 AI 資本支出見頂疑慮，而公司剛把企業數據全年下限上調到 150%"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='A', runway='🟢', val='🟡', moat_trend='→', week26=-17.34, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position=None, moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":false,"basis":"signal='A', val='🟡'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":false,"basis":"signal='A', val='🟡', ma='🟡'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='A', val='🟡', ma='🟡'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":true,"basis":"signal='A', val='🟡', ma='🟡'"},{"row":"8w","condition":"判斷者宣告 wait_for_price（價格合理但要等）→ 原 row10 進場改觀望（等價格）","hit":true,"basis":"wait_for_price=True, 等待條件='現價不加碼，首批依前份紀錄已建、續抱。回檔條件：股價 ≤1,150 且企業數據季營收未季減；另一條非價格路徑為 Q1 2027 營收指引中值 ≥14 億美元且旗艦平台份額未失守，兩者成立其一才做第二批'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":null,"requires_critic":[],"verdict":"觀望"},"thesis":{"H":[{"id":"H1","text":"企業數據的成長來自 GPU 與 ASIC 多客戶擴散加上模組含量提升，不靠單一平台；2027 年在產能擴到 80 億下仍能成長","2y":"2026 全年企業數據年增 ≥150%，2027 年企業數據營收高於 2026 年","5y":null,"10y":null,"threshold":"2026 全年年增 ≥150%；2027 年任一季企業數據營收不低於 Q3 2026 的 5.07 億美元","source":"公司季報新聞稿分市場營收、法說會","drift_rule":"兩年期：企業數據季營收較門檻偏離連 2 季 ≥5% 為削弱，連 3 季 ≥10% 為反轉"},{"id":"H2","text":"擴產與營運槓桿可以同時兌現：毛利率守在管理層 55～60% 模型內，非 GAAP 營益率繼續上升","2y":"2027 年毛利率每季 ≥55%，非 GAAP 營益率全年平均 ≥39%","5y":null,"10y":null,"threshold":"毛利率單季 ≥55%；非 GAAP 營益率 2027 年平均 ≥39%（Q3 2026 為 38.6%）","source":"公司季報新聞稿、法說會","drift_rule":"兩年期：毛利率或營益率較門檻偏離連 2 季 ≥5% 為削弱，連 3 季 ≥10% 為反轉"},{"id":"H3","text":"企業數據以外的曲線（通訊光模組與交換器、車用 48V 與區域架構、800V 高壓、記憶體介面）能在 2028 年 AI 資本支出放緩時接棒","2y":null,"5y":"2028 年企業數據以外分市場合計營收年增 ≥20%；800V 方案 2028 年產生可揭露營收","10y":null,"threshold":"企業數據以外合計營收 2028 年年增 ≥20%；800V 在 2028 年有營收","source":"公司季報新聞稿分市場營收、法說會","drift_rule":"五年期：合計營收成長較門檻偏離連 4 季 ≥5% 為削弱，連 6 季 ≥10% 為反轉"}],"R":[{"id":"R1","text":"旗艦 AI 平台供電份額再被分走：Infineon、Renesas 曾拿下 Blackwell 主要配額，ADI 以整合式穩壓切入，大客戶也可能自研；CSIMarket 稱某區隔份額下滑","h_ref":"H1","clock":"🔥","threshold":"企業數據季減 ≥15%，或公司、客戶確認旗艦平台主供應商換人","evidence_refs":["customer_second_source#3","competitive_share_entrants#3","substitute_technology#0","substitute_technology#1","customer_second_source#0"]},{"id":"R2","text":"AI 資本支出消化加全產業擴產：補助對手擴產縮短交期、對手數量增加、公司自己擴到 80 億；2028 年企業數據高基期回落","h_ref":"H1","clock":"🔥","threshold":"book-to-bill 低於 1，或企業數據年增由三位數降到 20% 以下","evidence_refs":["competitive_share_entrants#1","competitive_share_entrants#2"]},{"id":"R3","text":"通路與客戶集中：2025 年三大經銷商占 26%、18%、10%，合計 54%；與 OEM／ODM 無採購承諾，設計導入不保證持續採用","h_ref":"H1","clock":"⚡","threshold":"通路庫存超過 8 週，或單一經銷商超過 35%","evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#1","customer_second_source#1"]},{"id":"R4","text":"地緣與關稅：2025 年 92% 營收來自亞洲客戶，中國有生產與關鍵供應商，美中關稅、出口管制、台海局勢列於風險因子","h_ref":"H2","clock":"🐢","threshold":"管理層歸因關稅或管制使單季毛利率下修 ≥100bps，或營收指引因管制下修","evidence_refs":["reg_tariff_export#0","geo_supply_chain#0"]},{"id":"R5","text":"財報可信度：2026-02 審計委員會判定 FY2024 與 2025 各季財報不可信賴並重編（外國租稅優惠的遞延所得稅），證券集體訴訟與衍生訴訟未結；Q3 法說財務長改由 Tony Balow 擔任","h_ref":null,"clock":"⚡","threshold":"集體認證通過且不利和解；或再一次重編、內控重大缺失","evidence_refs":["major_events#0","major_events#1","lawsuit_class_action#0","sec_investigation_restatement#0","sec_investigation_restatement#1"]},{"id":"R6","text":"現金轉換率下滑：TTM FCF 利潤率 15.3%，低於 FY2025 的 23.8%，Q3 營業現金流 2.90 億只有非 GAAP 營業利益六成；擴產期存貨與營運資金吃現金","h_ref":"H2","clock":"🔥","threshold":"年度 FCF／GAAP 淨利連 2 年低於 0.75","evidence_refs":[]}],"single_thing":{"description":"Nvidia 下一代旗艦平台（Vera Rubin，VR200／R200）量產時，主供電份額由 KeyBanc 估的約七成降到 30% 以下，改由 Infineon、Renesas 或整合式穩壓方案為主","why_fatal":"企業數據占營收 42.1%，是成長與營益率擴張的主引擎；二手報導估旗艦平台約占 15% 營收，失守會同時打掉 H1 與市場給的成長溢價，是單一事件中對 EPS 與倍數衝擊最大者","if_happens":"企業數據在 2～3 季內下修 15～25%，FY2027 EPS 由 Base 40 降到約 34，Fwd P/E 向 30 倍收斂，股價約 1,020（約 −21%），若疊加產業消化再往 Bear 走；動作為減碼至觀察倉並重跑判斷","how_monitor":"每季企業數據營收（季減 ≥15% 為訊號）、管理層對旗艦平台的口徑、賣方通路調查與主要客戶的供電物料清單","probability":"20%（12～24 個月）"}},"appendix_a":{"growth_durability":8,"quality_score":8,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":36.75,"peg_fy2":1.66,"stress":{"pass":1,"total":3}},"eps_meta":{"base_eps_path":{"FY2025A":12.75,"FY2026E":27.55,"FY2027E":35.27,"FY2028E":41.1},"fy_end_month":12,"eps_basis":"FY2026E～FY2028E 為 Koyfin 非 GAAP 共識（分析師家數未載）；FY2025A 只有 GAAP 稀釋 EPS 12.75 可用（非 GAAP 年度值事實表未涵蓋），口徑不同，以此算的三年 CAGR 會高估；本判斷 PEG 改用 FY2026E 到 FY2028E 兩年 CAGR 22.1%"},"catalysts":[{"date":"2027-02","date_precision":"month","type":"guidance","event":"Q4 FY2026 財報與 Q1 2027 營收指引","impact":"高","watch":"Q1 指引中值是否 ≥14 億、企業數據全年是否達 150% 下限"},{"date":null,"date_precision":null,"type":"product","event":"Nvidia Vera Rubin 平台量產，旗艦供電份額見真章（時點事實表未涵蓋）","impact":"高","watch":"企業數據季營收、賣方通路調查份額"},{"date":"2027-09","date_precision":"quarter","type":"capacity","event":"產能達 80 億美元年化營收","impact":"中","watch":"營收是否跟上產能、存貨天數"},{"date":"2027-12","date_precision":"quarter","type":"product","event":"800V 資料中心架構初期營收（管理層稱 2027 年底到 2028）","impact":"中","watch":"800V 是否出現可揭露營收"}]}
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
