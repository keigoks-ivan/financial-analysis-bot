你是 DD 管線 v20 的判斷層閘（gate），標的 BESI（20261025）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（35 條）
- `f_kpi0_ifrs`（q1_business）｜營收（IFRS）＝283.4 €M（YoY +113.6%、QoQ +13.4%）｜期間與口徑：Q3-2026（季末 2026-09-30，公告於 2026-10-22）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 https://www.besi.com/investor-relations/press-releases/details/be-semiconductor-industries-nv-announces-q3-2026-results/（numbers.latest_quarter_kpis.items[0]，as_of Q3-2026（季末 2026-09-30，公告於 2026-10-22））
- `f_kpi1_orders`（q1_business）｜訂單 orders＝342.6 €M（YoY +96.1%、QoQ +17.0%）｜期間與口徑：Q3-2026（季末 2026-09-30，公告於 2026-10-22）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 https://www.besi.com/investor-relations/press-releases/details/be-semiconductor-industries-nv-announces-q3-2026-results/（numbers.latest_quarter_kpis.items[1]，as_of Q3-2026（季末 2026-09-30，公告於 2026-10-22））
- `f_kpi2`（q1_business）｜毛利率＝65.2 %｜期間與口徑：Q3-2026（季末 2026-09-30，公告於 2026-10-22）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 https://www.besi.com/investor-relations/press-releases/details/be-semiconductor-industries-nv-announces-q3-2026-results/（numbers.latest_quarter_kpis.items[2]，as_of Q3-2026（季末 2026-09-30，公告於 2026-10-22））
- `f_kpi3`（q1_business）｜淨利＝107.2 €M（YoY +323.7%、QoQ +20.4%；淨利率 37.8%）｜期間與口徑：Q3-2026（季末 2026-09-30，公告於 2026-10-22）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 https://www.besi.com/investor-relations/press-releases/details/be-semiconductor-industries-nv-announces-q3-2026-results/（numbers.latest_quarter_kpis.items[3]，as_of Q3-2026（季末 2026-09-30，公告於 2026-10-22））
- `f_kpi4`（q1_business）｜營業費用＝55.1 €M｜期間與口徑：Q3-2026（季末 2026-09-30，公告於 2026-10-22）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 https://www.besi.com/investor-relations/press-releases/details/be-semiconductor-industries-nv-announces-q3-2026-results/（numbers.latest_quarter_kpis.items[4]，as_of Q3-2026（季末 2026-09-30，公告於 2026-10-22））
- `f_kpi5`（q1_business）｜期末淨現金＝246.6 €M｜期間與口徑：Q3-2026（季末 2026-09-30，公告於 2026-10-22）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 https://www.besi.com/investor-relations/press-releases/details/be-semiconductor-industries-nv-announces-q3-2026-results/（numbers.latest_quarter_kpis.items[5]，as_of Q3-2026（季末 2026-09-30，公告於 2026-10-22））
- `f_kpi6_q4_26`（q1_business）｜Q4-26 指引＝營收 持平±5%（相對 Q3 €283.4M）；毛利率 63–65%；營業費用 +5–10%（相對 €55.1M） 文字｜期間與口徑：Q3-2026（季末 2026-09-30，公告於 2026-10-22）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司 IR 新聞稿 https://www.besi.com/investor-relations/press-releases/details/be-semiconductor-industries-nv-announces-q3-2026-results/（numbers.latest_quarter_kpis.items[6]，as_of Q3-2026（季末 2026-09-30，公告於 2026-10-22））
- `f_kpi7_hybrid_bonding`（q1_business）｜hybrid bonding 累計需求／訂單＝累計單位需求 >215 台；YTD-26 hybrid bonding 訂單較 FY2025 翻倍以上 文字｜期間與口徑：Q3-2026（季末 2026-09-30，公告於 2026-10-22）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司 IR 新聞稿 https://www.besi.com/investor-relations/press-releases/details/be-semiconductor-industries-nv-announces-q3-2026-results/（numbers.latest_quarter_kpis.items[7]，as_of Q3-2026（季末 2026-09-30，公告於 2026-10-22））
- `f_peer_besi_gross_margin_pct`（q2_moat）｜BESI 毛利率＝64.25 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.BESI.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_besi_operating_margin_pct`（q2_moat）｜BESI 營業利益率＝36.36 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.BESI.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_besi_fcf_margin_pct`（q2_moat）｜BESI FCF 利潤率＝23.08 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.BESI.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_klic_gross_margin_pct`（q2_moat）｜KLIC 毛利率＝48.18 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.KLIC.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_klic_operating_margin_pct`（q2_moat）｜KLIC 營業利益率＝13.21 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.KLIC.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_klic_fcf_margin_pct`（q2_moat）｜KLIC FCF 利潤率＝4.21 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.KLIC.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_042700_ks_gross_margin_pct`（q2_moat）｜042700.KS 毛利率＝57.35 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.042700.KS.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_042700_ks_operating_margin_pct`（q2_moat）｜042700.KS 營業利益率＝42.49 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.042700.KS.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_042700_ks_fcf_margin_pct`（q2_moat）｜042700.KS FCF 利潤率＝18.69 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.042700.KS.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_amat_gross_margin_pct`（q2_moat）｜AMAT 毛利率＝49.4 %｜期間與口徑：TTM ending 2026-07-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.AMAT.gross_margin_pct，as_of TTM ending 2026-07-31（4季加總））
- `f_peer_amat_operating_margin_pct`（q2_moat）｜AMAT 營業利益率＝31.09 %｜期間與口徑：TTM ending 2026-07-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.AMAT.operating_margin_pct，as_of TTM ending 2026-07-31（4季加總））
- `f_peer_amat_fcf_margin_pct`（q2_moat）｜AMAT FCF 利潤率＝18.23 %｜期間與口徑：TTM ending 2026-07-31（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.AMAT.fcf_margin_pct，as_of TTM ending 2026-07-31（4季加總））
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝4.96 USD/share｜期間與口徑：2026-10-24／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261024.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-10-24）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝7.27 USD/share｜期間與口徑：2026-10-24／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261024.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-10-24）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝9.31 USD/share｜期間與口徑：2026-10-24／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261024.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-10-24）
- `f_consensus_rev_fy2_pct`（q5_valuation）｜FY2 共識修正＝-0.55 %｜期間與口徑：2026-10-24／兩份 Koyfin 快照之間的 EPS 修正幅度（7.31 → 7.27）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261024.xlsx（numbers.consensus_revision.fy2.revision_pct，as_of 2026-10-24）
- `f_consensus_rev_fy3_pct`（q5_valuation）｜FY3 共識修正＝-1.59 %｜期間與口徑：2026-10-24／兩份 Koyfin 快照之間的 EPS 修正幅度（9.46 → 9.31）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261024.xlsx（numbers.consensus_revision.fy3.revision_pct，as_of 2026-10-24）
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝0.0 %｜期間與口徑：2026-07-30 → 2026-10-24／FY1 共識 EPS 4.96 → 4.96（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261024.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-10-24）
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝29.25 x｜期間與口徑：2026-10-24／分母＝FY1 EPS 4.96，分子＝快照價 145.1｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-10-24）
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝1.089 %｜期間與口徑：2026-10-25／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-10-25）
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝145.1 USD｜期間與口徑：2026-10-23（RTH 收盤，日線 fallback）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-10-23（RTH 收盤，日線 fallback））
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝-42.1 %｜期間與口徑：2026-10-23（RTH 收盤，日線 fallback）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-10-23（RTH 收盤，日線 fallback））
- `f_rsi14`（q5_valuation）｜RSI(14)＝30.44｜期間與口徑：2026-10-23（RTH 收盤，日線 fallback）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-10-23（RTH 收盤，日線 fallback））
- `f_ma_state`（q5_valuation）｜週線均線六態（decision_inputs.ma 必須等於此值）＝🟠｜期間與口徑：2026-10-25／timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-10-25）
  - 原文：「price 145.1 / W52 197.59 / W104 156.63 / W250 116.99 / W250 13週斜率 1.49%」
- `f_ma_w52`（q5_valuation）｜52 週均線＝197.59 USD｜期間與口徑：2026-10-25／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-10-25）
- `f_ma_w104`（q5_valuation）｜104 週均線＝156.63 USD｜期間與口徑：2026-10-25／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-10-25）
- `f_ma_w250`（q5_valuation）｜250 週均線＝116.99 USD｜期間與口徑：2026-10-25／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-10-25）

### findings_digest 中方向為負或來源衝突的條目（15 條）
- `competitive_share_entrants#0`（competitive_share_entrants｜方向 -｜狀態 ok）：TrendForce 2026-03：BESI 仍居混合鍵合機台首位，但 Hanmi、Hanwha Semitek、LG、SEMES、ASMPT 皆在建立混合鍵合能力，競爭開始浮現；未見任何對手 2026 年取得具名客戶混合鍵合訂單。
  - 來源：TrendForce News 2026-03-13 Hybrid bonding leader BESI reportedly draws takeover interest（as_of 2026-03-13）｜affects：moat_trend、decision_inputs.bear
- `competitive_share_entrants#1`（competitive_share_entrants｜方向 -｜狀態 ok）：Bits&Chips：BESI 執行長表示全球有約二十款鍵合機在開發，並出現數家中國業者；Canon 目標 2026 推出、LG 目標 2028。
  - 來源：Bits&Chips: Besi leads hybrid bonding race with twenty players chasing（as_of 2026-01-01）｜affects：moat_trend、thesis.R
- `competitive_share_entrants#2`（competitive_share_entrants｜方向 -｜狀態 ok）：報導稱 ASML 正開發混合鍵合機台，挑戰 BESI；BofA 認為不會假設其取得顯著份額；ASML 未公布產品或時程。
  - 來源：The Next Web: ASML's chip packaging move threatens Besi shares, Bank of America says; Dealroom 轉載（as_of 2026-10-01）｜affects：moat_trend、decision_inputs.bear
- `customer_second_source#0`（customer_second_source｜方向 -｜狀態 ok）：Bits&Chips 評論：TSMC 為 Besi 目前最重要客戶，預期將導入第二家 hybrid bonding 供應商（評論，非確認報導）；ASMPT、Süss、Shibaura 已出貨 hybrid bonding 設備
  - 來源：Bits&Chips - Besi's blue ocean is slowly turning redder（as_of 2026-06-01）｜affects：moat_trend、decision_inputs.bear
- `customer_second_source#1`（customer_second_source｜方向 -｜狀態 ok）：TrendForce：韓國 LG Electronics、SEMES、Hanmi、Hanwha Semitech 與 ASMPT 正建立競爭性 hybrid bonding 能力；SK hynix 於 2026-03 訂購 Kinex 系統
  - 來源：TrendForce News 2026-03-13（as_of 2026-03-13）｜affects：moat_trend
- `customer_concentration_credit#1`（customer_concentration_credit｜方向 -｜狀態 ok）：2026 Q1 混合鍵合成長主要來自單一客戶超預期的產能建置，顯示單一客戶訂單可左右單季
  - 來源：debelegger.nl 分析（引述 BESI Q1-26 說明）（as_of 2026-04-30）｜affects：decision_inputs.bear、thesis.R
- `supply_demand_durability#3`（supply_demand_durability｜方向 -｜狀態 ok）：SK Hynix將混合鍵合推遲至HBM5，可能延後Besi記憶體機會
  - 來源：Bits&Chips（as_of 2026-07-01）｜affects：decision_inputs.bear、thesis.R
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：荷蘭投資網站指出地緣政治、出口規範、客戶集中與匯率可能影響 BESI 2026 年的可預測性與利潤率
  - 來源：debelegger.nl 'Hybrid bonding maakt Besi kansrijk, maar dit zijn de valkuilen in 2026'（as_of 2026-01-29）｜affects：decision_inputs.bear、thesis.R
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：Bits&Chips 報導 Besi 混合鍵合領先但約二十個平台競爭，包含數家中國業者
  - 來源：bits-chips.com 'Besi leads hybrid bonding race with twenty players chasing'（as_of 2026-04-01）｜affects：moat_trend
- `end_markets#2`（end_markets｜方向 -｜狀態 ok）：BofA稱ASML進入混合鍵合支援可能對Besi構成壓力，但分析師未假設其取得顯著市佔
  - 來源：TheNextWeb: ASML's chip packaging move threatens Besi shares, Bank of America says（as_of 2026-10-06）｜affects：moat_trend、decision_inputs.bear
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：ASMPT、Süss、Shibaura 已出貨混合鍵合設備，韓國四家業者追逐 SK Hynix／Samsung；Bits&Chips 認為混合鍵合不再是 BESI 的藍海
  - 來源：Bits&Chips, BESI's blue ocean is slowly turning redder（as_of 2026-07-01）｜affects：moat_trend、decision_inputs.bear
- `substitute_technology#2`（substitute_technology｜方向 -｜狀態 ok）：全球約二十個混合鍵合平台在開發，BESI CEO 承認設備商大量進入、中國業者出現
  - 來源：Bits&Chips, BESI leads hybrid bonding race with twenty players chasing（as_of 2026-07-01）｜affects：moat_trend、decision_inputs.bear
- `substitute_technology#3`（substitute_technology｜方向 -｜狀態 ok）：韓國業者 LG、SEMES、Hanmi、Hanwha Semitech 開發混合鍵合機，ASMPT 也在建立能力，BESI 仍領先
  - 來源：TrendForce, Hybrid bonding leader BESI reportedly draws takeover interest（as_of 2026-03-13）｜affects：moat_trend
- `cyclical_supply_discipline_capacity#1`（cyclical_supply_discipline_capacity｜方向 -｜狀態 ok）：Hanmi 於仁川興建混合鍵合機工廠，投資 1000 億韓元，目標 2026 下半年完工、2027 年底前推出設備（同業新進入者，不同來源投資額不一致）。
  - 來源：Asiae, Hanmi Semiconductor Invests 100 Billion KRW in Hybrid Bonder Development（as_of 2025-07-25）｜affects：moat_trend、decision_inputs.bear
- `cyclical_prior_downcycle_behavior#0`（cyclical_prior_downcycle_behavior｜方向 -｜狀態 ok）：2019 下行：H1-19 營收年減 44.9%，但毛利率 55.9%（H1-18 為 56.5%），毛利率僅小幅下滑
  - 來源：Besi Q2-19 and H1-19 results press release（as_of 2019-07-25）｜affects：decision_inputs.bear、thesis.R

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 8 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/BESI_20261025/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":432.0,"bear_5y_price":84.0,"p_bull_pct":25,"p_bear_pct":32,"upside_5y_pct":47.6,"ev5y_pct":56.4,"irr_base_pct":8.1,"asym_ratio":3.7,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":4.96,"pe":29.25,"basis":"FY1（FY2026E）共識 EPS 4.96，前瞻口徑；終端倍數套用終端年 EPS，事實表無同業本益比可對照，錨定自身 FY1 29 倍與 FY2 20 倍"},"eps":{"bull":[7.8,10.5,12.0,14.0,16.0],"base":[6.9,8.3,7.4,8.8,10.2],"bear":[6.0,4.6,3.6,4.6,5.6]},"pe":{"bull":27,"base":21,"bear":15},"p":{"bull":25,"base":43,"bear":32},"yield_pct":{"dividend":1.089,"net_buyback":0.5},"second_stage":{"bull_cagr_pct":14,"base_cagr_pct":9},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### BESI_Q2_2026_Earnings_Call_20260723.md
- 2026-07-23｜Richard Blickman｜guidance：管理層預告 Q3 營收較 Q2 成長 10%–15%。（原話："will increase by 10% to 15% versus the second quarter"）
- 2026-07-23｜Richard Blickman｜margin：Q3 毛利率預期降至 63%–65%，管理層歸因於產品組合較不有利。（原話："anticipated to decrease to a range between 63% and 65%"）
- 2026-07-23｜Richard Blickman｜guidance：Q3 營業費用預期持平至增加 5%，主因研發支出增加。（原話："Operating expenses are anticipated to be flat to up 5%"）
- 2026-07-23｜Richard Blickman｜guidance：管理層表示 Q3 訂單動能持續。（原話："order momentum continuing in the third quarter of this year"）
- 2026-07-23｜Richard Blickman｜margin：管理層拆解營業槓桿：基線營業費用占營收比由去年 Q2 的 30% 降至 Q2'26 的 18.9%。（原話："operating expenses reduced from 30% of revenue in Q2 last"）
- 2026-07-23｜Richard Blickman｜product：管理層估計 AI 應用占系統訂單比重上半年約 60%，去年同期約 50%。（原話："Overall, we estimate that system orders for AI"）
- 2026-07-23｜Richard Blickman｜customer：Q2 新增混合鍵合訂單，來自 2 個既有客戶與 1 個新的超大規模客戶。（原話："Additional hybrid orders were received in the second quarter"）
- 2026-07-23｜Richard Blickman｜customer：混合鍵合客戶數由 2025 年底 15 家增至 Q2'26 底 21 家。（原話："Hybrid bonding customers adoption increased from 15 at"）
- 2026-07-23｜Richard Blickman｜customer：答分析師：超大規模客戶的訂單可能用於穿戴式（眼鏡）；另兩家一為 CPO、一為邏輯。（原話："the hyperscaler is probably for wearables."）
- 2026-07-23｜Richard Blickman｜competition：HBM 混合鍵合：三大記憶體廠之一正在評估，另一家剛開始評估。（原話："Also, we've indicated that another one is starting the"）
- 2026-07-23｜Richard Blickman｜competition：管理層轉述業界對 HBM 採用混合鍵合時程的不同看法（延後 vs. 近在眼前）。（原話："Some are voicing that it may delay."）
- 2026-07-23｜Richard Blickman｜competition：針對 JEDEC 放寬 HBM4E 厚度限制，管理層表示高度放寬不改變混合鍵合的效能與散熱優勢。（原話："heat or the height does not change that characteristic."）
- 2026-07-23｜Richard Blickman｜risk：管理層指出 HBM 混合鍵合量產的主要障礙是成本與良率。（原話："The major hurdles are simply cost and yield."）
- 2026-07-23｜Richard Blickman｜risk：以台灣邏輯大客戶為參照，管理層說明驗證歷時超過三年。（原話："It took us over 3 years."）
- 2026-07-23｜Richard Blickman｜risk：管理層談產能過剩：過往上行週期約 6–8 季後出現過剩。（原話："cycle last 6 quarters, maybe 8 and then you are bound to"）
- 2026-07-23｜Richard Blickman｜risk：被問是否走向產能過剩，管理層答以時間會證明。（原話："So are we heading into an overcapacity? Time will tell."）
- 2026-07-23｜Richard Blickman｜guidance：解釋 Q3 營收逆季節性成長：下游由智慧型手機轉為 AI 資料中心，訂單動能延續但組合不同。（原話："we have continued order momentum, but with a different mix."）
- 2026-07-23｜Richard Blickman｜commitment：AP7 擴產：管理層稱若按計畫，下半年可能再有一輪訂單，交期約 6 個月。（原話："we don't know, with a lead time of about 6 months"）
- 2026-07-23｜Richard Blickman｜commitment：管理層預期表現將顯著優於 Tech Insights 的市場成長預測（2025–2028 年 53%）。（原話："significantly exceed such projected growth rates"）
- 2026-07-23｜Richard Blickman｜commitment：管理層轉述客戶說法：處於多年期 AI 資本支出週期。（原話："Customers indicate that we are in a multiyear AI CapEx cycle"）
- 2026-07-23｜Richard Blickman｜capital_allocation：Q2 末淨現金增至 1.64 億歐元，可轉債轉股並支付年度股利。（原話："Our net cash position at the end of the second quarter '26"）
- 2026-07-23｜Richard Blickman｜capital_allocation：Q2 支付年度股利 1.254 億歐元。（原話："payment of EUR 125.4 million for the annual dividend"）
- 2026-07-23｜Richard Blickman｜product：TC Next 目前為單台訂單，尚未大量。（原話："single systems, not yet major volume."）
- 2026-07-23｜Richard Blickman｜product：CoWoS-like 已是訂單的重要部分，自 Q4 起持續。（原話："That's already a significant part of the orders."）
- 2026-07-23｜Richard Blickman｜product：IDM 訂單增加屬非混合鍵合的主流產品，車用仍未改善。（原話："still not very much improving is automotive."）
- 2026-07-23｜Richard Blickman｜product：混合鍵合用於高階手機的訂單尚未出現。（原話："Not yet we have seen those orders."）
- 2026-07-23｜Richard Blickman｜customer：被問台灣大客戶是否放緩，管理層稱未見放緩。（原話："but we don't see any slowdown in that."）

### BESI_Analyst_Investor_Day_BE_Semiconductor_Industries_N_V_20260618.md
- 2026-06-18｜Richard Blickman｜guidance：管理層說當天上午公布的目標模型區間由 EUR 1.5–1.9 billion 上調為 EUR 1.7–2.2 billion。（原話："up from EUR 1.5 billion to EUR 1.9 billion"）
- 2026-06-18｜Richard Blickman｜guidance：管理層提到部分分析師在第一時間的評論中對新模型略感失望。（原話："several of you, I won't call names, are a bit"）
- 2026-06-18｜Richard Blickman｜guidance：新模型 EUR 1.7–2.2 billion 中，Engine 1 部分約 EUR 1.1 billion,其餘為 Sub Micron。（原話："About EUR 1.1 billion is the Engine 1 part of that."）
- 2026-06-18｜Richard Blickman｜guidance：Sub Micron 目標由 EUR 0.5–0.9 billion 調為 EUR 0.6–1.1 billion,理由是邏輯晶片持續導入，區間差異取決於 HBM 導入。（原話："Submicron up from EUR 0.5 billion to EUR 0.9 billion"）
- 2026-06-18｜Richard Blickman｜guidance：管理層稱目標相較上次 Investor Day 提高約 15%,且對應已識別的客戶與業務。（原話："increased by about 15% versus last Investor Day"）
- 2026-06-18｜Richard Blickman｜guidance：管理層說明 HBM 導入速度會讓 Sub Micron 區間偏上緣的時點快或慢約 1–2 年。（原話："in a somewhat 1, 2 years slower trend"）
- 2026-06-18｜Peter Wiedner｜guidance：Peter Wiedner 說混合鍵合低情境(邏輯加 CPO)的機台數假設較去年模型增加 18%。（原話："we can increase that for 18% versus our last year model"）
- 2026-06-18｜Peter Wiedner｜guidance：加入手機與智慧眼鏡等邊緣裝置的高情境，整體較去年增加 12%。（原話："which then increases overall by 12%"）
- 2026-06-18｜Peter Wiedner｜guidance：混合鍵合機台累計需求的高情境上調至 2,200 台。（原話："up to a cumulative 2,200 machines"）
- 2026-06-18｜Peter Wiedner｜guidance：混合鍵合機台累計需求的低情境上調至 1,150 台。（原話："to 1,150 machines"）
- 2026-06-18｜Christoph Scheiring｜guidance：Mainstream die attach 的可及市場模型更新為 EUR 1.6 billion 水準，較上次約增 8%。（原話："addressable market model to a EUR 1.6 billion level"）
- 2026-06-18｜Christoph Scheiring｜guidance：Christoph 稱到 2030 年可及市場成長約 2 倍，並說相較去年模型上修。（原話："addressable market growing by a factor of 2 until 2030"）
- 2026-06-18｜Richard Blickman｜guidance：管理層形容目前處於 AI 帶動的大型上行循環的起點。（原話："We are at the very beginning of a significant up cycle"）
- 2026-06-18｜Richard Blickman｜guidance：舉去年例子說明模型偏保守：2025 年營收中約 40% 是年初預算之外的業務。（原話："about 40% of that EUR 600 million"）
- 2026-06-18｜Richard Blickman｜margin：管理層回顧毛利率在下行期往 62%、63% 靠。（原話："it was a bit trending towards 62%, 63%."）
- 2026-06-18｜Richard Blickman｜margin：管理層拆解口徑：淨利率低點 21%,依 Q2 毛利率與營業費用指引，淨利率會回到 30% 以上。（原話："it should move well again"）
- 2026-06-18｜Richard Blickman｜margin：管理層解釋調高營業利益率目標的理由：產品轉向更複雜的先進封裝。（原話："if you do your homework right, you have higher margins"）
- 2026-06-18｜Richard Blickman｜margin：管理層對市占率的口徑：市占是結果，先看毛利潛力。（原話："market share is an end result"）
- 2026-06-18｜Peter Wiedner｜margin：回應定價問題：每提高一級精度，機台價格都會上升，沒有給出具體數字。（原話："the price level is definitely going up with each increased"）
- 2026-06-18｜Richard Blickman｜margin：產能口徑：以每年 300 台、平均單價 2.5 million 概算混合鍵合機台產出。（原話："multiply that by 2.5 million as an average price"）
- 2026-06-18｜Christoph Scheiring｜margin：管理層稱低端製程轉向中國競爭者的業務因價格敏感、毛利不如預期而不追。（原話："we are not interested in as it is very, very price sensitive"）
- 2026-06-18｜Richard Blickman｜commitment：Richard 說明目前產能約每年 300 台混合鍵合機，下一階段已備妥。（原話："we are now at a level of building 300"）
- 2026-06-18｜Richard Blickman｜commitment：管理層承諾今年底前越南開始組裝首批鍵合機，自馬來西亞遷出部分產線。（原話："we will build the first bonders in Vietnam"）
- 2026-06-18｜Richard Blickman｜commitment：管理層說調整營運模型的方法是每次把產能加倍，這次打算準備得比加倍更多。（原話："we have always used the simple method, doubling each time"）
- 2026-06-18｜Richard Blickman｜commitment：管理層承認內部仍有改善空間，並以此說明目標調高屬自然管理。（原話："wrong in our company, there's still a lot to improve"）
- 2026-06-18｜Richard Blickman｜capital_allocation：管理層說明研發支出逐步增加。（原話："you see a gradual increase in R&D spends"）
- 2026-06-18｜Richard Blickman｜capital_allocation：對併購傳聞不回應，並稱產業併購近乎不存在，夥伴關係為主要路線。（原話："partnerships is the way to go"）
- 2026-06-18｜Peter Wiedner｜competition：Peter 稱 Besi 的混合鍵合機台路線圖與產品線沒有競爭對手能比。（原話："no other competitor of us is matching"）
- 2026-06-18｜Richard Blickman｜competition：Richard 提到市場上已宣布的混合鍵合機供應商超過 10 家，包含中國廠商。（原話："somebody counted there are over 10 Hybrid"）
- 2026-06-18｜Richard Blickman｜competition：Richard 承認是否擁有最佳鍵合機仍是挑戰。（原話："Whether we have the best bonder is still the challenge."）
- 2026-06-18｜Richard Blickman｜competition：Richard 回答領先期限：現行 100nm 為業界標準，競爭者將在下一輪切入。（原話："Competition will get in with the next round."）
- 2026-06-18｜Chris Scanlan｜competition：Chris 回應晶圓對晶圓鍵合的威脅問題：不認為對邏輯與記憶體堆疊構成威脅。（原話："we don't see a threat coming from wafer-to-wafer bonding"）
- 2026-06-18｜Peter Wiedner｜product：下一代 N50 機台(50nm 精度)的定位。（原話："which we call the N50, N50 for 50-nanometer"）
- 2026-06-18｜Peter Wiedner｜product：N50 今年開始在客戶端進行 beta 測試。（原話："start actually the beta test at the customer site this year"）
- 2026-06-18｜Peter Wiedner｜product：Peter 稱第一家 HBM 廠商將在 2027 年的 HBM4e 導入混合鍵合。（原話："will adopt the hybrid interconnect in HBM 4e in '27"）
- 2026-06-18｜Chris Scanlan｜product：Chris 重申 HBM 混合鍵合的首次導入點為 HBM4e,之後 HBM5 擴大。（原話："the intercept for hybrid bonding for HBM memory"）
- 2026-06-18｜Peter Wiedner｜product：Peter 稱 HBM5 世代時機台市場將以混合鍵合為主，而非 TCB。（原話："definitely far more than 50% will be hybrid"）
- 2026-06-18｜Peter Wiedner｜product：Peter 稱 CPO 在一年內從研發走到量產，是去年最令人興奮的發展，並放入低情境。（原話："the CPO has developed in one year into volume manufacturing"）
- 2026-06-18｜Peter Wiedner｜product：Peter 說明 HBM 仍留在中情境：為了與歷史圖表一致，而非不確定其會發生。（原話："not because we are not convinced it's not coming"）
- 2026-06-18｜Chris Scanlan｜product：Chris 稱 Arm 架構 CPU 供應商目前尚無採用混合鍵合者。（原話："for all the ARM CPU suppliers, none of them yet are using"）
- 2026-06-18｜Richard Blickman｜customer：Richard 稱已有超過 20 家客戶購買混合鍵合機。（原話："over 20 customers who have bought hybrid bonders"）
- 2026-06-18｜Peter Wiedner｜customer：Peter 稱三大 HBM 供應商都在評估混合鍵合，且都使用 Besi 機台。（原話："And by the way, they all do it with our machines."）
- 2026-06-18｜Christoph Scheiring｜customer：Christoph 稱 Chameo Flex 已完成一家客戶驗證，正等首張採購單。（原話："I'm expecting the first purchase order any moment"）
- 2026-06-18｜Christoph Scheiring｜customer：Christoph 稱 TSMC 將部分晶片對晶圓作業外包給 OSAT。（原話："TSMC decided to outsource their internal chip-to-"）
- 2026-06-18｜Peter Wiedner｜customer：Peter 稱已與美國 Terafab 團隊開始討論，對方確認會含封裝。（原話："also for us a large opportunity, the Terafab"）
- 2026-06-18｜Christoph Scheiring｜customer：Christoph 稱 Engine 1 中光子(收發器)占比將提高，部分取代過去較大的手機占比。（原話："the Photonics portion is seeing an increase"）
- 2026-06-18｜Peter Wiedner｜customer：Peter 稱手機應用處理器導入混合鍵合最大推力來自中國。（原話："I see the biggest drive for that coming out of China"）
- 2026-06-18｜Peter Wiedner｜customer：Peter 稱服務收入正加速，因混合鍵合裝在客戶前段廠，有常駐與服務合約。（原話："the service part is accelerating as we speak"）
- 2026-06-18｜Richard Blickman｜risk：Richard 提醒歷史上產業會出現高峰，表示不預測時點。（原話："if history repeats itself, that is what you should be"）
- 2026-06-18｜Richard Blickman｜risk：Richard 說產業發展從來不是直線。（原話："it's never a straight line"）
- 2026-06-18｜Christoph Scheiring｜risk：Christoph 稱中國市場競爭強度很高，受當地廠商與政策推動。（原話："the competitive intensity there is very high"）
- 2026-06-18｜Richard Blickman｜risk：Richard 稱為因應地緣政治，正檢視機台中的美國零件以減少使用。（原話："that we have less U.S. components in our"）

### 問答異常語氣（迴避／改口／保留）
- BESI_Q2_2026_Earnings_Call_20260723.md｜問：Robert Sanders（Deutsche Bank）問 2.5D 產能過剩風險最擔心什麼。｜答法：未直接指出擔憂來源，引用歷史週期統計，結尾稱『Nobody knows』並向提問者致歉無法給更好答案。
- BESI_Q2_2026_Earnings_Call_20260723.md｜問：Robert Sanders 問 Q2 混合鍵合出貨與訂單台數。｜答法：明確不揭露台數，只改報客戶數 21 家。
- BESI_Q2_2026_Earnings_Call_20260723.md｜問：Didier Scemama（BofA）與 Charles Shi（Needham）問 HBM 混合鍵合各客戶驗證進度與採用時程。｜答法：不給各家進度與時程，稱『下半年會更清楚』、『拭目以待』，僅說有一家進展最快。
- BESI_Analyst_Investor_Day_BE_Semiconductor_Industries_N_V_20260618.md｜問：Ruben Devos 追問：HBM 為何仍只放中情境、去年提的 AI 邏輯 500 台目標為何不再重複。｜答法：Peter 以保持圖表與歷史一致為由回答 HBM 的情境位置，對 500 台目標未重述數字，改談 NVIDIA 已含在先前預測中、變動主要來自 CPO。
- BESI_Analyst_Investor_Day_BE_Semiconductor_Industries_N_V_20260618.md｜問：François-Xavier Bouvignies(UBS)問下一代工具何時出現、5–10 年精度路線圖、以及機台定價空間。｜答法：定價只答價格會隨精度上升，未給數字;精度路線圖答客戶目標約 1 micron 以下，在本十年結束前，未給 N50 以外的具體時點。
- BESI_Analyst_Investor_Day_BE_Semiconductor_Industries_N_V_20260618.md｜問：Michael Roeg 追問：過去 5 年已售出逾 EUR 2 billion 設備，服務收入卻持平，為什麼。｜答法：Peter 以保固期延遲與早年混合鍵合出貨量小回答，分析師再度追問時，Peter 轉為說明覆晶機台不賣服務合約，未提供服務收入的數字。
- BESI_Analyst_Investor_Day_BE_Semiconductor_Industries_N_V_20260618.md｜問：分析師問市場對 Besi 被收購的傳聞，是否還需要夥伴。｜答法：Richard 未直接回答，只稱不回應傳聞，轉而強調對自身策略的信心與 Applied Materials 夥伴關係。
- BESI_Analyst_Investor_Day_BE_Semiconductor_Industries_N_V_20260618.md｜問：Martin Marandon(ODDO BHF)問 Besi 相對競爭者的領先幅度，以及是否有僅 Besi 進入驗證的 15nm 級產品。｜答法：Richard 未舉出具體客戶或產品例子，也說領先期限難以回答，改談 5 年後低精度段市場將出現競爭、但毛利較低。

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 6 | 4 |
| customer_second_source | found | 2 | 2 |
| customer_concentration_credit | found | 2 | 2 |
| supply_demand_durability | found | 4 | 2 |
| regulatory_antitrust | found | 1 | 3 |
| reg_tariff_export | none | 0 | 4 |
| geo_supply_chain | found | 2 | 2 |
| end_markets | found | 3 | 3 |
| substitute_technology | found | 4 | 3 |
| channel_business_model_shift | found | 1 | 2 |
| capital_markets_pricing | found | 4 | 4 |
| major_events | found | 1 | 4 |
| cyclical_supply_discipline_capacity | found | 2 | 3 |
| cyclical_inventory_price_position | found | 2 | 2 |
| cyclical_prior_downcycle_behavior | found | 3 | 2 |

未涵蓋／不適用軸的查詢詞原文（供判相關性）：
- **reg_tariff_export**（none）：BESI tariff section 232 2026；BESI export control OR entity list 2026；BE Semiconductor Industries China tariff OR trade restriction 2026；Besi tariff exposure supply chain 2026

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260710","verdict":"觀望","role":"核心","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"混合鍵合成為 HBM4／HBM4e 與先進邏輯封裝的主流鍵合技術，BESI 維持 60%+ 份額","columns":{"2Y 驗證點":"≥2 家記憶體廠 HBM 產線導入混合鍵合量產","5Y 驗證點":"混合鍵合佔先進封裝鍵合 &gt; 30%","10Y 驗證點":"混合鍵合成為 2.5D／3D 標準製程","數字門檻":"混合鍵合份額 ≥ 60%；HBM4/4E 世代開始導入","來源":"公司法說、TrendForce、SemiEngineering","漂移觸發":"連 4 季（5Y 假設）記憶體廠明示 16-high 前不導入 → 削弱"}},{"id":"H2","text":"先進封裝 capex 上行循環延續，BESI 營收 FY2025 €591M → FY2027E €1.3B","columns":{"2Y 驗證點":"季度訂單 YoY 保持正、Q2-26 guide 兌現（+30-40%）","5Y 驗證點":"營收較 2025 谷底翻倍以上、OM 回到 35%+","10Y 驗證點":"穿越 1-2 個 capex 週期仍結構性增長","數字門檻":"FY2027E 營收 €1,309M（共識）；OM &gt; 32%","來源":"yfinance 共識、公司 guidance","漂移觸發":"連 2 季（2Y 假設）訂單 YoY &lt; 0 → 削弱"}},{"id":"H3","text":"高估值（Fwd PE 40x／P/B 43x／EV·EBITDA 96x）由獨佔性支撐、不因循環或競爭崩解","columns":{"2Y 驗證點":"Fwd PE 不跌破 25x（護城河下限）","5Y 驗證點":"ROIC（剔現金）維持 &gt; 25%、GM &gt; 60%","10Y 驗證點":"混合鍵合定價權維持、無有效第二供給","數字門檻":"GM &gt; 60%；混合鍵合份額不流失","來源":"財報、產業份額報告","漂移觸發":"連 4 季 GM &lt; 58% 或份額掉出 60% → 反轉"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"先進封裝 capex 循環見頂／消化（客戶砍單）","columns":{"對應假設":"H2","時間尺度":"⚡ 短期（1-2 季）","監測指標":"季度訂單 YoY、book-to-bill","警戒閾值":"訂單 YoY 連 2 季 &lt; 0"}},{"id":"R2","text":"HBM4／HBM4E 沿用微凸塊／TCB，混合鍵合放量遞延至 HBM5（2028-2029）","columns":{"對應假設":"H1","時間尺度":"🔥 中期（4-6 季）","監測指標":"記憶體廠世代路線公告、Hanmi／K&amp;S TCB 訂單","警戒閾值":"16-high 前明示不導入混合鍵合"}},{"id":"R3","text":"韓廠（Hanmi／Hanwha／LG／SEMES）＋ ASMPT 縮小精度差距、客戶扶植第二供應源侵蝕份額","columns":{"對應假設":"H1／H3","時間尺度":"🐢 長期（2+ 年）","監測指標":"混合鍵合份額、客戶 second-source design win","警戒閾值":"份額掉出 60%"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"價格回落至 Fwd PE FY2027 ~28-32x（約 €180-210）；且／或 HBM4 混合鍵合 design-win 確認（≥2 家記憶體廠量產）化解 7/7 遞延疑慮","irr_base_pct":8.4,"ev5y_pct":43.0,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"核心","signal":"B","val":"🟠","ma":"✅","trap":"🟢","moat_trend":"↑","runway_post_y5":"🟢","asym_ratio":2.7,"ev5y_pct":43.0,"irr_base_pct":8.4,"max_dd_pct":-60.0,"bull_5y_price":578.0,"bear_5y_price":146.0,"p_bull_pct":28.0,"p_bear_pct":32.0,"rearm_trigger":"價格回落至 Fwd PE FY2027 ~28-32x（約 €180-210）；且／或 HBM4 混合鍵合 design-win 確認（≥2 家記憶體廠量產）化解 7/7 遞延疑慮","price_at_dd":251.4,"archetype":"循環/商品","cycle_position":"早循環"}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"BESI","date":"2026-10-25","schema":"v15.2","contract":"v19","company_name":"BE Semiconductor Industries N.V."},"oneliner":"混合鍵合龍頭的訂單與獲利仍在加速，股價半年跌四成，反映對手開始出貨、記憶體導入延後與 ASML 疑慮；兩年後本益比約 20 倍已不貴，但第二供應源風險要等 Q4 訂單與一月策略檢討結論才看得清。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/BESI_20261025/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/BESI_20261025/scenario.json","answers":{"q1_business":{"verdict":"賣後段鍵合設備給晶圓代工、記憶體廠與封測廠，錢卡在先進封裝「晶粒精準放置」這一節點；產業處於 AI 帶動的擴張期，但需求屬週期性，終將反轉。","reasoning":"Q3-26 營收 €283.4M，年增 113.6%、季增 13.4%；毛利率 65.2%，淨利 €107.2M（淨利率 37.8%），營業費用 €55.1M。訂單 €342.6M，訂單對營收約 1.21 倍（342.6÷283.4），近四季訂單 €1.2B（Q3 法說）。成長來源依法說為混合鍵合、光子與資料中心，另有 AI 伺服器電源管理；車用由過去占營收 15–20% 降到約 10%（Q3 法說）。Q3 訂單約四成來自中國（Q3 法說問答）。分部營收與前幾大客戶占比事實表未涵蓋。單點依賴：台積電被產業評論列為最重要客戶，2026 Q1 混合鍵合成長主要來自單一客戶超預期擴產，客戶集中是風險，不是護城河證據。供需持久度：週期性將反轉——管理層自述過往上行週期約 6–8 季後出現產能過剩（2026-07-23 法說），混合鍵合的結構需求只能拉長循環，不能消除循環。產業時鐘判擴張期：TechInsights 把 2026 年封裝設備成長預估上調到 37%，並預期 2027 年延續（Q3 法說轉述），訂單連續數季倍增，尚未見消化。Q4 指引營收持平 ±5%、毛利率 63–65%，管理層解釋為整線交期安排，不是客戶延後。","fact_refs":["f_kpi0_ifrs","f_kpi1_orders","f_kpi2","f_kpi3","f_kpi4","f_kpi5","f_kpi6_q4_26","f_kpi7_hybrid_bonding"],"verdict_values":{"revenue_quality":"以機台一次性銷售為主；訂單能見度由過去 1–1.5 季拉長到 2 季、部分專案更長（Q3 法說）；服務收入未揭露數字","unit_econ_note":"管理層以年產 300 台、平均單價約 €2.5M 概算混合鍵合產出；每升一級放置精度單價上升，未給數字（2026-06-18 投資人日）；供應鏈成本上升已以漲價轉嫁（Q3 法說）","archetype":{"primary":"循環/商品","secondary":"品質複利成長","confidence":"中","fingerprint":"後段設備資本支出循環，內含混合鍵合結構成長曲線"},"industry":{"clock_phase":"II","sd_verdict_source":"週期性將反轉：管理層自述上行週期約 6–8 季後過剩（2026-07-23 法說），本輪訂單倍增已約四季；混合鍵合屬結構需求，但訂單時點受少數客戶擴產左右","bargaining":{"up":"外包供應鏈與營運模式可讓產能年增約 70%，上游成本上升已轉嫁漲價，未見上游議價壓力","down":"客戶集中於台積電與三大記憶體廠，前一兩大客戶占比事實表未涵蓋；單一客戶擴產即可左右單季訂單","geo":"Q3 訂單約四成來自中國；荷蘭國安審查與出口規範是政策變數，管理層正減少機台中的美國零件"},"profit_pool_dir":"利潤池往先進封裝與混合鍵合遷移；BESI 過去四季毛利率 64.25%，高於 KLIC 48.18%、AMAT 49.4%","tam_table":[{"item":"封裝設備市場（TechInsights）","value":"2026 年成長 37%；2028 年達 $12B（Q3 法說轉述）"},{"item":"混合鍵合累計機台需求（公司模型）","value":"低情境 1,150 台、高情境 2,200 台（2026-06-18 投資人日）"},{"item":"已實現累計需求","value":"超過 215 台，客戶 23 家（Q3-26）"},{"item":"滲透率","value":"約 10–19%（215 台對 2,200／1,150 台，分母為公司自估）"},{"item":"主流晶粒貼合可及市場","value":"約 €1.6B，至 2030 年約成長 2 倍（投資人日）"},{"item":"公司長期營收目標","value":"€1.7–2.2B，營業利益率 45–55%（2026-06 上調）"},{"item":"利潤池占比 5 年前→現在","value":"事實表未涵蓋"}]}}},"q2_moat":{"verdict":"護城河方向判穩定：混合鍵合領先與毛利率優勢仍在，但對手已開始出貨、最大客戶可能導入第二供應源，不再能判擴大。","reasoning":"機制：放置精度路線圖領先（已售 215 台皆為 100nm 世代，本季開始出貨 50nm，25nm 開發中，Q3 法說）＋客戶驗證週期長（台積電驗證逾三年，2026-07-23 法說）＋與 Applied Materials 的整合平台。同業報酬率事實表未涵蓋，改用利潤率對照：BESI 過去四季毛利率 64.25%，高於 KLIC 48.18%、Hanmi 57.35%、AMAT 49.4%；營業利益率 36.36% 高於 KLIC 13.21%、AMAT 31.09%，但低於 Hanmi 42.49%（Hanmi 在 HBM 熱壓鍵合約占七成，屬不同機台）。客戶數 15→21→23 家，2026 年混合鍵合訂單已是 2025 全年兩倍以上，2026 年未見對手取得具名量產訂單。反方：ASMPT、Süss、Shibaura 已出貨混合鍵合設備，全球約二十個平台開發中，韓廠四家爭取三星與 SK hynix；管理層在投資人日自承「競爭者會在下一輪切入」「是否擁有最好的鍵合機仍是挑戰」。執行力判擴大（產能可年增約 70%，營業費用占營收由 32% 降到 16.4%），定價力判穩定（毛利率維持 63–65% 指引），合併為穩定。產業態勢：雙向拉鋸——競爭惡化（對手出貨、ASML 傳聞）對上結構轉好（混合鍵合由邏輯擴及 CPO、邊緣 AI 與記憶體），出口規範與荷蘭國安審查是另一項結構變數。投入資本事實表未涵蓋，當期報酬率無法精算。","fact_refs":["f_peer_besi_gross_margin_pct","f_peer_besi_operating_margin_pct","f_peer_besi_fcf_margin_pct","f_peer_klic_gross_margin_pct","f_peer_klic_operating_margin_pct","f_peer_klic_fcf_margin_pct","f_peer_042700_ks_gross_margin_pct","f_peer_042700_ks_operating_margin_pct","f_peer_042700_ks_fcf_margin_pct","f_peer_amat_gross_margin_pct","f_peer_amat_operating_margin_pct","f_peer_amat_fcf_margin_pct","f_kpi7_hybrid_bonding"],"verdict_values":{"moat":{"mechanism":"放置精度路線圖領先＋客戶產線驗證逾三年的轉換成本＋與 Applied Materials 的整合平台","execution":9,"pricing":8,"grade":"B","trend":"→","trend_evidence":"客戶 15→23 家、混合鍵合訂單較 2025 全年翻倍、毛利率守在 63–65%；但 ASMPT、Süss、Shibaura 已出貨，約二十個平台開發中，評論指台積電預期導入第二供應商，管理層自承下一輪精度世代競爭者會切入","competitor_notes":[{"name":"KLIC","strategy_note":"主力在打線與熱壓鍵合，利潤率遠低於 BESI，混合鍵合未見具名量產訂單，目前不構成直接威脅"},{"name":"ASMPT","strategy_note":"熱壓鍵合份額約 35–40%，並已出貨混合鍵合設備，是最可能成為第二供應源的成熟對手；財務數字事實表未涵蓋"},{"name":"042700.KS","strategy_note":"Hanmi 在 HBM 熱壓鍵合約占七成，投資約 1,000 億韓元建混合鍵合工廠，目標 2027 年底前推出，對記憶體客群是最近的威脅"},{"name":"AMAT","strategy_note":"持股約 9%、與 BESI 共推整合平台，現階段是夥伴；若轉為自研或收購對手，關係會反轉"},{"name":"ASML","strategy_note":"BofA 稱其將進入混合鍵合，但 ASML 未公布產品或時程；管理層稱雙方合作研究晶粒應力，ASML 目標是晶片內 3D 電晶體堆疊"}],"threats":[{"level":"🔴","text":"韓廠（SEMES 隸屬三星、Hanmi、Hanwha、LG）與 ASMPT、Süss、Shibaura 推出混合鍵合機，約二十個平台開發中；記憶體客戶有自家體系供應商可扶植，下一輪 50nm／25nm 世代是切入點","p":"35%","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1","customer_second_source#1","substitute_technology#0","substitute_technology#2","substitute_technology#3","geo_supply_chain#1","cyclical_supply_discipline_capacity#1"]},{"level":"🟡","text":"最大邏輯客戶台積電導入第二家混合鍵合供應商（產業評論，未確認）","p":"30%","evidence_refs":["customer_second_source#0"]},{"level":"🟡","text":"ASML 進入晶片對晶圓混合鍵合（賣方報導，ASML 未公布產品或時程）","p":"15%","evidence_refs":["competitive_share_entrants#2","end_markets#2"]}],"roic_durability":{"quadrant":"高利益率×高周轉（營業利益率 36.36%；周轉率事實表未涵蓋，依外包供應鏈、可快速擴產的營運模式推定）","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"使用者是代工與記憶體廠的封裝產線，決策者實為終端 GPU 大廠（管理層：最終客戶會指定要混合鍵合），付款者是代工與記憶體廠，三角色都成立。客戶要解決的是頻寬、功耗與散熱，混合鍵合是目前最佳解法之一；但記憶體缺貨時客戶先用既有製程滿足需求，急迫性不等於持久性，時點可延後。"},{"item":"決策層級","level":"🟡","text":"替代性在客戶單一製程站點衡量：台積電驗證逾三年，換供應商要重新驗證，轉換成本高；但領先客戶已有約 60 台裝機，擴產時引進第二家的成本最低，評論指台積電預期導入第二供應商。"},{"item":"價值鏈分配","level":"🟡","text":"BESI 毛利率 64.25% 高於前段設備商 AMAT 49.4%，在鏈上分到的比例高；但買方集中於少數代工與記憶體廠，議價力強，且 Applied Materials 同時是夥伴與持股約 9% 的股東，整合平台若由 AMAT 主導，價值可能往前段移。"},{"item":"社會容忍度","level":"🟡","text":"企業對企業設備，沒有消費端漲價的政治壓力；但 Q3 訂單約四成來自中國，荷蘭與美國出口規範、荷蘭國安審查是政策上限，管理層已在減少機台中的美國零件。"}],"roiic":"事實表未涵蓋（投入資本、資本支出與折舊未列）；營收由 FY2025 €591M 增至 2026 前三季 €718M，營業費用占營收下降，增量報酬方向偏高但無法量化","reinvest_rate":"低：FY2025 淨利 €131.6M，2026 Q2 支付年度股利 €125.4M，另有每年 €100M 回購，盈餘大部分配回股東；確切比率事實表未涵蓋","endo_ceiling":null,"formula_note":"內生成長＝增量報酬率×再投資率；兩者都缺數字，只能判斷內生上界明顯低於共識 EPS 成長，差額來自循環營運槓桿"}}}},"q3_growth":{"verdict":"跑道寬：混合鍵合累計需求約 215 台，對公司自估 1,150–2,200 台的累計空間，滲透約一至二成，且有 HBM、CPO、邊緣 AI 後續曲線；但分母是公司自估，記憶體導入時點已延後。","reasoning":"成長以量為主（機台數），價為輔（精度升級提高單價、成本轉嫁漲價），無併購，回購規模小。共識 EPS：FY1 4.96、FY2 7.27、FY3 9.31，FY1→FY3 年化約 37%；最近一次快照 FY2、FY3 各下修 0.55%、1.59%，FY1 近三個月不變。內生上界：盈餘多數配回股東，再投資率低，內生成長明顯低於 37%；缺口歸因於利潤率擴張（營業費用占營收由 32% 降到 16.4%，毛利率回到 65%）與循環復甦，可歸因，但會隨循環反轉。跑道：215 台對公司高情境 2,200 台約一成，對低情境 1,150 台約兩成；以 2026 年訂單翻倍的速度推，約 5–9 年到三成滲透。管理層 6 月投資人日說首家 HBM 廠 2027 年在 HBM4E 導入，Q3 法說改口「確切時點我們不知道」並承認採用「有所延後」，SK hynix 據報延到 HBM5，記憶體曲線延後 1–2 年列為基本假設。衰退訊號亮一個：EPS 成長顯著高於營收成長（法說：前三季營收年增 69%、淨利年增 179%），屬循環營運槓桿。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_fy2_pct","f_consensus_rev_fy3_pct","f_consensus_rev_3m_fy1_pct","f_kpi7_hybrid_bonding","f_kpi0_ifrs","f_kpi3"],"verdict_values":{"growth":{"driver_mix":"量為主（機台數），價為輔（精度升級、成本轉嫁漲價）；無併購；回購每年約 €100M","runway_years":"5–9","runway_post_y5":"🟢","endo_ceiling_basis":"再投資率低（2026 Q2 股利 €125.4M 對 FY2025 淨利 €131.6M），內生上界無法精算但明顯低於共識 FY1→FY3 年化約 37%；缺口歸因於循環復甦下的利潤率擴張","segments":{"expanded":false,"reason":"分部營收拆分不在事實表；投資人日只給長期目標拆分（主流業務約 €1.1B、次微米 €0.6–1.1B），無當期數字可展開"},"decay_signals":["毛利率連兩季年減：未亮（Q3 65.2%，指引 63–65%；逐季年比數字事實表未涵蓋）","核心市占近 12 個月縮減：未亮（客戶數 15→23，未見對手具名量產訂單；可靠份額數據不存在）","提價後銷量下滑：未亮（轉嫁漲價同時訂單年增 96%）","EPS 成長高於營收成長逾 5 個百分點：亮（前三季淨利年增 179% 對營收 69%，循環營運槓桿）","自由現金流對淨利連兩年低於 0.75：無法判斷（年度自由現金流事實表未涵蓋）","股權酬勞占營收逾 5% 且上升：無法判斷（事實表未涵蓋）","可及市場萎縮或被替代：未亮但需監測（SK hynix HBM4 16 層保留 MR-MUF）","產業倍數三年系統性下移：無法判斷（同業倍數歷史事實表未涵蓋）","維護性資本支出占自由現金流逾六成：未亮（輕資產外包模式）","停止投資新產能且營收三年內下滑：未亮（越南廠擴產中）"],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"資本配置大致健康但多項無法驗證：淨現金轉正並擴大回購，盈餘多配回股東；三項計分中兩項缺數據。","reasoning":"期末淨現金 €246.6M，較去年同期增加 €254.4M（Q3 法說）；自 2026-10-27 起回購計畫擴大到每年 €100M；2026 Q2 支付年度股利 €125.4M，可轉債已轉股（2026-07-23 法說），股數曾被稀釋。過去四季自由現金流利潤率 23.08%；自由現金流對淨利轉換率、股權酬勞占營收、現金去向四分比例事實表未涵蓋。管理層對併購的說法是「產業併購近乎不存在，以夥伴關係為主」，近年無收購，併購報酬一項不適用。回購買入收益：FY1 本益比 29.25 倍換算盈餘殖利率約 3.4%，FY2 約 5.0%；十年期公債殖利率不在證據包內，無法判斷是否過門檻。營運槓桿：Q3 營收年增 113.6%、淨利年增 323.7%，未見壓縮。","fact_refs":["f_kpi5","f_kpi3","f_peer_besi_fcf_margin_pct","f_fwd_pe_latest","f_dividend_yield_ttm"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":false,"passed":null,"input":"近年無收購，管理層表明以夥伴關係為主"},{"name":"buyback_yield","applicable":true,"passed":null,"input":"FY1 盈餘殖利率約 3.4%、FY2 約 5.0%；十年期殖利率不在證據包"},{"name":"sbc_dilution","applicable":true,"passed":null,"input":"股權酬勞與年度稀釋率事實表未涵蓋；2026 年可轉債轉股曾稀釋"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長不靠併購，近年無收購；現金去向以股利與回購為主，四分拆解數字事實表未涵蓋"}}}},"q5_valuation":{"verdict":"現價要求 2027 年 EPS 約 7.3 兌現、且循環不在 2028 年前明顯反轉；兩年後本益比約 20 倍，我大致相信獲利，但不相信競爭對毛利毫無影響，估值判合理而非便宜。","reasoning":"FY1 本益比 29.25 倍、FY2 約 20 倍（145.1÷7.27）、FY3 約 15.6 倍（145.1÷9.31）。成長調整後本益比：29.25 除以 FY1→FY3 年化 EPS 成長約 37%，約 0.79，落在便宜區；但分子分母都在循環上行段，景氣反轉時 EPS 會像 FY2022 2.9→FY2025 1.66 那樣回落，所以不以此論便宜。五年估值分位：事實表只有近期前瞻本益比，五年區間未涵蓋，無法計算。前份判斷時股價 251.4、FY1 本益比約 40 倍，現在下跌 42%；股價低於 52 週與 104 週均線、高於 250 週均線，RSI 30.4，屬超賣邊緣而非過熱。短期上行：一年後以基本情境 FY2028 EPS 8.3×21 倍約 174，約 +20%；中期三年以 FY2030 EPS 8.8×21 倍約 185，約 +27%。賣方目標價均值約 €297（2026-08，區間 €173–401）已過時且幣別不同，不採用。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_week26_return_pct","f_rsi14","f_ma_state","f_ma_w52","f_ma_w104","f_ma_w250","f_dividend_yield_ttm"],"verdict_values":{"valuation":{"basis":"前瞻本益比（FY1／FY2 共識 EPS）","tier":"高毛利後段設備","peers":{"expanded":false,"reason":"事實表只有同業利潤率，沒有同業本益比，無法做倍數對照"},"fwd_pe":29.25,"peg":0.79,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"FY1 本益比 29.25 倍、FY2 約 20 倍，成長調整後約 0.79；但獲利處於循環上行段，FY2、FY3 共識開始小幅下修，五年分位缺資料，判合理不判便宜","upside_short_pct":20.1,"upside_mid_pct":27.4,"denominator_disputed":false,"denominator_note":"分母為循環上行期的共識 EPS，不含一次性項目；事實表股價與共識 EPS 標示為美元，FY2025 實際 EPS 1.66 幣別未標（推測為歐元），三年成長率改以 FY1→FY3 計算，避免幣別混用"}}},"q6_how_wrong":{"verdict":"最可能看錯在把循環高段獲利當常態，以及低估第二供應源進入的速度；陷阱風險中等。","reasoning":"管理層多次迴避關鍵數字：不揭露混合鍵合出貨與訂單台數、不給 HBM 各客戶驗證時程、對產能過剩只答「沒人知道」、服務收入不給數字、對領先幅度未舉具體例證（2026-06-18 投資人日與 2026-07-23 法說問答）。這些空白正好落在論點最承重的三處：份額、記憶體時點、循環長度。歷史下行：2019 上半年營收年減 44.9%、2023 全年年減 19.9%，但毛利率兩次都守住（55.9%、64.9%），下行時傷的是量而非價。股價過去 26 週已跌 42.1%，部分反映 2026 年 3 月收購傳聞溢價退去與 10 月 BofA 降評。最強空方數字：FY2、FY3 共識 EPS 開始小幅下修，Q4 營收指引持平。訴訟與監管調查：證據包未見。","fact_refs":["f_week26_return_pct","f_rsi14","f_consensus_rev_fy2_pct","f_consensus_rev_fy3_pct","f_kpi6_q4_26"],"verdict_values":{"trap":{"verdict":"🟡","label":"循環獲利放大＋對手開始出貨"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":4.96,"pe":29.25,"basis":"FY1（FY2026E）共識 EPS 4.96，前瞻口徑；終端倍數套用終端年 EPS，事實表無同業本益比可對照，錨定自身 FY1 29 倍與 FY2 20 倍"},"valuation_basis":"eps_pe","eps":{"bull":[7.8,10.5,12.0,14.0,16.0],"base":[6.9,8.3,7.4,8.8,10.2],"bear":[6.0,4.6,3.6,4.6,5.6]},"pe":{"bull":27,"base":21,"bear":15},"p":{"bull":25,"base":43,"bear":32},"yield_pct":{"dividend":1.09,"net_buyback":0.5},"second_stage":{"bull_cagr_pct":14,"base_cagr_pct":9},"max_dd":{"lo":-65,"hi":-45,"basis":"過去 26 週股價已由約 251 跌到 145（−42%），估值修正可在半年內發生；歷史下行期營收曾年減 44.9%（2019 上半年）；Bear 終點跌幅約 −42%，路徑中再疊加循環谷底恐慌，從現價起算回撤區間取 −45%～−65%","trigger_time":null},"basis":{"bull":"HBM4E／HBM5 於 2027–2028 年採混合鍵合、GPU 邏輯 2028 年放量、CPO 擴大，營收逼近長期目標上緣 €2.2B、營業利益率 50–55%，競爭者未取得具名量產訂單","base":"AI 資本支出上行延續到 2028 年、2029 年一次消化，記憶體導入延到 HBM5；份額小幅流失但毛利率守在 60% 以上，2031 年營收接近長期目標中段","bear":"2027 下半年循環見頂、2028–2029 年消化如 2019 與 2023，台積電導入第二供應源、韓廠拿下記憶體客戶，毛利率掉到 55–58%，2031 年 EPS 仍低於目前 FY2 共識"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"2019 上半年營收年減 44.9%、2023 全年年減 19.9%；管理層說上行週期約 6–8 季後過剩，本輪訂單倍增已走約四季；2026 Q1 混合鍵合成長主要來自單一客戶擴產","assumption":"AI 資本支出上行延續到 2028 年","consequence":"若 2027 下半年見頂，疊加台積電雙供應與記憶體延後，EPS 在 2029 年谷底回到約 3.6，終端 5.6 配 15 倍，股價較現價再跌約四成","ruling":"採納：熊市機率維持 32%，以單季訂單與訂單對營收比作為最早警訊；與唯一致命點部分重疊（雙供應），故唯一致命點只看台積電事件，本條看循環","watch":"單季訂單、訂單對營收比、管理層對產能過剩的說法","evidence_refs":["cyclical_prior_downcycle_behavior#0","customer_concentration_credit#1","supply_demand_durability#3"]},{"view":"論點成功但股東經濟變差","evidence":"約二十個平台開發中，ASMPT、Süss、Shibaura 已出貨；管理層自承下一輪精度世代競爭者會切入；Q4 營業費用因策略顧問費增加 5–10%","assumption":"混合鍵合成為主流時 BESI 仍能維持 63–65% 毛利率","consequence":"技術普及但價格競爭使毛利率降到 55% 左右、研發支出上升，營收達標而 EPS 不達標","ruling":"部分採納：2019 與 2023 年下行期毛利率仍守在 55.9% 與 64.9%，定價韌性有歷史支持，但當時沒有混合鍵合對手；基本情境假設毛利率守在 60% 以上，低於 60% 即轉向熊市情境","watch":"季度毛利率、對手具名量產訂單","evidence_refs":["substitute_technology#0","substitute_technology#2","geo_supply_chain#1","customer_second_source#1"]},{"view":"價格已反映太多","evidence":"FY1 本益比仍有 29.25 倍；FY2、FY3 共識 EPS 開始下修 0.55% 與 1.59%；Q4 營收指引持平；BofA 降評並砍半目標價","assumption":"FY2 約 20 倍代表便宜","consequence":"若獲利處於循環高段，前瞻本益比低估真實倍數，股價下跌 42% 也不構成安全邊際","ruling":"部分反駁：股價已從約 40 倍修正到 29 倍，ASML 疑慮已反映在價格；但共識開始下修，故不追價，只在事件確認後建倉","watch":"共識 EPS 修正方向、Q4 訂單","evidence_refs":["end_markets#2","competitive_share_entrants#2"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟠","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟠","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 251.4 → 本次 145.1（-42.3%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=251.4","side_b":"本次 price_at_dd=145.1","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]角色由 dd_decision.py 機械路由：前份 核心 → 本次 追蹤","cause":"新證據","prior_field":["dca_role"],"side_a":"前份 dca_role=核心","side_b":"本次 dca_role=追蹤","ruling":"角色是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。沒有單一輸入能還原，屬多欄共同：估值 🟠→🟡、均線 ✅→🟠、陷阱燈 🟢→🟡、護城河趨勢 ↑→→。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 251.4 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 251.4 美元：Bull 價 578、Bear 價 146，五年期望值 +43.0%，基準年化 8.4%，不對稱比 2.7","side_b":"本次情境、股價仍用 251.4 美元：Bull 價 432、Bear 價 84，五年期望值 −9.7%，基準年化 −3.2%，不對稱比 0.84","ruling":"先換情境、股價不動：五年期望值少 52.7 個百分點，基準年化少 11.6 個百分點。不對稱比由 2.7 變為 0.84。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 251.4 美元：五年期望值 −9.7%，基準年化 −3.2%，不對稱比 0.84","side_b":"本次情境、股價 145.1 美元：五年期望值 +56.4%，基準年化 8.1%，不對稱比 3.67","ruling":"再換股價、情境不動：起點價下跌 42.3%，五年期望值多 66.1 個百分點，基準年化多 11.3 個百分點，不對稱比由 0.84 升到 3.67。合計五年期望值比前份多 13.4 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"ASML 是否進入晶片對晶圓混合鍵合","cause":"新證據","prior_field":null,"side_a":"BofA（2026-10-06）：ASML 進入混合鍵合是股價未反映的威脅，降評至中立並將目標價砍半","side_b":"管理層（2026-10-22 法說）：ASML 不是競爭者，其方向是晶片內 3D 電晶體堆疊，雙方合作研究晶粒應力","ruling":"方向相反，依證據裁決採管理層一側：ASML 未公布產品或時程，BofA 本身也不假設其取得顯著份額；但管理層說法無第三方佐證，保留為風險而非排除","evidence_level":"賣方報導與管理層說法，皆無產品證據","settle_metric":"ASML 是否公布晶片對晶圓鍵合產品或客戶評估","if_then":["若 ASML 在 2027 年內公布晶片對晶圓混合鍵合機台並有客戶評估，停止加碼，已持有者減碼一半","若 ASML 2027 年投資人日仍只談晶圓對晶圓與晶片內堆疊，移除此風險權重，牛市機率回到 28%"],"evidence_refs":["competitive_share_entrants#2","end_markets#2"]},{"axis":"記憶體導入混合鍵合的時點","cause":"新證據","prior_field":null,"side_a":"2026-06-18 投資人日，Peter Wiedner：第一家 HBM 廠將在 2027 年的 HBM4E 導入混合鍵合","side_b":"2026-10-22 法說，Richard Blickman：確切時點我們不知道，採用較優技術「有所延後」；另有報導稱 SK hynix 延到 HBM5","ruling":"程度差異，可調和：方向未變（Q3 有記憶體客戶同時下混合鍵合與 TC Next 訂單），時點延後；前份風險門檻「16 層前明示不導入」已對 SK hynix 一家觸發，牛市機率因此由 28% 降到 25%","evidence_level":"管理層前後說法＋產業報導","settle_metric":"2027 年記憶體廠量產導入公告","if_then":["若 2027 年中前有記憶體廠宣布 HBM4E 量產採混合鍵合，牛市機率回到 30%","若 2027 年底前無一公告，停止加碼並把記憶體曲線移出基本情境"],"evidence_refs":["supply_demand_durability#3"]},{"axis":"訂單強勁與 Q4 營收持平","cause":"新證據","prior_field":null,"side_a":"Q3 訂單 €342.6M、年增 96%，管理層稱動能延續到 Q4","side_b":"Q4 營收指引持平 ±5%，有分析師解讀為客戶延後","ruling":"程度差異，可調和：管理層說明為整線交期安排，部分 Q3 訂單排到 2027 上半年出貨，訂單對營收約 1.21 倍支持此說；以 Q1-27 營收指引驗證","evidence_level":"公司指引與法說問答","settle_metric":"Q1-27 營收指引是否季增","if_then":["若 Q1-27 營收指引季增，交期說法成立","若 Q1-27 再持平或下滑且單季訂單低於 €280M，視為消化開始，檢查減碼條件"],"evidence_refs":[]},{"axis":"現在就買的最強論證","cause":null,"prior_field":null,"side_a":"FY2 本益比約 20 倍、淨現金 €246.6M、訂單年增 96%、客戶 23 家；股價下跌主要來自 ASML 傳聞與收購溢價退去，不是基本面","side_b":"關鍵約束是第二供應源與記憶體時點，兩者在 Q4 財報與一月策略檢討前沒有新證據；共識 FY2、FY3 已開始小幅下修","ruling":"觀望：約束是護城河能否扛住第二供應源，不是價格；事件確認前不追","evidence_level":"財報數字＋產業報導","settle_metric":"Q4-26 單季訂單與對手具名量產訂單","if_then":["若股價續跌而 Q4 訂單≥€280M、毛利率≥62%，分批反買首倉，不停損","若股價先漲回 52 週均線上方而事件未確認，不追"],"evidence_refs":[]},{"axis":"估值、機率、回撤區間與整體結論","cause":"價格變動","prior_field":["val","signal","p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份（2026-07-10）：股價 251.4、FY1 本益比約 40 倍、估值偏貴；牛 28%／熊 32%；最大回撤 −60%；前份兩年驗證點「前瞻本益比不跌破 25 倍」","side_b":"本次：股價 145.1、FY1 29.25 倍、FY2 約 20 倍，估值合理；牛 25%／基本 43%／熊 32%；回撤區間 −45%～−65%；FY2 本益比已跌破 25 倍，市場不再為獨佔性付溢價","ruling":"估值由偏貴轉合理全由股價下跌造成，FY1 共識近三個月不變；品質與估值的綜合評級維持不變；牛市機率下調的原因另見記憶體時點一條；回撤改為區間表達，結論與倉位依新估值重算","evidence_level":"價格與共識快照","settle_metric":"股價與共識 EPS","if_then":[],"evidence_refs":[]},{"axis":"護城河方向、陷阱風險與循環位置","cause":"新證據","prior_field":["moat_trend","trap","cycle_position"],"side_a":"前份：護城河方向擴大、陷阱風險低、循環位置早循環","side_b":"本次：護城河方向穩定、陷阱風險中等、循環位置中循環","ruling":"護城河：ASMPT、Süss、Shibaura 已出貨、約二十平台開發、評論指台積電可能導入第二家（2026-06／07 報導），管理層自承下一輪世代競爭會切入，無法再判擴大；陷阱：EPS 成長高於營收成長的衰退訊號亮起，加上對手出貨；循環：訂單倍增已約四季，管理層自述上行週期 6–8 季，TechInsights 預期延續至 2027 年，判中循環，循環視角姿態為持有不加","evidence_level":"產業報導＋公司財報＋管理層說法","settle_metric":"對手具名量產訂單；單季訂單","if_then":["若 2027 上半年單季訂單仍≥€280M 且無對手量產訂單，護城河方向維持穩定","若對手取得具名量產訂單，護城河方向改判縮減並重跑情境"],"evidence_refs":["customer_second_source#0","substitute_technology#0","substitute_technology#2"]},{"axis":"五年後跑道與公司類型","cause":"新證據","prior_field":["runway_post_y5","archetype"],"side_a":"前份：五年後跑道寬，類型為循環／商品","side_b":"本次：維持跑道寬，類型維持循環／商品（次類型品質複利成長）","ruling":"客戶數 15→23、累計需求逾 215 台，對公司自估 1,150–2,200 台仍屬低滲透，CPO 與邊緣 AI 是新增曲線，維持寬；記憶體延後只動時點，不動空間","evidence_level":"公司揭露","settle_metric":"累計需求台數與客戶數","if_then":[],"evidence_refs":[]},{"axis":"重新進場條件","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"價格回落至 Fwd PE FY2027 ~28-32x（約 €180-210）；且／或 HBM4 混合鍵合 design-win 確認（≥2 家記憶體廠量產）化解 7/7 遞延疑慮","side_b":"Q4-26 單季訂單≥€280M，且主要客戶未公開向對手下混合鍵合量產訂單；兩者成立才重跑判斷建首倉","ruling":"價格條件已失效：FY2 本益比約 20 倍，低於前份 28–32 倍區間，價格不再是約束；關鍵約束改為第二供應源與訂單延續，進場首倉改綁事件、不設進場價；條件反向（訂單連兩季 <€230M）則轉為減碼","evidence_level":"價格與財報","settle_metric":"Q4-26 訂單與對手量產訂單","if_then":["條件成立：重跑判斷，通過則分批建首倉","訂單連兩季 <€230M：減碼一半"],"evidence_refs":[]},{"axis":"清倉／減碼指標與風險門檻","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未設清倉／減碼指標；風險門檻用「混合鍵合份額掉出 60%」與「訂單年增率連 2 季 <0」","side_b":"本次設四項：訂單連 2 季 <€230M 減碼一半、毛利率連 2 季 <60% 減碼、主要客戶公開向對手下量產訂單減碼一半、FY2 共識 <6.5 停止加碼；份額門檻改為具名訂單事件","ruling":"份額數據各來源互相矛盾（75%、42%、49% 並存），不能當可觀察門檻，改用具名訂單事件；訂單門檻由年增率改為絕對金額，因基期翻倍後年增率會機械轉負","evidence_level":"方法調整","settle_metric":"季報訂單、毛利率、共識快照","if_then":[],"evidence_refs":["competitive_share_entrants#5"]},{"axis":"唯一致命點","cause":"新證據","prior_field":["single_thing"],"side_a":"前份唯一致命點未設定（null）","side_b":"Single Thing：台積電公開把混合鍵合量產訂單分給第二家供應商","ruling":"Single Thing 新設：2026 年 6 月評論指台積電預期導入第二家，加上多家對手已出貨，最大客戶雙供應是對份額與毛利影響最大的單一事件","evidence_level":"產業評論，未確認","settle_metric":"主要客戶具名第二供應源訂單","if_then":["發生則減碼至半倉，未持有者不建倉"],"evidence_refs":["customer_second_source#0"]}],"triggers":[{"n":1,"text":"Q4-26 財報檢查訂單是否延續","type":"假設驗證","maps_to":"H2","metric":"單季訂單（€M）","threshold":"≥€280M 為確認；<€230M 為警訊","action":"確認且無對手量產訂單：重跑判斷建首倉；警訊：延長觀望","source_freq":"公司季報，每季","date":"2027-02","evidence_refs":[]},{"n":2,"text":"台積電公開把混合鍵合量產訂單分給第二家","type":"Single Thing","maps_to":"Single Thing","metric":"主要客戶具名第二供應源訂單","threshold":"任一公開確認","action":"減碼至半倉；未持有則不建倉","source_freq":"產業報導與公司揭露，持續","date":null,"evidence_refs":["customer_second_source#0"]},{"n":3,"text":"記憶體廠混合鍵合量產世代公告","type":"風險","maps_to":"R2","metric":"三大記憶體廠量產導入公告","threshold":"2027-12 前無一公告","action":"停止加碼，牛市機率降到 15%","source_freq":"記憶體廠法說，每季","date":"2027-12","evidence_refs":["supply_demand_durability#3"]},{"n":4,"text":"循環消化","type":"減碼","maps_to":"R1","metric":"單季訂單與訂單對營收比","threshold":"訂單連 2 季 <€230M 或比值連 2 季 <0.9","action":"減碼一半","source_freq":"公司季報，每季","date":null,"evidence_refs":["cyclical_prior_downcycle_behavior#0","customer_concentration_credit#1"]},{"n":5,"text":"對手取得具名量產訂單，或 ASML 公布晶片對晶圓鍵合產品","type":"風險","maps_to":"R3","metric":"對手具名混合鍵合量產訂單／ASML 產品公告","threshold":"任一出現","action":"停止加碼並重跑護城河評估","source_freq":"TrendForce、Bits&Chips、ASML 投資人日，持續","date":null,"evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1","competitive_share_entrants#2","substitute_technology#0","cyclical_supply_discipline_capacity#1"]},{"n":6,"text":"一月策略檢討結論","type":"複審日期","maps_to":"H1","metric":"管理層公布的混合鍵合、TC Next 與回焊路線及 3–5 年需求","threshold":"長期目標或混合鍵合需求情境下修","action":"下修則維持觀望並重估牛市機率；維持或上修則與 Q4 財報一併複審","source_freq":"公司公告，一次","date":"2027-01","evidence_refs":[]},{"n":7,"text":"出口規範收緊","type":"風險","maps_to":"R4","metric":"對中出口限制、中國訂單占比","threshold":"新增鍵合設備對中限制，或中國訂單占比單季腰斬","action":"減碼三分之一並重跑情境","source_freq":"荷蘭與美國政府公告，持續","date":null,"evidence_refs":["geo_supply_chain#0"]},{"n":8,"text":"重新評估進場","type":"估值rearm","maps_to":"H1","metric":"Q4 訂單與第二供應源事件","threshold":"單季訂單≥€280M 且無對手具名量產訂單","action":"重跑判斷，通過則分批建首倉","source_freq":"每季","date":"2027-02","evidence_refs":[]}],"kill_metrics":[{"metric":"單季訂單（€M）","bear_threshold":"連 2 季 <€230M（減碼一半）","window":"2027-Q1～2027-Q4","source":"公司季報新聞稿","last_status":"ok"},{"metric":"季度毛利率","bear_threshold":"連 2 季 <60%（減碼）","window":"2026-Q4～2027-Q4","source":"公司季報新聞稿","last_status":"ok"},{"metric":"主要邏輯或記憶體客戶向對手下混合鍵合量產訂單","bear_threshold":"任一公開確認（減碼一半）","window":"未來 24 個月","source":"公司揭露、TrendForce、Bits&Chips","last_status":"warning"},{"metric":"FY2 共識 EPS","bear_threshold":"低於 6.5（停止加碼）","window":"未來 6 個月","source":"Koyfin 共識快照","last_status":"ok"}],"evidence_dismissed":[],"action_conditions":{"rearm_trigger":"Q4-26 單季訂單≥€280M，且主要客戶未公開向對手下混合鍵合量產訂單；兩者成立才重跑判斷建首倉","exec_line":"條件成立後分兩批：首批在 Q4 財報後，次批待一月策略檢討未下修長期目標；若股價先跌而訂單與毛利率未惡化，分批反買、不停損；股價先漲而事件未到，不追"}},"decision_inputs":{"signal":"B","ma":"🟠","cycle_position":"中循環","cycle_verdict":"未觸發","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場把 ASML 進入與記憶體延後當成護城河崩解來定價，但 ASML 未公布晶片對晶圓產品、管理層稱雙方合作研究晶粒應力，Q3 訂單年增 96%、客戶增至 23 家；部分跌幅是 3 月收購傳聞溢價退去，不是基本面惡化","momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"等 2027 年 2 月 Q4-26 財報：單季訂單≥€280M，且主要客戶未公開向對手下混合鍵合量產訂單；2027 年 1 月策略檢討結論同時參考","asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null},"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8w(原9b)","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟠'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟢'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場把 ASML 進入與記憶體延後當成護城河崩解來定價，但 ASML 未公布晶片對晶圓產品、管理層稱雙方合作研究晶粒應力，Q3 訂單年增 96%、客戶增至 23 家；部分跌幅是 3 月收購傳聞溢價退去，不是基本面惡化"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":true,"basis":"capalloc_grade='C'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟢', val='🟡', moat_trend='→', week26=-42.1, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='循環/商品', cycle_position='中循環', moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":false,"basis":"signal='B', val='🟡'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":false,"basis":"signal='B', val='🟡', ma='🟠'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":true,"basis":"signal='B', val='🟡', ma='🟠'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟡', ma='🟠'"},{"row":"8w","condition":"判斷者宣告 wait_for_price（價格合理但要等）→ 原 row9b 進場改觀望（等價格）","hit":true,"basis":"wait_for_price=True, 等待條件='等 2027 年 2 月 Q4-26 財報：單季訂單≥€280M，且主要客戶未公開向對手下混合鍵合量產訂單；2027 年 1 月策略檢討結論同時參考'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":"中期 2-5 年","requires_critic":[]},"thesis":{"H":[{"id":"H1","text":"混合鍵合由邏輯擴散到 CPO 與邊緣 AI，BESI 維持首選供應商地位，客戶數與累計需求持續成長","2y":"2027 年底公司揭露累計需求≥350 台、客戶≥28 家","5y":"累計需求達公司低情境 1,150 台的一半以上","10y":"混合鍵合成為 3D 堆疊標準製程，BESI 仍為最大供應商","threshold":"累計需求每季增量≥20 台；主要客戶未公開向對手下量產訂單","source":"公司季報新聞稿與法說；TrendForce、Bits&Chips 的競爭報導","drift_rule":"5 年論點：連 4 季累計需求增量低於 20 台為削弱，連 6 季為反轉；任一主要客戶公開向對手下量產訂單即削弱"},{"id":"H2","text":"AI 帶動的先進封裝資本支出上行延續到 2027 年，訂單維持高檔、毛利率守住長期區間","2y":"2027 年各季訂單≥€250M、毛利率≥62%","5y":"跨過一次消化期後，2031 年 EPS 高於 2027 年","10y":null,"threshold":"單季訂單≥€250M；毛利率≥62%；FY2 共識 EPS≥6.5","source":"公司季報新聞稿與法說；Koyfin 共識快照","drift_rule":"2 年論點：連 2 季訂單低於門檻 5% 以上為削弱，連 3 季低於 10% 以上為反轉"},{"id":"H3","text":"記憶體廠在 HBM4E 或 HBM5 世代（2027–2029 年）至少一家量產導入混合鍵合，且使用 BESI 機台","2y":"2027 年底前至少一家記憶體廠公布量產導入世代","5y":"三大記憶體廠中至少兩家量產採用","10y":null,"threshold":"2027-12 前有一家量產宣布","source":"記憶體廠法說與技術發表、BESI 法說、TrendForce","drift_rule":"5 年論點：連 4 季無新的記憶體混合鍵合訂單為削弱，連 6 季為反轉"}],"R":[{"id":"R1","text":"循環見頂與訂單消化：擴產集中在少數客戶，單一客戶延後即可讓單季訂單驟降，歷史下行期營收曾年減約 45%","h_ref":"H2","clock":"⚡","threshold":"單季訂單連 2 季低於 €230M，或訂單對營收比連 2 季低於 0.9","evidence_refs":["cyclical_prior_downcycle_behavior#0","customer_concentration_credit#1"]},{"id":"R2","text":"記憶體延後：SK hynix 據報把混合鍵合延到 HBM5，記憶體缺貨讓客戶沿用既有製程，HBM 曲線延後 1–2 年以上","h_ref":"H3","clock":"🔥","threshold":"2027 年底前三大記憶體廠無一公布量產導入世代","evidence_refs":["supply_demand_durability#3"]},{"id":"R3","text":"第二供應源侵蝕：ASMPT、Süss、Shibaura 已出貨，韓廠四家與約二十個平台追趕，台積電可能導入第二家，另有 ASML 進入傳聞","h_ref":"H1","clock":"🐢","threshold":"任一主要邏輯或記憶體客戶公開向對手下混合鍵合量產訂單","evidence_refs":["competitive_share_entrants#0","competitive_share_entrants#1","competitive_share_entrants#2","customer_second_source#0","customer_second_source#1","substitute_technology#0","substitute_technology#2","substitute_technology#3","geo_supply_chain#1","cyclical_supply_discipline_capacity#1","end_markets#2"]},{"id":"R4","text":"地緣與出口規範：Q3 訂單約四成來自中國，出口規則、客戶集中與匯率會影響利潤的可預測性","h_ref":"H2","clock":"🔥","threshold":"荷蘭或美國對鍵合設備新增對中出口限制，或中國訂單占比單季腰斬","evidence_refs":["geo_supply_chain#0"]}],"single_thing":{"description":"台積電公開把混合鍵合量產訂單分給第二家供應商","why_fatal":"台積電是最重要客戶，混合鍵合是成長與高毛利的來源；最大客戶一旦雙供應，份額與定價同時被壓，牛市情境失效，基本情境的毛利率假設要下修","if_happens":"持有者減碼至半倉，未持有者不建倉；重跑情境，熊市機率提高到 40% 以上","how_monitor":"季報客戶揭露、對手訂單公告、TrendForce 與 Bits&Chips 產業報導，每季檢查","probability":"約 30%（12–24 個月；目前僅為評論，未見確認報導）"}},"appendix_a":{"growth_durability":7,"quality_score":8,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":19.96,"peg_fy2":0.54,"stress":{"pass":3,"total":5}},"eps_meta":{"base_eps_path":{"FY2025A":1.66,"FY2026E":4.96,"FY2027E":7.27,"FY2028E":9.31},"fy_end_month":12,"eps_basis":"共識 EPS 取自 Koyfin 快照（事實表標示美元）；FY2025A 1.66 取自年度財報稀釋 EPS，幣別未標示（推測為歐元），以此為基期的三年成長率會被幣別差異高估，判斷改以 FY1→FY3 年化約 37% 為準"},"catalysts":[{"date":"2027-01","date_precision":"month","type":"guidance","event":"策略檢討結論（16 週客戶路線圖深度訪談，涵蓋混合鍵合、TC Next 與回焊的 3–5 年需求）","impact":"中","watch":"長期目標與混合鍵合需求情境是否變動"},{"date":"2027-02","date_precision":"month","type":"guidance","event":"Q4-26 財報與 Q1-27 指引","impact":"高","watch":"單季訂單是否≥€280M、Q1 營收指引是否季增"},{"date":"2026-Q4","date_precision":"quarter","type":"product","event":"50nm 第二代混合鍵合機開始出貨","impact":"中","watch":"客戶驗證進度與重複訂單"},{"date":"2027-Q2","date_precision":"quarter","type":"product","event":"記憶體廠 HBM4E 世代鍵合技術選擇","impact":"高","watch":"是否宣布量產採混合鍵合"},{"date":"2027-Q3","date_precision":"quarter","type":"capacity","event":"美國邏輯客戶亞洲擴產與領先代工 AP7 擴產","impact":"中","watch":"新一輪混合鍵合訂單"}]}
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
