你是 DD 管線 v20 的判斷層閘（gate），標的 FIX（20261025）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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
- `f_kpi0_gaap`（q1_business）｜營收（GAAP）＝3265.656 USD M｜期間與口徑：Q2 FY2026（季末 2026-06-30，公告於 2026-07-23）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 8-K Ex.99.1（numbers.latest_quarter_kpis.items[0]，as_of Q2 FY2026（季末 2026-06-30，公告於 2026-07-23））
  - 註記：查無（未取得該季共識）
- `f_kpi2_gaap`（q1_business）｜GAAP 營業利益／利益率＝557.966 USD M（利益率 17.1%）｜期間與口徑：Q2 FY2026（季末 2026-06-30，公告於 2026-07-23）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 8-K Ex.99.1（numbers.latest_quarter_kpis.items[2]，as_of Q2 FY2026（季末 2026-06-30，公告於 2026-07-23））
  - 註記：查無
- `f_kpi1_non_gaap`（q1_business）｜Non-GAAP 營業利益／利益率＝— n/a｜期間與口徑：Q2 FY2026（公告於 2026-07-23）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司不揭露 non-GAAP 營業利益；僅揭露 Adjusted EBITDA 600.5M（利益率 18.4%）（numbers.latest_quarter_kpis.items[1]，as_of Q2 FY2026（公告於 2026-07-23））
  - 註記：查無
- `f_kpi5`（q1_business）｜管理層指引＝— n/a｜期間與口徑：Q2 FY2026（公告於 2026-07-23）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司新聞稿 8-K Ex.99.1（numbers.latest_quarter_kpis.items[5]，as_of Q2 FY2026（公告於 2026-07-23））
  - 註記：無數字指引；僅定性：optimistic about our results for the remainder of 2026 and well into 2027
- `f_kpi6_backlog`（q1_business）｜Backlog（在手訂單）＝14060 USD M｜期間與口徑：Q2 FY2026（季末 2026-06-30，公告於 2026-07-23）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 8-K Ex.99.1；same-store 13,700M（numbers.latest_quarter_kpis.items[6]，as_of Q2 FY2026（季末 2026-06-30，公告於 2026-07-23））
  - 註記：查無
- `f_earnings_recency`（q1_business）｜最近一次財報日＝2026-10-22 date｜期間與口徑：2026-10-22／距今 2 個交易日｜kind：realized
  - 來源：—（numbers.earnings_recency，as_of 2026-10-22）
- `f_peer_fix_gross_margin_pct`（q2_moat）｜FIX 毛利率＝25.66 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.FIX.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_fix_operating_margin_pct`（q2_moat）｜FIX 營業利益率＝16.45 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.FIX.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_fix_fcf_margin_pct`（q2_moat）｜FIX FCF 利潤率＝19.24 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.FIX.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_eme_gross_margin_pct`（q2_moat）｜EME 毛利率＝19.43 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.EME.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_eme_operating_margin_pct`（q2_moat）｜EME 營業利益率＝9.6 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.EME.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_eme_fcf_margin_pct`（q2_moat）｜EME FCF 利潤率＝6.3 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.EME.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_iesc_gross_margin_pct`（q2_moat）｜IESC 毛利率＝26.31 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.IESC.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_iesc_operating_margin_pct`（q2_moat）｜IESC 營業利益率＝12.38 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.IESC.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_iesc_fcf_margin_pct`（q2_moat）｜IESC FCF 利潤率＝5.73 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.IESC.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_pwr_gross_margin_pct`（q2_moat）｜PWR 毛利率＝15.46 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.PWR.gross_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_pwr_operating_margin_pct`（q2_moat）｜PWR 營業利益率＝6.12 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.PWR.operating_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_pwr_fcf_margin_pct`（q2_moat）｜PWR FCF 利潤率＝7.27 %｜期間與口徑：TTM ending 2026-06-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.PWR.fcf_margin_pct，as_of TTM ending 2026-06-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝49.03 USD/share｜期間與口徑：2026-10-24／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261024.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-10-24）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝60.22 USD/share｜期間與口徑：2026-10-24／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261024.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-10-24）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝75.95 USD/share｜期間與口徑：2026-10-24／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261024.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-10-24）
- `f_consensus_rev_fy1_pct`（q5_valuation）｜FY1 共識修正＝0.0 %｜期間與口徑：2026-10-24／兩份 Koyfin 快照之間的 EPS 修正幅度（49.03 → 49.03）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261024.xlsx（numbers.consensus_revision.fy1.revision_pct，as_of 2026-10-24）
- `f_consensus_rev_fy2_pct`（q5_valuation）｜FY2 共識修正＝0.0 %｜期間與口徑：2026-10-24／兩份 Koyfin 快照之間的 EPS 修正幅度（60.22 → 60.22）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261024.xlsx（numbers.consensus_revision.fy2.revision_pct，as_of 2026-10-24）
- `f_consensus_rev_fy3_pct`（q5_valuation）｜FY3 共識修正＝0.0 %｜期間與口徑：2026-10-24／兩份 Koyfin 快照之間的 EPS 修正幅度（75.95 → 75.95）｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261024.xlsx（numbers.consensus_revision.fy3.revision_pct，as_of 2026-10-24）
- `f_kpi3_fcf`（q4_capital）｜自由現金流（FCF）＝999.32 USD M｜期間與口徑：Q2 FY2026（季末 2026-06-30，公告於 2026-07-23）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿 8-K Ex.99.1（營業現金流 1,139.4M − 資本支出 141.4M）（numbers.latest_quarter_kpis.items[3]，as_of Q2 FY2026（季末 2026-06-30，公告於 2026-07-23））
  - 註記：查無
- `f_kpi4_sbc`（q4_capital）｜SBC 占營業利益＝1.65 %｜期間與口徑：Q2 FY2026（季末 2026-06-30，公告於 2026-07-23）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：SBC 9.206M 取自 yfinance quarterly_cashflow（新聞稿未揭露），÷ 新聞稿 GAAP 營業利益 557.97M；占營收約 0.28%（numbers.latest_quarter_kpis.items[4]，as_of Q2 FY2026（季末 2026-06-30，公告於 2026-07-23））
  - 註記：n/a
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝0.258 %｜期間與口徑：2026-10-25／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-10-25）
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝1160.86 USD｜期間與口徑：2026-10-23（RTH 收盤，日線 fallback）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-10-23（RTH 收盤，日線 fallback））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝23.68 x｜期間與口徑：2026-10-24／分母＝FY1 EPS 49.03，分子＝快照價 1160.86｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-10-24）
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝0.12 %｜期間與口徑：2026-07-30 → 2026-10-24／FY1 共識 EPS 48.97 → 49.03（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261024.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-10-24）
- `f_ma_state`（q5_valuation）｜週線均線六態（decision_inputs.ma 必須等於此值）＝🟢｜期間與口徑：2026-10-25／timing-appendix §F 週線六態：🟢 價<W52且>W104且三斜率正｜✅ 價>W52>W104>W250且W250斜率>+3%｜🟡 排列過但W250斜率−3~+3%｜🟠 價<W104但>W250｜❌ 價<W250或斜率<−3%｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-10-25）
  - 原文：「price 1160.86 / W52 1463.01 / W104 994.23 / W250 519.55 / W250 13週斜率 4.56%」
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝-32.69 %｜期間與口徑：2026-10-23（RTH 收盤，日線 fallback）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-10-23（RTH 收盤，日線 fallback））
- `f_rsi14`（q5_valuation）｜RSI(14)＝21.05｜期間與口徑：2026-10-23（RTH 收盤，日線 fallback）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-10-23（RTH 收盤，日線 fallback））
- `f_ma_w52`（q5_valuation）｜52 週均線＝1463.01 USD｜期間與口徑：2026-10-25／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-10-25）
- `f_ma_w104`（q5_valuation）｜104 週均線＝994.23 USD｜期間與口徑：2026-10-25／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-10-25）
- `f_ma_w250`（q5_valuation）｜250 週均線＝519.55 USD｜期間與口徑：2026-10-25／週線收盤 SMA（yfinance auto_adjust）｜kind：realized
  - 來源：程式計算：dd_screener_ma.compute_ma_snapshot（yfinance 週線收盤，W52/W104/W250 SMA，W250 斜率＝13 週變化）（ma_snapshot.json，as_of 2026-10-25）

### findings_digest 中方向為負或來源衝突的條目（11 條）
- `competitive_share_entrants#1`（competitive_share_entrants｜方向 -｜狀態 ok）：Zacks 文章列出 FIX 風險包含專案延遲、勞動成本通膨、競爭加劇與執行風險；未量化份額
  - 來源：Nasdaq/Zacks: Comfort Systems Stock Trading at a Premium: Buy, Hold or Fold?（as_of 2026-08-31）｜affects：decision_inputs.bear、thesis.R
- `customer_concentration_credit#0`（customer_concentration_credit｜方向 -｜狀態 ok）：FY2025 10-K：最大單一客戶占 2025 合併營收 12.8%、占 2025/12/31 應收帳款 10.2%；信用風險主要來自總承包商、業主/開發商、商業與工業公司，公司對工程有留置權
  - 來源：SEC EDGAR Comfort Systems USA Form 10-K FY2025 (concentration of credit risk note)，經搜尋摘要轉述，未讀全文（as_of 2026-02-26）｜affects：decision_inputs.bear、thesis.R
- `customer_concentration_credit#2`（customer_concentration_credit｜方向 -｜狀態 ok）：科技（資料中心）相關工程占營收比重：Nasdaq/Zacks 文稱 40%（前一年 31%），另一第三方摘要稱 2025 年約 45%，兩數字口徑不一致
  - 來源：Nasdaq/Zacks: Comfort Systems' Tech and Data Push: Growth or Concentration Risk?（as_of 2025-12-31）｜affects：decision_inputs.bear、thesis.R
- `supply_demand_durability#3`（supply_demand_durability｜方向 -｜狀態 ok）：含資料中心工作的承包商 backlog 比其他承包商長約四個月；2026 年 4 月 backlog 增幅幾乎全來自有資料中心業務的大型承包商，其他規模公司 backlog 皆低於去年；非住宅民間營建支出已連續七個月下滑
  - 來源：contractorplus.app Construction Backlog Indicator April 2026 / Wiss 2026 outlook（as_of 2026-04-30）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：Motley Fool 報導：FIX 在財報風險章節明確點出關稅風險（泛指關稅，非 Section 232 專指）；搜尋摘要另稱公司倚賴鋼、鋁、銅與進口零組件。
  - 來源：Motley Fool, Why Comfort Systems USA Stock Slid 17% Last Month（as_of 2025-03-07）｜affects：decision_inputs.bear、valuation
- `reg_tariff_export#2`（reg_tariff_export｜方向 -｜狀態 ok）：PwC（2026-02-26）：最高法院駁回 IEEPA 關稅後，政府改以其他授權宣布新全球關稅；E&C 產業核心問題是政策波動。摘要稱 2026 年 4 月時鋼鋁銅製品 50%、衍生品 25%、含此類金屬的工業電氣設備（變壓器、配電盤、導管系統）15%，全球基準 10% 至 2026 年 7 月；之後是否變動未確認。
  - 來源：PwC, Building in uncertainty（as_of 2026-02-26）｜affects：decision_inputs.bear、valuation
- `geo_supply_chain#0`（geo_supply_chain｜方向 -｜狀態 ok）：10-K 風險因素：公司、供應商與客戶自外國供應商進口部分原料、零組件與產品；貿易政策變動可能帶來關稅與貿易障礙。
  - 來源：Comfort Systems USA Form 10-K FY2025 (SEC)（as_of 2026-02-20）｜affects：decision_inputs.bear、thesis.R
- `geo_supply_chain#1`（geo_supply_chain｜方向 -｜狀態 ok）：10-K（FY2024）風險因素：若無法將關稅成本轉嫁客戶，經營結果可能受重大不利影響。
  - 來源：Comfort Systems USA Form 10-K FY2024 (SEC)（as_of 2025-02-20）｜affects：decision_inputs.bear、thesis.R
- `geo_supply_chain#2`（geo_supply_chain｜方向 -｜狀態 ok）：公司依賴第三方分包商與設備／材料供應商；供應商未如期履約會損及執行與獲利（一般性依賴，未點名單一供應商或地區）。
  - 來源：Comfort Systems USA Form 10-K FY2025 (SEC)（as_of 2026-02-20）｜affects：decision_inputs.bear、moat_trend
- `geo_supply_chain#3`（geo_supply_chain｜方向 -｜狀態 ok）：風險摘要稱商用 HVAC 設備、配電開關設備、大型發電機交期最長，常超過六個月（第三方彙整 SEC 揭露，非 10-K 原頁讀取）。
  - 來源：policyrisk.com FIX company risk summary（as_of 2026-02-20）｜affects：thesis.R、decision_inputs.bear
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：10-K 風險因素未列出取代其服務的替代技術；列出的替代性威脅是客戶自有員工的內部服務團隊（in-house）與垂直整合帶來的競爭加劇。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A Risk Factors（as_of 2026-02-19）｜affects：moat_trend、decision_inputs.bear

### 事實表自陳的缺口（2 條）
- q2_moat：evidence.numbers.peer_financials 該欄整欄為 null（常見於未單獨揭露研發的業者），事實表 agent 若能從財報補就補，補不到即為缺口，判斷者不得自行估。
- q6_how_wrong：digest.qa_flags 有 4 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/FIX_20261025/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":2310.0,"bear_5y_price":570.0,"p_bull_pct":25,"p_bear_pct":30,"upside_5y_pct":39.1,"ev5y_pct":27.1,"irr_base_pct":6.8,"asym_ratio":1.6,"scenario_tree":{"terminal_label":"FY2030E","start":{"eps":49.03,"pe":23.68,"basis":"FY2026E 共識 EPS（FY1，Koyfin 2026-10-24 快照）；終端倍數同以當年度 EPS 為分母"},"eps":{"bull":[50.6,66.0,82.0,95.0,105.0],"base":[50.2,62.0,72.0,79.0,85.0],"bear":[50.0,58.0,52.0,43.0,38.0]},"pe":{"bull":22,"base":19,"bear":15},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0.258,"net_buyback":0.6},"second_stage":{"bull_cagr_pct":12,"base_cagr_pct":7},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### FIX_Q2_2026_Earnings_Call_20260724.md
- 2026-07-24｜CFO Bill George｜guidance：CFO 預估 2026 全年同店營收成長落在 30% 中後段到 30% 高段（原話："full year increase that is in the mid- to high 30% range"）
- 2026-07-24｜CFO Bill George｜guidance：CFO 表示毛利率可能維持近幾季的高檔區間（原話："gross profit margins are likely to continue"）
- 2026-07-24｜CFO Bill George｜guidance：CFO 預期全年有效稅率約 23%（原話："We expect our full year effective tax rate to be around 23%."）
- 2026-07-24｜CFO Bill George｜guidance：全年資本支出約占營收 5%（原話："CapEx expenditures will be approximately 5% of our revenue"）
- 2026-07-24｜CFO Bill George｜guidance：管理層點出下半年（尤其第四季）比較基期很重（原話："some really, really heavy comparables coming up"）
- 2026-07-24｜President Trent McKenna｜guidance：CFO 說明財測是由現場人力負載由下而上建構（原話："We build it from the bottom up, Julio."）
- 2026-07-24｜CFO Bill George｜guidance：CFO 稱本季現金流除預收款外，沒有單一特殊項目（原話："there's no unique item to point out"）
- 2026-07-24｜CFO Bill George｜margin：剔除上季單次性利得後，Q2 毛利率較 Q1 上升（原話："absent the unique gains that we identified and quantified"）
- 2026-07-24｜CFO Bill George｜margin：機械部門毛利率升至 25.6%（去年同期 22.9%）（原話："Mechanical segment jumped to 25.6%"）
- 2026-07-24｜CFO Bill George｜margin：SG&A 占營收比由 9.7% 降至 8.8%（原話："declined from 9.7% of revenue last year to 8.8% this"）
- 2026-07-24｜CFO Bill George｜margin：CFO 稱專案估計變動的淨利得每年皆有，但本季較平常大（原話："They're bigger this quarter than usual."）
- 2026-07-24｜CFO Bill George｜margin：CFO 稱 2005 年起專案每年都有淨利得（原話："net gain in our jobs every single year ever"）
- 2026-07-24｜CFO Bill George｜margin：Q1 單次性利得口徑：4,300 萬美元超出一般利得範圍（原話："we identified $43 million of gains that"）
- 2026-07-24｜CFO Bill George｜margin：模組化投資報酬被形容為一年到兩年回收（原話："the returns are embarrassing"）
- 2026-07-24｜CFO Bill George｜margin：自由現金流約三分之一來自預收款，其餘為良好績效（原話："might be the advanced cash that we've gotten in the past"）
- 2026-07-24｜CEO Brian Lane｜capital_allocation：季股息調升 0.10 美元至 0.90 美元（原話："quarterly dividend by $0.10 to $0.90 per share"）
- 2026-07-24｜CFO Bill George｜capital_allocation：CFO 表示對自家股票評價看法空前正面，今年上半年買回較去年慢（原話："We like our stock better than we've ever liked it."）
- 2026-07-24｜CEO Brian Lane｜capital_allocation：新收購 Hunt Electric 預計年化營收約 2.5 億美元（原話："contribute about $250 million of annualized revenue"）
- 2026-07-24｜CFO Bill George｜capital_allocation：近期傾向買下廠房而非租賃（原話："We've been tending towards ownership lately"）
- 2026-07-24｜President Trent McKenna｜customer：科技類占上半年營收 58%（去年 40%）（原話："was 58% of our revenue, a substantial increase from 40%"）
- 2026-07-24｜President Trent McKenna｜customer：期末在手訂單創新高 141 億美元（原話："was a record $14.1 billion"）
- 2026-07-24｜President Trent McKenna｜customer：進入第三季時同店在手訂單較去年高 69%（原話："same-store backlog 69% higher than at this time last year"）
- 2026-07-24｜CFO Bill George｜customer：模組化本季新增訂單 5.1 億美元，超過消耗量（原話："Modular had bookings of $510 million."）
- 2026-07-24｜CFO Bill George｜customer：管理層稱建築類在手訂單多數在 18 至 24 個月內消耗（原話："burns on the construction side in the next 18 to 24"）
- 2026-07-24｜President Trent McKenna｜customer：與前沿實驗室及主機代管商有小型試點合約，尚屬早期（原話："some success with some pilot contracts"）
- 2026-07-24｜President Trent McKenna｜customer：與兩家超大規模客戶持續取得量的承諾，並以此支撐擴產（原話："willing to continue to provide us volume commitments"）
- 2026-07-24｜President Trent McKenna｜product：模組化產能預計 2027 夏末達約 500 萬平方呎（原話："5 million square feet of capacity by late summer 2027"）
- 2026-07-24｜President Trent McKenna｜product：資料中心服務商機屬長期，目前受 OEM 保固期影響（原話："it's not an immediate opportunity"）
- 2026-07-24｜President Trent McKenna｜commitment：管理層稱不會憑投機擴建廠房，需客戶多年承諾才擴張（原話："customers provide us meaningful multiyear commitments"）
- 2026-07-24｜CEO Brian Lane｜commitment：CEO 稱只接確定能執行的工作（原話："we only take work that we know we can perform"）
- 2026-07-24｜CFO Bill George｜competition：CFO 稱客戶扶植其他模組化廠商是因需求超過 FIX 產能，並非取代（原話："our customers are not inducing other people to build this to"）
- 2026-07-24｜CFO Bill George｜risk：被問資料中心輿論轉向時，CFO 稱客戶無放緩跡象（原話："so we see no letdown whatsoever"）
- 2026-07-24｜President Trent McKenna｜risk：被問州級暫停令，稱在手訂單多已規劃並取得許可（原話："was already planned, permitted through"）
- 2026-07-24｜President Trent McKenna｜risk：對資料中心輿論阻力的立場：終究會被蓋，地點可能改變（原話："data centers as many as can be built are going to get built"）

### 問答異常語氣（迴避／改口／保留）
- FIX_Q2_2026_Earnings_Call_20260724.md｜問：Goldman 問 10-Q 顯示估計變動對 Q2 營收貢獻約 7.7%、底層毛利率該如何看｜答法：未給底層毛利率數字，改談 2005 年以來歷史與 Q1 的 4,300 萬美元利得口徑；僅承認本季利得較平常大
- FIX_Q2_2026_Earnings_Call_20260724.md｜問：Sidoti 問下半年隱含同店成長約 20% 後段至 30% 出頭，是否可作為 2027 起跑點｜答法：未回答 2027 退出速率，改談財測由下而上編製與第四季比較基期偏重
- FIX_Q2_2026_Earnings_Call_20260724.md｜問：Goldman 問模組化每新增 100 萬平方呎的資本支出｜答法：未給單位資本支出，重申占營收 5% 的指引並稱租購之間仍有彈性
- FIX_Q2_2026_Earnings_Call_20260724.md｜問：Oppenheimer 問超額計費（billings in excess）大幅變動是否來自單一模組化客戶｜答法：未指明是否單一客戶，答為各項現金流因素的總和與客戶信任度

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 3 | 3 |
| customer_second_source | found | 2 | 2 |
| customer_concentration_credit | found | 3 | 3 |
| supply_demand_durability | found | 4 | 3 |
| regulatory_antitrust | found | 2 | 3 |
| reg_tariff_export | found | 4 | 4 |
| geo_supply_chain | found | 5 | 2 |
| end_markets | found | 3 | 3 |
| substitute_technology | found | 1 | 2 |
| channel_business_model_shift | found | 2 | 2 |
| capital_markets_pricing | found | 7 | 4 |
| major_events | found | 2 | 5 |

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20261013","verdict":"觀望","role":"追蹤","H":{"status":"unavailable"},"R":{"status":"unavailable"},"single_thing":null,"kill_metrics":null,"rearm_trigger":"股價 ≤ $1,200（FY27 共識 EPS 約 20 倍）且在手訂單未環比下滑；或 2026Q4 在手訂單 ≥ $16B 且股價 ≤ $1,400 → 重跑 DD","irr_base_pct":1.7,"ev5y_pct":7.1,"drift_watch_prior":{"dca_verdict":"觀望","dca_role":"追蹤","signal":"B","val":"🔴","ma":"✅","trap":"🟡","moat_trend":"↑","runway_post_y5":"🟡","asym_ratio":1.2,"ev5y_pct":7.1,"irr_base_pct":1.7,"max_dd_pct":-65,"bull_5y_price":3042.0,"bear_5y_price":640.0,"p_bull_pct":25,"p_bear_pct":30,"rearm_trigger":"股價 ≤ $1,200（FY27 共識 EPS 約 20 倍）且在手訂單未環比下滑；或 2026Q4 在手訂單 ≥ $16B 且股價 ≤ $1,400 → 重跑 DD","price_at_dd":1638.05,"archetype":"品質複利成長","cycle_position":"晚循環"}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"FIX","date":"2026-10-25","schema":"v15.0","contract":"v19","company_name":"Comfort Systems USA"},"oneliner":"在手訂單 178 億美元已大致鎖住 2027 年中 20% 區間的同店成長，股價十天跌約三成後 FY2027 本益比約 19 倍；代價是週期高點的利潤率與近六成資料中心集中，適合分批，不宜重壓。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/FIX_20261025/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/FIX_20261025/scenario.json","answers":{"q1_business":{"verdict":"賺的是資料中心業主與總承包商的機電施工錢（機械 HVAC／管線＋電氣），九成是專案制；錢卡在技工這一節點：需求超過產業可交付量，誰有人誰拿價。","reasoning":"最新已入表一季（Q2 2026）營收 32.66 億美元、GAAP 營業利益 5.58 億美元（利益率 17.1%），季末在手訂單 140.6 億美元；公司不揭露 non-GAAP 營業利益，也沒有數字財測。2026-10-23 的 Q3 法說逐字稿（事實表未收錄）：營收 38 億美元（年增 54%）、毛利率 24.8%、營業利益率 16.6%、每股盈餘 13.91 美元、在手訂單 178 億美元（年增 90%，環比 +27%，連續八季環比成長）。客戶結構（前九月）：工業 76%（其中科技 59%，去年 42%）、機構 16%、商業 8%；營收型態：新建 75%、既有建物 15%、服務 10%，模組化占 17%。分部：電氣營收年增 85%、毛利率 24.3%（去年 26.2%，剔除去年約 1.8 個百分點一次性利得後約持平），機械年增 43%、毛利率 25.1%（去年 24.3%）；電氣部門有一家子公司占該部門過半營收。單點依賴：最大單一客戶占 2025 營收 12.8%、應收 10.2%（機械部門）；模組化靠兩家超大規模雲端客戶的五年量承諾支撐擴產。這同時是護城河證據（其中一家合作 20 年、重複下單）與集中度風險。供需判斷：週期性，會在資料中心資本支出放緩時反轉；技工供給擴張慢，使反轉前利潤率能維持高檔，但資料中心以外的非住宅民間營建支出已連七月下滑，需求並不全面。產業時鐘判在過熱期：管理層稱限制因素是勞動力不是需求，客戶提早並擴大鎖產能。","fact_refs":["f_kpi0_gaap","f_kpi2_gaap","f_kpi1_non_gaap","f_kpi5","f_kpi6_backlog","f_earnings_recency"],"verdict_values":{"revenue_quality":"專案制占九成，按完工比例認列；專案估計變動每年都是淨利得（CFO：2005 年起每年皆然），分析師引述其對營收的貢獻上半年約 8%、第三季約 4.5%，管理層未否認數字；服務占 10%、第三季年增 13%，是較穩的一塊。","unit_econ_note":"管理層看的單位是每工時毛利，稱持續改善；第三季設備材料占成本比上升約 2 個百分點，拉低毛利率但不減每工時毛利（2026-10-23 法說）。","archetype":{"primary":"品質複利成長","secondary":"循環/商品","confidence":"中","fingerprint":"資本輕、客戶預收款使營運資金為負，獲利由工程景氣與技工供給決定；營業利益率由 FY2022 的 6.09% 升到 FY2025 的 14.42%。"},"industry":{"clock_phase":"III","sd_verdict_source":"週期性將反轉，但反轉時點被在手訂單往後推：管理層稱需求遠超產業可交付量、限制在勞動力（2026-10-23 法說），在手訂單消化期拉長到 18–24 個月；反面是 2026 年 4 月承包商調查顯示訂單增幅幾乎全來自有資料中心業務的大型承包商，非住宅民間營建支出連七月下滑。供給端（技工）可逆性低，需求端（資料中心資本支出）可逆性中等。","bargaining":{"up":"上游設備（商用 HVAC、開關設備、大型發電機）交期常超過六個月，鋼鋁銅受關稅；公司稱大型專案在早期鎖定供應商報價、合約已緩解設備與關稅風險，議價屬中性。","down":"下游是總承包商與超大規模業主；客戶為了鎖產能而提早、擴大下單並接受預收款，FIX 有挑案與條件的空間，這份議價力隨技工稀缺程度變動。","geo":"營運集中在德州、東南部、猶他、愛荷華等州；資料中心暫停令言論可能把工程移往友善州，模組化出貨不受工地州別限制。"},"profit_pool_dir":"利潤池正往握有技工與預製產能的機電承包商移動：FIX 的 TTM 營業利益率 16.45% 對 EME 9.6%、PWR 6.12%；屬可逆移動，取決於技工缺口何時收斂。","tam_table":{"expanded":false,"reason":"事實表未涵蓋 TAM 與滲透率；FIX 的成長限制在勞動力與在手訂單消化速度，不是滲透率，承重數字改看在手訂單與技工人數。"}}}},"q2_moat":{"verdict":"護城河方向向上，但上升的一部分來自技工稀缺這個週期因素：執行面持續拉開，定價面目前強但可逆。","reasoning":"機制：25,000 多名技工＋跨州旅行工班與合約工班（Kodiak、Pivot），加上預製與模組化產能（2026 年底逾 400 萬平方呎、2027 年底約 600 萬），讓 FIX 能在技工稀缺時接下別人做不了的量。可證方向：TTM 營業利益率 16.45% 對最直接對手 EME 9.6%，差 6.85 個百分點；FCF 利潤率 19.24% 對 6.3%。同業 ROIC 與投入資本事實表未涵蓋，只能用利益率差距代理；EME 歷年差距走勢也未涵蓋，無法證明差距在擴大。執行面判擴大：模組化利潤率已追平公司平均、每工時毛利持續改善、客戶重複下單、SG&A 占營收由 9.4% 降到 8.3%。定價面判擴大但可逆：客戶為搶產能提早鎖量，這是週期給的議價力，技工缺口收斂後會回吐。反例：模組化已有新進者以較寬鬆付款條件搶單，大客戶因買不夠而另找供應來源（2026-10-23 法說）；目前是量的外溢，不是份額流失，若變成價格競爭，定價分會先掉。","fact_refs":["f_peer_fix_gross_margin_pct","f_peer_fix_operating_margin_pct","f_peer_fix_fcf_margin_pct","f_peer_eme_gross_margin_pct","f_peer_eme_operating_margin_pct","f_peer_eme_fcf_margin_pct","f_peer_iesc_gross_margin_pct","f_peer_iesc_operating_margin_pct","f_peer_iesc_fcf_margin_pct","f_peer_pwr_gross_margin_pct","f_peer_pwr_operating_margin_pct","f_peer_pwr_fcf_margin_pct"],"verdict_values":{"moat":{"mechanism":"技工規模與跨州調度＋預製／模組化產能＋與超大規模客戶的多年量承諾","execution":9,"pricing":6,"grade":"B","trend":"↑","trend_evidence":"第三季營業利益率 16.6%（去年 15.5%）、機械毛利率 25.1%（去年 24.3%）、在手訂單年增 90%；CFO 稱每工時毛利持續變好。反證：大客戶因 FIX 產能不足另找供應來源、模組化新進者以寬鬆付款條件接單。","competitor_notes":[{"name":"EME","strategy_note":"規模較大、服務範圍更廣，爭取多據點超大規模大單時是最直接對手；TTM 營業利益率 9.6%、FCF 利潤率 6.3%，都明顯低於 FIX。"},{"name":"IESC","strategy_note":"毛利率 26.31% 與 FIX 相近，但營業利益率 12.38%、FCF 利潤率 5.73%，規模與預收款條件不如 FIX。"},{"name":"PWR","strategy_note":"偏電網與輸電，屬間接對手；毛利率 15.46%、營業利益率 6.12%，業務組合不同，不宜直接當定價錨。"}],"peer_na_reason":"事實表未涵蓋同業 ROIC 與投入資本，只能以營業利益率與 FCF 利潤率差距代理。","threats":[{"level":"🟡","text":"EME 規模更大、服務範圍更廣，爭取多據點超大規模大單時有優勢；第三方也點名競爭加劇、勞動成本通膨與執行風險，但未量化份額。","p":"25%","evidence_refs":["competitive_share_entrants#1"]},{"level":"🟡","text":"模組化新進者以 FIX 不接受的付款條件搶單，大客戶因買不夠另找供應來源；目前是需求外溢，需求放緩時會轉成價格競爭。","p":"30%","evidence_refs":[]},{"level":"🟡","text":"客戶自建服務團隊與垂直整合（10-K 列為替代性威脅），主要影響占營收 10% 的服務業務。","p":"15%","evidence_refs":["substitute_technology#0"]},{"level":"🟡","text":"依賴第三方分包商與設備材料供應商，供應商未如期交貨會傷害執行與利潤；未點名單一供應商或地區。","p":"20%","evidence_refs":["geo_supply_chain#2"]}],"roic_durability":{"quadrant":"高利益率×高周轉（推斷：營業利益率 16.45%、客戶預收款使營運資金為負、資產輕；投入資本事實表未涵蓋）","checkpoints":[{"item":"需求基礎值","level":"🟡","text":"使用者是資料中心營運者、決策者是業主與總承包商、付款者多半是全國性總承包商（模組化則由業主直接付款），三角色目前都成立。這是需要而不是想要：延後機電施工就延後整座資料中心上線，代價高；但急迫性不等於持久性，需求綁在超大規模業者的資本支出週期上，科技占營收 59%。"},{"item":"決策層級","level":"🟡","text":"替代性要在單一專案層級看：每案仍是比價投標，換承包商的成本不高；可觀察的黏著是模組化客戶合作 20 年與五年量承諾、重複下單、客戶為搶產能提早鎖量。這份黏著有一部分是稀缺造成的，產能寬鬆後會回到逐案比價。"},{"item":"價值鏈分配","level":"🟡","text":"整條鏈上晶片與設備（開關設備、冷卻、發電機交期逾六個月）拿走大部分價值，FIX 處在設計的晚段；目前技工是最難取代的環節，所以 FIX 分到超常份額（毛利率 24.8%、營業利益率 16.6%，EME 營業利益率 9.6%）。技工缺口收斂後，分配會往設備端與業主端回流。"},{"item":"社會容忍度","level":"🟡","text":"各州對資料中心用電、用水的反彈與選前暫停令言論已出現；管理層稱尚未看到任何專案延後，工程可能移往友善州，模組化不受工地州別影響（2026-10-23）。FIX 不靠監管授權，價格天花板不是主要問題，風險在需求被政策壓縮。"}],"roiic":"事實表未涵蓋投入資本；以模組化擴產一到兩年回本（2026-07-24 法說）與預收款使營運資金為負推估，增量報酬保守取約 45%","reinvest_rate":"約 35%：資本支出占營收 4–5%（2026 年約 5.4–6.7 億美元）扣折舊約 1.7 億，加上小型併購，除以約 17.5 億美元稅後營業利益；預收款帶來的營運資金流入未扣除","endo_ceiling":15,"formula_note":"內生成長參考值＝增量報酬約 45% × 再投資率約 35% ≈ 15%。FIX 的成長實際受技工人數而非資本限制，且客戶預收款墊資，這個數字是不靠利潤率擴張、不靠預收款時的成長參考，不是硬上限。"}}}},"q3_growth":{"verdict":"五年後跑道中等：在手訂單蓋到 2028 年，之後要看資料中心資本支出是否延續，沒有已證實的第二條曲線。","reasoning":"成長組成：量（在手訂單、技工人數擴張）為主，價（每工時毛利）次之，小型併購每年貢獻約 2–4% 營收（Hunt 約 2.5 億、Boys 與 NeoPod 合計逾 1 億、Feyen Zylstra 與 Meisner 2.0–2.4 億），回購約 0.6%。共識三年 EPS 年化：FY2025 實際 28.88 → FY2028E 75.95 為 38.0%；扣掉 2026 年利潤率跳升，FY2026E→FY2028E 為 24.5%（Koyfin 快照，家數未揭露；兩份快照間修正為 0，可能尚未反映第三季超出）。內生參考值約 15%（引護城河段）。缺口歸因：2026 年營業利益率由 14.4% 升到約 16.5% 的利潤率擴張、併購、以及客戶預收款墊資（公式未計）；三者可解釋大部分，剩下的依賴資料中心週期延續。跑道：在手訂單 178 億美元、消化 18–24 個月，覆蓋 2027 年大部分與 2028 年一部分營收；2027 同店成長口徑中 20% 區間。五年後沒有已證實的第二條曲線：服務只占 10%、年增 13%，模組化新客戶（前沿實驗室、主機代管商）尚未成為多年合約。衰退信號亮一個：EPS 年化成長遠高於營收。","fact_refs":["f_kpi6_backlog","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_fy1_pct","f_consensus_rev_fy2_pct","f_consensus_rev_fy3_pct"],"verdict_values":{"growth":{"driver_mix":"量為主（在手訂單消化、技工擴編）＋價（每工時毛利改善）＋小型併購約 2–4%／年＋淨回購約 0.6%／年","runway_years":"5–7（以在手訂單 18–24 個月消化期加上資料中心建置能見度推估，非滲透率口徑）","runway_post_y5":"🟡","endo_ceiling_basis":"引護城河段再投資推導：增量報酬約 45% × 再投資率約 35% ≈ 15%","segments":[{"item":"機械部門營收年增（Q3 2026）","value":"43%，毛利率 25.1%（去年 24.3%）"},{"item":"電氣部門營收年增（Q3 2026）","value":"85%，毛利率 24.3%（去年 26.2%，剔除一次性利得約持平）"},{"item":"科技（資料中心）占前九月營收","value":"59%（去年 42%）"},{"item":"工業客戶占前九月營收","value":"76%"},{"item":"機構（教育、醫療、政府）占營收","value":"16%"},{"item":"商業占營收","value":"8%"},{"item":"模組化占營收","value":"17%；產能 2026 年底逾 400 萬、2027 年底約 600 萬平方呎"},{"item":"服務占營收","value":"10%，第三季年增 13%"}],"decay_signals":["EPS 成長顯著高於營收：FY2022→FY2025 EPS 年化 61.8% 對營收 30.0%，亮","毛利率連兩季年減：未亮，第三季 24.8% 與去年持平","自由現金流／淨利低於 0.75：未亮，第三季 8.06 億對 4.89 億","SBC 占營收超過 5%：未亮，約 0.28%","核心市占縮減：事實表未涵蓋份額數據","產業估值倍數系統性下移：事實表未涵蓋"]}}},"q4_capital":{"verdict":"現金產生能力強但被預收款墊高，配置紀律中上：SBC 很低、股數淨減，併購報酬無法驗證，回購盈餘殖利率偏低。","reasoning":"自由現金流：Q2 2026 為 9.99 億美元，高於同季 GAAP 營業利益 5.58 億；Q3 為 8.06 億對淨利 4.89 億（1.65 倍）。這不是常態：Q2 法說稱約三分之一來自客戶預收款，Q3 另有 1.66 億美元稅款遞延到第四季；預收款隨工程進度回吐時，自由現金流／淨利會掉到 1 倍以下，正常化以約 1 倍看。SBC 只占營收約 0.28%、占營業利益 1.65%，年初至今註銷約 21.2 萬股。現金去向：資本支出（全年占營收 4–5%，擴模組化與預製廠，2027 上半年仍偏高，近期傾向自購廠房）、小型併購、回購（歷來用 15–20% 的自由現金流，第三季花 2 億美元，股價弱時加碼）、股息（季配調升到每股 1 美元）；年初至今回饋股東 3.49 億美元。","fact_refs":["f_kpi3_fcf","f_kpi4_sbc","f_kpi2_gaap","f_dividend_yield_ttm"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":true,"passed":null,"input":"近一年收購 Feyen Zylstra 與 Meisner（預期年營收 2.0–2.4 億美元、EBITDA 0.15–0.2 億美元）、Hunt（年化營收約 2.5 億）、Boys 與 NeoPod（合計逾 1 億）；收購價皆未揭露，已實現增量報酬無法計算。"},{"name":"buyback_yield","applicable":true,"passed":false,"input":"第三季回購約 2 億美元；以 FY2026 共識 EPS 49.03 計，即使按現價 1,160.86 盈餘殖利率也只約 4.2%，當季實際買價更高；10 年期殖利率事實表未涵蓋，需 ≤2.2% 才達標，判為未過。"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"SBC 約占營收 0.28%、占營業利益 1.65%；年初至今註銷約 21.2 萬股，淨股數下降。"}]},"governance":{"capital_returns":{"expanded":false,"reason":"併購每年只貢獻約 2–4% 營收，成長主要靠在手訂單消化與技工擴編，不是靠併購撐。"}}}},"q5_valuation":{"verdict":"現價要求 2027 年 EPS 達到共識、2028 年後利潤率不大幅回落才划算；前半我信（在手訂單已覆蓋），後半只給中等信心，判為合理區間。","reasoning":"現價 1,160.86 美元，對 FY2026 共識 EPS 49.03 為 23.7 倍、FY2027 60.22 為 19.3 倍、FY2028 75.95 為 15.3 倍；FY2026 共識近三個月只上修 0.12%。PEG：FY2025 實際 28.88→FY2028E 三年年化 38.0%，以 23.7 倍計為 0.62；扣掉 2026 年利潤率跳升，FY2026E→FY2028E 年化 24.5%，PEG 0.97。五年分位數：事實表只有最近一點本益比，未涵蓋五年高低，不計。賣方目標價（7–9 月，平均約 1,974–2,114 美元、最高 2,400）全部早於本月股價下跌，高低倍數比約 1.3，不當錨。短期上檔：FY2027E 60.22×21 倍＝1,265 美元，+8.9%；中期：FY2028E 75.95×19 倍＝1,443 美元，+24.3%。股息殖利率 0.26%（季配調升後約 0.34%）。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_consensus_rev_3m_fy1_pct","f_dividend_yield_ttm","f_ma_state"],"verdict_values":{"valuation":{"basis":"前瞻本益比（FY2026E／FY2027E 共識 EPS）為主尺，PEG 為輔","peers":{"expanded":false,"reason":"事實表只有同業利益率，未涵蓋同業前瞻本益比；終端倍數無法附同業現值對照，改以 FIX 自身現價倍數與成長熄火情境定錨。"},"fwd_pe":23.68,"peg":0.62,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"FY2027 本益比 19.3 倍、PEG 0.6–1.0 落在合理偏便宜；但分子是週期高點利潤率（營業利益率四年由 6.1% 升到 16.6%），若回到 FY2024 的 10.6%，同營收下 FY2026 倍數約 37 倍，所以只判合理，不判便宜。","upside_short_pct":8.9,"upside_mid_pct":24.3,"denominator_disputed":false,"denominator_note":"分母有兩個爭議源：專案估計變動利得（上半年約占營收 8%、第三季 4.5%）與週期高點利潤率。前者 2005 年起年年發生，且第三季占比下降時毛利率仍持平，不算一次性；後者是持續期問題，放進空方機率與終端倍數處理，不改分母。"}}},"q6_how_wrong":{"verdict":"最可能看錯的是把週期高點利潤率當成新常態；其次是本月股價下跌的原因不明。","reasoning":"依據見反證紀錄：論點失敗兩條（資料中心訂單反轉、下跌原因不明）、股東經濟變差一條（預收款回吐與成本壓縮）、價格反映太多一條（高點利潤率下的倍數）。價值陷阱信號亮一個（EPS 成長遠快於營收），判中度風險。股價 1,160.86 美元、26 週 −32.7%、RSI 21，跌破 52 週均線 1,463，仍在 104 週均線 994 與 250 週均線 520 之上。","fact_refs":["f_price_at_dd","f_week26_return_pct","f_rsi14","f_ma_w52","f_ma_w104","f_ma_w250"],"verdict_values":{"trap":{"verdict":"🟡","label":"週期高點利潤率"}}}},"scenario_inputs":{"terminal_label":"FY2030E","start":{"eps":49.03,"pe":23.68,"basis":"FY2026E 共識 EPS（FY1，Koyfin 2026-10-24 快照）；終端倍數同以當年度 EPS 為分母"},"eps":{"bull":[50.6,66.0,82.0,95.0,105.0],"base":[50.2,62.0,72.0,79.0,85.0],"bear":[50.0,58.0,52.0,43.0,38.0]},"pe":{"bull":22,"base":19,"bear":15},"p":{"bull":25,"base":45,"bear":30},"yield_pct":{"dividend":0.34,"net_buyback":0.6},"second_stage":{"bull_cagr_pct":12,"base_cagr_pct":7},"max_dd":{"lo":-60,"hi":-45,"basis":"空方終點約 570 美元（38×15），較現價約 −51%；250 週均線 519.55 美元約 −55%；本月十天內由 1,638 跌到 1,161（約 −29%）是實際波動參考；下緣 −60% 對應資料中心訂單反轉疊加倍數壓到 14 倍、EPS 回到 FY2025 約 29 美元的組合。歷史最大回撤事實表未涵蓋。","trigger_time":null},"basis":{"bull":"資料中心建置延續到 2029 年以後、模組化新客戶轉成多年合約，營收年增 20% 以上到 2028、之後約 10%；營業利益率守在 16–17%；終端 22 倍。","base":"2026 年 50.2（共識 49.03 加上第三季超出約 1.18）、2027 依中 20% 區間成長到 62；在手訂單消化後 2028 起放緩到 16%、10%、8%，利潤率持平；終端 19 倍，低於現價 23.7 倍以反映成長放緩。","bear":"2027 年仍有在手訂單撐到 58，2028 起資料中心資本支出收縮、利潤率往同業回落（營業利益率約 11–12%），2030 年 EPS 38；終端 15 倍為成長熄火到 10% 情境的倍數。"},"endo_ceiling_exceeded":true},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"科技占前九月營收 59%（去年 42%）；2026 年 4 月承包商調查顯示訂單增幅幾乎全來自有資料中心業務的大型承包商，其他規模承包商在手訂單低於去年、非住宅民間營建支出連七月下滑；第三方估科技工程占比 40–45%，口徑不一。","assumption":"資料中心資本支出至少延續到 2028 年。","consequence":"2028 年起訂單斷層，營收下滑、利潤率回落到同業水準，EPS 回到 30–40 美元、倍數壓到 14–15 倍，五年後股價約 −50%。","ruling":"部分採納：寫進 30% 空方機率與唯一致命點；反駁的是時點，在手訂單消化 18–24 個月，反轉最早反映在 2028 年財報。","watch":"季末在手訂單環比、科技營收占比、超大規模業者資本支出口徑。","evidence_refs":["supply_demand_durability#3","customer_concentration_credit#2"],"fact_refs":["f_kpi6_backlog"]},{"view":"論點失敗","evidence":"股價由 2026-10-13 的 1,638 美元跌到 10-23 的 1,160.86 美元（約 −29%），26 週 −32.7%、RSI 21；同期第三季財報超過共識、在手訂單創新高。事實表未涵蓋下跌原因。","assumption":"下跌是情緒或產業輪動，不是尚未公開的基本面利空。","consequence":"若是客戶端資本支出下修或大客戶變動的先行反應，第四季財報才會看到，屆時已加碼的部位會被套住。","ruling":"不可裁決至 2026 年第四季財報（2027 年 2 月）：首筆只建三分之一，FY2027 共識 EPS 三個月內下修 ≥5% 就凍結加碼。","watch":"FY2027 共識 EPS 修正、第四季在手訂單。","evidence_refs":[],"fact_refs":["f_week26_return_pct","f_rsi14","f_consensus_rev_fy2_pct"]},{"view":"論點成功但股東經濟變差","evidence":"自由現金流約三分之一來自預收款（2026-07-24），第三季另有 1.66 億稅款遞延；資本支出升到營收 4–5% 並傾向自購廠房；10-K 稱關稅成本若無法轉嫁會重大不利；2026 年鋼鋁銅製品關稅 50%、含金屬電氣設備 15%；第三方點名勞動成本通膨與競爭加劇。","assumption":"營收成長時每股自由現金流同步成長。","consequence":"營收照預期成長，但預收款回吐、資本密度上升、人工與材料成本吃掉利潤率，每股自由現金流停滯，股價跟著倍數往下。","ruling":"採納為監測項，不進主情境：管理層稱大型專案早期鎖定供應商報價、合約已緩解關稅風險，第三季毛利率持平；但自由現金流／淨利以約 1 倍為正常化基準，不用第三季的 1.65 倍。","watch":"TTM 自由現金流／淨利低於 0.75、毛利率連兩季年減 ≥1 個百分點。","evidence_refs":["geo_supply_chain#1","reg_tariff_export#2","competitive_share_entrants#1"],"fact_refs":["f_kpi3_fcf"]},{"view":"價格已反映太多","evidence":"營業利益率四年由 6.1% 升到 16.6%；以 FY2026 共識 EPS 計本益比 23.7 倍，若利益率回到 FY2024 的 10.6%，同營收下倍數約 37 倍。","assumption":"現有利潤率可以維持五年。","consequence":"即使業務不衰退，利潤率正常化就足以讓股價橫盤數年。","ruling":"部分反駁：FY2027 本益比 19.3 倍、FY2028 15.3 倍，而這兩年營收大半已在在手訂單內；利潤率正常化風險已放進空方與終端 19 倍，不再對現價加碼折扣。","watch":"2027 上半年毛利率是否如 CFO 所說回到平均；每工時毛利。","evidence_refs":[],"fact_refs":["f_fwd_pe_latest","f_consensus_eps_fy2","f_consensus_eps_fy3"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 ✅ → 本次 🟢","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=✅","side_b":"本次 ma=🟢","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 1638.05 → 本次 1160.86（-29.1%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=1638.05","side_b":"本次 price_at_dd=1160.86","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]裁決由 dd_decision.py 機械路由：前份 觀望 → 本次 進場","cause":"價格變動","prior_field":["dca_verdict"],"side_a":"前份 dca_verdict=觀望","side_b":"本次 dca_verdict=進場","ruling":"裁決是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。單獨改回前份值即還原前份裁決：估值 🔴→🟡。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]角色由 dd_decision.py 機械路由：前份 追蹤 → 本次 衛星","cause":"價格變動","prior_field":["dca_role"],"side_a":"前份 dca_role=追蹤","side_b":"本次 dca_role=衛星","ruling":"角色是矩陣輸出，判斷者寫稿時看不到；變動原因由程式反事實歸因（逐一把矩陣輸入改回前份值重算）。單獨改回前份值即還原前份角色：估值 🔴→🟡。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 1,638.05 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 1,638.05 美元：Bull 價 3,042、Bear 價 640，五年期望值 +7.1%，基準年化 1.7%，不對稱比 1.2","side_b":"本次情境、股價仍用 1,638.05 美元：Bull 價 2,310、Bear 價 570，五年期望值 −9.9%，基準年化 −0.3%，不對稱比 0.52","ruling":"先換情境、股價不動：五年期望值少 17.0 個百分點，基準年化少 2.0 個百分點。不對稱比由 1.2 變為 0.52。Bull、Bear 價位與股價無關，只受情境影響。情境樹重建本身讓期望報酬變差。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 1,638.05 美元：五年期望值 −9.9%，基準年化 −0.3%，不對稱比 0.52","side_b":"本次情境、股價 1,160.86 美元：五年期望值 +27.1%，基準年化 6.8%，不對稱比 1.62","ruling":"再換股價、情境不動：起點價下跌 29.1%，五年期望值多 37.0 個百分點，基準年化多 7.1 個百分點，不對稱比由 0.52 升到 1.62。合計五年期望值比前份多 20.0 個百分點。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"前份漂移：價格與估值","cause":"價格變動","prior_field":["val","max_dd_pct","p_bull_pct","p_bear_pct"],"side_a":"前份 2026-10-13：股價 1,638.05 美元、FY2026 本益比約 33 倍、估值偏貴；最大回撤 −65%；多方 25%、空方 30%；觀望。","side_b":"本次股價 1,160.86 美元（−29%），FY2026 23.7 倍、FY2027 19.3 倍，估值轉為合理；回撤區間 −45%～−60%（起點已低，空方終點約 570 美元與前份 640 美元相近）；機率維持多 25%、基準 45%、空方 30%；裁決與角色依本次輸入重新路由。","ruling":"估值結論的改變全部來自股價，FY2026 共識 EPS 近三月只動 +0.12%；機率不變，因為新證據（訂單與財測上修）與新風險（下跌原因不明、毛利率環比回落、財務長退休）互相抵銷。","evidence_level":"價格與共識快照（硬數據）","settle_metric":"股價對 FY2027 共識本益比","if_then":["若股價回到 FY2027 本益比 25 倍以上（約 1,505 美元）而第四季數據未到，不追"],"evidence_refs":[]},{"axis":"前份漂移：基本面判斷維持","cause":"新證據","prior_field":["signal","trap","moat_trend","runway_post_y5","archetype","cycle_position"],"side_a":"前份：綜合訊號 B、價值陷阱中度、護城河向上、五年後跑道中等、品質複利成長、晚循環。","side_b":"本次全部維持：第三季新證據（在手訂單 178 億、全年同店成長上調到 40% 中段、模組化產能目標上調到約 600 萬平方呎）強化向上方向，但同時出現大客戶另找供應來源、毛利率環比回落、財務長退休，抵銷後不改任何一欄。","ruling":"維持；若 2027 上半年毛利率回到 24% 以上且模組化新客戶簽成多年合約，跑道可升一級。","evidence_level":"公司財報與法說","settle_metric":"2027 上半年毛利率；模組化新客戶合約型態","if_then":["若模組化新客戶簽成多年量承諾，五年後跑道上調一級","若在手訂單連兩季環比下滑，護城河方向改判持平並重跑判斷"],"evidence_refs":[]},{"axis":"前份漂移：重跑條件與加碼門檻","cause":"新證據","prior_field":["rearm_trigger"],"side_a":"股價 ≤ $1,200（FY27 共識 EPS 約 20 倍）且在手訂單未環比下滑；或 2026Q4 在手訂單 ≥ $16B 且股價 ≤ $1,400 → 重跑 DD","side_b":"2026Q4 財報在手訂單 ≥170 億美元且毛利率 ≥23%，或股價 ≤$1,000 且在手訂單未環比下滑 → 進場／加碼並重跑判斷","ruling":"前份條件已觸發（股價 1,160.86 ≤ 1,200，在手訂單由 140.6 億升到 178 億），本次即為重跑；新門檻改為加碼條件：在手訂單門檻由 160 億提高到 170 億以反映新基期，價位由 1,200 降到 1,000（FY2027 約 16.6 倍、接近 104 週均線 994），因為下跌原因不明，加碼需要更大的安全邊際。","evidence_level":"公司財報（硬數據）","settle_metric":"2026 年第四季在手訂單與毛利率","if_then":["若第四季在手訂單 ≥170 億且毛利率 ≥23%，加碼到目標倉位三分之二"],"evidence_refs":[]},{"axis":"前份漂移：減碼與清倉門檻","cause":"方法變動","prior_field":["kill_metrics"],"side_a":"前份未登記減碼／清倉指標（null）","side_b":"在手訂單連兩季環比下滑或低於 140 億→減碼一半；季毛利率連兩季低於 22%→減碼一半；2027 同店成長低於 15%；最大客戶營收占比超過 15% 或應收超過 20%；TTM 自由現金流／淨利低於 0.75；主要模組化客戶縮減多年承諾→清倉。","ruling":"前份摘要沒有可對照的指標，本次依新格式補齊；門檻取本季實際值與公司口徑的下緣。","evidence_level":"公司財報與 10-K","settle_metric":"各指標每季讀數","if_then":["若任一減碼門檻觸發，減碼一半並重跑判斷"],"evidence_refs":[]},{"axis":"前份漂移：Single Thing","cause":"方法變動","prior_field":["single_thing"],"side_a":"前份未登記唯一致命點（null）","side_b":"兩家模組化合約客戶任一家縮減或延後五年量承諾，或最大科技客戶大幅下修資料中心資本支出並延後 FIX 承接的專案。","ruling":"前份摘要該欄為空；本次 Single Thing 取數學上最大的單一敏感項：科技客戶占營收 59%、模組化產能投資以兩家客戶承諾為前提，任一縮減同時打到營收、利潤率與新廠回收，發生即清倉。","evidence_level":"法說與 10-K","settle_metric":"模組化量承諾、季末在手訂單","if_then":["若任一模組化客戶公開縮減承諾，清倉"],"evidence_refs":[]},{"axis":"股價方向與基本面方向","cause":"新證據","side_a":"現在就買的最強論證：第三季每股盈餘 13.91 美元超過共識、在手訂單環比 +27% 到 178 億、全年同店成長口徑由 30% 中後段上調到 40% 中段、2027 給出中 20% 區間；股價卻跌三成，FY2027 只剩 19 倍，前份設定的重跑條件已觸發。","side_b":"現在就賣的最強論證：十天跌 29% 而財報很好，代表市場在定價財報以外的東西，可能是資料中心資本支出見頂或高點利潤率回吐；第三季毛利率環比下滑、財務長宣布退休，事實表未涵蓋真正原因，接刀的風險在原因不明。","ruling":"不可調和（方向相反），選基本面側但降低力度：178 億已簽約在手訂單是硬數據，2027 年營收大半已入袋，股價下跌原因不明不等於基本面受損。執行：首筆三分之一，第四季數據確認後才加碼。","evidence_level":"公司財報與法說（硬數據）對上股價（原因未知）","settle_metric":"2026 年第四季在手訂單與毛利率；FY2027 共識 EPS 修正","if_then":["若 2027 年 2 月第四季在手訂單 ≥170 億美元且毛利率 ≥23%，加碼到目標倉位三分之二","若股價續跌但在手訂單未環比下滑，分批反買，不停損","若股價先反彈到 FY2027 本益比 25 倍以上而第四季數據未到，不追","若 FY2027 共識 EPS 三個月內下修 ≥5% 或在手訂單環比下滑，停止加碼；連兩季下滑減碼一半"],"evidence_refs":[]},{"axis":"利潤率是結構還是週期","cause":"新證據","side_a":"結構：模組化利潤率追平公司平均、每工時毛利改善、SG&A 占營收由 9.4% 降到 8.3%、服務利潤創高。","side_b":"週期：營業利益率四年由 6.1% 升到 16.6%，與資料中心訂單同步；專案估計變動利得上半年約占營收 8%；電氣部門一家子公司毛利率曾到 30% 以上。","ruling":"可調和（程度差異）：拆成結構（營運槓桿與模組化規模，約對應 SG&A 下降的 1 個百分點）、週期（技工稀缺帶來的定價）與殘差（估計變動利得）；週期與殘差合計估占營業利益率 4–6 個百分點，放進 30% 空方機率與 19 倍終端倍數。","evidence_level":"公司財報與法說；拆分比例為估計","settle_metric":"2027 上半年毛利率；專案估計變動利得占營收比","if_then":["若 2027 上半年毛利率 ≥24% 且估計變動利得占營收低於 5%，結構占比上調，空方機率可降到 25%","若毛利率連兩季低於 22%，視為週期回吐開始，減碼一半"],"evidence_refs":[]},{"axis":"管理層前後口徑","cause":"新證據","side_a":"2026-07-24（CFO Bill George、總裁 Trent McKenna）：全年同店成長 30% 中後段、資本支出約占營收 5%、毛利率維持近幾季高檔、模組化 2027 夏末約 500 萬平方呎；稱客戶扶植其他模組化廠商不是要取代 FIX。","side_b":"2026-10-23：同店成長上調到 40% 中段、2027 中 20% 區間、資本支出 4–5%、模組化 2027 年底約 600 萬平方呎；但機械毛利率由 25.6% 降到 25.1%，CFO 首次說大客戶因買不夠而另找供應來源。","ruling":"可調和：財測全部兌現且上調，信用加分；毛利率小幅回落有具體解釋（設備材料占比 +2 個百分點、收購價格調整多 1,200 萬美元、早期工程保留準備），但屬一次性歸因，標為未證、監測。","evidence_level":"兩季法說逐字稿","settle_metric":"2027 上半年毛利率","if_then":["若 2027 上半年毛利率 ≥24%，管理層歸因成立","若 2027 上半年連兩季低於 23.5%，歸因失效，停止加碼"],"evidence_refs":[]},{"axis":"產業態勢","cause":"新證據","side_a":"結構轉好：在手訂單八季連續環比成長、需求超過產業可交付量、客戶提早並擴大鎖產能。","side_b":"競爭面：模組化新進者以寬鬆付款條件接單；其他結構變數：鋼鋁銅關稅 50%、含金屬電氣設備 15%、各州資料中心暫停令言論。","ruling":"雙向拉鋸，偏結構轉好：結構面有硬數據（178 億在手訂單），競爭與政策面目前只見言論與條件競爭，管理層稱未見專案延後或利潤率因此下滑（2026-10-23）。","evidence_level":"公司財報對上第三方與政策摘要","settle_metric":"專案延後揭露、毛利率","if_then":["若管理層揭露任一專案因州級法規延後，停止加碼並重跑判斷"],"evidence_refs":["reg_tariff_export#2"]}],"triggers":[{"n":1,"text":"在手訂單是否維持 150 億美元以上，並轉成 2027 年中 20% 區間的同店成長","type":"假設驗證","maps_to":"H1","metric":"季末在手訂單；同店營收年增","threshold":"在手訂單 ≥150 億美元；2027 同店年增 ≥20%","action":"兩項達標維持持股；任一不達標停止加碼","source_freq":"季報新聞稿（每季）","date":"2027-02","evidence_refs":[]},{"n":2,"text":"毛利率在工程進入中後段後回到 24% 以上","type":"假設驗證","maps_to":"H2","metric":"季毛利率","threshold":"季毛利率 ≥22%；2027 上半年回到 ≥24%","action":"連兩季低於 22% 減碼一半","source_freq":"季報（每季）","date":"2027-07","evidence_refs":[]},{"n":3,"text":"資料中心訂單放緩：在手訂單連兩季環比下滑","type":"風險","maps_to":"R1","metric":"季末在手訂單環比","threshold":"連 2 季環比下滑，或低於 140 億美元","action":"減碼一半並重跑判斷","source_freq":"季報新聞稿（每季）","date":null,"evidence_refs":["supply_demand_durability#3","customer_concentration_credit#2"]},{"n":4,"text":"主要模組化客戶縮減或延後五年量承諾","type":"Single Thing","maps_to":"single_thing","metric":"法說揭露的模組化量承諾與訂單","threshold":"任一家公開縮減、延後或不續約","action":"清倉","source_freq":"法說會（每季）與公司公告","date":null,"evidence_refs":[]},{"n":5,"text":"價格回到 FY2027 本益比約 16.6 倍且訂單未轉弱","type":"估值rearm","maps_to":"rearm","metric":"股價；季末在手訂單環比","threshold":"股價 ≤1,000 美元且在手訂單未環比下滑","action":"加碼到目標倉位三分之二","source_freq":"每日股價＋季報","date":null,"evidence_refs":[]},{"n":6,"text":"倍數重新拉高而共識未跟上","type":"減碼","maps_to":"H1","metric":"FY2027 共識本益比","threshold":"高於 28 倍（約 1,690 美元）且共識 EPS 未上修","action":"減碼三分之一","source_freq":"每日股價＋共識快照","date":null,"evidence_refs":[]},{"n":7,"text":"成本端吸收失敗：關稅、長交期設備或人工成本無法轉嫁","type":"風險","maps_to":"R3","metric":"毛利率年變動；管理層歸因","threshold":"毛利率連 2 季年減 ≥1 個百分點且歸因材料或人工成本","action":"停止加碼；連 3 季則減碼一半","source_freq":"季報與法說（每季）","date":null,"evidence_refs":["reg_tariff_export#0","reg_tariff_export#2","geo_supply_chain#0","geo_supply_chain#1","geo_supply_chain#3"]},{"n":8,"text":"財務長交棒後的執行與併購紀律","type":"風險","maps_to":"R5","metric":"實際營收與毛利率對公司口徑；高層異動","threshold":"交棒後兩季內實際低於公司口徑，或另有高層離職","action":"停止加碼並重跑判斷","source_freq":"季報與公司公告","date":"2027-08","evidence_refs":[]},{"n":9,"text":"下跌原因若是尚未公開的利空，會先出現在共識下修","type":"風險","maps_to":"R1","metric":"FY2027 共識 EPS 三個月修正","threshold":"下修 ≥5%","action":"凍結加碼","source_freq":"共識快照（每月）","date":null,"evidence_refs":[]},{"n":10,"text":"客戶集中惡化","type":"風險","maps_to":"R4","metric":"最大單一客戶占營收與應收","threshold":"營收占比超過 15% 或應收占比超過 20%","action":"停止加碼","source_freq":"10-K（每年）","date":"2027-02","evidence_refs":["customer_concentration_credit#0"]},{"n":11,"text":"2026 年第四季財報與 2027 財測後重新檢視","type":"複審日期","maps_to":null,"metric":"在手訂單、毛利率、2027 同店成長口徑","threshold":"財報公布","action":"重跑判斷","source_freq":"一次性","date":"2027-02","evidence_refs":[]}],"kill_metrics":[{"metric":"季末在手訂單（環比）","bear_threshold":"連 2 季環比下滑，或低於 140 億美元","window":"2 季","source":"公司季報新聞稿","last_status":"ok"},{"metric":"季毛利率","bear_threshold":"連 2 季低於 22%","window":"2 季","source":"公司季報","last_status":"ok"},{"metric":"2027 年同店營收年增","bear_threshold":"低於 15%","window":"FY2027","source":"公司財測與年報","last_status":"unknown"},{"metric":"最大單一客戶占營收／應收","bear_threshold":"營收占比超過 15% 或應收占比超過 20%","window":"每年年報","source":"10-K 信用集中附註","last_status":"ok"},{"metric":"TTM 自由現金流／淨利","bear_threshold":"低於 0.75","window":"4 季","source":"公司季報現金流量表","last_status":"ok"}],"evidence_dismissed":[],"action_conditions":{"rearm_trigger":"2026Q4 財報在手訂單 ≥170 億美元且毛利率 ≥23%，或股價 ≤$1,000 且在手訂單未環比下滑 → 進場／加碼並重跑判斷","exec_line":"首筆建立目標倉位三分之一；2027 年 2 月第四季在手訂單 ≥170 億且毛利率 ≥23%，或股價 ≤1,000 且在手訂單未環比下滑，加碼到三分之二；FY2027 共識 EPS 三個月內下修 ≥5% 凍結加碼；在手訂單連兩季環比下滑減碼一半；主要模組化客戶縮減承諾清倉。","holding_cap":"目標倉位上限 5%，第四季確認前 ≤2%"}},"decision_inputs":{"signal":"B","ma":"🟢","cycle_position":"晚循環","cycle_verdict":"右側可追蹤","thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":"市場用週期見頂的倍數定價（FY2027 本益比 19 倍、FY2028 15 倍），但在手訂單 178 億美元、消化 18–24 個月，2027 年營收大部分已簽約；即使週期反轉，最早落在 2028 年財報。此為推論，事實表未涵蓋本月下跌原因。","momentum_overheated":false,"cycle_gates_pass":null,"qc49_inherit_prior":false,"wait_for_price":null,"wait_for_price_condition":null,"asym_ratio":null,"irr_base_pct":null,"ev5y_pct":null},"decision_out":{"verdict":"進場","role":"衛星","row_hit":"9","audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='↑', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟢'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=市場用週期見頂的倍數定價（FY2027 本益比 19 倍、FY2028 15 倍），但在手訂單 178 億美元、消化 18–24 個月，2027 年營收大部分已簽約；即使週期反轉，最早落在 2028 年財報。此為推論，事實表未涵蓋本月下跌原因。"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟡', moat_trend='↑', week26=-32.69, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position='晚循環', moat='B', moat_trend='↑', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":false,"basis":"signal='B', val='🟡'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":true,"basis":"signal='B', val='🟡', ma='🟢'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟡', ma='🟢'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟡', ma='🟢'"},{"row":"9-verdict","condition":"命中 row9 → 進場","hit":true,"basis":"row_hit=9"},{"row":"QC-49","condition":"qc49_inherit_prior=False，不套用","hit":false,"basis":"qc49_inherit_prior=False"}],"pacing":[],"holding_cap":null,"requires_critic":[]},"thesis":{"H":[{"id":"H1","text":"在手訂單持續轉成營收：2027 年同店營收成長落在中 20% 區間（公司 2026-10-23 口徑），季末在手訂單維持 150 億美元以上。","2y":"2027 年同店營收年增 ≥20%","5y":null,"10y":null,"threshold":"2027 同店年增 ≥20%；任一季末在手訂單 ≥150 億美元（2026Q3 為 178 億）","source":"公司季報新聞稿與法說會（每季）","drift_rule":"TTM 營收連 2 季低於路徑 5% 以上為削弱，連 3 季低於 10% 以上為反轉"},{"id":"H2","text":"毛利率維持近幾季高檔：工程進入中後段後回到 24–25%，專案估計變動利得降到常態時仍 ≥22%。","2y":"2027 年全年毛利率 ≥23%","5y":null,"10y":null,"threshold":"季毛利率 ≥22%；2027 上半年回到 ≥24%（CFO 稱上半年回到平均）","source":"季報分部毛利率、10-Q 專案估計變動揭露","drift_rule":"TTM 毛利率連 2 季低於門檻 5% 以上為削弱，連 3 季低於 10% 以上為反轉"},{"id":"H3","text":"相對同業的執行優勢延續：營業利益率比 EME 高至少 4 個百分點（TTM 16.45% 對 9.6%），資料中心以外的機構與服務業務不萎縮。","2y":null,"5y":"2031 年 TTM 營業利益率對 EME 差距 ≥4 個百分點","10y":null,"threshold":"FIX 對 EME 的 TTM 營業利益率差距 ≥4 個百分點；服務營收年增 ≥0","source":"雙方季報（TTM 加總）","drift_rule":"差距連 4 季收窄 ≥5% 為削弱，連 6 季收窄 ≥10% 為反轉"}],"R":[{"id":"R1","text":"資料中心資本支出週期反轉：科技占營收 59%，增量訂單幾乎全來自資料中心，其他營建需求在走弱。","h_ref":"H1","clock":"🔥","threshold":"季末在手訂單連 2 季環比下滑，或低於 140 億美元","evidence_refs":["supply_demand_durability#3","customer_concentration_credit#2"]},{"id":"R2","text":"利潤率回吐：專案估計變動利得回到常態、電氣部門單一子公司高毛利率回落、設備材料占比上升。","h_ref":"H2","clock":"⚡","threshold":"季毛利率連 2 季低於 22%，或 10-Q 揭露專案估計變動轉為淨損失","evidence_refs":[]},{"id":"R3","text":"成本端吸收失敗：鋼鋁銅與含金屬電氣設備關稅、進口零組件、長交期設備，以及技工缺口推升的人工成本無法轉嫁。","h_ref":"H2","clock":"🔥","threshold":"毛利率連 2 季年減 ≥1 個百分點且管理層歸因材料或人工成本","evidence_refs":["reg_tariff_export#0","reg_tariff_export#2","geo_supply_chain#0","geo_supply_chain#1","geo_supply_chain#3"]},{"id":"R4","text":"客戶集中與信用：最大單一客戶占營收 12.8%，模組化依賴兩家超大規模客戶；客戶自建或另找供應來源。","h_ref":"H3","clock":"🐢","threshold":"最大客戶營收占比超過 15% 或應收占比超過 20%；或任一模組化客戶公開縮減量承諾","evidence_refs":["customer_concentration_credit#0"]},{"id":"R5","text":"財務長交棒：Bill George 2008 年起主導併購並兼管營運，2026 年報後交棒給 Julie Shaeff；併購紀律與財測準確度有交接風險。","h_ref":"H3","clock":"🔥","threshold":"交棒後兩季內實際營收或毛利率低於公司口徑，或另有高層離職","evidence_refs":[]}],"single_thing":{"description":"兩家模組化合約客戶（超大規模雲端業者）任一家縮減或延後五年量承諾，或最大科技客戶大幅下修資料中心資本支出並延後 FIX 承接的專案。","why_fatal":"科技占營收 59%、模組化占 17%，產能擴張（2027 年底約 600 萬平方呎）以這些承諾為前提；一旦縮減，營收、利潤率與新廠回收同時受傷，市場也會把整段在手訂單打折。","if_happens":"清倉，不等下一季數字確認。","how_monitor":"每季法說的模組化訂單與量承諾說法、季末在手訂單環比、超大規模業者資本支出口徑（事實表未涵蓋）。","probability":"12–24 個月約 15%"}},"appendix_a":{"growth_durability":6,"quality_score":8,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":19.28,"peg_fy2":0.79,"stress":{"pass":3,"total":4}},"eps_meta":{"base_eps_path":{"FY2025A":28.88,"FY2026E":49.03,"FY2027E":60.22,"FY2028E":75.95},"fy_end_month":12,"eps_basis":"基期為 FY2025 年報 GAAP 稀釋 EPS 28.88；共識為 Koyfin 2026-10-24 快照，兩份快照間修正為 0，可能尚未反映 2026Q3 實際 13.91 美元。"},"catalysts":[{"date":"2027-02","date_precision":"month","type":"guidance","event":"2026 年第四季財報與 2027 財測（財務長交棒前最後一次）","impact":"高","watch":"在手訂單是否 ≥170 億美元、毛利率是否回到 24% 附近、2027 同店成長口徑是否維持中 20% 區間"},{"date":"2026-11","date_precision":"month","type":"regulatory","event":"美國選舉後各州資料中心暫停令與限制法規動向","impact":"中","watch":"是否有在建專案被延後；管理層稱目前未見"},{"date":"2027-03","date_precision":"quarter","type":"other","event":"財務長 Bill George 交棒給 Julie Shaeff","impact":"中","watch":"併購節奏與財測口徑是否改變"},{"date":"2027-12","date_precision":"quarter","type":"capacity","event":"模組化產能達約 600 萬平方呎","impact":"中","watch":"新增產能是否有多年量承諾填滿；前沿實驗室與主機代管商是否簽成多年合約"}]}
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
