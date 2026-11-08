你是 DD 管線 v20 的判斷層閘（gate），標的 HUBS（20261108）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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
- `f_kpi0_gaap`（q1_business）｜營收（GAAP）＝947.6 USD M｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 財報新聞稿（8-K Ex.99.1，IR: ir.hubspot.com）https://www.sec.gov/Archives/edgar/data/0001404655/000119312526447249/hubs-ex99_1.htm（numbers.latest_quarter_kpis.items[0]，as_of Q3 2026（季末 2026-09-30，公告於 2026-11-04））
- `f_kpi1_non_gaap`（q1_business）｜Non-GAAP 營業利益＝214.2 USD M｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 財報新聞稿（8-K Ex.99.1，IR: ir.hubspot.com）https://www.sec.gov/Archives/edgar/data/0001404655/000119312526447249/hubs-ex99_1.htm（numbers.latest_quarter_kpis.items[1]，as_of Q3 2026（季末 2026-09-30，公告於 2026-11-04））
- `f_kpi2_non_gaap`（q1_business）｜Non-GAAP 營業利益率＝22.6 %｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 財報新聞稿（8-K Ex.99.1，IR: ir.hubspot.com）https://www.sec.gov/Archives/edgar/data/0001404655/000119312526447249/hubs-ex99_1.htm（numbers.latest_quarter_kpis.items[2]，as_of Q3 2026（季末 2026-09-30，公告於 2026-11-04））
- `f_kpi3_gaap`（q1_business）｜GAAP 營業利益＝71.9 USD M｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 財報新聞稿（8-K Ex.99.1，IR: ir.hubspot.com）https://www.sec.gov/Archives/edgar/data/0001404655/000119312526447249/hubs-ex99_1.htm（numbers.latest_quarter_kpis.items[3]，as_of Q3 2026（季末 2026-09-30，公告於 2026-11-04））
- `f_kpi4_gaap`（q1_business）｜GAAP 營業利益率＝7.6 %｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 財報新聞稿（8-K Ex.99.1，IR: ir.hubspot.com）https://www.sec.gov/Archives/edgar/data/0001404655/000119312526447249/hubs-ex99_1.htm（numbers.latest_quarter_kpis.items[4]，as_of Q3 2026（季末 2026-09-30，公告於 2026-11-04））
- `f_kpi7`（q1_business）｜客戶數＝311704 家｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 財報新聞稿（8-K Ex.99.1，IR: ir.hubspot.com）https://www.sec.gov/Archives/edgar/data/0001404655/000119312526447249/hubs-ex99_1.htm（numbers.latest_quarter_kpis.items[7]，as_of Q3 2026（季末 2026-09-30，公告於 2026-11-04））
- `f_kpi8_non_gaap`（q1_business）｜訂閱毛利率（Non-GAAP）＝85.4 %｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 財報新聞稿（8-K Ex.99.1，IR: ir.hubspot.com）https://www.sec.gov/Archives/edgar/data/0001404655/000119312526447249/hubs-ex99_1.htm（numbers.latest_quarter_kpis.items[8]，as_of Q3 2026（季末 2026-09-30，公告於 2026-11-04））
- `f_kpi10_q4_2026`（q1_business）｜指引：Q4 2026 營收＝946.0 USD M（區間 945.0–947.0）｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司 Q3 2026 財報新聞稿（8-K Ex.99.1，IR: ir.hubspot.com）https://www.sec.gov/Archives/edgar/data/0001404655/000119312526447249/hubs-ex99_1.htm（numbers.latest_quarter_kpis.items[10]，as_of Q3 2026（季末 2026-09-30，公告於 2026-11-04））
- `f_kpi11_fy2026`（q1_business）｜指引：FY2026 營收＝3686.0 USD M（區間 3,685–3,687）｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司 Q3 2026 財報新聞稿（8-K Ex.99.1，IR: ir.hubspot.com）https://www.sec.gov/Archives/edgar/data/0001404655/000119312526447249/hubs-ex99_1.htm（numbers.latest_quarter_kpis.items[11]，as_of Q3 2026（季末 2026-09-30，公告於 2026-11-04））
- `f_peer_hubs_gross_margin_pct`（q2_moat）｜HUBS 毛利率＝83.02 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.HUBS.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_hubs_operating_margin_pct`（q2_moat）｜HUBS 營業利益率＝5.45 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.HUBS.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_hubs_fcf_margin_pct`（q2_moat）｜HUBS FCF 利潤率＝18.89 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.HUBS.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_crm_operating_margin_pct`（q2_moat）｜CRM 營業利益率＝21.52 %｜期間與口徑：TTM ending 2026-07-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CRM.operating_margin_pct，as_of TTM ending 2026-07-31（4季加總））
- `f_peer_crm_fcf_margin_pct`（q2_moat）｜CRM FCF 利潤率＝34.49 %｜期間與口徑：TTM ending 2026-07-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CRM.fcf_margin_pct，as_of TTM ending 2026-07-31（4季加總））
- `f_peer_now_gross_margin_pct`（q2_moat）｜NOW 毛利率＝73.08 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.NOW.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_now_fcf_margin_pct`（q2_moat）｜NOW FCF 利潤率＝30.78 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.NOW.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
- `f_peer_team_gross_margin_pct`（q2_moat）｜TEAM 毛利率＝84.83 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.TEAM.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_team_operating_margin_pct`（q2_moat）｜TEAM 營業利益率＝0.16 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.TEAM.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_mndy_gross_margin_pct`（q2_moat）｜MNDY 毛利率＝88.74 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MNDY.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_mndy_fcf_margin_pct`（q2_moat）｜MNDY FCF 利潤率＝21.56 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MNDY.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝13.3 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-11-07）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝16.82 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-11-07）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝20.21 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-11-07）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝3687.28 USD m｜期間與口徑：2026-11-08／yfinance revenue_estimate 0y 平均（29 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝4108.03 USD m｜期間與口徑：2026-11-08／yfinance revenue_estimate +1y 平均（31 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi5_non_gaap_fcf`（q4_capital）｜Non-GAAP 自由現金流（FCF）＝188.0 USD M｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 財報新聞稿（8-K Ex.99.1，IR: ir.hubspot.com）https://www.sec.gov/Archives/edgar/data/0001404655/000119312526447249/hubs-ex99_1.htm（numbers.latest_quarter_kpis.items[5]，as_of Q3 2026（季末 2026-09-30，公告於 2026-11-04））
- `f_kpi6_sbc`（q4_capital）｜SBC（股權報酬費用）＝127.1 USD M｜期間與口徑：Q3 2026（季末 2026-09-30，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 Q3 2026 財報新聞稿（8-K Ex.99.1，IR: ir.hubspot.com）https://www.sec.gov/Archives/edgar/data/0001404655/000119312526447249/hubs-ex99_1.htm（numbers.latest_quarter_kpis.items[6]，as_of Q3 2026（季末 2026-09-30，公告於 2026-11-04））
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝-1072.72 USD m｜期間與口徑：2026-11-08／yfinance 最新一季：總債務 224.04、現金 1296.76（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝48.84 m shares｜期間與口徑：2026-11-08／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝200.61 USD｜期間與口徑：2026-11-06（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-11-06（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝15.08 x｜期間與口徑：2026-11-07／分母＝FY1 EPS 13.3，分子＝快照價 200.61｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-11-07）
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝48.46 x｜期間與口徑：2026-11-06（RTH 收盤，UTC）／2 個年度端點內的分位＝0.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-11-06（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝0.0 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 2 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ps_current`（q5_valuation）｜P/S（現值）＝2.73 x｜期間與口徑：2026-11-06（RTH 收盤，UTC）／4 個年度端點內的分位＝0.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ps，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝0.0 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ev_s_current`（q5_valuation）｜EV/S（現值）＝2.43 x｜期間與口徑：2026-11-06（RTH 收盤，UTC）／4 個年度端點內的分位＝0.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.ev_s，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝0.0 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 4 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ev_s_fwd`（q5_valuation）｜EV/S（EV ÷ FY1 共識營收）＝2.37 x｜期間與口徑：2026-11-08／f_ev_m ÷ f_rev_consensus_fy1_m（前瞻口徑；f_ev_s_current 是 trailing 12 個月營收口徑）｜kind：estimate
  - 來源：—（numbers.capital_structure.ev_m ÷ revenue_consensus.fy1.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_ev_m`（q5_valuation）｜目前企業價值 EV（市值＋淨負債）＝8724.36 USD m｜期間與口徑：2026-11-08／市值 9797.08 ＋ 淨負債 -1072.72｜kind：realized
  - 來源：—（numbers.capital_structure.ev_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_consensus_rev_fy1_pct`（q5_valuation）｜FY1 共識修正＝0.0 %｜期間與口徑：2026-11-07／兩份 Koyfin 快照之間的 EPS 修正幅度（13.3 → 13.3）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.fy1.revision_pct，as_of 2026-11-07）
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝0.15 %｜期間與口徑：2026-08-13 → 2026-11-07／FY1 共識 EPS 13.28 → 13.3（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-11-07）
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝1.66 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-11-06（RTH 收盤，UTC））
- `f_rsi14`（q5_valuation）｜RSI(14)＝33.76｜期間與口徑：2026-11-06（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ma_w250`（q5_valuation）｜250 週均線＝445.12 USD｜期間與口徑：2026-11-08／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）
- `f_ma_state`（q5_valuation）｜週線均線六態（decision_inputs.ma 必須等於此值）＝❌｜期間與口徑：2026-11-08／timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）
  - 原文：「price 200.61 / W52 256.6 / W104 425.37 / W250 445.12 / W250 13週斜率 -1.0%」
- `f_ma_w52`（q5_valuation）｜52 週均線＝256.6 USD｜期間與口徑：2026-11-08／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-11-08）
- `f_consensus_rev_fy2_pct`（q5_valuation）｜FY2 共識修正＝0.0 %｜期間與口徑：2026-11-07／兩份 Koyfin 快照之間的 EPS 修正幅度（16.82 → 16.82）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.fy2.revision_pct，as_of 2026-11-07）

### findings_digest 中方向為負或來源衝突的條目（20 條）
- `competitive_share_entrants#0`（competitive_share_entrants｜方向 -｜狀態 ok）：HubSpot 10-K FY2025 的競爭對手清單新增「AI agent 提供者」與「AI-native CRM 及工作流自動化新創」，並提到通用 LLM、vibe coding 等非專業方案可能搶單。
  - 來源：SEC EDGAR 10-K FY2025 Item 1 Business（as_of 2026-02-11）｜affects：moat_trend、decision_inputs.bear
- `competitive_share_entrants#1`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K 風險因子：公司可能面對依賴通用 LLM、生成式 AI 與通用 agent 的非專業方案競爭，需說服客戶其產品優於 vibe coding 等替代；對手可能以綑綁近零成本提供平台，迫使降價。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A Risk Factors（as_of 2026-02-11）｜affects：moat_trend、thesis.R、decision_inputs.bear
- `competitive_share_entrants#2`（competitive_share_entrants｜方向 -｜狀態 ok）：SaaStr 2026 摘要稱多數現今 YC 新創已不使用 Salesforce 或 HubSpot（新進入者／AI-native CRM 趨勢）。
  - 來源：NextGenABM: key takeaways from SaaStr AI 2026（as_of 2026-05-18）｜affects：moat_trend、decision_inputs.bear
- `customer_concentration_credit#0`（customer_concentration_credit｜方向 -｜狀態 ok）：Solutions Partners 及其轉介客戶約占 2025 年營收 49%（占客戶數約 25%），屬通路集中而非單一客戶集中。
  - 來源：SEC EDGAR 10-K FY2025 Item 1（as_of 2026-02-11）｜affects：thesis.R、decision_inputs.bear
- `supply_demand_durability#1`（supply_demand_durability｜方向 -｜狀態 ok）：Q2'26 NRR 為102%，較去年同期降1個百分點；管理層預期全年 NRR 約與去年持平。Q2 淨新增客戶7,000，低於預期，原因為轉換率較弱與買方猶豫（來自第三方摘要）。
  - 來源：HUBS 2Q26 AI Summary (platformaeronaut)（as_of 2026-08-05）｜affects：moat_trend、decision_inputs.bear
- `supply_demand_durability#2`（supply_demand_durability｜方向 -｜狀態 ok）：Gartner（轉述）：2030年前企業 SaaS 支出逾40%將脫離純席位計價；Bloomberg Intelligence 預期定價由席位轉向用量／成果計價。屬產業結構性轉變論述（二手轉述）。
  - 來源：Bloomberg Intelligence Agentic AI Deep Dive; secondary coverage（as_of 2026-01-01）｜affects：moat_trend、thesis.R
- `regulatory_antitrust#2`（regulatory_antitrust｜方向 -｜狀態 ok）：HubSpot 2026 年 10-Q 風險因子提及州級 AI 法規（加州、德州 2026 生效，Colorado 延至 2027-01-01）拼湊式立法。
  - 來源：SEC EDGAR 10-Q 2026-09-30（as_of 2026-11-05）｜affects：thesis.R
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：HubSpot 的平台主要功能由 AWS（北維吉尼亞、法蘭克福）與 Google Cloud（法蘭克福）第三方資料中心承載（FY2021 10-K 文字）
  - 來源：HubSpot 10-K FY2021（as_of 2022-02-25）｜affects：thesis.R、decision_inputs.bear
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：2025-10-20 AWS us-east-1 大規模中斷影響 HubSpot 主要基礎設施所在區域，並在 HubSpot 內部任務處理系統引發連鎖問題；HubSpot 啟動可靠度改善計畫
  - 來源：HubSpot Product blog: incident report for october 20 2025（as_of 2025-10-30）｜affects：thesis.R、decision_inputs.bear
- `end_markets#0`（end_markets｜方向 -｜狀態 ok）：Q3 2026 專業服務及其他營收 $17.3M、年減3%，因技術顧問服務減少、Payments 費用部分抵銷；總營收年增17%
  - 來源：HubSpot 10-Q 2026-09-30（as_of 2026-11-05）｜affects：thesis.R
- `end_markets#2`（end_markets｜方向 -｜狀態 ok）：Q4 2026 營收指引 $945.0–947.0M，年增12%（較 Q3 17% 減速）
  - 來源：HubSpot Q3 2026 8-K ex99.1（搜尋摘要轉述）（as_of 2026-11-05）｜affects：valuation、thesis.R
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：HubSpot 10-K(FY2025)風險因子：承認競爭者可能以新AI技術使其產品失去競爭力或過時，並面對通用LLM、generative AI、通用agent及vibe coding自建軟體等非專業替代方案。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-02-11）｜affects：moat_trend、thesis.R、decision_inputs.bear
- `channel_business_model_shift#1`（channel_business_model_shift｜方向 -｜狀態 ok）：2026 年 HubSpot 將旗艦 Breeze AI agent 轉向結果導向計價（客戶在 agent 完成任務時付費），底層仍為席位加點數（credits）；第三方報導指出宣布 AI 計價變動後股價大跌。
  - 來源：WebSearch 摘要（彙整 Search Engine Journal／第三方追蹤站；letsdatascience 等）（as_of 2026-05-07）｜affects：valuation、thesis.R
- `capital_markets_pricing#0`（capital_markets_pricing｜方向 -｜狀態 ok）：2026-08-05 Q3 指引：營收 $924–925M 低於共識 $941.2M；EPS $3.25–3.27 高於共識 $2.99；FY26 EPS 指引 $13.23–13.31（MarketBeat 所列共識 11.37，口徑不一）
  - 來源：MarketBeat, HubSpot issues Q3 2026 earnings guidance（as_of 2026-08-05）｜affects：valuation、thesis.R、decision_inputs.bear
- `capital_markets_pricing#1`（capital_markets_pricing｜方向 -｜狀態 ok）：Q2 2026 營收 $912M 優於預期 $898M、調整後 EPS $3.26 對 $3.02；財報後股價當日大跌（報導稱約 21%）
  - 來源：Motley Fool, Why HubSpot stock is plummeting today（as_of 2026-08-06）｜affects：valuation、decision_inputs.bear
- `capital_markets_pricing#2`（capital_markets_pricing｜方向 -｜狀態 ok）：分析師目標價 2026-08 共識約 $274–285（Walnut/Yahoo：均值 $273.96、中位 $250、區間 $190–450、33 位；Tickflow 8/1：$285.14）；2月 MarketBeat 均值 $452.70，年內大幅下修；各源口徑與日期不一
  - 來源：Walnut HUBS forecast / Tickflow / MarketBeat（as_of 2026-08-01）｜affects：valuation
- `major_events#1`（major_events｜方向 -｜狀態 ok）：2026-10-01 董事會核准重組計畫，裁減約 7% 員工（8-K Item 2.05）
  - 來源：SEC EDGAR 8-K 2026-10-06 Item 2.05（as_of 2026-10-06）｜affects：thesis.R、decision_inputs.bear
- `major_events#2`（major_events｜方向 -｜狀態 ok）：2026-08-05 Q2 財報下修指引後股價約跌 25%，多家律所（Block & Leviton、Johnson Fistel）宣布調查，但無已提起的集體訴訟、法院無認定
  - 來源：Block & Leviton 案件頁／Johnson Fistel 新聞稿（2026-05-11、2026-08-18）（as_of 2026-08-18）｜affects：thesis.R、decision_inputs.bear
- `lawsuit_class_action#0`（lawsuit_class_action｜方向 -｜狀態 ok）：律所宣布調查（Johnson Fistel 2026-05-11；Block & Leviton 2026-08-18），尚無已提起之證券集體訴訟；10-K 載明曾面臨 CIPA 追蹤器類集體訴訟/求償信
  - 來源：Block & Leviton 案件頁；HubSpot 10-K FY2025 Item 1A（as_of 2026-08-18）｜affects：thesis.R、decision_inputs.bear
- `lawsuit_class_action#1`（lawsuit_class_action｜方向 -｜狀態 ok）：10-K 風險因素：公司曾遭受 CIPA 追蹤器類訴訟
  - 來源：SEC EDGAR 10-K FY2025（as_of 2026-02-11）｜affects：thesis.R

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 10 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/HUBS_20261108/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":720.0,"bear_5y_price":136.8,"p_bull_pct":15,"p_bear_pct":35,"upside_5y_pct":82.1,"ev5y_pct":68.8,"irr_base_pct":12.7,"asym_ratio":3.5,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":13.3,"pe":15.08,"basis":"FY2026E 共識 non-GAAP EPS（FY1）與現價 200.61 美元；終端倍數同樣放在當年度 non-GAAP EPS 上。"},"eps":{"bull":[17.8,21.6,25.9,31.3,36.0],"base":[16.8,19.6,22.4,25.4,28.1],"bear":[15.1,15.0,14.8,14.9,15.2]},"pe":{"bull":20,"base":13,"bear":9},"p":{"bull":15,"base":50,"bear":35},"yield_pct":{"dividend":0,"net_buyback":0},"second_stage":{"bull_cagr_pct":11,"base_cagr_pct":7},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### HUBS_Q2_2026_Earnings_Call_20260805.md
- 2026-08-05｜Kate Bueker (CFO)｜guidance：下半年每季淨新增客戶預期降至 5,000–6,000（同句並預期 ASRPC 固定匯率成長為低至中個位數）（原話："net additions to be approximately 5,000 to 6,000"）
- 2026-08-05｜Kate Bueker (CFO)｜guidance：2026 全年 net new ARR 成長預期低於固定匯率營收成長（原話："expect net new ARR growth to be below constant currency"）
- 2026-08-05｜Kate Bueker (CFO)｜guidance：全年 NRR 預期大致持平（原話："net revenue retention to be roughly flat year-over-year"）
- 2026-08-05｜Kate Bueker (CFO)｜guidance：Q2 逆風預期持續整個下半年（原話："headwinds we saw in Q2 will persist throughout the remainder"）
- 2026-08-05｜Kate Bueker (CFO)｜guidance：Q3 營收財測區間（原話："revenue is expected to be in the range of $924 million"）
- 2026-08-05｜Kate Bueker (CFO)｜guidance：全年營收財測（as reported）區間（原話："revenue is now expected to be in the range of $3.678"）
- 2026-08-05｜Kate Bueker (CFO)｜guidance：全年 non-GAAP 營業利益財測維持（原話："to be in the range of $762 million to $766 million"）
- 2026-08-05｜Kate Bueker (CFO)｜guidance：全年 non-GAAP 稀釋 EPS 財測區間（原話："$13.23 and $13.31"）
- 2026-08-05｜Kate Bueker (CFO)｜guidance：全年自由現金流預期約 7.5 億美元（原話："be about $750 million."）
- 2026-08-05｜Yamini Rangan (CEO)｜margin：CEO 說 2027 營業利益率擴張 2–3 點（原話："2 to 3 points of operating margin expansion in 2027"）
- 2026-08-05｜Kate Bueker (CFO)｜margin：CFO 說今年財測含 2 點 non-GAAP 營業利益率槓桿（原話："2 points of non-GAAP operating margin leverage this year"）
- 2026-08-05｜Kate Bueker (CFO)｜margin：non-GAAP 利益率擴張歸因於人力支出紀律、部分被 AI 成本抵銷（原話："disciplined approach to head count spend, partially offset"）
- 2026-08-05｜Kate Bueker (CFO)｜margin：GAAP 營業利益率擴張部分來自 SBC 占營收下降逾 4 點（原話："4-point reduction in stock-based compensation expense"）
- 2026-08-05｜Kate Bueker (CFO)｜commitment：承諾 SBC 占營收逐年下降（原話："we remain committed to driving stock-based compensation"）
- 2026-08-05｜Kate Bueker (CFO)｜commitment：將於 Analyst Day 提供 SBC 細節（原話："Analyst Day next month"）
- 2026-08-05｜Kate Bueker (CFO)｜capital_allocation：Q2 回購逾 5 億美元（原話："more than $500 million of stock under our current"）
- 2026-08-05｜Kate Bueker (CFO)｜capital_allocation：董事會再授權最多 10 億美元回購（原話："an additional share repurchase program of up to $1 billion"）
- 2026-08-05｜Kate Bueker (CFO)｜capital_allocation：資金用途含有機創新與機會型併購（原話："investing in organic innovation and opportunistic M&A"）
- 2026-08-05｜Kate Bueker (CFO)｜customer：Q2 淨新增客戶低於管理層原預期 9,000–10,000（原話："below our 9,000 to 10,000 expectation"）
- 2026-08-05｜Kate Bueker (CFO)｜customer：淨新增不如預期歸因於轉換率與購買猶豫（原話："conversion rates and increased buyer hesitancy"）
- 2026-08-05｜Kate Bueker (CFO)｜customer：Q2 NRR 為 102%（原話："net revenue retention was 102%"）
- 2026-08-05｜Kate Bueker (CFO)｜customer：續約客戶出現降級壓力（原話："seeing some downgrade pressure as they sort of optimize"）
- 2026-08-05｜Yamini Rangan (CEO)｜customer：大單（ARR >12 萬美元）年增 38%（原話："deals over $120,000 ARR grew 38% year-over-year"）
- 2026-08-05｜Yamini Rangan (CEO)｜risk：CEO 承認 4 月起步慢、季度不如預期（原話："April got off to a slow start"）
- 2026-08-05｜Yamini Rangan (CEO)｜risk：買方決策更慢，需高層與董事會核准（原話："leading to longer sales cycles"）
- 2026-08-05｜Yamini Rangan (CEO)｜risk：CEO 表示假設 Q2 情況延續整個下半年（原話："what we saw in Q2 is what we will see in the second half"）
- 2026-08-05｜Kate Bueker (CFO)｜risk：CFO 表示壓力持續到 7 月（原話："we did see it continue into July"）
- 2026-08-05｜Yamini Rangan (CEO)｜risk：CEO 無法給出預算壓力緩解的確切時點（原話："I can't tell you an exact month or a quarter"）
- 2026-08-05｜Yamini Rangan (CEO)｜product：4 月起推出 agent／AEO 試用，管理層承認延長購買流程（原話："We knew this would create some near-term headwinds"）
- 2026-08-05｜Yamini Rangan (CEO)｜product：引進試用讓客戶先體驗再購買（原話："we introduced trials so customers can turn on agents"）
- 2026-08-05｜Yamini Rangan (CEO)｜product：定價改為結果導向並降低入門價（原話："introduced outcome-based pricing for several of"）
- 2026-08-05｜Yamini Rangan (CEO)｜product：Data agent 啟用客戶逾 1.6 萬（原話："Data agent has over 16,000 customers"）
- 2026-08-05｜Yamini Rangan (CEO)｜product：Breeze Assistant 週活躍使用量年初至今翻倍（原話："weekly active usage has doubled since the start of the year"）
- 2026-08-05｜Yamini Rangan (CEO)｜product：每月 agentic actions 年初至今成長逾 3 倍（原話："has increased more than 3x this year"）
- 2026-08-05｜Yamini Rangan (CEO)｜product：客服 agent 無人工介入解決率 72%（原話："Customer agent now resolved 72% of support"）
- 2026-08-05｜Yamini Rangan (CEO)｜product：降價與改制後 Q2 總 credit 用量仍成長（原話："Total credit consumption grew in Q2 despite the"）
- 2026-08-05｜Yamini Rangan (CEO)｜competition：CEO 稱市場競爭激烈、非贏家全拿（原話："it's never a winner-take-all market"）
- 2026-08-05｜Yamini Rangan (CEO)｜competition：CEO 稱客戶不想要來自 10 家廠商的 10 個 agent（原話："They don't want like 10 agents from 10 different vendors"）

### HUBS_Analyst_Investor_Day_HubSpot_Inc_20260917.md
- 2026-09-17｜CFO Kathryn Bueker｜guidance：2026 non-GAAP營業利益率財測21%（較前一年+2點）（原話："our 2026 guidance for non-GAAP operating margin is 21%"）
- 2026-09-17｜CFO Kathryn Bueker｜guidance：2027 non-GAAP營業利益率財測23%–24%（原話："In 2027, we expect non-GAAP operating margin of 23% to 24%"）
- 2026-09-17｜CFO Kathryn Bueker｜guidance：2026自由現金流預期7.5億美元（原話："we expect to deliver $750 million in free cash flow"）
- 2026-09-17｜CFO Kathryn Bueker｜commitment：2030長期目標：non-GAAP營業利益率30%（原話："We expect to deliver non-GAAP operating margins of 30%"）
- 2026-09-17｜CFO Kathryn Bueker｜commitment：2030目標含GAAP營業利益率20%、SBC占營收10%（原話："stock-based compensation as a percentage of revenue of 10%"）
- 2026-09-17｜CFO Kathryn Bueker｜margin：管理層稱2027年COGS成長將快於營收成長（積極投資agent採用）（原話："COGS growth will outpace revenue growth in 2027"）
- 2026-09-17｜CFO Kathryn Bueker｜margin：毛利壓力以模型路由與OpEx槓桿抵銷（原話："balance gross margin pressure with OpEx leverage"）
- 2026-09-17｜CFO Kathryn Bueker｜margin：毛利率策略：先求品質再優化成本（原話："quality number one, and then optimize cost over time"）
- 2026-09-17｜CFO Kathryn Bueker｜margin：客服端已三年未淨增客服人員（原話："We have not added a net new support rep."）
- 2026-09-17｜CFO Kathryn Bueker｜capital_allocation：過去12個月回購逾10億美元（原話："repurchased more than $1 billion in shares"）
- 2026-09-17｜CFO Kathryn Bueker｜capital_allocation：FCF用途含有機/併購與機會性回購（原話："free cash flow for organic and inorganic opportunities"）
- 2026-09-17｜CEO Yamini Rangan｜commitment：管理層重申不在成長與獲利間二選一（原話："committed to driving both durable growth"）
- 2026-09-17｜CEO Yamini Rangan｜risk：上市場客戶買委會擴大、決策延長（原話："larger buying committees"）
- 2026-09-17｜CEO Yamini Rangan｜risk：管理層稱採購遲疑非單季現象（原話："I don't think this is a 1 quarter kind of an effect"）
- 2026-09-17｜CEO Yamini Rangan｜risk：管理層預期仍有定價敏感度（原話："we will see some level of pricing sensitivity"）
- 2026-09-17｜CFO Kathryn Bueker｜risk：淨營收留存率近期大致持平（原話："net revenue retention goes, which is largely flat"）
- 2026-09-17｜CEO Yamini Rangan｜risk：2027能見度：管理層稱現在說還太早（原話："It's pretty early to say what happens in 2027"）
- 2026-09-17｜CEO Yamini Rangan｜product：Breeze Assistant採用率（CEO稱逾55%，8月）（原話："over 55% of our Pro+ customers are using Breeze Assistant"）
- 2026-09-17｜CFO Kathryn Bueker｜product：Breeze Assistant採用率（CFO稱57%，8月）（原話："57% in August"）
- 2026-09-17｜Jon Dick｜product：HubSpot agents觸及19% Pro+客戶，較年初2倍（原話："19% of Pro+ customers are using HubSpot agents as of August"）
- 2026-09-17｜CFO Kathryn Bueker｜product：自訂agent自7月上線後部署逾3,000個（原話："Over 3,000 custom agents have already been deployed"）
- 2026-09-17｜Duncan Lennox｜product：Aviator採模型中立、依任務選模型（原話："Switzerland of AI approach"）
- 2026-09-17｜Duncan Lennox｜product：每週持續執行數千個evals（原話："thousands of these evals that we've built out"）
- 2026-09-17｜Duncan Lennox｜product：ChatGPT連接器週活躍用戶自6月成長250%（原話："weekly active users on ChatGPT up 250% since June"）
- 2026-09-17｜CEO Yamini Rangan｜customer：連接器用戶約35萬、留存提升12點（原話："nearly 350,000 users on connectors"）
- 2026-09-17｜CEO Yamini Rangan｜customer：使用連接器的客群留存改善12點（原話："12-point improvement in retention"）
- 2026-09-17｜Jon Dick｜customer：夥伴參與上市場交易：勝率與ASP較高（原話："nearly an 8-point higher win rate, 75% higher ASP"）
- 2026-09-17｜Jon Dick｜customer：$12萬以上ARR大單年增38%（原話："deals over $120,000 of ARR, up 38% year-over-year"）
- 2026-09-17｜CFO Kathryn Bueker｜customer：Starter客戶15萬，約占客戶數一半（原話："150,000 starter customers on HubSpot"）
- 2026-09-17｜Jon Dick｜customer：下市場客戶價格敏感且時間受限（原話："They're more price sensitive, they're time constrained"）
- 2026-09-17｜Jon Dick｜customer：Q4加碼促銷下市場（原話："we are ramping up our promotion in Q4"）
- 2026-09-17｜Duncan Lennox｜product：AI Growth Bundle：新客Starter與credits折扣65%（原話："65% off HubSpot Starter and HubSpot credits"）
- 2026-09-17｜CFO Kathryn Bueker｜product：付費席位自2024定價簡化後成長80%（原話："paid seats up 80% since our 2024 pricing simplification"）
- 2026-09-17｜CFO Kathryn Bueker｜product：2024簡化席位定價帶來NRR約2點效益（原話："approximately 2 points of benefit in net revenue retention"）
- 2026-09-17｜CFO Kathryn Bueker｜product：4月降agent價並轉結果導向定價，造成短期逆風（原話："which created a near-term headwind"）
- 2026-09-17｜CFO Kathryn Bueker｜commitment：預期席位與credits將成營收主要驅動（原話："seats and credits will be the primary drivers"）
- 2026-09-17｜CEO Yamini Rangan｜product：非綁定go-to-market人員的項目將改按credits計（原話："should just be based on credits"）
- 2026-09-17｜CFO Kathryn Bueker｜product：Nordics/Benelux試點：初始ASP較低、後續成長較大（原話："lower initial ASPs, but larger growth trajectory"）
- 2026-09-17｜CFO Kathryn Bueker｜product：試點擴大到EMEA新客，下月起（原話："we're moving into EMEA for new customers next month"）
- 2026-09-17｜Jon Dick｜competition：對自行開發CRM：起步易、規模化難（原話："scaling it is exceptionally hard"）
- 2026-09-17｜Jon Dick｜competition：對AI點解決方案：不認為有人要agent sprawl（原話："we don't think anybody will want agents sprawl"）
- 2026-09-17｜Duncan Lennox｜competition：headless策略質疑：分析師問為何對應用軟體公司有利（原話："why is headless good for an application software company?"）
- 2026-09-17｜Jackson Ader (KeyBanc)｜competition：headless策略質疑：分析師問為何對應用軟體公司有利（原話："why is headless good for an application software company?"）

### 問答異常語氣（迴避／改口／保留）
- HUBS_Q2_2026_Earnings_Call_20260805.md｜問：Samad Samana（Jefferies）問除已知的定價、銷售訓練、服務條款變更與回滾外，是否還有其他決策干擾結果、是否需更積極行動｜答法：回答聚焦試用與定價兩項刻意改變及需求環境，未回應服務條款變更與回滾，也未直接回答是否需要更積極動作
- HUBS_Q2_2026_Earnings_Call_20260805.md｜問：Eamon Coughlin（Barclays）問 credit 用量中付費 vs 內含／試用的占比｜答法：改談 reach、depth、quality 等領先指標，未提供付費與內含用量的比例
- HUBS_Q2_2026_Earnings_Call_20260805.md｜問：Gabriela Borges（Goldman）問環境何時好轉、是否為新常態｜答法：未給時間表，僅說假設 Q2 情況延續下半年並提供客戶信心措施
- HUBS_Q2_2026_Earnings_Call_20260805.md｜問：Jackson Ader（KeyBanc）問客戶把預算轉去哪裡、預算壓力何時緩解｜答法：表示沒有水晶球、無法指出確切月份或季度，改談 token maxing 與結果導向定價
- HUBS_Q2_2026_Earnings_Call_20260805.md｜問：Rishi Jaluria（RBC）問是否有 AI 原生新廠商造成市場雜訊與更高審查｜答法：以易用與平台優勢回應，未點名競爭者或說明新廠商是否造成影響
- HUBS_Q2_2026_Earnings_Call_20260805.md｜問：Q&A 中 CEO 引用 agent 客戶數｜答法：口頭說「Customer agent, 18,000 customers that grew by 80%」，與準備稿 customer agent 逾 10,000、data agent 啟用 1.6 萬且季增 80% 不一致，隨即自行更正 data agent 為 1.6 萬
- HUBS_Analyst_Investor_Day_HubSpot_Inc_20260917.md｜問：Piper Sandler問：第一方產品使用前沿模型vs開源模型比重、是否自建模型｜答法：Lennox未給比重，稱持續評估各模型；Bueker稱毛利處於『very early』、品質優先
- HUBS_Analyst_Investor_Day_HubSpot_Inc_20260917.md｜問：Citi問：定價變動與促銷對近期營收/ARR成長形狀的影響｜答法：Bueker/Rangan談定價實驗與降門檻，未給近期營收或ARR影響的數字
- HUBS_Analyst_Investor_Day_HubSpot_Inc_20260917.md｜問：Raymond James問：NRR長期是否上升及合理水準｜答法：Bueker僅稱近期大致持平、長期有順風，未給數字
- HUBS_Analyst_Investor_Day_HubSpot_Inc_20260917.md｜問：Needham問：2027年AI工作流能見度是否改善營運環境｜答法：Rangan稱『pretty early to say』，未對2027給判斷

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 3 | 2 |
| customer_second_source | not_applicable | 0 | 1 |
| customer_concentration_credit | found | 2 | 1 |
| supply_demand_durability | found | 4 | 2 |
| regulatory_antitrust | found | 3 | 3 |
| reg_tariff_export | found | 2 | 1 |
| geo_supply_chain | found | 2 | 2 |
| end_markets | found | 6 | 3 |
| substitute_technology | found | 2 | 1 |
| channel_business_model_shift | found | 4 | 2 |
| capital_markets_pricing | found | 4 | 4 |
| major_events | found | 4 | 5 |

未涵蓋／不適用軸的查詢詞原文（供判相關性）：
- **customer_second_source**（not_applicable）：HubSpot customer concentration largest customer risk 10-K 2025

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260522","verdict":"B 觀望（thesis 偏 observation；估值 5Y 分位 3% 極便宜但 Pure MA ❌ 盲點 2 救援失敗 + 4 家券商 5/8 同步降評；等 Q2 FY26 8/6 Customer Agent ARR 揭露）","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"ARR YoY growth 維持 ≥ 18% — HubSpot 業務動能未被 AI native + Microsoft 蠶食，SMB CRM 換代週期持續","columns":{"2Y 驗證點":"Q2-Q4 FY26 ARR YoY ≥ 18%（vs Q1 +23% 維持高水位）","5Y 驗證點":"FY29 ARR 達 $6-7B（從 FY26 ~$3.7B 起算 17-18% CAGR）","10Y 驗證點":"FY31 sub rev $8-10B（10Y 從 FY25 .13B 起算 13-15% CAGR）","具體數字門檻":"FY26 全年 ARR ≥ +18% YoY；FY27 guide ≥ +15%","信息來源":"HUBS Q1 FY26 8-K + 5/7 earnings call","漂移觸發條件":"連 2 季 ARR YoY &lt; 18% → 削弱（2Y 假設適用 QC-34/35）"}},{"id":"H2","text":"Non-GAAP Operating Margin 持續擴張至 22-24% — operational leverage 兌現，GTM 轉型不傷利潤","columns":{"2Y 驗證點":"FY26 退出 Non-GAAP OpMargin ≥ 19%（vs Q1 18%）","5Y 驗證點":"FY29 Non-GAAP OpMargin ≥ 22%","10Y 驗證點":"FY31 Non-GAAP OpMargin 達 24%+ steady state","具體數字門檻":"FY26 退出率 ≥ 19%；FY27 入場 guide ≥ 20%","信息來源":"HUBS Q1 FY26 8-K + 5/7 earnings call","漂移觸發條件":"連 2 季 Non-GAAP OpMargin YoY 下降 ≥ 100bp → 削弱"}},{"id":"H3","text":"Customer Agent + Prospecting Agent ARR 達 -500M FY27 — AI 戰略兌現，pricing power 護城河加深","columns":{"2Y 驗證點":"Q4 FY26 Customer Agent ARR 揭露 ≥ $50M","5Y 驗證點":"FY29 Customer Agent ARR ≥ -B（佔 sub rev ~15-20%）","10Y 驗證點":"Agent ARR 成為獨立 line item disclosure","具體數字門檻":"Q4 FY26 揭露 ≥ $50M；FY27 揭露 ≥ -500M","信息來源":"5/7 earnings call Yamini 開場語 + Spring Spotlight 2026/3","漂移觸發條件":"連 2 季 Customer Agent active customer 絕對下降 → 反轉"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"Microsoft Copilot for Sales + AI-native CRM (Apollo/Clay/Attio) 從 mid-market 雙夾擊 HubSpot","columns":{"對應假設":"H1","時間尺度":"🔥 中期（4-6 季）","監測指標":"Microsoft Copilot for Sales 公開搶單案例；HubSpot 新客戶 ACV YoY 趨勢；NRR 趨勢","警戒閾值":"Microsoft / Apollo / Clay 任一拿下 ≥ -10M ACV HubSpot 客戶 ≥ 2 件；NRR 連 2 季 &lt; 100%"}},{"id":"R2","text":"GTM 從 contact-tier 轉 seats+credits 執行失敗 — customer churn 加速、新客戶 net add 變慢","columns":{"對應假設":"H1 / H2","時間尺度":"⚡ 短期（1-2 季）","監測指標":"Customer count quarterly net add；ARPU 趨勢；NRR","警戒閾值":"連 2 季 net add &lt; 10,000；NRR 連 2 季 &lt; 100%；Gross retention &lt; 88%"}},{"id":"R3","text":"SMB CRM 變 commodity / Google Workspace + Microsoft 365 內建 CRM 模組取代 standalone tier","columns":{"對應假設":"H3","時間尺度":"🐢 長期（2+ 年慢變數）","監測指標":"Google / Microsoft 是否公告內建 CRM；HubSpot Starter tier customer churn 加速","警戒閾值":"Google / Microsoft 任一公告免費 CRM 模組（≥ 50% 機率才砍倉）；Starter tier 客戶 YoY 連 4 季絕對下降"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🟢","ma":"❌","trap":"🟡","moat_trend":null,"runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":198.37,"archetype":null,"cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"HUBS","date":"2026-11-08","schema":"v15.0","contract":"v19","company_name":"HubSpot, Inc."},"oneliner":"客戶金額留存還穩，但淨留存、淨新增客戶與淨新增 ARR 一起轉弱，公司同時在降價；15 倍 non-GAAP 本益比扣掉股權報酬後並不便宜，等 2027 年 2 月的年度指引與 EMEA 試點結果再說。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/HUBS_20261108/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/HUBS_20261108/scenario.json","answers":{"q1_business":{"verdict":"賺中小企業行銷、銷售與客服團隊的訂閱費，錢卡在 CRM 資料加多產品整合這一節點；新客與加購兩個入口正在變窄。","reasoning":"最新一季營收 9.476 億美元，年增 17%，其中訂閱年增 18%，專業服務及其他 1,730 萬美元、年減 3%。訂閱占營收 98%，多數合約一年以內。non-GAAP 營益率 22.6%，GAAP 僅 7.6%，訂閱毛利率 85.4%。客戶 311,704 家、年增 12%，新增主要來自低價 Starter，單客訂閱營收 12,038 美元、年增 4%。Q4 指引中位數 9.46 億美元，低於 Q3 實績，年增率降到 12%，管理層明講逆風延續到 2027 年。單點依賴有兩個：Solutions Partners 及其轉介客戶占 2025 年營收約 49%，既是護城河也是集中度風險；主要基礎設施放在 AWS us-east-1，2025 年 10 月已出過事。可能看錯：Q3 實績高於指引上限約 2,300 萬美元，若 Q4 也如此，年增率約 15%，12% 的退出成長率就言過其實。","fact_refs":["f_kpi0_gaap","f_kpi1_non_gaap","f_kpi2_non_gaap","f_kpi3_gaap","f_kpi4_gaap","f_kpi7","f_kpi8_non_gaap","f_kpi10_q4_2026","f_kpi11_fy2026"],"verdict_values":{"revenue_quality":"訂閱占 98%，多數一年期以內，客戶金額留存在高 80%，可見度中等；一年期合約讓降級在續約時很快反映。","unit_econ_note":"單客訂閱營收 12,038 美元、年增 4%。Starter 約 15 萬家，約占客戶數一半。試點區 ASP 較低但 Pro+ 客戶量較高。付費與內含 credit 的比例，管理層在 2026-08-05 被問到時沒有回答。","archetype":{"primary":"品質複利成長","secondary":"轉機/特殊情境","confidence":"低","fingerprint":"營收成長仍有 17%、FCF 利潤率約 19%，但 GAAP 營益率僅 5.45%，成長正往 12% 換檔，定價與產品同時轉型。"},"industry":{"clock_phase":"IV","sd_verdict_source":"結構性持久為主：AI 改變買方找軟體的方式，入站獲客受壓屬結構性；預算排擠偏週期，但管理層 2026-08-05 與 2026-09-17 都說不出緩解時點。判 IV 的依據是淨新增 ARR 年減與客戶更在意價格，不是股價。","bargaining":{"up":"上游是模型與雲端。模型中立降低單一供應商風險，但 CFO 說 2027 年 COGS 成長快於營收。","down":"客戶分散，沒有單一大客戶；下市場對價格敏感，上市場決策層級提高，議價力往客戶移。","geo":"國際營收占 49%，地緣議價證據事實表未涵蓋。"},"profit_pool_dir":"有往模型層流出的跡象，毛利率 85.03%→83.76%→83.02%；五年利潤池占比事實表未涵蓋。","tam_table":{"expanded":false,"reason":"事實表沒有 CRM 與 SMB 行銷軟體的份額和滲透率，只有 Gartner 二手的企業應用軟體總額（2026 年 4,963 億美元、2030 年 8,126 億美元），無法拆成 TAM、SAM、滲透率與利潤池占比。"}}}},"q2_moat":{"verdict":"護城河收窄（↓）：客戶黏著還在，定價力與新客入口退步。","reasoning":"機制是 CRM 資料加多產品整合形成的轉換成本，再加入站獲客與夥伴通路。執行力穩定（7 分）：Q3 non-GAAP 營益率年增 3 點，20% 的 Pro+ 客戶使用 agent，但 2026 年留存與 ARR 看法兩度下修。定價力縮減（5 分）：淨留存由 Q2 的 102% 降到 101%，全年看法由大致持平改成降約 2 點；加購、聯絡人級距與版本升級已抵銷席位升級；agent 由每對話 1 美元改成每解決 0.5 美元，新客 Starter 與 credit 折扣 65%，試點區 ASP 較低。毛利率 85.03%→83.76%→83.02%。AI 新進者的威脅另記在威脅等級，不在趨勢重複扣分。同業 ROIC 差距取不到，改用留存與 ASP 當比較軸；FCF 利潤率 18.89%，低於 CRM 的 34.49% 與 NOW 的 30.78%。AI 曝險看兩點：淨增量的分界點是 2027 年底，屆時付費 credit 收入要大於定價改革讓出的收入；附著點的分界點是 2029 年，看工作是否仍寫回 HubSpot 的資料。反例：客戶金額留存穩在高 80%，使用連接器的客戶留存高 13 點，但這群客戶本來就較活躍，有自選偏誤；若 2027 年留存與加購止跌，趨勢應改回穩定。","fact_refs":["f_peer_hubs_gross_margin_pct","f_peer_hubs_operating_margin_pct","f_peer_hubs_fcf_margin_pct","f_peer_crm_operating_margin_pct","f_peer_crm_fcf_margin_pct","f_peer_now_gross_margin_pct","f_peer_now_fcf_margin_pct","f_peer_team_gross_margin_pct","f_peer_team_operating_margin_pct","f_peer_mndy_gross_margin_pct","f_peer_mndy_fcf_margin_pct","f_kpi8_non_gaap"],"verdict_values":{"moat":{"mechanism":"CRM 資料與多產品整合的轉換成本（客戶金額留存高 80%），搭配入站獲客與占營收約 49% 的夥伴通路。","execution":7,"pricing":5,"grade":"C","trend":"↓","trend_evidence":"淨留存 102%→101%，全年改為降約 2 點；淨新增客戶 7,000→5,300→低於 5,000；12 萬美元以上大單年增 38%→19%；2026 年淨新增 ARR 年減。","competitor_notes":[{"name":"CRM","strategy_note":"營益率 21.52%、FCF 利潤率 34.49%，獲利能力高於 HubSpot，靠收購補 agent，是上市場最直接的對手。"},{"name":"NOW","strategy_note":"毛利率 73.08% 低於 HubSpot，FCF 利潤率 30.78%，與 SMB 客群的重疊程度事實表未涵蓋。"},{"name":"TEAM","strategy_note":"毛利率 84.83% 相近，營益率僅 0.16%，研發密度 49.74%，GAAP 獲利接近零。"},{"name":"MNDY","strategy_note":"毛利率 88.74%、FCF 利潤率 21.56%，與 HubSpot 的客戶重疊與份額事實表未涵蓋。"},{"name":"AI 原生 CRM 新創","strategy_note":"10-K 已列為競爭者；份額與資本量級事實表未涵蓋。"}],"peer_na_reason":"事實表只有同業利潤率，沒有投入資本，無法計算 ROIC 差距。","threats":[{"level":"🔴","text":"通用 LLM、AI 原生 CRM 與 vibe coding 自建：10-K FY2025 新增列入競爭來源，部分新創已不用 HubSpot。目前沒有量化搶單或留存下滑的證據，屬生態攻擊，還不到架構替代。","p":35,"evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1","competitive_share_entrants#2","substitute_technology#0"]},{"level":"🟡","text":"席位轉用量或成果計價：Gartner 轉述 2030 年前逾 40% 企業 SaaS 支出脫離純席位，Ramp 資料則顯示目前仍以席位為主。公司正主動遷移，風險在收入重訂價。","p":40,"evidence_refs":["supply_demand_durability#2","channel_business_model_shift#1"]}],"roic_durability":{"quadrant":"無法判定：GAAP 營益率 5.45% 屬低利益率，投入資本周轉率事實表未涵蓋。","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者是行銷與銷售團隊，決策者在上市場已升到 CEO、CTO 與董事會，付款者在下市場變得更省。需要 CRM 的問題還在，高 80% 的客戶金額留存是證據；加購和版本升級可以延後，Q3 已轉成拖累。"},{"item":"決策層級","level":"🟡","text":"最小決策單位是每年續約時的席位與版本。Starter 約 15 萬家，約占客戶數一半，轉換成本低；Pro+ 較黏，62% 新 Pro+ 客戶一開始就買多個產品。多數合約一年以內，降級在續約時就會反映。"},{"item":"價值鏈分配","level":"🟡","text":"模型與雲端拿走的份額在增加：CFO 說 2027 年 COGS 成長快於營收，毛利率兩年降 2 點。連接器把介面交給 ChatGPT 與 Claude，目前工作仍寫回 HubSpot，Q3 建立 2,200 萬筆物件。毛利率若低於 80% 就轉紅。"},{"item":"社會容忍度","level":"🟢","text":"企業軟體沒有社會定價上限問題，定價限制來自客戶預算。州級 AI 法規與隱私執法屬合規成本，事實表未見針對 HubSpot 的調查。"}],"roiic":"事實表未涵蓋投入資本，無法計算","reinvest_rate":"事實表未涵蓋折舊與營運資金變動，無法計算","endo_ceiling":null,"formula_note":"當期 ROIC、增量 ROIC 與再投資率都缺輸入數字，不以估算代替。"}}}},"q3_growth":{"verdict":"Y5 之後跑道中等（🟡）：滲透率資料缺，第二曲線 credit 還沒證明能賺錢。","reasoning":"成長以量為主：客戶年增 12%，單客訂閱營收年增 4%，併購可忽略。共識 EPS 由 FY2025A 約 9.71 美元到 FY2028E 20.21 美元，三年 CAGR 27.7%。FY2025A 到 FY2027E 的 EPS CAGR 31.6%，同期營收 CAGR 14.5%，差 17 點，來自營益率上升與股數下降，可以歸因，但不是營收帶來的。跑道無法用滲透率算，事實表只有企業應用軟體總額。第二曲線是 credit：月用量年初至今增近 2.5 倍，但付費與內含比例沒有揭露，2026 年淨新增 ARR 還在年減，不能算已證實。也沒有證據顯示市場已飽和，所以判中等。可能看錯：EMEA 試點的 Pro+ 客戶量和 credit 用量若能在全球複製，跑道應升一級。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_kpi7","f_kpi10_q4_2026","f_kpi11_fy2026"],"verdict_values":{"growth":{"driver_mix":"量為主（客戶 +12%），價為輔（單客訂閱營收 +4%），併購可忽略；EPS 另受營益率擴張與回購推升。","runway_years":"事實表未涵蓋滲透率，無法換算","runway_post_y5":"🟡","endo_ceiling_basis":"事實表未涵蓋投入資本與再投資率，內生上界無法推導，情境以保守方式視為已超過。共識 EPS 與營收的差距可歸因於營益率擴張和回購。","segments":[{"item":"訂閱營收 Q3 年增","value":"18%"},{"item":"專業服務及其他 Q3","value":"1,730 萬美元，年減 3%"},{"item":"國內營收 Q3 年增","value":"16%"},{"item":"國際營收 Q3 年增","value":"18%，占營收 49%"}],"decay_signals":[{"item":"毛利率連兩季年減","lit":true,"evidence":"年度與 TTM 毛利率 85.03%→83.76%→83.02%，CFO 預告 2027 年 COGS 成長快於營收；單季序列事實表未涵蓋，以年度趨勢判定。"},{"item":"核心市占近 12 個月縮減","lit":false,"evidence":"事實表未涵蓋份額資料。"},{"item":"主力產品提價後銷量下滑","lit":false,"evidence":"公司是在降價，不是提價。"},{"item":"EPS CAGR 高於營收 CAGR 逾 5 點","lit":true,"evidence":"2025 至 2027 年相差 17 點。"},{"item":"FCF／淨利連兩年低於 0.75","lit":false,"evidence":"FCF 遠高於 GAAP 淨利，其中部分來自 SBC。"},{"item":"SBC 占營收逾 5% 且逐年上升","lit":false,"evidence":"Q3 為 13.4%，但占比年減逾 3 點，條件不成立。"},{"item":"TAM 萎縮或被替代技術壓縮","lit":false,"evidence":"Gartner 二手資料估計代理式 AI 到 2030 年侵蝕傳統應用軟體 1,160 億美元，但企業應用軟體總額仍成長，列入觀察。"},{"item":"產業估值倍數近三年系統性下移","lit":false,"evidence":"同業倍數事實表未涵蓋，只能看到本公司 P/S 為四個年度端點最低。"},{"item":"維持性資本支出占 FCF 逾 60%","lit":false,"evidence":"資本支出占營收 5–6%，約 2 億美元，不到 FCF 7.2 億美元的 30%。"},{"item":"停止投資新產能且收入三年內下滑","lit":false,"evidence":"不適用，收入仍在成長。"}],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"資本配置中等：今年回購大於 FCF，股數下降，但往後的授權額度大約只夠抵銷股權報酬。","reasoning":"2026 年累計回購近 10 億美元，高於全年 FCF 指引約 7.2 億美元，現金及有價證券為 13 億美元。FCF 指引由 7.5 億美元下修到 7.2 億美元，管理層沒有說明原因，同期有 6,000–7,000 萬美元遣散費。Q3 SBC 1.271 億美元，占營收 13.4%，年減逾 3 點；年化約 5.08 億美元，約占 FCF 七成，扣掉後 FCF 約 2.1 億美元。稀釋股數由全年假設 5,040 萬降到 Q4 假設 4,890 萬。2026 年 8 月新授權是 24 個月 10 億美元，每年約 5 億美元，差不多只抵銷 SBC。FY2025 FCF／GAAP 淨利 12.6 倍沒有參考價值，因為淨利太小。三年現金去向、債務到期與回購均價事實表未涵蓋。2030 年 SBC 占營收 10% 的目標是檢驗點。","fact_refs":["f_kpi5_non_gaap_fcf","f_kpi6_sbc","f_kpi0_gaap","f_net_debt_m","f_shares_diluted_m"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":false,"passed":null,"input":"2026-04 收購 Futurepedia 僅 1,910 萬美元，沒有回報資料，其他收購事實表未涵蓋。"},{"name":"buyback_yield","applicable":true,"passed":null,"input":"2026 年累計回購近 10 億美元；回購均價與 10 年期公債殖利率事實表未涵蓋，無法計算買入收益率。"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"全年稀釋股數假設 5,040 萬，Q4 假設 4,890 萬，股數淨減。前提是回購大於 SBC；只看 SBC，年化約 5.08 億美元，約市值 5.2%。"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購，事實表僅見一筆 1,910 萬美元收購；三年現金去向事實表未涵蓋。"}}}},"q5_valuation":{"verdict":"現價要求 FY2031 non-GAAP EPS 約 27 美元（屆時 13 倍）才有年化 12%；算得到，但前提是淨留存先止跌，這點目前信不過。","reasoning":"現價 200.61 美元等於 FY1 共識 15.08 倍、FY2 11.93 倍、EV／FCF 約 12.1 倍（EV 87.24 億美元、FCF 約 7.2 億美元）。同一家公司的 GAAP trailing P/E 是 48.46 倍，FCF 扣掉年化 SBC 後收益率約 2.2%。便宜與否取決於 SBC 算不算成本，這正是爭點，所以不把便宜當進場理由。Base 用 13 倍，低於現值，報酬全部來自 EPS 成長。五年分位事實表沒有，年度端點的 0% 只有 2 到 4 個點，不算五年分位。EPS 快照 13.3 美元低於公司新指引 13.59–13.61 美元，近兩份快照修正幅度為 0，Q3 的利空應該還沒進模型。護城河收窄時 Bear 錨不穩定，每次下修地板就下移，上下檔比只供參考，不作進場依據。可能看錯：Q4 指引若如過去一樣保守，年增率約 15%，現價就確實偏低。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_pe_current","f_pe_percentile","f_ps_current","f_ps_percentile","f_ev_s_current","f_ev_s_percentile","f_ev_s_fwd","f_ev_m","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_fy1_pct","f_consensus_rev_3m_fy1_pct","f_kpi5_non_gaap_fcf","f_kpi6_sbc","f_week26_return_pct","f_rsi14"],"verdict_values":{"valuation":{"basis":"non-GAAP Fwd P/E 為主，同時對照 GAAP trailing P/E 與 FCF 扣 SBC 後的收益率。","tier":"SMB 應用軟體，成長換檔中","peers":{"expanded":false,"reason":"事實表只有同業利潤率，沒有同業倍數，無法做同級比較。"},"fwd_pe":15.08,"peg":0.54,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"PEG 0.54（15.08 倍除以 FY2025A 到 FY2028E 的 EPS CAGR 27.7%）與 15.08 倍看來便宜，但分母沒有扣 SBC，GAAP trailing P/E 為 48.46 倍。分母正是爭點，便宜論證不成立，結論只給中性。五年分位事實表未提供。","upside_short_pct":9,"upside_mid_pct":45,"denominator_disputed":true,"denominator_note":"non-GAAP EPS 排除占營收 13.4% 的 SBC。Q3 non-GAAP EPS 3.81 美元，GAAP 1.67 美元；FCF 扣年化 SBC 後對市值收益率約 2.2%，遠低於 FY1 本益比隱含的 6.6%。"}}},"q6_how_wrong":{"verdict":"最容易看錯的是降速的性質：是轉型期還是護城河收窄，要到 2027 年 2 月才分得清。","reasoning":"衰退信號亮兩個，毛利率下滑與 EPS 成長高於營收成長，對應中度陷阱風險。淨留存在降，但客戶金額留存仍穩，兩條留存線沒有同時下滑，所以沒有升到高風險；客戶金額留存轉弱就要升級。成長熄火測試以 FY2029 EPS 計：成長降到 15%，22.4 美元乘 15 倍得 336 美元；降到 10%，乘 13 倍得 291 美元；降到 5%，約 15 美元乘 9 倍得 135 美元，跌 33%。三項過兩項。付費 credit 比例管理層至今沒回答，是最大的資訊缺口。歷史最大回撤事實表未涵蓋，只知道現價比 250 週線 445.12 美元低 55%。","fact_refs":["f_ma_w250","f_ma_state","f_ma_w52","f_kpi6_sbc","f_consensus_rev_fy2_pct"],"verdict_values":{"trap":{"verdict":"🟡","label":"成長換檔中的中度陷阱風險"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":13.3,"pe":15.08,"basis":"FY2026E 共識 non-GAAP EPS（FY1）與現價 200.61 美元；終端倍數同樣放在當年度 non-GAAP EPS 上。"},"eps":{"bull":[17.8,21.6,25.9,31.3,36.0],"base":[16.8,19.6,22.4,25.4,28.1],"bear":[15.1,15.0,14.8,14.9,15.2]},"pe":{"bull":20,"base":13,"bear":9},"p":{"bull":15,"base":50,"bear":35},"yield_pct":{"dividend":0,"net_buyback":0},"second_stage":{"bull_cagr_pct":11,"base_cagr_pct":7},"max_dd":{"lo":-50,"hi":-35,"basis":"2026-08-05 財報後單日跌約 21–25%，可作單次事件跌幅；Bear 終點約 137 美元（−32%）；若先跌到 Bear 倍數再疊一次指引下修，約 100–130 美元，即 −50% 到 −35%。淨現金 10.7 億美元與回購授權能撐下檔，但擋不住倍數壓縮。歷史最大回撤事實表未涵蓋。","trigger_time":null},"basis":{"bull":"credit 變成可見收入，2027 下半年淨留存回到 104% 以上，營收成長維持 10–12%，2031 年 non-GAAP 營益率 30%，倍數回到 20 倍。","base":"營收成長 10%、9%、8.5%、8%、7.5%，營益率由 23.5% 到 27%，低於公司 2030 年 30% 目標；股數小幅下降，回購效果已含在 EPS。倍數 13 倍低於現值，因成長更慢且 SBC 仍高；同業倍數事實表未涵蓋，只能對照自身現值 15.08 倍。","bear":"淨留存跌破 100%，客戶金額留存下滑，營收成長降到低個位數，為守客戶增加投入，營益率停在約 20%。9 倍取自成長熄火到 5% 的情境。Bear 機率 35% 的依據：相關指標已連兩季惡化，內生上界無法驗證，管理層也說逆風延續到 2027 年。"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"入站獲客受壓，淨留存連降，淨新增 ARR 年減；10-K 新增 AI 原生 CRM 與通用 LLM 為競爭來源，部分新創已不用 HubSpot。","assumption":"基準情境假設客戶金額留存維持高 80%，流失只發生在邊際客戶。","consequence":"5 年後虧 50% 最可能的路徑：Starter 與 Pro 客戶改用 LLM 加輕量資料庫，淨留存掉到 95% 附近，營收成長低個位數，倍數壓到 7–9 倍。","ruling":"採納。這條與唯一致命數字（淨留存跌破 100%）部分重疊，門檻已寫進觸發條件。目前沒有份額流失的量化證據，所以 Bear 機率放 35%，沒有更高。","watch":"客戶金額留存是否仍稱高 80%、Starter 客戶數、淨新增客戶。","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1","competitive_share_entrants#2","substitute_technology#0","supply_demand_durability#1"],"fact_refs":["f_kpi7"]},{"view":"論點成功但股東經濟變差","evidence":"CFO 在 2026-09-17 說 2027 年 COGS 成長快於營收；試點 ASP 較低；毛利率 85.03%→83.76%→83.02%；2026 年 10 月裁員約 7%，省下的錢有相當部分再投入留才與 AI。","assumption":"credit 定價高於模型成本，且付費用量夠大。付費與內含比例管理層在 2026-08-05 沒回答。","consequence":"agent 用得很好，但毛利率掉到 78% 左右。FY2031 營收 55.7 億美元下，5 點毛利率約少 2.8 億美元營業利益、每股約 5 美元，約占基準 EPS 18%。","ruling":"部分採納。管理層重申 2027 年營益率 23–24%，短期可靠人力成本抵銷，長期不能一直裁員，所以基準情境只給到 27%。","watch":"毛利率、SBC 占營收、付費 credit 是否揭露。","evidence_refs":["major_events#1","channel_business_model_shift#1"],"fact_refs":["f_peer_hubs_gross_margin_pct","f_kpi6_sbc"]},{"view":"價格已反映太多","evidence":"15.08 倍 non-GAAP 看似已反映壞消息，但 GAAP trailing P/E 48.46 倍，FCF 扣年化 SBC 後收益率約 2.2%。賣方 8 月目標價均值 273.96 美元定於 Q3 之前，EPS 快照近兩份沒有修正。","assumption":"市場繼續用 non-GAAP 倍數看這家公司，且 FY2027 EPS 共識 16.82 美元不再下修。","consequence":"分母改成扣 SBC 後，市場給的並不是低價；共識下修時地板跟著往下。","ruling":"採納。現在就買的最強論證：EV／FCF 約 12 倍、淨現金 10.7 億美元，2027 年營益率已被重申，試點有效，逆風有一部分是公司自己選的，留存一旦止跌，倍數有機會回到 20 倍。本次不採納這個論證，因為決勝數據 2027 年 2 月才到，Q3 利空還沒進 EPS 模型，先等第一個確認數據點。","watch":"賣方 EPS 與目標價更新、2027 年 2 月指引。","evidence_refs":["capital_markets_pricing#0","capital_markets_pricing#1","capital_markets_pricing#2"],"fact_refs":["f_fwd_pe_latest","f_pe_current","f_consensus_rev_fy1_pct","f_kpi6_sbc"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ❌ → 本次 ❌","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=❌","side_b":"本次 ma=❌","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；與前份相同。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 198.37 → 本次 200.61（+1.1%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=198.37","side_b":"本次 price_at_dd=200.61","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 198.37 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 198.37 美元：五年期望值 前份未列，基準年化 前份未列，前份未列不對稱比","side_b":"本次情境、股價仍用 198.37 美元：Bull 價 720、Bear 價 136.8，五年期望值 +70.7%，基準年化 13.0%，不對稱比 3.63","ruling":"先換情境、股價不動：五年期望值與基準年化前份未列，無法比較。前份未列不對稱比，本次為 3.63。Bull、Bear 價位與股價無關，只受情境影響。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 198.37 美元：五年期望值 +70.7%，基準年化 13.0%，不對稱比 3.63","side_b":"本次情境、股價 200.61 美元：五年期望值 +68.8%，基準年化 12.7%，不對稱比 3.49","ruling":"再換股價、情境不動：起點價上漲 1.1%，五年期望值少 1.9 個百分點，基準年化少 0.3 個百分點，不對稱比由 3.63 降到 3.49。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"一致判斷：短期獲利防線","cause":null,"prior_field":null,"side_a":"2026-08-05 CEO 說 2027 年營益率擴張 2–3 點，2026-09-17 CFO 給 23–24%，2026-11-04 CFO 再次確認。","side_b":"Q3 營益率 22.6%，Q4 指引約 23%，裁員約 7%。","ruling":"兩邊一致，屬可調和。2027 年目標接近 Q4 退出水準，達成難度不高；短期 EPS 下修風險主要來自營收。","evidence_level":"高，公司財報與電話會。","settle_metric":"FY2027 non-GAAP 營益率。","if_then":[],"evidence_refs":[]},{"axis":"不可調和：AI 是增量還是替代","cause":"新證據","prior_field":null,"side_a":"管理層：月 credit 用量年初至今增近 2.5 倍，連接器客戶留存高 13 點、席位升級 3 倍，headless 對 HubSpot 是加分。","side_b":"收入指標相反：淨留存降到 101%，2026 年淨新增 ARR 年減，入站獲客受壓，加購轉為拖累。","ruling":"不可裁決至 2027 年 2 月，暫採收入指標這一邊。依據是使用量可能來自內含額度，付費比例沒有揭露，連接器留存又有自選偏誤。硬數據點是淨留存、淨新增 ARR 與付費 credit 收入。","evidence_level":"中，使用量由管理層自述，收入指標為財報揭露。","settle_metric":"淨留存連兩季 ≥102%，單季淨新增 ARR 年增轉正，付費 credit 收入揭露。","if_then":["若連兩季淨留存 ≥102%、客戶金額留存仍為高 80%、淨新增 ARR 年增轉正，則重跑完整判斷，通過後首筆不超過 2%。","若淨留存單季跌破 100%，則不建倉，已持有者清倉。","若股價先站上 52 週線 256.6 美元而留存未改善，則不追。","若股價續跌但重啟條件未成立，則不分批反買，維持不建倉。"],"evidence_refs":["supply_demand_durability#1","end_markets#2"]},{"axis":"管理層口徑七週內改變","cause":"新證據","prior_field":null,"side_a":"2026-08-05 CFO：全年淨留存大致持平，淨新增 ARR 成長低於固定匯率營收成長，FCF 約 7.5 億美元；2026-09-17 CFO 仍說淨留存大致持平，FCF 7.5 億美元，大單年增 38%。","side_b":"2026-11-04 CFO：全年淨留存降約 2 點，淨新增 ARR 年減，FCF 約 7.2 億美元；CEO 說大單年增 19%。","ruling":"採信新數字，投資人日的說法在七週內失效，管理層對 2027 年的樂觀描述要打折。Q4 指引仍可能偏保守，兩者不互斥。","evidence_level":"高，電話會原話。","settle_metric":"2027 年 2 月實績與指引。","if_then":["若 Q4 營收低於 9.60 億美元，則視為指引不再保守，維持不建倉。"],"evidence_refs":["capital_markets_pricing#0"]},{"axis":"管理層歸因：刻意取捨的短期代價","cause":"新證據","prior_field":null,"side_a":"管理層把試用與定價改革列為刻意取捨，短期拖累、長期有利，並以 2024 年席位降價後留存改善為例。","side_b":"壓力自 Q2 起連兩季加重，2026-08-05 CEO 說不出緩解時點，2026-09-17 CEO 也說 2027 年還太早判斷；試用延長採購週期只能解釋一部分。","ruling":"不採信也不否定，標記為未證、監測。預登記：到 2027 年 Q2 財報（約 2027-08），淨留存仍 ≤101% 且單季淨新增客戶 ≤5,000，這項歸因視為不成立。","evidence_level":"中。","settle_metric":"2027-08 前的淨留存與淨新增客戶。","if_then":["若到 2027-08 兩項都未改善，則判定歸因不成立，維持不建倉，已持有者減碼一半。"],"evidence_refs":["supply_demand_durability#1"]},{"axis":"賣方共識與本次判斷","cause":"新證據","prior_field":null,"side_a":"8 月目標價均值 273.96 美元、中位 250 美元、區間 190–450 美元，最高最低比 2.37 倍；均值高於現價 37%，方向上反對本次結論。","side_b":"本次不進場，因 Q3 後的逆風尚未反映在 EPS 快照，快照 13.3 美元甚至低於公司新指引。","ruling":"分歧在框架。目標價隱含倍數回到約 20 倍，本次認為淨留存止跌前沒有理由回到 20 倍。不主張市場現在的低倍數是錯的。","evidence_level":"中，目標價資料停在 2026 年 8 月。","settle_metric":"Q3 後賣方 EPS 與目標價更新。","if_then":["若 FY2027 EPS 共識更新後仍 ≥16.8 美元且 2 月營收指引 ≥10%，則保留重啟機會。","若共識下修超過 5%，則同步下移 Bear 錨，維持不追。"],"evidence_refs":["capital_markets_pricing#2"]},{"axis":"產業態勢三軸","cause":"新證據","prior_field":null,"side_a":"競爭：10-K 新增 AI 原生 CRM 與通用 LLM，目前缺量化搶單資料。結構轉好：Gartner 估 2026 年全球軟體支出年增 15.1%，Ramp 資料顯示席位侵蝕慢於言論。","side_b":"其他結構變數：商業模式由席位轉席位加 credit，買方發現軟體的通路改由 AI 中介。","ruling":"其他結構變動中，指商業模式與通路兩項；競爭惡化尚無量化證據。依據是 Q3 電話會對入站需求與定價的說明。","evidence_level":"中。","settle_metric":"付費 credit 收入與入站以外的獲客占比。","if_then":[],"evidence_refs":["competitive_share_entrants#0","supply_demand_durability#2"]},{"axis":"基本面判斷變動","cause":"新證據","prior_field":["signal","trap","moat_trend","runway_post_y5"],"side_a":"2026-05-22：訊號 B、觀望、陷阱中度，護城河方向與跑道未評。","side_b":"2026-11-08：訊號 C，護城河收窄，跑道中等，陷阱中度；股價幾乎沒動（198.37→200.61 美元）。","ruling":"變動來自兩次財報，不是股價。前份假設 ARR 年增 ≥18% 已被 Q3 billings 年增 15% 與 Q4 營收年增 12% 否定，前份的淨新增門檻也已觸發。","evidence_level":"高。","settle_metric":"2027 年 2 月財報。","if_then":[],"evidence_refs":["supply_demand_durability#1","end_markets#2"]},{"axis":"估值方法與情境欄位","cause":"方法變動","prior_field":["val","archetype","cycle_position","p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份以五年估值分位 3% 判偏便宜，公司類型、循環位置、情境機率與回撤範圍未填。","side_b":"本次把 SBC 納入分母比較，便宜論證不成立，結論改中性；公司類型定為品質複利成長（低信心），循環位置不適用，情境機率與回撤範圍首次填入。","ruling":"屬方法變動。股價與前份幾乎相同，估值結論下修不是因為變貴，而是分母的爭點被納入。","evidence_level":"中。","settle_metric":"SBC 占營收與 GAAP 營益率。","if_then":[],"evidence_refs":[]},{"axis":"重啟與加碼門檻","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"前份未設重啟門檻，只寫等 2026-08-06 Customer Agent ARR 揭露。","side_b":"三項同時成立才重跑判斷：淨留存連兩季 ≥102%，客戶金額留存仍為高 80%，單季淨新增 ARR 年增轉正。","ruling":"舊等待事件沒有帶來揭露，所以改用公司確實會揭露的留存指標；重啟後也只是重跑判斷，不會直接加碼。","evidence_level":"高。","settle_metric":"季度留存指標。","if_then":[],"evidence_refs":[]},{"axis":"減碼與清倉門檻","cause":"新證據","prior_field":["kill_metrics"],"side_a":"連 2 季 net add < 10,000；NRR 連 2 季 < 100%；Gross retention < 88%","side_b":"單季淨新增客戶連 2 季 <4,000；淨留存單季 <100%；客戶金額留存低於 85% 或管理層不再稱高 80%。","ruling":"舊的淨新增門檻已觸發（Q2 7,000、Q3 5,300），這個觸發不撤銷，是本次不進場的理由之一。新門檻用於下一階段的減碼與清倉判斷。淨留存改為單季觸發，比舊門檻更嚴。客戶金額留存公司只揭露區間，88% 無法核對，所以改用可觀察的說法。","evidence_level":"高。","settle_metric":"季度財報電話會。","if_then":[],"evidence_refs":["supply_demand_durability#1"]},{"axis":"Single Thing 唯一致命點","cause":"新證據","prior_field":["single_thing"],"side_a":"前份未設唯一致命點。","side_b":"淨留存單季跌破 100%。","ruling":"本次依敏感度選定：每年少 1 點淨留存，FY2031 EPS 約少 4 美元；同年 1 點營益率約 1 美元。","evidence_level":"中，敏感度為本次推算。","settle_metric":"季度淨留存。","if_then":[],"evidence_refs":["supply_demand_durability#1"]},{"axis":"前份假設門檻更換","cause":"新證據","prior_field":["H1","H3"],"side_a":"H1：FY26 全年 ARR ≥ +18% YoY；FY27 guide ≥ +15%。H3：Q4 FY26 Customer Agent ARR 揭露 ≥ $50M。","side_b":"H1：FY2027 淨留存 ≥102%，客戶金額留存維持高 80%。H3：付費 credit 收入占訂閱營收 ≥3%，單客訂閱營收固定匯率年增 ≥3%。","ruling":"舊 H1 已被實績否定。舊 H3 的 ARR 公司沒有揭露，無法驗證，改用公司的新定價架構與可揭露指標。","evidence_level":"高。","settle_metric":"2027 年季度揭露。","if_then":[],"evidence_refs":["end_markets#2"]}],"triggers":[{"n":1,"text":"Q4 財報與 2027 年首次年度指引","type":"複審日期","maps_to":"H1","metric":"FY2027 營收指引中位數年增、營益率指引、淨留存","threshold":"營收 ≥10%，營益率 ≥23%，淨留存 ≥101%","action":"三項達標才開始累計重啟條件，任一未達則不追","source_freq":"公司財報，季度","date":"2027-02","evidence_refs":["end_markets#2","capital_markets_pricing#0"]},{"n":2,"text":"淨留存跌破 100%","type":"Single Thing","maps_to":"Single Thing","metric":"淨留存","threshold":"單季 <100%","action":"不建倉，已持有者清倉","source_freq":"財報電話會，季度","date":null,"evidence_refs":["supply_demand_durability#1"]},{"n":3,"text":"重啟條件三項同時成立","type":"估值rearm","maps_to":"H1","metric":"淨留存、客戶金額留存、單季淨新增 ARR","threshold":"連兩季淨留存 ≥102%，客戶金額留存仍為高 80%，淨新增 ARR 年增轉正","action":"重跑完整判斷，不直接建倉，通過後首筆不超過 2%","source_freq":"財報電話會，季度","date":null,"evidence_refs":[]},{"n":4,"text":"客戶金額留存轉弱","type":"清倉","maps_to":"R3","metric":"客戶金額留存","threshold":"管理層不再稱高 80%，或低於 85%","action":"已持有者清倉，重啟條件歸零","source_freq":"財報電話會，季度","date":null,"evidence_refs":["competitive_share_entrants#0","substitute_technology#0"]},{"n":5,"text":"獲利承諾未兌現","type":"假設驗證","maps_to":"H2","metric":"FY2027 non-GAAP 營益率、SBC 占營收","threshold":"營益率 ≥23%，SBC ≤12%","action":"任一未達，已持有者減碼一半","source_freq":"公司財報，年度","date":"2028-02","evidence_refs":[]},{"n":6,"text":"EMEA 試點結果與推行時程","type":"假設驗證","maps_to":"H3","metric":"試點區新 ARR、既有客戶遷移安排","threshold":"試點區新 ARR 高於未試點區，且沒有強制遷移既有客戶","action":"未達則不追","source_freq":"財報電話會","date":"2027-02","evidence_refs":["channel_business_model_shift#1"]},{"n":7,"text":"證券訴訟從律所調查變成正式案件","type":"風險","maps_to":"R6","metric":"已提起訴訟、法院認證、和解金額","threshold":"集體認證加不利和解；或刑事介入","action":"集體認證加不利和解則減碼一半；刑事介入則清倉","source_freq":"SEC 文件與法院紀錄，事件","date":null,"evidence_refs":["major_events#2","lawsuit_class_action#0","lawsuit_class_action#1"]},{"n":8,"text":"夥伴通路占比下降","type":"風險","maps_to":"R4","metric":"夥伴及轉介客戶占營收","threshold":"FY2026 10-K 低於 45%","action":"已持有者減碼一半","source_freq":"10-K，年度","date":"2027-02","evidence_refs":["customer_concentration_credit#0"]},{"n":9,"text":"價格先走、證據未到","type":"風險","maps_to":"R1","metric":"週收盤價相對 52 週線","threshold":"站上 256.6 美元而重啟條件未成立","action":"不追","source_freq":"週線","date":null,"evidence_refs":[]}],"kill_metrics":[{"metric":"淨留存（NRR）","bear_threshold":"單季低於 100%","window":"單季","source":"季度財報電話會","last_status":"warning"},{"metric":"客戶金額留存","bear_threshold":"低於 85% 或管理層不再稱高 80%","window":"單季","source":"季度財報電話會","last_status":"ok"},{"metric":"單季淨新增客戶","bear_threshold":"低於 4,000 家","window":"連 2 季","source":"公司財報","last_status":"warning"},{"metric":"FY2027 營收指引中位數年增","bear_threshold":"低於 9%","window":"2027 年 2 月","source":"公司財報","last_status":"unknown"},{"metric":"FY2027 non-GAAP 營益率","bear_threshold":"低於 23%","window":"FY2027","source":"公司財報","last_status":"unknown"},{"metric":"TTM 毛利率","bear_threshold":"低於 80%","window":"TTM","source":"公司財報","last_status":"warning"}],"action_conditions":{"rearm_trigger":"三項同時成立才重跑判斷：淨留存連兩季≥102%，客戶金額留存仍為高80%，單季淨新增ARR年增轉正","exec_line":"目前不建倉，不設進場價，等 2027 年 2 月財報；已持有者停止加碼，淨留存跌破 100% 就清倉。"}},"decision_inputs":{"signal":"C","ma":"❌","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":true,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等事件，不等價位：連兩季淨留存 ≥102%，客戶金額留存仍為高 80%，單季淨新增 ARR 年增轉正；第一個檢查點是 2027 年 2 月財報。"},"thesis":{"H":[{"id":"H1","text":"安裝基礎止血：客戶金額留存守住高 80%，淨留存回到 102% 以上，淨新增 ARR 年增轉正。","2y":"2027 年淨留存 ≥102%，淨新增 ARR 年增轉正。","5y":null,"10y":null,"threshold":"FY2027 淨留存 ≥102%，客戶金額留存維持高 80%。","source":"季度財報電話會。","drift_rule":"連 2 季低於門檻為削弱，連 3 季低於 100% 為反轉；留存率波動小，5%／10% 的偏離過寬，改用絕對點數。"},{"id":"H2","text":"獲利品質改善：non-GAAP 營益率照承諾上升，同時 SBC 占營收下降。","2y":"FY2027 non-GAAP 營益率 23–24%，SBC 占營收 ≤12%。","5y":"FY2030 non-GAAP 30%、GAAP 20%、SBC 10%（公司目標，基準情境打折到 FY2031 的 27%）。","10y":null,"threshold":"FY2027 non-GAAP 營益率 ≥23%，SBC 占營收 ≤12%。","source":"2026-09-17 投資人日 CFO 與季度財報。","drift_rule":"2 年門檻：TTM 連 2 季偏離 ≥5% 為削弱，連 3 季 ≥10% 為反轉。5 年門檻：連 4 季偏離 ≥5% 為削弱，連 6 季 ≥10% 為反轉。"},{"id":"H3","text":"席位加 credit 的新定價帶來淨增量收入，而不是把舊收入重新切分。","2y":"2027 年底前揭露付費 credit 收入，試點區新 ARR 高於未試點區。","5y":"FY2031 營收成長 ≥7.5%。","10y":null,"threshold":"付費 credit 收入占訂閱營收 ≥3%，單客訂閱營收固定匯率年增 ≥3%。","source":"季度財報電話會與 EMEA 試點揭露（預計 2027 年 2 月）。","drift_rule":"2 年門檻：TTM 連 2 季偏離 ≥5% 為削弱，連 3 季 ≥10% 為反轉。到 2027 年底仍未揭露付費 credit 收入，視為削弱。"}],"R":[{"id":"R1","text":"2027 年指引低於市場：Q4 指引中位數已低於 Q3 實績，管理層說逆風延續到 2027 年。","h_ref":"H1","clock":"⚡","threshold":"FY2027 營收指引中位數年增 <9%，或單季淨新增客戶連 2 季 <4,000。","evidence_refs":["end_markets#2","capital_markets_pricing#0","supply_demand_durability#1"]},{"id":"R2","text":"定價改革把既有收入重新訂價：試點 ASP 較低，一旦推到既有客戶，影響約 36 億美元的訂閱收入。","h_ref":"H3","clock":"🔥","threshold":"單客訂閱營收固定匯率年增連 2 季 <1%，或宣布強制遷移既有客戶。","evidence_refs":["channel_business_model_shift#1"]},{"id":"R3","text":"通用 LLM 與 AI 原生 CRM 從低階客戶開始替代。","h_ref":"H1","clock":"🐢","threshold":"客戶金額留存低於 85% 或管理層不再稱高 80%。","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1","competitive_share_entrants#2","substitute_technology#0"]},{"id":"R4","text":"夥伴通路占營收約 49%，AI 壓縮夥伴的服務收入；公司同時要靠夥伴協助試用轉付費，自家專業服務收入卻在下滑。","h_ref":"H1","clock":"🔥","threshold":"夥伴及轉介客戶占營收低於 45%。","evidence_refs":["customer_concentration_credit#0","end_markets#0"]},{"id":"R5","text":"主要基礎設施集中在第三方雲端，FY2021 10-K 已揭露，2025-10-20 AWS us-east-1 中斷也證實這個風險仍在。","h_ref":"H1","clock":"🐢","threshold":"單次中斷影響主要區域超過 24 小時，且造成可量化的客戶補償。","evidence_refs":["geo_supply_chain#0","geo_supply_chain#1"]},{"id":"R6","text":"法律與法規：律所調查尚未成案，CIPA 追蹤器訴訟有前例，州級 AI 法規各自為政。","h_ref":"H2","clock":"🐢","threshold":"證券集體訴訟獲認證，或單一州法規迫使主要 AI 功能停用。","evidence_refs":["regulatory_antitrust#2","major_events#2","lawsuit_class_action#0","lawsuit_class_action#1"]},{"id":"R7","text":"AI 成本與股權報酬拖累獲利品質，營益率靠人力節省撐住。","h_ref":"H2","clock":"🔥","threshold":"TTM 毛利率 <80%，或 SBC 占營收回升到 14% 以上。","evidence_refs":["major_events#1"]}],"single_thing":{"description":"淨留存單季跌破 100%，代表既有客戶整體開始縮水。目前為 101%，全年看法已改為降約 2 點。","why_fatal":"這是基準情境最大的單一敏感度。每年少 1 點淨留存，五年後約少 5% 營收，FY2031 約 2.8 億美元，以 80% 流量換算每股約少 4 美元，占基準 EPS 約 15%；同年 1 點營益率只值約 1 美元。跌破 100% 後成長只能靠新客，而新客已在放慢，倍數也會跟著壓縮。","if_happens":"結論轉為不持有，已持有者清倉；重啟至少等連兩季回到 102%。","how_monitor":"每季財報電話會揭露的淨留存，下一次在 2027 年 2 月；同時看客戶金額留存與加購拖累的說法。","probability":"12–24 個月約 40%"}},"appendix_a":{"growth_durability":5,"quality_score":5,"ai_risk":"🔴","long_term_confidence":"低","fpe_fy2":11.93,"peg_fy2":0.43,"stress":{"pass":2,"total":3}},"eps_meta":{"base_eps_path":{"FY2025A":9.71,"FY2026E":13.3,"FY2027E":16.82,"FY2028E":20.21},"fy_end_month":12,"eps_basis":"Non-GAAP 稀釋 EPS。FY2025A 由公司 FY2026 指引 13.59–13.61 美元與電話會所稱年增 40% 回推，約 9.71 美元，因年增率四捨五入約有 ±0.04 美元誤差；GAAP 0.86 美元為不同口徑。FY2026E 到 FY2028E 為 2026-11-07 Koyfin 共識快照，分析師家數事實表未涵蓋；FY2026E 13.3 美元低於公司新指引，快照應未更新 Q3。"},"catalysts":[{"date":"2027-02","date_precision":"month","type":"guidance","event":"Q4 2026 財報與 2027 年首次年度指引","impact":"高","watch":"營收成長、營益率指引、淨留存與淨新增客戶"},{"date":"2027-02","date_precision":"month","type":"product","event":"EMEA 席位加 credit 試點結果與後續推行時程","impact":"高","watch":"試點區新 ARR、ASP、既有客戶是否遷移"}],"decision_out":{"verdict":"迴避","role":"不持有","row_hit":"2","pacing":["row4：週線❌，進場節奏強制分批（starter 1/3＋趨勢確認後加碼），頁首掛「⚠️ 週線趨勢未確認，逢回分批勿接刀」"],"holding_cap":null,"audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='C'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":true,"basis":"thesis_irreconcilable=True"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":true,"basis":"moat_trend='↓', moat='C'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":true,"basis":"ma='❌'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]}],"requires_critic":[]}}
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
