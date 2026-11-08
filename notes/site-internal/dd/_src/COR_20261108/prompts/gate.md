你是 DD 管線 v20 的判斷層閘（gate），標的 COR（20261108）。你未參與寫判斷，這是一次跨模型冷讀，單回合、無工具：bundle 全文已附在本訊息「===== BUNDLE =====」分隔線之後，讀完就直接作答，沒有第二輪，也不能查證 bundle 以外的任何資料。

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

### 判斷檔 `fact_refs` 引到的事實（31 條）
- `f_kpi0_revenue_gaap_q4`（q1_business）｜Revenue (GAAP) Q4＝88.4 USD bn｜期間與口徑：Q4 FY2026（季末 2026-09-30，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿（Business Wire／Cencora IR 檔案庫）https://s203.q4cdn.com/785768684/files/doc_news/Cencora-Reports-Fiscal-2026-Fourth-Quarter-and-Fiscal-Year-End-Results-2026.pdf（numbers.latest_quarter_kpis.items[0]，as_of Q4 FY2026（季末 2026-09-30，公告於 2026-11-04））
  - 註記：共識營收未查（報導稱營收與調整後EPS均優於共識）；YoY +5.5%；QoQ 未取得
- `f_kpi2_adjusted_non_gaap_operat`（q1_business）｜Adjusted (non-GAAP) operating income / margin Q4＝1248.9 USD M｜期間與口徑：Q4 FY2026（季末 2026-09-30，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿（Business Wire／Cencora IR 檔案庫）https://s203.q4cdn.com/785768684/files/doc_news/Cencora-Reports-Fiscal-2026-Fourth-Quarter-and-Fiscal-Year-End-Results-2026.pdf（numbers.latest_quarter_kpis.items[2]，as_of Q4 FY2026（季末 2026-09-30，公告於 2026-11-04））
  - 註記：n/a；YoY +22.1%（去年同季 1,023.1M）；margin 1.41%（去年 1.22%，+19bp）
- `f_kpi3_adjusted_diluted_eps_q4`（q1_business）｜Adjusted diluted EPS Q4＝4.66 USD｜期間與口徑：Q4 FY2026（季末 2026-09-30，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿（Business Wire／Cencora IR 檔案庫）https://s203.q4cdn.com/785768684/files/doc_news/Cencora-Reports-Fiscal-2026-Fourth-Quarter-and-Fiscal-Year-End-Results-2026.pdf（numbers.latest_quarter_kpis.items[3]，as_of Q4 FY2026（季末 2026-09-30，公告於 2026-11-04））
  - 註記：共識 4.57（來源：247wallst／Nasdaq 轉述，非 IR）；YoY +21.4%（去年 3.84）；GAAP EPS 2.71
- `f_kpi5_guidance_fy2027_adjusted`（q1_business）｜Guidance FY2027 adjusted diluted EPS＝19.40–19.75 USD｜期間與口徑：Q4 FY2026（季末 2026-09-30，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：guidance
  - 來源：公司新聞稿（Business Wire／Cencora IR 檔案庫）https://s203.q4cdn.com/785768684/files/doc_news/Cencora-Reports-Fiscal-2026-Fourth-Quarter-and-Fiscal-Year-End-Results-2026.pdf（numbers.latest_quarter_kpis.items[5]，as_of Q4 FY2026（季末 2026-09-30，公告於 2026-11-04））
  - 註記：共識 FY1 EPS 19.70（來源：consensus_revision 20261107 快照，財報後）；成長 8–10%；調整後營業利益成長 4–6%、淨利息 490–510M、稅率約 20%、股數約 190M、調整後 FCF 約 3.5B、資本支出約 1.0B
- `f_peer_cor_gross_margin_pct`（q2_moat）｜COR 毛利率＝4.12 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.COR.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_cor_operating_margin_pct`（q2_moat）｜COR 營業利益率＝1.44 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.COR.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_mck_gross_margin_pct`（q2_moat）｜MCK 毛利率＝3.67 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MCK.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_mck_operating_margin_pct`（q2_moat）｜MCK 營業利益率＝1.67 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.MCK.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_cah_gross_margin_pct`（q2_moat）｜CAH 毛利率＝3.9 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CAH.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_cah_operating_margin_pct`（q2_moat）｜CAH 營業利益率＝1.26 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.CAH.operating_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_peer_hsic_gross_margin_pct`（q2_moat）｜HSIC 毛利率＝31.59 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.HSIC.gross_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_consensus_eps_fy1`（q5_valuation）｜FY1 共識 EPS＝19.7 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy1，as_of 2026-11-07）
- `f_consensus_eps_fy2`（q5_valuation）｜FY2 共識 EPS＝21.93 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy2，as_of 2026-11-07）
- `f_consensus_eps_fy3`（q5_valuation）｜FY3 共識 EPS＝24.27 USD/share｜期間與口徑：2026-11-07／Koyfin 快照共識值；財年口徑見判斷檔 eps_meta.eps_basis｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy3，as_of 2026-11-07）
- `f_rev_consensus_fy1_m`（q5_valuation）｜FY1 共識營收（百萬）＝352568.91 USD m｜期間與口徑：2026-11-08／yfinance revenue_estimate 0y 平均（6 位分析師）；與 f_consensus_eps_fy1 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy1.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_rev_consensus_fy2_m`（q5_valuation）｜FY2 共識營收（百萬）＝368784.58 USD m｜期間與口徑：2026-11-08／yfinance revenue_estimate +1y 平均（6 位分析師）；與 f_consensus_eps_fy2 同一財年｜kind：estimate
  - 來源：—（numbers.capital_structure.revenue_consensus.fy2.avg_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_kpi4_free_cash_flow_fy2026_op`（q1_business）｜Free cash flow FY2026 (operating CF − capex)＝3881 USD M｜期間與口徑：Q4 FY2026（季末 2026-09-30，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿（Business Wire／Cencora IR 檔案庫）https://s203.q4cdn.com/785768684/files/doc_news/Cencora-Reports-Fiscal-2026-Fourth-Quarter-and-Fiscal-Year-End-Results-2026.pdf（numbers.latest_quarter_kpis.items[4]，as_of Q4 FY2026（季末 2026-09-30，公告於 2026-11-04））
  - 註記：n/a；營運現金流 4,790M、資本支出 910M；調整後 FCF 3,808M（扣除反托拉斯和解收益 73M）；僅提供全年，未提供單季
- `f_peer_cor_fcf_margin_pct`（q2_moat）｜COR FCF 利潤率＝0.47 %｜期間與口徑：TTM ending 2026-09-30（4季加總）／yfinance quarterly_income_stmt／quarterly_cashflow（TTM sum，最近可得季數）｜kind：realized
  - 來源：—（numbers.peer_financials.COR.fcf_margin_pct，as_of TTM ending 2026-09-30（4季加總））
  - 註記：Research And Development 該公司未單獨揭露（常見於硬體/非軟體業者）
- `f_net_debt_m`（q5_valuation）｜目前淨負債（總債務－現金及短投）＝6385.82 USD m｜期間與口徑：2026-11-08／yfinance 最新一季：總債務 11266.15、現金 4880.33（含租賃負債口徑）｜kind：realized
  - 來源：—（numbers.capital_structure.net_debt_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_shares_diluted_m`（q5_valuation）｜目前股數（百萬股）＝190.83 m shares｜期間與口徑：2026-11-08／yfinance impliedSharesOutstanding（各類股合計）｜kind：realized
  - 來源：—（numbers.capital_structure.shares_diluted_m，as_of 2026-11-08）
  - 註記：股數＝目前流通股數（各類股合計）或最新季稀釋均股，未含未行使選擇權／可轉債的完整稀釋，終端股數的稀釋由判斷者在 shares_y5 自行反映；共識營收 FY3：yfinance 只有 0y／+1y 兩個年度，無第三年，留 null
- `f_dividend_yield_ttm`（q5_valuation）｜trailing 12個月股息殖利率＝0.72 %｜期間與口徑：2026-11-08／trailing 12個月股息（依除息日加總，非發放日）÷ 判斷日股價 × 100｜kind：realized
  - 來源：—（numbers.dividend_yield_ttm.value_pct，as_of 2026-11-08）
- `f_price_at_dd`（q5_valuation）｜判斷日股價＝333.56 USD｜期間與口徑：2026-11-06（RTH 收盤，UTC）／收盤價，與情境樹起點同源｜kind：realized
  - 來源：—（numbers.price_at_dd，as_of 2026-11-06（RTH 收盤，UTC））
- `f_fwd_pe_latest`（q5_valuation）｜Forward P/E（最近快照）＝16.93 x｜期間與口徑：2026-11-07／分母＝FY1 EPS 19.7，分子＝快照價 333.56｜kind：realized
  - 來源：—（numbers.valuation_history.fwd_recent_window.points[-1]，as_of 2026-11-07）
- `f_pe_current`（q5_valuation）｜Trailing P/E（現值）＝18.58 x｜期間與口徑：2026-11-06（RTH 收盤，UTC）／3 個年度端點內的分位＝0.0｜kind：realized
  - 來源：trailing 口徑：以年度財報 fiscal-year-end 對應最近週線收盤價，逐年估算 trailing P/E／P/S／EV/S（yfinance 免費層年度財報僅回溯 4-5 年，非連續日頻 5 年序列——樣本點數見各子欄 n_points）。fwd_recent_window 另用本站 data/eps-estimates/ 月度快照 archive（現存約 2026-05 起）算一段短窗真 fwd PE，非 5 年歷史，勿與 trailing 混用。（numbers.valuation_history.trailing.pe，as_of 2026-11-06（RTH 收盤，UTC））
- `f_pe_percentile`（q5_valuation）｜Trailing P/E 年度端點分位＝0.0 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 3 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.pe.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ps_percentile`（q5_valuation）｜P/S 年度端點分位＝100.0 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 3 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ps.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_ev_s_percentile`（q5_valuation）｜EV/S 年度端點分位＝100.0 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／**非五年分位**：只用 3 個年度端點，valuation.percentile_5y 另有口徑｜kind：realized
  - 來源：—（numbers.valuation_history.trailing.ev_s.current_percentile_within_annual_points，as_of 2026-11-06（RTH 收盤，UTC））
- `f_week26_return_pct`（q5_valuation）｜26 週報酬＝28.3 %｜期間與口徑：2026-11-06（RTH 收盤，UTC）／含息前價格報酬，對照基準 ^GSPC｜kind：realized
  - 來源：—（numbers.momentum_26w.return_26w_pct，as_of 2026-11-06（RTH 收盤，UTC））
- `f_rsi14`（q5_valuation）｜RSI(14)＝51.57｜期間與口徑：2026-11-06（RTH 收盤，UTC）／日線 14 期；rsi14_usable=True｜kind：realized
  - 來源：—（numbers.momentum_26w.rsi14，as_of 2026-11-06（RTH 收盤，UTC））
- `f_consensus_rev_3m_fy1_pct`（q5_valuation）｜FY1 共識近 3 個月修正＝10.3 %｜期間與口徑：2026-08-13 → 2026-11-07／FY1 共識 EPS 17.86 → 19.7（Koyfin 快照，約 90 天間距）；投影成 decision_inputs.consensus_rev_3m_pct｜kind：estimate
  - 來源：DD_universe_EPS_estimates_20261107.xlsx（numbers.consensus_revision.latest_snapshot.fy1 ÷ snapshot_90d_prior.fy1，as_of 2026-11-07）
- `f_kpi1_gaap_operating_income_ma`（q1_business）｜GAAP operating income / margin Q4＝906.8 USD M｜期間與口徑：Q4 FY2026（季末 2026-09-30，公告於 2026-11-04）／evidence.numbers.latest_quarter_kpis 逐項口徑照抄（metric 名稱即口徑）｜kind：realized
  - 來源：公司新聞稿（Business Wire／Cencora IR 檔案庫）https://s203.q4cdn.com/785768684/files/doc_news/Cencora-Reports-Fiscal-2026-Fourth-Quarter-and-Fiscal-Year-End-Results-2026.pdf（numbers.latest_quarter_kpis.items[1]，as_of Q4 FY2026（季末 2026-09-30，公告於 2026-11-04））
  - 註記：n/a；margin 1.03%（去年同季 18.5M、0.02%，含 PharmaLex 商譽減損 723.9M）

### findings_digest 中方向為負或來源衝突的條目（15 條）
- `competitive_share_entrants#1`（competitive_share_entrants｜方向 -｜狀態 ok）：10-K 風險因素稱產業整併（製造商、零售藥局、醫療提供者、保險人結盟）可能加大競爭壓力，持續整併可能降低議價力或造成客戶流失。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2025-11-25）｜affects：moat_trend、decision_inputs.bear
- `competitive_share_entrants#2`（competitive_share_entrants｜方向 -｜狀態 ok）：CSIMarket 營收基準同業群占比 Q2 2026 約 31.97%，去年同期 32.86%（聚合站、方法不明）
  - 來源：CSIMarket COR Competitors（as_of 2026-08-01）｜affects：moat_trend
- `competitive_share_entrants#3`（competitive_share_entrants｜方向 -｜狀態 ok）：Simply Wall St 敘事：專科經銷競爭、大客戶擴張自有專科業務與產業整併可能侵蝕議價力與市占
  - 來源：Simply Wall St narrative（as_of 2026-06-01）｜affects：moat_trend、decision_inputs.bear
- `customer_second_source#0`（customer_second_source｜方向 -｜狀態 ok）：FY2025 10-K 揭露客戶集中：Walgreens 與 Boots 合計約占營收 25%、Evernorth 約 13%、前十大客戶約 66%；並警告關鍵客戶或 GPO 合約可能到期未續、被終止或以較差條件續約。一手文件未載明客戶導入第二供應商或自製。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2025-11-25）｜affects：moat_trend、decision_inputs.bear
- `customer_concentration_credit#0`（customer_concentration_credit｜方向 -｜狀態 ok）：FY2025：前十大客戶約占營收 66%；Walgreens 與 Boots 合計約 25%、Evernorth 約 13%。
  - 來源：SEC EDGAR 10-K FY2025 Item 1（as_of 2025-11-25）｜affects：thesis.R、decision_inputs.bear
- `customer_concentration_credit#1`（customer_concentration_credit｜方向 -｜狀態 ok）：2025-09-30 Walgreens 與 Boots 合計占應收帳款淨額約 38%，Evernorth 約 5%；公司揭露最大客戶破產或信用失敗可能造成重大不利影響。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2025-11-25）｜affects：thesis.R、decision_inputs.bear
- `customer_concentration_credit#2`（customer_concentration_credit｜方向 -｜狀態 ok）：自 2026-07-01 起，部分 Walgreens 量體移出 Cencora；主供應商協議不變，占與 Walgreens 業務絕大部分。
  - 來源：Cencora Form 8-K (2026-08-12)（as_of 2026-08-12）｜affects：thesis.R、valuation、decision_inputs.bear
- `customer_concentration_credit#3`（customer_concentration_credit｜方向 -｜狀態 ok）：Walgreens 於 2025-08-28 被 Sycamore 私有化，評等機構撤銷評等；私有化前 S&P 為 BB- 並列負面 CreditWatch。查無 2026 年新降評。
  - 來源：investing.com／InvestmentGrade.com 搜尋摘要（as_of 2025-08-28）｜affects：thesis.R、decision_inputs.bear
- `regulatory_antitrust#0`（regulatory_antitrust｜方向 -｜狀態 ok）：10-K 風險因素：藥品供應鏈受 FTC、DEA、FDA、HHS 及英國／歐盟等多層監管，供應鏈安全新規可能大幅增加配送成本與負擔；業務可能涉及反壟斷等政府調查。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2025-11-25）｜affects：thesis.R、decision_inputs.bear
- `regulatory_antitrust#2`（regulatory_antitrust｜方向 -｜狀態 ok）：Cencora MWI Animal Health 與 Covetrus 合併案（2026-02-18 宣布）被報導受 FTC 審視；聚合站標題，未核一手。
  - 來源：myvetcandy.com 經搜尋聚合引述（as_of 2026-08-06）｜affects：triggers、thesis.R
- `reg_tariff_export#0`（reg_tariff_export｜方向 -｜狀態 ok）：Cencora FY2025 10-K 風險因素：公司可能因美國關稅或其他保護措施而面臨供應中斷、短缺或額外成本（含包裝、材料、設備），並點名既有芬太尼關稅、對等關稅、對印度／巴西產品的次級關稅，以及 Section 232 對藥品與原料的威脅性關稅；公司稱無法預測其實施或調整方式。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2025-11-25）｜affects：thesis.R、decision_inputs.bear
- `reg_tariff_export#1`（reg_tariff_export｜方向 -｜狀態 ok）：10-K 載明所購藥品受價格通膨／通縮及已威脅與已實施關稅影響；學名藥價格通縮加速會加重對經營結果的負面衝擊。
  - 來源：SEC EDGAR 10-K FY2025 Item 1A（as_of 2025-11-25）｜affects：thesis.R、valuation
- `substitute_technology#0`（substitute_technology｜方向 -｜狀態 ok）：2026年6月 PharmExec 報導：製造商直接對病患（DTP）配銷已從試點變成策略優先項目，潛在繞過傳統批發通路
  - 來源：PharmExec: rise of direct-to-patient models, bypassing traditional distribution channels（as_of 2026-06-25）｜affects：moat_trend、thesis.R、decision_inputs.bear
- `major_events#1`（major_events｜方向 -｜狀態 ok）：2026-05-06 公司下修財測後股價單日跌 17.3%，Rosen、Pomerantz 等律所宣布調查潛在證券詐欺請求（調查公告，非已提起之集體訴訟）。
  - 來源：Barchart／AccessNewswire：Rosen Law Firm、Pomerantz 調查公告（as_of 2026-05-15）｜affects：decision_inputs.bear、triggers
- `lawsuit_class_action#0`（lawsuit_class_action｜方向 -｜狀態 ok）：2026-05 股價大跌後多家律所宣布調查證券詐欺請求；搜尋未見已提起之證券集體訴訟。
  - 來源：Barchart：Rosen Law Firm 調查公告（as_of 2026-05-15）｜affects：decision_inputs.bear、triggers

### 事實表自陳的缺口（2 條）
- q2_moat：evidence.numbers.peer_financials 該欄整欄為 null（常見於未單獨揭露研發的業者），事實表 agent 若能從財報補就補，補不到即為缺口，判斷者不得自行估。
- q6_how_wrong：digest.qa_flags 有 4 條管理層迴避紀錄，內容須由事實表 agent 逐條落成事實或缺口

---

scenario_meta.json sidecar（判斷層情境樹權威，checklist ⑥(iii) 對帳用）

（來源：/Users/ivanchang/financial-analysis-bot/.dd_build/runs/COR_20261108/scenario_meta.json）
（以下 JSON 為緊湊格式（省空白），內容完整）
```json
{"bull_5y_price":627.0,"bear_5y_price":258.0,"p_bull_pct":20,"p_bear_pct":30,"upside_5y_pct":38.1,"ev5y_pct":29.9,"irr_base_pct":6.7,"asym_ratio":2.6,"scenario_tree":{"terminal_label":"FY2031E","start":{"eps":19.7,"pe":16.93,"basis":"FY2027E 共識 EPS 19.70 美元，現價 333.56 ÷ 19.70＝16.93 倍；終端倍數同樣對當年度 EPS。"},"eps":{"bull":[20.1,22.9,26.0,29.4,33.0],"base":[19.7,21.6,23.9,26.3,28.8],"bear":[19.0,19.5,20.2,20.9,21.5]},"pe":{"bull":19,"base":16,"bear":12},"p":{"bull":20,"base":50,"bear":30},"yield_pct":{"dividend":0.72,"net_buyback":0},"second_stage":{"bull_cagr_pct":10,"base_cagr_pct":7},"valuation_dependent":false}}
```

---

## ④b 舊逐字稿摘錄（前一季＋投資人日；對照管理層以前說過什麼）

### COR_Q3_2026_Earnings_Call_20260805.md
- 2026-08-05｜Eva Boratto｜guidance：CFO 上調 FY2026 調整後 EPS 財測至 17.75–17.95 美元（前次 17.70–17.90）（原話："adjusted EPS guidance range to $17.75 to $17.95"）
- 2026-08-05｜Eva Boratto｜guidance：美國營收預期落在 4%–6% 成長區間的下半段（原話："we would expect revenue to be in the"）
- 2026-08-05｜Eva Boratto｜guidance：合併營業利益成長財測下限上調至 13%–14%（原話："now expect growth to be in the range of 13% to 14%."）
- 2026-08-05｜Eva Boratto｜guidance：美國醫療解決方案營業利益成長財測 14.5%–15.5%（原話："income growth to be in the range of 14.5% to 15.5%."）
- 2026-08-05｜Eva Boratto｜guidance：國際部門營收成長降至約 8%（區間低端），原因為下半年美元走強（原話："we now expect revenue growth to be approximately 8%"）
- 2026-08-05｜Eva Boratto｜guidance：全年調整後自由現金流財測約 30 億美元不變（原話："guidance of approximately $3 billion remains unchanged."）
- 2026-08-05｜Eva Boratto｜guidance：FY2027 完整財測將於 11 月財報電話會提供；提供 MWI 與 Covetrus 合併的建模參考（營業利益逆風 1.5 億、EPS 逆風約 0.35 美元，假設年中交割）（原話："would have a $150 million operating income"）
- 2026-08-05｜Eva Boratto｜guidance：EyeSouth Retina 收購時點無更新，不建議納入模型（原話："we would not suggest incorporating that into the models"）
- 2026-08-05｜Eva Boratto｜guidance：Q4 隱含財測為各報告部門強勁雙位數成長；排除 OneOncology 後預期為全年最強有機成長（原話："we expect to"）
- 2026-08-05｜Eva Boratto｜margin：合併毛利率擴張 61bp 至 4.16%，管理層歸因於 2 月收購 OneOncology（原話："expanded by 61 basis points to 4.16%, largely due to our"）
- 2026-08-05｜Eva Boratto｜margin：營業費用成長 27% 反映 OneOncology；排除兩家 MSO 後固定匯率成長 5%（原話："Excluding both MSOs, operating"）
- 2026-08-05｜Eva Boratto｜margin：美國核心業務排除 OneOncology 與流失腫瘤客戶後營業利益雙位數有機成長（上季為 7%）（原話："a meaningful acceleration from the 7% last quarter."）
- 2026-08-05｜Eva Boratto｜margin：Other 部門營業利益成長多數來自待售會計處理，MWI 本身約成長 10%（原話："Underlying MWI delivered about 10% growth and"）
- 2026-08-05｜Eva Boratto｜margin：國際部門歐洲分銷受惠於新興市場國家製造商調價時點，Q4 預期不再有此效應（原話："Now we wouldn't expect that impact in Q4, given some of"）
- 2026-08-05｜Eva Boratto｜margin：OneOncology 因 UUG 子公司非控制權益會計判斷，Q3 起不加回非控制權益損失，對營業利益無影響（原話："we determined that there should not be a"）
- 2026-08-05｜Eva Boratto｜margin：營收口徑：美國營收受 24 億美元廠商降價拖累，GLP-1 年增 23 億美元，另有 2025 年流失腫瘤客戶與大型郵購客戶銷售下降（原話："manufacturer list price"）
- 2026-08-05｜Eva Boratto｜commitment：OneOncology 以 12 個月計、扣除融資後對調整後 EPS 預期中性（原話："we continue to expect OneOncology to be"）
- 2026-08-05｜Eva Boratto｜commitment：已全數償還 RCA 融資相關 8 億美元定期貸款（6 月季 4 億、7 月 4 億）（原話："fully paid off our RCA financing-related term loan balance"）
- 2026-08-05｜Robert Mauch｜commitment：CEO 對 FY2027 不給數字，只重申對長期財測有信心、將落在該區間內（原話："I'm not going to take it any further than that."）
- 2026-08-05｜Robert Mauch｜commitment：CEO 稱下半年成長加速是「機械性、非願景式」，並稱第二季為最低成長季度，進展符合計畫（原話："It was mechanical, not aspirational"）
- 2026-08-05｜Eva Boratto｜commitment：CFO 表示財測哲學為依內部紀律流程設定，並延續交付或超越預期的紀錄（原話："Cencora's long track record of delivering or exceeding"）
- 2026-08-05｜Eva Boratto｜capital_allocation：本季以均價 268 美元回購 10 億美元股票，稀釋股數 1.939 億股（原話："an average price of $268 per share."）
- 2026-08-05｜Eva Boratto｜capital_allocation：CFO 列出資本配置優先順序：內部投資、策略併購、機會式回購、合理且成長的股息，並提到要「增強彈性」（原話："opportunistic share repurchase, as we just did in the"）
- 2026-08-05｜Robert Mauch｜capital_allocation：MSO 投資聚焦於 RCA（眼底）與 OneOncology（腫瘤）的小型併購，不進入其他專科（原話："accretive tuck-in acquisitions within the retina"）
- 2026-08-05｜Eva Boratto｜capital_allocation：利息費用財測上調至約 4.9 億美元，主因 10 億回購減少利息收入；全年稀釋股數約 1.94 億股（原話："primarily reflecting lower interest"）
- 2026-08-05｜Robert Mauch｜product：MSO 價值創造三階段：整合、共享能力（臨床試驗）、開發新服務；管理層稱仍屬早期（原話："3 phases to the value creation thesis"）
- 2026-08-05｜Robert Mauch｜product：RCA 臨床試驗平台已屬成熟後段，OneOncology 仍處早期（原話："In OneOncology, it's in the earlier innings"）
- 2026-08-05｜Robert Mauch｜product：管理層對 Part B 與 Part D 生物相似藥的利潤區分：Part B 因加值服務較多而利潤機會較大，Part D 營收承壓但利潤增幅有限（原話："Part B will always be good"）
- 2026-08-05｜Eva Boratto｜product：GLP-1 銷售成長 25%，管理層稱大致符合預期（原話："In terms of the GLP-1s, up 25%, that was generally in line"）
- 2026-08-05｜Eva Boratto｜product：World Courier 與歐洲 3PL 雙位數營業利益成長；3PL 有強勁續約，World Courier 在 FY25 艱困後市場趨穩（原話："In 3PL, we"）
- 2026-08-05｜Robert Mauch｜competition：回應分析師對 3PL／特殊物流競爭加劇的提問，CEO 承認有可信的對手，但稱自身定位於高端且廠商偏好製藥專注者（原話："there certainly are"）
- 2026-08-05｜Robert Mauch｜risk：340B 新試辦指引仍在評估，管理層稱不同業務受影響不同，未量化，且不應假設全是負面（原話："I wouldn't assume that, that's all negative."）
- 2026-08-05｜Robert Mauch｜risk：對 ASP 規則變動風險，CEO 稱政策無意影響醫師給付，並預期到 2028 年 IRA 與 Part B 時醫師給付不會受負面影響（原話："physicians will not be negatively impacted."）
- 2026-08-05｜Robert Mauch｜risk：管理層稱市場仍在消化並滿一年的廠商降價影響（原話："As the market continues to digest and annualize list price"）
- 2026-08-05｜Robert Mauch｜customer：CEO 對客戶組合表示滿意，稱大小客戶關係良好，續約無需特別提出（原話："nothing to call out in terms of renewals."）
- 2026-08-05｜Eva Boratto｜customer：大型郵購客戶銷售下降，管理層稱符合預期且與第二季一致；前一季提及該客戶可能自行內部化（原話："lower sales to our large mail order customer as expected"）

### 問答異常語氣（迴避／改口／保留）
- COR_Q3_2026_Earnings_Call_20260805.md｜問：Lisa Gill 問 FY27 市場共識約 14% 成長是否落在範圍內、除兩項建模因素外還有無其他須考量｜答法：CEO 未直接確認或否認 14%，僅重申長期財測信心並稱不會再多說
- COR_Q3_2026_Earnings_Call_20260805.md｜問：Eric Percher 問 340B 對公司業務的影響與價值主張｜答法：CEO 未回答公司在 340B 的具體業務與價值主張，稱各業務影響不同、未曾說明、實施前不會量化
- COR_Q3_2026_Earnings_Call_20260805.md｜問：Kevin Caliendo 問 ASP 規則變動對 MSO／GPO 的潛在影響並請求量化｜答法：CEO 談政策意圖與信心，未提供任何量化
- COR_Q3_2026_Earnings_Call_20260805.md｜問：George Hill 問 World Courier／3PL 競爭是否升溫，及腫瘤市場放緩是否影響 Q4 財測｜答法：CEO 談能力與差異化未直接回應競爭加劇程度；CFO 以通用語氣稱趨勢良好，未直接回答腫瘤放緩問題

---

| axis | status | n_findings | n_queries |
|---|---|---|---|
| competitive_share_entrants | found | 4 | 2 |
| customer_second_source | found | 1 | 2 |
| customer_concentration_credit | found | 4 | 2 |
| supply_demand_durability | found | 3 | 2 |
| regulatory_antitrust | found | 3 | 3 |
| reg_tariff_export | found | 3 | 2 |
| geo_supply_chain | found | 1 | 2 |
| end_markets | found | 3 | 2 |
| substitute_technology | found | 2 | 2 |
| channel_business_model_shift | found | 2 | 2 |
| capital_markets_pricing | found | 4 | 4 |
| major_events | found | 3 | 4 |

---

## 前份判斷摘要（含 drift_watch_prior 20 欄前份值；漂移歸因對帳用）

```json
{"date":"20260525","verdict":"B 觀望偏進場","role":null,"H":{"status":"ok","format":"table","rows":[{"id":"H1","text":"Specialty/RCA 業務貢獻 OI 45%+","columns":{"2Y 驗證點":"RCA OI margin ≥ 10%；Specialty 整體 OI YoY ≥ 12%","5Y 驗證點":"Specialty + MSO OI ≥ 50% 全公司","10Y 驗證點":"Specialty + MSO + 國際 OI ≥ 60% 全公司","具體門檻":"FY26 Specialty OI 占比 ~40%；mgmt 預估 FY28 達 45%+","來源":"FY25 10-K、Q2 FY26 8-K","漂移觸發":"連 4 季 TTM 偏離 ≥ 5% → 削弱"}},{"id":"H2","text":"Pharma 段 OI margin 穩定在 1.20%+","columns":{"2Y 驗證點":"連 4 季 OI margin ≥ 1.15%","5Y 驗證點":"5Y 滾動均 OI margin ≥ 1.20%","10Y 驗證點":"10Y 平均 OI margin ≥ 1.10%","具體門檻":"FY25: Pharma OI margin ~1.25%","來源":"FY25 10-K、Q2 FY26 8-K","漂移觸發":"連 4 季 TTM 偏離 ≥ 5% → 削弱"}},{"id":"H3","text":"Walgreens 客戶結構保持穩定（無 Chapter 11 / 大規模分拆）","columns":{"2Y 驗證點":"WBA 不公告 Chapter 11；WBA store closure","5Y 驗證點":"Walgreens 30% client share 保持（不流失至 MCK/CAH）","10Y 驗證點":"無美國 retail pharmacy 結構性 disruption","具體門檻":"WBA 2025 公告 1,200 stores 關閉 (10%)；Sycamore 談判進行中","來源":"WBA 季度報表、媒體公開","漂移觸發":"WBA 任一重大公告 → 立即重評（不需連兩季）"}}]},"R":{"status":"ok","format":"table","rows":[{"id":"R1","text":"Walgreens 結構性問題（Sycamore 失敗 / Chapter 11 / 拆分）","columns":{"對應假設":"H3","時間尺度":"⚡ 短期（任何 WBA 8-K 揭露立即觸發）","監測指標":"WBA 季度 cash burn、store closure 公告、Sycamore 談判進度","警戒閾值":"WBA 公告 Chapter 11 / 出售 / >20% store closure → 立即清倉"}},{"id":"R2","text":"RCA 整合失敗（physician retention 不足）","columns":{"對應假設":"H1","時間尺度":"🔥 中期（4-6 季）","監測指標":"RCA OI margin（季度）、physician retention 率（年度）","警戒閾值":"連 4 季 OI margin 15% → 減倉 1/3"}},{"id":"R3","text":"Pharma margin 結構性壓縮（manufacturer 議價權惡化 + 關稅）","columns":{"對應假設":"H2","時間尺度":"🐢 長期（2+ 年慢變數）","監測指標":"Pharma segment OI margin（季度趨勢）、產業 PE 倍數","警戒閾值":"連 4 季 OI margin ≤ 1.10% → 結構性破壞，減倉 1/2"}}]},"single_thing":null,"kill_metrics":null,"rearm_trigger":null,"irr_base_pct":null,"ev5y_pct":null,"drift_watch_prior":{"dca_verdict":null,"dca_role":null,"signal":"B","val":"🟢","ma":"🟠","trap":"🟡","moat_trend":null,"runway_post_y5":null,"asym_ratio":null,"ev5y_pct":null,"irr_base_pct":null,"max_dd_pct":null,"bull_5y_price":null,"bear_5y_price":null,"p_bull_pct":null,"p_bear_pct":null,"rearm_trigger":null,"price_at_dd":274.91,"archetype":null,"cycle_position":null}}
```

---

## judgment.json 全文（被審對象，緊湊格式）

（以下 JSON 為緊湊格式（省空白），內容完整）

```json
{"meta":{"ticker":"COR","date":"2026-11-08","schema":"v15.0","contract":"v19","company_name":"Cencora, Inc."},"oneliner":"Cencora 把藥品配送的現金轉進專科藥與醫師管理平台，FY2027 指引撐得住約 10% 的 EPS 成長。但 333.56 美元的基本情境年報酬只有約 7%，Walgreens 占營收 25%、應收 38% 是最大斷點，現價不追，296 美元以下再談。","facts_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/COR_20261108/facts.json","scenario_ref":"/Users/ivanchang/financial-analysis-bot/.dd_build/runs/COR_20261108/scenario.json","answers":{"q1_business":{"verdict":"賺的是藥廠和藥局之間的配送與服務錢，每 100 美元營收只留約 1.4 美元營業利益，利潤節點正從一般配送移到專科藥與醫師管理平台。","reasoning":"收錢方式有三種：向製造商收配送與服務費、向藥局和醫院賺採購價差、透過 MSO 分享專科診所利潤。Q4 FY2026 營收 884 億美元，舊分部美國 783 億、營業利益 9.98 億；國際 78 億、1.52 億；Other 23 億、1.01 億。調整後毛利率 4.04%，調整後營業利益率 1.41%，毛利率多出的 57 個基點主要來自併購 OneOncology，不是原有業務漲價。2026-11-04 起改成專科藥與醫師服務、藥品配送與服務兩大分部，MSO 約占 FY2026 營業利益 10%。單點依賴是集中度風險，不是護城河證據：Walgreens 加 Boots 約占 FY2025 營收 25%，Evernorth 約 13%，前十大 66%。產業時鐘判擴張期，依據是 FY2026 營收增 5%、GLP-1 單季多 28 億美元、專科藥占美國藥品支出過半，不是股價。產業態勢判雙向拉鋸：競爭面有客戶轉單與整併壓議價（10-K、2026-08-12 8-K）；結構面專科藥五年增 80%（2026-11-04 法說，管理層口徑）；其他結構變數是製造商降價（Q4 少 28 億美元營收）與 Part B 給付規則。","fact_refs":["f_kpi0_revenue_gaap_q4","f_kpi2_adjusted_non_gaap_operat","f_kpi3_adjusted_diluted_eps_q4","f_kpi5_guidance_fy2027_adjusted","f_peer_cor_gross_margin_pct","f_peer_cor_operating_margin_pct"],"verdict_values":{"revenue_quality":"營收大多是藥價的轉手，製造商降價會直接縮小營收但利潤影響小，看營業利益比看營收準。","unit_econ_note":"靠周轉賺錢：毛利率約 4%，營業利益率約 1.4%。專科配送、MSO、物流毛利率較高，FY2026 專科營業利益率約 3.7%（2026-11-04 法說分析師口述，管理層未更正）。","archetype":{"primary":"品質複利成長","secondary":"受監管公用/穩定內需","confidence":"中","fingerprint":"千分之十幾的營業利益率，靠規模與周轉賺錢，EPS 成長靠專科組合、併購與回購疊加。"},"industry":{"clock_phase":"II","sd_verdict_source":"結構性持久：藥品需求不能延後，到 2030 年有 100 多項新腫瘤藥（2026-11-04 法說，管理層口徑）；三大批發商 2026 年配銷營收預估 9,330 億美元（Drug Channels），新進者難以複製。","bargaining":{"up":"對製造商有配送與商業化服務的議價，但製造商也在試直送病患，上游優勢只算中等。","down":"下游偏弱：前十大客戶占營收 66%，Walgreens 已部分移量。專科診所端較強，因為 MSO 直接持股。","geo":"以美國為主，國際約占 Q4 營收 9%；歐洲配送受美元影響，FY2027 約 2,000 萬美元逆風。"},"profit_pool_dir":"由傳統配送往專科與 MSO 移動。五年利潤池占比事實表未涵蓋，只能由指引反推 FY2026 專科約占 41%。","tam_table":{"expanded":false,"reason":"事實表未涵蓋 TAM、滲透率與五年利潤池占比，分部重編 8-K 也不在本次資料內，展開只能靠管理層口徑，不足以填表。"}}}},"q2_moat":{"verdict":"護城河穩定，評 B：規模與專科網路難以複製，但最大客戶份額在下滑，定價力沒有變強。","reasoning":"機制是全國配送網路、冷鏈與專科物流的規模，加上 MSO 把醫師端綁在平台上。事實表沒有投入資本，算不出對同業的 ROIC 差距，改看利潤率與最大客戶份額：COR 毛利率高於 McKesson 與 Cardinal，但營業利益率低於 McKesson，毛利率優勢主要來自併表 MSO 的業務組合，不能當成定價力提升。當期報酬屬低利益率、高周轉，營運資金天數事實表未涵蓋，只能定性。增量報酬看 OneOncology：2026-08-05 法說 Eva Boratto 稱 12 個月扣融資後 EPS 中性，首年報酬約等於稅後融資成本。可能看錯的地方：RCA 與 OneOncology 的臨床試驗和服務疊加尚未計入，管理層稱 OneOncology 仍在早期，若兩年後報酬明顯上升，這個判斷要改。","fact_refs":["f_peer_cor_gross_margin_pct","f_peer_cor_operating_margin_pct","f_peer_mck_gross_margin_pct","f_peer_mck_operating_margin_pct","f_peer_cah_gross_margin_pct","f_peer_cah_operating_margin_pct","f_peer_hsic_gross_margin_pct"],"verdict_values":{"moat":{"mechanism":"全國配送、冷鏈與專科物流的規模，加上 MSO 把專科醫師綁進平台；三家寡占下靠周轉率賺錢。","execution":8,"pricing":6,"grade":"B","trend":"→","trend_evidence":"執行面擴大：排除兩筆 MSO 併購與失去腫瘤客戶後，FY2026 美國核心營業利益成長約 13%。定價面縮減：毛利率上升主要來自併購，Walgreens 2026-07-01 起部分量體移出，大型郵購客戶連三季下滑。兩者抵銷，判穩定；最大客戶份額下滑，不能判擴大。","competitor_notes":[{"name":"McKesson","strategy_note":"營業利益率高於 COR、毛利率較低，成本效率或業務組合較好；ROIC 差距事實表無法計算。"},{"name":"Cardinal Health","strategy_note":"毛利率與營業利益率都略低於 COR，現金轉換表面較好，但 COR 的同業表現金數字與公司公告對不上，不作結論。"},{"name":"Henry Schein","strategy_note":"毛利率遠高於三家藥品配送商，業務結構不同，不能當比較基準。"},{"name":"UPS Logistics","strategy_note":"10-K 列為競爭對手，主要在物流與第三方物流；2026-08-05 法說 Robert Mauch 承認有可信對手，但沒有量化競爭程度。"}],"peer_na_reason":"事實表只有同業利潤率，沒有投入資本與 ROIC，無法計算報酬差距，改看利潤率與最大客戶份額方向。","threats":[{"level":"🟡","text":"製造商、藥局、醫療提供者與保險人持續整併，壓低議價力或造成客戶流失。","p":"40%","evidence_refs":["competitive_share_entrants#1"]},{"level":"🟡","text":"大客戶把部分量體移走或自建配送與專科業務。目前是個別客戶行為，尚未變成全行業轉向。","p":"35%","evidence_refs":["customer_second_source#0","competitive_share_entrants#3"]},{"level":"🟡","text":"製造商直送病患由試點變成策略項目，可能繞過批發通路。只有單篇產業報導，尚無量體數字；三大批發商的配銷規模與 MSO 持股是反面證據。","p":"30%","evidence_refs":["substitute_technology#0"]}],"roic_durability":{"quadrant":"低利益率×高周轉","checkpoints":[{"item":"需求基礎值","level":"🟢","text":"病患使用、醫師或 PBM 決定、保險付款，三個角色都成立；藥品不能延後。FY2026 在製造商降價下營收仍增 5%。"},{"item":"決策層級","level":"🟡","text":"替代發生在主供應商合約與品項層級。Walgreens 主協議不變但部分量體已移出，證明客戶能拆單；MSO 診所端黏著度較高。"},{"item":"價值鏈分配","level":"🟡","text":"配送環節只拿約 1.4% 營業利益率，前十大客戶占 66%，毛利率上升靠併購。MSO 是往價值鏈高處走，能否多拿利潤還沒證明。"},{"item":"社會容忍度","level":"🟡","text":"專科經濟依賴 Part B 給付、ASP 規則與 340B，2026-08-05 法說管理層拒絕量化。事實表未見立法直接針對配送商，故不判紅燈。"}],"roiic":"事實表未涵蓋收購對價與投入資本，無法計算。方向代理：OneOncology 12 個月扣融資後 EPS 中性（2026-08-05 法說 Eva Boratto），首年約等於稅後融資成本。","reinvest_rate":"事實表未涵蓋折舊、營運資金變動與收購淨額，無法計算；可得數字只有 FY2026 資本支出 9.1 億美元、FY2027 約 10 億美元。","endo_ceiling":null,"formula_note":"公式＝增量 ROIC × 再投資率，輸入都缺，不用替代數字硬算。"}}}},"q3_growth":{"verdict":"成長空間中等：傳統配送已飽和，專科藥與 MSO 是真實的第二曲線，但多半靠併購取得，滲透率事實表未涵蓋。","reasoning":"成長來自量、併購與回購，價格是負貢獻：Q4 GLP-1 多 28 億美元，製造商降價少 28 億美元。共識 EPS 由 FY2026 實際 17.97 美元到 FY2029 的 24.27 美元，三年複合 10.5%；共識營收 FY2027 到 FY2028 只增 4.6%。由指引反推專科權重：扣除 Other 的營業利益成長 8.5–11%，配送 2–4%，專科 18–21%，低中高三組都解出專科約占 FY2026 扣除 Other 營業利益的 41%。若專科年增 15%、配送 5%，FY2031 專科占比約 52%。CFO 說專科中雙位數目標包含小型併購，所以不能全當內生。回購每年約 2%（12.5 億美元 ÷ 636.5 億美元市值）。內生上界因 ROIIC 與再投資率都缺，無法計算，共識與上界的缺口無法量化，長期信心上限定為中。衰退信號亮兩個：最大客戶份額縮減；EPS 複合比營收複合高約 5.9 個百分點，其中部分是製造商降價和處分業務壓低營收。","fact_refs":["f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_rev_consensus_fy1_m","f_rev_consensus_fy2_m","f_kpi5_guidance_fy2027_adjusted"],"verdict_values":{"growth":{"driver_mix":"量（專科與 GLP-1）為主，併購次之，回購每年約 2%，價格為負。","runway_years":"事實表未涵蓋專科藥與 MSO 滲透率，無法換算年數","runway_post_y5":"🟡","endo_ceiling_basis":"事實表缺收購對價、投入資本、折舊與營運資金變動，內生上界無法推導。情境上按保守處理，Bear 機率取 30%。","segments":[{"item":"專科藥與醫師服務","value":"FY2027 營收增 9–14%，營業利益增 18–21%（含 OneOncology 前四個月延續），長期中雙位數；FY2026 約占扣除 Other 營業利益 41%（由指引反推）"},{"item":"藥品配送與服務","value":"FY2027 營收增 4–6%，營業利益增 2–4%（含客戶移量延續與約 1 個百分點匯率），長期中個位數"},{"item":"Other（待處分）","value":"FY2027 營收約 35 億美元、營業利益約 2 億美元，對集團營業利益成長約 −5 個百分點"},{"item":"MSO","value":"約占 FY2026 集團營業利益 10%，EyeSouth 視網膜業務與 American Oncology Network 未計入指引"}],"decay_signals":["核心市占近 12 個月縮減：Walgreens 部分移量、大型郵購客戶連三季下滑、FY2025 失去腫瘤客戶","EPS CAGR 顯著高於營收 CAGR：共識 EPS 10.5% 對營收約 4.6%"],"trap_rating":"🟡"}}},"q4_capital":{"verdict":"資本配置中等：回購時點好、股本稀釋低，但併購報酬還沒證明。","reasoning":"FY2026 FCF 38.81 億美元（營運現金流 47.90 億減資本支出 9.10 億），調整後 38.08 億，超過原指引約 30 億，管理層歸因於量、組合與時點，時點部分可能回吐；FY2027 指引約 35 億。對調整後淨利：FY2026 以 17.97 美元 × 約 1.94 億股計約 34.9 億，轉換率約 109%；FY2027 以指引中點 19.575 美元 × 1.90 億股計約 37.2 億，約 94%。資料衝突：同業表 COR 的 TTM FCF 利潤率 0.47% 與公司公告換算的 1.15% 對不上，本次採公司公告。淨負債 63.9 億美元，FY2027 年底償還 OneOncology 定期貸款 10 億。SBC 金額與近三年現金四分去向事實表未涵蓋。營運槓桿沒有壓縮：FY2027 營收增 3–5%、營業利益增 4–6%。","fact_refs":["f_kpi4_free_cash_flow_fy2026_op","f_peer_cor_fcf_margin_pct","f_net_debt_m","f_shares_diluted_m","f_dividend_yield_ttm"],"verdict_values":{"capalloc":{"items":[{"name":"ma_roiic","applicable":true,"passed":false,"input":"2026-08-05 法說 Eva Boratto：OneOncology 12 個月扣融資後調整後 EPS 中性，首年約等於稅後融資成本；Q4 FY2025 PharmaLex 商譽減損 7.239 億美元，該業務已列入待處分。對價與投入資本事實表未涵蓋。"},{"name":"buyback_yield","applicable":true,"passed":null,"input":"FY2026 回購 10 億美元、均價 268 美元，以 FY2026 調整後 EPS 17.97 美元計買入收益率 6.7%。10 年期公債殖利率事實表未涵蓋，無法判定是否高出 2 個百分點。"},{"name":"sbc_dilution","applicable":true,"passed":true,"input":"SBC 金額事實表未涵蓋，改用股數反推：Q4 稀釋股數年減 1.8%（約 350 萬股），10 億美元 ÷ 268 美元約回購 373 萬股，扣掉回購後股本年增約 0.1%，低於 1.5%。"}]},"governance":{"capital_returns":[{"item":"FY2026 股東回報","value":"約 15 億美元，含回購約 10 億（均價 268 美元）與股息"},{"item":"FY2027 回購計畫","value":"12.5 億美元"},{"item":"股息","value":"季配息調升 10%，連續第 22 次"},{"item":"債務","value":"RCA 定期貸款 8 億美元已還清；FY2027 年底償還 OneOncology 定期貸款 10 億美元"},{"item":"資本支出","value":"FY2026 9.1 億美元，FY2027 約 10 億美元"},{"item":"併購","value":"OneOncology 2026-02 完成；EyeSouth 視網膜業務與 American Oncology Network 待交割；對價事實表未涵蓋"}]}}},"q5_valuation":{"verdict":"現價合理偏滿。要賺 10% 年化，得靠 EPS 五年複合 12.6%，或倍數升到 18 倍，我只信 EPS 複合約 10%。","reasoning":"FY2027E 共識 19.70 美元對應 16.93 倍，已在指引 19.40–19.75 美元上緣。要達 10% 年報酬，扣 0.72% 股息後股價需年增 9.28%，五年後約 520 美元；16 倍下要 EPS 32.5 美元（由 17.97 美元複合 12.6%），基本情境 28.8 美元下要 18 倍。資料限制：trailing 本益比 18.58 倍在 3 個年度端點的分位為 0，但 18.58 倍隱含 EPS 約 17.95 美元，是調整後口徑，FY2025 GAAP EPS 只有 7.96 美元，歷史端點若用 GAAP 就不可比，事實表未列端點值，無法確認，所以不拿 0 分位當便宜證據；P/S 與 EV/S 同時在最高分位。賣方目標價 349–366 美元都在 2026-11-04 財報前，只比現價高 5–10%，支持不追。同業 Forward P/E 事實表未涵蓋。","fact_refs":["f_price_at_dd","f_fwd_pe_latest","f_pe_current","f_pe_percentile","f_ps_percentile","f_ev_s_percentile","f_consensus_eps_fy1","f_consensus_eps_fy2","f_consensus_eps_fy3","f_dividend_yield_ttm"],"verdict_values":{"valuation":{"basis":"FY2027E 共識 EPS 的 Forward P/E，FCF 殖利率對照。","tier":"藥品配送三大寡占","peers":{"expanded":false,"reason":"事實表只有同業利潤率，沒有 Forward P/E 或 EV/EBITDA，同業估值比較無法展開，補不到就不寫數字。"},"fwd_pe":16.93,"peg":1.61,"percentile_5y":null,"val_light":"🟡","val_light_derivation":"16.93 倍 ÷ 三年共識 EPS 複合 10.54%＝PEG 1.61，落在合理區間；FY2027 調整後 FCF 約 35 億美元 ÷ 市值 636.5 億美元＝殖利率約 5.5%；基本情境年報酬約 7%。事實表沒有五年序列，五年分位留空。1 年上檔：FY2028E 21.6 美元 × 16 倍＝345.6 美元，+3.6%；3 年上檔：FY2030E 26.3 美元 × 16 倍＝420.8 美元，+26.2%。","upside_short_pct":3.6,"upside_mid_pct":26.2,"denominator_disputed":false,"denominator_note":"Q4 GAAP EPS 2.71 美元與調整後 4.66 美元差距大，但 FY2027 調整後 FCF 每股約 18.4 美元，約為指引中點的 94%，調整後 EPS 有現金支撐，分母不是本次爭點。FY2027 含約 4,000 萬美元與 MWI 交易相關的營業外收益，是否持續事實表未涵蓋。"}}},"q6_how_wrong":{"verdict":"最可能看錯的是客戶集中，不是專科成長；其次是併購報酬與給付規則。","reasoning":"陷阱風險中等，衰退信號亮兩個。反證與裁定都在反證紀錄，共四條：Walgreens 斷點、專科給付規則、併購報酬、價格已反映。事實表沒有歷史最大回撤序列，路徑風險以 2026-05-06 單日跌 17.3% 與 Bear 倍數推估。","fact_refs":["f_week26_return_pct","f_rsi14","f_consensus_rev_3m_fy1_pct","f_kpi1_gaap_operating_income_ma"],"verdict_values":{"trap":{"verdict":"🟡","label":"生意沒壞，但客戶集中度高、併購報酬未證"}}}},"scenario_inputs":{"terminal_label":"FY2031E","start":{"eps":19.7,"pe":16.93,"basis":"FY2027E 共識 EPS 19.70 美元，現價 333.56 ÷ 19.70＝16.93 倍；終端倍數同樣對當年度 EPS。"},"eps":{"bull":[20.1,22.9,26.0,29.4,33.0],"base":[19.7,21.6,23.9,26.3,28.8],"bear":[19.0,19.5,20.2,20.9,21.5]},"pe":{"bull":19,"base":16,"bear":12},"p":{"bull":20,"base":50,"bear":30},"yield_pct":{"dividend":0.72,"net_buyback":0},"second_stage":{"bull_cagr_pct":10,"base_cagr_pct":7},"max_dd":{"lo":-40,"hi":-25,"basis":"淺端 −25%：略深於 Bear 五年終點 −22.7%（21.5 美元 × 12 倍＝258 美元）。深端 −40%：FY2026 實際 EPS 17.97 美元 × 12 倍＝216 美元（−35%），再加事件日過度反應約 5 個百分點。路徑參考是 2026-05-06 因下修財測單日跌 17.3%。","trigger_time":null},"basis":{"bull":"專科維持中雙位數以上，EyeSouth 與 American Oncology Network 增厚，配送約 5%，EPS 五年複合約 12.9%；專科占營業利益過半，倍數升到 19 倍。同業現值倍數事實表未涵蓋。","base":"FY2027 貼共識；FY2028 反映 MWI 半年延續約 0.35 美元，略低於共識；之後約 10%，落在長期目標 10–14% 下緣。倍數由 16.93 降到 16，介於前份約 15.4 倍與現值之間，同業現值倍數事實表未涵蓋。回購約 2% 已在 EPS 路徑內，淨回購填 0 以免重複計算。","bear":"Walgreens 或 Evernorth 再移出量體，Part B 規則壓低專科經濟，FY2027 低於指引下限，之後年增約 3%；倍數 12 倍，比 5 月約 15 倍再壓 3 倍，對應成長只剩 3–4%。機率 30% 依據是內生上界算不出、前十大客戶占 66%、給付風險未量化。"},"endo_ceiling_exceeded":null},"counter_evidence":{"blind_spots":[{"view":"論點失敗","evidence":"Walgreens 與 Boots 合計占 FY2025 營收約 25%、應收約 38%，私有化後評等已撤銷，2026-07-01 起部分量體移出。","assumption":"主供應商協議繼續有效，新股東不會進一步拆分採購。","consequence":"協議終止時 EPS 停在 20 美元上下，倍數 11 至 12 倍，股價約 220 至 240 美元，比現價跌 28% 至 34%；再加應收減損可到 −50%。","ruling":"採納為最大風險，與唯一致命點相同。協議未變不等於風險解除，因為私有化後外界看不到對方財務。","watch":"FY2026 10-K 的客戶與應收占比，以及任何揭露移量的 8-K。","evidence_refs":["customer_concentration_credit#1","customer_concentration_credit#3"],"fact_refs":[]},{"view":"論點失敗","evidence":"2026-08-05 法說 Robert Mauch 拒絕量化 340B 與 ASP 規則影響；2026-11-04 法說回答給付問題時只談政策倡議。","assumption":"給付變動不傷專科診所經濟，2028 年 IRA 延伸到 Part B 後醫師給付不受負面影響。","consequence":"專科成長由中雙位數降到個位數，EPS 路徑掉向 Bear，MSO 併購的資本回不來。","ruling":"部分採納。現有證據的時間窗蓋不到 2028 年風險窗，不能說風險已解，裁定為不可裁決至規則定案。","watch":"CMS 年度給付規則、專科分部毛利率、管理層是否開始量化。","evidence_refs":["regulatory_antitrust#0"],"fact_refs":[]},{"view":"論點成功但股東經濟變差","evidence":"OneOncology 首年 EPS 中性；資本支出升到約 10 億美元；Q4 GAAP EPS 2.71 美元對調整後 4.66 美元；EyeSouth 與 American Oncology Network 還要再花錢。","assumption":"MSO 併購之後靠臨床試驗與服務疊加拉高報酬。","consequence":"專科占比上升、調整後 EPS 達標，但增量資本報酬低於資本成本，每股 FCF 成長落後 EPS，倍數不會升。","ruling":"部分採納。基本情境倍數由 16.93 降到 16，不給專科化溢價。","watch":"FY2027 調整後 FCF、OneOncology 滿 24 個月的 EPS 貢獻、商譽減損。","evidence_refs":[],"fact_refs":["f_kpi1_gaap_operating_income_ma","f_kpi3_adjusted_diluted_eps_q4","f_kpi4_free_cash_flow_fy2026_op"]},{"view":"價格已反映太多","evidence":"26 週漲 28.3%，比前份 274.91 美元高 21.3%；FY2027 共識已在指引上緣；基本情境年報酬約 7%。","assumption":"市場會繼續用約 17 倍買 10% 成長，不回到 5 月的約 15 倍。","consequence":"回到 15 倍就是 296 美元，跌 11%，基本面不必變差。","ruling":"採納，這是本次不追的唯一約束。","watch":"FY2027E 共識本益比與財報後賣方目標價更新。","evidence_refs":[],"fact_refs":["f_week26_return_pct","f_fwd_pe_latest","f_consensus_eps_fy1","f_price_at_dd"]}],"contradictions":[{"axis":"[程式歸因]週線均線六態由程式算（timing-appendix §F）：前份 🟠 → 本次 🟡","cause":"方法變動","prior_field":["ma"],"side_a":"前份 ma=🟠","side_b":"本次 ma=🟡","ruling":"均線六態改由程式從週線收盤與 W52/W104/W250 計算，判斷者照抄；此欄變動屬方法變動，不是基本面新證據。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]判斷日現價由事實表帶入：前份 274.91 → 本次 333.56（+21.3%）","cause":"價格變動","prior_field":["price_at_dd"],"side_a":"前份 price_at_dd=274.91","side_b":"本次 price_at_dd=333.56","ruling":"現價是機械輸入，不構成判斷理由；起點價變動連帶影響的 IRR／EV／不對稱由 scenario 腳本重算，判斷者只需歸因情境輸入本身的改變。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：情境樹重建（股價固定在前份 274.91 美元重算）","cause":"方法變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct","bull_5y_price","bear_5y_price"],"side_a":"前份情境、股價 274.91 美元：五年期望值 前份未列，基準年化 前份未列，前份未列不對稱比","side_b":"本次情境、股價仍用 274.91 美元：Bull 價 627、Bear 價 258，五年期望值 +57.6%，基準年化 10.9%，不對稱比 13.88","ruling":"先換情境、股價不動：五年期望值與基準年化前份未列，無法比較。前份未列不對稱比，本次為 13.88。Bull、Bear 價位與股價無關，只受情境影響。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"[程式歸因]期望報酬拆解：股價變動（情境固定為本次重算）","cause":"價格變動","prior_field":["asym_ratio","ev5y_pct","irr_base_pct"],"side_a":"本次情境、股價 274.91 美元：五年期望值 +57.6%，基準年化 10.9%，不對稱比 13.88","side_b":"本次情境、股價 333.56 美元：五年期望值 +29.9%，基準年化 6.7%，不對稱比 2.59","ruling":"再換股價、情境不動：起點價上漲 21.3%，五年期望值少 27.7 個百分點，基準年化少 4.2 個百分點，不對稱比由 13.88 降到 2.59。拆解順序為先情境後股價。","evidence_level":"程式計算","settle_metric":"—","if_then":[],"evidence_refs":[]},{"axis":"共識上修是真的嗎","cause":null,"prior_field":null,"side_a":"FY1 共識三個月上修 10.3%（17.86 → 19.70 美元）。","side_b":"8 月的 FY1 是 FY2026，11 月的 FY1 已換成 FY2027，這是財年換算。同財年比較：FY2026 實際 17.97 美元只比 8 月共識多 0.6%；FY2027 在 2026-08-05 法說上 JPMorgan 分析師說市場約增 14%，以指引中點 17.85 美元換算約 20.35 美元，現在 19.70 美元，少約 3%，其中 MWI 的 0.35 美元在 8 月已提示。","ruling":"採 B 側，性質是方向相反但屬資料口徑，可調和。上修 10.3% 不能當動能證據，同財年實際方向是小幅下修。決策若引用此數字應人工覆核。","evidence_level":"程式快照加逐字稿；14% 為分析師口述，不是正式共識。","settle_metric":"FY2027 共識相對 19.70 美元的變化","if_then":["如果 2027-02 財報後 FY2027 共識高於 20.00 美元，上調基本情境 EPS 並重算進場價。","反向：如果共識跌破 19.40 美元，停止加碼。"],"evidence_refs":[]},{"axis":"管理層對客戶續約的說法","cause":null,"prior_field":null,"side_a":"2026-08-05 法說 Robert Mauch 說續約沒有需要特別提的。","side_b":"2026-08-12 8-K 揭露 2026-07-01 起部分 Walgreens 量體移出；2026-11-04 法說 Eva Boratto 把客戶移量列為 FY2027 配送分部的延續壓力。","ruling":"可調和但扣分。主協議未變，字面上不算續約，不過移量在法說當下已生效，依摘錄法說沒有主動提。此後客戶議題只看 8-K、10-K 數字。規模不大：配送指引 2–4% 比中個位數目標少約 2 個百分點，匯率占 1 個，移量約 1 個。","evidence_level":"一手 8-K 加逐字稿摘錄","settle_metric":"FY2026 與 FY2027 10-K 的 Walgreens 營收占比","if_then":["如果 FY2027 10-K 占營收低於 20%，減碼三分之一。","反向：如果占比維持 23% 以上且無新揭露，解除客戶揭露扣分。"],"evidence_refs":["customer_concentration_credit#2"]},{"axis":"現在就買還是等價位","cause":null,"prior_field":null,"side_a":"現在就買的最強論證：16.9 倍買 EPS 目標 10–14% 的公司；FY2027 排除 MWI 後 EPS 增 10–12%；FCF 殖利率約 5.5%；股息連續 22 次調升；賣方目標價都高於現價。","side_b":"現價已比前份高 21%，基本情境年報酬約 7%，FY2027 共識在指引上緣，新分部要到 2027-02 才有第一季實績。","ruling":"採 B 側。卡點只有價格，基本面沒有破；不是逢高賣出的理由，只是現在買的報酬不夠。可能看錯的地方是管理層一貫超標，FY2027 若超過指引上緣，等待會錯過一段。","evidence_level":"公司指引與程式估值資料","settle_metric":"股價相對 296 美元，以及專科分部前兩季營業利益成長","if_then":["如果股價收在 296 美元以下，且 Walgreens、Evernorth 沒有新增移量，分批反買，分三批。","如果股價續漲超過 366 美元而專科分部還沒有一季實績，不追。","反向：如果 FY2027 Q1、Q2 專科分部成長都 ≥ 18%，基本情境倍數由 16 倍提到 17 倍，進場價上移到約 314 美元。"],"evidence_refs":[]},{"axis":"估值結論由便宜轉合理","cause":"價格變動","prior_field":["val"],"side_a":"前份股價 274.91 美元，以當時 FY2026 指引中點 17.80 美元計約 15.4 倍，結論為便宜。","side_b":"現價 333.56 美元，FY2027E 共識 16.93 倍，結論轉為合理。","ruling":"主因是股價漲 21.3%，EPS 基礎換到下一財年只吸收一部分，倍數升約 1.5 倍。","evidence_level":"程式價格與共識","settle_metric":"FY2027E 共識本益比","if_then":["如果本益比回到 15 倍（約 296 美元），分批反買。","反向：如果本益比升到 19 倍以上而 EPS 未上修，不追。"],"evidence_refs":[]},{"axis":"綜合評等與陷阱風險維持不變","cause":"新證據","prior_field":["signal","trap"],"side_a":"前份綜合評等 B，陷阱風險中等。","side_b":"本次仍為 B 與中等，依據換成新分部指引、Walgreens 移量與 OneOncology 併表。","ruling":"結論不變，理由更新。專科成長證據變強，客戶集中證據變差，兩者抵銷。","evidence_level":"一手財報、8-K 與逐字稿","settle_metric":"專科分部營業利益成長與 Walgreens 占比","if_then":["如果兩項同時惡化，減碼三分之一。","反向：如果專科連兩季 ≥ 18% 且客戶占比穩定，把價格門檻上移重算。"],"evidence_refs":["customer_concentration_credit#2"]},{"axis":"前份空白欄位首次填寫","cause":"方法變動","prior_field":["moat_trend","runway_post_y5","archetype","cycle_position","max_dd_pct","p_bull_pct","p_bear_pct"],"side_a":"前份這些欄位沒有值。","side_b":"本次第一次填：護城河穩定、成長空間中等、商業類型為品質複利、非循環股不判循環位置、機率 20／50／30、Max DD −25% 至 −40%；定期定額結論與角色由程式產生。","ruling":"沒有舊值可比，不算結論改變。","evidence_level":"格式差異","settle_metric":"下一份報告對照本次值","if_then":["如果下一份這些欄位有變，按原因逐欄歸因。"],"evidence_refs":[]},{"axis":"Single Thing 由空白改為 Walgreens 主供應商協議","cause":"方法變動","prior_field":null,"side_a":"前份唯一致命點欄位為空。","side_b":"Walgreens 主供應商協議終止，或 Walgreens 申請破產。","ruling":"前份把 Walgreens 放在第一項風險，這次升為 Single Thing，因為 25% 營收、38% 應收是最大單一敏感度，發生時清倉。","evidence_level":"一手 10-K 與 8-K","settle_metric":"協議狀態與破產申請","if_then":["如果任一成立，清倉。","反向：如果 FY2027 10-K 占比仍在 23% 以上且主協議延續，下調事件機率。"],"evidence_refs":["customer_concentration_credit#0"]},{"axis":"清倉與減碼門檻更新","cause":"新證據","prior_field":null,"side_a":"WBA 公告 Chapter 11／出售／>20% store closure → 立即清倉；連 4 季 OI margin ≤ 1.10% → 結構性破壞，減倉 1/2；連 4 季 OI margin 15% → 減倉 1/3。","side_b":"主供應商協議終止或破產 → 清倉；再揭露移量或 FY2027 10-K 占營收低於 20% → 減碼三分之一；配送分部 FY2027 營業利益成長低於 2% → 停止加碼；專科分部 FY2027 低於 15% → 停止加碼。","ruling":"「出售」一項退休：Sycamore 私有化已於 2025-08-28 完成，主協議未變，前份寫談判中是過時資訊。店數改看公司揭露的營收占比，因為私有化後 Walgreens 不再公開季報。配送利益率 1.10% 與 RCA 利益率因新分部重編與未單獨揭露取不到值，保留在賣出指標並標資料缺口。","evidence_level":"一手 8-K、逐字稿；重編 8-K 不在本次資料內","settle_metric":"新分部第一季揭露","if_then":["如果新分部揭露配送利益率，恢復 1.10% 門檻並減碼一半。"],"evidence_refs":["customer_concentration_credit#3"]},{"axis":"重新進場條件新增","cause":"方法變動","prior_field":["rearm_trigger"],"side_a":"前份沒有重新進場條件。","side_b":"股價收盤 ≤ 296 美元（約 FY2027E 共識 15 倍），且 Walgreens、Evernorth 沒有新增移量，分批反買。","ruling":"296 美元由基本情境 460.8 美元、10% 年報酬倒推，與 FY2027E 共識 15 倍和 104 週均線 298.89 美元接近。","evidence_level":"情境推算與程式均線","settle_metric":"收盤價與大客戶揭露","if_then":["如果條件成立，分批反買，分三批。","反向：如果跌到 296 美元以下是因為大客戶移量，不買，先重做研究。"],"evidence_refs":[]}],"triggers":[{"n":1,"text":"Walgreens 主供應商協議終止，或 Walgreens 申請破產，立即清倉。","type":"Single Thing","maps_to":"Single Thing","metric":"主供應商協議狀態、破產申請","threshold":"協議終止或破產申請任一成立","action":"清倉","source_freq":"8-K，事件發生時","date":null,"evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#1","customer_concentration_credit#3"]},{"n":2,"text":"Walgreens 再揭露移量或占比跌破門檻，減碼三分之一。","type":"減碼","maps_to":"R1","metric":"Walgreens 與 Boots 占營收與應收比例","threshold":"再有 8-K 揭露移量，或 FY2027 10-K 占營收低於 20%，或占應收高於 45%","action":"減碼三分之一","source_freq":"8-K 即時，10-K 每年","date":"2027-11","evidence_refs":["customer_concentration_credit#2"]},{"n":3,"text":"Cigna 批發配送是一季內的新利空，管理層不評論，賣方模型是否納入事實表未涵蓋。第一個確認數據出來前不加碼，Evernorth 占比跌破門檻就減碼。Evernorth 與 Cigna 的關聯事實表未載明，本次按同一風險處理。","type":"減碼","maps_to":"R2","metric":"Evernorth 占營收比例","threshold":"由約 13% 降到 9% 以下，或公司確認協議縮減","action":"減碼三分之一","source_freq":"10-K 每年，法說每季","date":"2027-02","evidence_refs":["customer_second_source#0"]},{"n":4,"text":"專科分部成長不到門檻就停止加碼。","type":"假設驗證","maps_to":"H1","metric":"專科藥與醫師服務分部營業利益年增率","threshold":"FY2027 低於 15%，或 FY2028 起任兩季低於 10%","action":"停止加碼","source_freq":"季報，每季","date":"2027-02","evidence_refs":[]},{"n":5,"text":"配送分部成長不到門檻就停止加碼。","type":"假設驗證","maps_to":"H2","metric":"藥品配送與服務分部營業利益年增率","threshold":"FY2027 低於 2%，或 FY2028 低於 3%","action":"停止加碼","source_freq":"季報，每季","date":"2027-02","evidence_refs":[]},{"n":6,"text":"管理層把 FY2026 現金流超標歸因於量、組合與時點。FY2027 調整後 FCF 若低於門檻，視為歸因不成立。","type":"假設驗證","maps_to":"H3","metric":"調整後自由現金流","threshold":"FY2027 低於 30 億美元","action":"減碼三分之一","source_freq":"財報新聞稿，每年","date":"2027-11","evidence_refs":[]},{"n":7,"text":"關稅、學名藥通縮與供應鏈法規不做預測，只看公司有沒有吸收掉。","type":"風險","maps_to":"R5","metric":"配送分部營收成長減營業利益成長","threshold":"差距連 4 季大於 3 個百分點，且管理層歸因成本或學名藥通縮","action":"減碼三分之一","source_freq":"季報，每季","date":null,"evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","regulatory_antitrust#0"]},{"n":8,"text":"FTC 於 2026-05-20 對 MWI 與 Covetrus 合併發出補件要求，FY2027 指引假設年中完成，影響約營業利益 1.5 億美元、EPS 0.35 美元。","type":"風險","maps_to":"H3","metric":"MWI 與 Covetrus 交割時點","threshold":"2027-09-30 前未完成，或 FTC 提起訴訟","action":"停止加碼","source_freq":"8-K、季報","date":"2027-09","evidence_refs":["regulatory_antitrust#2"]},{"n":9,"text":"2026-05 股價下跌後多家律所宣布調查，目前只是調查公告，尚未提告，本身不動作。民事集體訴訟通過認證才減碼。","type":"風險","maps_to":"治理風險","metric":"證券集體訴訟進度","threshold":"正式提告且通過集體認證","action":"減碼一半","source_freq":"法院文件、10-Q","date":null,"evidence_refs":["major_events#1","lawsuit_class_action#0"]},{"n":10,"text":"若 SEC 或司法部就財測揭露介入，清倉。","type":"清倉","maps_to":"治理風險","metric":"SEC 或司法部調查","threshold":"公司揭露正式調查或刑事介入","action":"清倉","source_freq":"8-K、10-Q","date":null,"evidence_refs":["major_events#1"]},{"n":11,"text":"估值回到基本情境 10% 年報酬的價位，分批反買。","type":"估值rearm","maps_to":"H1","metric":"收盤價與大客戶揭露","threshold":"收盤 ≤ 296 美元，且 Walgreens、Evernorth 沒有新增移量","action":"分批反買","source_freq":"每日收盤，8-K","date":null,"evidence_refs":[]},{"n":12,"text":"FY2027 Q1 財報複審，對照 Q1 調整後 EPS 約 4.55 美元與新分部第一次實績。","type":"複審日期","maps_to":"H1","metric":"Q1 調整後 EPS、分部營業利益","threshold":"EPS 低於 4.55 美元，或專科分部成長低於 18%","action":"停止加碼","source_freq":"季報","date":"2027-02","evidence_refs":[]}],"kill_metrics":[{"metric":"Walgreens 與 Boots 主供應商協議及占營收比例","bear_threshold":"協議終止或破產；FY2027 10-K 占營收低於 20%","window":"每份 8-K、10-K，至 FY2027 10-K","source":"SEC 8-K、10-K 客戶集中揭露","last_status":"warning"},{"metric":"Evernorth 占營收比例","bear_threshold":"由約 13% 降到 9% 以下","window":"FY2026、FY2027 10-K","source":"SEC 10-K","last_status":"unknown"},{"metric":"專科藥與醫師服務分部營業利益年增率","bear_threshold":"FY2027 低於 15%，或 FY2028 起任兩季低於 10%","window":"FY2027 Q1 起逐季","source":"Cencora 季報新分部","last_status":"unknown"},{"metric":"藥品配送與服務分部營業利益年增率","bear_threshold":"FY2027 低於 2%，或 FY2028 低於 3%","window":"FY2027 Q1 起逐季","source":"Cencora 季報新分部","last_status":"unknown"},{"metric":"調整後自由現金流","bear_threshold":"FY2027 低於 30 億美元","window":"FY2027 全年","source":"Cencora 財報新聞稿","last_status":"unknown"},{"metric":"配送分部營業利益率（前份門檻，資料缺口）","bear_threshold":"連 4 季 ≤ 1.10%，新分部基期待重編資料確認","window":"FY2027 Q1 起逐季","source":"季報；分部重編 8-K 不在本次資料內","last_status":"unknown"},{"metric":"RCA 營業利益率（前份門檻，資料缺口）","bear_threshold":"前份文字為連 4 季 15%，方向不明；公司未單獨揭露","window":"待公司揭露","source":"事實表未涵蓋","last_status":"unknown"}],"evidence_dismissed":[{"ref":"competitive_share_entrants#2","reason":"聚合網站數字，同業群組成與計算方法都沒揭露；0.9 個百分點的差距也混入製造商降價與 GLP-1 組合差異，無法判定市占方向。客戶流失改用 10-K 與 8-K 一手證據判斷。"}],"action_conditions":{"rearm_trigger":"股價收盤 ≤ 296 美元（約 FY2027E 共識 15 倍），且 Walgreens、Evernorth 沒有新增移量","exec_line":"現價不追。跌到 296 美元以下且基本面未破，分三批反買；續漲而專科分部尚無實績，不追。"}},"decision_inputs":{"signal":"B","ma":"🟡","cycle_position":null,"cycle_verdict":null,"thesis_irreconcilable":false,"valuation_dependent":false,"market_wrong_reason_given":false,"momentum_overheated":false,"cycle_gates_pass":null,"wait_for_price":true,"wait_for_price_condition":"等股價收盤回到 296 美元以下（約 FY2027E 共識 15 倍），且 Walgreens、Evernorth 沒有新增移量。卡點是價格，基本面沒有破。"},"thesis":{"H":[{"id":"H1","text":"專科藥與醫師服務分部是成長引擎，營業利益維持中雙位數成長，占比逐年上升。","2y":"FY2027 分部營業利益成長 18–21%，FY2028 ≥ 13%","5y":"FY2031 占扣除 Other 後營業利益 ≥ 50%（FY2026 由指引反推約 41%）","10y":null,"threshold":"FY2027 低於 15%，或 FY2028 起任兩季低於 10%","source":"Cencora 季報新分部（FY2027 Q1 起）、2026-11-04 法說指引、分部重編 8-K","drift_rule":"2 年論點連 2 季偏離 ≥ 5% 算削弱，連 3 季偏離 ≥ 10% 算反轉；5 年論點連 4 季偏離 ≥ 5% 算削弱，連 6 季偏離 ≥ 10% 算反轉。"},{"id":"H2","text":"藥品配送與服務是現金底盤，扣掉客戶移量與匯率後仍能維持中個位數營業利益成長。","2y":"FY2027 分部營業利益成長 ≥ 2%，FY2028 ≥ 4%","5y":"FY2027–FY2031 平均年增 ≥ 4%","10y":null,"threshold":"FY2027 低於 2%，或 FY2028 低於 3%","source":"Cencora 季報新分部、2026-11-04 法說指引","drift_rule":"2 年論點連 2 季偏離 ≥ 5% 算削弱，連 3 季偏離 ≥ 10% 算反轉；5 年論點連 4 季偏離 ≥ 5% 算削弱，連 6 季偏離 ≥ 10% 算反轉。"},{"id":"H3","text":"調整後 EPS 有現金支撐，併購賺得回資本成本。","2y":"FY2027 調整後 FCF ≥ 35 億美元，約為調整後淨利 ≥ 90%","5y":"五年累計 FCF ÷ 調整後淨利 ≥ 90%，MSO 併購沒有大額減損","10y":null,"threshold":"FY2027 調整後 FCF 低於 30 億美元，或單筆商譽減損 ≥ 5 億美元","source":"季報現金流量表、年報商譽附註、法說資本配置段","drift_rule":"2 年論點連 2 季偏離 ≥ 5% 算削弱，連 3 季偏離 ≥ 10% 算反轉；5 年論點連 4 季偏離 ≥ 5% 算削弱，連 6 季偏離 ≥ 10% 算反轉。"}],"R":[{"id":"R1","text":"Walgreens 與 Boots 繼續移出量體，或財務惡化。私有化後評等撤銷，外界只能看公司揭露。","h_ref":"H2","clock":"⚡","threshold":"主協議終止或破產 → 清倉；再揭露移量、FY2027 10-K 占營收低於 20%，或占應收高於 45% → 減碼三分之一","evidence_refs":["customer_concentration_credit#0","customer_concentration_credit#1","customer_concentration_credit#2","customer_concentration_credit#3"]},{"id":"R2","text":"Evernorth（占營收約 13%）量體流失：Cigna 新設批發配送，法說未點名的大型郵購客戶連三季下滑。","h_ref":"H2","clock":"🔥","threshold":"10-K 占營收由 13% 降到 9% 以下，或公司確認協議縮減 → 減碼三分之一","evidence_refs":["customer_second_source#0"]},{"id":"R3","text":"Part B 給付、ASP 規則與 340B 改變專科經濟，管理層尚未量化。","h_ref":"H1","clock":"🐢","threshold":"規則定案後公司量化的分部營業利益衝擊 ≥ 5%，或專科分部毛利率連 2 季年減 → 減碼三分之一","evidence_refs":["regulatory_antitrust#0"]},{"id":"R4","text":"併購賺不回資本成本。OneOncology 首年 EPS 中性，PharmaLex 已減損 7.239 億美元，後面還有兩筆交易。","h_ref":"H3","clock":"🔥","threshold":"OneOncology 滿 24 個月（2028-02）仍無正 EPS 貢獻，或單筆商譽減損 ≥ 5 億美元 → 停止加碼","evidence_refs":[]},{"id":"R5","text":"關稅、學名藥通縮與供應鏈法規成本吸收不了。","h_ref":"H2","clock":"🐢","threshold":"配送分部營收成長減營業利益成長連 4 季大於 3 個百分點，且管理層歸因成本 → 減碼三分之一","evidence_refs":["reg_tariff_export#0","reg_tariff_export#1","regulatory_antitrust#0"]}],"single_thing":{"description":"Walgreens 主供應商協議終止，或 Walgreens 申請破產。","why_fatal":"Walgreens 與 Boots 合計約占 FY2025 營收 25%、應收帳款 38%，是最大的單一營收與信用敞口。協議終止會同時砍營收並拖累配送規模效益，破產還要加上應收減損。應收金額與該客戶利潤占比事實表未涵蓋，衝擊只能按比例粗估。","if_happens":"清倉，等應收損失金額和替代量體確定後再重做研究。參考跌幅是 Max DD 深端 −40%，加上應收減損可到 −50%。","how_monitor":"8-K 客戶揭露、FY2026 與 FY2027 10-K 的營收與應收占比、法說對移量的說法。私有化後 Walgreens 沒有公開季報，這是監測盲區。","probability":"12 至 24 個月約 8%。這是判斷值，沒有評等或違約資料可以校準。"}},"appendix_a":{"growth_durability":6,"quality_score":9,"ai_risk":"🟢","long_term_confidence":"中","fpe_fy2":15.21,"peg_fy2":1.44,"stress":{"pass":null,"total":null}},"eps_meta":{"base_eps_path":{"FY2026A":17.97,"FY2027E":19.7,"FY2028E":21.93,"FY2029E":24.27},"fy_end_month":9,"eps_basis":"調整後稀釋 EPS，財年 9 月底；FY2026A 來自 2026-11-04 法說，FY2027–FY2029 為 Koyfin 2026-11-07 共識快照，分析師家數事實表未涵蓋。"},"catalysts":[{"date":"2026-11","date_precision":"month","type":"other","event":"FY2026 10-K 申報","impact":"高","watch":"Walgreens、Boots 與 Evernorth 的營收和應收占比"},{"date":"2026-12","date_precision":"quarter","type":"other","event":"Profarma 股權出售預計於 FY2027 第一季完成","impact":"低","watch":"營收減少幅度是否符合指引"},{"date":"2027-02","date_precision":"month","type":"guidance","event":"FY2027 Q1 財報，新分部第一次實績","impact":"高","watch":"Q1 調整後 EPS 對約 4.55 美元，專科分部營業利益成長"},{"date":"2027-03","date_precision":"quarter","type":"regulatory","event":"MWI 與 Covetrus 合併假設於 FY2027 年中交割，FTC 審查中","impact":"中","watch":"FTC 結果與交割時點，EPS 影響約 0.35 美元"},{"date":"2028-01","date_precision":"quarter","type":"regulatory","event":"2028 年 IRA 延伸到 Part B（2026-08-05 法說提及）","impact":"高","watch":"專科診所給付與管理層是否量化影響"}],"decision_out":{"verdict":"觀望","role":"追蹤","row_hit":"8w(原9)","pacing":[],"holding_cap":null,"audit_rows":[{"row":"1","condition":"基本面評級 signal = X → 迴避","hit":false,"basis":"signal='B'"},{"row":"2","condition":"§11 強制裁決：thesis 不可調和不成立 → 迴避","hit":false,"basis":"thesis_irreconcilable=False"},{"row":"3","condition":"moat_trend ↓（§5）且 moat 等級 ≤ B → 迴避","hit":false,"basis":"moat_trend='→', moat='B'"},{"row":"4","condition":"週線結構趨勢過濾 ❌（附錄 A：價 < W250 或 W250 斜率轉負）","hit":false,"basis":"ma='🟡'"},{"row":"5","condition":"動能過熱（RSI 14d > 70 或 4 週漂移 > +10%，附錄 A）","hit":false,"basis":"momentum_overheated=False"},{"row":"6","condition":"基本面評級 signal = C → ≥ 觀望","hit":false,"basis":"signal='B'"},{"row":"7","condition":"runway_post_y5 = 🔴（§6.A''）→ ≥ 觀望（§13c ≤ 3Y 警示）","hit":false,"basis":"runway_post_y5='🟡'"},{"row":"7a","condition":"§10.6 標記「估值依賴型」且 §11 未給出「市場錯在哪」的具體理由 → ≥ 觀望，且持有年限上限中期 2-5 年","hit":false,"basis":"valuation_dependent=False, market_wrong_reason_given=False"},{"row":"7b","condition":"dd-meta capalloc_grade = C（DD 未提供 → N/A 不觸發）→ 持有年限上限中期 2-5 年（不降裁決）","hit":false,"basis":"capalloc_grade='B'"},{"row":"8a","condition":"無 Veto(6/7/7a) + signal≥B + runway_post_y5=🟢 + 26週漲幅<100%(邊界100-150%裁量) + 非估值依賴型 + moat_trend≠↓ + val∈{🟠,🔴} → 進場·條件式（爆發候選）","hit":false,"basis":"signal='B', runway='🟡', val='🟡', moat_trend='→', week26=28.3, valuation_dependent=False"},{"row":"8b","condition":"無 Hard Veto + archetype∈循環子型 + cycle_position∈{深谷投降／早循環} + QC-42反動能五閘全過 + moat底線（≠X 且非「↓且C」）→ 進場·條件式（循環衛星）","hit":false,"basis":"archetype='品質複利成長', cycle_position=None, moat='B', moat_trend='→', cycle_gates_pass=None"},{"row":"11.4b-denom","condition":"§11 4b.1 分母爭議檢查成立 → val 燈判定不可用（否則沿用機械讀數）","hit":false,"basis":"val_denominator_disputed=False"},{"row":"8","condition":"無 Hard Veto + signal≥B + val∈{🟠,🔴} → 觀望（等估值）","hit":false,"basis":"signal='B', val='🟡'"},{"row":"9","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟢,✅,🟡} → 進場","hit":true,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"9b","condition":"無 Veto + signal≥B + val≤🟡 + MA∈{🟠,-}（價<W104 但>W250，或樣本不足）→ 進場·條件式（長波段佈局）","hit":false,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"10","condition":"無 Veto + signal≥A + MA∈{🟢,✅,🟡} + val∈{🟢,🟡} → 進場","hit":false,"basis":"signal='B', val='🟡', ma='🟡'"},{"row":"8w","condition":"判斷者宣告 wait_for_price（價格合理但要等）→ 原 row9 進場改觀望（等價格）","hit":true,"basis":"wait_for_price=True, 等待條件='等股價收盤回到 296 美元以下（約 FY2027E 共識 15 倍），且 Walgreens、Evernorth 沒有新增移量。卡點是價格，基本面沒有破。'"},{"row":"QC-49","condition":"90 天內翻面須引前次已發火觸發器，否則承繼前次裁決","hit":false,"basis":"輸入缺(qc49_inherit_prior=null)，依保守方向處理：不套用（維持矩陣機械輸出）","input_gap":["qc49_inherit_prior"]},{"row":"role-held_now","condition":"觀望→role 預設追蹤，除非 held_now=True 沿用 prior_role","hit":false,"basis":"輸入缺(held_now=null)，依保守方向處理：維持預設追蹤","input_gap":["held_now"]}],"requires_critic":[]}}
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
