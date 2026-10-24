你是 DD 管線 v20 的判斷層閘（gate），標的 URI（20261024）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（26 條）
- `f_kpi0_gaap`（q1_business）｜總營收（GAAP）＝4893 USD m｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-21）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 8-K Ex.99.1 https://www.sec.gov/Archives/edgar/data/0001067701/000106770126000036/uri-9302026xex991.htm（numbers.latest_quarter_kpis.items[0]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-21））
  - 註記：未查證
- `f_kpi2_gaap`（q1_business）｜GAAP 營業利益／利益率＝1409 USD m（利益率 28.8%，自算）｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-21）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 8-K Ex.99.1 同上（numbers.latest_quarter_kpis.items[2]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-21））
  - 註記：未查證
- `f_kpi1_ebitda_non_gaap_non_gaap`（q1_business）｜調整後 EBITDA（公司揭露的 non-GAAP 獲利指標；新聞稿未揭露 non-GAAP 營業利益）＝2331 USD m（利益率 47.6%）｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-21）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 8-K Ex.99.1 同上（numbers.latest_quarter_kpis.items[1]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-21））
  - 註記：未查證
- `f_kpi6_fleet_productivity`（q1_business）｜車隊生產力（fleet productivity）＝6.5 % YoY｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-21）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 8-K Ex.99.1 同上（numbers.latest_quarter_kpis.items[6]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-21））
  - 註記：未查證
- `f_kpi7`（q1_business）｜二手設備銷售收入＝348 USD m（YoY +4.5%；GAAP 毛利率 44.8%，調整後 46.3%；OEC 回收率 51.4%）｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-21）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 8-K Ex.99.1 同上（numbers.latest_quarter_kpis.items[7]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-21））
  - 註記：未查證
- `f_kpi5_2026`（q1_business）｜全年 2026 指引（上調）＝營收 18.0–18.2B；調整後 EBITDA 8.3–8.4B；gross rental capex 5.2–5.5B；營運現金流 6.25–6.85B；FCF（不含重組付款）2.15–2.45B USD｜期間與口徑：Q3 FY2026（公告於 2026-10-21）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司新聞稿 8-K Ex.99.1 同上（numbers.latest_quarter_kpis.items[5]，as_of Q3 FY2026（公告於 2026-10-21））
  - 註記：未查證
- `f_peer_uri_gross_margin_pct`（q2_moat）｜URI 毛利率＝38.36 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.URI.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_uri_operating_margin_pct`（q2_moat）｜URI 營業利益率＝25.1 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.URI.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_hri_operating_margin_pct`（q2_moat）｜HRI 營業利益率＝13.14 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.HRI.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_wsc_operating_margin_pct`（q2_moat）｜WSC 營業利益率＝20.41 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.WSC.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_cat_operating_margin_pct`（q2_moat）｜CAT 營業利益率＝17.52 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CAT.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
- `f_peer_uri_fcf_margin_pct`（q2_moat）｜URI FCF 利潤率＝3.75 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.URI.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_hri_fcf_margin_pct`（q2_moat）｜HRI FCF 利潤率＝-2.64 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.HRI.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_wsc_fcf_margin_pct`（q2_moat）｜WSC FCF 利潤率＝12.98 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.WSC.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝51.84 USD/share｜期間與口徑：2026-10-24／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261024.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-10-24）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝60.91 USD/share｜期間與口徑：2026-10-24／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261024.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-10-24）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝69.22 USD/share｜期間與口徑：2026-10-24／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261024.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-10-24）
- `f_consensus_rev_fy3_pct`（q5_valuation）｜FY3 共識修正＝5.81 %｜期間與口徑：2026-10-24／兩份 Koyfin 快照之間的 EPS 修正幅度（65.42 → 69.22）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261024.xlsx（numbers.consensus_revision.fy3.revision_pct，as_of 2026-10-24）
- `f_kpi3_fcf`（q4_capital）｜自由現金流（FCF）＝272 USD m｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-21）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 8-K Ex.99.1 同上（numbers.latest_quarter_kpis.items[3]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-21））
  - 註記：未查證
- `f_kpi4_sbc_stock_compensation_e`（q4_capital）｜SBC（stock compensation expense, net）占 GAAP 營業利益＝3.05 %（SBC 43 ÷ 營業利益 1,409，自算；占營收 0.88%）｜期間與口徑：Q3 FY2026（季末 2026-09-30，公告於 2026-10-21）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 8-K Ex.99.1 同上（numbers.latest_quarter_kpis.items[4]，as_of Q3 FY2026（季末 2026-09-30，公告於 2026-10-21））
  - 註記：不適用
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝21.2 x｜期間與口徑：2026-10-24／分母＝FY1 EPS 51.84，分子＝快照價 1098.88｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-10-24）
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝1098.88 USD｜期間與口徑：2026-10-23（RTH 收盤，日線 fallback）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-10-23（RTH 收盤，日線 fallback））
- `f_consensus_rev_fy1_pct`（q5_valuation）｜FY1 共識修正＝3.54 %｜期間與口徑：2026-10-24／兩份 Koyfin 快照之間的 EPS 修正幅度（50.07 → 51.84）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261024.xlsx（numbers.consensus_revision.fy1.revision_pct，as_of 2026-10-24）
- `f_consensus_rev_fy2_pct`（q5_valuation）｜FY2 共識修正＝4.66 %｜期間與口徑：2026-10-24／兩份 Koyfin 快照之間的 EPS 修正幅度（58.2 → 60.91）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261024.xlsx（numbers.consensus_revision.fy2.revision_pct，as_of 2026-10-24）
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝0.701 %｜期間與口徑：2026-10-24／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-10-24）
- `f_rsi14`（q5_valuation）｜RSI(14)＝60.2｜期間與口徑：2026-10-23（RTH 收盤，日線 fallback）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-10-23（RTH 收盤，日線 fallback））

### findings_digest 中方向為負或來源衝突的條目（8 條）
- `competitive_share_entrants#1`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K 描述產業高度分散、競爭者含小型獨立業者、區域業者、全國性公司及設備廠商／經銷商；URI 自述相對市占小可能不利於抑制租金價格壓力。
  - 來源：SEC EDGAR 10-K FY2025 Item 1（as_of 2026-01-28）｜affects：moat_trend、decision_inputs.bear
- `competitive_share_entrants#2`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K 風險因子承認過去競爭壓力曾造成市占或價格下降，未來可能再發生，並可能遇到新競爭者。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-01-28）｜affects：moat_trend、thesis.R
- `regulatory_antitrust#0`（regulatory_antitrust｜方向 -｜狀態 ok）：URI 與同業被控透過 RB Global 子公司 Rouse Services 共享定價資料而共謀操縱價格的私人集體訴訟；URI 稱指控毫無根據並將積極抗辯（非政府調查）
  - 來源：Equipment Finance News｜RB Global, United Rentals call antitrust claims meritless（as_of 2025-04-03）｜affects：decision_inputs.bear、triggers
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：FY2025 10-K 風險因子：新設備成本（含原物料關稅）上升可能影響租賃車隊成本與財務結果；關稅列為可能推高成本的因素之一
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2026-01-28）｜affects：decision_inputs.bear、thesis.R
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：10-K 風險因素（FY2020–FY2023 版本相同）：集中採購使公司依賴一組關鍵供應商並承受其信用風險；供應商財務困難可能無法履約或要求重談條款。未點名單一製造商。
  - 來源：United Rentals Form 10-K FY2023 (SEC)（as_of 2024-02-01）｜affects：thesis.R、decision_inputs.bear
- `end_markets#5`（end_markets｜方向 -｜狀態 ok）：S&P Global 稱 CIE 板塊因營建市場停滯而處於停滯，一般工具板塊持續前進
  - 來源：RER 報導 ARA 預測（as_of 2026-05-01）｜affects：thesis.R
- `end_markets#7`（end_markets｜方向 -｜狀態 ok）：2025 年聯邦反托拉斯集體訴訟指 Sunbelt、URI、Herc 等藉 Rouse 租價基準資料協同定價，案件未決
  - 來源：Sunbelt profile 摘要（as_of 2026-09-01）｜affects：thesis.R、decision_inputs.bear
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：URI 10-K 風險因子載明：客戶需求變化可能使部分現有設備過時，須以更高成本購置新設備（FY2023 10-K 文字；搜尋未找到具名替代技術取代租賃的來源）
  - 來源：SEC EDGAR, United Rentals 10-K FY2023, Risk Factors（as_of 2024-02-01）｜affects：thesis.R、decision_inputs.bear

### 事實表自陳的缺口（1 條）
- q6_how_wrong：digest.qa_flags 有 5 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/URI_20261024/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":1940.0,"bear_5y_price":600.0,"p_bull_pct":20,"p_bear_pct":30,"upside_5y_pct":12.1,"ev5y_pct":7.7,"irr_base_pct":2.3,"asym_ratio":1.1,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":51.84,"pe":21.2,"basis":"FY2026 共識調整後 EPS 51.84，與終端倍數同為前瞻一年口徑"},"eps":{"bull":[63.5,72.5,81.0,89.0,97.0],"base":[60.0,66.0,70.0,73.5,77.0],"bear":[56.0,48.0,42.0,46.0,50.0]},"pe":{"bull":20,"base":16,"bear":12},"p":{"bull":20,"base":50,"bear":30},"yield_pct":{"dividend":0.701,"net_buyback":1.9},"second_stage":{"bull_cagr_pct":8,"base_cagr_pct":5},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### URI_Q2_2026_Earnings_Call_20260723.md
- 2026-07-23｜CFO｜guidance：CFO 公布全年營收財測上調 5 億美元至 175–178 億（原話："range of $17.5 billion to $17.8 billion"）
- 2026-07-23｜CFO｜guidance：CFO 說明調整後 EBITDA 財測上調 3 億並維持全年利潤率持平（原話："expectation to bring the revenue growth to the bottom"）
- 2026-07-23｜CFO｜guidance：總租賃 CapEx 財測上調 4.5 億，因需求更強（原話："we've increased our gross CapEx guidance by $450 million"）
- 2026-07-23｜CFO｜guidance：自由現金流財測維持 21.5–24.5 億，CapEx 增加由營運現金流增加抵銷（原話："we are reaffirming another year of strong free cash flow"）
- 2026-07-23｜CEO｜guidance：CEO 表示不給 2027 財測，但認為順風延續到明年（原話："We're not going to go as far as give '27 guidance"）
- 2026-07-23｜CEO｜guidance：CEO 說明 CapEx 季節節奏：新財測下 Q3 約引進 30–35%（原話："somewhere around 30% to 35% in Q3 -- balance in Q4,"）
- 2026-07-23｜CFO｜guidance：CFO 對下半年租賃營收成長不給落點，提醒看區間，主要變數為附屬與轉租，下次 10 月更新（原話："we would point people towards the range,"）
- 2026-07-23｜CEO｜guidance：CEO 說四月已有信心但通常不在四月上調，實際表現超出預期、專案管線更快更深（原話："The pipeline of projects moved faster and got deeper."）
- 2026-07-23｜CFO｜margin：CFO 拆解利潤率：報表口徑 +70bp，扣除出售鷹架業務利得後 -40bp（原話："Excluding both the gain on the sale of our scaffolding"）
- 2026-07-23｜CFO｜margin：CFO 再扣除附屬與轉租超額成長後，核心利潤率年增 40bp（原話："margins were up 40 basis points year-on-year, even"）
- 2026-07-23｜CFO｜margin：CFO 說附屬收入的燃料與運送成本轉嫁帶來營收但增量利潤有限（原話："brought limited incremental margin dollars."）
- 2026-07-23｜CFO｜margin：CFO 量化第二季自用燃料成本對利潤率的額外逆風（原話："20 or 30 basis points of additional headwind year-on-year"）
- 2026-07-23｜CFO｜margin：CFO 說明全年利潤率目標為持平（排除去年 H&E 影響）（原話："flat margins, excluding the impact of H&E last year."）
- 2026-07-23｜CFO｜margin：CFO 以去年對照量化運送成本：去年交貨成本增 20% 對租賃營收 6–7%，隱含約 1.15 億超額成本；今年 Q2 租賃營收 +12.7%、交貨 +11.7%（原話："rental revenue up 12.7%, delivery up 11.7%."）
- 2026-07-23｜CFO｜margin：CFO 說勞力、運送、維修三大核心成本今年皆領先預期曲線（原話："we're actually ahead of the curve on all 3."）
- 2026-07-23｜CFO｜margin：CFO 說第二季重組節省約 1,200 萬，已達年化速率；累計費用 5,100 萬，全年預期 5,500–6,500 萬（原話："benefit was on the order of about $12 million"）
- 2026-07-23｜CFO｜margin：CFO 稱附屬收入難以預測，Q3 燃料價格預期與 Q2 持平（原話："Our expectation is that fuel prices probably"）
- 2026-07-23｜CEO｜margin：CEO 說成本改善來自流程改變與執行，而非 CapEx 緩解重新調配成本（原話："is really more process change and execution"）
- 2026-07-23｜CEO｜customer：CEO 開場稱成長加速、客戶對大型專案保持樂觀（原話："Customers remain optimistic"）
- 2026-07-23｜CEO｜customer：CEO 說在地市場自一月以來已穩定，本地客戶約低個位數成長（原話："we are seeing stabilization with some very modest growth."）
- 2026-07-23｜CEO｜customer：CEO 確認半導體與電力（含資料中心）第二季雙雙加速（原話："Both of those have accelerated here in the second quarter."）
- 2026-07-23｜CEO｜customer：CEO 說電力垂直市場占營收逾一成（原話："in excess of 10% of our business"）
- 2026-07-23｜CEO｜customer：CEO 說石化與工業製造目前並未轉強，屬尚未啟動的上行空間；下游業者推遲歲修（原話："Industrial manufacturing is not really hot right now."）
- 2026-07-23｜CEO｜customer：CEO 說需求超預期主因是大型專案管線，涵蓋面廣（原話："projects across the board are just stronger and deeper"）
- 2026-07-23｜CEO｜product：專長業務租賃營收年增 25%，含 11 個新開據點（原話："exceptional rental revenue growth of 25% year-over-year"）
- 2026-07-23｜CFO｜product：CFO 說專長業務七大線皆雙位數成長，行動模組/儲存與 ROS 成長最快但規模最小（原話："I'll tell you, they're all in the double digits."）
- 2026-07-23｜CEO｜product：CEO 說電力產品十年來有機成長雙位數、據點已建置完成（原話："organically has been growing double digits for us"）
- 2026-07-23｜CFO｜product：CFO 說 AI 定價工具部分仍在試行，目前價格成功主因是產業紀律（原話："some things that we're working that are really in pilot"）
- 2026-07-23｜CFO｜competition：CFO 稱產業供需紀律是目前租金成功的最大因素（原話："that discipline that is critical."）
- 2026-07-23｜CEO｜competition：CEO 認為 URI 時間利用率高於產業，但產業整體也在提升（原話："the industry overall is driving higher time utilization"）
- 2026-07-23｜CEO｜competition：CEO 說產業整併會持續，連激進新開據點模式的業者也轉向併購（原話："The bigs will continue to get bigger."）
- 2026-07-23｜CEO｜risk：CEO 承認部分設備類別供給偏緊，額外 10 億美元設備買不到（原話："we wouldn't be able to get it."）
- 2026-07-23｜CEO｜risk：CEO 說若本地市場同時強勁，疊加大型專案需求將有供給挑戰（原話："it would be challenging today."）
- 2026-07-23｜CFO｜risk：CFO 指出運送重新調配成本仍在處理中，下半年須持續維持（原話："We've got to keep it up, right?"）
- 2026-07-23｜CFO｜capital_allocation：CFO 說上半年回饋股東 9.98 億，含回購 7.5 億與股利 2.48 億（原話："$750 million through repurchases and $248 million"）
- 2026-07-23｜CFO｜capital_allocation：CFO 重申今年回購 15 億，加股利約回饋 20 億（原話："intend to repurchase $1.5 billion of shares in 2026"）
- 2026-07-23｜CFO｜capital_allocation：S&P 將展望調為正向，12 個月內有機會升投資等級（原話："raising our credit outlook to positive from stable"）
- 2026-07-23｜CFO｜capital_allocation：CFO 說移向投資等級不影響資本配置與併購策略，內部政策原先使其留在高收益級（原話："internal financial policy that kept us in the high-yield"）
- 2026-07-23｜CEO｜capital_allocation：CEO 說併購管線穩健，成長 90% 以上為有機（原話："the pipeline continues to be robust."）
- 2026-07-23｜CFO｜capital_allocation：CFO 說併購以現金報酬率框架呈現，因收購會計可能短期稀釋 ROIC（原話："And that's why we frame the deals really as"）
- 2026-07-23｜CEO｜commitment：CEO 稱團隊靠艦隊生產力「贏得」額外 CapEx，且租金需抵銷通膨（原話："they earned this extra CapEx by"）
- 2026-07-23｜CEO｜commitment：CEO 表示預期租金與各項艦隊生產力組成皆為正向（原話："But rate is a good guy, and we expect it to"）
- 2026-07-23｜CEO｜commitment：CEO 表示明年仍會成長，但幅度與 CapEx 待規劃；預期多賣一些二手設備（原話："expect next year to certainly be another year of growth"）
- 2026-07-23｜CFO｜commitment：CFO 說公司不會迴避客戶要求的小型附屬服務，並會向市場說明對利潤率的影響（原話："So we're not going to shy away from them."）

### 問答異常語氣（迴避／改口／保留）
- URI_Q2_2026_Earnings_Call_20260723.md｜問：Rob Wertheimer / Ken Newman：租金（rate）是否已到位、後半年是否改善｜答法：管理層一貫不給租金數字，只說「rate is a good guy」並預期持續，未回答是否到位
- URI_Q2_2026_Earnings_Call_20260723.md｜問：David Raso：Q2 剔除利得後利潤率 -40bp 到下半年隱含 +10–20bp 的擺動因素｜答法：CFO 未列出擺動因素，改談上半年底層 +10bp 與「季度間正常變動」，並重述全年持平目標
- URI_Q2_2026_Earnings_Call_20260723.md｜問：Steve Fisher：CapEx 增加能否減輕重新調配成本、何時不必再提｜答法：CEO 先否認目前有特別強調，並否定 CapEx 為正向吸收原因；CFO 稱難以量化
- URI_Q2_2026_Earnings_Call_20260723.md｜問：Jamie Cook：CapEx 增加中 gen rent 與 specialty 的占比｜答法：CEO 拒絕拆分，僅稱可假設專長業務占不少
- URI_Q2_2026_Earnings_Call_20260723.md｜問：Tami Zakaria：下半年租賃營收成長是否放緩｜答法：CFO 不給具體預期，要求看區間，並稱要到 10 月才有更新

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 4 | 2 |
| customer_second_source | found | 1 | 2 |
| customer_concentration_credit | found | 2 | 1 |
| supply_demand_durability | found | 2 | 2 |
| regulatory_antitrust | found | 1 | 2 |
| reg_tariff_export | found | 3 | 2 |
| geo_supply_chain | found | 2 | 2 |
| end_markets | found | 8 | 4 |
| substitute_technology | found | 2 | 2 |
| channel_business_model_shift | found | 1 | 3 |
| capital_markets_pricing | found | 3 | 3 |
| major_events | found | 2 | 3 |

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260723","verdict":"觀望","role":"追蹤","H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"結構性租賃滲透 + specialty + 資料中心 capex 使 URI 成長跑贏廣義建築循環的收縮","columns":{"2Y 驗證點":"FY27 rental rev 續正成長；general rentals 不轉負","5Y 驗證點":"租賃滲透率 >62%；specialty 佔比續升","10Y 驗證點":"租賃取代擁有成主流、URI #1 地位穩固","具體數字門檻 / Sourced Floor":"Sourced：ARA 滲透率 59.5%（連 5 年創高）；specialty 20.2% CAGR；Q2 rental rev +12.7%；資料中心 capex >$1T 2026（Dell'Oro）狀態：兌現中但集中度風險升（靠資料中心＋份額，非廣義循環）","漂移觸發":"general rentals 連兩季轉負 → 削弱；資料中心 capex 增速放緩 + 廣義續縮 → 反轉"}},{"id":"H2","text":"URI 維持 #1 規模與定價紀律，Herc 併 H&E 後不侵蝕其 specialty/mega-project 領先","columns":{"2Y 驗證點":"URI 規模仍 ~4x Herc；specialty margin 穩定","5Y 驗證點":"市佔續升；賽局理性（無破壞性降價）","10Y 驗證點":"整併持續、前三大集中度升","具體數字門檻 / Sourced Floor":"Sourced：URI FY26 guide $17.5–17.8B vs Herc $4.275–4.4B（~4x）；但 Herc specialty locations +25%、EBITDA margin ~47% 已與 URI 46.6% 齊平（Herc Q1'26）狀態：規模領先穩，但 specialty 同場競爭升溫","漂移觸發":"specialty 段 margin 連兩季"}},{"id":"H3","text":"結構性再評價可維持（EV/EBITDA ~10x 非循環頂假象，而是租賃滲透 + 資本回報支撐的新常態）","columns":{"2Y 驗證點":"循環未反轉時倍數守住 ~9–10x","5Y 驗證點":"與 ACN/優質工業複利中位收斂","10Y 驗證點":"市場永久接受 URI 為結構複利而非純循環","具體數字門檻 / Sourced Floor":"Sourced：Fwd PE 20x vs 5Y 均 13.5x；EV/EBITDA ~10x vs 10Y 中位 7x（+40%）；P/B 7.2x vs 均 4.6x狀態：溢價已建立但脆弱（若循環反轉，歷史顯示回 6–8x EV/EBITDA）","漂移觸發":"循環反轉 + EV/EBITDA 回落至"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"廣義非住宅建築收縮惡化成衰退 + 資料中心 capex 增速放緩，兩條腿同時斷（peak-cycle 盈餘正常化 + de-rate）","columns":{"對應假設":"H1／H3","時間尺度":"🔥 中期（4–6 季，但循環反轉可快）","監測指標":"ABI（連 40 月","警戒閾值":"fleet productivity 轉負 + general rentals 轉負 → 循環反轉確認、減碼"}},{"id":"R2","text":"Rouse benchmark-pricing 反托拉斯 MDL 敗訴/禁令 → 全產業租賃定價權結構性壓縮（非 URI 規模可分散）","columns":{"對應假設":"H2／H3","時間尺度":"🐢 長期（2+ 年司法程序）","監測指標":"MDL 3152（N.D. Illinois）動議裁決；benchmark-pricing 是否被禁","警戒閾值":"MTD 被駁回進入實質審理 → 風險升；禁令 → §3.F 命中、清倉重評"}},{"id":"R3","text":"估值溢價回吐：市場把 URI 從「20x 結構複利」重估回「13x 循環股」","columns":{"對應假設":"H3","時間尺度":"🔥 中期（估值隨循環轉）","監測指標":"EV/EBITDA vs 自身歷史；Fwd PE 分位","警戒閾值":"循環轉弱 + EV/EBITDA 回落"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":"回檔至 Fwd PE ≤ 15x（~$770）或 EV/EBITDA ≤ 8x；或 ABI 持穩 >50 + 廣義非住宅建築回正確認循環續行","irr_base_pct":6.7,"ev5y_pct":25.0,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"追蹤","signal":"B","val":"🟠","ma":"✅","trap":"🟡","moat_trend":"→","runway_post_y5":"🟡","asym_ratio":1.82,"ev5y_pct":25.0,"irr_base_pct":6.7,"max_dd_pct":-55.0,"bull_5y_price":1760.0,"bear_5y_price":704.0,"p_bull_pct":25.0,"p_bear_pct":30.0,"rearm_trigger":"回檔至 Fwd PE ≤ 15x（~$770）或 EV/EBITDA ≤ 8x；或 ABI 持穩 >50 + 廣義非住宅建築回正確認循環續行","price_at_dd":1035.06,"archetype":"品質複利成長","cycle_position":"晚循環"}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"URI","date":"2026-10-24","schema":"v15.0","contract":"v19","company_name":"United Rentals"},"oneliner":"大型專案帶動 URI 季營收年增16%、全年指引再上調，但前瞻本益比21.2倍是以創紀錄利潤率的晚循環盈餘計價，基本情境五年年化報酬只有約5%，等回到約915美元再談","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/URI_20261024/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/URI_20261024/scenario.json","answers":{"q1_business":{"verdict":"URI 賺的是營建與工業客戶不想自己擁有設備的錢：把設備資本支出轉成按時間計費的租金。錢卡在車隊生產力（租金、時間利用率與組合）這一節點。Q3 2026 營收48.93億美元，GAAP 營業利益率28.8%，調整後 EBITDA 利潤率47.6%","reasoning":"最小交付：Q3 2026 總營收48.93億美元，其中租賃營收43.16億（約88%，年增17.8%），二手設備銷售3.48億（約7%，調整後毛利率46.3%，OEC 回收率51.4%）。分部方面，10-Q 揭露通用租賃設備租賃營收年增8.8%，專業租賃年增34.7%，兩者皆超過營收一成；分部金額占比事實表未涵蓋。GAAP 營業利益14.09億，利益率28.8%。TTM 毛利率38.36%，年度毛利率由 FY2022 的42.9%逐年降到 FY2025 的38.2%，代表成長來自量與組合，單位毛利被附屬與轉租收入稀釋。產業時鐘判在擴張期：ARA 預測美國租賃市場2026–2028年每年成長約3.6%–4.4%，營建設備板塊停滯、一般工具續成長，URI 靠大型專案跑贏產業，不是全面過熱。供需持久性判為週期性將反轉：大型專案管線到2027年有能見度，但管理層承認時間利用率已在歷史高點、轉租年增逾37%，同業有計畫車隊翻倍，供給可逆性高。議價權：客戶極分散（最大客戶占營收1%以下、前十大5%），錢不卡在客戶端；上游集中採購依賴少數設備廠，新車成本受關稅與原物料推升。單點依賴：無單一客戶依賴，集中度在大型專案這一需求型態，管理層稱成長主力仍是大型專案，在地市場只貢獻幾個百分點。","fact_refs":["f_kpi0_gaap","f_kpi2_gaap","f_kpi1_ebitda_non_gaap_non_gaap","f_kpi6_fleet_productivity","f_kpi7","f_kpi5_2026","f_peer_uri_gross_margin_pct"],"verdict_values":{"revenue_quality":"租賃營收約占88%，按時間計費且客戶分散，品質中上；大型專案集中與二手銷售會隨週期擺動","unit_econ_note":"車隊生產力年增6.5%（租金、時間利用率、組合皆正），減去假設車隊通膨1.5%後 OER 年增12.9%；附屬與轉租年增逾37%，利潤率低於核心租賃","archetype":{"primary":"品質複利成長","secondary":"循環/商品","confidence":"中","fingerprint":"資本密集的設備租賃平台，規模密度帶來利潤率領先，盈餘隨非住宅營建與工業資本支出週期擺動"},"industry":{"clock_phase":"II","sd_verdict_source":"週期性將反轉：大型專案需求延續到2027年有管理層說法與客戶調查支撐，但時間利用率已近上限、轉租暴增、同業擴車隊，供給可在一到兩年內補上","bargaining":{"up":"上游設備廠集中採購，依賴一組關鍵供應商；新車成本受關稅與原物料推升","down":"下游極分散，最大客戶占營收1%以下，前十大合計5%","geo":"美國與加拿大約1,800個據點，地緣風險低；中國採購占比未揭露"},"profit_pool_dir":"向大型業者集中（管理層稱大者恆大、整併持續）；利潤池占比的量化數字事實表未涵蓋","tam_table":{"expanded":false,"reason":"成熟產業，非低滲透或新品類；滲透率與利潤池分年數字事實表未涵蓋，只有 ARA 年成長預測，不足以展開"}}}},"q2_moat":{"verdict":"護城河方向持平：規模密度與一站式（通用加專業）讓 URI 營業利益率25.1%，比 Herc 的13.1%高12pp、比 WSC 的20.4%高4.7pp；北美市占約15%與去年持平，評 B 級，趨勢不擴大也不縮小","reasoning":"機制：美加約1,800個據點的密度讓車隊在專案間調度，時間利用率與運送成本優於小型業者；大型專案重視供應確定性與單一供應商，一站式組合（專業租賃 Q3 年增約35%，年初至今40個新據點）把客戶留在同一平台。可證方向：TTM 營業利益率 URI 25.1%、HRI 13.1%、CAT 17.5%、WSC 20.4%，顯示規模優勢存在；但事實表只有單期數字，無法判斷差距在擴大或收窄。市占約15%連兩年持平，次大對手 Sunbelt 約11–13%。執行力評8分：Q3 調整後 EBITDA 利潤率年增160bp，在低毛利的附屬與轉租成長、燃料與勞動成本通膨下仍擴張。定價力評6分：10-K 自承產業分散、相對市占小可能不利於抑制租金壓力，過去曾因競爭失去份額或價格；上一季 CFO 也說租金成功主因是產業供給紀律，不是 URI 單方定價。兩項平均7分，B 級；執行力與定價力皆穩定，趨勢持平。報酬持續期：CFO 揭露 ROIC 12.3%、年增30bp，屬高利益率、低周轉的資產密集型；四個檢查點皆黃燈，主要變數是需求週期與反托拉斯訴訟。再投資：增量報酬約12%、再投資率約40%（推估），內生成長上界約5%。","fact_refs":["f_peer_uri_operating_margin_pct","f_peer_hri_operating_margin_pct","f_peer_wsc_operating_margin_pct","f_peer_cat_operating_margin_pct","f_peer_uri_gross_margin_pct","f_peer_uri_fcf_margin_pct","f_peer_hri_fcf_margin_pct","f_peer_wsc_fcf_margin_pct","f_kpi1_ebitda_non_gaap_non_gaap"],"verdict_values":{"moat":{"mechanism":"規模密度加一站式產品組合：據點密度降低調度與運送成本、提高時間利用率；大型專案偏好單一供應商與供應確定性","execution":8,"pricing":6,"grade":"B","trend":"→","trend_evidence":"北美市占約15%與一年前持平（10-K）；營業利益率領先 HRI 12pp，但事實表只有單期數字，無跨期差距；租金上漲歸功產業紀律，未見 URI 單獨提價能力擴大","competitor_notes":[{"name":"HRI","strategy_note":"併 H&E 後擴專業租賃據點，TTM 營業利益率13.1%、FCF 利潤率−2.6%，以擴車隊換份額，財務彈性弱於 URI"},{"name":"AHT.L","strategy_note":"Sunbelt 為北美第二大，市占約11–13%，FY2027 指引租賃營收成長5–8%，與 URI 同打大型專案與專業租賃；事實表無其財務數字"},{"name":"WSC","strategy_note":"模組化空間租賃，毛利率50.5%、FCF 利潤率13.0%，只與 URI 專業租賃中的行動模組與儲存重疊，非全面競爭"},{"name":"CAT","strategy_note":"設備廠兼經銷體系，法說中被點名正更積極切入小型設備與大型專案租賃，是供應商也是潛在競爭者"}],"peer_na_reason":"AHT.L 事實表無損益資料，Sunbelt 只有市占與成長指引","threats":[{"level":"🟡","text":"同業與新進者擴車隊：有業者計畫車隊翻倍、設備廠切入大型專案，需求回落時可能壓租金；10-K 自承產業分散、市占小可能難以抑制租金壓力，過去曾因競爭失去份額或價格","p":"30%","evidence_refs":["competitive_share_entrants#1","competitive_share_entrants#2"]},{"level":"🟡","text":"客戶需求變化可能使部分既有設備過時，須以更高成本購置新設備（10-K 風險因子）；搜尋未見具名替代技術","p":"10%","evidence_refs":["substitute_technology#0"]},{"level":"🟡","text":"Herc 併 H&E 後在專業租賃同場競爭升溫，可能壓縮 URI 專業租賃的成長與利潤率","p":"25%","evidence_refs":[]}],"roic_durability":{"quadrant":"高利益率×低周轉","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"客戶要解決的是避免設備資本支出與閒置，租賃取代擁有屬需要而非想要；但大型專案的急迫性不等於持久性，管理層稱成長主力仍是大型專案、在地市場只貢獻幾個百分點，ARA 預測產業年成長約4%"},{"item":"決策層級","level":"🟡","text":"決策單位是單一工地或專案的租用決定，替代者多（Sunbelt、Herc 與區域業者），轉換成本低；大型專案重視供應確定性與減少現場廠商，讓 URI 在此客群替代性較低，但事實表無續約率或漲價後流失數據"},{"item":"價值鏈分配","level":"🟡","text":"上游設備廠集中，新車成本受關稅與原物料推升，集中採購依賴少數關鍵供應商；下游客戶分散不卡錢；二手回收率51.4%顯示殘值市場正常。URI 的位置靠規模與密度，不靠稀缺"},{"item":"社會容忍度","level":"🟡","text":"私人反托拉斯集體訴訟指控業者透過 Rouse 共享租金基準資料協同定價，案件未決；若法院禁止使用基準資料，全產業定價紀律可能鬆動，屬定價上限的法律風險，非監管授權"}],"roiic":"約12%（以 CFO 揭露 ROIC 12.3%、年增30bp推估增量報酬接近當期水準；事實表未涵蓋分年投入資本）","reinvest_rate":"約40%（推估區間30%–65%：以 FY2026 指引營業利益與自由現金流反推約30%–35%，以平均車隊規模年增7.9%反推更高）","endo_ceiling":5.0,"formula_note":"內生成長上界＝增量報酬約12%×再投資率約40%≈5%。NOPAT 以 TTM 營業利益率25.1%×FY2026 營收指引中值181億≈45億、稅率約25%（推估，事實表未涵蓋）≈34億；自由現金流指引中值23億。折舊與投入資本事實表未涵蓋，區間寬，取偏保守值"}}}},"q3_growth":{"verdict":"後五年跑道中等：成長由量（平均車隊規模年增7.9%）與價（車隊生產力6.5%）各占約一半，併購不到一成；專業租賃是第二條成長線，但核心租賃已成熟、產業年成長約4%","reasoning":"成長拆解：Q3 OER 年增12.9%＝車隊規模7.9%加車隊生產力6.5%減假設通膨1.5%；上一季管理層稱成長九成以上為有機。共識 EPS：FY2026 51.84、FY2027 60.91、FY2028 69.22，FY2026 到 FY2028 年化約15.5%；以 FY2025 GAAP 稀釋 EPS 38.61為基期算三年約21.5%，但基期為 GAAP、共識為調整後，口徑不同會高估成長。內生上界約5%（見護城河段）。缺口約10pp，歸因：利潤率擴張（調整後 EBITDA 利潤率年增160bp，屬週期高位的營運槓桿）、淨回購約2%，其餘約一半無法歸因，靠時間利用率與租金維持高檔，依賴週期延續，信心上限中。跑道：事實表未涵蓋滲透率，無法推算到30%滲透的年數；專業租賃仍有地理空白並持續新開據點，是有來源的第二曲線，但營收占比未揭露，不足以給寬跑道。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_fy3_pct","f_kpi6_fleet_productivity","f_kpi5_2026"],"verdict_values":{"growth":{"driver_mix":"量（車隊規模年增7.9%）約一半、價與組合（車隊生產力6.5%）約一半；附屬與轉租年增逾37%補量；併購不到一成；回購每年約減少2%股數","runway_years":"事實表未涵蓋滲透率，無法推算","runway_post_y5":"🟡","endo_ceiling_basis":"增量報酬約12%×再投資率約40%≈5%，推導見護城河段","segments":[{"item":"通用租賃設備租賃營收","value":"Q3 2026 年增8.8%（10-Q），來自平均車隊增加與需求強勁"},{"item":"專業租賃設備租賃營收","value":"Q3 2026 年增34.7%（10-Q），年初至今40個新據點，各業務線皆雙位數成長"},{"item":"二手設備銷售","value":"Q3 2026 收入3.48億美元、年增4.5%；全年預計賣出約28億 OEC，回收率約五成出頭"}],"decay_signals":["年度毛利率連續下滑：FY2022 42.9%到 FY2025 38.2%（以年度代替季度，部分來自附屬與轉租組合稀釋）","自由現金流對淨利偏低：FY2026 指引中值約23億對推估淨利約32億，比率約0.7；前一年度事實表未涵蓋，記半個","更新性資本支出占自由現金流比重高：全年預計賣出約28億 OEC 需重置，事實表未拆維持與成長資本支出，記半個"],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"資本配置中上：回購買入收益率不過關，股權激勵稀釋極低，併購增量報酬事實表未涵蓋；成長資本支出與股東回饋同時兼顧","reasoning":"自由現金流 Q3 2.72億、年初至今逾14億，全年指引21.5–24.5億。以 CFO 所稱每股約32美元對應約20億回饋反推股數約6,250萬股，搭配 FY2026 共識 EPS 51.84推估淨利約32億，自由現金流對淨利約0.7。股權激勵 Q3 4,300萬，占營收0.88%、占營業利益3.05%。現金去向（年初至今）：總租賃資本支出47億、回購11.25億、股利3.71億，併購規模小（分析師提及本季約1億）。淨槓桿1.8倍，在1.5–2.5倍目標區間內；S&P 本月升至投資等級，未來再融資利差會收窄。三項檢核：併購增量報酬缺資料；回購買入收益率＝1÷21.2≈4.7%，要過關須10年期公債殖利率低於2.7%，法說中分析師形容為利率偏高的環境，判不過；股權激勵年化約1.7億，對約687億市值稀釋約0.25%，遠低於1.5%，過關。","fact_refs":["f_kpi3_fcf","f_kpi4_sbc_stock_compensation_e","f_kpi5_2026","f_fwd_pe_latest","f_consensus_eps_fy1","f_price_at_dd"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":true,"passed":null,"input":"事實表未涵蓋併購後增量報酬；管理層以現金報酬率框架評估併購，近12個月未完成重大併購"},{"name":"buyback_yield","applicable":true,"passed":false,"input":"盈餘殖利率約4.7%（前瞻本益比21.2倍倒數）；需10年期殖利率≤2.7%才過，法說描述為高利率環境"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"股權激勵 Q3 4,300萬、年化約1.7億，對約687億市值毛稀釋約0.25%/年，且回購持續減少股數"}]},"governance":{"capital_returns":{"expanded":false,"reason":"成長九成以上為有機，不靠併購撐；回饋結構已寫在理由中，分年回購均價事實表未涵蓋"}}}},"q5_valuation":{"verdict":"現價要求大型專案週期延續到2028年以後、利潤率守在高檔，且市場續給高倍數才划算；週期延續我信一到兩年，五年不信，估值偏貴","reasoning":"股價1,098.88美元，FY2026 共識 EPS 51.84對應前瞻本益比21.2倍，FY2027 共識60.91對應18.0倍。共識近期上修 FY1 3.5%、FY2 4.7%、FY3 5.8%，盈餘動能正向。PEG 以 FY2026 到 FY2028 年化約15.5%計約1.37，看似合理，但分母是調整後 EBITDA 利潤率創紀錄47.6%的週期高位盈餘。五年估值分位事實表未涵蓋，不計算。賣方目標價均值約1,150–1,270美元（各平台不同），距現價約+5%到+15%，不支持大幅低估。情境樹基本情境（FY2031 EPS 77、本益比16倍）約1,232美元，加股息與淨回購約年化5%，低於8%的弱報酬線。結論：好生意，但價格已反映週期延續，要等更好的價格。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_fy1_pct","f_consensus_rev_fy2_pct","f_consensus_rev_fy3_pct","f_dividend_yield_ttm"],"verdict_values":{"valuation":{"basis":"前瞻本益比（FY2026 共識 EPS 51.84）；FY2027 18.0倍作交叉檢查","tier":"資本密集設備租賃","peers":{"expanded":false,"reason":"事實表同業對照只有利潤率，未含同業前瞻本益比，無法做倍數對照；終端倍數以自身現值21.2倍與 FY2027 18.0倍為錨"},"fwd_pe":21.2,"peg":1.37,"percentile_5y":null,"val_light":"🟠","val_light_derivation":"前瞻本益比21.2倍、PEG 約1.37；分母為週期高位盈餘，基本情境五年年化約5%低於8%，賣方目標均值上檔僅約5%–15%，判偏貴","upside_short_pct":6.7,"upside_mid_pct":12.1,"denominator_disputed":false,"denominator_note":"FY2026 GAAP 含鷹架業務出售利得，調整後口徑已排除；爭點在盈餘位於週期哪個位置，而非一次性項目"}}},"q6_how_wrong":{"verdict":"最可能看錯的地方是把大型專案高峰當成常態：若2027年後資料中心、半導體廠與電力專案同時退潮，而同業正在擴車隊，租金與時間利用率會一起掉","reasoning":"三個反證視角與裁定見反證紀錄。陷阱風險中等：衰退訊號約亮兩個（年度毛利率連降、自由現金流對淨利偏低），護城河未受損，風險在週期與估值，不在生意變差。另有兩項非經營風險：反托拉斯集體訴訟未決、設備成本受關稅推升。上一季法說管理層對租金是否到位、下半年利潤率擺動因素與資本支出拆分都未正面回答；本季對租金仍只說持續為正、不給數字。","fact_refs":["f_kpi6_fleet_productivity","f_fwd_pe_latest","f_rsi14"],"verdict_values":{"trap":{"verdict":"🟡","label":"週期高位盈餘陷阱風險中等"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":51.84,"pe":21.2,"basis":"FY2026 共識調整後 EPS 51.84，與終端倍數同為前瞻一年口徑"},"eps":{"bull":[63.5,72.5,81.0,89.0,97.0],"base":[60.0,66.0,70.0,73.5,77.0],"bear":[56.0,48.0,42.0,46.0,50.0]},"pe":{"bull":20,"base":16,"bear":12},"p":{"bull":20,"base":50,"bear":30},"yield_pct":{"dividend":0.7,"net_buyback":1.9},"second_stage":{"bull_cagr_pct":8,"base_cagr_pct":5},"max_dd":{"lo":-60,"hi":-40,"basis":"EPS 回落路徑：FY2026 51.84降到谷底約42（−19%），本益比由21.2倍壓到11–12倍，股價約460–500美元，即−54%到−58%；估值回吐路徑：EPS 持平、本益比回到14倍左右，約−34%到−40%；兩者合併取−40%到−60%","trigger_time":null},"basis":{"bull":"大型專案延續到2030年、在地市場接棒，車隊生產力每年正成長，利潤率續擴，終端20倍接近現值","base":"FY2027 略低於共識，2028年後大型專案放緩、成長回到中個位數加回購，終端16倍；同業倍數事實表未涵蓋，以自身 FY2027 18.0倍折價為錨","bear":"2028年前後大型專案退潮遇同業擴車隊，車隊生產力轉負、EPS 回落約兩成後緩步回升，終端12倍為成長熄火到約10%的倍數"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"S&P Global 指營建設備板塊因營建市場停滯；10-K 自承產業分散、市占小難抑制租金壓力；本季轉租年增逾37%、時間利用率歷史高點，同業計畫車隊翻倍","assumption":"大型專案需求可延續到2028年以後，且產業維持供給紀律","consequence":"若2027–2028年大型專案同時退潮，新車隊同步交付，車隊生產力轉負，EPS 回落兩成以上、本益比回到12倍，五年後虧45%–55%","ruling":"採納：放進 Bear 30%，並以2027年1月指引成長<3%作唯一致命點","watch":"車隊生產力、轉租增速、二手回收率、2027年1月指引","evidence_refs":["end_markets#5","competitive_share_entrants#1"],"fact_refs":["f_kpi6_fleet_productivity","f_kpi7"]},{"view":"論點成功但股東經濟變差","evidence":"FY2026 資本支出指引上調3億，自由現金流指引不變；自由現金流對淨利約0.7；10-K 指新設備成本含原物料關稅可能續升，集中採購依賴少數關鍵供應商","assumption":"營收成長能以相同報酬率轉成股東現金","consequence":"營收照預期成長，但每元新車成本上升、二手殘值回落，ROIC 從12.3%滑向資金成本，成長吃掉現金，回購縮手","ruling":"部分採納：目前 ROIC 年增30bp、回饋約3%，尚未發生；設 ROIC<11%減碼","watch":"ROIC、自由現金流指引、二手回收率、淨資本支出對租賃營收增速","evidence_refs":["reg_tariff_export#0","geo_supply_chain#1"],"fact_refs":["f_kpi3_fcf","f_kpi5_2026"]},{"view":"價格已反映太多","evidence":"前瞻本益比21.2倍，分母是調整後 EBITDA 利潤率創紀錄47.6%的盈餘；賣方目標均值上檔約5%–15%","assumption":"市場會持續給週期股高於現值的倍數","consequence":"即使 EPS 照共識成長，倍數回到16倍，五年年化只有約5%","ruling":"採納：不追價，等約915美元（FY2027 共識15倍）再建首倉","watch":"前瞻本益比、共識修正方向","evidence_refs":[],"fact_refs":["f_fwd_pe_latest","f_consensus_eps_fy2"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 1035.06 → 本次 1098.88（+6.2%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=1035.06","side_b":"本次 price_at_dd=1098.88","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 1,035.06 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 1,035.06 美元：Bull 價 1,760、Bear 價 704，五年期望值 +25.0%，基準年化 6.7%，不對稱比 1.82","side_b":"本次情境、股價仍用 1,035.06 美元：Bull 價 1,940、Bear 價 600，五年期望值 +14.4%，基準年化 3.5%，不對稱比 1.39","ruling":"先換情境、股價不動：五年期望值少 10.6 個百分點，基準年化少 3.2 個百分點。不對稱比由 1.82 變為 1.39。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 1,035.06 美元：五年期望值 +14.4%，基準年化 3.5%，不對稱比 1.39","side_b":"本次情境、股價 1,098.88 美元：五年期望值 +7.7%，基準年化 2.3%，不對稱比 1.12","ruling":"再換股價、情境不動：起點價上漲 6.2%，五年期望值少 6.6 個百分點，基準年化少 1.2 個百分點，不對稱比由 1.39 降到 1.12。合計五年期望值比前份少 17.3 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"成長延續與晚循環訊號並存","cause":null,"prior_field":null,"side_a":"管理層說比6–12個月前更樂觀，2027年是成長年；全年營收指引兩度上調；在地市場開始貢獻幾個百分點成長；客戶調查持續正面；上一季預告全年利潤率持平，本季實際隱含約+70bp","side_b":"時間利用率已在歷史高點、轉租暴增需外借設備；營建設備板塊停滯；同業與設備廠擴車隊；利潤率創紀錄","ruling":"可調和，屬程度差異：一到兩年成長延續可信，五年需週期折價。現在就買的最強論證：共識三年 EPS 皆上修、投資等級降低資金成本、每年回饋約3%，若2027指引≥8%，FY2027 18倍並不貴。裁定仍觀望，因基本情境年化約5%","evidence_level":"公司 8-K、法說、ARA 預測","settle_metric":"2027年1月總營收（不含二手）指引成長","if_then":["若2027指引成長≥8%且車隊生產力續正，股價≤1,000美元時分批建首倉約2%","若股價續漲但指引未出，不追","若指引成長<3%，不建倉，Bear 機率上調至40%"],"evidence_refs":["end_markets#5"]},{"axis":"結構判斷是否因 Q3 新資料改變","cause":"新證據","prior_field":["signal","trap","moat_trend","runway_post_y5","archetype","cycle_position"],"side_a":"前份（2026-07-23）：綜合訊號 B、陷阱風險中等、護城河持平、後五年跑道中等、品質複利成長型、晚循環","side_b":"本次維持不變：Q3 營收年增16%、指引再上調、專業租賃年增35%、S&P 升投資等級，屬既有論點兌現；時間利用率歷史高點與轉租暴增強化晚循環判斷","ruling":"新證據強化近期成長，未改變五年結構，各欄維持","evidence_level":"公司 8-K 與法說","settle_metric":"2027年1月全年指引","if_then":["若2027指引成長≥8%且車隊生產力續正，週期位置改判中循環並重算情境","若指引成長<3%，維持晚循環並把 Bear 機率上調至40%"],"evidence_refs":[]},{"axis":"估值與裁決","cause":"價格變動","prior_field":["val"],"side_a":"前份股價約1,035美元，估值偏貴，觀望、追蹤","side_b":"本次1,098.88美元（+6%），FY2026 共識 EPS 同步上修，前瞻本益比約21倍，估值結論仍偏貴；裁決與角色依新輸入重算","ruling":"股價漲幅與盈餘上修大致抵銷，估值結論不變","evidence_level":"收盤價與共識快照","settle_metric":"前瞻本益比","if_then":["若股價≤915美元且車隊生產力為正，進場首倉約2%","若股價續漲而共識不再上修，不追"],"evidence_refs":[]},{"axis":"情境機率與回撤範圍","cause":"方法變動","prior_field":["p_bull_pct","p_bear_pct","max_dd_pct"],"side_a":"前份 Bull 25%、Bear 30%，最大回撤單點−55%","side_b":"本次 Bull 20%、Base 50%、Bear 30%；最大回撤改為區間−40%到−60%","ruling":"Bull 下調5pp：Bull 路徑要大型專案延續到2030年且倍數守20倍，時間利用率已近上限、同業擴車隊，延續五年的機率比前份假設低；回撤改區間以涵蓋估值回吐與 EPS 回落兩條路徑","evidence_level":"法說與情境推導","settle_metric":"車隊生產力與2027指引","if_then":["若2027指引≥8%，Bull 機率回到25%","若車隊生產力連2季為負，Bear 機率上調至40%"],"evidence_refs":[]},{"axis":"進場首倉條件變動","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"回檔至 Fwd PE ≤ 15x（~$770）或 EV/EBITDA ≤ 8x；或 ABI 持穩 >50 + 廣義非住宅建築回正確認循環續行","side_b":"股價回到約915美元以下（FY2027 共識 EPS 60.91的15倍）且最近一季車隊生產力仍為正，才進場首倉","ruling":"FY2026 只剩一季，舊錨已被兌現，改用 FY2027 共識；EV/EBITDA 與 ABI 事實表未涵蓋、無法追蹤，刪除；15倍不變，價格錨因共識上修從約770上移到約915美元；加車隊生產力為正，避免週期轉弱時接刀","evidence_level":"共識快照","settle_metric":"股價與車隊生產力","if_then":["若兩條件同時成立，進場首倉約2%","若股價到價但車隊生產力為負，不買"],"evidence_refs":[]},{"axis":"出場門檻新設","cause":"新證據","prior_field":["kill_metrics"],"side_a":"前份未設定出場門檻（null）","side_b":"本次設五條：車隊生產力連2季<0減碼、2027指引成長<3%減碼、ROIC<11%減碼、二手回收率<45%減碼、法院禁止使用租金基準資料則清倉","ruling":"Q3 揭露 ROIC 12.3%、回收率51.4%、車隊生產力6.5%，可作為量化基準，故新設","evidence_level":"公司 8-K 與法說","settle_metric":"各季新聞稿","if_then":["任一減碼條件觸發，持有部位減半","禁令成立，清倉並重做研究"],"evidence_refs":[]},{"axis":"Single Thing 變動","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未設定唯一致命點（null）","side_b":"2027年1月全年指引中總營收（不含二手）成長低於3%，代表大型專案高峰已過、在地市場未接棒","ruling":"車隊生產力是盈餘最大單一敏感項，年度指引是最早、可明確判讀的離散事件，故設為 Single Thing","evidence_level":"法說：管理層稱1月才給2027指引","settle_metric":"2027年1月指引","if_then":["若成長<3%，不建倉，持有則減碼一半","若成長≥6%，維持追蹤並檢查進場價"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"2027年1月全年指引檢驗大型專案延續","type":"假設驗證","maps_to":"H1","metric":"2027 總營收（不含二手）指引成長","threshold":"≥6% 維持；3%–6% 削弱","action":"≥6% 維持追蹤；3%–6% 把 Bull 機率下調至15%","source_freq":"年度指引（每年1月）","date":"2027-01"},{"n":2,"text":"大型專案高峰已過","type":"Single Thing","maps_to":"Single Thing","metric":"2027 總營收（不含二手）指引成長","threshold":"<3%","action":"不建倉；若已持有減碼一半","source_freq":"年度指引","date":"2027-01"},{"n":3,"text":"週期反轉：車隊生產力轉負","type":"風險","maps_to":"R1","metric":"車隊生產力年增","threshold":"連續2季<0%","action":"減碼一半並停止加碼","source_freq":"季度新聞稿","date":null,"evidence_refs":["end_markets#5"]},{"n":4,"text":"反托拉斯集體訴訟進展","type":"風險","maps_to":"R2","metric":"Rouse 租金基準資料集體訴訟程序","threshold":"集體認證通過或不利和解；法院禁止使用基準資料","action":"前者減碼至半倉；後者清倉","source_freq":"法院文件與10-K／10-Q","date":null,"evidence_refs":["regulatory_antitrust#0","end_markets#7"]},{"n":5,"text":"同業擴車隊造成供給過剩","type":"風險","maps_to":"R3","metric":"二手設備 OEC 回收率","threshold":"連2季<45%","action":"減碼一半","source_freq":"季度新聞稿","date":null,"evidence_refs":["competitive_share_entrants#1","competitive_share_entrants#2"]},{"n":6,"text":"設備成本上升侵蝕報酬","type":"風險","maps_to":"R4","metric":"公司揭露 ROIC","threshold":"<11%","action":"減碼一半","source_freq":"季度法說","date":null,"evidence_refs":["reg_tariff_export#0","geo_supply_chain#1"]},{"n":7,"text":"價格回到合理區","type":"估值rearm","maps_to":"H1","metric":"股價與車隊生產力","threshold":"股價≤915美元且最近一季車隊生產力>0","action":"分批進場首倉約2%","source_freq":"每日股價／季度新聞稿","date":null},{"n":8,"text":"Q4 財報後複審","type":"複審日期","maps_to":null,"metric":"2027 指引全套","threshold":null,"action":"重跑研究","source_freq":"一次","date":"2027-01"}],"kill_metrics":[{"metric":"車隊生產力年增","bear_threshold":"連續2季<0%","window":"2026Q4–2027Q4","source":"公司季度新聞稿 8-K","last_status":"ok"},{"metric":"2027 總營收（不含二手）指引成長","bear_threshold":"<3%","window":"2027-01","source":"Q4 2026 新聞稿","last_status":"unknown"},{"metric":"公司揭露 ROIC","bear_threshold":"<11%","window":"滾動4季","source":"季度法說","last_status":"ok"},{"metric":"二手設備 OEC 回收率","bear_threshold":"連2季<45%","window":"滾動2季","source":"公司季度新聞稿 8-K","last_status":"ok"},{"metric":"Rouse 租金基準資料反托拉斯訴訟","bear_threshold":"法院禁止使用基準資料","window":"至判決","source":"法院文件與公司10-K","last_status":"unknown"}],"evidence_dismissed":[],"action_conditions":{"rearm_trigger":"股價回到約915美元以下（FY2027共識EPS 60.91的15倍）且最近一季車隊生產力仍為正","exec_line":"觀望；條件達成時分批建首倉約2%，2027年1月指引確認成長≥6%再加到約4%","holding_cap":"首倉≤2%，上限4%（深回撤可達−60%）"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":"晚循環","cycle_verdict":"等回踩","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":null,"wait_for_price":true,"wait_for_price_condition":"股價≤約915美元（FY2027 共識15倍）且車隊生產力續正"},"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟠', moat_trend='→', week26=13.2, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position='晚循環', moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":true,"basis":"signal='B', val='🟠'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":false,"basis":"signal='B', val='🟠', ma='🟡'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟠', ma='🟡'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟠', ma='🟡'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"pacing":[],"holding_cap":null,"requires_critic":[]},"thesis":{"H":[{"id":"H1","text":"大型專案（電力、基建、資料中心、製造）與專業租賃讓租賃營收在2027年續以高個位數以上成長，FY2027 共識 EPS 60.91可達成","2y":"FY2027 租賃營收年增≥6%，車隊生產力每季為正","5y":null,"10y":null,"threshold":"租賃營收年增≥6%；車隊生產力>0%","source":"季度 8-K 新聞稿與法說、2027年1月全年指引","drift_rule":"TTM 租賃營收成長連2季比門檻低5%以上＝削弱；連3季低10%以上＝反轉；車隊生產力連2季為負直接反轉"},{"id":"H2","text":"規模密度與一站式組合維持利潤率領先：營業利益率領先 Herc 至少8pp，調整後 EBITDA 利潤率在完整週期內守住45%以上","2y":null,"5y":"營業利益率領先 Herc ≥8pp；專業租賃年成長≥10%","10y":null,"threshold":"營業利益率領先 HRI ≥8pp（現為12pp）；調整後 EBITDA 利潤率≥45%（現47.6%）","source":"同業季報與年報、URI 季度新聞稿","drift_rule":"TTM 偏離門檻連4季≥5%＝削弱；連6季≥10%＝反轉"},{"id":"H3","text":"資本報酬高於資金成本：ROIC 守在11%以上、淨槓桿1.5–2.5倍，每年以股息加回購回饋約3%市值","2y":null,"5y":"ROIC≥11%；淨槓桿≤2.5倍；年回購≥10億美元","10y":null,"threshold":"ROIC≥11%（現12.3%）；淨槓桿≤2.5倍（現1.8倍）；年回購≥10億美元","source":"季度法說揭露 ROIC 與槓桿、10-K 現金流量表","drift_rule":"TTM 偏離門檻連4季≥5%＝削弱；連6季≥10%＝反轉"}],"R":[{"id":"R1","text":"週期反轉：大型專案高峰後下滑、在地市場未接棒，營建設備板塊已停滯，車隊生產力轉負、二手回收率下滑","h_ref":"H1","clock":"🔥","threshold":"車隊生產力連2季<0%→減碼一半","evidence_refs":["end_markets#5"]},{"id":"R2","text":"Rouse 租金基準資料反托拉斯集體訴訟：若法院禁止使用基準資料或不利和解，全產業定價紀律鬆動","h_ref":"H2","clock":"🐢","threshold":"集體認證通過或不利和解→減碼至半倉；禁令→清倉","evidence_refs":["regulatory_antitrust#0","end_markets#7"]},{"id":"R3","text":"競爭供給過剩：產業分散、URI 市占僅約15%，同業與設備廠擴車隊，需求回落時壓租金，過去曾因競爭失去份額或價格","h_ref":"H2","clock":"🔥","threshold":"二手回收率連2季<45%或車隊生產力轉負→減碼","evidence_refs":["competitive_share_entrants#1","competitive_share_entrants#2"]},{"id":"R4","text":"設備成本與供應商：關稅與原物料推升新車成本，集中採購依賴少數關鍵供應商，侵蝕新增投資報酬","h_ref":"H3","clock":"🐢","threshold":"ROIC<11%→減碼一半","evidence_refs":["reg_tariff_export#0","geo_supply_chain#1"]}],"single_thing":{"description":"2027年1月公布的全年指引中，總營收（不含二手）成長低於3%，代表大型專案高峰已過、在地市場未接棒","why_fatal":"車隊生產力是盈餘最大的單一敏感項：時間利用率已在歷史高點，成長一停，租金與利用率同步回落，加上同業擴車隊，EPS 可能回落兩成以上、本益比從21倍壓到12倍左右","if_happens":"不建倉；若已持有減碼一半，Bear 機率上調至40%並重跑情境樹","how_monitor":"2027年1月 Q4 財報與全年指引；期間每季看車隊生產力、轉租增速與管理層對大型專案管線的描述","probability":"約20%（12–24個月）"}},"appendix_a":{"growth_durability":6,"quality_score":7,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":18.0,"peg_fy2":1.33,"stress":{"pass":null,"total":null}},"eps_meta":{"base_eps_path":{"FY2025A":38.61,"FY2026E":51.84,"FY2027E":60.91,"FY2028E":69.22},"fy_end_month":12,"eps_basis":"共識為調整後 EPS（Koyfin 快照）；基期 FY2025A 38.61為 GAAP 稀釋 EPS（事實表未收調整後基期），三年 CAGR 因口徑不同偏高"},"catalysts":[{"date":"2027-01","date_precision":"month","type":"guidance","event":"Q4 2026 財報與2027全年指引（營收、資本支出、回購）","impact":"高","watch":"總營收（不含二手）成長是否≥6%、資本支出規模、車隊生產力"},{"date":null,"type":"regulatory","event":"Rouse 租金基準資料反托拉斯集體訴訟程序進展","impact":"中","watch":"集體認證、和解或禁令"},{"date":"2027-04","date_precision":"month","type":"other","event":"Q1 2027 財報","impact":"中","watch":"車隊生產力與在地市場是否接棒"}]}
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
