你是 DD 管線 v20 的判斷層閘（gate），標的 INCY（20261103）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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
- `f_kpi0_total_revenue_gaap`（q1_business）｜Total revenue (GAAP)＝1557.2 USD M｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000879169/000087916926000063/incy-q32026xexx991.htm（numbers.latest_quarter_kpis.items[0]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-29））
- `f_kpi1_non_gaap_operating_incom`（q1_business）｜Non-GAAP operating income＝-629.7 USD M｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000879169/000087916926000063/incy-q32026xexx991.htm（numbers.latest_quarter_kpis.items[1]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-29））
- `f_kpi2_gaap_operating_income`（q1_business）｜GAAP operating income＝-708.4 USD M｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000879169/000087916926000063/incy-q32026xexx991.htm（numbers.latest_quarter_kpis.items[2]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-29））
- `f_kpi3_gaap_eps_diluted`（q1_business）｜GAAP EPS (diluted)＝-3.86 USD｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000879169/000087916926000063/incy-q32026xexx991.htm（numbers.latest_quarter_kpis.items[3]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-29））
- `f_kpi6_fy2026_guidance_total_ne`（q1_business）｜FY2026 guidance: total net sales＝5,210–5,300 USD M｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000879169/000087916926000063/incy-q32026xexx991.htm（numbers.latest_quarter_kpis.items[6]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-29））
- `f_kpi7_fy2026_guidance_opzelura`（q1_business）｜FY2026 guidance: Opzelura net sales＝1,100–1,120 USD M｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000879169/000087916926000063/incy-q32026xexx991.htm（numbers.latest_quarter_kpis.items[7]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-29））
- `f_kpi8_fy2026_guidance_hematolo`（q1_business）｜FY2026 guidance: Hematology & Oncology net sales＝890–910 USD M｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000879169/000087916926000063/incy-q32026xexx991.htm（numbers.latest_quarter_kpis.items[8]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-29））
- `f_kpi9_fy2026_guidance_non_gaap`（q1_business）｜FY2026 guidance: non-GAAP R&D+SG&A opex＝4,625–4,695 USD M｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000879169/000087916926000063/incy-q32026xexx991.htm（numbers.latest_quarter_kpis.items[9]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-29））
- `f_peer_incy_gross_margin_pct`（q2_moat）｜INCY 毛利率＝92.69 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.INCY.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_incy_operating_margin_pct`（q2_moat）｜INCY 營業利益率＝11.66 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.INCY.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_earnings_recency`（q1_business）｜最近一次財報日＝2026-10-29 date｜期間與口徑：2026-10-29／距今 3 個交易日｜kind：realized
  - 來源：—（numbers.earnings_recency，as_of 2026-10-29）
- `f_peer_incy_fcf_margin_pct`（q2_moat）｜INCY FCF 利潤率＝11.31 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.INCY.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_vrtx_operating_margin_pct`（q2_moat）｜VRTX 營業利益率＝37.95 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.VRTX.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_regn_operating_margin_pct`（q2_moat）｜REGN 營業利益率＝26.87 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.REGN.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_bmrn_operating_margin_pct`（q2_moat）｜BMRN 營業利益率＝4.38 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.BMRN.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_exel_operating_margin_pct`（q2_moat）｜EXEL 營業利益率＝40.21 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.EXEL.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝3.58 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-10-31）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝8.74 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-10-31）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝9.06 USD/share｜期間與口徑：2026-10-31／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-10-31）
- `f_consensus_rev_fy1_pct`（q5_valuation）｜FY1 共識修正＝15.48 %｜期間與口徑：2026-10-31／兩份 Koyfin 快照之間的 EPS 修正幅度（3.1 → 3.58）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.fy1.revision_pct，as_of 2026-10-31）
- `f_consensus_rev_fy2_pct`（q5_valuation）｜FY2 共識修正＝0.34 %｜期間與口徑：2026-10-31／兩份 Koyfin 快照之間的 EPS 修正幅度（8.71 → 8.74）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.fy2.revision_pct，as_of 2026-10-31）
- `f_consensus_rev_fy3_pct`（q5_valuation）｜FY3 共識修正＝0.0 %｜期間與口徑：2026-10-31／兩份 Koyfin 快照之間的 EPS 修正幅度（9.06 → 9.06）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261031.xlsx（numbers.consensus_revision.fy3.revision_pct，as_of 2026-10-31）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝6036.48 USD m｜期間與口徑：2026-11-03／yfinance revenue_estimate 0y 平均（20 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝6277.74 USD m｜期間與口徑：2026-11-03／yfinance revenue_estimate +1y 平均（21 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi4_stock_based_compensation`（q1_business）｜Stock-based compensation＝69.8 USD M｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000879169/000087916926000063/incy-q32026xexx991.htm（numbers.latest_quarter_kpis.items[4]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-29））
- `f_kpi5_cash_equivalents_marketa`（q1_business）｜Cash, equivalents & marketable securities＝3854.6 USD M｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-29）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿（8-K Ex.99.1）https://www.sec.gov/Archives/edgar/data/0000879169/000087916926000063/incy-q32026xexx991.htm（numbers.latest_quarter_kpis.items[5]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-29））
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝-3817.16 USD m｜期間與口徑：2026-11-03／yfinance 最新一季：總債務 37.41、現金 3854.57（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_ev_m`（q5_valuation）｜目前企業價值 EV（市值＋淨負債）＝20433.26 USD m｜期間與口徑：2026-11-03／市值 24250.42 ＋ 淨負債 -3817.16｜kind：realized
  - 來源：—（numbers.capital_structure.ev_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝203.83 m shares｜期間與口徑：2026-11-03／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝118.97 USD｜期間與口徑：2026-11-02（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-11-02（RTH 收盤，UTC））
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝60.7 x｜期間與口徑：2026-11-02（RTH 收盤，UTC）／4 個年度端點內的分位＝10.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-11-02（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝10.0 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝4.03 x｜期間與口徑：2026-11-02（RTH 收盤，UTC）／4 個年度端點內的分位＝30.6｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝30.6 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝3.4 x｜期間與口徑：2026-11-02（RTH 收盤，UTC）／4 個年度端點內的分位＝23.4｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝23.4 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-11-02（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝33.23 x｜期間與口徑：2026-10-31／分母＝FY1 EPS 3.58，分子＝快照價 118.97｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-10-31）
- `f_ev_s_fwd`（q5_valuation）｜EV/S（EV ÷ FY1 共識營收）＝3.38 x｜期間與口徑：2026-11-03／f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）｜kind：estimate
  - 來源：—（numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m，as_of 2026-11-03）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝22.48 %｜期間與口徑：2026-11-02（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-11-02（RTH 收盤，UTC））
- `f_rsi14`（q5_valuation）｜RSI(14)＝54.28｜期間與口徑：2026-11-02（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-11-02（RTH 收盤，UTC））
- `f_ma_state`（q5_valuation）｜週線均線六態（decision_inputs.ma 必須等於此值）＝🟡｜期間與口徑：2026-11-03／timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）
  - 原文：「price 119.21 / W52 107.24 / W104 90.26 / W250 77.06 / W250 13週斜率 0.9%」
- `f_ma_w52`（q5_valuation）｜52 週均線＝107.24 USD｜期間與口徑：2026-11-03／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）
- `f_ma_w104`（q5_valuation）｜104 週均線＝90.26 USD｜期間與口徑：2026-11-03／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）
- `f_ma_w250`（q5_valuation）｜250 週均線＝77.06 USD｜期間與口徑：2026-11-03／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）
- `f_ma_slope_w250_pct`（q5_valuation）｜W250 13 週斜率＝0.9 %｜期間與口徑：2026-11-03／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-03）

### findings_digest 中方向為負或來源衝突的條目（13 條）
- `competitive_share_entrants#0`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K FY2025 披露：已收到 Apotex、Hikma、Sun、Granules 等多家學名藥廠對 JAKAFI 的 ANDA/NDA 通知函，Jakafi 面臨學名藥競爭風險
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-10）｜affects：moat_trend、thesis.R、decision_inputs.bear
- `competitive_share_entrants#1`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K 指出競爭對手包含大型藥廠與小型生技，資源多於 Incyte，可能開發出使其產品過時的藥物
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-10）｜affects：moat_trend、thesis.R
- `competitive_share_entrants#2`（competitive_share_entrants｜方向 -｜狀態 ok）：Fierce Pharma：Incyte 面對新競爭者並準備 Jakafi 專利懸崖（GSK Ojjaara 等）
  - 來源：Fierce Pharma（as_of 2026-01-01）｜affects：moat_trend、thesis.R
- `competitive_share_entrants#3`（competitive_share_entrants｜方向 -｜狀態 ok）：Fierce Pharma：Jakafi 趨近學名藥競爭，Incyte 更依賴 Opzelura
  - 來源：Fierce Pharma（as_of 2026-01-01）｜affects：moat_trend、valuation
- `customer_concentration_credit#0`（customer_concentration_credit｜方向 -｜狀態 ok）：FY2025 10-K：Jakafi/Opzelura 產品營收五大客戶占比 A 13%、B 9%、C 21%、D 18%、E 11%（合計約72%）；五大客戶占2025年底應收帳款54%（2024年底49%）。
  - 來源：SEC EDGAR 10-K FY2025 Item 8（as_of 2026-02-10）｜affects：decision_inputs.bear、thesis.R
- `regulatory_antitrust#2`（regulatory_antitrust｜方向 -｜狀態 ok）：FDA 對 Zynyz NSCLC sBLA 發出 Complete Response Letter，唯一理由為 Catalent Indiana 充填廠合規，非療效或安全性。
  - 來源：Incyte 8-K 2026-03-06 (Boardroom Alpha)（as_of 2026-03-06）｜affects：thesis.R、triggers
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：Incyte FY2025 10-K 風險因子揭露：營運及其CRO、供應商可能受國際貿易政策（關稅與貿易爭端、制裁、進出口許可要求）造成的業務中斷與不確定性影響。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-10）｜affects：decision_inputs.bear
- `reg_tariff_export#2`（reg_tariff_export｜方向 -｜狀態 ok）：Incyte 10-Q 風險揭露：ruxolitinib phosphate（Jakafi/Opzelura 活性成分）原料來自中國供應商，中美貿易爭端可能影響供應。
  - 來源：SEC EDGAR 10-Q 2026-09-30（as_of 2026-10-30）｜affects：decision_inputs.bear、thesis.R
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：Incyte 10-K 揭露 Jakafi 原料僅單一來源，並依賴單一或少數合格供應商（原料、API、成品）
  - 來源：Incyte Form 10-K FY2025（as_of 2026-02-15）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：Incyte 10-Q 風險因子提到關稅、制裁及俄烏與中東衝突可能干擾營運與供應商
  - 來源：Incyte Form 10-Q Q3 2026（as_of 2026-10-28）｜affects：thesis.R
- `end_markets#2`（end_markets｜方向 -｜狀態 ok）：Jakafi美國專利到期（LOE）約2028年12月，之後預期學名藥ruxolitinib侵蝕；公司目標2030年非Jakafi產品淨銷售$3–4B；ER劑型轉換目標3–5%
  - 來源：Fierce Pharma 'As Jakafi approaches generic competition, Incyte counts more on Opzelura'（as_of 2026-07-28）｜affects：thesis.R、decision_inputs.bear
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：10-K 稱生技製藥業競爭激烈且技術變化快速；合作夥伴可能追求替代技術或替代產品，而與公司產生衝突。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-10）｜affects：moat_trend、decision_inputs.bear
- `capital_markets_pricing#2`（capital_markets_pricing｜方向 -｜狀態 ok）：2026 年 2 月初始 guidance 低於當時共識（約 $5.52B；Opzelura 指引 $750–790M vs 共識 $801.5M）；Q2 後一來源稱 guidance 低於 $5.6B 共識，但該共識可能為上調前舊值，來源間不一致。
  - 來源：TIKR / 搜尋彙整（as_of 2026-02-15）｜affects：valuation、decision_inputs.bear

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 3 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/INCY_20261103/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":205.8,"bear_5y_price":57.8,"p_bull_pct":25,"p_bear_pct":30,"upside_5y_pct":-12.2,"ev5y_pct":-2.7,"irr_base_pct":-2.6,"asym_ratio":1.2,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":8.74,"pe":13.61,"basis":"起點用 FY2027E 共識 EPS 8.74 美元：判斷日距 FY2026 年底不到兩個月，未來 12 個月幾乎就是 FY2027。FY2026E 3.58 含 Vega 一次性費用，不採用。終端倍數同樣用前瞻一年口徑，套在 FY2031E 上。"},"eps":{"bull":[9.2,9.9,7.6,7.8,9.8],"base":[8.7,8.95,5.4,4.4,5.8],"bear":[8.3,8.2,4.0,2.8,3.4]},"pe":{"bull":21,"base":18,"bear":17},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0.0,"net_buyback":0.0},"second_stage":{"bull_cagr_pct":15,"base_cagr_pct":9},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### INCY_Q1_2009_Earnings_Call_20090507.md
- 2009-05-07｜CFO｜guidance：全年現金使用財測維持122–128百萬美元，不含潛在合作夥伴付款（原話："cash use guidance for the year remain unchanged"）
- 2009-05-07｜CFO｜margin：Q1期末現金與投資175.6百萬、當季現金使用42.2百萬，CFO稱符合計畫（原話："our cash use this quarter was 42.2 million"）
- 2009-05-07｜CFO｜margin：Q1 R&D費用29.6百萬，低於2008年Q1，聚焦近期價值程式（原話："R&D expense totaled 29.6 million"）
- 2009-05-07｜CFO｜guidance：CFO回答R&D費用走勢今年將相當平穩（原話："It should look pretty flat this year, Tom."）
- 2009-05-07｜CFO｜margin：CFO解釋Q1為現金消耗季節性最高季，因付息與營運資金支出（原話："So Q1 is seasonally the highest quarter for our burn."）
- 2009-05-07｜CFO｜risk：CFO承認可轉債餘額構成重大財務overhang（原話："represents a significant financial overhang"）
- 2009-05-07｜CFO｜capital_allocation：管理層稱有多種重組或減少可轉債的選項，處理債務將以股東價值最大化為焦點，但不公開討論（原話："will be focused on maximizing shareholder value"）
- 2009-05-07｜CEO｜guidance：已重新提交SPA，若FDA同意，預計上半年啟動myelofibrosis樞紐性Phase III（原話："we remain in a position to start our pivotal Phase III"）
- 2009-05-07｜CEO｜guidance：預期歐洲註冊試驗將於一個月左右內開始，每項試驗約需六個月收案（原話："take about six months to enroll each of these studies"）
- 2009-05-07｜CEO｜guidance：仍預期於2010年底或2011年初完成試驗並申報NDA（原話："filing the NDA in late 2010 or early 2011"）
- 2009-05-07｜CEO｜product：INCB28050口服JAK抑制劑類風濕關節炎六個月Phase II，預期2010上半年出結果（原話："results of the trial in the first half of 2010"）
- 2009-05-07｜CEO｜product：INCB13739糖尿病試驗中期分析摘要獲ADA晚期海報接受，最終數據預計6月初（原話："we expect to have the final data in early June"）
- 2009-05-07｜CEO｜product：424於PV與ET的Phase II已完成收案，預計ASH發表，管理層稱安全性與療效結果令人鼓舞（原話："This study is fully enrolled"）
- 2009-05-07｜CEO｜product：外用424乾癬Phase IIb結果預計夏末（原話："we look forward to having results late this summer"）
- 2009-05-07｜CEO｜commitment：JAK腫瘤計畫意圖保留北美權利，但若條件有吸引力會考慮美國以外合作（原話："It remains our intent to keep North American rights"）
- 2009-05-07｜CEO｜commitment：JAK發炎計畫可做全球授權，或保留部分適應症／分享下游經濟利益（原話："we could do a broad global licensing deal"）
- 2009-05-07｜CEO｜commitment：CEO結語列出最高優先：開始MF註冊試驗，並以合作改善財務狀況（原話："improve our financial position by partnering"）
- 2009-05-07｜CEO｜commitment：被問若無法與FDA達成SPA是否仍進行，CEO稱想要SPA但不拘泥（原話："We very much like to have the SPA. We are not wedded to it."）
- 2009-05-07｜CEO｜capital_allocation：c-MET前臨床資產合作為相當高優先，但對改善資產負債表的幫助不如發炎或MPD交易（原話："it doesn't move the needle as a pre-clinical entity"）
- 2009-05-07｜CEO｜capital_allocation：sheddase需待與Herceptin合用於轉移性乳癌的試驗完成後才較易取得價值；IDO尚未嘗試合作（原話："we've not attempted to partner at this point in time"）
- 2009-05-07｜CMO｜competition：CMO說明外用乾癬藥療效門檻：維他命D/A類似物約20%達clear或almost clear，近期核准藥約23%（原話："you get responses in the 20% range"）
- 2009-05-07｜CEO｜competition：CEO稱其c-MET分子是c-MET抑制劑中最佳（原話："we think we have the best molecule of the c-MET inhibitors"）
- 2009-05-07｜CEO｜risk：CEO說明13739中期分析僅涵蓋約35%最終收案病人，提醒勿先下假設（原話："interim analysis was done on about 35% of the patients"）
- 2009-05-07｜CMO｜risk：CMO稱FDA對SPA並非全有全無，其樂觀認為可核准或小幅修改（原話："we're pretty optimistic that we either get approval"）
- 2009-05-07｜CEO｜customer：13739夥伴洽談：因最終數據只需再七週，決定等到6月初再重新接觸對象（原話："We started to wait until early June"）
- 2009-05-07｜CEO｜customer：CEO稱JAK發炎計畫興趣濃厚（原話："There is a lot of interest in that program."）

### 問答異常語氣（迴避／改口／保留）
- INCY_Q1_2009_Earnings_Call_20090507.md｜問：第二版SPA的試驗設計與原先構想相比變動多少？｜答法：拒絕說明設計，稱待FDA同意後再提供清楚描述，僅重申NDA時程
- INCY_Q1_2009_Earnings_Call_20090507.md｜問：是否嘗試以有利條件回購可轉債，若無原因為何？｜答法：未回答是否嘗試回購，僅稱不願透露策略細節、以股東價值最大化為準
- INCY_Q1_2009_Earnings_Call_20090507.md｜問：JAK按適應症拆分授權是否被合作方視為問題？｜答法：稱難以深入，僅表示分子不同已將問題降到最低，不再進一步評論

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 4 | 2 |
| customer_second_source | found | 1 | 2 |
| customer_concentration_credit | found | 1 | 2 |
| supply_demand_durability | found | 2 | 2 |
| regulatory_antitrust | found | 3 | 3 |
| reg_tariff_export | found | 3 | 3 |
| geo_supply_chain | found | 2 | 2 |
| end_markets | found | 4 | 2 |
| substitute_technology | found | 2 | 2 |
| channel_business_model_shift | found | 1 | 1 |
| capital_markets_pricing | found | 6 | 4 |
| major_events | found | 4 | 4 |

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"status":"no_prior_dd"}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"INCY","date":"2026-11-03","schema":"v15.0","contract":"v19","company_name":"Incyte Corporation"},"oneliner":"Jakafi 占 2026 年淨銷售指引約六成，美國專利 2028 年底到期。FY2027E 13.6 倍看似便宜，其實套在到期前的高峰盈餘上。Base 情境 FY2031E EPS 5.8 美元×18 倍約 104 美元，低於現價；等 XR 轉換數據出來，或股價跌到 75 美元以下再談。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/INCY_20261103/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/INCY_20261103/scenario.json","answers":{"q1_business":{"verdict":"公司賺的是血液科與皮膚科處方藥的錢。Jakafi 約占 2026 年淨銷售指引六成，利潤靠美國專利與支付方淨價這一關守住；2028 年底專利到期後，這一關就鬆開了。","reasoning":"最新一季（2026 Q3）總營收 1,557.2 百萬美元，年增 14%，其中產品淨銷售約 13.2 億美元。分產品看：Jakafi 8.27 億（+4%，付費需求 +12%）；Opzelura 2.55 億（+36%，扣掉與 CMS 和解帶來的淨價改善後約 +21%）；血液腫瘤 2.35 億（+38%，其中 Niktimvo 0.67 億、Zynyz 0.58 億、Monjuvi 0.55 億）。總營收減產品淨銷售約 2.4 億美元，是權利金與合作收入。毛利：銷貨成本約占淨銷售 8%，TTM 毛利率 92.7%。營益：GAAP 營業虧損 708.4 百萬美元，主因是 Vega 收購的一次性 IPR&D 12.3 億美元；加回後本季營益率約 33%，算法是（−708.4＋1,230）÷1,557.2；FY2025 全年營益率 26.1%。2026 全年淨銷售指引 52.1～53.0 億美元，其中 Jakafi 指引 32.2～32.7 億，中點占比約 62%（3,245÷5,255）。這是集中度風險，不能當成 2029 年以後的護城河證據。單點依賴：上游 ruxolitinib 原料藥只有三家合格代工廠，部分原料來自中國；下游前五大客戶（批發商與專科藥局）約占產品營收 72%，最大兩家分別占 21% 與 18%，合計未過 40%。產業時鐘判 II（擴張），依據是慢性血液病與皮膚病的處方需求仍有雙位數成長（Jakafi 需求 +12%、Opzelura 處方 +24%）。供需持久性：需求面結構性持久；供給面可逆性高，專利一到期，同分子學名藥會一次進場。","fact_refs":["f_kpi0_total_revenue_gaap","f_kpi1_non_gaap_operating_incom","f_kpi2_gaap_operating_income","f_kpi3_gaap_eps_diluted","f_kpi6_fy2026_guidance_total_ne","f_kpi7_fy2026_guidance_opzelura","f_kpi8_fy2026_guidance_hematolo","f_kpi9_fy2026_guidance_non_gaap","f_peer_incy_gross_margin_pct","f_peer_incy_operating_margin_pct","f_earnings_recency"],"verdict_values":{"revenue_quality":"高。收入來自處方藥的經常性銷售，毛利率逾九成。但 2026 年 Opzelura 含與 CMS 和解的一次性沖回約 2.46 億美元，總營收另含權利金，看成長要用 pro forma 數字與產品淨銷售。","unit_econ_note":"每多賣一單位藥，邊際成本約為淨價的 8%，所以利潤幾乎全看淨價與專利期。Jakafi 淨銷售成長落後需求約 8 個百分點，代表淨價已經在讓步。","archetype":{"primary":"轉機/特殊情境","secondary":"品質複利成長","confidence":"中","fingerprint":"單一大藥專利到期前、靠第二產品與管線接棒的轉型期"},"industry":{"clock_phase":"II","sd_verdict_source":"需求面結構性持久：付費需求與處方都是雙位數成長（來源：2026 Q3 法說）。供給面可逆性高：Jakafi 美國專利約 2028 年 12 月到期，多家學名藥廠已遞申請（來源：10-K FY2025、Fierce Pharma）。","bargaining":{"up":"弱：原料藥與成品多半只有一家或少數幾家合格代工，ruxolitinib 原料藥有三家合格廠、部分原料在中國；公司以至少 24 個月庫存做緩衝。","down":"中偏弱：前五大客戶約占產品營收 72%，但它們只是通路。真正壓價的是 CMS、Medicaid 與商業保險：CMS 新模式年化約占 Jakafi 毛銷售 1%，Medicaid 改採國際參考價。","geo":"Opzelura 海外約占全年銷售 20%（不含一次性 CMS 影響）；歐洲 2026 年 7 月核准中度異位性皮膚炎，德國等市場 2027 年中起給付。232 條款對專利藥課關稅，與 HHS 簽定價協議者適用 0%，公司是否適用事實表未涵蓋。"},"profit_pool_dir":"往外流：2029 年起，Jakafi 的利潤池流向學名藥與支付方；公司內部的利潤來源由 Jakafi 轉向 Opzelura、血液腫瘤新藥與三期管線。","tam_table":{"expanded":false,"reason":"事實表未涵蓋骨髓增生性腫瘤、皮膚科、腸胃道腫瘤的 TAM 與滲透率；利潤池的遷移改由分部表與情境樹裡的 Jakafi 保留率處理。"}}}},"q2_moat":{"verdict":"護城河在縮減。最大利潤池 Jakafi 的專利保護 2028 年底到期；執行力在升、定價力在降，而新護城河（Opzelura 的處方網、突變專一抗體 989）還不夠大，接不了手。","reasoning":"機制：ruxolitinib 這個單一分子在專利期內的壟斷（口服 Jakafi＋外用 Opzelura），加上血液科與皮膚科的處方網。事實表沒有同業 ROIC，方向證據改用營益率代理：INCY TTM 營益率 11.7%，被 Vega 一次性費用壓低，FY2025 全年為 26.1%；同業 VRTX 38.0%、EXEL 40.2%、REGN 26.9%，對最強同業的差距是負的。執行力給 7 分：本季每個產品都年增，除 Jakafi 外核心業務 +30%，Jakafi XR 已核准上市，多個三期如期開跑；扣分在 Zynyz 肺癌補件因代工廠問題被 FDA 退件、CDK2 三期停止收案。定價力給 5 分：Jakafi 淨銷售 +4%，需求卻是 +12%，CMS 新模式與 Medicaid 國際參考價協議都在壓淨價；Opzelura 方面，管理層說 2027 年後價格以維持為主。趨勢：執行力擴大、定價力縮減，而定價力背後的專利 2028 年底歸零，所以合併判縮減。產業態勢分三條看：一是競爭惡化，Apotex、Hikma、Sun、Granules 已遞學名藥申請，GSK Ojjaara 在骨髓纖維化正面競爭；二是需求面持久，付費需求 +12%；三是法規與定價，包括 CMS 新模式、Medicaid 國際參考價、232 條款專利藥關稅。合起來的裁決是競爭惡化中。","fact_refs":["f_peer_incy_gross_margin_pct","f_peer_incy_operating_margin_pct","f_peer_incy_fcf_margin_pct","f_peer_vrtx_operating_margin_pct","f_peer_regn_operating_margin_pct","f_peer_bmrn_operating_margin_pct","f_peer_exel_operating_margin_pct","f_kpi0_total_revenue_gaap","f_kpi2_gaap_operating_income"],"verdict_values":{"moat":{"mechanism":"專利期內的單一分子壟斷（ruxolitinib：口服 Jakafi、外用 Opzelura），加上血液科與皮膚科的處方網（Opzelura 約 2 萬名處方醫師、超過 25 萬名使用者）。Jakafi 這一塊在 2028 年底後只剩 XR 劑型的轉換成本；989 等突變專一新藥是公司重建壟斷的嘗試。","execution":7,"pricing":5,"grade":"C","trend":"↓","trend_evidence":"定價力向下：Jakafi 淨銷售 +4%，付費需求卻是 +12%，差距來自 CMS 新模式與淨價讓步；Apotex、Hikma、Sun、Granules 等已遞學名藥申請通知，美國專利約 2028 年 12 月到期。執行力向上：除 Jakafi 外核心業務 +30%，每個產品都年增。但最大利潤池的保護兩年內歸零，合併判縮減。","competitor_notes":[{"name":"VRTX","strategy_note":"營益率與 FCF 率都約為 INCY 的三倍，研發密度卻較低，是單一治療領域壟斷做到極致的利潤結構；INCY 的研發密度高得多，代表它還在花錢找下一個壟斷。"},{"name":"REGN","strategy_note":"營益率 26.9%、研發密度 40%，可當多產品自研平台的參照；INCY 要在 2029 年後回到這個營益率，至少需要兩個三期資產成功。"},{"name":"BMRN","strategy_note":"營益率 4.4%、FCF 率卻有 21%，帳面利潤與現金落差大，跟 INCY 的 2024、2026 年一樣，不適合用當期本益比比較。"},{"name":"EXEL","strategy_note":"毛利率 96%、營益率 40%、FCF 率 46%，是這組同業裡最會把營收變成現金的公司。INCY 研發密度 57%（含 Vega），EXEL 是 33%：INCY 選擇把現金押在管線上，短期利潤率輸，賭的是 2030 年代。"},{"name":"GSK（Ojjaara）","strategy_note":"在骨髓纖維化與 Jakafi 正面競爭的 JAK 抑制劑，屬點對點競爭。真正的威脅是 2029 年上市的同分子學名藥，不是它。"}],"spread_notes":{"proxy":"營益率（TTM）","subject":"INCY 11.7%（含一次性 IPR&D）；FY2025 為 26.1%","best_peer":"EXEL 40.2%","direction":"差距為負；事實表只有單期數字，判斷不了是在收窄還是擴大"},"peer_na_reason":"事實表的同業對照只有毛利率、營益率、FCF 率與研發密度，沒有 ROIC 與投入資本，所以利差改用營益率代理。","threats":[{"level":"🔴","text":"同分子學名藥：Jakafi 美國專利約 2028 年 12 月到期，Apotex、Hikma、Sun、Granules 等已遞申請通知。到期後，藥局端可直接換成學名藥，XR 劑型是唯一緩衝。","p":"≥90%（2029 年上市的時點已知，不確定的是侵蝕有多深）","evidence_refs":["competitive_share_entrants#0","end_markets#2"]},{"level":"🟡","text":"GSK Ojjaara 等新的 JAK 抑制劑分食骨髓纖維化市場，屬點對點競爭。","p":"40%","evidence_refs":["competitive_share_entrants#2"]},{"level":"🟡","text":"資源更多的大藥廠可能讓公司產品過時（10-K 風險因子的一般性文字），實際落在管線上：胰臟癌有 pan-RAS 抑制劑 daraxonrasib，鉑抗卵巢癌已因 ADC 進展停掉 CDK2 三期。","p":"30%","evidence_refs":["competitive_share_entrants#1","substitute_technology#0"]},{"level":"🟡","text":"公司越來越依賴 Opzelura。Opzelura 同樣是 ruxolitinib，處方網是真的護城河，但 2026 年的淨價改善有一部分來自與 CMS 的和解，不是競爭力。","p":"30%","evidence_refs":["competitive_share_entrants#3"]}],"roic_durability":{"quadrant":"事實表未涵蓋投入資本，給不出數字。帳面看屬高利益率×高周轉（毛利率 92.7%、製造外包）；若把研發與收購 IPR&D 視為投入資本，則降為高利益率×低周轉。","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者（病患）、決策者（血液科、皮膚科醫師）、付款者（Medicare、Medicaid、商業保險）三個角色都成立。骨髓纖維化、真性紅血球增多症、移植物抗宿主病是需要、不是想要，延後治療的代價高。代理讀數：2026 Q3 Jakafi 付費需求 +12%、Opzelura 處方 +24%、新病患 +26%。要分開看的是：需求會留下，但目前的解決方案（品牌 Jakafi）2029 年起可以被同分子替代。"},{"item":"決策層級","level":"🔴","text":"替代性要在最小的決策單位看。學名藥上市後，換藥發生在藥局與藥品福利管理端，醫師不必重新決定，這一層的轉換成本近乎零。XR 劑型是把決策拉回醫師端的唯一工具，但 2026 年 9 月只占 Jakafi 系列約 3%，年底處方集覆蓋預計 >80%。Opzelura 的決策仍在醫師端（約 2 萬名處方醫師、25 萬名使用者），這一塊單看是 🟡。"},{"item":"價值鏈分配","level":"🟡","text":"專利期內，公司拿走價值鏈的大部分（毛利率 92.7%）。但支付方的份額在擴大：CMS 新模式年化約占 Jakafi 毛銷售 1%，Medicaid 改採國際參考價，Opzelura 的 Medicaid 回扣訴訟以和解收場。上游代工只有一家或少數幾家，這是供給風險，不是定價風險。"},{"item":"社會容忍度","level":"🟡","text":"高必要性加上高價格敏感度。Medicaid 國際參考價、232 條款專利藥關稅（簽定價協議者 0%），都顯示政治上限壓在經濟上限之下。公司選擇先簽協議，換取不受未來定價授權影響，並稱不影響 2026 年指引——等於付保費，代價是淨價有了天花板。優勢依賴專利授權，法源明確，到期即失效。"}],"roiic":"事實表未涵蓋投入資本與累計研發，算不出增量 ROIC。代理讀數：FY2022→FY2025 營業利益由約 5.9 億增到約 13.4 億美元（3,394.6×17.43%→5,141.2×26.12%）；但 FY2024 營益率曾掉到 2.39%（原因事實表未涵蓋），2026 年 Vega 的 12.3 億美元費用至今沒有營收，臨床階段收購的增量報酬尚未實現。","reinvest_rate":"接近 100%：TTM 研發密度 57%（含 Vega 一次性費用），現金主要流向研發與臨床階段收購。回購與股利事實表未涵蓋，算不出精確比率。","endo_ceiling":null,"formula_note":"內生成長率＝增量 ROIC×再投資率。兩個輸入都缺，天花板只能給方向：2029–2030 年因 Jakafi 到期為負，2031 年後取決於三期讀數。"}}}},"q3_growth":{"verdict":"成長跑道中等。2028 年前靠 Jakafi 的最後兩年、Opzelura 與血液腫瘤撐住；2029–2030 年 Jakafi 到期，盈餘下探；2031 年以後要看三期管線能不能接棒。","reasoning":"成長組成：量為主（Jakafi 需求 +12%、Opzelura 處方 +24%）；價為負（Jakafi 淨銷售只 +4%，Opzelura pro forma 成長裡價格小幅負貢獻）；併購補的是管線，不是營收。三年共識 EPS 從 FY2025A 6.41 到 FY2028E 9.06，年化約 12.2%，算法是（9.06÷6.41）^(1/3)−1。FY2026E 3.58 含 Vega 一次性費用，不能拿來算成長。缺口歸因：共識 FY2025A→FY2027E EPS +36%，營收只 +22%，差額來自費用槓桿，加上 Jakafi 到期前最後幾年的營收，所以歸為營益率擴張，不是再投資報酬。而且共識只到 FY2028，沒有涵蓋 2029 年的到期。內生天花板：事實表缺增量 ROIC 與再投資率，給不出數字；方向上，2029–2030 年為負。本次 Base 路徑從 FY2027E 8.70 到 FY2031E 5.80，年化約 −10%。跑道：Jakafi 這條約剩 2 年；第二條曲線（povorcitinib、989、G12D、latarcibart）都還在三期或審查中。管理層自己說 2030 年除 Jakafi 外核心業務目標 30～40 億美元，也說「還不能宣告勝利」，所以 5 年後的跑道給中等，不給寬。衰退信號亮 2 個：到期壓縮 TAM、EPS 成長快於營收；其餘多半事實表未涵蓋。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_fy1_pct","f_consensus_rev_fy2_pct","f_consensus_rev_fy3_pct","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_kpi6_fy2026_guidance_total_ne","f_kpi7_fy2026_guidance_opzelura","f_kpi8_fy2026_guidance_hematolo"],"verdict_values":{"growth":{"driver_mix":"量為主、價為負、併購補管線；2029 年起 Jakafi 量價同時下滑，成長全看第二產品與三期新藥。","runway_years":"約 2 年（Jakafi 專利 2028 年底到期）；第二條曲線的滲透率事實表未涵蓋，換算不出年限。","runway_post_y5":"🟡","endo_ceiling_basis":"事實表未涵蓋增量 ROIC 與再投資率。方向判斷：再投資率接近 100%（研發密度 57%，收購全數費用化），但 Vega 等臨床階段收購尚未產生營收；2029–2030 年內生成長為負，2031 年後取決於三期讀數。共識 2025–2028 年 12.2% 的成長不是再投資的成果，而是 Jakafi 到期前的最後高峰加上費用槓桿。","segments":[{"item":"Jakafi 系列（含 XR）","value":"2026 指引 32.2～32.7 億美元，約占淨銷售 62%。Q3 8.27 億（+4%）；XR 0.15 億，9 月占比約 3%。美國專利約 2028 年 12 月到期。"},{"item":"Opzelura","value":"2026 指引 11.0～11.2 億美元（含與 CMS 和解的一次性沖回約 2.46 億）。Q3 2.55 億（+36%，pro forma +21%）：美國 2.08 億、海外 0.47 億。"},{"item":"血液腫瘤（Niktimvo、Zynyz、Monjuvi 等）","value":"2026 指引 8.9～9.1 億美元；Q3 2.35 億（+38%）。"},{"item":"除 Jakafi 外核心業務合計","value":"Q3 4.90 億美元（+30%）；管理層目標 2030 年 30～40 億美元。"},{"item":"權利金與合作收入","value":"Q3 約 2.4 億美元，由總營收 1,557.2 百萬美元減產品淨銷售約 13.2 億推得；明細事實表未涵蓋。"}],"decay_signals":[{"item":"毛利率連 2 季年減","lit":null,"note":"事實表只有 TTM 毛利率 92.7%，沒有季度序列。"},{"item":"核心市占近 12 個月縮減","lit":false,"note":"Opzelura 新病患成長約為市場兩倍，品牌外用藥新病患份額 46%。"},{"item":"主力產品提價後銷量下滑","lit":false,"note":"Jakafi 是淨價讓步、需求 +12%，方向相反。"},{"item":"EPS 成長顯著高於營收成長","lit":true,"note":"共識 FY2025A→FY2027E EPS 年化約 16.8%，營收年化約 10.5%，差 6.3 個百分點。"},{"item":"FCF/NI 低於 0.75 連 2 年","lit":false,"note":"FY2025 約 1.03；FY2024 淨利過小、比值不具意義；FY2023 約 0.75。"},{"item":"SBC/營收高於 5% 且逐年上升","lit":false,"note":"Q3 約 4.5%（69.8÷1,557.2）；趨勢事實表未涵蓋。"},{"item":"TAM 萎縮或被替代技術壓縮","lit":true,"note":"Jakafi 品牌市場 2029 年起被學名藥壓縮；鉑抗卵巢癌因 ADC 進展停掉 CDK2 三期。"},{"item":"產業估值倍數近 3 年系統性下移","lit":null,"note":"事實表未涵蓋同業倍數序列。"},{"item":"維持性資本支出占 FCF 高於 60%","lit":false,"note":"沒有自有大型產能，製造外包。"},{"item":"停止投資新產能且收入 3 年內下滑","lit":false,"note":"研發與臨床投資仍在擴大。"}],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"現金多、稀釋低，但錢押在臨床階段收購上，報酬還沒兌現；資本配置中等。","reasoning":"FCF/NI：FY2025 約 1.03（13.30÷12.87 億），FY2023 約 0.75，FY2022 約 2.62；FY2024 淨利只有 0.33 億，比值不具比較意義。TTM FCF 利潤率 11.3%，被 Vega 的現金對價壓低。SBC：Q3 69.8 百萬美元，約占總營收 4.5%；年化約 2.8 億，占市值 242.5 億約 1.15%，低於 1.5% 門檻（這是毛稀釋，事實表沒有淨股數變化）。現金去向：期末現金與有價證券 3,854.6 百萬美元、債務約 37 百萬，淨現金約 38 億美元。2026 年最大一筆支出是 Vega 收購：現金對價約 12.7 億，另有最多 7.5 億銷售里程碑，前期款全數費用化。回購與股利事實表未涵蓋。計分三項：收購的已實現報酬不過（Vega 要到 2029 年初才有三期數據，目前報酬為零）；回購沒有資料；股權稀釋過關。","fact_refs":["f_kpi4_stock_based_compensation","f_kpi5_cash_equivalents_marketa","f_net_debt_m","f_ev_m","f_shares_diluted_m","f_peer_incy_fcf_margin_pct","f_kpi0_total_revenue_gaap"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":true,"passed":false,"input":"Vega 前期款約 12.5 億美元（現金對價約 12.7 億），2026 Q3 全數列為 IPR&D 費用，沒有營收；三期 2029 年初才讀數，已實現增量報酬為零，低於資金成本。"},{"name":"buyback_yield","applicable":null,"passed":null,"input":"事實表未涵蓋回購金額與均價。"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"Q3 SBC 69.8 百萬美元，年化約 2.8 億÷市值 242.5 億≈每年 1.15%（毛稀釋）。"}]},"governance":{"capital_returns":{"expanded":false,"reason":"事實表未涵蓋近三年的回購、股利與收購金額彙總。唯一可追的大額動作是 2026 年的 Vega 收購，已放進計分與反證處理。"}}}},"q5_valuation":{"verdict":"現價要求 2029 年後的谷底盈餘至少約 6.6 美元，而且市場還要給 18 倍。我只信到 5.8 美元，所以價格偏貴，我不信這個定價。","reasoning":"先處理分母。FY2026E 共識 3.58 美元含 Vega 一次性 IPR&D 12.3 億美元，trailing 60.7 倍與 forward 33.2 倍都失真，所以改用 FY2027E 8.74 美元：現價 118.97 對應 13.6 倍，FY2028E 9.06 對應 13.1 倍。淨現金約 38 億美元，約占市值 16%。問題是這兩年正是 Jakafi 到期前的最後高峰，便宜的論證不成立。三個情境：Base 路徑 FY2031E EPS 5.8 美元×18 倍約 104 美元，比現價低 12%；Bull 9.8 美元×21 倍約 206 美元（+73%）；Bear 3.4 美元×17 倍約 58 美元（−51%）。機率 25/45/30 加權後，5 年報酬約 −3%。12 個月看，FY2028E Base 8.95 美元×13.5 倍約 121 美元，約 +1.5%。年度端點分位（只有 4 個點，不是真正的五年分位）：EV/S 23.4、P/S 30.6、P/E 10.0，表面偏低，但分母同樣是到期前的高峰營收。PEG 用 FY2027E 13.6 倍÷三年共識 CAGR 12.2%，約 1.12，屬合理；但這個 CAGR 只算到 FY2028，沒有涵蓋到期。賣方查核：Investing.com 23 位分析師平均目標價 128.48 美元（+8%）；MarketBeat 7 月底約 113.6，Barchart 平均 127.1、最高 155。我和賣方的分歧在框架，不在事實：賣方用到期前的盈餘給倍數，我用到期後的谷底盈餘。動能：26 週 +22.5%，RSI 54，股價高於 52、104、250 週均線，均線排列成立，但 250 週斜率只有 +0.9%。事實表未涵蓋同業前瞻本益比，終端倍數只能對照本身 FY2027E 的 13.6 倍。","fact_refs":["f_price_at_dd","f_pe_current","f_pe_percentile","f_ps_current","f_ps_percentile","f_ev_s_current","f_ev_s_percentile","f_fwd_pe_latest","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_net_debt_m","f_ev_m","f_ev_s_fwd","f_week26_return_pct","f_rsi14","f_ma_state","f_ma_w52","f_ma_w104","f_ma_w250","f_ma_slope_w250_pct"],"verdict_values":{"valuation":{"basis":"前瞻本益比，分母用 FY2027E；FY2026E 含一次性 IPR&D，不採用","tier":"中型商業化生技（單一大藥到期前）","peers":{"expanded":false,"reason":"事實表的同業對照只有利潤率，沒有同業前瞻本益比或 EV/S，做不了跨公司的倍數錨；終端倍數改為對照本身 FY2027E 的 13.6 倍。"},"fwd_pe":33.23,"peg":1.12,"percentile_5y":23.4,"val_light":"🟠","val_light_derivation":"表面便宜（FY2027E 13.6 倍，EV/S 年度端點分位 23%），但分母是 Jakafi 到期前的高峰年。換成到期後的谷底盈餘，Base 5 年價約 104 美元，低於現價，機率加權 5 年約 −3%，所以判偏貴。分位只用 4 個年度端點，不是真正的五年分位。","upside_short_pct":1.5,"upside_mid_pct":-12.2,"denominator_disputed":true,"denominator_note":"FY2026E EPS 3.58 美元含 Vega 一次性 IPR&D 約 12.3 億美元（每股約 6 美元），也含 CMS 一次性沖回約 2.46 億美元；trailing 本益比同樣失真。改用 FY2027E 後，FY2027–2028E 又是到期前的高峰年，因此便宜論證無效。"}}},"q6_how_wrong":{"verdict":"最可能看錯的有兩處：一是 XR 轉換和 Opzelura 比預期強，Jakafi 保留率到 30%、核心業務 2030 年過 40 億美元；二是 989 的一線數據讓公司在骨髓纖維化重建壟斷。兩者任一成立，2031 年盈餘都會回到 9 美元以上。","reasoning":"三個視角的反證與裁決都寫在反證紀錄，這裡不重寫。最大回撤範圍 −35%～−60%，依據三點：一，股價回到 250 週均線 77.06 美元約 −35%，這不需要基本面惡化，只要市場提前把 2029 年的谷底定價；二，Bear 情境終點約 −51%；三，XR 轉換失敗與三期失利同時發生時，回撤可到 −60%。事實表未涵蓋歷史最大回撤、空方報告與未決訴訟金額。法說的三條迴避紀錄都來自 2009 年場次，是 17 年前的團隊，不拿來評現任管理層。價值陷阱風險：衰退信號亮 2 個（到期壓縮 TAM、EPS 成長快於營收），判中度。","fact_refs":["f_ma_w250","f_ma_w104","f_ma_w52","f_price_at_dd","f_week26_return_pct","f_rsi14"],"verdict_values":{"trap":{"verdict":"🟡","label":"到期前高峰盈餘撐出的低本益比"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":8.74,"pe":13.61,"basis":"起點用 FY2027E 共識 EPS 8.74 美元：判斷日距 FY2026 年底不到兩個月，未來 12 個月幾乎就是 FY2027。FY2026E 3.58 含 Vega 一次性費用，不採用。終端倍數同樣用前瞻一年口徑，套在 FY2031E 上。"},"eps":{"bull":[9.2,9.9,7.6,7.8,9.8],"base":[8.7,8.95,5.4,4.4,5.8],"bear":[8.3,8.2,4.0,2.8,3.4]},"pe":{"bull":21,"base":18,"bear":17},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0.0,"net_buyback":0.0},"second_stage":{"bull_cagr_pct":15,"base_cagr_pct":9},"max_dd":{"lo":-60,"hi":-35,"basis":"三個依據：一，股價回到 250 週均線 77.06 美元約 −35%，不需要基本面惡化，市場提前定價 2029 年谷底即可；二，Bear 情境終點約 −51%；三，XR 轉換失敗與三期失利同時發生時，再往下約 10 個百分點。事實表未涵蓋歷史最大回撤。","trigger_time":null},"basis":{"bull":"XR 保留 30%；Opzelura 與血液腫瘤讓除 Jakafi 外核心業務 2030 年超過 40 億美元；povorcitinib 2027 年上市；989 二線骨髓纖維化與 G12D 至少一個成功；費用率回落，營益率回到 30% 以上。終端 21 倍，反映 2030 年代重回成長。","base":"XR 保留約 20%；核心業務 2030 年約 33～34 億美元（管理層目標的下半段）；Jakafi 2029 年遭遇學名藥；研發維持高檔，營益率谷底約 17～20%，2031 年隨新藥上市回升。終端 18 倍：高於現值 13.6 倍，是因為分母從到期前高峰換成了到期後谷底。","bear":"XR 保留不到 10%；核心業務 2030 年約 26 億美元；989 或 G12D 三期失利，費用砍得慢。谷底盈餘中含大量淨現金帶來的利息，所以給 17 倍，相當於成長熄火後的倍數錨，而不是沿用現值 13.6 倍。"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"Jakafi 約占 2026 年淨銷售指引 62%；美國專利約 2028 年 12 月到期，Apotex、Hikma、Sun、Granules 等已遞學名藥申請通知；XR 占比在 2026 年 9 月只有約 3%。","assumption":"多頭假設 XR 能保住 Jakafi 的 10～30%，且除 Jakafi 外核心業務在 2030 年達到 30～40 億美元。","consequence":"若保留率不到 10%、核心業務只到 26 億美元，FY2031E EPS 約 3.4 美元，5 年後股價約 58 美元（−51%）。這是 5 年後虧掉一半最可能的劇本。","ruling":"採納，列為 Bear 路徑，機率 30%。這與唯一致命點在保留率上部分重疊；要再加上管線失利，才構成完整的虧一半故事。","watch":"XR 每季占比；除 Jakafi 外核心業務每季的年增率。","not_applicable_reason":null,"evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#3","end_markets#2"],"fact_refs":["f_kpi6_fy2026_guidance_total_ne"]},{"view":"論點成功但股東經濟變差","evidence":"Vega 前期款 12.5 億美元在 Q3 全數費用化，2029 年初才有三期數據；公司同時跑超過 10 個樞紐試驗，並說要「全額出資」；Jakafi 已與 CMS 簽 Medicaid 國際參考價協議；Opzelura 2027 年後的價格以維持為主。","assumption":"管線成功，每股盈餘就會跟著回升。","consequence":"就算 2030 年核心業務達 35 億美元，只要研發加上市費用維持在 36 億美元以上，營益率也只在 20% 上下，每股盈餘難回到 2027 年的水準。股東拿到的是更大的營收，不是更高的每股盈餘。","ruling":"部分採納。Base 已假設費用只小幅下降；Bull 要成立，營益率必須回到 30% 以上。","watch":"非 GAAP 研發加管銷費用指引占營收的比重；每筆收購的前期金額。","not_applicable_reason":null,"evidence_refs":["major_events#0","major_events#2","ma_merger#0"],"fact_refs":["f_kpi9_fy2026_guidance_non_gaap","f_kpi2_gaap_operating_income"]},{"view":"價格已反映太多","evidence":"26 週漲 22.5%，股價 118.97 美元高於 52、104、250 週均線；Investing.com 23 位分析師平均目標價 128.48 美元，上檔約 8%。FY2026E 共識上修 15.5%，但 FY2027E 只上修 0.3%、FY2028E 不動，代表市場沒有把今年的好表現延伸到到期之後。","assumption":"FY2027E 13.6 倍很便宜。","consequence":"這個便宜是假象：分母是到期前的兩個高峰年。用 FY2031E 谷底後的盈餘 5.8 美元×18 倍，只值約 104 美元。","ruling":"採納。價格偏貴，是現在不進場的主因。","watch":"股價距離 75 美元進場錨還有多遠。","not_applicable_reason":null,"evidence_refs":["capital_markets_pricing#3","capital_markets_pricing#4"],"fact_refs":["f_week26_return_pct","f_price_at_dd","f_consensus_rev_fy1_pct","f_consensus_rev_fy2_pct","f_consensus_rev_fy3_pct"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 None → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=None","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 None → 本次 118.97","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=None","side_b":"本次 price_at_dd=118.97","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"估值：低本益比 vs 到期後的谷底盈餘","cause":null,"prior_field":null,"side_a":"現在就買的最強論證：FY2027E 只有 13.6 倍，淨現金約 38 億美元（約市值 16%）；除 Jakafi 外核心業務 +30%，全年指引兩度上調；有六個三期資產，管理層說其中四個成功機率較高。若 989 在 CALR 突變骨髓纖維化取代 Jakafi、G12D 在胰臟癌成功，2031 年盈餘可回到 10 美元附近。","side_b":"這 13.6 倍套在 Jakafi 到期前的最後兩個高峰年。Jakafi 約占淨銷售 62%，XR 才 3%；學名藥 2029 年上市後，盈餘至少掉三成以上。三年共識只到 FY2028，看不到這一段。","ruling":"選 B 側。兩邊對 5 年盈餘的方向相反，屬不可調和。依據是公司揭露的三個數字：Jakafi 占比 62%、專利到期日、XR 占比 3%。Base FY2031E EPS 5.8 美元×18 倍約 104 美元，低於現價。卡住進場的單一條件，是價格高於到期後的 Base 價值。","evidence_level":"高：到期日、營收占比、XR 占比都來自公司揭露","settle_metric":"XR 占 Jakafi 系列的比重（每季）；除 Jakafi 外核心業務的單季淨銷售","if_then":["若 2027 Q4 XR 占比 ≥8%，且除 Jakafi 外核心業務單季 ≥6 億美元 → Base 2031 年盈餘上修到約 7 美元，重跑 DD，通過後首倉 2%","若股價先漲到 140 美元以上，而 XR 占比仍不到 5% → 不追","反向：若股價跌到 75 美元以下，而 XR 與核心業務數據沒有受損 → 重跑 DD 後分批反買，首倉 2%","若已持有，且 2027 Q4 XR 占比不到 5% → 清倉"],"evidence_refs":["end_markets#2","competitive_share_entrants#3","capital_markets_pricing#3","end_markets#0"]},{"axis":"管理層財測：年初低於共識 vs 之後兩度上調","cause":null,"prior_field":null,"side_a":"2026 年 2 月的初始淨銷售指引 47.7～49.4 億美元，低於當時共識（約 55.2 億，各來源口徑不一）；Opzelura 指引 7.5～7.9 億，低於共識的 8.015 億。","side_b":"Q2 上調到 51.3～52.6 億，Q3 再調到 52.1～53.0 億，Opzelura 調到 11.0～11.2 億。但 Q2 那次上調，大半來自與 CMS 和解的一次性沖回約 2.46 億美元。","ruling":"可調和，屬程度差異。年初指引偏保守；扣掉一次性沖回，實質上調幅度不大，Q3 的 Opzelura 與血液腫瘤上調才是真正來自需求。2027 年 2 月的指引即使低於共識，也不宜過度解讀。","evidence_level":"中：初始共識數字各來源不一致","settle_metric":"2027 全年指引與共識營收 62.8 億美元的落差","if_then":["若 2027 指引中點低於共識 5% 以上，且主因是 Jakafi 淨價 → Bear 機率提高到 35%"],"evidence_refs":["capital_markets_pricing#2","capital_markets_pricing#0","capital_markets_pricing#1","supply_demand_durability#1","major_events#1"]},{"axis":"Jakafi：需求成長 vs 淨銷售成長","cause":null,"prior_field":null,"side_a":"付費需求 +12%，各適應症都在成長，由真性紅血球增多症領頭。","side_b":"淨銷售只 +4%；CFO 說 CMS 新模式年化約占毛銷售 1%；Jakafi 另與 CMS 簽了 Medicaid 國際參考價協議。","ruling":"可調和。需求與價格方向相反，但兩者都成立，約 8 個百分點的差距就是淨價讓步。這支持定價力縮減的判斷，也代表到期前兩年的 Jakafi 營收不會像需求那樣成長。","evidence_level":"高：公司揭露","settle_metric":"Jakafi 淨銷售年增率減付費需求年增率","if_then":["若差距連 2 季擴大到 15 個百分點以上 → Base FY2027–2028 盈餘下修 5%"],"evidence_refs":["supply_demand_durability#0","major_events#2"]},{"axis":"管理層承諾與執行（新舊法說對照）","cause":null,"prior_field":null,"side_a":"2009-05-07 法說，當時的 CEO 說骨髓纖維化新藥將在「2010 年底或 2011 年初送件」，CFO 說可轉債是重大的財務壓力。本包沒有收錄這些承諾的結果。","side_b":"2026-10-29 法說，Pablo Cagnoni 說 axatilimab 併用 ruxolitinib 的一線移植物抗宿主病數據由 2026 Q4 延到 2027 Q1，理由是要在最相關的學會完整發表；CDK2 鉑抗卵巢癌三期停止收案；William Meury 說「還不能宣告勝利」。","ruling":"可調和。2009 年的場次距今 17 年，結果也未收錄，不拿來評現任團隊。現任團隊的延遲屬發表時點與競爭格局的調整，不是療效或安全問題；但同時跑超過 10 個樞紐試驗，執行風險管理層自己也承認。","evidence_level":"低：舊承諾沒有結果可對照","settle_metric":"EXCALIBUR-MF2 是否在 2026 年底前啟動；DAWN-302 是否在 2027 上半年啟動","if_then":["若兩者任一延後超過兩季 → H3 信心下調，Bull 機率降到 20%"],"evidence_refs":["regulatory_antitrust#2"]},{"axis":"Opzelura：處方網護城河 vs 法規帶來的淨價","cause":null,"prior_field":null,"side_a":"William Meury：約 2 萬名處方醫師、超過 25 萬人在用，「這就是護城河」；新病患成長約為市場兩倍，在品牌外用藥的新病患份額 46%。","side_b":"美國 Q3 +45% 裡，有一部分是與 CMS 和解後的淨價改善（pro forma 為 +25%）；Mohamed Issa 說 pro forma 下價格是小幅負貢獻，2027 年後價格以維持為主。","ruling":"可調和。需求面的護城河是真的（處方 +24%、新病患 +26%），但 2026 年的淨價順風是一次性的法規結果，不能外推。Base 只採用需求成長，價格假設持平。","evidence_level":"中","settle_metric":"Opzelura 美國 pro forma 成長率減處方成長率","if_then":["若 pro forma 成長連 2 季低於處方成長 10 個百分點以上 → 定價力再扣 1 分"],"evidence_refs":["end_markets#3","end_markets#0","major_events#1"]}],"triggers":[{"n":1,"text":"除 Jakafi 外核心業務是否走在 2030 年 30 億美元的路徑上","type":"假設驗證","maps_to":"H1","metric":"除 Jakafi 外核心業務的單季淨銷售","threshold":"2027 Q4 ≥6.0 億美元；連 2 季年增不到 15% 視為削弱","action":"達標：Base 的 2030 年核心業務上修到 35 億美元，重跑 DD；削弱：Bear 機率提高到 35%","source_freq":"季報（每季）","date":"2028-02"},{"n":2,"text":"XR 轉換速度","type":"假設驗證","maps_to":"H2","metric":"XR 占 Jakafi 系列淨銷售的比重","threshold":"2027 Q4 ≥8%","action":"達標且股價 ≤100 美元：重跑 DD，評估首倉 2%；不到 5%：不進場","source_freq":"季報與法說（每季）","date":"2028-02"},{"n":3,"text":"學名藥上市後，Jakafi 系列保留率跌破 10%","type":"Single Thing","maps_to":"Single Thing","metric":"學名藥上市後第 4 季的 Jakafi 系列淨銷售÷上市前一季","threshold":"不到 10%","action":"已持有：清倉；未持有：放棄事件型進場，只保留 75 美元的價格條件","source_freq":"季報","date":"2030-02","evidence_refs":["end_markets#2"]},{"n":4,"text":"代工廠合規出問題或原料藥斷料","type":"風險","maps_to":"R3","metric":"FDA 退件或警告信、斷貨、原料藥庫存政策","threshold":"Jakafi 或 Opzelura 任一發生","action":"減碼一半，等第一個解決時點","source_freq":"8-K／10-Q（事件觸發）","date":null,"evidence_refs":["regulatory_antitrust#2","geo_supply_chain#0","reg_tariff_export#2"]},{"n":5,"text":"學名藥提前上市","type":"清倉","maps_to":"R1","metric":"美國 ruxolitinib 學名藥的上市日","threshold":"早於 2028 年 12 月","action":"清倉","source_freq":"10-Q 法律程序揭露（每季）","date":"2028-12","evidence_refs":["competitive_share_entrants#0","end_markets#2"]},{"n":6,"text":"價格跌到到期後價值以下","type":"估值rearm","maps_to":"Base 情境","metric":"收盤價","threshold":"≤75 美元","action":"重跑 DD，通過後首倉 ≤2%","source_freq":"每日","date":null},{"n":7,"text":"989 一線骨髓纖維化數據，以及 FDA 對複合終點的意見","type":"假設驗證","maps_to":"H3","metric":"ASH 數據；一線樞紐試驗設計（2027 年初公布）","threshold":"數據足以啟動含 989 單藥或併用 ruxolitinib 的一線三臂試驗","action":"正面：Bull 機率提高到 30%；負面：Bull 機率降到 20%","source_freq":"學會發表與公司更新","date":"2027-03"},{"n":8,"text":"三期主要終點失敗","type":"清倉","maps_to":"R2","metric":"EXCALIBUR-MF2 或 DAWN-303 的主要終點","threshold":"任一失敗","action":"清倉","source_freq":"公司新聞稿（事件觸發）","date":"2029","evidence_refs":["competitive_share_entrants#1","substitute_technology#0"]},{"n":9,"text":"年度複審","type":"複審日期","maps_to":"全份","metric":"2026 Q4 財報與 2027 全年指引","threshold":"財報公布後","action":"重跑 DD","source_freq":"每年","date":"2027-02"}],"kill_metrics":[{"metric":"Jakafi XR 占 Jakafi 系列淨銷售的比重","bear_threshold":"2027 Q4 不到 5%（2026 年 9 月約 3%）","window":"2027 Q4 財報（2028 年 2 月）","source":"Incyte 季度新聞稿與法說","last_status":"ok"},{"metric":"除 Jakafi 外核心業務的單季淨銷售年增率","bear_threshold":"連 2 季不到 15%（2026 Q3 為 +30%）","window":"滾動 2 季","source":"Incyte 季度新聞稿（8-K Ex.99.1）","last_status":"ok"},{"metric":"Opzelura 美國 pro forma 淨銷售成長率減處方需求成長率","bear_threshold":"連 4 季 ≤−10 個百分點（2026 Q3 為 +25% 對 +24%）","window":"滾動 4 季","source":"Incyte 法說","last_status":"ok"},{"metric":"989 二線骨髓纖維化或 G12D 一線胰臟癌的樞紐試驗主要終點","bear_threshold":"任一失敗","window":"2028–2029","source":"公司新聞稿、學會發表","last_status":"unknown"},{"metric":"美國 ruxolitinib 學名藥上市日","bear_threshold":"早於 2028 年 12 月","window":"至 2028 年 12 月","source":"Incyte 10-Q／10-K 法律程序揭露","last_status":"ok"}],"evidence_dismissed":[{"ref":"customer_concentration_credit#0","reason":"這條證據量的是通路集中度，不是需求集中度。同一份 10-K 寫明產品賣給專科與零售藥局、專科經銷商和批發商，前五大客戶都是轉手商，最終處方由醫師與支付方決定。應收帳款占比由 49% 升到 54%，反映的是信用風險而非需求風險，而證據本身沒有任何呆帳或延遲付款紀錄。最大兩家的占比（21%、18%）已寫在「怎麼賺錢」的議價權段。"}],"action_conditions":{"rearm_trigger":"股價≤75 美元（以 Base 5 年價 104 美元計，年化約 7%），觸發後重跑 DD 再決定首倉","exec_line":"未持有：不追。股價 ≤75 美元，或 2027 Q4 XR 占比 ≥8% 且除 Jakafi 外核心業務單季 ≥6 億美元時，重跑 DD，首倉 ≤2%。已持有：2027 Q4 XR 占比不到 5%，或學名藥提前上市，即清倉。","holding_cap":"3%"}},"decision_inputs":{"signal":"C","ma":"🟡","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":true,"valuation_dependent":false,"market_wrong_reason_given":"市場用 FY2027E 13.6 倍判斷便宜，但三年共識只到 FY2028，沒有涵蓋 2029–2030 年 Jakafi 被學名藥侵蝕的那段。賣方平均目標價 128 美元，隱含到期後盈餘仍有 6.6 美元以上配 18 倍；我的 Base 只有 5.8 美元。","momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"股價 ≤75 美元；或 2027 Q4 XR 占 Jakafi 系列 ≥8%，讓 Base 盈餘上修後重算。","asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null},"decision_out":{"verdict":"迴避","role":"不持有","row_hit":"2","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='C'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":true,"basis":"thesis_irreconcilable=True"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":true,"basis":"moat_trend='↓', moat='C'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]}],"pacing":[],"holding_cap":null,"requires_critic":[]},"thesis":{"H":[{"id":"H1","text":"除 Jakafi 外的核心業務（Opzelura、Niktimvo、Zynyz、Monjuvi，加上 2027 年起的 povorcitinib）在 2030 年達到 30 億美元以上，補上 Jakafi 到期後的大半營收缺口。","2y":"FY2027 除 Jakafi 外核心淨銷售 ≥24 億美元（2026 Q3 年化約 19.6 億）","5y":"FY2030 ≥30 億美元（管理層目標 30～40 億的下緣）","10y":null,"threshold":"2027 Q4 單季 ≥6.0 億美元；連 2 季年增不到 15% 視為削弱","source":"公司季度新聞稿（8-K Ex.99.1）的分產品淨銷售","drift_rule":"2Y 口徑：TTM 偏離門檻連 2 季 ≥5% 為削弱、連 3 季 ≥10% 為反轉；5Y 口徑：連 4 季 ≥5% 為削弱、連 6 季 ≥10% 為反轉"},{"id":"H2","text":"Jakafi XR 在學名藥上市前轉過足夠的病患，讓 Jakafi 系列 2030 年保住 2028 年水準的 20% 以上。","2y":"2027 Q4 XR 占 Jakafi 系列 ≥8%（2026 年 9 月約 3%）","5y":"2030 年 Jakafi 系列淨銷售 ≥2028 年的 20%","10y":null,"threshold":"2027 Q4 XR 占比 ≥8%；不到 5% 視為反轉","source":"季報的 XR 淨銷售；法說揭露的 XR 占比與處方集覆蓋","drift_rule":"2Y 口徑：連 2 季低於當季路徑 ≥5% 為削弱、連 3 季 ≥10% 為反轉；5Y 口徑：學名藥上市後連 4 季保留率低於 20% 為削弱、連 6 季低於 10% 為反轉"},{"id":"H3","text":"六個三期資產中，至少兩個在 2029 年底前拿到核准或正面的樞紐讀數，讓公司在 2030 年代重回成長。","2y":"povorcitinib 美國化膿性汗腺炎核准（預期 2027 Q1），且 989 一線數據足以啟動一線樞紐試驗","5y":"989 二線骨髓纖維化（EXCALIBUR-MF2）或 G12D 一線胰臟癌（DAWN-303）至少一個正面","10y":"2030 年代的總營收超過 2028 年 Jakafi 高峰年","threshold":"2029 年底前 ≥2 個核准或正面樞紐讀數","source":"公司新聞稿、FDA 決定、ASH 與 ESMO 等學會發表","drift_rule":"10Y 口徑：跨 2 個年度未達標為削弱、跨 3 個年度為反轉；任一樞紐試驗失敗，立即重算情境機率"}],"R":[{"id":"R1","text":"Jakafi 被學名藥侵蝕得比預期快：多家學名藥廠已遞申請，美國專利約 2028 年 12 月到期，而 XR 占比還只有約 3%。","h_ref":"H2","clock":"🐢","threshold":"2027 Q4 XR 占比不到 5%，或學名藥上市日早於 2028 年 12 月","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#3","end_markets#2"]},{"id":"R2","text":"三期管線失利，或被競品壓過：大藥廠資源更多、技術變化快；胰臟癌有 pan-RAS 抑制劑 daraxonrasib，鉑抗卵巢癌已因 ADC 進展停掉 CDK2 三期。","h_ref":"H3","clock":"🐢","threshold":"989 二線骨髓纖維化或 DAWN-303 任一主要終點失敗","evidence_refs":["competitive_share_entrants#1","competitive_share_entrants#2","substitute_technology#0"]},{"id":"R3","text":"代工與原料藥的單一來源出事：Zynyz 肺癌補件已因 Catalent 充填廠合規問題被 FDA 退件；ruxolitinib 原料藥部分來自中國，關稅、制裁、地緣衝突都可能造成斷料。","h_ref":"H1","clock":"⚡","threshold":"Jakafi 或 Opzelura 因代工合規被退件、收到警告信或斷貨；或公司下修「至少 24 個月」的原料藥庫存政策","evidence_refs":["regulatory_antitrust#2","reg_tariff_export#0","reg_tariff_export#2","geo_supply_chain#0","geo_supply_chain#1"]},{"id":"R4","text":"美國藥價政策壓縮淨價：CMS 新模式、Jakafi 的 Medicaid 國際參考價協議、232 條款專利藥關稅。","h_ref":"H1","clock":"🔥","threshold":"Opzelura 美國 pro forma 淨銷售成長連 4 季落後處方需求成長 10 個百分點以上，或 Jakafi 淨銷售在 2029 年前轉為年減","evidence_refs":["major_events#2","reg_tariff_export#1"]},{"id":"R5","text":"收購花了錢卻沒換到營收：Vega 前期款 12.5 億美元（約市值 5%）全數費用化，2029 年初才有三期數據；若再做同類收購，現金與每股盈餘都會被吃掉。","h_ref":"H3","clock":"🐢","threshold":"再出現單筆前期款超過 10 億美元的臨床階段收購，且 latarcibart 三期失敗","evidence_refs":["major_events#0","ma_merger#0"]}],"single_thing":{"description":"Jakafi 學名藥 2029 年上市後，Jakafi 系列（含 XR）的保留率跌破管理層目標的下緣 10%。","why_fatal":"Jakafi 約占 2026 年淨銷售指引 62%，毛利率逾九成。保留率 10% 與 30% 之間差約 7 億美元營收，換算 FY2031E EPS 約 2.3 美元，是情境樹裡最大的單一敏感項，大於任何一個管線資產在 2031 年前的貢獻。","if_happens":"Base FY2031E EPS 由 5.8 美元降到約 3.5 美元，接近 Bear 路徑。已持有就清倉；未持有就放棄事件型進場，只保留 75 美元的價格條件，觸發時重跑 DD。","how_monitor":"每季追蹤 XR 的淨銷售與占比（2026 年 9 月約 3%，全年目標約 5,000 萬美元，年底處方集覆蓋預計 >80%）；2027 Q4 占比不到 5% 是先行警訊。","probability":"12–24 個月內不會定案（學名藥 2029 年才上市）。以目前約 3% 的轉換速度推估，最終跌破 10% 的機率約 35%。"}},"appendix_a":{"growth_durability":4,"quality_score":6,"ai_risk":"🟢","long_term_confidence":"低","fpe_fy2":13.61,"peg_fy2":1.12,"stress":{"pass":1,"total":3}},"eps_meta":{"base_eps_path":{"FY2025A":6.41,"FY2026E":3.58,"FY2027E":8.74,"FY2028E":9.06},"fy_end_month":12,"eps_basis":"Koyfin 共識快照（2026-10-31），分析師家數事實表未涵蓋；FY2025A 取年報稀釋 EPS；FY2026E 含 Vega 一次性 IPR&D。三年 CAGR 用 FY2025A→FY2028E 計算，約 12.2%。"},"catalysts":[{"date":"2026-12","date_precision":"month","type":"product","event":"ASH 公布 989 一線骨髓纖維化數據（約 55 名病患，含單藥與併用 ruxolitinib）","impact":"高","watch":"SVR35、TSS50 與貧血改善，能否支持一線三臂樞紐試驗"},{"date":"2026-12","date_precision":"quarter","type":"product","event":"ruxolitinib 乳膏用於輕中度化膿性汗腺炎、povorcitinib 用於結節性癢疹的三期頂線結果","impact":"中","watch":"管理層估計化膿性汗腺炎可為 Opzelura 增加 0.5～1 億美元"},{"date":"2026-12","date_precision":"quarter","type":"regulatory","event":"povorcitinib 歐洲化膿性汗腺炎核准（CHMP 已給正面意見）；EXCALIBUR-MF2 啟動","impact":"中","watch":"二線骨髓纖維化三期能否如期收進第一位病患"},{"date":"2027-02","date_precision":"month","type":"guidance","event":"2026 Q4 財報與 2027 全年指引","impact":"高","watch":"Jakafi 指引與 XR 占比；除 Jakafi 外核心業務的指引是否 ≥24 億美元"},{"date":"2027-03","date_precision":"quarter","type":"regulatory","event":"povorcitinib 美國化膿性汗腺炎、Monjuvi 一線瀰漫性大 B 細胞淋巴瘤預期核准","impact":"高","watch":"povorcitinib 的標籤是否同時涵蓋用過與未用過生物製劑的兩群病患"},{"date":"2027-03","date_precision":"quarter","type":"product","event":"axatilimab 併用 ruxolitinib 的一線慢性移植物抗宿主病二期數據","impact":"低","watch":"反應能維持多久"},{"date":"2028-12","date_precision":"month","type":"other","event":"Jakafi 美國專利約在此時到期，學名藥可上市","impact":"高","watch":"XR 占比與學名藥實際上市日"},{"date":"2029-03","date_precision":"quarter","type":"product","event":"latarcibart（類血友病）三期頂線；NEXERA-303（890 一線 MSS 大腸癌）2029 年頂線","impact":"中","watch":"Vega 收購是否開始有回報"}]}
```

---

## ⑤ 覆蓋面（程式判定，你回的 ⑤ 燈號會被覆寫）

燈號 🟢：核心軸皆有證據或不適用，非核心軸也沒有空軸。plan 時 archetype 為「品質複利成長」、判斷者歸「轉機/特殊情境」，轉機/特殊情境 的專屬核心軸未採證（不計燈號）：turnaround_catalyst_timeline、turnaround_liquidation_floor。

⑤ 的 reason 只需評論：空軸的查詢詞是否切題、判斷有沒有交代缺口對結論的影響。

---

## 尾段：回覆格式

只回一個 JSON 陣列，①–⑧ 每條一個元素，八個全出，不得跳號、不得多列，陣列外不得有任何文字（不加前言、不加 markdown 圍欄、不加附註）：

```json
[{"item": "①", "light": "🔴|🟡|🟢", "judgment_path": "$.路徑", "reason": "一句話"}]
```
